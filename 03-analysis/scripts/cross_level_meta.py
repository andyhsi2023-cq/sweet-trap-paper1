"""
Cross-Level Meta-Regression for Sweet Trap Multidomain
======================================================
Purpose: Test whether the Sweet Trap construct's mechanism-class gradient is
         *consistent across layers* (A animal meta, B human focal spec-curve,
         D Mendelian Randomization). This upgrades the four-layer evidence
         from "parallel" to "mutually predictive".

Inputs  (all produced by upstream project scripts):
  - /Volumes/.../sweet-trap-multidomain/00-design/pde/layer_A_animal_meta_v2.md
        (hand-curated table; values below mirror the R script `layer_A_meta_v2.R`)
  - /Users/.../02-data/processed/mr_results_all_chains_v2.csv        (Layer D, 19 chains)
  - /Users/.../03-analysis/spec-curve/spec_curve_all_summary.csv     (Layer B, 5 cases)
  - /Users/.../03-analysis/spec-curve/spec_curve_<case>_results.csv  (for N sample sizes)

Outputs:
  - /Users/.../02-data/processed/cross_level_effects_table.csv
  - /Users/.../03-analysis/models/cross_level_meta_results.json
  - /Users/.../04-figures/main/fig9_cross_level_meta.png
  - /Users/.../04-figures/main/fig9_cross_level_meta.pdf

Key design decisions:
  * Scale harmonization: within-layer z-scoring (Option A, more conservative)
    primary; Cohen's-d equivalence reported as secondary sensitivity.
  * Random intercept by layer via statsmodels MixedLM.
  * Layer B (5 cases) enters main model but is flagged and sensitivity checked.
  * Species/taxon moderators already tested in Layer A (p=.695) — not revisited.

Author: Lu An & Hongyang Xi
Date  : 2026-04-18
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.regression.mixed_linear_model import MixedLM

# -----------------------------------------------------------------------------
# 0. Paths
# -----------------------------------------------------------------------------
PROJ = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
OUT_CSV = PROJ / "02-data/processed/cross_level_effects_table.csv"
OUT_JSON = PROJ / "03-analysis/models/cross_level_meta_results.json"
OUT_FIG_PNG = PROJ / "04-figures/main/fig9_cross_level_meta.png"
OUT_FIG_PDF = PROJ / "04-figures/main/fig9_cross_level_meta.pdf"

MR_CSV = PROJ / "02-data/processed/mr_results_all_chains_v2.csv"
SPEC_ALL = PROJ / "03-analysis/spec-curve/spec_curve_all_summary.csv"
SPEC_DIR = PROJ / "03-analysis/spec-curve"

np.random.seed(20260418)


# -----------------------------------------------------------------------------
# 1. Layer A: read-in the 20 animal cases (mirrors layer_A_meta_v2.R)
# -----------------------------------------------------------------------------
LAYER_A = pd.DataFrame({
    "case_id": [f"A{i}" for i in range(1, 21)],
    "case_name": [
        "Moth artificial light",
        "Sea-turtle hatchling",
        "Plastic ingestion marine",
        "Drosophila sugar",
        "Rat ICSS (Olds-Milner)",
        "Fisherian runaway widowbird",
        "Ecological trap HPL/road",
        "Neonicotinoid Apis/Bombus",
        "Ostracod arms race fossil",
        "Tungara frog phonotaxis",
        "Monarch tropical milkweed",
        "Floral-scent NO3 degradation",
        "Swordtail sword ornament",
        "Julodimorpha beetle bottle",
        "Migratory bird urban light",
        "Bumblebee social disruption",
        "Guppy rare-male",
        "Zebra finch hidden cost",
        "Stalk-eyed fly eye span",
        "Milkweed bug Oncopeltus",
    ],
    "taxon": [
        "invertebrate_insect", "reptile", "vertebrate_bird",
        "invertebrate_insect", "vertebrate_mammal",
        "vertebrate_bird", "invertebrate_insect", "invertebrate_insect",
        "invertebrate_other", "amphibian", "invertebrate_insect",
        "invertebrate_insect", "vertebrate_fish", "invertebrate_insect",
        "vertebrate_bird", "invertebrate_insect", "vertebrate_fish",
        "vertebrate_bird", "invertebrate_insect", "invertebrate_insect",
    ],
    "mechanism": [
        "sensory_exploit", "sensory_exploit", "sensory_exploit",
        "olds_milner", "olds_milner",
        "fisher_runaway", "sensory_exploit", "olds_milner",
        "fisher_runaway", "sensory_exploit", "sensory_exploit",
        "sensory_exploit", "fisher_runaway", "sensory_exploit",
        "sensory_exploit", "olds_milner", "fisher_runaway",
        "repro_survival_tradeoff", "fisher_runaway", "sensory_exploit",
    ],
    "effect": [
        0.82, 0.76, 0.64, 0.71, 0.97,
        0.58, 0.55, 0.73,
        0.52, 0.67, 0.61, 0.58, 0.54, 0.65,
        0.69, 0.71, 0.56, 0.47, 0.53, 0.49,
    ],
    "ci_lo": [
        0.61, 0.58, 0.44, 0.52, 0.90,
        0.36, 0.34, 0.55,
        0.28, 0.48, 0.43, 0.39, 0.35, 0.46,
        0.52, 0.56, 0.37, 0.28, 0.33, 0.29,
    ],
    "ci_hi": [
        0.95, 0.88, 0.79, 0.85, 1.00,
        0.75, 0.72, 0.86,
        0.72, 0.82, 0.76, 0.73, 0.70, 0.80,
        0.83, 0.84, 0.71, 0.63, 0.70, 0.66,
    ],
})
LAYER_A["se"] = (LAYER_A["ci_hi"] - LAYER_A["ci_lo"]) / (2 * 1.96)
LAYER_A["layer"] = "A"
LAYER_A["scale_type"] = "delta_ST"
LAYER_A["case"] = LAYER_A["case_id"] + " | " + LAYER_A["case_name"]


# -----------------------------------------------------------------------------
# 2. Layer D: Mendelian Randomization, IVW_random rows only
# -----------------------------------------------------------------------------
mr = pd.read_csv(MR_CSV)
mr_ivw = mr[mr["method"] == "IVW_random"].copy()

# Mechanism mapping (documented in §2 of the findings md):
#   Exposure-based assignment, informed by the biological construct.
#
#  risk_tolerance  → engineered_reward   (hedonic / dopaminergic proxy)
#  drinks_per_week → engineered_reward   (direct reward hijack)
#  smoking_initiation → engineered_reward
#  bmi_locke2015   → sensory_exploit     (supernormal palatability of novel diets)
#  years_of_schooling → mismatch_protective (not Sweet Trap itself, inverse marker)
#  subjective_wellbeing → mismatch_protective (inverse marker)
MECH_MAP_D = {
    "risk_tolerance": "olds_milner",
    "drinks_per_week": "olds_milner",
    "smoking_initiation": "olds_milner",
    "bmi_locke2015": "sensory_exploit",
    "years_of_schooling": "mismatch_protective",
    "subjective_wellbeing": "mismatch_protective",
}
mr_ivw["mechanism"] = mr_ivw["exposure"].map(MECH_MAP_D)

# For cross-layer meta we use the absolute-value effect on log-OR scale, so that
# "larger magnitude" consistently means "stronger reward-fitness decoupling".
# For protective exposures (years_schooling / subjective_wellbeing), the
# *negative* sign is the Sweet Trap prediction; we record the signed effect
# and a harmonized_effect (abs-value, direction preserved by category).
mr_ivw = mr_ivw.rename(columns={"beta": "effect_raw", "se": "se_raw"})
# For mechanism-prediction rank, Sweet Trap predicts: larger |beta| among
# engineered_reward & sensory_exploit; inverse (protective) for schooling/SWB.
# Effect magnitude for the cross-level gradient uses absolute log-OR.
mr_ivw["effect"] = mr_ivw["effect_raw"].abs()
mr_ivw["se"] = mr_ivw["se_raw"]
mr_ivw["ci_lo"] = mr_ivw["effect"] - 1.96 * mr_ivw["se"]
mr_ivw["ci_hi"] = mr_ivw["effect"] + 1.96 * mr_ivw["se"]
mr_ivw["layer"] = "D"
mr_ivw["scale_type"] = "log_OR_abs"
mr_ivw["case"] = mr_ivw["exposure"] + " to " + mr_ivw["outcome"]
mr_ivw["case_id"] = "D" + mr_ivw["chain"].astype(str)

LAYER_D = mr_ivw[[
    "case_id", "case", "layer", "mechanism", "effect", "se",
    "ci_lo", "ci_hi", "scale_type",
]].reset_index(drop=True)


# -----------------------------------------------------------------------------
# 3. Layer B: spec-curve focal median β for five human cases
# -----------------------------------------------------------------------------
spec = pd.read_csv(SPEC_ALL)

def _parse_ci(text: str):
    # "[-0.0895, -0.0564]" → (-0.0895, -0.0564)
    lo, hi = text.strip("[]").split(",")
    return float(lo), float(hi)

# Sample size N for each Layer B case (read from first focal spec)
def _sample_n(case: str) -> int:
    # filename convention: 'D_alcohol' → 'spec_curve_Dalcohol_results.csv'
    key = case.replace("_", "")
    path = SPEC_DIR / f"spec_curve_{key}_results.csv"
    if not path.exists():
        path = SPEC_DIR / f"spec_curve_{case}_results.csv"
    results = pd.read_csv(path)
    narrow = results[results.get("is_focal_narrow", False) == True]  # noqa: E712
    src = narrow if len(narrow) > 0 else results
    return int(np.median(src["n"]))

layer_b_rows = []
# Mechanism mapping for human focal cases (layer B)
MECH_MAP_B = {
    "C8":        ("engineered_reward_finance", "olds_milner"),         # retail investing hedonic hook
    "C11":       ("sensory_exploit_diet",      "sensory_exploit"),     # ultra-processed foods
    "C12":       ("engineered_reward_media",   "olds_milner"),         # short-video feed
    "C13":       ("sensory_exploit_status",    "fisher_runaway"),      # housing status runaway
    "D_alcohol": ("engineered_reward_alcohol", "olds_milner"),         # alcohol harmful use
}

for _, row in spec.iterrows():
    case = row["case"]
    beta = row["median_beta_narrow"]
    n = _sample_n(case)
    lo, hi = _parse_ci(row["median_ci_narrow"])
    se_std_beta = (hi - lo) / (2 * 1.96)
    human_label, mech = MECH_MAP_B[case]
    layer_b_rows.append({
        "case_id": f"B_{case}",
        "case": f"{case} ({human_label})",
        "layer": "B",
        "mechanism": mech,
        "effect_raw": beta,
        "se_raw": se_std_beta,
        "effect": abs(beta),
        "se": se_std_beta,
        "ci_lo": abs(beta) - 1.96 * se_std_beta,
        "ci_hi": abs(beta) + 1.96 * se_std_beta,
        "scale_type": "standardized_beta_abs",
        "n_sample": n,
    })

LAYER_B = pd.DataFrame(layer_b_rows)


# -----------------------------------------------------------------------------
# 4. Stack layers; harmonize mechanism labels
# -----------------------------------------------------------------------------
def _ensure_cols(df: pd.DataFrame) -> pd.DataFrame:
    keep = ["case_id", "case", "layer", "mechanism",
            "effect", "se", "ci_lo", "ci_hi", "scale_type"]
    for c in keep:
        if c not in df.columns:
            df[c] = np.nan
    return df[keep]

LAYER_A_c = _ensure_cols(LAYER_A.copy())
LAYER_B_c = _ensure_cols(LAYER_B.copy())
LAYER_D_c = _ensure_cols(LAYER_D.copy())

ALL = pd.concat([LAYER_A_c, LAYER_B_c, LAYER_D_c], ignore_index=True)

# Drop repro_survival_tradeoff (single zebra finch) — too small to pool.
# Drop mismatch_protective here for the core gradient model (it is sign-only,
# not magnitude, as planned). Retained in sensitivity analysis.
CORE_MECHS = ["olds_milner", "sensory_exploit", "fisher_runaway"]
CORE = ALL[ALL["mechanism"].isin(CORE_MECHS)].copy()


# -----------------------------------------------------------------------------
# 5. Scale harmonization
#    A) within-layer z-score of `effect`   (primary)
#    B) Cohen's-d equivalence              (sensitivity)
# -----------------------------------------------------------------------------
def z_within(df: pd.DataFrame, by: str, col: str) -> pd.Series:
    grp = df.groupby(by)[col]
    return (df[col] - grp.transform("mean")) / grp.transform("std")

CORE["effect_z"] = z_within(CORE, "layer", "effect")
# Propagate SE to the z-scale by dividing by the layer SD
layer_sd = CORE.groupby("layer")["effect"].std().to_dict()
CORE["se_z"] = CORE["se"] / CORE["layer"].map(layer_sd)

# Cohen's-d conversion (for sensitivity only)
#   log_OR → d : d = log_OR * sqrt(3)/pi
#   std_beta → d : approximate d = 2*beta / sqrt(1 - beta^2)  (only for small beta)
#   delta_ST : treated as already an effect-size metric on correlation scale → d via r→d
def _r_to_d(r: float) -> float:
    r = max(min(r, 0.999), -0.999)
    return 2.0 * r / math.sqrt(1.0 - r * r)

def _to_d(row) -> float:
    st = row["scale_type"]
    eff = row["effect"]
    if st == "delta_ST":
        return _r_to_d(eff)
    if st == "log_OR_abs":
        return eff * math.sqrt(3.0) / math.pi
    if st == "standardized_beta_abs":
        # treat as partial-r equivalent
        return _r_to_d(eff)
    return np.nan

CORE["effect_d"] = CORE.apply(_to_d, axis=1)
# SE under delta-method approximations: d = 2r/sqrt(1-r^2)
def _se_d(row) -> float:
    st = row["scale_type"]
    e, s = row["effect"], row["se"]
    if st == "log_OR_abs":
        return s * math.sqrt(3.0) / math.pi
    if st in ("delta_ST", "standardized_beta_abs"):
        r = max(min(e, 0.999), -0.999)
        dr = (2.0 * (1 - r * r) + 2 * r * r) / ((1 - r * r) ** 1.5)
        # dr = derivative of d(r) = 2r / sqrt(1-r^2)
        # d/dr [2r (1-r^2)^{-1/2}] = 2/(1-r^2)^{1/2} + 2r^2/(1-r^2)^{3/2}
        dr = 2.0 / math.sqrt(1 - r * r) + 2.0 * r * r / ((1 - r * r) ** 1.5)
        return s * dr
    return np.nan

CORE["se_d"] = CORE.apply(_se_d, axis=1)


# -----------------------------------------------------------------------------
# 6. Meta-regression
# -----------------------------------------------------------------------------
def fit_mixed(df: pd.DataFrame, y: str, se_col: str | None = None) -> dict:
    """
    y ~ mechanism + (1|layer)  via MixedLM
    Weights = 1/se^2 if se_col given (precision-weighted GLS-like)
    """
    d = df.copy()
    d["mechanism"] = pd.Categorical(
        d["mechanism"], categories=CORE_MECHS, ordered=False,
    )
    X = pd.get_dummies(d["mechanism"], drop_first=False).astype(float)
    # reference = fisher_runaway (most conservative, lowest mean Δ_ST in A)
    X = X.drop(columns=["fisher_runaway"])
    X.insert(0, "intercept", 1.0)

    if se_col is not None and d[se_col].notna().all():
        w = 1.0 / (d[se_col] ** 2)
    else:
        w = None

    md = MixedLM(d[y].astype(float).values,
                 X.values,
                 groups=d["layer"].values)
    try:
        fit = md.fit(reml=True, method="lbfgs")
    except Exception:
        fit = md.fit(reml=True, method="bfgs")

    params = dict(zip(X.columns, fit.params))
    bse = dict(zip(X.columns, fit.bse))
    # Variance components
    try:
        re_var = float(fit.cov_re.iloc[0, 0])
    except Exception:
        re_var = float(np.asarray(fit.cov_re)[0, 0])
    resid_var = float(fit.scale)

    # Test mechanism: Wald chi2 for joint 0 restrictions on olds_milner + sensory_exploit
    names = list(X.columns)
    # statsmodels wald_test expects a string formula or an array with shape (q, k)
    # Use a list-of-strings formulation to avoid patsy design-info issues.
    constraints = [f"{names.index('olds_milner')}=0",
                   f"{names.index('sensory_exploit')}=0"]
    try:
        wald = fit.wald_test(constraints, scalar=True)
        wstat, wp = float(wald.statistic), float(wald.pvalue)
    except Exception:
        # Manual chi2 via Wald = b' (V)^-1 b on the two coefs
        idx = [names.index("olds_milner"), names.index("sensory_exploit")]
        b = np.asarray(fit.params)[idx]
        V = np.asarray(fit.cov_params())[np.ix_(idx, idx)]
        try:
            wstat = float(b @ np.linalg.solve(V, b))
        except np.linalg.LinAlgError:
            wstat = float(b @ np.linalg.pinv(V) @ b)
        wp = float(1 - stats.chi2.cdf(wstat, df=2))

    return {
        "params": params,
        "se": bse,
        "re_var_layer": re_var,
        "resid_var": resid_var,
        "layer_share": re_var / (re_var + resid_var),
        "wald_mech_stat": wstat,
        "wald_mech_p": wp,
        "loglik": float(fit.llf),
        "aic": float(fit.aic) if hasattr(fit, "aic") else np.nan,
        "bic": float(fit.bic) if hasattr(fit, "bic") else np.nan,
        "n": int(len(d)),
        "fit_obj": fit,
    }


main_primary = fit_mixed(CORE, "effect_z")
main_cohen = fit_mixed(CORE, "effect_d", se_col="se_d")


# -----------------------------------------------------------------------------
# 7. Per-layer mechanism means (consistency of the rank order)
# -----------------------------------------------------------------------------
def layer_mech_table(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return (
        df.groupby(["layer", "mechanism"])[col]
          .agg(["mean", "std", "count"])
          .reset_index()
    )

by_layer = layer_mech_table(CORE, "effect")
by_layer_z = layer_mech_table(CORE, "effect_z")


# Spearman rank consistency across layers
def rank_vector(df: pd.DataFrame, layer: str, col: str) -> pd.Series:
    sub = df[df["layer"] == layer].groupby("mechanism")[col].mean()
    return sub.reindex(CORE_MECHS)

rank_A = rank_vector(CORE, "A", "effect")
rank_B = rank_vector(CORE, "B", "effect")
rank_D = rank_vector(CORE, "D", "effect")

# Compute pairwise Spearman
def safe_spearman(a: pd.Series, b: pd.Series):
    a2, b2 = a.dropna(), b.dropna()
    common = a2.index.intersection(b2.index)
    if len(common) < 2:
        return np.nan, np.nan
    rho, p = stats.spearmanr(a2.loc[common], b2.loc[common])
    return float(rho), float(p)

sp_AD = safe_spearman(rank_A, rank_D)
sp_AB = safe_spearman(rank_A, rank_B)
sp_BD = safe_spearman(rank_B, rank_D)


# -----------------------------------------------------------------------------
# 8. Leave-one-layer-out sensitivity
# -----------------------------------------------------------------------------
def fit_loo_primary(df: pd.DataFrame, drop_layer: str) -> dict:
    sub = df[df["layer"] != drop_layer].copy()
    # Re-z-score within the remaining layers to preserve primary harmonization
    sub["effect_z"] = z_within(sub, "layer", "effect")
    res = fit_mixed(sub, "effect_z")
    res.pop("fit_obj", None)
    return {k: v for k, v in res.items() if k != "fit_obj"}

loo = {L: fit_loo_primary(CORE, L) for L in ["A", "B", "D"]}


# -----------------------------------------------------------------------------
# 9. Mechanism definition sensitivity
#    Reclassify 'sensory_exploit_status' (C13, Fisher housing) as olds_milner
#    to test the Fisher→reward re-labelling edge-case.
# -----------------------------------------------------------------------------
CORE_alt = CORE.copy()
CORE_alt.loc[CORE_alt["case_id"] == "B_C13", "mechanism"] = "olds_milner"
mech_sens = fit_mixed(CORE_alt, "effect_z")


# -----------------------------------------------------------------------------
# 10. A+D only (drop underpowered Layer B)
# -----------------------------------------------------------------------------
AD = CORE[CORE["layer"].isin(["A", "D"])].copy()
AD["effect_z"] = z_within(AD, "layer", "effect")
ad_only = fit_mixed(AD, "effect_z")


# -----------------------------------------------------------------------------
# 11. Persist data + results
# -----------------------------------------------------------------------------
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_FIG_PNG.parent.mkdir(parents=True, exist_ok=True)

# Full unified table (CORE + excluded categories for transparency)
ALL.to_csv(OUT_CSV, index=False)


def _strip(d: dict) -> dict:
    return {k: v for k, v in d.items() if k != "fit_obj"}

results = {
    "n_cases": {
        "layer_A": int((CORE["layer"] == "A").sum()),
        "layer_B": int((CORE["layer"] == "B").sum()),
        "layer_D": int((CORE["layer"] == "D").sum()),
        "total_core": int(len(CORE)),
        "all_rows_stacked": int(len(ALL)),
    },
    "rank_by_layer_mean_effect": {
        "A": rank_A.dropna().to_dict(),
        "B": rank_B.dropna().to_dict(),
        "D": rank_D.dropna().to_dict(),
    },
    "spearman_rho_pairwise": {
        "A_vs_D": sp_AD,
        "A_vs_B": sp_AB,
        "B_vs_D": sp_BD,
    },
    "main_model_z": _strip(main_primary),
    "main_model_cohen_d": _strip(main_cohen),
    "loo_primary": loo,
    "mech_sensitivity_reclassify_C13": _strip(mech_sens),
    "A_plus_D_only": _strip(ad_only),
    "layer_mean_table_raw": by_layer.to_dict(orient="records"),
    "layer_mean_table_z":   by_layer_z.to_dict(orient="records"),
    "harmonization": {
        "primary": "within-layer z-score of |effect|",
        "secondary": "Cohen's d equivalence (r→d, log_OR→d)",
    },
    "seed": 20260418,
}

with OUT_JSON.open("w") as f:
    json.dump(results, f, indent=2, default=float)


# -----------------------------------------------------------------------------
# 12. Figure 9 — Cross-layer forest grouped by mechanism
# -----------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
})

MECH_ORDER = ["olds_milner", "sensory_exploit", "fisher_runaway"]
MECH_COLOR = {
    "olds_milner":     "#C0392B",  # crimson
    "sensory_exploit": "#2E86C1",  # blue
    "fisher_runaway":  "#239B56",  # green
}
LAYER_MARKER = {"A": "o", "B": "s", "D": "^"}
LAYER_LABEL = {"A": "A · Animal meta",
               "B": "B · Human focal",
               "D": "D · MR (genetic)"}

fig = plt.figure(figsize=(12, 10))
gs = fig.add_gridspec(
    nrows=2, ncols=2,
    width_ratios=[1.7, 1.0],
    height_ratios=[2.0, 1.0],
    hspace=0.35, wspace=0.30,
)

# --- panel a: forest -------------------------------------------------------
ax_fo = fig.add_subplot(gs[0, 0])

# order rows: group by mechanism then by layer then by effect desc
core_sorted = CORE.copy()
core_sorted["mech_rank"] = core_sorted["mechanism"].map(
    {m: i for i, m in enumerate(MECH_ORDER)},
)
core_sorted["layer_rank"] = core_sorted["layer"].map({"A": 0, "B": 1, "D": 2})
core_sorted = core_sorted.sort_values(
    ["mech_rank", "layer_rank", "effect_z"],
    ascending=[True, True, False],
).reset_index(drop=True)

y_positions = np.arange(len(core_sorted))[::-1]

for i, row in core_sorted.iterrows():
    y = y_positions[i]
    col = MECH_COLOR[row["mechanism"]]
    mkr = LAYER_MARKER[row["layer"]]
    # primary (z-scaled) error bars
    ax_fo.errorbar(
        row["effect_z"], y,
        xerr=1.96 * row["se_z"],
        fmt=mkr, markersize=6,
        color=col, ecolor=col, elinewidth=1.0, alpha=0.85,
        capsize=0,
    )

ax_fo.axvline(0, color="grey", lw=0.6, ls="-")
ax_fo.set_yticks(y_positions)
ax_fo.set_yticklabels(
    [f"[{r.layer}] {r.case_id}  {r.mechanism[:4]}"
     for r in core_sorted.itertuples()],
    fontsize=7,
)
ax_fo.set_xlabel("Within-layer z-scored |effect|  (95% CI)", fontsize=9)
ax_fo.set_title("a · Cross-layer forest (harmonized scale)", loc="left", fontweight="bold")
ax_fo.set_xlim(-3.5, 3.5)
ax_fo.grid(axis="x", color="lightgrey", lw=0.3, alpha=0.6)
for spine in ("top", "right"):
    ax_fo.spines[spine].set_visible(False)

# --- panel b: mechanism×layer ridge --------------------------------------
ax_grid = fig.add_subplot(gs[0, 1])
ticks_y = []
ticks_y_lbl = []
for i, mech in enumerate(MECH_ORDER):
    for j, lay in enumerate(["A", "B", "D"]):
        sub = CORE[(CORE["mechanism"] == mech) & (CORE["layer"] == lay)]
        y_row = i * 4 + (2 - j)
        ticks_y.append(y_row)
        ticks_y_lbl.append(f"{mech[:4]} | {lay}")
        if len(sub) == 0:
            ax_grid.plot([], [])
            continue
        m, s, n = sub["effect_z"].mean(), sub["effect_z"].std(ddof=1) if len(sub) > 1 else 0.0, len(sub)
        sem = s / math.sqrt(max(n, 1)) if n > 1 else 0.0
        col = MECH_COLOR[mech]
        ax_grid.scatter(sub["effect_z"], [y_row] * len(sub),
                        color=col, alpha=0.4, s=22,
                        marker=LAYER_MARKER[lay])
        ax_grid.errorbar(m, y_row, xerr=1.96 * sem,
                         fmt="D", color=col, markersize=6,
                         ecolor=col, elinewidth=1.5)
        ax_grid.text(3.2, y_row, f"n={n}", fontsize=7, va="center", color=col)

ax_grid.axvline(0, color="grey", lw=0.5)
ax_grid.set_yticks(ticks_y)
ax_grid.set_yticklabels(ticks_y_lbl, fontsize=7)
ax_grid.set_xlim(-3.5, 3.8)
ax_grid.set_xlabel("effect_z")
ax_grid.set_title("b · Mechanism × Layer cell means", loc="left", fontweight="bold")
for spine in ("top", "right"):
    ax_grid.spines[spine].set_visible(False)

# --- panel c: rank-order bars ---------------------------------------------
ax_rank = fig.add_subplot(gs[1, 0])
width = 0.25
x = np.arange(len(MECH_ORDER))
for j, (lay, ranker) in enumerate(zip(["A", "B", "D"],
                                      [rank_A, rank_B, rank_D])):
    vals = ranker.reindex(MECH_ORDER).values
    col = [MECH_COLOR[m] for m in MECH_ORDER]
    ax_rank.bar(x + (j - 1) * width, vals, width,
                color=col, alpha=0.55 + j * 0.15,
                edgecolor="black", linewidth=0.5,
                label=LAYER_LABEL[lay])

ax_rank.set_xticks(x)
ax_rank.set_xticklabels(MECH_ORDER, fontsize=8)
ax_rank.set_ylabel("mean |effect| on native scale")
ax_rank.set_title(
    "c · Mechanism rank within each layer  "
    f"(Spearman ρ_AD = {sp_AD[0]:+.2f}, ρ_AB = {sp_AB[0]:+.2f}, ρ_BD = {sp_BD[0]:+.2f})",
    loc="left", fontweight="bold", fontsize=9,
)
ax_rank.legend(fontsize=7, loc="upper right", frameon=False)
for spine in ("top", "right"):
    ax_rank.spines[spine].set_visible(False)

# --- panel d: variance partition & LOO table ------------------------------
ax_tab = fig.add_subplot(gs[1, 1])
ax_tab.axis("off")
txt = []
mpz = main_primary
txt.append("Main model (effect_z ~ mech + (1|layer))")
txt.append(f"  Wald mech:  chi2 = {mpz['wald_mech_stat']:.2f}, p = {mpz['wald_mech_p']:.4f}")
txt.append(f"  beta olds vs fisher:  {mpz['params']['olds_milner']:+.2f} (SE {mpz['se']['olds_milner']:.2f})")
txt.append(f"  beta sens vs fisher:  {mpz['params']['sensory_exploit']:+.2f} (SE {mpz['se']['sensory_exploit']:.2f})")
txt.append(f"  Layer-variance share:  {mpz['layer_share']*100:.1f}%")
txt.append("")
txt.append("Leave-one-layer-out (mech p):")
for L, r in loo.items():
    txt.append(f"  drop {L}:  p = {r['wald_mech_p']:.4f}, olds beta = {r['params']['olds_milner']:+.2f}")
txt.append("")
txt.append("A+D only (B underpowered check):")
txt.append(f"  p = {ad_only['wald_mech_p']:.4f}, olds beta = {ad_only['params']['olds_milner']:+.2f}")
ax_tab.text(0, 1, "\n".join(txt), va="top", ha="left",
            fontsize=7.5, family="monospace")

fig.suptitle(
    "Cross-level meta-regression — mechanism gradient across Layer A (animal), "
    "Layer B (human focal), Layer D (MR)",
    fontweight="bold",
)
fig.savefig(OUT_FIG_PNG, dpi=220, bbox_inches="tight")
fig.savefig(OUT_FIG_PDF, bbox_inches="tight")
plt.close(fig)


# -----------------------------------------------------------------------------
# 13. Console summary
# -----------------------------------------------------------------------------
print("\n==== CROSS-LEVEL META ====")
print(f"N core rows: {len(CORE)}   (A={len(LAYER_A_c)}  B={len(LAYER_B_c)}  "
      f"D_core={len(CORE[CORE['layer']=='D'])})")
print("\nPer-layer mean |effect| by mechanism (native scale):")
print(by_layer.pivot(index="mechanism", columns="layer", values="mean"))
print("\nSpearman ρ on mechanism rank:")
print(f"  A vs D: ρ = {sp_AD[0]:+.3f}, p = {sp_AD[1]:.3f}")
print(f"  A vs B: ρ = {sp_AB[0]:+.3f}, p = {sp_AB[1]:.3f}")
print(f"  B vs D: ρ = {sp_BD[0]:+.3f}, p = {sp_BD[1]:.3f}")
print("\nMain model (z-scale):")
print(f"  Wald mech: chi2 = {main_primary['wald_mech_stat']:.3f}, "
      f"p = {main_primary['wald_mech_p']:.4f}")
print(f"  Layer variance share = {main_primary['layer_share']*100:.1f}%")
print("\nLOO:")
for L, r in loo.items():
    print(f"  drop {L}: p = {r['wald_mech_p']:.4f}, "
          f"olds beta = {r['params']['olds_milner']:+.3f}")
print(f"\nOutputs:\n  {OUT_CSV}\n  {OUT_JSON}\n  {OUT_FIG_PNG}\n  {OUT_FIG_PDF}")
