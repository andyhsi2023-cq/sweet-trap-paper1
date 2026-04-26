# 12-Week Gantt — Stage 6 Execution Plan (v4.2, Scheme C + eLife RPP)

**Start date:** 2026-04-24 (Friday, Week 0 → Monday 2026-04-27 Week 1 start)
**Target submission date:** Week 8-9 (2026-06-16 to 2026-06-23, eLife RPP portal)
**Primary venue:** **eLife Reviewed Preprint**
**Buffer weeks:** 10-12 for response-to-reviewers, OSF polishing, Paper 2 roadmap draft.
**Gates:** Week 4 (Feasibility), Week 7 (Internal Review), Week 9 (Submission).

---

## Architectural Change from v4.1 (2026-04-20)

- **Primary journal**: Proc R Soc B → **eLife Reviewed Preprint**. See `journal_matching_v4.md` v1.2.
- **Path F (Nematostella F2 operational)**: REMOVED. No longer needed at eLife RPP threshold 60+. Layer E fully moved to Paper 2 / Future Work roadmap.
- **Part 4 Genetic Causality**: COMPRESSED. Paper 1 executes H6a (positive selection scan) + H6f (cross-species genetic manipulation literature summary) only. H6b GxE / H6c parallel positive selection / H6d PRS / H6e recent selection → Paper 2 roadmap (6-12 months after Paper 1 publication).
- **Total research scope in Paper 1**: Part 1 Human (compressed) + Part 2 Animal (full) + Part 3 Molecular Architecture (full two-tier) + Part 4 Genetic Causality (lightweight, 2-3 weeks, H6a + H6f).
- **Submission timing**: moved slightly earlier because eLife RPP has shorter pre-submission internal-review cycle than Proc B (no need to anticipate desk-reject-based re-targeting).

---

## Week-by-Week Schedule

### Week 0 (2026-04-24 to 04-27) — Design finalisation + OSF & bioRxiv deposit

**Deliverables:**
- [ ] `journal_matching_v4.md` v1.2 finalised (complete 2026-04-24).
- [ ] `evidence_architecture_v4.md` v1.2 with §5 Part 4 added (this sprint).
- [ ] `research_question_and_hypotheses.md` with H6a + H6f added (this sprint).
- [ ] v3.x residue cleanup pass (Task #17, ~15 min).
- [ ] **Path D executed** (Andy approval required): bioRxiv priority preprint deposit + OSF full pre-registration; both timestamped in parallel.
- [ ] Docker/Singularity container built with R 4.4 + PAML + OrthoFinder + MCScanX + phytools + caper + ape + TwoSampleMR + MR-APSS + InterProScan.

**Agents:** PI (this plan); Data-engineer for container build.

**Gate criterion for Week 1:** OSF deposit timestamped; bioRxiv DOI assigned; container builds cleanly.

---

### Week 1 (2026-04-28 to 05-04) — Part 2 meta expansion start + Part 3 infrastructure + Part 4 planning

**Deliverables:**
- [ ] PRISMA search execution: PubMed + WoS + Scopus + bioRxiv across 6 pre-specified keyword clusters.
- [ ] Import existing 20-case coded set.
- [ ] Candidate-case pool reaches ≥ 150 after title-abstract screening.
- [ ] Part 3: Ensembl + Ensembl Metazoa + OrthoDB download scripts run.
- [ ] Reward-receptor target gene list finalised (DRD1-5, OPRM1/K1/D1/L1, TAS1R1-3, HCRTR1-2, NPY1/2/5R) — 15 target genes.
- [ ] **Part 4 H6a planning**: branch-site PAML codeml setup for 15 genes × (vertebrate sweet-food lineage + arthropod nectarivore + insect sensory-specialist + 2-3 CNGBdb Chinese-native species).

**Agents:**
- Literature agent (systematic review execution).
- Molecular-evolution agent (Ensembl/OrthoDB data pull).
- Molecular-evolution agent (PAML setup for H6a).

**Parallelism:** Part 2 meta search, Part 3 ortholog pull, Part 4 PAML setup all run simultaneously.

---

### Week 2 (2026-05-05 to 05-11) — Part 2 case coding + Part 1 cohort access + Part 4 CARSI PDF bulk download

**Deliverables:**
- [ ] Full-text screening of ≥ 100 candidate papers from Week 1 pool; target 50+ F1+F2-passing cases coded by authors.
- [ ] Coding sheet finalised; Tier 1/2/3 classification applied.
- [ ] Part 1: NHANES 1999-2023 data pull via CDC NHANES API; UKBB application status confirmed (pre-existing approval); HRS/ELSA/SHARE access requests submitted.
- [ ] Part 1: Crosswalk instrument finalised per cohort.
- [ ] Part 3: OrthoFinder run 1 on 6-phyla subset (Chordata, Arthropoda, Nematoda, Mollusca, Echinodermata, Cnidaria).
- [ ] **Part 4 H6f literature sweep**: via CARSI (Nature / ScienceDirect / Cell Press / Wiley / Springer) bulk PDF download of ~150 target papers; compile genetic-manipulation literature summary table (Drosophila DopR knockout, C. elegans NPR-1, mouse Drd2+/-, hummingbird TAS1R1 resurrection, etc.).

**Agents:**
- Literature agent continues case coding.
- Biobank-agent handles cohort access.
- Molecular-evolution agent runs OrthoFinder.
- CARSI-PDF-fetcher (Playwright-based) for H6f.

**Key risk:** HRS/ELSA/SHARE access processing may exceed 4 weeks. Mitigation: Part 1 behavioural stream succeeds on NHANES + UKBB + Add Health; delayed cohorts → SI.

---

### Week 3 (2026-05-12 to 05-18) — Part 2 coding closes + Part 3 first-pass dN/dS + Part 1 NHANES + Part 4 H6a branch-site

**Deliverables:**
- [ ] Part 2 coded case set closes at ≥ 50. If < 50, expand search via citation-snowballing.
- [ ] Part 2: phylogeny construction begins (TimeTree 5 mapping; grafting protocol for missing species).
- [ ] Part 3 H4a: codon-aligned sequences for 15 target genes across Chordata + Arthropoda; PAML codeml branch-model dN/dS run.
- [ ] Part 1: NHANES aspirational-behaviour × biomarker regression fitted.
- [ ] **Part 4 H6a first-pass**: branch-site Model A vs M1a LRT for 5 of 15 genes; identify positive-selection footprints on specific lineages (sweet-re-evolution hummingbirds per Baldwin 2014 as positive control).

**Agents:**
- Literature agent finalises case set.
- Phylogenetic-analysis agent starts.
- Molecular-evolution agent on H4a dN/dS + H6a branch-site (parallel).
- Biobank agent on NHANES.

---

### Week 4 (2026-05-19 to 05-25) — **GATE 1: Feasibility & signal strength**

**Deliverables:**
- [ ] All four Parts have produced preliminary numerical results.
- [ ] Part 2 preliminary meta: pooled Δ_ST on N ≥ 50; phylogenetic-signal K / λ first estimate.
- [ ] Part 3 preliminary: within-phylum LBD dN/dS for ≥ 5 of 15 target genes; cross-phylum InterPro Jaccard for sweet-receptor family vs random-ortholog baseline.
- [ ] Part 1 preliminary: NHANES + UKBB behavioural-β pooled with random-effects meta (2 of 6 cohorts).
- [ ] **Part 4 H6a preliminary**: branch-site positive-selection results for 5-8 of 15 genes; hummingbird TAS1R1 control validates pipeline.

**GATE 1 CRITERIA (updated for four-part architecture):**

| Signal | Go decision | No-go decision |
|---|---|---|
| Part 2 N ≥ 50 | ✓ proceed | < 40 → extend search another week; < 30 → reduce scope claim to "H2 ≥ 30" |
| Part 2 Δ_ST pooled > 0 (CI excluding 0) | ✓ proceed | CI crosses 0 → investigate outlier cases |
| Part 2 λ > 0 at p < 0.10 preliminary | ✓ proceed | λ ≈ 0 → reframe H3 to "convergent" rather than "inherited" |
| Part 3 H4a within-phylum dN/dS left-shifted vs baseline | ✓ proceed | If right-shifted (no conservation) → Part 3 reframes to partial |
| Part 3 H4b cross-phylum Jaccard > matched baseline on 1 gene family | ✓ proceed | If Jaccard ≤ baseline for all families → H4b falls; within-phylum-only claim |
| **Part 4 H6a branch-site produces ≥ 1 positive-selected gene on ≥ 1 lineage** | ✓ proceed | If zero positive selection detected across 8 gene-lineage pairs → H6a reframes to "purifying selection dominant" |
| Part 1 NHANES β in predicted direction with p < 0.10 | ✓ proceed | Null → re-examine crosswalk |

**PI decision required at end of Week 4:** continue, re-scope, or retreat. Re-scope options in `stage0_decision_memo.md` §4.

---

### Week 5 (2026-05-26 to 06-01) — Robustness & sensitivity + Part 4 H6f finalisation

**Deliverables:**
- [ ] Part 2: K and λ with 1,000 polytomy-randomisation bootstraps; leave-one-phylum-out sensitivity.
- [ ] Part 2: SIMMAP ancestral-state reconstruction with 100 replicates.
- [ ] Part 2: PGLS with life-history covariates on mammalian + avian subset.
- [ ] Part 3: H4a all 15 genes completed; branch-site M2a vs M1a test; genome-wide baseline comparison. H4b InterPro Jaccard + downstream DA→cAMP→PKA→CREB pathway-presence matrix across ≥ 4 phyla.
- [ ] Part 1: UKBB + HRS (if accessed) integration; pooled β across 3-4 cohorts.
- [ ] **Part 4 H6a robustness**: branch-site on all 15 genes × full lineage set; Bonferroni-corrected positive-selection gene list locked.
- [ ] **Part 4 H6f literature table finalised**: cross-species genetic-manipulation summary, ~30-50 papers tabulated.
- [ ] External coders begin receiving case descriptions (target: 3 coders, 50+ cases each).

**Agents:** All Part-specific agents run in parallel.

---

### Week 6 (2026-06-02 to 06-08) — Completion of analyses + figure drafts

**Deliverables:**
- [ ] Part 2 complete: meta + K + λ + SIMMAP + PGLS all locked; final tables & numbers.
- [ ] Part 3 complete: H4a + H4b full results; LBD-only analysis; baselined per species pair.
- [ ] Part 1: behavioural-β pool on all available cohorts; biomarker dose-response curves; trans-ancestry MR on 3-5 ancestries.
- [ ] **Part 4 complete**: H6a positive-selection map figure; H6f genetic-manipulation summary table.
- [ ] Figure drafts v1: Part 1 Figure, Part 2 Figure A (tree-on-forest), Part 2 Figure B (SIMMAP + PGLS), Part 3 Figure 3A + 3B, Part 4 Figure (positive-selection lineage map + H6f summary).
- [ ] External-coder results received and reliability computed.

**Agents:**
- Visualisation agent for figure drafts.
- Statistics agent for final number locks.

---

### Week 7 (2026-06-09 to 06-15) — Manuscript first draft + **GATE 2 internal review**

**Deliverables:**
- [ ] Main-text first draft, ~6,000 words (eLife Research Article word target; includes Introduction, Methods, Results, Discussion, with "Paper 2 Roadmap" paragraph flagging H6b-H6e + Layer E as future work).
- [ ] Abstract first draft, ~200-250 words.
- [ ] SI first draft covering: PRISMA flow; full 50+ case coding table; external-coder κ; dN/dS alignments; MR per-ancestry tables; NHANES spec-curve (500 specs); H6a branch-site complete output; H6f full lit table.
- [ ] Reference list updated (~180 refs, up from 150 estimate due to Part 4 H6f additions).
- [ ] **Internal peer-review by 3 agents** (mimicking eLife referee types): (a) phylogenetic-comparative, (b) molecular-evolution, (c) human-genetics MR.
- [ ] Each agent produces a 500-word review with 5-10 concrete critiques.
- [ ] **Hostile-referee review** (route-3 style) on full manuscript.
- [ ] Cover letter draft (≤ 400 words) for eLife RPP.

**GATE 2 CRITERIA:**

| Review outcome | Decision |
|---|---|
| All 3 internal reviewers recommend "send-to-review" | Proceed to Week 8-9 submission |
| 2 of 3 positive, 1 requests major method change | Make method change in Week 8; submit Week 9 |
| 2 of 3 negative (fundamental method or framing issue) | Halt; re-work; use buffer weeks 10-12 |
| Hostile review identifies ≥ 3 load-bearing problems | Halt; fix problems |

---

### Week 8 (2026-06-16 to 06-22) — Revision + eLife submission prep

**Deliverables:**
- [ ] All internal-review critiques addressed.
- [ ] Final manuscript + SI + figures + cover letter + reporting summary.
- [ ] **eLife submission materials finalised:**
  - Main text PDF
  - SI PDF
  - Figures (individual PDFs, publication-quality)
  - Cover letter (≤ 400 words; methodological-transparency emphasis)
  - Suggested reviewers: Bruce Robertson, one of Hale/Swearer, one of Kokko/Sol/Zuk, one molecular-evolution (e.g., Yamamoto/Feijó/Chao).
  - Editor-conflict declarations.

---

### Week 9 (2026-06-23 to 06-29) — **eLife Reviewed Preprint submission**

**Deliverables:**
- [ ] eLife portal submission Tuesday 2026-06-23 (earliest) or Thursday 2026-06-25 (comfortable).
- [ ] OSF full state confirmed: data + code + pre-registration + analysis protocol + manuscript snapshot.
- [ ] bioRxiv priority preprint (from Week 0) remains published; add "under review at eLife" banner per eLife RPP convention.

**eLife RPP process from submission:**
- Days 0-5: editorial triage (desk-reject or send-to-review). Expected: send-to-review, as RPP triage is broader than flagship journals.
- Days 5-30: peer review (2-3 reviewers).
- Days 30-42: reviewer reports + eLife Assessment draft.
- Days 42-45: authors respond to public review (optional).
- Day 45: **Reviewed Preprint published** with Assessment (Valuable / Important / Landmark × Solid / Compelling / Exceptional).

---

### Week 10 (2026-06-30 to 07-06) — eLife review monitoring + Paper 2 roadmap

**Deliverables:**
- [ ] Monitor eLife portal for reviewer comments (days 15-30 from submission).
- [ ] Begin Paper 2 scoping: H6b GxE interaction analytical plan; H6c parallel positive selection across 3-5 CNGBdb Chinese-native species; H6d PRS discriminant validity for 5 Sweet Trap human domains; H6e ancient DNA selection scan in human lineage.
- [ ] Begin Layer E roadmap (Paper 3 horizon): Nematostella behavioural approach-assay protocol; Aplysia reward-circuit protocol; bumblebee 3-site F2 operational definition.

---

### Weeks 11-12 (2026-07-07 to 07-20) — Buffer / response / Paper 2 prep

**Deliverables in buffer weeks:**
- [ ] If reviewer reports arrive: respond to public review; decide whether to upload revised version.
- [ ] If Reviewed Preprint published with "Valuable / Solid" or higher: Paper 1 done; pivot fully to Paper 2.
- [ ] If reviewer assessment weak ("Incomplete" or "Inadequate"): accept public record; carry reviewer critiques into Paper 2 design; do not resubmit Paper 1 for rescue (per `journal_matching_v4.md` §2.5 rule).

---

## Risk Register & Mitigation (updated for eLife RPP)

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| HRS/ELSA/SHARE access delayed > 8 weeks | 40 % | Low-medium | Part 1 succeeds on NHANES + UKBB + Add Health; delayed cohorts → SI |
| Part 2 case count < 50 | 20 % | Medium | H2 falsifier; reframe to "≥ 30"; H3 carries more weight |
| Part 2 phylogenetic signal null (λ < 0.1) | 25 % | Medium | Pre-specified "convergent" reframing; paper still publishable at eLife RPP |
| Part 3 H4b Jaccard ≤ baseline | 25 % | Medium | Pre-specified "within-phylum-only" degradation row in dependency table |
| **Part 4 H6a zero positive-selection signal** | 30 % | **Medium** | H6a reframes to "purifying selection dominant, no lineage-specific sweep"; paper maintains Part 4 on H6f lit summary only |
| External coders return κ < 0.60 | 20 % | Low-medium | Paper reports honestly; emphasises Δ_ST (continuous) over F1-F4 (categorical) in headline |
| eLife desk reject | 5-10 % | Low | Reformat to PLOS Biology (1-week reformat); `journal_matching_v4.md` §3 decision rule |
| eLife "Incomplete / Solid" reviewer assessment | 30-40 % | Low | Still publishes as citable Reviewed Preprint DOI; carry critiques to Paper 2 |
| eLife "Inadequate" reviewer assessment | 5-10 % | Medium-high | Reformat to Open Biology or PLOS Biology after accepting public record |
| Competing paper published during Weeks 1-8 | 5-10 % | High | Monitor bioRxiv weekly; Week 0 priority deposit is defensive anchor |
| Senior coauthor needed for Paper 2 Proc B route | 70 % (Paper 2 horizon) | N/A (Paper 1) | Recruit during Weeks 11-12 once Paper 1 assessment is in hand |

---

## Resource & Agent Orchestration

**Parallel tracks (Weeks 1-6):**
- Track A (Part 2): literature agent → coding → phylogenetic analysis.
- Track B (Part 3): molecular-evolution agent → OrthoFinder → PAML → synteny + InterPro Jaccard.
- Track C (Part 1): biobank agent → per-cohort regression → trans-ancestry MR.
- **Track D (Part 4, new)**: molecular-evolution agent (Track B extended) → branch-site H6a in parallel with H4a; CARSI-PDF-fetcher → H6f lit sweep in parallel with Part 2 coding.

**Critical path:** Track A (Part 2) remains load-bearing per H2 dependency structure.

**Compute resources:** All analyses fit on M5 Pro 24 GB + P1 external per `_meta/compute-ops-guide.md` rules. PAML codeml on 15 genes × 20-30 lineages → ~40 CPU-hours total (Mac OK, n_workers ≤ 2).

**Budget:**
- External coders × 3 × $100 = $300
- eLife APC $0-500 (via HUFLIT waiver route)
- bioRxiv deposit free
- OSF deposit free
- **Total: $300-800**

---

## Checkpoints Log (to be populated during execution)

| Week | Checkpoint | Status | Note |
|---|---|---|---|
| 0 | Design finalisation + Path D deposit | IN PROGRESS | 2026-04-24 |
| 1 | PRISMA search, 150+ candidates; Part 4 H6a PAML setup | — | |
| 2 | 50+ cases coded; CARSI PDF bulk-downloaded for H6f | — | |
| 3 | Part 3 H4a first dN/dS + Part 4 H6a first branch-site | — | |
| 4 | **GATE 1** (includes Part 4 H6a criterion) | — | Continue / re-scope / retreat |
| 5 | Sensitivity analyses + H6f table finalised | — | |
| 6 | Figure drafts v1 (5 figures incl. Part 4) | — | |
| 7 | Manuscript first draft + **GATE 2** | — | |
| 8 | Revision + eLife prep | — | |
| 9 | eLife submission | — | Target: 2026-06-23 |
| 10 | eLife monitoring + Paper 2 scoping | — | |
| 11-12 | Buffer + Paper 2 prep | — | |

---

*Document version 1.2 (2026-04-24). Authored by PI. Supersedes v1.0 (2026-04-20). Key changes: primary venue → eLife RPP; Path F removed; Part 4 (H6a + H6f) added as compressed new component; GATE 1 criterion expanded to include Part 4 H6a signal; risk register restructured around eLife RPP outcomes instead of Proc B desk-reject cascade; submission window moved to Week 8-9.*
