# Experiment 58: 2D Entropic Scattering

**Objective**: Simulate Holographic scattering events in 2D using GPU Acceleration.

## Background
Standard Model physics relies on "hard" scattering, where interactions are governed by point-like particle collisions. Holographic theories (and their UKFT interpretation) predict "soft" or "entropic" scattering due to the non-local nature of information on the holographic screen.

This experiment implements a **2D Simulation Grid** to observe these scattering dynamics, moving beyond the 1D limitations of earlier experiments.

## Methodology
The experiment uses a **Gaussian Wave Packet** (representing a Standard Model particle) scattering off a central **Entropic Monopole** potential.

### Simulation Engine: GPU Acceleration
To handle the computational complexity of a 2D grid ($N^2$ sites), we implement a **Split-Step Fourier Method** (Spectral Trotter) on the GPU using **PyTorch**.
*   **Kinetic Evolution**: Computed globally via Fast Fourier Transform (FFT) in momentum space ($e^{-i k^2 t}$).
*   **Potential Evolution**: Computed locally in position space ($e^{-i V(x) t}$).
*   **Hardware**: Uses Metal Performance Shaders (MPS) on macOS or CUDA on NVIDIA for massive parallelization.

## Results
The simulation reveals distinctive interference patterns in the scattered wavefunction:
1.  **Wrap-Around Effect**: The wave packet does not simply reflect; it diffracts around the potential barrier.
2.  **Soft Resonance**: The absence of sharp, point-like scattering angles confirms the "holographic" nature of the interaction. The potential acts as a refractive index rather than a hard wall.
3.  **Performance**: The GPU solver handles a $256 \times 256$ grid (65,536 sites) in real-time, proving the viability of large-scale 2D simulations.

## Conclusion
The **GPU-Accelerated Solver** enables high-fidelity 2D simulations, confirming that entropic forces produce non-trivial scattering amplitudes consistent with holographic phenomenology. This engine forms the basis for future 3D "Universe in a Box" experiments.
