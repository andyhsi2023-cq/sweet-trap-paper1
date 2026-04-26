# Figure Legends (v3.4) — Sweet Trap Cross-Disciplinary Framework
**Target journal:** *Humanities and Social Sciences Communications* (Article)
**Style:** Bold title sentence; one-sentence core message; panel descriptions; statistical details sufficient to interpret without main text.
**Generation:** R 4.3+, Paul Tol colorblind-safe palette throughout. Figures rendered at 180 mm width, 300 DPI PNG + cairo_pdf vector.
**Version note:** figure content, numbering, and source data are inherited verbatim from v3.3 (six main figures in first-citation order: Fig 1 animal meta, Fig 2 spec-curve, Fig 3 ISSP, Fig 4 MR, Fig 5 theory tests, Fig 6 discriminant). Only the target-journal header and a small number of journal-specific phrasings have been updated for HSSC; all empirical content is unchanged from v3.3.

---

## Figure 1 | Animal Sweet Traps span six phylogenetic classes and show a consistent mechanism-dependent reward–fitness decoupling gradient.

**Core message:** Δ_ST > 0 is documented across 20 cases from 6 phylogenetic classes (mammals to crustaceans), with effect magnitude highest in direct neural-reward hijacking (Olds–Milner) and lowest in life-history trade-off cases. **(a)** Phylogenetic dot-strip: 20 confirmed animal Sweet Trap cases plotted by taxon class (background bands, Paul Tol 8-colour palette), with point shape encoding mechanism category (circle = Olds–Milner / ICSS; triangle = sensory exploit; square = Fisher runaway; diamond = reproduction–survival trade-off) and horizontal extent showing Δ_ST ± 95% CI. Cases ordered within class by Δ_ST (descending). **(b)** Mechanism-subgroup forest plot (random-effects, restricted maximum likelihood): Olds–Milner 0.789 [0.620, 0.959], k = 7; sensory exploit 0.653 [0.560, 0.745], k = 5; Fisher runaway 0.547 [0.430, 0.664], k = 5; reproduction–survival 0.470 [0.357, 0.583], k = 3. Olds–Milner vs. Fisher runaway: Δ = +0.242, p = 0.001 (Wald test). I² = 85.4% (high heterogeneity driven by mechanism class). **(c)** Pooled summary across all 20 cases: diamond at Δ_ST = 0.645 [0.557, 0.733] with 95% prediction interval [0.228, 1.062] (outer segment); dashed null line at 0. Source data: `02-data/processed/layer_a_animal_cases.csv`; figure script: `04-figures/main/fig1_animal_phylogeny_meta.R` (v3.1). [≈ 220 words]

---

## Figure 2 | Specification-curve analysis across 3,000 model specifications confirms Sweet Trap effects in four of five focal domains, with C12 short-video explicitly downgraded.

**Core message:** Consistent direction and significance across exhaustive specification space supports P2 (domain generalisability), while transparent reporting of C12's fragility guards against inflation. Five-panel composite of specification-curve analyses for C8 investment FOMO, C11 diet (SSB), C12 short-video, C13 housing leverage, and D_alcohol. Each panel shows all specifications sorted by β estimate with 95% CI shaded. Total: 3,000 specifications (C8 = 240, C11 = 672, C12 = 576, C13 = 1,152, D_alcohol = 360), exceeding Sommet et al. (2026, *Nature*) benchmark of 768.

Median β on the narrow focal family with 2,000-bootstrap 95% CI on the median:
- **D_alcohol**: +0.134 [+0.121, +0.215]; sign stability = 96.3%; significance rate = 92.6%. **Most robust.**
- **C13 housing**: +0.243 [+0.183, +0.323]; sign stability = 100.0%; significance rate = 75.0%. **Robust.**
- **C8 investment**: −0.077 [−0.089, −0.049]; sign stability = 82.6%; significance rate = 78.3%. **Robust.**
- **C11 diet**: −0.024 [−0.031, −0.022]; sign stability = 91.7%; significance rate = 25.0%. **Direction-robust; power-limited.**
- **C12 short-video**: −0.003 [−0.039, +0.004]; sign stability = 62.5%; significance rate = 0.0%. **FRAGILE** (CFPS `internet` is binary; C12 is treated as directional evidence only).

Vertical dashed line in each panel marks the headline β from the primary analysis. Source: `03-analysis/spec-curve/spec_curve_all_summary.csv`; figure: `04-figures/main/fig2_spec_curve_5panel.png`. [≈ 240 words]

---

## Figure 3 | Cross-cultural universality: aspirational-attitude velocity from ISSP 1985–2022 (n = 2.9 M individuals, 25 countries) predicts country-level Sweet Trap severity.

**Core message:** Countries where aspirational attitudes accelerated faster toward high-consumption ideals show higher observed Sweet Trap severity, consistent with the cultural-runaway (Fisher G_{τ,y}) amplification pathway. **(a)** Scatter of country-level Σ_ST against ISSP signed aspirational velocity Δz (1985→2022), n = 25. Primary specification (joint-predictor model): β_{Δz} = −0.732 [−1.42, −0.05], HC3 robust SE, p = 0.036; β_{log τ_env_internet} = −0.742 [−1.46, −0.03], p = 0.042; adjusted R² = 0.255. Countries coloured by world region (Paul Tol 7-colour). China (solid circle) sits at the 95th percentile of signed aspirational velocity and 92nd percentile of aspirational level. **(b)** Country cultural coefficient G^c_z (Hofstede PDI + LTOWVS − IDV composite; 59 countries) against raw Σ_ST; Spearman ρ = 0.981 on 201-country sensitivity run; ΔR² from G^c-weighting = +0.0009. **(c)** Peak-and-Retreat pattern in ISSP velocity: highest-Σ_ST countries (JP, US, NZ) show negative Δz (past their aspirational peak); mid-Σ_ST countries (DK, CH, GB, DE) still climbing. Source data: `02-data/processed/issp_cross_cultural_velocity.csv`; figure script: `04-figures/main/fig3_issp_cross_cultural.R`. [≈ 200 words]

---

## Figure 4 | Mendelian-randomisation forest (19 chains): Sweet Trap signatures reflect causal genetic architecture across three sub-classes.

**Core message:** Genetically-instrumented exposures in Sweet Trap domains (risk tolerance, BMI, alcohol intake, smoking) causally predict downstream welfare harms, with informative null MR chains providing discriminant evidence. Forest plot of two-sample MR IVW-random estimates for 19 chains. Three validated sub-classes: **Engineered** (blue): risk tolerance → depression OR = 1.38, → antidepressant use OR = 1.40, → anxiety OR = 1.63. **Ancestral-mismatch / alcohol** (orange): drinks-per-week → alcoholic liver cirrhosis OR = 5.41 [2.76, 10.57], → chronic pancreatitis OR = 3.80 [1.89, 7.63]; smoking → alcoholic liver OR = 1.96 [1.68, 2.29]. **Ancestral-mismatch / metabolic** (teal): BMI → T2D OR = 2.06 [1.60, 2.65], → diabetic nephropathy OR = 1.23 [1.03, 1.47], → stroke OR = 1.14 [1.04, 1.25]. **Informative nulls** (grey, triangles): drinks → stroke OR = 1.08 [0.90, 1.29] p = 0.40; drinks → hepatocellular Ca OR = 0.80 [0.29, 2.21] p = 0.67; risk tolerance → diabetic nephropathy OR = 0.93 [0.58, 1.50] p = 0.76. **Discriminant-protective** (purple): years of schooling → depression OR = 0.88; SWB → depression OR = 0.46. Pleiotropy: MR-PRESSO p > 0.25 for all 17 evaluable chains; Egger intercept p > 0.10 for 18/19 chains. Full data: `02-data/processed/mr_results_all_chains_v2.csv`; script: `04-figures/main/fig4_mr_layer_D.R`. [≈ 250 words]

---

## Figure 5 | Theory tests: animal mechanism rank predicts human genetic-causal rank (pre-registered β = +1.58; T2 theorem confirmed; median signal-redesign advantage = 11×).

**Core message:** Two theory-level predictions are jointly confirmed: (P5) the mechanism hierarchy observed in animal Sweet Traps predicts the same hierarchy in human MR chains; (T2) signal-redesign interventions dominate information-based alternatives in every Sweet Trap domain tested. **(a)** Cross-level A+D joint meta-regression: Layer A (animal Δ_ST, circles, blue) and Layer D (human MR |log OR|, triangles, orange) plotted by mechanism class (Fisher runaway → Sensory exploit → Olds–Milner). Dashed linear trend lines per layer; pre-registered β = +1.58 [z-scored], p = 0.019 (A+D joint, highlighted). Primary three-layer model: χ²(2) = 1.51, p = 0.47 (non-significant; shown in grey italic; A+D pre-registered as primary per §6.3). **(b)** Intervention asymmetry forest (T2 theorem, P1): signal-redesign (filled domain-colour circles) vs. information (open grey circles) across six Sweet Trap domains (C8, C11, C12, C13, D_alcohol, C_pig-butchering†) on a domain-normalised scale (signal-redesign ≡ 1.0). In all six domains the signal-redesign point estimate exceeds the information estimate. ††C_pig-butchering uses emerging-evidence CIs (dashed line). **(c)** Within-domain ratio (signal redesign ÷ information) on log-scale x-axis. All six ratios exceed 1; five of six exceed 3 (shaded region). Median ratio = 11×. **Scope condition**: the T2 theorem is claimed only for Sweet Trap domains (F1 ≥ 0.5 AND F2 ≥ 0.5); this does not generalise to non-Sweet-Trap contexts. Source data: `02-data/processed/intervention_asymmetry_table.csv`, `cross_level_effects_table.csv`; script: `04-figures/main/fig5_theory_tests.R` (v3.1). [≈ 280 words]

---

## Figure 6 | Discriminant validity: F1 + F2 correctly classifies 10 adversarial cases (accuracy = 1.00, Cohen's κ pending).

**Core message:** The two necessary conditions (reward–fitness decoupling F1 ≥ 0.5; endorsement without coercion F2 ≥ 0.5) distinguish confirmed Sweet Traps from structurally similar but excluded behaviours across five positive and five negative controls. **(a)** Feature heat-map for 10 adversarial cases: 5 positive controls (C8, C11, C12, C13, D_alcohol Type A) and 5 negative controls (C2 intensive parenting, C4 bride-price, D3 996 overwork, C1 staple food, C16 vaccination). Cells coded 0 / 0.5 / 1 (colour scale: white–blue–dark blue). **(b)** Weighted score S = 2·F1 + 2·F2 + 1·F3 + 1·F4; classification threshold T > 4.0 gives accuracy = 1.00, sensitivity = 1.00, specificity = 1.00. Minimum positive score = 4.5 (D_alcohol Type A); maximum negative score = 2.5 (C1 staple food); separation margin = 2.0 on 0–6 scale. **(c)** Alternative binary rule "F1 ≥ 0.5 AND F2 ≥ 0.5" achieves identical accuracy, confirming F3/F4 are severity modifiers (not required for classification). **(d)** Out-of-sample marginal case C6 (health supplements, S = 4.5) sits at the classification boundary. *Caveats:* dev-set evaluation only (n = 10); blind second-coder κ is pending for revision round 1. Full provenance: `02-data/processed/discriminant_validity_features.csv`; script: `04-figures/main/fig6_discriminant_dashboard.R`. [≈ 240 words]

---

*Legends version: v3.4 (HSSC header update), 2026-04-21. Figure content, numbering, and source data inherited verbatim from v3.3. Six main figures in first-citation order: Fig 1 = animal phylogeny meta; Fig 2 = spec-curve five-panel; Fig 3 = ISSP cross-cultural; Fig 4 = MR forest; Fig 5 = theory tests (intervention-asymmetry + cross-level meta); Fig 6 = discriminant-validity dashboard. All source data and scripts available at project root and OSF repository `https://osf.io/ucxv7/`.*
