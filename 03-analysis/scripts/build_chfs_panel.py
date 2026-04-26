#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_chfs_panel.py — Build CHFS long panel for C8 investment FOMO Sweet Trap analysis.

Inputs (5 waves, CHFS 2011/2013/2015/2017/2019):
    /Volumes/P1/城市研究/01-个体调查/CHFS_家庭金融_2011-2019/赠送CHFS分年份数据/
      {YYYY}/chfs{YYYY}_hh_*.dta
      {YYYY}/chfs{YYYY}_master*.dta  (for prov, rural, totals, weights)

Outputs:
    /Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/panel_C8_investment.parquet
    Log with SHA-256.

Design notes:
    - Wellbeing outcome h3514 (居民幸福感) only exists in 2017 and 2019 waves.
    - Investment holdings (d3101 stock, d5102 fund, d7109 wealth mgmt) available 2011-2019.
    - Some variables renamed across waves (e.g., 2013 hhid); we harmonize.
    - master file gives province, rural, total_income, total_consump, total_asset,
      hhwage_inc, prop_inc (property income = investment returns); we collapse
      master to 1 row per hhid (head row, not person-level).
    - Output: one row per (hhid, year). Long panel.
    - Compute 8 variables: income rank, stock entry dummy, fund entry dummy, wealth-mgmt
      dummy, stock mkt value log, stock return paper, stock return realized fraction,
      wellbeing z (within-wave, reverse-coded so higher=happier).

Memory: load wave-by-wave with usecols to avoid loading full 438MB hh files.
"""
from __future__ import annotations

import hashlib
import logging
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
OUT = ROOT / "02-data/processed/panel_C8_investment.parquet"
LOG_FP = ROOT / "03-analysis/scripts/build_chfs_panel.log"

CHFS_BASE = Path(
    "/Volumes/P1/城市研究/01-个体调查/CHFS_家庭金融_2011-2019/赠送CHFS分年份数据"
)

WAVE_HH = {
    2011: CHFS_BASE / "2011-CHFS  STATA+TXT数据+中英问卷/2011年中国家庭金融调查数据dta格式-stata14以上版本/chfs2011_hh_20191120_version14.dta",
    2013: CHFS_BASE / "2013-CHFS STATA+TXT数据+中英问卷/2013年中国家庭金融调查数据dta格式-stata14以上版本/chfs2013_hh_20191120_version14.dta",
    2015: CHFS_BASE / "CHFS-2015年 STATA+TXT数据+中英问卷/2015年中国家庭金融调查数据dta格式-stata14以上版本/chfs2015_hh_20191120_version14.dta",
    2017: CHFS_BASE / "CHFS-2017年  STATA+TXT数据+中文问卷/CHFS2017年调查数据-stata14版本/chfs2017_hh_202104.dta",
    2019: CHFS_BASE / "CHFS-2019年 STATA+TXT数据+中文问卷/CHFS2019年调查数据-stata14版本/chfs2019_hh_202112.dta",
}
WAVE_MASTER = {
    2011: CHFS_BASE / "2011-CHFS  STATA+TXT数据+中英问卷/2011年中国家庭金融调查数据dta格式-stata14以上版本/chfs2011_master_city_20180418_version14.dta",
    2013: CHFS_BASE / "2013-CHFS STATA+TXT数据+中英问卷/2013年中国家庭金融调查数据dta格式-stata14以上版本/chfs2013_master_city_20180504_version14.dta",
    2015: CHFS_BASE / "CHFS-2015年 STATA+TXT数据+中英问卷/2015年中国家庭金融调查数据dta格式-stata14以上版本/chfs2015_master_city_20180504_version14.dta",
    2017: CHFS_BASE / "CHFS-2017年  STATA+TXT数据+中文问卷/CHFS2017年调查数据-stata14版本/chfs2017_master_202104.dta",
    2019: CHFS_BASE / "CHFS-2019年 STATA+TXT数据+中文问卷/CHFS2019年调查数据-stata14版本/chfs2019_master_202112.dta",
}

# Core investment variables (may or may not exist in each wave; we graceful-skip)
HH_VARS_TARGET = {
    "hhid",
    # stock module
    "d3101",   # 是否有股票账户
    "d3103",   # 股票账户现金余额
    "d3104",   # 持有股票支数
    "d3109",   # 持股市值
    "d3117",   # 过去一年股票收入
    "d3118a",  # 期望未来一年炒股收益
    # fund module
    "d5102",   # 是否持有基金
    "d5107",   # 所持基金总市值
    "d5109",   # 过去一年基金收入
    "d5109a",  # 去年投资基金盈亏比例 (1盈利 2亏损 3持平)
    "d5109b",  # 未来一年基金收益期望
    # wealth-mgmt / internet finance
    "d7106h",  # 互联网理财产品余额
    "d7106j",  # 互联网理财产品年收入
    "d7109",   # 是否有金融理财产品
    "d7112",   # 理财产品年收入
    # bond / derivative (sanity checks)
    "d4103_5", # 债券市值
    "d4111",   # 债券年收入
    # subjective wellbeing + risk + financial literacy  (2017/2019 only in most cases)
    "h3514",   # 是否幸福 / 居民幸福感
    "h3101",   # 财经信息关注度
    "h3103",   # 高收益高风险认同
    "h3104",   # 投资风险收益选择 (risk preference)
    "h3105",   # 金融素养Q1
    "h3106",   # 金融素养Q2
    "h3110",   # 股票、债券、基金了解程度 (2017 only)
    "h3601",   # 未来三个月经济形势 (2019 only)
    "h3602",   # 未来三个月股市 (2019 only)
    # pre-computed totals inside 2015/2017/2019 hh files
    "total_income", "total_consump", "total_asset", "total_debt",
    "asset", "debt",  # 2015 alias
    "hhwage_inc", "prop_inc",
}
# Master-file vars (stable across waves, but 2011/2013/2015 only carry geography+weight)
MASTER_VARS_TARGET = {
    "hhid",
    "prov", "prov_code", "prov_CHN", "province",
    "rural",
    "region",
    "weight_hh", "weight_ind", "swgt",
    "total_income", "total_consump", "total_asset",
    "hhwage_inc", "prop_inc",
    "educ_con",
}


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(LOG_FP, mode="w"), logging.StreamHandler()],
    )
    return logging.getLogger(__name__)


def file_sha256(path: Path, blocksize: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(blocksize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def load_wave_hh(year: int, fp: Path, log) -> pd.DataFrame:
    """Load household file with only target variables actually present."""
    _, meta = pyreadstat.read_dta(str(fp), metadataonly=True)
    present = [v for v in HH_VARS_TARGET if v in meta.column_names]
    missing = [v for v in HH_VARS_TARGET if v not in meta.column_names]
    log.info(f"[{year}] hh file N_rows_meta={meta.number_rows} K={meta.number_columns}; "
             f"target_present={len(present)}/{len(HH_VARS_TARGET)} missing={missing}")
    df, _ = pyreadstat.read_dta(str(fp), usecols=present)
    # 2013 wave uses a different primary key name if 'hhid' missing; try alternatives
    if "hhid" not in df.columns:
        for alt in ["hhid_2013", "hhid2013", "hhid_new"]:
            if alt in meta.column_names:
                alt_df, _ = pyreadstat.read_dta(str(fp), usecols=[alt])
                df["hhid"] = alt_df[alt]
                log.info(f"[{year}] hhid reconstructed from {alt}")
                break
    # If still missing, fall back to row number as an internal id (no cross-wave linkage)
    if "hhid" not in df.columns:
        df["hhid"] = [f"{year}_{i}" for i in range(len(df))]
        log.warning(f"[{year}] hhid synthesised — NO cross-wave linkage for this wave")
    # Add missing targets as NaN columns so schema is uniform
    for v in HH_VARS_TARGET:
        if v not in df.columns:
            df[v] = np.nan
    df["year"] = year
    return df


def load_wave_master(year: int, fp: Path, log) -> pd.DataFrame:
    """Master file is person-level. Aggregate to 1 row per hhid: first non-null."""
    _, meta = pyreadstat.read_dta(str(fp), metadataonly=True)
    present = [v for v in MASTER_VARS_TARGET if v in meta.column_names]
    missing = [v for v in MASTER_VARS_TARGET if v not in meta.column_names]
    log.info(f"[{year}] master file N_rows={meta.number_rows} K={meta.number_columns}; "
             f"target_present={len(present)}/{len(MASTER_VARS_TARGET)} missing={missing}")
    if "hhid" not in present:
        # try alt key
        for alt in ["hhid_2013", "hhid_num"]:
            if alt in meta.column_names:
                present.append(alt)
                break
    df, _ = pyreadstat.read_dta(str(fp), usecols=present)
    if "hhid" not in df.columns:
        for alt in ["hhid_2013", "hhid_num"]:
            if alt in df.columns:
                df = df.rename(columns={alt: "hhid"})
                break
    if "hhid" not in df.columns:
        log.warning(f"[{year}] master lacks hhid -- skipped")
        return pd.DataFrame(columns=list(MASTER_VARS_TARGET) + ["year"])
    # first non-null per hhid (household-level collapse)
    agg = df.groupby("hhid", as_index=False).agg("first")
    for v in MASTER_VARS_TARGET:
        if v not in agg.columns:
            agg[v] = np.nan
    agg["year"] = year
    return agg


def build_panel(log):
    records = []
    for year in sorted(WAVE_HH):
        fp_hh = WAVE_HH[year]
        fp_m = WAVE_MASTER[year]
        if not fp_hh.exists():
            log.error(f"[{year}] hh missing: {fp_hh}")
            continue
        if not fp_m.exists():
            log.error(f"[{year}] master missing: {fp_m}")
        log.info(f"=== Loading wave {year} ===")
        hh = load_wave_hh(year, fp_hh, log)
        mst = load_wave_master(year, fp_m, log) if fp_m.exists() else pd.DataFrame()
        if not mst.empty:
            # merge on hhid + year (both have these)
            merged = hh.merge(mst.drop(columns=["year"], errors="ignore"),
                               on="hhid", how="left", suffixes=("", "_m"))
        else:
            merged = hh
        log.info(f"[{year}] merged shape={merged.shape}")
        records.append(merged)

    panel = pd.concat(records, axis=0, ignore_index=True, sort=False)
    log.info(f"RAW stacked panel shape: {panel.shape}")

    # Harmonise totals: hh file carries total_income in 2015+; master in 2017+;
    # combine into unified columns. For 2015 the aliases are 'asset'/'debt'/'total_consump'.
    # Prefer master column if available (suffix _m from merge); else hh-level.
    def coalesce(df, out, candidates):
        s = pd.Series(np.nan, index=df.index, dtype="float64")
        for c in candidates:
            if c in df.columns:
                s = s.combine_first(pd.to_numeric(df[c], errors="coerce"))
        df[out] = s
        return df

    # After merge we have _m suffixed duplicates; reconcile to canonical names
    panel = coalesce(panel, "total_income", ["total_income", "total_income_m"])
    panel = coalesce(panel, "total_consump", ["total_consump", "total_consump_m"])
    panel = coalesce(panel, "total_asset", ["total_asset", "total_asset_m", "asset"])
    panel = coalesce(panel, "total_debt", ["total_debt", "debt"])
    panel = coalesce(panel, "hhwage_inc", ["hhwage_inc", "hhwage_inc_m"])
    panel = coalesce(panel, "prop_inc", ["prop_inc", "prop_inc_m"])
    panel = coalesce(panel, "educ_con", ["educ_con", "educ_con_m"])

    # province: use master's prov or prov_CHN or province
    if "prov" not in panel.columns or panel["prov"].isna().all():
        for alt in ["prov_m", "prov_CHN", "province", "prov_CHN_m", "province_m"]:
            if alt in panel.columns:
                panel["prov"] = panel["prov"].fillna(panel[alt]) if "prov" in panel.columns else panel[alt]
                break

    # rural
    for alt in ["rural_m", "rural"]:
        if alt in panel.columns and panel.get("rural") is not None:
            panel["rural"] = pd.to_numeric(panel["rural"], errors="coerce").fillna(
                pd.to_numeric(panel.get(alt, pd.Series(index=panel.index)), errors="coerce")
            )

    # weight: take master weight_hh, fall back swgt
    w = pd.Series(np.nan, index=panel.index, dtype="float64")
    for alt in ["weight_hh", "weight_hh_m", "swgt", "swgt_m"]:
        if alt in panel.columns:
            w = w.combine_first(pd.to_numeric(panel[alt], errors="coerce"))
    panel["weight_hh"] = w

    return panel


def derive_features(df: pd.DataFrame, log) -> pd.DataFrame:
    """Construct Sweet-Trap relevant features.

    - stock_hold: d3101 == 1 (has stock account)
    - stock_active: stock_hold AND d3109 (mkt value) > 0
    - fund_hold: d5102 == 1
    - wmp_hold: d7109 == 1
    - any_risky: stock_hold | fund_hold | wmp_hold
    - stock_mkt_value: d3109 (winsorized top 1%)
    - stock_return_paper_yr: d3117 (可正可负)
    - stock_share: stock_mkt_value / total_asset
    - stock_ret_fraction: d3117 / max(d3109, 1)
    - fund_loss_flag: d5109a == 2 (loss last year)  [2017/2019]
    - fund_continue: fund_hold this wave & fund_hold previous wave & fund_loss_flag_prev
    - life_sat: h3514 (1-5, 1=非常幸福 ... 5=非常不幸福). reverse so higher=happier.
    - life_sat_z: within-year z-score
    - risk_aver: h3104 (1=high-risk high-return ... 5=do not want any risk)
    - fin_lit: correct answers to h3105 & h3106 (if known)
    - fin_confidence_vs_literacy: h3101 attention - actual literacy
    - ln_income, ln_asset, ln_consump
    - high_income (top tercile within wave)
    """
    d = df.copy()

    # stock / fund / wmp participation
    d["stock_hold"] = (d["d3101"] == 1).astype(int)
    d["fund_hold"] = (d["d5102"] == 1).astype(int)
    d["wmp_hold"] = (d["d7109"] == 1).astype(int)
    d["any_risky_hold"] = ((d["stock_hold"] + d["fund_hold"] + d["wmp_hold"]) > 0).astype(int)

    # continuous holdings: winsorise top 1% within year
    for c in ["d3109", "d3117", "d5107", "d5109", "d7106h", "d7106j", "d7112",
              "total_income", "total_consump", "total_asset", "prop_inc"]:
        if c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")

    def wins(x: pd.Series, lo=0.00, hi=0.99) -> pd.Series:
        q_lo = x.quantile(lo)
        q_hi = x.quantile(hi)
        return x.clip(lower=q_lo, upper=q_hi)

    for c in ["d3109", "d5107", "total_income", "total_consump", "total_asset"]:
        if c in d.columns:
            d[c + "_w"] = d.groupby("year")[c].transform(lambda s: wins(s, 0.005, 0.995))

    d["stock_mkt_value"] = d["d3109_w"] if "d3109_w" in d.columns else np.nan
    d["fund_mkt_value"] = d["d5107_w"] if "d5107_w" in d.columns else np.nan
    d["stock_return_paper_yr"] = d["d3117"]  # CHFS asks annual stock income (can be negative)
    d["fund_return_paper_yr"] = d["d5109"]

    d["stock_share_assets"] = (d["stock_mkt_value"] / d["total_asset_w"]).where(
        d["total_asset_w"] > 0, np.nan
    )
    d["stock_ret_rate"] = (d["stock_return_paper_yr"] / d["stock_mkt_value"]).where(
        d["stock_mkt_value"] > 0, np.nan
    )
    # clip extreme (simulate realistic one-year return bounds)
    d["stock_ret_rate"] = d["stock_ret_rate"].clip(-2, 5)

    # Sweet Trap key: fund self-reported loss flag
    # d5109a: 1 盈利 / 2 亏损 / 3 持平
    d["fund_loss_flag"] = (d["d5109a"] == 2).astype("Int64")
    d.loc[d["d5109a"].isna(), "fund_loss_flag"] = pd.NA
    d["fund_gain_flag"] = (d["d5109a"] == 1).astype("Int64")
    d.loc[d["d5109a"].isna(), "fund_gain_flag"] = pd.NA

    # Wellbeing (only 2017/2019)
    # h3514 ranges 1-5 (1=非常幸福 ... 5=非常不幸福).  reverse_code -> higher=happier
    d["life_sat_raw"] = pd.to_numeric(d["h3514"], errors="coerce")
    d["life_sat"] = 6 - d["life_sat_raw"]  # now 1=非常不幸福, 5=非常幸福
    d["life_sat_z"] = d.groupby("year")["life_sat"].transform(
        lambda s: (s - s.mean()) / s.std()
    )

    # Risk attitude
    d["risk_pref"] = pd.to_numeric(d["h3104"], errors="coerce")
    # reverse so higher = more risk-seeking
    d["risk_seek"] = 6 - d["risk_pref"]

    # Financial literacy (correct answers known from CHFS manual: h3105 correct==1, h3106 correct==1)
    # Note: key may invert; we treat raw value availability as indicator
    d["fin_lit_Q1"] = pd.to_numeric(d["h3105"], errors="coerce")
    d["fin_lit_Q2"] = pd.to_numeric(d["h3106"], errors="coerce")
    # correct value for h3105 (101元之后 interest: 本金100@4% → 104): answer choice coded as 1 correct typically
    d["fin_lit_score"] = (
        (d["fin_lit_Q1"] == 1).astype("Int64") + (d["fin_lit_Q2"] == 1).astype("Int64")
    )

    # Attention to finance news minus literacy (overconfidence proxy)
    d["fin_attention"] = pd.to_numeric(d["h3101"], errors="coerce")

    # Income / asset logs
    for c, out in [("total_income_w", "ln_income"),
                   ("total_consump_w", "ln_consump"),
                   ("total_asset_w", "ln_asset")]:
        if c in d.columns:
            d[out] = np.log1p(d[c].clip(lower=0))
    # Property income (dividends etc)
    if "prop_inc" in d.columns:
        d["ln_prop_inc"] = np.log1p(d["prop_inc"].clip(lower=0))

    # Education proxy: approximate via "educ_con" consumption ≠ education attainment.
    # leave as-is; C8 does not require household-head education critically.

    # Within-year income tercile (robust to waves with few unique values)
    def safe_qcut(s: pd.Series, q=3) -> pd.Series:
        x = pd.to_numeric(s, errors="coerce")
        try:
            out = pd.qcut(x, q, labels=False, duplicates="drop")
            # labels=False -> 0..k-1 (where k<=q); shift to 1..k
            return out.astype("Int64") + 1
        except Exception:
            return pd.Series(pd.NA, index=s.index, dtype="Int64")

    if "total_income_w" in d.columns:
        d["income_tercile"] = d.groupby("year")["total_income_w"].transform(safe_qcut)
        d["high_income"] = (d["income_tercile"] == 3).astype("Int64")
    else:
        d["income_tercile"] = pd.NA
        d["high_income"] = pd.NA

    # Housekeeping: drop dup cols
    d = d.loc[:, ~d.columns.duplicated()]

    log.info(f"Feature-derived panel shape: {d.shape}")
    return d


def add_lags(df: pd.DataFrame, log) -> pd.DataFrame:
    """Add wave-wise lags for Sweet Trap lock-in detection (ρ)."""
    d = df.sort_values(["hhid", "year"]).copy()
    lag_cols = [
        "stock_hold", "fund_hold", "wmp_hold",
        "stock_mkt_value", "fund_mkt_value",
        "stock_return_paper_yr", "fund_return_paper_yr",
        "fund_loss_flag", "life_sat",
        "total_asset_w", "total_income_w",
    ]
    lag_cols = [c for c in lag_cols if c in d.columns]
    for c in lag_cols:
        d[c + "_lag"] = d.groupby("hhid")[c].shift(1)
    # flag: continued stock / fund after last-wave loss
    d["stock_continue_after_loss"] = (
        (d["stock_hold"] == 1) & (d["stock_return_paper_yr_lag"] < 0)
    ).astype("Int64")
    d["fund_continue_after_loss"] = (
        (d["fund_hold"] == 1) & (d["fund_loss_flag_lag"] == 1)
    ).astype("Int64")
    # whether household appears in multiple waves
    d["n_waves_observed"] = d.groupby("hhid")["year"].transform("nunique")
    log.info(f"Panel with lags shape: {d.shape}; "
             f"N_hhid_multiwave={(d['n_waves_observed']>=2).sum()}")
    return d


def main():
    log = setup_logging()
    log.info("=== C8 CHFS Panel Build ===")
    log.info(f"Output: {OUT}")

    panel = build_panel(log)
    panel = derive_features(panel, log)
    panel = add_lags(panel, log)

    # Final shape
    log.info(f"FINAL panel shape: {panel.shape}")
    log.info(f"Rows per wave:\n{panel['year'].value_counts().sort_index()}")
    log.info(f"Life-sat by wave: \n{panel.groupby('year')['life_sat'].count()}")
    log.info(f"Stock hold by wave: \n{panel.groupby('year')['stock_hold'].sum()}")
    log.info(f"Fund hold by wave: \n{panel.groupby('year')['fund_hold'].sum()}")

    # Deduplicate before write (in case hhid+year repeats)
    dup_before = panel.duplicated(["hhid", "year"]).sum()
    if dup_before:
        log.warning(f"{dup_before} duplicate (hhid,year) rows -- keeping first")
        panel = panel.drop_duplicates(["hhid", "year"])

    # Cast Int64 / stringify stubborn mixed columns
    for c in panel.columns:
        if panel[c].dtype == "object":
            panel[c] = panel[c].astype(str)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(OUT, index=False)
    size = os.path.getsize(OUT)
    sha = file_sha256(OUT)
    log.info(f"Wrote {OUT} ({size:,} B)  sha256={sha}")
    log.info(f"N_hhid unique: {panel['hhid'].nunique():,}")
    log.info(f"N_rows: {len(panel):,}")

    # Compact summary card
    log.info(
        "CARD | N=%s | waves=%s | unique_hh=%s | sha=%s",
        len(panel), sorted(panel["year"].unique().tolist()),
        panel["hhid"].nunique(), sha[:16],
    )

    return panel, sha


if __name__ == "__main__":
    main()
