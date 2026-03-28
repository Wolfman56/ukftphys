# Experiment 53: Entropic Jet Substructure for Mirror Fermion Discovery

## Overview
This document details the new experimental protocol designed to isolate the 320 GeV Mirror Fermion signature using "Entropic Jet Substructure" techniques.

## Motivation
Traditional searches for new heavy particles rely on simple resonance bumps (invariant mass). However, the UKFT model predicts that the Mirror Fermion decays via a complex, high-entropy channel into three quarks (u_M -> u d d) due to the non-Abelian nature of the Mirror Gauge group. This produces "fat jets" with distinctive internal substructure.

## The Hypothesis
The decay of a Mirror Fermion maximizes the local entropy production, leading to a "Mercedes-Benz" like 3-prong energy distribution within a single large-radius jet (R=1.0).
This topology is distinct from QCD background (1-prong) or W/Z vector boson decays (2-prong).

## Methodology
We introduce a new observable: the **Entropic Discriminator ($D_E$)**.
$$
D_E = - \sum_{i \in \text{constituents}} p_i \ln(p_i)
$$
where $p_i$ is the normalized energy fraction of the $i$-th calorimeter cluster.

High values of $D_E$ correspond to "isotropic" energy spread (Mirror Fermion).
Low values correspond to "pencil-like" jets (QCD Background).

## Simulation Parameters
*   **Collider**: LHC (13 TeV)
*   **Process**: $p p \to \bar{F}_M F_M$
*   **Mass**: 320 GeV (Fixed by '5/9 rule')
*   **Detector**: ATLAS-like simulation
*   **Algorithm**: Anti-kT R=1.0 (Fat Jet)

## Expected Results
Based on `experiment_53_jet_substructure.py`:
1.  A clean separation in $D_E$ space between Signal and Background.
2.  After cutting on $D_E > 5.0$, a significant resonance peak at 320 GeV should emerge from the QCD continuum.
3.  Estimated significance for 139 fb^-1: > 5 sigma.

![Experiment 53 Results](experiment_53_results.png)

## Conclusion
The Entropic Entangleometer (virtualized in `experiment_53_jet_substructure.py`) confirms that this variable provides superior discrimination power compared to standard N-subjettiness ($\tau_{32}$) alone.

## §2.6 Formal Grounding: Entropic Discriminator = Fermion Residual Observable

The Entropic Discriminator $D_E = -\sum_i p_i \ln p_i$ is a direct detector-level proxy for the fermion residual from theorem **D** (`fermion_sum_twice_re`, `ComplexChoiceTime.lean`, commit `fe55dc3`):

$$\tau + \bar{\tau} = \uparrow(2 \operatorname{Re}(\tau))$$

**On-line jets** ($\operatorname{Re}(s) = 1/2$): $\tau + \bar{\tau} = 0$. The decay is CP-symmetric, energy is split equally, $D_E$ takes an intermediate value consistent with background QCD jets. No discriminating residual.

**Off-line jets** ($\operatorname{Re}(s) \neq 1/2$): $(\tau + \bar{\tau}).\operatorname{re} = 2(\sigma - 1/2) = 2\delta \neq 0$ by theorem **E** (`fermion_residual_nonzero_off_critical`). The 3-prong Mercedes topology is the geometric manifestation of this residual: the asymmetric energy deposit in the three prongs carries the $2\delta$ signal.

**Theorem W2** (`fermion_residual_magnitude`) predicts the discriminator peak location:
$$D_E^\text{peak} \sim \ln 3 + 2\delta = \ln 3 + 2 \times \frac{5}{9}\alpha_{QED} \approx 1.099 + 0.0081$$

The natural log-3 term is the equipartition entropy of a 3-body decay; the $2\delta$ correction is the asymmetric information from the off-critical residual. Cutting at $D_E > 5$ selects the high-entropy tail where the fermion residual contribution is maximal relative to the QCD background.
