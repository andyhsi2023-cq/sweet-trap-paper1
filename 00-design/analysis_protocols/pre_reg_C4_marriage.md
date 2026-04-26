# Analysis Protocol: Sweet Trap Study C4 — 彩礼 / Marriage Market Wealth Transfer

**Registration date (internal lock):** 2026-04-17
**Parent construct document:** `sweet_trap_formal_model_v2.md` (Δ_ST + F1–F4)
**Parent design document:** `final_shortlist_and_design.md` §4 (C4 focal)
**Status:** Analytic protocol for the second human focal domain in the 4-domain human panel (C4 bride-price × sex-ratio). Locked before seeing coefficients.

---

## 1. Why this is a Sweet Trap candidate (recap)

- **Sweet signal (R_agent):** active family/community endorsement of large marriage-related wealth transfers (彩礼 / 嫁妆 / wedding expenditures). Signals family honour, commitment device, groom-family status gain.
- **Bitter outcome (F):** 20-year household debt service, savings depletion, bride-family dowry pressure, delayed/non-marriage of groom's unmarried siblings (the classical λ-channel).
- **F1 route (Δ_ST > 0):** Route A — ancestrally bride-price was a Zahavian commitment device, but in the present-day cash-and-credit × sex-ratio-imbalanced environment has run away and become pure dissipative waste (phenomenology_archive.md §C4).
- **F2 (endorsement):** active endorsement by groom and bride families and by the couple (phenomenology_archive.md §C4). Fails only under explicit coercion (not the modal case).
- **F3 mechanism:** M3 **trans-generational norm inheritance** — the norm floor is set by village/community and each family must meet or exceed it.
- **F4 (feedback blocked):** debt service is 20-year phenomenon; wedding "reward" is a one-day peak of social recognition; siblings' delayed marriage externalises cost forward in time.

**Differentiation from Wei-Zhang 2011 QJE** (sex ratio → aggregate savings): they test the aggregate macro consequence of sex-ratio-driven "competitive saving for sons." We test whether within the population **active endorsement of large marriage wealth transfers is associated with lower long-run welfare** — i.e., the Sweet-Trap diagnostic F1 at the micro level. Their paper is the *supply-side macro* of our story; ours is the *individual welfare* corollary.

---

## 2. Data source and empirical pivot from the design document

**Source:** CGSS 2017 (Chinese General Social Survey). File:
`/Volumes/P1/城市研究/01-个体调查/CGSS_2011-2023/CGSS2017/CGSS2017.dta`
(12,582 respondents × 787 variables.)

**Empirical pivot from the original design:**

1. **No direct "彩礼 amount" variable** exists in the publicly available CGSS 2017 release. The nearest substantive measure is the *EASS Family* ordinal item **d32** ("since marriage, have your parents helped you financially — for instance for housing or business — and how much?" 1 = yes, a lot; 2 = yes, some; 3 = no; 4 = parents deceased), plus its parallel **d33** for the spouse's parents.
   - **Interpretation:** d32 + d33 capture the direction and intensity of marriage-related intergenerational wealth transfer. In the bride-price regime this maps to what the couple received *from* parents; but even if the underlying transfer was bride-price from groom's family to bride's family, the bride's parents' onward help to the couple loads on d32 in many rural cases. The construct we test is therefore: *"intensity of marriage-related wealth transfer in either direction"* — which is the operational content of the Sweet signal in a Zahavian-runaway frame.
   - **Limitation (documented):** we cannot separate "bride-price to bride's family" from "dowry to couple" within d32/d33. This is a measurement limitation, not a conceptual one: both loadings amplify the wealth-transfer intensity at marriage.

2. **No county identifier**, only province (s41, 31 categories). The Wei-Zhang 2011 county × birth cohort sex ratio is therefore not reproducible. We substitute **province × 5-year marriage cohort sex ratio** constructed from the CGSS sample itself (n_province × cohort cells ≈ 124). This is coarser but preserves the identification logic.

3. **d-module split-sample:** only 3,093 of 12,582 respondents got the EASS Family module. This is by design (random rotation). Within those 3,093, 3,067 are married and have d32. Analytic sample: ~3,067.

4. **Cross-sectional, not panel.** The 2017 wave is the only CGSS wave carrying d32/d33. The construct's cross-time "Δ_ST = cor(R,F)_ancestral − cor(R,F)_current" is therefore estimated via a **pseudo-cohort decomposition**: marriages in 1950-1978 (pre-reform "ancestral" in the Chinese-institutional sense) vs 1990-2017 (reform-era runaway). Cohorts of ~2,000 early vs ~2,800 late in the CGSS married sample.

---

## 3. Variables

### 3.1 Primary Sweet signal (R_agent proxies)

- **r_transfer (ordinal, reverse-coded):** max of recode(d32) and recode(d33), where 1→3 (a lot), 2→2 (some), 3→1 (none), 4→missing. Range 1–3. Higher = more marriage wealth transfer.
- **r_transfer_high (binary):** 1 if either d32 = 1 or d33 = 1 ("a lot from at least one side"), 0 if both d32 ≠ 1 and d33 ≠ 1 and neither missing.

### 3.2 Sweet outcome DV (endorsement; short-term welfare)

- **happy (a36, Likert 1–5):** life happiness. Used as the primary **Sweet endorsement**: Sweet-Trap predicts higher transfer correlates with higher subjective welfare *at endorsement*.
- **marital_sat (d31, Likert 1–5, reverse-coded so higher = more satisfied):** marital satisfaction.
- **status (a43e, Likert 1–5, reverse-coded):** self-rated socioeconomic status.

### 3.3 Bitter outcome DV (F — long-run welfare)

- **life_sat (d21, reverse-coded):** overall life-situation satisfaction; conceptually the consumption-equivalent welfare in the construct. Overlaps but differs from a36 (happiness) — used here as the cooler "life as a whole" assessment.
- **happy_score (d41 0–10):** requires removal of code-0-as-missing (7,838 zeros are structural-missing tokens).
- **siblings_unmarried_share (constructed from d21_*, d22_* and d3d*):** fraction of known siblings currently unmarried given observed age. *Only computable for the subset who answered both d22 sibling counts and d3d marital statuses (n ~ 1,200–1,500).* Proxy for the sibling-λ channel.
- **kids_count (a681+a682):** number of children — constructed as a plausible long-run welfare/burden indicator; sign is ambiguous but included for completeness.

### 3.4 λ proxy — sex ratio at marriage market

- **sex_ratio_prov_cohort:** among CGSS 2017 respondents in the same province and 5-year marriage-year bin, the ratio of males to females. Constructed pre-filter to avoid endogenous selection.
- **high_sex_ratio:** 1 if sex_ratio_prov_cohort > 1.05 (sample-median-sensitive; check in sample).

### 3.5 Instrument for r_transfer (Wei-Zhang-type IV)

- **Z = sex_ratio_prov_cohort** used as instrument for **r_transfer** in 2SLS.
  - First-stage prediction: higher male surplus → more competitive wealth transfer.
  - Exclusion restriction (stated; falsification check below): sex ratio affects welfare only through marriage market channel, conditional on province FE + cohort FE. Imperfect because sex ratio is correlated with cohort-level economic development, hence province × cohort trends.
  - Falsification: placebo test on never-married (a69 = 1) — they should not be affected.

### 3.6 Controls

- age = 2017 − a3a_birth_year (from `a3a` reconstructed; or derived from `a2a1`/questionnaire year)
- sex = a2 (1 = male, 2 = female)
- educ_years = derived from a7a (education category) via standard crosswalk (illit=0; primary=6; junior=9; senior=12; college=15; graduate=18)
- hukou_rural = 1 if a18 = 1 (agricultural hukou) else 0
- log_hh_income = ln(1 + a62), winsorized at 99th pct
- province FE = s41 (31 provinces)
- marriage cohort FE = 5-year bins of a71b

---

## 4. Hypotheses (directional, one-sided, α = 0.05 uncorrected; α_Bonf = 0.01 across 5 primary tests)

- **H4.1 (Sweet):** Cor(r_transfer, happy | controls) > 0, pooled across CGSS 2017 married sample. Point-prediction |β| = 0.05–0.20 SD of happy.
- **H4.2 (Bitter, modern cohort):** Cor(r_transfer, life_sat | controls) ≤ 0 **for marriages post-1990** (reform-era). Point-prediction |β| non-positive, directional.
- **H4.3 (Δ_ST):** Cor(r_transfer, life_sat | controls)_{1950-1978} > Cor(r_transfer, life_sat | controls)_{1990-2017}. Difference Δ_ST > 0. Point-prediction Δ_ST > 0.10 (half a correlation-SD).
- **H4.4 (λ — sex ratio moderation):** β_{r_transfer × high_sex_ratio} on life_sat < 0: where sex-ratio is higher, marriage wealth transfers are associated with worse long-run welfare (the runaway intensifies).
- **H4.5 (sibling externalisation):** For male respondents with unmarried siblings, higher r_transfer in own marriage correlates with higher siblings_unmarried_share (the direct λ-channel test).

### 4.6 Secondary / exploratory
- **IV:** 2SLS of life_sat on r_transfer instrumented by sex_ratio_prov_cohort. First-stage F reported; if F < 10, flag as weak instrument and rely on OLS with caveats.
- **Specification curve:** ≥ 64 specifications varying DV (3) × covariates (4) × fixed-effects scheme (2) × sample (married vs married+age cap).

---

## 5. Sample inclusion/exclusion

1. a69 ∈ {3, 4} (initially married or remarried with spouse).
2. a71b non-missing (marriage year observable).
3. d32 or d33 non-missing (at least one of the wealth-transfer items observed).
4. 1950 ≤ a71b ≤ 2017.
5. Exclude d32/d33 ∈ {98, 99} (don't-know / refuse).
6. Age 20–90 at survey.

Expected analytic N ≈ 2,900 married respondents (after quality filters).

---

## 6. Analytic plan

1. **Descriptives.** By marriage cohort (pre-reform vs reform), show distributions of r_transfer, happy, life_sat, status.
2. **H4.1 Sweet OLS:** happy_i = β1 · r_transfer_i + X_i γ + FE + ε_i. Cluster-robust SE by province.
3. **H4.2 Bitter OLS, modern cohort:** life_sat_i = β2 · r_transfer_i + X_i γ + FE + ε_i, restricted to a71b ≥ 1990.
4. **H4.3 Δ_ST:** compute partial correlation within each cohort subsample via residualised regression (Frisch-Waugh-Lovell). Bootstrap 95% CI (B = 2,000, seed = 20260417) for Δ_ST.
5. **H4.4 λ interaction:** life_sat_i = β · r_transfer + γ · r_transfer × high_sex_ratio + δ · high_sex_ratio + X γ + FE + ε.
6. **H4.5 sibling externalisation:** siblings_unmarried_share_i = β · r_transfer_i + ..., restricted to male respondents with a682 + a681 ≥ 2 (has siblings).
7. **IV (secondary).** 2SLS, r_transfer instrumented by sex_ratio_prov_cohort. First-stage F-statistic reported with Stock-Yogo 10% critical value (F > 16.38 for one instrument, one endogenous regressor). Durbin–Wu–Hausman test for exogeneity.
8. **Specification curve (main-text robustness).** 2 Sweet DV × 2 Bitter DV × 4 control sets × 2 FE schemes × 2 cohort-sample definitions = 64 primary specs for Δ_ST-direction consistency. Report %-significant-and-consistent-sign.

---

## 7. Decision rules (anti-motivated-reasoning)

- **H4.1 Sweet confirmed** iff β1 > 0 with one-sided p < 0.01 AND specification-curve sign-consistency ≥ 75%.
- **H4.2 Bitter confirmed** iff β2 ≤ 0 with one-sided p < 0.05 in reform-era subsample AND direction holds in ≥ 60% of specifications.
- **H4.3 Δ_ST confirmed** iff 95% bootstrap CI for Δ_ST excludes 0 from below AND Δ_ST point estimate ≥ 0.05.
- **H4.4 λ confirmed** iff interaction one-sided p < 0.05 AND sign matches.
- **Falsification fallback:** if H4.1 fails (point β ≤ 0), F2 endorsement is not observed for this proxy — C4 is demoted from "Sweet Trap" to "pure Bitter" channel, mirroring D3's fate. Report honestly. If H4.3 also fails, the paper downgrades C4 to SI as a measurement-limit case.

---

## 8. Handling of the specification pivot

The original design specified county × birth-cohort sex-ratio IV + CGSS 2017/2021 panel. Audit shows:

- **Audit 1.** No county identifier in public CGSS 2017 (only province). **Consequence:** coarsen IV to province × 5-year marriage cohort. Bias direction: attenuation toward OLS if cohort-province sex-ratio is a noisy proxy for true marriage-market competition.
- **Audit 2.** No d32/d33 equivalent in CGSS 2021 (the 2021 wave replaced the Family module with a COVID-specific module). **Consequence:** no 2017 × 2021 panel merge. We rely on single-wave 2017 cross-section plus within-sample pseudo-cohort decomposition.
- **Audit 3.** d32/d33 are ordinal (4 categories) not continuous amounts. **Consequence:** treat as ordinal; do NOT log-transform. Primary specs use the numeric recoded scale (1–3); robustness uses the binary high-transfer indicator.
- **Audit 4.** Direct "彩礼 paid" vs "嫁妆 received" separation is unobservable. **Consequence:** the construct measured here is "intensity of marriage wealth transfer (either direction)", which is a more general Zahavian-runaway test, and we describe it that way in reporting.

These pivots are documented in the PDE findings document; they do NOT relax the decision rules in §7.

---

## 9. Random seed and reproducibility

- numpy.random.seed(20260417) set at top of script for all bootstrap and resampling steps.
- CGSS 2017 file SHA-256 recorded at read time and printed in the log.
- All intermediate processed data written to `02-data/processed/C4_cgss_marriage_panel.parquet` with SHA-256 check at re-entry.

---

## 10. Deliverables

1. `03-analysis/scripts/C4_marriage_market_sweet_trap.py` — end-to-end analysis script.
2. `02-data/processed/C4_cgss_marriage_panel.parquet` — analytic sample.
3. `02-data/processed/C4_results.json` — full numeric record.
4. `00-design/pde/C4_marriage_market_findings.md` — narrative PDE report.
5. `03-analysis/scripts/C4_marriage_market_sweet_trap.log` — execution log.

---

*End of C4 analysis protocol. Lock-in: yes, before running analysis.*
