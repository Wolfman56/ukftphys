
import numpy as np
import matplotlib.pyplot as plt

def run_experiment_53(n_events_mc=10000):
    """
    Simulate Jet Substructure for Mirror Fermion Decay (M -> 3j)
    Goal: Identify the 'D_E' Entropic Discriminator peak.
    """
    print(f"Running Experiment 53 (N={n_events_mc})...")
    
    # 1. Physics Model
    # Mirror Fermion Mass
    M_mirror = 320.0 # GeV
    
    # Standard Model Background (Main QCD jets)
    # Background: continuous distribution of jet masses
    bg_masses = np.random.exponential(scale=100.0, size=n_events_mc)
    bg_substructure_variable = np.random.normal(loc=0.2, scale=0.1, size=n_events_mc) # 'N-subjettiness' tau_32
    
    # Signal: Mirror Fermion (M -> q q q)
    # Signal: Peak at M=320 GeV
    sig_masses = np.random.normal(loc=M_mirror, scale=15.0, size=int(n_events_mc * 0.05)) # 5% signal
    # Signal Substructure: Very low tau_32 (3-prong, 'Mercedes' topology)
    sig_substructure_variable = np.random.normal(loc=0.05, scale=0.02, size=int(n_events_mc * 0.05))
    
    # Combine
    all_masses = np.concatenate([bg_masses, sig_masses])
    all_taus = np.concatenate([bg_substructure_variable, sig_substructure_variable])
    
    # 2. Compute Entropic Discriminator 'D_E'
    # D_E = -Sum(p_i log p_i) of constituents within the fat jet
    # Approx: D_E ~ 1/tau_32
    # For Signal (3-prong): tau_32 small -> D_E high
    # For Background (1 or 2-prong): tau_32 large -> D_E low
    
    D_E = 1.0 / (all_taus + 0.01) # Avoid div/0
    
    # 3. Apply Cuts
    # Select high D_E region
    cut_mask = D_E > 5.0
    
    selected_masses = all_masses[cut_mask]
    
    # 4. Analysis
    print(f"Total Events: {len(all_masses)}")
    print(f"Events passing D_E > 5.0: {len(selected_masses)}")
    
    # 5. Plot
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.hist(all_masses, bins=50, range=(0, 600), alpha=0.5, label='Inclusive')
    plt.hist(selected_masses, bins=50, range=(0, 600), alpha=0.8, color='red', label='High Entropic Discrim.')
    plt.axvline(M_mirror, color='k', linestyle='--', label='Mirror Mass (320)')
    plt.xlabel('Jet Mass (GeV)')
    plt.ylabel('Events')
    plt.legend()
    plt.title('Jet Mass Distribution (Background + Signal)')
    
    plt.subplot(1, 2, 2)
    plt.hist(D_E, bins=50, range=(0, 20), color='purple', alpha=0.7)
    plt.xlabel('Entropic Discriminator D_E')
    plt.ylabel('Events')
    plt.title('Discriminator Distribution')
    
    plt.tight_layout()
    plt.savefig('experiment_53_results.png')
    print("\nSaved plot to experiment_53_results.png")
    
    # Check for excess
    # Window [300, 340]
    window_mask = (selected_masses > 300) & (selected_masses < 340)
    n_signal_region = np.sum(window_mask)
    # Sidebands
    sideband_mask = ((selected_masses > 260) & (selected_masses < 300)) | ((selected_masses > 340) & (selected_masses < 380))
    n_sideband = np.sum(sideband_mask)
    
    print(f"Signal Region [300-340]: {n_signal_region}")
    print(f"Sideband Region (Control): {n_sideband}")
    significance = (n_signal_region - n_sideband) / np.sqrt(n_sideband + 1.0) # Approx S/sqrt(B)
    
    print(f"Estimated Significance: {significance:.2f} sigma")
    
    if significance > 3.0:
        print(">> SUCCESS: Strong evidence for Mirror Fermion decay topology.")
    else:
        print(">> INAPPROPRIATE: Signal too weak or background too high.")

if __name__ == "__main__":
    run_experiment_53() 
