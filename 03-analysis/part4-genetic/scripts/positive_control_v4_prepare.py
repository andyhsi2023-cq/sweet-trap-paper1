#!/usr/bin/env python
"""
positive_control_v4_prepare.py
==============================

Prepare codeml run dirs for v4 (15-taxon Baldwin-scale test).

Tree topology from tree_v4.treefile (ML on 15-taxon protein alignment):
  Danio_rerio outgroup
  Mammals (Homo, (Mus, Rattus))
  Aves = (Gallus, (((9 hummingbirds), Apus), Serinus))

For codeml we need:
  - unrooted tree (trifurcation at Danio / Mammals / Aves)
  - no branch lengths (PAML uses them only as starting values with fix_blength=1)
  - foreground branch marked with #1

Run dirs prepared:
  TAS1R1_pc_v4__apodiformes_mrca   - fg = internal branch to Apodiformes MRCA
                                     (the (hummingbirds, Apus) crown)
  TAS1R1_pc_v4__hummingbird_mrca   - fg = internal branch to crown hummingbird MRCA
                                     (Baldwin 2014's second main test)
  TAS1R1_pc_v4__apodiformes_clade  - fg = whole Apodiformes subtree (every branch
                                     inside, including Apus tip and all hummingbird
                                     internal + tip branches)
  TAS1R1_pc_v4__hummingbirds_clade - fg = every branch in the crown hummingbird
                                     subtree (Baldwin-style extended)
  TAS1R1_pc_v4__mouse_control      - fg = Mus_musculus tip (negative control)
"""
from __future__ import annotations
import re
import shutil
import sys
from pathlib import Path

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
WORK = ROOT / "data" / "positive_control" / "work"
RUNS = ROOT / "data" / "codeml_runs"
SCRIPTS = ROOT / "scripts"

NULL_CTL = SCRIPTS / "00_codeml_model_a_null.ctl"
ALT_CTL = SCRIPTS / "00_codeml_model_a_alt.ctl"
ALN_PHY = WORK / "codon_aligned_v4.phy"


# Base topology (unrooted, no branch lengths, no labels).
# Hummingbird ladder reflects ML order from tree_v4. What really matters for
# branch-site tests is the foreground branch position; internal hummingbird
# structure only affects nuisance-parameter estimates.
HB_CLADE = (
    "(((((((("
    "Calypte_anna,Amazilia_tzacatl),"
    "Patagona_gigas),"
    "Lophornis_magnificus),"
    "Heliangelus_exortis),"
    "Haplophaedia_aureliae),"
    "Heliothryx_barroti),"
    "Ramphodon_naevius),"
    "Florisuga_fusca)"
)

APOD_CLADE = f"({HB_CLADE},Apus_apus)"
AVES_CLADE = f"(Gallus_gallus,({APOD_CLADE},Serinus_canaria))"
MAMMALS    = "(Homo_sapiens,(Mus_musculus,Rattus_norvegicus))"

BASE_TREE = f"(Danio_rerio,{MAMMALS},{AVES_CLADE});"


def label_branch(tree: str, clade_str: str, tip_name: str | None = None,
                 tip_label: str | None = None, clade_label: str = "#1") -> str:
    """Return a copy of `tree` with one labelling applied.

    If `clade_str` is given, we append `clade_label` immediately after the
    CLOSING paren that matches the opening paren at the start of `clade_str`
    inside `tree`. Matching is done by substring location (there is only one
    instance of each full clade string in our curated trees).
    """
    # Find the position of the clade in the tree
    idx = tree.find(clade_str)
    if idx < 0:
        raise ValueError(f"clade not found in tree: {clade_str[:40]}... tree={tree[:80]}")
    # clade_str starts with '(' so the matching ')' is at idx + len(clade_str) - 1
    end = idx + len(clade_str)  # position right after closing ')'
    labelled = tree[:end] + clade_label + tree[end:]
    return labelled


def label_tip_marker(tree: str, tip_name: str, marker: str = "#1") -> str:
    """Append marker to a specific tip name. Regex-safe replace."""
    # Only replace one instance, require whole-word match
    pattern = re.compile(rf"\b{re.escape(tip_name)}\b")
    count = len(pattern.findall(tree))
    if count == 0:
        raise ValueError(f"tip {tip_name} not in tree")
    if count > 1:
        raise ValueError(f"tip {tip_name} appears {count} times")
    return pattern.sub(f"{tip_name}{marker}", tree, count=1)


def label_all_tips_in_clade(tree: str, clade: str, tips: list[str]) -> str:
    """Label the clade's internal MRCA branch + all its tips with #1.

    We apply the clade-label first, then each tip-label.
    """
    t = label_branch(tree, clade, clade_label="#1")
    # Re-find the clade after the label edit — the clade substring includes no
    # tip labels, so it still appears. Actually we just continue from t.
    for tip in tips:
        t = label_tip_marker(t, tip)
    return t


HB_TIPS = [
    "Calypte_anna", "Amazilia_tzacatl", "Patagona_gigas", "Lophornis_magnificus",
    "Heliangelus_exortis", "Haplophaedia_aureliae", "Heliothryx_barroti",
    "Ramphodon_naevius", "Florisuga_fusca",
]
APOD_TIPS = HB_TIPS + ["Apus_apus"]


def write_tree(path: Path, tree_str: str, n_tax: int = 16) -> None:
    path.write_text(f" {n_tax} 1\n{tree_str}\n")


def make_run_dir(run_id: str, tree_str: str) -> Path:
    d = RUNS / run_id
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(ALN_PHY, d / "alignment.phy")
    write_tree(d / "tree_labelled.nwk", tree_str, n_tax=16)
    for src, dst in [(NULL_CTL, "null.ctl"), (ALT_CTL, "alt.ctl")]:
        (d / dst).write_text(src.read_text())
    print(f"[prep] {run_id:45s}")
    print(f"        tree={tree_str}")
    return d


def main() -> int:
    assert ALN_PHY.exists(), ALN_PHY

    # 1. Apodiformes MRCA only (single internal branch foreground)
    t1 = label_branch(BASE_TREE, APOD_CLADE, clade_label="#1")
    make_run_dir("TAS1R1_pc_v4__apodiformes_mrca", t1)

    # 2. Crown hummingbird MRCA only
    t2 = label_branch(BASE_TREE, HB_CLADE, clade_label="#1")
    make_run_dir("TAS1R1_pc_v4__hummingbird_mrca", t2)

    # 3. Entire Apodiformes subtree: MRCA branch + hummingbird MRCA branch +
    #    all Apodiformes tips (Apus + all 9 hummingbirds). All get the same #1
    #    marker so PAML treats them as a single foreground class.
    #    Order: outer APOD_CLADE first (unique substring), then inner HB_CLADE.
    t3 = label_branch(BASE_TREE, APOD_CLADE, clade_label="#1")  # Apodiformes MRCA
    t3 = label_branch(t3, HB_CLADE, clade_label="#1")           # hummingbird MRCA (still substring)
    for tip in APOD_TIPS:
        t3 = label_tip_marker(t3, tip)
    make_run_dir("TAS1R1_pc_v4__apodiformes_clade", t3)

    # 4. Crown hummingbird subtree (MRCA + all hummingbird tips; Apus NOT foreground)
    t4 = label_branch(BASE_TREE, HB_CLADE, clade_label="#1")
    for tip in HB_TIPS:
        t4 = label_tip_marker(t4, tip)
    make_run_dir("TAS1R1_pc_v4__hummingbirds_clade", t4)

    # 5. Mouse negative control
    t5 = label_tip_marker(BASE_TREE, "Mus_musculus")
    make_run_dir("TAS1R1_pc_v4__mouse_control", t5)

    return 0


if __name__ == "__main__":
    sys.exit(main())
