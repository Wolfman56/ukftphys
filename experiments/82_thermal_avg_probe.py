"""Quick probe: does Boltzmann-averaging W_ΣΔ recover 5/9·α_QED?

This is the key open question flagged after Exp 81.
"""
import math
import numpy as np

DELTA_D   = math.pi**4 / 384
ALPHA_QED = 1.0 / 137.036
BIT_LEN   = math.floor(math.log2(151))   # = 7, for p=151

def w_sigma_delta(pt):
    """W_ΣΔ(p=151, pT) — same formula as 81_lean_bounds.py"""
    return DELTA_D / (BIT_LEN + 1) * math.exp(-math.log(max(pt, 1.0)) * ALPHA_QED)

target = (5.0 / 9.0) * ALPHA_QED

# ── pT table ─────────────────────────────────────────────────────────────────
print("pT (GeV)   W_ΣΔ(151,pT)   exp(-pT/100)   product")
for pt in [1, 5, 10, 50, 100, 150, 200, 500]:
    bz = math.exp(-pt / 100.0)
    print(f"  {pt:5}    {w_sigma_delta(pt):.6e}   {bz:.6e}   {w_sigma_delta(pt)*bz:.4e}")

print(f"\ntarget 5/9 * alpha_QED = {target:.6e}")

# ── Thermal average at EW scale T = 100 GeV ──────────────────────────────────
# Phase space: relativistic, massless limit → pT^2 * exp(-pT/T)
pts = np.linspace(0.1, 5000, 1_000_000)
w_arr = np.vectorize(w_sigma_delta)(pts)

T_EW = 100.0
phase_EW = pts**2 * np.exp(-pts / T_EW)
delta_bar_EW = np.trapz(w_arr * phase_EW, pts) / np.trapz(phase_EW, pts)
print(f"\ndelta_bar(T=100 GeV)   = {delta_bar_EW:.6e}")
print(f"ratio to target        = {delta_bar_EW / target:.4f}x")

# ── Thermal average at GUT scale T = 1e14 GeV (needs pT up to ~1e15) ─────────
# Use log-spaced grid for wide range
pts_gut = np.geomspace(0.1, 1e15, 2_000_000)
w_gut   = np.vectorize(w_sigma_delta)(pts_gut)
T_GUT   = 1e14
phase_GUT = pts_gut**2 * np.exp(-pts_gut / T_GUT)
delta_bar_GUT = np.trapz(w_gut * phase_GUT, pts_gut) / np.trapz(phase_GUT, pts_gut)
print(f"\ndelta_bar(T=1e14 GeV)  = {delta_bar_GUT:.6e}")
print(f"ratio to 5/9 (= 0.556) = {delta_bar_GUT / (5.0/9.0):.4e}")

# ── Analytic form of thermal average ─────────────────────────────────────────
# W_ΣΔ(pT) = C * pT^(-α_QED)   where C = DELTA_D / (BIT_LEN+1)
# Thermal avg of pT^(-α) with phase pT^2 exp(-pT/T):
#   <W> = C * Gamma(3 - alpha) * T^(-alpha) / Gamma(3)
#         since integral pT^(2-alpha) exp(-pT/T) dpT = T^(3-alpha) Gamma(3-alpha)
import scipy.special as sp
C     = DELTA_D / (BIT_LEN + 1)
alpha = ALPHA_QED
delta_bar_analytic_EW  = C * sp.gamma(3 - alpha) * T_EW**(-alpha) / math.gamma(3)
delta_bar_analytic_GUT = C * sp.gamma(3 - alpha) * T_GUT**(-alpha) / math.gamma(3)
print(f"\nAnalytic thermal average:")
print(f"  delta_bar_analytic(T=100 GeV)   = {delta_bar_analytic_EW:.6e}")
print(f"  delta_bar_analytic(T=1e14 GeV)  = {delta_bar_analytic_GUT:.6e}")
print(f"  Formula: C * Gamma(3 - alpha_QED) * T^(-alpha_QED) / 2")
print(f"  (5/9)*alpha_QED                 = {target:.6e}")
print(f"\nConclusion: the Boltzmann average of W_ΣΔ scales as T^(-alpha_QED),")
print(f"NOT a fixed constant. 5/9*alpha_QED is NOT the direct thermal average.")
print(f"The 5/9 rule must enter via a different channel (topology, not pT integration).")
