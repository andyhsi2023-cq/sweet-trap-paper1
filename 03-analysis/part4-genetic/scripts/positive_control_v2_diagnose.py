#!/usr/bin/env python
"""
positive_control_v2_diagnose.py
===============================

Diagnostic re-run: test 3 alternative foreground specifications on the 9-taxon
v2 alignment, to localize why the Apodiformes-MRCA test returned LRT=0.

Setups:
  A. TAS1R1_pc_v2__calypte_only    - fg = Calypte_anna tip (same as v1 setup)
  B. TAS1R1_pc_v2__apus_only       - fg = Apus_apus tip
  C. TAS1R1_pc_v2__apodiformes_clade - fg = {(Apus,Calypte) MRCA, Apus tip, Calypte tip}
                                     i.e. the entire Apodiformes subtree

Setup C is actually closer to Baldwin 2014: they labelled the Apodiformes
ancestral branch AND the crown hummingbird branches (since they had 3 humming-
birds + 2 swifts, the entire Apodiformes clade was foreground). With only 1 of
each extant species, the equivalent is: MRCA-branch + both tip branches = whole
Apodiformes subtree.
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

# A. Calypte tip only
TREE_A = (
    "(Danio_rerio,"
    "(Homo_sapiens,(Mus_musculus,Rattus_norvegicus)),"
    "(Gallus_gallus,"
    "((Apus_apus,Calypte_anna#1),"
    "(Serinus_canaria,Taeniopygia_guttata))));"
)

# B. Apus tip only
TREE_B = (
    "(Danio_rerio,"
    "(Homo_sapiens,(Mus_musculus,Rattus_norvegicus)),"
    "(Gallus_gallus,"
    "((Apus_apus#1,Calypte_anna),"
    "(Serinus_canaria,Taeniopygia_guttata))));"
)

# C. Apodiformes MRCA + both tips (whole Apodiformes clade as foreground)
#    All 3 marked with #1 -> PAML treats them as one foreground class
TREE_C = (
    "(Danio_rerio,"
    "(Homo_sapiens,(Mus_musculus,Rattus_norvegicus)),"
    "(Gallus_gallus,"
    "((Apus_apus#1,Calypte_anna#1)#1,"
    "(Serinus_canaria,Taeniopygia_guttata))));"
)


def write_tree(path: Path, tree_str: str) -> None:
    path.write_text(f" 9 1\n{tree_str}\n")


def make_run_dir(run_id: str, tree_str: str) -> Path:
    d = RUNS / run_id
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(ALN_PHY, d / "alignment.phy")
    write_tree(d / "tree_labelled.nwk", tree_str)
    for src, dst in [(NULL_CTL, "null.ctl"), (ALT_CTL, "alt.ctl")]:
        (d / dst).write_text(src.read_text())
    print(f"[prep] {run_id:40s} -> {d}")
    print(f"        tree={tree_str}")
    return d


def main() -> int:
    make_run_dir("TAS1R1_pc_v2__calypte_only", TREE_A)
    make_run_dir("TAS1R1_pc_v2__apus_only", TREE_B)
    make_run_dir("TAS1R1_pc_v2__apodiformes_clade", TREE_C)
    return 0


if __name__ == "__main__":
    sys.exit(main())
