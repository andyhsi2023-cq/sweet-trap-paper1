# Expanded Proof Sketches — Sweet Trap Theory (Paper 1, Phase B)

**Document**: Audit-proof expanded proof sketches for T1 and T2 (core theorems)
**Status**: v1.0, 2026-04-18
**Companion**: `theorems.md`, `lemmas.md`, `weak_joints_resolution.md`

**Purpose**: This document provides the non-trivial algebra and constructions referenced in `theorems.md`'s compact proof sketches. Its target reader is a referee (applied mathematician or economist with dynamical-systems training) who wants to verify that the theorems are rigorous at the level of "the direction is clear and the missing steps are routine".

We expand:
- **§1**: T2 full algebra (the core theorem; Paper 2 depends on this).
- **§2**: T2 non-linear corrections (second-order terms in argmax sensitivity).
- **§3**: T1 Jacobian computation with logistic-sigmoid curvature.
- **§4**: T1 Lyapunov function construction.
- **§5**: T1 basin-of-attraction radius estimate.
- **§6**: T4 envelope-theorem application (Milgrom-Segal 2002).

---

## §1 T2 Full Algebra — Intervention Asymmetry

### §1.1 Setup

Agent *i* with parameters (*ψ_i*, *α_i*, *w_i*, *k_i*, *β_i*, *λ_i*). At an LSE *s**, the subjective valuation A3.1 is

$$
\tilde U_i(s, t) \;=\; (1 - w_i) U_{\text{perc}}(s, t \mid \psi_i) + w_i \, \mathbb{E}[U_{\text{fit}}(s, t) \mid B_i(t)] - C_i(s, t)
$$

where *C_i*(*s*, *t*) is the cost term (A3+A4.1), which we treat as fixed during the intervention comparison (both interventions preserve the cost channel).

Write *Ũ*_i(*s**) = max_*s* *Ũ*_i(*s*). An intervention perturbs the utility landscape; we measure the induced shift in argmax.

### §1.2 Information intervention

**Perturbation**: *B_i* → *B_i*′ such that 𝔼[*U*_fit ∣ *B_i*′] = 𝔼[*U*_fit ∣ *B_i*] − Δ*B* uniformly across *s* near *s**.

**Effect on *Ũ*_i**:

$$
\tilde U_i'(s, t) \;=\; (1 - w_i) U_{\text{perc}}(s, t \mid \psi_i) + w_i \cdot [\mathbb{E}[U_{\text{fit}} \mid B_i] - \Delta B] - C_i(s, t)
$$

$$
= \tilde U_i(s, t) - w_i \cdot \Delta B
$$

Note: if Δ*B* is **uniform** in *s*, it shifts all of *Ũ*_i by a constant and **does not change the argmax**. For a non-degenerate response, the perturbation must be *s*-differential: Δ*B*(*s*) = Δ*B* · *h_B*(*s*) where *h_B*(*s*) is the signed relevance of belief to choice *s*.

Without loss of generality, suppose *h_B* is concentrated at *s** (the belief update is specifically about *s**'s fitness). Then near *s**:

$$
\tilde U_i'(s^*) - \tilde U_i'(s_0) \;=\; [\tilde U_i(s^*) - \tilde U_i(s_0)] - w_i \cdot \Delta B
$$

The agent's choice shifts from *s** to *s*_0 iff the advantage flips sign, which requires

$$
w_i \cdot \Delta B \;>\; \tilde U_i(s^*) - \tilde U_i(s_0)
$$

i.e., Δ*B* > [*Ũ*_i(*s**) − *Ũ*_i(*s*_0)] / *w_i*.

### §1.3 Signal redesign intervention

**Perturbation**: *φ*(*s**, *t*) → *φ*′(*s**, *t*) with ⟨*ψ_i*, *φ*′⟩ − ⟨*ψ_i*, *φ*⟩ = −Δ*φ* < 0. This is a reduction in the perceptual "pull" of *s**.

**Effect on *U*_perc**:

$$
U_{\text{perc}}'(s^*) \;=\; \sigma(\alpha_i \cdot [\langle \psi_i, \varphi \rangle - \Delta\varphi]) \;\approx\; U_{\text{perc}}(s^*) - \alpha_i \sigma'(\langle \psi_i, \varphi \rangle) \cdot \Delta\varphi
$$

(first-order Taylor expansion).

**Effect on *Ũ*_i**:

$$
\tilde U_i'(s^*) \;=\; (1-w_i) \cdot [U_{\text{perc}}(s^*) - \alpha_i \sigma' \cdot \Delta\varphi] + w_i \cdot \mathbb{E}[U_{\text{fit}} \mid B_i] - C_i
$$

$$
= \tilde U_i(s^*) - (1-w_i) \cdot \alpha_i \sigma' \cdot \Delta\varphi
$$

The agent's choice shifts from *s** to *s*_0 iff

$$
(1-w_i) \cdot \alpha_i \sigma' \cdot \Delta\varphi \;>\; \tilde U_i(s^*) - \tilde U_i(s_0)
$$

i.e., Δ*φ* > [*Ũ*_i(*s**) − *Ũ*_i(*s*_0)] / [(1−*w_i*) *α_i σ*′].

### §1.4 Matching convention and the key ratio (Stage 1-B revision, F1)

To compare interventions fairly, we require **equal utility-input shock**: the same "one unit of utility" injected through either channel. The matching convention is now an **operational dose-matching criterion** (see T2.1.1 in `theorems.md`) rather than an abstract axiom.

Define the **normalised intervention magnitudes**:
- Info intervention: Δ*B* measured in units of *U*_fit (e.g., belief about fitness cost in standardised units).
- Signal intervention: Δ*φ* measured in units of *U*_perc directly (after multiplication by *α_i σ*′ to give a utility-comparable scalar).

Set: Δ*U*_info := *w_i* · Δ*B* (the utility-unit impact of info intervention through the *w* channel).
Set: Δ*U*_signal := (1−*w_i*) · *α_i σ*′ · Δ*φ* (the utility-unit impact of signal intervention through the 1−*w* channel).

**Matching convention (operational)**: We stipulate Δ*B* = *α_i σ*′ · Δ*φ* — both measured in the same "perceived-fitness utility" scale. This corresponds to the operational dose-matching described in T2.1.1: in a comparative RCT, Info arm and Signal arm are calibrated to produce equal *U*_perc-output shifts (measured pre-intervention on a standardised scale). This is the natural convention because Δ*B* is already in *U*_fit units and *α_i σ*′ · Δ*φ* is already in *U*_perc units, and at the LSE these are comparable via the Δ_ST wedge.

**Scope restriction (resolving apparent tension with L5)**: The convention and the ratio result are defined in the non-saturated regime where *σ*′(*α ψ φ*) ≥ *σ*′_min > 0. Sweet Trap scope requires Δ_ST > 0, not full saturation (*σ* = 1); L5's curvature analysis applies at *σ* ∈ [0.789, 1) where *σ*′ is small but strictly positive. The two are mutually compatible: both T2 and L5 apply in the high-but-not-full-saturation Sweet Trap regime. In the saturation limit *σ*′ → 0, both channels become marginally ineffective and T2's ratio is indeterminate (0/0 form) — T2 is not claimed to hold there.

Under this convention:

$$
\frac{\Delta U_{\text{signal}}}{\Delta U_{\text{info}}} \;=\; \frac{(1-w_i) \cdot \alpha_i \sigma' \cdot \Delta\varphi}{w_i \cdot \Delta B} \;=\; \frac{(1-w_i) \cdot \alpha_i \sigma' \cdot \Delta\varphi}{w_i \cdot \alpha_i \sigma' \cdot \Delta\varphi} \;=\; \frac{1-w_i}{w_i}
$$

Alternatively (if no matching convention is imposed, and both Δ*B* and Δ*φ* are "same raw magnitude" in their own units — simpler but coarser):

$$
\frac{\Delta U_{\text{signal}}}{\Delta U_{\text{info}}} \;=\; \frac{(1-w_i) \alpha_i \sigma'}{w_i}
$$

which also satisfies (1 − *w_i*)/*w_i* ≥ 1.5 when *α_i σ*′ ≥ 1 (which holds in the Sweet Trap regime since the reward sensitivity *α* is elevated).

### §1.5 Translation to behavioural change Δ*b*

At an LSE, the behavioural response to a small utility perturbation is governed by the **argmax sensitivity**. For a smooth *Ũ*_i with local negative curvature at *s** (the LSE condition), the implicit function theorem gives:

$$
|\Delta b| \;\approx\; \frac{|\delta \tilde U|}{|\partial^2_s \tilde U|_{s^*}|}
$$

where |*∂²_s Ũ*| is the local concavity of *Ũ*_i (the "restoring force"). This denominator is:
- Determined by the *second* derivative of *U*_perc (L5: ∂²*U*_perc/∂*s*² = *α*² *σ*″ *ψ*² (∂*φ*/∂*s*)² < 0 near saturation),
- **Invariant** to which channel (info or signal) the perturbation comes through (since both *B* and *φ* act on *Ũ*_i via separable additive terms).

Therefore the ratio |Δ*b*_signal|/|Δ*b*_info| equals the ratio of *first-order* utility shocks:

$$
\boxed{\frac{|\Delta b_{\text{signal}}|}{|\Delta b_{\text{info}}|} \;=\; \frac{|\delta \tilde U_{\text{signal}}|}{|\delta \tilde U_{\text{info}}|} \;=\; \frac{1-w_i}{w_i}}
$$

This is the **core identity** of T2. The inequality (1−*w_i*)/*w_i* ≥ (1−*w*_max)/*w*_max follows immediately from A3.3 with equality iff *w_i* = *w*_max.

### §1.6 Population expectation (γ)

Let *F* be the distribution of *w_i* across the population, with support ⊂ [0, *w*_max]. Define

$$
\gamma \;=\; \mathbb{E}_F\!\left[\frac{1-w}{w} - 1\right] \cdot \mathbb{E}_F[|\Delta b_{\text{info}}|] \;=\; \mathbb{E}_F\!\left[\frac{1 - 2w}{w}\right] \cdot \mathbb{E}_F[|\Delta b_{\text{info}}|]
$$

For any *F* supported on [0, *w*_max] with *w*_max ≤ 0.4:

$$
\frac{1 - 2w}{w} \;\geq\; \frac{1 - 2 \cdot 0.4}{0.4} \;=\; \frac{0.2}{0.4} \;=\; 0.5
$$

Hence γ ≥ 0.5 · 𝔼_*F*[|Δ*b*_info|] > 0. **This is the γ in T2's statement**.

### §1.7 Shrinkage invariance under symmetric-shrinkage assumption (Stage 1-B revision, M3)

DellaVigna & Linos 2022 document that **academic information-nudge RCT effect sizes shrink by factor *κ*_info ≈ 1/3 when scaled to field**. Let *κ*_signal denote the corresponding shrinkage for signal-redesign interventions.

$$
|\Delta b_{\text{info}}|^{\text{field}} \;=\; \kappa_{\text{info}} \cdot |\Delta b_{\text{info}}|^{\text{RCT}}, \qquad |\Delta b_{\text{signal}}|^{\text{field}} \;=\; \kappa_{\text{signal}} \cdot |\Delta b_{\text{signal}}|^{\text{RCT}}
$$

Therefore:

$$
\frac{|\Delta b_{\text{signal}}|^{\text{field}}}{|\Delta b_{\text{info}}|^{\text{field}}} \;=\; \frac{\kappa_{\text{signal}}}{\kappa_{\text{info}}} \cdot \frac{|\Delta b_{\text{signal}}|^{\text{RCT}}}{|\Delta b_{\text{info}}|^{\text{RCT}}}
$$

**Three regimes**:
- *κ*_signal = *κ*_info (symmetric shrinkage): ratio preserved; T2's dominance holds in field.
- *κ*_signal < *κ*_info (signal more fragile to field conditions): field ratio is smaller than RCT ratio; dominance weakens, though 1.5× lower bound may still hold if the reduction is modest.
- *κ*_signal > *κ*_info (info more fragile): field ratio exceeds RCT ratio; dominance strengthens.

**Empirical status**: *κ*_info ≈ 1/3 is well-documented (DellaVigna-Linos 2022). *κ*_signal is less extensively studied; Mertens et al. 2022 *PNAS* (choice architecture) reports effects broadly preserved in field, suggesting *κ*_signal ∈ [0.3, 0.8]. Under the **symmetric-shrinkage assumption** (*κ*_signal ≈ *κ*_info), the 1.5× field-ratio claim holds; this is the scope boundary we flag for empirical verification. Paper 2 v2.4's observed empirical ratio (1.4×–3.1×, centred ~2.0×) is broadly consistent with approximate symmetry.

T2 in its current form is **conditional on the symmetric-shrinkage assumption**; a Stage 2 empirical follow-up measuring *κ*_signal directly is recommended.

---

## §2 T2 Non-Linear Corrections

The first-order algebra in §1 gives the core ratio (1−*w*)/*w*. For larger interventions (non-infinitesimal Δ*B*, Δ*φ*), second-order corrections enter. Here we sketch them to show the dominance result is robust.

### §2.1 Second-order Taylor of *Ũ*_i

$$
\tilde U_i(s + \Delta s) \;\approx\; \tilde U_i(s) + \partial_s \tilde U_i \cdot \Delta s + \tfrac{1}{2} \partial^2_s \tilde U_i \cdot \Delta s^2
$$

At an LSE, ∂_*s Ũ*_i = 0. A perturbation (in *B* or *φ*) adds a first-order term:

$$
\tilde U_i'(s) \;=\; \tilde U_i(s) + \delta \tilde U_i(s)
$$

The new argmax *s*_new satisfies ∂_*s Ũ*_i′ = 0. After expansion:

$$
\Delta s \;=\; -\frac{\partial_s \delta \tilde U_i}{\partial^2_s \tilde U_i}\bigg|_{s^*} + \mathcal{O}(\Delta s^2)
$$

The numerator is the first-order *gradient* of the perturbation, while the denominator is the LSE concavity. For moderate perturbations (|Δ*s*| smaller than the basin radius), higher-order corrections are subleading.

### §2.2 Non-linearity in *σ*(·) (info channel)

The info perturbation enters *Ũ*_i linearly (through the *w_i* · 𝔼[*U*_fit ∣ *B*] term). There is no non-linearity on this channel beyond second-order Taylor.

### §2.3 Non-linearity in *σ*(·) (signal channel)

The signal perturbation enters *Ũ*_i through *U*_perc = *σ*(*α ⟨ψ, φ⟩*). For a large Δ*φ*, second-order corrections include:

$$
U_{\text{perc}}(s^*, \varphi - \Delta\varphi) \;=\; \sigma(\alpha \langle\psi, \varphi\rangle - \alpha \Delta\varphi \cdot \psi_{\parallel})
$$

Expanding *σ* around *α⟨ψ, φ⟩*:

$$
\approx \sigma - \alpha \Delta\varphi \psi_{\parallel} \sigma' + \tfrac{1}{2} (\alpha \Delta\varphi \psi_{\parallel})^2 \sigma''
$$

Since in the Sweet Trap regime *σ* is near saturation (*σ* close to 1), *σ*′ is small and *σ*″ < 0. The second-order correction is *negative* (|*U*_perc'| less than linear approximation would suggest). This means large signal redesign interventions have **diminishing returns** — which is intuitive: one can't push *U*_perc below 0.

### §2.4 Conclusion on non-linearity

- Info channel: linear in Δ*B*; no surprise.
- Signal channel: non-linear in Δ*φ*, with diminishing returns for large interventions.

This means the dominance ratio (1−*w*)/*w* is an **upper bound** for large interventions. For infinitesimal interventions the ratio is exact; for large interventions, signal effectiveness plateaus while info effectiveness remains linear. But since info is capped at *w* < 0.5, info's linear growth still cannot catch signal's bounded-but-large effect unless Δ*B* ≫ Δ*φ*.

**Conservative conclusion**: T2's result (1−*w*)/*w* is valid for moderate interventions; for very large interventions, signal redesign's diminishing returns require case-by-case analysis.

---

## §3 T1 Jacobian Computation

### §3.1 Dynamics equation (5.1) near LSE

At *s* = *s** (stationarity), the Jacobian is:

$$
J(s^*) \;=\; \frac{\partial}{\partial s} \left[\alpha_i \partial_s U_{\text{perc}} - \beta_i \delta(\tau) (1-\lambda_i) I_{\text{visible}} \partial_s U_{\text{fit}}\right]\bigg|_{s^*}
$$

$$
= \alpha_i \partial^2_s U_{\text{perc}}(s^*) - \beta_i \delta(\tau)(1-\lambda_i) I_{\text{visible}} \partial^2_s U_{\text{fit}}(s^*)
$$

### §3.2 Curvature of *U*_perc (from L5)

Near *s**, *U*_perc = *σ*(*α⟨ψ, φ(s)⟩*). Chain rule (with *f*(*s*) = ⟨*ψ*, *φ*(*s*)⟩):

$$
\partial_s U_{\text{perc}} \;=\; \sigma'(\alpha f) \cdot \alpha f'(s)
$$

$$
\partial^2_s U_{\text{perc}} \;=\; \sigma''(\alpha f) \cdot \alpha^2 f'(s)^2 + \sigma'(\alpha f) \cdot \alpha f''(s)
$$

The first term has *σ*″ < 0 in the saturation regime (*σ* > 1/2, rising to *σ* > 0.789 for |*σ*″| to be non-trivial — see L5). The second term is scaled by *σ*′ which is small at saturation.

Assuming *f*″ = 0 (linear feature extractor, a common simplifying assumption; relaxable) and *σ* near saturation:

$$
\partial^2_s U_{\text{perc}}(s^*) \;\approx\; -|\sigma''(\alpha f)| \alpha^2 f'^2 \;=\; -\ell(\psi, \varphi) \;<\; 0
$$

where *ℓ* = |*α² σ*″ *f*′²| > 0 is the curvature magnitude.

### §3.3 Curvature of *U*_fit

In the Sweet Trap regime, *U*_fit is *decreasing* in *s* near *s** (moving further into the trap loses fitness). The second derivative ∂²*U*_fit/∂*s*² is typically positive (the fitness loss rate decelerates as the agent moves deeper — diminishing sensitivity) or near zero.

In either case, the cost-term contribution to the Jacobian is attenuated by *δ*(*τ*)(1−*λ_i*)*I*_visible ≤ 1 and often ≪ 1 (due to hyperbolic discount, externalisation, or F4-invisibility).

### §3.4 Net Jacobian

$$
J(s^*) \;\approx\; -\alpha_i \ell(\psi_i, \varphi) + [\text{small positive term}] \;<\; 0
$$

(treating *s* as scalar; for vector *s*, *J* is a matrix and we require eigenvalues with negative real parts — same conclusion holds by the same argument applied componentwise).

### §3.5 Decay rate *c*

The linearised dynamics *d*(*s* − *s**)/*dt* = *J*(*s**)(*s* − *s**) decay exponentially with rate |*J*(*s**)| = −Re(λ_max(*J*)). From §3.4:

$$
c \;\geq\; \alpha_i \ell(\psi_i, \varphi) \cdot \varepsilon^2 - \beta_i \delta_{\max} M
$$

where the *ε*² factor reflects that larger Δ_ST (hence larger *ε*) produces a steeper attractor (the curvature *ℓ* scales with Δ_ST since larger wedge → more saturated *σ* → ... [detail in §5]).

---

## §4 T1 Lyapunov Function Construction

### §4.1 Candidate

$$
V(s, t) \;=\; \tfrac{1}{2} \|s - s^*\|^2 + \mu \cdot g(\Delta_{\text{ST}}(s, t))
$$

with *μ* > 0 small and *g*: ℝ → ℝ_+ smooth convex with *g*(0) = 0, *g*′(*x*) ≥ 0. For concreteness, take *g*(*x*) = *x*² for *x* ≥ 0, extended smoothly to *x* < 0.

### §4.2 Derivative along trajectories

$$
\dot V \;=\; (s - s^*) \cdot \dot s + \mu g'(\Delta_{\text{ST}}) \cdot \nabla_s \Delta_{\text{ST}} \cdot \dot s + \mu g'(\Delta_{\text{ST}}) \cdot \partial_t \Delta_{\text{ST}}
$$

At *s* near *s**:
- First term: (s - s*) · ds/dt. Using (5.1) and Taylor-expansion around *s**:

$$
(s - s^*) \cdot \dot s \;\approx\; (s - s^*) \cdot J(s^*)(s - s^*) \;=\; (s - s^*)^T J(s^*) (s - s^*)
$$

Since *J*(*s**) < 0 (§3.4), this is *negative* of order ≤ −*c* ||*s* − *s**||².

- Second term: small correction of order *μ*, can be bounded by the first-order Taylor of *g*′ near zero.
- Third term: ∂_*t* Δ_ST — a dynamic term capturing environmental evolution. Under the persistence assumption in T1.1 (Δ_ST ≥ *ε* for *t* ∈ [*t*_0, *t*_0 + *T*]), this term is bounded.

Combining and choosing *μ* small:

$$
\dot V \;\leq\; -c' \|s - s^*\|^2 \;\leq\; -c' \cdot 2V + \mathcal{O}(\mu)
$$

where *c*′ ≥ *c* (from §3.5) minus a small correction.

For *t* ∈ [*t*_0, *t*_0 + *T*] with *T* large enough:

$$
V(s(t)) \;\leq\; V(s(t_0)) \cdot e^{-c' (t - t_0)}
$$

This is Lyapunov exponential stability.

### §4.3 Conversion to norm bound

Since *V* = ||*s* − *s**||²/2 + (*μ* term), and the *μ* term is positive and bounded by a constant times *V*, we have ||*s* − *s**||² ≤ 2*V*. Hence:

$$
\|s(t) - s^*\|^2 \;\leq\; 2 V(s(t)) \;\leq\; 2 V(s(t_0)) \cdot e^{-c'(t-t_0)} \;=\; C \|s(t_0) - s^*\|^2 \cdot e^{-c'(t-t_0)}
$$

with *C* ≥ 1 a prefactor. This is the claim in T1.1.

---

## §5 T1 Basin of Attraction Radius — Scale Estimate (Stage 1-B revision, M5)

**Stage 1-B disclaimer**: The following is a **directional scale estimate** based on Taylor-expansion validity region heuristics. It is **not** a rigorous analytical bound on basin radius. The T4 basin-comparison claim (originally in T4.1) has been demoted to **Observation 4.1** (empirical regularity) because this section's analysis does not rise to the standard of a theorem proof. Formal analytical characterisation of basin radius as a function of Δ_ST and *ψ* is listed as future work.

### §5.1 Setup

The basin of attraction *U*(*s**) is the set of initial conditions *s*(*t*_0) from which the trajectory *s*(*t*) converges to *s** as *t* → ∞. For linearised dynamics, the basin is "local" in the sense of §4's ||*s* − *s**|| exponential bound.

### §5.2 Second-order Taylor validity

The linearised dynamics are valid where the second-order Taylor expansion of (5.1) around *s** is a good approximation. This breaks down when

$$
\|s - s^*\| \;\sim\; \frac{|\partial^2_s \dot s|}{|\partial^3_s \dot s|} \bigg|_{s^*}
$$

A scale estimate: using *σ*″ / *σ*‴ ratios (the next non-zero derivative of *U*_perc), the basin radius scales as

$$
R_{\text{basin}} \;\sim\; \frac{1}{\alpha} \cdot \frac{|\sigma''|_{\max}}{|\sigma'''|_{\max}}
$$

For logistic *σ*, |*σ*″|/|*σ*‴| is O(1) near the inflection point, which for Sweet Trap agents near saturation is not the relevant regime. Near saturation (*σ* → 1), both *σ*″ and *σ*‴ are small but their ratio is finite and bounded below by a constant.

### §5.3 Scaling with Δ_ST

For larger Δ_ST, the curvature *ℓ* (§3.2) scales roughly as Δ_ST (under strong calibration, *σ* is highly saturated when Δ_ST is large, and the near-saturation curvature is larger). Hence:

$$
R_{\text{basin}} \;\sim\; \frac{1}{\alpha} \cdot h(\Delta_{\text{ST}})
$$

with *h* an increasing function. Concretely: *R*_basin grows with Δ_ST.

### §5.4 Consequence for T4 (scale estimate, empirical observation rather than theorem)

Since Δ_ST^EST ≥ Δ_ST^MST (T4.1), the scale estimate above suggests *R*_basin^EST ≥ *R*_basin^MST. This is consistent with the empirical pattern in Observation 4.1 (EST exhibits longer behavioural persistence and larger relapse rates than MST). However, this §5 argument does not rise to a rigorous lower bound; it is reported as a directional scale estimate supporting Observation 4.1, not as proof of a set-containment theorem.

---

## §6 T4 Envelope Theorem Application

### §6.1 Milgrom-Segal 2002 setup

**Milgrom-Segal 2002 *Econometrica* 70:583** (Envelope theorem for arbitrary choice sets): If *V*(*x*) = sup_{*s* ∈ *S*(*x*)} *f*(*s*, *x*), and *S*(*x*) and *f* satisfy regularity, then *V*(*x*) ≥ *f*(*s*_0, *x*) for any *s*_0 ∈ *S*(*x*), with strict inequality generically (at points where the argmax is uniquely *s*(*x*) ≠ *s*_0).

### §6.2 Application to T4

Let *x* parametrise the "environment" and let *f*(*s*_design, *x*) = Σ_*i* Δ_ST(*s*_design, *t* ∣ *ψ_i*) · *ω_j*(*i*) be the designer's objective. Define:

- Δ_ST^EST(*x*) = max_{*s* ∈ *S*_design} Σ_*i* Δ_ST(*s*, *t* ∣ *ψ_i*) *ω_j*(*i*) (EST at parameter *x*).
- Δ_ST^MST(*x*) = Σ_*i* Δ_ST(*s*_passive(*x*), *t* ∣ *ψ_i*) *ω_j*(*i*) where *s*_passive is the environmental-shift point.

If *s*_passive ∈ *S*_design (passive environment is an available design), then Δ_ST^EST ≥ Δ_ST^MST by definition of maximum. Strict inequality holds unless the designer's optimal point is *exactly* the passive shift — a measure-zero case in any non-trivial *S*_design.

**∎**

### §6.3 Strictness conditions

Strict inequality fails only if:
- The designer's search space is *exactly* {*s*_passive} (no optimisation freedom).
- The designer's objective is exactly orthogonal to Δ_ST (*ω_j* = 0 or negative).

Neither holds in realistic applications (commercial platforms, gambling machines, algorithmic feeds all have rich *S*_design and *ω_j* positively correlated with Δ_ST).

---

## §7 Technical assumptions and remaining gaps

### §7.1 Smoothness

All proofs assume:
- *U*_perc, *U*_fit are smooth (at least *C*²) in *s* near the equilibrium.
- *φ*(*s*, *t*) is smooth in *s*.
- The noise term *ξ_i*(*t*) is Wiener.

For discrete *S* (§5.3 of axioms), these are replaced by soft-max approximations. The results extend with modified constants.

### §7.2 Unknown distribution of *w_i*

§1.6 gives γ ≥ 0.5 · 𝔼_*F*[|Δ*b*_info|] for any distribution *F* on [0, *w*_max]. A sharper γ requires parametric assumption. We do not commit to such an assumption; the qualitative conclusion (γ > 0) is robust.

### §7.3 Environmental persistence

T1 assumes Δ_ST ≥ *ε* persistently. Transient Sweet Traps (where the environmental shift reverses) produce LSEs that become saddles. This is realistic — many fads and fashions fade. Full treatment of non-persistent Sweet Trap dynamics requires a non-autonomous formulation (Δ_ST depends on *t* explicitly), which we handle as a perturbation of the autonomous case in T1.

### §7.4 Inter-agent interaction (RST coupling)

T1's analysis is single-agent. RST (§7.1 of axioms) introduces population-level coupling via cultural covariance *G_c*. The single-agent LSE persists **conditional on the population distribution being near its own equilibrium** — i.e., T1 is a local theorem in both (*s*, *ψ̄*) space. Global analysis of the joint (single-agent, population-average) system is the subject of Phase C's §03-predictions.

### §7.5 Fragile spots (for Phase C positioning)

Two spots in the proofs are robust in direction but weak in constants:

**Fragile #1**: T2's "matching convention" (§1.4) assumes Δ*B* and Δ*φ* can be measured in comparable utility units. In practice, empirical interventions differ in "intensity" by orders of magnitude in different ways. Paper 2 must specify the matching convention operationally; the theoretical dominance (1−*w*)/*w* is an *asymptotic* statement about the limit of well-matched intervention magnitudes.

**Fragile #2**: T4's basin-radius comparison (§5) scales with Δ_ST via a function *h*(Δ_ST) whose analytical form is only loosely characterised. A sharp quantitative basin expansion would require case-by-case analysis. The *directional* claim (basin expands with Δ_ST) is robust, but the *quantitative* claim requires more work.

These are noted for Phase C to frame as "theorem-level directional claim; quantitative refinement requires case study".

---

*End of expanded proof sketches document. Audit-proof algebra for T2 (§1), T1 Jacobian and Lyapunov (§3, §4), basin (§5), T4 envelope (§6). Technical gaps noted in §7.*
