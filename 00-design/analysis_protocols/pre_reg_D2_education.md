# OSF Pre-registration: Sweet Trap Study D2 — Intensive Parenting (鸡娃) with 双减 2021 DID

**Target OSF registry:** PAP (Pre-Analysis Plan) standard template
**Study context:** Study D2 (maximum-novelty / policy-shocked Study) of a 5-domain multi-study manuscript submitted to *Nature Human Behaviour*. Working title: "The Sweet Trap: A Cross-Domain Behavioral Equilibrium of Rational Self-Harming Endorsement."
**Parent construct document:** `sweet-trap-multidomain/00-design/sweet_trap_construct.md` v1.0
**Parent design document:** `sweet-trap-multidomain/00-design/study_design_outline.md` §4
**Registration date (planned):** 2026-04-20 (before CFPS cleaning pipeline for D2 produces first headline coefficient; before 2021 DID event study is run)
**OSF URL:** [pending deposit]

---

## 1. Study information

### 1.1 Title
Intensive Parenting, Parental Status Endorsement, and Consumption Crowd-Out: A Pre-registered Within-Person and Difference-in-Differences Test of the Sweet Trap in Chinese Households Across the 2021 "Double Reduction" Policy Shock

### 1.2 Authors
- Lu An¹,²,\* (ORCID: 0009-0002-8987-7986)
- Hongyang Xi¹,²,\* (ORCID: 0009-0007-6911-2309)

¹ Department of Mammary Gland, Chongqing Health Center for Women and Children, Chongqing, China
² Department of Mammary Gland, Women and Children's Hospital of Chongqing Medical University, Chongqing, China
\* Both corresponding authors.

### 1.3 Research questions
- **RQ2.1** Does within-household education-expenditure share (education spending / total expenditure) raise parental life satisfaction contemporaneously?
- **RQ2.2** Does the same increase reduce within-household non-education consumption share at a one-wave lag (financial crowd-out)?
- **RQ2.3** After the July 2021 "Double Reduction" (双减) policy restricting private tutoring, do previously-high-tutoring households show a **drop** in parental satisfaction — indicating that their prior endorsement was driven by the now-removed sweet amenity (not by stable parental preferences)?

---

## 2. Hypotheses (directional, single-tailed)

### H2.1 — Sweet endorsement (parental satisfaction; P1 of construct)
Within-person: `∂ qn12012_{i,t} / ∂ eexp_share_{i,t} > 0` for households with `child_num ≥ 1`, where `eexp_share = eexp / expense`.
Directional, one-sided test at α_Bonf = 0.0125.

### H2.2 — Bitter welfare cost (consumption crowd-out, lagged)
Within-person: `∂ [(expense - eexp)/expense]_{i,t} / ∂ eexp_share_{i,t-1} < 0`.
Directional, one-sided test at α_Bonf = 0.0125.

### H2.3 — 双减 DID (λ-attenuation via policy shock; P2 of construct)
Difference-in-differences:
$$
qn12012_{i,t} = \alpha_i + \gamma_t + \delta \cdot (post2021_{t} \times high\_baseline\_tutoring_i) + X \cdot \phi + \varepsilon
$$
Directional prediction: **δ < 0**, one-sided.
If the Sweet Trap was operative pre-policy (θ-weighted endorsement of tutoring-as-status), forcible removal of the sweet amenity in 2021 should reduce the parental endorsement signal among previously-high-tutoring households relative to low-baseline households.
Directional, one-sided test at α_Bonf = 0.0125.

### H2.4 — Placebo DID (identification check)
Same DID framework with pseudo-treatment year 2019 (no policy):
$$
qn12012_{i,t} = \alpha_i + \gamma_t + \delta_{pbo} \cdot (post2019_{t} \times high\_baseline\_tutoring_i) + X \cdot \phi + \varepsilon
$$
Predicted: `δ_pbo` indistinguishable from 0 (two-sided p ≥ 0.10).
This is a **discriminant identification check**; not counted in the Bonferroni-corrected outcome tests.

### Point predictions
- |β̂(H2.1)| in the range 0.10–0.25 SD of `qn12012` per one-SD increase in `eexp_share`.
- |β̂(H2.2)| in the range −0.05 to −0.15 (share units) per one-SD lagged increase.
- |δ(H2.3)| in the range −0.15 to −0.40 SD of `qn12012` for high-baseline households post-2021.

---

## 3. Design plan

### 3.1 Study type
Observational with quasi-experimental DID component. Secondary analysis of CFPS 2010–2022 long panel. Two complementary identification strategies:
- Within-person FE (pure observational, for H2.1, H2.2).
- Difference-in-differences around July 2021 双减 policy, with pre-policy baseline tutoring intensity as group assignment (for H2.3, H2.4).

### 3.2 Study design

**Stage A — Within-person panel (for H2.1, H2.2):**
- Sample: households with `child_num ≥ 1`.
- Person FE + year FE; 2010–2022 waves.

**Stage B — 双减 DID (for H2.3, H2.4):**
- Sample: households observed in 2018 AND in ≥1 wave ∈ {2020, 2022}.
- `high_baseline_tutoring_i`: 1 if household's pre-policy (2018–2020) average `eexp_share` is in the top tercile of the pre-policy distribution; 0 if bottom two terciles. This is a **time-invariant** group assignment.
- `post2021_t`: 1 if `year ≥ 2022` (first CFPS wave fully after the July 2021 policy); 0 if `year ≤ 2020`.
- Event study: wave-by-wave differentials from 2014 through 2022, with 2020 as reference.

### 3.3 Timing of registration
Registration before D2 Stage A coefficients are generated and before the 双减 DID is run. Commit hash at registration: [to be recorded at OSF deposit].

### 3.4 Child-module merge decision (pre-specified contingency)
CFPS 2016–2022 child questionnaire contains child-level outcomes (child-reported `qp401`, `qn12012`, etc.). We will **attempt** the child-module merge in Stage 2 Week 1 of execution. Decision rule:
- **If merge succeeds** (≥70% of parent records matched to child records within household): child-level bitter-outcome analysis enters main text as H2.5 (exploratory, pre-registered-secondary).
- **If merge fails** (<70% match rate or critical variables missing): child-level analysis moves to SI §D; main-text D2 runs at parent-level only on H2.1–H2.4.
- This contingency is documented in §9; invoking the SI fallback is **not** a protocol deviation.

---

## 4. Sampling plan

### 4.1 Data source
Same as D3/D8: CFPS 2010–2022 non-balanced long panel.
- Frozen data cut: 2026-04-17. SHA256 hash: [to be recorded].
- Child-module files (if merge attempted): `CFPS 2016-2022 child questionnaire` on the same P1 disk. Path to be confirmed at Stage 2 Week 1.

### 4.2 Inclusion criteria — Stage A (within-person)
1. `child_num ≥ 1` in at least one wave (households with dependent children).
2. Valid `eexp` and `expense` observations in ≥2 waves.
3. Valid `qn12012` in ≥2 waves.
4. Respondent age 25–65 at wave observation.

### 4.3 Inclusion criteria — Stage B (DID)
1. Criteria from §4.2, plus:
2. Observed in 2018 (required for baseline group assignment).
3. Observed in ≥1 wave ∈ {2020, 2022}.
4. `eexp_share` defined (non-zero expense denominator) in 2018.

### 4.4 Exclusion criteria
1. Households with `eexp` reported but `expense` missing (cannot compute share).
2. `eexp_share` > 0.8 (implausible: education >80% of total expenditure = data error).
3. Households with child aging out (child turns 18) mid-panel: excluded from DID because their "high tutoring" baseline is non-meaningful post-aging-out.

### 4.5 Expected N
- Stage A full panel: ~50,000 person-years (households with `child_num ≥ 1`).
- Stage A balanced-at-entry: ~22,000 person-years, ~8,500 unique households.
- Stage B DID sample: ~18,000 household-year observations from ≈9,000 unique households.

### 4.6 Power justification
- Stage A (H2.1, H2.2): N ≈ 22,000 balanced yields >90% power at α_Bonf for expected β̂ ≈ 0.15 SD.
- Stage B (H2.3 DID): N ≈ 18,000 household-year with two-way clustering and expected δ ≈ −0.25 SD: ~80% power at α_Bonf = 0.0125. The interaction-treatment subgroup (high-baseline households) is ~33% of sample, reducing effective power; acceptable because effect size prior is relatively large.

---

## 5. Variables

### 5.1 Dependent variables
| Role | Variable | CFPS name | Scale | Expected N |
|:---|:---|:---|:---|---:|
| Sweet DV (primary) | Parental life satisfaction | `qn12012` | Likert 1–5 | 84,328 |
| Sweet DV (secondary, exploratory) | Trust in parents (child-reported, reversed as parent-pride proxy) | `qn10021` | Likert 1–5 | 70,707 |
| Bitter outcome (primary) | Non-education consumption share | `(expense - eexp)/expense` | Ratio | 85,594 |
| Bitter outcome (secondary, if child merge succeeds) | Child self-rated health | child `qp401` | Binary 0/1 | TBD post-merge |
| Bitter outcome (tertiary, if child merge succeeds) | Child life satisfaction | child `qn12012` | Likert 1–5 | TBD post-merge |

### 5.2 Primary treatment
`eexp_share_{i,t} = eexp_{i,t} / expense_{i,t}` — education expenditure share of total household expenditure. Winsorized at 1st/99th percentile within wave.

### 5.3 Secondary treatment
- `log(school)` — log tutoring spending (alternative narrow measure).
- `eexp_share` quartile indicators (non-linear check).

### 5.4 DID group-assignment variable
`high_baseline_tutoring_i` = 1 if household's mean `eexp_share` over 2018–2020 is in the top tercile of the pre-policy distribution (calculated on the analytic sample); 0 otherwise. **Time-invariant** by construction.

### 5.5 DID policy indicator
`post2021_t` = 1 if `year ≥ 2022`; 0 if `year ≤ 2020`. (2021 itself is not a CFPS wave.)

### 5.6 Moderators (λ proxies for Stage A)
- **Primary λ proxy:** `only_child = 1[child_num == 1]` — single-child households concentrate all externalization onto one child, raising per-child λ.
- **Secondary λ proxy:** `child_male = 1[child_gender == male]` — in Chinese context, sons historically receive higher investment intensity; gender moderation tests cultural-specific externalization.
- **Tertiary:** parent `eduy ≥ 12` × `occupation` — higher-SES parents have more external bequest capacity.

### 5.7 Controls
- `age`, `age²/100` of respondent
- `household_size`
- `log(fincome1)` (log household income)
- `rural` (0/1 urban-rural indicator; partially absorbed by person FE for non-migrators)

### 5.8 Fixed effects
- Person FE (`pid`) for Stage A.
- Household FE (`fid_base`) as alternative.
- Year FE (`year`) throughout.
- Province FE added in Stage B DID for regional heterogeneity robustness.

### 5.9 Standard errors
Two-way clustered at (`pid`, `year`) for Stage A. Clustered at `fid_base × post2021` for Stage B (stratum-robust DID SE).

---

## 6. Analysis plan

### 6.1 Primary specification (pre-registered; H2.1)
$$
qn12012_{i,t} = \alpha_i + \gamma_t + \beta_1 \cdot eexp\_share_{i,t} + X_{i,t} \cdot \phi + \varepsilon_{i,t}
$$
One-sided: `H_0: β_1 ≤ 0` vs. `H_A: β_1 > 0` at α_Bonf = 0.0125.

### 6.2 Primary specification (pre-registered; H2.2)
$$
[(expense - eexp)/expense]_{i,t} = \alpha_i + \gamma_t + \beta_2 \cdot eexp\_share_{i,t-1} + X_{i,t} \cdot \phi + \varepsilon_{i,t}
$$
One-sided: `H_0: β_2 ≥ 0` vs. `H_A: β_2 < 0` at α_Bonf = 0.0125.
**Note:** H2.2 is structurally bounded (shares sum to 1), so some crowd-out is mechanically expected. We pre-specify the test of interest as whether the crowd-out survives person FE and lags — i.e., whether previous-wave education spending predicts reduced subsequent non-education share, **not** merely the contemporaneous share identity.

### 6.3 DID specification (pre-registered; H2.3)
$$
qn12012_{i,t} = \alpha_i + \gamma_t + \delta \cdot (post2021_t \times high\_baseline\_tutoring_i) + X_{i,t} \cdot \phi + \varepsilon_{i,t}
$$
One-sided: `H_0: δ ≥ 0` vs. `H_A: δ < 0` at α_Bonf = 0.0125.
Event-study version: replace the single `post2021 × high_baseline` interaction with wave-by-wave interactions (2014, 2016, 2018, 2020, 2022 × high_baseline), with 2020 as the reference wave. Pre-trend test: coefficients for 2014, 2016, 2018 should be statistically indistinguishable from 0.

### 6.4 Placebo DID (pre-registered discriminant; H2.4)
$$
qn12012_{i,t} = \alpha_i + \gamma_t + \delta_{pbo} \cdot (post2019_t \times high\_baseline\_tutoring_i) + X_{i,t} \cdot \phi + \varepsilon_{i,t}
$$
Sample restricted to 2014–2020 (pre-policy window). Predicted: `δ_pbo` indistinguishable from 0 at α = 0.10 (two-sided).
This is a **discriminant check**; not counted toward the 4-hypothesis Bonferroni correction but is required to validate H2.3 identification.

### 6.5 Secondary specifications (pre-registered)
- Treatment: `log(school)` (narrow tutoring spend).
- Sweet DV alternate: `qn12016` future-confidence (close parent-pride proxy).
- Bitter outcome alternate: non-education expenditure level (not share) in log form.
- λ-interaction: `eexp_share × only_child`; `eexp_share × child_male`.
- Triple-diff DID: `δ × only_child` to test if 双减 effect concentrates among households with one child.

### 6.6 Specification curve (pre-registered)
≥500 variants combinatorially over:
- 3 treatment definitions (`eexp_share`, `log(school)`, `eexp_share` quartile)
- 2 Sweet DVs (`qn12012`, `qn12016`)
- 2 Bitter outcomes (non-edu share; log non-edu level)
- 4 sample filters (all child_num≥1, child_num=1 only, urban only, balanced-3+)
- 3 control sets
- 3 FE structures
- 3 λ proxies

Median ± IQR reported. Sign-consistency threshold: ≥80% for H2.1 and H2.2; ≥60% for H2.3.

### 6.7 Robustness (pre-registered)
- Triple-diff DID with regional enforcement intensity (using province-level policy strictness proxy — e.g., Beijing/Shanghai more stringent; inland provinces less).
- Alternative baseline-tutoring definitions: top quartile, top 20%, continuous.
- Alternative post-period: 2022-only vs. {2020, 2022} combined.
- Exclude households whose child ages out 2018→2022.

### 6.8 Exploratory (NOT pre-registered; flagged explicitly)
- **Triple interaction** `eexp_share × only_child × child_gender` — explicitly exploratory, not pre-registered, per construct paper's lesson from Study 5 (urban paper) that post-hoc triple-interaction rescues are impermissible.
- Sub-domain spend split (arts, STEM, language) if data permits.
- Parent-occupation heterogeneity beyond binary SES split.

---

## 7. Decision rules

### 7.1 Confirmation conditions
- **H2.1 confirmed:** β̂₁ > 0 with one-sided p < 0.0125 AND SCA median positive ≥80% sign consistency.
- **H2.2 confirmed:** β̂₂ < 0 with one-sided p < 0.0125 AND SCA median negative ≥80% sign consistency; **AND** the lagged (not contemporaneous) specification returns same sign (rules out pure share-identity mechanical).
- **H2.3 confirmed:** δ̂ < 0 with one-sided p < 0.0125 AND pre-trends (2014, 2016, 2018 coefficients) statistically indistinguishable from 0 (two-sided p > 0.10 each) AND SCA median negative ≥60% sign consistency.
- **H2.4 discriminant passed:** δ̂_pbo two-sided p > 0.10 (failure to reject no-placebo-effect null).

### 7.2 Null / falsification handling

**F1 rule applied to D2:**
- **If H2.1 null or opposite-signed** at α=0.05: D2 fails the Sweet pillar. Report null; domain treated as boundary-condition evidence. D2 retains its Figure 3 panel as a null alongside confirmed domains; the 双减 DID becomes the only informative part of the Study.
- **If H2.1 confirmed but H2.2 null/positive:** Sweet without Bitter at the household-budget level. Reframe: parenting spend raises parental satisfaction without detectable consumption crowd-out — D2 weakened on the Sweet Trap pair criterion.
- **If H2.1 and H2.2 both confirmed but H2.3 null:** the policy shock does not reduce the previously-high-baseline households' satisfaction. Two interpretations: (a) parental identity is stable and survives amenity removal (not a Sweet Trap — endorsement wasn't contingent on tutoring per se); or (b) the 2022 wave captures incomplete policy enforcement. Either way, the mechanism claim weakens. Report as "pair confirmed, policy-shock mechanism not detected."
- **If H2.4 placebo fails (δ̂_pbo two-sided p < 0.10):** identification compromised. Report DID result as suggestive rather than confirmatory; pre-trends reported transparently.
- **If child-module merge fails:** no change to H2.1–H2.4 at parent level. Child-level results move to SI §D. Not a deviation.

### 7.3 Re-analysis triggers (allowed)
- `eexp` reporting convention changes across waves detected → rerun with wave-harmonized measure.
- Child-module merge rate < 70% → invoke pre-specified fallback (§3.4).
- Non-convergence → dummy LSDV fallback.

### 7.4 Re-analysis prohibitions
- Switching from one-sided to two-sided post hoc.
- Changing top-tercile to top-quartile definition for `high_baseline_tutoring` after seeing DID result.
- Using 2021 as a "partial-treatment" wave after seeing results (2021 is not a CFPS wave; not available).
- Moving placebo year from 2019 to another year after seeing placebo result.
- Upgrading the exploratory triple interaction to a confirmatory finding.

---

## 8. Multiple comparisons

### 8.1 Within-domain
- D2 pre-registers three primary hypotheses (H2.1, H2.2, H2.3). H2.4 is a discriminant check.
- Holm-Bonferroni within D2: α_within = 0.05/3 = 0.0167 for the most stringent first-test threshold.

### 8.2 Cross-domain (primary correction)
- Four pre-registered primary hypotheses across D3, D8, D2, D5 → **α_Bonf = 0.05 / 4 = 0.0125**.
- Primary confirmation threshold for H2.1, H2.2, H2.3: one-sided p < 0.0125.
- H2.4 placebo uses α = 0.10 (two-sided) by convention as a discriminant validity check.

### 8.3 Power implications
- H2.1: N ≈ 22,000 balanced × expected β̂ 0.15 SD → >90% power at α_Bonf.
- H2.2: same sample × expected β̂ −0.08 share-points → ~80% power at α_Bonf (bounded-share variance lowers effective effect size).
- H2.3: N ≈ 18,000 DID sample × expected δ ≈ −0.25 SD → ~80% power at α_Bonf.
- **Weakest link in power:** H2.3 given the DID subsample size and the interaction-on-subgroup nature. If H2.3 returns p ∈ [0.0125, 0.05], reported as "directionally consistent, under-powered at the cross-domain threshold."

### 8.4 Secondary and exploratory
FDR correction (Benjamini-Hochberg) across SCA variants and secondary tests. Reported q-values alongside p-values.

---

## 9. Deviations handling

### 9.1 Anticipated deviation risks

| Risk | Likelihood | Handling |
|:---|:---:|:---|
| **Child-module merge fails (<70% match)** | **HIGH** (most likely deviation) | Pre-specified fallback (§3.4): child outcomes move to SI §D; parent-level H2.1–H2.4 unchanged. Not a deviation. |
| `eexp` reporting convention shift 2016→2018 | Medium | Wave-harmonization log; flag as robustness in main text. |
| `qn12012` missing spike in specific waves | Low (N = 84,328; 2.3% missing) | Ignore; IPW robustness in SCA. |
| 双减 policy partial enforcement (regional) | Medium | Triple-diff with provincial enforcement intensity as robustness; main DID averaged-effect. |
| `high_baseline_tutoring` group size imbalance (e.g., <25% of sample in top tercile) | Low | Adjust to top quartile if balance problem; report both. |
| 2022 wave delayed release | Low (CFPS 2022 released 2024-2025) | Cleaning pipeline confirms data availability before registration deposit. |

### 9.2 Protocol deviation reporting
Any deviation from §5–§6 affecting primary H2.1–H2.3 must be:
1. Documented in `03-analysis/logs/d2_deviations.log` with timestamp + rationale.
2. Reported in main text with explicit flag.
3. Both pre-registered and deviated results reported side-by-side.

### 9.3 Non-deviations
- Invoking §3.4 child-module fallback.
- Bootstrap replication count.
- Winsorization at 1/99th percentile.
- Choice of display format.
- Province-level enforcement robustness add-on.

### 9.4 Deviation specifically prohibited
- Re-defining "high baseline tutoring" to rescue a null H2.3.
- Dropping H2.4 placebo requirement to preserve H2.3.
- Adding waves or sub-periods post-hoc.

---

## 10. Data and code availability

### 10.1 Data
- CFPS public via ISSS, Peking University.
- Child-module data: same source, separate questionnaire files.
- Derived panel deposited at OSF at submission.

### 10.2 Code
- D2 scripts: `03-analysis/scripts/d2_*.py` and `.R`.
- SCA engine: `03-analysis/spec-curve/d2/`.
- DID event-study: `03-analysis/scripts/d2_did_shuangjian.R`.
- Deposited OSF + GitHub at submission; public at acceptance.

### 10.3 Pre-registration timing
Registered **before** D2 Stage A coefficients and before DID event study executed. Commit hash at registration: [to be recorded at OSF deposit].

---

## 11. Conflict of interest
None.

---

## 12. Cross-reference

Companion pre-registrations (same paper):
- `pre_reg_D3_996.md` — Headline; overwork.
- `pre_reg_D8_housing.md` — Second headline; mortgage burden.
- **`pre_reg_D2_education.md` — this document.**
- `pre_reg_D5_diet.md` — Boundary; food expenditure.
- Cross-reference overview: `README.md` in this directory.

D1 (urban over-investment) uses the prior OSF registration from the `infra-growth-mismatch` paper.

---

**Sign-off:**
Lu An, 2026-04-20 (to be dated at OSF deposit)
Hongyang Xi, 2026-04-20 (to be dated at OSF deposit)

**OSF Deposit URL:** [pending deposit]
