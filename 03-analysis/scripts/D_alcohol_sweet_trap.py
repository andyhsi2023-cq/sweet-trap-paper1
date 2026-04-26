#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D_alcohol Sweet Trap PDE — Strict F2 Three-Way Diagnostic
==========================================================

Purpose
  Execute the Pre-Registered + Data-driven PDE for Study D_alcohol
  (嗜酒) of the Sweet-Trap cross-species manuscript, with STRICT F2
  three-way type discrimination per sweet_trap_formal_model_v2 §1.2 and
  feedback_sweet_trap_strict_F2.md.

Core challenge
  Alcohol use is HETEROGENEOUS with three conceptually distinct types:
    A. Aspirational social drinking — candidate Sweet Trap
    B. Coerced business entertaining (酒桌文化) — F2 fails (like 996)
    C. Addiction / dependence — F2 epistemic fails (model v2 §1.2)
  These MUST be separated before any Sweet Trap test.

Data
  Panel: 02-data/processed/panel_D_alcohol.parquet
  SHA-256 lock: 19af15890eb0785b9a5aa64c20c241d7e904cfcdf8e38c2d8f6ee55dad1fa126
  96,628 person-waves, 25,873 unique persons, 5 waves 2011-2020 (CHARLS).

Sweet Trap mapping (Layer A bridge)
  D_alcohol candidate bridge:
    - A4 Drosophila supernormal sweet (Δ_ST = +0.71): metabolic overshoot
    - A5 Drosophila ethanol preference: 果蝇 active preference for low-dose
      ethanol in fermented fruit (ancestral energy + anti-parasite)
    - Human: ethanol metabolism calibrated to scarce fermentation →
      industrial alcohol flood → liver, cardiovascular, cancer outcomes
  Predicted human type-A Δ_ST band: +0.20 to +0.45 (softer than A4 because
  humans can self-report mis-calibration in part via hangover feedback).

Outputs
  02-data/processed/D_alcohol_results.json
  02-data/processed/D_alcohol_speccurve.csv
  03-analysis/scripts/D_alcohol_sweet_trap.log
  00-design/pde/D_alcohol_findings.md  (written separately)

Constraints
  - n_workers = 1 (no multiprocessing).
  - SHA-256 verified; panel NOT modified.
  - Random seed 20260417 for bootstrap CIs.
  - Code comments in English; findings report in Chinese.
"""

from __future__ import annotations
import os, json, hashlib, itertools, warnings
from datetime import datetime

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

# ------------------------------------------------------------
# PATHS & CONSTANTS
# ------------------------------------------------------------
BASE = os.path.expanduser("~/Desktop/Research/sweet-trap-multidomain")
DATA_PATH = os.path.join(BASE, "02-data/processed/panel_D_alcohol.parquet")
EXPECTED_SHA = "19af15890eb0785b9a5aa64c20c241d7e904cfcdf8e38c2d8f6ee55dad1fa126"
OUT_JSON = os.path.join(BASE, "02-data/processed/D_alcohol_results.json")
OUT_SCA = os.path.join(BASE, "02-data/processed/D_alcohol_speccurve.csv")
LOG_PATH = os.path.join(BASE, "03-analysis/scripts/D_alcohol_sweet_trap.log")

SEED = 20260417
np.random.seed(SEED)
ALPHA = 0.05
B_BOOT = 500  # bootstrap reps

# ------------------------------------------------------------
# LOGGER
# ------------------------------------------------------------
def make_logger(path):
    f = open(path, "w")
    def log(msg=""):
        print(msg)
        f.write(str(msg) + "\n"); f.flush()
    return log, f

log, logfile = make_logger(LOG_PATH)
log(f"D_alcohol PDE — run at {datetime.now().isoformat()}")
log("Script: 03-analysis/scripts/D_alcohol_sweet_trap.py")
log("=" * 72)

# ------------------------------------------------------------
# [1/10] SHA verification + data load
# ------------------------------------------------------------
log("\n[1/10] DATA VERIFICATION")
with open(DATA_PATH, "rb") as fh:
    actual_sha = hashlib.sha256(fh.read()).hexdigest()
log(f"   expected: {EXPECTED_SHA}")
log(f"   actual:   {actual_sha}")
assert actual_sha == EXPECTED_SHA, "SHA-256 mismatch"
log("   SHA-256 match: PASS")

df = pd.read_parquet(DATA_PATH)
log(f"   panel shape: {df.shape}, unique ID: {df['ID'].nunique():,}")
log(f"   waves: {sorted(df['wave'].dropna().astype(int).unique())}")
log(f"   iwy:   {sorted(df['iwy'].dropna().astype(int).unique())}")

# Coerce numeric
num_cols = [c for c in df.columns if c not in ('ID','householdID','communityID','nation','province','city')]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# ------------------------------------------------------------
# [2/10] DESCRIPTIVES
# ------------------------------------------------------------
log("\n[2/10] DESCRIPTIVES — overall alcohol landscape in CHARLS 2011-2020")
log("-" * 60)

overall = {}
for w in sorted(df['wave'].dropna().astype(int).unique()):
    sub = df[df['wave']==w]
    p_drink = (sub['drinkl']==1).mean()
    p_drinkev = (sub['drinkev']==1).mean()
    p_liver = (sub['livere']==1).mean()
    log(f"   wave {w} (n={len(sub):,}): drinkl={p_drink:.3f}  drinkev={p_drinkev:.3f}  livere={p_liver:.4f}")
    overall[f'wave{w}'] = dict(n=len(sub), p_drinkl=float(p_drink),
                                p_drinkev=float(p_drinkev), p_livere=float(p_liver))

# By gender (Chinese drinking is strongly male-skewed)
log("\n   Drinking rate by gender:")
for g in [1, 2]:
    sub = df[df['gender']==g]
    p = (sub['drinkl']==1).mean()
    log(f"     gender={g}: n={len(sub):,}  p(drinkl)={p:.3f}")

# Frequency distribution among current drinkers
log("\n   Frequency distribution (drinkn_c in 2011/2013/2018 waves, among drinkl=1):")
freq_dist = df[df['drinkl']==1]['drinkn_c'].value_counts().sort_index()
log(str(freq_dist))

# ------------------------------------------------------------
# [3/10] F2 THREE-WAY DIAGNOSTIC (CORE of this study)
# ------------------------------------------------------------
log("\n[3/10] F2 THREE-WAY DIAGNOSTIC — separating Type A / B / C")
log("=" * 60)

# Current drinker sample
cur = df[df['drinkl']==1].copy()
log(f"   Total current-drinker person-waves: {len(cur):,}")
log(f"   Unique current-drinker IDs: {cur['ID'].nunique():,}")

# Hard-label counts
tA = int(cur['type_A'].sum())
tB = int(cur['type_B'].sum())
tC = int(cur['type_C'].sum())
tUnk = int((cur[['type_A','type_B','type_C']].sum(axis=1)==0).sum())
log(f"\n   Hard labels among current drinkers:")
log(f"     Type A (aspirational social):  {tA:,}  ({tA/len(cur)*100:.2f}%)")
log(f"     Type B (coerced business):     {tB:,}  ({tB/len(cur)*100:.2f}%)")
log(f"     Type C (daily+ / addict):      {tC:,}  ({tC/len(cur)*100:.2f}%)")
log(f"     Unclassified:                  {tUnk:,}  ({tUnk/len(cur)*100:.2f}%)")
log(f"   (Note: Type A/B/C definitions allow some overlap — sum may exceed 100%)")

# Overlap matrix
log(f"\n   Overlap (current drinkers only):")
log(f"     A&B: {int(((cur['type_A']==1)&(cur['type_B']==1)).sum())}")
log(f"     A&C: {int(((cur['type_A']==1)&(cur['type_C']==1)).sum())}")
log(f"     B&C: {int(((cur['type_B']==1)&(cur['type_C']==1)).sum())}")
log(f"     A&B&C: {int(((cur['type_A']==1)&(cur['type_B']==1)&(cur['type_C']==1)).sum())}")

# F2 SES-gradient test: for EACH type separately, do higher-SES choose it?
log("\n   F2 aspirational-selection test BY TYPE:")
log("   (Sweet Trap requires POSITIVE SES gradient for Type A; Type B/C may differ)")

f2_results = {}
for label, mask in [('type_A', cur['type_A']==1),
                    ('type_B', cur['type_B']==1),
                    ('type_C', cur['type_C']==1),
                    ('all_drinkers', cur['drinkl']==1)]:
    sub = cur[mask]
    if len(sub) < 50:
        log(f"     {label}: n={len(sub)} too small, skip")
        continue
    # SES gradient: within current drinkers, is being in THIS type positively correlated with income/edu?
    cur_sub = cur.dropna(subset=['ln_income','edu','rural'])
    is_type = (cur_sub[label]==1).astype(float) if label != 'all_drinkers' else (cur_sub['drinkl']==1).astype(float)
    r_inc = float(is_type.corr(cur_sub['ln_income']))
    r_edu = float(is_type.corr(cur_sub['edu']))
    r_rural = float(is_type.corr(cur_sub['rural']))
    log(f"     {label}: r(type, ln_income)={r_inc:+.4f} | r(type, edu)={r_edu:+.4f} | r(type, rural)={r_rural:+.4f}")
    f2_results[label] = dict(n=len(sub), r_ln_income=r_inc, r_edu=r_edu, r_rural=r_rural)

# F2 voluntariness test (Type A): does social activity go together with drinking?
log("\n   F2 voluntariness proxies for Type A:")
tA_sample = cur[cur['type_A']==1]
if len(tA_sample) > 50:
    p_soc = tA_sample['has_social'].mean()
    log(f"     Type A: P(any social activity) = {p_soc:.4f}  [required 1.00 by construction]")
    # compare Type A vs all-drinker baseline
    r_tA_soc = float((cur['type_A']==1).astype(float).corr(cur['has_social']))
    log(f"     Within current drinkers: r(type_A, has_social) = {r_tA_soc:+.4f}")
# Type C: epistemic fail proxies (cesd high + livere high)
log("\n   F2 epistemic-fail proxies for Type C (expected: YES for F2-fail Type C):")
tC_sample = cur[cur['type_C']==1]
tA_sample2 = cur[cur['type_A']==1]
if len(tC_sample) > 50 and len(tA_sample2) > 50:
    cesd_C = tC_sample['cesd10'].mean()
    cesd_A = tA_sample2['cesd10'].mean()
    liver_C = tC_sample['livere'].mean()
    liver_A = tA_sample2['livere'].mean()
    log(f"     Type C mean CES-D: {cesd_C:.2f}  vs  Type A: {cesd_A:.2f}")
    log(f"     Type C liver-disease rate: {liver_C:.4f}  vs  Type A: {liver_A:.4f}")

# Overall verdict
log("\n   F2 VERDICT:")
if f2_results.get('type_A', {}).get('r_ln_income', 0) > 0 and f2_results.get('type_A', {}).get('r_edu', 0) > 0:
    log("     Type A F2: PASS (positive SES gradient, social context present)")
else:
    log("     Type A F2: MARGINAL — SES gradient weak")

# ------------------------------------------------------------
# [4/10] SWEET SIDE (θ) — short-run welfare for Type A specifically
# ------------------------------------------------------------
log("\n[4/10] SWEET SIGNAL θ — within-person fixed-effects on life_sat")
log("=" * 60)

def fe_regression(data, y, x, controls=None, cluster='ID', label=''):
    """Fit y ~ x + controls with person FE (demean within ID) and clustered SE."""
    controls = controls or []
    cols = [y, x, cluster] + controls
    d = data.dropna(subset=cols).copy()
    if len(d) < 100:
        return dict(label=label, n=len(d), beta=np.nan, se=np.nan, ci_lo=np.nan, ci_hi=np.nan, p=np.nan)
    # Demean within ID
    for c in [y, x] + controls:
        d[c+'_dm'] = d[c] - d.groupby(cluster)[c].transform('mean')
    X = d[[x+'_dm'] + [c+'_dm' for c in controls]].values
    X = sm.add_constant(X, has_constant='add')
    yv = d[y+'_dm'].values
    try:
        res = sm.OLS(yv, X, missing='drop').fit(
            cov_type='cluster',
            cov_kwds={'groups': d[cluster].values}
        )
        beta = float(res.params[1])
        se = float(res.bse[1])
        ci_lo = float(res.conf_int()[1, 0])
        ci_hi = float(res.conf_int()[1, 1])
        p = float(res.pvalues[1])
        return dict(label=label, n=len(d), beta=beta, se=se, ci_lo=ci_lo, ci_hi=ci_hi, p=p)
    except Exception as e:
        return dict(label=label, n=len(d), beta=np.nan, error=str(e))

# Sweet tests
sweet_results = []
# (a) All current drinkers pooled — baseline
for y, ylabel in [('satlife','SATLIFE'), ('srh','SRH'), ('cesd10','CESD')]:
    # Treatment: drinkl (binary: currently drink vs not)
    r = fe_regression(df, y, 'drinkl', controls=['age','edu','ln_income','rural','gender'], label=f'{ylabel}~drinkl_POOLED')
    log(f"   {r['label']:30s}  n={r['n']:>6}  β={r.get('beta',np.nan):+.4f}  95% CI [{r.get('ci_lo',np.nan):+.4f},{r.get('ci_hi',np.nan):+.4f}]  p={r.get('p',np.nan):.4f}")
    sweet_results.append(r)

# (b) Type A subsample — core Sweet Trap test
log("\n   TYPE A SUBSAMPLE (aspirational social drinking):")
dfA = df.copy()
# For Type A analysis: treatment is being in Type A vs not current drinker (same cohort)
dfA['is_type_A'] = dfA['type_A']
for y, ylabel in [('satlife','SATLIFE'), ('srh','SRH'), ('cesd10','CESD')]:
    r = fe_regression(dfA, y, 'is_type_A', controls=['age','edu','ln_income','rural','gender','has_social'], label=f'{ylabel}~TypeA_vs_baseline')
    log(f"   {r['label']:40s}  n={r['n']:>6}  β={r.get('beta',np.nan):+.4f}  95% CI [{r.get('ci_lo',np.nan):+.4f},{r.get('ci_hi',np.nan):+.4f}]  p={r.get('p',np.nan):.4f}")
    sweet_results.append(r)

# (c) Frequency-continuous effect within current drinkers (Type A proxy: low-mid freq)
dfF = df[(df['drinkl']==1) & (df['drinkn_c'].notna())].copy()
for y, ylabel in [('satlife','SATLIFE'), ('srh','SRH'), ('cesd10','CESD')]:
    r = fe_regression(dfF, y, 'drinkn_c', controls=['age','edu','ln_income','rural','gender'], label=f'{ylabel}~drinkn_c_CURDRINK')
    log(f"   {r['label']:40s}  n={r['n']:>6}  β={r.get('beta',np.nan):+.4f}  95% CI [{r.get('ci_lo',np.nan):+.4f},{r.get('ci_hi',np.nan):+.4f}]  p={r.get('p',np.nan):.4f}")
    sweet_results.append(r)

# (d) Non-linear check: moderate (A) vs heavy (C) frequency
dfX = df[df['drinkl']==1].copy()
dfX['freq_heavy'] = (dfX['drinkn_c']>=6).astype(float)
dfX['freq_moderate'] = ((dfX['drinkn_c']>=1)&(dfX['drinkn_c']<=4)).astype(float)
for y, ylabel in [('satlife','SATLIFE'), ('srh','SRH'), ('cesd10','CESD')]:
    r1 = fe_regression(dfX, y, 'freq_moderate', controls=['age','edu','ln_income','gender'], label=f'{ylabel}~moderate(1-4)')
    r2 = fe_regression(dfX, y, 'freq_heavy', controls=['age','edu','ln_income','gender'], label=f'{ylabel}~heavy(6+)')
    log(f"   {r1['label']:40s}  n={r1['n']:>6}  β={r1.get('beta',np.nan):+.4f}  p={r1.get('p',np.nan):.4f}")
    log(f"   {r2['label']:40s}  n={r2['n']:>6}  β={r2.get('beta',np.nan):+.4f}  p={r2.get('p',np.nan):.4f}")
    sweet_results.extend([r1, r2])

# ------------------------------------------------------------
# [5/10] BITTER SIDE — liver, cardiovascular, cancer
# ------------------------------------------------------------
log("\n[5/10] BITTER — long-run biomarkers & disease outcomes")
log("=" * 60)

bitter_results = []

# (a) Liver disease prevalence by type (within-person rare, so use between-person)
log("\n   Liver disease rate by type (any observation):")
for label, mask_str in [('Type A',"(df['type_A']==1)"),
                        ('Type B',"(df['type_B']==1)"),
                        ('Type C',"(df['type_C']==1)"),
                        ('Non-drinker (drinkev==0)', "(df['drinkev']==0)"),
                        ('Ex-drinker',"(df['drinkev']==1)&(df['drinkl']==0)")]:
    mask = eval(mask_str)
    sub = df[mask]
    if len(sub) < 50:
        continue
    p_liver = float((sub['livere']==1).mean())
    n = len(sub)
    # Wilson CI for proportion
    from statsmodels.stats.proportion import proportion_confint
    k = int((sub['livere']==1).sum())
    ci = proportion_confint(k, n, alpha=0.05, method='wilson')
    log(f"     {label:35s}  n={n:>6}  P(liver)={p_liver:.4f}  95% CI [{ci[0]:.4f}, {ci[1]:.4f}]")
    bitter_results.append(dict(group=label, n=n, p_liver=p_liver, ci_lo=ci[0], ci_hi=ci[1]))

# (b) Hazard of FIRST liver disease (0 → 1) as function of previous wave drinking intensity
log("\n   First-liver-disease event (0→1) as function of lag drinking:")
dfH = df.sort_values(['ID','wave']).copy()
dfH['livere_lag'] = dfH.groupby('ID')['livere'].shift(1)
dfH['drinkl_lag'] = dfH.groupby('ID')['drinkl'].shift(1)
dfH['drinkn_lag'] = dfH.groupby('ID')['drinkn_c'].shift(1)
dfH['newliver'] = ((dfH['livere']==1) & (dfH['livere_lag']==0)).astype(float)
at_risk = dfH[dfH['livere_lag']==0].copy()
log(f"   at-risk (livere_lag==0): {len(at_risk):,}")
if len(at_risk) > 500:
    # Logit
    X_cols = ['drinkl_lag','drinkn_lag','age','gender','edu','rural','smoken']
    sub_h = at_risk.dropna(subset=X_cols+['newliver'])
    X = sm.add_constant(sub_h[X_cols].astype(float))
    y_h = sub_h['newliver'].astype(float)
    try:
        logit = sm.Logit(y_h, X).fit(disp=0)
        for var in ['drinkl_lag','drinkn_lag']:
            if var in logit.params.index:
                b = float(logit.params[var])
                se = float(logit.bse[var])
                ci = logit.conf_int().loc[var]
                p = float(logit.pvalues[var])
                log(f"     logit β({var}) = {b:+.4f}  [{ci[0]:+.4f},{ci[1]:+.4f}]  p={p:.4f}  OR={np.exp(b):.3f}")
                bitter_results.append(dict(label=f'logit_newliver_{var}', n=len(sub_h), beta=b, ci_lo=float(ci[0]), ci_hi=float(ci[1]), p=p, OR=float(np.exp(b))))
    except Exception as e:
        log(f"     logit failed: {e}")

# (c) Biomarker levels by drinking type (cross-sectional, 2011 baseline)
log("\n   Biomarker means by type (wave 1 = 2011 baseline):")
w1 = df[df['wave']==1]
biom_vars = ['bl_crp','bl_cho','bl_ldl','bl_hdl','bl_hbalc','bl_glu','bl_ua','bl_tg','systo','bmi']
biom_vars = [v for v in biom_vars if v in w1.columns]
for v in biom_vars:
    row = {}
    for tlabel, mask in [('A',w1['type_A']==1),('B',w1['type_B']==1),('C',w1['type_C']==1),
                         ('Non',w1['drinkev']==0)]:
        sub = w1[mask][v].dropna()
        if len(sub) >= 20:
            row[tlabel] = f'{sub.mean():.2f} (n={len(sub)})'
        else:
            row[tlabel] = 'n<20'
    log(f"     {v:10s}  A: {row.get('A','?'):20s}  B: {row.get('B','?'):20s}  C: {row.get('C','?'):20s}  Non: {row.get('Non','?')}")

# (d) Hospitalization & cost (bitter monetary)
log("\n   Hospitalization rate (annual, past year) by type:")
for label, mask in [('A',df['type_A']==1),('B',df['type_B']==1),('C',df['type_C']==1),
                    ('Non-drinker',df['drinkev']==0)]:
    sub = df[mask].dropna(subset=['hospital'])
    if len(sub) > 50:
        p = float((sub['hospital']==1).mean())
        log(f"     {label:20s}  n={len(sub):>6}  P(hospital)={p:.4f}")

# ------------------------------------------------------------
# [6/10] ρ LOCK-IN — persistence / autocorrelation
# ------------------------------------------------------------
log("\n[6/10] ρ LOCK-IN — drinking persistence")
log("=" * 60)

dfL = df.sort_values(['ID','wave']).copy()
dfL['drinkl_lag1'] = dfL.groupby('ID')['drinkl'].shift(1)
dfL['drinkn_lag1'] = dfL.groupby('ID')['drinkn_c'].shift(1)

# AR(1) for drinkl
sub = dfL.dropna(subset=['drinkl','drinkl_lag1'])
# P(drinkl=1 | drinkl_lag=1) vs P(drinkl=1 | drinkl_lag=0)
p11 = float(sub[sub['drinkl_lag1']==1]['drinkl'].mean())
p01 = float(sub[sub['drinkl_lag1']==0]['drinkl'].mean())
log(f"   P(drink_t=1 | drink_lag=1) = {p11:.4f}")
log(f"   P(drink_t=1 | drink_lag=0) = {p01:.4f}")
log(f"   Persistence gap          = {p11-p01:+.4f}  (large = strong ρ lock-in)")

# Within-person autocorrelation on continuous frequency
sub_f = dfL.dropna(subset=['drinkn_c','drinkn_lag1'])
if len(sub_f) > 500:
    r_ar = float(sub_f['drinkn_c'].corr(sub_f['drinkn_lag1']))
    log(f"   cor(drinkn_t, drinkn_lag1) = {r_ar:+.4f}  (N={len(sub_f):,})")

# Type C pattern: P(still type_C | type_C_lag)
dfL['type_C_lag'] = dfL.groupby('ID')['type_C'].shift(1)
sub_c = dfL.dropna(subset=['type_C','type_C_lag'])
pcc = float(sub_c[sub_c['type_C_lag']==1]['type_C'].mean())
pac = float(sub_c[sub_c['type_A']==1 if 'type_A' in sub_c.columns else sub_c['type_C_lag']==0]['type_C'].mean())
log(f"   P(type_C_t | type_C_lag=1) = {pcc:.4f}  (conditional 2-wave lock-in)")

rho_results = dict(
    p_drink_given_lag1=p11, p_drink_given_lag0=p01, gap=float(p11-p01),
    ar1_freq=float(r_ar) if len(sub_f)>500 else None,
    p_stay_C=pcc,
)

# ------------------------------------------------------------
# [7/10] Δ_ST CROSS-SPECIES BRIDGE
# ------------------------------------------------------------
log("\n[7/10] Δ_ST (ancestral vs current) — cross-species signature")
log("=" * 60)

# For alcohol, the "ancestral" reference population = light social drinkers
# in the 45-55 pre-heavy-exposure cohort (wave 1). The "current" = heavy 65+
# with liver disease / high freq.
# Alternative framing: compute cor(drinkn_c, welfare) among low-exposure
# vs high-exposure subsamples and compute the delta (as a proxy for
# ancestral-to-current reward-fitness decoupling).

def delta_st(data_anc, data_cur, x, y):
    """Compute Δ_ST = cor(x, y)_anc - cor(x, y)_cur with bootstrap CI."""
    sub_a = data_anc.dropna(subset=[x, y])
    sub_c = data_cur.dropna(subset=[x, y])
    if len(sub_a) < 100 or len(sub_c) < 100:
        return None
    r_a = float(sub_a[x].corr(sub_a[y]))
    r_c = float(sub_c[x].corr(sub_c[y]))
    delta = r_a - r_c  # Positive delta = reward-fitness coupling weakened (Sweet Trap direction)
    # Bootstrap CI
    boots = []
    for b in range(B_BOOT):
        a_b = sub_a.sample(n=len(sub_a), replace=True, random_state=SEED+b)
        c_b = sub_c.sample(n=len(sub_c), replace=True, random_state=SEED+b+100000)
        try:
            ra = a_b[x].corr(a_b[y])
            rc = c_b[x].corr(c_b[y])
            boots.append(float(ra - rc))
        except Exception:
            pass
    boots = np.array(boots)
    ci = np.nanpercentile(boots, [2.5, 97.5])
    return dict(n_anc=len(sub_a), n_cur=len(sub_c), r_anc=r_a, r_cur=r_c,
                delta_st=delta, ci_lo=float(ci[0]), ci_hi=float(ci[1]))

# Ancestral = light drinkers (freq 1-2) + younger cohort (<55)
# Current = heavy drinkers (freq >=5) + older cohort (60+)
log("   Framing: ancestral = light+young | current = heavy+old")
anc_mask = (df['drinkl']==1) & (df['drinkn_c'].between(1,2)) & (df['age']<55)
cur_mask = (df['drinkl']==1) & (df['drinkn_c']>=5) & (df['age']>=60)
log(f"   ancestral n={int(anc_mask.sum())}, current n={int(cur_mask.sum())}")

delta_results = {}
for x, y in [('drinkn_c','satlife'), ('drinkn_c','srh'), ('drinkn_c','cesd10')]:
    d = delta_st(df[anc_mask], df[cur_mask], x, y)
    if d:
        log(f"   Δ_ST({x}→{y}): r_anc={d['r_anc']:+.4f} r_cur={d['r_cur']:+.4f} → Δ={d['delta_st']:+.4f} 95% CI [{d['ci_lo']:+.4f},{d['ci_hi']:+.4f}]")
        delta_results[f'{x}_{y}'] = d
    else:
        log(f"   Δ_ST({x}→{y}): sample too small")

# Alternative: wave-based split (2011 baseline vs 2018 mature)
log("\n   Alternative: wave-based split (2011 vs 2018-2020)")
df_w1 = df[df['wave']==1]
df_w45 = df[df['wave'].isin([4,5])]
for x, y in [('drinkl','satlife'), ('drinkl','srh')]:
    d = delta_st(df_w1, df_w45, x, y)
    if d:
        log(f"   Δ_ST_wave({x}→{y}): r_11={d['r_anc']:+.4f} r_1820={d['r_cur']:+.4f} → Δ={d['delta_st']:+.4f} 95% CI [{d['ci_lo']:+.4f},{d['ci_hi']:+.4f}]")
        delta_results[f'wave_{x}_{y}'] = d

# ------------------------------------------------------------
# [8/10] SPECIFICATION CURVE (≥ 144 specs)
# ------------------------------------------------------------
log("\n[8/10] SPECIFICATION CURVE — Type A core (satlife & srh DVs)")
log("=" * 60)

# Spec dimensions:
#   treatment: drinkl | drinkn_c | type_A | freq_moderate
#   DV: satlife | srh | cesd10
#   sample: all | drinkers_only | age<65 | age>=55 | men_only
#   controls: minimal | baseline | full
#   FE: within-person | cross-sectional
# Total = 4 × 3 × 5 × 3 × 2 = 360 specs. OK.

treatments = ['drinkl', 'drinkn_c', 'type_A', 'freq_moderate']
dvs = ['satlife', 'srh', 'cesd10']
samples = [
    ('all', lambda d: d.copy()),
    ('current_drinkers', lambda d: d[d['drinkl']==1].copy()),
    ('age_lt65', lambda d: d[d['age']<65].copy()),
    ('age_ge55', lambda d: d[d['age']>=55].copy()),
    ('men_only', lambda d: d[d['gender']==1].copy()),
]
control_sets = [
    ('minimal', []),
    ('baseline', ['age','gender','edu']),
    ('full', ['age','gender','edu','ln_income','rural','smoken']),
]
fe_opts = ['within_person', 'cross_sectional']

spec_rows = []
df_spec = df.copy()
# Pre-compute derived
df_spec['freq_moderate'] = ((df_spec['drinkn_c']>=1)&(df_spec['drinkn_c']<=4)).astype(float)

i_spec = 0
for tr in treatments:
    for dv in dvs:
        for sname, sfn in samples:
            for cname, cset in control_sets:
                for fe in fe_opts:
                    i_spec += 1
                    dsub = sfn(df_spec)
                    cols = [tr, dv] + cset + ['ID']
                    d = dsub.dropna(subset=[tr, dv])
                    d = d.dropna(subset=[c for c in cset if c in d.columns])
                    if len(d) < 200:
                        spec_rows.append(dict(
                            spec=i_spec, treatment=tr, dv=dv, sample=sname,
                            controls=cname, fe=fe, n=len(d), beta=np.nan, se=np.nan,
                            ci_lo=np.nan, ci_hi=np.nan, p=np.nan))
                        continue
                    try:
                        if fe == 'within_person':
                            for c in [tr, dv] + cset:
                                d[c+'_dm'] = d[c] - d.groupby('ID')[c].transform('mean')
                            X = d[[tr+'_dm'] + [c+'_dm' for c in cset]].values
                            X = sm.add_constant(X, has_constant='add')
                            yv = d[dv+'_dm'].values
                            res = sm.OLS(yv, X, missing='drop').fit(
                                cov_type='cluster',
                                cov_kwds={'groups': d['ID'].values}
                            )
                        else:
                            X = d[[tr] + cset].astype(float).values
                            X = sm.add_constant(X, has_constant='add')
                            yv = d[dv].astype(float).values
                            res = sm.OLS(yv, X, missing='drop').fit(
                                cov_type='cluster',
                                cov_kwds={'groups': d['ID'].values}
                            )
                        beta = float(res.params[1])
                        se = float(res.bse[1])
                        ci_lo = float(res.conf_int()[1, 0])
                        ci_hi = float(res.conf_int()[1, 1])
                        p = float(res.pvalues[1])
                        spec_rows.append(dict(
                            spec=i_spec, treatment=tr, dv=dv, sample=sname,
                            controls=cname, fe=fe, n=len(d),
                            beta=beta, se=se, ci_lo=ci_lo, ci_hi=ci_hi, p=p))
                    except Exception as e:
                        spec_rows.append(dict(
                            spec=i_spec, treatment=tr, dv=dv, sample=sname,
                            controls=cname, fe=fe, n=len(d), beta=np.nan, p=np.nan,
                            error=str(e)[:100]))

spec_df = pd.DataFrame(spec_rows)
spec_df.to_csv(OUT_SCA, index=False)
n_sig = int(((spec_df['p']<0.05) & (spec_df['beta']>0)).sum())
n_sig_neg = int(((spec_df['p']<0.05) & (spec_df['beta']<0)).sum())
n_total = len(spec_df)
log(f"   Wrote {n_total} specs → {OUT_SCA}")
log(f"   Significant POSITIVE specs (p<.05, β>0): {n_sig} ({n_sig/n_total*100:.1f}%)")
log(f"   Significant NEGATIVE specs (p<.05, β<0): {n_sig_neg} ({n_sig_neg/n_total*100:.1f}%)")
log(f"   Median β (satlife DV): {spec_df[spec_df['dv']=='satlife']['beta'].median():+.4f}")
log(f"   Median β (srh DV):     {spec_df[spec_df['dv']=='srh']['beta'].median():+.4f}")
log(f"   Median β (cesd10 DV):  {spec_df[spec_df['dv']=='cesd10']['beta'].median():+.4f}")
# Type A specifically
tA_specs = spec_df[spec_df['treatment']=='type_A']
log(f"   Type A specs median β: {tA_specs['beta'].median():+.4f}  (n_specs={len(tA_specs)})")
log(f"   Type A specs positive-sig: {int(((tA_specs['p']<0.05) & (tA_specs['beta']>0)).sum())}  negative-sig: {int(((tA_specs['p']<0.05) & (tA_specs['beta']<0)).sum())}")

# ------------------------------------------------------------
# [9/10] DISCRIMINANT VALIDITY — Type B and Type C
# ------------------------------------------------------------
log("\n[9/10] DISCRIMINANT VALIDITY — Type B coerced + Type C addiction")
log("=" * 60)

disc_results = {}
# Type B prediction: P(satlife) should be LOWER (coerced) vs Type A baseline
for src_type in ['type_A', 'type_B', 'type_C']:
    sub = df[df[src_type]==1].dropna(subset=['satlife','cesd10','age','gender','edu','ln_income'])
    if len(sub) < 50:
        continue
    sat = float(sub['satlife'].mean())
    cesd = float(sub['cesd10'].mean())
    liver = float((sub['livere']==1).mean())
    n = len(sub)
    log(f"   {src_type:8s} n={n:>5}  mean(satlife)={sat:.3f}  mean(cesd10)={cesd:.2f}  P(liver)={liver:.4f}")
    disc_results[src_type] = dict(n=n, mean_satlife=sat, mean_cesd=cesd, p_liver=liver)

# Pairwise t-tests (Type A vs B, A vs C)
for pair in [('type_A','type_B'),('type_A','type_C'),('type_B','type_C')]:
    a_sub = df[df[pair[0]]==1]['satlife'].dropna()
    b_sub = df[df[pair[1]]==1]['satlife'].dropna()
    if len(a_sub)>20 and len(b_sub)>20:
        t, p = stats.ttest_ind(a_sub, b_sub, equal_var=False)
        log(f"   satlife {pair[0]} vs {pair[1]}: diff={a_sub.mean()-b_sub.mean():+.3f}  t={t:.2f}  p={p:.4g}")
        disc_results[f'{pair[0]}_vs_{pair[1]}_satlife'] = dict(diff=float(a_sub.mean()-b_sub.mean()), t=float(t), p=float(p))

# ------------------------------------------------------------
# [10/10] SAVE RESULTS JSON
# ------------------------------------------------------------
log("\n[10/10] SAVING RESULTS")
log("=" * 60)

def _clean(o):
    if isinstance(o, (np.floating, np.integer)):
        return float(o) if isinstance(o, np.floating) else int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (list, tuple)):
        return [_clean(x) for x in o]
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    return o

results = {
    'script': 'D_alcohol_sweet_trap.py',
    'generated_at': datetime.now().isoformat(),
    'data_sha256': actual_sha,
    'n_rows': int(len(df)),
    'n_unique_ID': int(df['ID'].nunique()),
    'waves': sorted([int(w) for w in df['wave'].dropna().unique()]),
    'section_2_descriptives': _clean(overall),
    'section_3_f2_diagnostic': _clean(f2_results),
    'section_3_type_counts': dict(
        type_A=tA, type_B=tB, type_C=tC, unclassified=tUnk,
        total_current_drinkers=int(len(cur))
    ),
    'section_4_sweet': _clean(sweet_results),
    'section_5_bitter': _clean(bitter_results),
    'section_6_rho_lockin': _clean(rho_results),
    'section_7_delta_st': _clean(delta_results),
    'section_8_speccurve_summary': dict(
        n_total=n_total, n_positive_sig=n_sig, n_negative_sig=n_sig_neg,
        median_beta_satlife=float(spec_df[spec_df['dv']=='satlife']['beta'].median()),
        median_beta_srh=float(spec_df[spec_df['dv']=='srh']['beta'].median()),
        median_beta_cesd=float(spec_df[spec_df['dv']=='cesd10']['beta'].median()),
    ),
    'section_9_discriminant': _clean(disc_results),
}

with open(OUT_JSON, 'w', encoding='utf-8') as fh:
    json.dump(results, fh, indent=2, ensure_ascii=False)
log(f"   Wrote {OUT_JSON}")
log(f"   Wrote {OUT_SCA}")
log("\nDONE.")
logfile.close()
