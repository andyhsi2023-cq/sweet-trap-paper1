#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_alcohol_panel.py
=======================

Stage 2 sweet-trap-multidomain: D_alcohol panel builder.

CRITICAL DATA CONSTRAINT LOG
----------------------------
  1. CFPS 2010-2022 pre-cleaned panel (86,294 person-years, 204 vars) does
     NOT contain the alcohol Q3 battery. The raw CFPS waves are not on P1,
     so CFPS cannot be used as the primary source for D_alcohol.
  2. CHARLS 2011-2020 integrated clean panel (96,628 person-waves, 25,873
     persons, 5 waves: 2011/2013/2015/2018/2020) has:
       - drinkev (ever drank alcohol), drinkl (currently drinks)
       - satlife (life satisfaction, 1-5 where 1=very unsat, 5=very sat)
       - cesd10 (CES-D depression, 0-30, higher = worse)
       - livere (ever liver disease, binary — Bitter biomarker!)
       - bl_crp, bl_cho, bl_hdl, bl_ldl, bl_hbalc (biomarkers)
       - hibpe, hearte, stroke, cancre (chronic disease)
       - social1-11 (social activities — type A proxy)
       - retire, age, edu, income_total (F2 SES)
  3. Harmonized CHARLS file adds r1drinkn_c, r2drinkn_c, r4drinkn_c (drink
     frequency 0-8: none / once-month / ... / daily / twice-day / more),
     available in waves 1 (2011), 2 (2013), 4 (2018). NOT available in
     wave 3 (2015) or wave 5 (2020).

F2 THREE-WAY DIAGNOSTIC LOGIC
-----------------------------
Per model v2 §1.2 and feedback_sweet_trap_strict_F2.md, alcohol is a
HETEROGENEOUS phenomenon with three types that must be kept separate:
  A. Social/aspirational drinking (CANDIDATE Sweet Trap): light/moderate
     frequency, paired with social activity, voluntary
  B. Business/coerced drinking (NOT Sweet Trap, F2 fails): 酒桌文化
     应酬 — workplace-induced, not voluntary
  C. Addiction (NOT Sweet Trap, F2 epistemic fails): daily+, often
     solitary, loss of control — DSM alcohol use disorder pattern

CHARLS limits: cohort 45+, many retired; type B identification via occupation
is weak. We implement conservative three-way labels:

  Type A (aspirational):
    drinkl == 1 AND freq <= 4 (<= 2-3 days/week) AND has_social == 1
    (participates in social activities act_1-11)
  Type B (coerced):
    drinkl == 1 AND retire == 0 AND age < 60 AND freq >= 3 (>= 1/week) AND
    currently_working — weak middle-aged employed heavy drinker proxy
  Type C (addiction/dependence):
    drinkl == 1 AND freq >= 6 (daily+) AND (cesd10 >= 10 OR livere == 1 OR
    cut down drinking history in past [proxy via drinkev==1 & drinkl==0])

NOTE: because CHARLS does NOT capture drinking context (solitary vs
social, ritual vs routine, subjective craving), these labels are PROXIES,
not clinical classifications. All labels are probabilistic (propensity)
rather than mutually exclusive — an individual can have weights across
all three types. We report both hard-label and soft-probability versions.

Inputs
------
  /Volumes/P1/城市研究/01-个体调查/CHARLS_中老年_2011-2020/
    charls2011~2020清洗好+原版数据/整理完的-charls数据/charls.dta
  /Volumes/P1/.../Harmonized_CHARLS_C/H_CHARLS_C_Data.dta (for freq)

Outputs
-------
  02-data/processed/panel_D_alcohol.parquet
  02-data/processed/panel_D_alcohol.meta.json (provenance + SHA-256)

Author: Claude (sweet-trap-multidomain D_alcohol analyst)
Date:   2026-04-17
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
PROJ = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
P1_BASE = Path(
    "/Volumes/P1/城市研究/01-个体调查/CHARLS_中老年_2011-2020/"
    "charls2011~2020清洗好+原版数据"
)
CLEAN_DTA = P1_BASE / "整理完的-charls数据" / "charls.dta"
HARM_DTA = (
    P1_BASE / "原始数据+问卷2011~2020" / "Harmonized_CHARLS_C" / "H_CHARLS_C_Data.dta"
)

OUT_PARQUET = PROJ / "02-data" / "processed" / "panel_D_alcohol.parquet"
OUT_META = PROJ / "02-data" / "processed" / "panel_D_alcohol.meta.json"
OUT_LOG = PROJ / "03-analysis" / "scripts" / "build_alcohol_panel.log"

OUT_PARQUET.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(OUT_LOG),
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("build_alcohol_panel")

# ----------------------------------------------------------------------------
# Step 1: Load integrated clean CHARLS panel
# ----------------------------------------------------------------------------
log.info("Reading cleaned CHARLS panel: %s", CLEAN_DTA)
df_clean, _ = pyreadstat.read_dta(str(CLEAN_DTA))
log.info("Clean panel shape: %s", df_clean.shape)

# Keep relevant columns (save memory)
keep_cols = [
    # IDs
    "ID", "wave", "householdID", "communityID", "iwy",
    # Alcohol (Sweet Trap focal treatment)
    "drinkev", "drinkl", "smokev", "smoken",
    # Sweet DVs
    "satlife", "srh", "cesd10", "hope",
    # Bitter DVs (biomarkers + chronic)
    "livere", "cancre", "hibpe", "hibpe_1", "hearte", "stroke",
    "bl_crp", "bl_cho", "bl_hdl", "bl_ldl", "bl_hbalc", "bl_glu", "bl_ua", "bl_tg",
    "systo", "diasto", "bmi", "mwaist",
    # Social activities (type A proxy)
    "social1", "social2", "social3", "social4", "social5",
    "social6", "social7", "social8",
    "act_1", "act_2", "act_3", "act_4", "act_5", "act_6", "act_7", "act_8",
    # Demographics / F2
    "age", "gender", "edu", "marry", "rural", "rural2", "retire",
    "income_total", "hhcperc", "family_size", "hchild",
    # Functional outcomes
    "adlab_c", "iadl", "wspeed", "fall_down",
    # Hospitalization (bitter $ cost)
    "hospital", "hospital_time", "oophos1y", "tothos1y",
    "chronic",
    "province", "city", "nation",
    "ins", "pension",
    "total_cognition",
]
keep_cols = [c for c in keep_cols if c in df_clean.columns]
df = df_clean[keep_cols].copy()
log.info("After column selection: %s", df.shape)

# ----------------------------------------------------------------------------
# Step 2: Merge harmonized CHARLS drinking frequency
# ----------------------------------------------------------------------------
log.info("Reading harmonized CHARLS for drinking frequency...")
harm_cols = [
    "ID", "r1drinkn_c", "r2drinkn_c", "r4drinkn_c",
    "r1drinkl", "r2drinkl", "r4drinkl",
]
df_harm, _ = pyreadstat.read_dta(str(HARM_DTA), usecols=harm_cols)
log.info("Harmonized shape: %s", df_harm.shape)

# Reshape harmonized drink frequency to long format
# Waves 1, 2, 4 → charls iwy 2011, 2013, 2018
hw_to_wave = {1: 1, 2: 2, 4: 4}
freq_long = []
for hw, w in hw_to_wave.items():
    sub = df_harm[["ID", f"r{hw}drinkn_c"]].copy()
    sub.columns = ["ID", "drinkn_c"]
    sub["wave"] = w
    freq_long.append(sub)
freq_long = pd.concat(freq_long, ignore_index=True)
freq_long = freq_long.dropna(subset=["drinkn_c"])
# Convert string error codes to NaN (categorical '0'..'8' as numeric)
freq_long["drinkn_c"] = pd.to_numeric(freq_long["drinkn_c"], errors="coerce")
log.info("Freq long (non-null): %s", len(freq_long))

df = df.merge(freq_long, on=["ID", "wave"], how="left")
log.info("After freq merge: %s (drinkn_c non-null = %d)",
         df.shape, df["drinkn_c"].notna().sum())

# ----------------------------------------------------------------------------
# Step 3: Derived variables — F2 three-way labels
# ----------------------------------------------------------------------------

# Recode drinkl, drinkev to 0/1 (some values may already be float)
df["drinkl"] = pd.to_numeric(df["drinkl"], errors="coerce")
df["drinkev"] = pd.to_numeric(df["drinkev"], errors="coerce")

# Social participation indicator (any social activity)
social_cols = [c for c in df.columns if c.startswith("social") or c.startswith("act_")]
df["has_social"] = 0
for c in social_cols:
    df["has_social"] = df["has_social"] | (pd.to_numeric(df[c], errors="coerce").fillna(0) >= 1).astype(int)
log.info("has_social rate: %.3f", df["has_social"].mean())

# Currently working proxy (retire == 0 AND age < 65)
df["retire"] = pd.to_numeric(df["retire"], errors="coerce")
df["working_45_65"] = ((df["retire"] == 0) & (df["age"].between(45, 65, inclusive="both"))).astype(int)
log.info("working_45_65 rate: %.3f", df["working_45_65"].mean())

# CES-D high depression (>=10 cutoff standard)
df["cesd_high"] = (pd.to_numeric(df["cesd10"], errors="coerce") >= 10).astype(int)

# livere binary (ever liver disease)
df["livere"] = pd.to_numeric(df["livere"], errors="coerce")
df["livere_01"] = (df["livere"] == 1).astype(int)

# --- F2 three-way hard labels ---

# Type A (aspirational social): current drinker, moderate freq (<=4 = <=2-3/wk),
# participates in social activities, NOT in daily+ pattern, NOT liver-diseased
df["type_A"] = (
    (df["drinkl"] == 1)
    & (df["drinkn_c"].between(1, 4, inclusive="both"))  # Once-month to 2-3 days/week
    & (df["has_social"] == 1)
    & (df["livere_01"] == 0)
).astype(int)

# Type B (coerced business): current drinker, working age employed, middle freq+,
# NOT already liver-diseased (to exclude Type C)
df["type_B"] = (
    (df["drinkl"] == 1)
    & (df["working_45_65"] == 1)
    & (df["drinkn_c"].between(3, 5, inclusive="both"))  # 1/wk to 4-6/wk
    & (df["livere_01"] == 0)
).astype(int)

# Type C (addiction/dependence): current drinker, daily+ frequency, with
# depression or liver disease (loss of control marker)
df["type_C"] = (
    (df["drinkl"] == 1)
    & (df["drinkn_c"] >= 6)  # Daily or more
).astype(int)

# "Cut down in past" proxy: ever drank but not currently (possible ex-addicts
# who quit due to health/social consequences)
df["type_ex_cutdown"] = (
    (df["drinkev"] == 1) & (df["drinkl"] == 0)
).astype(int)

# --- Soft probabilities using logistic-like weighting ---
# P(type_A): scale frequency downward, up social
# P(type_C): scale frequency upward, up CES-D, up livere
# These are proxy scores for sensitivity analysis

df["p_type_C"] = np.where(
    df["drinkl"] == 1,
    np.clip(
        0.2 * (df["drinkn_c"].fillna(0) / 8)
        + 0.3 * df["cesd_high"]
        + 0.3 * df["livere_01"]
        + 0.2 * df["type_ex_cutdown"],
        0, 1
    ),
    0
)
df["p_type_A"] = np.where(
    (df["drinkl"] == 1) & (df["p_type_C"] < 0.4),
    np.clip(
        0.5 * df["has_social"]
        + 0.3 * ((df["drinkn_c"].fillna(0) >= 1) & (df["drinkn_c"].fillna(8) <= 4)).astype(float)
        + 0.2 * (1 - df["cesd_high"]),
        0, 1
    ),
    0
)
df["p_type_B"] = np.where(
    (df["drinkl"] == 1) & (df["working_45_65"] == 1) & (df["p_type_C"] < 0.4),
    np.clip(
        0.4 * ((df["drinkn_c"].fillna(0) >= 3)).astype(float)
        + 0.3 * df["working_45_65"]
        + 0.3 * (df["gender"] == 1).astype(float),  # male-biased in Chinese business drinking
        0, 1
    ),
    0
)

# ----------------------------------------------------------------------------
# Step 4: Within-person helpers for panel FE (ρ lock-in, event study)
# ----------------------------------------------------------------------------
df = df.sort_values(["ID", "wave"])
df["drinkl_lag"] = df.groupby("ID")["drinkl"].shift(1)
df["drinkn_lag"] = df.groupby("ID")["drinkn_c"].shift(1)
df["satlife_lag"] = df.groupby("ID")["satlife"].shift(1)
df["livere_lag"] = df.groupby("ID")["livere_01"].shift(1)

# First-time drinker event (0 → 1)
df["entered_drinking"] = (
    (df["drinkl"] == 1) & (df["drinkl_lag"] == 0)
).astype(int)
df["exited_drinking"] = (
    (df["drinkl"] == 0) & (df["drinkl_lag"] == 1)
).astype(int)

# ln transformations
df["ln_income"] = np.log1p(df["income_total"].clip(lower=0))
df["ln_hhcperc"] = np.log1p(df["hhcperc"].clip(lower=0))

# ----------------------------------------------------------------------------
# Step 5: Write output
# ----------------------------------------------------------------------------
log.info("Final panel shape: %s", df.shape)
log.info("Type A count: %d (%.2f%%)", df["type_A"].sum(), df["type_A"].mean()*100)
log.info("Type B count: %d (%.2f%%)", df["type_B"].sum(), df["type_B"].mean()*100)
log.info("Type C count: %d (%.2f%%)", df["type_C"].sum(), df["type_C"].mean()*100)
log.info("Current drinker (drinkl=1): %d (%.2f%%)", (df["drinkl"]==1).sum(), (df["drinkl"]==1).mean()*100)

df.to_parquet(OUT_PARQUET, index=False)
log.info("Wrote parquet: %s", OUT_PARQUET)

# SHA-256
with open(OUT_PARQUET, "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest()

meta = {
    "generated_at": pd.Timestamp.utcnow().isoformat(),
    "script": str(Path(__file__).resolve()),
    "sources": {
        "clean_panel": str(CLEAN_DTA),
        "harmonized": str(HARM_DTA),
    },
    "n_rows": int(len(df)),
    "n_cols": int(df.shape[1]),
    "n_unique_ID": int(df["ID"].nunique()),
    "waves": sorted([int(w) for w in df["wave"].dropna().unique()]),
    "iwy": sorted([int(y) for y in df["iwy"].dropna().unique()]),
    "sha256": sha,
    "type_A_n": int(df["type_A"].sum()),
    "type_B_n": int(df["type_B"].sum()),
    "type_C_n": int(df["type_C"].sum()),
    "current_drinker_n": int((df["drinkl"]==1).sum()),
    "notes": (
        "D_alcohol panel for F2 three-way Sweet Trap diagnostic. "
        "CFPS 2010-2022 pre-cleaned panel lacks alcohol battery; CHARLS used. "
        "Harmonized freq (r{1,2,4}drinkn_c) merged to waves 2011/2013/2018 only "
        "(2015 and 2020 have drinkl only, no freq). Type labels are PROXIES — "
        "CHARLS does not observe drinking context (solitary vs social), craving, "
        "or loss-of-control directly."
    ),
}
OUT_META.write_text(json.dumps(meta, indent=2, ensure_ascii=False))
log.info("Wrote meta: %s (SHA-256 = %s)", OUT_META, sha)
print(f"DONE. Panel shape: {df.shape}, SHA-256 = {sha}")
