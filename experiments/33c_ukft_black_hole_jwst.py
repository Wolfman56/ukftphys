
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os
from scipy.ndimage import gaussian_filter

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

class UKFTBlackHoleJWST:
    def __init__(self, resolution=200, frames=60): 
        self.res = resolution
        self.frames = frames
        self.size = 20.0
        self.R_s = 2.5 # Slightly larger event horizon
        
        # Camera Grid
        self.x = np.linspace(-self.size/2, self.size/2, self.res)
        self.y = np.linspace(-self.size/2, self.size/2, self.res)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # Generate Synthetic JWST Deep Field Background
        print("Generating Synthetic JWST Deep Field Background...")
        self.bg_texture = self._generate_jwst_background()

    def _generate_jwst_background(self):
        # Create a high-res canvas (2x simulation res to handle aliasing/lensing)
        canvas_res = self.res * 3
        canvas = np.zeros((canvas_res, canvas_res, 3))
        
        # 1. Thousands of faint distant galaxies (The "Noise")
        num_galaxies = 2000
        x_g = np.random.randint(0, canvas_res, num_galaxies)
        y_g = np.random.randint(0, canvas_res, num_galaxies)
        
        # Colors: Redshifted (Orange/Red) to Blue/White
        colors = np.random.rand(num_galaxies, 3)
        colors[:, 0] = 0.5 + 0.5 * colors[:, 0] # High Red channel
        colors[:, 2] *= 0.3 # Low Blue channel (High Redshift)
        
        canvas[y_g, x_g] = colors * 0.4 # Faint
        
        # Blur to make them blobs not pixels
        canvas = gaussian_filter(canvas, sigma=0.8)
        
        # 2. Add Bright Foreground Stars with Diffraction Spikes (JWST Style)
        # JWST has 6-pointed spikes + 2 horizontal
        num_stars = 15
        for _ in range(num_stars):
            cx, cy = np.random.randint(20, canvas_res-20, 2)
            brightness = np.random.uniform(0.8, 1.5)
            # Star Core
            canvas[cy, cx] = [1.0, 1.0, 1.0] 
            
            # Diffraction Spikes (Line drawing)
            # Angles: 90, 210, 330 (3 main axes for hexagon?) 
            # Real JWST: Vertical + X shape? 
            # Let's do a 6-point star
            length = np.random.randint(10, 40)
            angles = [0, 60, 120, 180, 240, 300]
            for ang in angles:
                rad_ang = np.radians(ang)
                dx = np.cos(rad_ang)
                dy = np.sin(rad_ang)
                for r in range(1, length):
                    px = int(cx + r * dx)
                    py = int(cy + r * dy)
                    if 0 <= px < canvas_res and 0 <= py < canvas_res:
                        falloff = (1 - r/length)**2
                        # Blue-ish spikes
                        canvas[py, px] += np.array([0.5, 0.7, 1.0]) * brightness * falloff * 0.8 / (r**0.5)

        # 3. Add a few "Spiral Galaxies" (Ellipses)
        num_spirals = 5
        for _ in range(num_spirals):
            cx, cy = np.random.randint(50, canvas_res-50, 2)
            a, b = np.random.randint(3, 10, 2)
            theta = np.random.uniform(0, np.pi)
            
            # Draw ellipse manually-ish
            Y, X = np.ogrid[:canvas_res, :canvas_res]
            # Rotate
            X_rot = (X - cx)*np.cos(theta) + (Y - cy)*np.sin(theta)
            Y_rot = -(X - cx)*np.sin(theta) + (Y - cy)*np.cos(theta)
            mask = (X_rot/a)**2 + (Y_rot/b)**2 <= 1
            
            # Color: spiral orange/white
            canvas[mask] += np.array([0.8, 0.6, 0.4]) * 0.5
            
        return np.clip(canvas, 0, 1)

    def render_frame(self, frame_idx):
        # 1. Black Hole Position
        t = frame_idx / self.frames
        bh_pos = np.array([-15.0 + 30.0 * t, 0.0]) 
        
        # 2. Ray Tracing Geometry
        rx = self.X - bh_pos[0]
        ry = self.Y - bh_pos[1]
        r_sq = rx**2 + ry**2
        r = np.sqrt(r_sq)
        
        mask_horizon = r < self.R_s
        
        # 3. Lensing Displacement
        LENS = 12.0 # Stronger lensing for dramatic effect
        defl_x = -rx / (r_sq + 0.1) * LENS
        defl_y = -ry / (r_sq + 0.1) * LENS
        
        # 4. Map to Background Texture
        # Texture Coords (0 to res*3)
        # Screen is [-10, 10]
        # Map Screen -> [0, res*3]
        scale = self.res * 3
        
        u = (self.X + self.size/2) / self.size * scale
        v = (self.Y + self.size/2) / self.size * scale
        
        # Look up at displaced position
        u_dist = u + defl_x * (scale / self.size)
        v_dist = v + defl_y * (scale / self.size)
        
        # Clipping
        u_idx = np.clip(u_dist.astype(int), 0, scale - 1)
        v_idx = np.clip(v_dist.astype(int), 0, scale - 1)
        
        # Sample
        img = self.bg_texture[v_idx, u_idx]
        
        # 5. Render The Causal Mirror (Horizon)
        # A perfectly reflective sphere has a complex look (reflecting the observer/darkness).
        # We'll give it a "Vantablack Paradox" look: Outer rim is Chrome, Inner is Void?
        # UKFT says it's a Mirror.
        # Let's make it a Dark Metallic Sphere.
        sphere_shade = np.clip(1.0 - (r[mask_horizon] / self.R_s)**2, 0, 1)
        
        # Reflection term: Dark Purple/Black center, Cyan Rim
        img[mask_horizon, 0] = sphere_shade * 0.1 
        img[mask_horizon, 1] = sphere_shade * 0.8
        img[mask_horizon, 2] = sphere_shade * 0.9 
        
        # 6. Photon Ring (The Fire)
        mask_ring = (r > self.R_s) & (r < self.R_s * 1.1)
        ring_intensity = (1.0 - (r[mask_ring] - self.R_s)/(self.R_s*0.1))
        
        # Add GOLD/white hot ring
        img[mask_ring] += np.outer(ring_intensity, [1.0, 0.8, 0.4])
        
        return np.clip(img, 0, 1), bh_pos

    def animate(self):
        fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
        ax.set_axis_off()
        img_buffer = np.zeros((self.res, self.res, 3))
        im = ax.imshow(img_buffer, origin='lower', extent=[-10, 10, -10, 10])
        
        def update(frame):
            print(f"Rendering frame {frame}/{self.frames}...", end='\r')
            img_data, bh_pos = self.render_frame(frame)
            im.set_data(img_data)
            ax.set_title(f"UKFT Black Hole (Experiment 33c)\nBackground: Synthetic Deep Field", color='white')
            return [im]

        ani = FuncAnimation(fig, update, frames=self.frames, blit=True)
        save_path = "results/33c_ukft_black_hole_jwst.gif"
        ani.save(save_path, writer='pillow', fps=15)
        print(f"\nSaved high-res visualization to {save_path}")

if __name__ == "__main__":
    sim = UKFTBlackHoleJWST(resolution=256, frames=60) # Higher res for final output
    sim.animate()
