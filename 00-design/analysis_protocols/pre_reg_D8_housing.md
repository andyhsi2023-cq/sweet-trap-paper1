# OSF Pre-registration: Sweet Trap Study D8 — Premium Housing / Status Goods

**Target OSF registry:** PAP (Pre-Analysis Plan) standard template
**Study context:** Study D8 (second headline / positional-goods anchor) of a 5-domain multi-study manuscript submitted to *Nature Human Behaviour*. Working title: "The Sweet Trap: A Cross-Domain Behavioral Equilibrium of Rational Self-Harming Endorsement."
**Parent construct document:** `sweet-trap-multidomain/00-design/sweet_trap_construct.md` v1.0
**Parent design document:** `sweet-trap-multidomain/00-design/study_design_outline.md` §3
**Registration date (planned):** 2026-04-20 (before CFPS cleaning pipeline for D8 produces first headline coefficient)
**OSF URL:** [pending deposit]

---

## 1. Study information

### 1.1 Title
Mortgage Burden, Status Endorsement, and Savings Crowd-Out: A Pre-registered Within-Person Test of the Positional Sweet Trap in Chinese Households, 2010–2022

### 1.2 Authors
- Lu An¹,²,\* (ORCID: 0009-0002-8987-7986)
- Hongyang Xi¹,²,\* (ORCID: 0009-0007-6911-2309)

¹ Department of Mammary Gland, Chongqing Health Center for Women and Children, Chongqing, China
² Department of Mammary Gland, Women and Children's Hospital of Chongqing Medical University, Chongqing, China
\* Both corresponding authors.

### 1.3 Research questions
- **RQ8.1** Does within-person mortgage burden (ratio of mortgage payment to household income) raise self-rated social status contemporaneously?
- **RQ8.2** Does the same increase in mortgage burden reduce within-person household liquid savings at a one-wave (≈2-year) lag?
- **RQ8.3** Does the contemporaneous status response to mortgage burden intensify among younger cohorts (age < 40) who face longer horizons for λ externalization onto future self?

---

## 2. Hypotheses (directional, single-tailed)

### H8.1 — Sweet endorsement (status, P1 of construct)
Within-person: `∂ dw_{i,t} / ∂ mortgage_burden_{i,t} > 0`, where `dw` is self-rated social status on a 1–5 Likert scale.
Directional, one-sided test at α_Bonf = 0.0125 (cross-domain correction; see §8).

### H8.2 — Bitter welfare cost (savings, lagged)
Within-person: `∂ log(savings)_{i,t} / ∂ mortgage_burden_{i,t-1} < 0`.
Directional, one-sided test at α_Bonf = 0.0125.

### H8.3 — λ-heterogeneity by age cohort (P2 of construct)
Within-person: `∂² dw / ∂ mortgage_burden ∂ lambda_young > 0`, where `lambda_young = 1[age < 40]`.
Younger cohorts externalize debt-service burden to future self over a longer horizon and thus exhibit larger contemporaneous status gain per unit mortgage burden.
Directional, one-sided test at α_Bonf = 0.0125.

### H8.4 — Positional validity check (distinguish from income)
When `log(fincome1)` and `log(total_asset)` are added as controls, the primary coefficient β̂₁ in H8.1 should retain ≥50% of its uncontrolled magnitude and remain significant (one-sided p < 0.05).
This is a **discriminant hypothesis**: if β̂₁ collapses to zero when income/wealth are controlled, the phenomenon is income-driven, not positional, and D8 is reframed.

### Point predictions
- |β̂(H8.1)| in the range 0.05–0.15 SD of `dw` per unit of `mortgage_burden` (prior: Luttmer 2005 QJE neighbor-income effect; Fang et al. 2016 AER).
- |β̂(H8.2)| in the range −0.1 to −0.3 log-points per one-SD increase in lagged `mortgage_burden` (standard crowding-out elasticity).
- β̂(H8.3) > 0.5 · β̂(H8.1).

---

## 3. Design plan

### 3.1 Study type
Observational, quasi-experimental. Secondary analysis of CFPS 2010–2022 long panel. Identification is within-person fixed-effect, exploiting within-household temporal variation in mortgage burden across waves in a period that spans the Chinese housing boom and its cooling.

### 3.2 Study design
Two-stage within-person panel model:
- **Stage 1 (Sweet, status):** `dw` regressed on contemporaneous `mortgage_burden` with person FE + year FE.
- **Stage 2 (Bitter, savings):** `log(savings)` regressed on 1-wave-lagged `mortgage_burden` with person FE + year FE.
- **Stage 3 (λ-moderation):** interaction of `mortgage_burden × age_young` in the Stage 1 model.
- **Stage 4 (positional check):** Stage 1 model plus `log(fincome1)` and `log(total_asset)` controls.

### 3.3 Timing of registration
Before the cleaning pipeline for D8 produces headline coefficients. Commit hash at registration: [to be recorded at OSF deposit].

---

## 4. Sampling plan

### 4.1 Data source
Same as D3: CFPS 2010–2022 non-balanced long panel at `/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/2010-2022cfps非平衡面板数据(stata_推荐使用）.dta`.
- Frozen data cut: 2026-04-17. SHA256 hash: [to be recorded].

### 4.2 Inclusion criteria
1. Urban household resident (`urban == 1` in at least one observation).
2. Valid `resivalue` (current residence value) in ≥1 wave, indicating a housing observation exists.
3. Valid `fincome1` (household income) in ≥2 waves for within-person identification.
4. Age 18–75 at wave observation.

### 4.3 Exclusion criteria
1. Zero observations of `mortage` across all waves AND zero `h_loan` (completely unmortgaged households at all times) — no treatment variation.
2. Extreme `mortgage_burden` values > 5 (mortgage payment more than 5× annual income — data error or severe outlier).
3. Households with structural ownership change (sold all real estate mid-panel without replacing) — these confound the interpretation.

### 4.4 Expected N
- Urban-resident person-years with `resivalue` observation: ~60,000.
- Homeowner subsample with `mortage` > 0 in at least one wave: ~45,000 person-years.
- Balanced-at-entry subsample (observed ≥3 waves): ~28,000.
- Expected N is data-determined.

### 4.5 Power justification
With clustered SE on `pid` and expected ICC ≈ 0.4 for `dw`, N ≈ 28,000 balanced-at-entry person-years yields >90% one-sided power to detect |β̂(H8.1)| ≥ 0.05 SD at α_Bonf = 0.0125.

---

## 5. Variables

### 5.1 Dependent variables
| Role | Variable | CFPS name | Scale | Expected N |
|:---|:---|:---|:---|---:|
| Sweet DV (primary) | Self-rated social status | `dw` | Likert 1–5 (5 = highest) | 83,991 |
| Sweet DV (secondary) | Life satisfaction | `qn12012` | Likert 1–5 | 84,328 |
| Bitter outcome (primary) | Log household liquid savings | `log(savings)` | Continuous (post-winsorization) | 85,983 |
| Bitter outcome (secondary) | House debts balance | `house_debts` | Continuous CNY | 85,287 |
| Bitter outcome (tertiary, D6 absorption) | Non-housing debts / income | `nonhousing_debts / fincome1` | Ratio | 73,000 |

### 5.2 Primary treatment
`mortgage_burden_{i,t} = mortage_{i,t} / fincome1_{i,t}` — ratio of annual mortgage payment to household income. Winsorized at 1st/99th percentiles within wave.

### 5.3 Secondary/robustness treatment
- `resivalue_pctl_{c,t}` — house value percentile rank within city × year (positional, relative).
- `log(house_debts)` — alternative treatment via total mortgage debt level.

### 5.4 Moderators (λ proxies)
- **Primary λ proxy:** `lambda_young = 1[age < 40]` — younger cohorts externalize debt-service to future self.
- **Secondary λ proxy:** `sole_debtor = 1[h_loan == 1 AND married == 0]` — non-shared debt implies higher personal λ exposure (lower ability to externalize to co-signer).
- **Tertiary:** `has_adult_child` — bequest motive reduces λ externalization (housing becomes bequest, cost internalized).

### 5.5 Controls
- `age`, `age²/100` (for within-person age-profile; person FE absorbs stable component).
- `household_size`
- `eduy` (time-invariant; used only in subgroup analyses).
- `log(fincome1)` (used in H8.4 positional check; NOT in primary spec to preserve within-person variation attributable to treatment).
- `log(total_asset)` (used in H8.4 only).

### 5.6 Fixed effects
- Person FE (`pid`)
- Year FE (`year`)
- Robustness: household FE (`fid*`) as alternative.

### 5.7 Standard errors
Two-way clustered at (`pid`, `year`). Robustness: household-clustered; wild-cluster bootstrap.

---

## 6. Analysis plan

### 6.1 Primary specification (pre-registered; H8.1)
$$
dw_{i,t} = \alpha_i + \gamma_t + \beta_1 \cdot mortgage\_burden_{i,t} + X_{i,t} \cdot \phi + \varepsilon_{i,t}
$$
- One-sided test: `H_0: β_1 ≤ 0` vs. `H_A: β_1 > 0` at α_Bonf = 0.0125.

### 6.2 Primary specification (pre-registered; H8.2)
$$
\log(savings)_{i,t} = \alpha_i + \gamma_t + \beta_2 \cdot mortgage\_burden_{i,t-1} + X_{i,t} \cdot \phi + \varepsilon_{i,t}
$$
- One-sided test: `H_0: β_2 ≥ 0` vs. `H_A: β_2 < 0` at α_Bonf = 0.0125.

### 6.3 Moderator specification (pre-registered; H8.3)
$$
dw_{i,t} = \alpha_i + \gamma_t + \beta_1 \cdot mortgage\_burden_{i,t} + \beta_3 \cdot (mortgage\_burden_{i,t} \times lambda\_young_i) + X \cdot \phi + \varepsilon
$$
- One-sided test: `H_0: β_3 ≤ 0` vs. `H_A: β_3 > 0` at α_Bonf = 0.0125.
- Note: `lambda_young` is time-varying (age crosses 40 during panel for some individuals); interaction identification uses within-person variation in both treatment and moderator.

### 6.4 Positional validity (pre-registered; H8.4)
$$
dw_{i,t} = \alpha_i + \gamma_t + \beta_1^{\text{pos}} \cdot mortgage\_burden_{i,t} + \phi_1 \log(fincome1)_{i,t} + \phi_2 \log(total\_asset)_{i,t} + X \cdot \phi + \varepsilon
$$
- Confirmation requires β̂₁^pos ≥ 0.5 · β̂₁ (from §6.1) AND one-sided p < 0.05.
- If β̂₁^pos < 0.5 · β̂₁ or p ≥ 0.05, the positional interpretation is **not confirmed**; domain reframed as income-driven.

### 6.5 Secondary specifications (pre-registered)
- Treatment: `resivalue_pctl` (within-city-year percentile rank).
- Sweet DV alternate: `qn12012` life satisfaction.
- Bitter outcome alternate: `house_debts` level; `nonhousing_debts/fincome1` (D6-absorption secondary).
- Sample: balanced-at-entry; homeowner-only.

### 6.6 Specification curve (pre-registered)
≥500 variants combinatorially over:
- 3 treatment definitions (`mortgage_burden`, `log(house_debts)`, `resivalue_pctl`)
- 2 Sweet DVs (`dw`, `qn12012`)
- 3 Bitter outcomes (`log(savings)`, `log(house_debts)`, `nonhousing_debts/income`)
- 4 sample filters (all urban, homeowner-only, balanced-3+, urban × age < 55)
- 3 control sets
- 3 FE structures (person+year, household+year, person+year+city-FE)
- 2 cluster levels
- 3 λ proxies (`lambda_young`, `sole_debtor`, `has_adult_child`)

Median ± IQR reported. Sign-consistency threshold: ≥80% in predicted direction for H8.1, H8.2; ≥60% for H8.3.

### 6.7 Robustness (pre-registered)
- Owner-occupier vs. investment-property split: if positional/status channel is the mechanism, the `dw` response should be similar for both (pure status); if income-effect, owner-occupied should dominate. Informative for H8.4.
- 2010–2015 vs. 2016–2022 sub-period split (housing-boom vs. cooling era).
- Province-heterogeneity via province FE.

### 6.8 Exploratory (NOT pre-registered)
- Triple interactions (`mortgage_burden × age × gender`).
- Urban-tier heterogeneity (Tier 1 vs. Tier 2 vs. Tier 3 cities) using external city classification.
- Post-2021 housing-policy shock (State Council "3 red lines"): tentative DID at regional developer-exposure level. Flagged exploratory.

---

## 7. Decision rules

### 7.1 Confirmation conditions
- **H8.1 confirmed:** β̂₁ > 0 with one-sided p < 0.0125 AND SCA median positive ≥80% sign consistency.
- **H8.2 confirmed:** β̂₂ < 0 with one-sided p < 0.0125 AND SCA median negative ≥80% sign consistency.
- **H8.3 confirmed:** β̂₃ > 0 with one-sided p < 0.0125 AND SCA median positive ≥60% sign consistency.
- **H8.4 confirmed (positional validity):** β̂₁^pos ≥ 0.5 · β̂₁ AND one-sided p < 0.05.

### 7.2 Null / falsification handling (F1/F2 rules, construct §1.4)
- **If H8.1 null or opposite-signed** at α=0.05 (95% one-sided CI includes 0 or excludes positive): D8 fails the Sweet pillar (F1). D8 treated as boundary-condition evidence; null reported in main text without post-hoc rescue; domain exits second-headline role for abstract.
- **If H8.1 confirmed but H8.2 null or positive:** Sweet without Bitter = not a Sweet Trap. Report as counterexample; reframe D8 as "status good with no detectable savings crowd-out" — this weakens the Sweet Trap claim for D8 but does not falsify the construct if other domains confirm.
- **If H8.4 fails (positional collapses to income):** downgrade D8 interpretation from "positional Sweet Trap" to "income-driven status signaling"; D8 remains in main text with explicit reframing.
- **If H8.1 and H8.2 both confirmed but H8.3 null:** the λ-channel is not age-mediated; pattern holds but cohort-externalization mechanism weakened. Report as "pair confirmed, λ-mediation indeterminate."

### 7.3 Re-analysis triggers (allowed without deviation)
- `mortage` missing rate spikes for specific waves (e.g., 2010 and 2012 have N < 20K for `mortage`) → rerun with wave-specific flagging.
- `savings` winsorization threshold sensitivity check.
- Non-convergence of person FE → dummy-variable least squares fallback.

### 7.4 Re-analysis prohibitions
- Switching from one-sided to two-sided after seeing results.
- Dropping the positional-validity check H8.4 to preserve the primary result.
- Changing mortgage-burden threshold or winsorization after seeing results.
- Swapping `dw` for `qn12012` as primary Sweet DV after seeing results.

---

## 8. Multiple comparisons

### 8.1 Within-domain
- D8 pre-registers four hypotheses (H8.1–H8.4). H8.4 is a discriminant check on H8.1, not a separate outcome test; it is not included in the Bonferroni count.
- Three primary outcome tests (H8.1, H8.2, H8.3) with Holm-Bonferroni within D8.

### 8.2 Cross-domain (primary correction)
- Four pre-registered primary hypotheses across the 4 new focal domains → **α_Bonf = 0.05 / 4 = 0.0125**.
- Primary confirmation threshold for H8.1, H8.2, H8.3: one-sided p < 0.0125.
- H8.4 (positional discriminant) uses α=0.05 because it is a sanity check, not an outcome hypothesis.

### 8.3 Power implications
- H8.1 with α_Bonf = 0.0125 and expected |β̂| ≈ 0.08 SD, N ≈ 28,000 → >90% power.
- H8.2 with expected β̂ ≈ −0.15 log-points, N ≈ 25,000 (lagged sample shrinks) → ~85% power.
- H8.3 interaction with expected magnitude 0.5·β̂₁, subsample imbalance (age<40 ≈ 40% of sample) → ~75% power; underpowered region flagged as "directionally consistent, under-powered" if p ∈ [0.0125, 0.05].

### 8.4 Secondary and exploratory
FDR correction (Benjamini-Hochberg) applied to all non-primary contrasts (SCA variants, secondary DVs, robustness tests). Reported q-values alongside p-values.

---

## 9. Deviations handling

### 9.1 Anticipated deviation risks

| Risk | Likelihood | Handling |
|:---|:---:|:---|
| `mortage` N sparse in early waves (2010, 2012) | High (observed N < 20K for those years) | Use post-2014 waves as primary DID-free window for H8.1; early waves as robustness. Flag in main text if invoked. |
| `dw` missingness in specific waves | Low (N = 83,991; missing 2.7%) | Ignore; robust to attrition weights in SCA. |
| `savings` distribution heavily skewed with zeros | Medium | Log-transform after adding 1; robustness: inverse hyperbolic sine transformation. |
| `total_asset` missing for >5% of sample | Low | H8.4 positional-validity check runs on available subsample; sample-size reduction acceptable. |
| `mortgage_burden` > 5 outliers | Low | Pre-specified winsorization at 1/99 percentile. |

### 9.2 Protocol deviation reporting
Any deviation from §5–§6 that affects primary H8.1–H8.3 results must be:
1. Documented in `03-analysis/logs/d8_deviations.log` with timestamp + rationale.
2. Reported in main text with explicit "deviation from pre-registration" flag.
3. Both pre-registered and deviated results reported side-by-side.

### 9.3 Non-deviations
- Choice of display format (coefplot vs. forest).
- Bootstrap replications (default 1,000).
- Winsorization at 1/99th percentile of `mortgage_burden` and `savings`.

---

## 10. Data and code availability

### 10.1 Data
- CFPS public via ISSS, Peking University (application required).
- Derived analytic panel deposited at OSF at submission; codebook included.
- Raw file: `/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/`.

### 10.2 Code
- All D8 scripts: `03-analysis/scripts/d8_*.py` and `.R`.
- SCA engine: `03-analysis/spec-curve/d8/`.
- Deposited at OSF + GitHub at submission; public at acceptance.

### 10.3 Pre-registration timing
This document registered **before** D8 headline coefficient generated. Commit hash at registration: [to be recorded at OSF deposit].

---

## 11. Conflict of interest
None.

---

## 12. Cross-reference

Companion pre-registrations (same paper):
- `pre_reg_D3_996.md` — Headline; overwork.
- **`pre_reg_D8_housing.md` — this document.**
- `pre_reg_D2_education.md` — Policy-shocked; parenting + 双减 DID.
- `pre_reg_D5_diet.md` — Boundary; food expenditure.
- Cross-reference overview: `README.md` in this directory.

D1 (urban over-investment) uses the prior OSF registration from the `infra-growth-mismatch` paper.

---

**Sign-off:**
Lu An, 2026-04-20 (to be dated at OSF deposit)
Hongyang Xi, 2026-04-20 (to be dated at OSF deposit)

**OSF Deposit URL:** [pending deposit]
