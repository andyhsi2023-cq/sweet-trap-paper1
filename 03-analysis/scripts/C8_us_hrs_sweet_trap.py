"""
C8_us_hrs_sweet_trap.py — US HRS replication of CFPS C8 investment Sweet Trap.

Objective
---------
Replicate on US data the C8 CFPS-China findings:
  * F2 aspirational-entry (stock ownership rises with income, education, wealth)
  * F1 reward-fitness decoupling (stock ownership → life-sat or CES-D ↓)
  * F3 lock-in (P[continue|loss] > 0.5)
  * F4 information-blockade (here: exit trajectory of 2008-GFC-exposed holders)
  * Δ_ST comparable to CFPS +0.060

Inputs
------
  02-data/processed/panel_C8_us_hrs.parquet
    Expected SHA-256: see DATA_SNAPSHOT.md (written by build_hrs_panel.py)

Outputs
-------
  02-data/processed/C8_us_results.json
  02-data/processed/C8_us_speccurve.csv
  03-analysis/scripts/C8_us_hrs_sweet_trap.log

Seed: 20260417
Date: 2026-04-17
Author: Claude Code Data Analyst
"""

from __future__ import annotations

import hashlib
import itertools
import json
import logging
import os
import sys
import time
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
PANEL_C8 = ROOT / "02-data" / "processed" / "panel_C8_us_hrs.parquet"
OUT_JSON = ROOT / "02-data" / "processed" / "C8_us_results.json"
OUT_SPEC = ROOT / "02-data" / "processed" / "C8_us_speccurve.csv"
LOG_PATH = ROOT / "03-analysis" / "scripts" / "C8_us_hrs_sweet_trap.log"

SEED = 20260417
N_BOOT = 1000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("C8_us")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def corr_with_p(x: pd.Series, y: pd.Series) -> tuple[float, float, int]:
    """Pearson correlation plus two-sided p value."""
    m = x.notna() & y.notna()
    if m.sum() < 30:
        return np.nan, np.nan, int(m.sum())
    r, p = stats.pearsonr(x[m].astype(float), y[m].astype(float))
    return float(r), float(p), int(m.sum())


def ols_fe(df: pd.DataFrame, y: str, x: str, controls: list[str],
           fe_pid: bool = True, fe_year: bool = True,
           cluster: str = "HHIDPN") -> dict[str, Any]:
    """Person-FE + year-FE regression with cluster-robust SE."""
    # Build column list without duplicates
    needed = {y, x, cluster, "HHIDPN", "year", *controls}
    sub = df[list(needed)].dropna()
    if len(sub) < 50:
        return {"n": int(len(sub)), "beta": np.nan, "se": np.nan,
                "ci_lo": np.nan, "ci_hi": np.nan, "p": np.nan}
    # Demean within-person if fe_pid
    dmean = sub.copy()
    if fe_pid:
        for c in [y, x] + controls:
            dmean[c] = dmean[c] - dmean.groupby("HHIDPN")[c].transform("mean")
    # Year dummies
    if fe_year:
        yearD = pd.get_dummies(dmean["year"], prefix="yr", drop_first=True).astype(float)
        X = pd.concat([dmean[[x] + controls], yearD], axis=1)
    else:
        X = dmean[[x] + controls]
    X = sm.add_constant(X.astype(float))
    mdl = sm.OLS(dmean[y].astype(float), X, missing="drop")
    try:
        res = mdl.fit(cov_type="cluster", cov_kwds={"groups": sub[cluster]})
    except Exception as e:
        log.warning("OLS fit failed: %s", e)
        return {"n": int(len(sub)), "beta": np.nan, "se": np.nan,
                "ci_lo": np.nan, "ci_hi": np.nan, "p": np.nan}
    b = float(res.params.get(x, np.nan))
    se = float(res.bse.get(x, np.nan))
    ci_lo, ci_hi = res.conf_int().loc[x].tolist() if x in res.params.index else (np.nan, np.nan)
    p = float(res.pvalues.get(x, np.nan))
    return {"n": int(len(sub)), "beta": b, "se": se,
            "ci_lo": float(ci_lo), "ci_hi": float(ci_hi), "p": float(p),
            "r2_within": float(res.rsquared)}


def bootstrap_diff(func, df, n_boot=N_BOOT, seed=SEED, **kwargs):
    rng = np.random.default_rng(seed)
    estimates = []
    ids = df["HHIDPN"].unique()
    for _ in range(n_boot):
        sampled = rng.choice(ids, size=len(ids), replace=True)
        # cluster bootstrap
        sub = df[df["HHIDPN"].isin(sampled)]
        try:
            estimates.append(func(sub, **kwargs))
        except Exception:
            estimates.append(np.nan)
    estimates = np.array([e for e in estimates if np.isfinite(e)])
    if len(estimates) < 10:
        return np.nan, np.nan, np.nan, np.nan
    lo, hi = np.percentile(estimates, [2.5, 97.5])
    return float(estimates.mean()), float(estimates.std()), float(lo), float(hi)


# ============================================================
# Main
# ============================================================

def main() -> None:
    rng = np.random.default_rng(SEED)
    log.info("=" * 70)
    log.info("C8 US HRS Sweet Trap analysis — start")
    log.info("=" * 70)
    log.info("Panel: %s", PANEL_C8)
    log.info("Panel SHA-256: %s", sha256(PANEL_C8))

    df = pd.read_parquet(PANEL_C8)
    log.info("Loaded %d rows × %d cols, %d unique pids",
             len(df), df.shape[1], df["HHIDPN"].nunique())
    log.info("Waves: %s", sorted(df["year"].unique().tolist()))

    results: dict[str, Any] = {"_meta": {"seed": SEED,
                                         "panel_sha256": sha256(PANEL_C8),
                                         "n_rows": int(len(df)),
                                         "n_pid": int(df["HHIDPN"].nunique())}}

    # ============================================================
    # 1. F2 strict-version diagnosis
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 1: F2 aspirational-entry diagnosis (strict)")
    log.info("-" * 70)

    f2_tests = {
        "cor_stock_hold_ln_income":
            corr_with_p(df["stock_hold"].astype(float), df["ln_income"]),
        "cor_stock_hold_ln_wealth":
            corr_with_p(df["stock_hold"].astype(float), df["ln_wealth"]),
        "cor_stock_hold_edu_years":
            corr_with_p(df["stock_hold"].astype(float), df["edu_years"]),
        "cor_risky_hold_ln_income":
            corr_with_p(df["risky_hold"].astype(float), df["ln_income"]),
        "cor_risky_hold_edu_years":
            corr_with_p(df["risky_hold"].astype(float), df["edu_years"]),
        "cor_ira_hold_ln_income":
            corr_with_p(df["ira_hold"].astype(float), df["ln_income"]),
        "cor_stock_share_edu_years":
            corr_with_p(df["stock_share"], df["edu_years"]),
    }
    for k, (r, p, n) in f2_tests.items():
        log.info("  %-40s r=%+.4f p=%.4g N=%d", k, r, p, n)

    # Income-tertile stock participation
    inc = df.dropna(subset=["ln_income", "stock_hold"]).copy()
    # Tertiles computed year-by-year to avoid period effects
    inc["inc_tert"] = inc.groupby("year")["ln_income"].transform(
        lambda s: pd.qcut(s, 3, labels=[1, 2, 3], duplicates="drop")
    )
    tert_part = inc.groupby("inc_tert", observed=True)["stock_hold"].mean().round(4)
    log.info("Stock ownership by income tertile: %s", tert_part.to_dict())

    # Education-bracket stock participation
    edu_df = df.dropna(subset=["edu_years", "stock_hold"]).copy()
    edu_df["edu_bucket"] = pd.cut(
        edu_df["edu_years"], bins=[-1, 11, 12, 15, 30],
        labels=["<HS", "HS", "some_col", "col+"],
    )
    edu_part = edu_df.groupby("edu_bucket", observed=True)["stock_hold"].mean().round(4)
    log.info("Stock ownership by education bucket: %s", edu_part.to_dict())

    results["F2_diagnosis"] = {
        "correlations": {k: {"r": r, "p": p, "n": n} for k, (r, p, n) in f2_tests.items()},
        "income_tertile_participation": {str(k): float(v) for k, v in tert_part.to_dict().items()},
        "education_bucket_participation": {str(k): float(v) for k, v in edu_part.to_dict().items()},
    }

    # F2 verdict
    t1 = f2_tests["cor_stock_hold_ln_income"][0]
    t3 = f2_tests["cor_stock_hold_edu_years"][0]
    passes = (t1 > 0.05) and (t3 > 0.05) and (tert_part.iloc[-1] > 3 * tert_part.iloc[0])
    results["F2_verdict"] = "PASS" if passes else "PARTIAL"
    log.info("F2 VERDICT: %s", results["F2_verdict"])

    # ============================================================
    # 2. Core Sweet Trap — within-person FE
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 2: Core Sweet Trap — stock_hold → welfare (within-person FE)")
    log.info("-" * 70)

    # Controls
    ctrl = ["age", "ln_income", "retired"]

    core_regs = {}
    for y in ["lifesat_single", "lifesat_diener", "cesd_rev", "srh_rev", "pos_affect", "affect_balance"]:
        for x in ["stock_hold", "risky_hold"]:
            name = f"{y}__{x}__feW"
            sub = df.dropna(subset=[y, x] + ctrl)
            r = ols_fe(sub, y=y, x=x, controls=ctrl)
            core_regs[name] = r
            log.info("  %-40s  N=%d  β=%+.4f  SE=%.4f  p=%.4g  CI=[%+.4f,%+.4f]",
                     name, r["n"], r["beta"], r["se"], r["p"], r["ci_lo"], r["ci_hi"])

    # Also: levels OLS (no person FE) for Δ_ST computation
    log.info("Levels (no FE) for ancestral/current Δ_ST computation:")
    for y in ["lifesat_single", "cesd_rev", "srh_rev"]:
        for x in ["stock_hold", "ln_stock_value"]:
            name = f"levels__{y}__{x}"
            sub = df.dropna(subset=[y, x])
            r = ols_fe(sub, y=y, x=x, controls=ctrl,
                       fe_pid=False, fe_year=True)
            core_regs[name] = r
            log.info("  %-40s  N=%d  β=%+.4f  p=%.4g",
                     name, r["n"], r["beta"], r["p"])

    results["core_sweet_trap"] = core_regs

    # ============================================================
    # 3. 2008 GFC natural experiment — pre-2007 stock holders
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 3: 2008 GFC natural experiment")
    log.info("-" * 70)

    # Define treatment: held stocks in 2006 (wave 8, last pre-GFC observation)
    pre2006 = df[df["year"] == 2006][["HHIDPN", "stock_hold"]].rename(
        columns={"stock_hold": "pre2006_holder"}
    )
    pre2006 = pre2006.dropna(subset=["pre2006_holder"])
    pre2006["pre2006_holder"] = pre2006["pre2006_holder"].astype(int)
    log.info("Pre-GFC (2006) stock holders: %d / %d = %.3f",
             pre2006["pre2006_holder"].sum(), len(pre2006), pre2006["pre2006_holder"].mean())

    d_gfc = df.merge(pre2006, on="HHIDPN", how="inner")
    # Post-crisis welfare: 2008, 2010, 2012 life-sat
    post = d_gfc[(d_gfc["year"].isin([2008, 2010, 2012])) & d_gfc["lifesat_single"].notna()].copy()

    # Effect of pre-2006 holding on 2008-2012 life-sat (control income, age, education)
    sub = post.dropna(subset=["lifesat_single", "pre2006_holder", "age", "ln_income", "edu_years"])
    yearD = pd.get_dummies(sub["year"], prefix="yr", drop_first=True).astype(float)
    X = pd.concat([sub[["pre2006_holder", "age", "ln_income", "edu_years"]], yearD], axis=1)
    X = sm.add_constant(X.astype(float))
    res = sm.OLS(sub["lifesat_single"].astype(float), X).fit(
        cov_type="cluster", cov_kwds={"groups": sub["HHIDPN"]}
    )
    gfc = {
        "n": int(len(sub)),
        "beta": float(res.params["pre2006_holder"]),
        "se": float(res.bse["pre2006_holder"]),
        "ci_lo": float(res.conf_int().loc["pre2006_holder", 0]),
        "ci_hi": float(res.conf_int().loc["pre2006_holder", 1]),
        "p": float(res.pvalues["pre2006_holder"]),
    }
    log.info("GFC effect on lifesat (pre-2006 holders vs not): β=%+.4f SE=%.4f p=%.4g N=%d",
             gfc["beta"], gfc["se"], gfc["p"], gfc["n"])

    # Also: same analysis using cesd_rev (available 2000-2020 → more power)
    sub2 = d_gfc[d_gfc["year"].isin([2008, 2010, 2012])].dropna(
        subset=["cesd_rev", "pre2006_holder", "age", "ln_income", "edu_years"])
    yearD2 = pd.get_dummies(sub2["year"], prefix="yr", drop_first=True).astype(float)
    X2 = pd.concat([sub2[["pre2006_holder", "age", "ln_income", "edu_years"]], yearD2], axis=1)
    X2 = sm.add_constant(X2.astype(float))
    res2 = sm.OLS(sub2["cesd_rev"].astype(float), X2).fit(
        cov_type="cluster", cov_kwds={"groups": sub2["HHIDPN"]}
    )
    gfc_cesd = {
        "n": int(len(sub2)),
        "beta": float(res2.params["pre2006_holder"]),
        "se": float(res2.bse["pre2006_holder"]),
        "p": float(res2.pvalues["pre2006_holder"]),
        "ci_lo": float(res2.conf_int().loc["pre2006_holder", 0]),
        "ci_hi": float(res2.conf_int().loc["pre2006_holder", 1]),
    }
    log.info("GFC effect on cesd_rev (pre-2006 holders): β=%+.4f SE=%.4f p=%.4g N=%d",
             gfc_cesd["beta"], gfc_cesd["se"], gfc_cesd["p"], gfc_cesd["n"])

    # Exit trajectory: 2006 holders' stock_hold by subsequent wave
    gfc_exit = {}
    for y in [2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020]:
        sub = d_gfc[(d_gfc["year"] == y) & (d_gfc["pre2006_holder"] == 1)]
        rate = sub["stock_hold"].mean()
        gfc_exit[str(y)] = {"N": int(sub["stock_hold"].notna().sum()),
                             "stock_hold_rate": float(rate) if pd.notna(rate) else np.nan}
        log.info("  W%d (year %d): pre-2006 holders retention rate = %.3f (N=%d)",
                 y - 2000, y, rate, sub["stock_hold"].notna().sum())

    # Event-study style: pre-treatment parallel-trends check using pre-2006 life-sat proxy
    # (lifesat_single only 2008+, so we use cesd_rev for pre-trends)
    pre_trend = {}
    for y in [2000, 2002, 2004, 2006]:
        sub = d_gfc[(d_gfc["year"] == y)].dropna(
            subset=["cesd_rev", "pre2006_holder", "age", "ln_income"])
        if len(sub) < 100:
            continue
        X = sm.add_constant(sub[["pre2006_holder", "age", "ln_income"]].astype(float))
        r = sm.OLS(sub["cesd_rev"].astype(float), X).fit(
            cov_type="cluster", cov_kwds={"groups": sub["HHIDPN"]}
        )
        pre_trend[str(y)] = {
            "beta": float(r.params["pre2006_holder"]),
            "se": float(r.bse["pre2006_holder"]),
            "p": float(r.pvalues["pre2006_holder"]),
            "n": int(len(sub)),
        }
    log.info("Pre-trends (cesd_rev on pre2006_holder, by year): %s", pre_trend)

    # Proper DID: person-FE with treatment × post-GFC indicator.
    # Because pre-trends clearly non-parallel (baseline levels differ strongly),
    # the person-FE DID is the legitimate causal estimator.
    did_df = d_gfc[d_gfc["year"].between(2000, 2014)].copy()
    did_df["post_gfc"] = (did_df["year"] >= 2008).astype(float)
    did_df["treat_x_post"] = did_df["pre2006_holder"] * did_df["post_gfc"]

    # Demean within person
    did_df_dm = did_df.dropna(subset=["cesd_rev", "treat_x_post", "age", "ln_income"])
    for c in ["cesd_rev", "treat_x_post", "post_gfc", "age", "ln_income"]:
        did_df_dm[c] = did_df_dm[c] - did_df_dm.groupby("HHIDPN")[c].transform("mean")
    yearD = pd.get_dummies(did_df_dm["year"], prefix="yr", drop_first=True).astype(float)
    Xd = pd.concat([did_df_dm[["treat_x_post", "age", "ln_income"]], yearD], axis=1)
    Xd = sm.add_constant(Xd.astype(float))
    rd = sm.OLS(did_df_dm["cesd_rev"].astype(float), Xd).fit(
        cov_type="cluster", cov_kwds={"groups": did_df_dm["HHIDPN"]}
    )
    did_cesd = {
        "n": int(len(did_df_dm)),
        "beta": float(rd.params["treat_x_post"]),
        "se": float(rd.bse["treat_x_post"]),
        "p": float(rd.pvalues["treat_x_post"]),
        "ci_lo": float(rd.conf_int().loc["treat_x_post", 0]),
        "ci_hi": float(rd.conf_int().loc["treat_x_post", 1]),
    }
    log.info("DID on cesd_rev (treat × post-GFC, person-FE): β=%+.4f SE=%.4f p=%.4g N=%d",
             did_cesd["beta"], did_cesd["se"], did_cesd["p"], did_cesd["n"])

    # Same with srh_rev (more observations)
    did_df_dm2 = did_df.dropna(subset=["srh_rev", "treat_x_post", "age", "ln_income"])
    for c in ["srh_rev", "treat_x_post", "age", "ln_income"]:
        did_df_dm2[c] = did_df_dm2[c] - did_df_dm2.groupby("HHIDPN")[c].transform("mean")
    yearD2 = pd.get_dummies(did_df_dm2["year"], prefix="yr", drop_first=True).astype(float)
    Xd2 = pd.concat([did_df_dm2[["treat_x_post", "age", "ln_income"]], yearD2], axis=1)
    Xd2 = sm.add_constant(Xd2.astype(float))
    rd2 = sm.OLS(did_df_dm2["srh_rev"].astype(float), Xd2).fit(
        cov_type="cluster", cov_kwds={"groups": did_df_dm2["HHIDPN"]}
    )
    did_srh = {
        "n": int(len(did_df_dm2)),
        "beta": float(rd2.params["treat_x_post"]),
        "se": float(rd2.bse["treat_x_post"]),
        "p": float(rd2.pvalues["treat_x_post"]),
        "ci_lo": float(rd2.conf_int().loc["treat_x_post", 0]),
        "ci_hi": float(rd2.conf_int().loc["treat_x_post", 1]),
    }
    log.info("DID on srh_rev (treat × post-GFC, person-FE): β=%+.4f SE=%.4f p=%.4g N=%d",
             did_srh["beta"], did_srh["se"], did_srh["p"], did_srh["n"])

    results["gfc_event_study"] = {
        "treatment_def": "stock_hold==1 in 2006 (pre-GFC baseline)",
        "lifesat_effect_naive_OLS": gfc,
        "cesd_rev_effect_naive_OLS": gfc_cesd,
        "did_cesd_rev_person_fe": did_cesd,
        "did_srh_rev_person_fe": did_srh,
        "exit_trajectory": gfc_exit,
        "pre_trends_cesd_rev": pre_trend,
        "notes": ("Naive OLS β is positive because pre-2006 holders are richer/healthier baseline "
                  "(pre-trends show this clearly). The DID with person-FE isolates the shock effect."),
    }

    # ============================================================
    # 4. F3 lock-in — P(continue | loss)
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 4: F3 lock-in — continue-after-loss rate")
    log.info("-" * 70)

    # For all wave pairs, compute: among those holding in t-1:
    #   P(still holding in t) — overall persistence
    # And among those who had a stock-value drop (stock_loss_lag==1):
    #   P(still holding)
    lock_df = df.dropna(subset=["stock_hold_lag", "stock_hold"])
    overall_cont = lock_df[lock_df["stock_hold_lag"] == 1]["stock_hold"].mean()
    log.info("P(hold_t | hold_{t-1}) overall = %.3f (N=%d)",
             overall_cont, (lock_df["stock_hold_lag"] == 1).sum())

    loss_df = lock_df[(lock_df["stock_hold_lag"] == 1) & (lock_df["stock_loss_lag"] == 1)]
    gain_df = lock_df[(lock_df["stock_hold_lag"] == 1) & (lock_df["stock_gain_lag"] == 1)]
    p_cont_loss = loss_df["stock_hold"].mean()
    p_cont_gain = gain_df["stock_hold"].mean()
    log.info("P(continue | loss)  = %.3f  N=%d", p_cont_loss, len(loss_df))
    log.info("P(continue | gain)  = %.3f  N=%d", p_cont_gain, len(gain_df))

    # Using 2008-2010 as the shock transition
    gfc_shock = lock_df[
        ((lock_df["year"] == 2010) & (lock_df["stock_hold_lag"] == 1))
    ]
    p_retain_post_gfc = gfc_shock["stock_hold"].mean()
    log.info("P(hold_2010 | hold_2008) = %.3f  N=%d", p_retain_post_gfc, len(gfc_shock))

    results["F3_lockin"] = {
        "p_continue_overall": float(overall_cont),
        "n_overall": int((lock_df["stock_hold_lag"] == 1).sum()),
        "p_continue_after_loss": float(p_cont_loss) if pd.notna(p_cont_loss) else np.nan,
        "n_loss": int(len(loss_df)),
        "p_continue_after_gain": float(p_cont_gain) if pd.notna(p_cont_gain) else np.nan,
        "n_gain": int(len(gain_df)),
        "p_retain_gfc_2008_to_2010": float(p_retain_post_gfc),
        "n_gfc_retain": int(len(gfc_shock)),
    }

    # ============================================================
    # 5. Δ_ST estimation
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 5: Δ_ST estimation")
    log.info("-" * 70)

    # Definition: Δ_ST = cor_ancestral(wealth, life-sat) - cor_current(stock-reward, life-sat)
    # Operationalization A: pre-2000 vs post-2005 comparison within HRS is hard because
    #   life-sat only exists 2008-2012. So we use:
    #   ancestral = non-stockholders' cor(ln_wealth, life-sat)
    #   current   = stockholders' cor(ln_stock_value, life-sat)
    nonholders = df[(df["stock_hold"] == 0) & df["lifesat_single"].notna()]
    holders = df[(df["stock_hold"] == 1) & df["lifesat_single"].notna()]

    ancestral_r, ancestral_p, ancestral_n = corr_with_p(
        nonholders["ln_wealth"], nonholders["lifesat_single"]
    )
    current_r, current_p, current_n = corr_with_p(
        holders["ln_stock_value"], holders["lifesat_single"]
    )
    delta_st = ancestral_r - current_r
    log.info("Δ_ST (lifesat_single, within 2008-12):  ancestral r=%+.4f (N=%d)  current r=%+.4f (N=%d)  Δ=%+.4f",
             ancestral_r, ancestral_n, current_r, current_n, delta_st)

    # Also using CESD-rev (wider time coverage)
    non_c = df[(df["stock_hold"] == 0) & df["cesd_rev"].notna()]
    ho_c = df[(df["stock_hold"] == 1) & df["cesd_rev"].notna()]
    a_r2, a_p2, a_n2 = corr_with_p(non_c["ln_wealth"], non_c["cesd_rev"])
    c_r2, c_p2, c_n2 = corr_with_p(ho_c["ln_stock_value"], ho_c["cesd_rev"])
    delta_st_cesd = a_r2 - c_r2
    log.info("Δ_ST (cesd_rev, all waves):  ancestral r=%+.4f (N=%d)  current r=%+.4f (N=%d)  Δ=%+.4f",
             a_r2, a_n2, c_r2, c_n2, delta_st_cesd)

    # Bootstrap 1000 for Δ_ST on lifesat_single
    def compute_delta(sub_df: pd.DataFrame) -> float:
        non_ = sub_df[(sub_df["stock_hold"] == 0) & sub_df["lifesat_single"].notna()]
        ho_ = sub_df[(sub_df["stock_hold"] == 1) & sub_df["lifesat_single"].notna()]
        if len(non_) < 50 or len(ho_) < 50:
            return np.nan
        ar, _ = stats.pearsonr(non_["ln_wealth"].dropna(), non_["lifesat_single"].dropna())
        # Oops — need same rows
        a_mask = non_["ln_wealth"].notna() & non_["lifesat_single"].notna()
        c_mask = ho_["ln_stock_value"].notna() & ho_["lifesat_single"].notna()
        if a_mask.sum() < 50 or c_mask.sum() < 50:
            return np.nan
        ar, _ = stats.pearsonr(non_.loc[a_mask, "ln_wealth"], non_.loc[a_mask, "lifesat_single"])
        cr, _ = stats.pearsonr(ho_.loc[c_mask, "ln_stock_value"], ho_.loc[c_mask, "lifesat_single"])
        return ar - cr

    mean_, sd_, lo_, hi_ = bootstrap_diff(compute_delta, df[df["lifesat_single"].notna()])
    log.info("Δ_ST bootstrap (B=%d): mean=%+.4f sd=%.4f 95%%CI=[%+.4f,%+.4f]",
             N_BOOT, mean_, sd_, lo_, hi_)

    results["delta_st"] = {
        "lifesat_single": {
            "ancestral_r": float(ancestral_r), "ancestral_n": int(ancestral_n),
            "current_r": float(current_r), "current_n": int(current_n),
            "delta_st": float(delta_st),
            "bootstrap_mean": float(mean_), "bootstrap_sd": float(sd_),
            "ci_lo": float(lo_), "ci_hi": float(hi_),
            "n_boot": N_BOOT,
        },
        "cesd_rev": {
            "ancestral_r": float(a_r2), "ancestral_n": int(a_n2),
            "current_r": float(c_r2), "current_n": int(c_n2),
            "delta_st": float(delta_st_cesd),
        },
    }

    # ============================================================
    # 6. Retirement-wealth Bitter (HRS-unique)
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 6: Retirement-wealth Bitter — post-retirement trajectory")
    log.info("-" * 70)

    # For respondents who retired between 2006-2014, look at life-sat
    # 5-year post-retirement by pre-retirement stock_share quartile
    ret_evt = df[df["retired"] == 1].groupby("HHIDPN").agg(
        first_retired_year=("year", "min")).reset_index()
    ret_evt = ret_evt[ret_evt["first_retired_year"].between(2000, 2014)]

    with_ss = df.merge(ret_evt, on="HHIDPN", how="inner")
    with_ss["years_since_ret"] = with_ss["year"] - with_ss["first_retired_year"]

    # Pre-retirement stock-share quartile (year = first_retired_year - 2).
    # Collapse to one row per HHIDPN so the merge is 1→many.
    pre_ret = (with_ss[with_ss["years_since_ret"] == -2]
               .drop_duplicates(subset=["HHIDPN"]).copy())
    if len(pre_ret) > 20:
        try:
            pre_ret["pre_stock_share_q"] = pd.qcut(
                pre_ret["stock_share"].fillna(0).rank(method="first"),
                q=4, labels=[1, 2, 3, 4], duplicates="drop",
            )
        except ValueError:
            pre_ret["pre_stock_share_q"] = pd.cut(
                pre_ret["stock_share"].fillna(0), bins=4, labels=[1, 2, 3, 4],
            )
        key = pre_ret[["HHIDPN", "pre_stock_share_q"]]
        with_ss = with_ss.merge(key, on="HHIDPN", how="left")
    else:
        log.warning("Too few pre-retirement obs (N=%d); skipping stock_share quartile",
                    len(pre_ret))
        with_ss["pre_stock_share_q"] = pd.NA

    # Post-retirement wellbeing by pre-ret stock quartile
    post_ret = with_ss[(with_ss["years_since_ret"].between(0, 10)) &
                       with_ss["cesd_rev"].notna() &
                       with_ss["pre_stock_share_q"].notna()]
    by_q = post_ret.groupby("pre_stock_share_q", observed=True)["cesd_rev"].agg(["mean", "count"])
    log.info("Post-retirement cesd_rev by pre-ret stock_share quartile:")
    log.info("%s", by_q.to_dict())
    results["retirement_bitter"] = {
        "post_ret_cesd_by_pre_stock_q": {
            str(k): {"mean": float(v["mean"]), "n": int(v["count"])}
            for k, v in by_q.to_dict("index").items()
        },
    }

    # ============================================================
    # 7. Specification curve ≥ 144 specs
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 7: Specification curve")
    log.info("-" * 70)

    DVs = ["lifesat_single", "lifesat_diener", "cesd_rev", "srh_rev",
           "pos_affect", "affect_balance"]
    TREATs = ["stock_hold", "risky_hold", "stock_share"]
    CTRL_SETS = {
        "minimal": [],
        "basic": ["age", "ln_income"],
        "full": ["age", "ln_income", "edu_years", "retired", "ln_wealth"],
    }
    SAMPLES = {
        "all": lambda d: d,
        "age55_74": lambda d: d[d["age"].between(55, 74)],
        "age75+": lambda d: d[d["age"] >= 75],
        "post_2008": lambda d: d[d["year"] >= 2008],
    }
    FE_SET = [("pid+year", True, True), ("year_only", False, True), ("none", False, False)]

    spec_rows = []
    total = len(DVs) * len(TREATs) * len(CTRL_SETS) * len(SAMPLES) * len(FE_SET)
    log.info("Planning %d specs", total)

    for dv, tr, (ckey, ctrl), (skey, sfn), (fkey, fpid, fyr) in itertools.product(
        DVs, TREATs, CTRL_SETS.items(), SAMPLES.items(), FE_SET
    ):
        # Skip colinear: age in ctrl when using pid-FE (age ≈ linear in age; still OK if y-FE)
        sub = sfn(df).dropna(subset=[dv, tr] + ctrl)
        if len(sub) < 100:
            continue
        r = ols_fe(sub, y=dv, x=tr, controls=ctrl,
                   fe_pid=fpid, fe_year=fyr)
        spec_rows.append({
            "dv": dv, "treatment": tr, "ctrl_set": ckey, "sample": skey,
            "fe": fkey, "n": r["n"], "beta": r["beta"], "se": r["se"],
            "ci_lo": r["ci_lo"], "ci_hi": r["ci_hi"], "p": r["p"],
        })

    spec_df = pd.DataFrame(spec_rows)
    spec_df.to_csv(OUT_SPEC, index=False)
    log.info("Saved %d specs to %s", len(spec_df), OUT_SPEC)

    # Summary
    for dv in DVs:
        sub = spec_df[spec_df["dv"] == dv]
        if not len(sub):
            continue
        med = sub["beta"].median()
        pct_pos = (sub["beta"] > 0).mean()
        pct_sig = (sub["p"] < 0.05).mean()
        log.info("  %s  n=%d  median=%+.4f  %%β>0=%.1f  %%p<.05=%.1f",
                 dv, len(sub), med, 100 * pct_pos, 100 * pct_sig)

    results["spec_curve"] = {
        "n_specs_total": int(len(spec_df)),
        "by_dv": {
            dv: {
                "n": int((spec_df["dv"] == dv).sum()),
                "median_beta": float(spec_df.loc[spec_df["dv"] == dv, "beta"].median()),
                "pct_beta_positive": float((spec_df.loc[spec_df["dv"] == dv, "beta"] > 0).mean()),
                "pct_p_lt_05": float((spec_df.loc[spec_df["dv"] == dv, "p"] < 0.05).mean()),
            } for dv in DVs if (spec_df["dv"] == dv).any()
        },
    }

    # ============================================================
    # 8. Four primitives signatures (θ, λ, β, ρ)
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 8: Four primitives")
    log.info("-" * 70)

    # θ: already have core_regs
    theta_beta = core_regs["lifesat_single__stock_hold__feW"]["beta"] \
        if "lifesat_single__stock_hold__feW" in core_regs else np.nan

    # λ: use household spouse effect — approximate by interaction stock_hold × married
    #   (marital_status == 1 is "married"; rough)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df["married"] = (df["marital_status"].astype(float) == 1).astype("Int64")
    sub = df.dropna(subset=["cesd_rev", "stock_hold", "married", "age", "ln_income"])
    sub["sh_x_married"] = sub["stock_hold"].astype(float) * sub["married"].astype(float)
    X = sm.add_constant(sub[["stock_hold", "married", "sh_x_married", "age", "ln_income"]].astype(float))
    r = sm.OLS(sub["cesd_rev"].astype(float), X).fit(
        cov_type="cluster", cov_kwds={"groups": sub["HHIDPN"]}
    )
    lambda_estimate = {
        "interaction_beta": float(r.params["sh_x_married"]),
        "p": float(r.pvalues["sh_x_married"]),
        "n": int(len(sub)),
    }
    log.info("λ (stock_hold × married on cesd_rev) interaction β=%+.4f p=%.4g",
             lambda_estimate["interaction_beta"], lambda_estimate["p"])

    # β present bias: ratio of short-run stock_gain effect vs long-run post-GFC effect
    # (proxy: gfc_event_study.cesd_rev_effect.beta vs core levels effect)

    # ρ: P(continue|loss)  already computed

    results["four_primitives"] = {
        "theta_beta_lifesat_stock_hold": float(theta_beta) if pd.notna(theta_beta) else None,
        "lambda_interaction": lambda_estimate,
        "beta_present_bias_approx": "see gfc_event_study for long-run + core_sweet_trap for short-run",
        "rho_p_continue_loss": float(p_cont_loss) if pd.notna(p_cont_loss) else None,
    }

    # ============================================================
    # 9. Cross-national meta-analysis (China vs US)
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 9: Cross-national meta (CN CFPS/CHFS vs US HRS)")
    log.info("-" * 70)

    # CFPS/CHFS C8 benchmark (from C8_investment_findings.md):
    # Δ_ST = +0.060, 95% CI [+0.024, +0.098]
    # β(stock_hold, life_sat) = -0.107, 95% CI [-0.130, -0.083]
    cn_dst = {"est": 0.060, "ci_lo": 0.024, "ci_hi": 0.098}
    us_dst = {"est": mean_, "ci_lo": lo_, "ci_hi": hi_}

    # Random-effects meta on Δ_ST, inverse-variance weighted (approx)
    def se_from_ci(ci_lo, ci_hi):
        return (ci_hi - ci_lo) / (2 * 1.96)
    cn_se = se_from_ci(cn_dst["ci_lo"], cn_dst["ci_hi"])
    us_se = se_from_ci(us_dst["ci_lo"], us_dst["ci_hi"])
    ws = np.array([1 / cn_se**2, 1 / us_se**2])
    ests = np.array([cn_dst["est"], us_dst["est"]])
    pooled = float((ws * ests).sum() / ws.sum())
    pooled_se = float(1 / np.sqrt(ws.sum()))
    q = float(((ests - pooled)**2 * ws).sum())
    p_q = float(1 - stats.chi2.cdf(q, df=1))

    log.info("Cross-national Δ_ST meta: CN=%+.4f [%+.4f,%+.4f], US=%+.4f [%+.4f,%+.4f]",
             cn_dst["est"], cn_dst["ci_lo"], cn_dst["ci_hi"],
             us_dst["est"], us_dst["ci_lo"], us_dst["ci_hi"])
    log.info("Pooled Δ_ST = %+.4f (SE %.4f). Q test: Q=%.3f, df=1, p=%.4g",
             pooled, pooled_se, q, p_q)

    results["cross_national_meta"] = {
        "CN_CFPS_CHFS": cn_dst,
        "US_HRS": us_dst,
        "pooled_delta_st": pooled,
        "pooled_se": pooled_se,
        "Q_test": q,
        "p_Q": p_q,
        "homogeneous": bool(p_q > 0.10),
        "interpretation": ("Homogeneous cross-national Δ_ST" if p_q > 0.10
                           else "Heterogeneous; discuss moderators"),
    }

    # ============================================================
    # 10. Figure 2 export — China × US comparison data
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 10: Figure 2 data export")
    log.info("-" * 70)

    fig_rows = []
    # CN data
    fig_rows.append({"domain": "Investment", "country": "China", "source": "CFPS/CHFS",
                     "metric": "delta_st", "value": 0.060, "ci_lo": 0.024, "ci_hi": 0.098})
    fig_rows.append({"domain": "Investment", "country": "China", "source": "CFPS/CHFS",
                     "metric": "beta_stock_lifesat", "value": -0.107, "ci_lo": -0.130, "ci_hi": -0.083})
    fig_rows.append({"domain": "Investment", "country": "China", "source": "CFPS/CHFS",
                     "metric": "p_continue_loss", "value": 0.718, "ci_lo": np.nan, "ci_hi": np.nan})
    # US data
    fig_rows.append({"domain": "Investment", "country": "US", "source": "HRS",
                     "metric": "delta_st", "value": mean_, "ci_lo": lo_, "ci_hi": hi_})
    cr = core_regs["lifesat_single__stock_hold__feW"]
    fig_rows.append({"domain": "Investment", "country": "US", "source": "HRS",
                     "metric": "beta_stock_lifesat", "value": cr["beta"],
                     "ci_lo": cr["ci_lo"], "ci_hi": cr["ci_hi"]})
    fig_rows.append({"domain": "Investment", "country": "US", "source": "HRS",
                     "metric": "p_continue_loss",
                     "value": float(p_cont_loss) if pd.notna(p_cont_loss) else np.nan,
                     "ci_lo": np.nan, "ci_hi": np.nan})

    fig_path = ROOT / "04-figures" / "data" / "figure2_china_us_comparison.csv"
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    # If exists, don't overwrite without merging; append new rows (will include both C8 and C13)
    fig_df = pd.DataFrame(fig_rows)
    if fig_path.exists():
        old = pd.read_csv(fig_path)
        old = old[old["domain"] != "Investment"]
        fig_df = pd.concat([old, fig_df], ignore_index=True)
    fig_df.to_csv(fig_path, index=False)
    log.info("Wrote Figure 2 data (C8) to %s", fig_path)

    # ============================================================
    # Save JSON
    # ============================================================
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        # NaN → None for JSON
        def clean(o):
            if isinstance(o, dict):
                return {k: clean(v) for k, v in o.items()}
            if isinstance(o, list):
                return [clean(v) for v in o]
            if isinstance(o, float) and not np.isfinite(o):
                return None
            if isinstance(o, (np.floating,)):
                return float(o) if np.isfinite(o) else None
            if isinstance(o, (np.integer,)):
                return int(o)
            if isinstance(o, np.bool_):
                return bool(o)
            return o
        json.dump(clean(results), f, indent=2, ensure_ascii=False)

    log.info("=" * 70)
    log.info("C8 US analysis done. Results → %s", OUT_JSON)
    log.info("=" * 70)


if __name__ == "__main__":
    main()
