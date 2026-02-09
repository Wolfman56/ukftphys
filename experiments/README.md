# UKFT Experiments

This directory contains specific experimental setups designed to test the **Choice-Guided Bohmian Mechanics** hypothesis.

## Experiment List

### [01_free_particle.py](./01_free_particle.py)
**Objective**: Baseline Regression Test.
*   **Setup**: A Gaussian wave packet initialized in empty space with constant velocity.
*   **Physics Checked**: 
    - Ensures the discrete propagator (`scipy.linalg.expm`) correctly evolves the wavefunction.
    - Verifies that particle trajectories follow the spreading wave packet (pure Bohmian drift).
*   **Key Indicator**: The "World Line" (Time vs Choice) should be roughly linear as density changes are smooth.

### [02_double_slit.py](./02_double_slit.py)
**Objective**: Detect "Choice Branching" geometries.
*   **Setup**: A high potential barrier ($V=20.0$) with two narrow slits.
*   **Hypothesis**: In standard Quantum Mechanics, the probability cloud shows interference fringes. In UKFT, "Choice" trajectories should distinctively navigate these fringes.
*   **Observation**: 
    - Watch how trajectories "decide" which slit to enter.
    - **Time Dilation**: Observe the Red "World Line" in the results. It should flatten (time slows) as the particle "processes" the complex information at the slits.

### [03_entropic_double_slit.py](./03_entropic_double_slit.py)
**Objective**: "The Golden Path" Visualization.
*   **Setup**: Double-slit barrier with high contrast visualization.
*   **Features**: 
    - **Magma Heatmap**: Empirical particle density.
    - **Lime Contours**: Theoretical quantum potential ridges.
    - **White Trails**: Individual choice-minimize trajectories ($T_0, T_1...$).
*   **Significance**: This is the flagship experiment demonstrating how `Choice` (Entropic Gravity) aligns particles with high-knowledge regions, sharpening the wavefunction reality.

### [03_entropic_sweep.py](./03_entropic_sweep.py)
**Objective**: Visualize the effect of Entropic Gravity ($\alpha$).
*   **Setup**: Runs the Double Slit experiment three times with varying $\alpha$ parameters:
    1.  **$\alpha=0.0$ (Control)**: Standard Bohmian Mechanics. Particles float passively on the quantum potential.
    2.  **$\alpha=5.0$ (Hybrid)**: Trajectories begin to cluster.
    3.  **$\alpha=15.0$ (Strong Choice)**: "Reality Sharpening".
*   **Interpretation**: 
    - At high $\alpha$, the simulation models a universe where "Action Minimization" (Choice) is dominant. 
    - Trajectories should look like lightning bolts or veins—rigidly sticking to the "optimal" (highest density) paths and avoiding low-probability regions almost entirely.

### [06_ukft_entropic_binary_plus_test_3d_dynamic.py](./06_ukft_entropic_binary_plus_test_3d_dynamic.py)
**Objective**: "Go Big or Go Home" - 3D Dynamic Space-Time warping.
*   **Setup**: Binary star system with a test particle on a dynamically recomputing curvature sheet.
*   **Features**:
    - **Pure Entropic Gravity**: Orbits sustained by $\nabla \rho$ maximization.
    - **Dynamic Curvature**: The background space-time grid warps live.
    - **Chaos**: Test particle capture and spiral dynamics.
*   **Significance**: Demonstrates that UKFT/Entropic Gravity can reproduce orbital mechanics and "curved space" phenomenology without General Relativity, using only knowledge density maximization.
