# experiments/exp32_void_scalar.py
"""
Experiment 32: The Void Scalar (Dark Energy as Vacuum Pressure) 🌌

Hypothesis: 
The "Void Scalar" (Particle 4) is not a particle in the traditional sense, but a 
topological defect manifesting as a 'bubble of nothing' in the Causal Graph.
While matter (Knots) pulls geometry inwards (Gravity), Voids push geometry outwards.
This repulsive pressure behaves exactly like Dark Energy ($\Lambda$).

Methodology:
1. Initialize a uniform 'Causal Sea' (flat spacetime).
2. Introduce a 'Void' (a region with constrained causal options / lower entropy).
3. Measure the pressure gradient: Does the Void collapse (Gravity) or expand (Dark Energy)?
4. Calculate the effective Cosmological Constant ($\Lambda$) from the expansion rate.

Expected Result:
Micro-voids should be unstable and collapse. 
However, macro-voids, or the collective effect of the "Choice Floor", should generate
a small, constant repulsive pressure corresponding to $\Lambda \approx 10^{-120}$ (in Planck units).
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Add package root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# We will use a simplified Lattice Boltzmann-like approach for Causal Flow
# to visualize the pressure gradients.

class CausalVoidSimulation:
    def __init__(self, size=64):
        self.size = size
        # Field: The "Choice Potential" (Phi). High = Many options, Low = Few.
        self.phi = np.ones((size, size, size)) * 1.0 
        # Gradients (Forces)
        self.force_field = np.zeros((size, size, size, 3))
        
    def create_void(self, radius=8, intensity=0.5):
        """Creates a spherical region of low choice potential (The Void)."""
        center = self.size // 2
        y, x, z = np.ogrid[-center:self.size-center, -center:self.size-center, -center:self.size-center]
        mask = x*x + y*y + z*z <= radius*radius
        
        # The Void has LOWER entropy/potential than the surroundings
        self.phi[mask] *= (1.0 - intensity)
        print(f"Void created at center with radius {radius} and depth {intensity}")

    def evolve_entropic_pressure(self, steps=200):
        """
         Simon Hossenfelder's "Zone of Avoidance" or the "Zero Point Energy" constraint.
         The vacuum cannot be truly empty. It has a 'ground state' of fluctuations.
         If Phi drops below Phi_min (The Vacuum Expectation Value), the system 
         MUST generate new links (Space Creation) to restore it. 
         This is the origin of Dark Energy (Lambda).
        """
        
        # History of Void Radius
        radii = []
        phi_min = 0.2  # The "Floor" of reality
        lambda_coupling = 0.05 # Strength of the creation operator
        
        print("\n--- Simulating Vacuum Dynamics ---")
        for t in range(steps):
            # 1. Compute Gradients (Standard Gravity/Diffusion)
            # F = grad(Phi) - flows from High to Low (filling the hole)
            laplacian = (np.roll(self.phi, 1, axis=0) + np.roll(self.phi, -1, axis=0) +
                         np.roll(self.phi, 1, axis=1) + np.roll(self.phi, -1, axis=1) +
                         np.roll(self.phi, 1, axis=2) + np.roll(self.phi, -1, axis=2) - 6*self.phi)
            
            # Gravity: Tries to normalize density (collapse void)
            self.phi += 0.05 * laplacian
            
            # 2. THE VOID SCALAR (Dark Energy Term)
            # If local potential is TOO LOW, the vacuum 'boils' to restore it.
            # Delta = Lambda * (Phi_min - Phi) where Phi < Phi_min
            vacuum_creation = np.maximum(0, phi_min - self.phi) * lambda_coupling
            
            # This creation pushes OUTWARD, acting as negative pressure
            self.phi += vacuum_creation
            
            # 3. Measure effective radius (where Phi drops below background)
            center = self.size // 2
            mid_slice = self.phi[center, center, :]
            # Void boundary where density is significantly lower than 1.0
            # We track the "event horizon" of the void
            void_mask = mid_slice < 0.8
            if np.any(void_mask):
                # Find the width of the hole
                indices = np.where(void_mask)[0]
                r = (indices[-1] - indices[0]) / 2.0
                radii.append(r)
            else:
                radii.append(0)
                
            if t % 20 == 0:
                print(f"Step {t}: Void Radius ~ {radii[-1]:.2f} | Max Vacuum Creation: {np.max(vacuum_creation):.5f}")

        return radii

    def visualize(self, radii):
        fig = plt.figure(figsize=(15, 6))
        
        # 1. Void Cross Section
        ax1 = fig.add_subplot(1, 2, 1)
        center = self.size // 2
        im = ax1.imshow(self.phi[center, :, :], cmap='twilight_shifted', vmin=0.5, vmax=1.5)
        ax1.set_title("Void Scalar Field Cross-Section ($\phi$)")
        plt.colorbar(im, ax=ax1)
        
        # 2. Dynamics
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.plot(radii, 'r-', linewidth=2, label='Void Radius')
        ax2.axhline(y=radii[0], color='gray', linestyle='--', label='Initial Size')
        ax2.set_xlabel("Time Step")
        ax2.set_ylabel("Effective Radius")
        ax2.set_title("Void Dynamics: Collapse vs Expansion")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/exp32_void_scalar.png')
        print("Detailed plot saved to results/exp32_void_scalar.png")

if __name__ == "__main__":
    print("Running Experiment 32: The Void Scalar Analysis...")
    sim = CausalVoidSimulation(size=64)
    sim.create_void(radius=10, intensity=0.8)
    
    # Run simulation
    radii = sim.evolve_entropic_pressure(steps=200)
    
    # Calculate 'effective lambda'
    # If slope is negative -> Gravity (Collapse)
    # If slope is positive -> Dark Energy (Expansion)
    delta_r = radii[-1] - radii[0]
    
    print("\n--- RESULTS ---")
    if delta_r < 0:
        print(f"Outcome: COLLAPSE (Gravity Dominates). Void shrunk by {-delta_r:.2f}")
    else:
        print(f"Outcome: EXPANSION (Dark Energy). Void grew by {delta_r:.2f}")
    
    sim.visualize(radii)
