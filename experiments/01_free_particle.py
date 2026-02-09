import numpy as np
import sys
import os

# Ensure local package is findable
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.solver import SimulationRunner
from ukft_sim.vis import plot_simulation_results, save_plots_to_html

# Config
N = 201
L_phys = 50.0
runner = SimulationRunner(N=N, L_phys=L_phys, T_ticks=400, M_particles=1000, alpha_entropic=5.0)

# Initial State: Gaussian Packet with Momentum
x_grid = runner.x_grid
width = 4.0
k0 = 1.5 
psi0 = np.exp(-(x_grid + L_phys/4)**2 / (2*width**2)) * np.exp(1j * k0 * x_grid)
psi0 /= np.linalg.norm(psi0)

# Run
results = runner.run(psi0)

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
    title_prefix="Free Particle"
)

save_plots_to_html(
    os.path.join('results', '01_free_particle_results.html'), 
    figs, 
    "PROPHET EXPERIMENT 01: Free Particle", 
    "Baseline test of discrete action minimization in free space."
)

print("Experiment 01 Complete. Saved to results/01_free_particle_results.html")
