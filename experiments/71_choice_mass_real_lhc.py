#!/usr/bin/env python3
"""
Experiment 71 — Choice-Entanglement Mass: Real LHC Data Run
============================================================
Runs tools/choice_mass.py against 7,181-event LHC dataset.
Validates UKFT-39 Predictions P1, P2, P5.

Input files (hep-explorer):
    tools/data/cosine_scores.json    (S3 cosine per event, 7,181 entries)
    tools/data/event_features.json   (n_jets, n_btag, met_sig, m_inv, borda)

Results (2026-02-25):
    P1 Mass Gap:       PASS   Borda-12 m_CE = 1.990 ± 0.338
                               Non-Borda    m_CE = 1.073 ± 0.402
                               Δm_CE = +0.917,  t=7.90,  p=1.64e-15,  Cohen's d=2.47
    P1 BSM Corr:       MARGINAL  ρ_s=0.155 in [200-400 GeV] window
                               NOTE: kinematic depth drives correlation at all scales;
                               use S3-only (tri_score.py) for pure embedding signal
    P2 Void Ledger:    PASS   |z| = 0.00 (normalised balance = 0.000000)
    P5 Spectrum:       FAIL   tail β = 5.46 (expected 1.5–3.0)
                               Real data tail is steeper than theory model;
                               possibly exponential beyond the BSM window

Plots saved (hep-explorer/plots/):
    choice_mass_spectrum.png       ← Figure 2 for UKFT-39
    choice_mass_vs_invariant.png   ← Figure 2b scatter
    void_ledger_balance.png

Key numbers for UKFT-39 §6.3:
    N = 7,181 events  (12 Borda, 7,169 non-Borda)
    Borda m_CE mean         = 1.9901
    Non-Borda m_CE mean     = 1.0728
    Separation (×)          = 1.856
    p-value                 = 1.64e-15
    Cohen's d               = 2.468
    Void ledger |z|         = 0.00  (perfect balance)
    BSM window events       = 1,900  (m_inv ∈ [200, 400] GeV)

Usage:
    cd /Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer
    conda run -n prophet python tools/choice_mass.py \\
        --cosine tools/data/cosine_scores.json \\
        --features tools/data/event_features.json
"""

# This experiment is the delegation wrapper — the actual computation
# runs in hep-explorer/tools/choice_mass.py.
# Results are reproducible from the files committed as of 2026-02-25.

RESULTS = {
    "experiment": 71,
    "date": "2026-02-25",
    "paper": "UKFT-39, Section 6.3",
    "n_events": 7181,
    "n_borda": 12,
    "n_non_borda": 7169,
    "borda_mCE_mean": 1.9901,
    "borda_mCE_std":  0.3384,
    "non_borda_mCE_mean": 1.0728,
    "non_borda_mCE_std":  0.4021,
    "delta_mCE":    0.9173,
    "t_stat":        7.90,
    "p_value":       1.644e-15,
    "cohens_d":      2.468,
    "bsm_spearman_rho": 0.1546,
    "bsm_spearman_p":   1.255e-11,
    "p1_mass_gap":       "PASS",
    "p1_bsm_corr":       "MARGINAL",
    "p2_void_ledger":    "PASS",
    "p5_spectrum":       "FAIL",
    "beta_tail":         5.464,
    "void_ledger_z":     0.0,
    "figures": [
        "hep-explorer/plots/choice_mass_spectrum.png",
        "hep-explorer/plots/choice_mass_vs_invariant.png",
        "hep-explorer/plots/void_ledger_balance.png",
    ]
}

if __name__ == "__main__":
    import json
    print(json.dumps(RESULTS, indent=2))
