
import numpy as np
import matplotlib.pyplot as plt
import torch
import sys
import os

# Add parent directory to path to import ukft_sim
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ukft_sim.gpu_solver import GPUSimulationRunner

def run_experiment_58():
    print("Running Experiment 58: 2D Entropic Scattering on GPU")
    
    # Parameters
    N = 256
    L = 20.0
    dt = 0.05
    steps = 400
    
    runner = GPUSimulationRunner(N=N, L=L)
    
    # 1. Initialize Wavepacket (Incident Particle)
    # Start on the left, moving right
    x0, y0 = -5.0, 0.0
    kx0, ky0 = 3.0, 0.0  # Momentum to the right
    sigma = 1.0
    
    runner.initialize_wavepacket(x0, y0, kx0, ky0, sigma)
    
    # 2. Define Entropic Monopole Potential
    # V(r) = alpha / r (softened) or Gaussian
    # The user mentioned "Entropic Monopole" which often implies a 1/r or similar potential
    # Let's use a softened Coulomb-like potential with an attractive/repulsive feature
    # Or purely entropic -> usually effectively attractive at long range.
    # Let's try a Gaussian potential well/barrier to represent the scattering center.
    
    def entropic_potential(X, Y):
        R = torch.sqrt(X**2 + Y**2)
        # Large central potential (Monopole)
        # Using a Soft-Core Coulomb: V = -Z / sqrt(r^2 + a^2)
        # Let's make it repulsive for scattering or attractive?
        # Scattering "off" a potential usually implies collision. 
        # A "Monopole" in some contexts is a topological defect.
        
        # Let's use a strong Gaussian barrier to see scattering clearly
        # V = V0 * exp(-r^2 / sigma_v^2)
        V0 = 50.0  # Height
        sigma_v = 1.5 # Width
        return V0 * torch.exp(-(X**2 + Y**2) / (2 * sigma_v**2))

    runner.set_potential(entropic_potential)
    
    print("Simulating...")
    
    # Capture frames
    import time
    start_time = time.time()
    
    initial_density = runner.get_density()
    
    # Run in batches
    for i in range(steps // 10):
        runner.step_trotter_2d(dt, steps=10)
        if i % 5 == 0:
            print(f"Step {i*10}/{steps}")
            
    end_time = time.time()
    print(f"Simulation completed in {end_time - start_time:.2f} seconds")
    
    final_density = runner.get_density()
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Initial
    im1 = axes[0].imshow(initial_density, extent=[-L/2, L/2, -L/2, L/2], origin='lower', cmap='inferno')
    axes[0].set_title("Initial Wavepacket")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    plt.colorbar(im1, ax=axes[0])
    
    # Final
    # Use log scale for scattering visibility if needed, but linear is fine for now
    im2 = axes[1].imshow(final_density, extent=[-L/2, L/2, -L/2, L/2], origin='lower', cmap='inferno')
    axes[1].set_title(f"Scattered State (t={steps*dt})")
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("y")
    plt.colorbar(im2, ax=axes[1])
    
    plt.tight_layout()
    output_path = "experiments/58_scattering_result.png"
    plt.savefig(output_path)
    print(f"Result saved to {output_path}")

if __name__ == "__main__":
    run_experiment_58()
