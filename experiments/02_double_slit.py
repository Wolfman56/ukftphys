import numpy as np
import sys
import os

# Ensure local package is findable
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.solver import SimulationRunner
from ukft_sim.vis import plot_simulation_results, save_plots_to_html

# Config
N = 251 # Slightly larger resolution
L_phys = 60.0 # Wider domain
runner = SimulationRunner(N=N, L_phys=L_phys, T_ticks=600, M_particles=1500, alpha_entropic=5.0)

# 1. Define Double Slit Potential
V_high = 20.0 # Height of barrier
barrier_pos = 0.0 # Center of barrier
barrier_width = 2.0
slit_width = 1.5
slit_separation = 4.0

x_grid = runner.x_grid
potential_barrier = np.zeros(N)

# Define Barrier Region
in_barrier_range = (x_grid > barrier_pos - barrier_width/2) & (x_grid < barrier_pos + barrier_width/2)

# Define Slits (holes in the barrier)
slit_1_center = barrier_pos - slit_separation/2
slit_2_center = barrier_pos + slit_separation/2

in_slit_1 = np.abs(x_grid - slit_1_center) < slit_width/2
in_slit_2 = np.abs(x_grid - slit_2_center) < slit_width/2

# Set Potential: High in barrier range, unless in a slit
mask_barrier = in_barrier_range & ~(in_slit_1 | in_slit_2)
potential_barrier[mask_barrier] = V_high

# 2. Initial State: Gaussian Packet centered to the LEFT, moving RIGHT towards barrier
# Start at -L_phys/4
width = 3.0
k0 = 2.0 # Slightly higher momentum to penetrate/diffract
psi0 = np.exp(-(x_grid + L_phys/3)**2 / (2*width**2)) * np.exp(1j * k0 * x_grid)
psi0 /= np.linalg.norm(psi0)

# Run
print(f"Running Double Slit Experiment (Barrier Height={V_high})...")
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
    title_prefix="Double Slit"
)

save_plots_to_html(
    os.path.join('results', '02_double_slit_results.html'), 
    figs, 
    "PROPHET EXPERIMENT 02: Double Slit Interference", 
    f"Choice-guided trajectories through a double slit barrier (V={V_high}). Note the branching in Choice Space."
)

print("Experiment 02 Complete. Saved to results/02_double_slit_results.html")
