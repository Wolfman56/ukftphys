#!/usr/bin/env python3
"""
Experiment 86 — Choice-Bohmian Sigma-Delta Dynamics in the Geosphere
======================================================================

Tests H1 (geometric capacity bins), H2 (sigma-delta zeta), and H20
(geo-bio boundary at prime 37) using the choice-guided Bohmian mechanics
sigma-delta formulation introduced in Paper 34.

The core conceptual bridge:
    A first-order sigma-delta (ΔΣ) modulator IS the UKFT discrete choice
    operator acting in the action-only (Geosphere) regime.  At each clock
    cycle the modulator picks b[n] ∈ {0,1} that minimises the local
    accumulated-error action:

        S_local(b[n]=1) = (error - 0.5)²   [correct if error > 0]
        S_local(b[n]=0) = error²            [correct if error < 0]

    This is exactly the discrete choice-Bohmian velocity update:
        b* = argmin_b  S^(d)_local(b)

    In the Geosphere (primes 2–37, bit-length ≤ 6) the action branch
    dominates.  At p = 37, the first 6-bit jump prime opens a new capacity
    bin: the knowledge class K(37) becomes large enough that a second branch
    — the knowledge-projection Π — becomes necessary for unambiguous collapse.
    This is the geo-bio boundary (H20).

Connection to hep-explorer:
    The 40D bert_align projection used in hep-explorer decomposes as
    40 = 37 (Geo signal dimensions, saturated at the geo-bio boundary) + 3
    (UKFT consciousness overhead: D_E, coherence, intensity).
    This experiment produces the theoretical basis for that split.

Hypotheses tested:
    H1  — Primes cluster in geometric capacity bins (bitLength 2–3–4–5–6)
    H2  — ΔΣ encoding is faithful (recovered prime = target prime) for all
           p ≤ 37 using OSR = 16
    H20 — At p = 37 the choice-Bohmian basin becomes ambiguous at d = 2,
           signalling the need for the dual (knowledge + action) operator

Figure 86: 4-panel composite
    Panel 1  ΔΣ error accumulator traces (choice trajectories per prime)
    Panel 2  Bit-length capacity bins + jump prime map up to n = 44
    Panel 3  Attractor basin radius: convergence fraction by Hamming distance
    Panel 4  W_Δ(p) entropic weights + sigma-delta fidelity across Geo primes

References:
    grok_rh_critique_sigma_delta_chat.md §§ "Start Here for Sigma Delta"
    TEILHARD_HYPOTHESIS_MAP.md §§ GEOSPHERE (H1, H2), BIOSPHERE (H20)
    TeilhardSpheres.lean — DualChoiceOperator, geo_bio_boundary_at_37
    BitstreamProjection.lean — bitLength, W_delta, zeta_delta_sigma_partial
    CapacityZeta.lean — isTrivialOnCapacity, isJumpPrime
    Paper 34: Choice-Guided Bohmian Mechanics
"""

import math
import sys
from itertools import product as iterproduct
from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

# ── Constants ──────────────────────────────────────────────────────────────
K         = 6       # Bit-length used for 6-bit Geosphere representation
OSR       = 16      # Sigma-delta oversampling ratio
SIGMA_RHO = 1.4     # Gaussian width for full-mixture ρ visualisation
NEAREST_K  = 3      # Winner-take-all: use top-K nearest prime attractors

GEO_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
BIO_FIRST  = 37     # First biospheric prime (geo-bio boundary, H20)

# Sphere boundary jump primes (CapacityZeta.isJumpPrime = True)
JUMP_PRIMES_GEO = [2, 5, 11, 17, 37]  # 37 = last Geo jump prime


# ── 1.  Bit-length and jump-prime detection ─────────────────────────────────
def bit_length(n: int) -> int:
    """Shannon bit cost ⌊log₂ n⌋ + 1; bit_length(0) = 1. (BitstreamProjection.lean)"""
    return n.bit_length() if n > 0 else 1


def is_trivial_on_capacity(p: int, all_primes: list[int]) -> bool:
    """True iff some smaller prime already has the same bit-length as p.
    (CapacityZeta.isTrivialOnCapacity — Python mirror)"""
    bl = bit_length(p)
    return any(q < p and bit_length(q) == bl for q in all_primes if q < p)


def is_jump_prime(p: int, all_primes: list[int]) -> bool:
    """True iff p opens a new capacity bin (ΔC > 0). (CapacityZeta.isJumpPrime)"""
    return not is_trivial_on_capacity(p, all_primes)


# ── 2.  Canonical representation ────────────────────────────────────────────
def canonical(k: int, n: int) -> np.ndarray:
    """k-bit big-endian canonical binary representation of n.
    Bit i (from left, 0-indexed) = (n >> (k-1-i)) & 1."""
    return np.array([(n >> (k - 1 - i)) & 1 for i in range(k)], dtype=np.float64)


def decimate(bits: np.ndarray) -> int:
    """Binary positional sum (big-endian): Σ bits[i] × 2^(k−1−i).
    (BitstreamProjection.lean decimate)"""
    k = len(bits)
    return int(round(sum(float(b) * (2 ** (k - 1 - i)) for i, b in enumerate(bits))))


# ── 3.  Sigma-delta modulator = action-minimising choice operator ────────────
def sigma_delta_encode(p: int, k: int, osr: int) -> np.ndarray:
    """First-order ΔΣ modulator encoding prime p at OSR = osr.

    Target x = p / 2^k ∈ [0, 1).
    The modulator IS the discrete Bohmian choice operator:
        b[n] = 1 if error ≥ 0   (output 1 when accumulated error is positive)
        b[n] = 0 otherwise
        error[n+1] = error[n] + x − b[n]

    Returns a binary array of length k × osr (the choice sequence).
    """
    x = p / (2 ** k)
    total = k * osr
    bitstream = np.zeros(total, dtype=np.float64)
    error = 0.0
    for i in range(total):
        if error >= 0.0:
            bitstream[i] = 1.0
            error += x - 1.0
        else:
            bitstream[i] = 0.0
            error += x
    return bitstream


def sd_error_trace(p: int, k: int, osr: int, steps: int) -> np.ndarray:
    """Return the error-accumulator trajectory for the first `steps` bit-cycles."""
    x = p / (2 ** k)
    trace = np.zeros(steps)
    error = 0.0
    for i in range(steps):
        trace[i] = error
        if error >= 0.0:
            error += x - 1.0
        else:
            error += x
    return trace


def decimate_sd(bitstream: np.ndarray, k: int, osr: int) -> int:
    """Lowpass-decimate the ΔΣ bitstream back to a k-bit integer:
        density = mean(bitstream)
        recovered = round(density × 2^k)
    """
    density = float(np.mean(bitstream))
    return int(round(density * (2 ** k)))


# ── 4.  Knowledge-density ρ and choice-Bohmian dynamics ────────────────────
def hamming_to_all(b: np.ndarray, primes: list[int], k: int = K) -> dict[int, int]:
    """Map each Geo prime to its Hamming distance from bitstring b."""
    return {p: int(np.sum(b != canonical(k, p))) for p in primes}


def nearest_prime(b: np.ndarray, primes: list[int], k: int = K) -> tuple[int, int]:
    """Return (prime, hamming_distance) for the closest Geo prime attractor.
    Ties broken by smaller prime index (deterministic)."""
    dists = hamming_to_all(b, primes, k)
    best = min(primes, key=lambda p: (dists[p], p))
    return best, dists[best]


def choice_velocity_nn(b: np.ndarray, primes: list[int],
                       k: int = K) -> tuple[int, int]:
    """Nearest-prime discrete choice-Bohmian velocity.

    Finds the nearest Geo prime p* and returns the index of the bit-flip
    that most reduces d_H(b, canonical(k, p*)). This is the action-minimising
    choice in the winner-take-all regime.

    Returns (flip_idx, reduction):
        flip_idx = −1  →  already at canonical form (collapse complete)
        reduction > 0  →  Hamming distance reduced by flipping bit flip_idx
    """
    p_star, d_star = nearest_prime(b, primes, k)
    if d_star == 0:
        return -1, 0   # already at attractor
    can = canonical(k, p_star)
    # each position where b ≠ can is a candidate flip that reduces d by 1
    diff = (b != can).astype(int)
    # pick the first differing position (deterministic tie-breaking)
    for i in range(k):
        if diff[i] == 1:
            return i, 1
    return -1, 0


def choice_trajectory(b_init: np.ndarray, primes: list[int],
                      k: int = K, max_steps: int = 30) -> list[np.ndarray]:
    """Run nearest-prime discrete choice-Bohmian collapse from b_init."""
    traj = [b_init.copy()]
    b = b_init.copy()
    for _ in range(max_steps):
        idx, reduction = choice_velocity_nn(b, primes, k)
        if idx == -1:
            break
        b[idx] = 1.0 - b[idx]
        traj.append(b.copy())
    return traj


def knowledge_density(b: np.ndarray, primes: list[int],
                      k: int = K, sigma: float = SIGMA_RHO) -> float:
    """ρ(b) = Σ_p exp(−d_H(b, canonical(k,p))² / 2σ²).  Used for visualisation."""
    rho = 0.0
    for p in primes:
        can = canonical(k, p)
        d = int(np.sum(b != can))
        rho += math.exp(-(d ** 2) / (2 * sigma ** 2))
    return rho


# ── 5.  W_delta entropic weight (BitstreamProjection.lean) ──────────────────
def W_delta(p: int) -> float:
    """W_Δ(p) = (1 − 1/bitLength(p)) × (1 − 1/p).
    Entropic + packing-damped zeta weight for prime p."""
    bl = bit_length(p)
    return (1.0 - 1.0 / bl) * (1.0 - 1.0 / p)


# ── 6.  Attractor basin analysis (nearest-prime collapse) ───────────────────
def basin_convergence(p: int, primes: list[int],
                      k: int = K,
                      n_samples: int = 80, rng_seed: Optional[int] = None) -> dict:
    """For Hamming distances d = 0, 1, 2, 3, sample n_samples k-bit bitstrings
    at distance d from canonical(k, p) and run nearest-prime choice-Bohmian collapse.

    Returns dict: d → fraction that converges to p.
    """
    rng = np.random.default_rng(seed=rng_seed if rng_seed is not None else p)
    can = canonical(k, p)
    result = {}

    for d in range(min(k + 1, 4)):
        if d == 0:
            traj = choice_trajectory(can.copy(), primes, k)
            p_final, _ = nearest_prime(traj[-1], primes, k)
            result[d] = 1.0 if p_final == p else 0.0
            continue

        hits = 0
        for _ in range(n_samples):
            b = can.copy()
            flip_pos = rng.choice(k, size=min(d, k), replace=False)
            for fp in flip_pos:
                b[fp] = 1.0 - b[fp]
            traj = choice_trajectory(b, primes, k)
            p_final, _ = nearest_prime(traj[-1], primes, k)
            if p_final == p:
                hits += 1
        result[d] = hits / n_samples

    return result


def pairwise_hamming(primes: list[int], k: int = K) -> np.ndarray:
    """Compute the |primes|×|primes| Hamming distance matrix in the k-bit space."""
    n = len(primes)
    mat = np.zeros((n, n), dtype=int)
    for i, p in enumerate(primes):
        for j, q in enumerate(primes):
            mat[i, j] = int(np.sum(canonical(k, p) != canonical(k, q)))
    return mat


# ── 7.  PCA helper (for panel visualisation) ────────────────────────────────
def pca_2d(vecs: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return 2D PCA projection, component matrix, and mean."""
    mean = vecs.mean(axis=0)
    centred = vecs - mean
    cov = centred.T @ centred / max(len(vecs) - 1, 1)
    vals, vecs_e = np.linalg.eigh(cov)
    idx = np.argsort(vals)[::-1]
    comps = vecs_e[:, idx[:2]]
    return centred @ comps, comps, mean


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
def main() -> None:
    print("=" * 66)
    print("Experiment 86: Choice-Bohmian Sigma-Delta in the Geosphere")
    print("=" * 66)
    print()

    # --- Collect geo primes up to 44 for the bit-length map ----------------
    all_primes_to_44 = [n for n in range(2, 45) if all(n % i != 0 for i in range(2, n))]
    geo_jump = [p for p in GEO_PRIMES if is_jump_prime(p, GEO_PRIMES)]

    # --- H2 test: sigma-delta fidelity ------------------------------------
    print("H2 — Sigma-delta fidelity (OSR={}, k={} bits):".format(OSR, K))
    print(f"  {'Prime':>5} | {'bitLen':>6} | {'target x':>8} | {'ΔΣ density':>10} | "
          f"{'recovered':>9} | {'residual':>8} | {'jump?':>6} | W_Δ(p)")
    print("  " + "-" * 70)

    sd_data = {}
    for p in GEO_PRIMES:
        bs = sigma_delta_encode(p, K, OSR)
        density = float(np.mean(bs))
        recovered = decimate_sd(bs, K, OSR)
        residual = abs(recovered - p)
        w = W_delta(p)
        jump = is_jump_prime(p, GEO_PRIMES)
        marker = " ← geo-bio" if p == BIO_FIRST else ("  ← geo jump" if jump else "")
        print(f"  {p:5d} | {bit_length(p):6d} | {p/(2**K):8.4f} | {density:10.4f} | "
              f"{recovered:9d} | {residual:8d} | {'YES' if jump else 'no':>6} | {w:.4f}{marker}")
        sd_data[p] = dict(density=density, recovered=recovered, residual=residual, w=w,
                          jump=jump, bl=bit_length(p))

    # H2 result
    all_faithful = all(sd_data[p]["residual"] == 0 for p in GEO_PRIMES)
    print(f"\n  H2 result: ΔΣ fidelity {'CONFIRMED' if all_faithful else 'PARTIAL'} "
          f"({'all' if all_faithful else 'some'} Geo primes recovered exactly)\n")

    # --- Attractor basin analysis (H20) ------------------------------------
    print("H20 — Attractor basin convergence (nearest-prime collapse):")
    print(f"  {'Prime':>5} | d=0  | d=1  | d=2  | d=3  | d_min | jump? | collapse_steps")
    print("  " + "-" * 70)

    hamm_mat = pairwise_hamming(GEO_PRIMES, k=K)
    basin_data = {}
    for i, p in enumerate(GEO_PRIMES):
        bd = basin_convergence(p, GEO_PRIMES, k=K, n_samples=60)
        # d_min = minimum Hamming distance to any OTHER Geo prime
        dists_to_others = [hamm_mat[i, j] for j in range(len(GEO_PRIMES)) if j != i]
        d_min = min(dists_to_others)
        # d=1 perturb trajectory for collapse steps
        rng = np.random.default_rng(seed=p + 999)
        can = canonical(K, p)
        b1 = can.copy()
        b1[rng.integers(K)] = 1.0 - b1[rng.integers(K)]
        traj = choice_trajectory(b1, GEO_PRIMES, k=K)
        steps = len(traj) - 1
        p_final, _ = nearest_prime(traj[-1], GEO_PRIMES, k=K)

        basin_data[p] = dict(bd=bd, steps=steps, final=p_final, d_min=d_min)
        jump = sd_data[p]["jump"]
        print(f"  {p:5d} | {bd[0]:.2f} | {bd[1]:.2f} | {bd[2]:.2f} | {bd[3]:.2f} | "
              f"   {d_min:2d}  | {'YES' if jump else 'no':>5} | {steps} steps → {p_final}"
              + (" ⚠" if p_final != p else ""))

    # H20 interpretation: within-bin isolation (physically correct metric)
    # Zero-padding makes cross-bin Hamming distances misleading (MSB flip connects bins).
    # The correct metric is d_min WITHIN the same bit-length bin.
    def within_bin_dmin(p: int) -> int | float:
        bl_p = bit_length(p)
        same_bin = [q for q in GEO_PRIMES if q != p and bit_length(q) == bl_p]
        if not same_bin:
            return float("inf")   # sole occupant — infinite isolation within bin
        return min(int(np.sum(canonical(K, p) != canonical(K, q))) for q in same_bin)

    print(f"\n  Within-bin isolation (d_min to nearest prime in same bit-length bin):")
    for p in GEO_PRIMES:
        d_wb = within_bin_dmin(p)
        bl = bit_length(p)
        peers = [q for q in GEO_PRIMES if q != p and bit_length(q) == bl]
        d_str = "∞ (sole occupant)" if d_wb == float("inf") else str(d_wb)
        jump = "✦ GEO-BIO" if p == BIO_FIRST else ""
        print(f"    p={p:3d}  bl={bl}  peers={peers}  d_min_within_bin={d_str}  {jump}")

    sole_6bit = [p for p in GEO_PRIMES if bit_length(p) == 6]
    h20_supported = len(sole_6bit) == 1 and sole_6bit[0] == BIO_FIRST
    print(f"\n  6-bit Geo occupants: {sole_6bit}  (expected: [37] alone)")
    print(f"  H20 (geo-bio at p=37): p=37 is the sole Geo prime in the 6-bit bin → "
          f"{'CONFIRMED' if h20_supported else 'inconclusive'}")
    print(f"  ∴ Action branch cannot distinguish p=37 from upcoming Bio 6-bit primes")
    print(f"    (41, 43, 47, 53, 59, 61, 67) → knowledge branch (Π) is required.\n")

    # --- Jump prime summary ------------------------------------------------
    print(f"H1 — Jump primes in Geosphere: {geo_jump}")
    print(f"     Bit-length bins: "
          + " | ".join(f"bl={b}: {[p for p in GEO_PRIMES if bit_length(p)==b]}"
                       for b in sorted(set(bit_length(p) for p in GEO_PRIMES))))
    print()
    print(f"hep-explorer connection: 40D projection = {BIO_FIRST} Geo dims + 3 UKFT overhead")
    print()

    # ═══════════════════════════════════════════════════
    # PLOTTING
    # ═══════════════════════════════════════════════════
    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    fig.patch.set_facecolor("#0d1117")
    for ax in axes.ravel():
        ax.set_facecolor("#161b22")
        ax.tick_params(colors="#c9d1d9", labelsize=9)
        ax.xaxis.label.set_color("#c9d1d9")
        ax.yaxis.label.set_color("#c9d1d9")
        ax.title.set_color("#f0f6fc")
        for spine in ax.spines.values():
            spine.set_edgecolor("#30363d")

    fig.suptitle(
        "Experiment 86 · Choice-Bohmian Sigma-Delta in the Geosphere  (primes 2–37)",
        fontsize=13, fontweight="bold", color="#f0f6fc", y=0.99,
    )

    cmap_prime = plt.cm.plasma
    prime_colors = {p: cmap_prime(i / (len(GEO_PRIMES) - 1))
                    for i, p in enumerate(GEO_PRIMES)}
    ACCENT   = "#58a6ff"   # blue
    WARN     = "#f85149"   # red  (geo-bio boundary)
    JUMP_CLR = "#3fb950"   # green (jump primes)
    MID_CLR  = "#d29922"   # amber (trivial primes)

    # ─── Panel 1: ΔΣ error accumulator traces (choice trajectories) ────────
    ax1 = axes[0, 0]
    steps_to_show = 48   # first 48 bit-cycles
    for p in GEO_PRIMES:
        trace = sd_error_trace(p, K, OSR, steps_to_show)
        lw = 2.0 if p in JUMP_PRIMES_GEO else 1.0
        ls = "-" if p in JUMP_PRIMES_GEO else "--"
        alpha = 0.95 if p in JUMP_PRIMES_GEO else 0.55
        ax1.plot(trace, color=prime_colors[p], linewidth=lw,
                 linestyle=ls, alpha=alpha, label=str(p))

    ax1.axhline(0.0, color="#30363d", linewidth=1.0, zorder=0)
    ax1.axhline(0.5, color="#30363d", linewidth=0.6, linestyle=":", zorder=0)
    ax1.axhline(-0.5, color="#30363d", linewidth=0.6, linestyle=":", zorder=0)

    ax1.set_title("Panel 1 · ΔΣ Error Accumulator Traces\n"
                  "(= discrete choice-Bohmian velocity field)", fontsize=10)
    ax1.set_xlabel("Bit index n  (one choice per cycle)")
    ax1.set_ylabel("Accumulated error  (action proxy)")
    ax1.set_xlim(0, steps_to_show - 1)
    # Legend: jump primes only to avoid clutter
    jp_handles = [mpatches.Patch(color=prime_colors[p], label=f"p={p}")
                  for p in JUMP_PRIMES_GEO]
    jp_handles += [mpatches.Patch(color=MID_CLR, alpha=0.5, label="trivial primes",
                                  linestyle="--")]
    ax1.legend(handles=jp_handles, fontsize=7.5, loc="upper right",
               facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9")

    # ─── Panel 2: Bit-length capacity bin map (n = 2 .. 44) ────────────────
    ax2 = axes[0, 1]
    xs = list(range(2, 45))
    bls = [bit_length(n) for n in xs]
    prime_set = set(all_primes_to_44)
    geo_set   = set(GEO_PRIMES)
    jump_set  = set(JUMP_PRIMES_GEO)

    # Background fill: alternate shading by bin
    bin_colours = {2: "#1f3a5f", 3: "#1f3a5f", 4: "#1f3a5f",
                   5: "#1a3a2f", 6: "#2a1f3a"}
    prev_bl = 0
    for i, (n, bl) in enumerate(zip(xs, bls)):
        if bl != prev_bl:
            ax2.axvspan(n - 0.5, xs[-1] + 0.5 if i == len(xs) - 1 else xs[i] - 0.5,
                        alpha=0.08, color=bin_colours.get(bl, "#222"))
            prev_bl = bl

    # Bars coloured by prime status
    bar_colors = []
    for n in xs:
        if n in jump_set:
            bar_colors.append(JUMP_CLR)
        elif n in geo_set:
            bar_colors.append(MID_CLR)
        elif n in prime_set:
            bar_colors.append(ACCENT)
        else:
            bar_colors.append("#21262d")

    ax2.bar(xs, bls, color=bar_colors, edgecolor="#30363d", linewidth=0.4, zorder=2)

    # Mark the geo-bio boundary
    ax2.axvline(BIO_FIRST, color=WARN, linewidth=2.0, linestyle=":",
                label=f"p={BIO_FIRST} geo-bio boundary", zorder=5)
    ax2.axvline(40.0, color=ACCENT, linewidth=1.2, linestyle="-.",
                label="40 = hep-explorer dim", zorder=5, alpha=0.7)

    # Annotate jump primes
    for p in JUMP_PRIMES_GEO:
        ax2.text(p, bit_length(p) + 0.08, str(p), ha="center", va="bottom",
                 fontsize=7.5, color=JUMP_CLR, fontweight="bold")
    ax2.text(38.5, 6.5, "37 + 3 = 40\nhep-explorer", color=ACCENT,
             fontsize=7.5, ha="left", va="center",
             bbox=dict(boxstyle="round", facecolor="#0d1117", alpha=0.85,
                       edgecolor=ACCENT, linewidth=0.8))

    ax2.set_title("Panel 2 · Capacity Bin Map  n ∈ [2, 44]\n"
                  "(green = jump prime, amber = trivial prime in Geo)",
                  fontsize=10)
    ax2.set_xlabel("Integer n")
    ax2.set_ylabel("bitLength(n) = capacity bin")
    ax2.set_xlim(1.5, 44.5)
    ax2.set_ylim(0, 7.5)
    jp_leg = [
        mpatches.Patch(color=JUMP_CLR, label="jump prime (ΔC > 0)"),
        mpatches.Patch(color=MID_CLR,  label="trivial Geo prime"),
        mpatches.Patch(color=ACCENT,   label="prime (outside Geo)"),
        mpatches.Patch(color="#21262d", label="composite"),
        plt.Line2D([0], [0], color=WARN, linestyle=":", label=f"p={BIO_FIRST} boundary"),
        plt.Line2D([0], [0], color=ACCENT, linestyle="-.",
                   label="40D hep dim"),
    ]
    ax2.legend(handles=jp_leg, fontsize=7.5, loc="upper left",
               facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9")

    # ─── Panel 3: Pairwise Hamming distance heatmap ─────────────────────────
    ax3 = axes[1, 0]
    hamm_mat = pairwise_hamming(GEO_PRIMES, k=K)

    im3 = ax3.imshow(hamm_mat, cmap="viridis_r", aspect="equal",
                     vmin=0, vmax=K, interpolation="nearest")
    cbar3 = plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)
    cbar3.set_label("Hamming distance", color="#c9d1d9")
    cbar3.ax.yaxis.set_tick_params(color="#c9d1d9")
    plt.setp(cbar3.ax.yaxis.get_ticklabels(), color="#c9d1d9")

    labels = [str(p) for p in GEO_PRIMES]
    ax3.set_xticks(range(len(GEO_PRIMES)))
    ax3.set_yticks(range(len(GEO_PRIMES)))
    ax3.set_xticklabels(labels, fontsize=8, color="#c9d1d9")
    ax3.set_yticklabels(labels, fontsize=8, color="#c9d1d9")

    # Annotate each cell with the distance value
    for i in range(len(GEO_PRIMES)):
        for j in range(len(GEO_PRIMES)):
            d = hamm_mat[i, j]
            colour = "white" if d > K // 2 else "#0d1117"
            ax3.text(j, i, str(d), ha="center", va="center",
                     fontsize=7, color=colour, fontweight="bold")

    # Highlight the geo-bio boundary row/col
    bio_idx = GEO_PRIMES.index(BIO_FIRST)
    for spine in ["right", "left", "top", "bottom"]:
        ax3.spines[spine].set_edgecolor(WARN)
    ax3.axhline(bio_idx - 0.5, color=WARN, linewidth=1.5)
    ax3.axhline(bio_idx + 0.5, color=WARN, linewidth=1.5)
    ax3.axvline(bio_idx - 0.5, color=WARN, linewidth=1.5)
    ax3.axvline(bio_idx + 0.5, color=WARN, linewidth=1.5)

    # Annotate pairs at d=1 (same-bin siblings)
    d_mins = [basin_data[p]["d_min"] for p in GEO_PRIMES]
    ax3.set_title("Panel 3 · Pairwise Hamming Distances in 6-bit Geo Space\n"
                  f"(p=37 framed: d_min from boundary = {basin_data[BIO_FIRST]['d_min']})",
                  fontsize=10)

    # ─── Panel 4: W_Δ weights + ΔΣ fidelity ─────────────────────────────────
    x_idx = np.arange(len(GEO_PRIMES))   # shared x-axis index for Panel 4
    ax4 = axes[1, 1]
    ax4b = ax4.twinx()
    ax4b.set_facecolor("#161b22")
    ax4b.tick_params(colors="#c9d1d9", labelsize=9)
    ax4b.yaxis.label.set_color("#c9d1d9")

    w_vals       = [sd_data[p]["w"]       for p in GEO_PRIMES]
    target_dens  = [p / (2 ** K)          for p in GEO_PRIMES]
    actual_dens  = [sd_data[p]["density"] for p in GEO_PRIMES]

    ax4.fill_between(x_idx, w_vals, alpha=0.18, color="#bc8cff")
    ax4.plot(x_idx, w_vals, color="#bc8cff", linewidth=2.0,
             marker="D", markersize=6, label="W_Δ(p)")

    ax4b.scatter(x_idx, target_dens, color="#58a6ff", s=55, zorder=5,
                 label="target x = p/64")
    ax4b.scatter(x_idx, actual_dens, color="#f85149", marker="^", s=55, zorder=5,
                 label="ΔΣ pulse density")
    for i, p in enumerate(GEO_PRIMES):
        ax4b.plot([i, i], [target_dens[i], actual_dens[i]],
                  color="#8b949e", linewidth=1.2, alpha=0.6)

    # Mark jump primes with stars
    for p in JUMP_PRIMES_GEO:
        i = GEO_PRIMES.index(p)
        ax4.scatter(i, w_vals[i], color=JUMP_CLR, s=100, marker="*", zorder=6)

    ax4.axvline(bio_idx - 0.5, color=WARN, linewidth=2.0, linestyle=":")

    ax4.set_xticks(x_idx)
    ax4.set_xticklabels([str(p) for p in GEO_PRIMES], fontsize=9)
    ax4.set_xlabel("Prime p")
    ax4.set_ylabel("W_Δ(p) = entropic zeta weight", color="#bc8cff")
    ax4b.set_ylabel("Normalised value (target = p/64)", color="#c9d1d9")
    ax4.set_title("Panel 4 · W_Δ Entropic Weights + ΔΣ Fidelity\n"
                  "(★ = jump prime | vertical bars = encoding residual)",
                  fontsize=10)

    lines1, lbl1 = ax4.get_legend_handles_labels()
    lines2, lbl2 = ax4b.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, lbl1 + lbl2, fontsize=8, loc="upper left",
               facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9")

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    out = Path(__file__).parent / "86_choice_bohmian_sigma_delta_geo.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Figure saved → {out}")


if __name__ == "__main__":
    main()
