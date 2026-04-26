#!/usr/bin/env python
"""
positive_control_v3_prepare.py
==============================

Prepare codeml run dirs on the v3 alignment (8 taxa; Taeniopygia dropped).

Run dirs:
  TAS1R1_pc_v3__apodiformes_mrca   - fg = internal branch to (Apus,Calypte) MRCA
  TAS1R1_pc_v3__apodiformes_clade  - fg = whole Apodiformes clade (Baldwin-style)
  TAS1R1_pc_v3__mouse_control      - fg = Mus_musculus tip (negative control)

Species tree (Prum 2015 Nature + Jarvis 2014 Science):
  Danio basal; Mammalia (Homo,(Mus,Rattus));
  Aves = (Gallus, ((Apus,Calypte), Serinus))
Unrooted trifurcation at Danio + mammals + aves subtrees.
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
ALN_PHY = WORK / "codon_aligned_v3.phy"

# Apodiformes ancestral branch = internal branch leading to (Apus,Calypte) MRCA
TREE_MRCA = (
    "(Danio_rerio,"
    "(Homo_sapiens,(Mus_musculus,Rattus_norvegicus)),"
    "(Gallus_gallus,"
    "((Apus_apus,Calypte_anna)#1,"
    "Serinus_canaria)));"
)

# Whole Apodiformes clade (MRCA + both tips) — closer to Baldwin 2014's design
TREE_CLADE = (
    "(Danio_rerio,"
    "(Homo_sapiens,(Mus_musculus,Rattus_norvegicus)),"
    "(Gallus_gallus,"
    "((Apus_apus#1,Calypte_anna#1)#1,"
    "Serinus_canaria)));"
)

# Mouse-tip negative control
TREE_MOUSE = (
    "(Danio_rerio,"
    "(Homo_sapiens,(Mus_musculus#1,Rattus_norvegicus)),"
    "(Gallus_gallus,"
    "((Apus_apus,Calypte_anna),"
    "Serinus_canaria)));"
)


def write_tree(path: Path, tree_str: str, n_tax: int = 8) -> None:
    path.write_text(f" {n_tax} 1\n{tree_str}\n")


def make_run_dir(run_id: str, tree_str: str) -> Path:
    d = RUNS / run_id
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(ALN_PHY, d / "alignment.phy")
    write_tree(d / "tree_labelled.nwk", tree_str, n_tax=8)
    for src, dst in [(NULL_CTL, "null.ctl"), (ALT_CTL, "alt.ctl")]:
        (d / dst).write_text(src.read_text())
    print(f"[prep] {run_id:40s} -> {d}")
    print(f"        tree={tree_str}")
    return d


def main() -> int:
    make_run_dir("TAS1R1_pc_v3__apodiformes_mrca", TREE_MRCA)
    make_run_dir("TAS1R1_pc_v3__apodiformes_clade", TREE_CLADE)
    make_run_dir("TAS1R1_pc_v3__mouse_control", TREE_MOUSE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
