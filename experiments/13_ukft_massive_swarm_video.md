# Experiment 13: High-Fidelity Cinematic Render (GPU Optimized)

## Overview
This experiment addresses the visualization bottleneck encountered in Experiment 12. Instead of relying on browser-based WebGL (Plotly), which struggles with >5,000 particles, this experiment implements a **Direct GPU Rasterizer**.

## Implementation Details
1.  **Massive Scale**: 100,000 Particles (2x previous).
2.  **GPU Compute Renderer**: A new compute shader `render_points` was added to the `EntropicGPUAccelerator`. This shader performs:
    *   3D Projection (MVP Matrix)
    *   Frustum Culling
    *   Density Accumulation (Atomic Operations)
3.  **Video Pipeline**: The GPU outputs a high-res density map directly to Python, which is compiled into an MP4/GIF using Matplotlib.

## Features
- **Cinematic Camera**: Smooth orbital camera movement around the binary system.
- **Logarithmic Density**: Visualizes faint quantum trails and dense accretion structures simultaneously.
- **Zero-Copy Logic**: The particle positions stay on the GPU/VRAM as much as possible (only mapped for the density readout, visualization data is much smaller than particle data).

## Results
- **Output**: `results/13_ukft_cinematic.mp4`
- **Performance**: Rendering 100k particles takes <50ms per frame.
