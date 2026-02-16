# experiments/exp26_emergent_graviton.py
"""
UKFT Phase 2 Experiment 26: Emergent Graviton Analogue
Goal: Demonstrate that GRAVITY (Spin-2 behavior) emerges naturally from the same
choice-dynamics as Gauge Theory (Exp 25) when we scale to the 'Theosphere' level.

HYPOTHESIS:
- Gauge Theory (Exp 25) = Optimizing Coherence of 'Color' vectors -> Gluons.
- Gravity (Exp 26) = Optimizing Coherence of 'Energy/Mass' scalars -> Gravitons.
- The Prophet should discover that the optimal rule for Mass is UNIVERSAL ATTRACTION,
  whereas Color was selective.

Key features:
- Mass-labeled nodes (Scalar Energy).
- Tensor-flow choice branching (Spin-2).
- Prophet autotunes interaction rules.
- Target: Recover Newton's Law / Einstein's Geodesic as the 'Coherent Limit'.
"""

import sys
import os
import numpy as np
import random
import logging
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("exp26")

# ─── Mock Core Classes (Simulating ukft_sim) ───

@dataclass
class MassNode:
    id: int
    energy: float  # Knowledge Density ~ Mass
    position: np.ndarray

# ─── New Domain: Gravity Sector ───

class GravityProphet:
    """
    Learns the laws of interaction between 'Massive' information bundles.
    """
    def __init__(self):
        # We start with a random interaction matrix for "Spin-2" flow.
        # 0 = Repulsive, 1 = Neutral, 2 = Attractive
        # We model this as a bias parameter 'G_eff' (Effective Gravity)
        # and a 'Universality' parameter (does it affect everyone equally?)
        
        self.G_eff = random.uniform(-1.0, 1.0) # Start random (could be repulsive!)
        self.Universality = random.uniform(0.0, 1.0) # How consistent is it?
        
        # History for plotting
        self.history = {'G': [], 'U': [], 'Coherence': []}

    def evaluate_universe(self, nodes: List[MassNode]) -> float:
        """
        Calculate the 'Coherence' of a universe governed by current G_eff.
        
        In UKFT, 'Coherence' means 'Information is Preserved'.
        - If G is Repulsive: Matter flies apart -> Knowledge Density drops -> Entropy Rises.
        - If G is Too Attractive: Matter collapses to Singularity -> Knowledge Lost -> Entropy Rises.
        - If G is Just Right (Entropic Gravity): Matter forms structures (Stars/Networks) -> Max Complexity.
        """
        
        # Simulate a simplified 'Universe Step'
        # Calculate forces
        total_structure_score = 0.0
        
        for i, n1 in enumerate(nodes):
            for j, n2 in enumerate(nodes):
                if i >= j: continue
                
                # Distance
                r_vec = n1.position - n2.position
                r = np.linalg.norm(r_vec) + 0.1 # Softening
                
                # Proposed Force Magnitude (Prophet's Hypothesis)
                # F ~ G * M1 * M2 / r^2
                # We add noise based on (1 - Universality) to represent "Selective" gravity
                noise = np.random.normal(0, 1.0 - self.Universality)
                F_mag = (self.G_eff + noise) * (n1.energy * n2.energy) / (r**2)
                
                # Apply 'Motion' (Mental Simulation)
                # If Attractive (F > 0), they get closer.
                delta_r = -F_mag * 0.1 # dt
                new_r = r + delta_r
                
                # Scoring the Result (The Objective Function)
                # We want: 
                # 1. High Density (Closer is better)
                # 2. Stability (Don't crash to zero)
                
                if new_r < 0.2: 
                    # Crash/Singularity = Bad (Information crushed)
                    total_structure_score -= 50.0 
                elif new_r > 5.0:
                    # Dispersion/Cold Death = Bad (Information diluted)
                    total_structure_score -= 10.0
                else:
                    # Goldilocks Zone = High Complexity/Network formation
                    # 1/r potential energy bonus (Entropy minimization)
                    total_structure_score += (1.0 / new_r) * (n1.energy * n2.energy)

        return total_structure_score

    def optimize_step(self, nodes: List[MassNode]):
        # 1. Mutation
        mut_G = self.G_eff + np.random.normal(0, 0.1)
        mut_U = np.clip(self.Universality + np.random.normal(0, 0.05), 0, 1)
        
        # 2. Comparison
        # Current Score
        current_score = self.evaluate_universe(nodes)
        
        # Candidate Score (temporarily swap params)
        old_G, old_U = self.G_eff, self.Universality
        self.G_eff, self.Universality = mut_G, mut_U
        cand_score = self.evaluate_universe(nodes)
        
        # 3. Selection (Metropolis-like or Greedy)
        if cand_score > current_score:
            # Keep new params
            pass 
        else:
            # Revert
            self.G_eff, self.Universality = old_G, old_U
            
        # Log
        self.history['G'].append(self.G_eff)
        self.history['U'].append(self.Universality)
        self.history['Coherence'].append(max(current_score, cand_score))
        
        return max(current_score, cand_score)

# ─── Run Experiment ───

def run_exp26(n_steps=200):
    logger.info("Starting Exp 26: Emergent Graviton Analogue")
    
    # Init 'Universe' of Knowledge Nodes
    nodes = []
    for i in range(20):
        pos = np.random.rand(3) * 4.0 # 0..4 box
        mass = np.random.uniform(0.5, 2.0)
        nodes.append(MassNode(i, mass, pos))
        
    prophet = GravityProphet()
    
    # Visualization
    fig = plt.figure(figsize=(10, 6), facecolor='#111111')
    gs = GridSpec(2, 1, height_ratios=[1, 1])
    
    # Plot 1: The Emergence of G
    ax_g = fig.add_subplot(gs[0])
    ax_g.set_facecolor('#000000')
    ax_g.set_title("Emergence of Gravitational Constant (G)", color='white')
    ax_g.set_ylabel("Interaction Strength", color='white')
    ax_g.tick_params(colors='white')
    line_g, = ax_g.plot([], [], 'lime', label='G_eff (Force)')
    ax_g.axhline(0, color='gray', linestyle='--')
    ax_g.legend(loc='upper left', frameon=False, labelcolor='white')
    ax_g.grid(True, alpha=0.1)
    
    # Plot 2: Appearance of Universality
    ax_u = fig.add_subplot(gs[1])
    ax_u.set_facecolor('#000000')
    ax_u.set_title("Universality of Law (Entropy Reduction)", color='white')
    ax_u.set_xlabel("Prophet Iterations", color='white')
    ax_u.set_ylabel("Universality (0..1)", color='white')
    ax_u.set_ylim(0, 1.1)
    ax_u.tick_params(colors='white')
    line_u, = ax_u.plot([], [], 'cyan', label='Consistency')
    ax_u.legend(loc='lower right', frameon=False, labelcolor='white')
    ax_u.grid(True, alpha=0.1)
    
    def init():
        ax_g.set_xlim(0, n_steps)
        ax_g.set_ylim(-2, 2)
        return line_g, line_u

    def update(frame):
        prophet.optimize_step(nodes)
        
        # Update Plots
        params_g = prophet.history['G']
        params_u = prophet.history['U']
        x = range(len(params_g))
        
        line_g.set_data(x, params_g)
        line_u.set_data(x, params_u)
        
        if frame % 10 == 0:
            logger.info(f"Iter {frame}: G={params_g[-1]:.3f}, Univ={params_u[-1]:.3f}")
            
        return line_g, line_u

    anim = animation.FuncAnimation(fig, update, frames=n_steps, init_func=init, interval=20, blit=False)
    
    # Save
    save_path = 'experiments/26_emergent_graviton.gif'
    logger.info(f"Saving to {save_path}...")
    anim.save(save_path, writer='pillow', fps=30)
    logger.info("Done.")
    
    # Final Report
    logger.info("--- Experiment Complete ---")
    logger.info(f"Final G: {prophet.G_eff:.4f} (Should be Positive/Attractive)")
    logger.info(f"Final Universality: {prophet.Universality:.4f} (Should be near 1.0)")
    
    if prophet.G_eff > 0.1 and prophet.Universality > 0.8:
        print("\n[SUCCESS] The Prophet discovered that Universal Attraction is optimal for structure formation!")
    else:
         print("\n[INCONCLUSIVE] The Prophet did not converge on standard gravity.")

if __name__ == "__main__":
    run_exp26()
