#!/usr/bin/env python
"""
positive_control_v4_fetch_hummingbirds.py
=========================================

Fetch additional hummingbird + swift TAS1R1 CDS to match Baldwin 2014 /
Cockburn 2022 MBE taxon sampling.

Targets:
  RefSeq:     XM_071767433.1  Heliangelus exortis  (predicted mRNA)
  Cockburn 2022 GenBank submissions (Trochilidae + Apodidae):
              OM142609.1  Florisuga fusca
              OM142616.1  Ramphodon naevius
              OM142617.1  Heliothryx barroti
              OM142618.1  Haplophaedia aureliae
              OM142619.1  Lophornis magnificus
              OM142620.1  Patagona gigas
              OM142621.1  Amazilia tzacatl

All fetched as GenBank records; CDS extracted from the /CDS feature (respecting
introns via feat.extract). Output format matches existing:
    >TAS1R1|<Species>|<Accession>
Stored at data/positive_control/<Species>_TAS1R1_cds.fasta
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from io import StringIO
from Bio import Entrez, SeqIO
from Bio.Seq import Seq

Entrez.email = "26708155@alu.cqu.edu.cn"

PC_DIR = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/data/positive_control")

TARGETS = [
    # (species_name, accession)
    ("Heliangelus_exortis", "XM_071767433.1"),
    ("Florisuga_fusca", "OM142609.1"),
    ("Ramphodon_naevius", "OM142616.1"),
    ("Heliothryx_barroti", "OM142617.1"),
    ("Haplophaedia_aureliae", "OM142618.1"),
    ("Lophornis_magnificus", "OM142619.1"),
    ("Patagona_gigas", "OM142620.1"),
    ("Amazilia_tzacatl", "OM142621.1"),
]


def fetch_cds(accession: str) -> tuple[str, str]:
    """Return (cds_nt, protein_id) from a GenBank record."""
    h = Entrez.efetch(db="nuccore", id=accession, rettype="gb", retmode="text")
    gb = h.read()
    h.close()
    rec = SeqIO.read(StringIO(gb), "genbank")
    cds_feat = None
    for f in rec.features:
        if f.type == "CDS":
            cds_feat = f
            break
    if cds_feat is None:
        raise ValueError(f"No CDS in {accession}")
    cds_nt = str(cds_feat.extract(rec.seq)).upper()
    pid = cds_feat.qualifiers.get("protein_id", ["?"])[0]
    return cds_nt, pid


def verify(cds_nt: str) -> tuple[bool, str]:
    if len(cds_nt) % 3 != 0:
        return False, f"len%3={len(cds_nt) % 3}"
    prot = str(Seq(cds_nt).translate(table=1, to_stop=False))
    core = prot.rstrip("*")
    if "*" in core:
        return False, f"premature stop at aa {core.index('*')}"
    return True, f"aa={len(core)} nt={len(cds_nt)}"


def main() -> int:
    summary = []
    for species, acc in TARGETS:
        print(f"\n=== {species} ({acc}) ===")
        try:
            cds_nt, pid = fetch_cds(acc)
            ok, msg = verify(cds_nt)
            print(f"  fetched: {msg}  protein={pid}  {'OK' if ok else 'FAIL'}")
            if not ok:
                summary.append((species, acc, pid, f"FAIL: {msg}"))
                continue
            out = PC_DIR / f"{species}_TAS1R1_cds.fasta"
            out.write_text(f">TAS1R1|{species}|{acc}\n{cds_nt}\n")
            prot = str(Seq(cds_nt).translate(table=1, to_stop=False)).rstrip("*")
            (PC_DIR / f"{species}_TAS1R1_protein.fasta").write_text(
                f">TAS1R1|{species}|{pid}\n{prot}\n")
            print(f"  [write] {out}")
            summary.append((species, acc, pid, msg))
        except Exception as e:
            print(f"  ERROR: {e}")
            summary.append((species, acc, "?", f"FAIL: {e}"))
        time.sleep(0.34)

    print("\n=== Summary ===")
    for sp, acc, pid, status in summary:
        print(f"  {sp:30s} {acc:18s} {pid:18s} {status}")

    return 0 if not any(s[3].startswith("FAIL") for s in summary) else 1


if __name__ == "__main__":
    sys.exit(main())
