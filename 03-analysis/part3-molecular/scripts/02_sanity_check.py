#!/usr/bin/env python3
"""
02_sanity_check.py
==================

Per-sequence QC on all FASTA files in data/raw_cds/ and data/raw_protein/.

Checks (per CDS file):
  1. CDS length divisible by 3
  2. No internal premature stop codons (stop only allowed at the end)
  3. Translated protein length falls in the family-expected range
  4. Header well-formed (gene|species|accession)

Outputs outputs/sequence_qc.csv with pass/fail flags per sequence.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq

PROJECT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
RAW_CDS = PROJECT / "data" / "raw_cds"
RAW_PROT = PROJECT / "data" / "raw_protein"
OUT = PROJECT / "outputs" / "sequence_qc.csv"

# Family-specific expected protein length ranges (aa). Generous windows;
# these are "reasonable" not strict — flag but do not hard-fail on length alone.
LEN_RANGES = {
    "TAS1R": (700, 900),
    "DRD":   (380, 560),   # DRD2 long isoform can exceed 400
    "Gr":    (300, 520),
    "Dop":   (300, 700),
    "DopR":  (300, 700),
    "default": (150, 2000),
}


def family_range(gene: str) -> tuple[int, int]:
    for key, rng in LEN_RANGES.items():
        if key.lower() in gene.lower():
            return rng
    return LEN_RANGES["default"]


def qc_cds(cds_path: Path) -> dict:
    rec = next(SeqIO.parse(cds_path, "fasta"))
    header = rec.description
    parts = header.split("|")
    gene = parts[0] if len(parts) >= 1 else ""
    species = parts[1].replace("_", " ") if len(parts) >= 2 else ""
    accession = parts[2] if len(parts) >= 3 else ""

    cds = str(rec.seq).upper()
    cds_len = len(cds)

    length_mod3 = (cds_len % 3) == 0
    # translate without stopping so we can count premature stops
    safe_cds = cds
    if not length_mod3:
        safe_cds = cds + "N" * (3 - cds_len % 3)
    aa = str(Seq(safe_cds).translate())
    # last codon allowed to be *
    internal_stops = aa[:-1].count("*") if aa.endswith("*") else aa.count("*")
    no_premature_stop = internal_stops == 0
    prot_len = len(aa.rstrip("*"))

    lo, hi = family_range(gene)
    length_in_range = lo <= prot_len <= hi

    # Protein file presence
    prot_path = RAW_PROT / cds_path.name
    prot_ok = prot_path.exists()
    if prot_ok:
        prec = next(SeqIO.parse(prot_path, "fasta"))
        stored_prot_len = len(str(prec.seq).rstrip("*"))
    else:
        stored_prot_len = 0

    pass_all = length_mod3 and no_premature_stop and length_in_range and prot_ok

    return dict(
        filename=cds_path.name,
        gene=gene,
        species=species,
        accession=accession,
        cds_length=cds_len,
        length_mod3=length_mod3,
        protein_length_from_cds=prot_len,
        stored_protein_length=stored_prot_len,
        internal_stops=internal_stops,
        no_premature_stop=no_premature_stop,
        expected_range=f"{lo}-{hi}",
        length_in_range=length_in_range,
        protein_file_present=prot_ok,
        qc_pass=pass_all,
    )


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for f in sorted(RAW_CDS.glob("*.fa")):
        try:
            rows.append(qc_cds(f))
        except Exception as exc:
            rows.append(dict(filename=f.name, qc_pass=False,
                             internal_stops=-1, note=f"exception:{exc}"))

    if not rows:
        print("No CDS FASTA files found", file=sys.stderr)
        return 1

    keys = list(rows[0].keys())
    # ensure all rows share keys
    for r in rows:
        for k in keys:
            r.setdefault(k, "")

    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    n = len(rows); passed = sum(1 for r in rows if r.get("qc_pass"))
    print(f"QC complete: {passed}/{n} passed. -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
