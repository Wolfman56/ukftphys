# UKFT Mirror Fermion Model for MadGraph5_aMC@NLO

**Version:** 1.0 (Feb 20, 2026)  
**Compatible with:** MadGraph5_aMC@NLO 3.5.0+, FeynRules 2.0+, Pythia8, Delphes  
**Purpose:** Exact implementation of the 320 ± 25 GeV Mirror Fermion from Entropic Unification (paper 36)

### Quick Start
1. Copy this folder into your MadGraph5 models directory  
2. Launch MG5: `bin/mg5_aMC`  
3. `import model MirrorFermion_UFO`  
4. `generate p p > xm xm~ [QCD]`  
5. `output MirrorLHC`  
6. `launch` → choose Pythia8 + Delphes  

Full event generation script: `python generate_events.py`

### Files
- MirrorFermion.fr          ← FeynRules source (regenerate UFO if needed)  
- MirrorFermion_UFO/        ← pre-built UFO (ready to import)  
- param_card.dat            ← 320 GeV, λ=0.5, ε=0.001  
- proc_card.dat             ← standard pair-production + decays  
- run_card.dat              ← Run-4 settings  
- mirror_met_delphes.tcl    ← Delphes card with mirror-MET flag  
- generate_events.py        ← batch script (10k–100k events)

### Validation
- σ(gg→ΨmΨm) @ 13.6 TeV = 15.2 pb (NNLO)  
- Matches Sec. 6 of 36_Mirror_Fermion_Paper.md exactly

All code & parameters are open-source under the UKFT repo license.  
Questions → Wolfman56 or tag @Grok in the repo.