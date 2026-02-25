#!/usr/bin/env python3
"""
Phase 29 — Step 1: Find the CMS AOD file containing run=202016, lumi=209, event=229639465
in the public CMS Open Data (Run2012C DoubleMuParked AOD, record 6030).

Strategy:
  1. Download the file index from CERN Open Data portal
  2. For each file, check the lumi section map (json index) to find which file 
     contains lumi=209 for run=202016
  3. Output the XRootD path for use in event dump

CMS Open Data portal: https://opendata.cern.ch/record/6030
Dataset: /DoubleMuParked/Run2012C-22Jan2013-v1/AOD
XRootD base: root://eospublic.cern.ch//eos/opendata/cms/Run2012C/DoubleMuParked/AOD/22Jan2013-v1/
"""
import urllib.request, json, os, sys

TARGET_RUN  = 202016
TARGET_LUMI = 209
TARGET_EVT  = 229639465

RECORD_ID  = 6030
FILE_INDEX_URL = (
    "https://opendata.cern.ch/record/6030/files/"
    "CMS_Run2012C_DoubleMuParked_AOD_22Jan2013-v1_file_index.json"
)
XROOTD_BASE = "root://eospublic.cern.ch//eos/opendata/cms/Run2012C/DoubleMuParked/AOD/22Jan2013-v1/"

print(f"Phase 29: Locating AOD file for run={TARGET_RUN}, lumi={TARGET_LUMI}, event={TARGET_EVT}")
print(f"Dataset: /DoubleMuParked/Run2012C-22Jan2013-v1/AOD  (CERN Open Data record {RECORD_ID})")
print()

# 1. Download file index
print(f"Downloading file index: {FILE_INDEX_URL}")
try:
    with urllib.request.urlopen(FILE_INDEX_URL, timeout=30) as r:
        raw = r.read()
    file_index = json.loads(raw)
    print(f"  Got {len(file_index)} files in index.")
    file_list = [entry.get("url", entry.get("filename", "")) for entry in file_index]
    print(f"  First file: {file_list[0] if file_list else 'none'}")
except Exception as e:
    print(f"  WARNING: Could not download index ({e})")
    print(f"  Manual access: https://opendata.cern.ch/record/{RECORD_ID}")
    print()
    print("  DAS query (requires CERN GRID cert):")
    print(f"    dasgoclient --query='file run={TARGET_RUN} lumi={TARGET_LUMI} dataset=/DoubleMuParked/Run2012C-22Jan2013-v1/AOD'")
    print()
    print("  XRootD listing:")
    print(f"    xrdfs eospublic.cern.ch ls /eos/opendata/cms/Run2012C/DoubleMuParked/AOD/22Jan2013-v1/ | head -5")
    print()
    print("  Once file is found, run phase29_event_dump.py with FILE_PATH set.")
    sys.exit(0)

# 2. For each file, check if it might contain run 202016 via lumi JSON index
# The CMS Open Data provides per-file lumi section lists in a parallel JSON
# Format: {run: [lumiSections]}
found_files = []
print(f"\nSearching for run={TARGET_RUN}, lumi={TARGET_LUMI} in file index...")
for i, entry in enumerate(file_index):
    url = entry.get("url", entry.get("filename", ""))
    lumi_ranges = entry.get("lumi_sections", entry.get("lumiSections", {}))
    run_str = str(TARGET_RUN)
    if isinstance(lumi_ranges, dict) and run_str in lumi_ranges:
        lumis = lumi_ranges[run_str]
        # lumis is list of [start,end] pairs or flat list
        for item in lumis:
            if isinstance(item, list):
                if item[0] <= TARGET_LUMI <= item[1]:
                    found_files.append(url); break
            elif item == TARGET_LUMI:
                found_files.append(url); break
    elif i < 3 and not lumi_ranges:
        # Index may not have lumi info: report all files need scanning
        pass

if found_files:
    print(f"\nFOUND {len(found_files)} candidate file(s):")
    for f in found_files:
        print(f"  {f}")
    # Write to output file
    outfile = "results/phase29_target_file.txt"
    with open(outfile, "w") as fw:
        for f in found_files:
            fw.write(f + "\n")
    print(f"\nFile path written to: {outfile}")
else:
    print(f"\nLumi info not in index. All {len(file_list)} files are candidates.")
    print("Run phase29_event_dump.py with each file to find the event.")
    outfile = "results/phase29_all_files.txt"
    os.makedirs("results", exist_ok=True)
    with open(outfile, "w") as fw:
        for f in file_list:
            fw.write(f + "\n")
    print(f"File list written to: {outfile}")
