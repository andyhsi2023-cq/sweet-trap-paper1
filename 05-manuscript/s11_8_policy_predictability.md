# §11.8 — Policy predictability as construct derivative [DIFF-C5]

**Status:** v2.4 new section (2026-04-18). Inserted after §11.7 Engineered Deception in the framework-refinements series. Replaces v2.3's DALY-anchored "welfare stakes" framing in the construct's interpretive layer.

**Relation to main text:** Main-text §8 reports the empirical instantiation (six focal domains; construct-derived ranking of signal-redesign vs information intervention effect sizes). Main-text Discussion implication (1) restates the law at the policy-framing level. This §11.8 documents the derivation — i.e., why the law follows from F1 + F2 *before* any empirical comparison — and pins down the scope condition and falsifiability rule.

---

## §11.8.1 Why F1 + F2 directly imply an intervention-asymmetry law

Recall (main text §1, §M1): the Sweet Trap classification is

- **F1 — Reward-fitness decoupling.** cor(R_agent, F)_current ≤ 0 ≪ cor(R_agent, F)_ancestral. The binding variable is not the agent's belief but the external signal distribution with which the reward system was calibrated.
- **F2 — Endorsement without coercion.** Pr(choose a | R_agent > 0, no coercion) > Pr(choose a | R_agent = 0, no coercion), under full information about downstream cost.

F2 is the pivotal condition for the policy implication. F2 states that the agent endorses the behaviour *even when* the fitness cost is known — i.e., endorsement is not contingent on the agent's belief about the cost. This is a definitional feature of the construct, not an empirical surprise: a phenomenon is not a Sweet Trap unless the endorsement survives the information being present.

A direct corollary follows. Consider the two canonical intervention classes:

- **Information interventions (belief channel):** nutrition labels, financial-literacy programmes, screen-time awareness campaigns, alcohol warning labels, fraud-victim awareness. These act on the agent's *cognitive representation* of the downstream cost — i.e., on the *belief* that the behaviour is harmful.
- **Signal-redesign interventions (F1 channel):** sugar taxes, auto-enrolment defaults, screen-time commitment devices, alcohol availability and price restrictions, LTV caps, platform cold-approach friction. These act on the *distributional properties* of the reward signal with which R_agent interacts — i.e., they modify F1 directly.

In Sweet Trap domains, F2 implies that the information channel is (by definition) not the binding constraint: the agent's endorsement does not require that the cost be unknown. Information interventions therefore operate on a variable whose change, under F2, cannot rescue the outcome. Signal-redesign interventions, by contrast, intervene on the channel (F1) that the construct definition identifies as binding.

**The derivation is construct-level, not empirical.** It does not depend on any particular intervention meta-analysis, or any assumption about the size of the effect. It predicts a *ranking*: within Sweet Trap domains, the expected magnitude of signal-redesign effects exceeds the expected magnitude of information effects on matched outcomes. The specific magnitudes are empirical questions, as is the specific factor by which one dominates the other in any given domain. What is *not* an empirical question — given the construct definition — is the direction of the ranking.

## §11.8.2 Scope condition: the law holds only in Sweet Trap domains

The law is domain-conditional. Two canonical failure conditions identify the boundary of the law's applicability:

### Failure of F1 (signal–fitness decoupling does not hold)

In domains where reward tracks fitness — i.e., cor(R_agent, F)_current > 0 — the F1 condition fails. Intervention design in such domains has nothing to gain from redesigning the reward signal (which is already well-calibrated); the behaviour-change problem is elsewhere. The construct makes no claim about intervention asymmetry in such domains, because they are not within its scope.

### Failure of F2 (endorsement depends on belief being wrong)

In domains where endorsement is contingent on the agent's *incorrect belief* about fitness — e.g., vaccine-hesitancy driven by misinformation about vaccine safety, or novel-risk domains where the individual's prior is simply wrong and correctable — F2 fails, because the endorsement is not robust to full information. In such domains, **information interventions target the binding variable**, and should therefore dominate signal-redesign interventions. The construct's policy-asymmetry law predicts, symmetrically, that in non-Sweet-Trap domains of this form, *information should dominate signal-redesign*.

Main text §8.3 operationalises this as a qualitative counter-example: the vaccine-hesitancy literature (Loomba et al. 2021 *Nat Hum Behav*; narrative-correction RCTs) shows that information interventions produce measurable effects in this domain — the pattern that the §8.2 six-domain set does *not* show. This cross-domain asymmetry is the strongest form of construct-scope validation we can offer without a paired-design RCT: the prediction holds in F1 + F2 domains and inverts in domains where F2 fails by belief-correction.

## §11.8.3 Falsifiability and post-publication test

The §11.8 law generates a precise falsification condition.

**Falsification condition A (domain-level).** In any domain classified as a Sweet Trap by F1 + F2, if a replicated RCT or meta-analytic update shows that an information intervention produces an effect size at least equal to a matched-outcome signal-redesign intervention, with 95% CIs non-overlapping the null, the construct's policy-asymmetry implication fails in that domain. Two consequences follow: (i) the construct-classification of that domain is called into question (does it satisfy F2 as strongly as assumed? is belief actually the binding variable?), and (ii) the scope condition of the §11.8 law must be narrowed.

**Falsification condition B (cross-domain).** If, across a pre-specified portfolio of ≥ 5 focal Sweet Trap domains, the median within-domain ratio of signal-redesign to information effect sizes is not significantly greater than 1 (one-sided Wilcoxon test, α = 0.05), the construct's policy-asymmetry implication fails as a general law. The six-domain portfolio reported in main-text Figure 8 and Table 4 constitutes the first-round test of this condition.

**Replication caveats acknowledged.** The nudge-replication literature (notably DellaVigna & Linos 2022, *Econometrica*) has shown that some signal-redesign / default-style interventions exhibit substantial effect-size shrinkage at scale. This is a known risk for the §11.8 law: if the six-domain interventions compiled in Fig. 8 are subject to similar shrinkage in future large-scale replications, the domain-level ranking may narrow. We treat this as a scope-refinement prediction: the §11.8 law should hold robustly in domains where F1 + F2 are both strong (high Δ_ST, high F2-aspirationality), and may weaken in borderline Sweet Trap domains (low Δ_ST, F2 = 0.5 boundary cases). The PUA boundary case in SI §11.7b is precisely such a borderline: we do not expect the §11.8 law to hold strongly in the late-phase trauma-bonded PUA target population, where F2 approaches coercion-adjacent.

## §11.8.4 What §11.8 does *not* claim

Two clarifications to prevent over-reading.

**The law is not a general statement about nudges.** Signal redesign, as used here, is a construct-level term referring to interventions on the F1 signal distribution. It is not synonymous with "nudge": a nudge in the Thaler-Sunstein sense may or may not operate on F1, and some nudges (e.g., reminder-SMS campaigns) operate on the information/belief channel. The §11.8 law is about the F1 channel specifically, regardless of whether a given intervention is conventionally labelled "nudge", "regulation", "tax", or "choice architecture". Main-text §8 reports the six-domain instantiation with domain-appropriate labels.

**The law is not a ranking of political feasibility.** Signal-redesign interventions may be politically more expensive than information interventions (sugar taxes face more opposition than sugar-awareness campaigns; LTV caps face lobbying opposition; platform-friction regulations face platform lobbying). The §11.8 law is a statement about *expected effect size on the target behavioural outcome*, not about political cost-benefit. Translating the law into policy requires the additional input of intervention cost, opposition, and enforcement feasibility.

## §11.8.5 Link to the construct's main contribution

The §11.8 law is the final interpretive piece of the v2.4 refactor. Where v1 was structured around an F1–F4 classification, v2 collapsed to F1 + F2 necessary-and-sufficient (§11.4), and v2.1–2.3 added the A + D cross-level concordance (§6) and the Engineered Deception sub-class (§11.7), **v2.4 closes the construct-to-policy derivation**: from F1 + F2 at construct level, to a falsifiable intervention-asymmetry law at policy level, testable against the existing intervention-effect meta-analytic literature (main-text §8) and falsifiable at both the domain level and the cross-domain level (§11.8.3). This is the sense in which Sweet Trap is not a typology or umbrella but a construct with a derivative law of policy effectiveness — the sense in which the paper's title ("*a cross-species reward–fitness decoupling equilibrium and a derived law of intervention effectiveness*") should be read.

---

*End of §11.8. Integrated into main text Discussion §1 ("policy interventions that reshape the signal distribution dominate information interventions — and this is not a post-hoc observation but a construct derivative"). Referenced by main-text §8.1, §8.3, §8.4. Relation to v2.3 §8 DALY anchor: orthogonal; the DALY aggregate is retained as Supplementary Appendix H descriptive-scale observation, the §11.8 law is the primary policy-stakes contribution.*
