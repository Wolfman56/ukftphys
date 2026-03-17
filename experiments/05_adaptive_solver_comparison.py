"""
Experiment 05: Old Solver vs AdaptiveSolver on Double Slit

Runs both solvers on the standard double-slit setup and compares:

  Panel A (top row): Sample trajectories — Old solver | Adaptive solver | Exact Bohmian
  Panel B (bottom row): Final particle density vs |ψ_T|² for each solver
  Panel C: Single-step velocity error across positions (t=0) for old vs adaptive
           at three different dt values, showing the O(√dt) scaling of adaptive.

Key architectural difference:
  Old solver  (solver.py):             3 fixed candidates {idx-1, idx, idx+1}
                                        ℓ = dx (fixed) → ℓ/dt diverges as dt→0
  AdaptiveSolver (solver_adaptive.py): velocity spacing c·√dt → ℓ = c·dt^{3/2}
                                        ℓ/dt = c·√dt → 0 as dt→0

Practical consequence demonstrated here:
  - Old solver at dt=0.05: trajectories "snap" to integer lattice steps,      producing quantization artefacts in the interference pattern
  - Adaptive solver at dt=0.05: smooth trajectories, better equivariance
  - Adaptive solver at dt=0.20: coarser time steps but comparable accuracy
    (4× larger dt → same O(√dt) error as old at 4× smaller dt)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.linalg
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.solver import SimulationRunner
from ukft_sim.solver_adaptive import AdaptiveSolver
from ukft_sim.physics import get_velocity_field, get_quantum_potential

from pathlib import Path
OUTDIR = Path(__file__).parent

# ── Shared double-slit setup ──────────────────────────────────────────────────

N       = 151
L_PHYS  = 50.0
T_TICKS = 180
M_PART  = 600

def build_double_slit_potential(x_grid, V_high=18.0, barrier_half_w=1.0,
                                 slit_half_w=1.2, slit_sep=4.0):
    """Identical barrier to Experiment 02."""
    V = np.zeros_like(x_grid)
    in_barrier = np.abs(x_grid) < barrier_half_w
    slit1 = np.abs(x_grid - (-slit_sep/2)) < slit_half_w
    slit2 = np.abs(x_grid - ( slit_sep/2)) < slit_half_w
    V[in_barrier & ~(slit1 | slit2)] = V_high
    return V

def build_psi0(x_grid):
    width = 3.0
    k0    = 2.0
    psi0 = np.exp(-(x_grid + L_PHYS/3)**2 / (2*width**2)) * np.exp(1j*k0*x_grid)
    psi0 /= np.linalg.norm(psi0)
    return psi0

def run_exact_bohmian(x_grid, psi0, potential_barrier, dt, T, M, t_hop=1.0, seed=7):
    """
    'Ground truth' solver: particles follow v_B field directly (no discretisation).
    Uses Euler integration with dt_sub = dt/10 for accuracy.
    ψ is evolved identically to both other solvers.
    """
    N = len(x_grid)
    diag = 2.0 * t_hop * np.ones(N) + potential_barrier
    off_d = -t_hop * np.ones(N - 1)
    H = np.diag(diag) + np.diag(off_d, 1) + np.diag(off_d, -1)
    H[0, -1] = H[-1, 0] = -t_hop

    psi = psi0.copy()
    rho0 = np.abs(psi0)**2; rho0 /= rho0.sum()
    rng = np.random.default_rng(seed)
    idx0 = rng.choice(N, size=M, p=rho0)
    pos = x_grid[idx0].copy()  # continuous positions

    history_pos = []
    history_rho = []

    n_sub = 10
    dt_sub = dt / n_sub

    for _ in range(T):
        history_rho.append(np.abs(psi)**2)
        idx_near = np.clip(np.searchsorted(x_grid, pos) - 1, 0, N-1)
        history_pos.append(idx_near)

        # Evolve ψ
        U = scipy.linalg.expm(-1j * H * dt)
        psi = U.dot(psi)

        # Euler sub-steps for particle positions
        for _ in range(n_sub):
            v_B = get_velocity_field(psi, t_hop)
            v_at_pos = np.interp(pos, x_grid, v_B)
            pos = pos + v_at_pos * dt_sub
            pos = np.clip(pos, x_grid[1], x_grid[-2])

    return np.array(history_rho), np.array(history_pos)


# ── Run all three solvers ─────────────────────────────────────────────────────

def run_all():
    x_grid   = np.linspace(-L_PHYS/2, L_PHYS/2, N)
    psi0     = build_psi0(x_grid)
    V_barrier = build_double_slit_potential(x_grid)

    print("Running Old Solver (SimulationRunner, dt=0.05)...")
    runner_old = SimulationRunner(
        N=N, L_phys=L_PHYS, dt_base=0.05, T_ticks=T_TICKS,
        M_particles=M_PART, alpha_entropic=0.0)
    res_old = runner_old.run(psi0.copy(), potential_barrier=V_barrier.copy())

    print("Running AdaptiveSolver (dt=0.05)...")
    adaptive_05 = AdaptiveSolver(
        x_grid, dt_base=0.05, c_scale=1.0, v_max=8.0,
        alpha_entropic=0.0, M_particles=M_PART, seed=42)
    res_adp05 = adaptive_05.run(psi0.copy(), potential_barrier=V_barrier.copy(),
                                T_ticks=T_TICKS)

    print("Running Exact Bohmian (Euler, dt=0.20, 10 sub-steps)...")
    rho_exact, pos_exact = run_exact_bohmian(
        x_grid, psi0.copy(), V_barrier.copy(), dt=0.20, T=T_TICKS,
        M=M_PART, seed=42)

    print("Running AdaptiveSolver (dt=0.20 — 4× larger step)...")
    adaptive_20 = AdaptiveSolver(
        x_grid, dt_base=0.20, c_scale=1.0, v_max=8.0,
        alpha_entropic=0.0, M_particles=M_PART, seed=42)
    res_adp20 = adaptive_20.run(psi0.copy(), potential_barrier=V_barrier.copy(),
                                T_ticks=T_TICKS)

    return x_grid, psi0, V_barrier, res_old, res_adp05, rho_exact, pos_exact, res_adp20


# ── Velocity error diagnostic ─────────────────────────────────────────────────

def velocity_error_old(x_grid, psi, dt, dx_fixed=None, n_sample=300, t_hop=1.0):
    """Velocity error for old 3-candidate solver at given dt."""
    if dx_fixed is None:
        dx_fixed = x_grid[1] - x_grid[0]
    rho = np.abs(psi)**2; rho /= rho.sum()
    rng = np.random.default_rng(0)
    idx = rng.choice(len(x_grid), size=n_sample, p=rho)
    pos = x_grid[idx]

    v_B_field = get_velocity_field(psi, t_hop)
    v_B_true  = np.interp(pos, x_grid, v_B_field)

    V_q_field = get_quantum_potential(psi, t_hop)
    W_field   = V_q_field  # no entropic term for this test

    errs = []
    for x, vB in zip(pos, v_B_true):
        u_cands = np.array([-dx_fixed/dt, 0.0, dx_fixed/dt])
        mids = x + u_cands * dt / 2
        W_mid = np.interp(mids, x_grid, W_field)
        acts  = dt/2 * (u_cands - vB)**2 + W_mid * dt
        u_best = u_cands[np.argmin(acts)]
        errs.append(abs(u_best - vB))
    return pos, v_B_true, np.array(errs)


# ── Plotting ──────────────────────────────────────────────────────────────────

TRAJ_ALPHA = 0.35
N_TRAJ     = 12   # trajectories to show

def _traj_lines(ax, x_grid, history_pos, T_show, color):
    """Plot a few particle trajectories from history_pos."""
    M = history_pos.shape[1]
    rng = np.random.default_rng(1)
    chosen = rng.choice(M, size=N_TRAJ, replace=False)
    times = np.arange(T_show)
    for i in chosen:
        xs = x_grid[history_pos[:T_show, i]]
        ax.plot(xs, times, color=color, alpha=TRAJ_ALPHA, lw=0.8)


def plot_all(x_grid, psi0, V_barrier,
             res_old, res_adp05, rho_exact, pos_exact, res_adp20):

    T_show = T_TICKS
    fig = plt.figure(figsize=(18, 11))
    gs_outer = gridspec.GridSpec(3, 4, figure=fig,
                                  hspace=0.45, wspace=0.35,
                                  height_ratios=[2.5, 1.5, 1.5])

    titles = [
        'Old Solver  (3 candidates, dt=0.05)',
        'AdaptiveSolver  (ℓ=c·dt³/², dt=0.05)',
        'Exact Bohmian  (Euler, dt=0.20)',
        'AdaptiveSolver  (ℓ=c·dt³/², dt=0.20)',
    ]
    colors = ['tomato', 'steelblue', 'forestgreen', 'darkorange']

    all_pos   = [res_old['history_pos'], res_adp05['history_pos'],
                 pos_exact,             res_adp20['history_pos']]
    all_rho   = [res_old['history_rho'], res_adp05['history_rho'],
                 rho_exact,             res_adp20['history_rho']]

    # ── Row 0: Trajectories ───────────────────────────────────────────────────
    for col, (title, hp, hr, color) in enumerate(zip(titles, all_pos, all_rho, colors)):
        ax = fig.add_subplot(gs_outer[0, col])
        # Background: density heatmap
        ax.imshow(np.array(hr).T, aspect='auto', origin='lower',
                  extent=[0, T_show, x_grid[0], x_grid[-1]],
                  cmap='magma', interpolation='nearest', alpha=0.75)
        # Trajectories
        _traj_lines(ax, x_grid, hp, T_show, color='white')
        ax.set_title(title, fontsize=9, pad=4)
        ax.set_xlabel('step', fontsize=8)
        if col == 0:
            ax.set_ylabel('position x', fontsize=9)
        ax.tick_params(labelsize=7)

    # ── Row 1: Final density vs |ψ_T|² ───────────────────────────────────────
    n_bins = 60
    bins   = np.linspace(x_grid[0], x_grid[-1], n_bins + 1)
    bctrs  = 0.5 * (bins[:-1] + bins[1:])

    for col, (hp, hr, color, title) in enumerate(zip(all_pos, all_rho, colors, titles)):
        ax = fig.add_subplot(gs_outer[1, col])
        # Analytic |ψ_T|²
        rho_T = hr[-1]
        norm = np.trapezoid(rho_T, x_grid)
        rho_T_norm = rho_T / norm if norm > 0 else rho_T
        ax.plot(x_grid, rho_T_norm, 'k-', lw=2, label=r'$|\psi_T|^2$', zorder=5)
        # Empirical
        final_idx = hp[-1]
        final_xs  = x_grid[final_idx]
        h, _ = np.histogram(final_xs, bins=bins, density=True)
        ax.bar(bctrs, h, width=(bins[1]-bins[0]), alpha=0.5, color=color, label='particles')
        # TV distance
        h_norm = h / h.sum() if h.sum() > 0 else h
        rt_norm = rho_T_norm / rho_T_norm.sum() if rho_T_norm.sum() > 0 else rho_T_norm
        rt_on_bins = np.interp(bctrs, x_grid, rho_T_norm)
        rt_on_bins /= rt_on_bins.sum() if rt_on_bins.sum() > 0 else 1.0
        tv = 0.5 * np.sum(np.abs(h_norm - rt_on_bins))
        ax.text(0.97, 0.97, f'TV={tv:.3f}', transform=ax.transAxes,
                ha='right', va='top', fontsize=8,
                bbox=dict(boxstyle='round', fc='white', alpha=0.7))
        ax.set_title(f'Final density  (T={T_TICKS})', fontsize=8, pad=3)
        if col == 0:
            ax.set_ylabel('density', fontsize=8)
        ax.legend(fontsize=7, loc='upper left')
        ax.tick_params(labelsize=7)
        ax.grid(True, alpha=0.2)

    # ── Row 2: Velocity error vs position, multiple dt ────────────────────────
    ax_vel = fig.add_subplot(gs_outer[2, :2])
    ax_vel_r = fig.add_subplot(gs_outer[2, 2:])

    psi_init = build_psi0(x_grid)   # t=0 wavefunction for clean comparison

    dt_vals_test = [0.05, 0.10, 0.20]
    palette = ['navy', 'royalblue', 'cornflowerblue']

    for dt_test, col_c in zip(dt_vals_test, palette):
        # Old solver
        pos_s, v_true, e_old = velocity_error_old(x_grid, psi_init, dt_test)
        ax_vel.scatter(pos_s, e_old, s=6, alpha=0.4, color=col_c,
                       label=f'Old  Δt={dt_test}')
        # Adaptive solver
        adp_tmp = AdaptiveSolver(x_grid, dt_base=dt_test, c_scale=1.0,
                                  v_max=8.0, alpha_entropic=0.0, M_particles=1)
        mean_err, p2, u_c2, v_B2 = adp_tmp.velocity_error_at(psi_init, dt_test, n_sample=300)
        ax_vel_r.scatter(p2, np.abs(u_c2 - v_B2), s=6, alpha=0.4, color=col_c,
                          label=f'Adaptive  Δt={dt_test}  mean={mean_err:.3f}')

    ax_vel.set_title('Old solver: velocity error ‖u_c − v_B‖  vs position', fontsize=9)
    ax_vel.set_xlabel('position x', fontsize=8)
    ax_vel.set_ylabel('velocity error', fontsize=8)
    ax_vel.legend(fontsize=7)
    ax_vel.grid(True, alpha=0.2)
    ax_vel.tick_params(labelsize=7)

    ax_vel_r.set_title('AdaptiveSolver: velocity error vs position', fontsize=9)
    ax_vel_r.set_xlabel('position x', fontsize=8)
    ax_vel_r.set_ylabel('velocity error', fontsize=8)
    ax_vel_r.legend(fontsize=7)
    ax_vel_r.grid(True, alpha=0.2)
    ax_vel_r.tick_params(labelsize=7)

    plt.suptitle('Experiment 05 — Old Solver vs AdaptiveSolver: Double Slit Comparison',
                 fontsize=14, fontweight='bold', y=1.01)

    outpath = OUTDIR / '05_adaptive_solver_comparison.png'
    fig.savefig(str(outpath), dpi=130, bbox_inches='tight')
    plt.close(fig)
    print(f"\nSaved: {outpath}")


if __name__ == '__main__':
    print("Experiment 05: Old Solver vs AdaptiveSolver — Double Slit")
    print("=" * 60)
    print(f"Setup: N={N}, T={T_TICKS}, M={M_PART} particles\n")

    x_grid, psi0, V_barrier, res_old, res_adp05, rho_exact, pos_exact, res_adp20 = run_all()
    plot_all(x_grid, psi0, V_barrier, res_old, res_adp05, rho_exact, pos_exact, res_adp20)

    print("\nDone.")
