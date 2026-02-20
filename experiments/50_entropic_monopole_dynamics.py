import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import os

# Create results directory
os.makedirs("results", exist_ok=True)

class EntropicMonopoleDynamics:
    def __init__(self, size=24):
        self.size = size
        self.phi = np.zeros((size, size, size, 3))
        self.vel = np.zeros((size, size, size, 3))
        self.center = size / 2.0
        
        # Initialize Hedgehog Configuration (Stable Monopole)
        self.initialize_hedgehog()
        
    def initialize_hedgehog(self):
        """Create the static topological defect (Hedgehog)."""
        x, y, z = np.indices((self.size, self.size, self.size))
        
        rx = x - self.center
        ry = y - self.center
        rz = z - self.center
        
        r_mag = np.sqrt(rx**2 + ry**2 + rz**2)
        r_mag[r_mag == 0] = 1e-6 # Avoid division by zero
        
        # Unit vector field n = r / |r|
        self.phi[..., 0] = rx / r_mag
        self.phi[..., 1] = ry / r_mag
        self.phi[..., 2] = rz / r_mag
        
        # Initial Velocities are zero
        self.vel[:] = 0.0

    def evolve(self, steps=1000, dt=0.05, probe_point=(6,6,6)):
        """
        Evolve the field using the O(3) Sigma Model dynamics.
        Lagrangian: L = 1/2 (d_t phi)^2 - 1/2 (grad phi)^2
        Constraint: |phi| = 1
        """
        energy_history = []
        radiation_signal = [] # Field value at probe point
        
        # Pre-compute neighbors for Laplacian
        # Using 6-point stencil
        
        for t in range(steps):
            # 1. Update Position (Half Step)
            # phi(t+dt/2) = phi(t) + vel(t) * dt/2
            # But constraint |phi|=1 must be maintained.
            # We use a projection method or a Lagrange multiplier.
            # Simple Verlet with Projection:
            
            # Laplacian (Force)
            laplacian = (
                np.roll(self.phi, 1, axis=0) + np.roll(self.phi, -1, axis=0) +
                np.roll(self.phi, 1, axis=1) + np.roll(self.phi, -1, axis=1) +
                np.roll(self.phi, 1, axis=2) + np.roll(self.phi, -1, axis=2) -
                6 * self.phi
            )
            
            # Perturbation at t=0 (Kick the core)
            if t == 0:
                core_slice = tuple([slice(int(self.center)-1, int(self.center)+2)] * 3)
                self.vel[core_slice] += np.random.normal(0, 5.0, self.vel[core_slice].shape)
            
            # Acceleration = Laplacian (Wave Equation)
            # Constraint force is directed along phi to keep |phi|=1
            # F_constraint = - (vel^2 + phi*Laplacian) * phi  (roughly)
            # Simpler: Unconstrained step -> Normalize
            
            # Velocity Verlet Integration (Naive Projection)
            force = laplacian
            
            # v(t+1/2) = v(t) + 0.5 * a(t) * dt
            self.vel += 0.5 * force * dt
            
            # x(t+1) = x(t) + v(t+1/2) * dt
            self.phi += self.vel * dt
            
            # Renormalize to enforce O(3) constraint |phi|=1
            # This is dissipatively equivalent to infinite stiffness
            norms = np.linalg.norm(self.phi, axis=3, keepdims=True)
            self.phi /= norms
            
            # Re-calculate Force (Laplacian) at new position
            new_laplacian = (
                np.roll(self.phi, 1, axis=0) + np.roll(self.phi, -1, axis=0) +
                np.roll(self.phi, 1, axis=1) + np.roll(self.phi, -1, axis=1) +
                np.roll(self.phi, 1, axis=2) + np.roll(self.phi, -1, axis=2) -
                6 * self.phi
            )
            
            # v(t+1) = v(t+1/2) + 0.5 * a(t+1) * dt
            self.vel += 0.5 * new_laplacian * dt
            
            # Remove radial component of velocity to keep it tangent to sphere
            # v_tangent = v - (v . phi) * phi
            v_dot_phi = np.sum(self.vel * self.phi, axis=3, keepdims=True)
            self.vel -= v_dot_phi * self.phi
            
            # Record Data
            # Measure fluctuations at probe point (Magnitude of deviation from equilibrium?)
            # Just taking the x-component at probe
            signal = self.phi[probe_point][0]
            radiation_signal.append(signal)

            # Measure Kinetic Energy
            kin_en = 0.5 * np.sum(self.vel**2)
            energy_history.append(kin_en)
            
        return np.array(radiation_signal), np.array(energy_history)

def analyze_spectrum(signal, dt=0.05):
    """
    Perform FFT on the radiation signal and fit to Planck Law.
    """
    n = len(signal)
    yf = fft(signal)
    xf = fftfreq(n, dt)[:n//2]
    power = 2.0/n * np.abs(yf[0:n//2])
    
    # Fit Candidates:
    # 1. Planck: E^3 / (exp(E/T) - 1)
    # 2. Bremsstrahlung/Power Law: 1/E
    # 3. Resonance: Lorentzian
    
    return xf, power

if __name__ == "__main__":
    print("Initializing Experiment 50: Entropic Monopole Dynamics...")
    
    sim = EntropicMonopoleDynamics(size=30)
    print("Simulating Monopole 'Ringdown' (Core Perturbation)...")
    
    signal, energy = sim.evolve(steps=2000, dt=0.05)
    
    # Remove DC offset / trend
    signal = signal - np.mean(signal)
    
    # Analyze
    freqs, power = analyze_spectrum(signal, dt=0.05)
    
    # Filter out very low freq (artifacts)
    mask = (freqs > 0.1) & (freqs < 5.0)
    freqs_fit = freqs[mask]
    power_fit = power[mask]
    
    # Plotting
    plt.figure(figsize=(12, 10))
    
    # Time Series
    plt.subplot(2, 1, 1)
    plt.plot(signal, label='Field Fluctuation at Probe (r=6)', color='blue', alpha=0.7)
    plt.title('Time Domain: Monopole "Ringdown" Signal')
    plt.xlabel('Time Steps')
    plt.ylabel('Field Amplitude $\phi_x$')
    plt.grid(True, alpha=0.3)
    
    # Frequency Domain
    plt.subplot(2, 1, 2)
    plt.plot(freqs, power, label='Power Spectrum', color='black')
    plt.xlim(0, 4.0)
    
    # Theoretical Curves Overlay
    # 1. Planck (Thermal)
    # Fit Temperature T roughly to peak
    # Peak of Planck x^3/(e^x-1) is ~2.82 T
    peak_freq = freqs_fit[np.argmax(power_fit)]
    T_fit = peak_freq / 2.82
    
    def planck(f, T):
        return 1e-1 * (f**3) / (np.exp(f/T) - 1 + 1e-9) # Scaled
    
    # 2. Resonance (Breit-Wigner)
    def lorentzian(f, f0, gamma):
        return 1e-2 / ((f - f0)**2 + (gamma/2)**2)
    
    # Normalize curves to peak power
    scale_factor = np.max(power_fit)
    
    # Planck Curve
    p_curve = planck(freqs, T_fit)
    p_curve = p_curve * (scale_factor / np.max(p_curve))
    
    # Lorentzian Curve
    l_curve = lorentzian(freqs, peak_freq, 0.5)
    l_curve = l_curve * (scale_factor / np.max(l_curve))
    
    plt.plot(freqs, p_curve, '--', label=f'Thermal Fit (Planck) T={T_fit:.2f}', color='red')
    plt.plot(freqs, l_curve, ':', label=f'Resonance Fit (Particle) f0={peak_freq:.2f}', color='green')
    
    plt.title('Frequency Domain: Spectral Analysis')
    plt.xlabel('Frequency $\omega$')
    plt.ylabel('Power')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/50_monopole_dynamics_spectrum.png')
    print("Simulation Complete. Spectrum saved to results/50_monopole_dynamics_spectrum.png")
