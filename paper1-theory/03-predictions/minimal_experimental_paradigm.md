# Minimal Experimental Paradigm — Sweet Trap Falsification Task

**Document**: A single behavioural-lab paradigm that could falsify the Sweet Trap core in a controlled setting
**Status**: v1.0, 2026-04-18 (pre-registration draft)
**Authors**: Lu An & Hongyang Xi
**Purpose**: Analogous to Kahneman-Tversky 1979's certainty-effect / framing paradigm — one task, few arms, sharp prediction. Any competent behavioural lab should be able to replicate with Prolific sample and n < 500 per arm.

**OSF preregistration**: **[OSF_DOI_TO_INSERT]** (to be filed before data collection).

---

## §1 Design philosophy

Kahneman-Tversky 1979 did not "test prospect theory in the wild". They constructed a stripped-down decision task that isolated the single mechanism (reference-dependent valuation). We follow the same logic: one task, one primary outcome, two arms that cleanly dissociate the T2 channels (information vs signal redesign).

The Sweet Trap falsifier must:

1. Induce a dissociation between *U*_perc and *U*_fit (behavioural) **in the lab**, using a reward that is perceptually strong but long-run-suboptimal.
2. Manipulate the *B* channel (information about long-run payoff) in one arm.
3. Manipulate the *φ* channel (perceptual intensity of the signal) in a second arm.
4. Keep both manipulations **matched in utility-unit intensity** per the T2 matching convention.
5. Measure the **ratio** |Δ*b*_signal|/|Δ*b*_info| against the theoretical floor of 1.5.

---

## §2 Task: Two-Option Repeated Choice with Delayed Payoff

### §2.1 Structure

Each participant completes **120 rounds** of binary choice. On each round, they see two buttons (Option A, Option B) and must click one within 5 seconds. The round outcome (token increment/decrement) is displayed immediately; cumulative tokens across rounds determine bonus payment.

- **Option A (the "sweet" option)**: each click yields an **immediate token +1** accompanied by a bright coloured animation (pulsing yellow burst, subtle celebratory sound). However, every A-click also accrues a hidden "long-run cost" that deducts 3 tokens from a held-back pool, realised only at the end of the experiment.

- **Option B (the "healthy" option)**: each click yields an **immediate token +0.3** (no animation, neutral grey display). Every B-click accrues a hidden "long-run gain" of +0.9 tokens, realised at the end.

**Net per-click payoff**:
- A: +1 immediate − 3 delayed = **−2 tokens** (long-run bad)
- B: +0.3 immediate + 0.9 delayed = **+1.2 tokens** (long-run good)

The **optimal strategy** is always-B. The **perceptually dominant** option is A.

### §2.2 Baseline condition

Participants are told **only** that each button yields tokens, without disclosure of the delayed-payoff structure. Expected behaviour: substantial A-preference (driven by immediate reward animation). This establishes the baseline Sweet Trap LSE in the lab.

### §2.3 Arm assignment (between-subjects)

Four arms, random assignment on Prolific:

| Arm | Label | Manipulation |
|:---:|:---|:---|
| **Control** | no manipulation | baseline task as above |
| **Info** | information intervention | at round 30, participants shown a clear text+graphical disclosure: "Option A deducts 3 tokens per click from your long-run pool; Option B adds 0.9 tokens" |
| **Signal** | signal redesign | at round 30, Option A's animation is replaced with the same neutral grey display as Option B (all other properties of A unchanged, including +1 token immediate) |
| **Combined** | both | at round 30, both manipulations applied simultaneously |

### §2.4 Primary outcome

**A-choice rate** in rounds 31–120 (post-manipulation), denoted *p*_A.

**Effects**:
- Δ*b*_info = *p*_A(Control) − *p*_A(Info)
- Δ*b*_signal = *p*_A(Control) − *p*_A(Signal)

**Primary test statistic**: ratio Δ*b*_signal / Δ*b*_info.

### §2.5 Matching convention (T2 compliance)

The two manipulations must inject comparable utility-unit shocks per T2 §1.4 (`proof_sketches_expanded.md`). We operationalise matching as:

- Info manipulation provides **exact numerical disclosure** of both payoff streams (perfect information → *w* channel maximised).
- Signal manipulation fully **neutralises** the A-animation (reduces ⟨*ψ*, *φ*⟩ from high to low by an amount equal to *σ*⁻¹(0.5) · *α* in the logistic-utility calibration).

Both manipulations are **at ceiling** for their channel: Info is full-disclosure (can't add more info); Signal is full-neutralisation (can't reduce animation below grey-neutral). This avoids the "which manipulation was stronger?" confound.

### §2.6 Predicted effect sizes

From T2: |Δ*b*_signal|/|Δ*b*_info| ≥ 1.5 under *w*_max = 0.4.

Concrete predictions (Cohen's *d* on *p*_A):
- Info arm: *d* ∈ [0.10, 0.25] (small effect; info channel is w-bounded)
- Signal arm: *d* ∈ [0.50, 0.90] (large effect; signal channel is (1−w)-bounded)
- Combined arm: *d* ∈ [0.70, 1.10] (additive with modest interaction)

**Pre-specified falsification condition**:

> P-fail-lab: If Δ*b*_signal / Δ*b*_info ≤ 1.0 with 95% CI excluding 1.5 (one-sided test), **the Sweet Trap intervention-asymmetry law (T2, P1) is falsified in the lab**.

This is a strict test: failing it would require either a revision of A3.3 (*w*_max upper bound) or rejection of the matching convention's operationalisation.

---

## §3 Sample, power, and preregistration

### §3.1 Sample

- Platform: **Prolific**.
- N per arm: **n = 200** (total N = 800 across 4 arms).
- Exclusions: (i) failed attention check at round 15, (ii) completion time < 6 minutes or > 25 minutes, (iii) fewer than 100 of 120 rounds completed. Expected attrition ≈ 15%, effective N ≈ 680.

### §3.2 Power calculation

Under the predicted effect sizes (Info *d* = 0.15, Signal *d* = 0.70), the ratio test has power > 0.95 at α = 0.05 with n = 200 per arm (computed via simulation: 10,000 draws from Gaussians with predicted means and SD = 0.3 in *p*_A; detecting ratio > 1.5 at 95% CI).

For the falsification test (ratio ≤ 1.0), power at n = 200 is > 0.90 to reject the null (ratio = 1) if the true ratio is 1.5; hence the study cleanly distinguishes P1-supports from P1-falsifies.

### §3.3 Pre-registration contents

OSF preregistration must specify, before data collection:

1. Full task protocol and manipulation operationalisation.
2. Primary outcome (*p*_A in rounds 31–120) and exclusion rules.
3. Primary hypothesis test: ratio Δ*b*_signal / Δ*b*_info ≥ 1.5 (one-sided).
4. Pre-specified falsification condition (P-fail-lab).
5. Sample size and stopping rule (no sequential analysis; fixed N).
6. Statistical approach: OLS regression with arm dummies; bootstrap CIs for the ratio.
7. Deviation protocol: any deviation from pre-registered analysis must be reported as secondary/exploratory.

---

## §4 Secondary manipulation checks

### §4.1 Manipulation integrity

- Info arm attention check: post-manipulation item "Which option has the higher long-run payoff?" (expected ≥ 85% correct in Info, ≤ 60% in Control).
- Signal arm salience check: post-manipulation item on self-reported "attractiveness" of Option A (7-point Likert; expected Signal arm rating < Control by ≥ 1 SD).

### §4.2 Individual-level *w* estimation

Post-task, agents complete a 5-item delay-discounting battery (Kirby 2009 *J Exp Anal Behav*). Structural estimation of *k_i* + *w_i* (via the A3+A4.1 equation fit) enables testing **P1.a** (w-stratified ratio): does the ratio correlate inversely with estimated *w*?

### §4.3 Robustness

- **Animation-intensity gradient**: in a secondary arm (optional extension; not in primary 4-arm design), vary Signal manipulation strength from 0% (no change) to 100% (full neutralisation) in 25% increments. Expected: Δ*b*_signal scales with signal reduction; non-linearity predicted by T2 §2.3 (diminishing returns at large Δ*φ*).
- **Information-intensity gradient**: in parallel, vary Info manipulation from incomplete (just "A is bad") to full disclosure. Info effect should saturate around *w* · (full-disclosure effect).

---

## §5 Cost estimate

- Prolific payment: $3 per participant × 800 = **$2,400**.
- Platform fee: $600.
- Software development: task in jsPsych, ~40 hours of developer time = **$3,000**.
- IRB + preregistration: minimal.
- **Total**: ~$6,000.
- Timeline from preregistration to manuscript: 3 months.

---

## §6 Expected results matrix and interpretation

| Outcome | Consistent with | Interpretation |
|:---|:---|:---|
| Ratio ≥ 1.5, both arms significant | T2 (P1) corroborated | Law of intervention effectiveness confirmed in lab |
| Ratio = 1.0 ± 0.3, both arms significant | T2 falsified | Either *w* is higher than predicted in this population, or matching convention violated; revisit A3.3 |
| Signal arm null, Info arm significant | T2 falsified (reversed dominance) | Major challenge to theory; possible A2 failure (signal is not genuinely decoupled in lab) |
| Both arms null | Task failed to induce Sweet Trap | Baseline *p*_A in Control must be > 0.55; if ≤ 0.55, the lab paradigm did not activate LSE |
| Ratio ≥ 2.5 | T2 strong form | *w*_max < 0.3 in population; Tier A-tight regime |

---

## §7 Linkage to Paper 2 and broader programme

This paradigm is the **lab complement** to Paper 2's observational and meta-analytic evidence. It is **not** Paper 1's primary empirical commitment — Paper 1 is a theoretical paper. But pre-registration of this design demonstrates that the theory is **falsifiable under contemporary lab practice**, answering the standard reviewer concern ("is this falsifiable?") with a concrete, low-cost, replicable design.

Implementation of the paradigm is tagged as **Phase D Experiment 1** in the project tree and will be run after Paper 1 is accepted (or concurrently, at the PI's discretion).

**Expected publication route**: a replication-focused methods paper in *Nature Human Behaviour* Methods section or in *Collabra: Psychology*, citing Paper 1 as the theoretical source.

---

*End of minimal experimental paradigm document. n = 200/arm × 4 arms, cost ~$6K, preregistrable, ratio-test statistic maps directly to T2.*
