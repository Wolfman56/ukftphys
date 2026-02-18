
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

class UKFTVolumeLens:
    def __init__(self, resolution=200, stars=8000, frames=60):
        self.res = resolution
        self.frames = frames
        self.box_size = 20.0 # Cube size [-10, 10]
        self.R_s = 1.0       # Schwarzschild Radius (Reduced to match weaker lens)
        # Reduced LENS_STRENGTH to prevent stars from being pushed off-screen entirely.
        # Was 15.0, now 2.0.
        self.LENS_STRENGTH = 2.0 
        
        # Camera Plate (Orthographic)
        # Position fixed at z = -self.box_size
        self.x_plate = np.linspace(-self.box_size/2, self.box_size/2, self.res)
        self.y_plate = np.linspace(-self.box_size/2, self.box_size/2, self.res)
        self.X, self.Y = np.meshgrid(self.x_plate, self.y_plate)
        
        # Star Field (3D Volume)
        # Randomly distributed in the box
        np.random.seed(42)
        self.star_pos = np.random.uniform(-self.box_size/2, self.box_size/2, (stars, 3))
        # Push stars deeper into Z so we have foreground/background relative to BH path
        # Let's make Z range [-10, 30] to give depth
        self.star_pos[:, 2] = np.random.uniform(-10, 30, stars)
        
        # Star Colors (Red/Blue/White)
        self.star_colors = np.random.rand(stars, 3)
        # Make them bright
        self.star_colors = 0.5 + 0.5 * self.star_colors

    def trace_rays(self, bh_pos):
        # Reverse Ray Tracing: Camera -> Scene
        # 1. Undistorted Ray targets (Z = infinity plane)
        # In orthogonal projection, a pixel (x,y) corresponds to a ray (x,y, z) moving +z.
        # If there were no gravity, it would hit a star at (x,y) if star.x=x and star.y=y.
        
        # With gravity, the ray gets bent.
        # We need to find which star's light ends up at pixel (x,y).
        # This is effectively "Where does pixel (x,y) look?"
        
        # Vector from BH to Pixel Ray (Impact Parameter b)
        # BH is at (BH_x, BH_y, BH_z)
        # Ray passes through (x, y, z_arbitrary).
        # The deflection happens mainly at the Z-plane of the Black Hole.
        # Let's approximate the "Thin Lens" model at Z = BH_z.
        
        # Relative coordinates on the lens plane
        dx = self.X - bh_pos[0]
        dy = self.Y - bh_pos[1]
        r_sq = dx**2 + dy**2
        r = np.sqrt(r_sq)
        
        # Mask Horizon (The Mirror)
        mask_horizon = r < self.R_s
        
        # Calculate Deflection Angle (theta)
        # theta ~ 1/r
        # Displacement vector *on the sky* relative to undistorted line of sight
        # shifts the "look at" coordinate.
        # A ray at X looks at source position X' = X - D * theta
        # where D is distance from Lens to Source.
        # Since sources are at varying Z, D varies per star!
        # This is the "Volumetric" part.
        
        # We can't vectorized look up a single background texture because depth varies.
        # Instead, we Project Stars onto the Camera.
        # WAIT! The prompt asked for "Reverse Ray Trace" (Camera -> Scene). 
        # But efficiently rendering 5000 stars with varying depth using reverse tracing usually requires a volumetric grid or distance fields.
        # A clearer way for "Points" is:
        # For each pixel, calculate the curved ray path.
        # Check distance to every star? Too slow (200x200x5000 = 200M ops).
        
        # Faster Reverse Approach:
        # Pre-splat stars onto the "Sky" at infinity?
        # No, depth parallax is key.
        
        # Hybrid Approach: "Splatting with Lensing"
        # 1. Transform Star Positions based on BH Lensing.
        # For each star S(xs, ys, zs):
        #   Calculate if ray from Camera(xc, yc) hits it.
        #   The perceived position P(u, v) on the plate is the solution to the lens equation.
        #   Lens Eq: beta = theta - alpha(theta)
        #   Where beta = true star position, theta = image position.
        #   We want theta (Where to draw the dot).
        #   This is "Forward Ray Tracing" math but generates the discrete image.
        #   Let's stick to this "Splatting" method as it's efficient for point stars.
        
        image = np.zeros((self.res, self.res, 3))
        
        # Vectorized Lensing of Stars
        # Relative position of Star to BH (in XY plane)
        # But wait, true lensing depends on Z-distances.
        # Lens Plane is at BH_z.
        # Observer is at -Infinity (Orthographic).
        
        # Constants
        D_s = self.star_pos[:, 2] - (-20.0) # Dist from Camera to Star? No, Orthographic.
        # Effective D_ls (Lens to Source) = Star_z - BH_z
        d_ls = self.star_pos[:, 2] - bh_pos[2]
        
        # Filter stars behind the camera or lens?
        # Only lensed if Star is *behind* the BH (z_star > z_bh).
        mask_behind_lens = d_ls > 0
        
        # Perceived Position Calculation
        # Einstein Radius R_E depends on distances.
        # R_E^2 ~ D_ls / D_s (normalized)
        # For Orthographic projection, the angular deflection theta = 4GM/bc^2.
        # The shift dX = theta * D_ls.
        # So observed position X_obs = X_star + shift?
        # Actually, gravity pulls light IN.
        # So the star appears pushed OUT.
        # Image position theta > Source position beta.
        # Beta = Theta - Alpha.
        # We know Beta (Star true pos). We want Theta (Image pos).
        # Beta = Theta - (k / Theta)   (where k ~ Einstein Radius squared)
        # Theta^2 - Beta*Theta - k = 0
        # Quadratic equation for Theta!
        # This gives TWO images (Theta+ and Theta-) -> Einstein Ring.
        
        # Vectors:
        # Beta_vec = (Star_x - BH_x, Star_y - BH_y)
        sx = self.star_pos[:, 0] - bh_pos[0]
        sy = self.star_pos[:, 1] - bh_pos[1]
        beta_mag = np.sqrt(sx**2 + sy**2) + 1e-6
        
        # Einstein Radius K for each star
        # K ~ sqrt(D_ls) roughly in this metric
        # Let's tune it.
        K = self.LENS_STRENGTH * np.sqrt(np.maximum(0, d_ls))
        
        # Solutions for Image Positions (relative to BH center)
        # Theta = (Beta + sqrt(Beta^2 + 4K^2)) / 2  (Major Image - Outer)
        # Theta' = (Beta - sqrt(Beta^2 + 4K^2)) / 2 (Minor Image - Inner/Inverted)
        
        # 1. Primary Image (Outer)
        # Shift magnitude
        theta_mag = (beta_mag + np.sqrt(beta_mag**2 + 4/self.res * K**2 * 50.0)) / 2.0 
        # Note: Scaling factor 50.0 is heuristic to match resolution
        
        scale_outer = theta_mag / beta_mag
        
        im_x_outer = bh_pos[0] + sx * scale_outer
        im_y_outer = bh_pos[1] + sy * scale_outer
        
        # 2. Secondary Image (Inner - usually inside Einstein Ring)
        # Only visible if star is significantly behind lens
        theta_mag_inner = (beta_mag - np.sqrt(beta_mag**2 + 4/self.res * K**2 * 50.0)) / 2.0
        scale_inner = theta_mag_inner / beta_mag
        
        im_x_inner = bh_pos[0] + sx * scale_inner
        im_y_inner = bh_pos[1] + sy * scale_inner
        
        # 3. Handling "The Mirror" (Horizon)
        # If an image falls within R_s of the BH, it is blocked/reflected.
        # Dist from BH center
        dist_outer = np.sqrt((im_x_outer - bh_pos[0])**2 + (im_y_outer - bh_pos[1])**2)
        dist_inner = np.sqrt((im_x_inner - bh_pos[0])**2 + (im_y_inner - bh_pos[1])**2)
        
        # FIX: Foreground stars (mask_behind_lens is False) should NOT be blocked by the BH.
        # They pass in front of it.
        # Background stars are blocked if they fall inside R_s.
        visible_outer = (dist_outer > self.R_s) | (~mask_behind_lens)
        
        # Secondary images only exist for background sources and must be outside R_s to be seen.
        visible_inner = (dist_inner > self.R_s) & mask_behind_lens
        
        # 4. Rasterize Points (Splatting)
        # Convert world coords to pixel coords
        # Map [-10, 10] to [0, res]
        def to_pix(x, y):
            px = ((x + self.box_size/2) / self.box_size * self.res).astype(int)
            py = ((y + self.box_size/2) / self.box_size * self.res).astype(int)
            return px, py

        # Draw Outer
        px_outer, py_outer = to_pix(im_x_outer, im_y_outer)
        # Bounds check
        valid_outer = (px_outer >= 0) & (px_outer < self.res) & (py_outer >= 0) & (py_outer < self.res) & visible_outer
        
        # Add color
        # Use discrete max blending instead of additive integration
        
        # Iterate over VALID INDICES 
        valid_indices = np.where(valid_outer)[0]
        
        if len(valid_indices) > 0:
            for i in valid_indices:
                current_pixel = image[py_outer[i], px_outer[i]]
                
                # Check if this specific star 'i' is behind the lens
                is_background = mask_behind_lens[i]
                
                if is_background:
                    # Lensed Background Star -> BLUE
                    draw_color = np.array([0.0, 0.5, 1.0]) 
                else:
                    # Foreground Star -> WHITE
                    draw_color = np.array([1.0, 1.0, 1.0])
                
                image[py_outer[i], px_outer[i]] = np.maximum(current_pixel, draw_color)
            
        # Draw Inner (Secondary Images - The "Ring")
        px_inner, py_inner = to_pix(im_x_inner, im_y_inner)
        valid_inner = (px_inner >= 0) & (px_inner < self.res) & (py_inner >= 0) & (py_inner < self.res) & visible_inner
        
        valid_indices_inner = np.where(valid_inner)[0]
        for i in valid_indices_inner:
             target_pix = image[py_inner[i], px_inner[i]]
             # Background Secondary: Red (The "Ghost" Image)
             new_color = np.array([1.0, 0.2, 0.2]) 
             image[py_inner[i], px_inner[i]] = np.maximum(target_pix, new_color)
             
        # Normalize
        image = np.clip(image, 0, 1)
        
        # Mirror Visualization: REMOVED by request.
        # The "Hole" is now invisible (black), defined only by the absence of stars.
        
        return image

    def animate(self):
        fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
        ax.set_axis_off()
        img_buffer = np.zeros((self.res, self.res, 3))
        im = ax.imshow(img_buffer, origin='lower', extent=[-10, 10, -10, 10])
        
        def update(frame):
            print(f"Rendering frame {frame}/{self.frames}...", end='\r')
            
            # Parametric Path for BH: Straight Push
            # Start IN FRONT of the volume (z < -10) and move BEHIND (z > 30)
            t = frame / self.frames # 0 to 1
            z_start = -15.0
            z_end = 35.0
            z = z_start + (z_end - z_start) * t
            
            # No Rotation - Straight Shot down the center
            x = 0.0
            y = 0.0
            
            bh_pos = np.array([x, y, z])
            
            # Update Title to explain Color Coding
            img_data = self.trace_rays(bh_pos)
            im.set_data(img_data)
            ax.set_title(f"UKFT Quantum Lensing\nWhite=Unlensed, Blue=Primary, Red=Secondary\nBH Depth Z={z:.1f}", color='white', fontsize=10)
            return [im]

        ani = FuncAnimation(fig, update, frames=self.frames, blit=True)
        save_path = "results/34_ukft_volume_lens.gif"
        print(f"Saving volumetric trace to {save_path}...")
        ani.save(save_path, writer='pillow', fps=15)
        print("\nDone!")

if __name__ == "__main__":
    sim = UKFTVolumeLens(resolution=300, stars=8000, frames=90)
    sim.animate()
