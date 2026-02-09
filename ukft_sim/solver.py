import numpy as np
import scipy.linalg
from .physics import get_quantum_potential, get_velocity_field, step_discrete_action_minimizer

from tqdm import tqdm

class SimulationRunner:
    def __init__(self, N=201, L_phys=50.0, t_hop=1.0, dt_base=0.05, 
                 T_ticks=400, M_particles=1000, alpha_entropic=5.0, force_type='standard'):
        self.N = N
        self.L_phys = L_phys
        self.t_hop = t_hop
        self.dt_base = dt_base
        self.T_ticks = T_ticks
        self.M_particles = M_particles
        self.alpha_entropic = alpha_entropic
        self.force_type = force_type
        
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
