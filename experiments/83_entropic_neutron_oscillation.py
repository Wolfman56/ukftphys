import numpy as np
import matplotlib.pyplot as plt
import os

# Experiment 83: Entropic Suppression of Neutron-Antineutron Oscillation
# Testing the "Static Vacuum Bias" (0.4%) on cold systems.
# Hypothesis: The Entropic Bias acts as a potential difference V = 2 * delta * m_n
# This splitting (approx 7.5 MeV) completely detunes the n-nbar transition,
# stabilizing matter against spontaneous oscillation into antimatter.

OUTPUT_DIR = "results/exp83_neutron_oscillation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Constants
m_n = 939.56542052 # MeV (Neutron mass)
hbar = 6.582119569e-16 # eV*s
alpha_qed = 1.0/137.035999084

# Entropic Bias Delta
delta_modern = (5.0/9.0) * alpha_qed # ~ 0.00405

# Oscillation Parameters (Current Limits)
tau_limit = 1e8 # seconds (Super-Kamiokande / ILL bounds)
epsilon_limit = hbar / tau_limit # eV
epsilon_limit_MeV = epsilon_limit * 1e-6 # MeV

print(f"Neutron Mass: {m_n:.2f} MeV")
print(f"Modern Entropic Bias Delta: {delta_modern:.6e}")
print(f"Oscillation Matrix Element (Limit): {epsilon_limit_MeV:.6e} MeV")

def probability_transition(t, delta, epsilon):
    # P(n -> nbar) = (epsilon^2 / (epsilon^2 + delta_E^2)) * sin^2(sqrt(epsilon^2 + delta_E^2) * t)
    # delta_E here IS the potential difference relative to the mixing energy.
    # Hamiltonian H = [[E, eps], [eps, E + 2*V]]
    # 2*V = 2 * delta * m_n
    
    V_entropic = delta * m_n
    detuning = V_entropic # Half splitting? No, usually in 2-level system, detuning is E2-E1.
    # Splitting = 2 * V_entropic.
    # Effective mixing angle tan(2theta) = 2*epsilon / (E_nbar - E_n)
    # E_nbar - E_n = 2 * V_entropic.
    
    splitting = 2.0 * V_entropic
    
    # Amplitude squared (transition probability max)
    P_max = (epsilon**2) / (epsilon**2 + (splitting/2.0)**2) 
    
    # We assume t is large (time averaged -> 1/2 of max? or just max bound)
    return P_max

def experiment_83():
    # 1. Calculate the Entropic Potential Splitting
    V_splitting = 2.0 * delta_modern * m_n
    print(f"Entropic Splitting Energy (2*V): {V_splitting:.4f} MeV")
    
    # 2. Calculate Suppression Factor
    suppression = probability_transition(1.0, delta_modern, epsilon_limit_MeV)
    print(f"Suppression Factor (P_max): {suppression:.6e}")
    
    # 3. Sweep of Entropic Bias (What if delta goes to zero?)
    # Simulate a hypothetical "Screening Experiment" where we cancel the entropic bias.
    
    deltas = np.logspace(-15, -2, 1000) # From 1e-15 to 1e-2
    splittings = 2.0 * deltas * m_n
    probs = (epsilon_limit_MeV**2) / (epsilon_limit_MeV**2 + (splittings/2.0)**2)
    
    plt.figure(figsize=(10, 6))
    plt.loglog(deltas, probs, label=r'Transition Probability $P(n \to \bar{n})$', color='navy', linewidth=2)
    
    # Mark the UKFT 5/9 Point
    pt_ukft = probability_transition(1.0, delta_modern, epsilon_limit_MeV)
    plt.scatter([delta_modern], [pt_ukft], color='red', s=100, zorder=5, label='UKFT Modern Vacuum\n($\delta = 5/9 \\alpha$)')
    
    # Mark the Unsuppressed Point (Free Oscillation Limit)
    # If delta < epsilon_limit/m_n
    threshold_delta = epsilon_limit_MeV / m_n
    plt.axvline(threshold_delta, linestyle='--', color='gray', alpha=0.5, label='Quasi-Free Oscillation Threshold')
    
    plt.title("Constraint on Neutron-Antineutron Oscillation by Entropic Gravity")
    plt.xlabel(r"Entropic Bias $\delta$ (Vacuum Asymmetry)")
    plt.ylabel(r"Max Oscillation Probability $P_{n \to \bar{n}}$")
    
    plt.text(1e-4, 1e-50, "Neutrons are Entropically Stable!\n(Suppression ~ $10^{-60}$)", fontsize=12, color='darkgreen', ha='left')
    
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/oscillation_suppression.png")
    print(f"Plot saved to {OUTPUT_DIR}/oscillation_suppression.png")
    
    # 4. Energy Scale Comparison Plot
    plt.figure(figsize=(8, 6))
    energies = [epsilon_limit_MeV*1e6, V_splitting*1e6] # to eV
    labels = ['Mixing Term ($\epsilon$)\n(GUT Scale Effect)', 'Entropic Splitting ($2\delta m$)\n(Vacuum Bias)']
    
    bars = plt.bar(labels, energies, color=['gray', 'crimson'], log=True)
    plt.ylabel("Energy Scale (eV)")
    plt.title("Why Neutrons Don't Oscillate")
    
    # Annotate values
    plt.text(0, energies[0]*1.5, f"{energies[0]:.2e} eV", ha='center')
    plt.text(1, energies[1]*1.5, f"{energies[1]:.2e} eV\n(~7.6 MeV)", ha='center')
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/energy_scales.png")
    print(f"Plot saved to {OUTPUT_DIR}/energy_scales.png")

if __name__ == "__main__":
    experiment_83()
