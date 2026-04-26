"""
build_hrs_panel.py — Build long-format US HRS panel for C8 (investment) and C13 (housing) replication.

Purpose
-------
Harmonize RAND HRS 1992-2020 v1 (SPSS .sav, wide format, 42,406 rows × 17,013 vars)
into a long person-wave panel with CFPS-comparable variables for two sibling Sweet
Trap analyses:

  * panel_C8_us_hrs.parquet  — investment / stock participation replication
  * panel_C13_us_hrs.parquet — housing / mortgage replication

Primary source
--------------
/Volumes/P1/城市研究/Harmonized HRS and RANDHRS/randhrs1992_2020v1.sav
  - 15 waves, 1992–2020, US biennial
  - 42,406 unique respondents (HHIDPN)
  - Uppercase variable names: R{n}* = individual vars, H{n}* = household vars

Key wave→year mapping
---------------------
  W1  1992    W5  2000    W9  2008   W13 2016
  W2  1994    W6  2002    W10 2010   W14 2018
  W3  1996    W7  2004    W11 2012   W15 2020
  W4  1998    W8  2006    W12 2014

Variable architecture
---------------------
Household-level (H{n}*):
  HATOTB  total assets (cross-wave)            HITOT   total HH income
  HASTCK  stock asset value                    HABOND  bond asset value
  HAIRA   IRA/401k value                       HACHCK  checking value
  HAHOUS  primary-residence value              HAMORT  total mortgage
  HADEBT  non-housing debt                     HAFHOUS asset-flag home ownership
  HAFSTCK asset-flag stock ownership           HAFMORT asset-flag has mortgage

Individual-level (R{n}*):
  RAGEY_B age at interview begin               RIEARN  R earnings
  RSHLT   self-rated health (1=excel..5=poor)  RCESD   CESD 8-item (0-8)
  RLBSATLIFE life sat 5-item Diener (W9-11 only; 1=str disagree..6=str agree avg?)
  RLBSATWLF  life sat 5-level scale            RLBPOSAFFECT positive affect (W8-15)
  RLBNEGAFFECT negative affect                 RRETEMP 1 if retired
  RJHOURS hours/week main job                  RWORK   =1 if working
  RLBRF   labor-force status                   RSAYRET considers self retired
  RRETYR  year retired                         RWHAPPY was happy (CESD item, W2-15)

Fixed (no wave prefix):
  RAGENDER, RARACEM, RAHISPAN, RAEDYRS, RAEDEGRM, RABYEAR, RABPLACE, HHIDPN, HHID, PN

Outputs
-------
  02-data/processed/panel_C8_us_hrs.parquet    (long format, filtered for C8 analysis)
  02-data/processed/panel_C13_us_hrs.parquet   (long format, filtered for C13 analysis)
  03-analysis/scripts/build_hrs_panel.log       (verbose progress + SHA-256 hashes)

Dependencies
------------
  pyreadstat, pandas, numpy, pyarrow
  RAM: peak ≈ 4-6 GB while reading the .sav (pyreadstat loads full table)

Author: Claude Code Data Analyst
Date: 2026-04-17
Seed: 20260417
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import pyreadstat

# ============================================================
# Paths & constants
# ============================================================

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
RAW_RANDHRS = Path(
    "/Volumes/P1/城市研究/Harmonized HRS and RANDHRS/randhrs1992_2020v1.sav"
)
OUT_DIR = ROOT / "02-data" / "processed"
LOG_PATH = ROOT / "03-analysis" / "scripts" / "build_hrs_panel.log"

# Wave → year (RAND HRS biennial)
WAVE_YEAR = {
    1: 1992, 2: 1994, 3: 1996, 4: 1998, 5: 2000,
    6: 2002, 7: 2004, 8: 2006, 9: 2008, 10: 2010,
    11: 2012, 12: 2014, 13: 2016, 14: 2018, 15: 2020,
}

# Sweet Trap analysis focuses on waves 5-15 (2000-2020). Earlier waves have
# thinner asset modules and no life-sat measurements. Wave 5+ aligns with
# CFPS 2010-2022 time-range for cross-national comparability.
WAVES = list(range(5, 16))  # 5..15 inclusive

# Fixed (time-invariant) variables to retain
FIXED_VARS = [
    "HHIDPN", "HHID", "PN",
    "RAGENDER", "RARACEM", "RAHISPAN",
    "RAEDYRS", "RAEDEGRM", "RABYEAR", "RABPLACE",
]

# Household-level time-varying variable bases (prepend H{wave})
H_VARS = {
    "HATOTB":   "hh_total_wealth",          # total of all assets
    "HITOT":    "hh_total_income",          # HH income (R+spouse)
    "HICAP":    "hh_cap_income",            # capital income
    "HASTCK":   "stock_value",              # stock asset $
    "HAFSTCK":  "has_stock_flag",           # 1 if household owns stock
    "HABOND":   "bond_value",               # bond asset $
    "HAFBOND":  "has_bond_flag",
    "HAIRA":    "ira_value",                # IRA / 401k
    "HAFIRA":   "has_ira_flag",
    "HACHCK":   "checking_value",
    "HAHOUS":   "home_value",               # primary residence value
    "HAFHOUS":  "has_home_flag",            # 1 if owns primary residence
    "HAMORT":   "mortgage_balance",         # total mortgage principal
    "HAFMORT":  "has_mortgage_flag",        # 1 if has mortgage
    "HAHMLN":   "home_loan_value",
    "HADEBT":   "non_housing_debt",         # debt excluding mortgage
    "HATOTH":   "total_housing_assets",     # (home - mortgage) equity base
    "HATOTN":   "total_nonhousing_wealth",
}

# Individual-level time-varying variable bases (prepend R{wave})
R_VARS = {
    "RAGEY_B":       "age",                 # age at interview begin
    "RIEARN":        "earnings",            # R labor earnings
    "RISRET":        "ret_inc",             # retirement income
    "RSHLT":         "srh",                 # self-rated health 1..5 (1=excel)
    "RCESD":         "cesd",                # CESD 8-item (0-8, higher=worse)
    "RLBSATLIFE":    "lifesat_single",      # W9-11 only, single-item life sat
    "RLBSATWLF":     "lifesat_diener",      # Diener 5-item composite W10+
    "RLBPOSAFFECT":  "pos_affect",          # positive affect (W8-15)
    "RLBNEGAFFECT":  "neg_affect",          # negative affect
    "RRETEMP":       "retired_empstat",     # =1 if retired in EMPSTAT
    "RSAYRET":       "self_retired",        # R considers self retired
    "RRETYR":        "retire_year",
    "RJHOURS":       "work_hours",          # hours/week main job
    "RWORK":         "works",               # =1 if working
    "RLBRF":         "lbr_force_status",
    "RINLBRF":       "in_labor_force",
    "RWHAPPY":       "cesd_happy",          # CESD: Was happy (reverse-coded)
    "RMSTAT":        "marital_status",
    "RIWSTAT":       "iw_status",           # interview status (1=interviewed)
}

# Sample membership flag
INW_FMT = "INW{n}"

# Random seed for determinism
SEED = 20260417

# ============================================================
# Logging
# ============================================================

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("build_hrs")


def sha256(path: Path) -> str:
    """Return SHA-256 of file in 64-char hex form."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ============================================================
# Step 1 — Build the list of columns we actually need
# ============================================================

def build_keep_cols(all_cols: list[str]) -> list[str]:
    """Return only those column names in the .sav that we will read."""
    keep: list[str] = []
    present = set(all_cols)

    for v in FIXED_VARS:
        if v in present:
            keep.append(v)
        else:
            log.warning("Fixed var %s not in sav", v)

    for w in WAVES:
        if (inw := INW_FMT.format(n=w)) in present:
            keep.append(inw)
        for base in H_VARS:
            col = f"H{w}{base[1:]}"  # HATOTB -> H{w}ATOTB
            if col in present:
                keep.append(col)
        for base in R_VARS:
            col = f"R{w}{base[1:]}"
            if col in present:
                keep.append(col)
    # de-duplicate preserving order
    seen: set[str] = set()
    out = []
    for c in keep:
        if c not in seen:
            out.append(c)
            seen.add(c)
    return out


# ============================================================
# Step 2 — Reshape wide → long
# ============================================================

def reshape_long(wide: pd.DataFrame) -> pd.DataFrame:
    """Convert wide RAND HRS to long (pid, wave, year)."""
    records = []
    for w in WAVES:
        inw_col = INW_FMT.format(n=w)
        if inw_col not in wide.columns:
            log.warning("INW%d missing; skipping", w)
            continue
        log.info("Reshaping wave %d (year %d)", w, WAVE_YEAR[w])
        # Only keep respondents who took this wave
        mask = wide[inw_col].fillna(0).astype("int8") == 1
        n_in = int(mask.sum())
        log.info("  W%d interviewed = %d", w, n_in)

        sub = wide.loc[mask, FIXED_VARS].copy()
        sub["wave"] = w
        sub["year"] = WAVE_YEAR[w]
        sub["in_wave"] = 1

        # Household vars
        for base, newname in H_VARS.items():
            col = f"H{w}{base[1:]}"
            if col in wide.columns:
                sub[newname] = wide.loc[mask, col].values
            else:
                sub[newname] = np.nan

        # Individual vars
        for base, newname in R_VARS.items():
            col = f"R{w}{base[1:]}"
            if col in wide.columns:
                sub[newname] = wide.loc[mask, col].values
            else:
                sub[newname] = np.nan

        records.append(sub)

    long = pd.concat(records, axis=0, ignore_index=True)
    log.info("Long panel: %d rows, %d cols", len(long), long.shape[1])
    return long


# ============================================================
# Step 3 — Derive analytic vars
# ============================================================

def ihs(x: pd.Series) -> pd.Series:
    """Inverse hyperbolic sine: log(x + sqrt(x^2 + 1)) — handles 0 and negatives."""
    return np.arcsinh(x.astype(float))


def derive_vars(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived variables: ownership dummies, shares, logs, demographics.

    NB — RAND HRS asset flags (H{w}AFSTCK etc) are data-quality codes
    (1=continuous value, 6=no asset, 9=no fin resp), NOT ownership indicators.
    The correct ownership proxy is H{w}ASTCK > 0 (asset value positive).
    For mortgage, H{w}AFMORT has 0 = "No asset" which is valid.
    """
    # --- Household wealth & income ---
    df["ln_wealth"] = ihs(df["hh_total_wealth"])
    df["ln_income"] = ihs(df["hh_total_income"])
    df["ln_ern"] = ihs(df["earnings"])

    # --- Stock ownership (C8 focal) ---
    # A value > 0 means the household reported owning some stock worth something.
    # NaN on stock_value = question not asked / no fin. resp → treat as NaN not 0.
    df["stock_hold"] = (df["stock_value"].fillna(-1) > 0).astype("Int64")
    df["stock_hold"] = df["stock_hold"].where(df["stock_value"].notna(), pd.NA)

    df["bond_hold"] = (df["bond_value"].fillna(-1) > 0).astype("Int64")
    df["bond_hold"] = df["bond_hold"].where(df["bond_value"].notna(), pd.NA)

    df["ira_hold"] = (df["ira_value"].fillna(-1) > 0).astype("Int64")
    df["ira_hold"] = df["ira_hold"].where(df["ira_value"].notna(), pd.NA)

    # Any risky asset (stock OR IRA OR bond > 0)
    stock_pos = df["stock_value"].fillna(0) > 0
    ira_pos = df["ira_value"].fillna(0) > 0
    bond_pos = df["bond_value"].fillna(0) > 0
    any_asset_observed = df[["stock_value", "ira_value", "bond_value"]].notna().any(axis=1)
    df["risky_hold"] = (stock_pos | ira_pos | bond_pos).astype("Int64")
    df["risky_hold"] = df["risky_hold"].where(any_asset_observed, pd.NA)

    # Stock share of total wealth (only defined when wealth > 0)
    with np.errstate(invalid="ignore", divide="ignore"):
        w = df["hh_total_wealth"].astype(float)
        s = df["stock_value"].astype(float).fillna(0)
        df["stock_share"] = np.where(w > 1000, np.clip(s / w, 0, 1), np.nan)
    df["ln_stock_value"] = ihs(df["stock_value"])
    df["ln_ira_value"] = ihs(df["ira_value"])

    # --- Housing (C13 focal) ---
    # home_own = home_value > 0; NaN preserved when home_value NaN
    df["home_own"] = (df["home_value"].fillna(-1) > 0).astype("Int64")
    df["home_own"] = df["home_own"].where(df["home_value"].notna(), pd.NA)

    # mortgage balance > 0
    df["has_mortgage"] = (df["mortgage_balance"].fillna(-1) > 0).astype("Int64")
    df["has_mortgage"] = df["has_mortgage"].where(df["mortgage_balance"].notna(), pd.NA)
    # Only meaningful for owners
    df["has_mortgage"] = df["has_mortgage"].where(df["home_own"] == 1, pd.NA)

    # Mortgage burden — mortgage balance / annual income (analogous to CFPS mortgage_burden)
    with np.errstate(invalid="ignore", divide="ignore"):
        inc = df["hh_total_income"].astype(float)
        mort = df["mortgage_balance"].astype(float).fillna(0)
        df["mortgage_burden"] = np.where(
            inc > 1000, np.clip(mort / inc, 0, 20), np.nan
        )
    # Loan-to-value (leverage ratio)
    with np.errstate(invalid="ignore", divide="ignore"):
        hv = df["home_value"].astype(float)
        df["ltv"] = np.where(hv > 1000, np.clip(mort / hv, 0, 3), np.nan)
    df["ln_home_value"] = ihs(df["home_value"])
    df["ln_mortgage"] = ihs(df["mortgage_balance"])
    df["ln_nonhousing_debt"] = ihs(df["non_housing_debt"])
    df["home_equity"] = df["home_value"].astype(float).fillna(0) - df["mortgage_balance"].astype(float).fillna(0)
    df["ln_home_equity"] = ihs(df["home_equity"])

    # --- Demographics ---
    df["female"] = (df["RAGENDER"].astype(float) == 2).astype("Int64")
    df["hispanic"] = (df["RAHISPAN"].astype(float) == 1).astype("Int64")
    df["white"] = (df["RARACEM"].astype(float) == 1).astype("Int64")
    df["black"] = (df["RARACEM"].astype(float) == 2).astype("Int64")
    df["edu_years"] = df["RAEDYRS"].astype(float)

    # --- Retirement ---
    df["retired"] = np.where(
        df["retired_empstat"].notna(),
        (df["retired_empstat"].astype(float) > 0).astype("Int64"),
        (df["self_retired"].astype(float) == 1).astype("Int64"),
    )

    # --- Happiness: CESD item "Was happy" is 1 if happy, 0 otherwise.
    # CESD score: higher = more depressed (0-8)
    df["cesd_score"] = df["cesd"].astype(float)
    # CESD reversed (happiness approximation): 8 - cesd
    df["cesd_rev"] = 8 - df["cesd_score"]

    # Self-rated health: reverse so higher = better (1 excel .. 5 poor → 5..1)
    df["srh_rev"] = 6 - df["srh"].astype(float)

    # Positive affect already is "higher = more positive"; negative affect opposite.
    # Combine into a composite "affect_balance" = pos - neg (only when both present)
    df["affect_balance"] = df["pos_affect"].astype(float) - df["neg_affect"].astype(float)

    # Cohort (age bucket at first obs)
    df["age"] = df["age"].astype(float)
    df["age_group"] = pd.cut(
        df["age"], bins=[-np.inf, 55, 65, 75, np.inf],
        labels=["<55", "55-64", "65-74", "75+"],
    ).astype(str)

    # Period markers for 2008 GFC natural experiment
    df["pre_2008"] = (df["year"] < 2008).astype(int)
    df["gfc_year"] = (df["year"] == 2008).astype(int)
    df["post_2008"] = (df["year"] > 2008).astype(int)

    return df


# ============================================================
# Step 4 — Build and save the two panels
# ============================================================

def main() -> None:
    rng = np.random.default_rng(SEED)  # noqa: F841 (kept for reproducibility record)

    log.info("=" * 70)
    log.info("HRS panel build — start")
    log.info("=" * 70)
    log.info("Source: %s", RAW_RANDHRS)
    t0 = time.time()
    src_hash = sha256(RAW_RANDHRS)
    log.info("Source SHA-256: %s", src_hash)
    log.info("Source size: %.1f MB", RAW_RANDHRS.stat().st_size / 1024 / 1024)

    # --- 1. Read metadata to determine column list ---
    log.info("Reading metadata…")
    _tmp, meta = pyreadstat.read_sav(str(RAW_RANDHRS), metadataonly=True)
    del _tmp
    all_cols = meta.column_names
    log.info("Source has %d rows × %d cols", meta.number_rows, meta.number_columns)

    keep_cols = build_keep_cols(all_cols)
    log.info("Keeping %d columns (%.2f%% of source)",
             len(keep_cols), 100 * len(keep_cols) / len(all_cols))

    # --- 2. Read wide data (subset) ---
    log.info("Reading wide subset… (may take 1-2 min)")
    t_read = time.time()
    wide, _ = pyreadstat.read_sav(
        str(RAW_RANDHRS), usecols=keep_cols, disable_datetime_conversion=True
    )
    log.info("Loaded wide: %d × %d in %.1fs, mem=%.1f MB",
             len(wide), wide.shape[1], time.time() - t_read,
             wide.memory_usage(deep=True).sum() / 1024 / 1024)

    # --- 3. Reshape to long ---
    log.info("Reshaping to long…")
    long = reshape_long(wide)
    del wide

    # --- 4. Derive analytical vars ---
    log.info("Deriving analytic variables…")
    long = derive_vars(long)

    # --- 5. Report wave coverage of life-sat vars ---
    for v in ["lifesat_single", "lifesat_diener", "cesd_score", "srh_rev",
              "pos_affect", "neg_affect"]:
        if v in long:
            by_year = long.groupby("year")[v].apply(lambda s: s.notna().sum())
            log.info("Coverage %s by year: %s", v, by_year.to_dict())

    # Report participation
    for v in ["stock_hold", "has_mortgage", "home_own", "risky_hold"]:
        if v in long:
            by_year = long.groupby("year")[v].mean().round(3)
            log.info("Mean %s by year: %s", v, by_year.to_dict())

    # --- 6. Build C8 (investment) panel ---
    log.info("-" * 70)
    log.info("Building C8 investment panel…")
    c8_cols = [
        "HHIDPN", "HHID", "PN", "wave", "year", "in_wave",
        "age", "female", "hispanic", "white", "black", "edu_years", "RABYEAR", "RABPLACE",
        "marital_status", "retired", "retire_year", "work_hours", "works",
        # Wealth / income
        "hh_total_wealth", "ln_wealth", "hh_total_income", "ln_income",
        "earnings", "ln_ern", "hh_cap_income",
        # Investment holdings (C8 core)
        "stock_hold", "stock_value", "ln_stock_value", "stock_share",
        "bond_hold", "bond_value",
        "ira_hold", "ira_value", "ln_ira_value",
        "risky_hold",
        # Welfare outcomes
        "lifesat_single", "lifesat_diener", "cesd_score", "cesd_rev",
        "srh", "srh_rev", "pos_affect", "neg_affect", "affect_balance",
        "cesd_happy",
        # Period markers
        "pre_2008", "gfc_year", "post_2008", "age_group",
    ]
    c8 = long[[c for c in c8_cols if c in long.columns]].copy()
    # Drop rows with no age (shouldn't happen for in_wave=1 but be safe)
    c8 = c8.dropna(subset=["age"])
    # Sort for panel lag derivation
    c8 = c8.sort_values(["HHIDPN", "wave"]).reset_index(drop=True)

    # Within-person lagged vars for ρ lock-in
    c8["stock_hold_lag"] = c8.groupby("HHIDPN")["stock_hold"].shift(1)
    c8["stock_value_lag"] = c8.groupby("HHIDPN")["stock_value"].shift(1)
    c8["hh_total_wealth_lag"] = c8.groupby("HHIDPN")["hh_total_wealth"].shift(1)
    c8["stock_value_change"] = c8["stock_value"].astype(float) - c8["stock_value_lag"].astype(float)
    c8["stock_loss_lag"] = ((c8["stock_value_change"] < -5000) & (c8["stock_hold_lag"] == 1)).astype("Int64")
    c8["stock_gain_lag"] = ((c8["stock_value_change"] > 5000) & (c8["stock_hold_lag"] == 1)).astype("Int64")
    # Exit event: was holder last wave, not holder now
    c8["exit_stock"] = ((c8["stock_hold_lag"] == 1) & (c8["stock_hold"] == 0)).astype("Int64")
    c8["continue_stock"] = ((c8["stock_hold_lag"] == 1) & (c8["stock_hold"] == 1)).astype("Int64")

    out_c8 = OUT_DIR / "panel_C8_us_hrs.parquet"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    c8.to_parquet(out_c8, index=False)
    c8_hash = sha256(out_c8)
    log.info("Wrote %s (%d × %d, SHA-256 %s)",
             out_c8, len(c8), c8.shape[1], c8_hash)

    # --- 7. Build C13 (housing) panel ---
    log.info("-" * 70)
    log.info("Building C13 housing panel…")
    c13_cols = [
        "HHIDPN", "HHID", "PN", "wave", "year", "in_wave",
        "age", "female", "hispanic", "white", "black", "edu_years", "RABYEAR", "RABPLACE",
        "marital_status", "retired", "work_hours", "works",
        # Wealth / income
        "hh_total_wealth", "ln_wealth", "hh_total_income", "ln_income",
        "earnings", "ln_ern",
        # Housing core
        "home_own", "home_value", "ln_home_value",
        "has_mortgage", "mortgage_balance", "ln_mortgage",
        "mortgage_burden", "ltv", "home_equity", "ln_home_equity",
        # Debt for stock-endowment Bitter
        "non_housing_debt", "ln_nonhousing_debt",
        # Welfare
        "lifesat_single", "lifesat_diener", "cesd_score", "cesd_rev",
        "srh", "srh_rev", "pos_affect", "neg_affect", "affect_balance",
        "cesd_happy",
        # Period markers
        "pre_2008", "gfc_year", "post_2008", "age_group",
    ]
    c13 = long[[c for c in c13_cols if c in long.columns]].copy()
    c13 = c13.dropna(subset=["age"])
    c13 = c13.sort_values(["HHIDPN", "wave"]).reset_index(drop=True)

    # Within-person lags
    c13["has_mortgage_lag"] = c13.groupby("HHIDPN")["has_mortgage"].shift(1)
    c13["mortgage_balance_lag"] = c13.groupby("HHIDPN")["mortgage_balance"].shift(1)
    c13["home_own_lag"] = c13.groupby("HHIDPN")["home_own"].shift(1)
    c13["home_value_lag"] = c13.groupby("HHIDPN")["home_value"].shift(1)
    c13["non_housing_debt_lag"] = c13.groupby("HHIDPN")["non_housing_debt"].shift(1)

    # Mortgage onset event: transition 0→1 in has_mortgage
    c13["mortgage_onset"] = ((c13["has_mortgage_lag"] == 0) & (c13["has_mortgage"] == 1)).astype("Int64")
    c13["mortgage_exit"] = ((c13["has_mortgage_lag"] == 1) & (c13["has_mortgage"] == 0)).astype("Int64")

    out_c13 = OUT_DIR / "panel_C13_us_hrs.parquet"
    c13.to_parquet(out_c13, index=False)
    c13_hash = sha256(out_c13)
    log.info("Wrote %s (%d × %d, SHA-256 %s)",
             out_c13, len(c13), c13.shape[1], c13_hash)

    # --- 8. Append SHA-256 to DATA_SNAPSHOT.md ---
    snapshot = OUT_DIR / "DATA_SNAPSHOT.md"
    addendum = f"""

---

## 2026-04-17 addendum — HRS US panels (C8 + C13 replication)

Source: `/Volumes/P1/城市研究/Harmonized HRS and RANDHRS/randhrs1992_2020v1.sav`
  SHA-256: `{src_hash}`
  Size: {RAW_RANDHRS.stat().st_size / 1024 / 1024:.1f} MB, 42,406 rows × 17,013 cols

Build script: `03-analysis/scripts/build_hrs_panel.py`
Waves: 5-15 (2000–2020, biennial)

| File | SHA-256 | Size (bytes) | Rows | Cols |
|:---|:---|---:|---:|---:|
| `panel_C8_us_hrs.parquet`  | `{c8_hash}` | {out_c8.stat().st_size} | {len(c8):,} | {c8.shape[1]} |
| `panel_C13_us_hrs.parquet` | `{c13_hash}` | {out_c13.stat().st_size} | {len(c13):,} | {c13.shape[1]} |

Coverage notes:
  * `lifesat_single` (RLBSATLIFE) only in waves 9-11 (years 2008, 2010, 2012) —
    enables the **2008 GFC natural experiment** window (life-sat observed *during* + 2 post-shock waves).
  * `lifesat_diener` (RLBSATWLF) wave 10+ (2010-2020).
  * `cesd_score` and `srh` are universal across waves (W2-W15 / W1-W15),
    enabling longer pre/post-2008 event-study windows.
  * `pos_affect` / `neg_affect` (Diener 12-question) waves 8-15 (2006-2020).
"""
    with open(snapshot, "a", encoding="utf-8") as f:
        f.write(addendum)
    log.info("Appended SHA-256 to %s", snapshot)

    log.info("=" * 70)
    log.info("Build complete in %.1fs", time.time() - t0)
    log.info("=" * 70)


if __name__ == "__main__":
    main()
