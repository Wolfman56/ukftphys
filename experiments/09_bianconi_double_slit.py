# experiments/09_bianconi_double_slit.py
"""
UKFT Bianconi Double Slit Experiment 🌌

Comparison of Wave Interference vs Trajectory Dynamics using 
Relative Entropy Force: F = alpha * grad(ln rho).

Unlike the standard experiment (F = alpha * grad rho), this force 
persists even in low density regions (dark fringes), potentially
altering the crossing behavior.
"""

import numpy as np
import scipy.linalg
import matplotlib.pyplot as plt
import os
import sys

# Add path to ukft_sim
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ukft_sim.solver import SimulationRunner
from ukft_sim.vis import plot_simulation_results, save_plots_to_html

# 1. Setup Simulation (Bianconi Mode)
L_phys = 50.0
N = 201
runner = SimulationRunner(N=N, L_phys=L_phys, T_ticks=150, M_particles=150, 
                          alpha_entropic=20.0, # High alpha to see effect clearly
                          force_type='bianconi') # NEW FLAG

# 2. Initial Wave Packet
x = runner.x_grid
sigma = 2.0
k0 = 2.0 # Forward momentum
psi0 = np.exp(-(x + 15)**2 / (2*sigma**2)) * np.exp(1j * k0 * x)
psi0 /= np.linalg.norm(psi0)

# 3. Double Slit Potential
V_pot = np.zeros(N)
# Barrier
barrier_idx = np.abs(x) < 2.0 # Width 4
V_pot[barrier_idx] = 20.0
# Slits
slit_width = 1.0
slit_sep = 3.0
slit_1 = (np.abs(x - slit_sep) < slit_width/2)
slit_2 = (np.abs(x + slit_sep) < slit_width/2)
V_pot[slit_1] = 0.0
V_pot[slit_2] = 0.0

# 4. Run Standard vs Bianconi check
# Wait, let's just run Bianconi here as requested.
results = runner.run(psi0, potential_barrier=V_pot)

# 5. Visualize
print("Generating Visualization...")
fig1, fig2, fig3 = plot_simulation_results(
    results['x_grid'], 
    results['choice_indices'], 
    results['history_rho'], 
    results['history_pos'], 
    results['history_time'], 
    L_phys, 
    runner.alpha_entropic, 
    runner.dt_base,
    title_prefix="Exp 09: Bianconi Double Slit"
)

# 6. Save
output_filename = "results/09_bianconi_double_slit.html"
save_plots_to_html(output_filename, [fig1, fig2, fig3], 
                   "Experiment 09: Bianconi Relative Entropy Double Slit",
                   "Evaluating the effect of grad(ln rho) force on interference trajectories.")
print(f"Results saved to {output_filename}")
