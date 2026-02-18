# Experiment 12: Massive Quantum Swarm (GPU Accelerated)

## Overview
This experiment validates the new **WGPU Entropic Accelerator** by scaling the particle count by 2 orders of magnitude (from ~500 to 50,000) while maintaining real-time frame rates.

## Technical Achievement
- **Particle Count**: 50,000
- **Technology**: WebGPU (via `wgpu-py`) running Compute Shaders (WGSL)
- **Performance**: >180 Million interactions/second
- **Visualization**: Plotly 3D (downsampled for rendering, full simulation on GPU)

## Physics
The simulation effectively models the **UKFT Quantum Potential** emergence from entropic forces.
- The swarming behavior creates a "SpaceTime Source" potential $R = \sqrt{\rho}$.
- The velocity law $v \sim \nabla \rho / \rho$ is successfully computed in parallel for 50k agents.

## Results
- **Animation**: [View Massive Swarm Simulation](../results/12_ukft_massive_swarm_gpu.html)
- The swarm exhibits coherent fluid-like properties, orbiting the binary system without scattering, behaving as a single macro-quantum object.
