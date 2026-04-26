# Revision Log — Stage 1-B (Theory Repair for NHB Article Standard)

**Status**: v1.0, 2026-04-18
**Scope**: Targeted repair of Paper 1 theory files to address 2 fatal flaws (F1, F2) + 8 major issues (M1–M8) identified in rigor audit.
**Standard**: NHB Article (not BBS Target Article). Tolerance: "operational definition + explicit scope" rather than axiomatic derivation.
**Do not touch**: `predictions.md`, `paper1_theory_draft.md`, `abstract.md` (Stage 1-A workspace). v3.0 manuscript merge is Stage 2.

---

## Map: rigor-audit item → files changed

| Item | Location | Files edited |
|:---:|:---|:---|
| **F1** T2 matching convention | `theorems.md` §T2.1, new §T2.1.1; `proof_sketches_expanded.md` §F.4 (now §1.4) | 2 |
| **F2** A3 scope/tautology | `axioms_and_formalism.md` §A3 (scope-defining reframe + A3.0 criterion); `lemmas.md` L3 scope tag | 2 |
| **M1** A3 vs A4 independence | `axioms_and_formalism.md` §A4 → P1 parameterization; `theorems.md` + `proof_sketches_expanded.md` "under A4" → "under P1" | 3 |
| **M2** T1 decay-rate precondition | `theorems.md` T1.1 precondition block | 1 |
| **M3** T2 shrinkage invariance | `theorems.md` T2 Step 4 scope; `proof_sketches_expanded.md` §1.7 | 2 |
| **M4** T3 → P5 derivation gap | `theorems.md` T3.4 reframed as "empirical regularity" (was theorem-derived) | 1 |
| **M5** T4 basin-radius claim | `theorems.md` T4.1 (basin → Observation 4.1); `proof_sketches_expanded.md` §5 qualifier | 2 |
| **M6** RST Lande mean-field | `lemmas.md` new L4.1 mean-field derivation; `axioms_and_formalism.md` §7.1 cross-ref | 2 |
| **M7** Fisher positioning | `positioning.md` §5; `relationship_to_existing_models.md` §4 | 2 |
| **M8** RA positioning | `positioning.md` §2; `relationship_to_existing_models.md` §2 | 2 |

---

## F1 — T2 matching convention (fatal flaw, now resolved at NHB standard)

**Before** (`theorems.md` T2.1):
> "|Δb_signal|/|Δb_info| ≥ (1−w_max)/w_max ≥ 1.5"

**After**:
> "Under **matched marginal perceived-utility conditions** (operational definition T2.1.1), |Δb_signal|/|Δb_info| ≥ (1−w_max)/w_max ≥ 1.5 in the Sweet Trap regime where σ' is bounded below by σ'_min > 0."

**New T2.1.1**: operational dose-matching (equal ΔU_perc output units in RCT calibration) + scope restriction to non-saturated regime (σ'(αψφ) ≥ σ'_min > 0). Saturation-limit degeneracy acknowledged honestly.

**Proof-sketch §1.4 change**: matching convention now stated as an empirical operationalization (dose-matched RCT arms), not an abstract axiom. Resolves L5 "σ'→0 at saturation" apparent self-contradiction by clarifying Sweet Trap requires Δ_ST > 0, not full saturation.

**Status under NHB**: resolved. BBS would still push for axiomatic derivation; NHB accepts "operational definition + scope statement".

---

## F2 — A3 endorsement-inertia tautology (fatal flaw, now resolved at NHB standard)

**Before** (`axioms_and_formalism.md` A3.3):
> "∀i, w_i ≤ w_max < ½"

This was tautological: "Sweet Trap agents are by assumption bounded-w" → "the Sweet Trap effect holds for bounded-w agents" → vacuous.

**After**: A3 reframed as **scope-defining axiom** with operational criterion A3.0:

> "**Sweet Trap scope (operational criterion A3.0)**: Empirically determined by (a) post-full-information-intervention abandonment rate < 30%, OR (b) observed choice pattern b_i satisfies argmax structure with inferred w < 0.45 over N ≥ 10 repeated choices. Agents outside this scope (e.g., one-glass-of-wine moderate-belief-calibration case) are by definition not Sweet Trap cases."

**L3 change**: added "within A3 scope" qualifier so the akrasia lemma is explicit about applicability.

**Status under NHB**: resolved. The scope is now *empirically testable* (not circularly defined); a population showing >30% abandonment upon information intervention is classified outside Sweet Trap scope and A3 does not apply to them. This converts A3 from a circular claim into a falsifiable scope statement.

---

## M1 — A3 vs A4 independence (demoted A4 to P1)

**Before**: A4 (hyperbolic discount) stated as a primary axiom.

**After**: A4 demoted to **Parameterization P1: Temporal preference form**. The core claim retained is that *some* form of temporal weighting δ'(τ) < 0 exists; hyperbolic is chosen for parsimony + life-history derivation (McNamara 2009), but the framework is parameterization-robust. Exponential δ = e^(−kτ) and Laibson β–δ remain derivable alternatives under P1.

**Downstream**: "under A4" → "under P1 (hyperbolic parameterization)" throughout `theorems.md` and `proof_sketches_expanded.md`. Core axiom count now 3 + 1 parameterization; the 4-axiom structural nominal preserved by keeping A4 as "Axiom A4 (Parameterized): …" with P1 sub-tag for clarity.

**Status**: resolved. Independence concern no longer applies because we do not claim A4 is irreducible.

---

## M2 — T1 decay-rate precondition

**Before**: T1 stated exponential decay with rate c ≥ α·ℓ·ε² − β·δ_max·M − D^drift without specifying when the bound is positive.

**After**: precondition added to T1.1:

> "T1 assumes α_i · ℓ · ε² > β_i · δ_max · M + D_i^drift (reward-sensitivity at equilibrium dominates cost-aversion-times-drift). Under this precondition, c > 0 and LSE holds. Violation of this precondition produces a saddle rather than a sink; see T1.4 scope."

**Status**: resolved.

---

## M3 — T2 shrinkage invariance scope

**Before**: T2 Step 4 asserted shrinkage-invariance as a theorem claim.

**After**: reframed as *conditional*: shrinkage-invariance holds *iff* field-to-RCT shrinkage factor κ applies symmetrically to both channels. DellaVigna-Linos 2022 documented κ ≈ 1/3 for info-type nudges; evidence for signal-redesign shrinkage is more limited. Flagged as scope boundary requiring empirical verification.

**Status**: resolved at NHB level. The paper now honestly states that the 1.5× field ratio is robust *under symmetric shrinkage*, not as a universal theorem.

---

## M4 — T3 → P5 derivation gap (P5 reframed empirical)

**Before**: P5 (cross-species rank preservation) implicitly presented as derivable from T3.

**After**: T3.4 now states explicitly — "T3 asserts that Sweet Trap *exists* across species; it does not assert numerically identical Δ_ST magnitudes. Cross-species *rank preservation* is an **empirical regularity consistent with T3**, not a theorem-derived prediction." P5 header in predictions.md to be flagged at Stage 2 manuscript integration (marker left; not edited here per scope).

**Status**: resolved. No overclaiming.

---

## M5 — T4 basin-radius claim (theorem → observation)

**Before** (`theorems.md` T4.1):
> "basin of attraction are **strictly larger** under EST than under MST"

**After**: basin comparison removed from T4 theorem statement. New **Observation 4.1** (explicitly labeled non-theorem):

> "Empirically, EST sub-class (algorithmic and engineered-deception) shows longer behavioral persistence and larger relapse rates after cessation than MST sub-class, consistent with wider basin of attraction. Formal analytical characterization of basin radius as a function of Δ_ST and ψ is left to future work."

**Proof-sketch §5** qualifier: explicitly flagged as "directional claim + scale estimate", not rigorous bound.

**Status**: resolved.

---

## M6 — RST Lande substitution mean-field derivation

**Before**: §7.1 used W̄_perc in Lande-Kirkpatrick equations without derivation from individual-level choice.

**After**: new **Lemma L4.1** (mean-field derivation):

> "For a population with individual ψ_i ~ F(ψ), population-mean perceived utility W̄_perc(q̄, ȳ) = ∫ U_perc(s; q̄ + η, ȳ) dF(η) is well-defined in mean-field limit (large N + weak individual deviation). Gaussian approximation + Fourier methods give ∂W̄_perc/∂q̄ as population-scalar gradient; Lande-Kirkpatrick equations (7.2)-(7.3) hold with W̄_perc substituted for W̄_fit. (Sketch + standard technique; full calculation deferred to math supplement §C.3.)"

Honest acknowledgement: full derivation is "sketch + standard technique" not complete proof. §7.1 of axioms file cross-references L4.1.

**Status**: resolved at NHB level.

---

## M7 — Fisher Runaway positioning

**Before** (`positioning.md` §5, `relationship_to_existing_models.md` §4):
> "Fisher Runaway ⊂ RST ⊂ Sweet Trap" (framed as strict containment)

**After**: reframed as **related but distinct theory**:

> "Fisher Runaway and RST share qualitative logic (self-reinforcing dynamics driven by trait-preference covariance) but are **formally different dynamical systems**: Fisher uses W̄_fit (mean fitness, bounded by biological fitness); RST uses W̄_perc (mean perceived utility, unbounded by fitness, derived from L4/L4.1). RST is a **perceived-utility-driven analogue** of Fisher's genetic-fitness-driven runaway, with different equilibrium structures."

**Status**: resolved. Honest positioning that acknowledges qualitative-but-not-formal equivalence.

---

## M8 — Rational Addiction positioning

**Before** (`positioning.md` §2, `relationship_to_existing_models.md` §2):
> "RA = degenerate specialization of Sweet Trap with {w=1, λ=0, U_perc ≡ U_fit}"

**After**: reframed as **conceptual complement**:

> "RA (Becker-Murphy 1988) and Sweet Trap are **boundary-adjacent but disjoint domains**. RA assumes U_perc ≡ U_fit (agent correctly forecasts long-run utility including addiction dynamics), which by construction precludes Sweet Trap (Δ_ST ≡ 0). Sweet Trap extends to cases where RA's foresight assumption fails — i.e., behaviors that *look* addictive but cannot be rationalized under RA. The two theories are conceptual complements rather than nested models."

**Status**: resolved. Avoids the "RA is a special case of Sweet Trap" overclaim that reviewers flagged as poorly motivated (RA's foresight assumption is qualitatively different, not a parameter limit).

---

## Overall NHB-standard assessment

| Item | Resolution grade under NHB Article standard |
|:---:|:---|
| F1 | **Resolved** — operational matching convention + scope restriction to non-saturated regime |
| F2 | **Resolved** — A3 now scope-defining with empirical criterion (abandonment rate / inferred w) |
| M1 | **Resolved** — A4 demoted to P1 parameterization; independence concern dissolved |
| M2 | **Resolved** — precondition explicit |
| M3 | **Resolved** — symmetric-shrinkage assumption stated; flagged for empirical verification |
| M4 | **Resolved** — P5 reframed as empirical regularity; no overclaim |
| M5 | **Resolved** — basin claim moved from theorem to empirical observation |
| M6 | **Mostly resolved** — mean-field sketch added; full derivation still "standard technique" gesture. **Arguable**: a BBS referee would push for complete algebra; NHB-level reviewer should accept. |
| M7 | **Resolved** — "related but distinct" positioning preserves Sweet Trap's extensions without overclaiming containment |
| M8 | **Resolved** — "conceptual complement" frame avoids RA-as-special-case overclaim |

**Arguable items remaining**: M6 (full mean-field derivation still gesture to supplement); matching convention (F1) now operational but a theoretically-minded referee could request axiomatic justification. Both are acceptable at NHB Article standard.

---

## Recommendations for Stage 2 (v3.0 manuscript integration)

1. **Propagate to main manuscript abstract/intro**: the F2 scope reframe (A3 as scope-defining axiom) is the most substantive theoretical move — the introduction must explain Sweet Trap as a *behavioral regime* characterized by empirical criterion A3.0, not a universal claim about human choice.

2. **Methods / Theory section**: add a one-paragraph "operational criterion for scope" subsection that states A3.0 explicitly. Reviewers will look for this.

3. **Matching convention (F1)**: the operational dose-matching definition should be echoed in Paper 2's empirical-comparison methodology (Paper 2 compares info-arm vs signal-arm RCTs; matching convention is the statistical principle).

4. **P5 (M4)**: downgrade predictions.md §P5 header from "theorem-derived prediction" to "empirical regularity consistent with T3". Stage 1-A may flag.

5. **Discussion**: add "future work" paragraph explicitly listing (a) full mean-field derivation for RST/L4.1, (b) formal basin-radius characterization (T4 Observation 4.1), (c) asymmetric-shrinkage test for T2 (M3). These honest gaps strengthen the paper; reviewers appreciate them.

6. **Positioning paragraph in intro**: reflect the Fisher-as-"related-but-distinct" (M7) and RA-as-"conceptual-complement" (M8) reframings; the old "strict containment" language will read as overclaim and invite pushback.

7. **Glossary / nomenclature**: note that "axioms" now refer to A1–A4 with A4 sub-labeled as parameterization P1; this nomenclature should be consistent across the v3.0 manuscript.

---

*End of Stage 1-B revision log. All changes trace to rigor_audit.md F1, F2, M1–M8. Theory core structure (4 axioms, 4 theorems, 5 lemmas, 5 predictions) preserved; A4 re-labeled as parameterization, L4.1 added.*
