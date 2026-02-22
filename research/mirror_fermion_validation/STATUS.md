# Mirror Fermion Validation - Status Report

**Date**: February 21, 2026
**Time**: ~3:30 PM (Local)

## Phase 1: Data Acquisition & Validation
- **Status**: **COMPLETE / SUCCESS**
- **Dataset**: `Run2012BC_DoubleMuParked_Muons.root` (2.1 GB)
- **Total Events Processed**: 61,540,413
- **Validation**:
    - **Dimuon Events**: 53,271,246
    - **Z-Boson Candidates (60-120 GeV range)**: 8,266,469
    - **Artifact**: `analysis/visuals/cms_z_peak_validation.png` (Z-Peak clearly visible at ~91 GeV).

## Phase 2: Entropic Scattering Test
- **Hypothesis**: Look for high-entropy recoil in $Z \to \mu\mu$ events.
- **Current Status**: **PENDING NEW DATA**
- **Blocker**: The Phase 1 dataset (Outreach Tool) contains **only Muon branches**.
    - *Missing*: Jets, Tracks, Particle Flow Candidates.
    - *Impact*: We verified the Z boson, but we cannot calculate the Entropic Discriminator ($D_E$) without hadronic recoil data.
- **Action Required**: Locate the full **AOD (Analysis Object Data)** or a NanoAOD that includes Jet/PF collections for this same run period (Run2012B/C).

## Actions Taken
1.  **Pipeline**: Implemented chunked processing in `tools/fetch_cms_doublemuon.py` (handles >2GB files).
2.  **Validation**: Updated `tools/check_mirror_fermion_hypothesis.py` to act as a **Z-Peak Validator**.
3.  **Cleanup**: Consolidated scripts into `tools/` and removed legacy `loaders/`.

## Next Session Objectives
1.  **Search**: Find the CMS 2012 **AOD** dataset (Record 6021 or similar) with Particle Flow information.
2.  **Update**: Modify `tools/fetch_cms_doublemuon.py` to handle AOD structure (more complex ROOT tree).
3.  **Analysis**: Run the full Entropic Discriminator logic on the new dataset.