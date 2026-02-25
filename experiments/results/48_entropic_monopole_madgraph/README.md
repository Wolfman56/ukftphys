# Experiment 48: Entropic Monopole MadGraph Simulation

## Overview
This experiment simulates the **30 GeV Entropic Monopole** as a scalar resonance using **MadGraph5_aMC@NLO v3.7.0**. Ideally, the monopole is a topological defect, but for collider phenomenology, we model it as a scalar field ($H$) with effective couplings to gluons (via the heavy quark loop approximation in the **HEFT** model).

## Configuration
- **Model:** `heft` (Higgs Effective Field Theory)
- **Process:** `g g > h` (Gluon Fusion production of the scalar)
- **Mass ($M_H$):** 30.0 GeV (Derived from Lattice QCD findings in Exp 46)
- **Width:** Auto-calculated
- **Events Generated:** 10,000

## Results

### Cross-Section
- **Total Cross-Section:** `189.1 ± 0.1566 pb`
- **Integrated Luminosity Equivalent:** ~52.9 fb⁻¹ (for 10k events, though effective lum printed was 63.3 pb⁻¹ for unweighted generation efficiency)

### Decay Width & Branching Ratios
The total decay width was calculated to be **1.18 MeV** ($1.182490 \times 10^{-3}$ GeV).
Because the mass (30 GeV) is below the $W W$ / $Z Z$ threshold but above the $b \bar{b}$ threshold, the dominant decay modes are:

1.  **$H \to b \bar{b}$:** ~94.5% ($BR \approx 0.945$)
2.  **$H \to \tau^- \tau^+$:** ~5.1% ($BR \approx 0.051$)
3.  **$H \to g g$:** ~0.34% ($BR \approx 0.0034$)
4.  **$H \to \gamma \gamma$:** ~0.0075% ($BR \approx 7.5 \times 10^{-5}$)

### Event File
- **Format:** Les Houches Event (LHE)
- **Location:** `monopole_process/Events/run_01/unweighted_events.lhe.gz`

## Interpretation
A 30 GeV scalar resonance produced via gluon fusion with SM-like couplings would have a significant cross-section (189 pb) at LHC energies. The dominant signature would be a pair of b-jets. This low-mass region is challenging due to high QCD backgrounds, but the unique "entropic" nature might imply different jet structures or missing energy signatures if the monopole has hidden sector couplings (not modeled here).
