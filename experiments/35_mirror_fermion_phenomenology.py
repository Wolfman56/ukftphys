
import gzip
import matplotlib.pyplot as plt
import numpy as np

# Path to LHE file
lhe_path = "../results/mirror_fermion_run_01/Events/run_01/unweighted_events.lhe.gz"

# Parse the LHE file manually since pylhe might not be installed
events = []
current_event = []
in_event = False

try:
    with gzip.open(lhe_path, 'rt') as f:
        for line in f:
            if '<event>' in line:
                in_event = True
                current_event = []
                continue
            if '</event>' in line:
                in_event = False
                events.append(current_event)
                continue
            if in_event:
                if not line.strip(): continue
                parts = line.split()
                # Skip the event header line (Nup, IDPRUP, XWGTUP...) which has fewer columns usually or distinct IDPRUP
                if len(parts) > 6: 
                    # Standard LHE particle line: ID, Status, Mother1, Mother2, Color1, Color2, Px, Py, Pz, E, M, Vtim, Spin
                    try:
                        pid = int(parts[0])
                        status = int(parts[1])
                        px = float(parts[6])
                        py = float(parts[7])
                        pz = float(parts[8])
                        e = float(parts[9])
                        m = float(parts[10]) # Mass
                        current_event.append({'pid': pid, 'status': status, 'p': (px, py, pz, e), 'm': m})
                    except ValueError:
                        pass # Header line
except FileNotFoundError:
    print(f"Error: file {lhe_path} not found.")
    exit(1)

print(f"Loaded {len(events)} events.")

# Extract invariant mass of the xm-xm~ pair (PID 6000001)
invariant_masses = []
xm_masses = []

for event in events:
    # Find the two outgoing mirror fermions (status might be 1 (final) or 2 (intermediate) depending on decay)
    # In unweighed_events.lhe from MG5, final state particles usually have status 1.
    # But since we didn't specify decays, they are stable in the event record (status 1).
    xms = [p for p in event if abs(p['pid']) == 6000001]
    
    if len(xms) >= 2:
        p1 = np.array(xms[0]['p'])
        p2 = np.array(xms[1]['p'])
        
        # Invariant Mass^2 = (E1+E2)^2 - (p1+p2)^2
        p_sum = p1 + p2
        e_sum = p_sum[3]
        vec_sum = p_sum[:3]
        inv_mass_sq = e_sum**2 - np.sum(vec_sum**2)
        if inv_mass_sq > 0:
            invariant_masses.append(np.sqrt(inv_mass_sq))
        
        xm_masses.append(xms[0]['m'])
        xm_masses.append(xms[1]['m'])

# Plot
plt.figure(figsize=(10, 5))

# Plot 1: Invariant Mass of the pair
plt.subplot(1, 2, 1)
plt.hist(invariant_masses, bins=20, color='skyblue', edgecolor='black')
plt.title(r'Invariant Mass of $x_m \bar{x}_m$ Pair')
plt.xlabel(r'$M_{x_m \bar{x}_m}$ [GeV]')
plt.ylabel('Events')
plt.grid(True, alpha=0.3)

# Plot 2: Mass of individual xm (Validation)
plt.subplot(1, 2, 2)
plt.hist(xm_masses, bins=10, color='lightgreen', edgecolor='black')
plt.title(r'reconstructed $x_m$ Mass')
plt.xlabel(r'$M_{x_m}$ [GeV]')
# Force x-axis to show the peak clearly
plt.xlim(min(xm_masses)-1, max(xm_masses)+1)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('35_mirror_fermion_madgraph.png')
print("Plot saved to 35_mirror_fermion_madgraph.png")
