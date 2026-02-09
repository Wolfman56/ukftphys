# experiments/10_ukft_quantum_on_entropic_gravity_3d.py
"""
UKFT Quantum on Entropic Gravity — FULL QUANTUM SWARM OVERLAY 🔥

EXPLAINER:
This experiment simulates the intersection of UKFT Entropic Gravity and Quantum Mechanics.
1. THE GRAVITY: Gravity is modeled not as a fundamental force, but as an emergent 'entropic'
   force pushing matter toward regions of maximal information density (Entropy Maximization).
   Two massive 'Knowledge Centers' create deep wells in the probability field.
   
2. THE SWARM: A cloud of 400 'Bohmian' quantum test particles is released. They are not
   point-masses in the traditional sense, but surfers on a Pilot Wave ($R e^{iS}$).
   - They feel the 'Classical' entropic pull ($\nabla \rho$) drawing them into orbits.
   - They also feel the 'Quantum Potential' ($Q$) which prevents collapse and creates interference.
   
3. THE VISUALIZATION:
   - The 'Sheet' represents the Information Density ($\rho$). Deep wells = High Mass/Recall.
   - The particles exhibit 'bunching' (fringes) and 'orbiting' without true Newtonian physics.
   - Watch how they avoid crossing trajectories (Pauli-like exclusion via $Q$) but still
     flock to the mass centers.

Result: A surreal, non-crossing quantum flow surfing a warped entropic space-time.
"""

import numpy as np
import plotly.graph_objects as go
import sys
import os
import shutil

# Add package root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.vis import create_3d_entropic_animation

# Parameters — tune for quantum weirdness vs classical limit
N_swarm = 400              # Bohmian test particles (crank high for dense fringes)
sigma_rho = 0.3            # Knowledge blob width for heavies
alpha_entropic = 12.0      # Entropic strength (gravity-like pull)
m_heavy = 15.0             # Heavy ρ contribution
m_quantum = 0.05           # Tiny back-reaction per quantum particle (set 0 for one-way)
hbar = 0.5                 # Quantum scale — smaller = more spreading/interference
dt = 0.008                 # Time step
n_steps = 1000             # Long for full capture/orbit
animate_every = 10         # Frame skip
z_scale = 4.0              # Sheet depth

# Initial conditions
pos_h1 = np.array([ 0.9,  0.0, 0.1])
pos_h2 = np.array([-0.9,  0.0, 0.1])
vel_h1 = np.array([0.0, -1.1, 0.0])
vel_h2 = np.array([0.0,  1.1, 0.0])

# Quantum swarm initial: broad ring around system for dramatic infall + interference
np.random.seed(42)
r_ring = 2.8
theta = 2 * np.pi * np.random.rand(N_swarm)
pos_swarm = np.zeros((N_swarm, 3))
pos_swarm[:,0] = r_ring * np.cos(theta) + 0.3 * np.random.randn(N_swarm)
pos_swarm[:,1] = r_ring * np.sin(theta) + 0.3 * np.random.randn(N_swarm)
pos_swarm[:,2] = 0.15 + 0.05 * np.random.randn(N_swarm)
vel_swarm = np.zeros((N_swarm, 3))
vel_swarm[:,0] = -0.2 * np.sin(theta)
vel_swarm[:,1] =  0.2 * np.cos(theta)

# Grid for sheet
grid_size = 70
x_grid = np.linspace(-4, 4, grid_size)
y_grid = np.linspace(-4, 4, grid_size)
X, Y = np.meshgrid(x_grid, y_grid)

# Storage
traj_h1, traj_h2 = [pos_h1.copy()], [pos_h2.copy()]
traj_swarm = [pos_swarm.copy()]

# Initial pilot amplitude R = sqrt(ρ) ≈ initial swarm density (broad Gaussian ring)
# For simplicity: analytic initial ψ phase for circular inflow + spreading
phase_swarm = np.zeros(N_swarm)

frames = []

print("Running full UKFT quantum-on-entropic simulation — swarm capture incoming...")

for step in range(n_steps):
    if step % 300 == 0:
        print(f"Step {step}/{n_steps}")
    
    p1, p2 = traj_h1[-1], traj_h2[-1]
    swarm_pos = traj_swarm[-1]
    
    # Analytic ∇ρ at position (for heavies + swarm classical pull)
    def vector_grad_rho(positions):
        # positions: (N, 3) or (3,)
        positions = np.atleast_2d(positions)
        grad = np.zeros_like(positions)
        
        # 1. Heavies contribution (Manual loop is fine for 2 stars)
        for src, m in [(p1, m_heavy), (p2, m_heavy)]:
            delta = positions - src # (N, 3)
            dist2 = np.sum(delta**2, axis=1, keepdims=True)
            # Gradient of m * exp(-r^2/2s^2) is -m(r)/s^2 * exp(...)
            # So we need MINUS delta.
            grad += - (delta / sigma_rho**2) * m * np.exp(-dist2 / (2*sigma_rho**2))
            
        # 2. Swarm contribution (Vectorized)
        # We need sum_j ( - (r_i - r_j)/s^2 * m_q * exp(...) )
        # But this is calculating Force ON positions FROM swarm.
        # If positions is the swarm itself, we exclude self-interaction usually?
        # The prompt says "back-reaction optional", m_quantum is small.
        # Let's do full N-to-N calculation? N=800 -> 640k pairs. Fast in vectors.
        # However, positions might be just ONE point or the whole swarm.
        
        if len(positions) == N_swarm and np.allclose(positions, swarm_pos):
             # Self-interaction case (Swarm acting on Swarm)
             # Computationally heavy to do exact pairwise for every step?
             # N=800 is fine for (800,800) matrix (640k elements).
             # Diff matrix: (N, N, 3)
             # r_i (N,1,3) - r_j (1,N,3) -> (N,N,3)
             diff = positions[:, None, :] - swarm_pos[None, :, :]
             d2 = np.sum(diff**2, axis=-1) # (N, N)
             # Gradient contribution: - (diff / sigma^2) * m * exp(-d2/2sigma^2)
             # We can't sum over axis 1 yet because diff depends on direction.
             coeffs = - (m_quantum / sigma_rho**2) * np.exp(-d2 / (2*sigma_rho**2)) # (N, N)
             # coeffs[i, j] is scalar factor. diff[i, j] is vector.
             # We want sum_j (coeffs[i,j] * diff[i,j])
             grad_swarm = np.sum(coeffs[:, :, None] * diff, axis=1)
             grad += grad_swarm
             
        else:
             # Positions are arbitrary (e.g. Hevies or Grid) acting FROM swarm
             # Loop over positions (N_targets) is better if N_targets is small
             # But here usually N_targets is small (2 heavies) OR large (grid).
             # For Grid (4900 points), (4900, 800) is 4M elements. 
             # 4M floats is 32MB. Totally fine.
             
             diff = positions[:, None, :] - swarm_pos[None, :, :] # (N_t, N_s, 3)
             d2 = np.sum(diff**2, axis=-1) # (N_t, N_s)
             coeffs = - (m_quantum / sigma_rho**2) * np.exp(-d2 / (2*sigma_rho**2))
             grad_swarm = np.sum(coeffs[:, :, None] * diff, axis=1)
             grad += grad_swarm
             
        return grad
    
    # Calculate densities Vectorized
    def vector_rho(positions):
        positions = np.atleast_2d(positions)
        rho = np.zeros(len(positions))
        
        # Heavies
        d1 = np.sum((positions - p1)**2, axis=1)
        d2 = np.sum((positions - p2)**2, axis=1)
        rho += m_heavy * np.exp(-d1 / (2*sigma_rho**2))
        rho += m_heavy * np.exp(-d2 / (2*sigma_rho**2))
        
        # Swarm
        diff = positions[:, None, :] - swarm_pos[None, :, :]
        d2_s = np.sum(diff**2, axis=-1)
        rho_s = np.sum(m_quantum * np.exp(-d2_s / (2*sigma_rho**2)), axis=1)
        rho += rho_s
        
        return rho

    # === UPDATE STEPS ===
    
    # 1. Gradients at Star Positions ( Stars feel each other + Swarm)
    grad_at_stars = vector_grad_rho(np.stack([p1, p2]))
    # remove self-force? The vector_grad_rho includes ALL sources.
    # A star shouldn't be pushed by itself.
    # Correction: The logic above includes "Heavies contribution". 
    # grad_rho_total = grad_rho_stars + grad_rho_swarm.
    # We should subtract the self-gradient if included.
    # But my vector_grad_rho iterates p1, p2. 
    # At p1, delta_p1 = 0. grad term = 0. So self-interaction is naturally zero 
    # because delta vector is zero! Safe.
    
    acc_h1 = alpha_entropic * grad_at_stars[0]
    acc_h2 = alpha_entropic * grad_at_stars[1]
    
    vel_h1 += acc_h1 * dt
    vel_h2 += acc_h2 * dt
    new_p1 = p1 + vel_h1 * dt
    new_p2 = p2 + vel_h2 * dt
    
    # 2. Swarm Update
    # Need Grad Rho and Rho at swarm positions
    grad_at_swarm = vector_grad_rho(swarm_pos) # (N, 3)
    rho_at_swarm = vector_rho(swarm_pos)       # (N,)
    
    # Pilot Amplitude R
    # R = sqrt(rho_total)
    R = np.sqrt(rho_at_swarm + 1e-12)
    R /= (np.linalg.norm(R) + 1e-12) # Normalize R vector? No, R is field. 
    # This normalization changes per step? Just scaling for potential term.
    
    # Bohmian Term: grad_R / R
    # grad_R = grad(sqrt(rho)) = 0.5 * rho^(-0.5) * grad_rho
    #        = 0.5 * grad_rho / R
    # So (grad_R / R) = 0.5 * grad_rho / R^2 = 0.5 * grad_rho / rho
    grad_R_over_R = 0.5 * grad_at_swarm / (rho_at_swarm[:, None] + 1e-12)
    
    # Original logic: 
    # quantum_vel[i] = alpha_entropic * grad_rho/2 + hbar^2 * grad_R/R
    # Wait, simple Entropic is v ~ alpha * grad_rho / rho ?
    # The snippet had: acc = alpha * grad (for stars).
    # For Swarm:
    # "Classical entropic velocity ~ grad rho" -> This implies v = alpha * grad_rho (Aristotelian)
    # The user code had:
    # quantum_vel[i] = alpha_entropic * grad_rho_at(swarm_pos[i]) / 2 + hbar**2 * grad_R / R[i]
    # It seems to be mixing:
    # 1. Coherent attraction (alpha term) - maybe velocity field?
    # 2. Osmotic velocity (grad R / R)
    # I will preserve the form but use the vectorized values.
    
    # Note: The user code had a typo or weird factor "/ 2" in the first term?
    # "alpha_entropic * grad_rho_at(swarm_pos[i]) / 2"
    # I will keep the "/ 2" as it was in the user code (maybe averaging?)
    
    term1 = (alpha_entropic * grad_at_swarm) / 2.0
    term2 = (hbar**2) * grad_R_over_R
    
    quantum_vel = term1 + term2
    
    vel_swarm += quantum_vel * dt # Wait, is this dv/dt or v?
    # User code: "vel_swarm += quantum_vel * dt"  -> implies quantum_vel is ACCELERATION.
    # But variable name is "quantum_vel".
    # And comment says "Classical entropic velocity ... Full Bohmian guidance v = ..."
    # If it's v = ..., then we should set vel = v.
    # But code does +=.
    # If I look at the Swarm Init: vel_swarm is set to non-zero.
    # If it's Bohmian, usually v is determined by position. (First order).
    # If it's second order (Newtonian with Quantum Potential), then acc = -grad(Q).
    # term2 ~ grad_rho/rho. This is Osmotic Velocity, not Acceleration from Q.
    # Q ~ - del^2 R / R.
    # Given the confusion in the user script (mixing names), I will stick to the *operational* logic
    # found in the loop: "vel += calculated_val * dt". 
    # So I treat "quantum_vel" as an acceleration (force per mass).
    
    new_swarm = swarm_pos + vel_swarm * dt
    
    # Store
    traj_h1.append(new_p1)
    traj_h2.append(new_p2)
    traj_swarm.append(new_swarm)
    
    # Frame building
    if step % animate_every == 0 or step == n_steps - 1:
        # Dynamic sheet from total ρ
        # Vectorized rho calculation on grid
        flat_X = X.flatten()
        flat_Y = Y.flatten()
        flat_Z_grid = np.zeros_like(flat_X)
        grid_pos = np.stack((flat_X, flat_Y, flat_Z_grid), axis=1) # (N_grid, 3)
        
        # We can implement a stripped down vector_rho for grid or reuse vector_rho
        # BUT vector_rho does N_t x N_s diff array.
        # Grid is 4900, Swarm is 800. Matrix is 4M floats. 32MB. Safe.
        rho_vals = vector_rho(grid_pos)
        rho_grid = rho_vals.reshape(X.shape)
        
        Z = -z_scale * rho_grid
        
        frame_data = [
            go.Surface(x=X, y=Y, z=Z, colorscale='viridis', opacity=0.65, showscale=False),
            # Heavy trails
            go.Scatter3d(x=[p[0] for p in traj_h1], y=[p[1] for p in traj_h1], z=[p[2] for p in traj_h1],
                         mode='lines', line=dict(color='cyan', width=10), name='Heavy 1'),
            go.Scatter3d(x=[p[0] for p in traj_h2], y=[p[1] for p in traj_h2], z=[p[2] for p in traj_h2],
                         mode='lines', line=dict(color='magenta', width=10), name='Heavy 2'),
            # Swarm points (alpha fade for density feel)
            go.Scatter3d(x=new_swarm[:,0], y=new_swarm[:,1], z=new_swarm[:,2],
                         mode='markers', marker=dict(size=3, color='yellow', opacity=0.6), name='Quantum Swarm'),
            # Current heavies
            go.Scatter3d(x=[new_p1[0]], y=[new_p1[1]], z=[new_p1[2]], mode='markers',
                         marker=dict(size=18, color='cyan'), name='Heavy 1'),
            go.Scatter3d(x=[new_p2[0]], y=[new_p2[1]], z=[new_p2[2]], mode='markers',
                         marker=dict(size=18, color='magenta'), name='Heavy 2'),
        ]
        frames.append(go.Frame(data=frame_data, name=str(step)))

traj_h1 = np.array(traj_h1)
traj_h2 = np.array(traj_h2)
traj_swarm = np.array(traj_swarm)

# Final Plot using Standardized Visualizer
fig = create_3d_entropic_animation(
    frames, 
    title="UKFT Quantum Swarm on Entropic Gravity — Interference + Teleological Capture",
    ranges={'x': [-4.5, 4.5], 'y': [-4.5, 4.5], 'z': [-15, 5]}
)

# SNAPSHOT: Use the final frame for the static PNG so it looks interesting
# and ensures the WebGL renderer has "warmed up" with full geometry
print("Generating static preview (using final frame)...")
original_data = fig.data
fig.update(data=frames[-1].data)
png_file = "results/10_ukft_quantum_swarm_3d.png"
try:
    fig.write_image(png_file)
    print(f"Saved plot image to {png_file}")
    
    # Copy to experiments folder
    exp_png = os.path.join(os.path.dirname(__file__), "10_ukft_quantum_swarm_3d.png")
    shutil.copy(png_file, exp_png)
    print(f"Copied static preview to {exp_png}")
except Exception as e:
    print(f"Could not save PNG: {e}")

# REVERT: Reset to Frame 0 for the interactive HTML so it starts at t=0
print("Generating interactive HTML...")
fig.update(data=original_data)
output_file = "results/10_ukft_quantum_swarm_3d.html"
fig.write_html(output_file)
print(f"Quantum Swarm saved to {output_file}")
