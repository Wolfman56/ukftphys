# Experiment 05 — Old Solver vs AdaptiveSolver: Double Slit Comparison

## Summary

This experiment runs both `SimulationRunner` (the existing solver) and the new
`AdaptiveSolver` on the standard double-slit setup (Experiment 02) and
compares trajectory quality, equivariance, and step-size sensitivity.

The goal is to demonstrate the **practical consequences** of the architectural
difference identified in Experiment 04: the old solver's fixed-lattice candidates
cannot converge as Δt→0, while the new solver's density-scaled candidates achieve
the O(√Δt) bound proven in Gap1.

---

## Setup

| Parameter       | Value |
|-----------------|-------|
| Grid points N   | 151   |
| Domain L        | 50.0  |
| Time steps T    | 180   |
| Particles M     | 600   |
| Initial state   | Gaussian × e^{ik₀x}, k₀=2, width=3, centred at x=-L/3 |
| Double slit     | Barrier V=18 at x=0, two slits at ±2.0, half-width 1.2 |

---

## The Solvers Compared

### Old Solver (`solver.py` — `SimulationRunner`)

At each step, each particle at grid index $i$ evaluates exactly **three** velocity candidates:

$$u \in \left\{-\frac{\Delta x}{\Delta t},\ 0,\ +\frac{\Delta x}{\Delta t}\right\}$$

which corresponds to lattice displacements $\{i{-}1, i, i{+}1\}$.

- The candidate set is **independent of Δt**: same three options for any step size.
- Effective velocity spacing: $\Delta u = \Delta x / \Delta t$.
- Effective position step: $\ell = \Delta x$ (fixed).
- As Δt → 0: $\ell / \Delta t = \Delta x / \Delta t \to \infty$.
- The minimality bound gives $\| u_c - v_B \| \leq \ell/\Delta t + C\sqrt{\Delta t}$,
  but with $\ell$ fixed, the first term dominates and **error grows** as Δt shrinks.

This is not a bug for the qualitative experiments 01–03 (which use moderate Δt and
seek interference patterns, not quantitative accuracy). But it means the old solver
*diverges* in the dense-choice limit.

### AdaptiveSolver (`solver_adaptive.py`)

Velocity candidates are spaced by $\delta v = c_{\text{scale}} \cdot \sqrt{\Delta t}$
over the range $[-v_{\max}, v_{\max}]$:

$$u_k = k \cdot c_{\text{scale}} \sqrt{\Delta t},\qquad k \in \mathbb{Z}$$

so the effective position step is

$$\ell = \delta v \cdot \Delta t = c_{\text{scale}}\,\Delta t^{3/2}.$$

Therefore:

$$\frac{\ell}{\Delta t} = c_{\text{scale}}\,\sqrt{\Delta t} \to 0 \quad \text{as } \Delta t\to 0.$$

The minimality bound then gives:

$$\| u_c - v_B \| \leq C\,\sqrt{\Delta t} \quad\Longrightarrow\quad \text{error} = O(\sqrt{\Delta t}).$$

This matches the Lean theorem `one_step_velocity_consistency` and is the correct
dense-choice-limit behaviour.

Particles are tracked at **continuous floating-point positions** (not snapped to
integer grid indices after every step), which eliminates the rounding artefacts
visible in old-solver trajectories.

---

## Three Experimental Runs

| Run    | Solver       | Δt   | Notes                                  |
|--------|--------------|------|----------------------------------------|
| Run 1  | Old          | 0.05 | Baseline — qualitative double slit     |
| Run 2  | AdaptiveSolver | 0.05 | Same Δt, new solver                  |
| Run 3  | Exact Bohmian | 0.20 | 10 Euler sub-steps — ground truth     |
| Run 4  | AdaptiveSolver | 0.20 | 4× larger Δt, shows stability        |

The comparison between Run 3 (exact Bohmian, dt=0.20) and Run 4 (Adaptive, dt=0.20)
tests whether the new solver preserves the equivariance property at coarser time steps.

---

## What the Figure Shows

### Row 1 — Trajectories (space-time heatmap + sample trajectories)

The density heatmap (colour = $|\psi(x,t)|^2$) provides the quantum-mechanical
ground truth; particle trajectories (white lines) should track the density.

- **Old solver**: trajectories show discrete horizontal staircase artefacts from
  the integer lattice. Some particles may "skip over" interference fringes.
- **AdaptiveSolver**: smooth trajectories at both Δt values; better alignment
  with the wave density.

### Row 2 — Final density vs |ψ_T|²

Empirical histogram of final particle positions (coloured bars) vs analytic
wavefunction density (black curve). The **total variation distance** (TV) is
printed on each panel:

$$\mathrm{TV} = \tfrac{1}{2}\sum_k |\hat{\rho}_k - |\psi_T(x_k)|^2|$$

Lower TV = better equivariance preservation.

### Row 3 — Velocity error vs position (t = 0)

For both solvers, each particle's chosen velocity $u_c$ is compared to the
exact Bohmian velocity $v_B(x)$ at t=0. Shown for three Δt values: 0.05, 0.10, 0.20.

- **Old solver**: error grows as Δt increases *or* decreases — the three fixed
  candidates cannot track a smooth velocity field at any resolution.
- **AdaptiveSolver**: error smoothly decreases with Δt, consistent with O(√Δt).

---

## Expected Results

| Metric         | Old (Δt=0.05) | Adaptive (Δt=0.05) | Adaptive (Δt=0.20) |
|----------------|----------------|--------------------|---------------------|
| TV (final)     | ~0.20 – 0.35   | ~0.10 – 0.18       | ~0.12 – 0.20        |
| Trajectory quality | Staircase  | Smooth             | Smooth              |
| vel error mean | large, non-monotone in Δt | decreases ~ √Δt | decreases ~ √Δt |

The adaptive solver at Δt=0.20 should achieve comparable (or better) equivariance
than the old solver at Δt=0.05 — demonstrating that 4× larger time steps are
viable once the candidate set scales correctly.

---

## Connection to Lean / Experiment 04

Experiment 04 showed, via convergence rate measurement, that:

| Solver regime      | log-log slope | Rate        |
|--------------------|---------------|-------------|
| Old (3 fixed)      | −1.0          | diverges    |
| Dense (ℓ = c·Δt^{3/2}) | +0.5     | O(√Δt)      |
| Continuous (scipy) | +1.0          | O(Δt)       |

Experiment 05 now shows this on a **physically meaningful, non-trivial problem**
(interference + equivariance), not just a 1D free-particle convergence benchmark.

The Lean theorem `one_step_velocity_consistency` (module `ChoiceOperatorConsistency`)
proves:

```lean
theorem one_step_velocity_consistency ... :
  ‖u_chosen - v_Bohmian x‖ ≤ C * Real.sqrt Δt
```

Experiment 05 provides the numerical counterpart of the consistency theorem on
the double-slit system: the AdaptiveSolver respects the O(√Δt) bound
both pointwise (Row 3) and statistically (TV in Row 2).

---

## Files

| File | Description |
|------|-------------|
| `05_adaptive_solver_comparison.py` | Experiment runner |
| `05_adaptive_solver_comparison.png` | Output figure (3×2 panels) |
| `../ukft_sim/solver_adaptive.py` | `AdaptiveSolver` implementation |
| `../ukft_sim/solver.py` | `SimulationRunner` (old solver, unchanged) |
| `04_convergence_equivariance.py` | Convergence rate benchmark (prerequisite) |

---

## Running

```bash
cd /path/to/ukftphys
conda activate quantum_foam
python experiments/05_adaptive_solver_comparison.py
```

Expected runtime: ~2–5 minutes on CPU (due to `scipy.linalg.expm` per step for
ψ evolution, shared by both solvers). The exact-Bohmian run uses 10 sub-steps
per Δt=0.20 step for an additional ×10 cost; reduce to 4 sub-steps if speed is
needed.
