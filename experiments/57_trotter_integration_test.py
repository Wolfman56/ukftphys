import sys
import os
import numpy as np
import time

# Add ukftphys root to path to allow treating ukft_sim as package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ukft_sim.solver import SimulationRunner

def test_integration():
    print("Testing SimulationRunner with solver_method='local'...")
    N = 201 # Odd number to test boundary conditions
    
    # Try initializing with solver_method (will fail if not updated)
    try:
        runner_local = SimulationRunner(N=N, T_ticks=10, solver_method='local')
        runner_global = SimulationRunner(N=N, T_ticks=10, solver_method='global')
    except TypeError as e:
        print(f"FAILED to initialize with solver_method (Refactor likely incomplete): {e}")
        return

    psi0 = np.zeros(N, dtype=complex)
    psi0[N//2] = 1.0

    print("Running Global...")
    start_g = time.time()
    res_g = runner_global.run(psi0)
    time_g = time.time() - start_g
    print(f"Global Time: {time_g*1000:.2f} ms")

    print("Running Local...")
    start_l = time.time()
    res_l = runner_local.run(psi0)
    time_l = time.time() - start_l
    print(f"Local Time: {time_l*1000:.2f} ms")

    # Compare results (Final Density)
    rho_g = res_g['history_rho'][-1]
    rho_l = res_l['history_rho'][-1]

    # Check conservation
    print(f"Global Norm: {np.sum(rho_g):.6f}")
    print(f"Local Norm: {np.sum(rho_l):.6f}")

    # MSE
    mse = np.mean((rho_g - rho_l)**2)
    print(f"MSE: {mse:.2e}")

    # Bhattacharyya Coefficient (Overlap of densities)
    # BC = sum(sqrt(p*q))
    bc = np.sum(np.sqrt(rho_g * rho_l))
    print(f"Fidelity (BC): {bc:.6f}")

    if bc > 0.99 and mse < 1e-4:
        print("SUCCESS: Local solver matches Global solver.")
    else:
        print("WARNING: Divergence detected.")

if __name__ == "__main__":
    test_integration()
