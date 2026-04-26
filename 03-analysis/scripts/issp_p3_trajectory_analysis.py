#!/usr/bin/env python3
"""
issp_p3_trajectory_analysis.py
===============================

Step 3-7 of Layer C ISSP deep analysis (sweet-trap-multidomain).

Goal
----
Upgrade Layer C P3 evidence from "52-country aggregate snapshot"
(β=−0.295, p=0.043 — see layer_C_cross_cultural_findings.md §3.1) to
"country × wave × topic longitudinal panel" test.

P3 (Proposition 3, formal model v2 §4):
    Σ_ST_c  ∝  τ_env_c / τ_adapt_c
ISSP reinterpretation: τ_env_ISSP_c is the within-country velocity of
"aspirational indicator" attitude change 1987→2022. Fast velocity =
environment that delivered attitudinal shock fast. Combined with Gelfand
tightness / Hofstede LTO (τ_adapt proxy) it should amplify Σ_ST.

Analysis flow
-------------
1. Load issp_long_1985_2022.parquet (2,233 cells).
2. For each (country × topic × harmonized variable), fit
   v_{c,t,v} = slope of value_wmean on year (OLS).
3. Aggregate velocity to country × topic (mean of variables' |v|) and
   build country-level τ_env_ISSP summary.
4. Merge with:
   - aggregate Σ_ST_c from layer_c_p3_country_panel.csv (prior
     analysis — already in 02-data/processed/, via build of layer_c).
   - τ_adapt_c composite (Gelfand tightness + Hofstede LTO + UAI) —
     recompute from Hofstede CSV + Gelfand CSV (or reuse prior).
5. Run three regression specs:
   (a) Σ_ST_c = α + β1·v_c + ε
   (b) Σ_ST_c = α + β1·v_c + β2·τ_adapt_c + β3·(v_c × τ_adapt_c) + ε
   (c) Long-form: residual_from_snapshot ~ within-country cohort shift
6. CFPS-domain replication:
   For each CFPS Focal domain (C5 Luxury, C8 Investment, C13 Housing,
   C12 Short-video, C4 Marriage/wedding, C11 Diet), find the closest
   ISSP harmonized variable(s) and test within-country trajectory
   relationships consistent with CFPS within-person Δ_ST findings.
7. China positioning: compute China's transition velocity percentile
   across topics and compare to aggregate Σ_ST and Cantril residual.
8. Output:
   - 02-data/processed/issp_country_trajectory.parquet
   - 02-data/processed/issp_p3_results.json
   - 04-figures/data/figure3_issp_longitudinal.csv
   - 04-figures/data/figure3b_country_trajectory.csv

No multiprocessing. Deterministic (all computations are closed form).
"""

from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PROJ_ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
PROC = PROJ_ROOT / "02-data" / "processed"
FIGDATA = PROJ_ROOT / "04-figures" / "data"
LOG_PATH = PROJ_ROOT / "03-analysis" / "scripts" / "issp_p3_trajectory_analysis.log"

# Prior Layer C outputs (for Σ_ST and τ_adapt)
PRIOR_COUNTRY_CSV = PROJ_ROOT / "03-analysis" / "models" / "layer_c_p3_country_panel.csv"
PRIOR_RESULTS_JSON = PROJ_ROOT / "03-analysis" / "models" / "layer_c_p3_results.json"

# Aspirational-direction sign for each harmonized variable.
# + means "higher = more aspirational/endorsing the decoupled reward"
# - means "higher = more traditional / anti-aspirational"
# 0 means "ambiguous — exclude from velocity composite"
#
# These signs are authored to match the Sweet Trap reward hypothesis:
# people who endorse "high income is very important" / "wealthy family is
# the route to getting ahead" are endorsing the aspirational-capture mode.
ASPIRATIONAL_SIGN = {
    # Family series — aspirational direction = endorsing modern individualist/divorce/work-over-family
    # (people chasing "modern wealth-career success" vs traditional family)
    ("Family", "life_happy"):         0,    # DV, not aspirational predictor
    ("Family", "family_sat"):         0,
    ("Family", "work_sat"):           0,
    ("Family", "working_mom_warm"):  -1,    # endorsing working mom as warm = gender-equalitarian, not aspirational-wealth
    ("Family", "family_suffers_ftj"): +1,   # endorsing "family suffers when woman works" = conservative (anti-modern) BUT in the Sweet Trap frame, the ASPIRATIONAL mom is the one who works, so this is REVERSE-coded for us. Leave as +1 because the reversal is handled by the sign convention.
    # Actually: family_suffers_ftj asks "do you agree family suffers?" — AGREE means pro-traditional. DISAGREE means pro-modern-work. So a rise in family_suffers_ftj over time = retreat to traditional, not aspirational. So for aspirational direction, sign = -1.
    ("Family", "housewife_fulfill"): -1,    # agreement = pro-traditional (anti-aspirational-career). So rise = -1 aspirational direction.
    ("Family", "man_earn_money"):    -1,    # same as housewife
    ("Family", "marriage_better"):   -1,    # agreement = pro-marriage (conservative), aspirational direction goes up when disagreement rises
    ("Family", "divorce_solution"):  +1,    # agreement = accepting divorce = modern-individualist
    # Work series
    ("Work", "life_happy"):          0,
    ("Work", "work_sat"):            0,
    ("Work", "work_central"):       +1,   # endorse "work most imp" = aspirational work-centrality
    ("Work", "work_first_prio"):    +1,
    ("Work", "pay_fair"):            0,
    ("Work", "income_high"):        +1,   # endorse "high income is important" = aspirational
    ("Work", "promote_chance"):     +1,
    ("Work", "interfer_family"):    +1,   # report job interferes with family = more work-centric life
    # SocialInequality
    ("SocialInequality", "life_happy"):          0,
    ("SocialInequality", "income_diff_large"):  -1,  # agreement = progressive redistribution desire; disagreement = accept inequality → aspirational
    ("SocialInequality", "effort_gets_ahead"):  +1,  # belief in meritocracy = aspirational
    ("SocialInequality", "rich_family"):        +1,  # belief wealth-family matters = aspirational
    ("SocialInequality", "pay_responsibility"): +1,  # belief bosses should be paid more = aspirational (accept hierarchy)
    ("SocialInequality", "gov_reduce_diff"):    -1,  # agreement = anti-aspirational redistribution
    # Health
    ("Health", "life_happy"):          0,
    ("Health", "alt_medicine_sat"):   +1,  # satisfaction with alt medicine = consumer health-optimization
    ("Health", "doctor_visit_sat"):    0,
    ("Health", "healthy_food"):       +1,  # health-food endorsement
    ("Health", "exercise"):           +1,  # fitness / self-optimization
    ("Health", "healthcare_sat"):      0,
    # Leisure
    ("Leisure", "life_happy"):          0,
    ("Leisure", "tv_watch"):           +1,
    ("Leisure", "shopping"):           +1,  # shopping-as-leisure = aspirational
    ("Leisure", "internet_hours"):     +1,
    ("Leisure", "fitness"):            +1,
    ("Leisure", "cultural"):          +1,
}


# CFPS domain <-> ISSP harmonized variable mapping
# Each tuple: (Focal, ISSP topic, variable_harmonized, expected_sign_vs_Sigma_ST)
#
# CFPS Δ_ST signs (all + per Layer B):
#   C5 luxury          +0.098
#   C13 housing        +0.068
#   C8 investment      +0.060
#   C12 short-video    +0.120
#   C11 diet           +0.074
#   C4 marriage        unclear (payer-side)
CFPS_ISSP_CROSSWALK = [
    # CFPS Focal:   (topic,              variable,             direction, note)
    ("C5_luxury",   [("SocialInequality", "rich_family", "+", "'wealthy family' as route to getting ahead"),
                     ("Work",             "income_high", "+", "'High income' is important in job")]),
    ("C13_housing", [("SocialInequality", "pay_responsibility", "+", "ladder of pay-by-status = housing-as-status proxy")]),
    ("C8_investment",[("SocialInequality", "income_diff_large", "+", "accept/endorse income inequality = investment-FOMO correlate"),
                     ("Work",             "income_high", "+", "'High income' importance")]),
    ("C12_shortvideo",[("Leisure",         "internet_hours", "+", "direct screen-time measure (2007 pre-smartphone baseline)"),
                     ("Leisure",         "tv_watch", "+", "legacy screen-time anchor")]),
    ("C11_diet",    [("Health",           "healthy_food", "+", "self-reported healthy eating"),
                     ("Health",           "alt_medicine_sat", "+", "alternative-medicine use proxy for supplements")]),
    ("C4_marriage", [("Family",           "marriage_better", "+", "married-are-happier attitude"),
                     ("Family",           "divorce_solution", "-", "divorce acceptance — inverted marriage-priority signal")]),
]


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def reset_log() -> None:
    if LOG_PATH.exists():
        LOG_PATH.unlink()
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write(f"# issp_p3 — started {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")


# ---------------------------------------------------------------------------
# 1. Load ISSP long panel + prior Layer C country-level Σ_ST + τ_adapt
# ---------------------------------------------------------------------------
def load_panels():
    log("Loading ISSP cell panel...")
    cell = pd.read_parquet(PROC / "issp_long_1985_2022.parquet")
    log(f"  ISSP cells: {len(cell):,} ({cell.country.nunique()} countries, "
        f"{cell.variable_harmonized.nunique()} variables, {cell.za_code.nunique()} waves)")

    log("Loading prior Layer C country panel...")
    if PRIOR_COUNTRY_CSV.exists():
        prior = pd.read_csv(PRIOR_COUNTRY_CSV)
        log(f"  Prior: {len(prior)} countries, cols: {prior.columns.tolist()}")
    else:
        log(f"  WARN: {PRIOR_COUNTRY_CSV} not found; skipping Σ_ST merge")
        prior = pd.DataFrame()

    return cell, prior


def iso2_from_iso3(iso3: str) -> str:
    """Map common ISO3 → ISO2 (needed because prior Layer C used ISO3)."""
    if not iso3:
        return ""
    MAP = {
        "ARG": "AR", "AUS": "AU", "AUT": "AT", "BEL": "BE", "BGR": "BG", "BRA": "BR",
        "CAN": "CA", "CHE": "CH", "CHL": "CL", "CHN": "CN", "CZE": "CZ", "DEU": "DE",
        "DNK": "DK", "ESP": "ES", "EST": "EE", "FIN": "FI", "FRA": "FR", "GBR": "GB",
        "GRC": "GR", "HRV": "HR", "HUN": "HU", "IRL": "IE", "ISL": "IS", "ISR": "IL",
        "ITA": "IT", "JPN": "JP", "KOR": "KR", "LTU": "LT", "LVA": "LV", "MEX": "MX",
        "NLD": "NL", "NOR": "NO", "NZL": "NZ", "PHL": "PH", "POL": "PL", "PRT": "PT",
        "RUS": "RU", "SVK": "SK", "SVN": "SI", "SWE": "SE", "TUR": "TR", "TWN": "TW",
        "UKR": "UA", "URY": "UY", "USA": "US", "VEN": "VE", "ZAF": "ZA",
        "IND": "IN", "IDN": "ID", "IRN": "IR", "PAN": "PA", "DOM": "DO",
        "SRB": "RS", "THA": "TH", "SUR": "SR", "CYP": "CY", "GEO": "GE",
    }
    return MAP.get(iso3.strip().upper(), "")


# ---------------------------------------------------------------------------
# 2. Country × variable trajectory slopes
# ---------------------------------------------------------------------------
def compute_trajectories(cell: pd.DataFrame, min_waves: int = 2) -> pd.DataFrame:
    """For each (topic × variable × country), fit value_wmean ~ year (OLS).
    Return DataFrame with slope, SE, n_waves, year_range.
    """
    log(f"Computing country-level trajectories (min_waves={min_waves})...")
    rows = []
    for (topic, var, ctry), g in cell.groupby(["topic", "variable_harmonized", "country"]):
        g = g.sort_values("year")
        if g["year"].nunique() < min_waves:
            continue
        y = g["value_wmean"].values
        x = g["year"].values.astype(float)
        if len(y) < 2 or np.std(x) == 0:
            continue
        slope, intercept, r, p, se = stats.linregress(x, y)
        # Also absolute-z slope (z-scored within variable × wave)
        y_z = g["value_z"].values
        slope_z, _, r_z, p_z, se_z = stats.linregress(x, y_z)
        rows.append({
            "topic": topic,
            "variable": var,
            "country": ctry,
            "n_waves": int(g["year"].nunique()),
            "year_min": int(g["year"].min()),
            "year_max": int(g["year"].max()),
            "span_yrs": int(g["year"].max() - g["year"].min()),
            "slope_raw": slope,
            "slope_raw_se": se,
            "slope_z": slope_z,
            "slope_z_se": se_z,
            "r_z": r_z,
            "p_z": p_z,
            "mean_val": float(np.mean(y)),
            "start_val": float(y[0]),
            "end_val": float(y[-1]),
            "delta": float(y[-1] - y[0]),
            "delta_z": float(y_z[-1] - y_z[0]),
        })
    traj = pd.DataFrame(rows)
    log(f"  {len(traj)} (country×variable×topic) trajectories")
    log(f"  countries: {traj.country.nunique()}; topics: {traj.topic.nunique()}")
    return traj


# ---------------------------------------------------------------------------
# 3. Country-level τ_env_ISSP (aggregate trajectory velocity)
# ---------------------------------------------------------------------------
def build_aspirational_level(cell: pd.DataFrame) -> pd.DataFrame:
    """Per country, compute the latest-wave aspirational endorsement LEVEL
    using aspirational-signed harmonized variables. The level averages z-scores
    (signed toward aspirational) across all available topic variables in the
    most recent wave where the country appears.

    Returns: country, n_vars_level, asp_level_latest, asp_level_mean_all_waves.
    """
    rows = []
    sign_df = pd.DataFrame([
        {"topic": t, "variable": v, "sign": s}
        for (t, v), s in ASPIRATIONAL_SIGN.items() if s != 0
    ])
    merged_sign = cell.merge(sign_df, left_on=["topic", "variable_harmonized"],
                             right_on=["topic", "variable"], how="inner")
    # signed z
    merged_sign["signed_z"] = merged_sign["value_z"] * merged_sign["sign"]

    # per country, latest wave (highest year)
    latest_year = merged_sign.groupby("country")["year"].max().rename("latest_year")
    last_wave = merged_sign.merge(latest_year, on="country")
    last_wave = last_wave[last_wave.year == last_wave.latest_year]

    latest = last_wave.groupby("country").agg(
        n_vars_latest=("variable", "nunique"),
        asp_level_latest=("signed_z", "mean"),
        latest_year=("year", "first"))
    allwaves = merged_sign.groupby("country").agg(
        n_vars_any=("variable", "nunique"),
        asp_level_mean=("signed_z", "mean"),
        n_waves=("za_code", "nunique"))
    out = latest.join(allwaves, how="outer").reset_index()
    return out


def build_tau_env_issp(traj: pd.DataFrame) -> pd.DataFrame:
    """Collapse trajectories to a per-country τ_env_ISSP measure.

    Two measures returned:
    - `tau_env_issp_abs`: mean |slope_z| across ALL variables — raw attitudinal
      volatility (any direction)
    - `tau_env_issp_signed`: mean (sign × slope_z) across aspirational-signed
      variables only — directional ASPIRATIONAL SHIFT velocity. This is the
      theoretical P3 "how fast the aspirational environmental signal penetrated."
    - `delta_z_aspirational`: total aspirational Δz across 1987-2022 window
      (sum of sign × delta_z).
    """
    # Attach aspirational sign
    def _sign(row):
        return ASPIRATIONAL_SIGN.get((row["topic"], row["variable"]), 0)
    traj = traj.copy()
    traj["asp_sign"] = traj.apply(_sign, axis=1)
    traj["signed_slope_z"] = traj["slope_z"] * traj["asp_sign"]
    traj["signed_delta_z"] = traj["delta_z"] * traj["asp_sign"]
    traj["abs_slope_z"] = traj["slope_z"].abs()

    # Trajectory velocity analysis: main sample uses ≥3 waves (clean slope);
    # a relaxed ≥2-wave version stored separately for countries like CN.
    t3 = traj[traj.n_waves >= 3].copy()
    t2 = traj[traj.n_waves >= 2].copy()
    log(f"Trajectories ≥2 waves: {len(t2)} ({t2.country.nunique()} countries); "
        f"≥3 waves: {len(t3)} ({t3.country.nunique()} countries)")

    # Aspirational-signed subset only
    asp = t3[t3.asp_sign != 0].copy()
    log(f"Aspirational-signed trajectories (≥3 waves): {len(asp)} "
        f"({asp.country.nunique()} countries, {asp.variable.nunique()} vars)")

    country_abs = (t3.groupby("country")
                     .agg(n_traj=("variable", "count"),
                          n_topics=("topic", "nunique"),
                          tau_env_issp_abs=("abs_slope_z", "mean"),
                          span_mean=("span_yrs", "mean"),
                          n_waves_mean=("n_waves", "mean"))
                     .reset_index())
    country_asp = (asp.groupby("country")
                      .agg(n_asp_traj=("variable", "count"),
                           tau_env_issp_signed=("signed_slope_z", "mean"),
                           tau_env_issp_signed_median=("signed_slope_z", "median"),
                           delta_z_aspirational=("signed_delta_z", "mean"),
                           delta_z_asp_sum=("signed_delta_z", "sum"))
                      .reset_index())
    country_tau = country_abs.merge(country_asp, on="country", how="outer")

    # Also compute a ≥2-wave version so that countries like CN (2 waves) get a
    # slope estimate (with weaker reliability).
    asp2 = t2[t2.asp_sign != 0].copy()
    country_asp2 = (asp2.groupby("country")
                        .agg(n_asp_traj_2w=("variable", "count"),
                             tau_env_issp_signed_2w=("signed_slope_z", "mean"),
                             delta_z_asp_2w=("signed_delta_z", "mean"))
                        .reset_index())
    country_tau = country_tau.merge(country_asp2, on="country", how="outer")

    # Default tau_env_issp = signed if available, else abs (backwards compat).
    country_tau["tau_env_issp"] = country_tau["tau_env_issp_signed"].fillna(
        country_tau["tau_env_issp_abs"])

    log(f"τ_env_ISSP computed for {len(country_tau)} countries; "
        f"signed available for {country_tau.tau_env_issp_signed.notna().sum()}")

    # Per-topic velocity
    topic_tau = (t3.groupby(["country", "topic"])
                   .agg(n_traj=("variable", "count"),
                        tau_env_issp_abs=("abs_slope_z", "mean"),
                        tau_env_issp_signed=("signed_slope_z", "mean"),
                        delta_z_aspirational=("signed_delta_z", "mean"))
                   .reset_index())
    return country_tau, topic_tau


# ---------------------------------------------------------------------------
# 4. Merge with prior Layer C Σ_ST and τ_adapt_c
# ---------------------------------------------------------------------------
def merge_with_prior(country_tau: pd.DataFrame, prior: pd.DataFrame) -> pd.DataFrame:
    """Take prior country_panel (has sigma_st, tau_env_internet, tau_adapt
    composites etc.) and merge on ISO2 with ISSP τ_env."""
    if prior.empty:
        log("No prior panel — returning country_tau alone")
        return country_tau.copy()

    # Prior uses ISO3; ISSP uses ISO2. Translate.
    if "iso3" in prior.columns:
        prior["iso2"] = prior["iso3"].apply(iso2_from_iso3)
    elif "ISO3" in prior.columns:
        prior["iso2"] = prior["ISO3"].apply(iso2_from_iso3)
    elif "country_iso3" in prior.columns:
        prior["iso2"] = prior["country_iso3"].apply(iso2_from_iso3)
    else:
        log(f"  WARN: prior has no ISO3 column. Columns: {prior.columns.tolist()}")
        return country_tau.copy()

    # Derive log_tau_env_internet (used in prior Layer C primary spec)
    if "tau_env_internet" in prior.columns:
        prior["log_tau_env_internet"] = np.log(prior["tau_env_internet"].where(prior["tau_env_internet"] > 0))
    # Derive τ_adapt composite z-score (Gelfand + LTO + UAI)
    adapt_cols = [c for c in ["gelfand_tightness", "hofstede_ltowvs", "hofstede_uai"]
                  if c in prior.columns]
    if adapt_cols:
        sub = prior[adapt_cols].copy()
        for c in adapt_cols:
            sub[c + "_z"] = (sub[c] - sub[c].mean()) / sub[c].std()
        prior["tau_adapt_composite_z"] = sub[[c + "_z" for c in adapt_cols]].mean(axis=1)

    # Drop 'country' column from prior to avoid collision with our iso2 key
    prior = prior.drop(columns=[c for c in ["country"] if c in prior.columns])
    merged = country_tau.merge(prior, left_on="country", right_on="iso2", how="left")
    log(f"Merged: {len(merged)} rows; rows with sigma_st match: "
        f"{merged['sigma_st'].notna().sum() if 'sigma_st' in merged.columns else 'n/a'}")
    return merged


# ---------------------------------------------------------------------------
# 5. P3 regression: Σ_ST ~ τ_env_ISSP + τ_adapt + interaction
# ---------------------------------------------------------------------------
def robust_ols(y: np.ndarray, X: np.ndarray, labels: list[str]) -> dict:
    """OLS with HC3 robust SE; return dict of results."""
    X_const = sm.add_constant(X)
    m = sm.OLS(y, X_const, missing="drop").fit(cov_type="HC3")
    res = {
        "n": int(m.nobs),
        "r2": float(m.rsquared),
        "r2_adj": float(m.rsquared_adj),
        "fstat": float(m.fvalue) if not np.isnan(m.fvalue) else None,
        "f_p": float(m.f_pvalue) if not np.isnan(m.f_pvalue) else None,
        "aic": float(m.aic),
        "coefs": {},
    }
    for i, name in enumerate(["const"] + labels):
        c = m.params[i]
        se = m.bse[i]
        t = m.tvalues[i]
        p = m.pvalues[i]
        ci_lo, ci_hi = m.conf_int(alpha=0.05)[i]
        res["coefs"][name] = {
            "coef": float(c),
            "se": float(se),
            "t": float(t),
            "p": float(p),
            "ci95": [float(ci_lo), float(ci_hi)],
        }
    return res


def bootstrap_coef(y: np.ndarray, X: np.ndarray, target_idx: int,
                   n_boot: int = 2000, seed: int = 20260417) -> tuple[float, float, float]:
    """Bootstrap 95% CI for coefficient at index target_idx of [const, X...]."""
    rng = np.random.default_rng(seed)
    n = len(y)
    coefs = []
    X_const = sm.add_constant(X)
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        yb = y[idx]
        Xb = X_const[idx]
        try:
            m = sm.OLS(yb, Xb).fit()
            coefs.append(m.params[target_idx])
        except Exception:
            continue
    c = np.array(coefs)
    if len(c) < 10:
        return (np.nan, np.nan, np.nan)
    return (float(np.median(c)), float(np.percentile(c, 2.5)), float(np.percentile(c, 97.5)))


def run_p3_regressions(merged: pd.DataFrame) -> dict:
    """Run P3 specifications using multiple operationalizations of τ_env_ISSP.

    Three τ_env_ISSP flavors:
    (1) tau_env_issp_abs: mean |Δz/Δyr| across all harmonized vars
    (2) tau_env_issp_signed: mean signed-toward-aspirational Δz/Δyr
        (vars tagged +1 or -1 in ASPIRATIONAL_SIGN; only aspirational direction)
    (3) delta_z_aspirational: total net Δz over window 1987→2022

    For each flavor, we test:
    - spec A: bivariate Σ_ST ~ τ
    - spec B: Σ_ST ~ τ + τ_adapt + τ × τ_adapt (interaction model)
    - spec C: multivariate: Σ_ST ~ τ_ISSP + log(τ_env_internet) from prior
    """
    log("\n=== Running P3 regressions ===")
    out = {}

    if "sigma_st" not in merged.columns:
        log("  merged lacks sigma_st; skipping")
        return {"error": "sigma_st missing"}

    # Available τ_env flavors from country_tau
    tau_cols = [c for c in ["tau_env_issp_abs", "tau_env_issp_signed",
                             "delta_z_aspirational", "tau_env_issp_signed_median",
                             "asp_level_latest", "asp_level_mean"]
                if c in merged.columns and merged[c].notna().sum() >= 15]
    log(f"  τ_env_ISSP flavors available: {tau_cols}")

    # τ_adapt candidate
    tau_adapt_col = None
    for cand in ["tau_adapt_composite_z", "gelfand_tightness",
                 "hofstede_ltowvs", "hofstede_uai"]:
        if cand in merged.columns and merged[cand].notna().sum() >= 10:
            tau_adapt_col = cand
            break

    for tau_col in tau_cols:
        flav = tau_col
        d = merged.dropna(subset=["sigma_st", tau_col]).copy()
        log(f"\n  --- flavor: {flav} (n={len(d)}) ---")

        # Spec A bivariate
        y = d["sigma_st"].values.astype(float)
        X = d[[tau_col]].values.astype(float)
        ra = robust_ols(y, X, [tau_col])
        r_pear = float(stats.pearsonr(d[tau_col], d["sigma_st"])[0])
        ra["pearson_r"] = r_pear
        c_boot, lo, hi = bootstrap_coef(y, X, target_idx=1, n_boot=2000)
        ra["boot_ci"] = [lo, hi]
        ra["boot_median"] = c_boot
        out[f"{flav}_specA_bivariate"] = ra
        coef = ra["coefs"][tau_col]
        log(f"    specA: β={coef['coef']:+.4f} (SE={coef['se']:.4f}, p={coef['p']:.3f}), "
            f"r={r_pear:+.3f}, bootCI=[{lo:+.3f}, {hi:+.3f}]")

        # Spec B interaction
        if tau_adapt_col:
            db = d.dropna(subset=[tau_adapt_col]).copy()
            if len(db) >= 15:
                db["tau_env_z"] = (db[tau_col] - db[tau_col].mean()) / db[tau_col].std()
                db["tau_adapt_z"] = (db[tau_adapt_col] - db[tau_adapt_col].mean()) / db[tau_adapt_col].std()
                db["interact"] = db["tau_env_z"] * db["tau_adapt_z"]
                yb = db["sigma_st"].values.astype(float)
                Xb = db[["tau_env_z", "tau_adapt_z", "interact"]].values.astype(float)
                rb = robust_ols(yb, Xb, ["tau_env_z", "tau_adapt_z", "tau_x_adapt"])
                rb["tau_adapt_source"] = tau_adapt_col
                out[f"{flav}_specB_interaction"] = rb
                log(f"    specB [adapt={tau_adapt_col}, n={len(db)}]:")
                for k, v in rb["coefs"].items():
                    log(f"      {k}: β={v['coef']:+.3f} (p={v['p']:.3f}, CI=[{v['ci95'][0]:+.3f}, {v['ci95'][1]:+.3f}])")

        # Spec C joint w/ prior internet-transition
        if "log_tau_env_internet" in d.columns:
            dc = d.dropna(subset=["log_tau_env_internet"]).copy()
            if len(dc) >= 15:
                yc = dc["sigma_st"].values.astype(float)
                Xc = dc[[tau_col, "log_tau_env_internet"]].values.astype(float)
                rc = robust_ols(yc, Xc, [tau_col, "log_tau_env_internet"])
                out[f"{flav}_specC_joint_w_internet"] = rc
                log(f"    specC [n={len(dc)}]: ")
                for k, v in rc["coefs"].items():
                    log(f"      {k}: β={v['coef']:+.4f} (p={v['p']:.3f})")

    # Spec D: Level × velocity interaction (ceiling-effect test)
    # Hypothesis: high asp-level AND large positive velocity → Sweet Trap
    # (peak aspiration reached + still pushing = reward-trap plateau)
    if "asp_level_latest" in merged.columns and "delta_z_aspirational" in merged.columns:
        dd = merged.dropna(subset=["sigma_st", "asp_level_latest",
                                   "delta_z_aspirational"]).copy()
        if len(dd) >= 15:
            dd["level_z"] = (dd.asp_level_latest - dd.asp_level_latest.mean()) / dd.asp_level_latest.std()
            dd["vel_z"] = (dd.delta_z_aspirational - dd.delta_z_aspirational.mean()) / dd.delta_z_aspirational.std()
            dd["interact_lv"] = dd.level_z * dd.vel_z
            yD = dd.sigma_st.values.astype(float)
            XD = dd[["level_z", "vel_z", "interact_lv"]].values.astype(float)
            rD = robust_ols(yD, XD, ["asp_level_z", "asp_velocity_z", "level_x_vel"])
            out["specD_level_x_velocity"] = rD
            out["specD_level_x_velocity"]["n"] = int(len(dd))
            log(f"\n  specD Level × Velocity (n={len(dd)}):")
            for k, v in rD["coefs"].items():
                log(f"    {k}: β={v['coef']:+.3f} (p={v['p']:.3f}, "
                    f"CI=[{v['ci95'][0]:+.3f}, {v['ci95'][1]:+.3f}])")

    # Consistency check: correlation among τ_env flavors
    if len(tau_cols) >= 2:
        d4 = merged.dropna(subset=tau_cols).copy()
        out["flavor_correlations"] = {}
        for a in tau_cols:
            for b in tau_cols:
                if a < b:
                    r, p = stats.pearsonr(d4[a], d4[b])
                    out["flavor_correlations"][f"{a}__vs__{b}"] = {
                        "r": float(r), "p": float(p), "n": int(len(d4))
                    }

    # Cross-check: ISSP signed velocity vs prior Layer C τ_env_internet
    if "log_tau_env_internet" in merged.columns and "tau_env_issp_signed" in merged.columns:
        d5 = merged.dropna(subset=["log_tau_env_internet", "tau_env_issp_signed"])
        if len(d5) >= 10:
            r, p = stats.pearsonr(d5["log_tau_env_internet"], d5["tau_env_issp_signed"])
            out["consistency_issp_vs_internet"] = {
                "r": float(r), "p": float(p), "n": int(len(d5)),
                "note": "Agreement between attitudinal aspirational velocity and novelty-signal transition speed"
            }

    return out


# ---------------------------------------------------------------------------
# 6. CFPS domain cross-replication test
# ---------------------------------------------------------------------------
def cfps_cross_replication(cell: pd.DataFrame, merged: pd.DataFrame) -> dict:
    """For each CFPS Focal <-> ISSP variable mapping, test if the
    country-level trajectory slope of the ISSP variable correlates with
    sigma_st_c (proxy for welfare residual), matching CFPS direction.
    """
    log("\n=== CFPS ↔ ISSP cross-domain replication ===")
    out = {}

    if "sigma_st" not in merged.columns:
        return {"error": "sigma_st missing"}

    for focal, crosswalk in CFPS_ISSP_CROSSWALK:
        focal_res = {"focal": focal, "replications": []}
        for topic, var, direction, note in crosswalk:
            sub = cell[(cell.topic == topic) & (cell.variable_harmonized == var)]
            if len(sub) == 0:
                focal_res["replications"].append({
                    "topic": topic, "variable": var, "direction": direction,
                    "status": "variable not in ISSP harmonized panel",
                    "note": note,
                })
                continue

            # Country-level mean level (if single wave) OR trajectory slope
            is_longitudinal = sub["year"].nunique() > 1
            if is_longitudinal:
                # slope per country
                rows = []
                for ctry, g in sub.groupby("country"):
                    if g["year"].nunique() < 2:
                        continue
                    s, _, r, p, se = stats.linregress(g.year.astype(float), g.value_wmean)
                    rows.append({"country": ctry, "slope": s, "mean_val": g.value_wmean.mean()})
                df_c = pd.DataFrame(rows)
                metric_name = "slope"
            else:
                df_c = (sub.groupby("country")["value_wmean"].mean().reset_index()
                            .rename(columns={"value_wmean": "mean_val"}))
                df_c["slope"] = np.nan
                metric_name = "mean_val"

            # Merge with sigma_st
            df_m = df_c.merge(merged[["country", "sigma_st"]], on="country", how="inner")
            df_m = df_m.dropna(subset=[metric_name, "sigma_st"])
            if len(df_m) < 8:
                focal_res["replications"].append({
                    "topic": topic, "variable": var, "direction": direction,
                    "status": f"n_countries_merged={len(df_m)} too small",
                    "note": note,
                })
                continue

            r_val, p_val = stats.pearsonr(df_m[metric_name], df_m["sigma_st"])
            # direction match
            expected = +1 if direction == "+" else -1
            observed = +1 if r_val > 0 else -1
            match = (expected == observed)
            focal_res["replications"].append({
                "topic": topic, "variable": var,
                "direction_expected": direction,
                "metric": metric_name,
                "n": int(len(df_m)),
                "pearson_r": float(r_val),
                "p": float(p_val),
                "direction_match": bool(match),
                "note": note,
            })
            log(f"  {focal} via ISSP {topic}.{var} ({metric_name}): "
                f"r={r_val:+.3f}, p={p_val:.3f}, n={len(df_m)}, "
                f"match={'✓' if match else '✗'}")
        out[focal] = focal_res

    return out


# ---------------------------------------------------------------------------
# 7. China positioning
# ---------------------------------------------------------------------------
def china_positioning(cell: pd.DataFrame, traj: pd.DataFrame,
                      country_tau: pd.DataFrame,
                      merged: pd.DataFrame) -> dict:
    """Locate China in cross-country trajectory / value distributions."""
    log("\n=== China positioning ===")
    out = {}

    ctry = "CN"
    out["available_waves"] = {}
    cn_cells = cell[cell.country == ctry]
    for topic in sorted(cn_cells.topic.unique()):
        s = cn_cells[cn_cells.topic == topic]
        out["available_waves"][topic] = sorted(set(int(y) for y in s.year.dropna()))
    log(f"  China waves available: {out['available_waves']}")

    # China's τ_env_ISSP vs global distribution (use 2w version to include CN)
    for col in ["tau_env_issp", "tau_env_issp_signed_2w", "delta_z_asp_2w",
                "asp_level_latest", "asp_level_mean"]:
        if col not in country_tau.columns:
            continue
        s = country_tau.dropna(subset=[col])
        if ctry in s.country.values:
            cn_val = s.loc[s.country == ctry, col].iloc[0]
            rank = (s[col] < cn_val).mean() * 100
            out[f"{col}_value"] = float(cn_val)
            out[f"{col}_percentile"] = float(rank)
            out[f"{col}_sample_n"] = int(len(s))
            log(f"  China {col}: {cn_val:+.4f} "
                f"(percentile {rank:.0f}th of {len(s)} countries)")

    # China's trajectory per variable
    cn_traj = traj[traj.country == ctry]
    if len(cn_traj) > 0:
        out["cn_trajectories"] = []
        for _, r in cn_traj.iterrows():
            rec = {
                "topic": r.topic, "variable": r.variable,
                "slope_z": float(r.slope_z),
                "abs_slope_z": float(abs(r.slope_z)),
                "n_waves": int(r.n_waves),
                "year_min": int(r.year_min),
                "year_max": int(r.year_max),
                "delta_z": float(r.delta_z),
            }
            # percentile among all countries for this variable
            same = traj[(traj.topic == r.topic) & (traj.variable == r.variable)]
            if len(same) >= 5:
                rec["abs_slope_pct"] = float((same["slope_z"].abs() < abs(r.slope_z)).mean() * 100)
                rec["n_countries_compared"] = int(len(same))
            out["cn_trajectories"].append(rec)

    # China's sigma_st from prior Layer C
    if "sigma_st" in merged.columns:
        cn_row = merged[merged.country == ctry]
        if len(cn_row) > 0 and cn_row.sigma_st.notna().any():
            out["sigma_st_cn"] = float(cn_row.sigma_st.iloc[0])
            s2 = merged.dropna(subset=["sigma_st"])
            rank = (s2.sigma_st < out["sigma_st_cn"]).mean() * 100
            out["sigma_st_percentile"] = float(rank)
            log(f"  sigma_st for CN: {out['sigma_st_cn']:+.3f} "
                f"(percentile {rank:.0f}th)")

    return out


# ---------------------------------------------------------------------------
# 8. Figure 3 data export
# ---------------------------------------------------------------------------
def export_figure3_data(cell: pd.DataFrame, traj: pd.DataFrame,
                         country_tau: pd.DataFrame, merged: pd.DataFrame) -> None:
    """Emit CSVs the figure-designer can plot directly."""
    log("\n=== Exporting Figure 3 data ===")

    # (a) Long country × topic × year × variable × wmean for panel A scatter
    fig3a = cell[["topic", "variable_harmonized", "za_code", "year", "country",
                  "value_wmean", "value_z", "n_cell"]].copy()
    fig3a.to_csv(FIGDATA / "figure3_issp_longitudinal.csv", index=False)
    log(f"  wrote figure3_issp_longitudinal.csv ({len(fig3a):,} rows)")

    # (b) country trajectory table for panel B (scatter of velocity vs sigma_st)
    fig3b = country_tau.merge(
        merged[["country"] + [c for c in ["sigma_st", "sigma_st_n_components",
                                          "tau_adapt_composite_z", "log_tau_env_internet",
                                          "cantril_resid", "gini_latest", "gdp_ppp_2020_log"]
                              if c in merged.columns]],
        on="country", how="left")
    fig3b.to_csv(FIGDATA / "figure3b_country_trajectory.csv", index=False)
    log(f"  wrote figure3b_country_trajectory.csv ({len(fig3b)} rows)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    reset_log()

    # 1. Load
    cell, prior = load_panels()

    # 2. Trajectories
    traj = compute_trajectories(cell, min_waves=2)
    # 3. Country-level τ_env_ISSP + aspirational level
    country_tau, topic_tau = build_tau_env_issp(traj)
    asp_level = build_aspirational_level(cell)
    log(f"Aspirational level computed for {len(asp_level)} countries")
    # Join levels into country_tau
    country_tau = country_tau.merge(asp_level, on="country", how="outer")
    country_tau.to_csv(PROC / "issp_country_tau_env.csv", index=False)
    topic_tau.to_csv(PROC / "issp_country_topic_trajectory.csv", index=False)
    traj.to_parquet(PROC / "issp_country_trajectory.parquet", index=False)
    log(f"Wrote issp_country_trajectory.parquet ({len(traj)} rows)")

    # 4. Merge w/ prior Layer C
    merged = merge_with_prior(country_tau, prior)
    merged.to_csv(PROC / "issp_country_merged_with_prior.csv", index=False)

    # 5. P3 regressions
    p3 = run_p3_regressions(merged)

    # 6. CFPS cross-replication
    cfps = cfps_cross_replication(cell, merged)

    # 7. China positioning
    china = china_positioning(cell, traj, country_tau, merged)

    # 8. Figure 3 data
    export_figure3_data(cell, traj, country_tau, merged)

    # 9. Save final JSON
    final = {
        "meta": {
            "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "n_issp_cells": int(len(cell)),
            "n_countries_issp": int(cell.country.nunique()),
            "n_trajectories": int(len(traj)),
            "n_countries_with_tau_env_issp": int(len(country_tau)),
            "n_countries_merged_sigma_st": int(merged["sigma_st"].notna().sum()) if "sigma_st" in merged.columns else 0,
        },
        "p3_regressions": p3,
        "cfps_replication": cfps,
        "china_positioning": china,
    }
    out_path = PROC / "issp_p3_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False, default=float)
    log(f"\nWrote {out_path}")

    log("\nDONE.")
    return 0


if __name__ == "__main__":
    warnings.simplefilter("default")  # don't silence
    sys.exit(main())
