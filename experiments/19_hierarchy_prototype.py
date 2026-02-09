import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# Ensure local package is findable for utility
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_experiment():
    print("Initializing UKFT Experiment 19: Hierarchical Consciousness Feedback...")
    print("Hypothesis: The Universe uses a Multi-Tiered Control System (Geo/Noo/Theo) to prevent Entropic Dissolution.")

    # -------------------------------------------------------------------------
    # 1. Simulation Setup
    # -------------------------------------------------------------------------
    N_swarm = 2000     # Sufficient for prototype loop
    n_steps = 500
    dt = 0.05
    
    # Physics Base Parameters
    alpha_base = 0.5   # Weak base gravity (system naturally expands/drifts)
    noise_level = 0.20 # Entropy/Random Fluctuations
    
    # Initial State: A loose cloud
    positions = np.random.randn(N_swarm, 3) * 2.0
    velocities = np.random.randn(N_swarm, 3) * 0.5
    
    # Trajectory History: (Steps, N, 3) -> We only store what we need for vis if memory constrained
    # But for N=2000, storing all is fine. 500 * 2000 * 3 * 8 bytes ~ 24MB.
    history_pos = np.zeros((n_steps, N_swarm, 3))
    
    # -------------------------------------------------------------------------
    # 2. Hierarchy Configuration (The "Epiphany")
    # -------------------------------------------------------------------------
    levels = ['geo', 'noo', 'theo']
    # Thresholds for Coherence (0.0 to 1.0). If metric drops below, trigger.
    thresholds = [0.80, 0.60, 0.40] 
    # Intervention Gain (How hard to pull back)
    ramps = [2.0, 8.0, 25.0]  
    # Damping (Friction) to stabilize the correction
    damping_levels = [0.98, 0.95, 0.90] # Higher intervention = more friction to kill chaos
    
    phi_history = []
    alpha_history = []
    level_history = [] # 0=None, 1=Geo, 2=Noo, 3=Theo
    
    # Initial Variance for normalization
    center_0 = np.mean(positions, axis=0)
    var_0 = np.mean(np.linalg.norm(positions - center_0, axis=1))
    
    # -------------------------------------------------------------------------
    # 3. Main Limit Loop
    # -------------------------------------------------------------------------
    print(f"Simulating {n_steps} steps of hierarchical control...")
    
    for step in range(n_steps):
        # A. Measure State (Perception)
        center = np.mean(positions, axis=0)
        # Variance = Mean distance from center
        variance = np.mean(np.linalg.norm(positions - center, axis=1))
        
        # Coherence Metric (phi): 1.0 = Perfect Clump, 0.0 = Infinite Scatter
        # Normalize relative to starting state? Or absolute?
        # Let's use a scale relative to var_0.
        # If var = var_0, phi = 0.8 (Stable). If var > var_0, phi drops.
        phi = 1.0 / (1.0 + 0.25 * (variance / var_0)**2 ) 
        # Tuning: if variance doubles, phi -> 1/(1+1) = 0.5.
        
        # B. Hierarchical Logic (The "Brain")
        intervention_force = 0.0
        active_damping = 0.995 # Default weak friction
        current_level_idx = 0 # None
        
        # Check Theo (Highest Priority)
        # Note: Logic usually cascades. 
        if 200 <= step < 225: # GOD SLEEPS: Disable control to allow chaos to bloom
             intervention_force = 0.0
             current_level_idx = 0
        elif phi < thresholds[2]: # Critical Collapse
            idx = 2
            gain = ramps[idx] * (thresholds[idx] - phi) # Proportional limit
            intervention_force = gain
            active_damping = damping_levels[idx]
            current_level_idx = 3
        elif phi < thresholds[1]: # Major Variance
            idx = 1
            gain = ramps[idx] * (thresholds[idx] - phi)
            intervention_force = gain
            active_damping = damping_levels[idx]
            current_level_idx = 2
        elif phi < thresholds[0]: # Minor Drift
            idx = 0
            gain = ramps[idx] * (thresholds[idx] - phi)
            intervention_force = gain
            active_damping = damping_levels[idx]
            current_level_idx = 1
            
        # Log
        phi_history.append(phi)
        alpha_eff = alpha_base + intervention_force
        alpha_history.append(alpha_eff)
        level_history.append(current_level_idx)
        
        # C. Physics Update
        # 1. Calculate Forces
        # Force 1: Entropic Gravity (Pull to Center of Mass)
        # F = - alpha * (x - center)
        # Simple harmonic well equivalent to "Mean Field" gravity
        dist_vec = positions - center
        acc_gravity = - alpha_eff * dist_vec 
        
        # Force 2: Noise/Entropy (The Enemy)
        # Add random kicks to simulate thermal expansion / chaos
        # Scale noise up over time to force the system to react?
        # Let's make noise sinusoidal to test response
        current_noise = noise_level * (1.0 + 2.0 * step/n_steps) # Ramp up entropy
        
        # STRESS TEST: The Great Disruption
        if 200 <= step < 260:
            current_noise *= 25.0 # Catastrophic entropy injection
            
        acc_noise = np.random.randn(N_swarm, 3) * current_noise
        
        # Explicit Velocity Kick to guarantee explosion
        if step == 200:
             # Radial explosion
             radial_vec = positions - center
             norms = np.linalg.norm(radial_vec, axis=1, keepdims=True) + 1e-6
             velocities += (radial_vec / norms) * 20.0
        
        # Total Acc
        acceleration = acc_gravity + acc_noise
        
        # 2. Integrate
        velocities = active_damping * velocities + acceleration * dt
        positions += velocities * dt
        
        # Store
        history_pos[step] = positions.copy()
        
        if step % 50 == 0:
            print(f"Step {step}: Phi={phi:.3f} | Alpha={alpha_eff:.2f} | Level={['None','Geo','Noo','Theo'][current_level_idx]}")

    # -------------------------------------------------------------------------
    # 4. Visualization (Dual Plot)
    # -------------------------------------------------------------------------
    print("Generating Telemetry Animation...")
    fig = plt.figure(figsize=(10, 8))
    
    # GridSpec
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])
    ax_sim = fig.add_subplot(gs[0], projection='3d')
    ax_telem = fig.add_subplot(gs[1])
    
    # 3D Plot
    scat = ax_sim.scatter([], [], [], s=2, c='cyan', alpha=0.6)
    ax_sim.set_xlim(-10, 10)
    ax_sim.set_ylim(-10, 10)
    ax_sim.set_zlim(-10, 10)
    ax_sim.set_title("UKFT Hierarchy Prototype: The Swarm")
    
    # Telemetry Plot
    ax_telem.set_xlim(0, n_steps)
    ax_telem.set_ylim(0, 1.1)
    ax_telem.set_xlabel("Time Step (Choice Index)")
    ax_telem.set_ylabel("Coherence (Phi)")
    
    line_phi, = ax_telem.plot([], [], 'b-', lw=2, label='Coherence')
    
    # Threshold Lines
    colors = ['green', 'orange', 'red']
    labels = ['GEO (Minor)', 'NOO (Major)', 'THEO (Critical)']
    for i in range(3):
        ax_telem.axhline(thresholds[i], color=colors[i], linestyle='--', alpha=0.5, label=f'{labels[i]} Threshold')
    
    # Active Level Indicator (Area fill)
    fill_poly = ax_telem.fill_between([], [], color='red', alpha=0.1) # Placeholder
    
    txt_status = ax_sim.text2D(0.05, 0.95, "", transform=ax_sim.transAxes, color='black', fontsize=12)

    def update(frame):
        # Update 3D
        pos = history_pos[frame]
        scat._offsets3d = (pos[:,0], pos[:,1], pos[:,2])
        
        # Color based on level?
        lvl = level_history[frame]
        c_map = {0: 'cyan', 1: 'green', 2: 'orange', 3: 'red'}
        scat.set_color(c_map[lvl])
        
        # Update Telemetry
        x_data = np.arange(frame + 1)
        y_data = phi_history[:frame + 1]
        line_phi.set_data(x_data, y_data)
        
        # Status Text
        lvl_name = ['PASSIVE', 'GEO CORRECTION', 'NOO INTERVENTION', 'THEO OVERRIDE'][lvl]
        txt_status.set_text(f"Status: {lvl_name}\nAlpha: {alpha_history[frame]:.2f}")
        
        return scat, line_phi, txt_status

    ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=20, blit=False)
    
    save_path = 'experiments/19_hierarchy_prototype.gif'
    print(f"Saving to {save_path}...")
    ani.save(save_path, writer='pillow', fps=30)
    print("Done.")

if __name__ == "__main__":
    run_experiment()
