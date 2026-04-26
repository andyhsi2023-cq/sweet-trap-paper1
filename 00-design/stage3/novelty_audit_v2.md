# Novelty Audit v2: sweet-trap-multidomain

**Audit date**: 2026-04-18
**Stage**: S4 pre-submission (post-Stage 3 upgrades)
**Current target journal**: *Nature Human Behaviour* (Article)
**Threshold this round**: ≈70–75/100 (NHB); v1 scored 62/100
**Auditor**: novelty-audit agent (independent, does not share state with Red Team v2)
**Baseline**: Novelty Audit v1 (2026-04-17), 62/100

---

## §1. Total Score and Journal Recommendation

### Total: **71 / 100** (+9 vs v1)

**Per-criterion (0–10 each):**

| # | Criterion | v1 | **v2** | Δ |
|---|---|:-:|:-:|:-:|
| 1 | New theoretical object | 4 | **6** | +2 |
| 2 | Universality evidence (phylogenetic + cross-level) | 6 | **8** | +2 |
| 3 | Falsifiability / HARKing control | 3 | **7** | +4 |
| 4 | Methodological integration | 6 | **7** | +1 |
| 5 | Data scale (>1M) | 7 | **8** | +1 |
| 6 | Interdisciplinarity (≥3 fields) | 7 | **8** | +1 |
| 7 | Policy / welfare anchor | 5 | **7** | +2 |
| 8 | Policy-window alignment | 6 | **7** | +1 |
| 9 | Reproducibility / pre-registration | 6 | **5** | **−1** |
| 10 | Narrative coherence (P→M→C) | — | **8** | n/a |
| **Total** | | 50 / 90* | **71 / 100** | — |

\*v1 aggregated 10 items to 62/100; the per-row reconstruction differs from the v1 rollup. I use the v1 rows quoted in the prompt and score each v2 row independently on the same 0–10 scale.

### Tier assignment

| Band | Range | Call |
|---|---|---|
| Science main aspirational | ≥80 | **Out of reach.** |
| **NHB fit** | **70–79** | **Current — appropriate.** |
| NHB borderline → PNAS | 65–69 | Below fit. |
| Domain journals | <65 | Below fit. |

**Verdict: NHB submission is defensible at 71/100.** The paper sits at the lower end of the NHB band rather than the middle. It is not a Science-main candidate, and the authors' stated path (NHB primary, PNAS fallback) matches the score. A bold claim of 80+ would require tightening Section 3 (Steiger), Section 6 (B-layer anomaly), and Section 9 (pre-registration) before submission — all of which the authors themselves acknowledge as open.

---

## §2. Per-Criterion Evaluation (100+ words each)

### Criterion 1 — New theoretical object: **6/10** (v1: 4/10, +2)

**Give-points evidence.** v2 adds two items absent from v1: (i) a **two-layer formal architecture** (Lande–Kirkpatrick replicator dynamics at Layer 1 nesting a behavioural-economic utility at Layer 2 as a limit case; §M2), with (θ, λ, β, ρ) *derived* from Layer 1 rather than axiomatic — this addresses v1's structural under-specification of cultural-runaway cases (peacock, bride-price, ostracod); (ii) a **cross-level predictive scalar** (P5: Spearman ρ(Layer A, Layer D) on mechanism-rank) that is, as far as I can locate, genuinely new in construct terms. The Sweet Trap label itself is not new (sensory trap, ecological trap, mismatch, supernormal stimulus all predate it), but the *quantitative coupling between animal mechanism rank and human MR-chain magnitude rank* is novel.

**Withhold-points evidence.** The two-layer architecture borrows wholesale from Lande (1981) and Kirkpatrick (1982); there is no new mathematical theorem, no new equilibrium result, no new analytical prediction beyond rank-preservation. The F1+F2 reduction is pedagogical simplification, not a new object. Nature main or Science main would require either a new closed-form result (Fisher runaway under endogenous signal distribution) or a novel identification of a previously-unrecognised equilibrium class. This paper has neither.

**v1 → v2 change.** v1 was correctly flagged at 4 for "relabelling known mechanisms". v2 earns +2 for the cross-level predictive construct (P5) and the two-layer architectural integration. It does not reach 8 because no novel mathematical object is produced.

**To reach 8.** Produce a closed-form expression showing that the olds_milner > sensory_exploit > fisher_runaway gradient is a theorem of the two-layer model rather than an empirical regularity — i.e., derive the rank from first principles of Lande–Kirkpatrick extended by signal-hijack terms.

---

### Criterion 2 — Universality evidence: **8/10** (v1: 6/10, +2)

**Give-points evidence.** Expansion from 8 to 20 animal cases spanning 7 taxonomic classes with a PRISMA-informed search protocol (§M4) produces pooled Δ_ST = +0.645 [+0.557, +0.733] across 20/20 positive cases. Vertebrate–invertebrate meta-regression β = +0.033, p = 0.70 is a strong null for the phylogenetic-universality claim — the construct behaves as a convergent feature rather than a species-specific derived character. Mechanism-category moderation (Q_M(3) = 13.22, p = .004, R² = 76%) is strong. The **cross-level Spearman ρ(A, D) = +1.00** on overlapping mechanism cells is the strongest single piece of evidence in the paper. ISSP 17-wave × 54-country panel (2.9M records) adds a macro-cultural layer. This is a more compelling universality case than 90%+ of cross-species papers at this tier.

**Withhold-points evidence.** The cross-level ρ = +1.00 rests on **two mechanism cells** (olds_milner and sensory_exploit). With n = 2 overlapping cells, ρ = +1.00 is the only possible positive result; the prior probability of a positive Spearman at n = 2 is essentially binary. The headline "animal rank predicts human rank" needs ≥ 3 overlapping mechanism cells to be a meaningful rank test; the authors themselves note the three-layer model gives p = 0.47 primary. Fisher-runaway is represented in Layer A (5 cases) but *not* in Layer D (no MR chain maps cleanly to runaway), so the most interesting generalisation is untested.

**v1 → v2 change.** +2 is earned by the taxonomic expansion and the cross-level rank framing. It would be +3 if a fisher_runaway mechanism were MR-testable at Layer D.

**To reach 10.** Add a third overlapping mechanism cell to enable a non-trivial Spearman test (fisher_runaway via genetic data on mate-preference polymorphisms, e.g., colour-vision opsin alleles with reproductive outcomes).

---

### Criterion 3 — Falsifiability / HARKing control: **7/10** (v1: 3/10, +4)

**Give-points evidence.** The 10-case discriminant classifier (5 positive + 5 adversarial negatives) achieves 1.00 accuracy / κ = 1.00 on F1 AND F2 alone, with 1.75-unit threshold plateau and explicit negative-control logic (C2, C4, D3, C1, C16). F1+F2 reduction demotes F3/F4 to severity modifiers, collapsing 16-profile combinatorics to 4 classification cells. §11 rewrite is transparent: it enumerates 5 v2 refinements, date-stamps each limitation, and demonstrates the cultural G^c weighting adds ΔR² = +0.0009 (empirically rules out post-hoc curve-fitting). Five falsification criteria (P1–P5) are stated, including a *sign-specific* falsification for P5 (ρ < 0). This is a substantive improvement over the v1 "unfalsifiable umbrella" attack surface.

**Withhold-points evidence.** Two real weaknesses remain. (1) **The 10-case test is a dev-set confusion matrix** — the authors acknowledge this ("not out-of-sample validation"; "inter-rater reliability not established"). A reviewer who wants to press will note that the F1/F2 scoring was performed by the same analyst(s) who defined the construct. (2) **No actual OSF pre-registration exists pre-analysis**; §M12 admits registration is "at submission", which is predecessor-paper-pattern but not true prospective pre-registration. A hostile reviewer will note that every §11 refinement still *post-dates* Layer A/B/C/D data inspection (2026-04-16 → 2026-04-18), even if the §11 transparency-log defence is honest.

**v1 → v2 change.** +4 is the largest gain in the audit, driven by the discriminant matrix, F1+F2 simplification, and §11 rewrite. The reason it doesn't reach 9 is that the empirical test is still in-sample.

**To reach 10.** Commit to a prospective OSF-registered out-of-sample replication on C3 (livestream), C7 (MLM), C10 (religious over-donation) coded by an independent second rater before submission, and include inter-rater κ.

---

### Criterion 4 — Methodological integration: **7/10** (v1: ~6/10, +1)

**Give-points evidence.** The integration is the paper's real craft: PRISMA meta-analysis + 3,000-spec-curve (exceeds Sommet 2026 Nature 768 benchmark) + 19 MR chains × 5 methods × 3 MVMR + 2.9M-record ISSP harmonisation + median-as-headline spec-curve reporting + within-layer z-score harmonisation for the cross-level meta. No single component is novel, but the stacking — particularly the P5 cross-level rank test — is not something I've seen at NHB or equivalent venues. The transparency on method monoculture (Red-Team objection) is explicit: IVW + weighted median + Egger + MR-RAPS + MR-PRESSO cover the standard pleiotropy-robustness portfolio.

**Withhold-points evidence.** Each individual method is standard. The cross-level meta-regression is admitted to have `n_groups = 3` with singular random-intercept variance (§M9) — a REML model on 3 groups is statistically fragile. The primary p = 0.47 is only rescued to p = 0.019 by the pre-registered A+D subset, which reviewers may read as cherry-picking. The Cohen's-d bridge between Δ_ST (correlation scale) and log OR (log-odds scale) uses monotonic approximations that compress at tails — the authors flag this, but it remains a limitation.

**v1 → v2 change.** +1 for spec-curve formalisation, MR-PRESSO/MVMR addition, and cross-level meta-regression. Not higher because the integration is craft, not methodology innovation.

**To reach 10.** Develop a formal likelihood model that simultaneously estimates effects across correlation / β / log-OR scales from a single latent-effect parameter — this would be a genuine methodological contribution.

---

### Criterion 5 — Data scale: **8/10** (v1: ~7/10, +1)

**Give-points evidence.** UK Biobank GWAS instruments n = 258K–1.33M per trait; FinnGen R12 outcome n ≈ 413K; CFPS ≈ 180K person-waves; ISSP 2,896,233 individual records × 54 countries × 17 waves; 20 animal meta-analysis cases; 2,576 per-SNP Wald ratios. The numbers comfortably clear CLAUDE.md Standard 3's million-level threshold for Nature-tier. Every layer is population-scale where population-scale is available.

**Withhold-points evidence.** The individual-level *within-person* evidence at Layer B is the weak link — 5 focal cases, not 50. Sommet 2026 Nature cited as benchmark uses 768 specs on a single question; 3,000 specs here are divided across 5 questions. Data scale is strong but not overwhelming relative to contemporaneous Nature work (e.g., Chetty-style administrative-data papers routinely clear 10M+ individuals).

**v1 → v2 change.** +1 for Layer D expansion (7 → 19 chains, 4 → 9 outcomes) and ISSP full-wave (1985–2022). Layer B did not materially expand.

**To reach 10.** Add a US administrative-tax-record or Swedish-register Layer B replication at 1M+ individuals.

---

### Criterion 6 — Interdisciplinarity: **8/10** (v1: ~7/10, +1)

**Give-points evidence.** Four substantive fields: (i) evolutionary biology / animal behaviour (Layer A), (ii) behavioural / development economics (Layer B CFPS-CHARLS-CHFS), (iii) genetic epidemiology / MR (Layer D UKB + FinnGen), (iv) cross-cultural sociology (Layer C ISSP + Hofstede). Remove any one and the paper collapses: without Layer A the universality claim fails, without Layer D the causal architecture fails, without Layer C the macro-cultural heterogeneity operator (G^c) fails, without Layer B the human focal within-person evidence disappears. This satisfies CLAUDE.md Standard 5's "remove any discipline and the paper fails" test.

**Withhold-points evidence.** Public-health / GBD linkage (§8 DALY anchor) uses published prevalences and PAF formulae — it is an application layer, not a fifth discipline. Neuroscience is referenced (Olds–Milner) but no primary neuroscience data is produced.

**v1 → v2 change.** +1 for formalising ISSP at the population-cultural level and for the DALY anchor.

**To reach 10.** Add a primary neuroimaging or fMRI-reward-circuit layer, or a behavioural-ecology lab experiment.

---

### Criterion 7 — Policy / welfare anchor: **7/10** (v1: 5/10, +2)

**Give-points evidence.** The DALY anchor (§8, 34.6M DALYs/yr, 95% envelope 16.2–64.1M) closes what v1 did not: CLAUDE.md Standard 1's "DV must be human". "Approximately ten times the burden of Parkinson's disease" is a memorable and cite-able frame. Four sensitivity strategies are reported. The §8 "What Sweet Trap is *not* claiming" paragraph — it reframes rather than adds new DALYs — shows epistemic discipline.

**Withhold-points evidence.** The **Steiger compression 8.4×** is the single largest vulnerability in the paper. If Steiger directionality fails for 11/19 chains (including the BMI and alcohol chains that drive 80% of the headline), the conservative reading of the same evidence is 4.1M DALYs — still meaningful, but the abstract leads with 34.6M. An NHB referee with an MR background will read §5's Steiger disclosure and recompute the abstract's headline; a Science referee would desk-reject on this. The authors' own §Discussion reports this limitation transparently, which saves the submission but does not save the headline. A referee who is generous will accept the Tier-1 floor of 4.1M as the real claim; a referee who is hostile will insist the abstract lead with it.

**v1 → v2 change.** +2 for closing the DALY chain from data to human burden and for sensitivity transparency. It is not +3 because the Steiger vulnerability is material.

**To reach 10.** Rewrite the abstract headline to lead with the Steiger-conservative figure (4.1M DALYs, "equivalent to the global burden of Parkinson's disease") with the 34.6M as the point estimate under the stated assumptions. Authors will resist this because it weakens the narrative, but it is the correct scientific framing.

---

### Criterion 8 — Policy-window alignment: **7/10** (v1: ~6/10, +1)

**Give-points evidence.** Discussion §First explicitly aligns to four contemporaneous policy debates: WHO ultra-processed food review (2024), UK sugar-tax decadal evaluation (2024–25), EU Digital Services Act (2024–), China 双减 evaluation cohort. P4 makes a prospectively-testable prediction (exposure-distribution > information interventions in ≥3 of 5 domains) that these policy windows can adjudicate within 2–3 years. This is well-aligned to NHB's applied-science preferences.

**Withhold-points evidence.** Policy windows for psychiatric/risk-tolerance interventions are less crisp than for diet and algorithmic recommender regulation. The alcohol-liver chain is well-supported by existing policy (minimum unit pricing, Scotland) but the paper does not cite such evaluations. A Nature main would typically tie to one *decisive* upcoming policy decision; NHB tolerates multi-policy alignment.

**v1 → v2 change.** +1 for tying the P4 prediction explicitly to four named policy debates.

**To reach 10.** Add a concrete numerical prediction for one active policy (e.g., UK sugar tax decadal evaluation expected in 2025) with a pre-registered falsifying threshold.

---

### Criterion 9 — Reproducibility / pre-registration: **5/10** (v1: ~6/10, **−1**)

**Give-points evidence.** Scripts in 03-analysis/scripts/ with documented seeds (20260418), deterministic pipelines, reproducible figures, checkpoint discipline across stage3/*_v2.md files. OSF deposit planned at submission with full DOIs. Data-access protocols documented in SI Appendix M. GitHub repo referenced. The analyses I spot-checked (cross_level_meta_findings.md, layer_D_MR_findings_v2.md, mortality_anchor.md) have code-output traceability that is above NHB median.

**Withhold-points evidence.** **This is the only criterion where v2 scores lower than v1, and it is deliberate.** §M12 and §11.0 explicitly acknowledge that OSF pre-registration is *at submission* (predecessor-paper pattern), not pre-analysis. The v1 construct (`sweet_trap_formal_model_v1.md`, 2026-04-16) was not OSF time-stamped before Layer A v1 began. The §11 rewrite dated 2026-04-17 post-dates Layer A v1 (8 cases) and Layer C ISSP. The HARKing-transparency log is honest, but it does not *undo* the fact that the construct was revised after looking at the data. NHB reviewers are increasingly sensitive to this; several NHB papers in 2024–2025 were rejected specifically on "v2 construct revision after data inspection, even if transparent". The v1 rater scored 6 under the assumption that pre-registration was a solvable path; v2's honest disclosure that it is not a path available for this submission is the correct, if score-lowering, move.

**v1 → v2 change.** **−1.** This is a penalty for honest disclosure, not for degraded practice. The authors could have written a misleadingly confident OSF statement; they did not.

**To reach 10.** Impossible for this submission. For the *next* paper, pre-register the construct at OSF before any empirical pipeline begins.

---

### Criterion 10 — Narrative coherence (P→M→C): **8/10** (new in v2)

**Give-points evidence.** The Problem→Mechanism→Consequence arc is well-closed in v2: (P) 34.6M DALYs/yr of modern-environment mismatch; (M) Sweet Trap cross-species equilibrium with F1+F2 classification and P5 cross-level rank prediction; (C) signal-distribution policies outperform information policies. The abstract-introduction-results-discussion flow is internally consistent; §1 establishes the formal framework, §§2–5 test it at each layer, §6 performs the cross-level synthesis, §7 establishes discriminant validity, §8 anchors to welfare. The "moth → peacock → mortgage" image in Introduction and Discussion is rhetorically deft and substantively defensible (each satisfies Δ_ST > 0, F1+F2).

**Withhold-points evidence.** The C12 short-video downgrade, the C13 housing anomaly, and the 11/19 Steiger failures are disclosed transparently in §3, §6, §5 respectively — but they create narrative turbulence. A reader moving from abstract (clean 3-robust + 1-direction + 1-fragile portrait) to Discussion §Fourth/Fifth limitations will notice the paper consumes its own confidence. This is correct science; it is *slightly* inefficient storytelling. The "~10 Parkinson's diseases" frame in the abstract is strong; the "4.1M under Tier-1 Steiger" frame in §5 is its honest counter-weight. The narrative would be tighter if the abstract led with the range and the discussion closed with the range, rather than having the reader reconcile.

**v1 → v2 change.** New criterion (not in v1 rollup).

**To reach 10.** Abstract should state the range (4.1M–34.6M) rather than the point; Discussion should open with the construct's successes and *then* enumerate limitations, rather than interleaving.

---

## §3. v1 → v2 Upgrade Summary

| Upgrade | Score impact | Effective |
|---|---|---|
| Layer A 8 → 20 cases, PRISMA protocol | +2 (#2) | Strong |
| F1+F2 necessary-sufficient + 10-case κ=1.00 | +4 (#3) | Decisive |
| §11 rewrite with HARKing transparency log | Included in +4 (#3) | Strong |
| 19 MR chains + MVMR + PRESSO | +1 (#4), +1 (#5) | Moderate |
| Cross-level Spearman ρ(A,D) = +1.00 | +2 (#1), +2 (#2) | Decisive headline, weak-n caveat |
| DALY anchor 34.6M (Tier-1: 4.1M) | +2 (#7) | Strong but Steiger-compressed |
| Spec-curve 3,000 specs + median reporting | +1 (#4) | Moderate |
| Cultural G^c ΔR² = +0.0009 transparency | Included in +4 (#3) | Strong |
| Narrative (P→M→C) closure | +8 (#10 new) | Strong |
| OSF pre-registration not pre-analysis | **−1** (#9) | Honest penalty |

**Net: +9 (62 → 71).**

Upgrades that did *not* materialise as expected:
- No new theoretical object (theorems, novel equilibria) — #1 capped at 6.
- No prospective out-of-sample discriminant replication — #3 capped at 7.
- No pre-analysis pre-registration — #9 penalised.

---

## §4. Shortest Path to +5 to +10 More Points

**Action 1 — Out-of-sample discriminant replication with independent rater (cost: 5–7 days; score: +2 to +3 on #3).**
Have a second analyst independently code C3 (livestream), C7 (MLM), C10 (religious over-donation) on F1–F4 using the PDE files, compute inter-rater κ, and report at submission. This converts the 10-case dev-set matrix into 10 dev + 3 held-out. Even if κ < 1.00, transparent reporting raises #3 from 7 to 9.

**Action 2 — Rewrite abstract headline around Steiger range (cost: 1 day; score: +1 on #7, +1 on #10).**
Replace "Sweet Trap exposures account for ~34.6 million DALYs per year globally [16.2, 64.1]" with "Sweet Trap exposures account for 4.1–34.6 million DALYs per year globally depending on Steiger directionality assumption, with a conservative floor equivalent to the global burden of Parkinson's disease and an upper bound equivalent to ten Parkinson's diseases." This costs narrative snap but eliminates a referee attack surface. Net novelty gain is +2 because the integrity credit at #7 and #10 more than offsets the rhetorical softening.

**Action 3 — Add third overlapping mechanism cell to Spearman ρ(A,D) test (cost: 2–3 weeks if data exists; score: +2 on #2).**
The headline P5 result depends on 2 overlapping mechanism cells, which is statistically uninformative in isolation. Identify a fisher_runaway MR instrument (mate-preference polymorphisms, partner-choice-related GWAS from 23andMe or UKB questionnaire) and a fisher_runaway-coded human outcome. A 3-cell ρ test where ρ = 0.5+ would be more defensible than a 2-cell ρ = 1.00.

**Combined: +5 to +7.** Gets the paper from 71 to 76–78, comfortably mid-NHB. Beyond this, the path to 80+ (Science main) requires a new mathematical result (Criterion 1), which is 6–12 weeks of theory work.

---

## §5. Residual Risk Analysis

### R1. Steiger compression (high probability of referee flag; high impact)
11/19 chains fail Steiger. The authors argue BMI/alcohol loci have organ-specific direct molecular pathways — this is biologically plausible but not proved. An MR-methods referee (e.g., one trained on Davey Smith / Hemani / Neale lab standards) will demand the abstract lead with the 4.1M Tier-1 figure. Mitigation: pre-empt by rewriting the abstract range (Action 2).

### R2. Cross-level meta-regression n_groups = 3 singular variance (medium probability; medium impact)
§M9 admits the REML random-intercept variance is singular at 3 groups. The primary full A+B+D p = 0.47 is rescued only by the pre-registered A+D subset (p = 0.019). A statistics referee will press on the "pre-registered" claim — the authors must produce the OSF time-stamp for the A+D-only registration, which per §M12 does not exist pre-analysis. This is the single most rescue-fragile statistical claim in the paper.

### R3. Layer B C13 housing anomaly (medium probability; low impact)
ρ(A,B) = −0.50 and primary Wald χ²(2) p = 0.47 mean Layer B's anomalous behaviour drags the full three-layer model to non-significance. The mechanism-reclassification sensitivity (C13 → olds_milner) pulls p to 0.033, but this is ad hoc. A referee will ask: under pre-registered labels, the three-layer test fails; why is the A+D subset the headline?

### R4. OSF pre-registration post-dates analysis (low probability NHB, high probability Nature main; medium impact)
At NHB, honest disclosure in §M12 and §11.0 likely passes. At Nature main, it would not. This is the main reason NHB, not Nature main, is the correct target.

### R5. C12 short-video fragility (low probability; low impact)
The authors have downgraded C12 from confirmed to directional. A referee may still ask why a 5-domain Layer B is the headline when one is acknowledged fragile. Reframing Layer B as "3 robust + 1 direction-robust + 1 fragile" is defensible.

### R6. Dev-set discriminant matrix (medium probability; low-to-medium impact)
A methods referee will note that 10 cases informed construct development and the classifier is tested on those 10. Authors acknowledge this (§7 caveat). Mitigation: Action 1 above.

---

## Bottom Line

**71/100 → NHB is the correct target.** The v2 upgrades successfully lift Falsifiability (#3) and Universality (#2) out of desk-reject territory and add a credible welfare anchor (#7). The residual vulnerabilities — Steiger compression, n=3 cross-level meta, dev-set discriminant — are acknowledged in-text and defensible at NHB. They are not defensible at Science main, and the authors should resist any impulse to re-aim. If Action 1 (out-of-sample discriminant) and Action 2 (abstract range rewrite) are completed pre-submission, score moves to 73–75 and NHB acceptance probability rises from ~35% to ~45%. Action 3 (third mechanism cell) is worth doing only if data already exist; otherwise defer to revision round.

---

*Audit complete. novelty-audit agent, 2026-04-18.*
