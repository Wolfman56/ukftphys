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

### [11_gpu_benchmark.md](./11_gpu_benchmark.md)
**Objective**: Hardware Acceleration Validation.
*   **Tech**: Validates the `wgpu` (WebGPU) installation and compute shader compilation.
*   **Result**: Benchmarked at >180 Million interactions/second (vs ~100k on CPU).

### [12_ukft_massive_swarm_gpu.md](./12_ukft_massive_swarm_gpu.md)
**Objective**: Massive Scale Simulation (50k Particles).
*   **Tech**: First full physics simulation running entirely on the GPU.
*   **Visuals**: Plotly visualization of a massive quantum fluid ring.

### [13_ukft_massive_swarm_video.md](./13_ukft_massive_swarm_video.md)
**Objective**: Direct GPU-to-Video Rendering.
*   **Problem**: Browser WebGL (Plotly) crashes with >5k particles.
*   **Solution**: Implemented a "Virtual Camera" compute shader to rasterize 100,000 particles directly on the GPU card.
*   **Result**: High-fidelity cinematic video of the quantum accretion disk.

## Creating New Experiments

When adding a new experiment script (e.g., `experiments/99_new_idea.py`), you **MUST** create a corresponding `explainer.md` file in the same directory (or a dedicated folder).

### Explainer Template
The explainer file (e.g., `experiments/99_new_idea_explainer.md`) must follow this structure to ensure scientific reproducibility:

```markdown
# Experiment 99: [Title]
**Objective**: [One sentence summary]

## Hypothesis
What are we testing? Reference specific equations or UKFT principles (e.g., "Testing if Entropic Gravity emerges from N \propto A").

## Methodology
*   **Setup**: Description of the initial conditions (e.g., "Two Gaussian packets colliding").
*   **Key Parameters**: List critical constants ($\alpha$, $N$, $dt$).
*   **Metric**: What are we measuring? (e.g., "Entropic Dimension $D_E$").

## Results (Expected or Observed)
*   **Observation**: What happened?
*   **Significance**: Does this support or refute the hypothesis?

## Usage
Command to run:
`python experiments/99_new_idea.py`
```

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

### [33_ukft_black_hole_visualizer.py](./33_ukft_black_hole_visualizer.py)
**Objective**: The Causal Mirror (Visualizing the UKFT Event Horizon).
*   **Concept**: 2D Ray Tracing of entropic gravity and causal density limits.
*   **Result**: Reveals a Black Hole as a **Reflective Sphere** (The "Black Stone") surrounded by a glowing photon ring.

### [34_ukft_volume_lens.py](./34_ukft_volume_lens.py)
**Objective**: Volumetric Lensing (The Star Field).
*   **Concept**: Forward projecting 8,000+ stars through a moving gravitational lens.
*   **Result**: Visualizes the dynamic "LSD" (Large Scale Distortion) of spacetime as the massive object passes through.

### [35_mirror_fermion_madgraph.md](./35_mirror_fermion_madgraph.md)
**Objective**: Phenomenology of the Mirror Fermion.
*   **Concept**: Using MadGraph5 to simulate the collider signature of the Mirror Fermion.
*   **Result**: Establishes baseline cross-sections for a heavy stable particle.

### [36_mirror_fermion_mass_scan.py](./36_mirror_fermion_mass_scan.py)
**Objective**: Mass Hierarchy Search.
*   **Concept**: Scanning the mass parameter space to find stable resonance points.
*   **Result**: Identifies a potential stability island around 320 GeV.

### [37_mirror_fermion_decay.py](./37_mirror_fermion_decay.py)
**Objective**: Decay Width Analysis.
*   **Concept**: Calculating the decay width ($\Gamma$) of the Mirror Fermion.
*   **Result**: Discovers the "5/9 Rule" ($\Gamma/M \approx 5/9 \alpha_{EM}$).

### [38_mirror_fermion_collider.py](./38_mirror_fermion_collider.py)
**Objective**: Collider Peak Simulation.
*   **Concept**: Simulating the invariant mass peak reconstruction at the LHC.
*   **Result**: Successful reconstruction of the 320 GeV peak over background.

### [39_mirror_fermion_detector.py](./39_mirror_fermion_detector.py)
**Objective**: Detector Response.
*   **Concept**: Comparing ideal vs. realistic detector responses using Gaussian smearing.
*   **Result**: The signal remains robust even with 5-10% energy resolution errors.

### [40_background_simulation.py](./40_background_simulation.py)
**Objective**: Standard Model Backgrounds.
*   **Concept**: Simulating $t\bar{t}$ and $W/Z$ backgrounds to estimate signal-to-noise.
*   **Result**: Identifying kinematic cuts to suppress the dominant top quark background.

### [41_entropic_link.py](./41_entropic_link.py)
**Objective**: The Entropic Link (Gravity = Entanglement).
*   **Concept**: Simulating the tension between entangled particles.
*   **Result**: Verifies that entanglement generates an attractive force indistinguishable from gravity.

### [42_geometric_factor_search.py](./42_geometric_factor_search.py)
**Objective**: Geometric Origin of Constants.
*   **Concept**: Searching for geometric relations (pi, e, golden ratio) in the coupling constants.
*   **Result**: Finds the "Geometric Factor" linking the fine-structure constant to the graph topology.

### [43_theoretical_5_9_investigation.ipynb](./43_theoretical_5_9_investigation.ipynb)
**Objective**: Theory of the 5/9 Rule.
*   **Concept**: Deriving the decay width ratio from SU(5) group theory factors.
*   **Result**: Theoretical confirmation of the empirical 5/9 scaling observed in Exp 37.

### [44_mirror_fermion_precision.py](./44_mirror_fermion_precision.py)
**Objective**: Precision Mass Measurement.
*   **Concept**: High-resolution scan of the 320 GeV region.
*   **Result**: Refines the mass prediction to $320 \pm 25$ GeV.

### [45_color_factor_verification.py](./45_color_factor_verification.py)
**Objective**: QCD Color Factors.
*   **Concept**: Verifying the color charge ($N_c=3$) enhancement of the production cross-section.
*   **Result**: Confirms experimentally that the object transforms as a color triplet.

### [46_entropic_monopole.py](./46_entropic_monopole.py)
**Objective**: The Entropic Monopole (The Field Knot).
*   **Concept**: Simulating a topological defect ("Hedgehog") in a 3D lattice vector field.
*   **Result**: Confirms a **stable** monopole with mass **30.0 Lattice Units** ($\sim$ 30 GeV).

### [47_void_scalar.py](./47_void_scalar.py)
**Objective**: Dark Energy as Entropic Pressure.
*   **Concept**: Simulating the "Void Scalar" field in low-information-density regions.
*   **Result**: Demonstrates that entropy maximization in voids creates an expansive "Vacuum Tension" (Dark Energy).

### [48_entropic_monopole_madgraph.md](./48_entropic_monopole_madgraph.md)
**Objective**: Collider Phenomenology of the Monopole.
*   **Concept**: Using MadGraph5 to simulate the 30 GeV Monopole production via Gluon Fusion.
*   **Result**: Cross-section $\sim 189$ pb. The particle is light but strongly interacting.

### [49_monopole_black_hole_analogue.md](./49_monopole_black_hole_analogue.md)
**Objective**: Monopole-Black Hole Duality.
*   **Concept**: Calculating the Hawking Temperature of a 30 GeV mass.
*   **Result**: Discovers a perfect duality: $T_H(30 \text{ GeV}) \approx 30 \text{ GeV}$. The Monopole behaves like a "Maximum Temperature" Black Hole.

### [50_entropic_monopole_dynamics.md](./50_entropic_monopole_dynamics.md)
**Objective**: The Sound of the Monopole.
*   **Concept**: Analyzing the acoustic/radiation spectrum of a perturbed monopole field.
*   **Result**: The spectrum matches a **Thermal Body** (Black Body Radiation) rather than a single particle resonance.

### [51_holographic_entropy_theory.md](./51_holographic_entropy_theory.md)
**Objective**: The Holographic Link (Strong Gravity).
*   **Concept**: Deriving the "Strong Gravity" constant ($G_s$) required for the Monopole to be a Black Hole.
*   **Result**: Finds $G_s \approx 10^{38} G_{Newton}$, matching the Strong Hierarchy scale.

### [52_holographic_pheno.md](./52_holographic_pheno.md)
**Objective**: Holographic Phenomenology.
*   **Concept**: Comparing standard decays ($H \to b\bar{b}$) vs. Holographic decays ($H \to \text{Mirror}$).
*   **Result**: The "Holographic" decay is characterized by a "Soft Resonance" with significant Missing Transverse Energy (MET) peaking at $\sim 15$ GeV ($M/2$).


### [53_mirror_fermion_jet_substructure.md](./53_mirror_fermion_jet_substructure.md)
**Objective**: Mirror Fermion Detection via Entropic Substructure.
*   **Concept**: Simulating the decay of Mirror Fermions ($F_M \to qqq$) vs QCD Jets ($g \to q\bar{q}$).
*   **Innovation**: Introduces the **Entropic Discriminator ($D_E$)**.
*   **Result**: Mirror Fermion jets are "entropicly maximizing" (isotropic, high $D_E$), whereas QCD jets are "fractal" (collinear, low $D_E$). >5 sigma separation.

### [54_holographic_newtonian_derivation.md](./54_holographic_newtonian_derivation.md)
**Objective**: First Principles Derivation of Newton's Law.
*   **Concept**: Simulating "Choice Density" on a spherical holographic screen.
*   **Fix**: Corrects the circular reasoning in Exp 26.
*   **Result**: Proves that if Information scales as Area ($N \propto A$), the Entropic Force $F = T \nabla S$ naturally obeys the Inverse Square Law ($1/r^2$).

### [55_parallel_causality_engine.md](./55_parallel_causality_engine.md)
**Objective**: $O(N)$ Causal Evolution.
*   **Concept**: Treating the simulation as a Cellular Automaton.
*   **Innovation**: Replacing global matrix exponentiation $O(N^3$) with local odd/even Trotter steps $O(N)$.
*   **Result**: Accelerates `ukft_sim` up to 100x while maintaining unitarity and causal fidelity.

### [56_mirror_fermion_width_check.md](./56_mirror_fermion_width_check.md)
**Objective**: Standard Model Consistency Check.
*   **Concept**: Verifying the decay width formula for heavy fermions.
*   **Result**: Confirms $\Gamma \approx \frac{G_F M^3}{8\pi\sqrt{2}} \approx 10$ GeV for a 320 GeV Mirror Fermion.

### [57_trotter_integration_test.md](./57_trotter_integration_test.md)
**Objective**: Validate the $O(N)$ Parallel Causality Engine.
*   **Concept**: Comparing Global Matrix Exponentiation ($O(N^3)$) vs. Local Trotter-Suzuki Decomposition ($O(N)$).
*   **Result**: Achieved ~3000x speedup with perfect fidelity ($|\langle \psi_G | \psi_L \rangle| = 1.0$), proving causality is preserved locally.

### [58_gpu_entropic_scattering.md](./58_gpu_entropic_scattering.md)
**Objective**: 2D Entropic Scattering on GPU.
*   **Concept**: Simulating a Gaussian Wave Packet scattering off an Entropic Monopole using a GPU-accelerated Split-Step Fourier method.
*   **Visuals**: Observe "Soft Resonance" – holographic diffraction patterns distinct from hard-sphere scattering.
*   **Tech**: Implemented a PyTorch-based GPU Solver capable of running $256 \times 256$ grids in real-time.
