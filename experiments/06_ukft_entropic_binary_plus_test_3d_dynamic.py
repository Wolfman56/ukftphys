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

# Parameters — tune for chaos or stability
sigma = 0.2                # Gaussian width (knowledge spread) — smaller = sharper 1/r-like attraction
alpha_entropic = 8.0       # Overall strength — higher = tighter orbits / faster infall
m_heavy = 10.0             # "Mass" scaling for heavy particles' ρ contribution
m_test = 0.1               # Tiny back-reaction from test particle (set 0 for none)
dt = 0.01                  # Time step
n_steps = 2000             # Long run for full spirals
animate_every = 10         # Frame skip for smoother animation / file size
z_scale = 3.0              # Visual depth scaling for sheet

# Initial positions (xy-plane orbit, slight z for visibility)
pos_h1 = np.array([ 0.8,  0.0, 0.05])
pos_h2 = np.array([-0.8,  0.0, 0.05])
pos_test = np.array([0.0, 2.5, 0.2])   # Start far out for dramatic infall

vel_h1 = np.array([0.0, -1.2, 0.0])
vel_h2 = np.array([0.0,  1.2, 0.0])
vel_test = np.array([-0.3, 0.0, 0.0])  # Slight tangential for orbit attempt

# Storage
positions_h1 = [pos_h1.copy()]
positions_h2 = [pos_h2.copy()]
positions_test = [pos_test.copy()]

# Grid for dynamic sheet (static grid, recompute Z per frame)
grid_size = 60
x_grid = np.linspace(-3, 3, grid_size)
y_grid = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x_grid, y_grid)

# Animation frames storage
frames = []

print("Running UKFT entropic 3-body simulation — this will take a moment...")

for step in range(n_steps):
    if step % 200 == 0:
        print(f"Step {step}/{n_steps}")
    
    # Current positions
    p1, p2, pt = positions_h1[-1], positions_h2[-1], positions_test[-1]
    
    # Knowledge density ρ at each particle position (sum of Gaussians)
    def rho_at(pos, sources=[(p1, m_heavy), (p2, m_heavy), (pt, m_test)]):
        rho = 0.0
        for src_pos, m_src in sources:
            dist2 = np.sum((pos - src_pos)**2) + 1e-8
            rho += m_src * np.exp(-dist2 / (2 * sigma**2))
        return rho
    
    rho1 = rho_at(p1, sources=[(p2, m_heavy), (pt, m_test)])  # Exclude self
    rho2 = rho_at(p2, sources=[(p1, m_heavy), (pt, m_test)])
    rho_t = rho_at(pt, sources=[(p1, m_heavy), (p2, m_heavy)])
    
    # Gradient ∇ρ ≈ direction to higher density
    def grad_rho_at(pos, sources):
        grad = np.zeros(3)
        eps = 1e-6
        for i in range(3):
            delta = np.zeros(3)
            delta[i] = eps
            grad[i] = (rho_at(pos + delta, sources) - rho_at(pos - delta, sources)) / (2 * eps)
        return grad
    
    grad1 = grad_rho_at(p1, sources=[(p2, m_heavy), (pt, m_test)])
    grad2 = grad_rho_at(p2, sources=[(p1, m_heavy), (pt, m_test)])
    grad_t = grad_rho_at(pt, sources=[(p1, m_heavy), (p2, m_heavy)])
    
    # Acceleration = alpha * ∇ρ (toward higher coherence / lower entropy)
    acc1 = alpha_entropic * grad1
    acc2 = alpha_entropic * grad2
    acc_t = alpha_entropic * grad_t
    
    # Euler update
    vel_h1 += acc1 * dt
    vel_h2 += acc2 * dt
    vel_test += acc_t * dt
    
    new_p1 = p1 + vel_h1 * dt
    new_p2 = p2 + vel_h2 * dt
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
        Z = -z_scale * (m_heavy / dist1 + m_heavy / dist2 + m_test / dist_t)
        
        frame_data = [
            # Dynamic sheet
            go.Surface(x=X, y=Y, z=Z, colorscale='viridis', opacity=0.7, showscale=False),
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
fig = go.Figure(data=frames[0].data, frames=frames)

fig.update_layout(
    title="UKFT Entropic Gravity — Binary + Test Particle on Dynamically Warped Space-Time Sheet",
    scene=dict(
        xaxis=dict(range=[-3.5, 3.5], title='X'),
        yaxis=dict(range=[-3.5, 3.5], title='Y'),
        zaxis=dict(range=[-12, 3], title='Z (entropic curvature)'),
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=0.6),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
    ),
    height=1000,
    template="plotly_dark",
    updatemenus=[dict(
        type="buttons",
        buttons=[dict(label="Play", method="animate",
                      args=[None, {"frame": {"duration": 60, "redraw": True}, "fromcurrent": True}]),
                 dict(label="Pause", method="animate",
                      args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])]
    )]
)

output_file = os.path.join("results", "06_ukft_entropic_binary_plus_test_3d_dynamic.html")
fig.write_html(output_file)

# Save PNG of the final frame
png_file = output_file.replace(".html", ".png")
try:
    fig.write_image(png_file)
    print(f"Saved plot image to {png_file}")
except Exception as e:
    print(f"Could not save PNG: {e}")

print(f"UKFT entropic 3-body complete. Saved to {output_file}")
print(f"Final separation heavy: {np.linalg.norm(positions_h1[-1] - positions_h2[-1]):.3f}")
