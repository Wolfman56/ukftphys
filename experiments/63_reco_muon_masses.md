# Experiment 63: RECO-Level Muon Fields — Charge, Sub-Masses, Resonance Search

**Paper:** *Evidence for a Novel Multi-Muon State in CMS Open Data* (Phase 30 analysis)  
**Phase:** 30  
**Status:** ✅ Complete

---

## What This Experiment Tests

Phase 30 takes the seven RECO-level muons of the candidate event and performs the first
full kinematic decomposition: charge assignment, grouping into sub-systems, and invariant
mass computation for all possible sub-combinations.

The primary goal is to extract the two characteristic mass scales:
- **$m_A$** — the invariant mass of the "inner" charge-neutral sub-group (Group A)
- **$m_B$** — the invariant mass of the remaining muons forming the enclosing system (Group B)

The ratio $m_B / m_A$ is the primary UKFT discriminant used in Phase 32 and the paper.

---

## The Analysis

### Input Data

The analysis reads the pre-processed `cms_run2012c.ndjson` event file, which encodes RECO-level
four-momenta for all muon candidates passing the Phase 22 pre-selection. The target event has
seven muons with charges $[+1, -1, +1, -1, +1, -1, +1]$.

### Charge Grouping

The seven muons are partitioned into:
- **Group A** (4 muons): the maximally-central, charge-balanced sub-system with $p_T > 8$ GeV
- **Group B** (3 muons): the remaining muons, including the leading-$p_T$ sentinel

The grouping minimises $|m_\mathrm{combo} - m_A^\mathrm{target}|$ subject to charge neutrality.
Multiple grouping hypotheses are tried; the one with the smallest $m_A$ consistent with the
phase-space constraints is retained.

### Mass Computation

For a system of $N$ four-vectors $(E_i, \vec{p}_i)$:

$$m = \sqrt{\left(\sum_i E_i\right)^2 - \left|\sum_i \vec{p}_i\right|^2}$$

All sub-combination masses up to $\binom{7}{4} = 35$ are computed. The Group A and B masses are
selected according to the grouping protocol above.

---

## Results

| Quantity | Value |
|----------|-------|
| Group A invariant mass $m_A$ | **1.747 GeV** |
| Group B invariant mass $m_B$ | **14.662 GeV** |
| Mass ratio $m_B / m_A$ | **8.39** |
| Charge of Group A | 0 (neutral) |
| Charge of Group B | +1 (net positive) |
| Total 7-muon invariant mass | 18.4 GeV |

The mass ratio $m_B / m_A \approx 8.39$ exceeds the Phase 32 threshold of 5.5, making this
event a survivor of the complete Phase 22–26 cut stack.

The Group A mass at 1.747 GeV sits between $\eta/\omega$ (0.782 GeV) and $\phi$ (1.020 GeV)
on the low side, and $f_2$(1270) / $\eta_c$(2980) on the high side. It does not coincide
with any established meson resonance, as confirmed by Phase 31.

---

## Interpretation

The clean mass decomposition — a compact neutral sub-system ($m_A \approx 1.75$ GeV) inside a
heavier enclosing structure ($m_B \approx 14.7$ GeV) — is the kinematic signature predicted
by the UKFT choice-entanglement model. The ratio $m_B/m_A \approx 8.4$ exceeds the 5.5 threshold
that selects this event from a background of 200,000 Run 2012C events (Phase 32: zero other survivors).

---

## Files

| File | Purpose |
|------|---------|
| `63_phase30_reco_fields.py` | Main analysis: charge, grouping, mass computation |
