# Stage 0 Decision Memo — Biological Reframing

**To:** PI (Andy) + Coauthor (L. An)
**From:** PI Strategy (agent)
**Date:** 2026-04-20
**Status:** Decisions required (§6) before Week 0 pre-registration deposit.

---

## 1. The Reframed Research Question

**Sweet Trap — the decoupling of proximate reward from fitness consequence under voluntary endorsement — is a biologically general phenomenon produced by evolutionary conservation of a shared reward architecture.**

Three operational hypotheses (full text: `research_question_and_hypotheses.md`):

- **H1:** In humans, Sweet Trap is simultaneously measurable as behavioural, biomarker, and genetically-instrumented causal evidence across ≥ 5 cohorts and ≥ 3 ancestries.
- **H2:** Sweet Trap occurs in ≥ 50 animal species spanning ≥ 6 phyla (extension of current 20-case v2 meta).
- **H3:** Susceptibility to Sweet Trap shows phylogenetic signal (Blomberg's K > 0.3, Pagel's λ > 0; likelihood-ratio test p < 0.05) — it is inherited, not convergent.
- **H4:** Reward-system receptor machinery (D1-D5, μ-opioid, TAS1R, orexin/NPY) is conserved across ≥ 6 phyla at dN/dS < 0.15 (ligand-binding domains), significantly below genome-wide baseline.
- **H5:** Cross-species susceptibility covaries with life-history traits in phylogenetically-controlled regression.

Hypotheses are designed to be independently falsifiable. H2 is the critical path; H3-H5 modulate framing but not publishability. H1 fails gracefully (paper becomes animal-only).

---

## 2. Evidence Architecture (Three Parts, Not Four Layers)

| Part | Claim | Data sources | Analysis | Lead output |
|------|-------|--------------|----------|-------------|
| **Part 1** Human | Sweet Trap in humans | NHANES 1999-2023, UK Biobank, HRS, ELSA, SHARE, Add Health Wave V; GBD 2021 anchor; MR across UKBB + FinnGen + BBJ + MVP + AoU | Pooled random-effects β; biomarker dose-response; trans-ancestry MR-APSS | 1 figure: forest (6 cohorts) + biomarker curves + trans-ancestry MR |
| **Part 2** Cross-animal | 50+ cases, phylogenetically structured | PRISMA search (WoS/PubMed/Scopus/bioRxiv); TimeTree 5 + Open Tree of Life; PanTHERIA + AnAge; GBIF | DL random-effects meta; Blomberg K + Pagel λ + SIMMAP; PGLS | 2 figures: tree-on-forest; SIMMAP + PGLS |
| **Part 3** Molecular conservation | Deep conservation of reward machinery | Ensembl + Ensembl Metazoa + OrthoDB + UniProt + InterPro | OrthoFinder + PAML branch-site + MCScanX synteny; genome-wide dN/dS baseline | 1 figure: phylogeny + dN/dS heatmap + synteny |

The **one-figure-paper distillation** is: the phylogeny of Animalia with Δ_ST on tips and reward-receptor conservation on a sidebar.

Full mapping of v3.x assets (keep/adapt/shrink/drop) in `evidence_architecture_v4.md §5`.

**Dropped from v3.x:** T2 intervention-asymmetry theorem; Layer B 3,000 specs (compressed to SI); Layer C ISSP (compressed to SI); T4 engineered escalation; §11 engineered deception; cross-level A+B+D meta (the cover-letter self-damage at NHB); all HSSC humanities/policy framing.

---

## 3. Journal Decision

**Primary: *Proceedings of the Royal Society B*. Backup: eLife (Reviewed Preprint). Reformat-ready second: Current Biology (Report format).**

- Proc B fit score 9.0/10: scope match, methodology expectation alignment, 45-60 day decision, no senior-author-snobbery risk.
- Desk-reject estimate: 18-25 %. Nat Ecol Evol was evaluated and rejected (desk-reject ~65 %, decision cycle 90-120 days, senior-author norm).
- Full target comparison: `journal_matching_v4.md`.

Under-10-week decision path: submit Proc B Week 9; if desk reject Week 10, 1-week reformat to eLife or Curr Biol; submit by Week 12. Gets us a decision (either venue) before project hit 4 months old.

---

## 4. 12-Week Timeline — Key Milestones

Full plan: `gantt_12_weeks.md`.

| Week | Milestone | Gate |
|------|-----------|------|
| 0 | OSF pre-registration deposit | — |
| 1-2 | PRISMA search + Part 3 ortholog pull + cohort access | — |
| 3 | First Part-1 NHANES analysis + Part-3 first dN/dS | — |
| **4** | All three Parts produce preliminary numerical results | **GATE 1: feasibility** |
| 5-6 | Robustness + sensitivity + PGLS + SIMMAP + trans-ancestry MR | — |
| 7 | Manuscript first draft | — |
| **8** | Internal peer-review by 3 agents + hostile-referee simulation | **GATE 2: manuscript quality** |
| 9 | Submit to Proc R Soc B | — |
| **10** | Proc B desk decision | **GATE 3: decision** |
| 11-12 | Buffer, reformat to backup, or respond to reviewers | — |

**Critical path:** Part 2 (load-bearing H2). External-coder reliability ($300 total) runs in parallel Week 3-6 without blocking critical path.

**Key risks & mitigations:** `gantt_12_weeks.md §Risk Register`. Most consequential: Part 3 dN/dS null (30 % probability) — mitigation is to reframe as "conservation-at-baseline-rate" rather than abandoning Part 3.

---

## 5. Competing Literature Posture

Closest antecedents: Robertson et al. 2013 (evolutionary trap field-defining paper); Hale & Swearer 2016 (largest prior meta); Nesse 1994 + 2019 (evolutionary mismatch theoretical parent).

**Sweet Trap's delta** (full analysis: `competing_literature_map.md`):
- Operational scalar Δ_ST allows cross-case quantitative comparison (novel).
- Phylogenetic-signal test on decoupling magnitude (never done before).
- Trans-ancestry MR + cross-phylum molecular conservation combined with comparative meta in one paper (novel).
- Formal separation of F1 (decoupling) from F2 (voluntary endorsement) clarifies conflation in HIREC/ecological-trap literatures.

**Must-cite lineage under-engaged in v3.x:** Nesse (mismatch theory direct parent), Stearns (life-history evolution, for H5 PGLS), P. Bateson (development + plasticity), Zuk (applied mismatch), Kokko (recent Fisher-runaway theory), Robertson (ongoing field leader).

**Competing threat:** A well-funded lab could produce a similar phylogenetic-signal paper in 6-12 months. Our timing advantage is the 12-week horizon.

---

## 6. Three Decisions the PI Needs to Make Now

### Decision 1 — Pre-registration timing

**Recommended:** Deposit the three core design documents (`research_question_and_hypotheses.md`, `evidence_architecture_v4.md`, `analytical_pipeline.md`) on OSF **at end of Week 0 (this week)**, before any new data extraction. The hostile-reviewer "post-hoc pre-registration" objection on the v3.x Layer B is avoided if we are genuinely ex-ante.

**PI choice required:** Confirm OSF deposit at end of Week 0 (yes/no/modify). Note: this commits us to the 5 hypotheses and their predicted magnitudes as stated.

---

### Decision 2 — Cohort access strategy

**The question:** Part 1 (human) works best with all 6 cohorts (NHANES, UKBB, HRS, ELSA, SHARE, Add Health V). HRS / ELSA / SHARE access takes 2-6 weeks of application processing.

**Options:**
- **(a) Parallel-apply now and accept the cohorts that come through by Week 6.** Part 1 reports on whichever cohorts are accessible at analysis deadline. Low effort, some schedule risk.
- **(b) Apply now but pre-commit to NHANES + UKBB + Add Health as the minimum set.** Safer timeline. Gives up ~2 of 6 cohorts.
- **(c) Shrink Part 1 to NHANES + UKBB only.** Simplest but weakest Part 1.

**PI recommendation:** Option (a). The worst case ( = (b)) is acceptable.

**PI choice required:** Confirm (a) / (b) / (c).

---

### Decision 3 — Author profile for submission

**The question:** Prior NHB and HSSC reviews both flagged author-profile signals (both 0009- ORCIDs, Mammary Gland affiliation, no senior behavioural-scientist coauthor). Proc B is tolerant of early-career authors, but not infinitely so; a senior evolutionary-biology coauthor would reduce desk-reject risk by an estimated 5-10 percentage points.

**Options:**
- **(a) Submit as two-author (L.A. + H.X.) unchanged.** Cleanest; no coordination overhead. Accepts baseline 18-25 % desk-reject.
- **(b) Solicit a senior evolutionary-biology coauthor between Weeks 4-7.** Who: a Chinese evolutionary-biology faculty member (Liang-jun Wu at IOZ? Hanna Kokko via cold email?) with publications in Proc B. Offer: co-author on the manuscript for substantive methodological input.
- **(c) Delay submission by 4-6 weeks while a senior coauthor is recruited.** Defensive but costs timeline.

**PI recommendation:** (a) for Proc B primary submission; if desk-rejected and re-submitting to NEE or Curr Biol, execute (b) before that re-submission. Rationale: Proc B is our lowest-risk target and a senior coauthor is not required there; NEE/Curr Biol brands benefit from one.

**PI choice required:** Confirm (a) / (b) / (c).

---

## 7. Immediate Next Action

**First downstream task to launch (Week 1 start):** **Part 2 PRISMA systematic-review execution.**

Rationale: Part 2 is the critical-path load-bearing component (H2). It determines the rest of the paper's viability. Everything else (Part 1 cohort access, Part 3 ortholog pulls) can run in parallel, but Part 2 coding is the rate-limiter for submission.

Specific Week 1 launch:
- Assign literature agent to execute the 6 pre-specified keyword-cluster searches across PubMed, Web of Science, Scopus, bioRxiv.
- Target 150+ candidate papers at title/abstract screening by end of Week 1.
- Coding sheet (F1/F2/Δ_ST/Tier/Quality) finalized and committed to OSF Week 0.

Secondary parallel launch (same week): **Molecular-evolution agent pulls Ensembl + Ensembl Metazoa + OrthoDB data for the 15 target receptor genes.** No dependency on Part 2; can start immediately.

---

## 8. What the PI Loses By Making This Pivot

Honesty demands naming the sunk costs:

- **6 working days of NHB + HSSC preparation work** (v3.0 → v3.4 manuscript revision, cover-letter iterations, figure tofu repair).
- **The policy/humanities framing** that integrated Schor/Frank/Veblen/Sen. That framing is not lost forever — it is a potential Paper 2 once the biological claim is established.
- **T2 intervention-asymmetry theorem** (1.5 floor), which represented the project's most distinctive theoretical move. T2 remains in archived v3.x but is no longer claim-in-chief.
- **3,000-spec robustness** on China panel — compressed to SI. This was a methodological signature move but does not serve the biological headline.

**Net honest assessment:** The pivot is painful (non-trivial sunk cost) but structurally sound. The prior architecture had five sources of simultaneous reviewer-risk (umbrella construct + breadth-without-depth + FinnGen-only + affiliation signal + policy overreach). The reframed architecture has **one** primary reviewer-risk (50-case meta + phylogenetic signal must succeed), with explicit fallback framings for H3/H4/H5 failures. Risk-adjusted expected value of submission is substantially higher.

---

*Memo version 1.0. Authored by PI. ~1,450 words across 2 pages.*
