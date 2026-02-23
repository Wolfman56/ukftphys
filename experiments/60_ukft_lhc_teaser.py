"""
Experiment 60: UKFT Teaser — From First Principles to Collider Data
====================================================================
A purely illustrative explainer experiment.  No real LHC data required.
All figures use synthetic distributions that are calibrated to match the
qualitative structure observed in the real hep-explorer validation arm.

Four visualisations:

  Fig 1 — The Knowledge Manifold
        Synthetic 2D projection of 7,000 SM events + 12 BSM candidates.
        SM bulk clusters near the manifold core; Borda-12 candidates sit
        as a discrete high-cosine island at the geodesic frontier.

  Fig 2 — The Cosine Distribution (BERT↔UKFT alignment)
        Bimodal histogram: SM bulk peaks near 0.58, Borda-12 near 0.85.
        The clean bimodal separation is the primary discrimination signal.

  Fig 3 — Recall@K Curve
        How many of the 12 BSM candidates land in the top-K events?
        Uniform weights (Phase 13 baseline): 6/12 at K=30.
        Optimal learned weights  (Phase 14): 12/12 at K=20.

  Fig 4 — The Choice-Entanglement Mass Hierarchy  (from Exp 59)
        Bar chart of m_CE by hierarchy level from the simulation arm,
        illustrating the 2535× geo→theo mass amplification.

Paper: UKFT-39
Run:   python experiments/60_ukft_lhc_teaser.py
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import norm, beta as scipy_beta

np.random.seed(2026)

OUT_DIR = os.path.dirname(__file__)

# ── shared aesthetics ───────────────────────────────────────────────────────
DARK_BG   = '#0d0d1a'
GOLD      = '#ffd700'
CYAN      = '#33ccff'
RED       = '#ff4444'
GREEN     = '#44ff88'
GREY      = '#555577'
FONTSIZE  = 12

def dark_fig(w=11, h=7):
    fig = plt.figure(figsize=(w, h), facecolor=DARK_BG)
    return fig

def dark_ax(fig, *args, **kw):
    ax = fig.add_subplot(*args, **kw)
    ax.set_facecolor(DARK_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor('#334')
    ax.tick_params(colors='#aaa', labelsize=10)
    ax.xaxis.label.set_color('#ccc')
    ax.yaxis.label.set_color('#ccc')
    ax.title.set_color('#eee')
    return ax


# ═══════════════════════════════════════════════════════════════════════════
# Fig 1 — The Knowledge Manifold
# ═══════════════════════════════════════════════════════════════════════════

def fig_manifold():
    n_sm    = 7169
    n_bsm   = 12

    # SM bulk: Gaussian blob centred near the manifold core
    sm_x = np.random.randn(n_sm) * 1.8 + 0.0
    sm_y = np.random.randn(n_sm) * 1.2 + 0.0
    # Add some long-range scatter (high-multiplicity SM events)
    tail_idx = np.random.choice(n_sm, 400, replace=False)
    sm_x[tail_idx] += np.random.randn(400) * 3.0
    sm_y[tail_idx] += np.random.randn(400) * 2.5

    # BSM island: compact cluster near (4.5, 3.2) — high geodesic distance from core
    bsm_x = np.random.randn(n_bsm) * 0.35 + 4.5
    bsm_y = np.random.randn(n_bsm) * 0.35 + 3.2

    # UKFT geodesic backbone: parameterised arc from (0,0) to (4.5, 3.2)
    t  = np.linspace(0, 1, 200)
    gx = 4.5 * t + 0.8 * np.sin(np.pi * t)
    gy = 3.2 * t - 0.6 * np.sin(2 * np.pi * t)

    # Cosine colour for SM events (proxy: distance from BSM island)
    cos_sm = 1.0 - np.sqrt((sm_x - 4.5)**2 + (sm_y - 3.2)**2) / 12.0
    cos_sm = np.clip(cos_sm, 0.2, 0.95)

    fig = dark_fig(12, 8)
    ax  = dark_ax(fig, 111)

    sc = ax.scatter(sm_x, sm_y, c=cos_sm, cmap='cool', s=3, alpha=0.35,
                    vmin=0.3, vmax=0.95, rasterized=True)
    ax.plot(gx, gy, color=GOLD, lw=2.0, alpha=0.7, zorder=4,
            label='UKFT geodesic backbone')
    ax.scatter(bsm_x, bsm_y, c=GOLD, s=180, marker='*', zorder=6,
               edgecolors='white', linewidths=0.5, label='BSM candidates (Borda-12)')
    ax.scatter([0], [0], c=GREEN, s=120, marker='D', zorder=5,
               label='Standard Model core')

    # Annotate BSM island
    ax.annotate('BSM island\n(cos ≈ 0.85)', xy=(4.5, 3.2),
                xytext=(5.8, 2.2), fontsize=10, color=GOLD,
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.5))
    ax.annotate('SM bulk\n(cos ≈ 0.58)', xy=(0.3, 0.3),
                xytext=(-4.5, 2.0), fontsize=10, color=CYAN,
                arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.5))

    cbar = fig.colorbar(sc, ax=ax, fraction=0.028, pad=0.02)
    cbar.set_label('BERT↔UKFT cosine alignment', color='#ccc', fontsize=10)
    cbar.ax.yaxis.set_tick_params(color='#aaa')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='#aaa')

    ax.set_title('UKFT Knowledge Manifold — LHC Events (7,181)\n'
                 'BSM candidates cluster at the geodesic frontier', fontsize=13)
    ax.set_xlabel('Manifold coordinate 1 (2D projection)')
    ax.set_ylabel('Manifold coordinate 2')
    ax.legend(fontsize=10, facecolor='#111', edgecolor='#445', labelcolor='#eee')
    ax.set_xlim(-8, 9);  ax.set_ylim(-5, 7)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, '60_manifold_schematic.png'),
                dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print("Saved: 60_manifold_schematic.png")


# ═══════════════════════════════════════════════════════════════════════════
# Fig 2 — Cosine Distribution
# ═══════════════════════════════════════════════════════════════════════════

def fig_cosine():
    # Calibrated to real Phase 12c-reg results:
    # SM bulk: mean≈0.576, std≈0.072
    # Borda:   mean≈0.853, std≈0.022
    n_sm  = 7169
    n_bsm = 12

    cos_sm  = np.clip(np.random.normal(0.576, 0.072, n_sm),  0.0, 1.0)
    cos_bsm = np.clip(np.random.normal(0.853, 0.022, n_bsm), 0.0, 1.0)

    fig = dark_fig(11, 6)
    ax  = dark_ax(fig, 111)

    bins = np.linspace(0.2, 1.01, 70)
    ax.hist(cos_sm,  bins=bins, density=True, color=CYAN,  alpha=0.55,
            label=f'SM bulk (n={n_sm:,})')
    ax.hist(cos_bsm, bins=bins, density=True, color=GOLD,  alpha=0.90,
            label=f'BSM candidates (Borda-12, n={n_bsm})')

    # Smooth KDE overlays
    xs = np.linspace(0.2, 1.0, 400)
    sm_kde  = norm.pdf(xs, 0.576, 0.072)
    bsm_kde = norm.pdf(xs, 0.853, 0.022)
    ax.plot(xs, sm_kde,  color=CYAN,  lw=2.0, alpha=0.8)
    ax.plot(xs, bsm_kde, color=GOLD,  lw=2.0, alpha=0.9)

    # Decision threshold annotation
    thresh = 0.76
    ax.axvline(thresh, color=RED, lw=1.5, ls='--', alpha=0.8,
               label=f'Approximate separation (cos={thresh})')
    ax.annotate('BSM island', xy=(0.86, 8.5), fontsize=11,
                color=GOLD, ha='center', fontweight='bold')
    ax.annotate('SM bulk', xy=(0.55, 2.0), fontsize=11,
                color=CYAN, ha='center')

    ax.set_xlabel('cos(BERT projection, UKFT field)  — alignment score', fontsize=12)
    ax.set_ylabel('Density', fontsize=12)
    ax.set_title('BERT↔UKFT Cosine Distribution\n'
                 'Phase 12c-reg: bimodal step discriminant separates SM from BSM',
                 fontsize=13)
    ax.legend(fontsize=10, facecolor='#111', edgecolor='#445', labelcolor='#eee')
    ax.set_xlim(0.25, 1.02)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, '60_cosine_distribution.png'),
                dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print("Saved: 60_cosine_distribution.png")


# ═══════════════════════════════════════════════════════════════════════════
# Fig 3 — Recall@K Curve
# ═══════════════════════════════════════════════════════════════════════════

def fig_recall():
    n_bsm = 12
    K_max = 60

    # Calibrated to real Phase 13/14 results
    # Uniform (Phase 13): Borda at ranks ~1,2,3,13,25,27 among 7181
    uniform_borda_ranks = sorted([1, 2, 3, 13, 25, 27, 38, 44, 49, 55, 58, 62])
    # Optimal (Phase 14): all 12 within top 20
    optimal_borda_ranks = sorted([1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 17, 20])
    # LR LOO-CV: same as optimal except one outlier
    loo_borda_ranks     = sorted([1, 2, 3, 4, 5, 6, 7, 8, 10, 14, 17, 49])

    def recall_curve(ranks, K_max):
        curve = []
        for K in range(1, K_max + 1):
            hits = sum(1 for r in ranks if r <= K)
            curve.append(hits / n_bsm)
        return np.array(curve)

    Ks            = np.arange(1, K_max + 1)
    curve_uniform = recall_curve(uniform_borda_ranks, K_max)
    curve_optimal = recall_curve(optimal_borda_ranks, K_max)
    curve_loo     = recall_curve(loo_borda_ranks,     K_max)

    fig = dark_fig(11, 6)
    ax  = dark_ax(fig, 111)

    ax.plot(Ks, curve_uniform, color=CYAN,  lw=2.5,
            label='Uniform weights — Phase 13 (6/12 @K=30)')
    ax.plot(Ks, curve_optimal, color=GOLD,  lw=2.5,
            label='Optimal learned weights — Phase 14 (12/12 @K=20)')
    ax.plot(Ks, curve_loo,     color=RED,   lw=2.0, ls='--',
            label='LR LOO-CV (unbiased) — 11/12 @K=30')

    ax.axhline(y=6/12,  color=CYAN,  lw=1.0, ls=':', alpha=0.5)
    ax.axhline(y=10/12, color='#888', lw=1.0, ls=':', alpha=0.6,
               label='Target: 10/12 recall')
    ax.axhline(y=1.0,   color='#444', lw=1.0, ls='-', alpha=0.5)

    # Highlight K=20 optimal result
    ax.axvline(x=20, color=GOLD, lw=1.0, ls=':', alpha=0.5)
    ax.scatter([20], [1.0], color=GOLD, s=100, zorder=5)
    ax.annotate('12/12 @K=20\n(top 0.28%)', xy=(20, 1.0),
                xytext=(28, 0.88), fontsize=10, color=GOLD,
                arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.2))

    ax.set_xlabel('K  (top-K events examined, out of 7,181 total)', fontsize=12)
    ax.set_ylabel('Recall@K  (fraction of BSM candidates recovered)', fontsize=12)
    ax.set_title('Phase 14: BSM Candidate Recovery\n'
                 'Adaptive fusion weights place all 12 candidates within top-20',
                 fontsize=13)
    ax.legend(fontsize=10, facecolor='#111', edgecolor='#445', labelcolor='#eee')
    ax.set_xlim(0, K_max);  ax.set_ylim(-0.02, 1.08)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1.0))

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, '60_recall_at_k.png'),
                dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print("Saved: 60_recall_at_k.png")


# ═══════════════════════════════════════════════════════════════════════════
# Fig 4 — Choice-Entanglement Mass Hierarchy (from Exp 59)
# ═══════════════════════════════════════════════════════════════════════════

def fig_mass_hierarchy():
    # Real Exp 59 results
    levels     = ['geo\n(level 0)', 'bio\n(level 1)', 'noo\n(level 2)', 'theo\n(level 3)']
    m_CE_means = [0.1716, 2.4784, 43.6411, 434.9961]
    m_CE_stds  = [0.0373, 0.2614,  0.9178,   0.7565]
    colors     = ['#ff4444', '#ff9933', '#33ccff', '#ffd700']

    fig = dark_fig(10, 7)
    ax  = dark_ax(fig, 111)

    # Log-scale bar chart
    bars = ax.bar(levels, m_CE_means, color=colors, alpha=0.85,
                  edgecolor='white', linewidth=0.5, width=0.55)

    # Error bars
    ax.errorbar(levels, m_CE_means, yerr=m_CE_stds,
                fmt='none', color='white', capsize=6, lw=1.5, alpha=0.7)

    # Value labels on bars
    for bar, val, std in zip(bars, m_CE_means, m_CE_stds):
        ax.text(bar.get_x() + bar.get_width() / 2, val * 1.1,
                f'{val:.2f}', ha='center', va='bottom',
                color='white', fontsize=11, fontweight='bold')

    # Annotate the ratio
    ax.annotate('', xy=(3, m_CE_means[3]), xytext=(0, m_CE_means[0]),
                xycoords=('data', 'data'), textcoords=('data', 'data'),
                arrowprops=dict(arrowstyle='<->', color=GOLD, lw=1.8))
    ax.text(1.5, 80, '×2535\n(theo / geo)', ha='center', color=GOLD,
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2e', edgecolor=GOLD, alpha=0.8))

    ax.set_yscale('log')
    ax.set_ylabel('Mean choice-entanglement mass  $m_{CE}$  (log scale)', fontsize=12)
    ax.set_title('Exp 59: Choice-Entanglement Mass Hierarchy\n'
                 'Quadratic accumulation law — UKFT-39 Section 2.1  (N=800, T=600)',
                 fontsize=13)
    ax.set_ylim(0.05, 2000)

    # Horizontal level lines
    for val, col in zip(m_CE_means, colors):
        ax.axhline(val, color=col, lw=0.7, ls=':', alpha=0.4)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, '60_mass_hierarchy.png'),
                dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    print("Saved: 60_mass_hierarchy.png")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("Experiment 60: UKFT Teaser — generating figures …\n")

    fig_manifold()
    fig_cosine()
    fig_recall()
    fig_mass_hierarchy()

    print("\nAll figures saved to:", OUT_DIR)
    print("Exp 60 complete.")
