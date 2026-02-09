# experiments/11_gpu_benchmark.py
import time
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ukft_sim.gpu import EntropicGPUAccelerator

def benchmark():
    print("Initializing GPU...")
    gpu = EntropicGPUAccelerator()
    
    # Setup massive scale
    N_particles = 100_000
    N_sources = 10
    
    print(f"Generating {N_particles} particles and {N_sources} sources...")
    particles_pos = np.random.randn(N_particles, 3).astype(np.float32) * 5.0
    particles_vel = np.random.randn(N_particles, 3).astype(np.float32) * 0.1
    
    sources = []
    for i in range(N_sources):
        pos = np.random.randn(3).astype(np.float32) * 2.0
        mass = 10.0
        sources.append((pos, mass))
        
    params = {
        'sigma': 1.0,
        'alpha': 10.0,
        'dt': 0.01,
        'damping': 0.99
    }
    
    print("Running GPU Simulation (Warmup)...")
    # Warmup
    gpu.run_simulation_step(particles_pos, particles_vel, sources, params)
    
    print("Running Benchmark (100 steps)...")
    t0 = time.time()
    for _ in range(100):
        particles_pos, particles_vel = gpu.run_simulation_step(particles_pos, particles_vel, sources, params)
    t1 = time.time()
    
    dt_avg = (t1 - t0) / 100
    fps = 1.0 / dt_avg
    print(f"Completed 100 steps in {t1-t0:.2f}s")
    print(f"Average Step Time: {dt_avg*1000:.2f}ms")
    print(f"Simulation Speed: {fps:.1f} FPS")
    print(f"Throughput: {N_particles * N_sources * fps / 1e6:.2f} M interactions/sec")

    # Grid Benchmark
    print("\nRunning Grid Benchmark (512x512)...")
    t0 = time.time()
    grid = gpu.compute_density_grid(512, 512, [-5, 5], [-5, 5], sources, 1.0)
    t1 = time.time()
    print(f"Grid Compute Time: {(t1-t0)*1000:.2f}ms")
    print(f"Grid Sum: {np.sum(grid)}")

if __name__ == "__main__":
    benchmark()
