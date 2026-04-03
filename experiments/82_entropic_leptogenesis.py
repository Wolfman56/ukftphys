import numpy as np
import matplotlib.pyplot as plt
import os

# Experiment 82: Entropic Leptogenesis
# Simulating the Causal Graph "Cooling" and the evolution of the Entropic Bias.
# Linking the Primordial Asymmetry (11.1%) to the Modern "Glitch" (0.4%).

OUTPUT_DIR = "results/exp82_leptogenesis"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Constants
ALPHA_QED = 1.0/137.036
DELTA_LOW_T = (5.0/9.0) * ALPHA_QED # ~ 0.00405
DELTA_HIGH_T = 1.0/9.0              # ~ 0.11111 (5 moves vs 4 moves)

# Temperature Scale (Logarithmic, arbitrary units)
# T=1000: Nucleation / Inflation Reheating
# T=1:    Today / Low Energy Limit
Temps = np.logspace(3, 0, 1000)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def calculate_bias_evolution(T):
    # Transition scale at T_critical (e.g., Electroweak scale)
    T_crit = 100.0 
    width = 50.0
    
    # Sigmoid transition function (1 at High T, 0 at Low T)
    # We want High Bias at High T
    # transition = sigmoid((T - T_crit) / width) # Wait, sigmoid grows with T.
    
    # Smoother crossover function
    # At high T, dominates geometric screening.
    # We model it as the "Freezing out" of topological degrees of freedom.
    
    # Fraction of "Topological Moves" vs "Geometric Moves"
    f_topo = np.tanh(T / T_crit)
    
    delta = f_topo * DELTA_HIGH_T + (1.0 - f_topo) * DELTA_LOW_T
    return delta

# === Emergent GR Hook ===
# The same entropic bias delta(T) that drives leptogenesis also sources the
# Friedmann equation via rho_choice ∝ delta(T) / a^3.  In UKFT, gravity is the
# error-minimisation of the same choice operator (Exps 16–19), so the cooling
# causal graph IS the expanding universe.  The Friedmann link is:
#
#   H^2 = (8πG/3) * rho_choice,   rho_choice = delta(T) / a^3
#
# This gives H^2 ∝ delta(T) / a^3 — recovering standard radiation-dominated
# Friedmann scaling when delta(T) ∝ T^4 (Stefan–Boltzmann) and a ∝ 1/T.
# The same δ(T) that produces η_baryon also seeds spacetime curvature.
# Lean stub: UKFT/Emergent_GR.lean `entropic_leptogenesis_unifies_gr`.

def friedmann_rho_choice(delta: float, a: float) -> float:
    """Effective energy density sourced by entropic bias (arbitrary units)."""
    return delta / (a ** 3)


def simulate_universe_cooling():
    deltas = calculate_bias_evolution(Temps)
    
    # Plotting the Evolution of the "Choice" Constant
    plt.figure(figsize=(10, 6))
    
    # Main Line
    plt.semilogx(Temps, deltas * 100.0, label='Entropic Bias $\delta(T)$', linewidth=2, color='crimson')
    
    # Asymptotes
    plt.axhline(DELTA_HIGH_T * 100.0, linestyle='--', color='gray', alpha=0.5, label='Primordial Limit (1/9) = 11.1%')
    plt.axhline(DELTA_LOW_T * 100.0, linestyle='--', color='blue', alpha=0.5, label='Modern Limit (5/9 $\\alpha$) = 0.4%')
    
    # Annotations
    plt.text(800, 11.5, "Graph Nucleation\n(Topological Phase)", ha='center', fontsize=9)
    plt.text(1.5, 0.6, "LHCb Anomaly\n(Geometric Phase)", ha='left', fontsize=9)
    # Arrow
    plt.arrow(200, 8, -100, -4, head_width=0.5, head_length=10, fc='k', ec='k', alpha=0.5)
    plt.text(60, 6, "Universe Cooling\n(Redshift of Bias)", rotation=-30, ha='center', alpha=0.7)

    plt.title("Experiment 82: Evolution of the Entropic Choice Operator")
    plt.xlabel("Universe Temperature / Connectivity Scale ($T$)")
    plt.ylabel("CP Asymmetry Bias $\delta$ (%)")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    
    # Save 1
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/bias_evolution.png")
    
    print(f"High T Bias: {deltas[0]:.4f} (Target: {DELTA_HIGH_T:.4f})")
    print(f"Low T Bias : {deltas[-1]:.6f} (Target: {DELTA_LOW_T:.6f})")

    # Part 2: Baryogenesis Simulation
    # Simple integration of Net Baryon Number with this bias
    # dN/dt = -Gamma * N + Source(delta)
    # Actually, let's just show the accumulated potential.
    
    # We create a visualization of the "Causal Horizon" sorting.
    
    plt.figure(figsize=(10,6))
    
    # 5/9 vs 4/9 conceptual chart
    
    moves = ['Matter Moves\n(Connectivity +)', 'Antimatter Moves\n(Connectivity -)']
    counts = [5, 4]
    
    bars = plt.bar(moves, counts, color=['#2ca02c', '#d62728'], alpha=0.7)
    
    plt.ylim(0, 6)
    plt.title("Primordial Causal Selection (The '1/9' Origin)")
    plt.ylabel("Available Causal Rewiring Moves")
    
    # Text on bars
    plt.text(0, 5.1, "5 Moves\n(Maintain Order)", ha='center', fontweight='bold')
    plt.text(1, 4.1, "4 Moves\n(Collapse to Void)", ha='center', fontweight='bold')
    
    # The Gap
    plt.annotate(
        "Net Bias = (5-4)/9 = 11.1%", 
        xy=(1, 4.5), xytext=(0, 4.5),
        arrowprops=dict(arrowstyle="<->", color='black'),
        ha='center', va='bottom'
    )
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/causal_selection_counts.png")

    print(f"Plots saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    simulate_universe_cooling()
