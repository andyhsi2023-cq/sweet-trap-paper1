#!/usr/bin/env python
"""
03_multiple_testing_v2.py
=========================

Aggregate Week-2 v2 production run results. Collects:
  - LRT + p from each codeml run dir (lrt_stats.tsv)
  - BEB site posteriors from alt rst file
  - Foreground omega estimates from alt_init{05,15}_mlc.out

Applies multiple-testing correction using BOTH:
  - Pre-registered n_tests = 15 genes * 4 lineages = 60 (alpha=8.33e-4)
  - Realised n_tests (actual number of completed non-control tests)

Outputs:
  outputs/branch_site_results.csv    - per-run stats + corrections
  outputs/branch_site_beb_sites.csv  - BEB site table
  outputs/h6a_production_run_report.md - narrative report
"""
from __future__ import annotations

import datetime as _dt
import logging
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
RUNS = ROOT / "data" / "codeml_runs"
OUT = ROOT / "outputs"
LOGS = ROOT / "logs"
MATRIX = ROOT / "scripts" / "branch_site_test_matrix_v2.tsv"

# v2 run_ids (21 production rows) + 3 v4 control rows to re-verify
V2_RUN_IDS = [
    # TAS1R1 on v4 16-taxon alignment
    "TAS1R1__mammalia_clade_v4",
    "TAS1R1__rodentia_clade_v4",
    "TAS1R1__homo_tip_v4",
    "TAS1R1__gallus_tip_v4",
    "TAS1R1__danio_tip_v4",
    "TAS1R1__passeriformes_tip_v4",
    "TAS1R1__apus_tip_v4",
    # TAS1R3 5-taxon
    "TAS1R3__mammalia_clade",
    "TAS1R3__rodentia_clade",
    "TAS1R3__homo_tip",
    "TAS1R3__gallus_tip",
    "TAS1R3__danio_tip",
    # TAS1R1 5-taxon cross-reference
    "TAS1R1__mammalia_clade_p3",
    # Gr_sweet 38-insect gene tree
    "Gr_sweet__dmel_Gr64_cluster",
    "Gr_sweet__amellifera_clade",
    "Gr_sweet__lepidoptera_clade",
    "Gr_sweet__coleoptera_clade",
    "Gr_sweet__aaegypti_clade",
    "Gr_sweet__dmel_all_clade",
    "Gr_sweet__Gr5a_tip",
    "Gr_sweet__Gr64a_tip",
]

CONTROL_RUN_IDS = [
    "TAS1R1_pc_v4__apodiformes_clade",   # positive control — Apodiformes clade (Baldwin 2014 design)
    "TAS1R1_pc_v4__hummingbirds_clade",  # positive control — crown hummingbirds
    "TAS1R1_pc_v4__mouse_control",       # negative control — mouse tip
]

ALL_ROWS = CONTROL_RUN_IDS + V2_RUN_IDS

# Pre-registered multiple-testing design
N_GENES = 15
N_LINEAGES = 4
N_PREREG = N_GENES * N_LINEAGES  # 60
ALPHA_PREREG = 0.05 / N_PREREG    # 8.33e-4


def parse_lrt_stats(run_dir: Path) -> dict:
    f = run_dir / "lrt_stats.tsv"
    if not f.exists():
        return {"run_id": run_dir.name, "status": "no_stats"}
    df = pd.read_csv(f, sep="\t")
    row = df.iloc[0].to_dict()
    # Normalise column names: controls (written by positive_control_v4_run) use
    # LRT / p_half; production (written by 02_run_branch_site.sh) uses
    # LRT_2dlnL / p_raw_half_chi2_df1.
    if "LRT" in row and "LRT_2dlnL" not in row:
        row["LRT_2dlnL"] = row["LRT"]
    if "p_half" in row and "p_raw_half_chi2_df1" not in row:
        row["p_raw_half_chi2_df1"] = row["p_half"]
    row["status"] = "ok"
    return row


def parse_beb(run_dir: Path, threshold: float = 0.95) -> list[dict]:
    """Parse BEB-significant positive-selection sites from the best alt mlc file.

    codeml's branch-site Model A alt run writes:
        Bayes Empirical Bayes (BEB) analysis (Yang, Wong & Nielsen 2005...)
        Positive sites for foreground lineages Prob(w>1):
            90 H 0.994**
           357 E 1.000**

    Only lines where the posterior P(w>1) >= threshold are kept. The
    `*` / `**` suffix matters only cosmetically (0.95*, 0.99**).
    """
    # Pick the alt mlc with the highest lnL (mirrors best-init choice)
    best_file = None
    best_lnL = None
    for candidate in ["alt_init05_mlc.out", "alt_init15_mlc.out", "alt_mlc.out"]:
        fp = run_dir / candidate
        if not fp.exists():
            continue
        text = fp.read_text()
        m = re.search(r"^lnL.*?(-\d+\.\d+)", text, flags=re.M)
        if not m:
            continue
        lnL = float(m.group(1))
        if best_lnL is None or lnL > best_lnL:
            best_lnL = lnL
            best_file = fp
    if best_file is None:
        return []
    text = best_file.read_text()
    # Find the 'Positive sites for foreground lineages Prob(w>1):' block
    m = re.search(
        r"Bayes Empirical Bayes.*?Positive sites for foreground[^\n]*\n(.*?)(?=\n\n)",
        text, flags=re.S,
    )
    if not m:
        return []
    block = m.group(1)
    rows = []
    for line in block.splitlines():
        # Pattern: optional leading WS, integer, space, single AA (A-Z) OR '-', space, posterior, optional stars
        mm = re.match(r"\s+(\d+)\s+(-|[A-Z])\s+([0-9.]+)(\*{0,2})\s*$", line)
        if mm:
            pp = float(mm.group(3))
            if pp >= threshold:
                rows.append({
                    "codon_site": int(mm.group(1)),
                    "codon_aa": mm.group(2),
                    "beb_posterior": pp,
                    "sig_mark": mm.group(4),
                })
    return rows


def parse_alt_omega(run_dir: Path) -> dict:
    """Extract foreground omega_2a from best alt mlc file."""
    best_lnL = None
    best_fg_w = None
    best_p2ab = None
    for candidate in ["alt_init05_mlc.out", "alt_init15_mlc.out", "alt_mlc.out"]:
        fp = run_dir / candidate
        if not fp.exists():
            continue
        text = fp.read_text()
        # lnL line
        m = re.search(r"^lnL.*?(-\d+\.\d+)", text, flags=re.M)
        if not m:
            continue
        lnL = float(m.group(1))
        if best_lnL is None or lnL > best_lnL:
            best_lnL = lnL
            # Parse foreground omega (site class 2a/2b)
            # "foreground w  0.1185  1.0000  9.3783  9.3783"
            m2 = re.search(r"foreground w\s+[0-9.]+\s+[0-9.]+\s+([0-9.]+)",
                           text)
            best_fg_w = float(m2.group(1)) if m2 else np.nan
            # Proportion of sites in class 2a+2b
            # "proportion   0.69866  0.28574  0.01107  0.00453"
            m3 = re.search(r"proportion\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)",
                           text)
            if m3:
                p2a = float(m3.group(3))
                p2b = float(m3.group(4))
                best_p2ab = p2a + p2b
            else:
                best_p2ab = np.nan
    return {"fg_omega_2a": best_fg_w, "p2a_p2b": best_p2ab}


def build_results() -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    beb_rows = []
    matrix_df = pd.read_csv(MATRIX, sep="\t")
    matrix_lookup = {
        f"{r['gene']}__{r['lineage_key']}": r for _, r in matrix_df.iterrows()
    }
    for run_id in ALL_ROWS:
        run_dir = RUNS / run_id
        stats = parse_lrt_stats(run_dir)
        if stats.get("status") == "no_stats":
            rows.append({
                "run_id": run_id,
                "status": "no_stats",
            })
            continue
        # metadata
        meta = matrix_lookup.get(run_id, {})
        is_control = run_id in CONTROL_RUN_IDS
        if is_control:
            if "apodiformes_clade" in run_id:
                fg_type_meta = "positive_control_clade"
                gene = "TAS1R1"
                lineage = "apodiformes_clade_v4_pc"
            elif "hummingbirds_clade" in run_id:
                fg_type_meta = "positive_control_clade"
                gene = "TAS1R1"
                lineage = "hummingbirds_clade_v4_pc"
            elif "mouse_control" in run_id:
                fg_type_meta = "negative_control_tip"
                gene = "TAS1R1"
                lineage = "mouse_control_v4_pc"
            else:
                fg_type_meta = "control"
                gene = "TAS1R1"
                lineage = run_id.split("__", 1)[-1]
        else:
            fg_type_meta = meta.get("fg_type", "unknown") if hasattr(meta, "get") else "unknown"
            gene = meta.get("gene") if hasattr(meta, "get") else run_id.split("__")[0]
            lineage = meta.get("lineage_key") if hasattr(meta, "get") else run_id.split("__", 1)[-1]
        omega = parse_alt_omega(run_dir)

        # BEB
        beb_hits = parse_beb(run_dir, threshold=0.95)
        for h in beb_hits:
            h["run_id"] = run_id
            h["gene"] = gene
            h["lineage"] = lineage
            beb_rows.append(h)

        # Normalise keys (stats may be float-dtypes)
        row = {
            "run_id": run_id,
            "gene": gene,
            "lineage": lineage,
            "fg_type": fg_type_meta,
            "role": "control" if is_control else "production",
            "lnL_null": stats.get("lnL_null"),
            "lnL_alt_best": stats.get("lnL_alt_best"),
            "LRT_2dlnL": stats.get("LRT_2dlnL"),
            "p_raw_half_chi2_df1": stats.get("p_raw_half_chi2_df1"),
            "fg_omega_2a": omega.get("fg_omega_2a"),
            "p2a_p2b": omega.get("p2a_p2b"),
            "n_beb_gt95": len(beb_hits),
            "status": "ok",
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    beb_df = pd.DataFrame(beb_rows) if beb_rows else pd.DataFrame(
        columns=["run_id", "gene", "lineage", "codon_site", "codon_aa",
                 "beb_posterior", "sig_mark"])

    return df, beb_df


def apply_corrections(df: pd.DataFrame) -> pd.DataFrame:
    # Separate realised n (production rows only, excluding controls)
    prod_mask = (df["role"] == "production") & (df["status"] == "ok") & df["p_raw_half_chi2_df1"].notna()
    n_realised = int(prod_mask.sum())
    alpha_realised = 0.05 / n_realised if n_realised else np.nan

    df["n_tests_prereg"] = N_PREREG
    df["alpha_prereg"] = ALPHA_PREREG
    df["n_tests_realised"] = n_realised
    df["alpha_realised"] = alpha_realised

    df["bonferroni_p_prereg"] = df["p_raw_half_chi2_df1"].apply(
        lambda p: min(p * N_PREREG, 1.0) if pd.notna(p) else np.nan)
    df["bonferroni_p_realised"] = df["p_raw_half_chi2_df1"].apply(
        lambda p: min(p * n_realised, 1.0) if (pd.notna(p) and n_realised) else np.nan)

    # BH q-values on the PRODUCTION subset only (controls excluded to avoid
    # biasing the discovery rate).
    prod_idx = df.index[prod_mask].tolist()
    prod_p = df.loc[prod_idx, "p_raw_half_chi2_df1"].values
    if len(prod_p) > 0:
        order = np.argsort(prod_p)
        ranks = np.empty_like(order)
        ranks[order] = np.arange(1, len(prod_p) + 1)
        q = prod_p * len(prod_p) / ranks
        # Monotonic: ensure q is non-decreasing when sorted by p
        sorted_q = q[order]
        for i in range(len(sorted_q) - 2, -1, -1):
            sorted_q[i] = min(sorted_q[i], sorted_q[i + 1])
        sorted_q = np.minimum(sorted_q, 1.0)
        q_monotone = np.empty_like(sorted_q)
        q_monotone[order] = sorted_q
        df["bh_q"] = np.nan
        df.loc[prod_idx, "bh_q"] = q_monotone
    else:
        df["bh_q"] = np.nan

    df["bonferroni_significant_prereg"] = (
        df["bonferroni_p_prereg"].notna() & (df["bonferroni_p_prereg"] < 0.05)
    )
    df["bonferroni_significant_realised"] = (
        df["bonferroni_p_realised"].notna() & (df["bonferroni_p_realised"] < 0.05)
    )
    df["bh_significant_q05"] = df["bh_q"].notna() & (df["bh_q"] < 0.05)
    df["bh_significant_q10"] = df["bh_q"].notna() & (df["bh_q"] < 0.10)

    return df


def main() -> int:
    LOGS.mkdir(exist_ok=True, parents=True)
    OUT.mkdir(exist_ok=True, parents=True)
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS / f"03_multiple_testing_v2_{stamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler(sys.stdout)],
        force=True,
    )
    logging.info("03_multiple_testing_v2 starting")
    df, beb_df = build_results()
    logging.info("Collected %d run rows, %d BEB sites (P>0.95)", len(df), len(beb_df))

    df = apply_corrections(df)
    df.to_csv(OUT / "branch_site_results.csv", index=False)
    beb_df.to_csv(OUT / "branch_site_beb_sites.csv", index=False)
    logging.info("Wrote branch_site_results.csv and branch_site_beb_sites.csv")

    prod = df[df["role"] == "production"]
    logging.info("Production rows: n=%d completed=%d",
                 len(prod), int(prod["p_raw_half_chi2_df1"].notna().sum()))
    bonf_prereg = prod["bonferroni_significant_prereg"].sum()
    bonf_real = prod["bonferroni_significant_realised"].sum()
    bh05 = prod["bh_significant_q05"].sum()
    bh10 = prod["bh_significant_q10"].sum()
    logging.info("Bonferroni-prereg significant: %d", int(bonf_prereg))
    logging.info("Bonferroni-realised significant: %d", int(bonf_real))
    logging.info("BH q<0.05: %d   BH q<0.10: %d", int(bh05), int(bh10))

    return 0


if __name__ == "__main__":
    sys.exit(main())
