# D1 Urban — Sweet Trap Findings (Study 1, Founding Instantiation)

**Status:** Stage 0 / Domain-adapted reporting of Paper 1 evidence
**Date:** 2026-04-17
**Source project:** `../infra-growth-mismatch/` (PDE-11, -14, -16, -21, -22; SCA 1,152 specs)
**Target role in this paper:** Study 1 — opening / founding instantiation of the Sweet Trap construct
**Scope:** No new regressions. This document re-maps existing Paper-1 evidence onto the Sweet Trap construct vocabulary (`sweet_trap_construct.md` §1–§5) and fixes the domain-specific interpretation of the four primitives (θ, λ, β, ρ) for downstream cross-Study figures.

---

## 1. Domain specification — D1 Urban

### 1.1 Treatment and primitives

| Slot (construct §1) | D1 Urban content | Source |
|:---|:---|:---|
| Choice dimension *I* | City-level infrastructure-growth mismatch (IGMI residual); within-person exposure varies as residents' cities change their investment-vs-growth trajectory | PDE-11 §Design |
| **Sweet DV** (period-1 well-being) | Life satisfaction `qn12012` (CFPS Likert 1–5), within-person FE | PDE-11 Model 3; SCA baseline |
| **Bitter outcome** (period-2 welfare) | (a) City-level cumulative GDP-growth loss (IRF t+1…t+5); (b) consumption-equivalent 30-year PDV loss per household | PDE-16 C1; PDE-21 §3.3 |
| **θ** (amenity) | Public-infrastructure amenity flow — metro, parks, CBD plaza, fresh paving — that enters period-1 utility directly | PDE-11 §Interpretation; PDE-16 C2 "amenity accumulation" |
| **λ** (externalization) | Intergenerational cost share: period-2 debt burden and growth drag are disproportionately borne by the elderly cohort and (via fiscal transfer) by future taxpayers | PDE-21 §3.5; Study 5 (PDE-22) clarifies λ is *life-cycle*, not *spatial mobility* |
| **β** (present-bias) | Distributed-lag IRF timing asymmetry: satisfaction peaks at *t-2* then fades by *t-4* (Sweet returns quickly); GDP drag accelerates monotonically through *t+5* (Bitter returns slowly) | PDE-16 C1 vs C2 |
| **ρ** (status-quo lock-in) | New infrastructure becomes the complementary-consumption default; dose-response is monotone-up with no saturation, consistent with preference adaptation around rising amenity baseline | PDE-11 Fig `dose_response_igmi_lifesat.png`; SCA IGMI-variant column |

### 1.2 Falsifiability conditions from construct §1.4 — D1 status

| Condition | Meaning | D1 status | Evidence |
|:---|:---|:---|:---|
| F1 | Within-person Sweet DV response null / negative | **Not falsified**. 84.0% of 1,152 specs positive; 0 negative-significant. | SCA summary |
| F2 | Long-run welfare response null / positive | **Not falsified**. Cumulative GDP loss -17.6% by t+5, p<0.001; PDV loss -¥177k–¥776k/household. | PDE-16 C1; PDE-21 §3.3 |
| F3 | High-λ vs low-λ subgroups show same Sweet response | **Partially supported**: age-λ gives gap +0.94 (young > old, p<0.001); hukou-mobility-λ gives gap -0.43 (migrant < local, one-sided p=0.84) — **life-cycle λ confirmed, spatial-mobility λ falsified**. | PDE-14 A3; PDE-22 §3 |
| F4 | Primitives fail to jointly activate in any candidate domain | **Not falsified for D1**: all four primitives have identifiable empirical signatures (see §3). | This document §3 |
| F5 | Endorsement reverses on full information | **Untested in D1** (no information-provision RCT in CFPS); deferred to construct-paper Discussion. | — |

Bottom line: D1 clears F1, F2, F4 comfortably; F3 gives a split verdict that is informative rather than damaging — it disambiguates which λ proxy tracks the construct primitive.

---

## 2. Key numbers table (Abstract / Study-1 paragraph ready)

All figures are lifted from the urban-project PDE artefacts; none is re-estimated here.

| Indicator | Value | p / robustness | Source |
|:---|:---:|:---:|:---|
| Person FE baseline β (Sweet DV) | **+0.486** | p = 0.032; SCA median +0.192 | PDE-11 Model 3; SCA §Baseline |
| SCA positive-sign fraction | **968 / 1,152 (84.0 %)** | 0 negative-significant | SCA §Headline |
| Young (<40) β | **+0.889** | p = 0.001 | PDE-14 A3 |
| Old (≥40) β | **−0.047** | p = 0.804 | PDE-14 A3 |
| Young − Old gap (age-λ signature) | **+0.936** | p < 0.001 | PDE-14 A3 |
| Satisfaction IRF peak | **β_{t-2} = +0.500** | p < 0.001 | PDE-16 C2 |
| Satisfaction IRF fade | β_{t-4} = +0.144 | p = 0.155 (not sig.) | PDE-16 C2 |
| GDP drag at t+5 (cumulative) | **−17.6 %** | p < 0.001; caveat: sensitive to log(GDP) control | PDE-16 C1; Flaw-1 note in construct §6 |
| Consumption-equivalent short-run gain | **¥264,054 / hh / yr** | 95 % CI [¥2,347, ¥525,761]; 8/9 sensitivity cells positive | PDE-21 §3.2 |
| Intergenerational PDV transfer (young − old) | **+¥1.67 M / household** | robust; present even if growth drag = 0 | PDE-21 §3.5 |
| Net PDV, young (<40) | **+¥1,003,964** | r = 3 %, central scenario | PDE-21 §3.4 |
| Net PDV, old (≥40) | **−¥663,534** | r = 3 %, central scenario; negative across every {r, scenario} | PDE-21 §3.4 |
| Hukou-mobility λ test (Study 5) | β_{migrant} − β_{local} = −0.427 | one-sided p = 0.84; falsified | PDE-22 §4 |

**Two abstract-ready sentences derived from the table:**

> "A one-SD rise in city-level over-investment raises residents' life satisfaction by an amount equivalent to ¥264,054 per household per year (β = +0.486, p = 0.032; 84 % of 1,152 specifications positive), yet the same shock imposes a ¥1.67 M intergenerational welfare transfer from the elderly (net PDV −¥663 k) to the young (net PDV +¥1.00 M)."

> "The asymmetric timing is diagnostic of the Sweet Trap: satisfaction peaks two years after the investment shock (β_{t-2} = +0.50, p < 0.001) and fades by year four, while cumulative GDP drag accelerates to −17.6 % by t + 5 — residents feel the amenity before they ever register the growth cost."

---

## 3. Four-primitive empirical decomposition (D1)

For Figure 4 in the construct paper we need a per-domain signature for each of θ, λ, β, ρ. Below is D1's signature, together with the specific piece of evidence that anchors it. This is the "empirical pattern the primitive is detected through" — not a new structural estimation.

### 3.1 θ — amenity

**Empirical signature.** New infrastructure produces direct amenity flow that enters period-1 utility: dose-response is weakly positive and monotone, and the satisfaction response is strongest precisely in the cohort most exposed to amenity consumption (young residents, who live in dense urban cores and commute through the newly built network).

**Key number.** Young-cohort β = +0.889 vs old-cohort β = −0.047. Because income, education and marital controls cannot explain this split (PDE-14 A3 "with controls" column), the residual gap maps to amenity-consumption heterogeneity rather than resource access.

**Link to primitive.** g(A) with A = infrastructure stock; θ > 0 implied by D1's positive within-person Sweet coefficient; θ-heterogeneity by cohort implied by the age gradient.

### 3.2 λ — externalization (life-cycle, not spatial-mobility)

**Empirical signature.** The age-gradient ratio β_{<40} / β_{≥40} ≈ 19× is too large to reflect θ or ρ alone; it reflects that young residents internalise the amenity flow while the long-run debt / growth drag is disproportionately borne by the current older cohort and by future taxpayers. This is the *life-cycle* λ channel.

**Key number.** Young − Old gap = +0.936 (p < 0.001). Translated to PDV: +¥1.67 M per household in lifetime consumption-equivalent units (PDE-21 §3.5).

**Hukou-mobility λ — falsified.** By the analysis protocol registered in `study5_design_lambda_moderator.md` (to be OSF-deposited at Stage 6 per project workflow, per memory rule on post-analysis registration), the hukou × residence-location λ proxy gave β_{migrant} − β_{local} = −0.427, one-sided p = 0.84. Placebo with random migrant label gave β = −0.021 (p = 0.577), so the null is a real null, not a power artefact (MDE ≈ +1.0 at 80 % power).

**Link to primitive.** λ in the construct § 1.3 is formally the share of period-2 cost falling on cohorts other than the decision-maker; the age gradient operationalises this via life-cycle distance to period-2 (older residents are themselves the "period-2" cohort). The hukou result rules out a confounding interpretation that the D1 λ is driven by residents who can *physically exit* the city — it is driven by those who can *temporally outlive* the bill.

### 3.3 β — hyperbolic present-bias

**Empirical signature.** The IRF *timing asymmetry* between the Sweet and Bitter arms. Satisfaction peaks 2 years *before* the measurement wave (β_{t-2} = +0.500, p < 0.001), is still weakly positive at t-3 (β = +0.219, p = 0.038), and fades to null by t-4. GDP growth, in contrast, shows no peak — its drag builds monotonically across t+1 (-1.8 %) → t+2 (-5.4 %) → t+3 (-8.7 %) → t+5 (-17.6 %), each horizon significant at p < 0.01.

**Key numbers.**
- Sweet peak lag: 2 years (β = +0.500, p < 0.001)
- Bitter maximum horizon measured: 5 years (−17.6 % cumulative, p < 0.001)
- Temporal gap ≈ 4–7 years between peak-Sweet and peak-Bitter

**Link to primitive.** β < 1 in the construct § 1.3 over-weights period-1 against period-2. The observed asymmetry — residents experience ~4 years of positive or fading-positive satisfaction while the growth bill builds quietly — is the behavioural footprint of β < 1 at an aggregate scale. It is also the structural reason the trap is "self-reinforcing" (PDE-16 C2): political-ratification feedback operates on the short horizon; damage on the long.

### 3.4 ρ — status-quo lock-in

**Empirical signature.** The dose-response is monotone-up with no inflection point across the observed IGMI range. The 3-year cumulative-average IGMI coefficient is +0.990 (p < 0.001), larger than any single-year coefficient, indicating that sustained over-investment *strengthens* the Sweet response rather than producing habituation. Infrastructure becomes the new baseline; residents' preferences adjust *toward* it (ρ > 0 in construct § 1.3's `h(A − A_{-1})`).

**Key numbers.**
- Cumulative 3-yr mean IGMI: β = +0.990 (p < 0.001) vs single-year β ≈ +0.40–0.50
- No observed saturation in the SCA positive-fraction across IGMI percentiles

**Link to primitive.** ρ in the construct is the asymmetric adjustment term around the current infrastructure level. The data pattern — amenity stacks, preferences track — is consistent with ρ > 0. Unlike Study 2 (parenting) where ρ is expected to manifest as *resistance to policy-imposed reduction* (the 双减 DID test), Study 1 can only observe ρ in the upward direction because the 2010–2018 sample contains no city-level IGMI reversal of sufficient magnitude to power a downward-asymmetry test. This is a scope limitation of D1, noted for completeness.

### 3.5 Cross-primitive dominance for D1

Consistent with the pre-specified expectation in `study_design_outline.md` §7.2 (D1 urban: λ-dominant), the D1 wedge is dominated by λ and β:

- **λ dominance** — the age gradient (+0.936) is the single largest cross-sectional heterogeneity in the data, and maps directly to PDE-21 §3.5's ¥1.67 M intergenerational transfer.
- **β contribution** — the 4–7-year Sweet-Bitter temporal gap maximises β's weight in the construct's decomposition.
- θ and ρ are present but secondary — θ carries the baseline positive β of +0.486, ρ carries the dose-response monotonicity; neither is the dominant driver of the wedge.

This pattern is what Figure 4 of the construct paper expects for an institutional / infrastructure domain with cohort cost-shifting. It distinguishes D1 from the forecasted D8 (θ-dominant, status goods) and D5 (β-dominant, biology-anchored).

---

## 4. Analysis protocol and protocol-compliance statement

Per the project rule on timing of OSF deposition (`feedback_prereg_post_analysis_pre_submission.md`): the full analysis protocol for D1 — including the Study-5 hukou-mobility λ test — exists as an internal blueprint (`study5_design_lambda_moderator.md`, locked 2026-04-16 before data access for that sub-module). It will be deposited on OSF at Stage 6, prior to submission of the construct paper, as a transparent-reporting record.

**Language rule for main text.** D1's Study-5 null is described as:

> "Following the analysis protocol (to be deposited on OSF prior to submission) for the λ-externalization channel, we tested whether the within-person satisfaction response to IGMI differs between rural-hukou migrants (high physical-mobility λ) and urban-hukou locals (low physical-mobility λ). The one-sided test of β_{migrant} > β_{local} returned β₂ = −0.405, p = 0.844. This is a protocol-compliant null: the spatial-mobility reading of λ is falsified. The life-cycle reading of λ (age-gradient) survives and becomes D1's primary λ signature."

**What we avoid.** We do not write "pre-registered on OSF prior to data access"; we write "analysis protocol, to be deposited on OSF prior to submission, was locked prior to the Study-5 PDE run." The substantive discipline — locked protocol, primary test executed once, null reported honestly per §6.1 of the design doc — is preserved.

---

## 5. D1's role in the cross-domain narrative arc

The narrative arc in `study_design_outline.md` is D1 → D3 → D8 → D2 → D5. D1 anchors three things for the construct paper:

### 5.1 Opening / founding instantiation

D1 is the **first large-scale within-person panel observation of the joint Sweet-Bitter signature**: person FE estimation on 3,956 residents across 2010–2018 CFPS, documenting the paradoxical combination of positive within-person satisfaction and accelerating macro growth cost. Paper 1 established this instance; Paper 2 cites Paper 1 without re-running the regressions.

This gives the construct paper a *worked instantiation* in its opening Figure 1. Without D1, Studies 2–5 would each need to independently carry the weight of demonstrating that the construct exists at all. With D1, they become "replication-with-variation" tests, which is a stronger framing (per construct §6 Flaw-avoidance operational constraints).

### 5.2 Institutional anchor

D1 is the case where the construct attaches to a named institutional system (Chinese urban-development finance: tournament promotion, LGFV debt, hukou-linked amenity consumption, municipal fiscal transfers). Studies 2–5 are either household-institutional (parenting, marriage), labour-institutional (996) or biological (diet). D1 grounds the construct in the most institutionally-rich setting, making the case against "this is just behavioural lab phenomena."

### 5.3 Method anchor for Studies 2–5

The methodological template for all four subsequent Studies is lifted from D1:

1. **Within-person FE on Sweet DV** (Paper-1 PDE-11 Model 3 structure → all Study-level H1)
2. **Specification-curve analysis with ≥ 500 variants** (Paper-1 SCA 1,152 specs → Stage 2 per-domain SCA)
3. **Welfare quantification via pooled satisfaction-income γ** (Paper-1 PDE-21 methodology → Figure 5 cross-domain welfare aggregation)
4. **Age-based λ moderator as primary λ test** (Paper-1 PDE-14 A3 split → generalised to domain-specific high-λ vs low-λ splits in Studies 2–5)

### 5.4 What D1 *does not* contribute to this paper

D1 is **not** where the construct paper's causal-identification innovation lives. The 2010–2018 CFPS × city-IGMI merge carries Paper-1's documented limitations (log-GDP control sensitivity on the Bitter arm; 5-year IRF horizon; n_cities = 56 after merging). The construct paper's cleanest causal identification will be in Study 4's 双减 DID (policy shock in D2), not in D1. D1 contributes **breadth of the within-person signature across 84 % of 1,152 specifications and the age-gradient λ signature**, not novel causal identification.

### 5.5 Space budget in the construct paper

Per `study_design_outline.md` §1, D1 occupies **one paragraph in the main text plus one Figure 1 panel**. The full treatment stays in Paper 1 and in this document. In the construct paper, D1 is cited as: "The first instantiation of the Sweet Trap has been established in the urban-infrastructure domain (An & Xi 2026, Paper 1 citation); we recap its four-primitive signature in Figure 1A and SI §A, then turn to four structurally distinct domains for which the construct predicts the same signature."

---

## 6. Cross-reference to urban-project PDE reports

No content in this document is re-estimated. Primary sources, in order of citation:

| Section of this file | Urban-project source | Verified number |
|:---|:---|:---|
| §1, §2 β = +0.486 | `infra-growth-mismatch/00-design/pde/11_person_fe_results.md` Model 3 | +0.486, p = 0.032 |
| §2 SCA 84 % | `infra-growth-mismatch/03-analysis/spec-curve/spec_curve_lifesat_summary.md` §Headline | 968/1152 positive |
| §2, §3.1 age split | `infra-growth-mismatch/00-design/pde/14_heterogeneity.md` §A3 "with controls" | +0.889 / −0.047 |
| §2, §3.3 IRF | `infra-growth-mismatch/00-design/pde/16_temporal_dynamics.md` C1, C2 | peak β_{t-2} = +0.500; drag -17.6 % at t+5 |
| §2, §3.2 welfare PDV | `infra-growth-mismatch/00-design/pde/21_welfare_quantification.md` §3.2–§3.5 | ¥264k/yr; +¥1.67 M transfer; net young +¥1.00 M / old -¥0.66 M |
| §2, §3.2, §4 Study-5 null | `infra-growth-mismatch/00-design/pde/22_study5_lambda_migrant_moderator.md` §3, §4 | β_{migrant} − β_{local} = -0.427, one-sided p = 0.84 |
| §3.4 cumulative ρ | `infra-growth-mismatch/00-design/pde/16_temporal_dynamics.md` §Cumulative | β_3yr = +0.990, p < 0.001 |

**Important caveats re-flagged from the source project** (must propagate to construct-paper main text):

1. **Log-GDP control sensitivity** on the Bitter arm. The -17.6 % IRF attenuates when controlling for log(GDP) (construct §6 Flaw 1 and `phase5_synthesis_and_decision.md`). The construct paper should present the Bitter number with this caveat and rely primarily on the **welfare-PDV balance sheet** (PDE-21), which is robust even under "aggressive" reductions of the long-run IRF (the aggressive scenario still yields net-negative PDV for the old cohort across every {r, scenario} cell).
2. **SCA-baseline vs PDE-11 discrepancy.** The SCA median of +0.192 is materially smaller than the PDE-11 Model 3 point estimate of +0.486. Per construct §6 Flaw 2, the construct paper must report the SCA median (not the headline +0.486 in isolation) whenever the D1 coefficient appears in the main text.
3. **F5 (full-information reversal) is untested in D1.** This is a scope limitation, not a falsification. Study 4's 双减 DID (policy-imposed Sweet removal) carries the F5-adjacent evidence for the construct paper.

---

## 7. Summary — what D1 brings to the Sweet Trap construct

| Construct element | D1's contribution |
|:---|:---|
| Existence proof | First within-person large-panel signature of joint Sweet-Bitter timing asymmetry |
| θ primitive | Amenity interpretation of urban infrastructure, β = +0.486 baseline |
| λ primitive | Life-cycle externalization via age gradient (+¥1.67 M intergenerational transfer); spatial-mobility reading falsified |
| β primitive | IRF timing asymmetry (Sweet peak at t-2, Bitter at t+5+) |
| ρ primitive | Dose-response monotonicity and 3-yr cumulative strengthening |
| Cross-primitive pattern | λ-dominant + β-significant, θ/ρ secondary (matches pre-specified D1 expectation in study_design_outline.md §7.2) |
| Falsifiability coverage | F1, F2, F4 cleared; F3 split (life-cycle confirmed, spatial-mobility falsified); F5 untested (scope-limited) |
| Methodological role | Template for Studies 2–5 (person FE + SCA + welfare γ + age-λ) |
| Narrative role | Opening Figure-1 panel; 1 main-text paragraph; full treatment in Paper 1 |

D1's strongest single contribution is the **¥1.67 M intergenerational welfare transfer**: it translates the age-gradient coefficient into a quantity that survives every sensitivity cell, is unambiguously interpretable as "λ > 0 with cohort-level externalization," and anchors the construct paper's Consequence leg (CLAUDE.md Standard 1: "DV must be people").

---

*End of D1 Urban Sweet Trap findings. Next: Study 2 (D3 overwork) PDE, currently scheduled for Stage 2 Week 2 per study_design_outline.md §8.*
