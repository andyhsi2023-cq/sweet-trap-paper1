# Sweet Trap Theory: An Axiomatic Framework for Reward–Fitness Decoupling in Evolved Decision Systems

**Paper 1 — Theoretical Foundation**
**Authors**: Lu An, Hongyang Xi
**Target level**: Kahneman-Tversky 1979 *Econometrica* (Prospect Theory) — theoretical piece with formal axiom system, central theorems, falsifiable predictions, and minimal experimental paradigm.
**Status**: v1.0 draft, 2026-04-18
**Word count (main text, target ≤ 6000)**: ~5,950 (excluding references and Math Supplement)

**Section targets**:
- Abstract: 250
- Introduction: 800
- The Theory: 2,500
- Main Theorems: 1,000
- Falsifiable Predictions: 500
- Relationship to Existing Frameworks: 500
- Discussion: 700

---

## Abstract (250 words)

A moth flies into a flame. A sea turtle eats a plastic bag. A human endorses a behaviour that their doctor, their family, and they themselves acknowledge is bad for them, and continues anyway. These are not three different phenomena. They are one phenomenon, which we call the Sweet Trap: **a persistent choice, endorsed by the agent, in which the reward signal driving the choice has decoupled from the fitness consequence it evolved to track**. We develop an axiomatic theory that formalises this phenomenon for any evolved decision-making architecture — biological or engineered — whose reward system was calibrated against one signal distribution and now faces another. Four axioms suffice: ancestral calibration, environmental decoupling, endorsement inertia, and partial cost visibility with hyperbolic discount. From these we derive four theorems: a stability theorem establishing that Sweet Traps are locally attractive equilibria; an intervention-asymmetry theorem establishing that signal-redesign interventions structurally dominate information interventions by a factor of at least (1 − *w*_max)/*w*_max ≥ 1.5 for any agent satisfying the axioms; a cross-species universality theorem establishing that moths, turtles, and humans are instances of the same phenomenon; and an engineered-escalation theorem establishing that adversarially designed traps are strictly worse than naturally emerging ones. We state five falsifiable predictions: one (cross-species mechanism-rank preservation) is strongly supported by a pre-registered cross-layer meta-regression (β = +1.58, p = 0.019); one (intervention asymmetry) is qualitatively corroborated across six independently-compiled domains with a harmonised-scale mini-meta pending; one (cultural amplification) is partially supported (joint-predictor R² = 0.255 across 25 ISSP countries, above the ≥ 0.15 falsification floor but below the ≥ 0.40 target); and two (persistence–severity monotonicity; engineered escalation) await empirical test with motivating anchors. We also specify a minimal experimental paradigm (n < 500 per arm on Prolific) that could refute the core intervention-asymmetry law in a single controlled study. The theory unifies evolutionary mismatch, ecological traps, Fisher runaway, and algorithmic manipulation under a single mathematical framework, while remaining orthogonal to prospect theory and sharper than bounded-rationality accounts.

**Keywords**: evolutionary mismatch; reward–fitness decoupling; engineered environments; behavioural dynamics; intervention asymmetry.

---

## 1. Introduction (800 words)

Every year, millions of migratory birds die in collisions with glass façades whose reflections perfectly mimic sky and forest. In the United States alone, the estimated toll is **365 million to 1 billion** avian deaths annually (Loss et al. 2014 *Condor*). The birds' visual systems — honed by millions of years of selection against actual predators and actual trees — register glass as navigable space. They die, and their children's visual systems are no better calibrated than their own.

That same year, an estimated **8 million tonnes** of plastic enter the oceans (Jambeck et al. 2015 *Science*). Sea turtles, whose olfactory apparatus evolved to track the chemical signature of jellyfish and crustacean prey, attend to plastic bags whose surface microbial communities produce identical olfactory cues (Savoca et al. 2016 *Sci Adv*). They eat the bags and die.

And that same year, adult humans in the United States spent a median **4.8 hours per day** on mobile devices (DataReportal 2023), consumed **17 teaspoons** of added sugar daily (Wang et al. 2023 *Lancet Planet Health*), and carried a median consumer debt of **$5,910** (Federal Reserve 2023). They did these things despite being individually, often articulately, aware that the behaviour was harming their health, their finances, or their relationships.

The three phenomena have been studied under different names — ecological trap, evolutionary mismatch, akrasia, addiction, rational-irrationality, dual-system failure, nudgeable bias — and by different disciplines. We propose that they are expressions of a single underlying regularity: **the decoupling of reward signals from fitness consequences, sustained by endorsement, in agents whose reward system was calibrated against a signal distribution that no longer matches their current environment**. We call this the **Sweet Trap**.

The name captures three features simultaneously: the agent experiences the choice as sweet (high perceived reward); the agent's behavioural trajectory is trapped (choice is persistent, locally stable, and hard to reverse); and the reward signal is sweetness-like in the technical sense — it was once a reliable indicator of fitness and has ceased to be. This paper provides an axiomatic formalisation of the Sweet Trap and derives its core consequences.

**Why a new theory, and why now?** Three arguments.

First, existing frameworks each capture one or two features but none captures all of them formally. Evolutionary mismatch (Williams-Nesse 1991; Lieberman 2013) captures the reward–fitness decoupling but has no formal decision rule or dynamics. Ecological trap (Robertson-Hutto 2006) captures the trap feature but only for habitat choice in non-cognitive agents. Rational addiction (Becker-Murphy 1988) has dynamics but assumes the agent's preferences and welfare are aligned — foreclosing Sweet Trap by axiom. Prospect theory (Kahneman-Tversky 1979) formalises subjective valuation but has no fitness function. Nudge theory (Thaler-Sunstein 2008) is a policy practice without a predictive theoretical engine. A unified formal framework has been missing.

Second, the **empirical signal has accumulated to the point where a formal theory is both possible and necessary**. The behavioural-economics revealed-preference literature (DellaVigna-Linos 2022 *Econometrica*), the choice-architecture meta-analyses (Mertens et al. 2022 *PNAS*), and the cross-species comparative data (Robertson et al. 2013 *Oikos*; this project's Paper 2 v2.4 compilation of 20 animal + 19 human-MR cases) all converge on patterns that require explanation beyond individual theories.

Third, the **modern environment is changing faster than reward systems can recalibrate**. Variable-ratio slot machines, algorithmic video feeds, hyper-palatable processed foods, and platform-mediated romantic scams are not accidents of environmental shift — they are adversarial engineering of the reward–fitness gap. A theory that cannot distinguish Mismatch Sweet Traps (passive environmental decoupling) from Engineered Sweet Traps (adversarial decoupling) misses what is most distinctive and urgent about contemporary behavioural ecology.

**This paper's contribution.** We present an axiomatic foundation (A1–A4), a central scalar Δ_ST that measures the reward–fitness wedge, and four theorems (T1–T4) that follow from the axioms. Theorem T2 — the **intervention asymmetry law** — is the analytical heart: it establishes that signal-redesign interventions dominate information interventions by a factor of at least 1.5 for any agent satisfying the axioms, a result that emerges directly from the endorsement-weight bound in A3 and is **shrinkage-invariant** (preserved under the ~3× academic-to-field effect-size shrinkage documented by DellaVigna-Linos). The theorem formalises what behavioural-economics practitioners have learned empirically: you cannot inform people out of Sweet Traps; you must redesign the signal environment.

The paper proceeds as follows. Section 2 introduces the theoretical primitives, axioms, and sub-classes. Section 3 states the four central theorems. Section 4 derives five falsifiable predictions from the theorems, with their current empirical status. Section 5 positions Sweet Trap Theory relative to seven adjacent frameworks. Section 6 discusses scope, limitations, and a minimal experimental paradigm that could falsify the core law in a single controlled study. Full proofs are in the Math Supplement.

---

## 2. The Theory (2,500 words)

### 2.1 Primitives

Let *S* be a measurable space — the **choice space** of admissible actions, states, or signal exposures. *S* may be discrete (cups of sugared drink per day), continuous (daily screen-time minutes), or symbolic (available consumer goods in a culture). A distinguished element *s*_0 ∈ *S* denotes **abstention** (no engagement, baseline). Agents are indexed *i* ∈ *I* = {1, …, *N*}; time *t* ∈ ℝ_+.

Each choice *s* at time *t* admits two utility evaluations, and **the central formal commitment of Sweet Trap Theory is that these two utilities can diverge**:

**Perceived utility** (what the agent's reward system assigns):
$$
U_{\text{perc}}(s, t \mid \psi_i) \;=\; \sigma\!\bigl(\alpha_i \cdot \langle \psi_i, \varphi(s, t) \rangle\bigr)
\qquad (1)
$$

where *σ* is the logistic sigmoid, *φ*: *S* × ℝ_+ → Φ maps choices into a feature space accessible to the agent's perceptual apparatus, *ψ_i* ∈ ℝ^*k* is the agent's reward-calibration parameter vector (genetic + developmental + cultural components), and *α_i* > 0 is reward sensitivity. The logistic form is committed (Modeling Commitment 2 in Math Supplement §A), anchored in the saturation properties of vertebrate and invertebrate dopaminergic reward circuits (Schultz 2016 *Physiol Rev*; Tobler et al. 2005 *Science*).

**Fitness utility** (what the choice actually delivers):
$$
U_{\text{fit}}(s, t) \;=\; \mathbb{E}\!\left[\int_t^\infty e^{-r(\tau - t)}\, W(s, \tau)\, d\tau\right]
\qquad (2)
$$

the expected discounted integral of future instantaneous fitness contribution *W*(*s*, *τ*). *U*_fit is an **objective** quantity — not conditional on the agent's beliefs — against which the agent's *U*_perc will be compared.

The **coupling** between the two utilities over the historical signal distribution *S*_hist(*t*) is:
$$
\rho(t) \;=\; \operatorname*{Corr}_{s \sim S_{\text{hist}}(t)}\!\bigl[U_{\text{perc}}(s, t \mid \psi), \; U_{\text{fit}}(s, t)\bigr]
\qquad (3)
$$

Well-calibrated reward systems have *ρ* ≈ 1; Sweet Trap domains have *ρ* < *ρ*_crit ≈ 0.3.

### 2.2 Axioms

Four axioms suffice. Each is stated formally; informal statements follow each.

**Axiom A1 (Ancestral Calibration).** There exists a strictly monotone-increasing continuous function *h*: ℝ → ℝ such that for all *s* ∈ *S*_anc and *t* < *t*_sep,
$$
U_{\text{perc}}(s, t \mid \psi) \;=\; h\!\bigl(U_{\text{fit}}(s, t)\bigr) + \varepsilon(s, t)
\qquad (4)
$$
with calibration noise *ε* of mean zero and variance much smaller than Var[*U*_fit] on *S*_anc.

*Informally*: in the ancestral regime, the reward system is a noisy but monotone encoder of fitness.

**Axiom A2 (Environmental Decoupling).** There exists *t*_sep and *ρ*_crit ∈ (0, 1) such that
$$
\forall\, s \in S_{\text{mod}} \setminus S_{\text{anc}},\; \forall\, t > t_{\text{sep}}: \quad \rho(s, t) \,<\, \rho_{\text{crit}}
\qquad (5)
$$

*Informally*: specific signals enter the agent's choice space that the reward system was not calibrated to evaluate.

Two routes to A2 coexist. **Route A (mismatch)** — environment shifts faster than *ψ* adapts (sugar, artificial light, processed food). **Route B (supernormal/novel signals)** — signals with no ancestral referent piggyback on general-purpose reward architecture (direct electrode stimulation, variable-ratio reinforcement schedules, algorithmic engagement feeds).

**Axiom A3 (Endorsement Inertia).** The agent's subjective valuation combines perceived utility and belief about fitness, with a *structurally bounded* weight on belief:
$$
\tilde U_i(s, t) \;=\; (1 - w_i)\, U_{\text{perc}}(s, t \mid \psi_i) + w_i\, \mathbb{E}[U_{\text{fit}}(s, t) \mid B_i(t)]
\qquad (6)
$$
with the choice rule *b_i*(*t*) = argmax_{*s*} *Ũ_i*(*s*, *t*), and the boundedness constraint
$$
\exists\, w_{\max} < \tfrac{1}{2}: \quad w_i \leq w_{\max} \text{ for all } i.
\qquad (7)
$$

*Informally*: agents do attend to beliefs about fitness, but they do so with less weight than they attend to perceived utility — hence the choice is dominated by (1 − *w_i*) > *w_i*.

The theoretical default is *w*_max = 0.4. Revealed-preference estimates in health-behaviour domains (smoking despite known mortality: Chaloupka et al. 2012 *Tobacco Control*) yield effective *w* ∈ [0.15, 0.35], well within the bound.

A3's scope excludes (i) coerced exposure (non-reward constraints force choice; e.g., 996 overtime work is *not* a Sweet Trap); (ii) acute clinical compulsion at DSM-5 threshold. These are distinct phenomena that may coexist with but are not identical to Sweet Traps.

**Axiom A4 (Partial Cost Visibility with Hyperbolic Discount).** Observable cost signal:
$$
c_i(s, t) \;=\; [U_{\text{fit}}(s_0, t) - U_{\text{fit}}(s, t)] \cdot I_{\text{visible}}(s, t) + \eta_c
\qquad (8)
$$
where *I*_visible ∈ {0, 1} and *η_c* is cost-measurement noise. Effective cost at horizon *τ*:
$$
c_{\text{eff}}(s, t; \tau) \;=\; \delta(\tau) \cdot c_i(s, t), \quad \delta(\tau) = \frac{1}{1 + k_i \, \tau}
\qquad (9)
$$

*Informally*: costs are observable only partially (many cumulate invisibly) and are hyperbolically discounted — the future cost of today's choice enters decision weakly. Hyperbolic *δ* is committed (not quasi-hyperbolic *β*-*δ*) based on empirical fit (Ainslie 1975 *Psychol Bull*) and behavioural-ecology congruence (McNamara et al. 2009 *TREE*).

### 2.3 The Sweet Trap Index Δ_ST

The keystone scalar of the theory:
$$
\boxed{\;\Delta_{\text{ST}}(s, t \mid \psi, B) \;=\; U_{\text{perc}}(s, t \mid \psi) \,-\, \mathbb{E}[U_{\text{fit}}(s, t) \mid B]\;}
\qquad (10)
$$

A **Sweet Trap realisation** is:
$$
\text{SweetTrap}(s, t) \iff \Delta_{\text{ST}}(s, t) > 0 \wedge \text{chose}(s) \text{ under } (6)
\qquad (11)
$$

That is: a positive reward–fitness wedge *and* endorsement. Both conditions are necessary. An agent with Δ_ST > 0 who does not choose the signal (e.g., because of a coercive intervention) is not in a Sweet Trap. An agent who chooses a signal with Δ_ST ≤ 0 (no reward–fitness wedge) is not in a Sweet Trap — they are making an ordinary rational choice.

The individual-level Δ_ST in (10) connects to a population-level **coupling drop** Δ_ST ∝ (*ρ*_AE − *ρ*(*t*)) via correlation properties of (1)–(3); see Math Supplement §B.

Δ_ST has three properties that make it the empirical core of the theory:

**Property 2.1 (sign)**: Under A1 on *S*_anc with *t* < *t*_sep, 𝔼[Δ_ST] ≈ 0. Under A2 on *S*_mod \ *S*_anc with *t* > *t*_sep, Δ_ST > 0 for signals *s* where the reward system is miscalibrated.

**Property 2.2 (magnitude–persistence)**: Behavioural persistence (the Lyapunov decay rate from T1 below) scales with |Δ_ST|². Larger wedges produce more persistent traps.

**Property 2.3 (belief invariance)**: Δ_ST is defined with respect to the agent's belief *B*. If beliefs are biased toward *U*_perc (agents who have convinced themselves the sweet signal is actually healthy), Δ_ST shrinks as measured, but the behavioural signature (endorsement of *s* with true *U*_fit < 0) remains. Δ_ST is robust to belief-bias distortion because we measure *U*_fit objectively.

### 2.4 Behavioural Dynamics

Let *s_i*(*t*) denote scalar engagement. The continuous-time dynamics:
$$
\frac{ds_i}{dt} \;=\; \alpha_i\, \frac{\partial U_{\text{perc}}}{\partial s} \,-\, \beta_i\, \delta(\tau)\, I_{\text{visible}}\, (1 - \lambda_i)\, \frac{\partial U_{\text{fit}}}{\partial s} + \sqrt{2 D_i}\, \xi_i(t)
\qquad (12)
$$

where *β_i* is cost aversion, *λ_i* ∈ [0, 1] is the fraction of cost externalised to agents *j* ≠ *i*, and *ξ_i*(*t*) is Gaussian white noise. The **Sweet Trap dynamical condition** obtains when
$$
\alpha_i |\nabla_s U_{\text{perc}}| \gg \beta_i\, \delta(\tau)\, (1 - \lambda_i)\, I_{\text{visible}}\, |\nabla_s U_{\text{fit}}|
\qquad (13)
$$

Under (13), engagement escalates even as *U*_fit decreases — reward-driven drift dominates cost-driven restoring force.

The cost-discount product *δ*(*τ*)(1 − *λ_i*)*I*_visible is the mechanism by which Sweet Traps become entrenched. Each of the three factors can independently shrink the cost-gradient:
- *δ*(*τ*) → 0 when costs are long-delayed (metabolic disease from diet; cognitive decline from screen-time).
- (1 − *λ_i*) → 0 when costs are externalised (pollution from consumption; debt borne by children or guarantors).
- *I*_visible → 0 when costs are invisible (mental-health effects of social media; microplastic accumulation; algorithmic-feed opportunity cost).

Beliefs update Bayesian over observed cost realisations; when *I*_visible = 0 the Bayesian update is stuck at the prior, so the belief *B* never catches up to *U*_fit. This is the dynamical mechanism by which invisibility sustains the trap.

### 2.5 Sub-classes: MST, RST, EST

Three sub-classes differ in *how* Δ_ST arises, while sharing A1–A4.

**Mismatch Sweet Trap (MST)**: passive environmental shift. *ψ* is calibrated on *S*_anc, environment has shifted to *S*_mod. Δ_ST grows with the Kullback-Leibler divergence between ancestral and modern feature distributions. Canonical cases: moth phototaxis (sensory trap), Drosophila hyperconsumption of sucrose (nutritional trap), honeybee neonicotinoid exposure (chemical trap), human consumption of hyper-palatable processed food.

**Runaway Sweet Trap (RST)**: cultural-genetic covariance drives escalation. Equations (formally stated in Math Supplement §C):
$$
\dot{\bar q} = G_q\, \partial_{\bar q} \bar W_{\text{perc}} + G^c_{q,y}\, \partial_{\bar y} \bar W_{\text{perc}}; \quad
\dot{\bar y} = G_y\, \partial_{\bar y} \bar W_{\text{perc}} + G^c_{q,y}\, \partial_{\bar q} \bar W_{\text{perc}}
\qquad (14)
$$

These are **Lande-Kirkpatrick dynamics rewritten with perceived mean utility *W̄*_perc in place of mean fitness *W̄*** — a critical extension (Lemma L4 in Math Supplement §D: cultural transmission is driven by observed perceived success, not by lifetime reproductive success; Cavalli-Sforza-Feldman 1981; Boyd-Richerson 1985; Henrich-McElreath 2003). Consequence: cultural runaway is **not fitness-bounded**. It escalates as long as perceived utility supports it, which under A2 can persist indefinitely while *W̄*_fit collapses. Canonical cases: conspicuous consumption (Frank 1999 *Luxury Fever*), bride-price inflation (Edlund 2006 *Economic Inquiry*), education-investment arms races in East Asia.

**Engineered Sweet Trap (EST)**: an external designer *j* solves
$$
s^*_{\text{design}} \;=\; \arg\max_{s \in S_{\text{design}}} \sum_i \Delta_{\text{ST}}(s, t \mid \psi_i) \cdot \omega_j(i)
\qquad (15)
$$

with extraction weight *ω_j*(*i*) per agent. EST includes: Olds-Milner direct electrode stimulation (the experimental gold-standard Δ_ST), variable-ratio slot machines (Dow-Schüll 2012 *Addiction by Design*), algorithmic recommendation systems trained to maximise engagement (Rahwan et al. 2019 *Nature*), predatory lending, romance-fraud protocols.

Classical Ecological Trap (Robertson-Hutto 2006) is a special case of MST under habitat-choice restriction (*w* = 0, no belief channel; *λ* = 0, full cost internalised; *S* = habitats). Fisher Runaway (Fisher 1930; Lande 1981) is a special case of RST under genetic-ψ restriction and mate-choice-signal restriction.

The unification of these four previously separate frameworks under a shared axiomatic core is the theoretical contribution of Paper 1.

---

## 3. Main Theorems (1,000 words)

Four theorems follow from A1–A4. Proof sketches appear below; full proofs are in the Math Supplement.

### 3.1 T1 — Sweet Trap Stability

**Theorem T1.** Let *s** ∈ *S* satisfy (i) Δ_ST(*s**, *t*) ≥ *ε* > 0 persistently, (ii) A3 with *w_i* ≤ *w*_max < 1/2, (iii) bounded cost-gradient |∂*U*_fit/∂*s*|_{*s**} ≤ *M*. Then *s** is a **locally stable equilibrium** of (12), with exponential return to equilibrium at rate
$$
c \;\gtrsim\; \alpha_i\, \ell(\psi_i, \varphi)\, \varepsilon^2 \,-\, \beta_i\, \delta_{\max}\, M \,-\, D_i^{\text{drift}}
\qquad (16)
$$

where *ℓ* is the local curvature of *U*_perc at *s** (bounded below by properties of the logistic σ near saturation; Lemma L5).

**Proof sketch.** The Jacobian *J*(*s**) of (12) has the form *α_i* ∂²_*s* *U*_perc − [cost term]. Under A3.3 and the persistent Δ_ST wedge, ∂²_*s* *U*_perc is strictly negative at *s** (L5), while the cost term is attenuated by *δ*(*τ*)(1 − *λ_i*)*I*_visible ≤ 1 and often ≪ 1. Hence all eigenvalues of *J*(*s**) have negative real parts. Constructing the Lyapunov function *V*(*s*) = ½‖*s* − *s**‖² + *μ g*(Δ_ST(*s*, *t*)) with *g*(·) smooth convex yields *V̇* ≤ −*c V*, giving the exponential decay. Full algebra in Math Supplement §E. ∎

**Interpretation.** Once an agent enters a Sweet Trap, local perturbations — a bad day, a temporary information campaign, an environmental wobble — decay back to the trap at exponential rate. The trap is not merely "undesirable in hindsight"; it is **mathematically attractive**. This is why the phenomenon is named a trap rather than a mistake.

### 3.2 T2 — Intervention Asymmetry (core theorem)

**Theorem T2.** Fix agent *i* with *w_i* ≤ *w*_max ≤ 0.4. Let *s** be a Sweet Trap LSE. Consider two interventions matched in utility-unit intensity:

- *Information intervention*: update belief *B_i* → *B_i*′ such that 𝔼[*U*_fit ∣ *B_i*′] decreases by Δ*B*.
- *Signal-redesign intervention*: reduce ⟨*ψ_i*, *φ*′⟩ − ⟨*ψ_i*, *φ*⟩ = −Δ*φ* < 0.

Then the induced behavioural changes satisfy
$$
\boxed{\;\frac{|\Delta b_{\text{signal}}|}{|\Delta b_{\text{info}}|} \;\geq\; \frac{1 - w_{\max}}{w_{\max}} \;\geq\; 1.5\;}
\qquad (17)
$$

with strict inequality for any *w_i* < *w*_max.

**Proof sketch.** The information perturbation enters *Ũ_i* through the *w_i* channel; the signal perturbation enters through the (1 − *w_i*) channel. At an LSE, the implicit-function theorem gives Δ*b* proportional to the first-order utility shock divided by the local curvature of *Ũ_i*. The denominator is channel-invariant (a property of the LSE itself). The ratio reduces to (1 − *w_i*)/*w_i* ≥ (1 − *w*_max)/*w*_max = 0.6/0.4 = 1.5. Full algebra in Math Supplement §F.

Crucially, the ratio is **shrinkage-invariant**: DellaVigna & Linos 2022 *Econometrica* document that academic nudge effect sizes shrink by factor ~3× in field deployment. Shrinkage applies symmetrically to both channels, so the ratio is preserved. T2 holds in field settings, not only in lab. ∎

**Interpretation.** Telling a trapped agent "this hurts you" enters decisions through a channel capped at *w*_max < 1/2. Redesigning the environment so the reward signal itself is weaker enters through a channel at least 0.5 and typically ≥ 0.6. The redesign channel is **algebraically at least 1.5× as effective** as the information channel, for every agent satisfying the axioms. This is a structural, not empirical, inequality.

### 3.3 T3 — Cross-Species Universality

**Theorem T3.** Let 𝒜 be any agent satisfying (i) a reward-calibration system *U*_perc(*s*, *t* ∣ *ψ*) with *ψ* shaped by exposure to *S*_anc; (ii) signal-space separability via a feature extractor *φ*; (iii) exposure at *t*_sep to *s* ∈ *S*_mod \ *S*_anc. Then A1–A4 apply to 𝒜 without modification; T1 and T2 hold with the same structural constants.

**Proof sketch.** Each axiom's primitives are species-neutral. A1 requires only a monotone noisy encoder — satisfied by every species with dopaminergic reward systems (Barron et al. 2010 *Biol Rev*). A2 requires only that *S* expands beyond *S*_anc. A3's weight *w* = 0 in pre-cognitive animals is the degenerate low-*w* limit, trivially satisfying *w* ≤ *w*_max. A4's hyperbolic form is documented across rats, pigeons, and humans (Mazur 1987; Rachlin 1974; Ainslie 1975). Δ_ST is well-defined for any agent with a reward system and an environmental-shift exposure. Full argument in Math Supplement §G. ∎

**Interpretation.** Sweet Trap is not a human failing. The mathematical structure — a reward system calibrated against one signal distribution suddenly exposed to another — is a generic feature of any evolved decision-making architecture. Moths, turtles, and humans are the same theorem playing out in different domains.

### 3.4 T4 — Engineered Escalation

**Theorem T4.** Let Δ_ST^MST(*s**) be the equilibrium Sweet Trap magnitude under MST (passive environmental shift). Let Δ_ST^EST(*s*^*_{design}) be the equilibrium under EST (designer solving (15)). For comparable populations and equivalent *ψ*-calibration:
$$
\Delta_{\text{ST}}^{\text{EST}}(s^*_{\text{design}}) \;\geq\; \Delta_{\text{ST}}^{\text{MST}}(s^*)
\qquad (18)
$$

with strict inequality generically. Further, the LSE decay rate satisfies *c*^EST ≥ *c*^MST and the basin of attraction satisfies *U*(*s*^*_{design})^EST ⊇ *U*(*s**)^MST.

**Proof sketch.** By the envelope theorem (Milgrom-Segal 2002 *Econometrica*), the maximum of Δ_ST over *S*_design is at least the value at any particular *s* ∈ *S*_design, including the passive-shift point. The designer can additionally tune the curvature *ℓ* by choosing signal features that maximise the local second-order response of *U*_perc — exactly what variable-ratio reinforcement schedules and reinforcement-learning recommendation systems do. Steeper attractor + larger wedge implies larger basin. Full argument in Math Supplement §H. ∎

**Interpretation.** Naturally emerging Sweet Traps are bad. Adversarially engineered Sweet Traps — platforms, slot machines, predatory lenders — are **strictly worse** along three axes: higher equilibrium wedge, faster local return after perturbation, larger basin of initial conditions from which the trap catches the agent. Interventions effective against MST may be insufficient against EST.

---

## 4. Falsifiable Predictions (500 words)

The axioms and theorems yield five empirically falsifiable predictions. Each is derived from a specific theorem; empirical status is declared (支持 = supported; 待测 = awaiting test; inferred = logically follows from supported results).

**P1 — Intervention asymmetry law.** For any Sweet Trap domain with *w*_max ≤ 0.4, the ratio |Δ*b*_signal|/|Δ*b*_info| ≥ 1.5. *Derivation*: T2. *Falsification*: meta-analysis ratio ≤ 1 across ≥ 4 domains. *Status*: **qualitatively supported; quantitative mini-meta pending**. Paper 2 v2.4 §8 compilation across **six** focal Sweet Trap domains (C8 investment, C11 diet, C12 short-video, C13 housing, D_alcohol, C_pig-butchering; `intervention_asymmetry_table.csv`) finds the signal-redesign point estimate exceeds the information point estimate in 6/6 domains; the 95% CIs do not overlap in 4/6. On the two domains with unit-matched arms (C8 pp/pp; C12 Cohen-d/Cohen-d) the ratios are 74× (Madrian & Shea 2001 auto-enrolment vs Fernandes et al. 2014 financial literacy) and 7× (Allcott et al. 2022 *AER* commitment-device vs information arm), both well above T2's 1.5 floor. A unified cross-domain median on a harmonised (Cohen-d equivalent) scale is deferred to a post-publication mini-meta because four of six domains have heterogeneous native units.

**P2 — Persistence–severity monotonicity.** Δ_ST magnitude correlates positively with behavioural persistence (Lyapunov decay rate *c*) and welfare deficit. Quantitatively, *c* ∼ *α ℓ* |Δ_ST|². *Derivation*: T1. *Falsification*: ≥ 5 high-Δ_ST instances with rapid self-correction (≥ 70% abandonment within 12 weeks absent intervention). *Status*: **awaiting empirical test**. Paper 2 v2.4 does not currently contain a cross-chain persistence-rank × |Δ_ST| correlation; its 19-chain MR results table records causal-effect magnitudes (IVW β, log OR) but not decay rates or post-intervention return fractions. Illustrative anchors consistent in direction — ~70% post-deactivation return within 4 weeks in short-video (Allcott et al. 2020 *AER*); 60–80% post-intervention weight regain within 12 months in diet (Mozaffarian 2016 *Circulation*) — motivate the prediction but do not operationalise its formal rank-correlation test. A persistence-proxy compilation across the 20 Layer-A, 5 Layer-B, and 19 Layer-D cases is a post-publication priority.

**P3 — Cultural amplification.** In RST-dominant domains, Hofstede-style cultural dimensions (PDI, LTOWVS, IDV) explain ≥ 40% of between-country Δ_ST variance. *Derivation*: Lemma L4 + RST dynamics (§2.5). *Falsification*: cross-country R² < 0.15, or sign-reversed correlation. *Status*: **partially supported**. Paper 2 v2.4's 59-country Hofstede-grounded *G*^c index (formula G^c = z(PDI) + z(LTOWVS) − z(IDV); `cultural_gc_results.json`) and 25-country ISSP aspirational-wealth longitudinal panel yield a joint-predictor R² of **0.255** (β_{Δz} = −0.732, p = 0.036; β_{log τ_env} = −0.742, p = 0.042), which exceeds P3's ≥ 0.15 falsification floor but does not reach the ≥ 0.40 prediction point. Paper 2 v2.4 itself notes Layer C aggregate ISSP cross-domain replication is weak (6/11 directional matches; `main_v2.4_draft.md:246` item 2).

**P4 — Engineered escalation.** EST platforms show equilibrium Δ_ST ≥ 1.5× MST analogues, with time-to-equilibrium < 1/2 of MST timescale. *Derivation*: T4. *Falsification*: matched-pair head-to-head with equal equilibrium Δ_ST or faster MST escalation. *Status*: **qualitatively supported; quantitative matched-platform test pending**. Paper 2 v2.4 Layer A shows the EST case (A5 Olds-Milner direct-stim, Δ_ST = +0.97) exceeds all MST sensory-exploitation cases (A1–A3, A7, A10–A15; Δ_ST ≤ 0.82). Platform-level illustrative anchors frequently cited in this space — TikTok engagement growth relative to YouTube auto-play 2018–2022, and the variable-ratio vs fixed-ratio reinforcement-schedule contrast (Dow-Schüll 2012 *Addiction by Design* for architectural characterisation) — motivate the qualitative EST > MST claim but the specific quantitative ratios in the literature are secondary-source and are not Paper 2 primary measurements. The quantitative `≥ 1.5×` and `< 1/2 timescale` predictions require a matched-platform Δ_ST study.

**P5 — Cross-species mechanism rank preservation.** The rank ordering of mechanisms by Δ_ST magnitude (Olds-Milner > sensory exploitation > Fisher runaway) is preserved across species. In humans: algorithmic engagement > supernormal food/media > cultural status signal. *Derivation*: T3. *Falsification*: rank reversal animal ↔ human on overlapping mechanism cells. *Status*: **strongly supported (pre-registered A+D joint test)**. Paper 2 v2.4's pre-registered A+D joint meta-regression (`cross_level_meta_findings.md` §3.4, main_v2.4_draft.md §6 and §M9) yields olds_milner β = +1.58 (within-layer z-scale), Wald χ²(2) = 5.49, **p = 0.019**. The descriptive Spearman ρ(A, D) = +1.00 on the **2 overlapping mechanism categories** (olds_milner, sensory_exploit) is a geometric identity at n = 2 — flagged as such in Paper 2 v2.4's limitations — and inferential support comes from the A+D joint β, not from the n = 2 ρ. Layer A mean Δ_ST: olds_milner = 0.780, sensory_exploit = 0.646; Layer D mean |log OR|: olds_milner = 0.553, sensory_exploit = 0.354; same rank order in both layers, magnitude ratios 1.21 (A) and 1.56 (D).

P5 is strongly supported by the pre-registered A+D joint test; P1 is qualitatively supported (6/6 domain direction, 4/6 CIs non-overlapping) with a harmonised-scale mini-meta pending; P3 is partially supported (R² = 0.255 exceeds falsification floor but below target); P2 and P4 await empirical test with motivating anchors from existing literature. An integrity audit comparing each prediction's empirical annotations against Paper 2 v2.4 source files is recorded at `paper1-theory/00-outline/integrity_audit_log.md`; v1.0 draft contained four prediction-level numerical mismatches that are corrected here. Sharpened sub-predictions (P1.a w-stratification; P2.a EST > MST persistence; P3.a MST-RST contrast; P4.a RL-acceleration; P5.a dopaminergic homology) plus the post-audit quantitative commitments (P1 harmonised mini-meta; P2 persistence-rank compilation; P4 matched-platform test) are pre-registered at **[OSF_DOI_TO_INSERT]**. Full tables in `03-predictions/predictions.md`.

---

## 5. Relationship to Existing Frameworks (500 words)

We specify formal relationships to seven adjacent theories; details in the Math Supplement and `04-positioning/positioning.md`.

**Prospect Theory (Kahneman-Tversky 1979)** is mathematically **orthogonal**. PT operates on reference-dependent valuation of a single utility; Sweet Trap operates on the wedge between two utilities. Both can be simultaneously true; a hybrid "PT-inside-Sweet-Trap" is derivable but not required.

**Rational Addiction (Becker-Murphy 1988)** is a **degenerate specialisation** of Sweet Trap with *w* = 1, *λ* = 0, *U*_perc ≡ *U*_fit. The agent is fully forward-looking and reward-fitness aligned; A3 is violated by construction. In any domain with observable externalisation *λ* > 0 (bride price, pollution, inter-generational debt), RA predicts no effect while Sweet Trap predicts Σ_ST scaling with *λ* — a clean empirical separator.

**Evolutionary Mismatch (Williams-Nesse 1991; Lieberman 2013)** is the **informal precursor**: Mismatch ⊂ MST ⊂ Sweet Trap. Sweet Trap formalises Mismatch by adding the decision rule (A3), the cost channel (A4), the cultural runaway subclass (RST), and the adversarial subclass (EST). Mismatch has no quantitative falsification; Sweet Trap has axiom-level falsification for each of A1–A4 and five empirical predictions P1–P5.

**Ecological Trap (Robertson-Hutto 2006)** is a **cross-species special case** of MST restricted to habitat choice in non-cognitive agents (*S* = habitats, *w* = 0, *λ* = 0). Sweet Trap extends the frame to non-habitat domains, cognitive agents, and engineered signals.

**Fisher Runaway (Fisher 1930; Lande 1981)** is a **proper sub-family of RST** under genetic-*ψ*, mate-choice-signal, no-designer, reproductive-cost restrictions. The critical difference is L4: RST uses perceived mean utility *W̄*_perc in place of Lande's mean fitness *W̄*, grounded in the cultural-transmission literature. Consequence: RST is **not fitness-bounded**. This explains why cultural escalation (luxury consumption exceeding household solvency) persists past any survival-cost boundary — a pattern Fisher runaway cannot generate.

**Nudge / Libertarian Paternalism (Thaler-Sunstein 2008)** is a policy philosophy backed by T2. Sweet Trap explains **when** nudges work (signal-redesign, (1 − *w*)-bounded channel) and **when** they fail (pure information, *w*-bounded channel). DellaVigna-Linos 2022's 3× academic-to-field shrinkage is interpreted as the disproportionate field-deployment of information-channel nudges.

**Bounded Rationality / Dual System (Kahneman 2011)** is a **compatible refinement**. Sweet Trap specifies which System-1 signals have decoupled from System-2 fitness estimates (A2 scope) and why deliberative override fails (A3.3 bounds System-2 weight). Sweet Trap makes the stronger prediction that even unbounded deliberation cannot override the choice — Lemma L3 (akrasia): a cognitively-aware agent with perfect belief still chooses the trap under the *w*-bound. This extends dual-system theory with a formal impossibility result.

**Summary**: Sweet Trap is a *strict extension* of Mismatch and Ecological Trap, a *proper generalisation* of Fisher Runaway, a *containing limit* of Rational Addiction, *orthogonal* to Prospect Theory, a *refinement* of dual-system, and the *theoretical engine* of Nudge.

---

## 6. Discussion (700 words)

### 6.1 Scope and limits

Sweet Trap Theory applies to choices where (i) a reward-calibration system exists; (ii) signals can be decomposed into a feature space accessible to that system; (iii) the choice space includes signals calibrated against (*S*_anc) and signals that are not (*S*_mod \ *S*_anc); (iv) the agent's weighting of beliefs about fitness is bounded below 1/2. Within this scope, A1–A4 generate T1–T4 and P1–P5 as formal consequences.

Outside this scope, Sweet Trap is silent. Bacterial chemotaxis (no reward system) is not a Sweet Trap candidate. Coerced overtime work under economic necessity (no voluntary endorsement — A3 scope excluded) is not a Sweet Trap even though it resembles one superficially. Acute clinical compulsion at DSM-5 threshold (failure of F2 endorsement signature) is a distinct phenomenon. These scope conditions are not weaknesses; they are the specification of what the theory is about.

**Two theoretical gaps** remain for future work. First, the *w*_max < 1/2 bound in A3 is a structural commitment with empirical anchors (typical revealed-preference estimates *w* ∈ [0.15, 0.35]), but populations at the *w*_max boundary (Tier B regime, 0.45 < *w*_max < 0.5) deliver only probabilistic rather than deterministic dominance in T2. Highly-informed professional populations evaluating well-studied risks might operate in Tier B, where T2's margin shrinks. Second, T4's basin-radius argument is directional but quantitatively loose — the function *h*(Δ_ST) governing basin expansion is characterised qualitatively rather than analytically. A sharp basin-radius estimate for EST vs MST would strengthen the engineered-escalation claim.

### 6.2 Path to replication

Sweet Trap Theory is **falsifiable at multiple levels**. Each axiom has a specific falsification test (see `axioms_and_formalism.md` falsifiability sections). Each theorem generates a prediction P1–P5 that can be refuted by existing or near-reach empirical data. And the core intervention-asymmetry law (T2 / P1) is testable in a **single controlled experiment**.

In `03-predictions/minimal_experimental_paradigm.md` we specify a 120-round repeated-choice task with two options: Option A yields high immediate reward with bright animation but negative long-run payoff; Option B yields modest immediate reward with neutral display but positive long-run payoff. Four arms (Control / Information disclosure / Signal redesign [animation removed] / Combined), n = 200 per arm on Prolific (total N = 800, cost ~$6K), test the ratio |Δ*b*_signal|/|Δ*b*_info|. Pre-specified falsification condition: if the ratio ≤ 1.0 with 95% CI excluding 1.5, the law is refuted in the lab. Under the theoretical prediction, signal arm *d* ∈ [0.50, 0.90] vs information arm *d* ∈ [0.10, 0.25], giving ratio ~2-5×. We have pre-registered this paradigm at **[OSF_DOI_TO_INSERT]**; implementation follows Paper 1 acceptance.

### 6.3 Why this matters now

Three arguments for the urgency of a formal Sweet Trap theory:

First, the **engineered sub-class is expanding**. Algorithmic recommendation systems trained on engagement metrics, variable-ratio reward schedules in consumer products, and platform-mediated predatory protocols are proliferating at a speed that empirical whack-a-mole cannot keep up with. A theory that distinguishes MST from EST, and predicts that interventions effective against MST may be insufficient against EST (T4), orients the policy response to what is structurally new.

Second, the **intervention-asymmetry law inverts the standard informational-paternalism playbook**. For two decades, behavioural public policy has defaulted to information provision — calorie labels, cigarette warnings, energy-efficiency disclosures — with disappointing field effects (DellaVigna-Linos 2022). T2 provides the mathematical explanation: information enters through the *w*-channel, which is structurally capped below 1/2. The most effective policy tools in Sweet Trap domains are **choice-architecture redesign** and **signal-supply regulation**, not information campaigns. This reframing has immediate application to diet policy (redesign food environments rather than disclose), gambling policy (regulate machine design rather than promote awareness), and platform policy (constrain engagement-optimising algorithms rather than mandate transparency).

Third, the **cross-species universality (T3) links human behaviour to deep evolutionary continuity**. The same mathematical structure that traps moths in flames traps humans in engagement feeds. This is not a rhetorical flourish — it is a theorem about the axioms being species-neutral. Recognising this continuity matters for research strategy (animal models are informative; Δ_ST is measurable across taxa), for ethical clarity (humans are not uniquely weak-willed), and for the theoretical unification of evolutionary biology, behavioural economics, and computational neuroscience under a shared formal framework.

A moth, a turtle, and a person scrolling a feed are not three phenomena. They are one phenomenon. This paper gives that phenomenon a name and a mathematics.

---

## References (not counted toward word budget; full list in Math Supplement)

**Theoretical foundation**:
Ainslie, G. (1975). Specious reward: A behavioral theory of impulsiveness and impulse control. *Psychological Bulletin*, 82(4), 463–496.
Becker, G. S., & Murphy, K. M. (1988). A theory of rational addiction. *Journal of Political Economy*, 96(4), 675–700.
Boyd, R., & Richerson, P. J. (1985). *Culture and the Evolutionary Process*. Chicago.
Cavalli-Sforza, L. L., & Feldman, M. W. (1981). *Cultural Transmission and Evolution*. Princeton.
Fisher, R. A. (1930). *The Genetical Theory of Natural Selection*. Oxford.
Henrich, J., & McElreath, R. (2003). The evolution of cultural evolution. *Evolutionary Anthropology*, 12, 123–135.
Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus & Giroux.
Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263–291.
Lande, R. (1981). Models of speciation by sexual selection on polygenic traits. *PNAS*, 78(6), 3721–3725.
Lieberman, D. E. (2013). *The Story of the Human Body*. Pantheon.
Milgrom, P., & Segal, I. (2002). Envelope theorems for arbitrary choice sets. *Econometrica*, 70(2), 583–601.
Nesse, R. M. (2005). Natural selection and the regulation of defenses. *Evolution and Human Behavior*, 26, 88–105.
Robertson, B. A., & Hutto, R. L. (2006). A framework for understanding ecological traps. *Ecology*, 87(5), 1075–1085.
Schlaepfer, M. A., Runge, M. C., & Sherman, P. W. (2002). Ecological and evolutionary traps. *TREE*, 17(10), 474–480.
Schultz, W. (2016). Dopamine reward prediction-error signalling. *Physiological Reviews*, 96, 853–951.
Thaler, R. H., & Sunstein, C. R. (2008). *Nudge*. Yale.

**Empirical anchors**:
Allcott, H., Braghieri, L., Eichmeyer, S., & Gentzkow, M. (2020). The welfare effects of social media. *AER*, 110(3), 629–676.
Barron, A. B., et al. (2010). Reward and its role in invertebrates. *Biological Reviews*, 85(4), 1051–1074.
Chaloupka, F. J., et al. (2012). Effectiveness of tax and price policies in tobacco control. *Tobacco Control*, 21(2), 172–180.
DellaVigna, S., & Linos, E. (2022). RCTs to scale. *Econometrica*, 90(1), 81–116.
Dow-Schüll, N. (2012). *Addiction by Design*. Princeton.
Jambeck, J. R., et al. (2015). Plastic waste inputs from land into the ocean. *Science*, 347(6223), 768–771.
Loss, S. R., Will, T., Loss, S. S., & Marra, P. P. (2014). Bird-building collisions in the United States. *Condor*, 116, 8–23.
Mertens, S., et al. (2022). The effectiveness of nudging: A meta-analysis. *PNAS*, 119, e2107346118.
Mozaffarian, D. (2016). Dietary priorities for cardiometabolic health. *Circulation*, 133, 187–225.
Rahwan, I., et al. (2019). Machine behaviour. *Nature*, 568, 477–486.
Savoca, M. S., et al. (2016). Marine plastic debris emits a keystone infochemical. *Science Advances*, 2, e1600395.
Tobler, P. N., Fiorillo, C. D., & Schultz, W. (2005). Adaptive coding of reward value by dopamine neurons. *Science*, 307, 1642–1645.

*Extended references in Math Supplement.*

---

## Math Supplement

Separate file: `math_supplement.md`. Contains:
- §A Axiomatic foundation with modeling commitments (MC-1 through MC-6)
- §B Δ_ST correlation-form derivation
- §C RST Lande-Kirkpatrick dynamics full derivation
- §D Lemmas L1–L5 with proofs
- §E T1 Jacobian, Lyapunov, basin algebra
- §F T2 full algebra with matching convention and non-linear corrections
- §G T3 species-neutrality argument
- §H T4 envelope theorem application
- §I Extended positioning (seven adjacent theories)
- §J Nomenclature (complete symbol table)
- §K Extended references

---

*End of Paper 1 main text, v1.0 draft, 2026-04-18. Total words ~5,950. See math_supplement.md for proofs and abstract.md for standalone abstract.*
