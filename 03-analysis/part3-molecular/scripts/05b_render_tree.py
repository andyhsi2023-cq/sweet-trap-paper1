#!/usr/bin/env python3
"""
05b_render_tree.py — render a newick tree to PDF using dendropy + matplotlib.

Falls back from ete3 because ete3 depends on the cgi module which was removed
in Python 3.13+.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import dendropy


def plot_tree(tree: dendropy.Tree, gene: str, out_pdf: Path) -> None:
    # Root at midpoint for display only
    try:
        tree.reroot_at_midpoint(update_bipartitions=False)
    except Exception:
        pass
    # Build x (cumulative branch length) and y (leaf order)
    leaves = list(tree.leaf_node_iter())
    n = len(leaves)
    y_pos: dict = {leaf: i for i, leaf in enumerate(leaves)}

    def depth(node, d=0.0):
        return d + (node.edge.length or 0.0)

    x_pos: dict = {}

    def walk(node, d=0.0):
        d2 = d + (node.edge.length or 0.0)
        x_pos[node] = d2
        for c in node.child_nodes():
            walk(c, d2)
    walk(tree.seed_node)

    # For internal nodes, y = mean of descendant leaf y
    def set_internal_y(node):
        if node.is_leaf():
            return y_pos[node]
        ys = [set_internal_y(c) for c in node.child_nodes()]
        y = sum(ys) / len(ys)
        y_pos[node] = y
        return y
    set_internal_y(tree.seed_node)

    fig, ax = plt.subplots(figsize=(10, max(4, 0.45 * n + 2)))
    # draw branches
    for edge in tree.preorder_edge_iter():
        if edge.head_node is None or edge.tail_node is None:
            continue
        x0 = x_pos[edge.tail_node]
        x1 = x_pos[edge.head_node]
        y1 = y_pos[edge.head_node]
        y0_parent = y_pos[edge.tail_node]
        # horizontal
        ax.plot([x0, x1], [y1, y1], color="black", lw=1.2)
        # vertical connector (drawn once from tail_node handling children below)
    # vertical connectors
    for node in tree.preorder_node_iter():
        if node.is_leaf():
            continue
        child_ys = [y_pos[c] for c in node.child_nodes()]
        if not child_ys:
            continue
        ax.plot([x_pos[node], x_pos[node]],
                [min(child_ys), max(child_ys)], color="black", lw=1.2)

    # leaf labels
    xmax = max(x_pos.values())
    for leaf in leaves:
        label = leaf.taxon.label if leaf.taxon else "?"
        ax.text(x_pos[leaf] + xmax * 0.01, y_pos[leaf], label,
                va="center", fontsize=9, family="monospace")

    # internal node labels (UFBoot) if present
    for node in tree.preorder_node_iter():
        if node.is_leaf() or node == tree.seed_node:
            continue
        if node.label:
            ax.text(x_pos[node] - xmax * 0.01, y_pos[node] + 0.15,
                    str(node.label), fontsize=7, ha="right",
                    color="tab:blue")

    ax.set_xlim(0, xmax * 1.4)
    ax.set_ylim(-0.5, n - 0.5)
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False); ax.spines["top"].set_visible(False)
    ax.set_xlabel("substitutions per site")
    ax.set_title(f"{gene} pilot ML tree (IQ-TREE MFP, UFBoot 1000)",
                 fontsize=11, weight="bold")
    plt.tight_layout()
    plt.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)
    print(f"PDF -> {out_pdf}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("newick")
    ap.add_argument("pdf")
    ap.add_argument("--title", default="ML tree")
    args = ap.parse_args()

    tree = dendropy.Tree.get(path=args.newick, schema="newick")
    plot_tree(tree, args.title, Path(args.pdf))
    return 0


if __name__ == "__main__":
    sys.exit(main())
