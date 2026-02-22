# Mirror Fermion Validation: Tools

This directory contains the Python scripts used for fetching, inspecting, and analyzing high-energy physics data.

## 1. Data Loaders

### `fetch_cms_doublemuon.py`
**Purpose**: Downloads and processes the CMS "DoubleMuParked" dataset (Run 1, 2012).
*   **Source**: CERN Open Data Portal (via EOS public HTTP link).
*   **Function**:
    1.  Downloads the raw ROOT file (~2.1 GB) to `../data/cms_doublemuon_full.root`.
    2.  Reads the file in chunks (streaming) to avoid memory overflow.
    3.  Filters for events with $\ge 2$ muons.
    4.  Saves the result as a localized Parquet file: `../data/cms_doublemuon_muons.parquet`.
*   **Usage**:
    ```bash
    python research/mirror_fermion_validation/tools/fetch_cms_doublemuon.py
    ```

## 2. Analysis Tools

### `check_mirror_fermion_hypothesis.py`
**Purpose**: Reconstructs Z-boson candidates and generates validation plots.
*   **Input**: `../data/cms_doublemuon_muons.parquet`
*   **Function**:
    1.  Loads the filtered Parquet data.
    2.  Reconstructs the invariant mass of the leading dimuon pair ($Z \to \mu^+\mu^-$).
    3.  Filters for the Z-peak window (60-120 GeV).
    4.  Generates the validation plot: `../analysis/visuals/cms_z_peak_validation.png`.
*   **Usage**:
    ```bash
    python research/mirror_fermion_validation/tools/check_mirror_fermion_hypothesis.py
    ```

### `inspect_root.py`
**Purpose**: A utility script to inspect the internal structure (branches/trees) of a ROOT file.
*   **Usage**:
    ```bash
    python research/mirror_fermion_validation/tools/inspect_root.py
    ```

## Datasets of Interest

1.  **CMS Run 1 DoubleMuParked** (8 TeV) - *Currently Implemented*
    *   **Source**: [CERN Open Data Portal](http://opendata.cern.ch/record/6030).
    *   **Description**: High-fidelity muon triggers from 2012B/C data. We currently use the "Outreach" subset which contains muons but lacks jets.

2.  **CMS Run 2 DoubleMuon** (13 TeV) - *Future Target*
    *   **Source**: [CERN Open Data Portal](http://opendata.cern.ch/record/12300).
    *   **Status**: Requires XRootD or substantially larger storage for AOD access.
