#!/usr/bin/env python3
"""
Layer C — P3 Novel-environment trigger (τ_env < τ_adapt) cross-national test
============================================================================

Theoretical target (formal model v2 §4 P3):
  Sweet Trap emergence requires τ_env < τ_adapt.
  Expected: Σ_ST negatively associated with log(τ_env / τ_adapt).
  (Smaller ratio = faster-than-adaptation environmental change = more trap.)

Operationalisation (country c):
  τ_env_c   — *inverse* speed of the novel-signal regime at country c.
              We use: time (in years) to traverse the modernization corridor
              measured by GDP per capita PPP moving from 10% to 80% of 2020
              median, OR internet penetration going from 5% to 60%.
              Faster transition = SMALLER τ_env.
  τ_adapt_c — proxied by cultural rigidity / time-lagged adaptation speed:
              Gelfand tightness (higher = slower adaptation) is canonical.
              Back-up: Hofstede long-term-orientation (ltowvs) inverse, or
              uncertainty-avoidance (uai) positive correlate.
  Σ_ST_c    — aggregate Sweet Trap severity. Three components:
              (a) Well-being residual: Cantril_ladder | (GDP, Gini, LE)
                  — negative residual means people are less happy than GDP
                  would predict.
              (b) Mental-health tail: suicide_rate (WHO) standardized.
              (c) Consumption/debt burden: household_consumption_per_capita
                  and domestic_credit_pct_gdp (the "luxury + housing" leg).
              Combined via z-score average (inverted so higher = more trap).

Falsification:
  We report partial correlation and OLS with 95% cluster-bootstrap CI at
  country level. Directional sign is the primary claim; magnitude second.
  If the coefficient on log(τ_env / τ_adapt) is null or positive in >2 of 3
  robustness specs, P3 at country level is NOT confirmed.

Outputs
-------
  03-analysis/models/layer_c_p3_results.json
  03-analysis/models/layer_c_p3_country_panel.csv
  04-figures/data/figure3_country_sigma_st.csv

Run
---
  /Users/andy/Desktop/Research/.corpus-index/venv312/bin/python \
      03-analysis/scripts/layer_c_p3_test.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

np.random.seed(20260417)

PROJECT_ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
PROC = PROJECT_ROOT / "02-data" / "processed"
MODELS = PROJECT_ROOT / "03-analysis" / "models"
MODELS.mkdir(parents=True, exist_ok=True)
FIG_DATA = PROJECT_ROOT / "04-figures" / "data"
FIG_DATA.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Load long panel + pivot to country x year
# ---------------------------------------------------------------------------
def load_panel() -> pd.DataFrame:
    long = pd.read_parquet(PROC / "layer_c_cross_national.parquet")
    # Time-varying part (year > 0) pivoted wide
    tv = long[long["year"] > 0].copy()
    wide = (tv.pivot_table(index=["iso3", "year"],
                           columns="variable", values="value",
                           aggfunc="first")
              .reset_index())
    # Time-invariant part (year == -1): merge back
    ti = long[long["year"] == -1][["iso3", "variable", "value"]]
    if not ti.empty:
        ti_wide = ti.pivot_table(index="iso3", columns="variable",
                                 values="value", aggfunc="first")
        wide = wide.merge(ti_wide, on="iso3", how="left")
    # Country name
    country_map = (long.groupby("iso3")["country"].first().to_dict())
    wide["country"] = wide["iso3"].map(country_map)
    return wide


# ---------------------------------------------------------------------------
# τ_env: time to traverse modernization corridor
# ---------------------------------------------------------------------------
def compute_tau_env(panel: pd.DataFrame) -> pd.DataFrame:
    """
    For each country:
      - internet_tau: years from internet_users_pct_pop first >= 5% to first >= 60%
      - gdp_tau:      years for gdp_per_capita_ppp_owid to double within 1990-2020
                      (shorter = faster regime change)
    Smaller tau_env = faster novel-signal transition.
    """
    rows = []
    for iso3, g in panel.groupby("iso3"):
        g = g.sort_values("year")
        # Internet penetration transition
        int_df = g[["year", "internet_users_pct_pop"]].dropna()
        tau_int = np.nan
        if len(int_df) >= 5:
            # first year >=5%
            above5 = int_df[int_df["internet_users_pct_pop"] >= 5]
            above60 = int_df[int_df["internet_users_pct_pop"] >= 60]
            if not above5.empty and not above60.empty:
                tau_int = (above60["year"].min() - above5["year"].min())
                if tau_int <= 0:
                    tau_int = np.nan

        # GDP PPP doubling time within 1990-2020
        gdp_df = g[(g["year"] >= 1990) & (g["year"] <= 2020)][
            ["year", "gdp_per_capita_ppp_owid"]].dropna()
        tau_gdp = np.nan
        if len(gdp_df) >= 10:
            lo = gdp_df.iloc[0]["gdp_per_capita_ppp_owid"]
            hi = gdp_df.iloc[-1]["gdp_per_capita_ppp_owid"]
            if lo > 0 and hi > lo:
                ratio = hi / lo
                years_span = gdp_df.iloc[-1]["year"] - gdp_df.iloc[0]["year"]
                # doubling time = years_span * log(2) / log(ratio)
                tau_gdp = years_span * np.log(2) / np.log(ratio)

        rows.append({"iso3": iso3, "tau_env_internet": tau_int,
                     "tau_env_gdp_doubling": tau_gdp})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# τ_adapt: cultural rigidity / adaptation resistance
# ---------------------------------------------------------------------------
def compute_tau_adapt(panel: pd.DataFrame) -> pd.DataFrame:
    """
    Pull per-country cultural indices. Higher Gelfand tightness =
    slower cultural adaptation. Higher Hofstede uncertainty-avoidance also
    tends to mean slower adaptation. We use Gelfand as primary (more direct
    construct) and Hofstede UAI as backup when Gelfand missing.
    """
    cols = ["iso3", "gelfand_tightness", "hofstede_uai",
            "hofstede_ltowvs", "hofstede_pdi"]
    have = [c for c in cols if c in panel.columns]
    invariant = (panel[have].dropna(subset=["iso3"])
                            .drop_duplicates("iso3"))
    return invariant


# ---------------------------------------------------------------------------
# Σ_ST: country-level Sweet Trap severity
# ---------------------------------------------------------------------------
def compute_sigma_st(panel: pd.DataFrame, focal_year_range=(2015, 2022)) -> pd.DataFrame:
    """
    Σ_ST components (averaged within focal year range per country):
      (a) happiness_residual: Cantril - E[Cantril | log(GDP_ppp), Gini, LE]
          Negative residual = unhappier than fundamentals predict.
      (b) suicide_z: age-std suicide rate, z-scored across countries
      (c) consumption_gap: log(HH_consumption_per_capita) detrended by log(GDP)
      (d) credit_burden: domestic credit pct GDP (z-scored)

    Σ_ST_c = mean of (-happiness_residual_z + suicide_z + credit_z + consumption_gap_z).
    Higher = more trap-like.
    """
    yr_lo, yr_hi = focal_year_range
    sub = panel[(panel["year"] >= yr_lo) & (panel["year"] <= yr_hi)].copy()

    # Country-year averaging
    def cmean(col: str) -> pd.Series:
        if col not in sub.columns:
            return pd.Series(dtype=float)
        return sub.groupby("iso3")[col].mean()

    cantril = cmean("cantril_ladder")
    gdp_ppp = cmean("gdp_per_capita_ppp_owid")
    gini = cmean("gini_index")
    le = cmean("life_expectancy_total")
    suicide = cmean("suicide_rate")
    hh_cons = cmean("household_consumption_per_capita")
    credit = cmean("domestic_credit_pct_gdp")

    df = pd.DataFrame({
        "iso3": cantril.index,
        "cantril": cantril.values,
    })
    df["log_gdp_ppp"] = np.log(gdp_ppp.reindex(df["iso3"]).values)
    df["gini"] = gini.reindex(df["iso3"]).values
    df["life_exp"] = le.reindex(df["iso3"]).values
    df["suicide"] = suicide.reindex(df["iso3"]).values
    df["log_hh_cons"] = np.log(hh_cons.reindex(df["iso3"]).values)
    df["credit_gdp"] = credit.reindex(df["iso3"]).values

    # (a) happiness residual: Cantril ~ log_gdp + gini + le
    reg = df.dropna(subset=["cantril", "log_gdp_ppp",
                            "gini", "life_exp"]).copy()
    X = sm.add_constant(reg[["log_gdp_ppp", "gini", "life_exp"]])
    if len(reg) > 20:
        m = sm.OLS(reg["cantril"], X).fit()
        reg["cantril_residual"] = reg["cantril"] - m.predict(X)
        df = df.merge(reg[["iso3", "cantril_residual"]], on="iso3", how="left")
        cant_reg_n = len(reg)
        cant_reg_r2 = m.rsquared
    else:
        df["cantril_residual"] = np.nan
        cant_reg_n = 0
        cant_reg_r2 = np.nan

    # (c) consumption gap: log_hh_cons ~ log_gdp → residual above predicted
    reg2 = df.dropna(subset=["log_hh_cons", "log_gdp_ppp"]).copy()
    if len(reg2) > 20:
        X2 = sm.add_constant(reg2[["log_gdp_ppp"]])
        m2 = sm.OLS(reg2["log_hh_cons"], X2).fit()
        reg2["consumption_gap"] = reg2["log_hh_cons"] - m2.predict(X2)
        df = df.merge(reg2[["iso3", "consumption_gap"]], on="iso3", how="left")
    else:
        df["consumption_gap"] = np.nan

    # z-score each component and combine
    def z(x: pd.Series) -> pd.Series:
        return (x - x.mean()) / x.std(ddof=1)

    df["neg_happiness_z"] = -z(df["cantril_residual"])  # low residual = high Σ_ST
    df["suicide_z"] = z(df["suicide"])
    df["credit_z"] = z(df["credit_gdp"])
    df["consumption_gap_z"] = z(df["consumption_gap"])

    df["sigma_st"] = df[["neg_happiness_z", "suicide_z",
                         "credit_z", "consumption_gap_z"]].mean(axis=1)
    # n_components counter: how many z's available per country
    df["n_components"] = df[["neg_happiness_z", "suicide_z",
                             "credit_z", "consumption_gap_z"]].notna().sum(axis=1)

    return df, {"cantril_residual_n": cant_reg_n, "cantril_residual_r2": cant_reg_r2}


# ---------------------------------------------------------------------------
# P3 regression
# ---------------------------------------------------------------------------
def run_p3_regression(merged: pd.DataFrame, tau_env_col: str,
                      tau_adapt_col: str, label: str) -> dict:
    """OLS: sigma_st = a + b * log(tau_env / tau_adapt) + controls + eps"""
    d = merged.dropna(subset=["sigma_st", tau_env_col, tau_adapt_col]).copy()
    if len(d) < 10:
        return {"label": label, "n": len(d), "note": "insufficient data"}
    d["ratio"] = d[tau_env_col] / d[tau_adapt_col]
    d = d[d["ratio"] > 0]
    d["log_ratio"] = np.log(d["ratio"])
    X = sm.add_constant(d[["log_ratio"]])
    m = sm.OLS(d["sigma_st"], X).fit(cov_type="HC3")
    pearson_r, pearson_p = stats.pearsonr(d["log_ratio"], d["sigma_st"])
    sp_r, sp_p = stats.spearmanr(d["log_ratio"], d["sigma_st"])
    # Bootstrap CI on beta
    rng = np.random.default_rng(20260417)
    boots = []
    for _ in range(2000):
        idx = rng.integers(0, len(d), len(d))
        db = d.iloc[idx]
        try:
            mb = sm.OLS(db["sigma_st"],
                        sm.add_constant(db[["log_ratio"]])).fit()
            boots.append(mb.params["log_ratio"])
        except Exception:
            pass
    beta_ci = (float(np.quantile(boots, 0.025)),
               float(np.quantile(boots, 0.975)))
    return {
        "label": label,
        "tau_env": tau_env_col,
        "tau_adapt": tau_adapt_col,
        "n_countries": int(len(d)),
        "beta_log_ratio": float(m.params["log_ratio"]),
        "se_HC3": float(m.bse["log_ratio"]),
        "p_two_sided": float(m.pvalues["log_ratio"]),
        "beta_ci95_boot": beta_ci,
        "r_squared": float(m.rsquared),
        "pearson_r": float(pearson_r),
        "pearson_p": float(pearson_p),
        "spearman_r": float(sp_r),
        "spearman_p": float(sp_p),
        "expected_sign": "negative (smaller ratio = more trap)",
        "n_bootstrap": len(boots),
    }


# ---------------------------------------------------------------------------
# Domain heterogeneity: does country-level Δ_ST for each human domain
# (luxury imports, housing debt, investment, short-video) echo CFPS findings?
# ---------------------------------------------------------------------------
def domain_heterogeneity(merged: pd.DataFrame) -> dict:
    """
    We don't have country-level Δ_ST for each of C5/C13/C8/C12 because we
    don't have per-country within-person panels for those. What we CAN test:
     (i) Do *levels* of domain proxies predict country Σ_ST?
        - Luxury proxy: consumption_gap_z (over-consumption vs GDP prediction)
        - Housing proxy: credit_gdp (private credit dominated by mortgages)
        - Investment proxy: domestic_credit_pct_gdp (financial depth)
        - Short-video proxy: internet_users_pct_pop most-recent
     (ii) Directional consistency with CFPS-China +Δ_ST findings:
        - CFPS4 (luxury +0.098, housing +0.068, investment +0.060,
          short-video +0.120) all positive.
        - Country-level analog: does each proxy correlate positively with
          Σ_ST in cross-section?
    """
    results = {}
    pairs = [
        ("luxury",      "consumption_gap_z"),
        ("housing",     "credit_z"),
        ("investment",  "credit_z"),  # same column; annotate
        ("shortvideo",  "internet_growth_2010_2020"),
    ]

    for name, col in pairs:
        if col not in merged.columns:
            results[name] = {"note": f"missing {col}"}
            continue
        d = merged.dropna(subset=["sigma_st", col])
        if len(d) < 20:
            results[name] = {"note": "n<20", "n": len(d)}
            continue
        r, p = stats.pearsonr(d[col], d["sigma_st"])
        # Partial r on log GDP
        if "log_gdp_ppp" in d.columns:
            dd = d.dropna(subset=["log_gdp_ppp"])
            if len(dd) > 20:
                try:
                    # partial r via residuals
                    X1 = sm.add_constant(dd[["log_gdp_ppp"]])
                    rx = sm.OLS(dd[col], X1).fit().resid
                    ry = sm.OLS(dd["sigma_st"], X1).fit().resid
                    pr, pp = stats.pearsonr(rx, ry)
                except Exception:
                    pr, pp = np.nan, np.nan
            else:
                pr, pp = np.nan, np.nan
        else:
            pr, pp = np.nan, np.nan
        results[name] = {
            "proxy_variable": col,
            "n_countries": int(len(d)),
            "pearson_r": float(r),
            "pearson_p": float(p),
            "partial_r_on_log_gdp": float(pr) if not np.isnan(pr) else None,
            "partial_p": float(pp) if not np.isnan(pp) else None,
            "cfps_china_delta_st": {"luxury": 0.098, "housing": 0.068,
                                    "investment": 0.060,
                                    "shortvideo": 0.120}[name],
            "direction_match_china": bool(r > 0),
        }
    return results


# ---------------------------------------------------------------------------
# China position in the cross-national distribution
# ---------------------------------------------------------------------------
def china_position(merged: pd.DataFrame) -> dict:
    """Where does China sit on (tau_env/tau_adapt, Sigma_ST)?"""
    chn = merged[merged["iso3"] == "CHN"]
    if chn.empty:
        return {"note": "China not in merged panel"}
    chn_row = chn.iloc[0].to_dict()
    # Rank China on each key axis
    cols = ["tau_env_internet", "tau_env_gdp_doubling",
            "gelfand_tightness", "sigma_st",
            "cantril_residual", "suicide", "credit_z",
            "consumption_gap_z"]
    rank = {}
    for c in cols:
        if c not in merged.columns:
            continue
        vals = merged[c].dropna()
        v = chn_row.get(c)
        if v is None or (isinstance(v, float) and np.isnan(v)):
            continue
        pct = (vals < v).mean()
        rank[c] = {"value": float(v),
                   "percentile": float(pct),
                   "n_countries_ranked": int(len(vals))}
    return {"china_row": {k: (v if not isinstance(v, float) or not np.isnan(v)
                              else None) for k, v in chn_row.items()},
            "ranks": rank}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("[P3] loading panel...")
    panel = load_panel()
    print(f"  panel shape = {panel.shape}  countries = {panel['iso3'].nunique()}"
          f"  years = {panel['year'].min()}..{panel['year'].max()}")

    print("[P3] computing tau_env...")
    tau_env = compute_tau_env(panel)

    print("[P3] computing tau_adapt...")
    tau_adapt = compute_tau_adapt(panel)

    print("[P3] computing Sigma_ST...")
    sigma, sigma_meta = compute_sigma_st(panel)

    merged = (sigma.merge(tau_env, on="iso3", how="left")
                   .merge(tau_adapt, on="iso3", how="left"))
    # Attach country name + most-recent internet use and 2010->2020 growth
    latest = (panel.dropna(subset=["internet_users_pct_pop"])
                    .sort_values("year")
                    .groupby("iso3").tail(1)[["iso3", "internet_users_pct_pop",
                                              "country"]]
                    .rename(columns={"internet_users_pct_pop": "internet_latest"}))
    merged = merged.merge(latest, on="iso3", how="left")

    # Internet growth rate 2010 -> 2020 (percentage-points per year)
    # as short-video-era novel-signal adoption speed
    pp2010 = (panel[(panel["year"].between(2008, 2012))]
                    .groupby("iso3")["internet_users_pct_pop"].mean())
    pp2020 = (panel[(panel["year"].between(2018, 2022))]
                    .groupby("iso3")["internet_users_pct_pop"].mean())
    growth = (pp2020 - pp2010).rename("internet_growth_2010_2020")
    merged = merged.merge(growth.reset_index(), on="iso3", how="left")

    # Composite tau_adapt (average z-score across tightness/LTO/UAI)
    for col in ("gelfand_tightness", "hofstede_ltowvs", "hofstede_uai"):
        if col in merged.columns:
            merged[f"{col}_z"] = ((merged[col] - merged[col].mean())
                                  / merged[col].std(ddof=1))
    merged["tau_adapt_composite_z"] = merged[
        ["gelfand_tightness_z", "hofstede_ltowvs_z", "hofstede_uai_z"]
    ].mean(axis=1)
    # Shift to strictly positive for log(ratio); documented as monotone affine
    shift = -merged["tau_adapt_composite_z"].min() + 0.5
    merged["tau_adapt_composite_positive"] = (
        merged["tau_adapt_composite_z"] + shift)

    # Preferred sample: countries with at least 3 of 4 Sigma_ST components
    merged_clean = merged[merged["n_components"] >= 3].copy()
    print(f"[P3] merged: {len(merged)} countries; "
          f"with n_components>=3: {len(merged_clean)}")

    print("[P3] running regressions (n_components>=3 sample)...")
    regs = []
    # Composite tau_adapt (largest sample)
    regs.append(run_p3_regression(merged_clean, "tau_env_internet",
                                  "tau_adapt_composite_positive",
                                  "PRIMARY_internet_composite"))
    regs.append(run_p3_regression(merged_clean, "tau_env_gdp_doubling",
                                  "tau_adapt_composite_positive",
                                  "gdp_doubling_composite"))
    # Primary: Gelfand tightness as tau_adapt
    regs.append(run_p3_regression(merged_clean, "tau_env_internet",
                                  "gelfand_tightness", "primary_internet_gelfand"))
    regs.append(run_p3_regression(merged_clean, "tau_env_gdp_doubling",
                                  "gelfand_tightness", "gdp_doubling_gelfand"))
    # Backup: Hofstede UAI
    regs.append(run_p3_regression(merged_clean, "tau_env_internet",
                                  "hofstede_uai", "internet_hofstede_uai"))
    regs.append(run_p3_regression(merged_clean, "tau_env_gdp_doubling",
                                  "hofstede_uai", "gdp_doubling_hofstede_uai"))
    # Hofstede long-term orientation
    regs.append(run_p3_regression(merged_clean, "tau_env_internet",
                                  "hofstede_ltowvs", "internet_hofstede_lto"))
    regs.append(run_p3_regression(merged_clean, "tau_env_gdp_doubling",
                                  "hofstede_ltowvs", "gdp_doubling_hofstede_lto"))
    # Sensitivity: full sample (n_components>=1)
    regs.append(run_p3_regression(merged, "tau_env_internet",
                                  "gelfand_tightness", "sensitivity_fullsample_gelfand"))
    regs.append(run_p3_regression(merged, "tau_env_internet",
                                  "hofstede_ltowvs", "sensitivity_fullsample_lto"))

    # Multivariate: sigma_st ~ log(tau_env) + tau_adapt (both variables on RHS)
    def run_multivar(df: pd.DataFrame, label: str) -> dict:
        d = df.dropna(subset=["sigma_st", "tau_env_internet",
                              "tau_adapt_composite_z"]).copy()
        d = d[d["tau_env_internet"] > 0]
        if len(d) < 15:
            return {"label": label, "note": "insufficient", "n": len(d)}
        d["log_tau_env"] = np.log(d["tau_env_internet"])
        X = sm.add_constant(d[["log_tau_env", "tau_adapt_composite_z"]])
        m = sm.OLS(d["sigma_st"], X).fit(cov_type="HC3")
        return {
            "label": label,
            "n_countries": int(len(d)),
            "beta_log_tau_env": float(m.params["log_tau_env"]),
            "se_log_tau_env_HC3": float(m.bse["log_tau_env"]),
            "p_log_tau_env": float(m.pvalues["log_tau_env"]),
            "beta_tau_adapt_z": float(m.params["tau_adapt_composite_z"]),
            "p_tau_adapt_z": float(m.pvalues["tau_adapt_composite_z"]),
            "r_squared": float(m.rsquared),
        }
    regs.append(run_multivar(merged_clean, "multivariate_internet_composite"))

    print("[P3] domain heterogeneity (using n_components>=3 sample)...")
    dom = domain_heterogeneity(merged_clean)

    print("[P3] China position (full sample; China has high coverage)...")
    chn = china_position(merged)

    results = {
        "design": {
            "tau_env_definition": ("internet_pct 5->60 years; gdp_ppp doubling "
                                   "time (years) within 1990-2020"),
            "tau_adapt_definition": ("Gelfand2011 tightness score (primary); "
                                     "Hofstede UAI, LTOWVS (backup)"),
            "sigma_st_components": ["neg_happiness_z (cantril residual | "
                                    "log GDP, gini, life-exp)",
                                    "suicide_z (WHO age-std)",
                                    "credit_z (domestic credit %GDP)",
                                    "consumption_gap_z (hh cons residual | "
                                    "log GDP)"],
            "focal_year_range": [2015, 2022],
            "sigma_st_model_n": sigma_meta["cantril_residual_n"],
            "sigma_st_model_r2": sigma_meta["cantril_residual_r2"],
        },
        "p3_regressions": regs,
        "domain_heterogeneity": dom,
        "china_position": chn,
    }

    out_json = MODELS / "layer_c_p3_results.json"
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False,
                                   default=lambda x: None
                                   if (isinstance(x, float) and np.isnan(x))
                                   else str(x)))
    print(f"[OUT] {out_json}")

    # Country panel (for audit)
    panel_out = MODELS / "layer_c_p3_country_panel.csv"
    cols_keep = ["iso3", "country", "sigma_st", "n_components",
                 "cantril", "cantril_residual", "suicide",
                 "credit_gdp", "credit_z", "consumption_gap",
                 "consumption_gap_z", "log_gdp_ppp", "gini",
                 "life_exp", "tau_env_internet", "tau_env_gdp_doubling",
                 "gelfand_tightness", "hofstede_uai", "hofstede_ltowvs",
                 "hofstede_pdi", "internet_latest"]
    keep = [c for c in cols_keep if c in merged.columns]
    merged[keep].sort_values("sigma_st", ascending=False).to_csv(
        panel_out, index=False, float_format="%.4f")
    print(f"[OUT] {panel_out}")

    # Figure 3 source data
    fig_cols = ["iso3", "country", "sigma_st", "tau_env_internet",
                "tau_env_gdp_doubling", "gelfand_tightness",
                "cantril", "cantril_residual", "suicide", "internet_latest"]
    fig_keep = [c for c in fig_cols if c in merged.columns]
    fig = merged[fig_keep].copy()
    fig["tau_ratio_internet_gelfand"] = (
        fig["tau_env_internet"] / fig["gelfand_tightness"])
    fig["tau_ratio_gdp_gelfand"] = (
        fig["tau_env_gdp_doubling"] / fig["gelfand_tightness"])
    fig["log_tau_ratio"] = np.log(fig["tau_ratio_internet_gelfand"])
    fig = fig.sort_values("sigma_st", ascending=False)
    fig_out = FIG_DATA / "figure3_country_sigma_st.csv"
    fig.to_csv(fig_out, index=False, float_format="%.4f")
    print(f"[OUT] {fig_out}")

    # Console summary
    print("\n=== P3 headline regressions ===")
    for r in regs:
        if "beta_log_ratio" in r:
            print(f"  {r['label']:35s} | n={r['n_countries']:3d} | "
                  f"β={r['beta_log_ratio']:+.3f} "
                  f"[{r['beta_ci95_boot'][0]:+.3f},"
                  f"{r['beta_ci95_boot'][1]:+.3f}] "
                  f"p={r['p_two_sided']:.3f} R²={r['r_squared']:.3f} "
                  f"Pearson r={r['pearson_r']:+.3f}")
        elif "beta_log_tau_env" in r:
            print(f"  {r['label']:35s} | n={r['n_countries']:3d} | "
                  f"β_log_tau_env={r['beta_log_tau_env']:+.3f} "
                  f"(se {r['se_log_tau_env_HC3']:.3f}, p {r['p_log_tau_env']:.3f}) "
                  f"| β_tau_adapt_z={r['beta_tau_adapt_z']:+.3f} "
                  f"(p {r['p_tau_adapt_z']:.3f}) R²={r['r_squared']:.3f}")
        else:
            print(f"  {r['label']:35s} | SKIPPED ({r.get('note','')})")

    print("\n=== Domain heterogeneity ===")
    for name, d in dom.items():
        if "pearson_r" in d:
            print(f"  {name:12s} | n={d['n_countries']:3d} r={d['pearson_r']:+.3f}"
                  f" p={d['pearson_p']:.3f} "
                  f"partial_r={d.get('partial_r_on_log_gdp')} "
                  f"match_China_direction={d['direction_match_china']}")
        else:
            print(f"  {name:12s} | {d}")

    print("\n=== China percentile ranks ===")
    for k, v in chn.get("ranks", {}).items():
        print(f"  {k:30s} value={v['value']:.3f} pct={v['percentile']:.2f}"
              f" (of {v['n_countries_ranked']} countries)")


if __name__ == "__main__":
    main()
