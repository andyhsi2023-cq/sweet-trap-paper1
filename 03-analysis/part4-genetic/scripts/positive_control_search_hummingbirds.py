#!/usr/bin/env python
"""
Search NCBI for additional hummingbird TAS1R1 CDS to enable Baldwin 2014's
"crown-hummingbird MRCA" foreground design.
"""
from Bio import Entrez
import time

Entrez.email = "26708155@alu.cqu.edu.cn"

# Candidate hummingbird species from Baldwin 2014 + recent genomes
CANDIDATES = [
    "Florisuga mellivora",
    "Topaza pella",
    "Archilochus alexandri",
    "Archilochus colubris",
    "Amazilia",
    "Selasphorus",
    "Lophornis ornatus",
    "Phaethornis",
    "Eupetomena macroura",
    "Anthracothorax",
    "Chaetura pelagica",  # also swift, for bonus
    "Hirundapus",         # another swift
    "Colibri",
    "Trochilus polytmus",
    "Patagona gigas",
    "Oreotrochilus",
]


def search(species: str):
    query = f'{species}[Organism] AND TAS1R1[Gene Name] AND refseq[filter]'
    handle = Entrez.esearch(db="nuccore", term=query, retmax=10)
    rec = Entrez.read(handle)
    handle.close()
    return rec.get("IdList", [])


def main():
    print(f"{'Species':<30} {'NumHits':>8}  Accessions")
    for sp in CANDIDATES:
        try:
            ids = search(sp)
            accs = []
            if ids:
                handle = Entrez.esummary(db="nuccore", id=",".join(ids))
                recs = Entrez.read(handle)
                handle.close()
                accs = [r.get("AccessionVersion", "?") for r in recs if
                        str(r.get("AccessionVersion", "")).startswith(("XM_", "NM_"))]
            print(f"{sp:<30} {len(accs):>8}  {accs[:3]}")
        except Exception as e:
            print(f"{sp:<30} ERROR: {e}")
        time.sleep(0.34)


if __name__ == "__main__":
    main()
