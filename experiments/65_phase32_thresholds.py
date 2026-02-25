import json, math, numpy as np
import os
os.chdir("/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer")

TARGET = '202016:209:229639465'
MU = 0.10565836727619171

def p4(pt, eta, phi):
    px = pt*math.cos(phi); py = pt*math.sin(phi); pz = pt*math.sinh(eta)
    E  = math.sqrt(px*px + py*py + pz*pz + MU*MU)
    return E, px, py, pz

def minv(p4s):
    E  = sum(p[0] for p in p4s); px = sum(p[1] for p in p4s)
    py = sum(p[2] for p in p4s); pz = sum(p[3] for p in p4s)
    return math.sqrt(max(0, E*E - px*px - py*py - pz*pz))

def dphi(a, b):
    d = abs(a - b)
    return d if d <= math.pi else 2*math.pi - d

thresholds = [1.0, 2.0, 3.0, 4.0, 5.0, 5.5, 6.0, 6.5, 7.0, 8.0]

survivors = []
with open('tools/data/cms_run2012c.ndjson') as f:
    for line in f:
        r   = json.loads(line)
        eid = f'{r["run"]}:{r["lumi"]}:{r["event"]}'
        mus = r.get('muons', [])
        nm  = len(mus)
        if nm < 7:
            continue
        pts  = [m['pt']  for m in mus]
        etas = [m['eta'] for m in mus]
        phis = [m['phi'] for m in mus]
        A = [i for i in range(nm) if phis[i] > 0]
        B = [i for i in range(nm) if phis[i] < 0]
        if not A or not B:
            continue
        phiA = np.mean([phis[i] for i in A])
        phiB = np.mean([phis[i] for i in B])
        dAB  = dphi(phiA, phiB)
        if dAB < math.radians(150):
            continue
        dphi_d = max([phis[i] for i in B]) - min([phis[i] for i in B])
        if dphi_d >= 0.10:
            continue
        if len(B) != 5:
            continue
        vecs = [p4(pts[i], etas[i], phis[i]) for i in range(nm)]
        mA   = minv([vecs[i] for i in A])
        mB   = minv([vecs[i] for i in B])
        if mB <= mA:
            continue
        survivors.append((eid, mA, mB, mB/mA, dphi_d, dAB*180/math.pi, nm))

print(f'Total survivors (m_B/m_A > 1): {len(survivors)}')
print()
for t in thresholds:
    s = [x for x in survivors if x[3] > t]
    tgt_in = any(x[0] == TARGET for x in s)
    print(f'm_B/m_A > {t:.1f}: {len(s):2d} events  target_survives={tgt_in}')

print()
print('All survivor details (sorted by ratio):')
print(f'  {"event_id":<35s}  mA(GeV)  mB(GeV)  ratio   Dphi_d    DphiAB   nMu')
for x in sorted(survivors, key=lambda s: -s[3]):
    flag = ' ← TARGET' if x[0] == TARGET else ''
    print(f'  {x[0]:<35s}  {x[1]:.4f}  {x[2]:.4f}  {x[3]:6.3f}  {x[4]:.4f}  {x[5]:.2f}°  {x[6]}{flag}')
