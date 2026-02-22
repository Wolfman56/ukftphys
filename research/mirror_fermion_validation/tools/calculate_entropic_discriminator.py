#!/usr/bin/env python3
"""
Calculate Entropic Discriminator (D_E) on CMS AOD Data
"""
import sys
import os
import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt
import vector

# Register vector for 4-momentum handling
vector.register_awkward()

def calculate_de(file_path):
    print(f"Loading: {file_path}")
    
    # Open the file
    with uproot.open(file_path) as file:
        events = file["Events"]
        
        # Read Jet Data
        print("Reading Jet Data...")
        prefix = "recoPFJets_ak5PFJets__RECO.obj"
        
        # Get momentum
        pt = events[f"{prefix}.pt_"].array()
        eta = events[f"{prefix}.eta_"].array()
        phi = events[f"{prefix}.phi_"].array()
        mass = events[f"{prefix}.mass_"].array()
        
        # Get specific energy components for Entropy calculation
        # We define D_E based on the macroscopic energy distribution of the jet
        # Components: ChargedHadron, NeutralHadron, Photon, Electron, Muon
        e_ch = events[f"{prefix}.m_specific.mChargedHadronEnergy"].array()
        e_nh = events[f"{prefix}.m_specific.mNeutralHadronEnergy"].array()
        e_ph = events[f"{prefix}.m_specific.mPhotonEnergy"].array()
        e_el = events[f"{prefix}.m_specific.mElectronEnergy"].array()
        e_mu = events[f"{prefix}.m_specific.mMuonEnergy"].array()
        
        # Total Energy (Approximate check)
        e_total = e_ch + e_nh + e_ph + e_el + e_mu
        
        # Calculate Fractions P_i
        # Add small epsilon to avoid div/0
        epsilon = 1e-9
        e_total_safe = np.maximum(e_total, epsilon)
        
        pk_ch = e_ch / e_total_safe
        pk_nh = e_nh / e_total_safe
        pk_ph = e_ph / e_total_safe
        pk_el = e_el / e_total_safe
        pk_mu = e_mu / e_total_safe
        
        # Calculate component entropies individually
        # D_E = - Sum(p * log(p))
        epsilon_log = 1e-9
        
        def entropy_component(p):
            # p * log(p) should go to 0 as p -> 0
            # np.log(p + epsilon) avoids -inf
            return -1.0 * p * np.log(p + epsilon_log)

        term_ch = entropy_component(pk_ch)
        term_nh = entropy_component(pk_nh)
        term_ph = entropy_component(pk_ph)
        term_el = entropy_component(pk_el)
        term_mu = entropy_component(pk_mu)
        
        # Sum over components
        d_e = term_ch + term_nh + term_ph + term_el + term_mu
        
        print(f"Calculated D_E for {len(ak.flatten(d_e))} jets.")
        
        # Filter: High pT jets only (> 30 GeV)
        mask = (pt > 30.0) & (np.abs(eta) < 2.5)
        
        selected_pt = pt[mask]
        selected_de = d_e[mask]
        
        selected_pt_flat = ak.to_numpy(ak.flatten(selected_pt))
        selected_de_flat = ak.to_numpy(ak.flatten(selected_de))
        
        print(f"Selected {len(selected_pt_flat)} jets with pT > 30 GeV.")
        
        # Plots
        output_dir = os.path.join(os.path.dirname(__file__), "../results")
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. D_E Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(selected_de_flat, bins=50, range=(0, 2.0), color='purple', alpha=0.7, label='CMS Data (AOD)')
        plt.xlabel('Entropic Discriminator $D_E$ (Component Entropy)')
        plt.ylabel('Jets')
        plt.title('Entropic Discriminator Distribution for CMS Jets (Rank 1)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.savefig(os.path.join(output_dir, "cms_entropy_distribution.png"))
        print("Saved cms_entropy_distribution.png")
        
        # 2. D_E vs pT (Is entropy correlated with energy?)
        plt.figure(figsize=(10, 6))
        plt.hist2d(selected_pt_flat, selected_de_flat, bins=(50, 50), range=((30, 200), (0, 2.0)), cmap='viridis', cmin=1)
        plt.colorbar(label='Jets')
        plt.xlabel('Jet pT [GeV]')
        plt.ylabel('Entropic Discriminator $D_E$')
        plt.title('Jet Entropy vs Momentum')
        plt.savefig(os.path.join(output_dir, "cms_entropy_vs_pt.png"))
        print("Saved cms_entropy_vs_pt.png")
        
        print("\nAnalysis Complete.")
        print(f"Mean D_E: {np.mean(selected_de_flat):.4f}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.join(script_dir, "../data/4804A3F3-CDEC-E211-BC43-00259073E4EA.root")
    
    target_file = sys.argv[1] if len(sys.argv) > 1 else default_path
    calculate_de(target_file)
