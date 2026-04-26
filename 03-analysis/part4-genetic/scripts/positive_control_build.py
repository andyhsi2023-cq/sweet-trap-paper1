#!/usr/bin/env python
"""
positive_control_build.py
=========================

Build the Baldwin-2014-style TAS1R1 positive-control alignment and tree.

Steps
-----
1. Read Part 3 TAS1R1 CDS (5 species: Danio, Gallus, Homo, Mus, Rattus).
2. Merge Calypte_anna TAS1R1 CDS fetched from NCBI (XM_030463417.1).
3. Strip stop codons, ensure in-frame.
4. Relabel records to short species names (e.g. 'Calypte_anna', 'Mus_musculus').
5. Translate proteins -> mafft --auto protein alignment.
6. Back-translate to codon alignment (protein-guided, strict).
7. IQ-TREE ML on codon alignment (GTR+G) -> labelled Newick.
8. Write outputs to data/positive_control/work/:
     - cds_stripped.fasta
     - protein_unaligned.fasta
     - protein_aligned.fasta
     - codon_aligned.fasta
     - codon_aligned.phy         (PAML Phylip sequential)
     - species_tree.nwk          (with short species labels)

Foreground labelling + codeml runs are handled by a separate driver.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
WORK = ROOT / "data" / "positive_control" / "work"
WORK.mkdir(parents=True, exist_ok=True)

PART3_CDS = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular/data/alignments/TAS1R1_input_cds.fasta")
CALYPTE_CDS = ROOT / "data" / "positive_control" / "Calypte_anna_TAS1R1_cds.fasta"


def short_label(full_id: str) -> str:
    """TAS1R1|Mus_musculus|ENS... -> Mus_musculus
       TAS1R1|Calypte_anna|XM... -> Calypte_anna"""
    parts = full_id.split("|")
    if len(parts) >= 2:
        return parts[1]
    return full_id


def strip_stop_and_trim_frame(seq: Seq) -> Seq:
    """Trim to in-frame length; remove terminal stop codon TAA/TAG/TGA if present."""
    s = str(seq).upper().replace("U", "T")
    # Trim to multiple of 3
    extra = len(s) % 3
    if extra:
        s = s[:-extra]
    # Remove terminal stop
    if len(s) >= 3 and s[-3:] in ("TAA", "TAG", "TGA"):
        s = s[:-3]
    return Seq(s)


def check_internal_stops(seq: Seq, name: str) -> int:
    """Return count of internal stop codons."""
    s = str(seq)
    n_stop = 0
    for i in range(0, len(s) - 2, 3):
        codon = s[i:i+3]
        if codon in ("TAA", "TAG", "TGA"):
            n_stop += 1
    return n_stop


def main() -> int:
    # ----- 1) Load & merge CDS -----
    records = []
    for path in (PART3_CDS, CALYPTE_CDS):
        for r in SeqIO.parse(path, "fasta"):
            sp = short_label(r.id)
            # Special-case Gallus (starts with ACG not ATG — upstream truncation
            # in the Ensembl record). Keep as-is; mafft aligns on protein, so a
            # partial N-terminus just shows up as a leading gap. We still need
            # an integer codon count.
            clean = strip_stop_and_trim_frame(r.seq)
            n_stop = check_internal_stops(clean, sp)
            print(f"[cds] {sp:20s} len(nt)={len(clean)}  codons={len(clean)//3}  internal_stops={n_stop}  src={path.name}")
            records.append(SeqRecord(clean, id=sp, description=""))
    assert len({r.id for r in records}) == len(records), "Duplicate species labels"
    assert any(r.id == "Calypte_anna" for r in records), "Calypte_anna not in merged set"
    SeqIO.write(records, WORK / "cds_stripped.fasta", "fasta")
    print(f"[write] {WORK/'cds_stripped.fasta'} ({len(records)} seqs)")

    # ----- 2) Translate -----
    prot_records = []
    for r in records:
        # table=1 standard; warn if any internal stops (there shouldn't be after stripping)
        prot = str(r.seq.translate(table=1, to_stop=False))
        if "*" in prot[:-1]:  # any stop before last residue
            print(f"[WARN] internal * in translated {r.id}: first at pos {prot.index('*')}")
        # Remove trailing stop if any
        prot = prot.rstrip("*")
        prot_records.append(SeqRecord(Seq(prot), id=r.id, description=""))
        print(f"[prot] {r.id:20s} len(aa)={len(prot)}  starts_with_M={prot.startswith('M')}")
    SeqIO.write(prot_records, WORK / "protein_unaligned.fasta", "fasta")

    # ----- 3) mafft protein alignment -----
    prot_in = WORK / "protein_unaligned.fasta"
    prot_out = WORK / "protein_aligned.fasta"
    cmd = ["mafft", "--auto", "--thread", "2", str(prot_in)]
    print(f"[mafft] {' '.join(cmd)}")
    with open(prot_out, "w") as fh:
        proc = subprocess.run(cmd, stdout=fh, stderr=subprocess.PIPE, check=True)
    print(f"[mafft] done -> {prot_out}; stderr tail: {proc.stderr.decode().splitlines()[-1] if proc.stderr else ''}")

    # ----- 4) Back-translate -----
    prot_aln = {r.id: str(r.seq) for r in SeqIO.parse(prot_out, "fasta")}
    cds_by_id = {r.id: str(r.seq) for r in records}
    codon_aln = []
    for sp, p in prot_aln.items():
        cds = cds_by_id[sp]
        # Walk protein-aligned sequence; each non-gap aa consumes one codon
        codon_seq = []
        cursor = 0
        for aa in p:
            if aa == "-":
                codon_seq.append("---")
            else:
                codon = cds[cursor:cursor+3]
                if len(codon) < 3:
                    # Pad (shouldn't happen if frame is right)
                    codon = codon + "N" * (3 - len(codon))
                codon_seq.append(codon)
                cursor += 3
        codon_str = "".join(codon_seq)
        codon_aln.append(SeqRecord(Seq(codon_str), id=sp, description=""))
        # consistency: cursor should equal len(cds) minus any trailing aa beyond protein
        if cursor != len(cds):
            print(f"[WARN] {sp}: cds_len={len(cds)} but consumed_codons_nt={cursor}  (residual={len(cds)-cursor})")
    # All codon-aligned should now be same length
    L = {len(r.seq) for r in codon_aln}
    assert len(L) == 1, f"Codon-aligned lengths differ: {L}"
    print(f"[codon-aln] length = {L.pop()} nt")
    SeqIO.write(codon_aln, WORK / "codon_aligned.fasta", "fasta")

    # ----- 5) Write PAML Phylip (sequential) -----
    phy_path = WORK / "codon_aligned.phy"
    with open(phy_path, "w") as fh:
        fh.write(f" {len(codon_aln)} {len(codon_aln[0].seq)}\n")
        for r in codon_aln:
            name = r.id[:30].ljust(30)
            fh.write(f"{name}  {str(r.seq)}\n")
    print(f"[phylip] {phy_path}")

    # ----- 6) IQ-TREE ML -----
    iq_prefix = WORK / "iqtree_run"
    cmd = [
        "iqtree", "-s", str(WORK / "codon_aligned.fasta"),
        "-st", "CODON", "-m", "GY", "-B", "1000",
        "-nt", "2", "-redo", "-pre", str(iq_prefix)
    ]
    print(f"[iqtree] {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("[iqtree] FAILED with GY; retrying simpler GTR on nt ...")
        cmd2 = [
            "iqtree", "-s", str(WORK / "codon_aligned.fasta"),
            "-m", "GTR+G", "-B", "1000",
            "-nt", "2", "-redo", "-pre", str(iq_prefix)
        ]
        print(f"[iqtree-retry] {' '.join(cmd2)}")
        proc = subprocess.run(cmd2, capture_output=True, text=True, check=True)
    tree_file = Path(str(iq_prefix) + ".treefile")
    if not tree_file.exists():
        print("[iqtree] stdout tail:\n", proc.stdout[-600:])
        print("[iqtree] stderr tail:\n", proc.stderr[-600:])
        raise SystemExit("IQ-TREE did not produce .treefile")
    tree_text = tree_file.read_text().strip()
    print(f"[iqtree] tree: {tree_text}")
    (WORK / "species_tree.nwk").write_text(tree_text + "\n")
    print(f"[write] {WORK/'species_tree.nwk'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
