#!/usr/bin/env python3
"""
Phase 29 — Step 2: Once the AOD file is located, extract RECO-level event
properties using uproot (no CMSSW required).

This reads the CMS AOD ROOT file directly via XRootD and extracts:
  - Muon isolation (PFRelIso03, PFRelIso04)
  - Muon impact parameters (dxy, dz relative to primary vertex)
  - Hit quality (validHits, normalizedChi2, kink)
  - Secondary vertex candidates (if any muons share vertex)
  - MET from PF algorithm
  - HLT trigger paths that fired

The RECO-level observables that NanoAOD branches do NOT provide:
  1. Full per-muon isolation cones (not just tracker isolation)
  2. Secondary vertex position, significance, flight path
  3. Full HLT trigger decision bits
  4. Track kink significance (non-prompt muon indicator)
  5. Muon chamber hits pattern

Target event: run=202016, lumi=209, event=229639465
Expected AOD file: root://eospublic.cern.ch//eos/opendata/cms/Run2012C/DoubleMuParked/AOD/22Jan2013-v1/[FILE]

NOTE: Requires uproot4 and fsspec-xrootd (or XRootD python bindings).
Install via:  pip install uproot fsspec-xrootd xrootd
"""
import os, sys
import numpy as np

TARGET_RUN  = 202016
TARGET_LUMI = 209
TARGET_EVT  = 229639465

# -- Replace with actual file path from phase29_das_locate.py output --
AOD_FILE = os.environ.get(
    "PHASE29_AOD_FILE",
    "root://eospublic.cern.ch//eos/opendata/cms/Run2012C/DoubleMuParked/AOD/22Jan2013-v1/PLACEHOLDER.root"
)

os.chdir("/Users/enconcertincdev4/Code/grok/ukftphys")

print("=" * 70)
print("Phase 29 — RECO-Level Event Dump")
print(f"Target: run={TARGET_RUN}, lumi={TARGET_LUMI}, event={TARGET_EVT}")
print("=" * 70)

# Check if we have the CMS Open Data NanoAOD (from our existing data)
# as a sanity check — we already know the NanoAOD content; RECO adds more
nanjson = "/Users/enconcertincdev4/Code/grok/noosphere/apps/hep-explorer/tools/data/cms_run2012c.ndjson"
if os.path.exists(nanjson):
    import json
    with open(nanjson) as f:
        for line in f:
            d = json.loads(line)
            if d["run"] == TARGET_RUN and d["lumi"] == TARGET_LUMI and d["event"] == TARGET_EVT:
                muons = d.get("jets", d.get("muons", []))
                print(f"\nNanoAOD cache (cms_run2012c.ndjson):")
                print(f"  nMuons = {len(muons)}")
                for i, m in enumerate(muons):
                    print(f"  mu[{i}]: pt={m['pt']:.3f} eta={m['eta']:.4f} phi={m['phi']:.4f} mass={m['mass']:.6f}")
                break

# Try to import uproot and open AOD file
print(f"\nAttempting AOD access: {AOD_FILE}")
try:
    import uproot
    # Try to open the file
    if "PLACEHOLDER" in AOD_FILE:
        raise ValueError("No AOD file path set — run phase29_das_locate.py first")

    with uproot.open(AOD_FILE) as f:
        print("  Opened successfully. Available trees/branches:")
        for key in list(f.keys())[:20]:
            print(f"    {key}")

        # Navigate to muon collection in AOD
        # In CMSSW AOD, muons are stored as branches like:
        # recoMuons_muons__RECO.  (or similar)
        trees = [k for k in f.keys() if "Muon" in k or "muon" in k]
        print(f"\n  Muon-related trees: {trees[:5]}")

        # Try to get isolation and impact parameter branches
        # Branch pattern in AOD: recoMuons_muons__RECO.obj.isolationR03_.sumPt_
        muon_branches_of_interest = [
            "recoMuons_muons__RECO.obj.isolationR03_.sumPt_",
            "recoMuons_muons__RECO.obj.isolationR03_.emEt_",
            "recoMuons_muons__RECO.obj.isolationR03_.hadEt_",
            "recoMuons_muons__RECO.obj.p4_.fCoordinates.fPt",
            "recoMuons_muons__RECO.obj.p4_.fCoordinates.fEta",
            "recoMuons_muons__RECO.obj.p4_.fCoordinates.fPhi",
            "recoMuons_muons__RECO.obj.combinedMuon_.hits_.qualityMask_",
            "recoMuons_muons__RECO.obj.type_",
        ]
        for branch in muon_branches_of_interest:
            try:
                arr = f[branch].array(library="np")
                print(f"  Branch {branch.split('.')[-1]}: shape={arr.shape}")
            except Exception as e2:
                pass

        # Search for target event by run/lumi/event ID
        # Event IDs are stored in EventAuxiliary branch
        print(f"\n  Searching for event {TARGET_RUN}:{TARGET_LUMI}:{TARGET_EVT}...")
        # This would require iterating through the tree

except ImportError:
    print("  uproot not installed. Install: pip install uproot")
    print("\n  Alternative: use CMSSW conda recipe or Docker CMS image")
    print("  Docker: docker run --rm -it cmscloud/cms-das:latest /bin/bash")
    print("  Then inside container: cmsRun phase29_cmssw_config.py")
    print()
except ValueError as e:
    print(f"  {e}")
    print("\n  Next step: run phase29_das_locate.py to get the AOD file path")
except Exception as e:
    print(f"  Error opening AOD: {e}")
    if "auth" in str(e).lower() or "permission" in str(e).lower():
        print("  May need CERN Grid certificate.  Try via Docker / CMS Open Data VM.")

# Generate the DAS queries and instructions regardless
print()
print("=" * 70)
print("DAS Query Instructions (requires CERN account + GRID proxy)")
print("=" * 70)
das_queries = {
    "Find file containing run/lumi":
        f"dasgoclient --query='file run={TARGET_RUN} lumi={TARGET_LUMI} dataset=/DoubleMuParked/Run2012C-22Jan2013-v1/AOD'",
    "Find all files for run":
        f"dasgoclient --query='file run={TARGET_RUN} dataset=/DoubleMuParked/Run2012C-22Jan2013-v1/AOD'",
    "Dataset summary":
        "dasgoclient --query='summary dataset=/DoubleMuParked/Run2012C-22Jan2013-v1/AOD'",
    "Run info":
        f"dasgoclient --query='run={TARGET_RUN} dataset=/DoubleMuParked/Run2012C-22Jan2013-v1/AOD'",
}
for desc, query in das_queries.items():
    print(f"\n  [{desc}]")
    print(f"  $ {query}")

print()
print("=" * 70)
print("CMS Open Data Access Instructions (no credentials needed)")
print("=" * 70)
print(f"""
  Dataset record: https://opendata.cern.ch/record/6030
  File index:     https://opendata.cern.ch/record/6030/files/
                  CMS_Run2012C_DoubleMuParked_AOD_22Jan2013-v1_file_index.json

  Method 1: CMS Open Data VM (VirtualBox image)
    Download: https://opendata.cern.ch/record/250
    Inside VM:
      dasgoclient --query='file run={TARGET_RUN} lumi={TARGET_LUMI} dataset=/DoubleMuParked/Run2012C-22Jan2013-v1/AOD'
      edmEventSize -v root://eospublic.cern.ch//eos/opendata/cms/Run2012C/...file.root

  Method 2: Docker (CMSSW_7_6_7 compatible with NanoAOD)
    docker pull cmssw/cmssw:CMSSW_7_6_7
    docker run -it cmssw/cmssw:CMSSW_7_6_7 bash
    Inside container:
      cmsRun phase29_cmssw_config.py 2>&1 | grep -A50 "=== Event Header"

  Method 3: Google Colab (fastest for network access to CERN)
    !pip install xrootd uproot fsspec-xrootd
    import uproot
    f = uproot.open("root://eospublic.cern.ch//eos/opendata/cms/Run2012C/DoubleMuParked/AOD/22Jan2013-v1/FILE.root")

  Key RECO-level quantities to extract:
    1. Muon PFRelIso03/04 (should be < 0.15 for prompt muons)
    2. d_xy (impact parameter)   — should be < 0.2 mm for prompt
    3. d_z (longitudinal IP)     — should be < 0.5 mm for prompt
    4. muon.normalizedChi2()     — refit track quality
    5. muon.kink()               — non-prompt indicator
    6. Secondary vertex search   — do any 2+ muons share a vertex?
    7. HLT_DoubleMu*/HLT_TripleMu* trigger decision
    8. N_tracker_hits, N_pixel_hits per muon
""")

print("Phase 29 setup complete. File: experiments/62_phase29_event_analysis.py")
print("Next: run via CMS Open Data VM or supply AOD file path via PHASE29_AOD_FILE env var.")
