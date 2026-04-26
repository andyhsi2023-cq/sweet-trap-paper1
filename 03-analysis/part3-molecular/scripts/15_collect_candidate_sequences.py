#!/usr/bin/env python3
"""
15_collect_candidate_sequences.py
=================================

Step 3 -> Step 4 bridge for BLASTP reciprocal strategy.

Collects the union of top-5 cnidarian hits (column 2) from the 3 forward
BLASTP result TSVs, fetches their full FASTA from each species' proteome
FASTA, and writes:

    outputs/blast_rbh/cnidarian_forward_hits.faa
    outputs/blast_rbh/cnidarian_forward_hits_manifest.tsv

The manifest records: accession, species, best_forward_anchor, forward_evalue,
forward_bitscore, forward_pident — for downstream reciprocal BLAST processing.
"""
import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
OUT = ROOT / "outputs" / "blast_rbh"
PROT_DIR = ROOT / "data" / "proteomes_cnidarian"

SPECIES_TO_FA = {
    "Hvul": PROT_DIR / "Hydra_vulgaris.protein.faa",
    "Nvec": PROT_DIR / "Nematostella_vectensis.protein.faa",
    "Adig": PROT_DIR / "Acropora_digitifera.protein.faa",
}

FIELDS = ["qseqid","sseqid","pident","length","mismatch","gapopen",
          "qstart","qend","sstart","send","evalue","bitscore","stitle"]


def load_proteome(fa: Path) -> dict:
    """Return dict: first_token_of_header -> full_fasta_record (with '>')."""
    recs = {}
    hdr, seq = None, []
    with fa.open() as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if hdr is not None:
                    acc = hdr[1:].split()[0]  # first whitespace token
                    recs[acc] = hdr + "\n" + "\n".join(seq) + "\n"
                hdr = line
                seq = []
            else:
                seq.append(line)
        if hdr is not None:
            acc = hdr[1:].split()[0]
            recs[acc] = hdr + "\n" + "\n".join(seq) + "\n"
    return recs


def main():
    # Gather all cnidarian hit accessions per species,
    # keeping best anchor evidence per accession.
    species_hits = defaultdict(dict)  # species -> acc -> best_hit_row
    for sp in ("Hvul", "Nvec", "Adig"):
        tsv = OUT / f"forward_DRD_vs_{sp}.tsv"
        with tsv.open() as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                d = dict(zip(FIELDS, row))
                acc = d["sseqid"]
                # keep the hit with the highest bitscore (best forward support)
                prev = species_hits[sp].get(acc)
                if prev is None or float(d["bitscore"]) > float(prev["bitscore"]):
                    species_hits[sp][acc] = d

    # Load proteomes and write candidate FASTA + manifest
    cand_fa = OUT / "cnidarian_forward_hits.faa"
    manifest = OUT / "cnidarian_forward_hits_manifest.tsv"

    n_total = 0
    with cand_fa.open("w") as fa, manifest.open("w", newline="") as m:
        mw = csv.writer(m, delimiter="\t")
        mw.writerow(["cand_id", "species", "accession", "best_forward_anchor",
                     "forward_evalue", "forward_bitscore", "forward_pident",
                     "forward_align_len", "stitle"])

        for sp in ("Hvul", "Nvec", "Adig"):
            proteome = load_proteome(SPECIES_TO_FA[sp])
            for acc, row in species_hits[sp].items():
                if acc not in proteome:
                    print(f"[warn] {acc} not found in {sp} proteome; skipping")
                    continue
                rec = proteome[acc]
                # Re-header to include species tag for downstream clarity
                lines = rec.splitlines()
                hdr = lines[0]
                rest = "\n".join(lines[1:])
                # custom header: >sp_acc|species|... original
                new_hdr = f">{sp}_{acc}|{sp}| " + hdr[1:]
                fa.write(new_hdr + "\n" + rest + "\n")
                mw.writerow([f"{sp}_{acc}", sp, acc, row["qseqid"],
                             row["evalue"], row["bitscore"], row["pident"],
                             row["length"], row["stitle"]])
                n_total += 1

    print(f"[collect] wrote {n_total} candidate sequences -> {cand_fa}")
    print(f"[collect] manifest -> {manifest}")
    # Report unique per species
    for sp in ("Hvul", "Nvec", "Adig"):
        print(f"  {sp}: {len(species_hits[sp])} unique accessions across all anchor queries")


if __name__ == "__main__":
    main()
