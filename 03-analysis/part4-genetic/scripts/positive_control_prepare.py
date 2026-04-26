#!/usr/bin/env python
"""
positive_control_prepare.py
===========================

Prepare codeml run directories for the two positive-control / negative-control
tests (Baldwin 2014 Baldwin-style TAS1R1 hummingbird vs. mouse).

Run dirs created:
  data/codeml_runs/TAS1R1_pc__hummingbird/
  data/codeml_runs/TAS1R1_pc__mouse_control/

Each contains:
  - alignment.phy
  - tree_labelled.nwk   (foreground tip tagged "#1")
  - null.ctl
  - alt.ctl
"""
from __future__ import annotations
import shutil
import sys
from pathlib import Path
from ete3 import Tree

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
WORK = ROOT / "data" / "positive_control" / "work"
RUNS = ROOT / "data" / "codeml_runs"
SCRIPTS = ROOT / "scripts"

NULL_CTL = SCRIPTS / "00_codeml_model_a_null.ctl"
ALT_CTL = SCRIPTS / "00_codeml_model_a_alt.ctl"

ALN_PHY = WORK / "codon_aligned.phy"
TREE_NWK = WORK / "species_tree.nwk"


def label_tip(tree_text: str, fg_tip: str) -> str:
    t = Tree(tree_text, format=0)
    hits = [leaf for leaf in t.get_leaves() if leaf.name == fg_tip]
    if not hits:
        raise ValueError(f"tip {fg_tip} not found; have {[l.name for l in t.get_leaves()]}")
    # Append PAML foreground marker
    hits[0].name = hits[0].name + " #1"
    return t.write(format=0)


def make_run_dir(run_id: str, fg_tip: str) -> Path:
    d = RUNS / run_id
    d.mkdir(parents=True, exist_ok=True)

    # alignment.phy
    shutil.copy(ALN_PHY, d / "alignment.phy")

    # tree_labelled.nwk
    tt = TREE_NWK.read_text().strip()
    labelled = label_tip(tt, fg_tip)
    (d / "tree_labelled.nwk").write_text(labelled + "\n")

    # ctl files
    for src, dst in [(NULL_CTL, "null.ctl"), (ALT_CTL, "alt.ctl")]:
        text = src.read_text()
        (d / dst).write_text(text)

    print(f"[prep] {run_id:40s} fg={fg_tip}  -> {d}")
    return d


def main() -> int:
    assert ALN_PHY.exists(), ALN_PHY
    assert TREE_NWK.exists(), TREE_NWK

    make_run_dir("TAS1R1_pc__hummingbird", "Calypte_anna")
    make_run_dir("TAS1R1_pc__mouse_control", "Mus_musculus")
    return 0


if __name__ == "__main__":
    sys.exit(main())
