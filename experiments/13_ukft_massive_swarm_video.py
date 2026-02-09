# experiments/13_ukft_massive_swarm_video.py
"""
Experiment 13: UKFT Massive Swarm Cinematic (GPU Rendering) 🎬

This experiment runs the Entropic Gravity simulation with 50,000 particles
and renders the output DIRECTLY on the GPU to a density buffer.

This bypasses the browser/Plotly bottleneck, allowing us to visualize
the full high-fidelity quantum swarm as a video sequence.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# Add package root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.gpu import EntropicGPUAccelerator

def create_perspective(fov_deg, aspect, near, far):
    f = 1.0 / np.tan(np.deg2rad(fov_deg) / 2)
    # Standard GL Perspective (Row Major for construction)
    # [ f/ar  0  0  0 ]
    # [ 0     f  0  0 ]
    # [ 0     0  A  B ]
    # [ 0     0 -1  0 ]
    A = (far + near) / (near - far)
    B = (2 * far * near) / (near - far)
    
    m = np.zeros((4, 4), dtype=np.float32)
    m[0,0] = f / aspect
    m[1,1] = f
    m[2,2] = A
    m[2,3] = B
    m[3,2] = -1.0
    
    return m

def look_at(eye, target, up):
    z = eye - target
    z /= np.linalg.norm(z)
    x = np.cross(up, z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    
    # View Matrix
    # [ Rx Ry Rz -dot(R,eye) ]
    m = np.eye(4, dtype=np.float32)
    m[0, :3] = x
    m[1, :3] = y
    m[2, :3] = z
    m[0, 3] = -np.dot(x, eye)
    m[1, 3] = -np.dot(y, eye)
    m[2, 3] = -np.dot(z, eye)
    
    return m

def run_cinematic_sim():
    print("🎬 Initializing Cinematic GPU Simulation...")
    gpu = EntropicGPUAccelerator()
    
    # Configuration
    N_swarm = 100_000 # Let's go for 100k! Plotly choked, but GPU won't.
    n_steps = 300
    width, height = 800, 600
    
    # Physics Config
    dt = 0.015
    alpha_param = 15.0 
    damping = 0.99
    sigma = 0.5
    
    # Initial State
    m_heavy = 15.0
    p1 = np.array([ 1.5,  0.0, 0.0])
    p2 = np.array([-1.5,  0.0, 0.0])
    v1 = np.array([ 0.0,  0.5, 0.0])
    v2 = np.array([ 0.0, -0.5, 0.0])
    
    # Particles: Disc + Random Cloud
    # 80% Disc
    n_disc = int(N_swarm * 0.8)
    theta = 2 * np.pi * np.random.rand(n_disc)
    r = 3.0 + 1.0 * np.random.randn(n_disc)
    z = 0.2 * np.random.randn(n_disc)
    
    pos_disc = np.zeros((n_disc, 3), dtype=np.float32)
    pos_disc[:, 0] = r * np.cos(theta)
    pos_disc[:, 1] = r * np.sin(theta)
    pos_disc[:, 2] = z
    
    vel_disc = np.zeros((n_disc, 3), dtype=np.float32)
    vel_disc[:, 0] = -r * np.sin(theta) * 0.6
    vel_disc[:, 1] =  r * np.cos(theta) * 0.6
    
    # 20% Uniform Cloud
    n_cloud = N_swarm - n_disc
    pos_cloud = (np.random.rand(n_cloud, 3) - 0.5) * 10
    vel_cloud = (np.random.rand(n_cloud, 3) - 0.5) * 0.2
    
    particles_pos = np.vstack([pos_disc, pos_cloud])
    particles_vel = np.vstack([vel_disc, vel_cloud])
    
    # Plotting Setup
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='black')
    ax.axis('off')
    img_display = ax.imshow(np.zeros((height, width)), cmap='magma', origin='upper', vmin=0, vmax=5)
    
    # Text overlay
    title_text = ax.text(0.5, 0.95, "UKFT Entropic Field: 100k Particles", 
                        transform=ax.transAxes, color='white', ha='center', fontsize=14)
    
    print(f"Starting Render Loop ({N_swarm} particles)...")
    
    def update(frame):
        nonlocal p1, p2, v1, v2, particles_pos, particles_vel
        
        # 1. Update Sources (Python)
        delta = p2 - p1
        dist = np.linalg.norm(delta)
        force = 5.0 * delta / (dist**3 + 1e-3)
        p1 += v1 * dt
        p2 += v2 * dt
        v1 += force * dt
        v2 -= force * dt
        
        sources = [(p1, m_heavy), (p2, m_heavy)]
        
        # 2. Update Physics (GPU)
        params = {'sigma': sigma, 'alpha': alpha_param, 'dt': dt, 'damping': damping}
        particles_pos, particles_vel = gpu.run_simulation_step(
            particles_pos, particles_vel, sources, params
        )
        
        # 3. Render (GPU)
        # Orbit Camera
        angle = frame * 0.02
        cam_dist = 12.0
        eye = np.array([np.cos(angle)*cam_dist, np.sin(angle)*cam_dist, 6.0])
        target = np.array([0, 0, 0])
        up = np.array([0, 0, 1])
        
        view = look_at(eye, target, up)
        proj = create_perspective(60, width/height, 0.1, 100.0)
        
        # Matrix multiply (Row Major logic matches numpy matmul, but we need to check WGPU order)
        # Proj * View * Model
        # In Python: mvp = proj @ view
        # We need to flatten it appropriately.
        # If we send Row-Major bytes to WGPU:
        # matrix[0] is row 0.
        # WGPU behaves as Column-Major if we declare `mat4x4`.
        # So we should send the TRANSPOSE of the python result.
        mvp = (proj @ view).T
        
        # Compute Density Image on GPU
        # Returns (H, W) float array of counts
        density_map = gpu.render_density_view(particles_pos, width, height, mvp)
        
        # Log compression for visibility
        visual_map = np.log1p(density_map)
        
        img_display.set_data(visual_map)
        title_text.set_text(f"Step {frame} | Particles: {N_swarm} | GPU Render")
        
        if frame % 20 == 0:
            print(f"Rendering frame {frame}/{n_steps}")
            
        return [img_display, title_text]

    print("Compiling animation...")
    ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=30, blit=True)
    
    out_path = "results/13_ukft_cinematic.mp4"
    # Try using ffmpeg if available, else gif
    try:
        ani.save(out_path, writer='ffmpeg', fps=30, dpi=100)
        print(f"Saved video to {out_path}")
    except Exception as e:
        alt_path = "results/13_ukft_cinematic.gif"
        print(f"FFMpeg failed ({e}), saving GIF to {alt_path}...")
        ani.save(alt_path, writer='pillow', fps=30)
        print(f"Saved GIF to {alt_path}")

if __name__ == "__main__":
    run_cinematic_sim()
