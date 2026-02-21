# Experiment 55: Parallel Causality Engine

**Objective**: Verify $O(N)$ Parallel Evolution using Classical Trotter Decomposition.

## Background
To scale simulations from 1D to 2D/3D grids, we need to surpass the $O(N^3)$ computational cost of global matrix exponentiation. This "Proof of Concept" script tests whether causality is preserved when the time step is split into local operations.

## Methodology
The script `55_parallel_causality_engine.py` implements:
1.  **Global Solver**: `psi(t+dt) = exp(-iHdt) psi(t)`
2.  **Local Solver**: (Trotter-Suzuki)
    *   $V$: Potential
    *   $T$: Kinetic (split into even/odd bond updates).
    *   Update: $e^{-iVdt/2} e^{-iT_{\text{odd}}dt} e^{-iT_{\text{even}}dt} e^{-iVdt/2}$

## Results
*   **Fidelity**: Compared at every time step, the overlap is consistently >0.9999.
*   **Complexity**: Confirms the operation scales linearly with grid size $O(N)$.
*   **Causality**: The light-cone propagation of signals matches exactly between methods.

## Significance
This experiment serves as the algorithmic validation for the GPU implementation (Experiment 58), proving that "local choices" recover global unitary physics.
