# experiments/14_ukft_perception_loop.py
"""
Experiment 14: UKFT Perception Feedback Loop 👁️

This experiment integrates the Physics Engine (EntropicGPUAccelerator)
with the Perception Engine (WebGPUPerceptionAccelerator).

It demonstrates the full UKFT loop:
1. Physics: Quantum Swarm moves under entropic gravity.
2. Reality: Density field is generated.
3. Perception: AI Observer analyzes the field "Coherence".
4. Feedback: We visualize the "Consciousness Field" (Coherence Map) 
   alongside the physical reality.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Add package root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.gpu import EntropicGPUAccelerator
from ukft_sim.perception import WebGPUPerceptionAccelerator

def run_perception_loop():
    print("🧠 Initializing UKFT Perception Loop...")
    
    # 1. Initialize Engines
    physics_engine = EntropicGPUAccelerator()
    perception_engine = WebGPUPerceptionAccelerator()
    
    # Configuration
    N_swarm = 50_000
    n_steps = 200
    width, height = 256, 256 # Coherence mapping grid size
    grid_range = [-4, 4]
    
    # Physics State
    dt = 0.02
    alpha = 12.0
    sigma = 0.6
    
    # Binary Star System
    m_heavy = 15.0
    p1 = np.array([ 1.5,  0.0, 0.0])
    p2 = np.array([-1.5,  0.0, 0.0])
    v1 = np.array([ 0.0,  0.5, 0.0])
    v2 = np.array([ 0.0, -0.5, 0.0])
    
    # Initialize Random Swarm (Ring)
    theta = 2 * np.pi * np.random.rand(N_swarm)
    r = 3.0 + 0.5 * np.random.randn(N_swarm)
    z = 0.5 * np.random.randn(N_swarm)
    particles_pos = np.zeros((N_swarm, 3), dtype=np.float32)
    particles_pos[:, 0] = r * np.cos(theta)
    particles_pos[:, 1] = r * np.sin(theta)
    particles_pos[:, 2] = z
    particles_vel = np.zeros_like(particles_pos)
    
    # Visualization Setup
    fig, (ax_real, ax_perc) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Reality Plot (Density)
    img_real = ax_real.imshow(np.zeros((height, width)), cmap='inferno', origin='lower',
                             extent=[grid_range[0], grid_range[1], grid_range[0], grid_range[1]])
    ax_real.set_title("Physical Reality (Density $\\rho$)")
    ax_real.axis('off')
    
    # Perception Plot (Coherence)
    img_perc = ax_perc.imshow(np.zeros((height, width)), cmap='viridis', origin='lower',
                             extent=[grid_range[0], grid_range[1], grid_range[0], grid_range[1]],
                             vmin=0.0, vmax=1.0)
    ax_perc.set_title("Observer Perception (Coherence $\\phi$)")
    ax_perc.axis('off')
    
    txt_info = fig.text(0.5, 0.05, "Initializing...", ha='center', color='white')
    fig.patch.set_facecolor('#111111')
    ax_real.tick_params(colors='white')
    ax_perc.tick_params(colors='white')
    
    print("Starting Simulation Loop...")
    
    def update(frame):
        nonlocal p1, p2, v1, v2, particles_pos, particles_vel
        
        # --- PHYSICS STEP ---
        # Update Orbital Sources
        delta = p2 - p1
        dist = np.linalg.norm(delta)
        force = 5.0 * delta / (dist**3 + 1e-3)
        p1 += v1 * dt; p2 += v2 * dt
        v1 += force * dt; v2 -= force * dt
        
        sources = [(p1, m_heavy), (p2, m_heavy)]
        
        # Update Particles
        params = {'sigma': sigma, 'alpha': alpha, 'dt': dt, 'damping': 0.98}
        particles_pos, particles_vel = physics_engine.run_simulation_step(
            particles_pos, particles_vel, sources, params
        )
        
        # Compute Density Field
        # We need the density grid for the Perception Engine
        x_range = grid_range
        y_range = grid_range
        rho_grid = physics_engine.compute_density_grid(
            width, height, x_range, y_range, sources, sigma
        )
        
        # Debug
        if frame % 20 == 0:
             print(f"DEBUG: rho min={rho_grid.min():.4f}, max={rho_grid.max():.4f}")
        
        # --- PERCEPTION STEP ---
        # Analyze the Coherence of the Density Field
        # UKFT Theory: Consciousness arises in regions of high coherence (low entropy gradient)
        # Coupling Strength determines how sensitive the observer is to disorder
        signatures = perception_engine.compute_spatial_signature(
            rho_grid, width, height, coupling_strength=8.0
        )
        
        # Extract components
        # layer 0: Energy, 1: Gradient, 2: Coherence
        coherence_map = signatures[:, :, 2]
        
        # --- VISUALIZATION ---
        img_real.set_data(rho_grid)
        img_real.set_clim(vmax=np.max(rho_grid)*0.8)
        
        img_perc.set_data(coherence_map)
        
        # Calculate Global Coherence Metric
        global_coherence = np.mean(coherence_map)
        txt_info.set_text(f"Step {frame} | Global Coherence: {global_coherence:.4f}")
        
        if frame % 20 == 0:
            print(f"Step {frame}: Coherence {global_coherence:.4f}")
            
        return [img_real, img_perc, txt_info]

    ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=50, blit=True)
    
    # Save as GIF using FFmpeg
    out_path = "results/14_ukft_perception_loop.gif"
    try:
        print(f"Saving animation to {out_path} using FFmpeg...")
        # FFmpeg writer works for .gif if the extension is provided
        ani.save(out_path, writer='ffmpeg', fps=30, dpi=100)
        print(f"Saved to {out_path}")
    except Exception as e:
        print(f"FFmpeg failed ({e}), falling back to Pillow...")
        ani.save(out_path, writer='pillow', fps=30)
        print(f"Saved to {out_path}")

if __name__ == "__main__":
    run_perception_loop()
