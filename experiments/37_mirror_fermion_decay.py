
import os
import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np
import shutil

# Configuration
mass_points = [320, 400, 500, 600, 800, 1000, 1500, 2000, 3000]
output_stats = []

# Paths
mg5_bin = "../../MG5_aMC_v3_7_0/bin/mg5_aMC"
output_dir = "mirror_fermion_decay_output"

print("Starting Mirror Fermion Decay Width Scan (Experiment 37)")
print("Method: Calculating Partial Width Gamma(xm > t h) directly via 1->2 process generation.")
print("-" * 60)
print(f"{'Mass [GeV]':<15} {'Width [GeV]':<15} {'Gamma/Mass':<15}")
print("-" * 60)

for mass in mass_points:
    # Run MG5 calculation
    current_out = f"{output_dir}_{mass}"
    
    if os.path.exists(current_out):
        shutil.rmtree(current_out)

    # Note: 'set MXm {mass}' updates the mass parameter in the run card/param card
    script_content = f"""
import model MirrorFermion_UFO
generate xm > t h
output {current_out}
launch
set MXm {mass}
set nevents 1000
0
"""

    with open("calc_width.mg5", "w") as f:
        f.write(script_content)
        
    try:
        # Run MG5
        result = subprocess.run([mg5_bin, "calc_width.mg5"], capture_output=True, text=True)
        output = result.stdout
        
        # 3. Parse the width
        # Look for "Width :   1.296" or similar
        # Pattern: "Width :   1.296 +- 4.674e-09 GeV"
        match = re.search(r"Width\s*:\s*([\d\.e\+\-]+)", output)
        
        width = 0.0
        if match:
            width = float(match.group(1))
        else:
            # Fallback: Look for "Cross-section :"
            match = re.search(r"Cross-section\s*:\s*([\d\.e\+\-]+)", output)
            if match:
                width = float(match.group(1))
        
        if width > 0:
            ratio = width / mass
            output_stats.append((mass, width, ratio))
            print(f"{mass:<15.1f} {width:<15.4f} {ratio:<15.6f}")
        else:
            print(f"{mass:<15.1f} {'FAILED':<15} {'N/A':<15}")
            # print(output[-500:]) 
            output_stats.append((mass, 0, 0))
            
    except Exception as e:
        print(f"Error at {mass} GeV: {e}")
        output_stats.append((mass, 0, 0))
    
    # Cleanup directory
    if os.path.exists(current_out):
        shutil.rmtree(current_out)

# 4. Plotting
masses = [x[0] for x in output_stats]
widths = [x[1] for x in output_stats]
ratios = [x[2] for x in output_stats]

plt.figure(figsize=(12, 5))

# Plot Gamma
plt.subplot(1, 2, 1)
plt.plot(masses, widths, 'b-o', label=r'$\Gamma_{x_m}$')
plt.xlabel("Mass $M_{x_m}$ [GeV]")
plt.ylabel("Decay Width $\Gamma$ [GeV]")
plt.title("Mirror Fermion Width vs Mass")
plt.grid(True)
plt.legend()

# Plot Gamma/Mass
plt.subplot(1, 2, 2)
plt.plot(masses, ratios, 'r-s', label=r'$\Gamma/M$')
plt.xlabel("Mass $M_{x_m}$ [GeV]")
plt.ylabel("$\Gamma / M$")
plt.title("Perturbativity check")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("37_mirror_fermion_decay_width.png")
print("\nPlot saved to 37_mirror_fermion_decay_width.png")
