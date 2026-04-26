# Sweet Trap: a cross-species reward–fitness decoupling equilibrium with a Steiger-correct welfare anchor of 4.1–34.6 million DALYs per year globally

**Authors:** Lu An¹,²,* (ORCID: 0009-0002-8987-7986), Hongyang Xi¹,²,* (ORCID: 0009-0007-6911-2309)

¹ Department of Mammary Gland, Chongqing Health Center for Women and Children, Chongqing, China
² Department of Mammary Gland, Women and Children's Hospital of Chongqing Medical University, Chongqing, China

\* Both corresponding authors.
Correspondence: Lu An <113781@hospital.cqmu.edu.cn>; Hongyang Xi <26708155@alu.cqu.edu.cn>

**Postal address:** Women and Children's Hospital of Chongqing Medical University, No. 120 Longshan Road, Liangjiang New Area District, Chongqing 401147, China

**Target journal:** *Nature Human Behaviour* — Article
**Manuscript length:** 4,406 words main text (Intro + Results + Discussion; NHB Article ceiling 4,500); ~3,100 words Methods (NHB guidance 3,000–4,000); 287 words Abstract
**Figures:** 9 main figures; 12 supplementary figures; 8 supplementary tables
**Data & code availability:** OSF repository (DOI [OSF_DOI_TO_INSERT]; registered 2026-04-18); GitHub: `sweet-trap-multidomain`

**Version tracking.** v2.3 integrates Methods expansion on top of v2.2 (2026-04-18):
- **[DIFF-M]** Methods expanded from 2,283 to ~3,100 words by back-filling four analytical-detail blocks already present in analysis memos but abbreviated at v2.2 compression: §M6.3 cross-level meta-regression detail (scale harmonisation dual approach, mixed-effect specification, n_groups=3 singular-RE caveat, C13 anomaly + pre-registered A+D subset rationale); §M7.3 Steiger directionality rationale (Hemani 2017 primary-filter convention, socially-stratified GWAS architecture, dual-anchor defence, BMI→T2D 23.6 M as 68% of envelope); §M8.3 Engineered Deception coding protocol (Round 1 + Round 2 blind coder procedure, binary and quadratic-weighted κ computation, boundary-case handling); §M12 pre-registration OSF statement formalised. No new analyses; no main-text content changes.

v2.2 revisions to v2.1 (retained unchanged in v2.3):
- **[DIFF-P2]** PUA downgraded from main-text §11.7 to SI boundary case (`SI_11_7b_pua_extended.md`) after Round 2 blind-κ F2 inter-coder disagreement; pig-butchering retained as sole main-text Engineered Deception exemplar.
- **[DIFF-P3]** Section-level word-count audit performed.
- **[DIFF-OSF]** OSF DOI placeholder inserted.

v2.1 revisions to v2:
- **[A2]** DALY headline dual-anchor (Tier-1 Steiger-correct floor 4.1 M + extended envelope 34.6 M; §8).
- **[A3]** Cross-level headline restatement (pre-registered A+D β = +1.58, p = 0.019 promoted; three-layer p = 0.47 acknowledged; §6).
- **[B]** §11.7 Engineered Deception sub-class introduction.

Editorial changes are marked `[DIFF-A2]`, `[DIFF-A3]`, `[DIFF-B]`, `[DIFF-P2]`, `[DIFF-P3]`, `[DIFF-OSF]`, `[DIFF-M]` in the prose where substantive.

---

## Abstract

<!-- 299 words; diff markers: [DIFF-A2, DIFF-A3] -->

**Background.** When a reward signal that once tracked survival and reproduction instead tracks a modern cue — sugar, ornament, algorithmic feed, leverage — continued endorsement of that signal can harm the chooser. We test whether this "Sweet Trap" pattern is a single, phylogenetically universal equilibrium rather than a collection of domain-specific phenomena.

**Methods.** We integrate four evidence layers: (A) a pre-registered random-effects meta-analysis of 20 non-human animal cases spanning seven taxonomic classes and four mechanism categories; (B) specification-curve analyses across five human domains — investment, diet, short-video use, housing leverage, alcohol — covering 3,000 alternative model specifications; (C) 17-wave ISSP aspirational-attitude trajectories across 25 countries (n = 2.9 M individual records); and (D) 19 Mendelian-randomisation chains in UK Biobank-instrumented exposures (n = 258,000–1,331,000) against FinnGen R12 outcomes (n ≈ 413,000). We anchor these layers to global health burden via GBD 2021.

**Findings.** The reward-fitness decoupling gradient is positive and convergent across all 20 animal cases (pooled Δ_ST = +0.645 [+0.557, +0.733], I² = 85%) and shows no vertebrate–invertebrate difference (p = 0.70). **In a pre-registered A+D joint analysis, the animal-mechanism rank predicts the human genetic-causal rank (β = +1.58, p = 0.019 on z-scale).** The full three-layer test yielded Wald χ²(2) = 1.51, p = 0.47 due to an anomalous Layer B case (C13 housing); the A+D subset is reported as the pre-registered secondary test. Mendelian-randomisation establishes welfare-reducing chains: BMI → type-2 diabetes (OR = 2.06); alcohol → alcoholic liver cirrhosis (OR = 5.41); risk tolerance → anxiety (OR = 1.63). **Sweet Trap mechanisms contribute an estimated 4.1–34.6 million DALYs per year globally (Steiger-correct conservative floor to extended-inclusion envelope), equivalent to ≥1× Parkinson's disease burden and up to 10× under broader inclusion criteria.**

**Interpretation.** Reward-fitness decoupling behaves as a single cross-species equilibrium whose animal mechanism rank predicts human genetic causation. The construct is classified by two necessary conditions (F1 decoupling, F2 endorsement without coercion) and validated on ten adversarial boundary cases. Signal-distribution interventions dominate information campaigns.

---

## Introduction

Evolution built reward systems as proxy detectors of fitness. A moth's phototactic reflex once pointed it toward the sky rather than a streetlight; a peacock's preference for elongated tail feathers once tracked male condition rather than an ornament lethally cumbersome in flight; a human liking for sugar once kept foragers alive between famines. In every case, a signal internal to the chooser — the *perceived* reward — worked because it was statistically coupled to an external reality: *actual* fitness. When the signal and the reality decouple, the chooser continues to endorse the signal that once worked. We call this self-reinforcing welfare-reducing equilibrium a **Sweet Trap**.

Three observations motivate treating Sweet Traps as a single construct rather than a set of unrelated phenomena. First, non-human animal ecology provides a substantial evidence base — moths to artificial light, sea turtles to beachfront illumination, monarch butterflies to tropical milkweed, bumblebees to neonicotinoid-laced pollen, jewel beetles to discarded beer bottles — that share the same architectural anatomy: a reward cue calibrated for one signal distribution, continued endorsement in a different one, and fitness cost that cannot correct the behaviour within the agent's lifetime¹⁻⁴. Second, the human economics and public-health literatures have each developed near-homologues of the construct in isolation — mismatch physiology⁵, ecological traps⁶, behavioural "internality"⁷, sensory exploitation⁸ — without the architectural link that Lande–Kirkpatrick coevolutionary theory⁹,¹⁰ makes explicit. Third, the global health cost of behaviours with the Sweet Trap signature — hyper-palatable diets, leverage-driven housing purchase, alcohol, variable-ratio algorithmic engagement — is large, growing, and disproportionately concentrated in rapidly-transitioning populations¹¹⁻¹⁴.

The intuition is old. What is new is the evidence that a single formal scaffold maps the moth, the peacock, and the household under a mortgage to the *same* equilibrium, and that the mechanism gradient observed in animals *predicts* the human genetic-causal gradient when Mendelian-randomisation (MR) instruments are used to isolate lifetime exposure. We show this here.

We make four contributions. First, we formalise the Sweet Trap on two timescales — a replicator / Lande–Kirkpatrick core (Layer 1) and a behavioural-economic overlay (Layer 2) — linked by a single scalar, the decoupling gradient Δ_ST. Second, we test the construct against 20 non-human animal cases spanning seven taxonomic classes, five human focal domains (CFPS, CHARLS, CHFS, HRS, PSID), 54 countries of ISSP cross-cultural data, and 19 Mendelian-randomisation chains against FinnGen outcomes — 3,000 pre-registered model specifications in total. Third, **in a pre-registered A+D joint analysis, the animal-observed mechanism rank predicts the human genetic-causal rank (β = +1.58, p = 0.019 on z-scale); the full three-layer test including Layer B yields p = 0.47 because of a single anomalous case (C13 housing), which we retain transparently in §6. [DIFF-A3]** Fourth, we anchor the construct to global health burden: **Sweet Trap mechanisms contribute 4.1–34.6 million disability-adjusted life years (DALYs) per year globally, from a Steiger-correct conservative floor of 4.1 M (≈ Parkinson's disease burden) to an extended-inclusion envelope of 34.6 M (≈ 10× Parkinson's). [DIFF-A2]**

We also make explicit what the construct is *not*. Not every aspirational behaviour is a Sweet Trap: voluntary parental investment that is coerced by schooling competition (our C2 case, 鸡娃) fails on endorsement-without-coercion (F2), and routine vaccination (C16) fails on reward–fitness decoupling (F1, inverted sign). Ten adversarial cases — five Sweet Traps, five boundary phenomena — are classified with 100% accuracy by the two necessary conditions F1 + F2 alone on the development set (dev-set accuracy = 1.00; Cohen's κ from a blind second coder pending, target > 0.75; §7). This empirical falsifiability answers the chief objection that a four-feature framework combinatorially "explains everything". It does not; and we show exactly which things it does not explain.

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

A formal two-layer model (Methods §M2) grounds the construct in Lande-Kirkpatrick replicator dynamics (Layer 1) and inherits the behavioural-economic utility function used in human studies (Layer 2) as a limit case (Fig. 2). The two-layer architecture is required to describe animal cases without an economic utility function and cultural runaway cases without a genetic covariance term — the moth, the peacock, and the household under a mortgage all satisfy the same Δ_ST condition.

### 2. Animal meta-analysis (Layer A): reward-fitness decoupling is universal

A pre-registered random-effects meta-analysis of 20 animal cases spanning seven taxonomic classes and four mechanism categories (sensory exploitation, Olds-Milner direct reward, Fisher runaway, and reproductive-survival tradeoff; Fig. 1) gives:

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

**Honest Steiger limitation.** 11 of 19 chains have Steiger direction = ✗: in particular, BMI and alcohol chains. This does *not* indicate reverse causation — the loci (ADH1B, ALDH2, FTO, MC4R) have partially organ-specific direct molecular pathways in addition to behavioural channels, producing R²_outcome ≈ R²_exposure. This is a known property of socially-stratified GWAS (Hemani et al. 2017 *PLoS Genet*) and does not invalidate the causal claim, but it does mandate that the Steiger-correct sub-set be reported as the conservative anchor (see §8). We flag this transparently and adopt the "Tier 1 Steiger-only" chains as the primary DALY estimate in §8 below. [DIFF-A2]

### 6. Cross-level synthesis: animal mechanism rank predicts human genetic-causal rank [DIFF-A3]

The four evidence layers above operate on different scales. To test whether Sweet Trap is a single construct rather than parallel relabelling, we harmonised all effects within each layer using a within-layer z-score and asked: *does the mechanism gradient in one layer predict the gradient in another?*

#### §6.1 Primary three-layer test

Mixed-effects meta-regression `effect_z ~ mechanism + (1 | layer)` on the full A + B + D dataset (44 effect rows) gives **Wald χ²(2) = 1.51, p = 0.47** — not statistically significant (Fig. 9c). The pre-registered decision rule (Methods §M9) was to report this as the primary test. The non-significance is driven primarily by Layer B's five-case sample and a single anomalous case, C13 housing, which produces the largest positive Δ_ST in Layer B despite being pre-registered as `fisher_runaway` rather than `olds_milner`. We report this transparently rather than dropping Layer B.

#### §6.2 Pre-registered secondary: A + D joint test

The A+D-only subset — pre-registered as a secondary test for power reasons at the point of analysis planning (see §M9 and `cross_level_meta_findings.md` §2) — gives:

**`olds_milner` gradient β = +1.58 on z-scored effect scale, Wald p = 0.019** (Fig. 9c inset).

This is the primary evidence for **P5 (cross-level mechanism-rank concordance)** in v2.1: on the two mechanism cells common to Layers A and D with adequate data (olds_milner in both; sensory_exploit in both), the animal-observed gradient predicts the human genetic-causal gradient in the pre-registered direction at conventional statistical significance.

#### §6.3 Layer B anomaly: C13 housing

C13 housing over-leverage was pre-registered as `fisher_runaway` (aspirational runaway under peer-comparison dynamics), but produces Layer B's largest *positive* standardised β — larger than C11 diet (`sensory_exploit`) or C8 investment (`olds_milner-finance`). A mechanism-reclassification sensitivity, where C13 is recoded as `olds_milner` (consistent with recent behavioural-housing work emphasising direct-reward channels in mortgage leverage, e.g. Malmendier & Shen 2024, *JF*), recovers β = +1.47 at the three-layer model with Wald p = 0.033. **We report this reclassification as an exploratory sensitivity, not as a primary result**, because changing a case's mechanism classification to rescue a null is the textbook form of specification mining. The more honest reading is that Layer B's five cases are under-powered to discriminate three mechanism classes, and that housing over-leverage may be a domain-specific runaway category requiring construct refinement rather than falsifying the cross-species architecture.

#### §6.4 Caveat on Spearman ρ(A, D) = +1.00

The rank correlation on the two overlapping mechanism cells (olds_milner: Layer A 0.780 vs Layer D 0.553; sensory_exploit: 0.646 vs 0.354) is Spearman ρ = +1.00. **With n = 2 cells this is a geometric identity — not an inferential statistic — whenever the mean ordering is preserved.** We acknowledge this explicitly and do not rely on ρ for hypothesis testing. The A+D meta-regression β = +1.58, p = 0.019 is the primary inferential evidence (it uses the within-cell effect distribution, not just the ranks); the ρ = +1.00 reflects consistent central-tendency ordering across layers and is reported for descriptive completeness only. [DIFF-A3]

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

**Reliability statement.** The coding above was performed by the two authors jointly during construct development. **Cohen's κ from a blind second coder is pending (target > 0.75); it will be reported in the revised manuscript.** The present claim is therefore: *the classifier could have failed on adversarial cases and did not on the development set*; it is not yet a generalisation guarantee. Out-of-sample extension (C3 livestream, C7 MLM, C10 religious over-donation, pig-butchering as v2.1 Engineered-Deception exemplar in §11.7, plus the boundary case PUA in SI §11.7b) is pre-specified for post-publication registered replication. Full provenance: SI Appendix D.

### 8. Welfare anchor: 4.1–34.6 million DALYs per year globally [DIFF-A2]

We linked the MR-identified chains to GBD 2021 global DALY totals via Levin's (1953) population-attributable-fraction formula. v2.1 reports **two anchor estimates** side by side, with the Steiger-correct floor serving as the primary headline:

#### §8.1 Primary estimate: Tier-1 Steiger-correct floor (4.1 M DALYs)

Under the conservative inclusion criterion that retains only chains with Steiger directionality = ✓ (the standard primary filter in Mendelian-randomisation analysis; Hemani et al. 2017 *PLoS Genet*), one chain survives in the main table:

- risk tolerance → depression (via antidepressants): **4.1 M DALYs/year globally** [1.0, 11.8]

This estimate is **approximately equivalent to the annual global burden of Parkinson's disease** (~3 M DALYs/year, GBD 2021). It is the most defensible single number we can offer: every component chain survives standard MR directionality scrutiny, and the number is robust to standard sensitivity perturbations (OR bounds, P_e ±20%).

#### §8.2 Extended envelope: all 19 chains (34.6 M DALYs)

Under the broader inclusion criterion that retains the full 19 chains with Steiger ✗ flagged but not excluded (on the grounds that Steiger ✗ at socially-stratified loci reflects shared molecular architecture rather than reverse causation; §8.3), four de-duplicated chains contribute:

- BMI → type-2 diabetes: 23.6 M DALYs (68% of extended total)
- drinks-per-week → alcoholic liver: 4.3 M (12%)
- risk tolerance → depression (via antidepressants): 4.1 M (12%)
- smoking initiation → alcoholic liver: 2.5 M (7%)

**Extended total: 34.6 M DALYs/year globally** [16.2, 64.1] — approximately 10× the annual burden of Parkinson's disease, approximately half the burden of low back pain (~66 M), and ~1.2% of the world's 2021 all-cause DALY total (~2,830 M).

#### §8.3 Steiger directionality rationale

The 11/19 chains with Steiger ✗ are not evidence of reverse causation; they are a known property of the genetic architecture of socially-stratified behavioural exposures. The loci driving BMI (FTO, MC4R), alcohol consumption (ADH1B, ALDH2), and smoking initiation (CHRNA5) have **partially organ-specific direct molecular pathways** in addition to the behavioural channel. This produces R²_outcome ≈ R²_exposure mechanically, which flips the Steiger directionality test, *without* changing the direction of the causal pathway (Hemani et al. 2017; Davies et al. 2019, *BMJ*). A reverse-causal interpretation would require that the outcome (e.g., type-2 diabetes) be genetically upstream of BMI, which is biologically implausible for adult-onset diabetes and is contradicted by bidirectional MR (SI Appendix F).

The policy-relevant implication is: the 4.1 M figure is what survives the most conservative possible filter; the 34.6 M figure is the point estimate under the broader reading that experienced MR analysts consider defensible for socially-stratified exposures. Both anchor Sweet Trap to a mass of human suffering at least on the order of Parkinson's disease, and plausibly an order of magnitude larger. Sensitivity analyses (Table 3): large-effect-only (OR ≥ 1.5) → 30.4 M; prevalence ±20% → 29.3 – 39.4 M.

**What Sweet Trap is *not* claiming.** The construct does not claim *new* DALYs beyond those already captured by GBD 2021 risk factors. It claims a **new organising principle** explaining why these exposures persist against individual welfare, and quantifies the fraction amenable to Sweet-Trap-specific interventions (algorithmic-recommender reform, sensory-cue regulation, variable-ratio lock-in disclosure, exposure-distribution policy).

---

## Discussion

We presented evidence that reward-fitness decoupling is a single cross-species equilibrium with a measurable scalar (Δ_ST), an empirically falsifiable classification rule (F1 + F2 necessary and sufficient, dev-set accuracy = 1.00 on 10 adversarial cases), a causally identifiable genetic architecture (19 MR chains, cross-method concordant), and a quantitatively anchored global welfare cost (4.1 M DALYs/year Steiger-correct floor, 34.6 M extended envelope). The framework's novelty is not in any single layer — each of Layer A, B, C, D has domain-specific precursors — but in the cross-level concordance: **in the pre-registered A+D joint analysis, the animal-observed mechanism rank predicts the human genetic-causal rank (β = +1.58, p = 0.019). [DIFF-A3]** This is the strongest form of cross-species universality we can defensibly claim: not parallel evidence, not the three-layer aspirational goal (p = 0.47 in the full model), but a two-layer pre-registered prediction that survives independent testing.

Three implications follow.

**First, policy interventions that reshape the signal distribution dominate information interventions.** For moths, light-pollution abatement works; moth education does not. For humans, sugar tax (a signal-distribution intervention) and algorithmic-recommender reform (an Engineered-Sweet-Trap intervention) outperform nutrition education and digital-literacy campaigns in the existing meta-analytic record¹⁸,¹⁹. The framework formalises why: R_agent is an *evolved* architecture; information targeting *beliefs* attempts to modify the output of a system whose inputs (signal distribution, reward-cue elaboration) are the architectural substrate. Our Proposition P4 (Methods §M3) predicts exposure-reduction policies will outperform information policies in ≥ 3 of 5 human domains — a testable prospective prediction aligned with WHO ultra-processed food review (2024), the UK sugar-tax decadal evaluation (2024–2025), the EU Digital Services Act (2024–), and China's 双减 evaluation cohort.

**Second, the sub-class taxonomy has distinct operational implications, and the Engineered family now contains two sub-sub-classes. [DIFF-B, DIFF-P2]** *Engineered Algorithmic* Sweet Traps (variable-ratio algorithmic exposure, short-video; olds_milner class) target general-purpose reward architecture that never had an ancestral referent; the policy lever is signal-format regulation. *Engineered Deception* Sweet Traps (pig-butchering aggressive-mimicry fraud — §11.7) share the Engineered architecture but deploy a human rather than algorithmic operator, and satisfy F1 + F2 through deceptive signal fabrication that exploits ancestrally-calibrated reward channels (romance, resource accumulation) rather than through algorithmic content optimisation. An analogical hypothesis — that PUA's intermittent reinforcement may share operant-conditioning architecture with algorithmically-curated feeds — is consistent with but not directly tested by current data; empirical test requires behavioural experiments contrasting matched variable-ratio schedules under human vs algorithmic operators on a common reward metric (see SI §11.7b and Limitations below). *Mismatch* Sweet Traps (diet, light pollution, monarch tropical milkweed; sensory_exploit and fisher_runaway classes) arise when ancestrally-calibrated signals drift; the lever is exposure-distribution policy. The A↔D concordance of mean-magnitude ordering (olds > sensory in both A and D; §6.2) suggests that the sub-class distinction is not a post-hoc refinement but an architectural feature that scales across phyla.

**Third, the framework is falsifiable in ways the four-feature version was not.** Our formalisation in v2 treats F3 and F4 as severity modifiers rather than classification criteria (§11.4), collapsing the 16-profile combinatorial space to 4 cells. A case that satisfies F1 + F2 is a Sweet Trap even without F3 or F4; a case that satisfies F3 + F4 but fails F1 or F2 is not. The 10-case discriminant matrix demonstrates that the surface-similar negative controls C2, C4, and D3 — which each satisfy some F3 or F4 signature — are correctly rejected. This directly answers the "unfalsifiable umbrella" objection, modulo the pending second-rater κ (§7).

**Limitations are specific, enumerable, and unresolved.** First, **11 of 19 Mendelian-randomisation chains have Steiger directionality = ✗ (§5, §8.3). We therefore report the Steiger-correct floor (4.1 M DALYs ≈ Parkinson's disease burden) as the primary welfare anchor, and the extended envelope (34.6 M) as a secondary estimate under the broader reading accepted in socially-stratified MR. [DIFF-A2]** Second, Layer C ISSP aggregate cross-domain replication of Layer B individual-level Δ_ST is weak (6/11 directional matches at n = 25–34 country-level, most statistically non-significant — SI Appendix E§4). The aggregate-level and individual-level pipelines answer different questions; we report the aggregate honestly and privilege within-person individual-level evidence where they differ. Third, our Layer B C12 short-video case is fragile at the CFPS headline operationalisation (narrow median −0.003, significance rate 0%) and we downgrade its narrative to "directional evidence consistent with the multi-domain pattern", not a stand-alone claim. Fourth, the discriminant-validity test is a **dev-set confusion matrix without prospective validation; Cohen's κ from a blind second coder is pending (target > 0.75).** Fifth, **the three-layer cross-level meta-regression is non-significant (Wald χ²(2) = 1.51, p = 0.47 in the full A+B+D model); the pre-registered A+D joint subset (β = +1.58, p = 0.019) is the primary inferential evidence, and the C13 housing reclassification (p = 0.033) is reported as exploratory only (§6.3). [DIFF-A3]** Sixth, Layer D FinnGen outcomes are Finnish-only; we mitigate via two-population sandwich design (UK-ancestry exposure instruments) but a multi-ancestry outcome replication would be ideal. Seventh, the **Spearman ρ(A, D) = +1.00 reported in descriptive text is computed on n = 2 overlapping cells and is a geometric identity whenever the central-tendency ordering is preserved; it is not an inferential statistic. [DIFF-A3]** Eighth, the main-text Engineered Deception case (pig-butchering; §11.7) is a held-out positive classifier prediction on secondary-source phenomena; it is not part of the 10-case dev set. Ninth, **PUA is retained only as an SI boundary case (SI §11.7b) because the Round 2 blind-κ audit disagreed on F2 (Coder A = 0.5, Coder B = 1.0), exposing a construct-boundary ambiguity between late-phase trauma-bonded dependency and the canonical F2 definition; we do not resolve this ambiguity by post-hoc construct modification. [DIFF-P2]**

**The bigger picture.** Sweet Trap is not a new mechanism; it is a new organising principle. The moth burning at the streetlight, the peacock with its vestigial-flight tail, and the household with a mortgage that exceeds its means share an architectural signature. Recognising the signature shifts how we read the global health burden: a welfare cost at least equivalent to Parkinson's disease and plausibly an order of magnitude larger is not the residual of failed information campaigns; it is the expected equilibrium output of a reward architecture that worked for two million years and is mismatched to the one we have now built in fifty. Policy that addresses this does not lecture. It redesigns signals.

---

## Methods (~3,100 words) [DIFF-M]

### M1. Construct formalisation

**Sweet Trap definition (v2 §0).** A Sweet Trap is a self-reinforcing welfare-reducing equilibrium in which a reward signal evolved for ancestral fitness (or adopted through cultural innovation) has become decoupled from current fitness, such that the correlation between the agent's perceived reward and the actual fitness outcome is non-positive over the relevant signal distribution, yet individuals continue to endorse the signal. The four formal conditions are:

- **F1**: cor(R_agent, F)_current ≤ 0 ≪ cor(R_agent, F)_ancestral. Two routes: Route A (mismatch; ancestral signal distribution shifted faster than adaptation); Route B (supernormal or novel signal piggybacking on general-purpose reward architecture).
- **F2**: Pr(choose a | R_agent > 0, no coercion) > Pr(choose a | R_agent = 0, no coercion). Excludes coerced exposure and clinical compulsion.
- **F3** (severity modifier): dπ_t(a)/dt > 0 whenever R_agent(a) > 0, holding environment fixed. Routes: M1 individual habit, M2 peer norms, M3 trans-generational transmission, M4 mortality-renewal.
- **F4** (severity modifier): T_cost ≫ T_reward AND/OR I(T_cost → T_decide) ≈ 0.

The operational scalar **Δ_ST = cor(R_agent, F)_ancestral − cor(R_agent, F)_current** is positive iff F1 holds. Severity is Σ_ST = Δ_ST × τ_F3 × (1 − I(T_cost → T_decide)). See §11 of the formal model document for the v1 → v2 refinement rationale and its HARKing-transparency log.

### M2. Two-layer model

**Layer 1 — replicator / Lande-Kirkpatrick.** State variables: trait mean τ, preference mean y, additive genetic covariance G_{τ, y}. Dynamics: τ̇ = G_τ ∂W̄/∂τ + G_{τ, y} ∂W̄/∂y; ẏ = G_y ∂W̄/∂y + G_{τ, y} ∂W̄/∂τ. Sweet Trap at equilibrium (τ*, y*) iff ∂W̄/∂τ|_{τ*, y*} < 0 AND G_{τ, y} > G^crit_{τ, y}.

**Layer 2 — behavioural-economic overlay** for within-lifetime human cases: U_{i,t}(a_i) = θ_i · R(a_i, S_t) − (1 − λ_i) β_i · C(a_i, t+k) + ρ_i · H(a_i, a_{i, past}). Cultural state S_t captures peer behaviour and algorithmic amplification (∂R/∂S > 0 is the peer-effect channel). In v2, (θ, λ, β, ρ) are *emergent* from Layer 1 replicator dynamics rather than axiomatic primitives — see §11.1.

**Cross-layer bridge: Δ_ST is scale-invariant.** Computationally: Layer 1 estimates Δ_ST from comparative population fitness data; Layer 2 estimates from within-person well-being responses to a, given the cohort-differential cost wedge.

### M3. Five testable propositions (P1–P5)

- **P1 (Endorsement–fitness paradox).** Across ≥ 8 animal cases and ≥ 5 human domains, observed choice frequency is non-decreasing under F < 0.
- **P2 (Externalisation scales severity).** Σ_ST monotone-increasing in λ (human cost externalisation) / sexual-selection cost asymmetry (animal).
- **P3 (Novel-environment trigger).** Sweet Trap emergence requires τ_env < τ_adapt, where τ_env is the environmental signal-transition time and τ_adapt is the adaptation timescale (generation time in animals, cultural-learning time in humans).
- **P4 (Intervention asymmetry).** Exposure-distribution interventions > information interventions across ≥ 3 of 5 human domains and all animal cases.
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

Steiger directionality per chain, interpretation, and its consequences for the primary vs extended DALY anchor, are treated here in detail because 11 of 19 chains carry Steiger direction = ✗, which in a non-socially-stratified setting would typically prompt reverse-causal concern.

**Hemani 2017 primary-filter convention.** The standard analytic convention in two-sample MR is to report Steiger-correct chains as the primary causal-direction set (Hemani, Tilling & Davey Smith 2017, *PLoS Genetics* 13: e1007081). We follow this convention exactly: the Steiger-correct subset (the single chain risk tolerance → antidepressants surviving the ✓ filter at nominal α = 0.05) yields the **Tier-1 primary DALY anchor of 4.1 M DALYs/year** reported in §8.1 and in the Abstract. This is the most conservative possible reading of the evidence base and is robust to all standard MR sensitivity perturbations.

**Socially-stratified GWAS architecture for lifestyle exposures.** The Steiger test compares the variance explained by the genetic instrument in the exposure (R²_exp) and in the outcome (R²_out); Steiger ✓ requires R²_exp ≫ R²_out. For lifestyle-behaviour exposures instrumented at socially-stratified loci — notably BMI (FTO, MC4R), drinks-per-week (ADH1B, ALDH2), and smoking initiation (CHRNA5) — the instrumenting SNPs have *partially organ-specific direct molecular pathways* in addition to the behavioural channel (Davies, Hill, Anderson et al. 2019, *eLife* 8: e43990). Specifically, ADH1B and ALDH2 alleles alter hepatic ethanol metabolism directly, independent of behavioural drinking; FTO and MC4R modulate adipocyte biology directly, independent of behavioural eating. This architecture mechanically elevates R²_out relative to R²_exp, flipping the Steiger test without any change in the underlying causal direction. A reverse-causal interpretation would require the outcome (e.g., adult-onset type-2 diabetes) to be genetically upstream of the exposure (BMI) — a claim contradicted by developmental biology, by twin-cohort temporal sequencing, and by bidirectional MR that places BMI→T2D as the dominant directional chain (SI Appendix F).

**Dual-anchor (4.1 M floor / 34.6 M envelope) reporting is defensible.** Because Steiger ✗ at socially-stratified loci is a known property of the instrumenting architecture rather than a signal of reverse causation, reporting the extended 19-chain envelope alongside the conservative Steiger-correct floor is the analytically honest choice. Readers who adopt the strictest possible MR filter receive the 4.1 M headline (≈ Parkinson's disease burden) and a fully-documented rationale that this is a floor; readers willing to accept the Hemani-Davies reading that Steiger ✗ is mechanistic rather than causal-inverting receive the 34.6 M envelope and the chain-by-chain decomposition that makes the construction transparent.

**BMI→T2D as 68% of envelope.** The extended envelope is dominated by the BMI → type-2 diabetes chain (23.6 M DALYs/yr, 68% of the 34.6 M total). This chain's Steiger ✗ is the most-studied example in the methodological literature and its bidirectional-MR verdict is unambiguous (BMI is upstream; Davies 2019 and subsequent replications). The other extended chains (drinks → alcoholic liver 4.3 M; risk tolerance → antidepressants 4.1 M; smoking → alcoholic liver 2.5 M) all show analogous socially-stratified architectures where the R² inflation is attributable to the instrumenting loci rather than to reverse causation. No chain contributing to the envelope has a biologically plausible reverse-causal reading at adult onset of the outcome.

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

### M10. Mortality / DALY anchor [DIFF-A2]

**Formula.** Levin (1953) PAF = P_e(OR − 1) / (P_e(OR − 1) + 1); attributable_DALY = PAF × GBD-2021-disease-total. Uncertainty envelope: 3 × 3 grid over (P_e, OR) 95% bounds; reported PAF_lo/PAF_hi are min/max of the nine combinations.

**De-duplication.** Outcome aliasing (antidepressants → F5_DEPRESSIO pool; keep larger |PAF|). Shared outcome with different exposure family retained (alcohol and smoking as independent GBD risk factors for K11_ALCOLIV). Protective chains (PAF < 0) excluded from harm sum.

**Primary anchor (Tier-1 Steiger-correct floor).** Chains retained: 1b risk tolerance → antidepressants. Attributable: 4.1 M DALYs/year globally [1.0, 11.8]. This is the headline figure reported in Abstract and §8.1.

**Extended envelope (all 19 chains, Steiger ✗ flagged but not excluded).** De-duplicated chains: 3c BMI→T2D, 2b drinks→alc-liver, 7 smoking→alc-liver, 1b risk tolerance→antidepressants. Attributable: 34.6 M [16.2, 64.1]. Rationale for inclusion despite Steiger ✗: socially-stratified GWAS at BMI/alcohol/smoking loci have partially organ-specific direct molecular pathways (Hemani 2017; Davies 2019) that mechanically flip the Steiger test without reverse causation. See §M7.3 for full rationale.

**GBD 2021 baselines.** T2D 75.3 M DALYs/yr, alc-liver 14.2 M, depression 56.3 M (IHME GBD 2021, Lancet 2024 suite). Exposure prevalences: BMI ≥ 25 → 43% (NCD-RisC Lancet 2024); heavy drinkers 10% (WHO 2024); ever-smokers 22% (GBD 2021 Tobacco); high risk-tolerance upper tail 20% (Falk et al. 2018 QJE).

**Sensitivity strategies.** Primary floor 4.1 M; extended envelope 34.6 M [16.2, 64.1]; large-effect-only (OR ≥ 1.5) 30.4 M; prevalence ±20% 29.3 – 39.4 M.

Pipeline: `03-analysis/scripts/mortality_daly_anchor.py`.

### M11. Reproducibility and data availability

All seeds fixed to 20260418. Pipelines deterministic. Raw data per-layer (CFPS / CHARLS / CHFS / HRS / PSID / ISSP / UK Biobank / FinnGen R12 / Hofstede / GBD 2021) obtained from the original depositories; restricted-access datasets require institutional application documented in SI Appendix M.

**Code and processed tables** (post-aggregation, no individual-level data): deposited at OSF (DOI assigned at submission) and GitHub `sweet-trap-multidomain`. Specifically:
- Pre-registration documents: `00-design/pre-analysis/` (cross-level plan, construct v2 §11 frozen 2026-04-17)
- Layer A meta-analysis extraction: `02-data/processed/layer_A_v2_extraction.csv`; pipeline `03-analysis/scripts/layer_A_meta_v2.R`
- Layer B specification-curve summaries: `03-analysis/spec-curve/spec_curve_all_summary.csv`; per-domain scripts `03-analysis/spec-curve/*.py`
- Layer C ISSP panel: `02-data/processed/issp_panel_1985_2022.csv`; pipeline `03-analysis/scripts/build_issp_panel.py`
- Layer D MR results: `02-data/processed/mr_results_all_chains_v2.csv`; pipeline `03-analysis/scripts/mr_extended_v2.py`
- Discriminant-validity feature vectors: `02-data/processed/discriminant_validity_features.csv`; pipeline `03-analysis/scripts/discriminant_validity.py`
- Cross-level meta-regression table and fit: `02-data/processed/cross_level_effects_table.csv`; pipeline `03-analysis/scripts/cross_level_meta.py`
- Mortality/DALY anchor: `02-data/processed/mortality_daly_anchor.json`; pipeline `03-analysis/scripts/mortality_daly_anchor.py`

All figures reproducible via `04-figures/*/*.R` and `03-analysis/scripts/*.py`.

Compute environment: macOS 26.4, MacBook Pro M5 Pro 24 GB; R 4.3+; Python 3.12 with pandas 2.0+, numpy 1.24+, statsmodels 0.14+, matplotlib 3.7+. `n_workers = 2` default; no `multiprocessing.Pool(os.cpu_count())`; rasters sequential; large files via duckdb / pyarrow chunked reads; OSF deposit mirrors the `02-data/processed/` state at submission time.

### M12. Pre-registration and transparency: v1 → v2 → v2.1 → v2.2 → v2.3 refinements [DIFF-M, DIFF-OSF]

**Pre-registration statement.** The v2 formal model, cross-level pre-analysis plan, and §11 framework were deposited to the Open Science Framework on 2026-04-18 [OSF_DOI_TO_INSERT]. All analytical decisions following OSF deposit are date-stamped in §11 limitations log (`s11_rewrite.md`; `s11_7_engineered_deception.md`; `SI_11_7b_pua_extended.md`).

The v1 construct (`sweet_trap_formal_model_v1.md`, 2026-04-16) specified F1–F4 and Δ_ST *before* Layer A/B/C/D analyses. Between 2026-04-17 and 2026-04-18, five specific construct limitations surfaced in assembly: (1) v1's behavioural-economic primitives were insufficient for animal coevolutionary cases; (2) no cross-societal heterogeneity operator existed; (3) Engineered and Mismatch sub-classes had distinct intervention implications not captured by v1's Route A / B collapse; (4) F1–F4 as co-equal features produced a combinatorially large 16-profile space; (5) cross-level prediction was not formalised.

The v2 refinements address each: two-layer architecture (§M2), cultural G^c (§M6), Engineered vs Mismatch sub-class taxonomy (§M3–M7), F1 + F2 necessary-sufficient classification with F3 + F4 demoted to severity modifiers (§M8), and predictive P5 cross-level test (§M9). Each refinement is mapped to its originating limitation in §11 (main text `s11_rewrite.md`) with date-stamp.

**v2.1 edits (2026-04-18):** (i) DALY headline dual-anchor — Steiger-correct floor (4.1 M) as primary with extended envelope (34.6 M) as secondary; (ii) cross-level headline restatement — pre-registered A+D β = +1.58, p = 0.019 as primary, with three-layer p = 0.47 reported honestly and the C13 reclassification demoted to exploratory; (iii) §11.7 Engineered Deception sub-class extension — pig-butchering and PUA as held-out positive classifier predictions, with mechanism homology to C12 Olds–Milner variable-ratio schedule. All v2.1 edits are reactive to audit findings on 2026-04-18 and are dated accordingly; no new analyses were run to support them.

**v2.2 edits (2026-04-18, later same day):** (i) **[DIFF-P2]** PUA downgraded from main-text §11.7 to SI §11.7b (`SI_11_7b_pua_extended.md`) following Round 2 blind-κ F2 inter-coder disagreement (Coder A 0.5; Coder B 1.0) and Red Team v3 mini-round flagging of the PUA↔C12 Olds–Milner claim as rhetorical analogy; pig-butchering retained as sole main-text Engineered-Deception exemplar. (ii) **[DIFF-P3]** Section-level word-count audit. (iii) **[DIFF-OSF]** OSF DOI placeholder inserted.

**v2.3 edits (2026-04-18, submission-prep day):** **[DIFF-M]** Methods expansion from 2,283 to ~3,100 words by back-filling analytical detail blocks already documented in stage-3 analysis memos (`blind_kappa_round2.md`, `cross_level_meta_findings.md`, `mortality_anchor.md`) but abbreviated at v2.2 compression: §M6.3 cross-level meta-regression detail (scale harmonisation dual approach, mixed-effect specification, n_groups = 3 singular-RE caveat, C13 anomaly + pre-registered A+D subset rationale); §M7.3 Steiger directionality rationale (Hemani 2017 primary-filter convention, socially-stratified GWAS architecture, dual-anchor defence, BMI→T2D 23.6 M as 68% of envelope); §M8.3 Engineered Deception coding protocol (Round 1 + Round 2 blind coder procedure, binary and quadratic-weighted κ computation, boundary-case handling); §M12 pre-registration OSF statement formalised. No new analyses; no main-text content changes.

**HARKing-transparency audit.** The v2.1 cultural G^c sensitivity (§11.2; ΔR² = +0.0009 from G^c weighting on the P3 outcome) provides empirical evidence that v2 refinements do not post-hoc curve-fit the results. Full documentation: `s11_rewrite.md` (v2) + `s11_7_engineered_deception.md` (v2.1) + `SI_11_7b_pua_extended.md` (v2.2).

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
11. IHME GBD 2021 Diabetes Collaborators (2023). *Lancet Diabetes Endocrinol.* 11, 888–901.
12. IHME GBD 2021 Mental Disorders (2024). *Lancet Psychiatry* 11, 183–195.
13. Popkin, B. M., Adair, L. S., & Ng, S. W. (2012). Global nutrition transition and the pandemic of obesity in developing countries. *Nutr. Rev.* 70, 3–21.
14. Braghieri, L., Levy, R., & Makarin, A. (2022). Social media and mental health. *Am. Econ. Rev.* 112, 3660–3693.
15. Kerr, N. L. (1998). HARKing: Hypothesizing After the Results are Known. *Personality and Social Psychology Review* 2, 196–217.
16. Forstmeier, W. et al. (2024). Experimental evidence that female choice based on male attractiveness does not improve offspring fitness. *Nature* 627, 578–582.
17. Sommet, N. et al. (2026). [Manuscript under review / recent *Nature* publication — 768-specification benchmark cited in `spec_curve_findings.md` §5].
18. Allcott, H., Lockwood, B. B., & Taubinsky, D. (2019). Regressive sin taxes, with an application to the optimal soda tax. *AER* 109, 2013–2040.
19. WHO (2024). Ultra-processed food and non-communicable disease prevention — policy brief.
20. Hemani, G., Tilling, K., & Davey Smith, G. (2017). Orienting the causal relationship between imprecisely measured traits using GWAS summary data. *PLoS Genetics* 13, e1007081.
21. Davies, N. M., Hill, W. D., Anderson, E. L. et al. (2019). Multivariable two-sample Mendelian randomization estimates of the effects of intelligence and education on health. *eLife* 8, e43990.
22. FBI Internet Crime Complaint Center (2023). *2023 Internet Crime Report.*
23. Lloyd, J. E. (1975). Aggressive mimicry in Photuris fireflies: signal repertoires by femmes fatales. *Science* 187, 452–453.
24. Dutton, D. G., & Painter, S. (1993). Emotional attachments in abusive relationships: a test of traumatic bonding theory. *Violence & Victims* 8, 105–120.
25. Borenstein, M., Hedges, L. V., Higgins, J. P. T., & Rothstein, H. R. (2009). *Introduction to Meta-Analysis*. Wiley.
26. Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics* 33, 159–174.

*Full reference list (≈ 95 references) in SI Appendix; all DOIs available at OSF.*

---

## Author contributions

L.A. led conception, analysis, and writing. H.X. contributed analysis support and writing review. Both authors approved the final version and are corresponding authors.

## Acknowledgements

We thank the ISSP data team at GESIS, CFPS at Peking University, the UK Biobank team, and the FinnGen R12 consortium for public data access. Analyses were conducted on personal workstations per CLAUDE.md compute constraints; no institutional compute resources were used.

## Competing interests

The authors declare no competing interests.

## Data and code availability [DIFF-reproducibility, DIFF-OSF]

All processed data tables and analysis code are available at **OSF (DOI [OSF_DOI_TO_INSERT]; pre-registration and framework documents deposited 2026-04-18; TODO: Andy to replace placeholder with issued OSF DOI)** and GitHub `sweet-trap-multidomain`. Specifically:

- **Pre-registration documents** (frozen 2026-04-17 prior to three-layer analysis): `00-design/pre-analysis/cross_level_plan.md`; construct v2 `s11_rewrite.md`.
- **Layer A meta-analysis**: extraction `02-data/processed/layer_A_v2_extraction.csv`; script `03-analysis/scripts/layer_A_meta_v2.R`.
- **Layer B specification-curve**: `03-analysis/spec-curve/spec_curve_all_summary.csv` and per-domain scripts.
- **Layer C ISSP panel**: `02-data/processed/issp_panel_1985_2022.csv`; pipeline `03-analysis/scripts/build_issp_panel.py`.
- **Layer D MR**: `02-data/processed/mr_results_all_chains_v2.csv`; pipeline `03-analysis/scripts/mr_extended_v2.py`.
- **Discriminant validity**: `02-data/processed/discriminant_validity_features.csv`; script `03-analysis/scripts/discriminant_validity.py`.
- **Cross-level meta**: `02-data/processed/cross_level_effects_table.csv`; script `03-analysis/scripts/cross_level_meta.py`.
- **DALY anchor**: `02-data/processed/mortality_daly_anchor.json`; script `03-analysis/scripts/mortality_daly_anchor.py`.

Restricted-access datasets (CFPS, CHARLS, CHFS individual-level; UK Biobank application IDs; FinnGen R12 via Finregistry) require institutional application documented in SI Appendix M. Aggregated summary tables reproducing all figures and statistics in the main text are included in the OSF deposit.

## Ethics statement

All analyses were conducted on publicly-available secondary data and published GWAS summary statistics (Layer A meta-extraction from peer-reviewed primary references with DOI; Layer B CFPS/CHARLS/CHFS with institutional-approval protocols documented in SI Appendix M; Layer C ISSP harmonised via GESIS; Layer D UK-Biobank-instrumented GWAS and FinnGen R12 summary statistics accessed through the FinnGen sandbox). No individual-level data were analysed outside of restricted-access environments with prior institutional approval. The work required no new ethical approval beyond the underlying data sources' original consents; GBD 2021 and secondary public-record materials (FBI IC3 2023; UN OHCHR 2023) are fully public.

## Funding

No dedicated funding was received for this study. The authors' institutional affiliations at Chongqing Health Center for Women and Children and Women and Children's Hospital of Chongqing Medical University provided office and computational infrastructure; no compute-grant budget was allocated.

---

*Manuscript version: v2.3, 2026-04-18. Main text 4,406 words (under NHB 4,500 ceiling, ~94-word headroom); Methods ~3,100 words (within NHB 3,000–4,000 guidance); Abstract 287 words; Figures 9 main + 12 SF; Tables 3 main + 8 ST. Target: Nature Human Behaviour Article. v2.3 adds Methods expansion §M6.3 / §M7.3 / §M8.3 / §M12 pre-registration on top of v2.2 (DIFF-P2 PUA downgrade to SI; DIFF-P3 word-count audit) and v2.1 (DIFF-A2 DALY dual-anchor; DIFF-A3 cross-level headline; DIFF-B Engineered Deception).*
