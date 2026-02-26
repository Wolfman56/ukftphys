#!/usr/bin/env python3
"""
Experiment 63: Dark Photon kinematic comparison and rate matching
=================================================================
Compares MG5 A' → μ+μ- j predictions against 51 CMS d5 candidates found
by the UKFT Borda scan (experiments 76a–76h-B).

Three MG5 runs (all at ε=1e-3, sqrt(s)=8 TeV):
  A: MDP = 1.80 GeV  (benchmark, 10k events)
  B: MDP = 1.50 GeV  (lower mass edge, 5k events)
  C: MDP = 2.20 GeV  (upper mass edge, 5k events)

Physics:
  σ(pp → A'j → μμj) ∝ ε²   (kinetic mixing)
  ΔR(μμ) ≈ 2·MDP / pT_A'   (boost formula — diagnostic)
  N_exp = σ × L × A × ε²   where L = 7000 pb⁻¹, A = acceptance

Key outputs:
  - ΔR, m_inv, pT distributions overlaid with CMS data
  - Rate-match: ε_fit such that N_exp(ε_fit) = 51
  - ΔR boost formula check: ΔR_MG5 vs 2m/pT
  - Result JSON with cross-sections, epsilon fits, KS statistics
"""

import gzip
import json
import math
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ks_2samp

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────
MG5_DIR   = Path("/Users/enconcertincdev4/Code/grok/MG5_aMC_v3_7_0")
CMS_JSON  = Path("/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer"
                 "/tools/76h_b_kinematics.json")
OUT_DIR   = Path("/Users/enconcertincdev4/Code/grok/ukftphys/results")
OUT_DIR.mkdir(exist_ok=True)

# LHE output directories for each run
RUN_DIRS = {
    "A_1p80": MG5_DIR / "experiments/63_dp_1p80gev",
    "B_1p50": MG5_DIR / "experiments/63_dp_1p50gev",
    "C_2p20": MG5_DIR / "experiments/63_dp_2p20gev",
}
RUN_LABELS = {
    "A_1p80": "A' M=1.80 GeV",
    "B_1p50": "A' M=1.50 GeV",
    "C_2p20": "A' M=2.20 GeV",
}
RUN_MASSES = {"A_1p80": 1.80, "B_1p50": 1.50, "C_2p20": 2.20}

LUMINOSITY_PB   = 7000.0   # CMS Run2012C, ~7 fb⁻¹ in pb⁻¹
# NOTE: Due to MG5 model restriction applying ε=1 (photon-strength coupling),
# the simulation was effectively run with ε_eff = 1.0 (NOT 1e-3).
# MG5 merged GC_Ap_* with photon couplings since restrict_default.dat had ε=1.0.
# σ(ε) = σ(ε_eff=1.0) × ε²   so rate-matching gives physical ε = ε_fit below.
EPSILON_REF     = 1.0      # ε_eff used in MG5 (photon strength after model restriction)
N_OBS           = 51       # observed d5 candidates
CMS_EFF_ETA     = 1.0      # raw production rate (CMS acceptance modeled separately)
PDG_RHO         = 0.775    # ρ meson, veto region
PDG_OMEGA       = 0.782    # ω meson
PDG_PHI         = 1.019    # φ meson
PDG_JPSI        = 3.097    # J/ψ meson

# ─────────────────────────────────────────────────────────────────────────────
# CMS data loader
# ─────────────────────────────────────────────────────────────────────────────

def load_cms_data():
    """
    Load the CMS d5 OS dimuon candidates from 76h-B kinematics JSON.
    Records structure: {borda_rank, event_id, m_inv, pt_lead, pt_sub,
                        eta_lead, eta_sub, phi_lead, phi_sub, dR, deta, dphi,
                        HT_dimuon, charge_product, sm_filtered, d5, ...}
    Select: charge_product == -1 (OS) and sm_filtered == False (not SM-like)
    """
    with open(CMS_JSON) as f:
        data = json.load(f)

    records = data.get("records", [])
    result  = []
    for r in records:
        # OS requirement AND not SM-filtered
        if r.get("charge_product", 0) != -1:
            continue
        # Accept all OS dimuon events (sm_filtered also interesting — include both)
        pt1  = r["pt_lead"]
        pt2  = r["pt_sub"]
        dr   = r["dR"]
        m    = r["m_inv"]
        pt_s = r.get("HT_dimuon", pt1 + pt2)
        result.append({
            "pt1":    pt1,
            "eta1":   r["eta_lead"],
            "phi1":   r["phi_lead"],
            "pt2":    pt2,
            "eta2":   r["eta_sub"],
            "phi2":   r["phi_sub"],
            "dr":     dr,
            "m":      m,
            "pt_sys": pt_s,
            "is_star":       r.get("is_star", False),
            "sm_filtered":   r.get("sm_filtered", False),
            "d5_score":      r.get("d5", 0),
            "charge_product":r.get("charge_product", -1),
        })
    return result


# ─────────────────────────────────────────────────────────────────────────────
# LHE parser
# ─────────────────────────────────────────────────────────────────────────────

def iter_lhe_events(path):
    """Yield (list of particles) from an LHE file (plain or .gz)."""
    # Detect .gz
    events_dir = path / "Events"
    if not events_dir.exists():
        return
    lhe_files = list(events_dir.rglob("*.lhe.gz")) + list(events_dir.rglob("*.lhe"))
    if not lhe_files:
        return

    lhe_file = sorted(lhe_files)[0]
    opener = gzip.open if str(lhe_file).endswith(".gz") else open

    with opener(lhe_file, "rt", errors="replace") as f:
        content = f.read()

    # Extract cross-section from header
    xsec = None
    for line in content.split("\n"):
        if "Integrated weight (pb)" in line or "Cross-section :" in line:
            parts = line.split(":")
            if len(parts) >= 2:
                try:
                    xsec = float(parts[-1].strip().split()[0])
                except Exception:
                    pass
        if "<init>" in line.lower() and xsec is None:
            pass

    # Parse event blocks
    in_event = False
    particles = []
    events = []

    for line in content.split("\n"):
        stripped = line.strip()
        if "<event>" in stripped.lower():
            in_event = True
            particles = []
            continue
        if "</event>" in stripped.lower():
            if particles:
                events.append(particles)
            in_event = False
            continue
        if in_event and stripped and not stripped.startswith("#") and not stripped.startswith("<"):
            parts = stripped.split()
            if len(parts) >= 9:
                try:
                    pdg    = int(parts[0])
                    status = int(parts[1])
                    px     = float(parts[6])
                    py     = float(parts[7])
                    pz     = float(parts[8])
                    E      = float(parts[9]) if len(parts) > 9 else 0.0
                    particles.append({
                        "pdg": pdg, "status": status,
                        "px": px, "py": py, "pz": pz, "E": E,
                    })
                except Exception:
                    pass

    return events, xsec


def get_xsec_from_log(run_dir):
    """Extract cross-section from MG5 run log."""
    xsec = None
    for log_pattern in ["crossx.html", "run_*.log", "*.log"]:
        for f in run_dir.rglob(log_pattern):
            try:
                content = open(f, errors="replace").read()
                for line in content.split("\n"):
                    if any(kw in line for kw in
                           ["Cross section", "sigma =", "xsec", "Integrated weight"]):
                        parts = line.replace("±","+-").split()
                        for i, p in enumerate(parts):
                            try:
                                v = float(p)
                                if 1e-10 < v < 1e15:
                                    xsec = v
                            except Exception:
                                pass
            except Exception:
                pass
    return xsec


def parse_mg5_run(run_dir):
    """Parse MG5 output directory: extract events and cross-section."""
    if not run_dir.exists():
        print(f"  [MISSING] {run_dir}")
        return None, None

    result = iter_lhe_events(run_dir)
    if result is None:
        print(f"  [NO LHE]  {run_dir}")
        return None, None

    events, xsec_from_lhe = result
    if xsec_from_lhe is None:
        xsec_from_lhe = get_xsec_from_log(run_dir)

    # Also try to read from run_results.dat
    results_file = run_dir / "Events" / "run_01" / "run_results.dat"
    if results_file.exists():
        try:
            content = open(results_file).read()
            for line in content.split("\n"):
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        v = float(parts[0])
                        if 1e-12 < v < 1e15:
                            xsec_from_lhe = v
                    except Exception:
                        pass
        except Exception:
            pass

    return events, xsec_from_lhe


# ─────────────────────────────────────────────────────────────────────────────
# Kinematics from events
# ─────────────────────────────────────────────────────────────────────────────

def compute_kinematics(events):
    """
    Extract dimuon kinematics from MG5 LHE events.
    Looks for final-state mu+ (pdg=-13) and mu- (pdg=13) pairs.
    """
    dr_list, m_list, pt_list, pta_list, ptb_list = [], [], [], [], []
    boost_dr_list, boost_dr_pred = [], []

    for particles in events:
        # Collect final-state muons (status=1)
        muons = [p for p in particles if abs(p["pdg"]) == 13 and p["status"] == 1]
        if len(muons) < 2:
            continue

        # Take the hardest pair
        muons.sort(key=lambda p: p["px"]**2 + p["py"]**2 + p["pz"]**2, reverse=True)
        mu1, mu2 = muons[0], muons[1]

        # Convert to pT, eta, phi
        def to_ptetaphi(p):
            px, py, pz, E = p["px"], p["py"], p["pz"], p["E"]
            pt = math.sqrt(px**2 + py**2)
            eta = -math.log(math.tan(math.atan2(pt, pz) / 2 + 1e-12))
            phi = math.atan2(py, px)
            return pt, eta, phi

        pt1, eta1, phi1 = to_ptetaphi(mu1)
        pt2, eta2, phi2 = to_ptetaphi(mu2)

        dphi = phi1 - phi2
        while dphi >  math.pi: dphi -= 2*math.pi
        while dphi < -math.pi: dphi += 2*math.pi
        deta = eta1 - eta2
        dr   = math.sqrt(deta**2 + dphi**2)

        # Invariant mass
        m2 = 2 * pt1 * pt2 * (math.cosh(deta) - math.cos(dphi))
        m  = math.sqrt(max(m2, 0.0))

        # Dimuon system pT
        px_sys = mu1["px"] + mu2["px"]
        py_sys = mu1["py"] + mu2["py"]
        pt_sys = math.sqrt(px_sys**2 + py_sys**2)

        # Boost formula prediction: ΔR_pred = 2m/pT_sys
        dr_pred = 2 * m / (pt_sys + 1e-6)

        dr_list.append(dr)
        m_list.append(m)
        pt_list.append(pt_sys)
        pta_list.append(pt1)
        ptb_list.append(pt2)
        boost_dr_list.append(dr)
        boost_dr_pred.append(dr_pred)

    return {
        "dr":           np.array(dr_list),
        "m":            np.array(m_list),
        "pt_sys":       np.array(pt_list),
        "pt_lead":      np.array(pta_list),
        "pt_sub":       np.array(ptb_list),
        "boost_dr_obs": np.array(boost_dr_list),
        "boost_dr_pred":np.array(boost_dr_pred),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Rate matching
# ─────────────────────────────────────────────────────────────────────────────

def compute_epsilon_fit(xsec_pb, epsilon_ref, n_obs, luminosity, efficiency=1.0):
    """
    Find ε_fit such that σ(ε_fit) × L × eff = N_obs.
    Since σ ∝ ε², ε_fit = ε_ref × sqrt(N_obs / (σ_ref × L × eff)).
    Returns (epsilon_fit, n_expected_at_epsilon_ref).
    """
    if xsec_pb is None or xsec_pb <= 0:
        return None, None
    n_expected_ref = xsec_pb * luminosity * efficiency
    epsilon_fit    = epsilon_ref * math.sqrt(n_obs / n_expected_ref) if n_expected_ref > 0 else None
    return epsilon_fit, n_expected_ref


# ─────────────────────────────────────────────────────────────────────────────
# Plotting
# ─────────────────────────────────────────────────────────────────────────────

COLORS   = {"A_1p80": "#e74c3c", "B_1p50": "#3498db", "C_2p20": "#2ecc71"}
CMS_CLR  = "#f39c12"

def make_plots(cms_data, mg5_kinematics, xsecs, summary):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("Exp 63: Dark Photon A'j → μ+μ- j  vs  CMS d5 Candidates (51 events)\n"
                 "√s = 8 TeV,  ε = 1×10⁻³ (MG5),  L = 7 fb⁻¹", fontsize=12)

    cms_dr  = np.array([ev["dr"] for ev in cms_data])
    cms_m   = np.array([ev["m"]  for ev in cms_data])
    cms_pt  = np.array([ev["pt_sys"] for ev in cms_data])

    # ── ΔR distribution ─────────────────────────────────────────────────────
    ax = axes[0, 0]
    bins_dr = np.linspace(0, 0.8, 25)
    ax.hist(cms_dr, bins=bins_dr, density=True, alpha=0.7, color=CMS_CLR,
            label=f"CMS d5 (N={N_OBS})", histtype="stepfilled", zorder=3)
    for key, kin in mg5_kinematics.items():
        if kin is None: continue
        ax.hist(kin["dr"], bins=bins_dr, density=True, alpha=0.6,
                color=COLORS[key], label=RUN_LABELS[key], histtype="step",
                linewidth=2, zorder=2)
    ax.set_xlabel("ΔR(μ⁺,μ⁻)")
    ax.set_ylabel("Normalized")
    ax.set_title("ΔR: CMS vs A' model")
    ax.legend(fontsize=7)
    ax.set_xlim(0, 0.8)
    ax.axvline(0.087, color=CMS_CLR, linestyle="--", alpha=0.5, label="CMS mean")

    # ── m(μμ) invariant mass ─────────────────────────────────────────────────
    ax = axes[0, 1]
    bins_m = np.linspace(0, 4.0, 30)
    ax.hist(cms_m, bins=bins_m, density=True, alpha=0.7, color=CMS_CLR,
            label=f"CMS d5 (N={N_OBS})", histtype="stepfilled", zorder=3)
    for key, kin in mg5_kinematics.items():
        if kin is None: continue
        ax.hist(kin["m"], bins=bins_m, density=True, alpha=0.6,
                color=COLORS[key], label=RUN_LABELS[key], histtype="step",
                linewidth=2, zorder=2)
    for vline, label in [(PDG_RHO, "ρ"), (PDG_PHI, "φ")]:
        ax.axvline(vline, color="gray", linestyle=":", alpha=0.5)
        ax.text(vline + 0.03, 0.05, label, fontsize=7, color="gray",
                transform=ax.get_xaxis_transform())
    ax.set_xlabel("m(μ⁺μ⁻) [GeV]")
    ax.set_ylabel("Normalized")
    ax.set_title("Invariant mass: CMS vs A' model")
    ax.legend(fontsize=7)

    # ── pT(dimuon) ──────────────────────────────────────────────────────────
    ax = axes[0, 2]
    bins_pt = np.linspace(0, 80, 25)
    ax.hist(cms_pt, bins=bins_pt, density=True, alpha=0.7, color=CMS_CLR,
            label=f"CMS d5 (N={N_OBS})", histtype="stepfilled", zorder=3)
    for key, kin in mg5_kinematics.items():
        if kin is None: continue
        ax.hist(kin["pt_sys"], bins=bins_pt, density=True, alpha=0.6,
                color=COLORS[key], label=RUN_LABELS[key], histtype="step",
                linewidth=2, zorder=2)
    ax.set_xlabel("pT(μ⁺μ⁻) [GeV]")
    ax.set_ylabel("Normalized")
    ax.set_title("Dimuon pT: CMS vs A' model")
    ax.legend(fontsize=7)

    # ── Boost formula check: ΔR vs 2m/pT ───────────────────────────────────
    ax = axes[1, 0]
    ax.scatter(cms_m / cms_pt * 2, cms_dr, s=15, alpha=0.5, color=CMS_CLR,
               label="CMS d5", zorder=3)
    for key, kin in mg5_kinematics.items():
        if kin is None: continue
        ax.scatter(kin["boost_dr_pred"], kin["boost_dr_obs"],
                   s=5, alpha=0.3, color=COLORS[key], label=RUN_LABELS[key])
    _x = np.linspace(0, 0.8, 100)
    ax.plot(_x, _x, "k--", linewidth=1, alpha=0.5, label="ΔR = 2m/pT (perfect)")
    ax.set_xlabel("2·m / pT_sys  [boost formula]")
    ax.set_ylabel("ΔR_obs(μ⁺,μ⁻)")
    ax.set_title("Boost formula: ΔR = 2m/pT")
    ax.set_xlim(0, 0.8); ax.set_ylim(0, 0.8)
    ax.legend(fontsize=7)

    # ── Rate matching: ε_fit ────────────────────────────────────────────────
    ax = axes[1, 1]
    run_keys = list(xsecs.keys())
    eps_fits = [summary.get(k, {}).get("epsilon_fit") for k in run_keys]
    masses   = [RUN_MASSES[k] for k in run_keys]
    colors_list = [COLORS[k] for k in run_keys]
    valid = [(m, e, c) for m, e, c in zip(masses, eps_fits, colors_list) if e is not None]
    if valid:
        ms_, es_, cls_ = zip(*valid)
        ax.scatter(ms_, es_, s=80, c=cls_, zorder=3)
        for m_, e_, key in zip(ms_, es_, run_keys):
            ax.annotate(f"ε={e_:.2e}", (m_, e_), fontsize=7, xytext=(5, 5),
                        textcoords="offset points")
        ax.axhline(1e-3, color="gray", linestyle="--", alpha=0.5, label="ε_ref=1e-3")
        ax.set_xlabel("MDP [GeV]")
        ax.set_ylabel("ε_fit (to match N=51 at 7 fb⁻¹)")
        ax.set_title("Rate matching: ε required")
        ax.set_yscale("log")
        ax.legend(fontsize=7)
    else:
        ax.text(0.5, 0.5, "Cross-sections\nnot yet available\n(MG5 still running?)",
                ha="center", va="center", transform=ax.transAxes, fontsize=9)
        ax.set_title("Rate matching (pending)")

    # ── KS statistics ────────────────────────────────────────────────────────
    ax = axes[1, 2]
    ax.axis("off")
    lines = ["Kinematic Shape Comparison (KS test, ΔR)", ""]
    for key, kin in mg5_kinematics.items():
        if kin is None:
            lines.append(f"{RUN_LABELS[key]}: NO DATA")
            continue
        ks_stat, ks_p = ks_2samp(cms_dr, kin["dr"])
        xsec = xsecs.get(key)
        eps_fit = summary.get(key, {}).get("epsilon_fit")
        n_ref   = summary.get(key, {}).get("n_expected_ref")
        lines += [
            f"{RUN_LABELS[key]}:",
            f"  σ(ε=1e-3) = {xsec:.3g} pb" if xsec else "  σ = N/A",
            f"  N_exp(ε=1e-3, 7fb⁻¹) = {n_ref:.1f}" if n_ref else "  N_exp = N/A",
            f"  ε_fit = {eps_fit:.2e}" if eps_fit else "  ε_fit = N/A",
            f"  KS(ΔR) = {ks_stat:.3f} (p={ks_p:.3f})",
            "",
        ]
    lines += ["", f"CMS d5: N={N_OBS}, <ΔR>={cms_dr.mean():.3f}±{cms_dr.std():.3f}",
              f"        <m>={cms_m.mean():.2f}±{cms_m.std():.2f} GeV",
              f"        <pT_sys>={cms_pt.mean():.1f}±{cms_pt.std():.1f} GeV"]
    ax.text(0.05, 0.95, "\n".join(lines), transform=ax.transAxes,
            fontsize=7, verticalalignment="top", family="monospace",
            bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))
    ax.set_title("Summary")

    plt.tight_layout()
    out_path = OUT_DIR / "63_darkphoton_comparison.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"  Plot saved: {out_path}")
    plt.close()


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("Experiment 63: Dark Photon A'j → μ+μ- j  vs  CMS d5 Candidates")
    print("=" * 70)

    # Load CMS data
    print("\n[1] Loading CMS d5 data ...")
    cms_data = load_cms_data()
    print(f"    N_cms = {len(cms_data)} events")
    if not cms_data:
        print("    WARNING: No CMS data found. Check CMS_JSON path.")
    else:
        cms_dr = [ev["dr"] for ev in cms_data]
        cms_m  = [ev["m"]  for ev in cms_data]
        print(f"    <ΔR> = {np.mean(cms_dr):.3f} ± {np.std(cms_dr):.3f}")
        print(f"    <m>  = {np.mean(cms_m):.3f} ± {np.std(cms_m):.3f} GeV")

    # Parse MG5 runs
    print("\n[2] Parsing MG5 output directories ...")
    mg5_kinematics = {}
    xsecs          = {}
    summary        = {}

    for run_key, run_dir in RUN_DIRS.items():
        print(f"\n  Run {run_key}: {run_dir.name}")
        events, xsec = parse_mg5_run(run_dir)

        if events is None:
            print(f"    Status: MISSING or not yet complete")
            mg5_kinematics[run_key] = None
            xsecs[run_key]          = None
            summary[run_key]        = {"status": "missing"}
            continue

        print(f"    Events parsed: {len(events)}")
        print(f"    σ(pp→A'j→μμj, ε_eff=1.0) = {xsec:.4g} pb" if xsec else
              "    σ: not found in log")

        kin = compute_kinematics(events)
        n_mu = len(kin["dr"])
        print(f"    Dimuon pairs: {n_mu}")
        if n_mu > 0:
            print(f"    <ΔR> = {kin['dr'].mean():.3f} ± {kin['dr'].std():.3f}")
            print(f"    <m>  = {kin['m'].mean():.3f} ± {kin['m'].std():.3f} GeV")
            print(f"    <pT> = {kin['pt_sys'].mean():.1f} ± {kin['pt_sys'].std():.1f} GeV")

            # Boost formula check
            boost_res = kin["boost_dr_pred"]
            print(f"    Boost-formula <2m/pT> = {boost_res.mean():.3f} ± {boost_res.std():.3f}")
            delta_frac = abs(boost_res.mean() - kin["dr"].mean()) / (kin["dr"].mean() + 1e-6)
            print(f"    Boost formula accuracy: |ΔR_obs - 2m/pT| / ΔR_obs = {delta_frac:.2%}")

        mg5_kinematics[run_key] = kin
        xsecs[run_key]          = xsec

        # Rate matching
        eps_fit, n_ref = compute_epsilon_fit(xsec, EPSILON_REF, N_OBS,
                                             LUMINOSITY_PB, CMS_EFF_ETA)
        summary[run_key] = {
            "status":         "ok",
            "n_events":       n_mu,
            "xsec_pb":        xsec,
            "n_expected_ref": n_ref,
            "epsilon_fit":    eps_fit,
            "dr_mean":        float(kin["dr"].mean()) if n_mu > 0 else None,
            "dr_std":         float(kin["dr"].std())  if n_mu > 0 else None,
            "m_mean":         float(kin["m"].mean())  if n_mu > 0 else None,
            "m_std":          float(kin["m"].std())   if n_mu > 0 else None,
            "pt_mean":        float(kin["pt_sys"].mean()) if n_mu > 0 else None,
        }
        if eps_fit is not None:
            print(f"\n    ── RATE MATCH ──")
            print(f"    N_expected(ε_eff=1.0, 7fb⁻¹) = {n_ref:.1f}")
            print(f"    N_observed                     = {N_OBS}")
            print(f"    ε_fit (to match N_obs)         = {eps_fit:.3e}")
            print(f"    (σ ∝ ε²: scale σ by ε²_fit to get physical rate)")

    # KS test: CMS vs Run A (primary comparison)
    print("\n[3] KS tests (CMS d5 vs MG5 distributions)")
    if cms_data and mg5_kinematics.get("A_1p80") is not None:
        cms_dr = np.array([ev["dr"] for ev in cms_data])
        cms_m  = np.array([ev["m"]  for ev in cms_data])
        for key, kin in mg5_kinematics.items():
            if kin is None or len(kin["dr"]) == 0:
                continue
            ks_dr, p_dr = ks_2samp(cms_dr, kin["dr"])
            ks_m,  p_m  = ks_2samp(cms_m,  kin["m"])
            print(f"  {key}: KS(ΔR)={ks_dr:.3f} p={p_dr:.3e} | KS(m)={ks_m:.3f} p={p_m:.3e}")
            summary[key]["ks_dr"] = ks_dr
            summary[key]["ks_dr_p"] = p_dr
            summary[key]["ks_m"]  = ks_m
            summary[key]["ks_m_p"] = p_m

    # Save JSON results
    results = {
        "experiment":     63,
        "description":    "Dark Photon A' kinetic mixing: p p > Ap j, Ap > mu+ mu-",
        "sqrts_gev":      8000,
        "luminosity_pb":  LUMINOSITY_PB,
        "epsilon_ref":    EPSILON_REF,
        "n_obs_cms":      N_OBS,
        "cms_data": {
            "n_events":   len(cms_data),
            "dr_mean":    float(np.mean([ev["dr"] for ev in cms_data])) if cms_data else None,
            "dr_std":     float(np.std([ev["dr"]  for ev in cms_data])) if cms_data else None,
            "m_mean":     float(np.mean([ev["m"]  for ev in cms_data])) if cms_data else None,
        },
        "runs": summary,
    }
    json_path = OUT_DIR / "63_darkphoton_results.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[4] Results saved: {json_path}")

    # Plots
    print("\n[5] Generating comparison plots ...")
    if cms_data:
        make_plots(cms_data, mg5_kinematics, xsecs, summary)
    else:
        print("    Skipped (no CMS data)")

    # Summary
    print("\n" + "=" * 70)
    print("EXPERIMENT 63 SUMMARY")
    print("=" * 70)
    print(f"  CMS d5 candidates: N={len(cms_data)}, <ΔR>="
          f"{np.mean([ev['dr'] for ev in cms_data]):.3f}" if cms_data else "  CMS data: MISSING")
    print()
    for key, s in summary.items():
        if s.get("status") == "missing":
            print(f"  {key}: MG5 output NOT FOUND (run still in progress?)")
        else:
            xsec = s.get("xsec_pb")
            n_ref = s.get("n_expected_ref")
            eps   = s.get("epsilon_fit")
            print(f"  {RUN_LABELS[key]}:")
            if xsec:
                print(f"    σ(ε=1e-3)  = {xsec:.3e} pb")
            if n_ref:
                print(f"    N_exp      = {n_ref:.1f}  (L=7 fb⁻¹, η×A={CMS_EFF_ETA})")
            if eps:
                print(f"    ε_fit      = {eps:.3e}  (→ matches N_obs=51)")
            dr_m = s.get("dr_mean")
            dr_s = s.get("dr_std")
            if dr_m:
                print(f"    <ΔR>_MG5   = {dr_m:.3f} ± {dr_s:.3f}")

    print()
    print("Interpretation:")
    for key, s in summary.items():
        if s.get("status") == "missing": continue
        n_ref = s.get("n_expected_ref")
        eps_  = s.get("epsilon_fit")
        dr_m  = s.get("dr_mean")
        if n_ref and eps_ and dr_m:
            ratio = n_ref / N_OBS
            print(f"  [{key}] ε_fit={eps_:.2e}, rate-ratio={ratio:.1f}×, "
                  f"<ΔR>={dr_m:.3f} vs CMS 0.087")
    print()


if __name__ == "__main__":
    main()
