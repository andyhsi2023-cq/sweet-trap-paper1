# OSF Pre-registration: Sweet Trap Study D3 — 996 Overwork (HEADLINE)

**Target OSF registry:** PAP (Pre-Analysis Plan) standard template
**Study context:** Study D3 (headline / abstract anchor) of a 5-domain multi-study manuscript submitted to *Nature Human Behaviour*. Working title: "The Sweet Trap: A Cross-Domain Behavioral Equilibrium of Rational Self-Harming Endorsement."
**Parent construct document:** `sweet-trap-multidomain/00-design/sweet_trap_construct.md` v1.0
**Parent design document:** `sweet-trap-multidomain/00-design/study_design_outline.md` §2
**Registration date (planned):** 2026-04-20 (before CFPS cleaning pipeline for D3 produces first headline coefficient)
**OSF URL:** [pending deposit]

---

## 1. Study information

### 1.1 Title
Within-Person Paradox of Overwork Endorsement and Health Cost: A Pre-registered Test of the Sweet Trap in a 12-Year Chinese Labor Panel

### 1.2 Authors
- Lu An¹,²,\* (ORCID: 0009-0002-8987-7986)
- Hongyang Xi¹,²,\* (ORCID: 0009-0007-6911-2309)

¹ Department of Mammary Gland, Chongqing Health Center for Women and Children, Chongqing, China
² Department of Mammary Gland, Women and Children's Hospital of Chongqing Medical University, Chongqing, China
\* Both corresponding authors.

### 1.3 Research questions
- **RQ3.1** Does weekly work hours above the statutory overtime threshold (>48h) raise within-person job satisfaction contemporaneously in the Chinese working-age population?
- **RQ3.2** Does the same increase in weekly work hours raise within-person incidence of chronic disease at a one-wave (≈2-year) lag?
- **RQ3.3** Does the contemporaneous satisfaction response to overtime intensify for workers whose family composition implies high externalization capacity (spouse + dependent children present)?

---

## 2. Hypotheses (directional, single-tailed)

### H3.1 — Sweet endorsement (P1 of construct)
Within-person: `∂ qg406_{i,t} / ∂ overtime_d_{i,t} > 0`.
Directional, one-sided test at α = 0.05 uncorrected; α_Bonf = 0.0125 after cross-domain correction (see §8).

### H3.2 — Bitter welfare cost (P1 complement, lagged)
Within-person: `∂ qp401_{i,t} / ∂ overtime_d_{i,t-1} > 0`.
Directional, one-sided test. One-wave lag (≈2 years) is the identifying timing assumption; shorter lags contaminated by reverse causation (sickness reduces work hours).

### H3.3 — λ-heterogeneity (P2 of construct)
Within-person: `∂² qg406_{i,t} / ∂ overtime_d_{i,t} ∂ λ_i > 0`, where `λ_i ≡ 1[spouse present × dependent-child present]`.
Directional, one-sided test. Workers who can externalize caregiving cost show larger Sweet endorsement.

### Point predictions
- |β̂(H3.1)| in the range 0.05–0.20 SD of `qg406` (prior: Goldin 2014 AER, Pencavel 2015 EJ cross-sectional estimates).
- |β̂(H3.2)| in the range 0.01–0.05 p.p. per overtime-indicator-unit per year lag (prior: Kivimäki et al. 2015 Lancet meta-analysis dose-response).
- β̂(H3.3) > 0.5 · β̂(H3.1) (interaction magnitude ~50% of baseline slope).

---

## 3. Design plan

### 3.1 Study type
Observational, quasi-experimental. Secondary analysis of the China Family Panel Studies (CFPS) 2010, 2012, 2014, 2016, 2018, 2020, 2022 waves. Identification is within-person fixed-effect, exploiting temporal variation in self-reported weekly work hours across waves for the same individual.

### 3.2 Study design
Two-stage within-person panel model:
- **Stage 1 (Sweet):** `qg406` regressed on contemporaneous `overtime_d` with person FE + year FE.
- **Stage 2 (Bitter):** `qp401` regressed on 1-wave-lagged `overtime_d` with person FE + year FE.

No manipulation. Temporal variation in work hours is exogenous to the fixed individual characteristics absorbed by person FE. Conditional on person FE and year FE, the remaining variation is interpreted as within-person movement along the overwork margin.

### 3.3 Timing of registration
Registration occurs **before** the cleaning pipeline for D3 produces headline coefficients. The current repository (commit hash to be recorded at deposit) contains no D3 headline results.

---

## 4. Sampling plan

### 4.1 Data source
- CFPS 2010-2022 non-balanced long panel.
- File: `/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/2010-2022cfps非平衡面板数据(stata_推荐使用）.dta`.
- Raw size: 86,294 person-years × 204 variables across 7 waves.
- Frozen data cut: 2026-04-17 snapshot; file SHA256 hash: [to be recorded at OSF deposit].

### 4.2 Inclusion criteria
1. `jobclass ∈ {employed wage earner}` (non-missing and indicating salaried employment).
2. Valid `workhour` in at least two waves (required for within-person identification).
3. Valid `qg406` overall job satisfaction observation in at least one wave paired with non-missing `workhour`.
4. Age 18–65 at wave observation.

### 4.3 Exclusion criteria
1. Self-employed, agricultural, retired, student, or unemployed in all observed waves (cannot operationalize overtime treatment).
2. Extreme `workhour` values (>100 h/week or <0) — treated as data entry error.
3. Individuals with job-class switches in every wave (cannot anchor a coherent employment state).

### 4.4 Expected N
- Overall employed person-year observations: ~41,000 (reported N for `workhour`).
- With `qg406` non-missing: ~30,000 person-years after inner join.
- Balanced-at-entry subsample (observed in ≥3 waves): ~18,000 person-years, ~7,500 unique individuals.
- Expected N is data-determined, not target-based.

### 4.5 Power justification
With two-way clustered SE on (person, year) and expected intra-class correlation ≈0.3, the design has >90% one-sided power to detect β₁ ≥ 0.05 SD at α=0.05 with N ≈ 18,000 person-years (5,000 unique workers observed in 3–7 waves). Power calculation notebook: `03-analysis/scripts/power_d3.R` [to be deposited with code].

---

## 5. Variables

### 5.1 Dependent variables
| Role | Variable | CFPS name | Scale | Expected N |
|:---|:---|:---|:---|---:|
| Sweet DV (primary) | Overall job satisfaction | `qg406` | Likert 1–5 (5 = most satisfied) | 53,015 |
| Sweet DV (secondary) | Promotion satisfaction | `qg405` | Likert 1–5 | 42,068 |
| Bitter outcome (primary) | Chronic disease past 6 months | `qp401` | Binary 0/1 | 84,351 |
| Bitter outcome (secondary) | Self-rated health (reversed) | `unhealth` | 1–5, higher = worse | 85,948 |
| Bitter outcome (mechanism) | Sleep hours | `qq4010` | Continuous h/day | 26,880 |

### 5.2 Primary treatment
`overtime_d_{i,t} = 1[workhour_{i,t} > 48]` — weekly hours above China's statutory overtime threshold. Chinese labor law specifies 40h standard week and ≤36h monthly overtime (i.e., ~48h/week cap). The 48h cutoff is a structural threshold, not a data-driven one.

### 5.3 Secondary/robustness treatment
`workhour` as continuous predictor (for specification-curve variants).

### 5.4 Moderator (λ proxy)
- **Primary λ proxy:** `lambda_family = 1[has_spouse × (child_num ≥ 1)]` — household composition implying concurrent caregiving burden that can be externalized to spouse.
- **Secondary λ proxy:** `migrant = 1[workplace city ≠ hukou city]` — migrant-separated worker bears personal cost; family bears relational separation cost.

### 5.5 Controls (covariate set X)
Common set held constant across the 5-domain paper:
- `age`, `age²/100`
- `gender` (within-household-context variable only; not absorbed by person FE because it is invariant, so used only for subgroup analyses)
- `eduy` (pre-period, time-invariant within person)
- `married` binary (used in moderator construction, not as separate control to avoid collinearity)
- `household_size`
- `log(fincome1)` (log household income, winsorized at 1st and 99th percentile)

### 5.6 Fixed effects
- Person FE (`pid`) — absorbs all time-invariant individual characteristics (gender, stable personality, hukou origin, baseline health).
- Year FE (`year`) — absorbs common shocks (macro fluctuations, policy environment).

### 5.7 Standard errors
Two-way clustered at (`pid`, `year`). Robustness: household-clustered; bootstrap with 1,000 replications (SCA variant).

---

## 6. Analysis plan

### 6.1 Primary specification (pre-registered; H3.1)
$$
qg406_{i,t} = \alpha_i + \gamma_t + \beta_1 \cdot overtime\_d_{i,t} + X_{i,t} \cdot \phi + \varepsilon_{i,t}
$$
- One-sided test: `H_0: β_1 ≤ 0` vs. `H_A: β_1 > 0` at α = 0.05 (uncorrected); α_Bonf = 0.0125 applied.

### 6.2 Primary specification (pre-registered; H3.2)
$$
qp401_{i,t} = \alpha_i + \gamma_t + \beta_2 \cdot overtime\_d_{i,t-1} + X_{i,t} \cdot \phi + \varepsilon_{i,t}
$$
- Linear probability model with person FE. Logit variant as SCA branch.
- One-sided test: `H_0: β_2 ≤ 0` vs. `H_A: β_2 > 0` at α_Bonf = 0.0125.

### 6.3 Moderator specification (pre-registered; H3.3)
$$
qg406_{i,t} = \alpha_i + \gamma_t + \beta_1 \cdot overtime\_d_{i,t} + \beta_3 \cdot (overtime\_d_{i,t} \times \lambda_i) + X \cdot \phi + \varepsilon
$$
- One-sided test: `H_0: β_3 ≤ 0` vs. `H_A: β_3 > 0` at α_Bonf = 0.0125.

### 6.4 Secondary specifications (pre-registered)
- Continuous treatment: replace `overtime_d` with `workhour` (log-linear).
- Alternate Sweet DV: `qg405` promotion satisfaction as outcome.
- Alternate Bitter outcome: `unhealth` (1–5) as OLS; `qq4010` sleep hours as mechanism check.
- Alternate sample: balanced-at-entry (observed ≥3 waves).

### 6.5 Specification curve (pre-registered; exploratory-inferential hybrid)
≥500 variants constructed combinatorially over:
- 2 treatment definitions (`overtime_d`, `log(workhour)`)
- 2 Sweet DVs (`qg406`, `qg405`)
- 3 Bitter outcomes (`qp401`, `unhealth`, `health`)
- 4 sample filters (all, balanced-3+, balanced-5+, age 25–55)
- 3 control sets (minimal, standard §5.5, extended with `industry` FE)
- 3 FE structures (person+year, person+year+industry, household+year)
- 2 cluster levels (person-year, household)
- 2 λ-proxy choices (`lambda_family`, `migrant`)

Median ± IQR reported in main text for each of H3.1, H3.2, H3.3. Sign-consistency threshold: ≥80% positive for H3.1 / H3.2; ≥60% for H3.3.

### 6.6 Robustness (pre-registered but clearly separated from primary)
- Healthy-worker-selection bounds: include `health_baseline` (first observed `health` per person) as control.
- Attrition weights: inverse-probability weighting using observed attrition patterns.
- Alternate `overtime_d` thresholds: 44h, 50h, 55h, 60h (placebo and dose-response).

### 6.7 Exploratory analyses (NOT pre-registered; flagged in main text)
- Triple interactions (e.g., `overtime × λ × gender`).
- Industry-heterogeneity beyond 2-digit aggregation.
- Post-2021 `wide-overtime enforcement` regional variation.
- Non-linear `workhour` splines.

---

## 7. Decision rules

### 7.1 Confirmation conditions
- **H3.1 confirmed:** β̂₁ > 0 with one-sided p < 0.0125 (Bonferroni-corrected) AND SCA median positive with ≥80% sign consistency.
- **H3.2 confirmed:** β̂₂ > 0 with one-sided p < 0.0125 AND SCA median positive with ≥80% sign consistency.
- **H3.3 confirmed:** β̂₃ > 0 with one-sided p < 0.0125 AND SCA median positive with ≥60% sign consistency.

### 7.2 Null / falsification handling (F1 rule, construct §1.4)
- **If H3.1 is null or opposite-signed** at α=0.05 (i.e., 95% one-sided CI includes 0 or excludes positive): domain D3 is treated as **boundary-condition evidence** consistent with the construct's F1 falsification rule. The null is reported in the main text without post-hoc rescue. D3 exits focal roster for abstract-number purposes; it remains in Figure 2 as a null panel alongside the four confirmed domains.
- **If H3.1 confirmed but H3.2 null or negative:** reframe as "Sweet without Bitter" — this falsifies the Sweet Trap interpretation for D3 (endorsement without long-run welfare cost = not a Sweet Trap). Report in main text; domain reframed as "pure Sweet" counterexample.
- **If H3.1 and H3.2 both confirmed but H3.3 null:** the λ-channel is specific to certain family compositions; Sweet Trap confirmed at the Sweet-Bitter level, λ-mediation weakened. Report as "construct-at-the-pair-level, primitive-specific λ role unclear."

### 7.3 Re-analysis triggers (allowed without protocol deviation)
- CFPS merge failure rate > 10% for any wave → rerun with flagged-wave diagnostic.
- Numerical non-convergence of person FE within-transform → switch to dummy-variable least-squares with same specification.
- Evidence of data-entry errors in `workhour` (e.g., implausible top codes) → document in cleaning log, rerun with winsorization.

### 7.4 Re-analysis prohibitions (would require protocol deviation)
- Moving from one-sided to two-sided test after seeing results.
- Adding or dropping controls ex post to achieve significance.
- Changing the 48h threshold after seeing results.
- Switching primary Sweet DV from `qg406` to any alternative after seeing results.

---

## 8. Multiple comparisons

### 8.1 Within-domain
- D3 pre-registers three hypotheses (H3.1, H3.2, H3.3).
- Holm-Bonferroni correction applied within the three D3 hypotheses: α_within_D3_H1 = 0.05/3 = 0.0167 for the most stringent first-test threshold.

### 8.2 Cross-domain (primary correction for this paper)
- The 5-domain Sweet Trap paper pre-registers primary hypotheses across D3, D8, D2, D5 (D1 re-uses the already-registered protocol from the `infra-growth-mismatch` paper).
- Four pre-registered primary hypotheses → **Bonferroni α_Bonf = 0.05 / 4 = 0.0125**.
- The primary confirmation threshold for H3.1, H3.2, H3.3 is α_Bonf = 0.0125 (one-sided).
- This is more conservative than within-domain Holm-Bonferroni; the cross-domain correction dominates.

### 8.3 Power implications
- With α_Bonf = 0.0125 one-sided and expected effect size 0.10 SD for H3.1, N ≈ 18,000 balanced-at-entry person-years retains >85% power.
- For H3.2 (p.p. coefficient on lagged treatment), expected effect 0.03 p.p., power remains >80% at α_Bonf given N ≈ 15,000 person-years with non-missing `qp401` lag.
- For H3.3 (interaction), power is ~70% at α_Bonf for expected effect size 0.5×β̂₁; this is the least powered of the three — if H3.3 returns a null at α_Bonf but is positive at α=0.05, we report as "directionally consistent, under-powered."

### 8.4 Secondary and exploratory analyses
FDR correction (Benjamini-Hochberg) applied to all non-primary contrasts (SCA variants, secondary DVs, robustness tests). Reported q-values alongside p-values.

---

## 9. Deviations handling

### 9.1 Anticipated deviation risks

| Risk | Likelihood | Handling |
|:---|:---:|:---|
| `qg406` missing rate > 40% in some waves (observed 38.5% overall) | Medium | Downgrade to `qg401` (income satisfaction, also Sweet) as primary; flag in paper as protocol deviation if invoked. |
| `qq4010` sleep N too small for robust mediation | High (already N=26,880 vs 84K+ for other outcomes) | Sleep mediation is pre-registered as mechanism-only (not confirmatory). Null sleep result does not invalidate H3.1 or H3.2. |
| `workplace` missing for >60% preventing `migrant` λ proxy | High | Primary λ proxy is `lambda_family` (N ≈ 73,000); `migrant` is secondary. Loss does not invalidate H3.3. |
| `overtime_d` distribution imbalance (e.g., <10% treated in some waves) | Low | Rerun with continuous `workhour`; report both. |

### 9.2 Protocol deviation reporting
Any deviation from §5–§6 specifications that affects primary results must be:
1. Documented in `03-analysis/logs/d3_deviations.log` with timestamp and rationale.
2. Reported in the main text with a "deviation from pre-registration" flag.
3. Both pre-registered and deviated results reported.

### 9.3 Non-deviations
The following do NOT require deviation reporting:
- Choice of point-estimate display (coefplot vs. forest plot).
- Bootstrap sample size selection for SE (default 1,000).
- Variable winsorization at 1/99th percentile (pre-specified as standard).

---

## 10. Data and code availability

### 10.1 Data
- CFPS data is publicly available from ISSS, Peking University (application required; standard terms).
- Derived analytic panel (post-cleaning) will be deposited on OSF at submission in Stata `.dta` and parquet formats, with full codebook.
- Raw file provenance: `/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/`.

### 10.2 Code
- All cleaning and analysis scripts: `03-analysis/scripts/d3_*.py` and `.R`.
- SCA engine: `03-analysis/spec-curve/d3/`.
- Deposited on OSF + GitHub at submission; made public at acceptance.

### 10.3 Pre-registration timing
This document is registered **before** the D3 analysis pipeline produces any headline coefficient. Commit hash at registration: [to be recorded at OSF deposit].

---

## 11. Conflict of interest
None. Authors declare no competing interests. No funding source influences the design or analysis.

---

## 12. Cross-reference to other pre-registrations

This D3 pre-registration is one of four that together pre-commit the Sweet Trap multi-domain paper's primary analysis:
- **D3 996 (this document)** — Headline Study; overwork → job satisfaction + chronic disease.
- `pre_reg_D8_housing.md` — Second-headline; mortgage burden → social status + savings crowd-out.
- `pre_reg_D2_education.md` — Policy-shocked; parenting spend → parental satisfaction + consumption crowd-out, with 2021 双减 DID.
- `pre_reg_D5_diet.md` — Boundary; food expenditure → chronic disease + satisfaction.
- Cross-reference overview: `README.md` in this directory.

D1 (urban over-investment) re-uses the prior OSF registration associated with the `infra-growth-mismatch` paper; no new registration for D1.

---

**Sign-off:**
Lu An, 2026-04-20 (to be dated at OSF deposit)
Hongyang Xi, 2026-04-20 (to be dated at OSF deposit)

**OSF Deposit URL:** [pending deposit]
