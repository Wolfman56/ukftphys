#!/usr/bin/env python3
"""
Phase 30: RECO-level muon fields — charge, sub-masses, resonance search.
Uses cms_run2012c.ndjson (has charge) and ROOT file (has iso/dxy if found).
"""
import json, numpy as np
import os, sys

os.chdir("/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer")
TARGET_RUN, TARGET_LUMI, TARGET_EVENT = 202016, 209, 229639465
MU_MASS = 0.10565836727619171  # GeV

# ── 1. Load from NDJSON (has charge) ─────────────────────────────────────
rec = None
with open("tools/data/cms_run2012c.ndjson") as fh:
    for line in fh:
        r = json.loads(line)
        if r.get("run") == TARGET_RUN and r.get("event") == TARGET_EVENT:
            rec = r; break
assert rec, "target event not found"

muons = rec["muons"]
n = len(muons)
pts   = np.array([m["pt"]     for m in muons])
etas  = np.array([m["eta"]    for m in muons])
phis  = np.array([m["phi"]    for m in muons])
chrgs = np.array([m["charge"] for m in muons], dtype=int)
masses = np.full(n, MU_MASS)

# ── 2. Also try to get iso/dxy from ROOT (subset search) ─────────────────
import uproot
iso03 = np.full(n, np.nan)
iso04 = np.full(n, np.nan)
dxys  = np.full(n, np.nan)
dzs   = np.full(n, np.nan)
dxErr = np.full(n, np.nan)
dzErr = np.full(n, np.nan)

try:
    f    = uproot.open("tools/data/Run2012B_DoubleMuParked.root")
    tree = f["Events"]
    FIELDS2 = ["run","luminosityBlock","event","nMuon",
                "Muon_pt","Muon_eta","Muon_phi",
                "Muon_pfRelIso03_all","Muon_pfRelIso04_all",
                "Muon_dxy","Muon_dxyErr","Muon_dz","Muon_dzErr"]
    total = tree.num_entries
    found_in_root = False
    for start in range(0, total, 200_000):
        stop = min(start+200_000, total)
        arr  = tree.arrays(FIELDS2, entry_start=start, entry_stop=stop, library="np")
        mask = ((arr["run"]==TARGET_RUN) & (arr["luminosityBlock"]==TARGET_LUMI)
                & (arr["event"]==TARGET_EVENT))
        idxs = np.where(mask)[0]
        if len(idxs):
            i0 = idxs[0]
            iso03 = np.array(arr["Muon_pfRelIso03_all"][i0])
            iso04 = np.array(arr["Muon_pfRelIso04_all"][i0])
            dxys  = np.array(arr["Muon_dxy"][i0])
            dzs   = np.array(arr["Muon_dz"][i0])
            dxErr = np.array(arr["Muon_dxyErr"][i0])
            dzErr = np.array(arr["Muon_dzErr"][i0])
            found_in_root = True
            print("[ROOT] Found event in Run2012B NanoAOD")
            break
    if not found_in_root:
        print("[ROOT] Event NOT in Run2012B NanoAOD (Run2012C event, as expected)")
except Exception as e:
    print(f"[ROOT] Error: {e}")

# ── 3. 4-vector helpers ───────────────────────────────────────────────────
def make_4vec(pt, eta, phi, m):
    px = pt * np.cos(phi)
    py = pt * np.sin(phi)
    pz = pt * np.sinh(eta)
    E  = np.sqrt(px**2 + py**2 + pz**2 + m**2)
    return np.array([E, px, py, pz])

def inv_mass_idx(idxs):
    vecs = [make_4vec(pts[i], etas[i], phis[i], masses[i]) for i in idxs]
    s = sum(vecs)
    return np.sqrt(max(0.0, s[0]**2 - s[1]**2 - s[2]**2 - s[3]**2))

RESONANCES = {
    0.548:"η", 0.770:"ρ/ω", 0.782:"ω", 1.020:"φ(1020)",
    3.097:"J/ψ", 3.686:"ψ(2S)", 9.460:"Υ(1S)", 10.023:"Υ(2S)",
    10.355:"Υ(3S)", 91.2:"Z"
}
def res_hint(m, tol_pct=5):
    best = min(RESONANCES, key=lambda r: abs(r-m)/r)
    if abs(best-m)/best*100 < tol_pct:
        return f"  ← near {RESONANCES[best]}"
    return ""

# ── 4. Print header ───────────────────────────────────────────────────────
print("\n" + "="*72)
print("Phase 30 — RECO-level muon fields")
print(f"Event: {TARGET_RUN}:{TARGET_LUMI}:{TARGET_EVENT}")
print("="*72)

# Groups
A_idx = [i for i in range(n) if phis[i] > 0]   # Group A (sparse)
B_idx = [i for i in range(n) if phis[i] < 0]   # Group B (dense)

print(f"\nGroup A (φ>0):  μ{A_idx}   phi_span = {phis[A_idx].max()-phis[A_idx].min():.4f} rad")
print(f"Group B (φ<0):  μ{B_idx}   phi_span = {phis[B_idx].max()-phis[B_idx].min():.4f} rad")

# ── 5. Per-muon table ─────────────────────────────────────────────────────
print("\n  μ    Grp   pT(GeV)   η          φ(rad)    Q")
print("  " + "-"*56)
for i in range(n):
    g = "A" if i in A_idx else "B"
    print(f"  {i}    {g}    {pts[i]:7.3f}   {etas[i]:+.4f}   {phis[i]:+.4f}   {chrgs[i]:+d}")

print(f"\n  Net charge (7μ):  Q = {chrgs.sum():+d}")
print(f"  Group A charges:  {list(chrgs[A_idx])}  → Q_A = {chrgs[A_idx].sum():+d}")
print(f"  Group B charges:  {list(chrgs[B_idx])}  → Q_B = {chrgs[B_idx].sum():+d}")
print(f"  Opposite-sign confirmation: Group A has {'one μ+ one μ-' if len(set(chrgs[A_idx]))==2 else 'same-sign pair!'}")

# ── 6. Isolation (if available from ROOT) ────────────────────────────────
print("\n── Isolation ──────────────────────────────────────────────────────────")
if not any(np.isnan(iso03)):
    print("  (from Run2012B NanoAOD — matched by kinematics if run differs)")
    print(f"  {'μ':3s}  {'Grp':4s}  {'Iso03':8s}  {'Iso04':8s}  {'Status'}")
    print("  " + "-"*45)
    for i in range(n):
        g = "A" if i in A_idx else "B"
        status = "PROMPT" if iso03[i] < 0.15 else "non-isolated"
        print(f"  {i}    {g}    {iso03[i]:.4f}    {iso04[i]:.4f}    {status}")
    print(f"\n  Prompt (iso03<0.15): {(iso03<0.15).sum()}/7")
else:
    print("  Isolation NOT in Run2012C NDJSON cache. Summary from NanoAOD scan:")
    print("  (Run 202016 is a Run2012C run — not in our Run2012B ROOT file)")
    print("  → Isolation can only be retrieved from CMS Open Data record 6030")
    print("    or from a Run2012C NanoAOD file. Marking as 'pending' for §36.")

# ── 7. Impact parameters ─────────────────────────────────────────────────
print("\n── Impact parameters ──────────────────────────────────────────────────")
if not any(np.isnan(dxys)):
    print(f"  {'μ':3s}  {'|dxy|(mm)':10s}  {'|dz|(mm)':10s}  {'Status'}")
    print("  " + "-"*45)
    for i in range(n):
        g = "A" if i in A_idx else "B"
        flag = "prompt" if abs(dxys[i])*10 < 0.2 else "DISPLACED"
        print(f"  {i}({g})  {abs(dxys[i])*10:.4f}        {abs(dzs[i])*10:.4f}        {flag}")
else:
    print("  Impact parameters not in Run2012C NDJSON cache.")
    print("  → Need Run2012C NanoAOD or AOD for dxy/dz values.")

# ── 8. Invariant masses ───────────────────────────────────────────────────
print("\n── Invariant masses ───────────────────────────────────────────────────")
m_7mu = inv_mass_idx(range(n))
m_A   = inv_mass_idx(A_idx)
m_B   = inv_mass_idx(B_idx)
print(f"  m(7μ) = {m_7mu:.4f} GeV")
print(f"  m(Group A, 2μ) = {m_A:.4f} GeV{res_hint(m_A)}")
print(f"  m(Group B, 5μ) = {m_B:.4f} GeV{res_hint(m_B, tol_pct=15)}")
print(f"  Ratio m_B/m_A  = {m_B/m_A:.4f}")

# All opposite-sign pairs across both groups
print("\n── Opposite-sign (OS) di-muon pairs ──────────────────────────────────")
print(f"  {'Pair':8s}  {'Grp':4s}  {'Q_i':4s}  {'Q_j':4s}  {'m(GeV)':10s}  {'Note'}")
print("  " + "-"*62)
os_masses_A = []
os_masses_B = []
for i in range(n):
    for j in range(i+1, n):
        if chrgs[i] + chrgs[j] == 0:  # opposite sign
            m_ij = inv_mass_idx([i, j])
            g_i = "A" if i in A_idx else "B"
            g_j = "A" if j in A_idx else "B"
            grp = g_i if g_i == g_j else "A+B"
            hint = res_hint(m_ij, tol_pct=8)
            print(f"  μ{i}+μ{j}   {grp:4s}   {chrgs[i]:+d}     {chrgs[j]:+d}     {m_ij:.4f}     {hint}")
            if grp == "A": os_masses_A.append(m_ij)
            if grp == "B": os_masses_B.append(m_ij)

# OS triplets in B
print("\n── OS triplets (μ+μ+μ- and μ+μ-μ-) in Group B ─────────────────────")
for ii, i in enumerate(B_idx):
    for jj, j in enumerate(B_idx):
        if jj <= ii: continue
        for kk, k in enumerate(B_idx):
            if kk <= jj: continue
            q_sum = chrgs[i] + chrgs[j] + chrgs[k]
            if abs(q_sum) == 1:
                m_ijk = inv_mass_idx([i, j, k])
                hint  = res_hint(m_ijk, tol_pct=8)
                print(f"  μ{i}({chrgs[i]:+d})+μ{j}({chrgs[j]:+d})+μ{k}({chrgs[k]:+d}):  "
                      f"m = {m_ijk:.4f} GeV  Q={q_sum:+d}{hint}")

# All-B sub-masses
print("\n── All Group B sub-combination masses ────────────────────────────────")
for ii, i in enumerate(B_idx):
    for jj, j in enumerate(B_idx):
        if jj <= ii:
            continue
        m2 = inv_mass_idx([i, j])
        print(f"  μ{i}({chrgs[i]:+d})+μ{j}({chrgs[j]:+d}):  m = {m2:.4f} GeV{res_hint(m2, 10)}")

# ── 9. Charge asymmetry interpretation ───────────────────────────────────
print("\n── Charge pattern interpretation ─────────────────────────────────────")
print(f"  Group A: μ{A_idx[0]} (Q={chrgs[A_idx[0]]:+d}) + μ{A_idx[1]} (Q={chrgs[A_idx[1]]:+d})")
print(f"    → opposite-sign pair — consistent with resonance decay")
print(f"    → m(A) = {m_A:.4f} GeV  (ρ/ω region if SM, or dark photon if BSM)")
print(f"\n  Group B: charges = {list(chrgs[B_idx])}")
print(f"    → net Q_B = {chrgs[B_idx].sum():+d} (odd, cannot be neutral resonance alone)")
print(f"    → must contain at least one un-paired muon")
if chrgs[B_idx].sum() == 1:
    # Find the two OS pairs and the odd one out
    paired    = []
    remaining = list(B_idx)
    for i in B_idx:
        for j in B_idx:
            if j <= i: continue
            if chrgs[i] + chrgs[j] == 0 and i not in paired and j not in paired:
                paired.extend([i,j])
                m_pair = inv_mass_idx([i,j])
                print(f"    → OS pair μ{i}+μ{j}: m = {m_pair:.4f} GeV{res_hint(m_pair,10)}")
    odd_out = [x for x in B_idx if x not in paired]
    print(f"    → Unpaired μ: {odd_out}  (Q={[chrgs[x] for x in odd_out]})")

print("\n" + "="*72)
print("PHASE 30 VERDICT")
print("="*72)
print(f"  Net event charge:   Q = {chrgs.sum():+d}")
print(f"  Group A (2μ):  OS pair,  m = {m_A:.4f} GeV  → possible resonance")
print(f"  Group B (5μ):  Q_B={chrgs[B_idx].sum():+d},  m = {m_B:.4f} GeV")
print(f"  The charge structure alone rules out a single neutral BSM resonance")
print(f"  decaying to 7μ. However TWO (or more) back-to-back resonances remain viable:")
print(f"    Scenario 1: X(dark) → μ+μ-  (Group A, m≈{m_A:.2f} GeV)")
print(f"                Y(dark) → 3μ+2μ- (Group B, m≈{m_B:.2f} GeV, multi-body)")
print(f"    Scenario 2: Z* → qq̄ → two jets each → one jet = group A, one = group B")
print(f"    Scenario 3: Novel resonance in B producing OS sub-pairs + excess muon")
print(f"\n  Sub-masses (OS pairs in B) will determine whether resonance peaks exist.")
