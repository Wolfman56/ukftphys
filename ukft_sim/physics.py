import numpy as np

def get_quantum_potential(psi, t_hop):
    """
    Computes V_quantum = - (hbar^2 / 2m) * (nabla^2 R / R).
    On lattice with t_hop, Kinetic ~ -t_hop * Delta_discrete.
    Effective V_Q ~ - t_hop * (R[i+1] + R[i-1] - 2R[i]) / R[i]
    """
    R = np.abs(psi) + 1e-12
    # Discrete Laplacian of R
    lap_R = np.roll(R, -1) + np.roll(R, 1) - 2*R
    # In tight-binding, the kinetic operator is correlate to t_hop * Laplacian
    # V_Q matches the "energy cost" of curvature.
    # Sign: High curvature (peak) -> Negative Laplacian -> Positive V_Q?
    # Standard QM: V_Q = - (1/2m) (R''/R). Peak has R'' < 0 -> V_Q > 0 (Repulsive).
    # Lattice H term is -t_hop.
    V_q = - t_hop * (lap_R / R) 
    return V_q

def get_velocity_field(psi, t_hop):
    """
    Bohmian Velocity v = J / rho.
    J[i] ~ 2 * t_hop * Im(psi[i]* psi[i+1]) (bond current)
    """
    # Current from i to i+1
    # J_{i->i+1} = 2 * t_hop * Im( conj(psi[i]) * psi[i+1] )
    # We assign v[i] as average of bond currents or just local current
    psi_conj = np.conj(psi)
    # Bond current i -> i+1
    J_bond = 2 * t_hop * np.imag(psi_conj * np.roll(psi, -1))
    rho = np.abs(psi)**2 + 1e-12
    # Velocity roughly J / rho. (Note: units of lattice sites / time)
    v = J_bond / rho
    return v

def get_analytic_density_and_gradient(target_pos, sources, sigma):
    """
    Computes exact Rho and Grad_Rho for a set of Gaussian sources.
    
    Args:
        target_pos (np.array): Position [x,y,z] to evaluate at.
        sources (list): List of tuples (pos_vector, mass).
        sigma (float): Width of Gaussian sources.
        
    Returns:
        (rho, grad_rho): Scalar density and Vector gradient.
        
    Math:
        Rho = Sum( m * exp(-r^2/2s^2) )
        Grad = Sum( m/s^2 * exp(...) * (pos_src - pos_target) )
    """
    rho = 0.0
    grad_rho = np.zeros_like(target_pos)
    
    for src_pos, m_src in sources:
        delta = src_pos - target_pos # Direction towards source
        dist2 = np.sum(delta**2)
        
        # Density contribution
        factor = m_src * np.exp(-dist2 / (2 * sigma**2))
        rho += factor
        
        # Gradient contribution (chain rule)
        # d/dx ( exp(-(x-x0)^2 / 2s^2) ) = exp(...) * (-1/2s^2) * 2(x-x0) * (-1)? 
        # Wait: d/dr (e^-r^2) = -2r e^-r^2. 
        # Here r = target - src.
        # d/d_target (...) = factor * (-(target-src) / s^2) = factor * (src-target) / s^2
        if sigma > 0:
            grad_rho += factor * (delta / sigma**2)
            
    return rho, grad_rho

def step_discrete_action_minimizer(pos_indices, psi, v_field, V_q, current_dt, alpha_entropic, t_hop, N, dx=1.0, force_type='standard'):
    """
    Selects next position to minimize Discrete Local Action.
    Action = Kinetic_mismatch + Potential_Cost
    
    force_type: 'standard' (Gradient of Rho) or 'bianconi' (Gradient of Log Rho)
    """
    probs = np.abs(psi)**2
    
    # Grid of potentials
    # UKFT: "Gravity" is attraction to high density (Entropic Potential)
    # Potential = V_quantum + V_entropic
    
    if force_type == 'bianconi':
        # Rel Entropy ~ log(rho)
        # Force ~ grad(log rho)
        # Potential ~ - log(rho)
        V_entropic = - alpha_entropic * np.log(probs + 1e-12)
    else: # standard
        # Standard ~ rho
        # Force ~ grad(rho)
        # V_entropic ~ - rho
        V_entropic = - alpha_entropic * probs
    
    V_total = V_q + V_entropic
    
    # 1. Kinetic Cost for candidate moves
    # v_field is "ideal velocity" at current index
    v_ideal = v_field[pos_indices] # Shape (M,)
    
    # Candidates moves: -1, 0, +1
    # Effective velocities: -1/dt, 0, 1/dt
    # Cost = 0.5 * mass * (v_actual - v_ideal)^2
    # Mass ~ 1/ (2 * t_hop * dx^2). Let's set mass scale = 1 for relative comparison
    
    u_L = -1.0 
    u_S = 0.0
    u_R = 1.0
    # Note: velocities are per-step (dx/dt is implicit in comparison if consistent)
    # If v_ideal is in "sites per step":
    # v_field calculation needs to be scrutinized. 
    # J_bond is "probability per time". v = J/rho is "sites per time".
    # So v_ideal * dt is "sites per step".
    
    target_displacement = v_ideal * current_dt
    
    # Kinetic Action ~ (displacement - target)^2
    K_L = (u_L - target_displacement)**2
    K_S = (u_S - target_displacement)**2
    K_R = (u_R - target_displacement)**2
    
    # 2. Potential Cost
    # Evaluated at target indices (periodic)
    idx_L = (pos_indices - 1) % N
    idx_S = pos_indices
    idx_R = (pos_indices + 1) % N
    
    P_L = V_total[idx_L]
    P_S = V_total[idx_S]
    P_R = V_total[idx_R]
    
    # Total Action
    # Weighting: Kinetic is usually dominant at small dt.
    # A_local = K + dt * V
    weight = current_dt
    S_L = K_L + weight * P_L
    S_S = K_S + weight * P_S
    S_R = K_R + weight * P_R
    
    # 3. Deterministic Minimization (with tie-breaking noise if needed, but strict here)
    # Stack: (3, M)
    S_stack = np.vstack([S_L, S_S, S_R])
    choices = np.argmin(S_stack, axis=0) # 0->L, 1->S, 2->R
    
    # Map back to steps -1, 0, 1
    steps = choices - 1 
    
    return (pos_indices + steps) % N, S_stack
