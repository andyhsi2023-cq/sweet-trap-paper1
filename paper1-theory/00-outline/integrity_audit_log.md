# Paper 1 Empirical-Integrity Audit Log

**Date**: 2026-04-18
**Auditor**: data-analyst agent (on behalf of peer-reviewer F3 fatal-flaw finding in `rigor_audit.md`)
**Scope**: P1-P5 empirical-status paragraphs in `03-predictions/predictions.md` (v1.0) and `05-manuscript/paper1_theory_draft.md` §4 and `05-manuscript/abstract.md`
**Source of truth**: Paper 2 v2.4 data files and manuscript as listed in §Verification files

**Verdict (summary)**: 4 of 5 predictions in Paper 1 v1.0 contained one or more empirical claims that do not match the Paper 2 v2.4 source data. Corrections are applied to predictions.md → v1.1; manuscript draft §4 and abstract updated in parallel. Axioms, theorems, and lemmas are **unchanged**.

---

## §1 Verification files

### Paper 1 v1.0 files audited
1. `paper1-theory/03-predictions/predictions.md` (v1.0)
2. `paper1-theory/05-manuscript/paper1_theory_draft.md` §4
3. `paper1-theory/05-manuscript/abstract.md`
4. `paper1-theory/03-predictions/minimal_experimental_paradigm.md` (no empirical claims; consistent)

### Paper 2 v2.4 source files consulted
1. `/02-data/processed/intervention_asymmetry_table.csv` — 12 rows (6 domains × 2 arms) for P1
2. `/02-data/processed/mr_results_all_chains_v2.csv` — 19 MR chains for P2
3. `/03-analysis/models/cultural_gc_coefficients.csv` + `cultural_gc_results.json` — 59-country G^c for P3
4. `/02-data/processed/cross_level_effects_table.csv` — 44-row integrated A+B+D table for P5
5. `/00-design/pde/cross_level_meta_findings.md` — cross-level meta-regression documentation
6. `/00-design/pde/spec_curve_findings.md` — 5-focal spec-curve findings
7. `/05-manuscript/main_v2.4_draft.md` — Paper 2 v2.4 §8 intervention-asymmetry, §6 cross-level meta, §M9/M10 methods
8. `/05-manuscript/figure_8_v2.4_spec.md` — Figure 8 data specification for Paper 2 §8
9. `/00-design/pde/layer_A_animal_meta_v2.md` — 20-animal cases + mechanism classification

---

## §2 Prediction-by-prediction audit

### P1 — Intervention Asymmetry Law

| # | Paper 1 v1.0 claim | Paper 2 v2.4 actual | Verdict |
|---|---|---|---|
| P1.a | "meta-evaluation across **7 domains**" | `intervention_asymmetry_table.csv` has **6 domains**: C8, C11, C12, C13, D_alcohol, C_pig-butchering. Main_v2.4_draft.md §8.2 and §8.4 explicitly use "six focal Sweet Trap domains". | **Incorrect**: 7 → 6 |
| P1.b | "ratio ∈ **[1.4, 3.1]**, median ≈ **2.0**" | Paper 2 v2.4 §8.2 and §M10 do **not** compute a scalar median ratio. Unit-matched ratios where computable: C8 = 74× (pp/pp), C12 = 7× (d/d). Other 4 domains have heterogeneous units (kcal vs %, pp vs %, d vs elasticity, d vs %) where a simple ratio is uninterpretable. Paper 2's Figure 8 Panel b reports within-domain ratios on a log scale with "most exceed 3" as the verbal summary. | **Incorrect**: "[1.4, 3.1] median 2.0" cannot be sourced from Paper 2 data; appears to be v1.0 drafting error |
| P1.c | "sugar-tax choice-architecture **2.4×** nutrition-label" | Paper 2 C11 row: info = −8 kcal/meal (CI spans 0); signal = −10% SSB consumption. Units mismatched; 2.4× ratio not directly derivable from Paper 2 numbers. | **Source unclear**: figure cited without unit-match; likely secondary-lit anchor, not Paper 2 |
| P1.d | "deactivation-friction **3.1×** screen-time awareness" | Paper 2 C12 row: info d = 0.05; signal d = 0.35. Ratio = 7.0×, not 3.1×. | **Incorrect**: 3.1 → 7.0 per Paper 2's unit-matched C12 |
| P1.e | "machine-regulation **2.8×** responsible-gambling messaging" | **No gambling row exists in `intervention_asymmetry_table.csv`**. Paper 2's gambling evidence is narrative-only (Dow-Schüll citation in discussion). | **Not in Paper 2 data** |
| P1.f | Domain list included "C14 gambling" | Paper 2 v2.4 does not include C14 as a focal domain in §8. Gambling appears only in §5 narrative (alcohol-gambling comparison). | **Domain list incorrect**: includes non-focal C14; Paper 2 focal list is C8/C11/C12/C13/D_alcohol/C_pig-butchering |

**Corrected status**: qualitative 已支持 (signal-redesign > information in all 6 domains; 4/6 CIs non-overlapping); quantitative ≥ 1.5 floor **awaiting harmonised-scale re-extraction**. Of the 2 unit-matched ratios available (C8 = 74×, C12 = 7×), both exceed T2's 1.5 floor by wide margins.

---

### P2 — Persistence–Severity Monotonicity

| # | Paper 1 v1.0 claim | Paper 2 v2.4 actual | Verdict |
|---|---|---|---|
| P2.a | "Spearman **ρ = +0.73**, p = 0.002 across **19 Layer-D chains**" | **No such statistic exists anywhere in Paper 2 v2.4.** Exhaustive search of /02-data/processed/, /00-design/pde/, and /05-manuscript/ returns no "persistence rank" column, no Lyapunov decay rate computation, no ρ = 0.73 result. The 19-chain MR results table (`mr_results_all_chains_v2.csv`) contains IVW β, SE, p, Q, I², Egger intercept, and Steiger direction — nothing that operationalises persistence as v1.0 claims. | **Fabricated / not traceable to Paper 2 data** |
| P2.b | "C12 Short-video (Δ_ST ≈ +0.68): 70% return to baseline within 4 weeks" | Not in Paper 2 data. Allcott et al. 2020 *AER* is cited secondary literature, not a Paper 2 measurement. | **Secondary-lit illustrative anchor**, not Paper 2 primary |
| P2.c | "C11 Diet (Δ_ST ≈ +0.45): 60-80% weight regain within 12 months" | Mozaffarian 2016 *Circulation* citation; not a Paper 2 computation. | **Secondary-lit illustrative anchor**, not Paper 2 primary |

**Corrected status**: **awaiting empirical test**. P2 is a theorem-derived prediction; Paper 2 v2.4 does not currently contain the persistence-rank cross-case table needed to test it. The direction implied by illustrative anchors is consistent with P2, but no formal statistic can be cited.

---

### P3 — Cultural Amplification

| # | Paper 1 v1.0 claim | Paper 2 v2.4 actual | Verdict |
|---|---|---|---|
| P3.a | "ρ(Δ_ST, *G*^c) = **+0.98**, **N = 34 countries**" for luxury | `cultural_gc_results.json` `spearman_rho_raw_vs_gc_weighted = 0.9814`. But this is a **reliability check** between the raw and weighted G^c indices (construct-level, n = 201 country-domain rows for sensitivity; n_countries_gc = 59). Paper 2 does **not** compute a country-level luxury-domain Δ_ST × G^c correlation. The ISSP 25-country panel reports ρ = 0.94 between raw and weighted G^c, not between G^c and Δ_ST. | **Misattributed statistic**: ρ=0.98 refers to a different quantity than Paper 1 claims. N=34 is not present in Paper 2 data (actual N = 59 for G^c coverage; 25 for ISSP panel). |
| P3.b | "**R² = 0.92** after PDI + LTOWVS adjustment" | Paper 2 Layer C primary regression: joint-predictor **R² = 0.255** (main_v2.3_draft.md:121; confirmed main_v2.4_draft.md §3). G^c additional explanatory power Δr² ≈ 0.0009 (`cultural_gc_results.json`, `delta_r2` field). | **R² = 0.92 does not exist in Paper 2**; fabricated |
| P3.c | "Education investment (C7): ρ(Δ_ST, LTOWVS) = **+0.84**" | C7 education is not a Paper 2 focal domain; no ρ computed. | **Not in Paper 2 data** |
| P3.d | "Bride-price inflation (C4): ρ(Δ_ST, PDI + kin-structure index) = **+0.79**" | C4 bride price is excluded from Paper 2 main-text (domain_selection_matrix.md: "CGSS measures receipt not payment; Δ_ST wrong-signed"; final score 4.66, moved to SI "if resources permit"). No cross-country bride-price regression exists in Paper 2. | **Not in Paper 2 data** |

**Corrected status**: **partially supported**. Paper 2 v2.4's ISSP 25-country panel shows joint-predictor R² = 0.255 for the aspirational-wealth domain (Δz + log τ_env), which exceeds P3's ≥ 0.15 falsification floor but does not reach the ≥ 0.40 prediction point. Paper 2 also notes Layer C ISSP cross-domain replication is weak (6/11 directional matches; `main_v2.4_draft.md:246` item 2). The luxury-specific, education-specific, and bride-price-specific ρ values in v1.0 are withdrawn as not traceable.

---

### P4 — Engineered Escalation

| # | Paper 1 v1.0 claim | Paper 2 v2.4 actual | Verdict |
|---|---|---|---|
| P4.a | "TikTok grew average daily minutes **3.2× faster** than YouTube (2018-2022)" | Not in Paper 2 data. No TikTok vs YouTube comparison table in Paper 2. | **Secondary-lit citation without clear primary source**; retain as illustrative only |
| P4.b | "variable-ratio slots **4× loss-chasing persistence** vs fixed-ratio roulette (Dow-Schüll 2012)" | Dow-Schüll 2012 *Addiction by Design* is an ethnography. It does not report a "4× loss-chasing persistence ratio" as a discrete statistic; Paper 2 cites Dow-Schüll only for architectural-argument purposes, not for this specific number. | **Misattributed to Dow-Schüll**; specific "4×" figure requires different primary source (candidate: Dixon et al. 2014 *J Gambling Studies*) |
| P4.c | "Food-delivery **1.8×** (Wang et al. 2023 *Lancet Planet Health*)" | Not identifiable in Paper 2's corpus of Wang et al. citations. Wang et al. 2023 *Lancet Planet Health* is cited in Paper 1 intro for added-sugar statistic, not food-delivery comparison. | **Citation mismatch**; primary source required |

**Corrected status**: **partially supported qualitatively, quantitative awaiting test**. Paper 2 Layer A shows Olds-Milner EST case (A5 Δ_ST = +0.97) exceeds all MST sensory-exploitation cases (A1-A3, A7 etc. with Δ_ST ≤ 0.82). Quantitative "50% higher" and "< 1/2 timescale" require a targeted matched-platform study.

---

### P5 — Cross-Species Mechanism Rank

| # | Paper 1 v1.0 claim | Paper 2 v2.4 actual | Verdict |
|---|---|---|---|
| P5.a | "Spearman ρ(A, D) = **+1.00** on **n = 6 overlapping mechanism cells**" | `cross_level_meta_findings.md` §3.2, §4: "Only **2 mechanisms in common** (olds, sensory); same direction. *p is undefined when only 2 ranks are compared (ρ can only be ±1).*" main_v2.4_draft.md:246 item 7 (Paper 2 Limitation list): "**Spearman ρ(A, D) = +1.00 on n = 2 cells is a geometric identity, not inferential.**" | **Critical n-miscount**: n=6 claimed; actual n=2. With n=2, ρ is not a statistic but a geometric identity. |
| P5.b | "cross-layer β = **+1.58**, p = **0.019**" | cross_level_meta_findings.md §3.4 row "A+D only": β = +1.58, p = 0.019. **This number is correct.** | **Accurate**: verified against source |
| P5.c | "animal cases N = 20; human MR chains N = 19" | layer_A_animal_meta_v2.md: 20 cases (19 used in gradient model, 1 excluded as singleton). mr_results_all_chains_v2.csv: 19 chains (15 core + 4 protective-inverse). | **Accurate** |

**Corrected status**: **strongly supported** via the pre-registered A+D joint test (β = +1.58, p = 0.019). The ρ = +1.00 must be reported as "rank-consistent on the 2 overlapping mechanism categories (geometric identity at n = 2)", **not** as "ρ = +1.00 on n = 6 cells".

---

## §3 Severity ranking

Most severe to least severe:

1. **P2 (ρ = +0.73, p = 0.002 across 19 chains)**: **Fabricated statistic**. No analogue exists in Paper 2 data. Most severe because it presents a specific statistic with p-value that never was computed. **Status**: withdrawn; P2 reclassified as "awaiting empirical test".

2. **P5 (n = 6 vs n = 2)**: **Critical n-miscount**. ρ = +1.00 on n=6 would be a real statistic (p ≈ 0.003); on n=2 it is a geometric identity with no inferential content. This **inverts the statistical meaning** of the claim. Paper 2 itself flags this as Limitation item 7. **Status**: corrected to "n = 2 overlapping mechanism means; geometric identity; inferential support comes from the A+D joint β = +1.58, p = 0.019".

3. **P3 (luxury R² = 0.92, 34 countries, ρ = 0.98)**: **Fabricated headline numbers**. Paper 2's actual R² = 0.255 across 25 countries for aspirational-wealth; luxury-specific regression not computed. **Status**: withdrawn; P3 reclassified as "partially supported (≥ 0.15 floor exceeded; ≥ 0.40 point not met)".

4. **P1 (7 domains, median 2.0, range [1.4, 3.1])**: **Wrong domain count and wrong ratio statistic**. Paper 2 has 6 domains not 7; does not compute a scalar median ratio; Paper 2's actual unit-matched ratios (C8 = 74×, C12 = 7×) clear T2's 1.5 floor by much larger margins than v1.0 reported. **Status**: corrected to qualitative-supported / quantitative-awaiting-harmonised-ratio.

5. **P4 (3.2×, 4×, 1.8×)**: **Secondary-lit numbers presented as primary**. Dow-Schüll 4× not in Dow-Schüll 2012; other two figures not traceable to Paper 2. **Status**: reclassified as illustrative only; quantitative claims require matched-platform study.

---

## §4 Files to edit (before/after line-level)

### 4.1 `paper1-theory/03-predictions/predictions.md` — complete rewrite (v1.0 → v1.1)

All five §P?.4 empirical-status paragraphs rewritten; new summary table at bottom; integrity-audit preamble added at top. **Completed 2026-04-18.**

### 4.2 `paper1-theory/05-manuscript/paper1_theory_draft.md`

Specific line edits:

| Line | v1.0 text (truncated) | v1.1 replacement |
|---|---|---|
| 22 (Abstract) | "five falsifiable predictions, **four** of which are already supported by existing empirical data" | "five falsifiable predictions, **of which one is strongly supported by the pre-registered Paper 2 v2.4 A+D joint meta-regression, one is partially supported, one is qualitatively supported pending harmonised-scale quantitative test, and two await empirical test with motivating anchors from existing literature**" |
| 284 (§4 P1) | "Paper 2 v2.4 meta-evaluation across **7 domains** yields ratio ∈ [1.4, 3.1], median ≈ 2.0. Concrete anchors: sugar-tax … 2.4× …; deactivation-friction 3.1× …; machine-regulation 2.8× responsible-gambling messaging." | "Paper 2 v2.4 §8 compilation across **6 domains** (C8/C11/C12/C13/D_alcohol/C_pig-butchering) finds signal-redesign effect exceeds information effect in 6/6 domains; CIs non-overlap in 4/6. On the 2 domains where both arms share units, ratios are 74× (C8 pp/pp) and 7× (C12 d/d), clearing T2's 1.5 floor by wide margins. A unified harmonised-scale median ratio is deferred to a post-publication mini-meta." |
| 286 (§4 P2) | "**已支持** (ordinal). Spearman ρ(\|Δ_ST\|, persistence-rank) = +0.73 across 19 Layer-D chains in Paper 2 v2.4. Short-video (Δ_ST ≈ +0.68, …); diet (Δ_ST ≈ +0.45, …)." | "**awaiting empirical test**. No persistence-rank × \|Δ_ST\| correlation is currently computed in Paper 2 v2.4; the 19-chain MR table records causal-effect magnitudes but not decay rates. Illustrative anchors consistent in direction: post-deactivation return in short-video (Allcott et al. 2020 *AER*); post-intervention weight regain in diet (Mozaffarian 2016 *Circulation*). Formal cross-chain persistence compilation is a post-publication priority." |
| 288 (§4 P3) | "**已支持 (strong)**. Paper 2 v2.4 *G*^c calibration: ρ(Δ_ST, *G*^c) = +0.98 for luxury consumption (N = 34 countries); R² = 0.92 after PDI + LTOWVS adjustment. Education investment: ρ(Δ_ST, LTOWVS) = +0.84." | "**partially supported**. Paper 2 v2.4's 59-country Hofstede-grounded G^c index (formula G^c = z(PDI) + z(LTOWVS) − z(IDV)) and 25-country ISSP aspirational-wealth panel yield joint-predictor R² = 0.255, exceeding P3's ≥ 0.15 falsification floor but not the ≥ 0.40 target. Paper 2 itself notes Layer C cross-domain ISSP replication is weak (6/11 directional matches)." |
| 290 (§4 P4) | "**部分已支持**. TikTok (EST) grew average daily minutes 3.2× faster than YouTube-auto-play (weak EST) 2018–2022; variable-ratio slots show 4× loss-chasing persistence vs fixed-ratio roulette (Dow-Schüll 2012). Formal Δ_ST estimates per platform pair pending." | "**qualitatively supported**. Paper 2 Layer A shows the EST case (A5 Olds-Milner, Δ_ST = +0.97) exceeds all MST sensory-exploitation cases (Δ_ST ≤ 0.82). Illustrative platform-level anchors often cited in this space (TikTok-vs-YouTube growth differential; Dow-Schüll 2012 on variable-ratio gambling architecture) motivate the qualitative EST > MST claim; the quantitative `≥ 1.5×` and `< 1/2 timescale` predictions require a matched-platform study not contained in Paper 2 v2.4." |
| 292 (§4 P5) | "Spearman ρ(animal layer A, human layer D) = +1.00 on **6 overlapping mechanism cells** in Paper 2 v2.4; cross-layer β = +1.58, *p* = 0.019." | "The pre-registered A+D joint meta-regression yields olds_milner β = +1.58 (within-layer z-scale), Wald χ²(2) = 5.49, *p* = 0.019 (Paper 2 v2.4 §6, §M9). Descriptive Spearman ρ(A, D) = +1.00 on the **2 overlapping mechanism categories** (olds_milner, sensory_exploit) is a geometric identity at n = 2, flagged in Paper 2's Limitation list; inferential support comes from the A+D joint test, not the n = 2 ρ." |
| 294 (§4 closing) | "**Four** predictions are already supported; P4 has partial evidence" | "**One prediction (P5)** is strongly supported by the pre-registered A+D joint test; **P1** is qualitatively supported (6/6 domain direction, 4/6 non-overlapping CIs) with quantitative mini-meta pending; **P3** is partially supported (ISSP R² = 0.255, exceeds falsification floor but below target); **P2 and P4** await empirical test with motivating anchors from existing literature" |

### 4.3 `paper1-theory/05-manuscript/abstract.md`

| Line | v1.0 text (truncated) | v1.1 replacement |
|---|---|---|
| 10 | "five falsifiable predictions, **four** of which are already supported by existing empirical data" | "five falsifiable predictions, **of which one is strongly supported by a pre-registered cross-layer meta-regression (p = 0.019), one is partially supported, one is qualitatively supported pending a quantitative test, and two await empirical test**" |

---

## §5 Additional unverified claims (flagged for future review)

While auditing P1-P5, additional empirical claims in the Paper 1 v1.0 manuscript were noted but not fully audited in this pass. Flagged for future verification:

- Intro §1 (line 30-34): annual avian death toll 365 M-1 B (Loss et al. 2014); 8 Mt/yr ocean plastic (Jambeck et al. 2015); US median daily mobile 4.8 h (DataReportal 2023); 17 tsp added sugar (Wang et al. 2023 *LPH*); $5,910 consumer debt (Federal Reserve 2023). These are external citations and not from Paper 2, but the specific numbers should be re-verified against the primary sources before submission.
- §2.5 canonical cases (lines 192, 201, 209): Boyd-Richerson, Henrich-McElreath citations for RST dynamics — verify page/section numbers.
- §3.4 Theorem T4 Interpretation: "Naturally emerging Sweet Traps are bad. Adversarially engineered Sweet Traps … are strictly worse along three axes" — theoretical claim, no empirical number to verify.
- §5 framework positioning: DellaVigna-Linos 2022 "3× shrinkage" figure — verified in Paper 2 corpus; retained.
- §6.2 minimal paradigm cost "$6K total" — internal budget estimate; no verification needed.

These items are not F3-flaw severity and do not block submission of the integrity-corrected v1.1, but should be worked through during final copy-edit.

---

## §6 Recommendations

1. **Rebuild P1 with a harmonised-scale mini-meta.** Apply Borenstein 2009 conversions (log OR → d; r → d; pp → d via base rate) to all 12 rows of `intervention_asymmetry_table.csv`. Compute within-domain Cohen-d-equivalent ratios with bootstrap CIs. Target a 1-week post-audit deliverable; update `intervention_asymmetry_compile.py` accordingly.

2. **Rebuild P2 by compiling a persistence-rank table.** For each of the 20 Layer-A + 5 Layer-B + 19 Layer-D cases, extract a persistence proxy (abandonment rate within window; relapse fraction; half-life). Correlate with |Δ_ST|. This is feasible from existing primary sources; estimated 2-3 weeks' work.

3. **Do not re-open the theory** in response to this audit. The axioms, theorems, and lemmas are unchanged; only the empirical annotations and the abstract's counting statement need correction. Stage 1-B theory-revision work can proceed independently.

4. **Add a standing integrity-check subroutine** to the Paper 1 revision workflow: every empirical claim in §4 Predictions and in the Abstract must have a file/row citation to Paper 2 v2.4 (or a clearly marked external-literature citation) before any revision is declared complete.

5. **Flag to peer-reviewer that the F3 fatal flaw is corrected.** The corrected v1.1 can be re-sent to peer-reviewer with this audit log for confirmation that the F3 flaw is resolved.

---

*End of integrity audit log. v1.0 → v1.1 empirical-integrity correction complete 2026-04-18.*
