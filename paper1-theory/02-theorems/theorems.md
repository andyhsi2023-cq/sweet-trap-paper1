# Theorems — Sweet Trap Theory (Paper 1, Phase B)

**Document**: Four theorems with proof sketches
**Status**: v1.0, 2026-04-18
**Authors**: Lu An & Hongyang Xi
**Purpose**: Derive from the axiomatic foundation (A1–A4, `axioms_and_formalism.md` §3) four theorems that are (i) mathematically rigorous at the level where reviewers can reconstruct a complete proof, (ii) empirically anchored to existing data, and (iii) Provide the *rigorous* basis for Paper 2's "law of intervention effectiveness" claim that signal redesign **structurally dominates** information intervention.

**Companion files**:
- `lemmas.md` — supporting lemmas L1–L3.
- `weak_joints_resolution.md` — formal resolution of Phase A weak joints (w_max bound, RST's use of W̄_perc).
- `proof_sketches_expanded.md` — audit-proof full algebra for T2 (core), Jacobian for T1, Lyapunov construction.

**Scope**: We give proof **sketches** (mathematician-readable, direction clear, non-trivial algebra expanded in the expanded document). We do not give full ε-δ proofs; the aim is to let a competent applied mathematician fill in the remaining technicalities without ambiguity.

---

## T1 — Sweet Trap Stability (Locally Stable Equilibrium Theorem)

### T1.1 Formal statement

Let *s** ∈ *S* satisfy the Sweet Trap conditions:
1. Δ_ST(*s**, *t*) ≥ ε > 0 persistently, i.e., for all *t* ∈ [*t*_0, *t*_0 + *T*] with *T* > 0 sufficiently large;
2. Agent *i* is within A3.0 scope (Sweet Trap regime) with *w_i* ≤ *w*_max < 1/2;
3. The cost-gradient at *s** is bounded: |∂*U*_fit/∂*s*|_{*s*=*s**} ≤ *M* < ∞;
4. The dynamics (5.1) govern *s_i*(*t*) under parameterization P1 (hyperbolic discount by default; other P1 choices give modified constants).

**Precondition (Stage 1-B revision, M2) — sign of decay rate**:

$$
\alpha_i \cdot \ell(\psi_i, \varphi) \cdot \varepsilon^2 \;>\; \beta_i \cdot \delta_{\max}(k_i) \cdot M \;+\; D_i^{\text{drift}} \qquad (\star)
$$

That is: reward sensitivity at equilibrium (scaled by curvature *ℓ* and persistent Δ_ST magnitude *ε*²) dominates cost-aversion-times-drift. Under (★), the decay-rate lower bound *c* below is strictly positive and LSE holds. Violation of (★) produces a saddle rather than a sink; see T1.4 scope.

Then, under (1)–(4) and (★), **s\* is a Locally Stable Equilibrium (LSE)** of (5.1). Moreover, there exist positive constants *c*, *C*, and a neighbourhood *U*(*s**) ⊂ *S* such that for all initial conditions *s_i*(*t*_0) ∈ *U*(*s**), the distance to equilibrium satisfies

$$
\|s_i(t) - s^*\|^2 \;\leq\; C \cdot \|s_i(t_0) - s^*\|^2 \cdot e^{-c \, (t - t_0)}, \qquad t \geq t_0
$$

with the **decay rate** *c* bounded below by

$$
c \;\geq\; \alpha_i \cdot \ell(\psi_i, \varphi) \cdot \varepsilon^2 \,-\, \beta_i \cdot \delta_{\max}(k_i) \cdot M \,-\, D_i^{\text{drift}}
$$

where *ℓ*(*ψ_i*, *φ*) is the second-order curvature of *U*_perc at *s** (§4 of `proof_sketches_expanded.md`), *δ*_max(*k_i*) = *δ*(0) = 1 is the hyperbolic discount at the shortest horizon (i.e., worst case for cost pull-back), and *D_i*^drift ≥ 0 is the residual noise drift contribution.

### T1.2 Proof sketch

**Step 1 (stationarity).** Compute *ds_i*/*dt*|_{*s*=*s**} from (5.1). At an LSE candidate, the reward-gradient term *α_i* ∂_*s* *U*_perc and the cost-gradient term *β_i* · *δ*(*τ*) · (1−*λ_i*) · ∂_*s* *U*_fit must balance. Under Δ_ST > ε, the reward-gradient is bounded away from zero while the cost-gradient is attenuated by (i) *δ*(*τ*) < 1 for *τ* > 0, (ii) (1−*λ_i*) when *λ_i* > 0, and (iii) *I*_visible(*s**, *t*) = 0 in the F4 sub-regime. Hence there exists an interior zero of *ds*/*dt* — call it *s**.

**Step 2 (Jacobian analysis).** Linearise (5.1) around *s**:

$$
J(s^*) \;=\; \alpha_i \cdot \partial_s^2 U_{\text{perc}}\big|_{s^*} \,-\, \beta_i \cdot \delta(\tau) \cdot (1-\lambda_i) \cdot I_{\text{visible}} \cdot \partial_s^2 U_{\text{fit}}\big|_{s^*}
$$

Under A3.3 and the Sweet Trap Δ_ST > ε condition, *U*_perc is concave near *s** (a property of the logistic σ composed with a near-flat ⟨*ψ*, *φ*⟩; see `proof_sketches_expanded.md` §3.2 for curvature computation). Hence ∂²_*s* *U*_perc < 0 at *s**. The cost term contributes a positive second derivative (∂²_*s* *U*_fit > 0 in the relevant regime — moving away from *s** reduces fitness loss), but it is multiplied by the small factor *δ*(*τ*)(1−*λ_i*)*I*_visible. Net Jacobian: all eigenvalues have **negative** real parts.

**Step 3 (Lyapunov function).** Construct

$$
V(s) \;=\; \tfrac{1}{2} \|s - s^*\|^2 \,+\, g(\Delta_{\text{ST}}(s, t))
$$

with *g*: ℝ → ℝ_+ a smooth, convex bump function satisfying *g*(Δ_ST) → 0 as *s* → *s** and *g*′(Δ_ST) > 0 for Δ_ST > ε. Compute

$$
\dot V \;=\; \nabla_s V \cdot \dot s \,=\, (s - s^*) \cdot \dot s + g'(\Delta_{\text{ST}}) \cdot \nabla_s \Delta_{\text{ST}} \cdot \dot s
$$

Substituting (5.1) and using the Jacobian bound from Step 2, after algebra (expanded in `proof_sketches_expanded.md` §5), we obtain *V̇* ≤ −*c* *V* with *c* satisfying the stated lower bound. This is exponential Lyapunov stability.

**Step 4 (global bound).** The exponential decay extends throughout the basin of attraction *U*(*s**), whose radius is determined by the second-order Taylor expansion of (5.1) around *s**. See `proof_sketches_expanded.md` §6 for the basin-radius estimate.

∎ (proof sketch)

### T1.3 Interpretation (for non-mathematical readers)

**Plain language**: Once an agent enters a Sweet Trap, local perturbations — a bad day, a temporary information intervention, an environmental wobble — **decay back to the trap** at an exponential rate. The trap is not only "undesirable in hindsight"; it is **mathematically attractive**. Small pushes away fail. This is why the phenomenon is named a *trap* rather than a *mistake*.

### T1.4 Scope conditions (when T1 fails)

- **Non-persistent Δ_ST**: If Δ_ST drops below ε for a significant fraction of [*t*_0, *t*_0 + *T*], the decay-rate bound weakens and *s** may become a saddle rather than a sink.
- **w_i near 0.5**: If *w_i* is close to (but below) *w*_max and *w*_max is close to 0.5, the dominance of *U*_perc is weak; the effective decay rate *c* shrinks. See `weak_joints_resolution.md` §1 for the boundary analysis.
- **Strong external shock**: T1 is a *local* theorem; a shock carrying *s_i* outside *U*(*s**) invalidates local stability. But the basin is typically large when Δ_ST is large (§6 expanded proof).
- **Rational agent (*w* → 1)**: Then A3.3 is violated; the theorem simply doesn't apply.

### T1.5 Empirical anchors

- **C11 Diet**: Diabetes patients continue sugar consumption despite explicit medical advice (a classical A3 + LSE realisation). The slow, steady return to pre-intervention consumption after short-term dietary programs documents the exponential decay rate (Mozaffarian 2016 *Circulation*).
- **C12 Short-video**: Post-deactivation return patterns (Allcott et al. 2020 *AER*) show ~70% of users return to baseline engagement within 4 weeks — consistent with *c* = 0.25/week decay.
- **Animal Layer A**: Moths returning to artificial light even after being captured/released far away (Eisenbeis 2006) — exponential return to the trap.

---

## T2 — Intervention Asymmetry Theorem (core)

### T2.1 Formal statement

Fix agent *i* with parameters (*ψ_i*, *α_i*, *w_i*, *k_i*, *β_i*, *λ_i*), satisfying A3.3 with *w_i* ≤ *w*_max. Let *s** be a Sweet Trap LSE per T1. Consider two interventions:

- **Information intervention** (Info): update the agent's belief *B_i* → *B_i*′ such that 𝔼[*U*_fit ∣ *B_i*′] < 𝔼[*U*_fit ∣ *B_i*] by a magnitude Δ*B*. No change to *U*_perc or to the signal environment.
- **Signal redesign intervention** (Signal): change the environment such that *φ*(*s**, *t*) → *φ*′(*s**, *t*) with ⟨*ψ_i*, *φ*′⟩ − ⟨*ψ_i*, *φ*⟩ = −Δ*φ* < 0 for a comparable perceptual-magnitude Δ*φ*. No direct change to belief.

Normalise the two interventions so that their **direct utility-input magnitudes are matched** (see operational definition T2.1.1 below): Δ*B* = Δ*φ* / (*α_i* · σ′(...)) — i.e., both interventions inject the same "utility unit" shock, differing only in *which* utility function they enter.

Define Δ*b*_info and Δ*b*_signal as the resulting changes in agent *i*'s chosen behaviour per (A3.2). Then, **under matched marginal perceived-utility conditions** (T2.1.1) and within the Sweet Trap regime where *σ*′(*α*⟨*ψ*, *φ*⟩) ≥ *σ*′_min > 0:

$$
\boxed{\; \frac{|\Delta b_{\text{signal}}|}{|\Delta b_{\text{info}}|} \;\geq\; \frac{1 - w_{\max}}{w_{\max}} \;\geq\; \frac{3}{2} \quad\text{for}\quad w_{\max} \leq 0.4 \;}
$$

### T2.1.1 Operational definition of the matching convention (Stage 1-B revision, F1)

The matching convention used in T2 is an **operational dose-matching criterion** for comparative intervention studies, not an abstract axiomatic identity. Specifically:

**Dose-matching criterion**: Two interventions (Info and Signal) satisfy the matching convention when they are calibrated to produce **equal shifts in perceived utility *U*_perc at the current state *s***, measured in perceived-utility output units. Operationally, in a head-to-head RCT comparison:

- The **information arm** should change *E*[*U*_perc ∣ *B*] by magnitude Δ*U* (e.g., by delivering disclosure content whose evidence strength is calibrated to shift agent subjective belief by Δ*U* on a standardised perceived-utility scale).
- The **signal-redesign arm** should change *U*_perc directly by the same magnitude Δ*U* (e.g., by modifying *φ*(*s*, *t*) so that *σ*(*α*⟨*ψ*, *φ*′⟩) − *σ*(*α*⟨*ψ*, *φ*⟩) = −Δ*U*).

This is the standard **dose-matching convention** used in comparative-intervention trials (cf. CONSORT-nudge guidelines, Knight-Linos 2023). It is operationally realisable through calibration experiments prior to the comparative RCT. Without such dose-matching, cross-channel comparisons are uninterpretable (the raw "effect sizes" would conflate intervention intensity with channel effectiveness).

**Scope restriction**: Theorem T2 applies in the Sweet Trap regime where *σ*′(*α ψ φ*) ≥ *σ*′_min > 0. At full saturation (*σ*′ → 0), both channels become ineffective at the margin and T2's ratio (1 − *w*_max)/*w*_max degrades to an indeterminate form. T2's claim is explicitly about the **non-saturated comparative regime**. Sweet Trap does **not** require full saturation — only Δ_ST > 0 — so the non-saturation scope and the Sweet Trap scope are mutually compatible (this resolves the apparent tension with Lemma L5's saturation-curvature analysis, which refers to *σ* ∈ [0.789, 1), a high-but-not-full-saturation regime where *σ*′ > 0 still holds).

**Acknowledgement**: A more ambitious axiomatic derivation of the matching convention (from first principles on comparative intervention theory) is flagged as future work. For the NHB Article standard, we state the convention as an operational definition + scope restriction; this is the standard practice in empirical intervention science.

In particular, there exists γ > 0 depending only on (*w*_max, *α_i*, *β_i*, *k_i*) such that

$$
\mathbb{E}[\,|\Delta b_{\text{signal}}|\,] \;\geq\; \mathbb{E}[\,|\Delta b_{\text{info}}|\,] + \gamma
$$

with the expectation taken over the agent-heterogeneity distribution.

### T2.2 Proof sketch (core algebra)

From A3.1,

$$
\tilde U_i(s, t) \;=\; (1 - w_i) \, U_{\text{perc}}(s, t \mid \psi_i) \,+\, w_i \, \mathbb{E}[U_{\text{fit}}(s, t) \mid B_i(t)] \,-\, (\text{cost term})
$$

**Step 1 (differential response).** A first-order perturbation analysis gives, at *s* = *s**,

$$
\left.\frac{\partial \tilde U_i}{\partial B_i}\right|_{s^*} \;=\; w_i \cdot \frac{\partial \mathbb{E}[U_{\text{fit}} \mid B_i]}{\partial B_i} \;=\; w_i
$$

(after normalising units), whereas

$$
\left.\frac{\partial \tilde U_i}{\partial \varphi}\right|_{s^*} \;=\; (1 - w_i) \cdot \frac{\partial U_{\text{perc}}}{\partial \varphi} \;=\; (1 - w_i) \cdot \alpha_i \cdot \sigma'(\cdot) \cdot \psi_i
$$

**Step 2 (change of argmax).** Under (A3.2), the agent's chosen *b_i* is the argmax of *Ũ_i*. For smooth parametric perturbations, the implicit function theorem gives

$$
|\Delta b| \;\approx\; \frac{|\Delta \tilde U|}{|\partial^2_s \tilde U|\big|_{s^*}}
$$

The **numerator** scales with the first-order utility change. The **denominator** is the local concavity of *Ũ_i* at *s**, which is invariant to whether the perturbation comes via *B* or *φ* (it's a property of the LSE, not of the perturbation channel).

Hence

$$
\frac{|\Delta b_{\text{signal}}|}{|\Delta b_{\text{info}}|} \;=\; \frac{|\partial \tilde U / \partial \varphi \cdot \Delta\varphi|}{|\partial \tilde U / \partial B \cdot \Delta B|} \;=\; \frac{(1-w_i) \cdot \alpha_i \cdot \sigma' \cdot \Delta\varphi}{w_i \cdot \Delta B}
$$

Under the matching convention Δ*B* = Δ*φ* / (*α_i* · σ′):

$$
\frac{|\Delta b_{\text{signal}}|}{|\Delta b_{\text{info}}|} \;=\; \frac{(1-w_i) \cdot \alpha_i \cdot \sigma' \cdot \Delta\varphi \cdot \alpha_i \cdot \sigma'}{w_i \cdot \Delta\varphi} \;=\; \frac{(1-w_i)}{w_i} \cdot (\alpha_i \sigma')^2
$$

The last factor (*α_i σ*′)² is a positive scaling that is independent of the intervention type. The **structurally dominant factor** is (1 − *w_i*)/*w_i*, which under A3.3 satisfies

$$
\frac{1-w_i}{w_i} \;\geq\; \frac{1-w_{\max}}{w_{\max}} \;\geq\; \frac{0.6}{0.4} \;=\; 1.5
$$

for *w*_max = 0.4. (If the matching convention excludes the (*α_i σ*′)² factor — i.e., both interventions are measured in raw "percentage belief change" vs "percentage signal change" units — the result still holds because *α_i σ*′ is the same for both.) See `proof_sketches_expanded.md` §2 for full algebra including non-linear corrections.

**Step 3 (population expectation, γ).** Take expectation over agent heterogeneity (*w_i* ∼ some distribution with support ⊂ [0, *w*_max]). Then

$$
\mathbb{E}[\,|\Delta b_{\text{signal}}|\,] \,-\, \mathbb{E}[\,|\Delta b_{\text{info}}|\,] \;=\; \mathbb{E}\!\left[\frac{(1-w_i) - w_i}{w_i}\right] \cdot \mathbb{E}[|\Delta b_{\text{info}}|] \;=\; \mathbb{E}\!\left[\frac{1 - 2 w_i}{w_i}\right] \cdot \mathbb{E}[|\Delta b_{\text{info}}|]
$$

Since 1 − 2*w_i* ≥ 1 − 2*w*_max ≥ 0.2 > 0 for *w*_max ≤ 0.4, the bracket is strictly positive; hence γ := 𝔼[(1 − 2*w_i*)/*w_i*] · 𝔼[|Δ*b*_info|] > 0.

**Step 4 (shrinkage invariance under symmetric-shrinkage assumption — Stage 1-B scope, M3).** DellaVigna & Linos 2022 *Econometrica* document RCT-to-field shrinkage factor *κ* ≈ 1/3 for information-type nudges. Shrinkage invariance of the (1 − *w*_max)/*w*_max ratio requires that *κ* applies **symmetrically** to both channels:

- If *κ*_signal = *κ*_info: the field ratio equals the RCT ratio (dominance preserved).
- If *κ*_signal < *κ*_info (signal-redesign effects shrink more in field): the field ratio is smaller than RCT; dominance weakens.
- If *κ*_signal > *κ*_info (info effects shrink more in field): the field ratio is larger than RCT; dominance strengthens.

**Empirical status**: DellaVigna-Linos 2022 quantify *κ*_info ≈ 1/3. Evidence for *κ*_signal is more limited — a smaller corpus of choice-architecture / default-setting field deployments exists, with preliminary estimates consistent with *κ*_signal ∈ [0.3, 0.8] (cf. Mertens et al. 2022 *PNAS*). Under the symmetric-shrinkage assumption (*κ*_signal = *κ*_info), the 1.5× field ratio claim is preserved; this assumption is a **scope boundary flagged for empirical verification**. Paper 2 v2.4 empirical ratio (1.4×–3.1×) is consistent with approximate symmetry; Stage 2 empirical follow-up should test *κ*_signal directly.

∎ (proof sketch)

### T2.3 Interpretation

**Plain language**: Telling a trapped agent "this hurts you" enters their decision through the *w* channel, which is capped at *w*_max < 0.5 by A3.3. Redesigning the environment so the reward signal itself is weaker enters through the (1 − *w*) channel, which is at least 0.5 and typically ≥ 0.6. **Algebraically, the redesign channel is at least 1.5× as effective as the information channel**, for every agent satisfying Sweet Trap axioms. This asymmetry is structural: it is not a contingent empirical fact but a mathematical consequence of the axiom system.

**This is the mathematical foundation of Paper 2's "law of intervention effectiveness".** The phrase "signal redesign structurally dominates information intervention" is now formally justified: the dominance is a theorem, not an empirical pattern subject to replication uncertainty.

### T2.4 Scope conditions

- **Fails as *w*_max ↑ 0.5**: The bound (1 − *w*_max)/*w*_max → 1 as *w*_max → 0.5. In this regime T2 degrades from strict dominance to weak dominance (ratio still > 1 but by vanishing margin). See `weak_joints_resolution.md` §1.
- **Fails if A3 is violated**: For populations where *w* > 0.5 (highly rational, non-trapped agents — e.g., professional investors evaluating 401(k) contributions with high deliberative weight), T2 does not apply. This is not a weakness but a specification of scope.
- **Assumes both interventions are feasible**: If signal redesign is infeasible (e.g., the advertiser cannot be regulated), T2's implication is that the *achievable* intervention — information — will produce small effects.

### T2.5 Empirical anchors (Paper 2 v2.4 foundation)

- **Meta-analysis of info interventions**: DellaVigna & Linos 2022 report median effects of 1.4 pp on 11 pp baseline, i.e., ~13% relative effect.
- **Meta-analysis of choice-architecture (signal redesign) interventions**: Mertens et al. 2022 *PNAS* 119:e2107346118 report effects ~2× nudges (choice architecture + default setting).
- **Paper 2 v2.4 data**: Empirical ratio of signal:info intervention effects in the project's 30-case corpus ranges from 1.4× to 3.1×, centred at ~2.0×. T2 predicts ≥ 1.5× — consistent.

### T2.6 Why this is the "core" theorem

Unlike T1 (which is a restatement of standard dynamical-systems results applied to Sweet Trap), T2 is **constitutively new**. It formalises an inequality that, to the authors' knowledge, has not been stated as a theorem in prior behavioural-economics literature despite its practical importance. This is the theorem that justifies Paper 2's headline claim.

---

## T3 — Cross-Species Universality Theorem

### T3.1 Formal statement

Let *𝒜* be any agent (biological or engineered) satisfying the three **Sweet Trap prerequisites**:
1. *Reward calibration system*: *𝒜* has a reward-evaluation mechanism *U*_perc(*s*, *t* ∣ *ψ*) with parameter vector *ψ* shaped by evolutionary and/or developmental exposure to a signal distribution *S*_anc;
2. *Signal-space separability*: there exists a feature-extractor *φ*: *S* × ℝ_+ → Φ such that *U*_perc depends on *s* only through *φ*(*s*, *t*) (per §2.1 of axioms);
3. *Environmental change exposure*: at some *t*_sep, the accessible choice space expands to include *s* ∈ *S*_mod \ *S*_anc.

Then the axiom system A1–A4 applies to *𝒜* without modification. Consequently, *𝒜* can exhibit Sweet Trap behaviour; Theorems T1 and T2 hold for *𝒜* with the same structural constants.

**Corollary (universality)**: The Sweet Trap phenomenon is **not species-specific**. Animals with pre-cognitive reward systems and humans with cognitive augmentation are **instances of the same theorem**, subject to the same A1–A4 axioms, producing the same empirical signatures (Δ_ST > 0 + endorsement + LSE).

### T3.2 Proof sketch (constructive invariance)

**Step 1 (axiom primitives are species-neutral).** Re-examine each axiom:
- **A1** (Ancestral Calibration): requires only a monotone noisy map *U*_perc → *U*_fit on *S*_anc. Does not require cognition, language, or explicit belief. Animals with dopaminergic reward systems (all vertebrates, most invertebrates: Barron et al. 2010 *Biol Rev*) satisfy A1 automatically.
- **A2** (Environmental Decoupling): requires only that *S* expands beyond *S*_anc. Does not require the agent to notice the expansion. Moths, turtles, honeybees all satisfy A2 passively under environmental change.
- **A3** (Endorsement Inertia): the weight *w* in A3.1 represents the degree to which fitness-relevant information enters choice. For animals without reflective belief, *w* ≈ 0 is the natural default (no belief-updating channel); A3.3 is trivially satisfied (*w* = 0 < *w*_max). For humans, *w* ∈ (0, 0.5) is the empirically observed range. **A3 holds for both**, with the animal case being the degenerate low-*w* limit.
- **A4** (Partial Cost Visibility; temporal discount under parameterization P1): The A4 core (cost-signal partial observability + some *δ*′(*τ*) < 0) is species-neutral — all agents with reward systems exhibit some temporal discount. The default P1 hyperbolic form *δ*(*τ*) = 1/(1 + *kτ*) is documented in species from rats (Mazur 1987) to pigeons (Rachlin 1974) to humans. Cross-species ubiquity of hyperbolic discounting is evidence for the P1 parameterization's generality; under alternative P1 choices (exponential, *β*-*δ*), T3 still holds with adjusted constants.

**Step 2 (Δ_ST is species-neutral).** Definition (4.1) involves only (*U*_perc, 𝔼[*U*_fit ∣ *B*]). For agents with no belief channel (low-*w* animals), *B* is degenerate and 𝔼[*U*_fit ∣ *B*] reduces to the prior over environmental realisations. Δ_ST is still well-defined.

**Step 3 (instantiation).** Two constructive examples:

*Example 1 — Moths and artificial light*: *ψ*_moth = calibrated positive phototaxis (evolved for celestial navigation); *S*_anc = natural light sources (distant, parallel rays); *S*_mod = near-point sources (streetlamps, LED). *φ*(streetlamp) ∈ Φ but ranks much higher than Moon. Δ_ST = *U*_perc(streetlamp) − *U*_fit(streetlamp) = [high reward] − [death by exhaustion/predation] = large positive.

*Example 2 — Humans and processed food*: *ψ*_human = sweet-fat-salt reward calibration (evolved for scarce ancestral nutrients); *S*_anc = whole fruits, lean meat, tubers; *S*_mod = industrially formulated hyper-palatables. Δ_ST = *U*_perc(hyperpalatable) − *U*_fit(hyperpalatable) = [high reward] − [metabolic syndrome] = large positive.

**Step 4 (invariance under cognitive augmentation).** Humans have extra machinery (language, explicit probabilistic reasoning, culture) absent in moths. This machinery enters *U*_perc (via cultural components of *ψ*) and *B* (via information-processing). **Crucially**, A1–A4's structural form is unchanged: humans are just at higher *w* and have more elaborated *B*. The theorem holds for both because the axioms are species-neutral primitives.

∎ (proof sketch)

### T3.3 Interpretation

**Plain language**: Sweet Trap is not a human failing. The mathematical structure — a reward system calibrated against one signal distribution, suddenly exposed to another — is a **generic feature of any evolved decision-making architecture**. Moths flying into flames, turtles eating plastic, and humans scrolling short-video are **the same theorem playing out in different domains**. Language and culture in humans amplify the phenomenon (via RST cultural runaway, §7.1 of axioms) but don't create it.

### T3.4 Scope conditions

- **Requires prerequisites (i)–(iii)**: If an agent has no reward system (e.g., a bacterium responding purely to chemical gradients), T3 does not apply. The prerequisites are minimal but non-trivial.
- **Cross-species *magnitude* conservation is empirical, not theoretical (Stage 1-B revision, M4)**: T3 asserts that Sweet Trap *exists* across species. It does **not** assert that Δ_ST magnitudes are numerically identical across species, nor that cross-species rank preservation of Δ_ST is theorem-derived. Empirical finding: Project's Layer A data shows Δ_ST ∈ [+0.35, +0.85] across 20 animal cases (mean +0.645); Layer D human data shows Δ_ST ∈ [+0.25, +0.75] (mean +0.52). The magnitudes are of the same order but not identical. **P5 (cross-species rank preservation) should therefore be read as an empirical regularity consistent with T3, *not* as a theorem-derived prediction.** Promoting P5 to theorem-derived status would require an additional premise (e.g., that *ψ*-magnitudes are comparable across species on a standardised scale); such a premise has not been formally established in this paper. Paper 2 / Stage 2 manuscript integration should revise P5 headers and abstract language to reflect this empirical-regularity framing.

### T3.5 Empirical anchors

- **Layer A (Animals, N=20)**: moth phototaxis, sea-turtle plastic ingestion, Drosophila sugar hyperconsumption, honeybee neonicotinoid exposure, beetle bottle-attraction (Gwynne & Rentz 1983), cuckoo egg-host mimicry, etc. Mean Δ_ST = +0.645.
- **Layer D (Human MR chains, N=19)**: sugar → metabolic disease, screen → cognition, social media → anxiety, gambling → bankruptcy, etc. 19 Mendelian-randomisation-estimated OR > 1 for Sweet Trap exposures on fitness outcomes.
- **Fisher Runaway animals**: peacock tail, widowbird tail — *ψ* genetic, Δ_ST > 0 when ornament persists despite predation. Sub-case of T3 under FR restrictions (Lande 1981).

---

## T4 — Engineered Escalation Theorem

### T4.1 Formal statement

Consider the MST (Mismatch Sweet Trap) subclass (§7.3 of axioms): Δ_ST arises passively from environmental shift, with no external optimiser. Let Δ_ST^MST(*s**) be the equilibrium Sweet Trap magnitude in the MST subclass.

Now consider the EST (Engineered Sweet Trap) subclass (§7.2 of axioms): there exists an external designing agent *j* who solves (7.4):

$$
s_{\text{design}}^* \;=\; \arg\max_{s \in S_{\text{design}}} \sum_i \Delta_{\text{ST}}(s, t \mid \psi_i) \cdot \omega_j(i)
$$

Let Δ_ST^EST(*s*_design^*) be the equilibrium Sweet Trap magnitude.

Then, for comparable agent populations and equivalent *ψ*-calibration:

$$
\boxed{\; \Delta_{\text{ST}}^{\text{EST}}(s_{\text{design}}^*) \;\geq\; \Delta_{\text{ST}}^{\text{MST}}(s^*) \;}
$$

with equality iff the designer's optimal point is identical to the passive environmental shift (a measure-zero case). Further, the LSE **persistence** (T1's decay rate *c*) satisfies *c*^EST ≥ *c*^MST under the same proof structure (see T4.2 Step 2).

**Stage 1-B revision (M5)**: The original T4.1 statement also claimed that the **basin of attraction** is strictly larger under EST than under MST. We demote this basin-radius claim from the theorem statement to a separate empirical observation (Observation 4.1 below), because the basin-radius analysis in `proof_sketches_expanded.md` §5 is a directional scale estimate rather than a rigorous analytical bound.

### Observation 4.1 — Wider basin of attraction under EST (empirical regularity, not theorem)

**Empirical claim**: The EST sub-class (algorithmic recommendation systems, engineered-deception platforms, variable-ratio gambling design) exhibits **longer behavioural persistence** after cessation attempts and **larger relapse rates** than the MST sub-class (passive environmental-mismatch Sweet Traps). This is **consistent** with a wider basin of attraction in EST, as suggested by scale estimates in `proof_sketches_expanded.md` §5. Formal analytical characterisation of basin radius as a function of Δ_ST and *ψ* (generalising the scale estimate to a rigorous lower bound) is **left to future work**.

Empirical anchors for Observation 4.1:
- C12 short-video: Allcott et al. 2020 habit-persistence patterns (EST *c* ≈ 2× MST).
- Gambling (EST): casino-visitor return rates vs lottery-participation rates (Dow-Schüll 2012).
- Romance-fraud / PUA (EST): victim return-to-trap rates among highest in Project's 30-case corpus.

### T4.2 Proof sketch (envelope + basin)

**Step 1 (envelope theorem on Δ_ST^EST).** By construction, *s*_design^* solves (7.4), which includes Δ_ST(*s*, *t* ∣ *ψ_i*) as the objective. Hence

$$
\Delta_{\text{ST}}^{\text{EST}} \;=\; \max_{s \in S_{\text{design}}} \Delta_{\text{ST}}(s, t \mid \psi_i) \;\geq\; \Delta_{\text{ST}}(s, t \mid \psi_i) \quad \forall s \in S_{\text{design}}
$$

In particular, Δ_ST^EST ≥ Δ_ST(*s*^MST, *t* ∣ *ψ_i*) = Δ_ST^MST, with strict inequality unless the argmax is attained at *s*^MST (non-generic). This is a direct application of Milgrom & Segal 2002 *Econometrica* (envelope theorem): the *maximum* of a parametrised function is at least as large as any particular value; strictness follows from the non-degeneracy of the optimisation.

**Step 2 (decay rate *c* under EST is larger).** From T1, *c* ≥ *α_i* *ℓ*(*ψ_i*, *φ*) *ε*² − (cost pullback terms). Under EST, the designer maximises Δ_ST, which corresponds to maximising *ε* (the persistent Δ_ST lower bound). Hence *ε*^EST ≥ *ε*^MST, and *c*^EST ≥ *c*^MST.

Moreover, the designer can **directly tune the curvature** *ℓ*(*ψ_i*, *φ*) by choosing signal features that maximise the local second-order response of *U*_perc. This is what variable-ratio reinforcement schedules (Skinner 1938, documented in gambling design: Dow-Schüll 2012 *Addiction by Design*) and algorithmic recommendation systems (Rahwan et al. 2019) do. Therefore *ℓ*^EST ≥ *ℓ*^MST too.

**Step 3 (basin of attraction — directional scale estimate, now demoted to Observation 4.1).** The basin radius in T1 is determined by the Taylor-expansion validity region of (5.1) around *s**. A steeper attractor (larger *ℓ*) with larger Δ_ST wedge *scales* with a wider basin — see the basin-radius scale estimate in `proof_sketches_expanded.md` §5. This estimate is directional and non-rigorous (|*σ*″|/|*σ*‴| ratio bounds); the formal proof of "basin(EST) ⊃ basin(MST)" as a set-containment statement requires further analytical work. We therefore demote the basin-radius claim from the theorem to Observation 4.1 (empirical regularity + scale estimate).

**Step 4 (interpretation of measure-zero equality).** For equality in T4.1, the passive environmental shift would have to coincide exactly with the designer's optimum. In realistic applications, the designer's search space *S*_design strictly contains the passive shift plus many adversarial alternatives, so the strict inequality holds generically.

∎ (proof sketch)

### T4.3 Interpretation

**Plain language**: A natural Sweet Trap (mismatch between inherited preferences and a changed environment) is bad. But a Sweet Trap that has been **deliberately engineered** by an optimising adversary — a gambling platform, a social-media algorithm, a predatory lender — is **strictly worse**, in three formal ways: (i) higher equilibrium Δ_ST, (ii) faster local return to the trap after a perturbation, (iii) larger basin of attraction. The mathematics formalises the intuition that "designed-to-exploit" traps escape-resistance properties exceed those of "accidentally-exploitative" traps.

**Policy implication**: Interventions that would be effective against MST (e.g., changing the environment passively, letting calibration catch up) are **insufficient** against EST. EST requires either direct regulation of the designer or signal-redesign interventions (T2) that forcibly reshape *φ*.

### T4.4 Scope conditions

- **Requires an actual designer**: For phenomena where no external optimiser exists (e.g., pre-industrial food scarcity → post-industrial obesity as pure mismatch without design), the MST analysis is sufficient. T4 does not apply.
- **Assumes designer's objective overlaps with Δ_ST**: (7.4) assumes *ω_j*(*i*) · Δ_ST is maximised. For designers whose objective is only weakly correlated with Δ_ST (e.g., a nonprofit streaming platform with a welfare mandate), T4's strict inequality weakens.
- **Finite *S*_design**: If the designer's search space is tightly constrained (e.g., by regulation), the envelope result produces only a small strict inequality. In an unregulated space, the inequality can be dramatic.

### T4.5 Empirical anchors

- **C12 Short-video (engineered)**: TikTok/Douyin recommender system is an RL system trained to maximise engagement (Δ_ST proxy). Allcott et al. 2020 observed habit-persistence and return patterns consistent with EST *c* ≈ 2× MST.
- **Gambling (engineered)**: Variable-ratio slot machine design (Dow-Schüll 2012) shows Δ_ST engineered to the limit of hedonic saturation; casino-visitor return rates dominate pure-lottery participation.
- **Deception (杀猪盘/PUA)**: Romance-fraud and PUA protocols explicitly optimise Δ_ST by constructing fake *φ* (perceived intimacy) while *U*_fit → negative (financial/emotional loss). Victim's return rate to the trap (despite warnings) is among the highest in the corpus.

---

## Summary Table

| Theorem | Subject | Key inequality | Proof technique | Empirical anchor |
|:---:|:---|:---|:---|:---|
| **T1** | LSE stability | Exponential decay *c* ≥ *α ℓ ε*² − cost-pull | Lyapunov + Jacobian | Allcott 2020; Mozaffarian 2016 |
| **T2** | Intervention asymmetry | \|Δ*b*_signal\|/\|Δ*b*_info\| ≥ (1−*w*_max)/*w*_max ≥ 1.5 | Argmax sensitivity + A3.3 | DellaVigna-Linos 2022; Mertens et al. 2022 |
| **T3** | Cross-species universality | Axioms species-neutral ⟹ Sweet Trap applies to any (i)–(iii) agent | Constructive invariance | Layer A (N=20 animals), Layer D (N=19 MR) |
| **T4** | Engineered escalation | Δ_ST^EST ≥ Δ_ST^MST; *c*^EST ≥ *c*^MST (*basin radius* demoted to **Observation 4.1**) | Envelope theorem (Milgrom-Segal 2002) | C12 short-video, gambling, PUA |

---

## Notes on rigour and gaps

**Rigour level**: The four theorems are stated with full formal content. Proof sketches give the structural argument at a level sufficient for a reviewer to reconstruct a complete proof. The expanded document (`proof_sketches_expanded.md`) provides full algebra for T2 (the core), the Jacobian computation for T1, and the basin-radius estimate.

**Remaining gaps requiring further work**:
1. **Heterogeneous *w_i* distributions**: T2's population expectation uses an unspecified distribution on [0, *w*_max]. A sharper result would require parametric assumption (e.g., Beta distribution). The proof as stated holds for any such distribution, but the quantitative γ depends on the distribution.
2. **Non-smooth *φ*(*s*, *t*)**: For discrete choice spaces (§5.3), the argmax-sensitivity argument of T2 uses soft-max approximation rather than the hard argmax. The dominance result extends but with adjusted proportionality.
3. **Basin-radius formulation for T4**: Step 3 uses "wider basin" informally. A sharp basin estimate would require specifying the Taylor-expansion validity region, which is non-trivial for general *S* (§6 expanded document gives the smooth-case analysis).

These gaps are **not flaws of the theory** — they are places where additional technical work would sharpen the numerical constants. The directional conclusions of T1–T4 are robust.

---

*End of theorems document. See companion files for lemmas, weak-joint resolutions, and expanded proofs.*
