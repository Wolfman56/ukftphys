# Universal Knowledge Field Theory (UKFT) Simulation

This repository contains a **Choice-Guided Bohmian Mechanics** simulator. It implements a novel interpretation of Quantum Mechanics where "Time" is emergent from a sequence of Discrete Action Minimizing choices.

## Theoretical Basis

This simulation code explores the intersection of:
1.  **Bohmian Mechanics**: Pilot-wave theory where particles have definite trajectories.
2.  **Entropic Gravity (Bianconi)**: Trajectories are biased towards regions of higher information density (Network Entropy).
3.  **Universal Knowledge Field Theory (UKFT)**:
    *   **Choice is Fundamental**: The simulation steps through "Choice Indices" ($n$), not Physical Time ($t$).
    *   **Dynamic Time**: Physical time is an emergent property. $dt \propto 1/\rho$. Time "slows down" (resolution increases) in regions of high Consciousness/Knowledge density.
    *   **Choice Space**: Trajectories do not cross in Physical Space-Time, but they "branch" in Choice Space based on the Entropic Gravity parameter.

## Project Structure

*   `ukft_sim/`: The core python package containing the physics engine, solver, and visualization logic.
    *   `physics.py`: Discrete Action Minimizer and Quantum Potential calc.
    *   `solver.py`: `SimulationRunner` handling the sequential choice loop and dynamic time.
    *   `vis.py`: Interactive 3D/2D plotting using Plotly.
*   `experiments/`: Reproducible experiment scripts (see `experiments/README.md`).
*   `results/`: Generated HTML reports and plots (git-ignored).
*   `archive/`: Deprecated monolithic scripts and notes.

## Installation

1.  **Clone the repo**
2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    Or using Conda:
    ```bash
    conda env create -f environment.yaml
    conda activate quantum_foam
    ```

## Usage

Run any experiment script from the root directory:

```bash
# Run the basic free particle test
python experiments/01_free_particle.py

# Run the double slit experiment
python experiments/02_double_slit.py
```

Results will be saved to the `results/` directory as interactive HTML files (e.g., `results/02_double_slit_results.html`). Open these in your browser to explore the 3D Choice Space.
