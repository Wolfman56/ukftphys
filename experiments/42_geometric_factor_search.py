import numpy as np
import math

# Constants
M_xm = 320.0       # GeV (Fixed value from model)
Gamma_xm = 1.296   # GeV (Physical width from MG5)
alpha_inv = 137.035999084 # QED Coupling (Inverse) at Q=0
alpha = 1.0 / alpha_inv

print("Experiment 42: Geometric Factor Search")
print("-" * 60)
print(f"Mirror Fermion Mass (M) : {M_xm} GeV")
print(f"Mirror Fermion Width (W): {Gamma_xm} GeV")
print(f"Fine Structure Const (a): {alpha:.8f}")

# Target Ratio
target = Gamma_xm / M_xm
print(f"Dimensionless Coupling  : {target:.8f}")
ratio = target / alpha
print(f"Target Ratio (W/M)/a    : {ratio:.8f}")
print("-" * 60)

# Search
candidates = []

# 1. Rational Factors
terms = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for n in terms:
    for d in terms:
        val = n/d
        diff = abs(val - ratio)
        if diff < 0.01:
            candidates.append(("$%d/%d$" % (n, d), val, diff))

# 2. Geometric Constants
pi = math.pi
e = math.e
gamma = 0.5772156649 # Euler-Mascheroni

geo_terms = {
    r"$1/\sqrt{3}$": 1/math.sqrt(3),
    r"$1/\sqrt{2}$": 1/math.sqrt(2),
    r"$\pi/6$": pi/6,
    r"$1/2 + \pi/100$": 0.5 + pi/100, # Joke/Test
    r"$e/5$": e/5,
    r"$9/5 \pi^2$": 9/(5*pi**2), # Random guess
    r"$\gamma$": gamma,
    r"$1/\ln(6)$": 1/math.log(6),
    r"$\ln(2)$": math.log(2), # 0.693
    r"$\ln(3)/2$": math.log(3)/2, # 0.549
    r"$\pi/e^2$": pi/(e**2),
    r"$2/\pi$": 2/pi, # 0.636
    r"$\pi/5$": pi/5, # 0.628
    r"$e/5$": e/5,    # 0.543
    r"$\sqrt{2/\pi}$": math.sqrt(2/pi), # 0.79
    r"$1/\phi$": 1/1.6180339887, # 0.618
    r"$\phi/3$": 1.6180339887/3, # 0.539
}

for name, val in geo_terms.items():
    diff = abs(val - ratio)
    if diff < 0.05:
        candidates.append((name, val, diff))

# 3. Sort and Print
candidates.sort(key=lambda x: x[2]) # Sort by difference

print("\nBest Geometric Matches:")
print(f"{'Candidate':<15} | {'Value':<10} | {'Error (%)':<10}")
print("-" * 45)
for name, val, diff in candidates[:10]:
    err_pct = (diff / ratio) * 100
    print(f"{name:<15} | {val:.6f}   | {err_pct:.2f}%")

print("-" * 60)
print("Analysis:")
best = candidates[0]
if best[0] == "$5/9$":
    print("The ratio is incredibly close to 5/9 (0.5555...).")
    print("Why 5/9? In String Theory or SM Group Theory?")
    print(" - 5/9 is the Hypercharge normalization factor in GUTs (SU(5)).")
    print(" - sin^2(theta_W) = 3/8 at GUT scale, but related factors appear.")
    print(" - Number of dimensions? (10-1)/... no.")
    print(" - Spin sums? 5/9?")
elif best[0] == r"$e/5$":
    print("Close to e/5 (0.543), but 5/9 is better.")
elif "ln(3)" in best[0]:
    print("Close to ln(3)/2 (0.549). Entropic factor ln(3) - 3 states?")

# Theoretical check for 5/9
print("\nHypothesis Check: The 5/9 Factor")
check_5_9 = (5.0/9.0) * alpha
print(f"Predicted Width (if 5/9 * alpha * M): {check_5_9 * M_xm:.4f} GeV")
print(f"Actual Width (Exp 37/38)           : {Gamma_xm:.4f} GeV")
print("-" * 60)
