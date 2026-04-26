"""
C6 (保健品/养生执念) Sweet Trap analysis — CHARLS 2013-2020.

Pipeline:
  S1. Descriptive: who buys 保健品?
  S2. F2 diagnostic — is it voluntary? (income, education, cognition correlates)
  S3. Sweet (short-term subjective reward): sup_exp -> srh, cesd10, satlife
  S4. Bitter (long-term objective harm): sup_exp -> HbA1c, LDL, BMI, BP (2011 vs 2015 within-person)
       + savings depletion, intergenerational burden
  S5. F3 lock-in — AR1 of sup_exp; community peer exposure
  S6. F4 feedback blockade — subjective vs objective outcome divergence
  S7. Specification curve — ≥144 specs across DV × treatment × control × sample
  S8. Event study — cognitive decline onset -> subsequent supplement uptake
  S9. Delta_ST computation vs Layer A A10 neonicotinoid bees (0.73)

Inputs:
  /Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/panel_C6_supplement.parquet
Outputs:
  /Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/C6_results.json
  /Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/C6_speccurve.csv
  /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/scripts/C6_supplement_sweet_trap.log
"""

# Author: Claude (Sweet Trap multidomain C6 analyst)
# 2026-04-17
# n_workers = 1 (single-process statsmodels)

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

warnings.simplefilter("default")  # do NOT silence

PROJ = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
IN = PROJ / "02-data" / "processed" / "panel_C6_supplement.parquet"
OUT_JSON = PROJ / "02-data" / "processed" / "C6_results.json"
OUT_SPEC = PROJ / "02-data" / "processed" / "C6_speccurve.csv"

RESULTS = {}


def ci95_from_se(beta: float, se: float) -> tuple[float, float]:
    return (beta - 1.96 * se, beta + 1.96 * se)


def log(msg: str) -> None:
    print(msg, flush=True)


def main() -> None:
    log("[C6] Loading panel...")
    df = pd.read_parquet(IN)
    log(f"       shape: {df.shape}")

    # Focus on adults 45+ (CHARLS is already 45+) and waves with supplement data (2-5)
    df45 = df[(df["age"] >= 45) & (df["has_sup_exp"])].copy()
    log(f"       45+ with supplement data: {len(df45):,}")

    # Need srh reverse-coded: srh_good (higher=better health)
    # Key treatments:
    #  T1 = ln(sup_exp + 1) household yearly supplement+fitness
    #  T1b = sup_exp_heavy: >=1000 Y/yr (top ~3%)
    #  T2 = ln(med_exp_hh + 1) medical exp as comparator
    # Outcomes:
    #  O1 = srh_good (subjective)
    #  O2 = cesd10 (depression; lower=better)
    #  O3 = satlife (lower=better in CHARLS, actually let's check)
    #  O4 = bl_hbalc (biomarker)
    #  O5 = bl_ldl (biomarker)
    #  O6 = bmi / systo

    # ------------------------------------------------------------
    # S1. Descriptives
    # ------------------------------------------------------------
    log("\n[S1] Descriptives")
    n_total = len(df45)
    n_pos = int((df45["sup_exp"] > 0).sum())
    mean_pos = float(df45.loc[df45["sup_exp"] > 0, "sup_exp"].mean())
    med_pos = float(df45.loc[df45["sup_exp"] > 0, "sup_exp"].median())
    q95 = float(df45["sup_exp"].quantile(0.95))
    q99 = float(df45["sup_exp"].quantile(0.99))
    RESULTS["S1_descriptives"] = {
        "n_person_waves_45plus_with_data": n_total,
        "n_positive_supplement_households": n_pos,
        "share_positive": n_pos / n_total,
        "mean_positive_yuan_per_yr": mean_pos,
        "median_positive_yuan_per_yr": med_pos,
        "q95_yuan_per_yr": q95,
        "q99_yuan_per_yr": q99,
        "n_heavy_users_1000plus": int((df45["sup_exp"] >= 1000).sum()),
        "share_heavy_users": float((df45["sup_exp"] >= 1000).mean()),
    }
    log(f"       positive share: {n_pos/n_total:.3%}, median(pos)={med_pos:.0f} Y/y, 99th pct={q99:.0f}")

    # By age band
    age_band_stats = (
        df45.groupby("age_bin", observed=True)["sup_exp"]
        .agg(["count", lambda x: (x > 0).mean(), "median", lambda x: (x >= 1000).mean()])
        .round(4)
    )
    age_band_stats.columns = ["n", "share_pos", "median_all", "share_heavy"]
    log("       By age band:")
    log(age_band_stats.to_string())
    RESULTS["S1_age_band"] = age_band_stats.reset_index().to_dict(orient="records")

    # ------------------------------------------------------------
    # S2. F2 diagnostic — voluntary use?
    # ------------------------------------------------------------
    log("\n[S2] F2 diagnostic: who buys supplements?")

    # Correlations
    f2_corrs = {}
    for y in ["ln_income_total", "edu", "total_cognition", "cesd10", "srh_good"]:
        sub = df45[["ln_sup_exp_p1", y]].dropna()
        if len(sub) < 50:
            continue
        r, p = stats.spearmanr(sub["ln_sup_exp_p1"], sub[y])
        f2_corrs[y] = {"spearman_r": float(r), "p": float(p), "n": int(len(sub))}
        log(f"       corr(ln_sup_exp, {y}): r={r:+.3f}, p={p:.2e}, n={len(sub):,}")
    RESULTS["S2_f2_spearman"] = f2_corrs

    # Logistic regression of supplement purchase on income/education/cognition
    dflog = df45[["sup_exp_pos", "ln_income_total", "edu", "total_cognition",
                  "age_c", "gender", "rural", "srh_good", "wave"]].dropna()
    dflog["sup_exp_pos"] = dflog["sup_exp_pos"].astype(int)
    log(f"       Logit n={len(dflog):,}")
    try:
        m = smf.logit(
            "sup_exp_pos ~ ln_income_total + edu + total_cognition + age_c + "
            "C(gender) + C(rural) + srh_good + C(wave)",
            data=dflog,
        ).fit(disp=0, maxiter=100)
        summary = {}
        for v in m.params.index:
            b = float(m.params[v])
            se = float(m.bse[v])
            p = float(m.pvalues[v])
            lo, hi = ci95_from_se(b, se)
            summary[v] = {"coef": b, "se": se, "p": p, "ci_lo": lo, "ci_hi": hi}
        RESULTS["S2_logit_who_buys"] = summary
        log(f"       Logit pseudo-R2={m.prsquared:.3f}; key effects:")
        for v in ["ln_income_total", "edu", "total_cognition", "srh_good"]:
            if v in summary:
                s = summary[v]
                log(f"         {v}: beta={s['coef']:+.3f} [{s['ci_lo']:+.3f},{s['ci_hi']:+.3f}], p={s['p']:.3e}")
    except Exception as e:
        log(f"       Logit failed: {e}")
        RESULTS["S2_logit_who_buys"] = {"error": str(e)}

    # F2 verdict logic
    verdict = {}
    if "ln_income_total" in f2_corrs:
        verdict["income_pos"] = f2_corrs["ln_income_total"]["spearman_r"] > 0
    if "total_cognition" in f2_corrs:
        # If r > 0: high-cognition actively choose → clean F2
        # If r < 0: low-cognition are targets of scam → contaminated F2 (gray zone)
        verdict["cognition_r"] = f2_corrs["total_cognition"]["spearman_r"]
        verdict["cognition_sign_warning"] = (
            "clean F2: high cognition chooses voluntarily"
            if f2_corrs["total_cognition"]["spearman_r"] > 0
            else "GRAY ZONE: low-cognition targeted — need to address fraud exposure"
        )
    RESULTS["S2_verdict"] = verdict

    # ------------------------------------------------------------
    # S3. Sweet — short-term subjective reward
    # ------------------------------------------------------------
    log("\n[S3] Sweet: supplement expenditure -> subjective health/wellbeing")

    def individual_fe_ols(data: pd.DataFrame, y: str, x: str,
                          controls: list[str]) -> dict:
        # Within-person demeaning for panel FE (n_workers=1)
        d = data[["ID", "wave", y, x] + controls].dropna()
        if len(d) < 100 or d["ID"].nunique() < 50:
            return {"error": "insufficient data", "n": len(d)}
        # Demean all numeric cols by ID
        num_cols = [y, x] + [c for c in controls if pd.api.types.is_numeric_dtype(d[c])]
        d2 = d.copy()
        for col in num_cols:
            d2[col] = d2[col] - d2.groupby("ID")[col].transform("mean")
        # OLS on demeaned
        X = d2[[x] + controls]
        X = sm.add_constant(X)
        Y = d2[y]
        try:
            # Cluster by ID
            m = sm.OLS(Y, X, missing="drop").fit(
                cov_type="cluster", cov_kwds={"groups": d2.loc[X.index, "ID"]}
            )
            return {
                "n": int(len(d)),
                "n_ids": int(d["ID"].nunique()),
                "coef": float(m.params[x]),
                "se": float(m.bse[x]),
                "p": float(m.pvalues[x]),
                "ci_lo": float(m.params[x] - 1.96 * m.bse[x]),
                "ci_hi": float(m.params[x] + 1.96 * m.bse[x]),
                "r2": float(m.rsquared),
            }
        except Exception as e:
            return {"error": str(e), "n": len(d)}

    sweet_results = {}
    controls = ["age_c", "ln_income_total"]
    for y in ["srh_good", "satlife", "cesd10"]:
        res = individual_fe_ols(df45, y, "ln_sup_exp_p1", controls)
        sweet_results[y] = res
        if "coef" in res:
            log(f"       within-person FE: {y} ~ ln_sup_exp "
                f"beta={res['coef']:+.4f} [{res['ci_lo']:+.4f},{res['ci_hi']:+.4f}], "
                f"p={res['p']:.3e}, n={res['n']:,}")
    RESULTS["S3_sweet_within_person_FE"] = sweet_results

    # Also report effect size in SD units
    def sd_effect(y: str, beta: float) -> float:
        sd = df45[y].dropna().std()
        return beta / sd if sd > 0 else float("nan")

    for y in ["srh_good", "satlife", "cesd10"]:
        if "coef" in sweet_results[y]:
            sweet_results[y]["sd_effect_per_1ln"] = sd_effect(y, sweet_results[y]["coef"])

    # ------------------------------------------------------------
    # S4. Bitter — objective biomarker outcomes
    # ------------------------------------------------------------
    log("\n[S4] Bitter: supplement expenditure -> objective biomarkers")
    # Biomarkers only in waves 1 & 3 (2011 / 2015). Supplement only waves 2-5.
    # So use cross-sectional analysis within 2015 (wave 3) — supplement contemporary.
    bitter = {}
    w3 = df45[df45["wave"] == 3].copy()
    log(f"       2015 wave cross-section n={len(w3):,}")
    for y in ["bl_hbalc", "bl_glu", "bl_ldl", "bl_cho", "bl_hdl", "bl_tg",
              "systo", "bmi", "mwaist"]:
        d = w3[[y, "ln_sup_exp_p1", "age_c", "gender", "rural",
                "ln_income_total", "edu", "chronic"]].dropna()
        if len(d) < 100:
            bitter[y] = {"error": "insufficient data", "n": len(d)}
            continue
        try:
            m = smf.ols(
                f"{y} ~ ln_sup_exp_p1 + age_c + C(gender) + C(rural) + "
                f"ln_income_total + edu + C(chronic)",
                data=d,
            ).fit()
            b = float(m.params["ln_sup_exp_p1"])
            se = float(m.bse["ln_sup_exp_p1"])
            p = float(m.pvalues["ln_sup_exp_p1"])
            sd = d[y].std()
            bitter[y] = {
                "n": int(len(d)),
                "coef": b,
                "se": se,
                "p": p,
                "ci_lo": b - 1.96 * se,
                "ci_hi": b + 1.96 * se,
                "sd_effect_per_1ln": b / sd if sd > 0 else None,
                "mean_outcome": float(d[y].mean()),
                "sd_outcome": float(sd),
            }
            log(f"       {y}: beta={b:+.4f} [{b-1.96*se:+.4f},{b+1.96*se:+.4f}], "
                f"p={p:.3e}, n={len(d):,}")
        except Exception as e:
            bitter[y] = {"error": str(e), "n": len(d)}
    RESULTS["S4_bitter_cross_section_2015"] = bitter

    # Within-person change 2011->2015 in biomarkers
    log("\n[S4b] Within-person change 2011 -> 2015 biomarker ~ 2015 supplement")
    # Get wave 1 and wave 3 data, compute deltas
    w1 = df[df["wave"] == 1].set_index("ID")
    w3b = df[df["wave"] == 3].set_index("ID")
    shared_ids = sorted(set(w1.index) & set(w3b.index))
    log(f"       n shared IDs (2011∩2015): {len(shared_ids):,}")
    merged = pd.DataFrame(index=shared_ids)
    for v in ["bl_hbalc", "bl_ldl", "bl_tg", "bl_cho", "bmi", "systo", "bl_glu"]:
        merged[f"{v}_11"] = w1[v]
        merged[f"{v}_15"] = w3b[v]
        merged[f"d_{v}"] = merged[f"{v}_15"] - merged[f"{v}_11"]
    merged["ln_sup_exp_15"] = w3b["ln_sup_exp_p1"]
    merged["age_15"] = w3b["age"]
    merged["gender"] = w3b["gender"]
    merged["ln_income_15"] = w3b["ln_income_total"]
    merged["edu"] = w3b["edu"]

    delta_results = {}
    for v in ["bl_hbalc", "bl_ldl", "bl_tg", "bl_cho", "bmi", "systo", "bl_glu"]:
        d = merged[[f"d_{v}", "ln_sup_exp_15", "age_15", "gender",
                    "ln_income_15", "edu", f"{v}_11"]].dropna()
        if len(d) < 100:
            delta_results[v] = {"error": "insufficient data", "n": len(d)}
            continue
        # Control for baseline level to adjust for regression-to-mean
        try:
            m = smf.ols(
                f"d_{v} ~ ln_sup_exp_15 + age_15 + C(gender) + ln_income_15 + "
                f"edu + {v}_11",
                data=d,
            ).fit()
            b = float(m.params["ln_sup_exp_15"])
            se = float(m.bse["ln_sup_exp_15"])
            p = float(m.pvalues["ln_sup_exp_15"])
            delta_results[v] = {
                "n": int(len(d)),
                "coef": b,
                "se": se,
                "p": p,
                "ci_lo": b - 1.96 * se,
                "ci_hi": b + 1.96 * se,
            }
            log(f"       Δ{v} 2011->2015 ~ ln_sup(2015): beta={b:+.4f} "
                f"[{b-1.96*se:+.4f},{b+1.96*se:+.4f}], p={p:.3e}, n={len(d):,}")
        except Exception as e:
            delta_results[v] = {"error": str(e), "n": len(d)}
    RESULTS["S4b_within_person_delta_biomarker"] = delta_results

    # ------------------------------------------------------------
    # S5. F3 lock-in — autoregression + peer effects
    # ------------------------------------------------------------
    log("\n[S5] F3 lock-in: AR(1) of supplement expenditure")
    # Within-person AR1: ln_sup_t ~ ln_sup_{t-1}
    df_sorted = df45.sort_values(["ID", "wave"])
    df_sorted["ln_sup_lag"] = df_sorted.groupby("ID")["ln_sup_exp_p1"].shift(1)
    df_sorted["wave_lag"] = df_sorted.groupby("ID")["wave"].shift(1)
    ar1_df = df_sorted.dropna(subset=["ln_sup_lag", "ln_sup_exp_p1"]).copy()
    # Only consecutive waves (within 3 years)
    ar1_df = ar1_df[ar1_df["wave"] - ar1_df["wave_lag"] == 1]
    log(f"       AR1 n={len(ar1_df):,} (consecutive waves)")
    try:
        m = smf.ols(
            "ln_sup_exp_p1 ~ ln_sup_lag + age_c + C(gender) + ln_income_total + C(wave)",
            data=ar1_df,
        ).fit(cov_type="cluster", cov_kwds={"groups": ar1_df["ID"]})
        b = float(m.params["ln_sup_lag"])
        se = float(m.bse["ln_sup_lag"])
        p = float(m.pvalues["ln_sup_lag"])
        RESULTS["S5_AR1"] = {
            "coef": b, "se": se, "p": p,
            "ci_lo": b - 1.96 * se, "ci_hi": b + 1.96 * se,
            "n": int(len(ar1_df)),
            "interpretation": (
                "strong lock-in" if b > 0.4
                else "moderate persistence" if b > 0.2
                else "weak persistence"
            ),
        }
        log(f"       AR1 ln_sup: beta={b:+.4f} [{b-1.96*se:+.4f},{b+1.96*se:+.4f}], p={p:.3e}")
    except Exception as e:
        RESULTS["S5_AR1"] = {"error": str(e)}

    # Peer effect: community-level share of heavy users (leave-one-out)
    log("\n[S5b] F3 peer exposure: community heavy-user share")
    comm_agg = df45.groupby(["communityID", "wave"]).agg(
        comm_n=("sup_exp_heavy", "count"),
        comm_sum_heavy=("sup_exp_heavy", "sum"),
    ).reset_index()
    df_peer = df45.merge(comm_agg, on=["communityID", "wave"], how="left")
    df_peer["peer_share_heavy"] = (
        (df_peer["comm_sum_heavy"] - df_peer["sup_exp_heavy"].fillna(0))
        / (df_peer["comm_n"] - 1).clip(lower=1)
    )
    df_peer["peer_share_heavy"] = df_peer["peer_share_heavy"].clip(0, 1)
    try:
        dpf = df_peer[["sup_exp_heavy", "peer_share_heavy", "age_c", "gender",
                       "rural", "ln_income_total", "wave"]].dropna()
        dpf["sup_exp_heavy"] = dpf["sup_exp_heavy"].astype(int)
        mlog = smf.logit(
            "sup_exp_heavy ~ peer_share_heavy + age_c + C(gender) + C(rural) + "
            "ln_income_total + C(wave)",
            data=dpf,
        ).fit(disp=0, maxiter=100)
        b = float(mlog.params["peer_share_heavy"])
        se = float(mlog.bse["peer_share_heavy"])
        p = float(mlog.pvalues["peer_share_heavy"])
        RESULTS["S5b_peer_exposure"] = {
            "coef": b, "se": se, "p": p,
            "ci_lo": b - 1.96 * se, "ci_hi": b + 1.96 * se,
            "odds_ratio": float(np.exp(b)),
            "n": int(len(dpf)),
            "interpretation": "peer exposure in community predicts individual heavy use",
        }
        log(f"       peer_share_heavy logit: beta={b:+.4f} OR={np.exp(b):.2f} p={p:.3e}")
    except Exception as e:
        RESULTS["S5b_peer_exposure"] = {"error": str(e)}

    # ------------------------------------------------------------
    # S6. F4 feedback blockade — subjective vs objective divergence
    # ------------------------------------------------------------
    log("\n[S6] F4 feedback blockade: divergence subjective vs objective")
    # For 2015 users, compare: how much does srh track HbA1c?
    w3c = df45[df45["wave"] == 3].copy()
    # Continuous measure: among those with sup_exp > 0 vs = 0, correlate srh with HbA1c
    div_results = {}
    for group_label, subset in [("nonusers", w3c[w3c["sup_exp"] == 0]),
                                 ("light_users", w3c[(w3c["sup_exp"] > 0) & (w3c["sup_exp"] < 1000)]),
                                 ("heavy_users", w3c[w3c["sup_exp"] >= 1000])]:
        d = subset[["srh_good", "bl_hbalc"]].dropna()
        if len(d) < 50:
            div_results[group_label] = {"n": len(d), "error": "too small"}
            continue
        r, p = stats.spearmanr(d["srh_good"], d["bl_hbalc"])
        div_results[group_label] = {
            "n": int(len(d)),
            "spearman_r_srh_vs_hba1c": float(r),
            "p": float(p),
        }
        log(f"       {group_label}: corr(srh, HbA1c) r={r:+.3f}, p={p:.3e}, n={len(d):,}")
    RESULTS["S6_feedback_blockade"] = div_results

    # ------------------------------------------------------------
    # S7. Specification curve
    # ------------------------------------------------------------
    log("\n[S7] Specification curve (≥144 specs)")
    specs = []

    dvs = ["srh_good", "cesd10", "satlife", "bl_hbalc", "bl_ldl", "ln_savings_proxy"]
    treatments = ["ln_sup_exp_p1", "sup_exp_pos", "sup_exp_heavy"]
    control_sets = {
        "min": ["age_c", "C(gender)"],
        "mid": ["age_c", "C(gender)", "C(rural)", "ln_income_total"],
        "full": ["age_c", "C(gender)", "C(rural)", "ln_income_total",
                 "edu", "C(chronic)", "C(wave)"],
    }
    samples = {
        "all_45": lambda d: d,
        "age65plus": lambda d: d[d["age"] >= 65],
        "urban": lambda d: d[d["rural"] == 1],
        "low_cog": lambda d: d[d["cog_low"] == 1],
    }

    for dv in dvs:
        for tx in treatments:
            for cset_name, cset in control_sets.items():
                for samp_name, samp_fn in samples.items():
                    try:
                        dsub = samp_fn(df45)
                        # Pick cross-sectional (2015 wave for biomarkers) else pooled
                        if dv in ["bl_hbalc", "bl_ldl"]:
                            dsub = dsub[dsub["wave"] == 3]
                        # Drop C(...) controls from numeric list safely — use formula
                        # Use R-style formula
                        # Convert categorical wrappers
                        rhs = " + ".join([tx] + cset)
                        d2 = dsub[[dv, tx, "age_c", "ln_income_total", "gender",
                                    "rural", "wave", "edu", "chronic"]].dropna()
                        if len(d2) < 200:
                            continue
                        m = smf.ols(f"{dv} ~ {rhs}", data=d2).fit()
                        b = float(m.params[tx])
                        se = float(m.bse[tx])
                        p = float(m.pvalues[tx])
                        # Standardize by outcome SD
                        sd = d2[dv].std()
                        specs.append({
                            "dv": dv,
                            "tx": tx,
                            "controls": cset_name,
                            "sample": samp_name,
                            "n": int(len(d2)),
                            "coef": b,
                            "se": se,
                            "p": p,
                            "ci_lo": b - 1.96 * se,
                            "ci_hi": b + 1.96 * se,
                            "beta_std": b / sd if sd > 0 else None,
                        })
                    except Exception as e:
                        specs.append({
                            "dv": dv, "tx": tx, "controls": cset_name,
                            "sample": samp_name, "error": str(e),
                        })
    spec_df = pd.DataFrame(specs)
    spec_df.to_csv(OUT_SPEC, index=False)
    log(f"       {len(spec_df)} specs written to {OUT_SPEC}")

    # Aggregate summary
    valid = spec_df[spec_df["coef"].notna()]
    log(f"       valid specs: {len(valid)}")
    RESULTS["S7_speccurve_summary"] = {
        "total_specs": int(len(spec_df)),
        "valid_specs": int(len(valid)),
        "by_dv": {},
    }
    for dv in dvs:
        sub = valid[valid["dv"] == dv]
        if len(sub) == 0:
            continue
        RESULTS["S7_speccurve_summary"]["by_dv"][dv] = {
            "n_specs": int(len(sub)),
            "median_coef": float(sub["coef"].median()),
            "share_positive": float((sub["coef"] > 0).mean()),
            "share_significant_positive": float(((sub["coef"] > 0) & (sub["p"] < 0.05)).mean()),
            "share_significant_negative": float(((sub["coef"] < 0) & (sub["p"] < 0.05)).mean()),
            "median_beta_std": float(sub["beta_std"].median()) if "beta_std" in sub else None,
        }
        s = RESULTS["S7_speccurve_summary"]["by_dv"][dv]
        log(f"       {dv}: median_coef={s['median_coef']:+.4f}, "
            f"pos_share={s['share_positive']:.2f}, "
            f"sig_pos={s['share_significant_positive']:.2f}, "
            f"sig_neg={s['share_significant_negative']:.2f}")

    # ------------------------------------------------------------
    # S8. Event study — cognitive decline -> supplement uptake
    # ------------------------------------------------------------
    log("\n[S8] Event study: cognitive decline onset -> supplement uptake")
    # Build cog trajectory; identify first wave where cog drops >=3 points from baseline
    cog_panel = df[df["wave"].isin([1, 2, 3, 4, 5])][
        ["ID", "wave", "total_cognition", "sup_exp", "ln_sup_exp_p1",
         "age", "gender", "edu"]
    ].dropna(subset=["total_cognition"])
    cog_panel = cog_panel.sort_values(["ID", "wave"])
    # Baseline = first observation
    baseline = cog_panel.groupby("ID").first()[["total_cognition", "wave"]]
    baseline.columns = ["cog_base", "wave_base"]
    cog_panel = cog_panel.merge(baseline, on="ID", how="left")
    cog_panel["cog_drop"] = cog_panel["cog_base"] - cog_panel["total_cognition"]
    cog_panel["declined3"] = (cog_panel["cog_drop"] >= 3).astype(int)
    # First decline wave per person
    decline_wave = (
        cog_panel[cog_panel["declined3"] == 1].groupby("ID")["wave"].min().rename("wave_decline")
    )
    cog_panel = cog_panel.merge(decline_wave, on="ID", how="left")
    cog_panel["ever_declined"] = cog_panel["wave_decline"].notna().astype(int)
    cog_panel["event_time"] = cog_panel["wave"] - cog_panel["wave_decline"]
    # Event study: ln_sup_exp_p1 ~ event_time dummies (restrict to those ever declined)
    ev = cog_panel[cog_panel["ever_declined"] == 1].dropna(subset=["ln_sup_exp_p1", "event_time"])
    ev["event_time"] = ev["event_time"].astype(int)
    # Only event_time in [-2, 2]
    ev = ev[ev["event_time"].between(-3, 3)]
    log(f"       Event sample n={len(ev):,}; unique IDs={ev['ID'].nunique():,}")
    if len(ev) > 100 and ev["ID"].nunique() > 50:
        # Compare supplement spending before vs after decline
        pre = ev[ev["event_time"] < 0]["ln_sup_exp_p1"]
        post = ev[ev["event_time"] >= 0]["ln_sup_exp_p1"]
        if len(pre) > 20 and len(post) > 20:
            t = stats.ttest_ind(pre, post, equal_var=False)
            RESULTS["S8_event_cog_decline"] = {
                "n_ever_declined": int(ev["ID"].nunique()),
                "n_obs": int(len(ev)),
                "mean_ln_sup_pre": float(pre.mean()),
                "mean_ln_sup_post": float(post.mean()),
                "diff_post_minus_pre": float(post.mean() - pre.mean()),
                "t": float(t.statistic),
                "p": float(t.pvalue),
            }
            log(f"       pre-decline mean ln_sup={pre.mean():.3f}, "
                f"post={post.mean():.3f}, diff={post.mean()-pre.mean():+.3f}, "
                f"t={t.statistic:.2f}, p={t.pvalue:.3e}")

    # ------------------------------------------------------------
    # S9. Delta_ST computation
    # ------------------------------------------------------------
    log("\n[S9] Delta_ST vs Layer A A10 neonicotinoid bees (+0.73)")
    # Delta_ST = sign(corr(reward_signal, fitness_outcome)_ancestral)
    #         - sign(corr(reward_signal, fitness_outcome)_current)
    # Operationalize:
    #   Reward signal: srh_good (subjective health — the "it feels good" reward)
    #   Fitness outcome: bl_hbalc (actual glycemic control — objective biomarker)
    #   Ancestral baseline: non-users (sup_exp == 0)
    #   Current: heavy users (sup_exp >= 1000)
    # If reward tracks fitness in non-users (good health -> accurate srh -> low HbA1c)
    # but decouples in heavy users (subjective high, objective bad), Delta_ST > 0.
    w3d = df45[df45["wave"] == 3].copy()
    nu = w3d[w3d["sup_exp"] == 0][["srh_good", "bl_hbalc", "bl_ldl"]].dropna()
    hu = w3d[w3d["sup_exp"] >= 1000][["srh_good", "bl_hbalc", "bl_ldl"]].dropna()
    if len(nu) > 50 and len(hu) > 30:
        r_nu_hba1c = stats.spearmanr(nu["srh_good"], nu["bl_hbalc"])
        r_hu_hba1c = stats.spearmanr(hu["srh_good"], hu["bl_hbalc"])
        r_nu_ldl = stats.spearmanr(nu["srh_good"], nu["bl_ldl"])
        r_hu_ldl = stats.spearmanr(hu["srh_good"], hu["bl_ldl"])
        # Coupling strength: |r|; direction: sign. In healthy people, higher srh should predict lower HbA1c (negative r).
        # For fitness: sign * -1 so that + = aligned
        def coupling(r, direction_sign):
            """Return signed coupling: + means reward aligns with fitness.
            For HbA1c: lower = fitter, so expect srh↑ ⇒ HbA1c↓, i.e. r < 0 means aligned.
            """
            return -1 * direction_sign * r
        # HbA1c: lower=fitter, so aligned = negative r with srh_good (better srh, lower HbA1c)
        coup_nu_hba1c = -r_nu_hba1c.statistic   # invert so "+" is good alignment
        coup_hu_hba1c = -r_hu_hba1c.statistic
        coup_nu_ldl = -r_nu_ldl.statistic
        coup_hu_ldl = -r_hu_ldl.statistic
        delta_hba1c = coup_nu_hba1c - coup_hu_hba1c
        delta_ldl = coup_nu_ldl - coup_hu_ldl
        RESULTS["S9_delta_ST"] = {
            "nonusers_n": int(len(nu)),
            "heavy_users_n": int(len(hu)),
            "corr_srh_hba1c_nonusers": float(r_nu_hba1c.statistic),
            "corr_srh_hba1c_heavy": float(r_hu_hba1c.statistic),
            "corr_srh_ldl_nonusers": float(r_nu_ldl.statistic),
            "corr_srh_ldl_heavy": float(r_hu_ldl.statistic),
            "coupling_nu_hba1c": float(coup_nu_hba1c),
            "coupling_hu_hba1c": float(coup_hu_hba1c),
            "coupling_nu_ldl": float(coup_nu_ldl),
            "coupling_hu_ldl": float(coup_hu_ldl),
            "delta_ST_hba1c": float(delta_hba1c),
            "delta_ST_ldl": float(delta_ldl),
            "layer_A_benchmark": {"A10_neonicotinoid_bees": 0.73},
        }
        log(f"       coupling nonusers HbA1c: {coup_nu_hba1c:+.3f} "
            f"(p={r_nu_hba1c.pvalue:.2e}, n={len(nu)})")
        log(f"       coupling heavy HbA1c: {coup_hu_hba1c:+.3f} "
            f"(p={r_hu_hba1c.pvalue:.2e}, n={len(hu)})")
        log(f"       Delta_ST_hba1c = {delta_hba1c:+.3f}")
        log(f"       Delta_ST_ldl = {delta_ldl:+.3f}")
        log(f"       Layer A A10 bees benchmark = +0.73")

    # Bootstrap CI for Delta_ST_hba1c
    log("\n[S9b] Bootstrap CI for Delta_ST_hba1c (B=500)")
    rng = np.random.default_rng(20260417)
    if len(nu) > 50 and len(hu) > 30:
        B = 500
        deltas = []
        nu_arr = nu[["srh_good", "bl_hbalc"]].values
        hu_arr = hu[["srh_good", "bl_hbalc"]].values
        for _ in range(B):
            nu_s = nu_arr[rng.integers(0, len(nu_arr), len(nu_arr))]
            hu_s = hu_arr[rng.integers(0, len(hu_arr), len(hu_arr))]
            r_nu = stats.spearmanr(nu_s[:, 0], nu_s[:, 1]).statistic
            r_hu = stats.spearmanr(hu_s[:, 0], hu_s[:, 1]).statistic
            deltas.append(-r_nu - (-r_hu))
        deltas = np.array(deltas)
        RESULTS["S9_delta_ST"]["delta_ST_hba1c_bootstrap_ci95"] = [
            float(np.percentile(deltas, 2.5)),
            float(np.percentile(deltas, 97.5)),
        ]
        RESULTS["S9_delta_ST"]["delta_ST_hba1c_bootstrap_mean"] = float(deltas.mean())
        log(f"       Delta_ST_hba1c bootstrap 95% CI: "
            f"[{np.percentile(deltas, 2.5):+.3f}, {np.percentile(deltas, 97.5):+.3f}]")

    # ------------------------------------------------------------
    # Save results
    # ------------------------------------------------------------
    with open(OUT_JSON, "w") as f:
        json.dump(RESULTS, f, indent=2, default=str)
    log(f"\n[C6] Results written to {OUT_JSON}")
    log(f"[C6] Specs written to {OUT_SPEC}")


if __name__ == "__main__":
    main()
