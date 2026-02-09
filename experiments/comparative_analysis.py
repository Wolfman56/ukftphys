import numpy as np
import matplotlib.pyplot as plt
import os

# Configuration matching recent edits
steps = 2000
dt = 0.01
sigma = 0.2
m_heavy = 10.0
m_test = 0.1

# Initial Conditions
pos_start = np.array([0.1, 2.5, 0.2])
vel_start = np.array([-0.8, -0.2, 0.0])

# Orbit
radius_orbit = 1.2
omega = 1.0

def get_heavy_pos(t):
    angle = omega * t
    p1 = np.array([radius_orbit * np.cos(angle), radius_orbit * np.sin(angle), 0])
    p2 = np.array([radius_orbit * np.cos(angle + np.pi), radius_orbit * np.sin(angle + np.pi), 0])
    return p1, p2

def run_sim(mode, alpha):
    pos = pos_start.copy()
    vel = vel_start.copy()
    traj = [pos.copy()]
    
    for i in range(steps):
        t = i * dt
        p1, p2 = get_heavy_pos(t)
        
        # Current pos
        p = pos
        
        # Distances
        d1_sq = np.sum((p - p1)**2)
        d2_sq = np.sum((p - p2)**2)
        
        # Rho (unnormalized sum of Gaussians)
        rho1 = m_heavy * np.exp(-d1_sq / (2 * sigma**2))
        rho2 = m_heavy * np.exp(-d2_sq / (2 * sigma**2))
        rho_tot = rho1 + rho2 + 1e-9
        
        # Gradients
        # Grad(exp(-r^2/2s^2)) = exp(...) * (-x/s^2)
        grad1 = rho1 * (-(p - p1) / sigma**2)
        grad2 = rho2 * (-(p - p2) / sigma**2)
        grad_tot = grad1 + grad2
        
        # Force Law
        if mode == 'standard':
            # Exp 06: F ~ alpha * grad_rho
            acc = alpha * grad_tot
        elif mode == 'bianconi':
            # Exp 07: F ~ alpha * grad_rho / rho
            # Plus Lambda term usually, but let's isolate the entropic part first.
            # In Exp 07 we added lambda * p. Let's include it for accuracy.
            lambda_cosmo = 0.05
            acc = (alpha * grad_tot / rho_tot) + (lambda_cosmo * p)
            
        # Update
        if mode == 'bianconi':
             vel *= 0.995 # Damping in 07
             
        vel += acc * dt
        pos += vel * dt
        traj.append(pos.copy())
        
    return np.array(traj)

# Run both
traj_06 = run_sim('standard', alpha=8.0)
traj_07 = run_sim('bianconi', alpha=2.0)

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Trajectory Plot
ax1.set_title("Particle Trajectories (XY Projection)")
ax1.set_xlim(-3.5, 3.5)
ax1.set_ylim(-3.5, 3.5)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)

# Plot Heavy Orbit (approx)
circle = plt.Circle((0, 0), radius_orbit, color='gray', fill=False, linestyle='--', alpha=0.5, label='Source Orbit')
ax1.add_artist(circle)

# Plot 06
ax1.plot(traj_06[:,0], traj_06[:,1], label='Exp 06: Standard (alpha=8)', color='cyan', alpha=0.8)
ax1.scatter(traj_06[-1,0], traj_06[-1,1], color='cyan', s=50, marker='x')

# Plot 07
ax1.plot(traj_07[:,0], traj_07[:,1], label='Exp 07: Bianconi (alpha=2)', color='magenta', alpha=0.8)
ax1.scatter(traj_07[-1,0], traj_07[-1,1], color='magenta', s=50, marker='x')

ax1.legend()
ax1.set_xlabel("X Position")
ax1.set_ylabel("Y Position")

# Force Law Comparison Plot
r = np.linspace(0, 5, 100)
# Simplify: 1 source at 0
rho = np.exp(-r**2 / (2 * sigma**2))
grad_mag = (r / sigma**2) * rho
force_std = 8.0 * grad_mag
force_bianconi = 2.0 * (grad_mag / rho) # = 2.0 * r / sigma^2

ax2.set_title("Effective Entropic Force Magnitude vs Distance (1D)")
ax2.plot(r, force_std, label='Standard Force (F ~ r * exp(-r^2))', color='cyan')
ax2.plot(r, force_bianconi, label='Bianconi Force (F ~ r)', color='magenta')
ax2.set_xlabel("Distance r")
ax2.set_ylabel("Force Magnitude")
ax2.grid(True)
ax2.legend()
ax2.set_ylim(0, 20) # Clamp to see the crossover

plt.tight_layout()
plt.savefig('results/trajectory_comparison.png')
print("Comparison generated at results/trajectory_comparison.png")
