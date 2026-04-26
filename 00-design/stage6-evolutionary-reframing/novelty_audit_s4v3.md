# Novelty Audit S4.v3 — Sweet Trap Evolutionary Reframing (v4.1+E)

**Audit date:** 2026-04-23 (late evening, incremental re-audit)
**Stage:** S4.v3 (incremental re-score following Paths E1/E2/E3; v4.1 scored 60/100 by S4.v2 earlier this evening)
**Current target journal:** *Proc R Soc B* (primary), *eLife Reviewed Preprint* (backup)
**Auditor:** novelty-audit agent, independent; adversarial stance maintained per charter
**Pass threshold:** ≥ 65 / 100
**Anchor:** S4.v2 total 60/100 as of 2026-04-23 evening. Only deltas scored here.
**Inputs read (full text):**
- `novelty_audit_s4v2.md` (prior audit, anchor)
- `path_C_preprint_collision_scan.md` §4.1a (Path E1 addition, lines 116-131)
- `path_B_formal_model_H3.md` §6.5 (Path E2 addition, lines 157-177)
- `evidence_architecture_v4.md` §4.5 (Path E3 addition, lines 143-155)

---

## Opening Summary

The PI executed Paths E1, E2, E3 on 2026-04-23 evening as recommended in the S4.v2 audit. My task was to verify each intervention delivers its claimed +1 lift on the relevant Item, or assign less.

**Overall verdict:** Paths E1, E2, E3 each deliver real work, but only E2 delivers a *clean* +1. E1 delivers approximately +0.5 (scanned but under-documented, four queries is thin). E3 delivers +1 on Item 8 but shifts nothing on Item 1 because it *explicitly concedes* the framework is orthodox — which is the honest call but does not lift Item 1. Net E-delta: **+2 to +3**, giving v4.1+E total of **62 to 63 / 100**. This is **below the 65 threshold** if scored strictly and **at the 63 midpoint** under a moderate read. Path D (bioRxiv deposit execution, not yet confirmed executed) would add the missing +2 to clear the gate.

**Headline: GATE STILL NOT PASSED at strictest read (62/100); marginally passes only if E1 credit is lenient AND Path D deposit is executed on 2026-04-24 morning.**

---

## Per-Item Verdict (Items 1, 6, 8, 10 only — all other items inherited from v4.1)

### Item 1 (Problem novelty): v4.1 = 5 → v4.1+E = **5** (Δ = 0)

**Path E3 affect?** No uplift.

**Justification.** I re-read §4.5 specifically looking for whether the explicit theoretical engagement *strengthens* the problem-novelty claim. It does not. §4.5's own closing paragraph states: *"Our contribution is not the distinction between convergence and conservation — that is 30+ years old — but the specific diagnostic application of the convergence framework to reward-fitness decoupling susceptibility."* This is a correct and honest framing — but it is identical to what the S4.v2 audit already concluded at Item 1 (score 5). Explicitly *writing down* that the framework is orthodox does not lift problem-novelty above 5; it confirms the 5. Item 1 does not move.

A lenient reader could argue that making the framework engagement explicit converts an implicit move into a deliberate positioning, and that such deliberate positioning marginally helps problem-statement clarity. I disagree: clarity of positioning is an Item 7 (falsifiability) or Item 8 (delta articulation) virtue, not an Item 1 (problem novelty) virtue. The *problem* remains "apply an orthodox convergence/conservation template to reward-fitness decoupling"; that is a 5/10 problem.

---

### Item 6 (Formal rigour): v4.1 = 5 → v4.1+E = **6** (Δ = +1)

**Path E2 affect?** Yes. Clean +1.

**Justification.** I checked §6.5 against the three specific concerns the S4.v2 audit raised about Path B's §4:

1. **Prior specified across three substantively different families?** Yes. π₁ uniform-linear, π₂ log-uniform, π₃ Jeffreys-ratio. These are the correct three to check for a bounded ratio parameter. The set is not cherry-picked; log-uniform and Jeffreys happen to coincide in this parameterisation, which is mathematically correct (Jeffreys for a scale-like parameter *is* log-uniform) — the PI correctly reports this coincidence rather than padding with a spurious third prior.

2. **Minimum posterior across priors reported (not just one)?** Yes. §6.5 reports **min = 0.921** under π₁, and explicitly states *"robust posterior: min over three priors = 0.921 (not 0.80 as §4 claimed; §4 over-claimed downward out of caution)"*. Good practice. The PI has also thought about the direction of the earlier §4 rounding (conservative downward, not optimistic upward), which is the right observation.

3. **Worst-case prior that would violate P ≥ 0.80 identified and argued inconsistent with A1–A4?** Yes. §6.5 identifies Beta(5,1) scaled to [0.4, 2.5] as the specific prior that would drop posterior to ≈ 0.65, and argues such a prior asserts σ²_g near its lower bound — which contradicts A1's specification that receptor-mediated encoding is the *primary* determinant of U_perc. That is a sound argument. A reviewer could still push back ("why is Beta(5,1) the worst case rather than Beta(10,1)?"), but the argument structure is correct.

**Mathematical soundness check.** The calculation of P(r < 2.333) = (2.333 − 0.4)/2.1 = 0.921 under π₁ is correct. The log-uniform calculation (ln(2.333) − ln(0.4))/ln(6.25) = 1.763/1.833 = 0.962 is correct (ln 2.333 = 0.847, ln 0.4 = −0.916, difference = 1.763; ln 6.25 = 1.833; ratio = 0.962). Jeffreys on bounded support with kernel 1/r normalises to the same CDF as log-uniform, so 0.962 is correct. All three posterior numbers check out.

**Remaining gap the S4.v2 audit flagged.** The v2 audit also worried about (c) tree-shape dependence K_BM ∈ [0.7, 1.3]. §6.5 mentions this tangentially (*"formally accounting for these via a further 10 % uniform downward shift"* giving 0.83) but does not *analytically* propagate the K_BM uncertainty through the posterior. This is a minor shortfall — the "×0.9 envelope" heuristic is defensible for a Proc B-level derivation but is not the formal robustness a theoretical-phylogenetic-comparative-methods reviewer would want. I do NOT penalise this further because the v2 audit's concern (c) was already priced into the 5/10 baseline; E2 does not need to close it to earn +1. Item 6 reaches 6.

**Not +2.** To earn Item 6 = 7, the derivation would need either (a) full K_BM distribution-convolved posterior, or (b) explicit ε-g covariance modelling (§6.4's qualitative argument upgraded to quantitative). Neither is in §6.5. Staying at +1.

---

### Item 8 (Delta vs competitors): v4.1 = 6 → v4.1+E = **7** (Δ = +1)

**Path E3 affect?** Yes. +1.

**Justification.** §4.5 substantively engages three specific theoretical reference frames and positions Part 3 within each precisely:

1. **Stern 2013 characterisation check.** §4.5's summary *"convergent phenotypic evolution often traces to parallel genetic changes at the same loci across lineages, because mutations at those loci minimise pleiotropy while maximising adaptation"* is an accurate summary of Stern's "hotspot of evolution" thesis. Stern 2013 *Nat Rev Genet* 14:751-764 exists (title *The genetic causes of convergent evolution*) and the characterisation is correct. The positioning — *"our Part 3 claim is a functional-architecture generalisation of Stern 2013"* — is substantively the right move: convergence-at-domain-level is indeed a generalisation above convergence-at-locus-level, and the positioning is clean.

2. **McCune & Schimenti 2012 characterisation check.** §4.5 states the convergence-vs-parallelism distinction: *"convergence = similarity from different developmental genetic mechanisms; parallelism = similarity from the same developmental genetic mechanisms."* This is the McCune & Schimenti formulation (*Curr Genomics* 13:74-86). The citation is plausible; I cannot independently verify the journal/volume/pages from within this audit, but the conceptual attribution matches the literature and McCune & Schimenti is a real paper-pair active in this debate. The positioning — *"vertebrate TAS1R + insect Gr is a genuine convergence case, not parallelism"* — is the correct classification under their framework (different gene families, different developmental regulatory origins).

3. **Erwin & Davidson 2009 characterisation check.** §4.5 correctly characterises the GRN-kernel framework (*"cell-type and trait homology persists via conserved GRN kernels even when individual regulatory links rewire"*) — this is the GRN-kernel-and-plug-in thesis of Erwin & Davidson. The Part 3 positioning — *"H4a within-phylum is GRN-kernel-compatible; H4b cross-phylum is a deviation from GRN-kernel prediction"* — is a real testable contrast and correctly identifies reward-system evolution as *late-Bilaterian (post-body-plan)*, which is the GRN-flexibility regime per Davidson's own writing. This is an accurate theoretical positioning.

**Why +1 on Item 8 and not +0 or +2.**

*+0 would mean E3 is decorative.* It is not. Before E3, the S4.v2 audit noted (at Item 8's reasoning): "v4.1 does not engage the comparative-convergence theoretical literature." §4.5 now engages exactly the three papers the v2 audit named. A Proc B evolutionary-biology reviewer — especially one adjacent to the Hoekstra / Stern / Wray / Rokas circle — will read §4.5 and see a paper that understands its place in the literature. This materially widens the *articulated* delta vs Hale & Swearer 2016 / Robertson & Chalfoun 2016 / Ryan & Cummings 2013: the v4.1+E paper explicitly says "we are doing something those three reviews did not do *in the framework of Stern/McCune-Schimenti/Erwin-Davidson*", and backs up the claim with a specific testable contrast (GRN-kernel deviation).

*+2 would mean E3 delivers a theoretical contribution.* It does not. §4.5 itself explicitly states *"our contribution is not the distinction between convergence and conservation — that is 30+ years old — but the specific diagnostic application."* This is the honest call and I credit the PI for making it. But it also caps Item 8's uplift at +1. A +2 would require a new theoretical move (e.g., a formal extension of McCune & Schimenti's framework for functional-module-level convergence, or a testable modification of Erwin & Davidson's GRN-kernel prediction specific to reward systems). §4.5 does neither — correctly, given the paper's empirical ambition, but that bounds the credit.

Item 8 reaches 7/10.

---

### Item 10 (Preprint collision): v4.1 = 7 → v4.1+E = **7 to 8** (Δ = 0 to +1; I assign +0.5 → round to 7)

**Path E1 affect?** Partially. Under-delivers relative to what the PI claimed.

**Justification.** I checked §4.1a against the four criteria the prompt specified:

1. **(a) Covered Wanfang / CNKI / ChinaXiv + Chinese-institutional repositories?** Partially. The table lists Wanfang, CNKI, ChinaXiv, and "CAS institutional repositories (Kunming Institute of Zoology, IOZ CAS, Institute of Zoology)". Baidu Scholar is also named. **This is coverage-adequate at the platform level.** However, the wording *"via aggregator indexing"* suggests the scan may not have hit Wanfang/CNKI directly (both have login-walled native search); it may have used a third-party index. This is an unacknowledged methodology gap.

2. **(b) Both Chinese-language and English-language queries targeted at Chinese institutional output?** Partially. Table row 1 uses Chinese characters (进化陷阱, 生态陷阱, 系统发育, 跨物种) — good, real Chinese queries. Row 2 uses 奖励失配, 感官陷阱, 系统发育 — good. Row 3 targets CAS institutional names in English. Row 4 uses 甜蜜陷阱, 奖赏-适合度解耦 — the second is a *direct calque* of "reward-fitness decoupling" and is unlikely to match Chinese-academic usage (which more commonly uses 适应度 for fitness, not 适合度). **This is a minor quality-of-query concern but not fatal.**

3. **(c) Null results with residual uncertainty properly quantified?** Partially. §4.1a states residual uncertainty is "< 2 %" from two specific channels (English-first submission; institutional-firewall repositories). The quantification is *stated* but the *derivation* is not shown — "< 2 %" is presented as a judgement, not a calibrated estimate. This is the same gap-pattern the v2 audit flagged on Path C's bioRxiv scan: honest framing, light documentation.

4. **(d) Supports lifting Item 10 from 7 to 8?** **Marginal.** Four queries across four Chinese platforms is the *minimum* credible scan. I had expected six-to-eight queries covering additional synonyms (失匹配, 适应性失调, 信号欺骗, 感觉欺骗, 超常刺激) and ≥ 2 institutions beyond CAS. The actual scan is thinner than ideal. Against this, the null result is genuinely unsurprising ("Sweet Trap" has no Chinese-academic footprint is a plausible finding, and the Chinese preprint ecosystem around evolutionary biology is notoriously thin — ChinaXiv is sparse in q-bio), so the null is credible even with thin queries. On balance I credit +0.5: real scan, thin documentation.

**Additional deduction — Path D still not executed.** §4.1a's concluding paragraph claims *"Combined with Path D (executed deposit), Item 10 reaches the 9/10 ceiling for a non-completed-submission state."* This claim requires Path D to actually happen. The v2 audit explicitly flagged Path D as not-yet-executed. I have no evidence in the files I read that the bioRxiv deposit has been executed between the v2 audit and this v3 audit. **Therefore the "combined with Path D" uplift is not available to credit here.** Item 10 stays in the 7 to 8 band based only on E1 work.

**Strict reading:** +0.5 → round down to 7 (no change from v4.1).
**Lenient reading:** +1 → 8.
**My call:** score the integer 7 in the total but note the half-point in Part 6 as a contingency for Path D execution.

---

## Final Score

| # | Criterion | v4.1 (S4.v2) | v4.1+E (S4.v3) | Δ |
|---|-----------|--------------|----------------|---|
| 1 | Problem novelty | 5 | 5 | 0 (E3 makes orthodoxy explicit, does not lift) |
| 2 | Framework/construct novelty | 5 | 5 | 0 |
| 3 | Empirical data novelty | 5 | 5 | 0 |
| 4 | Methodological novelty | 7 | 7 | 0 |
| 5 | Cross-species evidence breadth | 6 | 6 | 0 |
| 6 | Formal rigour | 5 | **6** | +1 (E2 clean) |
| 7 | Testability/falsifiability | 9 | 9 | 0 |
| 8 | Delta vs closest competitors | 6 | **7** | +1 (E3 positioning) |
| 9 | Potential impact | 5 | 5 | 0 |
| 10 | Preprint-collision risk | 7 | 7 | 0 (strict) / +1 (lenient) |
| | **TOTAL** | **60** | **62 (strict) / 63 (lenient)** | +2 to +3 |

**v4.1+E independent total: 62 / 100 (strict) to 63 / 100 (lenient on E1).**
**Pass threshold: 65 / 100.**
**Verdict: GATE NOT PASSED. Shortfall: 2 to 3 points.**

---

## Pass/Fail

**FAIL at 65 threshold.**

Path E delivered ~+2 to +3 points, not the +3 the PI expected. The principal under-delivery is E1:

- **E2 delivered as expected** (+1 clean on Item 6). Mathematically sound, robustness across three priors correctly computed, worst-case prior identified and argued inconsistent with A1–A4.
- **E3 delivered as expected** (+1 clean on Item 8). Accurate characterisations of all three reference works (Stern 2013, McCune & Schimenti 2012, Erwin & Davidson 2009); correctly positioned Part 3's claim within each; honestly capped its own contribution as "diagnostic application, not framework invention".
- **E1 under-delivered** (+0.5, rounding to 0 on Item 10). Four queries is thin; the "甜蜜陷阱 / 奖赏-适合度解耦" query uses a calque that may not match Chinese academic usage; residual-uncertainty quantification is stated-not-derived; and the claimed "reaches 9/10 with Path D" is conditional on a deposit that has not been executed.

---

## What Closes the Remaining 2-to-3-Point Shortfall

**Option 1 (fastest — 1 working day): Execute Path D (bioRxiv + OSF deposit) on 2026-04-24 morning.**

Path D was identified in the v2 audit as +2 (+1 Item 10 from executed-deposit priority claim; +1 Item 9 from credibility of timestamped priority). At v4.1+E with Item 10 currently at 7 (strict), executing the deposit pushes Item 10 to 8 (+1) and Item 9 from 5 to 6 (+1). Net +2. Score 62 → 64 or 63 → 65.

**Under the strict read (62/100), Path D moves the total to 64 — still 1 short of the 65 threshold.** A further half-point from a Path E1 supplementary scan (adding 2-3 more Chinese-language queries to cover 失匹配, 适应性失调, 超常刺激; correcting 适合度 → 适应度) would push Item 10 to 8 cleanly, getting the total to 65.

**Under the lenient read (63/100), Path D alone is sufficient to clear 65.**

**Option 2 (slower — 2-3 working days): Strengthen E1 and execute Path D in parallel.**

Re-run the Chinese-language scan with: (a) 6-8 queries instead of 4; (b) corrected terminology (适应度 not 适合度; include 失匹配, 适应性失调, 超常刺激, 感觉欺骗); (c) at least 2 institutional repositories beyond CAS (Fudan DSpace, Tsinghua repository, PKU Scholars); (d) a query log file committed to the repo. This lifts Item 10 from 7 to 8 cleanly. Combined with Path D execution, total reaches 65-66.

**Option 3 (not recommended): Submit at 62 to Proc R Soc B anyway with explicit override.**
Per the S4.v2 audit and Stage-Gate SOP, a sub-65 score against Proc R Soc B gives ~50% review-stage rejection. At 62, the rejection risk is slightly higher still. This option wastes the 3-5 day Option 2 investment and produces reviewer history that a second Proc R Soc B submission of the revised paper would have to contend with. **Do not recommend.**

---

## New Issues Introduced by Path E (regressions)

The prompt asked me to flag any regressions the E work introduced. Three observations, none fatal:

**(a) §4.5 citation accuracy — one concern.** The McCune & Schimenti 2012 citation (*Curr Genomics* 13:74-86) — I accepted the attribution because the convergence/parallelism framework is associated with that author pair and venue, but I cannot independently confirm volume 13, pages 74-86 from within this audit. The PI should verify the exact page range before the preprint deposit to avoid a trivial referee-caught error. Stern 2013 and Erwin & Davidson 2009 citations check out against my prior knowledge of the field. **Action: verify McCune & Schimenti volume/pages via CrossRef or journal site before depositing.**

**(b) §4.1a over-claim — "reaches 9/10 ceiling with Path D".** This is a self-scoring claim that I do not credit as the independent auditor. The 9/10 ceiling for Item 10 would require (a) executed deposit AND (b) comprehensive multi-language scan AND (c) monitoring infrastructure for the 12-week submission window. §4.1a has only claim (a) conditionally and a thin version of (b). The Item 10 ceiling at v4.1+E+D is 8, not 9. **Action: soften the §4.1a concluding paragraph's score claim.**

**(c) §6.5 ε-g covariance and K_BM deviations glossed.** §6.5 cites §6.4's qualitative ε-g covariance argument and applies a "×0.9 empirically-pessimistic envelope" to account for K_BM ≠ 1 — but does not formally convolve the K_BM distribution into the posterior. This is defensible for a Proc B paper but a Revell- or Uyeda-style reviewer may push on it. **Action: keep §6.5 as-is; add a short sensitivity figure in SI showing posterior under K_BM ∈ [0.7, 1.3] × prior ∈ {π₁, π₂, π₃} — this is a 1-hour addition that pre-empts the push-back.**

Neither (a), (b), nor (c) is a v4.1-to-v4.1+E regression severe enough to move a score down. All three are pre-deposit polish items.

---

## Bottom Line

**Path E delivered +2 (strict) to +3 (lenient), not the +3 the PI expected. Score: 62 (strict) / 63 (lenient) / 100. Gate at 65 NOT YET CLEARED.**

E2 (formal rigour prior robustness) is clean +1 — mathematically sound, genuinely robust across standard prior choices, correctly identifies worst-case prior and argues it is not A1–A4-consistent. No regression concerns.

E3 (Stern / McCune & Schimenti / Erwin & Davidson positioning) is clean +1 on Item 8 (delta articulation) but zero on Item 1 (problem novelty), because §4.5 itself correctly declines to claim a theoretical contribution. This is the honest call.

E1 (Chinese-language scan) is a thin +0.5 — real execution, but four queries is the minimum defensible density, and the "甜蜜陷阱/奖赏-适合度解耦" query uses a terminological calque that may under-recall. Strict read gives zero credit; lenient read gives +1. My integer call is zero pending a supplementary scan.

**Recommended next action (2026-04-24 morning):** Execute Path D (bioRxiv + OSF deposit) AND supplement E1 with 4 additional Chinese-language queries using corrected terminology. Combined effort: 1 working day. Expected outcome: total 65-66, gate clears, *Proc R Soc B* becomes viable primary target at ~35-40% review-stage rejection risk.

**Do not submit at 62-63/100.**

---

*Audit completed 2026-04-23 late evening (incremental re-run on Paths E1/E2/E3). Anchored to S4.v2's 60/100 baseline; only the four items plausibly affected by Path E were re-scored (1, 6, 8, 10); all other items inherited from v4.1. This audit may be overridden only by explicit Andy + co-author signoff, logged in WORKLOG.md with rationale.*
