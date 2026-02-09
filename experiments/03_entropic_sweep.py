import numpy as np
import sys
import os

# Ensure local package is findable
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.solver import SimulationRunner
from ukft_sim.vis import plot_simulation_results, save_plots_to_html

def run_experiment(target_alpha):
    print(f"--- Running Sweep for Alpha = {target_alpha} ---")
    
    # Config
    N = 201 
    L_phys = 60.0 
    # Use fewer particles/ticks for sweep speed if needed, but we want high quality
    runner = SimulationRunner(N=N, L_phys=L_phys, T_ticks=500, M_particles=1000, alpha_entropic=target_alpha)

    # 1. Define Double Slit Potential (Same as Experiment 02)
    V_high = 20.0 
    barrier_pos = 0.0 
    barrier_width = 2.0
    slit_width = 1.5
    slit_separation = 4.0

    x_grid = runner.x_grid
    potential_barrier = np.zeros(N)

    in_barrier_range = (x_grid > barrier_pos - barrier_width/2) & (x_grid < barrier_pos + barrier_width/2)
    slit_1_center = barrier_pos - slit_separation/2
    slit_2_center = barrier_pos + slit_separation/2
    in_slit_1 = np.abs(x_grid - slit_1_center) < slit_width/2
    in_slit_2 = np.abs(x_grid - slit_2_center) < slit_width/2

    mask_barrier = in_barrier_range & ~(in_slit_1 | in_slit_2)
    potential_barrier[mask_barrier] = V_high

    # 2. Initial State: Gaussian Packet
    width = 3.0
    k0 = 2.0 
    psi0 = np.exp(-(x_grid + L_phys/3)**2 / (2*width**2)) * np.exp(1j * k0 * x_grid)
    psi0 /= np.linalg.norm(psi0)

    # Run
    results = runner.run(psi0, potential_barrier=potential_barrier)

    # Visualize
    figs = plot_simulation_results(
        results['x_grid'], 
        results['choice_indices'], 
        results['history_rho'], 
        results['history_pos'], 
        results['history_time'],
        L_phys,
        runner.alpha_entropic,
        runner.dt_base,
        title_prefix=f"Sweep (Alpha={target_alpha})"
    )

    filename = os.path.join('results', f'03_sweep_alpha_{target_alpha}.html')
    
    description = f"""
    <h3>Entropic Gravity Sweep: Alpha = {target_alpha}</h3>
    <p><strong>Observation Goal:</strong> Observe how increasing the entropic gravity parameter sharpens the 'choice veins'.</p>
    <ul>
        <li><strong>Alpha = 0.0:</strong> Pure Bohmian Mechanics (Standard Quantum Potential). Trajectories should be smoother, less clustered.</li>
        <li><strong>Alpha > 0.0:</strong> UKFT Choice Dynamics. Particle paths 'collapse' towards high-density history ridges (Success Bias).</li>
    </ul>
    """

    save_plots_to_html(
        filename, 
        figs, 
        f"PROPHET EXPERIMENT 03: Entropic Sweep (α={target_alpha})", 
        description
    )
    print(f"Saved to {filename}")

if __name__ == "__main__":
    # Sweep values: Control (0), Moderate (5), Strong (15)
    alphas_to_test = [0.0, 5.0, 15.0]
    
    for alpha in alphas_to_test:
        run_experiment(alpha)
