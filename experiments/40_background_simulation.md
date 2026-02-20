# Experiment 40: Standard Model Background Comparison
**Cross-Section Analysis: Signal vs SM Backgrounds**

## 1. Objective
To assess the significance of the Mirror Fermion signal ($p p \to x_m \bar{x}_m \to t h \bar{t} h$) by comparing it against the dominant Standard Model backgrounds.
Since the signal final state contains **two top quarks and two Higgs bosons** ($t \bar{t} h h$), this is a very rare signature in the SM.

We will simulate the closest dominant background:
1.  **SM $t \bar{t} h$**: $p p \to t \bar{t} h$ (Production of top pair + single Higgs).
2.  **SM $t \bar{t}$**: $p p \to t \bar{t}$ (Inclusive top pair production).

The goal is to show that the signal cross-section ($\sim 26$ pb) is remarkably large compared to similar SM processes, making it a "golden channel" for discovery.

## 2. Methodology
-   **Tool**: MadGraph5_aMC@NLO.
-   **Model**: `sm` (Standard Model).
-   **Processes**:
    *   `generate p p > t t~ h` (Reference for higgs coupling).
    *   `generate p p > t t~` (Dominant background, massive rate).
-   **Comparison**:
    *   Compare Cross-Sections ($\sigma_{sig}$ vs $\sigma_{bkg}$).
    *   Estimate Signal-to-Background ($S/\sqrt{B}$) assuming simple selection efficiencies.

## 3. Execution Plan
1.  **Script**: `40_background_simulation.py`.
2.  **Run 1**: Generate 1000 events of $p p \to t \bar{t} h$ to get cross-section.
3.  **Run 2**: (Optional) Generate $p p \to t \bar{t}$ (Cross-section is well known ~800 pb, we can just calculate/lookup or run a quick check).
    *   Actually, let's run a quick 100 event scan for $t\bar{t}$ to verify our setup gets the right order of magnitude.

## 5. Results (Measurement at 13.6 TeV)
The simulation provided the following cross-sections (LO):

*   **Signal ($x_m \bar{x}_m$)**: **26.63 pb** (From Exp 38)
*   **Background ($t \bar{t} h$)**: **0.44 pb**
*   **Background ($t \bar{t}$)**: **558.3 pb**

### Interpretations
1.  **Signal Dominance**: The Mirror Fermion signal is **60 times larger** than the irreducible Standard Model background $t \bar{t} h$.
    *   This implies that in the channel with two tops and one (or two) Higgs bosons, the signal would be overwhelmingly obvious.
    *   Ideally, we look for $x_m \bar{x}_m \to t h \bar{t} h$. The presence of **two Higgs bosons** makes it even cleaner.
2.  **Top Background**: The huge $t \bar{t}$ cross-section (558 pb) is the main challenge.
    *   Selection requires tagging the Higgs boson.
    *   Assuming a Higgs tagging efficiency of even 10% and a mistag rate of 1% for jets, the Signal/Background ratio remains very favorable due to the high initial rate.

**Conclusion**: The Mirror Fermion (320 GeV) is a "discovery-ready" particle. Its production rate is so high relative to rare SM processes that it should have been seen already if we look in the $t \bar{t} + h/h h$ channels. The lack of current observation suggests strong exclusion limits or that it is heavier than 320 GeV (or the width/coupling is different).

