import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.sparse import diags, eye
from scipy.sparse.linalg import splu

# Create results directory
os.makedirs("results", exist_ok=True)

def simulate_barrier_nc(mirror_mass, Nc=1, dx=0.05, dt=0.02, L=100.0, T_max=4000):
    """
    Simulate scattering of a 'Color Multiplet' from a Mirror Barrier.
    
    Nc: Number of colors (components). 
        The barrier couples to EACH component with strength 'mirror_mass'.
        Hypothesis: The effective barrier seen by the COLOR SINGLET state is Nc * mirror_mass.
        Or conversely, the critical mass required per component scales as 1/Nc.
    """
    x = np.arange(0, L, dx)
    N = len(x)
    
    # Potential Setup
    x_mirror = 80.0
    width = 2.0
    
    # Mirror Barrier (Total Effective Potential)
    # If the particle is comprised of Nc constituents, the potential energy is Sum(V_i).
    # Since V_i = mirror_mass, V_total = Nc * mirror_mass.
    # This assumes tight binding (constituents are spatially coincident).
    
    # Correction Factor from Exp 44 (Gaussian Area Normalization)
    correction_factor = 1.59576
    
    # Total potential seen by the bound state
    V_eff = Nc * correction_factor * mirror_mass * 50.0 * np.exp(-(x - x_mirror)**2 / (2 * (width/4)**2))
    
    # Horizon Absorption (also scales with number of particles being absorbed?)
    # Generally, imaginary potential scales with N.
    V_imag_eff = Nc * (-5.0) * (1.0 - np.exp(-(x - (x_mirror + width))))
    mask_horizon = (x > x_mirror + width)
    V_imag = np.zeros_like(x)
    V_imag[mask_horizon] = V_imag_eff[mask_horizon]

    # Initial Wavepacket (Center of Mass)
    k0 = 2.0 
    sigma = 5.0
    x0 = 30.0
    psi = np.exp(-(x-x0)**2 / (2*sigma**2)) * np.exp(1j * k0 * x)
    norm = np.sqrt(np.sum(np.abs(psi)**2 * dx))
    psi = psi / norm
    
    # Hamiltonian Matrices for Crank-Nicolson
    # H = -1/2M_tot d^2/dx^2 + V_eff
    # Reduced mass of N identical particles -> CoM Mass = N * m0.
    # So kinetic term is 1/N.
    # H = (-1/(2*Nc)) * d^2/dx^2 + V_eff
    
    # Kinetic part coefficents
    off_diag_elem = -1.0 / (2.0 * Nc * dx**2)
    main_diag_elem = 1.0 / (Nc * dx**2)
    
    # Full H diagonal elements
    H_diag = main_diag_elem + V_eff + 1j * V_imag
    H_off  = off_diag_elem * np.ones(N-1)
    
    H = diags([H_off, H_diag, H_off], [-1, 0, 1])
    
    # Evolution Operators
    Identity = eye(N, format='csc')
    A = Identity + 1j * (dt / 2.0) * H
    B = Identity - 1j * (dt / 2.0) * H
    
    solve_A = splu(A)
    
    # Time Evolution
    current_psi = psi
    
    for t in range(T_max):
        current_psi = solve_A.solve(B @ current_psi)
        
    final_prob = np.sum(np.abs(current_psi)**2 * dx)
    return final_prob

def run_experiment_45():
    print("Running Experiment 45: Color Factor Scaling Verification")
    print("-------------------------------------------------------")
    
    # Scan Range for Nc=1 (Baseline)
    masses_1 = np.linspace(0.02, 0.20, 50) 
    print(f"Scanning Nc=1 Baseline...")
    results_1 = [simulate_barrier_nc(m, Nc=1) for m in masses_1]
    
    # Scan Range for Nc=3 (Color Triplet)
    # If scaling holds, critical mass should be ~ 1/3 of Baseline.
    masses_3 = np.linspace(0.005, 0.08, 50) 
    print(f"Scanning Nc=3 Hypothesis...")
    results_3 = [simulate_barrier_nc(m, Nc=3) for m in masses_3]

    # Analysis
    from scipy.interpolate import interp1d
    f1 = interp1d(masses_1, results_1, kind='cubic')
    f3 = interp1d(masses_3, results_3, kind='cubic')
    
    m1_fine = np.linspace(masses_1[0], masses_1[-1], 1000)
    m3_fine = np.linspace(masses_3[0], masses_3[-1], 1000)
    
    # Critical Mass (99% Unitarity)
    crit_1 = m1_fine[np.where(f1(m1_fine) >= 0.99)[0][0]]
    crit_3 = m3_fine[np.where(f3(m3_fine) >= 0.99)[0][0]]
    
    ratio = crit_1 / crit_3
    
    print("\nRESULTS:")
    print(f"Critical Mass (Nc=1): {crit_1:.5f}")
    print(f"Critical Mass (Nc=3): {crit_3:.5f}")
    print(f"Scaling Ratio (Expected ~3.0): {ratio:.4f}")
    
    # Physics Interpretation
    SCALE_TEV = 1.23
    mass_nc1_gev = crit_1 * SCALE_TEV * 1000
    mass_nc3_gev = crit_3 * 3.0 * SCALE_TEV * 1000 # If we define Mass = 3 * m_constituent
    
    print(f"-------------------------------------------------------")
    print(f"Theory Implication:")
    print(f"If Mirror Fermion is a singlet (Lepton): Mass ~ {mass_nc1_gev:.1f} GeV")
    print(f"If Mirror Fermion is a triplet (Quark):  Mass ~ {mass_nc3_gev:.1f} GeV")
    print(f"-------------------------------------------------------")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(m1_fine, f1(m1_fine), 'b-', label='Nc=1 (Singlet)')
    plt.plot(m3_fine, f3(m3_fine), 'r-', label='Nc=3 (Triplet)')
    
    plt.axvline(x=crit_1, color='b', linestyle='--', alpha=0.5)
    plt.axvline(x=crit_3, color='r', linestyle='--', alpha=0.5)
    plt.axhline(y=0.99, color='k', linestyle=':', label='Unitarity Thesis')
    
    plt.title(f"Experiment 45: Color Factor Scaling Verification\nRatio M(Nc=1)/M(Nc=3) = {ratio:.2f}")
    plt.xlabel("Constituent Coupling Parameter")
    plt.ylabel("Reflected Probability")
    plt.legend()
    plt.grid(True)
    
    plt.savefig("results/exp45_color_scaling.png")
    print("Plot saved.")

if __name__ == "__main__":
    run_experiment_45()
