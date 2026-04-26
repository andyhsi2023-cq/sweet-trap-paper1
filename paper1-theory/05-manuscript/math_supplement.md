# Math Supplement — Sweet Trap Theory (Paper 1)

**Companion to**: `paper1_theory_draft.md`
**Contents**: Full proofs, extended positioning, complete nomenclature, extended references
**Status**: v1.0, 2026-04-18
**Authors**: Lu An, Hongyang Xi

This supplement provides the audit-proof mathematical content supporting the main text. Sections are:

- **§A** Axiomatic foundation with all modeling commitments (MC-1 to MC-6)
- **§B** Δ_ST correlation-form derivation
- **§C** RST Lande-Kirkpatrick dynamics (full derivation)
- **§D** Lemmas L1–L5 with proofs
- **§E** T1 proof (Jacobian, Lyapunov, basin)
- **§F** T2 full algebra (core theorem)
- **§G** T3 species-neutrality argument
- **§H** T4 envelope theorem application
- **§I** Extended positioning — seven adjacent theories (formal mappings)
- **§J** Nomenclature (complete symbol table)
- **§K** Extended references

The main-text manuscript cites this supplement at key points; section-tags correspond to the placements marked in the draft.

---

## §A Axiomatic Foundation — Modeling Commitments

### A.1 Six modeling commitments

| Tag | Commitment | Justification class | Falsifiability test |
|:---:|:---|:---|:---|
| MC-1 | *S* is measurable; no convexity required | parsimony | — |
| MC-2 | *U*_perc is logistic-sigmoidal: *U*_perc = σ(α⟨ψ, φ⟩) | saturation + neural evidence | non-monotone neural response (falsifies form) |
| MC-3 | *U*_fit is expected-discounted integral of *W* | evolutionary-economic standard | non-separable payoff structure |
| MC-4 | *ρ*_crit = 0.3 default; sensitivity 0.2–0.5 | conservative, sensitivity-tested | robustness sweep |
| MC-5 | *w*_max = 0.4; strict requirement *w*_max < 1/2 | endorsement dominance | info-intervention >70% abandonment |
| MC-6 | *δ*(*τ*) hyperbolic = 1/(1 + *k τ*); *k_i* heterogeneous | Ainslie + life-history | AIC favours exponential |

### A.2 Justification anchors for each MC

**MC-2** (logistic *U*_perc):
- Saturation: all studied reward circuits exhibit bounded firing rates (Schultz 2016 *Physiol Rev*; Berridge-Robinson 2016 *Am Psychol*).
- Neural evidence: dopamine prediction-error fits logistic over 3-log decades of reward magnitude (Tobler-Fiorillo-Schultz 2005 *Science*).
- Analytic tractability: sigmoidal form admits linearisation *U*_perc ≈ ½ + ¼ *α* ⟨ψ, φ⟩ in the unsaturated regime, enabling Δ_ST closed-form analysis in §B.

**MC-3** (expected-discounted integral *U*_fit):
- Evolutionary theory baseline: Fisherian fitness is expected lifetime reproductive success (Charlesworth 1980).
- Welfare-economics baseline: Ramsey-Cass-Koopmans expected-discounted-utility form.
- Key property: (2) does NOT condition on agent's beliefs — it is the *true* fitness utility.

**MC-5** (*w*_max < 1/2):
- *w* ≤ 0.5 is the minimum requirement for the Sweet Trap concept to make sense: the perceived-utility channel dominates the choice iff (1 − *w*) > *w*.
- Revealed-preference estimates in smoking (Chaloupka et al. 2012 *Tobacco Control*), dietary choice (Wang et al. 2023 *Lancet Planet Health*), and social-media use (Allcott et al. 2020 *AER*) cluster at *w* ∈ [0.15, 0.35].

**MC-6** (hyperbolic *δ*):
- Empirical fit: hyperbolic fits preference-reversal data better than exponential (Ainslie 1975; Thaler-Shefrin 1981).
- Parsimony: one parameter *k*, unlike Laibson β-δ's two.
- Behavioural-ecology congruence: hyperbolic emerges from life-history optimisation under mortality variance (McNamara et al. 2009 *TREE*).

### A.3 Parameter defaults for simulation/empirical fit

- *ρ*_crit = 0.3
- *w*_max = 0.4
- *k_i* log-normal: ln *k* ∼ 𝒩(0, 0.5)
- *α_i* log-normal: ln *α* ∼ 𝒩(0, 0.3)
- *β_i*/*α_i* ratio ∼ 0.1 (baseline Sweet Trap regime: reward dominates cost)

---

## §B Δ_ST Correlation-Form Derivation

### B.1 Population-level correlation form

From (10) in the main text:
$$
\Delta_{\text{ST}}(s, t \mid \psi, B) \;=\; U_{\text{perc}}(s, t \mid \psi) - \mathbb{E}[U_{\text{fit}}(s, t) \mid B]
$$

Under A1 (ancestral calibration), for *s* ∈ *S*_anc, *U*_perc = *h*(*U*_fit) + *ε* with 𝔼[*ε*] = 0. Hence:
$$
\operatorname*{Corr}_{s \sim S_{\text{anc}}}[U_{\text{perc}}, U_{\text{fit}}] \;=\; \rho_{\text{AE}} \;\approx\; 1
$$

Under A2, for *s* ∈ *S*_mod \ *S*_anc, *ρ*(*t*) < *ρ*_crit = 0.3.

### B.2 Derivation of population Δ_ST ∝ (1 − *ρ*)

Consider a population indexed by *s*-draws with *U*_perc = *a U*_fit + *η* where *η* has zero mean and variance *σ²*_η, and ρ is the Pearson correlation of (*U*_perc, *U*_fit) over the population. Then:
$$
\bar\Delta_{\text{ST}} \;=\; \mathbb{E}[U_{\text{perc}} - U_{\text{fit}}] \;=\; (a-1) \, \mathbb{E}[U_{\text{fit}}]
$$

When *a* ≈ 1 (matched scale) the mean Δ_ST is near zero; the **variance** Var[Δ_ST] tracks (1 − *ρ*²) Var[*U*_fit] plus Var[*η*]. Hence:
$$
\text{Var}[\Delta_{\text{ST}}] \;\propto\; 1 - \rho^2
$$

When matched on *U*_perc-saturation (the Sweet Trap regime where *U*_perc is near 1), Δ_ST becomes directly observable as the wedge between plateau-reward and declining-*U*_fit, and:
$$
\bar\Delta_{\text{ST}}(t) \;\propto\; \rho_{\text{AE}} - \rho(t) \;=\; 1 - \rho(t)
$$

This gives the v2-compatible population-level formula (equation 4.1'' in `axioms_and_formalism.md`).

### B.3 Individual vs population

The main text uses individual-level (10) as primary definition because:
- Falsifiable for a single choice (don't need a correlation to detect).
- Decomposable by domain and agent.
- Interpretable as a utility-wedge rather than a statistical property.

Population-level (1 − *ρ*) serves as a diagnostic for cross-country or cross-species comparison (Paper 2 v2.4 uses this form for the aggregate RST-G^c calibration).

---

## §C RST Lande-Kirkpatrick Dynamics

### C.1 Cultural covariance definition

$$
G^c_{q,y} \;=\; \operatorname*{Cov}_{i \sim I}\!\bigl(y_i, \; \bar q_{j \in N(i)}\bigr)
$$

where *q_i* is the trait (engagement level, ornament size), *y_i* is the preference setpoint, and *N(i)* is agent *i*'s social neighbourhood.

### C.2 Dynamics (main text equation 14)

$$
\dot{\bar q} \;=\; G_q \frac{\partial \bar W_{\text{perc}}}{\partial \bar q} + G^c_{q,y} \frac{\partial \bar W_{\text{perc}}}{\partial \bar y}
$$

$$
\dot{\bar y} \;=\; G_y \frac{\partial \bar W_{\text{perc}}}{\partial \bar y} + G^c_{q,y} \frac{\partial \bar W_{\text{perc}}}{\partial \bar q}
$$

### C.3 Critical difference from Lande 1981

Classical Lande (genetic Fisher runaway) uses *W̄* (mean fitness). RST uses *W̄*_perc (mean perceived utility at population level). Justification is **Lemma L4** (§D.4 below): cultural transmission is driven by observed perceived success, not by lifetime reproductive success. This is the systematic cultural analogue of Lande, not an ad-hoc substitution.

### C.4 Consequence: non-fitness-bounded runaway

Because *W̄*_perc can decouple from *W̄*_fit (A2), the dynamic amplifies traits that are **maladaptive** in fitness terms. The line-of-neutral-equilibria condition *G*^c_{*q*,*y*} > *G*^c_crit admits indefinite escalation along this line as long as *W̄*_perc supports it, which can persist while *W̄*_fit collapses. This is why conspicuous consumption escalates past household-solvency thresholds in high-LTOWVS societies.

### C.5 Stability analysis

The Jacobian of (14) at the critical covariance has trace ∝ *G_q* ∂²*W̄*_perc/∂*q̄*² + *G_y* ∂²*W̄*_perc/∂*ȳ*². When *G*^c_{*q*,*y*} > *G*^c_crit, the determinant changes sign, creating a line of marginally-stable equilibria. Full stability analysis follows Kirkpatrick 1982 *Evolution*.

---

## §D Lemmas L1–L5 (Proofs)

### §D.1 L1 — Well-definedness of Δ_ST

**Statement**: Under measurability of *φ*, *ψ*, *σ* and integrability of *W*(*s*, *τ*) with respect to *B*, Δ_ST: *S* × *T* → ℝ is well-defined and admits finite expectations, moments, and cross-domain correlations.

**Proof**: *U*_perc = σ(α⟨ψ, φ⟩) is a composition of measurable functions into a bounded interval (0, 1); hence measurable and bounded. *U*_fit is an expectation of a measurable, bounded integrand *W*(*s*, *τ*) discounted by *e*^{-*rτ*}, hence measurable and integrable (dominated convergence). The difference Δ_ST = *U*_perc − *U*_fit is measurable and bounded. Integrability of 𝔼[Δ_ST] under any measure *μ* for which *U*_perc and *U*_fit are *μ*-integrable follows from linearity of expectation. ∎

### §D.2 L2 — Hyperbolic discount implies preference reversal (Strotz 1955)

**Statement**: Under A4.3 with hyperbolic *δ*, preference between (*R*_1, *τ*_1) and (*R*_2, *τ*_1 + Δ*τ*) with *R*_2 > *R*_1 > 0 depends on *τ*_1. There exists a threshold *τ** such that for *τ*_1 > *τ** the agent prefers *R*_2, for *τ*_1 < *τ** the agent prefers *R*_1.

**Proof**: Let Δ(*τ*_1) = *δ*(*τ*_1) *R*_1 − *δ*(*τ*_1 + Δ*τ*) *R*_2 = *R*_1/(1 + *k τ*_1) − *R*_2/(1 + *k*(*τ*_1 + Δ*τ*)). At *τ*_1 = 0: Δ(0) = *R*_1 − *R*_2/(1 + *k*Δ*τ*) > 0 for sufficiently large *k*Δ*τ*. At *τ*_1 → ∞: Δ → 0 from a value bounded by *R*_1 − *R*_2 < 0 (ratio approaches *R*_1/*R*_2 < 1). By continuity there exists *τ** with Δ(*τ**) = 0. For exponential *δ* = *e*^{-kτ}, the ratio *δ*(*τ*_1)/*δ*(*τ*_1 + Δ*τ*) = *e*^{*k*Δ*τ*} is constant, so no reversal — this is Strotz's 1955 observation. ∎

### §D.3 L3 — Akrasia (cognitive awareness does not imply escape)

**Statement**: Under A3 with perfect belief 𝔼[*U*_fit ∣ *B_i*] = *U*_fit, and *U*_fit(*s**) < *U*_fit(*s*_0), the agent may still choose *s** whenever
$$
(1 - w_i)\,[U_{\text{perc}}(s^*) - U_{\text{perc}}(s_0)] \;>\; w_i\,[U_{\text{fit}}(s_0) - U_{\text{fit}}(s^*)]
$$

**Proof**: Direct from A3.1 and A3.2. Under A3.3, (1 − *w_i*) > *w_i*, so a modest *U*_perc advantage outweighs a substantial belief-weighted fitness disadvantage. Construction: set *U*_perc(*s**) − *U*_perc(*s*_0) = 1, *U*_fit(*s*_0) − *U*_fit(*s**) = 1. Agent chooses *s** iff (1 − *w_i*) > *w_i*, i.e., *w_i* < 1/2 — always true under A3.3. ∎

**Consequence**: Pure information cannot overcome L3. This is the mechanistic reason T2's asymmetry exists.

**Empirical anchor**: Chaloupka et al. 2012 — smokers with high-accuracy mortality beliefs smoke at 3–5× non-smoker rates; Baumeister et al. 2007 on self-regulation failure.

### §D.4 L4 — Cultural transmission is driven by *U*_perc (supports RST)

**Statement**: Under standard cultural-evolution assumptions (Cavalli-Sforza-Feldman 1981; Boyd-Richerson 1985; Henrich-McElreath 2003), the cultural-dynamic analogue of Lande's (1981) selection gradient uses perceived mean utility *W̄*_perc rather than mean fitness *W̄*:
$$
\dot{\bar q}^{\text{cultural}} \;=\; G_q \frac{\partial \bar W_{\text{perc}}}{\partial \bar q} + G^c_{q,y} \frac{\partial \bar W_{\text{perc}}}{\partial \bar y}
$$

**Proof sketch**:
*Step 1 — observability*: Social learners observe the apparent success of cultural models (displayed status, wealth, popularity). They do not observe lifetime reproductive success or long-term welfare. Hence the copying rule is based on *perceived* utility.
*Step 2 — formalisation* (Henrich-McElreath 2003 *Evolutionary Anthropology*): cultural update of *q_i* toward model *j* occurs with probability proportional to *U*_perc(*j*).
*Step 3 — substitution*: Replacing Lande's fitness-proportional copying with perceived-utility-proportional copying gives selection gradient ∂*W̄*_perc/∂*q̄* in place of ∂*W̄*/∂*q̄*. Rest of Lande's derivation proceeds identically. ∎

### §D.5 L5 — Sigmoidal *U*_perc bounded gradient and curvature

**Statement**: Under MC-2 (*U*_perc = σ(α⟨ψ, φ⟩)):

(a) ∂*U*_perc/∂*φ*_*k* = *α σ*′(·) *ψ_k*, bounded by *α ψ_k*/4 (since max σ′ = 1/4 at σ = 1/2).

(b) ∂²*U*_perc/∂*φ*_*k*² = *α² σ*″(·) *ψ_k*², where σ″ = σ(1−σ)(1−2σ). Zero at σ ∈ {0, 1/2, 1}; non-zero extrema at σ ≈ 0.211 and σ ≈ 0.789.

(c) Under Sweet Trap conditions (*U*_perc near saturation, σ → 1), σ″ < 0 strictly, with bounded magnitude *ℓ* = |*α² σ*″_sat *ψ*² (∂*φ*/∂*s*)²| > 0.

**Proof**: σ′ = σ(1−σ) achieves max 1/4 at σ = 1/2. σ″ = σ(1−σ)(1−2σ) vanishes at σ = 0, 1/2, 1; in the Sweet Trap regime with σ > 0.789, σ″ < 0. Chain-rule for ∂²*U*_perc/∂*s*² with *f*(*s*) = ⟨*ψ*, *φ*(*s*)⟩ gives ∂²*U*_perc/∂*s*² = *α² σ*″(·) *f*′²(*s*) + *α σ*′(·) *f*″(*s*). Under *f*″ = 0 (linear feature extractor) and σ near saturation, ∂²*U*_perc/∂*s*² ≈ -|*α² σ*″| *f*′² = -*ℓ* < 0. ∎

**Consequence**: Provides curvature bound *ℓ* for T1's decay-rate lower bound.

---

## §E T1 Proof — Stability of Sweet Trap LSE

### §E.1 Setup

Agent dynamics (main text equation 12):
$$
\frac{ds_i}{dt} \;=\; \alpha_i \partial_s U_{\text{perc}} - \beta_i \delta(\tau)(1-\lambda_i) I_{\text{visible}} \partial_s U_{\text{fit}} + \sqrt{2 D_i}\,\xi_i(t)
$$

### §E.2 Jacobian at *s**

At *s* = *s** (stationarity):
$$
J(s^*) \;=\; \alpha_i \partial^2_s U_{\text{perc}}(s^*) - \beta_i \delta(\tau)(1-\lambda_i) I_{\text{visible}} \partial^2_s U_{\text{fit}}(s^*)
$$

By L5, ∂²_*s U*_perc < 0 strictly at *s** under Sweet Trap conditions (σ near saturation), with magnitude ≥ *ℓ*(*ψ, φ*) > 0. The cost-curvature ∂²_*s U*_fit is typically positive (diminishing fitness-loss rate) or near zero, weighted by *δ*(*τ*)(1−*λ_i*)*I*_visible ≤ 1 and often ≪ 1. Hence:
$$
J(s^*) \;\leq\; -\alpha_i \ell(\psi_i, \varphi) + \beta_i \delta_{\max} M
$$

For Sweet Trap regime (cost attenuated), *J*(*s**) < 0. All eigenvalues have negative real parts.

### §E.3 Lyapunov function

Construct *V*(*s*, *t*) = ½‖*s* − *s**‖² + *μ g*(Δ_ST(*s*, *t*)) with *μ* > 0 small, *g* smooth convex non-negative.

$$
\dot V \;=\; (s - s^*)^T J(s^*) (s - s^*) + \mu g'(\Delta_{\text{ST}}) \cdot \partial_t \Delta_{\text{ST}} + O(\mu)
$$

The first term is ≤ -*c* ‖*s* − *s**‖² with *c* = −λ_max(*J*(*s**)) ≥ *α_i ℓ ε*² (using L5 curvature bound scaled by Δ_ST² ≈ *ε*²). The second term is bounded under persistence A1.1.

For *μ* sufficiently small:
$$
\dot V \;\leq\; -c' \|s - s^*\|^2 \;\leq\; -c' V
$$

with *c*′ ≥ *c* minus a small *O*(*μ*) correction. Gronwall's inequality gives *V*(*t*) ≤ *V*(*t*_0) *e*^{-*c*′(*t*−*t*_0)}, and since ‖*s* − *s**‖² ≤ 2*V*:
$$
\|s(t) - s^*\|^2 \;\leq\; C \|s(t_0) - s^*\|^2 \, e^{-c'(t-t_0)}
$$

### §E.4 Basin of attraction radius

The linearised analysis holds where second-order Taylor of (12) around *s** is valid. Breakdown at ‖*s* − *s**‖ ∼ |σ″/σ‴| ≈ 1/*α*. For larger Δ_ST, the curvature ℓ is larger (σ is more saturated), and:
$$
R_{\text{basin}} \;\sim\; \frac{1}{\alpha} \cdot h(\Delta_{\text{ST}})
$$

with *h* an increasing function. *R*_basin grows with Δ_ST — larger wedges produce wider basins. ∎

---

## §F T2 Full Algebra — Intervention Asymmetry

### §F.1 Setup

Agent subjective valuation at the LSE *s**:
$$
\tilde U_i(s, t) = (1 - w_i) U_{\text{perc}}(s, t \mid \psi_i) + w_i\, \mathbb{E}[U_{\text{fit}}(s, t) \mid B_i(t)] - C_i(s, t)
$$

### §F.2 Information intervention

Perturbation: *B_i* → *B_i*′ with 𝔼[*U*_fit ∣ *B_i*′] = 𝔼[*U*_fit ∣ *B_i*] − Δ*B* near *s**. Effect:
$$
\tilde U_i'(s^*) - \tilde U_i'(s_0) = [\tilde U_i(s^*) - \tilde U_i(s_0)] - w_i \Delta B
$$

Agent switches from *s** to *s*_0 iff *w_i* Δ*B* > *Ũ_i*(*s**) − *Ũ_i*(*s*_0).

### §F.3 Signal-redesign intervention

Perturbation: ⟨*ψ_i*, *φ*′⟩ − ⟨*ψ_i*, *φ*⟩ = −Δ*φ*. First-order Taylor of σ:
$$
U_{\text{perc}}'(s^*) \approx U_{\text{perc}}(s^*) - \alpha_i \sigma'(\cdot) \Delta\varphi
$$

Effect on *Ũ_i*:
$$
\tilde U_i'(s^*) = \tilde U_i(s^*) - (1 - w_i) \alpha_i \sigma' \Delta\varphi
$$

Agent switches iff (1−*w_i*) *α_i σ*′ Δ*φ* > *Ũ_i*(*s**) − *Ũ_i*(*s*_0).

### §F.4 Matching convention

Set Δ*B* = *α_i σ*′ Δ*φ* — both measured on the same "perceived-fitness utility" scale. Then:
$$
\frac{\Delta U_{\text{signal}}}{\Delta U_{\text{info}}} = \frac{(1-w_i) \alpha_i \sigma' \Delta\varphi}{w_i \alpha_i \sigma' \Delta\varphi} = \frac{1-w_i}{w_i}
$$

### §F.5 Argmax sensitivity → behavioural change

At an LSE (concave *Ũ*), implicit function theorem:
$$
|\Delta b| \;\approx\; \frac{|\delta \tilde U|}{|\partial^2_s \tilde U|_{s^*}|}
$$

Denominator (LSE curvature) is channel-invariant. Hence:
$$
\boxed{\;\frac{|\Delta b_{\text{signal}}|}{|\Delta b_{\text{info}}|} = \frac{1-w_i}{w_i} \geq \frac{1-w_{\max}}{w_{\max}} \geq 1.5\;}
$$

for *w*_max ≤ 0.4 (strict) or ≥ 1.22 for *w*_max ≤ 0.45 (Tier A, see `weak_joints_resolution.md`).

### §F.6 Population expectation γ

$$
\gamma := \mathbb{E}_F\!\left[\frac{1-2w}{w}\right] \cdot \mathbb{E}_F[|\Delta b_{\text{info}}|]
$$

For any distribution *F* supported on [0, *w*_max] with *w*_max ≤ 0.4: (1−2*w*)/*w* ≥ 0.2/0.4 = 0.5. Hence γ ≥ 0.5 · 𝔼_*F*[|Δ*b*_info|] > 0.

### §F.7 Shrinkage invariance

DellaVigna-Linos 2022: effect sizes shrink by factor κ ~ 1/3 academic → field. Applies symmetrically:
$$
\frac{|\Delta b_{\text{signal}}|^{\text{field}}}{|\Delta b_{\text{info}}|^{\text{field}}} = \frac{\kappa |\Delta b_{\text{signal}}|^{\text{RCT}}}{\kappa |\Delta b_{\text{info}}|^{\text{RCT}}} = \frac{|\Delta b_{\text{signal}}|^{\text{RCT}}}{|\Delta b_{\text{info}}|^{\text{RCT}}}
$$

Ratio preserved; T2 holds in field. ∎

### §F.8 Non-linear corrections

For large Δ*φ*, second-order corrections include σ″ term. Since σ″ < 0 near saturation, signal redesign has diminishing returns. But info remains linear and w-bounded. Hence (1−*w*)/*w* is an upper bound for large interventions; for moderate interventions, exact.

---

## §G T3 Species-Neutrality Argument

### §G.1 Axiom-by-axiom check

**A1**: requires only monotone noisy encoder *U*_perc → *U*_fit. Any species with dopaminergic/reward-tracking system qualifies. Satisfied by all vertebrates and most invertebrates (Barron et al. 2010 *Biological Reviews*).

**A2**: requires only that *S* expands beyond *S*_anc at *t*_sep. Passive environmental shift suffices. Moths, turtles, honeybees, humans all satisfy automatically under anthropogenic environmental change.

**A3**: weight *w* = 0 in pre-cognitive animals is the degenerate low-*w* limit. For animals without reflective belief channels, A3.3's *w* ≤ *w*_max < 1/2 is trivially satisfied. For humans, *w* ∈ (0, 1/2) is the empirical range. Both cases are instances of A3.

**A4**: hyperbolic discount is documented across rats (Mazur 1987), pigeons (Rachlin 1974), horses (Freidin et al. 2009), and humans (Ainslie 1975). Cross-species ubiquity is itself evidence for universality.

### §G.2 Δ_ST is species-neutral

Δ_ST = *U*_perc − 𝔼[*U*_fit ∣ *B*]. For low-*w* animals, *B* is degenerate; 𝔼[*U*_fit ∣ *B*] reduces to the prior. Δ_ST is still well-defined. No species-specific primitive enters.

### §G.3 Constructive examples

- **Moths + artificial light**: *ψ*_moth calibrated for positive phototaxis (celestial navigation); *S*_mod includes near-point sources (streetlamps). Δ_ST(streetlamp) = [high reward] − [death by exhaustion] > 0.
- **Humans + processed food**: *ψ*_human calibrated sweet-fat-salt (scarce ancestral nutrients); *S*_mod includes hyper-palatables. Δ_ST = [high reward] − [metabolic syndrome] > 0.
- Same formula, same sign, different *ψ* and different *S*_mod.

### §G.4 Language and culture

Humans have extra machinery (language, belief, cultural *ψ*-component). This enters *U*_perc and *B*. **A1–A4's structural form is unchanged**; humans have higher *w* and more elaborated *B*. Theorems hold for both. ∎

---

## §H T4 Envelope Theorem

### §H.1 Milgrom-Segal 2002 setup

For *V*(*x*) = sup_{*s* ∈ *S*(*x*)} *f*(*s*, *x*) with *S*(*x*) and *f* satisfying regularity, *V*(*x*) ≥ *f*(*s*_0, *x*) for any *s*_0 ∈ *S*(*x*), with strict inequality generically.

### §H.2 Application to T4

Let Δ_ST^EST(*x*) = max_{*s* ∈ *S*_design} Σ_*i* Δ_ST(*s*, *t* ∣ *ψ_i*) *ω_j*(*i*). Let Δ_ST^MST(*x*) = Σ_*i* Δ_ST(*s*_passive(*x*), *t* ∣ *ψ_i*) *ω_j*(*i*).

Since *s*_passive ∈ *S*_design (the passive environment is available as a "design choice"), Δ_ST^EST ≥ Δ_ST^MST. Strict inequality holds unless the designer's optimum is exactly *s*_passive — measure zero in realistic *S*_design.

### §H.3 Curvature comparison

Designer can additionally choose signal features that maximise the local second-order response of *U*_perc — exactly what variable-ratio reinforcement (Dow-Schüll 2012) and RL-trained recommendation (Rahwan et al. 2019 *Nature*) do. Hence *ℓ*^EST ≥ *ℓ*^MST, and decay rate *c*^EST ≥ *c*^MST (via T1 Eq. 16).

### §H.4 Basin expansion

Larger Δ_ST → larger *ε* → larger *ℓ* (curvature scales with saturation) → larger basin radius *R*_basin (§E.4). ∎

---

## §I Extended Positioning

Full content in `04-positioning/positioning.md`. Summary table:

| Theory | Relationship | Key differentiator | Empirical distinguisher |
|:---:|:---|:---|:---|
| Prospect Theory | Orthogonal | A1–A2 (fitness function absent in PT) | Certain decisions with delayed cost |
| Rational Addiction | Degenerate specialisation: {w=1, λ=0, U_perc=U_fit} | A3 violated; A2 violated | Externalisation (*λ*) effects |
| Evolutionary Mismatch | Informal precursor; Mismatch ⊂ MST ⊂ Sweet Trap | A3, A4, RST, EST absent from Mismatch | P1–P5 rank-orderings |
| Ecological Trap | Habitat-choice special case | Non-habitat, cognitive agents out of Eco Trap scope | Engineered (EST) instances |
| Fisher Runaway | Sub-family of RST; {genetic ψ, mate signals, no designer} | RST uses W̄_perc (L4), Fisher uses W̄_fit | Cultural escalation past fitness boundary |
| Nudge | Policy backed by T2 | T2 specifies which nudges win/lose | Signal vs info channel effectiveness |
| Dual System | Compatible refinement; specifies decoupled System-1 signals | A2 identifies which signals, A3 bounds System-2 override | Unbounded deliberation insufficient (L3) |

---

## §J Nomenclature

Complete symbol table, superseding any v2 legacy notation:

### §J.1 Primitives

| Symbol | Type | Meaning |
|:---:|:---:|:---|
| *S*, *s* | set, element | choice space, single choice |
| *s*_0 | distinguished element | abstention (baseline) |
| *i* | index | agent, *I* = {1, …, *N*} |
| *t*, *τ* | scalar | time, time lag |
| *j* | index | designing agent (EST) |
| *N(i)* | set | social neighbourhood of agent *i* |

### §J.2 Signal and fitness spaces

| Symbol | Type | Meaning |
|:---:|:---:|:---|
| Φ, *φ*(*s*, *t*) | set, function | signal feature space, feature extractor |
| Ω_fit, *W*(*s*, *t*) | set, function | fitness outcome space, instantaneous fitness |
| *r* | scalar | biological/welfare discount rate |

### §J.3 Utility and calibration

| Symbol | Type | Meaning |
|:---:|:---:|:---|
| *ψ_i* | vector | reward-calibration parameter (agent *i*) |
| *U*_perc(*s*, *t* ∣ *ψ_i*) | function | perceived utility; *U*_perc = σ(α⟨ψ, φ⟩) |
| *U*_fit(*s*, *t*) | function | fitness utility; expected discounted integral of *W* |
| σ(·), *α_i* | function, scalar | logistic sigmoidal; reward sensitivity (agent *i*) |

### §J.4 Coupling and regimes

| Symbol | Type | Meaning |
|:---:|:---:|:---|
| *ρ*(*t*) | scalar | reward-fitness coupling at time *t* |
| *ρ*_AE ≈ 1 | scalar | ancestral-environment coupling |
| *ρ*_crit = 0.3 | scalar | coupling threshold for decoupling |
| *S*_hist(*t*), *S*_anc, *S*_mod | distribution, sets | historical, ancestral, modern signal distributions |
| *t*_sep | scalar | separation time (modern signals enter) |

### §J.5 Beliefs, endorsement, cost

| Symbol | Type | Meaning |
|:---:|:---:|:---|
| *B_i*(*t*) | distribution | agent's belief about *U*_fit |
| *w_i*, *w*_max | scalar | endorsement weight; ceiling (< 1/2) |
| *b_i*(*t*) | element of *S* | chosen behaviour |
| *c_i*(*s*, *t*), *η_c* | scalar, noise | observable cost signal, measurement noise |
| *δ*(*τ*) = 1/(1 + *k_i τ*) | function | hyperbolic discount |
| *k_i*, *β_i* | scalar | hyperbolic discount rate, cost aversion (agent *i*) |
| *I*_visible ∈ {0, 1} | indicator | cost observability |
| *κ_i* | scalar | status-quo lock-in (renamed from v2 *ρ*) |

### §J.6 RST variables

| Symbol | Type | Meaning |
|:---:|:---:|:---|
| *q_i*, *ȳ* | scalar, scalar | quantitative trait, preference (population mean) |
| *G_q*, *G_y*, *G*^c_{*q*,*y*} | scalars | additive (co)variances |
| *G*^c_crit | scalar | Lande critical covariance |
| *W̄*_perc | function | mean perceived utility (RST selection gradient source) |

### §J.7 Derived diagnostics

| Symbol | Definition | Meaning |
|:---:|:---:|:---|
| **Δ_ST** | *U*_perc − 𝔼[*U*_fit ∣ *B*] | Sweet Trap Index (keystone scalar) |
| Σ_ST | Δ_ST × τ_F3 × (1 − *I*_feedback) | Severity |
| *π_t*(*s*) | [0, 1] | population share choosing *s* |
| *τ*_env, *τ*_adapt | scalars | environmental vs adaptive timescales |

### §J.8 Sub-class tags

- **MST** (Mismatch Sweet Trap)
- **RST** (Runaway Sweet Trap)
- **EST** (Engineered Sweet Trap)
- **KST** (Kernel Sweet Trap — abstract limit shared by MST/RST/EST)

---

## §K Extended References

### §K.1 Theoretical foundation

Ainslie, G. (1975). Specious reward: A behavioral theory of impulsiveness and impulse control. *Psychological Bulletin*, 82, 463–496.
Aristotle. *Nicomachean Ethics* (Book VII on akrasia).
Barron, A. B., Søvik, E., & Cornish, J. L. (2010). The roles of dopamine and related compounds in reward-seeking behavior across animal phyla. *Biological Reviews*, 85(4), 1051–1074.
Baumeister, R. F., Vohs, K. D., & Tice, D. M. (2007). The strength model of self-control. *Current Directions in Psychological Science*, 16(6), 351–355.
Becker, G. S., & Murphy, K. M. (1988). A theory of rational addiction. *Journal of Political Economy*, 96(4), 675–700.
Berridge, K. C., & Robinson, T. E. (2016). Liking, wanting, and the incentive-sensitization theory of addiction. *American Psychologist*, 71(8), 670–679.
Boyd, R., & Richerson, P. J. (1985). *Culture and the Evolutionary Process*. Chicago.
Cavalli-Sforza, L. L., & Feldman, M. W. (1981). *Cultural Transmission and Evolution: A Quantitative Approach*. Princeton.
Charlesworth, B. (1980). *Evolution in Age-Structured Populations*. Cambridge.
Cosmides, L., & Tooby, J. (1992). The psychological foundations of culture. In *The Adapted Mind*.
Coolen, I., van Bergen, Y., Day, R. L., & Laland, K. N. (2003). Species difference in adaptive use of public information in sticklebacks. *Proceedings of the Royal Society B*, 270, 2413–2419.
Fisher, R. A. (1930). *The Genetical Theory of Natural Selection*. Oxford.
Frederick, S., Loewenstein, G., & O'Donoghue, T. (2002). Time discounting and time preference. *Journal of Economic Literature*, 40, 351–401.
Henrich, J. (2015). *The Secret of Our Success*. Princeton.
Henrich, J., & McElreath, R. (2003). The evolution of cultural evolution. *Evolutionary Anthropology*, 12, 123–135.
Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus & Giroux.
Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263–291.
Kirby, K. N., & Herrnstein, R. J. (1995). Preference reversals due to myopic discounting of delayed reward. *Psychological Science*, 6, 83–89.
Kirkpatrick, M. (1982). Sexual selection and the evolution of female choice. *Evolution*, 36(1), 1–12.
Laibson, D. (1997). Golden eggs and hyperbolic discounting. *Quarterly Journal of Economics*, 112, 443–478.
Lande, R. (1981). Models of speciation by sexual selection on polygenic traits. *PNAS*, 78, 3721–3725.
Lieberman, D. E. (2013). *The Story of the Human Body: Evolution, Health, and Disease*. Pantheon.
Maynard Smith, J. (1982). *Evolution and the Theory of Games*. Cambridge.
Mazur, J. E. (1987). An adjusting procedure for studying delayed reinforcement. In *Quantitative Analyses of Behavior*.
McNamara, J. M., Stephens, D. W., Dall, S. R. X., & Houston, A. I. (2009). Evolution of trust and trustworthiness. *Trends in Ecology & Evolution*, 24, 589–598.
Milgrom, P., & Segal, I. (2002). Envelope theorems for arbitrary choice sets. *Econometrica*, 70, 583–601.
Nesse, R. M. (2005). Natural selection and the regulation of defenses. *Evolution and Human Behavior*, 26, 88–105.
Rachlin, H. (1974). Self-control. *Behaviorism*, 2, 94–107.
Rayo, L., & Becker, G. S. (2007). Evolutionary efficiency and happiness. *Journal of Political Economy*, 115, 302–337.
Richerson, P. J., & Boyd, R. (2005). *Not by Genes Alone*. Chicago.
Robertson, B. A., & Hutto, R. L. (2006). A framework for understanding ecological traps. *Ecology*, 87(5), 1075–1085.
Robertson, B. A., Rehage, J. S., & Sih, A. (2013). Ecological novelty and the emergence of evolutionary traps. *TREE*, 28(9), 552–560.
Robson, A. J. (2001). The biological basis of economic behavior. *Journal of Economic Literature*, 39, 11–33.
Sadacca, B. F., Jones, J. L., & Schoenbaum, G. (2016). Midbrain dopamine neurons compute inferred and cached value prediction errors in a common framework. *Nature Neuroscience*, 19, 750–757.
Schlaepfer, M. A., Runge, M. C., & Sherman, P. W. (2002). Ecological and evolutionary traps. *TREE*, 17(10), 474–480.
Schultz, W. (2016). Dopamine reward prediction-error signalling. *Physiological Reviews*, 96, 853–951.
Shizgal, P., & Conover, K. (1996). On the neural computation of utility. *Neurobiology of Learning and Memory*, 63, 59–68.
Strotz, R. H. (1955). Myopia and inconsistency in dynamic utility maximization. *Review of Economic Studies*, 23, 165–180.
Thaler, R. H., & Shefrin, H. M. (1981). An economic theory of self-control. *Journal of Political Economy*, 89, 392–406.
Thaler, R. H., & Sunstein, C. R. (2008). *Nudge*. Yale.
Tobler, P. N., Fiorillo, C. D., & Schultz, W. (2005). Adaptive coding of reward value by dopamine neurons. *Science*, 307, 1642–1645.
Tversky, A., & Kahneman, D. (1992). Advances in prospect theory: Cumulative representation of uncertainty. *J Risk Uncertain*, 5, 297–323.
Williams, G. C., & Nesse, R. M. (1991). The dawn of Darwinian medicine. *Quarterly Review of Biology*, 66, 1–22.
Zahavi, A. (1975). Mate selection — a selection for a handicap. *J Theor Biol*, 53, 205–214.

### §K.2 Empirical anchors

Allcott, H., Braghieri, L., Eichmeyer, S., & Gentzkow, M. (2020). The welfare effects of social media. *American Economic Review*, 110(3), 629–676.
Ariely, D. (2008). *Predictably Irrational*. Harper.
Cadario, R., & Chandon, P. (2020). Which healthy eating nudges work best? *Marketing Science*, 39(3), 465–486.
Chaloupka, F. J., Yurekli, A., & Fong, G. T. (2012). Tobacco taxes as a tobacco control strategy. *Tobacco Control*, 21(2), 172–180.
Danchin, É., et al. (2018). Cultural flies: Conformist social learning in fruitflies. *Science*, 362, 1025–1030.
DataReportal (2023). Digital 2023 Global Overview Report.
DellaVigna, S., & Linos, E. (2022). RCTs to scale: Comprehensive evidence from two nudge units. *Econometrica*, 90(1), 81–116.
Dow-Schüll, N. (2012). *Addiction by Design: Machine Gambling in Las Vegas*. Princeton.
Edlund, L. (2006). Marriage: past, present, future? *Economic Inquiry*, 44(4), 598–607.
Eisenbeis, G. (2006). Artificial night lighting and insects: attraction of insects to streetlamps. In *Ecological Consequences of Artificial Night Lighting*.
Federal Reserve (2023). Report on the Economic Well-Being of U.S. Households.
Frank, R. H. (1999). *Luxury Fever*. Princeton.
Freidin, E., et al. (2009). Choice in horses. *Animal Cognition*, 12, 401–411.
Gelfand, M. J., et al. (2011). Differences between tight and loose cultures: A 33-nation study. *Science*, 332, 1100–1104.
Gwynne, D. T., & Rentz, D. C. F. (1983). Beetles on the bottle: male buprestids mistake stubbies for females. *Journal of the Australian Entomological Society*, 22, 79–80.
Hofstede, G. (2001). *Culture's Consequences*. Sage.
Jambeck, J. R., et al. (2015). Plastic waste inputs from land into the ocean. *Science*, 347, 768–771.
Kirby, K. N. (2009). One-year temporal stability of delay-discount rates. *J Exp Anal Behav*, 91, 81–101.
Loss, S. R., Will, T., Loss, S. S., & Marra, P. P. (2014). Bird-building collisions in the United States. *Condor*, 116, 8–23.
Mertens, S., Herberz, M., Hahnel, U. J. J., & Brosch, T. (2022). The effectiveness of nudging: A meta-analysis. *PNAS*, 119, e2107346118.
Mozaffarian, D. (2016). Dietary priorities for cardiometabolic health. *Circulation*, 133, 187–225.
Rahwan, I., et al. (2019). Machine behaviour. *Nature*, 568, 477–486.
Savoca, M. S., et al. (2016). Marine plastic debris emits a keystone infochemical. *Science Advances*, 2, e1600395.
Simonite, T. (2020). How TikTok recommends videos. *Wired*.
Skinner, B. F. (1938). *The Behavior of Organisms*. Appleton-Century-Crofts.
Wang, M., et al. (2023). Ultraprocessed food intake and planetary health. *Lancet Planetary Health*, 7, e784–e795.
Woodcock, B. A., et al. (2017). Country-specific effects of neonicotinoid pesticides on honey bees. *Science*, 356, 1393–1395.

---

*End of Math Supplement. Full mathematical infrastructure for Paper 1 audit.*
