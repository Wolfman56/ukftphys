import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

def main():
    print("Experiment 49: Monopole & Black Hole Thermodynamics Analogue")
    print("------------------------------------------------------------")

    # Physical Constants
    c = constants.c          # Speed of light (m/s)
    h = constants.h          # Planck constant (J s)
    hbar = constants.hbar    # Reduced Planck constant (J s)
    G = constants.G          # Gravitational constant (m^3 kg^-1 s^-2)
    kB = constants.k         # Boltzmann constant (J/K)
    eV = constants.e         # Electron volt (J)
    GeV = 1e9 * eV           # Giga-electron volt (J)
    M_sun = 1.989e30         # Solar mass (kg)
    M_pl = np.sqrt(hbar * c / G) # Planck Mass (kg)

    print(f"Planck Mass: {M_pl:.4e} kg")

    # --- 1. The 30 GeV Black Hole ---
    # T_H = (hbar c^3) / (8 pi G M kB)
    # We find M for T_H = 30 GeV
    
    def hawking_temp_to_mass(T_GeV):
        E_thermal = T_GeV * GeV
        numerator = hbar * c**3
        denominator = 8 * np.pi * G * E_thermal
        return numerator / denominator

    target_temp_GeV = 30.0
    mass_30GeV_BH = hawking_temp_to_mass(target_temp_GeV)

    print(f"\nTarget Temperature: {target_temp_GeV} GeV")
    print(f"Corresponding Black Hole Mass: {mass_30GeV_BH:.4e} kg")
    print(f"In Planck Masses: {mass_30GeV_BH / M_pl:.4f} M_pl")
    print(f"In Grams: {mass_30GeV_BH * 1000:.4f} g")

    # --- 2. Evaporation Time ---
    # t_evap = (5120 * pi * G^2 * M^3) / (hbar * c^4)
    
    def evaporation_time(M_kg):
        return (5120 * np.pi * G**2 * M_kg**3) / (hbar * c**4)

    t_evap_30GeV = evaporation_time(mass_30GeV_BH)
    print(f"Evaporation Time for 30 GeV BH: {t_evap_30GeV:.4e} s")

    # Compare with Particle Lifetime (from Exp 48)
    # Gamma = 1.18 MeV -> tau = 5.6e-22 s
    tau_particle = 5.6e-22
    print(f"Particle Lifetime (Exp 48): {tau_particle:.4e} s")
    
    ratio = t_evap_30GeV / tau_particle
    print(f"Discrepancy Factor (Evap Time / Decay Time): {ratio:.2e}")

    # --- 3. Radiation Spectrum ---
    # Plot the Hawking Radiation Spectrum for T = 30 GeV
    
    def planck_spectrum(E_GeV, T_GeV):
        # Normalized Planck distribution I(E) ~ E^3 / (exp(E/T) - 1)
        # Avoid division by zero at E=0
        mask = E_GeV > 0
        spectrum = np.zeros_like(E_GeV)
        spectrum[mask] = (E_GeV[mask]**3) / (np.exp(E_GeV[mask] / T_GeV) - 1)
        return spectrum

    energies = np.linspace(0.1, 200, 500) # GeV
    spectrum = planck_spectrum(energies, 30.0)

    plt.figure(figsize=(10, 6))
    plt.plot(energies, spectrum, label=f'Hawking Radiation (T={target_temp_GeV} GeV)', color='purple')
    plt.axvline(x=target_temp_GeV, color='r', linestyle='--', label='Peak Temperature Scale', alpha=0.7)
    
    # Peak of x^3 / (e^x - 1) is at x approx 2.82
    # So peak energy should be roughly 2.82 * T
    peak_energy = 2.821 * target_temp_GeV
    plt.axvline(x=peak_energy, color='g', linestyle=':', label=f'Peak Emission (~{peak_energy:.1f} GeV)')

    plt.title('Theoretical Emission Spectrum for T_H = 30 GeV')
    plt.xlabel('Particle Energy (GeV)')
    plt.ylabel('Intensity (Arbitrary Units)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_plot = 'experiments/49_monopole_black_hole_spectrum.png'
    plt.savefig(output_plot)
    print(f"\nSpectrum plot saved to {output_plot}")

if __name__ == "__main__":
    main()
