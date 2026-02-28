"""Append experiments 61-71 entries to README.md."""
import os

readme = os.path.join(os.path.dirname(__file__), "README.md")

entries = r"""
### [61_sm_7muon_background.md](./61_sm_7muon_background.md)
**Objective**: SM 7-Muon Background Rate Estimation (Phase 28).
*   **Paper**: *Evidence for a Novel Multi-Muon State in CMS Open Data* (supporting calculation)
*   **Concept**: MadGraph5 LO calculation of $pp \to 4\mu$ at 8 TeV as anchor; analytic EW coupling scaling ($\times\alpha_{EW}^{2\Delta n}$ per extra muon pair) extrapolates to 7-muon cross-section; Phase-26 cut efficiencies applied to get expected background count.
*   **Result**: $\sigma(7\mu) \approx 3.3 \times 10^{-10}$ fb → $N_\mathrm{bkg} \approx 1.78 \times 10^{-15}$ at 20 fb⁻¹. SM background negligible at any realistic luminosity.
*   **Figures**: `61_sm_7muon_cross_section_scaling.png`.

### [62_cms_das_aod_extraction.md](./62_cms_das_aod_extraction.md)
**Objective**: CMS DAS Dataset Location and RECO-Level AOD Extraction (Phase 29).
*   **Paper**: *Evidence for a Novel Multi-Muon State in CMS Open Data* (infrastructure)
*   **Concept**: Query CMS DAS for Run 2012C DoubleMu RECO; resolve XRootD file URIs for the block containing the target event; extract `isPFMuon`, `pfIsolationR04`, `dxy`, `dxyError`, `numberOfValidMuonHits` via uproot from AOD ROOT files.
*   **Result**: Target event (run 194756, lumi 5, event 3850699) located; RECO PF validity confirms summary-level conclusions: 2 PF muons, 5 non-PF.

### [63_reco_muon_masses.md](./63_reco_muon_masses.md)
**Objective**: RECO-Level Muon Kinematics — Charge, Sub-Masses, Grouping (Phase 30).
*   **Paper**: *Evidence for a Novel Multi-Muon State in CMS Open Data* §4
*   **Concept**: Seven RECO muons partitioned into charge-balanced Group A (inner, 4 muons) and Group B (outer, 3 muons); all 35 sub-combination masses computed; primary discriminants $m_A$ and $m_B$ extracted.
*   **Result**: $m_A = 1.747$ GeV, $m_B = 14.662$ GeV, ratio $m_B/m_A = 8.39$.

### [64_upsilon_resonance_search.md](./64_upsilon_resonance_search.md)
**Objective**: Upsilon(1S/2S/3S) and J/psi Resonance Null Test (Phase 31).
*   **Paper**: *Evidence for a Novel Multi-Muon State in CMS Open Data* §4.2
*   **Concept**: Scan all 21 dimuon and 35 four-muon sub-combinations of the candidate event against PDG windows for J/psi, psi(2S), Upsilon(1S/2S/3S); scan 200k Run 2012C events for genuine resonance rate.
*   **Result**: No sub-combination within ±3sigma of any known resonance. Target event is not a QCD resonance overlap.

### [65_cutflow_sole_survivor.md](./65_cutflow_sole_survivor.md)
**Objective**: Full Phase 22-26 Cut Stack — Sole Survivor Confirmation (Phase 32).
*   **Paper**: *Evidence for a Novel Multi-Muon State in CMS Open Data* §4.3
*   **Concept**: Apply all six cuts (C1-C6) sequentially to 200k Run 2012C events; threshold scan on $m_B/m_A$ from 2.0 to 8.0; confirm target event survives and no other event does.
*   **Result**: Sole survivor confirmed: run 194756 / lumi 5 / event 3850699; robust at all thresholds 5.0-7.9.

### [66_cutflow_rejection_figure.md](./66_cutflow_rejection_figure.md)
**Objective**: Publication Cut-Flow Rejection Curve (Phase 33).
*   **Paper**: *Evidence for a Novel Multi-Muon State in CMS Open Data* Appendix B
*   **Concept**: Two-panel log-scale figure: rejection factor per cut stage (Run 2012B 26M + Run 2012C 200k) and absolute survivor count; print-compatible light palette for JHEP submission.
*   **Result**: Total rejection ~1e7; both datasets converge to 1 survivor at C5-C6.
*   **Figures**: `66_cutflow_rejection_curve.png`.

### [67_isolation_ip_analysis.md](./67_isolation_ip_analysis.md)
**Objective**: Isolation, PF Validity, and Impact-Parameter Analysis (Phase 34).
*   **Paper**: *Evidence for a Novel Multi-Muon State in CMS Open Data* §4.3, §5.2
*   **Concept**: Run 2012B NanoAOD: flag non-PF muons (iso=-999), compute PF fraction at cut stages C3-C5; compare candidate event's 2/7 PF topology against 100%-non-PF background; report d_xy significance.
*   **Result**: 100% of background at C3-C5 has >=1 non-PF muon; candidate has mixed (2 PF + 5 non-PF) topology absent from background.
*   **Figures**: `67_isolation_distributions.png`, `67_isolation_vs_cuts.png`.

### [68_significance_computation.md](./68_significance_computation.md)
**Objective**: Final Significance: Power-Law Tail Fit + Four-Method Summary (Phase 35).
*   **Paper**: *Evidence for a Novel Multi-Muon State in CMS Open Data* §5, §6
*   **Concept**: Power-law fit to $m_B/m_A$ tail of C4-surviving events; extrapolate expected background under candidate's $m_B/m_A=8.39$; four significance methods A-D; add Q_A=0 charge cut.
*   **Result**: $Z_\mathrm{global}=3.3\sigma$ (conservative data-driven); $Z_\mathrm{theory}>10\sigma$; $Z_{Q_A=0}\geq5\sigma$.
*   **Figures**: `68_significance_ratio_fit.png`.

### [69_paper_draft_validation.md](./69_paper_draft_validation.md)
**Objective**: LaTeX Manuscript Consistency Check — arXiv Gate (Phase 36).
*   **Paper**: *Evidence for a Novel Multi-Muon State in CMS Open Data* (pre-submission)
*   **Concept**: Parse LaTeX source with regex; extract every embedded number (mA, mB, N_bkg, Z, iso, d_xy, m_CE); compare to analysis-chain reference values; pass/fail each numerical claim.
*   **Result**: All 11 numerical checks pass. **arXiv gate: OPEN.**

### [70_nanoaod_confirmation.md](./70_nanoaod_confirmation.md)
**Objective**: NanoAOD Independent Confirmation — Isolation and Displaced Vertex (Phase 71).
*   **Paper**: *Evidence for a Novel Multi-Muon State in CMS Open Data* §4.4
*   **Concept**: Stream full Run 2012C NanoAOD (35M events); locate target event by (run,lumi,event); extract pfRelIso04_all, dxy, dxyErr, isPFcand for all 16 reconstructed muons; cross-check against NDJSON conclusions.
*   **Result**: 14 non-PF sentinels + 2 PF-valid; Muon A: iso=12.9, d_xy=4.1sigma; Muon B: iso=8.9, **d_xy=29.2sigma** (467 micron displaced vertex); fully confirmed.
*   **Figures**: `70_displaced_vertex_significance.png`.

### [71_choice_mass_real_lhc.md](./71_choice_mass_real_lhc.md)
**Objective**: Choice-Entanglement Mass $m_\mathrm{CE}$ vs Real LHC Data — UKFT-39 Validation (Phase 71).
*   **Paper**: UKFT-39 — *Mass as Conscious Choice-Entanglement* §7
*   **Concept**: Compute $m_\mathrm{CE} = \sum_i \rho_i^2$ from the 7,181-event CMS dataset projected onto the UKFT knowledge manifold; test P1 (BSM elevation), P2 (void ledger flatness), P5 (tail power law).
*   **Predictions Tested**: P1 (m_CE(BSM)=1.990 vs m_CE(SM)=1.073, d=2.47, p=1.6e-15 ✅), P2 (|z|=0.00 ✅), P5 (beta=5.46, expected 1.5-3.0 ⚠️).
*   **Result**: Two of three predictions pass; P5 flags a domain-of-applicability question for synthetic-to-real tail exponent transfer.
*   **Figures**: `71_choice_mass_spectrum.png`, `71_void_ledger_balance.png`.
"""

with open(readme, "a", encoding="utf-8") as f:
    f.write(entries)

print(f"Appended. New size: {os.path.getsize(readme)} bytes")
