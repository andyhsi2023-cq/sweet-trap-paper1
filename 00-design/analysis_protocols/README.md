# Pre-registrations README — Sweet Trap Multi-Domain Paper

**Date:** 2026-04-17 (drafts); planned OSF deposit 2026-04-20
**Paper:** "The Sweet Trap: A Cross-Domain Behavioral Equilibrium of Rational Self-Harming Endorsement"
**Target journal:** *Nature Human Behaviour*
**Authors:** Lu An & Hongyang Xi (both corresponding)

---

## 1. Purpose

This directory contains four Pre-Analysis Plans (PAPs) that collectively lock the primary analysis for the four new focal domains in the 5-domain Sweet Trap paper. The fifth domain (D1 Urban over-investment) uses the prior OSF registration from the `infra-growth-mismatch` paper; no new registration for D1.

**Critical context.** The urban paper (`infra-growth-mismatch`) was flagged in Phase-5 synthesis for three presentation vulnerabilities: "harmful" overclaiming, headline coefficient cherry-picking, and a post-hoc triple-interaction rescue of a pre-registered null (see `sweet_trap_construct.md` §6). The construct paper explicitly commits to avoid these by deposit-before-analysis pre-registration across all new focal domains. **These four PAPs are the operational expression of that commitment.** Depositing them before Stage 2 begins is the primary defense against "post-hoc narrative" reviewer attacks.

---

## 2. Document list

| File | Domain | Role | Headline H1 |
|:---|:---|:---|:---|
| `pre_reg_D3_996.md` | D3 Overwork | **Headline / abstract anchor** | Within-person: `∂ qg406 / ∂ overtime_d > 0`; `∂ qp401 / ∂ overtime_d.L1 > 0` |
| `pre_reg_D8_housing.md` | D8 Premium housing | **Second headline / positional anchor** | Within-person: `∂ dw / ∂ mortgage_burden > 0`; `∂ log(savings) / ∂ mortgage_burden.L1 < 0` |
| `pre_reg_D2_education.md` | D2 Intensive parenting | **Policy-shocked / maximum novelty** | Within-person + 双减 DID: satisfaction drops for high-baseline-tutoring households post-2021 |
| `pre_reg_D5_diet.md` | D5 Diet | **Boundary / β-mechanism illustration** | Within-person: `∂ qp401 / ∂ food_share.L1 > 0`; `∂ qn12012 / ∂ Δ food_share > 0` |

D1 (urban, already executed) re-uses `../../infra-growth-mismatch/00-design/osf_preregistration_draft.md` plus the Study-1 registration for Study 1 of that paper.

---

## 3. One-line headline predictions

- **D3 996.** Workers whose weekly hours exceed 48 report higher within-person job satisfaction contemporaneously and higher within-person chronic-disease incidence at a one-wave lag; the satisfaction response is larger for workers with a spouse and dependent children.
- **D8 Housing.** Within-person increases in mortgage-income burden raise self-rated social status contemporaneously and reduce household liquid savings at a one-wave lag; the status response intensifies among cohorts under age 40.
- **D2 Parenting.** Within-household education-expenditure share raises parental life satisfaction contemporaneously and crowds out non-education consumption at a one-wave lag; after the 2021 双减 policy, high-baseline-tutoring households show a drop in parental satisfaction relative to low-baseline households — a policy-identified confirmation that prior endorsement was contingent on the now-removed amenity.
- **D5 Diet.** Within-person lagged food-expenditure share raises chronic-disease incidence; contemporaneous change in food share raises life satisfaction — with the Sweet response pre-committed as the most likely null given CFPS measurement coarseness.

---

## 4. Cross-domain identification template (shared across all four PAPs)

All four PAPs share the same within-person fixed-effect skeleton with per-domain treatments and outcomes:

```
Primary (Sweet DV ← Treatment):
  SweetDV_{i,t} = α_i + γ_t + β₁ · Treatment_{i,t} + X·φ + ε

Companion (Bitter outcome ← Treatment_{t-1}):
  BitterOutcome_{i,t} = α_i + γ_t + β₂ · Treatment_{i,t-1} + X·φ + ε

λ-moderator:
  SweetDV_{i,t} = α_i + γ_t + β₁·Treatment + β₃·(Treatment × λ) + X·φ + ε
```

Per-domain deviations from this template:
- **D2** adds a Stage B DID using the July 2021 双减 policy shock.
- **D5** uses `Δ food_share` (first-difference) as the Sweet-side treatment instead of levels.
- **D8** adds a separate discriminant check (H8.4) to rule out income-driven misattribution.

Minimal common covariates: `age, age², eduy, household_size, log(fincome1), year`. Person FE + year FE throughout. Two-way clustered SE on `(pid, year)` for primary; robustness variants in SCA.

---

## 5. Multiple-comparison strategy

### 5.1 Cross-domain Bonferroni (primary correction)

Four pre-registered primary hypotheses (H3.1, H8.1, H2.1, H5.1 — the Sweet-endorsement first test per domain) define the primary cross-domain confirmation count. Bonferroni correction:

> **α_Bonf = 0.05 / 4 = 0.0125 (one-sided)**

This threshold applies uniformly across all three primary tests within each of the four PAPs (H_d.1, H_d.2, H_d.3) — i.e., 12 primary one-sided tests at α_Bonf = 0.0125. This is a **strict** correction: one could argue for only applying across the four "headline" Sweet tests and using Holm-Bonferroni within-domain separately, but we commit to the stricter pooled α_Bonf to forestall reviewer objections.

### 5.2 Within-domain Holm-Bonferroni

Each PAP pre-registers three primary hypotheses. Within-domain Holm-Bonferroni α_within = 0.05/3 = 0.0167 is **less stringent** than α_Bonf = 0.0125 and is therefore not the binding threshold. Reported for transparency only.

### 5.3 Secondary and exploratory

All non-primary contrasts (SCA variants, secondary DVs, placebo tests, robustness, exploratory triples) report FDR-corrected q-values (Benjamini-Hochberg) alongside raw p-values.

### 5.4 Cross-domain confirmation threshold (pre-committed)

The paper pre-commits to the **construct-level cross-domain count** as the primary evidence statistic, not individual-domain point estimates:

- **≥ 4 of 5 focal domains confirm at SCA-median level** → construct confirmed.
- **3 of 5 confirm** → partial confirmation; paper reframed as "Selective Sweet Trap operation across domains."
- **≤ 2 of 5 confirm** → construct not supported; paper downgraded or redirected.

D1 has already confirmed. Thus the four new PAPs collectively determine whether the cross-domain threshold is reached.

### 5.5 Power implications of α_Bonf = 0.0125

| Domain | Hypothesis | Expected effect | N (balanced) | Power at α_Bonf = 0.0125 |
|:---|:---|:---|---:|:---:|
| D3 | H3.1 (Sweet) | 0.10 SD | 18,000 | >85% |
| D3 | H3.2 (Bitter lag) | 0.03 p.p. | 15,000 | ~80% |
| D3 | H3.3 (λ-interaction) | 0.5·β̂₁ | subsample | ~70% |
| D8 | H8.1 (Sweet status) | 0.08 SD | 28,000 | >90% |
| D8 | H8.2 (Savings crowd-out) | −0.15 logpts | 25,000 | ~85% |
| D8 | H8.3 (Age interaction) | 0.5·β̂₁ | subsample | ~75% |
| D2 | H2.1 (Sweet parent) | 0.15 SD | 22,000 | >90% |
| D2 | H2.2 (Cons crowd-out) | −0.08 pts | 22,000 | ~80% |
| D2 | H2.3 (双减 DID) | −0.25 SD | 18,000 | ~80% |
| D5 | H5.1 (Bitter health) | 0.02 p.p. | 24,000 | ~80% |
| D5 | H5.2 (Sweet satisf) | 0.05 SD | 24,000 | ~75% |
| D5 | H5.3 (λ-interaction) | 0.5·β̂₂ | subsample | ~70% |

**Observation.** Power at α_Bonf = 0.0125 is acceptable (≥80%) for most primary-first tests except H5.2 (boundary domain, pre-committed as most likely null), H5.3, H3.3, and H8.3 (interaction tests). A positive result at α = 0.05 but p > 0.0125 is reported as "directionally consistent, under-powered at cross-domain threshold." This is honest null reporting, not a protocol deviation.

---

## 6. Falsification commitments (construct-level F1–F5)

Each PAP implements construct's falsifiability rules:

- **F1 (within-person Sweet null)**: if H_d.1 (Sweet endorsement) is null or opposite-signed, domain d is treated as boundary-condition evidence; null reported without post-hoc rescue.
- **F2 (long-run Bitter null or positive)**: if H_d.2 (Bitter welfare cost) is null or positive, domain d's "Sweet Trap" interpretation is invalidated; the pair is reframed as "Sweet without Bitter" (not a Sweet Trap).
- **F3 (λ-heterogeneity null)**: if H_d.3 fires opposite-signed or non-null for low-λ groups, construct's externalization pillar is falsified in d.
- **F4 (cross-domain uniformity)**: if ≤ 2 of 5 focal domains confirm at SCA-median level, construct not supported.
- **F5 (reversal under information)**: not tested in this paper (requires RCT-style information intervention); noted as boundary scope condition.

---

## 7. Most-likely-to-falsify hypothesis (for psychological preparation)

**H5.2** is the most at-risk hypothesis for a null result:
- `Δ food_share` is a coarse revealed-preference proxy (expenditure composition shift, not caloric composition).
- CFPS lacks specific food-category variables needed to construct NOVA-style ultra-processed-food measures.
- Expected effect size 0.05 SD sits at the lower bound of detectable in N ≈ 24,000.
- Power at α_Bonf = 0.0125 is ~75%.

**This is pre-committed as the boundary-condition finding** (see `pre_reg_D5_diet.md` §7.2). Stage 2 executors should not treat a H5.2 null as project failure. D5's role in the paper is precisely to provide a domain where null is plausible and informative, strengthening the construct's falsifiability credentials.

**Second-most at-risk:** H2.3 (双减 DID). If households' parental identity is stable and survives tutoring-removal, the policy shock mechanism claim weakens. Pre-trend check (2014, 2016, 2018 coefficients = 0) and placebo (H2.4) are the identification safeguards.

**Third-most at-risk:** H3.3 and H8.3 (interaction tests). Interaction coefficients are typically 0.5× the main effect; at α_Bonf = 0.0125 with subgroup imbalance, they are underpowered by design. A "directionally consistent, under-powered" report here is acceptable.

---

## 8. Most-likely deviations (for Stage 2 execution guidance)

Ranked by prior probability of occurrence:

1. **D2 child-module merge failure** (~60% probability): pre-specified fallback in `pre_reg_D2_education.md` §3.4. Not a deviation; child outcomes move to SI.
2. **D5 H5.2 null result** (~55% probability): pre-committed boundary-condition handling in `pre_reg_D5_diet.md` §7.2. Not a deviation; null reported as informative.
3. **D3 `qq4010` sleep mechanism underpower** (~40% probability): sleep N is small (26,880); mediation check is pre-registered as mechanism-only, not confirmatory.
4. **D8 `mortage` sparse-wave problem 2010/2012** (~30% probability): use post-2014 waves as primary; early waves as robustness.
5. **D3 `workplace` migrant λ proxy missing >60%** (~50% probability): primary λ is `lambda_family`, not migrant. Loss does not invalidate H3.3.

Stage 2 executors: keep a running deviation log per domain at `03-analysis/logs/d{3,8,2,5}_deviations.log`. Any deviation affecting a primary coefficient must be reported in main text with "deviation from pre-registration" flag; both pre-registered and deviated results reported.

---

## 9. Deposit workflow

Planned sequence for OSF deposit (2026-04-20):

1. Final review of all four PAPs against construct `sweet_trap_construct.md` §6 construct-rules (no post-hoc rescue; SCA ≥500 variants; median reporting).
2. Record analytic-data SHA256 hash for the frozen CFPS cut 2026-04-17.
3. Record Git commit hash of the `sweet-trap-multidomain` repo immediately before deposit.
4. Create OSF project "Sweet Trap Multi-Domain Evidence" with four child components (one per domain) plus one parent meta-component.
5. Deposit the four PAP files + this README as a bundle.
6. Record the returned OSF URLs back into each PAP's "OSF URL: [pending deposit]" field.
7. Write a deposit-confirmation note into `HANDOFF.md` and the parent construct doc.
8. Stage 2 (parallel domain execution) begins only after deposit is confirmed.

---

## 10. Change log

- **v0.1 (2026-04-17):** Initial drafts created (this commit). All four PAPs drafted; OSF URLs pending.

---

## 11. Related documents

- `../sweet_trap_construct.md` — v1.0 construct foundation; falsifiability rules F1–F5; construct §6 anti-rescue commitments.
- `../cfps_variable_inventory.md` — variable audit with N and missingness; sample-size expectations.
- `../domain_selection_matrix.md` — Stage 1 decision record locking the 5-domain roster.
- `../study_design_outline.md` — detailed Study-level execution plan.
- `../../infra-growth-mismatch/00-design/osf_preregistration_draft.md` — D1 (urban) pre-registration used by reference.
- `../../01-literature/literature_by_domain.md` — benchmark papers per domain (anchoring prior effect-size expectations).

---

**Sign-off:** Lu An & Hongyang Xi, 2026-04-17 drafts; deposit 2026-04-20 planned.
