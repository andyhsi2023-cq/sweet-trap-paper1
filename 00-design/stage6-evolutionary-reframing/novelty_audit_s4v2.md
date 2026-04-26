# Novelty Audit S4.v2 — Sweet Trap Evolutionary Reframing (v4.1)

**Audit date:** 2026-04-23 (evening, while PI asleep)
**Stage:** S4.v2 (re-audit following Paths A+B+C; v4.0 scored 52/100 on 2026-04-21)
**Current target journal:** *Proceedings of the Royal Society B* (primary); *eLife Reviewed Preprint* (backup); *Current Biology* Report (reformat-ready conditional on H3 strong result)
**Auditor:** novelty-audit agent, independent; does NOT endorse PI, research-director, literature-specialist, or Path-document self-scoring
**Pass threshold:** ≥ 65 / 100
**Inputs read (full text):** `research_question_and_hypotheses.md` (v1.1 two-tier H4), `evidence_architecture_v4.md` (v1.1, 2026-04-23), `path_A_convergence_reframing.md`, `path_B_formal_model_H3.md`, `path_C_preprint_collision_scan.md`, `bioRxiv_priority_preprint_draft.md`, `public_data_feasibility_v4.md` §Part 3, `competing_literature_map.md` §1.1–§1.4, `novelty_audit_s0_v4.md` (for continuity of checklist)

---

## Part 0: Method Notes

1. I did **not** read the Path documents' §4 / §8 "expected score delta" tables before forming my own score. I scored each item independently, then cross-checked against the PI's self-reported deltas. Disagreements are explicit in Part 5.
2. I adversarially stress-tested three specific factual claims before scoring:
   (a) Does v4.1's Part 3 framing actually align with Robertson 2003 / Chao 2020 / Feijó 2019 / the feasibility doc? — **Verified: yes** (feasibility doc §Part 3 line 172 states verbatim "The ABSENCE of strict orthology is EVIDENCE FOR convergent evolution of sweet-trap architecture" and line 176 gives the 40–50% vertebrate-invertebrate dopamine identity figure that Path A invokes).
   (b) Does Path B's BM-mixed-model derivation hold up mathematically? — **Partly.** See Item 6 analysis below.
   (c) Is Path C's scan methodology rigorous enough for +2 on Item 10? — **Only partly.** See Item 10.
3. Priors on my own scoring: I am instructed to hold hostile-reviewer stance. Where Path-document self-scoring and my independent score diverge, my score governs (per agent charter).

---

## Part 1: Per-Item Re-Scoring (v4.0 → v4.1)

Each item scored 0–10, with Δ vs v4.0 and evidence.

### 1. Problem novelty — v4.0: 4 → v4.1: **5** (Δ = +1; PI claimed +2)

**Evidence for +1:** The v4.1 thesis reformulation ("convergent evolution onto functionally-equivalent reward architectures across phyla, with deep within-phylum conservation") does change the *empirical* problem from "is Sweet Trap phylogenetically inherited?" (which is the v4.0 question that collapses into Hale & Swearer's open questions) to "is reward-fitness decoupling susceptibility riding on convergent or on conserved architecture?" (a distinct comparative-molecular-evolution question not asked in the antecedent literatures).

**Why not +2 as Path A claims:** The distinction "convergent vs conserved architecture" is itself a *template* question in comparative evolutionary biology (cf. Erwin & Davidson 2009; Stern 2013 *The Genetic Causes of Convergent Evolution*; McCune & Schimenti 2012). What v4.1 does is *apply* that template to reward-fitness decoupling — a competent and valuable move, but one that readers from comparative molecular evolution will recognise as a familiar framing, not a problem-statement breakthrough. The "novel problem" status is *moderated*, not *transformed*.

**Not-a-8 ceiling:** Problem novelty for a Proc B paper requires either (a) a phenomenon no one has asked about, or (b) a phenomenon everyone's asked about from a new angle that re-opens. v4.1 achieves (b) weakly — the angle is fresh for the ecological-trap crowd but is orthodox template for the phylogenomics crowd.

---

### 2. Framework / construct novelty — v4.0: 3 → v4.1: **5** (Δ = +2; PI claimed +2)

**Evidence for +2:**
- The **two-tier H4a/H4b split** is a genuine conceptual structuring advance. Splitting an "H4 molecular" claim into positive-control (conservation, where failure is informative about the pipeline) + novelty test (convergence, where failure is informative about the phenomenon) is better-designed pre-registration than v4.0's monolithic H4.
- The **InterPro-domain Jaccard architectural-similarity metric** as the decisive H4b test is a measurable construct that v4.0 did not operationalise. This is not invented by the PI (InterPro-Jaccard profiles are used in comparative-genomics workflows since at least Finn et al. 2014), but applying it as the *primary outcome* for a convergence-vs-conservation classification in reward signalling is uncommon.

**Why I agree with the +2 but not more:**
- **F2 (voluntary endorsement) still has no operationalisation for cnidarians, annelids, or molluscs.** The framework is still anthropomorphic at the edges. Path A did not fix this. A Proc B reviewer working on invertebrate behaviour will ask: "How do you code F2 for Nematostella?" — the answer is still "we don't." If H2's 50-case target leans heavily on invertebrates (which it must to exceed Hale & Swearer 2016's 43-case vertebrate baseline), this will surface.
- **A1–A4 axioms are now partially reclaimed by Path B but only in a limited sense** (they feed into a *bound-derivation*, not a theorem). Item 6 scores that contribution, not Item 2.

---

### 3. Empirical data novelty — v4.0: 5 → v4.1: **5** (Δ = 0; PI claimed 0)

No data added by Paths A/B/C. The sources remain: public cohorts (Part 1), published case pool (Part 2), Ensembl/OrthoDB/InterPro/STRING (Part 3). Agree with PI's self-score.

**One note:** The bioRxiv priority deposit draft (Path C artefact) is not "data novelty" — it's a claim-staking instrument. It does not move Item 3.

---

### 4. Methodological novelty — v4.0: 6 → v4.1: **7** (Δ = +1; PI claimed +2)

**Evidence for +1:**
- The **unified convergence-vs-conservation classifier** combining (i) OrthoFinder paraphyly test, (ii) InterPro-Jaccard architecture test, (iii) STRING/Reactome downstream-coupling presence/absence — applied specifically to reward-system receptor families as a package — is a genuine methodological assembly. Each component is individually routine; the assembly for this question is not yet in the reward-evolution literature I can identify.
- The Jaccard-with-matched-random-ortholog-baseline design is methodologically sound.

**Why not +2 as PI claims:**
- The components are entirely off-the-shelf. OrthoFinder (Emms & Kelly 2019), InterPro (Paysan-Lafosse et al. 2023), STRING (Szklarczyk 2023), Reactome (Gillespie 2022), PAML codeml (Yang 2007), Blomberg K (2003). Nothing is invented.
- "First application to reward receptors as a coordinated package" is a legitimate methodological move but is a tier below "new estimator" or "new measurement modality". The PI's claim that this "applies 2020s phylogenomic methods, not 2003-era methods" is overstated — the *newest* tool in the pipeline is OrthoFinder v2.5 (methodology ca. 2015, updated through 2019); InterPro-Jaccard is 2010s workflow; Blomberg K remains 2003.
- A Proc B methods-savvy reviewer will read this as "competent, standard phylogenomic assembly" not "methodological contribution." Item 4's ceiling for a paper of this type is about 7.

**What would have earned +2:** A custom statistical test for distinguishing convergence from conservation signatures in Δ_ST that wasn't in the literature (e.g., a posterior-probability classifier over models of molecular evolution). Path A did not deliver this; it re-deployed existing classifiers.

---

### 5. Cross-species evidence breadth — v4.0: 7 → v4.1: **6** (Δ = −1; PI claimed 0)

**Why I DECREASED this score:** v4.1's H4b reaches for ≥4 phyla with convergence evidence (Chordata, Arthropoda, Mollusca, Cnidaria, with Annelida/Nematoda as extensions). This requires *molecular* data for each of those phyla. Mollusca's Ap-DA1 (*Aplysia*) and Lym-DA1 (*Lymnaea*) dopamine receptors are documented; Cnidaria's Nv-DA-like (*Nematostella*) dopamine signalling is documented (Ryan et al. 2013 — the feasibility doc lists this). **But the InterPro-Jaccard and downstream-coupling tests require genome-wide data for these clades with matched random-ortholog baselines. For Cnidaria and Mollusca, that baseline construction is feasible but expensive in curation time, and mistakes in baseline construction dominate the Jaccard p-value.** The combined demand — 50+ behavioural cases spanning 6+ phyla (H2) + molecular data across 4+ phyla with within-phylum baselines (H4a) + cross-phylum convergence architecture with matched baselines (H4b) — has a *narrower* feasibility envelope than the 20-case single-layer v3.x plan.

v4.0 scored 7 partly because "7 taxonomic classes" was aspirational and the v4.0 feasibility estimate was "30+ cases." v4.1 adds a molecular-breadth ambition to that case-breadth ambition. **The realised product (case breadth × molecular breadth) is more likely to be short than v4.0 alone.**

**PI's Path-document self-score kept Item 5 at 7.** I disagree with the PI on this. The two-tier H4 *expands* the breadth ambition without expanding the breadth feasibility; that is a net negative signal for the probability of achieving the full breadth claim.

**If realised at 50 behavioural cases × 4+ phyla molecular:** score is 7.
**If realised at 30–40 cases × 3 phyla molecular (the realistic case):** score is 5.
**My 6 reflects the expected mid-point.**

---

### 6. Formal rigour — v4.0: 3 → v4.1: **5** (Δ = +2; PI claimed +3)

This is the item where Path B lives. I read Path B carefully.

**Evidence for +2 (genuine progress):**
- The decomposition Δ_ST,i = γ·g_i + ε_i is well-motivated and connects to A1 (genotype-driven component) and A2 (environment-driven component) cleanly.
- The BM-mixed-model variance decomposition Var(Δ_ST) = γ²σ²_g Σ + σ²_ε I is standard phylogenetic-comparative methodology (Revell et al. 2008 does contain the relevant formulas for expected K under attenuation).
- Path B's §5 per-axiom role table is the single most useful deliverable from Path B. It does make A1, A2, A3(animal-limit), and A4 each individually load-bearing for the K > 0.30 prediction. Removing any one collapses the derivation. **This genuinely reclaims A1–A4 from decorative status.**

**Why not +3 as PI claims — three specific mathematical / epistemic concerns:**

**(a) The bounds σ²_ε/(γ²σ²_g) ∈ [0.4, 2.5] are interpretive, not deductive.**
Path B §4 justifies the upper bound with "if it were arbitrarily large, Sweet Trap would not be a *biological* phenomenon — it would be a purely anthropogenic-exposure phenomenon. A2 and A1 jointly constrain the ratio." Similarly the lower bound: "above this... contradicts A2." These are **definitional constraints dressed up as derived constraints.** A1 does not quantitatively tell you that σ²_ε/(γ²σ²_g) ≤ 2.5; it tells you g > 0. A2 does not tell you σ²_ε/(γ²σ²_g) ≥ 0.4; it tells you ε > 0 for sufficiently novel environments. The numeric cutoffs (28 % / 71 % variance) are free parameters chosen to bracket the literature-plausible range. This is honest literature-calibrated prior setting, but it is not deductive. A rigorous theoretical reviewer (the Kokko-style reviewer Path B is trying to deflect) will see this immediately.

**(b) The "80 % posterior probability of K > 0.30" claim requires an undisclosed prior.**
Path B §4 states "The theoretical prediction is therefore K ≥ 0.30 with >80 % probability across the A1–A4-consistent prior parameter space." But "across the A1–A4-consistent parameter space" requires a prior over σ²_ε/(γ²σ²_g). Path B implicitly uses a uniform prior on [0.4, 2.5]; if the prior is uniform in log-space (which is more standard for ratio parameters), the posterior shifts. The "80 %" number is not robust to reasonable prior specifications. This is a statable concern, not a fatal flaw — reviewers may let it go — but it is not a clean derivation.

**(c) The tree-shape dependence K_BM(tree) ∈ [0.7, 1.3] is swept under the rug.**
Path B §3 notes that K_BM = 1 for pure BM on a balanced tree and 0.7–1.3 on empirical trees. The stated K ∈ [0.29, 0.71] range multiplies by the midpoint K_BM ≈ 1, but if the relevant phylogeny is pectinate (long-branch, uneven taxon sampling — which happens in cross-phyla animal trees because Chordata is densely sampled and Cnidaria sparsely), the K distribution could shift ±0.1. This is a fixable caveat but is not addressed.

**Net: Path B moves A1–A4 from decorative to *partially* load-bearing, with acknowledged gaps in the bound derivation.** This earns +2 on formal rigour (5/10), not +3 (6/10). A Proc B referee who works in theoretical phylogenetic comparative methods will accept the derivation as an "interpretive bound" paper, not a "deductive prediction" paper. That is still an improvement over v4.0.

---

### 7. Testability / falsifiability — v4.0: 8 → v4.1: **9** (Δ = +1; PI claimed 0)

**Why I INCREASED despite PI keeping this flat:**

The two-tier H4 split, combined with the expanded 6-column (H1/H2/H3/H4a/H4b/H5) dependency table with six outcome rows, is *better* falsifiability design than v4.0 — not the same. Specifically:

- The dependency table now pre-specifies the headline under convergence-only, within-phylum-only, behavioural-only, and full-claim outcomes. This is stronger pre-registration than v4.0's 5-row table which had weaker graceful-degradation for H4 failure.
- The H4b falsification splits into case (i) deep-conservation-instead-of-convergence (reframes narrative) vs case (ii) no-functional-unity (drops cross-phylum claim). Separating two distinct failure modes of the same hypothesis is exemplary pre-registration discipline.
- Path B adds *theoretically-predicted* magnitudes (K ∈ [0.29, 0.71] with point prediction 0.5) replacing v4.0's descriptive guess (0.3–0.8). Theoretically-predicted magnitudes are harder to post-hoc massage than descriptive guesses.

**What I am not awarding a 10 for:** H2's "any two of three null" criterion for H1 remains loose (common confounders could null all three streams simultaneously). H5 power analysis for PGLS at N ≥ 30 mammalian/avian is still not shown. These are holdovers from v4.0.

---

### 8. Delta vs closest competitors — v4.0: 5 → v4.1: **6** (Δ = +1; PI claimed +2)

The PI claims the convergence framing creates a "real delta" vs Hale & Swearer 2016, Robertson & Chalfoun 2016, Ryan & Cummings 2013. I tested this competitor-by-competitor:

- **Hale & Swearer 2016** *Biol Rev*: Their paper is a PRISMA systematic review of ~43 vertebrate ecological-trap cases with attractiveness-fitness quantification. v4.1's delta: (a) +7 cases (v4.1 promises 50+), (b) +phylogenetic signal test, (c) +molecular layer with convergence-vs-conservation classifier, (d) +trans-ancestry human extension. The molecular convergence classifier is a genuine new delta vs Hale & Swearer 2016 (they have no molecular layer). **Real delta: moderate-to-large** (was moderate in v4.0).
- **Robertson & Chalfoun 2016** *Curr Opin Behav Sci*: Conceptual review. v4.1's delta is larger because now there is a quantitative molecular classifier, not just a quantitative case meta-analysis. **Delta widens.**
- **Ryan & Cummings 2013** *Annu Rev Ecol Evol Syst*: Sensory-trap mate-choice cross-species. v4.1's delta vs Ryan & Cummings: the convergence-architecture claim specifically about *reward-system* molecular signalling (as opposed to mate-choice sensory tuning) is a new move. **Delta widens modestly.**
- **Santos et al. 2021** *Science*: Single-domain (plastic) 138-species meta. v4.1 still multi-domain + phylogenetic + molecular. **Delta unchanged.**
- **Feijó et al. 2019** *Nature*: Vertebrate TAS1R sweet-receptor evolution + hummingbird umami-to-sweet re-evolution. v4.1 uses Feijó 2019 as a *within-vertebrate* reference point (H4a Chordata) and as a reference for TAS1R being paraphyletic to insect Grs (H4b Chordata × Arthropoda test). Feijó 2019 does not make a cross-phyla convergence-vs-conservation claim for reward signalling generally. **Delta preserved.**

**The consolidated delta (v4.1):** Sweet Trap contributes **operational quantification + phylogenetic-signal test + convergence-vs-conservation classifier + human extension**, integrated across a 50+ case base. The fourth item is new in v4.1 relative to v4.0. It does widen the delta.

**Why +1, not +2 (disagreeing with the PI):**

- A Proc B editor reading v4.1 alongside Hale & Swearer 2016 + Chao 2020 (Gr non-orthology with TAS1Rs) + Yamamoto & Vernier 2011 (vertebrate dopamine family conservation) will see v4.1 as *integrating* pieces that already exist rather than *discovering* something new. The integration is valuable, the discovery framing is not fully warranted.
- The specific empirical claim — "reward-fitness decoupling susceptibility rides on convergent architecture" — is not testable at the Jaccard level alone. To actually demonstrate convergent-architecture-causes-susceptibility you would need either (a) receptor-knockout experiments, or (b) a within-species causal link between g_i and Δ_ST_i. v4.1 does neither. The convergent-architecture claim is therefore *descriptive*, not *causal*. The PI's Path A argument that "convergence is a stronger claim than conservation" is correct *philosophically* but the empirical package cannot discriminate between convergence and *convergent-preservation-plus-independent-origin* versus *drift-attractor* mechanistic accounts. A rigorous molecular-evolution reviewer will note this.

**Score 6: real delta, not large delta. Clear advance over Hale & Swearer, but within the envelope of "Hale & Swearer 2016 Part 2 + a molecular chapter."**

---

### 9. Potential impact — v4.0: 5 → v4.1: **5** (Δ = 0; PI claimed 0, but I re-examine)

I re-examined Item 9 specifically at Andy's request (whether the convergence-on-reward-architecture headline changes citation trajectory).

**Case for +1:** A convergence-on-reward-architecture headline is more portable than a phylogenetic-signal-on-susceptibility headline. Convergence frameworks cross-pollinate between evolutionary biology, comparative genomics, and neuroscience; phylogenetic-signal-on-behaviour papers tend to stay within comparative ecology. If v4.1 lands at *Proc R Soc B* with the convergence-headline dominant, the Part 3 figure becomes a teaching-slide candidate in molecular-evolution and behavioural-ecology courses. That is citation fuel.

**Case for 0:** The convergence headline increases portability but also increases the reviewer pool that will scrutinise it. Molecular-evolutionists reviewing a convergence claim will demand things Path A cannot deliver (explicit selection tests beyond dN/dS, functional interchangeability assays across phyla, mechanistic linkage of receptor architecture to Δ_ST magnitude). Higher reviewer-demand increases revision burden and reduces the probability that the headline survives peer review intact. Conditional on publication, impact is higher; unconditional, expected impact is similar.

**Net: 5.** The pros and cons roughly cancel. At *Proc R Soc B* with v4.1 executed, plausible 5-year citation range 60–180 (median ~110), essentially the same expected value as v4.0 with different shape.

Path C's bioRxiv priority deposit does *not* directly raise Item 9 — preprint deposit primarily affects Item 10 (priority) and does not measurably shift citation trajectory of the eventual peer-reviewed paper in most empirical studies of preprint effects.

**I disagree with Path A §4's assertion that this stays at 5 "conservative"** — I agree with the 5, but not with the framing that Path B/C will lift it to 6. Neither Path B's bound derivation nor Path C's scan directly adds citation potential.

---

### 10. Risk of "已被做过" / preprint collision — v4.0: 6 → v4.1: **7** (Δ = +1; PI claimed +2)

**Evidence for +1:**
- Path C's 12-query scan across bioRxiv, EcoEvoRxiv, PsyArXiv, Authorea, OSF, arXiv q-bio, Preprints.org, and ResearchGate is methodologically reasonable. It finds no direct competitor at the three-part-integrated-scope.
- The lab-monitoring table (Robertson, Hale/Swearer/Sih, Nesse, Li/van Vugt, Ryan/Cummings) is well-chosen and correctly identifies LOW trajectory for each.
- The residual-uncertainty section is honest about four specific limitations (Chinese-language, indexing lag, embargoed manuscripts, conference abstracts).

**Why I REDUCE from the PI's claimed +2 to my +1:**

**(a) The Chinese-language blindspot is acknowledged but not closed.** Path C §4 proposes a "one-hour Chinese-language search on Wanfang + CNKI during Week 1" but the scan has not been executed. Given that Andy has Chinese-language access *right now* and the scan was written *before* completing that action, the +2 claim depends on an unscanned corpus. A rigorous Item 10 upgrade requires the corpus actually be scanned, not merely be scheduled. Crediting +2 at this point prematurely rewards planned-but-incomplete work.

**(b) The bioRxiv scan used WebSearch with keyword queries, not platform-native API queries.** WebSearch results depend on what Google Scholar / general search engines index, which is noisy and incomplete for fresh preprints. A more rigorous scan would hit the bioRxiv API (`https://api.biorxiv.org/pubs/biorxiv/[date_range]/[category]`) for each relevant collection with date filters. The keyword-based approach is a reasonable first pass but is less confident than an API-native scan.

**(c) The scan found bioRxiv 2025.04.18.649542 and 2025.10.21.683401 — I cannot independently verify these DOIs exist as described.** The scan notes them as "adjacent work" but the doc does not include the scan raw outputs. Path C §4 says "raw search results retained in memory context" but there is no attached log file. I cannot cross-check the PI's scan from this side.

**(d) The bioRxiv priority deposit itself has NOT been executed.** The `bioRxiv_priority_preprint_draft.md` is a draft ready for deposit, not a deposited preprint. Until the preprint has a DOI and is publicly indexed, there is no priority claim. Path C's argument for +2 includes Item 9 credit from "priority-claim credibility" — but no priority has actually been claimed yet. I do not award score for promised-but-not-executed deposit.

**My +1 credits:** a rigorous query breadth, an honest residual-risk section, and a deposit-ready draft. **My +1 does not credit:** unscanned Chinese corpus, API-incomplete scan method, un-executed deposit.

If Andy (a) executes the bioRxiv + OSF deposit and (b) runs the Wanfang/CNKI scan on 2026-04-24 morning, I would move Item 10 to 8. At scan-but-no-deposit, Item 10 is 7.

---

## Part 2: Summary Scoring

| # | Criterion | v4.0 | v4.1 | Δ | PI-claimed Δ | Agreement? |
|---|-----------|------|------|---|--------------|------------|
| 1 | Problem novelty | 4 | 5 | +1 | +2 | disagree (-1) |
| 2 | Framework/construct novelty | 3 | 5 | +2 | +2 | agree |
| 3 | Empirical data novelty | 5 | 5 | 0 | 0 | agree |
| 4 | Methodological novelty | 6 | 7 | +1 | +2 | disagree (-1) |
| 5 | Cross-species evidence breadth | 7 | 6 | −1 | 0 | disagree (-1) |
| 6 | Formal rigour | 3 | 5 | +2 | +3 | disagree (-1) |
| 7 | Testability/falsifiability | 8 | 9 | +1 | 0 | disagree (+1) |
| 8 | Delta vs closest competitors | 5 | 6 | +1 | +2 | disagree (-1) |
| 9 | Potential impact | 5 | 5 | 0 | 0 | agree |
| 10 | Preprint-collision risk | 6 | 7 | +1 | +2 | disagree (-1) |
| | **TOTAL** | **52** | **60** | **+8** | **+13** | PI over-claimed by 5 |

**v4.1 independent total: 60 / 100.**
**Pass threshold: 65 / 100.**
**Verdict: GATE NOT PASSED. Shortfall: 5 points.**

The PI's own Path-document self-scoring projected 52 → 69 (+17). My independent assessment is 52 → 60 (+8). The PI over-claimed by ~9 points across the checklist — primarily by taking "full credit" on Items 1, 4, 8, 10 where I gave "half credit", and by not noticing the Item 5 regression.

---

## Part 3: Top 3 Highlights vs Top 3 Risks (v4.1 revised)

### Top 3 Genuine Highlights

1. **The two-tier H4a/H4b restructuring is a real design improvement.** Splitting molecular conservation (positive control) from cross-phylum architectural convergence (novelty test) makes the pre-registration more disciplined and the failure modes more informative. Combined with the expanded 6-row dependency table, v4.1's falsifiability architecture is near-exemplary for pre-registered comparative biology.

2. **Path B's per-axiom load-bearing analysis is valuable even with its derivational weaknesses.** §5 of path_B_formal_model_H3.md genuinely reclaims A1–A4 from decorative status by showing that removing any one collapses the K > 0.30 prediction. The formal-weight ceiling is capped at "interpretive bound" not "theorem", but the axioms are no longer orphaned. That is the single most important gap-closure Path B achieved.

3. **The convergence-plus-conservation framing aligns v4.1 with the actual molecular data.** Path A's reframing is factually correct: the feasibility doc §Part 3 (lines 172, 176) already stated that insect Grs are non-orthologous to vertebrate TAS1Rs and that vertebrate-invertebrate dopamine identity sits at 40–50%. v4.0 committed to a deep-conservation prediction that would have been contradicted by the pipeline's own data at Week 6. v4.1 prevents that structural self-refutation. This is a non-trivial save.

### Top 3 Substantive Risks (v4.1)

1. **Cross-species × cross-phylum feasibility product is narrower than v4.0.** v4.1 simultaneously demands 50+ behavioural cases across 6+ phyla (H2) AND molecular coverage with matched baselines across 4+ phyla (H4a + H4b). Each ambition is individually stretched relative to current assets (20 cases, within-Chordata + within-Arthropoda molecular pilot data). Joint feasibility is worse than either alone. **Week 4 GATE 1 feasibility check is now double-jeopardy**: a miss on either layer degrades the headline.

2. **Path B's σ²_ε/(γ²σ²_g) ∈ [0.4, 2.5] bounds are presented as derived but are actually literature-calibrated priors.** A rigorous theoretical-phylogenetic-comparative-methods reviewer (e.g., a Revell- or Uyeda-style reviewer) will note this within one reading. The formal-rigour credit assigned (5/10) assumes the reviewer accepts "interpretive bound" framing; if the reviewer demands genuine deduction, the score could drop. Path B's §7 "what this derivation does NOT claim" section addresses this correctly by framing the result as a formal prediction with stated assumptions — but the Abstract and §4 of Path B still present the bounds in a more confident tone than §7 warrants. If the preprint draft makes the same confident claim, a competent reviewer will pick at it.

3. **Path C's bioRxiv deposit has not been executed.** The collision-risk score of 7 reflects a scan+draft combination, not a deposit. Until the preprint is actually deposited with a DOI, there is no priority claim. If a competing preprint appears between 2026-04-23 and whenever the deposit happens, the priority argument evaporates. **Time-to-deposit is now the critical path for Item 10.** Andy should execute the bioRxiv + OSF deposit on 2026-04-24 (first working day), not at Week 0 of the 12-week pipeline as previously planned.

---

## Part 4: Pass/Fail Verdict and Recommended Journal Targeting

### Verdict: GATE NOT PASSED at 60/100. Threshold is 65.

The Paths A+B+C effort moved the score from 52 → 60. That is genuine progress (+8 points) but is 5 points short of the 65 threshold. Per the Stage-Gate SOP and feedback_pipeline_enforcement.md, S4.v2 gate fail means the project does NOT proceed to S5 execution at the current journal target.

### Three Feasible Paths to Close the 5-Point Gap

**Path D (+2 points, 1 working day): Execute the bioRxiv + OSF deposit NOW.**
Moves Item 10 from 7 to 8 (deposit executed = priority claimed) and adds ~+1 on Item 9 (credibility from timestamped priority). **Execution: Andy deposits on 2026-04-24 morning using the `bioRxiv_priority_preprint_draft.md` already ready for polish + Playwright upload.** Net: +2 points. Score → 62.

**Path E (+3 points, 2–4 working days): Actually scan the Chinese-language corpus AND strengthen Path B's derivation.**
Two sub-actions:
- **E1 (+1 Item 10):** Run the Wanfang + CNKI scan for 进化陷阱 / 生态陷阱 / 奖励失配 / 感官陷阱 phylogenetic comparative queries. If the scan returns null, Item 10 lifts to 8 (full credit).
- **E2 (+1 Item 6 → 6/10):** Add to Path B an explicit **prior specification** over σ²_ε/(γ²σ²_g) (uniform on [0.4, 2.5]; uniform on log-space; or Jeffreys) and recompute the posterior probability of K > 0.30 under each prior, showing robustness across ≥2 of 3. This promotes the "80 % posterior" claim from assertion to demonstrated robustness. A competent theoretical reviewer will accept this.
- **E3 (+1 Item 8):** Add a short §2.6 paragraph to `evidence_architecture_v4.md` explicitly distinguishing v4.1's convergence claim from Stern 2013 / McCune & Schimenti 2012 / Erwin & Davidson 2009 template convergence frameworks. The current doc does not engage the comparative-convergence theoretical literature, which makes the "new problem" claim look naïver than it is. Engaging this literature *explicitly* closes the Item 1/Item 8 gap I flagged.

Net Path E: +3 points. Score (with D): 65. **Passes threshold.**

**Path F (+4 points, 6–8 working days, higher-leverage but slower): Operationalise F2 for invertebrates.**
If F2 (voluntary endorsement) can be operationally defined for *Nematostella* and annelids via a behavioural-approach assay (e.g., "taxon spontaneously approaches the stimulus source in chemotaxis arena" as binary F2-coding criterion), the framework-novelty floor lifts from 5 to 7 (+2 Item 2). The cross-species-breadth score returns from 6 to 7 (+1 Item 5) because the framework now travels to phyla where v4.0 had no operational anchor. And the delta-vs-competitors improves by +1 Item 8 because no prior ecological-trap work does F2-coding at invertebrate-level.

**Path F is higher-leverage than E but slower.** Andy's 12-week pipeline can absorb +1 week at the design end before starting S5 execution without schedule compromise, but +2 weeks starts to squeeze Weeks 10–12 manuscript writing. Recommended: Path D + E in Weeks 0–1, Path F if schedule tolerates.

### Recommended Journal Targeting at the CURRENT 60/100 Score

**If the project submits without further Path D/E/F intervention:**
- *Proc R Soc B* (target): ~45–55% review-stage rejection probability. Not desk-reject territory (60/100 passes Proc B's desk filter comfortably) but send-to-review-then-reject is real.
- *eLife Reviewed Preprint* (backup): almost certainly publishes at "Valuable / Solid evidence" verdict or better. This is the *safer* target at 60/100.
- *Current Biology* Report: only viable if H3 lands at K > 0.5 with short-form punchline. 60/100 average does not reformat to Current Biology Report unless one component lands strongly.

**Honest recommendation at 60/100: eLife Reviewed Preprint primary, Proc R Soc B secondary.** This inverts the current targeting.

**After Path D+E is executed (projected 65/100):**
- *Proc R Soc B* becomes viable as primary (review-stage rejection drops to ~35–40%).
- *eLife Reviewed Preprint* remains reasonable backup.

**After Path D+E+F (projected 68–70/100):**
- *Proc R Soc B* primary with moderate confidence. *eLife* as backup. NEE remains out of scope.

### Journal Targets to AVOID at any score ≤ 70

- *Nature Ecology & Evolution* — was correctly ruled out in v4.0 audit. v4.1 does not change this.
- *Nature* main, *Science*, *PNAS* direct — the paper is not a flagship-tier contribution. Cover letter to any of these wastes 1–2 months of review time.
- *Cell Reports* — wrong journal type for comparative biology; format-fit issues.

---

## Part 5: Explicit Disagreements with PI Path Documents

The parent task required me to state explicitly where I disagree with the PI's Path self-scoring. Six specific disagreements:

### 5.1 Path A §4 over-credits Item 1 (Problem novelty)

PI claims +2 on Item 1 ("convergence-vs-conservation distinction sharpens the problem statement from 'integrate known bits' to 'test whether reward-decoupling susceptibility rides on convergent vs shared architecture'"). I give +1. The convergent-vs-conserved template is an orthodox move in comparative molecular evolution; v4.1 *applies* it competently but does not invent the problem type.

### 5.2 Path A §4 over-credits Item 4 (Methodological novelty)

PI claims +2 on Item 4 ("applies 2020s phylogenomic methods, not 2003-era methods"). I give +1. The methods (OrthoFinder, InterPro, STRING, Reactome) are standard and have been available for years. The assembly into a convergence-vs-conservation classifier for reward receptors is the novel move, which earns +1; the "2020s methods" framing is inflated.

### 5.3 Path A §4 over-credits Item 8 (Delta vs competitors)

PI claims +2. I give +1. The convergence headline widens the delta vs Hale & Swearer 2016 and Robertson & Chalfoun 2016, but the underlying empirical package is still "operational quantification + phylogenetic-signal test + molecular classifier + human extension" — a valuable integration, not a delta discontinuity. A Proc B editor reading alongside Chao 2020 + Yamamoto & Vernier 2011 + Feijó 2019 will see v4.1 as "assembling known pieces into a coherent cross-species story", which is a +1, not a +2, advance.

### 5.4 Path B §8 over-credits Item 6 (Formal rigour)

PI claims +3 on Item 6 ("K > 0.30 is a derived prediction"). I give +2. The derivation holds up as an *interpretive bound derivation* but the critical σ²_ε/(γ²σ²_g) ∈ [0.4, 2.5] bounds are literature-calibrated priors, not deductive consequences of A1–A4. The "80 % posterior probability" claim silently uses a uniform prior that is not robust across reasonable prior specifications. Path B's §7 "NOT claims" section itself admits this limitation ("Not a theorem in the classical sense of T1–T4"); the self-score of +3 should have been +2 by the author's own caveat.

### 5.5 Path A §4 under-credits Item 5 (missed the breadth regression)

PI claims 0 on Item 5. I assign −1. The two-tier H4 expands the molecular-breadth ambition across 4+ phyla while H2 simultaneously demands 50+ behavioural cases across 6+ phyla. The feasibility product (case-breadth × molecular-breadth) is *tighter* than v4.0. The PI did not track this interaction. This is the single most important disagreement — it's the one where the PI didn't just over-claim but actually *missed a regression*.

### 5.6 Path C §5 over-credits Item 10

PI claims +2 on Item 10. I give +1. Three specific deductions: (a) Chinese-language corpus is scheduled-not-scanned, (b) the WebSearch-based scan is not API-native for bioRxiv, (c) the bioRxiv deposit itself is draft-not-deposited. Each is individually fixable but at the state of the audit, only +1 is defensible.

### 5.7 Item 7 under-credited by PI

One disagreement in the PI's favour: PI keeps Item 7 flat at 8. I raise to 9 (+1). The two-tier H4 falsification architecture with the 6-row dependency table (including separate case-(i) and case-(ii) H4b failure pathways) is meaningfully better pre-registration discipline than v4.0's monolithic H4. The PI missed this upgrade.

**Net effect of disagreements:** PI over-claimed by +1+1+1+1+(-1)+1-(-1) = +5 points. My 60 vs PI's projected 69 reflects these accounting corrections.

---

## Part 6: Bottom Line

**v4.1 Novelty Score: 60/100. GATE NOT PASSED (threshold 65).**

Paths A, B, C produced genuine progress (+8 points net) but the PI's self-scoring over-claimed by ~9 points across Items 1, 4, 5, 6, 8, 10. The single most important substantive concern is the cross-species × cross-phylum feasibility regression introduced by the two-tier H4 design (Item 5 went from 7 to 6), which the PI did not flag.

**Andy's morning decision tree (2026-04-24):**

1. **Do not advance to S5 execution at the Proc R Soc B target.** The gate has not passed.
2. **Execute Path D immediately (bioRxiv + OSF deposit on 2026-04-24 morning).** +2 points → 62. Also closes the Item 10 "unexecuted deposit" deduction.
3. **Execute Path E within 2–4 working days.** Wanfang/CNKI scan (E1), prior-robustness analysis for Path B (E2), Stern-2013-style convergence-literature engagement for Path A (E3). +3 points → 65.
4. **Re-audit at S4.v3 after D+E complete.** At 65/100, gate passes and S5 may proceed with *Proc R Soc B* primary.
5. **Optional Path F (operationalise F2 for invertebrates)** if schedule tolerates +1 week. Moves score to 68–70 and increases *Proc R Soc B* acceptance probability.

**If Andy wants to submit at 60/100 anyway (overriding the gate):** switch primary target to *eLife Reviewed Preprint*, move *Proc R Soc B* to secondary. This requires explicit Andy-override signoff per the SOP and must be logged.

**I do not recommend submitting to Proc R Soc B at 60/100.** The review-stage rejection probability is ~45–55% at that score, which wastes 2–3 months of the 12-week pipeline and produces a reviewer history that a second Proc B submission of the revised paper would have to contend with.

**Paths D+E are 3–5 working days of work and close the gate cleanly.** The effort-to-payoff ratio is strongly positive. Recommend execute.

---

*Audit completed 2026-04-23 evening (Andy asleep; Claude autonomous per Collaboration Protocol v1 fork windows) by novelty-audit agent as independent adversarial evaluator per Stage-Gate SOP v1.0 and the agent charter. This audit may be overridden only by explicit Andy + co-author signoff, logged in WORKLOG.md with rationale.*

*Internal-consistency note: this audit used the same 10-item checklist, same threshold, and same scoring rubric as `novelty_audit_s0_v4.md`. Where per-item scores changed, the change is justified against specific v4.1 design evidence, not against the PI's claims.*
