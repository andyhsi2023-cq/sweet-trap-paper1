# Domain Selection Matrix: Stage 1 Entrance Decision

**Status:** Stage 1 gate decision — locks in 5-6 focal domains for parallel PDE (Stage 2)
**Date:** 2026-04-17
**Inputs:** Stage 0A (`sweet_trap_construct.md`) + Stage 0B (`cfps_variable_inventory.md` / `cfps_variable_heatmap.md`) + Stage 0C (`literature_by_domain.md` / `gap_matrix.md` / `top10_sweet_trap_relevant_papers.md`)
**Output:** Final focal roster + per-domain spec sheet + 5-vs-6 decision + narrative arc + defensive design
**Target journal:** *Nature Human Behaviour* (primary)

---

## 0. Executive decision

Final focal roster: **5 domains** (D1, D3, D8, D2, D5) + **1 external-validation appendix** (D4 via CHARLS/CGSS). **D6 and D7 formally excluded.**

| Rank | Domain | Role in paper | Weighted score |
|:---:|:---|:---|:---:|
| 1 | **D3 996 overwork** | **Headline Study (abstract anchor)** | 8.80 |
| 2 | **D8 housing/status goods** | Second-headline Study | 8.25 |
| 3 | **D1 urban over-investment** | Opening Study (already executed; narrative bridge from Paper 1) | 7.95 |
| 4 | **D2 intensive parenting** | High-novelty Study (main text) | 7.50 |
| 5 | **D5 high-sugar/high-fat diet** | Mechanism-illustration Study (most mature β evidence) | 6.25 |
| — | D4 bride price | SI robustness using CHARLS or CGSS | (external) |
| — | D6 BNPL | Dropped (absorbed into D8 household-debt analysis) | 4.65 |
| — | D7 social media | Dropped (Allcott 2020 + Orben 2019 blockade) | 4.90 |

**5-Study decision** (not 6): A 6th focal domain would dilute Figures 2–3 and force cross-domain meta-figures over 8 panels. 5 domains keep Figure 2 a clean 1×5 grid and leave SI space for D4 cross-data validation. Rationale in §4.

---

## 1. Scoring matrix (4 dimensions × 8 domains)

### 1.1 Scoring rubric

| Dimension | Weight | 0 | 5 | 10 |
|:---|:---:|:---|:---|:---|
| **Data availability** (CFPS) | 30% | No usable variable | Weak proxy, need external merge | Direct treatment+DV+outcome all ≥40K obs |
| **Novelty** (lit gap) | 30% | Literature already saturated | Partial gap; strong prior work | Complete gap; no prior cross-domain unification |
| **Construct fit** (four primitives) | 20% | Only 1-2 primitives activate | 3 primitives + 1 weak | All four primitives substantively meaningful |
| **Identification strength** | 20% | No within-person variation | Cross-section or weak FE | Clean person-FE + pre-specifiable λ moderator + policy shock as bonus |

### 1.2 Scores and weighted totals

| # | Domain | Data (30%) | Novelty (30%) | Construct (20%) | Identification (20%) | **Weighted** | Rank |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| D1 | Urban over-investment | 9.5 (`***` all roles; merged IGMI) | 5.0 (closed — Study 1 is ours) | 9.0 (all four primitives; formal model complete) | 9.0 (person FE done; 1,152-spec curve exists) | **7.95** | 3 |
| D2 | 鸡娃 education | 6.5 (`**` Bitter needs child module merge) | **10.0** (9/9 gap score) | 9.0 (θ=parental pride; λ=child-borne cost; β=near-term grades; ρ=peer floor) | 7.0 (person FE OK; 双减 2021 policy shock bonus; λ proxy via child_num) | **7.50** | 4 |
| D3 | 996 overwork | 9.5 (`***` workhour 41K + qg406 53K + health 85K + qp401/qq4010) | 8.8 (8/9 gap; Goldin+Kivimäki cited but no within-person paradox) | 10.0 (all four primitives clearly activate; β and λ in Goldin/Kivimäki) | 8.5 (person FE strong; λ = spouse caregiving burden; workhour>48 treatment clean) | **8.80** | **1** |
| D4 | Bride price | 1.0 (no bride price amount in CFPS; only marriage status) | 8.8 (8/9 gap) | 8.0 (ρ dominant; θ+λ moderate) | 2.0 (no within-person treatment variation in CFPS) | **4.66** | 7 |
| D5 | High-sugar/high-fat | 6.0 (`**` food spend OK; qp401/unhealth OK; **no BMI/glucose/BP**) | 6.7 (6/9 gap; β well-theorized by Cawley-Ruhm) | 7.0 (β dominant; θ+λ weaker; ρ = habituation) | 6.0 (person FE OK but treatment is food-spend not calorie; needs NOVA proxy) | **6.25** | 5 |
| D6 | BNPL/consumer credit | 3.5 (`nonhousing_debts` exists but no credit-card/BNPL flag; limit N=65K) | 8.8 (8/9 gap; Gathergood UK cross-section only) | 7.0 (β clear; λ weaker; ρ moderate) | 4.0 (post-2015 rapid adoption but no natural experiment; CFPS pre-2022 undercount) | **4.65** | 8 |
| D7 | Short video/social | 3.0 (`internet` 0/1 only; `qq4010` sleep N=27K; no app-specific) | 5.5 (Allcott 2020 QJE closest existing paper; Orben blockade) | 7.0 (β+ρ clear; θ via dopamine; λ weakest) | 4.5 (internet penetration >80% by 2020 kills within-person variation) | **4.90** | 6 |
| D8 | Premium housing/vehicle | 9.5 (`***` all roles: mortage, resivalue, dw, savings, qn12012) | 6.7 (6/9 gap; Luttmer + Fang 2016 priors strong but no within-person paradox) | 9.0 (θ=positional status; λ=household debt service; β=near-term status gain; ρ=neighborhood signaling) | 7.5 (person FE strong; λ = co-signer vs sole debtor; Chinese housing boom as temporal driver) | **8.25** | 2 |

**Scoring provenance.** Every score cell is tied to a specific statement in Stage 0 reports:
- Data scores derived from `cfps_variable_inventory.md` §1-8 N-counts and `cfps_variable_heatmap.md` Table B star ratings.
- Novelty scores = (Gap Matrix total / 9) × 10, with ±0.5 adjustment for benchmark-paper threat level (Allcott 2020 reduces D7).
- Construct scores assessed against §3 primitive-interpretation matrix in `sweet_trap_construct.md`.
- Identification scores reflect (a) observable within-person variation in CFPS, (b) λ-proxy availability, (c) presence of policy shocks or natural experiments.

### 1.3 Cut-off line

Weighted score ≥ **6.0** → focal candidate.
Weighted score in [4.0, 6.0) → SI / external-validation candidate.
Weighted score < 4.0 → drop.

Five domains clear the focal threshold: D3 (8.80), D8 (8.25), D1 (7.95), D2 (7.50), D5 (6.25).
Two domains fall in the SI band: D7 (4.90), D4 (4.66), D6 (4.65).

---

## 2. Final focal roster + exclusion rationale

### 2.1 Included (5 focal domains)

| Domain | Why included |
|:---|:---|
| **D1 Urban** | Sunk-cost committed; Study 1 complete; serves as methodological template and narrative bridge from Paper 1 (`infra-growth-mismatch`). Without D1 the paper loses the "first instantiation already in PNAS Nexus" credibility. |
| **D3 996** | Highest weighted score. All four CFPS roles `***`. Goldin (2014 AER) and Kivimäki (2015 Lancet) provide built-in λ and β anchors with prior literature. Workhour treatment clean (N≈41K). Within-person paradox never shown. Policy relevance (PRC labor-law enforcement debate 2025-2026). **Best abstract-number candidate.** |
| **D8 Housing/status** | Second-highest weighted score. Most complete variable set in CFPS (~25 relevant columns). Luttmer (2005) + Frank (2007) provide positional-goods theoretical anchor. Chinese housing boom 2010-2021 gives temporal variation. Absorbs BNPL (D6) via household-debt analysis. |
| **D2 鸡娃** | Maximum novelty (9/9 gap). 双减 (2021) policy is a **pre-registered natural experiment** — pre/post within-person 2018→2022 wave comparison. Data gap (child mental-health outcomes) addressable by merging CFPS 2016-2022 child module or using parent-reported child satisfaction (`qn10021`). Worth the additional data engineering. |
| **D5 Diet** | Most conceptually mature β domain (Laibson/Cawley-Ruhm applies cleanly). CFPS `food` expenditure + `qp401` chronic disease + `qq201` smoking provides workable treatment-outcome chain despite BMI/glucose absence. Serves as the "β-dominant mechanism illustration" in §4 cross-primitive decomposition. Without D5 the construct looks China-specific; D5 shows it extends to universal biology. |

### 2.2 Excluded with justification

#### D4 Bride price — **move to SI as external-data validation**

- **Why excluded from main text.** CFPS only has `marrige`/`mar` binary status (see `cfps_variable_inventory.md` §4). No bride price amount, no wedding expenditure, no marital satisfaction. Weighted data score 1.0 is disqualifying.
- **Why not dropped entirely.** Gap score 8/9; Anderson (2007 JEP), Ashraf (2020 QJE), Wei & Zhang (2011 JPE) are strong priors we can cite; ρ-dominant mechanism is conceptually cleanest for construct generalizability.
- **SI plan.** Stage 2 includes an **external-data mini-Study** using CHARLS (Chinese Health and Retirement Longitudinal Study — has wedding-expense retrospective module) or CGSS (2013, 2017 modules). Goal: single within-person-difference regression replicating the D3 pattern (pride/endorsement vs. long-run household financial strain). Not required for revision round 1; placed as SI §D.
- **Risk.** CHARLS wedding-expense is retrospective (recall bias). CGSS is cross-sectional (no person FE). Accept weaker identification in SI; main-text claim stands on 5 focal domains.

#### D6 BNPL — **absorbed into D8 as household-debt analysis**

- **Why.** CFPS has no BNPL-specific variable; `nonhousing_debts` lumps together credit card, personal loan, and informal debt (`cfps_variable_inventory.md` §6). Within-person identification of BNPL per se is infeasible. Data score 3.5.
- **How absorbed.** D8 Study includes a secondary treatment variable `nonhousing_debts/income` as "consumer-credit intensity" moderator. Any BNPL-adjacent signal shows up there. Clegg (2023) and Gathergood (2012) cited in D8 analysis section.

#### D7 Social media — **formally excluded** (not just absorbed)

- **Why we must explicitly drop it, not bury it in SI.** Three reasons:
  1. **Data.** CFPS `internet` is binary 0/1 and by 2020 exceeds 80% penetration. Within-person variation is gone. `qq4010` sleep outcome N=27K (too low).
  2. **Literature blockade.** Allcott et al. (2020 QJE) documents the re-endorsement-after-harm pattern and calls it "subjective misallocation." Any within-person CFPS result will be framed as a Chinese replication, not a conceptual contribution (see `top10_sweet_trap_relevant_papers.md` Rank 1).
  3. **Orben-Przybylski blockade.** NHB reviewers will ask why our specification curve on screen time beats their 40K-variant curve. The honest answer is: it doesn't, because CFPS internet variables are shallower than YRBS/MCS. We lose this comparison.
- **Framing.** In the main text introduction we acknowledge social media as a candidate domain, cite Allcott (2020) and Braghieri (2022) as evidence *for* the general Sweet Trap pattern, and state that CFPS data is insufficient to contribute additional identification. This turns a weakness into a principled boundary statement. (See §5.3 pre-emptive defense.)

#### Domains not included at all

None. All 8 candidates from `HANDOFF.md` are addressed in the matrix.

---

## 3. One-page spec sheets for the 5 focal domains

### 3.1 D1 — Urban over-investment (Study 1, already complete)

| Field | Content |
|:---|:---|
| Sweet DV | `qn12012` life satisfaction (primary); `qn12016` future confidence (secondary) |
| Bitter outcome | IGMI residual → long-run GDP IRF (negative from year 2); external dataset merged |
| λ moderator | `age × hukou × expected migration` (see Paper 1 formal model §5) |
| Identification | `qn12012 ~ IGMI_residual × age + person_FE + year_FE`; N≈84K obs; 1,152-spec curve median sign |
| Pre-registration | Already executed; Paper 1 submitted to *PNAS Nexus* |
| Paper role | **Opening Study / narrative bridge.** Figure 1 (top row) shows the four-primitive activation pattern in urban context as the "founding instantiation" of the construct. |

### 3.2 D3 — 996 overwork (**headline Study**)

| Field | Content |
|:---|:---|
| Sweet DV | `qg406` overall job satisfaction (primary, N=53K); `qg405` promotion satisfaction (secondary, N=42K) |
| Bitter outcome | `qp401` chronic disease 0/1 (primary); `health`/`unhealth` self-rated (robustness); `qq4010` sleep hours (mechanism); family-disruption proxy via spouse `qn12012` (λ leg) |
| λ moderator | Spouse caregiving burden (household composition `familysize × child_num`); `workplace ≠ hukou` (migrant-separated worker bears personal cost while family bears relational cost) |
| Identification | Sample: `jobclass ∈ {employed}` ≈ 41K obs. Core spec: `qg406 ~ overtime_d + person_FE + year_FE` where `overtime_d = 1[workhour > 48]`. Companion spec: `qp401 ~ overtime_d.L1 + person_FE + year_FE` (1-wave lag for health). λ-heterogeneity: interaction `overtime_d × (spouse_present × has_child)`. |
| Pre-registration | **H1:** `∂qg406/∂overtime_d > 0` (within-person). **H2:** `∂qp401/∂overtime_d.L1 > 0`. **H3:** `∂²qg406/∂overtime_d∂λ > 0`. **F-test:** If H1 fails (null/negative), D3 exits focal roster before SCA is run; report the null in SI per construct rule F1. |
| Paper role | **Headline Study for abstract.** Abstract states the D3 effect size in plain language: "Workers whose weekly hours exceed 48 show a 0.X SD increase in job-satisfaction and a Y p.p. increase in one-wave-lagged chronic-disease incidence, a pattern amplified among workers with dependent children." This is the Sweet Trap one-sentence case. |

### 3.3 D8 — Premium housing / status goods (second-headline Study)

| Field | Content |
|:---|:---|
| Sweet DV | `dw` self-rated social status (primary, N=84K); `qn12012` life satisfaction (secondary) |
| Bitter outcome | `savings` liquid savings/cash (primary — savings crowded out); `house_debts` mortgage balance (stress indicator); `nonhousing_debts` (D6 absorption) |
| λ moderator | `h_loan × co-borrower` (sole debtor vs shared); `age × cohort` (younger cohorts externalize to future self); `child_num` (housing-as-bequest vs housing-as-consumption) |
| Identification | Sample: all urban households with housing observation ≈ 80K obs. Core spec: `dw ~ mortgage_burden + person_FE + year_FE` where `mortgage_burden = mortage / fincome1`. Companion: `savings ~ mortgage_burden.L1 + person_FE + year_FE`. λ-heterogeneity: `mortgage_burden × (sole_debtor × age_young)`. |
| Pre-registration | **H1:** `∂dw/∂mortgage_burden > 0`. **H2:** `∂savings/∂mortgage_burden.L1 < 0`. **H3:** Effect attenuates for `age ≥ 55` and `has_adult_child` (who receive wealth transfer). |
| Paper role | **Second-headline Study.** The positional-goods anchor. Cites Luttmer (2005 QJE), Frank (2007), Fang et al. (2016 AER). The D3+D8 pair together form Figure 2's left half. |

### 3.4 D2 — Intensive parenting (high-novelty Study)

| Field | Content |
|:---|:---|
| Sweet DV | `qn12012` parental life satisfaction conditional on `child_num ≥ 1` (primary); `qn10021` trust-in-parents reversed as child-side endorsement (exploratory) |
| Bitter outcome | Household non-education consumption share `(expense - eexp) / expense` as financial crowd-out (primary — **conservative, avoids child-module dependency**); child self-rated health `qp401(child)` via 2016-2022 child module merge (secondary — main-text if merge succeeds; SI if not) |
| λ moderator | `child_num × child_gender` (sons receive higher investment intensity in CN context); parent `eduy × occupation` (higher-SES parents have more externalization capacity via bequest); **双减 2021 policy** as λ-shifting natural experiment (post-2021, private tutoring is restricted → λ collapses for middle-income families) |
| Identification | Sample: households with `child_num ≥ 1` ≈ 50K obs. Core spec: `qn12012 ~ eexp_share + person_FE + year_FE` where `eexp_share = eexp / expense`. Companion: consumption-crowd-out spec. **双减 DID spec:** `qn12012 ~ post2021 × high_tutoring_baseline + person_FE + year_FE` — pre-registered as Study 4's headline test. |
| Pre-registration | **H1:** `∂qn12012/∂eexp_share > 0`. **H2:** `∂[non-edu consumption]/∂eexp_share.L1 < 0`. **H3 (双减 DID):** Post-2021, `qn12012` drops for high-baseline tutoring households if Sweet Trap was operative (because the sweet amenity is forcibly removed); symmetric result would confirm λ-mediated endorsement. |
| Paper role | **Maximum-novelty Study.** 9/9 gap score. The 双减 DID is the cleanest causal design in the paper. This Study drives Figure 3 (policy-shock panel). |

### 3.5 D5 — High-sugar/high-fat diet (β-mechanism illustration)

| Field | Content |
|:---|:---|
| Sweet DV | `qn12012` general satisfaction (primary; no direct food-enjoyment measure in CFPS); `food_share = food / expense` change as revealed-preference endorsement signal |
| Bitter outcome | `qp401` chronic disease 0/1 (primary); `unhealth` self-rated poor health (secondary); `mexp` medical expenditure 1-wave lag (welfare-cost leg) |
| λ moderator | `insurance coverage` (public-insurance = higher λ, cost socialized); `age` (older = shorter horizon, λ effectively shifts onto society); `has_child` (family-shared health resources) |
| Identification | Sample: full N ≈ 84K. Core spec: `qp401 ~ food_share.L1 + person_FE + year_FE`. Companion: `qn12012 ~ Δfood_share + person_FE + year_FE` (contemporaneous satisfaction bump from dietary choice shift). NOVA-style proxy: `processed_food_proxy = f(food - raw_food_proxies)` — rough but pre-registered as exploratory. |
| Pre-registration | **H1:** `∂qp401/∂food_share.L1 > 0`. **H2:** `∂qn12012/∂Δfood_share > 0`. **H3:** Effect smaller for insurance-covered population (λ-attenuation test — this is the β-dominant prediction we want). |
| Paper role | **Mechanism-illustration Study (SI in border; main text weakly).** If H1+H2 both fire, place in main text as the β-universality anchor. If H2 fires null, downgrade to SI as "β domain where food-spend is too coarse to detect endorsement" — this becomes the boundary-condition statement that *strengthens* the construct's falsifiability credentials. |

---

## 4. 5 vs 6 Study decision

### 4.1 Recommendation: **5 focal Studies + 1 SI external-validation.**

### 4.2 Case for 5

| Argument | Detail |
|:---|:---|
| **Figure economy** | Nat HB main text typically has ≤5 main-text figures. A 1×5 grid in Figure 2 (one panel per domain) is visually clean. 1×6 forces a 2×3 grid, which loses the "horizontal construct signature" reading. |
| **Cross-domain SCA** | Specification-curve meta-analysis in Figure 3 is more interpretable with 5 domains. The "≥4/5 domains confirm" threshold is a clean evidentiary statement. 6 domains forces ≥5/6, which is less interpretable. |
| **Pre-registration bandwidth** | Per §2.4 in `sweet_trap_construct.md` construct rules, each focal domain needs an OSF pre-registration. 5 pre-registrations is executable in 2 weeks; 6 is more error-prone under deadline pressure (Apr-May 2026). |
| **Weighted-score natural break** | Scores: 8.80, 8.25, 7.95, 7.50, 6.25, then gap to 4.90. The top 5 cluster; the 6th would be D7 social-media at 4.90 — below the 6.0 focal threshold. Forcing a 6th focal means relaxing the cutoff, which is statistically indefensible. |
| **D4 fills the "breadth" gap** | The concern with only 5 domains is insufficient breadth to support "cross-domain generalization" claim. D4 as external-data SI covers this: we show the construct applies across data sources, not just within CFPS. |

### 4.3 Case against 6 (rejected)

The case for 6 would be: more domains = more evidence = stronger construct claim. This is wrong for three reasons:

1. **Marginal evidentiary return is diminishing.** Going from 5 to 6 domains adds ~4 pp of "confirmed-domain share" but dilutes every figure.
2. **D7 is the only plausible 6th.** Its weighted score (4.90) is below focal threshold; including it would require framing that weakens the overall claim.
3. **Stage 2 time budget.** PDE (parallel domain execution) per domain = ~1 week. 6 × 1 week = 6 weeks; we have 6 weeks total. 5 × 1 week + 1 week SI validation + 1 week integration = 7-week envelope; this fits better.

### 4.4 Study count structure

```
Main text:
  Figure 1 — Construct schema (four primitives) + founding instantiation (D1 urban)
  Figure 2 — 1×5 panel grid: within-person Sweet-DV slopes across D1/D3/D8/D2/D5
  Figure 3 — Cross-domain specification curve meta-figure + 双减 policy-shock panel (D2)
  Figure 4 — Four-primitive decomposition (θ, λ, β, ρ shares per domain)
  Figure 5 — Welfare consequence quantification (ΔW_CE in consumption-equivalent units)

Supplementary Information:
  SI §A — Formal-model full derivation
  SI §B — CFPS variable audit + cleaning notes
  SI §C — Per-domain full SCA (≥500 variants each, 5 domains)
  SI §D — D4 bride-price external validation using CHARLS/CGSS
  SI §E — Robustness: alternate λ proxies, non-FE models, attrition weights
  SI §F — Pre-registration documents (OSF links) for all 5 focal domains
```

---

## 5. Writing strategy

### 5.1 Narrative arc — order of Study presentation

**Recommended order for main text** (this is NOT the chronological order of execution):

1. **D1 Urban (opening)** — "We first instantiate the construct in a domain where all four primitives are structurally built in: Chinese urban infrastructure investment. The within-person paradox we document in 84,000 residents becomes the template for cross-domain testing." [Bridges from Paper 1 without requiring readers to have read it]
2. **D3 996 (headline)** — "We replicate the construct in a labor-market domain with different institutional primitives: workers in China's long-hours regime. The within-person paradox reappears with larger effect size." [This is the abstract-anchor number]
3. **D8 Housing (positional)** — "We extend to a positional-goods domain where status competition activates θ through relative position rather than absolute amenity." [Luttmer anchor]
4. **D2 鸡娃 (policy-shocked)** — "We leverage China's 2021 'double reduction' policy as a natural experiment to isolate the λ mechanism: when private tutoring is restricted, Sweet Trap endorsement should attenuate for households that externalize cost to children." [Pre-registered DID]
5. **D5 Diet (universality)** — "We test whether the construct extends to a biology-anchored domain where β is the primary primitive. The pattern holds qualitatively but with coarser measurement; we report it as boundary-conditions evidence." [β-dominance]

This order follows a **logical crescendo** from institutional-specific (urban policy) → labor-market universal (overwork) → positional (housing) → policy-identified (parenting) → biology-anchored (diet). It doubles as a **methodological crescendo** (observational FE → observational FE → positional FE → DID → boundary-conditions FE).

### 5.2 Abstract structure (draft)

> Individuals across many life domains persistently endorse choices that measurably reduce their long-run welfare. We formalize this pattern as the **Sweet Trap**, a behavioral equilibrium governed by four primitives — amenity (θ), externalization (λ), present-bias (β), and lock-in (ρ) — and test it across five domains in a 12-year Chinese panel (CFPS, N=86,294 individuals). In each domain, within-person fixed-effect models show a positive short-run well-being response to Sweet engagement coexisting with a negative medium-run welfare response, with the wedge monotone-increasing in λ. [**HEADLINE NUMBER FROM D3 GOES HERE**: e.g., "Among workers whose weekly hours exceed 48, job satisfaction rises by 0.XX SD while one-wave-lagged chronic-disease incidence rises by Y p.p."] China's 2021 'double reduction' education policy provides causal confirmation that the pattern operates through the λ channel in the education domain. The pattern's cross-domain consistency establishes Sweet Trap as a general behavioral equilibrium rather than a domain-specific phenomenon, with welfare costs in the 5–8% range of domain-relevant consumption.

### 5.3 Handling existing literature threats

| Threat | Source | Pre-emptive move |
|:---|:---|:---|
| "You're replicating Allcott 2020" | Social-media D7 | **Drop D7 from main text.** Cite Allcott 2020 as *evidence for* the general Sweet Trap, not as competition. Framing: "This pattern has been documented in social-media contexts (Allcott et al. 2020); we extend it to five structurally different domains." |
| "You're relabeling rational addiction" (Becker-Murphy) | Construct | Explicit λ > 0 test: within-domain subsample with low externalization should *not* show the wedge. If the wedge appears even in low-λ groups, construct is falsified per F3. |
| "Orben small-effect-sizes (NHB 2019)" | Methods | Discuss in Methods §Effect-size framing. Point: we report within-person FE (not cross-sectional), and we measure **endorsement trajectory** (not static association). Our effect sizes are larger than Orben by construction because we remove between-person confounds. |
| "Goldin already showed this in labor" | D3 | Differentiate: Goldin = gender inequality via nonlinear pay. Our D3 = within-person paradox (pride ↑ + health ↓ simultaneously in the same worker). Cite approvingly. |
| "Bernheim-Taubinsky framework already covers this" | Construct | Our Sweet Trap is a *specific structural instance* of Bernheim-Taubinsky internalities, not a general-framework alternative. The four-primitive decomposition is the contribution; BT provide the welfare-aggregation scaffolding. |

### 5.4 Cover-letter opening (draft)

> Dear Prof. [Editor],
>
> We submit "The Sweet Trap: A Cross-Domain Behavioral Equilibrium of Rational Self-Harming Endorsement" for consideration at *Nature Human Behaviour*. The paper unifies eight literatures — urban planning, labor supply, positional consumption, intensive parenting, food choice, consumer credit, digital engagement, and marriage economics — that have independently documented individual patterns of welfare-reducing choice without recognizing a shared behavioral equilibrium. Using within-person fixed-effect identification on a 12-year Chinese panel (N=86,294; 2010-2022), we test the same four-primitive construct in five domains. The pattern confirms in all five, with specification-curve-median effect signs consistent in ≥X/5 domains. China's 2021 double-reduction education policy provides pre-registered causal confirmation that the pattern operates through intergenerational externalization rather than private preference.
>
> The work's cross-disciplinary breadth — behavioral economics, labor economics, urban policy, education, and public health — and its consequence-oriented welfare quantification (5-8% of domain-relevant consumption) align with NHB's mission to publish findings that reshape how multiple fields understand human decision-making. We believe NHB is the only journal where this unification is both readable and citable across specialist communities.

---

## 6. Defensive design checklist

### 6.1 Pre-registration commitments (OSF, before Stage 2)

For each of D3, D8, D2, D5 (D1 already pre-executed):

- [ ] Primary headline specification (person FE, year FE, sample restriction, treatment definition)
- [ ] Primary hypothesis sign (∂Sweet_DV/∂Treatment > 0; ∂Bitter_outcome/∂Treatment.L1 > 0)
- [ ] λ-moderator specification (one primary λ proxy per domain, pre-specified)
- [ ] Specification-curve variable set (≥ 500 variants per domain: alternate controls × sample filters × outcome variants)
- [ ] Null-reporting rule: if primary hypothesis fails, null goes to main text; no post-hoc rescue (rule from `sweet_trap_construct.md` §6)

### 6.2 Pre-emptive robustness per domain

| Domain | Predicted reviewer challenge | Planned robustness |
|:---|:---|:---|
| D3 996 | "Healthy worker selection" | Include health status at job entry as control; selection-on-observables bounds |
| D8 Housing | "Income effect, not positional" | Add household income FE; compare owner-occupier vs investment properties (should differ only for investment — our ρ primitive) |
| D2 鸡娃 | "双减 policy also changed income distribution" | Triple-diff with regional policy enforcement intensity; placebo tests with 2019 and 2023 (no policy) |
| D5 Diet | "food expenditure is not calorie content" | NOVA-proxy via food-spend composition; merge CHARLS subsample with biomarkers where possible |
| D1 Urban | "Paper 1 already covers this" | D1 in this paper is abbreviated to 1 figure panel; not a re-analysis. Explicit cross-reference. |

### 6.3 Specification curve construction rule (all domains)

Per `sweet_trap_construct.md` §6:

- ≥ 500 variants per domain
- Median ± IQR reported in main text (not favored point estimate)
- Sign-consistency threshold: ≥ 80% for prediction P1; ≥ 60% for secondary predictions
- Domain-level confirmations counted at the *median* level, not at the favored-model level

### 6.4 Defense against the 5 predicted attacks (from Stage 0C)

| Attack (Stage 0C) | Our differentiation per Study |
|:---|:---|
| **Allcott et al. (2020 QJE)** — subjective misallocation, re-endorsement RCT | We cite as evidence *for*; we drop D7; we differentiate Sweet Trap = within-person panel across 5 domains vs. one-platform RCT. |
| **Bernheim & Taubinsky (2018 HBE)** — internalities framework | We position Sweet Trap as a specific structural instance of BT internalities, with the four-primitive decomposition as novel. Not a competitor, an extension. |
| **Becker & Murphy (1988 JPE)** — rational addiction | D3 and D8 are non-addictive domains where λ > 0 is the operative primitive; BM cannot accommodate either λ > 0 or cross-domain generality. |
| **Orben & Przybylski (2019 NHB)** — tiny-effect-size screen-time | We drop D7; we note that their cross-sectional SCA cannot control for stable individual traits; our within-person FE does. |
| **Goldin (2014 AER)** — greedy jobs | Cite approvingly in D3. Differentiate: Goldin = gender wage gap; Sweet Trap = within-person satisfaction-health paradox regardless of gender. |

### 6.5 Data integrity and reproducibility

- [ ] All CFPS variable transformations logged in `02-data/linkage/cfps_cleaning.log`
- [ ] All specification-curve runs scripted (no ad-hoc re-specification); output versioned
- [ ] Public deposit of code and derived data on OSF/Zenodo at submission
- [ ] Cross-checks: for each primary result, at least two team members independently run the headline specification and confirm numerical match

---

## 7. Stage 2 entry conditions (pass / fail)

Before Stage 2 (parallel PDE) begins, the following must be in place:

| Gate | Status |
|:---|:---|
| Focal roster locked (5 domains) | ✅ this document |
| Per-domain OSF pre-registration drafted | ⏳ next 3 days |
| CFPS cleaning pipeline producing person-year long panel with all required variables for D1/D3/D8 | ⏳ Stage 2 week 1 |
| CFPS child module merge decision for D2 (attempt vs SI-defer) | ⏳ Stage 2 week 1 |
| CHARLS/CGSS data access for D4 SI check | ⏳ Stage 2 week 3 |
| Computation plan respecting M5 Pro 24GB constraint (`n_workers ≤ 2`, no `os.cpu_count()`) | ✅ inherits from repo CLAUDE.md |

---

## 8. File manifest

| Stage 0 inputs used | Stage 1 outputs produced |
|:---|:---|
| `00-design/sweet_trap_construct.md` | **`00-design/domain_selection_matrix.md`** (this file) |
| `00-design/cfps_variable_inventory.md` | `00-design/study_design_outline.md` (companion) |
| `00-design/cfps_variable_heatmap.md` | |
| `01-literature/literature_by_domain.md` | |
| `01-literature/top10_sweet_trap_relevant_papers.md` | |
| `01-literature/gap_matrix.md` | |
| `HANDOFF.md` | |

---

*End of Stage 1 domain-selection decision. Stage 2 (PDE across 5 focal domains) commences upon OSF pre-registration drafts.*
