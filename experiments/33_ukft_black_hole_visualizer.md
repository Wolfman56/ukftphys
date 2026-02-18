# Experiment 33: The UKFT "Black Hole" Visualizer

## 1. Background
In Standard General Relativity, a Black Hole is a region of infinite curvature (Singularity) hidden behind an Event Horizon. Matter falling in is lost forever.

However, **UKFT (Universal Knowledge Field Theory)** models the universe as a discrete Causal Graph with finite processing capacity.
-   **No Singularity**: Information density cannot exceed 1 bit per Planck volume (or grid cell).
-   **The Saturation Limit**: When a region reaches maximum causal density ($\rho_{max}$), it cannot process new events.
-   **The Mirror Effect**: To conserve Unitarity (Information), the "Event Horizon" must act as a perfect reflector (or scrambler). Light and matter should bounce off the "solid" vacuum.

## 2. Objective
Visualize what a Black Hole "looks like" under these rules:
1.  **Entropic Gravity Lensing**: Light rays bend towards high-density regions ($\vec{F} \propto \nabla \ln \rho$).
2.  **Causal Reflection**: Light rays that hit the Saturation Horizon ($\rho > \rho_{max}$) are reflected, not absorbed.

## 3. Simulation Setup
-   **Method**: 2D Ray Tracing on a scalar density field.
-   **The Hole**: A Gaussian "Mass" concentration.
-   **The Limit**: A cutoff density $\rho_{max}$ defines the radius of the "Solid Horizon".
-   **The Probe**: A swarm of 40 photon trajectories launched at the anomaly.

## 4. Expected visualization
Instead of a black disk that swallows light, we expect to see:
-   **The Halo**: A glowing ring of bent light (standard lensing).
-   **The Mirror**: A central "hard sphere" where light bounces back.

## 5. Visualization Color Key (The Physics of Light)
The simulation renders the scene in distinct colors representing Information Density Regimes:

*   **Cyan/Chrome Sphere (The Causal Mirror)**:
    *   **Region**: $r < R_s$ (Event Horizon).
    *   **Physics**: Maximum Causal Density ($\rho \ge \rho_{max}$).
    *   **Meaning**: The "hard drive" of space is full. Matter and light reflect off this surface to preserve unitarity.
*   **Golden Ring (The Photon Sphere)**:
    *   **Region**: Just outside the Horizon.
    *   **Physics**: High-Friction Processing Loop.
    *   **Meaning**: Light is trapped in orbit, generating "heat" (entropy) from the immense computational density.
*   **Red/Orange Background (The Entropic Lens)**:
    *   **Region**: The Distant Universe (JWST Deep Field).
    *   **Physics**: Gravitational Lensing ($\nabla \ln \rho$).
    *   **Meaning**: Ancient galaxies (high redshift) warped by the foreground mass.

## 6. Artifacts
-   **Code**: `experiments/33c_ukft_black_hole_jwst.py` (High-Res Flyby)
-   **Result**: `results/33c_ukft_black_hole_jwst.gif`

![The UKFT Black Hole Flyby](../results/33c_ukft_black_hole_jwst.gif)
