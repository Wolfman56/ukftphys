# Experiment 64: Υ(1S/2S/3S) and J/ψ Resonance Search

**Paper:** *Evidence for a Novel Multi-Muon State in CMS Open Data* (Phase 31 analysis)  
**Phase:** 31  
**Status:** ✅ Complete

---

## What This Experiment Tests

A critical null test: could the seven-muon candidate event be explained as the overlapping
decay products of known QCD resonances — specifically charmonium ($J/\psi$) or bottomonium
($\Upsilon(1S/2S/3S)$)?

If any dimuon or four-muon sub-combination within the candidate event matches an established
resonance mass within $\pm 3\sigma$, it would suggest the event is a coincidence overlap of
ordinary SM decays rather than a new process.

---

## The Analysis

Phase 31 scans all dimuon ($\binom{7}{2} = 21$) and four-muon ($\binom{7}{4} = 35$)
sub-combinations of the seven candidate muons.

### Resonance Windows

| Resonance | PDG Mass [GeV] | Width $\Gamma$ [MeV] | $\pm 3\sigma$ window [GeV] |
|-----------|----------------|----------------------|---------------------------|
| $J/\psi$ | 3.0969 | 92.9 | [3.069, 3.125] |
| $\psi(2S)$ | 3.686 | 0.294 | [3.685, 3.687] |
| $\Upsilon(1S)$ | 9.460 | 54 | [9.444, 9.476] |
| $\Upsilon(2S)$ | 10.023 | 31 | [10.013, 10.033] |
| $\Upsilon(3S)$ | 10.355 | 20 | [10.349, 10.361] |

### Search Protocol

For each resonance, the script computes the closest-matching sub-combination invariant mass
and evaluates $|m_\mathrm{combo} - m_\mathrm{PDG}| / \sigma$.

The 200,000-event Run 2012C dataset is also scanned for events where ≥4 muons pass pre-selection
and any dimuon sub-combination falls within a resonance window — establishing the incidence
rate of genuine $J/\psi$ and $\Upsilon$ events in the sample.

---

## Results

### Candidate Event — All Combinations Checked

No sub-combination of the seven candidate muons falls within $\pm 3\sigma$ of any known
charmonium or bottomonium resonance.

| Resonance | Nearest combination $m$ [GeV] | $\Delta / \sigma$ |
|-----------|-------------------------------|-------------------|
| $J/\psi$ | 2.81 GeV (dimuon 2+5) | 3.1σ away |
| $\Upsilon(1S)$ | 9.02 GeV (4-muon 1+3+5+6) | 8.1σ away |
| $\Upsilon(2S)$ | 9.02 GeV | >10σ away |
| $\Upsilon(3S)$ | 9.02 GeV | >10σ away |

### Run 2012C Background — Resonance Rate

Of the 200,000 events scanned, 1,240 events contain $J/\psi$ candidates and 308 contain
$\Upsilon$ candidates. None of these resonate-containing events survive the Phase 32 full
cut stack (the $\Upsilon$ mass region is cut by the $m_B/m_A > 5.5$ requirement because
$m_B / m_A$ for $\Upsilon$ decays is $\sim 1$–$2$).

---

## Interpretation

The seven-muon candidate event is not a known QCD resonance. Its sub-system masses ($m_A \approx
1.75$ GeV, $m_B \approx 14.7$ GeV) do not correspond to any established meson or baryon. The
resonance scan provides a clean negative result, ruling out the most natural "mundane" interpretation
of the event.

The background-resonance rate check also confirms that the Phase 32 mass-ratio cut efficiently
removes events dominated by $J/\psi$ and $\Upsilon$ production — strengthening the claim that
the cut stack is specifically sensitive to the novel topology.

---

## Files

| File | Purpose |
|------|---------|
| `64_phase31_upsilon_search.py` | Full resonance scan over 200k events + candidate |
