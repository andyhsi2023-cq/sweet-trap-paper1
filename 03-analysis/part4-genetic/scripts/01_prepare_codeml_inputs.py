#!/usr/bin/env python
"""
01_prepare_codeml_inputs.py
===========================

Purpose
-------
For every (gene, foreground-lineage) pair in the Part 4 H6a test matrix,
build a self-contained codeml run directory containing:

  data/codeml_runs/<gene>__<lineage>/
      ├── alignment.phy          (PAML-style Phylip interleaved, codon aligned)
      ├── tree_labelled.nwk      (Newick with foreground branch tagged "#1")
      ├── null.ctl               (derived from scripts/00_codeml_model_a_null.ctl)
      └── alt.ctl                (derived from scripts/00_codeml_model_a_alt.ctl)

Inputs
------
- Codon alignment  : ../part3-molecular/data/alignments/<gene>_codon.fasta
- Species tree     : ../part3-molecular/outputs/pilot_tree_<gene>.nwk  (preferred)
                     fallback: ../part3-molecular/outputs/species_tree.nwk
- Test matrix      : scripts/branch_site_test_matrix.tsv (this file generates it
                     on first call if absent; hand-edit as needed)

Foreground labelling rules
--------------------------
- If the lineage is a single terminal taxon (e.g. "hummingbird_TAS1R1"), mark
  the tip label with "#1".
- If the lineage is a clade (e.g. "Apidae"), mark the MRCA internal branch
  with "#1" (ete3 will handle this via node traversal).
- One "#1" mark per tree. PAML branch-site Model A allows only one foreground
  branch per run.

Positive control
----------------
The matrix ships with hummingbird TAS1R1 as the first row. This REPLICATES
Baldwin et al. 2014 Science (DOI 10.1126/science.1255097, PMID 25146290) and
functions as the pipeline validation run. Expected: omega_foreground > 1, LRT
p < 0.01. If this positive control fails, the pipeline is broken and no
downstream results should be trusted.

Outputs
-------
- data/codeml_runs/<gene>__<lineage>/ directories (one per row of matrix)
- logs/01_prepare_codeml_inputs_<timestamp>.log

Dependencies
------------
- Python >= 3.10
- Biopython (Bio.SeqIO, Bio.Phylo)
- ete3 (for MRCA-based clade labelling)
- pandas

Blocking status
---------------
This script is BLOCKED on Part 3 delivering:
  - ../part3-molecular/data/alignments/<gene>_codon.fasta   (one per gene)
  - ../part3-molecular/outputs/pilot_tree_<gene>.nwk        (one per gene)

Run in DRY-RUN mode (python 01_prepare_codeml_inputs.py --dry-run) to emit
the test matrix TSV and verify directory scaffolding without needing the
alignments.

Usage
-----
  python 01_prepare_codeml_inputs.py --dry-run         # emit matrix only
  python 01_prepare_codeml_inputs.py                   # full prep (needs Part 3)
  python 01_prepare_codeml_inputs.py --gene TAS1R1 --only-control
"""

from __future__ import annotations

import argparse
import datetime as _dt
import logging
import shutil
import sys
from pathlib import Path

import pandas as pd

# --- Repository layout ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]          # 03-analysis/part4-genetic
PART3 = ROOT.parent / "part3-molecular"
ALIGN_DIR = PART3 / "data" / "alignments"
TREE_DIR = PART3 / "outputs"
RUNS_DIR = ROOT / "data" / "codeml_runs"
LOGS_DIR = ROOT / "logs"
SCRIPTS_DIR = ROOT / "scripts"
MATRIX_TSV = SCRIPTS_DIR / "branch_site_test_matrix.tsv"

NULL_CTL_TEMPLATE = SCRIPTS_DIR / "00_codeml_model_a_null.ctl"
ALT_CTL_TEMPLATE = SCRIPTS_DIR / "00_codeml_model_a_alt.ctl"

# --- H6a test matrix (15 genes x >=4 foreground lineages + controls) -----------
# Each row: one codeml branch-site run. Foreground specification key:
#   fg_type = "tip"   -> fg_label matches a terminal taxon exactly
#   fg_type = "clade" -> fg_label is the MRCA of the listed tip taxa (pipe-sep)
#
# Genes covered (Paper 1 target list from evidence_architecture_v4 §5.1):
#   Sweet/umami taste : TAS1R1, TAS1R2, TAS1R3
#   Dopamine receptors: DRD1, DRD2, DRD3, DRD4, DRD5
#   Opioid receptors  : OPRM1, OPRK1, OPRD1, OPRL1
#   Orexin receptors  : HCRTR1, HCRTR2
#   Neuropeptide Y Rs : NPY1R, NPY2R, NPY5R   (15 total = 17 genes; using 15 core)
#
# Foreground lineages (from H6a evidence architecture):
#   - Hummingbird        (Calypte_anna): TAS1R1 positive control - Baldwin 2014
#   - Primate sugar-spec.(Homo + Pan)  : sweet/dopamine receptors
#   - Apidae nectarivore (Apis_mellifera + Bombus_terrestris): sweet pathway proxies
#   - Cetacean sensory   (Tursiops + Orcinus): OPRM1 / umami / sweet loss
#   - Giant panda        (Ailuropoda_melanoleuca): TAS1R1 umami pseudogene (Zhao 2010 control)

DEFAULT_MATRIX_ROWS = [
    # --- POSITIVE CONTROL (must recover Baldwin 2014 signal) ---
    {"gene": "TAS1R1",  "lineage_key": "hummingbird", "fg_type": "tip",
     "fg_label": "Calypte_anna",
     "notes": "POSITIVE_CONTROL Baldwin2014 Science 10.1126/science.1255097"},
    # --- NEGATIVE CONTROL (ancestral mammalian TAS1R1, expected no selection) ---
    {"gene": "TAS1R1",  "lineage_key": "mouse_control", "fg_type": "tip",
     "fg_label": "Mus_musculus",
     "notes": "NEGATIVE_CONTROL background mammalian lineage, expect LRT p>0.10"},
    # --- PANDA UMAMI LOSS (Zhao 2010, expect relaxed / pseudogenisation signal) ---
    {"gene": "TAS1R1",  "lineage_key": "panda", "fg_type": "tip",
     "fg_label": "Ailuropoda_melanoleuca",
     "notes": "Zhao2010 giant panda TAS1R1 pseudogenisation - relaxed constraint"},
    # --- SWEET TASTE in sugar-specialist primates ---
    {"gene": "TAS1R2",  "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": "Primate sugar-specialist foreground"},
    {"gene": "TAS1R3",  "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": "Primate sugar-specialist foreground"},
    # --- Dopamine receptors on primate foreground ---
    {"gene": "DRD1",    "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": "Primate sugar-specialist foreground"},
    {"gene": "DRD2",    "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": "Primate sugar-specialist foreground (Johnson-Kenny 2010 Drd2 mouse rationale)"},
    {"gene": "DRD3",    "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    {"gene": "DRD4",    "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": "DRD4 VNTR literature; allelic length variation"},
    {"gene": "DRD5",    "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    # --- Opioid receptors on primate foreground ---
    {"gene": "OPRM1",   "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    {"gene": "OPRK1",   "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    {"gene": "OPRD1",   "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    {"gene": "OPRL1",   "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    # --- Orexin on primate foreground ---
    {"gene": "HCRTR1",  "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    {"gene": "HCRTR2",  "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    # --- NPY receptors on primate foreground ---
    {"gene": "NPY1R",   "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    {"gene": "NPY2R",   "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    {"gene": "NPY5R",   "lineage_key": "primate_sugar",  "fg_type": "clade",
     "fg_label": "Homo_sapiens|Pan_troglodytes",
     "notes": ""},
    # --- Apidae nectarivore foreground (arthropod homologs; will use
    #     Drosophila/bee-specific orthologs from Ensembl Metazoa; matrix row
    #     retained here for completeness even though gene names differ across
    #     phyla - the alignment must contain the matching arthropod homolog set)
    {"gene": "DRD2",    "lineage_key": "apidae_nectar",  "fg_type": "clade",
     "fg_label": "Apis_mellifera|Bombus_terrestris",
     "notes": "Arthropod DopR1/DopR2 homologs; nectarivore foreground"},
    {"gene": "TAS1R2",  "lineage_key": "apidae_nectar",  "fg_type": "clade",
     "fg_label": "Apis_mellifera|Bombus_terrestris",
     "notes": "Arthropod Gr5a/Gr64 homologs; sweet-sensing nectarivore foreground"},
    # --- Cetacean sensory-specialist foreground ---
    {"gene": "OPRM1",   "lineage_key": "cetacean",       "fg_type": "clade",
     "fg_label": "Tursiops_truncatus|Orcinus_orca",
     "notes": "Cetacean reward pathway; sensory specialisation lineage"},
    {"gene": "TAS1R2",  "lineage_key": "cetacean",       "fg_type": "clade",
     "fg_label": "Tursiops_truncatus|Orcinus_orca",
     "notes": "Cetacean sweet-receptor loss documented (Feng 2014); relaxed constraint"},
]

# ------------------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------------------

def _setup_logging() -> Path:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS_DIR / f"01_prepare_codeml_inputs_{stamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler(sys.stdout)],
    )
    return log_path


def emit_matrix_if_absent() -> pd.DataFrame:
    """Write default test matrix TSV if not present, then read it back."""
    if not MATRIX_TSV.exists():
        df = pd.DataFrame(DEFAULT_MATRIX_ROWS)
        df.to_csv(MATRIX_TSV, sep="\t", index=False)
        logging.info("Emitted default test matrix -> %s (%d rows)", MATRIX_TSV, len(df))
    return pd.read_csv(MATRIX_TSV, sep="\t").fillna("")


def label_foreground_in_tree(tree_text: str, fg_type: str, fg_label: str) -> str:
    """
    Insert PAML "#1" foreground marker into a Newick string.

    fg_type == "tip"   -> suffix the matching terminal taxon with " #1"
    fg_type == "clade" -> use ete3 to find the MRCA of the pipe-separated tips
                          and suffix the internal node with " #1"
    """
    from ete3 import Tree

    tree = Tree(tree_text, format=1)
    if fg_type == "tip":
        leaves = [leaf for leaf in tree.get_leaves() if leaf.name == fg_label]
        if not leaves:
            raise ValueError(f"Tip '{fg_label}' not found in tree")
        leaves[0].name = leaves[0].name + " #1"
    elif fg_type == "clade":
        tip_names = fg_label.split("|")
        present = [t for t in tip_names if tree.search_nodes(name=t)]
        missing = [t for t in tip_names if t not in present]
        if missing:
            logging.warning("Tips missing for clade fg '%s': %s", fg_label, missing)
        if len(present) < 2:
            raise ValueError(
                f"Clade foreground needs >=2 present tips, got {present}"
            )
        mrca = tree.get_common_ancestor(present)
        # ete3 serialises internal labels via .name; assigning to mrca.name
        # places the label at the end of the Newick internal node definition,
        # which codeml parses as the foreground marker.
        mrca.name = "#1"
    else:
        raise ValueError(f"Unknown fg_type: {fg_type}")
    # format=1 preserves internal node names; newline avoided so PAML parses clean
    return tree.write(format=1)


def customise_ctl(template: Path, run_dir: Path, output_name: str) -> None:
    """Copy a ctl template into run_dir, blanking seqfile/treefile/outfile paths
    so that codeml uses the in-directory defaults (alignment.phy, tree_labelled.nwk)."""
    text = template.read_text()
    # The templates already reference alignment.phy / tree_labelled.nwk; we only
    # need to ensure the output filename points into the run dir.
    if output_name == "null.ctl":
        text = text.replace("outfile = null_mlc.out", "outfile = null_mlc.out")
    elif output_name == "alt.ctl":
        text = text.replace("outfile = alt_mlc.out", "outfile = alt_mlc.out")
    (run_dir / output_name).write_text(text)


def fasta_to_phylip(fasta_path: Path, out_path: Path) -> None:
    """Convert FASTA codon alignment to PAML-compatible Phylip sequential."""
    from Bio import SeqIO
    records = list(SeqIO.parse(fasta_path, "fasta"))
    if not records:
        raise ValueError(f"Empty FASTA: {fasta_path}")
    n = len(records)
    aln_len = len(records[0].seq)
    # verify equal length
    for r in records:
        if len(r.seq) != aln_len:
            raise ValueError(
                f"Unequal lengths in {fasta_path}: {r.id} has {len(r.seq)} vs {aln_len}"
            )
    with out_path.open("w") as fh:
        fh.write(f" {n} {aln_len}\n")
        for r in records:
            name = r.id[:30].ljust(30)
            fh.write(f"{name}  {str(r.seq)}\n")


# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------

def prepare_one(row: pd.Series, dry_run: bool = False) -> dict:
    gene = row["gene"]
    lineage_key = row["lineage_key"]
    fg_type = row["fg_type"]
    fg_label = row["fg_label"]
    run_id = f"{gene}__{lineage_key}"
    run_dir = RUNS_DIR / run_id

    aln_src = ALIGN_DIR / f"{gene}_codon.fasta"
    tree_src_primary = TREE_DIR / f"pilot_tree_{gene}.nwk"
    tree_src_fallback = TREE_DIR / "species_tree.nwk"

    result = {
        "run_id": run_id,
        "gene": gene,
        "lineage": lineage_key,
        "aln_present": aln_src.exists(),
        "tree_primary_present": tree_src_primary.exists(),
        "tree_fallback_present": tree_src_fallback.exists(),
        "prepared": False,
        "reason": "",
    }

    if dry_run:
        run_dir.mkdir(parents=True, exist_ok=True)
        result["reason"] = "dry_run_directory_scaffold_only"
        result["prepared"] = True
        return result

    if not aln_src.exists():
        result["reason"] = f"missing alignment: {aln_src}"
        return result

    tree_src = tree_src_primary if tree_src_primary.exists() else tree_src_fallback
    if not tree_src.exists():
        result["reason"] = f"missing tree (tried both {tree_src_primary.name} and {tree_src_fallback.name})"
        return result

    run_dir.mkdir(parents=True, exist_ok=True)
    fasta_to_phylip(aln_src, run_dir / "alignment.phy")

    tree_text = tree_src.read_text().strip()
    labelled = label_foreground_in_tree(tree_text, fg_type, fg_label)
    (run_dir / "tree_labelled.nwk").write_text(labelled + "\n")

    customise_ctl(NULL_CTL_TEMPLATE, run_dir, "null.ctl")
    customise_ctl(ALT_CTL_TEMPLATE, run_dir, "alt.ctl")

    result["prepared"] = True
    result["reason"] = "ok"
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="Emit matrix + scaffold empty run dirs; do not touch "
                         "alignments / trees (use before Part 3 delivers).")
    ap.add_argument("--gene", default=None,
                    help="Restrict to one gene symbol (e.g. TAS1R1).")
    ap.add_argument("--only-control", action="store_true",
                    help="Restrict to POSITIVE_CONTROL rows (hummingbird TAS1R1).")
    args = ap.parse_args()

    log_path = _setup_logging()
    logging.info("Starting 01_prepare_codeml_inputs (dry_run=%s)", args.dry_run)
    logging.info("Log file: %s", log_path)

    if not NULL_CTL_TEMPLATE.exists() or not ALT_CTL_TEMPLATE.exists():
        logging.error("Control file templates missing. Expected %s and %s",
                      NULL_CTL_TEMPLATE, ALT_CTL_TEMPLATE)
        return 2

    matrix = emit_matrix_if_absent()
    if args.gene:
        matrix = matrix[matrix["gene"] == args.gene]
    if args.only_control:
        matrix = matrix[matrix["notes"].str.contains("POSITIVE_CONTROL", na=False)]

    logging.info("Matrix has %d rows after filters", len(matrix))
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    for _, row in matrix.iterrows():
        try:
            r = prepare_one(row, dry_run=args.dry_run)
        except Exception as exc:  # noqa: BLE001
            logging.exception("Failed row %s__%s: %s", row["gene"], row["lineage_key"], exc)
            r = {"run_id": f"{row['gene']}__{row['lineage_key']}",
                 "prepared": False, "reason": f"exception: {exc}"}
        results.append(r)
        logging.info("[%s] %s", "OK " if r["prepared"] else "SKIP",
                     f"{r['run_id']}: {r['reason']}")

    out_summary = LOGS_DIR / "01_prepare_summary.tsv"
    pd.DataFrame(results).to_csv(out_summary, sep="\t", index=False)
    logging.info("Summary written: %s", out_summary)
    n_ok = sum(1 for r in results if r["prepared"])
    logging.info("Prepared %d / %d runs", n_ok, len(results))

    # Non-zero exit if nothing prepared in non-dry-run mode -> pipeline blocked
    if not args.dry_run and n_ok == 0:
        logging.error("No runs prepared. Part 3 alignments and trees are not "
                      "yet available; re-run with --dry-run or wait for Part 3.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
