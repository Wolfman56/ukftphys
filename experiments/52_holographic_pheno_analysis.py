import numpy as np
import matplotlib.pyplot as plt
import gzip
import xml.etree.ElementTree as ET
import os

# Physical Constants and Particle IDs
PID_H = 25
PID_B = 5
PID_TAU = 15
PID_NEUTRINO_TAU = 16

class LHEEvent:
    def __init__(self):
        self.particles = []
        self.met = 0.0
        self.scalar_pt = 0.0
        self.scalar_mass = 0.0

def parse_lhe(file_path):
    """
    Minimal LHE parser to extract kinematics.
    Returns list of LHEEvent objects.
    """
    events = []
    
    # Check if gzipped
    if file_path.endswith('.gz'):
        opener = gzip.open
    else:
        opener = open
        
    try:
        with opener(file_path, 'rt') as f:
            in_event = False
            current_event = None
            
            for line in f:
                line = line.strip()
                
                if line == '<event>':
                    in_event = True
                    current_event = LHEEvent()
                    continue
                    
                if line == '</event>':
                    if current_event:
                        # Calculate MET (Sum of invisible pt)
                        px_inv = 0.0
                        py_inv = 0.0
                        
                        # Find Scalar info
                        for p in current_event.particles:
                            pid = abs(p['id'])
                            # Status 1 = Final State
                            # Status 2 = Intermediate (Resonance)
                            # Status -1 = Initial State
                            
                            # Calculate MET from Neutrinos
                            if pid in [12, 14, 16] and p['status'] == 1:
                                px_inv += p['px']
                                py_inv += p['py']
                                
                            # Track Scalar (ID 25)
                            if pid == 25:
                                current_event.scalar_pt = np.sqrt(p['px']**2 + p['py']**2)
                                current_event.scalar_mass = p['m']
                        
                        current_event.met = np.sqrt(px_inv**2 + py_inv**2)
                        events.append(current_event)
                    in_event = False
                    continue
                    
                if in_event:
                    # Parse particle line
                    # ID Status Mother1 Mother2 Color1 Color2 Px Py Pz E M Lifetime Spin
                    parts = line.split()
                    try:
                        # Skip the event info line (first line after <event>)
                        if len(parts) < 13: 
                            continue
                            
                        particle = {
                            'id': int(parts[0]),
                            'status': int(parts[1]),
                            'px': float(parts[6]),
                            'py': float(parts[7]),
                            'pz': float(parts[8]),
                            'e': float(parts[9]),
                            'm': float(parts[10])
                        }
                        current_event.particles.append(particle)
                    except (ValueError, IndexError):
                        continue
                        
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []

    return events

def analyze_pheno():
    base_dir = "experiments/52_holographic_pheno"
    bb_path = os.path.join(base_dir, "bb_process/Events/run_01/unweighted_events.lhe.gz")
    tau_path = os.path.join(base_dir, "tau_process/Events/run_01/unweighted_events.lhe.gz")
    
    print("Parsing Hadronic (b-bbar) events...")
    bb_events = parse_lhe(bb_path)
    print(f"Loaded {len(bb_events)} events.")
    
    print("Parsing Holographic (tau-tau) events...")
    tau_events = parse_lhe(tau_path)
    print(f"Loaded {len(tau_events)} events.")
    
    # Histograms
    bins = np.linspace(0, 100, 50)
    
    # 1. Scalar pT Recoil (against the jet)
    bb_pt = [e.scalar_pt for e in bb_events]
    tau_pt = [e.scalar_pt for e in tau_events]
    
    # 2. Missing Transverse Energy (MET)
    # in b-bbar: MET should be 0 (no neutrinos, unless semi-leptonic B decay logic in parsing was fancier)
    # in tau-tau: MET comes from neutrinos
    bb_met = [e.met for e in bb_events]
    tau_met = [e.met for e in tau_events]
    
    # Plotting
    plt.figure(figsize=(14, 6))
    
    # Plot 1: Scalar pT (Production Mechanism Check)
    plt.subplot(1, 2, 1)
    plt.hist(bb_pt, bins=bins, alpha=0.5, label='Hadronic (Standard)', density=True, color='blue')
    plt.hist(tau_pt, bins=bins, alpha=0.5, label='Holographic (Entropic)', density=True, color='red',  histtype='step', linewidth=2)
    plt.xlabel('Scalar $p_T$ (GeV)')
    plt.ylabel('Normalized Events')
    plt.title('Production Kinematics ($g g \\to H + j$)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Missing Energy (The "Holographic Signal")
    plt.subplot(1, 2, 2)
    plt.hist(bb_met, bins=bins, alpha=0.5, label='Hadronic ($H \\to b\\bar{b}$)', density=True, color='blue')
    plt.hist(tau_met, bins=bins, alpha=0.5, label='Holographic ($H \\to \\tau\\tau \\to \\nu$...)', density=True, color='red', histtype='step', linewidth=2)
    plt.xlabel('Missing Energy (MET) [GeV]')
    plt.ylabel('Normalized Events')
    plt.title('Decay Signature (Information Loss)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_path = "experiments/52_holographic_pheno_comparison.png"
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Comparison plot saved to {output_path}")

if __name__ == "__main__":
    analyze_pheno()
