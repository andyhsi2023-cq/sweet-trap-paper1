#!/usr/bin/env python3
"""
01b_patch_known_aliases.py
==========================

Curated patches for cases where NCBI's gene-name index is mis-aliased
and the automated fetcher lands on the wrong accession.

Known issue: NCBI indexes "Gr5a" as a synonym of Gr64a (gene_uid 44873) for
Drosophila melanogaster, so a strict [Gene Name] search for Gr5a returns the
wrong gene. The real Gr5a is gene_uid 43250, RefSeq NM_143267.3.

This script overwrites incorrect FASTA files for known alias collisions and
updates the inventory CSV. Safe to re-run.
"""

from __future__ import annotations

import csv
import logging
import re
import sys
import time
from pathlib import Path

from Bio import Entrez, SeqIO

PROJECT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
RAW_CDS = PROJECT / "data" / "raw_cds"
RAW_PROT = PROJECT / "data" / "raw_protein"
INV = PROJECT / "outputs" / "ortholog_inventory.csv"

Entrez.email = "26708155@alu.cqu.edu.cn"
NCBI_SLEEP = 0.34

# Manual curation — verified accessions (PI should vet these)
# Sources: FlyBase for Drosophila; NCBI Gene records (2026-04-24)
PATCHES = [
    # (gene_label, species, true_nuccore_accession, source_note)
    ("Gr5a", "Drosophila melanogaster", "NM_143267.3",
     "FlyBase CG31445; gene_uid=43250; NCBI alias collision with Gr64a"),
]


def fetch_genbank(acc: str) -> tuple[str | None, str | None, str | None]:
    try:
        h = Entrez.efetch(db="nuccore", id=acc, rettype="gb", retmode="text")
        rec = SeqIO.read(h, "genbank"); h.close()
        time.sleep(NCBI_SLEEP)
    except Exception as exc:
        print(f"  efetch failed for {acc}: {exc}", file=sys.stderr)
        return None, None, None
    cds_feats = [f for f in rec.features if f.type == "CDS"]
    if not cds_feats:
        return None, None, None
    f = cds_feats[0]
    cds = str(f.extract(rec.seq))
    prot_acc = f.qualifiers.get("protein_id", [None])[0]
    prot_seq = f.qualifiers.get("translation", [None])[0]
    if prot_seq:
        prot_seq = prot_seq.replace(" ", "").replace("\n", "")
    return cds, prot_seq, prot_acc


def species_short(name: str) -> str:
    parts = name.replace(" ", "_").split("_")
    return (parts[0][0] + parts[1]).lower()


def write_fasta(path: Path, header: str, seq: str) -> None:
    with path.open("w") as fh:
        fh.write(f">{header}\n")
        for i in range(0, len(seq), 60):
            fh.write(seq[i:i+60] + "\n")


def main() -> int:
    # Load inventory
    with INV.open() as fh:
        rows = list(csv.DictReader(fh))

    for gene, species, acc, note in PATCHES:
        print(f"[patch] {gene} / {species} -> {acc}")
        cds, prot, pacc = fetch_genbank(acc)
        if not cds or not prot:
            print(f"  FAILED to fetch {acc}; skipping patch")
            continue
        short = species_short(species)
        cds_path = RAW_CDS / f"{gene}_{short}.fa"
        prot_path = RAW_PROT / f"{gene}_{short}.fa"
        header = f"{gene}|{species.replace(' ','_')}|{acc}"
        write_fasta(cds_path, header, cds)
        write_fasta(prot_path, header, prot)
        print(f"  wrote {cds_path.name} (CDS {len(cds)}, AA {len(prot)})")
        # Update inventory row
        patched = False
        for r in rows:
            if r["gene"] == gene and r["species"] == species:
                r["accession"] = acc
                r["cds_length"] = str(len(cds))
                r["protein_length"] = str(len(prot))
                r["fetched"] = "Y"
                r["source"] = "NCBI Entrez (manual curation)"
                r["note"] = f"{note}; protein={pacc or '-'}"
                patched = True
                break
        if not patched:
            # append new row
            rows.append(dict(
                gene=gene, species=species, lineage="Arthropoda",
                source="NCBI Entrez (manual curation)", accession=acc,
                cds_length=str(len(cds)), protein_length=str(len(prot)),
                fetched="Y",
                note=f"{note}; protein={pacc or '-'}",
            ))

    with INV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"inventory updated -> {INV}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
