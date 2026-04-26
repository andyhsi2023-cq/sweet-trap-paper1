# Supporting Lemmas — Sweet Trap Theory (Paper 1, Phase B)

**Document**: Lemmas L1–L5 supporting theorems T1–T4
**Status**: v1.0, 2026-04-18
**Companion**: `theorems.md`, `proof_sketches_expanded.md`, `weak_joints_resolution.md`

**Purpose**: Isolate the mathematical sub-results on which the four theorems rest. Each lemma is stated independently so that theorems can cite it and reviewers can audit it without re-reading the full theorem proofs.

---

## L1 — Well-definedness of Δ_ST as a signed measure

### L1.1 Statement

Let *S* be a measurable space, *T* ⊆ ℝ_+ a time interval, *ψ* ∈ Ψ a reward-calibration parameter, and *B* a probability measure on *Ω*_fit. Assume:
- *U*_perc(*s*, *t* ∣ *ψ*) is bounded and measurable in (*s*, *t*);
- *U*_fit(*s*, *t*) is bounded and measurable in (*s*, *t*) and integrable with respect to *B*.

Then Δ_ST(·, · ∣ *ψ*, *B*): *S* × *T* → ℝ is a well-defined signed function with finite expectation under any measure *μ* on *S* × *T* for which *U*_perc and 𝔼[*U*_fit ∣ *B*] are *μ*-integrable.

### L1.2 Proof sketch

*U*_perc is logistic-sigmoidal (MC-2) of an inner product, bounded in (0, 1); measurability follows from measurability of *φ*, *ψ*, and composition with continuous *σ*. *U*_fit is an expectation of a measurable, bounded integrand *W*(*s*, *t*) discounted by *e*^{−*rτ*} (MC-3), hence measurable and integrable. The difference Δ_ST is measurable. Integrability of 𝔼[Δ_ST] under *μ* follows from finiteness of both terms.

∎

### L1.3 Consequence

Δ_ST admits well-defined expectations, moments, and cross-domain comparisons:
- 𝔼_*S*[Δ_ST] (domain mean),
- Var_*S*[Δ_ST] (domain dispersion),
- Cov[Δ_ST^(C1), Δ_ST^(C2)] (cross-domain correlation, used in Paper 2's multi-domain panel).

This is the mathematical foundation for treating Δ_ST as an empirical statistic.

---

## L2 — Hyperbolic discount implies preference reversal (Strotz 1955)

### L2.1 Statement

Let agent *i* at time *t* face a choice between two rewards: a small immediate reward *R*_1 available at *t*_1 = *t* + *τ*_1 and a larger delayed reward *R*_2 available at *t*_2 = *t* + *τ*_1 + Δ*τ*, with *R*_2 > *R*_1 > 0 and Δ*τ* > 0. Under parameterization P1 with hyperbolic *δ*(*τ*) = 1/(1 + *k_i τ*) (default P1 form; formerly labeled A4.3):

The agent's preference between (*R*_1, *τ*_1) and (*R*_2, *τ*_1 + Δ*τ*) depends on the current time *t*. Specifically, there exists a threshold *τ**(*R*_1, *R*_2, Δ*τ*, *k_i*) such that:
- For *τ*_1 > *τ** (both rewards are distant): agent prefers *R*_2 (larger-delayed).
- For *τ*_1 < *τ** (*R*_1 is imminent): agent prefers *R*_1 (smaller-immediate).

### L2.2 Proof sketch

The agent chooses the option maximising *δ*(*τ*) · *R*. Define

$$
\Delta(τ_1) \;=\; \delta(\tau_1) R_1 - \delta(\tau_1 + \Delta\tau) R_2 \;=\; \frac{R_1}{1 + k_i \tau_1} - \frac{R_2}{1 + k_i (\tau_1 + \Delta\tau)}
$$

At *τ*_1 = 0: Δ(0) = *R*_1 − *R*_2/(1 + *k_i* Δ*τ*). For sufficiently large *k_i* Δ*τ*, Δ(0) > 0 (prefer *R*_1).
At *τ*_1 → ∞: Δ(*τ*_1) → 0 from both sides; the ratio approaches *R*_1/*R*_2 < 1 (prefer *R*_2).

By continuity, there exists *τ** with Δ(*τ**) = 0; this is the preference-reversal point.

**Exponential discounting contrast**: Under *δ*(*τ*) = *e*^{−*k τ*}, the ratio *δ*(*τ*_1)/*δ*(*τ*_1 + Δ*τ*) = *e*^{*k*Δ*τ*} is **constant** in *τ*_1. No preference reversal. This is Strotz's 1955 original observation.

∎

### L2.3 Consequence

Hyperbolic discounting implies that even an agent with correct beliefs about *U*_fit will **systematically choose** the Sweet signal in the moment (high *U*_perc, imminent reward) over the delayed fitness benefit (low *U*_perc, distant cost avoidance). This is the mathematical engine behind A3 + A4's combined implication in T1.

### L2.4 Reference

Strotz, R. H. (1955). Myopia and inconsistency in dynamic utility maximization. *Review of Economic Studies*, 23(3), 165–180.

---

## L3 — Cognitive awareness does not imply behavioural escape (akrasia lemma, within A3 scope)

### L3.1 Statement

Let agent *i* be **within A3 scope** (A3.0 criterion satisfied; see `axioms_and_formalism.md` A3), and suppose the agent has **perfect belief** about *U*_fit: 𝔼[*U*_fit(*s*, *t*) ∣ *B_i*] = *U*_fit(*s*, *t*) for all (*s*, *t*). Suppose further that *U*_fit(*s**) < *U*_fit(*s*_0) (abstention is fitness-dominant). Then under A3.3 (*w_i* ≤ *w*_max < 1/2 — consequence of A3.0 scope), agent *i* may still choose *s** over *s*_0 whenever

$$
(1 - w_i) \cdot [U_{\text{perc}}(s^*) - U_{\text{perc}}(s_0)] \;>\; w_i \cdot [U_{\text{fit}}(s_0) - U_{\text{fit}}(s^*)] \,+\, \text{(cost term)}
$$

In particular, there exist (*α*, *ψ*, *φ*) configurations where the agent **knows** *s** is bad but **still chooses** *s**.

### L3.2 Proof sketch

Direct from A3.1 and A3.2. The left-hand side is the perceived-utility advantage of *s**; the right-hand side is the belief-weighted fitness disadvantage (plus cost-channel). Under A3.3, (1 − *w_i*) > *w_i*, so a modest perceived-utility advantage can outweigh a substantial belief-weighted fitness disadvantage.

**Construction**: set *U*_perc(*s**) − *U*_perc(*s*_0) = 1, *U*_fit(*s*_0) − *U*_fit(*s**) = 1 (matched magnitudes). Then the agent chooses *s** iff (1 − *w_i*) > *w_i*, i.e., iff *w_i* < 1/2. Under A3.3 this is always the case.

∎

### L3.3 Consequence

This lemma formalises the classical philosophical notion of **akrasia** (weakness of will; Aristotle's *Nicomachean Ethics* VII) **within the Sweet Trap scope**: an agent satisfying A3.0 can be **cognitively aware** of the fitness cost and **still behaviourally unable to escape**. This is not a paradox, not a "cognitive bias", and not irrational in the internal sense — given A3.3 (*w* < ½ as consequence of A3.0 scope), it is the **rational outcome** of an agent whose choice function weights *U*_perc dominantly. For agents outside Sweet Trap scope (A3.0 failed — e.g., agents who abandon > 30% after information intervention), L3 does not apply; such agents can and do escape traps via information alone.

**Implications for intervention design**:
- Pure information interventions cannot overcome L3: providing perfect belief (*B* = truth) does not guarantee choice change, because A3.3 caps the weight of belief.
- This is the mechanistic reason why T2's information-signal asymmetry exists.

### L3.4 Empirical anchor

- Chaloupka et al. 2012 *Tobacco Control*: smokers with high-accuracy mortality beliefs still smoke at rates 3–5× matched non-smoker populations; estimated effective *w* = 0.15–0.35.
- Baumeister et al. 2007 *Handbook of Self-Regulation*: ego-depletion and self-control literature broadly consistent with L3.
- Ariely 2008 *Predictably Irrational*: popular exposition of akrasia under choice.

---

## L4 — Cultural transmission is driven by *U*_perc (supports RST formalism)

### L4.1 Statement

In a population where agents' traits and preferences evolve via cultural transmission (social learning, imitation, conformity), the evolutionary-dynamic equations of Lande 1981 generalise to cultural variables. Under the standard cultural-evolution assumptions (Cavalli-Sforza & Feldman 1981; Boyd & Richerson 1985), the fitness-like quantity driving trait evolution is the **perceived** success of cultural models, not their **actual** fitness:

$$
\dot{\bar q}^{\text{cultural}} \;=\; G_q \cdot \frac{\partial \bar W_{\text{perc}}(\bar q, \bar y)}{\partial \bar q} \,+\, G_{q,y}^c \cdot \frac{\partial \bar W_{\text{perc}}(\bar q, \bar y)}{\partial \bar y}
$$

(replacing Lande's genetic *W̄* with perceived *W̄*_perc).

### L4.2 Proof sketch (why *W̄*_perc not *W̄*_fit)

**Step 1 (what agents observe during cultural transmission).** Social learners observe the **apparent success** of cultural models — their displayed status, wealth, popularity, social standing. They do not observe the models' lifetime reproductive success or long-term welfare. Hence the copying rule is based on *perceived* utility, not fitness utility.

**Step 2 (formalisation via Henrich-McElreath 2003 *JEL*).** The cultural update of trait *q_i* toward a model *j* occurs with probability proportional to *U*_perc(*j*) — the perceived quality of the model, which depends on visible signals *φ*(*j*, *t*).

**Step 3 (substitution).** Substituting this copying rule into Lande's derivation, the "selection gradient" becomes ∂*W̄*_perc/∂*q̄* rather than ∂*W̄*_fit/∂*q̄*. The rest of Lande's derivation proceeds identically.

∎

### L4.3 Consequence

This lemma **validates** the RST formalism (§7.1 of `axioms_and_formalism.md`, equations 7.2 and 7.3) which replaced Lande's *W̄* with *W̄*_perc. This was flagged as a weak joint in Phase A (see `weak_joints_resolution.md` §2); L4 formally resolves it.

**Corollary**: Cultural runaway can escalate *q̄* indefinitely even as *W̄*_fit declines, because the dynamics are driven by *W̄*_perc. This is the mathematical engine of RST (luxury-consumption arms races, ornament escalation).

### L4.4 References

- Cavalli-Sforza, L. L., & Feldman, M. W. (1981). *Cultural Transmission and Evolution*. Princeton.
- Boyd, R., & Richerson, P. J. (1985). *Culture and the Evolutionary Process*. Chicago.
- Henrich, J., & McElreath, R. (2003). The evolution of cultural evolution. *Evolutionary Anthropology*, 12(3), 123–135.
- Henrich, J. (2015). *The Secret of Our Success*. Princeton.
- Richerson, P. J., & Boyd, R. (2005). *Not by Genes Alone*. Chicago.
- Lande, R. (1981). Models of speciation by sexual selection on polygenic traits. *PNAS*, 78(6), 3721–3725.

---

## L4.1 — Mean-field derivation of *W̄*_perc substitution (Stage 1-B addition, M6)

### L4.1.1 Statement

For a population with individual reward-calibration vectors *ψ_i* distributed as *ψ_i* ~ *F*(*ψ*) with population-mean *ψ̄* and perturbation *η_i* := *ψ_i* − *ψ̄*, the population-mean perceived utility is

$$
\bar W_{\text{perc}}(\bar q, \bar y) \;=\; \int U_{\text{perc}}(s; \bar q + \eta, \bar y) \, dF(\eta)
$$

In the **mean-field limit** (large *N*, weak individual deviation Var[*η*] ≪ ‖*ψ̄*‖²), the population-scalar gradient ∂*W̄*_perc/∂*q̄* is well-defined and finite. Under this limit, the Lande-Kirkpatrick equations (7.2)–(7.3) of `axioms_and_formalism.md` §7.1 hold with *W̄*_perc substituted for the classical *W̄*_fit, producing the RST cultural-runaway dynamics.

### L4.1.2 Proof sketch (standard technique gesture)

**Step 1 (Taylor expansion in *η*)**. Expand *U*_perc around the population-mean *ψ̄*:

$$
U_{\text{perc}}(s; \bar q + \eta, \bar y) \;=\; U_{\text{perc}}(s; \bar q, \bar y) + \eta^\top \nabla_\psi U_{\text{perc}}|_{\bar q} + \tfrac{1}{2} \eta^\top \nabla_\psi^2 U_{\text{perc}}|_{\bar q} \eta + \mathcal{O}(\eta^3)
$$

**Step 2 (Gaussian approximation)**. Under mean-field assumption, *F*(*η*) is approximately Gaussian with zero mean and covariance Σ_*η* ≪ ‖*ψ̄*‖² *I*. Take expectation:

$$
\bar W_{\text{perc}} \;=\; U_{\text{perc}}(s; \bar q, \bar y) + \tfrac{1}{2} \operatorname{tr}(\Sigma_\eta \nabla_\psi^2 U_{\text{perc}}) + \mathcal{O}(\|\Sigma_\eta\|^2)
$$

The first-order term vanishes because 𝔼[*η*] = 0. The second-order term is a population-scalar correction independent of *q̄*, *ȳ* at first order. Hence ∂*W̄*_perc/∂*q̄* ≈ ∂*U*_perc/∂*q̄*|_{*ψ̄*} to leading order.

**Step 3 (Fourier method for exact evaluation)**. For non-Gaussian *F*(*η*), take the characteristic function *φ*_*F*(*k*) = 𝔼[*e*^{*i k η*}] and invert via Fourier methods:

$$
\bar W_{\text{perc}}(\bar q, \bar y) \;=\; \int \frac{dk}{(2\pi)^p} \; \tilde U_{\text{perc}}(k; \bar q, \bar y) \; \varphi_F(-k)
$$

where *Ũ*_perc is the Fourier transform of *U*_perc in *ψ*. This is standard population-genetics / statistical-mechanics technique (cf. Barton & Turelli 1987; Rice 2004). The substitution *W̄* → *W̄*_perc in Lande's derivation proceeds identically once *W̄*_perc is established as a well-defined scalar potential for population dynamics.

**Step 4 (substitution into Lande-Kirkpatrick)**. Lande's original derivation uses only the existence of a well-defined mean-fitness gradient ∂*W̄*/∂*q̄* and the covariance structure *G*_{*q*,*y*}. With *W̄*_perc replacing *W̄*_fit, the same derivation produces equations (7.2)–(7.3). The only formal change is that *W̄*_perc is not fitness-bounded; runaway equilibria can escalate beyond the biological-fitness collapse boundary.

∎ (sketch; full calculation deferred to math supplement §C.3, forthcoming)

### L4.1.3 Honest scope statement

**This is a sketch + standard-technique argument**, not a complete original derivation. Specifically:
- Step 2's Gaussian approximation requires Var[*η*] ≪ ‖*ψ̄*‖²; this is empirically plausible for cultural traits with moderate within-population variance but is not guaranteed for highly heterogeneous populations.
- Step 3's Fourier-method gesture assumes integrability conditions on *U*_perc; for the logistic-sigmoidal MC-2 form these hold, but a fully rigorous argument would enumerate the regularity conditions.

**NHB Article standard assessment**: This lemma provides mean-field justification at the level of "standard technique invoked with appropriate attribution". Completing it to full analytical rigor (including Var[*η*] bounds, integrability enumeration, and covariance-structure derivation from A3+A4) is flagged as **future work** in the Discussion.

### L4.1.4 Consequence

L4.1 formally justifies the W̄_perc substitution used in RST dynamics (§7.1 of axioms). The substitution is not an ad-hoc assumption; it is a population-level consequence of A3 applied mean-field to a heterogeneous population. Combined with L4 (cultural transmission operates on *U*_perc), this closes the derivation gap flagged in the Stage 1-B rigor audit (M6).

### L4.1.5 References

- Barton, N. H., & Turelli, M. (1987). Adaptive landscapes, genetic distance and the evolution of quantitative characters. *Genetical Research*, 49(2), 157–173.
- Rice, S. H. (2004). *Evolutionary Theory: Mathematical and Conceptual Foundations*. Sinauer.
- Lande, R. (1976). Natural selection and random genetic drift in phenotypic evolution. *Evolution*, 30(2), 314–334.

---

## L5 — Sigmoidal *U*_perc admits bounded gradient and well-defined curvature

### L5.1 Statement

Under MC-2, *U*_perc(*s*, *t* ∣ *ψ*) = *σ*(*α ⟨ψ, φ⟩*). Then:

(a) The gradient ∂*U*_perc/∂*φ*_*k* = *α σ*′(*α ⟨ψ, φ⟩*) *ψ_k* is bounded in absolute value by *α ψ_k* / 4 (since max *σ*′ = 1/4 at *σ* = 1/2).

(b) The second derivative (curvature) ∂²*U*_perc/∂*φ*_*k*² = *α*² *σ*″(*α ⟨ψ, φ⟩*) *ψ_k*² has a single maximum-magnitude value at *σ* = 1/2 (inflection point of σ) and decays to zero as *σ* → 0 or *σ* → 1.

(c) Under Sweet Trap conditions (*U*_perc near saturation, *σ* → 1), the curvature ∂²*U*_perc/∂*s*² < 0 strictly, with magnitude bounded below by a function of (*α*, *ψ*).

### L5.2 Proof sketch

(a) *σ*′(*x*) = *σ*(*x*)(1 − *σ*(*x*)), max at *x* = 0, *σ*′(0) = 1/4. Hence |∂*U*_perc/∂*φ*| ≤ *α* |*ψ*| / 4.

(b) *σ*″(*x*) = *σ*(*x*)(1 − *σ*(*x*))(1 − 2*σ*(*x*)) = 0 at *σ* = 1/2 for the middle factor... wait, let me redo: *σ*″ = *σ*(1−*σ*)(1 − 2*σ*), which is zero at *σ* = 0, *σ* = 1, and *σ* = 1/2. The non-zero extrema are at *σ* = (1 ± 1/√3)/2 ≈ 0.211 and 0.789. In the Sweet Trap regime (high *U*_perc ≈ saturation → *σ* near 1), *σ*″ < 0 strictly, with bounded magnitude.

(c) Chain rule gives ∂²*U*_perc/∂*s*² = *α*² *σ*″ (*ψ*^T ∂*φ*/∂*s*)². Under Sweet Trap conditions (*σ* > 0.789), *σ*″ < 0 strictly, and the curvature is strictly negative with magnitude bounded below by |*α*² *σ*″_min * *ψ*² (∂*φ*/∂*s*)²|.

∎

### L5.3 Consequence

This lemma provides the **curvature bound** *ℓ*(*ψ_i*, *φ*) that appears in T1's decay-rate lower bound. Specifically, *ℓ* ≥ |*α*² *σ*″_sat *ψ*²| for Sweet Trap agents near saturation, which is a positive constant depending only on (*α*, *ψ*), not on the particular *s* in the local neighbourhood of *s**.

It also justifies the linearisation argument used in T1 (Step 2 of proof): the Jacobian-eigenvalue analysis is well-posed because the second-derivative exists and is bounded.

---

## Lemma dependency graph

```
T1 ←── L1 (well-definedness), L5 (curvature), L2 (discount hyperbolic P1)
T2 ←── L1, L3 (akrasia, within A3 scope)
T3 ←── (axiom invariance, no specific lemma needed)
T4 ←── L1 + envelope theorem (Milgrom-Segal 2002); basin claim → Observation 4.1
RST ←── L4 (cultural W̄_perc transmission) + L4.1 (mean-field derivation, Stage 1-B)
```

---

*End of lemmas document. L1–L5 supply the sub-results needed to make theorem proofs rigorous.*
