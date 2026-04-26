"""
Discriminant Validity Analysis — Sweet Trap Construct v2

Purpose:
  Build empirical confusion matrix for the F1-F4 classifier on 10 cases
  (5 positive controls = known Sweet Traps; 5 negative controls = systematic
  non-Sweet-Traps that share surface features). Report sensitivity,
  specificity, accuracy, Cohen's kappa. Perform leave-one-out cross-validation
  and threshold sensitivity analysis.

Inputs:
  - F1-F4 feature vectors derived from PDE evidence (hand-coded below with
    explicit provenance comment tags; NOT tuned to match outcome).
  - Ground-truth labels from pre-analysis PDE verdicts (00-design/pde/*.md).

Outputs:
  - 02-data/processed/discriminant_validity_features.csv
  - 02-data/processed/discriminant_validity_metrics.json
  - 03-analysis/models/discriminant_confusion_matrix.csv
  - Console report (stdout + written to .log)

Dependencies:
  Python 3.9+, pandas, numpy, sklearn (no parallelism required).

Author: Claude (Opus 4.7) for sweet-trap-multidomain project
Date: 2026-04-18
"""

from __future__ import annotations

import json
import logging
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    roc_auc_score,
)

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
PROJECT_ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
OUT_FEATURES = PROJECT_ROOT / "02-data" / "processed" / "discriminant_validity_features.csv"
OUT_METRICS = PROJECT_ROOT / "02-data" / "processed" / "discriminant_validity_metrics.json"
OUT_CM = PROJECT_ROOT / "03-analysis" / "models" / "discriminant_confusion_matrix.csv"
LOG_FILE = PROJECT_ROOT / "03-analysis" / "scripts" / "discriminant_validity.log"

for p in [OUT_FEATURES.parent, OUT_METRICS.parent, OUT_CM.parent, LOG_FILE.parent]:
    p.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, mode="w"), logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("discriminant")

# Fix seed for reproducibility of any downstream stochastic step
RNG_SEED = 20260418
np.random.seed(RNG_SEED)


# ----------------------------------------------------------------------------
# Feature vectors — each cell has a provenance tag (PDE file + section)
# ----------------------------------------------------------------------------
# Encoding convention:  0 = feature clearly NOT satisfied,
#                       0.5 = partial / marginal evidence,
#                       1 = feature clearly satisfied.
# F1 = reward-fitness decoupling (Δ_ST > 0 and CI excludes zero is ideal)
# F2 = voluntary endorsement (SES gradient positive; no coercion)
# F3 = self-reinforcing equilibrium (lock-in / AR1 / peer spread / policy-scale diffusion)
# F4 = absence of corrective feedback (cost lagged or borne by another agent)
# ----------------------------------------------------------------------------


@dataclass
class Case:
    case_id: str
    label_text: str
    is_sweet_trap: int  # ground-truth: 1 = Sweet Trap, 0 = Not Sweet Trap
    F1: float
    F2: float
    F3: float
    F4: float
    role: str  # "positive_control" | "negative_control"
    provenance: Dict[str, str]


CASES: List[Case] = [
    # -------------------- Positive controls (5) --------------------
    Case(
        case_id="C8",
        label_text="Investment FOMO (stock market)",
        is_sweet_trap=1,
        F1=1.0,  # Δ_ST = +0.060 [+0.024, +0.098] CI excludes 0
        F2=1.0,  # 7/7 F2 gates pass; 8× income gradient in stock participation
        F3=1.0,  # P(continue|last-wave loss) = 0.718; ρ lock-in strong
        F4=1.0,  # cor(financial-attention, return) = −0.094 (p = 0.00014)
        role="positive_control",
        provenance={
            "F1": "C8_investment_findings.md §0 TL;DR Δ_ST=+0.060 95%CI[+0.024,+0.098]",
            "F2": "C8 §0 F2 pre-gate 7/7 pass; stock participation 1.9/4.3/15.7% by income tercile",
            "F3": "C8 §0 P(continue|loss)=0.718; 55.8% non-exit 6y after 2015 crash",
            "F4": "C8 §0 cor(news_attention, return)=−0.094 → information channel inverted",
        },
    ),
    Case(
        case_id="C11",
        label_text="Sugar/fat/salt diet",
        is_sweet_trap=1,
        F1=0.5,  # CFPS share null / wrong-sign; CHARLS ln_food β = +0.059 positive
        F2=1.0,  # 91.7% of spec curve on ln_food → qn12012 positive; voluntary
        F3=1.0,  # within-person AR1 food_share = 0.251; habit lock-in
        F4=1.0,  # chronic disease lag ~10-20 y; biomarker (HbA1c) independent
        role="positive_control",
        provenance={
            "F1": "C11_diet_findings.md §0 Δ_ST mixed: share −0.023, ln_food Sweet 79% Bonf-pass",
            "F2": "C11 §0 ln_food × qn12012 91.7% positive specs; F2 voluntary by construction",
            "F3": "C11 §0 food_share within-person AR1 = 0.251 habit stickiness",
            "F4": "C11 §0 ln_mexp × food_share_lag 100% positive → medical cost deferred",
        },
    ),
    Case(
        case_id="C12",
        label_text="Short-video / algorithmic attention",
        is_sweet_trap=1,
        F1=1.0,  # Δ_ST(internet→qn12012)=+0.120 [+0.105,+0.136]; 3 DVs CI exclude 0
        F2=1.0,  # 10/10 F2 gates; cor(internet, eduy)=+0.50 strongest of any domain
        F3=1.0,  # ρ AR1 = 0.71 (strongest Layer B); 10.2% exit rate
        F4=0.5,  # Bitter null within-FE; sleep −0.23~−0.45h cross-section only
        role="positive_control",
        provenance={
            "F1": "C12_shortvideo_findings.md §0 Δ_ST=+0.120 3 DVs CI exclude 0",
            "F2": "C12 §0 F2 10/10 pass; strongest SES gradient cor(internet,eduy)=+0.50",
            "F3": "C12 §0 AR1 digital_intensity = 0.71; exit rate 10.2%",
            "F4": "C12 §0 Bitter within-FE null; cross-sec sleep −0.23–0.45h; composition masking",
        },
    ),
    Case(
        case_id="C13",
        label_text="Status housing / mortgage upgrading",
        is_sweet_trap=1,
        F1=1.0,  # Δ_ST all primary DVs positive; e.g., ln_resivalue→dw = +0.068 [+0.051,+0.085]
        F2=1.0,  # 7/7 F2 strict gates pass; cor(mortgage_burden, ln_income) = +0.097
        F3=1.0,  # ρ=0.44–0.45 within-pid; only 17% exit in 6 y — highest lock-in
        F4=1.0,  # debt crowd-IN into non-housing debt β=+0.93 (p=0.005) — deferred cost
        role="positive_control",
        provenance={
            "F1": "C13_housing_findings.md §0 all primary DVs Δ_ST ∈ [+0.05,+0.11] CI>0",
            "F2": "C13 §0 F2 7/7; mortgage positive SES gradient across edu/urban/income",
            "F3": "C13 §0 ρ AR1 = 0.44-0.45; exit rate 17% in 6y — highest durability",
            "F4": "C13 §0 non-housing debt crowd-IN β=+0.93 p=0.005 → cost realised via debt",
        },
    ),
    Case(
        case_id="D_alcohol_A",
        label_text="Alcohol — Type A aspirational/social drinkers",
        is_sweet_trap=1,
        F1=0.5,  # Δ_ST ≈ 0 pooled; event-study Δ_satlife = +0.14 on Type A entry (p=0.009)
        F2=1.0,  # Type A SES gradient positive: cor(r_inc)=+0.05, cor(r_edu)=+0.06
        F3=1.0,  # ρ=0.759 highest of all domains; cor(drinkn, drinkn_lag)=+0.713
        F4=0.5,  # liver disease lag exists but Type A has survivor bias (0% liver disease by construction)
        role="positive_control",
        provenance={
            "F1": "D_alcohol_findings.md §0 Δ_ST null pooled; event-study Type A satlife +0.14 p=0.009",
            "F2": "D_alcohol §0 Type A F2 positive SES gradient (vs Type C negative)",
            "F3": "D_alcohol §0 P(drinkl|drinkl_lag)=0.759 highest ρ across all cases",
            "F4": "D_alcohol §0 Type A 5y liver rate 4.8% < non-drinkers 7.2% — survivor-biased feedback",
        },
    ),
    # -------------------- Negative controls (5) --------------------
    Case(
        case_id="C2",
        label_text="Intensive parenting (鸡娃)",
        is_sweet_trap=0,
        F1=0.0,  # Δ_ST(eexp_share, qn12012) = −0.038 [−0.067, −0.010]; CI excludes positive
        F2=0.0,  # NEGATIVE SES gradient — low-edu/low-income/rural spend MORE share → coerced
        F3=0.0,  # Event-study shows MEAN-REVERSION not lock-in; high-baseline converges to low
        F4=0.5,  # Child psychological cost is deferred (if construct were right)
        role="negative_control",
        provenance={
            "F1": "C2_education_findings.md §0 Δ_ST=−0.038 95%CI[−0.067,−0.010] wrong sign",
            "F2": "C2 §0 eexp_share NEGATIVELY correlated with income/edu/urban — coerced, not aspirational",
            "F3": "C2 §0 event-study 2012-2018 mean-reverting; χ²=93.1 p<10⁻¹⁹ pretrend violation",
            "F4": "C2 construct: child mental health lagged if mechanism held (not observed)",
        },
    ),
    Case(
        case_id="C4",
        label_text="Marriage wealth transfer (彩礼)",
        is_sweet_trap=0,
        F1=0.0,  # Δ_ST = −0.04 to −0.11 wrong-sign in CGSS cohort decomposition
        F2=0.5,  # Partial — marital_sat β=+0.05 p=0.026 but λ interaction null; measurement-limited
        F3=0.5,  # Trans-generational norm transmission plausible but IV first-stage wrong-sign
        F4=0.5,  # Intergenerational cost transfer exists in principle
        role="negative_control",
        provenance={
            "F1": "C4_marriage_market_findings.md §0 Δ_ST=−0.04~−0.11 wrong-sign",
            "F2": "C4 §0 marital_sat β=+0.05 p=0.026 partial; life_sat null; happy p=0.056",
            "F3": "C4 §0 IV F=9.4 pooled; first-stage wrong-sign for sex ratio",
            "F4": "C4 §0 sibling externalisation null p=0.34",
        },
    ),
    Case(
        case_id="D3",
        label_text="996 compulsory overwork",
        is_sweet_trap=0,
        F1=0.0,  # within-person β(qg406)=−0.074 [−0.103,−0.044]; wrong sign, falsified
        F2=0.0,  # COERCED — workers endorse wage, not hours; refusal cost = dismissal
        F3=1.0,  # Employer-side lock-in real; 54% of CFPS employed work ≥48h (modal)
        F4=1.0,  # Chronic disease β=+0.023 at 1-wave lag — feedback blocked
        role="negative_control",
        provenance={
            "F1": "D3_996_findings.md §0 β=−0.074 p=8.7e-7 wrong sign; one-sided p=1.000",
            "F2": "D3 §0 F1 falsification rule; coerced exposure (construct v2 §1.2)",
            "F3": "D3 §2 54% employed ≥48h modal; industry/employer level lock-in",
            "F4": "D3 §3 H3.2 β=+0.023 one-sided p=0.040 chronic disease lag positive",
        },
    ),
    Case(
        case_id="C1_staple",
        label_text="Basic staple food (subsistence rice/grain)",
        is_sweet_trap=0,
        F1=0.0,  # Fitness requires caloric intake — reward aligned with fitness by calibration
        F2=1.0,  # Voluntary consumption; everyone eats
        F3=0.5,  # Mild habit formation but bounded by satiety
        F4=0.0,  # IMMEDIATE feedback: satiety, nausea if over; no temporal blocking
        role="negative_control",
        provenance={
            "F1": "phenomenology_archive.md §D5 structural poverty trap distinct; staple calorie needs → cor(R,F) > 0",
            "F2": "construct_v2 §1.2 voluntary consumption; no coercion",
            "F3": "sweet_trap_formal_model_v2 §1 F3 bounded by satiety; no accelerating π dynamics",
            "F4": "construct_v2 §1 F4 T_cost ≈ T_reward within meal; immediate satiety signal",
        },
    ),
    Case(
        case_id="C16_vaccine",
        label_text="Routine vaccination",
        is_sweet_trap=0,
        F1=0.0,  # Strong POSITIVE fitness benefit — inverse of Sweet Trap (Δ_ST < 0 by evolution)
        F2=1.0,  # Voluntary in most regimes; compliance driven by belief/endorsement
        F3=0.0,  # One-shot or periodic; no positive-feedback π dynamics
        F4=0.0,  # Immediate immune response (observable adverse events rare and quick);
        #          long-run protection directly observable in outbreak data
        role="negative_control",
        provenance={
            "F1": "construct v2 §1 F1 — vaccine reward (relief/compliance) is aligned with fitness, not decoupled",
            "F2": "standard public-health literature: voluntary uptake in non-mandate regimes",
            "F3": "one-shot / periodic schedule — no self-reinforcing π(a) dynamics",
            "F4": "immune response in days; epidemic protection observable within weeks (outbreak data)",
        },
    ),
]


def build_feature_frame(cases: List[Case]) -> pd.DataFrame:
    rows = []
    for c in cases:
        rows.append(
            {
                "case_id": c.case_id,
                "label_text": c.label_text,
                "role": c.role,
                "is_sweet_trap": c.is_sweet_trap,
                "F1": c.F1,
                "F2": c.F2,
                "F3": c.F3,
                "F4": c.F4,
                "F1_prov": c.provenance.get("F1", ""),
                "F2_prov": c.provenance.get("F2", ""),
                "F3_prov": c.provenance.get("F3", ""),
                "F4_prov": c.provenance.get("F4", ""),
            }
        )
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# Classifier: weighted sum over F1–F4
# ----------------------------------------------------------------------------
# The construct theory (sweet_trap_formal_model_v2 §1.5) asserts:
#   - F1 + F2 are NECESSARY (diagnostic core)
#   - F3 + F4 are TYPICAL (persistence features)
# Translate into weights: w_F1 = w_F2 = 2.0 (necessary), w_F3 = w_F4 = 1.0 (typical).
# Max score = 2×1 + 2×1 + 1×1 + 1×1 = 6.
# Baseline threshold T = 4.0 (requires near-full F1+F2 plus partial F3/F4, or
# full F1+F2 alone, to classify as Sweet Trap). Threshold sensitivity analysed.
# ----------------------------------------------------------------------------

WEIGHTS = np.array([2.0, 2.0, 1.0, 1.0])
THRESHOLDS = np.arange(2.5, 5.25, 0.25)
DEFAULT_THRESHOLD = 4.0


def score_cases(df: pd.DataFrame) -> np.ndarray:
    feats = df[["F1", "F2", "F3", "F4"]].to_numpy()
    return feats @ WEIGHTS


def classify(scores: np.ndarray, threshold: float) -> np.ndarray:
    return (scores > threshold).astype(int)


# ----------------------------------------------------------------------------
# Alternative: hard rule "F1 ≥ 0.5 AND F2 ≥ 0.5" (strict necessary-condition rule)
# ----------------------------------------------------------------------------


def classify_necessary_rule(df: pd.DataFrame, tau: float = 0.5) -> np.ndarray:
    """Hard rule: Sweet Trap requires F1 >= tau AND F2 >= tau."""
    return ((df["F1"] >= tau) & (df["F2"] >= tau)).astype(int).to_numpy()


# ----------------------------------------------------------------------------
# Metrics
# ----------------------------------------------------------------------------


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else float("nan")
    specificity = tn / (tn + fp) if (tn + fp) > 0 else float("nan")
    precision = tp / (tp + fp) if (tp + fp) > 0 else float("nan")
    npv = tn / (tn + fn) if (tn + fn) > 0 else float("nan")
    return {
        "TP": int(tp),
        "TN": int(tn),
        "FP": int(fp),
        "FN": int(fn),
        "accuracy": accuracy_score(y_true, y_pred),
        "sensitivity_recall": sensitivity,
        "specificity": specificity,
        "precision_PPV": precision,
        "NPV": npv,
        "F1_score": f1_score(y_true, y_pred, zero_division=0),
        "cohen_kappa": cohen_kappa_score(y_true, y_pred),
        "MCC": matthews_corrcoef(y_true, y_pred) if len(set(y_true)) > 1 and len(set(y_pred)) > 1 else float("nan"),
    }


def roc_auc_safe(y_true: np.ndarray, scores: np.ndarray) -> float:
    try:
        return roc_auc_score(y_true, scores)
    except Exception:
        return float("nan")


# ----------------------------------------------------------------------------
# Leave-one-out cross-validation (LOO-CV)
# ----------------------------------------------------------------------------


def loo_cv(df: pd.DataFrame, threshold: float) -> Dict[str, float]:
    """LOO-CV: with only 10 cases and a fixed weighted rule (no fitting),
    LOO is a robustness check: does misclassification concentrate on specific
    cases, or is the boundary stable?"""
    y_true = df["is_sweet_trap"].to_numpy()
    scores = score_cases(df)
    preds = classify(scores, threshold)
    per_case = []
    for i in range(len(df)):
        per_case.append(
            {
                "case_id": df.iloc[i]["case_id"],
                "label_text": df.iloc[i]["label_text"],
                "score": float(scores[i]),
                "pred": int(preds[i]),
                "truth": int(y_true[i]),
                "correct": int(preds[i] == y_true[i]),
            }
        )
    return {
        "threshold": threshold,
        "per_case": per_case,
        "overall": compute_metrics(y_true, preds),
        "roc_auc": roc_auc_safe(y_true, scores),
    }


# ----------------------------------------------------------------------------
# Threshold sweep
# ----------------------------------------------------------------------------


def threshold_sweep(df: pd.DataFrame) -> pd.DataFrame:
    y_true = df["is_sweet_trap"].to_numpy()
    scores = score_cases(df)
    records = []
    for T in THRESHOLDS:
        pred = classify(scores, T)
        m = compute_metrics(y_true, pred)
        records.append({"threshold": float(T), **m})
    return pd.DataFrame(records)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main() -> int:
    df = build_feature_frame(CASES)
    log.info("Feature frame built: %d cases (%d positive, %d negative)", len(df),
             int((df.is_sweet_trap == 1).sum()), int((df.is_sweet_trap == 0).sum()))
    log.info("Feature vectors:\n%s",
             df[["case_id", "role", "is_sweet_trap", "F1", "F2", "F3", "F4"]].to_string(index=False))

    # Save feature frame
    df.to_csv(OUT_FEATURES, index=False)
    log.info("Saved features -> %s", OUT_FEATURES)

    # Main classifier (weighted, default threshold)
    scores = score_cases(df)
    y_true = df["is_sweet_trap"].to_numpy()
    y_pred_main = classify(scores, DEFAULT_THRESHOLD)
    metrics_main = compute_metrics(y_true, y_pred_main)
    metrics_main["threshold"] = DEFAULT_THRESHOLD
    metrics_main["weights"] = {"w_F1": 2.0, "w_F2": 2.0, "w_F3": 1.0, "w_F4": 1.0}
    metrics_main["roc_auc"] = roc_auc_safe(y_true, scores)
    log.info("Main classifier (weighted, T=%.2f):\n%s",
             DEFAULT_THRESHOLD, json.dumps(metrics_main, indent=2))

    # Alternative rule: necessary-condition (F1≥0.5 AND F2≥0.5)
    y_pred_rule = classify_necessary_rule(df, tau=0.5)
    metrics_rule = compute_metrics(y_true, y_pred_rule)
    metrics_rule["rule"] = "F1>=0.5 AND F2>=0.5"
    log.info("Necessary-condition rule (F1>=0.5 AND F2>=0.5):\n%s",
             json.dumps(metrics_rule, indent=2))

    # Alternative rule: stricter necessary (F1 >= 1.0 AND F2 >= 1.0)
    y_pred_rule_strict = classify_necessary_rule(df, tau=1.0)
    metrics_rule_strict = compute_metrics(y_true, y_pred_rule_strict)
    metrics_rule_strict["rule"] = "F1>=1.0 AND F2>=1.0"
    log.info("Strict necessary-condition rule (F1=1 AND F2=1):\n%s",
             json.dumps(metrics_rule_strict, indent=2))

    # Threshold sweep
    sweep_df = threshold_sweep(df)
    log.info("Threshold sweep:\n%s", sweep_df.round(3).to_string(index=False))

    # LOO per-case behaviour at default threshold
    loo = loo_cv(df, DEFAULT_THRESHOLD)
    per_case_df = pd.DataFrame(loo["per_case"])
    log.info("Per-case at T=%.2f:\n%s", DEFAULT_THRESHOLD, per_case_df.to_string(index=False))

    # Confusion matrix as CSV (main weighted classifier at default threshold)
    cm = confusion_matrix(y_true, y_pred_main, labels=[0, 1])
    cm_df = pd.DataFrame(
        cm,
        index=["true_not_SweetTrap", "true_SweetTrap"],
        columns=["pred_not_SweetTrap", "pred_SweetTrap"],
    )
    cm_df.to_csv(OUT_CM)
    log.info("Confusion matrix (weighted, T=%.2f) saved -> %s", DEFAULT_THRESHOLD, OUT_CM)
    log.info("\n%s", cm_df.to_string())

    # Bundle everything to JSON
    output = {
        "seed": RNG_SEED,
        "n_cases": len(df),
        "n_positive": int((df.is_sweet_trap == 1).sum()),
        "n_negative": int((df.is_sweet_trap == 0).sum()),
        "weights": {"F1": 2.0, "F2": 2.0, "F3": 1.0, "F4": 1.0},
        "default_threshold": DEFAULT_THRESHOLD,
        "classifier_weighted_default": metrics_main,
        "rule_necessary_tau05": metrics_rule,
        "rule_necessary_tau10": metrics_rule_strict,
        "threshold_sweep": sweep_df.to_dict(orient="records"),
        "per_case_default": loo["per_case"],
    }
    with open(OUT_METRICS, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info("Saved metrics JSON -> %s", OUT_METRICS)

    # Summary ascii
    print("\n" + "=" * 70)
    print("SWEET TRAP DISCRIMINANT VALIDITY — SUMMARY")
    print("=" * 70)
    print(f"N = {len(df)}  |  positive controls = {(df.is_sweet_trap == 1).sum()}  |  negative controls = {(df.is_sweet_trap == 0).sum()}")
    print()
    print("Main classifier: weighted sum  S = 2·F1 + 2·F2 + 1·F3 + 1·F4  with threshold T > 4.0")
    print(f"  Accuracy       = {metrics_main['accuracy']:.3f}")
    print(f"  Sensitivity    = {metrics_main['sensitivity_recall']:.3f}  (recall on Sweet Traps)")
    print(f"  Specificity    = {metrics_main['specificity']:.3f}  (correct rejection of non-traps)")
    print(f"  Precision/PPV  = {metrics_main['precision_PPV']:.3f}")
    print(f"  Cohen's kappa  = {metrics_main['cohen_kappa']:.3f}")
    print(f"  Matthews corr  = {metrics_main['MCC']:.3f}")
    print(f"  F1 score       = {metrics_main['F1_score']:.3f}")
    print(f"  ROC AUC        = {metrics_main['roc_auc']:.3f}")
    print()
    print("Necessary-condition rule  (F1>=0.5 AND F2>=0.5):")
    print(f"  Accuracy       = {metrics_rule['accuracy']:.3f}")
    print(f"  Sensitivity    = {metrics_rule['sensitivity_recall']:.3f}")
    print(f"  Specificity    = {metrics_rule['specificity']:.3f}")
    print(f"  Cohen's kappa  = {metrics_rule['cohen_kappa']:.3f}")
    print()

    # Flag if accuracy < 80%
    if metrics_main["accuracy"] < 0.80:
        print("[DIAGNOSTIC] accuracy < 80% — construct needs refinement.")
    else:
        print("[OK] accuracy >= 80% — construct has adequate discriminant validity.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
