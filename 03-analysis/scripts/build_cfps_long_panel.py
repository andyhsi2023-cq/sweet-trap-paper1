#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_cfps_long_panel.py
=========================

Stage 2 sweet-trap-multidomain: CFPS 2010-2022 long-panel cleaning pipeline.
This is the SINGLE data entry point for all 5 focal domains' PDE analyses.

Inputs
------
  /Volumes/P1/城市研究/CFPS2010-2022清洗好数据/2010-2022cfps非平衡面板数据(stata_推荐使用）.dta
    shape: 86,294 person-years x 204 columns, waves 2010/2012/2014/2016/2018/2020/2022

Outputs
-------
  02-data/processed/cfps_long_panel.parquet
    Full cleaned person-year long panel with all 5-domain variables + common
    covariates + lambda proxies + derived binary indicators.

  02-data/processed/panel_D{1,2,3,5,8}.parquet
    Five "analysis-ready" subsets (overlapping), one per focal domain, with
    filter rules per domain spec sheet (domain_selection_matrix.md §3).

  02-data/linkage/variable_dict.csv
    Variable name / original CFPS label / recoding rule / role in this study.

  02-data/linkage/cfps_cleaning.log
    Full row-by-row cleaning log (rule applied, counts changed).

  00-design/pde/D0_data_cleaning_diagnostics.md
    Diagnostic report (year-coverage, N by domain, missingness, Tier confirmation).

Design principles
-----------------
  - Read the Stata dta ONCE (86K x 204 fits in memory on M5 Pro 24GB).
  - Do not modify source file (P1 is read-only).
  - All cleaning rules logged with before/after counts for audit trail.
  - Derived variables (overtime_48h, mortgage_burden, etc.) are computed
    centrally here so each domain PDE uses the same definition.
  - Likert reverse-coding applied where needed to standardize direction.
  - n_workers = 1 (no parallelism needed for in-memory work on 86K rows).

Author: Claude (sweet-trap-multidomain Stage 2 D0)
Date:   2026-04-17
Spec:   00-design/domain_selection_matrix.md §3 (per-domain spec sheets)
        00-design/cfps_variable_inventory.md (variable audit, Tier ratings)
        HANDOFF.md (task card for D0)
"""

from __future__ import annotations

import datetime as _dt
import json
import logging
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat

# ----------------------------------------------------------------------------
# 0. Paths & constants
# ----------------------------------------------------------------------------

REPO = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
P1_DTA = Path(
    "/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/"
    "2010-2022cfps非平衡面板数据(stata_推荐使用）.dta"
)

OUT_PARQUET_DIR = REPO / "02-data" / "processed"
OUT_LINKAGE_DIR = REPO / "02-data" / "linkage"
OUT_DESIGN_DIR = REPO / "00-design" / "pde"
OUT_PARQUET_DIR.mkdir(parents=True, exist_ok=True)
OUT_LINKAGE_DIR.mkdir(parents=True, exist_ok=True)
OUT_DESIGN_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUT_LINKAGE_DIR / "cfps_cleaning.log"

# CFPS missing-value codes. CFPS uses negative codes for different flavors
# of non-response. We coerce all of them to np.nan BEFORE any analysis.
# -1: don't know / refuse / not applicable (most common)
# -2: refuse
# -3: ???
# -8: wave-not-applicable (variable not collected this wave)
# -9: missing generic
# -10: structural skip
CFPS_MISSING_CODES = [-1, -2, -3, -8, -9, -10]

# ----------------------------------------------------------------------------
# 1. Logging
# ----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("cfps_panel")


# ----------------------------------------------------------------------------
# 2. Variable inventory — domain tag + role + recoding rule
# ----------------------------------------------------------------------------
# Each dict entry: column -> (role, recoding_rule, short_description)
# "role" ∈ {key, covariate, lambda_proxy, sweet_DV, treatment, bitter_outcome,
#           wealth, macro_context}
# "recoding_rule" is a short human-readable description; the actual logic
# is applied in clean_variable() / derive_variables() below.

VARIABLE_DICT = {
    # ------------------------------------------------------ 2.0 keys & frame
    "pid":      ("key", "none",             "个人 ID (financial respondent)"),
    "year":     ("key", "none",             "survey wave (2010-2022 biennial)"),
    "fid10":    ("key", "none",             "2010 household ID (for linkage)"),
    # ------------------------------------------------------ 2.1 demographic
    "age":      ("covariate",   "missing_codes_to_nan", "age in years"),
    "gender":   ("covariate",   "recode_1male_0female", "gender (0=female,1=male)"),
    "gen":      ("covariate",   "duplicate_of_gender",  "alt gender (1=male,0=female)"),
    "eduy":     ("covariate",   "missing_codes_to_nan", "years of schooling"),
    "educ":     ("covariate",   "missing_codes_to_nan", "completed education category"),
    "edu":      ("covariate",   "missing_codes_to_nan", "education level code"),
    "marrige":  ("covariate",   "recode_1married_0other","marital status"),
    "mar":      ("covariate",   "duplicate_of_marrige", "alt marital status"),
    "hukou":    ("lambda_proxy","recode_1rural_0urban", "hukou rural=1"),
    "rural":    ("lambda_proxy","duplicate_of_hukou",   "rural hukou dummy"),
    "res":      ("lambda_proxy","duplicate_of_hukou",   "hukou legacy field"),
    "communist":("lambda_proxy","recode_binary",        "CCP member"),
    "minzu":    ("covariate",   "recode_1han_0other",   "Han ethnicity"),
    "familysize":("covariate",  "missing_codes_to_nan", "household size"),
    "fml":      ("covariate",   "duplicate_familysize", "alt household size"),
    "size":     ("covariate",   "duplicate_familysize", "alt household size"),
    "child_num":("covariate",   "missing_codes_to_nan", "# minors in household"),
    "child_p":  ("covariate",   "missing_codes_to_nan", "child dependency ratio"),
    "elder_num":("covariate",   "missing_codes_to_nan", "# elders in household"),
    "child_gender":("lambda_proxy","recode_binary",     "first-child gender (1=male)"),
    "medsure_dum":("covariate", "recode_binary",        "has medical insurance"),
    # ------------------------------------------------------ 2.2 geography
    "provcd":   ("covariate",   "keep_raw",             "province code"),
    "city":     ("covariate",   "keep_raw",             "city admin code"),
    "code":     ("covariate",   "keep_raw",             "county admin code"),
    "provname": ("covariate",   "keep_raw",             "province name"),
    "cityname": ("covariate",   "keep_raw",             "city name"),
    "urban":    ("lambda_proxy","recode_binary",        "NBS urban classification"),
    # ------------------------------------------------------ 2.3 income / expense (logs)
    "lnincome": ("covariate",   "missing_codes_to_nan", "log total family income"),
    "lnconsume":("covariate",   "missing_codes_to_nan", "log total family expense"),
    "fincome1": ("covariate",   "missing_codes_to_nan", "total net family income"),
    "fincome1_per":("covariate","missing_codes_to_nan", "per capita family income"),
    "income_p": ("covariate",   "missing_codes_to_nan", "per capita family income (alt)"),
    "expense":  ("covariate",   "missing_codes_to_nan", "total family expense"),
    "expense_p":("covariate",   "missing_codes_to_nan", "per capita family expense"),
    "pce":      ("covariate",   "missing_codes_to_nan", "household consumption aggregate"),
    # ------------------------------------------------------ 2.4 D1 URBAN
    "qn12012":  ("sweet_DV",    "likert_1to5",          "life satisfaction (primary sweet DV)"),
    "qn12016":  ("sweet_DV",    "likert_1to5",          "confidence in future"),
    "qn1101":   ("covariate",   "likert_1to5_cap79",    "county govt evaluation"),
    # ------------------------------------------------------ 2.5 D2 EDUCATION/鸡娃
    "eexp":     ("treatment",   "missing_codes_to_nan", "education expenditure (family)"),
    "school":   ("treatment",   "missing_codes_to_nan", "tutoring/training expenditure"),
    "eec":      ("treatment",   "missing_codes_to_nan", "culture/education/entertainment expense"),
    "qn10021":  ("covariate",   "range_0to10",          "trust in parents (intergenerational)"),
    # ------------------------------------------------------ 2.6 D3 996/work
    "workhour": ("treatment",   "missing_codes_to_nan", "weekly work hours"),
    "gongzi":   ("sweet_DV",    "missing_codes_to_nan", "monthly after-tax wage"),
    "fwage":    ("covariate",   "missing_codes_to_nan", "family wage income"),
    "wage":     ("lambda_proxy","missing_codes_to_nan", "individual wage"),
    "jobclass": ("covariate",   "missing_codes_to_nan", "job class code"),
    "worknature":("covariate",  "recode_binary",        "job nature"),
    "workplace":("lambda_proxy","missing_codes_to_nan", "work location (migrant proxy)"),
    "industry": ("covariate",   "missing_codes_to_nan", "industry code"),
    "bianzhi":  ("covariate",   "recode_binary",        "编制 (state-sector employment)"),
    "job":      ("covariate",   "recode_binary",        "currently working"),
    "agri":     ("covariate",   "recode_binary",        "agri employment"),
    "qg401":    ("sweet_DV",    "likert_1to5",          "job-income satisfaction"),
    "qg402":    ("sweet_DV",    "likert_1to5",          "job-safety satisfaction"),
    "qg403":    ("sweet_DV",    "likert_1to5",          "job-environment satisfaction"),
    "qg404":    ("sweet_DV",    "likert_1to5",          "job-time satisfaction"),
    "qg405":    ("sweet_DV",    "likert_1to5_cap79",    "job-promotion satisfaction"),
    "qg406":    ("sweet_DV",    "likert_1to5",          "overall job satisfaction (primary D3 DV)"),
    "qq4010":   ("bitter_outcome","hours_range",        "sleep hours per day"),
    # ------------------------------------------------------ 2.7 D5 DIET/HEALTH
    "food":     ("treatment",   "missing_codes_to_nan", "food expenditure"),
    "dress":    ("covariate",   "missing_codes_to_nan", "clothing expenditure"),
    "daily":    ("covariate",   "missing_codes_to_nan", "household-goods expenditure"),
    "mexp":     ("bitter_outcome","missing_codes_to_nan","medical expenditure"),
    "med":      ("covariate",   "missing_codes_to_nan", "medical expenditure (alt)"),
    "health":   ("bitter_outcome","likert_1to5",        "self-rated health (1=worst)"),
    "unhealth": ("bitter_outcome","recode_binary",      "poor health 0/1"),
    "weak":     ("bitter_outcome","missing_codes_to_nan","# unhealthy in family"),
    "qp401":    ("bitter_outcome","recode_binary",      "chronic disease past 6 months"),
    "qq201":    ("covariate",   "recode_binary",        "smoked past month"),
    # ------------------------------------------------------ 2.8 D8 HOUSING/STATUS
    "dw":       ("sweet_DV",    "likert_1to5",          "self-rated social status (primary D8 DV)"),
    "resivalue":("treatment",   "missing_codes_to_nan", "current home value (wan yuan)"),
    "house":    ("covariate",   "missing_codes_to_nan", "housing expenditure"),
    "mortage":  ("treatment",   "missing_codes_to_nan", "mortgage payment (typo preserved from CFPS)"),
    "mor":      ("treatment",   "missing_codes_to_nan", "mortgage (alt label, 2020-2022)"),
    "h_loan":   ("lambda_proxy","recode_binary",        "has housing debt 0/1"),
    "house_debts":("bitter_outcome","missing_codes_to_nan","total housing debt"),
    "total_asset":("wealth",    "missing_codes_to_nan", "family net asset"),
    "Asset":    ("wealth",      "missing_codes_to_nan", "family net asset (yuan)"),
    "asset":    ("wealth",      "missing_codes_to_nan", "family net asset (log)"),
    "savings":  ("bitter_outcome","missing_codes_to_nan","cash + deposits"),
    "sav":      ("wealth",      "duplicate_savings",    "alt cash+deposits"),
    "cas":      ("wealth",      "missing_codes_to_nan", "cash+deposits (log)"),
    "finance_asset":("wealth",  "missing_codes_to_nan", "financial assets"),
    "fin":      ("wealth",      "missing_codes_to_nan", "financial assets (log)"),
    "Esta":     ("wealth",      "missing_codes_to_nan", "net real estate (yuan)"),
    "esta":     ("wealth",      "missing_codes_to_nan", "net real estate (log)"),
    "Est":      ("wealth",      "missing_codes_to_nan", "gross real estate (yuan)"),
    "est":      ("wealth",      "missing_codes_to_nan", "gross real estate (log)"),
    "Hast":     ("wealth",      "missing_codes_to_nan", "total real estate market value"),
    "hast":     ("wealth",      "missing_codes_to_nan", "total real estate value (log)"),
    "Land":     ("wealth",      "missing_codes_to_nan", "land asset"),
    "land":     ("wealth",      "missing_codes_to_nan", "land asset (log)"),
    "land_asset":("wealth",     "missing_codes_to_nan", "land asset (duplicate)"),
    "houseasset_gross":("wealth","missing_codes_to_nan","gross house asset"),
    "fixed_asset":("wealth",    "missing_codes_to_nan", "productive fixed asset"),
    "durables_asset":("wealth", "missing_codes_to_nan", "durable goods value (car/appliance proxy)"),
    "fxzc":     ("wealth",      "missing_codes_to_nan", "risk assets"),
    "fd":       ("lambda_proxy","missing_codes_to_nan", "housing loan (small N, 2020-2022)"),
    "company":  ("wealth",      "missing_codes_to_nan", "business asset"),
    # ------------------------------------------------------ 2.9 D6 (absorbed into D8)
    "qtqk":     ("lambda_proxy","recode_binary",        "has non-housing debt 0/1"),
    "nonhousing_debts":("bitter_outcome","missing_codes_to_nan","non-housing debt"),
    "nhd":      ("bitter_outcome","missing_codes_to_nan","non-housing debt (duplicate)"),
    "Nhd":      ("bitter_outcome","missing_codes_to_nan","non-housing debt (yuan)"),
    "limit":    ("lambda_proxy","recode_binary",        "credit constraint"),
    "debt_p":   ("bitter_outcome","missing_codes_to_nan","debt-income ratio (small N)"),
    # ------------------------------------------------------ 2.10 D7 internet (excluded focal, kept for SI)
    "internet": ("covariate",   "recode_binary",        "uses internet"),
    "mobile":   ("covariate",   "recode_binary",        "mobile internet"),
    "computer": ("covariate",   "recode_binary",        "computer internet"),
    "onlineshopoping":("covariate","recode_binary",     "online shopping"),
    "social":   ("covariate",   "missing_codes_to_nan", "social-gift expenditure"),
    "Soc":      ("covariate",   "missing_codes_to_nan", "social-gift expenditure (yuan)"),
    "soc":      ("covariate",   "missing_codes_to_nan", "social-gift expenditure (log)"),
    # ------------------------------------------------------ 2.11 Trust etc.
    "qn10022":  ("covariate",   "range_0to10",          "trust in neighbors"),
    "qn10023":  ("covariate",   "range_0to10",          "trust in Americans"),
    "qn10024":  ("covariate",   "range_0to10",          "trust in strangers"),
    "qn10025":  ("covariate",   "range_0to10",          "trust in local officials"),
    "qn10026":  ("covariate",   "range_0to10",          "trust in doctors"),
    # ------------------------------------------------------ 2.12 Macro city panel
    "人均GDP":         ("macro_context","keep_raw","per capita GDP"),
    "财政支出占GDP比重": ("macro_context","keep_raw","fiscal expenditure share"),
    "二产增加值亿":     ("macro_context","keep_raw","secondary-sector value added"),
    "三产增加值亿":     ("macro_context","keep_raw","tertiary-sector value added"),
    "产业结构指数":     ("macro_context","keep_raw","industrial-structure index"),
    "城镇化水平":       ("macro_context","keep_raw","urbanization level"),
    "社会消费额占GDP比重":("macro_context","keep_raw","retail-sales share"),
    "高等学校在校生人数占比":("macro_context","keep_raw","HE enrollment share"),
    "邮电业务占GDP比重": ("macro_context","keep_raw","postal-telecom share"),
    "工业总产值占GDP比重":("macro_context","keep_raw","industrial-output share"),
}

# Domain membership (from cfps_variable_catalog.csv 'domains' field +
# domain_selection_matrix.md §3 spec sheets)
DOMAIN_VARS = {
    "D1_urban": [
        "pid", "year", "provcd", "city", "cityname", "urban", "rural", "hukou",
        "qn12012", "qn12016",
    ],
    "D2_education": [
        "pid", "year", "eexp", "school", "eec", "child_num", "child_p",
        "child_gender", "qn10021", "qn12012", "expense", "fincome1",
        "eduy", "edu",
    ],
    "D3_work": [
        "pid", "year", "workhour", "gongzi", "wage", "fwage", "jobclass",
        "worknature", "workplace", "industry", "bianzhi", "job",
        "qg401", "qg402", "qg403", "qg404", "qg405", "qg406",
        "health", "unhealth", "qp401", "qq4010", "familysize", "child_num",
    ],
    "D5_diet": [
        "pid", "year", "food", "expense", "qp401", "qq201", "health", "unhealth",
        "weak", "mexp", "med", "qn12012", "medsure_dum", "age",
    ],
    "D8_housing": [
        "pid", "year", "resivalue", "mortage", "mor", "h_loan", "house_debts",
        "qtqk", "nonhousing_debts", "limit", "house", "total_asset", "Asset",
        "asset", "savings", "cas", "dw", "qn12012", "qn12016",
        "durables_asset", "fincome1", "age", "child_num",
    ],
}


# ----------------------------------------------------------------------------
# 3. Helper functions
# ----------------------------------------------------------------------------

def log_step(name: str, before: int, after: int, **extra):
    """Write a one-line cleaning log entry."""
    delta = after - before
    extras = " ".join(f"{k}={v}" for k, v in extra.items())
    log.info(f"[{name}] before={before} after={after} delta={delta} {extras}")


def winsorize(s: pd.Series, lo: float = 0.01, hi: float = 0.99) -> pd.Series:
    """Winsorize a numeric Series at percentile cutoffs (1% and 99% default)."""
    if s.dropna().empty:
        return s
    q_lo, q_hi = s.quantile([lo, hi])
    return s.clip(lower=q_lo, upper=q_hi)


def log_transform(s: pd.Series) -> pd.Series:
    """log(x+1) transform preserving NaN."""
    return np.log1p(s.clip(lower=0))


# ----------------------------------------------------------------------------
# 4. Load raw data (ONCE)
# ----------------------------------------------------------------------------

def load_raw() -> pd.DataFrame:
    log.info("=" * 70)
    log.info("STEP 1: Load raw CFPS Stata dta (ONCE)")
    log.info("=" * 70)
    log.info(f"  source: {P1_DTA}")

    if not P1_DTA.exists():
        raise FileNotFoundError(f"CFPS dta not found at {P1_DTA}")

    t0 = _dt.datetime.now()
    df, meta = pyreadstat.read_dta(str(P1_DTA), apply_value_formats=False)
    t1 = _dt.datetime.now()
    log.info(f"  loaded shape={df.shape}  took={t1 - t0}")
    log.info(f"  columns sample: {list(df.columns[:10])} ... total={len(df.columns)}")
    return df, meta


# ----------------------------------------------------------------------------
# 5. Clean variables
# ----------------------------------------------------------------------------

def clean_variables(df: pd.DataFrame) -> pd.DataFrame:
    log.info("=" * 70)
    log.info("STEP 2: Clean variables (missing codes -> NaN, recoding)")
    log.info("=" * 70)

    # Select only the columns we care about. Everything else is dropped.
    present = [c for c in VARIABLE_DICT if c in df.columns]
    missing = [c for c in VARIABLE_DICT if c not in df.columns]
    if missing:
        log.warning(f"  {len(missing)} expected columns MISSING from source: {missing}")

    df = df[present].copy()
    log.info(f"  kept {len(present)} of {len(VARIABLE_DICT)} dict columns")

    # Apply CFPS missing-code coercion to all numeric columns.
    nrows = len(df)
    total_coerced = 0
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            mask = df[col].isin(CFPS_MISSING_CODES)
            n = int(mask.sum())
            if n:
                df.loc[mask, col] = np.nan
                total_coerced += n
    log.info(f"  coerced {total_coerced:,} CFPS missing-code values to NaN "
             f"across {len(df.columns)} cols over {nrows:,} rows")

    # Column-specific recoding (only the ones where the rule needs logic)
    # Likert 1-5 variables with sentinel values > 5 (seen: qg405, qn1101 top5=79)
    for col in ["qg405", "qn1101"]:
        if col in df.columns:
            bad = df[col] > 5
            n = int(bad.sum())
            if n:
                df.loc[bad, col] = np.nan
                log.info(f"  [{col}] nulled {n:,} out-of-range (>5) values "
                         f"(treated as sentinel for refusal)")

    # Sleep hours range check: qq4010 should be 0-24
    if "qq4010" in df.columns:
        bad = (df["qq4010"] < 0) | (df["qq4010"] > 24)
        n = int(bad.sum())
        if n:
            df.loc[bad, "qq4010"] = np.nan
            log.info(f"  [qq4010] nulled {n:,} impossible sleep values (<0 or >24h)")

    # workhour clamp: 0 < x <= 168 (168 = hours in a week)
    if "workhour" in df.columns:
        bad = (df["workhour"] <= 0) | (df["workhour"] > 168)
        n = int(bad.sum())
        if n:
            df.loc[bad, "workhour"] = np.nan
            log.info(f"  [workhour] nulled {n:,} impossible weekly hours (<=0 or >168)")

    # age sanity check: 10-100
    if "age" in df.columns:
        bad = (df["age"] < 10) | (df["age"] > 100)
        n = int(bad.sum())
        if n:
            df.loc[bad, "age"] = np.nan
            log.info(f"  [age] nulled {n:,} implausible ages (<10 or >100)")

    return df


# ----------------------------------------------------------------------------
# 6. Derive analytic variables
# ----------------------------------------------------------------------------

def derive_variables(df: pd.DataFrame) -> pd.DataFrame:
    log.info("=" * 70)
    log.info("STEP 3: Derive analytic variables")
    log.info("=" * 70)

    # ----- wave label -----
    df["wave"] = df["year"].astype("Int64")

    # ----- binary indicators (core, used across ≥2 domains) -----
    # gender: ensure 'female' is 1=female
    if "gender" in df.columns:
        df["female"] = 1 - df["gender"]  # gender=1 male, so female=1-gender
        log.info(f"  derived `female` (1-gender): N={df['female'].notna().sum():,}")

    # age buckets and young dummy
    if "age" in df.columns:
        df["age_young"] = (df["age"] < 40).astype("Int64")
        df["age_mid"] = ((df["age"] >= 40) & (df["age"] < 55)).astype("Int64")
        df["age_old"] = (df["age"] >= 55).astype("Int64")
        df.loc[df["age"].isna(), ["age_young", "age_mid", "age_old"]] = pd.NA
        log.info(f"  derived age buckets (young<40/mid 40-55/old>=55): "
                 f"young={int(df['age_young'].sum(skipna=True)):,}, "
                 f"mid={int(df['age_mid'].sum(skipna=True)):,}, "
                 f"old={int(df['age_old'].sum(skipna=True)):,}")

    # migrant: hukou mismatch with urban residence
    if {"hukou", "urban"}.issubset(df.columns):
        # hukou=1 rural, urban=1 urban -> migrant=1 if rural hukou but living in urban area
        df["migrant"] = ((df["hukou"] == 1) & (df["urban"] == 1)).astype("Int64")
        df.loc[df["hukou"].isna() | df["urban"].isna(), "migrant"] = pd.NA
        log.info(f"  derived `migrant` (rural hukou & urban residence): "
                 f"N_flagged={int(df['migrant'].sum(skipna=True)):,}")

    # ----- D3 996 domain derived -----
    # overtime_48h: workhour >= 48  (China labor law threshold)
    if "workhour" in df.columns:
        df["overtime_48h"] = (df["workhour"] >= 48).astype("Int64")
        df.loc[df["workhour"].isna(), "overtime_48h"] = pd.NA
        log.info(f"  derived `overtime_48h` (>=48h/week): "
                 f"N_true={int(df['overtime_48h'].sum(skipna=True)):,}, "
                 f"N_valid={df['overtime_48h'].notna().sum():,}")

    # overtime_996: workhour >= 60 (96 per week = ~9am-9pm x 6d but we use >=60 as strong-996)
    if "workhour" in df.columns:
        df["overtime_60h"] = (df["workhour"] >= 60).astype("Int64")
        df.loc[df["workhour"].isna(), "overtime_60h"] = pd.NA

    # ----- D8 housing domain derived -----
    if {"mortage", "fincome1"}.issubset(df.columns):
        # mortgage burden = mortgage payment / total family income
        # Avoid division by zero and cap at sensible range
        denom = df["fincome1"].where(df["fincome1"] > 0)
        df["mortgage_burden"] = df["mortage"] / denom
        # Winsorize at 1/99% to kill tail outliers from zero-income denominators
        before_w = df["mortgage_burden"].describe()
        df["mortgage_burden"] = winsorize(df["mortgage_burden"])
        log.info(f"  derived `mortgage_burden` (mortage/fincome1): "
                 f"N={df['mortgage_burden'].notna().sum():,} "
                 f"(winsorized 1/99%; raw max={before_w['max']:.2f})")

    if "mortage" in df.columns:
        df["has_mortgage"] = (df["mortage"] > 0).astype("Int64")
        df.loc[df["mortage"].isna(), "has_mortgage"] = pd.NA
        log.info(f"  derived `has_mortgage` (mortage>0): "
                 f"N_true={int(df['has_mortgage'].sum(skipna=True)):,}")

    # log(savings+1), log(house_debts+1), log(resivalue+1)
    for col in ["savings", "house_debts", "resivalue", "nonhousing_debts",
                "total_asset", "durables_asset"]:
        if col in df.columns:
            # Winsorize first to kill top-coded outliers
            w = winsorize(df[col])
            df[f"ln_{col}"] = log_transform(w)
            log.info(f"  derived `ln_{col}` (log1p after 1/99% winsorize): "
                     f"N={df[f'ln_{col}'].notna().sum():,}")

    # ----- D2 education domain derived -----
    if {"eexp", "expense"}.issubset(df.columns):
        denom = df["expense"].where(df["expense"] > 0)
        df["eexp_share"] = df["eexp"] / denom
        df["eexp_share"] = winsorize(df["eexp_share"])
        log.info(f"  derived `eexp_share` (eexp/expense): "
                 f"N={df['eexp_share'].notna().sum():,}")

    if {"eexp", "fincome1"}.issubset(df.columns):
        denom = df["fincome1"].where(df["fincome1"] > 0)
        df["eexp_income_ratio"] = df["eexp"] / denom
        df["eexp_income_ratio"] = winsorize(df["eexp_income_ratio"])
        df["education_squeeze"] = (df["eexp_income_ratio"] > 0.15).astype("Int64")
        df.loc[df["eexp_income_ratio"].isna(), "education_squeeze"] = pd.NA
        log.info(f"  derived `education_squeeze` (eexp/fincome1 > 0.15): "
                 f"N_true={int(df['education_squeeze'].sum(skipna=True)):,}")

    if "child_num" in df.columns:
        df["has_child"] = (df["child_num"] >= 1).astype("Int64")
        df.loc[df["child_num"].isna(), "has_child"] = pd.NA
        log.info(f"  derived `has_child` (child_num>=1): "
                 f"N_true={int(df['has_child'].sum(skipna=True)):,}")

    # ----- D5 diet domain derived -----
    if {"food", "expense"}.issubset(df.columns):
        denom = df["expense"].where(df["expense"] > 0)
        df["food_share"] = df["food"] / denom  # Engel coefficient
        df["food_share"] = winsorize(df["food_share"])
        log.info(f"  derived `food_share` (food/expense): "
                 f"N={df['food_share'].notna().sum():,}")

    # ----- common log transforms -----
    for col in ["fincome1", "expense", "food", "eexp", "mexp"]:
        if col in df.columns:
            w = winsorize(df[col])
            df[f"ln_{col}"] = log_transform(w)

    # ----- post-2021 policy dummy (双减 for D2) -----
    df["post_2021"] = (df["year"] >= 2021).astype("Int64")

    log.info(f"  final shape after derivation: {df.shape}")
    return df


# ----------------------------------------------------------------------------
# 7. Validate panel structure
# ----------------------------------------------------------------------------

def validate_panel(df: pd.DataFrame) -> None:
    log.info("=" * 70)
    log.info("STEP 4: Validate panel structure")
    log.info("=" * 70)

    dup = df.duplicated(subset=["pid", "year"]).sum()
    log.info(f"  duplicated (pid, year) pairs: {dup}")
    assert dup == 0, f"Panel has {dup} duplicate (pid, year) rows"

    n_person_years = len(df)
    n_unique_pid = df["pid"].nunique()
    log.info(f"  n_person_years = {n_person_years:,}")
    log.info(f"  n_unique_pid   = {n_unique_pid:,}")
    log.info(f"  average waves per pid = {n_person_years / n_unique_pid:.2f}")

    waves = sorted(df["year"].dropna().unique().tolist())
    log.info(f"  waves present = {waves}")

    wave_counts = df["year"].value_counts().sort_index()
    log.info(f"  wave counts:")
    for y, n in wave_counts.items():
        log.info(f"    {int(y)}: {n:,}")


# ----------------------------------------------------------------------------
# 8. Write domain subsets
# ----------------------------------------------------------------------------

def write_domain_subsets(df: pd.DataFrame) -> dict:
    log.info("=" * 70)
    log.info("STEP 5: Write 5 domain analysis-ready subsets")
    log.info("=" * 70)

    # Common covariates + lambda proxies to always carry
    COMMON = [
        "pid", "year", "wave",
        "age", "age_young", "age_mid", "age_old",
        "female", "gender",
        "eduy", "educ", "edu",
        "marrige", "mar",
        "hukou", "rural", "res", "migrant",
        "communist", "minzu",
        "familysize", "child_num", "has_child", "child_gender",
        "provcd", "city", "provname", "cityname", "urban",
        "lnincome", "fincome1", "ln_fincome1",
        "expense", "ln_expense",
        "medsure_dum",
        "post_2021",
    ]

    # Derived variable names for each domain
    DOMAIN_DERIVED = {
        "D1_urban": [],  # nothing extra derived for D1 (use existing IGMI parquet)
        "D2_education": ["eexp_share", "eexp_income_ratio", "education_squeeze",
                         "ln_eexp"],
        "D3_work":      ["overtime_48h", "overtime_60h"],
        "D5_diet":      ["food_share", "ln_food", "ln_mexp"],
        "D8_housing":   ["mortgage_burden", "has_mortgage",
                         "ln_savings", "ln_house_debts", "ln_resivalue",
                         "ln_nonhousing_debts", "ln_total_asset",
                         "ln_durables_asset"],
    }

    # Filter rules per domain (conservative: all non-null on anchor variables)
    # D1: everyone with qn12012 (full sample, 84K) -- matches existing Paper 1 pipeline
    # D2: households with children AND eexp non-missing
    # D3: workhour valid AND qg406 valid (employed persons reporting hours + satisfaction)
    # D5: food_share valid AND qp401 valid
    # D8: mortgage info valid AND dw valid
    FILTERS = {
        "D1_urban":     lambda d: d["qn12012"].notna(),
        "D2_education": lambda d: (d["has_child"] == 1) & d["eexp"].notna(),
        "D3_work":      lambda d: d["workhour"].notna() & d["qg406"].notna(),
        "D5_diet":      lambda d: d["food_share"].notna() & d["qp401"].notna(),
        "D8_housing":   lambda d: d["mortage"].notna() & d["dw"].notna(),
    }

    summary = {}

    for dom, varlist in DOMAIN_VARS.items():
        # Columns = common + derived + domain-specific (dedup)
        cols = list(dict.fromkeys(COMMON + DOMAIN_DERIVED.get(dom, []) + varlist))
        cols = [c for c in cols if c in df.columns]

        # Filter to analysis-ready rows
        mask = FILTERS[dom](df)
        sub = df.loc[mask, cols].copy()

        n_py = len(sub)
        n_pid = sub["pid"].nunique()

        out = OUT_PARQUET_DIR / f"panel_{dom}.parquet"
        sub.to_parquet(out, index=False)
        size_mb = out.stat().st_size / 1e6

        summary[dom] = {
            "n_person_years": int(n_py),
            "n_unique_pid": int(n_pid),
            "n_columns": int(len(cols)),
            "waves": sorted(sub["year"].dropna().unique().astype(int).tolist()),
            "file": str(out.relative_to(REPO)),
            "size_MB": round(size_mb, 2),
        }
        log.info(f"  [{dom}] N_py={n_py:,}  N_pid={n_pid:,}  cols={len(cols)}  "
                 f"size={size_mb:.2f} MB  file={out.name}")

    return summary


# ----------------------------------------------------------------------------
# 9. Diagnostic outputs
# ----------------------------------------------------------------------------

def write_variable_dict() -> None:
    log.info("=" * 70)
    log.info("STEP 6: Write variable dictionary CSV")
    log.info("=" * 70)

    rows = []
    for col, (role, rule, desc) in VARIABLE_DICT.items():
        domains = [d for d, v in DOMAIN_VARS.items() if col in v]
        rows.append({
            "column": col,
            "role": role,
            "recoding_rule": rule,
            "description": desc,
            "domains": "|".join(domains),
        })
    vd = pd.DataFrame(rows)
    out = OUT_LINKAGE_DIR / "variable_dict.csv"
    vd.to_csv(out, index=False)
    log.info(f"  wrote variable_dict.csv ({len(vd)} rows) -> {out}")


def compute_year_coverage(df: pd.DataFrame) -> pd.DataFrame:
    """For each variable in VARIABLE_DICT, compute N non-null per wave."""
    waves = sorted(df["year"].dropna().unique().astype(int).tolist())
    rows = []
    for col in VARIABLE_DICT:
        if col not in df.columns:
            continue
        row = {"column": col, "role": VARIABLE_DICT[col][0], "total_N": int(df[col].notna().sum())}
        for y in waves:
            mask = (df["year"] == y) & df[col].notna()
            row[f"y{y}"] = int(mask.sum())
        rows.append(row)
    return pd.DataFrame(rows)


def compute_sweet_bitter_descriptives(df: pd.DataFrame) -> dict:
    """Compute mean/SD/N by wave for each domain's Sweet DV and Bitter outcome."""
    targets = {
        "D1_urban":     {"sweet": "qn12012", "bitter": None},
        "D2_education": {"sweet": "qn12012", "bitter": "eexp_share"},  # treatment as proxy
        "D3_work":      {"sweet": "qg406",   "bitter": "qp401"},
        "D5_diet":      {"sweet": "qn12012", "bitter": "qp401"},
        "D8_housing":   {"sweet": "dw",      "bitter": "savings"},
    }
    waves = sorted(df["year"].dropna().unique().astype(int).tolist())
    out = {}
    for dom, tgt in targets.items():
        out[dom] = {}
        for role, col in tgt.items():
            if col is None or col not in df.columns:
                continue
            by_wave = []
            for y in waves:
                s = df.loc[df["year"] == y, col]
                by_wave.append({
                    "year": int(y),
                    "N": int(s.notna().sum()),
                    "mean": float(s.mean()) if s.notna().any() else None,
                    "SD": float(s.std()) if s.notna().any() else None,
                })
            out[dom][role] = {"column": col, "by_wave": by_wave}
    return out


def compute_lambda_cross_tab(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-tab of lambda-proxy availability counts per wave."""
    lam_vars = ["age", "hukou", "workplace", "child_num", "communist",
                "h_loan", "familysize", "eduy", "migrant", "age_young",
                "child_gender", "limit"]
    lam_vars = [v for v in lam_vars if v in df.columns]
    waves = sorted(df["year"].dropna().unique().astype(int).tolist())
    rows = []
    for v in lam_vars:
        row = {"lambda_proxy": v, "total_N": int(df[v].notna().sum())}
        for y in waves:
            mask = (df["year"] == y) & df[v].notna()
            row[f"y{y}"] = int(mask.sum())
        rows.append(row)
    return pd.DataFrame(rows)


def write_diagnostics(df_full: pd.DataFrame,
                      panel_summary: dict) -> None:
    log.info("=" * 70)
    log.info("STEP 7: Write D0 diagnostics markdown")
    log.info("=" * 70)

    year_cov = compute_year_coverage(df_full)
    sweet_bitter = compute_sweet_bitter_descriptives(df_full)
    lam_tab = compute_lambda_cross_tab(df_full)

    # Also save CSVs
    year_cov.to_csv(OUT_LINKAGE_DIR / "variable_year_coverage.csv", index=False)
    lam_tab.to_csv(OUT_LINKAGE_DIR / "lambda_proxy_coverage.csv", index=False)
    (OUT_LINKAGE_DIR / "sweet_bitter_descriptives.json").write_text(
        json.dumps(sweet_bitter, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Tier confirmation: compare PDE-ready N against Stage 0B stated N
    TIER_EXPECTED = {
        "D1_urban":     {"anchor": "qn12012",   "stage0_N_anchor": 84328, "tier": "***"},
        "D2_education": {"anchor": "eexp",      "stage0_N_anchor": 85594, "tier": "**"},
        "D3_work":      {"anchor": "workhour",  "stage0_N_anchor": 41528, "tier": "***"},
        "D5_diet":      {"anchor": "food",      "stage0_N_anchor": 84365, "tier": "**"},
        "D8_housing":   {"anchor": "mortage",   "stage0_N_anchor": 85866, "tier": "***"},
    }

    lines = []
    L = lines.append
    L("# D0: CFPS Long-Panel Cleaning Diagnostics")
    L("")
    L(f"**Generated:** {_dt.datetime.now():%Y-%m-%d %H:%M}")
    L("**Pipeline script:** `03-analysis/scripts/build_cfps_long_panel.py`")
    L("**Source:** `/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/2010-2022cfps非平衡面板数据(stata_推荐使用）.dta`")
    L(f"**Full long panel:** `02-data/processed/cfps_long_panel.parquet` "
      f"({len(df_full):,} person-years × {len(df_full.columns)} cols)")
    L("")
    L("---")
    L("")
    L("## 1. Panel structure")
    L("")
    L(f"- **n_person_years** = {len(df_full):,}")
    L(f"- **n_unique_pid** = {df_full['pid'].nunique():,}")
    L(f"- **waves** = {sorted(df_full['year'].dropna().unique().astype(int).tolist())}")
    L("")
    L("| Wave | N | % |")
    L("|---:|---:|---:|")
    wc = df_full["year"].value_counts().sort_index()
    for y, n in wc.items():
        L(f"| {int(y)} | {n:,} | {n/len(df_full)*100:.1f}% |")
    L("")
    L("---")
    L("")
    L("## 2. Analysis-ready N by domain")
    L("")
    L("| Domain | N (person-years) | N (unique pid) | N cols | File | Size |")
    L("|:---|---:|---:|---:|:---|---:|")
    for dom, s in panel_summary.items():
        L(f"| {dom} | {s['n_person_years']:,} | {s['n_unique_pid']:,} | "
          f"{s['n_columns']} | `{s['file']}` | {s['size_MB']} MB |")
    L("")
    L("### Comparison to Urban project (infra-growth-mismatch)")
    L("")
    urban_n_cfps = panel_summary["D1_urban"]["n_person_years"]
    L(f"Paper-1 urban pipeline (`cfps_igmi_expanded.parquet`): ~28K person-years (IGMI-merged subsample).")
    L(f"This pipeline's D1_urban subset: {urban_n_cfps:,} person-years (full qn12012 sample, pre-IGMI-merge).")
    L(f"The difference is expected: the IGMI merge drops observations in cities without IGMI series.")
    L("")
    for dom, s in panel_summary.items():
        if dom == "D1_urban":
            continue
        ratio = s["n_person_years"] / 28000
        marker = "larger" if ratio > 1 else "smaller"
        L(f"- **{dom}**: {s['n_person_years']:,} person-years ({ratio:.2f}× urban-28K, {marker})")
    L("")
    L("---")
    L("")
    L("## 3. Tier confirmation vs Stage 0B ratings")
    L("")
    L("| Domain | Stage 0B Tier | Anchor var | Stage 0B N | Cleaned N | Status |")
    L("|:---|:---:|:---|---:|---:|:---|")
    for dom, exp in TIER_EXPECTED.items():
        anc = exp["anchor"]
        if anc not in df_full.columns:
            L(f"| {dom} | {exp['tier']} | `{anc}` | {exp['stage0_N_anchor']:,} | MISSING | FAIL |")
            continue
        cleaned_N = int(df_full[anc].notna().sum())
        diff = cleaned_N - exp["stage0_N_anchor"]
        pct = abs(diff) / exp["stage0_N_anchor"] * 100
        if pct < 5:
            status = "confirmed"
        elif pct < 20:
            status = "minor drift"
        else:
            status = "large drift — investigate"
        L(f"| {dom} | {exp['tier']} | `{anc}` | {exp['stage0_N_anchor']:,} | "
          f"{cleaned_N:,} | {status} ({diff:+,}) |")
    L("")
    L("Notes: Cleaned N < Stage 0B N usually reflects out-of-range value nulling "
      "(e.g. `qg405` sentinel 79, `workhour` > 168).")
    L("")
    L("---")
    L("")
    L("## 4. Year-coverage per variable (selected domain anchors)")
    L("")
    key_vars = [
        "pid", "year", "age", "gender", "eduy", "hukou",
        "qn12012", "dw",  # sweet DVs
        "workhour", "qg406", "qg401", "qp401", "health", "qq4010",  # D3
        "eexp", "school", "child_num",  # D2
        "food", "qq201",  # D5
        "mortage", "resivalue", "savings", "house_debts",  # D8
    ]
    yc_sub = year_cov[year_cov["column"].isin(key_vars)].copy()
    yc_sub = yc_sub.set_index("column").reindex(key_vars).dropna(how="all").reset_index()
    L("| Variable | Role | Total N | " + " | ".join(f"{y}" for y in sorted(df_full['year'].dropna().unique().astype(int))) + " |")
    L("|:---|:---|---:|" + "---:|" * len(sorted(df_full['year'].dropna().unique().astype(int))))
    waves = sorted(df_full["year"].dropna().unique().astype(int).tolist())
    for _, r in yc_sub.iterrows():
        wave_cells = " | ".join(str(int(r.get(f"y{y}", 0))) for y in waves)
        L(f"| `{r['column']}` | {r['role']} | {int(r['total_N']):,} | {wave_cells} |")
    L("")
    L("Full coverage table: `02-data/linkage/variable_year_coverage.csv`")
    L("")
    L("---")
    L("")
    L("## 5. Sweet DV × Bitter outcome descriptives by wave")
    L("")
    for dom, roles in sweet_bitter.items():
        L(f"### {dom}")
        L("")
        for role, info in roles.items():
            L(f"**{role}** = `{info['column']}`")
            L("")
            L("| Year | N | Mean | SD |")
            L("|---:|---:|---:|---:|")
            for w in info["by_wave"]:
                if w["mean"] is None:
                    L(f"| {w['year']} | 0 | — | — |")
                else:
                    L(f"| {w['year']} | {w['N']:,} | {w['mean']:.3f} | {w['SD']:.3f} |")
            L("")
    L("---")
    L("")
    L("## 6. λ (externalization capacity) proxy availability")
    L("")
    L("| λ proxy | Total N | " + " | ".join(f"{y}" for y in waves) + " |")
    L("|:---|---:|" + "---:|" * len(waves))
    for _, r in lam_tab.iterrows():
        wave_cells = " | ".join(str(int(r.get(f"y{y}", 0))) for y in waves)
        L(f"| `{r['lambda_proxy']}` | {int(r['total_N']):,} | {wave_cells} |")
    L("")
    L("Full λ cross-tab: `02-data/linkage/lambda_proxy_coverage.csv`")
    L("")
    L("---")
    L("")
    L("## 7. Cleaning rules applied")
    L("")
    L("1. **CFPS missing codes** (`-1, -2, -3, -8, -9, -10`) → `NaN` "
      "across all numeric columns.")
    L("2. **Out-of-range sentinels**:")
    L("   - `qg405`, `qn1101`: values > 5 (mostly `79` refusal code) → NaN")
    L("   - `qq4010`: < 0 or > 24 → NaN")
    L("   - `workhour`: ≤ 0 or > 168 → NaN")
    L("   - `age`: < 10 or > 100 → NaN")
    L("3. **Derived binaries**:")
    L("   - `overtime_48h = 1[workhour ≥ 48]` (China labor law)")
    L("   - `overtime_60h = 1[workhour ≥ 60]` (strong-996 proxy)")
    L("   - `has_mortgage = 1[mortage > 0]`")
    L("   - `education_squeeze = 1[eexp/fincome1 > 0.15]`")
    L("   - `has_child = 1[child_num ≥ 1]`")
    L("   - `age_young = 1[age < 40]`  (λ proxy: younger externalize more)")
    L("   - `migrant = 1[hukou=1 (rural) & urban=1]`")
    L("   - `post_2021 = 1[year ≥ 2021]` (双减 policy dummy)")
    L("4. **Derived shares/ratios**:")
    L("   - `mortgage_burden = mortage / fincome1` (winsorized 1/99%)")
    L("   - `eexp_share = eexp / expense` (winsorized 1/99%)")
    L("   - `eexp_income_ratio = eexp / fincome1` (winsorized 1/99%)")
    L("   - `food_share = food / expense` (winsorized 1/99%, Engel coefficient)")
    L("5. **Log transforms** (`log1p` after 1/99% winsorize):")
    L("   - `ln_savings, ln_house_debts, ln_resivalue, ln_nonhousing_debts, "
      "ln_total_asset, ln_durables_asset, ln_fincome1, ln_expense, "
      "ln_food, ln_eexp, ln_mexp`")
    L("6. **Female dummy**: `female = 1 - gender` (source `gender` is 1=male).")
    L("")
    L("No row deletions in the full long panel — all cleaning is via NaN "
      "assignment. Domain analysis-ready subsets apply filters post hoc.")
    L("")
    L("---")
    L("")
    L("## 8. Missing-data pattern assessment (informal)")
    L("")
    L("We do not run formal MCAR/MAR tests at this stage. Missing patterns are "
      "dominated by **wave-coverage holes** (CFPS questionnaires differ by wave "
      "— see Section 4) rather than item-level non-response. Specifically:")
    L("")
    L("- `workhour` (N=41,528; 51.9% missing) — collected 2010/2014/2016/2018/2020/2022 "
      "and only for employed respondents. 2012 wave does NOT collect it.")
    L("- `qg401-qg406` job-satisfaction — collected 2010/2014/2016/2018/2020/2022, "
      "not 2012. Plus only employed respondents answer.")
    L("- `qq4010` sleep — only 2014+ waves (26,880 N).")
    L("- `mor` (alt mortgage label) — 2020/2022 only; `mortage` is the stable 7-wave label.")
    L("- `communist` — 2010/2016/2018/2020/2022 only (skipped 2012/2014).")
    L("- `minzu` — 2010 only; impute from first-observed value in full panel "
      "is recommended (not done here; flagged for D1/D3 analysis scripts).")
    L("")
    L("Missingness in `eexp` is near-zero (0.8%) because CFPS asks all "
      "households regardless of child presence — NaN reflects true non-answer, "
      "not structural skip. Zero values (43,724 rows) reflect genuine "
      "no-education-spending households (50% of families), not missing.")
    L("")
    L("**Recommendation:** treat wave-structural missingness as MAR conditional "
      "on `year` fixed effects. Item-level missingness in treatment variables "
      "(e.g. `workhour` among employees) may be MNAR and should be probed via "
      "selection models in the D3 robustness section.")
    L("")
    L("---")
    L("")
    L("## 9. Outputs")
    L("")
    L("| File | Description |")
    L("|:---|:---|")
    L("| `02-data/processed/cfps_long_panel.parquet` | Full cleaned long panel |")
    for dom in panel_summary:
        L(f"| `02-data/processed/panel_{dom}.parquet` | {dom} analysis-ready subset |")
    L("| `02-data/linkage/variable_dict.csv` | Variable name / label / recoding rule |")
    L("| `02-data/linkage/variable_year_coverage.csv` | Wave-level N per variable |")
    L("| `02-data/linkage/lambda_proxy_coverage.csv` | λ-proxy availability cross-tab |")
    L("| `02-data/linkage/sweet_bitter_descriptives.json` | Descriptive stats (mean/SD) by wave/domain |")
    L("| `02-data/linkage/cfps_cleaning.log` | Full cleaning log |")
    L("| `00-design/pde/D0_data_cleaning_diagnostics.md` | **This file** |")
    L("")
    L("---")
    L("")
    L("*End D0 diagnostics. Stage 2 domain scripts consume these panels as "
      "the single data entry point.*")

    out = OUT_DESIGN_DIR / "D0_data_cleaning_diagnostics.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    log.info(f"  wrote diagnostics -> {out}")


# ----------------------------------------------------------------------------
# 10. Main
# ----------------------------------------------------------------------------

def main() -> int:
    log.info("#" * 70)
    log.info("# sweet-trap-multidomain Stage 2 D0:")
    log.info("# CFPS 2010-2022 long panel cleaning pipeline")
    log.info(f"# Start: {_dt.datetime.now():%Y-%m-%d %H:%M:%S}")
    log.info("#" * 70)

    # Step 1: load
    df_raw, _meta = load_raw()

    # Step 2: clean (missing codes, recoding, out-of-range)
    df_clean = clean_variables(df_raw)
    del df_raw  # free memory

    # Step 3: derive analytic vars
    df = derive_variables(df_clean)
    del df_clean

    # Step 4: validate
    validate_panel(df)

    # Step 5: write full long panel
    out_full = OUT_PARQUET_DIR / "cfps_long_panel.parquet"
    df.to_parquet(out_full, index=False)
    log.info(f"  wrote full long panel -> {out_full} "
             f"({out_full.stat().st_size / 1e6:.2f} MB)")

    # Step 6: write domain subsets
    panel_summary = write_domain_subsets(df)

    # Step 7: write variable dict + diagnostics
    write_variable_dict()
    write_diagnostics(df, panel_summary)

    log.info("#" * 70)
    log.info(f"# Done: {_dt.datetime.now():%Y-%m-%d %H:%M:%S}")
    log.info("#" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
