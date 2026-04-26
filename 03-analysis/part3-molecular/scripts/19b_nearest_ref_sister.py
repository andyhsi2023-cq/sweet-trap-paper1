#!/usr/bin/env python3
"""
19b_nearest_ref_sister.py
=========================

Extended tree analysis: for each cnidarian candidate, walk up parent nodes
until sister subtree contains at least one REFERENCE taxon (not a
candidate). Record that reference sister's class composition.

This answers: "when we leave the cnidarian-specific subtree, what amine
family do we join?"
"""
import re
from collections import Counter
from pathlib import Path

import dendropy

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
OUT  = ROOT / "outputs" / "blast_rbh"
TREE = ROOT / "outputs" / "orthofinder_dop" / "tree_cnidarian_placement" / "cnidarian_placement.contree"


def classify_taxon(name: str) -> str:
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


def main():
    tns = dendropy.TaxonNamespace()
    tree = dendropy.Tree.get(path=str(TREE), schema="newick",
                             taxon_namespace=tns,
                             preserve_underscores=True)
    tree.is_rooted = True
    # root on HRH1
    for t in tree.taxon_namespace:
        if t.label.startswith("HUMAN_HRH1"):
            tree.to_outgroup_position(tree.find_node_with_taxon_label(t.label),
                                       update_bipartitions=False)
            break

    label2node = {lf.taxon.label: lf for lf in tree.leaf_node_iter()}

    print(f"\n{'taxon':<30} {'levels_up':<10} {'ref_sister_composition':<60} {'nearest_ref_in_sister':<40}")
    print("-" * 140)

    for cand_lbl, leaf in label2node.items():
        if classify_taxon(cand_lbl) != "CAND_CNID":
            continue

        current = leaf
        levels = 0
        ref_sister_comp = None
        ref_sister_example = None
        support_chain = []
        while current.parent_node is not None:
            parent = current.parent_node
            if parent.label:
                support_chain.append(parent.label)
            siblings = [ch for ch in parent.child_nodes() if ch is not current]
            if not siblings:
                break
            # combine all sibling subtrees
            sib_labels = []
            for s in siblings:
                if s.is_leaf():
                    sib_labels.append(s.taxon.label)
                else:
                    sib_labels.extend(lf.taxon.label for lf in s.leaf_iter())
            sib_classes = [classify_taxon(l) for l in sib_labels]
            non_cand = [(l, c) for l, c in zip(sib_labels, sib_classes) if c != "CAND_CNID"]
            if non_cand:
                comp = Counter(c for _, c in non_cand)
                ref_sister_comp = ";".join(f"{k}:{v}" for k, v in comp.most_common())
                ref_sister_example = non_cand[0][0]
                break
            current = parent
            levels += 1

        comp_str = ref_sister_comp or "(root)"
        ex_str = (ref_sister_example or "")[:38]
        print(f"{cand_lbl[:28]:<30} {levels:<10} {comp_str[:58]:<60} {ex_str:<40}")


if __name__ == "__main__":
    main()
