import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# Ensure local package is findable for utility
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_experiment():
    print("Initializing UKFT Experiment 18: Learning the Speed of Light...")
    print("Hypothesis: 'c' is the emergent solution to minimizing Action (Lag) while maintaining Stability (Grid Causality).")

    # -------------------------------------------------------------------------
    # 1. Simulation Setup (The "Planck Grid")
    # -------------------------------------------------------------------------
    N = 100
    L_phys = 20.0
    Dx = L_phys / N
    Dt = 0.05
    
    # Fundamental Grid Limit (Courant Condition Boundary)
    # C_max = Dx / Dt 
    # If c > C_max, the "Universe" (Solver) should explode.
    
    c_limit_theoretical = Dx / Dt
    print(f"Space Quanta (Dx): {Dx:.3f}")
    print(f"Time Quanta (Dt): {Dt:.3f}")
    print(f"Theoretical Max Speed (c_grid): {c_limit_theoretical:.3f}")
    
    # -------------------------------------------------------------------------
    # 2. Results Containers for the Sweep
    # -------------------------------------------------------------------------
    # Sweep from safe to unstable
    c_values = np.linspace(1.0, 6.0, 50) 
    consistency_scores = []
    stability_scores = []
    
    # -------------------------------------------------------------------------
    # 3. Wave Solver Function
    # -------------------------------------------------------------------------
    def solve_causality_field(c_speed):
        """
        Runs the simulation for a specific Speed of Light 'c_speed'.
        Returns:
          - consistency (Inverse of time to resolve)
          - stability (Inverse of maximum anomalous field spikes)
        """
        # Initialize Field u (Information presence)
        # u[t, x]
        u_prev = np.zeros(N)
        u_curr = np.zeros(N)
        u_next = np.zeros(N)
        
        # Trigger event at center (Source of Reality)
        # Initial Gaussian pulse
        center_idx = N // 2
        u_prev[center_idx] = 1.0
        u_curr[center_idx] = 1.0
        # Add slight spread for numerical smoothness start
        u_prev[center_idx-1] = 0.5; u_prev[center_idx+1] = 0.5
        u_curr[center_idx-1] = 0.5; u_curr[center_idx+1] = 0.5
        
        # Courant Number
        C = c_speed * Dt / Dx
        C2 = C**2
        
        T_steps = 150
        
        exploded = False
        resolved_time = T_steps * Dt # Worst case default
        
        monitor_point_idx = int(0.7 * N) # Observer at some distance
        
        for t in range(T_steps):
            # Finite Difference Wave Equation: u_next = 2*u - u_prev + C^2 * (u_xx)
            # Standard 2nd order central difference
            
            # Vectorized Laplacian (with fixed boundary 0)
            u_xx = np.zeros(N)
            u_xx[1:-1] = u_curr[2:] - 2*u_curr[1:-1] + u_curr[:-2]
            
            u_next[1:-1] = 2*u_curr[1:-1] - u_prev[1:-1] + C2 * u_xx[1:-1]
            
            # Check for Explosion (Stability Metric)
            max_val = np.max(np.abs(u_next))
            if max_val > 10.0: # "Reality Breaking" threshold
                exploded = True
                return 0.0, 0.0 # FAIL: Universe ceased to exist
                
            # Check for Resolution (Signal Arrival at Observer)
            if u_next[monitor_point_idx] > 0.1 and resolved_time == T_steps * Dt:
                resolved_time = t * Dt
            
            # Cycle buffers
            u_prev[:] = u_curr[:]
            u_curr[:] = u_next[:]
            
        # Metrics
        # Consistency Score: Higher is better (Faster resolution)
        # Avoid div by zero
        consistency = 1.0 / (resolved_time + 0.1)
        
        # Stability Score:
        if exploded:
            return 0.0, 0.0
            
        return consistency, 1.0

    # -------------------------------------------------------------------------
    # 4. Run the "Evolution" (Parameter Sweep)
    # -------------------------------------------------------------------------
    print("Running Parameter Sweep/Evolution...")
    
    final_metrics = []
    
    for c_val in c_values:
        cons, stab = solve_causality_field(c_val)
        final_metrics.append((c_val, cons, stab))

    # Convert to arrays
    c_arr = np.array([x[0] for x in final_metrics])
    cons_arr = np.array([x[1] for x in final_metrics])
    
    # -------------------------------------------------------------------------
    # 5. Determine "Evolved" c
    # -------------------------------------------------------------------------
    # The Universe wants to Maximize Consistency (Speed), 
    # BUT constrained by Stability (Existence).
    # So it picks the highest c before it fails.
    
    valid_indices = np.where(cons_arr > 0)[0]
    if len(valid_indices) > 0:
        best_idx = valid_indices[-1] # The last valid one (highest speed)
        learned_c = c_arr[best_idx]
        best_cons = cons_arr[best_idx]
    else:
        learned_c = 0.0
        best_cons = 0.0
        
    print(f"\nRESULTS:")
    print(f"Grid Maximum (CFL limit): {c_limit_theoretical:.3f}")
    print(f"Universe 'Learned' Speed: {learned_c:.3f}")
    
    if abs(learned_c - c_limit_theoretical) < 0.5:
        print(">> SUCCESS: The universe optimized 'c' to match the Grid Resolution limit!")
        print(">> 'c' is physically equivalent to 1 pixel per tick.")
    
    # -------------------------------------------------------------------------
    # 6. Visualization
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot Consistency vs c
    # Mask zeros
    masked_cons = cons_arr.copy()
    masked_cons[masked_cons == 0] = np.nan
    
    ax.plot(c_arr, masked_cons, 'o-', color='cyan', label='Causal Efficiency (1/Lag)')
    
    # Vertical line for Theoretical Limit
    ax.axvline(c_limit_theoretical, color='red', linestyle='--', label=f'Stability Limit (CFL) = {c_limit_theoretical:.2f}')
    
    # Marker for Learned c
    ax.plot(learned_c, best_cons, 'r*', markersize=20, label=f"Learned 'c' = {learned_c:.2f}")
    
    ax.set_title("UKFT Exp 18: The Emergence of the Speed of Light")
    ax.set_xlabel("Candidate Speed (c)")
    ax.set_ylabel("Fitness (Resolving Power)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.text(0.05, 0.95, "Result: The Universe maximizes 'c' until SpaceTime tears", transform=ax.transAxes, color='white', bbox=dict(facecolor='black', alpha=0.7))
    
    save_fig = 'experiments/18_ukft_learning_c_results.png'
    plt.savefig(save_fig)
    print(f"Saved results to {save_fig}")
    

if __name__ == "__main__":
    run_experiment()
