import gzip
import numpy as np
import matplotlib.pyplot as plt
import os

# Experiment 81: Simulating the CERN Glitch
# Analyzes Mirror Fermion Pair Production and applies the "5/9" Entropic Bias
# to generate the observed CP Asymmetry.

LHE_FILE = "experiments/81_glitch_source/Events/run_01/unweighted_events.lhe.gz"
OUTPUT_DIR = "results/exp81_glitch"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Particle IDs
PID_XM = 6000001 # Mirror Fermion (observed in LHE)
PID_T = 6
PID_H = 25
PID_B = 5
PID_W = 24

# === Entropic Bias — Zeta-Delta-Sigma Weighting ===
# Replaces the flat (5/9) * alpha_QED constant.
# Full formula (Exp 42 / 80 extension):
#
#   W_ΣΔ(p) = Δ_d / (bitLen(p) + 1) * exp(-S_ΔΣ(b))
#
# where:
#   Δ_d   = E8 center density = π^4 / 384 ≈ 0.2537 (packing-Shannon factor)
#   bitLen(p) = floor(log2(p))            (sigma-delta bit length of prime p)
#   S_ΣΔ(b)  = entropic action of the bitstream b (conservative approximation:
#               use event pT as proxy — high pT → many bits → lower weight)
#
# Lean stub: UKFT/QFT_MirrorFermion.lean `mirror_fermion_amplitude`

import math

DELTA_D = math.pi**4 / 384          # E8 packing density ≈ 0.2537
ALPHA_QED = 1.0 / 137.036

def sigma_delta_weight(prime_proxy: float, pt_gev: float) -> float:
    """Full W_SigmaDelta weight for a mirror-fermion event.

    Args:
        prime_proxy: representative prime for this event (e.g., nearest prime
                     above mass in GeV).  For LHE events without an obvious
                     prime, use 151 (zero #15 proxy, bio-noo Teilhard boundary).
        pt_gev:      transverse momentum in GeV (used as proxy for S_SigmaDelta).
    """
    bit_len = math.floor(math.log2(max(prime_proxy, 2.0)))
    # S_SigmaDelta proxy: entropic cost ∝ log(pT/GeV) at high energy
    S_sigma_delta = math.log(max(pt_gev, 1.0)) * ALPHA_QED
    return DELTA_D / (bit_len + 1) * math.exp(-S_sigma_delta)

print(f"DELTA_D (E8 packing): {DELTA_D:.6f}")
print(f"W_SigmaDelta at p=151, pT=150 GeV: {sigma_delta_weight(151, 150):.6e}")

class Particle:
    def __init__(self, px, py, pz, E, pid, status):
        self.px = px
        self.py = py
        self.pz = pz
        self.E = E
        self.pid = pid
        self.status = status # 1=final, 2=intermediate
        
    def pt(self):
        return np.sqrt(self.px**2 + self.py**2)
    
    def eta(self):
        p = np.sqrt(self.px**2 + self.py**2 + self.pz**2)
        if p == self.pz: return 10.0 # Beam
        return 0.5 * np.log((p + self.pz)/(p - self.pz))
        
    def phi(self):
        return np.arctan2(self.py, self.px)

def parse_lhe(filename):
    events = []
    current_event = []
    
    with gzip.open(filename, 'rt') as f:
        in_event = False
        for line in f:
            if "<event>" in line:
                in_event = True
                current_event = []
                continue
            if "</event>" in line:
                in_event = False
                events.append(current_event)
                continue
            if in_event:
                if not line.strip(): continue
                parts = line.split()
                if len(parts) < 10: continue
                # MadGraph LHE format: PID Status Mothers Colors Px Py Pz E Mass Spin
                try:
                    pid = int(parts[0])
                    status = int(parts[1])
                    px = float(parts[6])
                    py = float(parts[7])
                    pz = float(parts[8])
                    E = float(parts[9])
                    current_event.append(Particle(px, py, pz, E, pid, status))
                except ValueError:
                    continue # ID line
                    
    return events

def decay_to_b(particle):
    # Simplified decay kinematic simulation
    # xm -> t + h -> (b + W) + h
    # We approximate the b-quark momentum direction
    # Just take particle direction + smearing
    # M_xm = 320, M_t = 173, M_h = 125
    # M_b = 4.2
    
    # Simple collinear approx for rapid check
    # b takes ~ 1/3 of energy?
    # Decay t -> b W. b takes ~ (1 - Mw^2/Mt^2) * Mt / 2 in rest frame?
    # Just scale
    scale = 0.35
    b_part = Particle(
        particle.px * scale, 
        particle.py * scale, 
        particle.pz * scale, 
        particle.E * scale, 
        np.sign(particle.pid) * PID_B, 
        1
    )
    return b_part

def analyze_glitch():
    print(f"Parsing {LHE_FILE}...")
    events = parse_lhe(LHE_FILE)
    print(f"Loaded {len(events)} events.")
    
    # Analysis Arrays
    b_pts_matter = []
    b_pts_antimatter = []
    weights_matter = []
    weights_antimatter = []
    
    asymmetry_vs_pt = []
    pt_bins = np.linspace(0, 500, 20)
    
    analyzed_count = 0
    matter_count = 0
    antimatter_count = 0

    for event in events:
        # Check if Mirror Fermions exist
        xms = [p for p in event if abs(p.pid) == PID_XM]
        if not xms: 
            # DEBUG: Print PIDs of first event if failing
            if analyzed_count == 0 and len(events) > 0 and event == events[0]:
                 print(f"DEBUG: First event PIDs: {[p.pid for p in event]}")
            continue
        
        analyzed_count += 1
        
        for xm in xms:
            # Simulate B-quark production via decay
            b_quark = decay_to_b(xm)
            
            # Apply Entropic Bias
            # Matter (PID > 0 for b-quark is DOWN-type? No, b is Bottom.
            # PID(b) = 5. PID(b~) = -5.
            # Mirror Fermion Xm: charge +2/3 (up type)? Or -1/3?
            # Model says Xm ~ Top partner. Charge +2/3.
            # Decay Xm -> t h -> b W h.
            # If Xm (+2/3) -> t (+2/3) h. t -> b (-1/3) W+.
            # So Xm (Matter) -> b (Matter). 
            # Xm~ (Antimatter) -> b~ (Antimatter).
            
            is_matter = (b_quark.pid > 0) # PDG: d,u,s,c,b,t > 0 are quarks (matter)
            
            if is_matter: matter_count += 1
            else: antimatter_count += 1
            
            # Weight modulation — full W_SigmaDelta (replaces flat 5/9 * alpha)
            # Prime proxy: use 151 (Teilhard bio-noo boundary, zero #15 region)
            # pT proxy for S_SigmaDelta entropic action
            pt = b_quark.pt()
            w_zeta = sigma_delta_weight(151, max(pt, 1.0))

            wt = 1.0
            if is_matter:
                wt *= (1.0 + w_zeta)
                b_pts_matter.append(pt)
                weights_matter.append(wt)
            else:
                wt *= (1.0 - w_zeta)
                b_pts_antimatter.append(pt)
                weights_antimatter.append(wt)

    print(f"DEBUG: Events with Xm: {analyzed_count}")
    print(f"DEBUG: Matter b-quarks: {matter_count}, Antimatter b-quarks: {antimatter_count}")

    # Convert to arrays
    b_m = np.array(b_pts_matter)
    w_m = np.array(weights_matter)
    b_a = np.array(b_pts_antimatter)
    w_a = np.array(weights_antimatter)
    
    # Calculate Asymmetry in bins
    bin_centers = 0.5 * (pt_bins[1:] + pt_bins[:-1])
    asymmetries = []
    errors = []
    
    for i in range(len(pt_bins)-1):
        low = pt_bins[i]
        high = pt_bins[i+1]
        
        # Mask
        mask_m = (b_m >= low) & (b_m < high)
        mask_a = (b_a >= low) & (b_a < high)
        
        # Weighted Counts
        N_m = np.sum(w_m[mask_m])
        N_a = np.sum(w_a[mask_a])
        
        # Raw counts (for error)
        n_m_raw = np.sum(mask_m)
        n_a_raw = np.sum(mask_a)
        
        if (N_m + N_a) > 0:
            A = (N_m - N_a) / (N_m + N_a)
            # Simple Poisson error approx
            err = 1.0 / np.sqrt(n_m_raw + n_a_raw + 1e-9)
        else:
            A = 0.0
            err = 0.0
            
        asymmetries.append(A)
        errors.append(err)
        
    asymmetries = np.array(asymmetries)
    errors = np.array(errors)
    
    # Plotting "The Glitch"
    plt.figure(figsize=(10, 6))
    plt.errorbar(bin_centers, asymmetries, yerr=errors, fmt='o-', color='purple', label='Simulated A_CP')
    
    # Theoretical Expected Line
    theory_acp = 2 * BIAS_DELTA # Approx
    plt.axhline(y=theory_acp, color='r', linestyle='--', label=f'Theory (2*Bias) = {theory_acp:.4f}')
    
    plt.title("Experiment 81: Potential Origin of the CERN Glitch\n(CP Asymmetry in b-quark sector from Mirror Fermion Entropic Bias)")
    plt.xlabel("pT(b) [GeV]")
    plt.ylabel("Asymmetry A_CP (Matter - Antimatter)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(-0.05, 0.05) # Zoom in
    
    plt.text(50, 0.03, r"Entropic Bias $\delta = 5/9 \alpha$", fontsize=12, color='red')
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/cern_glitch_asymmetry.png")
    print(f"Plot saved to {OUTPUT_DIR}/cern_glitch_asymmetry.png")
    
    # --- Kinematic Plot ---
    plt.figure(figsize=(10, 6))
    plt.hist(b_m, bins=50, range=(0, 500), alpha=0.5, label='Matter b-quarks', color='blue', histtype='stepfilled')
    plt.hist(b_a, bins=50, range=(0, 500), alpha=0.5, label='Antimatter b-quarks', color='orange', histtype='stepfilled')
    plt.yscale('log')
    plt.title("Constraint on 'The Glitch' Source: Heavy Parent Kinematics")
    plt.xlabel("pT(b) [GeV]")
    plt.ylabel("Events / 10 GeV")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.text(200, 100, f"Parent Mass: 320 GeV\n(Mirror Fermion)", fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/cern_glitch_kinematics.png")
    print(f"Plot saved to {OUTPUT_DIR}/cern_glitch_kinematics.png")
    
    print("-" * 40)
    print(f"Integrated Asymmetry: {np.mean(asymmetries):.6f}")
    print(f"Theory Prediction   : {theory_acp:.6f}")
    print("-" * 40)

if __name__ == "__main__":
    analyze_glitch()
