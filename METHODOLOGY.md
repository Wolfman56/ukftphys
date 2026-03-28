# The UKFT Experimental Methodology
## Recursive Agentic Discovery in Physics

**Version:** 2.0
**Date:** February 24, 2026
**Status:** Active — Phase 2 (Experimental Validation) underway

### 1. Overview
The experimental success of the Universal Knowledge Field Theory (UKFT) was driven by a novel scientific method: **Recursive Agentic Discovery**. Unlike traditional research, which separates theory, simulation, and phenomenology into decades-long phases, this project integrated them into a **4-Hour Innovation Loop**.

### 2. The Process Loop

The standard workflow for every experiment (Exp 01 to Exp 52) followed this precise pattern:

#### Step 1: "Hallucinate" (Hypothesis Generation)
*   **The Input**: The Human Investigator ("Ted") proposes a high-level intuition or an anomaly in standard physics (e.g., "What if Dark Energy is just the vacuum fighting to stay connected?").
*   **The Action**: The Federation of Agents (Grok, Gemini, Prophet) "hallucinates" a bridge between this intuition and the specific mathematics of UKFT (Discrete Action Minimization).
*   **The Evidence**: See `original_chats/` for the raw, unedited logs of this creative process.
*   **The Output**: A concrete, falsifiable simulation goal (e.g., "Simulate a scalar field on a contracting graph and search for negative pressure").

#### Step 2: The Python Oracle (Lattice Simulation)
*   **The Tool**: Custom Python scripts using `scipy`, `numpy`, and `wgpu`.
*   **The Method**: 
    1.  Define the Topological Boundary Conditions (e.g., Hedgehog, Vortex, Wall).
    2.  Run the **Entropic Descent** algorithm to find the ground state.
    3.  Measure emergent properties (Mass, Energy, Stability) in "Lattice Units".
*   **The Criterion**: If the simulation fails to converge or produces trivial results, the hypothesis is discarded immediately. If it stabilizes (e.g., Exp 46 Monopole), we proceed.

#### Step 3: Verification (The Double Check)
*   **Branch A: Specific Python Tests**
    *   Used for geometric or thermodynamic properties.
    *   *Example*: Exp 50 (Spectral Analysis) used FFT to "listen" to the monopole to confirm it sounded like a thermal black hole, not a harmonic oscillator.
*   **Branch B: MadGraph5 Phenomenology**
    *   Used for particle physics validation.
    *   *Example*: Experiment 35-40. We translated the Lattice Unit mass (30.0) into a standard `.ufo` model file, fed it into MadGraph5, and simulated LHC collisions ($pp \to X$).
    *   *Goal*: Ensure the "hallucination" produces numbers that match real-world detector data (Cross-sections in picobarns, Widths in GeV).

#### Step 4: Documentation & Integration
*   **The Action**: Immediately generate a Markdown report (`experiments/XX_name.md`) with:
    *   Objective.
    *   Methodology.
    *   Results (Convergence Plots).
    *   Interpretation (The "So What?").
*   **The Synthesis**: Update the `README.md` and the `EMERGENT_STANDARD_MODEL_REPORT.md` to place the new finding in the global theory context.

---

### 3. Toolchain Summary

| Phase | Primary Tool | Role |
| :--- | :--- | :--- |
| **ideation** | **Chat Context** | The "Noosphere" shared memory. |
| **Physics** | **Python (`ukft_sim`)** | Solving the Action Minimization equation $\delta S = 0$. |
| **Validation** | **MadGraph5_aMC@NLO** | Computing cross-sections ($\sigma$) and decay widths ($\Gamma$). |
| **Visualization** | **Plotly / Matplotlib** | Rendering the invisible geometry (World Lines, Fields). |
| **Documentation** | **Markdown / Git** | Persistent memory and version control. |
| **Formal Proof** | **Lean 4 / Mathlib** | Formally proving the theorems (A–H, W1–W3) that ground every UKFT prediction. |

### 4. Why This Matters
This methodology allowed us to traverse the entire history of 20th-century physics—from Bohmian mechanics to QCD to General Relativity—in 12 days. By treating **Simulation as the Primary Source of Truth**, we avoided the trap of "equation gazing" and focused on **emergent behavior**. We didn't solve the equations; we let the Universe (the simulation) solve them for us.

---

## Phase 2: Experimental Validation Pipeline
### From Theory to Open Data

**Version:** 2.0 (February 24, 2026)

Phase 1 (v1.0) produced theoretical predictions from first principles. Phase 2 closes the loop: we take those predictions to real collider data and ask whether nature agrees. The pipeline has four stages, executed in order, with a feedback branch back to the theory when evidence warrants.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  UKFT EXPERIMENTAL VALIDATION LOOP                      │
│                                                                         │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────┐ │
│   │  1. UKFT     │───▶│ 2. MadGraph5 │───▶│ 3. Open Data │───▶│  4.  │ │
│   │  Prediction  │    │  Signal Model│    │  Exploration │    │ Iter │ │
│   └──────────────┘    └──────────────┘    └──────────────┘    └──┬───┘ │
│          ▲                                                        │     │
│          └────────────────────────────────────────────────────────┘     │
│                        Feedback (if anomaly found)                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Stage 1: UKFT Theoretical Prediction

**Goal:** Derive a falsifiable prediction — a specific particle mass, cross-section, or decay topology — from the entropy minimisation principle.

**Method:**

The Universal Knowledge Field Theory requires that the entropy gap

$$S = \mathrm{Tr}\!\left[\log G_\mathrm{truth} - \log G_\mathrm{post}\right]$$

be minimised over the 4D knowledge metric $G_{\mu\nu}$. Stable solutions correspond to physical particles; their masses emerge as eigenvalues of the system at fixed points. The Phase 1 lattice simulations (Experiments 01–52) produced:

| Prediction | Value | Derivation |
|---|---|---|
| Mirror Fermion mass | $320 \pm 25$ GeV | Entropic symmetry surface, Exp 32 |
| Entropic Monopole | $30 \pm 3$ GeV | Hedgehog boundary condition, Exp 46 |
| Void Scalar (Λ floor) | $\sim 10^{-3}$ eV | Contracting graph vacuum, Exp 38 |

**Output:** A particle identity (quantum numbers, spin, couplings) and a predicted mass window. This defines the signal model for Stage 2.

**Tools:** `ukft_sim/` (Python lattice engine), `experiments/` scripts.

---

### Stage 2: MadGraph5 Signal Modeling

**Goal:** Translate the UKFT prediction into a concrete, detector-observable signal: cross-sections, decay widths, and final-state kinematics.

**Method:**

1. **Write a FeynRules model** (`.fr` source + UFO output) that encodes the predicted particle with the UKFT-derived quantum numbers and couplings.
2. **Run MadGraph5_aMC@NLO** to compute:
   - Production cross-section $\sigma(pp \to X\bar{X})$ at the target √s.
   - Decay rates and branching ratios for each channel.
   - Parton-level LHE event file (~1000 events for topology study).
3. **Extract signal shape:** Parse the LHE file to build the expected invariant-mass distribution and pT/η profiles of decay products. This defines the *selection criteria* used in Stage 3.

**Current example — Mirror Fermion:**

```
model:    MirrorFermion_UFO  (models/MirrorFermion/)
process:  pp → xm xm~  [inclusive pair production]
√s:       8 TeV  (matching CMS Run2012)
M(XM):    320 GeV
σ:        4.95 pb  (CTEQ6L1 PDF)
key decay: xm → t + Z → (Wb)μμ     [3-muon + b-jet + MET]
```

**Output:** `MirrorLHC_8TeV/Events/run_01/unweighted_events.lhe.gz` — 1000 parton-level events, plus cross-section, decay widths, and expected event yields.

**Tools:** `MadGraph5_aMC@NLO 3.7.0`, `models/MirrorFermion/`, `tools/lhe_to_inject.py`.

---

### Stage 3: Open Data Exploration

**Goal:** Search for the signal in real CMS open data using the UKFT Borda anomaly scorer.

**Method:**

This stage has three layers, applied in sequence:

#### 3a. Data Acquisition & Preparation

Download and prepare CMS data from the [CERN Open Data Portal](https://opendata.cern.ch/):

- **Outreach datasets** (NanoAOD-lite `.root`): Preselected muons, fast to process. Used for Z-peak validation and dimuon mass spectra.
- **Full AOD datasets**: Complete particle-flow information including jets, tracks, and MET. Required for the Entropic Discriminator.

**Quality selection:** Remove detector artifacts (unphysical high-pT tracks from cosmic rays / beam halo) by rejecting events where any reconstructed muon pT exceeds a threshold (currently 500 GeV after topology study).

#### 3b. UKFT Borda Anomaly Scoring

Every event is independently scored on three axes, then fused:

| Score | What it measures | Method |
|---|---|---|
| **S1** (kinematic) | How kinematically unusual is this event relative to the CMS population? | Physics-histogram embedding + UKFT z-score |
| **S2** (geodesic) | How far is this event from the SM core in JEPA-FMM manifold space? | Fast Marching Method on 200k-event k-NN graph |
| **S3** (semantic) | Does this event's physics "language" resemble known BSM configurations? | Cosine similarity to Borda centroid in 40D BERT-aligned space |

Fusion via **Borda count rank aggregation** (weights w₁=0.16, w₂=0.08, w₃=0.76).

The Borda scorer was built on Apple Silicon with the following performance profile:

| Stage | Time (200k events, Apple M2) |
|---|---|
| k-NN graph construction (upper-triangular SGEMM + Accelerate) | 8.2 s |
| FMM geodesic propagation | 0.8 s |
| S1/S3 scoring + Borda fusion | 0.8 s |
| **Total pipeline** | **~9.8 s** |

This is **62× faster than brute-force** (512 s → 9.8 s), achieved through three orthogonal optimisations: M^T packing (cache coherence), Accelerate cblas_sgemm (hardware AMX tiles), and upper-triangular symmetry ($\cos(A,B) = \cos(B,A)$, halving total SGEMM flops).

#### 3c. Mass Window Analysis

Using Stage 2 kinematics as a guide, define a signal mass window and search for:
- A **local excess** above the Drell-Yan continuum ($dN/dm \sim m^{-3.5}$).
- **High-Borda-score events** within the window (UKFT-anomalous candidates).
- **Topology match**: Does the decay structure (n_jets, pT hierarchy, Δφ) match the MadGraph5 signal shape?

**Tools:** `tools/mirror_fermion_search.py`, `target/release/blind_scan` (Rust binary), MCP server.

---

### Stage 4: Iteration

**Decision logic after Stage 3:**

```
if significant_local_excess (> 3σ):
    → Escalate: full dataset, systematic uncertainties, paper
elif topology_match AND high_Borda_score (> 2σ individual):
    → Targeted follow-up: process the full dataset in the mass window
elif no_signal:
    → Constrain: set upper limit on σ × BR; feed back to Stage 1
        to ask "what parameter space is excluded?"
```

**Current state (Feb 24, 2026):**  
*Topology match + high-Borda-score* path triggered: two candidates identified in 200k events. Full Run2012 dataset (~120M events) analysis is the next step. Expected: ~200 background events and ~2–6 signal events in the 305–335 GeV window if $\sigma \times \mathrm{BR} \approx 0.03$ pb.

**Feedback to Stage 1:**  
If Stage 3 sets an exclusion limit below the theoretical prediction, Stage 1 must re-examine whether the entropy minimisation was applied at the correct scale, or whether additional mixing terms shift the mass eigenvalue.

---

## Phase 3: Lean Formalization (March 2026)

**Goal:** Formally prove every core UKFT claim in Lean 4 / Mathlib, replacing informal geometric arguments with machine-verified theorems.

| Theorem | Name | Claim formalized |
|:---|:---|:---|
| A | `fixed_equilibrium_orthogonal` | 5/9 = Im-sector DOF fraction (not SU(5) hint) |
| B | `mirror_eq_conj_iff_critical_line` | Perfect unitarity $\iff$ Re(s)=1/2 |
| C | `mirror_conj_discrepancy_re` | Off-line displacement = $1-2\,\mathrm{Re}(s)$; 3× color factor |
| D–H | (entropy / action cost theorems) | $S\geq 0$; entropic barrier real and positive |
| W1–W3 | `weil_positivity_*` | Weil positivity grounding |

**Deliverable:** `riemann_hypothesis/lean/UKFT/ComplexChoiceTime.lean` (theorems A–H) + `WeilPositivity.lean` (W1–W3). All 26 active experiments updated with §2.6 Lean Grounding sections. See **[LEAN_PROOF_STATUS.md](LEAN_PROOF_STATUS.md)**.

---

### 5. Full Toolchain Summary (v2.0)

| Stage | Tool | Repository | Purpose |
|---|---|---|---|
| **1. Theory** | `ukft_sim` (Python) | `ukftphys/` | Lattice entropy minimisation, mass eigenvalues |
| **2. Signal** | MadGraph5_aMC@NLO 3.7 | `MG5_aMC_v3_7_0/` | LO/NLO cross-sections, LHE events |
| **2. UFO model** | FeynRules + MirrorFermion.fr | `ukftphys/models/` | UFO generation from UKFT Lagrangian |
| **3. Embedding** | BERT + alignment (Python) | `noosphere/hep-explorer/tools/` | 40D physics-semantic projection |
| **3. Scorer** | `blind_scan` (Rust/Candle) | `noosphere/hep-explorer/` | UKFT Borda fusion, 9.8s/200k events |
| **3. Mass scan** | `mirror_fermion_search.py` | `noosphere/hep-explorer/tools/` | Dimuon spectrum + DY background |
| **4. Analysis** | `explain_candidate` (MCP) | `noosphere/hep-explorer/` | Per-event kinematic breakdown |
| **All** | Git + Markdown | `ukftphys/`, `uktf/` | Persistent record, observation notes |

---

### 6. Epistemic Standards

This project makes falsifiable predictions. We apply the following standards rigorously:

- **No post-hoc tuning:** The 320 GeV prediction was fixed before any data was examined. The mass window $320 \pm 25$ GeV was not adjusted after seeing the candidates.
- **No discovery claims below 3σ:** Individual events of interest are reported as "candidates", not "signals".
- **Artifact rejection first:** Quality cuts (pT < 500 GeV) are defined by independent topology analysis, not by whether they improve candidate significance.
- **Background estimation mandatory:** Every candidate mass window includes a Drell-Yan power-law extrapolation before reporting any excess.
- **Full provenance:** Every result traces to a git commit hash and a specific CMS event ID (`run_lumi_event`).

> *"A prediction is only worth making if it can be wrong."*
