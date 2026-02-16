import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import os

os.makedirs("results", exist_ok=True)

def viz_choice_field_topology():
    """
    Visualizes the 4 Particle Topologies in the Choice Field.
    1. Coherence Boson (Linear Thread)
    2. Entropic Monopole (Knot/Loop)
    3. Void Scalar (Density Fluctuation)
    4. Mirror Fermion (Boundary Defect)
    """
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle("The 4 Fundamental Topologies of the UKFT Choice Field", fontsize=16)

    # 1. Coherence Boson (Thread)
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    t = np.linspace(0, 10, 100)
    x = t * 0.5
    y = np.sin(t) * 0.2
    z = np.cos(t) * 0.2
    # Add some "fuzz" to represent quantum uncertainty
    for _ in range(5):
        ax1.plot(x + np.random.normal(0, 0.1, 100), 
                 y + np.random.normal(0, 0.1, 100), 
                 z + np.random.normal(0, 0.1, 100), 'b-', alpha=0.3)
    ax1.plot(x, y, z, 'b-', linewidth=3)
    ax1.set_title("1. Coherence Boson (The Thread)\nMassless Force Carrier")
    ax1.set_axis_off()

    # 2. Entropic Monopole (Knot)
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    # Trefoil Knot
    t = np.linspace(0, 2*np.pi, 200)
    x = np.sin(t) + 2*np.sin(2*t)
    y = np.cos(t) - 2*np.cos(2*t)
    z = -np.sin(3*t)
    ax2.plot(x, y, z, 'r-', linewidth=4)
    # Cloud around it
    ax2.scatter(x + np.random.normal(0, 0.5, 200),
                y + np.random.normal(0, 0.5, 200),
                z + np.random.normal(0, 0.5, 200), c='r', alpha=0.1, s=10)
    ax2.set_title("2. Entropic Monopole (The Knot)\nMassive (~30 GeV) Stable Defect")
    ax2.set_axis_off()

    # 3. Void Scalar (Density Fluctuation)
    ax3 = fig.add_subplot(2, 2, 3)
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1*(X**2 + Y**2))
    ax3.contourf(X, Y, Z, cmap='Purples', levels=20)
    ax3.set_title("3. Void Scalar (The Ripple)\nDark Energy / Vacuum Pressure")
    ax3.set_aspect('equal')
    ax3.axis('off')

    # 4. Mirror Fermion (Boundary Defect)
    ax4 = fig.add_subplot(2, 2, 4)
    # Draw a "Horizon" line
    ax4.axvline(x=0, color='k', linestyle='--', linewidth=2)
    # Particle on one side
    circle1 = plt.Circle((-2, 0), 1.0, color='g', alpha=0.8)
    ax4.add_patch(circle1)
    ax4.text(-2, -1.5, "Matter", ha='center')
    # Reflection on other side (distorted)
    circle2 = plt.Circle((2, 0), 1.0, color='lime', alpha=0.4, linestyle=':')
    ax4.add_patch(circle2)
    ax4.text(2, -1.5, "Mirror\n(Anti-Choice)", ha='center')
    ax4.set_xlim(-5, 5)
    ax4.set_ylim(-3, 3)
    ax4.set_title("4. Mirror Fermion (The Reflection)\nBoundary Conservation State (~TeV)")
    ax4.axis('off')

    plt.tight_layout()
    plt.savefig("results/ukft_particle_topology.png")
    print("Saved results/ukft_particle_topology.png")

def viz_gravitational_anomaly_3d():
    """
    3D visualization of the anisotropic gravity in a jet.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Sphere of standard gravity (Unit sphere)
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x, y, z, color='gray', alpha=0.1)
    
    # Anomalous Gravity Spikes (Along Z axis)
    # The anomaly is at cos(theta) -> 1 (Z axis)
    # We draw a "Jet" shape
    z_jet = np.linspace(0, 4, 50)
    r_jet = 0.2 * np.exp(-z_jet/2) # Narrowing cone? Or just narrow cylinder
    
    # Cone top
    u = np.linspace(0, 2*np.pi, 30)
    Z_cone, U = np.meshgrid(z_jet, u)
    X_cone = 0.1 * Z_cone * np.cos(U) # Expanding cone
    Y_cone = 0.1 * Z_cone * np.sin(U)
    
    # Magnitude of force scales with Z? No, plot Surface where R = Force
    # F(theta) = 1 + 300 * delta(theta)
    
    # Plotting the "Force Surface"
    # R(theta) = 1 + Enhancement(theta)
    
    theta = np.linspace(0, np.pi, 100)
    phi = np.linspace(0, 2*np.pi, 100)
    THETA, PHI = np.meshgrid(theta, phi)
    
    # Gaussian enhancement at poles
    enhancement = 5.0 * np.exp(- (THETA)**2 / 0.05) + 5.0 * np.exp(- (THETA - np.pi)**2 / 0.05)
    R = 1.0 + enhancement
    
    X_f = R * np.sin(THETA) * np.cos(PHI)
    Y_f = R * np.sin(THETA) * np.sin(PHI)
    Z_f = R * np.cos(THETA)
    
    # Color by strength
    surf = ax.plot_surface(X_f, Y_f, Z_f, cmap='inferno', facecolors=cm.inferno(enhancement/np.max(enhancement)))
    
    ax.set_title("Gravitational Force Anisotropy in UKFT\n(The 'Spiky' Gravity of Jets)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z (Jet Axis)")
    
    plt.savefig("results/ukft_gravity_anisotropy_3d.png")
    print("Saved results/ukft_gravity_anisotropy_3d.png")

if __name__ == "__main__":
    viz_choice_field_topology()
    viz_gravitational_anomaly_3d()
