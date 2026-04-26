#!/usr/bin/env python
"""
positive_control_v2_build.py
============================

Steps 2-3 of the v2 Baldwin 2014 positive-control upgrade.

Build a 9-species TAS1R1 codon alignment (existing 6 + 3 new avians):
  - Danio_rerio (outgroup)
  - Gallus_gallus (non-Apodiformes bird)
  - Homo_sapiens, Mus_musculus, Rattus_norvegicus (mammals)
  - Calypte_anna (hummingbird, Apodiformes)
  - Apus_apus (swift, Apodiformes) [NEW]
  - Taeniopygia_guttata (zebra finch, passerine outgroup) [NEW]
  - Serinus_canaria (canary, passerine outgroup) [NEW]

Pipeline:
  1. Merge CDS from 6 existing species + 3 new avian species
  2. Strip stop codons, trim to in-frame length
  3. Translate to proteins
  4. MAFFT --auto protein alignment
  5. Protein-guided codon back-translation (strict: 1 aa = 1 codon)
  6. IQ-TREE on the protein alignment (MFP, -B 1000)
  7. Write: codon_aligned_v2.fasta, codon_aligned_v2.phy, protein_aln_v2.fasta,
     tree_v2.treefile, species_tree_v2.nwk
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
WORK.mkdir(parents=True, exist_ok=True)

# Existing (6 species) CDS come from the v1 cds_stripped.fasta (already cleaned)
V1_CDS = WORK / "cds_stripped.fasta"

# New avian CDS (raw, need same cleaning as v1)
NEW_CDS_FILES = [
    ("Apus_apus", PC / "Apus_apus_TAS1R1_cds.fasta"),
    ("Taeniopygia_guttata", PC / "Taeniopygia_guttata_TAS1R1_cds.fasta"),
    ("Serinus_canaria", PC / "Serinus_canaria_TAS1R1_cds.fasta"),
]


def short_label(full_id: str) -> str:
    parts = full_id.split("|")
    if len(parts) >= 2:
        return parts[1]
    return full_id


def strip_stop_and_trim_frame(seq: Seq) -> Seq:
    s = str(seq).upper().replace("U", "T")
    extra = len(s) % 3
    if extra:
        s = s[:-extra]
    if len(s) >= 3 and s[-3:] in ("TAA", "TAG", "TGA"):
        s = s[:-3]
    return Seq(s)


def check_internal_stops(seq: Seq) -> int:
    s = str(seq)
    n = 0
    for i in range(0, len(s) - 2, 3):
        if s[i:i+3] in ("TAA", "TAG", "TGA"):
            n += 1
    return n


def main() -> int:
    # ----- 1) Load existing cleaned CDS (6 species) -----
    records = []
    for r in SeqIO.parse(V1_CDS, "fasta"):
        sp = short_label(r.id) if "|" in r.id else r.id
        records.append(SeqRecord(Seq(str(r.seq)), id=sp, description=""))
        print(f"[v1 cds] {sp:25s} len_nt={len(r.seq)} codons={len(r.seq)//3}")

    # ----- 2) Load + clean new avian CDS -----
    for sp, path in NEW_CDS_FILES:
        rec = next(SeqIO.parse(path, "fasta"))
        clean = strip_stop_and_trim_frame(rec.seq)
        n_stop = check_internal_stops(clean)
        print(f"[new cds] {sp:25s} len_nt={len(clean)} codons={len(clean)//3} internal_stops={n_stop} src={path.name}")
        records.append(SeqRecord(clean, id=sp, description=""))

    # Dedupe check
    assert len({r.id for r in records}) == len(records), "Duplicate species labels"
    print(f"[merge] total records = {len(records)}")

    out_cds = WORK / "cds_v2_stripped.fasta"
    SeqIO.write(records, out_cds, "fasta")
    print(f"[write] {out_cds}")

    # ----- 3) Translate proteins -----
    prot_records = []
    for r in records:
        prot = str(r.seq.translate(table=1, to_stop=False))
        # Warn on internal stops
        core = prot.rstrip("*")
        if "*" in core:
            pos = core.index("*")
            print(f"[WARN] internal * in translated {r.id}: first at aa pos {pos}")
        prot = core
        prot_records.append(SeqRecord(Seq(prot), id=r.id, description=""))
        print(f"[prot] {r.id:25s} len_aa={len(prot)} starts_with_M={prot.startswith('M')}")

    prot_in = WORK / "protein_v2_unaligned.fasta"
    SeqIO.write(prot_records, prot_in, "fasta")

    # ----- 4) MAFFT protein alignment -----
    prot_out = WORK / "protein_aln_v2.fasta"
    cmd = ["mafft", "--auto", "--thread", "2", str(prot_in)]
    print(f"[mafft] {' '.join(cmd)}")
    with open(prot_out, "w") as fh:
        proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.PIPE, check=True)
    stderr_tail = proc.stderr.decode().splitlines()[-3:] if proc.stderr else []
    print(f"[mafft] done -> {prot_out}")
    for ln in stderr_tail:
        print(f"[mafft] {ln}")

    # ----- 5) Back-translate (strict protein-guided) -----
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
        codon_str = "".join(codon_seq)
        codon_aln.append(SeqRecord(Seq(codon_str), id=sp, description=""))
        if cursor != len(cds):
            print(f"[WARN] {sp}: cds_len={len(cds)} consumed_nt={cursor} residual={len(cds)-cursor}")

    lengths = {len(r.seq) for r in codon_aln}
    assert len(lengths) == 1, f"Codon-aligned lengths differ: {lengths}"
    L = lengths.pop()
    print(f"[codon-aln] length = {L} nt = {L//3} codons")

    out_codon = WORK / "codon_aligned_v2.fasta"
    SeqIO.write(codon_aln, out_codon, "fasta")
    print(f"[write] {out_codon}")

    # ----- 6) PAML Phylip sequential format -----
    phy_path = WORK / "codon_aligned_v2.phy"
    with open(phy_path, "w") as fh:
        fh.write(f" {len(codon_aln)} {L}\n")
        for r in codon_aln:
            name = r.id[:30].ljust(30)
            fh.write(f"{name}  {str(r.seq)}\n")
    print(f"[phylip] {phy_path}")

    # ----- 7) IQ-TREE on protein alignment -----
    # Use the protein alignment (per task spec Step 3: iqtree -s protein_aln.fasta)
    iq_prefix = WORK / "tree_v2"
    # Clean any existing files for -redo
    cmd = [
        "iqtree",
        "-s", str(prot_out),
        "-m", "MFP",
        "-B", "1000",
        "-nt", "2",
        "-redo",
        "--prefix", str(iq_prefix),
    ]
    print(f"[iqtree] {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("[iqtree] stdout tail:\n", proc.stdout[-1200:])
        print("[iqtree] stderr tail:\n", proc.stderr[-600:])
        raise SystemExit("IQ-TREE failed")
    tree_file = Path(str(iq_prefix) + ".treefile")
    tree_text = tree_file.read_text().strip()
    print(f"[iqtree] tree: {tree_text}")

    # Save a copy as species_tree_v2.nwk for convenience
    (WORK / "species_tree_v2.nwk").write_text(tree_text + "\n")
    print(f"[write] {WORK/'species_tree_v2.nwk'}")

    # Print the .iqtree summary section
    iqtree_log = Path(str(iq_prefix) + ".iqtree")
    if iqtree_log.exists():
        txt = iqtree_log.read_text()
        # Print key sections
        for section_header in ("Best-fit model", "NUMERICAL LIMITS", "TREE SEARCH", "ULTRAFAST BOOTSTRAP"):
            pass
        # Print last ~60 lines
        lines = txt.splitlines()
        print("\n--- iqtree .iqtree summary (tail) ---")
        for ln in lines[-80:]:
            print(ln)

    return 0


if __name__ == "__main__":
    sys.exit(main())
