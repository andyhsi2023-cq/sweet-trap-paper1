#!/usr/bin/env python
"""
positive_control_v4_build.py
============================

Build the Baldwin-2014-scale TAS1R1 alignment with 15 taxa:
  Mammals (3): Homo_sapiens, Mus_musculus, Rattus_norvegicus
  Fish outgroup: Danio_rerio
  Non-Apodiformes bird: Gallus_gallus
  Passerine outgroup: Serinus_canaria
  Swift (Apodidae): Apus_apus
  Hummingbirds (Trochilidae, 9): Calypte_anna, Amazilia_tzacatl, Patagona_gigas,
    Lophornis_magnificus, Haplophaedia_aureliae, Heliothryx_barroti,
    Ramphodon_naevius, Florisuga_fusca, Heliangelus_exortis

Writes:
  codon_aligned_v4.fasta / .phy
  protein_aln_v4.fasta
  tree_v4.* (IQ-TREE)
  species_tree_v4.nwk
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
PC = ROOT / "data" / "positive_control"
WORK = PC / "work"

# v1 alignment file (6 species, already cleaned)
V1_CDS = WORK / "cds_stripped.fasta"

# New species (all already cleaned by the fetch scripts; just parse and trim)
NEW_CDS = [
    ("Apus_apus",               PC / "Apus_apus_TAS1R1_cds.fasta"),
    ("Serinus_canaria",         PC / "Serinus_canaria_TAS1R1_cds.fasta"),
    ("Heliangelus_exortis",     PC / "Heliangelus_exortis_TAS1R1_cds.fasta"),
    ("Florisuga_fusca",         PC / "Florisuga_fusca_TAS1R1_cds.fasta"),
    ("Ramphodon_naevius",       PC / "Ramphodon_naevius_TAS1R1_cds.fasta"),
    ("Heliothryx_barroti",      PC / "Heliothryx_barroti_TAS1R1_cds.fasta"),
    ("Haplophaedia_aureliae",   PC / "Haplophaedia_aureliae_TAS1R1_cds.fasta"),
    ("Lophornis_magnificus",    PC / "Lophornis_magnificus_TAS1R1_cds.fasta"),
    ("Patagona_gigas",          PC / "Patagona_gigas_TAS1R1_cds.fasta"),
    ("Amazilia_tzacatl",        PC / "Amazilia_tzacatl_TAS1R1_cds.fasta"),
]


def short_label(full_id: str) -> str:
    parts = full_id.split("|")
    return parts[1] if len(parts) >= 2 else full_id


def strip_stop_and_trim(seq: Seq) -> Seq:
    s = str(seq).upper().replace("U", "T")
    if len(s) % 3:
        s = s[:-(len(s) % 3)]
    if s[-3:] in ("TAA", "TAG", "TGA"):
        s = s[:-3]
    return Seq(s)


def main() -> int:
    records = []
    for r in SeqIO.parse(V1_CDS, "fasta"):
        sp = short_label(r.id) if "|" in r.id else r.id
        records.append(SeqRecord(Seq(str(r.seq)), id=sp, description=""))
        print(f"[v1 cds]  {sp:25s} len_nt={len(r.seq)}")
    for sp, path in NEW_CDS:
        rec = next(SeqIO.parse(path, "fasta"))
        clean = strip_stop_and_trim(rec.seq)
        records.append(SeqRecord(clean, id=sp, description=""))
        print(f"[new cds] {sp:25s} len_nt={len(clean)}")

    assert len({r.id for r in records}) == len(records), "Duplicate labels"
    print(f"[merge] total = {len(records)}")

    SeqIO.write(records, WORK / "cds_v4_stripped.fasta", "fasta")

    # Translate
    prot_records = []
    for r in records:
        prot = str(r.seq.translate(table=1, to_stop=False)).rstrip("*")
        if "*" in prot:
            print(f"[WARN] internal * in {r.id} at aa {prot.index('*')}")
        prot_records.append(SeqRecord(Seq(prot), id=r.id, description=""))
        print(f"[prot] {r.id:25s} len_aa={len(prot)}")
    prot_in = WORK / "protein_v4_unaligned.fasta"
    SeqIO.write(prot_records, prot_in, "fasta")

    # MAFFT
    prot_out = WORK / "protein_aln_v4.fasta"
    cmd = ["mafft", "--auto", "--thread", "2", str(prot_in)]
    print(f"[mafft] {' '.join(cmd)}")
    with open(prot_out, "w") as fh:
        subprocess.run(cmd, stdout=fh, stderr=subprocess.PIPE, check=True)

    # Back-translate
    prot_aln = {r.id: str(r.seq) for r in SeqIO.parse(prot_out, "fasta")}
    cds_by_id = {r.id: str(r.seq) for r in records}
    codon_aln = []
    for sp, p in prot_aln.items():
        cds = cds_by_id[sp]
        codon_seq = []
        cursor = 0
        for aa in p:
            if aa == "-":
                codon_seq.append("---")
            else:
                codon = cds[cursor:cursor+3]
                if len(codon) < 3:
                    codon = codon + "N" * (3 - len(codon))
                codon_seq.append(codon)
                cursor += 3
        codon_aln.append(SeqRecord(Seq("".join(codon_seq)), id=sp, description=""))
    L = len(codon_aln[0].seq)
    print(f"[codon-aln] {L} nt = {L//3} codons")
    SeqIO.write(codon_aln, WORK / "codon_aligned_v4.fasta", "fasta")

    phy_path = WORK / "codon_aligned_v4.phy"
    with open(phy_path, "w") as fh:
        fh.write(f" {len(codon_aln)} {L}\n")
        for r in codon_aln:
            name = r.id[:30].ljust(30)
            fh.write(f"{name}  {str(r.seq)}\n")

    # IQ-TREE on protein alignment
    iq_prefix = WORK / "tree_v4"
    cmd = ["iqtree", "-s", str(prot_out), "-m", "MFP", "-B", "1000",
           "-nt", "2", "-redo", "--prefix", str(iq_prefix)]
    print(f"[iqtree] {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("[iqtree] FAIL", proc.stdout[-1000:], proc.stderr[-600:])
        raise SystemExit(1)
    tree_text = (Path(str(iq_prefix) + ".treefile")).read_text().strip()
    print(f"[iqtree] {tree_text}")
    (WORK / "species_tree_v4.nwk").write_text(tree_text + "\n")

    # Print iqtree summary tail
    iqtree_log = Path(str(iq_prefix) + ".iqtree")
    if iqtree_log.exists():
        lines = iqtree_log.read_text().splitlines()
        print("\n--- tree_v4.iqtree summary (ASCII tree) ---")
        in_tree = False
        for ln in lines:
            if "+----" in ln or in_tree:
                print(ln)
                in_tree = True
                if ln.strip() == "":
                    in_tree = False

    print("\n[gap summary per species]")
    for r in codon_aln:
        s = str(r.seq)
        g = s.count("-")
        print(f"  {r.id:25s} gap_frac={g/len(s):.2%}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
