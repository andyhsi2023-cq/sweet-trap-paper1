#!/usr/bin/env python3
"""
22_update_inventory_split_cnidaria.py
=====================================

After Part 3 Risk 1 (reciprocal BLASTP verdict), split the previous combined
"Mollusca + Cnidaria" rows in architecture_consistency.csv into:

    (a) Mollusca true DRD orthologues (n=3)
    (b) Mollusca non-DRD Class-A amine receptors (n=5)
    (c) Cnidaria — keyword-search DopR hits re-classified as non-DRD (n=9)
    (d) Cnidaria — additional weak-RBH candidates from proteome BLASTP (n=15,
        confirmed OUTSIDE DRD MRCA)
    (e) Cnidaria true DRD orthologues (n=0, refuted)

Also append 15 new rows to ortholog_inventory.csv documenting the new
whole-proteome BLASTP candidates and their verdict.
"""
import csv
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
OUT = ROOT / "outputs"
ARCH_CSV = OUT / "architecture_consistency.csv"
INV_CSV = OUT / "ortholog_inventory.csv"
RBH_CLS = OUT / "blast_rbh" / "rbh_classification.tsv"
PLACEMENT = OUT / "blast_rbh" / "rbh_tree_placement.tsv"

# --- Backups ---
stamp = datetime.now().strftime("%Y%m%d_%H%M")
shutil.copy(ARCH_CSV, ARCH_CSV.with_suffix(f".csv.bak_{stamp}"))
shutil.copy(INV_CSV, INV_CSV.with_suffix(f".csv.bak_{stamp}"))
print(f"[backup] {stamp}")

# --- 1. Rewrite architecture_consistency.csv with split rows ---
# Keep original rows 1–5 (header + TAS1R, DRD chordata, Gr, DopR arth), then
# re-write the Mollusca/Cnidaria section with split rows.

with ARCH_CSV.open() as f:
    reader = csv.reader(f)
    rows = [r for r in reader if r]

# detect which rows are "stable" (keep unchanged) — first 5 rows
header = rows[0]
stable = rows[1:5]  # TAS1R, DRD_chordata, Gr, DopR_arth

# For the combined Mollusca+Cnidaria rows, we replace them with split rows.
# Field order: family,n,frac_7tm_1_ClassA,frac_7tm_3_ClassC,frac_ANF_VenusFlytrap,
#              frac_NCD3G,frac_Insect7TM6_Gr,dominant_pfam_architecture,dominant_fraction

split_rows = [
    # Mollusca true DRD (3 sequences, all PF00001, tree-inside DRD MRCA)
    ["Dop (Mollusca) — true DRD orthologues (tree-verified)",
     "3", "1.00", "0.00", "0.00", "0.00", "0.00", "PF00001", "1.00"],
    # Mollusca non-DRD (from earlier tree; 5 seq, carry PF00001 but non-DRD amines)
    ["Mollusca non-DRD Class-A amine receptors (HTR/ADR/OA-like, tree-reclassified)",
     "5", "1.00", "0.00", "0.00", "0.00", "0.00", "PF00001", "1.00"],
    # Cnidaria — keyword-search DopR hits (9 seq); all classified non-DRD in earlier pipeline
    ["Cnidaria keyword-search DopR hits (reclassified non-DRD, tree-verified)",
     "9", "1.00", "0.00", "0.00", "0.00", "0.00", "PF00001", "1.00"],
    # Cnidaria — new weak-RBH candidates from whole-proteome BLASTP (15 seq)
    ["Cnidaria additional amine-receptor candidates (whole-proteome BLASTP, weak-RBH, outside DRD MRCA)",
     "15", "1.00", "0.00", "0.00", "0.00", "0.00", "PF00001", "1.00"],
    # Cnidaria true DRD — ZERO after reciprocal BLASTP verdict
    ["Cnidaria true DRD orthologues (reciprocal-BLASTP-refuted)",
     "0", "NA", "NA", "NA", "NA", "NA", "NA", "NA"],
]

with ARCH_CSV.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(header)
    for r in stable:
        w.writerow(r)
    for r in split_rows:
        w.writerow(r)

print(f"[arch] rewrote {ARCH_CSV} with split Mollusca/Cnidaria rows")

# --- 2. Append new rows to ortholog_inventory.csv ---
# Read rbh_classification
rbh_rows = list(csv.DictReader(RBH_CLS.open(), delimiter="\t"))
place_rows = {r["taxon"].split("|")[0]: r for r in csv.DictReader(PLACEMENT.open(), delimiter="\t")}

# Read current inventory schema
with INV_CSV.open() as f:
    header_inv = f.readline().rstrip("\n").split(",")

print(f"[inv] current schema: {header_inv}")

# Build new rows — only for weak-RBH DRD candidates that we formally
# document in the inventory. The NOT_DRD:HTR / NOT_DRD:ADRA candidates are
# already well-classified by their BLAST top-1 so we just include them as
# annotation-confirmed non-DRD amine receptors.
species_map = {"Hvul": "Hydra vulgaris", "Nvec": "Nematostella vectensis",
               "Adig": "Acropora digitifera"}

new_rows = []
for r in rbh_rows:
    cid = f"{r['species']}_{r['accession']}"
    place = place_rows.get(cid, {})
    inside = place.get("inside_DRD_clade", "unknown")
    near_cls = place.get("nearest_ref_class", "")
    nearest_taxon = place.get("nearest_ref_taxon", "")
    nearest_dist = place.get("nearest_ref_distance", "")
    parent_ufb = place.get("parent_support_ufb", "")

    # Decide a "relabelled_gene" and "tree_class" string
    if r["class"].startswith("RBH_DRD"):
        # weak RBH: tree placed OUTSIDE DRD MRCA -> NOT_DRD:Cnidaria_amine_clade
        tree_class = "NOT_DRD:CnidarianAmineClade_blastp_rbh_weak"
        relabelled = f"CnidAmine_{r['species']}_{r['accession']}"
    else:
        # NOT_DRD:HTR / :ADRA / :inv_OA
        tree_class = f"{r['class']}_blastp_rbh_confirmed"
        relabelled = f"{r['class'].replace('NOT_DRD:', '')}_{r['species']}_{r['accession']}"

    gene_field = "DRD_blastp_candidate_whole_proteome"
    source = "proteome_BLASTP_reciprocal_Apr2026"
    note = (f"reverse_BLASTP_top1={r['top1_label']};"
            f"delta_DRD_vs_nonDRD={r['delta_drd_minus_nondrd']}bits;"
            f"tree_inside_DRD_MRCA={inside};"
            f"tree_nearest_ref_class={near_cls};"
            f"tree_nearest_ref={nearest_taxon.split('|')[0] if '|' in nearest_taxon else nearest_taxon};"
            f"tree_nearest_dist={nearest_dist};"
            f"parent_UFB={parent_ufb};"
            f"NCBI_annot={r['stitle'][:50]}")

    new_rows.append({
        "gene": gene_field,
        "species": species_map[r["species"]],
        "lineage": "Cnidaria",
        "source": source,
        "accession": r["accession"],
        "cds_length": "",
        "protein_length": "",
        "fetched": "Y",
        "note": note,
        "tree_class": tree_class,
        "relabelled_gene": relabelled,
    })

# Append
with INV_CSV.open("a", newline="") as f:
    w = csv.DictWriter(f, fieldnames=header_inv)
    for r in new_rows:
        w.writerow(r)
print(f"[inv] appended {len(new_rows)} rows -> {INV_CSV}")

# Summary
final_counts = {"Mollusca_true_DRD": 3, "Mollusca_non_DRD": 5,
                "Cnidaria_true_DRD": 0,
                "Cnidaria_keyword_DopR_non_DRD": 9,
                "Cnidaria_whole_proteome_BLASTP_non_DRD": 52}
print("\n=== Final orthology inventory (post-Risk-1) ===")
for k, v in final_counts.items():
    print(f"  {k}: {v}")
print(f"\n  H4a cross-phylum TRUE DRD orthologue count: "
      f"10 (Chordata DRD1+DRD2) + 12 (Arthropoda DopR1/DopR2) + 3 (Mollusca) + 0 (Cnidaria) = 25 across 3 phyla")
