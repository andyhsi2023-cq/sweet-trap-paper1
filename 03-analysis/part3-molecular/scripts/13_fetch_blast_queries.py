#!/usr/bin/env python3
"""
13_fetch_blast_queries.py
=========================

目的
----
为 Part 3 Risk 1 BLASTP 双向互检策略准备 query 序列集合：

  (A) queries/DRD_anchors.faa
      vertebrate + invertebrate anchors，用于正向 BLASTP
      (anchor → 刺胞动物 proteome):
        - 5 human DRD (DRD1..DRD5, UniProt P21728 P14416 P35462 P21917 P21918)
        - Drosophila Dop1R1 (FBpp0305087 / UniProt Q24563)
        - Drosophila Dop2R (UniProt Q8IRY1)

  (B) queries/human_amine_reference.faa
      用于反向 BLASTP (刺胞动物 hit → human reference set),
      以区分 dopaminergic vs. serotonergic vs. adrenergic/octopaminergic:
        - 5 DRD (同上)
        - 7 HTR (HTR1A P08908, HTR1B P28222, HTR2A P28223, HTR2B P41595,
                 HTR4 Q13639, HTR6 P50406, HTR7 P34969)
        - 3 ADRB (ADRB1 P08588, ADRB2 P07550, ADRB3 P13945)
        - 2 ADRA (ADRA1A P35348, ADRA2A P08913)
        - 3 无脊椎对照 (Drosophila Dop1R1, Dop2R, Oct-β2R Q9VMH4)

使用
----
Entrez.email = "26708155@alu.cqu.edu.cn"  (按项目规则)
UniProt REST API，顺序下载，no parallel.

输出
----
    data/queries/DRD_anchors.faa
    data/queries/human_amine_reference.faa
    data/queries/query_manifest.tsv
"""
import sys, time, csv
from pathlib import Path
import urllib.request
import urllib.error

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
Q_DIR = ROOT / "data" / "queries"
Q_DIR.mkdir(parents=True, exist_ok=True)

DRD_ANCHORS = [
    # (uniprot_acc, short_label, long_label, organism)
    ("P21728", "HUMAN_DRD1", "Human dopamine D1 receptor",  "Homo sapiens"),
    ("P14416", "HUMAN_DRD2", "Human dopamine D2 receptor",  "Homo sapiens"),
    ("P35462", "HUMAN_DRD3", "Human dopamine D3 receptor",  "Homo sapiens"),
    ("P21917", "HUMAN_DRD4", "Human dopamine D4 receptor",  "Homo sapiens"),
    ("P21918", "HUMAN_DRD5", "Human dopamine D5 receptor",  "Homo sapiens"),
    # Drosophila canonical (FlyBase-verified)
    ("P41596", "DMEL_DOP1R1", "Drosophila Dop1R1 / DopR / FBgn0011582",        "Drosophila melanogaster"),
    ("Q8IS44", "DMEL_DOP2R",  "Drosophila Dop2R / D2R / FBgn0265749",          "Drosophila melanogaster"),
]

HUMAN_REF = [
    # Dopamine
    ("P21728", "HUMAN_DRD1", "DRD1", "DRD"),
    ("P14416", "HUMAN_DRD2", "DRD2", "DRD"),
    ("P35462", "HUMAN_DRD3", "DRD3", "DRD"),
    ("P21917", "HUMAN_DRD4", "DRD4", "DRD"),
    ("P21918", "HUMAN_DRD5", "DRD5", "DRD"),
    # Serotonin
    ("P08908", "HUMAN_HTR1A", "HTR1A", "HTR"),
    ("P28222", "HUMAN_HTR1B", "HTR1B", "HTR"),
    ("P28223", "HUMAN_HTR2A", "HTR2A", "HTR"),
    ("P41595", "HUMAN_HTR2B", "HTR2B", "HTR"),
    ("Q13639", "HUMAN_HTR4",  "HTR4",  "HTR"),
    ("P50406", "HUMAN_HTR6",  "HTR6",  "HTR"),
    ("P34969", "HUMAN_HTR7",  "HTR7",  "HTR"),
    # Adrenergic beta
    ("P08588", "HUMAN_ADRB1", "ADRB1", "ADRB"),
    ("P07550", "HUMAN_ADRB2", "ADRB2", "ADRB"),
    ("P13945", "HUMAN_ADRB3", "ADRB3", "ADRB"),
    # Adrenergic alpha
    ("P35348", "HUMAN_ADRA1A", "ADRA1A", "ADRA"),
    ("P08913", "HUMAN_ADRA2A", "ADRA2A", "ADRA"),
    # Invertebrate controls
    ("P41596", "DMEL_DOP1R1", "Dop1R1",  "inv_DRD"),
    ("Q8IS44", "DMEL_DOP2R",  "Dop2R",   "inv_DRD"),
    ("Q4LBB9", "DMEL_OCTB2R", "Oct-b2R", "inv_OA"),
]


def fetch_uniprot(acc: str, retries: int = 3, wait: float = 1.0) -> str:
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
    last_err = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read().decode("utf-8")
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            last_err = e
            time.sleep(wait * (i + 1))
    raise RuntimeError(f"UniProt fetch failed for {acc}: {last_err}")


def write_fa(entries, out_path: Path, label_idx: int = 1):
    """entries: list of tuples (acc, label, ...). label_idx = index of short label."""
    n = 0
    with out_path.open("w") as f:
        for row in entries:
            acc = row[0]
            label = row[label_idx]
            fa = fetch_uniprot(acc)
            # Re-header: replace first line with custom "short label"
            lines = fa.strip().splitlines()
            body = "\n".join(lines[1:])
            hdr = f">{label}|{acc}|{' '.join(lines[0].split()[1:])}"
            f.write(hdr + "\n" + body + "\n")
            n += 1
            time.sleep(0.4)  # be polite to UniProt
    return n


def main():
    print("[fetch] Writing DRD anchors ...")
    n1 = write_fa(DRD_ANCHORS, Q_DIR / "DRD_anchors.faa", label_idx=1)
    print(f"  -> {n1} entries")

    print("[fetch] Writing human + Dmel amine reference set ...")
    n2 = write_fa(HUMAN_REF, Q_DIR / "human_amine_reference.faa", label_idx=1)
    print(f"  -> {n2} entries")

    # Manifest
    man = Q_DIR / "query_manifest.tsv"
    with man.open("w") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["file", "label", "uniprot", "organism_or_family", "role"])
        for row in DRD_ANCHORS:
            acc, label, long_name, org = row
            w.writerow(["DRD_anchors.faa", label, acc, org, "forward_query_DRD_anchor"])
        for row in HUMAN_REF:
            acc, label, gene, fam = row
            w.writerow(["human_amine_reference.faa", label, acc, fam, "reverse_reference_amine_receptor"])
    print(f"[fetch] Manifest -> {man}")

    # Validate FASTAs
    for p in [Q_DIR / "DRD_anchors.faa", Q_DIR / "human_amine_reference.faa"]:
        n = sum(1 for ln in p.open() if ln.startswith(">"))
        print(f"  sanity: {p.name} has {n} records")

    return 0


if __name__ == "__main__":
    sys.exit(main())
