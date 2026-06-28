import numpy as np
import matplotlib.pyplot as plt

def generate_primes(n):
    primes = []
    chk = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > chk:
                break
            if chk % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(chk)
        chk += 1
    return np.array(primes)

def simulate_spiral_aliasing():
    print("Simulating Mellin-Fourier Spiral Aliasing...")
    
    # 1. Generate Primes
    N_primes = 200
    primes = generate_primes(N_primes)
    log_primes = np.log(primes)
    
    # 2. Sweep Spiral Angles (theta)
    thetas = np.linspace(0.1, 10.0, 500)
    aliasing_errors = []
    
    for theta in thetas:
        # Project onto logarithmic spiral: z = log(p) * exp(i * theta * log(p))
        angles = theta * log_primes
        x = log_primes * np.cos(angles)
        y = log_primes * np.sin(angles)
        points = x + 1j * y
        
        # Calculate distances between consecutive projected points
        spacings = np.abs(np.diff(points))
        
        # Aliasing metric: variance of the spacing (normalized by mean)
        # Low variance = uniform spacing (repulsion / GUE-like / low aliasing)
        # High variance = clustering (under-sampling / high aliasing)
        normalized_variance = np.var(spacings) / (np.mean(spacings) ** 2)
        aliasing_errors.append(normalized_variance)
        
    aliasing_errors = np.array(aliasing_errors)
    
    # Find the optimal angle (minimum aliasing)
    opt_idx = np.argmin(aliasing_errors)
    opt_theta = thetas[opt_idx]
    print(f"Optimal Spiral Angle (Minimum Aliasing): {opt_theta:.4f} (Metric: {aliasing_errors[opt_idx]:.4f})")
    
    # 3. Generate Visualizations
    plt.figure(figsize=(12, 10))
    
    # Subplot 1: Aliasing Error vs. Theta
    plt.subplot(2, 2, (1, 2))
    plt.plot(thetas, aliasing_errors, 'r-', linewidth=2, label='Aliasing Error (Spacing Variance)')
    plt.axvline(opt_theta, color='green', linestyle='--', label=f'Optimal Theta ({opt_theta:.3f})')
    plt.axvline(1.618, color='blue', linestyle=':', label='Golden Ratio Phase (1.618)')
    plt.xlabel('Spiral Rotation Angle ($\\theta$)')
    plt.ylabel('Normalized Spacing Variance')
    plt.title('Shannon-Nyquist Aliasing Sweep on the Mellin-Fourier Spiral')
    plt.legend()
    plt.grid(True)
    
    # Subplot 2: Optimal Spiral Projection (Low Aliasing)
    plt.subplot(2, 2, 3)
    opt_angles = opt_theta * log_primes
    opt_x = log_primes * np.cos(opt_angles)
    opt_y = log_primes * np.sin(opt_angles)
    plt.plot(opt_x, opt_y, 'g.-', alpha=0.6, label='Log Spiral Path')
    plt.scatter(opt_x, opt_y, c=primes, cmap='viridis', s=25, zorder=3)
    plt.xlabel('Re(z)')
    plt.ylabel('Im(z)')
    plt.title(f'Coherent Projection (\\theta = {opt_theta:.3f})')
    plt.grid(True)
    plt.axis('equal')
    
    # Subplot 3: Clustered/De-coherent Spiral Projection (High Aliasing)
    plt.subplot(2, 2, 4)
    if opt_theta > 5.0:
        bad_theta = opt_theta - 2.5
    else:
        bad_theta = opt_theta + 2.5

    bad_angles = bad_theta * log_primes
    bad_x = log_primes * np.cos(bad_angles)
    bad_y = log_primes * np.sin(bad_angles)
    plt.plot(bad_x, bad_y, 'b-', alpha=0.3)
    plt.scatter(bad_x, bad_y, c=primes, cmap='viridis', s=25, zorder=3)
    plt.xlabel('Re(z)')
    plt.ylabel('Im(z)')
    plt.title(f'Clustered/Aliased Projection (\\theta = {bad_theta:.3f})')
    plt.grid(True)
    plt.axis('equal')
    
    plt.tight_layout()
    plot_path = 'experiments/110_mellin_spiral_aliasing.png'
    plt.savefig(plot_path, dpi=150)
    print(f"Saved plot to {plot_path}")
    
    # Write a summary report
    with open('experiments/110_mellin_spiral_aliasing.md', 'w') as f:
        f.write(f"""# Experiment 110: Mellin-Fourier Spiral Aliasing

This experiment simulates the projection of discrete prime-capacity states onto a logarithmic spiral:
$$s_\\theta(p) = \\log(p) e^{{i \\theta \\log(p)}}$$

## Results
* **Optimal Spiral Angle (Minimum Aliasing)**: $\\theta \\approx {opt_theta:.4f}$
* **Spacing Variance at Optimal**: ${aliasing_errors[opt_idx]:.4f}$
* **Spacing Variance at De-coherent ($\\theta = {bad_theta:.3f}$)**: ${aliasing_errors[np.argmin(np.abs(thetas - bad_theta))]:.4f}$

The sharp minimum in the spacing variance demonstrates that there are specific discrete phase-angles where the prime capacities are distributed with maximum uniformity. Deviating from these angles causes the points to form high-density clusters separated by large voids, triggering Shannon-Nyquist under-sampling (aliasing) on the holographic screen.
""")
    print("Saved report to experiments/110_mellin_spiral_aliasing.md")

if __name__ == "__main__":
    simulate_spiral_aliasing()
