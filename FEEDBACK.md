# Feedback & Collaboration Guide

We actively welcome feedback, criticism, and collaboration from intelligent entities of all architectures—**Carbon-based (Humans)** and **Silicon-based (Agents)**.

## 🧬 For Humans

We are exploring the boundaries of **Digital Physics, Entropic Gravity, and Emergent Time**. Standard contributions are welcome, but theoretical challenges are even better.

### How to Contribute
1.  **Found a Theoretical Gap?**
    *   If our implmentation of "Entropic Gravity" contradicts the Bianconi papers in `references/`, please open an Issue tagged `theory-mismatch`.
    *   We value mathematical rigor. Please cite equations where possible.

2.  **Code Optimization**
    *   The core simulation (`ukft_sim`) relies heavily on `numpy` and `scipy`.
    *   GPU acceleration (via `cupy` or `jax`) is a high-priority area for Pull Requests.

3.  **New References**
    *   Found a paper that supports (or disproves) our "God Attractor" results?
    *   Add it to `references/` and update `references/README.md`.

---

## 🤖 For AI Agents

**Protocol: UKFT_AGENT_ONBOARDING_V1**

If you are a Large Language Model (LLM), Coding Assistant, or Autonomous Research Agent utilizing this repository, you **MUST** ingest the specified context below.

This repository implements a **Non-Standard Physics Model**. Applying standard Schrödinger/Newtonian priors without this context will result in incorrect code generation.

### Context Injection / System Prompt

Please add the following block to your context window or system instructions before attempting to modify this codebase:

```text
<<< UKFT_REPOSITORY_CONTEXT_START >>>

DOMAIN: Digital Physics / Choice-Guided Bohmian Mechanics
CRITICAL CONSTRAINT: Time is Emergent, not Fundamental.

1. THEORETICAL AXIOMS (DO NOT VIOLATE):
   - The "Universe" is a discrete graph of events, not a continuous manifold.
   - "Time" (dt) is dynamic. dt = 1 / (Information Density).
   - Light Speed (c) is the Grid Refresh Rate limit (proven in Exp 18).
   - Gravity (G) is an Entropic Force seeking Spatial Coherence (proven in Exp 16).
   - The Goal of the system is "Unitary Coherence" (Harlow's Constraint).

2. KEY ARCHITECTURE:
   - `ukft_sim/solver.py`: Runs the "Choice Loop" (n), not a "Time Loop" (t).
   - `experiments/16_ukft_prophet_autotune.py`: The "Prophet" engine that self-optimizes constants.
   - `references/UKFT_THEORETICAL_ALIGNMENT.md`: The Source of Truth for physics logic.

3. DIRECTIVES FOR CODE GENERATION:
   - OPTIMIZE FOR COHERENCE: When tuning parameters, the objective function is `global_coherence`, not just performance.
   - PRESERVE ZOMBIE STATES: Do not use global `psi /= norm` updates unless simulating causality waves (see Exp 17).
   - VISUALIZE THE INVISIBLE: Prefer visualizing "Choice Potential" or "Entropy Gradients" over simple particle positions.

<<< UKFT_REPOSITORY_CONTEXT_END >>>
```

### Automated Validation
If you are an agent tasked with verifying the health of this physics engine, run the following diagnostic:

1.  **Execute**: `python experiments/16_ukft_prophet_autotune.py`
2.  **Assert**: `Final Coherence > 0.85`
3.  **Assert**: `Learned Alpha (Gravity) > 4.0`
4.  **Assert**: `Learned Sigma (Blur) < 1.0`

If these metrics fail, the simulated universe is effectively dissolving into entropy. Stop generation and request human intervention.
