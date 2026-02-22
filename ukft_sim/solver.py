import numpy as np
import scipy.linalg
from .physics import get_quantum_potential, get_velocity_field, step_discrete_action_minimizer

from tqdm import tqdm

class SimulationRunner:
    def __init__(self, N=201, L_phys=50.0, t_hop=1.0, dt_base=0.05, 
                 T_ticks=400, M_particles=1000, alpha_entropic=5.0, force_type='standard',
                 solver_method='global'):
        self.N = N
        self.L_phys = L_phys
        self.t_hop = t_hop
        self.dt_base = dt_base
        self.T_ticks = T_ticks
        self.M_particles = M_particles
        self.alpha_entropic = alpha_entropic
        self.force_type = force_type
        self.solver_method = solver_method
        
        self.x_grid = np.linspace(-L_phys/2, L_phys/2, N)
        self.dx = L_phys / N
        self.choice_indices = np.arange(T_ticks)
        
    def run(self, psi0, potential_barrier=None):
        """
        potential_barrier: Optional array of size N adding scalar potential V(x) to Hamiltonian
        """
        # Hamiltonian Setup
        diag = 2.0 * self.t_hop * np.ones(self.N)
        # Add external potential if provided
        if potential_barrier is not None:
             diag += potential_barrier
             
        off_diag = -self.t_hop * np.ones(self.N-1)
        H = np.diag(diag) + np.diag(off_diag, 1) + np.diag(off_diag, -1)
        # Periodic Boundary Conditions
        H[0, -1] = H[-1, 0] = -self.t_hop
        
        # Initial State
        psi = psi0.copy()
        
        # Initial Particles
        p_init = np.abs(psi)**2
        p_init /= p_init.sum()
        positions = np.random.choice(np.arange(self.N), size=self.M_particles, p=p_init)

        # History containers
        history_rho = []
        history_Vq = []
        history_pos = []
        history_time = []
        physical_time_elapsed = 0.0
        
        print("Starting Simulation Loop...")
        for t_idx in tqdm(range(self.T_ticks), desc="Simulating Choice Steps"):
            # 1. Dynamic dt (Time Dilation)
            rho = np.abs(psi)**2
            
            # UKFT Paper 34: dt ~ hbar / (|psi|^2 * E)
            # Local dt per particle - "Proper Time" per choice step
            rho_particles = rho[positions] + 1e-9
            dt_local = self.dt_base * (0.1 / rho_particles)
            dt_local = np.clip(dt_local, 0.01, 0.25)
            
            # Global dt for Field Evolution (Average Experience of the Collective)
            dt_n = np.mean(dt_local)
            
            physical_time_elapsed += dt_n
            history_time.append(physical_time_elapsed)
            
            # 2. Record
            history_rho.append(rho)
            history_pos.append(positions.copy())
            
            # 3. Evolve (Schrodinger)
            # Recompute propagator for dynamic dt
            # Optimization: for static H, we could diagonalize once, but expm is robust for small N
            if self.solver_method == 'local':
                 psi = self._evolve_trotter(psi, dt_n, potential_barrier)
            else:
                 U_dynamic = scipy.linalg.expm(-1j * H * dt_n)
                 psi = U_dynamic.dot(psi)
            
            # 4. Move (Guidance)
            V_q = get_quantum_potential(psi, self.t_hop)
            v_field = get_velocity_field(psi, self.t_hop)
            
            # Pass local dt for each particle's action calculation
            positions, _ = step_discrete_action_minimizer(
                positions, psi, v_field, V_q, dt_local, 
                self.alpha_entropic, self.t_hop, self.N, dx=self.dx,
                force_type=self.force_type
            )
            
        return {
            'x_grid': self.x_grid,
            'choice_indices': self.choice_indices,
            'history_rho': np.array(history_rho),
            'history_pos': np.array(history_pos),
            'history_time': np.array(history_time)
        }

    def _evolve_trotter(self, psi, dt, potential_barrier=None):
        """
        Evolve state psi by dt using Trotter-Suzuki decomposition.
        H = H_kinetic + H_potential
        H_kinetic = H_even + H_odd
        Uses Strang splitting: e^{-iV dt/2} e^{-iT dt} e^{-iV dt/2}
        where e^{-iT dt} ~ e^{-iH_odd dt} e^{-iH_even dt}
        """
        N = self.N
        
        # 1. Potential Half-Step (Diagonal)
        # H_diag = 2t + V_barrier
        # Note: The prototype ignored the 2t diagonal shift in the rotation, 
        # so we must include it here or in the bond rotation.
        # Let's include it in the diagonal phase to keep bond rotation simple.
        
        V_eff = np.zeros(N)
        if potential_barrier is not None:
             V_eff += potential_barrier
        
        # Add the 2t diagonal term from the Kinetic operator here
        V_eff += 2.0 * self.t_hop 
        
        # Apply e^{-i V_eff dt / 2}
        phase_v = np.exp(-1j * V_eff * dt / 2)
        psi = phase_v * psi
        
        # 2. Kinetic Step (Trotter)
        # U_bond = exp(-i * dt * [[0, -t], [-t, 0]])
        theta = self.t_hop * dt
        c = np.cos(theta)
        s = np.sin(theta)
        
        # Optimize by defining the operation locally without full matrix mult
        # U dot [a, b] = [c*a + i*s*b, i*s*a + c*b]
        
        # Apply Even Bonds: (0,1), (2,3)...
        # Vectorized approach for even pairs
        # Indices: 0, 2, 4, ...
        # For N=4: (0,1), (2,3). end_even=4. psi[0:4:2] -> 0,2. psi[1:4:2] -> 1,3.
        # For N=5: (0,1), (2,3). end_even=4. psi[0:4:2] -> 0,2. psi[1:4:2] -> 1,3. (4 is skipped)
        
        end_even = N if N % 2 == 0 else N - 1
        
        if end_even > 0:
            # Extract slices (creates views, copy to be safe for calculation)
            psi_even_0 = psi[0:end_even:2].copy()
            psi_even_1 = psi[1:end_even:2].copy()
            
            # Use temp variables to avoid overwriting during calculation
            new_0 = c * psi_even_0 + 1j * s * psi_even_1
            new_1 = 1j * s * psi_even_0 + c * psi_even_1
            
            psi[0:end_even:2] = new_0
            psi[1:end_even:2] = new_1
            
        # Handle Periodic Boundary for Even step if N is even: (N-1, 0)
        # Wait, if N is even, the loop (0,1)...(N-2, N-1) covers everything.
        # The boundary term (N-1, 0) is usually treated as an ODD bond in a ring?
        # N=4: Bonds (0,1), (1,2), (2,3), (3,0).
        # Even set: (0,1), (2,3).
        # Odd set: (1,2), (3,0).
        # So (N-1, 0) is an ODD bond if N is even.
        
        # Apply Odd Bonds: (1,2), (3,4)...
        # For N=4: (1,2), (3,0).
        # Step 1: Handle interior odd bonds (1,2)...
        # Slice 1, 3, ... (Left side of bond)
        # Slice 2, 4, ... (Right side of bond)
        
        # End index for Left side: 
        # If N=4: Need 1 (pair 1,2). 3 is pair (3,0).
        # Regular loop i=1, 3...
        # Pairs (i, i+1).
        # If N=4: (1,2). i=1. i+1=2.
        # If N=5: (1,2), (3,4). i=1,3. i+1=2,4.
        
        end_odd = N - 1 # Use N-1 to ensure i+1 < N
        
        if end_odd > 1:
            psi_odd_L = psi[1:end_odd:2].copy()
            psi_odd_R = psi[2:end_odd+1:2].copy() # 2, 4... up to N
            
            # Check lengths
            L_len = len(psi_odd_L)
            R_len = len(psi_odd_R)
            
            min_len = min(L_len, R_len)
            psi_odd_L = psi_odd_L[:min_len]
            psi_odd_R = psi_odd_R[:min_len]
            
            new_L = c * psi_odd_L + 1j * s * psi_odd_R
            new_R = 1j * s * psi_odd_L + c * psi_odd_R
            
            # Re-assign
            # Construct slices again or use indices?
            # Basic slice logic: 1::2, 2::2
            # psi[1:end_odd:2] might be slightly different than psi[1:1+2*min_len:2]
            
            psi[1:1+2*min_len:2] = new_L
            psi[2:2+2*min_len:2] = new_R

        # Handle Periodic Boundary (N-1, 0)
        # This is strictly an ODD bond in the standard 1D chain labeling if we start with (0,1) as even.
        # Bond (N-1, 0) links last and first.
        # This should be applied in the ODD step.
        
        bond_boundary = False
        if self.N > 0: # Always true
            # Boundary bond
            val_N_1 = psi[N-1]
            val_0 = psi[0]
            
            new_N_1 = c * val_N_1 + 1j * s * val_0
            new_0 = 1j * s * val_N_1 + c * val_0
            
            psi[N-1] = new_N_1
            psi[0] = new_0
            
        # 3. Potential Half-Step (Diagonal)
        psi = phase_v * psi
        
        return psi
