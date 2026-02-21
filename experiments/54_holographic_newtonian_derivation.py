
import numpy as np
import matplotlib.pyplot as plt

def holographic_derivation():
    print("Deriving Entropic Gravity from Holographic Principles...")
    
    # Constants
    c = 1.0
    hbar = 1.0
    k_B = 1.0
    G_newton = 1.0
    
    # 1. Geometry (Spherical Screen)
    radii = np.linspace(1.0, 100.0, 50)
    
    # 2. Holographic Bit Count (N)
    # The number of bits on the screen must scale as Area (A)
    # N = Area / (Planck Length)^2 ~ A / G
    # Area = 4 * pi * r^2
    Bits_N = (4 * np.pi * radii**2) / G_newton
    
    # 3. Energy Source (Central Mass M)
    M_central = 1000.0
    E_total = M_central * c**2
    
    # 4. Emergent Temperature (T)
    # By Equipartition Theorem: E = 1/2 * N * k_B * T
    # Therefore, T = 2 * E / (N * k_B)
    Temperature_T = (2 * E_total) / (Bits_N * k_B)
    
    # 5. Entropic Force (F) on a test mass m
    # Verlinde: F delta_x = T delta_S
    # delta_S for a displacement of one Compton wavelength is roughly 2*pi*k_B
    # delta_S/delta_x ~ 2*pi*k_B * (m*c/hbar)
    # So F = T * (2*pi*k_B * m * c / hbar)
    
    m_test = 1.0
    gradient_S = (2 * np.pi * k_B * m_test * c) / hbar
    Force_F = Temperature_T * gradient_S
    
    # 6. Analyze Scaling
    print(f"{'Radius':<10} {'Bits (N)':<15} {'Temp (T)':<15} {'Force (F)':<15}")
    print("-" * 55)
    for i in range(0, 50, 10):
        r = radii[i]
        f = Force_F[i]
        # Check if F * r^2 is constant
        const_check = f * r**2
        print(f"{r:<10.1f} {Bits_N[i]:<15.1e} {Temperature_T[i]:<15.1e} {f:<15.4f} (F*r^2={const_check:.2f})")
        
    # Plot
    plt.figure(figsize=(10,6))
    plt.subplot(2,1,1)
    plt.loglog(radii, Force_F, 'bo-', label='Derived Entropic Force')
    plt.loglog(radii, 1000/radii**2, 'r--', label='Newtonian reference 1/r^2')
    plt.xlabel('Radius r')
    plt.ylabel('Force F')
    plt.title('Holographic Derivation of Newton\'s Law')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2,1,2)
    plt.plot(radii, Force_F * radii**2, 'g-')
    plt.xlabel('Radius r')
    plt.ylabel('F * r^2 (Should be Constant)')
    plt.title('Verification of Inverse Square Law')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('holographic_scaling.png')
    print("\nSaved plot to holographic_scaling.png")
    
    # Conclusion
    slope, intercept = np.polyfit(np.log(radii), np.log(Force_F), 1)
    print(f"\nSlope of log-log plot (Force scaling): {slope:.4f}")
    if abs(slope + 2.0) < 0.1:
        print(">> SUCCESS: Derived 1/r^2 from Holographic Entropy (N ~ Area).")
    else:
        print(f">> FAILURE: Derived r^{slope:.2f}, not 1/r^2.")

if __name__ == "__main__":
    holographic_derivation()
