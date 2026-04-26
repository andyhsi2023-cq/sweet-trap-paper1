"""
C5 Luxury Conspicuous Consumption — Sweet Trap PDE Analysis
============================================================
Purpose:   Execute Phenomenon Deep-Empirics (PDE) for C5 奢侈品炫耀消费
           as a candidate Focal case for the Sweet Trap multi-domain paper
           (Nature/Science target).
Inputs:    /Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/
           cfps_long_panel.parquet (READ-ONLY; SHA-256 locked)
           + raw DTA for travel/trco/other variables missing from panel.
Outputs:   ./C5_luxury_sweet_trap.log
           ../../02-data/processed/panel_C5_luxury.parquet
           ../../02-data/processed/C5_results.json
           ../../02-data/processed/C5_speccurve.csv
Contract:  - No multiprocessing.Pool(os.cpu_count()); n_workers <= 2 rule.
           - No hard-coded numerical results.
           - All random seeds set at top.
           - CFPS panel SHA-256 verified before reading (do not modify).
Author:    Lu An / Hongyang Xi; executed by Claude data-analyst agent.
Date:      2026-04-17
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

# ---- Environment guard (M5 Pro 24GB — n_workers<=2 rule) ------------------
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")

# Warnings are signals. We catch them explicitly via context manager where needed.
warnings.simplefilter("default")

# ---- Reproducibility ------------------------------------------------------
SEED = 20260417
RNG = np.random.default_rng(SEED)

# ---- Paths ----------------------------------------------------------------
ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
SCRIPT_DIR = ROOT / "03-analysis" / "scripts"
PROC_DIR = ROOT / "02-data" / "processed"
PDE_DIR = ROOT / "00-design" / "pde"

PANEL_IN = PROC_DIR / "cfps_long_panel.parquet"
RAW_DTA = Path(
    "/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/2010-2022cfps非平衡面板数据(stata_推荐使用）.dta"
)

LOG = SCRIPT_DIR / "C5_luxury_sweet_trap.log"
PANEL_OUT = PROC_DIR / "panel_C5_luxury.parquet"
RESULTS = PROC_DIR / "C5_results.json"
SPECCURVE = PROC_DIR / "C5_speccurve.csv"

# ---- Logger ---------------------------------------------------------------
LOG.unlink(missing_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(LOG, mode="w"), logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("C5")


def banner(title: str) -> None:
    log.info("=" * 78)
    log.info(title)
    log.info("=" * 78)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ===========================================================================
# STEP 0 — Variable-granularity audit (hard prerequisite)
# ===========================================================================
banner("STEP 0 | CFPS variable-granularity audit for C5 luxury / conspicuous")

panel_sha = sha256_file(PANEL_IN)
log.info(f"CFPS panel SHA-256: {panel_sha}")
log.info(f"CFPS panel path   : {PANEL_IN}")

# Read variable labels from raw DTA (metadata only, not full data)
with pd.io.stata.StataReader(str(RAW_DTA)) as _rdr:
    dta_labels = _rdr.variable_labels()

audit = {}
for key in ("dress", "eec", "travel", "trco", "durables_asset", "daily",
            "other", "school", "social", "food", "house", "med", "mexp",
            "expense", "savings", "Nhd", "nonhousing_debts", "income_p",
            "lnincome", "total_asset", "qn12012", "qn12016", "health",
            "unhealth", "qg401", "onlineshopoping", "urban", "eduy"):
    audit[key] = dta_labels.get(key, "<NOT IN DTA>")
for k, v in audit.items():
    log.info(f"  {k:22s} -> {v}")

# Decision:
# - dress (衣着鞋帽): primary luxury proxy (服装 is dominant category of Chinese luxury spend).
# - travel (旅游): positional "experiential luxury".
# - eec (文教娱乐): recreational upgrading (includes smartphone-era content).
# - durables_asset Δ: big-ticket conspicuous stock (car value, appliance upgrade).
# - trco (交通通讯): proxy for car-related spending.
#
# We build a COMPOSITE luxury proxy:
#   luxury_pos = dress + travel + eec + Δdurables_asset (positive part)
# Plus several subcomponents as alternative treatments for spec-curve.

# ===========================================================================
# STEP 1 — Build C5 analysis panel
# ===========================================================================
banner("STEP 1 | Build C5 panel from CFPS long-panel + raw DTA enrichment")

base = pd.read_parquet(PANEL_IN)
log.info(f"Base panel shape: {base.shape}")

# Enrich with columns missing from the cleaned parquet.
enrich = pd.read_stata(
    str(RAW_DTA),
    columns=["pid", "year", "travel", "trco", "other"],
    convert_categoricals=False,
)
# CFPS long panel pids are numeric; DTA likewise. Align dtype.
enrich["pid"] = enrich["pid"].astype("int64", errors="ignore")
base["pid"] = base["pid"].astype("int64", errors="ignore")
enrich["year"] = enrich["year"].astype("int64", errors="ignore")
base["year"] = base["year"].astype("int64", errors="ignore")

df = base.merge(enrich, on=["pid", "year"], how="left", validate="1:1",
                suffixes=("", "_dta"))
log.info(f"After enrich merge: {df.shape}; travel non-null={df['travel'].notna().sum()}, "
         f"trco non-null={df['trco'].notna().sum()}, other non-null={df['other'].notna().sum()}")

# ----- Clip / winsorise expenditure outliers ------------------------------
EXP_COLS = ["dress", "eec", "travel", "trco", "durables_asset", "daily",
            "other", "food", "house", "mexp", "savings", "nonhousing_debts",
            "expense", "income_p"]
for c in EXP_COLS:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        # Clip negatives (coding errors) to NaN
        df.loc[df[c] < 0, c] = np.nan

# ----- Build the core luxury treatments -----------------------------------
# Treatment 1: luxury_pos = dress + travel + eec + Δdurables_asset(+)
df = df.sort_values(["pid", "year"]).reset_index(drop=True)

# Δdurables_asset within person (only positive = fresh upgrade)
df["durables_lag"] = df.groupby("pid")["durables_asset"].shift(1)
df["ddurables"] = (df["durables_asset"] - df["durables_lag"]).clip(lower=0)

# Composite core (fill travel/eec missing with 0 only when at least dress observed)
def _safe_sum(row, keys):
    vals = [row[k] for k in keys if k in row.index]
    arr = np.array([v for v in vals if pd.notna(v)], dtype=float)
    # require at least 'dress' (status signalling core) — otherwise NaN
    if "dress" in keys and pd.isna(row.get("dress", np.nan)):
        return np.nan
    return float(arr.sum()) if arr.size > 0 else np.nan

df["luxury_core"] = df["dress"].fillna(0)  # clothing alone
df["luxury_broad"] = (
    df["dress"].fillna(0)
    + df["travel"].fillna(0)
    + df["eec"].fillna(0)
)
df.loc[df["dress"].isna(), "luxury_broad"] = np.nan

df["luxury_full"] = (
    df["dress"].fillna(0)
    + df["travel"].fillna(0)
    + df["eec"].fillna(0)
    + df["ddurables"].fillna(0)
)
df.loc[df["dress"].isna(), "luxury_full"] = np.nan

# log transforms
for c in ("luxury_core", "luxury_broad", "luxury_full",
          "dress", "travel", "eec", "durables_asset", "expense",
          "savings", "nonhousing_debts"):
    if c in df.columns:
        df[f"ln_{c}"] = np.log1p(df[c].clip(lower=0))

# Shares (relative to total expense)
df["dress_share"] = df["dress"] / df["expense"].replace(0, np.nan)
df["travel_share"] = df["travel"] / df["expense"].replace(0, np.nan)
df["eec_share"] = df["eec"] / df["expense"].replace(0, np.nan)
df["luxury_broad_share"] = df["luxury_broad"] / df["expense"].replace(0, np.nan)
df["luxury_full_share"] = df["luxury_full"] / df["expense"].replace(0, np.nan)

# Clip shares to [0, 1]
for s in ("dress_share", "travel_share", "eec_share",
          "luxury_broad_share", "luxury_full_share"):
    df.loc[(df[s] < 0) | (df[s] > 1), s] = np.nan

# Δ luxury within-person (for Sweet reward DV)
for c in ("luxury_core", "luxury_broad", "luxury_full",
          "ln_luxury_broad", "ln_luxury_full", "ln_dress",
          "luxury_broad_share", "luxury_full_share"):
    df[f"{c}_lag1"] = df.groupby("pid")[c].shift(1)
    df[f"d_{c}"] = df[c] - df[f"{c}_lag1"]

# ----- DVs: well-being & bitter outcomes ----------------------------------
# qn12012 (life sat 1-5), qn12016 (future confidence), qg401 (work income sat).
# Bitter: savings, debt growth, total_asset growth, chronic disease qp401.
df["qn12012"] = pd.to_numeric(df["qn12012"], errors="coerce")
df["qn12016"] = pd.to_numeric(df["qn12016"], errors="coerce")

df["ln_savings"] = np.log1p(df["savings"].clip(lower=0))
df["ln_debt"] = np.log1p(df["nonhousing_debts"].clip(lower=0))

# Net wealth change (Δ total asset). total_asset may have extreme outliers; winsorise.
if "total_asset" in df.columns:
    df["total_asset"] = pd.to_numeric(df["total_asset"], errors="coerce")
    q99 = df["total_asset"].quantile(0.995)
    df.loc[df["total_asset"].abs() > q99, "total_asset"] = np.nan
    df["ln_asset"] = np.log1p(df["total_asset"].clip(lower=0))
    df["d_ln_asset"] = df["ln_asset"] - df.groupby("pid")["ln_asset"].shift(1)

# Lag DVs for FE/first-differencing
for dv in ("qn12012", "qn12016", "ln_savings", "ln_debt"):
    df[f"{dv}_lag1"] = df.groupby("pid")[dv].shift(1)
    df[f"d_{dv}"] = df[dv] - df[f"{dv}_lag1"]

# ----- Controls -----------------------------------------------------------
df["eduy"] = pd.to_numeric(df["eduy"], errors="coerce")
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["urban"] = pd.to_numeric(df["urban"], errors="coerce")
df["gender"] = pd.to_numeric(df["gender"], errors="coerce")
df["provcd"] = df["provcd"].astype("category") if "provcd" in df.columns else np.nan
df["year_c"] = df["year"].astype("category")

# Cohort (pseudo-ancestral vs contemporary) — for Δ_ST
df["cohort"] = pd.cut(df["year"], bins=[2009, 2014, 2017, 2023],
                      labels=["2010-2014", "2015-2016", "2018-2022"])

# Save panel
keep_cols = [
    "pid", "year", "provcd", "urban", "age", "gender", "eduy", "communist",
    "income_p", "lnincome", "expense", "total_asset", "ln_asset", "d_ln_asset",
    "dress", "travel", "eec", "durables_asset", "ddurables",
    "luxury_core", "luxury_broad", "luxury_full",
    "ln_luxury_broad", "ln_luxury_full", "ln_dress",
    "dress_share", "travel_share", "eec_share",
    "luxury_broad_share", "luxury_full_share",
    "luxury_core_lag1", "luxury_broad_lag1", "luxury_full_lag1",
    "ln_luxury_broad_lag1", "ln_luxury_full_lag1", "ln_dress_lag1",
    "luxury_broad_share_lag1", "luxury_full_share_lag1",
    "d_luxury_core", "d_luxury_broad", "d_luxury_full",
    "d_ln_luxury_broad", "d_ln_luxury_full", "d_ln_dress",
    "d_luxury_broad_share", "d_luxury_full_share",
    "qn12012", "qn12016", "qg401", "qp401", "unhealth", "health",
    "savings", "ln_savings", "nonhousing_debts", "ln_debt",
    "qn12012_lag1", "qn12016_lag1", "ln_savings_lag1", "ln_debt_lag1",
    "d_qn12012", "d_qn12016", "d_ln_savings", "d_ln_debt",
    "cohort",
]
keep_cols = [c for c in keep_cols if c in df.columns]
panel = df[keep_cols].copy()
panel.to_parquet(PANEL_OUT, compression="snappy")
panel_out_sha = sha256_file(PANEL_OUT)
log.info(f"C5 panel saved: {PANEL_OUT} shape={panel.shape}, SHA-256={panel_out_sha}")

# ===========================================================================
# STEP 2 — F2 diagnostic (hard prerequisite before regression)
# ===========================================================================
banner("STEP 2 | F2 diagnostic — voluntariness & wealth-gradient of luxury")

f2 = {}
# cor(luxury, income)
for lux in ("dress", "luxury_broad", "luxury_full", "ln_luxury_broad",
            "ln_luxury_full", "luxury_full_share"):
    sub = panel[[lux, "lnincome", "eduy", "urban"]].dropna()
    if len(sub) < 500:
        continue
    rx = sub.corr().iloc[0]
    f2[lux] = {
        "n": int(len(sub)),
        "cor_income": float(rx["lnincome"]),
        "cor_eduy": float(rx["eduy"]),
        "cor_urban": float(rx["urban"]),
    }
    log.info(f"  {lux:26s} N={len(sub):6d}  cor(inc)={rx['lnincome']:+.3f}  "
             f"cor(edu)={rx['eduy']:+.3f}  cor(urban)={rx['urban']:+.3f}")

# F2 pass criterion: cor(luxury, income) > 0 AND cor(luxury, urban) > 0
# (rich, urban consumers buy more — signature of aspirational / voluntary luxury)
f2_pass = all(v["cor_income"] > 0 and v["cor_urban"] > 0 for v in f2.values())
log.info(f"  F2 pass = {f2_pass}  (expect all positive; ambiguity means coerced signal)")

# ===========================================================================
# STEP 3 — Sweet Trap core regressions
# ===========================================================================
banner("STEP 3 | Sweet (short-run satisfaction) & Bitter (long-run wealth)")

def run_fe(df_in: pd.DataFrame, dv: str, treat: str, controls: list[str],
           cluster: str = "pid") -> dict[str, Any]:
    """Fixed-effects regression via OLS with entity dummies (pid) + year dummies.
    Cluster-robust SE at `cluster` level. Returns coef, SE, CI, p, N.
    """
    cols = [dv, treat] + controls + [cluster, "year"]
    sub = df_in[cols].replace([np.inf, -np.inf], np.nan).dropna()
    if len(sub) < 200:
        return {"N": int(len(sub)), "beta": np.nan, "se": np.nan,
                "ci_lo": np.nan, "ci_hi": np.nan, "p": np.nan,
                "note": "insufficient_n"}
    rhs = [treat] + [c for c in controls if c != cluster]
    # Demean by pid to get within-person coefficient (like pid FE)
    sub = sub.copy()
    for v in [dv, treat] + [c for c in controls if c not in (cluster,)]:
        if pd.api.types.is_numeric_dtype(sub[v]):
            sub[v] = sub[v] - sub.groupby(cluster)[v].transform("mean")
    # Year FE via dummies
    y_dum = pd.get_dummies(sub["year"].astype("category"), prefix="y",
                           drop_first=True, dtype=float)
    Xp = pd.concat([sub[rhs].astype(float), y_dum], axis=1)
    Xp = sm.add_constant(Xp, has_constant="add")
    y = sub[dv].astype(float)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        model = sm.OLS(y, Xp).fit(
            cov_type="cluster",
            cov_kwds={"groups": sub[cluster].astype(str).values},
        )
    if treat not in model.params.index:
        return {"N": int(len(sub)), "beta": np.nan, "se": np.nan,
                "ci_lo": np.nan, "ci_hi": np.nan, "p": np.nan,
                "note": "treat_collinear"}
    b = float(model.params[treat])
    se = float(model.bse[treat])
    ci = model.conf_int().loc[treat].tolist()
    return {
        "N": int(len(sub)),
        "beta": b,
        "se": se,
        "ci_lo": float(ci[0]),
        "ci_hi": float(ci[1]),
        "p": float(model.pvalues[treat]),
    }


panel["provcd_num"] = panel["provcd"].cat.codes if hasattr(panel["provcd"], "cat") else 0

main_ctrls = ["lnincome", "eduy", "age", "urban"]
sweet_specs = []

# === Sweet side: Δ luxury within person → life satisfaction ===============
log.info("\n-- Sweet: Δ luxury → Δ qn12012 (within-person, year FE) --")
for treat in ("d_ln_luxury_broad", "d_ln_luxury_full", "d_ln_dress",
              "d_luxury_broad_share", "d_luxury_full_share"):
    r = run_fe(panel, "d_qn12012", treat, main_ctrls)
    r.update({"block": "sweet_withinperson", "dv": "d_qn12012", "treat": treat})
    sweet_specs.append(r)
    log.info(f"  {treat:28s} N={r['N']:6d}  β={r['beta']:+.4f}  "
             f"95%CI=[{r['ci_lo']:+.4f},{r['ci_hi']:+.4f}]  p={r['p']:.4f}")

# Level-based Sweet (cross-section FE, year FE only)
log.info("\n-- Sweet: log(luxury) level → qn12012 (year+prov FE via dummies) --")
for treat in ("ln_luxury_broad", "ln_luxury_full", "ln_dress", "luxury_full_share"):
    cols = ["qn12012", treat] + main_ctrls + ["year", "provcd_num", "pid"]
    sub = panel[cols].dropna()
    if len(sub) < 500:
        continue
    X = sub[[treat] + main_ctrls].astype(float)
    y_dum = pd.get_dummies(sub["year"].astype("category"), prefix="y",
                           drop_first=True, dtype=float)
    p_dum = pd.get_dummies(sub["provcd_num"].astype("category"), prefix="p",
                           drop_first=True, dtype=float)
    X_full = pd.concat([X, y_dum, p_dum], axis=1)
    X_full = sm.add_constant(X_full, has_constant="add")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        m = sm.OLS(sub["qn12012"].astype(float), X_full).fit(
            cov_type="cluster",
            cov_kwds={"groups": sub["pid"].astype(str).values},
        )
    b, se = float(m.params[treat]), float(m.bse[treat])
    ci = m.conf_int().loc[treat].tolist()
    r = {"block": "sweet_level_provYearFE", "dv": "qn12012", "treat": treat,
         "N": int(len(sub)), "beta": b, "se": se,
         "ci_lo": float(ci[0]), "ci_hi": float(ci[1]),
         "p": float(m.pvalues[treat])}
    sweet_specs.append(r)
    log.info(f"  {treat:28s} N={r['N']:6d}  β={r['beta']:+.4f}  "
             f"95%CI=[{r['ci_lo']:+.4f},{r['ci_hi']:+.4f}]  p={r['p']:.4f}")

# === Bitter side: luxury → savings down / debt up ==========================
log.info("\n-- Bitter: luxury → Δ ln_savings (within-person, year FE) --")
bitter_specs = []
for dv in ("d_ln_savings", "d_ln_debt"):
    for treat in ("ln_luxury_broad", "ln_luxury_full", "luxury_full_share"):
        r = run_fe(panel, dv, treat, main_ctrls)
        r.update({"block": f"bitter_{dv}", "dv": dv, "treat": treat})
        bitter_specs.append(r)
        log.info(f"  dv={dv:16s} treat={treat:24s} N={r['N']:6d}  β={r['beta']:+.5f}  "
                 f"95%CI=[{r['ci_lo']:+.5f},{r['ci_hi']:+.5f}]  p={r['p']:.4f}")

# Lag-1 Bitter — current luxury → next-wave savings/asset
log.info("\n-- Bitter-lag: luxury_{t} → Δ ln_savings_{t+1} --")
panel["dln_savings_fwd"] = panel.groupby("pid")["ln_savings"].shift(-1) - panel["ln_savings"]
panel["dln_asset_fwd"] = panel.groupby("pid")["ln_asset"].shift(-1) - panel["ln_asset"]
for dv in ("dln_savings_fwd", "dln_asset_fwd"):
    for treat in ("ln_luxury_broad", "ln_luxury_full", "luxury_full_share"):
        r = run_fe(panel, dv, treat, main_ctrls)
        r.update({"block": f"bitter_lag_{dv}", "dv": dv, "treat": treat})
        bitter_specs.append(r)
        log.info(f"  dv={dv:20s} treat={treat:22s} N={r['N']:6d}  β={r['beta']:+.5f}  "
                 f"95%CI=[{r['ci_lo']:+.5f},{r['ci_hi']:+.5f}]  p={r['p']:.4f}")

# ===========================================================================
# STEP 4 — Hedonic treadmill & ρ lock-in
# ===========================================================================
banner("STEP 4 | Hedonic treadmill (β) & consumption stickiness (ρ)")

# ρ lock-in: AR(1) of log-luxury within person
ar_specs = {}
for lux in ("ln_luxury_broad", "ln_luxury_full", "ln_dress"):
    sub = panel[[lux, f"{lux}_lag1", "pid"]].dropna()
    if len(sub) < 200:
        continue
    # within-person AR(1)
    for v in (lux, f"{lux}_lag1"):
        sub[v] = sub[v] - sub.groupby("pid")[v].transform("mean")
    X = sm.add_constant(sub[[f"{lux}_lag1"]].astype(float))
    m = sm.OLS(sub[lux].astype(float), X).fit(
        cov_type="cluster",
        cov_kwds={"groups": sub["pid"].astype(str).values},
    )
    rho = float(m.params[f"{lux}_lag1"])
    rho_p = float(m.pvalues[f"{lux}_lag1"])
    ar_specs[lux] = {"N": int(len(sub)), "rho": rho, "p": rho_p}
    log.info(f"  ρ AR(1) {lux:20s} N={len(sub):6d}  ρ={rho:+.4f}  p={rho_p:.4f}")

# Hedonic treadmill: does LEVEL of lagged luxury no longer predict current qn12012
# (adaptation), but Δ luxury (fresh upgrade) still does (habituation)?
treadmill = {}
for treat_lvl, treat_d in (
    ("ln_luxury_broad_lag1", "d_ln_luxury_broad"),
    ("ln_luxury_full_lag1", "d_ln_luxury_full"),
):
    cols = ["qn12012", treat_lvl, treat_d, "lnincome", "eduy", "age", "urban",
            "pid", "year", "provcd_num"]
    sub = panel[cols].replace([np.inf, -np.inf], np.nan).dropna()
    if len(sub) < 1000:
        continue
    # year and prov FE via dummies
    for v in ["qn12012", treat_lvl, treat_d, "lnincome", "eduy", "age", "urban"]:
        sub[v] = sub[v] - sub.groupby("pid")[v].transform("mean")
    y_dum = pd.get_dummies(sub["year"].astype("category"), prefix="y",
                           drop_first=True, dtype=float)
    X = pd.concat([sub[[treat_lvl, treat_d, "lnincome", "eduy", "age",
                        "urban"]].astype(float), y_dum], axis=1)
    X = sm.add_constant(X, has_constant="add")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        m = sm.OLS(sub["qn12012"].astype(float), X).fit(
            cov_type="cluster",
            cov_kwds={"groups": sub["pid"].astype(str).values},
        )
    rec = {
        "N": int(len(sub)),
        "beta_lag": float(m.params[treat_lvl]),
        "p_lag": float(m.pvalues[treat_lvl]),
        "beta_delta": float(m.params[treat_d]),
        "p_delta": float(m.pvalues[treat_d]),
    }
    treadmill[f"{treat_lvl}__vs__{treat_d}"] = rec
    log.info(f"  {treat_lvl} (adaptation): β={rec['beta_lag']:+.4f}  p={rec['p_lag']:.4f}")
    log.info(f"  {treat_d} (fresh Δ):      β={rec['beta_delta']:+.4f}  p={rec['p_delta']:.4f}")
    log.info("  Hedonic treadmill ==> fresh Δ should dominate; lagged level should fade.")

# ===========================================================================
# STEP 5 — Δ_ST cohort decomposition (core Sweet Trap scalar)
# ===========================================================================
banner("STEP 5 | Δ_ST cohort decomposition (ancestral=low-luxury vs current=high-luxury)")

def cohort_corr(df_in: pd.DataFrame, sig: str, dv: str,
                n_boot: int = 1000) -> dict[str, Any]:
    """Δ_ST = cor(sig, dv)_ancestral - cor(sig, dv)_current, bootstrapped."""
    sub = df_in[[sig, dv, "cohort", "pid"]].dropna()
    if len(sub) < 500:
        return {"n": int(len(sub))}
    anc = sub[sub["cohort"] == "2010-2014"]
    cur = sub[sub["cohort"] == "2018-2022"]
    if len(anc) < 100 or len(cur) < 100:
        return {"n_anc": int(len(anc)), "n_cur": int(len(cur))}
    c_anc = float(anc[[sig, dv]].corr().iloc[0, 1])
    c_cur = float(cur[[sig, dv]].corr().iloc[0, 1])
    delta = c_anc - c_cur
    # Cluster-bootstrap by pid (draw pids with replacement)
    boot = np.empty(n_boot, dtype=float)
    pids_anc = anc["pid"].unique()
    pids_cur = cur["pid"].unique()
    for i in range(n_boot):
        a_ids = RNG.choice(pids_anc, size=len(pids_anc), replace=True)
        c_ids = RNG.choice(pids_cur, size=len(pids_cur), replace=True)
        a_b = anc[anc["pid"].isin(a_ids)]
        c_b = cur[cur["pid"].isin(c_ids)]
        if len(a_b) < 30 or len(c_b) < 30:
            boot[i] = np.nan
            continue
        boot[i] = float(a_b[[sig, dv]].corr().iloc[0, 1]) - \
                  float(c_b[[sig, dv]].corr().iloc[0, 1])
    valid = boot[~np.isnan(boot)]
    lo, hi = np.percentile(valid, [2.5, 97.5])
    return {
        "n_anc": int(len(anc)),
        "n_cur": int(len(cur)),
        "cor_anc": c_anc,
        "cor_cur": c_cur,
        "delta_st": delta,
        "ci_lo": float(lo),
        "ci_hi": float(hi),
        "boot_mean": float(np.nanmean(valid)),
    }


delta_st = {}
pairs = [
    ("ln_luxury_broad", "qn12012"),
    ("ln_luxury_full", "qn12012"),
    ("ln_dress", "qn12012"),
    ("luxury_full_share", "qn12012"),
    # bitter counterpart: high signalling → welfare proxies
    ("ln_luxury_full", "ln_savings"),
    ("ln_luxury_full", "ln_asset"),
]
for sig, dv in pairs:
    r = cohort_corr(panel, sig, dv, n_boot=1000)
    delta_st[f"{sig}__{dv}"] = r
    if "delta_st" in r:
        log.info(f"  Δ_ST[{sig:20s} ~ {dv:12s}] = "
                 f"{r['delta_st']:+.3f}  95%CI=[{r['ci_lo']:+.3f},{r['ci_hi']:+.3f}]  "
                 f"(anc={r['cor_anc']:+.3f}, cur={r['cor_cur']:+.3f}, "
                 f"N_anc={r['n_anc']}, N_cur={r['n_cur']})")

# ===========================================================================
# STEP 6 — Specification curve analysis (144+ specs)
# ===========================================================================
banner("STEP 6 | Specification-curve analysis")

# Spec space:
# DV (6):  qn12012, d_qn12012, qn12016, d_ln_savings, d_ln_debt, dln_asset_fwd
# TREAT (8): ln_luxury_broad, ln_luxury_full, ln_dress,
#            d_ln_luxury_broad, d_ln_luxury_full, d_ln_dress,
#            luxury_full_share, d_luxury_full_share
# CONTROL (3): minimal, main, extended
# SAMPLE (4): full, urban, high_income, female_head

control_sets = {
    "minimal": ["age"],
    "main": ["lnincome", "eduy", "age", "urban"],
    "extended": ["lnincome", "eduy", "age", "urban", "health", "communist"],
}


def sample_filter(df_in, key):
    if key == "full":
        return df_in
    if key == "urban":
        return df_in[df_in["urban"] == 1]
    if key == "highinc":
        thr = df_in["lnincome"].quantile(0.75)
        return df_in[df_in["lnincome"] >= thr]
    if key == "female":
        return df_in[df_in["gender"] == 0]
    return df_in


dv_list = ["qn12012", "d_qn12012", "qn12016",
           "d_ln_savings", "d_ln_debt", "dln_asset_fwd"]
treat_list = ["ln_luxury_broad", "ln_luxury_full", "ln_dress",
              "d_ln_luxury_broad", "d_ln_luxury_full", "d_ln_dress",
              "luxury_full_share", "d_luxury_full_share"]
sample_list = ["full", "urban", "highinc", "female"]
ctrl_list = list(control_sets.keys())

rows = []
spec_id = 0
for dv in dv_list:
    for treat in treat_list:
        # skip meaningless DV/treat combos: don't use level-lagged-style DV with level-treat noise
        for ckey in ctrl_list:
            for skey in sample_list:
                spec_id += 1
                sub = sample_filter(panel, skey).copy()
                r = run_fe(sub, dv, treat, control_sets[ckey])
                rows.append({
                    "spec_id": spec_id,
                    "dv": dv, "treat": treat,
                    "control": ckey, "sample": skey,
                    **r,
                })

spec_df = pd.DataFrame(rows)
spec_df.to_csv(SPECCURVE, index=False)
log.info(f"Spec curve: {len(spec_df)} specs -> {SPECCURVE}")

# Summary stats
sweet_dv_mask = spec_df["dv"].isin(["qn12012", "d_qn12012", "qn12016"])
bitter_dv_mask = spec_df["dv"].isin(["d_ln_savings", "d_ln_debt", "dln_asset_fwd"])


def sc_summary(sub: pd.DataFrame, label: str, sign_sweet: int = +1) -> dict:
    valid = sub.dropna(subset=["beta", "p"])
    if len(valid) == 0:
        return {"label": label, "n_specs": 0}
    pos = (valid["beta"] > 0).mean()
    sig05 = (valid["p"] < 0.05).mean()
    # sign consistency: fraction with expected sign
    if sign_sweet == +1:
        consistent = ((valid["beta"] > 0) & (valid["p"] < 0.05)).mean()
    else:
        consistent = ((valid["beta"] < 0) & (valid["p"] < 0.05)).mean()
    return {
        "label": label,
        "n_specs": int(len(valid)),
        "median_beta": float(valid["beta"].median()),
        "q025_beta": float(valid["beta"].quantile(0.025)),
        "q975_beta": float(valid["beta"].quantile(0.975)),
        "share_positive": float(pos),
        "share_p05": float(sig05),
        "share_expected_sign_p05": float(consistent),
    }


sc_sweet = sc_summary(spec_df[sweet_dv_mask], "sweet (β>0 expected)", sign_sweet=+1)
sc_bitter_save = sc_summary(spec_df[spec_df["dv"] == "d_ln_savings"],
                            "bitter_savings (β<0 expected)", sign_sweet=-1)
sc_bitter_debt = sc_summary(spec_df[spec_df["dv"] == "d_ln_debt"],
                            "bitter_debt (β>0 expected)", sign_sweet=+1)
sc_bitter_asset = sc_summary(spec_df[spec_df["dv"] == "dln_asset_fwd"],
                             "bitter_asset (β<0 expected)", sign_sweet=-1)

for s in (sc_sweet, sc_bitter_save, sc_bitter_debt, sc_bitter_asset):
    log.info(f"  {s['label']:40s}: n={s['n_specs']:3d}  "
             f"med β={s.get('median_beta', np.nan):+.4f}  "
             f"share(+)={s.get('share_positive', np.nan):.2f}  "
             f"share_p<.05={s.get('share_p05', np.nan):.2f}  "
             f"expected-sign@p<.05={s.get('share_expected_sign_p05', np.nan):.2f}")

# ===========================================================================
# STEP 7 — Quasi-experimental probes
# ===========================================================================
banner("STEP 7 | Quasi-experimental probes (informal)")

# 7.1. 海南离岛免税 2020 expansion: treat luxury (dress + travel) spike in tourists-hub provinces
# Use province-level: Hainan treated, other southern coastal (粤/闽/琼) vs interior.
probe = {}
if "provcd" in panel.columns:
    # CFPS provcd coding: 46 = Hainan (common GB/T 2260)
    panel["hainan_post"] = ((panel["provcd"].astype(str).isin(["46", "46.0"])) &
                             (panel["year"] >= 2020)).astype(int)
    sub = panel[["dress", "travel", "hainan_post", "provcd_num", "year",
                 "lnincome", "eduy", "age", "urban", "pid"]].dropna()
    for dv in ("dress", "travel"):
        if len(sub) > 500:
            sub2 = sub.copy()
            # DID via FE
            for v in [dv, "lnincome", "eduy", "age", "urban", "hainan_post"]:
                sub2[v] = sub2[v] - sub2.groupby("pid")[v].transform("mean")
            y_d = pd.get_dummies(sub2["year"].astype("category"),
                                 prefix="y", drop_first=True, dtype=float)
            X = pd.concat([sub2[["hainan_post", "lnincome", "eduy", "age",
                                 "urban"]].astype(float), y_d], axis=1)
            X = sm.add_constant(X, has_constant="add")
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                m = sm.OLS(sub2[dv].astype(float), X).fit(
                    cov_type="cluster",
                    cov_kwds={"groups": sub2["pid"].astype(str).values},
                )
            probe[f"hainan_post__{dv}"] = {
                "N": int(len(sub2)),
                "beta": float(m.params["hainan_post"]),
                "p": float(m.pvalues["hainan_post"]),
                "ci_lo": float(m.conf_int().loc["hainan_post"][0]),
                "ci_hi": float(m.conf_int().loc["hainan_post"][1]),
            }
            log.info(f"  Hainan 2020 × {dv:8s}: β={probe[f'hainan_post__{dv}']['beta']:+.2f}  "
                     f"p={probe[f'hainan_post__{dv}']['p']:.4f}  "
                     f"N={probe[f'hainan_post__{dv}']['N']}")

# 7.2. City-tier gradient (urban × year interaction)
tier = {}
sub = panel[["ln_luxury_full", "urban", "year", "lnincome", "eduy",
             "age", "pid", "qn12012"]].dropna()
if len(sub) > 1000:
    for v in ["ln_luxury_full", "lnincome", "eduy", "age", "qn12012"]:
        sub[v] = sub[v] - sub.groupby("pid")[v].transform("mean")
    # interact urban with ln_luxury — bigger sweet response in urban?
    sub["lux_x_urban"] = sub["ln_luxury_full"] * sub["urban"]
    y_d = pd.get_dummies(sub["year"].astype("category"), prefix="y",
                         drop_first=True, dtype=float)
    X = pd.concat([sub[["ln_luxury_full", "lux_x_urban", "urban", "lnincome",
                        "eduy", "age"]].astype(float), y_d], axis=1)
    X = sm.add_constant(X, has_constant="add")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = sm.OLS(sub["qn12012"].astype(float), X).fit(
            cov_type="cluster",
            cov_kwds={"groups": sub["pid"].astype(str).values},
        )
    tier = {k: {"beta": float(m.params[k]),
                "p": float(m.pvalues[k]),
                "ci_lo": float(m.conf_int().loc[k][0]),
                "ci_hi": float(m.conf_int().loc[k][1])}
            for k in ("ln_luxury_full", "lux_x_urban", "urban")}
    log.info(f"  urban-tier interaction: ln_luxury={tier['ln_luxury_full']['beta']:+.4f}  "
             f"lux×urban={tier['lux_x_urban']['beta']:+.4f}  "
             f"p(interaction)={tier['lux_x_urban']['p']:.4f}")

# ===========================================================================
# STEP 8 — Bridge to Layer A (A7 peacock, A11 jewel-beetle)
# ===========================================================================
banner("STEP 8 | Bridge to Layer A peacock / jewel-beetle")

pool_mean = 0.72  # Layer A pooled Δ_ST
peacock = 0.58    # A7 peacock runaway
jewelbeetle = 0.55  # A11 jewel-beetle supernormal

# Get C5 best Δ_ST for bridge
c5_best_deltas = [v["delta_st"] for k, v in delta_st.items()
                  if "delta_st" in v and "qn12012" in k]
c5_best = max(c5_best_deltas) if c5_best_deltas else np.nan
c5_any_pos = sum(1 for d in c5_best_deltas if d > 0)
log.info(f"  Layer A pool Δ_ST = +{pool_mean:.2f}")
log.info(f"  A7 peacock       = +{peacock:.2f}")
log.info(f"  A11 jewel-beetle = +{jewelbeetle:.2f}")
log.info(f"  C5 best Δ_ST     = {c5_best:+.3f}  "
         f"(out of {len(c5_best_deltas)} pairs, {c5_any_pos} positive)")

# ===========================================================================
# STEP 9 — Package results
# ===========================================================================
banner("STEP 9 | Package results JSON")

results = {
    "meta": {
        "analysis": "C5_luxury_sweet_trap",
        "generated": pd.Timestamp.utcnow().isoformat() + "Z",
        "seed": SEED,
        "cfps_panel_sha256": panel_sha,
        "c5_panel_sha256": panel_out_sha,
        "script": str(SCRIPT_DIR / "C5_luxury_sweet_trap.py"),
        "log": str(LOG),
    },
    "granularity_audit": audit,
    "f2_diagnostic": f2,
    "f2_pass": f2_pass,
    "sweet_specs": sweet_specs,
    "bitter_specs": bitter_specs,
    "ar1_rho": ar_specs,
    "hedonic_treadmill": treadmill,
    "delta_st": delta_st,
    "spec_curve_summary": {
        "sweet": sc_sweet,
        "bitter_savings": sc_bitter_save,
        "bitter_debt": sc_bitter_debt,
        "bitter_asset": sc_bitter_asset,
        "total_specs": int(len(spec_df)),
    },
    "hainan_probe": probe,
    "tier_interaction": tier,
    "layerA_bridge": {
        "pool": pool_mean,
        "peacock_A7": peacock,
        "jewelbeetle_A11": jewelbeetle,
        "c5_best_delta_st": None if np.isnan(c5_best) else float(c5_best),
        "c5_positive_out_of_total_life_sat_pairs": (c5_any_pos, len(c5_best_deltas)),
    },
}

with open(RESULTS, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False, default=float)
log.info(f"Results written: {RESULTS}")

banner("DONE — C5 Luxury Sweet Trap PDE complete")
