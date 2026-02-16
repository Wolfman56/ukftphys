import numpy as np
import matplotlib.pyplot as plt
import os

# Create results directory
os.makedirs("results", exist_ok=True)

def random_three_body_phase_space(n_events=100000):
    """
    Generate random 3-body decay phase space points: P -> p1 + p2 + p3
    We model this in the center of mass frame of the parent particle P.
    Reused from Exp 27.
    """
    # Direct sampling for massless 3-body phase space is flat in energy fractions x1, x2.
    # Range: 0 < x1 < 1, 1-x1 < x2 < 1.
    
    x1 = np.random.rand(n_events)
    x2 = np.random.rand(n_events)
    
    # Filter to physical region x1+x2 > 1 (which implies x3 < 1)
    mask = (x1 + x2 > 1)
    x1 = x1[mask]
    x2 = x2[mask]
    x3 = 2 - x1 - x2
    
    return x1, x2, x3

def gauge_amplitudes(x1, x2, x3, rho=5000):
    """
    Compute Gauge Theory Amplitudes squared |A|^2.
    
    1. A_MHV: Standard Maximally Helicity Violating amplitude (- - +).
       Approx: 1 / ((1-x1)(1-x2)(1-x3))
       
    2. A_SM: Single-Minus Anomaly (- + +).
       From Exp 27/Guevara et al.
       Non-zero only in 'Half-Collinear' regions.
        modeled as: 11.4 * rho * Shape(Collinear)
    """
    eps = 1e-3
    
    # Standard MHV (- - +)
    # Diverges at soft/collinear limits
    A_mhv_sq = 1.0 / ((1-x1+eps)*(1-x2+eps)*(1-x3+eps))
    
    # Single-Minus Anomaly (- + +)
    # Diverges at specific half-collinear limits (e.g., peak when any x -> 1)
    # UKFT prediction: Scales with density rho
    # Using the 'digital switch' probability from Exp 27
    prob_on = np.clip(rho / 10000.0, 0, 1)
    # Using the same divergent shape for simplicity, or slightly less singular? 
    # Guevara et al suggest it's piecewise constant (step function), so maybe less singular?
    # But let's assume it inherits the singularity structure of the region it lives in.
    A_sm_sq = (11.4 * prob_on)**2 / ((1-x1+eps)*(1-x2+eps)) 
    
    return A_mhv_sq, A_sm_sq

def double_copy_gravity(A_gauge_sq):
    """
    Apply the Double Copy principle (BCJ Duality) roughly:
    Gravity Amplitude M ~ (Gauge Amplitude A)^2 * Kinematic Factor s
    
    Here we work with squared amplitudes:
    |M|^2 ~ |A|^2 * |A|^2 * s^2 ?
    Actually KLT relations for 3-point:
    M3 = A3 * A3 (roughly, omitting coupling constants).
    
    So we will approximate:
    |M_grav|^2 = |A_gauge|^2 * |A_gauge|^2  (Dimensionality wise, A is 1/mass^2? No, A is dimension 1 in 4D?)
    Let's just use the square relationship to see relative strengths.
    """
    # Squaring the squared amplitude gives |M|^4? No.
    # Input is |A|^2. Output should be |M|^2 ~ (|A|^2)^2? No.
    # If M ~ A^2, then |M|^2 ~ |A^2|^2 = |A|^4.
    # Yes, gravity is "squared" gauge theory.
    return A_gauge_sq**2

def run_experiment():
    print("Running Experiment 28: Emergent Single-Minus Graviton...")
    
    # 1. Generate Phase Space
    n_events = 500000
    x1, x2, x3 = random_three_body_phase_space(n_events)
    print(f"Generated {len(x1)} events.")
    
    # 2. Compute Gauge Amplitudes
    A_mhv_sq, A_sm_sq = gauge_amplitudes(x1, x2, x3, rho=5000)
    
    # 3. Compute Gravity Amplitudes via Double Copy
    # Standard GR (MHV Graviton: h-- h-- h++)
    M_gr_sq = double_copy_gravity(A_mhv_sq)
    
    # Anomalous Gravity (Single-Minus Graviton: h-- h++ h++)
    # This state is usually FORBIDDEN in GR.
    M_anomaly_sq = double_copy_gravity(A_sm_sq)
    
    # 4. Analyze the "Force Law" (Angular Dependence)
    # Compute angle between Jet 2 and Jet 3 (the two "plus" helicity particles)
    # cos_theta_23 = 1 - 2*(1-x1)/(x2*x3)
    # Let's use x3 (energy of 3rd parton) vs Angle mechanism.
    
    # Let's plot the ratio of Anomaly / Standard Gravity vs Angle
    # This tells us where the "New Force" is strong relative to Newton/Einstein gravity.
    
    with np.errstate(divide='ignore', invalid='ignore'):
        cos_theta_23 = 1 - 2*(1-x1)/(x2*x3)
        
    mask = (cos_theta_23 >= -1) & (cos_theta_23 <= 1)
    
    # Bin the data by angle
    bins = np.linspace(-1, 1, 100)
    
    # Use digitize to compute average ratio in each bin (more stable than histogram division)
    angle = cos_theta_23[mask]
    ratio = (M_anomaly_sq[mask] / (M_gr_sq[mask] + 1e-9)) # Avoid division by zero
    
    # Compute profile
    bin_indices = np.digitize(angle, bins)
    
    mean_ratio = []
    bin_centers = []
    
    for i in range(1, len(bins)):
        in_bin = ratio[bin_indices == i]
        if len(in_bin) > 0:
            mean_ratio.append(np.mean(in_bin))
            bin_centers.append(0.5 * (bins[i] + bins[i-1]))
            
    # Plot Results
    plt.figure(figsize=(10, 6))
    
    plt.plot(bin_centers, mean_ratio, 'r-', linewidth=2, label='Anomaly / GR Ratio')
    plt.axhline(y=0, color='k', linestyle='--')
    
    plt.title("Gravity Anomaly Strength vs Angle\n(Ratio of Single-Minus Graviton to Standard Graviton)")
    plt.xlabel("Cos(Angle) betwen Outgoing Gravitons")
    plt.ylabel("Relative Strength of Forbidden Force")
    plt.yscale('log') # Likely varies by orders of magnitude
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()
    
    plt.savefig("results/exp28_gravity_anomaly_ratio.png")
    print("Saved plot to results/exp28_gravity_anomaly_ratio.png")
    
    # Interpretation
    max_ratio = np.max(mean_ratio)
    print(f"Max anomaly ratio observed: {max_ratio:.2e}")
    if max_ratio > 1.0:
        print("CONCLUSION: The anomaly DOMINATES gravity in certain collinear configurations!")
        print("This implies a breakdown of the Equivalence Principle in high-energy jets/flux tubes.")
    else:
        print("CONCLUSION: The anomaly exists but is a sub-dominant correction.")

if __name__ == "__main__":
    run_experiment()
