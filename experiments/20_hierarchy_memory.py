import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# Ensure local package is findable for utility
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_experiment():
    print("Initializing UKFT Experiment 20: Hierarchical Memory Protocol...")
    print("Hypothesis: Higher tiers of control utilize longer 'memory' windows to avoid over-reaction.")

    # -------------------------------------------------------------------------
    # 1. Simulation Setup
    # -------------------------------------------------------------------------
    N_swarm = 2000     
    n_steps = 600      # Extended for memory windows
    dt = 0.05
    
    # Physics Base Parameters
    alpha_base = 0.5   
    noise_level = 0.20 
    
    # Initial State
    positions = np.random.randn(N_swarm, 3) * 2.0
    velocities = np.random.randn(N_swarm, 3) * 0.5
    
    history_pos = np.zeros((n_steps, N_swarm, 3))
    
    # -------------------------------------------------------------------------
    # 2. Hierarchy Configuration (Memory Edition)
    # -------------------------------------------------------------------------
    # Window sizes for sliding average of Phi
    W_geo = 10
    W_noo = 50
    W_theo = 100 # Adjusted for 600 steps scale (Grok suggested 200, but let's be responsive enough)

    # Thresholds
    thresholds = [0.80, 0.60, 0.40] 
    ramps = [2.0, 8.0, 25.0]  
    damping_levels = [0.98, 0.95, 0.90]
    
    phi_history = []
    # We maintain a buffer of historical Phi values
    # Init with '1.0' (perfect coherence) so we don't start PANICKING immediately
    phi_buffer = np.ones(W_theo) 

    alpha_history = []
    level_history = [] # 0=None, 1=Geo, 2=Noo, 3=Theo
    
    # Initial Variance for normalization
    center_0 = np.mean(positions, axis=0)
    var_0 = np.mean(np.linalg.norm(positions - center_0, axis=1))
    
    # -------------------------------------------------------------------------
    # 3. Main Limit Loop
    # -------------------------------------------------------------------------
    print(f"Simulating {n_steps} steps with memory windows [G:{W_geo}, N:{W_noo}, T:{W_theo}]...")
    
    for step in range(n_steps):
        # A. Measure State (Perception)
        center = np.mean(positions, axis=0)
        variance = np.mean(np.linalg.norm(positions - center, axis=1))
        
        # Instantaneous Phi
        phi_current = 1.0 / (1.0 + 0.25 * (variance / var_0)**2 ) 
        
        # Update Memory Buffer
        phi_buffer = np.roll(phi_buffer, -1)
        phi_buffer[-1] = phi_current
        
        # Calculate Hierarchical Perceptions (Smoothed Reality)
        phi_geo = np.mean(phi_buffer[-W_geo:])
        phi_noo = np.mean(phi_buffer[-W_noo:])
        phi_theo = np.mean(phi_buffer[-W_theo:])
        
        # B. Hierarchical Logic (The "Brain")
        intervention_force = 0.0
        active_damping = 0.995 
        current_level_idx = 0 
        
        # Check Theo (Needs sustained crisis per Grok)
        # Note: We use the *Averaged* phi for the check now.
        if 200 <= step < 225: # GOD SLEEPS (Delay)
             intervention_force = 0.0
             current_level_idx = 0
        elif phi_theo < thresholds[2]: # Critical Collapse (Long term avg dropped)
            idx = 2
            gain = ramps[idx] * (thresholds[idx] - phi_theo)
            intervention_force = gain
            active_damping = damping_levels[idx]
            current_level_idx = 3
        elif phi_noo < thresholds[1]: # Major Variance (Mid term avg dropped)
            idx = 1
            gain = ramps[idx] * (thresholds[idx] - phi_noo)
            intervention_force = gain
            active_damping = damping_levels[idx]
            current_level_idx = 2
        elif phi_geo < thresholds[0]: # Minor Drift (Short term avg dropped)
            idx = 0
            gain = ramps[idx] * (thresholds[idx] - phi_geo)
            intervention_force = gain
            active_damping = damping_levels[idx]
            current_level_idx = 1
            
        # Log (Store instantaneous for viz, but logic used avg)
        phi_history.append(phi_current)
        alpha_eff = alpha_base + intervention_force
        alpha_history.append(alpha_eff)
        level_history.append(current_level_idx)
        
        # C. Physics Update
        dist_vec = positions - center
        acc_gravity = - alpha_eff * dist_vec 
        
        current_noise = noise_level * (1.0 + 2.0 * step/n_steps)
        
        # STRESS TEST: The Great Disruption (Same as Exp 19)
        if 200 <= step < 260:
            current_noise *= 25.0 
            
        acc_noise = np.random.randn(N_swarm, 3) * current_noise
        
        if step == 200:
             radial_vec = positions - center
             norms = np.linalg.norm(radial_vec, axis=1, keepdims=True) + 1e-6
             velocities += (radial_vec / norms) * 20.0
        
        # Integrate
        acceleration = acc_gravity + acc_noise
        velocities = active_damping * velocities + acceleration * dt
        positions += velocities * dt
        history_pos[step] = positions.copy()
        
        if step % 50 == 0:
            print(f"Step {step}: Phi_Inst={phi_current:.3f} | Phi_Theo={phi_theo:.3f} | Alpha={alpha_eff:.2f} | Lv={current_level_idx}")

    # -------------------------------------------------------------------------
    # 4. Visualization
    # -------------------------------------------------------------------------
    print("Generating Telemetry Animation...")
    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])
    ax_sim = fig.add_subplot(gs[0], projection='3d')
    ax_telem = fig.add_subplot(gs[1])
    
    # 3D
    scat = ax_sim.scatter([], [], [], s=2, c='cyan', alpha=0.6)
    ax_sim.set_xlim(-15, 15)
    ax_sim.set_ylim(-15, 15)
    ax_sim.set_zlim(-15, 15)
    ax_sim.set_title("Exp 20: Hierarchy Memory (Smoothed Intervention)")
    
    # Telemetry
    ax_telem.set_xlim(0, n_steps)
    ax_telem.set_ylim(0, 1.1)
    ax_telem.set_xlabel("Time Step")
    ax_telem.set_ylabel("Coherence (Phi)")
    
    line_phi, = ax_telem.plot([], [], 'b-', lw=1, alpha=0.3, label='Instant')
    line_avg, = ax_telem.plot([], [], 'k-', lw=2, label='Theo Avg')
    
    colors = ['green', 'orange', 'red']
    for i in range(3):
        ax_telem.axhline(thresholds[i], color=colors[i], linestyle='--', alpha=0.5)
        
    txt_status = ax_sim.text2D(0.05, 0.95, "", transform=ax_sim.transAxes, color='black', fontsize=12)

    def update(frame):
        pos = history_pos[frame]
        scat._offsets3d = (pos[:,0], pos[:,1], pos[:,2])
        
        lvl = level_history[frame]
        c_map = {0: 'cyan', 1: 'green', 2: 'orange', 3: 'red'}
        scat.set_color(c_map[lvl])
        
        # Telemetry
        x_data = np.arange(frame + 1)
        # Reconstruct the running average for viz is hard without storing it, 
        # but let's just show instantaneous and maybe a simple convolution post-hoc?
        # Actually we didn't store the averages. 
        # Let's just show instantaneous for speed.
        line_phi.set_data(x_data, phi_history[:frame+1])
        
        # Re-calc average for viz at this frame? 
        # Approximating viz for "Theo Avg"
        if frame > 0:
            y_data = phi_history[:frame+1]
            # Simple window avg for plotting
            window = W_theo
            if frame < window:
                avg = np.cumsum(y_data) / (np.arange(len(y_data)) + 1)
            else:
                ret = np.cumsum(y_data, dtype=float)
                ret[window:] = ret[window:] - ret[:-window]
                avg = ret[window - 1:] / window
                # pad start
                pad = [1.0] * (window-1)
                avg = np.concatenate([pad, avg])
                avg = avg[:frame+1] # Trim explicitly
                
            line_avg.set_data(x_data, avg)
        
        txt_status.set_text(f"Status: {['PASSIVE','GEO','NOO','THEO'][lvl]}\nAlpha: {alpha_history[frame]:.2f}")
        return scat, line_phi, line_avg, txt_status

    ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=20, blit=False)
    ani.save('experiments/20_hierarchy_memory.gif', writer='pillow', fps=30)
    print("Done.")

if __name__ == "__main__":
    run_experiment()
