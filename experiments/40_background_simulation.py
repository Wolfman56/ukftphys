import os
import subprocess
import shutil

# Configuration
run_name = "background_run_01"
output_dir = "background_simulation_40"
mg5_bin = "../../MG5_aMC_v3_7_0/bin/mg5_aMC"

# 1. Create the MadGraph Script
print("Starting Experiment 40: Standard Model Background Simulation")
print("-" * 60)

if os.path.exists(f"{output_dir}_tth"):
    print(f"Cleaning previous run directory: {output_dir}_tth")
    shutil.rmtree(f"{output_dir}_tth")
if os.path.exists(f"{output_dir}_tt"):
    print(f"Cleaning previous run directory: {output_dir}_tt")
    shutil.rmtree(f"{output_dir}_tt")

# Define Process 1: Top Pair (tt~) + Higgs (h)
script_content_1 = f"""
import model sm
generate p p > t t~ h
output {output_dir}_tth
launch
set nevents 1000
set ebeam1 6800.0
set ebeam2 6800.0
0
"""

with open("run_background_tth_40.mg5", "w") as f:
    f.write(script_content_1)

# Define Process 2: Top Pair (tt~)
script_content_2 = f"""
import model sm
generate p p > t t~
output {output_dir}_tt
launch
set nevents 1000
set ebeam1 6800.0
set ebeam2 6800.0
0
"""

with open("run_background_tt_40.mg5", "w") as f:
    f.write(script_content_2)

# 2. Run MadGraph
print("Running MadGraph for SM tth process...")
try:
    subprocess.run([mg5_bin, "run_background_tth_40.mg5"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running MadGraph (tth): {e}")

print("\nRunning MadGraph for SM tt~ process...")
try:
    subprocess.run([mg5_bin, "run_background_tt_40.mg5"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running MadGraph (tt~): {e}")

# 3. Parse Results
def get_cross_section(run_dir):
    # Try reading from crossx.html
    html = os.path.join(run_dir, "crossx.html")
    if os.path.exists(html):
        # Look for "Cross-section : "
        with open(html, "r") as f:
            for line in f:
                if "Cross-section" in line:
                    # Typical line: <td align=center> <a href="./hits.html"> 0.5085 &plusmn; 0.002 </a> </td>
                    # Or in summary: <b> Cross-section : </b> 0.5085 +- 0.002 pb
                    # Let's try to extract numbers
                    try:
                        # Find numbers
                        parts = line.split()
                        # This is very fragile. Let's rely on user reading the terminal output if this fails.
                        return line.strip()
                    except:
                        pass
    return "Not found (Check terminal output)"


print("\n" + "="*60)
print("EXPERIMENT 40 RESULTS: CROSS SECTIONS (13.6 TeV)")
print("="*60)

sigma_tth = get_cross_section(f"{output_dir}_tth")
sigma_tt = get_cross_section(f"{output_dir}_tt")

print(f"SM p p > t t~ h  : {sigma_tth}")
print(f"SM p p > t t~    : {sigma_tt}")
print("-" * 60)
print("Signal (xm xm)   : ~26.63 pb (From Exp 38)")
print("="*60)

