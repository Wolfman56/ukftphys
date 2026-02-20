import numpy as np
from scipy.special import gamma
import math
from sympy import Rational

print("Experiment 43: Theoretical Investigation of the '5/9' Ratio")
print("==========================================================")

# Constants
target_ratio = 5.0/9.0
print(f"Target Ratio (5/9): {target_ratio:.6f}")

alpha_inv = 137.035999
alpha = 1.0 / alpha_inv
print(f"Fine Structure Constant (alpha): {alpha:.6e}")
print("-" * 60)

# ------------------------------------------------------------------
# 1. Hypercharge Normalization in SU(5)
# ------------------------------------------------------------------
print("\n1. Hypercharge Normalization in SU(5)")
print("-" * 40)

# C^2 factor
C_squared = 5.0/3.0 # Standard SU(5) normalization g1^2 = C^2 g'^2
inv_C_squared = 1.0/C_squared
sin2_theta_W_GUT = 3.0/8.0

print(f"SU(5) Hypercharge Factor (C^2 = 5/3) : {C_squared:.4f}")
print(f"Inverse Factor (3/5)                 : {inv_C_squared:.4f}")
print(f"sin^2(theta_W) at GUT (3/8)          : {sin2_theta_W_GUT:.4f}")

# Check against 5/9
print(f"Target 5/9                           : {target_ratio:.4f}")

# ------------------------------------------------------------------
# 2. Beta Function Coefficients
# ------------------------------------------------------------------
print("\n2. Beta Function Coefficients")
print("-" * 40)

# Standard Model 1-loop beta coefficients
# b = 11/3 C2(G) - 2/3 Tf Nf - 1/3 Ts Ns
# For SM:
b3 = 7.0       # SU(3): 11 - 4/3*3 = 7
b2 = 19.0/6.0  # SU(2): 22/3 - 4 - 1/6 = 19/6 = 3.166...
b1 = -41.0/10.0 # U(1): -41/10 = -4.1

print(f"b3 (SU(3)): {b3:.4f}")
print(f"b2 (SU(2)): {b2:.4f}")
print(f"b1 (U(1)) : {b1:.4f}")

# Ratios
print(f"Ratio b2/b3   : {b2/b3:.4f}")
print(f"Ratio |b1|/b3 : {abs(b1)/b3:.4f}")
print(f"Ratio |b1|/b2 : {abs(b1)/b2:.4f}")

# Check entropic gravity idea: 11 - 2/3 Nf
# If Nf = 5 (number of dimensions? no)
val_nf5 = 11.0 - (2.0/3.0)*5.0
print(f"11 - 2/3 * 5 = {val_nf5:.4f} (Is this 1/(5/9)? No)")

# ------------------------------------------------------------------
# 3. Geometric Factors in Higher Dimensions
# ------------------------------------------------------------------
print("\n3. Geometric Factors (Spheres and Balls)")
print("-" * 40)

def sphere_area(d):
    # Surface area of unit sphere S^{d-1} in R^d
    return 2 * np.pi**(d/2) / gamma(d/2)

def ball_volume(d):
    # Volume of unit ball B^d in R^d
    return np.pi**(d/2) / gamma(d/2 + 1)

found_match = False
print("Checking ratios for d=3..11:")
for d1 in range(3, 12):
    for d2 in range(3, 12):
        s1 = sphere_area(d1)
        s2 = sphere_area(d2)
        v1 = ball_volume(d1)
        v2 = ball_volume(d2)
        
        # Check S/S
        r_ss = s1/s2
        if abs(r_ss - target_ratio) < 0.01:
            print(f"  Sphere Area S_{d1-1} / S_{d2-1} : {r_ss:.4f}")
            if abs(r_ss - target_ratio) < 0.001: found_match = True
            
        # Check V/V
        r_vv = v1/v2
        if abs(r_vv - target_ratio) < 0.01:
            print(f"  Ball Volume V_{d1} / V_{d2}     : {r_vv:.4f}")
            if abs(r_vv - target_ratio) < 0.001: found_match = True

        # Check V/S mixes
        r_vs = v1/s2
        if abs(r_vs - target_ratio) < 0.01:
            print(f"  V_{d1} / S_{d2-1}               : {r_vs:.4f}")

if not found_match:
    print("  No simple geometric match found.")

# ------------------------------------------------------------------
# 4. Degrees of Freedom
# ------------------------------------------------------------------
print("\n4. Group Theory Degrees of Freedom")
print("-" * 40)
# SU(N) dim = N^2 - 1
# SO(N) dim = N(N-1)/2

dims = {
    "U(1)": 1,
    "SU(2)": 3,
    "SU(3)": 8,
    "SU(4)": 15,
    "SU(5)": 24,
    "SO(10)": 45,
    "E6": 78
}

print(f"Dimensions: {dims}")
print("Checking ratios of dimensions...")

for k1, v1 in dims.items():
    for k2, v2 in dims.items():
        if v2 == 0: continue
        r = v1/v2
        if abs(r - target_ratio) < 0.01:
            print(f"  Ratio {k1}/{k2} = {v1}/{v2} = {r:.4f}")

# Specific check: 5/9 * something?
# 5/9 * SU(5) dim (24)?
val = target_ratio * 24
print(f"  5/9 * dim(SU(5)) = {val:.4f} (Not integer)")
    
# ------------------------------------------------------------------
# 5. Connection to Unification
# ------------------------------------------------------------------
print("\n5. Unification Relations")
print("-" * 40)
# Standard SU(5) relation:
# sin^2(theta_W) = 3/8 at GUT scale
# alpha_EM = alpha_GUT * (8/3)? No, alpha_EM = alpha_2 * sin^2(theta_W)
# At GUT, alpha_1 = alpha_2 = alpha_3 = alpha_GUT
# So alpha_EM = (3/8) * alpha_GUT

relation_factor = (5.0/9.0) * (3.0/8.0)
print("If Gamma/M = (5/9) * alpha_EM")
print(f"And alpha_EM = (3/8) * alpha_GUT")
print(f"Then Gamma/M = (5/9)*(3/8) * alpha_GUT = {relation_factor:.4f} * alpha_GUT")
print(f"Fraction: 5/24")

# ------------------------------------------------------------------
# 6. Conclusion
# ------------------------------------------------------------------
print("\nConclusion:")
print("The factor 5/9 appears most famously in the hypercharge definition")
print("for SU(5) GUTs, where g1^2 = (5/3) g'^2. Though the factor is 5/3 (or 3/5 inverse),")
print("the '5' and '3' (which 3^2=9) are highly suggestive.")
print("Specifically, if alpha_1 = alpha_2 = alpha_3 at GUT scale,")
print("and alpha_em relates to alpha_2 and alpha_1.")
print("The ratio 5/9 is likely geometric in origin, related to the embedding of U(1)_Y in SU(5).")
