import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

def main():
    print("Experiment 51: Theoretical Derivation of the Holographic Link")
    print("-------------------------------------------------------------")
    
    # Constants
    hbar = constants.hbar
    c = constants.c
    G = constants.G
    kB = constants.k
    
    # Monopole Parameters from Exp 46/48
    M_monopole_GeV = 30.0
    M_monopole_kg = M_monopole_GeV * 1e9 * constants.e / c**2
    
    # 1. Horizon Radius (Schwarzschild)
    # R_s = 2GM/c^2
    R_s = 2 * G * M_monopole_kg / c**2
    print(f"Schwarzschild Radius R_s: {R_s:.4e} m")
    
    # 2. Compton Wavelength / Physical Size
    # R_c = hbar / (Mc)
    R_c = hbar / (M_monopole_kg * c)
    print(f"Compton Wavelength R_c:   {R_c:.4e} m")
    
    # 3. Holographic Bound check
    # The Bekenstein Entropy S_BH = A / (4 L_p^2)
    L_p = np.sqrt(hbar * G / c**3)
    print(f"Planck Length L_p:        {L_p:.4e} m")
    
    Area_BH = 4 * np.pi * R_s**2
    S_BH = Area_BH / (4 * L_p**2)
    print(f"Black Hole Entropy S_BH:  {S_BH:.4e} nats")
    
    # 4. Monopole Entropy (Estimated)
    # If the Monopole is a 'saturated' object in terms of information packing
    # relative to the STRONG interaction (or Mirror Gravity).
    # Let's define an 'Effective' Gravity G_strong
    # Force ratio F_s / F_g ~ 10^38
    # alpha_s ~ 1, alpha_g ~ (M/M_pl)^2
    
    # Let's derive the "Strong Gravity" constant G_s
    # Scale: 1 fermi (1e-15 m) is the size.
    # Energy: 30 GeV.
    
    # If R_s_effective = R_c (The particle is its own Black Hole)
    # 2 G_eff M / c^2 = hbar / (M c)
    # -> G_eff = hbar c / (2 M^2)
    
    G_eff = hbar * c / (2 * M_monopole_kg**2)
    print(f"Effective Strong Gravity G_eff: {G_eff:.4e} m^3 kg^-1 s^-2")
    print(f"Ratio G_eff / G: {G_eff / G:.4e}")
    
    # 5. Lifetime Scaling
    # t_evap ~ G^2 M^3
    # t_decay ~ G_eff^2 M^3
    
    t_decay_theory = (5120 * np.pi * G_eff**2 * M_monopole_kg**3) / (hbar * c**4)
    print(f"Predicted Lifetime (using G_eff): {t_decay_theory:.4e} s")
    
    # Compare with Exp 48 Result
    print(f"Observed Lifetime (Exp 48):       5.60e-22 s")
    
    # 6. Plot the Hierarchy
    masses = np.logspace(-28, 30, 100) # kg (electron to sun)
    
    # Schwarzschild Radius
    rs = 2 * G * masses / c**2
    # Compton Wavelength
    rc = hbar / (masses * c)
    
    plt.figure(figsize=(10,6))
    plt.loglog(masses, rs, label='Schwarzschild Radius ($R_s \propto M$)', color='black')
    plt.loglog(masses, rc, label='Compton Wavelength ($R_c \propto 1/M$)', color='blue')
    
    # Intersection Point (Planck Mass)
    mpl_val = np.sqrt(hbar*c/G)
    plt.scatter([mpl_val], [np.sqrt(hbar*G/c**3)], color='red', s=100, label='Planck Mass')
    
    # Our Monopole
    plt.scatter([M_monopole_kg], [R_c], color='green', s=100, label='Entropic Monopole (30 GeV)', marker='*')
    
    # Strong Gravity Line?
    # Intersection at ~1 GeV (Proton mass / Monopole mass range)
    # The G_eff line would cross R_c at the Monopole mass.
    rs_eff = 2 * G_eff * masses / c**2
    plt.loglog(masses, rs_eff, '--', label='Effective Strong Gravity Horizon', color='green', alpha=0.5)
    
    plt.axvline(x=M_monopole_kg, color='gray', linestyle=':', alpha=0.5)
    
    plt.xlabel('Mass (kg)')
    plt.ylabel('Length Scale (m)')
    
    plt.text(1e-25, 1e-10, 'Quantum Region\n(Particle)', fontsize=12)
    plt.text(1e10, 1e-5, 'Classical Region\n(Black Hole)', fontsize=12)
    plt.text(M_monopole_kg*2, 1e-16, 'Strong Gravity\nRegime', color='green')
    
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.title('The Holographic hierarchy: Monopole as a "Strong" Black Hole')
    
    plt.savefig('experiments/51_holographic_hierarchy.png')
    print("Hierarchy plot saved to experiments/51_holographic_hierarchy.png")

if __name__ == "__main__":
    main()
