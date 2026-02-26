"""
Experiment 75: Calibration Publication Figure
==============================================
Produces the four-panel money figure for the detector calibration paper section,
tying together Exps 64, 65, and 66 into a single publication-ready plot.

The kinematic identity  ΔR · H_T/2 = M_{A'}  (exact in collinear/boosted limit)
provides three independent mass handles from CMS Run 2012C OS dimuon data:

  m_inv  — standard 4-vector invariant mass (tracker monopoly)
  m_ΔR   — angular × scalar-pT (tracker-independent)
  M_fit  — global boost consistency fit

These agree at 0.06σ and offer a 0.61σ/% lever arm on pT + angular scale.

Panel layout:
  A (top-left)  : ΔR × HT/2 vs m_inv scatter — the kinematic identity
  B (top-right) : pT-binned ΔR power law with QM hyperbola family (Exp 65)
  C (bottom-left): Cross-calibration: m_ΔR vs m_inv with slope annotation
  D (bottom-right): Systematic injection scan — bias lever arm (Exp 66)

Outputs:
  results/75_calibration_publication_figure.png
  results/75_paper_numbers.json
"""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
from scipy.optimize import minimize_scalar
import warnings
warnings.filterwarnings("ignore")

DATA_PATH = "/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer/tools/76h_b_kinematics.json"
N_BOOT    = 10_000
RNG       = np.random.default_rng(42)

# ── 1. Load & filter ──────────────────────────────────────────────────────────
print("=" * 60)
print("EXP 75: CALIBRATION PUBLICATION FIGURE")
print("=" * 60)

with open(DATA_PATH) as f:
    raw = json.load(f)

recs   = [r for r in raw["records"] if r["charge_product"] == -1]
m_inv  = np.array([r["m_inv"]      for r in recs])
dR     = np.array([r["dR"]         for r in recs])
HT     = np.array([r["HT_dimuon"]  for r in recs])
pt_l   = np.array([r["pt_lead"]    for r in recs])
pt_s   = np.array([r["pt_sub"]     for r in recs])
N      = len(m_inv)
print(f"OS events: {N}")

# Derived quantities
m_dR   = dR * HT / 2.0
pT_avg = (pt_l + pt_s) / 2.0

# M_fit from Exp 65: minimise Σ(ΔR_i - 2M/HT_i)²
res = minimize_scalar(
    lambda M: np.sum((dR - 2.0 * M / HT) ** 2),
    bounds=(0.5, 5.0), method="bounded"
)
M_fit = res.x
print(f"M_fit = {M_fit:.4f} GeV")

# Bootstrap uncertainties
boots = {"m_inv": [], "m_dR": [], "M_fit": []}
for _ in range(N_BOOT):
    idx = RNG.integers(0, N, size=N)
    boots["m_inv"].append(m_inv[idx].mean())
    boots["m_dR"].append((dR[idx] * HT[idx] / 2.0).mean())
    res_b = minimize_scalar(
        lambda M: np.sum((dR[idx] - 2.0 * M / HT[idx]) ** 2),
        bounds=(0.5, 5.0), method="bounded"
    )
    boots["M_fit"].append(res_b.x)

unc = {k: np.std(v) for k, v in boots.items()}

# Correlation coefficient (Panel A)
r_val, p_val = stats.pearsonr(m_inv, m_dR)

# Cross-calibration slope (Panel C)
slope_cc, intercept_cc, r_cc, _, _ = stats.linregress(m_inv, m_dR)

# Systematic sensitivity (Panel D)
deltas  = [-5, -2, 0, +2, +5]
s_sigma = []

def pull_metric(m_dR_mod, m_inv_ref):
    resid = m_dR_mod - m_inv_ref
    sigma = resid.std()
    return resid.mean() / sigma if sigma > 0 else 0.0

pull0 = pull_metric(m_dR, m_inv)
for d in deltas:
    m_dR_pt  = (dR * HT * (1 + d/100) / 2.0)
    s_sigma.append(pull_metric(m_dR_pt, m_inv) - pull0)

sensitivity_pt = (s_sigma[-1] - s_sigma[0]) / (deltas[-1] - deltas[0])

# pT bins for Panel B (power law)
n_pt_bins = 5
pt_edges  = np.quantile(pT_avg, np.linspace(0, 1, n_pt_bins + 1))
pt_edges[0] -= 1e-6; pt_edges[-1] += 1e-6
pt_centres, dR_means, dR_errs = [], [], []
for j in range(n_pt_bins):
    mask = (pT_avg >= pt_edges[j]) & (pT_avg < pt_edges[j+1])
    if mask.sum() >= 3:
        pt_centres.append(pT_avg[mask].mean())
        dR_means.append(dR[mask].mean())
        dR_errs.append(dR[mask].std() / np.sqrt(mask.sum()))

pt_centres = np.array(pt_centres)
dR_means   = np.array(dR_means)
dR_errs    = np.array(dR_errs)

# pT power law fit: ΔR = A × pT^β
log_pt = np.log(pt_centres)
log_dR = np.log(dR_means)
beta_fit, log_A, r_pl, _, _ = stats.linregress(log_pt, log_dR)
A_fit = np.exp(log_A)

# QM hyperbola family: ΔR = 2 M / HT
M_ref    = M_fit
kx_vals  = [5, 8, 12, 15, 18]
HT_ref   = HT.mean()
sigma_v  = M_ref / HT_ref  # fixed
pt_line  = np.linspace(pt_centres.min() * 0.7, pt_centres.max() * 1.3, 200)

# ── 2. Print publication numbers ──────────────────────────────────────────────
print("\n--- Publication numbers ---")
print(f"  m_inv  = {m_inv.mean():.4f} ± {unc['m_inv']:.4f} GeV")
print(f"  m_ΔR   = {m_dR.mean():.4f} ± {unc['m_dR']:.4f} GeV")
print(f"  M_fit  = {M_fit:.4f} ± {unc['M_fit']:.4f} GeV")
tension = abs(m_dR.mean() - m_inv.mean()) / np.sqrt(unc["m_dR"]**2 + unc["m_inv"]**2)
print(f"  Tension m_inv vs m_ΔR: {tension:.2f}σ")
print(f"  r(m_ΔR, m_inv) = {r_val:.4f}  p = {p_val:.2e}")
print(f"  Cross-cal slope = {slope_cc:.6f}  offset = {intercept_cc:.4f} GeV")
print(f"  Slope deviation: {(slope_cc-1)*100:.3f}%")
print(f"  Systematic lever arm: {sensitivity_pt:.3f} σ per 1% bias")
print(f"  pT power law: β = {beta_fit:.3f}  (expect -1, collinear)")
print(f"  N events: {N}")
print(f"  CMS ΔR observed: 0.121  QM Born: 0.095  QM tuned: 0.093")

# ── 3. Build figure ───────────────────────────────────────────────────────────
fig = plt.figure(figsize=(13, 10))
gs  = gridspec.GridSpec(2, 2, hspace=0.38, wspace=0.32,
                        left=0.08, right=0.96, top=0.90, bottom=0.08)

# ─── Panel A: Kinematic identity scatter ──────────────────────────────────────
ax_A = fig.add_subplot(gs[0, 0])
ax_A.scatter(m_inv, m_dR, s=22, alpha=0.65, color="steelblue",
             edgecolors="k", linewidths=0.3, zorder=3, label="CMS OS events")
lim = [min(m_inv.min(), m_dR.min()) - 0.15, max(m_inv.max(), m_dR.max()) + 0.15]
ax_A.plot(lim, lim, "r--", lw=1.5, label="Unity (exact identity)")

# Linear fit line
x_fit = np.linspace(lim[0], lim[1], 200)
ax_A.plot(x_fit, slope_cc * x_fit + intercept_cc, "k-", lw=1.2, alpha=0.6,
          label=f"Fit: slope={slope_cc:.4f}")
ax_A.set_xlim(lim); ax_A.set_ylim(lim)
ax_A.set_xlabel(r"$m_{inv} = \sqrt{(p_{\mu^+}+p_{\mu^-})^2}$ [GeV]", fontsize=9)
ax_A.set_ylabel(r"$m_{\Delta R} = \Delta R \cdot H_T / 2$ [GeV]", fontsize=9)
ax_A.set_title(r"(A) Kinematic Identity: $m_{\Delta R}$ vs $m_{inv}$", fontsize=10, fontweight="bold")
ax_A.legend(fontsize=7.5)
ax_A.text(0.05, 0.92,
          f"r = {r_val:.4f}\np = {p_val:.1e}\nN = {N}",
          transform=ax_A.transAxes, va="top", fontsize=8,
          bbox=dict(boxstyle="round", fc="lightyellow", alpha=0.85))
ax_A.grid(alpha=0.25)
ax_A.set_aspect("equal")

# ─── Panel B: pT power law + QM hyperbola family ──────────────────────────────
ax_B = fig.add_subplot(gs[0, 1])
ax_B.errorbar(pt_centres, dR_means, yerr=dR_errs,
              fmt="o", color="darkblue", capsize=4, ms=6, lw=1.5, zorder=4,
              label="CMS binned ΔR")
ax_B.plot(pt_line, A_fit * pt_line ** beta_fit, "b--", lw=1.5,
          label=fr"Power law $\beta$={beta_fit:.2f}")

# QM hyperbola: ΔR = 2M / pT (collinear limit, pT ≈ HT/2)
qm_colors = plt.cm.Reds(np.linspace(0.35, 0.85, len(kx_vals)))
for kc, (kx, col) in enumerate(zip(kx_vals, qm_colors)):
    dR_qm = 2.0 * sigma_v * kx / pt_line
    ax_B.plot(pt_line, dR_qm, "-", color=col, lw=1.0, alpha=0.8,
              label=f"QM kx={kx}" if kc in [0, len(kx_vals)-1] else "_nolegend_")

ax_B.set_xlabel(r"$p_T^{\rm avg}$ [GeV]", fontsize=9)
ax_B.set_ylabel(r"$\langle \Delta R \rangle$", fontsize=9)
ax_B.set_title("(B) pT Power Law + QM Hyperbola Family", fontsize=10, fontweight="bold")
ax_B.legend(fontsize=6.5, loc="upper right")
ax_B.set_xlim(pt_line.min(), pt_line.max())
ax_B.grid(alpha=0.25)
ax_B.text(0.04, 0.12,
          fr"$\beta$ = {beta_fit:.3f}$\,$(expect $-1$, collinear)",
          transform=ax_B.transAxes, fontsize=7.5,
          bbox=dict(boxstyle="round", fc="lightyellow", alpha=0.85))

# ─── Panel C: Cross-calibration regression ────────────────────────────────────
ax_C = fig.add_subplot(gs[1, 0])
ax_C.scatter(m_inv, m_dR, s=22, alpha=0.55, color="purple",
             edgecolors="k", linewidths=0.3, zorder=3)
m_range = np.linspace(m_inv.min() - 0.1, m_inv.max() + 0.1, 200)
ax_C.plot(m_range, slope_cc * m_range + intercept_cc, "r-", lw=2.0,
          label=f"slope = {slope_cc:.4f}\noffset = {intercept_cc:+.4f} GeV")
ax_C.plot(m_range, m_range, "k--", lw=1, alpha=0.5, label="Unity")

# 1σ band from bootstrap
boot_m_dR = np.array(boots["m_dR"])
boot_m_inv = np.array(boots["m_inv"])
# compute bootstrap slope scatter
boot_slopes = []
for bi in range(min(500, N_BOOT)):
    idx = RNG.integers(0, N, size=N)
    sl, ic, _, _, _ = stats.linregress(m_inv[idx], m_dR[idx])
    boot_slopes.append(sl)
slope_err = np.std(boot_slopes)
ax_C.fill_between(m_range,
                  (slope_cc - slope_err) * m_range + intercept_cc,
                  (slope_cc + slope_err) * m_range + intercept_cc,
                  color="red", alpha=0.12, label=fr"$\pm1\sigma$ slope")

ax_C.set_xlabel(r"$m_{inv}$ [GeV]", fontsize=9)
ax_C.set_ylabel(r"$m_{\Delta R}$ [GeV]", fontsize=9)
ax_C.set_title("(C) Cross-Calibration Regression", fontsize=10, fontweight="bold")
ax_C.legend(fontsize=7.5)
ax_C.grid(alpha=0.25)
ax_C.text(0.05, 0.92,
          f"Slope from unity: {(slope_cc-1)*100:+.3f}%\n"
          f"Tension: {tension:.2f}σ",
          transform=ax_C.transAxes, va="top", fontsize=8,
          bbox=dict(boxstyle="round", fc="lightyellow", alpha=0.85))

# ─── Panel D: Systematic injection scan ───────────────────────────────────────
ax_D = fig.add_subplot(gs[1, 1])

# pT bias
s_pt = []
for d in deltas:
    m_mod = dR * HT * (1 + d/100) / 2.0
    s_pt.append(pull_metric(m_mod, m_inv))

# Angular bias
s_an = []
for d in deltas:
    m_mod = dR * (1 + d/100) * HT / 2.0
    s_an.append(pull_metric(m_mod, m_inv))

# Reset to zero at d=0
s_pt_rel = np.array(s_pt) - s_pt[2]
s_an_rel = np.array(s_an) - s_an[2]

ax_D.plot(deltas, s_pt_rel, "bo-", ms=7, lw=1.8, label="pT scale bias", zorder=4)
ax_D.plot(deltas, s_an_rel, "rs--", ms=7, lw=1.8, label="Angular (ΔR) bias", zorder=4)
ax_D.axhline(0, color="k", lw=0.8, linestyle=":")
ax_D.axhline(+1, color="gray", lw=0.7, linestyle="--", alpha=0.5)
ax_D.axhline(-1, color="gray", lw=0.7, linestyle="--", alpha=0.5)
ax_D.fill_between([-5.5, 5.5], -1, 1, color="green", alpha=0.06)
ax_D.set_xlim(-5.5, 5.5)
ax_D.set_xlabel("Injected bias δ (%)", fontsize=9)
ax_D.set_ylabel("Δ pull mean (σ)", fontsize=9)
ax_D.set_title("(D) Systematic Sensitivity", fontsize=10, fontweight="bold")
ax_D.legend(fontsize=8, loc="upper left")
ax_D.grid(alpha=0.25)

# Compute lever arm from linear fit
sl_pt, _, _, _, _ = stats.linregress(deltas, s_pt_rel)
sl_an, _, _, _, _ = stats.linregress(deltas, s_an_rel)
ax_D.text(0.97, 0.06,
          f"pT lever:     {sl_pt:+.3f} σ/%\n"
          f"Angular lever: {sl_an:+.3f} σ/%\n"
          f"(symmetry expected: m_ΔR = ΔR·HT/2)",
          transform=ax_D.transAxes, ha="right", va="bottom", fontsize=7.5,
          bbox=dict(boxstyle="round", fc="lightyellow", alpha=0.85))

# ─── Title & annotation ───────────────────────────────────────────────────────
fig.suptitle(
    r"In-Situ Mass Calibration via $\Delta R \cdot H_T/2 = M_{A'}$"
    "\nCMS Run 2012C OS Dimuon — 69 events",
    fontsize=12, fontweight="bold"
)

# Bottom citation note
fig.text(0.5, 0.005,
         f"Three mass handles: "
         fr"$m_{{inv}}$={m_inv.mean():.3f}±{unc['m_inv']:.3f} GeV  |  "
         fr"$m_{{\Delta R}}$={m_dR.mean():.3f}±{unc['m_dR']:.3f} GeV  |  "
         fr"$M_{{fit}}$={M_fit:.3f}±{unc['M_fit']:.3f} GeV  |  "
         f"Tension: {tension:.2f}σ",
         ha="center", fontsize=8, style="italic")

outpath = "results/75_calibration_publication_figure.png"
plt.savefig(outpath, dpi=180, bbox_inches="tight")
print(f"\nFigure saved: {outpath}")

# ── 4. LaTeX-ready numbers ────────────────────────────────────────────────────
print("\n--- LaTeX numbers for paper ---")
print(r"\newcommand{\mInvCMS}{" + f"{m_inv.mean():.3f} \\pm {unc['m_inv']:.3f}" + r"\,\text{GeV}}")
print(r"\newcommand{\mDRCMS}{"  + f"{m_dR.mean():.3f} \\pm {unc['m_dR']:.3f}" + r"\,\text{GeV}}")
print(r"\newcommand{\MFitCMS}{"  + f"{M_fit:.3f} \\pm {unc['M_fit']:.3f}" + r"\,\text{GeV}}")
print(r"\newcommand{\mDRCorr}{"  + f"{r_val:.4f}" + r"}")
print(r"\newcommand{\mDRSlope}{" + f"{slope_cc:.4f}" + r"}")
print(r"\newcommand{\mDRSlopeDevPct}{" + f"{(slope_cc-1)*100:.2f}" + r"\%}")
print(r"\newcommand{\mDRTension}{"+ f"{tension:.2f}" + r"\sigma}")
print(r"\newcommand{\sysLeverArmPT}{"  + f"{sl_pt:.3f}" + r"\,\sigma/\%}")
print(r"\newcommand{\sysLeverArmAng}{" + f"{sl_an:.3f}" + r"\,\sigma/\%}")
print(r"\newcommand{\pTpowerBeta}{" + f"{beta_fit:.3f}" + r"}")
print(r"\newcommand{\NeventsOS}{" + str(N) + r"}")

# ── 5. Save JSON ──────────────────────────────────────────────────────────────
paper_numbers = {
    "experiment": 75,
    "n_os_events": N,
    "mass_handles": {
        "m_inv":  {"mean": float(m_inv.mean()), "unc": float(unc["m_inv"])},
        "m_dR":   {"mean": float(m_dR.mean()),  "unc": float(unc["m_dR"])},
        "M_fit":  {"mean": float(M_fit),         "unc": float(unc["M_fit"])},
    },
    "tension_sigma": float(tension),
    "pearson_r": float(r_val),
    "pearson_p": float(p_val),
    "cross_cal_slope": float(slope_cc),
    "cross_cal_offset_GeV": float(intercept_cc),
    "slope_deviation_pct": float((slope_cc - 1) * 100),
    "sys_lever_pt":  float(sl_pt),
    "sys_lever_ang": float(sl_an),
    "pT_power_law_beta": float(beta_fit),
    "qm_sigma_v": float(sigma_v),
    "qm_M_fit_GeV": float(M_fit),
    "cms_dR_observed": 0.121,
    "qm_dR_born": 0.095,
    "qm_dR_tuned": 0.093,
}
json_path = "results/75_paper_numbers.json"
with open(json_path, "w") as f:
    json.dump(paper_numbers, f, indent=2)
print(f"\nNumbers saved: {json_path}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  r(m_ΔR, m_inv)  = {r_val:.4f}  (Exp 65: 0.9995)")
print(f"  Tension          = {tension:.2f}σ  (Exp 66: 0.06σ)")
print(f"  Cross-cal slope  = {slope_cc:.4f}  ({(slope_cc-1)*100:+.3f}% from unity)")
print(f"  Lever arm pT     = {sl_pt:.3f} σ/% ")
print(f"  Lever arm ΔR     = {sl_an:.3f} σ/% ")
print(f"  pT power β       = {beta_fit:.3f}  (Exp 65: -0.694)")
print()
print("  Calibration chain: Exps 64 → 65 → 66 → 74 → 75")
print("  Figure: results/75_calibration_publication_figure.png")
print("\nExp 75 complete.")
