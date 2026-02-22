# Mirror Fermion Validation - Status Report

**Date**: February 21, 2026
**Time**: ~2:00 PM (Local)

## Phase 1: Data Acquisition & Validation
- **Status**: **COMPLETE / SUCCESS** (with caveat)
- **Dataset**: `Run2012BC_DoubleMuParked_Muons.root` (2.1 GB)
- **Total Events Processed**: 61,540,413
- **Validation**:
    - **Dimuon Events**: 53,271,246
    - **Z-Boson Candidates (60-120 GeV range)**: 8,266,469
    - **Artifact**: `results/cms_z_peak_validation.png` (Z-Peak clearly visible at ~91 GeV).

## Phase 2: Entropic Scattering Test
- **Hypothesis**: Look for high-entropy recoil in $Z \to \mu\mu$ events.
- **Current Status**: **BLOCKED** on Data Content.
- **Finding**: The downloaded "Outreach Tool" dataset contains **only Muon branches**.
    - *Missing*: Jets, Tracks, Particle Flow Candidates.
    - *Impact*: We can see the Z boson, but we cannot see the "Recoil" system required to calculate the Entropic Discriminator ($D_E$).
- **Next Step**: Locate the full AOD (Analysis Object Data) or a NanoAOD that includes Jet/PF collections for this same run period.

## Actions Taken
1.  Fixed `fetch_cms_doublemuon.py` to handle large file processing via chunking (processed 60M events in <1 min).
2.  Updated `check_mirror_fermion_hypothesis.py` to act as a **Z-Peak Validator** in the absence of Jet data.
3.  Confirmed pipeline integrity.
