# Supplementary Information (v3.0) — Outline and Appendix Index

**Paper:** Sweet Trap: a theory of reward–fitness decoupling with cross-species empirical validation
**Version:** v3.0 NHB Article (theory + empirics merged)
**Status:** 2026-04-18

The v3.0 SI is organised in two blocks: **SI-Math** (Paper-1 theory details, 2,500–4,500 words) and **SI-Empirical** (Paper-2 appendices A–I, carried forward from v2.4 with minor updates). All material is available at OSF DOI [OSF_DOI_TO_INSERT].

---

## Block 1 — SI-Math: Theoretical Supplement (~3,500 words, 4,500-word ceiling)

### SI-Math §1. Full primitive-and-axiom statements

- §1.1 Measurable primitives (choice space *S*, Φ, Ω_fit, *ψ*, *B_i*(*t*)) — verbatim from `paper1-theory/01-math-foundation/axioms_and_formalism.md` §1.
- §1.2 Dual utility functions *U*_perc (logistic sigmoid; MC-2 justification) and *U*_fit (expected-discounted integral; MC-3) — verbatim §2.
- §1.3 Coupling *ρ*(*t*); MC-4 *ρ*_crit = 0.3 default.
- §1.4 Full axioms A1–A4 (formal statement + interpretation + scope + empirical anchor + falsification path for each) — verbatim §3.
- §1.5 A3.0 operational scope criterion (Stage 1-B F2 fix) + T2.1.1 dose-matching convention (Stage 1-B F1 fix).
- §1.6 A4 core + Parameterization P1 (Stage 1-B M1: hyperbolic demoted from axiom to parameterization).

### SI-Math §2. Sweet Trap Index Δ_ST (full treatment)

- §2.1 Definition (individual + population forms); relation to v2 correlation-gradient form.
- §2.2 Properties 4.1–4.4 (sign, realisation, magnitude-persistence, belief invariance).
- §2.3 Lemma L1 (Δ_ST well-defined signed measure).

### SI-Math §3. Behavioural dynamics

- §3.1 Continuous-time SDE (5.1).
- §3.2 Sweet Trap attractor condition (5.2).
- §3.3 Discrete-choice Markov dynamics (5.3).
- §3.4 Belief update (5.4); F4 mechanism for stuck beliefs.

### SI-Math §4. Four theorems T1–T4 (expanded proofs)

- §4.1 **T1 Stability.** Full Jacobian computation; Lyapunov function construction (*V* = ½‖*s* − *s**‖² + *g*(Δ_ST); *V̇* ≤ −*cV*); basin-radius estimate. Stage 1-B M2 precondition (★) statement and interpretation.
- §4.2 **T2 Intervention Asymmetry.** Full algebra from `paper1-theory/02-theorems/proof_sketches_expanded.md` §2. Population-expectation γ bound. Non-saturated-regime scope (*σ*′ ≥ *σ*′_min > 0). Stage 1-B M3 shrinkage-invariance discussion.
- §4.3 **T3 Universality.** Constructive invariance across A1–A4. Moth + human examples. Stage 1-B M4 discussion of magnitude rank preservation being empirical not theorem-derived.
- §4.4 **T4 Engineered Escalation.** Envelope-theorem application (Milgrom–Segal 2002). Observation 4.1 (basin-radius demoted from theorem statement; Stage 1-B M5).

### SI-Math §5. Lemmas L1–L5

- L1 Well-definedness of Δ_ST.
- L2 Hyperbolic discount → preference reversal (Strotz 1955).
- L3 Akrasia / System-2 override fails under A3.3.
- L4 Cultural *W̄*_perc in RST.
- **L4.1 (new, Stage 1-B M6).** Mean-field derivation of *W̄*_fit → *W̄*_perc substitution in cultural Lande–Kirkpatrick dynamics, via Gaussian approximation over agent-heterogeneity distribution *F*(*ψ*). Sketch only; full analytical derivation flagged future work.
- L5 Saturation-curvature bound on *σ*′.

### SI-Math §6. Sub-class formalisms

- §6.1 MST (Mismatch Sweet Trap) — ancestral *ψ*, environmental shift; *D*_KL driver.
- §6.2 RST (Runaway Sweet Trap) — cultural *G*^c; L4.1 mean-field. Fisher-parallel distinction (Stage 1-B M7).
- §6.3 EST (Engineered Sweet Trap) — designer optimisation (7.4); two sub-sub-classes (Algorithmic vs Deception).
- §6.4 Ecological Trap ⊂ MST ⊂ Sweet Trap (specialisation *w* = 0, *λ* = 0).

### SI-Math §7. Positioning matrix (full 7-theory treatment)

- §7.1 Prospect Theory — orthogonal.
- §7.2 Rational Addiction — conceptual complement, boundary-adjacent (Stage 1-B M8).
- §7.3 Evolutionary Mismatch — informal precursor; Mismatch ⊂ MST.
- §7.4 Ecological Trap — habitat-choice special case.
- §7.5 Fisher Runaway — parallel structure (Stage 1-B M7; *W̄*_fit vs *W̄*_perc).
- §7.6 Nudge / Libertarian Paternalism — policy backed by T2.
- §7.7 Dual-System Theory — refinement specifying which System-1 signals decouple and why deliberation fails.
- §7.8 Containment diagram (Fig. SI-M1).

### SI-Math §8. Nomenclature (full symbol table)

Verbatim from `paper1-theory/01-math-foundation/nomenclature.md`. Covers every primitive, parameter, and derived quantity used in the main text and methods.

### SI-Math §9. Appendix to Stage 1-B revisions

- §9.1 Revision log (from `paper1-theory/00-outline/revision_log_stage1B.md`): F1–F3 fatal flaws and M1–M8 majors, each with before/after wording.
- §9.2 Integrity audit log (from `paper1-theory/00-outline/integrity_audit_log.md`): P1–P5 empirical-status audit against Paper 2 v2.4 source files.
- §9.3 Peer-reviewer audit archive (Phase D).

---

## Block 2 — SI-Empirical: Appendices A–I

### Appendix A — Layer A (Animal meta-analysis): full 20 cases

- A.1 PRISMA flow diagram (380 → 312 → 48 → 20).
- A.2 Extraction table: 20 cases × 6 columns (species, mechanism, F1 route, Δ_ST, SE, quality tier).
- A.3 Forest plot (Fig. SI-A1) and funnel plot (Fig. SI-A2).
- A.4 Meta-regression moderator tables (mechanism, F1 route, quality tier, vert/invert).
- A.5 Publication-bias assessment (Egger's regression with bounded-Δ_ST caveats).
- Source: `02-data/processed/layer_A_v2_extraction.csv`; `00-design/pde/layer_A_animal_meta_v2.md`.

### Appendix B — Layer D (Mendelian randomisation): full 19 chains

- B.1 Per-chain table: exposure × outcome × instrument *n* × *F*-statistic × IVW OR [95% CI] × *p* × Steiger direction × method-concordance rating.
- B.2 Forest plots (Fig. SI-B1–B3 by sub-class).
- B.3 Funnel plots, LOO, single-SNP Wald ratios.
- B.4 MVMR results (three models).
- B.5 Steiger rationale (socially-stratified GWAS architecture; Hemani 2017; Davies 2019).
- Source: `02-data/processed/mr_results_all_chains_v2.csv`; `00-design/pde/layer_D_MR_findings_v2.md`.

### Appendix C — Spec-curve supplementary (Layer B)

- C.1 Per-domain full spec-curve plot (C8, C11, C12, C13, D_alcohol).
- C.2 Narrow-focal vs broad-focal comparison.
- C.3 Convergence-failure log.
- C.4 Domain-specific fragility diagnostics (C12 CFPS binary-exposure discussion).
- Source: `03-analysis/spec-curve/spec_curve_all_summary.csv`; `00-design/pde/spec_curve_findings.md`.

### Appendix D — Discriminant validity: 18-case details

- D.1 18-case PDE-provenance table (10 dev + 3 held-out Positives + 2 §11.7 Engineered-Deception + 3 systematic Negatives).
- D.2 Per-case F1–F4 scoring with coder notes.
- D.3 Round 1 vs Round 2 κ computations.
- D.4 Quadratic-weighted κ cell-level disagreement log.
- D.5 PUA boundary case handling (SI §11.7b cross-reference).
- Source: `00-design/pde/discriminant_validity_v2.md`; `00-design/stage3/blind_kappa_round2.md`.

### Appendix E — Cultural G^c (59-country table)

- E.1 59-country G^c index construction (PDI, LTOWVS, IDV z-scores and composite).
- E.2 Sensitivity Spearman ρ(raw, weighted) at α ∈ {0.3, 0.5, 0.7}.
- E.3 ISSP 25-country panel: per-country Δ*z* + log *τ*_env + σ_ST values.
- E.4 ISSP cross-domain replication weakness discussion (6/11 directional matches).
- E.5 Peak-and-retreat structure at country level (Japan/USA/NZ vs Denmark/Switzerland/UK).
- Source: `00-design/pde/cultural_Gc_calibration.md`; `03-analysis/models/cultural_gc_results.json`.

### Appendix F — Intervention-asymmetry sources (P1 test)

- F.1 Per-domain source table: information arm + signal-redesign arm × effect size (native units) × 95% CI × primary source citation.
- F.2 Six focal domains (C8, C11, C12, C13, D_alcohol, C_pig-butchering) + vaccine-hesitancy counter-example.
- F.3 Unit-matched ratio calculation (C8: pp/pp = 74×; C12: d/d = 7.0×).
- F.4 Heterogeneous-unit discussion and Borenstein Cohen-*d*-equivalent conversion protocol (pre-registered post-publication work).
- F.5 C13 + C_pig-butchering wider-CI annotations.
- Source: `02-data/processed/intervention_asymmetry_table.csv`; `05-manuscript/s11_8_policy_predictability.md`; Paper 1 predictions §P1 empirical-status paragraph.

### Appendix G — Minimal experimental paradigm (pre-registered protocol)

- G.1 Design: 3-arm factorial RCT within Sweet Trap scope (information vs signal-redesign vs control; *n* ≈ 400 per arm on Prolific).
- G.2 Dose-matching pre-calibration protocol (T2.1.1).
- G.3 Power analysis against T2's (1 − *w*_max)/*w*_max ≥ 1.5 prediction.
- G.4 Falsification criterion: ratio < 1.0 or CI excluding 1.5 at α = 0.05.
- G.5 Pre-registration form (OSF link at submission).
- Source: `paper1-theory/03-predictions/minimal_experimental_paradigm.md`.

### Appendix H — Orthogonal global-health accounting (retained from v2.4)

- H.1 Levin-PAF methodology (retained verbatim from v2.4 `SI_H_orthogonal_health_implications.md`).
- H.2 Steiger-correct floor (4.1 M DALYs/yr) — primary.
- H.3 Extended envelope (34.6 M DALYs/yr) — secondary.
- H.4 GBD 2021 baselines.
- H.5 Sensitivity analyses.
- H.6 Scope-honesty discussion (why this is orthogonal descriptive-scale, not primary claim): Sweet Trap already classifies the behaviours; treating GBD re-aggregation as primary "Sweet Trap causes X DALYs" attribution would be partially circular.
- Pipeline: `03-analysis/scripts/mortality_daly_anchor.py`.

### Appendix I — PUA boundary case (SI §11.7b)

- I.1 Retained verbatim from v2.4 `SI_11_7b_pua_extended.md`.
- I.2 Round 2 F2 disagreement documentation (Coder A 0.5 vs Coder B 1.0).
- I.3 Construct-boundary ambiguity: late-phase trauma-bonded dependency vs canonical F2 definition.
- I.4 Decision: PUA retained only as SI boundary case; not resolved by post-hoc construct modification.

---

## Figures and Tables Index

### Main-text figures (9)
- Fig. 1 — Sweet Trap feature system (F1–F4 → A1–A4 mapping + Δ_ST wedge schematic).
- Fig. 2 — Layer A forest plot with mechanism moderators (20 cases).
- Fig. 3 — Layer C ISSP 25-country panel (Δ*z* × log *τ*_env × σ_ST).
- Fig. 4 — Discriminant-validity scatter (10 dev cases).
- Fig. 5 — Layer B spec-curve cross-domain (3,000 specifications).
- Fig. 6 — Layer D MR forest (19 chains by sub-class).
- Fig. 7 — Layer B domain-specific spec-curve (C8, C11, C12, C13, D_alcohol).
- Fig. 8 — Intervention-asymmetry matrix (6 domains × 2 intervention types, with CIs).
- Fig. 9 — Cross-level synthesis (A+D pre-reg β = +1.58, p = 0.019; full three-layer; C13 anomaly).

### Main-text tables (2)
- Table 1 — Layer B narrow-focal summary.
- Table 2 — Layer D key MR chains by sub-class.

### Extended Data
- ED Table 1 — Positioning matrix (7 adjacent theories).
- ED Fig. 1 — Containment diagram (Sweet Trap and neighbouring theories).

### SI figures (by appendix)
- SI-M1 — Containment diagram (expanded).
- SI-A1 — Layer A full forest.
- SI-A2 — Funnel plot.
- SI-B1–B3 — MR forests by sub-class.
- SI-H1 — v2.3 DALY dual-anchor waterfall + Sankey (retained for reference).
- Further SI figures per appendix.

---

*End of SI outline v3.0. All referenced source files are in OSF deposit at [OSF_DOI_TO_INSERT] and GitHub `sweet-trap-multidomain`.*
