#!/usr/bin/env python3
"""
Fetch CMS DoubleMuParked Run2012B AOD Sample (Record 6004)
This script downloads a single 280MB AOD file to validate the presence of Particle Flow candidates.
"""
import os
import requests
import sys
from tqdm import tqdm

# Configuration
RECORD_ID = "6004"
FILE_NAME = "4804A3F3-CDEC-E211-BC43-00259073E4EA.root"
# XRootD HTTP Gateway for Open Data
URL = "http://opendata.cern.ch/eos/opendata/cms/Run2012B/DoubleMuParked/AOD/22Jan2013-v1/10000/4804A3F3-CDEC-E211-BC43-00259073E4EA.root"

# Robust path handling
tools_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(tools_dir, "../data")

def download_file(url, output_path):
    """Download a file with progress bar."""
    print(f"Downloading AOD sample from: {url}")
    print(f"Target: {output_path}")
    
    # Check if exists
    if os.path.exists(output_path):
        print(f"File already exists: {output_path}")
        return

    # Stream download
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 * 1024 # 1MB

    with open(output_path, 'wb') as file, tqdm(
        desc=FILE_NAME,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            size = file.write(data)
            bar.update(size)
    print("Download complete.")

if __name__ == "__main__":
    # Ensure directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, FILE_NAME)
    
    try:
        download_file(URL, output_path)
    except KeyboardInterrupt:
        print("\nDownload cancelled.")
        try:
            os.remove(output_path)
        except:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
