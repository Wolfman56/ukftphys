#!/usr/bin/env python3
"""
Phase 36 — Full Paper Draft Generation
=======================================
Validates that the paper LaTeX source is consistent with all computed
numerical results from Phases 22–35, and provides a quick sanity-check
of every key number embedded in the manuscript.

Output: console report + figures/phase36_paper_numbers.txt
"""

import os
import re
import sys

PAPER_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../noosphere/apps/hep-explorer/paper/cms_anomalous_7muon.tex",
)
OUTDIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUTDIR, exist_ok=True)

# ─── Ground-truth numerical results (from Phases 22–35) ────────────────────
GROUND_TRUTH = {
    # Target event
    "m_A_GeV":              1.747,
    "m_B_GeV":              14.662,
    "m_7mu_GeV":            331.495,
    "mass_ratio":           8.392,
    "Q_net":                1,
    "Q_A":                  0,
    "n_muon":               7,
    "dphi_AB_deg":          166.9,
    "dphi_dense_rad":       0.067,
    "MET_over_HT":          0.488,
    "S3_bert":              0.786,     # BERT S3 score
    # Run2012B cut-flow
    "N_total_2012B":        26_084_708,
    "N_after_C0":           216_719,
    "N_after_C1":           124_181,
    "N_after_C1q":          6_672,
    "N_after_C2":           353,
    "N_after_C3":           263,
    "N_after_C4":           113,
    "N_after_C5":           8,          # background at ratio > 8.392
    "rejection_at_C5":      3_260_588,
    # Significance
    "N_bkg_extrapolated":   0.061,      # Method A
    "Z_local_sole_survivor":4.42,       # Method B
    "Z_global_sole_survivor":3.30,      # Method B LEE
    "Z_madgraph":           10.0,       # Method C lower bound
    "N_bkg_madgraph":       1.78e-15,   # Method C
    # Isolation (Phase 34)
    "pct_bkg_PF_valid":     0.0,        # 0/263 PF-valid at C3
    # Run2012C (Phase 32)
    "N_run2012c":           200_000,
    "N_sole_survivor":      1,
}

# ─── Check paper contains key numbers ──────────────────────────────────────
def load_paper(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def check_number(text, value, label, fmt=None):
    """Return True if value (as string) appears in text (handles LaTeX notation)."""
    if fmt:
        s = fmt.format(value)
    else:
        s = str(value)
    candidates = [
        s,
        s.replace(",", ""),           # strip comma thousands separator
        s.replace(",", r"\,"),        # LaTeX thin-space thousands separator
        s.replace("e-", r"\times10^{-").rstrip("0").rstrip(".") + "}",
        s.replace("e+", r"\times10^{").rstrip("0").rstrip(".") + "}",
    ]
    # For scientific notation like 1.78e-15 -> 1.78\times10^{-15}
    if "e" in s.lower():
        mantissa, exp = s.lower().split("e")
        exp_int = int(exp)
        candidates.append(f"{mantissa}\\times10^{{{exp_int}}}")
        candidates.append(f"{mantissa}\\times10^{{-{abs(exp_int)}}}" if exp_int < 0 else f"{mantissa}\\times10^{{{exp_int}}}")
    # For large numbers like 3260588 -> 3.26 \times 10^6
    if isinstance(value, int) and value > 1_000_000:
        sci = f"{value:.2e}"
        m, e = sci.split("e+")
        candidates.append(f"{m} \\times 10^{int(e)}")
        candidates.append(f"{m}\\times10^{int(e)}")
    # For numbers with LaTeX thin space (200\,000)
    s_thin = s.replace(",", r"\,")
    candidates.append(s_thin)
    found = any(c in text for c in candidates)
    return found, s

def run_checks(paper_text):
    checks = [
        (1.747,         "m_A",          "{:.3f}"),
        (14.662,        "m_B",          "{:.3f}"),
        (331.495,       "m_7mu",        "{:.3f}"),
        (8.392,         "mass_ratio",   "{:.3f}"),
        (166.9,         "dphi_deg",     "{:.1f}"),
        (0.067,         "dphi_dense",   "{:.3f}"),
        (26_084_708,    "N_2012B",      "{:,}"),
        (263,           "N_C3",         "{}"),
        (113,           "N_C4",         "{}"),
        (8,             "N_C5",         "{}"),
        (3_260_588,     "rejection",    "{:,}"),
        (4.42,          "Z_local",      "{:.2f}"),
        (3.30,          "Z_global",     "{:.2f}"),
        (1.78e-15,      "N_bkg_theory", "{:.2e}"),
        (200_000,       "N_run2012c",   "{:,}"),
        (0.061,         "N_bkg_A",      "{:.3f}"),
    ]

    results = []
    all_pass = True
    for val, label, fmt in checks:
        found, s = check_number(paper_text, val, label, fmt)
        status = "PASS" if found else "FAIL"
        if not found:
            all_pass = False
        results.append((status, label, s))
    return results, all_pass

def print_table(results):
    print(f"\n{'='*55}")
    print(f"  Phase 36 — Paper Number Consistency Check")
    print(f"{'='*55}")
    print(f"  {'Status':<6}  {'Quantity':<22}  {'Value'}")
    print(f"  {'-'*6}  {'-'*22}  {'-'*20}")
    for status, label, val in results:
        marker = "✓" if status == "PASS" else "✗"
        print(f"  {marker} {status:<5}  {label:<22}  {val}")
    print(f"{'='*55}")

def main():
    abs_path = os.path.abspath(PAPER_PATH)
    if not os.path.exists(abs_path):
        print(f"ERROR: paper not found at {abs_path}")
        sys.exit(1)

    paper_text = load_paper(abs_path)
    results, all_pass = run_checks(paper_text)
    print_table(results)

    # Summary
    n_pass = sum(1 for r in results if r[0] == "PASS")
    n_fail = sum(1 for r in results if r[0] == "FAIL")
    print(f"\n  Passed: {n_pass}/{len(results)}  |  Failed: {n_fail}")

    # Paper statistics
    n_lines = paper_text.count("\n")
    n_words = len(paper_text.split())
    n_sections = paper_text.count(r"\section{") + paper_text.count(r"\subsection{")
    print(f"\n  Paper stats:")
    print(f"    Lines:    {n_lines}")
    print(f"    Words:    {n_words}")
    print(f"    Sections: {n_sections}")
    print(f"    File:     {abs_path}")

    # Save report
    out_path = os.path.join(OUTDIR, "phase36_paper_numbers.txt")
    with open(out_path, "w") as f:
        f.write("Phase 36 — Paper Consistency Report\n")
        f.write("=" * 55 + "\n")
        for status, label, val in results:
            f.write(f"[{status}]  {label:<22}  {val}\n")
        f.write(f"\nPassed: {n_pass}/{len(results)}\n")
        f.write(f"Lines: {n_lines}  Words: {n_words}\n")
    print(f"\n  Report saved to: {out_path}")

    if all_pass:
        print("\n  ✓ All key numbers present in paper. Draft consistent.\n")
    else:
        print("\n  ✗ Some numbers missing — review FAIL items above.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
