# Entropic Scattering Hypothesis & Validation Test

## 1. Theoretical Motivation

### Standard Model (Hard Scattering)
In standard Quantum Field Theory (QFT), interactions at the LHC are modeled as **point-like** collisions between partons (quarks/gluons).
*   **Mechanism**: $q\bar{q} \to Z$.
*   **Signature**: High momentum transfer ($Q^2$) results in "hard" radiation. The outgoing energy is highly collimated into **jets** (narrow cones of hadrons).
*   **Information Topology**: Information is localized. The entropy of the final state momentum distribution is low because the momentum vectors are aligned.

### UKFT (Holographic Scattering)
In the Topological/Holographic dual description (UKFT), particles are not points but **extended solitons** or "clouds" of information on the spacetime boundary.
*   **Mechanism**: The scattering is a "diffractive" process where the incoming wavepackets excite the bulk geometry.
*   **Signature**: The interaction "rings" the spacetime fabric. Instead of a single hard kick (jet), the energy is dissipated into many soft, incoherent quanta.
*   **Information Topology**: Information is delocalized. The final state momentum vectors are more isotropic (spread out).

## 2. The Entropic Discriminator ($D_E$)

To distinguish these two regimes, we define the **Entropic Discriminator** (Shannon Entropy):

$$ D_E = -\sum_{i} x_i \ln(x_i) $$

Where $x_i$ is the normalized energy fraction of the $i$-th particle in the recoil system ($E_i / E_{\text{total}}$).

*   **$D_E \to 0$ (Low Entropy)**: All energy is carried by one or two particles (QCD Jets).
*   **$D_E \to \text{Max}$ (High Entropy)**: Energy is shared equally among $N$ particles (Thermal/Holographic state).

## 3. The Validation Test: $Z \to \mu\mu$ Recoil

We use the **CMS DoubleMuon** dataset (Run 1) as our laboratory.

### Why this channel?
1.  **Clean Tag**: The $Z$ boson decays into two muons ($\mu^+\mu^-$), which are easy to trigger on and reconstruct.
2.  **Vertex Localization**: The muons tell us exactly *where* and *when* the hard interaction occurred.
3.  **The Recoil**: The $Z$ boson usually has some transverse momentum ($p_T(Z)$). By conservation of momentum, the rest of the event (the "recoil") must balance this $p_T$.

### The Prediction
We analyze the **Recoil System** (all tracks excluding the two muons).

*   **Null Hypothesis (Standard Model)**: The recoil balances the $Z$ via a focused QCD jet (a quark or gluon).
    *   *Expectation*: The recoil tracks are clustered. **Low $D_E$.**
*   **Alternative Hypothesis (UKFT)**: A fraction of $Z$ bosons are produced via holographic "bulk" interactions.
    *   *Expectation*: The recoil is a "puff" of soft, incoherent radiation. **High $D_E$.**

### Methodology
1.  Select events with exactly two opposite-sign muons with $80 < M_{\mu\mu} < 100$ GeV (Z-peak).
2.  Veto additional reconstructed leptons.
3.  Collect all other "Energy Flow" objects (tracks/towers) in the event.
4.  Compute $D_E$ for this recoil system.
5.  **Plot $D_E$ distribution**: Look for a "shoulder" or excess at high entropy values that is not predicted by standard QCD Monte Carlo.

## 4. Analysis Implementation

The analysis script is located at:
`research/mirror_fermion_validation/analysis/check_mirror_fermion_hypothesis.py`

It performs the following steps:
1.  Loads `cms_doublemuon_full.root` using `uproot`.
2.  Applies the dimuon selection ($p_T > 25$ GeV, $|\eta| < 2.4$, opposite charge).
3.  Reconstructs the recoil system from remaining charged tracks.
4.  Calculates $D_E$ for each valid event.
5.  Outputs a histogram `cms_entropic_discriminator.png`.
