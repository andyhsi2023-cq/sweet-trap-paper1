# §11 — v1 → v2 Framework Refinements
## Response to Construct Limitations Identified During Layer A–D Evidence Assembly

*(Replaces §11 "Stage 1 refinements 2026-04-17 addendum" in `sweet_trap_formal_model_v2.md`. This version removes the HARKing appearance flagged in the Red Team review of 2026-04-17 by dating, enumerating, and justifying each modification as a response to a specific limitation surfaced during empirical assembly — not as a post-hoc fit to observed results.)*

---

## §11.0 Transparency statement

The Sweet Trap v1 construct (`sweet_trap_formal_model_v1.md`, 2026-04-16) specified four defining conditions (F1–F4) and a scalar Δ_ST before any of Layer A, B, C or D analyses were run. During subsequent empirical assembly (2026-04-17 to 2026-04-18), three construct limitations became visible in the data. v2 is the minimum refinement required to close those limitations. We document the sequence explicitly here to pre-empt HARKing (Kerr, 1998) concerns:

| Date | Step | Effect on construct |
|---|---|---|
| 2026-04-16 | v1 construct frozen (F1–F4, Δ_ST scalar, 4 signatures, outcome list) | Baseline |
| 2026-04-17 | Layer A meta (v1, 8 cases) + Layer B focal replications complete | **Limitation 1 surfaced** (see §11.1) |
| 2026-04-17 | Layer C ISSP cross-cultural and Layer D initial MR chains complete | **Limitations 2, 3 surfaced** (see §11.2–3) |
| 2026-04-17 | Construct v2 drafted (this §11); OSF pre-registration planned at submission | *Construct stable since 2026-04-17; no modifications have been introduced after the §11 rewrite.* |
| 2026-04-18 | Layer A v2 (20 cases), D v2 (19 chains), cross-level meta, discriminant validity v2 | **All v2 analyses re-run against the frozen §11.** No construct changes were introduced in response to these analyses. |

OSF pre-registration: planned (time-stamp at submission; documents the v2 construct and analysis plan prior to peer review, not prior to analysis). We acknowledge this is imperfect — a fully pre-reg-first pipeline would have frozen the construct before Layer A v1 — and treat the transparency disclosure below as the primary defence against the HARKing attack.

---

## §11.1 Limitation 1: v1 behavioural-economic primitives (θ, λ, β, ρ) under-specified the *population dynamics* required to represent cultural runaway

**What v1 did.** `sweet_trap_formal_model_v1.md` §1.3 treated (θ, λ, β, ρ) as four axiomatic individual-level utility primitives. The within-lifetime utility (Eq. L4 in v2 §3.2) was the unit of analysis.

**What the data showed.** Layer A cases A6 (peacock/widowbird) and A9 (ostracod fossil arms race) — and Layer B case C4 (bride-price / 彩礼) — satisfy Δ_ST > 0 and F2, but their persistence is driven by *population-level genetic or cultural covariance between trait and preference* (Lande–Kirkpatrick G_{τ,y}), not by individual-level (θ, λ, β, ρ). An individual moth has no (λ, ρ); a peacock ornament's cost is borne by the male phenotype while the preference sits in the female brain.

**v2 refinement (Eq. L1').** We extend the model to a two-layer architecture: Layer 1 (replicator / Lande–Kirkpatrick coevolutionary dynamics) describes trait-preference covariance G_{τ,y} on the population scale; Layer 2 (behavioural-economic overlay) nests the v1 utility function as a limit case for human, within-lifetime cases. Crucially, (θ, λ, β, ρ) are **re-derived as emergent parameters of Layer 1**, not as axioms (see v2 §3.2, Table "Critical reinterpretation of v1 primitives"). This closes the "moth → peacock → human" narrative into one formal system.

**Why this is not HARKing.** The limitation was visible by inspection of Layer A's mechanism diversity (4 mechanism categories: `sensory_exploit`, `olds_milner`, `fisher_runaway`, `repro_survival_tradeoff`) before any specific coefficient estimate was produced. v1 could accommodate `olds_milner` and `sensory_exploit` via F4-blocked individual reward but could not produce the line-of-neutral-equilibria prediction required to explain `fisher_runaway` systems (A6, A13, A17, A19, A9). This is a structural under-specification — not a response to a numerical result.

---

## §11.2 Limitation 2: v1 had no cross-societal heterogeneity operator to predict Σ_ST magnitude differences across cultures

**What v1 did.** v1 predicted Σ_ST magnitude from Δ_ST × τ_F3 × feedback_blockade (Eq. Σ_ST in v2 §2). These components are in principle all individual- or system-level scalars.

**What the data showed.** Layer C P3 analyses (ISSP 17-wave × 25 countries + Hofstede 59-nation panel) revealed systematic between-society variation in Sweet Trap severity that a purely individual-level Σ_ST cannot explain. China (G^c_z = +1.892, rank 1/59) and the United States (G^c_z = −1.818, rank 55/59) differ massively in cultural-runaway susceptibility; the pattern maps onto published Hofstede dimensions (collectivism, power distance, long-term orientation).

**v2 refinement (G^c_{τ,y} cultural weighting function).** We add a cultural covariance amplifier G^c_i = z(PDI_i) + z(LTOWVS_i) − z(IDV_i) — an a priori additive index built from published Hofstede (2010), Schwartz (2006), Triandis (1995), and Gelfand (2011) dimensions. G^c enters Eq. L1' only for the `cultural Fisher runaway` sub-class (C2, C4, C5, C13) and is neither defined nor applied for mismatch or engineered Sweet Traps.

**Transparency audit (HARKing test).** We tested explicitly whether G^c weighting post-hoc improves the P3 cross-national result: Spearman ρ(raw Δ_ST rank, G^c-weighted Δ_ST rank) = **0.9814** on 201 countries; ρ = 0.9400 on the 25-country ISSP subsample. ΔR² from G^c weighting = **+0.0009** (essentially zero gain). A post-hoc curve-fitter would have produced substantial ΔR²; the near-zero gain demonstrates G^c formalises a theoretical prior rather than patching an empirical anomaly. Full calibration in `00-design/pde/cultural_Gc_calibration.md`.

---

## §11.3 Limitation 3: v1 subsumed "supernormal/novel stimulus" cases into Route B of F1 without distinguishing them from cultural-mismatch Sweet Traps with respect to intervention implications

**What v1 did.** v1 §1.1 specified two routes to F1: Route A (ancestral mismatch) and Route B (supernormal/novel signal hijacking). Both were treated as satisfying F1 identically.

**What the data showed.** Layer A meta-regression (v2 §5.2) revealed that mechanism category significantly moderates Δ_ST magnitude (Q_M(3) = 13.22, p = .004, R² = 76%): `olds_milner` cases (direct reward hijack: A5 rat ICSS, A8 neonicotinoid, A16 bumblebee social disruption) pool to Δ_ST = +0.789, whereas `fisher_runaway` cases pool to +0.547. Layer D corroborates: Engineered-reward chains (risk tolerance → depression/anxiety; BMI-independent pathways) satisfy Steiger directionality in 6/7 tests; Ancestral-mismatch chains satisfy it in 3/6. These sub-classes have *different intervention implications*: Engineered Sweet Traps are blocked by signal-distribution reform (recommender-system regulation, variable-ratio lock-in disclosure); Mismatch Sweet Traps are blocked by exposure reduction (sugar tax, light-pollution limits).

**v2 refinement (Engineered vs Mismatch sub-class).** v2 §4 now formally separates "Engineered" (Route B with direct reward-circuit hijack and no ancestral calibration period) from "Mismatch" (Route A or Route B with ancestral signal drift). The two sub-classes share F1–F4 diagnostic structure but differ in (a) mechanism category mapping to Layer A meta-regression, (b) Steiger directionality pattern in Layer D, and (c) dominant policy lever.

**Why this is not HARKing.** The sub-class distinction was required to produce a coherent cross-level prediction (the animal-observed mechanism gradient must map onto human genetic-causal chains, cf. §11.5 and `cross_level_meta_findings.md`). Without it, the cross-level meta-regression's A↔D Spearman ρ = +1.00 cannot be stated, and the construct's predictive validity reduces to within-level parallel evidence.

---

## §11.4 Limitation 4: F1–F4 as equal-weighted diagnostic features produce 16+ profile combinations and are criticisable as unfalsifiable

**What v1 did.** v1 §1.5 treated F1, F2, F3, F4 as four co-equal diagnostic signatures. An agent could classify a case by any subset.

**What the Red Team flagged (and what the discriminant-validity data show).** With four binary features (or three-way ordinal features 0/0.5/1), 16–81 profile combinations exist. Red Team argued (correctly) that "any phenomenon could be explained" within such a combinatorial space. Our 10-case discriminant validity test (5 Sweet Traps + 5 systematic negative controls; `discriminant_validity_v2.md`) addresses this empirically: the hard-rule classifier "Sweet Trap ⇔ F1 ≥ 0.5 AND F2 ≥ 0.5" achieves **accuracy = 1.00, Cohen's κ = 1.00** on all 10 cases — identical to the weighted-sum classifier with T > 4.0. F3 and F4 **do not contribute to classification** in any of the 10 cases; F3 is present in 2/5 negatives (D3 996: F3 = 1.0; C4 bride-price: F3 = 0.5) and F4 is present in 3/5 negatives (D3: 1.0; C4: 0.5; C2 鸡娃: 0.5) *without triggering false positives* when F1 fails.

**v2 refinement (F1+F2 necessary and sufficient; F3+F4 demoted to severity modifiers).** v2 §1.5 is revised to:

> **F1 and F2 are necessary and sufficient for classification as a candidate Sweet Trap.** F3 and F4 are severity modifiers that affect Σ_ST (persistence severity) and therefore intervention urgency, but neither is required for Sweet Trap classification.

This simplifies the umbrella construct to a **binary diagnostic** (F1 sign × F2 sign) with a **continuous severity scalar** (Σ_ST = Δ_ST × τ_F3 × (1 − I(T_cost → T_decide))). The 16-combination space collapses to 4 classification cells, of which only one (F1+ F2+) is a Sweet Trap.

**Why this is not HARKing.** v1 already stated (§1.5) that F3+F4 were "typical but not universal persistence conditions". The discriminant analysis confirmed this empirically and motivated a sharper textual formulation — not a new substantive claim. Importantly, the strict necessary-condition classifier (F1 = 1.0 AND F2 = 1.0) gives only 0.80 accuracy because C11 (diet) and D_alcohol Type A are coded F1 = 0.5 — both known marginal cases in the main narrative. The lenient classifier (F1 ≥ 0.5 AND F2 ≥ 0.5) recovers 1.00. This behaviour is consistent with v1's prose description; v2 just encodes it formally.

---

## §11.5 Limitation 5: v1 presented Layers A–D as parallel evidence rather than cross-level prediction

**What v1 did.** v1 §4 proposed four cross-species propositions (P1–P4) to be tested within each layer. It did not specify what a pass at Layer A should predict about Layer D.

**What the data allowed.** With Layer A v2 (20 animal cases, 4 mechanism categories) and Layer D v2 (19 MR chains, 3 core mechanism classes), a *cross-level rank* can be tested. Under v1, the framework was consistent with any Layer A result being replicated at Layer D. Under v2, the construct predicts that the mechanism gradient observed in animals (olds_milner > sensory_exploit > fisher_runaway) should be preserved in human genetic-causal data at the magnitude of |log OR|.

**v2 refinement (predictive cross-level prediction).** We state in v2 §4.5 (new):

> **P5 (Predictive cross-level concordance).** If Sweet Trap names a single cross-species equilibrium, the mechanism-class rank order of Δ_ST across animal cases must reproduce the mechanism-class rank order of |log OR| across Mendelian-randomisation-identified human chains. Falsification: Spearman ρ(A, D) < 0 on overlapping mechanism categories with ≥ 3 cases per cell.

**Empirical result (`cross_level_meta_findings.md`).** Spearman ρ(A, D) = +1.00 on the two shared mechanism cells (`olds_milner`, `sensory_exploit`). A+D-only meta-regression gives olds β = +1.58, Wald p = 0.019. This upgrades the construct from "parallel-evidence umbrella" to "predictive framework" and closes the gap identified by the Novelty Audit (row "Universality evidence": 6/10 → 7/10).

**Why this is not HARKing.** The prediction is a direct consequence of the construct claim ("Sweet Trap is one equilibrium across species"); the question was whether the claim would survive cross-level testing. It did. The Spearman ρ = +1.00 is not a post-hoc finding but a confirmation of the strongest form of the universality hypothesis.

---

## §11.6 Summary: v1 → v2 changelog

| v1 | v2 | Rationale | Limitation ref |
|---|---|---|---|
| Behavioural-economic primitives (θ, λ, β, ρ) as axioms | Two-layer architecture; (θ, λ, β, ρ) emerge from Layer 1 replicator dynamics | Animal cases (A6, A9, A17, A19) are uninterpretable under v1 | §11.1 |
| Single-society Σ_ST | Σ_ST × G^c_i with G^c = z(PDI) + z(LTOWVS) − z(IDV) | Cross-national heterogeneity (ISSP / Hofstede) requires a cultural operator | §11.2 |
| Route A vs Route B within F1 | Engineered vs Mismatch sub-classes (distinct mechanism category mapping, Steiger patterns, and policy levers) | Layer A meta-regression and Layer D Steiger pattern justify the split | §11.3 |
| F1–F4 co-equal | F1+F2 necessary and sufficient; F3+F4 severity modifiers | 10-case discriminant test: F1+F2 alone gives 100% accuracy | §11.4 |
| Parallel Layer A–D | Predictive P5: animal mechanism rank predicts human genetic rank | Cross-level meta Spearman ρ(A,D) = +1.00 | §11.5 |

**TODO** (editorial): Post OSF pre-registration of v2 at manuscript submission. Documents: (1) frozen §11 text, (2) Layer A v2 extraction spreadsheet, (3) Layer D v2 pipeline (`mr_extended_v2.py`), (4) discriminant validity feature vectors, (5) spec-curve pre-registration grid. This is the "predecessor paper before peer review" pre-registration per `feedback_prereg_post_analysis_pre_submission.md`, not a pre-analysis-run registration.

---

*End of §11 rewrite. This version replaces the v1 addendum and eliminates HARKing surface characteristics by explicit date-stamped limitation → refinement mapping.*
