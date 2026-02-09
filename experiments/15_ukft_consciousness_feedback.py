# experiments/15_ukft_consciousness_feedback.py
"""
Experiment 15: UKFT Consciousness Feedback Control 🧠⚡️

"The Big One": A closed-loop Control System where the Observer's
perception of "Coherence" continuously modifies the Physical Laws
(Gravity and Damping) to stabilize the reality.

Scenario:
1. System starts in equilibrium.
2. At t=60, a MASSIVE CHAOTIC EVENT (Entropy Injection) disrupts the swarm.
3. The Observer detects the drop in Coherence.
4. The Control Loop activates "Willpower" (Feedback), increasing Entropic Gravity
   and Damping to force the system back into a coherent quantum state.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec

# Add package root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.gpu import EntropicGPUAccelerator
from ukft_sim.perception import WebGPUPerceptionAccelerator

def run_feedback_loop():
    print("🧠⚡️ Initializing UKFT Consciousness Feedback System...")
    
    physics = EntropicGPUAccelerator()
    perception = WebGPUPerceptionAccelerator()
    
    # -------------------------------------------------------------------------
    # CONFIGURATION
    # -------------------------------------------------------------------------
    N_swarm = 60_000
    n_steps = 350
    width, height = 256, 256
    range_lim = 4.0
    
    # Base Physics
    dt_base = 0.02
    alpha_base = 12.0
    damping_base = 0.99
    sigma = 0.6
    
    # Control System (PID-like)
    target_coherence = 0.85
    Kp = 40.0 # Proportional Gain
    
    # Chaos Event
    chaos_frame = 60
    chaos_magnitude = 3.5 # Velocity kick
    
    # -------------------------------------------------------------------------
    # INITIALIZATION
    # -------------------------------------------------------------------------
    # Binary Star
    m_heavy = 15.0
    p1 = np.array([ 1.5,  0.0, 0.0]); v1 = np.array([ 0.0,  0.5, 0.0])
    p2 = np.array([-1.5,  0.0, 0.0]); v2 = np.array([ 0.0, -0.5, 0.0])
    
    # Swarm
    theta = 2 * np.pi * np.random.rand(N_swarm)
    r = 3.0 + 0.4 * np.random.randn(N_swarm)
    z = 0.4 * np.random.randn(N_swarm)
    
    pos = np.zeros((N_swarm, 3), dtype=np.float32)
    pos[:, 0] = r * np.cos(theta)
    pos[:, 1] = r * np.sin(theta)
    pos[:, 2] = z
    
    vel = np.zeros_like(pos)
    # Orbting velocity
    vel[:, 0] = -pos[:, 1] * 0.7
    vel[:, 1] =  pos[:, 0] * 0.7
    
    # -------------------------------------------------------------------------
    # VISUALIZATION LAYOUT
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(14, 8), facecolor='#050505')
    gs = GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[3, 1], figure=fig)
    
    # 1. Reality View
    ax_real = fig.add_subplot(gs[0, 0])
    ax_real.set_title("PHYSICAL REALITY (Density)", color='white', pad=10)
    ax_real.axis('off')
    img_real = ax_real.imshow(np.zeros((height, width)), cmap='inferno', 
                             origin='lower', vmin=0, vmax=20)
    
    # 2. Perception View
    ax_perc = fig.add_subplot(gs[0, 1])
    ax_perc.set_title("OBSERVER STATE (Coherence)", color='white', pad=10)
    ax_perc.axis('off')
    img_perc = ax_perc.imshow(np.zeros((height, width)), cmap='viridis', 
                             origin='lower', vmin=0, vmax=1.0)
    
    # 3. Telemetry Panel (Bottom)
    ax_telem = fig.add_subplot(gs[1, :])
    ax_telem.set_facecolor('#111111')
    ax_telem.set_xlim(0, n_steps)
    ax_telem.set_ylim(0, 1.2)
    ax_telem.set_title("CONSCIOUSNESS TELEMETRY", color='cyan', fontsize=10)
    ax_telem.tick_params(colors='gray')
    ax_telem.grid(True, alpha=0.2)
    
    # Lines
    line_coh, = ax_telem.plot([], [], 'c-', linewidth=2, label='Coherence (φ)')
    line_feed, = ax_telem.plot([], [], 'r--', linewidth=2, label='Feedback Force')
    ax_telem.axhline(target_coherence, color='gray', linestyle=':', label='Target')
    ax_telem.legend(loc='upper right', facecolor='#111111', edgecolor='none', labelcolor='white')
    
    # Data buffers
    history_t = []
    history_coh = []
    history_feed = []
    
    # Status Text
    txt_status = fig.text(0.5, 0.95, "Initializing System...", ha='center', 
                         color='white', fontsize=14, weight='bold')
    
    print("Starting Control Loop...")
    
    # -------------------------------------------------------------------------
    # SIMULATION LOOP
    # -------------------------------------------------------------------------
    def update(frame):
        nonlocal p1, p2, v1, v2, pos, vel, alpha_base, damping_base
        
        # --- 0. CHAOS INJECTION ---
        if frame == chaos_frame:
            print("💥 CHAOS EVENT DETECTED!")
            txt_status.set_text("💥 CRITICAL: CHAOS INJECTION 💥")
            txt_status.set_color('red')
            # Random massive kick
            kick = (np.random.rand(N_swarm, 3) - 0.5) * chaos_magnitude
            vel += kick.astype(np.float32)
        
        # --- 1. PHYSICS STEP (With Dynamic Parameters) ---
        # Get previous feedback value (or 0 for first frame)
        current_feedback = history_feed[-1] if history_feed else 0.0
        
        # Apply Control Law
        # Feedback strengthens gravity (alpha) and increases viscosity (damping)
        # alpha_eff = alpha * (1 + feedback)
        # damping_eff = damping * (1 - feedback * 0.1)  -> lower value = more damping
        
        alpha_eff = alpha_base * (1.0 + current_feedback * 2.0)
        damping_eff = damping_base * (1.0 - current_feedback * 0.1)
        if damping_eff < 0.90: damping_eff = 0.90 # clamp
        
        # Integrate Sources
        delta = p2 - p1; dist = np.linalg.norm(delta)
        force = 5.0 * delta / (dist**3 + 1e-3)
        p1 += v1 * dt_base; p2 += v2 * dt_base
        v1 += force * dt_base; v2 -= force * dt_base
        sources = [(p1, m_heavy), (p2, m_heavy)]
        
        # Run Physics
        params = {'sigma': sigma, 'alpha': alpha_eff, 'dt': dt_base, 'damping': damping_eff}
        pos, vel = physics.run_simulation_step(pos, vel, sources, params)
        
        # --- 2. PERCEPTION STEP ---
        grid_range = [-4, 4]
        rho_grid = physics.compute_density_grid(
            width, height, grid_range, grid_range, sources, sigma
        )
        
        signatures = perception.compute_spatial_signature(
            rho_grid, width, height, coupling_strength=8.0
        )
        coherence_map = signatures[:, :, 2]
        current_coherence = np.mean(coherence_map)
        
        # --- 3. CONTROL LOGIC (The "Mind") ---
        error = target_coherence - current_coherence
        
        # Only activate feedback if coherence drops BELOW target significantly
        if error > 0.02:
            feedback_signal = error * Kp
        else:
            feedback_signal = 0.0
            
        feedback_signal = np.clip(feedback_signal, 0.0, 1.0) # normalize 0-1
        
        # --- 4. VISUALIZATION UPDATE ---
        img_real.set_data(rho_grid)
        img_perc.set_data(coherence_map)
        
        # Update Telemetry
        history_t.append(frame)
        history_coh.append(current_coherence)
        history_feed.append(feedback_signal)
        
        line_coh.set_data(history_t, history_coh)
        line_feed.set_data(history_t, history_feed)
        
        # Text Logic
        if frame < chaos_frame:
            txt_status.set_text("System Stable | Monitoring...")
            txt_status.set_color('cyan')
        elif frame == chaos_frame:
            pass # handled above
        elif feedback_signal > 0.1:
            txt_status.set_text(f"⚠️ INTERVENTION ACTIVE | Force: {feedback_signal:.2f}")
            txt_status.set_color('orange')
        else:
             txt_status.set_text("System Restabilized.")
             txt_status.set_color('lime')

        if frame % 20 == 0:
            print(f"Step {frame}: Coh={current_coherence:.3f} | Feed={feedback_signal:.3f} | Alpha={alpha_eff:.1f}")
            
        return [img_real, img_perc, line_coh, line_feed, txt_status]

    print("Compiling Animation...")
    ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=40, blit=True)
    
    out_path = "experiments/15_ukft_consciousness_feedback.gif"
    try:
        print(f"Saving to {out_path}...")
        ani.save(out_path, writer='ffmpeg', fps=30, dpi=80) 
        # dpi=80 to keep file size managed for 14-inch figure
    except:
        ani.save(out_path, writer='pillow', fps=30)
    
    print("Done.")

if __name__ == "__main__":
    run_feedback_loop()
