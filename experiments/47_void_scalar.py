import numpy as np
import matplotlib.pyplot as plt
import os

# Create results directory
os.makedirs("results", exist_ok=True)

def scalar_field_pressure(size=20, epsilon=1.0, beta=10.0, steps=1000):
    """
    Simulate a scalar field subject to an "Existence" constraint:
    |phi|^2 >= epsilon (non-zero vacuum density must be maintained).
    
    This is based on the idea that the "Vacuum" is not empty; it's a fluctuating
    reservoir of information (Causal Graph).
    """
    
    # Initialize Field (Uniform Random +/- 1)
    phi = np.random.uniform(-1, 1, size=(size, size, size))
    
    # Dynamics: Metropolis-Hastings (Simple Monte Carlo)
    # Hamiltonian: H = Sum (grad phi)^2 + V(phi)
    # V(phi) = Lambda * (|phi|^2 - v^2)^2 (Higgs Potential?)
    # But here, we just enforce the Constraint via Rejection Sampling (or huge potential)
    
    # Let's say V(phi) = 0 for |phi| > epsilon, V(phi) = Infinity for |phi| < epsilon
    # This is a "Hard Sphere" condition for Vacuum Amplitude.
    
    pressure_accum = 0.0
    measure_count = 0
    
    # Main Loop
    for _ in range(steps):
        # Pick random site
        i, j, k = np.random.randint(0, size, 3)
        
        # Propose change
        dphi = np.random.normal(0, 0.1)
        phi_new_val = phi[i,j,k] + dphi
        
        # 1. Constraint Check (Vacuum Cannot Collapse)
        if abs(phi_new_val) < epsilon:
            # REJECT: Connectivity Violation
            # This rejection creates an effective "Pressure" outward
            # The system "wants" to relax to 0, but is forced to stay >= epsilon
            continue 
            
        # 2. Energy Check (Gradient Term)
        # Calculate local gradient energy change
        # H_local ~ Sum (phi_site - phi_neighbor)^2
        neighbors = []
        if i > 0: neighbors.append(phi[i-1,j,k])
        if i < size-1: neighbors.append(phi[i+1,j,k])
        if j > 0: neighbors.append(phi[i,j-1,k])
        if j < size-1: neighbors.append(phi[i,j+1,k])
        if k > 0: neighbors.append(phi[i,j,k-1])
        if k < size-1: neighbors.append(phi[i,j,k+1])
        
        E_old = sum([(phi[i,j,k] - n)**2 for n in neighbors])
        E_new = sum([(phi_new_val - n)**2 for n in neighbors])
        
        dE = E_new - E_old
        
        # Accept/Reject based on Boltzmann
        if dE < 0 or np.random.rand() < np.exp(-beta * dE):
            phi[i,j,k] = phi_new_val
            
            # Measure "Pressure" (Virial Theorem)
            # P ~ Kinetic Energy - Potential Gradient
            # In MC, Pressure is related to the acceptance rate or boundary force.
            # Let's define Pressure P = - dE/dV (Force per unit area)
            # Here, the constraint acts as a "Wall" at |phi|=epsilon.
            # The Pressure is the force exerted against this wall.
            # Every time we reject due to epsilon constraint, it's a collision with the wall.
            pass
        else:
            pass # Rejected due to energy
            
        # Proper Pressure Measurement:
        # P = <Sum (grad phi)^2> / Volume - Temperature?
        # Let's use the trace of the stress-energy tensor:
        # T_mn = dphi/dx_m * dphi/dx_n - 0.5 * delta_mn * (dphi)^2
        # Pressure P = 1/3 Trace(T)
        pass # To satisfy the virial theorem
        
    # Calculate Average Kinetic/Gradient Energy
    # Gradient Energy Density
    grad_sq = 0.0
    for i in range(size):
        for j in range(size):
            for k in range(size):
                # Simple finite difference
                dpx = (phi[(i+1)%size,j,k] - phi[i,j,k])**2
                dpy = (phi[i,(j+1)%size,k] - phi[i,j,k])**2
                dpz = (phi[i,j,(k+1)%size] - phi[i,j,k])**2
                grad_sq += (dpx + dpy + dpz)
                
    avg_grad_E = grad_sq / (size**3)
    
    # Pressure Estimate
    # For a scalar field, P = K - V_grad.
    # In equilibrium, <K> = T/2.
    # P ~ T/2 - <(grad phi)^2>/3
    # If constrained by epsilon, the "Wall" adds a positive pressure term?
    # P_wall ~ Frequency of hitting epsilon / Area
    
    # We'll return just the Gradient Energy Density as a proxy for "Vacuum Tension".
    # High Tension -> Negative Pressure (Binding).
    # Low Tension -> Positive Pressure (Expansion)?
    
    return avg_grad_E

def run_experiment_47():
    print("Running Experiment 47: The Void Scalar (Dark Energy)...")
    print("-----------------------------------------------------")
    
    # Sweep Epsilon (The "Vacuum Fullness" Parameter)
    # epsilon = 1.0 (High Density / Matter)
    # epsilon = 0.001 (Deep Void / Dark Energy)
    
    # Logarithmic sweep for better resolution of the transition
    epsilons = np.logspace(0, -3, 20)
    pressures = []
    
    print(f"Sweeping Vacuum Density (epsilon) on 10x10x10 Lattice (20 points)...")
    
    for eps in epsilons:
        print(f"  Simulating epsilon = {eps:.4f} ...")
        p = scalar_field_pressure(size=10, epsilon=eps, beta=10.0, steps=20000)
        pressures.append(p)
        print(f"    -> Average Gradient Tension: {p:.6f}")
        
    # Plot
    plt.figure(figsize=(10, 6))
    plt.semilogx(epsilons, pressures, 'bo-', linewidth=2, markersize=6, label='Vacuum Tension')
    
    # Add asymptote line
    floor_val = np.mean(pressures[-5:])
    plt.axhline(y=floor_val, color='r', linestyle='--', label=f'Vacuum Floor (~{floor_val:.4f})')
    
    plt.xlabel('Vacuum Consistenty Constraint (epsilon) [Log Scale]')
    plt.ylabel('Vacuum Tension (Energy Density)')
    plt.title('Experiment 47: Emergence of Dark Energy (Vacuum Floor)')
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()
    plt.gca().invert_xaxis() # High density on left, Low density (Void) on right
    
    output_path = "results/void_scalar_pressure.png"
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")
    
    # Interpretation
    print("\nInterpretation:")
    print("If Tension decreases as Epsilon decreases (Void), the vacuum relaxes.")
    print("Does it approach zero? Or a finite positive value (Dark Energy)?")
    print(f"Tension at Eps=1.0: {pressures[0]:.6f}")
    print(f"Tension at Eps=0.001: {pressures[-1]:.6f}")
    
    ratio = pressures[0] / pressures[-1]
    print(f"Dynamic Range Ratio: {ratio:.2f}")

if __name__ == "__main__":
    run_experiment_47()
