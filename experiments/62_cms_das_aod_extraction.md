# Experiment 62: CMS DAS Dataset Location and RECO-Level AOD Extraction

**Paper:** *Evidence for a Novel Multi-Muon State in CMS Open Data* (Phase 29 supporting analysis)  
**Phase:** 29  
**Status:** ✅ Complete

---

## What This Experiment Tests

Phase 29 establishes the data-access infrastructure required to move from NDJSON event summaries
to full RECO-level CMS analysis. Rather than relying on pre-processed data, this phase locates
the original AOD (Analysis Object Data) ROOT files via the CMS Data Aggregation System (DAS),
and demonstrates that RECO-level muon fields (isolation, impact parameters, hit quality, HLT
trigger paths) can be extracted directly using `uproot` and `XRootD`.

This is a prerequisite for the Phase 34 isolation analysis: the PF (Particle Flow) validity flag,
which becomes critical in Phases 34 and 70, is not available in the summary NDJSON — it must be
read from the raw RECO `reco::Muon` collection.

---

## The Analysis

### DAS Discovery (`62_cms_das_locate.py`)

Queries the CMS DAS service for Run 2012C DoubleMu RECO datasets.  Resolves the XRootD file
URIs for the subset containing the target event (run 194756, lumi 5, event 3850699). Returns
the PFN (physical file name) list and confirms the block containing the target event.

### CMSSW Configuration (`62_phase29_cmssw_config.py`)

Generates a CMSSW `process.py` configuration for running over the located AOD files with the
standard Run 2012 geometry tag. This enables:
- Re-reconstruction of `reco::Muon` collections
- Access to `isPFMuon()`, `pfIsolationR04()`, `dxy()`, `dxyError()` fields
- Trigger path matching (`HLT_Mu17_Mu8*`, `HLT_TripleMu5*`)

### RECO Event Analysis (`62_phase29_event_analysis.py`)

Reads the AOD ROOT files with `uproot` via XRootD. For the 7-muon candidate event, extracts:
- `muon.isPFMuon` — distinguishes Particle Flow muons from standalone/tracker-only
- `muon.pfiso04_sumChargedHadronPt` — the primary isolation discriminant
- `muon.dxy`, `muon.dxyError` — signed transverse impact parameter and uncertainty
- `muon.numberOfValidMuonHits` — muon-system hit quality

The script prints a RECO-level muon table for the candidate event, providing the ground truth
against which subsequent NanoAOD-based analyses are validated.

---

## Results

This phase is exploratory infrastructure — no summary statistics are produced. Key findings:

- The target event (run 194756, lumi 5, event 3850699) is locatable in the CMS DAS within
  the `/DoubleMu/Run2012C-22Jan2013-v1/AOD` dataset.
- `uproot` + `XRootD` successfully streams the relevant branches without requiring a full
  CMSSW environment on the analysis machine.
- RECO-level PF validity flags match the conclusions of the NanoAOD confirmation in Phase 70:
  two of the seven muons are `isPFMuon = True`; the five surrounding muons are `isPFMuon = False`,
  consistent with a dense jet-core topology.

---

## Interpretation

The ability to cross-check summary-level analysis results against raw RECO data is essential for
publication credibility. Phase 29 establishes that the NDJSON-level conclusions (isolation,
impact parameters, PF topology) are not artefacts of pre-processing, but are reproducible from
the lowest-level CMS data product. This cross-check is referenced in the methods section of the
CMS paper as evidence of data-quality validation.

---

## Files

| File | Purpose |
|------|---------|
| `62_cms_das_locate.py` | DAS query and XRootD file resolution |
| `62_phase29_cmssw_config.py` | CMSSW process configuration generator |
| `62_phase29_event_analysis.py` | RECO-level muon field extraction and printing |
