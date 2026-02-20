import matplotlib.pyplot as plt
import numpy as np
import os

# Data from Experiment 46 manual runs
lattice_sizes = [10, 20, 30, 60]
core_energies = [24.52, 25.46, 29.54, 29.98]

# Theoretical Prediction (from Emergent Standard Model)
prediction = 30.0

plt.figure(figsize=(10, 6))
plt.plot(lattice_sizes, core_energies, 'bo-', linewidth=2, markersize=8, label='Simulation Result')
plt.axhline(y=prediction, color='r', linestyle='--', linewidth=2, label='Prediction (30 GeV)')

plt.xlabel('Lattice Dimension (L)', fontsize=12)
plt.ylabel('Monopole Core Energy (Mass Units)', fontsize=12)
plt.title('Convergence of Entropic Monopole Mass', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.ylim(20, 35)

# Annotate the final point
plt.annotate(f'{core_energies[-1]:.2f} Units', 
             xy=(lattice_sizes[-1], core_energies[-1]), 
             xytext=(lattice_sizes[-1]-10, core_energies[-1]-3),
             arrowprops=dict(facecolor='black', shrink=0.05))

output_path = "results/monopole_convergence.png"
os.makedirs("results", exist_ok=True)
plt.savefig(output_path)
print(f"Convergence plot saved to {output_path}")
