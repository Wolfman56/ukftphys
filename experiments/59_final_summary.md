# Experiment 59: Choice-Entanglement Mass — Results Summary

**Date:** 2026-02-25
**Paper:** UKFT-39, Section 6.2

## Quantitative Results

### P1 — Mass Gap (Theo vs. Geo)
| Level | m_CE mean | m_CE std |
|---|---|---|
| geo | 0.1716 | 0.0373 |
| bio | 2.4784 | 0.2614 |
| noo | 43.6411 | 0.9178 |
| theo | 434.9961 | 0.7565 |

**Theo/Geo ratio: 2535.3x** (pass threshold: >10x) — PASS ✅

### P3 — Void Ledger Balance (Flatness)
κ is dimensionless fractional curvature: 0 = perfectly flat, 1 = fully unbalanced.
- Baseline |κ| mean (ledger active):    0.1572 (pass: <0.50) — PASS ✅

### P4 — Curvature During Disruption / Recovery
- Disruption |κ| mean (ledger disabled): 1.0000 (pass: >0.70) — PASS ✅
- Restored  |κ| mean (ledger re-active): 0.0000  (pass: < disruption) — PASS ✅

## Plots Generated
- `59_void_ledger_balance.png` — ledger balance and κ(t)
- `59_mass_spectrum.png` — bimodal m_CE distribution
- `59_inertia_recovery.png` — post-kick recovery by level
- `59_mass_growth.png` — m_CE accumulation over time

## Interpretation
The simulation confirms UKFT-39 predictions:
- Choice-entanglement mass accumulates exponentially faster in higher-hierarchy nodes (theo >> geo)
- Heavier (more choice-entangled) nodes resist scatter and recover faster after chaos kicks
- The void ledger keeps global action balanced (κ ≈ 0) when active
- Disabling the void ledger immediately generates curvature (κ ≠ 0) — geometry is not self-sustaining without ledger conservation
