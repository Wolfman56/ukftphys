#!/usr/bin/env python3
"""
Phase 34 (v2) — Isolation and Impact Parameter Analysis (corrected)
Run2012B NanoAOD (26.1M events)

Key physics: NanoAOD fills pfRelIso03_all = -999 for muons that are
StandAlone-only or do not have valid PF reconstruction. This is
itself a discriminant: b -> mu soft decays produce non-PF muons
(iso = -999), while prompt hard-scatter decays produce fully
reconstructed global/PF muons with valid iso ≥ 0.

Analysis strategy:
  1. Flag muons with valid iso: iso > -998 (real PF muon)
  2. Flag muons with valid dxy: |dxy| < 999 cm
  3. For each event passing our C3 / C4 / C5 cuts, report:
       - nMuon_valid_iso (both groups combined)
       - Fraction of events where ALL group muons have valid iso
       - For valid-iso muons: iso distribution and dxy distribution
  4. Define C6 cuts: all-group muons valid AND iso < 0.25
"""
import uproot
import awkward as ak
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json, os

BASE = "/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer"
ROOT_FILE = f"{BASE}/tools/data/Run2012B_DoubleMuParked.root"
OUT_FIG   = f"{BASE}/figures/phase34_isolation_distributions.png"
OUT_JSON  = f"{BASE}/results/phase34_isolation_stats.json"
os.makedirs(f"{BASE}/figures", exist_ok=True)
os.makedirs(f"{BASE}/results", exist_ok=True)

FILL = -999.0     # NanoAOD fill value
FILL_TOL = 1.0    # valid if value > FILL + FILL_TOL = -998

# ── Load ─────────────────────────────────────────────────────────────────
print("Loading Run2012B NanoAOD ...")
t = uproot.open(ROOT_FILE)["Events"]
ev = t.arrays(
    ["nMuon","Muon_pt","Muon_eta","Muon_phi","Muon_charge",
     "Muon_pfRelIso03_all","Muon_dxy","Muon_dxyErr","Muon_dz","Muon_dzErr"],
    library="ak"
)
N_total = len(ev)
print(f"  Total events: {N_total:,}")

# ── C0: nMuon >= 7 ────────────────────────────────────────────────────────
nmu    = ak.to_numpy(ev["nMuon"])
mask0  = nmu >= 7
ev7    = ev[mask0]
nmu7   = nmu[mask0]
print(f"C0 nMuon>=7: {ak.sum(mask0):,}")

# ── Geometry cuts on nMuon>=7 subset ─────────────────────────────────────
phi_  = ev7["Muon_phi"]
nA    = ak.to_numpy(ak.sum(phi_ > 0, axis=1))
nB    = ak.to_numpy(ak.sum(phi_ < 0, axis=1))

mean_phiA = ak.to_numpy(ak.mean(phi_[phi_ > 0], axis=1))
mean_phiB = ak.to_numpy(ak.mean(phi_[phi_ < 0], axis=1))
ok_AB     = (nA >= 1) & (nB >= 1)

dphi_AB = np.where(ok_AB,
    np.abs(mean_phiA - mean_phiB),
    0.0)
dphi_AB = np.where(dphi_AB > np.pi, 2*np.pi - dphi_AB, dphi_AB)

# C1
mask1 = ok_AB & (np.degrees(dphi_AB) > 150.0)
print(f"C1 Δφ(A,B)>150°: {np.sum(mask1):,}")

# C2: phi spread of group B
phi_B_all = phi_[phi_ < 0]
phiB_max  = ak.to_numpy(ak.max(phi_B_all, axis=1))
phiB_min  = ak.to_numpy(ak.min(phi_B_all, axis=1))
dph_dense = phiB_max - phiB_min
mask2 = mask1 & (dph_dense < 0.10)
print(f"C2 Δφ_dense<0.10: {np.sum(mask2):,}")

# C3: nB = 5
mask3 = mask2 & (nB == 5)
print(f"C3 nB=5 exact: {np.sum(mask3):,}")

# ── Per-event invariant masses + isolation for C3 survivors ──────────────
import math

def inv_mass(pts, etas, phis):
    """Massless 4-vector sum invariant mass."""
    px = pts * np.cos(phis); py = pts * np.sin(phis)
    pz = pts * np.sinh(etas); E  = pts * np.cosh(etas)
    m2 = E.sum()**2 - px.sum()**2 - py.sum()**2 - pz.sum()**2
    return math.sqrt(max(m2, 0.0))

idx_c3 = np.where(mask3)[0]
print(f"Computing per-event properties for {len(idx_c3):,} C3 events ...")

records = []  # one dict per surviving event

for iev in idx_c3:
    nm = int(nmu7[iev])

    pt_i   = np.array(ev7["Muon_pt"][iev])[:nm].astype(float)
    eta_i  = np.array(ev7["Muon_eta"][iev])[:nm].astype(float)
    phi_i  = np.array(ev7["Muon_phi"][iev])[:nm].astype(float)
    iso_i  = np.array(ev7["Muon_pfRelIso03_all"][iev])[:nm].astype(float)
    dxy_i  = np.array(ev7["Muon_dxy"][iev])[:nm].astype(float)
    dxyE_i = np.array(ev7["Muon_dxyErr"][iev])[:nm].astype(float)
    dz_i   = np.array(ev7["Muon_dz"][iev])[:nm].astype(float)
    dzE_i  = np.array(ev7["Muon_dzErr"][iev])[:nm].astype(float)

    idxA = np.where(phi_i > 0)[0]
    idxB = np.where(phi_i < 0)[0]
    if len(idxA) == 0 or len(idxB) == 0:
        continue

    mA = inv_mass(pt_i[idxA], eta_i[idxA], phi_i[idxA])
    mB = inv_mass(pt_i[idxB], eta_i[idxB], phi_i[idxB])
    ratio = mB / mA if mA > 0 else 0.0

    # Valid iso: iso > FILL + FILL_TOL
    iso_A  = iso_i[idxA];  valid_A = iso_A > (FILL + FILL_TOL)
    iso_B  = iso_i[idxB];  valid_B = iso_B > (FILL + FILL_TOL)
    n_valid_A = int(np.sum(valid_A))
    n_valid_B = int(np.sum(valid_B))
    all_valid_A = bool(np.all(valid_A))
    all_valid_B = bool(np.all(valid_B))
    both_all_valid = all_valid_A and all_valid_B

    # Tight iso: all valid AND iso < 0.25
    tight_A = all_valid_A and bool(np.all(iso_A[valid_A] < 0.25))
    tight_B = all_valid_B and bool(np.all(iso_B[valid_B] < 0.25))
    both_tight = tight_A and tight_B

    # dxy for valid muons
    dxy_A_valid  = dxy_i[idxA][valid_A]
    dxy_B_valid  = dxy_i[idxB][valid_B]
    dxyE_A_valid = dxyE_i[idxA][valid_A]
    dxyE_B_valid = dxyE_i[idxB][valid_B]

    with np.errstate(divide='ignore', invalid='ignore'):
        sig_A = np.abs(dxy_A_valid) / np.where(dxyE_A_valid > 0, dxyE_A_valid, 1e-9) \
                if len(dxy_A_valid) else np.array([])
        sig_B = np.abs(dxy_B_valid) / np.where(dxyE_B_valid > 0, dxyE_B_valid, 1e-9) \
                if len(dxy_B_valid) else np.array([])

    prompt_A = (len(sig_A) > 0) and bool(np.all(sig_A < 3.0))
    prompt_B = (len(sig_B) > 0) and bool(np.all(sig_B < 3.0))
    both_prompt = prompt_A and prompt_B

    records.append({
        "mA": mA, "mB": mB, "ratio": ratio,
        "n_valid_iso_A": n_valid_A, "n_valid_iso_B": n_valid_B,
        "nA": len(idxA), "nB": len(idxB),
        "all_valid_iso": int(both_all_valid),
        "tight_iso": int(both_tight),
        "prompt_dxy": int(both_prompt),
        "iso_A_vals": iso_A[valid_A].tolist() if n_valid_A > 0 else [],
        "iso_B_vals": iso_B[valid_B].tolist() if n_valid_B > 0 else [],
        "dxy_A_sig":  sig_A.tolist() if len(sig_A) else [],
        "dxy_B_sig":  sig_B.tolist() if len(sig_B) else [],
        "abs_dxy_A":  np.abs(dxy_A_valid).tolist() if len(dxy_A_valid) else [],
        "abs_dxy_B":  np.abs(dxy_B_valid).tolist() if len(dxy_B_valid) else [],
    })

print(f"  Computed {len(records):,} C3 records")

# ── Build arrays from records ─────────────────────────────────────────────
ratio_arr     = np.array([r["ratio"]         for r in records])
all_valid_arr = np.array([r["all_valid_iso"]  for r in records], dtype=bool)
tight_arr     = np.array([r["tight_iso"]      for r in records], dtype=bool)
prompt_arr    = np.array([r["prompt_dxy"]     for r in records], dtype=bool)
nvalid_A_arr  = np.array([r["n_valid_iso_A"]  for r in records])
nvalid_B_arr  = np.array([r["n_valid_iso_B"]  for r in records])

mask_c4 = ratio_arr > 1.0
mask_c5 = ratio_arr > 6.0

print(f"\nCut-flow summary:")
print(f"  C3 nB=5:         {len(records):>6,}")
print(f"  C4 ratio>1:      {np.sum(mask_c4):>6,}")
print(f"  C5 ratio>6:      {np.sum(mask_c5):>6,}")
print()
for lbl, msk in [("C3", np.ones(len(records), dtype=bool)),
                  ("C4 (ratio>1)", mask_c4),
                  ("C5 (ratio>6)", mask_c5)]:
    n = np.sum(msk)
    if n == 0:
        continue
    nv = np.sum(all_valid_arr[msk])
    nt = np.sum(tight_arr[msk])
    np_ = np.sum(prompt_arr[msk])
    # median valid iso per group (flatten across events with at least 1 valid muon)
    iso_A_flat = []
    iso_B_flat = []
    dxy_sig_flat = []
    for r in [records[i] for i in np.where(msk)[0]]:
        iso_A_flat.extend(r["iso_A_vals"])
        iso_B_flat.extend(r["iso_B_vals"])
        dxy_sig_flat.extend(r["dxy_A_sig"])
        dxy_sig_flat.extend(r["dxy_B_sig"])
    ia = np.array(iso_A_flat);  ib = np.array(iso_B_flat)
    ds = np.array(dxy_sig_flat)
    print(f"  {lbl} (N={n}):")
    print(f"    Events with ALL valid iso:   {nv:>5,}  ({100*nv/n:.1f}%)")
    print(f"    Events with tight iso (<0.25):{nt:>5,}  ({100*nt/n:.1f}%)")
    print(f"    Events with prompt dxy (σ<3): {np_:>5,}  ({100*np_/n:.1f}%)")
    if len(ia):
        print(f"    Group A iso: median={np.median(ia):.3f}  p95={np.percentile(ia,95):.3f}  N_muon={len(ia)}")
    if len(ib):
        print(f"    Group B iso: median={np.median(ib):.3f}  p95={np.percentile(ib,95):.3f}  N_muon={len(ib)}")
    if len(ds):
        print(f"    |dxy|/σ: median={np.median(ds):.2f}  p75={np.percentile(ds,75):.2f}  p95={np.percentile(ds,95):.2f}  N_muon={len(ds)}")
    print()

# ── Save stats ────────────────────────────────────────────────────────────
def stage_stats(msk, lbl):
    n = int(np.sum(msk))
    if n == 0:
        return {"label": lbl, "n": 0}
    nv = int(np.sum(all_valid_arr[msk]))
    nt = int(np.sum(tight_arr[msk]))
    np_v = int(np.sum(prompt_arr[msk]))
    iso_A_flat = [v for r in [records[i] for i in np.where(msk)[0]] for v in r["iso_A_vals"]]
    iso_B_flat = [v for r in [records[i] for i in np.where(msk)[0]] for v in r["iso_B_vals"]]
    dxy_s_flat = [v for r in [records[i] for i in np.where(msk)[0]]
                  for v in r["dxy_A_sig"] + r["dxy_B_sig"]]
    ia = np.array(iso_A_flat); ib = np.array(iso_B_flat); ds = np.array(dxy_s_flat)
    stats = {"label": lbl, "n": n,
             "n_all_valid_iso": nv, "frac_all_valid_iso": round(nv/n, 4),
             "n_tight_iso": nt,    "frac_tight_iso": round(nt/n, 4),
             "n_prompt_dxy": np_v, "frac_prompt_dxy": round(np_v/n, 4)}
    if len(ia): stats["iso_A"] = {"med": round(float(np.median(ia)),4),
                                   "p95": round(float(np.percentile(ia,95)),4)}
    if len(ib): stats["iso_B"] = {"med": round(float(np.median(ib)),4),
                                   "p95": round(float(np.percentile(ib,95)),4)}
    if len(ds): stats["dxy_sig"] = {"med": round(float(np.median(ds)),3),
                                     "p75": round(float(np.percentile(ds,75)),3),
                                     "p95": round(float(np.percentile(ds,95)),3)}
    return stats

out = {
    "C3": stage_stats(np.ones(len(records), dtype=bool), "C3 nB=5"),
    "C4": stage_stats(mask_c4, "C4 ratio>1"),
    "C5": stage_stats(mask_c5, "C5 ratio>6"),
    "combined_rejection_C4_tight_iso": int(np.sum(mask_c4 & tight_arr)),
    "combined_rejection_C4_prompt_dxy": int(np.sum(mask_c4 & prompt_arr)),
    "combined_rejection_C4_tight_OR_prompt": int(np.sum(mask_c4 & (tight_arr | prompt_arr))),
}
with open(OUT_JSON, "w") as fp:
    json.dump(out, fp, indent=2)
print(f"Stats saved: {OUT_JSON}")

# ── Figures ───────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(14, 8))

stage_data = [
    ("C3: nB=5", np.ones(len(records), dtype=bool)),
    ("C4: ratio>1", mask_c4),
    ("C5: ratio>6", mask_c5),
]
COLS = ["#1f77b4", "#d95f02", "#2ca02c"]

for col, (lbl, msk) in enumerate(stage_data):
    idxs = np.where(msk)[0]
    iso_A_flat = [v for r in [records[i] for i in idxs] for v in r["iso_A_vals"]]
    iso_B_flat = [v for r in [records[i] for i in idxs] for v in r["iso_B_vals"]]
    dxy_sig_all= [v for r in [records[i] for i in idxs] for v in r["dxy_A_sig"]+r["dxy_B_sig"]]

    n = len(idxs)
    ax0 = axes[0, col]
    ax1 = axes[1, col]

    # Row 0: Group B iso (more muons)
    arr = np.array(iso_B_flat)
    if len(arr):
        arr_c = np.clip(arr, 0, 3)
        ax0.hist(arr_c, bins=40, range=(0, 3), color=COLS[col], alpha=0.75, density=True)
        ax0.axvline(0.25, color="red",   ls="--", lw=1.5, label="tight 0.25")
        ax0.axvline(0.50, color="darkorange", ls=":", lw=1.5, label="medium 0.50")
    ax0.set_title(f"{lbl} (N={n:,})\nGroup B pfRelIso03 (valid muons only)", fontsize=8)
    ax0.set_xlabel("pfRelIso03", fontsize=8)
    ax0.legend(fontsize=7, framealpha=0.5)
    ax0.spines["top"].set_visible(False)
    ax0.spines["right"].set_visible(False)

    # Row 1: dxy significance
    ds = np.array(dxy_sig_all)
    if len(ds):
        ds_c = np.clip(ds, 0, 20)
        ax1.hist(ds_c, bins=40, range=(0, 20), color=COLS[col], alpha=0.75, density=True)
        ax1.axvline(3.0, color="red", ls="--", lw=1.5, label="prompt |dxy|/σ<3")
        ax1.axvline(5.0, color="darkorange", ls=":", lw=1.5, label="|dxy|/σ<5")
    ax1.set_title(f"{lbl} (N={n:,})\n|dxy|/σ_dxy (valid muons only)", fontsize=8)
    ax1.set_xlabel("|dxy| / σ_dxy", fontsize=8)
    ax1.legend(fontsize=7, framealpha=0.5)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

fig.suptitle("Run2012B NanoAOD — Isolation & Impact Parameter at Cut Stages\n"
             "(valid PF muons only; NanoAOD fill=−999 excluded; Phases 22–26 background survivors)",
             fontsize=10)
plt.tight_layout()
plt.savefig(OUT_FIG, dpi=150, bbox_inches="tight")
print(f"Figure saved: {OUT_FIG}")
print("\nDone.")
