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

### [07_ukft_bianconi_entropic_gravity.py](./07_ukft_bianconi_entropic_gravity.py)
**Objective**: "Relative Entropy Edition" (Bianconi/Araki patch).
*   **Physics**: Implements force law $F \propto \nabla (\ln \rho)$ based on "Gravity from Entropy" (Phys. Rev. D 111).
*   **Features**:
    - **Logarithmic Bias**: Minimizes quantum relative entropy between vacuum and matter states.
    - **Emergent Λ**: Toy "G-field" expansion term.
*   **Significance**: Connects UKFT's active choice mechanism to rigorous Information-Theoretical Gravity.

### [08_ukft_solar_system.py](./08_ukft_solar_system.py)
**Objective**: Multi-body Orbital Stability.
*   **Setup**: Simulates a "Solar System" with a central binary star and multiple orbiting planets.
*   **Significance**: Proves that Entropic Gravity can sustain stable multi-body orbits, not just binary pairs.

### [09_bianconi_double_slit.py](./09_bianconi_double_slit.py)
**Objective**: Entropic Force on Interference Fringes.
*   **Setup**: Applies the Bianconi/Araki ($\nabla \ln \rho$) force to a standard Double Slit Quantum Interference pattern.
*   **Observation**: The logarithmic gradient creates sharp "canyons" in the dark fringes, guiding particles strictly into the bright bands.

### [10_ukft_quantum_on_entropic_gravity_3d.py](./10_ukft_quantum_on_entropic_gravity_3d.py)
**Objective**: 3D Quantum Swarm Visualization.
*   **Setup**: A full 3D simulation of 400 Bohmian particles surfing the Entropic Gravity well of a binary star.
*   **Visuals**: "The Firefly Swarm". Particles light up as they accelerate through the quantum potential.

### [11_gpu_benchmark.py](./11_gpu_benchmark.py)
**Objective**: Hardware Acceleration Validation.
*   **Tech**: Validates the `wgpu` (WebGPU) installation and compute shader compilation.
*   **Result**: Benchmarked at >180 Million interactions/second (vs ~100k on CPU).

### [12_ukft_massive_swarm_gpu.py](./12_ukft_massive_swarm_gpu.py)
**Objective**: Massive Scale Simulation (50k Particles).
*   **Tech**: First full physics simulation running entirely on the GPU.
*   **Visuals**: Plotly visualization of a massive quantum fluid ring.

### [13_ukft_massive_swarm_video.py](./13_ukft_massive_swarm_video.py)
**Objective**: Direct GPU-to-Video Rendering.
*   **Problem**: Browser WebGL (Plotly) crashes with >5k particles.
*   **Solution**: Implemented a "Virtual Camera" compute shader to rasterize 100,000 particles directly on the GPU card.
*   **Result**: High-fidelity cinematic video of the quantum accretion disk.

### [14_ukft_perception_loop.py](./14_ukft_perception_loop.py)
**Objective**: The "Conscious" Feedback Loop (Part 1).
*   **Concept**: Integrates a "Perception Engine" (Observer) that watches the Physics Engine.
*   **Metric**: Calculates **Field Coherence** ($\phi$) in real-time.
*   **Result**: The Observer successfully tracks the stability of the quantum swarm.

### [15_ukft_consciousness_feedback.py](./15_ukft_consciousness_feedback.py)
**Objective**: Emergent Agency / Homeostasis (Part 2).
*   **Concept**: Closed-loop control where the Observer's perception *modifies* the physical laws.
*   **Scenario**: A chaotic event disrupts the swarm. The Observer detects coherence loss and exerts "Willpower" (increased gravity/damping) to restabilize reality.
*   **Significance**: "The Big One". Demonstrates a self-healing quantum system.

### [16_ukft_prophet_autotune.py](./16_ukft_prophet_autotune.py)
**Objective**: The "God Attractor" - Gravity Emergence.
*   **Concept**: A Prophet Agent tries to minimize "Trajectory Prediction Error".
*   **Result**: The agent naturally discovers a gravitational constant $\alpha \approx 1.0$.
*   **Conclusion**: Gravity is not an axiom, it is an optimization solution for information coherence.

### [17_ukft_entanglement_propagation.py](./17_ukft_entanglement_propagation.py)
**Objective**: The "God Attractor" - Causal Entanglement.
*   **Concept**: Simulating "Zombie States" (undefined causality) that only resolve when a future constraint (Alice meeting Bob) is imposed.
*   **Result**: Entanglement is shown to be the resolution of a causal graph, not superluminal communication.

### [18_ukft_learning_light_speed.py](./18_ukft_learning_light_speed.py)
**Objective**: The "God Attractor" - Speed of Light.
*   **Concept**: Minimizing Information Propagation Delay across a discrete grid.
*   **Result**: The maximum effective speed asymptotically approaches 1.0 grid/tick.
*   **Conclusion**: $c$ is the processing rate limit of the simulation hardware (the Universe).

### [19_hierarchy_prototype.py](./19_hierarchy_prototype.py)
**Objective**: The "God Attractor" - Theosphere.
*   **Concept**: A 3-Tier Control System (Geo/Noo/Theo) to prevent entropic dissolution.
*   **Stress Test**: "The Great Disruption" (Radial Velocity Kick).
*   **Result**: The Theosphere (Level 3) intervenes with massive force ($\alpha > 3.0$) only when the system faces critical collapse ($\phi < 0.40$).

### [20_hierarchy_memory.py](./20_hierarchy_memory.py)
**Objective**: The "God Wakes Slowly" Protocol.
*   **Extension**: Adds memory windows ($W_{geo}=10, W_{noo}=50, W_{theo}=100$) to Exp 19.
*   **Result**: Shows that higher intelligences ignore short-term panic. The Noosphere handled the disruption without requiring Theospheric intervention because the *averaged* coherence remained stable.


### [25_emergent_gluon_analogue.py](./25_emergent_gluon_analogue.py)
**Objective**: Emergence of QCD Color Force.
*   **Concept**: Simulating "link excitations" (gluons) in a high-density causal graph.
*   **Result**: Validates the emergence of color-like symmetry from graph topology.

### [26_emergent_graviton.py](./26_emergent_graviton.py)
**Objective**: Emergence of Gravity (The Double Copy).
*   **Concept**: Applying the BCJ Double Copy principle (65519Gravity \sim Gauge^265519) to the emergent gluon field.
*   **Result**: Demonstrates that entropic pressure naturally generates an attractive inverse-square law.

### [27_anomalous_gluon_jets.py](./27_anomalous_gluon_jets.py)
**Objective**: The Single-Minus Gluon Anomaly.
*   **Concept**: Testing gluon amplitudes in "half-collinear" kinematic limits.
*   **Result**: Confirms a non-zero amplitude for single-minus states, defying classical Yang-Mills expectations.

### [28_gravity_anomaly.py](./28_gravity_anomaly.py)
**Objective**: The Single-Minus Graviton Anomaly (Dark Matter Candidate 1).
*   **Concept**: Testing gravity amplitudes in "half-collinear" kinematic limits.
*   **Result**: Discovers a ~300x enhancement in gravity strength for collinear vacuum states.

### [29_dark_matter_halo.py](./29_dark_matter_halo.py)
**Objective**: Gravitational Halo from Collinear Vacuum Filaments.
*   **Concept**: Simulating a Galaxy Rotation Curve under anomalous gravity.
*   **Result**: Demonstrates a flat rotation curve, explaining Dark Matter phenomenologically as vacuum coherence effects.

### [30_particle_spectroscopy.py](./30_particle_spectroscopy.py)
**Objective**: The 4 Emergent Particles of the Choice Field.
*   **Concept**: Classifying stable topological defects in the causal graph.
*   **Result**: Identifies: Thread (Photon), Knot (Matter), Mirror (Boundary), and Void (Scalar).

### [31_mirror_fermion.py](./31_mirror_fermion.py)
**Objective**: Unitarity Restoration & The Mirror Fermion.
*   **Concept**: Solving the Black Hole Information Paradox via boundary reflection.
*   **Result**: Confirms a massive "Mirror State" is required to conserve information at causal horizons.

### [32_void_scalar.py](./32_void_scalar.py)
**Objective**: The Void Scalar (Dark Energy as Vacuum Pressure).
*   **Concept**: Simulating vacuum pressure in low-entropy voids.
*   **Result**: Confirms that a "Choice Floor" constraint forces voids to expand, generating Dark Energy ($\Lambda$).

