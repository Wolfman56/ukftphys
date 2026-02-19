
import os
import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np

# Configuration
mass_points = [200, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000, 2500, 3000]
cross_sections = []
errors = []

# Paths
mg5_bin = "../../MG5_aMC_v3_7_0/bin/mg5_aMC"
output_dir = "mirror_fermion_mass_scan"

# Create a temporary MG5 script for the scan
scan_script_path = "run_mass_scan.mg5"

def create_scan_script(masses):
    with open(scan_script_path, "w") as f:
        f.write("import model MirrorFermion_UFO\n")
        f.write("generate p p > xm xm~\n")
        f.write(f"output {output_dir} -f\n")
        f.write("launch\n")
        f.write("set nevents 100\n")  # Low stats for fast scan
        f.write("set ebeam1 6800.0\n")
        f.write("set ebeam2 6800.0\n")
        # Use the 'scan' feature in MadGraph:
        # scan mass 6000001 [200, 300, ...] 
        # But standard launch supports single point. We can iterate.
        # Alternatively, define a scan in the run_card or param_card.
        # Let's do a loop in Python invoking MG5 for each mass if scan syntax tricky.
        pass

# Actually, looping in Python is safer to parse results.
print("Starting Mass Scan...")

for m in mass_points:
    print(f"Running for M = {m} GeV...")
    
    # Write specific script for this mass
    # Note: re-generating the process every time is inefficient but robust for a short scan.
    # For production, we would generate once and use 'launch' multiple times.
    script_content = f"""
import model MirrorFermion_UFO
generate p p > xm xm~
output {output_dir}_{m} -f
launch
set nevents 1000
set ebeam1 6800.0
set ebeam2 6800.0
set MXm {float(m)}
set WXm 1.0  # Set a dummy width to avoid narrow width warnings/errors if any
0
quit
"""
    with open(scan_script_path, "w") as f:
        f.write(script_content)

    print(f"  Running MG5 for Mass {m}...")
    try:
        # Run MG5
        # We need to capture stdout to parse the cross-section
        result = subprocess.run([mg5_bin, scan_script_path], capture_output=True, text=True, timeout=600)
        
        # Parse cross-section from output
        # Look for: "Cross-section :   1.234 +- 0.005 pb" or "2.8125e+01 +/- 1.43e-01 pb"
        # Regex to handle floats and scientific notation
        match = re.search(r"Cross-section :\s+([\d\.eE\+\-]+)\s+\+-\s+([\d\.eE\+\-]+)\s+pb", result.stdout)
        if match:
            xs = float(match.group(1))
            err = float(match.group(2))
            cross_sections.append(xs)
            errors.append(err)
            print(f"  Result: {xs} +/- {err} pb")
        else:
            print("  Error: Could not parse cross-section.")
            cross_sections.append(0.0)
            errors.append(0.0)
            
    except subprocess.TimeoutExpired:
        print("  Error: Validation timed out.")
        cross_sections.append(0.0)
        errors.append(0.0)
    except Exception as e:
        print(f"  Error: {e}")
        cross_sections.append(0.0)
        errors.append(0.0)

# Clean up
if os.path.exists(scan_script_path):
    os.remove(scan_script_path)

# Filter out failed runs
valid_mask = np.array(cross_sections) > 0
m_val = np.array(mass_points)[valid_mask]
xs_val = np.array(cross_sections)[valid_mask]
err_val = np.array(errors)[valid_mask]

# Plot
plt.figure(figsize=(8, 6))
plt.errorbar(m_val, xs_val, yerr=err_val, fmt='o-', label='MadGraph5 LO', capsize=3)
plt.yscale('log')
plt.title(r'Mirror Fermion Pair Production $\sigma(pp \to x_m \bar{x}_m)$')
plt.xlabel(r'Mass $M_{x_m}$ [GeV]')
plt.ylabel(r'Cross Section [pb]')
plt.grid(True, which="both", ls="-", alpha=0.5)

# Add 1/M^2 trend line for comparison (normalized to first point)
if len(m_val) > 0:
    ref_m = m_val[0]
    ref_xs = xs_val[0]
    trend = ref_xs * (ref_m / m_val)**5  # PDF suppression makes it steeper than 1/s
    plt.plot(m_val, trend, '--', label=r'$\sim 1/M^5$ (PDF approx)')

plt.legend()
plt.tight_layout()
plt.savefig('36_mirror_fermion_mass_scan.png')
print("Scan complete. Plot saved to 36_mirror_fermion_mass_scan.png")
