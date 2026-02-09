import numpy as np
import sys
import os
import plotly.graph_objects as go
from tqdm import tqdm

# Add package root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.physics import get_analytic_density_and_gradient
from ukft_sim.vis import create_3d_entropic_animation

def run_experiment():
    print("Running Experiment 07: Quantum Swarm on Entropic Gravity...")
    
    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------
    tmp_n_particles = 100
    n_steps = 600
    dt = 0.05
    animate_every = 5
    
    # Physics Parameters
    alpha_entropic = 20.0  # Strength of entropic force
    sigma = 1.2            # Spread of the source masses (and particles' view of them)
    m_source = 100.0       # Mass of the static sources
    
    # Static Sources (Two Gravity Wells)
    # Format: (Position, Mass)
    sources = [
        (np.array([-2.5, 0.0, 0.0]), m_source),
        (np.array([ 2.5, 0.0, 0.0]), m_source)
    ]
    
    # Initialize Particle Swarm
    # Start as a cloud above the center
    # Center (0, 3, 0)
    start_center = np.array([0.0, 3.0, 0.0])
    # Cloud spread
    spread = 0.8
    particles_pos = np.random.randn(tmp_n_particles, 3) * spread + start_center
    # Initial Velocities (Thermal/Random)
    particles_vel = np.random.randn(tmp_n_particles, 3) * 0.1
    
    # History Storage
    hist_pos = [particles_pos.copy()]
    
    # ---------------------------------------------------------
    # Simulation Loop
    # ---------------------------------------------------------
    for step in tqdm(range(n_steps), desc="Simulating Swarm"):
        current_positions = hist_pos[-1]
        next_positions = np.zeros_like(current_positions)
        
        # Update each particle
        for i in range(tmp_n_particles):
            pos = current_positions[i]
            vel = particles_vel[i]
            
            # 1. Calculate Field Info at current position
            # We treat the particle as a probe in the field of the two large sources
            rho, grad_rho = get_analytic_density_and_gradient(pos, sources, sigma)
            
            # 2. Entropic Force
            # F_ent = alpha * (grad_rho / rho)
            # Add epsilon to avoid divide by zero if far away
            eps_rho = 1e-12
            acc = alpha_entropic * grad_rho / (rho + eps_rho)
            
            # 3. Time Integration (Semi-implicit Euler / Damped)
            # Apply damping to simulate "probability fluid" viscosity or thermal loss
            damping = 0.98
            vel = vel * damping + acc * dt
            
            new_pos = pos + vel * dt
            
            # Floor bounce (optional, but keeps them on the 'sheet' if we want 2D-ish)
            # Letting them move in 3D for now.
            
            next_positions[i] = new_pos
            particles_vel[i] = vel
            
        hist_pos.append(next_positions)

    # ---------------------------------------------------------
    # Visualization
    # ---------------------------------------------------------
    print("Generating Visualization Frames...")
    
    # Grid for Surface Rendering (Space-Time Sheet)
    x_range = np.linspace(-6, 6, 60)
    y_range = np.linspace(-6, 6, 60)
    X, Y = np.meshgrid(x_range, y_range)
    
    # Precalculate static field for visualization background
    # Using Gaussian Well visualization to match physics
    dist1_sq = (X - sources[0][0][0])**2 + (Y - sources[0][0][1])**2
    dist2_sq = (X - sources[1][0][0])**2 + (Y - sources[1][0][1])**2
    rho_field = m_source * np.exp(-dist1_sq/(2*sigma**2)) + \
                m_source * np.exp(-dist2_sq/(2*sigma**2))
    Z_surf = -0.5 * rho_field # Scale for visual depth
    
    frames = []
    
    for step in range(0, n_steps, animate_every):
        pos_data = hist_pos[step]
        
        frame_data = [
            # 1. The Entropic Gravity Well (Static Surface)
            go.Surface(
                x=X, y=Y, z=Z_surf,
                colorscale='Viridis',
                opacity=0.5,
                showscale=False,
                name='Entropy Field'
            ),
            # 2. The Source Masses (Red Orbs)
            go.Scatter3d(
                x=[s[0][0] for s in sources],
                y=[s[0][1] for s in sources],
                z=[0, 0], # Sit on the plane
                mode='markers',
                marker=dict(color='red', size=20, symbol='circle'),
                name='Sources'
            ),
            # 3. The Quantum Swarm (Blue/Cyan Dots)
            go.Scatter3d(
                x=pos_data[:, 0],
                y=pos_data[:, 1],
                z=pos_data[:, 2],
                mode='markers',
                marker=dict(
                    color='cyan', 
                    size=4,
                    line=dict(width=0)
                ),
                name='Prob-Swarm'
            )
        ]
        
        frames.append(go.Frame(data=frame_data, name=str(step)))
        
    # Create Final Animation
    fig = create_3d_entropic_animation(
        frames,
        title="Exp 07: Quantum Swarm on Entropic Field",
        ranges={'x':[-6,6], 'y':[-6,6], 'z':[-10, 5]}
    )
    
    # Save Results
    results_dir = os.path.join(os.path.dirname(__file__), '../results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Static Image (Final Frame)
    try:
        fig.update(data=frames[-1].data)
        fig.write_image(os.path.join(results_dir, "07_quantum_swarm.png"))
    except:
        pass
        
    # Interactive HTML (Reset to start)
    fig.update(data=frames[0].data)
    out_file = os.path.join(results_dir, "07_quantum_swarm.html")
    fig.write_html(out_file)
    print(f"Simulation saved to {out_file}")

if __name__ == "__main__":
    run_experiment()
