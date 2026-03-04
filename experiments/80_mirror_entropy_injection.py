import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.integrate import quad

# Experiment 80: Mirror Fermion Entropy Injection & CP Asymmetry
# Tests if the "5/9" Entropic Bias in Phase Space leads to the correct branching asymmetry.

os.makedirs("results", exist_ok=True)

def phase_space_integrand(E, mass_parent, mass_product, bias_factor):
    """
    Standard 2-body phase space density roughly proportional to momentum p.
    rho(E) ~ p / M^2
    We modify this with the Entropic Bias term: (1 + bias)
    """
    # Kinematics
    if E < mass_product: return 0.0
    
    # Momentum in rest frame
    # E is energy of product 1 (e.g. top quark)
    # p = sqrt(E^2 - m^2)
    p = np.sqrt(E**2 - mass_product**2)
    
    # Standard Phase Space Density
    rho_0 = p  # Simplified proportionality
    
    # Entropic Bias
    # The Void Scalar prefers Matter states.
    # bias > 0 for Matter, bias < 0 for Antimatter
    rho_biased = rho_0 * (1.0 + bias_factor)
    
    return rho_biased

def run_experiment_80():
    print("--- Experiment 80: Mirror Fermion Entropy Injection ---")
    
    # Constants
    M_mirror = 320.0 # GeV
    M_top = 173.0    # GeV
    M_higgs = 125.0  # GeV
    
    # The "5/9" Factor
    alpha_qed = 1.0/137.036
    factor_5_9 = 5.0/9.0
    
    # Theoretical Bias from Exp 42/79
    # This is the coupling to the Void Scalar
    theoretical_bias = factor_5_9 * alpha_qed
    print(f"Theory Bias (5/9 * alpha): {theoretical_bias:.6e}")
    
    # 1. Calculate Decay Widths (Proportional)
    # Channel: Psi -> t + h
    # We integrate over available energy range for the top quark
    # In 2-body decay, E is fixed, but let's assume a Breit-Wigner width smear
    # or just use the fixed point modulation for simplicity.
    
    # Actually, for 2-body decay, phase space is a point.
    # The density of states at that point is what matters.
    # p_final = sqrt(lambda(M^2, m1^2, m2^2)) / 2M
    
    def kallen_sqrt(x, y, z):
        return np.sqrt((x - y - z)**2 - 4*y*z)
    
    p_final = kallen_sqrt(M_mirror**2, M_top**2, M_higgs**2) / (2 * M_mirror)
    print(f"Final State Momentum p*: {p_final:.4f} GeV")
    
    # The "Matrix Element" |M|^2 contains the coupling.
    # We assume the interaction with Void Scalar modifies the effective coupling g_eff.
    # g_matter = g0 * (1 + delta)
    # g_anti   = g0 * (1 - delta)
    # Width ~ |g|^2 * PhaseSpace
    
    # Void Scalar VEV interaction (Exp 79 logic)
    # The bias defines the probability tilt.
    
    # Matter Width
    # Gamma ~ (1 + bias)^2
    width_matter = (1.0 + theoretical_bias)**2
    
    # Antimatter Width
    # Gamma ~ (1 - bias)^2
    width_antimatter = (1.0 - theoretical_bias)**2
    
    print(f"Prop. Width (Matter)    : {width_matter:.6f}")
    print(f"Prop. Width (Antimatter): {width_antimatter:.6f}")
    
    # 2. Calculate Asymmetry A_CP
    # A_CP = (Gamma_M - Gamma_A) / (Gamma_M + Gamma_A)
    a_cp = (width_matter - width_antimatter) / (width_matter + width_antimatter)
    
    print("-" * 30)
    print(f"Resulting CP Asymmetry A_CP : {a_cp:.6e}")
    print("-" * 30)
    
    # 3. Compare with LHCb "Glitch" (~ 0.5% - 1.0% ?)
    # The experimental values for A_CP in charm/beauty are often 10^-3 to 10^-2 range.
    # LHCb Lambda_b result? 
    # Exp 79 inferred: 0.011 (1.1%)
    # Here:
    
    print("Does this match Exp 79 inferred asymmetry?")
    print(f"Exp 79 Inferred: 0.011677")
    print(f"Exp 80 Derived : {a_cp:.6f}")
    
    ratio = abs(a_cp - 0.011677) / 0.011677
    print(f"Discrepancy: {ratio*100:.2f}%")
    
    # 4. Entropy Calculation
    # S = - Sum p ln p
    total = width_matter + width_antimatter
    p_m = width_matter / total
    p_a = width_antimatter / total
    
    print("\nEntropic Budget:")
    print(f"P(Matter)    : {p_m:.6f}")
    print(f"P(Antimatter): {p_a:.6f}")
    
    entropy = - (p_m * np.log(p_m) + p_a * np.log(p_a))
    max_entropy = np.log(2) # 0.693147
    
    efficiency = 1.0 - (entropy / max_entropy)
    print(f"Shannon Entropy: {entropy:.6f} nats")
    print(f"Max Entropy    : {max_entropy:.6f} nats")
    print(f"Diff (Info)    : {max_entropy - entropy:.6e} nats")
    print(f"Asymmetry Cost : {efficiency:.6e}")
    
    # 5. Check against 5/9 * alpha
    # Is the Information Injection (Diff) related to 5/9 * alpha?
    reference = factor_5_9 * alpha_qed
    print(f"\nReference (5/9 * alpha): {reference:.6e}")
    
    # Relation check
    # Diff ~ 0.5 * bias^2 ?
    # Let's check magnitude of A_CP vs Reference
    # A_CP is approx 2 * bias (if simple square)
    # A_CP / 2 = bias ?
    print(f"A_CP / 2               : {a_cp/2:.6e}")
    
    # Plotting
    biases = np.linspace(0, 0.02, 100)
    acps = []
    entropies = []
    
    for b in biases:
        w_m = (1+b)**2
        w_a = (1-b)**2
        acp = (w_m - w_a)/(w_m + w_a)
        acps.append(acp)
        
        pm = w_m / (w_m + w_a)
        pa = w_a / (w_m + w_a)
        ent = -(pm*np.log(pm) + pa*np.log(pa))
        entropies.append(np.log(2) - ent) # Information Gain
        
    plt.figure(figsize=(10,6))
    plt.subplot(1,2,1)
    plt.plot(biases, acps, label="A_CP")
    plt.axvline(x=theoretical_bias, color='r', linestyle='--', label="5/9 * alpha")
    plt.scatter([theoretical_bias], [a_cp], color='r')
    plt.xlabel("Entropic Bias (coupling)")
    plt.ylabel("Asymmetry A_CP")
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1,2,2)
    plt.plot(biases, entropies, label="Info Gain (dEntropy)")
    plt.axvline(x=theoretical_bias, color='r', linestyle='--')
    plt.xlabel("Entropic Bias (coupling)")
    plt.ylabel("Information Gain (nats)")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig("results/80_mirror_entropy_injection.png")
    print("Plot saved to results/80_mirror_entropy_injection.png")

if __name__ == "__main__":
    run_experiment_80()
