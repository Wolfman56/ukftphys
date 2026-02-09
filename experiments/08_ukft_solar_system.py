# experiments/08_ukft_solar_system.py
"""
UKFT Solar System Simulator (Bianconi Force) ☀️🪐

Demonstration of multi-body orbital stability using Entropic Gravity.
Features:
- Central binary "Star" (rotating heavy source).
- Multiple "Planets" (test particles) initialized at different radii.
- Uses the Unified 3D Visualizer with Slider Fix.
"""

import numpy as np
import plotly.graph_objects as go
import os
import sys

# Ensure local package is findable
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ukft_sim.vis import create_3d_entropic_animation

# Parameters
sigma = 0.2
alpha_entropic = 2.0
lambda_cosmo = 0.05
m_heavy = 10.0
dt = 0.01             # Finer time step for stability
n_steps = 2000
animate_every = 10
z_scale = 0.5         # Reduced for better visual dynamic range

# Initial Conditions - Solar System
# Binary Star
radius_star = 0.5
omega_star = 0.8
m_star = 10.0

# Planets (Test Particles)
# Adjust Mars velocity to desynchronize from Star Rotation (which is 0.8 rad/s)
# Mars R=1.5. v_circ for sync = 1.2.
# Let's make Mars faster: v=1.5 -> omega = 1.0. 
# Or slower: v=0.9 -> omega = 0.6.
planets_init = [
    # Inner Rocky
    {'pos': [1.5, 0, 0.1],  'vel': [0, 1.5, 0], 'color': 'red',   'name': 'Mars'}, # Faster
    # Goldilocks
    {'pos': [2.2, 0, 0.0],  'vel': [0, 1.8, 0], 'color': 'green', 'name': 'Earth'},
    # Gas Giant
    {'pos': [-3.0, 0, -0.1], 'vel': [0, -2.5, 0], 'color': 'orange', 'name': 'Jupiter'},
    # Comet (Elliptical)
    {'pos': [0, 4.0, 0.5], 'vel': [-0.5, 0, 0], 'color': 'white', 'name': 'Comet'}
]

# State vectors
# Heavy sources (managed explicitly as time-dependent field sources)
# Planets (integrated via Euler)

planet_positions = [ [np.array(p['pos'])] for p in planets_init ]
planet_vels = [ np.array(p['vel']) for p in planets_init ]

# Animation frames
frames = []

# Grid for visual sheet
grid_size = 40
x_grid = np.linspace(-4, 4, grid_size)
y_grid = np.linspace(-4, 4, grid_size)
X, Y = np.meshgrid(x_grid, y_grid)

print("Running UKFT Solar System Simulation...")

pos_stars_hist_1 = []
pos_stars_hist_2 = []

for step in range(n_steps):
    if step % 200 == 0:
        print(f"Step {step}/{n_steps}")
        
    t = step * dt
    angle = omega_star * t
    
    # Binary Star Positions (Prescribed)
    p_star1 = np.array([radius_star * np.cos(angle), radius_star * np.sin(angle), 0])
    p_star2 = np.array([radius_star * np.cos(angle + np.pi), radius_star * np.sin(angle + np.pi), 0])
    
    pos_stars_hist_1.append(p_star1)
    pos_stars_hist_2.append(p_star2)

    # Field Function (Bianconi Relative Entropy)
    def rho_at(pos, sources):
        rho = 0.0
        for src in sources:
            dist2 = np.sum((pos - src)**2) + 1e-8
            rho += m_star * np.exp(-dist2 / (2 * sigma**2))
        return rho

    def grad_rho_at(pos, sources):
        grad = np.zeros(3)
        eps = 1e-4
        r0 = rho_at(pos, sources)
        for i in range(3):
            d = np.zeros(3); d[i] = eps
            grad[i] = (rho_at(pos + d, sources) - rho_at(pos - d, sources)) / (2*eps)
        return grad, r0

    # Update Planets
    current_sources = [p_star1, p_star2]
    
    for i, p_hist in enumerate(planet_positions):
        pos = p_hist[-1]
        vel = planet_vels[i]
        
        grad, rho = grad_rho_at(pos, current_sources)
        
        # F = alpha * grad(rho)/rho + lambda * pos
        # Stability epsilon for rho
        eps_rho = 1e-12
        acc = alpha_entropic * grad / (rho + eps_rho)
        acc += lambda_cosmo * pos
        
        # Damping for stability
        vel *= 0.999
        
        vel += acc * dt
        new_pos = pos + vel * dt
        
        p_hist.append(new_pos)
        planet_vels[i] = vel

    # Build Frame
    if step % animate_every == 0 or step == n_steps - 1:
        # Dynamic Sheet potential Z
        # Z ~ - Sum(m/r) approximation or just visualize rho?
        # Let's visualize -log(rho) as the "Depth"
        # Calculate rho grid
        Z = np.zeros_like(X)
        # Vectorized grid calc? slow in python loop, let's do simple approximation
        # Just distance based sum like before for speed
        dist1 = np.sqrt((X - p_star1[0])**2 + (Y - p_star1[1])**2 + 1e-6)
        dist2 = np.sqrt((X - p_star2[0])**2 + (Y - p_star2[1])**2 + 1e-6)
        # Z = - (1/d1 + 1/d2) visualizer
        Z_stars = - z_scale * (m_star/dist1 + m_star/dist2)
        
        # Add planet dents?
        Z_planets = np.zeros_like(Z_stars)
        for i, p_hist in enumerate(planet_positions):
            p_curr = p_hist[-1]
            dist_p = np.sqrt((X - p_curr[0])**2 + (Y - p_curr[1])**2 + 1e-6)
            # Make planets "heavier" visually so their gravity wells are visible 
            # against the stars. (Visual Mass 2.0 instead of 0.5)
            Z_planets -= z_scale * (2.0 / dist_p)
            
        Z = Z_stars + Z_planets
        
        # Clamp Z for visibility (prevent infinite spikes)
        # With z_scale=0.5, typical deep values are around -20
        Z = np.maximum(Z, -20)
        
        frame_data = [
            # Gravity Well
            go.Surface(x=X, y=Y, z=Z, 
                       colorscale='viridis', 
                       # Dynamic Range: -20 (deep well) to 0 (flat space)
                       cmin=-20, cmax=0,
                       opacity=0.8, 
                       showscale=False),
            # Stars
            go.Scatter3d(x=[p_star1[0], p_star2[0]], y=[p_star1[1], p_star2[1]], z=[0,0], 
                         mode='markers', marker=dict(color='yellow', size=15), name='Stars'),
        ]
        
        # Add Planets and Trails
        for i, p_hist in enumerate(planet_positions):
            # Trail (last 50 steps)
            trail_len = 50
            trail = np.array(p_hist[-trail_len:]) if len(p_hist) > 1 else np.array([p_hist[0]])
            
            frame_data.append(go.Scatter3d(
                x=trail[:,0], y=trail[:,1], z=trail[:,2],
                mode='lines', line=dict(color=planets_init[i]['color'], width=4),
                name=f"{planets_init[i]['name']} Trail"
            ))
            # Head
            curr = p_hist[-1]
            frame_data.append(go.Scatter3d(
                x=[curr[0]], y=[curr[1]], z=[curr[2]],
                mode='markers', marker=dict(color=planets_init[i]['color'], size=8),
                name=planets_init[i]['name']
            ))
            
        frames.append(go.Frame(data=frame_data, name=str(step)))

# Final Plot
fig = create_3d_entropic_animation(
    frames, 
    title="UKFT Solar System Simulation (Bianconi Gravity)",
    ranges={'x': [-4,4], 'y': [-4,4], 'z': [-10, 2]}
)

# SNAPSHOT: Use the final frame for the static PNG so it looks interesting
# and ensures the WebGL renderer has "warmed up" with full geometry
print("Generating static preview (using final frame)...")
original_data = fig.data
fig.update(data=frames[-1].data)
png_file = "results/08_ukft_solar_system.png"
try:
    fig.write_image(png_file)
    print(f"Saved plot image to {png_file}")
except Exception as e:
    print(f"Could not save PNG: {e}")

# REVERT: Reset to Frame 0 for the interactive HTML so it starts at t=0
print("Generating interactive HTML...")
fig.update(data=original_data)
output_file = "results/08_ukft_solar_system.html"
fig.write_html(output_file)
print(f"Solar System saved to {output_file}")
