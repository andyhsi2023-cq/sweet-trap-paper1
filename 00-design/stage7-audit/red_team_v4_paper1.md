# Red Team Review: Sweet Trap v4 Paper 1
**Stage**: S7 (Pre-Submission Audit)
**Target journal**: eLife (Reviewed Preprint model)
**Date**: 2026-04-25
**Prior context**: Yes (project history consulted)
**Manuscript**: `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/manuscript.md` (5,638 words)

---

## 0. Desk-Reject Probability

**Overall desk-reject probability at eLife: 55–65%.**

eLife's Reviewed Preprint model has lower desk-reject thresholds than Nature/Science, but senior editors still screen for (a) fit-to-remit, (b) evident overreach, and (c) internal contradiction. This manuscript trips at least two of the three.

### Top-3 fatal-flaw candidates (ranked)

1. **Construct-phenotype-molecular mismatch is near-fatal.** The paper's central claim is about *reward-fitness decoupling under voluntary endorsement* ($\Delta_{ST}$) across 114 animal cases spanning moths/turtles/humans/nematodes. The molecular evidence (Parts 3–4) is about **sweet-taste receptors** (TAS1R / Gr) plus dopamine receptors. Sea turtles ingesting plastic, moths at streetlamps, and *Nematoda* cases do not involve sweet-taste receptors — they involve olfactory receptors, celestial-compass photoreceptors, and pheromone/CO₂ detection. The manuscript slides between "reward architecture in general" and "sweet receptors specifically" without a formal bridge. A desk editor reading §3.3–3.4 will notice that the molecular test for convergence is being done on a receptor family that is not implicated in the majority of the 114 animal cases that supposedly operationalise the construct. §4.4 even concedes: "A canonical *sweet-taste phenotype* has been invented twice" — but the paper's remit is not sweet-taste, it is reward-fitness decoupling.

2. **Post-hoc reframe of the main phylogenetic result (Deviation #5) is editorially conspicuous.** The pre-registered H3 predicted $K > 0.30$ from the A1–A4 axioms (§2.1, "$P(K > 0.30) \ge 0.92$"). The realised $K = 0.117$ with $p = 0.251$ — a null. Deviation #5 (table line 162) then **reframes the null as confirmatory for convergence**, citing @losos2011convergence and @stern2013genetic. This is structurally the "HARKing-after-null" pattern Kerr (1998) warned about and that Nosek et al. (2018) formalised as a pre-registration transparency failure. No matter how well-argued the reframe is philosophically, an editor sees: (a) pre-reg predicted positive signal with 92% prior, (b) observed null, (c) authors now claim the null was the predicted pattern all along. Under pre-registration transparency norms the correct move is to publish the disconfirmation *as* disconfirmation of the BM-inheritance hypothesis, not to re-derive convergence from it. This alone can carry desk-reject weight at Nature-family journals; at eLife it will certainly be raised by the first public reviewer.

3. **Part 4 H6a clade-significant result rests on n=4 honeybee Grs with Bonferroni $p = 0.049$, right at the screening boundary, from a realised denominator (n=21) that is less than half the pre-registered denominator (n=60).** Deviation #4 shrinks the gene scope from 15 to 4, which mechanically inflates the realised-$\alpha$ threshold 2.86× ($8.3\times 10^{-4} \to 2.4\times 10^{-3}$). The *Apis* clade "clears" Bonferroni-prereg at $p = 0.049$ — one rounding away from failing. Combined with the $\omega = 36.2$ on a 4-taxon clade (known boundary-estimation artefact on small trees, explicitly cited for tip foregrounds but not applied consistently to small clades), the sole positive signal is fragile. A methodological reviewer who re-runs with PAML's bootstrap clade-support will ask: does the signal survive removal of any single *Apis* Gr sequence?

---

## 1. Hostile Referee — First-Order Objections

### 1.1 The construct does not fit the molecular evidence
**Passage**: §3.3 / Table 3 (manuscript lines 217–244); §1 Introduction (lines 53–57).
**Why it fails**: The Introduction anchors Sweet Trap on moths-at-streetlamps, turtles-eating-plastic, and ultra-processed food. None of these three flagship cases involves sweet-taste receptors. Moths use celestial-compass photoreception [@fabian2024light]; turtles use olfactory volatiles [@santos2021plastic]; UPF mortality is dopaminergic + multi-system, with TAS1R involvement peripheral. Yet §3.3–3.4 evidence is **entirely** TAS1R / Gr_sweet / DRD. The cross-phylum Jaccard = 0 result the manuscript advertises as the convergence signature is a statement about **sweet taste**, not about the operational construct $\Delta_{ST}$. This is a bait-and-switch that the first reviewer will make explicit.

### 1.2 The H3 null is either H3 failure or H3 was never falsifiable
**Passage**: §2.1 (line 93) vs Deviation #5 (line 162) vs §3.2 (line 208) vs §4.2 (line 317).
**Why it fails**: The manuscript simultaneously claims (i) the A1–A4 axioms predicted $P(K > 0.30) \ge 0.92$ and (ii) the observed $K = 0.117$ (opposite direction) *confirms* the theory. Both cannot be true. Either the axioms generated a falsifiable prediction (in which case H3 failed and the paper should say so) or they did not (in which case §2.1's Supplementary Note S1 derivation is post-hoc). The falsification criterion in §2.3 (line 119) is explicit: "H3 fails if both $K < 0.10$ and Pagel's $\lambda$ 95% CI includes 0." Observed: $K = 0.117$ (0.017 above the threshold — essentially at it) and $\lambda$ CI = [0.0001, 0.413] (includes 0). **The pre-registered criterion is essentially triggered.** The manuscript never says this. A skeptical reviewer with the `phylosig_main.csv` in hand will.

### 1.3 $I^2 = 0\%$ across ancestries is being overstated
**Passage**: §3.1 (lines 174, 176), Table 1 (lines 184–191), Abstract (line 44).
**Why it fails**: $I^2 = 0\%$ is being presented as "consistency signal" across EUR/EAS/AFR. But examine the EAS row for BMI $\to$ mortality: OR = 1.10 with 95% CI [0.54, 2.24] ($p = 0.79$). A CI this wide contains essentially any EUR effect and would force $I^2 = 0$ *regardless of the underlying truth*. This is not consistency; it is statistical inertness. The correct interpretation is that EAS and AFR are non-informative about between-ancestry heterogeneity, because EAS $n = 1{,}122$ and AFR $n = 3{,}732$ are 400× and 100× smaller than EUR. The abstract's claim of "between-ancestry $I^2 = 0\%$" is technically true but substantively misleading. See Higgins & Thompson (2002, *Stat Med*) on low-$I^2$ interpretation under heterogeneous precision.

### 1.4 The Part 2 case corpus has two-coder reliability, externally recoded = "in progress"
**Passage**: §2.3 (line 111), §3.2 (line 206), §4.6 (line 331).
**Why it fails**: The pre-registered protocol required Fleiss' $\kappa \ge 0.70$ across three external coders on a blinded 30% sample. §4.6 concedes blinded external recoding is "in progress." The headline claim of "114 F1+F2 cases across 7 phyla" therefore rests on *two authors* coding their own construct against their own criteria. This is the inter-rater reliability failure mode the Cochrane Collaboration (Higgins et al. 2019, §8.4) flags as high-risk. A reviewer will ask why the paper is submitted before the pre-registered IRR check completed. The answer — "we promised it" — will not satisfy.

### 1.5 UPF deviation is framed as "instrument failure"; the alternative reading is "null result on the fifth chain"
**Passage**: Deviation #1 (line 158).
**Why it fails**: The pre-registered 5th chain returned OR = 0.906 with $p = 0.064$ (borderline protective — opposite direction from prediction). The manuscript attributes this to "healthy-eater bias" in processed-meat NOVA-4 proxy and defers the chain. But the pre-registered falsification criterion (§2.2 line 104) was "$\le 2$ of 4 chains show concordant direction" — after moving the goalposts from 5 to 4, 4/4 passes. Under the original 5-chain protocol, 4/5 still passes, but the point is the headline can only say "100% direction-consistent" by selectively removing the chain that failed. Reviewer will note that a protocol amendment motivated by a failed sub-test is a degree-of-freedom leak. See Simmons, Nelson & Simonsohn (2011, *Psychol Sci*) for why this counts as selective reporting.

### 1.6 Cnidaria is in Table 3 but Cnidaria has zero DRD orthologs
**Passage**: Table 3 (lines 231–239); Abstract claim "Class-A GPCR aminergic-receptor architecture is retained back to Cnidaria" (line 44).
**Why it fails**: The footnote below Table 3 (line 240) explicitly states: "A confirmatory whole-proteome reciprocal BLASTP scan across *Hydra vulgaris*, *Nematostella vectensis* and *Acropora digitifera* (n = 100,892 cnidarian proteins) recovered no true DRD orthologs." The Abstract, §3.3, and §4.3 nevertheless claim conservation "back to Cnidaria (~700 Myr; 4 phyla; n = 39)." This is achieved by redefining what is being conserved mid-paper: Tier-1 is DRD (3 phyla, not 4), Tier-2 is "Class-A GPCR aminergic" (4 phyla). But Class-A PF00001 is one of the most ancient and diverse Pfam domains — it is in effectively every bilaterian plus cnidarian genome regardless of reward function. Arguing that PF00001 presence in cnidarians supports a *reward-architecture* conservation claim is a scope slide from "DRD" to "any rhodopsin-like GPCR," which is ~800 receptors in the human genome alone. Fredriksson et al. 2003 (*Mol Pharmacol*) catalogues 241 non-olfactory Class-A GPCRs in humans; this domain is uninformative about reward-specific conservation.

### 1.7 Part 4 positive-control logic is asymmetric
**Passage**: §3.4 (lines 247–253), Table 2 (lines 263–289).
**Why it fails**: The hummingbird TAS1R1 result (LRT = 55.9, $\omega = 9.4$) validates the pipeline when the expected signal is present. The *Mus* tip (LRT = 0) validates when expected signal is absent. Fine. But the five "informative negatives" (*Drosophila* Gr64, *Drosophila* all-Grs, Lepidoptera, Coleoptera, *Aedes*) **all return LRT = 0.00 exactly**. In branch-site tests, an LRT of exactly 0.00 typically indicates boundary-constrained optimisation where the alternative model collapsed to the null — not a genuine biological negative. Anisimova et al. 2007 (*Genetics*) show this pattern in under-sampled clades. The fact that 5 of 6 production clades return LRT = 0.0 to three decimal places should flag concern about optimisation failure, not informative negative evidence.

### 1.8 "Foreground $\omega = 36.2$" is a red flag the paper quarantines for tips but not clades
**Passage**: §3.4 (lines 253, 265) + anisimova2007 citation.
**Why it fails**: The paper explicitly disqualifies tip foregrounds with $\omega > 50$ as "boundary-estimation artefacts" on small trees. The *Apis* clade foreground has n=4 taxa and returns $\omega = 36.2$ — in the same order of magnitude as the disqualified tips. Why does n=4 clade qualify but n=1 tip disqualify? If the answer is "because 4 > 1," the reviewer will note that the asymmetry is unprincipled; if the answer is "because clade ≥ tip categorically," the criterion should be pre-registered, not invoked post hoc. The primary H6a finding is quarantined by the same argument applied elsewhere in the same paper.

### 1.9 "Deep-time convergent architecture" claim is not properly tested against the null
**Passage**: §3.3 closing paragraph (line 227), §3.5 (line 301), Abstract (line 46).
**Why it fails**: The paper's convergence claim reduces to: Jaccard = 0 between vertebrate TAS1R Pfam and insect Gr Pfam. But **Jaccard = 0 between randomly-chosen vertebrate and insect GPCR pairs is not a rare event**. The Pfam system has ~20,000 domains; any two deep-time divergent receptor families are likely to carry non-overlapping Pfam annotations just by virtue of annotation granularity. Without a matched-random-ortholog baseline (which §2.4 line 128 pre-registered but §3.3 does not report), the Jaccard = 0 observation carries no distinctive evidentiary weight. Where is the distribution of Jaccard between vertebrate-non-TAS1R and insect-non-Gr orthologous pairs to show that 0 is the relevant tail?

### 1.10 The integrated §3.5 is four parallel findings with a claim of integration, not actual integration
**Passage**: §3.5 (lines 294–307).
**Why it fails**: Read literally, §3.5 summarises Parts 1–4 consecutively, then asserts they "close the core claim." There is no formal cross-Part test: no shared parameter estimated across Parts, no concordance statistic, no meta-analytic pooling across types of evidence. The integration is rhetorical, not statistical. An editor who wants to know what the reader should believe *because of the combination* vs. *because of Part 4 alone* has no quantitative answer. Gelman & Hill (2007, Ch. 21) on multi-source integration provides a template this paper does not follow.

### Recommendation: **Major Revision** (borderline Reject)

### Summary for the Editor
This manuscript attempts an ambitious four-part construct validation across humans, animal cases, molecular architecture, and positive selection. The central weakness is a mismatch between the broad construct (reward-fitness decoupling across 114 cases in 7 phyla) and the narrow molecular substrate (sweet-taste and dopamine receptors in 3–4 phyla). Combined with a pre-registered-null-reframed-as-confirmation pattern on the key phylogenetic-signal test, a fragile single-clade PAML result at the Bonferroni boundary, and inter-rater reliability deferred to post-submission, the paper is not yet ready for Reviewed Preprint status. The analyses are individually competent; the integration is not yet load-bearing.

---

## 2. Sympathetic Editor — Triage Call

### First 30 Seconds Impression
Title promises convergent evolution across Metazoa. Abstract is well-written and hits four evidence types. But two phrases in the abstract make me pause: "meta OR 1.121–1.414; $p < 10^{-3}$ on each; between-ancestry $I^2 = 0\%$" — the $I^2 = 0\%$ with UK-Biobank-subset EAS/AFR is suspiciously clean. And "A canonical sweet-taste phenotype has been invented twice" in the conclusion is a narrower claim than the title's Metazoa-wide "reward-fitness decoupling." The introduction (line 53) opens with moths, turtles, and UPF — none of which use the molecular substrate tested in Parts 3–4. That inconsistency between flagship cases and molecular evidence is what a public reviewer will hit first.

### Three Signals Checked
1. **Identification credibility**: ⚠️ MR design in Part 1 is standard and instruments look strong (mean F ~40–80). But presenting EAS (n=1,122) / AFR (n=3,732) UKB subsets as "trans-ancestry replication" overstates. The pre-registered Deviation #5 (K null reframed as convergence) is a transparency-cost I cannot ignore.
2. **Contribution first-order**: ⚠️ The *framework* (Sweet Trap construct + $\Delta_{ST}$ + four axioms) is ambitious and potentially first-order. Execution does not yet match ambition: Part 4 rests on a single clade at $p$-Bonferroni = 0.049 with foreground $\omega$ in the known-artefact range; Part 2 rests on two-coder IRR; Part 3 rests on a Jaccard statistic without a matched-baseline null.
3. **Literature engagement**: ✅/⚠️ Strong engagement with ecological-trap / convergence literature (Schlaepfer, Robertson, Stern, Losos). Thin engagement with the **convergence-null-detection** literature (Revell et al. 2008; Münkemüller et al. 2012 on phylogenetic-signal detection power; Harmon et al. 2019). The specific claim that a $K$ null *evidences* convergence needs more methodological grounding than @losos2011convergence alone.

### Decision: **Send to Public Review with Required Revision**

At eLife's Reviewed Preprint model I would forward to reviewers with explicit reviewer prompts on (a) construct–molecular-substrate fit, (b) the H3 pre-registration reframe, (c) the $I^2 = 0\%$ interpretation, and (d) the Part 4 single-clade boundary-$\omega$ concern. At a Nature-family journal this would be Desk Reject. At eLife, the Reviewed Preprint model tolerates work-in-progress, which mitigates (but does not eliminate) the IRR-in-progress and the Deviation #5 issues.

### Desk-Decision Letter Draft (if the editor chose to desk-reject; provided for calibration)

> Dear Drs An and Xi,
>
> Thank you for submitting your manuscript "Sweet Trap: Convergent Evolution of Reward-Fitness Decoupling Across Metazoa" to eLife. We have read the manuscript with interest and we recognise the ambition of the cross-scale construct-plus-phylogenetic-plus-molecular design.
>
> However, after internal discussion among the senior editors we have concluded that the manuscript in its current form does not meet our threshold for public review. Our primary concern is that the central molecular evidence (Parts 3 and 4) focuses on sweet-taste receptors and dopamine-receptor architecture, while the construct $\Delta_{ST}$ and the 114 animal cases span phenomena (phototaxis, chemoreception, cognitive UPF preference) whose mechanistic substrates are not these receptor families. A second concern is the reframing of the pre-registered phylogenetic-signal prediction ($K > 0.30$ with 92% prior) as confirmatory of convergence after the observed $K = 0.117$ null — this is a transparency issue that will dominate any public review we can arrange.
>
> We would welcome a revised submission in which the molecular evidence is either broadened to cover the receptor families relevant to the flagship cases, or the construct scope is narrowed to claims the molecular evidence can support. The pre-registration-adherence issue on H3 should be addressed either by reporting the null as disconfirmation of the BM-inheritance hypothesis (and building the convergence argument separately) or by providing a pre-registered alternative prediction that the null could confirm.

---

## 3. Methodological Expert — Technical Audit

### Part 1 (Mendelian Randomization)

**Measurement / Data Weaknesses**
1. **Leisure screen-time instrument (ukb-b-5192) has mean F = 40.8** — the weakest of the four pairs, and under a two-sample MR Egger-intercept test the SE ballooning (Egger $p = 0.27$) is consistent with invalid-instrument bias undetected by F-threshold. Under Bowden et al. 2016 (*IJE*) InSIDE violations, the IVW estimate is biased toward non-zero values when heterogeneity is high. With $Q_{\text{IVW}}$ $p = 2 \times 10^{-6}$ for screen-time, InSIDE is likely violated.
2. **Sugar-intake instrument (ukb-b-5237, $n_\text{SNP}=38$) has mean F = 61.6 EAS / 74.5 EUR**, but the exposure GWAS is a single UKB phenotype. There is no external validation from an independent sugar-intake cohort (e.g., EPIC, NHS II). Without this, the Jones et al. 2019 (*IJE*) winner's-curse correction should be applied but is not reported.
3. **All four outcome GWAS are all-cause or CVD-cause mortality**. These are composite endpoints with heterogeneous biological mediators. A proper Sweet Trap test requires decomposition to metabolic (BMI-mediated) vs behavioural (screen-mediated) mortality pathways — otherwise the four chains may be measuring partly-overlapping liability.

**Unaddressed Identification Threats**
1. **Correlated pleiotropy** is untested. MR-Egger intercept tests directional (uncorrelated) pleiotropy. MR-CAUSE (Morrison et al. 2020, *Nat Genet*) or LHC-MR would be appropriate for correlated pleiotropy, especially on BMI $\to$ mortality where metabolic-trait correlation is pervasive. Not reported.
2. **Assortative mating + dynastic effects** on alcohol and BMI: Brumpton et al. 2020 (*Nat Commun*) show within-sibship MR gives smaller effects than population MR for these exposures. No within-sibship sensitivity reported.
3. **Collider bias from UKB healthy-volunteer selection** (Fry et al. 2017, *Am J Epidemiol*): all three instruments + the EUR mortality outcome come from UKB variants. Non-random participation creates collider paths. Schoeler et al. 2023 (*Nat Hum Behav*) demonstrate measurable MR-effect-size inflation from this pathway on behavioural exposures.

**Missing Deliverables**
1. No MR-PRESSO global test reported despite §2.2 (line 100) noting "MR-PRESSO" in methods.
2. No Radial-MR outlier plots despite §2.2 (line 100) specifying them.
3. No Steiger-filtered estimates reported — methods state "Steiger filtering left causal-direction calls intact" (§3.1 line 178) but no before/after numbers.

**Part 1 Verdict**: **Needs patching** (not re-execution).

### Part 2 (PRISMA phylogenetic signal)

**Measurement / Data Weaknesses**
1. **$\Delta_{ST}$ is coded on a 0–1 interval from "reported effect sizes" (§2.3 line 109)** with no formal conversion function. Different primary studies report different effect-size types (approach latency, mortality rate, reproductive success) — a unified operationalisation is sketched but not reported. The $\Delta_{ST}$ values in `animal_cases_final.csv` therefore carry author-discretion noise at each coding step.
2. **114 cases, 56 species after within-species averaging**: species-level pooling loses information unnecessarily. A phylogenetic mixed model (Hadfield & Nakagawa 2010, *J Evol Biol*) with case-within-species random effects preserves full sample.
3. **Blomberg's K has low power to detect signal at n ≈ 50 species when true $\lambda$ ∈ (0.3, 0.7)** (Münkemüller et al. 2012, *Meth Ecol Evol*; Fig 3). The observed null could be a Type II error, not absence of signal. No power analysis reported.

**Unaddressed Identification Threats**
1. **Publication bias in the primary literature**: "ecological trap" cases are published when cost is large and evolutionary response lags; cases where the trap resolved or never formed are not published. This introduces systematic bias toward high-$\Delta_{ST}$ cases in the corpus, potentially inflating apparent cross-phylum uniformity.
2. **Temporal sampling confound**: Part 2 samples report from 1995–2026. Modern (post-2010) cases over-represent anthropogenic stimuli (ALAN, plastics, UPF); older cases over-represent supernormal-stimulus examples. The phylogenetic signal test conflates phylogenetic with temporal-sampling structure.
3. **Ecological niche confound**: ALAN-vulnerable insect orders share both phylum and ecological exposure; treating the Arthropoda clustering ($K = 1.446$) as "clade-specific reinforcement" rather than "shared ecological exposure producing spurious phylogenetic signal" is not tested. PGLS on ALAN-exposure as a covariate should be reported. It is promised (§2.3 line 117) but not delivered in Results.

**Missing Deliverables**
1. **Fleiss' $\kappa$ on external coders** — pre-registered, not reported.
2. **PRISMA-ScR checklist table** — standard for published PRISMA work; not present.
3. **PGLS covariate-adjusted $\Delta_{ST}$ analysis** — methods promise body mass, generation time, niche breadth (§2.3 line 117); Results never report the adjusted signal.
4. **Ancestral-state reconstruction** — SIMMAP promised in §2.3 line 115, never reported.

**Part 2 Verdict**: **Needs re-execution** on (IRR complete, power analysis, PGLS covariate-adjusted signal, and ALAN-stratified test).

### Part 3 (Molecular convergent architecture)

**Measurement / Data Weaknesses**
1. **Pfam Jaccard is a coarse metric**. Pfam domains are annotation constructs, not biological units. Two proteins with identical fold and function but different Pfam annotation will show Jaccard = 0; two distantly related proteins with shared accessory domain will show Jaccard > 0 despite no functional similarity. The ELM (Gouw et al. 2018, *NAR*) or Pfam-clan-level analysis (Finn et al. 2016, *NAR*) would strengthen the claim. Neither reported.
2. **The "two-tier separation" (DRD vs Class-A GPCR broader)** is a post-hoc resolution of the fact that Cnidaria has no DRD orthologs. Defensible as a biological fact but presented as if the tier structure was pre-registered. §2.4 line 128 does not pre-register a two-tier analytic plan.
3. **Cnidarian exclusion is argued twice**: once in the main text (line 221), once in the footnote to Table 3 (line 240). The two-tier framing allows cnidarians to be claimed for Tier-2 PF00001 conservation while excluded from Tier-1 DRD conservation. But Tier-2 conservation (all Class-A GPCRs carry PF00001) is essentially tautological: PF00001 is the defining Pfam of Class-A GPCRs. This is sampling on the dependent variable.

**Unaddressed Identification Threats**
1. **No matched-random-ortholog Jaccard baseline**. The significance of Jaccard = 0 between TAS1R and Gr is uninterpretable without knowing the expected Jaccard between two randomly-chosen vertebrate-insect orthologous pairs. Pre-registered (§2.4 line 128) but not delivered.
2. **Orthology inference with OrthoFinder on a 25-taxon tree** for DRD classification may under-recover true orthologs in non-model taxa. Expanding to OrthoFinder-SCORPiOs or PhylomeDB for validation is not done.
3. **Synteny cross-check (MCScanX + Genomicus, §2.4 line 134)** is promised but not reported in Results.

**Missing Deliverables**
1. Matched-random-ortholog Jaccard distribution (pre-registered, missing).
2. dN/dS ratios on LBD codons against genome-wide 500-ortholog baseline with Wilcoxon (§2.4 line 128, pre-registered, missing).
3. Downstream pathway-module presence test via STRING/Reactome across $\ge 4$ phyla (§2.4 line 132, pre-registered, missing).

**Part 3 Verdict**: **Needs patching** (matched baselines + PGLS + pathway module test) + clarify the two-tier structure as post-hoc.

### Part 4 (Branch-site positive selection)

**Measurement / Data Weaknesses**
1. **Bonferroni denominator manipulation**: $\alpha_\text{prereg} = 0.05/60 = 8.3 \times 10^{-4}$; $\alpha_\text{realised} = 0.05/21 = 2.4 \times 10^{-3}$. Reporting both is transparent, but the realised alpha is a *larger* alpha, which makes borderline results more likely to pass. The *Apis* Bonferroni-prereg $p = 0.049$ becomes "more significant" at realised-$\alpha$ ($p = 0.017$), but this is a mechanical consequence of reducing the denominator. Neither threshold was motivated from first principles; the 60 came from pre-registering 15 genes × 4 clades, the 21 came from what got run. Benjamini-Hochberg $q = 0.006$ is a cleaner adjustment for exploratory work.
2. **Foreground $\omega_{2a} = 36.2$ on a 4-taxon clade**: at these taxon sizes, the M-A model's site-class-2 $\omega$ is known to inflate beyond the biologically-meaningful range (Anisimova & Yang 2007, *Genetics*). The paper quarantines this for tips but not for small clades. The correct triangulation is to run (a) BUSTED (Murrell et al. 2015, *MBE*) for site-branch selection robust to small foregrounds, (b) aBSREL (Smith et al. 2015, *MBE*) for branch-specific selection without pre-specified foreground, and (c) RELAX (Wertheim et al. 2015, *MBE*) to rule out relaxation masquerading as positive selection.
3. **BEB sites (codons 533, 768) at $P \ge 0.90$**: neither exceeds the conventional $P \ge 0.95$ threshold for BEB confidence. The paper reports "0 at $\ge 0.95$, 2 at $\ge 0.90$" for *Apis* Gr. This is weaker than the presentation in Abstract and §3.4 suggests.

**Unaddressed Identification Threats**
1. **Alignment quality on the Gr family**: insect Gr sequences are notoriously divergent; the 1078-codon alignment is longer than most Gr ORFs, suggesting substantial gap columns. PAML's treatment of gap columns is sensitive to alignment algorithm. Re-alignment with PRANK (probabilistic, gap-aware) vs MAFFT should be shown as sensitivity.
2. **Tree-topology uncertainty**: a 4-taxon *Apis* clade gives no internal resolution. Rapid-topology-change effects on branch-site tests (Venkat et al. 2018, *Nat Ecol Evol*) are particularly severe at low taxon sampling. No topology sensitivity reported.
3. **Codon usage bias and GC content variation**: *Apis* has extreme AT-bias (~66% AT in coding regions) relative to *Drosophila* (~46% AT). GC-biased gene conversion can mimic positive selection. Galtier et al. 2018 (*Annu Rev Genet*) is the relevant reference.

**Missing Deliverables**
1. BUSTED / aBSREL / RELAX triangulation (strongly expected for any *Apis* clade positive-selection claim in 2026).
2. Alignment sensitivity (PRANK vs MAFFT vs Gblocks stringency).
3. Branch-site bootstrap clade-support (Anisimova & Yang 2007 recommend 100+ bootstraps on the foreground; paper reports none).

**Part 4 Verdict**: **Needs patching** (BUSTED/aBSREL/RELAX + alignment sensitivity + codon-bias control).

### Overall Methodological Verdict: **Needs patching across all four Parts, with Part 2 needing partial re-execution (IRR completion + PGLS + power analysis).**

---

## 4. Narrative Integrity — Does §3.5 Actually Integrate?

**No.** §3.5 is four parallel findings followed by a rhetorical claim of integration. There is no:
- Shared parameter across Parts (e.g., expected $\omega$ derivable from $\Delta_{ST}$).
- Concordance statistic testing whether the four Parts agree more than expected under chance concordance.
- Bayesian multi-evidence-source model pooling.
- Even a formal argument that Part 1 (humans) and Part 2 (animals) are testing the same construct rather than parallel traits named "$\Delta_{ST}$."

The paper's strongest possible integration claim — that convergent architecture (Part 3) explains cross-phylum null K (Part 2) and the *Apis* signal (Part 4) — is asserted in §4 but not quantified. Lamb et al. 2020 (*Ecol Lett*) on multi-evidence convergence tests shows what such integration should look like statistically. The current §3.5 is essentially "we found four things, and here's a narrative thread." An eLife public reviewer will call this the "stapled results" pattern.

---

## 5. Revealed Research Holes — Authors Should Disclose Proactively

1. **H3 triggered the pre-registered falsification criterion** ($K < 0.10$ is close-enough to $K = 0.117$ that reasonable readers will call it a pass, and $\lambda$ CI includes 0). Authors should say this explicitly in §3.2 and then defend the reframe, not silently bypass it.
2. **Part 2 IRR is not done**. This should be in the headline limitations, not buried in §4.6.
3. **Bonferroni-prereg $p = 0.049$ is one data-perturbation away from failing**. Authors should run leave-one-out (remove each *Apis* Gr sequence sequentially) and report.
4. **The 5 "informative negatives" in Part 4 all returning LRT = 0.000 exactly** is diagnostically suspicious for optimisation-boundary issues. Authors should re-run these with randomised starting-omega values per Yang & dos Reis 2011.
5. **No matched-random-ortholog Jaccard baseline** for Part 3. Pre-registered but missing.
6. **The construct $\Delta_{ST}$ is coded by two authors**. Even once IRR is run externally, the primary author-coding remains the ground truth. The entire Part 2 phylogenetic signal test inherits this coder-liability.
7. **PGLS covariate-adjusted analyses** promised in Methods §2.3 never appear in Results.
8. **The Abstract's "convergent evolution onto functionally equivalent reward architectures across phyla"** claim reduces, in the data, to Jaccard = 0 between two GPCR superfamilies on a specific receptor family (sweet taste). The generalisation from this to "reward architectures" broadly is not warranted by the evidence.

---

## 6. Acceptance Probability If Sent to Public Review

**eLife Reviewed Preprint posting: ~70% probability conditional on being sent to reviewers.**

eLife's Reviewed Preprint model does not gate on acceptance the way traditional journals do — reviewed preprints get posted with an eLife Assessment even if the assessment is "inadequate" or "incomplete." So conditional on being sent out, posting is near-certain. The substantive question is the **eLife Assessment wording**.

Realistic eLife Assessment prediction if the paper is reviewed as-is:
- **Significance**: "valuable" (not "important" or "landmark") — the construct is ambitious but the evidence is not yet decisive.
- **Strength of evidence**: "incomplete" (not "solid," not "compelling") — because of IRR-in-progress, construct-molecular mismatch, and the H3 reframe.
- Likely reviewer recommendation: substantial revisions to (a) narrow the claim to the molecular substrate actually tested, or broaden the molecular evidence to cover the flagship cases, and (b) report the H3 result as disconfirmation of BM-inheritance with convergence as a separate argument.

**Post-revision acceptance-of-revised-version probability: 50–60%** — contingent on addressing items 1–6 of Section 5.

**If aimed at a traditional journal (Nature Communications, PNAS, PLoS Biology) instead of eLife**: acceptance probability drops to **15–25%** pre-revision; **30–45%** post-revision.

---

## Final Synthesis: Bottom Line for the Author

Your framework is ambitious and potentially first-order. But the manuscript currently advertises a Metazoa-wide claim on the strength of sweet-taste receptor data, asks readers to accept a pre-registered null as confirmation of convergence, and rests its single clade-level positive-selection result at Bonferroni $p = 0.049$ with $\omega$ in the known-artefact range on n=4 taxa. Any one of these three, eLife's Reviewed Preprint model can absorb; all three together will produce an eLife Assessment in the "incomplete" band and a public review focused on scope-vs-evidence mismatch rather than on the science. The construct is real work. The current manuscript does not yet do it justice.

---

*Red-Team Review v1.0 — Stage 7 pre-submission audit, 2026-04-25*
