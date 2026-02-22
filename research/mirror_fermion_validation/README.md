# Fermi Mirror Validation

**Objective**: Validate the UKFT Mirror Fermion hypothesis using public High Energy Physics data.

This folder contains scripts and analysis tools to compare the theoretical predictions of the **Mirror Fermion ($F_M \sim 320 \text{ GeV}$)** against real-world collider data from CERN (LHC) and potentially legacy Tevatron results.

## Roadmap

1.  **Data Ingestion**: Establish pipelines to fetch relevant open datasets (e.g., CMS Open Data, HEPData).
2.  **Event Selection**: Filter for high-$p_T$ jets and missing energy signatures consistent with $F_M \to qqq$ decays.
3.  **Discriminator Validation**: Apply the **Entropic Discriminator ($D_E$)** from Experiment 53 to real QCD jets to confirm the background baseline.
4.  **Signal Search**: Look for deviations in the $D_E$ distribution or invariant mass spectra that could hint at Mirror Fermion presence.

## Validation Results

*   **Phase 1** (Feb 2026): Confirmed Standard Model Z-Boson Reconstruction. See [Phase 1 Report](REPORT_PHASE_1.md).

## Data Sources

We are using **CERN Open Data** for validation.

### Currently Used Dataset (Phase 1)
*   **Name**: CMS Run 2012B/C DoubleMuParked (Outreach Format)
*   **Source URL**: [Direct Link](https://eospublic.cern.ch//eos/opendata/cms/derived-data/AOD2NanoAODOutreachTool/Run2012BC_DoubleMuParked_Muons.root)
*   **Description**: A simplified ROOT file derived from the full "DoubleMuParked" 2012 dataset.
*   **Content**: Contains roughly 60 Million events with high-fidelity Muon candidates (ideal for Z-peak validation) but lacks Jets/Tracks (preventing Entropic Recoil analysis this round).
*   **Size**: ~2.1 GB.
*   **Loader**: `tools/fetch_cms_doublemuon.py` (downloads and converts to local Parquet).

### Target Dataset (Phase 2)
To perform the full **Entropic Scattering Test**, we need the full **AOD (Analysis Object Data)** version which includes:
*   **PF Jets** (Particle Flow)
*   **Tracks** (General Tracks collection)
*   **Missing Transverse Energy (MET)**

Potential Candidate: [CMS 2012 DoubleMuParked AOD](http://opendata.cern.ch/record/6021) (~1 TB total, will require significant filtering).

## Usage

### 1. Download & Process Data
Run the fetch tool to download the 2GB dataset and filter for dimuon events:
```bash
python research/mirror_fermion_validation/tools/fetch_cms_doublemuon.py
```
This generates `research/mirror_fermion_validation/data/cms_doublemuon_muons.parquet`.

### 2. Run Validation Analysis
Run the analyzer to reconstruct the Z-peak:
```bash
python research/mirror_fermion_validation/tools/check_mirror_fermion_hypothesis.py
```
This generates the plot in `analysis/visuals/cms_z_peak_validation.png`.

## Structure

*   `tools/`: Python scripts for data fetching and analysis.
*   `data/`: Local storage for downloaded ROOT files and processed Parquet data (git-ignored).
*   `analysis/visuals/`: Generated plots and results.
*   `REPORT_PHASE_1.md`: Detailed report of the first validation run.

*   `loaders/`: Scripts to fetch and convert data.
*   `analysis/`: Jupyter notebooks and Python scripts for physics analysis.
*   `results/`: Plots and statistical summaries.

## Getting Started

1.  **Download the Data** (~2GB):
    ```bash
    python research/mirror_fermion_validation/loaders/fetch_cms_doublemuon.py
    ```

2.  **Run the Validation**:
    ```bash
    python research/mirror_fermion_validation/analysis/check_mirror_fermion_hypothesis.py
    ```
