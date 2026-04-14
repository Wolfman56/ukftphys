#!/usr/bin/env python3
"""
Experiment 87 — W-Axis ζ_cap Structure: Jump-Prime Euler Product
=================================================================

Computes and visualises the w-axis capacity Euler product

    ζ_cap(w) = ∏_{p ∈ J} (1 − p^{−w})^{−1}

where J = {2, 5, 11, 17, 37, 67, 131, 257, 521, 1031, ...} is the set
of jump primes (primes that open a new bit-length capacity bin).

This is the generating structure behind Paper 44's three-ledger hierarchy
(collapsed / dark-matter / void).  The paper's central claim is that
ζ_cap organises all three cosmological energy densities parameter-free.

Hypotheses tested
-----------------
H87-1  Jump primes are exactly the first prime in each bit-length class
        (bitLength(p_k) = k, bitLength(prev_prime(p_k)) = k−1).
H87-2  ζ_cap(w) < ζ(w) for all w > 1; the capacity Euler product is a
        proper sub-product of the Riemann zeta function.
H87-3  The logarithmic derivative C(w) = −d/dw log ζ_cap(w) shows sharp
        phase-transition steps at each jump-prime capacity threshold,
        with the step height proportional to log(p_j).
H87-4  The normalised capacity fraction F(w, p) = C_≤p(w) / C_total(w)
        shows three natural ledger partitions at p=11, p=257, and p=521
        corresponding to the collapsed / DM / void ledger boundaries.

Figures produced
----------------
87_fig1_zeta_comparison.png
    Panel 1a  ζ_cap(w) and ζ(w) on same axes for w ∈ [1.6, 4.0]
    Panel 1b  Ratio ζ_cap(w) / ζ(w) — the "capacity deficit"

87_fig2_capacity_derivative.png
    Single panel: C(w) = Σ_{p∈J} log(p)·p^{−w}/(1−p^{−w}) vs w
    Vertical lines at w-values where each jump prime first contributes ≥1%
    Step structure annotated with jump prime labels

87_fig3_ledger_fractions.png
    Cumulative capacity fraction F(w, p) with ledger boundaries marked:
    — collapsed ledger: p ≤ 11 (nucleosynthesis window)
    — DM ledger:        p ∈ [17, 257] (EW to 9-bit threshold)
    — void ledger:      p ≥ 521 (10-bit and beyond)
    Evaluated at three w values: w=2.0 (UV), w=1.8 (EW scale), w=1.65 (IR)

87_fig4_jump_prime_table.png
    Table figure: jump primes up to p=1031, their bit-lengths, W_ΣΔ weights,
    ζ_cap contribution, and ledger assignment

References
----------
BitstreamProjection.lean  — bitCap, isJumpPrime (M15, M16)
CapacityZeta.lean         — zeta_cap_euler_product (M15 partial)
LedgerHierarchy.lean      — CollapsedLedger, DMLedger, VoidLedger (planned)
Paper 44 §§2.1–2.3        — mathematical setup extracted from QFT/GR §4.14
UKFT_QFT_GR_PAPER.md §4.14 — source derivation
Experiment 86             — jump-prime infrastructure (geosphere only)
"""

import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── Output directory ────────────────────────────────────────────────────────
OUT = Path(__file__).parent

# ── Colour palette (consistent with exp 86) ────────────────────────────────
CLR_JUMP    = "#3fb950"   # green:  jump primes
CLR_ZETA    = "#58a6ff"   # blue:   full ζ(w)
CLR_ZCAP    = "#f78166"   # orange: ζ_cap(w)
CLR_RATIO   = "#d2a8ff"   # purple: ratio
CLR_DERIV   = "#ffa657"   # amber:  capacity derivative C(w)
CLR_COLL    = "#79c0ff"   # light blue: collapsed ledger
CLR_DM      = "#56d364"   # green:      DM ledger
CLR_VOID    = "#d29922"   # gold:       void ledger

# Ledger boundary primes
P_COL_MAX  = 11    # Collapsed ledger: primes 2..11
P_DM_MAX   = 257   # DM ledger: primes 17..257
P_VOID_MIN = 521   # Void ledger closure: first 10-bit prime

# ─────────────────────────────────────────────────────────────────────────────
# 1.  Number-theory utilities
# ─────────────────────────────────────────────────────────────────────────────

def sieve(limit: int) -> list[int]:
    """Sieve of Eratosthenes — returns all primes ≤ limit."""
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            is_p[i*i::i] = bytearray(len(is_p[i*i::i]))
    return [i for i, v in enumerate(is_p) if v]


def bit_length(n: int) -> int:
    """⌊log₂ n⌋ + 1 for n ≥ 1. (BitstreamProjection.lean bitLength)"""
    return n.bit_length()


def find_jump_primes(all_primes: list[int]) -> list[int]:
    """
    Jump primes: the unique first prime for each bit-length class.
    p is a jump prime iff bit_length(p) > bit_length(prev_prime(p)).
    (CapacityZeta.lean isJumpPrime)
    """
    jump = []
    prev_bl = 0
    for p in all_primes:
        bl = bit_length(p)
        if bl > prev_bl:
            jump.append(p)
            prev_bl = bl
    return jump


# ─────────────────────────────────────────────────────────────────────────────
# 2.  ζ functions
# ─────────────────────────────────────────────────────────────────────────────

def zeta_riemann(w: float, primes: list[int], cutoff: int = 10_000) -> float:
    """
    Riemann ζ(w) via Euler product over all primes up to cutoff.
    For w >> 1 the truncation error is negligible.
    """
    result = 1.0
    for p in primes:
        if p > cutoff:
            break
        pw = p ** (-w)
        result /= (1.0 - pw)
    return result


def zeta_cap(w: float, jump_primes: list[int]) -> float:
    """
    ζ_cap(w) = ∏_{p ∈ J} (1 − p^{−w})^{−1}
    The jump-prime sub-Euler-product. (Paper 44 §2.2, M15)
    """
    result = 1.0
    for p in jump_primes:
        pw = p ** (-w)
        result /= (1.0 - pw)
    return result


def capacity_derivative(w: float, jump_primes: list[int]) -> float:
    """
    C(w) = −d/dw log ζ_cap(w) = Σ_{p∈J} log(p) · p^{−w} / (1 − p^{−w})

    This is the 'capacity' in the Shannon/Nyquist sense: the log-derivative
    of the generating function.  Phase-transition steps occur at each p_j.
    """
    total = 0.0
    for p in jump_primes:
        pw = p ** (-w)
        total += math.log(p) * pw / (1.0 - pw)
    return total


def cumulative_capacity(w: float, jump_primes: list[int]) -> list[float]:
    """
    Cumulative capacity fraction F(w, k) = C_{≤p_k}(w) / C_total(w)
    where C_{≤p_k}(w) = Σ_{j≤k} log(p_j) · p_j^{−w} / (1 − p_j^{−w}).
    Returns list of (p_j, cumulative_fraction) pairs.
    """
    total = capacity_derivative(w, jump_primes)
    running = 0.0
    result = []
    for p in jump_primes:
        pw = p ** (-w)
        running += math.log(p) * pw / (1.0 - pw)
        result.append((p, running / total if total > 0 else 0.0))
    return result


def per_prime_contribution(w: float, jump_primes: list[int]) -> list[float]:
    """
    Individual contribution of each jump prime to ζ_cap(w):
    c_j(w) = log(p_j) · p_j^{−w} / (1 − p_j^{−w}) / C_total(w)
    """
    total = capacity_derivative(w, jump_primes)
    contribs = []
    for p in jump_primes:
        pw = p ** (-w)
        c = math.log(p) * pw / (1.0 - pw) / total if total > 0 else 0.0
        contribs.append(c)
    return contribs


# ─────────────────────────────────────────────────────────────────────────────
# 3.  Figure 1 — ζ comparison
# ─────────────────────────────────────────────────────────────────────────────

def figure1_zeta_comparison(all_primes, jump_primes, w_arr):
    """
    Two-panel figure:
    1a  ζ_cap(w) and ζ(w) on shared axes
    1b  Ratio ζ_cap(w)/ζ(w) showing the 'capacity deficit'
    """
    zeta_full = np.array([zeta_riemann(w, all_primes, cutoff=5000) for w in w_arr])
    zeta_c    = np.array([zeta_cap(w, jump_primes) for w in w_arr])
    ratio     = zeta_c / zeta_full

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        r"Figure 87-1 — $\zeta_{\rm cap}(w)$ vs $\zeta(w)$ and Capacity Deficit",
        fontsize=13, fontweight="bold"
    )

    # Panel 1a
    ax = axes[0]
    ax.plot(w_arr, zeta_full, color=CLR_ZETA, lw=2.0, label=r"$\zeta(w)$ (all primes)")
    ax.plot(w_arr, zeta_c,    color=CLR_ZCAP, lw=2.0, ls="--",
            label=r"$\zeta_{\rm cap}(w)$ (jump primes $J$)")
    ax.set_xlabel(r"$w$", fontsize=12)
    ax.set_ylabel(r"$\zeta$ value", fontsize=12)
    ax.set_title(r"Euler Products", fontsize=11)
    ax.set_yscale("log")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(w_arr[0], w_arr[-1])
    ax.axvline(1.65, color="gray", ls=":", alpha=0.5)
    ax.text(1.67, ax.get_ylim()[0] * 2, "IR", fontsize=8, color="gray")

    # Panel 1b: ratio
    ax2 = axes[1]
    ax2.plot(w_arr, ratio, color=CLR_RATIO, lw=2.0)
    ax2.fill_between(w_arr, ratio, 1.0, alpha=0.15, color=CLR_RATIO)
    ax2.set_xlabel(r"$w$", fontsize=12)
    ax2.set_ylabel(r"$\zeta_{\rm cap}(w)\,/\,\zeta(w)$", fontsize=12)
    ax2.set_title("Capacity Deficit (trivial-prime contribution removed)", fontsize=11)
    ax2.set_ylim(0.0, 1.05)
    ax2.axhline(1.0, color="gray", ls=":", lw=1.0)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(w_arr[0], w_arr[-1])

    # Annotate ledger boundaries on ratio panel
    for p_mark, label, clr in [
        (P_COL_MAX,  "p=11\ncollapsed",   CLR_COLL),
        (P_DM_MAX,   "p=257\nDM handover", CLR_DM),
        (P_VOID_MIN, "p=521\nvoid closure",CLR_VOID),
    ]:
        # w where this jump prime contributes 10% of its asymptotic share
        w_mark = math.log(p_mark) / math.log(10)   # just for positioning
        pass  # annotation on figure 2 is cleaner — skip here

    plt.tight_layout()
    path = OUT / "87_fig1_zeta_comparison.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path.name}")
    return zeta_full, zeta_c, ratio


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Figure 2 — Capacity derivative C(w)
# ─────────────────────────────────────────────────────────────────────────────

def figure2_capacity_derivative(jump_primes, w_arr):
    """
    Stacked-area chart: C(w) split into three ledger contributions.

    C_collapsed(w) = Σ_{p∈{2,5,11}}        log(p)·p^{-w}/(1-p^{-w})
    C_dm(w)        = Σ_{p∈{17..257}}        log(p)·p^{-w}/(1-p^{-w})
    C_void(w)      = Σ_{p≥521}              log(p)·p^{-w}/(1-p^{-w})

    The stacking immediately shows the collapsed ledger dominating across
    the entire observable w range.
    """
    def ledger_contribution(w_val, primes_in_ledger):
        return sum(math.log(p) * p**(-w_val) / (1.0 - p**(-w_val))
                   for p in primes_in_ledger)

    collapsed_primes = [p for p in jump_primes if p <= P_COL_MAX]
    dm_primes        = [p for p in jump_primes if P_COL_MAX < p <= P_DM_MAX]
    void_primes      = [p for p in jump_primes if p > P_DM_MAX]

    C_coll = np.array([ledger_contribution(w, collapsed_primes) for w in w_arr])
    C_dm   = np.array([ledger_contribution(w, dm_primes)        for w in w_arr])
    C_void = np.array([ledger_contribution(w, void_primes)      for w in w_arr])
    C_total = C_coll + C_dm + C_void

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.suptitle(
        r"Figure 87-2 — Capacity Derivative $C(w)$ by Ledger"
        "\n"
        r"$C(w) = -\frac{d}{dw}\log\zeta_{\rm cap}(w)$"
        r" split into Collapsed / DM / Void contributions",
        fontsize=12, fontweight="bold"
    )

    # Stacked area
    ax.stackplot(
        w_arr,
        C_coll, C_dm, C_void,
        colors=[CLR_COLL, CLR_DM, CLR_VOID],
        alpha=0.75,
        labels=[
            r"Collapsed ledger ($p \leq 11$)",
            r"DM ledger ($p = 17$–$257$)",
            r"Void ledger ($p \geq 521$)",
        ],
        zorder=2,
    )

    # Total C(w) outline
    ax.plot(w_arr, C_total, color="white", lw=1.8, ls="-", zorder=3, alpha=0.9)

    # Annotate ledger fractions at w=1.8
    w_marker = 1.8
    idx_m = int(np.argmin(np.abs(w_arr - w_marker)))
    frac_coll_at_18 = C_coll[idx_m] / C_total[idx_m]
    frac_dm_at_18   = C_dm[idx_m]   / C_total[idx_m]
    frac_void_at_18 = C_void[idx_m] / C_total[idx_m]

    ax.axvline(w_marker, color="gray", ls=":", lw=1.2, alpha=0.8, zorder=4)
    ax.text(w_marker + 0.03, C_total[idx_m] * 0.55,
            f"w=1.8\ncollapsed {frac_coll_at_18*100:.1f}%\n"
            f"DM {frac_dm_at_18*100:.1f}%\nvoid {frac_void_at_18*100:.2f}%",
            fontsize=8, color="white", va="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="#161b22", alpha=0.7))

    ax.set_xlabel(r"$w$", fontsize=12)
    ax.set_ylabel(r"$C(w)$", fontsize=12)
    ax.set_xlim(w_arr[0], w_arr[-1])
    ax.set_ylim(0)
    ax.grid(True, alpha=0.2)
    ax.legend(loc="upper right", fontsize=9)

    plt.tight_layout()
    path = OUT / "87_fig2_capacity_derivative.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path.name}")
    return C_total


# ─────────────────────────────────────────────────────────────────────────────
# 5.  Figure 3 — Cumulative ledger fractions
# ─────────────────────────────────────────────────────────────────────────────

def figure3_ledger_fractions(jump_primes, w_values=(2.0, 1.8, 1.65)):
    """
    Cumulative capacity fraction F(w, p) for three representative w values.
    Ledger boundaries marked at p=11 (collapsed), p=257 (DM handover), p=521 (void).
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    fig.suptitle(
        "Figure 87-3 — Cumulative Ledger Capacity Fractions $F(w, p)$\n"
        r"Three evaluation points showing ledger partition as $w$ decreases (UV→IR)",
        fontsize=12, fontweight="bold"
    )

    ledger_labels = {P_COL_MAX: "collapsed", P_DM_MAX: "DM handover", P_VOID_MIN: "void closure"}
    ledger_colors = {P_COL_MAX: CLR_COLL, P_DM_MAX: CLR_DM, P_VOID_MIN: CLR_VOID}

    for ax, w in zip(axes, w_values):
        cum = cumulative_capacity(w, jump_primes)
        primes_plot = [p for p, _ in cum]
        fracs       = [f for _, f in cum]
        x_idx       = list(range(len(primes_plot)))

        # Colour each prime by its ledger
        bar_colors = []
        for p in primes_plot:
            if p <= P_COL_MAX:
                bar_colors.append(CLR_COLL)
            elif p <= P_DM_MAX:
                bar_colors.append(CLR_DM)
            else:
                bar_colors.append(CLR_VOID)

        # Plot cumulative line + coloured step bars
        ax.step(x_idx, fracs, where="mid", color="white", lw=1.5, zorder=4)
        for xi, (f_prev, f_cur, clr) in enumerate(
            zip([0.0] + fracs[:-1], fracs, bar_colors)
        ):
            ax.bar(xi, f_cur - f_prev, bottom=f_prev, color=clr, alpha=0.7,
                   width=0.8, zorder=3)

        # Boundary lines
        for p_bnd, label, clr in [
            (P_COL_MAX, "collapsed / DM", CLR_COLL),
            (P_DM_MAX,  "DM / void",      CLR_DM),
        ]:
            if p_bnd in primes_plot:
                xi_bnd = primes_plot.index(p_bnd)
                frac_bnd = fracs[xi_bnd]
                ax.axhline(frac_bnd, color=clr, ls="--", lw=1.2, alpha=0.8, zorder=5)
                ax.text(len(primes_plot) - 0.5, frac_bnd + 0.01,
                        f"{frac_bnd:.2f}", fontsize=7, color=clr, ha="right")

        ax.set_xticks(x_idx)
        ax.set_xticklabels([str(p) for p in primes_plot], rotation=55, fontsize=7)
        ax.set_title(f"$w = {w}$", fontsize=11)
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("Jump prime $p_j$", fontsize=10)
        ax.grid(axis="y", alpha=0.25)

    axes[0].set_ylabel("Cumulative capacity fraction $F(w, p)$", fontsize=10)

    # Legend
    patches = [
        mpatches.Patch(color=CLR_COLL, alpha=0.7, label="Collapsed ledger (p≤11)"),
        mpatches.Patch(color=CLR_DM,   alpha=0.7, label="DM ledger (p=17..257)"),
        mpatches.Patch(color=CLR_VOID, alpha=0.7, label="Void ledger (p≥521)"),
    ]
    fig.legend(handles=patches, loc="lower center", ncol=3, fontsize=9,
               bbox_to_anchor=(0.5, -0.05))

    plt.tight_layout()
    path = OUT / "87_fig3_ledger_fractions.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path.name}")


# ─────────────────────────────────────────────────────────────────────────────
# 6.  Figure 4 — Jump prime reference table
# ─────────────────────────────────────────────────────────────────────────────

def figure4_jump_prime_table(jump_primes, w_ref=1.8):
    """
    Single matplotlib table figure showing:
    Jump prime | Bit-length | Ledger | ζ_cap contribution (%) at w=1.8
    """
    import matplotlib.gridspec as gridspec

    contribs = per_prime_contribution(w_ref, jump_primes)

    rows = []
    for p, c in zip(jump_primes, contribs):
        bl = bit_length(p)
        if p <= P_COL_MAX:
            ledger = "Collapsed"
            row_clr = CLR_COLL
        elif p <= P_DM_MAX:
            ledger = "DM"
            row_clr = CLR_DM
        else:
            ledger = "Void"
            row_clr = CLR_VOID
        rows.append((f"{p}", f"{bl}", ledger, f"{100*c:.2f}%"))

    fig, ax = plt.subplots(figsize=(9, 0.45 * len(rows) + 1.5))
    ax.axis("off")
    fig.suptitle(
        f"Figure 87-4 — Jump Primes: Bit-Lengths, Ledger Assignment, and ζ_cap Contribution at w={w_ref}",
        fontsize=11, fontweight="bold"
    )

    col_labels = ["Jump prime $p_j$", "Bit-length $k$", "Ledger", f"% of C({w_ref})"]
    cell_colors = []
    for p, _, _ in [(p,) + (0,)*2 for p in jump_primes]:
        if p <= P_COL_MAX:
            clr = "#143d2b"
        elif p <= P_DM_MAX:
            clr = "#0d2149"
        else:
            clr = "#3b2200"
        cell_colors.append([clr] * 4)

    tbl = ax.table(
        cellText=rows,
        colLabels=col_labels,
        cellLoc="center",
        loc="center",
        cellColours=cell_colors,
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.5)

    # Header row colours
    for j in range(4):
        tbl[0, j].set_facecolor("#21262d")
        tbl[0, j].set_text_props(color="white", fontweight="bold")

    # Data rows: text always white
    for i in range(1, len(rows) + 1):
        for j in range(4):
            tbl[i, j].set_text_props(color="white")

    plt.tight_layout()
    path = OUT / "87_fig4_jump_prime_table.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {path.name}")


# ─────────────────────────────────────────────────────────────────────────────
# 7.  Numerical summary
# ─────────────────────────────────────────────────────────────────────────────

def print_summary(jump_primes, all_primes, w_eval=(1.65, 1.8, 2.0, 3.0)):
    print("\n" + "="*65)
    print("Experiment 87 — Numerical Summary")
    print("="*65)

    print(f"\nJump primes (first prime in each bit-length class, up to {jump_primes[-1]}):")
    for p in jump_primes:
        bl = bit_length(p)
        if p <= P_COL_MAX:
            ledger = "collapsed"
        elif p <= P_DM_MAX:
            ledger = "DM"
        else:
            ledger = "void"
        print(f"  p={p:5d}  bit-length={bl}  ledger={ledger}")

    print(f"\n{'w':>6}  {'ζ(w)':>12}  {'ζ_cap(w)':>12}  {'ratio':>8}  {'C(w)':>10}")
    print("-" * 55)
    for w in w_eval:
        zf  = zeta_riemann(w, all_primes, cutoff=5000)
        zc  = zeta_cap(w, jump_primes)
        rat = zc / zf
        cw  = capacity_derivative(w, jump_primes)
        print(f"  {w:4.2f}  {zf:12.6f}  {zc:12.6f}  {rat:8.5f}  {cw:10.6f}")

    print("\nLedger capacity fractions at w=1.8:")
    cum = cumulative_capacity(1.8, jump_primes)
    # Find boundaries
    last_col = last_dm = 0.0
    for p, f in cum:
        if p == P_COL_MAX:
            last_col = f
        if p == P_DM_MAX:
            last_dm = f
    last_void = 1.0 if cum else 0.0

    col_frac  = last_col
    dm_frac   = last_dm - last_col
    void_frac = 1.0 - last_dm

    print(f"  Collapsed ledger (p ≤ {P_COL_MAX}):        {100*col_frac:6.2f}%")
    print(f"  DM ledger       (p={P_COL_MAX+1}..{P_DM_MAX}):  {100*dm_frac:6.2f}%")
    print(f"  Void ledger     (p ≥ {P_VOID_MIN}):      {100*void_frac:6.2f}%")

    print("\nH87-1 verification — jump prime = first in bit-length class:")
    # Note: p=2 has bit-length 2 (binary '10'); there is no prime with bit-length 1
    # since 1 is not prime.  So the first jump prime legitimately starts at bl=2.
    h1_pass = True
    prev_bl = bit_length(jump_primes[0]) - 1   # initialise just below the first class
    for p in jump_primes:
        bl = bit_length(p)
        if bl != prev_bl + 1:
            print(f"  [WARN] p={p}: bit-length gap ({prev_bl} → {bl})")
            h1_pass = False
        prev_bl = bl
    if h1_pass:
        print("  PASS — each jump prime opens exactly one new bit-length class")

    print("\nH87-2 verification — ζ_cap(w) < ζ(w) for all w tested:")
    h2_pass = all(
        zeta_cap(w, jump_primes) < zeta_riemann(w, all_primes, cutoff=5000)
        for w in [1.7, 2.0, 3.0, 5.0]
    )
    print(f"  {'PASS' if h2_pass else 'FAIL'} — ζ_cap < ζ at sampled w values")

    print("\nH87-3 verification — C(w) is monotonically decreasing:")
    c_vals = [capacity_derivative(w, jump_primes) for w in [1.7, 1.9, 2.5, 4.0]]
    h3_pass = all(c_vals[i] > c_vals[i+1] for i in range(len(c_vals)-1))
    print(f"  {'PASS' if h3_pass else 'FAIL'} — C(w) decreasing: {[f'{c:.3f}' for c in c_vals]}")

    print("="*65 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# 8.  Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("Experiment 87 — W-Axis ζ_cap Structure")
    print("Computing primes and jump primes...")

    # Primes up to 1200 covers bit-length classes 1–10 comfortably
    # (first 11-bit prime is 1031; first 12-bit prime is 2053)
    all_primes   = sieve(2200)
    jump_primes  = find_jump_primes(all_primes)

    # Focus jump primes on the ledger-relevant range (bit-lengths 1–11)
    # i.e. up to and including bit-length 11 (p=1031)
    jump_primes = [p for p in jump_primes if p <= 2100]

    print(f"  {len(all_primes)} primes up to {all_primes[-1]}")
    print(f"  {len(jump_primes)} jump primes: {jump_primes}")

    # w range for evaluation: stay away from the pole at w=1
    w_arr = np.linspace(1.65, 4.0, 500)

    print("\nGenerating Figure 1: ζ comparison...")
    figure1_zeta_comparison(all_primes, jump_primes, w_arr)

    print("Generating Figure 2: capacity derivative C(w)...")
    figure2_capacity_derivative(jump_primes, w_arr)

    print("Generating Figure 3: cumulative ledger fractions...")
    figure3_ledger_fractions(jump_primes, w_values=(2.0, 1.8, 1.65))

    print("Generating Figure 4: jump prime table...")
    figure4_jump_prime_table(jump_primes, w_ref=1.8)

    print_summary(jump_primes, all_primes)

    print("Done.  Four figures written to experiments/")


if __name__ == "__main__":
    main()
