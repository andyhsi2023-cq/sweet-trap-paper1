#!/usr/bin/env python
"""
01_prepare_codeml_inputs_v2.py
==============================

Week-2 Part 4 production prep. Ports the v4 positive-control fix:
  - "#1" attaches to the CLOSING paren / tip name with NO intervening whitespace
    (the ete3 path used by v1 produced `A #1` which PAML silently drops)
  - explicit clade-MRCA labelling by substring match (not ete3 MRCA), mirroring
    `positive_control_v4_prepare.py`
  - tip-match by substring: tolerates the Part-3 composite tip format
    `TAS1R1|Homo_sapiens|ENST00000333172.11` (we look for the species-name token
    surrounded by non-word boundaries) — only ONE matching tip may exist.

Inputs
------
- V2 matrix : scripts/branch_site_test_matrix_v2.tsv (this script generates it
  if absent). Per-row fields:
    gene, lineage_key, fg_type, fg_label, alignment_source, notes
    - fg_type:        tip | clade | tip_underpowered
    - fg_label:       tip name   OR   pipe-separated list of tip anchor tokens
                       for MRCA definition (we label the MRCA internal branch
                       AND every tip in the clade, mirroring v4_apodiformes_clade
                       which was the winning gate configuration)
    - alignment_source:
        "v4_hummingbird"   -> data/positive_control/work/codon_aligned_v4.phy
                              + species_tree_v4.nwk (species-only names)
        "part3_tas1r1"     -> data/alignments/TAS1R1_codon.fasta (5 taxa, composite names)
        "part3_tas1r3"     -> data/alignments/TAS1R3_codon.fasta (5 taxa)
        "part3_gr"         -> data/alignments/Gr_sweet_codon.fasta (38 insect hits)
                              + Gr_family_pilot_tree.nwk
- Codon alignment  : see alignment_source mapping above
- Species/gene tree: see alignment_source mapping

Outputs
-------
- data/codeml_runs/<run_id>/alignment.phy
- data/codeml_runs/<run_id>/tree_labelled.nwk
- data/codeml_runs/<run_id>/null.ctl
- data/codeml_runs/<run_id>/alt.ctl
- logs/01_prepare_v2_<timestamp>.log + 01_prepare_v2_summary.tsv

Policy
------
Feasibility gates (documented in output summary):
  OK           -> alignment + tree present AND all tip anchors resolved
  SKIP_MISSING -> alignment or tree missing (dopamine/opioid/NPY genes; Part 3
                  did not deliver codon alignments for them)
  SKIP_RESOLVE -> foreground tips not found in tree (e.g. asking for `Apis_mellifera`
                  in an alignment whose tip names are `Gr_sweet_hit1_amellifera`)
  SKIP_SPARSE  -> alignment has < 4 taxa (TAS1R2 trio — insufficient for branch-site test)

Usage
-----
  python 01_prepare_codeml_inputs_v2.py                # prep all feasible rows
  python 01_prepare_codeml_inputs_v2.py --matrix-only  # emit matrix and exit
"""
from __future__ import annotations

import argparse
import datetime as _dt
import logging
import re
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
PART3 = ROOT.parent / "part3-molecular"
ALIGN_DIR = PART3 / "data" / "alignments"
TREE_DIR = PART3 / "outputs"

V4_WORK = ROOT / "data" / "positive_control" / "work"
RUNS_DIR = ROOT / "data" / "codeml_runs"
LOGS_DIR = ROOT / "logs"
SCRIPTS_DIR = ROOT / "scripts"

MATRIX_TSV = SCRIPTS_DIR / "branch_site_test_matrix_v2.tsv"
NULL_CTL = SCRIPTS_DIR / "00_codeml_model_a_null.ctl"
ALT_CTL = SCRIPTS_DIR / "00_codeml_model_a_alt.ctl"

# ------------------------------------------------------------------------------
# V2 MATRIX
# ------------------------------------------------------------------------------
# 22 rows + 3 already-done v4 control rows re-verified.
#
# Gate-cleared positive controls (already in codeml_runs/, reuse in aggregation):
#   TAS1R1_pc_v4__apodiformes_clade   LRT=55.90  p=3.8e-14
#   TAS1R1_pc_v4__hummingbirds_clade  LRT=61.06  p=2.8e-15
#   TAS1R1_pc_v4__mouse_control       LRT=0.00   p=0.500
#
# All 22 non-control rows below; we pick alignment by (gene, foreground).
# ------------------------------------------------------------------------------

V2_ROWS = [
    # === TIER A: v4 hummingbird TAS1R1 alignment (16 taxa) =====================
    # Use Baldwin-scale taxon set to test non-hummingbird lineages in same tree.
    {"gene": "TAS1R1", "lineage_key": "mammalia_clade_v4", "fg_type": "clade",
     "fg_label": "Homo_sapiens|Mus_musculus|Rattus_norvegicus",
     "alignment_source": "v4_hummingbird",
     "notes": "Mammalian TAS1R1 ancestor (omnivore-to-herbivore MRCA) against hummingbird-rich tree"},
    {"gene": "TAS1R1", "lineage_key": "rodentia_clade_v4", "fg_type": "clade",
     "fg_label": "Mus_musculus|Rattus_norvegicus",
     "alignment_source": "v4_hummingbird",
     "notes": "Rodent umami-specialist lineage (granivore shift)"},
    {"gene": "TAS1R1", "lineage_key": "homo_tip_v4", "fg_type": "tip_underpowered",
     "fg_label": "Homo_sapiens",
     "alignment_source": "v4_hummingbird",
     "notes": "Human TAS1R1 lineage (sensitivity; single tip)"},
    {"gene": "TAS1R1", "lineage_key": "gallus_tip_v4", "fg_type": "tip_underpowered",
     "fg_label": "Gallus_gallus",
     "alignment_source": "v4_hummingbird",
     "notes": "Chicken TAS1R1 (omnivore sauropsid; known TAS1R1 divergence)"},
    {"gene": "TAS1R1", "lineage_key": "danio_tip_v4", "fg_type": "tip_underpowered",
     "fg_label": "Danio_rerio",
     "alignment_source": "v4_hummingbird",
     "notes": "Zebrafish outgroup tip (sensitivity)"},
    {"gene": "TAS1R1", "lineage_key": "passeriformes_tip_v4", "fg_type": "tip_underpowered",
     "fg_label": "Serinus_canaria",
     "alignment_source": "v4_hummingbird",
     "notes": "Canary granivore passerine (seed-eater; sensitivity)"},
    {"gene": "TAS1R1", "lineage_key": "apus_tip_v4", "fg_type": "tip_underpowered",
     "fg_label": "Apus_apus",
     "alignment_source": "v4_hummingbird",
     "notes": "Swift (insectivore Apodiformes; sister to hummingbirds)"},

    # === TIER B: Part-3 TAS1R3 alignment (5 taxa) ==============================
    {"gene": "TAS1R3", "lineage_key": "mammalia_clade", "fg_type": "clade",
     "fg_label": "Homo_sapiens|Mus_musculus|Rattus_norvegicus",
     "alignment_source": "part3_tas1r3",
     "notes": "Mammalian TAS1R3 ancestor (sweet-receptor clade)"},
    {"gene": "TAS1R3", "lineage_key": "rodentia_clade", "fg_type": "clade",
     "fg_label": "Mus_musculus|Rattus_norvegicus",
     "alignment_source": "part3_tas1r3",
     "notes": "Rodent TAS1R3 lineage"},
    {"gene": "TAS1R3", "lineage_key": "homo_tip", "fg_type": "tip_underpowered",
     "fg_label": "Homo_sapiens",
     "alignment_source": "part3_tas1r3",
     "notes": "Human TAS1R3 lineage (sensitivity)"},
    {"gene": "TAS1R3", "lineage_key": "gallus_tip", "fg_type": "tip_underpowered",
     "fg_label": "Gallus_gallus",
     "alignment_source": "part3_tas1r3",
     "notes": "Chicken TAS1R3 (sauropsid sweet-lineage)"},
    {"gene": "TAS1R3", "lineage_key": "danio_tip", "fg_type": "tip_underpowered",
     "fg_label": "Danio_rerio",
     "alignment_source": "part3_tas1r3",
     "notes": "Zebrafish outgroup"},

    # === TIER C: Part-3 TAS1R1 alignment (5 taxa; cross-reference to v4) =======
    # Single mammalia_clade row — main tests go through v4 alignment
    {"gene": "TAS1R1", "lineage_key": "mammalia_clade_p3", "fg_type": "clade",
     "fg_label": "Homo_sapiens|Mus_musculus|Rattus_norvegicus",
     "alignment_source": "part3_tas1r1",
     "notes": "Mammalian TAS1R1 ancestor on Part-3 5-taxon alignment (cross-reference)"},

    # === TIER D: Part-3 Gr_sweet alignment (38 insect sequences) ===============
    # Tips use the hit format `Gr_sweet_hitN_<species>` or `Gr5a_dmelanogaster`.
    # We label all tips containing the anchor substring as foreground + their MRCA.
    {"gene": "Gr_sweet", "lineage_key": "dmel_Gr64_cluster", "fg_type": "clade",
     "fg_label": "Gr64a_dmelanogaster|Gr64b_dmelanogaster|Gr64c_dmelanogaster|Gr64d_dmelanogaster|Gr64e_dmelanogaster|Gr64f_dmelanogaster",
     "alignment_source": "part3_gr",
     "notes": "Drosophila Gr64 sweet-receptor cluster (canonical sweet GRs)"},
    {"gene": "Gr_sweet", "lineage_key": "amellifera_clade", "fg_type": "clade",
     "fg_label": "Gr_sweet_hit1_amellifera|Gr_sweet_hit2_amellifera|Gr_sweet_hit3_amellifera|Gr_sweet_hit4_amellifera",
     "alignment_source": "part3_gr",
     "notes": "Honeybee (A. mellifera) nectarivore Gr clade — key H6a prediction"},
    {"gene": "Gr_sweet", "lineage_key": "lepidoptera_clade", "fg_type": "clade",
     "fg_label": "Gr_sweet_hit1_bmori|Gr_sweet_hit2_bmori|Gr_sweet_hit3_bmori|Gr_sweet_hit4_bmori|Gr_sweet_hit5_bmori|Gr_sweet_hit6_bmori|Gr_sweet_hit1_msexta|Gr_sweet_hit2_msexta|Gr_sweet_hit3_msexta|Gr_sweet_hit4_msexta|Gr_sweet_hit5_msexta|Gr_sweet_hit6_msexta|Gr_sweet_hit7_msexta",
     "alignment_source": "part3_gr",
     "notes": "Lepidoptera (Bombyx+Manduca) Gr clade — herbivore larva to nectar-feeding adult"},
    {"gene": "Gr_sweet", "lineage_key": "coleoptera_clade", "fg_type": "clade",
     "fg_label": "Gr_sweet_hit1_tcastaneum|Gr_sweet_hit2_tcastaneum|Gr_sweet_hit3_tcastaneum|Gr_sweet_hit4_tcastaneum|Gr_sweet_hit5_tcastaneum|Gr_sweet_hit6_tcastaneum|Gr_sweet_hit7_tcastaneum",
     "alignment_source": "part3_gr",
     "notes": "Coleoptera (Tribolium granary beetle) Gr clade — granivorous pest"},
    {"gene": "Gr_sweet", "lineage_key": "aaegypti_clade", "fg_type": "clade",
     "fg_label": "Gr_sweet_hit1_aaegypti|Gr_sweet_hit2_aaegypti|Gr_sweet_hit3_aaegypti|Gr_sweet_hit4_aaegypti|Gr_sweet_hit5_aaegypti|Gr_sweet_hit6_aaegypti|Gr_sweet_hit7_aaegypti",
     "alignment_source": "part3_gr",
     "notes": "Mosquito (Aedes aegypti) Gr clade — haematophagous reward shift"},
    {"gene": "Gr_sweet", "lineage_key": "dmel_all_clade", "fg_type": "clade",
     "fg_label": "Gr5a_dmelanogaster|Gr64a_dmelanogaster|Gr64b_dmelanogaster|Gr64c_dmelanogaster|Gr64d_dmelanogaster|Gr64e_dmelanogaster|Gr64f_dmelanogaster",
     "alignment_source": "part3_gr",
     "notes": "All D. melanogaster Gr5a+Gr64 sweet receptors as combined foreground"},
    {"gene": "Gr_sweet", "lineage_key": "Gr5a_tip", "fg_type": "tip_underpowered",
     "fg_label": "Gr5a_dmelanogaster",
     "alignment_source": "part3_gr",
     "notes": "D. melanogaster Gr5a (trehalose-specific sweet receptor; single tip)"},
    {"gene": "Gr_sweet", "lineage_key": "Gr64a_tip", "fg_type": "tip_underpowered",
     "fg_label": "Gr64a_dmelanogaster",
     "alignment_source": "part3_gr",
     "notes": "D. melanogaster Gr64a (broad-spectrum sweet; single tip)"},
]

# ------------------------------------------------------------------------------
# Alignment-source resolution
# ------------------------------------------------------------------------------

def resolve_alignment_source(source: str) -> tuple[Path | None, Path | None, str]:
    """Return (alignment_phy, tree_newick, taxon_rename_mode)."""
    if source == "v4_hummingbird":
        aln = V4_WORK / "codon_aligned_v4.phy"
        tree = V4_WORK / "species_tree_v4.nwk"
        return aln, tree, "species_only"
    if source == "part3_tas1r1":
        aln = ALIGN_DIR / "TAS1R1_codon.fasta"
        tree = TREE_DIR / "pilot_tree_tas1r1.nwk"
        return aln, tree, "composite"  # TAS1R1|Danio_rerio|ENSDART...
    if source == "part3_tas1r3":
        aln = ALIGN_DIR / "TAS1R3_codon.fasta"
        tree = TREE_DIR / "pilot_tree_tas1r3.nwk"
        return aln, tree, "composite"
    if source == "part3_gr":
        aln = ALIGN_DIR / "Gr_sweet_codon.fasta"
        tree = TREE_DIR / "Gr_family_pilot_tree.nwk"
        return aln, tree, "literal"  # Gr5a_dmelanogaster (no species-only rename)
    return None, None, ""

# ------------------------------------------------------------------------------
# Conversion utilities
# ------------------------------------------------------------------------------

def fasta_to_phylip_species_only(fasta_path: Path, out_path: Path) -> list[str]:
    """Convert FASTA to PAML Phylip, stripping `GENE|` prefix and `|accession` suffix
    so tip names are species-only (matches the v4_hummingbird convention)."""
    from Bio import SeqIO
    records = list(SeqIO.parse(fasta_path, "fasta"))
    if not records:
        raise ValueError(f"Empty FASTA: {fasta_path}")
    aln_len = len(records[0].seq)
    names = []
    for r in records:
        if len(r.seq) != aln_len:
            raise ValueError(f"Unequal length in {fasta_path}")
        # Strip "GENE|" prefix and "|accession" suffix
        parts = r.id.split("|")
        if len(parts) == 3:
            name = parts[1]
        else:
            name = r.id
        names.append(name)
    with out_path.open("w") as fh:
        fh.write(f" {len(records)} {aln_len}\n")
        for name, r in zip(names, records):
            padded = name[:30].ljust(30)
            fh.write(f"{padded}  {str(r.seq)}\n")
    return names


def fasta_to_phylip_literal(fasta_path: Path, out_path: Path) -> list[str]:
    """Convert FASTA to PAML Phylip preserving tip IDs verbatim."""
    from Bio import SeqIO
    records = list(SeqIO.parse(fasta_path, "fasta"))
    if not records:
        raise ValueError(f"Empty FASTA: {fasta_path}")
    aln_len = len(records[0].seq)
    names = []
    for r in records:
        if len(r.seq) != aln_len:
            raise ValueError(f"Unequal length in {fasta_path}")
        names.append(r.id)
    with out_path.open("w") as fh:
        fh.write(f" {len(records)} {aln_len}\n")
        for r in records:
            padded = r.id[:30].ljust(30)
            fh.write(f"{padded}  {str(r.seq)}\n")
    return names


def rewrite_tree_species_only(tree_text: str) -> str:
    """For Part-3 trees with `GENE|SPECIES|ACC` tips: strip to `SPECIES`."""
    # Replace `TAS1R1|Homo_sapiens|ENST00000333172.11` -> `Homo_sapiens`
    return re.sub(r"[A-Za-z0-9_\-]+\|([A-Za-z_]+)\|[A-Za-z0-9_.]+", r"\1", tree_text)


def strip_branch_lengths_and_support(tree_text: str) -> str:
    """Remove `:NNN.NNN` branch lengths and `NNN:` bootstrap-attached branch-lengths.
    Also strips node-support labels (numbers immediately after ')' before ':' or ',').
    Leaves labels like `#1` untouched because they are not bare numerics."""
    # 1. strip branch lengths  ":12.345" or ":1e-06"
    t = re.sub(r":[0-9]+\.?[0-9]*(?:[eE][+-]?[0-9]+)?", "", tree_text)
    # 2. strip internal-node numeric labels (bootstrap): ")100" -> ")"
    t = re.sub(r"\)[0-9]+", ")", t)
    return t


# ------------------------------------------------------------------------------
# Foreground labelling (v4-style, no leading space before #1)
# ------------------------------------------------------------------------------

def label_tip(tree: str, tip: str, marker: str = "#1") -> tuple[str, bool]:
    """Append marker directly to the tip name (no space). Returns (new_tree, ok)."""
    pattern = re.compile(rf"\b{re.escape(tip)}\b")
    count = len(pattern.findall(tree))
    if count == 0:
        return tree, False
    if count > 1:
        # Multiple hits (usually from substring-style Gr names) - not a problem
        # but we want to mark ALL of them if asked via this function; caller
        # decides. For single-tip foreground calls we reject duplicates.
        return tree, False
    return pattern.sub(f"{tip}{marker}", tree, count=1), True


def label_all_tips_matching(tree: str, tips: list[str]) -> tuple[str, list[str]]:
    """Label every listed tip (must be exact-match terminal taxa in tree).
    Returns (new_tree, list_of_successfully_labelled_tips)."""
    labelled = []
    t = tree
    for tip in tips:
        pattern = re.compile(rf"\b{re.escape(tip)}\b(?!#)")
        if pattern.search(t):
            t = pattern.sub(f"{tip}#1", t, count=1)
            labelled.append(tip)
    return t, labelled


def label_mrca(tree: str, tips: list[str]) -> tuple[str, bool]:
    """Label the MRCA internal branch of the given tips with #1 (no space).

    Strategy:
      1. Build an ete3 tree; find the MRCA; get its deepest descendant set.
      2. In the ORIGINAL Newick text, identify the smallest enclosing
         parenthesised clade whose leaves are exactly that descendant set.
      3. Insert `#1` immediately after the closing `)` of that clade.

    This avoids ete3's `.name = "#1"` serialisation quirks by operating on
    the raw Newick string (same approach as v4 prep).
    """
    from ete3 import Tree
    try:
        t = Tree(tree, format=1)
    except Exception:
        # Try format=5 (internal node labels but no branch lengths)
        try:
            t = Tree(tree, format=5)
        except Exception as e:
            logging.error("ete3 parse failed: %s", e)
            return tree, False

    present = [tip for tip in tips if t.search_nodes(name=tip)]
    if len(present) < 2:
        return tree, False

    mrca = t.get_common_ancestor(present)
    mrca_leaves = set(l.name for l in mrca.get_leaves())

    # Walk the Newick string and find the minimal enclosing clade with matching leaves.
    # Simpler approach: write MRCA subtree via ete3 into a canonical form, strip
    # branch lengths/bootstrap, then find that substring in the (stripped) input.
    sub = mrca.write(format=9)  # topology only, no branch lengths, leaf names only
    sub = sub.rstrip(";").strip()
    # Also clean the input tree similarly for substring matching
    clean = strip_branch_lengths_and_support(tree)

    # Now we need a canonical-form match of the MRCA clade inside the cleaned tree.
    # ete3 may reorder siblings. Strategy: find smallest `(...)` substring whose
    # unlabelled leaf set equals mrca_leaves.
    pos = _find_minimal_clade_span(clean, mrca_leaves)
    if pos is None:
        logging.warning("Could not locate MRCA clade span for %s", tips[:5])
        return tree, False
    start, end = pos  # end is position of the matching ')'
    labelled = clean[:end + 1] + "#1" + clean[end + 1:]
    return labelled, True


def _find_minimal_clade_span(newick_clean: str, target_leaves: set[str]) -> tuple[int, int] | None:
    """Return (start, end) of the minimal parenthesised clade in newick_clean whose
    leaf set exactly equals target_leaves. Indices refer to '(' and ')'."""
    # Build index of matching parens
    stack = []
    pairs = []  # list of (open_idx, close_idx)
    for i, ch in enumerate(newick_clean):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if not stack:
                return None
            o = stack.pop()
            pairs.append((o, i))
    # For each pair, extract the leaf set
    best = None
    best_len = None
    for o, c in pairs:
        clade_str = newick_clean[o:c + 1]
        # Extract leaf tokens: split on `(`, `)`, `,` and drop empty
        leaves = set()
        for token in re.split(r"[(),]", clade_str):
            token = token.strip()
            # Drop trailing #1 / numeric support (none here since we strip_branch_lengths_and_support)
            token = token.rstrip("#1").rstrip()
            if token and not token.isdigit():
                leaves.add(token)
        if leaves == target_leaves:
            L = c - o
            if best_len is None or L < best_len:
                best = (o, c)
                best_len = L
    return best


# ------------------------------------------------------------------------------
# Row preparation
# ------------------------------------------------------------------------------

def customise_ctl(template: Path, run_dir: Path, out_name: str) -> None:
    text = template.read_text()
    (run_dir / out_name).write_text(text)


def prepare_row(row: dict, dry_run: bool = False) -> dict:
    gene = row["gene"]
    lineage_key = row["lineage_key"]
    fg_type = row["fg_type"]
    fg_label = row["fg_label"]
    source = row["alignment_source"]
    run_id = f"{gene}__{lineage_key}"
    run_dir = RUNS_DIR / run_id

    result = {
        "run_id": run_id,
        "gene": gene,
        "lineage": lineage_key,
        "fg_type": fg_type,
        "alignment_source": source,
        "prepared": False,
        "reason": "",
        "n_fg_labelled": 0,
    }

    aln_path, tree_path, rename_mode = resolve_alignment_source(source)
    if aln_path is None:
        result["reason"] = f"unknown alignment_source={source}"
        return result
    if not aln_path.exists():
        result["reason"] = f"SKIP_MISSING: no alignment at {aln_path}"
        return result
    if not tree_path.exists():
        result["reason"] = f"SKIP_MISSING: no tree at {tree_path}"
        return result

    if dry_run:
        run_dir.mkdir(parents=True, exist_ok=True)
        result["prepared"] = True
        result["reason"] = "dry_run"
        return result

    run_dir.mkdir(parents=True, exist_ok=True)

    # --- Build alignment.phy ---
    if rename_mode == "species_only":
        # v4_hummingbird: source is already .phy with species-only names
        shutil.copy(aln_path, run_dir / "alignment.phy")
    elif rename_mode == "composite":
        fasta_to_phylip_species_only(aln_path, run_dir / "alignment.phy")
    elif rename_mode == "literal":
        fasta_to_phylip_literal(aln_path, run_dir / "alignment.phy")
    else:
        result["reason"] = f"unknown rename_mode={rename_mode}"
        return result

    # --- Build labelled tree ---
    tree_text = tree_path.read_text().strip()
    if rename_mode == "composite":
        tree_text = rewrite_tree_species_only(tree_text)
    # Strip branch lengths + bootstrap before labelling (PAML doesn't need them;
    # fix_blength=0 in ctl means codeml ignores them anyway, and it avoids
    # parser edge-cases when inserting #1 near `)100:0.123`)
    tree_text = strip_branch_lengths_and_support(tree_text)

    fg_tips = fg_label.split("|")
    n_labelled = 0

    if fg_type == "tip" or fg_type == "tip_underpowered":
        if len(fg_tips) != 1:
            result["reason"] = f"tip fg should be single name, got {fg_tips}"
            return result
        labelled_tree, ok = label_tip(tree_text, fg_tips[0])
        if not ok:
            result["reason"] = f"SKIP_RESOLVE: tip '{fg_tips[0]}' not in tree"
            return result
        n_labelled = 1
    elif fg_type == "clade":
        # POLICY: For species trees (v4_hummingbird, part3_tas1r1, part3_tas1r3),
        # label MRCA + all tips (v4_apodiformes_clade winning design).
        # For GENE trees (part3_gr), species are paraphyletic (paralogs scattered
        # across the tree), so MRCA labelling incorrectly engulfs other species.
        # Only label the tip branches — this mirrors how H6a-type tests treat
        # gene-family trees (the foreground is the union of paralog branches in
        # the focal species).
        is_gene_tree = (source == "part3_gr")
        if is_gene_tree:
            labelled_tree, labelled_tips = label_all_tips_matching(tree_text, fg_tips)
            if len(labelled_tips) < 2:
                result["reason"] = f"SKIP_RESOLVE: fewer than 2 tips labelled ({labelled_tips})"
                return result
            n_labelled = len(labelled_tips)
        else:
            labelled_tree, mrca_ok = label_mrca(tree_text, fg_tips)
            if not mrca_ok:
                result["reason"] = f"SKIP_RESOLVE: could not label MRCA for {fg_tips}"
                return result
            labelled_tree, labelled_tips = label_all_tips_matching(labelled_tree, fg_tips)
            n_labelled = 1 + len(labelled_tips)  # MRCA branch + tips
            if len(labelled_tips) < 2:
                result["reason"] = f"SKIP_RESOLVE: fewer than 2 tips labelled ({labelled_tips})"
                return result
    else:
        result["reason"] = f"unknown fg_type={fg_type}"
        return result

    # Count taxa in alignment
    with (run_dir / "alignment.phy").open() as fh:
        header = fh.readline().split()
        n_tax = int(header[0])

    if n_tax < 4:
        result["reason"] = f"SKIP_SPARSE: only {n_tax} taxa in alignment"
        return result

    # Write tree
    (run_dir / "tree_labelled.nwk").write_text(f" {n_tax} 1\n{labelled_tree};\n")
    # Oops - we need to avoid double semicolon; strip_branch_lengths... already
    # removes trailing ';' sometimes
    fix_text = (run_dir / "tree_labelled.nwk").read_text()
    fix_text = fix_text.replace(";;", ";")
    (run_dir / "tree_labelled.nwk").write_text(fix_text)

    # --- Copy ctl templates ---
    customise_ctl(NULL_CTL, run_dir, "null.ctl")
    customise_ctl(ALT_CTL, run_dir, "alt.ctl")

    result["prepared"] = True
    result["reason"] = "OK"
    result["n_fg_labelled"] = n_labelled
    return result


# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------

def _setup_logging() -> Path:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS_DIR / f"01_prepare_v2_{stamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler(sys.stdout)],
        force=True,
    )
    return log_path


def emit_matrix() -> pd.DataFrame:
    df = pd.DataFrame(V2_ROWS)
    df.to_csv(MATRIX_TSV, sep="\t", index=False)
    logging.info("Wrote v2 matrix: %s (%d rows)", MATRIX_TSV, len(df))
    return df


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--matrix-only", action="store_true")
    ap.add_argument("--only", default=None,
                    help="Restrict to a single run_id (gene__lineage)")
    args = ap.parse_args()

    log_path = _setup_logging()
    logging.info("01_prepare_codeml_inputs_v2 starting; log=%s", log_path)

    matrix = emit_matrix()
    if args.matrix_only:
        return 0

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for _, row in matrix.iterrows():
        row_d = row.to_dict()
        run_id = f"{row_d['gene']}__{row_d['lineage_key']}"
        if args.only and args.only != run_id:
            continue
        try:
            r = prepare_row(row_d, dry_run=args.dry_run)
        except Exception as exc:
            logging.exception("Row failure: %s", run_id)
            r = {"run_id": run_id, "prepared": False, "reason": f"exception: {exc}",
                 "fg_type": row_d.get("fg_type", ""),
                 "alignment_source": row_d.get("alignment_source", ""),
                 "n_fg_labelled": 0, "gene": row_d["gene"], "lineage": row_d["lineage_key"]}
        results.append(r)
        logging.info("[%s] %s (n_fg=%d)",
                     "OK  " if r["prepared"] else "SKIP",
                     f"{r['run_id']} :: {r['reason']}",
                     r.get("n_fg_labelled", 0))

    summary = LOGS_DIR / "01_prepare_v2_summary.tsv"
    pd.DataFrame(results).to_csv(summary, sep="\t", index=False)
    n_ok = sum(1 for r in results if r["prepared"])
    logging.info("Prepared %d / %d runs. Summary: %s", n_ok, len(results), summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
