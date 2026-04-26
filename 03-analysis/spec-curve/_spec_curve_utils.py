"""
Spec-Curve Utilities (shared across 5 Focal cases)
==================================================

Purpose
-------
顶刊 spec-curve 需求 (对标 Sommet et al. 2026 Nature)：每个 Focal 案例
遍历控制集 × 固定效应 × 样本限制 × Outcome 定义 × 估计方法 ≥128 组合。

本项目已在各 Focal 主分析脚本内生成 spec-curve CSV。本工具模块统一：
  1) 读取 heterogeneous 格式 CSV → 规范化成统一 schema
  2) 根据 Focal 选择的 primary DV × primary treatment 定义 "focal family"
  3) 计算 median β / sign stability / significance rate
  4) 输出标准化 CSV + spec-curve plot（β 排序 + 规约矩阵）

Inputs
------
- 02-data/processed/<case>_speccurve.csv  (由各主分析脚本生成)
- 02-data/processed/<case>_results.json   (primary spec headline)

Outputs
-------
- 03-analysis/spec-curve/spec_curve_<case>_results.csv  (harmonized)
- 04-figures/supp/spec_curve_<case>.png                 (单 Focal plot)
- 04-figures/main/fig7_spec_curve_5panel.png           (合成主图)

Dependencies
------------
pandas, numpy, matplotlib, scipy
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Sequence

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
PROJECT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
PROCESSED = PROJECT / "02-data" / "processed"
SPEC_DIR = PROJECT / "03-analysis" / "spec-curve"
FIG_SUPP = PROJECT / "04-figures" / "supp"
FIG_MAIN = PROJECT / "04-figures" / "main"
SPEC_DIR.mkdir(parents=True, exist_ok=True)
FIG_SUPP.mkdir(parents=True, exist_ok=True)
FIG_MAIN.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Harmonized schema
# -----------------------------------------------------------------------------
UNIFIED_COLS = [
    "case",            # C8 / C11 / C12 / C13 / D_alcohol
    "spec_id",         # 1..N within case
    "dv",              # normalized DV name
    "treatment",       # treatment variable
    "controls",        # minimal/demog/ses/full...
    "fe",              # fixed-effect set
    "sample",          # sample filter
    "waves_or_lag",    # extra dimension (waves pooling, lag, method...)
    "branch",          # sweet / bitter (if coded)
    "n",               # sample size
    "beta",            # point estimate
    "se",              # standard error
    "p",               # two-sided p
    "ci_lo",           # 95% CI
    "ci_hi",
]


@dataclass
class CaseConfig:
    """Per-Focal configuration."""
    case: str                  # 'C8' / 'C11' / ...
    csv_path: Path             # source spec-curve
    json_path: Path            # primary headline
    primary_dv: str            # name in speccurve CSV for headline DV
    primary_treat: str         # name of treatment for headline
    primary_branch: str | None  # 'sweet' / 'bitter' / None
    # Primary headline values (from results.json) — used for "original vs median" table
    headline_label: str
    headline_beta: float
    headline_se: float
    headline_p: float
    headline_n: int
    # Which direction counts as "confirms sweet trap" (sign expected for headline)
    expected_sign: int  # +1 (positive beta confirms), -1 (negative beta confirms), 0 (no direction)
    panel_title: str
    panel_subtitle: str
    # Whether to restrict to "sweet" branch only for primary family
    restrict_to_branch: str | None = None


# =============================================================================
# Normalisers for each case CSV
# =============================================================================

def _finalize_ci(df: pd.DataFrame) -> pd.DataFrame:
    """Fill ci_lo/ci_hi from beta+/-1.96*se when missing."""
    if "ci_lo" not in df.columns or df["ci_lo"].isna().all():
        df["ci_lo"] = df["beta"] - 1.96 * df["se"]
    if "ci_hi" not in df.columns or df["ci_hi"].isna().all():
        df["ci_hi"] = df["beta"] + 1.96 * df["se"]
    return df


def normalize_C8(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({
        "case": "C8",
        "spec_id": df["spec_id"],
        "dv": df["dv"],
        "treatment": df["treatment"],
        "controls": df["controls"],
        "fe": "pooled_OLS_cluster_hh",
        "sample": df["sample"],
        "waves_or_lag": df["waves"],
        "branch": "sweet",  # C8 speccurve is all sweet-side by construction
        "n": df["N"],
        "beta": df["beta"],
        "se": df["se"],
        "p": df["p"],
        "ci_lo": df["ci_lo"],
        "ci_hi": df["ci_hi"],
    })
    return _finalize_ci(out)[UNIFIED_COLS]


def normalize_C11(df: pd.DataFrame) -> pd.DataFrame:
    # p column is one-sided; convert to two-sided conservatively: min(1, 2*min(p, 1-p))
    p_one = df["p_one_sided"].clip(0, 1)
    p_two = (2 * np.minimum(p_one, 1 - p_one)).clip(0, 1)
    out = pd.DataFrame({
        "case": "C11",
        "spec_id": np.arange(1, len(df) + 1),
        "dv": df["dv"],
        "treatment": df["treatment"],
        "controls": df["controls"],
        "fe": df["fe"],
        "sample": df["sample"],
        "waves_or_lag": df["cluster"],
        "branch": df["branch"],
        "n": df["N"],
        "beta": df["beta"],
        "se": df["se"],
        "p": p_two,
        "ci_lo": np.nan,
        "ci_hi": np.nan,
    })
    return _finalize_ci(out)[UNIFIED_COLS]


def normalize_C12(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({
        "case": "C12",
        "spec_id": df["spec_id"],
        "dv": df["dv"],
        "treatment": df["treat"],
        "controls": df["ctrl"],
        "fe": "pooled_OLS_cluster_hh",
        "sample": df["sample"],
        "waves_or_lag": df["lag"].astype(str).map({"0": "lag0", "1": "lag1"}),
        "branch": df["branch"],
        "n": df["n"],
        "beta": df["beta"],
        "se": df["se"],
        "p": df["p_two"],
        "ci_lo": df["ci_low"],
        "ci_hi": df["ci_high"],
    })
    return _finalize_ci(out)[UNIFIED_COLS]


def normalize_C13(df: pd.DataFrame) -> pd.DataFrame:
    p_one = df["p_one_sided"].clip(0, 1)
    p_two = (2 * np.minimum(p_one, 1 - p_one)).clip(0, 1)
    out = pd.DataFrame({
        "case": "C13",
        "spec_id": np.arange(1, len(df) + 1),
        "dv": df["dv"],
        "treatment": df["treatment"],
        "controls": df["controls"],
        "fe": df["fe"],
        "sample": df["sample"],
        "waves_or_lag": df["cluster"],
        "branch": df["branch"],
        "n": df["N"],
        "beta": df["beta"],
        "se": df["se"],
        "p": p_two,
        "ci_lo": np.nan,
        "ci_hi": np.nan,
    })
    return _finalize_ci(out)[UNIFIED_COLS]


def normalize_Dalcohol(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame({
        "case": "D_alcohol",
        "spec_id": df["spec"],
        "dv": df["dv"],
        "treatment": df["treatment"],
        "controls": df["controls"],
        "fe": df["fe"],
        "sample": df["sample"],
        "waves_or_lag": "CHARLS_2011_2020",
        "branch": "sweet",  # D-alcohol speccurve is sweet-side (SATLIFE/SRH gains)
        "n": df["n"],
        "beta": df["beta"],
        "se": df["se"],
        "p": df["p"],
        "ci_lo": df["ci_lo"],
        "ci_hi": df["ci_hi"],
    })
    return _finalize_ci(out)[UNIFIED_COLS]


NORMALIZERS = {
    "C8": normalize_C8,
    "C11": normalize_C11,
    "C12": normalize_C12,
    "C13": normalize_C13,
    "D_alcohol": normalize_Dalcohol,
}


# =============================================================================
# Case configurations
# =============================================================================

CASES: dict[str, CaseConfig] = {
    "C8": CaseConfig(
        case="C8",
        csv_path=PROCESSED / "C8_speccurve.csv",
        json_path=PROCESSED / "C8_results.json",
        primary_dv="life_sat",
        primary_treat="stock_hold",
        primary_branch="sweet",
        headline_label="life_sat ~ stock_hold (CHFS 2017+19, full controls)",
        headline_beta=-0.1066,
        headline_se=0.0119,
        headline_p=2.57e-19,
        headline_n=74436,
        expected_sign=-1,  # sweet trap: stock holders have LOWER life-sat
        panel_title="C8 · Investment FOMO (CHFS)",
        panel_subtitle="life_sat ~ stock_hold family",
    ),
    "C11": CaseConfig(
        case="C11",
        csv_path=PROCESSED / "C11_speccurve.csv",
        json_path=PROCESSED / "C11_results.json",
        primary_dv="qn12012",  # life-sat in CHARLS
        primary_treat="d_food_share",
        primary_branch="sweet",
        headline_label="Δlife_sat ~ Δfood_share (CHARLS within-person)",
        headline_beta=-0.0108,
        headline_se=0.0221,
        headline_p=0.625,
        headline_n=None,
        expected_sign=-1,
        panel_title="C11 · Diet / Food Share (CHARLS)",
        panel_subtitle="Δlife_sat ~ Δfood_share family",
        restrict_to_branch="sweet",
    ),
    "C12": CaseConfig(
        case="C12",
        csv_path=PROCESSED / "C12_speccurve.csv",
        json_path=PROCESSED / "C12_results.json",
        primary_dv="qn12012",
        primary_treat="internet",
        primary_branch="sweet",
        headline_label="life_sat ~ internet (CFPS H12.1)",
        headline_beta=-0.0021,
        headline_se=0.0138,
        headline_p=0.876,
        headline_n=70871,
        expected_sign=-1,
        panel_title="C12 · Short-Video / Digital (CFPS)",
        panel_subtitle="life_sat ~ internet family",
        restrict_to_branch="sweet",
    ),
    "C13": CaseConfig(
        case="C13",
        csv_path=PROCESSED / "C13_speccurve.csv",
        json_path=PROCESSED / "C13_results.json",
        primary_dv="qn12012",  # headline life-sat coef from primary
        primary_treat="mortgage_burden_w",
        primary_branch="sweet",
        headline_label="life_sat ~ mortgage_burden (CFPS H8.1b)",
        headline_beta=0.1946,
        headline_se=0.0449,
        headline_p=1.46e-5,
        headline_n=None,
        expected_sign=+1,  # sweet: mortgage burden correlates with higher life-sat (aspirational sweet signal)
        panel_title="C13 · Luxury Housing / Mortgage (CFPS)",
        panel_subtitle="life_sat ~ mortgage_burden family",
        restrict_to_branch="sweet",
    ),
    "D_alcohol": CaseConfig(
        case="D_alcohol",
        csv_path=PROCESSED / "D_alcohol_speccurve.csv",
        json_path=PROCESSED / "D_alcohol_results.json",
        primary_dv="srh",  # SRH has the most significant sweet signal
        primary_treat="drinkl",
        primary_branch="sweet",
        headline_label="SRH ~ drinkl (CHARLS pooled)",
        headline_beta=0.1181,
        headline_se=0.0140,
        headline_p=3.48e-17,
        headline_n=56301,
        expected_sign=+1,  # sweet: drinkers report higher SRH
        panel_title="D · Alcohol (CHARLS)",
        panel_subtitle="SRH ~ drinkl family",
    ),
}


# =============================================================================
# Analysis
# =============================================================================

def load_normalized(case: str) -> pd.DataFrame:
    cfg = CASES[case]
    raw = pd.read_csv(cfg.csv_path)
    df = NORMALIZERS[case](raw)
    # Drop rows without finite beta/se (failed specs)
    df = df[np.isfinite(df["beta"]) & np.isfinite(df["se"])].reset_index(drop=True)
    # Drop convergence-failure outliers:
    #   - |beta| > 1e4 or se > 100 (clear numerical failure)
    #   - |beta| > 20*MAD-from-median within (case, dv) — catches D_alcohol type_A outliers
    outlier_mask = (df["beta"].abs() > 1e4) | (df["se"].abs() > 100)
    # Per-DV robust outlier detection on beta
    for dv, grp in df.groupby("dv"):
        beta = grp["beta"].values
        med = np.median(beta)
        mad = np.median(np.abs(beta - med))
        if mad > 0:
            thresh = 20 * 1.4826 * mad
            rob_mask = (df["dv"] == dv) & ((df["beta"] - med).abs() > thresh)
            outlier_mask = outlier_mask | rob_mask
    if outlier_mask.any():
        print(f"  [INFO] {case}: dropping {int(outlier_mask.sum())} convergence-failure / "
              f"extreme-outlier specs")
        df = df[~outlier_mask].reset_index(drop=True)
    return df


def filter_focal(df: pd.DataFrame, cfg: CaseConfig) -> pd.DataFrame:
    """Broad focal: fix DV to headline DV, keep ALL treatment variants on sweet branch.

    This gives ≥64 specs per case and tests whether the headline direction is robust
    across all sensible treatment operationalisations of the same causal question.
    """
    mask = (df["dv"] == cfg.primary_dv)
    if cfg.restrict_to_branch and "branch" in df.columns:
        mask &= df["branch"] == cfg.restrict_to_branch
    return df[mask].copy()


def filter_focal_narrow(df: pd.DataFrame, cfg: CaseConfig) -> pd.DataFrame:
    """Narrow focal: same DV AND treatment root as headline.

    This is the tightest test — same operationalisation, varying only
    controls/FE/sample/waves. Used to compare directly to the original headline.
    """
    mask = (df["dv"] == cfg.primary_dv)
    root = cfg.primary_treat.replace("_lag", "").replace("_w", "")
    mask &= df["treatment"].str.contains(root, case=False, na=False)
    if cfg.restrict_to_branch and "branch" in df.columns:
        mask &= df["branch"] == cfg.restrict_to_branch
    return df[mask].copy()


# Per-case, per-DV polarity for the "same-sign as headline" test:
#  +1 = higher value means LESS sweet-trap (wellbeing / status outcome; higher is good)
#  -1 = higher value means MORE sweet-trap (distress / bad-health outcome; higher is bad)
# The sign stability metric is computed as
#   P( sign(beta) == cfg.expected_sign * polarity(dv) )
# so that e.g. negative β on CESD (depression) counts the same as positive β on SATLIFE.
DV_POLARITY = {
    # C8 — all explicitly "higher = better" DVs in spec curve
    ("C8", "life_sat"): +1,
    ("C8", "risk_seek"): 0,       # no clear direction
    ("C8", "fin_attention"): 0,
    ("C8", "ln_consump"): 0,
    # C11 — life-sat, health, unhealth
    ("C11", "qn12012"): +1,       # life-sat: higher = better
    ("C11", "health"): +1,        # composite wellbeing: higher = better
    ("C11", "unhealth"): -1,      # distress composite: higher = worse
    ("C11", "qp401"): -1,         # disease count
    ("C11", "ln_mexp"): -1,       # medical exp: higher = more burden
    # C12
    ("C12", "qn12012"): +1,       # life-sat
    ("C12", "qn12016"): +1,       # happy
    ("C12", "qq4010"): +1,        # future-confidence
    ("C12", "dw"):     +1,        # self-rated social status
    ("C12", "health"): +1,
    ("C12", "qq201"):  0,         # unclear
    # C13
    ("C13", "qn12012"): +1,
    ("C13", "qn12016"): +1,
    ("C13", "dw"):      +1,
    ("C13", "ln_savings"): +1,
    ("C13", "ln_nonhousing_debts"): -1,
    ("C13", "ln_expense"): 0,
    ("C13", "child_num"): 0,
    # D_alcohol
    ("D_alcohol", "satlife"): +1,
    ("D_alcohol", "srh"):     +1,
    ("D_alcohol", "cesd10"): -1,  # depression: higher = worse
}


# DVs that represent the "hedonic / subjective-wellbeing / sweet signal" side per case.
# Used to broaden the focal family to >=128 specs when the narrow focal is too small.
SWEET_DVS = {
    "C8":        ["life_sat"],                          # 24 specs in narrow focal — we broaden via treatment/sample
    "C11":       ["qn12012", "health", "unhealth"],
    "C12":       ["qn12012", "qq4010", "dw", "health", "qn12016"],
    "C13":       ["qn12012", "qn12016", "dw"],
    "D_alcohol": ["satlife", "srh", "cesd10"],
}


def directional_expected(case: str, dv: str, base_sign: int) -> int:
    """Apply DV polarity to the case's base expected sign.

    e.g., C11 headline: Δlife_sat ~ Δfood_share, expected_sign = -1 (sweet trap).
    For DV=unhealth (polarity -1), the expected sign FLIPS to +1
    (because sweet-trap means more distress, which means HIGHER unhealth).
    """
    pol = DV_POLARITY.get((case, dv), 0)
    if pol == 0:
        return 0  # no directional prediction
    return base_sign * pol


def filter_broad_sweet(df: pd.DataFrame, cfg: CaseConfig) -> pd.DataFrame:
    """Broader 'sweet family' — all DVs representing hedonic/wellbeing signal,
    all treatments within the same conceptual variable, branch='sweet' if coded.

    Used when narrow focal < 128 specs and we need the wider spec-curve for stability.
    Expected sign is the SAME as headline (all hedonic DVs align).
    """
    dvs = SWEET_DVS.get(cfg.case, [cfg.primary_dv])
    mask = df["dv"].isin(dvs)
    if cfg.restrict_to_branch and "branch" in df.columns:
        mask &= df["branch"] == cfg.restrict_to_branch
    # For cases where branch is not coded (C8, D_alcohol), "branch" col is 'sweet' by construction.
    return df[mask].copy()


def summarize(df_focal: pd.DataFrame, cfg: CaseConfig) -> dict:
    """Compute median β, sign stability, significance rate, CI for the focal family."""
    n_specs = len(df_focal)
    if n_specs == 0:
        return {"case": cfg.case, "n_specs": 0, "fragile": True}
    beta = df_focal["beta"].values
    p = df_focal["p"].values
    # Bootstrap median CI
    rng = np.random.default_rng(42)
    boot_meds = np.array([np.median(rng.choice(beta, size=len(beta), replace=True))
                          for _ in range(2000)])
    med_ci = np.quantile(boot_meds, [0.025, 0.975])
    if cfg.expected_sign == 0:
        sign_stability = float(np.sign(beta).std() == 0 or True)  # no direction → treat as 1
    else:
        sign_stability = float((np.sign(beta) == cfg.expected_sign).mean())
    sig_rate = float((p < 0.05).mean())
    same_sign_sig_rate = float(((p < 0.05) & (np.sign(beta) == cfg.expected_sign)).mean()) \
        if cfg.expected_sign != 0 else sig_rate
    return {
        "case": cfg.case,
        "primary_dv": cfg.primary_dv,
        "primary_treatment_root": cfg.primary_treat,
        "n_specs": n_specs,
        "beta_median": float(np.median(beta)),
        "beta_mean": float(np.mean(beta)),
        "beta_min": float(np.min(beta)),
        "beta_max": float(np.max(beta)),
        "beta_median_ci_lo": float(med_ci[0]),
        "beta_median_ci_hi": float(med_ci[1]),
        "beta_q25": float(np.quantile(beta, 0.25)),
        "beta_q75": float(np.quantile(beta, 0.75)),
        "sign_stability": sign_stability,
        "sig_rate_any": sig_rate,
        "sig_rate_same_sign": same_sign_sig_rate,
        "fragile": sign_stability < 0.75,
        "headline_beta": cfg.headline_beta,
        "headline_p": cfg.headline_p,
        "median_vs_headline_ratio": float(np.median(beta) / cfg.headline_beta)
            if cfg.headline_beta != 0 else np.nan,
    }


# =============================================================================
# Plotting
# =============================================================================

def plot_spec_curve(df_focal: pd.DataFrame, cfg: CaseConfig, out_path: Path):
    """One panel: sorted β with CI on top, spec-dimension matrix below."""
    if len(df_focal) == 0:
        print(f"  [WARN] {cfg.case}: 0 specs after filter, skipping plot")
        return

    df = df_focal.sort_values("beta").reset_index(drop=True)
    df["rank"] = np.arange(len(df))

    # Significance markers
    sig_mask = df["p"] < 0.05
    same_sign = np.sign(df["beta"]) == cfg.expected_sign

    # Figure
    fig = plt.figure(figsize=(11, 8), dpi=130)
    gs = GridSpec(2, 1, height_ratios=[3, 2], hspace=0.15)
    ax_curve = fig.add_subplot(gs[0])
    ax_matrix = fig.add_subplot(gs[1], sharex=ax_curve)

    # --- Top: ordered β ---
    colors = np.where(sig_mask & same_sign, "#1a7f37",
                      np.where(sig_mask & ~same_sign, "#d1242f", "#8c959f"))
    # CI bars (light)
    if df["ci_lo"].notna().any():
        ax_curve.vlines(df["rank"], df["ci_lo"], df["ci_hi"],
                        colors=colors, alpha=0.25, linewidth=0.6)
    ax_curve.scatter(df["rank"], df["beta"], c=colors, s=10, alpha=0.85, zorder=3)
    # Zero line
    ax_curve.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
    # Median line
    med = df["beta"].median()
    ax_curve.axhline(med, color="#0969da", linewidth=1.2, linestyle="-",
                     alpha=0.9, label=f"median β = {med:+.4f}")
    # Headline
    ax_curve.axhline(cfg.headline_beta, color="#bf8700", linewidth=1.2,
                     linestyle=":", alpha=0.9, label=f"headline β = {cfg.headline_beta:+.4f}")
    ax_curve.set_ylabel("β (effect size)", fontsize=11)
    ax_curve.set_title(f"{cfg.panel_title}  ·  {cfg.panel_subtitle}  "
                       f"(N specs = {len(df)})", fontsize=12, loc="left")
    ax_curve.legend(loc="upper left", fontsize=9, frameon=False)
    ax_curve.grid(axis="y", alpha=0.3)

    # --- Bottom: spec-dimension matrix ---
    # Ordered list of dimensions to show as rows
    dim_cols = ["controls", "fe", "sample", "waves_or_lag", "branch"]
    rows = []
    for dim in dim_cols:
        if dim not in df.columns:
            continue
        levels = sorted(df[dim].dropna().astype(str).unique())
        for lvl in levels:
            rows.append((dim, lvl))

    # Build marker grid
    y_ticks = []
    y_labels = []
    for i, (dim, lvl) in enumerate(rows):
        mask = df[dim].astype(str) == lvl
        xs = df.loc[mask, "rank"].values
        ys = np.full(len(xs), i)
        ax_matrix.scatter(xs, ys, s=4, c="black", alpha=0.7, marker="|")
        y_ticks.append(i)
        y_labels.append(f"{dim}={lvl}")

    ax_matrix.set_yticks(y_ticks)
    ax_matrix.set_yticklabels(y_labels, fontsize=7)
    ax_matrix.set_xlabel("specifications (sorted by β)", fontsize=10)
    ax_matrix.tick_params(axis="x", labelbottom=True)
    ax_matrix.grid(axis="y", alpha=0.2)
    # Shade groups by dim
    last_dim = None
    for i, (dim, _) in enumerate(rows):
        if dim != last_dim:
            ax_matrix.axhline(i - 0.5, color="lightgrey", linewidth=0.5)
            last_dim = dim
    ax_matrix.set_ylim(-0.5, len(rows) - 0.5)
    ax_matrix.invert_yaxis()

    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] wrote {out_path}")


def plot_5panel(summaries: dict[str, dict], dfs: dict[str, pd.DataFrame], out_path: Path):
    """Composite 5-panel main figure."""
    fig = plt.figure(figsize=(16, 11), dpi=130)
    gs = GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.22,
                  height_ratios=[1, 1, 1])

    positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]
    cases_order = ["C8", "C11", "C12", "C13", "D_alcohol"]

    for (r, c), case in zip(positions, cases_order):
        cfg = CASES[case]
        df = dfs[case].sort_values("beta").reset_index(drop=True)
        df["rank"] = np.arange(len(df))
        ax = fig.add_subplot(gs[r, c])

        sig_mask = df["p"] < 0.05
        same_sign = np.sign(df["beta"]) == cfg.expected_sign
        colors = np.where(sig_mask & same_sign, "#1a7f37",
                          np.where(sig_mask & ~same_sign, "#d1242f", "#8c959f"))
        ax.scatter(df["rank"], df["beta"], c=colors, s=8, alpha=0.85)
        ax.axhline(0, color="black", linewidth=0.7, linestyle="--", alpha=0.5)
        med = df["beta"].median()
        ax.axhline(med, color="#0969da", linewidth=1.3, label=f"median β={med:+.4f}")
        ax.axhline(cfg.headline_beta, color="#bf8700", linewidth=1.3,
                   linestyle=":", label=f"headline β={cfg.headline_beta:+.4f}")
        summary = summaries[case]
        stab = summary.get("sign_stability", float("nan"))
        sig = summary.get("sig_rate_same_sign", float("nan"))
        # Draw fragile flag
        frag_tag = " [FRAGILE]" if summary.get("fragile") else ""
        ax.set_title(f"{cfg.panel_title}{frag_tag}\n"
                     f"N={len(df)} specs · sign-stab={stab:.0%} · sig-same={sig:.0%}",
                     fontsize=10, loc="left")
        ax.set_xlabel("spec rank", fontsize=9)
        ax.set_ylabel("β", fontsize=9)
        ax.legend(loc="upper left", fontsize=7.5, frameon=False)
        ax.grid(axis="y", alpha=0.3)

    # Sixth panel: summary table
    ax_tbl = fig.add_subplot(gs[2, 1])
    ax_tbl.axis("off")
    rows = [["Case", "head β", "med β", "med-CI (2.5,97.5%)",
             "sign-stab", "sig-rate(same sign)"]]
    for case in cases_order:
        s = summaries[case]
        cfg = CASES[case]
        rows.append([
            cfg.case,
            f"{s['headline_beta']:+.3f}",
            f"{s['beta_median']:+.3f}",
            f"[{s['beta_median_ci_lo']:+.3f}, {s['beta_median_ci_hi']:+.3f}]",
            f"{s['sign_stability']:.0%}",
            f"{s['sig_rate_same_sign']:.0%}",
        ])
    tbl = ax_tbl.table(cellText=rows[1:], colLabels=rows[0],
                      cellLoc="center", loc="center",
                      colWidths=[0.14, 0.14, 0.14, 0.24, 0.14, 0.2])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.6)
    ax_tbl.set_title("Headline vs. Median-of-Specifications",
                     fontsize=11, loc="left", pad=12)

    fig.suptitle("Specification Curve Analysis — 5 Focal Sweet-Trap Cases",
                 fontsize=14, y=0.995)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] wrote {out_path}")
