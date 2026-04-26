# Evidence Architecture v4 — Three-Part Biological Claim

**Date:** 2026-04-20
**Supersedes:** v3.x four-layer architecture (Layer A animal + Layer B 3,000 specs + Layer C ISSP + Layer D MR) which was a human-panel paper with an animal force-multiplier.
**New structure:** Three parts, each answering one biological question; data-sources pooled across domains per part rather than per layer.

---

## 1. Architectural Logic

Each Part answers exactly one question. Each Part draws on multiple data sources pooled into one synthesis. The four Parts together compose a complete evolutionary-biology argument: **the phenomenon exists in humans → it exists broadly across animals → the underlying molecular machinery was convergently built across phyla and conserved within phyla → specific lineages exposed to Sweet-Trap environments carry positive-selection footprints on the reward-receptor machinery**.

| Part | Question | Method family | Key statistic | Fails at… |
|------|----------|---------------|---------------|-----------|
| **Part 1** | Does Sweet Trap exist in humans with measurable behavioural, physiological, and genetic signatures? | Cross-cohort pooled synthesis (behavioural) + trans-ancestry MR (causal) | Pooled β across ≥5 cohorts; OR across ≥3 ancestries | H1 |
| **Part 2** | How broadly across Animalia does Sweet Trap occur, and is its distribution phylogenetically structured? | PRISMA meta + PGLS + Blomberg K + Pagel λ + ancestral-state reconstruction | Pooled Δ_ST (N ≥ 50), λ and K, reconstruction topology | H2, H3, H5 |
| **Part 3** | Is Sweet Trap produced by convergent functional architecture of reward signalling across phyla, with within-phylum conservation of receptor families? | Two-tier molecular scan: within-phylum sequence alignment + branch dN/dS + synteny; cross-phylum InterPro domain architecture + paraphyly test + downstream coupling comparison | Within-phylum LBD dN/dS vs matched baseline; cross-phylum InterPro Jaccard ≥ 0.70 with LBD identity 30–50 % | H4a, H4b |
| **Part 4** (lightweight) | Are specific evolutionary lineages exposed to Sweet-Trap environments marked by lineage-specific positive-selection footprints on reward-receptor genes, and is cross-species genetic manipulation literature directionally consistent with the Δ_ST framework? | PAML branch-site Model A (foreground vs background null) on 15 reward-receptor genes across ecological-shift lineages + literature synthesis table of ≥ 30 published genetic-manipulation experiments | Branch-site LRT p < 0.05 on ≥ 3 of 15 genes across ≥ 4 lineages (H6a); directional-consistency ≥ 70 % across ≥ 30 manipulation experiments (H6f) | H6a, H6f |

---

## 2. Part 1 — Human Sweet Trap (multi-source pooled evidence)

### 2.1 Three evidence streams

| Stream | Target signature | Data sources | Analysis |
|--------|------------------|--------------|----------|
| **1-Behavioural** | F1+F2 profiles in nationally-representative and longitudinal cohorts | **NHANES 1999-2023** (US, dietary + biomarker + mortality-linked); **UK Biobank** behavioural phenotypes (n≈500K, under-used in v3.x); **HRS** (US retirees, financial-decision arm); **ELSA** (UK); **SHARE** (EU multi-country retirees); **Add Health Wave V** (US adolescent→mid-adult tracking) | Pooled random-effects meta-regression of standardized β for aspirational-reward → fitness-outcome linkage, with cohort as random effect and age/sex/SES covariates. |
| **1-Biomarker** | Dose-response behaviour → physiology | NHANES (HbA1c, BMI, CRP, telomere); UKBB (accelerometer + biomarker panel + linked hospital records); **GBD 2021** burden-of-disease anchor (independent validation that the behaviour-disease linkage carries population-level attributable burden) | Behaviour-decile comparison of biomarker trajectories; GBD DALY anchor as effect-size plausibility check (not primary inference) |
| **1-Causal** | Trans-ancestry Mendelian randomization | **UKBB + FinnGen + BBJ (BioBank Japan) + Million Veterans + AoU (All of Us)** — five ancestry groups minimum; the existing 19 FinnGen chains are retained but are a minority of the new Part 1 evidence | Cross-ancestry MR with IVW + MR-Egger + weighted-median + MVMR + Steiger; **heterogeneity test across ancestries** (key directional robustness metric) |

### 2.2 Target output

A single figure (Part 1 summary) combining three panels:
- (a) Forest plot of behavioural β across 6 cohorts (with pooled random-effects diamond).
- (b) Biomarker dose-response curves (NHANES + UKBB overlaid).
- (c) Trans-ancestry MR forest of top 5 exposure-outcome pairs across 5 biobanks.

### 2.3 Relation to v3.x Layer B/C/D

| v3.x component | v4 fate |
|----------------|---------|
| Layer B 3,000 specs (CFPS + CHARLS + CHFS, China) | **Compressed to SI.** Kept as one of six cohorts but not central; the headline is no longer "specification robustness of Chinese panel results". Spec-curve methodology retained only for the NHANES aspirational-eating domain as a methods showcase, reduced to ~500 specs. |
| Layer C ISSP 25-country | **Dropped from main text.** Cross-cultural variation is within-human variation; the reframing prioritizes cross-*species* over cross-*culture*. ISSP results move to SI as a "trans-cultural robustness" note. |
| Layer D FinnGen-only 19 MR chains | **Retained and extended.** FinnGen becomes one of 5 ancestry groups. Chains expanded from 19 (single-ancestry) to 19 × 5 ancestries = up to 95 chains where instruments are available. Headline: trans-ancestry MR is now the causal anchor, not FinnGen-only. |

### 2.4 Why this is stronger than v3.x

- **Ancestry breadth directly disarms hostile-reviewer Objection #7** (FinnGen-only → single European founder population).
- **Multiple cohorts with independent sampling** reduce the "post-hoc case selection" concern the 3,000-spec robustness check was trying to address; six-cohort convergence is a more credible signal than 3,000 specs on one panel.
- **GBD 2021 as external anchor** replaces the v3.x 4.1-34.6 M DALY envelope (which was internal) with an independent population-health benchmark.

---

## 3. Part 2 — Cross-Animal-Taxa Distribution (meta + phylogenetic)

### 3.1 Three evidence streams

| Stream | Target signature | Data sources | Analysis |
|--------|------------------|--------------|----------|
| **2-Meta** | Δ_ST pooled across ≥50 animal systems | Systematic review expansion from 20 to 50+ cases. Searches: PubMed + Web of Science + Scopus + bioRxiv, 1995-2026. Keywords: "ecological trap", "evolutionary trap", "sensory trap", "sensory exploitation", "supernormal stimulus", "reward mismatch", "superstimulus". Secondary harvest: Robertson & Hutto 2006 + Hale & Swearer 2016 review lists + Dryad/Figshare open-data deposits. | PRISMA flow; pre-registered coding sheet (binary F1/F2, Δ_ST tier, quality score). Random-effects DL meta-analysis with subgroup (phylum × mechanism × route). |
| **2-Phylogeny** | Phylogenetic signal in Δ_ST | Species–phylogeny matching via **TimeTree 5** + **Open Tree of Life**; taxonomic harmonisation via **GBIF** | Blomberg's K and Pagel's λ with 95 % bootstrap CI; likelihood-ratio test λ ≠ 0; stochastic character mapping (SIMMAP) for binary susceptibility presence; ancestral-state reconstruction under Mk model (continuous Δ_ST under BM and OU). |
| **2-LifeHistory** | PGLS with life-history covariates | **PanTHERIA** (mammals), **AnAge** (vertebrates), **Arthropod Body Size Database** + individual-paper extraction for invertebrates | PGLS regression of Δ_ST on {generation time, body mass, brood size, niche breadth, sensory specialization dummy}. |

### 3.2 Target output

Two figures:
- **Part 2 Figure A:** 50+ case forest plot with phylogenetic tree alongside (tree-on-forest visualisation, e.g. ggtree + pheatmap style).
- **Part 2 Figure B:** Ancestral-state reconstruction on phylogeny + PGLS coefficient plot.

### 3.3 Relation to v3.x Layer A

| v3.x component | v4 fate |
|----------------|---------|
| Layer A 20-case meta v2 | **Retained as core; extended to 50+.** The existing 20 cases are pre-coded and become the anchor set. |
| Layer A quality-score gradient (0-6) | **Retained.** Used as covariate in sensitivity analyses to address hostile-reviewer objection on Tier-3 "theoretical prior" inclusion (Methodological Weakness #1: run sensitivity without Tier 3). |
| Layer A publication-bias caveat | **Addressed properly.** With N ≥ 50 the Egger test becomes appropriately-powered (Sterne et al. 2011 floor is k ≥ 30); we also add trim-and-fill and PET-PEESE. |

### 3.4 Why phylogenetic-signal analysis is the key methodological innovation

No prior paper in the ecological-trap / evolutionary-trap / reward-mismatch literature has performed a phylogenetic-signal test on susceptibility magnitude. The closest existing work (Hale & Swearer 2016 Biol Rev, Robertson et al. 2013 TREE) stopped at cataloguing cases by taxon without formal phylogenetic inference. This is the **one-figure-paper** distillation: the answer to "is Sweet Trap a universal or a convergent phenomenon?" is quantitatively answerable for the first time.

---

> **Post-hoc status note (2026-04-25, Stage 7 audit revision)**: The pre-registered H3 primary prediction ($P(K > 0.30) \ge 0.92$ from A1–A4 axioms) **failed at the cross-phylum scale**: observed $K = 0.117$ ($p = 0.251$) lies above the falsification threshold ($K < 0.10$) but below the predicted zone. BM-inheritance reading of H3 is disconfirmed on the present 56-species corpus. The convergence interpretation of the cross-phylum null is **post-hoc and hypothesis-generating**, pending independent-dataset re-test with PGLS-adjusted covariates (ALAN exposure, body mass, generation time, publication period) in Paper 2. Within-Arthropoda $K = 1.45$ ($p = 0.007$) confirms predicted structure at sub-clade scale and serves as pipeline-validation evidence. See `05-manuscript/manuscript.md` §3.2 and §4.2 for the honest-disclosure revision, and Deviation log row #5 (revised).

> **H6a status note (2026-04-25)**: The Apis Gr_sweet clade-level positive-selection signal (LRT = 9.92; Bonferroni-prereg $p = 0.049$; $\omega = 36.2$ on $n = 4$) is reclassified from SUPPORTED to **TENTATIVELY SUPPORTED** pending replication on an expanded *Apis*–*Bombus*–*Vespa* $n \ge 10$ taxon set with BUSTED / aBSREL / RELAX triangulation (Paper 2). See Deviation log row #6.

## 4. Part 3 — Convergent Functional Architecture of Reward Signalling, with Within-Phylum Conservation (molecular)

**Two-tier structure.** Part 3 makes two logically distinct claims, tested with different analyses:

- **Tier H4a (within-phylum conservation):** Within Chordata, and separately within Arthropoda, the core reward-receptor gene families are under strong purifying selection at their ligand-binding domains. This is a *positive control* that the pipeline works, and a *necessary condition* for the phylogenetic-signal logic of H3 (for related species to share susceptibility, their receptor machinery has to be conserved enough to matter).
- **Tier H4b (cross-phylum convergent functional architecture):** Across Bilaterian phyla, reward signalling is implemented by **non-orthologous but architecturally equivalent** receptor systems. The Chordata sweet-taste receptors (TAS1R2/TAS1R3) and the Arthropoda gustatory receptors (Gr5a/Gr64 family) are paraphyletic — they are not descendants of a single common Bilaterian ancestor receptor — yet both implement sweet-sensing with a Venus flytrap ligand-binding module embedded in a 7TM GPCR architecture coupled to cAMP/PKA signalling. Repeated independent invention of the same architecture is the evolutionary signature predicted by "Sweet Trap is shaped by evolution."

This reframing **resolves a factual tension** in v4.0 of the architecture document: the v4.0 Part 3 predicted deep cross-phylum sequence conservation (dN/dS < 0.15, pairwise identity > 50 % across ≥6 phyla). The underlying data — insect Grs are not orthologs of vertebrate TAS1Rs; vertebrate–invertebrate dopamine receptor pairwise identity is 40–50 % not > 70 % — is *inconsistent* with the deep-conservation prediction but *consistent* with (indeed, *supports*) the convergence prediction. Convergence is the stronger evolutionary claim: a conserved trait can emerge from a single ancient origin plus drift; a convergent trait requires repeated selection pressure. Our data lands in the convergence regime.

### 4.1 Evidence streams (two tiers × three streams)

#### Tier H4a — Within-phylum conservation (positive control)

| Stream | Target signature | Data sources | Analysis |
|--------|------------------|--------------|----------|
| **3a-Orthology-within** | Reward-receptor orthologs recoverable within each phylum at high coverage | Ensembl (all vertebrate genomes) + Ensembl Metazoa (Drosophila 12-genomes + Apis + Tribolium + Aedes) + OrthoDB | For Chordata: D1-D5, OPRM1, TAS1R1/2/3, OX1R/OX2R ortholog recovery across vertebrate classes. For Arthropoda: DopR1/DopR2/DopEcR, Gr5a/Gr64-family, opioid-like peptide receptors across major insect orders. Pairwise LBD amino-acid identity within phylum. |
| **3a-Selection-within** | Within-phylum purifying selection at LBD | UniProt sequences aligned with MAFFT; **PAML codeml** branch-model dN/dS with LBD mask from **InterPro** (IPR000276 for class-A GPCR, IPR000073 for TAS1R Venus flytrap) | Within-Chordata and within-Arthropoda branch-model dN/dS; comparison to matched-gene genome-wide dN/dS distribution (Wilcoxon one-sided). Expected: reward-receptor LBD dN/dS significantly below genome-wide median within each phylum. |
| **3a-Synteny-within** | Micro-synteny retention within each phylum | Ensembl + **Genomicus** | Dopamine-receptor cluster micro-synteny across vertebrate classes (Genomicus blocks, 10-gene windows). Gr-family clustered loci micro-synteny across Drosophilidae. |

#### Tier H4b — Cross-phylum convergent architecture (the novelty claim)

| Stream | Target signature | Data sources | Analysis |
|--------|------------------|--------------|----------|
| **3b-Paraphyly** | Receptor families are **not** descended from a single Bilaterian ancestor gene | Same genome sources as H4a + **OrthoFinder** tree inference | Maximum-likelihood species-tree reconciliation of receptor-family gene trees. **Expected outcome:** vertebrate TAS1Rs and insect Grs form reciprocally monophyletic clades, indicating independent origin. Similarly for Ap-DA1 / Lym-DA1 (Mollusca) vs vertebrate D-receptors. |
| **3b-Architecture** | Shared InterPro domain architecture across non-orthologous receptor families | **InterPro** (IPR000073 Venus flytrap; IPR000276 GPCR class-A; plus G-protein interaction motifs IPR000832/IPR003051) + **UniProt** | Per-receptor InterPro domain profile; Jaccard similarity across receptor families in different phyla. Matched random-ortholog baseline (sampled from non-reward genes of equivalent expression / length) provides null Jaccard distribution. **Expected:** reward-receptor cross-phylum Jaccard ≥ 0.70 vs random baseline ≤ 0.30. |
| **3b-Downstream-coupling** | Common downstream G-protein / cAMP-PKA signal-transduction logic across phyla | **STRING** functional-interaction database + **Reactome** pathway annotations + literature-curated reward-circuit maps (Kandel 2000 *Aplysia*; Neckameyer 1996 *Drosophila*; Wightman & Robinson 2002 vertebrate NAc) | Pathway-level conservation score: does Chordata DRD1→cAMP→PKA→CREB pathway have architecturally-equivalent DopR1→cAMP→PKA→CREB counterpart in Drosophila? Binary presence/absence across ≥4 phyla for 5 core signalling modules; Fisher exact test against random-pathway baseline. |

### 4.2 Target outputs

Part 3 delivers two linked figures:

- **Figure 3A — Within-phylum conservation panel (H4a positive control):** Per-phylum LBD dN/dS boxplots for reward-receptor family members vs matched-gene baseline, with Wilcoxon p-values. Expected: reward-receptor LBD dN/dS distribution left-shifted of baseline within Chordata and within Arthropoda.
- **Figure 3B — Cross-phylum convergence panel (H4b novelty figure):** Three-panel figure: (i) gene-family ML trees showing paraphyly of sweet/dopamine receptor families across Chordata/Arthropoda/Mollusca/Cnidaria, (ii) InterPro domain architecture grid (receptor × phylum × domain presence) with Jaccard similarity heatmap, (iii) downstream signalling pathway schematic with module presence/absence matrix across ≥4 phyla.

Optional third figure (Figure 3C, possibly SI): Within-phylum synteny blocks for the dopamine-receptor cluster across vertebrate classes.

### 4.3 Relation to v3.x and to v4.0 prior framing

Part 3 is **new content** relative to v3.x. The 19 MR chains informed molecular mechanism at the allele level (e.g. FTO, ADH1B) within humans but did not touch cross-phylum molecular evolution. The existing MR results inform Part 1 (human causal) but do not substitute for Part 3.

Relative to **v4.0** of this document (the Stage 6 reframing's first draft), the present Part 3 reorganises the claim structure without discarding analyses:

| v4.0 Stream | v4.0 prediction | Disposition in current v4.1 | New interpretation |
|---|---|---|---|
| Orthology across ≥6 phyla with LBD identity > 50 % | Deep conservation | **REPURPOSED as H4b Stream 3b-Paraphyly** | Identity 30–50 % *between* phyla is the expected signature of convergence, not a problem |
| dN/dS < 0.15 on ≥80 % internal branches | Cross-phylum purifying selection | **SPLIT:** within-phylum kept (3a-Selection-within); cross-phylum dropped | Cross-phylum dN/dS is not meaningful when receptor pairs are non-orthologous |
| Synteny across Chordata + Arthropoda | Gene-cluster conservation | **DEMOTED:** within-phylum synteny only (3a-Synteny-within) | Cross-phylum synteny is unreliable signal when gene families are paraphyletic |
| TAS1R Cambrian origin + carnivore loss | Deep-origin narrative | **REPLACED by architectural convergence narrative** | TAS1R (vertebrate) and Gr5a/Gr64 (insect) are independent solutions to the same sweet-detection problem; carnivore loss is an H4a within-phylum event |

### 4.4 Feasibility — 2-3 weeks with open data, unchanged compute envelope

All data sources (Ensembl, Ensembl Metazoa, OrthoDB, OrthoFinder, UniProt, InterPro, STRING, Reactome, Genomicus) are public APIs or downloadable flat files. The `ape`, `phytools`, `phylotools`, `seqinr`, `InterProScan`, and `tidysq` packages (plus PAML codeml + OrthoFinder v2.5) handle all analyses. Expected compute:

- H4a Tier: within-Chordata + within-Arthropoda alignment + dN/dS: 2 days per phylum × 2 phyla = 4 days (n_workers ≤ 2 per CLAUDE.md compute rules).
- H4b Tier: OrthoFinder gene-family tree inference: 1 day. InterPro Jaccard computation: 0.5 days. STRING/Reactome pathway extraction: 1 day. Downstream coupling literature curation: 1.5 days.
- Figure assembly: 1-2 days.

Total: 9-11 working days, conservative envelope 2-3 weeks. Matches the original v4.0 estimate; the two-tier reorganisation does not increase compute.

### 4.5 Theoretical positioning within the comparative-convergence literature (Path E3 addition, 2026-04-23 evening)

The convergence-vs-conservation distinction underlying §4 is not a new theoretical move; it is a well-established framework in comparative molecular evolution. The *contribution of this paper is not to invent the framework* but to apply it as a diagnostic test to reward-fitness decoupling susceptibility — a phenomenon previously analysed only via non-quantitative synthesis (Robertson & Chalfoun 2016; Hale & Swearer 2016; Ryan & Cummings 2013). We explicitly locate Part 3's claim within three theoretical reference frames:

**(i) Stern 2013 — Genetic hotspots of phenotypic variation (*Nat Rev Genet* 14:751-764).** Stern's framework posits that convergent phenotypic evolution often traces to parallel genetic changes at the *same* loci across lineages, because mutations at those loci minimise pleiotropy while maximising adaptation (a pleiotropy–adaptation attractor). Our Part 3 claim is a **functional-architecture generalisation of Stern 2013**: reward signalling does *not* converge at the single-locus level (H4b Stream 3b-Paraphyly confirms vertebrate TAS1Rs and insect Grs are *not* the same gene), but *does* converge at the **domain-architecture level** (Venus flytrap module + GPCR class-A topology + cAMP/PKA coupling). This generalises Stern's hotspot framework from "same locus" to "same functional building blocks", and situates Sweet Trap susceptibility within the broader class of functionally-convergent traits without claiming locus-level convergence — a cleanly distinguishable claim from Stern 2013 in the logical space of convergent-evolution hypotheses.

**(ii) McCune & Schimenti 2012 — Mechanism-based distinction between convergence and parallelism (*Curr Genomics* 13:74-86).** McCune & Schimenti formalised the widely-cited definition of **convergence** = similarity *from different developmental genetic mechanisms*; **parallelism** = similarity *from the same developmental genetic mechanisms*. Under this definition: vertebrate TAS1R + insect Gr are a genuine **convergence** case (different gene families with different developmental regulatory origins), not a parallelism case. Our Part 3 therefore makes a *convergence* claim in McCune & Schimenti's precise terminology — and this is the analytically-strong claim, because convergence requires the same selective pressure to have repeatedly found the same functional architecture from different starting points, whereas parallelism could be explained by shared ancestral developmental constraint without independent selection. For Sweet Trap's thesis ("shaped by evolution"), the convergence reading is the load-bearing empirical claim.

**(iii) Erwin & Davidson 2009 — Gene regulatory network evolution and deep homology (*Nat Rev Genet* 10:141-148; *Curr Top Dev Biol* 86).** Erwin & Davidson articulated the framework of **gene regulatory networks** (GRNs) as the unit of conservation and homology in evolution — arguing that cell-type and trait homology persists via conserved GRN "kernels" even when individual regulatory links rewire. Our Part 3 H4a within-phylum conservation tier is compatible with the GRN-kernel framework for receptor signalling within Chordata and within Arthropoda, but our H4b cross-phylum convergence claim is a **stronger deviation**: we argue that across phyla the signalling *architecture* converges without a single conserved GRN kernel. This is a testable empirical divergence from the Erwin-Davidson predictions and is partly the reason Part 3 is novel rather than derivative — we specifically test whether the reward-signalling "kernel" is deeply conserved (the Erwin-Davidson prediction) or whether it is architecturally convergent from multiple independent origins (our prediction). The reward-signalling domain is a particularly good test case for the GRN-kernel vs architectural-convergence contrast because reward-system evolution is late-Bilaterian (post-body-plan) and therefore falls in the GRN-flexibility rather than GRN-kernel regime.

**Summary of theoretical positioning.** Part 3 is best understood as an *application* of the comparative-convergence framework (Stern 2013; McCune & Schimenti 2012) and an *empirical test* of a contrast with the GRN-kernel framework (Erwin & Davidson 2009), operationalised through the domain-architecture Jaccard test (Stream 3b-Architecture) and the pathway-module presence test (Stream 3b-Downstream-coupling). Our contribution is not the *distinction* between convergence and conservation — that is 30+ years old — but the *specific diagnostic application* of the convergence framework to reward-fitness decoupling susceptibility across ≥4 phyla, and the testing of whether reward signalling has a conserved GRN kernel (supporting Erwin & Davidson predictions in-phylum, departing cross-phylum).

Citations: Stern 2013 *Nat Rev Genet* 14:751-764; McCune & Schimenti 2012 *Curr Genomics* 13(1):74-84; Erwin & Davidson 2009 *Nat Rev Genet* 10:141-148.

---

## 5. Part 4 — Genetic Causality (lightweight, Paper 1 scope)

**Scope contract.** Part 4 is the causal-genetic complement to Part 3's descriptive molecular-architecture scan. Paper 1 executes **two streams** of Part 4 — H6a (positive-selection branch-site scan) and H6f (cross-species genetic-manipulation literature summary) — with a total 2-3 working week budget. Four additional gene-level hypotheses (H6b GxE / H6c cross-species parallel positive selection / H6d PRS discriminant validity / H6e recent selection scans) are **announced but not tested in Paper 1**; they are deposited on OSF as Paper 2 roadmap at Week 0 pre-registration to establish conceptual priority on the full gene-level agenda without overpromising in Paper 1.

This scope contract is the result of Andy's 2026-04-24 strategic decision to downgrade Paper 1's target venue (Proc R Soc B → eLife Reviewed Preprint) and compress Part 4 from the full six-sub-hypothesis programme to the lightweight two-stream version. See `journal_matching_v4.md` v1.2 §1.1 for the EV calculation driving the decision.

### 5.1 Two evidence streams (Paper 1)

| Stream | Target signature | Data sources | Analysis |
|--------|------------------|--------------|----------|
| **4a-BranchSite** (H6a) | Lineage-specific positive selection on reward-receptor LBD on ecological-shift foreground lineages | Ensembl + Ensembl Metazoa + OrthoDB (aligned with H4a data pull) + **PAML codeml branch-site Model A** | For 15 target genes (DRD1-5, OPRM1/K1/D1/L1, TAS1R1-3, HCRTR1-2, NPY1/2/5R), run branch-site Model A with foreground = ecological-shift lineages {hummingbird (Baldwin 2014 positive control); primate sugar-specialists; Apidae nectarivore; cetacean sensory-specialist; (stretch) giant panda umami loss via CNGBdb}. Background = matched null. LRT on ω foreground > 1 and p < 0.05 Bonferroni-corrected. |
| **4b-LiteratureSynthesis** (H6f) | Published genetic-manipulation experiments in non-human metazoan organisms show directional consistency with Δ_ST logic | PubMed + CARSI-mediated full-text access (Nature / ScienceDirect / Cell Press / Wiley / Springer / EMBO Press / Rockefeller UP) 2000-2026 | Compile ~30-50 published experiments that (i) manipulate a reward-receptor gene (DopR family / TAS1R family / opioid / orexin / NPY-receptor homologs), (ii) in a non-human metazoan organism (Drosophila, C. elegans, Apis, rodents), (iii) measure a phenotype coded against F1+F2 or Δ_ST. Code each experiment for organism, gene, manipulation type, behaviour, direction of effect, sample size, DOI. Summary table + directional-consistency fraction. |

### 5.2 Target outputs

Part 4 delivers one main figure plus one summary table:

- **Figure 4 — Lineage-specific positive selection map (H6a).** Phylogeny of target lineages (≥ 4 ecological-shift lineages + ≥ 2 control lineages) with branch-site Model A LRT p-values rendered per-lineage-per-gene cell. Hummingbird TAS1R1 positive control highlighted as pipeline-validation reference.
- **Table 4 — Cross-species genetic-manipulation summary (H6f).** ≥ 30 rows, each an experiment; columns = organism / gene / manipulation / phenotype / direction / N / DOI / F1-F2 coding. Directional-consistency fraction reported with binomial CI.

### 5.3 Relation to v3.x and to Parts 1-3

Part 4 is **new content** relative to v3.x (v3.x treated genetic-level evidence exclusively through the 19-MR-chain FinnGen pipeline at the human allele level, without cross-species positive selection or experimental-manipulation literature).

Relative to Parts 1-3 of V4:
- Part 4 is the **causal** counterpart to Part 3's **descriptive** molecular analysis. Part 3 asks "what does the receptor look like?"; Part 4 asks "has selection been acting on the receptor in lineages where Sweet Trap environments emerged?"
- Part 4's H6f summary table provides a **cross-phylum evidence bridge** that does not require new experiments by the authors; it leverages the published experimental literature, which is exactly the kind of synthesis the eLife RPP reviewer community expects.
- Part 1's 19 MR chains remain in Part 1 (human causal stream), not moved to Part 4. Part 4 is cross-species, not human-allele.

### 5.4 Feasibility — 2-3 working weeks with open data + CARSI-accelerated literature access

- **H6a compute**: PAML codeml branch-site Model A + null on 15 genes × ~6 foreground lineages × ~2 control lineages = 15 × 8 × 2 = 240 codeml runs. Per-run wall-time on M5 Pro ~0.5-1 hour → ~150-200 CPU-hours total (n_workers ≤ 2 per `_meta/compute-ops-guide.md` rules). Effective calendar time: **8-12 days**.
- **H6f compile**: Literature search (PubMed + key journals) → screening → full-text extraction → coding → table compilation. Calendar time: **4-6 days**. CARSI grants zero-friction PDF access to ~140 of ~150 target papers.
- **Total Part 4 Paper-1 budget**: **12-18 days**, comfortably within Weeks 1-5 of the 12-week plan.

### 5.5 Paper 2 / Paper 3 roadmap (announced, not executed)

The following gene-level evidence types are **explicitly announced in Paper 1's Discussion** as future work, to establish priority:

| Horizon | Sub-hypothesis | Scope | Estimated timeline |
|---|---|---|---|
| Paper 2 (6-12 months) | H6b GxE interaction | UKB + FinnGen + AoU reward-receptor allele × environment interaction for 5 human Sweet Trap domains | 3-4 months execution |
| Paper 2 | H6c cross-species parallel positive selection | H6a extended to 3-5 CNGBdb Chinese-native species + other independent ecological-shift lineages | 2 months execution |
| Paper 2 | H6d PRS discriminant validity | Per-domain PRS on UKB/FinnGen/BBJ/MVP/AoU with trans-ancestry replication | 2-3 months execution |
| Paper 2 | H6e recent selection scans | AADR v54 + 1000 Genomes selection-scan on reward-receptor loci in past 10 kyr of human evolution | 1-2 months execution |
| Paper 3 (Layer E, 12+ months) | Receptor-knockdown behavioural rescue experiments | Nematostella / Aplysia / bumblebee 3-site F2 operational + knockdown phenotype rescue | 6-12 months execution with wet-lab capacity |

Paper 1 does **not** claim any of H6b-H6e or Layer E evidence; it claims Paper 1 as the construct + comparative + architecture + lineage-selection + literature-synthesis package, with the causal-manipulation and cross-ancestry GxE programme explicitly reserved for follow-up work.

---

## 6. Component-by-Component Disposition of v3.x Assets

Mapping legend: **KEEP** = move to new part unchanged; **ADAPT** = modify and re-purpose; **SHRINK** = retain in SI only; **DROP** = remove from project.

| v3.x asset | Location in v3.x | Disposition | v4 Part |
|-----------|------------------|-------------|---------|
| F1-F4 conditions + A1-A4 axioms | main §M1.1, §M1.2 | **KEEP** (conceptual spine) | Intro + Methods |
| Δ_ST = U_perc − E[U_fit] formalism | §M1.1 | **KEEP** | Intro + Methods |
| T1 stability theorem | §M1.3 | **KEEP** | Methods (supports pooled-meta interpretation) |
| T2 intervention-asymmetry | §M1.3 | **DROP** | — (was policy corollary) |
| T3 cross-species universality | §M1.3 | **ADAPT** (re-stated as empirical prediction for Part 2) | Methods + Results |
| T4 engineered escalation | §11.7 + §M1.3 | **DROP** | — |
| 20-case Layer A meta | 00-design/pde/layer_A_animal_meta_v2.md | **KEEP**, extend to 50+ | Part 2 |
| 19 MR chains (FinnGen) | 00-design/pde/layer_D_MR_findings_v2.md | **ADAPT** to 1 ancestry among ≥5 | Part 1 (causal stream) + Part 3 (within-human allele-level conservation, supports H4a Chordata tier) |
| 3,000 specs (CFPS China) | spec_curve_findings.md | **SHRINK** to SI + 500-spec NHANES replication | SI |
| ISSP 25-country | layer_C_ISSP_deep_findings.md | **SHRINK** to SI | SI |
| Cross-level A+B+D meta + β=1.58 headline | cross_level_meta_findings.md | **DROP** (this was the Cover-Letter self-damage) | — |
| P3 β=-0.73 peak-and-retreat | layer_C_ISSP_deep_findings.md | **DROP** (Layer C is out of main) | — |
| Discriminant-validity 18-case κ=1.00 | discriminant_validity_v2.md | **ADAPT**: re-apply to expanded 50+ case Part 2 set using blind coders other than authors (addresses hostile Objection #8) | Part 2 Methods |
| Mortality DALY anchor 34.6 M | mortality_anchor.md | **ADAPT** to GBD 2021 external anchor for Part 1 effect plausibility | Part 1 |
| Cultural G^c | cultural_Gc_calibration.md | **DROP** (cross-cultural framing out) | — |
| §11 Engineered Deception | 05-manuscript/archived-v3.4 | **DROP** | — |
| HSSC policy paragraphs | archived-v3.4/main_v3.4_hssc_draft.md | **DROP** | — |

---

## 7. Predicted Key Statistics (for pre-registration)

These are the *numbers the paper will report*. Pre-registering them forces honest reporting:

| Part | Statistic | Predicted magnitude (directional) | Null-retention criterion |
|------|-----------|-----------------------------------|--------------------------|
| 1-Behavioural | Pooled β (aspirational reward → fitness proxy) across 6 cohorts | β ≥ 0.10 in predicted direction, 95 % CI excludes 0 | 95 % CI crosses 0 |
| 1-Biomarker | NHANES + UKBB biomarker dose-response slope (top-vs-bottom decile of reward exposure) | ≥ 0.3 SD separation on HbA1c, ≥ 0.4 SD on BMI | < 0.1 SD separation |
| 1-Causal | Trans-ancestry MR OR direction | ≥ 3 of 5 exposure-outcome pairs with same-direction OR in ≥ 3 of 5 ancestries | ≤ 2 pairs concordant |
| 2-Meta | Pooled Δ_ST on N ≥ 50 | +0.40 to +0.70 | CI crosses 0 |
| 2-Phylogeny | Blomberg's K | 0.3 ≤ K ≤ 0.8 | K < 0.1 |
| 2-Phylogeny | Pagel's λ (likelihood ratio p) | p < 0.05 | p > 0.20 |
| 2-LifeHistory | PGLS β (generation time → Δ_ST) | positive, p < 0.10 | p > 0.30 |
| 3a-Orthology-within (Chordata) | Fraction of sampled vertebrate genomes with recoverable D1-like + D2-like + OPRM1 orthologs | ≥ 95 % | < 80 % |
| 3a-Orthology-within (Arthropoda) | Fraction of sampled insect genomes with recoverable DopR1/DopR2/DopEcR orthologs | ≥ 90 % | < 70 % |
| 3a-Selection-within (Chordata) | Within-Chordata LBD dN/dS for dopamine + opioid receptors vs matched-gene genome-wide dN/dS (Wilcoxon one-sided) | p < 0.01, receptor median < 0.15 | p > 0.10 |
| 3a-Selection-within (Arthropoda) | Within-Arthropoda LBD dN/dS for dopamine receptors vs matched-gene genome-wide dN/dS (Wilcoxon one-sided) | p < 0.01, receptor median < 0.15 | p > 0.10 |
| 3a-Synteny-within | Dopamine-receptor micro-synteny retention across vertebrate classes (Genomicus 10-gene windows) | ≥ 60 % of vertebrate pairs retain ≥ 1 block | < 30 % retention |
| 3b-Paraphyly | Reciprocal monophyly of vertebrate TAS1Rs vs insect Grs in OrthoFinder ML tree (UF-bootstrap support) | ≥ 95 % UFBoot on the separating node | node not supported |
| 3b-Paraphyly (backup) | Reciprocal monophyly of vertebrate D-receptors vs arthropod Dop-receptors | ≥ 95 % UFBoot on the separating node | node not supported |
| 3b-Architecture-Jaccard | Cross-phylum InterPro domain-composition Jaccard similarity for sweet/dopamine receptor families vs matched random-ortholog baseline | reward Jaccard ≥ 0.70; baseline ≤ 0.30; Mann-Whitney p < 0.001 | reward Jaccard ≤ 0.50 or baseline ≥ 0.50 |
| 3b-Architecture-LBD-identity | Cross-phylum pairwise LBD amino-acid identity for sweet/dopamine receptor families (Chordata × Arthropoda × Mollusca × Cnidaria) | 30 – 50 % (consistent with convergence, not deep conservation) | > 70 % (would re-invoke deep-conservation framing) |
| 3b-Downstream-coupling | Presence of DA→cAMP→PKA→CREB core module across ≥ 4 phyla (STRING + Reactome + literature) | 5 / 5 core modules present in ≥ 4 phyla | ≤ 2 / 5 modules shared |
| 4a-BranchSite-Control (H6a positive control) | Hummingbird TAS1R1 foreground branch-site Model A LRT (replicating Baldwin et al. 2014) | ω > 1, LRT p < 0.01 | p > 0.10 (pipeline validation failure) |
| 4a-BranchSite-Lineage (H6a main) | Reward-receptor genes showing LRT p < 0.05 on ≥ 1 ecological-shift foreground lineage (of 15 genes × 4 lineages = 60 tests) | ≥ 3 of 15 genes significant across ≥ 4 lineages; ≥ 2 pass Bonferroni α = 0.0033 | ≤ 1 gene-lineage pair significant |
| 4a-BranchSite-SiteModel | M2a vs M1a LRT at positive-selection sites within LBD (InterPro IPR000073 / IPR000276 masked) | Site-class ω > 1 posterior > 0.95 at ≥ 5 LBD codons on ≥ 1 gene-lineage pair | Site-class ω > 1 unsupported anywhere |
| 4b-Lit-DirectionalConsistency (H6f) | Directional consistency across coded genetic-manipulation experiments | ≥ 70 % concordance with Δ_ST direction across ≥ 30 experiments; binomial 95 % CI lower bound ≥ 0.60 | < 50 % concordance |
| 4b-Lit-PhylumCoverage (H6f) | Phyla represented in the summary table | ≥ 3 phyla (Chordata + Arthropoda + Nematoda minimum) | ≤ 2 phyla |

Predicted values come from prior literature where available (e.g. Pagel's λ > 0 is the norm for behavioural ecology traits — Blomberg et al. 2003; dopamine-receptor within-vertebrate conservation — Yamamoto & Vernier 2011; sweet-receptor paraphyly vertebrate-insect — Robertson et al. 2003; Chao et al. 2020; hummingbird TAS1R1 positive selection — Baldwin et al. 2014; panda T1R1 pseudogenisation — Zhao et al. 2010; Drosophila DopR manipulation phenotypes — Kaun et al. 2011; mouse Drd2 phenotypes — Johnson & Kenny 2010) and from the 20-case v2 result extrapolation otherwise. The cross-phylum LBD identity range 30–50 % is the direct prediction of convergence and is consistent with the published vertebrate-insect dopamine-receptor identity window (Feijó et al. 2019 ~40–50 %; Yamamoto & Vernier 2011 45–52 %). The H6a directional predictions are calibrated conservatively: the Baldwin et al. 2014 positive control is the one result we require; all other lineage signals are **exploratory** predictions with null expectation of ~30 % detection rate at p < 0.05 Bonferroni-corrected.

---

## 8. One-Figure-Paper Test

If the paper were one figure only, that figure would be: **the phylogeny of Animalia with Δ_ST values rendered on the tips, convergent-but-within-phylum-conserved reward-receptor architecture rendered as a sidebar (vertebrate TAS1R / insect Gr / molluscan Ap-DA / cnidarian Nv-DA columns showing shared InterPro domain composition despite non-orthology), the human Sweet Trap signal anchored at the Homo branch, and lineage-specific positive-selection footprints marked as stars at ecological-shift branches (hummingbird TAS1R1, primate sugar-specialist DRD2, nectarivore insect DopR, cetacean OPRM1, etc.).**

This figure is Part 2 Figure A + Part 3 Figure 3B + Part 4 Figure 4 combined. It makes the four-part claim visible at a glance — behavioural universality, phylogenetic structure, convergent molecular architecture, and lineage-specific positive selection — and visually encodes the evolutionary logic: the same reward-decoupling susceptibility appears across taxa because the same functional architecture was independently invented, preserved within each lineage, and *actively shaped by selection* in specific lineages where Sweet Trap environments emerged.

---

*Document version 1.2 (2026-04-24). Authored by PI. Supersedes v1.1 (2026-04-23) and v4.0 (2026-04-20). Key revisions in v1.2: (a) §1 architectural table extended from three to four Parts to add **Part 4 Genetic Causality (lightweight)** covering H6a branch-site positive selection and H6f cross-species genetic-manipulation literature summary; (b) new §5 Part 4 written; (c) §7 predictions table extended with 5 new rows for Part 4 statistics; (d) §8 one-figure-paper test updated to include lineage-specific positive-selection stars. The **full six-sub-hypothesis gene-level programme (H6b-H6e + Layer E)** remains defined in `research_question_and_hypotheses.md` §3 but is **explicitly reserved for Paper 2 / Paper 3 horizon**, not executed in Paper 1, per Andy's 2026-04-24 strategic decision to downgrade Paper 1 target venue to eLife Reviewed Preprint and compress Part 4 to the 2-3-week lightweight version.*
