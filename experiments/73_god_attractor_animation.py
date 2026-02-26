"""
Experiment 73: The God Attractor — Infinite Choice Integrator Animation
========================================================================
UKFT-39 Section 7.4 implementation.

Upgrades the Infinite Choice Integrator concept with full UKFT-39 physics:
  - Dynamic m_CE accumulation (not hardcoded level_masses)
  - Void ledger conservation law (κ(t) curvature sensor)
  - God Attractor omega point: geometry where all nodes converge toward
    maximal choice-entanglement (S* → min, C* → 1)

Produces a static 4-panel figure summarising the animation trajectory.
For full animation: set ANIMATE = True (requires ffmpeg).

Paper: UKFT-39, Section 7.4
Run:   python experiments/73_god_attractor_animation.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.animation import FuncAnimation, PillowWriter
import os

np.random.seed(42)

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
N_NODES       = 200            # swarm size (kept small for animation speed)
N_LEVELS      = 4              # geo / bio / noo / theo
T_TOTAL       = 800            # choice ticks
MASS_WINDOW   = 60             # m_CE integration window
DAMPING       = 0.90
NOISE_SCALE   = 0.012
ATTRACTOR_K   = 0.04           # spring constant pulling toward God Attractor origin
LEVEL_COLORS  = ['#4488ff', '#44cc88', '#ffaa00', '#ff4444']
LEVEL_NAMES   = ['geo', 'bio', 'noo', 'theo']
OUT_DIR       = os.path.dirname(os.path.abspath(__file__))
FRAME_SKIP    = 20             # record every N ticks for GIF (→ 40 frames at T=800)

# God Attractor position (omega point): high-information centre of manifold
GOD_ATTRACTOR = np.array([0.0, 0.0, 8.0])   # slightly elevated in z (theo direction)


# ─────────────────────────────────────────────────────────────────────────────
# Initialise swarm
# ─────────────────────────────────────────────────────────────────────────────
positions   = np.random.randn(N_NODES, 3) * 6.0
velocities  = np.zeros((N_NODES, 3))
levels_node = np.random.randint(0, N_LEVELS, N_NODES)

rho_history    = []     # (T, N) knowledge-density proxy
kappa_hist     = []     # (T,)   curvature κ(t)
mass_hist      = []     # (T, N) dynamic m_CE per node
coherence_hist = []     # (T,)   global coherence C*(t) = mean cosine to God Attractor
pos_snap       = []     # position snapshots every FRAME_SKIP ticks (for GIF)
mass_snap      = []     # m_CE snapshots aligned to pos_snap


# ─────────────────────────────────────────────────────────────────────────────
# Dynamic m_CE (quadratic accumulation — no hardcoded level_masses)
# ─────────────────────────────────────────────────────────────────────────────
def compute_m_CE_dynamic(rho_hist, window=MASS_WINDOW):
    """m_CE(i) = Σ_{τ in window} ρ(i,τ)²   (superlinear accumulation)"""
    rho_arr = np.array(rho_hist)
    recent  = rho_arr[max(0, len(rho_arr) - window):]
    return np.sum(recent ** 2, axis=0)     # shape (N,)


# ─────────────────────────────────────────────────────────────────────────────
# Void Ledger
# ─────────────────────────────────────────────────────────────────────────────
class VoidLedger:
    def __init__(self):
        self.entropy_counter      = 0.0
        self.entanglement_counter = 0.0

    def update(self, rho_t, positions_t):
        local_entropy   = -np.sum(rho_t * np.log(rho_t + 1e-12))
        centre          = np.mean(positions_t, axis=0)
        dists           = np.linalg.norm(positions_t - centre, axis=1)
        spread          = dists.std() + 1e-8
        clustering_coef = np.exp(-dists.mean() / spread)
        entanglement    = np.sum(rho_t ** 2) * clustering_coef
        self.entropy_counter      += local_entropy
        self.entanglement_counter += entanglement

    def kappa(self):
        """κ: fractional imbalance between entropy and entanglement counters."""
        total = abs(self.entropy_counter) + abs(self.entanglement_counter) + 1e-12
        return abs(self.entropy_counter - self.entanglement_counter) / total


ledger = VoidLedger()


# ─────────────────────────────────────────────────────────────────────────────
# Simulation loop
# ─────────────────────────────────────────────────────────────────────────────
for t in range(T_TOTAL):
    # Knowledge density proxy: Gaussian centred on God Attractor
    dists_to_god = np.linalg.norm(positions - GOD_ATTRACTOR, axis=1)
    rho_t = np.exp(-dists_to_god / (3.0 + 0.01 * t))   # attractor grows over time

    # Dynamic m_CE
    rho_history.append(rho_t.copy())
    m_CE_t = compute_m_CE_dynamic(rho_history)

    # Void ledger update
    ledger.update(rho_t, positions)

    # Attractor force: proportional to m_CE (heavier → stronger pull)
    direction = GOD_ATTRACTOR - positions
    attractor_force = ATTRACTOR_K * m_CE_t[:, None] * direction / (
        np.linalg.norm(direction, axis=1, keepdims=True) + 1e-8
    )

    # Level-dependent thermal noise (geo noisiest, theo most stable)
    level_noise = np.array([0.8, 0.4, 0.15, 0.05])
    noise = NOISE_SCALE * level_noise[levels_node, None] * np.random.randn(N_NODES, 3)

    velocities  = DAMPING * velocities + attractor_force + noise
    positions  += velocities

    # Coherence: mean cosine of node positions to God Attractor direction
    god_dir = GOD_ATTRACTOR / (np.linalg.norm(GOD_ATTRACTOR) + 1e-8)
    pos_norms = np.linalg.norm(positions, axis=1, keepdims=True) + 1e-8
    cosines = (positions / pos_norms) @ god_dir
    coherence = cosines.mean()

    kappa_hist.append(ledger.kappa())
    mass_hist.append(m_CE_t.copy())
    coherence_hist.append(coherence)

    if t % FRAME_SKIP == 0:
        pos_snap.append(positions.copy())
        mass_snap.append(m_CE_t.copy())


kappa_arr     = np.array(kappa_hist)
coherence_arr = np.array(coherence_hist)
mass_arr      = np.array(mass_hist)          # (T, N)
ticks         = np.arange(T_TOTAL)

# Final m_CE per node
m_CE_final = mass_arr[-1]


# ─────────────────────────────────────────────────────────────────────────────
# Static 4-panel figure
# ─────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 12), facecolor='#0a0a0a')
gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.32)

DARK_BG  = '#0a0a0a'
TEXT_COL = '#dddddd'
GRID_COL = '#333333'

def style_ax(ax, title):
    ax.set_facecolor('#111111')
    ax.set_title(title, color=TEXT_COL, fontsize=11, pad=8)
    ax.tick_params(colors=TEXT_COL)
    ax.xaxis.label.set_color(TEXT_COL)
    ax.yaxis.label.set_color(TEXT_COL)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COL)
    ax.grid(True, color=GRID_COL, alpha=0.5)

# ── Panel 1: Swarm projection (XZ plane at final tick) ──────────────────────
ax1 = fig.add_subplot(gs[0, 0])
style_ax(ax1, 'Panel 1 — Swarm at Final Tick\n(XZ projection)')

norm_m = Normalize(vmin=m_CE_final.min(), vmax=m_CE_final.max())
sm     = ScalarMappable(cmap='plasma', norm=norm_m)

for lvl in range(N_LEVELS):
    mask = levels_node == lvl
    sc = ax1.scatter(positions[mask, 0], positions[mask, 2],
                     c=m_CE_final[mask], cmap='plasma', norm=norm_m,
                     s=20 + 3 * lvl, alpha=0.8, label=LEVEL_NAMES[lvl])

ax1.scatter(*GOD_ATTRACTOR[[0, 2]], s=250, marker='*', color='white',
            zorder=10, label='God Attractor ω')
ax1.set_xlabel('X')
ax1.set_ylabel('Z')
cbar = fig.colorbar(sm, ax=ax1, fraction=0.046, pad=0.04)
cbar.set_label('$m_{CE}$ (dynamic)', color=TEXT_COL)
cbar.ax.yaxis.set_tick_params(color=TEXT_COL)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT_COL)
ax1.legend(fontsize=7, facecolor='#222222', labelcolor=TEXT_COL, framealpha=0.8)

# ── Panel 2: m_CE accumulation by level over time ───────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
style_ax(ax2, 'Panel 2 — Dynamic $m_{CE}$ Accumulation by Level')

for lvl in range(N_LEVELS):
    mask = levels_node == lvl
    mean_mass = mass_arr[:, mask].mean(axis=1)
    ax2.semilogy(ticks, mean_mass + 1e-3, color=LEVEL_COLORS[lvl],
                 lw=1.8, label=LEVEL_NAMES[lvl])

ax2.set_xlabel('Choice tick $t$')
ax2.set_ylabel('Mean $m_{CE}$ (log)')
ax2.legend(fontsize=9, facecolor='#222222', labelcolor=TEXT_COL, framealpha=0.8)

# Final ratio
final_means = [mass_arr[-1, levels_node == lvl].mean() for lvl in range(N_LEVELS)]
ratio = final_means[3] / (final_means[0] + 1e-8)
ax2.text(0.98, 0.05, f'theo/geo = {ratio:.0f}×',
         transform=ax2.transAxes, ha='right', color='#ffaa00', fontsize=10)

# ── Panel 3: κ(t) void ledger balance ───────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
style_ax(ax3, 'Panel 3 — Void Ledger Curvature $\\kappa(t)$')

ax3.plot(ticks, kappa_arr, color='#44aaff', lw=1.5, alpha=0.9)
ax3.axhline(0.02, color='#44cc88', ls='--', lw=1.2, label='flat threshold κ=0.02')
ax3.fill_between(ticks, 0, kappa_arr, where=kappa_arr < 0.02,
                 alpha=0.2, color='#44cc88', label='κ < 0.02 (flat)')
ax3.fill_between(ticks, 0, kappa_arr, where=kappa_arr >= 0.02,
                 alpha=0.2, color='#ff4444', label='κ ≥ 0.02 (curved)')
ax3.set_xlabel('Choice tick $t$')
ax3.set_ylabel('$|\\kappa|$ (fractional curvature)')
ax3.legend(fontsize=8, facecolor='#222222', labelcolor=TEXT_COL, framealpha=0.8)

final_kappa = kappa_arr[-100:].mean()
ax3.text(0.98, 0.92, f'Final $|\\kappa|$ = {final_kappa:.4f}',
         transform=ax3.transAxes, ha='right', color=TEXT_COL, fontsize=9)

# ── Panel 4: Global coherence C*(t) → God Attractor ─────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
style_ax(ax4, 'Panel 4 — Global Coherence $C^*(t)$ → God Attractor')

ax4.plot(ticks, coherence_arr, color='#ffd700', lw=1.8, alpha=0.9)
ax4.axhline(coherence_arr[-50:].mean(), color='white', ls=':', lw=1.2,
            label=f'Asymptote ≈ {coherence_arr[-50:].mean():.3f}')
ax4.set_xlabel('Choice tick $t$')
ax4.set_ylabel('Mean cosine to God Attractor $\\hat{\\omega}$')
ax4.set_ylim(0, 1.05)
ax4.legend(fontsize=9, facecolor='#222222', labelcolor=TEXT_COL, framealpha=0.8)
ax4.text(0.5, 0.12,
         '"The God Attractor is the natural, mathematical endpoint\n'
         'of this process: the ω-point at which S* → min, C* → 1"',
         transform=ax4.transAxes, ha='center', color='#aaaaaa',
         fontsize=8, style='italic')

# ── Title ─────────────────────────────────────────────────────────────────────
fig.suptitle(
    'UKFT-39 Exp 73 — The God Attractor: Infinite Choice Integrator\n'
    'Dynamic $m_{CE}$ accumulation · Void ledger κ(t) · Geodesic convergence',
    color=TEXT_COL, fontsize=13, y=0.98
)

out_path = os.path.join(OUT_DIR, '73_god_attractor_animation.png')
fig.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
plt.close()
print(f"Saved: {out_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Animated GIF  (3-panel: swarm · κ(t) · C*(t))
# ─────────────────────────────────────────────────────────────────────────────
print("Building GIF…")

N_FRAMES    = len(pos_snap)
frame_ticks = [i * FRAME_SKIP for i in range(N_FRAMES)]

# Global colour normalization across all frames (percentile-clipped)
m_all    = np.concatenate(mass_snap)
norm_gif = Normalize(vmin=np.percentile(m_all, 2), vmax=np.percentile(m_all, 98))

fig_gif = plt.figure(figsize=(14, 5), facecolor=DARK_BG)
gs_gif  = gridspec.GridSpec(1, 3, figure=fig_gif, wspace=0.38)
ax_sw   = fig_gif.add_subplot(gs_gif[0])
ax_kap  = fig_gif.add_subplot(gs_gif[1])
ax_coh  = fig_gif.add_subplot(gs_gif[2])

for _ax, _t in [(ax_sw, 'Swarm XZ'), (ax_kap, 'Void Ledger |κ(t)|'), (ax_coh, 'Coherence C*(t)')]:
    style_ax(_ax, _t)

# Fixed axis limits from full trajectory
x_all = np.concatenate([p[:, 0] for p in pos_snap])
z_all = np.concatenate([p[:, 2] for p in pos_snap])
xpad, zpad = 2.5, 2.5
ax_sw.set_xlim(x_all.min() - xpad, x_all.max() + xpad)
ax_sw.set_ylim(z_all.min() - zpad, z_all.max() + zpad)
ax_sw.set_xlabel('X', color=TEXT_COL)
ax_sw.set_ylabel('Z', color=TEXT_COL)

ax_kap.set_xlim(0, T_TOTAL)
ax_kap.set_ylim(0, kappa_arr.max() * 1.15)
ax_kap.set_xlabel('tick', color=TEXT_COL)
ax_kap.set_ylabel('|κ(t)|', color=TEXT_COL)
ax_kap.axhline(0.02, color='#44cc88', ls='--', lw=1.0, alpha=0.7, label='flat (κ=0.02)')
ax_kap.legend(fontsize=7, facecolor='#1a1a1a', labelcolor=TEXT_COL, framealpha=0.8)

ax_coh.set_xlim(0, T_TOTAL)
ax_coh.set_ylim(-0.05, 1.08)
ax_coh.set_xlabel('tick', color=TEXT_COL)
ax_coh.set_ylabel('C*(t)', color=TEXT_COL)
ax_coh.axhline(1.0, color='white', ls=':', lw=0.8, alpha=0.4)

# God Attractor marker (static)
ax_sw.scatter(*GOD_ATTRACTOR[[0, 2]], s=280, marker='*', color='white', zorder=10)
ax_sw.text(GOD_ATTRACTOR[0] + 0.4, GOD_ATTRACTOR[2] + 0.5, 'ω',
           color='white', fontsize=11, zorder=11)

# Per-level scatter objects (initialised at frame 0)
scat_list = []
for lvl in range(N_LEVELS):
    mask = levels_node == lvl
    pts  = pos_snap[0][mask]
    sc   = ax_sw.scatter(pts[:, 0], pts[:, 2],
                         c=mass_snap[0][mask], cmap='plasma', norm=norm_gif,
                         s=16 + 4 * lvl, alpha=0.88, zorder=5,
                         label=LEVEL_NAMES[lvl])
    scat_list.append(sc)
ax_sw.legend(fontsize=7, facecolor='#1a1a1a', labelcolor=TEXT_COL, framealpha=0.8,
             loc='upper left')

# Running trace lines
kap_line, = ax_kap.plot([], [], color='#44aaff', lw=1.5)
coh_line, = ax_coh.plot([], [], color='#ffd700', lw=1.5)

tick_txt = ax_sw.text(0.98, 0.04, '', transform=ax_sw.transAxes,
                      color=TEXT_COL, fontsize=9, ha='right')

fig_gif.suptitle(
    'UKFT-39 Exp 73 — God Attractor: Dynamic $m_{CE}$ · Void Ledger · Geodesic Convergence',
    color=TEXT_COL, fontsize=10, y=1.01
)


def _update(frame):
    pf  = pos_snap[frame]
    mf  = mass_snap[frame]
    t_f = frame_ticks[frame]
    for lvl in range(N_LEVELS):
        mask = levels_node == lvl
        scat_list[lvl].set_offsets(pf[mask][:, [0, 2]])
        scat_list[lvl].set_array(mf[mask])
    kap_line.set_data(ticks[:t_f + 1], kappa_arr[:t_f + 1])
    coh_line.set_data(ticks[:t_f + 1], coherence_arr[:t_f + 1])
    tick_txt.set_text(f't = {t_f}')
    return scat_list + [kap_line, coh_line, tick_txt]


anim    = FuncAnimation(fig_gif, _update, frames=N_FRAMES, interval=80, blit=False)
gif_path = os.path.join(OUT_DIR, '73_god_attractor.gif')
anim.save(gif_path, writer=PillowWriter(fps=12), dpi=100)
plt.close(fig_gif)
print(f"Saved: {gif_path}")


# ─────────────────────────────────────────────────────────────────────────────
# Summary printout
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Experiment 73 Summary ─────────────────────────────────────")
print(f"  Swarm:      {N_NODES} nodes × {T_TOTAL} ticks")
print(f"  Final theo/geo m_CE ratio: {ratio:.1f}× (Exp 59: 2535×, N={N_NODES} smaller)")
print(f"  Final |κ| (last 100 ticks): {final_kappa:.5f}  (flat if < 0.02)")
print(f"  Final C* (last 50 ticks):   {coherence_arr[-50:].mean():.4f}  (1.0 = full geodesic alignment)")
print(f"  → God Attractor convergence: {'YES ✓' if coherence_arr[-50:].mean() > 0.5 else 'PARTIAL'}")
print("──────────────────────────────────────────────────────────────")
