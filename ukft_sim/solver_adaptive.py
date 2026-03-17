"""
AdaptiveSolver — choice operator with proper ℓ = c·dt^(3/2) candidate scaling.

Contrast with existing SimulationRunner in solver.py:

    Old:  candidates = {idx-1, idx, idx+1}
          ℓ = dx (fixed grid spacing)
          ℓ/dt = dx/dt  → DIVERGES as dt → 0
          Cannot converge in dense-choice limit.

    New:  velocity candidates spaced at δv = c_scale·√dt
          ℓ = δv·dt = c_scale·dt^(3/2)
          ℓ/dt = c_scale·√dt → 0 as dt → 0
          Achieves O(√dt) velocity consistency (proven by Gap1 minimality bound).

Particles are tracked at CONTINUOUS float positions (not integer lattice indices).
Grid fields (ψ, v_B, V_Q) are evaluated via np.interp at continuous positions.

See experiments/04_convergence_equivariance.py for the numerical validation of
the convergence rate, and experiments/05_adaptive_solver_comparison.py for a
side-by-side comparison with the old solver on the double-slit setup.
"""

import numpy as np
import scipy.linalg
from .physics import get_quantum_potential, get_velocity_field


class AdaptiveSolver:
    """
    Choice-guided Bohmian solver with dense velocity candidates.

    Parameters
    ----------
    x_grid : ndarray, shape (N,)
        Spatial grid (uniform).
    dt_base : float
        Base timestep. ψ is evolved with this dt each step.
    c_scale : float
        Candidate scaling constant.  Velocity spacing = c_scale * √dt.
        Smaller c_scale → finer candidates → better accuracy (at higher cost).
    v_max : float
        Velocity candidate window: u ∈ [−v_max, +v_max].
        Should exceed max expected |v_B| by a safe margin.
    alpha_entropic : float
        Entropic gravity coupling (same meaning as SimulationRunner).
    t_hop : float
        Tight-binding hopping parameter (kinetic energy scale).
    M_particles : int
        Number of particles.
    """

    def __init__(self, x_grid: np.ndarray, dt_base: float = 0.05,
                 c_scale: float = 1.0, v_max: float = 8.0,
                 alpha_entropic: float = 0.0, t_hop: float = 1.0,
                 M_particles: int = 1000, seed: int = 42):
        self.x_grid = x_grid
        self.dx = x_grid[1] - x_grid[0]
        self.N = len(x_grid)
        self.dt_base = dt_base
        self.c_scale = c_scale
        self.v_max = v_max
        self.alpha_entropic = alpha_entropic
        self.t_hop = t_hop
        self.M_particles = M_particles
        self.rng = np.random.default_rng(seed)

    # ── Core step ─────────────────────────────────────────────────────────────

    def step(self, positions: np.ndarray, psi: np.ndarray, dt: float) -> np.ndarray:
        """
        Move particles using dense velocity candidates with ℓ = c_scale·dt^(3/2).

        Fully vectorised over particles and candidates; no Python-level loop.

        Parameters
        ----------
        positions : ndarray, shape (M,)  — continuous positions (floats)
        psi       : ndarray, shape (N,)  — current wavefunction on x_grid
        dt        : float

        Returns
        -------
        new_positions : ndarray, shape (M,)
        """
        # Grid fields
        v_B_field = get_velocity_field(psi, self.t_hop)        # (N,)
        V_q_field = get_quantum_potential(psi, self.t_hop)      # (N,)
        rho_field = np.abs(psi)**2                              # (N,)
        V_entr_field = -self.alpha_entropic * rho_field         # (N,)
        W_field = V_q_field + V_entr_field                      # (N,) total potential

        # Interpolate v_B at continuous particle positions
        v_B_at_pos = np.interp(positions, self.x_grid, v_B_field)  # (M,)

        # Dense velocity candidates: spacing c_scale·√dt  →  ℓ = c_scale·dt^{3/2}
        dv = self.c_scale * np.sqrt(dt)
        u_cands = np.arange(-self.v_max, self.v_max + dv * 0.5, dv)  # (K,)
        K = len(u_cands)

        # Broadcast for vectorised evaluation: shapes (M,1) and (1,K)
        x_M1  = positions[:, np.newaxis]            # (M, 1)
        u_1K  = u_cands[np.newaxis, :]              # (1, K)
        vB_M1 = v_B_at_pos[:, np.newaxis]           # (M, 1)

        # Candidate midpoints and W values — vectorised interpolation
        midpoints_flat = (x_M1 + u_1K * (dt / 2)).ravel()       # (M*K,)
        W_mid = np.interp(midpoints_flat, self.x_grid, W_field)
        W_mid = W_mid.reshape(len(positions), K)                 # (M, K)

        # Discrete local action: S(u) = dt/2·(u−v_B)² + W(q+u·dt/2)·dt
        actions = dt / 2 * (u_1K - vB_M1)**2 + W_mid * dt       # (M, K)

        best_idx = np.argmin(actions, axis=1)                    # (M,)
        best_u   = u_cands[best_idx]                             # (M,)

        new_pos = positions + best_u * dt
        # Reflective boundary: stay inside grid domain
        x_lo, x_hi = self.x_grid[1], self.x_grid[-2]
        new_pos = np.clip(new_pos, x_lo, x_hi)
        return new_pos

    # ── Full simulation run ────────────────────────────────────────────────────

    def run(self, psi0: np.ndarray, potential_barrier: np.ndarray = None,
            T_ticks: int = None) -> dict:
        """
        Full simulation run returning the same dict as SimulationRunner.run().

        Parameters
        ----------
        psi0              : initial wavefunction, shape (N,)
        potential_barrier : optional external potential V(x), shape (N,)
        T_ticks           : number of time steps (defaults to dt_base-scaled estimate)

        Returns
        -------
        dict with keys: x_grid, choice_indices, history_rho, history_pos, history_time
            history_pos contains nearest-grid-index integers for vis compatibility.
        """
        T = T_ticks if T_ticks is not None else max(1, int(5.0 / self.dt_base))

        # Build Hamiltonian (identical to SimulationRunner)
        diag = 2.0 * self.t_hop * np.ones(self.N)
        if potential_barrier is not None:
            diag = diag + potential_barrier
        off_diag = -self.t_hop * np.ones(self.N - 1)
        H = (np.diag(diag)
             + np.diag(off_diag, 1)
             + np.diag(off_diag, -1))
        H[0, -1] = H[-1, 0] = -self.t_hop

        psi = psi0.copy()

        # Initial particles: sample from |ψ₀|² at continuous positions
        rho0 = np.abs(psi0)**2
        rho0 /= rho0.sum()
        start_idx = self.rng.choice(self.N, size=self.M_particles, p=rho0)
        positions = self.x_grid[start_idx].copy()   # float array

        history_rho = []
        history_pos = []    # stored as nearest grid indices (int) for vis compat
        history_time = []
        t_elapsed = 0.0

        for _ in range(T):
            dt = self.dt_base
            history_rho.append(np.abs(psi)**2)

            # Convert continuous positions → nearest grid indices for vis
            idx = np.clip(np.searchsorted(self.x_grid, positions) - 1, 0, self.N - 1)
            history_pos.append(idx)
            history_time.append(t_elapsed)
            t_elapsed += dt

            # Evolve ψ (same as SimulationRunner — matrix exponential)
            U = scipy.linalg.expm(-1j * H * dt)
            psi = U.dot(psi)

            # Move particles with dense candidates
            positions = self.step(positions, psi, dt)

        return {
            'x_grid':        self.x_grid,
            'choice_indices': np.arange(T),
            'history_rho':   np.array(history_rho),
            'history_pos':   np.array(history_pos),
            'history_time':  np.array(history_time),
            # Extra: keep continuous positions for analysis
            '_final_positions_continuous': positions,
        }

    # ── Velocity error diagnostic ─────────────────────────────────────────────

    def velocity_error_at(self, psi: np.ndarray, dt: float,
                          n_sample: int = 200) -> tuple:
        """
        Sample n_sample particles from |ψ|², measure mean ||u_c - v_B||.
        Returns (mean_error, positions_sampled, u_c_values, v_B_values).
        Useful for comparing against old solver at the same dt.
        """
        rho = np.abs(psi)**2
        rho /= rho.sum()
        idx = self.rng.choice(self.N, size=n_sample, p=rho)
        sample_pos = self.x_grid[idx]

        v_B_field = get_velocity_field(psi, self.t_hop)
        v_B_true = np.interp(sample_pos, self.x_grid, v_B_field)

        new_pos = self.step(sample_pos, psi, dt)
        u_c = (new_pos - sample_pos) / dt

        mean_err = np.mean(np.abs(u_c - v_B_true))
        return mean_err, sample_pos, u_c, v_B_true
