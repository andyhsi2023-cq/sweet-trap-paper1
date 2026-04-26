"""
C12 Short-Video / Digital-Attention — Sweet Trap PDE
=====================================================

Position in Sweet-Trap research programme
  C12 is the human-level homologue of A6 Olds–Milner rat brain self-
  stimulation (Δ_ST=+0.97, strongest animal case). Together with C8
  investment FOMO (previous human variable-ratio reinforcement case),
  C12 locks the second human data-point under the "variable-ratio /
  algorithmic reward schedule" mechanism class.

Data ceiling (honest audit of CFPS 2010–2022 cleaned long panel)
  The CFPS public panel exposes only binary digital-engagement dummies:
    - internet       (2010, 2014–2022; 2012 missing)
    - mobile         (2016–2022)
    - computer       (2016–2022)
    - onlineshopoping (2014–2022)
  No hours-per-day / minutes-per-day / app-specific / Douyin-Kuaishou
  variables exist in the public release. We therefore operationalise
  C12 as the "digital-attention bundle" (binary + composite) and flag
  the ceiling on treatment granularity throughout.

F2 strict-version (Andy 2026-04-17) — hard pre-gate
  Under coerced-exposure hypotheses (H0_coerce):
    cor(internet, ln_income) ≤ 0 or cor(internet, eduy) ≤ 0
  Under aspirational selection (C12 Sweet Trap, H1):
    cor(internet, ln_income) > 0 AND cor(internet, eduy) > 0
  If H0_coerce cannot be rejected, demote C12 to "coerced-digital-
  divide" story (not Sweet Trap) analogous to C2 / D3 failures.

Pre-registered hypotheses
  H12.1 Sweet (qn12012):   β(life_sat ~ internet | person FE, year FE,
                            controls) > 0
  H12.2 Sweet (dw):        β(dw ~ digital_intensity | ...) > 0
  H12.3 Bitter (sleep):    β(qq4010 ~ heavy_digital_lag | ...) < 0
  H12.4 Bitter (health):   β(health ~ internet_lag | ...) < 0
  H12.5 λ (young):         β(qn12012 ~ internet×young_u30 | ...) > 0
  H12.6 Δ_ST (2010-2014 ancestral vs 2018-2022 current):
                            cor(internet, welfare) drops → Δ_ST > 0
  H12.7 Douyin-shock event study (2018 pre, 2020+ post): post-shock
         internet intensification correlates with Bitter DV worsening.

  α_Bonf (within C12, 4 primary DVs) = 0.0125

Outputs
  02-data/processed/C12_results.json
  02-data/processed/C12_speccurve.csv (≥ 144 specs)
  03-analysis/scripts/C12_shortvideo_sweet_trap.log
  00-design/pde/C12_shortvideo_findings.md (separate deliverable, written
                                             by hand after this script)

Compute discipline
  n_workers = 1; single-pass ops; SHA-256 verify; seed 20260417.
"""

import os
import json
import hashlib
import itertools
from datetime import datetime

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

# ------------------------------------------------------------
# Paths & constants
# ------------------------------------------------------------
BASE = "/Users/andy/Desktop/Research/sweet-trap-multidomain"
DATA = os.path.join(BASE, "02-data/processed/panel_C12_shortvideo.parquet")
EXPECTED_SHA = "8b628cd93f88e5e0b4f116f321d599c5ce22ec2046d507b8c7b04bb6712515c1"
OUT_JSON = os.path.join(BASE, "02-data/processed/C12_results.json")
OUT_SCA = os.path.join(BASE, "02-data/processed/C12_speccurve.csv")
LOG = os.path.join(BASE, "03-analysis/scripts/C12_shortvideo_sweet_trap.log")

SEED = 20260417
np.random.seed(SEED)
ALPHA_BONF = 0.0125


# ------------------------------------------------------------
# Logging
# ------------------------------------------------------------
def log(msg):
    ts = datetime.utcnow().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ------------------------------------------------------------
# Small utilities
# ------------------------------------------------------------
def pearson(x, y):
    """Return (r, p, n) with NaN-safe dropping."""
    d = pd.concat([pd.Series(x), pd.Series(y)], axis=1).dropna()
    if len(d) < 3:
        return (np.nan, np.nan, len(d))
    r, p = stats.pearsonr(d.iloc[:, 0], d.iloc[:, 1])
    return (r, p, len(d))


def within_demean(df, varlist, group):
    """Remove group means (for 2-way FE via Frisch-Waugh style)."""
    out = df.copy()
    for v in varlist:
        if v in out.columns:
            gmean = out.groupby(group)[v].transform("mean")
            out[v + "_w"] = out[v] - gmean
    return out


def twoway_fe_ols(df, y, treat, controls, cluster, weights=None):
    """Two-way FE via absorbing via dummy-var or within transform.
    Using statsmodels OLS with cluster SE (no FE library dep).
    We double-demean: subtract person mean and year mean (approx for
    unbalanced; use iterative demean)."""
    d = df.dropna(subset=[y, treat, "pid", "year"] + controls).copy()
    if len(d) < 50:
        return None

    for v in [y, treat] + controls:
        # iterative double demean (Gauss-Seidel on 2-way FE)
        for _ in range(8):
            d[v] = d[v] - d.groupby("pid")[v].transform("mean")
            d[v] = d[v] - d.groupby("year")[v].transform("mean")

    X = sm.add_constant(d[[treat] + controls])
    y_vec = d[y]
    try:
        if cluster is not None:
            model = sm.OLS(y_vec, X).fit(
                cov_type="cluster", cov_kwds={"groups": d[cluster]}
            )
        else:
            model = sm.OLS(y_vec, X).fit()
    except Exception as e:
        log(f"  regression failed: {e}")
        return None

    return {
        "n": len(d),
        "beta": float(model.params[treat]),
        "se": float(model.bse[treat]),
        "t": float(model.tvalues[treat]),
        "p_two": float(model.pvalues[treat]),
        "ci_low": float(model.conf_int().loc[treat, 0]),
        "ci_high": float(model.conf_int().loc[treat, 1]),
        "r2": float(model.rsquared),
    }


def bootstrap_diff_cor(df_a, df_b, x, y, n_boot=500):
    """Bootstrap CI for cor_a - cor_b with independent resampling."""
    rng = np.random.default_rng(SEED)
    vals = []
    d_a = df_a[[x, y]].dropna()
    d_b = df_b[[x, y]].dropna()
    if len(d_a) < 30 or len(d_b) < 30:
        return None
    for _ in range(n_boot):
        ia = rng.integers(0, len(d_a), size=len(d_a))
        ib = rng.integers(0, len(d_b), size=len(d_b))
        ra = np.corrcoef(d_a.iloc[ia, 0], d_a.iloc[ia, 1])[0, 1]
        rb = np.corrcoef(d_b.iloc[ib, 0], d_b.iloc[ib, 1])[0, 1]
        vals.append(ra - rb)
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return {
        "diff": float(np.mean(vals)),
        "ci_low": float(lo),
        "ci_high": float(hi),
        "cor_a": float(np.corrcoef(d_a.iloc[:, 0], d_a.iloc[:, 1])[0, 1]),
        "cor_b": float(np.corrcoef(d_b.iloc[:, 0], d_b.iloc[:, 1])[0, 1]),
        "n_a": int(len(d_a)),
        "n_b": int(len(d_b)),
    }


# ============================================================
# MAIN
# ============================================================
def main():
    open(LOG, "w").close()
    log("=== C12_shortvideo_sweet_trap.py START ===")
    log(f"SEED={SEED}  α_Bonf={ALPHA_BONF}")

    # --------------------------------------------------------
    # Load & verify
    # --------------------------------------------------------
    actual_sha = sha256_file(DATA)
    log(f"Panel SHA-256: {actual_sha}")
    log(f"  Expected:      {EXPECTED_SHA}")
    assert actual_sha == EXPECTED_SHA, "Panel SHA mismatch — rebuild!"
    df = pd.read_parquet(DATA)
    log(f"  shape: {df.shape}, unique pid: {df['pid'].nunique()}, "
        f"waves: {sorted(df['year'].unique().tolist())}")

    # Summary of treatment coverage
    log("Treatment coverage:")
    for c in ["internet", "mobile", "computer", "onlineshopoping",
              "digital_intensity", "heavy_digital", "qq4010"]:
        if c in df.columns:
            log(f"  {c}: n={df[c].notna().sum()}, "
                f"mean={df[c].mean():.3f}, sd={df[c].std():.3f}")

    results = {
        "meta": {
            "generated_at": datetime.utcnow().isoformat(timespec="seconds"),
            "panel_sha": actual_sha,
            "n_rows": int(df.shape[0]),
            "n_cols": int(df.shape[1]),
            "n_unique_pid": int(df["pid"].nunique()),
            "waves": sorted(df["year"].unique().tolist()),
            "seed": SEED,
            "alpha_bonf": ALPHA_BONF,
        }
    }

    # --------------------------------------------------------
    # §1 F2 strict-version pre-gate
    # --------------------------------------------------------
    log("\n=== §1 F2 STRICT pre-gate ===")
    f2 = {}
    df_adult = df[df["age"] >= 15].copy()

    tests = [
        ("internet", "ln_income"),
        ("internet", "eduy"),
        ("internet", "urban"),
        ("digital_intensity", "ln_income"),
        ("digital_intensity", "eduy"),
        ("digital_intensity", "urban"),
        ("heavy_digital", "ln_income"),
        ("heavy_digital", "eduy"),
        ("onlineshopoping", "ln_income"),
        ("onlineshopoping", "eduy"),
    ]
    for x, y in tests:
        r, p, n = pearson(df_adult[x], df_adult[y])
        f2[f"cor({x},{y})"] = {"r": r, "p": p, "n": n}
        passed = (r > 0) and (p < 0.05)
        log(f"  cor({x},{y}) = {r:+.4f} [p={p:.2e}, n={n}]  "
            f"{'PASS' if passed else 'FAIL'}")

    # Income-tercile gradient
    df_14 = df_adult[(df_adult["year"] >= 2014)
                     & df_adult["internet"].notna()
                     & df_adult["fincome1"].notna()].copy()
    df_14["inc_terc"] = pd.qcut(df_14["fincome1"], 3, labels=["Q1", "Q2", "Q3"])
    terc_rate = df_14.groupby("inc_terc", observed=True)["internet"].mean().to_dict()
    log(f"  internet rate by income tercile: {terc_rate}")
    t3_t1 = terc_rate["Q3"] / terc_rate["Q1"] if terc_rate["Q1"] > 0 else np.nan
    log(f"  T3/T1 = {t3_t1:.2f}×  {'PASS' if t3_t1 > 2 else 'FAIL'}")
    f2["income_tercile_rate"] = {str(k): float(v) for k, v in terc_rate.items()}
    f2["T3_over_T1"] = float(t3_t1)

    # Edu bracket
    df_14["edu_br"] = pd.cut(df_14["eduy"], [-0.5, 6, 9, 12, 30],
                             labels=["<=6", "7-9", "10-12", "13+"])
    edu_rate = df_14.groupby("edu_br", observed=True)["internet"].mean().to_dict()
    log(f"  internet rate by edu bracket: {edu_rate}")
    f2["edu_bracket_rate"] = {str(k): float(v) for k, v in edu_rate.items()}

    # Aspirational vs escape: does LOW life_sat predict HIGHER use? (灰区 proxy)
    # If cor(internet, life_sat) is positive conditional on income → aspirational
    # If cor(internet, life_sat) is negative → escape (逃避型)
    d = df_adult.dropna(subset=["internet", "qn12012", "fincome1"]).copy()
    d["ln_income"] = np.log(d["fincome1"].clip(lower=1))
    # residualise qn12012 on ln_income
    X = sm.add_constant(d[["ln_income", "eduy", "urban", "age", "age2"]])
    try:
        mod = sm.OLS(d["qn12012"], X).fit()
        d["qn12012_resid"] = d["qn12012"] - mod.predict(X)
        r_asp, p_asp, n_asp = pearson(d["internet"], d["qn12012_resid"])
        log(f"  cor(internet, qn12012 | income,edu,urb,age) = {r_asp:+.4f} "
            f"[p={p_asp:.3e}, n={n_asp}]  "
            f"(positive => aspirational; negative => escape)")
        f2["aspirational_vs_escape"] = {"r_resid": r_asp, "p": p_asp, "n": n_asp}
    except Exception as e:
        log(f"  residualisation failed: {e}")

    results["f2_pregate"] = f2

    # F2 OVERALL VERDICT
    passes = sum(1 for k, v in f2.items()
                 if isinstance(v, dict) and v.get("r", 0) > 0 and v.get("p", 1) < 0.05)
    log(f"\n  F2 VERDICT: {passes}/10 canonical correlations positive & significant")
    results["f2_verdict"] = "PASS" if passes >= 8 else "MARGINAL" if passes >= 5 else "FAIL"

    # --------------------------------------------------------
    # §2 Primary regressions (Sweet side)
    # --------------------------------------------------------
    log("\n=== §2 Sweet side — within-person FE regressions ===")
    sweet = {}

    # Controls: age, age2, familysize, married, ln_income
    controls_full = ["age", "age2", "familysize", "married", "ln_income"]

    for spec_name, treat, dv in [
        ("H12.1 life_sat ~ internet", "internet", "qn12012"),
        ("H12.1b life_sat ~ digital_intensity", "digital_intensity", "qn12012"),
        ("H12.1c life_sat ~ heavy_digital", "heavy_digital", "qn12012"),
        ("H12.2 dw ~ internet", "internet", "dw"),
        ("H12.2b dw ~ digital_intensity", "digital_intensity", "dw"),
        ("H12.2c future_conf ~ internet", "internet", "qn12016"),
    ]:
        res = twoway_fe_ols(df, y=dv, treat=treat, controls=controls_full, cluster="pid")
        sweet[spec_name] = res
        if res is not None:
            log(f"  {spec_name}")
            log(f"    β={res['beta']:+.4f}  SE={res['se']:.4f}  "
                f"p={res['p_two']:.3e}  95%CI=[{res['ci_low']:+.4f},{res['ci_high']:+.4f}]  "
                f"N={res['n']}")

    results["sweet"] = sweet

    # --------------------------------------------------------
    # §3 Bitter side
    # --------------------------------------------------------
    log("\n=== §3 Bitter side — long-run costs ===")
    bitter = {}

    # §3.1 Sleep crowd-out (qq4010 hours/day, 2014+)
    for spec_name, treat, dv in [
        ("H12.3 sleep ~ internet_lag", "internet_lag", "qq4010"),
        ("H12.3b sleep ~ digital_intensity_lag", "digital_intensity_lag", "qq4010"),
        ("H12.3c sleep ~ heavy_digital_lag", "heavy_digital_lag", "qq4010"),
        ("H12.3d sleep ~ internet", "internet", "qq4010"),
        ("H12.4 health ~ internet_lag", "internet_lag", "health"),
        ("H12.4b health ~ heavy_digital_lag", "heavy_digital_lag", "health"),
        ("H12.4c qq201_smoke ~ internet_lag", "internet_lag", "qq201"),
        ("H12.4d ln_travel ~ internet", "internet", "ln_travel"),
        ("H12.4e ln_eec ~ internet", "internet", "ln_eec"),
    ]:
        res = twoway_fe_ols(df, y=dv, treat=treat, controls=controls_full, cluster="pid")
        bitter[spec_name] = res
        if res is not None:
            log(f"  {spec_name}")
            log(f"    β={res['beta']:+.4f}  SE={res['se']:.4f}  "
                f"p={res['p_two']:.3e}  95%CI=[{res['ci_low']:+.4f},{res['ci_high']:+.4f}]  "
                f"N={res['n']}")

    results["bitter"] = bitter

    # --------------------------------------------------------
    # §4 λ interaction (young cohort moderator)
    # --------------------------------------------------------
    log("\n=== §4 λ externalisation — young × treatment interaction ===")
    lam = {}
    d = df.copy()
    d["int_x_young"] = d["internet"] * d["young_u30"]
    d["digi_x_young"] = d["digital_intensity"] * d["young_u30"]

    for spec_name, treat, dv in [
        ("H12.5 life_sat ~ internet×young_u30", "int_x_young", "qn12012"),
        ("H12.5b dw ~ internet×young_u30", "int_x_young", "dw"),
        ("H12.5c sleep ~ internet×young_u30", "int_x_young", "qq4010"),
        ("H12.5d life_sat ~ digital×young_u30", "digi_x_young", "qn12012"),
    ]:
        ctrl = ["internet", "young_u30"] + controls_full if "int_x_" in treat else \
               ["digital_intensity", "young_u30"] + controls_full
        res = twoway_fe_ols(d, y=dv, treat=treat, controls=ctrl, cluster="pid")
        lam[spec_name] = res
        if res is not None:
            log(f"  {spec_name}")
            log(f"    β={res['beta']:+.4f}  SE={res['se']:.4f}  "
                f"p={res['p_two']:.3e}  N={res['n']}")

    results["lambda"] = lam

    # --------------------------------------------------------
    # §5 Δ_ST (time-split ancestral vs current)
    # --------------------------------------------------------
    log("\n=== §5 Δ_ST — ancestral-era vs current-era ===")
    delta_st = {}
    df_anc = df[df["year"].isin([2010, 2012, 2014])]
    df_cur = df[df["year"].isin([2018, 2020, 2022])]

    for x, y in [
        ("internet", "qn12012"),
        ("internet", "qn12016"),
        ("internet", "dw"),
        ("internet", "health"),
        ("internet", "qq4010"),       # sleep
        ("digital_intensity", "qn12012"),
        ("digital_intensity", "dw"),
        ("digital_intensity", "qq4010"),
    ]:
        res = bootstrap_diff_cor(df_anc, df_cur, x, y)
        if res is None:
            log(f"  Δ_ST({x}→{y}): insufficient data")
            continue
        # Δ_ST is ancestral cor minus current cor
        delta = res["cor_a"] - res["cor_b"]
        # ci needs re-computation in that direction
        rng = np.random.default_rng(SEED)
        vals = []
        d_a = df_anc[[x, y]].dropna()
        d_b = df_cur[[x, y]].dropna()
        for _ in range(500):
            ia = rng.integers(0, len(d_a), size=len(d_a))
            ib = rng.integers(0, len(d_b), size=len(d_b))
            ra = np.corrcoef(d_a.iloc[ia, 0], d_a.iloc[ia, 1])[0, 1]
            rb = np.corrcoef(d_b.iloc[ib, 0], d_b.iloc[ib, 1])[0, 1]
            vals.append(ra - rb)
        lo, hi = np.percentile(vals, [2.5, 97.5])
        delta_st[f"{x}→{y}"] = {
            "cor_ancestral": float(res["cor_a"]),
            "cor_current": float(res["cor_b"]),
            "delta_ST": float(delta),
            "ci_low": float(lo),
            "ci_high": float(hi),
            "n_a": int(len(d_a)),
            "n_b": int(len(d_b)),
        }
        log(f"  Δ_ST({x}→{y}) = {delta:+.4f}  "
            f"[CI {lo:+.4f},{hi:+.4f}]  "
            f"cor_anc={res['cor_a']:+.4f}  cor_cur={res['cor_b']:+.4f}  "
            f"(Na={len(d_a)}, Nb={len(d_b)})")

    results["delta_st"] = delta_st

    # --------------------------------------------------------
    # §6 Douyin-shock event study (2018 = pre; 2020+ = post)
    # --------------------------------------------------------
    log("\n=== §6 Douyin-shock event study ===")
    ev = {}
    # Pre-post within-person change in DVs split by internet intensity in 2018
    df_2018 = df[df["year"] == 2018][["pid", "internet"]].rename(
        columns={"internet": "internet_2018"}
    )
    df_es = df.merge(df_2018, on="pid", how="left")
    df_es = df_es[df_es["internet_2018"].notna()].copy()
    df_es["t_rel"] = df_es["year"] - 2018

    for dv in ["qn12012", "qn12016", "dw", "health", "qq4010", "qq201"]:
        # For each relative year, compute mean change relative to t=0 (2018)
        trajectory = {}
        for t in [-4, -2, 0, 2, 4]:
            sub = df_es[df_es["t_rel"] == t]
            if len(sub) == 0:
                continue
            by_group = sub.groupby("internet_2018")[dv].agg(["mean", "std", "count"])
            trajectory[int(t)] = {
                str(g): {
                    "mean": float(by_group.loc[g, "mean"]) if g in by_group.index else None,
                    "std": float(by_group.loc[g, "std"]) if g in by_group.index else None,
                    "n": int(by_group.loc[g, "count"]) if g in by_group.index else 0,
                }
                for g in by_group.index
            }
        ev[dv] = trajectory

    results["event_study"] = ev

    for dv, traj in ev.items():
        log(f"  {dv} trajectory (by 2018 internet status):")
        for t, groups in sorted(traj.items()):
            parts = [f"t={t}"]
            for g, vals in groups.items():
                if vals["mean"] is not None:
                    parts.append(f"internet_2018={g}:{vals['mean']:.3f}(n={vals['n']})")
            log(f"    " + " | ".join(parts))

    # Specifically: did post-2018 internet-users' sleep drop faster?
    for dv in ["qq4010", "qn12012", "health"]:
        if dv not in ev or 0 not in ev[dv] or 4 not in ev[dv]:
            continue
        if "1.0" in ev[dv][0] and "1.0" in ev[dv][4] and \
           "0.0" in ev[dv][0] and "0.0" in ev[dv][4]:
            d_user = (ev[dv][4]["1.0"]["mean"] - ev[dv][0]["1.0"]["mean"])
            d_nonuser = (ev[dv][4]["0.0"]["mean"] - ev[dv][0]["0.0"]["mean"])
            DiD = d_user - d_nonuser
            log(f"  [DiD-like] Δ{dv}(2022-2018) user - non_user = {DiD:+.4f}")

    # --------------------------------------------------------
    # §7 ρ lock-in: auto-correlation within person
    # --------------------------------------------------------
    log("\n=== §7 ρ lock-in — within-person autocorr ===")
    rho = {}
    for v in ["internet", "mobile", "computer", "onlineshopoping",
              "digital_intensity", "heavy_digital"]:
        if v not in df.columns or f"{v}_lag" not in df.columns:
            continue
        d = df.dropna(subset=[v, f"{v}_lag"])
        if len(d) < 100:
            continue
        r, p, n = pearson(d[v], d[f"{v}_lag"])
        rho[v] = {"auto_cor_within_person": float(r), "p": float(p), "n": int(n)}
        log(f"  {v}: auto-cor (t vs t-1) = {r:+.4f}  [p={p:.2e}, n={n}]")

    # Exit rate: % of internet==1 households that drop to internet==0 2 years later
    d = df[df["internet"].notna() & df["internet_lag"].notna()]
    exit_rate = (
        d[(d["internet_lag"] == 1) & (d["internet"] == 0)].shape[0]
        / max(d[d["internet_lag"] == 1].shape[0], 1)
    )
    rho["exit_rate_2yr"] = float(exit_rate)
    log(f"  Exit rate from internet (2-yr): {exit_rate:.3f}")
    results["rho"] = rho

    # --------------------------------------------------------
    # §8 Specification curve (≥ 144 specs)
    # --------------------------------------------------------
    log("\n=== §8 Specification curve analysis (SCA) ===")
    sca_rows = []

    DVs_sweet = ["qn12012", "qn12016", "dw"]
    DVs_bitter = ["qq4010", "health", "qq201"]
    TREATS = ["internet", "digital_intensity", "heavy_digital", "onlineshopoping"]
    SAMPLES = [
        ("all", lambda d: d[d["age"] >= 15]),
        ("young_u30", lambda d: d[(d["age"] >= 15) & (d["age"] < 30)]),
        ("mid_30_55", lambda d: d[(d["age"] >= 30) & (d["age"] < 55)]),
        ("old_55p", lambda d: d[d["age"] >= 55]),
    ]
    CTRL_SETS = [
        ("minimal", ["age", "age2"]),
        ("ses", ["age", "age2", "familysize", "married", "ln_income"]),
        ("ses+edu", ["age", "age2", "familysize", "married", "ln_income", "eduy"]),
    ]
    LAGS = [False, True]

    total = len(DVs_sweet + DVs_bitter) * len(TREATS) * len(SAMPLES) * len(CTRL_SETS) * len(LAGS)
    log(f"  projected specs: {total}")

    spec_id = 0
    for dv in DVs_sweet + DVs_bitter:
        branch = "sweet" if dv in DVs_sweet else "bitter"
        for treat in TREATS:
            for sample_name, sample_fn in SAMPLES:
                for ctrl_name, ctrl_cols in CTRL_SETS:
                    for lag in LAGS:
                        spec_id += 1
                        t_col = f"{treat}_lag" if lag else treat
                        if t_col not in df.columns:
                            continue
                        sub = sample_fn(df)
                        try:
                            res = twoway_fe_ols(sub, y=dv, treat=t_col,
                                                 controls=ctrl_cols, cluster="pid")
                        except Exception:
                            res = None
                        row = {
                            "spec_id": spec_id,
                            "branch": branch,
                            "dv": dv,
                            "treat": t_col,
                            "sample": sample_name,
                            "ctrl": ctrl_name,
                            "lag": int(lag),
                            "n": res["n"] if res else None,
                            "beta": res["beta"] if res else None,
                            "se": res["se"] if res else None,
                            "p_two": res["p_two"] if res else None,
                            "ci_low": res["ci_low"] if res else None,
                            "ci_high": res["ci_high"] if res else None,
                        }
                        sca_rows.append(row)

    sca_df = pd.DataFrame(sca_rows)
    sca_df.to_csv(OUT_SCA, index=False)
    log(f"  SCA rows saved: {len(sca_df)}  → {OUT_SCA}")

    # SCA summary
    for branch in ["sweet", "bitter"]:
        sub = sca_df[sca_df["branch"] == branch].dropna(subset=["beta"])
        if len(sub) == 0:
            continue
        med = sub["beta"].median()
        sign_pos = (sub["beta"] > 0).mean()
        sig05 = (sub["p_two"] < 0.05).mean()
        sig_bonf = (sub["p_two"] < ALPHA_BONF).mean()
        log(f"  [{branch}] n_specs={len(sub)}  median β={med:+.4f}  "
            f"sign+={sign_pos:.3f}  sig@0.05={sig05:.3f}  sig@bonf={sig_bonf:.3f}")
        results.setdefault("sca_summary", {})[branch] = {
            "n_specs": int(len(sub)),
            "median_beta": float(med),
            "frac_positive": float(sign_pos),
            "frac_sig_05": float(sig05),
            "frac_sig_bonf": float(sig_bonf),
        }

    # Per-DV breakdown
    by_dv = (
        sca_df.dropna(subset=["beta"])
        .groupby("dv")
        .agg(
            n=("beta", "size"),
            med_beta=("beta", "median"),
            frac_pos=("beta", lambda s: (s > 0).mean()),
            frac_sig05=("p_two", lambda s: (s < 0.05).mean()),
            frac_sig_bonf=("p_two", lambda s: (s < ALPHA_BONF).mean()),
        )
    )
    log(f"\n  SCA per-DV:")
    for dv, row in by_dv.iterrows():
        log(f"    {dv}: n={row['n']}  med β={row['med_beta']:+.4f}  "
            f"sign+={row['frac_pos']:.3f}  sig05={row['frac_sig05']:.3f}")

    results["sca_per_dv"] = by_dv.reset_index().to_dict("records")

    # --------------------------------------------------------
    # Save JSON
    # --------------------------------------------------------
    with open(OUT_JSON, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    log(f"\nResults JSON → {OUT_JSON}")
    log(f"SCA CSV → {OUT_SCA}")
    log("=== C12_shortvideo_sweet_trap.py END ===")


if __name__ == "__main__":
    main()
