#!/usr/bin/env python
"""
05_h6f_triage_pilot.py
======================

Purpose
-------
Downsize the full PubMed harvest (~4,000 records from the 9-query library) to
a tight pilot hit list of ~80-150 records that the Week-2 screener will read
in full. The triage applies:
  (1) Per-phylum caps so no single phylum dominates.
  (2) Title-keyword filters that boost canonical signals (knockout, CRISPR,
      pharmacological, RNAi, mutant in title).
  (3) Year downweighting of older reviews (but retention of pre-2000 seminal
      papers flagged by our canonical-paper list).
  (4) Explicit inclusion of canonical anchor PMIDs regardless of triage rules.

Inputs
------
- outputs/H6f_pilot_hit_list.csv   (the full harvest from 04_*.py)

Outputs
-------
- outputs/H6f_full_harvest.csv       (renamed copy of input - never filtered)
- outputs/H6f_pilot_hit_list.csv     (OVERWRITTEN with triaged ~80-150 rows)
- outputs/H6f_phylum_coverage.md     (re-written with triaged counts)
- logs/05_h6f_triage_pilot_<ts>.log

Notes
-----
Triage rules are pre-registered in H6f_search_strategy.md §4 + §5. Canonical
anchor papers (e.g. Johnson-Kenny 2010 Drd2; de Bono 1998 NPR-1) are retained
regardless of the keyword filter. Screening at Week-2 uses the pilot list;
the full harvest remains available in H6f_full_harvest.csv for reservoir
sampling if the pilot yields insufficient included studies.
"""

from __future__ import annotations

import datetime as _dt
import logging
import re
import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs"
LOGS_DIR = ROOT / "logs"

FULL_CSV = OUT_DIR / "H6f_full_harvest.csv"
PILOT_CSV = OUT_DIR / "H6f_pilot_hit_list.csv"
COVERAGE_MD = OUT_DIR / "H6f_phylum_coverage.md"

# Canonical anchor PMIDs (verified via Entrez) - must remain in pilot
CANONICAL_ANCHORS = {
    "20348917": "Johnson PM & Kenny PJ 2010 Nat Neurosci - Drd2 palatable food rats",
    "9741632":  "de Bono M & Bargmann CI 1998 Cell - NPR-1 C. elegans social feeding",
    "25146290": "Baldwin MW et al. 2014 Science - TAS1R1 hummingbird sweet detection "
                "(biochem, not manipulation; retained for H6a positive-control reference)",
}

# Keyword boosters - rows whose title matches any of these are prioritised
# within each phylum bucket. Encoded as lowercase substrings (case-folded match).
TITLE_BOOST_TERMS = [
    "knockout", "knock-out", "knock out",
    "knockdown", "knock-down", "knock down",
    "crispr",
    "rnai", "rna interference",
    "pharmacological", "antagonist", "agonist",
    "mutant", "loss of function", "loss-of-function",
    "overexpress",
    "transgenic",
    "conditional",
    "viral vector",
    "receptor block",
    "genetic manipulation",
]

# Per-phylum pilot caps - ensure diversity across phyla
PHYLUM_CAPS = {
    "Chordata (rodent)": 35,
    "Chordata (non-rodent)": 10,
    "Arthropoda (Drosophila)": 15,
    "Arthropoda (Hymenoptera)": 15,
    "Nematoda": 15,
    "Mollusca": 15,
    "Cnidaria": 12,
    "cross-phylum": 8,
}  # total approx. 125, within 80-150 target


def setup_logging() -> Path:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    p = LOGS_DIR / f"05_h6f_triage_pilot_{stamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(p), logging.StreamHandler(sys.stdout)],
    )
    return p


def title_boost_score(title: str) -> int:
    """Count boost-term hits in title (case-insensitive). Zero if no title."""
    if not isinstance(title, str) or not title:
        return 0
    t = title.lower()
    return sum(1 for term in TITLE_BOOST_TERMS if term in t)


def year_weight(year_str: str) -> float:
    """Recent years and pre-2000 seminal years both get a weight bump. Mid-range
    (2005-2015) gets slight downweight so we dont over-harvest that dense era."""
    try:
        y = int(str(year_str)[:4])
    except Exception:
        return 0.5
    if y < 1998:
        return 0.9  # seminal pre-2000 (e.g. de Bono 1998)
    if 1998 <= y <= 2004:
        return 1.0
    if 2005 <= y <= 2015:
        return 0.85
    if y >= 2016:
        return 1.1  # recent CRISPR-era
    return 0.8


def main() -> int:
    setup_logging()
    if not PILOT_CSV.exists():
        logging.error("Input %s missing. Run 04_h6f_pubmed_harvest.py first.", PILOT_CSV)
        return 2

    # 1. Preserve full harvest (copy to _full_harvest.csv)
    shutil.copy(PILOT_CSV, FULL_CSV)
    logging.info("Archived full harvest -> %s (%d rows)",
                 FULL_CSV, len(pd.read_csv(FULL_CSV)))

    df = pd.read_csv(FULL_CSV)
    df["pubmed_id"] = df["pubmed_id"].astype(str)
    df["title"] = df["title"].fillna("")
    df["year"] = df["year"].fillna("").astype(str)
    df["phylum_bucket"] = df["phylum_candidate"].apply(
        lambda s: s.split(";")[0].strip()
    )

    # 2. Score rows
    df["title_boost"] = df["title"].apply(title_boost_score)
    df["year_weight"] = df["year"].apply(year_weight)
    df["triage_score"] = df["title_boost"] * df["year_weight"] + 0.3 * df["year_weight"]

    # Canonical anchors get maximum score
    df.loc[df["pubmed_id"].isin(CANONICAL_ANCHORS), "triage_score"] = 9999.0

    # 3. Drop obvious review articles (low priority unless canonical)
    is_review = df["pub_types"].fillna("").str.lower().str.contains("review")
    keep_review = df["pubmed_id"].isin(CANONICAL_ANCHORS)
    drop_reviews_mask = is_review & (~keep_review)
    n_review = drop_reviews_mask.sum()
    logging.info("Dropping %d reviews (non-canonical)", n_review)
    df = df.loc[~drop_reviews_mask]

    # 4. Per-bucket cap by triage score
    frames = []
    for bucket, cap in PHYLUM_CAPS.items():
        sub = df[df["phylum_bucket"] == bucket].copy()
        if sub.empty:
            logging.warning("Bucket '%s' has 0 rows", bucket)
            continue
        sub = sub.sort_values(["triage_score", "year"], ascending=[False, False])
        sub = sub.head(cap)
        frames.append(sub)
        logging.info("Bucket %-30s retained %d / cap=%d", bucket, len(sub), cap)

    pilot = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    # Ensure canonical anchors present even if their bucket was full
    for pid, note in CANONICAL_ANCHORS.items():
        if pid not in set(pilot["pubmed_id"]):
            row = df[df["pubmed_id"] == pid]
            if len(row) > 0:
                logging.info("Force-including canonical anchor %s (%s)", pid, note)
                pilot = pd.concat([pilot, row], ignore_index=True)

    pilot = pilot.drop_duplicates(subset="pubmed_id").sort_values(
        ["phylum_bucket", "year"], ascending=[True, False]
    )

    # 5. Add triage column (pending/boosted/canonical) for transparency
    pilot["triage"] = "pending"
    pilot.loc[pilot["pubmed_id"].isin(CANONICAL_ANCHORS), "triage"] = "canonical_anchor"
    pilot.loc[pilot["title_boost"] >= 1, "triage"] = pilot.apply(
        lambda r: "canonical_anchor" if r["pubmed_id"] in CANONICAL_ANCHORS
        else "boosted_by_title", axis=1
    )

    # 6. Write pilot
    # Order columns sensibly
    col_order = ["pubmed_id", "year", "journal", "phylum_candidate",
                 "phylum_bucket", "title", "authors_first3", "doi",
                 "query_label", "title_boost", "triage_score", "triage"]
    cols = [c for c in col_order if c in pilot.columns] + \
           [c for c in pilot.columns if c not in col_order]
    pilot = pilot[cols]
    pilot.to_csv(PILOT_CSV, index=False)
    logging.info("Wrote pilot %s (%d rows)", PILOT_CSV, len(pilot))

    # 7. Re-write coverage markdown
    coverage_lines = [
        "# H6f Phylum Coverage (triaged pilot)",
        "",
        f"Generated: {_dt.datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
        "## Triage process",
        "",
        "- Input: `outputs/H6f_full_harvest.csv` (raw PubMed harvest, 9 queries).",
        "- Filters applied (pre-registered in `H6f_search_strategy.md` §4):",
        "  1. Non-canonical review articles dropped.",
        "  2. Title-keyword boost for canonical manipulation terms (knockout, CRISPR, RNAi, pharmacological, mutant, etc.).",
        "  3. Year weighting: 1995-1998 seminal boost, 2005-2015 slight downweight, 2016+ recent-CRISPR boost.",
        "  4. Per-phylum caps ensuring no single bucket dominates (targets ~80-150 total).",
        "  5. Canonical anchor PMIDs force-included regardless of filter (Johnson-Kenny 2010; de Bono 1998; Baldwin 2014).",
        "",
        "## Triaged pilot counts by phylum bucket",
        "",
        "| Phylum bucket | Cap | Retained |",
        "|---------------|-----|----------|",
    ]
    for bucket, cap in PHYLUM_CAPS.items():
        n = int((pilot["phylum_bucket"] == bucket).sum())
        coverage_lines.append(f"| {bucket} | {cap} | {n} |")
    coverage_lines += [
        f"| **TOTAL** | ~125 | {len(pilot)} |",
        "",
        "## Coverage pre-registered thresholds",
        "",
        "- **Minimum (Paper 1 required):** >= 2 phyla with >= 5 studies each after full-text screening.",
        "- **Ideal:** 4 phyla with 3-10 coded experiments each.",
        "- Pilot-level phyla covered: "
        f"**{int(sum((pilot['phylum_bucket'] == b).sum() >= 5 for b in PHYLUM_CAPS.keys()))} buckets with >= 5 pilot entries**.",
        "",
        "## Canonical anchor inclusion verification",
        "",
    ]
    for pid, note in CANONICAL_ANCHORS.items():
        present = pid in set(pilot["pubmed_id"].astype(str))
        coverage_lines.append(f"- PMID {pid} [{'INCLUDED' if present else 'MISSING'}] : {note}")
    coverage_lines += [
        "",
        "## Week-2 workflow",
        "",
        "1. Each pilot row gets title + abstract triage: `include_candidate`, `exclude_review`, `exclude_not_manipulation`, `exclude_not_reward_receptor`, `exclude_human_only`, `unclear_needs_fulltext`.",
        "2. `unclear` + `include_candidate` rows proceed to full-text.",
        "3. Coding uses `H6f_extraction_template.csv` schema.",
        "4. 20% double-coding for kappa.",
        "5. If final included N < 30 or < 3 phyla, sample additional rows from `H6f_full_harvest.csv` by dropping the phylum cap on the under-represented bucket(s).",
        "",
        "## Notes on cnidarian coverage",
        "",
        "- Cnidaria bucket is shallow (~20 raw hits). Full-text attrition likely leaves 0-2 usable cases.",
        "- **Planned supplementation:** manual harvest from Layden & Martindale (2014) *Nematostella* neuropeptide literature + Anderson et al. 2020 jellyfish behavioural reviews via reference-list trawl.",
        "- If Cnidaria ends with 0 coded experiments, H6f falls back to 3-phylum coverage (Chordata + Arthropoda + Nematoda) which still passes the minimum threshold.",
    ]
    COVERAGE_MD.write_text("\n".join(coverage_lines))
    logging.info("Wrote %s", COVERAGE_MD)

    logging.info("DONE: pilot has %d rows across %d phylum buckets",
                 len(pilot), pilot["phylum_bucket"].nunique())
    return 0


if __name__ == "__main__":
    sys.exit(main())
