# KZM in Materials — Literature Review

*Supporting material for Exp 107 / Exp 108 and Paper 41.*

---

## 1. Foundational Theory

### 1.1 Original Proposals

**Kibble (1976)** — *J. Phys. A 9, 1387*  
Proposed that topological defects form when a system is driven through a
symmetry-breaking phase transition faster than the causal-contact time allows
regions to coordinate.  Original context: cosmological field theories (monopoles,
cosmic strings, domain walls).  Key insight: defect density is set by the
correlation length at the "freeze-out" moment when fluctuations can no longer
track the moving critical point.

**Zurek (1985)** — *Nature 317, 505*  
Independently proposed the condensed-matter analogue: liquid $^4$He cooled
through the superfluid transition generates vortices at a density set by the
competition between the cooling rate and the equilibration time.  Derived the
scaling law $n_\text{def} \propto \tau_Q^{-d\nu/(1+\nu z)}$ in $d$ dimensions.

**Zurek (1996)** — *Phys. Rep. 276, 177*  
Full review establishing the KZM for condensed-matter systems.  Covers the
adiabatic–impulse approximation, the freeze-out correlation length, and the
connection to Ginzburg–Landau theory.

### 1.2 Theoretical Developments

**del Campo & Zurek (2014)** — *Int. J. Mod. Phys. A 29, 1430018*  
Comprehensive review covering KZM in diverse systems: ultracold atoms, ion
traps, superconductors, liquid crystals, cosmological analogues.  Establishes
the adiabatic–impulse picture as the standard framework.

**Chandran, Erez, Gubser & Sondhi (2012)** — *Phys. Rev. B 86, 064304*  
Kibble–Zurek problem is non-trivial even for purely classical models: spatial
correlations in the ordered phase are set by $\xi_\text{KZM}$ but the defect
density formula depends sensitively on whether the system is in the over- or
underdamped regime.

**Zurek, Dorner & Zoller (2005)** — *Phys. Rev. Lett. 95, 105701*  
Dynamics of the quantum transverse-field Ising chain: quasi-particle excitations
play the role of defects.  KZM exponent verified analytically.  First bridge
between classical and quantum KZM.

---

## 2. 2D Ising Model — Numerics and Experiment

### 2.1 Monte Carlo Studies

**Jelic & Cugliandolo (2011)** — *J. Stat. Mech. P02032*  
Careful MC study of KZM in the 2D FM Ising model.  Finds the DWD scales as
$\rho \propto \tau_Q^{-1/3}$ (model-A exponent) over more than two decades in
quench rate.  Key methodological point: N≥500 reps required to resolve the
scaling at small n_sweeps due to single-wall sampling noise.  **Directly
relevant to our Exp 107/108 design.**

**Biroli, Cugliandolo & Sicilia (2010)** — *Phys. Rev. E 81, 050101(R)*  
Coarsening vs KZM: distinguishes the power law expected from pure coarsening
($\rho \propto t^{-1}$ for model-A) from the KZM power law ($\rho \propto
\tau_Q^{-1/3}$) for the 2D Ising model.  The two regimes are separated by
the freeze-out scale $n_\text{freeze} \approx \xi_\text{KZM}^2$.

**Rams, Zwolak & Damski (2012)** — *Sci. Rep. 2, 655*  
KZM in the 2D quantum Ising model.  Finds $z=1$ (quantum), so the exponent is
$\nu/(1+\nu z) = 1/(1+1) = 1/2$.  Confirms that classical and quantum KZM are
in different universality classes.

**Liu & Mazenko (1992)** — *Phys. Rev. B 46, 5963*  
Early simulation showing Ising dynamics ($z \approx 2$) in the coarsening regime
after a quench to $T < T_c$.  Establishes the baseline for what "model-A"
dynamics looks like in the 2D Ising model.

### 2.2 Antiferromagnetic Ising Specifics

The 2D AF Ising on a square lattice is related to the 2D FM Ising by the
staggered transformation $\sigma_i \to (-1)^{i_x + i_y} \sigma_i$:

$$
H_\text{AF} = J_\text{AF} \sum_{\langle ij\rangle} \sigma_i \sigma_j
\xrightarrow{\text{stagger}} H_\text{FM} = -J_\text{FM} \sum_{\langle ij\rangle}
\tilde\sigma_i \tilde\sigma_j
$$

This maps $J_\text{AF} > 0 \to J_\text{FM} = J_\text{AF} > 0$ with no change in
the critical universality.  The AF model has the same $T_c$, same $\nu$, same
$z$, and the same KZM exponent as the FM model.  The DWD observable for the AF
model (same-sign bonds) corresponds to the domain-wall observable for the FM
model (opposite-sign bonds) under the staggered transformation.

**Consequence for Exp 107/108**: all theoretical predictions for the 2D FM
Ising KZM apply directly to our AF model.

### 2.3 Finite-Size and Finite-N Effects

**Francuz, Dziarmaga, Gardas & Zurek (2016)** — *Phys. Rev. B 93, 075134*  
Finite-size scaling of KZM: for $L < \xi_\text{KZM}$, the density saturates at
$\rho \sim L^{-d}$.  For $L \gg \xi_\text{KZM}$, bulk KZM scaling holds.  Our
L=256 with $n_\text{max}=1.6 \times 10^6$ is in the $L > \xi_\text{KZM}$ regime
for the single-wall n-range (n ≤ 25600).

**Albash & Lidar (2018)** — *Rev. Mod. Phys. 90, 015002*  
Review of adiabatic quantum computation and quantum annealing.  Discusses
zero-censoring and finite-sample effects when measuring KZM in systems where
the ground-state probability is small.  Our "zero censoring" problem (P(DWD>0)
≈ 0.3 at some L, n) is a classical version of this issue.

---

## 3. Experimental Observations of KZM

### 3.1 Liquid Crystals

**Chuang, Durrer, Turok & Yurke (1991)** — *Science 251, 1336*  
First clean experimental observation of KZM: liquid crystal cooled through the
isotropic–nematic transition.  Topological defect density scales with cooling
rate as predicted.  Classic benchmark for KZM theory.

**Bowick, Chandar, Schiff & Srivastava (1994)** — *Science 263, 943*  
Liquid crystal monopole density follows $\rho \propto \tau_Q^{-\nu/(1+\nu z)}$
over 1.5 decades.  Established that the exponent, not just the scaling, is
accessible experimentally.

### 3.2 Ultracold Atoms

**Chen et al. (2011)** — *Phys. Rev. Lett. 106, 145302*  
BEC formation through a quench: vortex density follows KZM power law.
Demonstrated in a quasi-2D geometry; exponent consistent with 2D XY universality.

**Navon, Gaunt, Smith & Hadzibabic (2015)** — *Science 347, 167*  
Homogeneous BEC: first observation of KZM in a 3D system with controlled
quench rate.  Measured scaling exponent agrees with theory within 20%.

### 3.3 Ion Traps

**Ulm et al. (2013)** — *Nat. Commun. 4, 2290*  
Structural phase transition in a trapped ion crystal: kinks (topological defects)
freeze in at a rate consistent with KZM.  ~100 ions; 1D geometry.

**Pyka et al. (2013)** — *Nat. Commun. 4, 2291*  
Independent experimental confirmation in same geometry; different group.
Both Ulm et al. and Pyka et al. confirm $\rho \propto \tau_Q^{-1/4}$ (1D KZM).

### 3.4 Superconductors

**Monaco, Mygind & Rivers (2002)** — *Phys. Rev. Lett. 89, 080603*  
Flux trapping in a Josephson junction ring cooled through $T_c$.  Fluxoid
density follows the KZM prediction for a 1D ring geometry.

**Maniv, Polturak & Koren (2003)** — *Phys. Rev. Lett. 91, 197001*  
Vortex density in thin superconducting films (2D): observed KZM scaling over
one decade.  First 2D experimental KZM observation in a superconductor.

---

## 4. GPU and HPC Methods for Ising Simulations

### 4.1 Checkerboard Decomposition

**Preis, Virnau, Paul & Schneider (2009)** — *J. Comput. Phys. 228, 4468*  
GPU Monte Carlo for Ising model using checkerboard (2-sublattice) decomposition.
Reports 1.4 × 10⁹ spin-flips/s on a single GTX 295.  Establishes the
correctness of parallel checkerboard updates.  **Direct algorithmic ancestor
of our WGSL implementation.**

**Weigel (2011)** — *J. Phys.: Conf. Ser. 280, 012006*  
Survey of GPU Monte Carlo methods for spin models.  Discusses RNG requirements
(per-thread independence), update rule correctness, and performance.  Recommends
linear congruential or XorShift generators for on-device use (PCG32 is a modern
improvement over both).

**Block, Virnau & Preis (2010)** — *Comput. Phys. Commun. 181, 1549*  
Multi-GPU Ising simulations.  Establishes that nearest-neighbour communication
between sublattice updates is the bottleneck, not GPU compute.  Our per-rep
independent runs avoid this bottleneck entirely (no inter-rep communication).

### 4.2 WGSL / WebGPU

**W3C WebGPU specification (2024)**  
WGSL (WebGPU Shading Language) is the compute shader language for the WebGPU
API.  It targets Metal (macOS/iOS), Vulkan (Linux/Android), and DX12 (Windows)
through a single portable shader source.  The `wgpu` Rust crate provides the
native (non-browser) backend.

No prior published KZM measurements using WGSL are known to us as of 2026;
this work appears to be the first.

---

## 5. Summary: Gap Filled by Exp 107/108

| Prior art gap | Our contribution |
|---------------|-----------------|
| No WGSL/WebGPU Ising GPU implementation | First WGSL checkerboard Metropolis with validated RNG |
| Most 2D Ising KZM studies use FM model | AF model via staggered equivalence; DWD observable |
| N=20 reps insufficient (Jelic & Cugliandolo) | N=200 (Exp 108) targeting the single-wall regime |
| GPU KZM studies use CUDA/OpenCL | Portable WGSL targeting Apple Metal (consumer hardware) |
| No UKFT/collapse-operator connection | §7 / §10.4: KZM as physical analogue of $\hat{C}$ operator |

---

## 6. Recommended Follow-up Reading

1. **del Campo & Zurek (2014)** — best single-paper KZM review; start here
2. **Jelic & Cugliandolo (2011)** — closest methodological comparison (2D Ising MC)
3. **Preis et al. (2009)** — GPU checkerboard Metropolis (our algorithmic basis)
4. **Francuz et al. (2016)** — finite-size KZM scaling (L vs ξ_KZM regime map)
5. **Biroli et al. (2010)** — coarsening vs KZM distinction in 2D Ising
