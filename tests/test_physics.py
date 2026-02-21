
import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.physics import get_quantum_potential, get_velocity_field

class TestPhysicsFunctions(unittest.TestCase):

    def test_get_quantum_potential_flat(self):
        """Test Quantum Potential for a flat wavefunction (V=0)"""
        psi = np.ones(10)
        V_q = get_quantum_potential(psi, t_hop=1.0)
        # For constant psi, R'' is 0, so V_q should be 0
        np.testing.assert_allclose(V_q, 0.0, atol=1e-12)

    def test_get_quantum_potential_gaussian(self):
        """Test Quantum Potential for a Gaussian"""
        x = np.linspace(-5, 5, 100)
        psi = np.exp(-x**2/2)
        # Check output shape
        V_q = get_quantum_potential(psi, t_hop=1.0)
        self.assertEqual(V_q.shape, psi.shape)
        # Check positive curvature (repulsive) near center?
        # Gaussian R = exp(-x^2/2). R'' = (x^2 - 1) * R.
        # V_q ~ - R''/R ~ -(x^2 - 1). 
        # Center x=0 -> V_q ~ +1. Correct.
        center_idx = 50
        self.assertTrue(V_q[center_idx] > 0) # Expect positive potential at peak curvature

    def test_get_velocity_field_zero(self):
        """Test Velocity Field for real wavefunction (v=0)"""
        psi = np.exp(-np.linspace(-5, 5, 100)**2)
        v = get_velocity_field(psi, t_hop=1.0)
        np.testing.assert_allclose(v, 0.0, atol=1e-12)
    
    def test_get_velocity_field_moving(self):
        """Test Velocity Field for plane wave (constant v)"""
        x = np.arange(100)
        k = 0.5
        psi = np.exp(1j * k * x)
        v = get_velocity_field(psi, t_hop=1.0)
        # J_bond ~ 2 * t * Im(psi* psi_next)
        # psi[i]*psi[i+1] = exp(-ikx) * exp(i k(x+1)) = exp(ik)
        # Im(exp(ik)) = sin(k)
        # v = 2 * t * sin(k) / |1|^2 = 2 * t * sin(k)
        expected = 2.0 * 1.0 * np.sin(k)
        # Allow small deviation due to boundary effects or roll
        np.testing.assert_allclose(v[1:-1], expected, rtol=1e-5)

if __name__ == '__main__':
    unittest.main()
