"""
Experiment 62 companion analysis
─────────────────────────────────
Parses MG5 LHE output for:
  - 62_sm_dimuon_j_8tev  (SM null hypothesis)
  - 62_mirror_fermion_2gev  (MirrorFermion, MXm=2 GeV)
  - 62_mirror_fermion_1gev  (MirrorFermion, MXm=1 GeV)

Computes per-event ΔR(μμ), m_inv, pT kinematics.
Overlays against the 51-event clean d5 population from 76h-B.

Outputs:
  results/62_d5_comparison.json
  results/62_d5_comparison.png
"""

import xml.etree.ElementTree as ET
import json, math, pathlib, gzip, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

BASE = pathlib.Path(__file__).parent.parent  # ukftphys root
D5_JSON = (pathlib.Path(__file__).parent.parent.parent /
           "noosphere/apps/hep-explorer/tools/76h_b_kinematics.json")
RESULTS = BASE / "results"
RESULTS.mkdir(exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────────
def delta_r(eta1, phi1, eta2, phi2):
    deta = eta1 - eta2
    dphi = phi1 - phi2
    while dphi >  math.pi: dphi -= 2*math.pi
    while dphi < -math.pi: dphi += 2*math.pi
    return math.sqrt(deta**2 + dphi**2)

def four_momentum(px, py, pz, e):
    return (px, py, pz, e)

def inv_mass(p1, p2):
    """Invariant mass of two four-vectors (E, px, py, pz)."""
    e   = p1[3] + p2[3]
    px  = p1[0] + p2[0]
    py  = p1[1] + p2[1]
    pz  = p1[2] + p2[2]
    m2  = e**2 - px**2 - py**2 - pz**2
    return math.sqrt(max(m2, 0))

def pt_eta_phi(px, py, pz):
    pt  = math.sqrt(px**2 + py**2)
    eta = math.atanh(pz / math.sqrt(px**2 + py**2 + pz**2 + 1e-20))
    phi = math.atan2(py, px)
    return pt, eta, phi

def parse_lhe(lhe_path):
    """Parse a MG5 LHE file (plain or .gz) and return per-event muon pairs."""
    events = []
    if not os.path.exists(lhe_path):
        return None  # file not found

    in_event = False
    current_particles = []

    opener = gzip.open if lhe_path.endswith(".gz") else open
    with opener(lhe_path, 'rt', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if line.startswith("<event>"):
                in_event = True
                current_particles = []
            elif line.startswith("</event>"):
                in_event = False
                # extract muons
                muons = [(pid, px, py, pz, e, status)
                         for (pid, px, py, pz, e, status) in current_particles
                         if abs(pid) == 13 and status == 1]
                if len(muons) >= 2:
                    # sort by pT descending
                    muons_sorted = sorted(muons,
                                          key=lambda m: -math.sqrt(m[1]**2 + m[2]**2))
                    m1, m2 = muons_sorted[0], muons_sorted[1]
                    p1 = (m1[1], m1[2], m1[3], m1[4])
                    p2 = (m2[1], m2[2], m2[3], m2[4])
                    pt1, eta1, phi1 = pt_eta_phi(*p1[:3])
                    pt2, eta2, phi2 = pt_eta_phi(*p2[:3])
                    m_inv = inv_mass(p1, p2)
                    dR    = delta_r(eta1, phi1, eta2, phi2)
                    asym  = (pt1 - pt2) / (pt1 + pt2 + 1e-20)
                    events.append({
                        "m_inv": m_inv,
                        "dR": dR,
                        "pt_lead": pt1, "eta_lead": eta1, "phi_lead": phi1,
                        "pt_sub": pt2, "eta_sub": eta2, "phi_sub": phi2,
                        "HT_dimuon": pt1 + pt2,
                        "asymmetry": asym,
                        "charge_product": -1 if m1[0] != m2[0] else 1,
                    })
                current_particles = []
            elif in_event:
                parts = line.split()
                if len(parts) >= 10:
                    try:
                        pid    = int(parts[0])
                        status = int(parts[1])
                        px     = float(parts[6])
                        py     = float(parts[7])
                        pz     = float(parts[8])
                        e      = float(parts[9])
                        current_particles.append((pid, px, py, pz, e, status))
                    except ValueError:
                        pass

    print(f"  Parsed: {len(events)} events with dimuon pairs from {lhe_path}")
    return events

# ── locate LHE files ─────────────────────────────────────────────────────────
def find_lhe(run_dir):
    """Find the LHE event file in a MG5 run directory."""
    run_dir = pathlib.Path(run_dir)
    candidates = list(run_dir.rglob("unweighted_events.lhe")) + \
                 list(run_dir.rglob("unweighted_events.lhe.gz"))
    if candidates:
        return str(candidates[0])
    # also check events/
    for p in run_dir.rglob("*.lhe"):
        return str(p)
    return None

sm_dir   = BASE / "experiments/62_sm_dimuon_j_8tev"
mf2_dir  = BASE / "experiments/62_mirror_fermion_2gev"
mf1_dir  = BASE / "experiments/62_mirror_fermion_1gev"

print("Locating LHE output files...")
sm_lhe  = find_lhe(sm_dir)
mf2_lhe = find_lhe(mf2_dir)
mf1_lhe = find_lhe(mf1_dir)
print(f"  SM:    {sm_lhe}")
print(f"  MF2:   {mf2_lhe}")
print(f"  MF1:   {mf1_lhe}")

# ── load d5 data ─────────────────────────────────────────────────────────────
print("\nLoading 76h-B d5 kinematic data...")
with open(D5_JSON) as f:
    d5_data = json.load(f)

d5_records = [r for r in d5_data["records"]
              if not r.get("sm_filtered", True) and r.get("dR") is not None]
print(f"  clean d5 events with kinematics: {len(d5_records)}")

d5_m   = np.array([r["m_inv"] for r in d5_records])
d5_dR  = np.array([r["dR"]    for r in d5_records])
d5_pt1 = np.array([r["pt_lead"] for r in d5_records])
d5_HT  = np.array([r["HT_dimuon"] for r in d5_records])
d5_asym = np.array([r["asymmetry"] for r in d5_records])

# ── cross-section extraction from MG5 log ────────────────────────────────────
def read_xsec(run_dir):
    """Try to extract cross-section from MG5 run output."""
    run_dir = pathlib.Path(run_dir)
    for logf in run_dir.rglob("*.log"):
        with open(logf) as f:
            for line in f:
                if "Cross-section" in line or "cross section" in line.lower():
                    parts = line.split()
                    for i, p in enumerate(parts):
                        try:
                            xsec = float(p)
                            unit = parts[i+1] if i+1 < len(parts) else "?"
                            return xsec, unit, line.strip()
                        except (ValueError, IndexError):
                            pass
    # fallback: check crossx.html or Banner
    for f in run_dir.rglob("crossx.html"):
        import re
        with open(f) as fh:
            txt = fh.read()
        m = re.search(r'([\d\.Ee\+\-]+)\s*\+\/\-\s*([\d\.Ee\+\-]+)\s*(pb|fb)', txt)
        if m:
            return float(m.group(1)), m.group(3), f"from {f.name}"
    return None, None, "not found"

# ── parse LHE events ─────────────────────────────────────────────────────────
sm_events  = parse_lhe(sm_lhe)  if sm_lhe  else None
mf2_events = parse_lhe(mf2_lhe) if mf2_lhe else None
mf1_events = parse_lhe(mf1_lhe) if mf1_lhe else None

# ── expected event counts (CMS Run2012C luminosity) ──────────────────────────
# CMS Run 2012C: integrated luminosity ~ 7.0 fb^-1
# (Run2012B+C combined ~ 12 fb^-1; Run2012C alone ~ 7 fb^-1 per CMS PAS)
LUMI_2012C = 7.0e3  # pb^-1

def expected_counts(xsec_pb, lumi_pb_inv, n_gen, n_pass_cuts):
    """N_exp = xsec * lumi * (n_pass/n_gen) acceptance"""
    if xsec_pb is None or n_gen == 0:
        return None
    acceptance = n_pass_cuts / n_gen
    return xsec_pb * lumi_pb_inv * acceptance

# ── summary statistics ───────────────────────────────────────────────────────
def arr_ev(ev_list, key):
    return np.array([e[key] for e in ev_list]) if ev_list else np.array([])

def print_summary(label, evts):
    if not evts:
        print(f"  {label}: NO DATA (MG5 not run yet)")
        return
    m   = arr_ev(evts, "m_inv")
    dR  = arr_ev(evts, "dR")
    pt1 = arr_ev(evts, "pt_lead")
    print(f"  {label}: N={len(evts)}")
    if len(m):
        print(f"    m_inv:  {m.mean():.2f} ± {m.std():.2f}  "
              f"median={np.median(m):.2f}")
    if len(dR):
        print(f"    ΔR:     {dR.mean():.3f} ± {dR.std():.3f}  "
              f"median={np.median(dR):.3f}")
    if len(pt1):
        print(f"    pT_lead:{pt1.mean():.1f} ± {pt1.std():.1f}")

print("\n── Kinematic summaries ─────────────────────────────────────────────")
print_summary("SM (p p > mu+ mu- j)", sm_events)
print_summary("MirrorFermion MXm=2 GeV", mf2_events)
print_summary("MirrorFermion MXm=1 GeV", mf1_events)
print(f"\n  CMS data (clean d5): N={len(d5_records)}")
print(f"    m_inv:  {d5_m.mean():.2f} ± {d5_m.std():.2f}  "
      f"median={np.median(d5_m):.2f}")
print(f"    ΔR:     {d5_dR.mean():.3f} ± {d5_dR.std():.3f}  "
      f"median={np.median(d5_dR):.3f}")

# ── theoretical ΔR prediction ─────────────────────────────────────────────────
print("\n── Theoretical ΔR(m_inv) at <pT>=39 GeV ─────────────────")
m_vals = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
for m in m_vals:
    dR_pred = 2 * m / 39.0
    print(f"  m={m:.1f} GeV → ΔR_theory = {dR_pred:.3f}")

# ── plot ──────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10))
fig.suptitle("Exp 62: d5 Mirror Fermion — CMS Data vs MG5 Predictions (√s=8 TeV)",
             fontsize=13, fontweight="bold")
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.40, wspace=0.32)

bins_m  = np.linspace(0, 3.5, 22)
bins_dR = np.linspace(0, 0.5, 26)
bins_pt = np.linspace(0, 60, 26)

# ── utility: normalize to data count ─────────────────────────────────────────
def norm_hist(ax, data, bins, label, color, alpha=0.6, n_target=None, style="step"):
    if data is None or len(data) == 0:
        return
    h, e = np.histogram(data, bins=bins)
    scale = (n_target / h.sum()) if (n_target and h.sum() > 0) else 1.0
    cx = 0.5*(e[:-1] + e[1:])
    if style == "step":
        ax.step(e[:-1], h * scale, where="post", color=color, alpha=alpha,
                label=label, linewidth=1.5)
    else:
        ax.bar(cx, h * scale, width=e[1]-e[0], color=color, alpha=alpha,
               label=label, align="center")
    return h.sum()

n_d5 = len(d5_records)

# Panel 0: m_inv
ax = fig.add_subplot(gs[0, 0])
norm_hist(ax, d5_m, bins_m, f"CMS clean d5 (N={n_d5})", "red", style="bar")
sm_m  = arr_ev(sm_events, "m_inv")  if sm_events  else np.array([])
mf2_m = arr_ev(mf2_events, "m_inv") if mf2_events else np.array([])
mf1_m = arr_ev(mf1_events, "m_inv") if mf1_events else np.array([])
norm_hist(ax, sm_m,  bins_m, "SM DY+j (normalized)", "steelblue", n_target=n_d5)
norm_hist(ax, mf2_m, bins_m, "MirrorF MXm=2 GeV", "green", n_target=n_d5)
norm_hist(ax, mf1_m, bins_m, "MirrorF MXm=1 GeV", "purple", n_target=n_d5)
ax.set_xlabel("m_inv (GeV)")
ax.set_ylabel("events (normalized)")
ax.set_title("Dimuon invariant mass")
ax.legend(fontsize=7)

# Panel 1: ΔR
ax = fig.add_subplot(gs[0, 1])
norm_hist(ax, d5_dR, bins_dR, f"CMS clean d5 (N={n_d5})", "red", style="bar")
sm_dR  = arr_ev(sm_events,  "dR") if sm_events  else np.array([])
mf2_dR = arr_ev(mf2_events, "dR") if mf2_events else np.array([])
norm_hist(ax, sm_dR,  bins_dR, "SM DY+j", "steelblue", n_target=n_d5)
norm_hist(ax, mf2_dR, bins_dR, "MirrorF MXm=2 GeV", "green", n_target=n_d5)
ax.axvline(0.114, color="red", ls="--", lw=1.5, label="data mean 0.114")
ax.set_xlabel("ΔR(μ,μ)")
ax.set_title("ΔR(μ,μ) — collimation key diagnostic")
ax.legend(fontsize=7)

# Panel 2: pT_lead
ax = fig.add_subplot(gs[0, 2])
norm_hist(ax, d5_pt1, bins_pt, f"CMS clean d5", "red", style="bar")
sm_pt  = arr_ev(sm_events,  "pt_lead") if sm_events  else np.array([])
mf2_pt = arr_ev(mf2_events, "pt_lead") if mf2_events else np.array([])
norm_hist(ax, sm_pt,  bins_pt, "SM DY+j", "steelblue", n_target=n_d5)
norm_hist(ax, mf2_pt, bins_pt, "MirrorF MXm=2 GeV", "green", n_target=n_d5)
ax.set_xlabel("pT_lead (GeV)")
ax.set_title("Leading muon pT")
ax.legend(fontsize=7)

# Panel 3: ΔR vs m_inv scatter (data + theoretical curve)
ax = fig.add_subplot(gs[1, 0])
m_theory = np.linspace(0.2, 3.5, 200)
for pT_sys in [20, 30, 40, 50]:
    dR_theory = 2 * m_theory / pT_sys
    ls = "-" if pT_sys == 39 else "--"
    lw = 2 if pT_sys == 39 else 1
    ax.plot(m_theory, dR_theory, ls=ls, lw=lw, alpha=0.7,
            label=f"2m/pT at pT={pT_sys}")
ax.scatter(d5_m, d5_dR, c="red", s=20, alpha=0.7, zorder=5, label="CMS data")
if sm_events:
    ax.scatter(sm_m, sm_dR, c="steelblue", s=5, alpha=0.3, label="SM DY+j")
if mf2_events:
    ax.scatter(mf2_m, mf2_dR, c="green", s=5, alpha=0.3, label="MF 2 GeV")
# Star event
star = next((r for r in d5_records if r.get("is_star")), None)
if star:
    ax.scatter([star["m_inv"]], [star["dR"]], s=200, marker="*", color="gold",
               zorder=10, label=f"star (m={star['m_inv']:.2f})")
ax.set_xlim(0, 3.5); ax.set_ylim(0, 0.5)
ax.set_xlabel("m_inv (GeV)")
ax.set_ylabel("ΔR(μ,μ)")
ax.set_title("m_inv vs ΔR: data + theory curves")
ax.legend(fontsize=6)

# Panel 4: pT_lead vs m_inv (check for kinematic regime)
ax = fig.add_subplot(gs[1, 1])
ax.scatter(d5_m, d5_pt1, c="red", s=20, alpha=0.7, label="CMS data")
if sm_events:
    ax.scatter(sm_m, sm_pt, c="steelblue", s=5, alpha=0.3, label="SM DY+j")
ax.set_xlabel("m_inv (GeV)")
ax.set_ylabel("pT_lead (GeV)")
ax.set_title("pT_lead vs m_inv")
ax.legend(fontsize=7)

# Panel 5: HT_dimuon distribution
ax = fig.add_subplot(gs[1, 2])
bins_ht = np.linspace(10, 80, 22)
norm_hist(ax, d5_HT, bins_ht, f"CMS clean d5", "red", style="bar")
sm_ht = arr_ev(sm_events, "HT_dimuon") if sm_events else np.array([])
norm_hist(ax, sm_ht, bins_ht, "SM DY+j", "steelblue", n_target=n_d5)
ax.set_xlabel("HT(μμ) = pT1+pT2 (GeV)")
ax.set_title("Dimuon scalar HT")
ax.legend(fontsize=7)

plt.savefig(RESULTS / "62_d5_comparison.png", dpi=120, bbox_inches="tight")
print(f"\nSaved: results/62_d5_comparison.png")

# ── JSON output ───────────────────────────────────────────────────────────────
def summary_dict(evts, label):
    if not evts:
        return {"label": label, "n_events": 0, "status": "MG5 not run yet"}
    m  = arr_ev(evts, "m_inv")
    dR = arr_ev(evts, "dR")
    pt = arr_ev(evts, "pt_lead")
    return {
        "label": label,
        "n_events": len(evts),
        "m_inv_mean": float(m.mean()) if len(m) else None,
        "m_inv_std":  float(m.std())  if len(m) else None,
        "dR_mean":    float(dR.mean()) if len(dR) else None,
        "dR_std":     float(dR.std())  if len(dR) else None,
        "pt_lead_mean": float(pt.mean()) if len(pt) else None,
    }

out = {
    "experiment": "62",
    "description": "Low-mass dimuon MG5 comparison vs d5 population",
    "cms_data": {
        "n_clean_d5": len(d5_records),
        "m_inv_mean": float(d5_m.mean()),
        "m_inv_median": float(np.median(d5_m)),
        "dR_mean": float(d5_dR.mean()),
        "dR_std": float(d5_dR.std()),
        "pt_lead_mean": float(d5_pt1.mean()),
        "HT_dimuon_mean": float(d5_HT.mean()),
        "source": "76h_b_kinematics.json",
    },
    "mg5_sm":  summary_dict(sm_events,  "p p > mu+ mu- j (SM, 8 TeV)"),
    "mg5_mf2": summary_dict(mf2_events, "p p > xm xm~ MXm=2 GeV (8 TeV)"),
    "mg5_mf1": summary_dict(mf1_events, "p p > xm xm~ MXm=1 GeV (8 TeV)"),
    "theoretical_dR": {
        f"m{m:.1f}_pT39": float(2*m/39)
        for m in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    },
    "key_diagnostic": (
        "If SM DY+j ΔR distribution peaks at ~0.11 matching data → SM explanation. "
        "If SM gives broad/large ΔR and data is narrowly peaked at 0.11 → BSM signal. "
        "MirrorFermion pair production (QCD) at MXm=1-2 GeV gives production "
        "cross-section for rate comparison with 51 observed events at L~7 fb^-1."
    ),
    "dR_boosted_formula": "ΔR ≈ 2m/pT  (exact for back-to-back decay in boosted frame)",
    "status": "MG5 comparison pending — run 62_d5_lowmass_dimuon.mg5 first"
              if not sm_events else "MG5 output loaded and analyzed",
}

with open(RESULTS / "62_d5_comparison.json", "w") as f:
    json.dump(out, f, indent=2)
print("Saved: results/62_d5_comparison.json")

# ── final print ───────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("EXP 62 ANALYSIS SUMMARY")
print("="*60)
print(f"CMS clean d5 population: N={len(d5_records)}, "
      f"<ΔR>={d5_dR.mean():.3f}, <m>={d5_m.mean():.2f} GeV")
print(f"Theoretical <ΔR(2 GeV, 39 GeV)> = {2*2.0/39:.3f}")
if sm_events:
    print(f"SM p p > mu mu j:  N={len(sm_events)}, "
          f"<ΔR>={arr_ev(sm_events,'dR').mean():.3f}")
else:
    print("SM p p > mu mu j:  NOT YET RUN")
if mf2_events:
    print(f"MirrorF MXm=2GeV:  N={len(mf2_events)}")
else:
    print("MirrorF MXm=2GeV:  NOT YET RUN")
print("\nNext: run 62_d5_lowmass_dimuon.mg5 in MG5_aMC, then re-run this script.")
