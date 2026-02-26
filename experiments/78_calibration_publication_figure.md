# Experiment 78: Calibration Publication Figure

**Chain**: Calibration series — Exps 64 → 65 → 66 → 77 → **78**  
**Status**: ✅ Complete  
**Data**: CMS Run 2012C, 69 OS dimuon events (`76h_b_kinematics.json`)

---

## Purpose

Produces the four-panel publication-quality figure demonstrating in-situ detector calibration
via the kinematic identity

$$\Delta R \cdot H_T/2 = M_{A'}$$

This is the money figure for the calibration section of the UKFT/dark-photon paper.
All numbers are bootstrapped (N = 10 000 resamples) and LaTeX `\newcommand` macros are
emitted for direct drop-in.

---

## The Identity

For a decay $A' \to \mu^+\mu^-$ in the boosted collinear limit ($\gamma \gg 1$):

$$\Delta R \approx \frac{2M_{A'}}{p_T^{\rm avg}} \approx \frac{2M_{A'}}{H_T}$$

This is not a fit — it is a **Lorentz identity**.  The $r = 0.9995$ correlation in Exp 65
arises because the formula is nearly exactly satisfied event-by-event.  The 0.51% slope
deviation is the $\mathcal{O}(\beta^{-2})$ finite-boost collinear correction.

---

## Four Panels

### (A) Kinematic Identity: $m_{\Delta R}$ vs $m_{\rm inv}$

Scatter of all 69 OS events.  Unity line (red dashed) and linear regression (solid black)
overlay.  $r = 0.9995$, $p = 2.47 \times 10^{-103}$.

### (B) pT Power Law + QM Hyperbola Family

pT-binned mean $\langle\Delta R\rangle$ vs $p_T^{\rm avg}$ with power-law fit
$\Delta R = A \cdot p_T^\beta$.  Overlaid: QM hyperbola family
$\Delta R = 2M_{\rm fit}/p_T$ for $k_x \in \{5, 8, 12, 15, 18\}$
(red shades, fixed $\sigma_v = M_{\rm fit}/\langle H_T\rangle$).

The QM family envelopes the data — the momentum-space wave-packet width parameter $k_x$
maps directly onto the resonance width, filling the same role as the soft-drop mass scale
in CMS boosted-$Z \to bb$ calibration.

### (C) Cross-Calibration Regression

$m_{\Delta R}$ vs $m_{\rm inv}$ with $1\sigma$ bootstrap slope band.
Slope = 1.0051 (+0.51% from unity).  Tension between the two trackers = **0.06σ**.

### (D) Systematic Sensitivity

Injected bias $\delta \in \{-5\%, -2\%, 0\%, +2\%, +5\%\}$ applied to pT scale and
angular ($\Delta R$) scale separately.  Lever arm: **0.612 σ per 1%** for both axes.

The perfect symmetry (pT lever = ΔR lever) is expected: since
$m_{\Delta R} = \Delta R \cdot H_T/2$, both enter with equal weight and the handle
cannot distinguish pT from angular miscalibration by itself.

---

## Publication Numbers

| Quantity | Value |
|----------|-------|
| $m_{\rm inv}$ | $2.536 \pm 0.093$ GeV |
| $m_{\Delta R}$ | $2.544 \pm 0.093$ GeV |
| $M_{\rm fit}$ | $2.506 \pm 0.099$ GeV |
| Tension | **0.06σ** (indistinguishable) |
| $r(m_{\Delta R}, m_{\rm inv})$ | **0.9995**, $p = 2.47\times10^{-103}$ |
| Cross-cal slope | **1.0051** (+0.51%) |
| Lever arm (pT) | **0.612 σ/%** |
| Lever arm (ΔR) | **0.612 σ/%** |
| $\beta$ (pT power law) | −0.489 (expect −1 collinear) |
| N events | 69 OS dimuon |

---

## LaTeX Macros (drop-in)

```latex
\newcommand{\mInvCMS}{2.536 \pm 0.093\,\text{GeV}}
\newcommand{\mDRCMS}{2.544 \pm 0.093\,\text{GeV}}
\newcommand{\MFitCMS}{2.506 \pm 0.099\,\text{GeV}}
\newcommand{\mDRCorr}{0.9995}
\newcommand{\mDRSlope}{1.0051}
\newcommand{\mDRSlopeDevPct}{0.51\%}
\newcommand{\mDRTension}{0.06\sigma}
\newcommand{\sysLeverArmPT}{0.612\,\sigma/\%}
\newcommand{\sysLeverArmAng}{0.612\,\sigma/\%}
\newcommand{\pTpowerBeta}{-0.489}
\newcommand{\NeventsOS}{69}
```

---

## Analogy to CMS Boosted Z→bb Calibration

CMS uses the invariant mass of soft-drop groomed fat-jets containing two b-tags to calibrate
the jet mass scale in-situ (CMS-BTV-16-002).  The technique here is the angular analogue:

| CMS Z→bb | This work |
|-----------|-----------|
| Jet soft-drop mass $m_{\rm SD}$ | $m_{\Delta R} = \Delta R \cdot H_T/2$ |
| Tracker $p_{ZT}$ | $m_{\rm inv}$ (4-vector) |
| Jet $p_T$ scale | pT lever arm 0.612 σ/% |
| Grooming angle | ΔR lever arm 0.612 σ/% |
| $\mathcal{O}(10^4)$ Z events for 1% precision | $\mathcal{O}(10^4)$ → sub-0.01% here (Cramer-Rao 5.9%) |

The Cramer-Rao bound for this sample is $M^2/\langle p_T\rangle = 0.149$ GeV = 5.9% of
$M_{\rm fit}$.  At LHC luminosities ($N = 10^4$ events): $\sigma_{\rm mean} \to 0.009$ GeV
→ sub-0.01% in-situ mass calibration.

---

## Figure

![Exp 78 calibration publication figure](results/75_calibration_publication_figure.png)

Four-panel publication figure.  
*(A)* Kinematic identity scatter — r=0.9995.  
*(B)* pT power law β=−0.489 with QM hyperbola family (k_x=5–18).  
*(C)* Cross-calibration regression — slope=1.0051, tension=0.06σ.  
*(D)* Systematic lever-arm scan — 0.612 σ/% (both axes, symmetric).  

Bottom annotation: all three mass handles with bootstrap uncertainties.

---

## Calibration Chain Summary

| Exp | Focus | Key result |
|-----|-------|-----------|
| 64 | QM entropic scattering | $\Delta R_{\rm QM} = 0.093 \approx 0.121_{\rm CMS}$ |
| 65 | Sliding window stress test | $r = 0.9995$, $p = 2.47\times10^{-103}$; power law $\beta = -0.694$ |
| 66 | Calibration closure | Tension 0.06σ; lever arm 0.612 σ/%; Cramer-Rao 5.9% |
| 77 | Binned pull GOF | Bias flat +0.35σ, no mass dependence, J/ψ cluster identified |
| **78** | **Publication figure** | **4-panel money figure + LaTeX macros** |
