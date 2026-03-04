import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Experiment 79: Entropic CP Asymmetry from Void Scalar Bias
# Tests the hypothesis that Matter/Antimatter asymmetry emerges from the Choice Operator
# acting on the Void Scalar field with a "5/9" entropic bias.

# Create results directory
os.makedirs("results", exist_ok=True)
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def run_entropic_cp_simulation(
    grid_size=30, 
    steps=5000, 
    n_particles=20000, 
    alpha_qed=1.0/137.036,
    coupling_factor=5.0/9.0, # The "5/9" Rule
    epsilon_void=0.2,        # Vacuum floor from Exp 47
    sim_amplification=50.0   # Amplify small effect for visibility
):
    print(f"--- Experiment 79: Entropic CP Asymmetry Simulation ---")
    print(f"Grid Size: {grid_size}^3")
    print(f"Particles: {n_particles} Baryons, {n_particles} Antibaryons")
    print(f"Coupling Bias (delta): {coupling_factor} * alpha = {coupling_factor * alpha_qed:.6f}")
    print(f"Simulation Amplification: {sim_amplification}x")
    
    # 1. Initialize Void Scalar Field (Phi)
    # The field fluctuates but maintains a non-zero vacuum expectation value (VEV)
    # due to the "Existence Constraint" |phi| > epsilon
    phi = np.random.uniform(epsilon_void, 1.0, size=(grid_size, grid_size, grid_size))
    
    # 2. Initialize Particles
    # Structure: [x, y, z, type] where type = +1 (Baryon), -1 (Antibaryon)
    # Status: 1 = Active, 0 = Decayed/Annihilated
    particles = np.zeros((2 * n_particles, 5)) 
    
    # Baryons
    particles[:n_particles, 0:3] = np.random.randint(0, grid_size, size=(n_particles, 3))
    particles[:n_particles, 3] = 1.0  # Type
    particles[:n_particles, 4] = 1.0  # Status
    
    # Antibaryons
    particles[n_particles:, 0:3] = np.random.randint(0, grid_size, size=(n_particles, 3))
    particles[n_particles:, 3] = -1.0 # Type
    particles[n_particles:, 4] = 1.0  # Status
    
    # Track History
    history_baryons = []
    history_antibaryons = []
    asymmetry_log = []
    
    # Entropic Bias Parameter
    # This represents the "tilt" in the Choice Operator due to the Mirror Fermion reflection
    # delta ~ (Gamma/M) ~ (5/9) * alpha
    ent_bias = coupling_factor * alpha_qed
    
    print("Starting Simulation Loop...")
    
    for t in range(steps):
        # A. Evolve Scalar Field (Metropolis - Simplified from Exp 47)
        # Random fluctuation
        noise = np.random.normal(0, 0.05, size=(grid_size, grid_size, grid_size))
        phi_new = phi + noise
        
        # Apply Vacuum Constraint (Hard Wall at epsilon)
        # If |phi| < epsilon, the "Pressure" restores it. 
        # Here we just clamp it or reject. Let's clamp to maintain VEV.
        # This creates a persistent "positive" field if initialized positive.
        # (Assuming Spontaneous Symmetry Breaking has chosen +ve sector)
        phi_new = np.where(np.abs(phi_new) < epsilon_void, 
                           np.sign(phi_new) * epsilon_void + 0.01 * np.random.randn(), 
                           phi_new)
        
        # Energy/Smoothness Update (Diffusion)
        # phi_new += 0.1 * laplacian(phi) ... simplified as weighted average
        phi = 0.9 * phi + 0.1 * phi_new 
        
        # B. Evolve Particles (Choice Operator) - Vectorized
        active_mask = particles[:, 4] == 1.0
        n_active = np.sum(active_mask)
        
        if n_active > 0:
            # 1. Random Walk
            moves = np.random.randint(-1, 2, size=(n_active, 3))
            current_pos = particles[active_mask, 0:3].astype(int)
            new_pos = (current_pos + moves) % grid_size
            particles[active_mask, 0:3] = new_pos
            
            # 2. Entropic Survival Check
            # Get local phi values
            # Vectorized indexing: phi[x, y, z]
            local_phi = phi[new_pos[:, 0], new_pos[:, 1], new_pos[:, 2]]
            
            # Interaction: Type * Effective Bias * Phi
            types = particles[active_mask, 3]
            effective_interactions = types * ent_bias * sim_amplification * local_phi
            
            # Decay Probability
            base_decay_prob = 0.001
            decay_probs = base_decay_prob * np.exp(-effective_interactions)
            
            # Decay Event
            random_rolls = np.random.rand(n_active)
            decayed = random_rolls < decay_probs
            
            # Update Status
            # We need to map back to original indices
            # Or just update the values in place for the active subset?
            # Assigning to particles[active_mask, 4] works in numpy
            current_status = particles[active_mask, 4]
            current_status[decayed] = 0.0
            particles[active_mask, 4] = current_status
                
        # C. Counts
        n_b = np.sum((particles[:, 3] == 1.0) & (particles[:, 4] == 1.0))
        n_ab = np.sum((particles[:, 3] == -1.0) & (particles[:, 4] == 1.0))
        
        history_baryons.append(n_b)
        history_antibaryons.append(n_ab)
        
        if (n_b + n_ab) > 0:
            a_cp = (n_b - n_ab) / (n_b + n_ab)
        else:
            a_cp = 0.0
        asymmetry_log.append(a_cp)
        
        if t % 500 == 0:
            print(f"Step {t:4d}: B={n_b}, anti-B={n_ab}, A_CP={a_cp:.5f}")

    # Final Analysis
    final_b = history_baryons[-1]
    final_ab = history_antibaryons[-1]
    final_acp = asymmetry_log[-1]
    
    # Scale back the observed asymmetry by the amplification factor
    # A_obs ~ bias * Amp * T
    # A_true ~ A_obs / Amp
    inferred_asymmetry = final_acp / sim_amplification
    
    print("-" * 40)
    print(f"Final Count: Baryons={final_b}, Antibaryons={final_ab}")
    print(f"Final Raw Asymmetry (A_CP): {final_acp:.6f}")
    print(f"Inferred Physical Asymmetry: {inferred_asymmetry:.6f}")
    
    # Check 5/9 prediction
    predicted_bias_mag = coupling_factor * alpha_qed
    print(f"Theoretical Bias (5/9 * alpha): {predicted_bias_mag:.6f}")
    
    # Ratio
    if predicted_bias_mag > 0:
        ratio = inferred_asymmetry / predicted_bias_mag
        print(f"Ratio (Inferred / Theoretical): {ratio:.2f}")
    
    # Plotting
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(history_baryons, label='Baryons (Matter)', color='blue')
    plt.plot(history_antibaryons, label='Antibaryons (Antimatter)', color='red', linestyle='--')
    plt.xlabel('Time Step')
    plt.ylabel('Count')
    plt.title('Matter vs Antimatter Survival')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(asymmetry_log, color='purple')
    plt.xlabel('Time Step')
    plt.ylabel('Asymmetry A_CP')
    plt.title(f'Emergent Asymmetry (Target ~ {predicted_bias_mag:.4f} order)')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='black', alpha=0.5)
    
    # Add theoretical band (roughly proportional to bias parameter)
    # The actual A_CP aggregation depends on the integration time, typically A ~ bias * T_effective
    
    plt.tight_layout()
    plt.savefig(f"results/79_entropic_cp_asymmetry_{TIMESTAMP}.png")
    print(f"Plot saved to results/79_entropic_cp_asymmetry_{TIMESTAMP}.png")

if __name__ == "__main__":
    run_entropic_cp_simulation()
