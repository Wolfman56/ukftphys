import uproot

FILE = "research/mirror_fermion_validation/loaders/data/cms_doublemuon_full.root"

try:
    with uproot.open(FILE) as file:
        print("Keys in file:", file.keys())
        if "Events" in file:
            tree = file["Events"]
            print("Number of entries:", tree.num_entries)
            print("First 50 branches:", tree.keys()[:50])
            # Check for anything looking like "Jet" or "Muon"
            print("\nMatching 'Jet' branches:")
            print([k for k in tree.keys() if "Jet" in k])
            print("\nMatching 'Muon' branches:")
            print([k for k in tree.keys() if "Muon" in k])
        else:
            print("'Events' tree not found.")
except Exception as e:
    print(f"Error: {e}")
