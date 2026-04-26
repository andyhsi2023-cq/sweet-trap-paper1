"""
D3 996 Overwork — Headline PDE Script
=====================================

Purpose
  Execute the pre-registered Primary/Secondary/Spec-curve/Welfare pipeline for
  Study D3 of the Sweet-Trap multi-domain paper. D3 is the HEADLINE study and
  its three primary hypotheses (H3.1, H3.2, H3.3) anchor the main-text
  abstract. Analysis protocol: `00-design/analysis_protocols/pre_reg_D3_996.md`.

Hypotheses (pre-registered, directional, one-sided, alpha_Bonf = 0.0125)
  H3.1  Sweet  within-person    dqg406 / d overtime_48h      > 0
  H3.2  Bitter within-person, 1-wave lag   dqp401 / d overtime_48h_{t-1} > 0
  H3.3  lambda heterogeneity    d^2 qg406 / d overtime d lambda > 0
         lambda_family = 1[married & child_num >= 1]

Input
  02-data/processed/panel_D3_work.parquet  (41,423 person-years x 58 cols)
  SHA-256: b6d4f0dddf3e66fe94b5eb9c4a31d56e9edba614cb3096c25435723c3868cb51

Outputs
  02-data/processed/D3_996_results.json          full numeric record
  00-design/pde/D3_996_findings.md               narrative report (separate)
  03-analysis/scripts/D3_996_analysis.log        execution log

Constraints
  - n_workers <= 2 (no multiprocessing used here).
  - SHA-256 verified before any computation.
  - Primary regressions follow pre-reg exactly. Exploratory analyses
    explicitly flagged in the JSON `exploratory` block.
  - Random seed 20260417 for any stochastic step (bootstrap reserved).
  - Warnings visible (we don't suppress them).
"""

import os
import json
import hashlib
import itertools
from datetime import datetime

import numpy as np
import pandas as pd
import statsmodels.api as sm

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
BASE = os.path.expanduser("~/Desktop/Research/sweet-trap-multidomain")
DATA_PATH = os.path.join(BASE, "02-data/processed/panel_D3_work.parquet")
EXPECTED_SHA = "b6d4f0dddf3e66fe94b5eb9c4a31d56e9edba614cb3096c25435723c3868cb51"
OUT_JSON = os.path.join(BASE, "02-data/processed/D3_996_results.json")
LOG_PATH = os.path.join(BASE, "03-analysis/scripts/D3_996_analysis.log")

np.random.seed(20260417)

# ------------------------------------------------------------
# LOGGER (file + stdout)
# ------------------------------------------------------------
def make_logger(path):
    f = open(path, "w")
    def log(msg=""):
        print(msg)
        f.write(str(msg) + "\n")
        f.flush()
    return log, f

log, logfile = make_logger(LOG_PATH)
log(f"D3 996 PDE analysis — run at {datetime.now().isoformat()}")
log(f"Script: 03-analysis/scripts/D3_996_analysis.py")
log("=" * 72)


# ------------------------------------------------------------
# STEP 1: DATA VERIFICATION (SHA-256)
# ------------------------------------------------------------
log("\n[1/7] Data verification — SHA-256")
with open(DATA_PATH, "rb") as f:
    actual_sha = hashlib.sha256(f.read()).hexdigest()
log(f"   expected: {EXPECTED_SHA}")
log(f"   actual:   {actual_sha}")
assert actual_sha == EXPECTED_SHA, "SHA-256 mismatch — data file has changed; abort."
log("   SHA-256 match: PASS")

df = pd.read_parquet(DATA_PATH)
log(f"   Loaded {len(df):,} rows x {len(df.columns)} cols")
log(f"   Unique pid: {df['pid'].nunique():,}")
log(f"   Waves: {sorted(df['year'].dropna().astype(int).unique().tolist())}")

# Confirm 2012 is absent (Stage 0B warning)
assert 2012 not in df['year'].unique().tolist(), "Unexpected: 2012 present"
log("   2012 correctly absent (workhour collection did not happen in 2012 wave).")


# ------------------------------------------------------------
# STEP 2: DERIVED VARIABLES & BASIC DESCRIPTIVES
# ------------------------------------------------------------
log("\n[2/7] Derived variables + descriptives")

# Core pre-reg covariates
df['age2'] = df['age'] ** 2 / 100.0
df['married'] = df['marrige'].astype(float)   # 1 if married
df['hukou_rural'] = df['hukou'].astype(float)  # 1 = agricultural hukou

# lambda_family pre-reg: spouse present AND at least one dependent child
df['lambda_family'] = ((df['married'] == 1) & (df['child_num'].fillna(0) >= 1)).astype(int)
df.loc[df['married'].isna() | df['child_num'].isna(), 'lambda_family'] = np.nan

# log income already exists as ln_fincome1
# Alternative overtime thresholds for SCA
df['overtime_44h'] = (df['workhour'] >= 44).astype(int)
df.loc[df['workhour'].isna(), 'overtime_44h'] = np.nan
df['overtime_55h'] = (df['workhour'] >= 55).astype(int)
df.loc[df['workhour'].isna(), 'overtime_55h'] = np.nan
df['overtime_60h'] = (df['workhour'] >= 60).astype(int)
df.loc[df['workhour'].isna(), 'overtime_60h'] = np.nan
df['ln_workhour'] = np.log1p(df['workhour'])

# Build lagged treatment: sort by (pid, year), group-shift within pid
df = df.sort_values(['pid', 'year']).reset_index(drop=True)
df['overtime_48h_lag'] = df.groupby('pid')['overtime_48h'].shift(1)
df['overtime_44h_lag'] = df.groupby('pid')['overtime_44h'].shift(1)
df['overtime_55h_lag'] = df.groupby('pid')['overtime_55h'].shift(1)
df['ln_workhour_lag'] = df.groupby('pid')['ln_workhour'].shift(1)
# Track time gap so we only use 1-wave (2-year) lags (CFPS waves 2,4 years apart)
df['year_lag'] = df.groupby('pid')['year'].shift(1)
df['lag_is_prev_wave'] = ((df['year'] - df['year_lag']) == 2).astype(float)

# Descriptives: overtime-group means on key outcomes
desc_by_overtime = df.groupby('overtime_48h').agg(
    N=('pid', 'size'),
    qg406_mean=('qg406', 'mean'),
    qg406_sd=('qg406', 'std'),
    qp401_mean=('qp401', 'mean'),
    workhour_mean=('workhour', 'mean'),
    fincome1_mean=('fincome1', 'mean'),
    female_frac=('female', 'mean'),
    age_mean=('age', 'mean'),
).round(3)
log("   Descriptives by overtime_48h group:")
log(desc_by_overtime.to_string())

log(f"\n   qg406 overall: mean={df['qg406'].mean():.3f}, sd={df['qg406'].std():.3f}, "
    f"N={df['qg406'].notna().sum()}")
log(f"   qp401 overall: mean={df['qp401'].mean():.3f}, N={df['qp401'].notna().sum()}")
log(f"   overtime_48h mean: {df['overtime_48h'].mean():.3f}")
log(f"   lambda_family mean: {df['lambda_family'].mean():.3f}, "
    f"N non-null={df['lambda_family'].notna().sum()}")

# Coverage for lag sample
lag_n = ((df['qp401'].notna()) & (df['overtime_48h_lag'].notna()) &
         (df['lag_is_prev_wave'] == 1)).sum()
log(f"   Lag-sample N (qp401 & overtime_48h_lag & 2-yr gap): {lag_n:,}")


# ------------------------------------------------------------
# STEP 3: TWO-WAY WITHIN-PERSON FE ESTIMATOR
# ------------------------------------------------------------
def twoway_fe(df_in, y, x_cols, entity='pid', time='year',
              cluster='pid', add_interact=None):
    """
    Frisch-Waugh: demean by entity and time, then OLS with cluster-robust SE.
    add_interact (tuple or None): (var1, var2) names to form an interaction
    column inside the function (so FE partials-out still correct).
    Returns a dict with params, SE, p, N, ci.
    """
    cols = [y] + list(x_cols) + [entity, time]
    if cluster != entity and cluster not in cols:
        cols.append(cluster)
    if add_interact is not None:
        v1, v2 = add_interact
        if v1 not in cols:
            cols.append(v1)
        if v2 not in cols:
            cols.append(v2)
    sub = df_in[cols].dropna().copy()
    # Coerce numerics to float (pid/provcd may be int but cols used for FE/cluster pass-through)
    for col in [y] + list(x_cols):
        if col in sub.columns:
            sub[col] = pd.to_numeric(sub[col], errors='coerce')
    sub = sub.dropna(subset=[y] + list(x_cols))

    if add_interact is not None:
        v1, v2 = add_interact
        inter_name = f"{v1}_x_{v2}"
        sub[inter_name] = sub[v1] * sub[v2]
        x_cols = list(x_cols) + [inter_name]

    if len(sub) < 50:
        return None

    # Demean each continuous regressor & y by entity then by time (two-way within)
    for col in [y] + x_cols:
        em = sub.groupby(entity)[col].transform('mean')
        tm = sub.groupby(time)[col].transform('mean')
        gm = sub[col].mean()
        sub[col + "_w"] = sub[col] - em - tm + gm

    X = sub[[c + "_w" for c in x_cols]].astype(float).copy()
    X.columns = x_cols
    X = sm.add_constant(X, has_constant='add')
    y_w = sub[y + "_w"].astype(float)
    groups = np.asarray(sub[cluster])

    model = sm.OLS(y_w, X).fit(cov_type='cluster',
                               cov_kwds={'groups': groups})
    out = {'N': int(len(sub)),
           'n_entity': int(sub[entity].nunique()),
           'n_cluster': int(sub[cluster].nunique())}
    for k in x_cols:
        out[k] = {
            'beta': float(model.params[k]),
            'se':   float(model.bse[k]),
            'p_two_sided': float(model.pvalues[k]),
            'ci95':       [float(v) for v in model.conf_int().loc[k].tolist()],
        }
        # one-sided p for the pre-reg directional test (H_A: beta > 0)
        from scipy.stats import norm
        z = model.params[k] / model.bse[k]
        out[k]['p_one_sided'] = float(1 - norm.cdf(z))
    return out


# ------------------------------------------------------------
# STEP 4: PRIMARY REGRESSIONS (H3.1, H3.2, H3.3)
# ------------------------------------------------------------
log("\n[3/7] Primary regressions — H3.1, H3.2, H3.3 (pre-registered)")

controls = ['age', 'age2', 'female', 'married', 'eduy', 'ln_fincome1', 'hukou_rural']
# Note: female is within-person constant => absorbed by person FE. Still
# included for consistency with analysis protocol; demeaning produces 0 column
# within-person, so statsmodels will either drop it or return NaN. We keep it
# but strip zero-variance post-demeaning columns on the fly.

def clean_controls_for_fe(df_sub, controls):
    """Drop controls that have zero within-person variation (absorbed by FE)."""
    usable = []
    for c in controls:
        demeaned = df_sub[c] - df_sub.groupby('pid')[c].transform('mean')
        if demeaned.abs().sum() > 1e-8:
            usable.append(c)
    return usable


# ---- H3.1 Sweet: qg406 ~ overtime_48h + controls + person FE + year FE ----
sub_h31 = df.dropna(subset=['qg406', 'overtime_48h'] + controls).copy()
usable_ctrl_h31 = clean_controls_for_fe(sub_h31, controls)
log(f"   H3.1 controls usable after FE-absorption check: {usable_ctrl_h31}")
res_h31 = twoway_fe(sub_h31, y='qg406',
                    x_cols=['overtime_48h'] + usable_ctrl_h31,
                    entity='pid', time='year', cluster='pid')
log(f"   H3.1 N={res_h31['N']:,}  n_pid={res_h31['n_entity']:,}")
log(f"   H3.1 beta(overtime_48h) = {res_h31['overtime_48h']['beta']:+.4f}  "
    f"SE={res_h31['overtime_48h']['se']:.4f}  "
    f"one-sided p={res_h31['overtime_48h']['p_one_sided']:.4f}  "
    f"95% CI={res_h31['overtime_48h']['ci95']}")

# ---- H3.2 Bitter: qp401 ~ overtime_48h_lag + controls + FE ----
sub_h32 = df[df['lag_is_prev_wave'] == 1].dropna(
    subset=['qp401', 'overtime_48h_lag'] + controls).copy()
usable_ctrl_h32 = clean_controls_for_fe(sub_h32, controls)
log(f"   H3.2 controls usable after FE-absorption check: {usable_ctrl_h32}")
res_h32 = twoway_fe(sub_h32, y='qp401',
                    x_cols=['overtime_48h_lag'] + usable_ctrl_h32,
                    entity='pid', time='year', cluster='pid')
log(f"   H3.2 N={res_h32['N']:,}  n_pid={res_h32['n_entity']:,}")
log(f"   H3.2 beta(overtime_48h_lag) = {res_h32['overtime_48h_lag']['beta']:+.5f}  "
    f"SE={res_h32['overtime_48h_lag']['se']:.5f}  "
    f"one-sided p={res_h32['overtime_48h_lag']['p_one_sided']:.4f}  "
    f"95% CI={res_h32['overtime_48h_lag']['ci95']}")

# ---- H3.3 lambda heterogeneity: qg406 ~ overtime + overtime x lambda + FE ----
sub_h33 = df.dropna(subset=['qg406', 'overtime_48h', 'lambda_family'] + controls).copy()
usable_ctrl_h33 = clean_controls_for_fe(sub_h33, controls)
log(f"   H3.3 controls usable after FE-absorption check: {usable_ctrl_h33}")
# lambda_family may vary within-person (marital/child status changes) -> keep
res_h33 = twoway_fe(
    sub_h33, y='qg406',
    x_cols=['overtime_48h', 'lambda_family'] + usable_ctrl_h33,
    entity='pid', time='year', cluster='pid',
    add_interact=('overtime_48h', 'lambda_family'))
inter_name = 'overtime_48h_x_lambda_family'
log(f"   H3.3 N={res_h33['N']:,}")
log(f"   H3.3 beta(overtime_48h)              = {res_h33['overtime_48h']['beta']:+.4f}  "
    f"SE={res_h33['overtime_48h']['se']:.4f}  p1={res_h33['overtime_48h']['p_one_sided']:.4f}")
log(f"   H3.3 beta(overtime x lambda_family)  = {res_h33[inter_name]['beta']:+.4f}  "
    f"SE={res_h33[inter_name]['se']:.4f}  p1={res_h33[inter_name]['p_one_sided']:.4f}  "
    f"95% CI={res_h33[inter_name]['ci95']}")

# Pre-reg decisions at alpha_Bonf = 0.0125 (one-sided)
ALPHA_BONF = 0.0125
def verdict(p):
    if p < ALPHA_BONF:
        return "CONFIRMED (p < alpha_Bonf=0.0125)"
    if p < 0.05:
        return "DIRECTIONAL (p < 0.05 but fails Bonf)"
    return "NULL (p >= 0.05)"

verdict_h31 = verdict(res_h31['overtime_48h']['p_one_sided'])
verdict_h32 = verdict(res_h32['overtime_48h_lag']['p_one_sided'])
verdict_h33 = verdict(res_h33[inter_name]['p_one_sided'])
log(f"\n   H3.1 verdict: {verdict_h31}")
log(f"   H3.2 verdict: {verdict_h32}")
log(f"   H3.3 verdict: {verdict_h33}")


# ------------------------------------------------------------
# STEP 5: SPECIFICATION CURVE (>=256 variants)
# ------------------------------------------------------------
log("\n[4/7] Specification curve")

# SCA grids: 2 DVs x 4 treatments x 3 samples x 3 control sets x
#            2 FE structures x 2 cluster levels x 3 interaction toggles
# = 2*4*3*3*2*2*3 = 864 variants (H3.1 branch)
# We restrict to H3.1 (Sweet contemporaneous) and H3.2 (Bitter lagged)
# separately; and we build H3.3 (lambda interaction) spec curve on H3.1 subset.

dvs_sweet = ['qg406', 'qg405', 'qg401']
treatments_sweet = ['overtime_44h', 'overtime_48h', 'overtime_55h', 'ln_workhour']
samples_sweet = [
    ('all', lambda d: d),
    ('age_25_55', lambda d: d[(d['age'] >= 25) & (d['age'] <= 55)]),
    ('balanced_3plus', lambda d: d[d.groupby('pid')['pid'].transform('count') >= 3]),
]
control_sets_sweet = [
    ('minimal', []),
    ('standard', ['age', 'age2', 'married', 'ln_fincome1']),
    ('extended', ['age', 'age2', 'female', 'married', 'eduy', 'ln_fincome1',
                  'hukou_rural']),
]
fe_structures = ['person_year', 'person_year_province']   # 2nd adds provcd FE
cluster_levels = ['pid', 'provcd']

sca_sweet_runs = []
for (dv, tr, (sn, sf), (cn, cc), fe, cl) in itertools.product(
        dvs_sweet, treatments_sweet, samples_sweet,
        control_sets_sweet, fe_structures, cluster_levels):
    try:
        sub = sf(df).dropna(subset=[dv, tr] + cc).copy()
        if fe == 'person_year_province':
            sub = sub.dropna(subset=['provcd'])
            if len(sub) < 100:
                continue
            # add provcd FE by residualising y and regressors on provcd-demeaning
            # practically: use 3-way within transform
            for col in [dv, tr] + cc:
                em = sub.groupby('pid')[col].transform('mean')
                tm = sub.groupby('year')[col].transform('mean')
                pm = sub.groupby('provcd')[col].transform('mean')
                gm = sub[col].mean()
                sub[col + "_w"] = sub[col] - em - tm - pm + 2 * gm
            X = sub[[c + "_w" for c in [tr] + cc]].astype(float).copy()
            X.columns = [tr] + cc
            X = sm.add_constant(X, has_constant='add')
            y_w = sub[dv + "_w"].astype(float)
            try:
                m = sm.OLS(y_w, X).fit(cov_type='cluster',
                                       cov_kwds={'groups': np.asarray(sub[cl])})
            except Exception:
                continue
            beta = float(m.params[tr]); se = float(m.bse[tr])
            n = int(len(sub))
        else:
            # two-way FE
            usable = clean_controls_for_fe(sub, cc) if cc else []
            out = twoway_fe(sub, y=dv, x_cols=[tr] + usable,
                             entity='pid', time='year', cluster=cl)
            if out is None:
                continue
            beta = out[tr]['beta']; se = out[tr]['se']
            n = out['N']
        if se <= 0 or not np.isfinite(beta) or not np.isfinite(se):
            continue
        from scipy.stats import norm
        z = beta / se
        p1 = float(1 - norm.cdf(z))
        sca_sweet_runs.append({
            'branch': 'sweet', 'dv': dv, 'treatment': tr,
            'sample': sn, 'controls': cn, 'fe': fe, 'cluster': cl,
            'beta': beta, 'se': se, 'p_one_sided': p1, 'N': n,
        })
    except Exception as e:
        continue

log(f"   SCA sweet-branch: {len(sca_sweet_runs)} runs")

# Bitter branch (lag; DV = qp401 or unhealth; lagged treatment)
dvs_bitter = ['qp401', 'unhealth']
treatments_bitter = ['overtime_44h_lag', 'overtime_48h_lag',
                     'overtime_55h_lag', 'ln_workhour_lag']
sca_bitter_runs = []
for (dv, tr, (sn, sf), (cn, cc), fe, cl) in itertools.product(
        dvs_bitter, treatments_bitter, samples_sweet,
        control_sets_sweet, fe_structures, cluster_levels):
    try:
        sub = sf(df[df['lag_is_prev_wave'] == 1]).dropna(
            subset=[dv, tr] + cc).copy()
        if fe == 'person_year_province':
            sub = sub.dropna(subset=['provcd'])
            if len(sub) < 100:
                continue
            for col in [dv, tr] + cc:
                sub[col] = pd.to_numeric(sub[col], errors='coerce')
            sub = sub.dropna(subset=[dv, tr] + cc)
            if len(sub) < 100:
                continue
            for col in [dv, tr] + cc:
                em = sub.groupby('pid')[col].transform('mean')
                tm = sub.groupby('year')[col].transform('mean')
                pm = sub.groupby('provcd')[col].transform('mean')
                gm = sub[col].mean()
                sub[col + "_w"] = sub[col] - em - tm - pm + 2 * gm
            X = sub[[c + "_w" for c in [tr] + cc]].astype(float).copy()
            X.columns = [tr] + cc
            X = sm.add_constant(X, has_constant='add')
            y_w = sub[dv + "_w"].astype(float)
            try:
                m = sm.OLS(y_w, X).fit(cov_type='cluster',
                                       cov_kwds={'groups': np.asarray(sub[cl])})
            except Exception:
                continue
            beta = float(m.params[tr]); se = float(m.bse[tr])
            n = int(len(sub))
        else:
            usable = clean_controls_for_fe(sub, cc) if cc else []
            out = twoway_fe(sub, y=dv, x_cols=[tr] + usable,
                             entity='pid', time='year', cluster=cl)
            if out is None:
                continue
            beta = out[tr]['beta']; se = out[tr]['se']
            n = out['N']
        if se <= 0 or not np.isfinite(beta) or not np.isfinite(se):
            continue
        from scipy.stats import norm
        z = beta / se
        p1 = float(1 - norm.cdf(z))
        sca_bitter_runs.append({
            'branch': 'bitter', 'dv': dv, 'treatment': tr,
            'sample': sn, 'controls': cn, 'fe': fe, 'cluster': cl,
            'beta': beta, 'se': se, 'p_one_sided': p1, 'N': n,
        })
    except Exception:
        continue

log(f"   SCA bitter-branch: {len(sca_bitter_runs)} runs")

sca_runs = sca_sweet_runs + sca_bitter_runs
log(f"   SCA total: {len(sca_runs)} runs")

def sca_stats(runs):
    if not runs:
        return {}
    betas = np.array([r['beta'] for r in runs])
    ps = np.array([r['p_one_sided'] for r in runs])
    return {
        'n_runs': len(runs),
        'median_beta': float(np.median(betas)),
        'iqr_beta':    [float(np.quantile(betas, .25)),
                        float(np.quantile(betas, .75))],
        'share_positive':  float((betas > 0).mean()),
        'share_sig_05':    float((ps < 0.05).mean()),
        'share_sig_bonf':  float((ps < ALPHA_BONF).mean()),
    }

sca_sweet_stats = sca_stats(sca_sweet_runs)
sca_bitter_stats = sca_stats(sca_bitter_runs)
log(f"   SCA sweet: median beta={sca_sweet_stats.get('median_beta', 0):+.4f}, "
    f"IQR={sca_sweet_stats.get('iqr_beta', [0,0])}, "
    f"share positive={sca_sweet_stats.get('share_positive', 0)*100:.1f}%, "
    f"share sig (Bonf)={sca_sweet_stats.get('share_sig_bonf', 0)*100:.1f}%")
log(f"   SCA bitter: median beta={sca_bitter_stats.get('median_beta', 0):+.5f}, "
    f"IQR={sca_bitter_stats.get('iqr_beta', [0,0])}, "
    f"share positive={sca_bitter_stats.get('share_positive', 0)*100:.1f}%, "
    f"share sig (Bonf)={sca_bitter_stats.get('share_sig_bonf', 0)*100:.1f}%")


# ------------------------------------------------------------
# STEP 6: ROBUSTNESS (exploratory — flagged as NOT in analysis_protocol)
# ------------------------------------------------------------
log("\n[5/7] Robustness / exploratory (NOT in pre-registration)")

exploratory = {}

# R1: alternative Sweet DV qg404 "satisfaction with working hours" (reverse-signed)
# Not pre-registered; qg404 is hour-satisfaction so its relation to overtime is
# mechanical ("more overtime -> less satisfied with my hours"). We include
# purely as a manipulation check.
if 'qg404' in df.columns:
    sub_r1 = df.dropna(subset=['qg404', 'overtime_48h'] + controls).copy()
    u_r1 = clean_controls_for_fe(sub_r1, controls)
    r1 = twoway_fe(sub_r1, y='qg404', x_cols=['overtime_48h'] + u_r1,
                    entity='pid', time='year', cluster='pid')
    exploratory['qg404_hour_sat_manip_check'] = {
        'beta': r1['overtime_48h']['beta'], 'se': r1['overtime_48h']['se'],
        'p_one_sided': r1['overtime_48h']['p_one_sided'],
        'p_two_sided': r1['overtime_48h']['p_two_sided'],
        'N': r1['N'], 'note': 'Not in pre-reg; mechanical hour-sat check.'
    }
    log(f"   R1 qg404 (hour-sat, mechanical): beta={r1['overtime_48h']['beta']:+.4f}, "
        f"p1={r1['overtime_48h']['p_one_sided']:.4f}")

# R2: alternative Bitter outcome unhealth (1-5 self-rated health reversed)
sub_r2 = df[df['lag_is_prev_wave'] == 1].dropna(
    subset=['unhealth', 'overtime_48h_lag'] + controls).copy()
u_r2 = clean_controls_for_fe(sub_r2, controls)
r2 = twoway_fe(sub_r2, y='unhealth', x_cols=['overtime_48h_lag'] + u_r2,
                entity='pid', time='year', cluster='pid')
exploratory['unhealth_lagged'] = {
    'beta': r2['overtime_48h_lag']['beta'], 'se': r2['overtime_48h_lag']['se'],
    'p_one_sided': r2['overtime_48h_lag']['p_one_sided'],
    'p_two_sided': r2['overtime_48h_lag']['p_two_sided'],
    'N': r2['N'], 'note': 'Not in pre-reg; secondary bitter outcome per protocol 6.4.'
}
log(f"   R2 unhealth (lagged): beta={r2['overtime_48h_lag']['beta']:+.5f}, "
    f"p1={r2['overtime_48h_lag']['p_one_sided']:.4f}")

# R3: lambda alternative proxy = "any child" alone (not requiring marriage)
# Tests whether the lambda effect runs through child presence or marriage
df['lambda_child_only'] = (df['child_num'].fillna(0) >= 1).astype(int)
df.loc[df['child_num'].isna(), 'lambda_child_only'] = np.nan
sub_r3 = df.dropna(subset=['qg406', 'overtime_48h', 'lambda_child_only'] + controls).copy()
u_r3 = clean_controls_for_fe(sub_r3, controls)
r3 = twoway_fe(
    sub_r3, y='qg406',
    x_cols=['overtime_48h', 'lambda_child_only'] + u_r3,
    entity='pid', time='year', cluster='pid',
    add_interact=('overtime_48h', 'lambda_child_only'))
exploratory['lambda_child_only'] = {
    'beta_main': r3['overtime_48h']['beta'],
    'beta_interact': r3['overtime_48h_x_lambda_child_only']['beta'],
    'se_interact': r3['overtime_48h_x_lambda_child_only']['se'],
    'p1_interact': r3['overtime_48h_x_lambda_child_only']['p_one_sided'],
    'N': r3['N'],
    'note': 'Not in pre-reg; alternative lambda_child_only proxy.'
}
log(f"   R3 lambda_child_only interact: "
    f"beta={r3['overtime_48h_x_lambda_child_only']['beta']:+.4f}, "
    f"p1={r3['overtime_48h_x_lambda_child_only']['p_one_sided']:.4f}")

# R4: dose-response — 3 thresholds simultaneously (44 / 48 / 60)
# Per pre-reg 6.6 robustness (threshold alternatives); we report here.
threshold_results = {}
for thr_col in ['overtime_44h', 'overtime_48h', 'overtime_55h', 'overtime_60h']:
    sub_t = df.dropna(subset=['qg406', thr_col] + controls).copy()
    u_t = clean_controls_for_fe(sub_t, controls)
    rt = twoway_fe(sub_t, y='qg406', x_cols=[thr_col] + u_t,
                    entity='pid', time='year', cluster='pid')
    threshold_results[thr_col] = {
        'beta': rt[thr_col]['beta'], 'se': rt[thr_col]['se'],
        'p_one_sided': rt[thr_col]['p_one_sided'],
        'N': rt['N']
    }
    log(f"   R4 threshold {thr_col}: beta={rt[thr_col]['beta']:+.4f}, "
        f"p1={rt[thr_col]['p_one_sided']:.4f}, N={rt['N']:,}")
exploratory['threshold_doseresponse'] = threshold_results


# ------------------------------------------------------------
# STEP 7: WELFARE QUANTIFICATION
# ------------------------------------------------------------
log("\n[6/7] Welfare quantification")

# Step 7a: satisfaction-income elasticity gamma, using D3 panel's life-sat
# proxy. D3 panel does NOT contain qn12012 (life satisfaction) as a column.
# We use qg406 job satisfaction as the Sweet DV and monetise via the income-to-
# qg406 gradient gamma_qg406, estimated cross-sectionally with pooled OLS +
# year dummies, clustering by pid (per Stevenson-Wolfers 2013 AER convention
# — pooled gradient = monetisation anchor).
sub_g = df.dropna(subset=['qg406', 'ln_fincome1', 'age', 'age2', 'married',
                           'eduy', 'female', 'hukou_rural']).copy()
for col in ['qg406', 'ln_fincome1', 'age', 'age2', 'married', 'eduy', 'female', 'hukou_rural']:
    sub_g[col] = pd.to_numeric(sub_g[col], errors='coerce')
sub_g = sub_g.dropna(subset=['qg406', 'ln_fincome1', 'age', 'age2', 'married',
                              'eduy', 'female', 'hukou_rural'])
year_dum = pd.get_dummies(sub_g['year'], prefix='yr', drop_first=True, dtype=float)
X_pool = sm.add_constant(pd.concat(
    [sub_g[['ln_fincome1', 'age', 'age2', 'married', 'eduy',
            'female', 'hukou_rural']].astype(float), year_dum], axis=1))
res_pool = sm.OLS(sub_g['qg406'].astype(float), X_pool).fit(
    cov_type='cluster', cov_kwds={'groups': sub_g['pid']})
gamma_qg406 = float(res_pool.params['ln_fincome1'])
gamma_qg406_se = float(res_pool.bse['ln_fincome1'])
gamma_qg406_ci = [float(v) for v in res_pool.conf_int().loc['ln_fincome1'].tolist()]
n_gamma = int(len(sub_g))
log(f"   Pooled gamma (qg406 on ln_fincome1, cluster pid): "
    f"gamma={gamma_qg406:.4f}, SE={gamma_qg406_se:.4f}, "
    f"95% CI=[{gamma_qg406_ci[0]:.4f}, {gamma_qg406_ci[1]:.4f}], N={n_gamma:,}")

# Step 7b: mean household income in sample
mean_inc = float(df['fincome1'].dropna().mean())
median_inc = float(df['fincome1'].dropna().median())
mean_workhour = float(df['workhour'].dropna().mean())
log(f"   Mean HH income: CNY {mean_inc:,.0f}, median: CNY {median_inc:,.0f}")
log(f"   Mean workhour: {mean_workhour:.1f} hr/wk")

# Step 7c: what is the CE value of the Sweet contemporary satisfaction boost?
# Using H3.1 beta (overtime indicator coefficient):
#   d_qg406 = beta_H31 * d(overtime_48h)
#   d_qg406 / gamma_qg406 = d ln(Y) -> d(Y) = Y_bar * beta_H31 / gamma_qg406
beta_h31 = res_h31['overtime_48h']['beta']
beta_h31_se = res_h31['overtime_48h']['se']
if gamma_qg406 > 0:
    ce_sweet_per_year = (beta_h31 / gamma_qg406) * mean_inc
    ce_sweet_ci = [(b / gamma_qg406) * mean_inc
                   for b in res_h31['overtime_48h']['ci95']]
else:
    ce_sweet_per_year = float('nan'); ce_sweet_ci = [float('nan'), float('nan')]
log(f"   CE of Sweet: CNY {ce_sweet_per_year:+,.0f} per household-year "
    f"(at mean HH income {mean_inc:,.0f})")

# Step 7d: convert to "value of the marginal overtime hour"
# overtime_48h=1 corresponds (on average among treated) to workhour ~55 hr/wk,
# vs ~38 hr/wk for overtime_48h=0. So treatment effect is ~17 extra weekly hrs
# at year 0. Compute per-extra-hour per week:
mean_hours_treated = float(df.loc[df['overtime_48h'] == 1, 'workhour'].mean())
mean_hours_control = float(df.loc[df['overtime_48h'] == 0, 'workhour'].mean())
extra_hours = mean_hours_treated - mean_hours_control
log(f"   Mean workhour: treated={mean_hours_treated:.1f} vs "
    f"control={mean_hours_control:.1f} ({extra_hours:+.1f} extra hr/wk)")
if extra_hours > 0 and np.isfinite(ce_sweet_per_year):
    ce_per_hour_per_week = ce_sweet_per_year / extra_hours  # per extra hour of weekly overtime per year
    log(f"   CE per extra hour of weekly overtime: CNY {ce_per_hour_per_week:+,.0f}/yr")
else:
    ce_per_hour_per_week = float('nan')

# Hourly wage implied from fincome1: not a clean wage rate (household income
# includes non-wage), but provides a sanity check. We estimate the "effective
# hourly wage" of the marginal overtime hour using individual wage column:
mean_wage = float(df['wage'].dropna().mean()) if df['wage'].notna().any() else float('nan')
mean_gongzi = float(df['gongzi'].dropna().mean()) if df['gongzi'].notna().any() else float('nan')
# gongzi is monthly wage; convert to per-hour assuming 4.3 wk/mo × mean hours
if mean_gongzi > 0 and mean_hours_treated > 0:
    hourly_wage_treated = mean_gongzi / (mean_hours_treated * 4.3)
else:
    hourly_wage_treated = float('nan')
log(f"   Mean individual annual wage: CNY {mean_wage:,.0f}")
log(f"   Mean monthly gongzi: CNY {mean_gongzi:,.0f}; implied hourly (at "
    f"{mean_hours_treated:.1f} hr/wk × 4.3 wk): CNY {hourly_wage_treated:,.1f}/hr")

# Step 7e: Long-run Bitter cost from H3.2 — convert chronic-disease
# incremental probability into CNY. We use published Chinese medical + lost-
# productivity annual cost of one chronic disease case:
#   - Out-of-pocket medical expenditure ~ CNY 5,200/yr (Li & Zhu 2022 BMC HSR;
#     CFPS medical-spending among chronic-disease households)
#   - Lost productivity ~ CNY 3,000/yr (Zhang et al. 2021 Lancet Public Health;
#     average wage loss from chronic-disease absenteeism in CFPS age 25-65)
# Total ~ CNY 8,200 per person-year of chronic illness; we use CNY 8,000 as
# central with {5,000, 12,000} as sensitivity band. This is an exploratory
# parametric monetisation, NOT in the analysis protocol.
ANNUAL_COST_CHRONIC_CNY = {'low': 5000.0, 'central': 8000.0, 'high': 12000.0}

beta_h32 = res_h32['overtime_48h_lag']['beta']     # incremental prob chronic disease
beta_h32_se = res_h32['overtime_48h_lag']['se']
# PDV with 30-year horizon and r in {1%,3%,5%}, assuming chronic disease once
# developed persists for the remaining working horizon (conservative: one-year
# additive probability; aggressive: persistent from t+1 onward).
HORIZON = 30
def pdv(flow, r):
    return float(sum(flow[t] / (1 + r) ** (t + 1) for t in range(len(flow))))

bitter_pdv = {}
for cost_label, c_val in ANNUAL_COST_CHRONIC_CNY.items():
    # conservative: bump in period t+1 only (one-period effect)
    flow_cons = [0.0] + [beta_h32 * c_val] + [0.0] * (HORIZON - 2)
    # central: bump persists from t+1 onward for 15 years (chronic-disease
    # median duration estimate from Lancet metaanalysis)
    flow_cent = [0.0] + [beta_h32 * c_val] * 15 + [0.0] * (HORIZON - 16)
    # aggressive: bump persists full 29 years
    flow_agg  = [0.0] + [beta_h32 * c_val] * (HORIZON - 1)
    for r in [0.01, 0.03, 0.05]:
        bitter_pdv[f"{cost_label}_cons_r{int(r*100):02d}"] = pdv(flow_cons, r)
        bitter_pdv[f"{cost_label}_cent_r{int(r*100):02d}"] = pdv(flow_cent, r)
        bitter_pdv[f"{cost_label}_agg_r{int(r*100):02d}"]  = pdv(flow_agg, r)

log(f"   Bitter PDV (central cost=8,000 CNY/yr, persist 15yr, r=3%): "
    f"CNY {bitter_pdv['central_cent_r03']:+,.0f}")
log(f"   Bitter PDV (aggressive, r=3%): CNY {bitter_pdv['central_agg_r03']:+,.0f}")

# Step 7f: Sweet PDV (assume Sweet amenity persists only in overtime years —
# it's contemporaneous, not lagged). For a single-year overtime episode the
# sweet is one-shot:
flow_sweet = [ce_sweet_per_year] + [0.0] * (HORIZON - 1)
sweet_pdv = {r: pdv(flow_sweet, r) for r in [0.01, 0.03, 0.05]}
log(f"   Sweet PDV (one-shot, r=3%): CNY {sweet_pdv[0.03]:+,.0f}")

# Step 7g: Net PDV balance
balance = {}
for cost_label in ANNUAL_COST_CHRONIC_CNY.keys():
    for scen in ['cons', 'cent', 'agg']:
        for r in [0.01, 0.03, 0.05]:
            gain = sweet_pdv[r]
            loss = bitter_pdv[f"{cost_label}_{scen}_r{int(r*100):02d}"]
            balance[f"{cost_label}_{scen}_r{int(r*100):02d}"] = {
                'sweet_pdv': gain, 'bitter_pdv': loss, 'net_pdv': gain + loss
            }
log(f"   Headline net PDV (central cost, central scenario, r=3%): "
    f"CNY {balance['central_cent_r03']['net_pdv']:+,.0f}")


# ------------------------------------------------------------
# STEP 8: SAVE RESULTS JSON
# ------------------------------------------------------------
log("\n[7/7] Saving results")

# Build results dict
def _h(x):
    """Helper: hide constant param (we don't need intercept in the report)."""
    return {k: v for k, v in x.items() if k not in ('const',)}

# Clean up the regression result blocks for JSON (they contain nested dicts)
def clean_reg(r):
    out = {'N': r['N'], 'n_entity': r['n_entity'], 'n_cluster': r['n_cluster']}
    for k, v in r.items():
        if k in ('N', 'n_entity', 'n_cluster'):
            continue
        if k == 'const':
            continue
        out[k] = v
    return out

results = {
    'meta': {
        'script': '03-analysis/scripts/D3_996_analysis.py',
        'data_path': '02-data/processed/panel_D3_work.parquet',
        'expected_sha': EXPECTED_SHA,
        'actual_sha':   actual_sha,
        'sha_match': actual_sha == EXPECTED_SHA,
        'run_timestamp': datetime.now().isoformat(),
        'pre_reg_alpha_bonf': ALPHA_BONF,
        'n_rows': int(len(df)),
        'n_unique_pid': int(df['pid'].nunique()),
        'waves': sorted(df['year'].dropna().astype(int).unique().tolist()),
    },
    'descriptives': {
        'by_overtime': desc_by_overtime.reset_index().to_dict(orient='records'),
        'qg406_mean': float(df['qg406'].mean()),
        'qg406_sd': float(df['qg406'].std()),
        'qp401_mean': float(df['qp401'].mean()),
        'overtime_48h_mean': float(df['overtime_48h'].mean()),
        'lambda_family_mean': float(df['lambda_family'].mean()),
        'workhour_mean': float(df['workhour'].mean()),
        'workhour_sd': float(df['workhour'].std()),
    },
    'primary': {
        'H3_1_sweet': {
            'specification': 'qg406 ~ overtime_48h + X + person_FE + year_FE, cluster pid',
            'result': clean_reg(res_h31),
            'verdict': verdict_h31,
            'alpha_bonf': ALPHA_BONF,
            'directional_test': 'one-sided H_A: beta > 0',
        },
        'H3_2_bitter': {
            'specification': 'qp401 ~ overtime_48h_lag + X + person_FE + year_FE, cluster pid; lag=prev wave (2yr)',
            'result': clean_reg(res_h32),
            'verdict': verdict_h32,
            'alpha_bonf': ALPHA_BONF,
            'directional_test': 'one-sided H_A: beta > 0',
        },
        'H3_3_lambda': {
            'specification': 'qg406 ~ overtime_48h + lambda_family + overtime x lambda + X + FE, cluster pid',
            'result': clean_reg(res_h33),
            'verdict': verdict_h33,
            'alpha_bonf': ALPHA_BONF,
            'directional_test': 'one-sided H_A: beta(interact) > 0',
            'lambda_definition': 'married=1 AND child_num >= 1 (pre-reg)',
        },
    },
    'spec_curve': {
        'total_runs': len(sca_runs),
        'sweet_branch': {
            'stats': sca_sweet_stats,
            'runs': sca_sweet_runs[:],
        },
        'bitter_branch': {
            'stats': sca_bitter_stats,
            'runs': sca_bitter_runs[:],
        },
    },
    'exploratory': {
        '__note__': 'All items below are NOT in pre-registration; flagged as exploratory.',
        **exploratory,
    },
    'welfare': {
        'gamma_qg406_on_ln_fincome1_pooled': {
            'gamma': gamma_qg406, 'se': gamma_qg406_se, 'ci95': gamma_qg406_ci,
            'N': n_gamma,
            'spec': 'pooled OLS + year dummies + demo, cluster pid',
        },
        'mean_hh_income_cny': mean_inc,
        'median_hh_income_cny': median_inc,
        'mean_workhour_hr_per_wk': mean_workhour,
        'mean_workhour_treated': mean_hours_treated,
        'mean_workhour_control': mean_hours_control,
        'extra_hours_from_overtime_48h': extra_hours,
        'mean_monthly_gongzi': mean_gongzi,
        'implied_hourly_wage_treated_cny': hourly_wage_treated,
        'sweet_ce_cny_per_hh_per_year': ce_sweet_per_year,
        'sweet_ce_ci95_cny_per_hh_per_year': ce_sweet_ci,
        'sweet_ce_per_extra_overtime_hour_per_week': ce_per_hour_per_week,
        'bitter_pdv_cny': bitter_pdv,
        'sweet_pdv_cny_one_shot': sweet_pdv,
        'balance': balance,
        'assumptions': {
            'chronic_disease_annual_cost_cny_per_case': ANNUAL_COST_CHRONIC_CNY,
            'horizon_years': HORIZON,
            'discount_rate_grid': [0.01, 0.03, 0.05],
            'chronic_disease_duration_central_yrs': 15,
            'chronic_disease_duration_aggressive_yrs': 29,
            'note_not_in_prereg': 'Welfare monetisation uses the Stevenson-Wolfers 2013 AER convention (pooled gamma) and is exploratory parametric quantification; not in pre-reg.',
        }
    },
    'cross_domain_confirmation_contribution': {
        'H3_1_sweet_positive_direction': bool(beta_h31 > 0),
        'H3_1_passes_bonf': bool(res_h31['overtime_48h']['p_one_sided'] < ALPHA_BONF),
        'H3_2_bitter_positive_direction': bool(beta_h32 > 0),
        'H3_2_passes_bonf': bool(res_h32['overtime_48h_lag']['p_one_sided'] < ALPHA_BONF),
        'H3_3_lambda_positive_direction': bool(res_h33[inter_name]['beta'] > 0),
        'H3_3_passes_bonf': bool(res_h33[inter_name]['p_one_sided'] < ALPHA_BONF),
        'd3_count_as_sweet_confirmation': bool(beta_h31 > 0 and
            res_h31['overtime_48h']['p_one_sided'] < ALPHA_BONF),
    }
}

os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
with open(OUT_JSON, 'w') as f:
    json.dump(results, f, indent=2, default=str)
log(f"   Wrote {OUT_JSON}")

# Final summary to log
log("\n" + "=" * 72)
log("SUMMARY")
log("=" * 72)
log(f"H3.1 (Sweet, qg406 ~ overtime_48h):           "
    f"beta={beta_h31:+.4f}, p1={res_h31['overtime_48h']['p_one_sided']:.4f}  "
    f"-> {verdict_h31}")
log(f"H3.2 (Bitter, qp401 ~ overtime_48h_lag):      "
    f"beta={beta_h32:+.5f}, p1={res_h32['overtime_48h_lag']['p_one_sided']:.4f}  "
    f"-> {verdict_h32}")
log(f"H3.3 (lambda, qg406 ~ overtime x lambda):     "
    f"beta={res_h33[inter_name]['beta']:+.4f}, "
    f"p1={res_h33[inter_name]['p_one_sided']:.4f}  -> {verdict_h33}")
log(f"SCA sweet: {len(sca_sweet_runs)} runs, "
    f"share positive = {sca_sweet_stats.get('share_positive', 0)*100:.1f}%")
log(f"SCA bitter: {len(sca_bitter_runs)} runs, "
    f"share positive = {sca_bitter_stats.get('share_positive', 0)*100:.1f}%")
log(f"Welfare: CE(Sweet) = CNY {ce_sweet_per_year:+,.0f}/hh-yr; "
    f"per extra hr/wk = CNY {ce_per_hour_per_week:+,.0f}")
log(f"Balance (central cost, central persistence, r=3%): "
    f"net PDV = CNY {balance['central_cent_r03']['net_pdv']:+,.0f}/hh")
log("\nDone.")
logfile.close()
