# Weak Joints Resolution — Phase A → Phase B

**Document**: Formal resolution of weak joints in Phase A axiomatic foundation
**Status**: v1.0, 2026-04-18
**Companion**: `theorems.md`, `lemmas.md`, `axioms_and_formalism.md`

**Purpose**: Two weak joints were flagged during Phase A review:
1. **A3 endorsement ceiling *w*_max boundary behavior** — what happens as *w*_max approaches 1/2, and is the strict inequality *w*_max < 1/2 sustainable?
2. **RST use of *W̄*_perc in lieu of *W̄*_fit** — is the replacement mathematically justified, or is it an ad-hoc substitution?

This document provides formal resolutions. Each resolution states: (i) the precise issue, (ii) the resolution strategy (tighten, relax, or reinterpret), (iii) the rationale, and (iv) the downstream consequences for theorem statements.

---

## §1 Weak Joint #1: A3 *w*_max boundary — dominance vs degradation

### §1.1 The issue

A3.3 asserts *w_i* ≤ *w*_max < 1/2, with MC-5 committing *w*_max = 0.4 as the theoretical default. Theorem T2's dominance result

$$
|\Delta b_{\text{signal}}|/|\Delta b_{\text{info}}| \;\geq\; (1 - w_{\max})/w_{\max}
$$

is strict when *w*_max is strictly less than 1/2 but **degenerates** as *w*_max → 1/2 (the ratio → 1, no dominance). Question: is *w*_max = 0.4 a safe margin from this degradation, or is the theorem fragile near *w*_max = 0.5?

Additionally: in populations where the empirically estimated effective *w* is 0.45 or higher (possibly in highly informed populations on well-studied risks), does T2 fail?

### §1.2 Resolution: two-tier interpretation of *w*_max

**Tier A (Strict Dominance regime)**: *w*_max ≤ 0.45

- (1 − *w*_max)/*w*_max ≥ 0.55/0.45 ≈ 1.22.
- T2 delivers **strict** inequality with margin γ > 0 (from T2 Step 3).
- **Canonical Sweet Trap domains**: C5 luxury, C6 health supplements, C8 investment, C11 diet, C12 short-video, C13 housing, C14 gambling — all Paper 2 v2.4 domains fall in Tier A by empirical estimation of effective *w*.

**Tier B (Probabilistic Dominance regime)**: *w*_max ∈ (0.45, 0.5)

- (1 − *w*_max)/*w*_max is close to 1 but still > 1.
- T2 delivers **stochastic** dominance: 𝔼[|Δ*b*_signal|] > 𝔼[|Δ*b*_info|], but the margin is small.
- Example boundary case: *w*_max = 0.49 gives ratio ≈ 1.04; dominance holds only in expectation, not for every realisation.

**Tier C (Rejected / out of scope)**: *w*_max ≥ 0.5

- A3.3 is violated. The agent is outside Sweet Trap scope.
- The theory simply doesn't apply. This is not a weakness of T2 but a specification of its scope.

### §1.3 Downstream consequence for Paper 2

Paper 2's empirical work reports the effective *w* estimated from each domain. If *w* is in Tier A, the "law of intervention effectiveness" holds as a **deterministic inequality**. If *w* is in Tier B, the law holds as a **probabilistic inequality** (effect of signal redesign > effect of information, in expectation). Paper 2's v2.4 effect-size distribution (median ratio ~2.0×) suggests Tier A is the empirically relevant regime.

**Recommendation**: Paper 2 reports *w* estimates per domain; Paper 1 Theorem T2 is qualified: "under Tier A regime (*w*_max ≤ 0.45), strict dominance with γ ≥ 0.5; under Tier B regime (*w*_max ∈ (0.45, 0.5)), probabilistic dominance with margin shrinking as *w*_max → 0.5."

### §1.4 Why not tighten A3.3 to *w*_max < 0.45?

A tempting resolution is to simply commit MC-5 to *w*_max ≤ 0.45 to avoid Tier B altogether. We **reject** this for three reasons:

1. **Empirical testability**: Keeping *w*_max as an estimable parameter (with theoretical ceiling 0.5) allows empirical estimation and falsification. If we commit *w*_max = 0.45, we conflate theory with parameter choice.

2. **Paper 1 theoretical generality**: A3.3's strict inequality *w*_max < 1/2 is the **minimum** requirement for the Sweet Trap concept to make sense (perceived utility must dominate, however narrowly). Restricting further would unnecessarily narrow the theory.

3. **Empirical estimability**: Revealed-preference estimation (e.g., via the discrepancy between stated beliefs about health harm and actual consumption) typically yields point estimates of effective *w* in [0.15, 0.35] — well within Tier A. The Tier A/B boundary is a rare-event concern.

### §1.5 Formal re-statement of T2 (post-resolution)

**T2 (tier-aware version)**: Under A1–A4 with *w_i* ≤ *w*_max:

(i) If *w*_max ≤ 0.45 (Tier A): |Δ*b*_signal|/|Δ*b*_info| ≥ (1−*w*_max)/*w*_max ≥ 1.22, with population margin γ ≥ 0.5.

(ii) If 0.45 < *w*_max < 0.5 (Tier B): 𝔼[|Δ*b*_signal|] > 𝔼[|Δ*b*_info|], with population margin γ → 0 as *w*_max → 0.5.

(iii) If *w*_max ≥ 0.5: A3.3 violated, Sweet Trap scope not applicable.

The canonical statement in `theorems.md` §T2 uses the Tier A version (*w*_max ≤ 0.4), which is the MC-5 commitment; the tier-aware version is provided here for completeness.

---

## §2 Weak Joint #2: RST uses *W̄*_perc instead of *W̄*_fit

### §2.1 The issue

RST's Lande-Kirkpatrick dynamics (§7.1 of axioms, equations 7.2 and 7.3):

$$
\dot{\bar q} \;=\; G_q \frac{\partial \bar W_{\text{perc}}}{\partial \bar q} \,+\, G_{q,y}^c \frac{\partial \bar W_{\text{perc}}}{\partial \bar y}
$$

The original Lande 1981 derivation used *W̄* (mean fitness). Phase A RST substitutes *W̄*_perc (mean perceived utility). This substitution was flagged as a "critical extension" but not formally justified. Question: is the substitution mathematically valid, or is it an ad-hoc move to rescue cultural runaway under Sweet Trap assumptions?

### §2.2 Resolution: the substitution is justified by cultural transmission dynamics

**Key insight**: Lande's derivation models **genetic inheritance**. The "selection gradient" ∂*W̄*/∂*q̄* represents the differential reproductive success of individuals with different *q* values. This is fundamentally fitness.

When we generalise to **cultural transmission**, the "copying" is no longer driven by reproductive success (cultural models need not be biologically-fit; they're socially-observed). Cultural models are selected based on their **apparent success** — their displayed status, popularity, or perceived utility. This is *U*_perc, not *U*_fit.

**L4** (in `lemmas.md`) formalises this: under standard cultural-evolution assumptions (Cavalli-Sforza & Feldman 1981; Boyd & Richerson 1985; Henrich-McElreath 2003), the selection gradient in the cultural case is ∂*W̄*_perc/∂*q̄*.

**Therefore**: equations (7.2)–(7.3) in `axioms_and_formalism.md` §7.1 are **not** a modification of Lande — they are the **correct** cultural analogue. Lande's *W̄* → *W̄*_perc is not ad-hoc; it is the systematic substitution required when moving from genetic to cultural transmission.

### §2.3 Consequence: the cultural runaway is "stronger" than Fisher runaway

**Genetic Fisher runaway** (Lande 1981): *τ̄* (trait) and *ȳ* (preference) co-evolve driven by ∂*W̄*_fit/∂*q̄*. When *G*_{*τ*,*y*} > *G*^crit, the system has a line of neutral equilibria.

**Cultural RST runaway** (Paper 1 §7.1): *q̄* and *ȳ* co-evolve driven by ∂*W̄*_perc/∂*q̄*. Because *W̄*_perc can decouple from *W̄*_fit (A2), the dynamic can amplify traits that are **maladaptive** in fitness terms.

In other words, cultural runaway is **not constrained by fitness**. This is why luxury-consumption escalation can persist long after it becomes fitness-negative (e.g., conspicuous consumption at levels threatening household solvency: C5 case).

### §2.4 Corollary for paper structure

The RST sub-class is where Sweet Trap theory **most sharply diverges** from classical Fisher runaway. Paper 1's §04-positioning (forthcoming) should highlight this:
- Fisher runaway is fitness-bounded: the trait cannot escalate indefinitely because *W̄*_fit eventually opposes it.
- RST (Sweet Trap cultural runaway) is **perceived-utility bounded**: the trait escalates as long as *W̄*_perc continues to support it, which under A2 can persist indefinitely even as *W̄*_fit collapses.

### §2.5 Citation infrastructure

The lemma L4 cites:
- Richerson, P. J., & Boyd, R. (2005). *Not by Genes Alone*. Chicago.
- Henrich, J. (2015). *The Secret of Our Success*. Princeton.
- Cavalli-Sforza & Feldman 1981, Boyd & Richerson 1985, Henrich-McElreath 2003.

These establish that cultural transmission is driven by observed perceived success, not fitness. The substitution is the **consensus** in cultural-evolution theory, not a novel move.

---

## §3 Summary of resolutions

| Weak joint | Resolution strategy | Formal impact | Downstream |
|:---|:---|:---|:---|
| **#1** *w*_max boundary | Two-tier interpretation: Tier A (strict) and Tier B (probabilistic) dominance | T2 statement refined; γ → 0 at *w*_max = 0.5 | Paper 2 reports *w* estimates per domain |
| **#2** RST *W̄*_perc | Formal lemma L4 + cultural-transmission literature | RST formalism validated; not ad-hoc | Paper 1 §04-positioning highlights divergence from Fisher |

---

## §4 Other potential weak joints reviewed (no action taken)

The following were flagged in Phase A note-taking but determined to not require Phase B resolution:

### §4.1 MC-4 *ρ*_crit = 0.3 default

**Issue**: Why 0.3 specifically?

**Decision**: Already addressed with sensitivity sweep in MC-4 (range [0.2, 0.5] preserves qualitative conclusions). No action required in Phase B; sensitivity analysis is part of Paper 1 §03-predictions.

### §4.2 MC-6 hyperbolic vs quasi-hyperbolic

**Issue**: Could use Laibson β-δ instead of pure hyperbolic.

**Decision**: Keep pure hyperbolic per MC-6; Laibson β-δ is a convex combination and doesn't sharpen results. No action in Phase B; sensitivity to exponential form is in Paper 1 §03-predictions robustness.

### §4.3 A3's scope exclusion for "coerced exposure"

**Issue**: How to operationally distinguish voluntary endorsement from coerced exposure?

**Decision**: Handled by F2 operationalisation in `discriminant_validity_v2.md` §1.3. The F2 "endorsement signature" measurement protocol already discriminates coerced exposures (C2/D3 negative controls). No additional Phase B work required.

### §4.4 Bellman extension for state-dependent *W*

**Issue**: MC-3 allows state-dependent fitness via Bellman functional (§2.2 of axioms). Is this formalised in Phase B theorems?

**Decision**: Not required for T1–T4. The time-separable case suffices. State-dependent extension is reserved for a sub-paper on rational-addiction-like dynamics, flagged as Phase D work.

---

*End of weak joints resolution document. Two Phase A concerns formally resolved; theory is consistent for Phase B theorem proofs.*
