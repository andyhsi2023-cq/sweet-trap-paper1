# Axioms and Formalism — Sweet Trap Theory

**Paper**: Sweet Trap — Paper 1, Theoretical Foundation
**Document**: Mathematical foundation (Phase A)
**Status**: v1.0, 2026-04-18
**Authors**: Lu An & Hongyang Xi
**Target level**: Kahneman-Tversky 1979 (Prospect Theory) mathematical rigour. Reviewers (economist, evolutionary biologist, behavioural-science theorist) should be able to prove theorems on this basis without supplementary clarification.

**Companion files**:
- `nomenclature.md` — complete symbol table with types and domains.
- `relationship_to_existing_models.md` — formal comparison to Prospect Theory, Rational Addiction, Evolutionary Mismatch, Fisher Runaway, Zahavi Handicap.

**Upstream constraints**:
- `00-design/sweet_trap_formal_model_v2.md` §1 (F1–F4 feature system), §2 (Δ_ST definition), §11 (empirical refinements).
- `00-design/pde/discriminant_validity_v2.md` (F1+F2 necessary-and-sufficient on 10 positive/negative controls; F3 + F4 demoted to severity modifiers).
- `00-design/stage4/benchmark_construct_vs_daly.md` (theoretical framing must anchor "policy predictability + evolutionary inevitability", not DALY).

---

## §1 Primitives

### 1.1 Choice space

Let *S* be a measurable space — the **choice space** of admissible actions, states, or signal exposures. No structural assumption beyond measurability is imposed; *S* may be:

- **Discrete** (e.g., *S* = {invest, abstain}; *S* = {n cups of sugar-sweetened beverage per day, *n* ∈ {0, 1, 2, 3}});
- **Continuous** (e.g., *S* = ℝ₊ for daily screen-time minutes; *S* = ℝ_+^3 for a vector of engagements);
- **Symbolic / combinatorial** (e.g., *S* = {all possible consumer goods in a culture}).

A distinguished element *s*_0 ∈ *S* denotes **abstention** (no engagement, baseline). Define *S*^* = *S* \ {*s*_0} as the set of non-trivial choices.

**Modeling commitment (MC-1)**: We do **not** assume convexity, differentiability, or ordering on *S*. Continuous-time dynamics in §5 presuppose *S* ⊂ ℝ^*d* for some *d*; for purely discrete cases (e.g., moth species in A1), those dynamics reduce to a jump process on a graph — see §5.3.

### 1.2 Agents and time

Agents indexed *i* ∈ *I* = {1, …, *N*} (finite) or ℕ (population limit). Time *t* ∈ ℝ_+ (continuous) or *t* ∈ ℤ_+ (discrete panel). We use continuous time in §5 dynamics; empirical predictions in Paper 1 §03-predictions/ translate to discrete panel regression via the Euler scheme. A **time lag** τ ≥ 0 is a separate scalar (distinct from v2's trait variable *τ*, now renamed *q*).

### 1.3 Signal and fitness spaces

- **Signal feature space** Φ ⊆ ℝ^*k*. The **signal feature extractor** is a measurable map φ: *S* × ℝ_+ → Φ. φ(*s*, *t*) is the vector of perceptual features the agent's sensory apparatus extracts when exposed to *s* at time *t*. The time argument on φ is essential: it carries the environmental shift (novel signals, supernormal stimuli appear in Φ at time ≥ *t*_sep).

- **Fitness outcome space** Ω_fit ⊆ ℝ^*m*. For animals, Ω_fit is {survival, reproduction}; for humans, Ω_fit is the multidimensional objective-welfare space (health, wealth, mental health, relational capital) which is projected to a scalar via the consumption-equivalent utility *W*(*s*, *t*).

- **Instantaneous fitness-contribution function** *W*: *S* × ℝ_+ → ℝ. *W* is allowed to be negative (harmful choice accrues negative fitness).

### 1.4 State variables — complete list

| Variable | Type | Level | Time-invariant on …? |
|:---:|:---|:---|:---|
| *s_i*(*t*) | *S*-valued | agent-*i*, time-*t* | — (the dynamic quantity) |
| *ψ_i* | vector in Ψ ⊆ ℝ^*p* | agent-*i* | behavioural timescale (years); varies across generations |
| *α_i*, *β_i*, *k_i*, *w_i*, *κ_i*, *λ_i* | scalar | agent-*i* | behavioural lifetime |
| *B_i*(*t*) | distribution on Ω_fit | agent-*i*, time-*t* | — |
| *S*_hist(*t*) | distribution on *S* | population, time-*t* | slowly-varying |
| *π_t*(*s*) | scalar in [0, 1] | population | — |

Agent state is (*s_i*, *ψ_i*, *B_i*). Environmental state is (*S*_hist, Φ, *W*). Coupling *ρ*(*t*) is a population-level diagnostic computed from these.

---

## §2 Dual utility functions

The **central formal commitment** of Sweet Trap theory is that every agent is characterised by **two** utility functions over the same choice space, and their **divergence** is the object of interest.

### 2.1 Perceived utility *U*_perc

**Axiomatic commitment (MC-2)**: The perceived utility takes the form

$$
\boxed{\;U_{\text{perc}}(s, t \mid \psi_i) \;=\; \sigma\!\Bigl( \alpha_i \cdot \langle \psi_i, \varphi(s, t) \rangle \Bigr)\;}
\qquad (2.1)
$$

where:
- *σ*: ℝ → (0, 1) is the **logistic sigmoidal** transform *σ*(*x*) = 1/(1 + exp(−*x*));
- ⟨·,·⟩ is the Euclidean inner product on *Φ* ≅ ℝ^*k*;
- *α_i* > 0 is agent *i*'s **reward sensitivity**;
- *ψ_i* ∈ ℝ^*k* is agent *i*'s **reward calibration parameter vector**.

**Justification of sigmoidal form (MC-2a)**: The logistic form is committed (not ad-hoc) because:
1. **Saturation**: reward circuits in all animals studied (Schultz 2016 *Physiol Rev*; Berridge & Robinson 2016 *Am Psychol*) exhibit bounded firing rates. A sigmoidal captures saturation without additional parameters.
2. **Exponential-family conjugacy**: logistic regression is the unique discriminator consistent with independent ψ-features; allows analytic derivation of Δ_ST in regime where agent's feature projection ⟨ψ, φ⟩ is small (linearisation: *U*_perc ≈ ½ + ¼·*α*·⟨*ψ*, *φ*⟩).
3. **Empirical anchor**: dopamine prediction-error encoding fits logistic over 3-log decades of reward magnitude (Tobler, Fiorillo & Schultz 2005 *Science* 307:1642–1645).

**Falsifiability of MC-2**: If reward-fMRI or single-unit data in a given domain show non-monotonic *U*_perc with respect to ⟨*ψ*, *φ*⟩ (e.g., an inverted-U), MC-2 fails. The theory can accommodate this by replacing *σ* with a unimodal kernel, but then the SI must renegotiate §4 proofs.

**Scope of ψ**: *ψ* encodes both genetic (evolved calibration) and developmental/cultural (learned calibration) components. For moths, *ψ* is essentially genetic. For humans, *ψ* has a substantial cultural layer (e.g., "LV-bag is high-status" is learned). We treat *ψ* as fixed on the decision timescale for all agents; cultural evolution of *ψ* is modelled via §7.1.

**Empirical anchor**: Sadacca, Jones & Schoenbaum 2016 *Nature Neurosci* on *ψ*-heterogeneity in reward-learning; Coolen et al. 2003 *Behav Ecol* on conformist calibration.

### 2.2 Fitness utility *U*_fit

**Modeling commitment (MC-3)**: Fitness utility is the expected discounted integral of future instantaneous fitness:

$$
\boxed{\;U_{\text{fit}}(s, t) \;=\; \mathbb{E}\!\left[ \int_t^\infty e^{-r(\tau - t)} \, W(s, \tau) \, d\tau \right]\;}
\qquad (2.2)
$$

with:
- *r* > 0 the **biological/welfare discount rate** (population-level; distinct from agent-level *k_i*);
- *W*: *S* × ℝ_+ → ℝ the instantaneous fitness contribution;
- 𝔼[·] taken over environmental stochasticity (not over the agent's beliefs).

**Justification of integrated-expected form (MC-3a)**:
1. **Evolutionary theory baseline**: Fisherian fitness is defined as expected lifetime reproductive success; (2.2) is the generalised-lifetime formalism à la Charlesworth 1980 *Evolution in Age-Structured Populations*.
2. **Welfare-economics baseline**: (2.2) is the standard expected-discounted-utility form in Ramsey-Cass-Koopmans; unlike consumer utility, *W* here is objectively measured (not self-reported).
3. **Separability from beliefs**: (2.2) does NOT condition on agent's beliefs *B_i* — it is the *true* fitness utility, against which the agent's *U*_perc is compared.

**Falsifiability of MC-3**: If fitness is not time-separable (e.g., state-dependent: the fitness cost of one unit of *s* depends on the path of past *s*-consumption), (2.2) requires generalisation to a Bellman functional:

$$
U_{\text{fit}}(s, t) \;=\; W(s, t) + e^{-r \Delta t} \, \mathbb{E}[U_{\text{fit}}(s^*, t + \Delta t)]
$$

where *s** is the fitness-optimal continuation. We admit this extension for rational-addiction-like dynamics and handle it in §7.4 (state-dependent sub-class).

**Scope commitment**: In the discrete-panel empirical work, (2.2) specialises to *U*_fit(*s*, *t*) = Σ_{τ=t}^{t+K} *γ*^(τ−t) *W*(*s*, *τ*) with *γ* = exp(−*r*), *K* = horizon; this matches the structural recovery in Paper 2 (discussed in `05-manuscript/draft`).

### 2.3 Coupling parameter *ρ*

Define the **historical signal distribution** *S*_hist(*t*): the distribution over *S* experienced by the agent's evolutionary/cultural lineage up to time *t*. Let *ρ*(*t*) denote:

$$
\rho(t) \;=\; \operatorname*{Corr}_{s \sim S_{\text{hist}}(t)}\!\bigl[ U_{\text{perc}}(s, t \mid \psi), \; U_{\text{fit}}(s, t) \bigr]
\qquad (2.3)
$$

where both utilities are evaluated at the same *s*, *t* pair, and the correlation is over *s*.

- **AE regime**: *ρ*(*t*) ≈ 1 when the agent's *ψ* was calibrated against signals *s* drawn from (a stable) *S*_hist(*t*). This is Axiom A1.
- **ME regime**: *ρ*(*t*) < *ρ*_crit when novel signals enter *S* that were not in *S*_hist and thus not in the calibration set of *ψ*. This is Axiom A2.

**Modeling commitment (MC-4)**: *ρ*_crit = 0.3 by default (conservative but strict). The theory is robust to *ρ*_crit ∈ [0.2, 0.5]; see sensitivity analysis in Paper 1 §03-predictions/robustness.md (forthcoming, Phase B).

---

## §3 Axiom system (A1–A4)

This section presents four axioms from which the Sweet Trap predictions in Paper 1 §03-predictions/ are derivable as theorems (Phase B of the work). Each axiom includes: formal statement; interpretation; scope condition; empirical anchor reference; falsifiability sketch.

### Axiom A1 — Ancestral Calibration

**Formal statement**:

$$
\exists\, h : \mathbb{R} \to \mathbb{R}\; \text{strictly monotone increasing, continuous,} \qquad \qquad \text{(A1.1)}
$$

$$
\forall s \in S_{\text{anc}},\; \forall t < t_{\text{sep}}:\quad U_{\text{perc}}(s, t \mid \psi) \;=\; h(U_{\text{fit}}(s, t)) \;+\; \varepsilon(s, t) \qquad \text{(A1.2)}
$$

with *ε*(*s*, *t*) a **calibration noise** with 𝔼[*ε*] = 0 and Var[*ε*] = *σ*²_cal ≪ Var[*U*_fit] on *S*_anc.

**Interpretation**: In the ancestral regime, the reward system is a **noisy but monotone** encoder of fitness. The monotone function *h* need not be linear; only increasing. Any agent facing *S*_anc in *t* < *t*_sep has *U*_perc that ranks signals in the same order as *U*_fit, with additive noise below fitness variation.

**Scope condition**: A1 applies only to (*s*, *t*) in the ancestral regime. A1 does not prescribe the form of *h*; in §4 we use the consequence that *ρ*(*t*) → 1 as the noise shrinks.

**Empirical anchor**:
- Shizgal & Conover 1996 *Neurobiol Learn Mem* — self-stimulation calibrates to caloric intake.
- Schultz 2016 *Physiol Rev* — dopamine RPE tracks reward magnitude across taxa.
- Cosmides & Tooby 1992 *The Adapted Mind* — domain-specific psychological adaptations.

**Falsifiability of A1**:
- **Test T_A1**: estimate *h* in a species/domain of current environment where we have independent measurement of both *U*_perc (via neural assay) and *U*_fit (via lifetime-reproductive-success tracking in field). Find violations of monotonicity.
- **Known weak case**: A3 plastic ingestion in turtles — A1 applied to *S*_anc (shrimp-and-jellyfish olfactory cues) predicts monotone *h*; applied to *S*_mod (plastic with similar olfactory signature) predicts A1 fails — which is a pass of the axiom's scope, not a falsification. A true falsification would require finding a taxon where *U*_perc ranking contradicts *U*_fit ranking **within** *S*_anc.

### Axiom A2 — Environmental Decoupling

**Formal statement**:

$$
\exists\, t_{\text{sep}} \in \mathbb{R}_+,\; \exists\, \rho_{\text{crit}} \in (0, 1):\qquad \qquad \text{(A2.1)}
$$

$$
\forall s \in S_{\text{mod}} \setminus S_{\text{anc}},\; \forall t > t_{\text{sep}}:\quad \rho(s, t) \;<\; \rho_{\text{crit}} \qquad \text{(A2.2)}
$$

where *ρ*(*s*, *t*) is the local coupling — computed by restricting the historical distribution to a neighbourhood of *s* under a measurable partition of *S*.

**Interpretation**: After time *t*_sep, specific signals enter the agent's choice space that are **not** calibrated. On those signals, the relation (A1.2) fails: *U*_perc can be high while *U*_fit is zero or negative.

**Scope condition**: A2 is local (restricted to *s* ∈ *S*_mod \ *S*_anc). It does not claim *every* novel signal decouples — it claims decoupling occurs for some novel signals in every domain where Sweet Trap instantiates.

**Two routes to A2** (matching v2 §1.1):
- **Route A (mismatch)**: calibration was against *S*_anc; environment has shifted to *S*_mod faster than *ψ* can adapt. Empirical pattern: sensory trap (moth/light), nutritional trap (Drosophila/sugar; human/processed food).
- **Route B (supernormal / novel signal)**: a signal with no ancestral referent piggybacks on general-purpose reward architecture (Olds-Milner, livestream tipping, variable-ratio slot machines). Δ_ST is maximal by design.

**Empirical anchor**:
- Schlaepfer, Runge & Sherman 2002 *TREE* — ecological traps as local A2 violations.
- Nesse 2005 *Evol Hum Behav* — evolutionary mismatch.
- Woodcock et al. 2017 *Science* — neonicotinoid colony reproduction (A2 Route A in honeybees).
- Olds & Milner 1954 *J Comp Physiol Psychol* — A2 Route B (experimental).

**Falsifiability of A2**:
- **Test T_A2**: Identify a signal *s* ∈ *S*_mod \ *S*_anc for which *ρ*(*s*, *t*) ≥ *ρ*_crit across the distribution of ψ_i. For example, if automobile-design choices (arguably novel) turned out to maintain high reward-fitness coupling, this would be a ψ calibration surprise — and a falsification.

### Axiom A3 — Endorsement Inertia (*Scope-defining*)

**Important framing note (Stage 1-B revision)**: A3 is a **scope-defining axiom**, not a universal claim about all human choice. A3 carves out the Sweet Trap regime — a specific behavioural class characterised by the empirical criterion A3.0 below. Agents satisfying A3.0 are within Sweet Trap scope; A1, A2, A3, A4 apply to them. Agents not satisfying A3.0 are by definition outside Sweet Trap scope and this framework makes no claim about them. This framing addresses the tautology concern flagged in the rigor audit (F2).

**Operational Sweet Trap scope criterion (A3.0)**:

Sweet Trap scope is empirically determined by either condition holding for the agent/population and target signal *s**:

1. **Information-intervention test**: Post-full-information-intervention abandonment rate of *s** is < 30% (where "full information" means delivering a credible, comprehensive disclosure of *U*_fit(*s**) ≪ *U*_fit(*s*_0) — e.g., Surgeon-General-strength warning + quantified risk estimates). Abandonment rate ≥ 30% implies the agent has inferred *w* ≥ 0.45 and is outside Sweet Trap scope.

2. **Revealed-*w* test**: Observed choice pattern *b_i* satisfies the argmax structure (A3.2) with inferred *w* < 0.45 over a window of *N* ≥ 10 repeated choices. Structural estimation (e.g., via revealed-preference inversion of A3.1 with observed (*U*_perc, *E*[*U*_fit ∣ *B*]) estimates) can recover *w*.

Agents outside this scope (e.g., "one glass of wine at dinner" under moderate belief calibration where the agent demonstrably responds to health information; casual recreational users who quit easily on disclosure; professional investors evaluating 401(k) contributions with high deliberative weight) are by definition **not Sweet Trap cases**, and A3 does not apply to them. A3 is therefore a scope-defining axiom for a specific behavioural regime, **not a universal statement about all human choice**.

**Formal statement (within A3.0 scope)**: Given agent *i*'s belief *B_i*(*t*) about *U*_fit, define the agent's subjective valuation of *s*:

$$
\tilde U_i(s, t) \;=\; (1 - w_i) \cdot U_{\text{perc}}(s, t \mid \psi_i) \;+\; w_i \cdot \mathbb{E}[U_{\text{fit}}(s, t) \mid B_i(t)] \qquad \text{(A3.1)}
$$

Choice rule:

$$
b_i(t) \;=\; \arg\max_{s \in S_{\text{available}}(t)} \tilde U_i(s, t) \qquad \text{(A3.2)}
$$

**Boundedness constraint (A3.3)** — consequence of A3.0, not independent assumption:

$$
\exists\, w_{\max} < \tfrac{1}{2} :\quad \forall i \text{ in Sweet Trap scope},\; w_i \leq w_{\max} \qquad \text{(A3.3)}
$$

Per A3.0, *w*_max = 0.45 is the operational cutoff; *w*_max = 0.4 is the modelling default used in theorem proofs (provides safety margin against measurement noise).

**Interpretation**: Agents do attend to (and form beliefs about) fitness, but they do so with a **structurally bounded weight** *w* ≤ *w*_max < ½. When *U*_perc and 𝔼[*U*_fit ∣ *B*] disagree, the **perceived utility dominates the choice** by a factor of at least 1 − *w*_max > ½.

**Scope condition**: A3 applies to choices made under endorsement — i.e., voluntary, uncoerced action. It does NOT apply to:
1. Coerced exposure (where choice is forced by non-reward constraints; e.g., 996 overwork). See `discriminant_validity_v2.md` §1.3, C2/D3 negative controls.
2. Acute clinical compulsion (e.g., substance-use disorder at DSM-5 threshold), where the agent reports subjective loss of control — F2 fails.

**Modeling commitment (MC-5)**: *w*_max = 0.4 is the **theoretical default**. *w*_max < ½ is the **invariant lower-bound requirement**. A rational agent has *w* = 1, which violates A3.3 and is outside the Sweet Trap scope.

**Justification of *w*_max < ½**: Below ½ the perceived-utility term dominates in every possible comparison (since (1−*w*) > *w*). Above ½ the agent is "more rational than hedonic" and Δ_ST no longer implies trap behaviour.

**Empirical anchor**:
- Revealed-preference literature on health-behaviour gaps (e.g., smoking cessation despite known mortality: Chaloupka et al. 2012 *Tobacco Control*). Estimated effective *w* typically 0.15–0.35.
- Berridge & Robinson 2016 — wanting ≠ liking; wanting dominates choice.

**Falsifiability of A3**:
- **Test T_A3**: Provide agents with strong beliefs that *U*_fit < 0 (information intervention) and observe whether their choice shifts to prefer *s*_0. If agents robustly abandon *s* upon receiving the belief update, their *w* is close to 1 and A3.3 fails for that population.
- **Existing evidence against A3**: if well-designed information interventions achieved >70% abandonment of the Sweet-Trap signal, A3 would be seriously weakened. Actually observed: typical 5–15% effect from pure-information interventions (see v2 §4 P4 meta-literature). A3 survives.

### Axiom A4 — Partial Cost Visibility (with Parameterization P1 for Temporal Discount)

**Stage 1-B revision (M1)**: A4 has two parts. The **axiomatic core** of A4 is the observable-cost equation (A4.1) and the assertion that *some* form of temporal discount exists with *δ*′(*τ*) < 0. The **specific hyperbolic form** (A4.3) is demoted to **Parameterization P1** — a modelling choice for parsimony and evolutionary-stability rationale (McNamara 2009), not a second independent axiom. Theorems T1–T4 hold under any P1 specification that preserves *δ*′(*τ*) < 0 and bounded *δ*(0) = 1; constants depend on the specific form.

**Formal statement**: The observable cost signal is

$$
c_i(s, t) \;=\; \bigl[ U_{\text{fit}}(s_0, t) - U_{\text{fit}}(s, t) \bigr] \cdot I_{\text{visible}}(s, t) \;+\; \eta_c \qquad \text{(A4.1)}
$$

with *I*_visible ∈ {0, 1} the observability indicator and *η_c* ∼ 𝒩(0, *σ*²_c) noise.

The agent's **effective cost** for decision at horizon *τ* is

$$
c_{\text{eff}}(s, t; \tau) \;=\; \delta(\tau) \cdot c_i(s, t) \qquad \text{(A4.2)}
$$

**Axiomatic content of A4 (core)**: *δ*(*τ*) satisfies *δ*(0) = 1, 0 ≤ *δ*(*τ*) ≤ 1, and *δ*′(*τ*) < 0 for *τ* > 0. Theorems T1–T4 rely only on this core.

**Parameterization P1 (default form, not an independent axiom)** — hyperbolic discount:

$$
\boxed{\;\delta(\tau) \;=\; \frac{1}{1 + k_i \cdot \tau},\qquad k_i > 0.\;} \qquad \text{(P1; formerly labeled A4.3)}
$$

The choice of hyperbolic δ(τ) = 1/(1+kτ) vs exponential *e*^{−*kτ*} vs Laibson quasi-hyperbolic *β*-*δ* is a **parameterization** choice under the A4 core; the framework is parameterization-robust. Hyperbolic is the default for three reasons given in MC-6 below (parsimony + fit + evolutionary grounding). Under exponential or *β*-*δ*, theorems T1–T4 hold with modified numerical constants (typically weakening the decay-rate bound in T1 but preserving the dominance direction in T2).

**Interpretation**: Agents do receive noisy cost signals about choices, but they **heavily discount** future-cost components via hyperbolic time-preference (Ainslie 1975 *Psychol Bull*). The parameter *k_i* is heterogeneous across agents.

**Scope condition**: (A4) applies to cost signals that are (i) observable and (ii) temporally discountable. Costs that are acute and vivid (immediate) satisfy *δ*(0) = 1 (full weight). Costs that are borne by others (externalised via *λ_i*; see §5) are reduced by (1 − *λ_i*) before being discounted.

**Modeling commitment (MC-6)** — default parameterization under P1: hyperbolic *δ*(*τ*) = 1/(1+*kτ*) is the default, chosen (not axiomatically required) over exponential (*δ* = *e*^{−kτ}) or quasi-hyperbolic (Laibson *β*-*δ*). Justification:
1. **Empirical fit**: hyperbolic fits preference-reversal data (Ainslie 1975; Thaler & Shefrin 1981) better than exponential.
2. **Parsimony**: one parameter *k*, unlike Laibson's two (*β*, *δ*).
3. **Behavioural-ecology congruence**: McNamara, Stephens, Dall & Houston 2009 *TREE* show hyperbolic discount is evolutionarily stable under mortality variance — it naturally emerges from A1-grounded life-history optimisation.

**Falsifiability of MC-6**:
- If elicitation data (Frederick, Loewenstein & O'Donoghue 2002 *JEL*) in a target domain show exponential pattern (Δ(*τ*+Δ*τ*)/Δ(*τ*) constant), MC-6 fails and the theorems in Phase B must be re-derived with exponential discount. Predictions typically weaken but do not collapse.

**Empirical anchor**:
- Ainslie 1975 *Psychol Bull*; Laibson 1997 *QJE* (quasi-hyperbolic).
- Kirby & Herrnstein 1995 *Psychol Sci* — hyperbolic across commodities.

**Falsifiability of A4 itself**:
- **Test T_A4**: Regress observed choice behaviour against a two-parameter model (*δ*(*τ*) with hyperbolic form) and against the Laibson *β*-*δ* form. If *β*-*δ* is robustly preferred by AIC across multiple Sweet-Trap domains, A4 is qualified (retains scope but needs updated form).

### A3 + A4 together: the Sweet Trap choice

Combining A3 and A4, the agent's complete subjective valuation (for a single-period decision with a cost at horizon *τ*) is:

$$
\tilde U_i(s, t, \tau) \;=\; (1-w_i) U_{\text{perc}}(s, t \mid \psi_i) + w_i \mathbb{E}[U_{\text{fit}}(s, t) \mid B_i(t)] - \frac{(1-\lambda_i) \beta_i \cdot c_i(s,t) \cdot I_{\text{visible}}}{1 + k_i \tau} \qquad \text{(A3+A4.1)}
$$

This is the behavioural-economic utility used in §5 for dynamics.

### Why not more axioms?

Per the task's parsimony constraint, we stop at 4. An A5 was considered (externalization λ as standalone axiom) but rejected: *λ_i* is a **parameter** (fraction of cost borne by others) rather than an axiom because its empirical value is domain-specific and not universal. It enters (A3+A4.1) as a scaling factor on the cost term without requiring its own statement. Runaway Sweet Trap dynamics (§7.1) are derivable from A1-A4 plus the Lande-Kirkpatrick covariance assumption — also not a separate axiom.

---

## §4 Sweet Trap Index (core measure)

### 4.1 Definition

**The keystone scalar of the theory**:

$$
\boxed{\;\Delta_{\text{ST}}(s, t \mid \psi, B) \;=\; U_{\text{perc}}(s, t \mid \psi) \;-\; \mathbb{E}\!\bigl[ U_{\text{fit}}(s, t) \,\big|\, B \bigr]\;} \qquad (4.1)
$$

**Observable-population version** (used in empirical estimation): replace *B* with the population-mean unbiased expectation *U*_fit:

$$
\bar\Delta_{\text{ST}}(s, t) \;=\; U_{\text{perc}}(s, t \mid \psi) \;-\; U_{\text{fit}}(s, t) \qquad (4.1')
$$

**Correlation-form** (anchor for cross-species comparability, matching v2's Δ_ST definition): noting that under A1, *ρ*_AE = 1 and *U*_perc = *h*(*U*_fit); under A2, *ρ*(*t*) < *ρ*_crit. Then at the *population level*:

$$
\bar\Delta_{\text{ST}}(t) \;\propto\; (\rho_{\text{AE}} - \rho(t)) \;=\; 1 - \rho(t) \qquad \text{(4.1'')}
$$

Equation (4.1'') is the v2-compatible form; (4.1) is the individual-level version used in theorem proofs.

### 4.2 Core properties (proof sketches — full proofs in Phase B)

**Property 4.1** (Sign of Δ_ST under A1 + A2): For *s* ∈ *S*_anc, *t* < *t*_sep, Δ_ST(*s*, *t*) = *h*(*U*_fit(*s*, *t*)) − *U*_fit(*s*, *t*) + *ε*. Under mild regularity on *h*, 𝔼[Δ_ST] is near zero on *S*_anc. For *s* ∈ *S*_mod \ *S*_anc, *t* > *t*_sep, A2 implies large |Δ_ST|.

**Property 4.2** (Sweet Trap realisation):

$$
\text{SweetTrap}(s, t) \iff \Delta_{\text{ST}}(s, t) > 0 \;\;\wedge\;\; \text{chose}(s) \text{ under (A3.2)} \qquad (4.2)
$$

That is: **Δ_ST > 0 AND endorsement**. This is exactly the F1 + F2 sufficiency result from `discriminant_validity_v2.md` §4.3.

**Property 4.3** (Magnitude-persistence relation): Under (A4) and dynamic A3 application, behavioural persistence is monotone in |Δ_ST| (proof Phase B / Paper 1 §02-theorems/). Welfare deficit ΔW is monotone increasing in |Δ_ST| × (1 − *w*_max). This is the formal version of v2 Prop 1 (endorsement–fitness paradox).

**Property 4.4** (Belief invariance): Δ_ST is defined with respect to the belief *B*. If *B* coincides exactly with the true *U*_fit, then (4.1) reduces to (4.1'). If *B* is biased toward *U*_perc (A5 scenario rejected above — subjectively-rationalised trap), Δ_ST shrinks but the behavioural signature (endorsement of *s* with *U*_fit < 0) remains.

### 4.3 Relation to v2 definition

V2 §2 defined Δ_ST as a gradient in correlation: Δ_ST = *ρ*_AE − *ρ*_current. (4.1) and (4.1'') are related: **individual-level Δ_ST is the utility-wedge; population-level Δ_ST is the correlation drop**; the two are connected via the coupling (2.3).

Paper 1 unification: **we use (4.1) as the primary definition** because it is falsifiable for a single agent or single choice (you don't need a correlation to detect). The v2 (4.1'') form remains a useful population-level diagnostic and is recovered as a corollary.

---

## §5 Behavioural dynamics

### 5.1 Continuous-time evolution of agent engagement

Let *s_i*(*t*) be scalar engagement (e.g., daily sugar intake, weekly social-media hours). Define the agent's dynamics:

$$
\boxed{\;\frac{d s_i}{d t} \;=\; \alpha_i \cdot \frac{\partial U_{\text{perc}}}{\partial s}\bigg|_{s_i, t, \psi_i} \;-\; \beta_i \cdot \delta(\tau) \cdot I_{\text{visible}}(s_i, t) \cdot (1 - \lambda_i) \cdot \frac{\partial U_{\text{fit}}}{\partial s}\bigg|_{s_i, t} \;+\; \sqrt{2 D_i} \cdot \xi_i(t)\;} \qquad (5.1)
$$

where:
- *α_i* > 0: reward sensitivity (gradient-ascent step-size on *U*_perc);
- *β_i* > 0: cost aversion (gradient-descent step-size on observable fitness-cost, weighted by discount and externalisation);
- *δ*(*τ*) per P1 (hyperbolic default, formerly A4.3);
- *I*_visible per (A4.1);
- *λ_i*: externalisation share — fraction of cost borne by others — scales down the "effective gradient" the agent responds to;
- *ξ_i*(*t*): white-noise (Wiener) perturbation with diffusion *D_i* to capture stochastic exploration.

### 5.2 Sweet Trap attractor

**Sweet Trap condition (dynamical)**:

$$
\alpha_i \cdot |\nabla_s U_{\text{perc}}| \;\gg\; \beta_i \cdot \delta(\tau) \cdot (1 - \lambda_i) \cdot I_{\text{visible}} \cdot |\nabla_s U_{\text{fit}}| \qquad (5.2)
$$

Under (5.2), (5.1) predicts *ds_i*/*dt* > 0 even when *U*_fit decreases — **engagement escalates toward welfare loss**.

### 5.3 Discrete-choice dynamics (for *S* categorical)

When *S* is finite-discrete, replace (5.1) with a **continuous-time Markov chain** on *S*:

$$
\Pr[s_i(t + dt) = s' \mid s_i(t) = s] \;=\; \nu_{s \to s'} \cdot dt \qquad (5.3)
$$

with transition rates *ν*_{*s*→*s'*} = *ν*_0 · exp(*α_i*[*U*_perc(*s'*) − *U*_perc(*s*)] − *β_i* · *δ*(*τ*) · (1 − *λ_i*) · [*c*(*s'*) − *c*(*s*)]).

This is the Glauber / soft-max choice rule used in discrete-choice econometrics; (5.1) is its continuous limit.

### 5.4 Cost-channel update (belief dynamics)

Beliefs update by Bayesian rule on observed cost realisations:

$$
B_i(t + dt) \;\propto\; B_i(t) \cdot \mathcal{L}(c_i(s_i, t) \mid U_{\text{fit}}) \qquad (5.4)
$$

with likelihood ℒ from (A4.1). When *I*_visible = 0 (F4-blocked feedback), belief stays stuck — this is the dynamical mechanism by which F4 sustains the trap.

---

## §6 Equilibrium concepts

### 6.1 Instantaneous endorsement

A choice *s** is **instantaneously endorsed** by agent *i* at *t* iff *s** satisfies (A3.2) — i.e., it is the *argmax* of *Ũ_i*(*s*, *t*) over currently-available *S*.

### 6.2 Persistent endorsement

A choice *s** is **persistently endorsed** by agent *i* over a horizon *T* iff *s_i*(*t'*) = *s** for all *t'* ∈ [*t*, *t* + *T*]. Equivalently, *s** is a steady-state of (5.1) or a recurrent state of (5.3) over this horizon. This corresponds empirically to "I am still doing *s**" — the F3 persistence phenomenon.

### 6.3 Locally stable equilibrium (LSE)

*s** is a **locally stable equilibrium (LSE)** iff:
1. *ds_i*/*dt*\|_{*s_i* = *s**} = 0 (stationarity);
2. Small perturbations decay: for all |δ*s*| < *ε*, *s_i*(*t*) → *s** as *t* → ∞.

Formally, the Jacobian of (5.1) at *s** has all eigenvalues with negative real parts.

**Sweet Trap ⟹ LSE in bounded-w environment**: Under A1–A4 with *w_i* ≤ *w*_max < ½, a signal *s** with Δ_ST(*s**) > 0 and A4-discounted cost gradient is an LSE. (Proof Phase B.)

### 6.4 Evolutionarily Stable Strategy (ESS) considerations

At the **population level** (over many agents sharing *ψ*), Maynard Smith 1982 ESS analysis applies. A strategy "engage in *s**" is **ESS-stable** against a mutant strategy "abstain" iff the mutant's payoff (*U*_perc = 0) is less than the population payoff (*U*_perc at high engagement). This holds as long as A3.3 binds: the mutant who values fitness more (*w* > *w*_max) does worse on *U*_perc and is out-competed in terms of revealed preference, even if better off in fitness.

**Key theorem (Phase B)**: In mixed populations, Sweet Trap engagement is an ESS as long as *w*_max < ½ and signal supply (from *j* ∈ *J* designers, or from environmental shift) exceeds a critical threshold.

This ESS-stability is the **evolutionary inevitability** framing recommended by `benchmark_construct_vs_daly.md` §5 — a stronger anchor than DALY because it asserts the equilibrium's robustness.

---

## §7 Sub-class formalisms

### 7.1 Cultural-runaway subclass (RST)

**Cultural covariance** (from v2 §11.2):

$$
G_{\tau, y}^{\text{c}} \;=\; \operatorname{Cov}_{i \sim I}\!\bigl( y_i, \; \bar q_{j \in N(i)} \bigr) \qquad (7.1)
$$

where *q_i* is the trait (engagement level, ornament size), *y_i* is the preference setpoint, and *N(i)* is agent *i*'s social neighbourhood.

**Cultural Lande-Kirkpatrick dynamics**:

$$
\dot{\bar q} \;=\; G_q \frac{\partial \bar W_{\text{perc}}}{\partial \bar q} + G_{q,y}^c \frac{\partial \bar W_{\text{perc}}}{\partial \bar y} \qquad (7.2)
$$

$$
\dot{\bar y} \;=\; G_y \frac{\partial \bar W_{\text{perc}}}{\partial \bar y} + G_{q,y}^c \frac{\partial \bar W_{\text{perc}}}{\partial \bar q} \qquad (7.3)
$$

Note the replacement of *W̄* (mean fitness, Lande 1981) with *W̄*_perc (mean perceived utility at population level). This is a **critical extension**: classical Fisher runaway has agents optimising over fitness; in RST, agents optimise over *U*_perc because of A3. The runaway equilibrium is therefore driven by a self-amplifying **cultural feedback on perceived utility**, not on fitness.

**Formal justification (Stage 1-B revision, M6)**: The substitution *W̄* → *W̄*_perc in the Lande-Kirkpatrick equations is derived in **Lemma L4.1** (`lemmas.md`) via a mean-field argument over agent-heterogeneity distribution *F*(*ψ*). The derivation uses standard Gaussian approximation + Fourier-method techniques; the full calculation is sketched in `02-theorems/math_supplement §C.3` (a forthcoming supplementary document). We acknowledge this is a sketch + standard-technique argument rather than a complete original derivation; completing it to full analytical rigor is flagged as future work in the Discussion.

**Sweet Trap condition in RST**: (7.2)–(7.3) have a line-of-neutral-equilibria when *G_{q,y}^c* > *G*^c_crit (the cultural analogue of Lande's threshold). On this line, *q̄* can escalate indefinitely despite *W̄*_fit decreasing at a rate bounded by ∂*W̄*_perc/∂*q̄*.

**Empirical anchor**: Danchin et al. 2018 *Science* 362:1025 (Drosophila cultural mate-choice); Cavalli-Sforza & Feldman 1981; calibrated in `cultural_Gc_calibration.md` (v2 file).

### 7.2 Engineered Sweet Trap subclass (EST)

Let *j* ∈ *J* be an **external designing agent** (platform, advertiser, institution) who controls the **signal design** *s*_design ∈ *S*_design ⊂ *S*. The designer's objective:

$$
\max_{s_{\text{design}} \in S_{\text{design}}} \; \sum_i \Delta_{\text{ST}}(s_{\text{design}}, t \mid \psi_i) \cdot \omega_j(i) \qquad (7.4)
$$

where *ω_j*(*i*) is the designer's extraction weight on agent *i* (revenue per unit of *i*'s Δ_ST, for example).

**Key prediction**: EST has the **largest** equilibrium Δ_ST because (7.4) is an adversarial optimisation, whereas MST has Δ_ST bounded by the rate of environmental shift.

**Examples**:
- Olds-Milner electrode: experimenter designs direct reward with Δ_ST = +1 by construction.
- Variable-ratio reinforcement schedules in gambling: designer tunes *φ*(*s*, *t*) to maximise dopamine prediction-error signal.
- Algorithmic recommendation: RL-trained systems minimise regret in maximising engagement, which under A3+A4 is equivalent to maximising Δ_ST × *α*.

**Empirical anchor**: Simonite 2020; Rahwan et al. 2019 *Nature* 568:477 (machine behaviour); C12 PDE of this project.

### 7.3 Mismatch Sweet Trap subclass (MST)

Classical evolutionary mismatch (Lieberman 2013; Nesse 2005): *ψ* calibrated on *S*_anc; environment shifts to *S*_mod. Δ_ST grows as a function of the distance between distributions:

$$
\Delta_{\text{ST}}(s, t) \;\propto\; D_{\text{KL}}\bigl( \varphi(S_{\text{anc}}, t) \,\Big\|\, \varphi(S_{\text{mod}}(s), t) \bigr) \qquad (7.5)
$$

when the feature map *φ* is near-invariant to the substrate change. This is the *supernormal* case: artificial light has the *same feature φ* as natural light (positive phototaxis signal) but is at a different intensity / location.

### 7.4 Ecological trap as a special case

Robertson & Hutto 2006 *Ecology* 87:1075: habitat choice in novel environment. Formally, Sweet Trap restricted to *S* = {habitat patches}, with *U*_perc = habitat-cue preference calibrated on *S*_anc (pre-disturbance habitat features), *U*_fit = patch-specific survival-reproduction.

**Ecological trap ⊂ MST ⊂ Sweet Trap**: ecological trap is a type-specific instantiation with:
- *S* = habitats;
- *ψ* = habitat-cue preference (fixed on generation);
- Route A only (no route B available in habitat choice);
- *λ* = 0 (individual bears full cost);
- *w* = 0 (animals have no conscious belief update on habitat cost).

Under these specialisations, our general Δ_ST > 0 + endorsement machinery reduces exactly to Robertson-Hutto's habitat-selection trap condition.

### 7.5 Subclass summary

| Subclass | *ψ* calibration | Driver of Δ_ST | Signal supply | Canonical model |
|:---:|:---|:---|:---|:---|
| **MST** (Mismatch) | ancestral | environmental shift | exogenous | Schlaepfer 2002 |
| **RST** (Runaway) | cultural, self-referential | *G*^c amplification | endogenous (7.1)–(7.3) | Lande 1981 (cultural form) |
| **EST** (Engineered) | general-purpose | designer's (7.4) optimisation | adversarial | Olds-Milner / platform RL |
| **Kernel (KST)** | any | Δ_ST > 0 + endorsement | any | This paper §3 |

All three subclasses share A1–A4. They differ in *how* Δ_ST arises. The unification is the theoretical contribution.

---

## Appendix A — Summary of modeling commitments

| Tag | Commitment | Justification class | Falsifiability test |
|:---:|:---|:---|:---|
| MC-1 | *S* is measurable; no convexity required | parsimony | — |
| MC-2 | *U*_perc is logistic-sigmoidal in ⟨*ψ*, *φ*⟩ | saturation + neural evidence | non-monotone neural response |
| MC-3 | *U*_fit is expected-discounted integral of *W* | evolutionary-economic standard | non-separable payoff |
| MC-4 | *ρ*_crit = 0.3 | conservative, sensitivity-tested | robustness sweep 0.2–0.5 |
| MC-5 | *w*_max = 0.4; strict: *w*_max < 0.5 | endorsement dominance | info-intervention > 70% abandonment |
| MC-6 | *δ*(*τ*) hyperbolic; *k_i* heterogeneous | Ainslie + life-history | AIC favours exponential |

**Parameter defaults for simulation/empirical fit**: *ρ*_crit = 0.3, *w*_max = 0.4, *k_i* log-normal (ln *k* ∼ 𝒩(0, 0.5)), *α_i* log-normal (ln *α* ∼ 𝒩(0, 0.3)), *β_i*/*α_i* ratio ∼ 0.1 (baseline; Sweet Trap regime where reward dominates).

---

## Appendix B — Axiom–Feature–Subclass map

| Axiom | F-feature (v2) | Most directly implies | Tested in (Paper 1) |
|:---:|:---:|:---|:---|
| **A1** | — (pre-condition for F1) | ρ_AE ≈ 1 on *S*_anc | §02-theorems/T1 (AE benchmark) |
| **A2** | **F1** (ρ decoupling) | Δ_ST > 0 on *S*_mod | T2 (Δ_ST sign) |
| **A3** | **F2** (endorsement) | *w*_max-bounded rational hold-up | T3 (endorsement-welfare paradox) |
| **A4** | **F3** × **F4** | Persistence despite signalled cost | T4 (intervention asymmetry) |

Full theorem statements in `02-theorems/` (Phase B deliverable).

---

*End of axiomatic foundation v1. This document fully specifies the mathematical primitives, axioms, and dynamics for Paper 1 of sweet-trap-multidomain. Phase B will derive theorems T1–T4 on this basis. Phase C translates theorems to empirical predictions for the multi-domain panel data.*
