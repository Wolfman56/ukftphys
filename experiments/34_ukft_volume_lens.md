# Experiment 34: UKFT Volumetric Lensing (The Star Field)

## 1. Background
Previous experiments (Exp 33) visualized a Black Hole against a "flat" background plane.
This experiment takes the simulation to **3D**. We distribute thousands of stars in a volumetric cube ($x, y, z$) and fly a UKFT Black Hole through it.

## 2. Objective
Visualize the **Dynamic Distortion of Spacetime** as a high-density object moves through a crowded star field.
Specific goals:
1.  **Parallax Lensing**: Foreground stars should be unaffected, while background stars are warped.
2.  **Einstein Rings**: When a star aligns perfectly behind the lens, its light should split into arcs or rings.
3.  **The Causal Mirror**: The core of the Black Hole should remain a solid, reflective obstacle (Cyan Sphere).

## 3. Simulation Method: "Ray Splatting"
Instead of reverse ray-marching (which is computationally expensive for volumetric point clouds), we use a **Forward Projection** technique based on the Lens Equation:
$$ \theta_{\pm} = \frac{\beta \pm \sqrt{\beta^2 + 4K}}{2} $$
Where:
-   $\beta$: True angular position of the star.
-   $\theta$: Apparent angular position (Image).
-   $K$: Lensing strength (proportional to Mass and Distances).

For every star in the volume, we solve this quadratic equation to find its **two possible image locations** on the camera plate:
1.  **Primary Image**: Shifted outwards (The main "lensed" star).
2.  **Secondary Image**: Inverted and shifted inwards (The "Einstein Ring" counterpart).

## 4. The Scene
-   **Stars**: 8,000 point sources with random colors and depths ($z \in [-10, 30]$).
-   **Black Hole**: Spiral path moving from front to back ($z: -10 \to 30$).
-   **Camera**: Orthographic Plate fixed at $z = -20$.

## 5. Visual Results
Watch how the background stars "fluidly" warp around the massive object, while foreground stars remain fixed until the object passes them.

![Volumetric Lensing](../results/34_ukft_volume_lens.gif)

**Key Features:**
-   **The Swim**: As the BH approaches a background star, the star appears to be "pushed away" by the lens.
-   **The Split**: If alignment is perfect, the star splits into two images on opposite sides of the ring.
-   **The Mirror**: The central Cyan Sphere blocks starlight (reflecting it away), creating a "hole" in the star field that isn't black, but solid.
