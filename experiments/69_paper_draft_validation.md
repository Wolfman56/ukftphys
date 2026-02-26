# Experiment 69: Paper Draft Validation — Numbers Consistency Check

**Paper:** *Evidence for a Novel Multi-Muon State in CMS Open Data* — pre-submission gate  
**Phase:** 36  
**Status:** ✅ Complete — arXiv gate OPEN

---

## What This Experiment Tests

Phase 36 is the internal consistency gate before arXiv submission. The goal is to parse the
LaTeX source of the CMS paper and verify that every embedded numerical claim — cross-sections,
event counts, significance values, mass values, isolation figures — matches the computed values
from Phases 22–35.

This is not a physics calculation. It is an automated fact-check: read the paper, extract the
numbers, compare them to the analysis chain, flag any discrepancy.

---

## The Analysis

`69_phase36_paper_draft.py` reads the LaTeX source file (the full `.tex` manuscript) and
applies a series of regular-expression patterns to extract:

| Pattern | Example extracted value |
|---------|------------------------|
| Cross-section claims | "$\sigma < 10^{-9}$ fb" |
| Significance statements | "3.3$\sigma$", "$>10\sigma$" |
| Invariant mass values | "$m_A = 1.747$ GeV", "$m_B = 14.662$ GeV" |
| Mass ratio | "$m_B/m_A = 8.39$" |
| Event counts | "200,000 events", "sole survivor" |
| Isolation values | "iso = 12.9", "iso = 8.9" |
| Impact parameter | "29.2$\sigma$" displacement |
| Background counts | "$N_\mathrm{bkg} = 1.78 \times 10^{-15}$" |

Each extracted value is compared to the reference computed in the relevant experiment.
A pass/fail status is recorded. The output is written to `figures/phase36_paper_numbers.txt`.

---

## Results

All numerical claims in the manuscript pass the consistency check. No discrepancies between
the paper text and the analysis chain were found.

### Summary from `phase36_paper_numbers.txt`

```
ARXIV GATE CHECK — Phase 36
============================
✅ mA = 1.747 GeV          (Phase 30 value: 1.747)
✅ mB = 14.662 GeV         (Phase 30 value: 14.662)
✅ mB/mA = 8.39            (Phase 32 threshold check: pass)
✅ N_bkg (SM) = 1.78e-15   (Phase 28 value: 1.78e-15)
✅ N_bkg (data) = 8 @ C5   (Phase 32 count: 8)
✅ Z_global = 3.3σ          (Phase 35 Method A: 3.3σ)
✅ Z_theory > 10σ           (Phase 35 Method D: >10σ)
✅ iso_muA = 12.9           (Phase 34 value: 12.9)
✅ iso_muB = 8.9            (Phase 34 value: 8.9)
✅ dxy_sig = 29.2σ          (Phase 70 value: 29.2σ)
✅ m_CE (Borda) = 1.990     (Phase 71 value: 1.990)
============================
RESULT: ALL CHECKS PASS — GATE OPEN
```

---

## Interpretation

The automated gate check is a lightweight but important safeguard. In a multi-phase analysis
spanning twelve distinct computational experiments, transcription errors are a real risk.
By grounding every paper claim back to its computation, Phase 36 ensures the manuscript is
self-consistent before submission.

The gate-open result means the paper is cleared for arXiv upload. The check file
`figures/phase36_paper_numbers.txt` serves as an audit log for reviewers.

---

## Files

| File | Purpose |
|------|---------|
| `69_phase36_paper_draft.py` | LaTeX parsing and number extraction |
| `results/phase36_paper_numbers.txt` | Full consistency check output |
