# Positioning — Sweet Trap Theory vs Seven Adjacent Frameworks

**Document**: Formal positioning of Sweet Trap Theory against seven existing theoretical frameworks
**Status**: v1.0, 2026-04-18
**Upstream**: `relationship_to_existing_models.md` (Phase A formal mappings), `axioms_and_formalism.md`, `theorems.md`

**Purpose**: For each adjacent theory, specify (i) formal relationship to Sweet Trap; (ii) empirical distinguishability; (iii) which theorem/axiom marks the departure. Reviewers should be able to confirm: Sweet Trap is not relabeling; it is a strict extension, proper specialisation, or mathematically orthogonal along specified axes.

Seven theories covered:
1. Prospect Theory (Kahneman-Tversky 1979)
2. Rational Addiction (Becker-Murphy 1988)
3. Evolutionary Mismatch (Williams-Nesse 1991; Lieberman 2013)
4. Ecological Trap (Robertson-Hutto 2006)
5. Fisher Runaway (Fisher 1930; Lande 1981)
6. Nudge / Libertarian Paternalism (Thaler-Sunstein 2008)
7. Bounded Rationality / Dual System (Kahneman 2011)

---

## §1 Prospect Theory (Kahneman-Tversky 1979 *Econometrica*)

**Formal relationship**: Mathematically orthogonal. PT operates on reference-dependent valuation of a *single* utility function; Sweet Trap operates on the wedge between *two* utility functions (*U*_perc and *U*_fit).

**Where they differ (axiom level)**: PT has no fitness function; it takes agent preferences as given. Sweet Trap's A1–A2 posit an evolutionarily-grounded *U*_fit distinct from the agent's *U*_perc. This is the foundational divergence: PT is a theory of **subjective valuation under risk**, Sweet Trap is a theory of **decoupling between subjective valuation and objective welfare**.

**Empirical distinguishability**: In a **certain** (non-probabilistic) decision with delayed welfare consequence (e.g., sugary drinks, daily short-video), PT is silent (no risk structure). Sweet Trap predicts escalation via T1. Any observation of Sweet Trap behaviour in risk-free domains distinguishes the two.

**Hybrid**: A "PT-inside-Sweet-Trap" model (§1.2 of `relationship_to_existing_models.md`, Hybrid-1 equation) is derivable: let *U*_perc itself have PT form. The Sweet Trap claim is preserved; PT's probability-weighting contributes to a richer *U*_perc specification. Not part of Paper 1 core.

**One-line**: PT describes how agents weight outcomes under risk; Sweet Trap describes how agent objectives can be systematically decoupled from welfare.

---

## §2 Rational Addiction (Becker-Murphy 1988 *JPE*)

**Formal relationship (Stage 1-B revision, M8)**: Rational Addiction and Sweet Trap occupy **disjoint but boundary-adjacent domains** — they are **conceptual complements** rather than nested models. The earlier framing (RA as a "degenerate specialisation" of Sweet Trap with {*w*=1, *λ*=0, *U*_perc ≡ *U*_fit}) overstated the nesting relationship: RA's foresight assumption is qualitatively distinct from a parameter limit of Sweet Trap.

**Axiom-level position**: RA assumes *U*_perc ≡ *U*_fit — the agent correctly forecasts long-run utility *including addiction dynamics* (tolerance, reinforcement, withdrawal). This assumption by construction precludes Sweet Trap: if *U*_perc ≡ *U*_fit then Δ_ST ≡ 0, which violates the Sweet Trap precondition A2. The two theories therefore apply to **disjoint** domains:

- **RA applies** to agents whose consumption trajectories are consistent with fully-rational forecasting of long-run costs (with discount rate *β* correctly tuned). RA's empirical successes are in domains where agents demonstrably respond to price changes and information in forward-looking ways (Chaloupka 1991 on cigarette demand elasticities).
- **Sweet Trap applies** to agents whose consumption trajectories cannot be rationalised under RA — i.e., A3.0 scope (post-information-intervention abandonment < 30%, or inferred *w* < 0.45). Sweet Trap extends to cases where RA's foresight assumption **fails empirically**.

**Boundary-adjacency**: The two theories share mathematical machinery (discounted-sum utilities, state-dependent payoffs) but differ in their foundational utility object (*U* single vs (*U*_perc, *U*_fit) wedge). An agent population can in principle contain both RA-compliant and Sweet-Trap-scope subpopulations; classification is empirical (via A3.0 criterion).

**Empirical distinguishability**: Paper 2 v2.4 Table 3 reports A3.0 abandonment-rate tests for 12 domains. Domains where abandonment ≥ 30% are excluded from Sweet Trap scope and may be RA-compliant. Domains where abandonment < 30% (C11 diet, C12 short-video, C5 luxury, C6 supplements, C8 investment, C13 housing) are within Sweet Trap scope and RA does not apply. This is the **operational way to distinguish** the two theories, not via nested parameter limits.

**Externalisation (*λ*) note**: Sweet Trap accommodates *λ* > 0 (externalised costs); RA does not model externalisation as a primitive. In domains where *λ* > 0 is observable (bride price paid by elders — C4; parenting investment — C2), Sweet Trap has extra predictive content that RA lacks. This is evidence that the two theories have **partially non-overlapping scope**, not that one subsumes the other.

**One-line**: RA and Sweet Trap are conceptual complements — RA forecloses Sweet Trap by assuming *U*_perc ≡ *U*_fit; Sweet Trap applies precisely to behaviours that look addictive but cannot be rationalised under RA's foresight assumption. The two theories occupy disjoint but boundary-adjacent domains, with the A3.0 criterion determining which theory applies to a given population.

---

## §3 Evolutionary Mismatch (Williams-Nesse 1991; Lieberman 2013)

**Formal relationship**: Mismatch is the **informal precursor** to Sweet Trap. Sweet Trap formalises Mismatch for *behavioural-choice* phenomena, adding endorsement (A3), cost-channel (A4), and non-mismatch subclasses (EST, RST).

$$
\text{Mismatch} \;\subset\; \text{MST} \;\subset\; \text{Sweet Trap}
$$

**Which axioms Mismatch lacks**: A3 (endorsement weight), A4 (cost channel with hyperbolic discount), §7.1 RST (cultural runaway), §7.2 EST (designer-driven). Mismatch has only A1–A2 in informal form.

**Empirical distinguishability**: Mismatch has no quantitative falsification procedure; Sweet Trap has axiom-level falsification (see each axiom's falsifiability section in `axioms_and_formalism.md`). Mismatch predicts "things will go wrong when environment changes"; Sweet Trap predicts **specific rank-ordered patterns** (P1–P5) that Mismatch cannot generate.

**What Sweet Trap adds**:
1. Endorsement condition — why agents *continue* behaviour despite cost.
2. Cost-channel — why cost signals fail to correct.
3. EST — why adversarial design intensifies Mismatch predictions.
4. RST — why cultural runaway can escalate without environmental shift.

**One-line**: Mismatch says "evolved traits can misfire in modern environments"; Sweet Trap specifies *when*, *why*, and *how to intervene*.

---

## §4 Ecological Trap (Robertson-Hutto 2006 *Ecology*)

**Formal relationship**: Ecological Trap is a **cross-species special case** of Sweet Trap restricted to habitat-choice behaviour. Formally:

$$
\text{Eco Trap} \;=\; \text{Sweet Trap}\;\bigg|_{S = \{\text{habitats}\},\;\; \psi = \text{habitat-cue preference},\;\; w_i = 0,\;\; \lambda_i = 0}
$$

with A1 calibrated on pre-disturbance habitat features, A2 activated by anthropogenic disturbance.

**Which axioms are constant**: A1, A2 apply directly. A3 trivialises at *w* = 0 (no belief channel in non-cognitive habitat choice). A4 simplifies (*δ* ≈ 1 for immediate habitat preference; discount not relevant).

**Empirical distinguishability**: Ecological Trap literature focuses narrowly on habitat-selection bugs (reproductive failure in cotton fields with novel-looking vegetation; bird nesting on thermally-lethal artificial surfaces). Sweet Trap extends to:
- Non-habitat choice domains (diet, mate-signal choice, ornament expression).
- Cognitive agents (humans with *w* > 0, elaborated *B*).
- Designer-driven domains (EST not accessible to Eco Trap frame).

**What Sweet Trap upgrades**: from "habitat-choice bug in reproducing vertebrates" to "**general signal-fitness decoupling framework** spanning pre-cognitive to post-cognitive agents and natural to engineered signals".

**One-line**: Ecological Trap is Sweet Trap restricted to habitat choice in non-reflective agents; Sweet Trap is the general-purpose framework.

---

## §5 Fisher Runaway (Fisher 1930; Lande 1981; Kirkpatrick 1982)

**Formal relationship (Stage 1-B revision, M7)**: Fisher Runaway is a **related but distinct theory** — not a strict sub-family of RST. Both describe self-reinforcing dynamics driven by covariance between trait and preference; both use Lande-Kirkpatrick-style equations. The key difference lies in the **objective functional** driving population-level evolution:

- **Fisher Runaway** uses *W̄*_fit (mean fitness): agents/alleles are selected by genetic fitness in the classical Mendelian sense. The dynamical system is **bounded by biological fitness**; runaway equilibria eventually terminate at fitness-collapse boundaries (the peacock's tail cannot grow beyond predation-induced extinction).
- **RST** uses *W̄*_perc (mean perceived utility, derived from L4 / L4.1 mean-field argument): cultural transmission copies agents by their *perceived* success, not their biological fitness. The dynamical system is **bounded only by perceived utility**, which need not bottom out at fitness collapse.

This makes RST a **perceived-utility-driven analogue** of Fisher's genetic-fitness-driven runaway, sharing qualitative logic but operating on formally different dynamical systems. They are therefore best characterised as **parallel theoretical structures** with different primitives, not as a nested family.

**Qualitative commonalities**: trait-preference covariance mechanism; Lande-Kirkpatrick equation structure; line-of-neutral-equilibria under critical covariance threshold.

**Formal differences**: (a) objective functional (*W̄*_fit vs *W̄*_perc); (b) equilibrium structure (fitness-bounded vs perceived-utility-bounded); (c) transmission mechanism (genetic inheritance with Mendelian covariance vs cultural imitation with L4 perceived-success-based copying); (d) scope of inherited traits (phenotypic morphology in Fisher vs any signal/preference pair in RST).

**Consequence**: Fisher runaway equilibria saturate at survival-cost boundaries; RST runaway can escalate indefinitely as long as *U*_perc continues to support it. This explains why luxury-consumption escalation can persist long after fitness-negative thresholds (C5 conspicuous consumption at household-solvency-threatening levels in Paper 2 v2.4 data).

**Empirical distinguishability**: In cultural-trait escalation (luxury spending, education investment, bride price), observe whether escalation saturates at a fitness-cost boundary (Fisher-style dynamics) or continues past it (RST-style dynamics). Paper 2 v2.4 C5 luxury data (household-level spending exceeding 30% of income in high-LTOWVS societies) is RST-consistent; Fisher's fitness-bounded structure cannot accommodate this pattern without additional scaffolding.

**Historical relationship**: We acknowledge Fisher Runaway as the **intellectual precursor** to RST — the mathematical apparatus of trait-preference-covariance dynamics originates with Fisher 1930 and was formalised by Lande 1981 and Kirkpatrick 1982. RST adapts this apparatus to a cultural-transmission setting with W̄_perc, which is a **non-trivial substitution** requiring L4 / L4.1 justification. It is more accurate to describe RST as "inspired by and extending the Lande-Kirkpatrick framework to perceived-utility dynamics" than as "a containment of Fisher Runaway".

**One-line**: Fisher Runaway and RST are related but distinct theories — both use trait-preference covariance dynamics, but Fisher uses fitness-bounded selection while RST uses perceived-utility-bounded cultural transmission. They are parallel structures, not nested families.

---

## §6 Nudge / Libertarian Paternalism (Thaler-Sunstein 2008 *Nudge*)

**Formal relationship**: Nudge is a **policy-intervention philosophy** backed by empirical evidence that choice-architecture changes behaviour. Sweet Trap provides the **theoretical rationale for nudge's differential effectiveness**:

- Where nudges work (default-option changes in retirement savings; choice-architecture in cafeteria food; smart-default organ donation): these are signal-redesign interventions (φ channel) operating in Sweet Trap domains → T2 predicts strong effects.
- Where nudges fail (pure information campaigns; disclosure labels alone): these are B-channel interventions → T2 predicts weak effects.

$$
\text{Nudge effectiveness} \;=\; \text{T2 prediction about which channel is deployed}
$$

**Which theorem matters**: **T2 (Intervention Asymmetry)** directly predicts nudge-effectiveness variation. Nudges that redesign signals win; nudges that only inform lose.

**Empirical distinguishability**: Nudge literature is empirically observed; Sweet Trap provides the **mechanistic explanation**. Where nudges "shouldn't work" by RA (because fully rational agents wouldn't be nudge-sensitive) but do (because *w* < 1 in A3), Sweet Trap predicts the effect size proportional to (1−*w*)/*w*.

**Contribution to nudge literature**: DellaVigna & Linos 2022's finding of ~3× shrinkage academic→field is interpreted by Sweet Trap as the shrinkage of |Δ*b*_info| while signal-redesign interventions preserve their ratio advantage. This explains why field-deployed "nudge units" have had mixed success: they have disproportionately deployed information-channel nudges.

**Policy implication (Paper 1 §7 Discussion)**: Under Sweet Trap, the most effective policy tools in trap domains are **choice-architecture redesign** and **signal-supply regulation**, not information campaigns.

**One-line**: Nudge is the policy practice; Sweet Trap is the theory explaining when nudge wins (signal channel, (1−w)-bounded) and when it loses (info channel, w-bounded).

---

## §7 Bounded Rationality / Dual System (Kahneman 2011 *Thinking, Fast and Slow*)

**Formal relationship**: Dual-system theory posits that human cognition operates through System 1 (fast, automatic, associative) and System 2 (slow, deliberative, rule-based). Sweet Trap is **compatible** with and **refines** dual-system theory by specifying *which* System-1 reward signals have decoupled from System-2 fitness estimates.

**Mapping**:
- *U*_perc ≈ System-1 reward signal (associative, immediate, ⟨ψ, φ⟩-driven).
- 𝔼[*U*_fit ∣ *B*] ≈ System-2 fitness estimate (deliberative, model-based).
- *w* ≈ the weight System-2 has over System-1 in the choice rule.

**Which axiom matters**: **A3** specifies *w* < 1/2 as the Sweet Trap regime. In dual-system terms: Sweet Trap describes cases where System-1 reward dominates System-2 deliberation. This reframes A3 not as a novel assumption but as a specification of the Kahneman regime for a particular class of stimuli.

**Sweet Trap's specific content beyond dual-system**:
1. Identifies *which* System-1 signals are decoupled (A2: novel signals in *S*_mod \ *S*_anc, not all System-1 signals).
2. Provides a formal *U*_perc mechanism (sigmoidal, ψ-calibrated), not just "fast and associative".
3. Adds cost-channel A4 (hyperbolic discount) and externalisation *λ* absent in dual-system theory.
4. Specifies intervention asymmetry T2, absent in dual-system theory.

**Empirical distinguishability**: Dual-system predicts "System-2 can override System-1 with effort". Sweet Trap predicts that even **unbounded** deliberation fails to override (bounded *w* < 1/2 in A3.3; akrasia L3). In Sweet Trap domains, System-2 awareness is insufficient for choice change — a stronger claim than dual-system alone.

**One-line**: Dual-system theory describes the cognitive architecture; Sweet Trap specifies which signals decouple and why deliberative override fails within this architecture.

---

## §8 Summary matrix

| Theory | Formal relationship to Sweet Trap | Key differentiating axiom/theorem | Empirical distinguisher |
|:---:|:---|:---|:---|
| **1. Prospect Theory** | Orthogonal (different utility object) | A1–A2 (fitness function absent in PT) | Certain decisions with delayed cost |
| **2. Rational Addiction** | Conceptual complement (disjoint, boundary-adjacent; Stage 1-B revision) | A3.0 scope criterion distinguishes applicability | A3.0 abandonment-rate test + externalisation *λ* effects |
| **3. Evolutionary Mismatch** | Informal precursor: Mismatch ⊂ MST ⊂ Sweet Trap | A3, A4, §7.1, §7.2 absent from Mismatch | P1–P5 rank-orderings |
| **4. Ecological Trap** | Habitat-choice special case | Non-habitat domains, cognitive agents out of Eco Trap scope | Engineered (EST) instances |
| **5. Fisher Runaway** | Related but distinct theory (parallel, not nested; Stage 1-B revision) | RST uses *W̄*_perc (L4 + L4.1 mean-field); Fisher uses *W̄*_fit | Escalation past fitness-collapse boundary |
| **6. Nudge** | Policy backed by T2 | T2 specifies which nudges win/lose | Signal vs info channel effectiveness |
| **7. Dual System** | Compatible refinement; specifies decoupled System-1 signals | A2 identifies which signals, A3 bounds System-2 override | Unbounded deliberation insufficient |

---

## §9 Containment diagram (visual)

```
                  ┌────────────────────────────────────────────────────┐
                  │              Sweet Trap Theory                     │
                  │  (A1 + A2 + A3[scope A3.0] + A4[P1]; T1-T4)        │
                  │                                                    │
                  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │
                  │  │     MST      │  │     RST      │  │   EST    │  │
                  │  │              │  │ (W̄_perc      │  │          │  │
                  │  │ ⊃ Eco Trap   │  │  via L4/L4.1)│  │ ⊃ Gambling│ │
                  │  │ ⊃ Mismatch   │  │              │  │   design │  │
                  │  │              │  │              │  │ ⊃ Algo    │ │
                  │  │              │  │              │  │   feeds  │  │
                  │  └──────────────┘  └──────────────┘  └──────────┘  │
                  └────────────────────────────────────────────────────┘
                            │                    │
                 parallel-structure       disjoint/boundary-adjacent
                            │                    │
                  ┌─────────▼─────────┐  ┌───────▼──────────────┐
                  │  Fisher Runaway   │  │  Rational Addiction  │
                  │  (W̄_fit,         │  │  (U_perc ≡ U_fit     │
                  │   fitness-bounded;│  │   forecloses ST;     │
                  │   related but     │  │   conceptual         │
                  │   distinct)       │  │   complement)        │
                  └───────────────────┘  └──────────────────────┘

     ┌─────────────────┐                                ┌───────────────┐
     │ Prospect Theory │                                │ Bounded       │
     │  (orthogonal,   │                                │ Rationality / │
     │   compatible    │                                │ Dual System   │
     │   hybrid)       │                                │ (refinement)  │
     └─────────────────┘                                └───────────────┘

                              ┌──────────────────┐
                              │ Nudge / Lib Pat  │
                              │ (policy, backed  │
                              │   by T2)         │
                              └──────────────────┘
```

---

## §10 Consolidated claim

**Sweet Trap Theory is:**
- **Strict extension** of Evolutionary Mismatch (adds A3, A4, RST, EST).
- **Proper generalisation** of Ecological Trap (all habitat-choice special cases recoverable; extends to non-habitat and cognitive domains).
- **Parallel structure to Fisher Runaway** — related but distinct (Stage 1-B revision, M7): shares covariance-dynamics apparatus but operates on W̄_perc (L4 / L4.1) rather than W̄_fit.
- **Conceptual complement to Rational Addiction** — disjoint, boundary-adjacent domains (Stage 1-B revision, M8): RA's *U*_perc ≡ *U*_fit assumption precludes Sweet Trap; A3.0 criterion distinguishes applicability empirically.
- **Mathematically orthogonal** to Prospect Theory (different utility object; hybrid available but not required).
- **Refinement** of Bounded Rationality / Dual System (specifies *which* System-1 signals decouple and why deliberation fails).
- **Theoretical rationale** for Nudge / Libertarian Paternalism (T2 predicts differential effectiveness).

**Sweet Trap Theory is not:**
- A theory of biased beliefs (Bayesian prior errors are orthogonal).
- A cognitive-bias framework (no "illusion" invoked; axioms describe architecture).
- A preference-reversal theory (preferences internally consistent; the wedge is utility-fitness).
- A general welfare-economics framework (specific to reward-calibrated choice).

---

*End of positioning document. Seven adjacent theories mapped; Sweet Trap's contribution specified as strict extension / specialisation / refinement / rationale along each axis.*
