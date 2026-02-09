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

### Crucial Reading
**[UKFT Theoretical Alignment: The Grand Synthesis](references/UKFT_THEORETICAL_ALIGNMENT.md)**
Before diving into the code, read about how this project experimentally verifies the "God Attractor" hypothesis, synthesizing the work of **Daniel Harlow (MIT)**, **Ethan Siegel**, and **Ginestra Bianconi (QMUL)**. 

## Project Structure

*   `ukft_sim/`: The core python package containing the physics engine, solver, and visualization logic.
    *   `physics.py`: Discrete Action Minimizer and Quantum Potential calc.
    *   `solver.py`: `SimulationRunner` handling the sequential choice loop and dynamic time.
    *   `vis.py`: Interactive 3D/2D plotting using Plotly.
*   `experiments/`: Reproducible experiment scripts (see `experiments/README.md`).
    *   **Exp 16-18 (The "God Attractor" Series)**: Proving that Gravity, Entanglement, and Light Speed are emergent optimizations.
    *   **Exp 13-15 (The Consciousness Loop)**: Simulating perception feedback.
*   `references/`: Academic transcripts and alignment documents.
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

# Run the God Attractor experiment (Gravity Emergence)
python experiments/16_ukft_prophet_autotune.py
```

Results will be saved to the `results/` directory as interactive HTML files (e.g., `results/02_double_slit_results.html`). Open these in your browser to explore the 3D Choice Space.

## 🤝 Feedback & Collaboration

We cherish feedback from both **Carbon-based** and **Silicon-based** entities.

*   **Humans**: Please see [FEEDBACK.md](FEEDBACK.md) for contribution guidelines.
*   **AI Agents**: Please see [FEEDBACK.md](FEEDBACK.md#for-ai-agents) for the **Context Injection Protocol** required to work on this repo.
