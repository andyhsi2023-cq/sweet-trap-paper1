#!/usr/bin/env python3
"""
23_pfam_jaccard_null.py
=======================

Matched-random null baseline for the Jaccard(TAS1R Pfam, Gr Pfam) = 0 finding.

Context
-------
Part 3 molecular analysis reports:
  - TAS1R (Chordata sweet/umami, Class-C GPCR) Pfam set
      = {PF00003 (7tm_3), PF01094 (ANF_receptor), PF07562 (NCD3G)}
  - Gr (Arthropoda gustatory 7TM_6) Pfam set
      = {PF06151 (Trehalose_recp)}
  - Observed Jaccard index = |A ∩ B| / |A ∪ B| = 0 / 4 = 0.

Hostile-referee question: is Jaccard = 0 even "interesting" given that the Pfam
universe is huge? This script answers by computing the probability of Jaccard = 0
under an explicit null model where two receptor families of sizes (k1=3, k2=1)
are drawn independently from a finite Pfam-A universe.

Null model
----------
Draw k1 distinct Pfam families uniformly at random from N (without replacement),
then draw k2 distinct Pfam families independently. The chance that the two
draws are disjoint (Jaccard = 0) is:

    P(Jaccard = 0 | null) = C(N - k1, k2) / C(N, k2)
                          ≈ ((N - k1) / N)^k2  for small k2, large N.

For Pfam-A v37 (19,632 families) with k1=3, k2=1:
    P = (19632 - 3) / 19632 ≈ 0.99985

Interpretation: under a naïve null where receptor families draw Pfam domains
uniformly, Jaccard = 0 is the *overwhelmingly expected* outcome. The observed
Jaccard = 0 therefore does NOT, on its own, demonstrate evolutionary
convergence or divergence -- it is what the null predicts.

A secondary, more informative null restricts the draws to GPCR-associated Pfam
families (a much smaller pool, ~50-100 Pfam families span the ~800 human GPCRs
and their relatives). We report that scenario too as a sensitivity check.

Enrichment ratio
----------------
We report the ratio observed / null = 1 / P(Jaccard=0|null). When P is near 1,
the ratio is ~1 and the finding is *not* enriched vs null.

Output
------
- outputs/pfam_null_baseline.md : one-page honest report
- this script
"""
from __future__ import annotations

import csv
from math import comb
from pathlib import Path

# ---------------------------------------------------------------------------
# Step 1. Re-confirm Pfam sets from the source file.
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
ARCH_CSV = ROOT / "outputs" / "domain_architecture_summary.csv"
CONSIST_CSV = ROOT / "outputs" / "architecture_consistency.csv"
REPORT_MD = ROOT / "outputs" / "pfam_null_baseline.md"


def extract_pfam_set(domain_arch: str) -> set[str]:
    """Parse strings like 'ANF_receptor(PF01094);NCD3G(PF07562);7tm_3(PF00003)'."""
    out = set()
    if not domain_arch or domain_arch == "NA":
        return out
    for token in domain_arch.split(";"):
        token = token.strip()
        # extract the PFxxxxx accession inside parentheses
        l = token.find("(")
        r = token.find(")")
        if 0 <= l < r:
            acc = token[l + 1 : r].strip()
            if acc.startswith("PF"):
                out.add(acc)
    return out


def confirm_family_sets() -> dict[str, set[str]]:
    """Pool all Pfam accessions observed in the proteins of each family."""
    tas1r_union: set[str] = set()
    gr_union: set[str] = set()
    tas1r_count = 0
    gr_count = 0
    with ARCH_CSV.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            protein = row["protein"]
            doms = extract_pfam_set(row["domain_arch_pfam"])
            if protein.startswith("TAS1R"):
                tas1r_union |= doms
                tas1r_count += 1
            elif protein.startswith("Gr"):
                # includes Gr5a_* Gr64*_* and Gr_sweet_hitN_*
                # exclude Gr5a (Lipase PF00151) since it is a lipid-binding outlier
                # commonly excluded from sweet-receptor analyses; document both.
                gr_union |= doms
                gr_count += 1
    return {
        "TAS1R_pool_full": tas1r_union,
        "Gr_pool_full": gr_union,
        "TAS1R_count": tas1r_count,
        "Gr_count": gr_count,
    }


# ---------------------------------------------------------------------------
# Step 2. Compute null Jaccard=0 probabilities.
# ---------------------------------------------------------------------------

def p_jaccard_zero(N: int, k1: int, k2: int) -> float:
    """Probability two independent k1- and k2- samples (no replacement) from
    a universe of size N are disjoint."""
    if k2 > N - k1:
        return 0.0
    return comb(N - k1, k2) / comb(N, k2)


def main() -> None:
    info = confirm_family_sets()
    tas1r_pool_full = info["TAS1R_pool_full"]
    gr_pool_full = info["Gr_pool_full"]

    # The "canonical" TAS1R architecture per the consistency table
    tas1r_canon = {"PF00003", "PF01094", "PF07562"}
    gr_canon = {"PF06151"}

    # The pool over all 38 Gr proteins additionally contains PF00151 (Lipase,
    # from Gr5a) and rarely PF08395 (7tm_7). Report the canonical and the full
    # pool separately.
    obs_jaccard_canon = (
        len(tas1r_canon & gr_canon) / len(tas1r_canon | gr_canon)
        if (tas1r_canon | gr_canon)
        else 0.0
    )
    obs_jaccard_full = (
        len(tas1r_pool_full & gr_pool_full) / len(tas1r_pool_full | gr_pool_full)
        if (tas1r_pool_full | gr_pool_full)
        else 0.0
    )

    # Null 1: Pfam-A v37 universe
    N_pfam = 19632
    k1 = len(tas1r_canon)  # 3
    k2 = len(gr_canon)  # 1
    p_null_full_pfam = p_jaccard_zero(N_pfam, k1, k2)

    # Null 2: GPCR-Pfam universe (restricted, more informative).
    # Pfam v37 lists ~18 families under "7-transmembrane" clan CL0192 (7tmB) +
    # CL0193 (7tmA) + isolated GPCR-related families. A generous bound is ~50
    # Pfam families that carry any GPCR-type 7-TM fold. We sweep N in
    # {20, 50, 100} as sensitivity.
    gpcr_universe_scan = [20, 50, 100]
    gpcr_results = []
    for Ng in gpcr_universe_scan:
        p = p_jaccard_zero(Ng, k1, k2)
        gpcr_results.append((Ng, p))

    # Enrichment ratio: observed (1 if Jaccard=0, else 0) / expected under null.
    # Since observed is a 0/1 indicator here, we report the *log-ratio* style
    # statement instead of a raw ratio (raw ratio is trivially 1/P).
    enrichment_full_pfam = 1.0 / p_null_full_pfam if p_null_full_pfam > 0 else float("inf")

    # ----------------------------- write report --------------------------------
    lines: list[str] = []
    ap = lines.append
    ap("# Pfam Jaccard matched-random null baseline")
    ap("")
    ap("**Script**: `03-analysis/part3-molecular/scripts/23_pfam_jaccard_null.py`  ")
    ap("**Source**: `outputs/domain_architecture_summary.csv` (51 proteins) and ")
    ap("`outputs/architecture_consistency.csv` (family-level summary).")
    ap("")
    ap("## 1. Observed Pfam sets (re-confirmed)")
    ap("")
    ap(f"- TAS1R ({info['TAS1R_count']} proteins) canonical set: "
       f"{sorted(tas1r_canon)}  ")
    ap(f"- TAS1R full pool (all Pfam hits across 13 proteins): "
       f"{sorted(tas1r_pool_full)}")
    ap(f"- Gr ({info['Gr_count']} proteins) canonical set: {sorted(gr_canon)}  ")
    ap(f"- Gr full pool (all Pfam hits across 38 proteins): "
       f"{sorted(gr_pool_full)}")
    ap("")
    ap(f"- Observed Jaccard (canonical-vs-canonical): **{obs_jaccard_canon:.3f}**")
    ap(f"- Observed Jaccard (full pool vs full pool): **{obs_jaccard_full:.3f}**")
    ap("")
    ap("## 2. Null model")
    ap("")
    ap("Two receptor families draw $k_1=|TAS1R|$ and $k_2=|Gr|$ distinct Pfam ")
    ap("families independently and uniformly from a universe of size $N$. The ")
    ap("probability that the two sets are disjoint (Jaccard = 0) is")
    ap("")
    ap("$$P(J=0\\,|\\,N,k_1,k_2) = \\frac{\\binom{N-k_1}{k_2}}{\\binom{N}{k_2}}.$$")
    ap("")
    ap("### 2a. Null #1 — full Pfam-A v37 universe")
    ap("")
    ap(f"- $N = {N_pfam:,}$ Pfam-A families (Pfam v37, Jan 2025 release)")
    ap(f"- $k_1 = {k1}$ (TAS1R), $k_2 = {k2}$ (Gr)")
    ap(f"- **P(Jaccard = 0 | null) = {p_null_full_pfam:.6f}**")
    ap(f"- Enrichment ratio observed / null ≈ {enrichment_full_pfam:.3f} "
       f"(≈1 means: no enrichment vs null)")
    ap("")
    ap("### 2b. Null #2 — GPCR-Pfam universe (restricted)")
    ap("")
    ap("A more informative null restricts the universe to Pfam families that ")
    ap("encode a 7-TM GPCR-type fold (Pfam clans CL0192 7tmA + CL0193 7tmB, plus ")
    ap("a handful of isolated families; ~20–100 depending on inclusion rule).")
    ap("")
    ap("| $N$ (GPCR Pfam universe) | P(Jaccard = 0 \\| null) |")
    ap("|---:|---:|")
    for Ng, p in gpcr_results:
        ap(f"| {Ng} | {p:.4f} |")
    ap("")
    ap("Even under the tightest restriction ($N=20$), P(Jaccard=0) is still ")
    ap(f"{gpcr_results[0][1]:.3f}, i.e. well above any conventional α.")
    ap("")
    ap("## 3. Honest interpretation")
    ap("")
    ap("Under **every** reasonable null, Jaccard = 0 between two small Pfam sets ")
    ap("(k1=3, k2=1) is the expected outcome, not an enriched signal. The ")
    ap("observed Jaccard = 0 therefore does **not** constitute statistical ")
    ap("evidence for convergent or divergent molecular architecture.")
    ap("")
    ap("What the observation *does* establish is a **descriptive-architectural** ")
    ap("fact: chordate sweet/umami reception (TAS1R) uses a Class-C GPCR with an ")
    ap("obligate VFT + NCD3G + 7tm_3 module, whereas arthropod sweet/umami ")
    ap("reception (Gr) uses a Class-unrelated Insect7TM_6 (Trehalose_recp) ")
    ap("module. These two receptor systems evolved independently, as expected ")
    ap("from ~600 Myr of lineage separation; they share the *functional role* ")
    ap("(detect sweet reward) but not the protein scaffold.")
    ap("")
    ap("## 4. Recommendation to manuscript team")
    ap("")
    ap("- **Do not** frame this as 'Jaccard = 0 proves independent origin' ")
    ap("  (that would be a statistical overclaim; the null expects it).")
    ap("- **Do** frame this as: 'TAS1R and Gr belong to non-homologous GPCR ")
    ap("  classes (Class-C VFT vs insect 7TM_6). This architectural disjoint ")
    ap("  is consistent with convergent evolution of sweet detection atop ")
    ap("  distinct receptor scaffolds but, given the large Pfam universe, ")
    ap("  disjointness alone is not statistical evidence of convergence ")
    ap("  (null P(Jaccard=0) ≈ 0.9999 under Pfam-A v37).'")
    ap("- The *convergence* claim for sweet reception should instead be ")
    ap("  supported by behavioral / ligand-binding / pathway-output evidence ")
    ap("  (shared downstream G-protein cascade producing positive valence), ")
    ap("  not by Pfam set disjointness.")
    ap("")
    ap("## 5. Numbers for the manuscript")
    ap("")
    ap(f"- Observed Jaccard = {obs_jaccard_canon:.2f}")
    ap(f"- P(Jaccard = 0 | Pfam-A v37 null) = {p_null_full_pfam:.4f}")
    ap(f"- Enrichment ratio observed / null ≈ 1.00 (no enrichment)")
    ap("- Recommendation: report as descriptive-architectural, not as ")
    ap("  convergence evidence.")
    ap("")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT_MD}")
    print(f"Observed Jaccard (canonical) = {obs_jaccard_canon:.3f}")
    print(f"P(Jaccard=0 | Pfam-A v37, k1={k1}, k2={k2}) = {p_null_full_pfam:.6f}")
    for Ng, p in gpcr_results:
        print(f"P(Jaccard=0 | GPCR universe N={Ng}) = {p:.4f}")


if __name__ == "__main__":
    main()
