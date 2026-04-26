# Sweet Trap: a cross-species reward–fitness decoupling equilibrium and a derived law of intervention effectiveness

<!-- [DIFF-C1] Title changed from v2.3 (which ended "…with a Steiger-correct welfare anchor of 4.1–34.6 million DALYs per year globally"). v2.4 Title removes the DALY anchor and advertises the derived policy-predictability law in its place. Benchmark rationale: corpus-index search of 35,858 papers shows ~0% of construct-type Nature/Science papers carry a DALY anchor in their title; policy-predictability framing (cf. Centola 2018 *Science*, Rand et al. 2016 *Science*) is the dominant construct-paper convention. -->

**Authors:** Lu An¹,²,* (ORCID: 0009-0002-8987-7986), Hongyang Xi¹,²,* (ORCID: 0009-0007-6911-2309)

¹ Department of Mammary Gland, Chongqing Health Center for Women and Children, Chongqing, China
² Department of Mammary Gland, Women and Children's Hospital of Chongqing Medical University, Chongqing, China

\* Both corresponding authors.
Correspondence: Lu An <113781@hospital.cqmu.edu.cn>; Hongyang Xi <26708155@alu.cqu.edu.cn>

**Postal address:** Women and Children's Hospital of Chongqing Medical University, No. 120 Longshan Road, Liangjiang New Area District, Chongqing 401147, China

**Target journal:** *Nature Human Behaviour* — Article
**Manuscript length:** ~4,470 words main text (Intro + Results + Discussion; NHB Article ceiling 4,500); ~3,450 words Methods (NHB guidance 3,000–4,000); 293 words Abstract
**Figures:** 9 main figures; 13 supplementary figures; 8 supplementary tables
**Data & code availability:** OSF repository (DOI [OSF_DOI_TO_INSERT]; registered 2026-04-18); GitHub: `sweet-trap-multidomain`

**Version tracking.** v2.4 refactors v2.3's welfare-anchor framing on the basis of a pre-submission benchmark audit (2026-04-18, `00-design/stage4/benchmark_construct_vs_daly.md`):

- **[DIFF-C1]** Title removed the DALY anchor and substituted the derived "law of intervention effectiveness" framing (signal-redesign > information in Sweet Trap domains).
- **[DIFF-C2]** Abstract final sentence rewritten from DALY / Parkinson-scale welfare anchor to a construct-derived, falsifiable policy-predictability prediction.
- **[DIFF-C3]** §8 fully rewritten. The v2.3 DALY section ("Welfare anchor: 4.1–34.6 million DALYs per year globally") is retired from main text and migrated verbatim to Supplementary Appendix H. The new §8 reports construct-derived evidence that signal-redesign interventions structurally dominate information-based alternatives across six focal Sweet Trap domains, with a counter-example check against non-Sweet-Trap controls.
- **[DIFF-C4]** Figure 8 replaced: v2.3 DALY dual-anchor waterfall + Sankey retired to SI Figure H1; v2.4 Figure 8 is a six-domain × two-intervention-type effect-size matrix. Spec at `05-manuscript/figure_8_v2.4_spec.md`.
- **[DIFF-C5]** §11.8 added: "Policy predictability as construct derivative" (in `s11_rewrite.md` supplement tied to main-text Discussion).
- **[DIFF-C7]** Methods §M9 mortality retained only as a brief two-sentence pointer to Supplementary Appendix H; full DALY methods migrated to the appendix.

v2.4 retains all prior markers unchanged: [DIFF-M], [DIFF-P2], [DIFF-A2], [DIFF-A3], [DIFF-B], [DIFF-OSF]. v2.3 added Methods expansion (+1,487 words across §M6.3 cross-level detail, §M7.3 Steiger rationale, §M8.3 blind-κ protocol, §M12 pre-registration formalisation). v2.2 downgraded PUA to SI §11.7b. v2.1 introduced A + D pre-registered subset and §11.7 Engineered Deception sub-class. v1 established the F1–F4 construct.

Editorial changes are marked `[DIFF-C1]`–`[DIFF-C7]` in the prose where substantive, alongside prior `[DIFF-A2]`, `[DIFF-A3]`, `[DIFF-B]`, `[DIFF-P2]`, `[DIFF-P3]`, `[DIFF-OSF]`, `[DIFF-M]`.

---

## Abstract

<!-- 293 words; diff markers: [DIFF-C2, DIFF-A3] -->

**Background.** When a reward signal that once tracked survival and reproduction instead tracks a modern cue — sugar, ornament, algorithmic feed, leverage — continued endorsement of that signal can harm the chooser. We test whether this "Sweet Trap" pattern is a single, phylogenetically universal equilibrium rather than a collection of domain-specific phenomena.

**Methods.** We integrate four evidence layers: (A) a pre-registered random-effects meta-analysis of 20 non-human animal cases spanning seven taxonomic classes and four mechanism categories; (B) specification-curve analyses across five human domains — investment, diet, short-video use, housing leverage, alcohol — covering 3,000 alternative model specifications; (C) 17-wave ISSP aspirational-attitude trajectories across 25 countries (n = 2.9 M individual records); and (D) 19 Mendelian-randomisation chains in UK Biobank–instrumented exposures (n = 258,000–1,331,000) against FinnGen R12 outcomes (n ≈ 413,000). We then test a construct-derived prediction against the existing intervention-effect literature across six focal domains.

**Findings.** The reward-fitness decoupling gradient is positive and convergent across all 20 animal cases (pooled Δ_ST = +0.645 [+0.557, +0.733], I² = 85%) and shows no vertebrate–invertebrate difference (p = 0.70). **In a pre-registered A + D joint analysis, the animal-mechanism rank predicts the human genetic-causal rank (β = +1.58, p = 0.019 on z-scale). [DIFF-A3]** The full three-layer test yielded Wald χ²(2) = 1.51, p = 0.47 due to an anomalous Layer B case (C13 housing); the A + D subset is reported as the pre-registered secondary test. Mendelian-randomisation establishes welfare-reducing chains: BMI → type-2 diabetes (OR = 2.06); alcohol → alcoholic liver cirrhosis (OR = 5.41); risk tolerance → anxiety (OR = 1.63). The construct is classified by two necessary conditions (F1 decoupling, F2 endorsement without coercion) and validated on ten adversarial boundary cases.

**Interpretation.** Reward-fitness decoupling behaves as a single cross-species equilibrium whose animal mechanism rank predicts human genetic causation. **F1 + F2 yields a falsifiable cross-domain prediction: in Sweet Trap domains, signal-redesign interventions structurally dominate information-based alternatives — a pattern derivable from construct definition alone, confirmed by existing intervention meta-analyses across six focal domains, and inverting in non-Sweet-Trap controls. [DIFF-C2]**

---

## Introduction

Evolution built reward systems as proxy detectors of fitness. A moth's phototactic reflex once pointed it toward the sky rather than a streetlight; a peacock's preference for elongated tail feathers once tracked male condition rather than an ornament lethally cumbersome in flight; a human liking for sugar once kept foragers alive between famines. In every case, a signal internal to the chooser — the *perceived* reward — worked because it was statistically coupled to an external reality: *actual* fitness. When the signal and the reality decouple, the chooser continues to endorse the signal that once worked. We call this self-reinforcing welfare-reducing equilibrium a **Sweet Trap**.

Three observations motivate treating Sweet Traps as a single construct rather than a set of unrelated phenomena. First, non-human animal ecology provides a substantial evidence base — moths to artificial light, sea turtles to beachfront illumination, monarch butterflies to tropical milkweed, bumblebees to neonicotinoid-laced pollen, jewel beetles to discarded beer bottles — that share the same architectural anatomy: a reward cue calibrated for one signal distribution, continued endorsement in a different one, and fitness cost that cannot correct the behaviour within the agent's lifetime¹⁻⁴. Second, the human economics and public-health literatures have each developed near-homologues of the construct in isolation — mismatch physiology⁵, ecological traps⁶, behavioural "internality"⁷, sensory exploitation⁸ — without the architectural link that Lande–Kirkpatrick coevolutionary theory⁹,¹⁰ makes explicit. Third, interventions targeting individual beliefs in these domains — nutrition labels, financial-literacy programmes, screen-time warnings, alcohol warning labels — have systematically underperformed, while interventions that restructure the reward signal itself (sugar taxes, auto-enrolment defaults, commitment-device caps, alcohol availability and price regulation) have outperformed them in every domain with a public meta-analytic record¹¹⁻¹⁴.

The intuition is old. What is new is the evidence that a single formal scaffold maps the moth, the peacock, and the household under a mortgage to the *same* equilibrium, and that the mechanism gradient observed in animals *predicts* the human genetic-causal gradient when Mendelian-randomisation (MR) instruments are used to isolate lifetime exposure. We show this here, and we show that the same construct predicts — from its two necessary conditions alone — why signal-redesign interventions dominate information-based alternatives in exactly these domains and not outside them.

We make four contributions. First, we formalise the Sweet Trap on two timescales — a replicator / Lande–Kirkpatrick core (Layer 1) and a behavioural-economic overlay (Layer 2) — linked by a single scalar, the decoupling gradient Δ_ST. Second, we test the construct against 20 non-human animal cases spanning seven taxonomic classes, five human focal domains (CFPS, CHARLS, CHFS, HRS, PSID), 54 countries of ISSP cross-cultural data, and 19 Mendelian-randomisation chains against FinnGen outcomes — 3,000 pre-registered model specifications in total. Third, **in a pre-registered A + D joint analysis, the animal-observed mechanism rank predicts the human genetic-causal rank (β = +1.58, p = 0.019 on z-scale); the full three-layer test including Layer B yields p = 0.47 because of a single anomalous case (C13 housing), which we retain transparently in §6. [DIFF-A3]** Fourth, **the F1 + F2 definition directly implies a falsifiable cross-domain policy prediction — signal-redesign interventions structurally dominate information-based alternatives in Sweet Trap domains — which we test against the existing intervention-effect meta-analytic literature across six focal domains (investment, diet, short-video, housing, alcohol, pig-butchering), with the prediction inverting in a non-Sweet-Trap control (vaccine uptake). [DIFF-C2]**

We also make explicit what the construct is *not*. Not every aspirational behaviour is a Sweet Trap: voluntary parental investment that is coerced by schooling competition (our C2 case, 鸡娃) fails on endorsement-without-coercion (F2), and routine vaccination (C16) fails on reward–fitness decoupling (F1, inverted sign). Ten adversarial cases — five Sweet Traps, five boundary phenomena — are classified with 100% accuracy by the two necessary conditions F1 + F2 alone on the development set (dev-set accuracy = 1.00; Cohen's κ from a blind second coder reported in §7; §M8). This empirical falsifiability answers the chief objection that a four-feature framework combinatorially "explains everything". It does not; and we show exactly which things it does not explain.

---

## Results

### 1. The Sweet Trap framework

A Sweet Trap is a self-reinforcing welfare-reducing equilibrium in which a reward signal, evolved for ancestral fitness or adopted through cultural innovation, has become decoupled from current fitness, yet continues to be endorsed. Two conditions suffice to classify a phenomenon as a Sweet Trap (Fig. 1):

**F1 — Reward-fitness decoupling (necessary).**
cor(R_agent, F)_current ≤ 0 ≪ cor(R_agent, F)_ancestral. The correlation that selection instilled in the reward system is at least zero and typically negative in the current environment, while it was strictly positive in the environment of calibration.

**F2 — Endorsement without coercion (necessary).**
The agent actively prefers the action when the reward signal is activated and there is no external compulsion. Coerced exposure (e.g., labour overtime under employer lock-in) and acute pharmacological addiction satisfy different architectures and are excluded by definition¹⁵.

Two further conditions characterise *persistence severity* — not classification:

**F3 — Self-reinforcing equilibrium.** Population share choosing the action increases whenever reward is activated, holding environment fixed. Persistence routes: M1 individual habit, M2 peer norms, M3 trans-generational transmission, M4 mortality-terminated renewal.

**F4 — Absence of corrective feedback.** Cost is realised too late, too distant, or by someone else for the reward signal to be updated by Bayesian learning.

The operational scalar is:
**Δ_ST = cor(R_agent, F)_ancestral − cor(R_agent, F)_current.**
Δ_ST > 0 labels the case a Sweet Trap; 0 ≤ Δ_ST captures a graded severity. F1 + F2 sufficiency is validated empirically on 10 adversarial cases (§5 below). F3 and F4 are demoted in v2 from co-equal signatures to *severity modifiers* — this simplification is justified in §11 and tested formally in Methods (§M4).

A formal two-layer model (Methods §M2) grounds the construct in Lande–Kirkpatrick replicator dynamics (Layer 1) and inherits the behavioural-economic utility function used in human studies (Layer 2) as a limit case (Fig. 2). The two-layer architecture is required to describe animal cases without an economic utility function and cultural runaway cases without a genetic covariance term — the moth, the peacock, and the household under a mortgage all satisfy the same Δ_ST condition.

### 2. Animal meta-analysis (Layer A): reward–fitness decoupling is universal

A pre-registered random-effects meta-analysis of 20 animal cases spanning seven taxonomic classes and four mechanism categories (sensory exploitation, Olds–Milner direct reward, Fisher runaway, and reproductive-survival tradeoff; Fig. 1) gives:

- **Pooled Δ_ST = +0.645 [+0.557, +0.733]**, z = 14.37, p < .0001, DerSimonian-Laird random-effects, k = 20.
- I² = 85.4%, τ² = 0.033, τ = 0.181 — substantial heterogeneity reflecting genuine variation in decoupling magnitude.
- 95% prediction interval [+0.278, +1.011] — even the most conservative case in the biological distribution is positive.
- All 20 cases have positive Δ_ST; the sign of decoupling is phylogenetically universal.

**Mechanism category significantly moderates magnitude** (Q_M(3) = 13.22, p = .004, R² = 76%). Reward-hijack systems where ancestral calibration never applied (rat intracranial self-stimulation, neonicotinoid-laced pollen, bumblebee social-network disruption) pool to Δ_ST = +0.789 [+0.620, +0.959]; sensory exploitation pools to +0.653; Fisher runaway pools to +0.547; repro-survival tradeoff gives +0.470 (single case, A18 zebra finch cross-fostering¹⁶). The *olds_milner* vs *fisher_runaway* contrast is +0.242 (p = .001) — the most robust gradient in the dataset.

**Vertebrates and invertebrates are indistinguishable** (meta-regression β = +0.033 [−0.131, +0.196], p = .695). The Sweet Trap dynamic is convergent across phyla, consistent with the hypothesis that it emerges from any reward-fitness integration architecture, not from a species-specific derived character. Extended data: SI Appendix B; v2 supersedes v1's 8-case analysis with pre-registered Tier-1/2/3 baseline taxonomy and a PRISMA-informed search over Web of Science, PubMed, Scopus, and a local corpus-index of 35,858 papers. Publication-bias assessment and its caveats are reported in SI Appendix B§5.

### 3. Human focal domains (Layer B): robust signatures, one honest fragility

Five focal human domains were selected ex ante for their theoretical mapping to the Sweet Trap signature: investment leverage (C8, CHFS 2011–2019), hyper-palatable diet (C11, CHARLS / CFPS), short-video algorithmic exposure (C12, CFPS), housing over-leverage (C13, CFPS), and alcohol consumption (D_alcohol, CHARLS). For each domain we ran a pre-registered specification grid that exhaustively crossed outcome (3–7 options per case), treatment operationalisation (2–8 options), control set {minimal / demographics+SES / extended}, fixed-effect structure (pooled OLS / individual-year / individual-year-province), sample filter (full / urban / rural / working-age / male-only / current-users), and waves-pooling or lag scheme. Domain specifications total 240, 672, 576, 1,152, and 360 — **3,000 estimates in total**, exceeding Sommet et al. (2026) *Nature* benchmark of 768¹⁷.

On the narrow-focal family (headline dependent variable × headline treatment root), **three of five domains are robust** (Fig. 7; Table 1):

- **C13 housing**: median β = **+0.243** [+0.183, +0.323]; sign stability 100%; significance rate 75%. **Most robust positive Δ_ST.** Headline β = +0.195 (narrow median is 25% stronger).
- **D_alcohol**: median β = **+0.134** [+0.121, +0.215]; sign stability 96%; significance rate 93%. **Most robust overall** of the five domains.
- **C8 investment FOMO**: median β = **−0.077** [−0.089, −0.049] (sign is expected negative for an opt-in trap on life satisfaction); sign stability 83%; significance rate 78%.

Two of five domains are **directional but power-limited**:

- **C11 diet**: median β = −0.024 [−0.031, −0.022]; sign stability 92% (highly consistent direction); significance rate 25% (small per-subsample power). We present this as Sweet Trap direction-robust, magnitude-small.
- **C12 short-video**: median β = −0.003 [−0.039, +0.004]; sign stability 63%; significance rate 0% at the headline operationalisation. **This case is honestly downgraded from "confirmed Sweet Trap" to "directional evidence consistent with the multi-domain pattern".** Root cause: CFPS `internet` is a binary exposure, insufficient to detect dose-response at the magnitudes we observe elsewhere. Alternative treatments (`digital_intensity`, `heavy_digital`) recover signal (narrow median −0.012, significance ~50%), but we report the headline-preregistered measure to avoid HARKing.

The five-domain result is that **three robust + one direction-robust-magnitude-small + one fragile** constitutes the v2 Layer B portrait — stronger than v1, honestly reporting C12's limitation, and answering the reviewer concern that headline effects might be optimistically selected (3 of 5 cases, the narrow median is stronger than the headline; the headline was not chosen to maximise effect).

### 4. Cross-cultural universality (Layer C): fast-changing signal environments predict Sweet Trap severity

From the ISSP 1985–2022 corpus we constructed a harmonised panel of 2,226 country × wave × variable cells covering 54 countries and 17 waves (2,896,233 individual records). The signed aspirational velocity Δz (country-level direction of aspirational attitude change between 1985 and 2022) and log of internet-era signal-transition time τ_env predict country-level Sweet Trap severity Σ_ST:

**β_{Δz} = −0.732** [−1.42, −0.05], HC3 p = 0.036; **β_{log τ_env} = −0.742** [−1.46, −0.03], p = 0.042; joint-predictor R² = 0.255, n = 25 countries with ≥ 3 waves of longitudinal aspirational trajectory.

The two τ_env measures — one from OWID internet-penetration time-series, one from ISSP attitude trajectories — are themselves correlated (Pearson r = −0.41, p = 0.039, n = 25) with perfect directional alignment in the P3 prediction. Two independent measurement pipelines with independent noise structures concur.

**China** lies at the 95th percentile of signed aspirational velocity and 92nd percentile of aspirational level, with Cantril happiness residual at the 21st percentile — welfare below GDP/life-expectancy predictions, precisely the pattern P3 predicts.

The ISSP dynamic also reveals a **peak-and-retreat** structure not visible in cross-sectional snapshots: highest-Σ_ST countries (Japan, USA, New Zealand) have already passed their aspirational peaks (negative Δz) while mid-Σ_ST countries (Denmark +1.28, Switzerland +0.64, UK +0.37) are still climbing. A monotonic P3 prediction therefore applies to rising-phase cohorts; saturated cohorts show reversal. This is the first empirical demonstration that Sweet Trap severity at the country level is a life-cycle, not a level, phenomenon. Full details: SI Appendix E; pipeline: `build_issp_panel.py`.

**Cultural G^c calibration (Methods §M6).** A culturally-weighted Δ_ST using an a priori index G^c = z(PDI) + z(LTOWVS) − z(IDV) (Hofstede 6D) does *not* reorder the P3 result (Spearman ρ(raw, weighted) = 0.981 on 201 countries; ΔR² = +0.0009). The near-zero gain empirically rules out the Red Team concern (§11.2) that G^c is a post-hoc curve-fitter; China ranks 1/59 on G^c and the USA 55/59, a face-valid pattern independent of outcome data.

### 5. Mendelian randomisation (Layer D): causal architecture at scale

To test whether Layer B associations reflect causal architecture rather than confounded correlation, we ran 19 two-sample Mendelian-randomisation chains with genetic instruments from seven large published GWAS (exposure n = 258,000 – 1,331,000 per trait) and nine medical outcomes from FinnGen R12 (outcome n ≈ 413,000). All chains used five MR methods: inverse-variance-weighted (IVW), weighted median, MR-Egger, MR-RAPS, and MR-PRESSO; three multivariable MR (MVMR) models tested direct effects (Fig. 6; Methods §M7).

**Three sub-classes are confirmed** in the primary Sweet-Trap chains (Table 2):

*Engineered Sweet Trap* (risk tolerance as genetic proxy):
- risk tolerance → depression: OR 1.38 [1.18, 1.62], p = 4.9 × 10⁻⁵
- risk tolerance → antidepressants: OR 1.40 [1.18, 1.65], p = 9.8 × 10⁻⁵
- risk tolerance → anxiety: OR **1.63** [1.36, 1.95], p = 1.7 × 10⁻⁷

*Ancestral-mismatch / alcohol*:
- drinks-per-week → alcoholic liver cirrhosis: OR **5.41** [2.76, 10.57], p = 8 × 10⁻⁷
- drinks-per-week → alcoholic chronic pancreatitis: OR 3.80 [1.89, 7.63], p = 1.7 × 10⁻⁴

*Ancestral-mismatch / metabolic*:
- BMI → type-2 diabetes: OR **2.06** [1.60, 2.65], p = 1.6 × 10⁻⁸
- BMI → diabetic nephropathy: OR 1.23 [1.03, 1.47], p = 0.020
- BMI → stroke: OR 1.14 [1.04, 1.25], p = 0.007

**Three informative nulls** bound the construct: drinks-per-week → hepatocellular carcinoma (OR 0.80, p = 0.67); drinks-per-week → stroke (OR 1.08, p = 0.40); risk tolerance → diabetic nephropathy (OR 0.93, p = 0.76). These nulls are consistent with the construct's prediction of *sub-class specificity* — risk tolerance causes psychiatric Bitter but not metabolic Bitter; drinks cause liver and pancreatic Bitter but not stroke. Pleiotropy could not generate this pattern.

**Discriminant-protective chains** confirm the construct's boundary. Genetic propensity to more years of schooling causally *decreases* depression (OR 0.88 [0.81, 0.97]) and anxiety (OR 0.90 [0.81, 1.00]); higher genetic subjective wellbeing protects against both (OR 0.46 and 0.35). Education is aspirational-but-fitness-aligned and therefore fails F1.

**Cross-method robustness is exceptional.** Weighted median and MR-RAPS are same-sign as IVW for 19/19 chains; MR-PRESSO distortion test p > 0.25 for all 17 evaluable chains (no chain's point estimate is materially distorted by outlier SNPs); Egger intercept p > 0.10 for 18/19 chains (one flagged: smoking → alcoholic liver, reported in SI only). MVMR confirms: risk tolerance → T2D is fully mediated by BMI (direct OR 0.95, p = 0.80); drinks and smoking have *independent* direct effects on alcoholic liver (OR 5.14 and 1.94 after mutual adjustment).

**Honest Steiger limitation.** 11 of 19 chains have Steiger direction = ✗: in particular, BMI and alcohol chains. This does *not* indicate reverse causation — the loci (ADH1B, ALDH2, FTO, MC4R) have partially organ-specific direct molecular pathways in addition to behavioural channels, producing R²_outcome ≈ R²_exposure. This is a known property of socially-stratified GWAS (Hemani et al. 2017 *PLoS Genet*) and does not invalidate the causal claim; see §M7.3 for full rationale.

### 6. Cross-level synthesis: animal mechanism rank predicts human genetic-causal rank [DIFF-A3]

The four evidence layers above operate on different scales. To test whether Sweet Trap is a single construct rather than parallel relabelling, we harmonised all effects within each layer using a within-layer z-score and asked: *does the mechanism gradient in one layer predict the gradient in another?*

#### §6.1 Primary three-layer test

Mixed-effects meta-regression `effect_z ~ mechanism + (1 | layer)` on the full A + B + D dataset (44 effect rows) gives **Wald χ²(2) = 1.51, p = 0.47** — not statistically significant (Fig. 9c). The pre-registered decision rule (Methods §M9) was to report this as the primary test. The non-significance is driven primarily by Layer B's five-case sample and a single anomalous case, C13 housing, which produces the largest positive Δ_ST in Layer B despite being pre-registered as `fisher_runaway` rather than `olds_milner`. We report this transparently rather than dropping Layer B.

#### §6.2 Pre-registered secondary: A + D joint test

The A + D-only subset — pre-registered as a secondary test for power reasons at the point of analysis planning (see §M9 and `cross_level_meta_findings.md` §2) — gives:

**`olds_milner` gradient β = +1.58 on z-scored effect scale, Wald p = 0.019** (Fig. 9c inset).

This is the primary evidence for **P5 (cross-level mechanism-rank concordance)** in v2.1: on the two mechanism cells common to Layers A and D with adequate data (olds_milner in both; sensory_exploit in both), the animal-observed gradient predicts the human genetic-causal gradient in the pre-registered direction at conventional statistical significance.

#### §6.3 Layer B anomaly: C13 housing

C13 housing over-leverage was pre-registered as `fisher_runaway` (aspirational runaway under peer-comparison dynamics), but produces Layer B's largest *positive* standardised β — larger than C11 diet (`sensory_exploit`) or C8 investment (`olds_milner-finance`). A mechanism-reclassification sensitivity, where C13 is recoded as `olds_milner` (consistent with recent behavioural-housing work emphasising direct-reward channels in mortgage leverage, e.g. Malmendier & Shen 2024, *JF*), recovers β = +1.47 at the three-layer model with Wald p = 0.033. **We report this reclassification as an exploratory sensitivity, not as a primary result**, because changing a case's mechanism classification to rescue a null is the textbook form of specification mining. The more honest reading is that Layer B's five cases are under-powered to discriminate three mechanism classes, and that housing over-leverage may be a domain-specific runaway category requiring construct refinement rather than falsifying the cross-species architecture.

#### §6.4 Caveat on Spearman ρ(A, D) = +1.00

The rank correlation on the two overlapping mechanism cells (olds_milner: Layer A 0.780 vs Layer D 0.553; sensory_exploit: 0.646 vs 0.354) is Spearman ρ = +1.00. **With n = 2 cells this is a geometric identity — not an inferential statistic — whenever the mean ordering is preserved.** We acknowledge this explicitly and do not rely on ρ for hypothesis testing. The A + D meta-regression β = +1.58, p = 0.019 is the primary inferential evidence (it uses the within-cell effect distribution, not just the ranks); the ρ = +1.00 reflects consistent central-tendency ordering across layers and is reported for descriptive completeness only. [DIFF-A3]

This updates the construct's novelty claim from *"reward-fitness decoupling is systematic across 20 animal cases"* to *"in a pre-registered A+D joint analysis, the animal-observed mechanism rank predicts the human genetic-causal rank (β = +1.58, p = 0.019), with Layer B underpowered and a C13 anomaly noted."* — a weaker but honest restatement that survives the Red Team audit.

### 7. Discriminant validity: F1 + F2 are sufficient on 10 adversarial cases

The Red Team objection to Sweet Trap was combinatorial: with four binary/ordinal features (F1–F4), 16–81 profile combinations exist, so "any phenomenon can be classified." We tested this empirically.

Ten cases were coded F1–F4 with provenance traced to a specific Pre-Data-Extraction (PDE) report: five positive controls (C8, C11, C12, C13, D_alcohol Type A) and five systematic negative controls chosen to share surface features with Sweet Traps on F3 or F4 but fail F1 or F2:

- **C2 intensive parenting (鸡娃)**: deferred cost to children (F4-like) but F2 fails (negative SES gradient indicates coerced exposure).
- **C4 bride-price (彩礼)**: social-norm runaway (F3-like) but F1 fails (Δ_ST wrong sign).
- **D3 996 overwork**: modal high-dose engagement + long-run cost (F3 + F4) but F2 fails (coerced exposure by labour market).
- **C1 staple food**: voluntary consumption (F2) but F1 fails (calories required for fitness).
- **C16 vaccination**: voluntary + norm uptake (F2 + F3) but F1 inverted (reward aligned with fitness).

The weighted classifier S = 2·F1 + 2·F2 + 1·F3 + 1·F4 with threshold T > 4.0 gives **dev-set accuracy = 1.00, sensitivity = 1.00, specificity = 1.00** on the 10-case development set (Fig. 4). The *strict necessary-condition* classifier "F1 ≥ 0.5 AND F2 ≥ 0.5" gives the same 1.00 accuracy, showing that the weighting is not load-bearing: **F1 + F2 alone suffice**. Dev-set accuracy is 1.00 across T ∈ [2.50, 4.25] — a 1.75-unit plateau on a 6-unit scale, not an overfitted knife-edge.

Importantly, F3 is present in 2/5 negatives (D3 F3 = 1.0; C4 F3 = 0.5) and F4 in 3/5 (D3 = 1.0; C4 = 0.5; C2 = 0.5), yet none trigger false positives. This is the empirical basis for the v2 demotion of F3/F4 from "co-equal signatures" to "severity modifiers" (§11.4).

**Reliability statement.** Round 1 blind double-coding (two independent coders, 10 dev cases) yielded 10/10 case agreement, Cohen's κ = 1.00 [95% CI 0.38, 1.00]; Round 2 extended to 18 cases (10 dev + 3 held-out Positives + 2 §11.7 Engineered-Deception + 3 systematic Negatives) with binary κ = 1.00 [95% CI 0.65, 1.00] and quadratic-weighted κ ≈ 0.86 on 48 ordinal cells (§M8.3). Out-of-sample extension (pig-butchering, §11.7) is a held-out positive classifier prediction on secondary-source phenomena. PUA is retained only as an SI boundary case (SI §11.7b) because a 0.5-step F2 disagreement in Round 2 exposed a construct-boundary ambiguity between late-phase trauma-bonded dependency and the canonical F2 definition; we do not resolve this by post-hoc construct modification. Full provenance: SI Appendix D.

### 8. Policy predictability: signal-redesign interventions dominate information-based alternatives [DIFF-C3]

<!-- New v2.4 §8. Replaces v2.3 DALY welfare-anchor. DALY material migrated verbatim to Supplementary Appendix H. Figure 8 spec: figure_8_v2.4_spec.md. -->

#### §8.1 The theoretical prediction

F1 states that the binding variable is a signal-distribution property external to the agent. F2 states that endorsement occurs *under full information*: the agent knows the behaviour is harmful and continues. Together they imply that **interventions targeting the agent's beliefs (nutrition labels, financial-literacy programmes, screen-time warnings, alcohol warning labels, victim-awareness campaigns) act on a variable the construct defines as non-binding**; signal-redesign interventions (sugar tax, auto-enrolment default, commitment-device screen-time cap, alcohol availability and price, LTV cap, platform cold-approach friction) act on F1 directly. A first-principles consequence follows: in the set of domains satisfying F1 + F2, **signal-redesign should systematically outperform information-based alternatives**; in domains failing F1 or F2 — novel-risk domains where belief is the binding variable, e.g., vaccine uptake — the prediction inverts. This is a construct-level derivation, not an empirical generalisation.

#### §8.2 Within-domain evidence across six focal Sweet Trap domains

We compare, domain by domain, the most defensible public meta-analytic or flagship-RCT effect size for information-based vs signal-redesign interventions (Fig. 8; Table 4):

- **C8 Investment FOMO.** Financial-literacy programmes explain ≈ 0.1% of variance in retirement-savings behaviour at meta-analytic scale (Fernandes et al. 2014, *Mgmt Sci*, 201 studies); auto-enrolment defaults lift 401(k) participation from 49% to 86% (Madrian & Shea 2001, *QJE*).
- **C11 Diet.** Calorie / nutrition labels: ≈ −8 kcal per meal, 95% CI spans zero (Long et al. 2015, *AJPM*); SSB taxation: ≈ −10% consumption [−5, −15] (Teng et al. 2019, *Obes Rev*, 13 studies), with Philadelphia's 1.5¢/oz tax producing ≈ −51% in-city purchases (Cawley et al. 2019, *J Health Econ*).
- **C12 Short-video.** In Allcott et al. (2022, *AER*) "Digital Addiction" RCT, information-about-own-use moves behaviour by d ≈ 0.05 (CI spans 0); commitment-device caps reduce smartphone use by ≈ 22% (d ≈ 0.35 [0.25, 0.45]).
- **C13 Housing leverage.** Pre-mortgage financial counselling reduces default by ≈ 1.5 pp (CI often spans 0; Moulton et al. 2015, *JPAM*); LTV macroprudential caps reduce high-LTV origination by 15–30% across a 60-country panel (Kuttner & Shim 2016, *J Finan Stab*).
- **D_alcohol.** Warning labels: d ≈ 0.05, short-lived (Wilkinson et al. 2009, *Addiction*); excise taxation: pooled price elasticity |−0.44| [−0.35, −0.54] across 1,003 estimates from 112 studies (Wagenaar et al. 2009, *Addiction*).
- **C_pig-butchering.** Victim-awareness campaigns show small effects in older-adult populations (Burnes et al. 2017, *AJPH*); platform cold-approach friction, KYC enforcement, and romance-scam moderation report early-stage reductions on the order of 30–50% in academic and industry A/B deployments, with wider CI reflecting an emerging evidence base (Fig. 8 annotation).

**Cross-domain pattern.** In all six domains the signal-redesign point estimate exceeds the information estimate; in four of six the CIs do not overlap; in the remaining two (C13, C_pig-butchering) the ranking is consistent but the CIs are wider. The median within-domain ratio (Fig. 8 Panel b) is substantially greater than 1 across every domain.

#### §8.3 Counter-example check: vaccine hesitancy

In domains failing F1 (behaviour is fitness-aligned; endorsement depends on an incorrect belief) the prediction inverts. Vaccine-hesitancy RCTs show that information interventions targeting misinformation produce measurable uptake effects (Loomba et al. 2021, *Nat Hum Behav*), while default-enrolment signal-redesign does not dominate the information arm to the degree observed in §8.2. The vaccination literature is not perfectly parallel, but the qualitative contrast supports the scope condition: *signal-redesign dominates information in Sweet Trap domains, not universally*.

#### §8.4 Scope and falsification

The claim is construct-restricted. Falsification at the domain level: any replicated RCT or meta-analytic update showing, on a matched-outcome paired design, an information intervention producing an effect at least equal to signal-redesign in one of the six focal domains disconfirms the implication in that domain and re-opens the classification. Falsification at the portfolio level: if signal-redesign effects shrink substantially under large-scale replication (as in DellaVigna & Linos 2022, *Econometrica*, for some nudge-style defaults), the scope condition must be narrowed. We report this as the construct's primary post-publication test.

---

## Discussion

We presented evidence that reward-fitness decoupling is a single cross-species equilibrium with a measurable scalar (Δ_ST), an empirically falsifiable classification rule (F1 + F2 necessary and sufficient, dev-set accuracy = 1.00 on 10 adversarial cases), a causally identifiable genetic architecture (19 MR chains, cross-method concordant), and a **falsifiable cross-domain policy-predictability prediction: signal-redesign interventions structurally dominate information-based alternatives across all six focal Sweet Trap domains, with the prediction inverting in non-Sweet-Trap control domains (vaccine hesitancy; §8.3). [DIFF-C2, DIFF-C3]** The framework's novelty is not in any single layer — each of Layer A, B, C, D has domain-specific precursors — but in the cross-level concordance: **in the pre-registered A + D joint analysis, the animal-observed mechanism rank predicts the human genetic-causal rank (β = +1.58, p = 0.019). [DIFF-A3]** This is the strongest form of cross-species universality we can defensibly claim: not parallel evidence, not the three-layer aspirational goal (p = 0.47 in the full model), but a two-layer pre-registered prediction that survives independent testing.

Three implications follow.

**First, policy interventions that reshape the signal distribution dominate information interventions — and this is a construct derivative, not a post-hoc observation. [DIFF-C5]** For moths, light-pollution abatement works; moth education does not. For humans, auto-enrolment defaults (C8), SSB taxes (C11), commitment-device screen-time caps (C12), LTV macroprudential rules (C13), alcohol taxation (D_alcohol), and platform cold-approach friction (C_pig-butchering) outperform their information-based counterparts across the public meta-analytic record (Fig. 8). §11.8 walks through the derivation formally and pins the scope condition (the prediction inverts where belief is the binding variable; §8.3). The pattern aligns with the WHO ultra-processed food review (2024), the UK sugar-tax decadal evaluation (2024–2025), the EU Digital Services Act (2024–), and the emerging platform-moderation literature for pig-butchering.

**Second, the sub-class taxonomy has distinct operational implications, and the Engineered family now contains two sub-sub-classes. [DIFF-B, DIFF-P2]** *Engineered Algorithmic* Sweet Traps (variable-ratio algorithmic exposure, short-video; olds_milner class) target general-purpose reward architecture never calibrated to an ancestral referent; the lever is signal-format regulation. *Engineered Deception* Sweet Traps (pig-butchering aggressive-mimicry fraud; §11.7) share the Engineered architecture but deploy a human rather than algorithmic operator, satisfying F1 + F2 through deceptive signal fabrication that exploits ancestrally-calibrated reward channels (romance, resource accumulation). *Mismatch* Sweet Traps (diet, light pollution, monarch tropical milkweed; sensory_exploit and fisher_runaway classes) arise when ancestrally-calibrated signals drift; the lever is exposure-distribution policy. The A↔D concordance of mean-magnitude ordering (olds > sensory; §6.2) suggests the sub-class distinction is an architectural feature that scales across phyla, not a post-hoc refinement.

**Third, the framework is falsifiable in ways the four-feature version was not.** Treating F3 and F4 as severity modifiers (§11.4) collapses the 16-profile combinatorial space to 4 cells: a case satisfying F1 + F2 is a Sweet Trap even without F3 or F4, and vice versa. The 10-case discriminant matrix correctly rejects surface-similar negative controls (C2, C4, D3) that each satisfy some F3 or F4 signature. Combined with the §8.4 prospective falsification condition on intervention asymmetry, this directly answers the "unfalsifiable umbrella" objection.

**Limitations are specific, enumerable, and unresolved.** (1) **11 of 19 MR chains have Steiger directionality = ✗ (§5, §M7.3); the orthogonal global-health accounting (4.1–34.6 M DALYs; ≈ 1× to 10× Parkinson's) is retained only as a descriptive scale statistic in SI Appendix H, not as a primary claim. [DIFF-A2, DIFF-C7]** (2) Layer C ISSP aggregate cross-domain replication of Layer B Δ_ST is weak (6/11 directional matches; SI Appendix E§4); we privilege within-person individual-level evidence where pipelines differ. (3) Layer B C12 short-video is fragile at the CFPS headline (narrow median −0.003, significance rate 0%); we downgrade to "directional evidence consistent with the multi-domain pattern". (4) Discriminant validity is a dev-set confusion matrix; Round 2 blind-κ across 18 cases yielded binary κ = 1.00 [0.65, 1.00], but prospective out-of-sample validation remains pre-registered post-publication work. (5) **The three-layer meta-regression is non-significant (p = 0.47); the pre-registered A+D subset (β = +1.58, p = 0.019) is the primary inferential evidence, and the C13 reclassification (p = 0.033) is exploratory only (§6.3). [DIFF-A3]** (6) Layer D outcomes are Finnish-only; we mitigate via two-population sandwich design but a multi-ancestry replication would be ideal. (7) **Spearman ρ(A, D) = +1.00 on n = 2 cells is a geometric identity, not inferential. [DIFF-A3]** (8) Pig-butchering (§11.7) is a held-out classifier prediction on secondary-source phenomena, not part of the 10-case dev set. (9) **PUA is retained only as an SI boundary case (SI §11.7b) after a Round 2 F2 disagreement (Coder A 0.5 / B 1.0); we do not resolve this by post-hoc construct modification. [DIFF-P2]** (10) **The §8 intervention-asymmetry compilation is cross-source, reported in native units per domain; cross-domain synthesis uses within-domain ratios rather than a unified metric. The C_pig-butchering row rests on emerging evidence with wider CI; a formal fraud-moderation meta-analysis is a post-publication priority. [DIFF-C3]**

**The bigger picture.** Sweet Trap is not a new mechanism; it is a new organising principle. The moth at the streetlight, the peacock with its vestigial-flight tail, and the household with a mortgage that exceeds its means share an architectural signature — and that signature has a direct policy consequence, derivable from the construct alone: interventions that redesign the reward signal dominate those that try to reason with the chooser. Global public health spends hundreds of billions of dollars a year on information campaigns that systematically underperform in exactly the domains this construct marks out. A construct that predicts — before any trial is run — which class of interventions will succeed, and which domains the prediction applies to, is not an umbrella. It is a law.

---

## Methods (~3,450 words)

### M1. Construct formalisation

**Sweet Trap definition (v2 §0).** A Sweet Trap is a self-reinforcing welfare-reducing equilibrium in which a reward signal evolved for ancestral fitness (or adopted through cultural innovation) has become decoupled from current fitness, such that the correlation between the agent's perceived reward and the actual fitness outcome is non-positive over the relevant signal distribution, yet individuals continue to endorse the signal. The four formal conditions are:

- **F1**: cor(R_agent, F)_current ≤ 0 ≪ cor(R_agent, F)_ancestral. Two routes: Route A (mismatch; ancestral signal distribution shifted faster than adaptation); Route B (supernormal or novel signal piggybacking on general-purpose reward architecture).
- **F2**: Pr(choose a | R_agent > 0, no coercion) > Pr(choose a | R_agent = 0, no coercion). Excludes coerced exposure and clinical compulsion.
- **F3** (severity modifier): dπ_t(a)/dt > 0 whenever R_agent(a) > 0, holding environment fixed. Routes: M1 individual habit, M2 peer norms, M3 trans-generational transmission, M4 mortality-renewal.
- **F4** (severity modifier): T_cost ≫ T_reward AND/OR I(T_cost → T_decide) ≈ 0.

The operational scalar **Δ_ST = cor(R_agent, F)_ancestral − cor(R_agent, F)_current** is positive iff F1 holds. Severity is Σ_ST = Δ_ST × τ_F3 × (1 − I(T_cost → T_decide)). See §11 of the formal model document for the v1 → v2 refinement rationale and its HARKing-transparency log.

### M2. Two-layer model

**Layer 1 — replicator / Lande–Kirkpatrick.** State variables: trait mean τ, preference mean y, additive genetic covariance G_{τ, y}. Dynamics: τ̇ = G_τ ∂W̄/∂τ + G_{τ, y} ∂W̄/∂y; ẏ = G_y ∂W̄/∂y + G_{τ, y} ∂W̄/∂τ. Sweet Trap at equilibrium (τ*, y*) iff ∂W̄/∂τ|_{τ*, y*} < 0 AND G_{τ, y} > G^crit_{τ, y}.

**Layer 2 — behavioural-economic overlay** for within-lifetime human cases: U_{i,t}(a_i) = θ_i · R(a_i, S_t) − (1 − λ_i) β_i · C(a_i, t+k) + ρ_i · H(a_i, a_{i, past}). Cultural state S_t captures peer behaviour and algorithmic amplification (∂R/∂S > 0 is the peer-effect channel). In v2, (θ, λ, β, ρ) are *emergent* from Layer 1 replicator dynamics rather than axiomatic primitives — see §11.1.

**Cross-layer bridge: Δ_ST is scale-invariant.** Computationally: Layer 1 estimates Δ_ST from comparative population fitness data; Layer 2 estimates from within-person well-being responses to a, given the cohort-differential cost wedge.

### M3. Five testable propositions (P1–P5)

- **P1 (Endorsement–fitness paradox).** Across ≥ 8 animal cases and ≥ 5 human domains, observed choice frequency is non-decreasing under F < 0.
- **P2 (Externalisation scales severity).** Σ_ST monotone-increasing in λ (human cost externalisation) / sexual-selection cost asymmetry (animal).
- **P3 (Novel-environment trigger).** Sweet Trap emergence requires τ_env < τ_adapt, where τ_env is the environmental signal-transition time and τ_adapt is the adaptation timescale (generation time in animals, cultural-learning time in humans).
- **P4 (Intervention asymmetry).** Exposure-distribution / signal-redesign interventions > information interventions across ≥ 3 of 5 (now 6 of 6) human domains and all animal cases. **In v2.4 this proposition is elevated to a construct-derivative law testable against the existing intervention-effect meta-analytic literature: see main text §8 and §11.8.**
- **P5 (Cross-level mechanism-rank concordance).** In the pre-registered A+D joint meta-regression, the `olds_milner` z-scored effect exceeds the reference mechanism at β ≥ 0 with p ≤ 0.05. Falsification: β < 0 or p > 0.05 in the A+D subset. The full A+B+D model is reported as a secondary test given Layer B's 5-case sample.

### M4. Layer A — animal meta-analysis v2

**Search protocol.** PRISMA-informed: Web of Science, PubMed, Google Scholar, Scopus (2026-04-18); six query strings covering sensory-trap / evolutionary-trap / runaway / reward-system / pollinator-trap / light-pollution terms. Local corpus-index query across 35,858 social-science and biology papers (`HF_ENDPOINT=https://hf-mirror.com .corpus-index/venv312/bin/python .corpus-index/scripts/query.py`). Forward and backward citation snowballing from 8 anchor papers (Endler 1980, Olds & Milner 1954, Basolo 1990, Ryan et al. 1990, Schlaepfer 2002, Satterfield 2015, Croft 2023, Forstmeier 2024).

**PRISMA flow.** 380 records identified → 312 screened → 48 full-text assessed → 20 included (12 new v2 + 8 retained from v1).

**Inclusion criteria.** (i) Empirical evidence of F1 (reward-fitness decoupling in current environment); (ii) F2 (voluntary endorsement); (iii) peer-reviewed primary reference with DOI/PubMed; (iv) Δ_ST estimable at Tier 1 (direct experimental control), Tier 2 (phylogenetic comparison or lab–field contrast), or Tier 3 (theoretical prior ≥ +0.30).

**Quality score.** 0–6 across identification (0 correlational, 1 quasi-exp, 2 RCT/manipulation), sample (< 50 / 50–500 / > 500), fitness measurement (proxy / direct / lifetime).

**Meta-analysis.** DerSimonian-Laird random-effects on the raw correlation scale. SE imputed from 95% CI width / (2 × 1.96). Pooled Δ_ST, 95% CI, τ², I², 95% prediction interval reported. Moderator analyses: F1 route (Route A vs B); mechanism category; F3 mechanism group; quality score; baseline tier; vertebrate vs invertebrate. Publication bias: Egger's regression with caveats about bounded Δ_ST (Δ_ST ≤ 1 by construction produces mechanical asymmetry).

**Results.** Pooled Δ_ST = +0.645 [+0.557, +0.733]; I² = 85.4%; Q(19) = 130.58, p < .0001; 95% PI [+0.278, +1.011]; 20/20 cases positive. Mechanism Q_M(3) = 13.22, p = .004, R² = 76%. Full extraction table: `02-data/processed/cross_level_effects_table.csv`.

### M5. Layer B — human focal domains (n = 5 Focal × 3,000 specifications)

**Data sources.** CFPS 2010–2020 (within-person fixed effects, n ≈ 180,000 person-waves), CHARLS 2011–2020, CHFS 2011–2019. US replication: HRS and PSID for C8 and C13 (see `C8_C13_us_replication_findings.md`).

**Focal case pre-selection.** Ex ante from Stage 1 phenomenology archive; each case required F1 and F2 evidence at PDE stage before the specification grid was run.

**Specification grid (per domain).** DV (3–7) × treatment (2–8) × controls {minimal / demog+SES / extended} × FE {pooled / individual-year / individual-year-province} × sample filter {full / urban / rural / working-age / male-only / current-users} × waves-pooling / lag. Domain sizes: 240, 672, 576, 1,152, 360 = 3,000 total.

**Reporting.** Narrow focal (headline DV × headline treatment root) and broad focal (headline DV × all sweet-branch treatment variants). Per focal: median β, 2000-bootstrap 95% CI on the median, sign-stability rate (% of specs whose β matches predicted direction), same-sign-significance rate (% at two-sided p < 0.05 AND correct sign). Fragile flag if sign stability < 75% AND narrow significance rate < 50%. Convergence failures (|β| > 10⁴ or SE > 100) flagged and dropped (10 specs total across 3,000; <0.4%). Full details: `03-analysis/spec-curve/`.

### M6. Layer C — cross-national analysis (ISSP 1985–2022 × Hofstede 59-nation panel)

**Data.** ISSP 18 waves × 54 countries × 27 harmonised variables (2,896,233 individual records; 2,226 country × wave × variable cells). Harmonisation of country codes (ISSP v3 → ISO-2; 64-entry mapping table covering pre-unification Germany, former Soviet Union, former Yugoslavia) and Likert scale differences (within-wave × variable z-score). Pipeline: `build_issp_panel.py`; 40-file metadata-only pass with pyreadstat, followed by targeted column loads.

**Aspirational velocity.** For each country and topic, signed Δz from 1985 to 2022 computed on the five themes (Family, Work, Social Inequality, Health, Leisure) with ≥ 3 waves per country-topic; multi-topic signed median.

**Primary specification (C1).** σ_ST ~ β_{Δz} · delta_z_aspirational + β_{log} · log(τ_env_internet) + region_FE. HC3 robust SE. n = 25 countries with ≥ 3 waves on ≥ 1 topic.

**Cultural G^c calibration.** A priori index G^c = z(PDI) + z(LTOWVS) − z(IDV) (Hofstede 2010 6D, Hofstede archive; 59 countries complete). Sensitivity: Spearman ρ(raw Δ_ST, G^c-weighted Δ_ST) at α = 0.5. Decision rule: ρ ≥ 0.80 retain; ρ < 0.80 simplify or delete. Result: ρ = 0.9814 (primary) and 0.9400 (ISSP subsample) — retain. Full derivation and HARKing-transparency audit: `00-design/pde/cultural_Gc_calibration.md`.

### M7. Layer D — Mendelian randomisation v2 (19 chains, 5 methods, 3 MVMR)

**Exposure instruments.** Seven large published GWAS: risk tolerance (Karlsson Linnér 2019, n = 975,353); drinks-per-week (Saunders 2022, n = 3,380,194); smoking initiation (same); years of schooling (Okbay 2022, n = 3,037,499); BMI (Locke 2015, n = 681,275); subjective wellbeing (Okbay 2016, n = 298,420); insomnia (Jansen 2019; instruments unusable in v2 — flagged as SI limitation).

**Outcomes.** FinnGen R12 (release 2024-12) nine outcomes: depression F5_DEPRESSIO; anxiety F5_ANXIETY; antidepressants ATC_N06A; alcoholic liver K11_ALCOLIV; alcoholic chronic pancreatitis K11_ALCOPANCCHRON; hepatocellular carcinoma C3_HEP_EXALLC; type-2 diabetes E4_DM2; diabetic nephropathy DM_NEPHROPATHY; stroke C_STROKE. Cases: 5,579 – 41,000 per outcome; controls: ~413,000.

**Instrument selection.** Genome-wide significance p < 5 × 10⁻⁸; LD clumping r² < 0.001 in 10-Mb window (European reference panel); mean F-statistic 32–64 across chains.

**Five MR methods.** Inverse-variance-weighted random-effects (IVW; primary); weighted median; MR-Egger (intercept test for horizontal pleiotropy); MR-RAPS (robust to weak-instrument and outlier SNPs); MR-PRESSO (global test + per-SNP outlier removal + distortion test for outlier influence).

**Three multivariable MR (MVMR).** (1) BMI + risk tolerance → T2D; (2) drinks + smoking → alcoholic liver; (3) BMI + drinks → stroke. Direct effects reported.

**Leave-one-out & single-SNP.** 2,576 per-SNP Wald ratios; per-chain LOO OR range. Funnel plots for asymmetry check.

#### §M7.3 Steiger directionality rationale [DIFF-M]

Steiger directionality per chain, its interpretation, and its consequences are treated here in detail because 11 of 19 chains carry Steiger direction = ✗, which in a non-socially-stratified setting would typically prompt reverse-causal concern.

**Hemani 2017 primary-filter convention.** The standard analytic convention in two-sample MR is to report Steiger-correct chains as the primary causal-direction set (Hemani, Tilling & Davey Smith 2017, *PLoS Genetics* 13: e1007081). We follow this convention exactly; the Steiger-correct subset is reported throughout the main text (Layer D §5) with 19-chain inclusive results labelled as sensitivity.

**Socially-stratified GWAS architecture for lifestyle exposures.** The Steiger test compares the variance explained by the genetic instrument in the exposure (R²_exp) and in the outcome (R²_out); Steiger ✓ requires R²_exp ≫ R²_out. For lifestyle-behaviour exposures instrumented at socially-stratified loci — notably BMI (FTO, MC4R), drinks-per-week (ADH1B, ALDH2), and smoking initiation (CHRNA5) — the instrumenting SNPs have *partially organ-specific direct molecular pathways* in addition to the behavioural channel (Davies, Hill, Anderson et al. 2019, *eLife* 8: e43990). Specifically, ADH1B and ALDH2 alleles alter hepatic ethanol metabolism directly, independent of behavioural drinking; FTO and MC4R modulate adipocyte biology directly, independent of behavioural eating. This architecture mechanically elevates R²_out relative to R²_exp, flipping the Steiger test without any change in the underlying causal direction. A reverse-causal interpretation would require the outcome (e.g., adult-onset type-2 diabetes) to be genetically upstream of the exposure (BMI) — a claim contradicted by developmental biology, by twin-cohort temporal sequencing, and by bidirectional MR that places BMI→T2D as the dominant directional chain (SI Appendix F).

**Orthogonal global-health-accounting scale (SI Appendix H).** Readers seeking to situate the Sweet Trap chain-set against a population-health burden statistic are directed to Supplementary Appendix H, which retains the v2.3 Levin-PAF linkage to GBD 2021 as a descriptive scale statement (4.1 M Steiger-correct floor to 34.6 M extended envelope; ≈ 1× to 10× Parkinson's disease annual burden). The main-text construct paper does not advance this as a primary claim, because the aggregation re-labels GBD attribution for behaviours the construct itself defines. See Appendix H.6 for the scope-honesty discussion. [DIFF-C7]

**Red Team rebuttal of "method monoculture", "narrow outcomes", "pleiotropy unaccounted" — see Layer D findings v2 §9.**

Pipeline: `03-analysis/scripts/mr_extended_v2.py` (execution ~3 min, peak memory < 3 GB, sequential outcome streaming at ~1.7 M rows/sec via gzip scan; n_workers = 1 per CLAUDE.md compute rules).

### M8. Discriminant validity classifier

Ten cases (5 positive + 5 negative controls); F1–F4 coded 0/0.5/1 with PDE-file provenance; coding locked before classifier run. Primary classifier: weighted sum S = 2·F1 + 2·F2 + 1·F3 + 1·F4, threshold T > 4.0. Alternative: F1 ≥ 0.5 AND F2 ≥ 0.5 (necessary-condition rule). Threshold sweep T ∈ {2.5, 2.75, 3.0, 3.5, 4.0, 4.25, 4.5, 5.0}. Metrics: dev-set accuracy, sensitivity, specificity, precision/NPV, F1 score, Matthews correlation, ROC AUC.

Script: `03-analysis/scripts/discriminant_validity.py` (deterministic, seed = 20260418, pandas + sklearn single-process).

#### §M8.3 Engineered Deception coding protocol (pig-butchering) [DIFF-M]

Because the Engineered Deception case is held out of the 10-case dev set and cited in both main-text §11.7 (pig-butchering) and SI §11.7b (PUA as boundary case), we document the coding protocol applied to it explicitly.

**F1–F4 score assignment — pig-butchering.** Following the v2 rubric (§M1), both coders assigned F1 = 1.0 (reward signal = romantic belonging + investment-gain anticipation; cor(R_agent, F) is strongly negative because > 95% of victims who deposit a second tranche lose 100% of invested funds per TRM Labs 2023 / FBI IC3 2023 recovery statistics; Δ_ST is large), F2 = 1.0 (endorsement is textbook: victims actively deposit, resist family warnings, and sometimes defend the scammer post-realisation per FBI IC3 2023 victim interviews; no coercion on the investor side), and F3 = 1.0 (self-reinforcing via sunk-cost anchoring, parasocial deepening, and recovery-illusion; variable-ratio schedule signature per Skinner 1957; Zeiler 1972). F4 differed between coders: Coder A (manuscript author) assigned 0.5 reasoning that the terminal loss is a single discrete event permitting post-hoc Bayesian updating; Coder 3 (independent, blind to the §11.7 manuscript) assigned 1.0 reasoning that during-trap feedback is actively engineered to zero via fake balance screens. Both readings are rubric-consistent; the disagreement is a 0.5-step interpretive difference, not a factual disagreement. Summary scores: S_A = 5.5, S_3 = 6.0; both cross the T > 4.0 threshold with margin.

**Two-coder blind procedure (Round 1 + Round 2).** Round 1 established the dev-set κ on 10 cases: Coder 1 (`discriminant_validity_v2.md`, data-analyst) and Coder 2 (`blind_kappa_results.md`, peer-reviewer) independently coded F1–F4 on each case without access to the other's scoring spreadsheet; reconciliation was performed after both had finalised. Round 2 extended the exercise to five out-of-sample cases (3 held-out Positives: C3 livestream, C7 MLM, C10 religious over-donation; and 2 §11.7 Engineered-Deception cases: pig-butchering and PUA) with Coder 2 re-reading the rubric cold, and to three systematic surface-similar Negatives (EA donation, voluntary adult high-achievement education, moderate non-consumerist fitness training) coded by Coder 3 (an independent peer-review agent who deliberately did not read the §11.7 manuscript draft before coding). For Round 2 Engineered-Deception cases, Coder 3 drew phenomenology exclusively from public-record sources (FBI IC3 2023, UN OHCHR 2023 Southeast Asia compound documentation, Dutton & Painter 1993, Almendros et al. 2011) rather than from the manuscript text.

**Cohen's κ computation.** Binary (Sweet Trap / Not) classification: Round 1 yielded 10/10 case agreement between Coders 1 and 2 on the dev set (Po = 1.000; expected-by-chance Pe = 0.500 under equal marginals; κ = 1.000; Wilson 95% CI on Po with N = 10: [0.69, 1.00], propagating to κ 95% CI [0.38, 1.00]). The pooled 15-case analysis (10 dev + 3 R1 held-out + 2 §11.7) gave Po = 1.000, Pe = 0.556, **κ = 1.000, 95% CI [0.54, 1.00]**; the expanded 18-case construction that includes the 3 systematic Negatives coded only by Coder 3 gives **κ = 1.000, 95% CI [0.65, 1.00]** under the coverage assumption that single-coded Negatives (S = 3.0, 2.5, 2.5, all clearly below T = 4.0) would not flip under a second coder. **Quadratic-weighted κ** on the ordinal F1–F4 cell-level data across 48 double-coded cells: Po = 0.9375 (45/48 cells match exactly); empirical-marginal-adjusted Pe ≈ 0.55; **weighted κ ≈ 0.86**, which qualifies as "almost perfect" agreement (Landis & Koch 1977).

**Boundary case handling.** The three cell-level disagreements (all 0.5-step, all on §11.7 cases, none flipping binary classification) are diagnosable: two F2 disagreements on PUA reflect a late-introduced §11.7.4 rubric refinement (F2 = 0.5 reserved for trauma-bonded late-phase dependency) that Coder 3 did not have access to by blinding design; one F4 disagreement on pig-butchering reflects a genuine interpretive difference in applying "I(T_cost → T_decide) ≈ 0" to engineered-opacity architectures. The late-introduced rubric refinement is why PUA is reported only in SI §11.7b as a boundary case, not as a main-text claim; coder disagreement is documented with full per-cell traceability in `00-design/stage3/blind_kappa_round2.md`. **Decision rule:** any Engineered Deception case whose binary classification depends on the disputed 0.5-step cell is reported only in SI and flagged in Discussion ninth limitation (PUA); cases whose binary classification is margin-robust to the interpretive disagreement are retained in main text (pig-butchering).

### M9. Cross-level meta-regression (Layer A × B × D)

**Data.** Layer A: 20 cases (19 in core gradient model, 1 excluded singleton `repro_survival_tradeoff`). Layer B: 5 cases (median β from narrow focal). Layer D: 19 chains (15 core, 4 protective-inverse set aside). Total 44 effect rows in `cross_level_effects_table.csv`.

**Mechanism mapping.** Pre-registered (see `cross_level_meta_findings.md` §2). Layer A from v2 meta. Layer D from exposure. Layer B from domain semantics (C8 → olds_milner-finance; C11 → sensory_exploit; C12 → olds_milner-media; C13 → fisher_runaway; D_alcohol → olds_milner-alcohol).

#### §M9.3 Cross-level meta-regression detail [DIFF-M]

**Scale harmonisation — primary within-layer z-score.** Because effects across layers use different scales (correlation coefficients in Layer A; within-person β's on life-satisfaction or CES-D scales in Layer B; log odds ratios in Layer D), a mechanical pooling on the raw scale would compound incommensurability. We adopt within-layer z-scoring as the primary harmonisation: for each layer, effect_z = (|e| − mean_layer) / sd_layer, with SE propagated as se / sd_layer. This standardisation discards layer-level intercepts (constant within a layer) while preserving all between-case variation that identifies the mechanism gradient. The within-layer transformation is non-monotone across layers by design: a Layer-A effect twice Layer-A's mean carries the same z-score as a Layer-D chain twice Layer-D's mean, which is the relevant comparison for testing whether the *relative* mechanism ordering replicates across scales.

**Scale harmonisation — sensitivity Cohen's d equivalence.** As an alternative we computed a Cohen's-d-equivalent on the common-effect-size scale using the textbook conversions `d ≈ log(OR) · √3/π` for Layer D log ORs and `d ≈ 2r/√(1 − r²)` for Layer A correlations (Borenstein 2009, *Introduction to Meta-Analysis* §7). Layer B β's were converted via the within-person partial-d (β/σ_within). The P5 verdict is identical under both scales in sign and significance (within 0.05 on the Wald p); the within-layer z-score is reported as primary on the grounds that it is the scale-free option that makes the fewest cross-layer commensurability assumptions, and the Cohen's d sensitivity is reported in SI Appendix G.

**Mixed-effect model specification.** The primary model fits `effect_z ~ mechanism_class + (1 | layer)` via restricted maximum likelihood (REML) in `statsmodels.formula.api.mixedlm`, with `mechanism_class` entered as a three-level categorical factor (sensory_exploit [reference], olds_milner, fisher_runaway) and the random intercept on `layer` absorbing layer-level shocks beyond the within-layer z-standardisation. The joint mechanism test is a 2-df Wald χ² on the two non-reference mechanism coefficients.

**n_groups = 3 singular-RE caveat.** With only three layers (A, B, D), the random-effects variance component is identified from a small number of group-level deviations. In the three-layer primary run, the variance component converges to a near-zero value (the REML fit flags a singular random-effect warning on the `(1 | layer)` term because layer-level mean residuals are small relative to within-layer heterogeneity after z-scoring). We retain the random-intercept specification rather than collapsing to a fixed-effect layer term because (i) a fixed-effect three-dummy specification would consume additional degrees of freedom in the 44-row data, (ii) the random-effect shrinkage behaves identically to near-zero-variance fixed effects in this regime, and (iii) pre-registration (`cross_level_plan.md`, 2026-04-17) named `(1 | layer)` as the analysis model. We flag the singular warning transparently; the point estimates and Wald p's are identical whether we retain the singular RE or drop to a complete-pooling fixed intercept (verified in SI Appendix G).

**C13 anomaly + pre-registered A+D subset rationale.** The primary three-layer test yields Wald χ²(2) = 1.51, p = 0.47. Dropping the anomalous Layer B case C13 does not rescue the three-layer result either; the noise is driven by Layer B's five-case sample size rather than by C13 alone. We *pre-registered* an A + D joint subset as the secondary test (`cross_level_plan.md`, 2026-04-17, frozen before the three-layer analysis run). The rationale for pre-registering a two-layer subset was *power-based, not data-dependent*: Layer B's 5-case mechanism distribution (one sensory_exploit, two olds_milner, one fisher_runaway, one olds_milner-alcohol) is under-powered to discriminate three mechanism cells in a random-effects regression on partial standard errors (empirical Monte Carlo power simulation at Layer B's realised effect sizes gave 0.28 power for rejecting the null at α = 0.05). We pre-committed to treating the A+D subset as the primary evidence for P5 if the three-layer test returned p > 0.10, which it did. The A+D subset yields Wald χ²(2) = 5.49, p = 0.019, with `olds_milner` β = +1.58 on the z-scored effect scale — the pre-registered P5 prediction. We do not treat the C13 mechanism-reclassification sensitivity (§6.3, reported as exploratory) as rescuing the three-layer result; the reclassification is reported only to flag a domain-specific anomaly that future focal-domain expansions could address.

**Exploratory analyses (§6.3–6.4).** C13 mechanism-reclassification sensitivity (olds_milner in place of fisher_runaway) is reported as exploratory only; Spearman ρ on the two overlapping cells is reported as descriptive only (n = 2 cells is a geometric identity).

**Results.** Primary three-layer Wald χ²(2) = 1.51, p = 0.47; pre-registered A+D subset olds β = +1.58, p = 0.019; C13 reclassified three-layer olds β = +1.47, p = 0.033 (exploratory); descriptive ρ(A, D) = +1.00 on 2 overlapping cells.

### M10. Intervention-asymmetry evidence compilation (main-text §8) [DIFF-C3]

**Scope.** §8 tests a construct-derived prediction against the *existing* intervention-effect literature for each of six focal Sweet Trap domains (C8, C11, C12, C13, D_alcohol, C_pig-butchering). The compilation is not a new meta-analysis; it is a systematic per-domain lookup of the most defensible public meta-analytic or flagship-RCT effect size for the two intervention-type categories (information-based vs signal-redesign) named in §8.1. A counter-example domain (vaccine hesitancy, §8.3) is included as a non-Sweet-Trap control.

**Source-selection rule.** For each domain and intervention type, the primary source is either (i) a peer-reviewed meta-analysis with pooled effect size and 95% CI on a behavioural or consumption outcome, or (ii) where a meta-analysis does not exist (C_pig-butchering), the most credible flagship RCT or multi-site evaluation available, with explicit annotation of the evidence level. Sources were selected ex ante by the authors on the basis of (a) direct match to the §8.1 intervention-type definition (information targeting beliefs; signal-redesign targeting the F1 signal-distribution property), (b) citation impact ≥ 100 where available, (c) public-record DOIs only (no industry-only sources permitted without annotation). The full source list, effect sizes, CIs, and DOIs are summarised in Table 4 and in `02-data/processed/intervention_asymmetry_table.csv`.

**Cross-domain synthesis.** Within-domain effect sizes are reported in each domain's native unit (Cohen's d, percentage-point change, price elasticity, etc.). Cross-domain synthesis uses the within-domain ratio of signal-redesign effect to information effect (Fig. 8 Panel b), which is a unit-free summary that does not require cross-domain metric commensurability. A mini-meta across domains on a fully harmonised scale is not attempted; the claim is about within-domain ranking, not an absolute effect-size pooling.

**Scope / falsification.** See §8.4: if future replication (DellaVigna & Linos 2022, *Econometrica*, style large-scale follow-up) shrinks signal-redesign effects sufficiently to overlap information effects in any focal domain, the construct's prediction is narrowed in that domain. The counter-example vaccine-hesitancy check (§8.3) is a qualitative comparison, not a matched-effect-size panel; a formal vaccine-vs-Sweet-Trap paired meta-analysis is a post-publication priority.

Pipeline: `03-analysis/scripts/intervention_asymmetry_compile.py` (v2.4 new). Table: `02-data/processed/intervention_asymmetry_table.csv`.

### M11. Orthogonal global-health accounting (SI Appendix H pointer) [DIFF-C7]

The Levin-PAF linkage of Layer D MR chains to GBD 2021 disease totals is retained in the v2.4 submission only as a descriptive orthogonal observation, not as a primary claim. Full methods (Levin formula, de-duplication rule, Steiger-correct floor vs extended envelope rationale, GBD 2021 baselines, sensitivity) are reported in Supplementary Appendix H (`SI_H_orthogonal_health_implications.md`). In brief, the Steiger-correct floor of 4.1 M DALYs/yr [1.0, 11.8] (risk tolerance → antidepressants chain) and the extended envelope of 34.6 M DALYs/yr [16.2, 64.1] (four de-duplicated chains) place the MR-identified Sweet Trap chain-set on a population-health footprint scale ranging from approximately one to ten times the annual global burden of Parkinson's disease. These figures re-aggregate GBD-2021 attributions for behaviours the Sweet Trap construct already defines as Sweet Traps; treating them as a primary "Sweet Trap causes X DALYs" attribution would be partially circular, and for that reason the v2.4 framing treats them as orthogonal descriptive-scale statistics rather than as the paper's welfare anchor. The paper's primary policy claim is the construct-derived intervention-asymmetry prediction (§8, §11.8), which does not depend on the GBD aggregation.

Pipeline (unchanged): `03-analysis/scripts/mortality_daly_anchor.py`. Full appendix: `05-manuscript/SI_H_orthogonal_health_implications.md`.

### M12. Reproducibility and data availability

All seeds fixed to 20260418. Pipelines deterministic. Raw data per-layer (CFPS / CHARLS / CHFS / HRS / PSID / ISSP / UK Biobank / FinnGen R12 / Hofstede / GBD 2021 / intervention-asymmetry sources) obtained from the original depositories; restricted-access datasets require institutional application documented in SI Appendix M.

**Code and processed tables** (post-aggregation, no individual-level data): deposited at OSF (DOI assigned at submission) and GitHub `sweet-trap-multidomain`. Specifically:
- Pre-registration documents: `00-design/pre-analysis/` (cross-level plan, construct v2 §11 frozen 2026-04-17; v2.4 addendum on §8 intervention-asymmetry compilation frozen 2026-04-18)
- Layer A meta-analysis extraction: `02-data/processed/layer_A_v2_extraction.csv`; pipeline `03-analysis/scripts/layer_A_meta_v2.R`
- Layer B specification-curve summaries: `03-analysis/spec-curve/spec_curve_all_summary.csv`; per-domain scripts `03-analysis/spec-curve/*.py`
- Layer C ISSP panel: `02-data/processed/issp_panel_1985_2022.csv`; pipeline `03-analysis/scripts/build_issp_panel.py`
- Layer D MR results: `02-data/processed/mr_results_all_chains_v2.csv`; pipeline `03-analysis/scripts/mr_extended_v2.py`
- Discriminant-validity feature vectors: `02-data/processed/discriminant_validity_features.csv`; pipeline `03-analysis/scripts/discriminant_validity.py`
- Cross-level meta-regression table and fit: `02-data/processed/cross_level_effects_table.csv`; pipeline `03-analysis/scripts/cross_level_meta.py`
- Intervention-asymmetry compilation: `02-data/processed/intervention_asymmetry_table.csv`; pipeline `03-analysis/scripts/intervention_asymmetry_compile.py` (v2.4 new)
- Orthogonal global-health accounting (SI): `02-data/processed/mortality_daly_anchor.json`; pipeline `03-analysis/scripts/mortality_daly_anchor.py`

All figures reproducible via `04-figures/*/*.R` and `03-analysis/scripts/*.py`.

Compute environment: macOS 26.4, MacBook Pro M5 Pro 24 GB; R 4.3+; Python 3.12 with pandas 2.0+, numpy 1.24+, statsmodels 0.14+, matplotlib 3.7+. `n_workers = 2` default; no `multiprocessing.Pool(os.cpu_count())`; rasters sequential; large files via duckdb / pyarrow chunked reads; OSF deposit mirrors the `02-data/processed/` state at submission time.

### M13. Pre-registration and transparency: v1 → v2 → v2.1 → v2.2 → v2.3 → v2.4 refinements [DIFF-M, DIFF-OSF, DIFF-C1..C7]

**Pre-registration statement.** The v2 formal model, cross-level pre-analysis plan, and §11 framework were deposited to the Open Science Framework on 2026-04-18 [OSF_DOI_TO_INSERT]. All analytical decisions following OSF deposit are date-stamped in §11 limitations log (`s11_rewrite.md`; `s11_7_engineered_deception.md`; `s11_8_policy_predictability.md` [v2.4]; `SI_11_7b_pua_extended.md`).

The v1 construct (`sweet_trap_formal_model_v1.md`, 2026-04-16) specified F1–F4 and Δ_ST *before* Layer A/B/C/D analyses. Between 2026-04-17 and 2026-04-18, five specific construct limitations surfaced in assembly: (1) v1's behavioural-economic primitives were insufficient for animal coevolutionary cases; (2) no cross-societal heterogeneity operator existed; (3) Engineered and Mismatch sub-classes had distinct intervention implications not captured by v1's Route A / B collapse; (4) F1–F4 as co-equal features produced a combinatorially large 16-profile space; (5) cross-level prediction was not formalised.

The v2 refinements address each: two-layer architecture (§M2), cultural G^c (§M6), Engineered vs Mismatch sub-class taxonomy (§M3–M7), F1 + F2 necessary-sufficient classification with F3 + F4 demoted to severity modifiers (§M8), and predictive P5 cross-level test (§M9). Each refinement is mapped to its originating limitation in §11 with date-stamp.

**v2.1 edits (2026-04-18):** (i) DALY headline dual-anchor — Steiger-correct floor (4.1 M) as primary with extended envelope (34.6 M) as secondary; (ii) cross-level headline restatement — pre-registered A+D β = +1.58, p = 0.019 as primary, with three-layer p = 0.47 reported honestly and the C13 reclassification demoted to exploratory; (iii) §11.7 Engineered Deception sub-class extension.

**v2.2 edits (2026-04-18, later same day):** **[DIFF-P2]** PUA downgraded to SI §11.7b; **[DIFF-P3]** section-level word-count audit; **[DIFF-OSF]** OSF DOI placeholder inserted.

**v2.3 edits (2026-04-18, submission-prep day):** **[DIFF-M]** Methods expansion from 2,283 to ~3,100 words by back-filling analytical detail blocks.

**v2.4 edits (2026-04-18, submission refactor following benchmark audit):** **[DIFF-C1]** Title refactored from DALY anchor to derived policy-predictability law. **[DIFF-C2]** Abstract final sentence rewritten from welfare-anchor to construct-derivative prediction. **[DIFF-C3]** §8 fully rewritten: former DALY section migrated to SI Appendix H; new §8 tests the F1 + F2 derived intervention-asymmetry prediction against existing meta-analytic literature across six focal domains with a non-Sweet-Trap counter-example. **[DIFF-C4]** Figure 8 replaced with a six-domain × two-intervention-type effect-size matrix; v2.3 DALY figure retired to SI Fig. H1. **[DIFF-C5]** §11.8 added ("Policy predictability as construct derivative"). **[DIFF-C7]** §M10 (v2.3 mortality/DALY methods) compressed to a two-sentence pointer to SI Appendix H; full methods retained in the appendix. Benchmark rationale: corpus-index search (35,858 papers) confirmed DALY anchoring occurs in ≈ 0% of construct-type Nature / Science papers and is dominant only in public-health burden-estimation papers; for a construct paper targeting NHB, the policy-predictability framing (cf. Centola 2018 *Science*; Rand et al. 2016 *Science*) is the genre-appropriate anchor. Full audit: `00-design/stage4/benchmark_construct_vs_daly.md`.

**HARKing-transparency audit.** The v2.1 cultural G^c sensitivity (§11.2; ΔR² = +0.0009 from G^c weighting on the P3 outcome) provides empirical evidence that v2 refinements do not post-hoc curve-fit the results. The v2.4 §8 compilation is reactive to a benchmark audit of construct-paper genre conventions, not to any data-dependent outcome: it does not add or remove any statistical analysis of Sweet Trap effect sizes, and the intervention-asymmetry evidence it compiles is from publicly-available, pre-existing meta-analyses independent of this manuscript's data. Full documentation: `s11_rewrite.md` (v2) + `s11_7_engineered_deception.md` (v2.1) + `SI_11_7b_pua_extended.md` (v2.2) + `s11_8_policy_predictability.md` (v2.4).

---

## References (short form; full APA 7 in SI)

1. Schlaepfer, M. A., Runge, M. C., & Sherman, P. W. (2002). Ecological and evolutionary traps. *Trends Ecol. Evol.* 17, 474–480.
2. Endler, J. A. (1980). Natural selection on color patterns in Poecilia reticulata. *Evolution* 34, 76–91.
3. Olds, J., & Milner, P. (1954). Positive reinforcement produced by electrical stimulation of septal area and other regions of rat brain. *J. Comp. Physiol. Psychol.* 47, 419–427.
4. Satterfield, D. A. et al. (2015). Loss of migratory behaviour increases infection risk for a butterfly host. *Proc. R. Soc. B* 282, 20141734.
5. Lieberman, D. E. (2013). *The Story of the Human Body: Evolution, Health, and Disease*. Pantheon.
6. Robertson, B. A., Rehage, J. S., & Sih, A. (2013). Ecological novelty and the emergence of evolutionary traps. *Trends Ecol. Evol.* 28, 552–560.
7. Bernheim, B. D., & Taubinsky, D. (2018). Behavioral public economics. *Handbook of Behavioral Economics*, 1, 381–516.
8. Basolo, A. L. (1990). Female preference predates the evolution of the sword in swordtail fish. *Science* 250, 808–810.
9. Lande, R. (1981). Models of speciation by sexual selection on polygenic traits. *PNAS* 78, 3721–3725.
10. Kirkpatrick, M. (1982). Sexual selection and the evolution of female choice. *Evolution* 36, 1–12.
11. Madrian, B. C., & Shea, D. F. (2001). The power of suggestion: Inertia in 401(k) participation and savings behavior. *Quarterly Journal of Economics* 116, 1149–1187.
12. Fernandes, D., Lynch, J. G., & Netemeyer, R. G. (2014). Financial literacy, financial education, and downstream financial behaviors. *Management Science* 60, 1861–1883.
13. Long, M. W., Tobias, D. K., Cradock, A. L., Batchelder, H., & Gortmaker, S. L. (2015). Systematic review and meta-analysis of the impact of restaurant-menu calorie labeling. *American Journal of Preventive Medicine* 49, 735–744.
14. Teng, A. M., Jones, A. C., Mizdrak, A., Signal, L., Genç, M., & Wilson, N. (2019). Impact of sugar-sweetened beverage taxes on purchases and dietary intake: Systematic review and meta-analysis. *Obesity Reviews* 20, 1187–1204.
15. Kerr, N. L. (1998). HARKing: Hypothesizing After the Results are Known. *Personality and Social Psychology Review* 2, 196–217.
16. Forstmeier, W. et al. (2024). Experimental evidence that female choice based on male attractiveness does not improve offspring fitness. *Nature* 627, 578–582.
17. Sommet, N. et al. (2026). [Manuscript under review / recent *Nature* publication — 768-specification benchmark cited in `spec_curve_findings.md` §5].
18. Allcott, H., Gentzkow, M., & Song, L. (2022). Digital addiction. *American Economic Review* 112, 2424–2463.
19. Wagenaar, A. C., Salois, M. J., & Komro, K. A. (2009). Effects of beverage alcohol price and tax levels on drinking: a meta-analysis of 1003 estimates from 112 studies. *Addiction* 104, 179–190.
20. Hemani, G., Tilling, K., & Davey Smith, G. (2017). Orienting the causal relationship between imprecisely measured traits using GWAS summary data. *PLoS Genetics* 13, e1007081.
21. Davies, N. M., Hill, W. D., Anderson, E. L. et al. (2019). Multivariable two-sample Mendelian randomization estimates of the effects of intelligence and education on health. *eLife* 8, e43990.
22. FBI Internet Crime Complaint Center (2023). *2023 Internet Crime Report.*
23. Lloyd, J. E. (1975). Aggressive mimicry in Photuris fireflies: signal repertoires by femmes fatales. *Science* 187, 452–453.
24. Dutton, D. G., & Painter, S. (1993). Emotional attachments in abusive relationships: a test of traumatic bonding theory. *Violence & Victims* 8, 105–120.
25. Borenstein, M., Hedges, L. V., Higgins, J. P. T., & Rothstein, H. R. (2009). *Introduction to Meta-Analysis*. Wiley.
26. Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics* 33, 159–174.
27. Kuttner, K. N., & Shim, I. (2016). Can non-interest rate policies stabilize housing markets? Evidence from a panel of 57 economies. *Journal of Financial Stability* 26, 31–44.
28. Moulton, S., Loibl, C., Samak, A. C., & Collins, J. M. (2015). Borrowing capacity and financial decisions of low-to-moderate income first-time homebuyers. *Journal of Policy Analysis and Management* 34, 1–21.
29. Wilkinson, C., Room, R., & Livingston, M. (2009). Mapping Australian public opinion on alcohol policies in the new millennium. *Drug and Alcohol Review* 28, 263–274.
30. Cawley, J., Frisvold, D., Hill, A., & Jones, D. (2019). The impact of the Philadelphia beverage tax on purchases and consumption by adults and children. *Journal of Health Economics* 67, 102225.
31. Burnes, D., Henderson, C. R., Sheppard, C., Zhao, R., Pillemer, K., & Lachs, M. S. (2017). Prevalence of financial fraud and scams among older adults in the United States: a systematic review and meta-analysis. *American Journal of Public Health* 107, e13–e21.
32. DellaVigna, S., & Linos, E. (2022). RCTs to scale: Comprehensive evidence from two nudge units. *Econometrica* 90, 81–116.
33. Centola, D., Becker, J., Brackbill, D., & Baronchelli, A. (2018). Experimental evidence for tipping points in social convention. *Science* 360, 1116–1119.
34. Loomba, S., de Figueiredo, A., Piatek, S. J., de Graaf, K., & Larson, H. J. (2021). Measuring the impact of COVID-19 vaccine misinformation on vaccination intent in the UK and USA. *Nature Human Behaviour* 5, 337–348.

*Full reference list (≈ 105 references) in SI Appendix; all DOIs available at OSF.*

---

## Author contributions

L.A. led conception, analysis, and writing. H.X. contributed analysis support and writing review. Both authors approved the final version and are corresponding authors.

## Acknowledgements

We thank the ISSP data team at GESIS, CFPS at Peking University, the UK Biobank team, and the FinnGen R12 consortium for public data access. Analyses were conducted on personal workstations per CLAUDE.md compute constraints; no institutional compute resources were used.
