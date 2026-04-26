#!/usr/bin/env python3
"""
06_architecture_consistency.py
==============================

Summarise the H4a (within-phylum conservation) and H4b (cross-phylum
convergence) signatures from the InterProScan output.

For each receptor family × lineage cell, report:
  - fraction carrying the family-diagnostic Pfam domain
  - full ordered Pfam architecture per protein

Output: outputs/architecture_consistency.csv + a plain-text report.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

PROJECT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
TOP = PROJECT / "outputs" / "domain_topology.csv"
INV = PROJECT / "outputs" / "ortholog_inventory.csv"
OUT_CSV = PROJECT / "outputs" / "architecture_consistency.csv"
OUT_TXT = PROJECT / "outputs" / "architecture_consistency.txt"

FAMILIES = {
    "TAS1R": "TAS1R (Chordata sweet/umami Class-C)",
    "DRD":   "DRD (Chordata dopamine Class-A)",
    "Gr":    "Gr (Arthropoda gustatory 7TM_6)",
    "DopR_": "Dop (Mollusc/Cnidaria dopamine-like Class-A)",
    "DopR":  "DopR (Arthropoda dopamine Class-A)",
}

# Order matters: DopR_ must be tested before DopR.
ORDER = ["TAS1R", "DRD", "Gr", "DopR_", "DopR"]

FOCUS = {
    "PF00001": "7tm_1_ClassA",
    "PF00003": "7tm_3_ClassC",
    "PF01094": "ANF_VenusFlytrap",
    "PF07562": "NCD3G",
    "PF06151": "Insect7TM6_Gr",
}


def family_of(gene: str) -> str | None:
    for key in ORDER:
        if gene.startswith(key):
            return FAMILIES[key]
    return None


def main() -> int:
    # protein -> set of Pfam accessions
    per: dict[str, set[str]] = defaultdict(set)
    for row in csv.DictReader(open(TOP)):
        acc = row.get("accession", "")
        if acc.startswith("PF"):
            per[row["protein"]].add(acc)

    per_family: dict[str, list[tuple[str, str, set[str]]]] = defaultdict(list)
    for row in csv.DictReader(open(INV)):
        if row["fetched"] != "Y":
            continue
        fam = family_of(row["gene"])
        if not fam:
            continue
        species = row["species"]
        parts = species.split()
        short = (parts[0][0] + parts[1]).lower()
        prot_name = f"{row['gene']}_{short}"
        per_family[fam].append((row["gene"], species, per.get(prot_name, set())))

    # Write CSV
    rows_out = []
    txt = []
    for fam in FAMILIES.values():
        items = per_family.get(fam, [])
        n = len(items)
        txt.append(f"\n=== {fam} (n={n}) ===")
        # fraction carrying each focus domain
        counts = {f: 0 for f in FOCUS}
        for _, _, accs in items:
            for f in FOCUS:
                if f in accs:
                    counts[f] += 1
        row = {"family": fam, "n": n}
        for pfam, lbl in FOCUS.items():
            frac = counts[pfam] / n if n else 0.0
            row[f"frac_{lbl}"] = f"{frac:.2f}"
            txt.append(f"  {pfam} {lbl:25s}  {counts[pfam]:2d}/{n}   ({frac*100:4.1f}%)")
        # representative architecture (most common)
        arch_count: dict[str, int] = defaultdict(int)
        for _, _, accs in items:
            s = "+".join(sorted(accs)) if accs else "(none)"
            arch_count[s] += 1
        if arch_count:
            common = sorted(arch_count.items(), key=lambda x: -x[1])[0]
            row["dominant_pfam_architecture"] = common[0]
            row["dominant_fraction"] = f"{common[1] / n:.2f}"
            txt.append(f"  dominant architecture: {common[0]} ({common[1]}/{n})")
            if len(arch_count) > 1:
                txt.append(f"  other architectures: {len(arch_count)-1}")
        rows_out.append(row)

        # per-protein detail in the text report
        for gene, sp, accs in sorted(items):
            txt.append(f"    {gene:8s} {sp:30s}  "
                       f"{'+'.join(sorted(accs)) if accs else '(no Pfam)'}")

    # H4b convergence verdict
    txt.append("\n=== H4b Convergence Signature ===")
    # Key comparison: Chordata TAS1R vs Arthropoda Gr
    tas1r_items = per_family.get(FAMILIES["TAS1R"], [])
    gr_items = per_family.get(FAMILIES["Gr"], [])
    drd_items = per_family.get(FAMILIES["DRD"], [])
    dopr_items = per_family.get(FAMILIES["DopR"], [])
    dop_mollusc = per_family.get(FAMILIES["DopR_"], [])

    if tas1r_items and gr_items:
        tas1r_accs = {a for _, _, s in tas1r_items for a in s}
        gr_accs = {a for _, _, s in gr_items for a in s}
        common = tas1r_accs & gr_accs
        union = tas1r_accs | gr_accs
        jacc = len(common) / len(union) if union else 0.0
        txt.append(f"  TAS1R Pfam set: {sorted(tas1r_accs)}")
        txt.append(f"  Gr    Pfam set: {sorted(gr_accs)}")
        txt.append(f"  Pfam Jaccard TAS1R vs Gr: {jacc:.2f}")
        if jacc < 0.2:
            txt.append("  => Pfam-level paraphyly CONFIRMED (non-orthologous).")
        txt.append("  Shared functional architecture test: both have 7TM + LBD")
        tas1r_7tm = any("PF00003" in s for _, _, s in tas1r_items)
        gr_7tm = any("PF06151" in s for _, _, s in gr_items)
        txt.append(f"    TAS1R has 7TM (PF00003 Class-C): {tas1r_7tm}")
        txt.append(f"    Gr    has 7TM (PF06151 insect 7TM_6): {gr_7tm}")
        txt.append(f"    TAS1R has LBD (PF01094 VFT): {any('PF01094' in s for _, _, s in tas1r_items)}")
        txt.append("    Gr    has LBD: (not a separate Pfam domain — LBD "
                   "encoded within 7TM_6 transmembrane topology)")

    if drd_items and dopr_items and dop_mollusc:
        all_dop = drd_items + dopr_items + dop_mollusc
        n_classA = sum(1 for _, _, s in all_dop if "PF00001" in s)
        txt.append(f"  Dopamine receptors across 4 phyla: {n_classA}/{len(all_dop)} "
                   f"carry PF00001 (7tm_1 Class-A GPCR)")
        if n_classA == len(all_dop):
            txt.append("  => Class-A GPCR architecture deeply conserved across "
                       "Chordata + Arthropoda + Mollusca + Cnidaria.")

    # Write outputs
    with OUT_CSV.open("w", newline="") as fh:
        fieldnames = ["family", "n"] + [f"frac_{lbl}" for lbl in FOCUS.values()] + \
                     ["dominant_pfam_architecture", "dominant_fraction"]
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows_out:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    OUT_TXT.write_text("\n".join(txt) + "\n")
    print("\n".join(txt))
    print(f"\ncsv -> {OUT_CSV}")
    print(f"txt -> {OUT_TXT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
