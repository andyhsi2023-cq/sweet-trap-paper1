#!/usr/bin/env python
"""
positive_control_v4_beb_analyze.py
==================================

Extract and analyze BEB (Bayes Empirical Bayes) results from v4 codeml runs.

For each run, parse the alt model's mlc file for positively-selected sites
(P(w>1) under site class 2a/2b) and:
  - Count sites at P > 0.50, > 0.80, > 0.95, > 0.99
  - Map each site back to the Calypte_anna residue position (vs. human position
    used in Baldwin 2014 Table 1)
  - Check whether the site coordinates overlap with the VFT (Venus flytrap)
    domain (approximately human positions 25-525 in the extracellular N-terminus)
  - Cross-check against Baldwin 2014 reported sites (site 147, 179, 288, 358,
    390, 392, 393, 439, 442, 447, 450, 451, 461, 469, 477, 491, 505, 517, 539
    in human TAS1R1 coords)

Writes to outputs/positive_control_v4_beb_sites.tsv and prints summary.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from Bio import SeqIO

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
RUNS = ROOT / "data" / "codeml_runs"
WORK = ROOT / "data" / "positive_control" / "work"
OUTPUTS = ROOT / "outputs"

# Baldwin 2014 Table 1 BEB sites (human TAS1R1 numbering) — the 19 VFT-domain
# sites under P > 0.95 they reported in Fig. 3 & Table 1.
# These are reconstructed from the paper (Baldwin 2014 Science).
BALDWIN_HUMAN_SITES = {
    147, 179, 288, 358, 390, 392, 393, 439, 442, 447, 450, 451, 461, 469,
    477, 491, 505, 517, 539,
}

# VFT (Venus flytrap) domain approximate range in human TAS1R1
# (Part 3 InterProScan PF01094 coords: roughly 30-520 in human)
VFT_HUMAN_RANGE = (30, 525)


def alignment_column_to_species_position(codon_aln_path: Path, species: str,
                                          column_1based: int) -> int | None:
    """Return the 1-based residue position in `species` that corresponds to
    alignment codon column `column_1based`, or None if that column is a gap."""
    aln = {r.id: str(r.seq) for r in SeqIO.parse(codon_aln_path, "fasta")}
    if species not in aln:
        return None
    codons = []
    seq = aln[species]
    # Extract codons
    for i in range(0, len(seq), 3):
        codons.append(seq[i:i+3])
    if column_1based < 1 or column_1based > len(codons):
        return None
    target = codons[column_1based - 1]
    if "-" in target:
        return None
    # Count non-gap codons up to and including target
    pos = 0
    for i, c in enumerate(codons):
        if "-" not in c:
            pos += 1
        if i == column_1based - 1:
            return pos
    return None


def parse_beb_sites(mlc_path: Path) -> list[tuple[int, str, float]]:
    """Parse the BEB output block in an alt-model mlc file.

    Returns a list of (column_1based, reference_aa, posterior_prob).
    The ref AA is the residue of the first taxon in the alignment (typically
    the tree's branch-site reference; codeml writes residues as seen in the
    first sequence).
    """
    text = mlc_path.read_text()
    # Find the BEB block. Format:
    #   Bayes Empirical Bayes (BEB) analysis ...
    #   Positive sites for foreground lineages Prob(w>1):
    #        1 M   0.123
    #       81 H   0.939*
    #       ...
    # It may be followed by another block "Naive Empirical Bayes (NEB)" which
    # we ignore.
    m = re.search(r"Bayes Empirical Bayes \(BEB\).*?Positive sites for foreground lineages.*?\n(.*?)(?:\n\s*\n|Prob\(w>1\)|The grid|\nGrid|\nNaive Empirical Bayes)",
                  text, re.DOTALL)
    if not m:
        # Try simpler pattern
        m = re.search(r"Positive sites for foreground lineages Prob\(w>1\):(.*?)(?:The grid|\n\s*\n\s*\n|\nNote)",
                      text, re.DOTALL)
        if not m:
            return []
    block = m.group(1)

    sites = []
    for line in block.splitlines():
        line = line.strip()
        if not line:
            continue
        m2 = re.match(r"^(\d+)\s+([A-Z\-*])\s+([0-9.]+)(\*{0,2})", line)
        if m2:
            col = int(m2.group(1))
            aa = m2.group(2)
            p = float(m2.group(3))
            sites.append((col, aa, p))
    return sites


def run_analysis(run_name: str, codon_aln_path: Path) -> dict:
    mlc = RUNS / run_name / "alt_init15_mlc.out"
    if not mlc.exists():
        mlc = RUNS / run_name / "alt_init05_mlc.out"
    if not mlc.exists():
        print(f"[skip] {run_name}: no alt mlc")
        return {}

    # Use the best-alt by lnL
    alt05 = RUNS / run_name / "alt_init05_mlc.out"
    alt15 = RUNS / run_name / "alt_init15_mlc.out"
    lnLs = {}
    for p in (alt05, alt15):
        if p.exists():
            m = re.search(r"^lnL.*?(-\d+\.\d+)", p.read_text(), re.MULTILINE)
            if m:
                lnLs[p] = float(m.group(1))
    if not lnLs:
        return {}
    best = max(lnLs, key=lnLs.get)
    sites = parse_beb_sites(best)

    # Load alignment once
    aln = {r.id: str(r.seq) for r in SeqIO.parse(codon_aln_path, "fasta")}

    # Build pos mappings: alignment col -> species-specific residue #
    def col_to_pos(sp: str, col: int) -> int | None:
        if sp not in aln:
            return None
        codons = [aln[sp][i:i+3] for i in range(0, len(aln[sp]), 3)]
        if col > len(codons) or "-" in codons[col-1]:
            return None
        return sum(1 for c in codons[:col] if "-" not in c)

    # Annotate
    anno = []
    for col, aa, p in sites:
        calypte_pos = col_to_pos("Calypte_anna", col)
        human_pos = col_to_pos("Homo_sapiens", col)
        vft = (human_pos is not None) and (VFT_HUMAN_RANGE[0] <= human_pos <= VFT_HUMAN_RANGE[1])
        baldwin = (human_pos is not None) and (human_pos in BALDWIN_HUMAN_SITES)
        # Also report what's at that column in key species
        residues = {}
        for sp in ("Calypte_anna", "Apus_apus", "Gallus_gallus",
                   "Homo_sapiens", "Mus_musculus", "Danio_rerio"):
            if sp in aln:
                codons = [aln[sp][i:i+3] for i in range(0, len(aln[sp]), 3)]
                if col <= len(codons):
                    codon = codons[col-1]
                    if "-" in codon:
                        residues[sp] = "-"
                    else:
                        try:
                            from Bio.Seq import Seq
                            residues[sp] = str(Seq(codon).translate())
                        except Exception:
                            residues[sp] = "?"
        anno.append({
            "aln_col": col, "ref_aa": aa, "P_fg>1": p,
            "Calypte_pos": calypte_pos,
            "Human_pos": human_pos,
            "In_VFT": vft,
            "Baldwin2014_site": baldwin,
            "residues": residues,
        })
    return {"run": run_name, "mlc": best.name, "n_sites": len(sites),
            "sites": anno}


def main() -> int:
    codon_aln_path = WORK / "codon_aligned_v4.fasta"

    v4_runs = sorted(d.name for d in RUNS.iterdir()
                     if d.is_dir() and d.name.startswith("TAS1R1_pc_v4__"))

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    out_tsv = OUTPUTS / "positive_control_v4_beb_sites.tsv"
    with out_tsv.open("w") as fh:
        fh.write("run\taln_col\tref_aa\tP_fg_gt1\tCalypte_pos\tHuman_pos\tIn_VFT\tBaldwin2014\t"
                "Calypte\tApus\tGallus\tHomo\tMus\tDanio\n")

        print(f"{'Run':<45} | {'P>0.5':>5} {'P>0.8':>5} {'P>0.95':>6} {'P>0.99':>6} | Baldwin_overlap")
        print("-" * 110)
        for name in v4_runs:
            res = run_analysis(name, codon_aln_path)
            if not res:
                continue
            sites = res["sites"]
            p5 = [s for s in sites if s["P_fg>1"] > 0.50]
            p8 = [s for s in sites if s["P_fg>1"] > 0.80]
            p95 = [s for s in sites if s["P_fg>1"] > 0.95]
            p99 = [s for s in sites if s["P_fg>1"] > 0.99]
            baldwin_hit = [s for s in sites if s.get("Baldwin2014_site") and s["P_fg>1"] > 0.50]
            in_vft = [s for s in p95 if s.get("In_VFT")]
            print(f"{name:<45} | {len(p5):>5} {len(p8):>5} {len(p95):>6} {len(p99):>6} | "
                  f"{len(baldwin_hit)} baldwin-hit (P>0.5); VFT@P>0.95: {len(in_vft)}")
            for s in sites:
                r = s["residues"]
                fh.write("\t".join([
                    name, str(s["aln_col"]), s["ref_aa"], f"{s['P_fg>1']:.4f}",
                    str(s.get("Calypte_pos", "")), str(s.get("Human_pos", "")),
                    "Y" if s.get("In_VFT") else "N",
                    "Y" if s.get("Baldwin2014_site") else "N",
                    r.get("Calypte_anna", ""), r.get("Apus_apus", ""),
                    r.get("Gallus_gallus", ""), r.get("Homo_sapiens", ""),
                    r.get("Mus_musculus", ""), r.get("Danio_rerio", ""),
                ]) + "\n")
            if p95:
                print(f"  {'col':>4} {'Cal':>5} {'Hum':>5} {'P':>7} {'VFT':>4} {'B2014':>5}  residues(Cal/Apus/Gal/Hum/Mus/Dan)")
                for s in p95[:25]:
                    r = s["residues"]
                    print(f"  {s['aln_col']:>4} {s.get('Calypte_pos',''):>5} {s.get('Human_pos',''):>5} "
                          f"{s['P_fg>1']:>7.4f} {'Y' if s.get('In_VFT') else 'n':>4} "
                          f"{'Y' if s.get('Baldwin2014_site') else 'n':>5}  "
                          f"{r.get('Calypte_anna','')} {r.get('Apus_apus','')} "
                          f"{r.get('Gallus_gallus','')} {r.get('Homo_sapiens','')} "
                          f"{r.get('Mus_musculus','')} {r.get('Danio_rerio','')}")

    print(f"\n[write] {out_tsv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
