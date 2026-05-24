"""
Exp 108 — KZM Domain-Wall Density: Single-Wall Regime Analysis
===============================================================
Reads 107_exp108_raw.csv (L∈{256,512}, 6 n-values per L, N=200 reps) and produces:
  Fig 4 — log-log mean DWD vs n_sweeps per L  (+ OLS power-law overlays)
  Fig 5 — defect-probability (fraction non-zero reps) vs n_sweeps per L
  Fig 6 — per-L zero-censoring corrected fits (1×2 subplot)

Outputs:
  108_fig4_loglog_dwd.pdf / .png
  108_fig5_defect_prob.pdf / .png
  108_fig6_censored_fit.pdf / .png
  108_fit_summary.txt
"""

import pathlib
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats

# ── paths ──────────────────────────────────────────────────────────────────
HERE = pathlib.Path(__file__).parent
RAW  = HERE / "107_exp108_raw.csv"
OUT  = HERE  # write outputs alongside script

if not RAW.exists():
    raise FileNotFoundError(f"Input file not found: {RAW}")

# ── load & aggregate ───────────────────────────────────────────────────────
df = pd.read_csv(RAW)
print(f"Loaded {len(df)} rows from {RAW.name}")
print(f"L values: {sorted(df['L'].unique())}")
print(f"n_sweeps values: {sorted(df['n_sweeps'].unique())}")
print(f"Reps per (L, n): {df.groupby(['L','n_sweeps'])['rep'].count().to_dict()}")

agg = (
    df.groupby(["L", "n_sweeps"])["dwd"]
    .agg(
        mean_dwd="mean",
        std_dwd="std",
        n_nonzero=lambda x: (x > 0).sum(),
        n_total="count",
    )
    .reset_index()
)
agg["defect_prob"] = agg["n_nonzero"] / agg["n_total"]
agg["se_dwd"]      = agg["std_dwd"] / np.sqrt(agg["n_total"])

LS      = sorted(agg["L"].unique())
PALETTE = {256: "#2ca02c", 512: "#d62728"}
MARKERS = {256: "^",       512: "D"}

# ── OLS power-law fit helper ────────────────────────────────────────────────
def fit_powerlaw(n_arr, dwd_arr, mask=None):
    """
    Returns (exponent, intercept_log, r2, n_used).
    mask: boolean array — True = include. Default: all points where dwd > 0.
    """
    if mask is None:
        mask = dwd_arr > 0
    x = np.log(n_arr[mask])
    y = np.log(dwd_arr[mask])
    if x.size < 2:
        return np.nan, np.nan, np.nan, int(mask.sum())
    slope, intercept, r, *_ = stats.linregress(x, y)
    return slope, intercept, r**2, int(mask.sum())

# ── collect fit results ────────────────────────────────────────────────────
fit_all      = {}   # full dataset (any mean > 0)
fit_censored = {}   # restricted: n_nonzero >= 3 (at least 3/N non-zero)

MIN_NONZERO = 3

for L in LS:
    sub = agg[agg["L"] == L].sort_values("n_sweeps")
    n   = sub["n_sweeps"].values.astype(float)
    d   = sub["mean_dwd"].values

    fit_all[L]      = fit_powerlaw(n, d)

    mask_cens = sub["n_nonzero"].values >= MIN_NONZERO
    fit_censored[L] = fit_powerlaw(n, d, mask_cens)

# ── print quick summary to console ────────────────────────────────────────
print(f"\n{'L':>6}  {'n_pts':>6}  {'expo(all)':>10}  {'R²(all)':>8}  "
      f"{'expo(≥3nz)':>11}  {'R²(≥3nz)':>9}  {'n_pts_cens':>11}")
print("-" * 75)
for L in LS:
    ea, _, ra, na = fit_all[L]
    ec, _, rc, nc = fit_censored[L]
    print(f"{L:>6}  {na:>6}  {ea:>10.4f}  {ra:>8.4f}  "
          f"{ec:>11.4f}  {rc:>9.4f}  {nc:>11}")
print(f"\nTheory (2D model-A AF Ising, KZM): exponent = -1/3 ≈ -0.3333")

# ── per-L aggregation table ────────────────────────────────────────────────
print("\nPer-(L, n_sweeps) summary:")
print(agg[["L", "n_sweeps", "n_total", "n_nonzero", "defect_prob",
           "mean_dwd", "se_dwd"]].to_string(index=False))

# ── write fit summary ──────────────────────────────────────────────────────
summary_path = OUT / "108_fit_summary.txt"
with open(summary_path, "w") as f:
    f.write("Exp 108 — KZM Power-Law Fit Summary (Single-Wall Regime)\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Design: L∈{{256,512}}, n∈{{800,1600,3200,6400,12800,25600}}, N=200 reps\n")
    f.write(f"Input:  107_exp108_raw.csv\n\n")
    f.write(f"{'L':>6}  {'expo(all)':>10}  {'R²(all)':>8}  "
            f"{'expo(≥3nz)':>11}  {'R²(≥3nz)':>9}  {'n_pts':>6}\n")
    f.write("-" * 60 + "\n")
    for L in LS:
        ea, _, ra, na = fit_all[L]
        ec, _, rc, nc = fit_censored[L]
        f.write(f"{L:>6}  {ea:>10.4f}  {ra:>8.4f}  "
                f"{ec:>11.4f}  {rc:>9.4f}  {nc:>6}\n")
    f.write("\nTheory (2D model-A AF Ising, KZM): exponent = -1/3 ≈ -0.3333\n")
    f.write(f"Min nonzero threshold: {MIN_NONZERO} reps\n\n")
    f.write("Per-(L, n_sweeps) table:\n")
    f.write(agg[["L", "n_sweeps", "n_total", "n_nonzero", "defect_prob",
                  "mean_dwd", "se_dwd"]].to_string(index=False))
    f.write("\n")
print(f"\nFit summary → {summary_path}")

# fit range for overlays
n_fit_256 = np.logspace(np.log10(600), np.log10(32000), 200)
n_fit_512 = np.logspace(np.log10(600), np.log10(32000), 200)

# ══════════════════════════════════════════════════════════════════════════
# Fig 4 — combined log-log mean DWD vs n_sweeps for both L
# ══════════════════════════════════════════════════════════════════════════
fig4, ax4 = plt.subplots(figsize=(7, 5))

n_fit = np.logspace(np.log10(600), np.log10(32000), 200)

for L in LS:
    sub = agg[agg["L"] == L].sort_values("n_sweeps")
    n   = sub["n_sweeps"].values.astype(float)
    d   = sub["mean_dwd"].values
    err = sub["se_dwd"].values
    nz  = d > 0

    # data: filled = non-zero mean, hollow = zero mean
    if nz.any():
        ax4.errorbar(
            n[nz], d[nz], yerr=err[nz],
            fmt=MARKERS[L], color=PALETTE[L], ms=6, lw=1.2,
            label=f"L={L}", zorder=3,
        )
    if (~nz).any():
        ax4.plot(
            n[~nz], np.full((~nz).sum(), 3e-6),
            MARKERS[L], color=PALETTE[L], ms=6,
            mfc="none", mew=1.5, zorder=3,
        )

    # OLS overlay (censored fit)
    ec, ic, rc, nc_pts = fit_censored[L]
    if not np.isnan(ec):
        y_fit = np.exp(ic) * n_fit**ec
        ax4.plot(
            n_fit, y_fit, "--", color=PALETTE[L], lw=1.0, alpha=0.7,
            label=f"  fit β={ec:.3f} R²={rc:.2f} (n_pts={nc_pts})",
        )

# KZM theory line anchored at L=512 smallest-n point
sub512 = agg[(agg["L"] == 512)].sort_values("n_sweeps")
nz512 = sub512["mean_dwd"].values > 0
if nz512.any():
    anchor_n = sub512["n_sweeps"].values[nz512][0]
    anchor_d = sub512["mean_dwd"].values[nz512][0]
    y_kzm    = anchor_d * (n_fit / anchor_n) ** (-1 / 3)
    ax4.plot(n_fit, y_kzm, "k:", lw=1.5, label="KZM theory β=−1/3")

ax4.set_xscale("log")
ax4.set_yscale("log")
ax4.set_xlabel("$n_{\\mathrm{sweeps}}$ (quench duration)", fontsize=12)
ax4.set_ylabel("Mean domain-wall density $\\langle \\rho_{\\mathrm{DW}} \\rangle$", fontsize=12)
ax4.set_title(
    "Exp 108 — KZM Scaling: Single-Wall Regime\n"
    "$L\\in\\{256,512\\}$, $N=200$ reps, $n\\in[800, 25600]$",
    fontsize=11,
)
ax4.legend(fontsize=8, ncol=2, loc="lower left")
ax4.grid(True, which="both", ls=":", alpha=0.4)
ax4.set_ylim(bottom=1e-6)

fig4.tight_layout()
for ext in ("pdf", "png"):
    p = OUT / f"108_fig4_loglog_dwd.{ext}"
    fig4.savefig(p, dpi=150)
    print(f"Saved {p}")
plt.close(fig4)

# ══════════════════════════════════════════════════════════════════════════
# Fig 5 — defect probability vs n_sweeps
# ══════════════════════════════════════════════════════════════════════════
fig5, ax5 = plt.subplots(figsize=(7, 4.5))

for L in LS:
    sub = agg[agg["L"] == L].sort_values("n_sweeps")
    n   = sub["n_sweeps"].values.astype(float)
    p   = sub["defect_prob"].values

    ax5.plot(
        n, p,
        marker=MARKERS[L], color=PALETTE[L], lw=1.5,
        ms=6, label=f"L={L}",
    )

ax5.axhline(0.5, color="grey", ls=":", lw=1.0, label="50% threshold")
ax5.set_xscale("log")
ax5.set_xlabel("$n_{\\mathrm{sweeps}}$", fontsize=12)
ax5.set_ylabel("Defect probability $P(\\rho_{\\mathrm{DW}}>0)$", fontsize=12)
ax5.set_title("Exp 108 — Fraction of runs with $\\geq 1$ domain wall", fontsize=11)
ax5.set_ylim(-0.02, 1.05)
ax5.legend(fontsize=9)
ax5.grid(True, which="both", ls=":", alpha=0.4)

fig5.tight_layout()
for ext in ("pdf", "png"):
    p = OUT / f"108_fig5_defect_prob.{ext}"
    fig5.savefig(p, dpi=150)
    print(f"Saved {p}")
plt.close(fig5)

# ══════════════════════════════════════════════════════════════════════════
# Fig 6 — per-L zero-censoring corrected fits (1×2 panels)
# ══════════════════════════════════════════════════════════════════════════
fig6, axes = plt.subplots(1, 2, figsize=(11, 5), sharex=True, sharey=True)

for idx, L in enumerate(LS):
    ax = axes[idx]
    sub = agg[agg["L"] == L].sort_values("n_sweeps")
    n   = sub["n_sweeps"].values.astype(float)
    d   = sub["mean_dwd"].values
    err = sub["se_dwd"].values
    nz  = d > 0
    mask_cens = sub["n_nonzero"].values >= MIN_NONZERO

    # data
    ax.errorbar(n[nz], d[nz], yerr=err[nz], fmt="o", color=PALETTE[L],
                ms=5, lw=1, label="data (mean>0)", zorder=3)
    for ni in n[~nz]:
        ax.annotate("", xy=(ni, 2e-6), xytext=(ni, 5e-6),
                    arrowprops=dict(arrowstyle="->", color="grey", lw=0.8))

    # censored fit
    ec, ic, rc, nc_pts = fit_censored[L]
    if not np.isnan(ec):
        y_fit = np.exp(ic) * n_fit**ec
        ax.plot(n_fit, y_fit, "--", color=PALETTE[L], lw=1.2,
                label=f"fit β={ec:.3f} R²={rc:.2f}")

    # KZM theory
    if nz.any():
        anchor_n = n[nz][0]
        anchor_d = d[nz][0]
        y_kzm = anchor_d * (n_fit / anchor_n) ** (-1 / 3)
        ax.plot(n_fit, y_kzm, "k:", lw=1.2, label="KZM −1/3")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title(f"L = {L}", fontsize=12, color=PALETTE[L])
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", ls=":", alpha=0.35)
    ax.set_ylim(bottom=1e-6)
    ax.set_xlabel("$n_{\\mathrm{sweeps}}$", fontsize=11)
    if idx == 0:
        ax.set_ylabel("Mean DWD", fontsize=11)

fig6.suptitle(
    "Exp 108 — Zero-censoring corrected KZM fits per system size",
    fontsize=12,
)
fig6.tight_layout()
for ext in ("pdf", "png"):
    p = OUT / f"108_fig6_censored_fit.{ext}"
    fig6.savefig(p, dpi=150)
    print(f"Saved {p}")
plt.close(fig6)

# ── throughput estimate ────────────────────────────────────────────────────
# From timing data: total time / total spin flips
# Total spin flips = sum over all runs of L^2 * n_sweeps * 2 (checkerboard)
total_flips = 0
for _, row in df.iterrows():
    L = int(row["L"])
    n = int(row["n_sweeps"])
    total_flips += L * L * n * 2  # factor 2 for checkerboard sublattice steps

# Read timing from CSV if available, else note unavailable
print(f"\nTotal spin flips: {total_flips:.3e}")
print("(Throughput requires total wall-clock time from binary output)")

print("\nAll figures written.")
print(f"Summary: {summary_path}")
