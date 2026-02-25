#!/usr/bin/env python3
"""
Phase 35 (v2) — Significance with ALL Phase 22-26 cuts correctly applied to Run2012B.

Key finding from v1: without Q_A=0 (opposite-sign pair in Group A),
153/1,035 C4 events in Run2012B have ratio > 8.392 — mass ratio alone is not rare.
The charge cut Q_A=0 is the critical missing cut.

This script adds:
  C1_charge: Q_A = 0 (opposite-sign pair in Group A, i.e., nA=2, exactly 1 Q=+1 and 1 Q=-1)
  C2_dense: tighten Δφ_dense < 0.07 (Phase 24 value)

Then fits the surviving m_B/m_A distribution and computes significance.
"""
import uproot, awkward as ak
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm as sp_norm
import json, os, math

BASE      = "/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer"
ROOT_FILE = f"{BASE}/tools/data/Run2012B_DoubleMuParked.root"
OUT_JSON  = f"{BASE}/results/phase35_significance.json"
OUT_FIG   = f"{BASE}/figures/phase35_ratio_fit.png"
os.makedirs(f"{BASE}/figures", exist_ok=True)
os.makedirs(f"{BASE}/results", exist_ok=True)

TARGET_RATIO = 8.392
N_total      = 26_084_708
N_Run2012C   = 200_000

print("Loading Run2012B NanoAOD ...")
t  = uproot.open(ROOT_FILE)["Events"]
ev = t.arrays(["nMuon","Muon_pt","Muon_eta","Muon_phi","Muon_charge"], library="ak")

nmu   = ak.to_numpy(ev["nMuon"])

# ── C0: nMuon >= 7 ────────────────────────────────────────────────────────
mask0 = nmu >= 7
ev7   = ev[mask0]; nmu7 = nmu[mask0]
phi_  = ev7["Muon_phi"]
chg_  = ev7["Muon_charge"]
print(f"C0 nMuon>=7: {len(ev7):,}")

# ── C1: Δφ(A,B) > 150° ───────────────────────────────────────────────────
nA = ak.to_numpy(ak.sum(phi_ > 0, axis=1))
nB = ak.to_numpy(ak.sum(phi_ < 0, axis=1))
ok = (nA >= 1) & (nB >= 1)
mpA = ak.to_numpy(ak.mean(phi_[phi_ > 0], axis=1))
mpB = ak.to_numpy(ak.mean(phi_[phi_ < 0], axis=1))
dphi = np.where(ok, np.degrees(np.abs(mpA - mpB)), 0.0)
dphi = np.where(dphi > 180, 360 - dphi, dphi)
mask1 = ok & (dphi > 150.0)
print(f"C1 Δφ(A,B)>150°: {np.sum(mask1):,}")

# ── C1_charge: Q_A = 0  (Group A = 2 muons, one +1 one -1) ───────────────
chg_A  = chg_[phi_ > 0]
n_pos_A = ak.to_numpy(ak.sum(chg_A == 1,  axis=1))
n_neg_A = ak.to_numpy(ak.sum(chg_A == -1, axis=1))
mask_qA = (nA == 2) & (n_pos_A == 1) & (n_neg_A == 1)
mask1q = mask1 & mask_qA
print(f"C1 + Q_A=0 (OS pair in A): {np.sum(mask1q):,}")

# ── C2: Δφ_dense(B) < 0.07 rad (Phase 24 value) ──────────────────────────
phiB_max = ak.to_numpy(ak.max(phi_[phi_ < 0], axis=1))
phiB_min = ak.to_numpy(ak.min(phi_[phi_ < 0], axis=1))
dph_dense = phiB_max - phiB_min
mask2 = mask1q & (dph_dense < 0.07)
print(f"C2 Δφ_dense<0.07: {np.sum(mask2):,}")

# ── C3: nB = 5 ────────────────────────────────────────────────────────────
mask3 = mask2 & (nB == 5)
idx3  = np.where(mask3)[0]
print(f"C3 nB=5: {len(idx3):,}")

# ── Invariant mass calculation ────────────────────────────────────────────
def inv_mass(pts, etas, phis):
    px = pts * np.cos(phis); py = pts * np.sin(phis)
    pz = pts * np.sinh(etas); E = pts * np.cosh(etas)
    m2 = E.sum()**2 - px.sum()**2 - py.sum()**2 - pz.sum()**2
    return math.sqrt(max(m2, 0.0))

pt_np  = ak.to_numpy(ak.pad_none(ev7["Muon_pt"],  target=12, clip=True))
eta_np = ak.to_numpy(ak.pad_none(ev7["Muon_eta"], target=12, clip=True))
phi_np = ak.to_numpy(ak.pad_none(ev7["Muon_phi"], target=12, clip=True))

print(f"Computing invariant masses for {len(idx3):,} C3 events ...")
ratios = []; mA_list = []; mB_list = []
for iev in idx3:
    nm = int(nmu7[iev])
    phi_i = phi_np[iev][:nm].astype(float)
    pt_i  = pt_np[iev][:nm].astype(float)
    eta_i = eta_np[iev][:nm].astype(float)
    idxA  = np.where(phi_i > 0)[0]
    idxB  = np.where(phi_i < 0)[0]
    if len(idxA) == 0 or len(idxB) == 0: continue
    mA = inv_mass(pt_i[idxA], eta_i[idxA], phi_i[idxA])
    mB = inv_mass(pt_i[idxB], eta_i[idxB], phi_i[idxB])
    if mA <= 0: continue
    ratios.append(mB/mA); mA_list.append(mA); mB_list.append(mB)

ratios = np.array(ratios)
mask_c4 = ratios > 1.0
r_c4    = ratios[mask_c4]
print(f"\nC4 (ratio>1): {len(r_c4):,}")
print(f"  range: [{r_c4.min():.3f}, {r_c4.max():.3f}]  median: {np.median(r_c4):.3f}")

# Count how many have ratio > target
n_above = np.sum(r_c4 > TARGET_RATIO)
print(f"  Events at ratio > {TARGET_RATIO}: {n_above}")

# Phase 26 proxy: ratio > 6
n_above_6 = np.sum(r_c4 > 6.0)
print(f"  Events at ratio > 6.0: {n_above_6}")

r_c4_sorted = np.sort(r_c4)[::-1]
print(f"\nTop 10 ratios:")
for rr in r_c4_sorted[:10]:
    print(f"  {rr:.4f}")

# ── Fit the m_B/m_A distribution (power-law in log space) ─────────────────
log_r = np.log(r_c4)
bins  = np.linspace(np.log(1.0), np.log(max(r_c4.max(), TARGET_RATIO * 1.5)), 30)
bin_c = 0.5 * (bins[:-1] + bins[1:])
bin_w = np.diff(bins)[0]
counts, _ = np.histogram(log_r, bins=bins)
nz = counts > 0
xfit = bin_c[nz]; yfit = counts[nz].astype(float); yerr = np.sqrt(yfit)

def pl_log(lr, lnA, alpha):
    return np.exp(lnA) * np.exp(-alpha * lr)

power_ok = False
lognorm_ok = False
try:
    p_pw, cov_pw = curve_fit(pl_log, xfit, yfit, sigma=yerr, p0=[np.log(len(r_c4)), 1.5], maxfev=5000)
    alpha = p_pw[1]
    print(f"\nPower-law fit: alpha={p_pw[1]:.3f} ± {np.sqrt(cov_pw[1,1]):.3f}")
    power_ok = True
except Exception as e:
    print(f"Power-law fit failed: {e}")

def lognorm_log(lr, lnA, mu, sig):
    return np.exp(lnA) * np.exp(-0.5 * ((lr - mu)/sig)**2)

try:
    p_ln, cov_ln = curve_fit(lognorm_log, xfit, yfit, sigma=yerr,
                              p0=[np.log(len(r_c4)/5), 0.5, 0.8], maxfev=5000)
    print(f"Log-normal fit: mu={p_ln[1]:.3f} ± {np.sqrt(cov_ln[1,1]):.3f}  "
          f"sigma={p_ln[2]:.3f} ± {np.sqrt(cov_ln[2,2]):.3f}")
    lognorm_ok = True
except Exception as e:
    print(f"Log-normal fit failed: {e}")

# ── Extrapolate to ratio > TARGET_RATIO ───────────────────────────────────
print("\n" + "="*60)
print("P-VALUE SUMMARY")
print("="*60)

results = {
    "cut_flow": {
        "C0_nMuGe7":      int(len(ev7)),
        "C1_dphi150":     int(np.sum(mask1)),
        "C1q_QA0":        int(np.sum(mask1q)),
        "C2_dense007":    int(np.sum(mask2)),
        "C3_nB5":         int(len(idx3)),
        "C4_ratio_gt1":   int(len(r_c4)),
        "C4_ratio_gt6":   int(n_above_6),
        "C4_ratio_gtTgt": int(n_above),
    },
}

log_r_tgt = math.log(TARGET_RATIO)

# Method A: power-law
if power_ok:
    A_pw = math.exp(p_pw[0])
    if p_pw[1] > 0:
        integral = A_pw / p_pw[1] * math.exp(-p_pw[1] * log_r_tgt)
        N_bkg_pw = integral / bin_w
        N_bkg_full = N_bkg_pw / len(r_c4) * N_total
        p_A = 1 - math.exp(-N_bkg_full) if N_bkg_full > 0 else 1.0
        if 0 < p_A < 1:
            Z_A = sp_norm.ppf(1 - p_A)
        else:
            Z_A = float('inf') if p_A == 0 else -float('inf')
        print(f"\nMethod A (Power-law, all Phase 22-26 cuts):")
        print(f"  N_expected (C4 sample) = {N_bkg_pw:.4f}")
        print(f"  N_expected (26.1M scaled) = {N_bkg_full:.4e}")
        print(f"  p-value = {p_A:.4e}  Z = {Z_A:.2f}σ")
        results["method_A_powerlaw"] = {
            "N_expected_in_C4": float(N_bkg_pw),
            "N_expected_full": float(N_bkg_full),
            "p_value": float(p_A),
            "Z_sigma": float(Z_A),
        }

# Method A2: log-normal
if lognorm_ok:
    A_ln = math.exp(p_ln[0]); mu_ln = p_ln[1]; sig_ln = abs(p_ln[2])
    import math as m2
    integral_ln = A_ln * sig_ln * math.sqrt(2*math.pi) * 0.5 * math.erfc(
        (log_r_tgt - mu_ln) / (sig_ln * math.sqrt(2)))
    N_bkg_ln = integral_ln / bin_w
    N_bkg_ln_full = N_bkg_ln / len(r_c4) * N_total
    p_A2 = 1 - math.exp(-N_bkg_ln_full) if N_bkg_ln_full > 0 else 1.0
    if 0 < p_A2 < 1:
        Z_A2 = sp_norm.ppf(1 - p_A2)
    else:
        Z_A2 = float('inf') if p_A2 == 0 else -float('inf')
    print(f"\nMethod A2 (Log-normal fit):")
    print(f"  N_expected (C4 sample) = {N_bkg_ln:.4f}")
    print(f"  N_expected (26.1M scaled) = {N_bkg_ln_full:.4e}")
    print(f"  p-value = {p_A2:.4e}  Z = {Z_A2:.2f}σ")
    results["method_A2_lognormal"] = {
        "N_expected_in_C4": float(N_bkg_ln),
        "N_expected_full": float(N_bkg_ln_full),
        "p_value": float(p_A2),
        "Z_sigma": float(Z_A2),
    }

# Method B: empirical — counting at ratio > max(r_c4 < TARGET)
r_below_tgt = r_c4[r_c4 < TARGET_RATIO]
if len(r_below_tgt) > 0:
    r_max_below = r_below_tgt.max()
    n_above_max = int(np.sum(r_c4 > r_max_below))
    N_empirical_full = n_above_max / len(r_c4) * N_total
    p_B = 1 - math.exp(-N_empirical_full)
    Z_B = sp_norm.ppf(1 - p_B) if 0 < p_B < 1 else (float('inf') if p_B == 0 else -float('inf'))
    print(f"\nMethod B (empirical counting at ratio > 2nd-highest below target):")
    print(f"  Threshold = {r_max_below:.4f}  N_above = {n_above_max}  scaled = {N_empirical_full:.3f}")
    print(f"  p-value = {p_B:.4e}  Z = {Z_B:.2f}σ")
    results["method_B_empirical"] = {
        "threshold": float(r_max_below),
        "n_above_in_C4": n_above_max,
        "N_expected_full": float(N_empirical_full),
        "p_value": float(p_B),
        "Z_sigma": float(Z_B),
    }

# Method C: Poisson zero-count upper limit from Run2012C 200k
# 0/200k at ratio > 5.5 (Phase 32) → 95% CL UL = 3.0 events in 200k
# Scaled to 26.1M: 3.0 * 26.1M / 200k = 391 expected (too conservative — UL only)
# Better: use 0/200k at the CURRENT threshold accounting for charge cut
# The 0/200k with ALL cuts gives: UL rate per event = 3.0/200k = 1.5e-5
N_UL_200k = 3.0   # 95% CL for 0 observed
rate_UL    = N_UL_200k / N_Run2012C
N_UL_full  = rate_UL * N_total
print(f"\nMethod C (Poisson UL from 0 observed in Run2012C 200k):")
print(f"  UL (95% CL) on N_bkg in 200k = {N_UL_200k}")
print(f"  Rate UL per event = {rate_UL:.3e}")
print(f"  Scaled to 26.1M: {N_UL_full:.2f} (conservative upper limit)")
results["method_C_UL"] = {
    "N_UL_95pct_in_200k": N_UL_200k,
    "rate_UL": float(rate_UL),
    "N_UL_scaled_26M": float(N_UL_full),
}

# Method D: sole survivor counting in Run2012C 200k with ALL Phase 22-26 cuts
# 1 survivor (the target) in 200k at m_B/m_A > 5.5
p_D = 1.0 / N_Run2012C
Z_D = sp_norm.ppf(1 - p_D) if p_D < 1 else 0.0
# LEE correction
Z_local = Z_D
N_trials = N_Run2012C
threshold_LEE = math.sqrt(2 * math.log(N_trials))
Z_global = max(Z_local - threshold_LEE / max(Z_local, 1e-6), 0)
print(f"\nMethod D (sole survivor in 200k Run2012C):")
print(f"  p_local = {p_D:.3e}  Z_local = {Z_D:.2f}σ")
print(f"  LEE threshold = {threshold_LEE:.2f}  Z_global ≈ {Z_global:.2f}σ")
results["method_D_counting"] = {
    "n_survivors_in_200k": 1,
    "p_local": float(p_D),
    "Z_local": float(Z_D),
    "LEE_threshold": float(threshold_LEE),
    "Z_global_approx": float(Z_global),
}

# ── Combined estimate ─────────────────────────────────────────────────────
print("\n" + "="*60)
print("COMBINED SUMMARY")
print("="*60)
print(f"  Without charge cut (v1): 153/1,035 C4 events above target ratio")
print(f"  With charge cut Q_A=0 (v2): {n_above}/C4 events above target ratio")
print(f"  Z (sole survivor, 200k, LEE-corrected) = {Z_global:.2f}σ")
if power_ok and "Z_sigma" in results.get("method_A_powerlaw", {}):
    print(f"  Z (power-law extrapolation, full cuts) = {results['method_A_powerlaw']['Z_sigma']:.2f}σ")

with open(OUT_JSON, "w") as fp:
    json.dump(results, fp, indent=2)
print(f"\nResults saved: {OUT_JSON}")

# ─────────────────────────────────────────────────────────────────────────
# Figure: before/after charge cut + ratio distribution + fits
# ─────────────────────────────────────────────────────────────────────────
# Load v1 ratios (without charge cut) for comparison
print("\nReloading C4 ratios WITHOUT charge cut for comparison figure ...")
mask3_noq = (ak.to_numpy(ak.sum(phi_ > 0, axis=1)) >= 1) & \
            (ak.to_numpy(ak.sum(phi_ < 0, axis=1)) >= 1) & \
            ok & (dphi > 150.0) & (dph_dense < 0.10) & (nB == 5)
idx3_noq = np.where(mask3_noq)[0]
ratios_noq = []
for iev in idx3_noq:
    nm = int(nmu7[iev])
    phi_i = phi_np[iev][:nm].astype(float)
    pt_i  = pt_np[iev][:nm].astype(float)
    eta_i = eta_np[iev][:nm].astype(float)
    idxA  = np.where(phi_i > 0)[0]
    idxB  = np.where(phi_i < 0)[0]
    if not idxA.size or not idxB.size: continue
    mA = inv_mass(pt_i[idxA], eta_i[idxA], phi_i[idxA])
    mB = inv_mass(pt_i[idxB], eta_i[idxB], phi_i[idxB])
    if mA > 0: ratios_noq.append(mB/mA)
r_noq = np.array([r for r in ratios_noq if r > 1])

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Panel 1: without charge cut
ax0 = axes[0]
bins_lo = np.linspace(1, 20, 40)
ax0.hist(r_noq, bins=bins_lo, color="#aec7e8", alpha=0.8, label=f"NO Q_A=0 (N={len(r_noq):,})")
ax0.axvline(TARGET_RATIO, color="red", lw=1.8, ls="--", label=f"Target {TARGET_RATIO:.2f}")
ax0.set_title("C4 ratio distribution\n(WITHOUT charge cut)", fontsize=9)
ax0.set_xlabel("m_B/m_A"); ax0.legend(fontsize=7)
ax0.spines["top"].set_visible(False); ax0.spines["right"].set_visible(False)
ax0.text(0.62, 0.82, f"N>target: {int(np.sum(r_noq>TARGET_RATIO))}",
         transform=ax0.transAxes, fontsize=8, color="darkred")

# Panel 2: with charge cut
ax1 = axes[1]
ax1.hist(r_c4, bins=bins_lo, color="#4c9ed9", alpha=0.8, label=f"WITH Q_A=0 (N={len(r_c4):,})")
ax1.axvline(TARGET_RATIO, color="red", lw=1.8, ls="--", label=f"Target {TARGET_RATIO:.2f}")
ax1.set_title("C4 ratio distribution\n(WITH Q_A=0, Δφ_dense<0.07)", fontsize=9)
ax1.set_xlabel("m_B/m_A"); ax1.legend(fontsize=7)
ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
ax1.text(0.62, 0.82, f"N>target: {n_above}",
         transform=ax1.transAxes, fontsize=8, color="darkred")

# Panel 3: log-scale tail — fit and target
ax2 = axes[2]
ax2.semilogy()
bins_log = np.linspace(1, 20, 40)
ax2.hist(r_c4, bins=bins_log, color="#4c9ed9", alpha=0.70, label=f"With Q_A=0 (N={len(r_c4):,})")
r_plot = np.linspace(1, 20, 300)
lr_plot = np.log(r_plot)
if power_ok:
    yfit_pw = pl_log(lr_plot, *p_pw)
    total_pw = np.trapz(yfit_pw, lr_plot)
    bin_w_disp = bins_log[1] - bins_log[0]
    scale_pw = len(r_c4) * bin_w_disp / bin_w / total_pw * bin_w
    ax2.plot(r_plot, yfit_pw * scale_pw, color="navy", lw=1.8, label=f"Power-law α={p_pw[1]:.2f}")
if lognorm_ok:
    yfit_ln = lognorm_log(lr_plot, *p_ln)
    total_ln = np.trapz(yfit_ln, lr_plot)
    scale_ln = len(r_c4) * bin_w_disp / bin_w / total_ln * bin_w
    ax2.plot(r_plot, yfit_ln * scale_ln, color="darkorange", lw=1.8, ls="--",
             label=f"Log-normal μ={p_ln[1]:.2f}")
ax2.axvline(TARGET_RATIO, color="red", lw=1.8, ls="--", label=f"Target {TARGET_RATIO:.2f}")
ax2.axvspan(TARGET_RATIO, 20.5, alpha=0.10, color="red")
ax2.set_xlim(1, 20); ax2.set_ylim(0.3, 2e3)
ax2.set_xlabel("m_B/m_A"); ax2.set_ylabel("Events/bin (log)")
ax2.set_title("Tail fit — all Phase 22-26 cuts\n(log scale)", fontsize=9)
ax2.legend(fontsize=7, framealpha=0.5)
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)
if "method_A_powerlaw" in results:
    Z_show = results["method_A_powerlaw"]["Z_sigma"]
    N_show = results["method_A_powerlaw"]["N_expected_full"]
    ax2.text(0.35, 0.12,
             f"N_exp={N_show:.2e}\nZ={Z_show:.1f}σ (pwlaw)",
             transform=ax2.transAxes, fontsize=8, color="darkred",
             bbox=dict(boxstyle="round", fc="white", alpha=0.7))

fig.suptitle("Phase 35 — Statistical Significance of 7-Muon Anomaly Event\n"
             "CMS Run2012B DoubleMuParked 26.1M events, all Phase 22–26 cuts", fontsize=10)
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=150, bbox_inches="tight")
print(f"Figure saved: {OUT_FIG}")
print("\nDone.")
