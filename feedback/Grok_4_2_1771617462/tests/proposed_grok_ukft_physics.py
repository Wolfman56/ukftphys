# UKFT Core Physics Module
# Version: 2026-02-20-v1.0
# Contains centralized EntropicAction and reflection_probability (from chat Feb 19)

import numpy as np

# Global constants (from Exp 30-31 calibration)
LATTICE_SCALE_TEV = 1.23
M_CRIT = 0.26
KAPPA = 18.4

class EntropicAction:
    """
    Central class for all entropic action calculations.
    Directly from Mirror Fermion derivation (chat Feb 19).
    """
    def __init__(self):
        self.M_CRIT = M_CRIT
        self.KAPPA = KAPPA
        self.LATTICE_SCALE_TEV = LATTICE_SCALE_TEV

    def reflection_probability(self, M: float) -> float:
        """
        Reflection probability P(M) from local entropic action minimization.
        Exact formula used in 35_Entropic_Unification.md and 36_Mirror_Fermion_Paper.md.
        """
        if M <= self.M_CRIT:
            return 0.0
        return 1 - np.exp(-self.KAPPA * (M - self.M_CRIT))

    def physical_mass(self, M_lattice: float) -> float:
        """Convert lattice mass to physical GeV."""
        return M_lattice * self.LATTICE_SCALE_TEV

    def critical_physical_mass(self) -> float:
        """Returns 320 GeV (the Mirror Fermion prediction)."""
        return self.physical_mass(self.M_CRIT)

# Convenience instance
entropic = EntropicAction()

# Backward-compatible function for existing scripts
def reflection_probability(M: float) -> float:
    """Global convenience wrapper (exactly as used in Phase 1 script)."""
    return entropic.reflection_probability(M)

# Example usage (run in REPL)
if __name__ == "__main__":
    print("=== EntropicAction Test (from chat history) ===")
    print(f"Lattice scale: 1 unit = {LATTICE_SCALE_TEV} TeV")
    print(f"M_crit (lattice): {M_CRIT}")
    print(f"Mirror Fermion mass: {entropic.critical_physical_mass():.0f} GeV")
    print(f"P(M=0.26) = {reflection_probability(0.26):.4f}")
    print(f"P(M=0.50) = {reflection_probability(0.50):.4f}")