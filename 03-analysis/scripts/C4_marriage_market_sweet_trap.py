"""
C4 Marriage-Market Sweet Trap — PDE Analysis Script
====================================================

Purpose
  Execute the pre-registered primary / secondary / spec-curve / IV pipeline
  for Study C4 of the Sweet-Trap multi-domain paper. C4 is the second human
  focal domain (bride-price / marriage wealth transfer × sex-ratio IV).

  Construct:  sweet_trap_formal_model_v2.md  (Δ_ST + F1–F4)
  Protocol:   00-design/analysis_protocols/pre_reg_C4_marriage.md

Hypotheses (pre-registered, directional, one-sided, alpha_Bonf = 0.01)
  H4.1  Sweet   partial cor(r_transfer, happy | controls)             > 0
  H4.2  Bitter  partial cor(r_transfer, life_sat | controls, modern)  < 0
  H4.3  Delta_ST = cor(..)_{pre-reform} - cor(..)_{reform-era}        > 0
  H4.4  lambda  beta(r_transfer x high_sex_ratio)  on life_sat         < 0
  H4.5  sibling r_transfer -> siblings_unmarried_share                 > 0
  Secondary: 2SLS of life_sat on r_transfer instrumented by sex ratio.

Input
  /Volumes/P1/城市研究/01-个体调查/CGSS_2011-2023/CGSS2017/CGSS2017.dta

Outputs
  02-data/processed/C4_cgss_marriage_panel.parquet  -- analytic sample
  02-data/processed/C4_results.json                 -- full numeric record
  03-analysis/scripts/C4_marriage_market_sweet_trap.log
  00-design/pde/C4_marriage_market_findings.md      -- separate write-up

Constraints
  - n_workers <= 2 (no multiprocessing used here).
  - Random seed 20260417 for all bootstrap / resampling steps.
  - Warnings visible.
  - d32/d33 recoded before any correlation; observation-level input unchanged.

Author:  Claude (opus-4-7) under Andy's Sweet-Trap project
Date:    2026-04-17
"""

import os
import json
import hashlib
from datetime import datetime

import numpy as np
import pandas as pd
import pyreadstat
import statsmodels.api as sm
from scipy import stats

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
BASE = os.path.expanduser("~/Desktop/Research/sweet-trap-multidomain")
CGSS_2017 = "/Volumes/P1/城市研究/01-个体调查/CGSS_2011-2023/CGSS2017/CGSS2017.dta"
OUT_PARQUET = os.path.join(BASE, "02-data/processed/C4_cgss_marriage_panel.parquet")
OUT_JSON = os.path.join(BASE, "02-data/processed/C4_results.json")
LOG_PATH = os.path.join(BASE, "03-analysis/scripts/C4_marriage_market_sweet_trap.log")

np.random.seed(20260417)

# ------------------------------------------------------------
# LOGGER
# ------------------------------------------------------------
class Tee:
    def __init__(self, path):
        self.f = open(path, "w", buffering=1)
    def write(self, msg):
        self.f.write(msg)
        self.f.flush()
        import sys as _sys
        _sys.__stdout__.write(msg)
    def close(self):
        self.f.close()

def log(msg=""):
    TEE.write(str(msg) + "\n")

TEE = Tee(LOG_PATH)

log("=" * 70)
log(f"C4 Marriage-Market Sweet Trap PDE — start {datetime.now().isoformat()}")
log("=" * 70)

# ------------------------------------------------------------
# 1. DATA LOAD & HASH
# ------------------------------------------------------------
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

log(f"\n[1] Loading CGSS 2017 from {CGSS_2017}")
file_sha = sha256_file(CGSS_2017)
log(f"    SHA-256: {file_sha}")

raw, meta = pyreadstat.read_dta(CGSS_2017)
log(f"    Raw dims: {raw.shape}")

# ------------------------------------------------------------
# 2. VARIABLE CONSTRUCTION
# ------------------------------------------------------------
log("\n[2] Variable construction")

def recode_to_nan(s, missing_codes=(98, 99)):
    s = pd.to_numeric(s, errors="coerce")
    s = s.where(~s.isin(missing_codes), np.nan)
    return s

def recode_d32(x):
    # 1 = yes, a lot;  2 = yes, some;  3 = none;  4 = parents deceased
    # => map to intensity: 3 if 1; 2 if 2; 1 if 3; NA otherwise
    if pd.isna(x):
        return np.nan
    if x == 1:
        return 3.0
    if x == 2:
        return 2.0
    if x == 3:
        return 1.0
    # 4 parents deceased, 98/99 missing => NA
    return np.nan

df = pd.DataFrame()
df["resp_id"] = raw["id"]
df["province"] = raw["s41"].astype(int)
df["sex_male"] = (raw["a2"] == 1).astype(int)
df["birth_year"] = pd.to_numeric(raw["a31"], errors="coerce")
df["age"] = 2017 - df["birth_year"]
df["educ_cat"] = pd.to_numeric(raw["a7a"], errors="coerce")

# Education years crosswalk
edu_years = {
    1: 0, 2: 3, 3: 6, 4: 9, 5: 12, 6: 12, 7: 12, 8: 12,
    9: 15, 10: 15, 11: 16, 12: 16, 13: 19, 14: np.nan,
}
df["educ_years"] = df["educ_cat"].map(edu_years)

# Hukou
df["hukou_rural"] = (raw["a18"] == 1).astype(int)
df["hukou_rural_ever"] = raw["a18"].isin([1, 3]).astype(int)

# Income
df["hh_income"] = pd.to_numeric(raw["a62"], errors="coerce")
# replace sentinel 9999999 with NA
df.loc[df["hh_income"] >= 9000000, "hh_income"] = np.nan
df["ln_hh_income"] = np.log1p(df["hh_income"])

# Marriage status and year
df["marstat"] = pd.to_numeric(raw["a69"], errors="coerce")
df["first_marr_year"] = pd.to_numeric(raw["a70"], errors="coerce")
df["curr_marr_year"] = pd.to_numeric(raw["a71b"], errors="coerce")
# Prefer a71b (current spouse marriage year); fall back to a70
df["marr_year"] = df["curr_marr_year"].fillna(df["first_marr_year"])
df.loc[~df["marr_year"].between(1950, 2017), "marr_year"] = np.nan

# Marriage-cohort 5-year bins
df["marr_cohort"] = (df["marr_year"] // 5 * 5).astype("Int64")

# Sweet signal proxies (d32 from own parents, d33 from spouse's parents)
df["d32_raw"] = raw["d32"]
df["d33_raw"] = raw["d33"]
df["d32_intensity"] = df["d32_raw"].apply(recode_d32)
df["d33_intensity"] = df["d33_raw"].apply(recode_d32)
# r_transfer: max of two intensities (strongest side of transfer)
df["r_transfer"] = df[["d32_intensity", "d33_intensity"]].max(axis=1)
# Binary "a lot from at least one side"
df["r_transfer_high"] = (
    (df["d32_raw"] == 1) | (df["d33_raw"] == 1)
).astype(int)
# Mask where both are missing
both_miss = df["d32_intensity"].isna() & df["d33_intensity"].isna()
df.loc[both_miss, "r_transfer_high"] = np.nan

# Sweet outcome DVs
df["happy"] = recode_to_nan(raw["a36"])  # 1-5, 5 = very happy
df["status"] = recode_to_nan(raw["a43e"])
df["status"] = 6 - df["status"]  # reverse: 5 = upper, 1 = lower (was 1 = upper)
df["marital_sat"] = recode_to_nan(raw["d31"])
df["marital_sat"] = 6 - df["marital_sat"]  # reverse: 5 = very satisfied

# Bitter outcome DVs
df["life_sat"] = recode_to_nan(raw["d21"])
df["life_sat"] = 6 - df["life_sat"]  # reverse: 5 = very satisfied

# happy_score d41 0-10 — treat "0" flagged as missing token (7838 of 11937 are 0, implausible).
d41 = pd.to_numeric(raw["d41"], errors="coerce")
# 0 appears ~7838 times — likely skip code. Keep only 1-10.
df["happy_score"] = d41.where((d41 >= 1) & (d41 <= 10), np.nan)

# Children count
df["kids_male"] = pd.to_numeric(raw["a681"], errors="coerce")
df["kids_female"] = pd.to_numeric(raw["a682"], errors="coerce")
df["kids_total"] = df["kids_male"].fillna(0) + df["kids_female"].fillna(0)
df.loc[df["kids_male"].isna() & df["kids_female"].isna(), "kids_total"] = np.nan

# Sibling marital statuses (d3d*): count unmarried = 1 = never married
sib_mar_cols = [c for c in ["d3d1","d3d2","d3d3","d3d4","d3d5","d3d6","d3d7","d3d8","d3d9","d3d10"] if c in raw.columns]
sib_marr_df = raw[sib_mar_cols].apply(pd.to_numeric, errors="coerce")
# count sibling records observed and how many are never-married (code 1)
sib_any = sib_marr_df.notna().sum(axis=1)
sib_unmarr = (sib_marr_df == 1).sum(axis=1)
# Only meaningful if respondent has any sibling marital-status observations
df["sib_observed"] = sib_any
df["sib_unmarried"] = sib_unmarr
df["sib_unmarried_share"] = np.where(sib_any > 0, sib_unmarr / sib_any, np.nan)

# ------------------------------------------------------------
# 3. SAMPLE FILTER
# ------------------------------------------------------------
log("\n[3] Sample filter")
n0 = len(df)
sub = df[df["marstat"].isin([3, 4])].copy()
log(f"    a69 in (3=initial marriage, 4=remarried): {len(sub):>6d} / {n0}")
sub = sub[sub["marr_year"].notna()]
log(f"    valid marriage year (1950-2017):         {len(sub):>6d}")
sub = sub[sub["r_transfer"].notna() | sub["r_transfer_high"].notna()]
log(f"    at least one of d32/d33 observed:        {len(sub):>6d}")
sub = sub[sub["age"].between(20, 90)]
log(f"    age 20-90:                               {len(sub):>6d}")
sub = sub[sub["birth_year"].notna()]
log(f"    birth year present:                      {len(sub):>6d}")
sub = sub[sub["educ_years"].notna()]
log(f"    education observed:                      {len(sub):>6d}")
sub = sub[sub["ln_hh_income"].notna()]
log(f"    hh income observed:                      {len(sub):>6d}")
log(f"    FINAL analytic N = {len(sub)}")

# ------------------------------------------------------------
# 4. SEX-RATIO CONSTRUCTION (province x 5-yr marriage cohort)
# ------------------------------------------------------------
log("\n[4] Sex-ratio construction (province x 5-yr marriage cohort)")

# Use the FULL married sample (including those without d-module) to construct
# the sex ratio, so the IV is not contaminated by d-module split-sample selection.
married_all = df[df["marstat"].isin([3, 4])].copy()
married_all = married_all[married_all["marr_year"].between(1950, 2017)]
sr = married_all.groupby(["province", "marr_cohort"]).apply(
    lambda g: (g["sex_male"] == 1).sum() / max((g["sex_male"] == 0).sum(), 1)
).reset_index().rename(columns={0: "sex_ratio_prov_cohort"})
# Also keep cell size for weight
cell_n = married_all.groupby(["province", "marr_cohort"]).size().reset_index(name="cell_n")
sr = sr.merge(cell_n, on=["province", "marr_cohort"], how="left")
log(f"    cells (prov x cohort): {len(sr)} ; median cell_n = {sr['cell_n'].median():.0f}")
log(f"    sex_ratio mean = {sr['sex_ratio_prov_cohort'].mean():.3f}, "
    f"sd = {sr['sex_ratio_prov_cohort'].std():.3f}")
log(f"    sex_ratio quantiles: 10%={sr['sex_ratio_prov_cohort'].quantile(.1):.2f}, "
    f"50%={sr['sex_ratio_prov_cohort'].quantile(.5):.2f}, "
    f"90%={sr['sex_ratio_prov_cohort'].quantile(.9):.2f}")

# Drop cells with n < 20 to reduce measurement noise, leave NA if too thin
sr.loc[sr["cell_n"] < 20, "sex_ratio_prov_cohort"] = np.nan

sub = sub.merge(sr[["province", "marr_cohort", "sex_ratio_prov_cohort", "cell_n"]],
                on=["province", "marr_cohort"], how="left")
log(f"    after merge: sex_ratio observed N = {sub['sex_ratio_prov_cohort'].notna().sum()} / {len(sub)}")

median_sr = sub["sex_ratio_prov_cohort"].median()
sub["high_sex_ratio"] = (sub["sex_ratio_prov_cohort"] > median_sr).astype("Int64")
sub.loc[sub["sex_ratio_prov_cohort"].isna(), "high_sex_ratio"] = pd.NA
log(f"    median sex_ratio = {median_sr:.3f}; 'high' = > median")

# Pre/post reform cohort
sub["prereform"] = (sub["marr_year"] <= 1978).astype(int)
sub["reformera"] = (sub["marr_year"] >= 1990).astype(int)
log(f"    pre-reform (<=1978) N = {sub['prereform'].sum()}")
log(f"    reform-era (>=1990) N = {sub['reformera'].sum()}")
log(f"    transition (1979-1989) N = {len(sub) - sub['prereform'].sum() - sub['reformera'].sum()}")

# ------------------------------------------------------------
# 5. DESCRIPTIVES
# ------------------------------------------------------------
log("\n[5] Descriptives by marriage cohort")

def describe_cohort(gdf, name):
    log(f"  Cohort [{name}]  N={len(gdf)}")
    for v in ["r_transfer", "r_transfer_high", "happy", "life_sat", "marital_sat",
              "status", "happy_score", "sex_ratio_prov_cohort",
              "hh_income", "educ_years"]:
        if v in gdf.columns:
            s = gdf[v].dropna()
            if len(s) > 0:
                log(f"    {v:25s}  n={len(s):5d}  mean={s.mean():8.3f}  sd={s.std():.3f}  "
                    f"median={s.median():.2f}")

describe_cohort(sub[sub["prereform"] == 1], "pre-reform (<=1978)")
describe_cohort(sub[(sub["marr_year"].between(1979, 1989))], "transition (1979-1989)")
describe_cohort(sub[sub["reformera"] == 1], "reform-era (>=1990)")
describe_cohort(sub, "POOLED")

# Distribution of r_transfer across cohorts
log("\n  r_transfer distribution (pct) across cohorts:")
for label, mask in [("prereform", sub["prereform"]==1), ("reformera", sub["reformera"]==1)]:
    vc = sub.loc[mask, "r_transfer"].value_counts(normalize=True, dropna=False).sort_index()
    log(f"    [{label}] " + "  ".join([f"{k}:{v*100:.1f}%" for k, v in vc.items()]))

# ------------------------------------------------------------
# 6. SAVE ANALYTIC PANEL
# ------------------------------------------------------------
log("\n[6] Save analytic panel")
keep = ["resp_id", "province", "sex_male", "birth_year", "age", "educ_years",
        "hukou_rural", "hukou_rural_ever", "hh_income", "ln_hh_income",
        "marstat", "marr_year", "marr_cohort", "prereform", "reformera",
        "r_transfer", "r_transfer_high", "d32_raw", "d33_raw",
        "happy", "status", "marital_sat", "life_sat", "happy_score",
        "kids_total", "kids_male", "kids_female",
        "sib_observed", "sib_unmarried", "sib_unmarried_share",
        "sex_ratio_prov_cohort", "high_sex_ratio", "cell_n"]
panel = sub[keep].copy()
# parquet cannot handle Int64 mixed with NA in high_sex_ratio — cast to float
panel["high_sex_ratio"] = panel["high_sex_ratio"].astype("float64")
panel.to_parquet(OUT_PARQUET, index=False)
panel_sha = hashlib.sha256(open(OUT_PARQUET, "rb").read()).hexdigest()
log(f"    Wrote {OUT_PARQUET}  SHA-256 = {panel_sha}")
log(f"    Shape = {panel.shape}")

# ------------------------------------------------------------
# 7. PRIMARY REGRESSIONS
# ------------------------------------------------------------
log("\n[7] Primary regressions")

def make_X(df_, include=("age", "age_sq", "sex_male", "educ_years", "ln_hh_income",
                         "hukou_rural_ever"), add_province_FE=True, add_cohort_FE=True):
    X = pd.DataFrame(index=df_.index)
    X["const"] = 1.0
    for v in include:
        if v == "age_sq":
            X["age_sq"] = (df_["age"] ** 2) / 100
        elif v in df_.columns:
            X[v] = df_[v]
    if add_province_FE:
        prov_dum = pd.get_dummies(df_["province"], prefix="prov", drop_first=True).astype(float)
        X = pd.concat([X, prov_dum], axis=1)
    if add_cohort_FE:
        coh_dum = pd.get_dummies(df_["marr_cohort"].astype(int), prefix="coh", drop_first=True).astype(float)
        X = pd.concat([X, coh_dum], axis=1)
    return X

def run_ols(df_, dv, endog="r_transfer", cluster_col="province", include=None,
            add_province_FE=True, add_cohort_FE=True, label=""):
    d = df_.dropna(subset=[dv, endog]).copy()
    if include is None:
        include = ("age", "age_sq", "sex_male", "educ_years", "ln_hh_income", "hukou_rural_ever")
    X = make_X(d, include=include, add_province_FE=add_province_FE, add_cohort_FE=add_cohort_FE)
    X.insert(1, endog, d[endog].values)
    y = d[dv].astype(float).values
    model = sm.OLS(y, X.astype(float))
    if cluster_col is not None and cluster_col in d.columns:
        res = model.fit(cov_type="cluster", cov_kwds={"groups": d[cluster_col].values})
    else:
        res = model.fit(cov_type="HC1")
    beta = res.params[endog]
    se = res.bse[endog]
    p_two = res.pvalues[endog]
    ci = res.conf_int().loc[endog].tolist()
    log(f"  [{label}] DV={dv}  endog={endog}  N={len(d)}  beta={beta:+.4f}  "
        f"SE={se:.4f}  CI95=[{ci[0]:+.4f}, {ci[1]:+.4f}]  p2sided={p_two:.3g}  R2={res.rsquared:.3f}")
    return {
        "label": label, "DV": dv, "endog": endog, "N": len(d),
        "beta": float(beta), "SE": float(se), "p_two_sided": float(p_two),
        "CI95_lo": float(ci[0]), "CI95_hi": float(ci[1]),
        "R2": float(res.rsquared),
        "p_one_sided_pos": float(p_two / 2 if beta > 0 else 1 - p_two / 2),
        "p_one_sided_neg": float(p_two / 2 if beta < 0 else 1 - p_two / 2),
    }

results = {"meta": {
    "script": "C4_marriage_market_sweet_trap.py",
    "start_iso": datetime.now().isoformat(),
    "cgss_2017_sha256": file_sha,
    "panel_sha256": panel_sha,
    "analytic_N": int(len(panel)),
    "seed": 20260417,
}}

log("\n--- H4.1 Sweet: r_transfer -> happy (pooled) ---")
results["H4_1_happy_pooled"] = run_ols(panel, "happy", label="H4.1 pooled, happy")

log("\n--- H4.1b Sweet: r_transfer -> marital_sat (pooled) ---")
results["H4_1_marital_pooled"] = run_ols(panel, "marital_sat", label="H4.1b pooled, marital_sat")

log("\n--- H4.1c Sweet: r_transfer -> status (pooled) ---")
results["H4_1_status_pooled"] = run_ols(panel, "status", label="H4.1c pooled, status")

log("\n--- H4.2 Bitter: r_transfer -> life_sat (reform-era) ---")
reform = panel[panel["reformera"] == 1]
results["H4_2_life_sat_reform"] = run_ols(reform, "life_sat", label="H4.2 reform, life_sat")

log("\n--- H4.2b Bitter: r_transfer -> life_sat (pooled) ---")
results["H4_2_life_sat_pooled"] = run_ols(panel, "life_sat", label="H4.2b pooled, life_sat")

log("\n--- H4.2c Bitter: r_transfer -> kids_total (pooled) ---")
results["H4_2_kids_pooled"] = run_ols(panel, "kids_total", label="H4.2c pooled, kids_total")

# ------------------------------------------------------------
# 8. Δ_ST ESTIMATION (H4.3)
# ------------------------------------------------------------
log("\n[8] Delta_ST estimation (H4.3)")

def partial_corr(df_, x, y, controls, cluster_col="province"):
    """Partial correlation of x and y after regressing each on controls.
       controls is a pandas DataFrame of covariates (already with const and FE).
    """
    d = df_.dropna(subset=[x, y]).copy()
    d = d[d[controls.columns.intersection(d.columns).tolist() + []].notna().all(axis=1)] if False else d
    # Residualise
    C = controls.loc[d.index].astype(float)
    x_res = sm.OLS(d[x].astype(float).values, C).fit().resid
    y_res = sm.OLS(d[y].astype(float).values, C).fit().resid
    r = np.corrcoef(x_res, y_res)[0, 1]
    return r, len(d)

def partial_corr_ready(df_, x, y, include=("age", "age_sq", "sex_male",
                                           "educ_years", "ln_hh_income",
                                           "hukou_rural_ever"),
                       add_province_FE=True, add_cohort_FE=False):
    d = df_.dropna(subset=[x, y] + [c for c in include if c not in ("age_sq",)]).copy()
    X = make_X(d, include=include, add_province_FE=add_province_FE,
               add_cohort_FE=add_cohort_FE)
    xv = d[x].astype(float).values
    yv = d[y].astype(float).values
    x_res = sm.OLS(xv, X.astype(float)).fit().resid
    y_res = sm.OLS(yv, X.astype(float)).fit().resid
    r = np.corrcoef(x_res, y_res)[0, 1]
    return r, len(d)

def bootstrap_delta_st(df_, x, y, cohort_col, rng, n_boot=2000,
                       add_cohort_FE=False):
    pre = df_[df_[cohort_col].str.lower() == "pre"].copy()
    post = df_[df_[cohort_col].str.lower() == "post"].copy()
    pre_idx = pre.index.to_numpy()
    post_idx = post.index.to_numpy()
    boot = np.empty(n_boot)
    for b in range(n_boot):
        pi = rng.choice(pre_idx, size=len(pre_idx), replace=True)
        qi = rng.choice(post_idx, size=len(post_idx), replace=True)
        try:
            r_pre, _ = partial_corr_ready(df_.loc[pi], x, y,
                                          add_cohort_FE=add_cohort_FE)
            r_post, _ = partial_corr_ready(df_.loc[qi], x, y,
                                           add_cohort_FE=add_cohort_FE)
            boot[b] = r_pre - r_post
        except Exception:
            boot[b] = np.nan
    return boot

# Build "cohort" column for Δ_ST
st = panel.copy()
st["cohort_bin"] = np.where(st["prereform"] == 1, "pre",
                    np.where(st["reformera"] == 1, "post", "mid"))

# Main Δ_ST: x=r_transfer, y=life_sat
for y_var in ["life_sat", "happy", "marital_sat"]:
    log(f"\n  Delta_ST for ({y_var}) ~ (r_transfer):")
    pre_sub = st[st["cohort_bin"] == "pre"]
    post_sub = st[st["cohort_bin"] == "post"]
    try:
        r_pre, n_pre = partial_corr_ready(pre_sub, "r_transfer", y_var,
                                          add_cohort_FE=False)
    except Exception as e:
        r_pre, n_pre = np.nan, 0
        log(f"    r_pre error: {e}")
    try:
        r_post, n_post = partial_corr_ready(post_sub, "r_transfer", y_var,
                                            add_cohort_FE=False)
    except Exception as e:
        r_post, n_post = np.nan, 0
        log(f"    r_post error: {e}")
    delta = r_pre - r_post
    log(f"    r_pre  = {r_pre:+.4f}  (N_pre  = {n_pre})")
    log(f"    r_post = {r_post:+.4f}  (N_post = {n_post})")
    log(f"    Delta_ST = {delta:+.4f}")
    # bootstrap
    rng = np.random.default_rng(20260417)
    boots = bootstrap_delta_st(st[st["cohort_bin"].isin(["pre", "post"])],
                               "r_transfer", y_var, "cohort_bin",
                               rng, n_boot=2000, add_cohort_FE=False)
    valid = boots[~np.isnan(boots)]
    ci_lo, ci_hi = np.quantile(valid, [0.025, 0.975])
    p_gt0 = float((valid <= 0).mean())
    log(f"    Bootstrap 95% CI = [{ci_lo:+.4f}, {ci_hi:+.4f}]  "
        f"1-sided p(Delta<=0) = {p_gt0:.3g}  (B = {len(valid)})")
    results[f"H4_3_delta_ST_{y_var}"] = {
        "r_pre": float(r_pre), "r_post": float(r_post), "delta": float(delta),
        "N_pre": int(n_pre), "N_post": int(n_post),
        "boot_CI95_lo": float(ci_lo), "boot_CI95_hi": float(ci_hi),
        "p_one_sided": p_gt0,
    }

# ------------------------------------------------------------
# 9. LAMBDA INTERACTION (H4.4) — sex-ratio moderation
# ------------------------------------------------------------
log("\n[9] H4.4 lambda interaction (sex ratio)")

lam_sub = panel.dropna(subset=["high_sex_ratio", "r_transfer", "life_sat"]).copy()
lam_sub["rt_x_highsr"] = lam_sub["r_transfer"] * lam_sub["high_sex_ratio"]

for dv in ["life_sat", "happy"]:
    d = lam_sub.dropna(subset=[dv]).copy()
    X = make_X(d, include=("age","age_sq","sex_male","educ_years","ln_hh_income",
                           "hukou_rural_ever"),
               add_province_FE=True, add_cohort_FE=True)
    X.insert(1, "r_transfer", d["r_transfer"].values)
    X.insert(2, "high_sex_ratio", d["high_sex_ratio"].values)
    X.insert(3, "rt_x_highsr", d["rt_x_highsr"].values)
    y = d[dv].astype(float).values
    res = sm.OLS(y, X.astype(float)).fit(cov_type="cluster",
                                         cov_kwds={"groups": d["province"].values})
    beta = res.params["rt_x_highsr"]
    se = res.bse["rt_x_highsr"]
    p2 = res.pvalues["rt_x_highsr"]
    ci = res.conf_int().loc["rt_x_highsr"].tolist()
    log(f"  [lambda] DV={dv}  N={len(d)}  beta(rt x high_sr)={beta:+.4f}  "
        f"SE={se:.4f}  CI95=[{ci[0]:+.4f},{ci[1]:+.4f}]  p2={p2:.3g}")
    # Also main effect coefficients for completeness
    log(f"    main rt      beta={res.params['r_transfer']:+.4f}  SE={res.bse['r_transfer']:.4f}")
    log(f"    main high_sr beta={res.params['high_sex_ratio']:+.4f}  SE={res.bse['high_sex_ratio']:.4f}")
    results[f"H4_4_lambda_{dv}"] = {
        "DV": dv, "N": len(d),
        "beta_interaction": float(beta), "SE": float(se),
        "CI95_lo": float(ci[0]), "CI95_hi": float(ci[1]),
        "p_two_sided": float(p2),
        "beta_r_transfer": float(res.params["r_transfer"]),
        "beta_high_sr": float(res.params["high_sex_ratio"]),
    }

# ------------------------------------------------------------
# 10. SIBLING EXTERNALISATION (H4.5)
# ------------------------------------------------------------
log("\n[10] H4.5 sibling externalisation")

sib = panel[(panel["sib_observed"] >= 1) & (panel["sex_male"] == 1)].copy()
log(f"  Male respondents with sibling marital info: N = {len(sib)}")

d = sib.dropna(subset=["sib_unmarried_share", "r_transfer"]).copy()
if len(d) >= 100:
    X = make_X(d, include=("age","age_sq","educ_years","ln_hh_income","hukou_rural_ever"),
               add_province_FE=True, add_cohort_FE=True)
    X.insert(1, "r_transfer", d["r_transfer"].values)
    # Also control for sib_observed to account for total siblings
    X.insert(2, "sib_observed", d["sib_observed"].values)
    y = d["sib_unmarried_share"].astype(float).values
    res = sm.OLS(y, X.astype(float)).fit(cov_type="cluster",
                                         cov_kwds={"groups": d["province"].values})
    beta = res.params["r_transfer"]
    se = res.bse["r_transfer"]
    p2 = res.pvalues["r_transfer"]
    ci = res.conf_int().loc["r_transfer"].tolist()
    log(f"  [H4.5] DV=sib_unmarried_share  N={len(d)}  beta={beta:+.4f}  "
        f"SE={se:.4f}  CI95=[{ci[0]:+.4f},{ci[1]:+.4f}]  p2={p2:.3g}")
    results["H4_5_sibling"] = {
        "N": len(d), "beta": float(beta), "SE": float(se),
        "p_two_sided": float(p2),
        "CI95_lo": float(ci[0]), "CI95_hi": float(ci[1]),
    }
else:
    log("  Insufficient N for H4.5")
    results["H4_5_sibling"] = {"N": len(d), "note": "insufficient N"}

# ------------------------------------------------------------
# 11. IV 2SLS (secondary)
# ------------------------------------------------------------
log("\n[11] IV 2SLS — r_transfer instrumented by sex_ratio_prov_cohort")

from linearmodels.iv import IV2SLS

iv_sub = panel.dropna(subset=["r_transfer", "life_sat", "sex_ratio_prov_cohort"]).copy()
X_cols = ["age", "age_sq", "sex_male", "educ_years", "ln_hh_income", "hukou_rural_ever"]
iv_sub["age_sq"] = (iv_sub["age"] ** 2) / 100
prov_dum = pd.get_dummies(iv_sub["province"], prefix="prov", drop_first=True).astype(float)
# include cohort FE sparingly — sex_ratio IS defined per cohort so may absorb it. Skip cohort FE.
Xiv = pd.concat([
    pd.Series(1.0, index=iv_sub.index, name="const"),
    iv_sub[X_cols].astype(float),
    prov_dum,
], axis=1)

for dv_iv in ["life_sat", "happy"]:
    dd = iv_sub.dropna(subset=[dv_iv]).copy()
    Xi = Xiv.loc[dd.index]
    try:
        ivmod = IV2SLS(dependent=dd[dv_iv].astype(float),
                       exog=Xi.astype(float),
                       endog=dd[["r_transfer"]].astype(float),
                       instruments=dd[["sex_ratio_prov_cohort"]].astype(float))
        ivres = ivmod.fit(cov_type="clustered", clusters=dd["province"])
        beta_iv = ivres.params["r_transfer"]
        se_iv = ivres.std_errors["r_transfer"]
        ci_iv = [ivres.conf_int().loc["r_transfer", "lower"],
                 ivres.conf_int().loc["r_transfer", "upper"]]
        p_iv = ivres.pvalues["r_transfer"]
        # First-stage F via linearmodels
        try:
            f_stat = float(ivres.first_stage.diagnostics.loc["r_transfer", "f.stat"])
        except Exception as _ex:
            log(f"    first-stage parse error: {_ex}")
            f_stat = float("nan")
        log(f"  [IV] DV={dv_iv}  N={len(dd)}  beta={beta_iv:+.4f}  SE={se_iv:.4f}  "
            f"CI95=[{ci_iv[0]:+.4f},{ci_iv[1]:+.4f}]  p2={p_iv:.3g}  first-stage F={f_stat:.2f}")
        results[f"IV_{dv_iv}"] = {
            "N": len(dd), "beta": float(beta_iv), "SE": float(se_iv),
            "CI95_lo": float(ci_iv[0]), "CI95_hi": float(ci_iv[1]),
            "p_two_sided": float(p_iv),
            "first_stage_F": f_stat,
            "weak_instrument_flag": bool(f_stat < 10 if not np.isnan(f_stat) else True),
        }
    except Exception as e:
        log(f"  [IV error] {dv_iv}: {e}")
        results[f"IV_{dv_iv}"] = {"error": str(e)}

# ------------------------------------------------------------
# 12. SPECIFICATION CURVE
# ------------------------------------------------------------
log("\n[12] Specification curve")

spec_rows = []
DVs = ["happy", "life_sat", "marital_sat"]
ENDOGs = ["r_transfer", "r_transfer_high"]
CTL_SETS = {
    "min": ("age", "age_sq", "sex_male"),
    "educ": ("age", "age_sq", "sex_male", "educ_years"),
    "full": ("age", "age_sq", "sex_male", "educ_years", "ln_hh_income", "hukou_rural_ever"),
}
FE_SCHEMES = [
    ("none", False, False),
    ("prov", True, False),
    ("prov_coh", True, True),
]
SAMPLE_DEFS = {
    "all": lambda df_: df_,
    "reform": lambda df_: df_[df_["reformera"] == 1],
    "prereform": lambda df_: df_[df_["prereform"] == 1],
}

for dv in DVs:
    for endog in ENDOGs:
        for cset_name, ctls in CTL_SETS.items():
            for fe_name, prov_fe, coh_fe in FE_SCHEMES:
                for sam_name, sam_fn in SAMPLE_DEFS.items():
                    d = sam_fn(panel).dropna(subset=[dv, endog]).copy()
                    if len(d) < 80:
                        continue
                    try:
                        X = make_X(d, include=ctls,
                                   add_province_FE=prov_fe,
                                   add_cohort_FE=coh_fe)
                        X.insert(1, endog, d[endog].values)
                        y = d[dv].astype(float).values
                        # drop dummies with all-zero variance after filtering
                        X = X.loc[:, (X.astype(float).var() > 1e-10) | (X.columns == "const")]
                        res = sm.OLS(y, X.astype(float)).fit(
                            cov_type="cluster", cov_kwds={"groups": d["province"].values}
                        )
                        beta = float(res.params[endog])
                        se = float(res.bse[endog])
                        p = float(res.pvalues[endog])
                        spec_rows.append({
                            "dv": dv, "endog": endog, "ctl": cset_name,
                            "fe": fe_name, "sample": sam_name,
                            "N": len(d), "beta": beta, "SE": se, "p": p,
                            "sig05_pos": int(beta > 0 and p < 0.05),
                            "sig05_neg": int(beta < 0 and p < 0.05),
                        })
                    except Exception as e:
                        spec_rows.append({
                            "dv": dv, "endog": endog, "ctl": cset_name,
                            "fe": fe_name, "sample": sam_name,
                            "N": len(d), "error": str(e),
                        })

spec_df = pd.DataFrame(spec_rows)
n_ok = spec_df["beta"].notna().sum()
log(f"  Total spec rows: {len(spec_df)}  converged: {n_ok}")

def spec_summary(sub, label):
    n = len(sub)
    if n == 0:
        log(f"  {label}: n=0 (no specs)")
        return {}
    pos_frac = (sub["beta"] > 0).mean()
    sig_pos_frac = (sub["sig05_pos"] == 1).mean()
    sig_neg_frac = (sub["sig05_neg"] == 1).mean()
    med_beta = sub["beta"].median()
    log(f"  {label:20s}  n={n:3d}  median_beta={med_beta:+.4f}  "
        f"frac(beta>0)={pos_frac:.2%}  sig+={sig_pos_frac:.2%}  sig-={sig_neg_frac:.2%}")
    return {
        "n": int(n), "median_beta": float(med_beta),
        "frac_positive": float(pos_frac),
        "sig_positive_frac": float(sig_pos_frac),
        "sig_negative_frac": float(sig_neg_frac),
    }

log("\n  Spec-curve summary by sample x DV:")
for dv in DVs:
    for sam in ["all", "reform", "prereform"]:
        sub = spec_df[(spec_df["dv"] == dv) & (spec_df["sample"] == sam) &
                      spec_df["beta"].notna()]
        results[f"speccurve_{dv}_{sam}"] = spec_summary(sub, f"{dv} / {sam}")

# Save spec curve raw
spec_csv = OUT_PARQUET.replace(".parquet", "_speccurve.csv")
spec_df.to_csv(spec_csv, index=False)
log(f"  Saved spec curve raw: {spec_csv}")

# ------------------------------------------------------------
# 13. PLACEBO & FIRST-STAGE SENSITIVITY
# ------------------------------------------------------------
log("\n[13] Placebo — first-stage sensitivity by cohort")
# Sex ratio is an IV for wealth transfer ONLY if it actually moves wealth transfer.
# First-stage check by cohort; pre-reform cohort should show smaller/nil first stage
# because sex-ratio imbalance had not emerged (one-child policy started 1979).

def first_stage_check(sam, label):
    d = sam.dropna(subset=["r_transfer", "sex_ratio_prov_cohort"]).copy()
    if len(d) < 50:
        log(f"  {label}: N too small ({len(d)})")
        return None
    X = make_X(d, include=("age","age_sq","sex_male","educ_years","ln_hh_income",
                            "hukou_rural_ever"),
               add_province_FE=True, add_cohort_FE=False)
    X.insert(1, "sex_ratio_prov_cohort", d["sex_ratio_prov_cohort"].values)
    y = d["r_transfer"].astype(float).values
    res = sm.OLS(y, X.astype(float)).fit(cov_type="cluster",
                                         cov_kwds={"groups": d["province"].values})
    beta = float(res.params["sex_ratio_prov_cohort"])
    se = float(res.bse["sex_ratio_prov_cohort"])
    p = float(res.pvalues["sex_ratio_prov_cohort"])
    # F-stat for instrument strength in this subsample
    try:
        from scipy import stats as _stats
        f_stat = float(res.tvalues["sex_ratio_prov_cohort"] ** 2)
    except Exception:
        f_stat = float("nan")
    log(f"  [{label}]  N={len(d)}  first-stage beta={beta:+.4f}  SE={se:.4f}  "
        f"p2={p:.3g}  F(robust)={f_stat:.2f}")
    return {"N": len(d), "beta": beta, "SE": se, "p_two_sided": p, "F_robust": f_stat}

results["firststage_pooled"] = first_stage_check(panel, "pooled")
results["firststage_prereform"] = first_stage_check(panel[panel["prereform"]==1], "prereform")
results["firststage_reform"] = first_stage_check(panel[panel["reformera"]==1], "reform")

# Also: sensitivity of H4.1 sign when d-module random-draw selection effects considered
# (placebo within-sample: r_transfer vs a NON-marriage outcome)
log("\n  Placebo: r_transfer -> self-rated health (a15, not directly marriage-related)")
a15 = pd.to_numeric(raw["a15"], errors="coerce")
a15 = a15.where((a15>=1) & (a15<=5), np.nan)
# 5 = very healthy, 1 = very unhealthy — keep forward
hh = panel.copy()
hh["self_health"] = a15.loc[hh.index].values if len(a15) == len(raw) else np.nan
# alternative: map via resp_id
_tmp = raw[["id"]].copy()
_tmp["self_health"] = a15.values
hh = panel.merge(_tmp, left_on="resp_id", right_on="id", how="left")
d = hh.dropna(subset=["self_health", "r_transfer"]).copy()
X = make_X(d, include=("age","age_sq","sex_male","educ_years","ln_hh_income","hukou_rural_ever"),
           add_province_FE=True, add_cohort_FE=True)
X.insert(1, "r_transfer", d["r_transfer"].values)
y = d["self_health"].astype(float).values
res = sm.OLS(y, X.astype(float)).fit(cov_type="cluster",
                                     cov_kwds={"groups": d["province"].values})
beta = float(res.params["r_transfer"])
se = float(res.bse["r_transfer"])
p = float(res.pvalues["r_transfer"])
log(f"  [placebo health] N={len(d)}  beta={beta:+.4f}  SE={se:.4f}  p2={p:.3g}")
results["placebo_self_health"] = {"N": len(d), "beta": beta, "SE": se, "p_two_sided": p}

# ------------------------------------------------------------
# 14. SAVE RESULTS JSON
# ------------------------------------------------------------
results["meta"]["end_iso"] = datetime.now().isoformat()

def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o) if not np.isnan(o) else None
    if isinstance(o, (np.ndarray,)):
        return o.tolist()
    if pd.isna(o):
        return None
    raise TypeError(f"not serializable: {type(o)}")

with open(OUT_JSON, "w") as f:
    json.dump(results, f, indent=2, default=_json_default)
log(f"\n[14] Wrote results JSON: {OUT_JSON}")
log(f"End {datetime.now().isoformat()}")
TEE.close()
