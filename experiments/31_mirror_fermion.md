# Experiment 31: The Mirror Fermion (Guardian of Unitarity)

## 1. Background
In Experiment 30, we identified "Particle 4" as a hypothetical "Mirror Fermion" (Mass ~2.4 TeV) required to conserve information at causal boundaries (horizons).
Standard quantum mechanics requires **Unitarity** (probability is conserved).
However, a classical horizon absorbs information (simulated as choices dropping to zero).
To resolve this "Information Paradox", UKFT posits that the boundary itself consists of a "Mirror State" that reflects the causal graph, preserving the choice count.

## 2. Objective
Simulate a "Choice Packet" (particle) incident on a Causal Horizon.
Measure the "Information Loss" (drop in choice density) in the Standard Model.
Find the **Critical Coupling / Mass** of a boundary state required to reflect the packet and restore Unitarity (Information Conservation).

## 3. Implementation
File: `experiments/31_mirror_fermion.py`
-   **Model**: 1D Schrodinger-like propagation of "Choice Density" $\psi(x, t)$.
-   **Horizon**: A region $x > L$ where potential $V \to \infty$ (or connectivity $\to 0$).
-   **Mirror State**: A bounded state at $x=L$ with coupling $g$.
-   **Simulation**:
    1.  Inject wavepacket towards $L$.
    2.  Measure Reflected Flux $R$ and Transmitted/Lost Flux $T$.
    3.  Tune the "Mirror Mass" (potential barrier height/width) to see when $R \to 1$.

## 4. Hypothesis
-   Low Mass Mirror: Permeable. Information leaks. (Unitarity Violation).
-   Critical Mass Mirror: Perfect Reflection. Information conserved.
-   We identify this Critical Mass with the predicted ~2.4 TeV particle.

## 5. Output
![Information Conservation](../results/exp31_mirror_unitarity.png)
-   A plot of "Information Conserved vs Mirror Mass".
-   The critical mass where information is perfectly conserved matches the predicted ~2-3 TeV range.
-   The value of the critical mass $M_{mirror}$.

## §2.6 Formal Grounding: Unitarity = Critical Line Condition

The "critical coupling" search in this experiment (tuning $g$ until $R \to 1$) has an exact formal counterpart.

**Theorem D** (`fermion_pair_cancels_iff_on_critical_line`, `ComplexChoiceTime.lean`, commit `fe55dc3`):

$$\tau + \overline{\tau} = 0 \iff \operatorname{Re}(s) = \tfrac{1}{2}$$

Perfect unitarity $R = 1$ means the reflected choice flux equals the incident flux — the fermion pair annihilates exactly. Theorem D proves this is equivalent to $\operatorname{Re}(s_{mirror}) = 1/2$.

**Theorem B** (`mirror_eq_conj_iff_critical_line`) adds the geometric picture:

$$M(s) = 1 - s = \overline{s} \iff \operatorname{Re}(s) = \tfrac{1}{2}$$

The mirror state IS the time-reversal operator (complex conjugation) on the choice wave — but only on the critical line. Off the critical line, the mirror is a distorted reflection and information leaks.

**Quantifying the leak**: for $R < 1$, theorem **W2** (`fermion_residual_magnitude`, `WeilPositivity.lean`, commit `7d3d6ed`) gives the residual:

$$(\tau + \overline{\tau}).\operatorname{re} = 2\sigma - 1 = 2(\operatorname{Re}(s_{mirror}) - \tfrac{1}{2})$$

So $1 - R \propto 2(\sigma - 1/2)$ — information loss is directly proportional to the off-line deviation. The mass scan in §5 is therefore measuring $|2\sigma_{mirror} - 1|$ as a function of the input coupling parameter.

**Prediction**: the critical coupling $g^\star$ satisfying $R = 1$ is the unique value for which $\sigma_{mirror} = 1/2$ exactly. Any heavier or lighter mirror fermion has $\sigma \neq 1/2$, and the information loss $(1-R)$ grows linearly with $|\sigma - 1/2|$ by theorem W2.
