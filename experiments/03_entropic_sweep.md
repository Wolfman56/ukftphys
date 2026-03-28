# Experiment 03a: Entropic Parameter Sweep

## Objective
To visualize the effect of the **Entropic Gravity Parameter ($\alpha$)** on particle trajectories.
*   **Hypothesis**: Increasing $\alpha$ biases choices towards regions of higher Knowledge Density (Network Entropy), effectively "sharpening" reality and suppressing low-probability outlier paths.

## Comparative Analysis

### Control: $\alpha = 0.0$ (Standard Bohmian)
Particles act passively. They surf the quantum potential but explore the full width of the wave packet, including low-density tails.
![Alpha 0.0 Trajectories](03_sweep_alpha_0.0_fig2.png)

### Hybrid: $\alpha = 5.0$ (Biased Choice)
Trajectories begin to cluster. The "fuzziness" of the quantum probability cloud starts to resolve into structured "veins" of high probability.
![Alpha 5.0 Trajectories](03_sweep_alpha_5.0_fig2.png)

### Strong Choice: $\alpha = 15.0$ (Reality Sharpening)
**The Collapse of Probability.** Trajectories rigidly adhere to the density maxima. The particle "refuses" to exist in low-information regions. This represents the transition from Quantum Potentiality to Classical Actuality via high-frequency choice.
![Alpha 15.0 Trajectories](03_sweep_alpha_15.0_fig2.png)

## Interactive Results
[Alpha 0.0 Simulation](../results/03_sweep_alpha_0.0.html)
[Alpha 5.0 Simulation](../results/03_sweep_alpha_5.0.html)
[Alpha 15.0 Simulation](../results/03_sweep_alpha_15.0.html)

## §2.6 Formal Note

The α parameter is the entropic gravity coefficient weighting the density bonus against the kinetic cost. Theorem **G** (`realActionCostCoeff_zero_iff`, `ComplexChoiceTime.lean`, commit `fe55dc3`) formalizes the kinetic cost factor as $\operatorname{Re}(\Delta t)$:

$$\mathrm{cost}(u) = \operatorname{Re}(\Delta t) \cdot \|u - v^{\psi}\|^2$$

The α → 0 regime (standard Bohmian) corresponds to $\operatorname{Re}(\Delta t)$ dominating — kinetic cost is the only constraint, and trajectories explore the full probability cloud. The α → ∞ regime corresponds to the entropic bonus overwhelming the kinetic term, formally equivalent to $\operatorname{Re}(\Delta t) \to 0$: the system sits on the *zero manifold* $\{\operatorname{Re}(dt) = 0\}$.

Theorem **A** (`fixed_equilibrium_orthogonal`) proves that this zero manifold and the prime manifold $\{\operatorname{Im}(dt) = 0\}$ intersect only at $dt = 0$. Reality sharpening is therefore the formal approach to the zero-manifold equilibrium — the unique point where entropy cost and kinetic cost simultaneously vanish.
