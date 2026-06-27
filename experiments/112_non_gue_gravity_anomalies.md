# Experiment 112: Emergent Gravity under Non-GUE Spacings

This experiment simulates the emergent entropic force on a holographic screen when the spacing of the capacity-generating zeros deviates from the Gaussian Unitary Ensemble (GUE).

## Theoretical Background
In Verlinde's entropic gravity, the number of bits $N$ on the holographic screen scales as the Area ($A = 4\pi r^2$). Under the equipartition theorem:
$$F = T \frac{dS}{dr} \propto \frac{1}{N} \propto \frac{1}{r^2}$$
This uniform scaling is a direct consequence of the uniform GUE spacing of the zeros. 

If the spacing deviates from GUE, the capacity density of the screen becomes non-uniform:
1. **Poisson Spacing (No Repulsion)**: Zeros cluster randomly, producing local density fluctuations. This introduces stochastic fluctuations in the gravitational force $\vec{F}(r)$.
2. **Linear Capacity Saturation**: At large scales, the capacity of the screen saturates and scales linearly with radius ($N(r) \propto r$). Under this regime, the temperature scales as $T \propto 1/r$, yielding an emergent force:
   $$F(r) \propto \frac{1}{r}$$
   This force law implies a **flat rotation curve**:
   $$v(r) = \sqrt{F \cdot r} \approx \text{constant}$$

## Results
* **GUE Spacing**: Produces the classical Newtonian $1/r^2$ force and a Keplerian velocity decay $v \propto 1/\sqrt{r}$.
* **Poisson Spacing**: Introduces localized gravitational anomalies and velocity fluctuations.
* **Linear Saturation**: Successfully generates a **flat rotation curve** at large distances ($r > r_0$), matching the observed rotation curves of galaxies without invoking physical dark matter particles.
