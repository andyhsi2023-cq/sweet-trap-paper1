# Relationship to Existing Models — Sweet Trap Theory (Paper 1)

**Date**: 2026-04-18, v1.0
**Document**: Phase A / Mathematical Foundation — formal positioning
**Predecessors**:
- `axioms_and_formalism.md` §3 (A1–A4)
- `00-design/sweet_trap_formal_model_v2.md` §5 (verbal differentiation table)

**Purpose**: Formal (mathematical, not verbal) comparison between Sweet Trap theory and five adjacent theoretical frameworks. For each, we specify:
1. Formal statement of the adjacent theory's primitives and decision rule;
2. Formal mapping (where it exists) to Sweet Trap primitives;
3. Where the two theories overlap and where they are mathematically orthogonal;
4. The empirical contrast that distinguishes them.

Goal: reviewers should be able to check that Sweet Trap is a **strict theoretical extension** where claimed, a **proper specialisation** where claimed, and **not merely a relabeling** anywhere.

---

## §1 Prospect Theory (Kahneman & Tversky 1979 *Econometrica*)

### 1.1 PT primitives and decision rule

Prospect Theory replaces expected utility *E*[*u*(*x*)] with a weighted value:

$$
V \;=\; \sum_i \pi(p_i) \cdot v(x_i - x_{\text{ref}}) \qquad \text{(PT-1)}
$$

with:
- *v*(·): value function, *concave* for gains (*x* > *x*_ref), *convex* for losses (*x* < *x*_ref), **kinked** at zero with loss aversion coefficient *λ*_PT ≈ 2.25 (Tversky & Kahneman 1992);
- *π*(·): probability weighting function, inverse-S-shaped — over-weights small probabilities, under-weights large ones;
- *x*_ref: reference point — the keystone primitive of PT.

Four axioms (often cited): reference dependence, loss aversion, diminishing sensitivity, probability weighting.

### 1.2 Formal mapping to Sweet Trap

Sweet Trap and PT operate in **mathematically orthogonal** spaces. The orthogonality is precise:

| Axis | Prospect Theory | Sweet Trap |
|:---|:---|:---|
| **Utility domain** | gains/losses *around a reference point* | two distinct utility functions over the same choice |
| **Stochasticity** | probability weighting over uncertain outcomes | expectation over environmental stochasticity (no probability weighting) |
| **Time** | static one-shot decision | continuous-time dynamics over *t*, with hyperbolic discount |
| **Agent population** | representative agent | heterogeneous agents with individual *ψ_i*, *w_i*, *k_i* |
| **Welfare comparison** | implicit (no fitness function) | explicit (Δ_ST = *U*_perc − *U*_fit) |

**Formal statement of orthogonality**: PT is a theory of **single-agent deviations from expected utility**. Sweet Trap is a theory of **wedge between perceived and fitness utility**. Neither subsumes the other; both can be simultaneously true.

**Hybrid model (derivable but not required)**: One may define a "**PT-inside-Sweet-Trap**" hybrid where *U*_perc itself has PT-form:

$$
U_{\text{perc}}(s, t \mid \psi) \;=\; \sum_i \pi_\psi(p_i) \cdot v_\psi(\varphi_i(s, t) - \varphi_{\text{ref}, \psi}) \qquad \text{(Hybrid-1)}
$$

In this hybrid, *ψ* parametrises the reference point, value function shape, and probability weighting. The Sweet Trap claim (A2 decoupling, A3 endorsement-inertia) still holds: even if each choice is evaluated via PT weighting, the outcome *U*_perc still diverges from *U*_fit under A2. The hybrid formalism is useful for domains where risk (gambling: C12) is central but is not part of the Paper 1 core theory.

### 1.3 Where they overlap

**Kinked value function** *v* ≈ reward-architecture adaptation to asymmetric cost-benefit in ancestral environment. If A1 is granted, the PT *v* shape is *derivable* from the ancestral calibration of *ψ* (Robson 2001 *JEL*; Rayo & Becker 2007 *JPE*). This is **not a claim we make in Paper 1**; it is a bridge opportunity for a future paper.

### 1.4 Where they differ sharply (empirical contrast)

**PT does not predict** that agents endorse signals with *U*_fit < 0 (PT has no fitness function to measure *U*_fit against). PT predicts preference reversals *within* the agent's subjective valuation.

**Sweet Trap does not predict** probability-weighting distortions as such; those are orthogonal phenomena.

**Crucial empirical divergence**: In a domain where the Sweet signal is certain (not probabilistic — e.g., daily screen-time, not gambling), PT has no prediction. Sweet Trap does: A2 + A3 produce escalation of engagement.

### 1.5 One-line summary

PT is about how agents subjectively weight outcomes under risk. Sweet Trap is about how the *entire subjective objective function* can be decoupled from fitness. The two coexist in the same behavioural space without formal redundancy.

---

## §2 Rational Addiction (Becker & Murphy 1988 *JPE*)

### 2.1 RA primitives and decision rule

A representative agent chooses consumption *c_t* of an addictive good to maximise:

$$
\sum_{t=0}^\infty \beta^t \, u(c_t, S_t, y_t) \qquad \text{(RA-1)}
$$

subject to:
- Addictive stock dynamics: *S*_{*t*+1} = (1 − *δ*) *S_t* + *c_t* (depreciation + accumulation);
- Budget constraint: *y_t* + *p_t* *c_t* ≤ *M*;
- Tolerance: ∂*u*/∂*S* ≤ 0 (higher addictive stock reduces utility);
- Reinforcement: ∂²*u*/∂*c*∂*S* ≥ 0 (higher stock raises marginal utility of consumption).

The RA agent is **fully forward-looking** (perfectly rational), maximises expected lifetime utility, with no belief error and no welfare-economic wedge.

### 2.2 Formal mapping to Sweet Trap (Stage 1-B revision, M8)

**Revised framing**: RA and Sweet Trap are **conceptual complements** — they occupy **disjoint but boundary-adjacent domains**, not a nested specialization relationship. The earlier framing (RA as "Sweet Trap with {*w*=1, *λ*=0, *U*_perc ≡ *U*_fit}") overstated the structural equivalence: RA's foresight assumption is qualitatively different from a parameter limit of Sweet Trap.

**Why not nested**: Setting *w* = 1 + *U*_perc ≡ *U*_fit in Sweet Trap equations does yield a single-utility system formally similar to RA, but this operation is not a "parameter limit" — it is a **change of foundational premise**. Sweet Trap's A2 (environmental decoupling producing Δ_ST > 0) is violated by construction when *U*_perc ≡ *U*_fit. The resulting system is a **different theory altogether**, not a degenerate Sweet Trap.

**Correct positioning**: RA and Sweet Trap answer different questions:
- **RA answers**: Given an agent who correctly forecasts long-run utility including addiction dynamics, how do they optimise consumption?
- **Sweet Trap answers**: Given an agent whose reward calibration *ψ* was shaped by *S*_anc and who now faces *S*_mod, how do they choose?

These questions are **not nested**; they have disjoint agent-population scopes.

**Boundary-adjacency**: A3.0 criterion (see `axioms_and_formalism.md`) provides the empirical partition. Populations with post-information-intervention abandonment rate ≥ 30% may be RA-compliant and are **outside Sweet Trap scope**. Populations with abandonment rate < 30% are **within Sweet Trap scope** and RA does not apply — their behavioural patterns cannot be rationalised under RA's foresight assumption.

**Shared mathematical machinery**: Both theories use discounted-sum utilities and state-dependent payoffs. But their foundational utility objects differ (single *U* vs wedge (*U*_perc, *U*_fit)), making cross-theory predictions non-translatable.

**Empirical implication**: RA predicts large choice updates upon information provision (rational agents update forward-looking valuations). Sweet Trap (within A3.0 scope) does not — because *w* < 0.45 caps the weight of belief-driven choice. The A3.0 abandonment test is therefore the **operational method to distinguish which theory applies** to a given population, not a "test of which theory is true in general".

### 2.3 Empirical divergence

| Test | RA prediction | Sweet Trap prediction | Domain |
|:---:|:---|:---|:---:|
| Information intervention | Substantial choice update if beliefs shift | Minor update (bounded by 1 − (1 − *w*_max)) = bounded by 0.5 | All Sweet Trap domains |
| Price shock (tax) | Significant reduction proportional to *e*_price | Response is blunted if *α* · ∂*U*_perc/∂*s* is large (reward dominates) | Diet (C11), housing (C13) |
| Externalisation (*λ* > 0) | No effect (not in RA) | Σ_ST scales with *λ* | Bride price (C4), parenting (C2) |

**Discriminating prediction**: In domains where *λ* > 0 is observably present (cohort-level cost shifting), RA fails but Sweet Trap predicts observed pattern.

**V2 §5 v.s. this document**: V2's differentiation was verbal ("RA is the closest construct but has λ = 0"). Stage 1-B revision explicitly corrects the intermediate "specialisation" framing: **RA is not a specialisation of Sweet Trap; the two are conceptual complements with disjoint agent-scope determined by the A3.0 criterion**. The three distinguishing features (*U*_perc ≡ *U*_fit foresight assumption; absence of *λ* primitive; large-information-response prediction) partition the two theories' applicability domains rather than nest one within the other.

### 2.4 One-line summary (Stage 1-B revision)

RA and Sweet Trap are conceptual complements: RA's foresight assumption (*U*_perc ≡ *U*_fit) by construction precludes Sweet Trap (Δ_ST ≡ 0). Sweet Trap extends to behaviours that look addictive but cannot be rationalised under RA's foresight; the two theories occupy disjoint but boundary-adjacent domains with the A3.0 criterion determining applicability empirically.

---

## §3 Evolutionary Mismatch (Lieberman 2013 *The Story of the Human Body*; Nesse 2005 *Evol Hum Behav*)

### 3.1 Mismatch primitives

Evolutionary mismatch is an **informal theoretical frame**, not a formal model. Its primitives:
- Ancestral environment *E*_anc with selection pressures ∇*W*_anc.
- Modern environment *E*_mod with distinct selection pressures ∇*W*_mod.
- A trait *T* (physiological or psychological) shaped by *W*_anc.
- Maladaptation: ∇*W*_mod · *T* < 0.

No formal decision rule; no time dynamics; no individual heterogeneity; no cost-feedback channel.

### 3.2 Formal mapping to Sweet Trap

Sweet Trap is the **formalisation of evolutionary mismatch** for the *behavioural/preference* class of traits, with specific additions:

- Mismatch's "trait *T*" = Sweet Trap's reward-calibration *ψ_i*.
- Mismatch's "*E*_anc vs *E*_mod" = Sweet Trap's distinction between *S*_anc and *S*_mod (A1 / A2).
- Mismatch's "maladaptation" = Sweet Trap's Δ_ST > 0 on *S*_mod \ *S*_anc.

**Sweet Trap is STRICT EXTENSION of Mismatch**:
1. Mismatch has no endorsement condition; Sweet Trap adds A3 (rational-endorsement from the agent's perspective).
2. Mismatch has no cost-channel formalism; Sweet Trap adds A4 (hyperbolic discount + partial visibility).
3. Mismatch has no RST-like self-amplification; Sweet Trap includes cultural runaway (§7.1).
4. Mismatch has no EST subclass; Sweet Trap formalises designer-driven Δ_ST maximisation.

**Formal relation**: **Evolutionary Mismatch ⊂ MST ⊂ Sweet Trap**.

Every mismatch phenomenon with an endorsement signature is an MST. Mismatches without endorsement (e.g., physiological malfunctions: UV damage to skin in industrial latitudes) are not Sweet Traps — they lack F2.

### 3.3 Empirical divergence

- Mismatch: supports cross-cultural evolutionary-psychology claims but has no falsification procedure beyond "was the modern trait not in the ancestral environment?".
- Sweet Trap: has formal falsification at the axiom level (see each axiom's falsifiability section) + the empirical Δ_ST > 0 test.

### 3.4 One-line summary

Sweet Trap formalises the mismatch frame for reward-driven choice, adds endorsement + cost-channel machinery, and includes non-mismatch subclasses (EST, RST-novel) that mismatch cannot reach.

---

## §4 Fisher Runaway (Fisher 1930; Lande 1981; Kirkpatrick 1982)

### 4.1 Fisher-Lande-Kirkpatrick primitives

State variables at population level: trait mean *τ̄* (e.g., peacock tail length) and preference mean *ȳ* (female preference strength). Dynamics:

$$
\dot{\bar\tau} \;=\; G_\tau \partial_\tau \bar W + G_{\tau, y} \partial_y \bar W \qquad \text{(FR-1)}
$$

$$
\dot{\bar y} \;=\; G_y \partial_y \bar W + G_{\tau, y} \partial_\tau \bar W \qquad \text{(FR-2)}
$$

with *G_τ*, *G_y* additive genetic variances, *G*_{*τ*,*y*} the key trait-preference covariance. **Lande's theorem**: when *G*_{*τ*,*y*} > *G*^crit, the system admits a line-of-neutral-equilibria (runaway).

### 4.2 Formal mapping to Sweet Trap (Stage 1-B revision, M7)

**Revised framing**: Fisher Runaway and RST are **related but formally distinct dynamical systems** — not a strict containment relation. Both use Lande-Kirkpatrick-style equations, but they operate on different objective functionals:

- **Fisher-Lande-Kirkpatrick**: dynamics driven by *W̄*_fit (mean biological fitness). Runaway equilibria are fitness-bounded — escalation terminates at fitness-collapse boundaries (peacock tail cannot outgrow predation-induced extinction).
- **RST**: dynamics driven by *W̄*_perc (mean perceived utility, derived via L4 + L4.1 mean-field argument from cultural-transmission theory). Runaway equilibria are perceived-utility-bounded — escalation can continue past fitness-negative thresholds as long as the cultural reward signal continues to support it.

**Shared apparatus**: trait-preference covariance *G*_{*q*,*y*} (or its cultural analogue *G*^c); Lande-Kirkpatrick equation structure (FR-1)–(FR-2); line-of-neutral-equilibria under critical covariance threshold.

**Non-shared content**: (a) objective functional (*W̄*_fit vs *W̄*_perc); (b) transmission mechanism (Mendelian genetic inheritance vs cultural L4 perceived-success imitation); (c) boundary structure (fitness collapse vs perceived-utility continuation); (d) scope of traits (phenotypic morphology vs any signal/preference pair).

**Formal status**: Fisher Runaway and RST are **parallel theoretical structures** sharing apparatus but differing in primitives. We do not claim Fisher ⊂ RST as a set-containment relation; rather, RST **adapts** the Lande-Kirkpatrick framework to a cultural-transmission setting via the L4/L4.1 substitution.

**Historical positioning**: Fisher 1930 → Lande 1981 → Kirkpatrick 1982 is the intellectual precursor lineage for RST's mathematical apparatus. We acknowledge this lineage explicitly. RST's novel contribution is the W̄_perc substitution (L4 + L4.1), which is not a Fisher-style restriction but a genuine theoretical extension to cultural dynamics.

**FR-I–FR-IV restrictions (historical note)**: The earlier "four-restriction" framing listed Fisher-specific modelling choices (mate-choice signals; genetic *ψ*; no external designer; reproductive-cost only). These are **descriptive properties** of the Fisher model, not "restrictions" that reduce RST to Fisher. A Fisher-style system arises when one combines the Lande-Kirkpatrick apparatus with these specific primitive choices; this is a separate theoretical object, not a parameter-limit of RST.

### 4.3 V2 §5 refinement — Sweet Trap is not Fisher Runaway (Stage 1-B revision)

Fisher Runaway is definitionally a *sexual selection* phenomenon operating on genetic covariance. Sweet Trap (and specifically RST) spans domains where sexual selection is absent (screen-time, luxury consumption outside mate-choice context, gambling) and uses cultural-transmission dynamics (L4 / L4.1) in place of Mendelian genetic inheritance. The two theories therefore operate on **different primitives** — they share apparatus but are not nested families.

### 4.4 One-line summary (Stage 1-B revision, M7)

Fisher Runaway and RST are related but distinct dynamical systems — both use Lande-Kirkpatrick-style covariance equations, but Fisher operates on *W̄*_fit (biological, fitness-bounded) while RST operates on *W̄*_perc (perceived, L4/L4.1-derived, unbounded). They are parallel theoretical structures sharing intellectual lineage, not nested families.

---

## §5 Zahavi Handicap Principle (Zahavi 1975 *J Theor Biol*)

### 5.1 Zahavi primitives

A trait *T* is **honest** iff the cost of producing/maintaining *T* is greater for low-quality than for high-quality individuals — the "handicap" imposes a differential signal-cost that selects against cheating.

Formally: *T* is honest iff the selection-gradient against cheaters satisfies:

$$
\partial_T \bar W_{\text{cheater}}(T) \;<\; \partial_T \bar W_{\text{honest}}(T) \qquad \text{(Z-1)}
$$

for all sufficiently large *T*.

### 5.2 Formal mapping to Sweet Trap

Zahavi is a theory of **signal reliability**, not a theory of decoupling. Its relation to Sweet Trap:

**Sweet Trap ⊃ Zahavi-failure**: A Zahavi signal that STOPS being honest (e.g., because the cost-structure changes, or because the signal-receiver's *ψ* is calibrated on the old cost-structure while the new signal is artificially cheap to produce) becomes a Sweet Trap.

Examples:
- **Luxury-goods counterfeiting**: original Zahavi-honest status signal (genuine LV bag) becomes Zahavi-failed in the presence of high-quality replicas. Receivers' *ψ* is still calibrated on the signal → Δ_ST > 0 on replicas. This is an MST-like pattern within a Zahavi frame.
- **Height-elevator shoes / cosmetic surgery**: formerly-honest physical markers gamed by artificial augmentation. Signal-receivers' *ψ* still triggers; fitness benefit to sender is hijacked.

**Formal relation**: **Zahavi-failure → Sweet Trap (of the receiver of the signal)**. Specifically, the receiver becomes the Sweet Trap agent; the sender exploits the receiver's *ψ*.

Interestingly, this maps to the EST subclass where the "designer" *j* is the sender who optimises signal-appearance without paying the honest cost.

### 5.3 One-line summary

Zahavi describes when signals remain honest; Sweet Trap describes what happens when they stop (either by environmental shift or by adversarial signalling) — the receiver of a failed honest signal becomes a Sweet Trap agent.

---

## §6 Summary Matrix

| Model | Relation to Sweet Trap | Formal criterion | Empirical domain |
|:---:|:---|:---|:---|
| **Prospect Theory** | Orthogonal | Different utility object: *v*(*x* − *x*_ref) vs Δ_ST = *U*_perc − *U*_fit | Risk decisions |
| **Rational Addiction** | Conceptual complement (disjoint; Stage 1-B revision) | A3.0 criterion partitions applicability; RA assumes *U*_perc ≡ *U*_fit | Addictive consumption (A3.0 classifies population) |
| **Evolutionary Mismatch** | Informal precursor | Mismatch ⊂ MST ⊂ Sweet Trap | Behavioural mismatches |
| **Fisher Runaway** | Related but distinct (parallel; Stage 1-B revision) | Both use Lande-Kirkpatrick apparatus; Fisher uses *W̄*_fit, RST uses *W̄*_perc (L4/L4.1) | Sexual selection vs cultural escalation |
| **Zahavi Handicap** | Failure-complement | Zahavi-failure → Sweet Trap for signal receiver | Honest/dishonest signalling |

---

## §7 Non-claim: what Sweet Trap is NOT

To preempt reviewer confusion:

- **Sweet Trap is not a theory of biased beliefs.** Agents may have correct or incorrect beliefs; A3 specifies that their beliefs receive bounded weight *w* < ½ regardless of belief accuracy.
- **Sweet Trap is not a cognitive-bias framework.** No "cognitive illusion" is invoked; the axioms describe architecture (A1, A2), decision rule (A3), and cost signal (A4).
- **Sweet Trap is not a preference-reversal theory.** Preferences can be consistent; the divergence is between *U*_perc (which drives choice) and *U*_fit (which drives welfare). Both are internally consistent.
- **Sweet Trap is not a general welfare-economics framework.** It is specific to reward-calibrated choice. It has nothing to say about e.g., pure tax-compliance decisions or pure-information-processing bias.

---

## §8 What Sweet Trap uniquely predicts

Propositions (from Paper 1 §03-predictions/, forthcoming Phase C) that **no single adjacent model** predicts:

- **P-unique 1**: Sweet Trap engagement is an ESS **despite** negative *U*_fit. (PT silent; RA predicts quitting; Mismatch has no ESS machinery; Fisher yes but only for mate signals; Zahavi not applicable.)

- **P-unique 2**: Interventions on signal distribution (reducing *φ* in Φ) dominate interventions on belief *B*. (RA silent — RA has no *ψ*; PT predicts belief effects should matter more; Mismatch silent; Fisher silent.)

- **P-unique 3**: Δ_ST is conserved across species with homologous reward architecture (moth + human) when evaluated on equivalent signal-shift distance. (No adjacent model spans cross-species; Mismatch implies but does not predict quantitative conservation.)

- **P-unique 4**: Engineered Sweet Traps (EST) exhibit higher Δ_ST than Mismatch Sweet Traps (MST). (No adjacent model distinguishes mechanism-of-origin for decoupling.)

These four unique predictions are the empirical content that distinguishes Sweet Trap from any adjacent theory. Each is targeted in Paper 1 §03-predictions/.

---

## §9 Containment diagram

```
                          ┌────────────────────────────────────┐
                          │          Sweet Trap                │
                          │   (A1 + A2 + A3 + A4, §3)          │
                          │                                    │
                          │   ┌────────────┐   ┌───────────┐   │
                          │   │    MST     │   │    RST    │   │
                          │   │  (Route A) │   │  cultural │   │
                          │   │            │   │  runaway  │   │
                          │   │ ⊃ Eco trap │   │ ⊃ Fisher  │   │
                          │   │ ⊃ Mismatch │   │    runaway│   │
                          │   └────────────┘   └───────────┘   │
                          │   ┌──────────────────────────────┐ │
                          │   │           EST                │ │
                          │   │   (designer-driven, §7.2)    │ │
                          │   │   ⊃ Olds-Milner              │ │
                          │   │   ⊃ Variable-ratio gambling  │ │
                          │   │   ⊃ Algorithmic feeds        │ │
                          │   └──────────────────────────────┘ │
                          └────────────────────────────────────┘

                          [Orthogonal: Prospect Theory — different axis]
                          [Conceptual complement (Stage 1-B): Rational Addiction — 
                             RA assumes U_perc ≡ U_fit, forecloses ST by construction;
                             A3.0 criterion partitions agent populations]
                          [Parallel structure (Stage 1-B): Fisher Runaway — 
                             shares Lande-Kirkpatrick apparatus; Fisher uses W̄_fit,
                             RST uses W̄_perc (L4/L4.1); related but formally distinct]
                          [Complementary: Zahavi honest signalling — 
                             its failure mode enters Sweet Trap via receiver]
```

---

*End of relationship document. This file, together with `axioms_and_formalism.md` and `nomenclature.md`, constitutes the complete Phase A mathematical foundation for Paper 1. Phase B will derive theorems on this basis.*
