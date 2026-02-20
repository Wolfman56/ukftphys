
import os
import subprocess
import gzip
import matplotlib.pyplot as plt
import numpy as np
import shutil
import math

# Configuration
run_name = "collider_run_01"
output_dir = "mirror_fermion_collider_38"
mg5_bin = "../../MG5_aMC_v3_7_0/bin/mg5_aMC"

# 1. Create the MadGraph Script
print("Starting Experiment 38: Full Mirror Fermion Collider Simulation")
print("-" * 60)

# Check if output directory exists to clean up
if os.path.exists(output_dir):
    print(f"Cleaning previous run directory: {output_dir}")
    shutil.rmtree(output_dir)

script_content = f"""
import model MirrorFermion_UFO
generate p p > xm xm~, (xm > t h), (xm~ > t~ h)
output {output_dir}
launch
set nevents 10000
set ebeam1 6800.0
set ebeam2 6800.0
set use_syst False
0
"""

with open("run_collider_38.mg5", "w") as f:
    f.write(script_content)

# 2. Run MadGraph
print("Running MadGraph5_aMC@NLO...")
try:
    subprocess.run([mg5_bin, "run_collider_38.mg5"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running MadGraph: {e}")
    exit(1)

# 3. Locate and Parse LHE file
lhe_path = os.path.join(output_dir, "Events", "run_01", "unweighted_events.lhe.gz")
if not os.path.exists(lhe_path):
    # Depending on MG5 version/settings, it might not be gzipped or named differently
    lhe_path_unzip = os.path.join(output_dir, "Events", "run_01", "unweighted_events.lhe")
    if os.path.exists(lhe_path_unzip):
        lhe_path = lhe_path_unzip
    else:
        print(f"Error: Could not find LHE file at {lhe_path} or {lhe_path_unzip}")
        exit(1)

print(f"Parsing LHE file: {lhe_path}")

# Invariant Mass Arrays
m_xm_reco = []  # Reconstructed from t + h

def get_p4(parts):
    # LHE format: px, py, pz, E, m
    # indices 6, 7, 8, 9, 10
    px = float(parts[6])
    py = float(parts[7])
    pz = float(parts[8])
    E  = float(parts[9])
    return np.array([E, px, py, pz])

def inv_mass(p4):
    E, px, py, pz = p4
    m2 = E**2 - (px**2 + py**2 + pz**2)
    # Floating point issues can make m2 slightly negative for massless particles
    return math.sqrt(max(0, m2))

# Open file (handle gzip or plain)
open_func = gzip.open if lhe_path.endswith(".gz") else open
mode = "rt"     if lhe_path.endswith(".gz") else "r"

print("Parsing events with parent matching...")

with open_func(lhe_path, mode) as f:
    event_lines = []
    in_event = False
    
    for line in f:
        if "<event>" in line:
            in_event = True
            event_lines = []
            continue
            
        if "</event>" in line:
            in_event = False
            
            # Process the event block
            if len(event_lines) < 2: continue
            
            # Line 0 of event block contains: N_particles, process_id, weight, etc.
            # We skip it for particle parsing, but use it to offset if needed.
            # Particles start at index 1 of event_lines list.
            
            p_map = {}
            
            # Enumerate particles. LHE particles are 1-indexed in Mother refs.
            # event_lines[0] is header. event_lines[1] is particle 1.
            for i, pline in enumerate(event_lines[1:], start=1):
                parts = pline.strip().split()
                if len(parts) < 10: continue
                
                try:
                    pdg = int(parts[0])
                    moth1 = int(parts[2])
                    p4 = get_p4(parts)
                    p_map[i] = {'pdg': pdg, 'moth1': moth1, 'p4': p4}
                except ValueError:
                    continue
            
            # Reconstruct Strategy:
            # 1. Find all 't' (or 't~') particles.
            # 2. Check if their mother is 'xm' (or 'xm~').
            # 3. If so, look for a 'h' with the SAME mother index.
            # 4. Combine physics vectors.
            
            # Note: Mother index points to the line number in the event block.
            
            for idx, p in p_map.items():
                # Check for Top Quark (6) or Anti-Top (-6)
                if abs(p['pdg']) == 6: 
                    top_p4 = p['p4']
                    moth_idx = p['moth1']
                    
                    # Verify mother exists in map
                    if moth_idx in p_map:
                        moth_pdg = p_map[moth_idx]['pdg']
                        
                        # Verify mother is Mirror Fermion (6000001)
                        if abs(moth_pdg) == 6000001:
                            
                            # Search for sibling Higgs (25)
                            # Iterate through other particles
                            for h_idx, h_p in p_map.items():
                                if h_idx == idx: continue # Skip self
                                
                                # Check PDG and Mother
                                if h_p['pdg'] == 25 and h_p['moth1'] == moth_idx:
                                    # Found decay pair (t, h) from same xm!
                                    higgs_p4 = h_p['p4']
                                    
                                    # Calculate Invariant Mass of the pair
                                    # p_sys = p_top + p_higgs
                                    p_sys = top_p4 + higgs_p4
                                    m_reco = inv_mass(p_sys)
                                    
                                    m_xm_reco.append(m_reco)
                                    
                                    # Break inner loop (found the h for this t)
                                    break 
            continue
        
        if in_event:
            event_lines.append(line)



print(f"Reconstructed {len(m_xm_reco)} Mirror Fermion candidates.")

# 4. Plotting
plt.figure(figsize=(10, 6))
plt.hist(m_xm_reco, bins=100, range=(250, 400), alpha=0.7, color='blue', edgecolor='black', label='reco(xm)')
plt.axvline(x=320.0, color='r', linestyle='--', linewidth=2, label='True Mass 320 GeV')
plt.xlabel("Invariant Mass $M(t, h)$ [GeV]")
plt.ylabel("Events / Bin")
plt.title("Constraint: Experiment 38 - Mirror Fermion Mass Peak")
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig("38_mirror_fermion_collider_mass_peak.png")
print("Plot saved to 38_mirror_fermion_collider_mass_peak.png")

# Stats
peak_mean = np.mean(m_xm_reco)
peak_std = np.std(m_xm_reco)
print(f"Reconstructed Peak: {peak_mean:.2f} +/- {peak_std:.2f} GeV")
