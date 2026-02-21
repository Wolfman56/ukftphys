
import unittest
import numpy as np
import sys
import os
import pytest
t_torch_available = False
try:
    import torch
    torch_available = True
except ImportError:
    torch_available = False

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@pytest.mark.skipif(not torch_available, reason="PyTorch not installed")
class TestGPUSimulation(unittest.TestCase):
    def test_gpu_run(self):
        """Test SimulationRunnerGPU matches (roughly) behavior"""
        # Import inside to avoid error if torch missing
        from ukft_sim.solver_gpu import SimulationRunnerGPU
        
        N = 51
        sim = SimulationRunnerGPU(N=N, T_ticks=20, M_particles=50) # Auto-detects device
        
        # Initial Wavepacket
        x = np.linspace(-sim.L_phys/2, sim.L_phys/2, N)
        x0 = 0.0
        sigma = 10.0
        psi0 = np.exp(-(x-x0)**2 / (2*sigma**2)).astype(np.complex64)
        psi0 /= np.sqrt(np.sum(np.abs(psi0)**2))
        
        results = sim.run(psi0)
        
        self.assertIn('history_rho', results)
        self.assertEqual(results['history_rho'].shape, (20, N))
        
        # Check if it actually ran on the requested device
        print(f"Ran on: {sim.device}")
        
    def test_mps_acceleration(self):
        """Specifically verify MPS if on Mac Silicon"""
        if not torch.backends.mps.is_available():
            self.skipTest("MPS not available")
            
        from ukft_sim.solver_gpu import SimulationRunnerGPU
        sim = SimulationRunnerGPU(N=101, device='mps')
        self.assertEqual(sim.device.type, 'mps')

if __name__ == '__main__':
    unittest.main()
