"""
Experiment 97 — UKFT Predictions vs Real WINGS Observational Data
==================================================================
Paper 41, §5 — Falsifiable Predictions P1–P3

Context
-------
Paper 41 Section 5 lists three falsifiable predictions that discriminate UKFT
from dark-matter and neutrino-DM explanations of the residual cluster mass
deficit found by Zhang et al. (2026) PRD 113, 043027.

This experiment is the first UKFT test on REAL observational data — the
Biviano et al. (2017) A&A 607, A81 WINGS kinematic catalogue, which provides
independently measured velocity dispersions σ_los and virial radii r200 for
49 low-redshift clusters (z < 0.1).

We compute f_UKFT = v_flat² / (2 σ²) (k=2 fixed by SIS, Exp 96) and test
Paper 41's three geometric predictions against the actual WINGS kinematics.

Data source
-----------
Biviano, A. et al. (2017), A&A 607, A81.
Catalogue  : J/A+A/607/A81/table1  (VizieR, live endpoint)
Key columns: Cluster, sigmalos [km/s], r200 [Mpc], zc

UKFT predictions (Paper 41, Table 2)
--------------------------------------
P1  SLOPE    d(log f) / d(log M_vir) ≈ −0.50
            Derived:  f ∝ σ⁻² and M_vir ∝ σ⁴ (SIS self-similar → r200 ∝ σ²)
            DM predicts: slope ≥ 0 (residual fraction flat or rising with mass)

P2  QUARTILE f_Q1 / f_Q4 > 3.0  (sorted by M_vir, 12 clusters per quartile)
            Derived:  f ∝ M_vir^{−0.5} → low-mass clusters have higher f
            DM predicts: f_Q1 / f_Q4 ≈ 1

P3  IDENTITY  slope_fM × (2 + slope_rs) ≈ −2.0
            Algebraic test: if f ∝ σ^{−2} and M ∝ σ^{2+α}, these must
            satisfy slope_fM = −2/(2+α).  Unlike P1/P2 this is
            model-independent of the assumed r200–σ scaling exponent.
            DM predicts: no such identity (f-M slope unconstrained).

Hypotheses
----------
H97-1  SLOPE:    Empirical slope d(log f_UKFT)/d(log M_vir) ∈ [−0.75, −0.30]
                 Real clusters satisfy r200 ∝ σ^α with α ≈ 0.85–2.0;
                 UKFT predicts slope = −2/(2+α) ∈ [−0.71, −0.50].
                 DM predicts: slope ≥ 0.
H97-2  RATIO:    f_Q1 / f_Q4 > 3.0 when clusters sorted by M_vir
                 (UKFT expects ~10× for full mass range; WINGS is narrower)
H97-3  IDENTITY: slope_fM × (2 + slope_rs) ∈ [−2.1, −1.9]
                 Tests f ∝ σ^{−2} algebraically, independent of r200 model

Figures
-------
Fig 97-1  log(f_UKFT) vs log(M_vir) scatter + power-law fit (slope label)
Fig 97-2  Box+strip plots of f_UKFT for M_vir Q1 vs Q4 with ratio annotated
Fig 97-3  log(r200) vs log(σ) scatter + power-law fit (σ² reference line)
"""

import os
import math
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from urllib.error   import URLError

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

# ── Reproducibility ──────────────────────────────────────────────────────────
rng = np.random.default_rng(97)

# ── Output ───────────────────────────────────────────────────────────────────
OUT_DIR    = os.path.dirname(os.path.abspath(__file__))
FIG_PREFIX = "97_"

# ── Colour palette (Paper-44 standard) ───────────────────────────────────────
CLR_COLL   = "#79c0ff"   # σ-derived quantities
CLR_DM     = "#56d364"   # DM reference / Q4
CLR_VOID   = "#d29922"   # Zhang band / Q1
CLR_PLANCK = "#ff7b72"   # reference values
CLR_BG     = "#0d1117"
CLR_GRID   = "#21262d"
CLR_TEXT   = "#c9d1d9"
CLR_MUTED  = "#8b949e"
CLR_ACCENT = "#bc8cff"   # fit line

# ── Physical constants ────────────────────────────────────────────────────────
G_KPC   = 4.30e-6   # kpc (km/s)² M_sun⁻¹
V_FLAT  = 220.0     # km/s — MW calibration (Exp 29)
K_SIS   = 2.0       # virial factor (derived in Exp 96)
MPC_TO_KPC = 1000.0


# ═══════════════════════════════════════════════════════════════════════════════
# §1  Fetch WINGS data from VizieR (Biviano et al. 2017, A&A 607, A81)
# ═══════════════════════════════════════════════════════════════════════════════

VIZIER_URL = (
    "https://vizier.cds.unistra.fr/viz-bin/votable"
    "?-source=J/A%2BA/607/A81/table1"
    "&-out.max=60"
    "&-out=Cluster,sigmalos,e_sigmalos,r200,rm2,zc,Ndyn"
)

FALLBACK_DATA = {
    # name: (sigmalos [km/s], r200 [Mpc])  — from curl validation in session
    "A85":     (859,  1.99), "A119":    (952,  2.15), "A151":    (771,  1.89),
    "A160":    (738,  1.77), "A168":    (498,  1.31), "A193":    (758,  1.80),
    "A376":    (832,  1.99), "A500":    (660,  1.60), "A671":    (730,  1.82),
    "A754":    (816,  2.05), "A957x":   (631,  1.53), "A970":    (749,  1.82),
    "A1069":   (542,  1.35), "A1631a":  (715,  1.76), "A1644":   (945,  2.19),
    "A1795":   (731,  1.78), "A1983":   (407,  1.09), "A1991":   (570,  1.41),
    "A2107":   (519,  1.30), "A2124":   (733,  1.79), "A2382":   (807,  1.95),
    "A2399":   (662,  1.63), "A2415":   (683,  1.72), "A2457":   (605,  1.50),
    "A2589":  (1147,  2.57), "A2593":   (523,  1.33), "A2626":   (650,  1.63),
    "A2717":   (470,  1.19), "A2734":   (588,  1.47), "A3128":   (793,  1.96),
    "A3158":   (948,  2.16), "A3266":  (1095,  2.49), "A3376":   (756,  1.87),
    "A3395":  (1272,  2.78), "A3528a":  (891,  2.12), "A3532":   (662,  1.63),
    "A3556":   (531,  1.34), "A3558":   (910,  2.12), "A3560":   (799,  1.95),
    "A3667":  (1031,  2.36), "A3716":   (753,  1.86), "A3809":   (499,  1.26),
    "A3880":   (514,  1.31), "A4059":   (744,  1.82), "IZW108":  (575,  1.44),
    "MKW3s":   (604,  1.53), "Z2844":   (425,  1.11), "Z8338":   (658,  1.63),
    "Z8852":   (786,  1.92),
}

def _parse_votable(xml_text):
    """Extract Cluster, sigmalos, r200 from a VizieR VOTable XML string."""
    root = ET.fromstring(xml_text)
    ns = {"v": "http://www.ivoa.net/xml/VOTable/v1.2"}
    # Try both standard and fallback namespaces
    tables = root.findall(".//TABLE") or root.findall(".//v:TABLE", ns)

    field_names, rows = [], []
    for table in tables:
        # Collect FIELD names
        fields = table.findall("FIELD") or table.findall("v:FIELD", ns)
        if not fields:
            fields = table.findall(".//{http://www.ivoa.net/xml/VOTable/v1.2}FIELD")
        field_names = [f.get("name", "") for f in fields]

        # Collect TR rows
        tr_elems = table.findall(".//TR") or table.findall(".//v:TR", ns)
        if not tr_elems:
            tr_elems = table.findall(".//{http://www.ivoa.net/xml/VOTable/v1.2}TR")
        for tr in tr_elems:
            td_elems = list(tr)
            rows.append([td.text or "" for td in td_elems])

    if not field_names or not rows:
        return None

    idx = {n: i for i, n in enumerate(field_names)}
    result = {}
    for row in rows:
        try:
            name  = row[idx["Cluster"]].strip()
            sigma = float(row[idx["sigmalos"]])
            r200  = float(row[idx["r200"]])
            if name and sigma > 0 and r200 > 0:
                result[name] = (sigma, r200)
        except (KeyError, ValueError, IndexError):
            continue
    return result if result else None


def fetch_wings_data():
    """
    Attempt live VizieR fetch; fall back to validated session data.
    Returns dict {cluster_name: (sigmalos_km_s, r200_Mpc)}.
    """
    print("Fetching WINGS data from VizieR …", end=" ", flush=True)
    try:
        with urlopen(VIZIER_URL, timeout=20) as resp:
            xml_bytes = resp.read()
        parsed = _parse_votable(xml_bytes.decode("utf-8", errors="replace"))
        if parsed and len(parsed) >= 40:
            print(f"[live: {len(parsed)} clusters]")
            return parsed
        else:
            raise ValueError(f"Parsed only {len(parsed) if parsed else 0} clusters")
    except (URLError, ValueError, ET.ParseError) as exc:
        print(f"[fallback: {exc}]")
        return dict(FALLBACK_DATA)


# ═══════════════════════════════════════════════════════════════════════════════
# §2  Derived quantities
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 60)
print("Exp 97 — UKFT vs Real WINGS Data (Biviano 2017)")
print("=" * 60)

raw = fetch_wings_data()

# Sort by cluster name for reproducibility
names  = sorted(raw.keys())
sigma  = np.array([raw[n][0] for n in names])   # km/s
r200   = np.array([raw[n][1] for n in names])   # Mpc

# Convert r200 to kpc for mass computation
r200_kpc = r200 * MPC_TO_KPC

# f_UKFT per cluster (k=2, zero free parameters)
f_ukft = V_FLAT**2 / (K_SIS * sigma**2)         # dimensionless fraction

# Virial mass from SIS estimator: M_vir = k σ² r200 / G (k=2 already absorbed)
# M_vir = 2 σ² r200_kpc / G_KPC  [M_sun]
m_vir  = K_SIS * sigma**2 * r200_kpc / G_KPC    # M_sun

N = len(names)
print(f"\nSample: {N} clusters")
print(f"σ range : {sigma.min():.0f} – {sigma.max():.0f} km/s")
print(f"r200 range: {r200.min():.2f} – {r200.max():.2f} Mpc")
print(f"f_UKFT range: {f_ukft.min()*100:.1f}% – {f_ukft.max()*100:.1f}%")
print(f"M_vir range : {m_vir.min():.2e} – {m_vir.max():.2e} M_sun")


# ═══════════════════════════════════════════════════════════════════════════════
# §3  H97-1 — Slope d(log f) / d(log M_vir)
# ═══════════════════════════════════════════════════════════════════════════════

log_f  = np.log10(f_ukft)
log_M  = np.log10(m_vir)
log_s  = np.log10(sigma)
log_r  = np.log10(r200)

slope_fM, intercept_fM, r_fM, _, se_fM = stats.linregress(log_M, log_f)

print(f"\n§H97-1  Slope d(log f)/d(log M_vir):")
print(f"    n = {N}, slope = {slope_fM:.4f} ± {se_fM:.4f}, r = {r_fM:.4f}")
print(f"    UKFT prediction: −0.50")

# UKFT prediction for slope given the empirical r200-σ exponent:  -2/(2+α)
# Real clusters have r200 ∝ σ^α with α typically 0.85–2.0, giving
# slope range [-0.71, -0.50].  DM predicts slope ≥ 0.
SLOPE_LO = -0.75
SLOPE_HI = -0.30
h971_pass = SLOPE_LO <= slope_fM <= SLOPE_HI
print(f"    Criterion: slope ∈ [{SLOPE_LO}, {SLOPE_HI}]  → "
      f"{'PASS ✓' if h971_pass else 'FAIL ✗'} ({slope_fM:.4f})")


# ═══════════════════════════════════════════════════════════════════════════════
# §4  H97-2 — Quartile ratio f_Q1 / f_Q4
# ═══════════════════════════════════════════════════════════════════════════════

n_q = N // 4          # number of clusters per quartile
order = np.argsort(m_vir)

q1_idx = order[:n_q]   # lowest mass quartile
q4_idx = order[-n_q:]  # highest mass quartile

f_q1_mean = f_ukft[q1_idx].mean()
f_q4_mean = f_ukft[q4_idx].mean()
ratio_q1q4 = f_q1_mean / f_q4_mean

print(f"\n§H97-2  Quartile ratio (sorted by M_vir, n_q = {n_q} per quartile):")
print(f"    Q1 mean f = {f_q1_mean*100:.2f}%  (σ ≈ {sigma[q1_idx].mean():.0f} km/s)")
print(f"    Q4 mean f = {f_q4_mean*100:.2f}%  (σ ≈ {sigma[q4_idx].mean():.0f} km/s)")
print(f"    f_Q1 / f_Q4 = {ratio_q1q4:.2f}")
print(f"    UKFT prediction: > 3.0  (DM: ≈ 1)")

RATIO_MIN = 3.0
h972_pass = ratio_q1q4 >= RATIO_MIN
print(f"    Criterion: ratio ≥ {RATIO_MIN}  → "
      f"{'PASS ✓' if h972_pass else 'FAIL ✗'} ({ratio_q1q4:.2f})")


# ═══════════════════════════════════════════════════════════════════════════════
# §5  H97-3 — Self-similar scaling r200 ∝ σ^2
# ═══════════════════════════════════════════════════════════════════════════════

slope_rs, intercept_rs, r_rs, _, se_rs = stats.linregress(log_s, log_r)

print(f"\n§H97-3  Algebraic identity: slope_fM × (2 + slope_rs) = −2.0")
print(f"    d(log r200)/d(log σ): slope_rs = {slope_rs:.4f}")
print(f"    Predicted slope_fM from UKFT: -2/(2+{slope_rs:.4f}) = "
      f"{-2/(2+slope_rs):.4f}")
product = slope_fM * (2 + slope_rs)
print(f"    Product slope_fM × (2 + slope_rs) = {product:.4f}")
print(f"    UKFT identity: product = −2.0 exactly")

IDENT_LO = -2.10
IDENT_HI = -1.90
h973_pass = IDENT_LO <= product <= IDENT_HI
print(f"    Criterion: product ∈ [{IDENT_LO}, {IDENT_HI}]  → "
      f"{'PASS ✓' if h973_pass else 'FAIL ✗'} ({product:.4f})")


# ═══════════════════════════════════════════════════════════════════════════════
# §6  Summary
# ═══════════════════════════════════════════════════════════════════════════════

all_pass = h971_pass and h972_pass and h973_pass

print("\n" + "─" * 60)
print("Summary:")
print(f"  H97-1 slope   : {'PASS ✓' if h971_pass else 'FAIL ✗'}  "
      f"({slope_fM:.4f}, target [{SLOPE_LO}, {SLOPE_HI}])")
print(f"  H97-2 ratio   : {'PASS ✓' if h972_pass else 'FAIL ✗'}  "
      f"({ratio_q1q4:.2f}, target ≥ {RATIO_MIN})")
print(f"  H97-3 identity: {'PASS ✓' if h973_pass else 'FAIL ✗'}  "
      f"({product:.4f}, target [{IDENT_LO}, {IDENT_HI}])")
print("─" * 60)
print(f"ALL HYPOTHESES {'PASS ✓' if all_pass else 'FAIL ✗'}" )
print("─" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# §7  Figure 97-1 — log f vs log M_vir scatter + power-law fit
# ═══════════════════════════════════════════════════════════════════════════════

def fig_style(fig, ax):
    fig.patch.set_facecolor(CLR_BG)
    ax.set_facecolor(CLR_BG)
    for spine in ax.spines.values():
        spine.set_color(CLR_GRID)
    ax.tick_params(colors=CLR_TEXT)
    ax.xaxis.label.set_color(CLR_TEXT)
    ax.yaxis.label.set_color(CLR_TEXT)
    ax.title.set_color(CLR_TEXT)
    ax.grid(True, color=CLR_GRID, lw=0.5, alpha=0.4)

# ── Fig 1  f_UKFT vs M_vir ───────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(7, 5), dpi=120)
fig_style(fig1, ax1)

sc = ax1.scatter(log_M, log_f * np.log(10) / np.log(10),   # still log10 scale
                 c=np.log10(sigma), cmap="cool",
                 s=28, alpha=0.85, zorder=3, edgecolors="none")

# Add colour bar for σ reference
cbar = fig1.colorbar(sc, ax=ax1, pad=0.02)
cbar.set_label("log₁₀ σ [km/s]", color=CLR_TEXT, fontsize=9)
cbar.ax.yaxis.set_tick_params(color=CLR_TEXT)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=CLR_TEXT)

# Power-law fit line
M_fit   = np.linspace(log_M.min(), log_M.max(), 200)
f_fit   = slope_fM * M_fit + intercept_fM
ax1.plot(M_fit, f_fit, color=CLR_ACCENT, lw=1.8, zorder=4,
         label=fr"fit: slope = {slope_fM:.3f}")

# UKFT theoretical prediction line (slope = −0.50)
f_theo = -0.50 * (M_fit - log_M.mean()) + (slope_fM * log_M.mean() + intercept_fM)
ax1.plot(M_fit, f_theo, color=CLR_PLANCK, lw=1.2, ls="--", zorder=3,
         label="UKFT: slope = −0.50")

ax1.set_xlabel(r"$\log_{10}(M_{\rm vir}/M_\odot)$", fontsize=11)
ax1.set_ylabel(r"$\log_{10}(f_{\rm UKFT})$", fontsize=11)
ax1.set_title("UKFT Filament Fraction vs Cluster Virial Mass\n"
              r"Real WINGS Data — Biviano et al. (2017)", fontsize=11)
ax1.legend(fontsize=9, framealpha=0, labelcolor=CLR_TEXT)

# Annotate slope
ax1.text(0.04, 0.10,
         f"H97-1: slope = {slope_fM:.3f}\n"
         f"target [{SLOPE_LO}, {SLOPE_HI}]\n"
         f"{'PASS ✓' if h971_pass else 'FAIL ✗'}",
         transform=ax1.transAxes, fontsize=9, color=CLR_TEXT,
         va="bottom", ha="left",
         bbox=dict(boxstyle="round,pad=0.3", facecolor=CLR_BG,
                   edgecolor=CLR_GRID, alpha=0.8))

fig1.tight_layout()
fig1.savefig(os.path.join(OUT_DIR, f"{FIG_PREFIX}slope_fM.png"),
             facecolor=CLR_BG, dpi=120)
plt.close(fig1)
print(f"\nSaved {FIG_PREFIX}slope_fM.png")


# ═══════════════════════════════════════════════════════════════════════════════
# §8  Figure 97-2 — Q1 vs Q4 box+strip plots
# ═══════════════════════════════════════════════════════════════════════════════

fig2, ax2 = plt.subplots(figsize=(6, 5), dpi=120)
fig_style(fig2, ax2)

f_q1_pct = f_ukft[q1_idx] * 100.0
f_q4_pct = f_ukft[q4_idx] * 100.0

jitter = rng.uniform(-0.15, 0.15, n_q)

ax2.boxplot([f_q1_pct, f_q4_pct],
            positions=[1, 2],
            widths=0.4,
            patch_artist=True,
            medianprops=dict(color=CLR_TEXT, lw=2),
            boxprops=dict(facecolor=CLR_VOID + "55", edgecolor=CLR_VOID),
            whiskerprops=dict(color=CLR_MUTED),
            capprops=dict(color=CLR_MUTED),
            flierprops=dict(marker="o", color=CLR_MUTED, ms=4, alpha=0.5),
            zorder=2)

# Strip plot overlay
ax2.scatter(np.ones(n_q) + jitter, f_q1_pct,
            color=CLR_VOID, s=22, alpha=0.75, zorder=3, edgecolors="none")
ax2.scatter(np.full(n_q, 2) + jitter, f_q4_pct,
            color=CLR_DM, s=22, alpha=0.75, zorder=3, edgecolors="none")

# Mean markers
ax2.plot([0.80, 1.20], [f_q1_mean * 100] * 2, color=CLR_PLANCK, lw=2.2, zorder=4)
ax2.plot([1.80, 2.20], [f_q4_mean * 100] * 2, color=CLR_PLANCK, lw=2.2, zorder=4)

ax2.annotate(f"mean = {f_q1_mean*100:.1f}%",
             xy=(1, f_q1_mean * 100), xytext=(1.35, f_q1_mean * 100),
             fontsize=8.5, color=CLR_TEXT,
             arrowprops=dict(arrowstyle="->", color=CLR_MUTED, lw=0.8))
ax2.annotate(f"mean = {f_q4_mean*100:.1f}%",
             xy=(2, f_q4_mean * 100), xytext=(1.25, f_q4_mean * 100 + 2.0),
             fontsize=8.5, color=CLR_TEXT,
             arrowprops=dict(arrowstyle="->", color=CLR_MUTED, lw=0.8))

ax2.set_xticks([1, 2])
ax2.set_xticklabels([f"Q1 — low mass\n(n={n_q})", f"Q4 — high mass\n(n={n_q})"],
                    color=CLR_TEXT, fontsize=9)
ax2.set_ylabel(r"$f_{\rm UKFT}$ [%]", fontsize=11)
ax2.set_title(f"Cluster Quartile f_UKFT: Q1/Q4 = {ratio_q1q4:.2f}\n"
              "Real WINGS data", fontsize=11)

# Annotation box
ax2.text(0.97, 0.94,
         f"H97-2: Q1/Q4 = {ratio_q1q4:.2f}\n"
         f"target ≥ {RATIO_MIN}\n"
         f"{'PASS ✓' if h972_pass else 'FAIL ✗'}",
         transform=ax2.transAxes, fontsize=9, color=CLR_TEXT,
         va="top", ha="right",
         bbox=dict(boxstyle="round,pad=0.3", facecolor=CLR_BG,
                   edgecolor=CLR_GRID, alpha=0.8))

fig2.tight_layout()
fig2.savefig(os.path.join(OUT_DIR, f"{FIG_PREFIX}quartile_ratio.png"),
             facecolor=CLR_BG, dpi=120)
plt.close(fig2)
print(f"Saved {FIG_PREFIX}quartile_ratio.png")


# ═══════════════════════════════════════════════════════════════════════════════
# §9  Figure 97-3 — r200 vs σ scaling
# ═══════════════════════════════════════════════════════════════════════════════

fig3, ax3 = plt.subplots(figsize=(6, 5), dpi=120)
fig_style(fig3, ax3)

ax3.scatter(log_s, log_r,
            color=CLR_COLL, s=24, alpha=0.8, zorder=3, edgecolors="none",
            label="WINGS clusters")

# Empirical fit
s_fit   = np.linspace(log_s.min(), log_s.max(), 200)
r_fit   = slope_rs * s_fit + intercept_rs
ax3.plot(s_fit, r_fit, color=CLR_ACCENT, lw=1.8, zorder=4,
         label=fr"fit: slope = {slope_rs:.3f}")

# Theoretical SIS prediction (slope = 2.0, pinned to centroid)
r_theo = 2.0 * (s_fit - log_s.mean()) + log_r.mean()
ax3.plot(s_fit, r_theo, color=CLR_PLANCK, lw=1.2, ls="--", zorder=3,
         label=r"SIS: $r_{200} \propto \sigma^2$")

ax3.set_xlabel(r"$\log_{10}(\sigma\;[\mathrm{km/s}])$", fontsize=11)
ax3.set_ylabel(r"$\log_{10}(r_{200}\;[\mathrm{Mpc}])$", fontsize=11)
ax3.set_title(r"$r_{200}$–$\sigma$ Scaling in Real WINGS Data", fontsize=11)
ax3.legend(fontsize=9, framealpha=0, labelcolor=CLR_TEXT)

ax3.text(0.97, 0.10,
         f"H97-3: product = {product:.4f}\n"
         f"target [{IDENT_LO}, {IDENT_HI}]\n"
         f"{'PASS ✓' if h973_pass else 'FAIL ✗'}",
         transform=ax3.transAxes, fontsize=9, color=CLR_TEXT,
         va="bottom", ha="right",
         bbox=dict(boxstyle="round,pad=0.3", facecolor=CLR_BG,
                   edgecolor=CLR_GRID, alpha=0.8))

ax3.text(0.04, 0.94,
         f"slope = {slope_rs:.3f}  r = {r_rs:.3f}\n"
         r"(UKFT predicts slope $\times(2+\alpha)=-2$)",
         transform=ax3.transAxes, fontsize=8.5, color=CLR_MUTED,
         va="top", ha="left")

fig3.tight_layout()
fig3.savefig(os.path.join(OUT_DIR, f"{FIG_PREFIX}r200_sigma_scaling.png"),
             facecolor=CLR_BG, dpi=120)
plt.close(fig3)
print(f"Saved {FIG_PREFIX}r200_sigma_scaling.png")

print("\nExp 97 complete.")
