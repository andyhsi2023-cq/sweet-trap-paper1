# Nomenclature — Sweet Trap Formal Theory (Paper 1)

**Date**: 2026-04-18
**Status**: Phase A / Mathematical Foundation, v1.0
**Scope**: Complete symbol table for the axiomatic system in `axioms_and_formalism.md`. Every downstream document (theorems, predictions, manuscript) must use these symbols consistently.
**Predecessor notation**: `00-design/sweet_trap_formal_model_v2.md` §8 (legacy) is preserved but superseded where they differ. Legacy symbols are noted in the right-most column.

---

## 1. Primitives — domains, sets, indices

| Symbol | Type | Domain | Meaning | Legacy (v2 §8) |
|:---:|:---:|:---|:---|:---:|
| *S* | set | arbitrary measurable space | **Choice space**: the set of admissible actions, states, or signal exposures. Discrete or continuous. | — |
| *s* | element of *S* | *s* ∈ *S* | A single choice, action, or exposure. Can be a scalar (e.g., daily screen minutes), a vector (e.g., (screen, diet, credit)), or a symbol (e.g., "buy-luxury-bag"). | *a* |
| *s₀* | element of *S* | distinguished point in *S* | The **null/abstention** choice (baseline; no engagement). | — |
| *i* | index | *i* ∈ *I* = {1, …, N} | **Agent index**. Finite population for empirical work, countable for limit theorems. | *i* |
| *N* | cardinality | ℕ or ∞ | Population size. | — |
| *t* | index | *t* ∈ ℝ₊ (cts) or ℤ₊ (disc) | **Time**. Continuous for ODE formulations, discrete for panel data. | *t* |
| *τ* | scalar | *τ* ∈ ℝ₊ | **Time lag** between decision and cost realisation. Distinct from v2's trait variable *τ* — see R1 below. | (conflict) |
| *j* | index | *j* ∈ *J* | Index for **designing agents** (e.g., advertisers, platforms, cultural institutions) in engineered sub-class. | — |
| *N(i)* | set | *N(i)* ⊂ *I* | **Social neighbourhood** of agent *i* in a cultural-runaway network. | — |

**Naming conflict resolution (R1)**: v2 §8 used *τ* both for "trait mean" (Lande-Kirkpatrick) and implicitly for time lags. Paper 1 theory uses *τ* **only** for time lags. The Lande-Kirkpatrick trait variable is renamed *q* (quantitative-trait, see §8 below).

---

## 2. Signal and fitness spaces

| Symbol | Type | Domain | Meaning | Legacy |
|:---:|:---:|:---|:---|:---:|
| *Φ* | set | ℝ^*k* for some *k* ≥ 1 | **Signal feature space**. The agent's sensory/perceptual apparatus projects *s* onto features *φ*(*s*, *t*). | — |
| *φ*(*s*, *t*) | function | *φ*: *S* × ℝ₊ → *Φ* | **Signal feature extractor**. Represents what the perceptual/reward system actually registers when choice *s* is taken at time *t*. Depends on *t* because the **signal distribution** in the environment shifts over time. | — |
| *φ*(*s*) | function | time-invariant case | Shortcut when features don't depend on *t*. | — |
| *Ω_fit* | set | subset of ℝ^*m*, *m* ≥ 1 | **Fitness outcome space**. Includes survival, reproduction, consumption-equivalent welfare, health trajectories. | — |
| *W*(*s*, *t*) | function | *W*: *S* × ℝ₊ → ℝ | **Instantaneous fitness-contribution function**. The rate of fitness accrual at time *t* if *s* is chosen at *t*. Can be negative (harmful choice). | (implicit) |
| *r* | scalar | *r* ∈ (0, 1) | **Biological/welfare discount rate** applied to future fitness. Distinct from individual hyperbolic bias *k*; *r* is a population-level baseline. | — |

---

## 3. Perceived utility (reward-system evaluation)

| Symbol | Type | Domain | Meaning | Legacy |
|:---:|:---:|:---|:---|:---:|
| *ψ_i* | vector | *ψ_i* ∈ Ψ ⊂ ℝ^*p* | **Reward calibration parameter vector** of agent *i*. Contains heritable (genetic) + developmental + cultural components. Treated as time-invariant on behavioural timescales; slowly varying on evolutionary/cultural-generation timescales. | — |
| *U*_perc(*s*, *t* ∣ *ψ_i*) | function | *U*_perc: *S* × ℝ₊ × Ψ → ℝ | **Perceived utility** — what the agent's neural reward system assigns to *s* at *t*. Sigmoidal form (see A1-commitment in `axioms_and_formalism.md` §2.1). | *R*_agent |
| *σ*(·) | function | *σ*: ℝ → (0, 1) | **Sigmoidal reward transform**. Committed to logistic: *σ*(*x*) = 1 / (1 + exp(−*x*)). Justified in §2.1.2 of the axiomatic doc. | — |
| *α_i* | scalar | *α_i* > 0 | **Reward sensitivity** of agent *i* — the slope of *U*_perc with respect to the feature-projection. Heterogeneous. | *θ* (partial overlap) |

**Committed functional form**:
*U*_perc(*s*, *t* ∣ *ψ_i*) = *σ*( *α_i* · ⟨*ψ_i*, *φ*(*s*, *t*)⟩ )
where ⟨·,·⟩ is the Euclidean inner product in *Φ*. See A1 justification.

---

## 4. Fitness utility (welfare/reproductive integration)

| Symbol | Type | Domain | Meaning | Legacy |
|:---:|:---:|:---|:---|:---:|
| *U*_fit(*s*, *t*) | function | *U*_fit: *S* × ℝ₊ → ℝ | **Fitness utility** — the expected discounted integral of future instantaneous fitness conditional on choosing *s* at *t*. | *F* |
| 𝔼[·] | operator | expectation over environmental stochasticity | Taken w.r.t. the true distribution of future environmental realisations, independent of the agent's beliefs. | — |

**Committed functional form**:
*U*_fit(*s*, *t*) = 𝔼[ ∫*_t^∞* *e*^(−*r*(*τ*−*t*)) · *W*(*s*, *τ*) d*τ* ]
Continuous-time version; discrete-time analogue uses summation and per-period discount *γ* = exp(−*r*).

---

## 5. Coupling parameter (the keystone)

| Symbol | Type | Domain | Meaning | Legacy |
|:---:|:---:|:---|:---|:---:|
| *ρ*(*t*) | scalar | *ρ* ∈ [−1, 1] | **Reward-fitness coupling** at time *t*: the correlation between *U*_perc and *U*_fit evaluated over the historical distribution of signals *S*_hist(*t*) at *t*. | — |
| *ρ*_AE | scalar | *ρ*_AE ≈ 1 | **Ancestral-environment coupling** (pre-separation, pre-novel-signal). | — |
| *ρ*_crit | scalar | *ρ*_crit ∈ (0, 1) | **Coupling threshold** below which a decoupling regime is said to obtain. Default commitment: *ρ*_crit = 0.3 (weak but positive; conservative). | — |
| *S*_hist(*t*) | probability distribution | on *S* | **Historical signal distribution** available to agent's population lineage up to time *t*. | — |
| *t*_sep | scalar | *t*_sep ∈ ℝ₊ | **Separation time**: the time at which specific signals enter the choice space that were absent from *S*_hist and thus outside the calibration period of *ψ_i*. | — |
| *S*_anc, *S*_mod | sets | *S*_anc ⊂ *S*, *S*_mod ⊂ *S* | **Ancestral** vs **modern** subsets of choice space. *S*_mod \ *S*_anc are the novel exposures. | — |

**Naming commitment (R2)**: *ρ* in this document is **always** the reward-fitness coupling scalar. v2's §1.3 also used *ρ* (letter rho) for a lock-in parameter (`sweet_trap_construct.md` §1.3) — Paper 1 renames that to **κ** (lock-in). See §7.

---

## 6. Beliefs, endorsement, choice rule

| Symbol | Type | Domain | Meaning | Legacy |
|:---:|:---:|:---|:---|:---:|
| *B_i*(*t*) | distribution | on *Ω_fit* | Agent *i*'s **subjective belief** about *U*_fit at time *t*. May be noisy, biased, or partial. | — |
| 𝔼[*U*_fit ∣ *B_i*(*t*)] | scalar | | Agent *i*'s **expected-fitness belief** for *s* at *t*. | — |
| *w_i* | scalar | *w_i* ∈ [0, 1] | **Endorsement weight**: the weight agent *i* puts on their belief about *U*_fit relative to *U*_perc when choosing. | — |
| *w*_max | scalar | *w*_max ∈ (0, 1/2) | **Endorsement ceiling**: the structural upper bound on *w* that distinguishes Sweet Trap (*w* ≤ *w*_max) from rational agent (*w* = 1). Default commitment: *w*_max = 0.4. | — |
| *b_i*(*t*) | element of *S* | *b_i*: ℝ₊ → *S* | Agent *i*'s **chosen behaviour** at time *t*. | — |

---

## 7. Costs and discounting

| Symbol | Type | Domain | Meaning | Legacy |
|:---:|:---:|:---|:---|:---:|
| *c_i*(*s*, *t*) | scalar | ℝ | **Observable cost signal** agent *i* receives about *s* at *t*. *c_i* is an imperfect estimate of the fitness-cost differential *U*_fit(*s*_0, *t*) − *U*_fit(*s*, *t*). | — |
| *η_c* | scalar | *η_c* ∼ 𝒩(0, *σ*²_c) | **Measurement noise** on the cost signal. | — |
| *δ*(*τ*) | function | *δ*: ℝ₊ → (0, 1] | **Hyperbolic discount function** applied by agent's decision rule to future costs. *δ*(*τ*) = 1/(1 + *k* · *τ*) per A4 commitment. | *β* (partial) |
| *k_i* | scalar | *k_i* > 0 | Agent *i*'s **hyperbolic discount rate**. Higher *k* = steeper present-bias. | *β* ~ 1−exp(−*k*·Δ*t*) |
| *β_i* | scalar | *β_i* > 0 | **Cost aversion** coefficient in dynamics — the strength with which observed (discounted) costs steer behaviour. | *β* (partial) |
| *I*_visible(*s*, *t*) | indicator | {0, 1} | **Cost observability indicator**: 1 if a cost signal is available for *s* at *t*; 0 otherwise. | — |
| *κ_i* | scalar | *κ_i* ≥ 0 | **Status-quo lock-in** parameter (renamed from v2's *ρ*). Asymmetric adjustment cost around current engagement level. | *ρ* (v2) |

**Commitment**: Paper 1 writes *δ*(*τ*) with hyperbolic form (not quasi-hyperbolic *β*-*δ* à la Laibson). This is a modeling choice, justified in A4.

---

## 8. Cultural-runaway subclass (Lande-Kirkpatrick variables)

| Symbol | Type | Domain | Meaning | Legacy |
|:---:|:---:|:---|:---|:---:|
| *q_i* | scalar | ℝ | **Quantitative trait** of agent *i* (e.g., luxury-spending level, ornament size). Population mean *q̄*. Renamed from v2's *τ* to avoid time-lag conflict. | *τ* (v2) |
| *y_i* | scalar | ℝ | **Preference / reward-setpoint** of agent *i* for trait *q* in others. Population mean *ȳ*. | *y* |
| *G_q*, *G_y* | scalars | ≥ 0 | Additive genetic (or cultural) variances. | *G_τ*, *G_y* |
| *G*_{*q*,*y*} | scalar | ℝ | **Cultural/genetic covariance** between trait and preference. | *G*_{*τ*,*y*} |
| *G*^c | scalar | ℝ | **Cultural covariance** specifically — Cov(*y_i*, *q̄*_{*j*∈*N*(*i*)}) per v2 §11.2. | same |
| *G*^c_crit | scalar | ≥ 0 | **Lande critical covariance** threshold for runaway instability. | *G*^{crit}_{*τ*,*y*} |
| *W̄*(*q*, *y*) | function | ℝ² → ℝ | Population **mean fitness** as a function of mean trait and preference. | same |

---

## 9. Behavioural dynamics

| Symbol | Type | Domain | Meaning | Legacy |
|:---:|:---:|:---|:---|:---:|
| ∇_*s* *U*_perc | function | cotangent space of *S* | Gradient of perceived utility in direction of choice variation. | — |
| ∇_*s* *U*_fit | function | same | Gradient of fitness utility. | — |
| d*s_i*/d*t* | derivative | tangent of *s_i*(*t*) | Rate of change of agent *i*'s engagement level (continuous-time). | — |
| Δ*s_i* | finite difference | Δ*s_i* = *s_{i,t+1}* − *s_{i,t}* | Discrete-time update. | — |
| *λ_i* | scalar | *λ_i* ∈ [0, 1] | **Externalisation share**: fraction of *c_i*(*s*, *t*) that is borne by agents *j* ≠ *i*. Preserved from v2. | same |

---

## 10. Derived diagnostics

| Symbol | Type | Domain | Meaning | Legacy |
|:---:|:---:|:---|:---|:---:|
| **Δ_ST(*s*, *t* ∣ *ψ*, *B*)** | scalar | ℝ | **Sweet Trap Index**: Δ_ST = *U*_perc(*s*, *t* ∣ *ψ*) − 𝔼[*U*_fit(*s*, *t*) ∣ *B*]. Equivalent form in population: Δ_ST(*t*) = *ρ*_AE − *ρ*(*t*) if the population's *U*_perc is unbiased estimator of *U*_fit. Details in §4 of axiomatic doc. | Δ_ST (v2) |
| **Σ_ST(*s*, *t*)** | scalar | ℝ₊ | **Severity**: Δ_ST × *τ*_F3 × (1 − *I*_feedback), as in v2. | Σ_ST |
| *π_t*(*s*) | scalar | [0, 1] | **Population share** choosing *s* at *t*. | same |
| *τ*_env | scalar | ℝ₊ | **Environmental signal-shift timescale** (Prop 3 in v2). | same |
| *τ*_adapt | scalar | ℝ₊ | **Adaptive/calibration timescale**. | same |

---

## 11. Subclass tags

| Tag | Meaning | F1 route | Typical F3 mechanism | v2 anchor |
|:---:|:---|:---:|:---:|:---:|
| **MST** | **Mismatch Sweet Trap** — ancestral reward calibrated in *S*_anc, deployed against *S*_mod | Route A | M1 / M4 | v2 §11.3 |
| **RST** | **Runaway Sweet Trap** — cultural-genetic covariance *G*^c drives arms-race escalation | Route A' (self-amplifying signal) | M2 / M3 | v2 §11.3 |
| **EST** | **Engineered Sweet Trap** — external agent *j* designs signals to maximise Δ_ST | Route B | M1 / M2 | v2 §11.3 |
| **KST** | **Kernel Sweet Trap** — abstract limit; all three subclasses share the keystone Δ_ST > 0 & endorsement structure | — | — | new |

---

## 12. Cross-reference to v2

| v2 §8 symbol | Paper 1 symbol | Change |
|:---:|:---:|:---|
| *a* | *s* | rename (clearer "state/signal" semantics) |
| *R*_agent(*a*) | *U*_perc(*s*, *t* ∣ *ψ*) | elaborated with parameter dependence |
| *F*(*a*) | *U*_fit(*s*, *t*) | elaborated with time argument |
| Δ_ST | Δ_ST | preserved, redefined with beliefs (§10) |
| Σ_ST | Σ_ST | preserved |
| *τ*, *y* | *q*, *y* | *τ* renamed to *q*; *y* preserved |
| *G*_{*τ*,*y*} | *G*_{*q*,*y*} | rename |
| *G*^{crit}_{*τ*,*y*} | *G*^c_crit | rename + specialisation |
| *θ*, *λ*, *β*, *ρ* (v2 L4) | *α*, *λ*, *k*/*β*, *κ* (Paper 1) | reinterpreted as dynamical coefficients |
| F1, F2, F3, F4 | F1, F2, F3, F4 | preserved unchanged |
| *τ*_env, *τ*_adapt | *τ*_env, *τ*_adapt | preserved |

**Collision rule**: when a legacy-v2 document references *τ* as trait, Paper 1 reads *q*. When a legacy-v2 document references *ρ* as lock-in, Paper 1 reads *κ*. When v2 references *β* as present-bias, Paper 1 reads *k* (for discount rate) + *β* (for cost aversion) — the v2 *β* has been split into two.

---

## 13. Quick cheat-sheet (for manuscript reviewers)

The five symbols you need to follow the paper:

1. **Δ_ST = *U*_perc − 𝔼[*U*_fit ∣ *B*]**. The single scalar. Δ_ST > 0 + endorsement = Sweet Trap.
2. ***ρ*(*t*)**. Reward-fitness coupling. Ancestral ≈ 1, modern < 1 (often near 0 or negative).
3. ***ψ_i***. Calibration parameters inherited by agent *i*. Fixed on behavioural timescale.
4. ***w*_max**. Endorsement ceiling. When *w_i* ≤ *w*_max, agent's choice is dominated by *U*_perc.
5. ***δ*(*τ*) = 1/(1 + *k* · *τ*)**. Hyperbolic discount of future costs. Not quasi-hyperbolic.

---

*End of nomenclature v1. Changes require coordinated update of `axioms_and_formalism.md` §2–§7 and `relationship_to_existing_models.md`. Any v2.x legacy document that contradicts this file is superseded by this nomenclature within the scope of Paper 1.*
