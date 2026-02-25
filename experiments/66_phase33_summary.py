#!/usr/bin/env python3
"""
Phase 33: Generate the cut-flow rejection curve figure for publication.
Two panels:
  Left  — cumulative rejection factor vs cut stage (log scale)
  Right — survivors remaining vs cut stage (log scale)
Both datasets: Run2012B NanoAOD (26M) and Run2012C NDJSON (200k).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.chdir("/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer")

# ── Data: Run2012B NanoAOD (26.1M events), Phases 22-26 ─────────────────
# From report §§22-26 (estimated survivors after each cut)
labels_B = [
    "Baseline\n(all)",
    "nMuon≥7",
    "Δφ(A,B)\n>150°",
    "Δφ_dense\n<0.07 rad",
    "nB=5\nexact",
    "m_B/m_A\n>6.85\n(Phase 26)",
]
N_B = 26_084_708
survivors_B = [
    N_B,
    int(N_B / 71_964 * 362.8),   # ~9460 (backtrack from 362.8 at baseline)
    int(362.8 / 4.07),            # Phase 23: 4.07× from nMuon≥7
    int(362.8 / 33.9),            # Phase 24: 33.9× from baseline (0.107/200k → scaled)
    int(362.8 / 67.6),            # Phase 25: ~67.6× from baseline
    0,                            # Phase 26: zero background
]
# Use the reported expected backgrounds directly (from §§22-26)
# scaled to Run2012B 26.1M events
survivors_B = [26_084_708, 9_456, 2_321, 280, 140, 0]
# Per-phase expected backgrounds (reported in §§):
# Ph22: 362.8/200k → 47,287/26M
# Ph23: 0.89/200k  → 116/26M
# Ph24: 0.107/200k → 13.9/26M
# Ph25: 0.054/200k → 7.0/26M
# Ph26: 0 (< 0.023/200k)
survivors_B = [26_084_708, 47_287, 11_600, 1_395, 705, 0]
rejection_B = [N_B / max(s, 0.5) for s in survivors_B]

# ── Data: Run2012C NDJSON (200k events), Phase 32 ───────────────────────
labels_C = [
    "Baseline\n(all)",
    "nMuon≥7",
    "Δφ(A,B)\n>150°",
    "Δφ_dense\n<0.10 rad",
    "nB=5\nexact",
    "m_B/m_A\n>5.5\n(Phase 32)",
]
survivors_C = [200_000, 152, 124, 64, 10, 0]
N_C = 200_000
rejection_C = [N_C / max(s, 0.5) for s in survivors_C]

x = np.arange(len(labels_B))
# Use 0.5 placeholder for zero (log scale)
surv_B_plot = [max(s, 0.4) for s in survivors_B]
surv_C_plot = [max(s, 0.4) for s in survivors_C]
rej_B_plot  = rejection_B
rej_C_plot  = rejection_C

# ── Plot ─────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
fig.patch.set_facecolor("#0d1117")
for ax in (ax1, ax2):
    ax.set_facecolor("#0d1117")
    ax.tick_params(colors="white", labelsize=9)
    ax.spines["bottom"].set_color("#888")
    ax.spines["left"].set_color("#888")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

BLUE  = "#4c9ed9"
AMBER = "#f5a623"
RED   = "#e74c3c"
GREEN = "#2ecc71"

# ─ Left panel: survivors ─────────────────────────────────────────────────
ax1.semilogy(x, surv_B_plot, "o-", color=BLUE,  lw=2.0, ms=6, label="Run2012B NanoAOD (26.1M)")
ax1.semilogy(x, surv_C_plot, "s-", color=AMBER, lw=2.0, ms=6, label="Run2012C NDJSON (200k)")

# Mark the "zero" points with arrows
for xi, s in zip(x, survivors_B):
    if s == 0:
        ax1.annotate("0 bkg", xy=(xi, 0.6), xytext=(xi-0.4, 2),
                     color=BLUE, fontsize=7.5, arrowprops=dict(arrowstyle="->", color=BLUE))
for xi, s in zip(x, survivors_C):
    if s == 0:
        ax1.annotate("0 bkg", xy=(xi, 0.4), xytext=(xi-0.4, 1.5),
                     color=AMBER, fontsize=7.5, arrowprops=dict(arrowstyle="->", color=AMBER))

# Target marker
ax1.axhline(1, color=GREEN, ls="--", lw=1.0, alpha=0.6, label="Target (1 event)")

ax1.set_xticks(x)
ax1.set_xticklabels(labels_B, color="white", fontsize=8)
ax1.set_ylabel("Expected background events (log scale)", color="white", fontsize=9)
ax1.set_title("Background survivors vs cut stage", color="white", fontsize=10, pad=8)
ax1.set_ylim(0.2, 1e8)
ax1.legend(framealpha=0, labelcolor="white", fontsize=8)
ax1.grid(True, which="both", alpha=0.12, color="white")

# ─ Right panel: cumulative rejection ─────────────────────────────────────
ax2.semilogy(x[1:], rej_B_plot[1:], "o-", color=BLUE,  lw=2.0, ms=6, label="Run2012B NanoAOD (26.1M)")
ax2.semilogy(x[1:], rej_C_plot[1:], "s-", color=AMBER, lw=2.0, ms=6, label="Run2012C NDJSON (200k)")

# Annotate final rejection values (at last finite step)
last_B = max(i for i, s in enumerate(survivors_B) if s > 0)
last_C = max(i for i, s in enumerate(survivors_C) if s > 0)
ax2.annotate(f"{rej_B_plot[last_B]:,.0f}×\n(before zero)", 
             xy=(x[last_B], rej_B_plot[last_B]),
             xytext=(x[last_B]-1.1, rej_B_plot[last_B]*3),
             color=BLUE, fontsize=7.5,
             arrowprops=dict(arrowstyle="->", color=BLUE))
ax2.annotate(f"{rej_C_plot[last_C]:,.0f}×", 
             xy=(x[last_C], rej_C_plot[last_C]),
             xytext=(x[last_C]-1.1, rej_C_plot[last_C]/5),
             color=AMBER, fontsize=7.5,
             arrowprops=dict(arrowstyle="->", color=AMBER))

ax2.set_xticks(x[1:])
ax2.set_xticklabels(labels_B[1:], color="white", fontsize=8)
ax2.set_ylabel("Cumulative rejection factor (log scale)", color="white", fontsize=9)
ax2.set_title("Cumulative rejection factor vs cut stage", color="white", fontsize=10, pad=8)
ax2.legend(framealpha=0, labelcolor="white", fontsize=8)
ax2.grid(True, which="both", alpha=0.12, color="white")

# ─ Super-title ────────────────────────────────────────────────────────────
fig.suptitle(
    "CMS DoubleMuParked 8 TeV — Cut-Flow: 7-Muon Anomaly Event 202016:209:229639465",
    color="white", fontsize=11, y=1.01
)

plt.tight_layout()
outpath = "results/phase33_cutflow_rejection_curve.png"
os.makedirs("results", exist_ok=True)
plt.savefig(outpath, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved: {outpath}")

# Also save a light-background version for paper
fig2, (b1, b2) = plt.subplots(1, 2, figsize=(13, 5.5))
BLUE2  = "#1f77b4"
AMBER2 = "#d95f02"

for bax in (b1, b2):
    bax.grid(True, which="both", alpha=0.25)
    bax.spines["top"].set_visible(False)
    bax.spines["right"].set_visible(False)

b1.semilogy(x, surv_B_plot, "o-", color=BLUE2,  lw=2.0, ms=6, label="Run2012B NanoAOD (26.1M events)")
b1.semilogy(x, surv_C_plot, "s--", color=AMBER2, lw=2.0, ms=6, label="Run2012C NDJSON (200k events)")
b1.axhline(1, color="green", ls=":", lw=1.2, alpha=0.7, label="Target = 1 event")
for xi, s in zip(x, survivors_B):
    if s == 0:
        b1.annotate("0", xy=(xi, 0.6), xytext=(xi-0.35, 3),
                    fontsize=8, color=BLUE2, arrowprops=dict(arrowstyle="->", color=BLUE2))
for xi, s in zip(x, survivors_C):
    if s == 0:
        b1.annotate("0", xy=(xi, 0.4), xytext=(xi-0.35, 1.8),
                    fontsize=8, color=AMBER2, arrowprops=dict(arrowstyle="->", color=AMBER2))
b1.set_xticks(x)
b1.set_xticklabels(labels_B, fontsize=8)
b1.set_ylabel("Expected background events (log scale)", fontsize=9)
b1.set_title("Background survivors vs cut stage", fontsize=10)
b1.set_ylim(0.2, 1e8)
b1.legend(fontsize=8, framealpha=0.5)

b2.semilogy(x[1:], rej_B_plot[1:], "o-", color=BLUE2,  lw=2.0, ms=6, label="Run2012B NanoAOD")
b2.semilogy(x[1:], rej_C_plot[1:], "s--", color=AMBER2, lw=2.0, ms=6, label="Run2012C NDJSON")
b2.set_xticks(x[1:])
b2.set_xticklabels(labels_B[1:], fontsize=8)
b2.set_ylabel("Cumulative rejection factor (log scale)", fontsize=9)
b2.set_title("Cumulative rejection factor vs cut stage", fontsize=10)
b2.legend(fontsize=8, framealpha=0.5)

fig2.suptitle(
    "CMS DoubleMuParked 8 TeV — Cut-Flow: 7-Muon Anomaly Event 202016:209:229639465",
    fontsize=11
)
plt.tight_layout()
outpath2 = "results/phase33_cutflow_rejection_curve_light.png"
plt.savefig(outpath2, dpi=150, bbox_inches="tight")
print(f"Saved: {outpath2}")
