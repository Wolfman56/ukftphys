#!/usr/bin/env python3
"""
Phase 31: Search cms_run2012c.ndjson (200k events) for any 3-muon sub-combination
with invariant mass near Υ(1S)=9.460, Υ(2S)=10.023, Υ(3S)=10.355 GeV.
Also records same for di-muon pairs near J/ψ=3.097, ψ(2S)=3.686, Υ(1S)=9.460.
Reports rates and whether the target event is anomalous or typical.
"""
import json, numpy as np, os, math
from itertools import combinations
from collections import defaultdict

os.chdir("/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer")

TARGET_RUN, TARGET_LUMI, TARGET_EVENT = 202016, 209, 229639465
MU_MASS = 0.10565836727619171

# ── 4-vector helpers ──────────────────────────────────────────────────────
def make_p4(pt, eta, phi, m=MU_MASS):
    px = pt * math.cos(phi)
    py = pt * math.sin(phi)
    pz = pt * math.sinh(eta)
    E  = math.sqrt(px*px + py*py + pz*pz + m*m)
    return E, px, py, pz

def inv_mass_p4s(p4s):
    E  = sum(p[0] for p in p4s)
    px = sum(p[1] for p in p4s)
    py = sum(p[2] for p in p4s)
    pz = sum(p[3] for p in p4s)
    s2 = E*E - px*px - py*py - pz*pz
    return math.sqrt(max(0.0, s2))

# ── Resonance windows ─────────────────────────────────────────────────────
RESONANCES_2MU = {
    "J/ψ":    (3.097, 0.10),   # ±100 MeV
    "ψ(2S)":  (3.686, 0.10),
    "Υ(1S)":  (9.460, 0.30),   # ±300 MeV (broader for 3-body kinematics)
    "Υ(2S)":  (10.023, 0.30),
    "Υ(3S)":  (10.355, 0.30),
}
RESONANCES_3MU = {
    "Υ(1S)_3mu":  (9.460,  0.50),
    "Υ(2S)_3mu":  (10.023, 0.50),
    "Υ(3S)_3mu":  (10.355, 0.50),
}

def in_window(m, center, half_width):
    return abs(m - center) < half_width

# ── Main scan ─────────────────────────────────────────────────────────────
n_events     = 0
n_ge3mu      = 0
n_ge7mu      = 0
hits_2mu     = defaultdict(list)   # res_name → [event_id, ...]
hits_3mu     = defaultdict(list)
target_found = None
all_nmuo     = []

print("Scanning cms_run2012c.ndjson …")
with open("tools/data/cms_run2012c.ndjson") as fh:
    for line in fh:
        rec = json.loads(line)
        n_events += 1
        if n_events % 20000 == 0:
            print(f"  {n_events:,} events processed …")

        mus = rec.get("muons", [])
        nm  = len(mus)
        all_nmuo.append(nm)

        if nm < 2:
            continue
        n_ge3mu += (nm >= 3)
        n_ge7mu += (nm >= 7)

        is_target = (rec.get("run") == TARGET_RUN and
                     rec.get("event") == TARGET_EVENT)
        eid = f"{rec.get('run')}:{rec.get('lumi')}:{rec.get('event')}"

        p4s    = [make_p4(m["pt"], m["eta"], m["phi"]) for m in mus]
        chgs   = [m.get("charge", 0) for m in mus]

        # ── Di-muon OS pairs ─────────────────────────────────────────────
        for i, j in combinations(range(nm), 2):
            if chgs[i] + chgs[j] != 0:
                continue
            m2 = inv_mass_p4s([p4s[i], p4s[j]])
            for rname, (rcenter, rhw) in RESONANCES_2MU.items():
                if in_window(m2, rcenter, rhw):
                    hits_2mu[rname].append((eid, m2, i, j))
                    if is_target:
                        print(f"  [TARGET] OS pair μ{i}+μ{j}: m={m2:.4f} GeV → IN {rname} window")

        if nm < 3:
            continue

        # ── 3-muon sub-combinations ──────────────────────────────────────
        for i, j, k in combinations(range(nm), 3):
            q3 = chgs[i] + chgs[j] + chgs[k]
            if abs(q3) != 1:   # require |Q|=1 (physical triplet from Υ-like)
                continue
            m3 = inv_mass_p4s([p4s[i], p4s[j], p4s[k]])
            for rname, (rcenter, rhw) in RESONANCES_3MU.items():
                if in_window(m3, rcenter, rhw):
                    hits_3mu[rname].append((eid, m3, i, j, k, q3))
                    if is_target:
                        print(f"  [TARGET] Triplet μ{i}+μ{j}+μ{k} (Q={q3:+d}): "
                              f"m={m3:.4f} GeV → IN {rname} window")
                        if target_found is None:
                            target_found = []
                        target_found.append((rname, m3, i, j, k))

print(f"\nDone. {n_events:,} events scanned.")

# ── nMuon distribution ────────────────────────────────────────────────────
print("\n── nMuon distribution (Run2012C, 200k events) ──────────────────────")
from collections import Counter
nm_counts = Counter(all_nmuo)
for k in sorted(nm_counts):
    pct = nm_counts[k] / n_events * 100
    bar = "█" * int(pct / 0.5)
    print(f"  nMuon={k:2d}: {nm_counts[k]:7,}  ({pct:5.1f}%)  {bar}")
print(f"\n  Events with nMuon ≥ 3:  {n_ge3mu:,}  ({n_ge3mu/n_events*100:.2f}%)")
print(f"  Events with nMuon ≥ 7:  {n_ge7mu:,}  ({n_ge7mu/n_events*100:.4f}%)")

# ── Di-muon resonance hit rates ───────────────────────────────────────────
print("\n── Di-muon OS pair resonance rates ─────────────────────────────────")
for rname, (rcenter, rhw) in RESONANCES_2MU.items():
    h = hits_2mu[rname]
    unique_events = len(set(x[0] for x in h))
    print(f"  {rname:10s} [{rcenter-rhw:.3f}–{rcenter+rhw:.3f} GeV]:  "
          f"{len(h):5d} pairs in {unique_events:5d} events  "
          f"({unique_events/n_events*100:.3f}%)")

# ── 3-muon resonance hit rates ────────────────────────────────────────────
print("\n── 3-muon |Q|=1 sub-combination resonance rates ─────────────────────")
for rname, (rcenter, rhw) in RESONANCES_3MU.items():
    h = hits_3mu[rname]
    unique_events = len(set(x[0] for x in h))
    print(f"  {rname:15s} [{rcenter-rhw:.3f}–{rcenter+rhw:.3f} GeV]:  "
          f"{len(h):5d} triplets in {unique_events:5d} events  "
          f"({unique_events/n_events*100:.3f}%)")

# ── Focus: Υ(1S) triplet events — are any also nMuon≥7? ──────────────────
print("\n── Events with Υ(1S) 3-mu triplet AND nMuon≥7 ───────────────────────")
upsilon_eids = set(x[0] for x in hits_3mu["Υ(1S)_3mu"])
target_eid   = f"{TARGET_RUN}:{TARGET_LUMI}:{TARGET_EVENT}"
print(f"  Total Υ(1S)-triplet events: {len(upsilon_eids)}")
print(f"  Is target in Υ(1S) set?  {target_eid in upsilon_eids}")
print(f"  (Target cluster triplet mass was 9.661 GeV, window ±0.50 GeV)")

# Count how many Υ(1S)-triplet events also have nMuon>=7
n_y1s_and_7mu = 0
with open("tools/data/cms_run2012c.ndjson") as fh:
    for line in fh:
        rec = json.loads(line)
        eid = f"{rec.get('run')}:{rec.get('lumi')}:{rec.get('event')}"
        if eid in upsilon_eids and len(rec.get("muons", [])) >= 7:
            n_y1s_and_7mu += 1
            if eid == target_eid:
                print(f"    TARGET EVENT confirmed in Υ(1S)∩nMu≥7")
            else:
                nm = len(rec.get("muons", []))
                print(f"    Other event: {eid}  nMuon={nm}")
print(f"  Events with Υ(1S) triplet AND nMuon≥7: {n_y1s_and_7mu}")

# ── Show closest triplet masses around Υ(1S) in 7mu events ───────────────
print("\n── All 7mu events: minimum distance to Υ(1S) in any 3mu sub-combo ──")
UPS1S = 9.460
with open("tools/data/cms_run2012c.ndjson") as fh:
    for line in fh:
        rec = json.loads(line)
        mus = rec.get("muons", [])
        if len(mus) < 7:
            continue
        eid  = f"{rec.get('run')}:{rec.get('lumi')}:{rec.get('event')}"
        p4s  = [make_p4(m["pt"], m["eta"], m["phi"]) for m in mus]
        chgs = [m.get("charge", 0) for m in mus]
        best = min(
            (abs(inv_mass_p4s([p4s[i],p4s[j],p4s[k]]) - UPS1S),
             inv_mass_p4s([p4s[i],p4s[j],p4s[k]]),
             i, j, k)
            for i,j,k in combinations(range(len(mus)),3)
            if abs(chgs[i]+chgs[j]+chgs[k]) == 1
        ) if any(abs(chgs[i]+chgs[j]+chgs[k])==1
                 for i,j,k in combinations(range(len(mus)),3)) else (99, 0, 0, 0, 0)
        flag = " ← TARGET" if eid == target_eid else ""
        print(f"  {eid}  Δ={best[0]:.4f} GeV  m3={best[1]:.4f} GeV{flag}")

print("\n── VERDICT ──────────────────────────────────────────────────────────")
n_y1s = len(set(x[0] for x in hits_3mu["Υ(1S)_3mu"]))
rate  = n_y1s / n_events
print(f"  Υ(1S)-triplet (±0.5 GeV) appears in {n_y1s}/{n_events} events = {rate:.4f} = {rate*100:.2f}%")
if n_y1s_and_7mu <= 1:
    print(f"  Target is {'the only' if n_y1s_and_7mu==1 else 'not in'} nMuon≥7 event with Υ(1S)-triplet")
    print(f"  → Not a common background feature at this multiplicity")
else:
    print(f"  {n_y1s_and_7mu} events have both nMuon≥7 AND Υ(1S) triplet")
    print(f"  → Υ(1S) triplet in 7mu events is {'rare' if n_y1s_and_7mu < 10 else 'common'}")
