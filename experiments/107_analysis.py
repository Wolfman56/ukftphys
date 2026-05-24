"""
Exp 107 — KZM Domain-Wall Density: Publication Plots
======================================================
Reads 107_exp107_raw.csv and produces:
  Fig 1 — log-log mean DWD vs n_sweeps per L  (+ OLS power-law overlays)
  Fig 2 — defect-probability (fraction non-zero reps) vs n_sweeps per L
  Fig 3 — survival-corrected exponent: OLS fit restricted to points where
           mean_dwd > 0 (zero-censoring correction, Option 2)

Outputs:
  107_fig1_loglog_dwd.pdf / .png
  107_fig2_defect_prob.pdf / .png
  107_fig3_censored_fit.pdf / .png
  107_fit_summary.txt
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
RAW  = HERE / "107_exp107_raw.csv"
OUT  = HERE  # write outputs alongside script

# ── load & aggregate ───────────────────────────────────────────────────────
df = pd.read_csv(RAW)

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
PALETTE = {64: "#1f77b4", 128: "#ff7f0e", 256: "#2ca02c", 512: "#d62728"}
MARKERS = {64: "o",       128: "s",        256: "^",       512: "D"}

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

# ── write fit summary ──────────────────────────────────────────────────────
summary_path = OUT / "107_fit_summary.txt"
with open(summary_path, "w") as f:
    f.write("Exp 107 — KZM Power-Law Fit Summary\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"{'L':>6}  {'expo(all)':>10}  {'R²(all)':>8}  "
            f"{'expo(≥3nz)':>11}  {'R²(≥3nz)':>9}  {'n_pts':>6}\n")
    f.write("-" * 60 + "\n")
    for L in LS:
        ea, _, ra, na = fit_all[L]
        ec, _, rc, nc = fit_censored[L]
        f.write(f"{L:>6}  {ea:>10.4f}  {ra:>8.4f}  "
                f"{ec:>11.4f}  {rc:>9.4f}  {nc:>6}\n")
    f.write("\nTheory (2D model-A AF Ising, KZM): exponent = -1/3 ≈ -0.3333\n")
    f.write(f"Min nonzero threshold: {MIN_NONZERO} reps\n")
print(f"Fit summary → {summary_path}")

# ══════════════════════════════════════════════════════════════════════════
# Fig 1 — log-log mean DWD vs n_sweeps
# ══════════════════════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(7, 5))

n_fit = np.logspace(np.log10(200), np.log10(204800), 200)

for L in LS:
    sub = agg[agg["L"] == L].sort_values("n_sweeps")
    n   = sub["n_sweeps"].values.astype(float)
    d   = sub["mean_dwd"].values
    err = sub["se_dwd"].values
    nz  = d > 0

    # data points (filled = non-zero mean, hollow = zero mean)
    ax1.errorbar(
        n[nz], d[nz], yerr=err[nz],
        fmt=MARKERS[L], color=PALETTE[L], ms=6, lw=1.2,
        label=f"L={L}", zorder=3,
    )
    if (~nz).any():
        ax1.plot(
            n[~nz], np.full((~nz).sum(), 3e-5),
            MARKERS[L], color=PALETTE[L], ms=6,
            mfc="none", mew=1.5, zorder=3,
        )

    # OLS overlay (censored fit)
    ec, ic, rc, nc_pts = fit_censored[L]
    if not np.isnan(ec):
        y_fit = np.exp(ic) * n_fit**ec
        ax1.plot(
            n_fit, y_fit, "--", color=PALETTE[L], lw=1.0, alpha=0.7,
            label=f"  fit β={ec:.3f} R²={rc:.2f} (n={nc_pts})",
        )

# KZM theory line anchored at L=512 n=200 point
sub512 = agg[(agg["L"] == 512) & (agg["n_sweeps"] == 200)]
if not sub512.empty:
    anchor = sub512["mean_dwd"].values[0]
    y_kzm  = anchor * (n_fit / 200) ** (-1 / 3)
    ax1.plot(n_fit, y_kzm, "k:", lw=1.5, label="KZM theory β=−1/3")

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlabel("$n_{\\mathrm{sweeps}}$ (quench duration)", fontsize=12)
ax1.set_ylabel("Mean domain-wall density $\\langle \\rho_{\\mathrm{DW}} \\rangle$", fontsize=12)
ax1.set_title("Exp 107 — KZM Scaling: 2D AF Ising GPU (Checkerboard Metropolis)", fontsize=11)
ax1.legend(fontsize=8, ncol=2, loc="lower left")
ax1.grid(True, which="both", ls=":", alpha=0.4)
ax1.set_ylim(bottom=2e-5)

fig1.tight_layout()
for ext in ("pdf", "png"):
    p = OUT / f"107_fig1_loglog_dwd.{ext}"
    fig1.savefig(p, dpi=150)
    print(f"Saved {p}")
plt.close(fig1)

# ══════════════════════════════════════════════════════════════════════════
# Fig 2 — defect probability vs n_sweeps
# ══════════════════════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(7, 4.5))

for L in LS:
    sub = agg[agg["L"] == L].sort_values("n_sweeps")
    n   = sub["n_sweeps"].values.astype(float)
    p   = sub["defect_prob"].values

    ax2.plot(
        n, p,
        marker=MARKERS[L], color=PALETTE[L], lw=1.5,
        ms=6, label=f"L={L}",
    )

ax2.axhline(0.5, color="grey", ls=":", lw=1.0, label="50% threshold")
ax2.set_xscale("log")
ax2.set_xlabel("$n_{\\mathrm{sweeps}}$", fontsize=12)
ax2.set_ylabel("Defect probability $P(\\rho_{\\mathrm{DW}}>0)$", fontsize=12)
ax2.set_title("Exp 107 — Fraction of runs with $\\geq 1$ domain wall", fontsize=11)
ax2.set_ylim(-0.02, 1.05)
ax2.legend(fontsize=9)
ax2.grid(True, which="both", ls=":", alpha=0.4)

fig2.tight_layout()
for ext in ("pdf", "png"):
    p = OUT / f"107_fig2_defect_prob.{ext}"
    fig2.savefig(p, dpi=150)
    print(f"Saved {p}")
plt.close(fig2)

# ══════════════════════════════════════════════════════════════════════════
# Fig 3 — censored-fit comparison: full vs ≥3-nonzero fits, per L
# ══════════════════════════════════════════════════════════════════════════
fig3, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=True, sharey=True)
axes = axes.flatten()

for idx, L in enumerate(LS):
    ax = axes[idx]
    sub = agg[agg["L"] == L].sort_values("n_sweeps")
    n   = sub["n_sweeps"].values.astype(float)
    d   = sub["mean_dwd"].values
    err = sub["se_dwd"].values
    nz  = d > 0
    mask_cens = sub["n_nonzero"].values >= MIN_NONZERO

    # all mean>0 points
    ax.errorbar(n[nz], d[nz], yerr=err[nz], fmt="o", color=PALETTE[L],
                ms=5, lw=1, label="data (mean>0)", zorder=3)
    # zero-mean points (shown as lower-limit arrows)
    for ni in n[~nz]:
        ax.annotate("", xy=(ni, 2e-5), xytext=(ni, 4e-5),
                    arrowprops=dict(arrowstyle="->", color="grey", lw=0.8))

    # censored fit (n_nonzero >= 3)
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
    ax.set_title(f"L = {L}", fontsize=11)
    ax.legend(fontsize=7.5, loc="lower left")
    ax.grid(True, which="both", ls=":", alpha=0.35)
    ax.set_ylim(bottom=1e-5)
    if idx >= 2:
        ax.set_xlabel("$n_{\\mathrm{sweeps}}$", fontsize=10)
    if idx % 2 == 0:
        ax.set_ylabel("Mean DWD", fontsize=10)

fig3.suptitle("Exp 107 — Zero-censoring corrected fits per system size", fontsize=12)
fig3.tight_layout()
for ext in ("pdf", "png"):
    p = OUT / f"107_fig3_censored_fit.{ext}"
    fig3.savefig(p, dpi=150)
    print(f"Saved {p}")
plt.close(fig3)

print("\nAll figures written. Summary:")
print(open(summary_path).read())
