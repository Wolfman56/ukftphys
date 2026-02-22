#!/usr/bin/env python3
"""
Inspect CMS AOD Root File Content
Checks for the presence of Particle Flow Jets and Tracks.
"""
import sys
import os
import uproot
import warnings

# Suppress warnings about unknown branches in ROOT files.
warnings.filterwarnings("ignore")

def inspect_file(file_path):
    print(f"Inspecting: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    try:
        with uproot.open(file_path) as file:
            # Check for standard tree names
            tree_names = [k for k in file.keys() if "Events" in k]
            if not tree_names:
                print("Error: 'Events' tree not found in file.")
                print(f"Keys found: {file.keys()}")
                return

            # Use the first 'Events' tree found (likely 'Events;1')
            tree_name = tree_names[0]
            print(f"Opening tree: {tree_name}")
            events = file[tree_name]
            
            try:
                n_entries = events.num_entries
                print(f"Events loaded. Total entries: {n_entries}")
            except Exception as e:
                print(f"Could not read num_entries: {e}")
                return

            # Define specific branch patterns we need for Entropic Discriminator
            # We need:
            # 1. Jet Collection (e.g., ak5PFJets)
            # 2. Track Collection (e.g., generalTracks)
            required_patterns = {
                "Jets": ["recoPFJets", "ak5PFJets"],
                "Tracks": ["recoTracks", "generalTracks"]
            }
            
            all_branches = events.keys()
            found_summary = {}

            print("\n--- Searching for Physics Objects ---")
            
            for category, patterns in required_patterns.items():
                print(f"\nChecking {category}:")
                found_in_category = []
                for pattern in patterns:
                    # Case insensitive search
                    matches = [b for b in all_branches if pattern.lower() in b.lower()]
                    if matches:
                        found_in_category.extend(matches)
                        print(f"  Found matches for '{pattern}':")
                        for m in matches:
                            print(f"    - {m}")
                
                if not found_in_category:
                    print(f"  ❌ No matches found for {category}")
                    found_summary[category] = False
                else:
                    found_summary[category] = True

            print("\n--- Verification Result ---")
            if all(found_summary.values()):
                print("✅ SUCCESS: Dataset contains necessary physics objects for Phase 2 (Entropic Discriminator).")
            else:
                missing = [k for k, v in found_summary.items() if not v]
                print(f"⚠️  WARNING: Missing objects: {', '.join(missing)}")
                print("   This dataset may not be suitable for the Mirror Fermion analysis.")

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Default to the known file name if not provided
    # Adjust path to be relative to this script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.join(script_dir, "../data/4804A3F3-CDEC-E211-BC43-00259073E4EA.root")
    
    target_file = sys.argv[1] if len(sys.argv) > 1 else default_path
    inspect_file(target_file)
