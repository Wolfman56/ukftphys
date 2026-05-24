#!/usr/bin/env python3
"""
Exp 107 — KZM Square-AF Ising: Python Ground Truth
====================================================

Reference (CPU) implementation of the square-lattice antiferromagnetic (AF)
Ising model with checkerboard Metropolis dynamics.

PURPOSE: Ground-truth validator for the WGSL/GPU implementation in NooGine.
         NOT for actual Exp 107 measurements (too slow at large L).

Model
-----
  H = J_AF · Σ_{NN} σ_i · σ_j     (J_AF = 0.5, positive = AF coupling)

  Square lattice, L×L, periodic BC.
  Sublattices:
    A = {(i,j) : (i+j)%2 == 0}
    B = {(i,j) : (i+j)%2 == 1}
  Ground state: A=+1, B=−1 (or vice versa).

  T_c(J_AF=0.5) = 2·J_AF / ln(1+√2) ≈ 1.135,   β_c ≈ 0.882

Cooling schedule
----------------
  β_hot = 0.10, β_cold = 4.00, linear ramp over n_sweeps steps.
  T_c crossed at ≈ (β_c − β_hot)/(β_cold − β_hot) ≈ 20% of the sweep.

  The ramp is identical to the WGSL/Rust implementation so that the
  two implementations can be compared directly at the same seed.

Domain wall density (DWD)
--------------------------
  Bond σ_i–σ_j is an AF domain wall when σ_i·σ_j > 0 (same sign = violates AF order).
  DWD = (n same-sign NN bonds) / (2·L²)
    Perfect AF ground state → DWD = 0
    Random T→∞ state       → DWD ≈ 0.5

KZM prediction (2D Ising universality)
---------------------------------------
  DWD ∝ n_sweeps^(−ν/(1+νz)) = n_sweeps^(−1/3)
  ν=1, z=2 (model-A dynamics), exponent ≈ −0.333

Validation parameters
---------------------
  L ∈ {8, 16, 32}  — small enough for NumPy (each run < 1 s)
  n_sweeps ∈ {100, 200, 500, 1000, 2000, 5000}  — 1.7 decades
  N_REPEATS = 20

Output
------
  107_gt_raw.csv     — per-replica rows: L, n_sweeps, rep, dwd, seed
  107_gt_summary.csv — aggregate rows:   L, n_sweeps, dwd_mean, dwd_std, n_reps

  The validate_against_rust() function compares a Rust CSV (same format as
  107_gt_raw.csv) against the Python summary.  Run Rust with mode=validate
  and redirect stdout to 107_rust_output.csv, then call this script again.
"""

import csv
import os
import time
from collections import defaultdict

import numpy as np
from scipy.stats import linregress

# ── UKFT constants ─────────────────────────────────────────────────────────
PHI    = (1.0 + 5.0**0.5) / 2.0   # 1.618…
W_STAR = 0.338_799_85

# ── Model parameters ───────────────────────────────────────────────────────
J_AF       = 0.5                                      # AF coupling (J > 0)
T_C        = 2.0 * J_AF / np.log(1.0 + np.sqrt(2.0)) # ≈ 1.1347
BETA_C     = 1.0 / T_C                                # ≈ 0.8814
BETA_HOT   = 0.10   # start: high T, fully disordered
BETA_COLD  = 4.00   # end:   low T, well-ordered

# ── Validation study parameters ────────────────────────────────────────────
VALID_SIZES   = [8, 16, 32]
N_SWEEPS_LIST = [100, 200, 500, 1000, 2000, 5000]
N_REPEATS     = 20
BASE_SEED     = 42

# ── KZM theory ─────────────────────────────────────────────────────────────
NU         = 1.0
Z_DYN      = 2.0
EXP_THEORY = NU / (1.0 + NU * Z_DYN)   # 1/3 ≈ 0.333
EXP_LO     = 0.20   # loose bounds for small-L finite-size noise
EXP_HI     = 0.50


# ══════════════════════════════════════════════════════════════════════════════
# Physics implementation
# ══════════════════════════════════════════════════════════════════════════════

class SquareAFIsing:
    """
    Square-lattice AF Ising model with 2-sublattice checkerboard Metropolis.

    Mirrors the WGSL implementation in noogine/src/gpu/shaders/ising_metropolis.wgsl
    exactly so that DWD values can be compared at the same (L, n_sweeps, seed).

    State:
      spins     — (L, L) float64 array of ±1 values
      sublattice — parity(i,j) = (i+j) % 2  →  0=A, 1=B

    Domain wall convention (matching WGSL):
      Bond (i,j)-(nbr) is a domain wall when spins[i,j] * spins[nbr] > 0.
      DWD = fraction of such bonds over all 2·L² NN bonds.
    """

    def __init__(self, L: int, seed: int) -> None:
        self.L   = L
        self.rng = np.random.default_rng(seed)
        # Hot start: uniformly random ±1 (matching Rust PCG hot-start)
        self.spins = self.rng.choice(
            [-1.0, 1.0], size=(L, L)
        ).astype(np.float64)

    # ── Single Metropolis sweep ───────────────────────────────────────────

    def _sweep(self, beta: float) -> None:
        """
        One full sweep = two sublattice passes (parity 0 then parity 1).

        For each sublattice:
          ΔE = −2·J_AF·σ_i·(σ_N + σ_S + σ_E + σ_W)
          Accept if ΔE < 0 or uniform[0,1) < exp(−β·ΔE).

        Vectorised over the L×L grid: all sites of the same sublattice are
        updated simultaneously (correct because no two A-sites share a NN bond).
        """
        sigma = self.spins
        ii, jj = np.meshgrid(np.arange(self.L), np.arange(self.L), indexing='ij')
        parity = (ii + jj) % 2

        for sub in range(2):
            # 4-NN sum (periodic BC via np.roll)
            nn_sum = (
                np.roll(sigma, -1, axis=0)   # east  (i+1, j)
              + np.roll(sigma, +1, axis=0)   # west  (i-1, j)
              + np.roll(sigma, -1, axis=1)   # north (i, j+1)
              + np.roll(sigma, +1, axis=1)   # south (i, j-1)
            )
            # ΔE = −2·J·σ_center·(Σ_nn σ_j)
            dE   = -2.0 * J_AF * sigma * nn_sum
            r    = self.rng.random((self.L, self.L))
            # Accept: lower energy OR Boltzmann roll (clip to avoid exp overflow)
            acc  = (dE < 0.0) | (r < np.exp(-beta * np.clip(dE, None, 500.0)))
            flip = acc & (parity == sub)
            sigma = np.where(flip, -sigma, sigma)

        self.spins = sigma

    # ── KZM cooling run ───────────────────────────────────────────────────

    def run(self, n_sweeps: int) -> float:
        """
        Cool β linearly from BETA_HOT → BETA_COLD over n_sweeps Metropolis sweeps.
        Returns final domain wall density (DWD).
        """
        betas = np.linspace(BETA_HOT, BETA_COLD, n_sweeps)
        for beta in betas:
            self._sweep(float(beta))
        return self._dwd()

    # ── Domain wall density ───────────────────────────────────────────────

    def _dwd(self) -> float:
        """
        Fraction of NN bonds where σ_i·σ_j > 0 (domain wall in AF order).

        Counts right-bonds  σ(i,j)·σ(i+1,j)  and
               down-bonds   σ(i,j)·σ(i,j+1)
        with periodic BC.  Denominator = 2·L² (total NN bond count).
        """
        s = self.spins
        bonds_right = s * np.roll(s, -1, axis=0)   # σ(i,j)·σ(i+1,j)
        bonds_down  = s * np.roll(s, -1, axis=1)   # σ(i,j)·σ(i,j+1)
        n_walls = int(np.sum(bonds_right > 0)) + int(np.sum(bonds_down > 0))
        n_bonds = 2 * self.L * self.L
        return float(n_walls) / max(n_bonds, 1)


# ══════════════════════════════════════════════════════════════════════════════
# Experiment runner
# ══════════════════════════════════════════════════════════════════════════════

def run_ground_truth() -> list:
    """
    Run all (L, n_sweeps, rep) combinations.
    Returns list of dicts with keys: L, n_sweeps, rep, dwd, seed.
    """
    rows  = []
    total = len(VALID_SIZES) * len(N_SWEEPS_LIST) * N_REPEATS
    idx   = 0
    t0    = time.time()

    for L in VALID_SIZES:
        for n in N_SWEEPS_LIST:
            for rep in range(N_REPEATS):
                # Seed formula must match Rust:
                #   seed = BASE_SEED + rep*997 + L*7 + n  (all wrapping u32 additions)
                seed = (BASE_SEED + rep * 997 + L * 7 + n) & 0xFFFFFFFF
                sim  = SquareAFIsing(L=L, seed=seed)
                dwd  = sim.run(n_sweeps=n)
                rows.append({"L": L, "n_sweeps": n, "rep": rep, "dwd": dwd, "seed": seed})
                idx += 1
                print(
                    f"  [{idx:>4}/{total}] L={L:>3} n={n:>5} rep={rep+1:>2}/{N_REPEATS}"
                    f"  DWD={dwd:.6f}  ({time.time()-t0:.1f}s)",
                    flush=True,
                )

    return rows


def summarise(rows: list) -> list:
    """Aggregate per (L, n_sweeps): mean and std DWD across repeats."""
    buckets: dict = defaultdict(list)
    for r in rows:
        buckets[(r["L"], r["n_sweeps"])].append(r["dwd"])

    summary = []
    for (L, n) in sorted(buckets):
        vals = buckets[(L, n)]
        summary.append({
            "L":        L,
            "n_sweeps": n,
            "dwd_mean": float(np.mean(vals)),
            "dwd_std":  float(np.std(vals, ddof=1) if len(vals) > 1 else 0.0),
            "n_reps":   len(vals),
        })
    return summary


# ══════════════════════════════════════════════════════════════════════════════
# KZM analysis
# ══════════════════════════════════════════════════════════════════════════════

def fit_kzm(summary_rows: list, L: int) -> dict:
    """
    Log-log regression: log(DWD) = slope·log(n_sweeps) + const.
    KZM theory: slope ≈ −1/3 (slower quench → fewer domain walls).
    """
    sel = [r for r in summary_rows if r["L"] == L and r["dwd_mean"] > 1e-9]
    if len(sel) < 3:
        return {"exponent": float("nan"), "A": float("nan"), "r2": 0.0}
    xs = np.log([r["n_sweeps"] for r in sel])
    ys = np.log([r["dwd_mean"]  for r in sel])
    slope, intercept, r, _, _ = linregress(xs, ys)
    return {"exponent": float(slope), "A": float(np.exp(intercept)), "r2": float(r**2)}


# ══════════════════════════════════════════════════════════════════════════════
# Rust validation
# ══════════════════════════════════════════════════════════════════════════════

def validate_against_rust(rust_csv: str, summary_rows: list, tol: float = 0.05) -> bool:
    """
    Compare Rust output CSV against Python ground truth.

    Rust CSV format (stdout of `ising_kzm validate`):
        L,n_sweeps,rep,dwd

    For each (L, n_sweeps) bucket, compares mean DWD.
    Returns True if max discrepancy < tol.

    Note: exact per-replica match is NOT expected (Python uses numpy RNG,
    Rust uses PCG hash).  Only mean DWD should agree within ~tol.
    """
    if not os.path.exists(rust_csv):
        print(f"[validate] Rust CSV not found: {rust_csv}  — skipping")
        return False

    # Load Rust rows
    rust_buckets: dict = defaultdict(list)
    with open(rust_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (int(row["L"]), int(row["n_sweeps"]))
            rust_buckets[key].append(float(row["dwd"]))

    print("\n── Rust vs Python validation ─────────────────────────────────────")
    print(f"  {'L':>5} {'n_sweeps':>8}  {'py_mean':>8}  {'rs_mean':>8}  {'|Δ|':>7}  {'status':>6}")
    max_delta = 0.0
    all_pass  = True

    for r in summary_rows:
        key = (r["L"], r["n_sweeps"])
        if key not in rust_buckets:
            print(f"  {key[0]:>5} {key[1]:>8}  {'—':>8}  {'—':>8}  {'—':>7}  MISSING")
            all_pass = False
            continue
        py_mean = r["dwd_mean"]
        rs_mean = float(np.mean(rust_buckets[key]))
        delta   = abs(py_mean - rs_mean)
        max_delta = max(max_delta, delta)
        status = "PASS" if delta < tol else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"  {key[0]:>5} {key[1]:>8}  {py_mean:>8.5f}  {rs_mean:>8.5f}  {delta:>7.5f}  {status}")

    overall = "PASS" if (all_pass and max_delta < tol) else "FAIL"
    print(f"\n  Max |Δ| = {max_delta:.5f}  (tol={tol:.3f})  →  {overall}\n")
    return all_pass and max_delta < tol


# ══════════════════════════════════════════════════════════════════════════════
# I/O helpers
# ══════════════════════════════════════════════════════════════════════════════

def save_csv(rows: list, path: str) -> None:
    if not rows:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Saved {len(rows)} rows → {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    out_dir  = os.path.dirname(os.path.abspath(__file__))
    raw_csv  = os.path.join(out_dir, "107_gt_raw.csv")
    sum_csv  = os.path.join(out_dir, "107_gt_summary.csv")
    rust_csv = os.path.join(out_dir, "107_rust_output.csv")

    print("=" * 68)
    print("Exp 107 — Square-AF Ising: Python Ground Truth")
    print("=" * 68)
    print(f"  J_AF = {J_AF},  T_c ≈ {T_C:.4f},  β_c ≈ {BETA_C:.4f}")
    print(f"  β schedule: {BETA_HOT} → {BETA_COLD}")
    print(f"  Lattice sizes:  {VALID_SIZES}")
    print(f"  n_sweeps grid:  {N_SWEEPS_LIST}")
    print(f"  Repeats:        {N_REPEATS}")
    print(f"  Theory exponent: −{EXP_THEORY:.3f}  (DWD ∝ n^exponent)")
    print()

    rows    = run_ground_truth()
    summary = summarise(rows)

    save_csv(rows,    raw_csv)
    save_csv(summary, sum_csv)

    # ── KZM fit (sanity check on ground truth) ────────────────────────────
    print("\n── KZM fit (Python ground truth, small L) ─────────────────────────")
    print(f"  Theory: exponent ≈ −{EXP_THEORY:.3f}")
    for L in VALID_SIZES:
        fit = fit_kzm(summary, L)
        flag = ""
        if not (EXP_LO <= abs(fit["exponent"]) <= EXP_HI):
            flag = "  ← outside [0.20, 0.50] (expected at small L)"
        print(
            f"  L={L:>3}  exponent={fit['exponent']:+.4f}"
            f"  R²={fit['r2']:.4f}{flag}"
        )

    print(
        "\n  Note: KZM fit at L≤32 is noisy (finite-size effects dominate).\n"
        "  The ground-truth purpose is validation of DWD magnitudes,\n"
        "  not a clean power-law fit.  Use Rust at L∈{64,128,256,512}\n"
        "  for the actual Exp 107 power-law measurement."
    )

    # ── Validate against Rust if output exists ─────────────────────────────
    validate_against_rust(rust_csv, summary)

    print("\nDone.")


if __name__ == "__main__":
    main()
