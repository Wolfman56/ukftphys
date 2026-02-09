import numpy as np
import sys
import os

# Ensure local package is findable
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.solver import SimulationRunner
from ukft_sim.vis import plot_heatmap_with_contours

# Config
N = 151 # Reduced resolution for speed
L_phys = 60.0 # Wider domain

# "Standard" Entropic Parameter (UKFT Paper 34)
alpha_entropic = 2.0 
T_ticks = 300 # Reduced for quick verification
dt_base = 0.2 

runner = SimulationRunner(
    N=N, 
    L_phys=L_phys, 
    T_ticks=T_ticks, 
    M_particles=500, # Fewer particles
    dt_base=dt_base,
    alpha_entropic=alpha_entropic
)

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
width = 3.0
k0 = 2.0 # Slightly higher momentum to penetrate/diffract
psi0 = np.exp(-(x_grid + L_phys/3)**2 / (2*width**2)) * np.exp(1j * k0 * x_grid)
psi0 /= np.linalg.norm(psi0)

# Run
print(f"Running Entropic Double Slit Experiment (alpha={alpha_entropic}, dt={dt_base})...")
results = runner.run(psi0, potential_barrier=potential_barrier)

# Visualize with new Heatmap + Contours
output_filename = os.path.join('results', 'ukft_choice_guided_double_slit.html')

print(f"Generating Visualization: {output_filename}")
plot_heatmap_with_contours(
    results['history_pos'],
    results['history_rho'],
    alpha_entropic=alpha_entropic,
    filename=output_filename
)

print("Experiment 03 Complete.")
