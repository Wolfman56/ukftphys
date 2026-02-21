# Grok Feedback: Physics Check & Proposal Review
**Date:** 2026-02-20
**Reviewer:** Copilot (Internal Execution Agent)
**Source:** `feedback/Grok_4_2_1771617462/tests/proposed_grok_ukft_physics.py`

## 1. Execution Output
The proposed script was executed, yielding the following results:
```text
=== EntropicAction Test (from chat history) ===
Lattice scale: 1 unit = 1.23 TeV
M_crit (lattice): 0.26
Mirror Fermion mass: 0 GeV
P(M=0.26) = 0.0000
P(M=0.50) = 0.9879
```

## 2. Issues Detected (Code Proposal Review)
The proposed implementation of `EntropicAction` contains critical logic errors that contradict the validated Phase 3 results.

### A. Unit Conversion Error (Mass)
*   **The Bug**: The method `physical_mass` returns syntax in **TeV**, but the docstring claims it returns "physical GeV".
    *   Calculation: `0.26 * 1.23 = 0.3198` (TeV).
    *   Formatted Output: `:.0f` rounds 0.32 to `0`.
*   **The Fix**: Multiply by 1000 to convert to GeV.
    ```python
    return M_lattice * self.LATTICE_SCALE_TEV * 1000.0
    ```

### B. Reflection Probability Formula Mismatch
*   **The Bug**: The proposed formula `1 - exp(-k*(M-Mc))` returns `0.0` at critical mass (`M=Mc`).
*   **The requirement**: Phase 3 validation established that at critical mass, the reflection probability must be **0.5 (50%)**.
*   **The Fix**: Use the Sigmoid function (Fermi-Dirac distribution) derived in Phase 3.
    ```python
    return 1.0 / (1.0 + np.exp(self.KAPPA * (M - self.M_CRIT)))
    ```
    *(Note: Sign of kappa might need adjustment depending on definition, but sigmoid is the correct shape).*

## 3. Recommended Actions
1.  **Reject** the proposed code in its current form.
2.  **Use** the structure (Class `EntropicAction`) but **Patch** the methods with the correct logic from Phase 3.
3.  **Instruct** the external agent to output Markdown documentation for proposals in the future, rather than Python scripts that print text.

## 4. Revised `ukft_sim/physics.py` Plan
We will implement `EntropicAction` in `ukft_sim/physics.py` with the following corrected logic:

```python
import numpy as np

class EntropicAction:
    M_CRIT = 0.26
    LATTICE_SCALE_TEV = 1.23
    KAPPA = 18.4

    @classmethod
    def reflection_probability(cls, M_lattice: float) -> float:
        """
        Returns reflection probability P(M).
        At M = M_CRIT, P = 0.5.
        """
        # Sigmoid function for 50% crossing at M_CRIT
        return 1.0 / (1.0 + np.exp(cls.KAPPA * (M_lattice - cls.M_CRIT)))

    @classmethod
    def physical_mass_gev(cls, M_lattice: float) -> float:
        """Returns physical mass in GeV."""
        return M_lattice * cls.LATTICE_SCALE_TEV * 1000.0
```
