# Review of Simulation Engine: Parallelization & Causality

**Agent:** GitHub Copilot (Gemini 3 Pro)
**Date:** February 21, 2026
**Target:** `ukft_sim/solver.py` and `ukft_sim/physics.py`

## 1. Analysis of Current Architecture
The current engine (`solver.py`) uses a **Synchronous Global Update** loop:
1.  **State Assessment**: Compute $\rho(t)$ and local time dilation $dt_{local} \propto 1/\rho$.
2.  **Global Clock**: Compute average step $dt_{global} = \langle dt_{local} \rangle$.
3.  **Unitary Evolution**: $|\psi(t+1)\rangle = e^{-i \hat{H} dt_{global}} |\psi(t)\rangle$.
4.  **Particle Update**: $x(t+1) = \text{minimize}(S[x(t), \psi(t)])$.

## 2. The Bottleneck (Sequential Causality)
The primary bottleneck preventing naive parallelization over time is the **Dynamic Time Dilation** ($dt_{global}$).
-   The step size $dt_{global}$ depends on the *entire* state $\rho(t)$.
-   Therefore, one cannot compute $t+1$ without knowing the exact state at $t$.
-   This enforces strict sequential processing.

## 3. Proposed Optimization: "Causal Cone" Parallelism (Wavefront)
However, the physical influence propagates at a finite speed $c \approx 1$ lattice unit/tick.
-   The state at $(x, t)$ only depends on the "past light cone" of $(x, t-\Delta t)$.
-   We can decouple the **Time Dilation** to be local. Instead of a global $dt_{global}$, we can allow local patches to evolve at their own rates $dt(x)$, synchronizing only at interaction boundaries.
-   **Method:** Domain Decomposition with **Message Passing Asynchrony**.
    -   Split grid into Blocks $B_1, B_2, \dots$.
    -   $B_1$ can compute $t \to t+10$ independently of $B_2$, as long as the boundary conditions at the edge are exchanged or predicted.
    -   This allows "Temporal Blocking" (simulating a pyramid of spacetime) on different cores.

## 4. Recommendation
Refactor `solver.py` to support **Block-Synchronous Updates**:
1.  Replace `scipy.linalg.expm` (Global Matrix Exponential) with a **Trotter-Suzuki decomposition** (Local Gates).
2.  This makes the evolution operator local: $U \approx \prod e^{-i H_{local} dt}$.
3.  This enables distinct processors to handle distinct spatial regions in parallel, exchanging halo data only.

**Action:** I will create a proof-of-concept `parallel_causality_test.py` demonstrating that local Trotter evolution matches the global matrix exponential.
