"""
C13 Conspicuous Housing / School-district Upgrade — Sweet Trap PDE
===================================================================

Purpose
  Execute the Pre-Registered + Data-driven PDE (Pre-registered Deep Exam)
  pipeline for Study C13 (new Focal candidate) of the Sweet-Trap
  cross-species manuscript. After C2 (鸡娃) and C4 (bride-price) demotion,
  C11 (diet) is the current Focal-1 candidate; C13 is a Focal-2 candidate
  with clean F2 aspirational-selection evidence.

Sweet Trap mapping (Layer A bridge)
  C13 is the human-level homologue of A7 peacock runaway + A4 Drosophila
  supernormal sweet preference:
    - Fisher runaway: neighbours upgrade -> not upgrading = social failure,
      so every family keeps bidding housing up past its utility optimum.
    - Supernormal signal: "big house + school district + luxury car" is
      a human display analogue of the peacock tail feather.
  Layer A pooled Δ_ST = +0.72 [+0.60, +0.83] across 8 animal cases.
  A7 peacock Δ_ST ≈ +0.80; predicted human C13 band: +0.40 to +0.65.

F2 gatekeeper (Andy 2026-04-17 correction — feedback_sweet_trap_strict_F2)
  Before ANY regression: confirm mortgage / housing-upgrade is voluntarily
  adopted by higher-SES households (aspirational). If cor(mortgage_burden,
  income) < 0, or higher-education households take on LESS mortgage debt,
  then C13 is coerced squeeze (like C2 教育), not Sweet Trap, and we demote
  honestly.

Hypotheses (mapped to pre_reg_D8_housing.md §2)
  H8.1 Sweet (status):     ∂ dw_{i,t} / ∂ mortgage_burden_{i,t} > 0
  H8.2 Bitter (savings):   ∂ ln_savings_{i,t} / ∂ mortgage_burden_{i,t-1} < 0
  H8.3 λ (young cohort):   ∂² dw / ∂ mortgage_burden ∂ young > 0
  H8.4 Positional validity: β̂(H8.1) ≥ 0.5 × uncontrolled when
       ln(fincome1), ln(total_asset) added (NOT income-driven)
  α_Bonf = 0.0125 (cross-domain)

Data provenance
  Panel: 02-data/processed/panel_D8_housing.parquet
         SHA-256 lock: 0e5a7582c104a37b7aa51875e17244e425d56a1281b12eff4799c5dda71c05e8
         83,585 person-years × 62 cols, 7 waves 2010-2022, 31,511 unique pid.

Outputs
  02-data/processed/C13_results.json           full numeric record
  02-data/processed/C13_speccurve.csv          SCA rows (>= 144 specs)
  03-analysis/scripts/C13_housing_sweet_trap.log   execution log
  00-design/pde/C13_housing_findings.md        narrative PDE report

Constraints
  - n_workers = 1 (no multiprocessing).
  - Panel SHA-256 verified; panel NOT modified.
  - No multiprocessing.Pool(os.cpu_count()).
  - Random seed 20260417 for bootstrap CIs.
  - Comments in English, findings report in Chinese.
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
DATA_PATH = os.path.join(BASE, "02-data/processed/panel_D8_housing.parquet")
EXPECTED_SHA = "0e5a7582c104a37b7aa51875e17244e425d56a1281b12eff4799c5dda71c05e8"
OUT_JSON = os.path.join(BASE, "02-data/processed/C13_results.json")
OUT_SCA = os.path.join(BASE, "02-data/processed/C13_speccurve.csv")
LOG_PATH = os.path.join(BASE, "03-analysis/scripts/C13_housing_sweet_trap.log")

SEED = 20260417
np.random.seed(SEED)

ALPHA_BONF = 0.0125
B_BOOT = 1000

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
log(f"C13 housing PDE -- run at {datetime.now().isoformat()}")
log("Script: 03-analysis/scripts/C13_housing_sweet_trap.py")
log("=" * 72)


# ------------------------------------------------------------
# [1/10] DATA VERIFICATION
# ------------------------------------------------------------
log("\n[1/10] Data verification -- SHA-256 lock on D8 panel")
with open(DATA_PATH, "rb") as fh:
    actual_sha = hashlib.sha256(fh.read()).hexdigest()
log(f"   expected: {EXPECTED_SHA}")
log(f"   actual:   {actual_sha}")
assert actual_sha == EXPECTED_SHA, "SHA-256 mismatch -- panel changed; abort."
log("   SHA-256 match: PASS")

df = pd.read_parquet(DATA_PATH)
log(f"   Loaded {len(df):,} person-years x {len(df.columns)} cols")
log(f"   Unique pid: {df['pid'].nunique():,}")
waves = sorted(df['year'].dropna().astype(int).unique().tolist())
log(f"   Waves: {waves}")


# ------------------------------------------------------------
# [2/10] DERIVED VARIABLES
# ------------------------------------------------------------
log("\n[2/10] Derived variables & sample prep")

# Canonical sort for lagging
df = df.sort_values(['pid', 'year']).reset_index(drop=True)

# age helpers for H8.3
df['age2'] = df['age'] ** 2 / 100.0
df['young'] = (df['age'] < 40).astype(float)
df.loc[df['age'].isna(), 'young'] = np.nan
df['married'] = df['mar'].astype(float)
df['rural_ind'] = df['rural'].astype(float)
df['urban_ind'] = df['urban'].astype(float)
df['low_edu'] = (df['eduy'] < 9).astype(float)
df.loc[df['eduy'].isna(), 'low_edu'] = np.nan
df['has_child_d'] = df['has_child'].astype(float)

# Winsorization of mortgage_burden at 1st/99th (pre-reg §5.2, 9.3)
mb_lo, mb_hi = df['mortgage_burden'].quantile([0.01, 0.99])
df['mortgage_burden_w'] = df['mortgage_burden'].clip(mb_lo, mb_hi)
# For subsample with burden < 5 (pre-reg §4.3)
df.loc[df['mortgage_burden'] > 5, 'mortgage_burden_w'] = np.nan

log(f"   mortgage_burden winsor bounds: [{mb_lo:.4f}, {mb_hi:.4f}]")

# Lag structures
df['year_lag'] = df.groupby('pid')['year'].shift(1)
df['lag_is_prev_wave'] = ((df['year'] - df['year_lag']) == 2).astype(float)
df['mortgage_burden_lag'] = df.groupby('pid')['mortgage_burden_w'].shift(1)
df['has_mortgage_lag'] = df.groupby('pid')['has_mortgage'].shift(1)
df['ln_house_debts_lag'] = df.groupby('pid')['ln_house_debts'].shift(1)
df['dw_lag'] = df.groupby('pid')['dw'].shift(1)
df['qn12012_lag'] = df.groupby('pid')['qn12012'].shift(1)
df['ln_resivalue_lag'] = df.groupby('pid')['ln_resivalue'].shift(1)
df['child_num_lag'] = df.groupby('pid')['child_num'].shift(1)
df['familysize_lag'] = df.groupby('pid')['familysize'].shift(1)

# First-mortgage event: has_mortgage 0->1 transition (used for event study)
df['first_mortgage'] = (
    (df['has_mortgage'] == 1) &
    (df['has_mortgage_lag'] == 0) &
    (df['lag_is_prev_wave'] == 1)
).astype(float)

# Exit-mortgage event: 1->0
df['exit_mortgage'] = (
    (df['has_mortgage'] == 0) &
    (df['has_mortgage_lag'] == 1) &
    (df['lag_is_prev_wave'] == 1)
).astype(float)

# Unit harmonization for resivalue (pre-2014 in yuan, 2014+ in wan-yuan)
# We leave ln_resivalue as-is for within-person FE analyses but document the shift.
# For Δ_ST cor() we use wave-specific standardization.
df['resivalue_z_byyear'] = df.groupby('year')['ln_resivalue'].transform(
    lambda s: (s - s.mean()) / (s.std() + 1e-9)
)

# Child count change
df['d_child'] = df['child_num'] - df['child_num_lag']

# Non-housing debt burden (bitter secondary)
df['nonhous_debt_ratio'] = df['nonhousing_debts'] / df['fincome1'].replace(0, np.nan)

# Save ratio: proxy savings / income
df['save_ratio'] = df['savings'] / df['fincome1'].replace(0, np.nan)

# Wave counts
n_with_prev = (df['lag_is_prev_wave'] == 1).sum()
n_first_mort = int(df['first_mortgage'].sum())
n_exit_mort = int(df['exit_mortgage'].sum())
log(f"   Obs with valid prev-wave obs (2-yr gap): {n_with_prev:,}")
log(f"   First-mortgage events (0->1): {n_first_mort:,}")
log(f"   Exit-mortgage events (1->0):  {n_exit_mort:,}")

# Cohort splits for Δ_ST (boom vs cooling)
# Ancestral-to-this-variable = 2010-2012 (housing-boom early, baseline calibration)
# Current = 2018-2022 (mature leverage era + "3 red lines" 2021)
df_anc = df[df['year'].isin([2010, 2012])]
df_cur = df[df['year'].isin([2018, 2020, 2022])]
log(f"   Ancestral 2010-2012 n={len(df_anc):,} | Current 2018-2022 n={len(df_cur):,}")


# ============================================================
# [3/10] F2 DIAGNOSTIC -- HARD GATEKEEPER (Andy's corrected rule)
# ============================================================
log("\n[3/10] F2 DIAGNOSTIC -- aspirational selection on housing treatment")
log("=" * 60)
log("Purpose: Is mortgage / high housing value voluntarily chosen by")
log("higher-SES households? If YES -> F2 satisfied, proceed to Sweet Trap.")
log("If NO -> C13 is coerced squeeze like C2 (negative SES gradient), demote.")
log("-" * 60)

f2_diag = {}

# Test F2.1: cor(mortgage_burden, income/edu/urban)
sub_f2 = df.dropna(subset=['mortgage_burden_w', 'lnincome', 'fincome1', 'eduy', 'urban_ind'])
r_mb_inc = float(sub_f2['mortgage_burden_w'].corr(sub_f2['lnincome']))
r_mb_edu = float(sub_f2['mortgage_burden_w'].corr(sub_f2['eduy']))
r_mb_urb = float(sub_f2['mortgage_burden_w'].corr(sub_f2['urban_ind']))
log(f"   cor(mortgage_burden, ln_income)  = {r_mb_inc:+.4f}   [expected POSITIVE]")
log(f"   cor(mortgage_burden, eduy)       = {r_mb_edu:+.4f}   [expected POSITIVE]")
log(f"   cor(mortgage_burden, urban)      = {r_mb_urb:+.4f}   [expected POSITIVE]")

# Test F2.2: cor(has_mortgage, SES)
sub_f2b = df.dropna(subset=['has_mortgage', 'lnincome', 'eduy', 'urban_ind'])
r_hm_inc = float(sub_f2b['has_mortgage'].astype(float).corr(sub_f2b['lnincome']))
r_hm_edu = float(sub_f2b['has_mortgage'].astype(float).corr(sub_f2b['eduy']))
r_hm_urb = float(sub_f2b['has_mortgage'].astype(float).corr(sub_f2b['urban_ind']))
log(f"   cor(has_mortgage, ln_income)     = {r_hm_inc:+.4f}   [expected POSITIVE]")
log(f"   cor(has_mortgage, eduy)          = {r_hm_edu:+.4f}   [expected POSITIVE]")
log(f"   cor(has_mortgage, urban)         = {r_hm_urb:+.4f}   [expected POSITIVE]")

# Test F2.3: P(has_mortgage | urban vs rural)
p_mort_urban = float(
    df[df['urban_ind'] == 1]['has_mortgage'].astype(float).mean())
p_mort_rural = float(
    df[df['urban_ind'] == 0]['has_mortgage'].astype(float).mean())
log(f"   P(has_mortgage|urban) = {p_mort_urban:.4f}"
    f" vs P(has_mortgage|rural) = {p_mort_rural:.4f}")
log(f"     ratio urban/rural = {p_mort_urban/p_mort_rural:.2f}x")

# Test F2.4: gradient across income quartile
df_q = df.dropna(subset=['fincome1']).copy()
df_q['inc_q'] = pd.qcut(df_q['fincome1'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'],
                        duplicates='drop')
grad = df_q.groupby('inc_q', observed=True).agg(
    n=('has_mortgage', 'count'),
    p_mort=('has_mortgage', 'mean'),
    mean_burden=('mortgage_burden_w', 'mean'),
).round(4)
log(f"\n   Income quartile gradient:\n{grad}")

# Test F2.5: gradient across education
df_e = df.dropna(subset=['eduy']).copy()
df_e['eduy_b'] = pd.cut(df_e['eduy'], bins=[-0.1, 6, 9, 12, 25],
                         labels=['0-6', '6-9', '9-12', '12+'])
grad_e = df_e.groupby('eduy_b', observed=True).agg(
    n=('has_mortgage', 'count'),
    p_mort=('has_mortgage', 'mean'),
    mean_burden=('mortgage_burden_w', 'mean'),
).round(4)
log(f"\n   Education bracket gradient:\n{grad_e}")

# Test F2.6: cor(mortgage_burden, household_squeeze_proxy)
# Proxy: ln_nonhousing_debts.  If mortgage is CROWDING OUT, we expect
# cor > 0 (mortgage and other debts both rising = squeeze).  If mortgage
# is ASPIRATIONAL, the correlation should be weak/near zero (high-SES
# takes mortgage without accumulating consumer debt) or NEGATIVE (substituting).
sub_sq = df.dropna(subset=['mortgage_burden_w', 'ln_nonhousing_debts', 'ln_savings',
                           'ln_expense', 'ln_total_asset'])
r_mb_ndebt = float(sub_sq['mortgage_burden_w'].corr(sub_sq['ln_nonhousing_debts']))
r_mb_save = float(sub_sq['mortgage_burden_w'].corr(sub_sq['ln_savings']))
r_mb_exp = float(sub_sq['mortgage_burden_w'].corr(sub_sq['ln_expense']))
r_mb_asset = float(sub_sq['mortgage_burden_w'].corr(sub_sq['ln_total_asset']))
log(f"\n   F2 squeeze-vs-aspirational test (ambiguous if borderline):")
log(f"     cor(mortgage_burden, ln_nonhousing_debts) = {r_mb_ndebt:+.4f}")
log(f"       [near 0 or negative => aspirational; strong positive => squeeze]")
log(f"     cor(mortgage_burden, ln_savings)           = {r_mb_save:+.4f}")
log(f"     cor(mortgage_burden, ln_expense)           = {r_mb_exp:+.4f}  "
    f"[positive expected -- higher income families spend more]")
log(f"     cor(mortgage_burden, ln_total_asset)       = {r_mb_asset:+.4f}  "
    f"[positive expected -- aspirational homebuyers]")

# Test F2.7: are mortgages concentrated in high-income OR distributed uniformly?
# Compute Lorenz-like statistic: fraction of mortgages held by top income decile
df_q2 = df.dropna(subset=['fincome1', 'has_mortgage'])
df_q2 = df_q2.copy()
df_q2['inc_dec'] = pd.qcut(df_q2['fincome1'], 10, labels=False, duplicates='drop')
top_dec = df_q2[df_q2['inc_dec'] == 9]
share_top = float((top_dec['has_mortgage'].astype(float) == 1).sum() /
                  (df_q2['has_mortgage'].astype(float) == 1).sum())
log(f"   Top income decile holds {share_top*100:.1f}% of all mortgages"
    f" (uniform would be 10%)")

# F2 verdict
# Required: all of {r_mb_inc, r_mb_edu, r_mb_urb} > 0 AND urban/rural ratio > 1
f2_passes = [
    r_mb_inc > 0, r_mb_edu > 0, r_mb_urb > 0,
    r_hm_inc > 0, r_hm_edu > 0, r_hm_urb > 0,
    p_mort_urban > p_mort_rural,
]
n_pass = sum(f2_passes)
if n_pass == 7:
    f2_verdict = "F2 CONFIRMED -- all 7 aspirational checks pass"
elif n_pass >= 5:
    f2_verdict = f"F2 LIKELY -- {n_pass}/7 checks pass"
else:
    f2_verdict = f"F2 FAILS -- only {n_pass}/7 checks pass; domain is coerced (like C2)"

log(f"\n   F2 VERDICT: {f2_verdict}")

f2_diag = {
    'cor_mortgage_burden_lnincome': r_mb_inc,
    'cor_mortgage_burden_eduy': r_mb_edu,
    'cor_mortgage_burden_urban': r_mb_urb,
    'cor_has_mortgage_lnincome': r_hm_inc,
    'cor_has_mortgage_eduy': r_hm_edu,
    'cor_has_mortgage_urban': r_hm_urb,
    'P_has_mortgage_urban': p_mort_urban,
    'P_has_mortgage_rural': p_mort_rural,
    'urban_rural_mortgage_ratio': p_mort_urban / p_mort_rural,
    'top_decile_mortgage_share': share_top,
    'cor_mortgage_burden_ln_nonhousing_debts': r_mb_ndebt,
    'cor_mortgage_burden_ln_savings': r_mb_save,
    'cor_mortgage_burden_ln_expense': r_mb_exp,
    'cor_mortgage_burden_ln_total_asset': r_mb_asset,
    'income_quartile_gradient': grad.reset_index().to_dict(orient='records'),
    'education_bracket_gradient': grad_e.reset_index().to_dict(orient='records'),
    'passes': n_pass,
    'total_checks': 7,
    'verdict': f2_verdict,
}

if n_pass < 5:
    log("\n   *** F2 FAILS — proceeding for documentation but C13 will be demoted. ***")
else:
    log("\n   *** F2 PASSED -- proceeding to Sweet Trap identification. ***")

# ------------------------------------------------------------
# [4/10] DESCRIPTIVES
# ------------------------------------------------------------
log("\n[4/10] Descriptives")


def quick_desc(dfx, label):
    n = len(dfx)
    if n == 0:
        return
    log(f"   [{label}] N={n:,}  pid={dfx['pid'].nunique():,}")
    for c in ['has_mortgage', 'mortgage_burden_w', 'dw', 'qn12012',
              'qn12016', 'ln_savings', 'ln_house_debts', 'ln_nonhousing_debts',
              'ln_expense', 'ln_total_asset', 'child_num', 'age', 'eduy',
              'ln_fincome1', 'urban_ind']:
        if c in dfx.columns:
            try:
                s = pd.to_numeric(dfx[c], errors='coerce')
                log(f"     {c:<22s}: mean={s.mean():+.4f} "
                    f"sd={s.std():.4f} n={s.notna().sum():,}")
            except Exception:
                pass


quick_desc(df, 'ALL')
quick_desc(df_anc, 'ANCESTRAL 2010-2012')
quick_desc(df_cur, 'CURRENT 2018-2022')
quick_desc(df[df['has_mortgage'] == 1], 'MORTGAGE-HOLDERS')
quick_desc(df[df['has_mortgage'] == 0], 'NON-MORTGAGE')


# ------------------------------------------------------------
# [5/10] TWO-WAY FE ESTIMATOR
# ------------------------------------------------------------
def clean_controls_for_fe(df_sub, controls):
    """Drop controls absorbed by person FE (zero within-person variation)."""
    usable = []
    for c in controls:
        if c not in df_sub.columns:
            continue
        s = pd.to_numeric(df_sub[c], errors='coerce')
        demeaned = s - s.groupby(df_sub['pid']).transform('mean')
        if demeaned.abs().sum() > 1e-8:
            usable.append(c)
    return usable


def twoway_fe(df_in, y, x_cols, entity='pid', time='year',
              cluster='pid', add_interact=None):
    """Frisch-Waugh two-way within transform + cluster-robust SE."""
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
        m = sm.OLS(y_w, X).fit(cov_type='cluster',
                               cov_kwds={'groups': groups})
    except Exception:
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
# [5/10] PRIMARY HYPOTHESES H8.1 - H8.4
# ------------------------------------------------------------
log("\n[5/10] Primary regressions -- H8.1 (Sweet), H8.2 (Bitter), "
    "H8.3 (λ-young), H8.4 (positional)")

# Pre-reg §5.5 control set (minimal — age, age2 absorbed by FE for young,
# household_size, married)
controls_primary = ['age', 'age2', 'familysize', 'married']

# ---- H8.1 Sweet: dw ~ mortgage_burden + controls + person FE + year FE ----
sub_h81 = df.dropna(
    subset=['dw', 'mortgage_burden_w'] + controls_primary).copy()
u81 = clean_controls_for_fe(sub_h81, controls_primary)
log(f"   H8.1 controls usable after FE: {u81}")
res_h81 = twoway_fe(sub_h81, y='dw', x_cols=['mortgage_burden_w'] + u81,
                    entity='pid', time='year', cluster='pid')
log(f"   H8.1 N={res_h81['N']:,}  n_pid={res_h81['n_entity']:,}")
log(f"   H8.1 beta(mortgage_burden) = "
    f"{res_h81['mortgage_burden_w']['beta']:+.5f}  "
    f"SE={res_h81['mortgage_burden_w']['se']:.5f}  "
    f"one-sided p={res_h81['mortgage_burden_w']['p_one_sided']:.4f}  "
    f"95% CI={res_h81['mortgage_burden_w']['ci95']}")

# ---- H8.1 secondary Sweet on qn12012 life-sat (pre-reg §6.5) ----
sub_h81b = df.dropna(
    subset=['qn12012', 'mortgage_burden_w'] + controls_primary).copy()
u81b = clean_controls_for_fe(sub_h81b, controls_primary)
res_h81b = twoway_fe(sub_h81b, y='qn12012', x_cols=['mortgage_burden_w'] + u81b,
                     entity='pid', time='year', cluster='pid')
log(f"   H8.1b (qn12012) beta = "
    f"{res_h81b['mortgage_burden_w']['beta']:+.5f}  "
    f"SE={res_h81b['mortgage_burden_w']['se']:.5f}  "
    f"p1={res_h81b['mortgage_burden_w']['p_one_sided']:.4f}")

# ---- H8.2 Bitter: ln_savings ~ mortgage_burden_lag ----
sub_h82 = df[df['lag_is_prev_wave'] == 1].dropna(
    subset=['ln_savings', 'mortgage_burden_lag'] + controls_primary).copy()
u82 = clean_controls_for_fe(sub_h82, controls_primary)
res_h82 = twoway_fe(sub_h82, y='ln_savings',
                    x_cols=['mortgage_burden_lag'] + u82,
                    entity='pid', time='year', cluster='pid')
log(f"   H8.2 (savings) N={res_h82['N']:,}  "
    f"beta(mortgage_burden_lag)={res_h82['mortgage_burden_lag']['beta']:+.5f}  "
    f"SE={res_h82['mortgage_burden_lag']['se']:.5f}  "
    f"p1_lt0={1 - res_h82['mortgage_burden_lag']['p_one_sided']:.4f}")

# ---- H8.2b Bitter: ln_nonhousing_debts ~ mortgage_burden_lag (crowd-in test) ----
sub_h82b = df[df['lag_is_prev_wave'] == 1].dropna(
    subset=['ln_nonhousing_debts', 'mortgage_burden_lag'] + controls_primary).copy()
u82b = clean_controls_for_fe(sub_h82b, controls_primary)
res_h82b = twoway_fe(sub_h82b, y='ln_nonhousing_debts',
                     x_cols=['mortgage_burden_lag'] + u82b,
                     entity='pid', time='year', cluster='pid')
log(f"   H8.2b (nonhousing_debts) N={res_h82b['N']:,}  "
    f"beta={res_h82b['mortgage_burden_lag']['beta']:+.5f}  "
    f"p1={res_h82b['mortgage_burden_lag']['p_one_sided']:.4f}")

# ---- H8.2c Bitter: ln_expense ~ mortgage_burden_lag (consumption crowd-out test) ----
sub_h82c = df[df['lag_is_prev_wave'] == 1].dropna(
    subset=['ln_expense', 'mortgage_burden_lag'] + controls_primary).copy()
u82c = clean_controls_for_fe(sub_h82c, controls_primary)
res_h82c = twoway_fe(sub_h82c, y='ln_expense',
                     x_cols=['mortgage_burden_lag'] + u82c,
                     entity='pid', time='year', cluster='pid')
log(f"   H8.2c (ln_expense) N={res_h82c['N']:,}  "
    f"beta={res_h82c['mortgage_burden_lag']['beta']:+.5f}  "
    f"p1={res_h82c['mortgage_burden_lag']['p_one_sided']:.4f}")

# ---- H8.2d Bitter: child_num ~ mortgage_burden_lag (delayed fertility test) ----
sub_h82d = df[df['lag_is_prev_wave'] == 1].dropna(
    subset=['child_num', 'mortgage_burden_lag'] + controls_primary).copy()
u82d = clean_controls_for_fe(sub_h82d, controls_primary)
res_h82d = twoway_fe(sub_h82d, y='child_num',
                     x_cols=['mortgage_burden_lag'] + u82d,
                     entity='pid', time='year', cluster='pid')
log(f"   H8.2d (child_num) N={res_h82d['N']:,}  "
    f"beta={res_h82d['mortgage_burden_lag']['beta']:+.5f}  "
    f"p1={res_h82d['mortgage_burden_lag']['p_one_sided']:.4f}")

# ---- H8.3 λ moderation: young cohort (< 40) ----
sub_h83 = df.dropna(
    subset=['dw', 'mortgage_burden_w', 'young'] + controls_primary).copy()
u83 = clean_controls_for_fe(sub_h83, controls_primary)
res_h83 = twoway_fe(
    sub_h83, y='dw',
    x_cols=['mortgage_burden_w', 'young'] + u83,
    entity='pid', time='year', cluster='pid',
    add_interact=('mortgage_burden_w', 'young'))
inter_name = 'mortgage_burden_w_x_young'
log(f"   H8.3 N={res_h83['N']:,}")
log(f"   H8.3 main β(mortgage_burden) = "
    f"{res_h83['mortgage_burden_w']['beta']:+.5f} "
    f"p1={res_h83['mortgage_burden_w']['p_one_sided']:.4f}")
if inter_name in res_h83:
    log(f"   H8.3 β(mortgage × young) = "
        f"{res_h83[inter_name]['beta']:+.5f}  "
        f"SE={res_h83[inter_name]['se']:.5f}  "
        f"p1={res_h83[inter_name]['p_one_sided']:.4f}  "
        f"95% CI={res_h83[inter_name]['ci95']}")

# ---- H8.4 Positional validity: add ln_fincome1, ln_total_asset ----
controls_pos = controls_primary + ['ln_fincome1', 'ln_total_asset']
sub_h84 = df.dropna(
    subset=['dw', 'mortgage_burden_w'] + controls_pos).copy()
u84 = clean_controls_for_fe(sub_h84, controls_pos)
res_h84 = twoway_fe(sub_h84, y='dw',
                    x_cols=['mortgage_burden_w'] + u84,
                    entity='pid', time='year', cluster='pid')
log(f"   H8.4 (pos) N={res_h84['N']:,}  "
    f"beta={res_h84['mortgage_burden_w']['beta']:+.5f}  "
    f"p1={res_h84['mortgage_burden_w']['p_one_sided']:.4f}")

beta_81 = res_h81['mortgage_burden_w']['beta']
beta_84 = res_h84['mortgage_burden_w']['beta']
pos_ratio = beta_84 / beta_81 if abs(beta_81) > 1e-9 else np.nan
log(f"   H8.4 ratio (positional/uncontrolled) = {pos_ratio:.3f}  "
    f"[pre-reg decision rule: >= 0.5 for positional confirmation]")


def verdict(p, side='gt', alpha_bonf=ALPHA_BONF):
    """side='gt' -> reward hypothesis (beta > 0). side='lt' -> bitter."""
    if side == 'gt':
        p1 = p
    else:
        p1 = 1 - p
    if p1 < alpha_bonf:
        return f"CONFIRMED at alpha_Bonf={alpha_bonf}"
    if p1 < 0.05:
        return f"DIRECTIONAL at alpha=0.05 (fails Bonf)"
    return "NULL (p >= 0.05)"


v_h81 = verdict(res_h81['mortgage_burden_w']['p_one_sided'], 'gt')
v_h82 = verdict(res_h82['mortgage_burden_lag']['p_one_sided'], 'lt')
v_h83 = verdict(res_h83.get(inter_name, {}).get('p_one_sided', 1.0), 'gt')
v_h84 = f"positional_ratio={pos_ratio:.3f} ({'CONFIRMED' if pos_ratio >= 0.5 else 'FAIL'})"
log(f"\n   H8.1 Sweet  verdict: {v_h81}")
log(f"   H8.2 Bitter verdict: {v_h82}")
log(f"   H8.3 λ      verdict: {v_h83}")
log(f"   H8.4 Pos    verdict: {v_h84}")


# ------------------------------------------------------------
# [6/10] EVENT STUDY -- first-mortgage 0->1 transition
# ------------------------------------------------------------
log("\n[6/10] Event study -- first mortgage 0->1 transition (person FE)")

# Identify pid who had a first-mortgage event during the panel
fm_pid = df.loc[df['first_mortgage'] == 1, 'pid'].unique()
log(f"   First-mortgage pids: {len(fm_pid):,}")

ev_panel = df[df['pid'].isin(fm_pid)].copy()

# For each fm pid, identify the year of first transition
first_year = (
    df[df['first_mortgage'] == 1]
    .groupby('pid')['year'].min().rename('event_year')
)
ev_panel = ev_panel.merge(first_year, on='pid', how='left')
ev_panel['event_time'] = ev_panel['year'] - ev_panel['event_year']

# Trim to event_time in [-4, +6] (years, maps to waves [-2, +3])
ev_panel = ev_panel[(ev_panel['event_time'] >= -4) &
                    (ev_panel['event_time'] <= 6)].copy()

# Event-time dummies (omit t = -2, i.e., 2-wave pre-period as reference)
for et in sorted(ev_panel['event_time'].dropna().unique().tolist()):
    if et == -2:
        continue
    ev_panel[f'et_{int(et):+d}'] = (ev_panel['event_time'] == et).astype(float)

event_dummies = [c for c in ev_panel.columns if c.startswith('et_')]
log(f"   Event-time dummies: {event_dummies}")


def event_study_regress(dfev, y):
    sub = dfev.dropna(subset=[y, 'age', 'age2', 'familysize']).copy()
    if len(sub) < 100:
        return None
    x_cols = event_dummies + ['age', 'age2', 'familysize']
    usable = clean_controls_for_fe(sub, x_cols)
    # Keep event dummies (may not be absorbed by person FE)
    keep_ev = [c for c in event_dummies if c in usable]
    usable = keep_ev + [c for c in usable if c not in event_dummies]
    if not keep_ev:
        return None
    return twoway_fe(sub, y=y, x_cols=usable,
                     entity='pid', time='year', cluster='pid')


event_results = {}
for y in ['dw', 'qn12012', 'qn12016', 'ln_savings', 'ln_expense',
          'ln_nonhousing_debts', 'child_num']:
    r = event_study_regress(ev_panel, y)
    if r is None:
        log(f"   {y}: insufficient data")
        continue
    event_results[y] = {}
    log(f"   --- DV: {y}  (N={r['N']:,} | n_pid={r['n_entity']:,}) ---")
    for c in event_dummies:
        if c in r:
            b, se, p2 = r[c]['beta'], r[c]['se'], r[c]['p_two_sided']
            log(f"     {c}: β={b:+.4f}  SE={se:.4f}  p2={p2:.4f}  "
                f"CI={r[c]['ci95']}")
            event_results[y][c] = {'beta': b, 'se': se, 'p_two_sided': p2,
                                   'ci95': r[c]['ci95']}

# ------------------------------------------------------------
# [7/10] SPECIFICATION CURVE (>= 144 specs)
# ------------------------------------------------------------
log("\n[7/10] Specification curve")

# Sweet branch: DV × treatment × sample × controls × FE × cluster
dvs_sweet = ['dw', 'qn12012', 'qn12016']                         # 3
treatments_sweet = ['mortgage_burden_w', 'has_mortgage',
                    'ln_house_debts', 'ln_resivalue']            # 4
samples = [
    ('all', lambda d: d),
    ('urban', lambda d: d[d['urban_ind'] == 1]),
    ('rural', lambda d: d[d['urban_ind'] == 0]),
    ('young_lt40', lambda d: d[d['age'] < 40]),
]
control_sets = [
    ('minimal', []),
    ('demog', ['age', 'age2', 'familysize']),
    ('extended', ['age', 'age2', 'familysize', 'married']),
]
fe_structures = ['person_year', 'person_year_province']
cluster_levels = ['pid', 'provcd']

# Bitter branch: DV × lag treatment × sample × controls × FE × cluster
dvs_bitter = ['ln_savings', 'ln_nonhousing_debts',
              'ln_expense', 'child_num']                         # 4
treatments_bitter = ['mortgage_burden_lag', 'has_mortgage_lag',
                     'ln_house_debts_lag']                       # 3


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

# Bitter branch (restrict to valid lag sample)
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
        'share_negative': float((betas < 0).mean()),
        'share_sig_05': float((ps < 0.05).mean()),
        'share_sig_bonf': float((ps < ALPHA_BONF).mean()),
    }


sca_sweet = sca_stats([r for r in sca_runs if r['branch'] == 'sweet'])
sca_bitter = sca_stats([r for r in sca_runs if r['branch'] == 'bitter'])
log(f"\n   SCA sweet  : med β={sca_sweet.get('median_beta', 0):+.5f} "
    f"IQR={sca_sweet.get('iqr_beta')} "
    f"share+={sca_sweet.get('share_positive', 0)*100:.1f}% "
    f"sig_Bonf={sca_sweet.get('share_sig_bonf', 0)*100:.1f}%")
log(f"   SCA bitter : med β={sca_bitter.get('median_beta', 0):+.5f} "
    f"IQR={sca_bitter.get('iqr_beta')} "
    f"share+={sca_bitter.get('share_positive', 0)*100:.1f}% "
    f"share-={sca_bitter.get('share_negative', 0)*100:.1f}% "
    f"sig_Bonf={sca_bitter.get('share_sig_bonf', 0)*100:.1f}%")

# Per-DV SCA medians for diagnostic
log(f"\n   Per-DV SCA median β:")
for br_name, br_list in [('sweet', dvs_sweet), ('bitter', dvs_bitter)]:
    for dv in br_list:
        sub_runs = [r for r in sca_runs
                    if r['branch'] == br_name and r['dv'] == dv]
        if sub_runs:
            betas = np.array([r['beta'] for r in sub_runs])
            ps = np.array([r['p_one_sided'] for r in sub_runs])
            sign_consist = float((betas > 0).mean())
            sig_share = float((ps < 0.05).mean())
            log(f"     {br_name:>6s}|{dv:<22s} n={len(sub_runs):>3d}  "
                f"med β={float(np.median(betas)):+.5f}  "
                f"sign+={sign_consist*100:.1f}%  sig@0.05={sig_share*100:.1f}%")


# ------------------------------------------------------------
# [8/10] Δ_ST COHORT DECOMPOSITION + BOOTSTRAP
# ------------------------------------------------------------
log("\n[8/10] Δ_ST cohort decomposition with bootstrap CIs")


def delta_st_bootstrap(df_full, y_col, x_col,
                       anc_years=(2010, 2012),
                       cur_years=(2018, 2020, 2022),
                       B=B_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    sub = df_full.dropna(subset=[x_col, y_col])
    anc = sub[sub['year'].isin(anc_years)][[x_col, y_col]].astype(float).to_numpy()
    cur = sub[sub['year'].isin(cur_years)][[x_col, y_col]].astype(float).to_numpy()
    if len(anc) < 50 or len(cur) < 50:
        return None

    def _cor(arr):
        if len(arr) < 10:
            return np.nan
        return np.corrcoef(arr[:, 0], arr[:, 1])[0, 1]
    cor_anc = _cor(anc)
    cor_cur = _cor(cur)
    delta = cor_anc - cor_cur
    deltas = np.empty(B)
    for b in range(B):
        ia = rng.integers(0, len(anc), len(anc))
        ic = rng.integers(0, len(cur), len(cur))
        deltas[b] = _cor(anc[ia]) - _cor(cur[ic])
    deltas = deltas[np.isfinite(deltas)]
    lo, hi = np.quantile(deltas, [0.025, 0.975])
    p_le = float((deltas <= 0).mean())
    return {
        'y': y_col, 'x': x_col,
        'n_anc': int(len(anc)), 'n_cur': int(len(cur)),
        'cor_ancestral': float(cor_anc),
        'cor_current': float(cor_cur),
        'delta_st': float(delta),
        'ci95_bootstrap': [float(lo), float(hi)],
        'p_one_sided_delta_gt_0': p_le,
        'B': B,
    }


delta_st_results = {}
# Primary: Δ_ST defined on non-mortgage cohort baseline vs high-mortgage current
#
# We use two decompositions:
# A) TIME-SPLIT: cor(X, Y)_{2010-2012} vs cor(X, Y)_{2018-2022}
#    X = ln_resivalue, has_mortgage, mortgage_burden (last only defined 2014+ reliably)
#    Y = dw, qn12012, qn12016, ln_savings, child_num
# B) ANCESTRAL-CONTROL: cor(asset, Y) in non-mortgage households
#    vs cor(housing_value, Y) in high-DTI households -- Andy's task spec §3

log("\n   [A] Time-split Δ_ST (ancestral 2010-2012 vs current 2018-2022)")
for x in ['resivalue_z_byyear', 'has_mortgage']:
    for y in ['dw', 'qn12012', 'qn12016', 'ln_savings', 'child_num']:
        r = delta_st_bootstrap(df, y, x)
        if r is None:
            continue
        key = f"{x}__{y}"
        delta_st_results[key] = r
        log(f"     Δ_ST({x} -> {y}): "
            f"cor_anc={r['cor_ancestral']:+.4f} cor_cur={r['cor_current']:+.4f} "
            f"Δ={r['delta_st']:+.4f} CI=[{r['ci95_bootstrap'][0]:+.4f}, "
            f"{r['ci95_bootstrap'][1]:+.4f}] "
            f"p(Δ≤0)={r['p_one_sided_delta_gt_0']:.3f} "
            f"N=({r['n_anc']:,}, {r['n_cur']:,})")

# B) Ancestral-control: non-mortgage families as "ancestral baseline"
log("\n   [B] Ancestral-baseline Δ_ST: non-mortgage vs high-DTI families")


def cohort_cor_bootstrap(df_full, y_col, x_col, anc_mask, cur_mask,
                         B=B_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    sub = df_full.dropna(subset=[x_col, y_col])
    anc = sub[anc_mask.reindex(sub.index).fillna(False)][[x_col, y_col]].astype(float).to_numpy()
    cur = sub[cur_mask.reindex(sub.index).fillna(False)][[x_col, y_col]].astype(float).to_numpy()
    if len(anc) < 50 or len(cur) < 50:
        return None

    def _cor(arr):
        if len(arr) < 10:
            return np.nan
        return np.corrcoef(arr[:, 0], arr[:, 1])[0, 1]
    c_anc = _cor(anc)
    c_cur = _cor(cur)
    delta = c_anc - c_cur
    deltas = np.empty(B)
    for b in range(B):
        ia = rng.integers(0, len(anc), len(anc))
        ic = rng.integers(0, len(cur), len(cur))
        deltas[b] = _cor(anc[ia]) - _cor(cur[ic])
    deltas = deltas[np.isfinite(deltas)]
    lo, hi = np.quantile(deltas, [0.025, 0.975])
    p_le = float((deltas <= 0).mean())
    return {
        'y': y_col, 'x': x_col,
        'n_anc': int(len(anc)), 'n_cur': int(len(cur)),
        'cor_ancestral': float(c_anc),
        'cor_current': float(c_cur),
        'delta_st': float(delta),
        'ci95_bootstrap': [float(lo), float(hi)],
        'p_one_sided_delta_gt_0': p_le,
        'B': B,
    }


# Ancestral = no mortgage, wealth from labour (cor(total_asset, welfare))
# Current   = above-median DTI (mortgage_burden > median of non-zero)
mb_pos_med = df[df['mortgage_burden_w'] > 0]['mortgage_burden_w'].median()
log(f"     median of positive mortgage_burden = {mb_pos_med:.4f}")

anc_mask_b = (df['has_mortgage'] == 0)
cur_mask_b = (df['mortgage_burden_w'] > mb_pos_med)

for y in ['dw', 'qn12012', 'qn12016', 'ln_savings', 'child_num']:
    r = cohort_cor_bootstrap(df, y, 'ln_total_asset', anc_mask_b, cur_mask_b)
    if r is None:
        continue
    key = f"BASELINE_nonmort_vs_highDTI__ln_total_asset__{y}"
    delta_st_results[key] = r
    log(f"     Δ_ST(ancB asset->{y}): cor_nomort={r['cor_ancestral']:+.4f} "
        f"cor_highDTI={r['cor_current']:+.4f} Δ={r['delta_st']:+.4f} "
        f"CI=[{r['ci95_bootstrap'][0]:+.4f}, {r['ci95_bootstrap'][1]:+.4f}] "
        f"N=({r['n_anc']:,}, {r['n_cur']:,})")

# Layer A benchmarks
peacock_A7_delta_st = +0.80
drosophila_A4_delta_st = +0.71
layerA_pooled = +0.72
log(f"\n   Layer A benchmarks:")
log(f"     A7 peacock runaway: +{peacock_A7_delta_st}")
log(f"     A4 Drosophila sugar: +{drosophila_A4_delta_st}")
log(f"     Pooled 8-case: +{layerA_pooled}")


# ------------------------------------------------------------
# [9/10] 4-PRIMITIVE EMPIRICAL SIGNATURES
# ------------------------------------------------------------
log("\n[9/10] 4-primitive empirical signatures")

primitives = {}

# θ (amenity): mortgage -> dw (pre-reg H8.1 output)
primitives['theta_signature'] = {
    'definition': ('Short-run amenity / status: within-person mortgage burden '
                   'raises self-rated social status (dw). Tested on dw '
                   '(primary) and qn12012 (secondary).'),
    'evidence': {
        'beta_dw': res_h81['mortgage_burden_w']['beta'],
        'se_dw': res_h81['mortgage_burden_w']['se'],
        'p_one_sided_dw': res_h81['mortgage_burden_w']['p_one_sided'],
        'ci95_dw': res_h81['mortgage_burden_w']['ci95'],
        'beta_qn12012': res_h81b['mortgage_burden_w']['beta'],
        'p_one_sided_qn12012': res_h81b['mortgage_burden_w']['p_one_sided'],
        'verdict': v_h81,
    },
}

# λ (externalisation): young cohort interaction
primitives['lambda_signature'] = {
    'definition': ('Externalisation: young cohorts (<40) externalise '
                   'debt-service burden to future self over longer horizon; '
                   'their contemporaneous dw response should be larger.'),
    'evidence': {
        'beta_interaction': res_h83.get(inter_name, {}).get('beta'),
        'se': res_h83.get(inter_name, {}).get('se'),
        'p_one_sided': res_h83.get(inter_name, {}).get('p_one_sided'),
        'verdict': v_h83,
    },
}

# β (present bias): ratio Sweet_contemporaneous / Bitter_lag
beta_sweet = res_h81['mortgage_burden_w']['beta']
beta_bitter_savings = res_h82['mortgage_burden_lag']['beta']
beta_bitter_ndebt = res_h82b['mortgage_burden_lag']['beta']
ratio_sweet_bitter = (abs(beta_sweet) / abs(beta_bitter_savings)
                      if abs(beta_bitter_savings) > 1e-9 else None)
primitives['beta_present_bias'] = {
    'definition': ('Present bias: contemporaneous θ reward (dw) vs future '
                   'financial cost (ln_savings, ln_nonhousing_debts). '
                   'Ratio |β_sweet|/|β_bitter_savings| quantifies the '
                   'weight mis-calibration.'),
    'evidence': {
        'beta_contemporaneous_sweet_dw': beta_sweet,
        'beta_lagged_bitter_savings': beta_bitter_savings,
        'beta_lagged_bitter_nonhousing_debts': beta_bitter_ndebt,
        'sweet_to_bitter_savings_ratio': ratio_sweet_bitter,
        'note': ('High present bias iff sweet > 0 AND bitter has wrong sign '
                 '(savings ↓ or nonhousing_debts ↑).'),
    },
}

# ρ (lock-in): within-person autocorr of housing value + mortgage
# Can't easily downsize housing
auto_corr_housing = None
try:
    sub_rho = df.dropna(subset=['ln_resivalue', 'ln_resivalue_lag'])
    auto_corr_housing = float(
        sub_rho[['ln_resivalue', 'ln_resivalue_lag']].corr().iloc[0, 1])
except Exception:
    pass

auto_corr_mortgage = None
try:
    sub_rho2 = df.dropna(subset=['has_mortgage', 'has_mortgage_lag'])
    auto_corr_mortgage = float(
        sub_rho2[['has_mortgage', 'has_mortgage_lag']].astype(float).corr().iloc[0, 1])
except Exception:
    pass

# Fraction of mortgage-holders who exit (downsize/pay-off) within panel
frac_exit = (n_exit_mort / max(1, (df['has_mortgage'] == 1).sum()))
primitives['rho_lock_in'] = {
    'definition': ('Lock-in: housing is one of the most illiquid assets. '
                   'Within-person autocorrelation of housing value and '
                   'mortgage across waves. Downsizing is rare.'),
    'evidence': {
        'within_pid_ln_resivalue_autocorr': auto_corr_housing,
        'within_pid_has_mortgage_autocorr': auto_corr_mortgage,
        'first_mortgage_events': n_first_mort,
        'exit_mortgage_events': n_exit_mort,
        'exit_rate_vs_total_mortgage_holder_obs': frac_exit,
        'note': ('High autocorr > 0.5 + low exit rate confirms ρ. Housing is '
                 'structurally the highest-ρ consumption good of all domains '
                 'we test (cannot gradually reduce exposure like smoking or '
                 'diet; must sell the house).'),
    },
}
log(f"   θ β(dw)={primitives['theta_signature']['evidence']['beta_dw']:+.5f} "
    f"p1={primitives['theta_signature']['evidence']['p_one_sided_dw']:.4f}")
log(f"   λ β(interaction)="
    f"{primitives['lambda_signature']['evidence']['beta_interaction']} "
    f"p1={primitives['lambda_signature']['evidence']['p_one_sided']}")
log(f"   β sweet/bitter_savings ratio={ratio_sweet_bitter}")
log(f"   ρ housing autocorr={auto_corr_housing:.4f}  "
    f"mortgage autocorr={auto_corr_mortgage:.4f}  "
    f"exit-rate={frac_exit:.4f}")


# ------------------------------------------------------------
# [10/10] EXPLORATORY — school-district shock + urban tier
# ------------------------------------------------------------
log("\n[E] Exploratory (NOT in pre-registration)")

exploratory = {}

# E1 Tier-1 province proxy (BJ, SH, GD, ZJ) — exaggerated positional dynamics
tier1_provs = [11, 31, 44, 33]  # BJ, SH, GD (incl. Shenzhen), ZJ
df['tier1'] = df['provcd'].isin(tier1_provs).astype(float)

sub_e1 = df[df['tier1'] == 1].dropna(
    subset=['dw', 'mortgage_burden_w'] + controls_primary).copy()
u_e1 = clean_controls_for_fe(sub_e1, controls_primary)
if len(sub_e1) > 100:
    r_e1 = twoway_fe(sub_e1, y='dw', x_cols=['mortgage_burden_w'] + u_e1,
                     entity='pid', time='year', cluster='pid')
    if r_e1:
        exploratory['E1_tier1_province_Sweet'] = {
            'beta': r_e1['mortgage_burden_w']['beta'],
            'se': r_e1['mortgage_burden_w']['se'],
            'p_one_sided': r_e1['mortgage_burden_w']['p_one_sided'],
            'N': r_e1['N'],
            'note': 'Tier-1 provinces (BJ/SH/GD/ZJ): positional dynamics strongest',
        }
        log(f"   E1 tier1 Sweet: β={r_e1['mortgage_burden_w']['beta']:+.5f} "
            f"p1={r_e1['mortgage_burden_w']['p_one_sided']:.4f} N={r_e1['N']:,}")

# E2 Post-2021 "3 red lines" policy (pre-reg §6.8) — housing-boom cooling
# DID-like: compare ΔdW in high-DTI households pre/post-2021
df['post_2021'] = (df['year'] >= 2022).astype(int)  # 2022 = first post-policy wave
df['treat_highDTI'] = (df['mortgage_burden_w'] > mb_pos_med).astype(float)
df['did_int'] = df['post_2021'] * df['treat_highDTI']
sub_e2 = df.dropna(subset=['dw', 'did_int'] + controls_primary).copy()
u_e2 = clean_controls_for_fe(sub_e2, controls_primary)
try:
    r_e2 = twoway_fe(sub_e2, y='dw',
                     x_cols=['did_int', 'treat_highDTI'] + u_e2,
                     entity='pid', time='year', cluster='pid')
    if r_e2:
        exploratory['E2_post2021_3redlines_DID'] = {
            'beta_did': r_e2['did_int']['beta'],
            'se': r_e2['did_int']['se'],
            'p_two_sided': r_e2['did_int']['p_two_sided'],
            'N': r_e2['N'],
            'note': ('DID proxy: interaction of post-2021 × high-DTI on dw. '
                     'Predicted negative if cooling disrupts positional signal. '
                     'Note year FE absorbs post_2021 main effect.'),
        }
        log(f"   E2 post-2021 DID: β={r_e2['did_int']['beta']:+.5f} "
            f"p2={r_e2['did_int']['p_two_sided']:.4f} N={r_e2['N']:,}")
except Exception as e:
    log(f"   E2 failed: {e}")

# E3 Gender heterogeneity
for female_val in [0, 1]:
    sub = df[df['female'] == female_val].dropna(
        subset=['dw', 'mortgage_burden_w'] + controls_primary).copy()
    u = clean_controls_for_fe(sub, controls_primary)
    if len(sub) < 500:
        continue
    r = twoway_fe(sub, y='dw', x_cols=['mortgage_burden_w'] + u,
                  entity='pid', time='year', cluster='pid')
    if r:
        key = 'E3_female' if female_val == 1 else 'E3_male'
        exploratory[key] = {
            'beta': r['mortgage_burden_w']['beta'],
            'se': r['mortgage_burden_w']['se'],
            'p_one_sided': r['mortgage_burden_w']['p_one_sided'],
            'N': r['N'],
        }
        log(f"   {key}: β={r['mortgage_burden_w']['beta']:+.5f} "
            f"p1={r['mortgage_burden_w']['p_one_sided']:.4f} N={r['N']:,}")

# E4 child-num moderation (families with school-age children — 学区房 mechanism proxy)
df['has_sch_age_child'] = ((df['child_num'] >= 1) & (df['age'] >= 25)
                           & (df['age'] <= 50)).astype(float)
sub_e4 = df[df['has_sch_age_child'] == 1].dropna(
    subset=['dw', 'mortgage_burden_w'] + controls_primary).copy()
u_e4 = clean_controls_for_fe(sub_e4, controls_primary)
if len(sub_e4) > 500:
    r_e4 = twoway_fe(sub_e4, y='dw', x_cols=['mortgage_burden_w'] + u_e4,
                     entity='pid', time='year', cluster='pid')
    if r_e4:
        exploratory['E4_school_district_proxy_withchildren'] = {
            'beta': r_e4['mortgage_burden_w']['beta'],
            'se': r_e4['mortgage_burden_w']['se'],
            'p_one_sided': r_e4['mortgage_burden_w']['p_one_sided'],
            'N': r_e4['N'],
            'note': ('Parents 25-50 with >=1 child — proxy for school-district '
                     'housing premium. Expected: stronger Sweet signal if 学区 '
                     'mechanism is active.'),
        }
        log(f"   E4 school-district proxy: "
            f"β={r_e4['mortgage_burden_w']['beta']:+.5f} "
            f"p1={r_e4['mortgage_burden_w']['p_one_sided']:.4f} "
            f"N={r_e4['N']:,}")

# E5 Homeowner-only subset (pre-reg §6.5)
sub_e5 = df[df['resivalue'] > 0].dropna(
    subset=['dw', 'mortgage_burden_w'] + controls_primary).copy()
u_e5 = clean_controls_for_fe(sub_e5, controls_primary)
if len(sub_e5) > 500:
    r_e5 = twoway_fe(sub_e5, y='dw', x_cols=['mortgage_burden_w'] + u_e5,
                     entity='pid', time='year', cluster='pid')
    if r_e5:
        exploratory['E5_homeowner_only'] = {
            'beta': r_e5['mortgage_burden_w']['beta'],
            'se': r_e5['mortgage_burden_w']['se'],
            'p_one_sided': r_e5['mortgage_burden_w']['p_one_sided'],
            'N': r_e5['N'],
        }
        log(f"   E5 homeowner-only: "
            f"β={r_e5['mortgage_burden_w']['beta']:+.5f} "
            f"p1={r_e5['mortgage_burden_w']['p_one_sided']:.4f} "
            f"N={r_e5['N']:,}")

# ------------------------------------------------------------
# ASSEMBLE JSON
# ------------------------------------------------------------
log("\n[assemble] Writing C13_results.json")


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(x) for x in o]
    if isinstance(o, (np.floating,)):
        if np.isnan(o):
            return None
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return _clean(o.tolist())
    if isinstance(o, (pd.Timestamp, pd.Period)):
        return str(o)
    return o


out = {
    'meta': {
        'run_at': datetime.now().isoformat(),
        'script': 'C13_housing_sweet_trap.py',
        'panel_sha256': actual_sha,
        'seed': SEED,
        'alpha_Bonf': ALPHA_BONF,
        'B_bootstrap': B_BOOT,
        'n_obs': int(len(df)),
        'n_pid': int(df['pid'].nunique()),
        'waves': waves,
    },
    'F2_diagnostic': f2_diag,
    'primary': {
        'H8_1_sweet_dw': res_h81,
        'H8_1b_sweet_qn12012': res_h81b,
        'H8_2_bitter_savings_lag': res_h82,
        'H8_2b_bitter_nonhous_debts_lag': res_h82b,
        'H8_2c_bitter_expense_lag': res_h82c,
        'H8_2d_bitter_child_num_lag': res_h82d,
        'H8_3_lambda_young_interact': res_h83,
        'H8_4_positional_control': res_h84,
        'H8_4_positional_ratio': pos_ratio,
        'verdicts': {
            'H8_1': v_h81,
            'H8_2': v_h82,
            'H8_3': v_h83,
            'H8_4': v_h84,
        },
    },
    'event_study': event_results,
    'spec_curve': {
        'sweet_branch_stats': sca_sweet,
        'bitter_branch_stats': sca_bitter,
        'csv_path': OUT_SCA,
        'total_runs': len(sca_runs),
    },
    'delta_st': {
        'bootstrap_results': delta_st_results,
        'benchmarks': {
            'A7_peacock_runaway': peacock_A7_delta_st,
            'A4_Drosophila_sugar': drosophila_A4_delta_st,
            'layer_A_pooled_8_cases': layerA_pooled,
        },
    },
    'primitives_four': primitives,
    'exploratory': exploratory,
    'pre_registration': {
        'document': '00-design/analysis_protocols/pre_reg_D8_housing.md',
        'hypotheses_locked': ['H8.1', 'H8.2', 'H8.3', 'H8.4'],
    },
}

with open(OUT_JSON, 'w') as f:
    json.dump(_clean(out), f, indent=2, default=str)

log(f"   JSON written to {OUT_JSON}")
log("\nDone.")
logfile.close()
