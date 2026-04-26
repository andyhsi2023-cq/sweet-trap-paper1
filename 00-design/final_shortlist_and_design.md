# Stage 0ε — Final Shortlist & Stage 1 Design

**Status:** Stage 0ε (terminal for Stage 0). After this, Stage 1 (data acquisition + pre-registration) begins.
**Date:** 2026-04-17
**Upstream:** `sweet_trap_formal_model_v2.md`, `phenomenology_archive.md`, `data_matching_three_layers.md`.
**Downstream:** `identification.md` (per domain), `specification-map.md` (spec curve), `causal-chain.md` (Problem→Mechanism→Consequence), OSF pre-registration.

---

## 0. Headline decision

**4 human focal domains × 8 animal cases × 3 cross-cultural checks.** Cross-species universality claim is supported by three nested evidence levels (Layers A/B/C of `data_matching_three_layers.md`), all pre-registered before Layer B regressions are run.

**Primary target journal:** *Science*.
**Fallback order (Collaboration Contract v1):** Nature main → Nature Ecology & Evolution → Nature Human Behaviour.

---

## 1. Focal domain decision matrix (humans)

Weights chosen in advance per Stage 0γ `target_journal_benchmarks.md`:
- **Construct fit** (Δ_ST + F1–F4 + F2 endorsement strength): weight 0.30
- **Data availability** (CFPS × external): weight 0.25
- **Identification strength** (natural experiment / IV present?): weight 0.20
- **Novelty** (gap matrix score, benchmark distance): weight 0.15
- **Cross-species bridge** (direct analogue to one of the 8 primary animal cases?): weight 0.10

Scores 0–10. Total / 10 gives priority ranking.

| # | Case | Construct fit (×0.30) | Data (×0.25) | Identification (×0.20) | Novelty (×0.15) | Cross-species bridge (×0.10) | Weighted | Decision |
|:-:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| C2 | 鸡娃 × 双减 DID | 9 (F1+F2+F3 all strong; C is "parent savings + child mental health") | 8 (CFPS `eexp`/`school`/`dw`, youth module merge required) | 10 (2021 policy cut is sharp; pre/post × treated/not-treated) | 9 (9/9 gap score, stage-0γ benchmarks) | 9 (direct homologue of A7 Fisher runaway — coordination game peer-inflation) | **8.95** | **Focal 1 (lead)** |
| C4 | 彩礼 × sex-ratio IV | 10 (Zahavian handicap × runaway; F3 M3 trans-generational) | 7 (CGSS 2017/2021 module + CFPS `marrige` × province-sex-ratio; already on P1) | 9 (sex-ratio IV strong, Wei-Zhang 2011 precedent) | 10 (9/9 gap score; no within-person yet in literature) | 10 (direct homologue of A7 Fisher runaway on the other branch — intergenerational cost transfer via λ) | **9.15** | **Focal 2** |
| C11 | Sugar/fat/salt × CHARLS biomarker | 8 (classical Lieberman mismatch; F2 endorsement sometimes borderline clinical) | 9 (CFPS `food`/`qp401`/`health` + CHARLS HbA1c/BP/BMI) | 6 (no sharp policy cut in CFPS window; rely on Allcott-Lockwood-Taubinsky 2019 sugar-tax meta for P4) | 6 (strong prior literature — Nolan 2017 *Science*, Lieberman 2013) | 10 (direct homologue of A5 Drosophila sugar + A3 plastic-ingestion Route B — the canonical mismatch example) | **7.90** | **Focal 3** |
| C1 | 打鸡血 × tech-layoff cohort | 9 (the paradigmatic F2-endorsed case; distinguishes from D1 996 as textbook) | 6 (CFPS `qg405`/`qg406`/`qn12016` good, but layoff cross-walk requires supplementary data) | 7 (layoff timing quasi-exogenous from worker's view, but identification needs roster cross-walk) | 8 (no formal Sweet Trap test; 996 literature treats coerced not endorsed) | 7 (analogue to A6 Olds-Milner direct reward hijack, weaker than C4's Fisherian homologue) | **7.45** | **Focal 4 (conditional on data-supplement decision)** |
| C5 | Luxury/conspicuous consumption | 7 (clean F1+F2; F3 universal) | 7 (CFPS composite: `dress`+`eec`+`durables_asset` usable) | 4 (no natural experiment) | 5 (strong prior lit — Heffetz 2011, Bertrand-Morse 2016) | 7 (homologue of A4 Tinbergen supernormal stimulus) | **5.85** | **Tier 2 — SI only** |
| C13 | Status housing | 7 (clean F1+F2+F3) | 8 (CFPS `resivalue`+`mortage`+`dw`+`savings`) | 5 (school-district policy variation exists in specific cities) | 5 (prior lit — Fang 2016) | 6 (homologue of A4 supernormal; overlaps with C5) | **6.45** | **Tier 2 — SI or as companion paper** |
| Others (C3, C6, C7, C8, C9, C10, C12, C14, C15, C16) | See `data_matching_three_layers.md` §B.1 | Various | CFPS insufficient | Various | Various | Various | N/A | **Excluded from focal; appear in 27-case Table 1 only** |

### Interpretation of the ranking

- **C4 彩礼 tops the ranking** because it is the cleanest human analogue of Fisher runaway with a macro-identifiable driver (sex-ratio) and a trans-generational cost externalisation (λ) that Layer 1's animal F7 does not possess. It is the paper's "quantitative Zahavi-fails" case and is what makes the cross-species parallel convincing.
- **C2 鸡娃** is the policy-aligned lead case: 双减 was 2021, CFPS 2022 wave is post-policy, and the DID is the paper's cleanest within-species identification.
- **C11 diet** is the Lieberman-mismatch baseline; biomarker grounding (CHARLS) makes the "well-being vs welfare" paradox quantifiable at clinical scale.
- **C1 打鸡血** is conditional: if the tech-layoff roster cross-walk is achievable (Fork #4), it becomes Focal 4 and delivers the paper's most striking "endorsement shattered by events" case. If not, demote to SI and expand C4/C5/C11 coverage.

### Why we did *not* pick 996, housing-as-focal, or single-internet

- **996** fails F2 at the definition level (Stage 0α §D.1).
- **Housing (C13)** is a Sweet Trap but does not map to the "three scales, one mechanism" Figure 2 narrative as cleanly as the Fisher-runaway × 鸡娃 pairing. Keeping it in Focal would dilute the narrative arc. Retained in SI for generalisability robustness.
- **Pure internet/short-video (C12)** is over-studied (Allcott 2020, Braghieri 2022) and CFPS lacks the needed platform detail. Cited, not replicated.
- **Luxury (C5)** is a Sweet Trap but is well-covered by Heffetz, Bertrand-Morse, and the status-consumption economics literature; our marginal contribution would be small.

---

## 2. Animal case shortlist (Layer A)

Fixed from `data_matching_three_layers.md` §A.2. Restated here for completeness:

| # | Case | F1 route | F3 mechanism | Δ_ST unit | Primary Nature/Science source |
|:-:|:---|:---:|:---:|:---|:---|
| 1 | Moth/artificial light | A | M4 | mortality/exposure-hour | Fabian 2024 + Swaddle 2015 |
| 2 | Sea-turtle hatchling | A | M4 | ocean-reach proportion | FWC 1995–2022 panel |
| 3 | Plastic ingestion | B | M1+M4 | ingestion × gastric mortality | Santos 2021 *Science* |
| 4 | Drosophila sugar | A | M1 | preference × lifespan Δ | Libert 2007 *Science* |
| 5 | Olds-Milner self-stim | B | M1 | lever-press × fitness Δ | Olds & Milner 1954 + replications |
| 6 | Peacock runaway | A | M2 | ornament × survival cost | Andersson 1982 + Kokko 2002 |
| 7 | Ecological/road trap | A | M1+M2 | preference × fitness Δ | Schlaepfer 2002 + Robertson-Hutto 2006 + Horváth 2009 |
| 8 | Neonicotinoid bees | B | M1+M2 | preference × colony output | Woodcock 2017 + Rundlöf 2015 + Linguadoca 2024 |

**Backup pool** (if any primary source turns out to lack open data after further audit): A8 Zahavi failure (guppy, *Science* 2023 ade5671), A11 supernormal (*Nature* 2025 09216). Target: always 8 primary + 2 backup.

**Deliverable:** SI Appendix C, one 15-page meta-synthesis; pre-registered before Layer B is run.

---

## 3. Cross-cultural shortlist (Layer C)

Fixed from `data_matching_three_layers.md` §C.4:

| Data | Module / Wave | Focal case coverage | Deliverable |
|:---|:---|:---|:---|
| **ISSP Family 2012 + 2022** | bride-price, dowry, wedding-cost items | C4 彩礼 | Country-level Σ_ST map (~40 countries) |
| **ISSP Work Orientations 2015** | aspirational work values | C1 打鸡血 | Country-level aspirational-work scale × Σ_ST |
| **WVS Wave 7 (2017-2022)** | life satisfaction (A008), materialism (E016), religion (F034), food security (Cantril ladder proxy) | C11 diet, C2 education aspiration, C5 status | ~80-country universality check |
| **ESS Rounds 8–11** | European within-region robustness | All 4 focal | Secondary robustness |

**Minimum interpretable cross-cultural test:** P3 prediction (τ_env / τ_adapt predicts Σ_ST) across ≥ 30 countries for ≥ 2 focal domains. This is the bar for "Science-level universality."

---

## 4. Each focal domain as a Sweet–Bitter–λ–Identification triple

### C2 鸡娃 × 双减 DID

- **Sweet signal (R_agent):** parental status pride + anticipated child success. Proxies: `dw` (self-rated social status, N=83,991, Likert 1–5), `qn12012` (parent life satisfaction). Secondary: `qn10021` (trust in parents — child's side).
- **Bitter outcome (F):**
  - Short-run parent: savings reduction (`savings`, `cas`); `house_debts` increase.
  - Long-run parent: life-satisfaction reversal 5-10 yr post-investment; proxied by `qn12012` within-person slope.
  - Child welfare: requires CFPS youth module merge (family × child year). Target variables: child CES-D (if available in youth questionnaire); child sleep; child GPA proxy.
- **λ proxy:** `child_num` > 0 (required filter); `child_gender` (heterogeneity); urban × provincial-tier × household-disposable-income rank. Cost externalisation = child welfare reduction not felt by parent at decision time.
- **Identification:** 2021 July 双减 policy × treatment intensity (pre-policy tutoring share of income). DID on `pid × year`. Parallel-trends test on 2014–2020 waves.
- **Registration (pre-OSF):** spec curve of 128+ specifications (2 DV × 4 outcome-window × 4 controls × 4 fixed-effects schemes × 2 robust standard errors).

### C4 彩礼 × sex-ratio IV

- **Sweet signal:** family honour + successful marriage completion + groom family status gain. Proxies in CGSS 2017: wedding-cost satisfaction (A58 series); life-satisfaction (A36). In CFPS (partial): marital transition × `dw`.
- **Bitter outcome:**
  - Groom family: 20-year debt service (`house_debts` + `nonhousing_debts`); savings depletion; delayed daughter's marriage (intergenerational λ).
  - Bride family: dowry commitment; daughter economic vulnerability.
  - Sister-of-groom: delayed/non-marriage (the classic λ-externalisation case).
- **λ proxy:** sex ratio at marriage age × county; family sibling composition; groom-family rural vs urban.
- **Identification:** sex-ratio IV (Wei & Zhang 2011 *JPE* precedent) × within-family panel on bride-price trajectory. CGSS 2013 × 2017 × 2021 panel cross-walk.
- **Cross-cultural:** ISSP Family 2022 bride-price × dowry prevalence — test if χ-correlated Σ_ST across Africa, South Asia, China, MENA.

### C11 sugar/fat/salt × CHARLS biomarker

- **Sweet signal:** gustatory-reward-driven consumption preference. Proxies: `food` expenditure; in CHARLS — self-reported eating frequency for sweetened drinks, red meat, processed foods.
- **Bitter outcome:**
  - Short: `health` self-rating; `qp401` chronic disease onset; `mexp` medical expenditure increase.
  - Long (biomarker-grounded via CHARLS): HbA1c ≥ 6.5 (diabetes); BP ≥ 140/90 (hypertension); BMI > 28 (obesity by Chinese criteria).
- **λ proxy:** medical-insurance status (`medsure_dum` = 1, cost externalised to public insurer) — direct test of Proposition 2.
- **Identification:** within-person FE on `food` × `qp401` in CFPS; panel replication in CHARLS 2011/2013/2015/2018/2020 with biomarker outcomes. Policy cross-sectional: provincial sugar-tax or trans-fat-ban natural experiments (several Chinese cities post-2019).
- **Cross-cultural:** WVS Wave 7 × food-security × life-satisfaction; plus global sugar-tax DID meta-review (Allcott-Lockwood-Taubinsky 2019 extended with post-2020 country data).

### C1 打鸡血 × tech-layoff cohort (conditional)

- **Sweet signal:** anticipated promotion / equity / mission fulfilment. Proxies: `qg405` (promotion satisfaction); `qg406` (overall job satisfaction); `qn12016` (future confidence); new variable if layoff cohort data cross-walked: self-reported IPO expectation.
- **Bitter outcome:** post-layoff life-satisfaction crash (`qn12012`); health deterioration (`health`, `qp401`); financial depletion (`savings`, `nonhousing_debts`); partner / family dissolution (`marrige` transitions).
- **λ proxy:** dual-income household (partner income → tenure cost externalised); mortgage status (sunk cost).
- **Identification:** layoff timing as quasi-exogenous shock. Cross-walk via CFPS `qg` self-reported job-change reason × industry codes × post-2022 wave. If cross-walk successful, DID on layoff vs retained cohort.
- **Decision point (Fork #4):** If CFPS `qg` self-report insufficient, Andy to decide (a) scrape Maimai + LayOffs.fyi for firm-level layoff timing and match to CFPS via industry × province + firm size, or (b) demote C1 to SI and expand C5 housing/luxury as Focal 4.

---

## 5. Proposition-to-focal-domain coverage matrix

A Stage 1 pre-registration must show each of P1–P4 is tested on at least one focal domain and at least one animal case.

| Proposition | Animal test cases | Human test cases | Cross-cultural test | Pass / Fail criterion |
|:---|:---|:---|:---|:---|
| P1 Endorsement–fitness paradox | All 8 primary animal cases | All 4 focal | WVS Wave 7 life-sat × self-reported engagement | ≥ 5/8 animal + ≥ 2/4 human show within-person Cor(R_agent, F) ≤ 0 |
| P2 λ amplifies Σ_ST | A7 peacock (ornament cost asymmetry) + A10 neonic (colony-level externalisation) | C2 鸡娃 (child-welfare cost), C4 彩礼 (sibling), C11 diet (insurance) | ISSP Family 2022 × sex-ratio-bride-price | Σ_ST is monotone increasing in λ in ≥ half of tested domains |
| P3 τ_env / τ_adapt trigger | All 8 animal cases with Δt-since-signal-emergence | C11 diet (nutrition transition, 25 yr China vs 100+ yr UK) | Cross-country WVS × time-since-phenomenon | negative Σ_ST vs (τ_env/τ_adapt) slope across cases |
| P4 Exposure > belief interventions | A1 moth (light abatement) + A10 neonic (pesticide reg) + A4 beetle (bottle-colour) | C2 双减 (exposure intervention); compare to parenting-advice campaigns | Global sugar-tax meta-review | Exposure-policy effect > belief-policy effect in ≥ 3 of 5 comparisons |

---

## 6. Stage 1 timeline (parallelised, ~3 months)

Built on `data_matching_three_layers.md` §D.

### Month 1 (S1.1 — foundation)
- Week 1–2: OSF pre-registration of Layers A/B/C protocol (immutable before data touch).
- Week 1–4: **Parallel** (a) Layer B CFPS re-derivation for C2, C5, C11, C1; (b) Layer A animal-case compilation (Santos 2021, Woodcock 2017, FWC turtle data); (c) ISSP download + harmonisation.

### Month 2 (S1.2 — identification)
- Week 5–6: C2 双减 DID — pre/post × treated/not, parallel-trends test.
- Week 5–6: Layer A Δ_ST harmonisation + forest plots for P1, P3, P4.
- Week 7–8: C4 彩礼 CGSS integration + sex-ratio IV + CGSS × CFPS cross-walk.
- Week 7–8: Layer C cross-country regressions (P3, P4).

### Month 3 (S1.3 — synthesis)
- Week 9–10: C11 diet CHARLS biomarker merge + FE regressions.
- Week 9–10: CFPS youth module merge for C2 child-outcome.
- Week 11–12: Joint spec curve (`specification-map.md`) — all 4 focal × all layers; figures 1–5 drafts.

End of Month 3 deliverable: **complete empirical results package + Results draft v1**, per Andy's 2026-04-16 target on the companion project.

### Critical path

The critical path runs through C4 彩礼 CGSS integration (8 days × 1 analyst) because it has the most data-engineering risk and is conceptually the strongest case. Assign earliest.

---

## 7. Risk register — which focal is most likely to return null?

| Risk | Prior probability | Mitigation |
|:---|:---:|:---|
| **C11 diet returns null on P1** (within-person FE on `food` × chronic disease) | 15–20 % (literature is very strong; null unlikely) | CHARLS biomarker fallback preserves P1 even if CFPS noisy. |
| **C2 鸡娃 double-减 DID has weak first stage** (policy was partially rolled-back after 2022) | 25 % | Pre-registered heterogeneity cuts (urban × tier × pre-period intensity); test on sharper 2021 initial window. |
| **C4 彩礼 IV fails first-stage** (sex-ratio × bride-price gradient may have flattened post-2018 as one-child cohort aged out) | 20 % | Use historical sex-ratio (census 2000, when cohort was born) as a Bartik-style exposure IV rather than contemporaneous sex ratio. |
| **C1 layoff cross-walk infeasible** (CFPS self-report + Maimai scrape both return noisy data) | 40 % | Fork #4 contingency: demote to SI, expand C5 housing/luxury to Focal 4. |
| **Layer C shows heterogeneity too large for universality claim** (P3 slope within 95 % CI of zero) | 25 % | Soften claim to "universal mechanism with cultural moderation"; keep paper publishable at NE&E or NHB even if Science declines. |
| **Layer A Δ_ST heterogeneity too large to pool** (I² > 90%) | 30 % | Report as heterogeneous by design; use meta-regression on F1 route (A vs B) × F3 mechanism (M1-M4) to explain heterogeneity rather than pool it away — this is Hunter-Schmidt style, acceptable in Nature/Science. |

**Highest overall risk: C1 layoff cross-walk** — 40 % chance of infeasibility forcing a structural change in Focal 4. This is why C1 is *conditional* not confirmed.

**Second-highest risk:** Layer C universality claim softening — 25 %. But a softened universality claim is still publishable at Science with the right framing ("universal mechanism with cultural moderation"), so not fatal.

---

## 8. Supplementary data requests summary

Per `data_matching_three_layers.md` §B.4, consolidated here for Andy's one-shot decision:

| Supplement | Project value | Cost / effort | Recommended? |
|:---|:---|:---|:---:|
| **CGSS 2017/2021 bride-price module integration** | Critical for C4 Focal 2 | On P1 already; 8 days engineering | **Yes — required** |
| **CHARLS 2015/2018 biomarker merge** | Transformative for C11 Focal 3 | On P1 already; 5 days engineering | **Yes — required** |
| **CFPS youth module cross-table merge** | Necessary for C2 child-outcome half | In CFPS but separate table; 5 days engineering | **Yes — required** |
| **Tech-layoff roster cross-walk for C1** | Enables C1 Focal 4 | Options: (a) CFPS self-report only; (b) Maimai / LayOffs.fyi scrape 2022–2024 | **Fork #4 — Andy decides.** Claude recommendation: try (a) first (zero new data cost), escalate to (b) only if (a) yields N_treated < 500. |
| **ISSP + WVS download** | Layer C minimum viable | Open data; 5 days download + harmonise | **Yes — required** |
| **ESS Rounds 8–11 download** | European robustness | Open data; 3 days | **Yes — required** |
| **Gallup World Poll** | Additional cross-cultural leg | License; substantial cost | **No, defer** (only if Science reviewer demands) |
| **Platform webscraping for C3 livestream** | Enables C3 as possible Focal | Engineering + legal risk; 20+ days | **No** — C3 remains out of focal; covered by Discussion + cross-species Table 1. |

---

## 9. What a successful Stage 1 looks like

By the end of Stage 1 we should have:

1. **Layer A** — 8-case quantitative narrative synthesis with forest plots for P1, P3, P4; OSF-pre-registered; submitted as SI Appendix C.
2. **Layer B** — 4 focal-domain within-person (or within-family) FE regressions with spec curve (~500 specifications each); figures for the Results main text.
3. **Layer C** — cross-cultural regressions across ~40–80 countries for P3 and P4; figure for universality check.
4. **Integration figure (Figure 5)** — Σ_ST across all 27 cases with animal and human cases on the same scale; the paper's keystone visual.

**Readiness gate before submission:** (i) all spec curves show the sign of the effect is direction-consistent in ≥ 75 % of specifications per focal; (ii) at least 3 of 4 focal domains have p < 0.05 under the pre-registered primary specification; (iii) Layer A meta shows positive pooled effect with I² reported honestly; (iv) Layer C shows ≥ 30-country coverage with slope of the correct sign.

If all four gates are passed, submit to Science.
If 3/4 passed, submit to Nature main with focus shifted to the strongest three focals.
If 2/4 passed, submit to NE&E with the focus narrowed to the two strongest.
If ≤ 1/4 passed, we are at NHB grade and the paper falls back to the original domain-scope.

---

## 10. Files produced by Stage 0ε

- `00-design/final_shortlist_and_design.md` (this document) — authoritative focal/animal/cross-cultural list.
- `00-design/data_matching_three_layers.md` — full three-layer data matching protocol.
- (to be created in Stage 1) `00-design/identification.md` — one-pager per focal domain, identification strategy in one sentence.
- (to be created) `00-design/specification-map.md` — the spec-curve design.
- (to be created) `00-design/causal-chain.md` — Problem → Mechanism → Consequence.

Proceed to Stage 1 with this final shortlist unless Andy vetoes C1 or demands additional focal domains.

---

*End of Stage 0ε Final Shortlist & Design. Stage 0 complete.*
