#!/usr/bin/env python3
"""
20_render_placement_tree.py
===========================

Render the 51-taxon cnidarian placement tree as a PDF for SI.
Taxa are colored by functional class:

  - DRD (reference): black, bold (both vertebrate DRD1/DRD2 and arthropod
    DopR1/DopR2 and mollusc Dop)
  - HTR: blue
  - ADRB / ADRA: green
  - OA (Dmel Oct-b2R): orange
  - HRH1 (root outgroup): gray
  - Cnidarian candidates: red, bold italic

Uses Bio.Phylo (matplotlib backend).
"""
from pathlib import Path
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from Bio import Phylo

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
IN_TREE  = ROOT / "outputs" / "orthofinder_dop" / "tree_cnidarian_placement" / "cnidarian_placement.contree"
OUT_PDF  = ROOT / "outputs" / "orthofinder_dop" / "tree_cnidarian_placement" / "cnidarian_placement.pdf"
OUT_PNG  = ROOT / "outputs" / "orthofinder_dop" / "tree_cnidarian_placement" / "cnidarian_placement.png"


def simplify(name: str) -> str:
    m = re.match(r"^(DRD[12])\|([^|]+)\|", name)
    if m:
        return f"{m.group(1)} {m.group(2)}"
    m = re.match(r"^(DopR[12])\|([^|]+)\|", name)
    if m:
        return f"{m.group(1)} {m.group(2)}"
    m = re.match(r"^DopR_(\d)\|([^|]+)\|", name)
    if m:
        return f"molluscan Dop{m.group(1)} {m.group(2)}"
    m = re.match(r"^HUMAN_(\w+)", name)
    if m:
        return f"human {m.group(1)}"
    m = re.match(r"^DMEL_(\w+)", name)
    if m:
        return f"Dmel {m.group(1)}"
    m = re.match(r"^(Hvul|Nvec|Adig)_(XP_\S+)", name)
    if m:
        sp_pretty = {"Hvul": "Hydra", "Nvec": "Nematostella", "Adig": "Acropora"}[m.group(1)]
        return f"{sp_pretty} {m.group(2).split('.')[0]} (CAND)"
    return name[:25]


def color_for(name: str) -> str:
    if re.match(r"^(DRD[12])\|", name): return "#1a1a1a"          # black
    if re.match(r"^DopR[12]\|", name): return "#1a1a1a"            # black
    if re.match(r"^DopR_\d\|", name): return "#1a1a1a"             # black
    if name.startswith("HUMAN_HTR"): return "#1F77B4"               # blue
    if name.startswith("HUMAN_ADRB"): return "#2CA02C"              # green
    if name.startswith("HUMAN_ADRA"): return "#2CA02C"              # green
    if name.startswith("DMEL_OCTB"): return "#FF7F0E"               # orange
    if name.startswith("HUMAN_HRH"): return "#7F7F7F"               # gray
    if re.match(r"^(Hvul|Nvec|Adig)_", name): return "#D62728"      # red
    return "#000000"


def main():
    tree = Phylo.read(str(IN_TREE), "newick")
    # root on HRH1
    for clade in tree.get_terminals():
        if clade.name and clade.name.startswith("HUMAN_HRH1"):
            tree.root_with_outgroup({"name": clade.name})
            break

    # assign color per terminal
    for term in tree.get_terminals():
        term.color = color_for(term.name or "")

    # Rename terminals to simplified labels (for display)
    for term in tree.get_terminals():
        term.name = simplify(term.name or "")

    fig, ax = plt.subplots(figsize=(10, 14))
    Phylo.draw(tree, axes=ax, do_show=False,
               label_func=lambda c: c.name if c.is_terminal() else (c.confidence or ""),
               branch_labels=lambda c: None)
    ax.set_title("Cnidarian placement tree: DRD candidates vs. amine receptor references\n"
                 "(ML, LG+G4, UFBoot B=1000, rooted on human HRH1)", fontsize=9)
    plt.tight_layout()
    plt.savefig(OUT_PDF, dpi=300, bbox_inches="tight")
    plt.savefig(OUT_PNG, dpi=200, bbox_inches="tight")
    print(f"[plot] -> {OUT_PDF}")
    print(f"[plot] -> {OUT_PNG}")


if __name__ == "__main__":
    main()
