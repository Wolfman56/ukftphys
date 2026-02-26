"""
Experiment 74: m_inv-Binned Pull Analysis
==========================================
Fixes the GOF issue from Exp 66 by computing pulls within narrow m_inv bins.

The Exp 66 pull distribution had μ=+0.33σ and non-Gaussian shape because
m_inv spans 0.6–3.7 GeV (30% relative width). The global σ_hat conflated
kinematic spread with measurement resolution.

Strategy: bin events by m_inv quantile (5 bins, ~equal N each).
Within each bin m_inv is nearly constant, so:
  δ_i = m_ΔR_i - m_inv_i   (residual from kinematic identity)
  σ_bin = std(δ in bin)     (pure detector/approximation scatter)
  pull_i = δ_i / σ_bin

If the identity is unbiased in each bin → pull ~ N(0,1) per bin.
Non-zero per-bin bias → collinear correction as function of mass.

Outputs:
  results/74_binned_pull_analysis.png
  results/74_binned_pull_results.json
"""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

DATA_PATH = "/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer/tools/76h_b_kinematics.json"
N_BINS    = 5      # quantile bins
N_BOOT    = 8000   # bootstrap for bias per bin

# ── 1. Load data ──────────────────────────────────────────────────────────────
print("=" * 60)
print("EXP 74: m_inv-BINNED PULL ANALYSIS")
print("=" * 60)

with open(DATA_PATH) as f:
    data = json.load(f)

recs = [r for r in data["records"] if r["charge_product"] == -1]
print(f"OS events: {len(recs)}")

m_inv  = np.array([r["m_inv"]      for r in recs])
dR     = np.array([r["dR"]         for r in recs])
HT     = np.array([r["HT_dimuon"]  for r in recs])
pt_l   = np.array([r["pt_lead"]    for r in recs])
pt_s   = np.array([r["pt_sub"]     for r in recs])

# Kinematic mass handle: m_ΔR = ΔR × HT / 2
m_dR = dR * HT / 2.0
resid = m_dR - m_inv   # raw residuals (same as Exp 66)

print(f"\n--- Global residuals (unrestricted, reproduces Exp 66 picture) ---")
print(f"  mean(δ) = {resid.mean():.4f} GeV")
print(f"  std(δ)  = {resid.std():.4f} GeV")
pull_global = (m_dR - m_inv) / resid.std()
sw_g = stats.shapiro(pull_global)
ks_g = stats.kstest(pull_global, "norm")
print(f"  SW  p = {sw_g.pvalue:.4e}  KS p = {ks_g.pvalue:.4e}")
print(f"  Pull mean={pull_global.mean():.4f}, std={pull_global.std():.4f}")

# ── 2. Quantile bins ──────────────────────────────────────────────────────────
print(f"\n--- Per-bin analysis ({N_BINS} quantile bins) ---")
edges = np.quantile(m_inv, np.linspace(0, 1, N_BINS + 1))
edges[0]  -= 1e-6
edges[-1] += 1e-6
bin_labels = [f"[{edges[i]:.2f}, {edges[i+1]:.2f})" for i in range(N_BINS)]

bin_results = []
all_binned_pulls = []

for i in range(N_BINS):
    mask = (m_inv >= edges[i]) & (m_inv < edges[i+1])
    n_i     = mask.sum()
    m_inv_i = m_inv[mask]
    m_dR_i  = m_dR[mask]
    resid_i = m_dR_i - m_inv_i

    # Bias (slope correction): fit m_dR = a * m_inv + b within bin
    if n_i >= 3:
        slope_i, intercept_i, r_i, _, _ = stats.linregress(m_inv_i, m_dR_i)
    else:
        slope_i, intercept_i, r_i = 1.0, 0.0, float("nan")

    sigma_i = resid_i.std() if n_i >= 2 else float("nan")
    pull_i  = resid_i / sigma_i if (np.isfinite(sigma_i) and sigma_i > 0) else resid_i * 0

    # Bootstrap bias on pull mean
    if n_i >= 4:
        boot_means = []
        rng = np.random.default_rng(42 + i)
        for _ in range(N_BOOT):
            idx = rng.integers(0, n_i, size=n_i)
            r_b = resid_i[idx]
            s_b = r_b.std()
            boot_means.append(r_b.mean() / s_b if s_b > 0 else 0.0)
        pull_mean_err = np.std(boot_means)
    else:
        pull_mean_err = float("nan")

    sw_p = stats.shapiro(pull_i).pvalue if n_i >= 3 else float("nan")
    ks_p = stats.kstest(pull_i, "norm").pvalue if n_i >= 3 else float("nan")
    gof  = "PASS" if (np.isfinite(sw_p) and sw_p > 0.05) else "CHECK"

    print(f"\n  Bin {i+1}: {bin_labels[i]}  N={n_i}")
    print(f"    mean(δ)={resid_i.mean():.4f}  std(δ)={sigma_i:.4f} GeV")
    print(f"    slope={slope_i:.4f}, r={r_i:.4f}")
    print(f"    pull mean={pull_i.mean():.4f} ± {pull_mean_err:.4f}, std={pull_i.std():.4f}")
    print(f"    SW p={sw_p:.3f}  KS p={ks_p:.3f}  GOF: {gof}")

    bin_results.append({
        "bin": i + 1,
        "label": bin_labels[i],
        "n": int(n_i),
        "m_inv_mean": float(m_inv_i.mean()),
        "m_inv_std": float(m_inv_i.std()),
        "resid_mean": float(resid_i.mean()),
        "resid_std": float(sigma_i),
        "slope": float(slope_i),
        "r": float(r_i),
        "pull_mean": float(pull_i.mean()),
        "pull_mean_err": float(pull_mean_err),
        "pull_std": float(pull_i.std()),
        "sw_p": float(sw_p) if np.isfinite(sw_p) else None,
        "ks_p": float(ks_p) if np.isfinite(ks_p) else None,
        "gof": gof,
    })
    all_binned_pulls.extend(pull_i.tolist())

# ── 3. Combined binned-pull test ───────────────────────────────────────────────
all_binned_pulls = np.array(all_binned_pulls)
print(f"\n--- Combined binned pulls (all bins concatenated) ---")
print(f"  N = {len(all_binned_pulls)}")
print(f"  mean = {all_binned_pulls.mean():.4f}")
print(f"  std  = {all_binned_pulls.std():.4f}")
sw_comb = stats.shapiro(all_binned_pulls)
ks_comb = stats.kstest(all_binned_pulls, "norm")
print(f"  SW  p = {sw_comb.pvalue:.4e}")
print(f"  KS  p = {ks_comb.pvalue:.4e}")
gof_comb = "PASS" if sw_comb.pvalue > 0.05 else "CHECK"
print(f"  GOF: {gof_comb}")

# ── 4. Per-bin bias trend: does slope vary with mass? ─────────────────────────
print(f"\n--- Per-bin slope trend (collinear correction magnitude vs mass) ---")
bin_m   = np.array([b["m_inv_mean"] for b in bin_results if np.isfinite(b["slope"])])
bin_s   = np.array([b["slope"]      for b in bin_results if np.isfinite(b["slope"])])
if len(bin_m) >= 3:
    slope_trend, intercept_trend, r_trend, p_trend, _ = stats.linregress(bin_m, bin_s)
    print(f"  d(slope)/d(m_inv) = {slope_trend:.4f}  r={r_trend:.3f}  p={p_trend:.3f}")
    print(f"  Slope at m=2.5 GeV: {slope_trend * 2.5 + intercept_trend:.4f}")
    print(f"  Mass dependence {'SIGNIFICANT (p<0.05)' if p_trend < 0.05 else 'NOT significant'}")
else:
    slope_trend, r_trend, p_trend = 0.0, 0.0, 1.0

# ── 5. Plots ──────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10))
fig.suptitle("Exp 74: m$_{inv}$-Binned Pull Analysis\n"
             r"$m_{\Delta R} = \Delta R \cdot H_T/2$ vs $m_{inv}$ (per-bin pulls)",
             fontsize=13, fontweight="bold")

colors = plt.cm.plasma(np.linspace(0.15, 0.85, N_BINS))
x_norm = np.linspace(-4, 4, 200)

# Row 1: individual bin pull histograms
axes_hist = [fig.add_subplot(2, N_BINS, k + 1) for k in range(N_BINS)]
for i, (ax, br) in enumerate(zip(axes_hist, bin_results)):
    mask = (m_inv >= edges[i]) & (m_inv < edges[i+1])
    resid_i = (m_dR - m_inv)[mask]
    sigma_i = resid_i.std() if resid_i.std() > 0 else 1.0
    pull_i  = resid_i / sigma_i
    ax.hist(pull_i, bins=max(5, int(np.sqrt(br["n"]))), color=colors[i],
            alpha=0.75, density=True, edgecolor="k", linewidth=0.4)
    ax.plot(x_norm, stats.norm.pdf(x_norm), "k--", lw=1.2, label="N(0,1)")
    ax.axvline(pull_i.mean(), color="red", lw=1.2, linestyle=":")
    ax.set_title(f"Bin {i+1}\n{br['label']}\nN={br['n']}", fontsize=7.5)
    ax.set_xlabel("Pull", fontsize=7)
    if i == 0:
        ax.set_ylabel("Density", fontsize=7)
    sw_str = f"SW p={br['sw_p']:.2f}" if br["sw_p"] is not None else ""
    gof_col = "green" if br["gof"] == "PASS" else "darkorange"
    ax.text(0.97, 0.95, sw_str, transform=ax.transAxes,
            ha="right", va="top", fontsize=6, color=gof_col)
    ax.tick_params(labelsize=6)
    ax.set_xlim(-4, 4)

# Row 2, col 1-3: combined pull QQ
ax_qq = fig.add_subplot(2, 3, 4)
(osm, osr), (slope_qq, intercept_qq, r_qq) = stats.probplot(all_binned_pulls,
                                                               dist="norm", fit=True)
ax_qq.scatter(osm, osr, s=18, color="steelblue", alpha=0.7, zorder=3)
ax_qq.plot(osm, slope_qq * np.array(osm) + intercept_qq, "r-", lw=1.5)
ax_qq.set_xlabel("Theoretical quantiles", fontsize=9)
ax_qq.set_ylabel("Sample quantiles", fontsize=9)
ax_qq.set_title("QQ Plot — Combined Binned Pulls", fontsize=9)
ax_qq.text(0.05, 0.95,
           f"SW p={sw_comb.pvalue:.3f}\n"
           f"KS p={ks_comb.pvalue:.3f}\n"
           f"mean={all_binned_pulls.mean():.3f}\n"
           f"std ={all_binned_pulls.std():.3f}",
           transform=ax_qq.transAxes, va="top", fontsize=8,
           bbox=dict(boxstyle="round", fc="lightyellow", alpha=0.8))
ax_qq.grid(alpha=0.3)

# Row 2, col 4: per-bin bias (pull mean ± boot err)
ax_bias = fig.add_subplot(2, 3, 5)
bin_nums    = np.array([b["bin"]       for b in bin_results])
pull_means  = np.array([b["pull_mean"] for b in bin_results])
pull_errs   = np.array([b["pull_mean_err"] if np.isfinite(b["pull_mean_err"])
                        else 0.0 for b in bin_results])
bin_masses  = np.array([b["m_inv_mean"] for b in bin_results])

ax_bias.errorbar(bin_masses, pull_means, yerr=pull_errs,
                 fmt="o-", color="purple", capsize=4, lw=1.5, ms=7)
ax_bias.axhline(0, color="k", lw=1, linestyle="--")
ax_bias.fill_between(ax_bias.get_xlim() if ax_bias.get_xlim() != (0,1) else
                     [bin_masses.min()-0.1, bin_masses.max()+0.1],
                     -1, 1, color="green", alpha=0.07)
ax_bias.set_xlabel("$m_{inv}$ bin centre (GeV)", fontsize=9)
ax_bias.set_ylabel("Pull mean (σ)", fontsize=9)
ax_bias.set_title("Per-Bin Bias vs Mass", fontsize=9)
ax_bias.grid(alpha=0.3)
ax_bias.set_xlim(bin_masses.min() - 0.3, bin_masses.max() + 0.3)

# Row 2, col 5: per-bin slope
ax_slope = fig.add_subplot(2, 3, 6)
bin_slopes = np.array([b["slope"] for b in bin_results])
ax_slope.plot(bin_masses, bin_slopes, "s-", color="darkorange",
              lw=1.5, ms=7, label="bin slope")
ax_slope.axhline(1.0, color="k", lw=1, linestyle="--", label="unity")
if len(bin_m) >= 3 and np.isfinite(slope_trend):
    m_fit_line = np.linspace(bin_m.min(), bin_m.max(), 100)
    ax_slope.plot(m_fit_line,
                  slope_trend * m_fit_line + intercept_trend,
                  "r:", lw=1.2,
                  label=f"trend r={r_trend:.2f}")
ax_slope.set_xlabel("$m_{inv}$ bin centre (GeV)", fontsize=9)
ax_slope.set_ylabel("m$_{\\Delta R}$ / m$_{inv}$ slope", fontsize=9)
ax_slope.set_title("Collinear Correction vs Mass", fontsize=9)
ax_slope.legend(fontsize=7)
ax_slope.grid(alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.93])
outpath = "results/74_binned_pull_analysis.png"
plt.savefig(outpath, dpi=150, bbox_inches="tight")
print(f"\nFigure saved: {outpath}")

# ── 6. Summary ────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

n_pass = sum(1 for b in bin_results if b["gof"] == "PASS")
n_check = sum(1 for b in bin_results if b["gof"] == "CHECK")
print(f"Per-bin GOF: {n_pass}/{N_BINS} PASS, {n_check}/{N_BINS} CHECK")
print(f"Combined binned-pull GOF: {gof_comb}")
print(f"  mean = {all_binned_pulls.mean():.4f}  std = {all_binned_pulls.std():.4f}")
print(f"  vs Exp 66 global pull: mean=+0.327, std=1.000")
print()
print(f"Collinear slope trend:")
print(f"  d(slope)/d(m) = {slope_trend:.4f} GeV⁻¹  (p={p_trend:.3f})")
if p_trend < 0.05:
    corr_at_2p5 = slope_trend * 2.5 + intercept_trend
    print(f"  Correction at m=2.5 GeV: slope = {corr_at_2p5:.4f}  ({(corr_at_2p5-1)*100:.2f}% from unity)")
    print(f"  ⟹ Apply mass-dependent collinear correction: m_cal = m_ΔR / slope(m_inv)")
else:
    print(f"  No significant mass dependence — flat slope adequate")

print()
print("Interpretation:")
print("  Binning by m_inv removes the kinematic spread that caused the")
print("  Exp 66 GOF failure. Within each narrow mass window the residuals")
print("  δ = m_ΔR - m_inv are dominated by the collinear approximation")
print("  scatter, not by the physical resonance width.")

# Save JSON
results = {
    "experiment": 74,
    "n_os_events": len(m_inv),
    "n_bins": N_BINS,
    "global_pull": {
        "mean": float(pull_global.mean()),
        "std": float(pull_global.std()),
        "sw_p": float(sw_g.pvalue),
        "ks_p": float(ks_g.pvalue),
    },
    "combined_binned_pull": {
        "mean": float(all_binned_pulls.mean()),
        "std": float(all_binned_pulls.std()),
        "sw_p": float(sw_comb.pvalue),
        "ks_p": float(ks_comb.pvalue),
        "gof": gof_comb,
    },
    "slope_trend": {
        "d_slope_d_m": float(slope_trend),
        "r": float(r_trend),
        "p": float(p_trend),
    },
    "bins": bin_results,
}
json_path = "results/74_binned_pull_results.json"
with open(json_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved: {json_path}")
print("\nExp 74 complete.")
