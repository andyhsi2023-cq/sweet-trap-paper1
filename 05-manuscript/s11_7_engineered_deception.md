# §11.7 — Engineered Deception: extending the Engineered sub-class beyond algorithmic media

*(New section added in v2.1. Status: construct extension, not primary analysis. The two cases below are reported as *positive classifier predictions on held-out phenomena* that illustrate construct generalisation; they are not part of the 10-case discriminant-validity dev set and do not enter the κ calculation.)*

---

## §11.7.1 Why extend the Engineered sub-class?

v2 §11.3 introduced an Engineered / Mismatch distinction grounded in *mechanism architecture* — Engineered Sweet Traps target general-purpose reward circuitry with a signal that has no ancestral referent, whereas Mismatch Sweet Traps exploit a reward calibration that once tracked fitness. Within v2 the only worked Engineered case was **C12 short-video / algorithmic feed**: a variable-ratio intermittent-reinforcement schedule running on an Olds–Milner-type direct-reward bypass.

Two observations motivate extending the Engineered sub-class into a *family* with ≥ 2 members:

1. **A second distinct human phenomenon appears to share C12's Olds–Milner architecture but is engineered by a human rather than an algorithm.** If the same variable-ratio intermittent-reinforcement mechanism drives both algorithmic and human-engineered cases, that is additional evidence for mechanism-level universality across operators (machine vs human) within a single Engineered family.
2. **A second sub-family emerges on a different axis.** Certain large-scale fraud schemes satisfy F1 + F2 through *aggressive mimicry* — a perpetrator deploying an artificial signal that exploits an *ancestrally-calibrated* reward system (romance, wealth) in the victim. This shares F2 "aspirational endorsement" but shifts the engineering from "reinforcement schedule" to "deceptive signal fabrication."

We therefore promote the Engineered sub-class from single-case (C12) to a **family of two sub-sub-classes**:

| Sub-sub-class | Operator | Mechanism | Example |
|---|---|---|---|
| **Engineered Algorithmic** | Automated system | Variable-ratio Olds–Milner direct reward | C12 short-video / algorithmic feed |
| **Engineered Deception** | Human perpetrator | Aggressive mimicry of aspirational reward cue | Pig-butchering scam; PUA intermittent reinforcement |

Both share F1 + F2 and both qualify as Engineered under v2 §11.3 (no ancestral calibration for the *engineered* signal, by construction). The two sub-sub-classes differ in policy lever: Algorithmic requires *signal-format regulation* (recommender transparency, reinforcement-schedule disclosure); Deception requires *mimicry detection and interdiction* (financial-fraud monitoring, platform authentication).

---

## §11.7.2 Case 1 — Pig-butchering (杀猪盘): a financial-romantic aggressive-mimicry Sweet Trap

**Phenomenon.** Long-con financial-romantic fraud in which a perpetrator cultivates a manufactured romantic relationship online over weeks or months, then introduces a fraudulent cryptocurrency or foreign-exchange "investment opportunity" that progressively drains the victim's savings. The term "杀猪盘" ("pig-butchering") refers to the metaphor of fattening the victim (deepening trust and cumulative deposits) before the slaughter (final withdrawal and disappearance of the perpetrator).

**Scale.**
- **United States**: FBI Internet Crime Complaint Center (IC3) reported approximately USD 4.5 billion in confidence-/romance-fraud losses in 2023, with pig-butchering-style schemes accounting for the largest and fastest-growing category (FBI IC3 2023 Internet Crime Report).
- **China**: The Ministry of Public Security (公安部) reported that telecom and online fraud (电信网络诈骗) handled more than 437,000 criminal cases nationwide in 2023, with pig-butchering among the top loss-per-case categories; Global Times (2024-01) and Xinhua reporting cite multi-billion-RMB annual loss totals.
- **Global**: INTERPOL (2023) and UN Office on Drugs and Crime (2023) describe industrial-scale operations run from compounds in Southeast Asia, with labour obtained through human trafficking — a structural feature that multiplies the welfare cost.

**F1 — Reward-fitness decoupling.** F1 = 1.0. The engineered signal (perceived romantic partner + perceived high-return investment) activates two ancestrally-calibrated reward channels (pair-bonding; resource accumulation). Current cor(R_agent, F) is strongly negative — actual fitness outcome is savings destruction and often debt. Ancestral cor(R_agent, F) for the constituent signals (pair-bond formation under courtship; investment of effort in a trusted partner) was strictly positive. Δ_ST is large.

**F2 — Endorsement without coercion.** F2 = 1.0. The victim actively prefers the action (continued contact, incremental deposits) throughout the relationship up to the moment of realisation; there is no external compulsion. This is the critical F2 boundary for v2.1: *aspirational under deception is F2 = 1*, because the chooser's *internal* preference is the relevant criterion — the deception operates on the signal distribution seen by the chooser, not on the chooser's freedom to choose. This is distinct from:
- **C4 bride-price (彩礼)** — F2 fails because exposure is driven by kin / social-network compulsion, not individual endorsement under the perceived reward.
- **D3 996 overwork** — F2 fails because exposure is driven by employer lock-in, not endorsement.
- **Coerced trafficking victims within the pig-butchering operation** — F2 fails on the labour side (labourers), but succeeds on the victim side (investors). Pig-butchering is therefore a two-sided phenomenon with Sweet Trap architecture on the *victim* side only.

**F3 — Self-reinforcing equilibrium (severity modifier).** F3 = 1.0 at the individual level: each successful "deposit → apparent return" cycle strengthens the reward signal. At the population level, F3 is also present: perpetrator operations scale through platform evasion, and victim populations are replenished by new entrants as detection tools are developed.

**F4 — Absence of corrective feedback (severity modifier).** F4 = 0.5. Cost is realised in a single terminal event (not gradually), which in principle allows Bayesian updating — but only after the terminal event. During the pre-terminal phase, apparent positive feedback (simulated investment returns) *inverts* the sign of the corrective-feedback channel, making F4 effectively positive during the trap.

**Classifier score.** S = 2·F1 + 2·F2 + 1·F3 + 1·F4 = 2.0 + 2.0 + 1.0 + 0.5 = **5.5** > 4.0 → **Positive Sweet Trap** (Engineered Deception sub-sub-class).

**Animal homology — aggressive mimicry.** The mechanism is recognised in biology as *aggressive mimicry*: a predator deploys a signal calibrated to the prey's ancestrally-fit reward system (food, mate, nest site) to lure the prey into an attack. Canonical examples:
- **Anglerfish (琵琶鱼)** deploy an illicium with bioluminescent esca that mimics small prey, luring planktivores within strike range (Pietsch 2009, *Oceanographic Handbook of Deep-Sea Fishes*).
- **Photuris fireflies (致命拟态萤火虫)** mimic the flash codes of female Photinus fireflies to attract and consume Photinus males (Lloyd 1975, *Science* 187, 452–453).
- **Bolas spiders** (Mastophora) release chemical mimics of female moth pheromones to attract male moths within striking range (Eberhard 1977, *Science* 198, 1173–1175).

In all three cases the prey's reward architecture — evolved for a legitimate signal distribution (conspecific mate, conspecific prey) — is exploited by an engineered signal deployed by a different species. This is the animal homologue of pig-butchering's romantic-financial signal fabrication. The cross-species concordance strengthens the claim that Engineered Deception is not a human-specific category but a mechanism with a direct biological precedent.

---

## §11.7.3 Case 2 — PUA (Pick-up Artist) intermittent reinforcement: shared Olds–Milner architecture with C12 algorithmic feed

**Phenomenon.** A manipulation practice in which the perpetrator applies a scripted pattern of *alternating affirmation and rejection* (negging, orbiting, hot-and-cold) to induce an intense romantic fixation in the target, often followed by emotional or material extraction. The technique is explicitly described in PUA training materials as "push-pull" or "cat-string theory" — labels that map directly onto the behavioural-psychology literature on *variable-ratio intermittent reinforcement*.

**Scale.** Prevalence estimates are harder to quantify than pig-butchering because the phenomenon sits partly in legal grey area and partly in informal peer-driven practice; however:
- Multiple cohort studies of intimate-partner abuse report "intermittent reinforcement" as a core mechanism of coercive-control escalation (Stark 2007, *Coercive Control*; Hardy & Gilligan 2020, *J. Interpersonal Violence*).
- PUA-inspired manipulation is documented as a risk factor for trauma-bonding and PTSD in victims (Dutton & Painter 1993, *Violence & Victims* 8, 105–120; Carnes 2015, *Betrayal Bond*).
- Chinese-language analogues are documented under the terms "精神控制" and "情感操纵" in family-violence research and in public-health surveys of young adults.

**F1 — Reward-fitness decoupling.** F1 = 1.0. The engineered intermittent schedule produces *higher* subjective reward signal (attachment intensity, preoccupation) than a stable positive relationship would — while current cor(R_agent, F) is strongly negative (documented adverse outcomes: depression, self-esteem degradation, trauma-bonding, economic loss). Ancestrally, "intermittent partner availability" signals (legitimate uncertainty under mate-choice conditions) correlated positively with long-run reproductive outcome for those who persisted through honest courtship — the signal is exploited here by engineering artificial intermittency.

**F2 — Endorsement without coercion.** F2 = 0.5. The target actively prefers continued engagement under the perceived reward, but the boundary with coercion is less clean than in pig-butchering: repeated intermittent reinforcement can produce trauma-bonding with documented neuroendocrine correlates (Dutton & Painter 1993) that narrow the scope of "choice." We code F2 at the midpoint to reflect this boundary-case status: *aspirational endorsement is present in the initial and mid-phase; coercion-like dependency emerges in the late phase.* The classifier remains positive at F2 = 0.5.

**F3 — Self-reinforcing equilibrium (severity modifier).** F3 = 1.0. Each intermittent positive cycle deepens the conditioned dopaminergic response. Well-characterised in both behavioural-psychology (Skinner) and clinical literature on abusive relationships.

**F4 — Absence of corrective feedback (severity modifier).** F4 = 0.5. Cost is realised gradually (eroded self-esteem, social isolation) and often only after exit from the relationship. Information about what is happening is often available in principle (friends warn) but discounted by the reward architecture during the trap.

**Classifier score.** S = 2·F1 + 2·F2 + 1·F3 + 1·F4 = 2.0 + 1.0 + 1.0 + 0.5 = **4.5** > 4.0 → **Positive Sweet Trap** (Engineered Deception sub-sub-class; borderline).

*(Note: an earlier v2.1 scratch pad suggested S = 5.0; re-coding under the strict F2 = 0.5 rule yields S = 4.5. The case remains above the T > 4.0 threshold.)*

**Mechanism alignment with C12.** PUA intermittent reinforcement and C12 short-video algorithmic feed *share the same Olds–Milner variable-ratio schedule*. The *operator* differs (human perpetrator in PUA, recommender algorithm in C12), but the *mechanism* — variable-ratio intermittent reinforcement exploiting direct dopaminergic reward bypass — is identical. This is **strong within-family evidence that C12 is not a one-off**: the same architecture drives a second Engineered sub-sub-class case with an entirely different operator, domain, and cultural context. The cross-operator concordance (machine vs human both producing the same behavioural phenotype from the same variable-ratio schedule) is itself a falsifiable claim we extend to future replication.

---

## §11.7.4 Construct-extension power and F2 strict-boundary statement

**Classifier evaluation on held-out cases.** The 10-case discriminant-validity matrix (§M8) defined the classifier and its threshold T > 4.0. Pig-butchering and PUA are **not** part of the 10-case set, so they do not enter the dev-set κ = 1.00 calculation. We report them as *prospective classifier predictions* on held-out phenomena:

| Case | F1 | F2 | F3 | F4 | S | Threshold | Predicted |
|---|---:|---:|---:|---:|---:|:---:|---|
| Pig-butchering | 1.0 | 1.0 | 1.0 | 0.5 | 5.5 | > 4.0 | Positive |
| PUA | 1.0 | 0.5 | 1.0 | 0.5 | 4.5 | > 4.0 | Positive (borderline) |

Both classify positive on the held-out set. This is not out-of-sample *validation* in the strict sense — we have no independent ground-truth labels beyond our own coding — but it demonstrates that the classifier's positive region is not a vacuous superset of the dev set.

**F2 strict-boundary statement.** Both cases clarify the F2 boundary:

> **F2 = 1 requires the chooser's *internal preference to act* to be activated by the perceived reward signal in the absence of *external* compulsion on the choice itself. Deception operates on the signal distribution seen by the chooser, not on the chooser's freedom to respond to that distribution; hence aspirational endorsement under deception is F2 = 1.**
>
> **Conversely, F2 = 0 when the choice itself is compelled by external structure (employer lock-in in D3 996; kin/social-network obligation in C4 bride-price; trafficking-enforced labour in the perpetrator-side compounds of pig-butchering), regardless of any reward activation.**
>
> **F2 = 0.5 is reserved for cases where initial endorsement is genuine but late-phase dependency narrows choice — notably trauma-bonded PUA targets. This midpoint is the *boundary of the construct*, not a mechanism invention: the trap has converted aspirational endorsement into something that approaches coercion.**

This strict-boundary statement is the v2.1 companion to the F2 treatment in §11.4 (F3/F4 demotion) and preserves the necessary-condition status of F2 without adding new degrees of freedom to the classifier.

---

## §11.7.5 Methods integration

**Methods §2.4 Construct application** (v2.1 edit). Where v2 §2.4 described the Engineered sub-class via C12 alone, v2.1 distinguishes:

- **Engineered Algorithmic**: operator is an automated recommender or reinforcement-learning system; mechanism is variable-ratio Olds–Milner direct reward; policy lever is signal-format regulation. v2 example: C12.
- **Engineered Deception**: operator is a human perpetrator; mechanism is either aggressive mimicry of an ancestrally-calibrated reward cue (pig-butchering; aligns with anglerfish, bolas spider, Photuris firefly animal homologues) or engineered intermittent reinforcement (PUA; aligns with the C12 variable-ratio schedule); policy lever is mimicry detection and interdiction. v2.1 qualitative examples: pig-butchering, PUA.

Both sub-sub-classes remain within the v2 F1 + F2 necessary-and-sufficient classification rule. No new features are introduced.

---

*End of §11.7. Caveats: (i) the two v2.1 cases are qualitative extensions, not independently coded by a second rater; (ii) scale statistics are cited from secondary sources (FBI IC3 2023; China MPS 2023; INTERPOL 2023; UNODC 2023); (iii) animal-homology citations are non-exhaustive; a future registered replication could apply the classifier to ≥ 10 additional held-out cases to test generalisation formally.*
