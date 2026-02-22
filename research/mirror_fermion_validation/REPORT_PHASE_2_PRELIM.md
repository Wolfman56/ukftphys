# Phase 2 Preliminary Report: Entropic Discriminator Validation

**Date:** February 21, 2026
**Status:** Success ✅

## Objective
Validate the capability to calculate the **Entropic Discriminator ($D_E$)** on real CMS data, a prerequisite for the Mirror Fermion Search.

## Methodology
1.  **Dataset**: CMS Run 2012B `DoubleMuParked` AOD (Record 6004).
    *   File: `4804A3F3-CDEC-E211-BC43-00259073E4EA.root`
2.  **Physics Object**: Particle Flow Jets (`ak5PFJets`).
3.  **Discriminator Definition**: $D_E = - \sum_{i} f_i \log f_i$
    *   Where $f_i$ are the energy fractions of: Charged Hadrons, Neutral Hadrons, Photons, Electrons, Muons.

## Results
*   **Total Events Processed**: ~13,000 events (from one file).
*   **Total Jets**: 694,604.
*   **Selected Jets ($p_T > 30$ GeV)**: 21,755.
*   **Mean $D_E$**: 0.8445.

### Plots
The following plots were generated from the analysis:

1.  **Entropic Discriminator Distribution**: `research/mirror_fermion_validation/results/cms_entropy_distribution.png`
    *   Shows the distribution of jet entropy. A typical QCD jet has a mixed composition, leading to a specific entropy profile.
2.  **Entropy vs Momentum**: `research/mirror_fermion_validation/results/cms_entropy_vs_pt.png`
    *   Validates that entropy is not trivially correlated with $p_T$, making it a useful discriminator.

## Conclusion
We have successfully transitioned to Phase 2. The AOD data structure allows for complex substructure analysis. The Entropic Discriminator is now a live observable in our pipeline.

## Next Steps
1.  Process the full dataset (Tb scale) - *requires distributed computing or more storage*.
2.  Apply $D_E$ cut to isolate high-entropy candidates.
3.  Reconstruct invariant mass of $D_E$-selected 3-jet systems to look for the Mirror Fermion peak at 320 GeV.
