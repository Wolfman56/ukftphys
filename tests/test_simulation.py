
import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ukft_sim.solver import SimulationRunner

class TestSimulationRunner(unittest.TestCase):
    def test_run_basic(self):
        """Test SimulationRunner.run with basic settings"""
        N = 51
        sim = SimulationRunner(N=N, T_ticks=50, M_particles=100)
        
        # Initial Wavepacket
        x = sim.x_grid
        x0 = 0.0
        sigma = 10.0
        psi0 = np.exp(-(x-x0)**2 / (2*sigma**2))
        psi0 /= np.sqrt(np.sum(np.abs(psi0)**2))
        
        results = sim.run(psi0)
        
        self.assertIn('choice_indices', results)
        self.assertIn('history_rho', results)
        self.assertIn('history_pos', results)
        
        # Check shapes
        self.assertEqual(results['history_rho'].shape, (50, N))
        self.assertEqual(results['history_pos'].shape, (50, 100)) # M_particles
    
    def test_run_potential_barrier(self):
        """Test SimulationRunner.run with potential barrier"""
        N = 51
        sim = SimulationRunner(N=N, T_ticks=20, M_particles=50)
        
        V = np.zeros(N)
        V[25] = 10.0 # Barrier at center
        
        psi0_left = np.exp(-(sim.x_grid+10)**2/10)
        psi0_left /= np.sqrt(np.sum(psi0_left**2))
        
        results = sim.run(psi0_left, potential_barrier=V)
        
        # Can check if density is suppressed in barrier region?
        # Just check it ran without error
        self.assertEqual(len(results['history_rho']), 20)

if __name__ == '__main__':
    unittest.main()
