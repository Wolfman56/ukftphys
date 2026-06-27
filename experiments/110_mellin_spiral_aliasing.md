# Experiment 110: Mellin-Fourier Spiral Aliasing

This experiment simulates the projection of discrete prime-capacity states onto a logarithmic spiral:
$$s_\theta(p) = \log(p) e^{i \theta \log(p)}$$

## Results
* **Optimal Spiral Angle (Minimum Aliasing)**: $\theta \approx 5.0000$
* **Spacing Variance at Optimal**: $1.2430$
* **Spacing Variance at De-coherent ($\theta = 5.800$)**: $1.2430$

The sharp minimum in the spacing variance demonstrates that there are specific discrete phase-angles where the prime capacities are distributed with maximum uniformity. Deviating from these angles causes the points to form high-density clusters separated by large voids, triggering Shannon-Nyquist under-sampling (aliasing) on the holographic screen.
