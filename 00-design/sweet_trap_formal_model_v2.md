# Sweet Trap — Cross-Species Formal Model v2

**Status:** Stage 0β — Formal construct v2 (supersedes `sweet_trap_construct.md` v1)
**Date:** 2026-04-17
**Target journal:** *Science* (primary) / *Nature* main / *Nature Ecology & Evolution* (backup)
**Authors:** Lu An & Hongyang Xi (both corresponding)
**Position in pipeline:** Outputs of Stage 0α (`phenomenology_archive.md`, 27 cases) and 0γ (`literature_cross_species.md`, `adjacent_construct_map.md`, `target_journal_benchmarks.md`) feed directly into the model below. Downstream: `identification.md`, `specification-map.md`, `causal-chain.md`.

---

## 0. One-sentence definition (the paper's keystone)

> **A Sweet Trap is a self-reinforcing welfare-reducing equilibrium in which a reward signal evolved for ancestral fitness (or adopted through cultural innovation) has become decoupled from current fitness, such that the correlation between the agent's perceived reward and the actual fitness outcome is non-positive over the relevant signal distribution, yet individuals continue to endorse the signal.**

Two equivalent short forms:

- *Popular:* "Healthy machinery, wrong signal — chosen anyway."
- *Technical:* "Cor(R_agent, F) ≤ 0 under endorsement, sustained by F3 + F4 dynamics."

The construct is defined on **two timescales and any species with a reward architecture**. The moth (within-lifetime, no learning), the peacock (between-generation, genetic), the parent (within-generation, cultural) — all satisfy the same four-feature definition.

---

## 1. The four defining conditions (formal)

Let *a ∈ A* denote a choice/action. Define two functions of *a*:

- *R_agent(a)*: the **perceived reward** signal the agent's reward architecture returns when *a* is selected. In animals, this is the dopaminergic/incentive-salience response; in humans, the same plus culturally constructed anticipated rewards (status, belonging, identity).
- *F(a)*: the **fitness outcome** of *a*. In non-human animals, *F* = lifetime reproductive success × survival. In humans, *F* = long-run welfare, operationalized as consumption-equivalent utility across ≥ 20 years (or multidimensional objective welfare: health + wealth + mental health + relational capital).

The *relevant signal distribution* is the empirical distribution over *a* induced by the agent's current environment. All correlations and expectations below are taken with respect to this distribution.

### F1 — Reward–fitness decoupling (diagnostic; necessary)

$$
\text{cor}\bigl(R_{\text{agent}}(a), F(a)\bigr)_{\text{current}} \;\leq\; 0 \;\ll\; \text{cor}\bigl(R_{\text{agent}}(a), F(a)\bigr)_{\text{ancestral}}
\tag{F1}
$$

The correlation that selection (biological or cultural) instilled in the reward system is at least zero and typically negative in the current environment, while it was strictly positive in the environment of calibration. Two routes to F1:

- **Route A (mismatch):** *R_agent* was calibrated for an ancestral signal distribution and the distribution has shifted faster than adaptation. (Moth/light; Drosophila/sugar; human/processed food.)
- **Route B (supernormal/novel signal):** A signal with no ancestral referent piggy-backs on general-purpose reward architecture. (Olds–Milner electrode; livestream tipping; MLM narratives; neonicotinoid-laced nectar.)

Both routes satisfy F1; neither requires the stronger Nesse–Lieberman ancestral-mismatch statement. This broadening is adopted from `phenomenology_archive.md` §0.

### F2 — Endorsement without epistemic access (diagnostic; necessary)

$$
\Pr\bigl(\text{choose } a \mid R_{\text{agent}}(a) > 0, \text{ no coercion}\bigr) \;>\; \Pr\bigl(\text{choose } a \mid R_{\text{agent}}(a) = 0, \text{ no coercion}\bigr)
\tag{F2}
$$

The agent actively prefers *a* when its perceived-reward signal is active, above baseline, in the absence of external compulsion. Two exclusions follow:

- **Coerced exposure** (e.g., 996 compulsory overwork): F2 fails because choice is not driven by *R_agent* but by the cost of refusal. `phenomenology_archive.md` §D1.
- **Acute pharmacological addiction** (e.g., nicotine) and **clinical compulsion** (e.g., oniomania): F2 holds behaviourally but the epistemic condition (agent does not experience the choice as subjectively reasonable; reports loss of control) fails. These are adjacent slices of reward-miscalibration, not Sweet Traps. `phenomenology_archive.md` §D2–D4.

F1 + F2 together are the *diagnostic core*. Any phenomenon satisfying both is a **candidate Sweet Trap**.

### F3 — Self-reinforcing equilibrium (persistence; typical but not universal)

Let *π_t(a)* denote the share of the population choosing *a* at time *t*. Then

$$
\frac{d\pi_t(a)}{dt} \;>\; 0 \quad \text{whenever } R_{\text{agent}}(a) > 0, \text{ holding environment fixed.}
\tag{F3}
$$

The equilibrium is attained from below through one of four persistence mechanisms (heterogeneous across cases but formally interchangeable):

- **M1 Individual habit / neural sensitization** (Berridge–Robinson incentive salience): increasing *π* at the individual level by repeated choice. Dominant in A5 Drosophila sugar, A6 Olds–Milner, C11 sugar/fat, C12 gacha.
- **M2 Intra-generational peer norms** (conformist learning; Henrich 2015; Danchin et al. 2018 Drosophila cultural mate choice): *R_agent(a)* is augmented by observing others choose *a*. Dominant in C2 鸡娃, C5 luxury, C13 housing, and — remarkably — A7 Fisherian runaway.
- **M3 Trans-generational norm inheritance** (cultural transmission with within-lineage memory): *π* diffuses through family lines. Dominant in C4 彩礼.
- **M4 Mortality termination** (the "cost" is death; no within-lifetime learning): *π* is maintained by the rate of newly exposed individuals equalling or exceeding the removal rate. Dominant in A1 moth, A2 turtle, A4 jewel-beetle.

F3 is weaker in transient experimental phenomena (A11 supernormal stimulus in the lab; 3.5/4 in the feature table). A case can be a Sweet Trap without F3 if F1 + F2 hold and the time horizon is long enough for the population to be locked in by inflow alone.

### F4 — Absence of corrective feedback (persistence; typical but not universal)

Let *T_reward* be the timing of the reward and *T_cost* the timing of the fitness consequence. Let *I(T_cost → T_decide)* be the information channel between the cost realisation and the next decision epoch. F4 requires:

$$
T_{\text{cost}} \gg T_{\text{reward}} \quad \text{and/or} \quad I(T_{\text{cost}} \to T_{\text{decide}}) \approx 0.
\tag{F4}
$$

The channel *I* can be blocked by: temporal separation (costs realised at senescence), cohort separation (costs borne by others — the *λ* channel), identity reinterpretation (religious, MLM), or mortality (no next decision). F4 distinguishes Sweet Trap from ordinary reinforcement-learnable mistakes: feedback arrives on the wrong side of the decision horizon or to the wrong agent, so ordinary learning cannot repair *R_agent*.

F4 is weakest in slow-change handicap failures (A8) where within-lifetime learning can sometimes repair the miscalibration. A case can be a Sweet Trap without F4 if F1 + F2 + F3 hold, at the cost of faster predicted recovery after intervention.

### Hierarchy

- **F1 + F2** are **necessary**. Every one of the 27 cases in `phenomenology_archive.md` §E satisfies both. A phenomenon without both is not a Sweet Trap.
- **F3 + F4** are **typical persistence conditions** that explain why an F1+F2-diagnostic phenomenon persists. A phenomenon can be a Sweet Trap with weak F3 or weak F4, but it will be easier to correct.

This hierarchy resolves the v1 problem of treating (θ, λ, β, ρ) as four co-equal primitives: the v1 primitives are now reinterpreted as *persistence mechanism parameters that generate F3 + F4*, not as *primitives of the construct itself*. The construct is prior to them; they are one possible implementation of F3 + F4 in the human cultural slice.

---

## 2. The operational scalar: Δ_ST

The four features are qualitative. We introduce a single quantitative index:

$$
\boxed{\; \Delta_{\text{ST}}(a; \text{env}) \;=\; \text{cor}\bigl(R_{\text{agent}}, F\bigr)_{\text{ancestral}} \;-\; \text{cor}\bigl(R_{\text{agent}}, F\bigr)_{\text{current}} \;}
\tag{Δ_ST}
$$

Interpreted as a signal decoupling gradient. Δ_ST > 0 means the reward system has slipped away from its calibration. Δ_ST captures F1 with a sign. The full diagnostic is:

$$
\text{Sweet Trap}(a) \;=\; \mathbb{1}\bigl[\Delta_{\text{ST}}(a) > 0 \text{ and F2 holds for } a\bigr]
$$

Persistence severity is a further scalar:

$$
\Sigma_{\text{ST}}(a) = \Delta_{\text{ST}}(a) \times \underbrace{\tau_{\text{F3}}(a)}_{\text{persistence time}} \times \underbrace{(1 - I(T_{\text{cost}} \to T_{\text{decide}}))}_{\text{feedback block}}
$$

Δ_ST is the paper's keystone metric for three reasons.

**(i) Cross-species comparability.** Animal *F* is reproductive success × survival; human *F* is consumption-equivalent welfare. Both map to the same scalar via correlation with *R_agent*. The units (units of correlation) are species-agnostic.

**(ii) Intervention targeting.** Δ_ST can be reduced by two routes: (a) changing the signal distribution (e.g., reducing night-time light pollution, sugar tax, 双减 policy) so that *R_agent* activates less; or (b) re-wiring the architecture (rare in animals, historically rare in humans, but possible via pharmacology or cultural re-framing). Δ_ST being observable lets policy be judged by whether it actually shrinks the gradient, not by whether it shrinks a symptom.

**(iii) Falsifiability.** If in a proposed domain Δ_ST is not statistically different from zero, the domain is not a Sweet Trap, and the construct loses scope. Our 27 cases in `phenomenology_archive.md` §E survive this test by design (pre-filtered for F1 + F2); a novel domain must survive it prospectively.

### Anticipated criticism of Δ_ST

- **"The ancestral baseline is unobservable."** For animals, we use closely-related extant species in non-disturbed environments as the ancestral proxy (standard in evolutionary trap literature; Schlaepfer 2002; Swaddle 2015). For humans, we use either (i) pre-industrial population data where available, (ii) within-culture control populations that are less exposed to the novel signal (rural vs urban; low-screen vs high-screen siblings), or (iii) theoretical priors derived from evolutionary psychology (Cosmides & Tooby 1992). The "unobservable baseline" criticism applies equally to mismatch theory, which is nonetheless accepted. We address it by triangulating across (i)–(iii).
- **"Correlation is too coarse."** Correlation captures the average signal-fitness relationship. For some cases (e.g., non-monotonic fitness curves) a more refined metric is needed — we retain a mutual-information variant, *MI(R_agent, F)*, for SI robustness. The paper's main text uses correlation for interpretability.
- **"The signal distribution is endogenous."** Yes — F3 + F4 endogenise the distribution. The causal-identification strategy (next section) handles endogeneity via natural experiments that shift the signal distribution quasi-exogenously (e.g., 双减; Facebook college-by-college rollout; artificial-light phase-outs).

### Tradeoff: one scalar vs multi-feature report

A single scalar sacrifices information. We retain the four-feature profile (F1, F2, F3, F4) for the main diagnostic tables and reserve Δ_ST for the cross-species quantitative figure. This mirrors the OceanEquity-Index approach (Nature 2024, corpus-indexed): the paper has both an integrative index and a full feature dashboard.

---

## 3. Two-layer formal model

The model has an **evolutionary/replicator core** (Layer 1) and a **behavioural-economic overlay** (Layer 2) bridged by Δ_ST. Layer 1 alone describes all 11 animal cases (A1–A11) and F3-dominant animal-analogue human cases. Layer 2 is added when human cultural institutions generate cost-externalisation (the *λ* channel) that Layer 1 does not admit.

### 3.1 Layer 1 — Replicator / Lande–Kirkpatrick coevolutionary dynamics

State variables:

- *τ*: mean value of a trait (ornament, consumption level, behaviour intensity) in the population.
- *y*: mean value of a preference (the reward-signal setpoint) in the population.
- *G_τ*, *G_y*: additive genetic (or cultural) variances of trait and preference.
- *G_{τ,y}*: additive covariance — the key parameter in Fisher runaway.
- *W(τ, y)*: mean fitness as a function of trait and preference.

**Lande–Kirkpatrick coupled dynamics:**

$$
\dot\tau \;=\; G_\tau \frac{\partial \bar W}{\partial \tau} \;+\; G_{\tau,y} \frac{\partial \bar W}{\partial y}
\tag{L1}
$$

$$
\dot y \;=\; G_y \frac{\partial \bar W}{\partial y} \;+\; G_{\tau,y} \frac{\partial \bar W}{\partial \tau}
\tag{L2}
$$

Lande (1981) and Kirkpatrick (1982) showed that when the preference–trait covariance is large enough, the system has a **line of neutral equilibria** along which the joint distribution (*τ, y*) can walk indefinitely — the classic runaway.

**Sweet Trap condition in Layer 1.** The population is in a Sweet Trap at (τ*, y*) iff:

$$
\underbrace{\frac{\partial \bar W}{\partial \tau}\bigg|_{\tau^*, y^*} < 0}_{\text{trait is costly at equilibrium}} \quad\text{and}\quad \underbrace{G_{\tau,y} > G^{\text{crit}}_{\tau,y}}_{\text{runaway stability}}
\tag{L3}
$$

where *G^crit_{τ,y}* is Lande's critical covariance (threshold depending on *G_τ* and *G_y* and the curvature of *W*). Equation (L3) is exactly Δ_ST > 0 **plus** F3 via genetic correlation: the trait reduces fitness (F1 instantiated by ∂W/∂τ < 0 at equilibrium) and the preference is locked by correlation with the trait (F3 instantiated by G_{τ,y}).

**Coverage of Layer 1.**

- **Pure sensory traps (A1–A4, A9, A11):** G_{τ,y} is effectively zero; the equilibrium is maintained by new exposure of uncalibrated individuals. These are "leaky" Sweet Traps: Δ_ST > 0 but F3 is only M4 (mortality termination).
- **Classical runaway (A7, A8):** G_{τ,y} > G^{crit}_{τ,y}; full Lande–Kirkpatrick. Peacock/widowbird/swordtail.
- **Signal-hijack (A3, A5, A10):** *τ* and *y* are genetically uncoupled from the *signal source* (plastic; sucrose abundance; neonicotinoid concentration). The dynamics are then reducible to (L1) with *τ = a* set exogenously by the environment; *y* responds to novel signal but cannot drive it back down.

### 3.2 Layer 2 — Behavioural-economic overlay for human cultural cases

For human cases, the replicator core is too slow to track cultural evolution; a behavioural-economic overlay is added. Agent *i*'s utility from action *a_i* in period *t*:

$$
U_{i,t}(a_i) \;=\; \underbrace{\theta_i \cdot R(a_i, S_t)}_{\text{amenity/reward}} \;-\; \underbrace{(1 - \lambda_i)\,\beta_i \cdot C(a_i, t+k)}_{\text{internalised deferred cost}} \;+\; \underbrace{\rho_i \cdot H(a_i, a_{i,\text{past}})}_{\text{lock-in}}
\tag{L4}
$$

Where:

- *R(a, S_t)*: reward as a function of the action and current social/signal state *S_t* (norms, peer behaviour, algorithmic amplification). *∂R/∂S* > 0 captures peer effects; *∂R/∂a* > 0 is the direct reward gradient.
- *C(a, t+k)*: fitness/welfare cost at horizon *k*. Convex in *a*.
- *H(a, a_past)*: history-dependent lock-in (habit, sunk identity).
- *θ_i, λ_i, β_i, ρ_i*: heterogeneous individual parameters.

**Critical reinterpretation of v1 primitives.** The v1 construct `sweet_trap_construct.md` §1.3 treated (θ, λ, β, ρ) as primitives. In v2, they are **emergent parameters of the underlying replicator system in Layer 1**:

| v2 Parameter | v1 Name | Layer 1 origin |
|:---:|:---|:---|
| *θ* | Amenity weight | Steepness of *R_agent* around *a* — the derivative of the reward signal at the decision point. Evolutionary origin: calibration against ancestral *F*. |
| *λ* | Externalisation share | Fraction of *C(a)* realised to individuals other than the decision-maker. Generated by population structure: cohort differential (Layer 1 has no cohorts natively; Layer 2 introduces them). |
| *β* | Present bias | Evolutionary origin: selection for present-bias in short-lived ancestral organisms with high extrinsic mortality. Formally derivable from (L1)–(L2) as the steady-state temporal discount implied by optimal life-history theory (Kaplan & Gangestad 2005; Stearns 1992). |
| *ρ* | Status-quo lock-in | Emergent from M2/M3 cultural-replicator dynamics: a social norm with nonzero *G_{τ,y}_cultural* produces status-quo persistence at the individual level. |

**This is the theoretical contribution.** v1 treated the behavioural-economic primitives as axioms. v2 *derives* them from evolutionary first principles. This answers Reviewer 3's likely attack ("Behavioural economics paper with evolutionary garnish") by showing that the BE overlay is a limiting case of the evolutionary core, not a parallel track.

### 3.3 Bridge — unifying the two layers

The four defining conditions map cleanly to both layers:

| Condition | Layer 1 expression | Layer 2 expression |
|:---|:---|:---|
| **F1** (Δ_ST > 0) | *∂W/∂τ* < 0 at equilibrium with *y* fixed from ancestral *W_anc* | *R(a, S) · ∂a/∂R* dominates −*(1-λ)βC'* even though *C'(a*)* > 0 |
| **F2** (endorsement) | Agent (phenotype) actively expresses preference *y* for *τ* | Revealed preference: observed action *a_i* maximises *U_{i,t}* |
| **F3** (self-reinforcement) | *G_{τ,y}* > *G^{crit}* (Lande) | *∂R/∂S_t > 0* with social state *S_t* rising in *π(a)* |
| **F4** (feedback blocked) | Cost is in fitness, not in phenotype utility; no within-lifetime signal | *λ > 0* and/or *k >> 0* break the *C*-to-*R_agent* channel |

**The unified scalar Δ_ST is invariant across layers.** Computationally, in Layer 1 Δ_ST is estimated from comparative population fitness data; in Layer 2 from the implied revealed-preference wedge (I* − I** in v1 notation, or equivalently the within-person well-being response to *a* given cohort-differential cost).

### 3.4 Why two layers rather than one

**One-layer purely evolutionary (Layer 1 alone)** cannot handle:
- Intra-generational cost-externalisation channels (a living parent's 鸡娃 spending shifts child welfare *now*, not across generations).
- Culturally novel signals with no ancestral referent (C3 livestream, C7 MLM): G_{τ,y} is not defined because there is no *τ* inherited.
- Hyperbolic discounting as a within-lifetime phenomenon distinct from evolutionary discounting.

**One-layer purely behavioural (v1 Layer 2 alone)** cannot handle:
- Animal cases (no economic utility function for moths).
- The evolutionary origin of (θ, λ, β, ρ) — why humans even have these parameters.
- Why the same mathematical structure appears in sexual selection, habitat choice, and consumer markets.

**Two-layer architecture** is the minimum needed for the 27-case cross-species coverage. The tradeoff: greater mathematical complexity for reviewers, but the payoff is the "one equation, three domains" narrative (moth + peacock + 鸡娃) that Science/Nature main demands — see `phenomenology_archive.md` §F.1.

---

## 4. Four testable cross-species propositions

Each proposition is falsifiable on both animal and human data. For each, we specify the animal test and the human test, and give the meta-analytic strategy for cross-species validation.

### Proposition 1 — Endorsement–fitness paradox

> **P1.** When Δ_ST(a) > 0 and R_agent(a) is activated, the choice frequency π(a) does not spontaneously decline even though expected F(a) ≤ 0.

**Animal test.** Olds–Milner rats (A6): lever-pressing rate with food/water foregone; Woodcock et al. 2017 *Science* (neonicotinoid-laced nectar preference in field-realistic colonies with known colony-level reproductive failure). Meta-criterion: across ≥ 8 animal cases in Section A of `phenomenology_archive.md`, observed *π(a)* is non-decreasing under experimentally-verified F < 0.

**Human test.** Within-person well-being response to *a* estimated with individual FE in longitudinal data (CFPS for 鸡娃, 996 aspirational overwork, 彩礼; external panels for diet, social media). Meta-criterion: ≥ 5 of 8 candidate human domains show within-person *∂W_1/∂a > 0* while objective *∂W_2/∂a < 0* under pre-registered specification curves.

**Cross-species synthesis.** Meta-analytically combine animal effect sizes (standardised as preference strength ÷ fitness loss) with human effect sizes (well-being slope ÷ welfare slope). Expected convergence: both distributions are centred on positive endorsement × negative welfare, with modest cross-species variance.

**Falsification.** If in > 2 of 8 human domains, well-being responds negatively to engagement when objective welfare is negative, P1 fails for humans and the scope narrows. If > 3 of 11 animal cases show spontaneous preference attenuation, P1 fails for animals.

### Proposition 2 — Heterogeneous *λ* (or its animal homologue) amplifies trap severity

> **P2.** The persistence Σ_ST is monotone increasing in the share of fitness cost externalised to other individuals (human *λ*) or to future generations (animal analogue: differential mortality in Fisher runaway).

**Animal test.** In sexual selection cases (A7, A8), we expect Σ_ST to scale with female-specific cost (peacock: males bear ornament cost; females bear preference cost only indirectly via offspring). Meta-analyse 30+ sexual-selection datasets for the preference-cost–ornament-cost asymmetry (building on Kokko et al. 2002).

**Human test.** For each of 5 focal domains, identify λ proxies (age × migration expectation for urban; whether parent expects to support child in old age for 鸡娃; whether groom vs bride family bears 彩礼; public-insurance coverage for diet; co-signer status for credit). Within each domain, regress Σ_ST on λ proxy with specification curve.

**Cross-species synthesis.** Both animal and human λ predict persistence. The prediction is not just "λ > 0 is necessary" (v1 claim) but "λ magnitude scales Σ_ST continuously" — a quantitative, not just qualitative, scaling.

**Falsification.** If λ heterogeneity is null in > half of human domains with adequate power, or if sexual-selection ornament-cost asymmetry does not predict runaway magnitude in the meta-analysis, P2 fails.

### Proposition 3 — Novel-environment trigger

> **P3.** Sweet Traps emerge when the signal distribution shifts faster than sensory/cognitive adaptation. Formally: let *τ_env* be the environmental signal-shift timescale and *τ_adapt* be the adaptation timescale (generation time for animals; cultural-learning time for humans). Sweet Trap emergence requires *τ_env < τ_adapt*.

**Animal test.** For each of A1, A2, A3, A9, A10, compute *τ_env* (time since widespread artificial light / plastic / pesticide) and *τ_adapt* (generation time). All five cases satisfy *τ_env / τ_adapt ≪ 1*. Compare to cases where this ratio is ≥ 1 (slow climate change) which should show no clear trap formation.

**Human test.** Nutrition transition (C11): *τ_env* ≈ 25–50 years for China, 100+ years for UK/US; *τ_adapt* ≈ 1 cultural generation (25 years). Rapid-transition populations should show stronger Sweet Trap signals. Similarly for social media (C12; *τ_env* ≈ 15 years), knowledge-payment (C9; *τ_env* ≈ 10 years), livestream (C3; *τ_env* ≈ 7 years).

**Cross-species synthesis.** Plot *τ_env / τ_adapt* on the x-axis and Σ_ST on the y-axis for all 27 cases. Prediction: strong negative relationship (smaller *τ_env / τ_adapt* → larger Σ_ST).

**Falsification.** If the ratio does not predict Σ_ST across cases (e.g., bride price runaway despite *τ_env / τ_adapt ≈ 1* in some cultures), P3 fails for that branch and the theory must accommodate a purely cultural-runaway subclass.

### Proposition 4 — Corrective-feedback failure and intervention asymmetry

> **P4.** Because R_agent is produced by evolved architecture, interventions targeting *beliefs* (information, education) are systematically weaker than interventions targeting the *signal distribution* (reducing exposure) or the *reward architecture* (pharmacological, structural).

**Animal test.** Light-pollution abatement (reducing exposure) reduces moth/turtle mortality; "educating" moths is not a thing. Bottle-colour regulation in Western Australia reduced *Julodimorpha* bottle mounting. Reviewed in Science 2023 (adg5277).

**Human test.** Policy meta-analysis across 5 domains:
- Sugar tax (exposure) > nutrition education (belief) — confirmed by Allcott, Lockwood & Taubinsky 2019 AER.
- 双减 (exposure) > parenting advice (belief) — prospective test using 2021 cutoff.
- Housing market caps (exposure) > buyer-awareness campaigns (belief) — cross-city comparison.
- Screen-time limits imposed (exposure) > media-literacy education (belief) — Braghieri 2022 RCT framing.
- 彩礼 ceiling enforcement (exposure) > "plain-wedding" campaigns (belief) — cross-county Chinese data.

**Cross-species synthesis.** The relative magnitude of "exposure interventions" vs "information interventions" should converge: exposure-targeting consistently stronger across species and domains. This is the "policy" leg of the paper and its broadest-interest claim.

**Falsification.** If in > 2 of 5 human domains, information interventions match or exceed exposure interventions, the evolutionary-architecture claim weakens and Sweet Trap becomes closer to Bernheim–Taubinsky internality theory. This is the most falsification-vulnerable proposition.

### Which proposition is most at risk?

**P4 is most likely to falsify (25–35% prior probability of empirical failure).** Evidence on information interventions is mixed; for some domains (e.g., tobacco warning labels, HIV awareness in specific cohorts), information has worked. If P4 falsifies, Sweet Trap does not collapse — it becomes a construct with *heterogeneous* feedback-failure across domains, which is still useful but loses the strong universal-architecture claim that buys Science.

P2 is second-most-risky (20–30%): the quantitative scaling of Σ_ST on λ may fail statistical power even if the sign is right in each domain.

P1 is lowest-risk (≤ 10%): the endorsement–fitness paradox is the definitional core; if it falsifies we have no paper, but the 27-case archive was pre-filtered for it.

P3 is mid-risk (15%): the *τ_env / τ_adapt* framing is elegant but may be statistically underpowered across 27 heterogeneous cases.

---

## 5. Differentiation from adjacent constructs (quantitative)

The v1 construct differentiated verbally; v2 differentiates numerically via Δ_ST and the F1–F4 profile.

| Construct | F1 (Δ_ST > 0) | F2 (endorsement) | F3 (self-reinforce) | F4 (feedback blocked) | Scope of *a* | Formal model |
|:---|:---:|:---:|:---:|:---:|:---|:---|
| **Fisher runaway** | ✓ at equilibrium | ✓ | ✓ (G_{τ,y}) | ∼ | Mate choice only | Lande–Kirkpatrick (Layer 1 only) |
| **Ecological trap (Schlaepfer 2002)** | ✓ | ✓ | ✗ (no lock-in required) | ✓ | Habitat choice only | Verbal / verbal-dynamics |
| **Evolutionary trap (Robertson 2013)** | ✓ | partial | partial | ✓ | Behaviour in novel env | Verbal |
| **Mismatch (Lieberman 2013)** | ✓ | ✗ (passive response) | ✗ | ✓ | Human physiology | Verbal |
| **Internality (Bernheim–Taubinsky)** | ✗ (not evolutionary) | ✓ | ✗ | partial | Single-agent choice | Yes (welfare calculus) |
| **Addiction (Becker–Murphy; Volkow)** | ambiguous route | ✓ / clinical | ✓ (neural) | ✓ | Substance/behaviour | Yes (neural + econ) |
| **Coerced exposure (996)** | possibly ✓ | **✗** | ✓ | ✓ | Labour | Principal-agent |
| **Sunk cost** | ✗ | n.a. | ✗ | ✗ | Past-anchored decision | Yes (behavioural) |
| **Temptation (Gul–Pesendorfer)** | ✗ | behaviourally, no epistemic | ✗ | partial | Intertemporal choice | Yes |
| **SWEET TRAP (this paper)** | ✓ (required) | ✓ (required) | ✓ (typical) | ✓ (typical) | Cross-species, cross-domain | **Two-layer** |

**The quantitative differentiator: only Sweet Trap requires {F1 + F2} as strict necessary conditions and provides a formal two-layer model.** Every other construct either weakens one of the conditions (e.g., ecological trap has F1 but not explicit F2), restricts scope (Fisher: mate choice only; addiction: one domain; internality: human only), or lacks a formal mechanism generating the condition (mismatch).

**The Δ_ST differentiator.** For Fisher runaway, Δ_ST is computable from Lande–Kirkpatrick but typically not emphasised — Fisher literature focuses on *G_{τ,y}*. For ecological traps, Δ_ST is implicit in the definition but not measured. For internality, there is no Δ_ST because there is no evolutionary baseline. Sweet Trap's contribution is *making Δ_ST the primary cross-species observable*, unifying the measurement problem that the adjacent constructs treat separately.

### Key quantitative test: Sweet Trap ⊃ Ecological Trap and ⊃ Fisher Runaway

The construct is a strict superset:
- Every ecological trap (in the Schlaepfer sense) satisfies F1 + F2. Some have F3 (e.g., A9 indigo buntings with site fidelity) and some do not (transient habitat traps).
- Every Fisher runaway satisfies F1 + F2 + F3. F4 can be weak (the fitness cost is borne directly by the male phenotype within its lifetime, so feedback is *present* but cannot motivate behaviour change because it is terminal).
- Some Sweet Traps are neither ecological traps nor runaways (C3 livestream, C7 MLM — novel cultural signals with no ancestral referent and no genetic-covariance dynamics).

**The claim "Sweet Trap ⊃ Ecological Trap ∪ Fisher runaway"** is the Section 1 headline of the Results for Science.

---

## 6. Empirical pipeline and 27-case correspondence

Each of the 27 cases in `phenomenology_archive.md` is mapped one-to-one to the two-layer model. The table below shows the mapping for a representative set; the full mapping is in SI Appendix §A.

| Case | Layer | Layer 1 params | Layer 2 params | F1 route | F3 mechanism | Δ_ST proxy |
|:---|:---:|:---|:---|:---:|:---:|:---|
| A1 Moth-to-flame | 1 only | *τ* = flight angle, *y* = phototactic setpoint, *G_{τ,y}* ≈ 0 | — | Route A | M4 mortality | Moth mortality at lights / no-light control |
| A2 Turtle hatchling | 1 only | *τ* = crawl direction, *y* = photic setpoint | — | Route A | M4 | Beach survival rate with/without shield |
| A5 Drosophila sugar | 1 only | *τ* = feeding rate, *y* = gustatory setpoint | — | Route A | M1 habit | Life-span under sucrose vs control |
| A6 Olds–Milner | 1 only | *τ* = lever-press, *y* = direct reward stim | — | Route B | M1 | Experimental — by construction Δ_ST = +1 |
| A7 Peacock | 1 only | *G_{τ,y}* > G^crit | — | Route A (signal shift ≈ hypothesised environment change) | M2/M3 | Tail length vs survival cost |
| A10 Neonicotinoid bees | 1 only | *τ* = visit rate, *y* = nicotinic-receptor preference | — | Route B | M1 + M2 waggle | Colony reproductive output |
| C1 打鸡血/画饼 | 2 | → θ from *y*, ρ from M2 | θ high, λ low–mid, β high, ρ high | Route B (cultural signal) | M2 peer overwork norm | Well-being in year-1 vs year-5 layoff cohort |
| C2 鸡娃 | 2 | → λ from cohort differential | θ high, λ high, β mid, ρ high | Route A | M2 peer norm | Parent well-being vs child mental-health |
| C4 彩礼 | 2 | Zahavi failure | θ mid, λ high (intergenerational), β high, ρ very high | Route A | M3 trans-generational | Wedding debt vs marriage stability |
| C11 Sugar/fat/salt | 2 | Directly from A5 | θ mid, λ mid (public-health system), β high, ρ high | Route A | M1 + M2 | HbA1c trajectory × food environment |
| C12 Short-video/gacha | 2 | Directly from A6 | θ high, λ low, β very high, ρ high | Route B | M1 | Sleep × mental-health × dopamine-system measure |

Full mapping for all 27 cases in SI §A.

**Narrative deployment in Science Results.** Each of §F.1–F.3 in `phenomenology_archive.md` gets one Results figure:

- **Figure 2 (Same positive-feedback mechanism at three scales):** moth (individual sensory) + peacock (genetic coevolution) + 鸡娃 (cultural coevolution). Same Lande–Kirkpatrick equations with different interpretations of *τ* and *y*.
- **Figure 3 (Signal-hijack pathway):** plastic/turtle (material mimicry) + neonicotinoid/bee (chemical mimicry) + sugar/fat/salt (ancestral reward in super-abundant environment). Same F1 Route A structure.
- **Figure 4 (Direct reward hijack without ancestral mimicry):** Olds–Milner (electrode) + livestream (parasocial) + MLM (narrative). F1 Route B. Demonstrates that Sweet Trap is *not* just ancestral mismatch.

---

## 7. Science paper structure (draft)

```
Title: "Sweet Traps: A cross-species framework for reward-fitness decoupling"
       (alt: "From moths to markets: A formal theory of self-reinforcing welfare reduction")

Abstract (150 words)
Introduction (500 words) — paradox + three cross-species examples + formal model preview
Results 1: The formal framework and Δ_ST metric (+ Figure 1: concept + 4-feature profile)
Results 2: Cross-species validation — literature synthesis of 11 animal cases (+ Figure 2: "same mechanism, three scales")
Results 3: Within-person human tests — 3–4 domains from CFPS + 1–2 external panels (+ Figure 3: endorsement-welfare paradox)
Results 4: Cross-cultural universality check — WVS/ESS meta (+ Figure 4: direct reward hijack)
Results 5: Policy implication — exposure vs belief interventions (+ Figure 5: P4 meta)
Discussion (500 words): Scope, boundary conditions, what this does and does not explain
Methods: Layer 1 derivation; Layer 2 derivation; identification strategies per domain; Δ_ST estimation
SI Appendix A: 27-case feature profile (extension of phenomenology_archive.md §E)
SI Appendix B: Formal derivations and proofs
SI Appendix C: Animal meta-analysis
SI Appendix D: Human pre-registered analyses per domain
SI Appendix E: Code (Python + R)
```

**Draft Introduction paragraph 1 (the hook).**

> Every night, hundreds of millions of moths die at artificial lights. Their navigation system — evolved over a hundred million years to fly in straight lines under the moon — computes a doomed logarithmic spiral under a porch bulb that is a million times closer. The moth is not making a mistake. It is, neurologically and behaviourally, doing exactly what three hundred thousand generations of ancestors were shaped to do. This same architecture — reward signals calibrated in one environment, deployed in another — predicts the behaviour of a peacock whose ornament shortens its life, a fruit fly that starves in an odour field without calories, a honeybee that prefers neonicotinoid-laced nectar that poisons its colony, a Chinese parent who invests half the household's discretionary income in a child's tutoring that yields neither admission nor well-being, a delivery driver who tips three thousand yuan a month to a streamer he has never met. We propose the **Sweet Trap** — a self-reinforcing welfare-reducing equilibrium in which reward signals evolved for ancestral fitness, or adopted through cultural innovation, have been decoupled from current fitness — as a single mechanism for all of these. We formalise the condition as a cross-species scalar, Δ_ST, derive it from Lande–Kirkpatrick coevolution in animals and behavioural public economics in humans, and test four empirical predictions on 11 animal cases, 8 human domains, and 2.1 million person-years of panel data across three cultures.

**Alternative openings** (for A/B testing with Andy):

- Start with 鸡娃 + 双减 natural experiment (more policy-punch, less cross-species wow).
- Start with Olds–Milner (mechanistic, but risks "it's just addiction" framing).
- Start with Δ_ST as a graph across the 27 cases (visual, but abstract).

Recommended: the moth-opening above, because it establishes *cross-species* before the reader can bucket the paper as "behavioural economics".

---

## 8. Notation (downstream documents must use consistently)

| Symbol | Meaning |
|:---:|:---|
| *a* | Action/choice |
| *R_agent(a)* | Perceived reward signal |
| *F(a)* | Fitness outcome (species-specific) |
| *Δ_ST* | Reward-fitness decoupling gradient (Eq. Δ_ST) |
| *Σ_ST* | Sweet Trap persistence severity |
| *τ, y* | Layer-1 trait and preference |
| *G_{τ,y}* | Covariance between trait and preference |
| *G^{crit}_{τ,y}* | Lande critical covariance |
| *θ, λ, β, ρ* | Layer-2 emergent parameters (from v1) |
| *S_t* | Social signal state |
| *H* | History/lock-in function |
| *π_t(a)* | Population share choosing *a* at *t* |
| *τ_env, τ_adapt* | Environmental and adaptive timescales (Prop 3) |
| *I(T_cost → T_decide)* | Information channel from cost realisation to next decision |
| F1, F2, F3, F4 | Defining conditions 1–4 |

---

## 9. Open questions for Stage 0γ → Stage 1 handoff

1. **Layer 1 fit for A11 supernormal stimulus lab experiments.** Short-horizon experiments violate F3 (no lock-in within minutes); yet they are critical for showing the diagnostic F1 + F2 outside of natural populations. Treated as an independent *diagnostic substrate*, not as a Sweet Trap instantiation.
2. **Layer 2 fit for non-Chinese contexts.** The λ parameter has clean Chinese instances (彩礼, 鸡娃 with multi-generational cost transfer, state-pension-system-underwritten lifestyle diseases). The cross-cultural check must demonstrate that λ > 0 is recoverable in Western panels (HRS/PSID/UKHLS) with different social-policy architectures.
3. **Graded F2.** Some cases have mixed coercion/endorsement (C13 housing — peer pressure shades into economic cornering). A graded F2 preserves the construct but complicates the diagnostic. We treat the paper's main headline cases as clean (F2 ≈ 1) and put graded cases in SI.
4. **Relationship to Bernheim–Taubinsky welfare calculus.** Our Δ_ST can be translated into their internality units via the mapping *internality ≈ Δ_ST × WTP for the signal*. This bridges Sweet Trap to welfare economics without subsuming it. A standalone methods note is planned.

---

## 10. References (additions beyond v1 §10)

Supplement to `sweet_trap_construct.md` v1 §10:

- **Danchin, E. et al. 2018.** Cultural flies: Conformist social learning in fruitflies predicts long-lasting mate-choice tradition. *Science* 362, 1025–1030. DOI:10.1126/science.aat1590.
- **Dreyer, D. et al. 2025.** Migratory moths navigate using the stars. *Nature* News & Views. DOI:10.1038/d41586-025-01709-5 [VERIFY].
- **Fabian, S.T. et al. 2024.** Why flying insects gather at artificial light. *Nature Communications* 15, 689.
- **Fisher, R.A. 1930.** *The Genetical Theory of Natural Selection.* Oxford: Clarendon Press.
- **Kaplan, H. & Gangestad, S.W. 2005.** Life history theory and evolutionary psychology. In *The Handbook of Evolutionary Psychology* (Buss ed.), 68–95.
- **Kirkpatrick, M. 1982.** Sexual selection and the evolution of female choice. *Evolution* 36, 1–12.
- **Kokko, H., Brooks, R., McNamara, J.M. & Houston, A.I. 2002.** The sexual selection continuum. *Proc. R. Soc. B* 269, 1331–1340.
- **Lande, R. 1981.** Models of speciation by sexual selection on polygenic traits. *PNAS* 78, 3721–3725.
- **Robertson, B.A., Rehage, J.S. & Sih, A. 2013.** Ecological novelty and the emergence of evolutionary traps. *TREE* 28, 552–560.
- **Santos, R.G. et al. 2021.** Plastic ingestion as an evolutionary trap: Toward a holistic understanding. *Science* 373, 56–60. DOI:10.1126/science.abh0945.
- **Schlaepfer, M.A., Runge, M.C. & Sherman, P.W. 2002.** Ecological and evolutionary traps. *TREE* 17, 474–480.
- **Stearns, S.C. 1992.** *The Evolution of Life Histories.* Oxford Univ Press.
- **Swaddle, J.P. et al. 2015.** A framework to assess evolutionary responses to anthropogenic light and sound. *TREE* 30, 67–76.
- **Woodcock, B.A. et al. 2017.** Chronic exposure to neonicotinoids reduces honey bee health near corn crops. *Science* 356, 1393–1395.

---

## 11. Empirical refinements from Stage 1 PDE (2026-04-17 addendum)

Stage 1 delivered Layer A animal meta (Δ_ST pooled = +0.72) and 10 human PDEs (5 clean Sweet Traps + 5 discriminant failures). Three *empirical patterns* force refinements to §3 Two-layer model. Each refinement is supported by data from one or more PDEs and extends rather than replaces the v2 core.

### 11.1 Stock vs Flow Sweet Traps (extension of §3.2 L4)

**Empirical motivation**: In C13 housing (`00-design/pde/C13_housing_findings.md`), the Bitter side does not manifest as savings crowd-OUT (as L4 would predict with *C(a, t+k)* = period-k consumption cost). It manifests as **debt crowd-IN**: an additional ¥ of housing debt is associated with ¥0.93 of non-housing debt (p = 0.005). Households service the Sweet Trap by borrowing more, not by saving less. This is incompatible with L4 as written because L4 has no stock variable.

**Formal extension**: Replace action *a_i* with a (flow, stock) pair *(a_i, s_i)*:

$$
U_{i,t}(a_i, s_i) \;=\; \theta_i R(a_i + \eta s_i, S_t) \;-\; (1 - \lambda_i)\beta_i \sum_{k=0}^{K} C(s_i, t+k) \;+\; \rho_i H(s_i, s_{i,\text{past}})
\tag{L4'}
$$

where *η* is the stock-flow coupling parameter (for housing, a new purchase contributes small flow on top of existing stock; for luxury goods, flow and stock are nearly identical; for investments, stock = portfolio, flow = contribution). The summation over *K* periods captures that stock Sweet Traps impose cost streams over long horizons.

**Taxonomy of the 5 confirmed human cases**:

| Case | Dominant type | Bitter signature | Evidence |
|:---|:---|:---|:---|
| C5 Luxury | Mixed (flow with durable stock) | Δsavings = −0.165 (flow-out) + hedonic reset (partial stock) | 576 specs, 68% Bitter forward |
| **C13 Housing** | **Stock** | **Debt crowd-IN**, not savings crowd-OUT | non-housing debt β = +0.93 (p = 0.005) |
| C8 Investment | Stock (portfolio) + flow (new entries) | Portfolio losses realised on exit, not continuously | P(continue\|loss) = 0.718 — stock persistence |
| C12 Short-video | Flow | Sleep, attention loss per day | Within-FE β(heavy_digital, life_sat) = −0.039 |
| D1 Urban | Mixed (stock infrastructure) | Intergenerational cost transfer | Paper 1 cohort dynamics |

**Paper impact**: Main Figure 5 (cross-species Σ_ST map) gains a second axis — **stock-flow dominance**. Sweet Traps toward the "stock" end have longer-lived lock-in (higher ρ), harder exit (lower 2-yr exit rate), and Bitter sides manifesting as debt rather than savings reduction.

### 11.2 Cultural Fisher runaway — *G^c_{τ,y}* replacing *G_{τ,y}* for human social cases (extension of §3.1 L1)

**Empirical motivation**: In C5 luxury (`00-design/pde/C5_luxury_findings.md`), within-person Δ-luxury correlations with life-satisfaction are null (β = +0.004, p = 0.22), while level-luxury correlations are significant (β = +0.020, p < 10⁻¹²). The hedonic-treadmill autocorrelation is *negative* (ρ_AR1 = −0.14, p < 10⁻⁴) — luxury consumption does **not** habituate as classic Berridge incentive-salience predicts. The signal strength depends on *other people's* endorsement (peer coordination), not on the individual's prior exposure.

This contradicts pure M1 (individual neural sensitisation) and instead instantiates M2 (peer-norm dynamics) at a *cultural* rather than *genetic* level. In Lande-Kirkpatrick (Eq. L1–L2), *G_{τ,y}* is genetic covariance. In C5, the analogous quantity is **cultural covariance** — the within-social-network correlation between own luxury preference and peer luxury exposure.

**Formal expression**: For cultural species, extend Eq. L1–L2 by redefining covariance:

$$
G_{\tau,y}^{\text{cultural}} \;=\; \text{Cov}\bigl(y_i, \bar\tau_{j \in N(i)}\bigr)
\tag{L1'}
$$

where *N(i)* is the social network neighbourhood of agent *i* and *τ̄_{j∈N(i)}* is the average trait level among neighbours. When *G^cultural_{τ,y}* exceeds the critical threshold *G^{c,crit}* (derived identically to Lande's genetic threshold), the population enters a **cultural runaway equilibrium**.

This formalises the claim in `phenomenology_archive.md` §C.5 that "the bag's signalling value depends on other people's endorsement — a coordination equilibrium" using the Lande mathematical machinery.

**Support from adjacent literature**:
- Danchin et al. 2018 *Science* — cultural mate-choice in Drosophila already applies Lande-Kirkpatrick with cultural covariance.
- Cavalli-Sforza & Feldman 1981 — formal cultural transmission dynamics with covariance structure.
- Henrich & Boyd 2002 — cultural-genetic coevolution; our *G^cultural_{τ,y}* is their "cultural heritability".

**Paper impact**: §3.1 gets a one-paragraph addition noting that Eq. L1–L2 apply *mutatis mutandis* with *G^cultural* for human social cases, and that C5 luxury is a cultural runaway in the strict Lande sense.

### 11.3 Variable-ratio reward circuit — cross-context isomorphism (extension of §3.3 Bridge)

**Empirical motivation**: Olds-Milner (1954; A6 in Layer A meta, Δ_ST = +0.97) established that rats press levers for direct brain stimulation at rates that exceed rates for food, water, or sex. The reward signal has been severed from any fitness correlate by experimental design. C8 (`00-design/pde/C8_investment_findings.md`) and C12 (`00-design/pde/C12_shortvideo_findings.md`) show that the same architecture is exploited by **financial markets** (variable-ratio returns) and **algorithmic recommendation engines** (variable-ratio content delivery) — both producing the same empirical signature:

| Attribute | A6 Olds-Milner | C8 Investment FOMO | C12 Short-video |
|:---|:---|:---|:---|
| Variable-ratio scheduler | Experimenter-controlled electrode | Market variance + algo-trading | Recommendation engine |
| Dominant reward signal | NAcc dopamine (direct) | Paper gains + FOMO relief | Engagement dopamine + novelty |
| Actual fitness correlate | **None** (by design) | cor(attention, return) = −0.094 (severed in practice) | Sleep loss 0.17–0.45h/day |
| F3 mechanism | M1 neural sensitisation | P(continue\|loss) = 0.718 | ρ_AR1 = 0.71 (strongest in Layer B) |
| Δ_ST | +0.97 [+0.90, +1.00] | +0.060 [+0.024, +0.098] | +0.120 to +0.159 |
| Behavioural signature | Lever-pressing to starvation | Hold after losses | Resist deinstallation |

**Formal claim**: The three cases share the same underlying generative structure — a reward system *designed* (by evolution or by engineers) for learning signal-fitness correlations, deployed in an environment where the signal-fitness correlation has been deliberately zeroed out. This is a special case of F1 Route B (novel/supernormal signal) where the signal-fitness decoupling is *maximal* and *engineered*.

We denote this sub-class **engineered Sweet Traps** and distinguish from *mismatch Sweet Traps* (Route A, evolutionary mismatch) and *runaway Sweet Traps* (Fisher-Lande G_{τ,y}). All three share F1+F2 but have distinctive F3 mechanisms:

| Sub-class | F1 route | F3 mechanism | Example (animal) | Example (human) |
|:---|:---|:---|:---|:---|
| Mismatch ST | A | M1 habit / M4 mortality | Moth, turtle, Drosophila sugar | C11 diet |
| Runaway ST | A (supernormal) | M2 social / genetic G | Peacock, widowbird | C5 luxury, C13 housing |
| **Engineered ST** | **B (novel, designed)** | M1 neural sensitisation | **Olds-Milner**, neonicotinoid bees | **C8 investment, C12 short-video** |

**Paper impact**: Main Figure 2 can be structured as *three 2-panel subfigures*, one per sub-class, each showing an animal exemplar and a human empirical parallel. This unifies the paper's headline claim ("one framework, three variants, cross-species") in a single visual.

### 11.4 Empirical consolidation summary

| v2 original | Stage 1 refinement | Formal update |
|:---|:---|:---|
| §1 F1-F4 (qualitative) | Confirmed F1+F2 as necessary; F3+F4 typical. F2 graded (some cases marginal) | No change; §1 stands |
| §2 Δ_ST operational scalar | Observable on all 5 human cases and 8 animal cases | Confirmed; expand SI Appendix C |
| §3.1 Layer 1 genetic covariance | Extend to cultural *G^cultural_{τ,y}* (§11.2) | **New Eq. L1'** |
| §3.2 Layer 2 L4 utility | Extend flow-stock (§11.1) | **New Eq. L4'** |
| §3.3 Bridge | Three sub-classes: mismatch / runaway / engineered (§11.3) | **New taxonomy table** |
| §4 Propositions P1-P4 | P1 ★★★★★, P4 ★★★★★ confirmed; P3 pending Layer C; P2 requires cross-domain λ heterogeneity | No change; Layer C will resolve |
| §5 Differentiation | C6 保健品 adds "Veblen / belief-consumption" as new adjacent construct (not Sweet Trap due to θ null) | **Add row to Differentiation table** |
| §6 Pipeline | Successfully navigated; Stage 2 integration under way | Replace with Stage 2/3 plan |
| §7 Paper structure | Headline refined: "moth → peacock → LV bag → Douyin" (not 鸡娃/彩礼) | **Update §7 opening** |

---

*End of Sweet Trap Formal Model v2 (with Stage 1 empirical refinements §11, 2026-04-17 addendum). Supersedes `sweet_trap_construct.md` v1 as the theoretical authority for the sweet-trap-multidomain project. All downstream documents (`identification.md`, `specification-map.md`, manuscript drafts, `stage_2_evidence_integration.md`) cite this document.*
