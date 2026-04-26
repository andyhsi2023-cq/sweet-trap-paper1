#!/usr/bin/env python3
"""
17_compute_rbh_calls.py
=======================

Step 4 analysis: classify each of the 52 cnidarian candidates into one of:

  * RBH_DRD          — top-1 reverse hit is HUMAN_DRD* OR DMEL_DOP1R1/DOP2R,
                       AND bitscore-delta to the best non-DRD hit >= 10
                       AND forward evidence includes a DRD anchor
  * RBH_DRD_weak     — top-1 reverse hit is DRD but bitscore-delta to best
                       non-DRD hit < 10 (ambiguous placement)
  * NOT_DRD:HTR / NOT_DRD:ADR / NOT_DRD:OA / NOT_DRD:other
                     — top-1 reverse hit is from that family

The delta threshold of 10 bits corresponds to ~e^(-10) ≈ 4e-5 likelihood
ratio — a conservative but standard RBH confidence cutoff.

输入:
  outputs/blast_rbh/cnidarian_forward_hits_manifest.tsv (52 rows)
  outputs/blast_rbh/reverse_cnidaria_vs_human.tsv (1254 rows, multi-hit per cand)

输出:
  outputs/blast_rbh/rbh_classification.tsv
  outputs/blast_rbh/rbh_summary.tsv            (counts per species x class)
  outputs/blast_rbh/rbh_drd_candidates.faa    (sequences flagged RBH_DRD*)
"""
import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
OUT  = ROOT / "outputs" / "blast_rbh"

FIELDS = ["qseqid","sseqid","pident","length","mismatch","gapopen",
          "qstart","qend","sstart","send","evalue","bitscore","stitle"]

# family map: UniProt short-label prefix -> family class
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

DELTA_STRONG = 10.0  # bitscore delta to separate top-1 from best other-family


def parse_sseqid(sseqid: str) -> str:
    # UniProt label appears as "HUMAN_DRD1|P21728|..." when we custom-headed;
    # but makeblastdb may return only the first ID token. We stored the short
    # label as the first token, so splitting on '|' works.
    return sseqid.split("|", 1)[0]


def load_manifest(path: Path):
    rows = {}
    with path.open() as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            rows[row["cand_id"]] = row
    return rows


def load_reverse(path: Path):
    """Return: dict cand_id -> list of hit dicts (sorted by bitscore desc)."""
    by_cand = defaultdict(list)
    with path.open() as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            d = dict(zip(FIELDS, parts))
            d["bitscore_f"] = float(d["bitscore"])
            d["evalue_f"] = float(d["evalue"])
            by_cand[d["qseqid"].split("|", 1)[0]].append(d)  # cand_id is first token
    for cid in by_cand:
        by_cand[cid].sort(key=lambda x: x["bitscore_f"], reverse=True)
    return by_cand


def load_faa(path: Path):
    """Return dict: qseqid_first_token -> full fasta record."""
    recs = {}
    hdr, seq = None, []
    with path.open() as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if hdr is not None:
                    first = hdr[1:].split()[0].split("|")[0]
                    recs[first] = hdr + "\n" + "\n".join(seq) + "\n"
                hdr = line
                seq = []
            else:
                seq.append(line)
        if hdr is not None:
            first = hdr[1:].split()[0].split("|")[0]
            recs[first] = hdr + "\n" + "\n".join(seq) + "\n"
    return recs


def classify(hits):
    if not hits:
        return {"class": "NO_HIT", "top1_family": "", "top1_label": "",
                "top1_bitscore": "", "delta_top1_other_family": "",
                "best_drd_family_bitscore": "", "best_nondrd_family_bitscore": ""}

    top1 = hits[0]
    top1_label = parse_sseqid(top1["sseqid"])
    top1_family = FAM_MAP.get(top1_label, "UNK")

    # best hit per family
    best_per_fam = {}
    for h in hits:
        fam = FAM_MAP.get(parse_sseqid(h["sseqid"]), "UNK")
        if fam not in best_per_fam or h["bitscore_f"] > best_per_fam[fam]["bitscore_f"]:
            best_per_fam[fam] = h

    # DRD confidence: top DRD-family bitscore vs top non-DRD-family bitscore
    drd_like_fams = {"DRD", "inv_DRD"}
    best_drd = max(
        (h["bitscore_f"] for fam, h in best_per_fam.items() if fam in drd_like_fams),
        default=float("-inf"),
    )
    best_nondrd = max(
        (h["bitscore_f"] for fam, h in best_per_fam.items() if fam not in drd_like_fams),
        default=float("-inf"),
    )

    delta_drd = best_drd - best_nondrd if best_drd != float("-inf") and best_nondrd != float("-inf") else float("nan")

    # Decision tree
    if top1_family in drd_like_fams:
        if best_nondrd == float("-inf") or (best_drd - best_nondrd) >= DELTA_STRONG:
            call = "RBH_DRD_strong"
        else:
            call = "RBH_DRD_weak"
    else:
        call = f"NOT_DRD:{top1_family}"

    # top-1 bitscore delta vs top non-same-family
    other_fam_top = max(
        (h["bitscore_f"] for fam, h in best_per_fam.items() if fam != top1_family),
        default=float("-inf"),
    )
    delta_top1_other = (top1["bitscore_f"] - other_fam_top) if other_fam_top != float("-inf") else float("nan")

    return {
        "class": call,
        "top1_label": top1_label,
        "top1_family": top1_family,
        "top1_bitscore": top1["bitscore_f"],
        "top1_evalue": top1["evalue_f"],
        "delta_top1_other_family": delta_top1_other,
        "best_drd_family_bitscore": best_drd if best_drd != float("-inf") else "",
        "best_nondrd_family_bitscore": best_nondrd if best_nondrd != float("-inf") else "",
        "delta_drd_minus_nondrd": delta_drd,
    }


def main():
    manifest = load_manifest(OUT / "cnidarian_forward_hits_manifest.tsv")
    reverse = load_reverse(OUT / "reverse_cnidaria_vs_human.tsv")
    faa_lookup = load_faa(OUT / "cnidarian_forward_hits.faa")

    rows_out = []
    for cand_id, manrow in manifest.items():
        hits = reverse.get(cand_id, [])
        cls = classify(hits)
        out = {
            "cand_id": cand_id,
            "species": manrow["species"],
            "accession": manrow["accession"],
            "stitle": manrow["stitle"],
            "forward_best_anchor": manrow["best_forward_anchor"].split("|")[0],
            "forward_evalue": manrow["forward_evalue"],
            "forward_bitscore": manrow["forward_bitscore"],
            "forward_pident": manrow["forward_pident"],
            **cls,
        }
        rows_out.append(out)

    # Sort by species, then class priority (strong DRD first), then bitscore
    class_rank = {"RBH_DRD_strong": 0, "RBH_DRD_weak": 1}
    rows_out.sort(key=lambda r: (r["species"],
                                  class_rank.get(r["class"], 99),
                                  -(r["top1_bitscore"] if isinstance(r["top1_bitscore"], (int, float)) else 0)))

    out_tsv = OUT / "rbh_classification.tsv"
    keys = ["cand_id","species","accession","class","top1_label","top1_family",
            "top1_bitscore","top1_evalue","delta_top1_other_family",
            "best_drd_family_bitscore","best_nondrd_family_bitscore",
            "delta_drd_minus_nondrd",
            "forward_best_anchor","forward_evalue","forward_bitscore","forward_pident",
            "stitle"]
    with out_tsv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, delimiter="\t")
        w.writeheader()
        for r in rows_out:
            w.writerow({k: r.get(k, "") for k in keys})
    print(f"[rbh] -> {out_tsv}")

    # Summary
    summary = defaultdict(lambda: defaultdict(int))
    for r in rows_out:
        summary[r["species"]][r["class"]] += 1

    sum_tsv = OUT / "rbh_summary.tsv"
    classes = sorted({r["class"] for r in rows_out})
    with sum_tsv.open("w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["species"] + classes + ["total"])
        for sp in ("Hvul", "Nvec", "Adig"):
            row = [sp] + [summary[sp].get(c, 0) for c in classes]
            row.append(sum(summary[sp].values()))
            w.writerow(row)
    print(f"[rbh] -> {sum_tsv}")

    # Print summary
    print("\n=== RBH Summary ===")
    print("species\t" + "\t".join(classes) + "\ttotal")
    for sp in ("Hvul", "Nvec", "Adig"):
        cells = [str(summary[sp].get(c, 0)) for c in classes]
        print(f"{sp}\t" + "\t".join(cells) + f"\t{sum(summary[sp].values())}")

    # Write DRD candidate FASTA (strong + weak) for tree placement
    drd_fa = OUT / "rbh_drd_candidates.faa"
    n = 0
    with drd_fa.open("w") as f:
        for r in rows_out:
            if r["class"] in ("RBH_DRD_strong", "RBH_DRD_weak"):
                rec = faa_lookup.get(r["cand_id"])
                if rec:
                    f.write(rec)
                    n += 1
    print(f"[rbh] wrote {n} DRD candidate sequences -> {drd_fa}")


if __name__ == "__main__":
    main()
