#!/usr/bin/env python
"""
positive_control_v2_prepare.py
==============================

Step 4 of the v2 Baldwin 2014 positive-control upgrade.

Prepare codeml run directories for:
  TAS1R1_pc_v2__apodiformes     - foreground = MRCA of (Apus, Calypte)  [Baldwin 2014 design]
  TAS1R1_pc_v2__mouse_control   - foreground = Mus_musculus tip         [negative control]

Uses the 9-species codon alignment (codon_aligned_v2.phy) and a fixed species
tree representing the accepted avian/mammal phylogeny (Prum et al. 2015 Nature,
Jarvis et al. 2014 Science). ML gene-tree topology is congruent with this
species tree (Apodiformes (Calypte,Apus) sister to Passeriformes (Serinus,
Taeniopygia)), but bootstrap on (Calypte,Apus) is 52% due to the truncated
Taeniopygia RefSeq. Using the fixed species tree is the standard practice for
branch-site tests (Yang 2007, Anisimova & Yang 2007).

For apodiformes test: label the INTERNAL branch leading to the (Apus,Calypte)
MRCA with "#1". This is the "ancestral Apodiformes branch" design of Baldwin
2014.

For mouse control: label the Mus_musculus tip with "#1".

Outputs under data/codeml_runs/TAS1R1_pc_v2__*/:
  alignment.phy
  tree_labelled.nwk
  null.ctl
  alt.ctl
"""
from __future__ import annotations
import shutil
import sys
from pathlib import Path

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
WORK = ROOT / "data" / "positive_control" / "work"
RUNS = ROOT / "data" / "codeml_runs"
SCRIPTS = ROOT / "scripts"

NULL_CTL = SCRIPTS / "00_codeml_model_a_null.ctl"
ALT_CTL = SCRIPTS / "00_codeml_model_a_alt.ctl"

ALN_PHY = WORK / "codon_aligned_v2.phy"

# Accepted species tree (Prum 2015 Nature + TimeTree):
#   Danio_rerio basal; Mammalia (Homo,(Mus,Rattus));
#   Aves = (Gallus, ((Apus,Calypte), (Serinus,Taeniopygia)))
# We provide two labelled versions.

# PAML branch-site Model A requires an UNROOTED tree. Use a trifurcation at
# the root (Danio as one subtree, Mammalia + Aves as the other two). PAML will
# otherwise print "This is a rooted tree. Please check!" and can silently drop
# foreground markers that sit on internal branches adjacent to a bifurcating
# root.
#
# Also IMPORTANT: the foreground marker must be attached directly (no space):
#   (Apus_apus,Calypte_anna)#1        <- correct
#   (Apus_apus,Calypte_anna) #1       <- parsed as 2 tokens, label lost

# Apodiformes-ancestral foreground: branch leading to the (Apus,Calypte) MRCA
SPECIES_TREE_APODIFORMES = (
    "(Danio_rerio,"
    "(Homo_sapiens,(Mus_musculus,Rattus_norvegicus)),"
    "(Gallus_gallus,"
    "((Apus_apus,Calypte_anna)#1,"
    "(Serinus_canaria,Taeniopygia_guttata))));"
)

# Mouse-tip negative control foreground
SPECIES_TREE_MOUSE = (
    "(Danio_rerio,"
    "(Homo_sapiens,(Mus_musculus#1,Rattus_norvegicus)),"
    "(Gallus_gallus,"
    "((Apus_apus,Calypte_anna),"
    "(Serinus_canaria,Taeniopygia_guttata))));"
)


def write_tree_with_header(path: Path, tree_str: str, n_tax: int = 9) -> None:
    """PAML prefers a ' n_tax 1\n' header line before the newick tree."""
    path.write_text(f" {n_tax} 1\n{tree_str}\n")


def make_run_dir(run_id: str, tree_str: str) -> Path:
    d = RUNS / run_id
    d.mkdir(parents=True, exist_ok=True)

    # alignment.phy
    shutil.copy(ALN_PHY, d / "alignment.phy")

    # tree_labelled.nwk (with PAML header line)
    write_tree_with_header(d / "tree_labelled.nwk", tree_str, n_tax=9)

    # ctl files
    for src, dst in [(NULL_CTL, "null.ctl"), (ALT_CTL, "alt.ctl")]:
        (d / dst).write_text(src.read_text())

    print(f"[prep] {run_id:40s} tree -> {d/'tree_labelled.nwk'}")
    print(f"        tree={tree_str}")
    return d


def main() -> int:
    assert ALN_PHY.exists(), f"Missing {ALN_PHY}"
    make_run_dir("TAS1R1_pc_v2__apodiformes", SPECIES_TREE_APODIFORMES)
    make_run_dir("TAS1R1_pc_v2__mouse_control", SPECIES_TREE_MOUSE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
