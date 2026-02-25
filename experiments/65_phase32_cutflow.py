#!/usr/bin/env python3
"""
Phase 32: Apply the complete Phase 22–26 cut stack to the full 200k
Run2012C NDJSON. Produce a sequential cut-flow table and confirm that
the target event is the sole survivor.
"""
import json, numpy as np, math, os
from itertools import combinations

os.chdir("/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer")

TARGET_RUN, TARGET_LUMI, TARGET_EVENT = 202016, 209, 229639465
MU_MASS = 0.10565836727619171

# ── 4-vector helpers ──────────────────────────────────────────────────────
def make_p4(pt, eta, phi, m=MU_MASS):
    px = pt * math.cos(phi);  py = pt * math.sin(phi)
    pz = pt * math.sinh(eta);  E = math.sqrt(px*px+py*py+pz*pz+m*m)
    return E, px, py, pz

def inv_mass_p4s(p4s):
    E=sum(p[0] for p in p4s); px=sum(p[1] for p in p4s)
    py=sum(p[2] for p in p4s); pz=sum(p[3] for p in p4s)
    return math.sqrt(max(0.0, E*E-px*px-py*py-pz*pz))

def dphi(a, b):
    d = abs(a - b)
    return d if d <= math.pi else 2*math.pi - d

# ── Cut parameters (matching Phase 22–26 definitions) ─────────────────────
CUT_NMUON_MIN       = 7
CUT_DPHI_BACK2BACK  = math.radians(150)   # Δφ(A,B) > 150°
CUT_DPHI_DENSE_MAX  = 0.10                 # Dphi_dense < 0.10 rad (loose)
CUT_NB_EXACT        = 5                    # exact nB = 5
CUT_MASS_RATIO_MIN  = 1.0                  # m_dense > m_sparse

# ── Cut stages ────────────────────────────────────────────────────────────
stages = [
    "All events",
    "nMuon ≥ 7",
    "Back-to-back: Δφ(A,B) > 150°",
    "Dense cluster: Δφ_dense < 0.10 rad",
    "Exact nB = 5",
    "m_dense > m_sparse",
]
counts    = [0] * len(stages)
survivors = [[] for _ in stages]  # store event IDs that survive to each stage

print("Scanning cms_run2012c.ndjson for Phase 22–26 cut flow …")

with open("tools/data/cms_run2012c.ndjson") as fh:
    for line in fh:
        rec  = json.loads(line)
        eid  = f"{rec.get('run')}:{rec.get('lumi')}:{rec.get('event')}"
        mus  = rec.get("muons", [])
        nm   = len(mus)

        # Stage 0 — all events
        counts[0] += 1
        survivors[0].append(eid)

        # Stage 1 — nMuon ≥ 7
        if nm < CUT_NMUON_MIN:
            continue
        counts[1] += 1
        survivors[1].append(eid)

        pts  = [m["pt"]  for m in mus]
        etas = [m["eta"] for m in mus]
        phis = [m["phi"] for m in mus]

        # Split into Group A (φ>0) and Group B (φ<0)
        A = [i for i in range(nm) if phis[i] > 0]
        B = [i for i in range(nm) if phis[i] < 0]
        if len(A) == 0 or len(B) == 0:
            continue  # degenerate event

        # Mean phi of each group
        phi_A = np.mean([phis[i] for i in A])
        phi_B = np.mean([phis[i] for i in B])
        dAB   = dphi(phi_A, phi_B)      # in [0, π]

        # Stage 2 — Back-to-back
        if dAB < CUT_DPHI_BACK2BACK:
            continue
        counts[2] += 1
        survivors[2].append(eid)

        # Dphi_dense = max spread within the larger group
        grp_dense = B if len(B) >= len(A) else A
        phis_dense = [phis[i] for i in grp_dense]
        dphi_dense = max(phis_dense) - min(phis_dense)

        # Stage 3 — Dense cluster
        if dphi_dense >= CUT_DPHI_DENSE_MAX:
            continue
        counts[3] += 1
        survivors[3].append(eid)

        # Stage 4 — Exact nB = 5
        if len(B) != CUT_NB_EXACT:
            continue
        counts[4] += 1
        survivors[4].append(eid)

        # Invariant masses
        p4s = [make_p4(pts[i], etas[i], phis[i]) for i in range(nm)]
        m_A = inv_mass_p4s([p4s[i] for i in A])
        m_B = inv_mass_p4s([p4s[i] for i in B])

        # Stage 5 — m_dense > m_sparse
        if m_B <= m_A:
            continue
        counts[5] += 1
        survivors[5].append(eid)

print("Done.\n")

# ── Print cut-flow table ──────────────────────────────────────────────────
target_eid = f"{TARGET_RUN}:{TARGET_LUMI}:{TARGET_EVENT}"
print("=" * 72)
print("Phase 32 — Full Cut-Flow (Run2012C NDJSON, 200,000 events)")
print("=" * 72)
print(f"\n  {'Cut stage':<40s}  {'Survivors':>10s}  {'Reject factor':>14s}  {'Target?'}")
print("  " + "-" * 75)
for i, stage in enumerate(stages):
    n = counts[i]
    if i == 0:
        fac = "—"
    else:
        fac = f"{counts[0]/n:.1f}×" if n > 0 else "∞"
    tgt = "✓" if target_eid in survivors[i] else "✗"
    print(f"  {stage:<40s}  {n:>10,}  {fac:>14s}  {tgt}")

# ── Final survivors ───────────────────────────────────────────────────────
final = survivors[-1]
print(f"\n  Final survivors (all cuts): {len(final)}")
for eid in final:
    flag = " ← TARGET" if eid == target_eid else ""
    print(f"    {eid}{flag}")

# ── Detailed kinematics of ALL final survivors ────────────────────────────
print(f"\n── Detailed kinematics of final survivors ─────────────────────────────")
with open("tools/data/cms_run2012c.ndjson") as fh:
    for line in fh:
        rec = json.loads(line)
        eid = f"{rec.get('run')}:{rec.get('lumi')}:{rec.get('event')}"
        if eid not in final:
            continue
        mus   = rec.get("muons", [])
        pts   = [m["pt"]  for m in mus]
        etas  = [m["eta"] for m in mus]
        phis  = [m["phi"] for m in mus]
        chrgs = [m.get("charge", 0) for m in mus]
        nm    = len(mus)
        A     = [i for i in range(nm) if phis[i] > 0]
        B     = [i for i in range(nm) if phis[i] < 0]
        p4s   = [make_p4(pts[i], etas[i], phis[i]) for i in range(nm)]
        m_A   = inv_mass_p4s([p4s[i] for i in A])
        m_B   = inv_mass_p4s([p4s[i] for i in B])
        m_7mu = inv_mass_p4s(p4s)
        phi_A = np.mean([phis[i] for i in A])
        phi_B = np.mean([phis[i] for i in B])
        dAB   = math.degrees(dphi(phi_A, phi_B))
        dphi_dense = max([phis[i] for i in B]) - min([phis[i] for i in B])
        flag  = " ← TARGET" if eid == target_eid else ""
        print(f"\n  {eid}{flag}")
        print(f"    nMuon={nm}  nA={len(A)}  nB={len(B)}")
        print(f"    Δφ(A,B)={dAB:.2f}°  Δφ_dense={dphi_dense:.4f} rad")
        print(f"    m_A={m_A:.4f} GeV  m_B={m_B:.4f} GeV  ratio={m_B/m_A:.3f}")
        print(f"    m(7μ)={m_7mu:.4f} GeV")
        print(f"    pT range: {min(pts):.1f}–{max(pts):.1f} GeV")
        print(f"    η range: {min(etas):.3f}–{max(etas):.3f}")
        print(f"    charges: {[int(c) for c in chrgs]}  Q_net={int(sum(chrgs)):+d}")

# ── Summary ───────────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("VERDICT")
print("=" * 72)
n_final = len(final)
if n_final == 1 and final[0] == target_eid:
    print(f"  CONFIRMED: Target event is THE SOLE SURVIVOR of all Phase 22–26 cuts")
    print(f"  in 200,000 Run2012C DoubleMuParked events.")
    print(f"  Background estimate: <1/{counts[0]:,} = <{1/counts[0]:.2e} events")
elif target_eid in final:
    others = [e for e in final if e != target_eid]
    print(f"  Target survives. {len(others)} other event(s) also pass all cuts:")
    for e in others:
        print(f"    {e}")
else:
    print(f"  ! Target event did NOT survive all cuts — investigate coordinate differences")
    print(f"  {n_final} survivors: {final}")
