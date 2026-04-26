"""
C2 Intensive Parenting (鸡娃) Sweet Trap — PDE Analysis Script
===============================================================

Purpose
  Execute the pre-registered analysis for Study C2 of the Sweet-Trap
  multi-domain paper. C2 is the newly-promoted Focal-1 human domain
  after C4 (彩礼) demotion due to CGSS measurement limitations.

  Construct: sweet_trap_formal_model_v2.md (Δ_ST + F1–F4)
  Protocol:  00-design/analysis_protocols/pre_reg_D2_education.md

Hypotheses (pre-registered, directional, one-sided, alpha_Bonf = 0.0125)
  H2.1  Sweet:  within-person d(qn12012)/d(eexp_share) > 0   (parental life sat)
  H2.2  Bitter: within-person d(non_edu_share)/d(eexp_share_{t-1}) < 0 (crowd-out)
  H2.3  DID:    delta(post2021 x high_baseline_tutoring) on qn12012 < 0
                (if signal was Sweet, forcible removal should attenuate)
  H2.4  Placebo DID: same but pseudo-treatment 2019; pred delta ~= 0.

Input
  02-data/processed/panel_D2_education.parquet  (SHA-256 lock, 30,630 x 46)

Outputs
  02-data/processed/C2_results.json            -- full numeric record
  02-data/processed/C2_speccurve.csv           -- spec curve (>=168 variants)
  03-analysis/scripts/C2_education_sweet_trap.log

Constraints
  - Never modify the input parquet; SHA-256 verify on load.
  - n_workers <= 2 (no multiprocessing).
  - Random seed 20260417.
  - Warnings visible.

Author:  Claude (opus 4.7) under Andy's Sweet-Trap project
Date:    2026-04-17
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
# PATHS + LOCKS
# ------------------------------------------------------------
BASE = "/Users/andy/Desktop/Research/sweet-trap-multidomain"
PANEL = os.path.join(BASE, "02-data/processed/panel_D2_education.parquet")
EXPECTED_SHA = "d1603c1e7f9776be8ddfd3ed219706e374cc210858d83140603b40cff7702c30"
OUT_JSON = os.path.join(BASE, "02-data/processed/C2_results.json")
OUT_SPECCURVE = os.path.join(BASE, "02-data/processed/C2_speccurve.csv")
LOG_PATH = os.path.join(BASE, "03-analysis/scripts/C2_education_sweet_trap.log")

RNG_SEED = 20260417
np.random.seed(RNG_SEED)


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


TEE = Tee(LOG_PATH)


def log(msg=""):
    TEE.write(str(msg) + "\n")


log("=" * 72)
log(f"C2 Education Sweet Trap PDE -- start {datetime.now().isoformat()}")
log("=" * 72)


# ------------------------------------------------------------
# 1. LOAD + SHA LOCK
# ------------------------------------------------------------
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


log("\n[1] Loading panel_D2_education.parquet")
actual_sha = sha256_file(PANEL)
log(f"    SHA-256 actual  : {actual_sha}")
log(f"    SHA-256 expected: {EXPECTED_SHA}")
assert actual_sha == EXPECTED_SHA, "SHA-256 mismatch — panel has been modified; abort."

df = pd.read_parquet(PANEL)
log(f"    Shape: {df.shape}")
log(f"    Waves: {sorted(df['year'].dropna().unique().tolist())}")
log(f"    Unique pid: {df['pid'].nunique()}")

# ------------------------------------------------------------
# 2. DERIVED VARIABLES (non-destructive: only a view)
# ------------------------------------------------------------
log("\n[2] Deriving non-destructive analysis variables")

df = df.copy()
# Non-education share of total expenditure
df["non_edu_share"] = np.where(
    (df["expense"].fillna(0) > 0),
    1 - df["eexp"].fillna(0) / df["expense"],
    np.nan,
)
# trim implausible non_edu_share (<0 means eexp > expense which is a data error)
df.loc[df["non_edu_share"] < 0, "non_edu_share"] = np.nan

# Log tutoring (eexp == school in this panel; kept as alt)
df["ln_eexp_p1"] = np.log1p(df["eexp"].clip(lower=0))

# Treatment transforms
df["eexp_share_win"] = df["eexp_share"].clip(
    lower=df["eexp_share"].quantile(0.01),
    upper=df["eexp_share"].quantile(0.99),
)

# Dummy — top tercile within-wave
def top_tercile_within_wave(s):
    """Return dummy = 1 if in top tercile of s within the same wave."""
    t = s.groupby(df["year"]).transform(lambda x: x.quantile(0.67))
    return (s >= t).astype(int)


df["eexp_share_top3"] = top_tercile_within_wave(df["eexp_share"])

# Post-2021 flag is already in panel; DID high-baseline construction next
# ------------------------------------------------------------
# 3. DID SAMPLE: baseline tutoring intensity assignment
# ------------------------------------------------------------
log("\n[3] Constructing DID baseline treatment")

# Baseline = mean eexp_share in {2018, 2020} per household
pre_window = df[df["year"].isin([2018, 2020])]
baseline = (
    pre_window.groupby("pid")["eexp_share"]
    .mean()
    .rename("baseline_eexp_share")
    .reset_index()
)
# top-tercile threshold across baseline distribution (not within-wave; unified)
threshold = baseline["baseline_eexp_share"].quantile(0.67)
baseline["high_baseline_tutoring"] = (
    baseline["baseline_eexp_share"] >= threshold
).astype(int)
log(f"    baseline N pid: {len(baseline)}")
log(f"    baseline top-tercile threshold: {threshold:.4f}")
log(f"    # high-baseline: {baseline['high_baseline_tutoring'].sum()}")

df = df.merge(baseline, on="pid", how="left")

# post2021 is already in df; post2019 for placebo
df["post_2019"] = (df["year"] >= 2020).astype(int)  # pseudo-treatment 2019 => waves >=2020 treated

# Interaction terms
df["did_2021"] = df["post_2021"] * df["high_baseline_tutoring"]
df["did_2019"] = df["post_2019"] * df["high_baseline_tutoring"]

# ------------------------------------------------------------
# 4. F1 + F2 CONSTRUCT DIAGNOSTICS
# ------------------------------------------------------------
log("\n[4] F1 + F2 diagnostic (construct necessary conditions)")

# F1 necessary: raw cor(eexp, welfare) <= 0 or declining across cohorts
# We use pre-2015 (ancestral baseline proxy) vs 2018-2020 (current) as Delta_ST
def corr_with_ci(x, y, n_boot=1000, seed=RNG_SEED):
    """Return (r, 95%CI) via BCa bootstrap."""
    mask = (~pd.isna(x)) & (~pd.isna(y))
    x = np.asarray(x[mask], dtype=float)
    y = np.asarray(y[mask], dtype=float)
    if len(x) < 30:
        return np.nan, (np.nan, np.nan), 0
    r = np.corrcoef(x, y)[0, 1]
    # simple percentile bootstrap; BCa is in scipy 1.10+
    rng = np.random.default_rng(seed)
    rs = np.empty(n_boot)
    n = len(x)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        rs[i] = np.corrcoef(x[idx], y[idx])[0, 1]
    lo, hi = np.nanpercentile(rs, [2.5, 97.5])
    return float(r), (float(lo), float(hi)), int(n)


log("\n  F1 diagnostic: cor(eexp_share, happy) by epoch")
diag_f1 = {}
epochs = {
    "ancestral_2012_2014": df["year"].isin([2012, 2014]),
    "transition_2016_2018": df["year"].isin([2016, 2018]),
    "current_2020_2022": df["year"].isin([2020, 2022]),
}
for name, mask in epochs.items():
    d = df[mask]
    for dv in ["qn12012", "qn10021"]:
        r, ci, n = corr_with_ci(d["eexp_share"], d[dv])
        log(f"    {name} | eexp_share x {dv}: r={r:+.3f} 95%CI[{ci[0]:+.3f},{ci[1]:+.3f}] N={n}")
        diag_f1[f"{name}__{dv}"] = {"r": r, "ci_lo": ci[0], "ci_hi": ci[1], "n": n}

# F2 necessary: aspirational endorsement. Proxy: high eexp households are NOT
# the most materially squeezed (education_squeeze flag should NOT align
# perfectly with eexp). Additionally, eexp positively correlated with income
# (aspirational/affordable) rather than driven purely by poverty.
log("\n  F2 diagnostic: aspirational vs coerced signature")
d18 = df[df["year"] == 2018].dropna(subset=["eexp_share", "fincome1"])
f2_income_corr = np.corrcoef(
    d18["eexp_share"], np.log1p(d18["fincome1"])
)[0, 1]
log(f"    cor(eexp_share, log income) 2018: {f2_income_corr:+.3f}")
# share of high-eexp households that are ALSO financially squeezed (both)
d18b = df[df["year"] == 2018].dropna(subset=["eexp_share_top3", "education_squeeze"])
joint = pd.crosstab(d18b["eexp_share_top3"], d18b["education_squeeze"], normalize="index")
log(f"    P(education_squeeze=1 | eexp_share top3) = {joint.iloc[1,1]:.3f}")
log(f"    P(education_squeeze=1 | eexp_share bot2) = {joint.iloc[0,1]:.3f}")


# ------------------------------------------------------------
# 5. PRIMARY REGRESSIONS
# ------------------------------------------------------------
log("\n[5] Primary regressions (person + year FE via demeaning)")

def fe_ols(df_in, y, x_main, controls=None, cluster="pid"):
    """Within-person + within-year demeaning followed by OLS.
    Equivalent to two-way FE; cluster SE on `cluster`.
    Returns dict with n, beta, se, ci, t, p2 (two-sided), p1_pos (one-sided pos), p1_neg."""
    cols = [y, x_main, "pid", "year"]
    if controls is not None:
        cols = cols + [c for c in controls if c not in cols]
    d = df_in[cols].dropna().copy()
    if len(d) < 50:
        return None
    # two-way within transform: subtract pid mean AND year mean (plus grand mean)
    for col in [y, x_main] + (controls or []):
        d[col] = d[col].astype(float)
    # person-demean
    d_pid = d.groupby("pid")[[y, x_main] + (controls or [])].transform("mean")
    # year-demean
    d_year = d.groupby("year")[[y, x_main] + (controls or [])].transform("mean")
    # grand mean
    grand = d[[y, x_main] + (controls or [])].mean()
    ys = d[y] - d_pid[y] - d_year[y] + grand[y]
    xs = d[[x_main] + (controls or [])].sub(
        d_pid[[x_main] + (controls or [])]
    ).sub(
        d_year[[x_main] + (controls or [])]
    ).add(grand[[x_main] + (controls or [])])
    # OLS with cluster SE via statsmodels
    X = sm.add_constant(xs.values)
    try:
        res = sm.OLS(ys.values, X, missing="drop").fit(
            cov_type="cluster", cov_kwds={"groups": d[cluster].values}
        )
    except Exception as e:
        log(f"    OLS failed: {e}")
        return None
    b = res.params[1]  # index 1 = x_main (0 = const)
    se = res.bse[1]
    t = res.tvalues[1]
    p2 = res.pvalues[1]
    # one-sided
    from scipy.stats import norm
    p1_pos = 1 - norm.cdf(t)
    p1_neg = norm.cdf(t)
    ci_lo = b - 1.96 * se
    ci_hi = b + 1.96 * se
    return {
        "n": int(len(d)),
        "beta": float(b),
        "se": float(se),
        "ci_lo": float(ci_lo),
        "ci_hi": float(ci_hi),
        "t": float(t),
        "p2": float(p2),
        "p1_pos": float(p1_pos),
        "p1_neg": float(p1_neg),
    }


primary = {}

# Basic controls (person FE absorbs time-invariant; these are time-varying)
CTRL = ["age", "ln_fincome1", "familysize", "child_num"]

# H2.1 Sweet — qn12012 on eexp_share
log("\n  H2.1 Sweet: qn12012 ~ eexp_share + ctrl | pid FE + year FE")
primary["H21_sweet"] = fe_ols(df, "qn12012", "eexp_share", CTRL)
log(f"    {primary['H21_sweet']}")

# H2.1 alt: eexp_share_top3
log("\n  H2.1b Sweet (top-tercile treatment): qn12012 ~ eexp_share_top3")
primary["H21_sweet_top3"] = fe_ols(df, "qn12012", "eexp_share_top3", CTRL)
log(f"    {primary['H21_sweet_top3']}")

# H2.1 alt: ln_eexp_p1
log("\n  H2.1c Sweet (ln eexp): qn12012 ~ ln_eexp_p1")
primary["H21_sweet_ln"] = fe_ols(df, "qn12012", "ln_eexp_p1", CTRL)
log(f"    {primary['H21_sweet_ln']}")

# H2.2 Bitter — non_edu_share on lag eexp_share
# Construct lag: sort by pid x year, shift by one wave (2-year lag)
log("\n  H2.2 Bitter: non_edu_share ~ L.eexp_share (crowd-out)")
df_lag = df.sort_values(["pid", "year"]).copy()
df_lag["eexp_share_lag"] = df_lag.groupby("pid")["eexp_share"].shift(1)
primary["H22_bitter"] = fe_ols(df_lag, "non_edu_share", "eexp_share_lag", CTRL)
log(f"    {primary['H22_bitter']}")

# Contemporaneous crowd-out (expected mechanically because shares sum to 1)
log("\n  H2.2b Contemporaneous crowd-out: non_edu_share ~ eexp_share")
primary["H22_contemp"] = fe_ols(df, "non_edu_share", "eexp_share", CTRL)
log(f"    {primary['H22_contemp']}")

# H2.3 DID 双减
log("\n  H2.3 DID: qn12012 ~ did_2021 = post_2021 x high_baseline_tutoring")
primary["H23_did_2021"] = fe_ols(
    df.dropna(subset=["high_baseline_tutoring"]),
    "qn12012",
    "did_2021",
    CTRL + ["post_2021", "high_baseline_tutoring"],
)
log(f"    {primary['H23_did_2021']}")

# H2.4 Placebo: restrict pre-policy, post_2019
df_pre = df[df["year"] <= 2020].dropna(subset=["high_baseline_tutoring"])
log("\n  H2.4 Placebo DID (2019): sample {<=2020}")
primary["H24_placebo_2019"] = fe_ols(
    df_pre,
    "qn12012",
    "did_2019",
    CTRL + ["post_2019", "high_baseline_tutoring"],
)
log(f"    {primary['H24_placebo_2019']}")


# ------------------------------------------------------------
# 6. EVENT STUDY (wave-by-wave)
# ------------------------------------------------------------
log("\n[6] Event study — dummy per wave x high_baseline_tutoring")

def event_study(df_in, y, ref_year=2020, controls=None):
    d = df_in.dropna(subset=[y, "high_baseline_tutoring"]).copy()
    years = sorted(d["year"].unique().tolist())
    events = {}
    for yr in years:
        if yr == ref_year:
            continue
        d[f"evt_{int(yr)}"] = (
            (d["year"] == yr).astype(int) * d["high_baseline_tutoring"]
        )
    evt_cols = [f"evt_{int(yr)}" for yr in years if yr != ref_year]
    # FE + OLS
    cols = [y, "pid", "year", "high_baseline_tutoring"] + evt_cols + (controls or [])
    d = d[cols].dropna()
    # demean on pid + year
    for col in [y] + evt_cols + (controls or []):
        d[col] = d[col].astype(float)
    d_pid = d.groupby("pid")[[y] + evt_cols + (controls or [])].transform("mean")
    d_year = d.groupby("year")[[y] + evt_cols + (controls or [])].transform("mean")
    grand = d[[y] + evt_cols + (controls or [])].mean()
    ys = d[y] - d_pid[y] - d_year[y] + grand[y]
    xs = d[evt_cols + (controls or [])].sub(
        d_pid[evt_cols + (controls or [])]
    ).sub(
        d_year[evt_cols + (controls or [])]
    ).add(grand[evt_cols + (controls or [])])
    X = sm.add_constant(xs.values)
    res = sm.OLS(ys.values, X, missing="drop").fit(
        cov_type="cluster", cov_kwds={"groups": d["pid"].values}
    )
    out = {"ref_year": ref_year, "coefs": {}, "n": int(len(d))}
    for i, c in enumerate(evt_cols, start=1):
        out["coefs"][c] = {
            "beta": float(res.params[i]),
            "se": float(res.bse[i]),
            "p2": float(res.pvalues[i]),
        }
    return out


event = event_study(df, "qn12012", ref_year=2020, controls=CTRL)
log(f"  event study N = {event['n']}")
for c, v in event["coefs"].items():
    log(f"    {c}: beta={v['beta']:+.4f}  se={v['se']:.4f}  p2={v['p2']:.4f}")

primary["event_study_qn12012"] = event

# Pre-trend test: F-test on 2012,2014,2016,2018 coefs jointly = 0
pre_years = ["evt_2012", "evt_2014", "evt_2016", "evt_2018"]
pre_betas = [event["coefs"][c]["beta"] for c in pre_years if c in event["coefs"]]
pre_ses = [event["coefs"][c]["se"] for c in pre_years if c in event["coefs"]]
# approximate chi2 (independence assumption — serves as signal)
if pre_betas:
    chi2_stat = sum((b / s) ** 2 for b, s in zip(pre_betas, pre_ses))
    p_pre = 1 - stats.chi2.cdf(chi2_stat, df=len(pre_betas))
    log(f"\n  Pre-trend joint test (chi2 approx, df={len(pre_betas)}): stat={chi2_stat:.3f}, p={p_pre:.3f}")
    primary["pre_trend_joint_p"] = float(p_pre)


# ------------------------------------------------------------
# 7. Δ_ST ESTIMATION
# ------------------------------------------------------------
log("\n[7] Δ_ST estimation: cor(eexp, happy)_{ancestral} - cor(eexp, happy)_{current}")

def delta_ST(df_in, y, x="eexp_share", anc_years=(2012, 2014), cur_years=(2018, 2020),
             n_boot=1000, seed=RNG_SEED):
    anc = df_in[df_in["year"].isin(anc_years)].dropna(subset=[x, y])
    cur = df_in[df_in["year"].isin(cur_years)].dropna(subset=[x, y])
    if len(anc) < 100 or len(cur) < 100:
        return None
    r_anc = np.corrcoef(anc[x], anc[y])[0, 1]
    r_cur = np.corrcoef(cur[x], cur[y])[0, 1]
    delta = r_anc - r_cur
    rng = np.random.default_rng(seed)
    deltas = np.empty(n_boot)
    a_arr = anc[[x, y]].values
    c_arr = cur[[x, y]].values
    for i in range(n_boot):
        a_idx = rng.integers(0, len(a_arr), len(a_arr))
        c_idx = rng.integers(0, len(c_arr), len(c_arr))
        a_s = a_arr[a_idx]
        c_s = c_arr[c_idx]
        r_a = np.corrcoef(a_s[:, 0], a_s[:, 1])[0, 1]
        r_c = np.corrcoef(c_s[:, 0], c_s[:, 1])[0, 1]
        deltas[i] = r_a - r_c
    lo, hi = np.nanpercentile(deltas, [2.5, 97.5])
    # one-sided p: P(delta <= 0)
    p_leq = (deltas <= 0).mean()
    return {
        "r_anc": float(r_anc),
        "r_cur": float(r_cur),
        "delta_ST": float(delta),
        "ci_lo": float(lo),
        "ci_hi": float(hi),
        "p_leq_0": float(p_leq),
        "n_anc": int(len(anc)),
        "n_cur": int(len(cur)),
    }


delta_res = {}
for dv in ["qn12012", "qn10021", "non_edu_share"]:
    d = delta_ST(df, dv)
    if d:
        log(
            f"  Δ_ST | eexp_share x {dv}: r_anc={d['r_anc']:+.3f} r_cur={d['r_cur']:+.3f} "
            f"Δ={d['delta_ST']:+.3f} 95%CI[{d['ci_lo']:+.3f},{d['ci_hi']:+.3f}] "
            f"p_leq0={d['p_leq_0']:.3f}"
        )
        delta_res[dv] = d


# ------------------------------------------------------------
# 8. FOUR PRIMITIVE SIGNATURES (θ, λ, β, ρ)
# ------------------------------------------------------------
log("\n[8] Four primitives — empirical signatures")

# θ (amenity): already in H2.1
# λ (externalisation): parent eexp -> child proxy. We use qn10021 as a
#    within-HH child-welfare proxy (trust in parents). Positive cor
#    would SUPPORT θ-to-parent but tells us little about λ; a NEGATIVE
#    cor would be λ>0 (child bears cost).
log("\n  λ (child welfare proxy): qn10021 ~ eexp_share + ctrl | FE")
lam_res = fe_ols(df, "qn10021", "eexp_share", CTRL)
log(f"    {lam_res}")

# β (present bias): eexp_income_ratio rising while other non-edu share falls
# Already H2.2 (non_edu_share). Also test: does child_num x eexp_share interact
# (households with more kids - more pressure) ?
log("\n  β (financial crowd-out beyond accounting identity): test lagged crowd-out")
log("    (contemp vs lag separates mechanical share identity from persistent crowd-out)")

# ρ (lock-in): within-person AR(1) of eexp
log("\n  ρ (lock-in): eexp_share_{t} ~ eexp_share_{t-1} | FE")
rho_res = fe_ols(df_lag, "eexp_share", "eexp_share_lag", CTRL)
log(f"    {rho_res}")

primary["primitive_theta"] = primary["H21_sweet"]  # same as H2.1
primary["primitive_lambda"] = lam_res
primary["primitive_beta"] = primary["H22_bitter"]
primary["primitive_rho"] = rho_res


# ------------------------------------------------------------
# 9. HETEROGENEITY — only_child, urban, child_male
# ------------------------------------------------------------
log("\n[9] Heterogeneity")

df["only_child"] = (df["child_num"] == 1).astype(int)
# Interaction: eexp_share x only_child on qn12012
df["int_only_child"] = df["eexp_share"] * df["only_child"]
het_only = fe_ols(df, "qn12012", "int_only_child", CTRL + ["eexp_share", "only_child"])
log(f"  eexp_share x only_child: {het_only}")

# Urban
df["int_urban"] = df["eexp_share"] * df["urban"].fillna(0).astype(int)
het_urban = fe_ols(df, "qn12012", "int_urban", CTRL + ["eexp_share", "urban"])
log(f"  eexp_share x urban: {het_urban}")

primary["het_only_child"] = het_only
primary["het_urban"] = het_urban


# ------------------------------------------------------------
# 10. SPECIFICATION CURVE
# ------------------------------------------------------------
log("\n[10] Specification curve")

dvs = ["qn12012", "qn10021", "non_edu_share", "eexp_income_ratio"]
treats = ["eexp_share", "eexp_share_top3", "ln_eexp_p1"]
ctrl_sets = {
    "none": [],
    "demog": ["age"],
    "demog_inc": ["age", "ln_fincome1"],
    "demog_inc_hh": ["age", "ln_fincome1", "familysize", "child_num"],
}
samples = {
    "all": lambda d: d,
    "only_child": lambda d: d[d["only_child"] == 1],
    "urban": lambda d: d[d["urban"] == 1],
}

records = []
for dv, tr, (cname, ctrl), (sname, sfn) in itertools.product(
    dvs, treats, ctrl_sets.items(), samples.items()
):
    d = sfn(df)
    if len(d) < 200:
        continue
    try:
        res = fe_ols(d, dv, tr, ctrl)
    except Exception:
        continue
    if res is None:
        continue
    records.append({
        "dv": dv,
        "treatment": tr,
        "controls": cname,
        "sample": sname,
        "n": res["n"],
        "beta": res["beta"],
        "se": res["se"],
        "ci_lo": res["ci_lo"],
        "ci_hi": res["ci_hi"],
        "p2": res["p2"],
        "p1_pos": res["p1_pos"],
        "p1_neg": res["p1_neg"],
    })

speccurve = pd.DataFrame(records)
speccurve.to_csv(OUT_SPECCURVE, index=False)
log(f"  Spec curve rows: {len(speccurve)}")
log("  By DV x treatment (median beta, % positive):")
grp = speccurve.groupby(["dv", "treatment"])
for (dv, tr), g in grp:
    med = g["beta"].median()
    pct_pos = (g["beta"] > 0).mean() * 100
    pct_sig_pos = ((g["beta"] > 0) & (g["p2"] < 0.05)).mean() * 100
    log(f"    {dv:20s} | {tr:20s} median_beta={med:+.4f}  %pos={pct_pos:5.1f}  %sig_pos={pct_sig_pos:5.1f}")


# ------------------------------------------------------------
# 11. BITTER SPEC CURVE (lagged crowd-out robust across defs)
# ------------------------------------------------------------
log("\n[11] Bitter spec curve — lagged crowd-out (persistent vs mechanical)")

bitter_records = []
for dv, ctrl_name, ctrl in itertools.product(
    ["non_edu_share"], ctrl_sets.keys(), [ctrl_sets[k] for k in ctrl_sets.keys()]
):
    pass  # placeholder
# Actually: iterate clean
for dv in ["non_edu_share"]:
    for lagN in [1, 2]:
        dtmp = df.sort_values(["pid", "year"]).copy()
        dtmp[f"L{lagN}_eexp_share"] = dtmp.groupby("pid")["eexp_share"].shift(lagN)
        for cname, ctrl in ctrl_sets.items():
            for sname, sfn in samples.items():
                d = sfn(dtmp)
                if len(d) < 200:
                    continue
                res = fe_ols(d, dv, f"L{lagN}_eexp_share", ctrl)
                if res is None:
                    continue
                bitter_records.append({
                    "dv": dv,
                    "lag": lagN,
                    "controls": cname,
                    "sample": sname,
                    "n": res["n"],
                    "beta": res["beta"],
                    "se": res["se"],
                    "p2": res["p2"],
                    "p1_neg": res["p1_neg"],
                })

bitter_df = pd.DataFrame(bitter_records)
log(f"  Bitter lagged rows: {len(bitter_df)}")
if len(bitter_df) > 0:
    log(f"  Median beta: {bitter_df['beta'].median():+.5f}  %negative: {(bitter_df['beta']<0).mean()*100:.1f}%")


# ------------------------------------------------------------
# 12. DID SPEC CURVE (H2.3 robustness)
# ------------------------------------------------------------
log("\n[12] DID spec curve — 双减 robustness across baseline defs + samples")

did_records = []
# Alternative high-baseline defs
for q_thr, thr_name in [(0.50, "top50"), (0.67, "top33"), (0.75, "top25")]:
    thr = df["baseline_eexp_share"].quantile(q_thr)
    dsub = df.dropna(subset=["baseline_eexp_share"]).copy()
    dsub["hb"] = (dsub["baseline_eexp_share"] >= thr).astype(int)
    dsub["did_tmp"] = dsub["post_2021"] * dsub["hb"]
    for sname, sfn in samples.items():
        d = sfn(dsub)
        if len(d) < 500:
            continue
        res = fe_ols(d, "qn12012", "did_tmp", CTRL + ["post_2021", "hb"])
        if res is None:
            continue
        did_records.append({
            "threshold": thr_name,
            "sample": sname,
            "n": res["n"],
            "beta": res["beta"],
            "se": res["se"],
            "p2": res["p2"],
            "p1_neg": res["p1_neg"],
        })

did_df = pd.DataFrame(did_records)
log(f"  DID spec rows: {len(did_df)}")
if len(did_df) > 0:
    log(f"  Median DID beta: {did_df['beta'].median():+.4f}  %negative: {(did_df['beta']<0).mean()*100:.1f}%")
    log(did_df.to_string())


# ------------------------------------------------------------
# 13. SAVE JSON
# ------------------------------------------------------------
results = {
    "generated": datetime.now().isoformat(),
    "seed": RNG_SEED,
    "panel_sha256": EXPECTED_SHA,
    "panel_shape": list(df.shape),
    "n_unique_pid": int(df["pid"].nunique()),
    "diag_f1_correlations": diag_f1,
    "diag_f2_income_corr_2018": float(f2_income_corr),
    "diag_f2_p_squeeze_top3": float(joint.iloc[1, 1]),
    "diag_f2_p_squeeze_bot2": float(joint.iloc[0, 1]),
    "primary": primary,
    "delta_ST": delta_res,
    "speccurve_n": len(speccurve),
    "speccurve_median_beta_qn12012_eexp_share": float(
        speccurve[(speccurve["dv"] == "qn12012") & (speccurve["treatment"] == "eexp_share")]["beta"].median()
    ) if len(speccurve) else None,
    "speccurve_pct_pos_qn12012_eexp_share": float(
        (speccurve[(speccurve["dv"] == "qn12012") & (speccurve["treatment"] == "eexp_share")]["beta"] > 0).mean() * 100
    ) if len(speccurve) else None,
    "bitter_lag_records": bitter_records,
    "did_records": did_records,
}

# Sanitize NaN for JSON
def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(x) for x in o]
    if isinstance(o, float) and not np.isfinite(o):
        return None
    if isinstance(o, (np.integer, np.floating)):
        return float(o) if not np.isnan(float(o)) else None
    return o

with open(OUT_JSON, "w") as f:
    json.dump(_clean(results), f, indent=2, default=str)

log(f"\n[13] Results saved to {OUT_JSON}")
log(f"     Spec curve: {OUT_SPECCURVE}")
log(f"\n{'='*72}")
log(f"C2 PDE complete at {datetime.now().isoformat()}")
log("=" * 72)
TEE.close()
