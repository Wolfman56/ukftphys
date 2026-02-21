#!/usr/bin/env python3
import os
import re
import subprocess
import argparse
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration
MG5_PATH = "/Users/enconcertincdev4/Code/grok/MG5_aMC_v3_7_0/bin/mg5_aMC"
MODEL_NAME = "MirrorFermion_UFO"
OUTPUT_DIR = "results/mg5_width_scan"

def create_mg5_script(mass, run_name):
    """
    Creates a MadGraph script to calculate the decay width of the Mirror Fermion (xm)
    for a given mass.
    """
    script_content = f"""
import model {MODEL_NAME}
generate xm > t h
output {OUTPUT_DIR}/{run_name} -f
launch
set MXm {mass}
set nevents 1000
set time_of_flight 0
done
"""
    return script_content

def run_mg5(script_content, run_name):
    """
    Runs the MadGraph script and returns the width (cross section).
    """
    script_file = f"temp_{run_name}.mg5"
    with open(script_file, "w") as f:
        f.write(script_content)
    
    print(f"Running MG5 for {run_name}...")
    try:
        # Run MG5 and capture output
        # Verify MG5_PATH exists
        if not os.path.exists(MG5_PATH):
           raise FileNotFoundError(f"MG5 binary not found at {MG5_PATH}")

        result = subprocess.run(
            [MG5_PATH, script_file], 
            capture_output=True, 
            text=True,
            check=True
        )
        output = result.stdout
        
        # Parse the output for the result
        # For a decay process A > B C, the "Cross section (pb)" reported by MG5 is actually the Width (GeV) * conversion factor?
        # WAIT: MadGraph reports "Cross-section :   X.XXXXe+XX pb"
        # If the comprehensive width is computed, it usually says "Computed width : ...".
        # However, for 1->N processes, MG5 outputs the partial width in GeV? 
        # Actually, MG5 usually reports cross sections in pb. 
        # But if the initial state is a single particle, it calculates the partial decay width.
        # The unit is GeV.
        # Let's check standard MG5 behavior for 1 particle initial state.
        # "If you generate a decay process, the cross section is the decay width in GeV."
        # Confirming this assumption is key.
        
        # Try to parse Width (for decay) or Cross-section (for scattering)
        # Pattern: "Width :   1.234e+00 +- 1.2e-03 GeV"
        # Pattern: "Cross-section :   1.234e+00 +- 1.2e-03 pb"
        
        match_width = re.search(r"Width\s*:\s*([\d\.eE\+\-]+)\s+\+-", output)
        match_xs = re.search(r"Cross-section\s*:\s*([\d\.eE\+\-]+)\s+\+-", output)
        
        if match_width:
            return float(match_width.group(1))
        elif match_xs:
            return float(match_xs.group(1))
        else:
            print("Could not parse width from MG5 output.")
            print("--- MG5 OUTPUT SNIPPET (LAST 2000 CHARS) ---")
            print(output[-2000:])  # Print last 2000 chars to see results
            print("--- END SNIPPET ---")
            return None

    except subprocess.CalledProcessError as e:
        print(f"MG5 Execution Failed: {e}")
        print(e.stderr)
        return None
    finally:
        if os.path.exists(script_file):
            os.remove(script_file)

def main():
    parser = argparse.ArgumentParser(description="Automated MadGraph Width Scan for Mirror Fermion")
    parser.add_argument("--min_mass", type=float, default=300.0, help="Minimum mass (GeV)")
    parser.add_argument("--max_mass", type=float, default=1000.0, help="Maximum mass (GeV)")
    parser.add_argument("--steps", type=int, default=5, help="Number of mass steps")
    args = parser.parse_args()

    masses = np.linspace(args.min_mass, args.max_mass, args.steps)
    widths = []

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Starting Width Scan for {MODEL_NAME} (xm > t h)")
    print(f"Mass Range: {args.min_mass} - {args.max_mass} GeV")
    
    for m in masses:
        run_name = f"run_mass_{int(m)}"
        script = create_mg5_script(m, run_name)
        width = run_mg5(script, run_name)
        
        if width is not None:
            widths.append(width)
            print(f"Mass: {m:.1f} GeV -> Width: {width:.4e} GeV")
        else:
            widths.append(0.0)
            
    # Save results
    results_file = os.path.join(OUTPUT_DIR, "width_scan_results.txt")
    with open(results_file, "w") as f:
        f.write("Mass(GeV)\tWidth(GeV)\n")
        for m, w in zip(masses, widths):
            f.write(f"{m}\t{w}\n")
            
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(masses, widths, 'ro-', label=r'$\Gamma(X_m \to t h)$')
    plt.xlabel("Mirror Fermion Mass (GeV)")
    plt.ylabel("Decay Width (GeV)")
    plt.title(f"Mirror Fermion Partial Width Scan\nModel: {MODEL_NAME}")
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(OUTPUT_DIR, "width_scan_plot.png"))
    print(f"Results saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
