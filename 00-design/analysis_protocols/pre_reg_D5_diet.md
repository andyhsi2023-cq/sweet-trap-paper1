# OSF Pre-registration: Sweet Trap Study D5 — High-Sugar/High-Fat Diet (Boundary / β-Mechanism Illustration)

**Target OSF registry:** PAP (Pre-Analysis Plan) standard template
**Study context:** Study D5 (boundary-condition / β-mechanism illustration) of a 5-domain multi-study manuscript submitted to *Nature Human Behaviour*. Working title: "The Sweet Trap: A Cross-Domain Behavioral Equilibrium of Rational Self-Harming Endorsement."
**Parent construct document:** `sweet-trap-multidomain/00-design/sweet_trap_construct.md` v1.0
**Parent design document:** `sweet-trap-multidomain/00-design/study_design_outline.md` §5
**Registration date (planned):** 2026-04-20 (before CFPS cleaning pipeline for D5 produces first headline coefficient)
**OSF URL:** [pending deposit]

---

## 1. Study information

### 1.1 Title
Dietary Expenditure, Contemporaneous Satisfaction, and Chronic Disease Cost: A Pre-registered Within-Person Boundary Test of the Sweet Trap in a 12-Year Chinese Panel

### 1.2 Authors
- Lu An¹,²,\* (ORCID: 0009-0002-8987-7986)
- Hongyang Xi¹,²,\* (ORCID: 0009-0007-6911-2309)

¹ Department of Mammary Gland, Chongqing Health Center for Women and Children, Chongqing, China
² Department of Mammary Gland, Women and Children's Hospital of Chongqing Medical University, Chongqing, China
\* Both corresponding authors.

### 1.3 Research questions
- **RQ5.1** Does within-person lagged food-expenditure share (food / total expense) raise within-person chronic-disease incidence at a one-wave lag (long-run bitter welfare cost)?
- **RQ5.2** Does within-person contemporaneous change in food share raise life satisfaction (short-run sweet endorsement)?
- **RQ5.3** Does the satisfaction response to contemporaneous food-share change attenuate for individuals with higher health literacy (education ≥ 9 years), indicating that the endorsement is β- and information-mediated?

### 1.4 Role in the paper
D5 is explicitly pre-registered as **boundary-condition evidence**. CFPS lacks biomarkers (BMI, glucose, blood pressure) and specific food-category variables (sugar, fat, ultra-processed). `food_share` is a coarse treatment proxy. We pre-commit to two equally acceptable outcomes:
- **Confirmation:** If H5.1 and H5.2 both fire, D5 extends the construct to biology-anchored domains.
- **Null:** If H5.2 is null, D5 becomes a **boundary-condition finding** that strengthens the construct's falsifiability (reported prominently as "domain where CFPS measurement is insufficient for Sweet DV detection"). Per the urban-paper lessons, no post-hoc rescue is permitted.

---

## 2. Hypotheses (directional, single-tailed)

### H5.1 — Bitter welfare cost (chronic disease, lagged)
Within-person: `∂ qp401_{i,t} / ∂ food_share_{i,t-1} > 0`.
Directional, one-sided test at α_Bonf = 0.0125.

### H5.2 — Sweet endorsement (contemporaneous satisfaction)
Within-person: `∂ qn12012_{i,t} / ∂ Δ food_share_{i,t} > 0`, where `Δ food_share_{i,t} ≡ food_share_{i,t} - food_share_{i,t-1}`.
Operationalization: contemporaneous change in food-spending composition as a revealed-preference signal of dietary palatability shift.
Directional, one-sided test at α_Bonf = 0.0125.

### H5.3 — λ-attenuation via health literacy
Within-person: `∂² qn12012_{i,t} / ∂ Δ food_share_{i,t} ∂ low_edu_i > 0`, where `low_edu_i = 1[eduy < 9]`.
Lower-education individuals externalize long-run metabolic cost to future self (via less-informed intertemporal trade-off) and show larger contemporaneous satisfaction response to food-share shifts.
Directional, one-sided test at α_Bonf = 0.0125.

### Point predictions
- |β̂(H5.1)| in the range 0.01–0.04 p.p. per one-SD increase in lagged `food_share` (prior: small-effect diet-disease epidemiology literature, e.g., Mozaffarian 2016 JAMA).
- |β̂(H5.2)| in the range 0.02–0.08 SD of `qn12012` per one-SD `Δ food_share`. **This is the most likely null** (see §7 and §1.4).
- β̂(H5.3) > 0.5 · β̂(H5.2).

---

## 3. Design plan

### 3.1 Study type
Observational. Secondary analysis of CFPS 2010–2022 long panel. Identification is within-person fixed-effect, exploiting within-household temporal variation in food-expenditure composition.

### 3.2 Study design
- **Stage 1 (Bitter, primary evidentiary test):** `qp401` on 1-wave-lagged `food_share` with person FE + year FE.
- **Stage 2 (Sweet, contemporaneous):** `qn12012` on contemporaneous `Δ food_share` with person FE + year FE.
- **Stage 3 (λ-moderation):** interaction `Δ food_share × low_edu` in Stage 2 model.

### 3.3 Known limitations (pre-specified)
1. `food_share` measures expenditure composition, not caloric content, nutrient density, or ultra-processed classification. The treatment is coarse.
2. CFPS has no BMI, blood glucose, blood pressure, or specific food-category variables.
3. Chronic disease `qp401` is a binary self-report with 6-month recall window — may miss asymptomatic metabolic disease.
4. `food_share` movements can reflect income shocks (Engel's Law) rather than dietary composition shifts; controlling for log income partially addresses this.

### 3.4 NOVA-proxy exploration (exploratory, NOT pre-registered)
CFPS subsequent audits may reveal sub-components of food expenditure (e.g., `food_outside`, `food_staples`, `food_processed` if such sub-items exist). If so, a NOVA-style processed-food proxy will be constructed as exploratory. **Not pre-registered**; flagged explicitly in main text.

### 3.5 Timing of registration
Registration before D5 coefficients are generated. Commit hash at registration: [to be recorded at OSF deposit].

---

## 4. Sampling plan

### 4.1 Data source
Same as D3/D8/D2: CFPS 2010–2022 non-balanced long panel.
- Frozen data cut: 2026-04-17. SHA256 hash: [to be recorded].

### 4.2 Inclusion criteria
1. Adult respondent: age ≥ 18 at wave observation.
2. Valid `food` expenditure in ≥2 waves.
3. Valid `expense` (total household expenditure) in ≥2 waves, non-zero (required for share denominator).
4. Valid `qp401` (chronic disease) observation in ≥1 wave.

### 4.3 Exclusion criteria
1. `food_share > 0.8` or `food_share < 0.05` — implausible extremes (Engel coefficient outside plausible range for any developed economy).
2. Respondents with `health` observations but no `food` observations (cannot construct treatment).
3. Respondents with terminal illness diagnosis at wave 1 (their `qp401` is structurally 1 and cannot change).

### 4.4 Expected N
- Adult person-years with `food`, `expense`, `qp401` all non-missing: ~72,000.
- Balanced-at-entry (observed ≥3 waves): ~30,000, ~11,000 unique respondents.
- Lagged sample (require t and t-1 observations): ~24,000.

### 4.5 Power justification
- H5.1 with expected β̂ ≈ 0.02 p.p. per SD of lagged `food_share`, N ≈ 24,000 → ~80% power at α_Bonf = 0.0125.
- H5.2 with expected β̂ ≈ 0.05 SD of `qn12012`, N ≈ 24,000 → ~75% power at α_Bonf. The power margin is narrow, reflecting the coarseness of the treatment; this is part of the boundary-condition framing.
- H5.3 (interaction, low-edu subgroup ~40%) → ~70% power at α_Bonf.

---

## 5. Variables

### 5.1 Dependent variables
| Role | Variable | CFPS name | Scale | Expected N |
|:---|:---|:---|:---|---:|
| Sweet DV (primary) | Life satisfaction | `qn12012` | Likert 1–5 | 84,328 |
| Sweet DV (secondary) | Future confidence | `qn12016` | Likert 1–5 | 84,110 |
| Bitter outcome (primary) | Chronic disease past 6 months | `qp401` | Binary 0/1 | 84,351 |
| Bitter outcome (secondary) | Self-rated health reversed | `unhealth` | 1–5 | 85,948 |
| Bitter outcome (financial) | Log medical expenditure | `log(mexp)` | Continuous | 85,401 |

### 5.2 Primary treatment
- **Stage 1 (Bitter):** `food_share_{i,t-1} = food_{i,t-1} / expense_{i,t-1}` — one-wave-lagged food expenditure share.
- **Stage 2 (Sweet):** `Δ food_share_{i,t} = food_share_{i,t} - food_share_{i,t-1}` — contemporaneous first-difference as revealed-preference proxy.

### 5.3 Secondary treatment
- `log(food)` — log food expenditure level (alternative, less relative-intensity).
- `food_share` tercile indicators (non-linear check).
- `qq201` smoking behavior (additional lifestyle treatment for companion analysis; not pre-registered as primary but SCA variant).

### 5.4 Moderators (λ proxies)
- **Primary λ proxy:** `low_edu = 1[eduy < 9]` — below-9-year education indicates lower health literacy; higher λ (lack of information → externalization of long-run cost to future self as "unforeseen").
- **Secondary λ proxy:** `has_public_insurance` (constructed from `insurance` variables; details pending cleaning) — publicly insured respondents partially externalize medical cost to the health system.
- **Tertiary λ proxy:** `age ≥ 55` — older respondents have shorter horizon, externalizing long-run cost to end-of-life public welfare.

### 5.5 Controls
- `age`, `age²/100`
- `household_size`
- `log(fincome1)` — crucial to separate Engel's-Law income effect from genuine composition shift.
- `rural` (0/1)
- `marriage` status

### 5.6 Fixed effects
- Person FE (`pid`)
- Year FE (`year`)

### 5.7 Standard errors
Two-way clustered at (`pid`, `year`).

---

## 6. Analysis plan

### 6.1 Primary specification (pre-registered; H5.1)
$$
qp401_{i,t} = \alpha_i + \gamma_t + \beta_1 \cdot food\_share_{i,t-1} + X_{i,t} \cdot \phi + \varepsilon_{i,t}
$$
Linear probability model with person FE; logit variant as SCA branch.
One-sided: `H_0: β_1 ≤ 0` vs. `H_A: β_1 > 0` at α_Bonf = 0.0125.

### 6.2 Primary specification (pre-registered; H5.2)
$$
qn12012_{i,t} = \alpha_i + \gamma_t + \beta_2 \cdot \Delta food\_share_{i,t} + X_{i,t} \cdot \phi + \varepsilon_{i,t}
$$
One-sided: `H_0: β_2 ≤ 0` vs. `H_A: β_2 > 0` at α_Bonf = 0.0125.

### 6.3 Moderator specification (pre-registered; H5.3)
$$
qn12012_{i,t} = \alpha_i + \gamma_t + \beta_2 \cdot \Delta food\_share_{i,t} + \beta_3 \cdot (\Delta food\_share_{i,t} \times low\_edu_i) + X \cdot \phi + \varepsilon
$$
One-sided: `H_0: β_3 ≤ 0` vs. `H_A: β_3 > 0` at α_Bonf = 0.0125.

### 6.4 Secondary specifications (pre-registered)
- Treatment alternate: `log(food)` level (not share) — addresses composition-vs-income concern.
- Sweet DV alternate: `qn12016` future confidence.
- Bitter outcome alternate: `unhealth` continuous; `log(mexp)` — financial cost of Bitter.
- Sample alternate: balanced-at-entry; age-restricted (25–60).
- Control variation: include/exclude `log(fincome1)` to assess sensitivity to income channel.

### 6.5 Specification curve (pre-registered)
≥500 variants combinatorially over:
- 3 treatment definitions (`food_share.L1`, `log(food).L1`, `food_share` tercile indicators)
- 2 Sweet DVs (`qn12012`, `qn12016`)
- 3 Bitter outcomes (`qp401`, `unhealth`, `log(mexp)`)
- 4 sample filters (all adults, balanced-3+, age 25–60, urban only)
- 3 control sets (minimal, standard §5.5, extended with `smoking qq201`)
- 3 FE structures (person+year, household+year, person+year+province)
- 2 cluster levels
- 3 λ proxies

Median ± IQR reported. Sign-consistency threshold: ≥80% for H5.1; ≥60% for H5.2 (explicitly lower threshold reflecting boundary-condition status); ≥60% for H5.3.

### 6.6 Robustness (pre-registered)
- Healthy-baseline restriction: exclude respondents with `qp401 = 1` in their first observed wave (selection check).
- Winsorization sensitivity: 1/99 vs. 5/95 percentile.
- Income-heterogeneity: split by `fincome1` tercile; if Engel mechanics dominate, low-income tercile should show Δ food_share response purely mechanical.
- Smoking add-on: include `qq201` as companion lifestyle treatment in SCA.

### 6.7 Exploratory (NOT pre-registered; flagged)
- NOVA-style processed-food proxy (pending food-sub-component availability).
- External data merge with CHARLS subsample for biomarker validation (noted in construct paper §6.2).
- Triple interactions (e.g., `Δ food_share × low_edu × age`).

---

## 7. Decision rules

### 7.1 Confirmation conditions
- **H5.1 confirmed:** β̂₁ > 0 with one-sided p < 0.0125 AND SCA median positive ≥80% sign consistency.
- **H5.2 confirmed:** β̂₂ > 0 with one-sided p < 0.0125 AND SCA median positive ≥60% sign consistency.
- **H5.3 confirmed:** β̂₃ > 0 with one-sided p < 0.0125 AND SCA median positive ≥60% sign consistency.

### 7.2 Null / falsification handling (F1 rule; explicitly pre-committed)

**This is the domain where null reporting is most likely and most informative.** Per construct §6 and the urban paper's lessons:

- **If H5.1 confirmed but H5.2 null or negative** (most likely scenario a priori): Report as **boundary-condition evidence**. D5 establishes the Bitter pillar but the Sweet pillar is not detectable with CFPS food-expenditure data. Main-text framing: "The Sweet Trap's Bitter pillar extends to the biology-anchored food domain, while the Sweet pillar is not detectable with expenditure-composition data — a measurement boundary that strengthens construct falsifiability by ruling out tautological confirmation." D5 retains its Figure 2 panel as a null-Sweet / positive-Bitter domain.

- **If H5.2 confirmed but H5.1 null:** Sweet without Bitter — not a Sweet Trap for D5. Reframe as "food-expenditure shifts raise satisfaction without detectable long-run chronic disease consequence in CFPS measurement." D5 moves to SI.

- **If both H5.1 and H5.2 null:** Domain does not support Sweet Trap at any level. Reported honestly in main text as "D5 does not show the pattern within CFPS measurement." Construct is not damaged: the paper pre-commits to D5 as the riskiest domain for falsification (§1.4).

- **If both H5.1 and H5.2 confirmed but H5.3 null:** Pair confirmed; λ-mediation via education is absent. Mechanism claim weakens at the λ leg; construct-at-pair-level still supported. Report as "construct confirmed, β/ρ-dominated (not λ-dominated) in the diet domain" — consistent with the paper's construct-level prediction (P3 in `sweet_trap_construct.md`) that D5 is β-dominant.

### 7.3 Explicit anti-rescue commitment
Per construct paper §6 (Flaw 3 from urban paper): no post-hoc rescue of a null H5.2 is permitted. Specifically prohibited:
- Redefining `Δ food_share` as quartile-indicator or log-diff after seeing null.
- Sub-sample restriction to specific age bins after seeing null.
- Switching to a non-pre-registered Sweet DV after seeing null.
- Adding a three-way interaction to rescue the pattern.

### 7.4 Re-analysis triggers (allowed)
- CFPS `food` variable harmonization issues across waves → rerun with wave-harmonized measure.
- Non-convergence → dummy LSDV fallback.
- Evidence of `food` measurement units shifting across waves → document and winsorize.

### 7.5 Re-analysis prohibitions
- Switching from one-sided to two-sided post hoc.
- Changing the `food_share` definition after seeing results.
- Changing `low_edu` threshold from 9 years after seeing results.
- Dropping the "revealed-preference" framing of Δ food_share to adopt a different (more favorable) operationalization after seeing null.

---

## 8. Multiple comparisons

### 8.1 Within-domain
- D5 pre-registers three primary hypotheses (H5.1, H5.2, H5.3).
- Holm-Bonferroni within D5: α_within = 0.05/3 = 0.0167.

### 8.2 Cross-domain (primary correction)
- Four pre-registered primary hypotheses across D3, D8, D2, D5 → **α_Bonf = 0.05 / 4 = 0.0125**.
- Primary confirmation threshold for H5.1, H5.2, H5.3: one-sided p < 0.0125.

### 8.3 Power implications — **narrowest of the four domains**
- H5.1: power ~80% at α_Bonf.
- H5.2: power ~75% at α_Bonf; if null at p < 0.0125 but positive at p < 0.05, reported as "directionally consistent, under-powered at the cross-domain threshold" — but the main message is that D5 is the boundary domain where this outcome is pre-committed as informative.
- H5.3: power ~70% at α_Bonf.

The power margin is narrow by design. D5's role in the paper is to provide a domain where null is plausible and informative; pre-registration at α_Bonf is deliberately stringent to prevent weak-positive results from being mis-interpreted as strong Sweet Trap confirmation.

### 8.4 Secondary and exploratory
FDR correction (Benjamini-Hochberg) for non-primary contrasts (SCA variants, secondary DVs, NOVA proxy, smoking add-on). Reported q-values alongside p-values.

---

## 9. Deviations handling

### 9.1 Anticipated deviation risks

| Risk | Likelihood | Handling |
|:---|:---:|:---|
| `food_share` measurement too coarse to detect H5.2 | **HIGH** (pre-committed as most likely null) | Report null honestly per §7.2. Not a deviation. |
| `insurance` variable structure unclear for `has_public_insurance` λ proxy | Medium | Fallback to `low_edu` as primary λ proxy (already pre-specified as primary). |
| `food` includes dining-out which may correlate with income shocks | High | Pre-specified control for `log(fincome1)`; SCA includes `food` decomposition if sub-items available. |
| `qp401` binary with high variance | Medium | LPM with linear transformation; logit as SCA variant. |
| Food-category sub-items not available for NOVA proxy | High | NOVA proxy moves to SI; not a deviation. |

### 9.2 Protocol deviation reporting
Any deviation from §5–§6 affecting primary results must be:
1. Documented in `03-analysis/logs/d5_deviations.log` with timestamp + rationale.
2. Reported in main text with explicit flag.
3. Both pre-registered and deviated results reported side-by-side.

### 9.3 Non-deviations
- Invoking null-reporting path per §7.2.
- Moving NOVA-style proxy to SI if food sub-components unavailable.
- Fallback from `has_public_insurance` to `low_edu` as primary λ (both pre-specified).

### 9.4 Explicitly prohibited (would count as protocol deviation requiring disclosure)
- Redefining `Δ food_share` to first-month-change or any non-wave-to-wave difference after seeing null.
- Switching primary Sweet DV from `qn12012` to `qn12016` after seeing null.
- Post-hoc restriction to specific food categories to achieve significance.

---

## 10. Data and code availability

### 10.1 Data
- CFPS public via ISSS, Peking University.
- Derived panel deposited at OSF at submission.
- Optional CHARLS external validation subsample (SI §D, Sweet Trap construct paper §6.2): separate pre-registration addendum if pursued.

### 10.2 Code
- D5 scripts: `03-analysis/scripts/d5_*.py` and `.R`.
- SCA engine: `03-analysis/spec-curve/d5/`.
- Deposited OSF + GitHub at submission; public at acceptance.

### 10.3 Pre-registration timing
Registered **before** D5 coefficients generated. Commit hash at registration: [to be recorded at OSF deposit].

---

## 11. Conflict of interest
None.

---

## 12. Cross-reference

Companion pre-registrations (same paper):
- `pre_reg_D3_996.md` — Headline; overwork.
- `pre_reg_D8_housing.md` — Second headline; mortgage burden.
- `pre_reg_D2_education.md` — Policy-shocked; parenting + 双减 DID.
- **`pre_reg_D5_diet.md` — this document.**
- Cross-reference overview: `README.md` in this directory.

D1 (urban over-investment) uses the prior OSF registration from the `infra-growth-mismatch` paper.

---

**Sign-off:**
Lu An, 2026-04-20 (to be dated at OSF deposit)
Hongyang Xi, 2026-04-20 (to be dated at OSF deposit)

**OSF Deposit URL:** [pending deposit]
