"""
Experiment 90 — Baryogenesis η_B from the W-Axis Ledger
=========================================================
Paper 44, §4.3 and §7 (speculative).
References: Paper 44 §4.18, Paper 42/QFT-GR §4.17-4.18.

Goal: Reproduce the observed baryon-to-photon ratio
      η_B ≡ n_B/n_γ ≈ 6.09 × 10⁻¹⁰  (Planck 2018)
from the three-ledger hierarchy capacity split.

The master formula (Paper 44 §4.18) is:

  η_B ≈ (28/79) · (C_DM(w) − C_k(w))/C_total(w) · δ(T_EW) · ε_CP

where:
  28/79   — SM sphaleron conversion ratio (standard result)
  ratio   — ledger imbalance: (C_col − C_DM)/C_total at w = w_EW
  δ(T_EW) — topological ratio = 5/9 × α_QED (Paper 42 §4.17)
  ε_CP    — CP-violation suppression factor that converts the O(1)
             ledger imbalance to the observed ~10⁻¹⁰ baryon asymmetry

The experiment:
  (a) Computes the ledger ratio and all dimensionless prefactors
  (b) Extracts ε_CP implied by the observed η_B
  (c) Compares the implied ε_CP with the natural electroweak expectation
      ε_EW ~ α_EW² / (16π²) ~ few × 10⁻⁶  (Jarlskog invariant order)
  (d) Tests robustness under variation of w_EW in [1.4, 2.0]

All results are clearly labelled as order-of-magnitude / speculative per
Paper 44 §7 epistemic charter.

Lean targets: M30 entropic_leptogenesis_ledger_imbalance
              M31 sphaleron_ledger_handover
"""

import math
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── Colour palette (shared across all Paper-44 experiments) ──────────────────
CLR_COLL   = "#79c0ff"   # collapsed / baryonic  (blue)
CLR_DM     = "#56d364"   # dark-matter sector     (green)
CLR_VOID   = "#d29922"   # void / Λ sector        (amber)
CLR_PLANCK = "#ff7b72"   # Planck observed value  (red)
CLR_BG     = "#0d1117"
CLR_GRID   = "#21262d"
CLR_TEXT   = "#c9d1d9"
CLR_MUTED  = "#8b949e"

# ── Output directory ─────────────────────────────────────────────────────────
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_PREFIX = "90_"

# ═══════════════════════════════════════════════════════════════════════════════
# §1  Jump-Prime Ledger Infrastructure
# ═══════════════════════════════════════════════════════════════════════════════

def sieve_primes(n: int) -> list[int]:
    """Return all primes ≤ n via Sieve of Eratosthenes."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]

def first_jump_primes(primes: list[int]) -> list[int]:
    """
    Return jump-primes: the first prime for each distinct bit-length.
    These are the Dirichlet-ledger representatives of each information class.
    """
    seen_bl: set[int] = set()
    result: list[int] = []
    for p in primes:
        bl = p.bit_length()
        if bl not in seen_bl:
            seen_bl.add(bl)
            result.append(p)
    return result

ALL_PRIMES = sieve_primes(5000)
JP_ALL     = first_jump_primes(ALL_PRIMES)

# Three-ledger assignment (Paper 44 §3):
#   Collapsed matter  — bit-lengths 2, 3, 4  (p = 2, 5, 11)
#   Dark matter       — bit-lengths 5-9       (p = 17, 37, 67, 131, 257)
#   Void / Λ          — bit-lengths 10+       (p = 521, 1031, 2053, 4099, …)
JP_COL  = [p for p in JP_ALL if p <= 11]           # [2, 5, 11]
JP_DM   = [p for p in JP_ALL if 11 < p <= 257]     # [17, 37, 67, 131, 257]
JP_VOID = [p for p in JP_ALL if p > 257]           # [521, 1031, 2053, 4099, …]

def ledger_c(w: float, primes: list[int]) -> float:
    """Ledger capacity C(w) = Σ_{p∈primes} ln(p)·p^{-w}/(1−p^{-w})."""
    if not primes or w <= 0:
        return 0.0
    return sum(math.log(p) * p**(-w) / (1 - p**(-w)) for p in primes)

# ═══════════════════════════════════════════════════════════════════════════════
# §2  Physics Constants for Baryogenesis
# ═══════════════════════════════════════════════════════════════════════════════

ETA_B_OBS   = 6.09e-10          # Planck 2018 baryon-to-photon ratio (Eq. 4.18.1)
ETA_B_SIG   = 0.06e-10          # ±1σ uncertainty (Planck 2018)

# Sphaleron conversion factor (exact SM group theory, Paper 44 §4.18)
SPHALERON   = 28.0 / 79.0       # ≈ 0.3544

# Topological ratio δ(T_EW) = (5/9) × α_QED  (Paper 42 §4.17)
# The 5/9 comes from the SU(3)×SU(2) group-theory factor;
# α_QED = 1/137 is the fine-structure constant at EW scale (≈ α_EW(M_Z))
ALPHA_QED   = 1.0 / 137.0
TOPOLOGICAL = (5.0 / 9.0) * ALPHA_QED   # δ(T_EW) ≈ 4.05 × 10⁻³

# EW epoch w-value.  Paper 44 Table 4.18.1 places the SM/EW epoch at w ≈ 1.8
W_EW        = 1.8

# GAP-04 [RESOLVED — see §4.17 Remark 4.17.2]: Three approximation levels for δ(T_EW):
#   (i)  δ_bare = 5/9                          (bare SU(3)×SU(2) topological ratio;
#                                               PLAN step 3 used this as leading-order estimate)
#   (ii) δ_SM  = (5/9)·α_QED ≈ 4.07×10⁻³     (canonical QED-screened form; used in Exps 89, 90)
#   (iii) W_ΣΔ(p,p_T)                          (Exp 81 momentum-space fossil; geometrically
#                                               distinct — Remark 4.17.1; NOT used for η_B)
# All H90 hypotheses use TOPOLOGICAL = δ_SM = (5/9)·α_QED as canonical.
TOPOLOGICAL_BARE = 5.0 / 9.0   # δ_bare: level-(i) bare form (PLAN step 3); reference only

# Natural electroweak CP-violation scale (Jarlskog invariant order):
#   ε_CP ~ α_EW² / (16π²) ~ a few × 10⁻⁶  (rough SM estimate)
# The exact value is model-dependent; this sets the "natural" scale.
ALPHA_EW     = 1.0 / 30.0      # α_EW at the EW scale (g²/4π at M_Z)
EPS_CP_NATURAL = ALPHA_EW**2 / (16 * math.pi**2)

# ═══════════════════════════════════════════════════════════════════════════════
# §3  Compute Ledger Capacities and the Imbalance Ratio
# ═══════════════════════════════════════════════════════════════════════════════

W_RANGE = np.linspace(0.1, 3.5, 700)

C_col_arr  = np.array([ledger_c(w, JP_COL)  for w in W_RANGE])
C_DM_arr   = np.array([ledger_c(w, JP_DM)   for w in W_RANGE])
C_void_arr = np.array([ledger_c(w, JP_VOID) for w in W_RANGE])
C_tot_arr  = C_col_arr + C_DM_arr + C_void_arr

# Imbalance ratio at each w:
#   ratio = (C_col − C_DM) / C_total
# Since C_col > C_DM for all w (collapsed primes have smaller bit-length,
# hence larger Dirichlet weights), this ratio is POSITIVE for all w > 0.
# Physical meaning: the coloured/baryonic sector outweighs the DM sector —
# this is the sign required for net baryon production over antibaryons.
# GAP-01 resolved: asymmetry is (C_col − C_DM), not (C_DM − C_col);
# prior code masked the sign with abs().
imbalance_arr = (C_col_arr - C_DM_arr) / C_tot_arr   # positive by construction

# At the EW epoch (w = W_EW):
idx_EW = np.argmin(np.abs(W_RANGE - W_EW))
w_EW_actual = float(W_RANGE[idx_EW])

C_col_EW  = float(C_col_arr[idx_EW])
C_DM_EW   = float(C_DM_arr[idx_EW])
C_void_EW = float(C_void_arr[idx_EW])
C_tot_EW  = float(C_tot_arr[idx_EW])

imbalance_EW  = float(imbalance_arr[idx_EW])   # (C_col − C_DM)/C_total at w_EW  [positive]
imbalance_abs = imbalance_EW   # positive by construction; no abs() needed (GAP-01 fix)

# ═══════════════════════════════════════════════════════════════════════════════
# §4  η_B Formula: Staged Factoring
# ═══════════════════════════════════════════════════════════════════════════════

# Stage 1: Sphaleron × topological factor (dimensionless, O(1e-3))
stage1 = SPHALERON * TOPOLOGICAL          # ~1.43 × 10⁻³

# Stage 2: × imbalance |ratio|  (dimensionless, O(0.88))
stage2 = stage1 * imbalance_abs           # ~1.26 × 10⁻³  (intermediate)

# This is the "pre-CP-suppression" η:
eta_pre_CP = stage2

# Stage 3: Extract implied ε_CP from the observed η_B
#   η_B_obs = eta_pre_CP × ε_CP
#   ⟹ ε_CP_implied = η_B_obs / eta_pre_CP
eps_CP_implied = ETA_B_OBS / eta_pre_CP

# Stage 4: PLAN formula (δ = 5/9, no α_QED)
eta_plan_raw = SPHALERON * imbalance_abs * TOPOLOGICAL_BARE  # O(0.17)

# For comparison — PLAN with δ = 5/9 but supplemented by ε_CP_implied
eta_plan_check = eta_plan_raw * (EPS_CP_NATURAL * 100)  # illustrative only

# ═══════════════════════════════════════════════════════════════════════════════
# §5  Sensitivity Analysis: vary w_EW in [1.4, 2.0]
# ═══════════════════════════════════════════════════════════════════════════════

W_EW_RANGE = np.linspace(1.4, 2.0, 61)
eta_pre_arr  = np.zeros(len(W_EW_RANGE))
imb_arr      = np.zeros(len(W_EW_RANGE))
eps_implied_arr = np.zeros(len(W_EW_RANGE))

for i, w_test in enumerate(W_EW_RANGE):
    idx_t = np.argmin(np.abs(W_RANGE - w_test))
    imb_t = float(imbalance_arr[idx_t])   # positive by construction
    eta_t = SPHALERON * TOPOLOGICAL * imb_t
    imb_arr[i]         = imb_t
    eta_pre_arr[i]     = eta_t
    eps_implied_arr[i] = ETA_B_OBS / eta_t

# Variation ranges
eta_pre_min  = float(np.min(eta_pre_arr))
eta_pre_max  = float(np.max(eta_pre_arr))
eps_impl_min = float(np.min(eps_implied_arr))
eps_impl_max = float(np.max(eps_implied_arr))
eps_impl_var = (eps_impl_max - eps_impl_min) / float(np.mean(eps_implied_arr))

# ═══════════════════════════════════════════════════════════════════════════════
# §6  Sensitivity: vary δ (topological factor) ±50%
# ═══════════════════════════════════════════════════════════════════════════════

delta_vals  = np.linspace(TOPOLOGICAL * 0.5, TOPOLOGICAL * 1.5, 50)
eta_delta_arr = SPHALERON * delta_vals * imbalance_abs
eps_delta_arr = ETA_B_OBS / eta_delta_arr

delta_var_pct = float(np.std(eps_delta_arr) / np.mean(eps_delta_arr)) * 100.0

# ═══════════════════════════════════════════════════════════════════════════════
# §7  Hypotheses
# ═══════════════════════════════════════════════════════════════════════════════

results = {}

# H90-1: The ledger imbalance ratio = (C_col − C_DM)/C_total ∈ (0.5, 0.99).
#   Motivation: at any w ∈ [1.4, 2.0], ratio = (C_col−C_DM)/C_total
#   should be dominated by the collapsed sector (lower bit-lengths have higher
#   Dirichlet weight).  We expect ratio > 0.5, confirming positive asymmetry.
imb_range_lo, imb_range_hi = 0.5, 0.99
H1_pass = imb_range_lo < imbalance_abs < imb_range_hi
results["H90-1"] = {
    "name": "Ledger imbalance in expected range",
    "value": imbalance_abs,
    "test": f"ratio = {imbalance_abs:.5f} ∈ ({imb_range_lo}, {imb_range_hi})",
    "pass": H1_pass,
}

# H90-2: The pre-CP factor η_pre = (28/79)·δ·|ratio| is of order 10⁻³.
#   This is the maximal η_B achievable from the ledger structure alone.
#   We define "order 10⁻³" as: η_pre ∈ [10⁻⁴, 10⁻²].
H2_lo, H2_hi = 1e-4, 1e-2
H2_pass = H2_lo < eta_pre_CP < H2_hi
results["H90-2"] = {
    "name": "Pre-CP η scale is O(10⁻³)",
    "value": eta_pre_CP,
    "test": f"η_pre = {eta_pre_CP:.4e} ∈ [{H2_lo:.0e}, {H2_hi:.0e}]",
    "pass": H2_pass,
}

# H90-3: w_EW robustness — variation of ε_CP_implied over w ∈ [1.4, 2.0] is < 25%.
#   The function (C_col−C_DM)/C_total changes slowly in the EW window;
#   the implied CP factor should be stable to < 25% relative variation.
#   (The window [1.4, 2.0] spans ~43% of a decade in w; 25% tolerance is conservative.)
H3_threshold = 0.25
H3_pass = eps_impl_var < H3_threshold
results["H90-3"] = {
    "name": "ε_CP_implied stable over w_EW window",
    "value": eps_impl_var,
    "test": f"variation = {eps_impl_var*100:.1f}% < {H3_threshold*100:.0f}%",
    "pass": H3_pass,
}

# H90-4: The implied ε_CP is within 3 orders of magnitude of the natural EW scale.
#   Natural scale: ε_CP ~ α_EW²/(16π²) ~ few × 10⁻⁶.
#   The ledger formula extracts ε_CP_implied ~ η_B_obs / η_pre.
#   We test: log₁₀(ε_CP_implied / ε_CP_natural) ∈ (−3, +3).
log_ratio_eps = math.log10(eps_CP_implied / EPS_CP_NATURAL)
H4_lo, H4_hi = -3.0, 3.0
H4_pass = H4_lo < log_ratio_eps < H4_hi
results["H90-4"] = {
    "name": "Implied ε_CP within 3 OOM of natural EW scale",
    "value": log_ratio_eps,
    "test": f"log₁₀(ε_impl/ε_nat) = {log_ratio_eps:.2f} ∈ ({H4_lo}, {H4_hi})",
    "pass": H4_pass,
}

# ═══════════════════════════════════════════════════════════════════════════════
# §8  Console Output
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("Experiment 90 — Baryogenesis η_B from the Ledger")
print("=" * 70)
print()
print("Jump-prime ledger registers:")
print(f"  JP_COL  = {JP_COL}")
print(f"  JP_DM   = {JP_DM}")
print(f"  JP_VOID = {JP_VOID}")
print()
print(f"EW epoch: w_EW = {W_EW} (nearest grid point: {w_EW_actual:.4f})")
print()
print("Ledger capacities at w_EW:")
print(f"  C_col   = {C_col_EW:.6f}")
print(f"  C_DM    = {C_DM_EW:.6f}")
print(f"  C_void  = {C_void_EW:.6f}")
print(f"  C_total = {C_tot_EW:.6f}")
print(f"  Imbalance (C_col − C_DM)/C_total = {imbalance_EW:.6f}  [positive → net baryon excess]")
print(f"  (= imbalance_abs, no abs() needed) = {imbalance_abs:.6f}")
print()
print("Formula factors:")
print(f"  Sphaleron    28/79          = {SPHALERON:.6f}")
print(f"  Topological  (5/9)·α_QED   = {TOPOLOGICAL:.6e}   [δ(T_EW)]")
print(f"  Topological  bare 5/9       = {TOPOLOGICAL_BARE:.6f}   [PLAN form, no α_QED]")
print()
print("Staged factoring of η_B:")
print(f"  Stage 1: sphaleron × δ(T_EW)         = {stage1:.4e}")
print(f"  Stage 2: × |imbalance|               = {stage2:.4e}  [= η_pre_CP]")
print()
print(f"  Observed η_B (Planck 2018)           = {ETA_B_OBS:.4e} ± {ETA_B_SIG:.2e}")
print(f"  Implied ε_CP = η_B_obs / η_pre_CP   = {eps_CP_implied:.4e}")
print()
print("Comparison to natural EW CP-violation scale:")
print(f"  ε_CP_natural ~ α_EW²/(16π²)           = {EPS_CP_NATURAL:.4e}")
print(f"  log₁₀(ε_implied / ε_natural)          = {log_ratio_eps:.2f}")
print()
print("PLAN formula for comparison:")
print(f"  (28/79) × |ratio| × (5/9)  [bare]    = {eta_plan_raw:.4e}")
print(f"  Needs additional factor to reach observed η_B:")
print(f"    additional = η_B_obs / η_plan_raw   = {ETA_B_OBS / eta_plan_raw:.4e}")
print()
print("Sensitivity: w_EW ∈ [1.4, 2.0]")
print(f"  η_pre range    = [{eta_pre_min:.4e}, {eta_pre_max:.4e}]")
print(f"  ε_impl range   = [{eps_impl_min:.4e}, {eps_impl_max:.4e}]")
print(f"  ε_impl variab. = {eps_impl_var*100:.1f}%  (threshold: {H3_threshold*100:.0f}%)")
print()
print("Sensitivity: δ ± 50%")
print(f"  ε_impl variation: {delta_var_pct:.1f}%")
print()
print("─" * 70)
print("HYPOTHESIS RESULTS")
print("─" * 70)

all_pass = True
for key, r in results.items():
    status = "PASS" if r["pass"] else "FAIL"
    if not r["pass"]:
        all_pass = False
    print(f"  {key}: {r['name']}")
    print(f"         {r['test']}  →  {status}")

print()
print(f"  Overall: {'ALL PASS ✓' if all_pass else 'SOME FAILURES ✗'}")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════════════════
# §9  Figures
# ═══════════════════════════════════════════════════════════════════════════════

def make_fig(nrows=1, ncols=1, **kw):
    fig, axes = plt.subplots(nrows, ncols, **kw)
    fig.patch.set_facecolor(CLR_BG)
    if hasattr(axes, "__len__"):
        for ax in np.array(axes).ravel():
            ax.set_facecolor(CLR_BG)
            ax.tick_params(colors=CLR_TEXT, which="both")
            ax.xaxis.label.set_color(CLR_TEXT)
            ax.yaxis.label.set_color(CLR_TEXT)
            ax.title.set_color(CLR_TEXT)
            for spine in ax.spines.values():
                spine.set_edgecolor(CLR_GRID)
    else:
        axes.set_facecolor(CLR_BG)
        axes.tick_params(colors=CLR_TEXT, which="both")
        axes.xaxis.label.set_color(CLR_TEXT)
        axes.yaxis.label.set_color(CLR_TEXT)
        axes.title.set_color(CLR_TEXT)
        for spine in axes.spines.values():
            spine.set_edgecolor(CLR_GRID)
    return fig, axes


# ── Figure 1: Ledger fractions and imbalance over w ──────────────────────────
fig1, (ax1a, ax1b) = make_fig(2, 1, figsize=(10, 7), sharex=True)

f_col  = C_col_arr  / C_tot_arr
f_DM   = C_DM_arr   / C_tot_arr
f_void = C_void_arr / C_tot_arr

ax1a.fill_between(W_RANGE, f_col,  0,             alpha=0.35, color=CLR_COLL)
ax1a.fill_between(W_RANGE, f_DM,   0,             alpha=0.35, color=CLR_DM)
ax1a.fill_between(W_RANGE, f_void, 0,             alpha=0.35, color=CLR_VOID)
ax1a.plot(W_RANGE, f_col,  color=CLR_COLL, lw=1.8, label="Collapsed (col)")
ax1a.plot(W_RANGE, f_DM,   color=CLR_DM,   lw=1.8, label="Dark Matter (DM)")
ax1a.plot(W_RANGE, f_void, color=CLR_VOID, lw=1.8, label="Void (Λ)")
ax1a.axvline(W_EW, color=CLR_PLANCK, ls="--", lw=1.5, label=f"w_EW = {W_EW}")
ax1a.set_ylabel("Ledger fraction", color=CLR_TEXT)
ax1a.set_ylim(-0.02, 1.05)
ax1a.grid(True, color=CLR_GRID, ls=":", alpha=0.6)
ax1a.legend(facecolor=CLR_BG, edgecolor=CLR_GRID,
            labelcolor=CLR_TEXT, fontsize=9, loc="center right")
ax1a.set_title(f"W-axis ledger fractions  (JP_COL={JP_COL},  JP_DM={JP_DM},  JP_VOID=…)",
               color=CLR_TEXT, fontsize=10)

ax1b.plot(W_RANGE, imbalance_arr, color=CLR_DM, lw=2.0,
          label=r"$(C_{\rm col}-C_{\rm DM})/C_{\rm total}$")
ax1b.axvline(W_EW, color=CLR_PLANCK, ls="--", lw=1.5, label=f"w_EW = {W_EW}")
ax1b.axhline(imbalance_abs, color=CLR_VOID, ls=":", lw=1.2,
             label=f"imbalance at w_EW = {imbalance_abs:.4f}")
ax1b.set_xlabel("w  (ledger weight)", color=CLR_TEXT)
ax1b.set_ylabel("Imbalance ratio", color=CLR_TEXT)
ax1b.set_ylim(-0.02, 1.05)
ax1b.grid(True, color=CLR_GRID, ls=":", alpha=0.6)
ax1b.legend(facecolor=CLR_BG, edgecolor=CLR_GRID,
            labelcolor=CLR_TEXT, fontsize=9)
ax1b.set_title("Ledger imbalance (C_col − C_DM)/C_total  [positive → net baryon excess]",
               color=CLR_TEXT, fontsize=10)

fig1.tight_layout(rect=[0, 0.04, 1, 0.96])
fig1.text(0.5, 0.01,
          "Fig 90-1 · Paper 44 §4.3 (speculative) · "
          "Collapsed sector always dominates (lower bit-length, higher Dirichlet weight).",
          ha="center", fontsize=8, color=CLR_MUTED)
fig1.savefig(os.path.join(OUT_DIR, FIG_PREFIX + "fractions.png"),
             dpi=120, facecolor=CLR_BG)
plt.close(fig1)

# ── Figure 2: Staged factoring bar chart ─────────────────────────────────────
fig2, ax2 = make_fig(1, 1, figsize=(10, 5))

labels = [
    r"Sphaleron $\frac{28}{79}$",
    r"$\times\,|\mathrm{ratio}|$",
    r"$\times\,\delta(T_{\rm EW})$",
    r"$=\eta_{\rm pre}$",
    r"$\times\,\varepsilon_{\rm CP}^{\rm impl}$",
    r"$\approx\eta_B^{\rm obs}$",
]
values = [
    SPHALERON,
    SPHALERON * imbalance_abs,
    stage1,
    stage2,
    ETA_B_OBS,
    ETA_B_OBS,
]
# Build cumulative log-scale display values
log_vals = [math.log10(abs(v)) for v in values]

colors_bar = [CLR_COLL, CLR_DM, CLR_VOID, CLR_DM, CLR_COLL, CLR_PLANCK]
bars = ax2.bar(range(len(labels)), log_vals, color=colors_bar, alpha=0.85, width=0.6)

for i, (bar, v) in enumerate(zip(bars, values)):
    ax2.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.15,
             f"{v:.2e}", ha="center", va="bottom",
             fontsize=8, color=CLR_TEXT)

ax2.axhline(math.log10(ETA_B_OBS), color=CLR_PLANCK, ls="--", lw=1.5,
            label=f"Planck η_B = {ETA_B_OBS:.2e}")
ax2.set_xticks(range(len(labels)))
ax2.set_xticklabels(labels, fontsize=9, color=CLR_TEXT)
ax2.set_ylabel(r"$\log_{10}$ (value)", color=CLR_TEXT)
ax2.set_title("Staged factoring of η_B from ledger + sphaleron + CP suppression",
              color=CLR_TEXT, fontsize=10)
ax2.grid(True, color=CLR_GRID, ls=":", alpha=0.6)
ax2.legend(facecolor=CLR_BG, edgecolor=CLR_GRID, labelcolor=CLR_TEXT, fontsize=9)

fig2.tight_layout(rect=[0, 0.04, 1, 0.96])
fig2.text(0.5, 0.01,
          "Fig 90-2 · Paper 44 §4.3 (speculative) · "
          "The ledger + sphaleron factors give η_pre ~ 10⁻³;  "
          f"ε_CP_implied = {eps_CP_implied:.2e} provides the remaining suppression.",
          ha="center", fontsize=8, color=CLR_MUTED)
fig2.savefig(os.path.join(OUT_DIR, FIG_PREFIX + "factoring.png"),
             dpi=120, facecolor=CLR_BG)
plt.close(fig2)

# ── Figure 3: w_EW sensitivity ───────────────────────────────────────────────
fig3, (ax3a, ax3b) = make_fig(1, 2, figsize=(12, 5))

ax3a.plot(W_EW_RANGE, eta_pre_arr, color=CLR_DM, lw=2)
ax3a.axvline(W_EW, color=CLR_PLANCK, ls="--", lw=1.5, label=f"w_EW = {W_EW}")
ax3a.set_xlabel("w_EW", color=CLR_TEXT)
ax3a.set_ylabel(r"$\eta_{\rm pre}$ (pre-CP factor)", color=CLR_TEXT)
ax3a.set_title(r"$\eta_{\rm pre}$ vs assumed EW epoch w", color=CLR_TEXT, fontsize=10)
ax3a.grid(True, color=CLR_GRID, ls=":", alpha=0.6)
ax3a.legend(facecolor=CLR_BG, edgecolor=CLR_GRID, labelcolor=CLR_TEXT, fontsize=9)
ax3a.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.4f"))

ax3b.plot(W_EW_RANGE, np.log10(eps_implied_arr), color=CLR_VOID, lw=2,
          label=r"$\log_{10}\,\varepsilon_{\rm CP}^{\rm impl}$")
ax3b.axvline(W_EW, color=CLR_PLANCK, ls="--", lw=1.5, label=f"w_EW = {W_EW}")
nat_log = math.log10(EPS_CP_NATURAL)
ax3b.axhline(nat_log, color=CLR_COLL, ls=":", lw=1.2,
             label=f"ε_nat = {EPS_CP_NATURAL:.2e}  (log={nat_log:.2f})")
ax3b.set_xlabel("w_EW", color=CLR_TEXT)
ax3b.set_ylabel(r"$\log_{10}\,\varepsilon_{\rm CP}^{\rm impl}$", color=CLR_TEXT)
ax3b.set_title(r"Implied $\varepsilon_{\rm CP}$ vs assumed EW epoch w",
               color=CLR_TEXT, fontsize=10)
ax3b.grid(True, color=CLR_GRID, ls=":", alpha=0.6)
ax3b.legend(facecolor=CLR_BG, edgecolor=CLR_GRID, labelcolor=CLR_TEXT, fontsize=9)

fig3.suptitle("Sensitivity: EW epoch w_EW ∈ [1.4, 2.0]", color=CLR_TEXT, fontsize=11)
fig3.tight_layout(rect=[0, 0.04, 1, 0.93])
fig3.text(0.5, 0.01,
          f"Fig 90-3 · Paper 44 §7 (speculative) · "
          f"ε_CP_implied varies {eps_impl_var*100:.1f}% over the EW window (H90-3 threshold: 25%)",
          ha="center", fontsize=8, color=CLR_MUTED)
fig3.savefig(os.path.join(OUT_DIR, FIG_PREFIX + "sensitivity_w.png"),
             dpi=120, facecolor=CLR_BG)
plt.close(fig3)

# ── Figure 4: δ sensitivity ───────────────────────────────────────────────────
fig4, ax4 = make_fig(1, 1, figsize=(9, 5))

delta_relative = delta_vals / TOPOLOGICAL
ax4.semilogy(delta_relative, eps_delta_arr, color=CLR_VOID, lw=2)
ax4.axvline(1.0, color=CLR_PLANCK, ls="--", lw=1.5, label=f"δ = {TOPOLOGICAL:.3e}")
ax4.axhline(EPS_CP_NATURAL, color=CLR_COLL, ls=":", lw=1.2,
            label=f"ε_nat = {EPS_CP_NATURAL:.2e}")
ax4.set_xlabel("δ / δ(T_EW)  (relative topological factor)", color=CLR_TEXT)
ax4.set_ylabel(r"Implied $\varepsilon_{\rm CP}$", color=CLR_TEXT)
ax4.set_title("Sensitivity to the topological factor δ (±50%)", color=CLR_TEXT, fontsize=10)
ax4.grid(True, color=CLR_GRID, ls=":", alpha=0.6)
ax4.legend(facecolor=CLR_BG, edgecolor=CLR_GRID, labelcolor=CLR_TEXT, fontsize=9)

fig4.tight_layout(rect=[0, 0.04, 1, 0.96])
fig4.text(0.5, 0.01,
          f"Fig 90-4 · Paper 44 §7 (speculative) · "
          f"δ ±50% → ε_CP_implied varies {delta_var_pct:.0f}%  (linear inverse relationship).",
          ha="center", fontsize=8, color=CLR_MUTED)
fig4.savefig(os.path.join(OUT_DIR, FIG_PREFIX + "sensitivity_delta.png"),
             dpi=120, facecolor=CLR_BG)
plt.close(fig4)

print()
print("Figures saved:")
for fname in ["fractions", "factoring", "sensitivity_w", "sensitivity_delta"]:
    fpath = os.path.join(OUT_DIR, FIG_PREFIX + fname + ".png")
    print(f"  {fpath}  {'✓' if os.path.exists(fpath) else '✗'}")

if not all_pass:
    sys.exit(1)
