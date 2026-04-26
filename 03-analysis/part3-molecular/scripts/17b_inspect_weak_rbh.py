#!/usr/bin/env python3
"""
17b_inspect_weak_rbh.py
=======================

For each RBH_DRD_weak candidate, show top-5 reverse hits so we can see
whether the "near-tie" is between DRD vs HTR, DRD vs ADRB, or DRD vs OA.
This tells us what the candidate is actually most similar to.
"""
import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
OUT  = ROOT / "outputs" / "blast_rbh"

FIELDS = ["qseqid","sseqid","pident","length","mismatch","gapopen",
          "qstart","qend","sstart","send","evalue","bitscore","stitle"]

FAM_MAP = {
    "HUMAN_DRD1": "DRD", "HUMAN_DRD2": "DRD", "HUMAN_DRD3": "DRD",
    "HUMAN_DRD4": "DRD", "HUMAN_DRD5": "DRD",
    "HUMAN_HTR1A": "HTR", "HUMAN_HTR1B": "HTR", "HUMAN_HTR2A": "HTR",
    "HUMAN_HTR2B": "HTR", "HUMAN_HTR4": "HTR", "HUMAN_HTR6": "HTR",
    "HUMAN_HTR7": "HTR",
    "HUMAN_ADRB1": "ADRB", "HUMAN_ADRB2": "ADRB", "HUMAN_ADRB3": "ADRB",
    "HUMAN_ADRA1A": "ADRA", "HUMAN_ADRA2A": "ADRA",
    "DMEL_DOP1R1": "inv_DRD", "DMEL_DOP2R": "inv_DRD",
    "DMEL_OCTB2R": "inv_OA",
}


def load_reverse(path: Path):
    by_cand = defaultdict(list)
    with path.open() as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            d = dict(zip(FIELDS, parts))
            d["bitscore_f"] = float(d["bitscore"])
            by_cand[d["qseqid"].split("|", 1)[0]].append(d)
    for cid in by_cand:
        by_cand[cid].sort(key=lambda x: x["bitscore_f"], reverse=True)
    return by_cand


def load_classification(path: Path):
    rows = {}
    with path.open() as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            rows[row["cand_id"]] = row
    return rows


def main():
    rev = load_reverse(OUT / "reverse_cnidaria_vs_human.tsv")
    cls = load_classification(OUT / "rbh_classification.tsv")

    out = OUT / "rbh_weak_top5_detail.tsv"
    with out.open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["cand_id","species","accession","ncbi_desc","call",
                    "rank","hit_label","hit_family","bitscore","evalue","pident"])
        for cid, row in cls.items():
            if not row["class"].startswith("RBH_DRD"):
                continue
            hits = rev.get(cid, [])[:5]
            for i, h in enumerate(hits, 1):
                lab = h["sseqid"].split("|", 1)[0]
                fam = FAM_MAP.get(lab, "UNK")
                # strip verbose ncbi desc
                desc = row["stitle"]
                if len(desc) > 70:
                    desc = desc[:70] + "..."
                w.writerow([cid, row["species"], row["accession"], desc,
                            row["class"], i, lab, fam, h["bitscore"], h["evalue"], h["pident"]])

    print(f"[inspect] -> {out}")

    # Also print to stdout in readable form
    with out.open() as f:
        for line in f:
            print(line.rstrip())


if __name__ == "__main__":
    main()
