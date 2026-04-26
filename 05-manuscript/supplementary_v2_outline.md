# Supplementary Information Outline (v2)
**Target journal:** Nature Human Behaviour
**Manuscript:** Sweet Trap — a cross-species reward–fitness decoupling framework
**Version:** 2026-04-18

---

## SI Appendix A — Formal model v2 and v1 → v2 changelog
- A.1 Full formal construct (F1–F4, Δ_ST, Σ_ST, Layer 1 + Layer 2 equations)
- A.2 v1 → v2 limitation → refinement mapping (see `05-manuscript/s11_rewrite.md`; incorporates HARKing-transparency table)
- A.3 Transparency statement and OSF pre-registration metadata (at submission)
- **Source file:** `00-design/sweet_trap_formal_model_v2.md` + `05-manuscript/s11_rewrite.md`

## SI Appendix B — Layer A: animal meta-analysis (20 cases)
- B.1 PRISMA-informed search protocol (6 query strings, Web of Science + PubMed + Scopus + local corpus-index of 35,858 papers)
- B.2 20-case extraction table with per-case F1 route, mechanism, Δ_ST, 95% CI, tier (1/2/3), quality score, primary reference DOI
- B.3 Random-effects DerSimonian-Laird meta-analysis: pooled Δ_ST = +0.645 [+0.557, +0.733], I² = 85.4%, τ² = 0.0329, 95% PI [+0.278, +1.011]
- B.4 Moderator analyses: F1 route (β_B = +0.155, p = .028, R² = 61%); mechanism category (Q_M = 13.22, p = .004, R² = 76%); quality (β = +0.112, p < .001, R² = 75%); baseline tier; vertebrate vs invertebrate (p = .695)
- B.5 Publication-bias discussion (Egger t = −12.55; caveats about bounded Δ_ST)
- B.6 Forest plot for all 20 cases (supplementary figure)
- **Source file:** `00-design/pde/layer_A_animal_meta_v2.md` + `03-analysis/scripts/layer_A_meta_v2.R`

## SI Appendix C — Layer B: human focal domains (5 cases) and Chinese panel data pipeline
- C.1 CFPS 2010–2020 panel construction; within-person fixed effects; winsorisation protocol
- C.2 CHARLS + CHFS cross-validation
- C.3 Per-case PDE report:
  - C.3.1 C8 investment FOMO (spec-curve 240, narrow median β = −0.077)
  - C.3.2 C11 diet (spec-curve 672, narrow median β = −0.024)
  - C.3.3 C12 short-video (spec-curve 576, narrow median β = −0.003 — **FRAGILE**)
  - C.3.4 C13 housing (spec-curve 1,152, narrow median β = +0.243)
  - C.3.5 D_alcohol (spec-curve 360, narrow median β = +0.134)
- C.4 US replication for C8 and C13 using HRS + PSID (directional concordance)
- C.5 C12 fragility discussion and proposed future work with continuous digital-intensity measures
- **Source files:** `00-design/pde/C{8,11,12,13}_*_findings.md`, `D_alcohol_findings.md`, `C8_C13_us_replication_findings.md`

## SI Appendix D — Discriminant validity v2: F1+F2 necessary-sufficient classification
- D.1 Selection logic for 5 positive and 5 negative controls; rationale for each adversarial choice
- D.2 Feature coding convention (0 / 0.5 / 1) with PDE-file provenance for every cell
- D.3 Full confusion matrix (accuracy = 1.00, Cohen's κ = 1.00)
- D.4 Six alternative classifiers (threshold sweep T ∈ [2.5, 5.0]); robustness of 100% accuracy across T ∈ [2.50, 4.25]
- D.5 Out-of-sample marginal case: C6 health supplements (score = 4.5, correctly at boundary)
- D.6 Caveats: dev-set evaluation, single-coder, inter-rater reliability deferred to revision round 1
- D.7 Codebook for future out-of-sample extension
- **Source file:** `00-design/pde/discriminant_validity_v2.md` + `02-data/processed/discriminant_validity_features.csv`

## SI Appendix E — Layer C: ISSP 1985–2022 cross-national analysis
- E.1 Data engineering: 18 waves × 54 countries × 27 harmonized variables; 2.9 M individual records
- E.2 Country-code and Likert-scale harmonisation (ISSP v3 → ISO-2; 64-entry mapping table)
- E.3 Aspirational velocity construction: signed Δz 1985→2022, within-wave z-score, Hofstede 6D covariates
- E.4 Primary specification C1: β_{Δz} = −0.732, p = 0.036; β_{log τ_env_internet} = −0.742, p = 0.042; joint R² = 0.255 (n = 25)
- E.5 10-specification robustness grid
- E.6 Peak-and-Retreat pattern (JP/US/NZ post-peak vs DK/CH/GB/DE pre-peak)
- E.7 CFPS × ISSP cross-domain aggregate matching (mixed: 6/11 directional, low power)
- E.8 China-specific trajectory: aspirational velocity 95th percentile; aspirational level 92nd percentile; Cantril residual 21st percentile
- **Source files:** `00-design/pde/layer_C_cross_cultural_findings.md` + `00-design/pde/layer_C_ISSP_deep_findings.md`

## SI Appendix F — Cultural G^c calibration (a priori index for §11.2)
- F.1 Theoretical derivation: Triandis 1995, Hofstede 2010, Schwartz 2006, Gelfand 2011 — why PDI + LTOWVS − IDV
- F.2 Exclusion of Indulgence vs Restraint (IVR): a priori circularity concern
- F.3 59-country coefficient table (China +1.892, USA −1.818)
- F.4 Rank-stability analyses: Spearman ρ(raw Δ_ST, G^c-weighted Δ_ST) = 0.981 on 201 countries; ΔR² = +0.0009
- F.5 ISSP subsample sensitivity: ρ = 0.94, n = 25
- F.6 Three alternative formulae and their ρ with primary formulation
- F.7 Face-validity interpretation: East Asian + Eastern European cluster at top; Anglo-Nordic cluster at bottom
- **Source file:** `00-design/pde/cultural_Gc_calibration.md`

## SI Appendix G — Layer D: Mendelian randomisation v2 (19 chains, 5 methods, 3 MVMR)
- G.1 Data sources: UK Biobank-instrumented exposure GWAS (n = 258,000–1,331,000); FinnGen R12 outcomes (n ≈ 413,000)
- G.2 Instrument selection: 5×10⁻⁸ significance, LD clumping (r² < 0.001, 10 Mb window), F-statistic (mean F = 32–64)
- G.3 19-chain table: exposure → outcome, n SNP, IVW OR [95% CI], Cochran Q, I², Egger intercept p, Steiger direction
- G.4 Five-method validation: IVW, weighted median, MR-Egger, MR-RAPS, MR-PRESSO (19/19 same-sign for IVW and RAPS; 18/19 directionally concordant for ≥ 4 methods; 17/17 evaluable MR-PRESSO distortion tests p > 0.25)
- G.5 MVMR direct effects:
  - G.5.1 BMI + risk tolerance → T2D (risk tolerance fully mediated by BMI)
  - G.5.2 Drinks + smoking → alcoholic liver (both independent direct effects)
  - G.5.3 BMI + drinks → stroke (BMI robust, drinks null confirmed)
- G.6 Informative nulls: drinks → stroke (p = 0.40), drinks → hepatocellular Ca (p = 0.67), risk tolerance → nephropathy (p = 0.76) — empirical bounds on construct
- G.7 Discriminant-protective chains: years of schooling → depression (OR 0.88), SWB → depression (OR 0.46) — F1 fails (reward = fitness aligned)
- G.8 Leave-one-out and single-SNP Wald analyses: 2,576 per-SNP estimates; no "killer SNP" identified
- G.9 Funnel plots (19-panel grid): no visual asymmetry beyond Egger formal test
- G.10 Steiger directionality limitations (11/19 chains Steiger ✗; interpretation as partial organ-specific GWAS architecture, not reverse causation)
- G.11 Discussion of 88% Steiger vulnerability (flagged in Results §4 and Discussion)
- **Source files:** `00-design/pde/layer_D_MR_findings_v2.md` + `02-data/processed/mr_results_all_chains_v2.csv`, `mr_mvmr_v2.csv`, `mr_loo_all_v2.csv`

## SI Appendix H — Specification-curve analysis (3,000 specs across 5 focal domains)
- H.1 Pre-registered grid dimensions (DV, treatment, controls, fixed effects, sample filter, waves/lag)
- H.2 Harmonised 15-column schema across 5 domains
- H.3 Per-domain curves with narrow focal (headline DV × headline treatment) vs broad focal (all sweet-branch treatment variants)
- H.4 Median β, 2000-bootstrap CI, sign stability, same-sign significance rate
- H.5 Fragility diagnostic (C12: narrow sign-stability 62.5%, significance 0%; root cause = binary `internet` measurement)
- H.6 Per-domain discussion (C8 robust narrow; C11 direction robust but power-limited; C13 100% sign-stable; D_alcohol most robust)
- **Source file:** `00-design/pde/spec_curve_findings.md` + `03-analysis/spec-curve/spec_curve_all_summary.csv`

## SI Appendix I — Cross-level meta-regression (Layer A × B × D)
- I.1 Scale harmonisation: within-layer z-score (primary); Cohen's-d equivalence (secondary)
- I.2 Mechanism mapping (pre-registered): Layer A 20 cases + Layer D 15 core chains + Layer B 5 focal
- I.3 Mixed-effects meta-regression (primary): Wald χ²(2) = 1.51, p = 0.47
- I.4 Leave-one-layer-out sensitivity: drop B → olds β = +1.58, p = 0.019 (pre-registered A+D-only)
- I.5 Spearman rank correlation: ρ(A, D) = +1.00; ρ(A, B) = −0.50 (C13 anomaly); ρ(B, D) = +1.00
- I.6 Mechanism-reclassification sensitivity (C13 → olds_milner)
- I.7 C13 housing anomaly discussion: informative (domain-specific runaway) not fatal (cross-species universality survives without C13)
- **Source file:** `00-design/pde/cross_level_meta_findings.md`

## SI Appendix J — Mortality / DALY anchor (GBD 2021 × MR)
- J.1 GBD 2021 DALY baselines: T2D (75.3 M), alc liver (14.2 M), depression (56.3 M)
- J.2 Exposure prevalence sources: NCD-RisC, WHO 2024, GBD 2021 Tobacco, Falk et al. 2018, WHR 2024
- J.3 Per-chain PAF calculation using Levin 1953 formula; 3×3 uncertainty grid
- J.4 Headline: 34.6 M DALYs/yr [16.2, 64.1]
- J.5 Five-strategy sensitivity: Main 34.6 M; Tier-1 Steiger only 4.1 M; large-effect-only 30.4 M; prevalence ±20% ranges
- J.6 Benchmarks: GBD all-smoking 231 M, all-BMI 160 M, all-alcohol 88 M, all-diet 187 M; low back pain 66 M; Parkinson's 3 M
- J.7 Method transparency: Levin vs GBD TMREL vs Miettinen; dichotomous exposure assumption; outcome-aliasing de-duplication rules
- J.8 Limitations: 3/4 counted chains have Steiger ✗ (not reverse causation; partially organ-specific genetic architecture)
- **Source file:** `00-design/stage3/mortality_anchor.md`

## SI Appendix K — Causal identification: MR as the 1-sentence strategy
- K.1 Why two-sample MR: UK Biobank exposure instruments + FinnGen outcomes = two-population sandwich design
- K.2 1-sentence identification: "Genetic variants randomly assigned at conception serve as instrumental variables for lifetime behavioural exposure."
- K.3 Assumption hierarchy: relevance (F-stat), independence (population stratification), exclusion (Egger / PRESSO / Steiger)
- K.4 Why we do not rely on Steiger alone (biology of BMI, alcohol, smoking loci is inherently partly-direct-molecular)
- K.5 Comparison to alternative identification (RCT: ethics; Diff-in-Diff: endogenous policy; natural experiment: not globally generalisable)

## SI Appendix L — Policy window alignment
- L.1 WHO ultra-processed food policy (2024–2027 review)
- L.2 UK sugar tax decadal evaluation (2024–2025)
- L.3 EU Digital Services Act — algorithmic recommender rules (2024–)
- L.4 China 双减 evaluation cohort (2021-exposed)
- L.5 Each policy windows's mapping to Sweet Trap sub-class (Mismatch vs Engineered)

## SI Appendix M — Reproducibility manifest
- M.1 File listing: 23 checkpoint files in `00-design/`, 19 CSV outputs in `02-data/processed/`, 12 scripts in `03-analysis/scripts/`
- M.2 Random seed: 20260418 across all stochastic steps
- M.3 Compute environment: macOS 26.4, MacBook Pro M5 Pro 24 GB, R 4.3+, Python 3.12 with pandas/numpy/statsmodels/matplotlib
- M.4 Compute rule compliance: n_workers ≤ 2; no multiprocessing fork on M5 Pro; exactextract for raster operations (none used here)
- M.5 Run instructions per script; expected runtime
- M.6 Data availability: public datasets listed with DOIs; restricted datasets (CFPS, CHARLS, CHFS, ISSP restricted waves) require institutional access; OSF repository at submission
- **Source files:** `_meta/compute-ops-guide.md`, `HANDOFF.md`

## SI Appendix N — Red Team rebuttal log
- N.1 Red Team objection 1: "Umbrella construct unfalsifiable (16+ profile combinations)" — rebutted by SI Appendix D (F1+F2 sufficient, accuracy 1.00, κ = 1.00)
- N.2 Red Team objection 2: "Δ_ST baseline circular" — rebutted by tiered baseline (T1 direct / T2 phylogenetic / T3 theoretical prior), Tier-1-only sensitivity retains positive pooled effect
- N.3 Red Team objection 3: "§11 HARKing" — rebutted by `05-manuscript/s11_rewrite.md` and SI Appendix A (transparency date-stamp of v1 freeze 2026-04-16 → v2 refinements 2026-04-17 mapped to specific limitations)
- N.4 Red Team objection 4: "MR method monoculture" — rebutted by 5-method concordance (IVW + WMed + Egger + RAPS + PRESSO) in SI Appendix G
- N.5 Red Team objection 5: "Narrow outcomes (4 FinnGen phenotypes)" — rebutted by 9 FinnGen outcomes in v2
- N.6 Red Team objection 6: "Unaccounted pleiotropy" — rebutted by per-chain PRESSO global + distortion tests; all 17 evaluable chains distortion p > 0.25
- N.7 Red Team objection 7: "Finnish-only outcomes" — mitigated by two-population sandwich (UK-ancestry exposure IVs); future work noted
- N.8 Acknowledged limitations still open: sex-stratified MR (future v3); inter-rater reliability on discriminant feature coding (round-1 revision); prospective out-of-sample discriminant cases (post-publication registered replication)

## SI Appendix O — Pre-registration documentation (at submission)
- O.1 OSF repository URL (time-stamped at submission)
- O.2 Frozen v2 formal model text
- O.3 Spec-curve pre-registration grid
- O.4 Cross-level meta-regression pre-registered mechanism mapping
- O.5 Mortality anchor pre-registered aggregation rules (de-duplication, Levin formula)
- **Acknowledgment:** The v1 construct was not OSF-registered before Layer A v1 began (2026-04-16); we address this in the HARKing-transparency section of the manuscript Methods.

---

## Supplementary Figures (SF1–SF12)
- SF1 — Layer A forest plot (20 cases, mechanism-coloured, ordered by Δ_ST)
- SF2 — Layer A funnel plot + Egger regression
- SF3 — Layer A mechanism-category subgroup forests
- SF4 — Layer B per-domain spec-curve detail (5 figures × 1 panel each)
- SF5 — CFPS panel attrition and within-person balance diagnostics
- SF6 — US replication (HRS, PSID) per-domain forest
- SF7 — ISSP 17-wave × 54-country harmonised trajectory heatmap
- SF8 — Country G^c distribution with regional labels
- SF9 — Layer D 19-chain extended forest (IVW + PRESSO corrected, per-chain)
- SF10 — Layer D 19-panel funnel grid
- SF11 — Layer D leave-one-out per-chain range bars (2,576 rows summarised)
- SF12 — DALY anchor Sankey (Exposure → Disease → DALY)

## Supplementary Tables (ST1–ST8)
- ST1 — Layer A 20-case extraction table (full version of main-text Fig. 1 data)
- ST2 — Layer B 5-domain detail table (sample size, covariates, winsorisation, within-person design)
- ST3 — ISSP 54-country × 17-wave × 27-variable coverage matrix
- ST4 — Layer D 19-chain full statistics (IVW / WMed / Egger / RAPS / PRESSO / Steiger / Q / I² / MVMR direct effects)
- ST5 — Spec-curve 3,000-row full results (one row per specification, all 5 domains)
- ST6 — Cross-level meta-regression per-case effect sizes (44 rows: 19 A + 5 B + 15 D + 5 others-excluded-with-reason)
- ST7 — Mortality anchor per-chain PAF + attributable DALY + sensitivity strategies
- ST8 — Discriminant-validity feature vectors (10 cases × F1–F4 + provenance)

---

*End of SI outline. All component source files live under `/Users/andy/Desktop/Research/sweet-trap-multidomain/00-design/pde/`, `02-data/processed/`, `03-analysis/scripts/`, and `04-figures/`. At submission, a consolidated SI PDF will be generated from this outline plus the main manuscript.*
