#!/usr/bin/env python3
"""
10_tree_classify.py
===================

Reads the global ML tree of 62 biogenic-amine receptors and classifies
each mollusc/cnidarian MollCnid_DopR_* candidate according to whether
it branches within the DRD clade (sister to or nested within vertebrate
DRD1/DRD2/DRD3/DRD4/DRD5), or within a non-dopamine clade (HTR, ADR,
OA, TAR, CHRM, HRH).

Classification rule
-------------------
Let D = set of terminal taxa labeled DRD1/DRD2/DRD3/DRD4/DRD5 anchors.
For each candidate c:
  1. Find the smallest monophyletic subtree containing c and any anchor.
  2. Let A = anchors in that subtree; N = other (non-DRD) anchors in that subtree.
  3. If A is wholly within D (i.e., only DRD anchors present, no HTR/ADR/etc.)
     and the smallest clade containing c and ≥1 DRD anchor is NOT nested
     within a larger clade dominated by non-DRD anchors -> TRUE_DRD.
  4. Else assign the dominant neighbor-anchor family in c's immediate
     sister subtree (HTR / OA / TAR / ADR / CHRM / HRH / mixed).

We also report per-candidate:
  - nearest_anchor_label
  - nearest_anchor_distance (branch-sum)
  - sister_family_majority

Uses ete3 (already in the env).
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from ete3 import Tree

PROJECT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
OFDIR = PROJECT / "outputs" / "orthofinder_dop"
TREEFILE = OFDIR / "global_tree_v2" / "global_amine_tree_v2.treefile"
OUT_CSV = OFDIR / "tree_classification.csv"
OUT_MD = OFDIR / "tree_classification_summary.md"

DRD_RE = re.compile(r"(?:__|\|)(DRD1|DRD2|DRD3|DRD4|DRD5|DRD2A|DRD1_candidate|DRD2_candidate|DopR1_invert_anchor|DopR2_invert_anchor)(?:__|$)")
HTR_RE = re.compile(r"(?:__|\|)(HTR1A|HTR2A|HTR1B|5HT1A_Dmel|5HT2A_Dmel|5HT7_Dmel|5HT1Ap_Acal|5HT2_Acal)(?:__|$)")
ADR_RE = re.compile(r"(?:__|\|)(ADRA1A|ADRB1)(?:__|$)")
OA_RE = re.compile(r"(?:__|\|)(OctR_Oamb_Dmel|OctB2R_Dmel)(?:__|$)")
TAR_RE = re.compile(r"(?:__|\|)(TyrR_Dmel)(?:__|$)")
CHRM_RE = re.compile(r"(?:__|\|)(CHRM1)(?:__|$)")
HRH_RE = re.compile(r"(?:__|\|)(HRH1)(?:__|$)")
CAND_RE = re.compile(r"__MollCnid_DopR_\d_candidate__")
INVERT_DOPR_RE = re.compile(r"__DopR[12]?_candidate__")  # not in this tree; placeholder
VERT_DRD_RE = re.compile(r"__DRD[12]_candidate__")
# invert Dop1R/Dop2R candidates (confirmed dopamine receptors, used as DRD anchors)
INVERT_DRD_ANCHOR_RE = re.compile(r"__DopR[12]_invert_anchor__")


def family_of(name: str) -> str:
    """Assign one of TRUE_DRD / HTR / ADR / OA / TAR / CHRM / HRH /
    candidate / unknown to a leaf label."""
    if VERT_DRD_RE.search(name) or DRD_RE.search(name):
        return "TRUE_DRD"
    if HTR_RE.search(name):
        return "HTR"
    if ADR_RE.search(name):
        return "ADR"
    if OA_RE.search(name):
        return "OA"
    if TAR_RE.search(name):
        return "TAR"
    if CHRM_RE.search(name):
        return "CHRM"
    if HRH_RE.search(name):
        return "HRH"
    if CAND_RE.search(name):
        return "candidate"
    return "unknown"


def load_tree(path: Path) -> Tree:
    # iqtree treefile format is newick with support values
    return Tree(str(path), format=0)


def root_outgroup(tree: Tree) -> Tree:
    """Root the tree on HRH1 (histamine H1) — the most divergent
    monoamine receptor in our panel; commonly used as class-A
    aminergic-GPCR outgroup."""
    outgroup = [l for l in tree.get_leaves() if l.name.startswith("NP_000912.1")]
    if not outgroup:
        return tree
    tree.set_outgroup(outgroup[0])
    return tree


def find_drd_clade_mrca(tree: Tree) -> "Tree":
    """Find the MRCA of all vertebrate DRD anchors (NP_* DRD1-5). This
    defines the 'true DRD clade'."""
    drd_anchors = [l for l in tree.get_leaves()
                   if DRD_RE.search(l.name) and not CAND_RE.search(l.name)
                   and not l.name.endswith("_candidate__" + l.name.rsplit("__", 1)[-1])]
    # simpler: vertebrate DRD anchor leaves are those where the family
    # detector returns TRUE_DRD and the name is not a candidate.
    drd_anchors = [l for l in tree.get_leaves()
                   if family_of(l.name) == "TRUE_DRD" and not CAND_RE.search(l.name)
                   and "_candidate" not in l.name]
    if len(drd_anchors) < 2:
        raise RuntimeError(f"too few DRD anchors to define MRCA: {len(drd_anchors)}")
    mrca = tree.get_common_ancestor(drd_anchors)
    return mrca, drd_anchors


def is_within(node: "Tree", ancestor: "Tree") -> bool:
    """True if `node` is inside the subtree rooted at `ancestor`."""
    cur = node
    while cur is not None:
        if cur is ancestor:
            return True
        cur = cur.up
    return False


def nearest_anchor(leaf, all_anchors):
    # compute distances to every anchor
    best = None; best_d = float("inf")
    for a in all_anchors:
        d = leaf.get_distance(a)
        if d < best_d:
            best_d = d; best = a
    return best, best_d


def k_nearest_by_family(leaf, anchors_by_family, k: int = 3) -> tuple[str, float, list[tuple[str, str, float]]]:
    """Return the family with the best (smallest) mean branch-length
    distance among k-nearest anchors. Also return the k-list of
    (family, anchor_name, distance) for transparency.

    This is a cleaner 'who are you closest to in the tree?' metric
    than MRCA containment, which on this tree trivially subsumes
    60/62 leaves under the DRD-anchor MRCA.
    """
    all_pairs = []
    for fam, lst in anchors_by_family.items():
        for a in lst:
            d = leaf.get_distance(a)
            all_pairs.append((fam, a.name, d))
    all_pairs.sort(key=lambda t: t[2])
    knn = all_pairs[:k]
    # majority vote weighted by 1/distance
    from collections import defaultdict as dd
    w = dd(float)
    for fam, _, d in knn:
        w[fam] += 1.0 / max(d, 1e-6)
    best_fam = max(w.items(), key=lambda t: t[1])[0]
    return best_fam, knn[0][2], knn


def classify_candidate(leaf: "Tree", drd_mrca: "Tree", anchors_by_family: dict[str, list]) -> dict[str, object]:
    # Skip drd_mrca check — on this tree the DRD MRCA subsumes nearly
    # everything (anchors span tree). Instead use nearest-anchor-by-
    # family with a k=3 distance-weighted vote.
    # Nearest-anchor
    all_anchors = [a for lst in anchors_by_family.values() for a in lst]
    near, near_d = nearest_anchor(leaf, all_anchors)
    near_fam = family_of(near.name) if near else "unknown"
    # k=3 family vote
    k3_fam, _, knn = k_nearest_by_family(leaf, anchors_by_family, k=3)
    knn_str = ";".join(f"{fam}:{dist:.3f}" for fam, _, dist in knn)
    # Sister family majority at the next internal split
    sister_fam = "NA"
    if leaf.up is not None:
        siblings = [c for c in leaf.up.children if c is not leaf]
        sister_leaves = []
        for sib in siblings:
            sister_leaves.extend(sib.get_leaves())
        fams = Counter(family_of(s.name) for s in sister_leaves if family_of(s.name) not in ("candidate",))
        if fams:
            sister_fam = fams.most_common(1)[0][0]
    # Final call rule: use NEAREST-ANCHOR as primary signal (most
    # defensible single-leaf criterion). Also compute confidence by
    # the delta between nearest and second-nearest of a DIFFERENT
    # family (how much does the call hinge on tree noise?).
    sorted_pairs = sorted(
        [(fam, a.name, leaf.get_distance(a))
         for fam, lst in anchors_by_family.items() for a in lst],
        key=lambda t: t[2])
    d1_fam, _, d1 = sorted_pairs[0]
    d_other = None
    for fam, _, d in sorted_pairs[1:]:
        if fam != d1_fam:
            d_other = d
            break
    delta = (d_other - d1) if d_other is not None else float("inf")
    # call
    if d1_fam == "TRUE_DRD":
        call = "TRUE_DRD"
    else:
        call = f"NOT_DRD:{d1_fam}"
    # mark low confidence if delta < 0.3 branch-length units (i.e., the
    # nearest-family call could flip under moderate tree perturbation)
    if delta < 0.3:
        call = call + "_low_confidence"
    return dict(
        candidate=leaf.name,
        nearest_anchor=near.name if near else "NA",
        nearest_anchor_family=near_fam,
        nearest_anchor_distance=f"{near_d:.4f}" if near else "NA",
        k3_family_vote=k3_fam,
        k3_nearest=knn_str,
        sister_family_majority=sister_fam,
        delta_d_next_other_family=f"{delta:.3f}" if delta != float("inf") else "inf",
        final_call=call,
    )


def main() -> int:
    if not TREEFILE.exists():
        print(f"ERROR: tree file not found: {TREEFILE}", file=sys.stderr)
        return 1
    tree = load_tree(TREEFILE)
    tree = root_outgroup(tree)
    drd_mrca, drd_anchors = find_drd_clade_mrca(tree)
    print(f"DRD MRCA subtree size: {len(drd_mrca.get_leaves())} leaves")

    # Collect anchors by family (exclude candidates)
    anchors_by_family: dict[str, list] = defaultdict(list)
    for leaf in tree.get_leaves():
        fam = family_of(leaf.name)
        if fam in ("candidate", "unknown"):
            continue
        if "_candidate" in leaf.name:
            continue
        anchors_by_family[fam].append(leaf)
    for fam, ls in anchors_by_family.items():
        print(f"  anchors {fam}: n={len(ls)}")

    # Classify each mollusc/cnidarian candidate
    candidates = [l for l in tree.get_leaves() if CAND_RE.search(l.name)]
    print(f"candidates: n={len(candidates)}")

    rows = [classify_candidate(c, drd_mrca, anchors_by_family) for c in candidates]
    # also classify vertebrate DRD candidates (as sanity check)
    vert_candidates = [l for l in tree.get_leaves()
                       if VERT_DRD_RE.search(l.name) and l not in candidates]
    for v in vert_candidates:
        r = classify_candidate(v, drd_mrca, anchors_by_family)
        r["candidate"] = v.name + "  [VERT_SANITY]"
        rows.append(r)

    # write CSV
    with OUT_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"wrote {OUT_CSV}")

    # summary md
    lines = ["# Tree-based classification of mollusc/cnidarian DopR candidates\n"]
    lines.append(f"Tree: `{TREEFILE}`")
    lines.append(f"Rooted on HRH1 (outgroup)")
    lines.append(f"Total leaves: {len(tree.get_leaves())}")
    lines.append(f"DRD MRCA clade size: {len(drd_mrca.get_leaves())}")
    lines.append("")
    lines.append("## Classification (mollusc/cnidarian candidates)")
    lines.append("| candidate | nearest anchor | near. family | dist | delta to next-other-fam | k=3 vote | call |")
    lines.append("|---|---|---|---|---|---|---|")
    mc_rows = [r for r in rows if "VERT_SANITY" not in r["candidate"]]
    for r in sorted(mc_rows, key=lambda x: (x["final_call"], x["candidate"])):
        lines.append(f"| {r['candidate']} | {r['nearest_anchor']} | {r['nearest_anchor_family']} | {r['nearest_anchor_distance']} | {r['delta_d_next_other_family']} | {r['k3_family_vote']} | {r['final_call']} |")
    call_counts = Counter(r["final_call"] for r in mc_rows)
    lines.append("\n### Call distribution (candidates, n=17)")
    for call, n in call_counts.most_common():
        lines.append(f"- {call}: {n}")
    # sanity: vertebrate DRD candidates should all be TRUE_DRD
    lines.append("\n### Vertebrate DRD-candidate sanity check (should be TRUE_DRD)")
    vs_rows = [r for r in rows if "VERT_SANITY" in r["candidate"]]
    vs_call_counts = Counter(r["final_call"] for r in vs_rows)
    for call, n in vs_call_counts.most_common():
        lines.append(f"- {call}: {n}")
    OUT_MD.write_text("\n".join(lines))
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
