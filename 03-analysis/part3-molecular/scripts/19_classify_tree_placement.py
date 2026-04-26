#!/usr/bin/env python3
"""
19_classify_tree_placement.py
=============================

Given the 50-taxon placement tree
(outputs/orthofinder_dop/tree_cnidarian_placement/cnidarian_placement.contree),
decide for each of the 15 cnidarian candidates whether it sits inside the
"true DRD" clade or outside it.

Classification rules:
  * Define REFERENCE DRD clade = MRCA of all vertebrate DRD1+DRD2+arthropod
    DopR1+DopR2 + mollusc Dop (= the 25-taxon set already accepted).
  * A cnidarian candidate is "INSIDE_DRD" if it lies within the DRD clade
    MRCA.
  * Otherwise classify by which reference taxon (HTR/ADRB/ADRA/OA/HRH)
    is its nearest neighbor by patristic distance.

Implementation uses dendropy (ete3 broken on Python 3.14 cgi module).
"""
import csv
import sys
import re
from collections import Counter
from pathlib import Path

import dendropy

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
OUT  = ROOT / "outputs" / "blast_rbh"
TREE = ROOT / "outputs" / "orthofinder_dop" / "tree_cnidarian_placement" / "cnidarian_placement.contree"


def classify_taxon(name: str) -> str:
    """Return functional class tag for a tip name."""
    if re.match(r"^DRD[12]\|", name):
        return "REF_DRD_vert"
    if re.match(r"^DopR[12]\|", name):
        return "REF_DRD_arth"
    if re.match(r"^DopR_\d\|", name):
        return "REF_DRD_moll"
    if name.startswith("HUMAN_HTR"):
        return "OUT_HTR"
    if name.startswith("HUMAN_ADRB"):
        return "OUT_ADRB"
    if name.startswith("HUMAN_ADRA"):
        return "OUT_ADRA"
    if name.startswith("DMEL_OCTB2R"):
        return "OUT_OA"
    if name.startswith("HUMAN_HRH1"):
        return "OUT_HRH"
    if re.match(r"^(Hvul|Nvec|Adig)_", name):
        return "CAND_CNID"
    return "UNK"


def load_tree_iqtree_sanitized(path: Path) -> dendropy.Tree:
    """
    IQ-TREE sanitizes taxon labels by replacing '|' with '_' in the newick
    output. We load and restore the original label mapping via FASTA.
    """
    tns = dendropy.TaxonNamespace()
    tree = dendropy.Tree.get(path=str(path), schema="newick",
                             taxon_namespace=tns,
                             preserve_underscores=True)
    return tree


def main():
    tree = load_tree_iqtree_sanitized(TREE)
    leaf_taxa = [t for t in tree.taxon_namespace]
    print(f"[tree] loaded {len(leaf_taxa)} taxa from {TREE.name}")

    # taxon name -> class
    # note: iqtree may keep or sanitize; we try both
    def t_class(name: str) -> str:
        # try as-is
        c = classify_taxon(name)
        if c != "UNK":
            return c
        # try converting underscores back to '|' after first 4 chars if cnidarian
        return "UNK"

    leaf_classes = {t.label: classify_taxon(t.label) for t in leaf_taxa}
    cls_counter = Counter(leaf_classes.values())
    print(f"[tree] class counts: {dict(cls_counter)}")
    if cls_counter.get("UNK", 0) > 0:
        unks = [lb for lb, c in leaf_classes.items() if c == "UNK"][:10]
        print(f"[tree] WARN UNK leaves (sample): {unks}")

    # Root tree on HRH1 (histamine outgroup)
    hrh_label = next((t.label for t in leaf_taxa if t.label.startswith("HUMAN_HRH1")), None)
    if hrh_label:
        hrh_node = tree.find_node_with_taxon_label(hrh_label)
        if hrh_node is not None:
            tree.to_outgroup_position(hrh_node, update_bipartitions=False)
            print(f"[tree] rooted on {hrh_label}")

    # Identify references & candidates
    ref_drd_labels = [l for l, c in leaf_classes.items() if c.startswith("REF_DRD")]
    cand_labels = [l for l, c in leaf_classes.items() if c == "CAND_CNID"]
    out_labels = [l for l, c in leaf_classes.items() if c.startswith("OUT_")]
    print(f"[tree] REF_DRD={len(ref_drd_labels)} CAND={len(cand_labels)} OUT={len(out_labels)}")

    # MRCA of all DRD references
    ref_drd_taxa = [tree.taxon_namespace.get_taxon(lbl) for lbl in ref_drd_labels]
    mrca_drd = tree.mrca(taxa=ref_drd_taxa)
    drd_mrca_leaves = {l.taxon.label for l in mrca_drd.leaf_iter()}
    print(f"[tree] DRD MRCA subtree contains {len(drd_mrca_leaves)} leaves")

    # Pairwise distance matrix (patristic)
    pdm = tree.phylogenetic_distance_matrix()

    # For each candidate, compute:
    #   - inside DRD MRCA
    #   - sister composition & support
    #   - nearest reference leaf + class + distance
    rows = []

    # Build name -> node
    label2node = {lf.taxon.label: lf for lf in tree.leaf_node_iter()}

    for cand_lbl in cand_labels:
        node = label2node[cand_lbl]
        parent = node.parent_node

        # Inside DRD MRCA?
        inside = cand_lbl in drd_mrca_leaves

        # Sister clade
        siblings = [ch for ch in parent.child_nodes() if ch is not node] if parent else []
        if siblings:
            sis = siblings[0]
            sis_labels = [lf.taxon.label for lf in sis.leaf_iter()]
            sis_classes = [classify_taxon(l) for l in sis_labels]
            sis_comp = Counter(sis_classes)
            sis_size = len(sis_labels)
            sis_top_example = sis_labels[0]
            parent_support = parent.label if parent.label else "NA"
        else:
            sis_labels = []
            sis_size = 0
            sis_comp = Counter()
            sis_top_example = ""
            parent_support = "NA"

        # Nearest reference (non-candidate) by patristic distance
        cand_taxon = tree.taxon_namespace.get_taxon(cand_lbl)
        best_d = None
        best_ref = None
        for ref_lbl in ref_drd_labels + out_labels:
            rt = tree.taxon_namespace.get_taxon(ref_lbl)
            if rt is None:
                continue
            d = pdm.distance(cand_taxon, rt)
            if best_d is None or d < best_d:
                best_d = d
                best_ref = ref_lbl

        row = {
            "taxon": cand_lbl,
            "inside_DRD_clade": inside,
            "sister_size": sis_size,
            "sister_composition": ";".join(f"{k}:{v}" for k, v in sis_comp.most_common()),
            "sister_top_example": sis_top_example,
            "parent_support_ufb": parent_support,
            "nearest_ref_taxon": best_ref or "",
            "nearest_ref_class": classify_taxon(best_ref) if best_ref else "",
            "nearest_ref_distance": f"{best_d:.4f}" if best_d is not None else "",
        }
        rows.append(row)

    # Write TSV
    out_tsv = OUT / "rbh_tree_placement.tsv"
    fields = ["taxon", "inside_DRD_clade", "sister_size", "sister_composition",
              "sister_top_example", "parent_support_ufb",
              "nearest_ref_taxon", "nearest_ref_class", "nearest_ref_distance"]
    with out_tsv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"[tree] -> {out_tsv}")

    # Summary
    inside_n = sum(1 for r in rows if r["inside_DRD_clade"])
    print(f"\n=== Tree placement summary ===")
    print(f"Candidates inside DRD MRCA clade: {inside_n}/{len(rows)}")
    print(f"Candidates outside DRD MRCA clade: {len(rows)-inside_n}/{len(rows)}")

    near_cls_counter = Counter(r["nearest_ref_class"] for r in rows)
    print("\nNearest reference class (by patristic distance):")
    for k, v in near_cls_counter.most_common():
        print(f"  {k}: {v}")

    # Per-candidate print
    print("\n=== Per-candidate placement ===")
    hdr = f"{'taxon':<30} {'in_DRD':<7} {'nearest_class':<14} {'dist':<7} {'UFB':<5} {'sis_n':<6} {'sis_comp':<50}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        tax_short = r["taxon"][:28]
        comp = r["sister_composition"][:48]
        ufb = str(r["parent_support_ufb"])[:5]
        print(f"{tax_short:<30} {str(r['inside_DRD_clade']):<7} {r['nearest_ref_class']:<14} {r['nearest_ref_distance']:<7} {ufb:<5} {str(r['sister_size']):<6} {comp:<50}")


if __name__ == "__main__":
    main()
