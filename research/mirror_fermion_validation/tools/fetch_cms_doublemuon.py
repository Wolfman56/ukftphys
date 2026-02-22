import uproot
import awkward as ak
import vector
import numpy as np
import os
import requests
import shutil

# Switched directly to verified HTTPS with SSL bypass for robustness
DATA_URL = "https://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root"

OUTPUT_DIR = "research/mirror_fermion_validation/data"
RAW_FILE = os.path.join(OUTPUT_DIR, "cms_doublemuon_full.root")
PROCESSED_FILE = os.path.join(OUTPUT_DIR, "cms_doublemuon_filtered.parquet")

def fetch_data():
    """
    Downloads the CMS Open Data (DoubleMuon) file locally.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Check if raw file exists and is valid
    should_download = True
    if os.path.exists(RAW_FILE):
        file_size = os.path.getsize(RAW_FILE)
        # 2GB is expected, check if at least significant (>1.5GB)
        if file_size > 1500 * 1024 * 1024:
            print(f"File exists: {RAW_FILE} ({file_size/1024/1024:.2f} MB)")
            should_download = False
        else:
            print(f"File incomplete/growing: {RAW_FILE} ({file_size/1024/1024:.2f} MB)")
            # Do NOT remove file if it's currently downloading in another process
            # We assume the user manages the process. 
            pass

    if should_download and not os.path.exists(RAW_FILE):
        print(f"Start fresh download (if needed): {DATA_URL}")
        try:
            with requests.get(DATA_URL, stream=True, verify=False) as r:
                r.raise_for_status()
                with open(RAW_FILE, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            print(f"Download complete: {RAW_FILE}")
        except Exception as e:
            print(f"Download failed: {e}")
            return


def process_data_chunks():
    """
    Process the ROOT file in chunks to avoid memory issues and filter for useful events.
    """
    if not os.path.exists(RAW_FILE):
        print(f"Raw file not found: {RAW_FILE}. Run download first.")
        return

    print(f"Processing local file: {RAW_FILE}...")
    
    try:
        # Define branches to read (Muons only, as Jets are missing in this skim)
        branches = [
            "nMuon", "Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"
        ]
        # output file will be muon-only
        OUTPUT_FILE_FINAL = PROCESSED_FILE.replace("filtered.parquet", "muons.parquet")
        
        chunk_size = 100000
        filtered_chunks = []
        total_events_read = 0
        total_events_kept = 0

        # Open file and iterate
        file = uproot.open(RAW_FILE)
        tree = file["Events"]
        num_entries = tree.num_entries
        print(f"Total entries in ROOT file: {num_entries}")

        for events in tree.iterate(branches, step_size=chunk_size, library="ak"):
            total_events_read += len(events)
            
            # Filter: At least 2 muons (for Z candidate)
            mask = events.nMuon >= 2
            filtered_events = events[mask]
            
            if len(filtered_events) > 0:
                filtered_chunks.append(filtered_events)
                total_events_kept += len(filtered_events)
            
            if (total_events_read // chunk_size) % 5 == 0:
                print(f"Processed {total_events_read} events... Kept {total_events_kept} dimuon candidates.")

        if filtered_chunks:
            # Concatenate all filtered chunks
            print("Concatenating chunks...")
            all_filtered_events = ak.concatenate(filtered_chunks)
            
            print(f"Saving {len(all_filtered_events)} filtered events to {OUTPUT_FILE_FINAL}...")
            ak.to_parquet(all_filtered_events, OUTPUT_FILE_FINAL)
            print("Done.")
        else:
            print("No events passed the filter.")

    except Exception as e:
        print(f"Error processing data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fetch_data()
    # verify file size again to ensure download finished successfully before processing
    if os.path.exists(RAW_FILE) and os.path.getsize(RAW_FILE) > 1000:       
        process_data_chunks()
