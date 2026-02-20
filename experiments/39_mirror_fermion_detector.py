import os
import gzip
import math
import random
import numpy as np
import matplotlib.pyplot as plt

# Configuration
input_dir = "mirror_fermion_collider_38"
lhe_file = os.path.join(input_dir, "Events", "run_01", "unweighted_events.lhe.gz")
output_plot = "39_mirror_fermion_detector_comparison.png"

# Smearing Parameters
# Energy resolution for Top Quark (Jet-based reconstruction): ~15%
SIGMA_TOP = 0.15 
# Energy resolution for Higgs (b-bbar reconstruction): ~10%
SIGMA_HIGGS = 0.10

def get_p4(parts):
    # LHE format: px, py, pz, E
    px = float(parts[6])
    py = float(parts[7])
    pz = float(parts[8])
    E  = float(parts[9])
    return np.array([E, px, py, pz])

def smear_p4(p4, resolution):
    """
    Apply Gaussian smearing to the energy and scale momentum vector accordingly
    to maintain mass (approximate) or just scale 4-vector (massless measuring).
    Here we scale the 3-momentum magnitude to match the smeared energy, 
    preserving the direction (which is usually well measured) but changing E and |p|.
    However, for massive particles like t/h, we should probably just smear E and p 
    by the same factor to preserve velocity/mass approx, or smear E and recalculate p (or vice versa).
    
    Standard FastSim: Smear Energy E' = E * (1 + gauss(0, res)).
    Then scale p3 by (E'/E). This scales mass by same factor.
    """
    factor = 1.0 + random.gauss(0, resolution)
    # Ensure factor is not negative (though unlikely with 10% res)
    factor = max(0.0, factor)
    return p4 * factor

def inv_mass(p4):
    E, px, py, pz = p4
    m2 = E**2 - (px**2 + py**2 + pz**2)
    return math.sqrt(max(0, m2))

print(f"Reading LHE file: {lhe_file}")
if not os.path.exists(lhe_file):
    # Try unzipped
    lhe_file_unzip = lhe_file.replace(".gz", "")
    if os.path.exists(lhe_file_unzip):
        lhe_file = lhe_file_unzip
    else:
        print("Error: LHE file not found. Please run Experiment 38 first.")
        exit(1)

open_func = gzip.open if lhe_file.endswith(".gz") else open
mode = "rt" if lhe_file.endswith(".gz") else "r"

m_parton = []
m_smeared = []

with open_func(lhe_file, mode) as f:
    event_lines = []
    in_event = False
    
    for line in f:
        if "<event>" in line:
            in_event = True
            event_lines = []
            continue
            
        if "</event>" in line:
            in_event = False
            if len(event_lines) < 2: continue
            
            # Parse Particles
            # Line 0 is header, particles from 1
            # Dict: id -> {pdg, moth1, p4}
            p_map = {}
            for i, pline in enumerate(event_lines[1:], start=1):
                parts = pline.strip().split()
                if len(parts) < 10: continue
                pdg = int(parts[0])
                moth1 = int(parts[2])
                p4 = get_p4(parts)
                p_map[i] = {'pdg': pdg, 'moth1': moth1, 'p4': p4}
            
            # Reconstruct (t + h) pairs from same xm mother
            # Logic from Exp 38
            for idx, p in p_map.items():
                if abs(p['pdg']) == 6: # Top
                    moth_idx = p['moth1']
                    if moth_idx in p_map and abs(p_map[moth_idx]['pdg']) == 6000001:
                        # Found top from xm. Look for sibling Higgs.
                        for h_idx, h_p in p_map.items():
                            if h_idx != idx and h_p['pdg'] == 25 and h_p['moth1'] == moth_idx:
                                # Found Pair
                                p_top = p['p4']
                                p_higgs = h_p['p4']
                                
                                # Parton Level Mass
                                m_true = inv_mass(p_top + p_higgs)
                                m_parton.append(m_true)
                                
                                # Smeared Level Mass
                                # Smear independently
                                p_top_sm = smear_p4(p_top, SIGMA_TOP)
                                p_higgs_sm = smear_p4(p_higgs, SIGMA_HIGGS)
                                m_reco = inv_mass(p_top_sm + p_higgs_sm)
                                m_smeared.append(m_reco)
                                break
            continue
            
        if in_event:
            event_lines.append(line)

print(f"Processed {len(m_parton)} candidates.")

# Plotting
plt.figure(figsize=(10, 6))
bins = np.linspace(200, 450, 100)

plt.hist(m_parton, bins=bins, alpha=0.5, label='Parton Level (Ideal)', color='blue', density=True)
plt.hist(m_smeared, bins=bins, alpha=0.5, label='Reconstructed (Smeared)', color='red', density=True, histtype='step', linewidth=2)

plt.xlabel('Invariant Mass M(t, h) [GeV]')
plt.ylabel('Normalized Events')
plt.title(f'Mirror Fermion Mass Reconstruction (Smeared)\nInput Mass=320 GeV, $\sigma_E(t)$={SIGMA_TOP*100}%, $\sigma_E(h)$={SIGMA_HIGGS*100}%')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(200, 450)

# Calculate statistics for smeared
mean_sm = np.mean(m_smeared)
std_sm = np.std(m_smeared)
print(f"Parton Mean: {np.mean(m_parton):.2f}, Width: {np.std(m_parton):.2f}")
print(f"Smeared Mean: {mean_sm:.2f}, Width: {std_sm:.2f}")

plt.text(0.05, 0.95, f'Smeared Peak: {mean_sm:.1f} GeV\nResolution: {std_sm:.1f} GeV', 
         transform=plt.gca().transAxes, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.savefig(output_plot)
print(f"Plot saved to {output_plot}")
