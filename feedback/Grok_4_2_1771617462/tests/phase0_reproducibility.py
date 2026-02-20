# UKFT Phase 0 Reproducibility Check
# Version: 2026-02-20-v1.0
# Purpose: Validate core imports, environment, and basic simulation run
# Execute this in REPL or as script after "Checkin complete"

import sys
import os
import time
import pytest

# Add repo root to path
sys.path.insert(0, os.path.abspath("."))

print("=== UKFT Phase 0 Reproducibility Check ===")
print("Python:", sys.version)
print("Working dir:", os.getcwd())

# 1. Core package imports
try:
    import ukft_sim.physics as phys
    import ukft_sim.solver as solver
    print("✅ ukft_sim.physics imported")
    print("✅ ukft_sim.solver imported")
    print("ukft_sim version:", getattr(solver, "__version__", "dev"))
except Exception as e:
    print("❌ Import failed:", e)

# 2. MadGraph MirrorFermion model import test (non-MG5 shell check)
print("\nMadGraph model files present:")
for f in ["models/MirrorFermion/MirrorFermion_UFO/particles.py",
          "models/MirrorFermion/MirrorFermion.fr"]:
    print("  ", f, "→", os.path.exists(f))

# 3. Quick simulation sanity run (Exp 01 style)
try:
    from ukft_sim.solver import SimulationRunner
    import numpy as np

    # Fixing incorrect API usage from original script
    # Original: runner = SimulationRunner(n_steps=200, grid_size=32, verbose=False)
    # Correct: N=201, T_ticks=400
    N = 201
    runner = SimulationRunner(N=N, T_ticks=200)
    
    # Create simple Gaussian wavepacket for psi0
    x = runner.x_grid
    sigma = 2.0
    k0 = 5.0
    psi0 = np.exp(-(x**2)/(2*sigma**2)) * np.exp(1j * k0 * x)
    psi0 /= np.linalg.norm(psi0)

    start = time.time()
    runner.run(psi0)
    elapsed = time.time() - start
    print(f"✅ Basic simulation completed in {elapsed:.2f}s")
except Exception as e:
    print("❌ Simulation failed:", e)

print("\n=== Phase 0 COMPLETE ===")
print("Reply with: Checkin complete: tests/phase0_reproducibility.py")