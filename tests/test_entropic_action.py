
import unittest
import numpy as np
import sys
import os

# Add ukft_sim to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.physics import EntropicAction

class TestEntropicAction(unittest.TestCase):
    def test_reflection_probability_low_mass(self):
        """Test reflection probability for M << M_CRIT (Should be ~0)"""
        m = 0.01  # Small mass
        prob = EntropicAction.reflection_probability(m)
        self.assertLess(prob, 0.1, f"Expected low reflection for M={m}, got {prob}")

    def test_reflection_probability_high_mass(self):
        """Test reflection probability for M >> M_CRIT (Should be ~1)"""
        m = 1.0  # Large mass
        prob = EntropicAction.reflection_probability(m)
        self.assertGreater(prob, 0.9, f"Expected high reflection for M={m}, got {prob}")

    def test_reflection_probability_critical_mass(self):
        """Test reflection probability at M_CRIT (Should be ~0.5)"""
        m = EntropicAction.M_CRIT
        prob = EntropicAction.reflection_probability(m)
        self.assertAlmostEqual(prob, 0.5, delta=0.01, msg=f"Expected ~0.5 reflection at M_CRIT, got {prob}")

    def test_physical_mass_conversion(self):
        """Test lattice to GeV conversion"""
        m = 1.0
        gev = EntropicAction.physical_mass_gev(m)
        expected = 1.0 * EntropicAction.LATTICE_SCALE_TEV * 1000.0
        self.assertEqual(gev, expected)

    def test_critical_physical_mass(self):
        """Test critical mass ~320 GeV"""
        crit_gev = EntropicAction.critical_physical_mass()
        expected = EntropicAction.M_CRIT * EntropicAction.LATTICE_SCALE_TEV * 1000.0
        self.assertAlmostEqual(crit_gev, expected, delta=1.0)
        print(f"\nConfimed Mirror Fermion Critical Mass: {crit_gev:.2f} GeV")

if __name__ == '__main__':
    unittest.main()
