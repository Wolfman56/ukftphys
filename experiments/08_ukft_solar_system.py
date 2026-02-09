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
from ukft_sim.physics import get_analytic_density_and_gradient

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

    # Update Planets
    current_sources = [(p_star1, m_star), (p_star2, m_star)]
    
    for i, p_hist in enumerate(planet_positions):
        pos = p_hist[-1]
        vel = planet_vels[i]
        
        rho, grad = get_analytic_density_and_gradient(pos, current_sources, sigma)
        
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
        # Use Gaussian wells for visualization to match the analytic density field
        # Z ~ - Sum(m * exp(-r^2/2sigma^2))
        
        # Calculate rho grid for Stars
        dist1_sq = (X - p_star1[0])**2 + (Y - p_star1[1])**2
        dist2_sq = (X - p_star2[0])**2 + (Y - p_star2[1])**2
        
        # Gaussian Wells for Stars
        # We invert the density to show "gravity wells"
        rho_stars = m_star * np.exp(-dist1_sq / (2 * sigma**2)) + \
                    m_star * np.exp(-dist2_sq / (2 * sigma**2))
        
        # Add planet dents (Visual only)
        # We give planets a slightly sharper sigma for visibility
        rho_planets = np.zeros_like(rho_stars)
        sigma_visual_planet = 0.5
        for i, p_hist in enumerate(planet_positions):
            p_curr = p_hist[-1]
            dist_p_sq = (X - p_curr[0])**2 + (Y - p_curr[1])**2
            # Visual mass factor 2.0
            rho_planets += 2.0 * np.exp(-dist_p_sq / (2 * sigma_visual_planet**2))
            
        # Z is represented as negative density (Deep wells where mass is high)
        Z = - z_scale * (rho_stars + rho_planets)
        
        # No clamping needed for Gaussians as they are finite
        
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
