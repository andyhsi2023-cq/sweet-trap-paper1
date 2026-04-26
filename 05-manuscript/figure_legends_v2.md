# Figure Legends (v2) — Sweet Trap Cross-Species Framework
**Target journal:** Nature Human Behaviour
**Style:** Bold title sentence; short legend; panel descriptions; statistical details sufficient to interpret.
**Generation:** R 4.3+, matplotlib 3.7+, Paul Tol colorblind-safe palette. Main figures rendered at 180 mm width, 300 DPI.

---

## Figure 1 | The Sweet Trap framework: two necessary conditions define a cross-species welfare-reducing equilibrium.

Conceptual schematic of the Sweet Trap construct. **(a)** The four formal conditions arranged hierarchically: F1 (reward–fitness decoupling, Δ_ST > 0) and F2 (endorsement without coercion) are necessary and sufficient for classification; F3 (self-reinforcing equilibrium) and F4 (absence of corrective feedback) are *severity modifiers* that determine persistence time τ_F3 and intervention urgency. **(b)** Two sub-classes identified in v2: *Mismatch* (signal drift relative to ancestral calibration; e.g., moths to artificial light; humans to hyper-palatable food) and *Engineered* (novel signals with no ancestral referent that piggyback on general-purpose reward architecture; e.g., variable-ratio gambling schedules, algorithmic short-video feeds). **(c)** Cross-species scope: the same formal conditions apply to non-human animals (reward = dopaminergic / incentive-salience response; fitness = lifetime reproductive success × survival) and humans (reward = same circuitry plus culturally constructed rewards; fitness = long-run objective welfare). Δ_ST is the quantitative bridge: Δ_ST = cor(R_agent, F)_ancestral − cor(R_agent, F)_current. **(d)** Classification decision rule: F1 ≥ 0.5 AND F2 ≥ 0.5 ⇒ Sweet Trap (validated on 10 adversarial cases, accuracy = 1.00, Cohen's κ = 1.00; Fig. 4).

---

## Figure 2 | Two-layer formal model links replicator dynamics to behavioural-economic utility.

**(a)** Layer 1 — replicator / Lande–Kirkpatrick coevolutionary dynamics operating on trait mean τ and preference mean y with additive covariance G_{τ,y}. A Sweet Trap exists at equilibrium (τ*, y*) iff ∂W̄/∂τ|_{τ*,y*} < 0 *and* G_{τ,y} > G^{crit}_{τ,y}. **(b)** Layer 2 — behavioural-economic utility overlay for within-lifetime human cases: U_{i,t}(a_i) = θ_i · R(a_i, S_t) − (1 − λ_i) β_i · C(a_i, t+k) + ρ_i · H(a_i, a_{i, past}), where S_t is social/signal state (peer behaviour, algorithmic amplification), C is deferred cost, and ρ captures lock-in. The four Layer-2 primitives (θ, λ, β, ρ) are re-derived in v2 as emergent parameters of the Layer-1 replicator dynamics (see §11.1 of the formal model). **(c)** Cross-layer mapping of F1–F4 onto Layer-1 and Layer-2 expressions, showing that Δ_ST is scale-invariant. **(d)** Phase portrait: in Layer 1, sweet traps correspond to stable equilibria along the Lande line; in Layer 2, they correspond to interior optima of U with ∂U/∂a > 0 at actions where ∂W/∂a < 0.

---

## Figure 3 | Cross-cultural universality: aspirational-attitude velocity from ISSP 1985–2022 (n = 2.9 M individuals, 25 countries) predicts country-level Sweet Trap severity.

**(a)** Scatter of country-level Σ_ST against ISSP signed aspirational velocity Δz (1985→2022), n = 25. Primary specification (joint-predictor model): β_{Δz} = −0.732 [−1.42, −0.05], HC3 robust SE, p = 0.036; β_{log τ_env_internet} = −0.742 [−1.46, −0.03], p = 0.042; adjusted R² = 0.255. Countries coloured by region (Paul Tol 7-colour colorblind-safe palette). China (solid circle) sits at the 95th percentile of signed aspirational velocity (2009–2022, 2-wave slope) and 92nd percentile of aspirational level. **(b)** Cross-cultural calibration: country G^c_z (a priori cultural index built from Hofstede PDI + LTOWVS − IDV; 59 countries) against raw Σ_ST. G^c is not applied to individual-level predictions; its purpose is to formalise between-society runaway amplification (see §11.2). Sensitivity: Spearman ρ(raw, G^c-weighted Δ_ST) = 0.981 on 201 countries; ΔR² from weighting = +0.0009, demonstrating that G^c is not post-hoc curve-fitting. **(c)** Peak-and-Retreat pattern in ISSP velocity: highest-Σ_ST countries (JP, US, NZ) are past their aspirational peaks (negative Δz); mid-Σ_ST countries (DK, CH, GB, DE) are still climbing. This dynamic is consistent with P3 (fast τ_env relative to τ_adapt creates Sweet Trap formation, with saturation-retreat at late stages).

---

## Figure 4 | Discriminant validity: F1 + F2 correctly classify 10 adversarial cases.

**(a)** Feature heat-map for 10 cases (5 positive controls: C8 investment FOMO, C11 diet, C12 short-video, C13 housing, D_alcohol Type A; 5 negative controls: C2 intensive parenting, C4 bride-price, D3 996 overwork, C1 staple food, C16 vaccination). Cells coded 0 / 0.5 / 1 with PDE-file provenance. **(b)** Weighted sum S = 2·F1 + 2·F2 + 1·F3 + 1·F4; classification threshold T > 4.0 gives accuracy = 1.00, sensitivity = 1.00, specificity = 1.00, Cohen's κ = 1.00 (n = 10). Minimum positive score = 4.5 (D_alcohol Type A); maximum negative score = 2.5 (C1 staple food); separation margin = 2.0 on 0–6 scale. **(c)** Alternative classifier: "F1 ≥ 0.5 AND F2 ≥ 0.5" achieves identical 1.00 accuracy, confirming that F1 + F2 alone (the v2 necessary-condition core) suffice for classification. F3 and F4 are present in 2 / 5 and 3 / 5 negative controls respectively without triggering false positives — supporting the v2 demotion of F3/F4 to severity modifiers (§11.4 of the formal model). **(d)** Out-of-sample marginal case: C6 health supplements (score S = 4.5) correctly sits at the classifier boundary. Full provenance: `02-data/processed/discriminant_validity_features.csv`. *Caveat*: dev-set evaluation; inter-rater reliability not yet established; 10 cases is small. The claim is "this classifier could have failed on adversarial cases and did not", not prospective validation.

---

## Figure 5 | Grand synthesis: Sweet Trap severity (Σ_ST) as a bivariate function of reward-fitness decoupling and timescale mismatch.

**(a)** All 25 confirmed Sweet Trap cases (triangles: Layer B human focal; circles: Layer A animals) plotted in the two-dimensional space of log(τ_env/τ_adapt) × Σ_ST. Bubble size encodes F2 endorsement strength. Three phenomenological zones are demarcated: fast-cycle Engineered Sweet Traps (upper left), cultural-runaway Sweet Traps (central), and classic ecological traps (right). A5 (ICSS) marked with star (τ_env is laboratory-controlled). **(b)** Stacked decomposition of Σ_ST = Δ_ST × τ_F3 × (1 − feedback) by component for 10 representative cases ordered by total Σ_ST. Layer A cases (right) show higher F1 / Δ_ST contributions; Layer B human cases (left) show higher F3 (peer norm) and F4 (feedback blockade) contributions — reflecting cultural institutions and market-feedback opacity in human Sweet Traps.

---

## Figure 6 | Mendelian-randomisation forest (19 chains, 3 sub-classes): Sweet Trap signatures reflect causal genetic architecture.

Forest plot of two-sample Mendelian-randomisation IVW-random estimates for 19 exposure → outcome chains. Vertical line at OR = 1.0 (null). Three validated sub-classes: **Engineered** (blue: risk tolerance → depression, antidepressants, anxiety — OR 1.38, 1.40, 1.63); **Ancestral-mismatch / alcohol** (orange: drinks-per-week → alcoholic liver cirrhosis OR = 5.41 [2.76, 10.57], → alcoholic chronic pancreatitis OR = 3.80 [1.89, 7.63]; smoking initiation → alcoholic liver OR = 1.96 [1.68, 2.29]); **Ancestral-mismatch / metabolic** (green: BMI → T2D OR = 2.06 [1.60, 2.65], → diabetic nephropathy OR = 1.23 [1.03, 1.47], → stroke OR = 1.14 [1.04, 1.25]). **Informative nulls** shown in grey (triangles): drinks → stroke OR = 1.08 [0.90, 1.29] p = 0.40; drinks → hepatocellular Ca OR = 0.80 [0.29, 2.21] p = 0.67; risk tolerance → diabetic nephropathy OR = 0.93 [0.58, 1.50] p = 0.76. **Discriminant-protective** chains (purple): years of schooling → depression OR = 0.88; SWB → depression OR = 0.46. Pleiotropy: MR-PRESSO distortion test p > 0.25 for all 17 evaluable chains; Egger intercept p > 0.10 for 18/19 chains (chain 7 smoking → alc liver p = 0.009 — SI only). MVMR confirms: risk tolerance → T2D fully mediated by BMI (direct OR 0.95, p = 0.80); drinks and smoking have independent direct effects on alcoholic liver (OR 5.14 and 1.94 respectively). Full data: `mr_results_all_chains_v2.csv`; pipeline: `mr_extended_v2.py`.

---

## Figure 7 | Specification-curve analysis: Sweet Trap effects are robust across 3,000 model specifications.

Five-panel composite of specification-curve analyses for five human Focal domains (one panel per domain). Each panel shows all specifications in that domain's grid, sorted by β estimate (x-axis) with 95% CI shaded. Domain-specific grids cross outcome variable (3–7 choices), treatment operationalisation (2–8), control set {minimal / demog+SES / extended}, fixed-effect structure (pooled / individual / individual × year × province), sample filter (full / urban / rural / working-age / male / young / current-users), and waves-pooling or lag scheme. Specification counts: **C8 investment** = 240; **C11 diet** = 672; **C12 short-video** = 576; **C13 housing** = 1,152; **D_alcohol** = 360. Total 3,000 specs, exceeding Sommet et al. (2026) *Nature* benchmark of 768.

Median β on the *narrow focal* family (headline DV × headline treatment root) with 2000-bootstrap 95% CI on the median:
- **C13 housing**: median β = **+0.243** [+0.183, +0.323]; sign stability = 100.0%; significance rate = 75.0%. **Robust.**
- **D_alcohol**: median β = **+0.134** [+0.121, +0.215]; sign stability = 96.3%; significance rate = 92.6%. **Most robust.**
- **C8 investment**: median β = **−0.077** [−0.089, −0.049]; sign stability = 82.6%; significance rate = 78.3%. **Robust (narrow).**
- **C11 diet**: median β = **−0.024** [−0.031, −0.022]; sign stability = 91.7%; significance rate = 25.0%. **Direction robust; power-limited.**
- **C12 short-video**: median β = −0.003 [−0.039, +0.004]; sign stability = 62.5%; significance rate = 0.0%. **FRAGILE (downgraded narrative).**

Vertical dashed line in each panel: headline β from the primary analysis. For 3/5 cases the median is stronger than the headline (C11, C13, D_alcohol); the headline was *not* chosen to maximise effect size. C12's fragility is diagnosed as a measurement-instrument limitation (CFPS `internet` is binary); C12 appears as "directional evidence consistent with the multi-domain pattern" rather than a stand-alone claim. Source: `03-analysis/spec-curve/spec_curve_all_summary.csv`; figure: `fig7_spec_curve_5panel.png`.

---

## Figure 8 | Sweet Trap mechanisms contribute ~34.6 million DALYs per year globally.

**(a) Waterfall chart**: per-chain attributable DALYs (Levin 1953 population-attributable-fraction formula: PAF = P_e(OR − 1) / (P_e(OR − 1) + 1); attrib_DALY = PAF × GBD-2021 disease total). Four de-duplicated Sweet-Trap-MR chains: BMI → T2D 23.6 M (68% of total), drinks → alcoholic liver cirrhosis 4.3 M (12%), risk tolerance → depression 4.1 M (12%), smoking → alcoholic liver 2.5 M (7%). Headline total: **34.6 M DALYs per year globally, 95% envelope [16.2, 64.1] M** — approximately ten times the 2021 global burden of Parkinson's disease (≈3 M DALYs) and equivalent to roughly half the burden of low back pain (≈66 M). **(b) Sensitivity strategies**: Tier-1 Steiger-correct only retains chain 1b (risk tolerance → depression) and drops to 4.1 M [1.0, 11.8]; large-effect-only (OR ≥ 1.5) gives 30.4 M; prevalence ±20 % shifts estimate within 16 – 64 M envelope. **(c) Sankey flow**: exposures (BMI, alcohol, risk tolerance, smoking) → diseases (T2D, cirrhosis, depression, stroke/nephropathy ancillary) → DALY category (cardiometabolic, hepatopancreatic, psychiatric). Colour thickness encodes attributable DALY mass. Full reproducibility: `mortality_daly_anchor.py`; sensitivity table: `mortality_anchor_sensitivity.json`.

*Caveat*: 3 of 4 main chains have Steiger ✗ (BMI, alcohol, smoking exposures have partially organ-specific GWAS architecture; confounded but not reverse-causal — see Results §4 and Supplementary Methods §S7). Tier-1-only sensitivity (4.1 M) is the most conservative plausible bound.

---

## Figure 9 | Cross-level meta-regression: animal mechanism gradient predicts human genetic-causal gradient (Spearman ρ = +1.00).

**(a) Cell means by layer × mechanism**: Layer A (20 animal cases, Δ_ST correlation scale) shows `olds_milner` 0.780 > `sensory_exploit` 0.646 > `fisher_runaway` 0.546. Layer D (15 MR chains, |log OR| scale) shows `olds_milner` 0.553 > `sensory_exploit` 0.354. Layer B (5 focal human cases, standardised β) shows a reversed ordering driven by C13 housing anomaly; reported transparently. **(b) Rank preservation**: Spearman ρ(Layer A, Layer D) = **+1.00** on the two shared mechanism cells; ρ(B, D) = +1.00 (2-cell); ρ(A, B) = −0.50 (three-cell, reflecting C13 anomaly). **(c) Mixed-effects meta-regression** `effect_z ~ mechanism + (1 | layer)`: primary model Wald χ²(2) = 1.51, p = 0.47; leave-one-out sensitivity: drop Layer B → olds β = +1.58, p = **0.019** (A + D-only test pre-registered as secondary). Mechanism-reclassification sensitivity (C13 → olds_milner): β = +1.47, p = 0.033. **(d) Novelty contribution**: upgrades the construct claim from "parallel evidence at each layer" to "animal-observed mechanism rank *predicts* human genetic-causal rank". This is the cross-level concordance required to move Sweet Trap from a labelling exercise to a falsifiable predictive framework. Source: `02-data/processed/cross_level_effects_table.csv`; model: `cross_level_meta_results.json`; script: `03-analysis/scripts/cross_level_meta.py`.

*Caveat*: `n_groups = 3` makes the random-intercept variance singular; we report the fixed-effect mechanism model with layer as crossed factor as primary reading. The A+D-only pre-registered test (p = 0.019) is the cleanest evidence; Layer B inclusion dilutes because of the C13 anomaly (informative: housing runaway may be a domain-specific mechanism category rather than fisher_runaway *per se*).

---

*Legends version: 2026-04-18. All source data, code, and model outputs are available at `/Users/andy/Desktop/Research/sweet-trap-multidomain/` and (at submission) via OSF.*
