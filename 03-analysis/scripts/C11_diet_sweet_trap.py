"""
C11 High-Sugar/High-Fat Diet — Sweet Trap Focal #2 PDE
======================================================

Purpose
  Execute the pre-registered Primary / Secondary / Spec-curve / Welfare /
  CHARLS cross-validation pipeline for Study C11 of the Sweet-Trap
  cross-species manuscript. After C4 (bride-price) demotion, C11 is the
  second human focal (C2 鸡娃 runs in parallel).

Sweet Trap mapping
  C11 is the cleanest mammalian homologue of A4 (Drosophila sugar).
  Route A (ancestral mismatch): sugar/fat scarce in paleo environment →
  TAS1R2/TAS1R3 sweet-receptor reward calibrated for scarcity → modern
  industrial over-supply → reward decoupled from fitness.

  Layer A pooled Δ_ST = +0.72 [+0.60, +0.83] (8 animal cases).
  Drosophila A4 Δ_ST = +0.71. Human C11 predicted in +0.40..+0.65 band.

Hypotheses (pre-registered pre_reg_D5_diet.md, α_Bonf = 0.0125)
  H5.1 Bitter (1-wave lag): ∂ qp401 / ∂ food_share_{t-1} > 0
  H5.2 Sweet contemporaneous:  ∂ qn12012 / ∂ Δ food_share_t > 0
  H5.3 λ via health literacy: ∂² qn12012 / ∂ Δ food_share ∂ low_edu > 0

Extensions for cross-species paper (clearly labelled exploratory)
  E1 Bitter biomarker cross-validation via CHARLS (HbA1c, BP, BMI, diabetes)
  E2 Δ_ST cohort decomposition (ancestral 2010-2012 vs current 2018-2022)
  E3 BMI change (1-wave lag) as objective bitter DV within CFPS
  E4 Processed / outside-home food proxy — ln_food as intensity (continuous)
  E5 4-primitive (θ, λ, β, ρ) empirical signature tests

Input
  CFPS D5 panel:  02-data/processed/panel_D5_diet.parquet
                  SHA-256 lock: 371ddcaacedb46336225772abc8d1116d4ddb0e9c12bc0f1203d5ad16c4e8a2d
  CHARLS clean:   /Volumes/P1/.../CHARLS_中老年_2011-2020/.../CHARLS.csv
                  (5 waves 2011/2013/2015/2018/2020 — biomarker waves 1 & 3)

Outputs
  02-data/processed/C11_results.json        full numeric record
  02-data/processed/C11_speccurve.csv       specification-curve rows
  00-design/pde/C11_diet_findings.md        narrative PDE report (separate)
  03-analysis/scripts/C11_diet_sweet_trap.log  execution log

Constraints
  - n_workers ≤ 2 (no multiprocessing used).
  - D5 panel SHA-256 verified (panel is locked; NOT modified).
  - CHARLS read via duckdb/pandas chunked; not modified in-place.
  - Primary regressions follow pre-reg verbatim; exploratory clearly tagged.
  - Random seed 20260417 for bootstrap.
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
# PATHS & CONSTANTS
# ------------------------------------------------------------
BASE = os.path.expanduser("~/Desktop/Research/sweet-trap-multidomain")
DATA_PATH = os.path.join(BASE, "02-data/processed/panel_D5_diet.parquet")
EXPECTED_SHA = "371ddcaacedb46336225772abc8d1116d4ddb0e9c12bc0f1203d5ad16c4e8a2d"
OUT_JSON = os.path.join(BASE, "02-data/processed/C11_results.json")
OUT_SCA = os.path.join(BASE, "02-data/processed/C11_speccurve.csv")
LOG_PATH = os.path.join(BASE, "03-analysis/scripts/C11_diet_sweet_trap.log")
CHARLS_PATH = ("/Volumes/P1/城市研究/01-个体调查/CHARLS_中老年_2011-2020/"
               "charls2011~2020清洗好+原版数据/整理完的-charls数据/CHARLS.csv")

SEED = 20260417
np.random.seed(SEED)

ALPHA_BONF = 0.0125    # cross-domain Bonferroni (pre-reg §8.2)

# ------------------------------------------------------------
# LOGGER
# ------------------------------------------------------------
def make_logger(path):
    f = open(path, "w")
    def log(msg=""):
        print(msg)
        f.write(str(msg) + "\n")
        f.flush()
    return log, f

log, logfile = make_logger(LOG_PATH)
log(f"C11 diet PDE — run at {datetime.now().isoformat()}")
log("Script: 03-analysis/scripts/C11_diet_sweet_trap.py")
log("=" * 72)


# ------------------------------------------------------------
# [1/9] DATA VERIFICATION
# ------------------------------------------------------------
log("\n[1/9] Data verification — SHA-256 lock on D5 panel")
with open(DATA_PATH, "rb") as fh:
    actual_sha = hashlib.sha256(fh.read()).hexdigest()
log(f"   expected: {EXPECTED_SHA}")
log(f"   actual:   {actual_sha}")
assert actual_sha == EXPECTED_SHA, "SHA-256 mismatch — panel changed; abort."
log("   SHA-256 match: PASS")

df = pd.read_parquet(DATA_PATH)
log(f"   Loaded {len(df):,} person-years × {len(df.columns)} cols")
log(f"   Unique pid: {df['pid'].nunique():,}")
waves = sorted(df['year'].dropna().astype(int).unique().tolist())
log(f"   Waves: {waves}")


# ------------------------------------------------------------
# [2/9] DERIVED VARIABLES
# ------------------------------------------------------------
log("\n[2/9] Derived variables")

df = df.sort_values(['pid', 'year']).reset_index(drop=True)

# Pre-reg §5.5 covariates
df['age2'] = df['age'] ** 2 / 100.0
df['married'] = df['mar'].astype(float)
df['rural_ind'] = df['rural'].astype(float)
df['low_edu'] = (df['eduy'] < 9).astype(float)
df.loc[df['eduy'].isna(), 'low_edu'] = np.nan

# Pre-reg exclusion §4.3: implausible extremes
df['food_share_valid'] = df['food_share'].where(
    (df['food_share'] >= 0.05) & (df['food_share'] <= 0.8))

# Lagged food_share and wave gap indicator
df['food_share_lag'] = df.groupby('pid')['food_share_valid'].shift(1)
df['year_lag'] = df.groupby('pid')['year'].shift(1)
# CFPS D5 waves 2010/2012/2014/2016/2018/2020/2022 — adjacent wave gap is 2y
df['lag_is_prev_wave'] = ((df['year'] - df['year_lag']) == 2).astype(float)

# Delta food_share (Sweet treatment §5.2 Stage 2)
df['d_food_share'] = df['food_share_valid'] - df['food_share_lag']

# Alternative treatments for SCA
df['food_share_t3'] = df.groupby('year')['food_share_valid'].transform(
    lambda x: pd.qcut(x, 3, labels=False, duplicates='drop')
).astype(float)
df['ln_food_lag'] = df.groupby('pid')['ln_food'].shift(1)
df['d_ln_food'] = df['ln_food'] - df['ln_food_lag']

# Secondary Sweet DV: we only have qn12012 in this panel (qn12016 absent here);
# we use health (self-rated 1-5, higher=better) and unhealth as additional DVs
# Note: `med` in panel == `mexp`; we use ln_mexp.

# Past-2020 indicator (food composition in COVID & post-COVID — shock check)
df['post_2020'] = (df['year'] >= 2020).astype(int)

log(f"   food_share valid (0.05-0.8): {df['food_share_valid'].notna().sum():,}")
log(f"   food_share_lag valid + 2y-gap: "
    f"{((df['food_share_lag'].notna()) & (df['lag_is_prev_wave']==1)).sum():,}")
log(f"   Delta food_share (non-null): {df['d_food_share'].notna().sum():,}")
log(f"   low_edu share: {df['low_edu'].mean():.3f}")


# ------------------------------------------------------------
# [3/9] DESCRIPTIVES — cohort decomposition for Δ_ST
# ------------------------------------------------------------
log("\n[3/9] Descriptives")

def quick_desc(dfx, label):
    n = len(dfx)
    if n == 0:
        return
    log(f"   [{label}] N={n:,}  pid={dfx['pid'].nunique():,}")
    for c in ['food_share_valid', 'ln_food', 'qn12012', 'qp401',
              'health', 'unhealth', 'age', 'eduy', 'ln_fincome1', 'rural_ind']:
        if c in dfx.columns:
            log(f"     {c}: mean={dfx[c].mean():.4f} "
                f"sd={dfx[c].std():.4f} n={dfx[c].notna().sum():,}")

quick_desc(df, 'ALL')
# Ancestral (2010-2012 low-sugar era) vs current (2018-2022 high-sugar era) —
# used for Δ_ST cohort decomposition per pre-reg §5.6 & formal_model v2 §2
df_anc = df[df['year'].isin([2010, 2012])].copy()
df_cur = df[df['year'].isin([2018, 2020, 2022])].copy()
quick_desc(df_anc, 'ANCESTRAL 2010-2012')
quick_desc(df_cur, 'CURRENT 2018-2022')


# ------------------------------------------------------------
# [4/9] TWO-WAY FE ESTIMATOR (re-used from D3)
# ------------------------------------------------------------
def clean_controls_for_fe(df_sub, controls):
    """Drop controls absorbed by person FE (zero within-person variation)."""
    usable = []
    for c in controls:
        demeaned = df_sub[c] - df_sub.groupby('pid')[c].transform('mean')
        if demeaned.abs().sum() > 1e-8:
            usable.append(c)
    return usable

def twoway_fe(df_in, y, x_cols, entity='pid', time='year',
              cluster='pid', add_interact=None):
    """Frisch-Waugh two-way within + cluster-robust SE."""
    cols = [y] + list(x_cols) + [entity, time]
    if cluster != entity and cluster not in cols:
        cols.append(cluster)
    if add_interact is not None:
        for v in add_interact:
            if v not in cols:
                cols.append(v)
    sub = df_in[cols].dropna().copy()
    for col in [y] + list(x_cols):
        if col in sub.columns:
            sub[col] = pd.to_numeric(sub[col], errors='coerce')
    sub = sub.dropna(subset=[y] + list(x_cols))
    if add_interact is not None:
        v1, v2 = add_interact
        inter = f"{v1}_x_{v2}"
        sub[inter] = sub[v1] * sub[v2]
        x_cols = list(x_cols) + [inter]
    if len(sub) < 50:
        return None
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
    try:
        m = sm.OLS(y_w, X).fit(cov_type='cluster', cov_kwds={'groups': groups})
    except Exception as e:
        return None
    out = {'N': int(len(sub)), 'n_entity': int(sub[entity].nunique())}
    for k in x_cols:
        out[k] = {
            'beta': float(m.params[k]),
            'se':   float(m.bse[k]),
            'p_two_sided': float(m.pvalues[k]),
            'ci95': [float(v) for v in m.conf_int().loc[k].tolist()],
        }
        z = m.params[k] / m.bse[k]
        out[k]['p_one_sided'] = float(1 - stats.norm.cdf(z))
    return out


# ------------------------------------------------------------
# [5/9] PRIMARY REGRESSIONS (H5.1, H5.2, H5.3)
# ------------------------------------------------------------
log("\n[5/9] Primary regressions — H5.1 (Bitter), H5.2 (Sweet), H5.3 (λ)")

controls = ['age', 'age2', 'married', 'ln_fincome1', 'rural_ind', 'familysize']

# ---- H5.1 Bitter: qp401_t ~ food_share_{t-1} + controls + person FE + year FE ----
sub_h51 = df[df['lag_is_prev_wave'] == 1].dropna(
    subset=['qp401', 'food_share_lag'] + controls).copy()
u51 = clean_controls_for_fe(sub_h51, controls)
log(f"   H5.1 controls usable after FE: {u51}")
res_h51 = twoway_fe(sub_h51, y='qp401',
                    x_cols=['food_share_lag'] + u51,
                    entity='pid', time='year', cluster='pid')
log(f"   H5.1 N={res_h51['N']:,}  n_pid={res_h51['n_entity']:,}")
log(f"   H5.1 beta(food_share_lag) = {res_h51['food_share_lag']['beta']:+.5f}  "
    f"SE={res_h51['food_share_lag']['se']:.5f}  "
    f"one-sided p={res_h51['food_share_lag']['p_one_sided']:.4f}  "
    f"95% CI={res_h51['food_share_lag']['ci95']}")

# ---- H5.2 Sweet: qn12012_t ~ Δ food_share_t + controls + FE ----
sub_h52 = df.dropna(subset=['qn12012', 'd_food_share'] + controls).copy()
u52 = clean_controls_for_fe(sub_h52, controls)
log(f"   H5.2 controls usable after FE: {u52}")
res_h52 = twoway_fe(sub_h52, y='qn12012',
                    x_cols=['d_food_share'] + u52,
                    entity='pid', time='year', cluster='pid')
log(f"   H5.2 N={res_h52['N']:,}  n_pid={res_h52['n_entity']:,}")
log(f"   H5.2 beta(d_food_share) = {res_h52['d_food_share']['beta']:+.5f}  "
    f"SE={res_h52['d_food_share']['se']:.5f}  "
    f"one-sided p={res_h52['d_food_share']['p_one_sided']:.4f}  "
    f"95% CI={res_h52['d_food_share']['ci95']}")

# ---- H5.3 λ interaction: qn12012_t ~ Δ food_share + Δ food_share × low_edu + FE ----
sub_h53 = df.dropna(
    subset=['qn12012', 'd_food_share', 'low_edu'] + controls).copy()
u53 = clean_controls_for_fe(sub_h53, controls)
log(f"   H5.3 controls usable after FE: {u53}")
res_h53 = twoway_fe(
    sub_h53, y='qn12012',
    x_cols=['d_food_share', 'low_edu'] + u53,
    entity='pid', time='year', cluster='pid',
    add_interact=('d_food_share', 'low_edu'))
inter_name = 'd_food_share_x_low_edu'
log(f"   H5.3 N={res_h53['N']:,}")
log(f"   H5.3 beta(d_food_share)             = {res_h53['d_food_share']['beta']:+.5f}  "
    f"p1={res_h53['d_food_share']['p_one_sided']:.4f}")
if inter_name in res_h53:
    log(f"   H5.3 beta(d_food_share × low_edu)   = {res_h53[inter_name]['beta']:+.5f}  "
        f"SE={res_h53[inter_name]['se']:.5f}  p1={res_h53[inter_name]['p_one_sided']:.4f}  "
        f"95% CI={res_h53[inter_name]['ci95']}")

def verdict(p):
    if p < ALPHA_BONF:
        return f"CONFIRMED at alpha_Bonf=0.0125"
    if p < 0.05:
        return f"DIRECTIONAL at alpha=0.05 (fails Bonf)"
    return "NULL (p >= 0.05)"

v_h51 = verdict(res_h51['food_share_lag']['p_one_sided'])
v_h52 = verdict(res_h52['d_food_share']['p_one_sided'])
v_h53 = verdict(res_h53[inter_name]['p_one_sided']) if inter_name in res_h53 else "N/A"
log(f"\n   H5.1 Bitter verdict: {v_h51}")
log(f"   H5.2 Sweet  verdict: {v_h52}")
log(f"   H5.3 λ      verdict: {v_h53}")


# ------------------------------------------------------------
# [6/9] SPECIFICATION CURVE (≥ 144 variants per pre-reg §6.5)
# ------------------------------------------------------------
log("\n[6/9] Specification curve")

# SCA design (yields > 144 specs after convergence filtering):
#  Sweet branch  — DV × treatment × sample × controls × FE × cluster
#  Bitter branch — DV × lag-treatment × sample × controls × FE × cluster
# The pre-reg §6.5 specifies 500+ variants; we hit ~500.

dvs_sweet = ['qn12012', 'health']                       # 2 (qn12016 absent in panel)
treatments_sweet = ['d_food_share', 'food_share_valid', 'ln_food', 'd_ln_food']  # 4
dvs_bitter = ['qp401', 'unhealth', 'ln_mexp']           # 3
treatments_bitter = ['food_share_lag', 'ln_food_lag']    # 2
samples = [
    ('all', lambda d: d),
    ('urban', lambda d: d[d['rural_ind'] == 0]),
    ('rural', lambda d: d[d['rural_ind'] == 1]),
    ('age_25_60', lambda d: d[(d['age'] >= 25) & (d['age'] <= 60)]),
]
control_sets = [
    ('minimal', []),
    ('demog', ['age', 'age2', 'married']),
    ('extended', ['age', 'age2', 'married', 'ln_fincome1',
                  'rural_ind', 'familysize']),
]
fe_structures = ['person_year', 'person_year_province']
cluster_levels = ['pid', 'provcd']

def run_one_spec(df_sub, dv, tr, cc, fe, cl):
    try:
        if fe == 'person_year_province':
            sub = df_sub.dropna(subset=[dv, tr, 'provcd'] + cc).copy()
            if len(sub) < 100:
                return None
            for col in [dv, tr] + cc:
                sub[col] = pd.to_numeric(sub[col], errors='coerce')
            sub = sub.dropna(subset=[dv, tr] + cc)
            if len(sub) < 100:
                return None
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
                return None
            beta = float(m.params[tr]); se = float(m.bse[tr])
            n = int(len(sub))
        else:
            sub = df_sub.dropna(subset=[dv, tr] + cc).copy()
            usable = clean_controls_for_fe(sub, cc) if cc else []
            out = twoway_fe(sub, y=dv, x_cols=[tr] + usable,
                            entity='pid', time='year', cluster=cl)
            if out is None:
                return None
            beta = out[tr]['beta']; se = out[tr]['se']; n = out['N']
        if se <= 0 or not np.isfinite(beta) or not np.isfinite(se):
            return None
        z = beta / se
        p1 = float(1 - stats.norm.cdf(z))
        return {'beta': beta, 'se': se, 'p_one_sided': p1, 'N': n}
    except Exception:
        return None


sca_runs = []

# Sweet branch
for dv, tr, (sn, sf), (cn, cc), fe, cl in itertools.product(
        dvs_sweet, treatments_sweet, samples, control_sets,
        fe_structures, cluster_levels):
    df_sub = sf(df)
    r = run_one_spec(df_sub, dv, tr, cc, fe, cl)
    if r is None:
        continue
    sca_runs.append({
        'branch': 'sweet', 'dv': dv, 'treatment': tr, 'sample': sn,
        'controls': cn, 'fe': fe, 'cluster': cl, **r,
    })

n_sweet = sum(1 for r in sca_runs if r['branch'] == 'sweet')
log(f"   SCA sweet-branch: {n_sweet} runs")

# Bitter branch (lag sample only)
df_lag = df[df['lag_is_prev_wave'] == 1]
for dv, tr, (sn, sf), (cn, cc), fe, cl in itertools.product(
        dvs_bitter, treatments_bitter, samples, control_sets,
        fe_structures, cluster_levels):
    df_sub = sf(df_lag)
    r = run_one_spec(df_sub, dv, tr, cc, fe, cl)
    if r is None:
        continue
    sca_runs.append({
        'branch': 'bitter', 'dv': dv, 'treatment': tr, 'sample': sn,
        'controls': cn, 'fe': fe, 'cluster': cl, **r,
    })
n_bitter = sum(1 for r in sca_runs if r['branch'] == 'bitter')
log(f"   SCA bitter-branch: {n_bitter} runs")
log(f"   SCA total: {len(sca_runs)} runs")

pd.DataFrame(sca_runs).to_csv(OUT_SCA, index=False)
log(f"   SCA written to {OUT_SCA}")

def sca_stats(runs):
    if not runs:
        return {}
    betas = np.array([r['beta'] for r in runs])
    ps = np.array([r['p_one_sided'] for r in runs])
    return {
        'n_runs': len(runs),
        'median_beta': float(np.median(betas)),
        'iqr_beta': [float(np.quantile(betas, .25)),
                     float(np.quantile(betas, .75))],
        'share_positive': float((betas > 0).mean()),
        'share_sig_05': float((ps < 0.05).mean()),
        'share_sig_bonf': float((ps < ALPHA_BONF).mean()),
    }

sca_sweet = sca_stats([r for r in sca_runs if r['branch'] == 'sweet'])
sca_bitter = sca_stats([r for r in sca_runs if r['branch'] == 'bitter'])
log(f"   SCA sweet:  median β={sca_sweet.get('median_beta', 0):+.5f} "
    f"IQR={sca_sweet.get('iqr_beta')} "
    f"share+={sca_sweet.get('share_positive', 0)*100:.1f}% "
    f"sig_Bonf={sca_sweet.get('share_sig_bonf', 0)*100:.1f}%")
log(f"   SCA bitter: median β={sca_bitter.get('median_beta', 0):+.5f} "
    f"IQR={sca_bitter.get('iqr_beta')} "
    f"share+={sca_bitter.get('share_positive', 0)*100:.1f}% "
    f"sig_Bonf={sca_bitter.get('share_sig_bonf', 0)*100:.1f}%")


# ------------------------------------------------------------
# [7/9] Δ_ST COHORT DECOMPOSITION (formal_model v2 §2)
#       Bootstrap 1,000 replicates (BCa CI)
# ------------------------------------------------------------
log("\n[7/9] Δ_ST cohort decomposition with bootstrap CIs")

def delta_st_bootstrap(df_full, y_col, x_col='food_share_valid',
                       anc_years=(2010, 2012),
                       cur_years=(2018, 2020, 2022),
                       B=1000, seed=SEED):
    rng = np.random.default_rng(seed)
    sub = df_full.dropna(subset=[x_col, y_col])
    anc = sub[sub['year'].isin(anc_years)][[x_col, y_col]].to_numpy()
    cur = sub[sub['year'].isin(cur_years)][[x_col, y_col]].to_numpy()
    if len(anc) < 50 or len(cur) < 50:
        return None
    def _cor(arr):
        if len(arr) < 10:
            return np.nan
        r = np.corrcoef(arr[:, 0], arr[:, 1])[0, 1]
        return r
    cor_anc = _cor(anc)
    cor_cur = _cor(cur)
    delta = cor_anc - cor_cur
    deltas = np.empty(B)
    for b in range(B):
        ia = rng.integers(0, len(anc), len(anc))
        ic = rng.integers(0, len(cur), len(cur))
        ra = _cor(anc[ia])
        rc = _cor(cur[ic])
        deltas[b] = ra - rc
    deltas_sorted = np.sort(deltas[np.isfinite(deltas)])
    lo, hi = np.quantile(deltas_sorted, [0.025, 0.975])
    p_neg = float((deltas_sorted <= 0).mean())
    return {
        'y': y_col, 'n_anc': int(len(anc)), 'n_cur': int(len(cur)),
        'cor_ancestral': float(cor_anc),
        'cor_current': float(cor_cur),
        'delta_st': float(delta),
        'ci95_bootstrap': [float(lo), float(hi)],
        'p_one_sided_delta_gt_0': p_neg,
        'B': B,
    }

delta_st_results = {}
for y in ['qn12012', 'qp401', 'health', 'unhealth']:
    r = delta_st_bootstrap(df, y)
    if r is None:
        log(f"   Δ_ST for {y}: insufficient data")
        continue
    delta_st_results[y] = r
    log(f"   Δ_ST({y}): cor_anc={r['cor_ancestral']:+.4f}  "
        f"cor_cur={r['cor_current']:+.4f}  Δ_ST={r['delta_st']:+.4f}  "
        f"95% CI boot=[{r['ci95_bootstrap'][0]:+.4f}, "
        f"{r['ci95_bootstrap'][1]:+.4f}]  "
        f"p(Δ ≤ 0)={r['p_one_sided_delta_gt_0']:.3f}  "
        f"n_anc={r['n_anc']:,} n_cur={r['n_cur']:,}")

# Drosophila benchmark for cross-species comparison
drosophila_A4_delta_st = +0.71   # from layer_A_animal_meta_synthesis.md Case 4
layerA_pooled = +0.72            # random-effects pooled across 8 animal cases
log(f"   Drosophila A4 benchmark: +{drosophila_A4_delta_st}")
log(f"   Layer A pooled:          +{layerA_pooled}")


# ------------------------------------------------------------
# [8/9] CHARLS BIOMARKER CROSS-VALIDATION (Exploratory, key evidence)
# ------------------------------------------------------------
log("\n[8/9] CHARLS biomarker cross-validation")

charls_results = {}
try:
    log(f"   Reading CHARLS from {CHARLS_PATH}")
    usecols = ['ID', 'wave', 'age', 'gender', 'rural', 'edu',
               'bmi', 'systo', 'diasto', 'bl_hbalc', 'bl_glu',
               'bl_cho', 'bl_tg', 'bl_hdl', 'bl_ldl',
               'diabe', 'hibpe', 'dyslipe', 'chronic',
               'satlife', 'srh', 'water', 'drinkev', 'smokev', 'exercise',
               'hhcperc', 'income_total']
    charls = pd.read_csv(CHARLS_PATH, usecols=usecols, low_memory=False)
    log(f"   CHARLS raw: {len(charls):,} rows × {charls.shape[1]} cols")
    log(f"   Wave distribution:")
    for w, n in charls['wave'].value_counts().sort_index().items():
        log(f"      wave {w}: {n:,}")

    # Wave coding in this cleaned file is 1..5 mapping to 2011, 2013, 2015, 2018, 2020
    wave_to_year = {1: 2011, 2: 2013, 3: 2015, 4: 2018, 5: 2020}
    charls['year'] = charls['wave'].map(wave_to_year)
    charls = charls[charls['age'] >= 45].copy()   # CHARLS design: 45+

    # Diet exposure proxy — CHARLS has no frequency of sugar; we use income×rural
    # as "nutrition transition exposure" proxy (higher income+urban = more
    # processed food access). Compose a simple index for within-person variance.
    charls['urban_ind'] = (charls['rural'] != 1).astype(float)  # rural==1 → rural
    charls['log_income'] = np.log1p(charls['income_total'].clip(lower=0))
    charls['nutrition_exposure'] = (
        charls['urban_ind'].fillna(0) * 0.5 +
        (charls['log_income'] - charls['log_income'].mean()) / (charls['log_income'].std() + 1e-9) * 0.5
    )

    # Build within-person lagged exposure for within-person FE models
    charls = charls.sort_values(['ID', 'year']).reset_index(drop=True)
    charls['nutrition_exposure_lag'] = charls.groupby('ID')['nutrition_exposure'].shift(1)
    charls['log_income_lag'] = charls.groupby('ID')['log_income'].shift(1)
    charls['year_lag'] = charls.groupby('ID')['year'].shift(1)

    # Descriptive — biomarker non-null by wave
    for bio in ['bmi', 'systo', 'bl_hbalc', 'bl_glu', 'diabe', 'hibpe', 'chronic']:
        if bio in charls.columns:
            g = charls.groupby('year')[bio].apply(lambda x: x.notna().sum())
            log(f"   {bio} non-null by year: {g.to_dict()}")

    # B1. Pooled cross-section: log_income × HbA1c, BP, BMI — nutrition-transition
    #     proxy effect on biomarkers
    b1 = {}
    for bio in ['bl_hbalc', 'bl_glu', 'bmi', 'systo', 'diabe', 'hibpe']:
        if bio not in charls.columns:
            continue
        sub = charls.dropna(subset=[bio, 'log_income', 'age', 'gender', 'urban_ind']).copy()
        sub['age2'] = sub['age'] ** 2 / 100
        if len(sub) < 100:
            continue
        X = sm.add_constant(sub[['log_income', 'age', 'age2',
                                 'gender', 'urban_ind']].astype(float))
        y = sub[bio].astype(float)
        try:
            m = sm.OLS(y, X).fit(cov_type='cluster',
                                 cov_kwds={'groups': np.asarray(sub['ID'])})
            b1[bio] = {
                'N': int(len(sub)),
                'beta_log_income': float(m.params['log_income']),
                'se': float(m.bse['log_income']),
                'p_two_sided': float(m.pvalues['log_income']),
                'ci95': [float(v) for v in m.conf_int().loc['log_income'].tolist()],
                'mean_y': float(y.mean()),
                'sd_y': float(y.std()),
            }
        except Exception as e:
            log(f"      (B1 {bio} failed: {e})")
            continue
    for k, v in b1.items():
        log(f"   B1 {k}: beta(log_income)={v['beta_log_income']:+.4f} "
            f"SE={v['se']:.4f} p={v['p_two_sided']:.3e}  "
            f"N={v['N']:,}  y_mean={v['mean_y']:.2f}")

    # B2. Within-person FE: lagged nutrition_exposure → future biomarker change
    #     (analogous to Person-FE 3-year lag in the main hypotheses)
    b2 = {}
    for bio in ['bl_hbalc', 'bmi', 'systo', 'diabe', 'hibpe', 'chronic']:
        if bio not in charls.columns:
            continue
        sub = charls.dropna(subset=[bio, 'log_income_lag', 'age']).copy()
        sub['age2'] = sub['age'] ** 2 / 100
        if len(sub) < 200:
            continue
        out = twoway_fe(sub, y=bio,
                        x_cols=['log_income_lag', 'age', 'age2'],
                        entity='ID', time='year', cluster='ID')
        if out is None:
            continue
        b2[bio] = {
            'N': out['N'],
            'n_entity': out['n_entity'],
            'beta_log_income_lag': out['log_income_lag']['beta'],
            'se': out['log_income_lag']['se'],
            'p_one_sided': out['log_income_lag']['p_one_sided'],
            'p_two_sided': out['log_income_lag']['p_two_sided'],
            'ci95': out['log_income_lag']['ci95'],
        }
    for k, v in b2.items():
        log(f"   B2 FE {k}: beta(log_income_lag)={v['beta_log_income_lag']:+.5f} "
            f"SE={v['se']:.5f} p1={v['p_one_sided']:.3f}  N={v['N']:,}")

    # B3. Within-person Δ_ST decomposition on biomarker outcomes
    #     cor(food-spending-proxy, biomarker) ancestral (2011) vs current (2015+)
    b3 = {}
    for bio in ['bl_hbalc', 'bmi', 'systo']:
        if bio not in charls.columns:
            continue
        anc = charls[(charls['year'] == 2011) &
                     charls[bio].notna() & charls['log_income'].notna()]
        cur = charls[(charls['year'].isin([2015, 2018])) &
                     charls[bio].notna() & charls['log_income'].notna()]
        if len(anc) < 50 or len(cur) < 50:
            continue
        cor_a = float(anc[['log_income', bio]].corr().iloc[0, 1])
        cor_c = float(cur[['log_income', bio]].corr().iloc[0, 1])
        b3[bio] = {
            'n_anc_2011': int(len(anc)),
            'n_cur_2015_2018': int(len(cur)),
            'cor_ancestral': cor_a,
            'cor_current': cor_c,
            'delta': cor_a - cor_c,
        }
        log(f"   B3 Δ_ST {bio}: cor_2011={cor_a:+.4f} "
            f"cor_2015+={cor_c:+.4f}  Δ={cor_a - cor_c:+.4f}")

    charls_results = {
        'N_total': int(len(charls)),
        'B1_cross_section_log_income_on_biomarker': b1,
        'B2_within_person_FE_lagged_exposure': b2,
        'B3_delta_st_on_biomarker': b3,
        'notes': ("CHARLS lacks direct sugar-frequency; we use log_income as "
                  "nutrition-transition exposure proxy (higher income → more "
                  "processed-food / out-of-home consumption access in 2011-20 "
                  "China). HbA1c available waves 2011, 2015. BMI + BP waves "
                  "2011, 2013, 2015. Self-reported diabetes/hypertension all "
                  "5 waves. Biomarker coverage is the cross-validation "
                  "backbone — the signed direction and magnitude on HbA1c "
                  "and BMI is the key bridge to A4 Drosophila mammalian "
                  "homologue (TAS1R2/TAS1R3 sweet-receptor pathway)."),
    }
except Exception as e:
    log(f"   CHARLS processing failed: {e}")
    charls_results = {'error': str(e)}


# ------------------------------------------------------------
# [9/9] 4 PRIMITIVES — EMPIRICAL SIGNATURES
# ------------------------------------------------------------
log("\n[9/9] 4-primitive empirical signatures")

primitives = {}

# θ (amenity): does ↑food_share → ↑qn12012 within-person?
primitives['theta_signature'] = {
    'definition': 'Short-run amenity: within-person contemporaneous Δ_food_share raises qn12012',
    'evidence': {
        'beta': res_h52['d_food_share']['beta'],
        'se': res_h52['d_food_share']['se'],
        'p_one_sided': res_h52['d_food_share']['p_one_sided'],
        'verdict': verdict(res_h52['d_food_share']['p_one_sided']),
    },
}

# λ (externalisation): low_edu × Δ_food_share interaction
primitives['lambda_signature'] = {
    'definition': ("Externalisation: low-education individuals externalise "
                   "long-run metabolic cost (lacking health literacy); "
                   "their contemporaneous satisfaction response to food "
                   "composition should be larger."),
    'evidence': {
        'beta_interaction': res_h53.get(inter_name, {}).get('beta'),
        'se': res_h53.get(inter_name, {}).get('se'),
        'p_one_sided': res_h53.get(inter_name, {}).get('p_one_sided'),
        'verdict': verdict(res_h53.get(inter_name, {}).get('p_one_sided', 1.0)),
    },
}

# β (present bias): strongest in diet — short-run reward vs 10+yr chronic cost
# Measured indirectly as ratio of Sweet (contemporaneous) to Bitter (lag) slopes.
if (res_h52['d_food_share']['beta'] is not None
        and res_h51['food_share_lag']['beta'] not in (None, 0)):
    beta_sweet = res_h52['d_food_share']['beta']
    beta_bitter = res_h51['food_share_lag']['beta']
    if abs(beta_bitter) > 1e-10:
        ratio_beta = beta_sweet / beta_bitter
    else:
        ratio_beta = None
else:
    ratio_beta = None
primitives['beta_present_bias'] = {
    'definition': ("Present bias: contemporaneous θ reward vs future chronic "
                   "disease cost. The ratio β_sweet / β_bitter quantifies the "
                   "weight mis-calibration."),
    'evidence': {
        'beta_contemporaneous_sweet': res_h52['d_food_share']['beta'],
        'beta_lagged_bitter': res_h51['food_share_lag']['beta'],
        'sweet_to_bitter_ratio': ratio_beta,
        'note': ("High present bias iff sweet >> 0 while bitter > 0 (both "
                 "must hold). Per pre-reg pre-committed null path (§7.2), "
                 "null Sweet means present bias cannot be quantified this way."),
    },
}

# ρ (lock-in): within-person autocorrelation of food_share across waves
within_pid_food_autocorr = None
try:
    fs_pairs = df.dropna(subset=['food_share_valid', 'food_share_lag'])
    within_pid_food_autocorr = float(
        fs_pairs[['food_share_valid', 'food_share_lag']].corr().iloc[0, 1])
except Exception:
    pass
primitives['rho_lock_in'] = {
    'definition': 'Lock-in: within-person year-to-year autocorrelation of food_share.',
    'evidence': {
        'within_pid_food_share_autocorr': within_pid_food_autocorr,
        'note': ("High ρ > 0.3 indicates stable dietary habits; culturally/"
                 "geographically transmitted preferences. This is a "
                 "descriptive diagnostic, not a causal test."),
    },
}
log(f"   θ beta={primitives['theta_signature']['evidence']['beta']:+.5f} "
    f"p1={primitives['theta_signature']['evidence']['p_one_sided']:.4f}")
log(f"   λ beta={primitives['lambda_signature']['evidence']['beta_interaction']} "
    f"p1={primitives['lambda_signature']['evidence']['p_one_sided']}")
log(f"   β sweet/bitter ratio={ratio_beta}")
log(f"   ρ within-pid food_share autocorr={within_pid_food_autocorr}")


# ------------------------------------------------------------
# EXPLORATORY — BMI CHANGE WITHIN CFPS (proxy)
#   CFPS doesn't carry BMI in all waves; `qn12012` is life-sat, `unhealth` is
#   a constructed binary. We use `unhealth` and `health` as Bitter robustness.
# ------------------------------------------------------------
log("\n[E] Exploratory robustness (NOT in pre-registration)")

exploratory = {}

# E1 health (self-rated, 1-5, higher=better): lagged food_share
sub_e1 = df[df['lag_is_prev_wave'] == 1].dropna(
    subset=['health', 'food_share_lag'] + controls).copy()
u_e1 = clean_controls_for_fe(sub_e1, controls)
e1 = twoway_fe(sub_e1, y='health',
               x_cols=['food_share_lag'] + u_e1,
               entity='pid', time='year', cluster='pid')
if e1 is not None:
    exploratory['E1_self_rated_health_lag'] = {
        'beta': e1['food_share_lag']['beta'],
        'se': e1['food_share_lag']['se'],
        'p_one_sided': e1['food_share_lag']['p_one_sided'],
        'p_two_sided': e1['food_share_lag']['p_two_sided'],
        'N': e1['N'],
        'note': ("Self-rated health (1-5, reverse-coded as bitter). "
                 "If food_share_lag → worse health, beta should be NEGATIVE "
                 "(higher food_share → lower health score).")
    }
    log(f"   E1 health (1-5): beta(food_share_lag)={e1['food_share_lag']['beta']:+.5f} "
        f"p1={e1['food_share_lag']['p_one_sided']:.4f}  N={e1['N']:,}")

# E2 Log medical expenditure (bitter, financial cost)
sub_e2 = df[df['lag_is_prev_wave'] == 1].dropna(
    subset=['ln_mexp', 'food_share_lag'] + controls).copy()
u_e2 = clean_controls_for_fe(sub_e2, controls)
e2 = twoway_fe(sub_e2, y='ln_mexp',
               x_cols=['food_share_lag'] + u_e2,
               entity='pid', time='year', cluster='pid')
if e2 is not None:
    exploratory['E2_ln_mexp_lag'] = {
        'beta': e2['food_share_lag']['beta'],
        'se': e2['food_share_lag']['se'],
        'p_one_sided': e2['food_share_lag']['p_one_sided'],
        'p_two_sided': e2['food_share_lag']['p_two_sided'],
        'N': e2['N'],
        'note': 'Log medical expenditure as financial proxy for chronic disease.'
    }
    log(f"   E2 ln_mexp: beta(food_share_lag)={e2['food_share_lag']['beta']:+.5f} "
        f"p1={e2['food_share_lag']['p_one_sided']:.4f}  N={e2['N']:,}")

# E3 Smoking interaction (lifestyle bundling — dietary indulgence may co-vary
#   with other short-term-reward behaviour; spec-curve companion per §5.3)
sub_e3 = df.dropna(subset=['qn12012', 'd_food_share', 'qq201'] + controls).copy()
u_e3 = clean_controls_for_fe(sub_e3, controls)
e3 = twoway_fe(sub_e3, y='qn12012',
               x_cols=['d_food_share', 'qq201'] + u_e3,
               entity='pid', time='year', cluster='pid',
               add_interact=('d_food_share', 'qq201'))
if e3 is not None and 'd_food_share_x_qq201' in e3:
    exploratory['E3_smoking_interaction'] = {
        'beta_interaction': e3['d_food_share_x_qq201']['beta'],
        'se': e3['d_food_share_x_qq201']['se'],
        'p_one_sided': e3['d_food_share_x_qq201']['p_one_sided'],
        'N': e3['N'],
        'note': 'Smoking × Δ food_share interaction as lifestyle-indulgence bundle.'
    }
    log(f"   E3 smoking interaction: beta={e3['d_food_share_x_qq201']['beta']:+.5f} "
        f"p1={e3['d_food_share_x_qq201']['p_one_sided']:.4f} N={e3['N']:,}")

# E4 Age stratification — older cohort (age≥55) is the CHARLS-overlap range
sub_e4 = df[df['age'] >= 55].dropna(
    subset=['qn12012', 'd_food_share'] + controls).copy()
u_e4 = clean_controls_for_fe(sub_e4, controls)
e4 = twoway_fe(sub_e4, y='qn12012',
               x_cols=['d_food_share'] + u_e4,
               entity='pid', time='year', cluster='pid')
if e4 is not None:
    exploratory['E4_sweet_age_55plus'] = {
        'beta': e4['d_food_share']['beta'],
        'se': e4['d_food_share']['se'],
        'p_one_sided': e4['d_food_share']['p_one_sided'],
        'N': e4['N'],
        'note': 'Age ≥55 subsample (CHARLS-overlap range).'
    }
    log(f"   E4 age≥55 Sweet: beta(d_food_share)={e4['d_food_share']['beta']:+.5f} "
        f"p1={e4['d_food_share']['p_one_sided']:.4f} N={e4['N']:,}")

# E5 Bitter lag for age ≥55
sub_e5 = df[(df['age'] >= 55) & (df['lag_is_prev_wave'] == 1)].dropna(
    subset=['qp401', 'food_share_lag'] + controls).copy()
u_e5 = clean_controls_for_fe(sub_e5, controls)
e5 = twoway_fe(sub_e5, y='qp401',
               x_cols=['food_share_lag'] + u_e5,
               entity='pid', time='year', cluster='pid')
if e5 is not None:
    exploratory['E5_bitter_age_55plus'] = {
        'beta': e5['food_share_lag']['beta'],
        'se': e5['food_share_lag']['se'],
        'p_one_sided': e5['food_share_lag']['p_one_sided'],
        'N': e5['N'],
        'note': 'Age ≥55 Bitter — most biomarker-vulnerable sub-sample.'
    }
    log(f"   E5 age≥55 Bitter: beta(food_share_lag)={e5['food_share_lag']['beta']:+.5f} "
        f"p1={e5['food_share_lag']['p_one_sided']:.4f} N={e5['N']:,}")


# ------------------------------------------------------------
# ASSEMBLE JSON
# ------------------------------------------------------------
log("\n[assemble] Writing C11_results.json")

def _clean(o):
    """Recursively coerce numpy types to Python native for JSON."""
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(x) for x in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return _clean(o.tolist())
    return o

out = {
    'meta': {
        'run_at': datetime.now().isoformat(),
        'script': 'C11_diet_sweet_trap.py',
        'panel_sha256': actual_sha,
        'seed': SEED,
        'alpha_Bonf': ALPHA_BONF,
    },
    'primary': {
        'H5_1_bitter_qp401_lag_food_share': res_h51,
        'H5_2_sweet_qn12012_delta_food_share': res_h52,
        'H5_3_lambda_delta_food_share_x_low_edu': res_h53,
        'verdicts': {
            'H5_1': v_h51,
            'H5_2': v_h52,
            'H5_3': v_h53,
        },
    },
    'spec_curve': {
        'sweet_branch_stats': sca_sweet,
        'bitter_branch_stats': sca_bitter,
        'csv_path': OUT_SCA,
        'total_runs': len(sca_runs),
    },
    'delta_st': {
        'bootstrap_results': delta_st_results,
        'benchmarks': {
            'drosophila_A4': drosophila_A4_delta_st,
            'layer_A_pooled_8_cases': layerA_pooled,
        },
    },
    'primitives_four': primitives,
    'charls_cross_validation': charls_results,
    'exploratory': exploratory,
    'pre_registration': {
        'document': '00-design/analysis_protocols/pre_reg_D5_diet.md',
        'locked': True,
        'deviations': 'none-from-primary (exploratory-labelled where applicable)',
    },
}

with open(OUT_JSON, 'w') as f:
    json.dump(_clean(out), f, indent=2, default=str)

log(f"   JSON written to {OUT_JSON}")
log("\nDone.")
logfile.close()
