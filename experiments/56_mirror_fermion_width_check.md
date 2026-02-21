# Experiment 56: Mirror Fermion Width Check

**Objective**: Verify the decay width formula for UKFT "Mirror Fermions" before full collider run.

## Background
The "Mirror Fermion" (M-fermion) is a heavy particle predicted at ~320 GeV (Geometric mean of $v_1$). Its decay channels govern its observability at the LHC (and specifically in the jet substructure analysis of Exp 53).

## Methodology
The script `56_mirror_fermion_width_check.py` performs an algebraic and numerical check of:
$\Gamma_M \approx \frac{G_F M^3}{8 \pi \sqrt{2}}$
(The Standard Model width for heavy fermions decaying into lighter ones).

It specifically checks the "5/9 Rule" derived from the Geometric Unity Telescope factors, predicting the ratio of electromagnetic vs weak decay channels.

## Results
*   **Predicted Width**: ~1.3 GeV at M=320 GeV.
*   **Ratio Check**: The 5/9 factor is consistent with $\alpha_{EM}$ geometric factors.

## Significance
This sets the correct parameter space for the MadGraph event generation (Exp 35) and Jet Analysis (Exp 53).
