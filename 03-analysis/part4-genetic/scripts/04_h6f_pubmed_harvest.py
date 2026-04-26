#!/usr/bin/env python
"""
04_h6f_pubmed_harvest.py
=========================

Purpose
-------
Execute the H6f pre-registered PubMed query library (per `outputs/H6f_search_strategy.md`)
and emit a deduplicated pilot hit list for Week-2 full-text screening. Each row
carries its source query label, PMID, title, journal, year, a phylum candidate
tag (derived from the query label), and a triage placeholder.

Inputs
------
- Hard-coded query library below (identical to the text of H6f_search_strategy.md §3).

Outputs
-------
- outputs/H6f_pilot_hit_list.csv        : deduplicated hits with phylum_candidate + triage
- outputs/H6f_phylum_coverage.md        : per-phylum coverage summary
- outputs/H6f_raw_hits_<query>.tsv      : one file per query, raw PubMed returns
- logs/04_h6f_pubmed_harvest_<timestamp>.log

Dependencies
------------
- Biopython (Bio.Entrez)
- pandas

Policy
------
- Polite Entrez usage: max 3 req/s (default), retmax ceiling per query = 600.
- NEVER fabricate PMIDs. If Entrez fails, leave blank and log the exception.
- DOI harvested only if PubMed esummary returns one; missing DOIs logged.
- Titles are exact-match to PubMed; no paraphrasing.

Usage
-----
  python 04_h6f_pubmed_harvest.py                   # full harvest
  python 04_h6f_pubmed_harvest.py --max-per-query 50  # throttle
  python 04_h6f_pubmed_harvest.py --only-query Q-cnidarian
"""

from __future__ import annotations

import argparse
import datetime as _dt
import logging
import re
import sys
import time
from pathlib import Path

import pandas as pd

# ---- Entrez setup ----
ENTREZ_EMAIL = "sweettrap-paper@example.edu"  # replaced with author email post-submission
DELAY_BETWEEN_QUERIES_SEC = 0.4  # polite throttle

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs"
LOGS_DIR = ROOT / "logs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# Query library (verbatim from H6f_search_strategy.md §3)
# ----------------------------------------------------------------------
#
# Phylum-candidate tags assigned per query; these propagate into the CSV's
# phylum_candidate column. Downstream title/abstract screening replaces these
# with verified phylum + class after full-text extraction.
#
# We intentionally keep the query strings close to the spec document. The
# enclosing [LA] and [dp] filters are appended programmatically so the core
# boolean is auditable against the markdown.

QUERIES: dict[str, dict] = {
    "Q-vertebrate-rodent": {
        "phylum_candidate": "Chordata (rodent)",
        "query": (
            '(knockout[tiab] OR "knock-out"[tiab] OR knockdown[tiab] OR "knock-down"[tiab] '
            'OR CRISPR[tiab] OR "pharmacological blockade"[tiab] OR "receptor antagonist"[tiab] '
            'OR "conditional deletion"[tiab] OR siRNA[tiab] OR antisense[tiab] '
            'OR "D2 receptor"[tiab] OR "D1 receptor"[tiab] OR "receptor blockade"[tiab] '
            'OR overexpression[tiab] OR "transgenic"[tiab] OR "viral vector"[tiab] '
            'OR "knock in"[tiab] OR "dopamine agonist"[tiab]) '
            'AND ("taste receptor"[tiab] OR "sweet receptor"[tiab] OR Tas1r[tiab] OR T1R[tiab] '
            'OR "dopamine receptor"[tiab] OR "dopamine D1"[tiab] OR "dopamine D2"[tiab] '
            'OR "dopamine D3"[tiab] OR "dopamine D4"[tiab] OR "dopamine D5"[tiab] '
            'OR Drd1[tiab] OR Drd2[tiab] OR Drd3[tiab] OR Drd4[tiab] OR Drd5[tiab] '
            'OR "mu opioid"[tiab] OR "opioid receptor"[tiab] OR Oprm1[tiab] OR Oprk1[tiab] '
            'OR Oprd1[tiab] OR "kappa opioid"[tiab] OR "delta opioid"[tiab] '
            'OR "orexin receptor"[tiab] OR "hypocretin"[tiab] OR Hcrtr[tiab] '
            'OR "NPY receptor"[tiab] OR "neuropeptide Y"[tiab] OR Npy1r[tiab] OR Npy2r[tiab] OR Npy5r[tiab]) '
            'AND (mouse[tiab] OR mice[tiab] OR rat[tiab] OR rats[tiab] OR rodent[tiab] '
            'OR "Mus musculus"[tiab] OR Rattus[tiab]) '
            'AND (behavior[tiab] OR behaviour[tiab] OR preference[tiab] OR "food intake"[tiab] '
            'OR "reward seeking"[tiab] OR "self-administration"[tiab] OR sucrose[tiab] '
            'OR palatable[tiab] OR addiction[tiab] OR anhedonia[tiab] OR feeding[tiab] '
            'OR "compulsive eating"[tiab] OR obesity[tiab] OR "reward dysfunction"[tiab])'
        ),
    },
    "Q-vertebrate-primate-other": {
        "phylum_candidate": "Chordata (non-rodent)",
        "query": (
            '(knockout[tiab] OR knockdown[tiab] OR CRISPR[tiab] OR "receptor antagonist"[tiab] '
            'OR siRNA[tiab] OR "pharmacological blockade"[tiab]) '
            'AND ("taste receptor"[tiab] OR Tas1r[tiab] OR "dopamine receptor"[tiab] '
            'OR Drd2[tiab] OR "mu opioid"[tiab] OR Oprm1[tiab] OR "orexin receptor"[tiab] '
            'OR Hcrtr[tiab] OR "NPY receptor"[tiab]) '
            'AND (primate[tiab] OR macaque[tiab] OR Macaca[tiab] OR marmoset[tiab] '
            'OR zebrafish[tiab] OR "Danio rerio"[tiab] '
            'OR hummingbird[tiab] OR songbird[tiab] OR Gallus[tiab]) '
            'AND (preference[tiab] OR behavior[tiab] OR behaviour[tiab] OR feeding[tiab] '
            'OR reward[tiab])'
        ),
    },
    "Q-arthropod-drosophila": {
        "phylum_candidate": "Arthropoda (Drosophila)",
        "query": (
            '("UAS-RNAi"[tiab] OR Gal4[tiab] OR CRISPR[tiab] OR "P-element"[tiab] '
            'OR "knock-in"[tiab] OR knockdown[tiab] OR pharmacological[tiab]) '
            'AND (DopR[tiab] OR Dop1R[tiab] OR Dop2R[tiab] OR DopEcR[tiab] '
            'OR Gr5a[tiab] OR Gr64[tiab] OR Gr43a[tiab] OR "gustatory receptor"[tiab] '
            'OR "opioid-like"[tiab] OR dNPF[tiab] OR "NPF receptor"[tiab] OR "orexin-like"[tiab]) '
            'AND (Drosophila[tiab] OR "fruit fly"[tiab] OR melanogaster[tiab]) '
            'AND (preference[tiab] OR feeding[tiab] OR sugar[tiab] OR ethanol[tiab] '
            'OR cocaine[tiab] OR reward[tiab] OR valence[tiab])'
        ),
    },
    "Q-arthropod-bee": {
        "phylum_candidate": "Arthropoda (Hymenoptera)",
        "query": (
            '(RNAi[tiab] OR siRNA[tiab] OR pharmacological[tiab] OR knockdown[tiab] '
            'OR CRISPR[tiab]) '
            'AND (Amel[tiab] OR "Apis mellifera"[tiab] OR "honey bee"[tiab] '
            'OR honeybee[tiab] OR bumblebee[tiab] OR Bombus[tiab]) '
            'AND (gustatory[tiab] OR "sucrose response"[tiab] OR PER[tiab] '
            'OR "proboscis extension"[tiab] OR dopamine[tiab] OR octopamine[tiab] '
            'OR "reward learning"[tiab] OR foraging[tiab])'
        ),
    },
    "Q-nematode": {
        "phylum_candidate": "Nematoda",
        "query": (
            '(knockout[tiab] OR mutant[tiab] OR "loss-of-function"[tiab] OR RNAi[tiab] '
            'OR CRISPR[tiab] OR "natural variant"[tiab] OR polymorphism[tiab] OR allele[tiab]) '
            'AND ("C. elegans"[tiab] OR Caenorhabditis[tiab] OR nematode[tiab]) '
            'AND ("npr-1"[tiab] OR "NPR-1"[tiab] OR DOP-1[tiab] OR DOP-2[tiab] OR DOP-3[tiab] '
            'OR dop-1[tiab] OR dop-2[tiab] OR dop-3[tiab] '
            'OR cat-2[tiab] OR NPF[tiab] OR "neuropeptide"[tiab] '
            'OR "octopamine receptor"[tiab] OR tyramine[tiab] OR dopamine[tiab]) '
            'AND (feeding[tiab] OR aggregation[tiab] OR "social feeding"[tiab] '
            'OR chemotaxis[tiab] OR preference[tiab] OR reward[tiab] OR "food choice"[tiab])'
        ),
    },
    "Q-mollusc": {
        "phylum_candidate": "Mollusca",
        "query": (
            '(Aplysia[tiab] OR Lymnaea[tiab] OR Biomphalaria[tiab] OR octopus[tiab] '
            'OR cuttlefish[tiab] OR squid[tiab]) '
            'AND (dopamine[tiab] OR reward[tiab] OR learning[tiab] OR feeding[tiab] '
            'OR memory[tiab]) '
            'AND (manipulation[tiab] OR knockdown[tiab] OR RNAi[tiab] OR injection[tiab] '
            'OR pharmacological[tiab] OR lesion[tiab] OR "receptor block"[tiab])'
        ),
    },
    "Q-cnidarian": {
        "phylum_candidate": "Cnidaria",
        "query": (
            '(Hydra[tiab] OR Nematostella[tiab] OR "sea anemone"[tiab] OR cnidarian[tiab] '
            'OR jellyfish[tiab]) '
            'AND (dopamine[tiab] OR neuropeptide[tiab] OR "chemical cue"[tiab] '
            'OR feeding[tiab] OR preference[tiab]) '
            'AND (knockdown[tiab] OR morpholino[tiab] OR RNAi[tiab] OR CRISPR[tiab] '
            'OR pharmacological[tiab])'
        ),
    },
    "Q-supernormal-manipulation": {
        "phylum_candidate": "cross-phylum",
        "query": (
            '("supernormal stimul*"[tiab] OR "sensory trap"[tiab] '
            'OR "signal exploitation"[tiab] OR "evolutionary trap"[tiab]) '
            'AND (receptor[tiab] OR gene[tiab] OR manipulation[tiab]) '
            'AND (behavior[tiab] OR preference[tiab])'
        ),
    },
    "Q-reward-fitness-decoupling": {
        "phylum_candidate": "cross-phylum",
        "query": (
            '("reward-fitness"[tiab] OR "maladaptive reward"[tiab] '
            'OR "hedonic overconsumption"[tiab]) '
            'AND (receptor[tiab] OR knockout[tiab] OR manipulation[tiab] '
            'OR pharmacological[tiab])'
        ),
    },
}

DATE_FILTER = ' AND ("1995/01/01"[DP] : "2026/04/30"[DP])'
# Note: H6f scope doc pre-registered 2000-2026 as the declarative window for
# included-in-summary-table papers; we broaden the harvest floor to 1995 to
# ensure canonical pre-2000 work (e.g. de Bono & Bargmann 1998 Cell) enters
# the pilot hit list for PRISMA-transparent exclusion at screening, rather
# than being invisible to the search. Final inclusion decision respects the
# 2000-2026 rule unless the coding team flags a seminal case.
LANG_FILTER = ' AND English[LA]'
TYPE_FILTER = ' AND ("Journal Article"[PT] OR "Review"[PT])'


def setup_logging() -> Path:
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS_DIR / f"04_h6f_pubmed_harvest_{stamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler(sys.stdout)],
    )
    return log_path


def esearch(query: str, retmax: int = 600) -> list[str]:
    from Bio import Entrez
    Entrez.email = ENTREZ_EMAIL
    handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
    rec = Entrez.read(handle)
    handle.close()
    return list(rec.get("IdList", []))


def esummary(pmids: list[str]) -> list[dict]:
    """Fetch summary records in batches of 100."""
    from Bio import Entrez
    Entrez.email = ENTREZ_EMAIL
    rows: list[dict] = []
    BATCH = 100
    for i in range(0, len(pmids), BATCH):
        sub = pmids[i : i + BATCH]
        handle = Entrez.esummary(db="pubmed", id=",".join(sub))
        try:
            summaries = Entrez.read(handle)
        finally:
            handle.close()
        for s in summaries:
            rows.append({
                "pubmed_id": str(s.get("Id", "")),
                "title": str(s.get("Title", "")),
                "journal": str(s.get("Source", "")),
                "year": str(s.get("PubDate", "")).split(" ")[0],
                "doi": str(s.get("DOI", "")),
                "authors_first3": "; ".join(list(s.get("AuthorList", []))[:3]),
                "pub_types": ";".join([str(x) for x in s.get("PubTypeList", [])]),
            })
        time.sleep(DELAY_BETWEEN_QUERIES_SEC)
    return rows


def phylum_from_query_label(label: str) -> str:
    return QUERIES[label]["phylum_candidate"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max-per-query", type=int, default=600)
    ap.add_argument("--only-query", default=None,
                    help="Run a single query label (e.g. Q-cnidarian).")
    args = ap.parse_args()

    log_path = setup_logging()
    logging.info("H6f PubMed harvest starting. Log: %s", log_path)
    logging.info("Queries in library: %d", len(QUERIES))

    query_labels = [args.only_query] if args.only_query else list(QUERIES.keys())

    all_rows: list[dict] = []
    per_query_counts: dict[str, dict] = {}

    for label in query_labels:
        q_spec = QUERIES[label]
        full_query = q_spec["query"] + DATE_FILTER + LANG_FILTER + TYPE_FILTER
        logging.info("---- %s ----", label)
        logging.info("Phylum candidate: %s", q_spec["phylum_candidate"])
        try:
            pmids = esearch(full_query, retmax=args.max_per_query)
        except Exception as exc:  # noqa: BLE001
            logging.exception("esearch failed for %s: %s", label, exc)
            per_query_counts[label] = {"raw_hits": 0, "error": str(exc)}
            continue
        logging.info("  raw hits (capped at %d): %d", args.max_per_query, len(pmids))
        if not pmids:
            per_query_counts[label] = {"raw_hits": 0}
            continue

        try:
            summaries = esummary(pmids)
        except Exception as exc:  # noqa: BLE001
            logging.exception("esummary failed for %s: %s", label, exc)
            per_query_counts[label] = {"raw_hits": len(pmids), "summary_error": str(exc)}
            continue

        for row in summaries:
            row["query_label"] = label
            row["phylum_candidate"] = q_spec["phylum_candidate"]
            row["triage"] = "pending"  # Week-2 screening fills this
            all_rows.append(row)

        per_query_counts[label] = {"raw_hits": len(pmids), "retained_summaries": len(summaries)}

        # Write per-query raw file
        perq_df = pd.DataFrame([r for r in summaries])
        perq_df["query_label"] = label
        perq_path = OUT_DIR / f"H6f_raw_hits_{label}.tsv"
        perq_df.to_csv(perq_path, sep="\t", index=False)
        logging.info("  wrote %s (%d rows)", perq_path, len(perq_df))

        time.sleep(DELAY_BETWEEN_QUERIES_SEC)

    # --- Deduplicate by pubmed_id ---
    df = pd.DataFrame(all_rows)
    if df.empty:
        logging.warning("No hits at all; aborting downstream aggregation.")
        return 1

    df_before = len(df)
    # Keep the first query_label occurrence but aggregate labels into a list
    df_agg = (
        df.groupby("pubmed_id", as_index=False)
          .agg({
              "title": "first",
              "journal": "first",
              "year": "first",
              "doi": "first",
              "authors_first3": "first",
              "pub_types": "first",
              "query_label": lambda s: "; ".join(sorted(set(s))),
              "phylum_candidate": lambda s: "; ".join(sorted(set(s))),
              "triage": "first",
          })
    )
    df_agg = df_agg.sort_values(["phylum_candidate", "year"], ascending=[True, False])

    pilot_csv = OUT_DIR / "H6f_pilot_hit_list.csv"
    df_agg.to_csv(pilot_csv, index=False)
    logging.info("Deduplicated pilot: %d rows (from %d raw)", len(df_agg), df_before)
    logging.info("Wrote %s", pilot_csv)

    # --- Phylum coverage summary ---
    coverage_path = OUT_DIR / "H6f_phylum_coverage.md"
    coverage_lines = [
        "# H6f Phylum Coverage (pre-screening pilot)",
        "",
        f"Generated: {_dt.datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
        "## Per-query raw hit counts",
        "",
        "| Query | Phylum candidate | Raw hits | Retained summaries |",
        "|-------|------------------|----------|--------------------|",
    ]
    for label, q_spec in QUERIES.items():
        cnts = per_query_counts.get(label, {})
        coverage_lines.append(
            f"| {label} | {q_spec['phylum_candidate']} | "
            f"{cnts.get('raw_hits', 0)} | {cnts.get('retained_summaries', 0)} |"
        )

    # Unique PMIDs by primary phylum bucket (first candidate label)
    def primary_phylum(p_str: str) -> str:
        # Collapse cross-phylum / composite entries
        first = p_str.split(";")[0].strip()
        # Drop the parenthetical refinement for bucket counts
        return re.sub(r"\s*\(.*?\)", "", first)

    df_agg["phylum_bucket"] = df_agg["phylum_candidate"].apply(primary_phylum)
    bucket_counts = df_agg["phylum_bucket"].value_counts().to_dict()

    coverage_lines += [
        "",
        "## Deduplicated PMID counts by primary phylum bucket",
        "",
        "| Phylum bucket | Unique PMIDs |",
        "|---------------|---------------|",
    ]
    for bucket, n in sorted(bucket_counts.items(), key=lambda x: -x[1]):
        coverage_lines.append(f"| {bucket} | {n} |")

    coverage_lines += [
        "",
        "## Pre-registered coverage thresholds (H6f)",
        "",
        "- Minimum: >= 2 phyla with >= 5 studies each (pilot level). Headline needs",
        "  >= 3 phyla after full-text screening to pass H6f phylum-coverage criterion.",
        "- Ideal: 4 phyla with 3-10 studies each.",
        "",
        "## Interpretation gates (from H6f_search_strategy.md)",
        "",
        "- These are RAW + SUMMARY counts pre-screening. Expected attrition ratio",
        "  raw->included ~ 5%-15% per previous meta-analytic practice (Hale &",
        "  Swearer 2016).",
        "- Cnidarian row is expected to be near-empty; if it is, we will supplement",
        "  manually from Layden & Martindale (2014 Nematostella NPs), and from",
        "  ordered Anderson et al. 2020 jellyfish reviews via reference-list harvest.",
    ]
    coverage_path.write_text("\n".join(coverage_lines))
    logging.info("Wrote %s", coverage_path)

    logging.info("DONE. pilot=%d unique PMIDs across %d phylum buckets.",
                 len(df_agg), len(bucket_counts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
