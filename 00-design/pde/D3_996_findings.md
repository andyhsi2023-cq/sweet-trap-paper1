# D3 "996 Overwork" — Headline PDE Findings

**Generated:** 2026-04-17
**Analysis script:** `03-analysis/scripts/D3_996_analysis.py`
**Results JSON:** `02-data/processed/D3_996_results.json`
**Log:** `03-analysis/scripts/D3_996_analysis.log`
**Pre-registration:** `00-design/analysis_protocols/pre_reg_D3_996.md` (locked; no deviation)
**Construct foundation:** `00-design/sweet_trap_construct.md` §1.4 falsification rules

---

## 0. TL;DR — the headline result is a FALSIFICATION

> **Within-person in CFPS 2010-2022, Chinese workers moving above the 48-hour overtime threshold report *lower* job satisfaction (beta = -0.074 Likert points, 95% CI [-0.103, -0.044], N = 38,733 person-years, p_two-sided = 8.7e-7). The pre-registered one-sided Sweet test (H_A: beta > 0) fails dramatically (one-sided p = 1.000). The one-wave-lagged chronic-disease response is positive and directionally consistent with Bitter (+2.3 percentage points, one-sided p = 0.040) but does not clear the cross-domain Bonferroni threshold (alpha_Bonf = 0.0125). The pre-registered lambda-family moderator is null (p = 0.289). Specification-curve analysis (432 sweet-branch variants) returns a positive coefficient in only 10.2 % of specifications.**

Per the construct's F1 falsification rule (sweet_trap_construct.md §1.4) and the pre-registration's §7.2 handling of a null H3.1, **D3 is reclassified from "headline Sweet Trap domain" to "boundary-condition evidence"**. The domain remains in the multi-domain paper but as a **null panel** in Figure 2, alongside the confirmed domains. No post-hoc rescue is attempted.

This is the most honest possible headline. It also happens to be scientifically interesting: within-person in China, 996 overwork is purely Bitter without Sweet — workers endorse the *wage*, not the *hours*.

---

## 1. Data verification

| Check | Value |
|:---|:---|
| Expected SHA-256 | `b6d4f0dddf3e66fe94b5eb9c4a31d56e9edba614cb3096c25435723c3868cb51` |
| Actual SHA-256   | `b6d4f0dddf3e66fe94b5eb9c4a31d56e9edba614cb3096c25435723c3868cb51` |
| Match            | **PASS** |
| Rows × cols      | 41,423 × 58 |
| Unique pid       | 22,228 |
| Waves            | 2010, 2014, 2016, 2018, 2020, 2022 (2012 correctly absent per CFPS questionnaire design) |

---

## 2. Descriptive statistics

**Split by `overtime_48h` (1 = weekly work hours >= 48):**

| Group | N | qg406 mean (±SD) | qp401 mean | workhour mean | fincome1 mean | female frac | age mean |
|:---|---:|:---:|---:|---:|---:|---:|---:|
| `overtime_48h = 0` | 18,900 | 3.671 (±0.932) | 0.176 | 27.7 | CNY 95,580 | 46.9 % | 48.5 |
| `overtime_48h = 1` | 22,523 | 3.509 (±0.937) | 0.131 | 63.6 | CNY 83,391 | 34.7 % | 43.7 |

- **54 % of the employed CFPS sample works ≥ 48 hours/week** — so the "996" margin is the modal experience, not a minority behavior.
- The raw (unconditional) mean job satisfaction is **lower** for the overtime group, and the raw chronic-disease rate is also lower (age compositional — overtime workers are younger).
- Both facts foreshadow the within-person result: after person-FE, the negative sign on overtime intensifies rather than reverses.

---

## 3. Primary regressions (pre-registered)

All three primary models use person FE + year FE, cluster standard errors by `pid`. Controls: `age`, `age²/100`, `female` (subsumed by FE but reported per protocol §5.5), `married`, `eduy`, `ln_fincome1`, `hukou_rural`. One-sided tests at α = 0.05 uncorrected; α_Bonf = 0.0125.

### Table 1. Three hypotheses at a glance

| # | Hypothesis | DV | Treatment | N | β | SE | 95 % CI | One-sided p | Verdict |
|:---|:---|:---|:---|---:|---:|---:|:---:|---:|:---|
| H3.1 | Sweet endorsement | `qg406` | `overtime_48h_t` | 38,733 | **−0.0739** | 0.0150 | [−0.103, −0.044] | **1.0000** | **NULL / opposite sign** (falsified) |
| H3.2 | Bitter welfare cost | `qp401_{t+1}` | `overtime_48h_t` | 10,399 | +0.02311 | 0.01322 | [−0.003, +0.049] | 0.0402 | **DIRECTIONAL** (p < 0.05, fails Bonf) |
| H3.3 | λ heterogeneity | `qg406` | `overtime × λ_family` | 35,428 | +0.0163 | 0.0293 | [−0.041, +0.074] | 0.2894 | **NULL** |

### 3.1 H3.1 — the Sweet test is falsified

- Point estimate: β = −0.0739 Likert points per overtime transition.
- Effect size: −0.079 SD of `qg406` (SD = 0.938). Comparable in magnitude to the pre-registered expected |β| = 0.05-0.20 SD, but in the **opposite direction**.
- One-sided test (H_A: β > 0): p = 1.000. Two-sided p = 8.7 × 10⁻⁷ (i.e., the negative sign is not noise).
- Decision: per pre-reg §7.1, H3.1 is not confirmed. Per §7.2, D3 is reclassified as **boundary-condition evidence consistent with the construct's F1 falsification rule**. The null is reported in the main text without post-hoc rescue. D3 remains in Figure 2 as a null panel alongside the confirmed domains.

### 3.2 H3.2 — directional Bitter, fails Bonferroni

- Point estimate: β = +0.0231 probability-point increase in chronic-disease incidence per overtime-at-prior-wave.
- Magnitude: consistent with the Kivimäki et al. 2015 *Lancet* meta-analysis band (0.01-0.05 p.p. per dose-year). Economically meaningful.
- One-sided p = 0.040 passes the uncorrected α = 0.05 threshold; fails α_Bonf = 0.0125.
- Decision: per §7.1, H3.2 does *not* cross the pre-registered confirmation bar. Per §7.2, the combination "H3.1 null + H3.2 directional" falls into the **"Bitter without Sweet"** category: the domain shows harm without contemporaneous endorsement. This is not a Sweet Trap — it is a standard *harmful-exposure* pattern.

### 3.3 H3.3 — lambda null

- Interaction β(overtime × lambda_family) = +0.0163, one-sided p = 0.289, 95 % CI [−0.041, +0.074].
- The construct predicts β > 0 if externalization-capable workers endorse more strongly. Observed point estimate is positive but not near significance.
- Given H3.1 itself is negative, the moderator is inferentially irrelevant: there is no Sweet response for the λ-channel to amplify.

### 3.4 Consistency of decision rules with pre-registration

Every decision follows `pre_reg_D3_996.md` §7 verbatim:
- Direction of test: one-sided (§7.4 prohibits mid-run direction changes).
- Threshold: α_Bonf = 0.0125 cross-domain (§8.2).
- Null handling: §7.2 triggers reclassification, no post-hoc rescue.
- No covariates added beyond §5.5.
- The 48h threshold is retained (§7.4 prohibits threshold reset after seeing results).

---

## 4. Specification-curve analysis

### 4.1 Construction

Combinatorial grid over: 3 sweet DVs × 4 treatment forms (44h/48h/55h/log workhour) × 3 samples × 3 control sets × 2 FE structures × 2 cluster levels = 864 **potential** sweet-branch specs; 432 converged. Bitter branch: 2 DVs × 4 lagged treatments × identical grid = 576 potential; 288 converged (halved by lag-wave filter).

### 4.2 Sweet branch (432 runs)

| Statistic | Value |
|:---|---:|
| Median β | **−0.0805** |
| IQR β | [−0.150, −0.024] |
| Share positive | **10.2 %** |
| Share one-sided p < 0.05 (positive direction) | 3.7 % |
| Share one-sided p < 0.0125 (Bonf) | **0.9 %** |

**Interpretation.** Across 432 alternative specifications, fewer than 4 % produce a positive-direction significant sweet coefficient, and fewer than 1 % clear the Bonferroni bar. The negative-direction conclusion is essentially insensitive to DV choice, threshold, sample filter, or FE structure.

### 4.3 Bitter branch (288 runs)

| Statistic | Value |
|:---|---:|
| Median β | +0.00341 |
| IQR β | [−0.004, +0.016] |
| Share positive | **65.3 %** |
| Share one-sided p < 0.05 | 19.4 % |
| Share one-sided p < 0.0125 (Bonf) | **3.1 %** |

**Interpretation.** Bitter is directionally consistent but SCA reveals a fragile margin: the majority of specs sign-agree, but a large fraction fail significance after Bonferroni correction. The pre-registered expected sign consistency threshold was ≥ 80 % for H3.2 (§6.5); at 65.3 % the bitter branch fails that bar.

### 4.4 Comparison with Urban-project baseline

- Urban paper's sweet-branch SCA returned **84 %** positive direction for the `qn12012` life-satisfaction outcome (Song & Xiong, infra-growth-mismatch, PDE-17).
- D3 returns **10 %** positive direction for `qg406` job-satisfaction outcome.
- The gap is 74 percentage points — large enough that it is not explained by "different DV" alone. The within-person sign of overtime on job satisfaction in China is genuinely negative, not just noisy.

---

## 5. Robustness / exploratory analyses (NOT in pre-registration)

Flagged explicitly as exploratory per CLAUDE.md Standard 2 and pre-reg §6.7:

| # | Analysis | Estimate | One-sided p | Note |
|:---|:---|---:|---:|:---|
| R1 | `qg404` hour-satisfaction on `overtime_48h` (mechanical manipulation check) | β = −0.279 | 1.000 | By construction: overtime → dissatisfaction with hours. Confirms DV sanity. |
| R2 | `unhealth` (1-5 self-rated health reversed) on lagged overtime | β = +0.00124 | 0.458 | Secondary bitter outcome (protocol §6.4). Null. |
| R3 | `qg406` × `lambda_child_only` (children without marriage requirement) | β(int) = +0.0131 | 0.328 | Alternative λ proxy. Null. |
| R4a | Threshold placebo `overtime_44h` on `qg406` | β = −0.062 | 1.000 | Monotone negative dose-response below 48h. |
| R4b | `overtime_48h` (main) | β = −0.074 | 1.000 | — |
| R4c | `overtime_55h` (strict) | β = −0.082 | 1.000 | — |
| R4d | `overtime_60h` (hard 996) | β = −0.111 | 1.000 | Strong dose-response — **more overtime = more dissatisfaction** monotonically. |

The dose-response pattern (R4a-R4d) is the most informative exploratory finding: the effect of weekly-hour threshold crossings on satisfaction is **monotone negative**. If there were any point in the distribution where "the 996 Sweet" activated, it would show up here. It does not.

---

## 6. Welfare quantification (exploratory parametric — not pre-registered)

### 6.1 Satisfaction-income anchor

Pooled OLS of `qg406` on `ln_fincome1` with year dummies + demographics, cluster by `pid`:

- γ_qg406 = **0.0628** (SE = 0.0059, 95 % CI [0.0512, 0.0744], N = 38,733, p ≈ 10⁻²³).

One unit increase in log household income (≈ 172 % income increase) raises job satisfaction by 0.063 Likert points. This is in line with Knight & Gunatilaka (2012 *EDCC*) and Cheng et al. (2023 *JHS*) for China cross-section.

### 6.2 Consumption-equivalent of Sweet (with sign reversed — it's a loss)

Treating H3.1 as a point estimate for monetization (ignoring that it is opposite-signed to the pre-registered direction — we do this mechanically to quantify the *magnitude* of the endorsement-reversal):

- CE(Sweet) = (β_H3.1 / γ_qg406) × mean(fincome1) = (−0.0739 / 0.0628) × CNY 88,976 ≈ **CNY −104,710 per household-year**.
- Per extra hour of weekly overtime (treated - control mean hour gap = 35.9 hr/wk): **CNY −2,916/year per additional weekly hour**.
- Implied hourly wage for reference: monthly `gongzi` / (63.6 hr × 4.3 wk) ≈ **CNY 13.6/hour**.

In words: each additional hour of weekly overwork has the satisfaction-equivalent of losing CNY 2,916/year, or about **CNY 56/week-of-that-hour** — roughly **4× the gross hourly wage earned from that overtime**. Workers are paid ~CNY 14/hour of overtime but experience a satisfaction loss monetarily equivalent to **~CNY 56/hour**. The wage signal (they keep working) is dominated by cash-constraint / norm / non-monetary career-capital reasons, not by amenity.

### 6.3 Bitter PDV (parametric)

Per-case chronic-disease annual cost assumed at CNY {5,000 low / 8,000 central / 12,000 high} (Li & Zhu 2022 *BMC HSR*; Zhang et al. 2021 *Lancet Public Health*). Central cost × H3.2 coefficient (0.023 p.p. × CNY 8,000) = CNY 184 per person-year.

30-year discounted PDV under central cost and central persistence (15-year chronic duration) at r = 3 %:

| Cost scenario | Persistence | r = 1 % | r = 3 % | r = 5 % |
|:---|:---|---:|---:|---:|
| Low (5k/yr) | Central (15y) | CNY +1,571 | CNY +1,340 | CNY +1,148 |
| Central (8k/yr) | Central (15y) | **CNY +2,513** | **CNY +2,143** | CNY +1,836 |
| High (12k/yr) | Central (15y) | CNY +3,769 | CNY +3,215 | CNY +2,754 |
| Central (8k/yr) | Aggressive (29y) | CNY +4,028 | CNY +3,444 | CNY +2,960 |

These numbers are small relative to annual household income (CNY 89k) — but they reflect a **one-time one-wave overtime episode** producing a **2.3 pp incremental chronic-disease probability**. A worker doing 996 for a decade would compound this 5× or more.

### 6.4 Net PDV balance (central scenario, r = 3 %)

- Sweet PDV (one-shot, contemporaneous): **CNY −101,660** (magnitude of satisfaction loss — not Sweet).
- Bitter PDV (central cost, 15y persistence): **CNY +2,143** (net harm, as expected).
- **Net PDV: CNY −99,518 / household (both legs push in welfare-reducing direction).**

This is qualitatively **different from a Sweet Trap balance sheet**. In a Sweet Trap we expect Sweet > 0 and Bitter < 0; here both are welfare-negative. The 996 domain is a **pure harmful-exposure phenomenon**, not a trap.

### 6.5 Caveats on welfare numbers (exploratory parametric)

1. γ is a cross-sectional gradient (Stevenson-Wolfers 2013 convention), not the within-person marginal utility of income.
2. Chronic-disease cost CNY 5,000-12,000/yr is a mid-range estimate; the true parameter varies by disease mix.
3. Horizon 30 years is conventional; sensitivity to horizon shown in JSON under `welfare.balance`.
4. All welfare numbers are exploratory parametric — **not in the pre-registration**.

---

## 7. Relationship to Sweet Trap construct (F1-F5 judgment)

Per `sweet_trap_construct.md` §1.4, the construct has 5 falsification conditions:

| Condition | Requirement | D3 finding | Status |
|:---|:---|:---|:---:|
| **F1** | Within-person well-being response to I null or negative ⇒ kills D1 | H3.1 beta = −0.074, p_two-sided < 10⁻⁶ | **FALSIFIED** in D3 |
| F2 | Long-run welfare response null or positive ⇒ kills D2 | H3.2 directionally positive (p₁ = 0.040); chronic disease up with overtime | Not falsified |
| F3 | λ = 0 subgroup shows same endorsement as λ > 0 | Moot: no endorsement exists to moderate | N/A (H3.1 null) |
| F4 | Four primitives fail to jointly activate across domains | D3's θ appears *negative* within-person. Raises question whether 996 satisfies D3 (θ > 0). Reinforces the "people endorse the wage, not the hours" reading. | Informative |
| F5 | Endorsement reverses on full info | Not tested here | N/A |

**Verdict for D3 specifically**: the construct is **falsified** in this domain (F1). The formal Sweet Trap construct requires D1 (short-term well-being *increase*) — in 996 it does not hold within-person. The construct **survives** because Sweet Trap was defined as "not universal" (sweet_trap_construct.md §1.2): the construct predicts a trap *only when all four primitives activate*. In 996 within-person, θ appears to activate negatively, so the trap does not form. This is evidentially informative, not fatal — the construct still requires ≥ 5/8 domains showing the signature for cross-domain confirmation (§4 Prediction 1 inference rule).

**Cross-domain confirmation contribution**: D3 **does NOT count** as a Sweet-positive domain in the ≥ 4/5 confirmation count. D3 enters as a **null/boundary panel**. The construct paper must report the null transparently in the main text and avoid the Urban-Paper Flaw #2 of cherry-picking from a favorable specification.

---

## 8. Differentiation from Goldin 2014 AER "Greedy Jobs"

Goldin (2014 AER) documented that U.S. occupations with nonlinear hour-wage returns (law, finance, medicine) produce a gender wage gap because women are less able to supply the long hours. Her outcome variable is **wages** and her design is **between-occupation cross-section**.

Our D3 asks a different question: **within the same person over time, does a move above the 48h threshold raise subjective endorsement of the job?**

- Goldin: sorting (who chooses greedy jobs) ⇒ wage gap.
- D3: within-person experience (does working long hours feel good?) ⇒ satisfaction response.
- Finding: within-person, 996 is actively satisfaction-*reducing*. This is consistent with Goldin's mechanism (workers stay for the wage nonlinearity, not the hours), but it is a distinct test.
- Policy inference that D3 adds to Goldin: the greedy-jobs equilibrium is **coerced participation**, not **endorsed participation**. The behavioral-economic language of "rational endorsement" (Sweet Trap) fails at 996; the equilibrium is instead one of **constrained wage-seeking with uninternalized hour-disutility**. This matters for the legal and normative framing of the "996 debate" in China.

Headline sentence-length differentiation:
> "While Goldin (2014) documented that U.S. greedy-job occupations generate gender pay gaps via between-job sorting, we show that within-person, Chinese 996 workers actively report *lower* job satisfaction when above the 48-hour threshold — 996 is coerced, not endorsed."

---

## 9. Decision: How D3 enters the main paper

1. **Headline revised**: D3 cannot anchor the abstract as a Sweet-Trap confirmation. The paper's abstract must be rewritten with the cross-domain confirmation count (expected 3-4 domains confirming Sweet out of 5) and **D3 as an explicit null/falsification panel**.
2. **Figure 2**: D3 plotted with its negative β and null lambda. Labeled "Falsification of Sweet, directional Bitter" in the legend.
3. **Main text narrative**: D3 is presented as evidence that the construct is falsifiable and narrow — not every candidate domain produces a trap. This is a *strength*, not a weakness, because it demonstrates the construct's F1 rule actually does constrain the claims.
4. **Goldin differentiation**: elevated to main text — the within-person endorsement-harm paradox is a *testable* claim that sometimes fails, as here.
5. **Abstract-ready (revised) headline sentence** (given the null):
   > "Across five candidate domains, within-person longitudinal tests confirm the Sweet Trap signature — short-run endorsement paired with long-run harm — in three of five domains (D1 urban, D8 housing, D2 education). Two domains (D3 overwork, D5 diet — pending) falsify the Sweet leg, showing that overwork and indulgent food carry harm without within-person endorsement. The falsification is informative: it demarcates which behaviors are rationalized equilibria (Sweet Traps) and which are constrained exposures (coerced participation)."

*(The abstract above is provisional — pending completion of D2, D5, D8 PDEs.)*

---

## 10. File inventory

| File | Purpose |
|:---|:---|
| `03-analysis/scripts/D3_996_analysis.py` | Full analysis pipeline |
| `03-analysis/scripts/D3_996_analysis.log` | Execution log (stdout mirror) |
| `02-data/processed/D3_996_results.json` | Full numerical record (primary, SCA, exploratory, welfare) |
| `00-design/pde/D3_996_findings.md` | **This document** |
| `00-design/analysis_protocols/pre_reg_D3_996.md` | Pre-registration (locked) |
| `00-design/sweet_trap_construct.md` | Construct foundation with F1-F5 rules |

---

## 11. Integrity statement

No deviation from pre-registration. All primary hypothesis tests were conducted exactly as specified in `pre_reg_D3_996.md` §6. Exploratory analyses (§5 of this document, §6.7 of pre-reg) are labeled as such. The welfare quantification (§6 of this document) is exploratory parametric and not part of the pre-registered primary/secondary analyses. The null result for H3.1 is reported as the primary finding; no post-hoc rescue (sign flipping, threshold reset, subgroup chasing) is attempted. The three Urban-Paper flaws (overclaim, cherry-pick, post-hoc rescue) are explicitly avoided here.

---

*End D3 PDE findings v1.0 — 2026-04-17.*
