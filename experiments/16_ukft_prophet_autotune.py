# experiments/16_ukft_prophet_autotune.py
"""
Experiment 16: Prophet Autotuning (The God Attractor) 🛐

We test the hypothesis that the "Fundamental Constants" of the universe
(Gravity Strength 'Alpha', Space-Time Sharpness 'Sigma') are not arbitrary,
but are emergent values that evolved to maximize Quantum Coherence (Harlow's Constraint).

Protocol:
1. Start with a chaotic, unstable universe (random/sub-optimal constants).
2. Run the Prophet Control Loop:
   - Measure Global Coherence (\phi).
   - Perturb constants (\alpha, \sigma) stochastically (Mutation).
   - Selection: If coherence improves, adopt new constants. (Evolution).
3. Observe if the system converges to a specific "God Attractor" point in parameter space.
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

def run_god_attractor_search():
    print("🛐 Initializing Prophet Autotuner...")
    
    physics = EntropicGPUAccelerator()
    perception = WebGPUPerceptionAccelerator()
    
    # -------------------------------------------------------------------------
    # CONFIGURATION
    # -------------------------------------------------------------------------
    N_swarm = 60_000
    n_steps = 400
    width, height = 256, 256
    
    # Initial "Bad" Gene Pool
    # We start with weak gravity and blurry spacetime -> Low structure
    current_alpha = 2.0  # Target is around 12-15
    current_sigma = 1.2  # Target is around 0.5-0.6 (Sharp)
    current_damping = 0.95 
    
    # Optimization Params
    learning_rate_alpha = 0.5
    learning_rate_sigma = 0.05
    
    # Physics State
    dt = 0.02
    
    # -------------------------------------------------------------------------
    # INITIALIZATION
    # -------------------------------------------------------------------------
    # Binary Star (Static Pattern for consistency during tuning)
    m_heavy = 15.0
    p1 = np.array([ 1.5,  0.0, 0.0]); v1 = np.array([ 0.0,  0.5, 0.0])
    p2 = np.array([-1.5,  0.0, 0.0]); v2 = np.array([ 0.0, -0.5, 0.0])
    
    # Swarm: Diffuse Cloud (High Entropy start)
    pos = (np.random.rand(N_swarm, 3).astype(np.float32) - 0.5) * 8.0
    pos[:, 2] *= 0.2 # Flatten slightly
    vel = (np.random.rand(N_swarm, 3).astype(np.float32) - 0.5) * 0.1
    
    # -------------------------------------------------------------------------
    # VISUALIZATION
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(16, 9), facecolor='#050505')
    gs = GridSpec(2, 3, width_ratios=[2, 1, 1], height_ratios=[1, 1], figure=fig)
    
    # 1. The Universe (Density View)
    ax_univ = fig.add_subplot(gs[:, 0]) # Left Half
    ax_univ.set_title("THE UNIVERSE (Emergent Structure)", color='white')
    ax_univ.axis('off')
    img_univ = ax_univ.imshow(np.zeros((height, width)), cmap='magma', 
                             origin='lower', vmin=0, vmax=15)
    
    # 2. Parameter Space (The God Attractor)
    ax_phase = fig.add_subplot(gs[0, 1])
    ax_phase.set_title("PARAMETER SPACE (Searching...)", color='lime')
    ax_phase.set_facecolor('#111111')
    ax_phase.set_xlabel('Gravity (Alpha)', color='gray')
    ax_phase.set_ylabel('Sharpness (1/Sigma)', color='gray') # Plot inverse sigma
    ax_phase.tick_params(colors='white')
    ax_phase.grid(True, alpha=0.1)
    ax_phase.set_xlim(0, 25)
    ax_phase.set_ylim(0, 3.0) 
    
    line_path, = ax_phase.plot([], [], 'o-', color='lime', markersize=3, alpha=0.6)
    point_curr, = ax_phase.plot([], [], 'Dw', markersize=8) # Current state
    
    # 3. Coherence Metric (The Goal Function)
    ax_metric = fig.add_subplot(gs[1, 1])
    ax_metric.set_title("GLOBAL COHERENCE (\u03C6)", color='cyan')
    ax_metric.set_facecolor('#111111')
    ax_metric.set_xlim(0, n_steps)
    ax_metric.set_ylim(0, 1.0)
    ax_metric.tick_params(colors='white')
    
    line_coh, = ax_metric.plot([], [], 'c-', linewidth=2)
    
    # 4. Text Output
    ax_text = fig.add_subplot(gs[:, 2])
    ax_text.axis('off')
    txt_info = ax_text.text(0.1, 0.5, "Initializing...", color='white', 
                           fontsize=12, family='monospace', va='center')
    
    # Buffers
    hist_alpha = []
    hist_inv_sigma = []
    hist_coh = []
    hist_frames = []
    
    # Optimization State
    best_coherence = 0.0
    
    print("Starting Evolution...")
    
    def update(frame):
        nonlocal p1, p2, v1, v2, pos, vel
        nonlocal current_alpha, current_sigma, best_coherence
        
        # --- 1. PHYSICS STEP ---
        # Update Stars
        delta = p2 - p1; dist = np.linalg.norm(delta)
        force = 5.0 * delta / (dist**3 + 1e-3)
        p1 += v1 * dt; p2 += v2 * dt
        v1 += force * dt; v2 -= force * dt
        sources = [(p1, m_heavy), (p2, m_heavy)]
        
        # Run Physics with CURRENT GENES
        params = {'sigma': current_sigma, 'alpha': current_alpha, 'dt': dt, 'damping': current_damping}
        pos, vel = physics.run_simulation_step(pos, vel, sources, params)
        
        # --- 2. PERCEPTION STEP ---
        grid_range = [-5, 5]
        rho_grid = physics.compute_density_grid(
            width, height, grid_range, grid_range, sources, current_sigma
        )
        
        signatures = perception.compute_spatial_signature(
            rho_grid, width, height, coupling_strength=8.0
        )
        coherence_map = signatures[:, :, 2]
        current_coherence = np.mean(coherence_map)
        
        # --- 3. EVOLUTION STEP (Autotuning) ---
        # Simple Gradient Ascent / Hill Climbing logic
        # Every 10 frames, try a mutation
        if frame % 5 == 0 and frame > 20: 
            # We want to Maximize Coherence
            # Bias direction: High Alpha, Low Sigma typically = Structure
            # But let the system find it.
            
            # Error term: How far are we from Unity? (Harlow)
            delta_coh = current_coherence - best_coherence
            
            if current_coherence >= best_coherence * 0.99:
                 # It's good or getting better, keep pushing in same direction roughly
                 # Or add random momentum
                 best_coherence = current_coherence
                 
                 # Mutation: Exploration
                 d_alpha = (np.random.rand() - 0.4) * learning_rate_alpha # slight bias up
                 d_sigma = (np.random.rand() - 0.6) * learning_rate_sigma # slight bias down (sharper)
                 
            else:
                 # It got worse! Revert/Panic
                 # Since we can't rewind time easily in this loop, we just invert the gradient of change
                 # Actually, just random jump back towards known good
                 d_alpha = (np.random.rand() - 0.5) * learning_rate_alpha * 5.0
                 d_sigma = (np.random.rand() - 0.5) * learning_rate_sigma * 2.0
            
            # Apply genes
            current_alpha += d_alpha
            current_sigma += d_sigma
            
            # Constraints
            current_alpha = np.clip(current_alpha, 0.5, 25.0)
            current_sigma = np.clip(current_sigma, 0.1, 3.0)

        # --- 4. VISUALIZATION ---
        img_univ.set_data(rho_grid)
        
        # Phase Plot
        hist_alpha.append(current_alpha)
        hist_inv_sigma.append(1.0/current_sigma)
        hist_coh.append(current_coherence)
        hist_frames.append(frame)
        
        line_path.set_data(hist_alpha, hist_inv_sigma)
        point_curr.set_data([current_alpha], [1.0/current_sigma])
        
        line_coh.set_data(hist_frames, hist_coh)
        
        # Text
        info = (
            f"STEP: {frame}\n\n"
            f"GENES (CONSTANTS):\n"
            f" Alpha (G):   {current_alpha:.2f}\n"
            f" Sigma (S):   {current_sigma:.2f}\n"
            f" 1/Sigma:     {1.0/current_sigma:.2f}\n\n"
            f"METRICS:\n"
            f" Coherence:   {current_coherence:.4f}\n\n"
            f"STATUS:\n"
            f" {'CONVERGING' if current_coherence > 0.6 else 'CHAOS'}"
        )
        txt_info.set_text(info)
        
        if frame % 20 == 0:
            print(f"Gen {frame}: Alpha={current_alpha:.2f} Sigma={current_sigma:.2f} -> Coh={current_coherence:.3f}")
            
        return [img_univ, line_path, point_curr, line_coh, txt_info]

    ani = animation.FuncAnimation(fig, update, frames=n_steps, interval=30, blit=True)
    
    out_path = "experiments/16_ukft_prophet_autotune.gif"
    try:
        print(f"Saving to {out_path}...")
        ani.save(out_path, writer='ffmpeg', fps=30, dpi=80) 
        print("Done.")
    except:
        print("FFMpeg missing, using pillow")
        ani.save(out_path, writer='pillow', fps=30)

if __name__ == "__main__":
    run_god_attractor_search()
