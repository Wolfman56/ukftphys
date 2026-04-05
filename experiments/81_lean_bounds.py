"""Experiment 81 — Lean bound extraction.

Reads the existing MadGraph5 LHE sample (10k events of pp → Xm Xm~),
applies the full W_ΣΔ sigma-delta weighting, and produces tight numerical
bounds suitable for hardcoding into the Lean theorems:

    glitch_asymmetry_from_sigma_delta  (ChoiceBohmian.lean)
    glitch_asymmetry_recovered         (QFT_MirrorFermion.lean)

Outputs:
    - Integrated asymmetry A_mean and A_std over pT ∈ [50, 500] GeV
    - Tight ε bound for the |A − target| < ε Lean statement
    - Per-event charge_asym_scalar values (mean ± std)

Run: conda activate prophet && python 81_lean_bounds.py
"""

import gzip
import math
import os
import statistics

# ── Paths ────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
LHE  = os.path.join(BASE, "81_glitch_source/Events/run_01/unweighted_events.lhe.gz")

# ── W_ΣΔ formula (mirrors Lean: QFT_MirrorFermion.mf_amplitude) ─────────────
DELTA_D   = math.pi**4 / 384     # E8 packing density ≈ 0.2537
ALPHA_QED = 1.0 / 137.036
PRIME_PROXY = 151                  # Teilhard bio-noo boundary (zero #15)

def sigma_delta_weight(pt_gev: float) -> float:
    """W_ΣΔ(p=151, pT) — matches QFT_MirrorFermion.sigma_delta_weight."""
    bit_len = math.floor(math.log2(max(PRIME_PROXY, 2)))
    S = math.log(max(pt_gev, 1.0)) * ALPHA_QED
    return DELTA_D / (bit_len + 1) * math.exp(-S)

# ── LHE parser ───────────────────────────────────────────────────────────────
PID_XM = 6000001

class Particle:
    __slots__ = ("px", "py", "pz", "E", "pid")
    def __init__(self, px, py, pz, E, pid):
        self.px, self.py, self.pz, self.E, self.pid = px, py, pz, E, pid

    def pt(self) -> float:
        return math.sqrt(self.px**2 + self.py**2)

def parse_lhe(path: str):
    events = []
    with gzip.open(path, "rt") as f:
        current: list[Particle] = []
        in_event = False
        for line in f:
            if "<event>" in line:
                in_event = True;  current = [];  continue
            if "</event>" in line:
                in_event = False;  events.append(current);  continue
            if not in_event:
                continue
            parts = line.split()
            if len(parts) < 10:
                continue
            try:
                pid    = int(parts[0])
                px, py, pz, E = (float(parts[i]) for i in (6, 7, 8, 9))
                current.append(Particle(px, py, pz, E, pid))
            except ValueError:
                pass
    return events

# ── Analysis ─────────────────────────────────────────────────────────────────
def analyze():
    print(f"Reading {LHE} …")
    events = parse_lhe(LHE)
    print(f"Loaded {len(events)} events.")

    # Global weighted counts
    W_matter = 0.0
    W_antimatter = 0.0

    # Per-event asymmetries for charge_asym_scalar distribution
    per_event_asym: list[float] = []

    # b-decay scale (see Exp 81 comment: ~35% of parent)
    DECAY_SCALE = 0.35

    for event in events:
        xms = [p for p in event if abs(p.pid) == PID_XM]
        if not xms:
            continue

        ev_matter = 0.0
        ev_anti   = 0.0

        for xm in xms:
            pt = math.sqrt((xm.px * DECAY_SCALE)**2 + (xm.py * DECAY_SCALE)**2)
            w = sigma_delta_weight(max(pt, 1.0))
            if xm.pid > 0:   # Xm (matter)
                ev_matter += 1.0 + w
            else:            # Xm~ (antimatter)
                ev_anti   += 1.0 - w

        W_matter     += ev_matter
        W_antimatter += ev_anti

        # charge_asym_scalar for this event (Lean observable)
        denom = ev_matter + ev_anti
        if denom > 0:
            per_event_asym.append((ev_matter - ev_anti) / denom)

    # ── Integrated asymmetry ─────────────────────────────────────────────────
    A_int = (W_matter - W_antimatter) / (W_matter + W_antimatter)

    A_mean = statistics.mean(per_event_asym)
    A_std  = statistics.stdev(per_event_asym) if len(per_event_asym) > 1 else 0.0
    A_max  = max(abs(a) for a in per_event_asym)

    print()
    print("=" * 60)
    print(f"  W_ΣΔ at p=151, pT=150 GeV : {sigma_delta_weight(150):.6e}")
    print(f"  Integrated asymmetry A_int : {A_int:.8f}")
    print(f"  Per-event A mean           : {A_mean:.8f}")
    print(f"  Per-event A std            : {A_std:.8f}")
    print(f"  Per-event A max            : {A_max:.8f}")
    print(f"  Events with Xm             : {len(per_event_asym)}")
    print("=" * 60)

    # ── Lean bound recommendations ────────────────────────────────────────────
    # glitch_asymmetry_recovered: ∃ ε > 0, ∀ events, |A - 10⁻³| < ε
    # We use A_max as the conservative bound across all events.
    # The actual A values are O(W_ΣΔ) ≈ 10⁻³, so ε = A_max + 1e-4 is tight.
    eps_recovered = round(A_max + 1e-4, 6)

    # glitch_asymmetry_from_sigma_delta: charge_asym = 1/1000
    # In ChoiceBohmian, charge_asym uses canonical all-True bitstream.
    # The per-event distribution from MadGraph gives the physics answer.
    print()
    print("Lean bound recommendations:")
    print(f"  glitch_asymmetry_recovered  ε  = {eps_recovered}  (A_max + 1e-4)")
    print(f"  glitch_asymmetry_from_sigma: target A_int = {A_int:.6f}")
    print()
    print("Paste into Lean:")
    print(f"  -- glitch_asymmetry_recovered")
    print(f"  use {eps_recovered}")
    print(f"  -- glitch_asymmetry_from_sigma_delta:")
    print(f"  -- charge_asym target ≈ {A_int:.4e} (integrated over 10k events)")

if __name__ == "__main__":
    analyze()
