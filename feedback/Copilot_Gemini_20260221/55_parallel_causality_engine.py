
import numpy as np
import scipy.linalg
import time

def compare_evolution(N=100, dt=0.01):
    print(f"Testing Local vs Global Evolution for N={N} sites...")
    
    # 1. Hamiltonian
    t_hop = 1.0
    diag = 2.0 * t_hop * np.ones(N)
    off_diag = -t_hop * np.ones(N-1)
    H = np.diag(diag) + np.diag(off_diag, 1) + np.diag(off_diag, -1)
    H[0, -1] = H[-1, 0] = -t_hop
    
    psi0 = np.zeros(N, dtype=complex)
    psi0[N//2] = 1.0 # Delta function
    
    # 2. Global Evolution (Current Method)
    start_global = time.time()
    U_global = scipy.linalg.expm(-1j * H * dt)
    psi_global = U_global.dot(psi0)
    end_global = time.time()
    print(f"Global Expm Time: {(end_global - start_global)*1000:.2f} ms")
    
    # 3. Local Evolution (Trotter-Suzuki 1st Order)
    # H = H_even + H_odd
    # e^-iHdt ~ e^-iH_odd dt * e^-iH_even dt
    start_local = time.time()
    
    # Even Bonds: (0,1), (2,3), ...
    # Odd Bonds: (1,2), (3,4), ...
    # Each bond is a 2x2 matrix: [[2t, -t], [-t, 2t]] (ignoring diagonal shift for now)
    # Actually, kinetic term is T_ij = -t(|i><j| + h.c.)
    # The diagonal 2t comes from 2*I - T.
    
    # Local Operators (Unitary matrices for 2 sites)
    # U_bond = exp(-i * dt * [[0, -t], [-t, 0]]) (Just kinetic hopping)
    theta = t_hop * dt
    # exp(i theta sigma_x) = cos(theta) I + i sin(theta) sigma_x
    c = np.cos(theta)
    s = np.sin(theta)
    U_bond = np.array([[c, 1j*s], [1j*s, c]]) 
    
    psi_local = psi0.copy()
    
    # Apply Even Bonds
    for i in range(0, N-1, 2):
        pair = psi_local[i:i+2]
        psi_local[i:i+2] = U_bond.dot(pair)
    # Periodic (N-1, 0) if N even
    if N % 2 == 0:
        # Wrap around boundary
        pair = np.array([psi_local[N-1], psi_local[0]])
        res = U_bond.dot(pair)
        psi_local[N-1] = res[0]
        psi_local[0] = res[1]
        
    # Apply Odd Bonds
    for i in range(1, N-1, 2):
        pair = psi_local[i:i+2]
        psi_local[i:i+2] = U_bond.dot(pair)
        
    end_local = time.time()
    print(f"Local Trotter Time: {(end_local - start_local)*1000:.2f} ms")
    
    # 4. Compare Fidelity
    overlap = np.abs(np.vdot(psi_global, psi_local))**2
    print(f"Fidelity (Overlap): {overlap:.6f}")
    
    if overlap > 0.99:
        print(">> SUCCESS: Local Evolution matches Global (Parallelizable).")
    else:
        print(">> WARNING: Fidelity low. Needs higher order Trotter or smaller dt.")

if __name__ == "__main__":
    compare_evolution(N=200, dt=0.01)
