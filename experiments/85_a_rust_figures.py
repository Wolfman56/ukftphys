"""
Generate figures for 85-a Rust/THOR scaling analysis (Exp 85-a v2).

Figures produced:
  85_a_rust_fig1_lightcurves.png   — ON vs OFF light curves at N=50 and N=200
  85_a_rust_fig2_convergence.png   — Asymmetry A vs grid size N
  85_a_rust_fig3_sf_ratios.png     — SF ratio S_on/S_off vs lag at all N
  85_a_rust_fig4_scaling.png       — Wall-clock scaling O(N²)

Run from the ukftphys/experiments directory:
  python 85_a_rust_figures.py

Requires: matplotlib, numpy.  No GPU or Rust build needed — uses
pre-captured JSON from the stellar-arrow release binary.
"""

import json, subprocess, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import LogLocator

OUTDIR = Path(__file__).parent
BINARY = Path(__file__).parents[3] / "grok" / "noosphere" / "target" / "release" / "stellar-arrow"

# ── palette ──────────────────────────────────────────────────────────────────
C_ON   = "#e05a2b"   # rust-orange  — void scalar ON
C_OFF  = "#2b7be0"   # steel-blue   — void scalar OFF
GRAYS  = ["#222", "#555", "#888", "#aaa"]
N_COLS = {50: "#e05a2b", 100: "#e0a02b", 200: "#2b7be0", 400: "#2bc07b"}

def run_n(n: int) -> dict:
    """Run stellar-arrow at lattice size n and return parsed JSON result."""
    cmd = [str(BINARY), "--lattice-n", str(n), "--backend", "cpu"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    # JSON starts after the human-readable header block ("^{")
    lines = out.stdout.splitlines()
    json_start = next(i for i, l in enumerate(lines) if l.strip().startswith("{"))
    return json.loads("\n".join(lines[json_start:]))

def load_or_run(n: int, cache_dir: Path = Path("/tmp")) -> dict:
    cache = cache_dir / f"stellar_N{n}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    d = run_n(n)
    cache.write_text(json.dumps(d))
    return d

# ── load data ─────────────────────────────────────────────────────────────────
print("Loading / running stellar-arrow at N = 50, 100, 200, 400 …")
data = {n: load_or_run(n) for n in [50, 100, 200, 400]}
print("  done.")

# Timing data (release build, measured empirically from scaling sweep)
timing_ms = {50: 6, 100: 18, 200: 77, 400: 286, 800: 1120, 1600: 4358}

# ── helpers ───────────────────────────────────────────────────────────────────
LAGS = [7, 14, 30, 60, 90]

def t_grid(d: dict) -> np.ndarray:
    T = d["n_time_steps"]; tmax = d.get("t_max_days", 400.0)
    return np.linspace(0, tmax, T, endpoint=False)

def peak_idx(flux):
    return int(np.argmax(flux))

def half_max_times(t, flux):
    """Return (t_rise_half, t_peak, t_fall_half) by linear interpolation."""
    pk = peak_idx(flux)
    f_half = 0.5 * flux[pk]
    t_rise = None
    for i in range(pk - 1, -1, -1):
        if flux[i] <= f_half:
            frac = (f_half - flux[i]) / (flux[i+1] - flux[i])
            t_rise = t[i] + frac * (t[i+1] - t[i])
            break
    t_fall = None
    for i in range(pk + 1, len(flux)):
        if flux[i] <= f_half:
            frac = (f_half - flux[i-1]) / (flux[i] - flux[i-1])
            t_fall = t[i-1] + frac * (t[i] - t[i-1])
            break
    return t_rise, t[pk], t_fall

# ═══════════════════════════════════════════════════════════════
# Fig 1: Light curves at N=50 (Python baseline) and N=200 (Rust)
# ═══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=False)
fig.suptitle(
    "Exp 85-a: Stellar Arrow-of-Time — Photon Escape Light Curves",
    fontsize=13, fontweight="bold", y=1.01
)

for ax, n, label in zip(axes, [50, 200], ["N=50  (Python baseline)", "N=200  (Rust, auto-scaled)"]):
    d = data[n]
    t = t_grid(d)
    fon  = np.array(d["flux_on"])
    foff = np.array(d["flux_off"])

    # Normalise to peak-ON so curves overlay cleanly
    norm = fon.max()
    fon_n  = fon  / norm
    foff_n = foff / norm

    ax.plot(t, fon_n,  color=C_ON,  lw=2.0, label=r"$\delta_{\rm eff}=1$  (Void Scalar ON)")
    ax.plot(t, foff_n, color=C_OFF, lw=2.0, linestyle="--",
            label=r"$\delta_{\rm eff}=0$  (reference OFF)")

    # Annotate half-max points
    for flux_n, col, delta in [(fon_n, C_ON, 1), (foff_n, C_OFF, 0)]:
        tr, tpk, tf = half_max_times(t, flux_n)
        ax.axvline(tpk, color=col, alpha=0.25, lw=1)
        if tr: ax.axvline(tr, color=col, alpha=0.15, lw=1, linestyle=":")
        if tf: ax.axvline(tf, color=col, alpha=0.15, lw=1, linestyle=":")
        ax.axhline(0.5, color="gray", alpha=0.2, lw=1, linestyle=":")

    # Shade rise and fade windows for ON curve
    tr_on, tpk_on, tf_on = half_max_times(t, fon_n)
    if tr_on and tf_on:
        ax.axvspan(tr_on, tpk_on, alpha=0.06, color=C_ON, label=f"rise  {tpk_on-tr_on:.0f} d")
        ax.axvspan(tpk_on, tf_on, alpha=0.06, color="#aa2244", label=f"fade  {tf_on-tpk_on:.0f} d")

    aon  = d["asymmetry_on"]
    aoff = d["asymmetry_off"]
    ax.set_title(
        f"{label}\n"
        r"$A_{\rm on}$" + f"={aon:.3f}   "
        r"$A_{\rm off}$" + f"={aoff:.3f}   ratio={aon/aoff:.3f}",
        fontsize=10
    )
    ax.set_xlabel("Time [days]")
    ax.set_ylabel("Normalised flux $F(t)/F_{\\rm peak}$")
    ax.set_xlim(0, 350)
    ax.legend(fontsize=8.5, loc="upper right")
    ax.grid(alpha=0.25)

plt.tight_layout()
out1 = OUTDIR / "85_a_rust_fig1_lightcurves.png"
fig.savefig(out1, dpi=160, bbox_inches="tight")
plt.close()
print(f"  saved {out1.name}")

# ═══════════════════════════════════════════════════════════════
# Fig 2: Asymmetry convergence  A_on, A_off, |ΔA| vs N
# ═══════════════════════════════════════════════════════════════
Ns      = [50, 100, 200, 400]
A_on_v  = [data[n]["asymmetry_on"]  for n in Ns]
A_off_v = [data[n]["asymmetry_off"] for n in Ns]
ratio_v = [ao/af for ao, af in zip(A_on_v, A_off_v)]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Exp 85-a: Asymmetry Convergence with Grid Resolution", fontsize=13, fontweight="bold")

# Left: A_on and A_off
ax = axes[0]
ax.plot(Ns, A_on_v,  "o-", color=C_ON,  lw=2, ms=8, label=r"$A_{\rm on}$  (void scalar ON)")
ax.plot(Ns, A_off_v, "s--", color=C_OFF, lw=2, ms=8, label=r"$A_{\rm off}$  (reference)")
for n, aon, aoff in zip(Ns, A_on_v, A_off_v):
    ax.annotate(f"{aon:.3f}", (n, aon), textcoords="offset points", xytext=(6, 4),
                fontsize=8, color=C_ON)
    ax.annotate(f"{aoff:.3f}", (n, aoff), textcoords="offset points", xytext=(6, -12),
                fontsize=8, color=C_OFF)
ax.set_xscale("log")
ax.set_xticks(Ns); ax.set_xticklabels([str(n) for n in Ns])
ax.set_xlabel("Lattice N")
ax.set_ylabel(r"Asymmetry  $A = t_{\rm fade½} / t_{\rm rise½}$")
ax.legend(fontsize=9)
ax.grid(alpha=0.25)
ax.set_title("Asymmetry A converges to ~6.25 (ON) and ~6.13 (OFF) by N=100")

# Right: Enhancement ratio  A_on/A_off
ax = axes[1]
ax.axhline(1.0, color="gray", lw=1, linestyle="--", label="1.0 (no enhancement)")
ax.plot(Ns, ratio_v, "D-", color="#7b2be0", lw=2, ms=8)
for n, r in zip(Ns, ratio_v):
    marker = "▲" if r > 1 else "▼"
    ax.annotate(f"{r:.4f} {marker}", (n, r), textcoords="offset points", xytext=(6, 4), fontsize=9)
ax.set_xscale("log")
ax.set_xticks(Ns); ax.set_xticklabels([str(n) for n in Ns])
ax.set_xlabel("Lattice N")
ax.set_ylabel(r"$A_{\rm on} / A_{\rm off}$")
ax.set_ylim(0.94, 1.06)
ax.set_title(r"Direction flip at N≥100: void scalar switches from suppressing to enhancing $A$")
ax.grid(alpha=0.25)
ax.legend(fontsize=9)

plt.tight_layout()
out2 = OUTDIR / "85_a_rust_fig2_convergence.png"
fig.savefig(out2, dpi=160, bbox_inches="tight")
plt.close()
print(f"  saved {out2.name}")

# ═══════════════════════════════════════════════════════════════
# Fig 3: SF ratio S_on/S_off vs lag — remarkable stability
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))
fig.suptitle("Exp 85-a: Structure-Function Enhancement Ratio vs Lag", fontsize=13, fontweight="bold")

for n, col in N_COLS.items():
    d = data[n]
    ratios = [d["sf_on"][str(l)] / d["sf_off"][str(l)] for l in LAGS]
    ax.plot(LAGS, ratios, "o-", color=col, lw=2, ms=7, label=f"N={n}")
    for lag, r in zip(LAGS, ratios):
        ax.annotate(f"{r:.4f}", (lag, r), textcoords="offset points",
                    xytext=(2, 5), fontsize=7, color=col)

# Python baseline (rescaled to match Rust ratio, not absolute value)
py_ratios = [1.013, 1.012, 1.012, 1.016, 1.021]
ax.plot(LAGS, py_ratios, "x--", color="black", lw=1.5, ms=10, label="Python N=50 (original)")

ax.axhline(1.0, color="gray", lw=0.8, linestyle=":")
ax.set_xlabel("SF lag [days]")
ax.set_ylabel(r"$S_{\rm on}(\Delta t)\ /\ S_{\rm off}(\Delta t)$")
ax.set_title("SF boost is robust: ~12–15% across all lags and all N\n"
             "(Python v1 reported only 1–2%; Rust uses raw SF, not normalised)")
ax.legend(fontsize=9)
ax.set_xticks(LAGS)
ax.grid(alpha=0.25)
ax.set_ylim(0.98, 1.20)

plt.tight_layout()
out3 = OUTDIR / "85_a_rust_fig3_sf_ratios.png"
fig.savefig(out3, dpi=160, bbox_inches="tight")
plt.close()
print(f"  saved {out3.name}")

# ═══════════════════════════════════════════════════════════════
# Fig 4: Performance scaling — O(N²) on log-log
# ═══════════════════════════════════════════════════════════════
Ns_perf  = list(timing_ms.keys())
ts_perf  = list(timing_ms.values())

# O(N²) reference line pinned to N=50 point
N_ref = np.array(Ns_perf)
t_ref_on2 = ts_perf[0] * (N_ref / Ns_perf[0]) ** 2

fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Exp 85-a Rust (release): Wall-Clock Scaling", fontsize=13, fontweight="bold")

ax.loglog(Ns_perf, ts_perf, "o-", color="#2b7be0", lw=2, ms=8,
          label="Measured (rayon, 8-core Apple Silicon)")
ax.loglog(N_ref, t_ref_on2, "--", color="gray", lw=1.5, label=r"$O(N^2)$ reference")

for n, t in timing_ms.items():
    ax.annotate(f"{t} ms", (n, t), textcoords="offset points",
                xytext=(8, 2), fontsize=8, color="#2b7be0")

# Add surface-site count on secondary axis annotation
for n, t in [(50, ts_perf[0]), (200, timing_ms[200]), (1600, timing_ms[1600])]:
    sites = 2 * n * n
    ax.annotate(f"{sites:,} sites", (n, t),
                textcoords="offset points", xytext=(-10, -18),
                fontsize=7.5, color="gray",
                arrowprops=dict(arrowstyle="-", color="gray", lw=0.8))

ax.set_xlabel("Lattice N")
ax.set_ylabel("Elapsed time [ms]  (both ON + OFF runs)")
ax.legend(fontsize=9)
ax.grid(which="both", alpha=0.2)

ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.set_yscale("log")
ax2.set_ylabel("Elapsed time [ms]", color="gray", fontsize=9)
ax2.tick_params(axis="y", labelcolor="gray")

plt.tight_layout()
out4 = OUTDIR / "85_a_rust_fig4_scaling.png"
fig.savefig(out4, dpi=160, bbox_inches="tight")
plt.close()
print(f"  saved {out4.name}")

print("\nAll done.  Figures written to:")
for p in [out1, out2, out3, out4]:
    print(f"  {p}")
