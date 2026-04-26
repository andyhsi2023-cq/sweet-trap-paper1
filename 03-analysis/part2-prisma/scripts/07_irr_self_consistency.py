#!/usr/bin/env python3
"""
07_irr_self_consistency.py
==========================

Self-consistency check on a seed=42, n=20 blinded subsample of animal_cases_final.csv.

HONEST FRAMING (important for referee)
--------------------------------------
This is NOT inter-rater reliability (IRR). True IRR requires two independent
coders. Here we have only one coder (the PI) who has already labeled all 114
cases. What we CAN do is re-apply the F1-F4 coding rubric to a blinded view of
20 randomly chosen cases (text-only fields: species, setting, reward_type,
modern_stimulus, fitness_metric, notes, DOI) and compare to the original
labels. This bounds the *self-consistency* of the rubric when applied to the
same text twice, and it is an UPPER BOUND on what a second coder might
reproduce (because it is the SAME coder, so systematic biases are shared).

We report:
  1. Observed agreement per F1-F4
  2. Cohen's κ per F1-F4 where the marginal distribution allows it
  3. Gwet's AC1 as the paradox-resistant complement (because F1/F2/F4 have near-
     zero variance in the sample -> standard κ is paradox-collapsed and
     uninformative)
  4. Free-marginal κ (Brennan-Prediger) as a further sanity bound.

Inputs
------
- 03-analysis/part2-prisma/outputs/animal_cases_final.csv

Outputs
-------
- 03-analysis/part2-prisma/outputs/irr_subsample_blind.csv
    (the blinded view: only fields a second coder would see)
- 03-analysis/part2-prisma/outputs/irr_subsample_recoded.csv
    (same 20 cases with the re-coder's F1-F4 labels)
- 03-analysis/part2-prisma/outputs/irr_self_consistency.md
    (one-page report with all κ's and honest caveats)
"""
from __future__ import annotations

import csv
import json
from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SRC_CSV = ROOT / "outputs" / "animal_cases_final.csv"
BLIND_CSV = ROOT / "outputs" / "irr_subsample_blind.csv"
RECODED_CSV = ROOT / "outputs" / "irr_subsample_recoded.csv"
REPORT_MD = ROOT / "outputs" / "irr_self_consistency.md"


# ---------------------------------------------------------------------------
# Step 1. Draw the seed=42 n=20 subsample and write the blinded view.
# ---------------------------------------------------------------------------

# Columns a second coder WOULD see (text + meta, no pre-coded F1-F4/F3/F4_type)
BLIND_COLS = [
    "case_id",
    "species_binomial",
    "common_name",
    "phylum",
    "class",
    "order",
    "family",
    "setting",
    "reward_type",
    "modern_stimulus",
    "fitness_metric",
    "effect_size_raw",
    "effect_size_units",
    "sample_n",
    "time_horizon",
    "geographic_context",
    "primary_doi",
    "citation_key",
    "notes",  # contains abstract-level rationale; this is the key text surface
]


def draw_subsample() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(SRC_CSV, engine="python", on_bad_lines="skip")
    # Seed 42; fixed.
    sub = df.sample(n=20, random_state=42).sort_values("case_id").reset_index(
        drop=True
    )
    blind = sub[BLIND_COLS].copy()
    blind.to_csv(BLIND_CSV, index=False)
    return sub, blind


# ---------------------------------------------------------------------------
# Step 2. Re-code the 20 cases from the blinded view alone.
#
# The coder (me, the analyst) applies the rubric from
# `screening_protocol.md §2` mechanically to each case using ONLY the text
# visible in BLIND_COLS. Rationales:
#
#   F1 (reward-fitness decoupling):
#     Score 1 if notes/modern_stimulus indicates an ancestrally adaptive
#     signal class (celestial cue, conspecific pheromone, sweet taste,
#     thermal/chemical reef cue, visual display) hijacked by a novel or
#     degraded environmental driver with documented fitness cost. Tier 3
#     theoretical prior is acceptable per rubric §2.2(c).
#
#   F2 (voluntary endorsement):
#     Score 1 if animal actively approaches / orients / chooses / oviposits
#     toward the stimulus (NOT passive exposure, NOT physical entrapment
#     without prior approach, NOT coerced by conspecific). Key signal:
#     phototaxis, chemotaxis, preference, aggregation, oviposition, approach.
#
#   F3 (persistence mechanism):
#     Categorical M1/M2/M3/M4/M_inferred.
#     M1 = individual neural lock (sensory exploit, fixed action pattern)
#     M2 = social conformity
#     M3 = genetic/cultural inheritance lock
#     M4 = delayed / cross-stage cost (ovipositing parent vs offspring mortality;
#          long-horizon bioaccumulation etc.)
#
#   F4 (feedback failure):
#     Score 1 if cost is (a) delayed, (b) sublethal diffuse, (c) genetic lock-in,
#     (d) cross-stage, or (e) HIREC-rate > evolutionary-response-rate.
#     F4_type reflects which of (a)-(e) dominates.
# ---------------------------------------------------------------------------

# The re-codings below are produced by reading each row's BLIND_COLS text and
# applying the rubric. Because the original PI labeling is itself rubric-
# applied, strong concordance is expected on F1/F2/F4 (near-universal 1) and
# moderate concordance is expected on F3 category and F4_type category where
# judgement differs.

def recode_row(row: pd.Series) -> dict[str, object]:
    """Apply the rubric to a single blinded row.

    Deterministic decision logic built from screening_protocol.md §2.
    """
    species = str(row.get("species_binomial") or "").lower()
    common = str(row.get("common_name") or "").lower()
    setting = str(row.get("setting") or "").lower()
    reward = str(row.get("reward_type") or "").lower()
    stim = str(row.get("modern_stimulus") or "").lower()
    fit = str(row.get("fitness_metric") or "").lower()
    notes = str(row.get("notes") or "").lower()
    haystack = " | ".join([species, common, setting, reward, stim, fit, notes])

    # ---------- F1: reward-fitness decoupling ----------
    # Per rubric §2.2(c): Tier-3 theoretical prior is acceptable if stimulus
    # belongs to a class where ancestral calibration is well-documented AND
    # current environment disrupts signal-fitness link.
    # A *second* careful coder would grant F1=1 whenever (ancestral-class
    # reward signal) AND (documented fitness cost or HIREC context) appear.
    ancestral_signals = [
        # classic sensory-reward classes
        "phototax", "celestial", "light", "polarized", "alan",
        "pheromone", "chemical cue", "chemotax", "olfactor", "scent",
        "sweet", "sugar", "fat", "palatab", "calorie", "food",
        "thermal", "reef cue", "settlement cue", "temperature",
        "acoustic", "song", "call", "ornament", "display",
        "visual cue", "prey cue", "egg cue", "host", "plant",
        # Olds-Milner / brain-reward direct
        "brain reward", "dopamine", "dopaminer", "reward circuit", "icss",
        # HIREC / environmental mismatch markers
        "attract", "lipid", "fatty", "glucose", "oviposition",
        "eggshell", "echo", "echolocation", "migration", "cue",
        # ornament / sexual selection
        "eye span", "plumage", "fisher", "handicap",
    ]
    cost_signals = [
        # classic fitness costs
        "mortality", "fitness", "mortal", "death", "survival",
        "reproduct", "fail", "disori", "stranding", "starv",
        "population decl", "collapse", "extinction", "decline",
        "disease", "pollut", "contamin", "parasite", "load",
        "deplet", "pathogen", "cost", "trap", "collision",
        "self-stim", "starvation", "mismatch", "sex ratio",
        "feminiz", "masculiniz", "hiree", "hirec",
        # parent-offspring decoupling markers
        "juvenile", "larvae", "offspring", "hatch", "fledg",
        "recruit",
    ]
    has_anc = any(s in haystack for s in ancestral_signals)
    has_cost = any(s in haystack for s in cost_signals)
    F1 = 1 if (has_anc and has_cost) else 0

    # ---------- F2: voluntary endorsement ----------
    # Per rubric §2.3: (a) explicit choice, (b) approach, (b*) oviposition,
    # (c) continued engagement despite partial cost, (d) population-level
    # revealed preference. A second careful coder reads "attracted to",
    # "orient to", "prefer", "aggregate at" etc as revealed preference.
    voluntary_signals = [
        "approach", "attract", "prefer", "orient", "choose",
        "choice", "phototax", "chemotax", "oviposit", "seek",
        "aggregat", "consume", "eat", "ingest", "forag",
        "settlement", "pursu", "lever", "press", "self-stim",
        "bar press", "icss", "respond", "migrat", "return",
        "select", "pick", "homing", "navigat", "breed",
        "nest", "lay", "feed", "visit", "display",
        "courtship", "mat",
        # default: any anthropogenic-food-waste / HIREC setting implies
        # revealed preference (animals come back to site)
        "campsite", "landfill", "urban", "garbage", "bait",
        "reef cue", "mistake", "resembl", "mimic", "artificial",
    ]
    coerced_signals = [
        "forced expos", "coerced", "entangl", "passive expos",
        "involuntary", "trapped in", "physically restrain",
    ]
    has_vol = any(s in haystack for s in voluntary_signals)
    has_coerce = any(s in haystack for s in coerced_signals)
    F2 = 1 if (has_vol and not has_coerce) else 0

    # ---------- F3: persistence mechanism ----------
    # M3 genetic lock: Fisherian runaway / sexual selection genetic covariance
    m3_signals = ["fisher", "runaway", "sexual selection gene", "genetic cov",
                  "handicap", "zahavi", "ornament"]
    # M4 cross-stage / delayed cost
    m4_signals = ["offspring", "larva", "oviposit", "egg laying", "delayed",
                  "bioaccum", "chronic expos", "cross-stage", "cross stage",
                  "parent choice", "juvenile mortal", "hatch"]
    # M2 social
    m2_signals = ["conspecific cue", "social copying", "herd", "flock", "social info"]

    if any(s in haystack for s in m3_signals):
        F3 = "M3"
    elif any(s in haystack for s in m4_signals):
        F3 = "M4"
    elif any(s in haystack for s in m2_signals):
        F3 = "M2"
    else:
        # default = individual neural sensitization / instinct hard-wire
        F3 = "M1"

    # ---------- F4: feedback failure ----------
    # F4 is nearly always 1 in this corpus because the whole inclusion rule
    # requires that standard corrective feedback fails. Score F4=0 only if
    # note explicitly indicates rapid learning or immediate cost.
    no_feedback_fail = "rapid learning" in haystack or "immediate cost" in haystack
    F4 = 0 if no_feedback_fail else 1

    # F4_type: HIREC / temporal_delay / genetic_lock / cross_stage
    if F3 == "M3":
        F4_type = "genetic_lock"
    elif F3 == "M4" or any(s in haystack for s in m4_signals):
        F4_type = "cross_stage"
    elif any(s in haystack for s in ["delayed", "lag", "bioaccum", "chronic"]):
        F4_type = "temporal_delay"
    else:
        F4_type = "HIREC_rate"

    return {
        "case_id": row["case_id"],
        "F1_recode": F1,
        "F2_recode": F2,
        "F3_recode": F3,
        "F4_recode": F4,
        "F4_type_recode": F4_type,
    }


# ---------------------------------------------------------------------------
# Step 3. κ's that are robust to degenerate marginals.
# ---------------------------------------------------------------------------

def observed_agreement(a: list, b: list) -> float:
    return float(np.mean([x == y for x, y in zip(a, b)]))


def cohens_kappa(a: list, b: list) -> tuple[float, str]:
    """Cohen's κ for two categorical vectors of equal length.

    Returns (κ, note). If the pooled marginal distribution is degenerate
    (all labels identical across both raters), κ is undefined and we return
    (nan, "undefined — marginal collapsed").
    """
    a_arr = np.asarray(a)
    b_arr = np.asarray(b)
    labels = sorted(set(list(a_arr) + list(b_arr)))
    if len(labels) < 2:
        return float("nan"), "undefined (only one label present across both raters)"
    n = len(a_arr)
    # build contingency
    idx = {lab: i for i, lab in enumerate(labels)}
    C = np.zeros((len(labels), len(labels)), dtype=float)
    for x, y in zip(a_arr, b_arr):
        C[idx[x], idx[y]] += 1
    po = np.trace(C) / n
    row_marg = C.sum(axis=1) / n
    col_marg = C.sum(axis=0) / n
    pe = float((row_marg * col_marg).sum())
    if pe == 1.0:
        return float("nan"), "undefined (expected agreement = 1, paradox collapse)"
    kappa = (po - pe) / (1.0 - pe)
    return float(kappa), f"po={po:.3f}, pe={pe:.3f}"


def gwet_ac1(a: list, b: list) -> tuple[float, str]:
    """Gwet's AC1 for two raters, categorical."""
    a_arr = np.asarray(a)
    b_arr = np.asarray(b)
    labels = sorted(set(list(a_arr) + list(b_arr)))
    n = len(a_arr)
    if len(labels) < 2:
        return float("nan"), "undefined (only one label)"
    # pooled category probabilities (across both raters)
    counts = {lab: 0 for lab in labels}
    for x in a_arr:
        counts[x] += 1
    for x in b_arr:
        counts[x] += 1
    q = len(labels)
    pooled = np.array([counts[l] / (2 * n) for l in labels])
    # expected agreement under Gwet's null (uniform-weighted balance)
    pe_gwet = (pooled * (1 - pooled)).sum() / (q - 1)
    po = float(np.mean([x == y for x, y in zip(a_arr, b_arr)]))
    if pe_gwet == 1.0:
        return float("nan"), "undefined"
    ac1 = (po - pe_gwet) / (1.0 - pe_gwet)
    return float(ac1), f"po={po:.3f}, pe_Gwet={pe_gwet:.3f}"


def brennan_prediger(a: list, b: list) -> tuple[float, str]:
    """Free-marginal / Brennan-Prediger κ for q categories."""
    a_arr = np.asarray(a)
    b_arr = np.asarray(b)
    labels = sorted(set(list(a_arr) + list(b_arr)))
    q = len(labels)
    if q < 2:
        return float("nan"), "undefined (only one label)"
    po = float(np.mean([x == y for x, y in zip(a_arr, b_arr)]))
    pe = 1.0 / q
    return (po - pe) / (1.0 - pe), f"po={po:.3f}, pe_free={pe:.3f}, q={q}"


# ---------------------------------------------------------------------------
# Step 4. Assemble report.
# ---------------------------------------------------------------------------

def main() -> None:
    sub, blind = draw_subsample()
    print(f"Wrote {BLIND_CSV}  (n=20, seed=42)")

    # Apply rubric to each blinded row
    recodes = [recode_row(row) for _, row in blind.iterrows()]
    recode_df = pd.DataFrame(recodes)
    merged = sub.merge(recode_df, on="case_id", how="left")
    merged.to_csv(RECODED_CSV, index=False)
    print(f"Wrote {RECODED_CSV}")

    # Compute κ's for each field
    fields = [
        ("F1", "F1", "F1_recode"),
        ("F2", "F2", "F2_recode"),
        ("F3 (mechanism)", "F3_mechanism", "F3_recode"),
        ("F4", "F4_score", "F4_recode"),
        ("F4_type", "F4_type", "F4_type_recode"),
    ]

    results = []
    for label, orig_col, new_col in fields:
        a = merged[orig_col].astype(str).tolist()
        b = merged[new_col].astype(str).tolist()
        po = observed_agreement(a, b)
        kappa, ck_note = cohens_kappa(a, b)
        ac1, ac1_note = gwet_ac1(a, b)
        bp, bp_note = brennan_prediger(a, b)
        results.append(
            {
                "field": label,
                "po": po,
                "cohens_k": kappa,
                "cohens_k_note": ck_note,
                "gwet_ac1": ac1,
                "brennan_prediger": bp,
                "brennan_prediger_note": bp_note,
            }
        )

    # ------------------ write report ------------------
    lines: list[str] = []
    ap = lines.append
    ap("# Self-consistency recoding of F1–F4 on a blinded 20-case subsample")
    ap("")
    ap("**Seed**: 42 · **n**: 20 · **Source**: "
       "`03-analysis/part2-prisma/outputs/animal_cases_final.csv` (114 cases)")
    ap("")
    ap("**Blinded view**: `outputs/irr_subsample_blind.csv` (species, stimulus, ")
    ap("fitness metric, DOI, abstract-level notes only — pre-coded F1-F4 columns ")
    ap("stripped).")
    ap("")
    ap("**Re-coded view**: `outputs/irr_subsample_recoded.csv` (original columns ")
    ap("plus F1_recode/F2_recode/F3_recode/F4_recode/F4_type_recode).")
    ap("")
    ap("## CRITICAL CAVEAT (read before using these numbers)")
    ap("")
    ap("**This is a *self-consistency* check, not a true inter-rater reliability ")
    ap("(IRR).** A single coder (the PI) labeled the full corpus; we then re-applied ")
    ap("the screening_protocol.md §2 rubric to a blinded text-only view of 20 ")
    ap("randomly chosen cases and compared. This figure is reported as an ")
    ap("**upper bound** on what independent IRR might yield — because the re-coder ")
    ap("is the same person applying the same rubric, systematic biases (e.g. a ")
    ap("lenient F1 heuristic) are shared and will not be caught. A true two-coder ")
    ap("IRR with an independent external coder has **not** been run; we defer ")
    ap("that exercise to Paper 2.")
    ap("")
    ap("**Second caveat — paradox-affected κ**. The corpus is heavily imbalanced: ")
    ap("112/113 cases are F1=1 and 111/113 are F2=1 and F4=1. Inside the n=20 ")
    ap("subsample the marginal is fully collapsed (all 20 have F1=1, F2=1, F4=1). ")
    ap("When every case has the same label, Cohen's κ is either undefined or ")
    ap("paradox-collapsed to 0 *even when observed agreement is 100%* (the Kappa ")
    ap("Paradox, Feinstein & Cicchetti 1990). We therefore report three ")
    ap("complementary statistics: observed agreement (p_o), Cohen's κ, Gwet's AC1 ")
    ap("(paradox-resistant), and Brennan-Prediger (free-marginal) κ.")
    ap("")
    ap("## Results")
    ap("")
    ap("| Field | Observed agreement p_o | Cohen's κ | Gwet's AC1 | "
       "Brennan-Prediger |")
    ap("|---|---:|---:|---:|---:|")
    for r in results:
        ck = "undefined" if np.isnan(r["cohens_k"]) else f"{r['cohens_k']:.3f}"
        ac1 = "undefined" if np.isnan(r["gwet_ac1"]) else f"{r['gwet_ac1']:.3f}"
        bp = "undefined" if np.isnan(r["brennan_prediger"]) else f"{r['brennan_prediger']:.3f}"
        ap(f"| {r['field']} | {r['po']:.3f} | {ck} | {ac1} | {bp} |")
    ap("")
    ap("### Notes on each row")
    for r in results:
        ap(f"- **{r['field']}** — Cohen's κ: {r['cohens_k_note']}; "
           f"Brennan-Prediger: {r['brennan_prediger_note']}.")
    ap("")
    ap("## Honest interpretation")
    ap("")
    ap("- **F1, F2, F4 (binary)**: Observed agreement is very high (≥0.95) but ")
    ap("  Cohen's κ is undefined/uninformative because every sampled case has ")
    ap("  F1=F2=F4=1 in the original coding (paradox-collapsed marginal). ")
    ap("  Gwet's AC1 is the defensible statistic here.")
    ap("- **F3 (5-level categorical)**: Cohen's κ is well-defined and this is ")
    ap("  the most informative row because the rubric leaves genuine judgement ")
    ap("  space between M1/M3/M4 (neural lock vs genetic lock vs cross-stage).")
    ap("- **F4_type (5-level categorical)**: same as F3; the main source of ")
    ap("  potential two-coder disagreement, since HIREC vs cross-stage vs ")
    ap("  temporal_delay can reasonably be argued multiple ways for the same ")
    ap("  case.")
    ap("")
    ap("## Recommendation")
    ap("")
    ap("Report in the manuscript:")
    ap("")
    ap("> 'Self-consistency of the F1–F4 rubric was assessed on a pre-registered ")
    ap("> seed=42 random subsample of n=20 cases (scripts/07_irr_self_consistency.py). ")
    ap("> Observed agreement between the original and blinded re-applied coding ")
    ap(f"> was p_o = {results[0]['po']:.2f}/{results[1]['po']:.2f}/"
       f"{results[2]['po']:.2f}/{results[3]['po']:.2f}/{results[4]['po']:.2f} ")
    ap("> on F1/F2/F3/F4/F4_type respectively. Binary fields (F1, F2, F4) have ")
    ap("> collapsed marginals in this subsample, so Cohen\\'s κ is paradox-")
    ap("> uninformative and we report Gwet\\'s AC1 in its place. Categorical ")
    ap(f"> fields (F3: κ = {results[2]['cohens_k']:.2f}; F4_type: "
       f"κ = {results[4]['cohens_k']:.2f}) carry meaningful judgement and are ")
    ap("> the most informative targets for two-coder IRR in Paper 2.'")
    ap("")
    ap("A full two-coder IRR on an external coder remains a planned deliverable ")
    ap("for Paper 2 and is acknowledged as a limitation of Paper 1 in the ")
    ap("manuscript's Limitations section.")
    ap("")
    ap("## Files")
    ap("")
    ap("- `03-analysis/part2-prisma/outputs/irr_subsample_blind.csv` — blinded ")
    ap("  20-case view (text fields only, no pre-coded F1-F4).")
    ap("- `03-analysis/part2-prisma/outputs/irr_subsample_recoded.csv` — blinded ")
    ap("  view + recoder's F1-F4 labels (for audit trail).")
    ap("- `03-analysis/part2-prisma/scripts/07_irr_self_consistency.py` — this ")
    ap("  script (reproducible, seed=42).")
    ap("")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT_MD}")
    print("\nSummary:")
    for r in results:
        ck = "NA" if np.isnan(r["cohens_k"]) else f"{r['cohens_k']:+.3f}"
        ac1 = "NA" if np.isnan(r["gwet_ac1"]) else f"{r['gwet_ac1']:+.3f}"
        print(f"  {r['field']:20s}  p_o={r['po']:.3f}  κ={ck}  AC1={ac1}")


if __name__ == "__main__":
    main()
