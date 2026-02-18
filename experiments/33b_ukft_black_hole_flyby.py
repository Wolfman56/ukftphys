
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

class UKFTBlackHoleFlyby:
    def __init__(self, resolution=150, frames=60): # 150x150 res
        self.res = resolution
        self.frames = frames
        self.size = 20.0
        self.R_s = 2.0   
        self.c = 1.0 # Speed of light/causality
        
        # Camera Grid (View Plane)
        self.x = np.linspace(-self.size/2, self.size/2, self.res)
        self.y = np.linspace(-self.size/2, self.size/2, self.res)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # Precompute Background Texture (Space-Time Fabric)
        # We model the background as a "Cosmic Web" at Z=Infinity
        # Simple grid + noise
        self.bg_texture = np.zeros((self.res*2, self.res*2, 3)) # Larger BG to handle deflection
        # Add grid lines
        grid_spacing = 20
        self.bg_texture[::grid_spacing, :, :] = [0.0, 0.2, 0.5] # Blue lines
        self.bg_texture[:, ::grid_spacing, :] = [0.0, 0.2, 0.5]
        # Add stars
        np.random.seed(42)
        random_stars = np.random.rand(self.res*2, self.res*2) > 0.99
        self.bg_texture[random_stars] = [1.0, 1.0, 1.0]

    def render_frame(self, frame_idx):
        # 1. Update Black Hole Position (Moving Left -> Right across view)
        t = frame_idx / self.frames
        bh_pos_screen = np.array([-15.0 + 30.0 * t, 0.0]) 
        
        # 2. Ray Tracing Geometry
        # Vector from BH center to Pixel on Screen
        rx = self.X - bh_pos_screen[0]
        ry = self.Y - bh_pos_screen[1]
        r_sq = rx**2 + ry**2
        r = np.sqrt(r_sq)
        
        # 3. Mask Horizon (The Mirror Core)
        # In UKFT Exp 33, rho > rho_max acts as a PERFECT REFLECTOR.
        # We render it as a glossy metallic sphere.
        mask_horizon = r < self.R_s
        
        # 4. Lensing Deflection (Outside the Horizon)
        # Approximating deflection angle alpha ~ 4GM/c^2 * 1/b
        # On screen displacement: delta_theta ~ 1/b
        # We shift the "lookup coordinates" on the background texture.
        # LENS_STRENGTH constant
        LENS = 8.0 
        # Displace outward from center
        defl_x = -rx / (r_sq + 0.1) * LENS
        defl_y = -ry / (r_sq + 0.1) * LENS
        
        # Calculate lookup coordinates on background texture
        # Map Screen [-10, 10] to texture indices [0, 2*res]
        # Base coords
        u = (self.X + self.size/2) / self.size * self.res # 0..res
        v = (self.Y + self.size/2) / self.size * self.res # 0..res
        
        # Distorted coords
        u_dist = u + defl_x * (self.res / self.size)
        v_dist = v + defl_y * (self.res / self.size)
        
        # Clamp/Wrap indices
        u_idx = np.clip(u_dist.astype(int), 0, self.res - 1)
        v_idx = np.clip(v_dist.astype(int), 0, self.res - 1)
        
        # 5. Build Image
        img = np.zeros((self.res, self.res, 3))
        
        # Procedural Background Sampling (Grid + Noise)
        # Instead of sampling texture (hard with distortion), generate pattern on fly
        # Grid function of Distorted Coords
        grid_x = (np.abs(self.X + defl_x) % 2.0) < 0.1
        grid_y = (np.abs(self.Y + defl_y) % 2.0) < 0.1
        on_grid = grid_x | grid_y
        
        img[on_grid] = [0.0, 0.3, 0.7] # Warped Grid Lines (Cyan-Blue)
        
        # Star Noise
        star_val = (np.sin((self.X + defl_x)*5) * np.cos((self.Y + defl_y)*5))
        img[star_val > 0.9] = [1.0, 1.0, 1.0] # Warped Stars
        
        # 6. Render The "Mirror" (Horizon)
        # Reflective core.
        # Simple shader: Sphere normal dot Light source
        # Normal vector N = (rx, ry, z) / R
        # Use simple gradient
        sphere_shade = np.clip(1.0 - (r[mask_horizon] / self.R_s)**2, 0, 1)
        img[mask_horizon, 0] = sphere_shade * 0.1 # Dark
        img[mask_horizon, 1] = sphere_shade * 0.9 # Cyan Glow
        img[mask_horizon, 2] = sphere_shade * 1.0 # White Center
        
        # 7. Render Photon Ring (Accretion Edge)
        # Just outside R_s
        mask_ring = (r > self.R_s) & (r < self.R_s * 1.15)
        ring_intensity = (1.0 - (r[mask_ring] - self.R_s)/(self.R_s*0.15))
        img[mask_ring] = [1.0, 0.8, 0.2] * ring_intensity[:, np.newaxis]

        return img, bh_pos_screen

    def animate(self):
        fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
        ax.set_axis_off()
        img_buffer = np.zeros((self.res, self.res, 3))
        im = ax.imshow(img_buffer, origin='lower', extent=[-10, 10, -10, 10])
        
        def update(frame):
            img_data, bh_pos = self.render_frame(frame)
            im.set_data(img_data)
            ax.set_title(f"UKFT Black Hole Flyby: The Causal Mirror", color='white', pad=10)
            return [im]

        print(f"Rendering {self.frames} frames...")
        ani = FuncAnimation(fig, update, frames=self.frames, blit=True)
        save_path = "results/33b_ukft_black_hole_flyby.gif"
        ani.save(save_path, writer='pillow', fps=15)
        print(f"Animation saved to {save_path}")

if __name__ == "__main__":
    sim = UKFTBlackHoleFlyby(resolution=200, frames=60)
    sim.animate()
