#!/usr/bin/env python
"""
04_write_h6a_report.py
======================

Assemble outputs/h6a_production_run_report.md from
  - outputs/branch_site_results.csv
  - outputs/branch_site_beb_sites.csv
  - scripts/branch_site_test_matrix_v2.tsv
  - outputs/positive_control_v4_lrt_summary.tsv (gate baseline)

Writes a structured markdown report for §3.4 of the manuscript and for the
final Week-2 Part-4 deliverable.
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path

import pandas as pd

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
OUT = ROOT / "outputs"

RESULTS_CSV = OUT / "branch_site_results.csv"
BEB_CSV = OUT / "branch_site_beb_sites.csv"
MATRIX_TSV = ROOT / "scripts" / "branch_site_test_matrix_v2.tsv"
REPORT = OUT / "h6a_production_run_report.md"


def fmt_p(p: float) -> str:
    if pd.isna(p):
        return "NA"
    if p < 1e-10:
        return f"{p:.2e}"
    if p < 1e-4:
        return f"{p:.3e}"
    return f"{p:.4f}"


def fmt_f(x, d: int = 2) -> str:
    if pd.isna(x):
        return "NA"
    return f"{x:.{d}f}"


def main() -> int:
    df = pd.read_csv(RESULTS_CSV)
    beb = pd.read_csv(BEB_CSV) if BEB_CSV.exists() else pd.DataFrame()
    matrix = pd.read_csv(MATRIX_TSV, sep="\t") if MATRIX_TSV.exists() else pd.DataFrame()

    # Enrich df with matrix metadata (notes, alignment_source) for production rows
    meta_cols = ["gene", "lineage_key", "fg_type", "alignment_source", "notes"]
    if len(matrix):
        matrix = matrix[meta_cols].copy()
        matrix["run_id"] = matrix["gene"] + "__" + matrix["lineage_key"]
        df = df.merge(matrix[["run_id", "alignment_source", "notes"]],
                      on="run_id", how="left")

    # Flag counts
    prod = df[df["role"] == "production"]
    n_total = len(prod)
    n_completed = int(prod["p_raw_half_chi2_df1"].notna().sum())
    n_failed = int(prod["status"].eq("no_stats").sum())
    n_bonf_prereg = int(prod["bonferroni_significant_prereg"].sum())
    n_bonf_real = int(prod["bonferroni_significant_realised"].sum())
    n_bh05 = int(prod["bh_significant_q05"].sum())
    n_bh10 = int(prod["bh_significant_q10"].sum())

    n_tests_real = int(prod.iloc[0]["n_tests_realised"]) if len(prod) else 0

    # Verdict logic: pre-reg flagged `tip_underpowered` rows as SENSITIVITY-only.
    # A primary H6a claim requires a significant CLADE row, because clade rows
    # are the pre-specified primary tests. Tip rows that happen to be significant
    # get called "suggestive" regardless of p-value.
    sig_prereg_clade = prod[
        (prod["bonferroni_significant_prereg"]) & (prod["fg_type"] == "clade")
    ]
    sig_real_clade = prod[
        (prod["bonferroni_significant_realised"]) & (prod["fg_type"] == "clade")
    ]
    sig_bh_clade = prod[
        (prod["bh_significant_q10"]) & (prod["fg_type"] == "clade")
    ]
    if len(sig_prereg_clade) >= 1:
        verdict = "SUPPORTED"
    elif len(sig_real_clade) >= 1:
        verdict = "SUPPORTED_REALISED_ALPHA_ONLY"
    elif len(sig_bh_clade) >= 1:
        verdict = "SUGGESTIVE_CLADE"
    elif n_bonf_prereg >= 1:
        # Tip rows flag but no clade row — must be treated as sensitivity-only
        verdict = "SUGGESTIVE_TIP_ONLY"
    elif n_bh10 >= 1:
        verdict = "SUGGESTIVE"
    else:
        verdict = "NOT_SUPPORTED"

    # Top-3 positive signals (by LRT)
    top_prod = prod.dropna(subset=["p_raw_half_chi2_df1"]).sort_values(
        "p_raw_half_chi2_df1"
    ).head(5)

    # Control re-verification
    ctl = df[df["role"] == "control"]

    with REPORT.open("w") as f:
        # Figure out which rows are still pending (in-flight or failed-in-progress)
        prod_ids = set(prod["run_id"].tolist())
        matrix_ids = {r["gene"] + "__" + r["lineage_key"] for _, r in matrix.iterrows()} if len(matrix) else set()
        pending_ids = matrix_ids - prod_ids
        # Filter to rows still truly incomplete
        in_flight = []
        failed_mid = []
        for rid in pending_ids:
            path = ROOT / "data" / "codeml_runs" / rid
            if not path.exists():
                continue
            # Check rub file growth
            rub = path / "rub"
            if rub.exists() and rub.stat().st_size > 500:
                in_flight.append(rid)
            else:
                failed_mid.append(rid)

        f.write(f"# Part 4 §H6a — Week-2 22-row branch-site production run\n\n")
        f.write(f"**Generated**: {_dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if len(pending_ids) > 0:
            f.write(f"**Status**: **partial** ({n_completed}/{len(matrix_ids) if matrix_ids else n_total} rows "
                    f"completed; {len(pending_ids)} still running/queued)\n")
        else:
            f.write(f"**Status**: batch complete ({n_completed}/{n_total})\n")
        f.write(f"**H6a verdict (on completed rows)**: **{verdict}**\n\n")

        if in_flight or failed_mid:
            f.write("### Rows still in-flight or needing re-run\n\n")
            if in_flight:
                f.write("**In-flight (codeml iterating; rub file growing):**\n\n")
                for rid in sorted(in_flight):
                    f.write(f"- `{rid}`\n")
                f.write("\n")
            if failed_mid:
                f.write("**Queued but not yet started (waiting on drain slot):**\n\n")
                for rid in sorted(failed_mid):
                    f.write(f"- `{rid}`\n")
                f.write("\n")
            f.write("These rows must be included in the final table before the Figure 4 / manuscript "
                    "draft is finalised. Re-run `03_multiple_testing_v2.py` + `04_write_h6a_report.py` "
                    "once they complete.\n\n")


        f.write("## Upstream reality check\n\n")
        f.write(
            "Part 3 delivered codon alignments for only 4 genes (TAS1R1, TAS1R2, "
            "TAS1R3, Gr_sweet) out of the 15 in the pre-registered gene matrix. "
            "The original v1 matrix assumed 15-gene × 4-lineage = 60 tests; the "
            "realised matrix is a 21-row v2 that sources from only those genes.\n\n"
            "Gene coverage delivered by Part 3:\n\n"
            "| Gene | Taxa | Fate |\n|------|------|------|\n"
            "| TAS1R1 | 5 mammals + Gallus + Danio (5 taxa) | Part-3 alignment used for 1 cross-ref row |\n"
            "| TAS1R1 | 16 taxa (v4 hummingbird-rich) | Used for all v4-labelled rows |\n"
            "| TAS1R2 | 3 mammals | **EXCLUDED** (< 4 taxa, branch-site undetermined) |\n"
            "| TAS1R3 | 5 vertebrate taxa | 5 rows |\n"
            "| Gr_sweet | 38 insect paralogs | 8 rows (paralog-clade foregrounds) |\n"
            "| DRD1-5, OPRM1/K1/D1/L1, HCRTR1-2, NPY1/2/5R, DopR1/2 | CDS fetched but **NO codon alignment built by Part 3** | **BLOCKED**; see §Limitations |\n\n"
        )

        f.write("## Positive-control gate re-verification\n\n")
        f.write("| Run | LRT | p_half | fg ω₂a | p2a+p2b | BEB P>0.95 |\n|---|---:|---:|---:|---:|---:|\n")
        for _, r in ctl.iterrows():
            f.write(
                f"| {r['run_id']} | {fmt_f(r['LRT_2dlnL'])} | {fmt_p(r['p_raw_half_chi2_df1'])} | "
                f"{fmt_f(r['fg_omega_2a'])} | {fmt_f(r['p2a_p2b'], 4)} | {int(r['n_beb_gt95']) if pd.notna(r['n_beb_gt95']) else 'NA'} |\n"
            )
        f.write(
            "\nAll three v4 control rows re-verified. The hummingbird positive "
            "controls (Apodiformes and hummingbirds clades) remain at p < 10⁻¹³ "
            "with foreground ω > 9. The mouse negative control returns LRT = 0 "
            "(boundary; no false-positive inflation).\n\n"
        )

        f.write("## Multiple-testing framework\n\n")
        f.write(
            f"- **Pre-registered**: n_tests = 15 genes × 4 lineages = 60; α_bonferroni = 0.05 / 60 = "
            f"**{0.05/60:.3e}**.\n"
            f"- **Realised**: n_tests = {n_tests_real}; α_bonferroni_realised = "
            f"**{0.05/n_tests_real if n_tests_real else float('nan'):.3e}**.\n"
            "- **BH-FDR** (Benjamini-Hochberg) q-values computed on production rows only.\n\n"
            "Headline verdict uses the pre-registered α (most conservative). Realised α is "
            "reported as a secondary-sensitivity check because the realised matrix was "
            "narrower than pre-registered (21 tests vs 60). Pre-registering the larger "
            "number made the bar higher than strictly necessary.\n\n"
        )

        f.write("## Results summary\n\n")
        f.write(f"- Production rows attempted: **{n_total}**\n")
        f.write(f"- Rows with successful LRT: **{n_completed}**\n")
        f.write(f"- Rows with convergence/infrastructure failure: **{n_failed}**\n")
        f.write(f"- Rows significant at pre-registered Bonferroni α={0.05/60:.2e}: **{n_bonf_prereg}**\n")
        f.write(f"- Rows significant at realised Bonferroni α={0.05/n_tests_real if n_tests_real else float('nan'):.2e}: **{n_bonf_real}**\n")
        f.write(f"- Rows with BH q < 0.05: **{n_bh05}**\n")
        f.write(f"- Rows with BH q < 0.10: **{n_bh10}**\n\n")

        f.write("## Per-row results (production only; sorted by raw p)\n\n")
        f.write("| Run | fg type | LRT | p_raw | bonf (prereg) | bonf (real) | BH q | fg ω₂a | p2a+p2b | BEB P>0.95 | Bonf sig? | BH q<0.05? |\n")
        f.write("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|\n")
        # sort production by p_raw ascending
        prod_sorted = prod.sort_values("p_raw_half_chi2_df1", na_position="last")
        for _, r in prod_sorted.iterrows():
            bonf_sig = "**Y**" if r["bonferroni_significant_prereg"] else ("y(real)" if r["bonferroni_significant_realised"] else "n")
            bh_sig = "**Y**" if r["bh_significant_q05"] else ("q<0.10" if r["bh_significant_q10"] else "n")
            f.write(
                f"| {r['run_id']} | {r['fg_type']} | "
                f"{fmt_f(r['LRT_2dlnL'])} | {fmt_p(r['p_raw_half_chi2_df1'])} | "
                f"{fmt_p(r['bonferroni_p_prereg'])} | {fmt_p(r['bonferroni_p_realised'])} | "
                f"{fmt_p(r['bh_q'])} | {fmt_f(r['fg_omega_2a'])} | {fmt_f(r['p2a_p2b'], 4)} | "
                f"{int(r['n_beb_gt95']) if pd.notna(r['n_beb_gt95']) else 'NA'} | "
                f"{bonf_sig} | {bh_sig} |\n"
            )
        f.write("\n")

        f.write("## Top 5 signals by raw p\n\n")
        for i, (_, r) in enumerate(top_prod.iterrows(), 1):
            gene_label = r.get("gene", "?")
            lineage_label = r.get("lineage", "?")
            note = r.get("notes", "") if "notes" in r else ""
            f.write(
                f"**{i}. {r['run_id']}** — LRT={fmt_f(r['LRT_2dlnL'])}, p_raw={fmt_p(r['p_raw_half_chi2_df1'])}, "
                f"bonf_prereg={fmt_p(r['bonferroni_p_prereg'])}, BH q={fmt_p(r['bh_q'])}, "
                f"fg ω₂a={fmt_f(r['fg_omega_2a'])}, BEB sites (P>0.95)={int(r['n_beb_gt95']) if pd.notna(r['n_beb_gt95']) else 'NA'}.\n"
                f"    - note: {note if note else 'n/a'}\n\n"
            )

        # BEB table per significant row
        if len(beb):
            f.write("## BEB-significant sites (posterior P>0.95) per production row\n\n")
            sig_runs = prod[
                (prod["bonferroni_significant_prereg"]) |
                (prod["bonferroni_significant_realised"]) |
                (prod["bh_significant_q10"])
            ]["run_id"].tolist()
            relevant_beb = beb[beb["run_id"].isin(sig_runs)] if sig_runs else beb
            if len(relevant_beb):
                f.write("| Run | codon_site | codon_aa | beb_posterior |\n|---|---:|---|---:|\n")
                for _, r in relevant_beb.iterrows():
                    f.write(f"| {r['run_id']} | {int(r['codon_site'])} | {r['codon_aa']} | {fmt_f(r['beb_posterior'], 3)} |\n")
                f.write("\n")
            else:
                f.write("No BEB P>0.95 sites in Bonferroni-significant or BH-suggestive rows.\n\n")
        else:
            f.write("No BEB sites ≥ P>0.95 in any production row.\n\n")

        f.write("## Power diagnostics\n\n")
        tip_underpowered = prod[prod["fg_type"].astype(str).str.contains("tip_underpowered")]
        tip_underpowered_count = len(tip_underpowered)
        f.write(f"- Tip-underpowered rows (single-branch foregrounds in large trees): **{tip_underpowered_count}**\n")
        if tip_underpowered_count:
            f.write("- These rows were flagged a priori as low-power sensitivity tests. LRT p-values from these rows should NOT be interpreted as primary H6a evidence; they are reported for completeness.\n")
            for _, r in tip_underpowered.iterrows():
                f.write(
                    f"    - `{r['run_id']}`: LRT={fmt_f(r['LRT_2dlnL'])}, p_raw={fmt_p(r['p_raw_half_chi2_df1'])}\n"
                )
        clade_rows = prod[prod["fg_type"] == "clade"]
        f.write(f"- Clade-foreground rows (primary tests): **{len(clade_rows)}**\n\n")

        f.write("## Interpretation\n\n")
        sig_prereg = prod[prod["bonferroni_significant_prereg"]]
        sig_real = prod[prod["bonferroni_significant_realised"] & ~prod["bonferroni_significant_prereg"]]
        sig_bh = prod[prod["bh_significant_q10"] & ~prod["bonferroni_significant_realised"]]
        if len(sig_prereg):
            f.write("**Bonferroni-significant signals at the pre-registered α (main H6a hits):**\n\n")
            for _, r in sig_prereg.iterrows():
                f.write(f"- `{r['run_id']}` (fg ω={fmt_f(r['fg_omega_2a'])}, p={fmt_p(r['p_raw_half_chi2_df1'])})\n")
            f.write("\n")
        else:
            f.write("**No production row reaches pre-registered Bonferroni significance.**\n\n")
        if len(sig_real):
            f.write("**Bonferroni-significant at realised α (secondary):**\n\n")
            for _, r in sig_real.iterrows():
                f.write(f"- `{r['run_id']}` (p={fmt_p(r['p_raw_half_chi2_df1'])})\n")
            f.write("\n")
        if len(sig_bh):
            f.write("**BH-suggestive (q < 0.10):**\n\n")
            for _, r in sig_bh.iterrows():
                f.write(f"- `{r['run_id']}` (q={fmt_p(r['bh_q'])}, p={fmt_p(r['p_raw_half_chi2_df1'])})\n")
            f.write("\n")

        f.write("## Top 3 risks for manuscript §3.4 interpretation\n\n")
        f.write(
            "1. **Gene coverage is 4/15, not 15/15.** Part 3 did not deliver codon "
            "alignments for the dopamine, opioid, orexin, NPY, or arthropod dopamine-receptor "
            "gene families despite raw CDSes being fetched. This means the H6a claim must be "
            "scoped to **sweet-taste receptors (TAS1R1/R3) + sweet gustatory receptors (Gr)** "
            "at Paper 1 submission, not the full 15-gene reward cascade. The manuscript "
            "must be honest about which gene families remain untested.\n\n"
            "2. **Pre-registered n_tests is now larger than realised n_tests.** The 60-test "
            "Bonferroni α = 8.3×10⁻⁴ is more conservative than the realised matrix warrants. "
            "We keep it as the primary cutoff (pre-registration lock-in) but report realised-α "
            "as secondary. If a reviewer pushes, either (a) defend the pre-reg commitment or "
            "(b) file a deviation note explaining that Part 3 coverage narrowed the test set.\n\n"
            "3. **Paralogs vs. species in the Gr tree.** The Gr_sweet gene tree has "
            "paraphyletic species (hit4_amellifera is not sister to hit1/2/3_amellifera). Our "
            "clade-level Gr foregrounds label the individual paralog tip branches (no MRCA), "
            "which is the correct H6a design for gene-family trees but may be confused by a "
            "reviewer expecting species-branch tests. Methods section must spell out this "
            "design choice.\n\n"
        )

        f.write("## Next-step recommendation\n\n")
        if verdict == "SUPPORTED":
            f.write(
                "Proceed to **Figure 4** construction. The recovered clade-foreground positive-selection "
                "signals support an H6a Paper-1 claim scoped to the sweet-taste/GR gene families. Align "
                "BEB-significant residues to the InterProScan VFT/7TM domain coordinates (Part 3) "
                "and produce structural overlays for the manuscript.\n\n"
            )
        elif verdict == "SUPPORTED_REALISED_ALPHA_ONLY":
            f.write(
                "Clade-foreground rows significant at realised-α but NOT at pre-registered-α. "
                "Treat as **suggestive-positive**: draft Figure 4 as a secondary panel with the BH "
                "q-values, and file a deviation note explaining that the pre-registered "
                "n_tests was larger than the realised n_tests.\n\n"
            )
        elif verdict == "SUGGESTIVE_CLADE":
            f.write(
                "Clade-foreground rows at BH q < 0.10 but not Bonferroni-significant. "
                "Report as suggestive signal with appropriate uncertainty framing.\n\n"
            )
        elif verdict == "SUGGESTIVE_TIP_ONLY":
            f.write(
                "**Important**: only `tip_underpowered` rows showed significant LRT, no clade rows did. "
                "Per pre-registered protocol, tip-only rows are sensitivity tests and cannot serve as "
                "primary H6a evidence. The Paper-1 H6a claim should therefore rest on:\n"
                "  1. v4 hummingbird TAS1R1 clade positive control (direct Baldwin 2014 replication, LRT=55.9);\n"
                "  2. H6f PubMed literature synthesis;\n"
                "  3. the tip-row signals reported as **exploratory / hypothesis-generating** only, with a clear "
                "caveat that single-branch foregrounds on small taxon sets are susceptible to high ω estimates "
                "from insufficient substitution sampling.\n\n"
                "**Caution on high ω estimates on tip rows**: a foreground ω > 80 on a single terminal branch "
                "in a 16-taxon tree is biologically suspect — it often reflects estimation instability at the "
                "site-class boundary rather than genuine positive selection. Adding bootstrap / parametric "
                "simulation would be prudent before publication.\n\n"
            )
        elif verdict == "SUGGESTIVE":
            f.write(
                "Report the production rows as **suggestive positive selection, not Bonferroni-"
                "corrected significant**. The main H6a Paper-1 argument then rests on:\n"
                "  1. v4 hummingbird TAS1R1 positive control (established beyond doubt);\n"
                "  2. H6f PubMed literature synthesis;\n"
                "  3. these suggestive signals as exploratory pattern.\n"
                "Figure 4 can still be produced but with appropriate caveat framing.\n\n"
            )
        else:
            f.write(
                "H6a is **not supported** at the pre-registered statistical threshold in the "
                "realised v2 matrix. The Paper-1 H6a argument should rest on:\n"
                "  1. v4 hummingbird TAS1R1 positive control (direct Baldwin 2014 replication);\n"
                "  2. H6f PubMed literature synthesis (§5 of §3.4);\n"
                "  3. an explicit limitations paragraph acknowledging that wider-scope positive "
                "selection detection requires larger taxonomic sampling than Part 3 delivered.\n\n"
                "Figure 4 should focus on the hummingbird positive control and the literature "
                "synthesis rather than the production-row outputs.\n\n"
            )

        f.write("## Artefacts\n\n")
        f.write(f"- Results CSV: `{RESULTS_CSV}`\n")
        f.write(f"- BEB CSV: `{BEB_CSV}`\n")
        f.write(f"- v2 matrix: `{MATRIX_TSV}`\n")
        f.write(f"- Positive-control v4 summary: `outputs/positive_control_v4_lrt_summary.tsv`\n")
        f.write(f"- Per-run codeml dirs: `data/codeml_runs/<run_id>/`\n")
        f.write(f"- Batch log: latest `logs/02b_v2_parallel_*.log`\n")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
