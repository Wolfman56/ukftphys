# experiments/12_ukft_massive_swarm_gpu.py
"""
UKFT Massive Quantum Swarm (GPU Accelerated) 🚀

Simulates 50,000 quantum test particles surfing the entropic gravity field
of a binary star system.

Powered by WGPU Entropic Accelerator.
"""

import numpy as np
import sys
import os
import wgpu

# Add package root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.gpu import EntropicGPUAccelerator
from ukft_sim.vis import create_3d_entropic_animation
import plotly.graph_objects as go

def run_simulation():
    print("Initializing GPU Accelerator...")
    gpu = EntropicGPUAccelerator()
    
    # Configuration
    N_swarm = 50_000 # Massive Scale
    n_steps = 400
    animate_every = 4
    dt = 0.01
    
    # Physics Parameters
    alpha = 12.0
    hbar = 0.5
    # Effective alpha for combined Quantum + Entropic drift
    # v ~ 0.5 * (alpha + hbar^2) * grad_rho/rho
    # GPU shader implements: acc = alpha_param * grad_rho / rho
    # We want velocity update. If high damping, acc -> vel/dt. 
    # Let's keep inertial dynamics (damping < 1.0) for swirling.
    alpha_param = 12.0 
    damping = 0.98
    sigma = 0.6 # Sharper wells
    
    # Initial State: Binary System Sources
    # We will animate sources manually in Python loop (cheap)
    m_heavy = 15.0
    p1 = np.array([ 1.5,  0.0, 0.0])
    p2 = np.array([-1.5,  0.0, 0.0])
    v1 = np.array([ 0.0,  0.5, 0.0])
    v2 = np.array([ 0.0, -0.5, 0.0])
    
    # Initial State: Swarm (Ring)
    theta = 2 * np.pi * np.random.rand(N_swarm)
    r = 3.5 + 0.5 * np.random.randn(N_swarm)
    z = 0.5 * np.random.randn(N_swarm)
    
    particles_pos = np.zeros((N_swarm, 3), dtype=np.float32)
    particles_pos[:, 0] = r * np.cos(theta)
    particles_pos[:, 1] = r * np.sin(theta)
    particles_pos[:, 2] = z
    
    # Velocity (Tangential)
    particles_vel = np.zeros((N_swarm, 3), dtype=np.float32)
    particles_vel[:, 0] = -r * np.sin(theta) * 0.5
    particles_vel[:, 1] =  r * np.cos(theta) * 0.5
    
    frames = []
    
    # Grid for visualization (computed on GPU!)
    grid_res = 128 # Higher res grid
    x_range = [-5, 5]
    y_range = [-5, 5]
    X_grid, Y_grid = np.meshgrid(
        np.linspace(x_range[0], x_range[1], grid_res),
        np.linspace(y_range[0], y_range[1], grid_res)
    )
    
    print(f"Starting Simulation ({N_swarm} particles)...")
    
    for step in range(n_steps):
        if step % 50 == 0:
            print(f"Step {step}/{n_steps}")
            
        # Update Sources (Classical Orbit - Python side is fine for 2 bodies)
        # Attraction between stars
        delta = p2 - p1
        dist = np.linalg.norm(delta)
        force = 5.0 * delta / (dist**3 + 1e-3) # Standard Gravity for stars
        # Or Entropic? Let's use simple logic for stars to keep them orbiting
        p1 += v1 * dt
        p2 += v2 * dt
        v1 += force * dt
        v2 -= force * dt
        
        # Prepare Sources for GPU
        sources = [
            (p1, m_heavy),
            (p2, m_heavy)
        ]
        
        # Run Swarm on GPU
        params = {
            'sigma': sigma,
            'alpha': alpha_param,
            'dt': dt,
            'damping': damping
        }
        
        particles_pos, particles_vel = gpu.run_simulation_step(
            particles_pos, particles_vel, sources, params
        )
        
        # Visualization Frame
        if step % animate_every == 0:
            # 1. Compute Density Grid on GPU
            # We want to visualize the potential Z ~ -rho
            rho_grid = gpu.compute_density_grid(
                grid_res, grid_res, x_range, y_range, sources, sigma
            )
            Z_surf = -3.0 * rho_grid # Scale for visuals
            
            # 2. Downsample particles for plotting (WebGPU handles 50k, Plotly struggles with >5k)
            # Plot 3000 representative particles
            mask = np.random.choice(N_swarm, 3000, replace=False)
            plot_pos = particles_pos[mask]
            
            frame_data = [
                # Entropic Sheet
                go.Surface(
                    x=X_grid, y=Y_grid, z=Z_surf,
                    colorscale='Viridis', opacity=0.6, showscale=False,
                    name='SpaceTime'
                ),
                # Stars
                go.Scatter3d(
                    x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
                    mode='markers', marker=dict(color=['cyan', 'magenta'], size=15),
                    name='Sources'
                ),
                # Swarm
                go.Scatter3d(
                    x=plot_pos[:, 0], y=plot_pos[:, 1], z=plot_pos[:, 2],
                    mode='markers', 
                    marker=dict(color='yellow', size=2, opacity=0.5),
                    name='Quantum Swarm'
                )
            ]
            frames.append(go.Frame(data=frame_data, name=str(step)))
            
    # Finalize
    print("Generating Animation...")
    fig = create_3d_entropic_animation(
        frames,
        title=f"UKFT Massive Swarm ({N_swarm} Particles) - GPU Accelerated",
        ranges={'x': [-5,5], 'y':[-5,5], 'z':[-15, 5]}
    )
    
    out_file = "results/12_ukft_massive_swarm_gpu.html"
    fig.write_html(out_file)
    print(f"Saved to {out_file}")
    
    # PNG Snapshot
    try:
        fig.update(data=frames[-1].data)
        fig.write_image("experiments/12_ukft_massive_swarm_gpu.png")
    except:
        pass

if __name__ == "__main__":
    run_simulation()
