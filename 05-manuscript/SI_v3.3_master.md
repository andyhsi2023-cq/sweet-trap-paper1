---
title: "Supplementary Information — Sweet Trap: a theory of reward–fitness decoupling with cross-species empirical validation"
author:
  - Lu An
  - Hongyang Xi (corresponding)
date: "2026-04-18"
---

# Supplementary Information

## Sweet Trap: a theory of reward–fitness decoupling with cross-species empirical validation

**Authors:** Lu An, Hongyang Xi (corresponding)
**Linked manuscript:** `main_v3.3_submission` (Nature Human Behaviour Article submission)
**OSF deposit:** <https://osf.io/ucxv7/>
**Version:** SI v3.3 (2026-04-18)

---

## Cross-referencing convention for this SI

- References of the form **"main-text Fig. N"** and **"main-text Table N"** point to the six figures and two tables of the main manuscript (`main_v3.3_submission`).
- References of the form **"Supplementary Figure S*N*"** and **"Supplementary Table S*N*"** are internal to this SI document; numbering restarts at S1 within this file.
- References of the form **"Supplementary Note *N*"** and **"Supplementary Appendix *X*"** point to sections of this SI (see Table of Contents below).
- References of the form **"ED Table N"** and **"ED Fig. N"** point to Extended Data items submitted alongside the main manuscript.

All bracketed tokens of the form `[OSF_DOI_TO_INSERT]` in the source outline have been replaced by the live OSF link above.

---

## Table of Contents

1. **Supplementary Note 1** — SI overview, block structure, and index of source files
2. **Supplementary Appendix B** — Axiomatic derivations of θ, λ, β, ρ from Layer 1 evolutionary dynamics
3. **Supplementary Note 2** — §11 framework refinements transparency log (v1 → v2)
4. **Supplementary Note 3** — §11.7 Engineered Deception sub-class (pig-butchering; aggressive-mimicry homologues)
5. **Supplementary Note 4** — §11.7b PUA extended analysis (boundary case, F2 inter-coder disagreement)
6. **Supplementary Note 5** — §11.8 Policy predictability as construct derivative
7. **Supplementary Appendix H** — Orthogonal global-health implications (Levin-PAF / DALY)
8. **Supplementary Note 6** — Extended Data items (narrative)
9. **Supplementary Note 7** — Expanded figure legends for main-text Fig. 1–6

---

\newpage

# Supplementary Note 1 — SI overview and index of source files

**Paper:** Sweet Trap: a theory of reward–fitness decoupling with cross-species empirical validation
**Version:** v3.3 NHB Article (theory + empirics merged)
**Status:** 2026-04-18

The v3.3 SI is organised in two blocks: **SI-Math** (theory details, 2,500–4,500 words) and **SI-Empirical** (appendices A–I, carried forward from v2.4 with minor updates). All material is available at OSF deposit <https://osf.io/ucxv7/>.

## Block 1 — SI-Math: Theoretical Supplement (~3,500 words; 4,500-word ceiling)

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

- §4.1 **T1 Stability.** Full Jacobian computation; Lyapunov function construction (*V* = ½‖*s* − *s\**‖² + *g*(Δ_ST); *V̇* ≤ −*cV*); basin-radius estimate. Stage 1-B M2 precondition (★) statement and interpretation.
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
- §7.8 Containment diagram (Supplementary Figure S1).

### SI-Math §8. Nomenclature (full symbol table)

Verbatim from `paper1-theory/01-math-foundation/nomenclature.md`. Covers every primitive, parameter, and derived quantity used in the main text and methods.

### SI-Math §9. Appendix to Stage 1-B revisions

- §9.1 Revision log (from `paper1-theory/00-outline/revision_log_stage1B.md`): F1–F3 fatal flaws and M1–M8 majors, each with before/after wording.
- §9.2 Integrity audit log (from `paper1-theory/00-outline/integrity_audit_log.md`): P1–P5 empirical-status audit against Paper 2 v2.4 source files.
- §9.3 Peer-reviewer audit archive (Phase D).

<!-- outline item pending: SI-Math §1–§9 full text drafts are retained in `paper1-theory/` source repository and will be compiled into a separate SI-Math PDF at revision stage. The axiomatic derivation of θ, λ, β, ρ (Supplementary Appendix B below) is the load-bearing theoretical supplement for the initial submission. -->

---

## Block 2 — SI-Empirical: Appendices A–I

### Appendix A — Layer A (Animal meta-analysis): full 20 cases

- A.1 PRISMA flow diagram (380 → 312 → 48 → 20).
- A.2 Extraction table: 20 cases × 6 columns (species, mechanism, F1 route, Δ_ST, SE, quality tier).
- A.3 Forest plot (Supplementary Figure S2) and funnel plot (Supplementary Figure S3).
- A.4 Meta-regression moderator tables (mechanism, F1 route, quality tier, vert/invert).
- A.5 Publication-bias assessment (Egger's regression with bounded-Δ_ST caveats).
- Source: `02-data/processed/layer_A_v2_extraction.csv`; `00-design/pde/layer_A_animal_meta_v2.md`.

### Appendix B — Layer D (Mendelian randomisation): full 19 chains

- B.1 Per-chain table: exposure × outcome × instrument *n* × *F*-statistic × IVW OR [95% CI] × *p* × Steiger direction × method-concordance rating.
- B.2 Forest plots (Supplementary Figures S4–S6 by sub-class).
- B.3 Funnel plots, LOO, single-SNP Wald ratios.
- B.4 MVMR results (three models).
- B.5 Steiger rationale (socially-stratified GWAS architecture; Hemani 2017; Davies 2019).
- Source: `02-data/processed/mr_results_all_chains_v2.csv`; `00-design/pde/layer_D_MR_findings_v2.md`.

*(Note: "Appendix B" in this empirical block is distinct from "Supplementary Appendix B — Axiomatic Derivations" at the head of this SI, which is the load-bearing theoretical appendix. Empirical-block Appendix B above is deferred to OSF with a pointer; the theoretical Appendix B is reproduced in full below.)*

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
- D.5 PUA boundary case handling (Supplementary Note 4 cross-reference).
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

Reproduced in full below as **Supplementary Appendix H**.

### Appendix I — PUA boundary case

Reproduced in full below as **Supplementary Note 4** (§11.7b).

---

## Figures and tables index (SI-internal)

- **Supplementary Figure S1** — Containment diagram (Sweet Trap and neighbouring theories; companion to SI-Math §7.8).
- **Supplementary Figure S2** — Layer A full forest (20 cases).
- **Supplementary Figure S3** — Layer A funnel plot.
- **Supplementary Figures S4–S6** — Layer D MR forests by sub-class.
- **Supplementary Figure S7** — v2.3 DALY dual-anchor waterfall + Sankey (retained for reference; companion to Supplementary Appendix H).
- Additional SI figures per appendix are released at OSF <https://osf.io/ucxv7/>.

Supplementary Tables S1–S*n* are released in spreadsheet form (`.csv` and `.xlsx`) at OSF; see per-appendix source-file pointers above.

---

\newpage

# Supplementary Appendix B — Derivation of the Layer 2 primitives (θ, λ, β, ρ) from Layer 1 evolutionary dynamics

**Status:** Draft v1 (2026-04-17)
**Purpose:** Formal derivation of the four behavioural-economic primitives in the main-text Layer 2 utility (L4) from Layer 1 replicator / life-history fundamentals. Required to support the claim in §3.2 of `sweet_trap_formal_model_v2.md` that v2 *derives* rather than *assumes* the (θ, λ, β, ρ) quadruple.
**Target length in SI:** 3–4 printed pages.
**Author map:** Lu An (formal model) and Hongyang Xi (empirical calibration).
**Depends on:** Section 3 of main formal model.

---

## B.0 Notation and set-up

Throughout this appendix we use the following primitives, reused from the main model:

- *W(τ, y, e)*: mean fitness of an individual with trait *τ* and preference *y* in environment *e*. For humans, fitness is reinterpreted as *long-run individual welfare* (≥ 20 year consumption-equivalent utility; see §2 of main model for why this reinterpretation is conservative).
- *R(a, S)*: the reward signal elicited by action *a* in signal-state *S*. Generated by the evolved reward architecture; treated as exogenous at the individual's decision epoch.
- *F(a)*: fitness / welfare outcome of action *a*.
- *e_anc*, *e_cur*: ancestral and current environments (equivalently, ancestral and current signal distributions).
- *Lifespan*: *T* total, with discrete decision epochs *t* = 1, …, *T*. Define *φ_t* = probability of survival from *t* to *t+1* under ambient mortality. *φ_t* captures extrinsic risk: predation, disease, violence, accident, excluding voluntary lifestyle-induced mortality.

All four derivations share a common strategy. We start from Layer 1 — an evolutionary or replicator dynamic that the organism does not observe — and ask: *what Layer 2 parameter must an individual decision-maker endowed with the resulting architecture behave as if she is maximising?* The answer is the primitive. This is the **evolutionary consistency** approach: Layer 2 preferences are not axiomatic; they are the "as-if" utility function an evolutionary optimum would display at the individual level.

A subtle but important caveat: the primitives are evolutionary *optima for ancestral e_anc*, not for *e_cur*. Their miscalibration in *e_cur* is precisely what generates Δ_ST > 0. The derivations below therefore establish *where the primitives come from* and *why they fail to update*, which is exactly the bridge the Layer 1 → Layer 2 reinterpretation in §3.2 claims.

---

## B.1 Derivation of θ — the amenity / reward weight

### B.1.1 Statement

*θ_i* scales the marginal utility an individual *i* derives from the reward signal *R(a, S)*. The claim in main-text Table §3.2 is that θ originates as *the steepness of the evolved reward gradient at the decision point*, calibrated against ancestral fitness.

### B.1.2 Derivation

Consider an ancestrally-calibrated reward architecture that returns *R_agent(a) = Φ(E_{e_anc}[F(a)])* for some smooth increasing function Φ. That is, the reward signal reports the expected ancestral fitness of the action, through a monotone transform.

Suppose the individual chooses *a* to maximise a period utility *U(a) = θ · R_agent(a) − c(a)*, where *c(a)* is a known immediate cost. The first-order condition is

$$
θ \cdot \frac{\partial R_{\text{agent}}}{\partial a}\bigg|_{a^*} \;=\; \frac{\partial c}{\partial a}\bigg|_{a^*}.
$$

If the architecture is evolutionarily optimal, the action *a\** selected by this first-order condition must coincide with the ancestral fitness optimum *a_anc* = argmax_{a} F_{anc}(a). Substituting and using *R_agent = Φ(E[F])*:

$$
θ \cdot Φ'(E[F(a^*)]) \cdot \frac{\partial E_{e_{\text{anc}}}[F]}{\partial a}\bigg|_{a^*} \;=\; \frac{\partial c}{\partial a}\bigg|_{a^*}.
$$

At the ancestral optimum, ∂E[F]/∂a = ∂c/∂a (envelope / Hamiltonian condition for evolutionary equilibrium; Charnov 1976), so cancelling gives:

$$
\boxed{\; θ^* \;=\; \frac{1}{Φ'(E[F(a^*)])} \;}
\tag{B.1}
$$

**Interpretation.** θ is the *inverse slope of the reward-transform at the ancestral optimum*. An organism whose reward function is highly sensitive (steep Φ′) near the ancestral optimum has low θ (small marginal utility of R — the signal does a lot of work on its own); an organism whose reward function is flat near the optimum needs high θ to align behaviour with fitness. θ is thus **not a free individual parameter but a function of evolved reward curvature**.

### B.1.3 Why θ miscarries in e_cur

If the current environment shifts the signal distribution such that *R_agent* activates at an action *a′ ≠ a_anc*, the individual still applies the fixed θ* from equation (B.1). The FOC is now:

$$
θ^* \cdot Φ'(E_{e_{\text{cur}}}[F(a′)]) \cdot \frac{\partial E_{e_{\text{cur}}}[F]}{\partial a}\bigg|_{a'} \;=\; \frac{\partial c}{\partial a}\bigg|_{a'}.
$$

*E_{e_cur}[F]* need not satisfy the ancestral envelope condition — ∂E_{cur}[F]/∂a at *a′* can be negative while θ*·Φ′ still solves the FOC, giving us F1 (Δ_ST > 0): the agent chooses actions that reduce expected current fitness while the reward architecture still reports positive signal.

**Reference:** Grafen (1990, *Journal of Theoretical Biology*); Houston & McNamara (1999). The derivation here follows the "evolved preferences" framework of Robson (2001, *Journal of Economic Literature*).

### B.1.4 Heterogeneity of θ

Heterogeneity in θ across individuals arises from heterogeneity in the evolved reward transform Φ itself, in turn generated by (i) genetic variation in reward-circuit sensitivity (dopaminergic polymorphisms; DRD2 Taq1A, DAT1 VNTR), (ii) developmental plasticity (Kaplan–Gangestad 2005 environmental calibration), and (iii) for humans only, cultural overlay on Φ (Henrich 2015 — cultural normalisation of the reward transform). This generates the empirical dispersion θ_i that the main-text L4 utility admits.

---

## B.2 Derivation of λ — the externalisation share

### B.2.1 Statement

*λ_i* is the share of the fitness / welfare cost *C(a)* borne by individuals other than the decision-maker (spouse, offspring, future self of others, the public). Main-text claim: λ is *generated by population structure*, specifically cohort and kin differential, which Layer 1 lacks natively.

### B.2.2 Derivation via inclusive fitness

Hamilton (1964) shows that the evolutionarily correct decision criterion for a social organism is *inclusive fitness*:

$$
F_{\text{incl}}(a) \;=\; F_{\text{self}}(a) + \sum_{j \neq i} r_{ij} F_j(a)
$$

where *r_{ij}* is the coefficient of relatedness (0.5 for parent–offspring; 0.25 grandparent–grandchild; 0 unrelated). An ancestrally adapted organism optimises inclusive fitness, not personal fitness. The first-order condition is

$$
\frac{\partial F_{\text{self}}}{\partial a} + \sum_{j} r_{ij} \frac{\partial F_j}{\partial a} \;=\; 0.
$$

Let *C(a) ≡ −∂F/∂a · Δa* be the (positive) cost of increasing *a* marginally. Partition *C(a)* into self-borne and other-borne:

$$
C(a) = C_{\text{self}}(a) + C_{\text{other}}(a), \quad \text{with } λ \equiv \frac{C_{\text{other}}(a)}{C(a)}.
$$

Under Hamilton's rule, the individual *does not internalise C_other* at face value; she internalises it weighted by relatedness. The effective cost she weighs in her utility is:

$$
C_{\text{effective}}(a) = C_{\text{self}}(a) + \bar r \cdot C_{\text{other}}(a) = (1 - λ) C(a) + \bar r · λ · C(a),
$$

where *r̄* is the average relatedness of the other-party cost-bearers. Equivalently:

$$
\boxed{\; (1 - λ_{\text{Layer 2}}) \;=\; (1 - λ) + \bar r \, λ \;=\; 1 - λ(1 - \bar r) \;}
\tag{B.2}
$$

**Interpretation.** λ_Layer 2 = λ(1 − r̄). Two limits:

- If *r̄ = 1* (all cost-bearers are the self), λ_Layer 2 = 0: full internalisation. This is the Layer 1 baseline.
- If *r̄ = 0* (all cost-bearers are unrelated strangers — the public good), λ_Layer 2 = λ: no internalisation.

**The empirical λ in the Sweet Trap main-text thus corresponds to λ(1 − r̄), not raw λ.** This is important: 鸡娃 (intensive-parenting) spending has r̄ = 0.5 (child), so a parent's effective externalisation is *halved* relative to a policy measure of raw λ. This is why pure selfishness is not required for a Sweet Trap — even Hamiltonian kin altruism leaves a *λ* wedge equal to *λ(1 − 0.5) = 0.5 λ*.

### B.2.3 Why λ is not only kin-externalisation

Layer 2 admits three additional non-kin channels that Hamilton does not cover but that cultural evolution generates:

- **Intergenerational externalities within lineage (trans-lineage discounting):** even with *r_ij = 0.5* to one's child, evolved discounting (see §B.3) reduces the salience of future child welfare. Effective *λ* for horizons > 20 years is *λ_raw × (1 − r̄) × β^k*, where *β^k* is the hyperbolic discount factor evaluated at horizon *k*. Bride-price (彩礼) and 鸡娃 both activate this channel.
- **Public-good externalities (genuine non-kin):** 996 in Chinese firms produces cost to spouse (*r̄ = 0*, legally a non-kin cost-bearer under evolutionary standards), co-workers (*r̄ ≈ 0*), and downstream. *λ (1 − r̄) ≈ λ*.
- **Self-to-future-self externalities:** consumption today is cost to future-self. Inter-temporal λ: *λ (1 − β^k)*, where *β* is the hyperbolic factor and *k* the horizon. This is where λ and β intersect.

### B.2.4 Animal analogue of λ

In animal Fisher runaway, the "cost-bearer" of a male's ornament is the male itself (within-generation) or his offspring (between-generation). The animal-λ is captured by the ratio *(male mortality cost) / (female preference-maintenance cost)*. Kokko et al. (2002) show runaway magnitude scales with this ratio — Layer 1's emergent λ. Main-text Proposition 2 exploits this cross-species scaling.

**References:** Hamilton (1964, *J. Theor. Biol.*); Frank (1998, *Foundations of Social Evolution*) for inclusive-fitness accounting; Bernheim & Taubinsky (2018, *Handbook of Behavioural Economics*) for λ-as-internality; Bergstrom (1995, *QJE*) for kinship economics.

---

## B.3 Derivation of β — the present-bias / hyperbolic-discounting parameter

### B.3.1 Statement

*β_i* is the quasi-hyperbolic present-bias parameter of Laibson (1997): *U_t = u_t + β ∑_{k≥1} δ^k u_{t+k}*. Main-text claim: β is derivable from evolutionary life-history theory under extrinsic mortality, specifically from Stearns (1992) and Kaplan–Gangestad (2005).

### B.3.2 Derivation

Consider an ancestral organism with survival probabilities *φ_t* at each period. Its evolutionary expected future fitness is

$$
V_t \;=\; F_t + \sum_{k \geq 1} \left( \prod_{s=0}^{k-1} φ_{t+s} \right) F_{t+k}.
$$

**Step 1 — Constant mortality benchmark.** If *φ_t = φ* is constant, the expected future fitness is

$$
V_t = F_t + \sum_k φ^k F_{t+k},
$$

which is *exponentially* discounted with rate *δ = φ*. Standard exponential discounting arises naturally as *the survival factor of a constant-hazard environment*.

**Step 2 — Youth-elevated extrinsic mortality.** Empirical and phylogenetic evidence (Hamilton 1966 on senescence; Williams 1957; Stearns 1992 §3) shows that ancestral *φ_t* is *not* constant but is systematically *lower in early life* due to (a) predation on juveniles, (b) infant mortality, (c) adolescent violence. Let *φ_t = φ_youth < φ_adult* for *t < T_youth* and *φ_adult* for *t ≥ T_youth*. Then:

$$
V_t = F_t + \underbrace{φ_{\text{youth}}}_{\text{first-period discount}} F_{t+1} + \underbrace{φ_{\text{youth}}^{T_{\text{youth}}}}_{\text{youth-phase discount}} \sum_{k > T_{\text{youth}}} φ_{\text{adult}}^{k - T_{\text{youth}}} F_{t+k}.
$$

**Step 3 — The quasi-hyperbolic collapse.** Treat an adult-period decision as a sub-problem where *T_youth* periods are already past, but the evolved discounting reflex was *calibrated for a younger organism*. The adult's decision-time reward-signal architecture applies the ancestral *φ_youth* to the *next* period and *φ_adult* to later ones. Define

$$
β \;\equiv\; \frac{φ_{\text{youth}}}{φ_{\text{adult}}}, \quad δ \;\equiv\; φ_{\text{adult}}.
$$

Then

$$
V_t \;\approx\; F_t + β \sum_{k \geq 1} δ^k F_{t+k}.
\tag{B.3}
$$

This is exactly Laibson's quasi-hyperbolic form. **β emerges as the ratio of juvenile to adult survival in the ancestral environment.** For ancestral *H. sapiens* (Gurven & Kaplan 2007 *Population & Development Review*, Hadza and Tsimane demography), *φ_youth ≈ 0.95*, *φ_adult ≈ 0.99*, giving β ≈ 0.96 per-year → ~0.6 on a decade horizon, which matches empirically estimated β in behavioural experiments (Frederick, Loewenstein, O'Donoghue 2002 *J. Econ. Lit.*).

### B.3.3 Why β miscarries in e_cur

Current environment *e_cur* has dramatically lower extrinsic mortality — *φ_youth ≈ 0.995*, *φ_adult ≈ 0.995* — so the *evolutionarily correct* β is near 1. But the evolved architecture still applies the ancestral β ≈ 0.96. Individuals thus overweight the present relative to what their actual life history warrants. This is F1 on the temporal axis: *cor(R_agent, F) ≤ 0* for temporally-extended choices because R_agent is recruited with an evolved-β that doesn't match *e_cur*.

**Empirical corollary.** Populations with higher extrinsic mortality (e.g., historical high-violence environments, high-HIV regions) show *more* present bias, as β̂ is evolutionarily calibrated to local *φ*. This is confirmed by Pepper & Nettle (2017 *Behavioral and Brain Sciences*) life-history analyses and by Griskevicius et al. (2011 *JPSP*).

**References:** Stearns (1992 *Evolution of Life Histories*, ch. 5); Kaplan & Gangestad (2005) in *Handbook of Evolutionary Psychology*; Rogers (1994) — "Evolution of time preference by natural selection" *AER*; Robson & Samuelson (2007 *Econometrica*) — "The evolution of time preference with aggregate uncertainty."

### B.3.4 Heterogeneity of β

Heterogeneity in β across individuals arises from: (i) life-history-plasticity calibration (children who experienced high early-life adversity have lower β in adulthood — well-documented; see Belsky et al. 2012), (ii) genetic variation in serotonin reuptake (Kirby 2005), and (iii) age (β rises with age up to midlife, then falls; Green et al. 1994). All three are consistent with (B.3): they shift the agent's perceived *φ_youth*.

---

## B.4 Derivation of ρ — the status-quo / lock-in parameter

### B.4.1 Statement

*ρ_i* is the weight of history-dependent lock-in in period utility (*H(a, a_past)* in main-text L4). Main-text claim: ρ is an emergent parameter of cultural-replicator dynamics (M2 + M3 persistence mechanisms in main-text §1 F3), not an axiom of individual rationality.

### B.4.2 Derivation

Consider a population where the mean trait *τ* and mean preference *y* coevolve under cultural transmission (Danchin et al. 2018; Henrich 2015; Boyd & Richerson 1985). A conformist-biased cultural transmitter (common in human cultures) updates her preference *y_{i,t+1}* toward the population mean *τ̄_t* with weight *α_c*:

$$
y_{i,t+1} = (1 - α_c) y_{i,t} + α_c \bar τ_t + ε_{i,t}.
$$

Re-writing in terms of the individual's action *a_{i,t}* (which is a noisy realisation of *y_{i,t}*): at any decision epoch, the individual chooses *a_{i,t}* to match some fraction of her own past *a_{i,t-1}* and some fraction of *τ̄_t*. The implied period utility, *up to a constant*, that rationalises this behaviour is:

$$
U_{i,t}(a) = \tilde U_{i,t}(a) - ρ \cdot (a - a_{i,t-1})^2 - ρ_c \cdot (a - \bar τ_t)^2,
$$

where *ρ = α_h* is the individual-level habit weight and *ρ_c = α_c* is the peer-conformity weight. The main-text L4 collapses these into a single *ρ* with *H(a, a_past)* encompassing both individual habit and peer-norm anchoring, because the empirical identification strategy cannot separate them without group-level variation.

### B.4.3 Emergence of ρ from cultural runaway

Consider a two-trait replicator with cultural inheritance: trait *τ* (e.g., 鸡娃 spending) and preference *y* (valuing child prestige). Cultural covariance *G^c_{τ,y}* can be built up by assortative transmission (parents-who-value-child-prestige teach their children to value it). Lande–Kirkpatrick dynamics in cultural form (Henrich & Boyd 2002; Cavalli-Sforza & Feldman 1981):

$$
\dot{\bar τ} = G^c_τ \frac{\partial \bar W}{\partial τ} + G^c_{τ,y} \frac{\partial \bar W}{\partial y}, \quad \dot{\bar y} = G^c_y \frac{\partial \bar W}{\partial y} + G^c_{τ,y} \frac{\partial \bar W}{\partial τ}.
$$

If *G^c_{τ,y}* exceeds a critical threshold *G^{c,crit}*, the system is in a runaway equilibrium with the *individual-level* status-quo lock-in ρ emerging from the non-separable second term. Formally:

$$
\boxed{\; ρ_i \;=\; \alpha_h + \alpha_c + G^c_{τ,y}(i) \cdot \text{transmission fidelity}_i \;}
\tag{B.4}
$$

**Interpretation.** ρ is not a primitive; it is the *sum of three channels*: (1) individual habit formation *α_h*, (2) peer-conformity *α_c*, and (3) emergent cultural-genetic covariance that makes deviation from the current population mean costly. Channel (3) is the one that generates the Sweet Trap persistence: even an individual who knows (believes) her choice is welfare-reducing continues to conform, because *U* penalises deviation through the peer-state term.

### B.4.4 Why ρ generates persistence (F3)

Rearranging the individual FOC with ρ > 0 and letting the population be in the runaway equilibrium (*τ̄_t = a\**):

$$
a_{i,t}^* \;=\; \text{argmax}_a U_i(a) \;=\; \frac{\theta_i R'(a) + 2ρ_i (a_{i,t-1} + \bar τ_t)}{2 ρ_i + \text{curvature of } U}.
$$

For *ρ_i* large, *a_{i,t}\** → (*a_{i,t-1}* + *τ̄_t*) / 2. This is a stable attractor at the population equilibrium *τ̄*. Any individual-level intervention that changes θ or β but not τ̄ leaves *a\** close to the runaway equilibrium — hence the main-text P4 claim that exposure-targeting interventions (which change *τ̄* by altering the signal distribution) dominate belief-targeting interventions (which change θ_i or β_i only).

### B.4.5 Animal analogue of ρ

In peacocks (A7), ρ is the genetic covariance *G_{τ,y}* from Layer 1. The female preference and male ornament are locked because preference is partially inherited alongside the ornament. Cultural ρ is the same mathematical structure implemented on cultural rather than genetic variance. This is why main-text §3.3 Bridge claims **F3 has a unified form across layers**.

**References:** Boyd & Richerson (1985 *Culture and the Evolutionary Process*); Cavalli-Sforza & Feldman (1981 *Cultural Transmission and Evolution*); Henrich & Boyd (2002 *Current Anthropology*); Samuelson (1937 *Review of Economic Studies*) on status-quo in economics; Dixit & Pindyck (1994) on real-options analogue.

---

## B.5 Summary table — where the four primitives come from

| Primitive | Evolutionary source | Formal expression | Current-environment failure mode |
|:---:|:---|:---|:---|
| **θ** | Inverse steepness of evolved reward-signal transform Φ at ancestral optimum. | (B.1): *θ = 1/Φ′(E[F(a*)])*. | Signal distribution shifts so *a* ≠ *a*_anc; θ stays fixed → Δ_ST > 0. |
| **λ** | Inclusive-fitness weighting of non-self cost-bearers × post-ancestral cohort structure. | (B.2): *(1 − λ_L2) = 1 − λ (1 − r̄)*. | Novel non-kin cohorts (industrial workplaces; Ponzi-chains); r̄ drops; λ_L2 rises. |
| **β** | Ratio of juvenile to adult ancestral extrinsic-mortality survival probabilities. | (B.3): *β = φ_youth / φ_adult*. | *e_cur* has low and flat mortality; evolved β undervalues future. |
| **ρ** | Cultural habit + conformity + emergent cultural-genetic covariance *G^c_{τ,y}*. | (B.4): *ρ = α_h + α_c + G^c_{τ,y} · fidelity*. | Novel signals (livestream, MLM) accumulate cultural *G^c* before corrective information arrives. |

**The unified claim.** All four primitives are evolutionary solutions to the ancestral optimisation problem. They are not axioms; they are *maximand-consistent parameters of an ancestrally optimal agent*. Their continued use in *e_cur* produces F1 (reward–fitness decoupling) through four distinct but mathematically parallel mechanisms. Main-text §3.2's claim that v2 *derives rather than assumes* (θ, λ, β, ρ) is thus substantiated.

---

## B.6 Cross-species mapping of the four derivations

The derivations in B.1–B.4 apply *mutatis mutandis* across species. We give the mapping for the three representative Sweet Trap cases:

| Case | θ (reward-transform) | λ (externalised cost) | β (time preference) | ρ (lock-in) |
|:---|:---|:---|:---|:---|
| **A1 Moth** | Phototactic response *Φ* calibrated for moonlight. | n.a. (solitary, no kin decision). | Within-lifetime survival (pre-mating mortality is the cost); *β ≈ 0* because no post-decision period. | G_{τ,y} ≈ 0: no Lande runaway, just new-entrant flow. |
| **A7 Peacock** | Female preference transform *Φ* over ornament length. | Male ornament cost borne by male (non-kin to female); λ_{Layer 2 anim} ≈ 1. | Lifetime-reproductive-success discounting: runaway persists because post-mating cost falls on offspring carrying *τ*. | Classical Lande *G_{τ,y}* > *G^crit*. |
| **C4 彩礼 (bride-price)** | Cultural transform of bride-price → status signal. | Cost to groom family + bride future household; r̄ ≈ 0.25 (offspring, grandchildren) → λ_L2 ≈ 0.75 λ. | Generations of hyperbolic discounting applied to wealth allocation 20–40 years forward. | G^c_{τ,y} across counties is large; ρ high. |

The derivations can be applied to all 27 cases of `phenomenology_archive.md`. Case-by-case implementation is deferred to SI Appendix C (to be drafted as Layer A/B/C empirical results stabilise).

---

## B.7 Anticipated criticisms of the derivation

1. **"This is just hand-waving — you're renaming existing behavioural-economics parameters with evolutionary labels."** The test is equation (B.3): present-bias *β* is derived from ancestral mortality rates, with a numerical prediction (β ≈ 0.96/year for *H. sapiens*) that matches independent empirical estimates (Frederick, Loewenstein, O'Donoghue 2002). This is a *quantitative consistency check*, not a rebranding.

2. **"The derivations assume the evolutionary optimum is achieved."** Correct — they are *optimality* derivations. For species far from evolutionary optimum (e.g., recent introductions; fast-changing cultural environments), the predicted (θ, λ, β, ρ) will not match the ancestrally derived expressions. That is *exactly what Δ_ST measures*: the gap between predicted and actual. The derivation sets up the benchmark against which F1 is quantified.

3. **"You can't identify all four primitives in CFPS / CHARLS empirically."** True — the primary empirical strategy in the main text does not identify each primitive separately. It identifies Δ_ST as a composite and leaves the primitives-decomposition to Section 3 of the theoretical contribution. The derivations here justify *why* the main-text's composite metric is the natural unifying quantity across layers.

4. **"Hamilton (B.2) requires known *r̄*."** For human cases we use demographic estimates (*r̄* to spouse ≈ 0 unless consanguineous; *r̄* to child = 0.5; *r̄* to public good ≈ 0 for strangers; *r̄* to in-group ≈ 0.01–0.05 depending on endogamy). For animal cases, *r̄* is standard in behavioural ecology. Parametric sensitivity analysis for *r̄* ∈ [0, 0.5] is reported in Supplementary Figure S3 (sensitivity envelope accompanying this appendix).

---

## B.8 Bridge to empirical sections

The four derivations (B.1)–(B.4) each generate an empirical test. Main-text Propositions P1–P4 are the *joint* empirical test; the per-primitive tests are:

- **θ test (derived from B.1)**: Rural-urban sibling comparison in CFPS — siblings separated by urban vs rural exposure should show θ-heterogeneity predicted by signal-distribution difference. Operationalised in *Layer B urban PDE*.
- **λ test (derived from B.2)**: Bride-price heterogeneity by *r̄* to affected party — arranged vs love marriages should show λ gradient. Operationalised in *Layer B C4 彩礼 PDE*.
- **β test (derived from B.3)**: Present-bias estimate by extrinsic-mortality proxy (province-level violent-crime rate historical; father's age-at-death; HIV prevalence). From CFPS 2010–2022 time preference module + CHARLS. Operationalised in *cross-domain β calibration*, SI Appendix D.
- **ρ test (derived from B.4)**: Cultural *G^c_{τ,y}* estimation — correlation of parent and child attitudes toward 鸡娃, controlling for shared environment via cousin-pair design. Operationalised in *Layer B C2 鸡娃 × 双减 PDE*.

Each per-primitive test is **not in the main text**; they are SI corroborations that the composite Δ_ST finding is consistent with each primitive's derivation. This mirrors *Nature Human Behaviour*'s preference for a single headline metric with supplementary decomposition (e.g., Sommet et al. 2026 *Nature Human Behaviour* on relative-deprivation).

---

**End of Supplementary Appendix B.**

*Next to be drafted: SI Appendix C — case-by-case mapping of the 27 phenomenology-archive cases onto Layer 1 and Layer 2 parameters. Deferred until Layer A animal meta-synthesis (Task #35) returns with quantitative Δ_ST estimates.*

---

\newpage

# Supplementary Note 2 — §11 Framework refinements (v1 → v2) transparency log

## Response to construct limitations identified during Layer A–D evidence assembly

*(Replaces the "Stage 1 refinements 2026-04-17 addendum" in `sweet_trap_formal_model_v2.md`. This version removes the HARKing appearance flagged in the Red Team review of 2026-04-17 by dating, enumerating, and justifying each modification as a response to a specific limitation surfaced during empirical assembly — not as a post-hoc fit to observed results.)*

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

**v2 refinement (Eq. L1′).** We extend the model to a two-layer architecture: Layer 1 (replicator / Lande–Kirkpatrick coevolutionary dynamics) describes trait–preference covariance G_{τ,y} on the population scale; Layer 2 (behavioural-economic overlay) nests the v1 utility function as a limit case for human, within-lifetime cases. Crucially, (θ, λ, β, ρ) are **re-derived as emergent parameters of Layer 1**, not as axioms (see v2 §3.2, Table "Critical reinterpretation of v1 primitives"). This closes the "moth → peacock → human" narrative into one formal system.

**Why this is not HARKing.** The limitation was visible by inspection of Layer A's mechanism diversity (4 mechanism categories: `sensory_exploit`, `olds_milner`, `fisher_runaway`, `repro_survival_tradeoff`) before any specific coefficient estimate was produced. v1 could accommodate `olds_milner` and `sensory_exploit` via F4-blocked individual reward but could not produce the line-of-neutral-equilibria prediction required to explain `fisher_runaway` systems (A6, A13, A17, A19, A9). This is a structural under-specification — not a response to a numerical result.

---

## §11.2 Limitation 2: v1 had no cross-societal heterogeneity operator to predict Σ_ST magnitude differences across cultures

**What v1 did.** v1 predicted Σ_ST magnitude from Δ_ST × τ_F3 × feedback_blockade (Eq. Σ_ST in v2 §2). These components are in principle all individual- or system-level scalars.

**What the data showed.** Layer C P3 analyses (ISSP 17-wave × 25 countries + Hofstede 59-nation panel) revealed systematic between-society variation in Sweet Trap severity that a purely individual-level Σ_ST cannot explain. China (G^c_z = +1.892, rank 1/59) and the United States (G^c_z = −1.818, rank 55/59) differ massively in cultural-runaway susceptibility; the pattern maps onto published Hofstede dimensions (collectivism, power distance, long-term orientation).

**v2 refinement (G^c_{τ,y} cultural weighting function).** We add a cultural covariance amplifier G^c_i = z(PDI_i) + z(LTOWVS_i) − z(IDV_i) — an a priori additive index built from published Hofstede (2010), Schwartz (2006), Triandis (1995), and Gelfand (2011) dimensions. G^c enters Eq. L1′ only for the `cultural Fisher runaway` sub-class (C2, C4, C5, C13) and is neither defined nor applied for mismatch or engineered Sweet Traps.

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

*End of Supplementary Note 2. This version replaces the v1 addendum and eliminates HARKing surface characteristics by explicit date-stamped limitation → refinement mapping.*

---

\newpage

# Supplementary Note 3 — §11.7 Engineered Deception: extending the Engineered sub-class beyond algorithmic media

*(New section added in v2.1. Status: construct extension, not primary analysis. The two cases below are reported as positive classifier predictions on held-out phenomena that illustrate construct generalisation; they are not part of the 10-case discriminant-validity dev set and do not enter the κ calculation.)*

---

## §11.7.1 Why extend the Engineered sub-class?

v2 §11.3 introduced an Engineered / Mismatch distinction grounded in *mechanism architecture* — Engineered Sweet Traps target general-purpose reward circuitry with a signal that has no ancestral referent, whereas Mismatch Sweet Traps exploit a reward calibration that once tracked fitness. Within v2 the only worked Engineered case was **C12 short-video / algorithmic feed**: a variable-ratio intermittent-reinforcement schedule running on an Olds–Milner-type direct-reward bypass.

Two observations motivate extending the Engineered sub-class into a *family* with ≥ 2 members:

1. **A second distinct human phenomenon appears to share C12's Olds–Milner architecture but is engineered by a human rather than an algorithm.** If the same variable-ratio intermittent-reinforcement mechanism drives both algorithmic and human-engineered cases, that is additional evidence for mechanism-level universality across operators (machine vs human) within a single Engineered family.
2. **A second sub-family emerges on a different axis.** Certain large-scale fraud schemes satisfy F1 + F2 through *aggressive mimicry* — a perpetrator deploying an artificial signal that exploits an *ancestrally-calibrated* reward system (romance, wealth) in the victim. This shares F2 "aspirational endorsement" but shifts the engineering from "reinforcement schedule" to "deceptive signal fabrication."

We therefore promote the Engineered sub-class from single-case (C12) to a **family of two sub-sub-classes**:

| Sub-sub-class | Operator | Mechanism | Example |
|---|---|---|---|
| **Engineered Algorithmic** | Automated system | Variable-ratio Olds–Milner direct reward | C12 short-video / algorithmic feed |
| **Engineered Deception** | Human perpetrator | Aggressive mimicry of aspirational reward cue | Pig-butchering scam; PUA intermittent reinforcement |

Both share F1 + F2 and both qualify as Engineered under v2 §11.3 (no ancestral calibration for the *engineered* signal, by construction). The two sub-sub-classes differ in policy lever: Algorithmic requires *signal-format regulation* (recommender transparency, reinforcement-schedule disclosure); Deception requires *mimicry detection and interdiction* (financial-fraud monitoring, platform authentication).

---

## §11.7.2 Case 1 — Pig-butchering (杀猪盘): a financial-romantic aggressive-mimicry Sweet Trap

**Phenomenon.** Long-con financial-romantic fraud in which a perpetrator cultivates a manufactured romantic relationship online over weeks or months, then introduces a fraudulent cryptocurrency or foreign-exchange "investment opportunity" that progressively drains the victim's savings. The term "杀猪盘" ("pig-butchering") refers to the metaphor of fattening the victim (deepening trust and cumulative deposits) before the slaughter (final withdrawal and disappearance of the perpetrator).

**Scale.**

- **United States:** FBI Internet Crime Complaint Center (IC3) reported approximately USD 4.5 billion in confidence- / romance-fraud losses in 2023, with pig-butchering-style schemes accounting for the largest and fastest-growing category (FBI IC3 2023 Internet Crime Report).
- **China:** The Ministry of Public Security (公安部) reported that telecom and online fraud (电信网络诈骗) handled more than 437,000 criminal cases nationwide in 2023, with pig-butchering among the top loss-per-case categories; *Global Times* (2024-01) and Xinhua reporting cite multi-billion-RMB annual loss totals.
- **Global:** INTERPOL (2023) and UN Office on Drugs and Crime (2023) describe industrial-scale operations run from compounds in Southeast Asia, with labour obtained through human trafficking — a structural feature that multiplies the welfare cost.

**F1 — Reward–fitness decoupling.** F1 = 1.0. The engineered signal (perceived romantic partner + perceived high-return investment) activates two ancestrally-calibrated reward channels (pair-bonding; resource accumulation). Current cor(R_agent, F) is strongly negative — actual fitness outcome is savings destruction and often debt. Ancestral cor(R_agent, F) for the constituent signals (pair-bond formation under courtship; investment of effort in a trusted partner) was strictly positive. Δ_ST is large.

**F2 — Endorsement without coercion.** F2 = 1.0. The victim actively prefers the action (continued contact, incremental deposits) throughout the relationship up to the moment of realisation; there is no external compulsion. This is the critical F2 boundary for v2.1: *aspirational under deception is F2 = 1*, because the chooser's *internal* preference is the relevant criterion — the deception operates on the signal distribution seen by the chooser, not on the chooser's freedom to choose. This is distinct from:

- **C4 bride-price (彩礼)** — F2 fails because exposure is driven by kin / social-network compulsion, not individual endorsement under the perceived reward.
- **D3 996 overwork** — F2 fails because exposure is driven by employer lock-in, not endorsement.
- **Coerced trafficking victims within the pig-butchering operation** — F2 fails on the labour side (labourers), but succeeds on the victim side (investors). Pig-butchering is therefore a two-sided phenomenon with Sweet Trap architecture on the *victim* side only.

**F3 — Self-reinforcing equilibrium (severity modifier).** F3 = 1.0 at the individual level: each successful "deposit → apparent return" cycle strengthens the reward signal. At the population level, F3 is also present: perpetrator operations scale through platform evasion, and victim populations are replenished by new entrants as detection tools are developed.

**F4 — Absence of corrective feedback (severity modifier).** F4 = 0.5. Cost is realised in a single terminal event (not gradually), which in principle allows Bayesian updating — but only after the terminal event. During the pre-terminal phase, apparent positive feedback (simulated investment returns) *inverts* the sign of the corrective-feedback channel, making F4 effectively positive during the trap.

**Classifier score.** S = 2·F1 + 2·F2 + 1·F3 + 1·F4 = 2.0 + 2.0 + 1.0 + 0.5 = **5.5** > 4.0 → **Positive Sweet Trap** (Engineered Deception sub-sub-class).

**Animal homology — aggressive mimicry.** The mechanism is recognised in biology as *aggressive mimicry*: a predator deploys a signal calibrated to the prey's ancestrally-fit reward system (food, mate, nest site) to lure the prey into an attack. Canonical examples:

- **Anglerfish (琵琶鱼)** deploy an illicium with bioluminescent esca that mimics small prey, luring planktivores within strike range (Pietsch 2009, *Oceanographic Handbook of Deep-Sea Fishes*).
- **Photuris fireflies (致命拟态萤火虫)** mimic the flash codes of female *Photinus* fireflies to attract and consume *Photinus* males (Lloyd 1975, *Science* 187, 452–453).
- **Bolas spiders** (*Mastophora*) release chemical mimics of female moth pheromones to attract male moths within striking range (Eberhard 1977, *Science* 198, 1173–1175).

In all three cases the prey's reward architecture — evolved for a legitimate signal distribution (conspecific mate, conspecific prey) — is exploited by an engineered signal deployed by a different species. This is the animal homologue of pig-butchering's romantic-financial signal fabrication. The cross-species concordance strengthens the claim that Engineered Deception is not a human-specific category but a mechanism with a direct biological precedent.

---

## §11.7.3 Case 2 — PUA (Pick-up Artist) intermittent reinforcement: boundary case

*(Full PUA discussion — including Round 2 inter-coder disagreement on F2 and the "shared Olds–Milner schedule" analogical hypothesis — is deferred to **Supplementary Note 4** below, which reproduces SI §11.7b in full. The main-text §11.7 retains pig-butchering alone as the canonical Engineered-Deception exemplar, and replaces all PUA citations with a forward reference to Supplementary Note 4.)*

---

## §11.7.4 Construct-extension power and F2 strict-boundary statement

**Classifier evaluation on held-out cases.** The 10-case discriminant-validity matrix (§M8) defined the classifier and its threshold T > 4.0. Pig-butchering and PUA are **not** part of the 10-case set, so they do not enter the dev-set κ = 1.00 calculation. We report them as *prospective classifier predictions* on held-out phenomena:

| Case | F1 | F2 | F3 | F4 | S | Threshold | Predicted |
|---|---:|---:|---:|---:|---:|:---:|---|
| Pig-butchering | 1.0 | 1.0 | 1.0 | 0.5 | 5.5 | > 4.0 | Positive |
| PUA (Coder A, strict) | 1.0 | 0.5 | 1.0 | 0.5 | 4.5 | > 4.0 | Positive (borderline) |
| PUA (Coder B, canonical) | 1.0 | 1.0 | 1.0 | 0.5 | 5.5 | > 4.0 | Positive |

Both classify positive on the held-out set. This is not out-of-sample *validation* in the strict sense — we have no independent ground-truth labels beyond our own coding — but it demonstrates that the classifier's positive region is not a vacuous superset of the dev set.

**F2 strict-boundary statement.** Both cases clarify the F2 boundary:

> **F2 = 1 requires the chooser's *internal preference to act* to be activated by the perceived reward signal in the absence of *external* compulsion on the choice itself. Deception operates on the signal distribution seen by the chooser, not on the chooser's freedom to respond to that distribution; hence aspirational endorsement under deception is F2 = 1.**
>
> **Conversely, F2 = 0 when the choice itself is compelled by external structure (employer lock-in in D3 996; kin/social-network obligation in C4 bride-price; trafficking-enforced labour in the perpetrator-side compounds of pig-butchering), regardless of any reward activation.**
>
> **F2 = 0.5 is reserved for cases where initial endorsement is genuine but late-phase dependency narrows choice — notably trauma-bonded PUA targets. This midpoint is the *boundary of the construct*, not a mechanism invention: the trap has converted aspirational endorsement into something that approaches coercion.**

This strict-boundary statement is the v2.1 companion to the F2 treatment in §11.4 (F3/F4 demotion) and preserves the necessary-condition status of F2 without adding new degrees of freedom to the classifier.

---

## §11.7.5 Methods integration

**Methods §2.4 Construct application** (v2.1 edit). Where v2 §2.4 described the Engineered sub-class via C12 alone, v2.1 distinguishes:

- **Engineered Algorithmic:** operator is an automated recommender or reinforcement-learning system; mechanism is variable-ratio Olds–Milner direct reward; policy lever is signal-format regulation. v2 example: C12.
- **Engineered Deception:** operator is a human perpetrator; mechanism is either aggressive mimicry of an ancestrally-calibrated reward cue (pig-butchering; aligns with anglerfish, bolas spider, Photuris firefly animal homologues) or engineered intermittent reinforcement (PUA; aligns with the C12 variable-ratio schedule); policy lever is mimicry detection and interdiction. v2.1 qualitative examples: pig-butchering, PUA.

Both sub-sub-classes remain within the v2 F1 + F2 necessary-and-sufficient classification rule. No new features are introduced.

---

*End of Supplementary Note 3. Caveats: (i) the two v2.1 cases are qualitative extensions, not independently coded by a second rater beyond the blind-κ Round 2 audit reported in Supplementary Note 4; (ii) scale statistics are cited from secondary sources (FBI IC3 2023; China MPS 2023; INTERPOL 2023; UNODC 2023); (iii) animal-homology citations are non-exhaustive; a future registered replication could apply the classifier to ≥ 10 additional held-out cases to test generalisation formally.*

---

\newpage

# Supplementary Note 4 — §11.7b Extended Engineered Deception: Pickup Artist (PUA) as boundary case

*(Status: Supplementary Information. Downgraded from main-text §11.7 in v2.2 following Red Team v3 mini-round diagnosis. PUA is retained as a **boundary case** rather than a canonical Engineered-Deception exemplar because (a) inter-coder disagreement on F2 emerged in the Round 2 blind-κ audit (Coder B: F2 = 1.0; Coder A late refinement: F2 = 0.5), and (b) the "PUA shares Olds–Milner variable-ratio schedule with C12" claim is an **analogical hypothesis consistent with, but not directly tested by, current data**. The v2.2 main text retains pig-butchering alone as the Engineered-Deception main-text exemplar.)*

---

## §11.7b.1 Rationale for supplementary placement

v2.1 §11.7.3 presented PUA intermittent reinforcement as a second Engineered-Deception exemplar sharing C12 short-video's Olds–Milner variable-ratio architecture. Two post-v2.1 audit findings motivate the v2.2 downgrade to SI:

1. **Inter-coder disagreement on F2.** In the Round 2 blind-κ audit (`00-design/stage3/blind_kappa_round2.md`), Coder B coded PUA F2 = 1.0 per the canonical v2 construct definition ("active preference under perceived reward, no external compulsion on the choice itself"), while Coder A's late refinement (§11.7.4 strict-boundary statement) coded F2 = 0.5 to reflect late-phase trauma-bonded dependency. Both readings are defensible under v2, but the disagreement itself exposes a construct-boundary ambiguity — namely, whether late-phase trauma-bonding narrows F2 or constitutes a post-Sweet-Trap clinical condition outside the construct's scope. We do not resolve this ambiguity in v2.2 and flag PUA as a **boundary case** where two reasonable coders can reach S = 4.5 (below-threshold risk) or S = 5.5 (above-threshold).

2. **Rhetorical nature of the "shared Olds–Milner schedule" claim.** The v2.1 main-text formulation ("PUA and C12 share the same Olds–Milner variable-ratio schedule despite different operators") was flagged as a *rhetorical analogy* rather than an *empirical finding* by Red Team v3. The claim is plausible, consistent with behavioural-psychology and clinical literatures on intermittent reinforcement (Skinner; Stark 2007; Dutton & Painter 1993), but **not directly tested** in our data. Direct testing would require within-person behavioural experiments contrasting variable-ratio algorithmic stimuli against variable-ratio human stimuli on a common reward metric (e.g., preoccupation-index or attachment-intensity measurement). No such experiment is in the v2.2 evidence base. The v2.2 main text accordingly replaces the direct-equivalence claim with a softened analogical-hypothesis formulation (see main-text §11.7 and §11.7b.3 below).

---

## §11.7b.2 F1–F4 assignment for PUA (retained from v2.1 §11.7.3)

**Phenomenon.** A manipulation practice in which the perpetrator applies a scripted pattern of alternating affirmation and rejection (negging, orbiting, hot-and-cold) to induce intense romantic fixation in the target, often followed by emotional or material extraction. The technique is explicitly described in PUA training materials as "push-pull" or "cat-string theory" — labels that map onto the behavioural-psychology literature on variable-ratio intermittent reinforcement.

**Scale (qualitative).** Prevalence estimates are harder to quantify than pig-butchering because the phenomenon sits partly in legal grey area and partly in informal peer-driven practice. Indirect indicators:

- Multiple cohort studies of intimate-partner abuse report "intermittent reinforcement" as a core mechanism of coercive-control escalation (Stark 2007, *Coercive Control*; Hardy & Gilligan 2020, *J. Interpersonal Violence*).
- PUA-inspired manipulation is documented as a risk factor for trauma-bonding and PTSD in victims (Dutton & Painter 1993, *Violence & Victims* 8, 105–120; Carnes 2015, *Betrayal Bond*).
- Chinese-language analogues are documented under the terms "精神控制" and "情感操纵" in family-violence research and public-health surveys of young adults.

**F1 — Reward–fitness decoupling.** F1 = 1.0. The engineered intermittent schedule produces *higher* subjective reward signal (attachment intensity, preoccupation) than a stable positive relationship would — while current cor(R_agent, F) is strongly negative (documented adverse outcomes: depression, self-esteem degradation, trauma-bonding, economic loss). Ancestrally, intermittent partner-availability signals (legitimate uncertainty under mate-choice conditions) correlated positively with long-run reproductive outcomes for those who persisted through honest courtship — the signal is exploited here by engineering artificial intermittency.

**F2 — Endorsement without coercion.** **F2 = 0.5 (Coder A late refinement) or F2 = 1.0 (Coder B canonical v2).** Coder A's reasoning: repeated intermittent reinforcement can produce trauma-bonding with documented neuroendocrine correlates (Dutton & Painter 1993) that narrow the scope of "choice" in late-phase; the midpoint reflects this boundary-case status. Coder B's reasoning: the canonical v2 F2 definition scores *whether the target actively prefers continued engagement under the perceived reward signal in the absence of external compulsion on the choice itself* — this holds throughout the relationship by construction of the phenomenon, making F2 = 1.0 per the unmodified construct. **Neither coder is wrong under v2 as written; the disagreement is evidence that v2's F2 definition does not crisply handle late-phase dependency narrowing.** v2.2 retains this ambiguity rather than resolving it by construct modification, on the grounds that resolution would require post-hoc construct refinement tailored to a single case.

**F3 — Self-reinforcing equilibrium (severity modifier).** F3 = 1.0. Each intermittent positive cycle deepens the conditioned dopaminergic response. Well-characterised in both behavioural-psychology (Skinner) and clinical literature on abusive relationships (Stark 2007; Hardy & Gilligan 2020).

**F4 — Absence of corrective feedback (severity modifier).** F4 = 0.5. Cost is realised gradually (eroded self-esteem, social isolation) and often only after exit from the relationship. Information about what is happening is often available in principle (friends warn) but discounted by the reward architecture during the trap.

**Classifier score (two-coder reconciliation).**

- Coder A (strict F2 = 0.5): S = 2·1.0 + 2·0.5 + 1·1.0 + 1·0.5 = 4.5 (above T = 4.0, borderline positive)
- Coder B (canonical F2 = 1.0): S = 2·1.0 + 2·1.0 + 1·1.0 + 1·0.5 = 5.5 (clearly above threshold)

**Boundary-case status.** PUA's mean S across the two coders is 5.0 with disagreement of 1.0 unit on the S scale. This is the *largest* inter-coder disagreement in the Round 2 blind-κ audit and concentrates on a single feature (F2). Pig-butchering, by contrast, received S = 5.5 unanimously from both coders. On these grounds, v2.2 retains pig-butchering in the main text as the canonical Engineered-Deception exemplar and places PUA in SI with boundary-case labelling.

---

## §11.7b.3 Analogical hypothesis: does PUA share C12's Olds–Milner variable-ratio schedule?

The v2.1 main-text claim — "PUA and C12 short-video share the same Olds–Milner variable-ratio schedule despite different operators" — is an **analogical hypothesis consistent with but not directly tested by current data**. Three observations support the hypothesis:

1. **Mechanistic surface match.** PUA training materials explicitly describe the push-pull technique as "intermittent reinforcement" (e.g., Strauss 2005, *The Game*; Jeffries 2007), and the behavioural-psychology literature on variable-ratio schedules (Skinner 1938, 1953) is the direct operationalisation of that label.
2. **Clinical-trauma convergence.** Dutton & Painter (1993) and Carnes (2015) both identify intermittent reinforcement as the core conditioning mechanism in trauma-bonded abusive relationships, invoking the same operant-conditioning framework as the behavioural-psychology literature on variable-ratio algorithmic feeds (e.g., Eyal 2014, *Hooked*; Schüll 2012, *Addiction by Design*).
3. **Cross-operator invariance prediction.** If variable-ratio intermittent reinforcement is the causal kernel, then the operator (human vs algorithm) should be irrelevant to the outcome signature holding the reinforcement schedule constant. This is a testable prediction.

Three observations cut against the direct-equivalence claim:

1. **No within-person behavioural comparison exists.** To our knowledge no study contrasts PUA-style human-administered variable-ratio stimuli against algorithmically-administered variable-ratio stimuli on a common reward metric within the same participants. The claim is based on parallel mechanistic descriptions from two literatures, not on a direct comparison.
2. **Schedule parameters likely differ systematically.** Algorithmic feeds have schedule parameters (inter-reward interval, reward magnitude distribution) that can be empirically measured from platform telemetry; PUA schedules are scripted but variable across practitioners and targets. The *category* is the same (variable-ratio); the *parameters* may differ substantially.
3. **Downstream outcomes partially differ.** C12 short-video outcomes (in our Layer B headline) include subjective wellbeing decline; PUA outcomes (in clinical literature) centre on trauma-bonding, PTSD, and depression. The subjective-reward architecture is arguably shared; the downstream cost structure differs.

**v2.2 formulation.** We therefore state in the main text:

> *An analogical hypothesis — that PUA's intermittent reinforcement may share operant-conditioning architecture with algorithmically-curated feeds — is consistent with but not directly tested by current data; empirical test requires behavioural experiments (see Supplementary Note 4 Limitations).*

This formulation (i) preserves the scientific content of the v2.1 claim, (ii) classifies it explicitly as a hypothesis rather than a finding, and (iii) specifies the experimental design that would constitute a direct test.

---

## §11.7b.4 Future registered replication

We pre-specify a registered replication testing the cross-operator-invariance prediction:

- **Design.** Within-person counterbalanced exposure to variable-ratio schedules under two operator conditions (human confederate vs algorithmic simulation) with matched schedule parameters (inter-reward interval, reward magnitude distribution calibrated from published algorithmic-feed telemetry).
- **Primary outcome.** Preoccupation-index and attachment-intensity measurement 24 h and 7 d post-exposure, normalised to within-person baseline.
- **Falsifier.** If the human-operator condition produces systematically higher outcome than algorithmic-operator condition at matched schedule parameters (non-overlapping 95% CI on within-person difference), the "pure schedule-driven" account fails and at least one operator-specific channel must be invoked.

Submission of this replication design to OSF is pre-committed following main-manuscript acceptance; pre-registration DOI will be appended to the v2.2 Data and code availability statement at that stage.

---

## §11.7b.5 Relation to main-text §11.7

In the v2.2 main text, §11.7 Engineered Deception retains **pig-butchering (杀猪盘) only** as the canonical Engineered-Deception exemplar, with F1–F4 coding and animal-homology citations as in v2.1. All references to PUA in Methods and Discussion are replaced with forward references to this supplementary file. The softened analogical-hypothesis formulation quoted in §11.7b.3 is the text used in main-manuscript §11.7.

*End of Supplementary Note 4.*

---

\newpage

# Supplementary Note 5 — §11.8 Policy predictability as construct derivative

**Status:** v2.4 new section (2026-04-18). Inserted after §11.7 Engineered Deception in the framework-refinements series. Replaces v2.3's DALY-anchored "welfare stakes" framing in the construct's interpretive layer.

**Relation to main text:** Main-text §8 reports the empirical instantiation (six focal domains; construct-derived ranking of signal-redesign vs information intervention effect sizes). Main-text Discussion implication (1) restates the law at the policy-framing level. This Supplementary Note 5 documents the derivation — i.e., why the law follows from F1 + F2 *before* any empirical comparison — and pins down the scope condition and falsifiability rule.

---

## §11.8.1 Why F1 + F2 directly imply an intervention-asymmetry law

Recall (main text §1, §M1): the Sweet Trap classification is

- **F1 — Reward–fitness decoupling.** cor(R_agent, F)_current ≤ 0 ≪ cor(R_agent, F)_ancestral. The binding variable is not the agent's belief but the external signal distribution with which the reward system was calibrated.
- **F2 — Endorsement without coercion.** Pr(choose a | R_agent > 0, no coercion) > Pr(choose a | R_agent = 0, no coercion), under full information about downstream cost.

F2 is the pivotal condition for the policy implication. F2 states that the agent endorses the behaviour *even when* the fitness cost is known — i.e., endorsement is not contingent on the agent's belief about the cost. This is a definitional feature of the construct, not an empirical surprise: a phenomenon is not a Sweet Trap unless the endorsement survives the information being present.

A direct corollary follows. Consider the two canonical intervention classes:

- **Information interventions (belief channel):** nutrition labels, financial-literacy programmes, screen-time awareness campaigns, alcohol warning labels, fraud-victim awareness. These act on the agent's *cognitive representation* of the downstream cost — i.e., on the *belief* that the behaviour is harmful.
- **Signal-redesign interventions (F1 channel):** sugar taxes, auto-enrolment defaults, screen-time commitment devices, alcohol availability and price restrictions, LTV caps, platform cold-approach friction. These act on the *distributional properties* of the reward signal with which R_agent interacts — i.e., they modify F1 directly.

In Sweet Trap domains, F2 implies that the information channel is (by definition) not the binding constraint: the agent's endorsement does not require that the cost be unknown. Information interventions therefore operate on a variable whose change, under F2, cannot rescue the outcome. Signal-redesign interventions, by contrast, intervene on the channel (F1) that the construct definition identifies as binding.

**The derivation is construct-level, not empirical.** It does not depend on any particular intervention meta-analysis, or any assumption about the size of the effect. It predicts a *ranking*: within Sweet Trap domains, the expected magnitude of signal-redesign effects exceeds the expected magnitude of information effects on matched outcomes. The specific magnitudes are empirical questions, as is the specific factor by which one dominates the other in any given domain. What is *not* an empirical question — given the construct definition — is the direction of the ranking.

## §11.8.2 Scope condition: the law holds only in Sweet Trap domains

The law is domain-conditional. Two canonical failure conditions identify the boundary of the law's applicability:

### Failure of F1 (signal–fitness decoupling does not hold)

In domains where reward tracks fitness — i.e., cor(R_agent, F)_current > 0 — the F1 condition fails. Intervention design in such domains has nothing to gain from redesigning the reward signal (which is already well-calibrated); the behaviour-change problem is elsewhere. The construct makes no claim about intervention asymmetry in such domains, because they are not within its scope.

### Failure of F2 (endorsement depends on belief being wrong)

In domains where endorsement is contingent on the agent's *incorrect belief* about fitness — e.g., vaccine-hesitancy driven by misinformation about vaccine safety, or novel-risk domains where the individual's prior is simply wrong and correctable — F2 fails, because the endorsement is not robust to full information. In such domains, **information interventions target the binding variable**, and should therefore dominate signal-redesign interventions. The construct's policy-asymmetry law predicts, symmetrically, that in non-Sweet-Trap domains of this form, *information should dominate signal-redesign*.

Main text §8.3 operationalises this as a qualitative counter-example: the vaccine-hesitancy literature (Loomba et al. 2021, *Nat. Hum. Behav.*; narrative-correction RCTs) shows that information interventions produce measurable effects in this domain — the pattern that the §8.2 six-domain set does *not* show. This cross-domain asymmetry is the strongest form of construct-scope validation we can offer without a paired-design RCT: the prediction holds in F1 + F2 domains and inverts in domains where F2 fails by belief-correction.

## §11.8.3 Falsifiability and post-publication test

The §11.8 law generates a precise falsification condition.

**Falsification condition A (domain-level).** In any domain classified as a Sweet Trap by F1 + F2, if a replicated RCT or meta-analytic update shows that an information intervention produces an effect size at least equal to a matched-outcome signal-redesign intervention, with 95% CIs non-overlapping the null, the construct's policy-asymmetry implication fails in that domain. Two consequences follow: (i) the construct-classification of that domain is called into question (does it satisfy F2 as strongly as assumed? is belief actually the binding variable?), and (ii) the scope condition of the §11.8 law must be narrowed.

**Falsification condition B (cross-domain).** If, across a pre-specified portfolio of ≥ 5 focal Sweet Trap domains, the median within-domain ratio of signal-redesign to information effect sizes is not significantly greater than 1 (one-sided Wilcoxon test, α = 0.05), the construct's policy-asymmetry implication fails as a general law. The six-domain portfolio reported in main-text Fig. 5 and Supplementary Table S1 constitutes the first-round test of this condition.

**Replication caveats acknowledged.** The nudge-replication literature (notably DellaVigna & Linos 2022, *Econometrica*) has shown that some signal-redesign / default-style interventions exhibit substantial effect-size shrinkage at scale. This is a known risk for the §11.8 law: if the six-domain interventions compiled in main-text Fig. 5 are subject to similar shrinkage in future large-scale replications, the domain-level ranking may narrow. We treat this as a scope-refinement prediction: the §11.8 law should hold robustly in domains where F1 + F2 are both strong (high Δ_ST, high F2-aspirationality), and may weaken in borderline Sweet Trap domains (low Δ_ST, F2 = 0.5 boundary cases). The PUA boundary case in Supplementary Note 4 is precisely such a borderline: we do not expect the §11.8 law to hold strongly in the late-phase trauma-bonded PUA target population, where F2 approaches coercion-adjacent.

## §11.8.4 What §11.8 does *not* claim

Two clarifications to prevent over-reading.

**The law is not a general statement about nudges.** Signal redesign, as used here, is a construct-level term referring to interventions on the F1 signal distribution. It is not synonymous with "nudge": a nudge in the Thaler–Sunstein sense may or may not operate on F1, and some nudges (e.g., reminder-SMS campaigns) operate on the information / belief channel. The §11.8 law is about the F1 channel specifically, regardless of whether a given intervention is conventionally labelled "nudge", "regulation", "tax", or "choice architecture". Main-text §8 reports the six-domain instantiation with domain-appropriate labels.

**The law is not a ranking of political feasibility.** Signal-redesign interventions may be politically more expensive than information interventions (sugar taxes face more opposition than sugar-awareness campaigns; LTV caps face lobbying opposition; platform-friction regulations face platform lobbying). The §11.8 law is a statement about *expected effect size on the target behavioural outcome*, not about political cost–benefit. Translating the law into policy requires the additional input of intervention cost, opposition, and enforcement feasibility.

## §11.8.5 Link to the construct's main contribution

The §11.8 law is the final interpretive piece of the v2.4 refactor. Where v1 was structured around an F1–F4 classification, v2 collapsed to F1 + F2 necessary-and-sufficient (§11.4), and v2.1–2.3 added the A + D cross-level concordance (§6) and the Engineered Deception sub-class (§11.7), **v2.4 closes the construct-to-policy derivation**: from F1 + F2 at construct level, to a falsifiable intervention-asymmetry law at policy level, testable against the existing intervention-effect meta-analytic literature (main-text §8) and falsifiable at both the domain level and the cross-domain level (§11.8.3). This is the sense in which Sweet Trap is not a typology or umbrella but a construct with a derivative law of policy effectiveness — the sense in which the paper's title ("*a cross-species reward–fitness decoupling equilibrium and a derived law of intervention effectiveness*") should be read.

---

*End of Supplementary Note 5. Integrated into main-text Discussion §1 ("policy interventions that reshape the signal distribution dominate information interventions — and this is not a post-hoc observation but a construct derivative"). Referenced by main-text §8.1, §8.3, §8.4. Relation to v2.3 §8 DALY anchor: orthogonal; the DALY aggregate is retained as Supplementary Appendix H descriptive-scale observation, the §11.8 law is the primary policy-stakes contribution.*

---

\newpage

# Supplementary Appendix H — Orthogonal global-health implications

**Status (v2.4, 2026-04-18):** *Secondary orthogonal analysis; not a primary claim of the construct paper.*

This appendix explores the downstream global-health footprint of Sweet Trap mechanisms by linking the MR-identified chains of Layer D (main-text §5) to GBD 2021 disease totals via Levin's population-attributable-fraction formula. The analysis was the main-text §8 in manuscript v2.3 and is retained in the Supplementary Information in v2.4 as a secondary observation that a reader focused on public-health accounting may find useful. **The paper's primary contribution is theoretical (cross-species construct + F1 + F2 classifier + pre-registered A + D concordance + derived policy-predictability prediction in main-text §8 and Supplementary Note 5) rather than epidemiological.**

This framing matters. The construct paper does not claim the DALY figures below as an independent contribution; the figures re-aggregate GBD-attributed conditions that happen to overlap with the Sweet Trap domain set. Aggregating GBD totals for behaviours the construct already defines as Sweet Traps is circular if read as a "Sweet Trap causes X DALYs" attribution; it is non-circular only as a descriptive statement of *orthogonal scale* — i.e., "the MR-identified chains that survive construct-inclusion criteria map to exposure–disease pairs on the order of Parkinson's-disease burden globally." We report it that way.

---

## H.1 Methods: Levin PAF linkage to GBD 2021

**Formula.** Levin (1953) PAF = P_e (OR − 1) / [P_e (OR − 1) + 1]; attributable DALY = PAF × GBD-2021 disease total. Uncertainty envelope: 3 × 3 grid over (P_e, OR) 95% bounds; PAF_lo / PAF_hi are the min / max of the nine combinations.

**De-duplication.** Outcome aliasing (antidepressants → F5_DEPRESSIO pool; keep larger |PAF|). Shared outcome across different exposure families is retained (alcohol and smoking as independent GBD risk factors for K11_ALCOLIV). Protective chains (PAF < 0) are excluded from the harm sum.

**GBD 2021 baselines.** T2D 75.3 M DALYs/yr, alcoholic liver 14.2 M, depression 56.3 M (IHME GBD 2021, *Lancet* 2024 suite). Exposure prevalences: BMI ≥ 25 → 43% (NCD-RisC *Lancet* 2024); heavy drinkers ≈ 10% (WHO 2024); ever-smokers ≈ 22% (GBD 2021 Tobacco Collaborators); high risk-tolerance upper tail 20% (Falk et al. 2018 *QJE*).

**Pipeline.** `03-analysis/scripts/mortality_daly_anchor.py`.

---

## H.2 Conservative floor: Steiger-correct subset

Under the conservative inclusion criterion that retains only chains with Steiger directionality = ✓ (the standard primary filter in two-sample MR; Hemani, Tilling & Davey Smith 2017, *PLoS Genet.* 13: e1007081), one chain survives the filter at nominal α = 0.05 and the Levin-PAF is computable:

- risk tolerance → depression (via antidepressants): **4.1 M DALYs/yr globally** [1.0, 11.8]

This is approximately equivalent to the GBD-2021 annual global burden of Parkinson's disease (≈ 3 M DALYs/yr).

## H.3 Extended envelope: all 19 chains

Under the broader inclusion criterion that retains the full 19 chains with Steiger ✗ flagged but not excluded (on the grounds that Steiger ✗ at socially-stratified loci reflects shared molecular architecture rather than reverse causation; see main-text §M7.3), four de-duplicated chains contribute:

- BMI → type-2 diabetes: 23.6 M DALYs (68% of extended total)
- drinks-per-week → alcoholic liver cirrhosis: 4.3 M (12%)
- risk tolerance → depression (via antidepressants): 4.1 M (12%)
- smoking initiation → alcoholic liver cirrhosis: 2.5 M (7%)

**Extended total: 34.6 M DALYs/yr globally** [16.2, 64.1] — approximately 10 × the annual burden of Parkinson's disease, approximately half the burden of low back pain (≈ 66 M), and ≈ 1.2 % of the world's 2021 all-cause DALY total (≈ 2,830 M).

## H.4 Steiger directionality rationale

The 11/19 chains with Steiger ✗ are not evidence of reverse causation; they are a known property of the genetic architecture of socially-stratified behavioural exposures. The loci driving BMI (FTO, MC4R), alcohol consumption (ADH1B, ALDH2), and smoking initiation (CHRNA5) have *partially organ-specific direct molecular pathways* in addition to the behavioural channel. This produces R²_outcome ≈ R²_exposure mechanically, which flips the Steiger directionality test, *without* changing the direction of the causal pathway (Hemani 2017; Davies et al. 2019 *eLife*). A reverse-causal interpretation would require the outcome (e.g., type-2 diabetes) to be genetically upstream of BMI, which is biologically implausible for adult-onset diabetes and is contradicted by bidirectional MR (see Appendix F in the OSF deposit).

## H.5 Sensitivity

Primary floor 4.1 M; extended envelope 34.6 M [16.2, 64.1]; large-effect-only (OR ≥ 1.5) 30.4 M; prevalence ± 20% 29.3 – 39.4 M.

---

## H.6 Why this is retained only as secondary / orthogonal observation

**Scope-of-claim honesty.** The Sweet Trap v2.4 paper is a *construct paper*, not a *burden-estimation paper*. The construct is defined by F1 (reward–fitness decoupling) and F2 (endorsement without coercion). Domains were selected for this paper on construct grounds (C8, C11, C12, C13, D_alcohol are Sweet Traps; C2, C4, D3 are not). Aggregating the GBD totals of the Sweet Trap domains is therefore a re-labelling of pre-existing GBD attribution: the Sweet Trap construct does not claim *new* DALYs beyond those already captured by GBD 2021 risk factors.

What the construct *does* claim is a **new organising principle** explaining why these exposures persist against individual welfare, and a **falsifiable intervention prediction** (Supplementary Note 5): in domains satisfying F1 + F2, signal-redesign interventions structurally dominate information-based alternatives. This is the paper's primary contribution. The Appendix-H DALY aggregate is a descriptive, orthogonal statistic retained for readers who wish to situate the construct's footprint on the global-health accounting scale.

**Avoiding circular attribution.** If a reader reads the Appendix-H total as "Sweet Trap causes 4–35 M DALYs", the attribution is partially circular: the construct itself selects which exposures enter the sum. We therefore present the figures as: *the MR-identified Sweet Trap chains that survive Steiger-correct / extended inclusion criteria correspond to an annual global-health footprint of 4.1–34.6 M DALYs*, which is a descriptive scale statement rather than a causal attribution.

**Non-circular alternatives the main paper adopts.** The main paper's primary policy claim (main-text §8 and Supplementary Note 5) is derived from the construct definition (F1 + F2) *without* reference to GBD data: the construct directly predicts the asymmetry between signal-redesign and information-based interventions, and this prediction is testable against the existing intervention-effect meta-analytic literature (main-text Fig. 5). This is the non-circular form of the stakes claim.

---

## Supplementary Figure S7 — Dual-anchor DALY visualisation (retired from main-text figures)

**(a) Dual-anchor headline chart.** *Primary (left bar):* Steiger-correct floor 4.1 M DALYs/yr [1.0, 11.8] — retains only chain 1b (risk tolerance → antidepressants) under standard MR Steiger directionality filtering; approximately equivalent to the 2021 global burden of Parkinson's disease (≈ 3 M). *Extended (right bar):* full envelope 34.6 M DALYs/yr [16.2, 64.1] — all four de-duplicated MR chains under the broader inclusion rule (Steiger ✗ flagged but not excluded per Hemani 2017 for socially-stratified exposures): BMI → T2D 23.6 M (68%), drinks → alcoholic liver cirrhosis 4.3 M (12%), risk tolerance → antidepressants 4.1 M (12%), smoking → alcoholic liver 2.5 M (7%). ≈ 10× Parkinson's and ≈ half the burden of low back pain (≈ 66 M). Both anchors use Levin's (1953) PAF formula. **(b) Sensitivity panel:** primary floor 4.1 M; large-effect-only (OR ≥ 1.5) 30.4 M; prevalence ± 20% 29.3–39.4 M. **(c) Sankey flow (extended envelope):** exposures (BMI, alcohol, risk tolerance, smoking) → diseases (T2D, cirrhosis, depression, ancillary) → DALY category (cardiometabolic, hepatopancreatic, psychiatric).

Full reproducibility: `03-analysis/scripts/mortality_daly_anchor.py`; sensitivity table: `mortality_anchor_sensitivity.json`.

---

## H.7 References cited in this appendix

- IHME GBD 2021 Collaborators (2024). *Lancet* 403 suite.
- NCD-RisC (2024). *Lancet* 403, 1027–1050.
- WHO (2024). *Global status report on alcohol and health*.
- Falk, A., Becker, A., Dohmen, T., Enke, B., Huffman, D., & Sunde, U. (2018). *QJE* 133, 1645–1692.
- Hemani, G., Tilling, K., & Davey Smith, G. (2017). *PLoS Genet.* 13, e1007081.
- Davies, N. M., Hill, W. D., Anderson, E. L. et al. (2019). *eLife* 8, e43990.
- Levin, M. L. (1953). *Acta Unio Int. Contra Cancrum* 9, 531–541.

---

*End of Supplementary Appendix H. This appendix explores health burden as one downstream manifestation of Sweet Trap mechanisms; the paper's primary contribution is theoretical rather than epidemiological.*

---

\newpage

# Supplementary Note 6 — Extended Data items (narrative)

**Date:** 2026-04-18
**Rationale:** Because the v3.x refactor dissolves the v3.1 §2 Theory section into Introduction narrative, readers lose the tabular synopsis of axioms and theorems. ED Table 1 restores that synopsis in one page without affecting main-text word count. ED Fig. 1 is proposed but not required for initial submission; ED Fig. 2 describes the pre-registered minimal experimental paradigm for future P1 confirmatory test (Appendix G in v3.1 SI outline).

This file describes 1 ED Table (committed) + 2 ED Figures (optional; ED Fig. 1 strongly recommended for reviewer accessibility; ED Fig. 2 documents future work flagged in Discussion ¶3). The ED items are delivered to NHB separately from this SI PDF and are reproduced here in narrative form so that reviewers reading the SI alone can see the full structure.

---

## ED Table 1 — Axiom system A1–A4 and theorem set T1–T4 synopsis (committed)

**Panel A — Axioms**

| Axiom | Claim (narrative) | Formal core | Scope / route variations | Falsification criterion |
|---|---|---|---|---|
| **A1 Ancestral Calibration** | Reward evolved because it tracked fitness in the ancestral signal distribution. | ∃ monotone *h*: *U*_perc = *h*(*U*_fit) + *ε* on *S*_anc, *σ*²_cal ≪ Var[*U*_fit]. | Applies to any agent with a reward-evaluation circuit; vertebrates + most invertebrates (dopaminergic RPE documented). | Find a taxon whose *U*_perc ranking contradicts *U*_fit ranking within *S*_anc (no known case). |
| **A2 Environmental Decoupling** | Novel signals outside the ancestral distribution no longer track fitness. | ∃ *t*_sep, *ρ*_crit ∈ (0, 1): *ρ*(*s*, *t*) < *ρ*_crit for *s* ∈ *S*_mod \ *S*_anc. | Route A: mismatch (environment shifts faster than calibration). Route B: supernormal / novel (Olds–Milner, variable ratio, algorithmic feeds). | Identify an *s* ∈ *S*_mod \ *S*_anc with *ρ* ≥ *ρ*_crit across the *ψ_i* distribution. |
| **A3 Endorsement Inertia** (scope-defining) | Within a specified scope, agents continue to endorse signals even when they know better. | A3.0 scope: post-info abandonment < 30% OR revealed *w* < 0.45. Within scope: *b_i* = argmax[(1 − *w_i*)*U*_perc + *w_i* 𝔼[*U*_fit]], *w_i* ≤ *w*_max < ½ (default 0.4). | Agents outside A3.0 scope (e.g., informed professional investors with *w* > 0.45) are **not Sweet Trap cases**; A3 makes no claim about them. This resolves the "any phenomenon fits" tautology concern (Stage 1-B F2). | Information interventions achieving > 70% abandonment in candidate Sweet Trap domains (observed: 5–15%). |
| **A4 Partial Cost Visibility + P1** | Fitness costs are gated by visibility and discounted by a decreasing function of horizon. | Observable cost *c_i*·*I*_visible; effective cost *δ*(*τ*)·*c_i*, *δ*(0) = 1, *δ*′ < 0 (axiomatic core). Default P1: *δ*(*τ*) = 1/(1 + *k_i τ*) hyperbolic. | Core (*δ*′ < 0) is universal; P1 is a parameterisation. Exponential or Laibson *β*-*δ* preserve theorem directions with modified constants. | A domain where observed intertemporal cost treatment violates *δ*′ < 0 (no known case). |

**Panel B — Theorems**

| Theorem | Key inequality | Proof technique | Scope where it holds | Anchor |
|---|---|---|---|---|
| **T1 Sweet Trap Stability** | ‖*s_i*(*t*) − *s\**‖² ≤ *C*·‖*s_i*(*t*_0) − *s\**‖²·*e*^{−*c*(*t*−*t*_0)}, *c* ≥ *α ℓ ε*² − *β δ*_max *M* − *D*^drift | Jacobian negativity + Lyapunov function + basin Taylor expansion | Persistent Δ_ST ≥ *ε* > 0; bounded cost gradient; A3.0 scope | Allcott 2020 *AER* post-deactivation return; Mozaffarian 2016 *Circulation* |
| **T2 Intervention Asymmetry (core)** | \|Δ*b*_signal\| / \|Δ*b*_info\| ≥ (1 − *w*_max)/*w*_max ≥ 1.5 for *w*_max ≤ 0.4 | Argmax sensitivity on *Ũ_i* = (1−*w*)*U*_perc + *w*·𝔼[*U*_fit]; A3.3 bound on *w* | Dose-matched operational convention (T2.1.1); non-saturated regime *σ*′ ≥ *σ*′_min > 0; symmetric field shrinkage *κ*_signal ≈ *κ*_info | DellaVigna–Linos 2022 *Econometrica*; Mertens et al. 2022 *PNAS* |
| **T3 Cross-Species Universality** | A1–A4 are species-neutral ⟹ Sweet Trap applies to any agent with (i) reward calibration, (ii) signal-space separability via *φ*, (iii) environmental change exposure | Constructive invariance: each axiom's primitives verified species-neutral; moth + human worked examples | Magnitude rank preservation (empirical olds > sensory > fisher) requires additional *ψ*-commensurability premise → reported as empirical regularity, not theorem-derived (Stage 1-B M4) | Layer A (20 animal cases); Layer D (19 MR chains); Olds & Milner 1954 |
| **T4 Engineered Escalation** | Δ_ST^EST ≥ Δ_ST^MST; decay rate *c*^EST ≥ *c*^MST (*basin radius* demoted to Observation 4.1) | Envelope theorem (Milgrom–Segal 2002 *Econometrica*) on the designer's optimisation max_{s_design} Σ_i Δ_ST·ω_j | Designer's objective aligns with Δ_ST; *S*_design strictly larger than passive shift set | C12 short-video (Allcott 2020); gambling (Dow-Schüll 2012); engineered-deception pig-butchering |

**Panel C — Sub-classes**

| Sub-class | Generating mechanism | Empirical domains | Dynamics |
|---|---|---|---|
| **MST (Mismatch)** | Passive environmental shift (no designer); *ψ* calibrated ancestrally | Diet (C11); light pollution (moths); monarch tropical milkweed | Δ_ST fixed by environmental shift; decay rate *c* from T1 |
| **RST (Runaway)** | Culturally-transmitted *ψ* with self-referential covariance | Luxury consumption; dowry; status signalling (Layer C Hofstede patterns) | *W̄*_perc-based Lande–Kirkpatrick dynamics (Lemma L4.1) drive indefinite escalation |
| **EST (Engineered)** | External designer *j* optimises *φ* to maximise Σ_i Δ_ST·ω_j | C12 short-video (algorithmic); Olds–Milner self-stim (lab); slot machines; pig-butchering / PUA | T4: Δ_ST^EST ≥ Δ_ST^MST; *c*^EST ≥ *c*^MST |

---

## ED Fig. 1 — Axiom system dependency diagram (recommended, optional for initial submission)

**Purpose:** visually depict (i) the four axioms as nodes, (ii) their dependencies (A4 requires A1 primitives; A3 uses A4 cost-visibility; T1 depends on A1+A2+A3+A4; T2 depends on A3.0 + non-saturation scope; T3 depends on A1–A4 species-neutrality; T4 depends on T1 + envelope), (iii) the three sub-classes MST/RST/EST as downstream nodes.

**Suggested layout:** top row = A1 A2 A3 A4; middle row = T1 T2 T3 T4 with edges to axioms; bottom row = MST RST EST with edges to relevant theorems. Falsification criteria as callout labels.

**Status:** **recommended, not committed**. If reviewers find the narrative-only axiom exposition in Introduction inadequate, this figure would restore the structural view. Can be generated via `04-figures/extended/ed_fig1_axiom_diagram.R` at revision stage; not required for initial submission.

---

## ED Fig. 2 — Minimal pre-registered 3-arm factorial experimental paradigm (future work)

**Purpose:** document the minimal RCT design that could refute T2 in a single controlled study under the operational dose-matching convention (T2.1.1).

**Design:** 3-arm between-subjects; *n* = 400 per arm (total 1,200) via Prolific.

- **Arm 1 (Info, dose-calibrated):** participants receive disclosure information calibrated (in a pre-RCT pilot) to shift 𝔼[*U*_fit | *B*] by Δ*U*.
- **Arm 2 (Signal-redesign, dose-matched):** participants face a choice environment where *φ* is modified to shift *U*_perc directly by the same Δ*U*.
- **Arm 3 (Control):** no intervention.

**Primary outcome:** |Δ*b*_signal|/|Δ*b*_info| ratio in the target choice-domain task (e.g., short-video scrolling duration; high-LTV mortgage preference; SSB purchase).

**Pre-registered decision rule:** ratio ≥ 1.5 with 95% lower CL > 1.0 supports T2 prediction P1. Ratio < 1.0 refutes T2 (strong falsification). Ratio in [1.0, 1.5] with CL crossing 1.5 is inconclusive.

**Status:** **flagged future work in Discussion ¶3.** Not required for this submission. OSF-registered protocol at `paper1-theory/04-empirics/minimal_experimental_paradigm.md`.

---

## Items committed for initial submission

| Item | Status | Target location |
|---|---|---|
| ED Table 1 | **committed** | Submission file bundle (2-page PDF) |
| ED Fig. 1 | recommended optional | Would supplement ED Table 1; create at revision if requested |
| ED Fig. 2 | future-work reference only | Referenced in Discussion ¶3 + Methods §M6 |

**Total ED items at submission:** 1 (well below NHB Article ED ceiling of 10).

---

\newpage

# Supplementary Note 7 — Expanded figure legends for main-text Fig. 1–6

**Target journal:** Nature Human Behaviour (Article)
**Style:** Bold title sentence; one-sentence core message; panel descriptions; statistical details sufficient to interpret without main text.
**Generation:** R 4.3+, Paul Tol colorblind-safe palette throughout. Figures rendered at 180 mm width, 300 DPI PNG + cairo_pdf vector.
**v3.1 changes:** 9 → 6 figures per NHB Article limit. Old Fig 1 (8-case animal forest) + old Fig 2 (Layer B panels) → new Fig. 1 (20-case phylogenetic dot strip + mechanism subgroup + pooled summary). Old Fig 3 → new Fig. 2. Old Fig 4 → new Fig. 4 (unchanged). Old Fig 6 → new Fig. 5. Old Fig 7 → new Fig. 3. Old Fig 8 (intervention) + old Fig 9 (cross-level meta) → new Fig. 6. Old Figs 1, 2, 5, 8/9 originals retained in `04-figures/supp/`.
**v3.2 renumber (B1 fix):** Figures reordered to match first-citation sequence in main text. Old Fig 3 (spec-curve) → Fig. 2; old Fig 2 (ISSP) → Fig. 3; old Fig 5 (MR) → Fig. 4; old Fig 6 (theory tests) → Fig. 5; old Fig 4 (discriminant) → Fig. 6.

---

## Main-text Fig. 1 | Animal Sweet Traps span six phylogenetic classes and show a consistent mechanism-dependent reward–fitness decoupling gradient.

**Core message:** Δ_ST > 0 is documented across 20 cases from 6 phylogenetic classes (mammals to crustaceans), with effect magnitude highest in direct neural-reward hijacking (Olds–Milner) and lowest in life-history trade-off cases. **(a)** Phylogenetic dot-strip: 20 confirmed animal Sweet Trap cases plotted by taxon class (background bands, Paul Tol 8-colour palette), with point shape encoding mechanism category (circle = Olds–Milner / ICSS; triangle = sensory exploit; square = Fisher runaway; diamond = reproduction–survival trade-off) and horizontal extent showing Δ_ST ± 95% CI. Cases ordered within class by Δ_ST (descending). **(b)** Mechanism-subgroup forest plot (random-effects, restricted maximum likelihood): Olds–Milner 0.789 [0.620, 0.959], k = 7; sensory exploit 0.653 [0.560, 0.745], k = 5; Fisher runaway 0.547 [0.430, 0.664], k = 5; reproduction–survival 0.470 [0.357, 0.583], k = 3. Olds–Milner vs. Fisher runaway: Δ = +0.242, p = 0.001 (Wald test). I² = 85.4% (high heterogeneity driven by mechanism class). **(c)** Pooled summary across all 20 cases: diamond at Δ_ST = 0.645 [0.557, 0.733] with 95% prediction interval [0.228, 1.062] (outer segment); dashed null line at 0. Source data: `02-data/processed/layer_a_animal_cases.csv`; figure script: `04-figures/main/fig1_animal_phylogeny_meta.R` (v3.1). [≈ 220 words]

---

## Main-text Fig. 2 | Specification-curve analysis across 3,000 model specifications confirms Sweet Trap effects in four of five focal domains, with C12 short-video explicitly downgraded.

**Core message:** Consistent direction and significance across exhaustive specification space supports P2 (domain generalisability), while transparent reporting of C12's fragility guards against inflation. Five-panel composite of specification-curve analyses for C8 investment FOMO, C11 diet (SSB), C12 short-video, C13 housing leverage, and D_alcohol. Each panel shows all specifications sorted by β estimate with 95% CI shaded. Total: 3,000 specifications (C8 = 240, C11 = 672, C12 = 576, C13 = 1,152, D_alcohol = 360), exceeding Sommet et al. (2026, *Nature*) benchmark of 768.

Median β on the narrow focal family with 2,000-bootstrap 95% CI on the median:

- **D_alcohol:** +0.134 [+0.121, +0.215]; sign stability = 96.3%; significance rate = 92.6%. **Most robust.**
- **C13 housing:** +0.243 [+0.183, +0.323]; sign stability = 100.0%; significance rate = 75.0%. **Robust.**
- **C8 investment:** −0.077 [−0.089, −0.049]; sign stability = 82.6%; significance rate = 78.3%. **Robust.**
- **C11 diet:** −0.024 [−0.031, −0.022]; sign stability = 91.7%; significance rate = 25.0%. **Direction-robust; power-limited.**
- **C12 short-video:** −0.003 [−0.039, +0.004]; sign stability = 62.5%; significance rate = 0.0%. **FRAGILE** (CFPS `internet` is binary; C12 is treated as directional evidence only).

Vertical dashed line in each panel marks the headline β from the primary analysis. Source: `03-analysis/spec-curve/spec_curve_all_summary.csv`; figure: `04-figures/main/fig2_spec_curve_5panel.png`. [≈ 240 words]

---

## Main-text Fig. 3 | Cross-cultural universality: aspirational-attitude velocity from ISSP 1985–2022 (n = 2.9 M individuals, 25 countries) predicts country-level Sweet Trap severity.

**Core message:** Countries where aspirational attitudes accelerated faster toward high-consumption ideals show higher observed Sweet Trap severity, consistent with the cultural-runaway (Fisher G_{τ,y}) amplification pathway. **(a)** Scatter of country-level Σ_ST against ISSP signed aspirational velocity Δ*z* (1985→2022), n = 25. Primary specification (joint-predictor model): β_{Δz} = −0.732 [−1.42, −0.05], HC3 robust SE, p = 0.036; β_{log τ_env_internet} = −0.742 [−1.46, −0.03], p = 0.042; adjusted R² = 0.255. Countries coloured by world region (Paul Tol 7-colour). China (solid circle) sits at the 95th percentile of signed aspirational velocity and 92nd percentile of aspirational level. **(b)** Country cultural coefficient G^c_z (Hofstede PDI + LTOWVS − IDV composite; 59 countries) against raw Σ_ST; Spearman ρ = 0.981 on 201-country sensitivity run; ΔR² from G^c-weighting = +0.0009. **(c)** Peak-and-retreat pattern in ISSP velocity: highest-Σ_ST countries (JP, US, NZ) show negative Δ*z* (past their aspirational peak); mid-Σ_ST countries (DK, CH, GB, DE) still climbing. Source data: `02-data/processed/issp_cross_cultural_velocity.csv`; figure script: `04-figures/main/fig3_issp_cross_cultural.R`. [≈ 200 words]

---

## Main-text Fig. 4 | Mendelian-randomisation forest (19 chains): Sweet Trap signatures reflect causal genetic architecture across three sub-classes.

**Core message:** Genetically-instrumented exposures in Sweet Trap domains (risk tolerance, BMI, alcohol intake, smoking) causally predict downstream welfare harms, with informative null MR chains providing discriminant evidence. Forest plot of two-sample MR IVW-random estimates for 19 chains. Three validated sub-classes: **Engineered** (blue): risk tolerance → depression OR = 1.38, → antidepressant use OR = 1.40, → anxiety OR = 1.63. **Ancestral-mismatch / alcohol** (orange): drinks-per-week → alcoholic liver cirrhosis OR = 5.41 [2.76, 10.57], → chronic pancreatitis OR = 3.80 [1.89, 7.63]; smoking → alcoholic liver OR = 1.96 [1.68, 2.29]. **Ancestral-mismatch / metabolic** (teal): BMI → T2D OR = 2.06 [1.60, 2.65], → diabetic nephropathy OR = 1.23 [1.03, 1.47], → stroke OR = 1.14 [1.04, 1.25]. **Informative nulls** (grey, triangles): drinks → stroke OR = 1.08 [0.90, 1.29], p = 0.40; drinks → hepatocellular Ca OR = 0.80 [0.29, 2.21], p = 0.67; risk tolerance → diabetic nephropathy OR = 0.93 [0.58, 1.50], p = 0.76. **Discriminant-protective** (purple): years of schooling → depression OR = 0.88; SWB → depression OR = 0.46. Pleiotropy: MR-PRESSO p > 0.25 for all 17 evaluable chains; Egger intercept p > 0.10 for 18/19 chains. Full data: `02-data/processed/mr_results_all_chains_v2.csv`; script: `04-figures/main/fig4_mr_layer_D.R`. [≈ 250 words]

---

## Main-text Fig. 5 | Theory tests: animal mechanism rank predicts human genetic-causal rank (pre-registered β = +1.58; T2 theorem confirmed; median signal-redesign advantage = 11×).

**Core message:** Two theory-level predictions are jointly confirmed: (P5) the mechanism hierarchy observed in animal Sweet Traps predicts the same hierarchy in human MR chains; (T2) signal-redesign interventions dominate information-based alternatives in every Sweet Trap domain tested. **(a)** Cross-level A+D joint meta-regression: Layer A (animal Δ_ST, circles, blue) and Layer D (human MR |log OR|, triangles, orange) plotted by mechanism class (Fisher runaway → Sensory exploit → Olds–Milner). Dashed linear trend lines per layer; pre-registered β = +1.58 [z-scored], p = 0.019 (A+D joint, highlighted). Primary three-layer model: χ²(2) = 1.51, p = 0.47 (non-significant; shown in grey italic; A+D pre-registered as primary per §6.3). **(b)** Intervention asymmetry forest (T2 theorem, P1): signal-redesign (filled domain-colour circles) vs. information (open grey circles) across six Sweet Trap domains (C8, C11, C12, C13, D_alcohol, C_pig-butchering†) on a domain-normalised scale (signal-redesign ≡ 1.0). In all six domains the signal-redesign point estimate exceeds the information estimate. †C_pig-butchering uses emerging-evidence CIs (dashed line). **(c)** Within-domain ratio (signal redesign ÷ information) on log-scale x-axis. All six ratios exceed 1; five of six exceed 3 (shaded region). Median ratio = 11×. **Scope condition:** the T2 theorem is claimed only for Sweet Trap domains (F1 ≥ 0.5 AND F2 ≥ 0.5); this does not generalise to non-Sweet-Trap contexts. Source data: `02-data/processed/intervention_asymmetry_table.csv`, `cross_level_effects_table.csv`; script: `04-figures/main/fig5_theory_tests.R` (v3.1). [≈ 280 words]

---

## Main-text Fig. 6 | Discriminant validity: F1 + F2 correctly classifies 10 adversarial cases (accuracy = 1.00, Cohen's κ pending).

**Core message:** The two necessary conditions (reward–fitness decoupling F1 ≥ 0.5; endorsement without coercion F2 ≥ 0.5) distinguish confirmed Sweet Traps from structurally similar but excluded behaviours across five positive and five negative controls. **(a)** Feature heat-map for 10 adversarial cases: 5 positive controls (C8, C11, C12, C13, D_alcohol Type A) and 5 negative controls (C2 intensive parenting, C4 bride-price, D3 996 overwork, C1 staple food, C16 vaccination). Cells coded 0 / 0.5 / 1 (colour scale: white–blue–dark blue). **(b)** Weighted score S = 2·F1 + 2·F2 + 1·F3 + 1·F4; classification threshold T > 4.0 gives accuracy = 1.00, sensitivity = 1.00, specificity = 1.00. Minimum positive score = 4.5 (D_alcohol Type A); maximum negative score = 2.5 (C1 staple food); separation margin = 2.0 on 0–6 scale. **(c)** Alternative binary rule "F1 ≥ 0.5 AND F2 ≥ 0.5" achieves identical accuracy, confirming F3/F4 are severity modifiers (not required for classification). **(d)** Out-of-sample marginal case C6 (health supplements, S = 4.5) sits at the classification boundary. *Caveats:* dev-set evaluation only (n = 10); blind second-coder κ is pending for revision round 1. Full provenance: `02-data/processed/discriminant_validity_features.csv`; script: `04-figures/main/fig6_discriminant_dashboard.R`. [≈ 240 words]

---

*Legends version: v3.1 (renumbered v3.2 B1-fix), 2026-04-18. Consolidates from v2.4 (9 figures) to 6 figures per NHB Article maximum. Fig. order revised to match first-citation sequence in main text: Fig. 1 = animal phylogeny (unchanged); Fig. 2 = spec-curve (was Fig 3); Fig. 3 = ISSP cross-cultural (was Fig 2); Fig. 4 = MR forest (was Fig 5); Fig. 5 = theory tests (was Fig 6); Fig. 6 = discriminant dashboard (was Fig 4). All source data and scripts remain available at project root and at OSF <https://osf.io/ucxv7/>.*

---

\newpage

# End of Supplementary Information v3.3

**Document version:** SI v3.3 (2026-04-18)
**Linked manuscript:** `main_v3.3_submission` (Nature Human Behaviour Article submission)
**OSF deposit:** <https://osf.io/ucxv7/>
**Corresponding author:** Hongyang Xi

All source files referenced in this SI are available in the OSF deposit above and in the project GitHub repository `sweet-trap-multidomain`.
