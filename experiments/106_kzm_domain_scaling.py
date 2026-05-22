#!/usr/bin/env python3
"""
Exp 106 — Kibble–Zurek Mechanism: Domain Wall Density Power Law
================================================================
Dedicated multi-rate, multi-size KZM study of the π_n Ising domain field.
Measures DWD ∝ τ_Q^{−ν/(1+νz)} and fits the KZM power-law exponent.

Motivation (flagged in Exp 105 H105-5):
  "KZM power-law needs dedicated multi-rate study" — this is that study.

Theory (2D Ising universality class):
  ν = 1   (correlation-length exponent)
  z = 2   (dynamical exponent, model-A dynamics)
  KZM prediction: DWD ∝ τ_Q^{−ν/(1+νz)} = τ_Q^{−1/3}  →  exponent ≈ 0.333

  Equivalently: DWD ∝ rate^{1/3}  where  rate = Δβ / τ_Q = (β_end − β_start) / n_sweeps.

Cooling schedule (same as Exp 105):
  β linearly from β_start = 0.2 → β_end = 6.0 in n_sweeps steps.
  T_c(J_MODE=0.50) = 2·J_MODE / ln(1+√2) ≈ 1.135, β_c ≈ 0.882.
  Schedule crosses T_c after ≈9% of the sweep regardless of n_sweeps,
  guaranteeing the KZM impulse-freeze picture holds across all rates.

Model:
  Pure 2D Ising domain model (no coupled spin MC).
  H = −J_MODE · Σ_{intra-NNN} π_i·π_j  −  J_CROSS · Σ_{inter-NN} π_A·π_B
  No external field (H_COUPLING = 0) → clean scaling.
  Honeycomb lattice, shape (L, L, 2), 3-colour × 2-sublattice checkerboard.

Study parameters:
  Lattice sizes L ∈ {16, 32, 64}
  Cooling times  n_sweeps ∈ {500, 1000, 2000, 4000, 8000, 16000}
  Repeats        N_REPEATS = 8  (average over independent initial conditions)

Hypotheses:
  H106-1: KZM power-law fit R² > 0.90  at L = 32
  H106-2: |KZM exponent| ∈ [0.25, 0.50]  (expected 1/3 for 2D Ising)
  H106-3: Exponent spread across L < 0.15  (finite-size consistent)

UKFT connection:
  DWD is the inverse of the knowledge coherence length ξ_k:
    ξ_k ∝ τ_Q^{1/3}
  which maps to UKFT: knowledge density ρ ∝ τ_Q^{1/3} near T_c.
  Faster quench → shorter ξ_k → more domain walls → less coherent altermagnetic signal.
  This validates the Czochralski analogy from Exp 105.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import time
from scipy.stats import linregress

# ── UKFT constants ────────────────────────────────────────────────────────────
PHI    = (1.0 + 5.0**0.5) / 2.0   # 1.618…
W_STAR = 0.338_799_85

# ── Domain Ising parameters (FeS, consistent with Exp 105) ───────────────────
J_MODE   = 0.50
J_CROSS  = 0.15
# T_c (2D Ising, J_MODE): 2*J/ln(1+√2) ≈ 1.135, β_c ≈ 0.882
T_C_DOMAIN = 2.0 * J_MODE / np.log(1.0 + np.sqrt(2.0))

BETA_START = 0.20
BETA_END   = 6.00
BETA_C     = 1.0 / T_C_DOMAIN   # ≈ 0.882 — crossed at (β_c - β_start)/(β_end - β_start) ≈ 9%

# ── KZM study parameters ─────────────────────────────────────────────────────
LATTICE_SIZES = [16, 32, 64]
N_SWEEPS_LIST = [500, 1000, 2000, 4000, 8000, 16000]
N_REPEATS     = 8
BASE_SEED     = 42

# ── KZM theory ───────────────────────────────────────────────────────────────
NU          = 1.0
Z_DYN       = 2.0
EXP_THEORY  = NU / (1.0 + NU * Z_DYN)   # 1/3
EXP_LO      = 0.25
EXP_HI      = 0.50

# ── NNN bond offsets (6 bonds, intra-sublattice, t1 + t2 triplets) ────────────
# t1: (+1,0), (-1,+1), (0,-1)
# t2: (0,+1), (-1,0), (+1,-1)
ALL_NNN = [(+1,0), (-1,+1), (0,-1), (0,+1), (-1,0), (+1,-1)]


# ── Domain Ising model ────────────────────────────────────────────────────────

class DomainIsingKZM:
    """
    Pure 2D Ising domain model on honeycomb for KZM power-law measurement.

    π_n ∈ {−1, +1} per site per sublattice.
    3-colour × 2-sublattice vectorised Metropolis.
    No coupled spin lattice (H_COUPLING = 0 for clean scaling).
    """

    def __init__(self, L: int, seed: int) -> None:
        self.Ni      = L
        self.Nj      = L
        self.rng     = np.random.default_rng(seed)
        self.pi_n    = self.rng.choice([-1.0, 1.0],
                                        size=(L, L, 2)).astype(np.float64)
        ii, jj       = np.meshgrid(np.arange(L), np.arange(L), indexing='ij')
        self.colour  = (ii + 2 * jj) % 3   # shape (L, L)

    # ── Single Metropolis sweep ───────────────────────────────────────────────

    def _sweep(self, beta: float) -> None:
        """3-colour × 2-sublattice checkerboard Metropolis."""
        for s in range(2):
            opp   = 1 - s
            m_opp = self.pi_n[:, :, opp]

            # Cross-sublattice NN sum (3 bonds per site)
            if s == 0:   # A bonds to B(i,j), B(i-1,j), B(i,j-1)
                nn_cross = (m_opp
                            + np.roll(m_opp, +1, axis=0)
                            + np.roll(m_opp, +1, axis=1))
            else:        # B bonds to A(i,j), A(i+1,j), A(i,j+1)
                nn_cross = (m_opp
                            + np.roll(m_opp, -1, axis=0)
                            + np.roll(m_opp, -1, axis=1))

            for c in range(3):
                m = self.pi_n[:, :, s]
                # Intra-sublattice NNN sum (6 bonds per site)
                nnn_sum = (np.roll(m, -1, axis=0)
                           + np.roll(np.roll(m, +1, axis=0), -1, axis=1)
                           + np.roll(m, +1, axis=1)
                           + np.roll(m, -1, axis=1)
                           + np.roll(m, +1, axis=0)
                           + np.roll(np.roll(m, -1, axis=0), +1, axis=1))

                dE   = (2.0 * J_MODE  * m * nnn_sum
                      + 2.0 * J_CROSS * m * nn_cross)
                rand = self.rng.random((self.Ni, self.Nj))
                acc  = (dE < 0.0) | (rand < np.exp(-beta * np.clip(dE, None, 500.0)))
                upd  = acc & (self.colour == c)
                self.pi_n[:, :, s] = np.where(upd, -m, m)

    # ── Run cooling schedule ──────────────────────────────────────────────────

    def run(self, n_sweeps: int) -> float:
        """Cool β linearly from BETA_START to BETA_END. Return final DWD."""
        betas = np.linspace(BETA_START, BETA_END, n_sweeps)
        for beta in betas:
            self._sweep(float(beta))
        return self._dwd()

    # ── Domain wall density ───────────────────────────────────────────────────

    def _dwd(self) -> float:
        """
        Fraction of intra-sublattice NNN bonds that cross a mode boundary.
        n_walls / (Ni * Nj * 2 * 6)  — same denominator used in Exp 105.
        """
        n_walls = 0
        n_bonds = 0
        for s in range(2):
            m = self.pi_n[:, :, s]
            for di, dj in ALL_NNN:
                nbr     = np.roll(np.roll(m, -di, axis=0), -dj, axis=1)
                n_walls += int(np.sum(m * nbr < 0))
                n_bonds += self.Ni * self.Nj
        return float(n_walls) / max(n_bonds, 1)


# ── KZM sweep ─────────────────────────────────────────────────────────────────

def run_kzm_sweep() -> dict:
    """
    Returns results[L] = list of (n_sweeps, dwd_mean, dwd_std) tuples.
    """
    results = {}
    total_runs = len(LATTICE_SIZES) * len(N_SWEEPS_LIST) * N_REPEATS
    run_idx    = 0
    t0 = time.time()

    for L in LATTICE_SIZES:
        rows = []
        for n in N_SWEEPS_LIST:
            dwds = []
            for rep in range(N_REPEATS):
                seed = BASE_SEED + rep * 997 + L * 7 + n
                sim  = DomainIsingKZM(L=L, seed=seed)
                dwd  = sim.run(n_sweeps=n)
                dwds.append(dwd)
                run_idx += 1
                elapsed = time.time() - t0
                print(f"  [{run_idx:>3}/{total_runs}] L={L:>3} n={n:>6}"
                      f" rep={rep+1}/{N_REPEATS} → DWD={dwd:.5f}"
                      f"  ({elapsed:.1f}s)", flush=True)
            dwd_mean = float(np.mean(dwds))
            dwd_std  = float(np.std(dwds, ddof=1) if len(dwds) > 1 else 0.0)
            rows.append((n, dwd_mean, dwd_std))
            print(f"  L={L:>3}  n={n:>6}  DWD={dwd_mean:.5f} ± {dwd_std:.5f}")
        results[L] = rows
    return results


# ── KZM power-law fit ─────────────────────────────────────────────────────────

def fit_kzm(ns: list, dwds: list) -> dict:
    """
    Log-log regression: log(DWD) = exponent·log(n_sweeps) + log(A).
    KZM theory: exponent ≈ −1/3 (DWD decreases as n_sweeps increases).
    Returns dict with keys: exponent, A (prefactor), r2.
    """
    valid = [(n, d) for n, d in zip(ns, dwds) if d > 1e-9 and n > 0]
    if len(valid) < 3:
        return {"exponent": float("nan"), "A": float("nan"), "r2": 0.0}
    xs = np.log([v[0] for v in valid])
    ys = np.log([v[1] for v in valid])
    slope, intercept, r, _, _ = linregress(xs, ys)
    return {"exponent": float(slope), "A": float(np.exp(intercept)), "r2": float(r**2)}


# ── Hypothesis evaluation ─────────────────────────────────────────────────────

def evaluate_hypotheses(results: dict) -> dict:
    """
    H106-1: R² > 0.90  at L = 32  (power-law describes data well)
    H106-2: |exponent| ∈ [0.25, 0.50]  at L = 32  (consistent with KZM 1/3)
    H106-3: exponent spread across L < 0.15  (finite-size independent)
    """
    fits = {}
    for L in LATTICE_SIZES:
        ns   = [row[0] for row in results[L]]
        dwds = [row[1] for row in results[L]]
        fits[L] = fit_kzm(ns, dwds)

    # H106-1 — goodness of fit at L=32
    r2_32 = fits[32]["r2"]
    h1 = ("PASS" if r2_32 > 0.90 else "FAIL",
          f"R²={r2_32:.3f} at L=32 (threshold 0.90)")

    # H106-2 — exponent magnitude at L=32
    exp_32 = abs(fits[32]["exponent"])
    h2 = ("PASS" if (EXP_LO <= exp_32 <= EXP_HI) else "FAIL",
          f"|exp|={exp_32:.3f} (expected [{EXP_LO:.2f},{EXP_HI:.2f}], theory 1/3)")

    # H106-3 — exponent spread across lattice sizes
    exps = [abs(fits[L]["exponent"]) for L in LATTICE_SIZES
            if not (fits[L]["exponent"] != fits[L]["exponent"])]  # filter nan
    if len(exps) >= 2:
        spread = float(max(exps) - min(exps))
        h3 = ("PASS" if spread < 0.15 else "FAIL",
              f"spread={spread:.3f} across L={LATTICE_SIZES}")
    else:
        h3 = ("FAIL", "insufficient L points for spread measure")

    n_pass = sum(1 for h in [h1, h2, h3] if h[0] == "PASS")
    return {
        "H106-1 R²>0.90":         h1,
        "H106-2 exp∈[0.25,0.50]": h2,
        "H106-3 L-scaling":       h3,
        "fits":                   fits,
        "n_pass":                 n_pass,
        "summary":                f"{n_pass}/3 PASS",
    }


# ── Figure ────────────────────────────────────────────────────────────────────

def make_figure(results: dict, hyp: dict) -> None:
    fits   = hyp["fits"]
    colors = {"L=16": "#4c72b0", "L=32": "#dd8452", "L=64": "#55a868"}
    lcolors = [colors["L=16"], colors["L=32"], colors["L=64"]]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle(
        "Exp 106 — KZM Domain Wall Density Power Law\n"
        "π_n Ising domain field on honeycomb (FeS parameters, no coupled spin)\n"
        f"β: {BETA_START}→{BETA_END}, T_c(J_MODE={J_MODE})≈{T_C_DOMAIN:.3f},  "
        f"Expected exponent 1/3≈{EXP_THEORY:.3f}",
        fontsize=10, fontweight="bold")

    # ── (0) Log-log DWD vs n_sweeps per L ────────────────────────────────────
    ax0 = axes[0]
    for L, col in zip(LATTICE_SIZES, lcolors):
        ns   = [row[0] for row in results[L]]
        dwds = [row[1] for row in results[L]]
        errs = [row[2] for row in results[L]]
        ax0.errorbar(ns, dwds, yerr=errs, fmt="o-", color=col,
                     lw=1.5, ms=5, capsize=3, label=f"L={L}")
        f = fits[L]
        if not (f["exponent"] != f["exponent"]):
            ns_arr  = np.array(ns, dtype=float)
            fit_arr = f["A"] * ns_arr ** f["exponent"]
            ax0.plot(ns_arr, fit_arr, "--", color=col, lw=1,
                     label=f"  fit exp={f['exponent']:.3f} R²={f['r2']:.3f}")

    # KZM theory reference at L=32 data level
    ns_ref = np.array(N_SWEEPS_LIST, dtype=float)
    mid_n  = ns_ref[len(ns_ref) // 2]
    mid_d  = results[32][len(ns_ref) // 2][1]
    ref    = mid_d * (ns_ref / mid_n) ** (-EXP_THEORY)
    ax0.plot(ns_ref, ref, "k:", lw=1.5, label=f"KZM theory n^{{−1/3}}")

    ax0.set_xscale("log"); ax0.set_yscale("log")
    ax0.set_xlabel("n_sweeps (cooling time τ_Q)", fontsize=9)
    ax0.set_ylabel("DWD (domain wall density)", fontsize=9)
    ax0.set_title("Log-Log: DWD vs n_sweeps", fontsize=10)
    ax0.legend(fontsize=7)
    ax0.tick_params(labelsize=8)

    # ── (1) Exponent vs L bar chart ───────────────────────────────────────────
    ax1 = axes[1]
    valid_Ls  = [L for L in LATTICE_SIZES
                 if not (fits[L]["exponent"] != fits[L]["exponent"])]
    exp_vals  = [abs(fits[L]["exponent"]) for L in valid_Ls]
    bars      = ax1.bar(range(len(valid_Ls)), exp_vals,
                        color=[lcolors[LATTICE_SIZES.index(L)] for L in valid_Ls],
                        alpha=0.8, edgecolor="black", linewidth=0.8)
    ax1.axhline(EXP_THEORY, color="black", ls="--", lw=1.5,
                label=f"Theory 1/3 ≈ {EXP_THEORY:.3f}")
    ax1.axhline(EXP_LO,     color="gray",  ls=":",  lw=1,  label=f"bounds [{EXP_LO},{EXP_HI}]")
    ax1.axhline(EXP_HI,     color="gray",  ls=":",  lw=1)
    ax1.set_xticks(range(len(valid_Ls)))
    ax1.set_xticklabels([f"L={L}" for L in valid_Ls], fontsize=9)
    ax1.set_ylabel("|KZM exponent|", fontsize=9)
    ax1.set_title("KZM Exponent by Lattice Size", fontsize=10)
    ax1.legend(fontsize=8)
    ax1.set_ylim(0.0, 0.75)
    ax1.tick_params(labelsize=8)
    for bar, ev in zip(bars, exp_vals):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                 f"{ev:.3f}", ha="center", va="bottom", fontsize=8)

    # ── (2) Hypothesis summary ────────────────────────────────────────────────
    ax2 = axes[2]
    ax2.axis("off")
    lines = [
        "Exp 106  KZM Domain Wall Scaling",
        "─" * 38,
        f"T_c(J_MODE={J_MODE}) = {T_C_DOMAIN:.3f}",
        f"β schedule: {BETA_START} → {BETA_END}",
        f"Lattice sizes: {LATTICE_SIZES}",
        f"Cooling rates: {N_SWEEPS_LIST}",
        f"Repeats/point: {N_REPEATS}",
        "",
        "Fits:",
    ]
    for L in LATTICE_SIZES:
        f = fits[L]
        if f["exponent"] == f["exponent"]:
            lines.append(f"  L={L:>3}: exp={f['exponent']:+.3f}  R²={f['r2']:.3f}")
        else:
            lines.append(f"  L={L:>3}: INSUFFICIENT DATA")
    lines += [
        "",
        "Theory: exp = −ν/(1+νz) = −1/3 ≈ −0.333",
        "(2D Ising: ν=1, z=2)",
        "",
        f"H106-1 {hyp['H106-1 R²>0.90'][0]}  {hyp['H106-1 R²>0.90'][1]}",
        f"H106-2 {hyp['H106-2 exp∈[0.25,0.50]'][0]}  {hyp['H106-2 exp∈[0.25,0.50]'][1]}",
        f"H106-3 {hyp['H106-3 L-scaling'][0]}  {hyp['H106-3 L-scaling'][1]}",
        "",
        f"Result: {hyp['summary']}",
    ]
    ax2.text(0.03, 0.97, "\n".join(lines), transform=ax2.transAxes,
             fontsize=7.5, va="top", family="monospace",
             bbox=dict(facecolor="#f0f4f8", edgecolor="#4c72b0",
                       boxstyle="round,pad=0.4"))

    plt.tight_layout()
    out_path = os.path.join(os.path.dirname(__file__), "106_kzm_domain_scaling.png")
    fig.savefig(out_path, dpi=110, bbox_inches="tight")
    print(f"[Exp 106] Figure saved → {out_path}")
    plt.close(fig)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 72)
    print("Experiment 106 — Kibble–Zurek Mechanism: Domain Wall Power Law")
    print(f"T_c(J_MODE={J_MODE}) = {T_C_DOMAIN:.4f}  β_c = {BETA_C:.4f}")
    print(f"KZM prediction: DWD ∝ n_sweeps^{{−{EXP_THEORY:.3f}}}")
    print(f"Lattice sizes:  {LATTICE_SIZES}")
    print(f"Cooling times:  {N_SWEEPS_LIST}  ({N_REPEATS} repeats each)")
    print("=" * 72)
    print()

    t_start = time.time()
    results = run_kzm_sweep()
    t_run   = time.time() - t_start
    print(f"\nSimulation complete in {t_run:.1f}s")

    hyp = evaluate_hypotheses(results)

    print("\n── Hypothesis Results ──")
    for key in ["H106-1 R²>0.90", "H106-2 exp∈[0.25,0.50]", "H106-3 L-scaling"]:
        status, detail = hyp[key]
        sym = "✓" if status == "PASS" else "✗"
        print(f"  {sym} {key}: {status}  ({detail})")
    print(f"\n  {hyp['summary']}")
    print()

    make_figure(results, hyp)

    # Text report
    out_dir = os.path.dirname(__file__)
    txt_path = os.path.join(out_dir, "106_kzm_domain_scaling_results.txt")
    with open(txt_path, "w") as f:
        f.write("Experiment 106 — KZM Domain Wall Density Power Law\n")
        f.write("=" * 60 + "\n")
        f.write(f"T_c(J_MODE={J_MODE}) = {T_C_DOMAIN:.4f}\n")
        f.write(f"KZM theory: DWD ∝ n_sweeps^{{-1/3}}  (2D Ising, ν=1, z=2)\n\n")
        for L in LATTICE_SIZES:
            f.write(f"L = {L}\n")
            for row in results[L]:
                n, dwd_m, dwd_s = row
                f.write(f"  n={n:>6}  DWD={dwd_m:.5f} ± {dwd_s:.5f}\n")
            fit = hyp["fits"][L]
            if fit["exponent"] == fit["exponent"]:
                f.write(f"  Fit: exponent={fit['exponent']:+.4f}  R²={fit['r2']:.4f}\n")
            f.write("\n")
        f.write("\nHypotheses:\n")
        for key in ["H106-1 R²>0.90", "H106-2 exp∈[0.25,0.50]", "H106-3 L-scaling"]:
            status, detail = hyp[key]
            f.write(f"  {key}: {status}  ({detail})\n")
        f.write(f"\nResult: {hyp['summary']}\n")
    print(f"[Exp 106] Results written → {txt_path}")


if __name__ == "__main__":
    main()
