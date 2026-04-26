"""
C13_us_hrs_sweet_trap.py — US HRS replication of CFPS C13 housing Sweet Trap.

Objective
---------
Replicate on US data the CFPS-China C13 findings:
  * F2 aspirational-entry (mortgage rises with income, education, wealth)
  * θ Sweet (event study on mortgage onset → life-sat)
  * Stock-endowment Bitter: debt crowd-IN (non-housing debt rises)
  * Δ_ST comparable to CFPS's ~0.07-0.10

Inputs
------
  02-data/processed/panel_C13_us_hrs.parquet

Outputs
-------
  02-data/processed/C13_us_results.json
  02-data/processed/C13_us_speccurve.csv
  03-analysis/scripts/C13_us_hrs_sweet_trap.log

Seed: 20260417
Date: 2026-04-17
"""

from __future__ import annotations

import hashlib
import itertools
import json
import logging
import sys
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
PANEL_C13 = ROOT / "02-data" / "processed" / "panel_C13_us_hrs.parquet"
OUT_JSON = ROOT / "02-data" / "processed" / "C13_us_results.json"
OUT_SPEC = ROOT / "02-data" / "processed" / "C13_us_speccurve.csv"
LOG_PATH = ROOT / "03-analysis" / "scripts" / "C13_us_hrs_sweet_trap.log"

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
log = logging.getLogger("C13_us")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def corr_with_p(x: pd.Series, y: pd.Series) -> tuple[float, float, int]:
    m = x.notna() & y.notna()
    if m.sum() < 30:
        return np.nan, np.nan, int(m.sum())
    r, p = stats.pearsonr(x[m].astype(float), y[m].astype(float))
    return float(r), float(p), int(m.sum())


def ols_fe(df: pd.DataFrame, y: str, x: str, controls: list[str],
           fe_pid: bool = True, fe_year: bool = True,
           cluster: str = "HHIDPN") -> dict[str, Any]:
    needed = {y, x, cluster, "HHIDPN", "year", *controls}
    sub = df[list(needed)].dropna()
    if len(sub) < 50:
        return {"n": int(len(sub)), "beta": np.nan, "se": np.nan,
                "ci_lo": np.nan, "ci_hi": np.nan, "p": np.nan}
    dmean = sub.copy()
    if fe_pid:
        for c in [y, x] + controls:
            dmean[c] = dmean[c] - dmean.groupby("HHIDPN")[c].transform("mean")
    if fe_year:
        yearD = pd.get_dummies(dmean["year"], prefix="yr", drop_first=True).astype(float)
        X = pd.concat([dmean[[x] + controls], yearD], axis=1)
    else:
        X = dmean[[x] + controls]
    X = sm.add_constant(X.astype(float))
    try:
        res = sm.OLS(dmean[y].astype(float), X, missing="drop").fit(
            cov_type="cluster", cov_kwds={"groups": sub[cluster]}
        )
    except Exception as e:
        log.warning("OLS failed: %s", e)
        return {"n": int(len(sub)), "beta": np.nan, "se": np.nan,
                "ci_lo": np.nan, "ci_hi": np.nan, "p": np.nan}
    b = float(res.params.get(x, np.nan))
    se = float(res.bse.get(x, np.nan))
    ci_lo, ci_hi = res.conf_int().loc[x].tolist() if x in res.params.index else (np.nan, np.nan)
    return {"n": int(len(sub)), "beta": b, "se": se,
            "ci_lo": float(ci_lo), "ci_hi": float(ci_hi),
            "p": float(res.pvalues.get(x, np.nan)),
            "r2_within": float(res.rsquared)}


def bootstrap_diff(func, df, n_boot=N_BOOT, seed=SEED, **kwargs):
    rng = np.random.default_rng(seed)
    ests = []
    ids = df["HHIDPN"].unique()
    for _ in range(n_boot):
        s = rng.choice(ids, size=len(ids), replace=True)
        sub = df[df["HHIDPN"].isin(s)]
        try:
            ests.append(func(sub, **kwargs))
        except Exception:
            ests.append(np.nan)
    e = np.array([x for x in ests if np.isfinite(x)])
    if len(e) < 10:
        return np.nan, np.nan, np.nan, np.nan
    lo, hi = np.percentile(e, [2.5, 97.5])
    return float(e.mean()), float(e.std()), float(lo), float(hi)


# ============================================================

def main() -> None:
    log.info("=" * 70)
    log.info("C13 US HRS Sweet Trap analysis — start")
    log.info("=" * 70)
    log.info("Panel: %s", PANEL_C13)
    log.info("Panel SHA-256: %s", sha256(PANEL_C13))

    df = pd.read_parquet(PANEL_C13)
    log.info("Loaded %d rows × %d cols, %d unique pids",
             len(df), df.shape[1], df["HHIDPN"].nunique())

    results: dict[str, Any] = {"_meta": {
        "seed": SEED,
        "panel_sha256": sha256(PANEL_C13),
        "n_rows": int(len(df)),
        "n_pid": int(df["HHIDPN"].nunique()),
    }}

    # ============================================================
    # 1. F2 strict diagnosis
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 1: F2 aspirational-entry diagnosis (strict)")
    log.info("-" * 70)

    f2_tests = {
        "cor_has_mortgage_ln_income":
            corr_with_p(df["has_mortgage"].astype(float), df["ln_income"]),
        "cor_has_mortgage_edu_years":
            corr_with_p(df["has_mortgage"].astype(float), df["edu_years"]),
        "cor_has_mortgage_ln_wealth":
            corr_with_p(df["has_mortgage"].astype(float), df["ln_wealth"]),
        "cor_mortgage_burden_ln_income":
            corr_with_p(df["mortgage_burden"], df["ln_income"]),
        "cor_mortgage_burden_edu_years":
            corr_with_p(df["mortgage_burden"], df["edu_years"]),
        "cor_home_own_ln_income":
            corr_with_p(df["home_own"].astype(float), df["ln_income"]),
        "cor_home_own_edu_years":
            corr_with_p(df["home_own"].astype(float), df["edu_years"]),
        "cor_ln_home_value_edu_years":
            corr_with_p(df["ln_home_value"], df["edu_years"]),
    }
    for k, (r, p, n) in f2_tests.items():
        log.info("  %-40s  r=%+.4f  p=%.4g  N=%d", k, r, p, n)

    # Tertile participation
    inc = df.dropna(subset=["ln_income", "has_mortgage"]).copy()
    inc["inc_tert"] = inc.groupby("year")["ln_income"].transform(
        lambda s: pd.qcut(s, 3, labels=[1, 2, 3], duplicates="drop")
    )
    tert_mort = inc.groupby("inc_tert", observed=True)["has_mortgage"].mean().round(4)
    log.info("Has-mortgage by income tertile (among owners): %s", tert_mort.to_dict())

    edu_df = df.dropna(subset=["edu_years", "has_mortgage"]).copy()
    edu_df["edu_bucket"] = pd.cut(
        edu_df["edu_years"], bins=[-1, 11, 12, 15, 30],
        labels=["<HS", "HS", "some_col", "col+"],
    )
    edu_mort = edu_df.groupby("edu_bucket", observed=True)["has_mortgage"].mean().round(4)
    log.info("Has-mortgage by education bucket: %s", edu_mort.to_dict())

    results["F2_diagnosis"] = {
        "correlations": {k: {"r": r, "p": p, "n": n} for k, (r, p, n) in f2_tests.items()},
        "income_tertile_mortgage": {str(k): float(v) for k, v in tert_mort.to_dict().items()},
        "education_bucket_mortgage": {str(k): float(v) for k, v in edu_mort.to_dict().items()},
    }

    # Pass check — for US the focal F2 variable is `has_mortgage`
    t1 = f2_tests["cor_has_mortgage_ln_income"][0]
    t2 = f2_tests["cor_has_mortgage_edu_years"][0]
    passes = (t1 > 0.05) and (t2 > 0.05) and (tert_mort.iloc[-1] > 1.5 * tert_mort.iloc[0])
    results["F2_verdict"] = "PASS" if passes else "PARTIAL"
    log.info("F2 VERDICT: %s", results["F2_verdict"])

    # ============================================================
    # 2. Core Sweet Trap — within-person FE
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 2: Core Sweet Trap — mortgage burden → welfare (person-FE)")
    log.info("-" * 70)

    ctrl = ["age", "ln_income", "retired"]
    core_regs = {}
    for y in ["lifesat_single", "lifesat_diener", "cesd_rev", "srh_rev",
              "pos_affect", "affect_balance"]:
        for x in ["mortgage_burden", "has_mortgage", "ln_mortgage", "ltv"]:
            key = f"{y}__{x}__feW"
            sub = df.dropna(subset=[y, x] + ctrl)
            r = ols_fe(sub, y=y, x=x, controls=ctrl)
            core_regs[key] = r
            log.info("  %-42s  N=%d  β=%+.4f  p=%.4g  CI=[%+.4f,%+.4f]",
                     key, r["n"], r["beta"], r["p"], r["ci_lo"], r["ci_hi"])

    results["core_sweet_trap"] = core_regs

    # ============================================================
    # 3. Event study: mortgage onset (0→1)
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 3: Event study — first mortgage onset")
    log.info("-" * 70)

    # For each person, the first wave when mortgage_onset == 1
    onset = df[df["mortgage_onset"] == 1].groupby("HHIDPN").agg(
        first_mort_year=("year", "min")).reset_index()
    log.info("N first-onset events: %d", len(onset))

    evt = df.merge(onset, on="HHIDPN", how="inner")
    evt["years_since_onset"] = evt["year"] - evt["first_mort_year"]
    # Keep ±6 years around event
    evt = evt[evt["years_since_onset"].between(-6, 10)]

    # Event-time regression — dummy for each year
    # Use cesd_rev (widest coverage)
    event_results = {}
    for dv in ["cesd_rev", "srh_rev", "lifesat_single", "lifesat_diener"]:
        sub = evt.dropna(subset=[dv, "age", "ln_income"])
        if len(sub) < 500:
            continue
        # Year since onset dummies, reference = −2
        ysd = pd.get_dummies(sub["years_since_onset"].astype(int), prefix="t").astype(float)
        # Drop t_-2 as reference
        if "t_-2" in ysd.columns:
            ysd = ysd.drop("t_-2", axis=1)
        # Demean within person
        sub_dm = sub.copy()
        for c in [dv, "age", "ln_income"]:
            sub_dm[c] = sub_dm[c] - sub_dm.groupby("HHIDPN")[c].transform("mean")
        ysd_dm = ysd.copy()
        for col in ysd_dm.columns:
            ysd_dm[col] = ysd_dm[col] - ysd_dm.groupby(sub["HHIDPN"])[col].transform("mean")
        yearD = pd.get_dummies(sub["year"], prefix="yr", drop_first=True).astype(float)
        X = pd.concat([ysd_dm, sub_dm[["age", "ln_income"]], yearD], axis=1)
        X = sm.add_constant(X.astype(float))
        res = sm.OLS(sub_dm[dv].astype(float), X).fit(
            cov_type="cluster", cov_kwds={"groups": sub["HHIDPN"]}
        )
        event_results[dv] = {}
        for t in [-6, -4, 0, 2, 4, 6, 8, 10]:
            col = f"t_{t}"
            if col in res.params.index:
                event_results[dv][str(t)] = {
                    "beta": float(res.params[col]),
                    "se": float(res.bse[col]),
                    "p": float(res.pvalues[col]),
                    "n": int(len(sub)),
                }
        log.info("Event study %s (t_-2 is ref):", dv)
        for t, r in event_results[dv].items():
            log.info("  t=%s  β=%+.4f  SE=%.4f  p=%.4g", t, r["beta"], r["se"], r["p"])

    results["event_study"] = event_results

    # ============================================================
    # 4. Debt crowd-IN (Bitter primary signature from CFPS C13)
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 4: Debt crowd-IN (Bitter)")
    log.info("-" * 70)

    # Within-person regression: Δ mortgage → Δ non-housing debt
    debt_reg = {}
    for y in ["ln_nonhousing_debt"]:
        for x in ["has_mortgage", "mortgage_burden", "ln_mortgage"]:
            key = f"{y}__{x}"
            sub = df.dropna(subset=[y, x, "age", "ln_income"])
            r = ols_fe(sub, y=y, x=x, controls=["age", "ln_income"])
            debt_reg[key] = r
            log.info("  %-40s  N=%d  β=%+.4f  p=%.4g  CI=[%+.4f,%+.4f]",
                     key, r["n"], r["beta"], r["p"], r["ci_lo"], r["ci_hi"])

    # Onset event study on non-housing debt
    sub = evt.dropna(subset=["ln_nonhousing_debt", "age", "ln_income"])
    if len(sub) > 500:
        ysd = pd.get_dummies(sub["years_since_onset"], prefix="t").astype(float)
        for col in list(ysd.columns):
            if col in ["t_-2.0", "t_-2"]:
                ysd = ysd.drop(col, axis=1)
        sub_dm = sub.copy()
        for c in ["ln_nonhousing_debt", "age", "ln_income"]:
            sub_dm[c] = sub_dm[c] - sub_dm.groupby("HHIDPN")[c].transform("mean")
        ysd_dm = ysd.copy()
        for col in ysd_dm.columns:
            ysd_dm[col] = ysd_dm[col] - ysd_dm.groupby(sub["HHIDPN"])[col].transform("mean")
        yearD = pd.get_dummies(sub["year"], prefix="yr", drop_first=True).astype(float)
        X = pd.concat([ysd_dm, sub_dm[["age", "ln_income"]], yearD], axis=1)
        X = sm.add_constant(X.astype(float))
        res = sm.OLS(sub_dm["ln_nonhousing_debt"].astype(float), X).fit(
            cov_type="cluster", cov_kwds={"groups": sub["HHIDPN"]}
        )
        debt_event = {}
        for t in [-6, -4, 0, 2, 4, 6, 8, 10]:
            col = f"t_{t}"
            if col in res.params.index:
                debt_event[str(t)] = {
                    "beta": float(res.params[col]),
                    "se": float(res.bse[col]),
                    "p": float(res.pvalues[col]),
                }
        log.info("Event study non-housing debt (ref t=-2):")
        for t, r in debt_event.items():
            log.info("  t=%s  β=%+.4f  SE=%.4f  p=%.4g", t, r["beta"], r["se"], r["p"])
        debt_reg["event_study_nonhousing_debt"] = debt_event
    else:
        log.warning("Too few obs for non-housing-debt event study.")

    results["bitter_debt_crowdin"] = debt_reg

    # ============================================================
    # 5. Δ_ST estimation
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 5: Δ_ST — reward-fitness decoupling for housing")
    log.info("-" * 70)

    # Ancestral: non-mortgage-holder cor(ln_wealth, life-sat)
    # Current:   mortgage-holder cor(ln_home_value, life-sat)
    non_m = df[(df["has_mortgage"] == 0) & df["lifesat_single"].notna()]
    has_m = df[(df["has_mortgage"] == 1) & df["lifesat_single"].notna()]
    a_r, a_p, a_n = corr_with_p(non_m["ln_wealth"], non_m["lifesat_single"])
    c_r, c_p, c_n = corr_with_p(has_m["ln_home_value"], has_m["lifesat_single"])
    d_life = a_r - c_r
    log.info("Δ_ST (lifesat_single): ancestral r=%+.4f (N=%d) current r=%+.4f (N=%d) Δ=%+.4f",
             a_r, a_n, c_r, c_n, d_life)

    # With CESD (broader)
    non_m2 = df[(df["has_mortgage"] == 0) & df["cesd_rev"].notna()]
    has_m2 = df[(df["has_mortgage"] == 1) & df["cesd_rev"].notna()]
    a2, a2p, a2n = corr_with_p(non_m2["ln_wealth"], non_m2["cesd_rev"])
    c2, c2p, c2n = corr_with_p(has_m2["ln_home_value"], has_m2["cesd_rev"])
    d_cesd = a2 - c2
    log.info("Δ_ST (cesd_rev): ancestral r=%+.4f (N=%d) current r=%+.4f (N=%d) Δ=%+.4f",
             a2, a2n, c2, c2n, d_cesd)

    # Alternative: use mortgage_burden as reward signal
    has_m3 = df[(df["has_mortgage"] == 1) & df["lifesat_single"].notna()]
    c3, c3p, c3n = corr_with_p(has_m3["mortgage_burden"], has_m3["lifesat_single"])
    d_burden = a_r - c3
    log.info("Δ_ST (lifesat via mortgage_burden): ancestral r=%+.4f, current r=%+.4f, Δ=%+.4f",
             a_r, c3, d_burden)

    # Bootstrap lifesat Δ_ST
    def compute_delta(subdf: pd.DataFrame) -> float:
        nm = subdf[(subdf["has_mortgage"] == 0) & subdf["lifesat_single"].notna() & subdf["ln_wealth"].notna()]
        hm = subdf[(subdf["has_mortgage"] == 1) & subdf["lifesat_single"].notna() & subdf["ln_home_value"].notna()]
        if len(nm) < 50 or len(hm) < 50:
            return np.nan
        ar, _ = stats.pearsonr(nm["ln_wealth"], nm["lifesat_single"])
        cr, _ = stats.pearsonr(hm["ln_home_value"], hm["lifesat_single"])
        return ar - cr

    mean_, sd_, lo_, hi_ = bootstrap_diff(compute_delta, df[df["lifesat_single"].notna()])
    log.info("Δ_ST bootstrap (B=%d): mean=%+.4f sd=%.4f 95%%CI=[%+.4f,%+.4f]",
             N_BOOT, mean_, sd_, lo_, hi_)

    results["delta_st"] = {
        "lifesat_single_via_wealth_home": {
            "ancestral_r": float(a_r), "ancestral_n": int(a_n),
            "current_r": float(c_r), "current_n": int(c_n),
            "delta_st": float(d_life),
            "bootstrap_mean": float(mean_),
            "bootstrap_sd": float(sd_),
            "ci_lo": float(lo_), "ci_hi": float(hi_),
            "n_boot": N_BOOT,
        },
        "cesd_rev": {
            "ancestral_r": float(a2), "ancestral_n": int(a2n),
            "current_r": float(c2), "current_n": int(c2n),
            "delta_st": float(d_cesd),
        },
        "lifesat_via_mortgage_burden": {
            "ancestral_r": float(a_r), "current_r": float(c3),
            "delta_st": float(d_burden),
        },
    }

    # ============================================================
    # 6. ρ lock-in — mortgage persistence
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 6: ρ lock-in")
    log.info("-" * 70)

    lock_df = df.dropna(subset=["has_mortgage", "has_mortgage_lag"])
    lock_df_has = lock_df[lock_df["has_mortgage_lag"] == 1]
    p_cont_mort = lock_df_has["has_mortgage"].mean()
    log.info("P(has_mortgage_t | has_mortgage_{t-1}) = %.3f (N=%d)",
             p_cont_mort, len(lock_df_has))

    # 2006→2008 GFC: pre-GFC mortgage holders' retention to 2010-2020
    pre2006_mort = df[df["year"] == 2006][["HHIDPN", "has_mortgage"]].rename(
        columns={"has_mortgage": "pre2006_mort"})
    pre2006_mort = pre2006_mort.dropna(subset=["pre2006_mort"])
    d_gfc = df.merge(pre2006_mort[pre2006_mort["pre2006_mort"] == 1], on="HHIDPN", how="inner")
    exit_traj = {}
    for yr in [2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020]:
        sub = d_gfc[(d_gfc["year"] == yr)]["has_mortgage"]
        rate = sub.mean()
        exit_traj[str(yr)] = {"N": int(sub.notna().sum()),
                              "retention": float(rate) if pd.notna(rate) else None}
        log.info("  year=%d: pre-2006 mortgage holders retention=%.3f N=%d",
                 yr, rate, sub.notna().sum())

    # Within-person AR(1) for log home value
    within_ar1_home = df.dropna(subset=["ln_home_value", "home_value_lag"])
    within_ar1_home["ln_home_value_lag"] = np.arcsinh(within_ar1_home["home_value_lag"])
    ar1_home_r, _, _ = corr_with_p(within_ar1_home["ln_home_value"],
                                     within_ar1_home["ln_home_value_lag"])
    log.info("Within-person AR(1) ln_home_value = %+.3f", ar1_home_r)

    results["rho_lockin"] = {
        "p_continue_mortgage": float(p_cont_mort),
        "n_continue_mortgage": int(len(lock_df_has)),
        "gfc_pre2006_mort_retention_trajectory": exit_traj,
        "within_pid_ar1_ln_home_value": float(ar1_home_r),
    }

    # ============================================================
    # 7. Specification curve ≥ 144 specs
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 7: Specification curve")
    log.info("-" * 70)

    DVs = ["lifesat_single", "lifesat_diener", "cesd_rev", "srh_rev", "pos_affect"]
    TREATs = ["has_mortgage", "mortgage_burden", "ln_mortgage", "ltv"]
    CTRL_SETS = {
        "minimal": [],
        "basic": ["age", "ln_income"],
        "full": ["age", "ln_income", "edu_years", "retired", "ln_wealth"],
    }
    SAMPLES = {
        "all": lambda d: d,
        "owners": lambda d: d[d["home_own"] == 1],
        "age55_74": lambda d: d[d["age"].between(55, 74)],
        "post_2008": lambda d: d[d["year"] >= 2008],
    }
    FE_SET = [("pid+year", True, True), ("year_only", False, True), ("none", False, False)]

    rows = []
    for dv, tr, (ckey, ctrl), (skey, sfn), (fkey, fpid, fyr) in itertools.product(
        DVs, TREATs, CTRL_SETS.items(), SAMPLES.items(), FE_SET
    ):
        sub = sfn(df).dropna(subset=[dv, tr] + ctrl)
        if len(sub) < 100:
            continue
        r = ols_fe(sub, y=dv, x=tr, controls=ctrl, fe_pid=fpid, fe_year=fyr)
        rows.append({
            "dv": dv, "treatment": tr, "ctrl_set": ckey, "sample": skey,
            "fe": fkey, "n": r["n"], "beta": r["beta"], "se": r["se"],
            "ci_lo": r["ci_lo"], "ci_hi": r["ci_hi"], "p": r["p"],
        })

    spec_df = pd.DataFrame(rows)
    spec_df.to_csv(OUT_SPEC, index=False)
    log.info("Saved %d specs to %s", len(spec_df), OUT_SPEC)
    for dv in DVs:
        s = spec_df[spec_df["dv"] == dv]
        if not len(s):
            continue
        log.info("  %s  n=%d  median_β=%+.4f  %%β>0=%.1f  %%p<.05=%.1f",
                 dv, len(s), s["beta"].median(),
                 100 * (s["beta"] > 0).mean(), 100 * (s["p"] < 0.05).mean())

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
    # 8. Four primitives signatures
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 8: Four primitives")
    log.info("-" * 70)

    theta = core_regs.get("lifesat_single__mortgage_burden__feW", {}).get("beta", np.nan)
    rho = float(p_cont_mort)
    # λ: age interaction — younger mortgage holders (age<60) may have stronger external
    df["young"] = (df["age"] < 65).astype("Int64")
    sub = df.dropna(subset=["cesd_rev", "mortgage_burden", "young", "age", "ln_income"])
    sub = sub.copy()
    sub["mb_x_young"] = sub["mortgage_burden"] * sub["young"].astype(float)
    # person-FE
    for c in ["cesd_rev", "mortgage_burden", "mb_x_young", "ln_income"]:
        sub[c] = sub[c] - sub.groupby("HHIDPN")[c].transform("mean")
    yearD = pd.get_dummies(sub["year"], prefix="yr", drop_first=True).astype(float)
    X = pd.concat([sub[["mortgage_burden", "mb_x_young", "ln_income"]], yearD], axis=1)
    X = sm.add_constant(X.astype(float))
    res = sm.OLS(sub["cesd_rev"].astype(float), X).fit(
        cov_type="cluster", cov_kwds={"groups": sub["HHIDPN"]}
    )
    lambda_interaction = {
        "beta": float(res.params["mb_x_young"]),
        "se": float(res.bse["mb_x_young"]),
        "p": float(res.pvalues["mb_x_young"]),
        "n": int(len(sub)),
    }
    log.info("λ (mortgage_burden × young on cesd_rev): β=%+.4f p=%.4g",
             lambda_interaction["beta"], lambda_interaction["p"])

    results["four_primitives"] = {
        "theta_beta": float(theta) if pd.notna(theta) else None,
        "rho_p_continue_mortgage": rho,
        "lambda_interaction_age_young": lambda_interaction,
        "beta_present_bias_approx": "see event_study trajectory",
    }

    # ============================================================
    # 9. Cross-national meta
    # ============================================================
    log.info("-" * 70)
    log.info("STEP 9: Cross-national meta")
    log.info("-" * 70)

    # CFPS C13 benchmark:
    # Δ_ST (dw, ancestral-baseline): +0.071 [+0.037, +0.109]
    # β mortgage_burden → qn12012 = +0.195 (CFPS), 95% CI [+0.107, +0.283]
    cn_dst = {"est": 0.068, "ci_lo": 0.051, "ci_hi": 0.085}  # time-split resivalue→dw
    us_dst = {"est": mean_, "ci_lo": lo_, "ci_hi": hi_}

    def se_from_ci(lo, hi):
        return (hi - lo) / (2 * 1.96)
    cn_se = se_from_ci(cn_dst["ci_lo"], cn_dst["ci_hi"])
    us_se = se_from_ci(us_dst["ci_lo"], us_dst["ci_hi"])
    ws = np.array([1 / cn_se**2, 1 / us_se**2])
    ests = np.array([cn_dst["est"], us_dst["est"]])
    pooled = float((ws * ests).sum() / ws.sum())
    pooled_se = float(1 / np.sqrt(ws.sum()))
    q = float(((ests - pooled)**2 * ws).sum())
    p_q = float(1 - stats.chi2.cdf(q, df=1))

    log.info("CN Δ_ST = %+.4f [%+.4f,%+.4f]", cn_dst["est"], cn_dst["ci_lo"], cn_dst["ci_hi"])
    log.info("US Δ_ST = %+.4f [%+.4f,%+.4f]", us_dst["est"], us_dst["ci_lo"], us_dst["ci_hi"])
    log.info("Pooled = %+.4f  Q=%.3f  p_Q=%.4g", pooled, q, p_q)

    results["cross_national_meta"] = {
        "CN_CFPS": cn_dst,
        "US_HRS": us_dst,
        "pooled_delta_st": pooled,
        "pooled_se": pooled_se,
        "Q_test": q,
        "p_Q": p_q,
        "homogeneous": bool(p_q > 0.10),
    }

    # ============================================================
    # 10. Figure 2 export
    # ============================================================
    fig_path = ROOT / "04-figures" / "data" / "figure2_china_us_comparison.csv"
    fig_rows = []
    fig_rows.append({"domain": "Housing", "country": "China", "source": "CFPS",
                     "metric": "delta_st", "value": 0.068, "ci_lo": 0.051, "ci_hi": 0.085})
    fig_rows.append({"domain": "Housing", "country": "China", "source": "CFPS",
                     "metric": "beta_mortburden_lifesat", "value": 0.195, "ci_lo": 0.107, "ci_hi": 0.283})
    fig_rows.append({"domain": "Housing", "country": "China", "source": "CFPS",
                     "metric": "debt_crowd_in_coef", "value": 0.93, "ci_lo": np.nan, "ci_hi": np.nan})
    cr = core_regs.get("lifesat_single__mortgage_burden__feW", {})
    fig_rows.append({"domain": "Housing", "country": "US", "source": "HRS",
                     "metric": "delta_st", "value": mean_, "ci_lo": lo_, "ci_hi": hi_})
    fig_rows.append({"domain": "Housing", "country": "US", "source": "HRS",
                     "metric": "beta_mortburden_lifesat",
                     "value": cr.get("beta", np.nan),
                     "ci_lo": cr.get("ci_lo", np.nan), "ci_hi": cr.get("ci_hi", np.nan)})
    dr = debt_reg.get("ln_nonhousing_debt__has_mortgage", {})
    fig_rows.append({"domain": "Housing", "country": "US", "source": "HRS",
                     "metric": "debt_crowd_in_coef",
                     "value": dr.get("beta", np.nan),
                     "ci_lo": dr.get("ci_lo", np.nan), "ci_hi": dr.get("ci_hi", np.nan)})

    df_fig = pd.DataFrame(fig_rows)
    if fig_path.exists():
        old = pd.read_csv(fig_path)
        old = old[old["domain"] != "Housing"]
        df_fig = pd.concat([old, df_fig], ignore_index=True)
    df_fig.to_csv(fig_path, index=False)
    log.info("Wrote Figure 2 data (C13) to %s", fig_path)

    # ============================================================
    # Save JSON
    # ============================================================
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
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(clean(results), f, indent=2, ensure_ascii=False)

    log.info("=" * 70)
    log.info("C13 US analysis complete. Results → %s", OUT_JSON)
    log.info("=" * 70)


if __name__ == "__main__":
    main()
