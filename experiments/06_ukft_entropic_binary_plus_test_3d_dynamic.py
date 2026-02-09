# experiments/06_ukft_entropic_binary_plus_test_3d_dynamic.py
"""
UKFT Entropic Gravity Demo — GO BIG OR GO HOME EDITION 🔥

All three upgrades combined:
1. Pure entropic attraction (no Newtonian force): mutual "gravity" from knowledge density ρ
   (sum of Gaussians at heavy masses). Acceleration ∝ ∇ρ toward higher coherence.
2. Light test particle (tiny back-reaction) spiraling in / orbiting the binary system.
3. Fully dynamic rubber sheet: recomputed every frame from current ρ — space-time warps live!

Visual: Two heavy "knowledge centers" in stable orbit via teleological entropic pull,
        light test particle falling in with trail, sheet curving dynamically.
"""

import numpy as np
import plotly.graph_objects as go
import os
import sys

# Ensure local package is findable
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ukft_sim.vis import create_3d_entropic_animation

# Parameters — tune for chaos or stability
sigma = 0.2                # Gaussian width (knowledge spread) — smaller = sharper 1/r-like attraction
alpha_entropic = 8.0       # Overall strength — higher = tighter orbits / faster infall
m_heavy = 10.0             # "Mass" scaling for heavy particles' ρ contribution
m_test = 0.1               # Tiny back-reaction from test particle (set 0 for none)
dt = 0.01                  # Time step
n_steps = 2000             # Long run for full spirals
animate_every = 10         # Frame skip for smoother animation / file size
z_scale = 0.5              # Visual depth scaling for sheet

# Initial positions (Prescribed Orbit for heavy, dynamic for test)
radius_orbit = 1.2
omega = 1.0  # Angular velocity for heavy particles
pos_h1 = np.array([ radius_orbit,  0.0, 0.0])
pos_h2 = np.array([-radius_orbit,  0.0, 0.0])
pos_test = np.array([0.1, 2.5, 0.2])   # Start "off-axis"

vel_h1 = np.zeros(3) # Not used
vel_h2 = np.zeros(3) # Not used
vel_test = np.array([-0.8, -0.2, 0.0])  # Inward trajectory

# Storage
positions_h1 = [pos_h1.copy()]
positions_h2 = [pos_h2.copy()]
positions_test = [pos_test.copy()]

# Grid for dynamic sheet (static grid, recompute Z per frame)
# Reduced grid size for better browser performance with animations
grid_size = 40
x_grid = np.linspace(-3, 3, grid_size)
y_grid = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x_grid, y_grid)

# Animation frames storage
frames = []

print("Running UKFT entropic 3-body simulation — this will take a moment...")

for step in range(n_steps):
    if step % 200 == 0:
        print(f"Step {step}/{n_steps}")
    
    # Update Heavy Particles (Prescribed Rotation)
    t = step * dt
    angle = omega * t
    
    # Heavy 1: Counter-clockwise
    new_p1 = np.array([
        radius_orbit * np.cos(angle),
        radius_orbit * np.sin(angle),
        0.05 * np.sin(3*angle) 
    ])
    
    # Heavy 2: Counter-clockwise (opposite phase)
    new_p2 = np.array([
        radius_orbit * np.cos(angle + np.pi),
        radius_orbit * np.sin(angle + np.pi),
        0.05 * np.sin(3*angle + np.pi)
    ])

    # Update Test Particle (Dynamic)
    pt = positions_test[-1]
    
    # Knowledge density ρ at each particle position (sum of Gaussians)
    def rho_at(pos, sources=[(new_p1, m_heavy), (new_p2, m_heavy)]):
        rho = 0.0
        for src_pos, m_src in sources:
            dist2 = np.sum((pos - src_pos)**2) + 1e-8
            rho += m_src * np.exp(-dist2 / (2 * sigma**2))
        return rho
    
    rho_t = rho_at(pt, sources=[(new_p1, m_heavy), (new_p2, m_heavy)])
    
    # Gradient ∇ρ ≈ direction to higher density
    def grad_rho_at(pos, sources):
        grad = np.zeros(3)
        eps = 1e-6
        for i in range(3):
            delta = np.zeros(3)
            delta[i] = eps
            grad[i] = (rho_at(pos + delta, sources) - rho_at(pos - delta, sources)) / (2 * eps)
        return grad
    
    grad_t = grad_rho_at(pt, sources=[(new_p1, m_heavy), (new_p2, m_heavy)])
    
    # Acceleration = alpha * ∇ρ (toward higher coherence / lower entropy)
    acc_t = alpha_entropic * grad_t
    
    # Damping
    vel_test *= 0.995

    # Euler update
    vel_test += acc_t * dt
    new_pt = pt + vel_test * dt
    
    positions_h1.append(new_p1)
    positions_h2.append(new_p2)
    positions_test.append(new_pt)
    
    # Build frame every N steps
    if step % animate_every == 0 or step == n_steps - 1:
        # Dynamic sheet from current positions
        dist1 = np.sqrt((X - new_p1[0])**2 + (Y - new_p1[1])**2 + 1e-6)
        dist2 = np.sqrt((X - new_p2[0])**2 + (Y - new_p2[1])**2 + 1e-6)
        dist_t = np.sqrt((X - new_pt[0])**2 + (Y - new_pt[1])**2 + 1e-6)
        
        # Calculate Depth (Visual Mass Boost for Test Particle = 2.0)
        Z = -z_scale * (m_heavy / dist1 + m_heavy / dist2 + 2.0 / dist_t)
        
        # Clamp Z for visibility (prevent infinite spikes)
        Z = np.maximum(Z, -20)
        
        frame_data = [
            # Dynamic sheet
            go.Surface(x=X, y=Y, z=Z, 
                       colorscale='viridis', 
                       # Dynamic Range: -20 (deep well) to 0 (flat space)
                       cmin=-20, cmax=0,
                       opacity=0.8, 
                       showscale=False),
            # Trails
            go.Scatter3d(x=[p[0] for p in positions_h1], y=[p[1] for p in positions_h1], z=[p[2] for p in positions_h1],
                         mode='lines', line=dict(color='cyan', width=8), name='Heavy 1 trail'),
            go.Scatter3d(x=[p[0] for p in positions_h2], y=[p[1] for p in positions_h2], z=[p[2] for p in positions_h2],
                         mode='lines', line=dict(color='magenta', width=8), name='Heavy 2 trail'),
            go.Scatter3d(x=[p[0] for p in positions_test], y=[p[1] for p in positions_test], z=[p[2] for p in positions_test],
                         mode='lines', line=dict(color='yellow', width=6), name='Test particle trail'),
            # Current positions
            go.Scatter3d(x=[new_p1[0]], y=[new_p1[1]], z=[new_p1[2]], mode='markers',
                         marker=dict(size=14, color='cyan'), name='Heavy 1'),
            go.Scatter3d(x=[new_p2[0]], y=[new_p2[1]], z=[new_p2[2]], mode='markers',
                         marker=dict(size=14, color='magenta'), name='Heavy 2'),
            go.Scatter3d(x=[new_pt[0]], y=[new_pt[1]], z=[new_pt[2]], mode='markers',
                         marker=dict(size=10, color='yellow'), name='Test particle'),
            # Centroid
            go.Scatter3d(x=[0], y=[0], z=[0], mode='markers',
                         marker=dict(size=8, color='white', symbol='x'), name='Centroid')
        ]
        frames.append(go.Frame(data=frame_data, name=str(step)))

positions_h1 = np.array(positions_h1)
positions_h2 = np.array(positions_h2)
positions_test = np.array(positions_test)

# Final figure
fig = create_3d_entropic_animation(
    frames, 
    title="UKFT Entropic Gravity — Binary + Test Particle on Dynamically Warped Space-Time Sheet"
)

# SNAPSHOT: Use the LAST frame for the PNG
print("Generating static preview (using final frame)...")
original_data = fig.data
fig.update(data=frames[-1].data)

output_file = os.path.join("results", "06_ukft_entropic_binary_plus_test_3d_dynamic.html")
png_file = output_file.replace(".html", ".png")

try:
    fig.write_image(png_file)
    print(f"Saved plot image to {png_file}")
except Exception as e:
    print(f"Could not save PNG: {e}")

# REVERT to Frame 0 for HTML
print("Generating interactive HTML...")
fig.update(data=original_data)
fig.write_html(output_file)

print(f"UKFT entropic 3-body complete. Saved to {output_file}")
print(f"Final separation heavy: {np.linalg.norm(positions_h1[-1] - positions_h2[-1]):.3f}")
