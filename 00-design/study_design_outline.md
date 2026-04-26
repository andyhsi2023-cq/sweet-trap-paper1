# Study Design Outline: 5 Focal Studies + 1 SI External-Validation

**Status:** Stage 1 gate output — detailed Study-level execution plan
**Date:** 2026-04-17
**Companion to:** `domain_selection_matrix.md`
**Target journal:** *Nature Human Behaviour*

---

## 0. Cross-Study identification template

All five Studies share the same identification skeleton. The template is:

```
Primary (Sweet DV ← Treatment):
  SweetDV_{i,t} = α_i + γ_t + β₁ · Treatment_{i,t} + X_{i,t} · φ + ε_{i,t}

Companion (Bitter outcome ← Treatment, one-wave lag):
  BitterOutcome_{i,t} = α_i + γ_t + β₂ · Treatment_{i,t-1} + X_{i,t} · φ + ε_{i,t}

λ-moderator test:
  SweetDV_{i,t} = α_i + γ_t + β₁ · Treatment_{i,t} + β₃ · (Treatment × λ_proxy)_{i,t} + X · φ + ε

Welfare quantification (per Prediction 4):
  ΔW_{CE,d,G} = β̂₁ · σ(W) + β̂₂ · σ(Y) / (1+r)^τ  −  costs(Treatment)
```

where α_i is person FE, γ_t is wave FE, X is a minimal covariate set held constant across domains.

**Minimal cross-domain covariates (common across all 5 Studies):**
`age, age², gender (as within-household moderator only), eduy (pre-period), household_size, year dummies`. Nothing that varies endogenously with Treatment enters X unless pre-registered as a specification-curve branch.

**Sample rule common across Studies:** balanced-at-entry sample (observed in ≥ 3 waves). Robustness: unbalanced-at-entry sample, inverse-probability attrition weights.

**Standard errors:** two-way clustered at (person, year) for the primary spec; household-clustered alternative in SCA.

---

## 1. Study 1 — Urban over-investment (D1)

**Executed in Paper 1 (`infra-growth-mismatch`). Main-text recap is 1 paragraph + 1 Figure 1 panel.**

| Field | Content |
|:---|:---|
| Sample | N ≈ 84,000 person-years, 2010-2022 CFPS × city-level IGMI merge |
| Treatment | `IGMI_residual_{c,t}` — city-level infrastructure-growth-mismatch residual |
| Sweet DV | `qn12012` life satisfaction (1-5 Likert) |
| Bitter outcome (domain-level, city-level, not within-person) | GDP impulse-response from year 2 onward (−0.34 SD at 5-yr horizon) |
| λ moderator | Age × hukou × expected-migration (young movable = high λ) |
| Identification | Person FE + year FE. Primary coefficient from Paper 1: β=+0.486 (p=0.032, Model 3). SCA median: +0.192. |
| Pre-reg | OSF pre-reg from Paper 1 re-used; explicit cross-reference |
| Role in this paper | **Opening Study** — narrative bridge from Paper 1. Figure 1 Panel A shows D1 as the founding instantiation. No new analysis in Paper 2. |

**Why include if no new analysis?** D1 establishes that all four primitives activated jointly in one domain with a documented within-person paradox. Without D1, the construct lacks a worked instantiation; with D1, the remaining 4 Studies are "replication with variation" tests, which is a stronger framing.

---

## 2. Study 2 — 996 overwork (D3) — **HEADLINE STUDY**

**Why headline:** highest weighted score (8.80), cleanest identification, λ proxy operationalizable, policy relevance (PRC labor law enforcement 2025-2026).

### 2.1 Sample

- CFPS 2010-2022, 7 waves
- Restrict: `jobclass ∈ {employed wage earner}` — drops farmers, retirees, students, self-employed
- Expected N ≈ 40,000 person-years × 20,000 unique persons
- Balanced-at-entry subsample (observed ≥3 waves): N ≈ 25,000

### 2.2 Variables

| Variable | Name in CFPS | N | Role |
|:---|:---|:---:|:---|
| Treatment | `workhour` (weekly hours) → derived `overtime_d = 1[workhour > 48]` | 41K | 996-binary |
| Treatment continuous | `workhour` | 41K | continuous alternative |
| Sweet DV primary | `qg406` overall job satisfaction (5-point) | 53K | Sweet endorsement |
| Sweet DV secondary | `qg405` promotion satisfaction | 42K | Sweet, career-focused |
| Bitter outcome primary | `qp401` chronic disease 0/1 | 84K | Welfare cost (health) |
| Bitter outcome secondary | `health` self-rated 1-5 | 85K | Welfare cost (general) |
| Bitter outcome mechanism | `qq4010` sleep hours | 27K | Mechanism mediator |
| λ proxy | `(has_spouse × has_child)` from `familysize, child_num` | 73K | Externalization to family |
| λ proxy alt | `workplace ≠ hukou city` (migrant flag) | 32K | Migrant separation |

### 2.3 Pre-registered hypotheses

**H1 (Sweet response, P1 of construct):**
`qg406_{i,t} = α_i + γ_t + β₁ · overtime_d_{i,t} + X·φ + ε`
Predicted: **β₁ > 0 with p < 0.05**.

**H2 (Bitter response, P1 complement):**
`qp401_{i,t} = α_i + γ_t + β₂ · overtime_d_{i,t-1} + X·φ + ε`
Predicted: **β₂ > 0 with p < 0.05**. One-wave lag (~2 years) is the identifying timing assumption.

**H3 (λ-heterogeneity, P2):**
`qg406_{i,t} = α_i + γ_t + β₁ · overtime_d + β₃ · (overtime_d × (spouse × child))_{i,t} + X·φ + ε`
Predicted: **β₃ > 0**. Workers who externalize caregiving cost to spouse show larger satisfaction response.

**F-test / falsification:** If H1 fails (null or negative with 95% CI excluding positive), D3 exits focal roster; null reported in main text per F1 rule. If H2 fails, mechanism falsified; D3 becomes "Sweet without Bitter" = not a Sweet Trap = reported but reframed.

### 2.4 Expected output

- Figure 2 Panel A: coefplot of β̂₁ for Sweet DV (with 95% CI); β̂₂ for Bitter outcome
- Figure 3 Panel A: specification curve across ≥500 variants (alt treatments, alt samples, alt controls)
- Figure 4 primitive decomposition: D3 λ-share + β-share estimated via structural method
- Main text: "Workers whose weekly hours exceed 48 show a β̂₁ = [TBD] SD increase in job satisfaction and a β̂₂ = [TBD] p.p. increase in one-wave-lagged chronic-disease incidence; the λ-moderation β̂₃ confirms that the pattern intensifies for workers whose family bears concurrent caregiving burden."

### 2.5 Role in paper

**Headline / abstract anchor.** The D3 coefficient triplet (β̂₁, β̂₂, β̂₃) is the one-sentence Sweet Trap demonstration, repeated in Abstract, Introduction's last paragraph, and Conclusion.

---

## 3. Study 3 — Premium housing / status goods (D8)

**Why second-headline:** weighted 8.25, Luttmer 2005 QJE theoretical anchor, Chinese housing boom provides temporal variation, absorbs D6 (BNPL) via household-debt secondary analysis.

### 3.1 Sample

- CFPS 2010-2022, 7 waves
- Restrict: urban households with housing observations — N ≈ 60,000 person-years
- Homeowner subsample for primary identification: N ≈ 45,000

### 3.2 Variables

| Variable | CFPS | N | Role |
|:---|:---|:---:|:---|
| Treatment primary | `mortgage_burden = mortage / fincome1` | 20-86K (varies by year) | Mortgage stress intensity |
| Treatment alt | `resivalue` (house value percentile rank within city × year) | 86K | Positional house value |
| Sweet DV primary | `dw` self-rated social status | 84K | Status pride (status good) |
| Sweet DV secondary | `qn12012` life satisfaction | 84K | General endorsement |
| Bitter outcome primary | `savings` liquid savings (log) | 86K | Savings crowd-out |
| Bitter outcome secondary | `house_debts` balance | 85K | Debt stress level |
| Bitter outcome tertiary (D6 absorption) | `nonhousing_debts / income` | 73K | Consumer-credit burden |
| λ proxy primary | sole-debtor flag (`h_loan = 1` × `married = 0`) vs shared | 85K | Externalization to co-signer |
| λ proxy secondary | `age × child_num` — has-adult-child = housing-as-bequest = low λ | 73K | Intergenerational wealth transfer |

### 3.3 Pre-registered hypotheses

**H1:** `dw_{i,t} = α_i + γ_t + β₁ · mortgage_burden_{i,t} + X·φ + ε`. Predicted **β₁ > 0**.

**H2:** `log(savings)_{i,t} = α_i + γ_t + β₂ · mortgage_burden_{i,t-1} + X·φ + ε`. Predicted **β₂ < 0** (savings crowded out).

**H3:** Sole-debtor interaction: `dw ~ mortgage_burden × sole_debtor`. Predicted: **β₃ > 0** for sole debtors (can't externalize → lower λ → weaker Sweet endorsement — this is a **negative λ prediction** that strengthens the construct).

**H4 (positional test, distinguish from income):** Add `log(household_income)` and `total_asset` as controls; primary coefficient should survive. If β₁ disappears when income is controlled, D8 collapses to income story (not positional); report and downgrade.

### 3.4 Expected output

- Figure 2 Panel B: β̂₁ for `dw` (status); β̂₂ for `savings` (welfare cost)
- Figure 2 companion panel: positional-goods mechanism — `dw` response to percentile-rank treatment vs absolute-value treatment
- Figure 4 primitive decomposition: D8 expected to be θ-dominant (status) + ρ-significant (neighborhood lock-in)

### 3.5 Role in paper

**Second headline.** Pairs with D3 as the "labor + consumption" dual Sweet Trap. Provides the Luttmer (2005 QJE) and Frank (2007) narrative connection for Western readers.

---

## 4. Study 4 — Intensive parenting / 双减 policy shock (D2)

**Why high-novelty / high-leverage:** max novelty (9/9), 双减 DID is the cleanest causal identification in the paper, gives policy-relevance hook.

### 4.1 Sample

- CFPS 2010-2022, 7 waves
- Restrict: households with `child_num ≥ 1` — N ≈ 50,000 person-years
- DID sample (2018-2022 waves only, pre/post 2021): N ≈ 18,000
- Child-module merge (optional): CFPS 2016, 2018, 2020, 2022 child questionnaire — attempted in Week 2 of Stage 2; SI fallback if merge fails.

### 4.2 Variables

| Variable | CFPS | N | Role |
|:---|:---|:---:|:---|
| Treatment primary | `eexp_share = eexp / expense` | 85K | Parenting intensity |
| Treatment secondary | `school` education training spend | 85K | Shadow-education spending |
| Sweet DV primary | `qn12012` (parental) life satisfaction | 84K | Parental endorsement |
| Bitter outcome primary | `(expense - eexp) / expense` non-education consumption share | 85K | Financial crowd-out on family |
| Bitter outcome secondary (if child module merged) | child `qp401`, child `qn12012` | TBD | Child welfare |
| λ proxy | `child_gender = male` (sons receive higher investment intensity); parent `eduy × occupation` | 78K / 85K | Parent-to-child cost transfer capacity |
| 双减 DID treatment | `post2021 × high_baseline_tutoring` | 18K | Policy-shift λ reduction |

### 4.3 Pre-registered hypotheses

**H1:** `qn12012_{i,t} = α_i + γ_t + β₁ · eexp_share_{i,t} + X·φ + ε`. Predicted **β₁ > 0**.

**H2:** `(non-edu consumption share)_{i,t} = α_i + γ_t + β₂ · eexp_share_{i,t-1} + X·φ + ε`. Predicted **β₂ < 0**.

**H3 (双减 DID):**
`qn12012_{i,t} = α_i + γ_t + δ · (post2021_{t} × high_baseline_tutoring_{i}) + X·φ + ε`
Predicted: **δ < 0** if Sweet Trap was operative pre-policy (forcible removal of the sweet amenity causes satisfaction loss); an asymmetric result (satisfaction doesn't drop) would indicate pre-policy Sweet Trap was driven by tutoring specifically rather than parental-status generally.

**H4 (placebo):** Same DID with pseudo-treatment year 2019 (no policy). Predicted: **δ = 0**.

### 4.4 Expected output

- Figure 2 Panel C: β̂₁ and β̂₂ coefplots
- **Figure 3 Panel C: 双减 DID event-study** — plotting wave-specific satisfaction differential between high-baseline-tutoring vs low-baseline-tutoring households from 2014 to 2022, with 2021 as intervention
- Policy-relevance callout box

### 4.5 Role in paper

**Policy-shocked Study.** The 双减 DID is the paper's most causally-identified result. Figure 3 Panel C is designed to be the "natural experiment" visual. If H3 fires as predicted, this Study carries significant narrative weight at review.

### 4.6 Contingency if child module merge fails

**Fallback plan:** Keep Study 4 at the parent level only. The primary Sweet DV (parental satisfaction) and primary Bitter outcome (household consumption crowd-out) do not require child module. The 双减 DID remains the headline result. Child-level welfare evidence moves from main text to SI §D (child-module merge, when completed post-submission).

---

## 5. Study 5 — High-sugar/high-fat diet (D5)

**Why included:** highest β-mechanism maturity (Laibson/Cawley-Ruhm/Hall 2019 RCT), needed for cross-biology universality argument, prevents construct from looking China-institution-specific.

### 5.1 Sample

- CFPS 2010-2022, 7 waves
- Full sample: N ≈ 84,000 person-years
- Adults only (age ≥ 18): N ≈ 72,000

### 5.2 Variables

| Variable | CFPS | N | Role |
|:---|:---|:---:|:---|
| Treatment primary | `food_share = food / expense` | 84K | Food-spending intensity (proxy for dietary pattern) |
| Treatment alt | NOVA-style processed-food proxy (requires construction from sub-components if available) | TBD | Ultra-processed food exposure |
| Sweet DV | `qn12012` satisfaction (general) + `Δfood_share` interpreted as revealed preference | 84K | Endorsement |
| Bitter outcome primary | `qp401` chronic disease 0/1 | 84K | Metabolic welfare cost |
| Bitter outcome secondary | `unhealth` self-rated poor health | 86K | General welfare |
| Bitter outcome tertiary | `log(mexp)` medical expenditure | 85K | Financial welfare cost (λ channel) |
| λ proxy primary | has-public-insurance flag (cost socialized → high λ) | TBD from `insurance` vars | Health-system externalization |
| λ proxy secondary | `age` (older = shorter horizon, cost to society = high λ) | 86K | Temporal horizon |

### 5.3 Pre-registered hypotheses

**H1:** `qp401_{i,t} = α_i + γ_t + β₁ · food_share_{i,t-1} + X·φ + ε`. Predicted **β₁ > 0**.

**H2:** `qn12012_{i,t} = α_i + γ_t + β₂ · Δfood_share_{i,t} + X·φ + ε`. Predicted **β₂ > 0**. (Contemporaneous satisfaction bump from dietary freedom / palatability shift.)

**H3 (λ-attenuation):** `qn12012 ~ Δfood_share × has_public_insurance`. Predicted: **β₃ > 0** (public-insurance population has higher λ, stronger Sweet response). Consistent with Bernheim-Taubinsky moral-hazard framing.

**F-test:** If H2 is null or negative — meaning food-spend increases don't correlate with satisfaction — then D5 fails P1 and exits main text. This is a real risk because `food_share` is coarse; we would then report in SI as "domain where CFPS measurement is insufficient for Sweet DV detection." This is the boundary-conditions-statement that strengthens construct falsifiability.

### 5.4 Expected output

- Figure 2 Panel D: β̂₁, β̂₂ coefplots
- Figure 4 primitive decomposition: D5 expected to be β-dominant, λ-moderate, θ-weak, ρ-moderate (habituation)

### 5.5 Role in paper

**Universality anchor / boundary-conditions check.** If results fire, D5 establishes the construct extends to biology-anchored domains (not just institutional). If results are null, D5 becomes the falsifiability evidence that the construct is real (not tautological) — a finding that survives peer review better than forced confirmations.

**Publication framing:** We commit in the main text to either outcome being acceptable; the pre-registered plan includes both "Study 5 confirms" and "Study 5 boundary" write-ups.

---

## 6. SI Study — Bride price / wedding expenditure (D4, external validation)

**Why in SI rather than main text:** CFPS lacks bride-price variables (see `cfps_variable_inventory.md` §4). Does not qualify for focal roster but represents a structurally distinct domain that tests construct generalizability.

### 6.1 Data source alternatives (decide in Stage 2 Week 3)

| Dataset | Wedding variable | Panel? | Feasibility |
|:---|:---|:---|:---|
| **CHARLS** (China Health and Retirement Longitudinal Study) | Retrospective wedding-expense in wave 2013; possibly wave 2018 | Yes, 4 waves | Moderate — recall bias, older population |
| **CGSS 2013 / 2017** | Direct bride-price module | Cross-section | Lower — no within-person ID |
| **CFPS family module** (fa1, fb1 questionnaires) | Unknown; audit needed | TBD | To investigate |

**Decision:** Attempt CHARLS first (has retrospective + longitudinal); CGSS as fallback cross-sectional validation.

### 6.2 Design (preliminary)

- Treatment: `log(bride_price_paid)` or `log(total_wedding_expense)`
- Sweet DV: retrospective marital satisfaction or life satisfaction 5-10 years post-wedding
- Bitter outcome: household net worth trajectory 2013 → 2018
- λ proxy: groom's vs bride's family responsibility shares (CHARLS has some signal on this)
- Identification: cross-sectional with geography × birth-cohort FE; OR within-person pre/post if CHARLS panel permits

### 6.3 Role

**SI §D robustness only.** Not a main-text Study. Answers the question: "Does the construct generalize beyond CFPS to other Chinese datasets and to an institution (marriage payments) where ρ is dominant?"

---

## 7. Cross-Study aggregation plan

### 7.1 Specification-curve meta-analysis (Figure 3)

For each focal domain d ∈ {D1, D3, D8, D2, D5}:
1. Run ≥ 500 specifications varying: outcome variant, sample filter, covariate set, FE structure, treatment definition, cluster level.
2. Compute median β̂₁^d and median β̂₂^d with 95% bootstrap CI.
3. Stack across domains into a single cross-domain SCA panel.

**Headline meta-statistic:** "In X of 5 focal domains, the specification-curve-median sign confirms the pre-registered prediction with 95% CI excluding zero."
**Pre-committed threshold:** X ≥ 4 / 5 for construct-confirmation claim. X = 3 / 5 would downgrade to "partial confirmation, domain-specific." X ≤ 2 / 5 would be construct-falsifying.

### 7.2 Primitive decomposition (Figure 4)

For each focal domain, structurally estimate the share of the Sweet-Bitter wedge attributable to each of θ, λ, β, ρ:
- θ share: co-variation with amenity consumption
- λ share: heterogeneity across high-λ vs low-λ subgroups
- β share: differential coefficient on immediate vs lagged outcome
- ρ share: asymmetric adjustment (positive vs negative Treatment changes)

**Cross-domain prediction (P3 from construct):** `corr(σ_d(β), temporal_gap_d) > 0` and `corr(σ_d(λ), cohort_separation_d) > 0`.

Expected pattern based on domain characteristics:
- D1 urban: λ-dominant (fiscal transfer across cohorts)
- D3 996: β + λ balanced
- D8 housing: θ-dominant (positional) + ρ-moderate
- D2 鸡娃: λ-dominant (child-borne)
- D5 diet: β-dominant

If the predicted pattern emerges, P3 is confirmed. If the decomposition is uniform across domains, construct is weakened (one-primitive-dominant relabeling concern).

### 7.3 Welfare quantification (Figure 5)

For each domain, compute consumption-equivalent net welfare using:

`ΔW_{CE,d} = β̂₁^d · σ(Sweet DV)^d − β̂₂^d · σ(Bitter outcome)^d / (1+r)^τ_d`

where τ_d is the typical Sweet-Bitter temporal gap (years), and r = 0.03.

Aggregation: sum across 5 domains using CFPS population weights. Target: a single "cross-domain Sweet Trap welfare cost" figure in the 5-8% of domain-relevant consumption range.

---

## 8. Execution timeline (Stage 2: weeks 1-5)

| Week | Task | Outputs |
|:---|:---|:---|
| 1 | Finalize OSF pre-registrations for D3, D8, D2, D5; update D1 pre-reg cross-ref | 4 OSF pre-reg documents |
| 1 | CFPS cleaning pipeline: derive `overtime_d`, `mortgage_burden`, `eexp_share`, `food_share`; QA long panel | Long-panel parquet file; cleaning log |
| 2 | Execute headline specs for D3 (parallel agent 1) | D3 headline result |
| 2 | Execute headline specs for D8 (parallel agent 2) | D8 headline result |
| 3 | Execute headline specs for D2 + 双减 DID (parallel agent 3); CHARLS access for D4 | D2 headline + DID; D4 data obtained |
| 3 | Execute headline specs for D5 (parallel agent 4) | D5 headline result |
| 4 | Specification-curve analysis for all 5 domains (serial, one per day) | 5 SCA outputs |
| 5 | Primitive decomposition + welfare quantification (integrated) | Figure 4 + Figure 5 data |
| 5 | D4 SI external-validation execution | SI §D |

Computation regime: each domain's PDE runs at most 2 workers in parallel (M5 Pro 24GB constraint per repo CLAUDE.md).

---

## 9. Exit criteria → Stage 3 (integration)

| Criterion | Pass condition |
|:---|:---|
| D1 confirmed | Already done (β̂₁ = +0.486, p = 0.032) |
| D3 headline | H1 fires with |β̂₁| > 0.1 SD; H2 fires; specification curve median-positive ≥ 60% |
| D8 headline | H1 fires; H2 fires; status-interpretation survives income control |
| D2 headline + DID | H1 fires; 双减 H3 fires with predicted sign |
| D5 headline | H1 or H2 fires; if both null, report as boundary finding |
| Cross-domain | ≥ 4/5 focal domains confirm at median-SCA level |

**If cross-domain < 3/5:** manuscript downgraded to "Selective Sweet Trap operation across domains" framing for NHB, or redirected to a specialized journal (e.g., J. of Behavioral and Experimental Economics).

---

## 10. File manifest

Current outputs:
- `00-design/domain_selection_matrix.md` — Stage 1 decision record
- `00-design/study_design_outline.md` — this file

Stage 2 inputs to prepare:
- `00-design/osf_prereg_D3.md`, `osf_prereg_D8.md`, `osf_prereg_D2.md`, `osf_prereg_D5.md`
- `02-data/linkage/cfps_cleaning.md` — pipeline spec
- `03-analysis/scripts/cfps_long_panel_builder.py`
- `03-analysis/spec-curve/` — per-domain SCA subdirectories

---

*End of Stage 1 study design outline. Stage 2 (parallel domain execution) begins upon OSF pre-registration completion.*
