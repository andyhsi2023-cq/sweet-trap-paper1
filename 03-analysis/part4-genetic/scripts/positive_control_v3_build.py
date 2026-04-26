#!/usr/bin/env python
"""
positive_control_v3_build.py
============================

v3: Drop the truncated Taeniopygia_guttata RefSeq (563aa vs 830aa expected;
41% gap fraction in the v2 alignment) and rebuild the alignment + tree with
8 species:
  Danio_rerio, Gallus_gallus, Homo_sapiens, Mus_musculus, Rattus_norvegicus,
  Calypte_anna, Apus_apus, Serinus_canaria.

Serinus_canaria is a 832aa passerine outgroup (complete). With only Serinus as
the single passerine outgroup, we lose one outgroup taxon but keep a fully
sequenced one that won't skew the alignment via gap columns.

Outputs are written in parallel to the v2 ones:
  codon_aligned_v3.fasta, codon_aligned_v3.phy
  protein_aln_v3.fasta, tree_v3.*, species_tree_v3.nwk
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

V1_CDS = WORK / "cds_stripped.fasta"  # 6 species

NEW_CDS_FILES = [
    ("Apus_apus", PC / "Apus_apus_TAS1R1_cds.fasta"),
    ("Serinus_canaria", PC / "Serinus_canaria_TAS1R1_cds.fasta"),
]


def short_label(full_id: str) -> str:
    parts = full_id.split("|")
    return parts[1] if len(parts) >= 2 else full_id


def strip_stop_and_trim_frame(seq: Seq) -> Seq:
    s = str(seq).upper().replace("U", "T")
    extra = len(s) % 3
    if extra:
        s = s[:-extra]
    if len(s) >= 3 and s[-3:] in ("TAA", "TAG", "TGA"):
        s = s[:-3]
    return Seq(s)


def main() -> int:
    records = []
    for r in SeqIO.parse(V1_CDS, "fasta"):
        sp = short_label(r.id) if "|" in r.id else r.id
        records.append(SeqRecord(Seq(str(r.seq)), id=sp, description=""))
        print(f"[v1 cds] {sp:25s} len_nt={len(r.seq)}")
    for sp, path in NEW_CDS_FILES:
        rec = next(SeqIO.parse(path, "fasta"))
        clean = strip_stop_and_trim_frame(rec.seq)
        records.append(SeqRecord(clean, id=sp, description=""))
        print(f"[new cds] {sp:25s} len_nt={len(clean)}")
    print(f"[merge] total = {len(records)}")

    SeqIO.write(records, WORK / "cds_v3_stripped.fasta", "fasta")

    # Translate
    prot_records = []
    for r in records:
        prot = str(r.seq.translate(table=1, to_stop=False)).rstrip("*")
        if "*" in prot:
            print(f"[WARN] internal * in {r.id}")
        prot_records.append(SeqRecord(Seq(prot), id=r.id, description=""))
        print(f"[prot] {r.id:25s} len_aa={len(prot)}")
    prot_in = WORK / "protein_v3_unaligned.fasta"
    SeqIO.write(prot_records, prot_in, "fasta")

    # MAFFT
    prot_out = WORK / "protein_aln_v3.fasta"
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
    SeqIO.write(codon_aln, WORK / "codon_aligned_v3.fasta", "fasta")

    # Phylip
    phy_path = WORK / "codon_aligned_v3.phy"
    with open(phy_path, "w") as fh:
        fh.write(f" {len(codon_aln)} {L}\n")
        for r in codon_aln:
            name = r.id[:30].ljust(30)
            fh.write(f"{name}  {str(r.seq)}\n")

    # IQ-TREE
    iq_prefix = WORK / "tree_v3"
    cmd = ["iqtree", "-s", str(prot_out), "-m", "MFP", "-B", "1000",
           "-nt", "2", "-redo", "--prefix", str(iq_prefix)]
    print(f"[iqtree] {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("[iqtree] FAIL", proc.stdout[-600:], proc.stderr[-600:])
        raise SystemExit(1)
    tree_text = (Path(str(iq_prefix) + ".treefile")).read_text().strip()
    print(f"[iqtree] {tree_text}")
    (WORK / "species_tree_v3.nwk").write_text(tree_text + "\n")

    # Gap summary
    print("\n[gap summary per species]")
    for r in codon_aln:
        s = str(r.seq)
        g = s.count("-")
        print(f"  {r.id:25s} gap_frac={g/len(s):.2%}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
