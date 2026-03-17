"""
Experiment 04: Choice Operator Convergence Rate + Equivariance

Tests the theoretical bound from Gap1 paper (Paper 34, papers/34_Choice_Guided_Bohmian_Mechanics.md).

The bound from the minimality inequality is:

    ||u_c - v_B|| ≤ ℓ/Δt  +  C·√Δt

NOT  C·Δt  as stated in the paper's proof sketch.

Why: comparing objective at minimiser vs at the "target" candidate gives
    m/2 ||u_c - v_B||^2  ≤  m/2 (ℓ/Δt)^2  +  L_W·c_r·Δt
Taking sqrt:  ||u_c - v_B||  ≤  ℓ/Δt + √(2 L_W c_r Δt / m)  =  ℓ/Δt + C·√Δt

Three solver regimes tested:
  1. Old (fixed lattice, 3 candidates)  — ℓ = dx  →  ℓ/Δt = dx/Δt  DIVERGES
  2. Dense discrete (ℓ = c·Δt^{3/2})  — ℓ/Δt = c·√Δt  →  O(√Δt) proven bound
  3. Continuous (scipy minimize)        — ℓ → 0  →  O(Δt) from first-order expansion
                                          (tighter than the bound proves!)

Physics setup:
  1D free particle, ħ = m = 1
  Initial state: ψ₀(x) ∝ exp(-(x-x₀)²/(4σ²) + ik₀x)
  Exact v_B(x) = k₀  (uniform — phase gradient is purely k₀ for Gaussian)
  Exact V_Q(x) = (4σ² - (x-x₀)²) / (8σ⁴)

Figure 1: log-log convergence — slope confirms O(√Δt) for dense, O(Δt) for continuous
Figure 2: single-step equivariance at Δt=0.1 — empirical density vs |ψ(Δt)|²
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import minimize_scalar
from pathlib import Path

OUTDIR = Path(__file__).parent

# ── Analytic physics: free particle Gaussian coherent state ───────────────────
K0    = 1.5     # initial momentum (ħ=m=1)
SIGMA = 2.0     # Gaussian width
X0    = 0.0     # centre

def v_bohmian(x: np.ndarray) -> np.ndarray:
    """Exact Bohmian velocity: uniform k₀ for Gaussian initial state."""
    return np.full_like(np.asarray(x, dtype=float), K0)

def V_quantum(x: np.ndarray) -> np.ndarray:
    """Exact quantum potential for Gaussian: (4σ²-(x-x₀)²) / (8σ⁴)."""
    x = np.asarray(x, dtype=float)
    return (4*SIGMA**2 - (x - X0)**2) / (8 * SIGMA**4)

def psi_density(x: np.ndarray, t: float = 0.0) -> np.ndarray:
    """
    |ψ(x,t)|² integrated over free-particle evolution.
    Centre shifts to X0 + K0*t; width expands to σ(t) = √(σ²+(t/(2σ))²).
    """
    x = np.asarray(x, dtype=float)
    sigma_t = np.sqrt(SIGMA**2 + (t / (2*SIGMA))**2)
    centre_t = X0 + K0 * t
    unnorm = np.exp(-(x - centre_t)**2 / (2*sigma_t**2))
    return unnorm / (np.sqrt(2*np.pi) * sigma_t)


# ── Three choice-operator implementations ─────────────────────────────────────

def _action(u: np.ndarray, x: float, dt: float) -> np.ndarray:
    """Discrete local action: S(u) = dt/2·(u−v_B)² + V_Q(x+u·dt/2)·dt."""
    return dt/2 * (u - K0)**2 + V_quantum(x + u*dt/2) * dt


def step_old(x: float, dt: float, dx: float = 0.25) -> float:
    """
    Old solver: 3 fixed lattice candidates {x-dx, x, x+dx}.
    Velocity options: {-dx/dt, 0, +dx/dt}.
    ℓ = dx is FIXED → ℓ/dt = dx/dt DIVERGES as dt→0.
    """
    u_cands = np.array([-dx/dt, 0.0, dx/dt])
    acts = _action(u_cands, x, dt)
    return x + u_cands[np.argmin(acts)] * dt


def step_dense(x: float, dt: float, c_scale: float = 1.0, v_max: float = 10.0) -> float:
    """
    Dense solver: velocity spacing δv = c_scale·√dt  →  ℓ = c_scale·dt^{3/2}.
    ℓ/dt = c_scale·√dt → 0 as dt→0.  Achieves O(√dt) bound.
    """
    dv = c_scale * np.sqrt(dt)
    u_cands = np.arange(-v_max, v_max + dv*0.5, dv)
    acts = _action(u_cands, x, dt)
    return x + u_cands[np.argmin(acts)] * dt


def step_continuous(x: float, dt: float, v_max: float = 10.0) -> float:
    """
    Continuous solver: scipy bounded minimisation over velocity.
    ℓ = 0 effectively → O(dt) from first-order potential shift.
    Better than the bound proves, because the bound is not tight.
    """
    res = minimize_scalar(lambda u: float(_action(np.array([u]), x, dt)[0]),
                          bounds=(-v_max, v_max), method='bounded',
                          options={'xatol': 1e-10})
    return x + res.x * dt


# ── Part A: Convergence rate sweep ────────────────────────────────────────────

def measure_convergence(n_test: int = 300, dx_old: float = 0.25) -> dict:
    """Sweep dt, measure mean ||u_c - v_B|| for all three solvers."""
    rng = np.random.default_rng(42)
    x_test = rng.normal(X0, SIGMA, size=n_test)

    dt_vals = np.logspace(-2.5, 0, 30)
    errs = {k: [] for k in ('old', 'dense', 'continuous')}

    for dt in dt_vals:
        e_old, e_den, e_con = [], [], []
        for x in x_test:
            v_true = K0
            u_old = (step_old(x, dt, dx=dx_old) - x) / dt
            u_den = (step_dense(x, dt) - x) / dt
            u_con = (step_continuous(x, dt) - x) / dt
            e_old.append(abs(u_old - v_true))
            e_den.append(abs(u_den - v_true))
            e_con.append(abs(u_con - v_true))
        errs['old'].append(np.mean(e_old))
        errs['dense'].append(np.mean(e_den))
        errs['continuous'].append(np.mean(e_con))

    return dt_vals, {k: np.array(v) for k, v in errs.items()}


def empirical_slope(dt_vals, errs, dt_max=0.05) -> float:
    """Log-log slope in the small-dt regime."""
    mask = (dt_vals < dt_max) & (errs > 0)
    if mask.sum() < 3:
        return float('nan')
    return float(np.polyfit(np.log(dt_vals[mask]), np.log(errs[mask]), 1)[0])


# ── Part B: Single-step equivariance ─────────────────────────────────────────

def measure_equivariance(dt: float = 0.10, M: int = 6000, n_bins: int = 80):
    """
    Sample M particles from |ψ₀|², apply one step, compare histogram to |ψ(dt)|².
    Returns (bin_centres, rho_true, hist_old, hist_dense, hist_cont).
    """
    rng = np.random.default_rng(99)
    x_range = np.linspace(-8, 8, 1000)

    # Sample from |ψ₀|² via rejection
    p0 = psi_density(x_range)
    p0 /= p0.sum()
    starts = rng.choice(x_range, size=M, p=p0)

    # Move particles
    x_old  = np.array([step_old(x, dt)        for x in starts])
    x_den  = np.array([step_dense(x, dt)       for x in starts])
    x_con  = np.array([step_continuous(x, dt)  for x in starts])

    # True target density at time dt
    bins = np.linspace(-8, 10, n_bins + 1)
    centres = 0.5 * (bins[:-1] + bins[1:])
    rho_true = psi_density(centres, t=dt)
    rho_true /= rho_true.sum()

    def hist_norm(positions):
        h, _ = np.histogram(positions, bins=bins)
        h = h.astype(float)
        h /= h.sum() if h.sum() > 0 else 1.0
        return h

    return centres, rho_true, hist_norm(x_old), hist_norm(x_den), hist_norm(x_con)


# ── Plotting ──────────────────────────────────────────────────────────────────

def run_and_plot():
    print("Part A: convergence sweep (≈30 dt values × 300 particles)...")
    dt_vals, errs = measure_convergence()

    print("Part B: equivariance check (6000 particles, one step)...")
    centres, rho_true, h_old, h_den, h_con = measure_equivariance()

    fig = plt.figure(figsize=(15, 6))
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.35)

    # ── Panel A: Convergence rate ─────────────────────────────────────────────
    ax = fig.add_subplot(gs[0])

    ax.loglog(dt_vals, errs['old'],        'r-o',  ms=4, lw=1.8,
              label=r'Old solver  (3 fixed, $\ell=dx$)  → $\ell/\Delta t$ diverges')
    ax.loglog(dt_vals, errs['dense'],      'b-s',  ms=4, lw=1.8,
              label=r'Dense solver ($\ell = c\,\Delta t^{3/2}$)  $\sim\Delta t^{0.5}$')
    ax.loglog(dt_vals, errs['continuous'], 'g-^',  ms=4, lw=1.8,
              label=r'Continuous (scipy)  $\sim\Delta t^{1.0}$')

    # Reference slope lines
    dt_ref = np.array([dt_vals[3], dt_vals[-2]])
    ax.loglog(dt_ref, 0.6  * dt_ref**(-1.0), 'r--', alpha=0.45, lw=1.2, label='slope −1')
    ax.loglog(dt_ref, 0.55 * dt_ref**0.5,    'b--', alpha=0.45, lw=1.2, label='slope +½')
    ax.loglog(dt_ref, 0.04 * dt_ref**1.0,    'g--', alpha=0.45, lw=1.2, label='slope +1')

    # Annotate empirical slopes
    s_den = empirical_slope(dt_vals, errs['dense'])
    s_con = empirical_slope(dt_vals, errs['continuous'])
    ax.text(0.04, 0.05, f'Dense slope: {s_den:.2f}  (theory: 0.50)\n'
                        f'Continuous slope: {s_con:.2f}  (theory: 1.00)\n\n'
                        r'Gap1 paper claims $O(\Delta t)$' '\n'
                        r'Minimality bound proves $O(\sqrt{\Delta t})$',
            transform=ax.transAxes, fontsize=8.5, va='bottom',
            bbox=dict(boxstyle='round', fc='lightyellow', alpha=0.85))

    ax.set_xlabel(r'$\Delta t$', fontsize=13)
    ax.set_ylabel(r'Mean $\|u_c - v_B\|$', fontsize=13)
    ax.set_title('Panel A — Convergence Rate of Choice Operator', fontsize=13)
    ax.legend(fontsize=8.5, loc='upper right')
    ax.grid(True, which='both', alpha=0.25)

    # ── Panel B: Equivariance ─────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1])

    ax2.plot(centres, rho_true, 'k-',  lw=2.5, label=r'Target $|\psi(\Delta t)|^2$', zorder=5)
    ax2.bar(centres, h_old,  width=(centres[1]-centres[0]),
            alpha=0.4, color='red',   label='Old solver')
    ax2.bar(centres, h_den,  width=(centres[1]-centres[0]),
            alpha=0.4, color='blue',  label='Dense solver')
    ax2.bar(centres, h_con,  width=(centres[1]-centres[0]),
            alpha=0.4, color='green', label='Continuous')

    # TV distances
    tv = lambda h: 0.5 * np.sum(np.abs(h - rho_true))
    ax2.text(0.97, 0.97,
             f'TV distance (Δt=0.10)\n'
             f'  Old:        {tv(h_old):.3f}\n'
             f'  Dense:      {tv(h_den):.3f}\n'
             f'  Continuous: {tv(h_con):.3f}',
             transform=ax2.transAxes, fontsize=8.5, va='top', ha='right',
             bbox=dict(boxstyle='round', fc='lightcyan', alpha=0.85))

    ax2.set_xlabel('position $x$', fontsize=13)
    ax2.set_ylabel('probability density', fontsize=13)
    ax2.set_title(r'Panel B — Single-Step Equivariance ($\Delta t = 0.10$)', fontsize=13)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.25)
    ax2.set_xlim(-8, 10)

    plt.suptitle('Experiment 04 — Choice Operator: Convergence Rate & Equivariance',
                 fontsize=14, fontweight='bold', y=1.01)

    outpath = OUTDIR / '04_convergence_equivariance.png'
    fig.savefig(str(outpath), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"\nSaved: {outpath}")

    # Print summary
    print("\n=== Empirical convergence slopes (small-dt regime) ===")
    print(f"  Old solver:   {empirical_slope(dt_vals, errs['old']):.2f}   (expected: ~0, saturates at constant error ≈ |v_B|)")
    print(f"  Dense solver: {empirical_slope(dt_vals, errs['dense']):.2f}   (expected: +0.5)")
    print(f"  Continuous:   {empirical_slope(dt_vals, errs['continuous']):.2f}   (expected: +1.0)")
    print("\n=== Equivariance TV distances at Δt=0.10 ===")
    print(f"  Old:        {tv(h_old):.4f}")
    print(f"  Dense:      {tv(h_den):.4f}")
    print(f"  Continuous: {tv(h_con):.4f}")


if __name__ == '__main__':
    print("Experiment 04: Choice Convergence Rate + Equivariance")
    print("=" * 55)
    run_and_plot()
    print("\nDone.")
