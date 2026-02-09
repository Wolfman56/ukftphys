import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# Ensure local package is findable for utility
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_experiment():
    print("Initializing UKFT Experiment 17: Dual-Source Entanglement Resolution...")
    
    # Constants
    Dx = 0.2
    Dt = 0.05
    L_phys = 40.0
    X = np.arange(-L_phys/2, L_phys/2, Dx)
    N = len(X)
    c_speed = 5.0
    
    # Locations
    loc_A = -10.0 # Alice
    loc_B = 10.0  # Bob
    
    # Time Evolution
    T_steps = 400
    event_time_idx = 50
    
    # History buffers
    hist_info_A = [] # Signal from A
    hist_info_B = [] # Signal from B
    
    # Store "Status" strings for A and B to display on plot
    status_history_A = []
    status_history_B = []

    print(f"Simulating {T_steps} steps of Dual-Choice Propagation...")
    
    for t_idx in range(T_steps):
        time_sim = t_idx * Dt
        
        # 1. Propagate Signals (Analytic Light Cones)
        info_A = np.zeros(N)
        info_B = np.zeros(N)
        
        if t_idx >= event_time_idx:
            delta_t = (t_idx - event_time_idx) * Dt
            radius = c_speed * delta_t
            
            # Simple expanding spheres
            # Signal A (Alerts about 'Down' measurement at A)
            dist_A = np.abs(X - loc_A)
            info_A = 1.0 / (1.0 + np.exp(5.0 * (dist_A - radius)))
            
            # Signal B (Alerts about 'Up' measurement at B)
            dist_B = np.abs(X - loc_B)
            info_B = 1.0 / (1.0 + np.exp(5.0 * (dist_B - radius)))

        hist_info_A.append(info_A)
        hist_info_B.append(info_B)
        
        # 2. Determine State/Status at Detectors
        # Check if Signal B has reached A
        has_signal_B_reached_A = False
        has_signal_A_reached_B = False
        
        if t_idx >= event_time_idx:
            # Distance needed
            dist_AB = abs(loc_B - loc_A)
            travel_time = dist_AB / c_speed
            time_elapsed = (t_idx - event_time_idx) * Dt
            
            if time_elapsed >= travel_time:
                has_signal_B_reached_A = True
                has_signal_A_reached_B = True
                
        # Status A Logic
        if t_idx < event_time_idx:
            sta = "SUPERPOSITION (Entangled)"
            stb = "SUPERPOSITION (Entangled)"
        else:
            if not has_signal_B_reached_A:
                sta = "LOCAL: DOWN | WAITING FOR B..." # Zombie/Pending
                stb = "LOCAL: UP | WAITING FOR A..."
            else:
                sta = "RESOLVED: DOWN (Confirmed B=UP)" # Consistency Check Passed
                stb = "RESOLVED: UP (Confirmed A=DOWN)"
        
        status_history_A.append(sta)
        status_history_B.append(stb)

    # Visualization
    print("Generating Dual-Wave Animation...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Draw static detectors
    ax.axvline(loc_A, color='k', linestyle=':', alpha=0.3)
    ax.axvline(loc_B, color='k', linestyle=':', alpha=0.3)
    ax.text(loc_A, 1.05, "Alice", ha='center', fontweight='bold')
    ax.text(loc_B, 1.05, "Bob", ha='center', fontweight='bold')
    
    # Lines
    line_sig_A, = ax.plot(X, hist_info_A[0], 'r--', lw=2, label="Signal from A (Is Down)")
    line_sig_B, = ax.plot(X, hist_info_B[0], 'b--', lw=2, label="Signal from B (Is Up)")
    
    # Fill between to show "Resolved Zone" (where both signals exist)
    # fill_resolved = ax.fill_between(X, 0, 0, color='purple', alpha=0.1, label='Causal Agreement Zone')
    
    # Text
    txt_time = ax.text(0.5, 1.05, '', transform=ax.transAxes, ha='center', fontsize=12)
    txt_stat_A = ax.text(0.15, 0.5, '', transform=ax.transAxes, ha='left', color='red', fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='red'))
    txt_stat_B = ax.text(0.85, 0.5, '', transform=ax.transAxes, ha='right', color='blue', fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='blue'))

    ax.set_ylim(-0.1, 1.2)
    ax.set_xlim(-L_phys/2, L_phys/2)
    ax.set_ylabel("Causal Information Level")
    ax.set_xlabel("Position")
    ax.set_title("UKFT Exp 17b: Dual Source Entanglement Resolution")
    ax.legend(loc='lower center')
    ax.grid(True, alpha=0.2)

    def animate(i):
        # Update lines
        data_A = hist_info_A[i]
        data_B = hist_info_B[i]
        line_sig_A.set_ydata(data_A)
        line_sig_B.set_ydata(data_B)
        
        # Text
        current_time = i * Dt
        txt_time.set_text(f"Time: {current_time:.2f}")
        
        # Status
        txt_stat_A.set_text(status_history_A[i])
        txt_stat_B.set_text(status_history_B[i])
        
        return line_sig_A, line_sig_B, txt_time, txt_stat_A, txt_stat_B

    ani = animation.FuncAnimation(fig, animate, frames=T_steps, interval=25, blit=False)
    
    save_path = 'experiments/17_ukft_entanglement_propagation.gif'
    print(f"Saving to {save_path}...")
    ani.save(save_path, writer='pillow', fps=30)
    print("Done.")

if __name__ == "__main__":
    run_experiment()
