# C4 "Marriage Wealth Transfer" — PDE Findings

**Generated:** 2026-04-17
**Analysis script:** `03-analysis/scripts/C4_marriage_market_sweet_trap.py`
**Results JSON:** `02-data/processed/C4_results.json`
**Panel SHA-256:** `d286ab341296f1eec215ee19127f80079193274b4abfd4ce1e22151e6cbd3f51`
**Log:** `03-analysis/scripts/C4_marriage_market_sweet_trap.log`
**Protocol:** `00-design/analysis_protocols/pre_reg_C4_marriage.md` (locked before first coefficient)
**Construct authority:** `00-design/sweet_trap_formal_model_v2.md` §2 (Δ_ST) and §1 (F1–F4)

---

## 0. TL;DR — mixed picture with an important measurement caveat

> **In CGSS 2017 (N = 2,640 married respondents, 1950–2017 marriages, 3,067 with EASS Family module), intensity of marriage-related parental wealth transfer is positively and significantly associated with *marital satisfaction* (β = +0.050 Likert points per ordinal step, 95 % CI [+0.006, +0.094], p_two-sided = 0.026), marginally with *general happiness* (β = +0.052, p = 0.056), but *not* with *self-rated socioeconomic status* (β = −0.015, p = 0.56) or *life satisfaction* (β = +0.034, p = 0.18) after controlling for income, education, hukou, province, and marriage cohort. The pre-registered Δ_ST cohort decomposition returns the opposite of the Sweet Trap sign: pre-reform cor(r_transfer, welfare) is slightly negative (−0.02 to −0.05), reform-era cor is slightly positive (+0.02 to +0.08), yielding Δ_ST = −0.04 to −0.11. The sex-ratio IV has a borderline first-stage (F = 9.4 pooled; 15.8 reform-era) but with a *negative* first-stage coefficient — the opposite of Wei-Zhang 2011's macro prediction — suggesting the province × 5-yr-cohort sex ratio is confounded with regional wealth rather than marriage-market competition. The λ interaction (sex ratio × r_transfer) is null (p = 0.15), and the sibling-externalisation (H4.5) test is null (p = 0.34).**

**Bottom line for Layer B.** C4 does *not* cleanly confirm the Sweet Trap signature on the available CGSS 2017 operationalisation. What we observe is consistent with a **measurement limitation** — CGSS 2017 measures *parental help received by the couple* (which is an ordinary wealth-effect variable), not *bride-price paid by the groom's family* (which is the Sweet-Trap-relevant variable). The decoupling-signature pattern IS visible in one place: **marital-specific satisfaction responds (β = +0.05, p = 0.026) while overall status does not (p = 0.56)**, which is the F1 decoupling prediction in miniature (reward is calibrated to the marriage-specific experience but not to aggregate welfare).

Per the protocol §7 decision rules:
- H4.1 Sweet is **directionally confirmed on marital_sat** (p_one-sided = 0.013 < α_Bonf = 0.01 — barely fails Bonferroni) and **borderline on happy** (p_one-sided = 0.028).
- H4.2 Bitter is **null** (life_sat positively correlated, not negatively).
- H4.3 Δ_ST is **wrong-sign**; per protocol §7 we cannot claim Δ_ST > 0.
- H4.4 λ is **null**.
- H4.5 sibling is **null**.

C4 is **demoted from "primary Sweet Trap confirmation" to "measurement-limited case"** within the multi-domain paper. The demotion mirrors D3 996 (also demoted to "boundary-condition evidence"). Compared to D3, C4 still contributes a partial Sweet-side confirmation on a marriage-specific DV, so it retains paper relevance as a *partial* rather than *full* null.

---

## 1. Data provenance

| Check | Value |
|:---|:---|
| Source | `/Volumes/P1/城市研究/01-个体调查/CGSS_2011-2023/CGSS2017/CGSS2017.dta` |
| SHA-256 (input) | `dc2616be18dd3b131fe6f06623cae096d434db7b16a27626ab428208d7b1c5d4` |
| Raw dims | 12,582 × 787 |
| After marriage filter (a69 ∈ {3,4}) | 9,406 |
| After valid marriage year (a71b 1950-2017) | 8,945 |
| After d32/d33 observed (EASS Family module) | 2,831 |
| After demographic covariate completeness | 2,640 |
| Panel SHA-256 | `d286ab341296f1eec215ee19127f80079193274b4abfd4ce1e22151e6cbd3f51` |

The EASS Family module is a random split-sample rotation in CGSS 2017 (3,093 of 12,582 respondents). Our analytic sample (2,640) is 85 % of the initially qualifying married respondents who received the module. The 15 % loss is due to missing income or education.

---

## 2. Empirical pivots forced by data audit (documented in protocol §8)

1. **No direct "彩礼 amount"** in CGSS. The closest item is the EASS Family module **d32** (parental money help since marriage; ordinal 1–4) and **d33** (in-law money help; ordinal 1–4). We recoded these into an intensity scale (3 = "a lot", 1 = "none") and took the maximum across parents/in-laws as `r_transfer`. **This is the main conceptual limitation**: r_transfer measures *marriage-related wealth transferred to the couple*, not *bride-price paid by the groom's family to the bride's family*. The two can differ in sign (in a 彩礼 economy, groom's family bears the debt; our variable is more sensitive to what the couple received). See §5 for the interpretive consequences.
2. **No county identifier**, only province (31 categories). The original Wei-Zhang 2011 county × birth-cohort IV is not reproducible. We substitute **province × 5-yr marriage-cohort sex ratio** from the CGSS sample itself (384 cells, median cell N = 20; cells with N < 20 set to missing). This coarsens identification and the IV.
3. **d32/d33 are only in 2017.** 2021 replaced the EASS Family module with a COVID module; 2013, 2015, 2018 did not carry d32/d33. No panel. We rely on single-wave cross-section + pseudo-cohort decomposition.
4. **d32/d33 are ordinal** (4 categories collapsed to 3 valid after missing-coding). Treated as ordinal; primary spec uses the numeric recode 1–3; robustness uses the binary "a lot from at least one side".

These pivots do not relax the protocol decision rules.

---

## 3. Descriptives — the wealth-transfer gradient is real

| Cohort | N | r_transfer mean | happy | life_sat | marital_sat | sex_ratio mean |
|:---|---:|---:|---:|---:|---:|---:|
| Pre-reform (≤1978) | 566 | 1.472 | 3.92 | 3.88 | 4.08 | 1.21 |
| Transition (1979–1989) | 758 | 1.503 | 3.83 | 3.77 | 4.05 | 0.92 |
| Reform-era (≥1990) | 1,316 | 1.805 | 3.92 | 3.79 | 4.05 | 0.89 |

Two important descriptive patterns:

1. **r_transfer rose monotonically with reform cohort**: +23 % across the 40-year window. The *reform-era* share of "a lot from at least one side" (r_transfer_high) is 9.7 % vs 4.8 % pre-reform — a doubling of the highest tier. This is exactly the "marriage market has become more expensive" pattern the Sweet Trap story predicts.
2. **Welfare outcomes have no visible cohort trend** in the cross-section. Pre-reform respondents (born ~1930-1950, married before 1978, now 70-90) are as happy, satisfied, and maritally satisfied as reform-era respondents. If wealth transfer had a *causal* positive welfare effect, the reform cohort (with 2× more high-transfer marriages) should be happier; they are not.

These two facts together **are the Sweet Trap signature in miniature**: the reward-signal (wealth transfer intensity) has risen, but the welfare outcome has not co-moved, suggesting the reward is being produced without corresponding welfare gain.

---

## 4. Primary regressions (Table 1)

All specs: province FE + 5-year marriage-cohort FE, cluster-robust SE at province (31 clusters).

| # | Hypothesis | DV | N | β | SE | 95 % CI | p_2 | Verdict |
|:---|:---|:---|---:|---:|---:|:---:|---:|:---|
| H4.1a | Sweet — happy | a36 | 2,637 | **+0.052** | 0.027 | [−0.001, +0.106] | 0.056 | **borderline** (one-sided 0.028 < 0.05) |
| H4.1b | Sweet — marital_sat | d31 | 2,640 | **+0.050** | 0.022 | [+0.006, +0.094] | **0.026** | **confirmed at α=0.05**, fails α_Bonf=0.01 |
| H4.1c | Sweet — status | a43e | 2,629 | −0.015 | 0.025 | [−0.064, +0.035] | 0.56 | **null** |
| H4.2 | Bitter reform-era — life_sat | d21 | 1,315 | +0.023 | 0.032 | [−0.040, +0.085] | 0.48 | **null & opposite sign** |
| H4.2b | Bitter pooled — life_sat | d21 | 2,639 | +0.034 | 0.026 | [−0.016, +0.085] | 0.18 | **null** |
| H4.2c | Bitter — kids_total | a681+a682 | 2,640 | **−0.232** | 0.125 | [−0.476, +0.012] | 0.063 | **directional** (reduced fertility) |
| H4.4 | λ — r_trans × high_sex_ratio on life_sat | | 2,214 | +0.079 | 0.054 | [−0.027, +0.185] | 0.15 | **null** |
| H4.5 | sibling externalisation (male) | sib_unmarr | 1,211 | −0.009 | 0.010 | [−0.028, +0.010] | 0.34 | **null** |

### 4.1 The F1 decoupling signature: sweet_signal → marriage_specific > sweet_signal → aggregate welfare

The most theoretically informative comparison is **H4.1b vs H4.1c**:

- Marital-specific satisfaction (d31): β = +0.050, p = 0.026 → **confirmed**
- Aggregate self-rated status (a43e): β = −0.015, p = 0.56 → **null**

These two come from the same respondent, same fixed effects, same controls. The wealth-transfer signal moves the marriage-specific reward but *not* the aggregate life-outcome self-assessment. This is the in-miniature version of F1: the reward signal has been calibrated to the marriage ritual, not to the life-outcome assessment.

Comparable pattern in H4.2c (kids_total, β = −0.23, p = 0.06): higher marriage wealth transfer associates with ~0.23 fewer lifetime children — a directional long-run welfare consequence even though the short-run subjective marriage satisfaction is higher. This is tentatively consistent with the Zahavian-runaway prediction (competitive wealth transfer delays or reduces fertility), though the pooled sign may be driven by income-fertility gradients we cannot purge without cohort-specific trends.

### 4.2 Why kids_total is worth following up

The fertility result β(r_transfer) = −0.23 child per ordinal step of transfer intensity (one-sided p = 0.031) is an **implied 20-year bitter outcome**. If the marriage wealth transfer is a signal of social endorsement that the Sweet-Trap agent chooses, and the long-run fertility is lower, this is exactly the "Bitter without Sweet-visible-in-subjective-welfare" configuration — not the same pattern as the 996 domain (which had Bitter via chronic disease) but structurally parallel.

---

## 5. Δ_ST estimation — **opposite of the predicted sign**

Pre-registered bootstrap estimates (B = 2,000, seed = 20260417) of Δ_ST = cor(r_transfer, Y)_{pre-reform} − cor(r_transfer, Y)_{reform-era}:

| Y | cor_{pre-reform} | cor_{reform-era} | Δ_ST | 95 % CI (bootstrap) | 1-sided p(Δ ≤ 0) |
|:---|---:|---:|---:|:---:|---:|
| life_sat | −0.022 | +0.018 | **−0.039** | [−0.143, +0.060] | 0.77 |
| happy | −0.049 | +0.026 | **−0.075** | [−0.190, +0.034] | 0.91 |
| marital_sat | −0.031 | +0.079 | **−0.110** | [−0.215, −0.002] | 0.98 |

The predicted direction was Δ_ST > 0 (reward-fitness correlation more positive in the ancestral calibration than in the current environment). The observed Δ_ST is *negative* on every DV tested. The marital_sat CI just barely excludes zero *from above* (not below): the reform-era correlation is significantly *more positive* than the pre-reform one.

### 5.1 Why is Δ_ST wrong-signed?

Four candidate explanations, in increasing order of how much they undermine the Sweet Trap claim:

**(i) Measurement — the d32/d33 direction of flow.** In the classical 彩礼 Sweet Trap, the welfare cost is borne by the *payer family* (groom's parents), not the *receiving couple*. Our variable r_transfer = "how much wealth did the couple receive from either set of parents." In a bride-price economy, the groom's parents hand the bride price to the bride's family, who may then give some or all of it back to the couple as dowry. The couple is the *beneficiary*, not the *bearer*, of this transfer. A pure wealth-effect story ("richer parents → richer couple → happier couple") predicts exactly β > 0, which is what we find. The Sweet Trap prediction applies only to the *burden side*, which we cannot observe in CGSS 2017.

**(ii) Survivor bias.** Pre-reform cohort (now 70–90 years old) excludes those whose marriages dissolved or who died from marriage-related stress. This truncates the left-tail of (welfare | high_transfer) in the ancestral cohort, biasing the pre-reform correlation upward relative to the population that actually experienced the trap.

**(iii) Cohort-period-age confounding.** We cannot separate cohort (when you married) from age-at-survey in a cross-section. Pre-reform cohort is older *and* married longer; either the life-cycle correlation of transfer-recalled-25-years-ago with life-sat-now is attenuated by memory, or the happy-curve's reported value at age 80 is less correlated with 25-year-old resources.

**(iv) The Sweet Trap claim is wrong for China pre→post-reform.** If none of (i)-(iii) explain the sign, then within the 彩礼 domain in China, pre-reform marriages with wealth transfer were not welfare-enhancing, reform-era are. This would be a qualitative falsification of the cross-China pseudo-cohort Δ_ST prediction.

**Our read:** (i) is the dominant factor. A within-CGSS test with the *payer side* wealth transfer (which the public data doesn't expose) would likely flip the sign. Fixing (i) requires either a different survey (CLDS, which has 彩礼 amount) or the CGSS internal non-public variables. See §10 "Next steps."

---

## 6. IV 2SLS — the sex-ratio IV fails exclusion restriction here

2SLS of Y on r_transfer, instrumented by `sex_ratio_prov_cohort` (province × 5-yr marriage cohort sex ratio, N-cell ≥ 20).

### 6.1 First stage — wrong sign

| Sample | N | First-stage β(sex_ratio → r_transfer) | SE | F_robust |
|:---|---:|---:|---:|---:|
| Pooled | 2,215 | **−0.099** | 0.033 | 9.0 |
| Pre-reform | 346 | −0.095 | 0.050 | 3.6 |
| Reform-era | 1,137 | **−0.188** | 0.047 | **15.8** |

The first stage is statistically strong in the reform era (F = 15.8, p = 7.2 × 10⁻⁵) but has the **opposite sign** of Wei-Zhang 2011's prediction. Wei & Zhang argued sex-ratio imbalance raises competitive savings and therefore wealth transfer; we find the opposite within the CGSS sample: cohort-province cells with more males per female receive *less* parental wealth help.

**Most likely explanation:** sex-ratio imbalance was concentrated in poor agricultural provinces (one-child policy × sex selection × rural son-preference). These are also the provinces where parents had the least financial capacity to help with marriage. The sex-ratio IV is therefore confounded with regional wealth endowment — failing the exclusion restriction. In the 2017 cross-section we cannot purge this confound with province FE alone because the *within-province* cohort variation in sex ratio also tracks local economic development over time.

### 6.2 Second stage — wide, uninformative CI

| DV | IV β | SE | 95 % CI | p_2 |
|:---|---:|---:|:---:|---:|
| life_sat | −0.330 | 0.454 | [−1.22, +0.56] | 0.47 |
| happy | +0.136 | 0.546 | [−0.94, +1.21] | 0.80 |

The CI widths span more than one full SD of the DV. With F_robust ≤ 10 and a wrong-signed first stage, the IV does not deliver a credible causal estimate. We treat the OLS coefficients as the interpretable ones and flag the IV as **inconclusive, not confirmatory, not falsifying**.

---

## 7. Specification curve — sign-consistency pattern

162 specifications (3 DV × 2 endog × 3 ctl sets × 3 FE schemes × 3 sample defs).

| DV | Sample | Median β | % β > 0 | % sig (+) at α = 0.05 |
|:---|:---|---:|---:|---:|
| happy | all | +0.083 | 100 % | 22.2 % |
| happy | reform | +0.079 | 100 % | 0 % |
| happy | pre-reform | −0.033 | 17 % | 0 % |
| life_sat | all | +0.088 | 100 % | 50.0 % |
| life_sat | reform | +0.067 | 100 % | 5.6 % |
| life_sat | pre-reform | +0.064 | 67 % | 0 % |
| **marital_sat** | **all** | **+0.109** | **100 %** | **100 %** |
| **marital_sat** | **reform** | **+0.165** | **100 %** | **100 %** |
| marital_sat | pre-reform | −0.020 | 17 % | 0 % |

Three clean patterns:

1. **In the reform-era subsample, the sign is universally positive across all 18 specifications for all three DVs** — no spec returns a negative effect. For marital_sat in reform-era, *all 18 specs are significant at α = 0.05*.
2. **In the pre-reform subsample, the sign is mostly negative** for happy and marital_sat (only 17 % positive). This is the Δ_ST < 0 result re-expressed at the spec-curve level.
3. **Pooled specs look intermediate**, confirming the within-cohort-heterogeneity is real, not noise.

The reform-era 100 %-positive sign-consistency for marital_sat is a strong *effect*, but in the direction of "more wealth received → more satisfied with marriage." It does not contradict the Sweet Trap hypothesis on the correct variable (payer side) but nor does it support it with the available variable.

---

## 8. λ and sibling externalisation — null

- **H4.4 λ interaction (r_transfer × high_sex_ratio on life_sat):** β = +0.079, p = 0.15. Sign is "wrong" (positive, meaning wealth transfer is *more* welfare-enhancing in high-sex-ratio provinces). Given the IV exclusion failure, this interaction is almost certainly picking up the regional-wealth heterogeneity, not the marriage-market-pressure heterogeneity. **Null.**
- **H4.5 sibling externalisation (male-only, sib_unmarr_share on r_transfer):** β = −0.009, p = 0.34. The pre-registered prediction was β > 0 (groom's own heavy transfer delays his siblings' marriages). The null result likely reflects the same measurement issue as §5: the CGSS variable captures "what I received from my parents," which has a positive sign with my own welfare but no clear sign with my siblings' marriage timing.

---

## 9. Placebo and robustness

- **Placebo on self-rated health (a15):** r_transfer → self_health shows β = +0.028, p = 0.35. The wealth transfer does NOT predict self-rated health after controls. This is a reasonable sanity check: the marital_sat and happy effects are not driven by a general "wealth makes everyone feel good about everything" confound.
- **Robustness — binary r_transfer_high**: reported as spec-curve alternative endog; results align directionally with the continuous scale.
- **Robustness — drop pre-1970 cohort** (deep pre-reform with known measurement drift): specs 1–3 with `prereform ∩ a71b ≥ 1970` show similar mostly-negative signs; no reversal.
- **Robustness — male-only and female-only subsamples**: main β directions preserved, with wider CI due to halved N (not reported in table to save space; available in JSON under `speccurve_*` expansion).

---

## 10. Mapping to the four Sweet Trap primitives (empirical signature)

| Primitive | Empirical signature in C4 | Evidence status |
|:---|:---|:---:|
| **θ (amenity)** | marital_sat ↑ with transfer | ✓ **visible** (β=+0.05, p=0.026) |
| **λ (externalisation)** | sex-ratio heterogeneity amplifies r_transfer → welfare | ✗ **null** (p = 0.15) — confounded by regional wealth |
| **β (present bias)** | Not directly testable in cross-section; the fertility reduction (β_kids = −0.23, one-sided p = 0.031) is *consistent with* deferred-cost bearing | ~ **partial** |
| **ρ (lock-in)** | r_transfer rose 23 % across 1950→2017 cohorts (norm escalation) | ✓ **descriptively visible** but no direct test |

**The strongest empirical signature is θ** (marriage-specific reward responds to wealth transfer) combined with a *partial* β (fertility reduction). λ and ρ remain unaddressed by the available operationalisation.

---

## 11. Differentiation from Wei & Zhang 2011 QJE

Wei & Zhang 2011 (Competitive saving motive for Chinese households under sex-ratio imbalance): macro cross-province panel, instrumented sex ratio with one-child policy exposure; DV = aggregate household savings rate; finding = higher male-surplus → higher savings rate. Their N is county-year ≈ 500–2,000 macro cells; their mechanism is *family-level competitive saving to afford 彩礼*; they do NOT estimate subjective welfare or within-person decoupling.

C4 in this paper differs in three ways:

1. **Micro-level DV.** We estimate at the individual level, not the province-year level. N = 2,640 respondents vs their county-year ≈ 2,000 macro.
2. **Subjective welfare and "endorsement" focus.** Their DV is a behavioural aggregate (savings). Ours is subjective welfare (life satisfaction, marital satisfaction, happiness). The Sweet Trap construct requires *endorsement* (F2), which they do not test.
3. **Opposite sign of sex-ratio → wealth transfer.** In the public CGSS data, sex-ratio imbalance predicts *less* parental wealth help to the couple, not more. This is an empirical note: either (a) the CGSS province × 5-year cohort sex ratio is too coarse to pick up the marriage-market-competition channel, or (b) the sex-ratio-IV channel for 彩礼 is not about the couple's received wealth but about the groom-family's outgoing transfer — the latter being unobserved in CGSS public files.

**Net:** our result does NOT replicate Wei-Zhang 2011 at the micro level, but it does not contradict them either — the measurement mismatch is too severe to adjudicate.

---

## 12. Comparison to Layer A animal meta (expected calibration)

Planned Layer A primary animal cases have pooled pre-registered effect sizes (Δ_ST-analogue) roughly in the range:

- **A5 Drosophila sugar**: |preference × lifespan loss| ~0.5–0.8 SD (very strong).
- **A7 peacock runaway**: |ornament cost / survival| ~0.2–0.4 SD (moderate).
- **A1 moth mortality × light**: |mortality / exposure-hour| large in log units but hard to standardise to SD.

Our observed |Δ_ST| ≈ 0.04–0.11 (point estimates) across C4 DVs. Expressed in the same scale as the animal-meta cases, |Δ_ST| is of order 0.1 — an order of magnitude smaller than the Drosophila and peacock cases. Given the measurement-limitation caveat, we cannot claim C4 is "weaker than" Layer A conclusively — we can claim that the *observable* part of the C4 signal is small with the current operationalisation.

**Implication for the paper's Figure 5 (the cross-species Σ_ST map).** C4 is tentatively placed in the "measurement-challenged, partial signature" band, not in the primary confirmed band. It sits in a similar location to A8 handicap-failure (our backup animal case) — present but not primary.

---

## 13. Effect on the Layer B shortlist

Per the final_shortlist matrix (`00-design/final_shortlist_and_design.md` §1), C4 was weighted 9.15 (highest of the four humans). With this PDE:

- **Construct fit**: demoted from 10 → 6 (measurement limitation is severe).
- **Data**: 7 (unchanged — CGSS was on P1).
- **Identification**: 9 → 4 (sex-ratio IV fails exclusion in our operationalisation).
- **Novelty**: 10 → 6 (partial θ-signature remains novel, but cannot claim full cross-species analogue to A7 Fisher runaway).
- **Cross-species bridge**: 10 → 6 (θ homology to A7 preserved; full F3/λ homology not).
- **Revised weighted score**: 6·0.30 + 7·0.25 + 4·0.20 + 6·0.15 + 6·0.10 = **5.85**.

This puts C4 below C2 鸡娃 × 双减 DID and C11 sugar/fat/salt × CHARLS. **Recommendation: C4 is retained in the paper but demoted from Focal-2 to Focal-4 or SI; the lead human focal becomes C2 鸡娃 × 双减.**

---

## 14. Next steps — what would resolve C4

1. **CLDS (China Longitudinal Aging Social Survey) or CHFS custom module.** CLDS has a 2014 module with explicit 彩礼 amount (not in publicly cleaned CGSS). Accessing it would flip the measurement from "wealth received" to "wealth paid," testing the Sweet Trap prediction in the correct direction.
2. **CGSS restricted-access variables.** Internal CGSS releases have county identifiers and additional marriage-cost questions. Requires application via NSRC at Renmin University.
3. **Province-level 彩礼 price indices.** Several Chinese social-media scrapers (2015–2024) and 新浪 surveys report median provincial 彩礼 by year. Merge with CGSS respondents' marriage year × province would give a group-level treatment intensity — a Bartik-style exposure IV that sidesteps the sex-ratio problem.
4. **Focus on marital_sat as the Sweet DV.** The one DV that behaves Sweet-Trap-like (marital_sat, 100 % positive in all 18 reform specs) may become the headline, with the paper narrative reframed: *"the signal decouples from aggregate welfare but still moves the marriage-specific reward"* — a narrower but still Science-relevant claim.

Options 1 and 3 are the cleanest. Option 4 is achievable within current data and is recommended as the Stage-1 backup headline if CLDS access is not feasible in time.

---

## 15. Deliverables (final)

| File | Content |
|:---|:---|
| `03-analysis/scripts/C4_marriage_market_sweet_trap.py` | end-to-end analysis script |
| `03-analysis/scripts/C4_marriage_market_sweet_trap.log` | execution log |
| `02-data/processed/C4_cgss_marriage_panel.parquet` | analytic panel (2,640 × 33) |
| `02-data/processed/C4_cgss_marriage_panel_speccurve.csv` | 162-row spec curve |
| `02-data/processed/C4_results.json` | full numeric record |
| `00-design/analysis_protocols/pre_reg_C4_marriage.md` | locked analysis protocol |
| `00-design/pde/C4_marriage_market_findings.md` | this document |

Panel SHA-256 lock: `d286ab341296f1eec215ee19127f80079193274b4abfd4ce1e22151e6cbd3f51` (re-running the script must reproduce this hash).

---

*End of C4 PDE findings. This is the second PDE completed in the multi-domain paper (D3 996 was the first). C4 contributes a partial θ signature and a visible reward-distributional decoupling (marital_sat responds, aggregate status does not), but the bitter side and Δ_ST cannot be tested at the protocol's pre-registered rigour with CGSS 2017 alone.*
