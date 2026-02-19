# Delphes card for Mirror Fermion analysis
# Extra handling for mirror-boundary MET (xmInv)

set Delphes $::env(DELPHES_PATH)

module track MET {
  add EnergyFraction 0.001   # invisible scalar treated as MET
  set Label "xmInv"
}

# Standard ATLAS/CMS-like card with MET > 200 GeV cut for mirror signature
include "cards/delphes_card_ATLAS.tcl"

# Custom filter for mirror MET
set Filter MET {
  set PtMin 200.
  set EtaMax 5.0
}