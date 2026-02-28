"""Generate figures for experiments 61 and 70."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Figure 61: SM 7-muon cross-section scaling ────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor="#0d1117")
ax.set_facecolor("#0d1117")

labels  = ["pp→4μ\n(MG5 LO anchor)", "pp→5μ\n(×α²_EW)", "pp→6μ\n(×α⁴_EW)", "pp→7μ\n(×α⁶_EW)"]
sigmas  = [1.23e-2, 3.7e-5, 1.1e-7, 3.3e-10]   # fb, representative values from exp 61
colors  = ["#4c8fd6", "#2ea44f", "#f0883e", "#e63946"]

bars = ax.bar(labels, sigmas, color=colors, width=0.5, log=True, zorder=3)
ax.set_ylabel("σ  [fb]", color="white", fontsize=13)
ax.set_title("SM Multi-Muon Cross-Section Scaling (8 TeV)\nPhase 28 Background Anchoring", color="white", fontsize=13, pad=12)
ax.tick_params(colors="white", labelsize=11)
ax.spines["bottom"].set_color("#444")
ax.spines["left"].set_color("#444")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.label.set_color("white")
ax.set_ylim(1e-12, 1e1)

# N_bkg annotation at 7μ bar
ax.annotate("N_bkg @ 20 fb⁻¹\n≈ 1.8 × 10⁻¹⁵→ P(obs≥1) < 10⁻¹⁴",
            xy=(3, sigmas[3]), xytext=(2.2, 1e-8),
            arrowprops=dict(arrowstyle="->", color="white", lw=1.2),
            color="white", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="#1c2533", ec="#444"))

# include cut-efficiency note
ax.text(0, 8e-12, "Cut-efficiency ε(Phase-26) applied to each process.",
        color="#888", fontsize=8)

for spine in ax.spines.values():
    spine.set_color("#333")
ax.grid(axis="y", color="#222", linestyle="--", zorder=0)
fig.tight_layout(pad=1.5)
fig.savefig("61_sm_7muon_cross_section_scaling.png", dpi=150, bbox_inches="tight",
             facecolor=fig.get_facecolor())
plt.close()
print("Saved 61_sm_7muon_cross_section_scaling.png")

# ── Figure 70: displaced-vertex significance ──────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(10, 5), facecolor="#0d1117")

mu_labels  = ["Muon A\n(iso=12.9)", "Muon B\n(iso=8.9)"]
dxy_val    = [0.046e-3, 0.467e-3]   # m, dummy placeholder → convert to mm
dxy_sig    = [4.1, 29.2]
iso_vals   = [12.9, 8.9]

# Left: dxy significance
ax = axes[0]; ax.set_facecolor("#0d1117")
c = ["#f0883e", "#e63946"]
bars2 = ax.barh(mu_labels, dxy_sig, color=c, height=0.4, zorder=3)
ax.axvline(x=5.0, color="#2ea44f", lw=1.5, ls="--", label="5σ threshold")
ax.set_xlabel("|dxy / σ_dxy|", color="white", fontsize=12)
ax.set_title("Displaced-Vertex Significance\n(Phase 71 confirmation)", color="white", fontsize=11)
ax.tick_params(colors="white"); ax.legend(fontsize=9, labelcolor="white",
    facecolor="#1c2533", edgecolor="#444")
for spine in ax.spines.values(): spine.set_color("#333")
ax.grid(axis="x", color="#222", ls="--", zorder=0)
# annotate 29.2σ
ax.text(dxy_sig[1]+0.4, 1, "29.2σ", color="#e63946", fontsize=12, va="center", fontweight="bold")
ax.text(dxy_sig[0]+0.4, 0, "4.1σ", color="#f0883e", fontsize=11, va="center")

# Right: PF validity at cut stages
ax2 = axes[1]; ax2.set_facecolor("#0d1117")
stages   = ["C3\n(pre-mass)", "C4\n(m_A cut)", "C5\n(m_B cut)", "target\nevent"]
pf_valid = [0.0, 0.0, 0.0, 100.0]   # % of background with ≥1 non-PF muon
bkg_surv = [100.0, 100.0, 100.0, 0.0]

x = np.arange(len(stages))
ax2.bar(x - 0.2, pf_valid,  width=0.35, color="#4c8fd6", label="Target: % PF-valid", zorder=3)
ax2.bar(x + 0.2, bkg_surv,  width=0.35, color="#888", label="Bkg: % surviving", zorder=3)
ax2.set_xticks(x); ax2.set_xticklabels(stages, color="white", fontsize=10)
ax2.set_ylabel("% of events", color="white", fontsize=12)
ax2.set_title("PF Validity: Background vs Target\n(100% background has ≥1 non-PF)", color="white", fontsize=11)
ax2.legend(fontsize=9, labelcolor="white", facecolor="#1c2533", edgecolor="#444")
ax2.tick_params(colors="white")
for spine in ax2.spines.values(): spine.set_color("#333")
ax2.grid(axis="y", color="#222", ls="--", zorder=0)

fig.tight_layout(pad=1.5)
fig.savefig("70_displaced_vertex_significance.png", dpi=150, bbox_inches="tight",
             facecolor=fig.get_facecolor())
plt.close()
print("Saved 70_displaced_vertex_significance.png")
print("Done.")
