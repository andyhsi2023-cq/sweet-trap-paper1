#!/usr/bin/env python
"""
positive_control_v2_fetch.py
============================

Step 1 of the v2 Baldwin 2014 positive-control upgrade.

Fetch 3 additional avian TAS1R1 CDS from NCBI:
- Apus apus (Gene ID 127392763) — common swift, sister to hummingbirds
- Taeniopygia guttata (Gene ID 115498064) — zebra finch, passerine outgroup
- Serinus canaria (Gene ID 103820937) — canary, passerine outgroup

For each species:
1. efetch gene XML -> parse RefSeq mRNA accession
2. efetch nuccore to get CDS FASTA
3. Verify length % 3 == 0 and no premature stops
4. Write cleaned CDS to data/positive_control/<Species>_TAS1R1_cds.fasta

Output convention matches existing Calypte_anna_TAS1R1_cds.fasta:
    >TAS1R1|<Species_name>|<Accession>
    <sequence ...>
"""
from __future__ import annotations
import sys
import time
import re
from pathlib import Path
from Bio import Entrez, SeqIO
from Bio.Seq import Seq

Entrez.email = "26708155@alu.cqu.edu.cn"

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
PC_DIR = ROOT / "data" / "positive_control"
PC_DIR.mkdir(parents=True, exist_ok=True)

SPECIES = [
    # (species_name, gene_id)
    ("Apus_apus", "127392763"),
    ("Taeniopygia_guttata", "115498064"),
    ("Serinus_canaria", "103820937"),
]


def fetch_refseq_for_gene(gene_id: str) -> list[str]:
    """Return candidate RefSeq mRNA accessions for a given NCBI Gene ID."""
    # elink from gene -> nuccore (mRNA entries)
    handle = Entrez.elink(dbfrom="gene", db="nuccore", id=gene_id,
                          linkname="gene_nuccore_refseqrna")
    rec = Entrez.read(handle)
    handle.close()
    uids = []
    for linkset in rec:
        for ldb in linkset.get("LinkSetDb", []):
            if ldb.get("LinkName") == "gene_nuccore_refseqrna":
                uids.extend(l["Id"] for l in ldb.get("Link", []))
    if not uids:
        # Fallback: try generic gene_nuccore link, filter for XM_ later
        handle = Entrez.elink(dbfrom="gene", db="nuccore", id=gene_id)
        rec = Entrez.read(handle)
        handle.close()
        for linkset in rec:
            for ldb in linkset.get("LinkSetDb", []):
                uids.extend(l["Id"] for l in ldb.get("Link", []))
    return uids


def fetch_accession_from_uid(uid: str) -> tuple[str, str]:
    """Return (accession, title) for a given nuccore UID."""
    handle = Entrez.esummary(db="nuccore", id=uid)
    rec = Entrez.read(handle)
    handle.close()
    acc = rec[0].get("AccessionVersion", rec[0].get("Caption", ""))
    title = rec[0].get("Title", "")
    return acc, title


def fetch_cds_from_mrna(accession: str) -> tuple[str, str]:
    """Fetch the annotated CDS (nt) from an mRNA RefSeq record.

    Returns (cds_nt, protein_id). We use rettype='gb' and pull the CDS feature's
    /translation and the underlying sequence slice, to be robust to mRNAs with
    UTR flanking regions.
    """
    handle = Entrez.efetch(db="nuccore", id=accession, rettype="gb", retmode="text")
    gb_text = handle.read()
    handle.close()

    # Parse Genbank
    from io import StringIO
    rec = SeqIO.read(StringIO(gb_text), "genbank")
    seq_full = str(rec.seq).upper()

    # Find CDS feature
    cds_feat = None
    for feat in rec.features:
        if feat.type == "CDS":
            cds_feat = feat
            break
    if cds_feat is None:
        raise ValueError(f"No CDS feature in {accession}")

    # Extract CDS nucleotide sequence (respecting joins, but for mRNAs this is typically one span)
    cds_nt = str(cds_feat.extract(rec.seq)).upper()
    protein_id = cds_feat.qualifiers.get("protein_id", ["?"])[0]
    return cds_nt, protein_id


def verify_cds(cds_nt: str, species: str) -> tuple[bool, str]:
    """Check length mod 3 and absence of premature stops. Returns (ok, msg)."""
    if len(cds_nt) % 3 != 0:
        return False, f"length={len(cds_nt)} not divisible by 3"
    # Translate strictly
    prot = str(Seq(cds_nt).translate(table=1, to_stop=False))
    # Last residue may or may not be *; trim and check interior
    core = prot.rstrip("*")
    if "*" in core:
        # premature stop
        pos = core.index("*")
        return False, f"premature stop at aa pos {pos} (codon {pos*3}-{pos*3+2})"
    return True, f"len_nt={len(cds_nt)} aa={len(core)}"


def main() -> int:
    results = []
    for species, gene_id in SPECIES:
        print(f"\n=== {species} (Gene ID {gene_id}) ===")

        # 1. Enumerate mRNA UIDs
        uids = fetch_refseq_for_gene(gene_id)
        print(f"  {len(uids)} nuccore UIDs linked")
        time.sleep(0.34)

        # 2. Resolve to accessions; pick XM_* (predicted mRNA) or NM_* (validated)
        candidates = []
        for uid in uids[:20]:  # safety cap
            acc, title = fetch_accession_from_uid(uid)
            if acc.startswith(("XM_", "NM_")):
                candidates.append((acc, title))
            time.sleep(0.34)

        if not candidates:
            print(f"  [FAIL] No XM_/NM_ mRNA accessions found.")
            results.append((species, None, None, "no mRNA"))
            continue

        # Prefer NM_ over XM_; among same-type, prefer the longest title (usually most recent)
        candidates.sort(key=lambda x: (not x[0].startswith("NM_"), x[0]))
        print("  candidate accessions:")
        for acc, title in candidates[:5]:
            print(f"    {acc}  {title[:80]}")

        # 3. Iterate candidates, take the first that yields a clean in-frame CDS
        chosen = None
        last_msg = ""
        for acc, title in candidates:
            try:
                cds_nt, prot_id = fetch_cds_from_mrna(acc)
                ok, msg = verify_cds(cds_nt, species)
                print(f"  try {acc}: {'OK' if ok else 'FAIL'} — {msg}  (protein {prot_id})")
                if ok:
                    chosen = (acc, cds_nt, prot_id, msg)
                    break
                else:
                    last_msg = msg
            except Exception as e:
                print(f"  try {acc}: exception {e}")
                last_msg = str(e)
            time.sleep(0.34)

        if chosen is None:
            print(f"  [FAIL] no clean CDS for {species}: {last_msg}")
            results.append((species, None, None, last_msg))
            continue

        acc, cds_nt, prot_id, msg = chosen

        # 4. Write FASTA (same format as Calypte)
        out_path = PC_DIR / f"{species}_TAS1R1_cds.fasta"
        header = f">TAS1R1|{species}|{acc}"
        # Wrap at 80 chars to match existing style, but single-line is fine too
        with out_path.open("w") as fh:
            fh.write(header + "\n")
            fh.write(cds_nt + "\n")
        print(f"  [write] {out_path}")

        # Also write the protein for reference
        prot = str(Seq(cds_nt).translate(table=1, to_stop=False)).rstrip("*")
        prot_path = PC_DIR / f"{species}_TAS1R1_protein.fasta"
        with prot_path.open("w") as fh:
            fh.write(f">TAS1R1|{species}|{prot_id}\n")
            fh.write(prot + "\n")

        results.append((species, acc, prot_id, msg))

    print("\n=== Summary ===")
    print(f"{'Species':<30} {'Accession':<20} {'Protein':<20} {'Status'}")
    for sp, acc, pid, msg in results:
        status = "OK" if acc else f"FAIL: {msg}"
        print(f"{sp:<30} {acc or '-':<20} {pid or '-':<20} {status}")

    failures = [r for r in results if r[1] is None]
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
