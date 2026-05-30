# Copilot Instructions — ukftphys

This is **ukftphys**, the physics simulation and collider validation application of the grok/nooverse ecosystem. It applies UKFT (Unified Knowledge Field Theory) to experimental particle physics via Python lattice simulation, MadGraph5 phenomenology, and Lean 4 formal proofs.

For full context, read `agent_baton.md` and `copilot_feedback_baton.md` in this repo.

## Architecture Position

Four-layer system: Foundation → Interface → Application → **Product/App layer**.

**This repo's position**: App layer. ukftphys is the public face of UKFT physics work — a standalone research application that consumes UKFT theory from `uktf` and publishes validated results. It is the domain application driving HEP (High-Energy Physics) validation.

**Workspace reading order** (mandatory): `uktf` (theory oracle) → `nooverse` (architecture truth) → **ukftphys** (this repo — physics domain).

## The Iterative Discovery Loop

Every experiment follows the Phase 3+ loop:

```
Hypothesis → Experiment → Formal Proof → Refined Hypothesis
     ↑                                           │
     └───────────── theorems filter ─────────────┘
```

1. **Hypothesize** — falsifiable prediction grounded in UKFT axioms
2. **Experiment** — Python lattice sim (`ukft_sim/`) or MadGraph5 cross-section
3. **Formalize** — Lean 4 proof (zero `sorry`) in `ukft_riemann_hypothesis/` or `lean-publish/`
4. **Refine** — proved theorems (A–H, W1–W3) constrain the next hypothesis

## Key Validated Predictions

| Prediction | Status | Evidence |
|---|---|---|
| Mirror Fermion at ~320 GeV | **3.3σ signal confirmed** (331.5 GeV, CMS 7-muon run 202016) | UKFT-35, Exps 22–36 |
| DM/baryon ratio = 5 (jump-prime cardinality) | Planck 2018: 5.36 (within 7%) | UKFT-44, Exp 88 |
| Re(s_mirror) = 0.50406 ± 0.00003 | 4 independent observables agree | Exps 37, 41, 79, 80 |

## Repository Layout

| Path | Purpose |
|------|---------|
| `ukft_sim/` | Core Python physics engine — **Red Zone, do not modify without confirmation** |
| `experiments/` | 100+ numbered experiment scripts and results — **Red Zone** |
| `papers/` | Publications and theory documents — **Red Zone** |
| `feedback/` | Agent session logs and exploratory work — **Green Zone** |
| `models/` | MadGraph5 UFO model files |
| `results/` | Simulation output plots and data |
| `METHODOLOGY.md` | Full Recursive Agentic Discovery methodology |
| `agent_baton.md` | Current phase and mission — read first |
| `LEAN_PROOF_STATUS.md` | 11 formally proved theorems (A–H, W1–W3) |
| `EMERGENT_STANDARD_MODEL_REPORT.md` | Synthesis of all validated predictions |

## Toolchain

| Phase | Tool | Role |
|-------|------|------|
| Physics simulation | Python (`ukft_sim/`) + `scipy`, `numpy`, `wgpu` | Entropic descent, lattice simulation |
| Collider validation | MadGraph5_aMC@NLO | Cross-sections (σ), decay widths (Γ) |
| Formal proof | Lean 4 / Mathlib (in `ukft_riemann_hypothesis/`) | Zero-sorry theorem proving |
| Visualization | Plotly / Matplotlib | Field geometry, world lines |
| Environment | `conda` — see `environment.yaml` | Python dependencies |

## Current Phase

**Phase 4 (Collider Validation)** — active on branch `phase-three-dilation`.
- Phase 3 (Lean Formalization) complete: all 11 theorems (A–H, W1–W3) proved with zero `sorry`
- Phase 4: systematic Mirror Fermion search in CMS Run 2 dataset (~120M events, 305–335 GeV window)
- Latest: Experiment 109 (entangled light topology integrator)

## Code Style

- **Python-first** (exception to ecosystem Rust-first rule): ukftphys is a physics research app — all simulation code is Python
- **Script discipline**: Every script must determine its own directory for outputs:
  ```python
  import os
  SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
  plt.savefig(os.path.join(SCRIPT_DIR, 'my_plot.png'))
  ```
- **Experiment format**: Every new experiment needs a corresponding `explainer.md` following `experiments/README.md` template
- **Lean proofs**: All Lean 4 work goes in `ukft_riemann_hypothesis/` or `lean-publish/` — NOT in this repo

## Session Protocol (Green Zone / Red Zone)

- **Green Zone** (free to create/edit/delete): `feedback/Copilot_[Model]_[Timestamp]/`
- **Red Zone** (requires explicit user confirmation before modifying):
  - `ukft_sim/` — core physics engine
  - `experiments/` — historical data
  - `papers/` — publications
- Create a session log at `feedback/Copilot_[Model]_[Date]/feedback_summary.md` on start

## Terminology

- **Mirror Fermion** — UKFT-predicted particle at ~320 GeV restoring unitarity at causal horizons
- **Void Scalar** — Dark Energy as vacuum choice floor pressure (~10⁻¹²⁰)
- **Entropic descent** — the simulation algorithm minimizing δS = 0
- **Jump primes** — {2, 5, 11, 17, 37, 67, 131, 257, 521, 1031} — DAG topology boundaries
- **δ-triangle** — Re(s_mirror) = 1/2 + δ, δ = (5/9)α_QED ≈ 0.00406
- **Recursive Agentic Discovery** — the 4-step Hypothesis→Experiment→Prove→Refine loop

## What NOT to Do

- Do not write Lean 4 source files in this repo — use `ukft_riemann_hypothesis/` or `lean-publish/`
- Do not modify Red Zone files without explicit confirmation
- Do not save script outputs relative to CWD — always use `SCRIPT_DIR`
- Do not propose new experiments that contradict proved theorems A–H or W1–W3
