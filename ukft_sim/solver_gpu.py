
import torch
import numpy as np
from tqdm import tqdm

def get_quantum_potential_torch(psi, t_hop, device):
    """Computes V_quantum using PyTorch tensors."""
    R = torch.abs(psi) + 1e-12
    # Discrete Laplacian: roll(-1) + roll(1) - 2*R
    # dim=0 is the spatial dimension for 1D
    lap_R = torch.roll(R, -1, 0) + torch.roll(R, 1, 0) - 2*R
    V_q = - t_hop * (lap_R / R)
    return V_q

def get_velocity_field_torch(psi, t_hop, device):
    """Computes velocity field using PyTorch tensors."""
    psi_conj = torch.conj(psi)
    # J_bond = 2 * t * Im(psi* psi_next)
    J_bond = 2 * t_hop * torch.imag(psi_conj * torch.roll(psi, -1, 0))
    rho = torch.abs(psi)**2 + 1e-12
    v = J_bond / rho
    return v

def step_discrete_action_minimizer_torch(pos_indices, psi, v_field, V_q, current_dt, alpha_entropic, t_hop, N, dx=1.0, force_type='standard'):
    """GPU-accelerated Action Minimizer."""
    probs = torch.abs(psi)**2
    
    if force_type == 'bianconi':
        V_entropic = - alpha_entropic * torch.log(probs + 1e-12)
    else:
        V_entropic = - alpha_entropic * probs
        
    V_total = V_q + V_entropic
    
    # Kinetic Cost
    v_ideal = v_field[pos_indices] # Fancy indexing works in PyTorch
    
    target_displacement = v_ideal * current_dt
    
    # Cost = (u - target)^2
    # u = -1, 0, 1
    # We broadcast: target has shape (M,), u needs to compare
    
    u_vals = torch.tensor([-1.0, 0.0, 1.0], device=psi.device).view(3, 1)
    target_disp = target_displacement.view(1, -1)
    
    # Kinetic Matrix (3, M)
    K = (u_vals - target_disp)**2
    
    # Potential Cost
    # Indices for neighbors
    idx_L = (pos_indices - 1) % N
    idx_S = pos_indices
    idx_R = (pos_indices + 1) % N
    
    # Gather V_total at these indices
    # indices shape (M,)
    P_L = V_total[idx_L]
    P_S = V_total[idx_S]
    P_R = V_total[idx_R]
    
    P_stack = torch.stack([P_L, P_S, P_R]) # (3, M)
    
    # Total Action
    weight = current_dt.view(1, -1) # (1, M) for broadcasting against (3, M)
    S_stack = K + weight * P_stack
    
    # Minimization
    choices = torch.argmin(S_stack, dim=0) # (M,) values 0,1,2
    
    # Steps
    steps = choices - 1 # -1, 0, +1
    
    new_pos = (pos_indices + steps) % N
    return new_pos

class SimulationRunnerGPU:
    def __init__(self, N=201, L_phys=50.0, t_hop=1.0, dt_base=0.05, 
                 T_ticks=400, M_particles=1000, alpha_entropic=5.0, force_type='standard', device=None):
        self.N = N
        self.L_phys = L_phys
        self.t_hop = t_hop
        self.dt_base = dt_base
        self.T_ticks = T_ticks
        self.M_particles = M_particles
        self.alpha_entropic = alpha_entropic
        self.force_type = force_type
        
        if device is None:
            if torch.cuda.is_available():
                self.device = torch.device('cuda')
            elif torch.backends.mps.is_available():
                self.device = torch.device('mps')
            else:
                self.device = torch.device('cpu')
        else:
            self.device = torch.device(device)
            
        print(f"SimulationRunnerGPU initialized on {self.device}")
        
        self.x_grid = torch.linspace(-L_phys/2, L_phys/2, N, device=self.device)
        self.dx = L_phys / N
        self.choice_indices = np.arange(T_ticks)
        
    def run(self, psi0_np, potential_barrier=None):
        # Hamiltonian Construction (Static)
        diag = 2.0 * self.t_hop * torch.ones(self.N, device=self.device)
        if potential_barrier is not None:
             V_ext = torch.tensor(potential_barrier, dtype=torch.float32, device=self.device)
             diag += V_ext
             
        off_diag = -self.t_hop * torch.ones(self.N-1, device=self.device)
        
        # Build H sparse or dense? Check N.
        # For N=1000, dense is fine on GPU.
        H = torch.diag(diag) + torch.diag(off_diag, 1) + torch.diag(off_diag, -1)
        H[0, -1] = -self.t_hop
        H[-1, 0] = -self.t_hop
        
        # Initial State
        psi = torch.tensor(psi0_np, dtype=torch.complex64, device=self.device)
        
        # Particles
        p_init = torch.abs(psi)**2
        p_init /= p_init.sum()
        
        # Sampling on GPU or CPU?
        # torch.multinomial fits
        # num_samples=M, replacement=True
        positions = torch.multinomial(p_init, self.M_particles, replacement=True)

        history_rho = []
        history_pos = []
        history_time = []
        physical_time_elapsed = 0.0
        
        # Evolution Loop
        for t_idx in tqdm(range(self.T_ticks), desc=f"GPU Sim ({self.device})"):
            rho = torch.abs(psi)**2
            
            # dt logic
            rho_particles = rho[positions] + 1e-9
            dt_local = self.dt_base * (0.1 / rho_particles)
            dt_local = torch.clamp(dt_local, 0.01, 0.25)
            dt_n = torch.mean(dt_local)
            
            physical_time_elapsed += dt_n.item()
            history_time.append(physical_time_elapsed)
            
            # Record (move to CPU for history to save VRAM?)
            # Let's keep in VRAM if small, or move. 
            # Moving to CPU is safer for large T.
            history_rho.append(rho.cpu().numpy())
            history_pos.append(positions.cpu().numpy())
            
            # Time Evolution
            # Matrix Exp on GPU
            # U = exp(-i * H * dt)
            # Complex H: -i * H
            # torch.linalg.matrix_exp works for complex matrices? Yes.
            
            # Cast H to complex
            H_c = H.to(torch.complex64)
            exponent = -1j * H_c * dt_n
            
            # MPS backend doesn't support linalg_matrix_exp as of Torch 2.X
            if self.device.type == 'mps':
                U_dynamic = torch.linalg.matrix_exp(exponent.cpu()).to(self.device)
            else:
                U_dynamic = torch.linalg.matrix_exp(exponent)
            
            psi = torch.matmul(U_dynamic, psi)
            
            # Guidance
            V_q = get_quantum_potential_torch(psi, self.t_hop, self.device)
            v_field = get_velocity_field_torch(psi, self.t_hop, self.device)
            
            positions = step_discrete_action_minimizer_torch(
                positions, psi, v_field, V_q, dt_local,
                self.alpha_entropic, self.t_hop, self.N, dx=self.dx,
                force_type=self.force_type
            )
            
        return {
            'x_grid': self.x_grid.cpu().numpy(),
            'choice_indices': self.choice_indices,
            'history_rho': np.array(history_rho),
            'history_pos': np.array(history_pos),
            'history_time': np.array(history_time)
        }
