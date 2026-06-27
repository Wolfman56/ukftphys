"""
Mertens Function × Jump Primes — Tier Analysis
Copilot/Claude session 2026-05-31

Investigates:
  1. Growth rate of M(n) within each jump-prime tier
  2. Tier increments S_k = M(p_{k+1}) - M(p_k)  vs  sqrt(p_k) bound
  3. "Information capacity" per tier: Shannon entropy of Möbius values {-1,0,+1}
  4. Ratio |M(n)| / sqrt(n) inside each tier (local RH-proxy)

Jump primes: {2, 5, 11, 17, 37, 67, 131, 257, 521, 1031, 2053}
All results saved relative to this script's directory.
"""

import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Constants ────────────────────────────────────────────────────────────────

JUMP_PRIMES = [2, 5, 11, 17, 37, 67, 131, 257, 521, 1031, 2053, 4099, 8209, 16411, 32771]

TIER_NAMES = [
    "Tier 0: Geosphere",
    "Tier 1: Geosphere-Bio",
    "Tier 2: Biosphere",
    "Tier 3: Bio-Noo",
    "Tier 4: Noosphere-Lo",
    "Tier 5: Noosphere-Hi",
    "Tier 6: Theo-Gate",
    "Tier 7: Theosphere-Lo",
    "Tier 8: Theosphere-Hi",
    "Tier 9: Theosphere-Top",
    "Tier 10: Cosmic-Lo",
    "Tier 11: Cosmic-Mid",
    "Tier 12: Cosmic-Hi",
    "Tier 13: Cosmic-Top",
]

N = 33000  # int32 cumsum; safe up to |M| ~ 2^31 (practical limit ~10^13)

# ─── Möbius sieve ─────────────────────────────────────────────────────────────

def mobius_sieve(n: int) -> np.ndarray:
    """Return mu[0..n] via a linear sieve."""
    mu = np.zeros(n + 1, dtype=np.int8)
    mu[1] = 1
    is_composite = np.zeros(n + 1, dtype=bool)
    primes = []
    for i in range(2, n + 1):
        if not is_composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > n:
                break
            is_composite[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

# ─── Compute ──────────────────────────────────────────────────────────────────

print(f"Sieving Möbius function to N={N} ...")
mu = mobius_sieve(N)
ns = np.arange(1, N + 1)
# int8 cumsum silently overflows at |M| > 127 (~N > 700k).
# Cast to int32 before cumsum — exact arithmetic, no float involved.
M  = np.cumsum(mu[1:].astype(np.int32))  # M[i] = M(i+1), 0-indexed
M_abs_over_sqrt = np.abs(M) / np.sqrt(ns)

# ─── Tier statistics ──────────────────────────────────────────────────────────

def entropy_of_mobius(mu_block: np.ndarray) -> float:
    """Shannon entropy of the {-1, 0, +1} distribution in a block."""
    total = len(mu_block)
    if total == 0:
        return 0.0
    counts = {v: np.sum(mu_block == v) for v in (-1, 0, 1)}
    h = 0.0
    for c in counts.values():
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return h

tiers = []
for k in range(len(JUMP_PRIMES) - 1):
    lo = JUMP_PRIMES[k]
    hi = JUMP_PRIMES[k + 1]
    if hi > N:
        break
    # M values at boundaries (1-indexed; M array is 0-indexed at position n-1)
    M_lo = M[lo - 2] if lo >= 2 else 0   # M(lo)
    M_hi = M[hi - 2]                      # M(hi)
    S_k  = M_hi - M_lo

    # Möbius values in the half-open interval (lo, hi]
    block_mu = mu[lo + 1 : hi + 1]
    H = entropy_of_mobius(block_mu)

    # max |M(n)| / sqrt(n) inside this tier
    tier_ns   = ns[lo - 1 : hi]
    tier_M    = M[lo - 1 : hi]
    max_ratio = np.max(np.abs(tier_M) / np.sqrt(tier_ns))
    # density of squarefree numbers (mu != 0)
    squarefree_frac = np.mean(block_mu != 0)

    tiers.append({
        "k": k,
        "lo": lo,
        "hi": hi,
        "name": TIER_NAMES[k] if k < len(TIER_NAMES) else f"Tier {k}",
        "M_lo": int(M_lo),
        "M_hi": int(M_hi),
        "S_k": int(S_k),
        "sqrt_lo": math.sqrt(lo),
        "ratio": abs(S_k) / math.sqrt(lo),
        "entropy": H,
        "max_ratio": max_ratio,
        "squarefree_frac": squarefree_frac,
    })

# ─── Print table ──────────────────────────────────────────────────────────────

header = f"{'Tier':<26} {'[lo, hi]':>14}  {'M(lo)':>6}  {'M(hi)':>6}  {'S_k':>6}  {'|S_k|/√lo':>10}  {'H(bits)':>8}  {'max|M|/√n':>10}  {'Squarefree':>10}"
print("\n" + header)
print("-" * len(header))
for t in tiers:
    print(f"{t['name']:<26} [{t['lo']:4d},{t['hi']:5d}]  {t['M_lo']:>6}  {t['M_hi']:>6}  {t['S_k']:>6}  {t['ratio']:>10.4f}  {t['entropy']:>8.4f}  {t['max_ratio']:>10.4f}  {t['squarefree_frac']:>10.4f}")

# ─── Figure 1: M(n) with tier boundaries ──────────────────────────────────────

fig, axes = plt.subplots(3, 1, figsize=(14, 12))
fig.suptitle("Mertens Function × Jump-Prime Tiers", fontsize=14, y=1.01)

colors = plt.cm.tab10(np.linspace(0, 1, len(JUMP_PRIMES)))

ax = axes[0]
ax.plot(ns, M, color="steelblue", linewidth=0.9, label="M(n)")
ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
for i, jp in enumerate(JUMP_PRIMES[:-1]):
    if jp <= N:
        ax.axvline(jp, color=colors[i], linewidth=1.0, alpha=0.7,
                   label=f"p={jp}")
ax.fill_between(ns, -np.sqrt(ns), np.sqrt(ns), alpha=0.12, color="grey",
                label="±√n envelope")
ax.set_ylabel("M(n)")
ax.set_xlabel("n")
ax.set_xlim(1, N)
ax.legend(fontsize=7, ncol=6, loc="lower left")
ax.set_title("M(n) with jump-prime tier boundaries and ±√n envelope")

# ─── Figure 1b: |M(n)| / sqrt(n) ─────────────────────────────────────────────

ax = axes[1]
ax.plot(ns, M_abs_over_sqrt, color="crimson", linewidth=0.8)
for i, jp in enumerate(JUMP_PRIMES[:-1]):
    if jp <= N:
        ax.axvline(jp, color=colors[i], linewidth=1.0, alpha=0.6)
ax.axhline(1.0, color="black", linewidth=0.8, linestyle="--", label="|M|/√n = 1 (Mertens conjecture)")
ax.set_ylabel("|M(n)| / √n")
ax.set_xlabel("n")
ax.set_xlim(1, N)
ax.set_ylim(0, 1.2)
ax.legend(fontsize=9)
ax.set_title("|M(n)| / √n — local RH-proxy (never exceeds 1.0 here)")

# ─── Figure 1c: Tier entropy + |S_k|/sqrt(lo) ────────────────────────────────

ax = axes[2]
ks = [t["k"] for t in tiers]
entropies = [t["entropy"] for t in tiers]
ratios    = [t["ratio"] for t in tiers]
tier_labels = [f"[{t['lo']},{t['hi']}]" for t in tiers]

x = np.arange(len(tiers))
w = 0.35
b1 = ax.bar(x - w/2, entropies, w, color="teal", alpha=0.8, label="Entropy H (bits)")
b2 = ax.bar(x + w/2, ratios,    w, color="coral", alpha=0.8, label="|S_k| / √lo")
ax.set_xticks(x)
ax.set_xticklabels(tier_labels, rotation=35, ha="right", fontsize=8)
ax.set_ylabel("Value")
ax.legend()
ax.set_title("Per-tier: Shannon entropy of μ values vs |S_k|/√lo")

plt.tight_layout()
out = os.path.join(SCRIPT_DIR, "mertens_tiers.png")
plt.savefig(out, dpi=140, bbox_inches="tight")
print(f"\nSaved: {out}")
plt.close()

# ─── Figure 2: running S_k and entropy scatter ────────────────────────────────

fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5))
fig2.suptitle("Jump-Prime Tier Aggregates", fontsize=13)

ax = axes2[0]
tier_centers = [(t["lo"] + t["hi"]) / 2 for t in tiers]
sk_vals = [t["S_k"] for t in tiers]
ax.bar(range(len(tiers)), sk_vals, color=["steelblue" if s >= 0 else "crimson" for s in sk_vals],
       alpha=0.85)
ax.axhline(0, color="black", linewidth=0.7)
ax.set_xticks(range(len(tiers)))
ax.set_xticklabels([f"[{t['lo']},{t['hi']}]" for t in tiers], rotation=40, ha="right", fontsize=8)
ax.set_ylabel("S_k = M(hi) − M(lo)")
ax.set_title("Tier increment S_k (signed)")

ax = axes2[1]
ax.scatter(entropies, ratios, s=80, c=range(len(tiers)), cmap="plasma", zorder=3)
for i, t in enumerate(tiers):
    ax.annotate(f"[{t['lo']},{t['hi']}]", (entropies[i], ratios[i]),
                fontsize=7, textcoords="offset points", xytext=(4, 4))
ax.set_xlabel("Entropy H (bits)")
ax.set_ylabel("|S_k| / √lo")
ax.set_title("Information capacity vs cancellation ratio")
ax.grid(True, alpha=0.3)

plt.tight_layout()
out2 = os.path.join(SCRIPT_DIR, "mertens_aggregates.png")
plt.savefig(out2, dpi=140, bbox_inches="tight")
print(f"Saved: {out2}")
plt.close()

print("\nDone.")
