# Experiment 08: UKFT "Solar System" Simulator

## Objective
Demonstrate that **Entropic Gravity** (specifically the Bianconi/Araki Relatie Entropy formulation) can support stable, multi-body orbital mechanics that mimic a Solar System.

## The Theory
In this simulation, we model gravity **not** as a fundamental force, but as an **Emergent Entropic Force**.
*   **Matter** acts as a source of Information Density ($\rho$).
*   **Space-Time** is a "Knowledge Field".
*   **Gravity** ($F$) is the tendency of all systems to maximize their entropy (or minimize relative entropy) by moving towards higher density regions.

The specific force law used here is:
$$ \vec{F} = \alpha \nabla(\ln \rho) + \Lambda \vec{r} $$

This creates a **Harmonic Oscillator** potential ($F \propto r$) at large distances, which is incredibly stable for orbits, ensuring that "Planets" don't just drift away into the void as they would with a standard Gaussian force.

## The Setup
*   **Binary Star**: Two heavy information sources rotating in the center.
*   **Planets**:
    1.  **Mars (Red)**: Inner rocky planet.
    2.  **Earth (Green)**: Stable "Goldilocks" orbit.
    3.  **Jupiter (Orange)**: Distant gas giant (counter-rotating).
    4.  **Comet (White)**: Highly elliptical orbit intersecting the system.

## Comparison to Standard Physics
*   **Newton/Einstein**: Gravity is $1/r^2$. Orbits are Keplerian ellipses.
*   **UKFT (Bianconi)**: Gravity is effectively $r$ (Harmonic) at this scale. Orbits are also ellipses, but the period dynamics differ slightly. The fact that we get stable ellipses at all from pure *Information Theory* is the key insight.

## Results
!(results/08_ukft_solar_system.png)

Open [results/08_ukft_solar_system.html](./results/08_ukft_solar_system.html) for the interactive 3D simulation.
*   **Slider**: Scrub through time to see the binary star rotation and planetary orbits.
*   **Heatmap**: The green/blue surface represents the "Entropic Curvature" of space-time. Notice how the stars and planets create "dents" in the fabric of knowledge.
