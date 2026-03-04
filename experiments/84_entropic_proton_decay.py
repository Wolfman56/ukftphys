import numpy as np
import matplotlib.pyplot as plt
import os

# Create results directory if it doesn't exist
output_dir = "results/exp84_proton_decay"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Physical Constants (Natural Units: hbar = c = k_B = 1)
GeV = 1.0
MeV = 1e-3
keV = 1e-6
eV = 1e-9

# Entropic Bias Parameters (from Exp 82/83)
delta_modern = 4.05e-3  # 0.4% Entropic Bias
m_proton = 0.938 * GeV
V_barrier = 2 * delta_modern * m_proton  # ~7.6 MeV barrier to symmetric phase

# Temperature Range (Log Scale)
# From Big Bang (10^16 GeV) to CMB (10^-4 eV)
T_range = np.logspace(16, -13, 1000) * GeV

# 1. Thermal Activation Suppression (Boltzmann Factor)
# Probability of fluctuating into the Symmetric Phase where B-violation is allowed.
# P_sym ~ exp(-V_barrier / T)
P_symmetric_phase = np.exp(-V_barrier / T_range)

# 2. Effective Proton Lifetime
# Baseline GUT lifetime (if vacuum was symmetric): tau_0 ~ 10^34 years
tau_GUT = 1e34  # years
# Effective lifetime: tau_eff = tau_GUT / P_sym
tau_eff = tau_GUT / (P_symmetric_phase + 1e-100) # prevent div/0

# Convert T to relevant units for plotting
T_GeV = T_range / GeV

# Plot 1: The "Shutoff" of Proton Decay
plt.figure(figsize=(10, 6))
plt.loglog(T_GeV, tau_eff, label='Entropic Proton Lifetime', color='blue', linewidth=2)
plt.axhline(y=tau_GUT, color='red', linestyle='--', label='Standard GUT Lifetime ($10^{34}$ yrs)')
plt.axvline(x=V_barrier/GeV, color='green', linestyle=':', label='Entropic Barrier ($7.6$ MeV)')
plt.axvline(x=2.3e-13, color='cyan', linestyle=':', label='Current CMB ($2.7$ K)')

plt.xlabel('Temperature (GeV)')
plt.ylabel('Proton Lifetime (Years)')
plt.title('Exp 84: Entropic Suppression of Proton Decay')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.gca().invert_xaxis()  # Time flows left (High T) to right (Low T)

output_path_1 = os.path.join(output_dir, "proton_stability_evolution.png")
plt.savefig(output_path_1)
print(f"Plot saved to {output_path_1}")

# Plot 2: Suppression Factor at Key Epochs
epochs = {
    "GUT Scale": 1e16 * GeV,
    "Electroweak": 100 * GeV,
    "QCD Phase": 0.150 * GeV,
    "Nucleosynthesis": 1e-3 * GeV,
    "Recombination": 0.3 * eV,
    "Today (CMB)": 2.3e-4 * eV
}

print("\n--- Entropic Suppression Factors ---")
print(f"Barrier Height (V): {V_barrier/MeV:.4f} MeV")

suppressions = []
labels = []

for name, T in epochs.items():
    factor = np.exp(-V_barrier / T)
    suppressions.append(factor)
    labels.append(name)
    lifetime_boost = 1/factor if factor > 1e-100 else float('inf')
    print(f"{name:15s} (T={T:.1e} GeV): Suppression = {factor:.2e}, Boost = {lifetime_boost:.2e}")

# Save numeric results
with open(os.path.join(output_dir, "suppression_factors.txt"), "w") as f:
    f.write(f"Entropic Barrier: {V_barrier/MeV:.4f} MeV\n\n")
    for name, T in epochs.items():
        factor = np.exp(-V_barrier / T)
        f.write(f"{name:15s} (T={T:.1e} GeV): Suppression = {factor:.2e}\n")

