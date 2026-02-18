import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

class UKFTBlackHoleSimulator:
    def __init__(self, size=100, resolution=1.0):
        self.size = size
        self.res = resolution
        self.x = np.linspace(-size/2, size/2, int(size*resolution))
        self.y = np.linspace(-size/2, size/2, int(size*resolution))
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # Physics Constants
        self.c = 1.0  # Speed of light/causality
        self.G_entropic = 2.5 # Entropic Gravity Strength
        self.rho_max = 5.0    # SATURATION LIMIT (The "Event Horizon")
        self.rho_crit = 0.95 * self.rho_max # Warning zone
        
        # Black Hole Setup (Gaussian Choice Density)
        self.R_s = 10.0 # Schwarzschild Radius approx
        self.rho_field = self._init_black_hole()
        
        # Particles (Light Rays)
        self.particles = []
        self.history = []

    def _init_black_hole(self):
        # Create a massive Gaussian density well
        # In UKFT, "Mass" is just high information density
        r2 = self.X**2 + self.Y**2
        rho = 15.0 * np.exp(-r2 / (2 * self.R_s**2))
        return rho

    def add_photon_swarm(self, n_photons=50, x_start=-40):
        # Create a wall of photons moving right
        ys = np.linspace(-40, 40, n_photons)
        for y in ys:
            self.particles.append({
                'r': np.array([x_start, y], dtype=float),
                'v': np.array([1.0, 0.0], dtype=float) * self.c, # Moving Right
                'alive': True,
                'path': []
            })
            
    def get_gradient_log_rho(self, pos):
        # Calculate Entropic Force: F = grad(ln(rho))
        # rho(r) = A * exp(-r^2 / 2s^2)
        # ln(rho) = ln(A) - r^2 / 2s^2
        # grad(ln rho) = -r / s^2 ==> Harmonic Oscillator / Hooke's Law attraction!
        # But wait, UKFT typically uses 1/r potential for emergent gravity?
        # Let's use the raw gradient of the field we constructed.
        
        # Interpolate grad based on grid? Or analytical?
        # Analytical is smoother for simulation.
        x, y = pos
        r2 = x**2 + y**2
        
        # Check Saturation Limit
        # If density is too high, the gradient should REVERSE (Mirror Effect)
        # or become a hard wall.
        
        local_rho = 15.0 * np.exp(-r2 / (2 * self.R_s**2))
        
        if local_rho > self.rho_max:
             # MIRROR EFFECT: The force becomes repulsive!
             # This simulates the "Causal Graph is Full" pressure.
             return -1.0 * (-np.array([x, y]) / self.R_s**2) # Push OUT
        
        # Normal Entropic Gravity (Pull IN)
        # grad(ln rho) = -r vector / sigma^2
        return (-np.array([x, y]) / self.R_s**2)

    def step(self, dt=0.5):
        for p in self.particles:
            if not p['alive']: continue
            
            p['path'].append(p['r'].copy())
            
            # 1. Calculate Acceleration (Entropic Gravity + Curvature)
            # F = alpha * grad(ln rho)
            force_dir = self.get_gradient_log_rho(p['r'])
            acc = self.G_entropic * force_dir
            
            # 2. Update Velocity (Kick)
            p['v'] += acc * dt
            
            # 3. Enforce Speed Limit (c)
            v_mag = np.linalg.norm(p['v'])
            if v_mag > self.c:
                p['v'] = (p['v'] / v_mag) * self.c
                
            # 4. Update Position (Drift)
            p['r'] += p['v'] * dt
            
            # 5. Check Boundary / Horizon
            x, y = p['r']
            r_curr = np.sqrt(x**2 + y**2)
            local_rho = 15.0 * np.exp(-(r_curr**2) / (2 * self.R_s**2))
            
            # Event Horizon Visualization
            if local_rho > self.rho_max:
                p['status'] = 'REFLECTED'
                # Simple elastic bounce off the "Solid Vacuum"
                # In full UKFT this is a Causal Reversal, here we model as bounce
                normal = -p['r'] / r_curr
                p['v'] = p['v'] - 2 * np.dot(p['v'], normal) * normal
                # Push out slightly to avoid getting stuck
                p['r'] += p['v'] * dt * 2.0
                
            if abs(x) > self.size/2 or abs(y) > self.size/2:
                p['alive'] = False

    def run(self, steps=200):
        print(f"Running UKFT Black Hole Simulation ({steps} steps)...")
        for i in range(steps):
             self.step()
        print("Simulation complete.")

    def plot(self):
        plt.figure(figsize=(10, 8))
        ax = plt.gca()
        
        # 1. Plot Density Field (The "Hole")
        # Mask the central region where rho > rho_max (The Mirror)
        masked_rho = np.ma.masked_where(self.rho_field > self.rho_max, self.rho_field)
        
        # Plot the "Halo" (Vacuum Filaments)
        plt.contourf(self.X, self.Y, self.rho_field, levels=50, cmap='inferno', alpha=0.3)
        
        # Plot the "Mirror Horizon" (Solid Sphere)
        circle = plt.Circle((0, 0), self.R_s * np.sqrt(2*np.log(15.0/self.rho_max)), 
                           color='black', fill=True, label='Event Horizon (Mirror)')
        ax.add_patch(circle)
        
        # Add a shiny rim to the mirror
        circle_rim = plt.Circle((0, 0), self.R_s * np.sqrt(2*np.log(15.0/self.rho_max)), 
                               color='cyan', fill=False, linewidth=2, linestyle='--', label='Causal Boundary')
        ax.add_patch(circle_rim)

        # 2. Plot Photon Trajectories
        for i, p in enumerate(self.particles):
            path = np.array(p['path'])
            if len(path) > 1:
                # Color code: Yellow=Light, Red=Lensed/HighAccel?
                plt.plot(path[:,0], path[:,1], color='gold', linewidth=0.8, alpha=0.6)
                
                # Plot intersection points?
        
        plt.title("Visualizing a UKFT 'Black Hole': The Causal Mirror")
        plt.xlabel("Space X")
        plt.ylabel("Space Y")
        plt.legend(loc='upper right')
        plt.xlim(-50, 50)
        plt.ylim(-50, 50)
        plt.grid(True, linestyle=':', alpha=0.3)
        
        # Save
        filename = "results/33_ukft_black_hole_visualizer.png"
        plt.savefig(filename, dpi=150)
        print(f"Saved visualization to {filename}")
        plt.close()

if __name__ == "__main__":
    sim = UKFTBlackHoleSimulator()
    sim.add_photon_swarm(n_photons=40, x_start=-45)
    sim.run(steps=300)
    sim.plot()

