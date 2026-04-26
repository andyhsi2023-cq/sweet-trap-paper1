# Analytical Pipeline — Stage 6

**Date:** 2026-04-20
**Scope:** Methodological choices for Parts 1-3 with explicit justification and alternatives considered.
**Principle:** Every statistical choice is defended against the hostile-review objections on the prior manuscript (HSSC hostile review 2026-04-21), and against the NHB desk-reject diagnostic on the prior manuscript.

---

## 1. Part 2 — Phylogenetic-Signal Analysis

### 1.1 Primary method: Both Blomberg's K and Pagel's λ, reported jointly

**Choice:** Report *both* Blomberg's K (Blomberg, Garland & Ives 2003 *Evolution* 57:717) and Pagel's λ (Pagel 1999 *Nature* 401:877) with 95 % bootstrap CIs. Likelihood-ratio test λ = 0 vs λ_MLE as the formal inference anchor.

**Why both:**
- **K** is a ratio of observed to expected variance under Brownian motion; values > 1 indicate phylogenetic signal *stronger* than expected under BM (e.g., conserved deep traits), values < 1 indicate weaker-than-BM signal, and values ≈ 0 indicate random distribution across the tree.
- **λ** is a scaling parameter in the variance-covariance matrix; λ = 1 recovers full BM, λ = 0 recovers a star phylogeny (no signal), intermediate values indicate the proportion of trait covariance explained by phylogeny.
- They capture *different* notions of "signal" and are known to disagree in informative ways (Münkemüller et al. 2012 *Methods Ecol Evol* 3:743). Reporting both is the methodological-rigor standard in the behavioural-ecology literature we are submitting to.

**Alternatives considered and rejected:**
- **Moran's I on the phylogeny** (Gittleman & Kot 1990): older, less sensitive to tree topology at depth; superseded by K/λ.
- **K* (Ives et al. 2007):** estimates K with measurement error; considered for Part 2 because Δ_ST has per-case CIs. **We use this as a sensitivity analysis** — not as primary because the measurement-error structure across Tier 1/2/3 cases is itself heterogeneous and Ives' K* assumes homoscedastic measurement error.
- **Phylogenetic eigenvector regression (Diniz-Filho 1998):** viable but requires arbitrary eigenvector-selection criteria; leaves room for researcher degrees of freedom.

**Robustness layer:**
- Run K and λ with the tree polytomies resolved randomly 1,000 times (to bound topology uncertainty).
- Run K and λ dropping one phylum at a time (leave-one-phylum-out) to detect single-clade domination.
- Compare K and λ under the full 50+ tree vs. a reduced vertebrate-only tree, to separate "deep" from "recent" phylogenetic structure.

### 1.2 Ancestral-state reconstruction

**Choice:** Stochastic character mapping (SIMMAP; Bollback 2006 *BMC Bioinformatics* 7:88) for binary susceptibility (Sweet Trap present/absent on the candidate-case phylogeny), and continuous-trait ancestral reconstruction under Brownian motion and Ornstein-Uhlenbeck models for Δ_ST magnitude (using `phytools::contMap` in R).

**Why SIMMAP rather than parsimony:** Parsimony reconstructions ignore branch-length information and give over-confident point estimates. SIMMAP samples from the posterior distribution over histories given the data and tree, which is the rigorous way to ask "is there ≥2 independent origins of Sweet Trap susceptibility?"

**Model comparison:** BM vs OU vs Early Burst using AIC (Harmon et al. 2010 *Evolution* 64:2385); if OU is selected we report the selection-strength parameter α and infer whether Sweet Trap susceptibility is evolving toward a fitness optimum (OU) or drifting neutrally (BM).

### 1.3 PGLS for life-history covariates

**Choice:** Phylogenetic Generalized Least Squares (Grafen 1989 *Philos Trans R Soc B*) with λ estimated jointly with regression coefficients. Implementation: `caper::pgls` in R, with degrees of freedom, residual λ, and likelihood reported.

**Why not simple Felsenstein independent-contrasts regression:** PIC requires BM and gives no flexibility in phylogenetic-signal strength; PGLS subsumes PIC and allows λ to vary.

### 1.4 Tree sources and harmonisation

- **TimeTree 5** (Kumar et al. 2022 *Mol Biol Evol* 39): calibrated time-tree, preferred for all analyses requiring branch lengths.
- **Open Tree of Life** (Hinchliff et al. 2015 *PNAS* 112): topology-only tree as sensitivity check.
- **Taxonomic harmonisation:** **GBIF** backbone taxonomy resolves synonyms across source datasets.
- **Missing taxa protocol:** species absent from TimeTree are grafted at the lowest confident clade using `taxize` + manual check; grafted species are tested as sensitivity (drop all grafted species, re-run K/λ).

### 1.5 Response to hostile-reviewer methodological objections

- **Objection on Tier-3 "theoretical prior" inclusion:** primary analysis excludes Tier 3; Tier-3 cases enter only in a pre-registered sensitivity analysis. Publication-bias tests (Egger, trim-and-fill, PET-PEESE) all run on Tier-1/2-only subset as primary.
- **Objection on Egger under-powered at k=20:** with k ≥ 50 and mechanism-stratified subgroups, Egger becomes informative per subgroup.
- **Objection on κ=1.00 implausibility:** discriminant-validity re-coding for Part 2 uses **three external coders blinded to authors' prior coding**, recruited via [explicit strategy below — see §4]. Target κ reported on held-out 30 % of cases.

---

## 2. Part 3 — Molecular Evolution Analysis

### 2.1 Ortholog recovery

**Choice:** `OrthoFinder2` (Emms & Kelly 2019 *Genome Biol* 20:238) as primary, validated against NCBI HomoloGene, Ensembl Compara, and InParanoid.

**Why OrthoFinder rather than reciprocal-best-BLAST:** OrthoFinder resolves many-to-many orthologies and is the community standard; reciprocal-BLAST is known to fail on tandem-duplicated gene families (which includes TAS1R and opioid receptors).

**Target genes:**
- **Dopamine receptors:** DRD1, DRD2, DRD3, DRD4, DRD5 (5 genes)
- **Opioid receptors:** OPRM1, OPRK1, OPRD1, OPRL1 (4 genes)
- **Taste receptors:** TAS1R1, TAS1R2, TAS1R3 (sweet/umami), TAS2R (bitter, as negative-control family given its tandem evolution)
- **Orexin/neuropeptide-Y reward pathway:** HCRTR1, HCRTR2, NPY1R, NPY2R, NPY5R

### 2.2 Selection-pressure estimation (dN/dS)

**Choice:** `PAML codeml` branch-site model M2a vs M1a null test (Yang 2007 *Mol Biol Evol* 24:1586), run on codon alignments from PRANK or MAFFT + Gblocks trimming.

**Why branch-site not simple ω_foreground / ω_background:** The branch-site model explicitly tests for positive selection on a subset of sites in a subset of branches, which is the biologically-relevant question ("was there adaptive divergence at a specific node?"). Simpler ratios conflate purifying and neutral sites.

**Sensitivity layer:**
- Run with codon alignment from both PRANK (best for indel-heavy) and MAFFT-linsi (best for distant homologs); compare ω estimates.
- Drop one taxon at a time; report ω range across leave-one-out.

**Genome-wide baseline:** For each species pair in the reward-receptor analysis, compute dN/dS on a matched random sample of 500 one-to-one orthologs of similar length (±20 %) and similar expression level (log-expression ±1 SD in available RNA-seq atlas). Report reward-receptor ω as Z-score relative to this baseline distribution.

**Why baseline matters:** The claim "reward receptors are conserved" is only meaningful relative to what conservation *typically* looks like in that species pair. Without the baseline the dN/dS numbers are uninterpretable.

### 2.3 Synteny

**Choice:** `MCScanX` (Wang et al. 2012 *Nucleic Acids Res* 40:e49) on Ensembl gene coordinates, with `Genomicus` (Nguyen et al. 2018) as cross-check.

**Deliverable:** Conserved synteny block maps at the DRD1-DRD2 locus and the OPRM1 locus across ≥1 chordate, ≥1 arthropod, and ≥1 lophotrochozoan genome.

### 2.4 Ligand-binding-domain focus

**Choice:** Use InterPro / Pfam coordinates to extract the ligand-binding domain (e.g., GPCR 7TM for dopamine receptors, Class C GPCR Venus-Flytrap for TAS1R). Run primary dN/dS on LBD only, with full-gene dN/dS as secondary.

**Why LBD-only primary:** The biological prediction is that *reward signalling* is conserved. The ligand-binding domain is the mechanistic locus of reward recognition. Full-gene conservation is confounded by GPCR structural scaffolding conservation that is not reward-specific.

---

## 3. Part 1 — Multi-Source Meta-Synthesis

### 3.1 Behavioural stream: pooled β across 6 cohorts

**Choice:** Two-stage individual-participant-data (IPD) meta-analysis *where possible* (Burke, Ensor & Riley 2017 *Stat Med* 36:855); aggregate-data random-effects meta-regression where IPD is not accessible.

**Stage 1 (within-cohort):** Fit a standardized linear model within each cohort:
- Predictor: aspirational-reward-pursuit index (per-cohort operationalisation following pre-registered crosswalk — see §3.4)
- Outcome: fitness-proxy (BMI, HbA1c, telomere, depression, mortality hazard)
- Covariates: age, sex, education, income quintile, cohort-specific confounders.
- Extract β_std and SE.

**Stage 2 (across cohorts):** DerSimonian-Laird random-effects pooling on β_std, with cohort-level moderators (country, birth cohort mean age, survey year).

**Why two-stage IPD-where-possible rather than full IPD:** Full IPD requires harmonizing raw data across NHANES, UKBB, HRS, ELSA, SHARE, Add Health with different access agreements. Two-stage IPD achieves the same inferential validity with feasible data access.

### 3.2 Biomarker stream: dose-response across cohorts

**Choice:** Restricted-cubic-spline regression of biomarker on behaviour decile, fitted per cohort, with pooled spline knots. Plot overlaid curves.

**Rationale:** Dose-response non-linearity is biologically expected (e.g., BMI vs. sugar intake has threshold effects). Linear β hides this.

### 3.3 Causal stream: trans-ancestry MR

**Choice:** Primary inference via **MR-APSS** (Hu et al. 2022 *Nat Commun* 13:7045) which accounts for correlated and uncorrelated horizontal pleiotropy jointly — directly addressing hostile-review Methodological Weakness #2 (pleiotropy bias in Davies et al. 2019).

**Secondary methods:** IVW + MR-Egger + weighted-median + MR-PRESSO + MR-RAPS (as in v3.x) for cross-method concordance.

**Ancestry groups targeted:**
- **EUR:** UK Biobank + FinnGen (existing) + GERA + Estonian Biobank
- **EAS:** BioBank Japan + TWB (Taiwan Biobank)
- **AFR:** Million Veteran Program AFR + AoU AFR + UKBB AFR (smaller)
- **AMR:** AoU AMR
- **SAS:** UKBB SAS + GenomeAsia100k where accessible

**Exposure-outcome chain harmonization:** Same 19 chains as v3.x, but with ancestry-specific GWAS summary statistics used per ancestry. Report per-ancestry MR result + pooled cross-ancestry MR (random-effects meta on log-OR across ancestries).

**Ancestry-heterogeneity test:** Cochran Q across ancestries per chain; I² reported. If Q significantly rejects homogeneity on a chain, we report ancestry-specific results separately and flag the chain as "ancestry-context-dependent".

**Why MR-APSS as primary:** It is the 2022+ state-of-the-art for trans-ancestry MR; addresses the FinnGen-drift objection in the Natural way (MR-APSS explicitly models the GWAS-level horizontal pleiotropy that drives drift). The older IVW/Egger remain as reporting anchors for comparability with prior literature.

### 3.4 Crosswalk across cohorts (aspirational-reward-pursuit index)

**Challenge:** NHANES, UKBB, HRS, ELSA, SHARE, and Add Health use different instruments for reward-related behaviour. A crosswalk is required.

**Strategy:** Pre-register a construct-based operationalization per cohort, documented in Week 2-3 of the 12-week plan:
- **NHANES:** ultra-processed food share (%UPF by NOVA classification) + gambling frequency + digital-screen self-report.
- **UKBB:** risk-tolerance item + alcohol frequency + behavioural touchscreen reward-task performance (where available in sub-cohort).
- **HRS + ELSA + SHARE:** financial-risk-taking item + smoking/drinking + "keeping up with neighbours" status-consumption proxy.
- **Add Health Wave V:** problem-gambling + substance use + debt-financed status consumption.

**Validation of crosswalk:** Within each cohort, compute an internal-consistency α across 3-5 items. Drop any cohort where α < 0.50. Report the crosswalk scheme in full in the Methods and in an OSF-deposited protocol before analysis.

### 3.5 GBD 2021 as external anchor

**Choice:** Independent plausibility check, not inferential input.

Extract GBD 2021 attributable-DALY estimates for the same behaviour-disease pairs represented in the MR chains (e.g., BMI-attributable T2D DALY; alcohol-attributable liver-disease DALY). Compare against back-of-envelope projection from MR OR × exposure prevalence × disease baseline rate. If MR projection is within 3× of GBD, we report "MR-predicted burden consistent with independent population-health estimate". If not, we report the discrepancy and its likely source (e.g., MR captures lifetime effect, GBD captures cross-sectional period effect).

**This explicitly does not claim MR-derived DALYs as a primary number.** It is a cross-validation. The hostile-reviewer welfare-quantification objection (Methodological Weakness #3) is avoided by never claiming welfare quantification as a primary finding.

---

## 4. Blind Coding Protocol for Part 2 (addressing κ=1.00 objection)

**Design:** Three external coders recruited from evolutionary-biology PhD-student pools (via departmental mailing lists at 2-3 institutions + Twitter/Bluesky call-out) with modest honorarium ($100 per coder, $300 total, within the existing project discretion).

**Protocol:**
- Authors code 50+ cases to produce "ground truth" coding A.
- External coders receive 50+ case descriptions (text only, blinded to authors' coding, blinded to each other) and apply the F1-F4 criteria using the pre-registered coding sheet.
- Primary inter-rater agreement: Fleiss' κ across three external coders (target ≥ 0.70).
- Author-vs-external agreement: Cohen's κ per external coder against author coding (target ≥ 0.60 for each).

**Why this fixes the v3.x κ=1.00 objection:** The v3.x κ = 1.00 was with two authors as primary coders. The hostile review correctly flagged this as author-internal. External-coder protocol produces an independent κ estimate with realistic bounds.

**Falsifier:** If Fleiss' κ among external coders < 0.60, the Sweet Trap coding scheme is judged as unreliable and we report that openly. The paper can still go forward by using Δ_ST magnitude (continuous) as the primary variable rather than F1-F4 classification (binary) — which is the direction Part 2's phylogenetic-signal analysis uses anyway.

---

## 5. Spec-Curve Reduction (SI only)

**Choice:** Retain 500-spec curve on *one* NHANES behaviour-biomarker pair (NHANES HbA1c × ultra-processed food) as a methods showcase for Part 1 robustness. Drop the 3,000-spec China-panel curve to a single sentence in SI.

**Rationale:** Spec-curve has become standard in behavioural science (Simonsohn et al. 2020), and including one serves as a methodological credibility anchor. But the 3,000-spec China result is no longer the centrepiece.

---

## 6. Open Software, Pre-Registration, and Reproducibility

- **All code deposited on OSF + GitHub** at Week 0 (pre-analysis) for the analytical-pipeline scaffolding; updated weekly.
- **Seeded random-number generation** throughout (set.seed(20260420) as project-wide seed).
- **Docker/Singularity container** with R 4.4 + PAML + MCScanX + OrthoFinder + phytools + caper + ape + TwoSampleMR + MR-APSS pinned.
- **Pre-registration timestamp verification:** OSF DOI, not author-controlled timestamp. The hostile-reviewer "pre-registration post-data" objection is avoided because no new Part 2/Part 3 data have been extracted yet.

---

## 7. Summary Table — Method Choice vs. Hostile-Review Objection

| Hostile-review objection (v3.4) | v4 mitigation |
|---------------------------------|---------------|
| T2 proof hand-waved at Hessian-channel invariance | T2 dropped entirely. |
| A+D pre-registration data-contingent | New pre-registration is ex ante (no new data yet). |
| FinnGen-only ancestry | Trans-ancestry MR across 5 groups. |
| κ=1.00 author-internal | Three external coders on 50+ cases. |
| Tier-3 "theoretical priors" in meta | Primary analysis excludes Tier 3. |
| Egger under-powered at k=20 | N ≥ 50 restores power; trim-and-fill + PET-PEESE added. |
| Layer C circular predictor | Layer C dropped from main. |
| Cross-level p=0.47 | Cross-level meta dropped; no three-layer test claimed. |
| Welfare quantification claim unsubstantiated | No welfare claim made; GBD is plausibility check only. |
| Pleiotropy bias (Davies 2019) unacknowledged | MR-APSS + MVMR-Egger (Sanderson 2024) primary. |

---

*Document version 1.0. Authored by PI.*
