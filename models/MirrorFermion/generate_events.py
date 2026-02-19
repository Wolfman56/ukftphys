#!/usr/bin/env python3
"""
UKFT Mirror Fermion Event Generation Script
Run after: mg5_aMC> output MirrorLHC
"""

import os
import subprocess

def run_madgraph():
    mg5 = "mg5_aMC"  # or full path
    commands = """
    import model MirrorFermion_UFO
    generate p p > xm xm~ [QCD]
    add process p p > xm xm~ , xm > t h , xm~ > t~ h~
    add process p p > xm xm~ , xm > t z , xm~ > t~ z
    add process p p > xm xm~ , xm > b w+ , xm~ > b~ w-
    add process p p > xm xm~ , xm > xmInv , xm~ > xmInv
    output MirrorLHC
    launch MirrorLHC
    shower=Pythia8
    detector=Delphes
    analysis=madanalysis5
    done
    """
    with open("mg_commands.txt", "w") as f:
        f.write(commands)
    
    subprocess.run([mg5, "mg_commands.txt"])

if __name__ == "__main__":
    run_madgraph()
    print("✅ 10k Mirror Fermion events generated in MirrorLHC/")
    print("   Check: MirrorLHC/Events/run_01/unweighted_events.lhe")
    print("   Delphes ROOT: MirrorLHC/Events/run_01/tag_1_delphes_events.root")