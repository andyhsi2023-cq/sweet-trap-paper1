# Research Question and Hypotheses — Stage 6 Evolutionary Reframing

**Date:** 2026-04-20
**Project:** sweet-trap-multidomain
**Stage:** 6 (root reframing after NHB desk reject 2026-04-20 + HSSC hostile review 2026-04-21)
**Supersedes:** HSSC policy-framing path (v3.4, archived)

---

## 1. One-Sentence Thesis

**Sweet Trap — the decoupling of proximate reward from fitness consequence under voluntary endorsement — is a biologically general phenomenon produced by convergent evolution onto functionally-equivalent reward architectures across phyla, with deep within-phylum conservation of the underlying receptor families, manifesting in humans, in other animals, and in the molecular record of reward-system evolution.**

This is a biology statement, not a policy statement. The target audience is evolutionary biologists, behavioural ecologists, and comparative neuroscientists. Policy/humanities implications are out-of-scope for this paper; they become Paper 2.

---

## 2. Why This Reframing Is Structurally Stronger

The NHB desk reject and the HSSC hostile review converged on the same diagnosis: the prior framing tried to simultaneously (a) be a human-behavioural-science paper, (b) carry a cross-species evidence layer as "force multiplier", and (c) make policy claims. That is three triage categories for one editor. Every triage path had a fatal signal mismatch.

The evolutionary reframing solves this by making the cross-species evidence the **headline**, not a supplement. The paper now has one triage category — evolutionary biology / behavioural ecology — and within that category the three-part architecture (humans as one clade among many; 50+ animal cases; cross-phylum molecular convergence with within-phylum conservation) is a coherent comparative-biology argument of the sort that *Proceedings B*, *Nat Ecol Evol*, and *Current Biology* regularly publish.

Secondary structural benefits:

1. **Umbrella-construct anxiety dissolves.** Evolutionary biology journals *expect* broad constructs validated across taxa (e.g. "evolutionary trap", "life-history theory", "parent-offspring conflict"). NHB/HSSC do not.
2. **Author-institution plausibility improves.** An evolutionary-biology paper from a biomedical affiliation is normal; a cross-disciplinary policy paper from a Mammary Gland department is not.
3. **Intervention-asymmetry theorem (T2) can be dropped.** T2 was the single most-attacked component in the hostile review (Hessian-channel-invariance step; dose-matching); it was a policy-oriented corollary that the biology framing does not need.
4. **Pre-registration apologetics can be demoted.** An evolutionary-biology paper carrying a 20-case meta + phylogenetic-signal test + cross-phylum convergence / within-phylum conservation scan does not require the garden-of-forking-paths defence a 3,000-spec human-panel paper requires.

---

## 3. Five Testable Hypotheses

Each hypothesis is stated with a predicted empirical signature and a pre-specified falsification criterion. The falsification criteria are *hard*: if the stated empirical pattern does not appear, the hypothesis is rejected and the paper's claim is weakened in a specified way.

### H1 — Human Sweet Trap exists and is behaviourally, physiologically, and genetically measurable

**Claim:** In contemporary human populations, the Sweet Trap signature (F1 reward-fitness decoupling under F2 voluntary endorsement) is detectable simultaneously in (a) self-reported behaviour, (b) physiological/biomarker outcomes, and (c) genetically-instrumented causal chains.

**Predicted signatures:**
- **(a) Behavioural:** In NHANES 1999-2023, UK Biobank behavioural phenotypes, and Add Health Wave V, aspirational-reward-pursuit indices (ultra-processed-food intake, problem-gambling, short-sleep-for-late-content, debt-financed status consumption) correlate *positively* with self-reported reward endorsement (F2-consistent) and *negatively* with fitness proxies (BMI, HbA1c, telomere length, depression, mortality).
- **(b) Biomarker:** Per-unit-behaviour dose-response relationships with mortality-relevant biomarkers visible in NHANES and UKBB linked mortality (GBD 2021 burden anchor).
- **(c) Causal:** Trans-ancestry Mendelian-randomization (not FinnGen-only) shows risk-tolerance and reward-sensitivity exposures causally raise metabolic, alcoholic, and psychiatric burden.

**Falsification criterion:** If *any two of the three* (behavioural, biomarker, causal) converge on a null or opposite-sign result across pooled data sources, H1 is rejected and the human claim is restricted to narrow phenotypes. Specifically: pooled behavioural β (across ≥5 cohorts) must have 95 % CI excluding 0 in the predicted direction; pooled trans-ancestry MR OR (≥3 ancestry groups) must have 95 % CI excluding 1 in the predicted direction on ≥3 of 5 exposure-outcome pairs.

**Prior-evidence strength:** Strong. NHANES, UKBB, and the current FinnGen-only MR battery already partially support (b) and (c). The weakness is ancestry coverage and behavioural cohort breadth, which is exactly what the new data sources fix.

---

### H2 — Sweet Trap is phylogenetically widespread across Animalia

**Claim:** The Sweet Trap signature (Δ_ST > 0: ancestral reward-fitness alignment reversed by environmental change or novel stimulus under voluntary approach behaviour) occurs in ≥50 independent animal cases spanning ≥6 phyla, including but not limited to Chordata (mammals, birds, reptiles, amphibians, fish), Arthropoda (insects, arachnids), Mollusca, Cnidaria, and Annelida.

**Predicted signatures:**
- Systematic review of PubMed + Web of Science returns ≥100 candidate cases ("ecological trap", "evolutionary trap", "sensory trap", "supernormal stimulus", "reward mismatch") after PRISMA screening.
- ≥50 cases pass F1+F2 criteria with estimable Δ_ST using the pre-registered coding scheme (extended from the 20-case v2 base).
- Pooled Δ_ST in a DerSimonian-Laird random-effects model exceeds +0.3 with 95 % CI excluding 0, replicating the N=20 v2 headline at quadrupled scale.
- The 50+ cases map onto a phylogenetic tree (TimeTree / Open Tree of Life) covering ≥6 phyla and ≥12 classes.

**Falsification criterion:** If systematic review returns fewer than 50 F1+F2-passing cases from the declared search, or if pooled Δ_ST CI crosses 0, H2 is rejected. A weaker but still informative fallback: if the case set concentrates in ≤3 classes (e.g. only insects, birds, and mammals), then the "across Animalia" claim reduces to "across tetrapods + insects", which has different theoretical implications and requires headline revision.

**Prior-evidence strength:** Moderate-strong. The 20-case v2 meta already covers 7 classes. Expansion to 50+ is a question of search effort, not whether cases exist; the ecological-trap literature alone (Robertson & Hutto 2006; Hale & Swearer 2016) counts >400 candidate systems.

---

### H3 — Sweet Trap susceptibility carries phylogenetic signal: related species share similar susceptibility

**Claim:** Among animals exhibiting Sweet Trap, susceptibility (operationalized via Δ_ST magnitude and mechanism category) is non-independently distributed across the phylogeny; species sharing recent common ancestry show more similar susceptibility than expected under independent acquisition.

**Predicted signatures:**
- Blomberg's K > 0.3 for Δ_ST magnitude on the TimeTree-derived phylogeny (N ≥ 50 species).
- Pagel's λ significantly > 0 (likelihood-ratio test vs λ = 0) at α = 0.05.
- Ancestral-state reconstruction (stochastic character mapping) identifies ≥2 evolutionarily-deep origins of Sweet Trap susceptibility (expected: one at the bilaterian-reward-system origin, one or more clade-specific for sensory-exploit-heavy groups).

**Falsification criterion:** If Blomberg's K < 0.1 and Pagel's λ not distinguishable from 0 (95 % CI includes 0), H3 is rejected. That outcome would reposition the paper: Sweet Trap would then be a *convergent* phenomenon (independently evolved in many lineages because the underlying physics of reward-fitness integration is the same everywhere) rather than an *inherited* phenomenon. Both are publishable claims, but the framing changes — convergence = "universal dynamical constraint"; inherited = "deep homology of vulnerability". We pre-commit to reporting whichever result we find without post-hoc narrative fitting.

**Prior-evidence strength:** Weak (novel analysis — no prior phylogenetic-signal test exists for Δ_ST). This is the paper's main methodological innovation. The alternative outcome is not a null but an informative reframing.

---

### H4 — Reward signalling is produced by convergent functional architecture across phyla, with deep within-phylum conservation of receptor families

**Overall claim:** Reward signalling is an evolutionary convergence phenomenon at the cross-phylum level and a conservation phenomenon at the within-phylum level. The two-tier structure is the core prediction: within a phylum, core receptor families (dopamine, opioid, sweet-taste) are held under strong purifying selection at their ligand-binding domains; across phyla, **non-orthologous but architecturally equivalent** receptor systems have been evolved *independently* and converged onto shared functional architectures (GPCR class-A topology, Venus flytrap / 7TM ligand-binding modules, G-protein → cAMP/PKA coupling). Convergence is *a stronger evolutionary claim than conservation alone*: a conserved trait is compatible with drift; a convergent trait requires repeated selection for the same functional outcome. This two-tier structure is the specific evolutionary signature predicted by the "Sweet Trap is produced by evolution" thesis.

We split H4 into H4a (within-phylum conservation) and H4b (cross-phylum convergence). Both must hold for the full H4 to pass; either alone yields a qualified but publishable outcome.

---

#### H4a — Within-phylum conservation of reward receptor families

**Claim:** Within each major phylum sampled, core reward receptor families are under strong purifying selection at the ligand-binding domain, exceeding the within-phylum genome-wide median.

**Predicted signatures:**
- **Chordata:** Dopamine D1-like and D2-like receptor orthologs recoverable in ≥95 % of sampled vertebrate genomes (Ensembl + NCBI Homologene); LBD pairwise amino-acid identity > 70 %; ligand-binding-domain dN/dS < 0.15 on ≥80 % of internal vertebrate branches (PAML codeml branch-model). μ-opioid receptor (OPRM1) orthologs recoverable in ≥90 % of sampled vertebrate genomes. TAS1R2/TAS1R3 orthologs recoverable across Mammalia (with documented carnivore-lineage pseudogenisation in felids / phocids as independent relaxed-constraint episodes).
- **Arthropoda:** Dopamine receptor orthologs (DopR1, DopR2, DopEcR) recoverable in ≥90 % of sampled insect genomes (Ensembl Metazoa + FlyBase + OrthoDB); LBD pairwise identity > 60 % within Insecta; LBD dN/dS < 0.15 on ≥80 % of internal insect branches. Gustatory receptor family (Gr5a-Gr64) paralog diversification documentable within Diptera / Hymenoptera.
- **Synteny (within-phylum):** Dopamine-receptor gene cluster micro-synteny retained across vertebrate classes (Genomicus blocks). Gr-family micro-synteny retained across Drosophilidae.
- **Baseline comparison:** Genome-wide matched-gene dN/dS distribution empirically estimated per phylum; reward-receptor dN/dS tested via Wilcoxon one-sided at p < 0.01.

**Falsification (H4a):** If within-phylum LBD dN/dS for reward-receptor orthologs does not significantly exceed matched-gene baseline (Wilcoxon p > 0.10 in *either* Chordata *or* Arthropoda), H4a is rejected for that phylum and the claim reduces to "within-phylum conservation holds only for a subset of reward receptor families."

**Prior-evidence strength:** Strong. Vertebrate dopamine-receptor family conservation documented (Yamamoto & Vernier 2011; Callier et al. 2003; Le Crom et al. 2003). Arthropod dopamine-receptor family conservation documented (Mustard et al. 2005; Karam et al. 2020). TAS1R carnivore pseudogenisation documented (Jiang et al. 2012). The within-phylum tier is a replication of established results using a unified pipeline, not a novelty claim — it functions as a **positive control** for the pipeline before the cross-phylum convergence test.

---

#### H4b — Cross-phylum functional convergence despite non-orthology

**Claim:** Across Bilaterian phyla (minimum: Chordata × Arthropoda × Mollusca × Cnidaria, with Annelida + Nematoda as extensions), reward signalling is implemented by **paraphyletic receptor systems** — lineages whose orthology does not trace to a single Bilaterian-ancestor receptor gene — that nevertheless share (i) GPCR class-A seven-transmembrane topology, (ii) Venus flytrap / 7TM ligand-binding module architecture (InterPro IPR000073 for TAS1R-family taste receptors; IPR000276 for rhodopsin-like GPCRs), and (iii) downstream G-protein → adenylyl-cyclase → cAMP/PKA signal transduction coupling. Convergence onto the same functional architecture from independent molecular starting points is the predicted evolutionary signature.

**Predicted signatures:**
- **TAS1R family (Chordata) vs Gr5a/Gr64 family (Arthropoda):** Phylogenetically paraphyletic (Chao et al. 2020; Robertson et al. 2003). Both share Venus flytrap module (IPR000073) AND 7TM GPCR architecture. Cross-phylum LBD pairwise identity 30–45 % (well below within-phylum levels), confirming independent evolutionary origin with architectural convergence.
- **Dopamine receptors (Chordata D1–D5) vs dopamine-like receptors (Arthropoda DopR1/DopR2/DopEcR, Mollusca Ap-DA1 Aplysia / Lym-DA1 Lymnaea, Cnidaria Nv-DA-like Nematostella):** All share GPCR class-A topology (IPR000276) and cAMP/PKA downstream coupling; cross-phylum LBD identity 40–50 %; phylogenetic analysis (Yamamoto & Vernier 2011; Van Nieuwenhuyzen et al. 2018) shows independent paralog expansion in each phylum, not descent from a single Bilaterian ancestor receptor.
- **μ-opioid receptor (Chordata) vs enkephalin-like / opioid-like peptides (invertebrates):** Functionally analogous reward-circuit role in invertebrates (Kream & Stefano 2006) without strict ortholog; predicted GPCR-cAMP architecture shared.
- **Cross-phylum phylogeny:** Maximum-likelihood trees for each receptor family show independent duplication-divergence events within each phylum (not shared Bilaterian ancestry).
- **Architectural convergence as main test:** Jaccard similarity of InterPro domain composition across cross-phylum reward-receptor homologs ≥ 0.70 (vs matched random-ortholog baseline ≤ 0.30). This is the **one decisive test** of H4b.

**Falsification (H4b):** H4b is rejected if **either** (i) cross-phylum LBD pairwise identity for reward-receptor homologs exceeds 70 % across ≥3 non-sister phyla (which would indicate deep sequence conservation, not convergence; this would actually resolve to the v3 "deep conservation" framing, which is also publishable but changes the headline), *or* (ii) architectural convergence fails — InterPro Jaccard ≤ 0.40, or downstream G-protein coupling differs across phyla. Case (i) would refute convergence by revealing strict conservation; case (ii) would refute convergence by revealing **no functional unity** across phyla (the weaker outcome — paper would downgrade to within-phylum-only and drop the cross-phylum claim).

**Prior-evidence strength:** Moderate-to-strong. The *components* of the H4b claim are documented piecewise: Venus flytrap module sharing across taste and metabotropic glutamate receptors (Pin et al. 2003), GPCR topology conservation across Metazoa (Fredriksson et al. 2003), non-orthology of Drosophila Gr with vertebrate TAS1R (Robertson et al. 2003; Feijó et al. 2019), dopamine-signalling presence in Nematostella (Ryan et al. 2013). The *integration* of these components into a single quantitative convergence claim for reward signalling specifically has not been made — this is where H4b's novelty sits.

**Why convergence is a stronger claim than conservation:** A conserved trait can be explained by historical contingency (a single ancient origin, subsequent drift-limited divergence). A convergent trait — the same functional architecture evolved independently in multiple lineages — requires *repeated selection pressure for the same functional outcome*. The latter is precisely the evolutionary signature implied by the thesis "Sweet Trap is produced by evolution": if reward-fitness decoupling susceptibility appears across taxa *because* the underlying receptor architecture was independently built the same way each time, then Sweet Trap is not an accident but a near-inevitable consequence of building any behaving organism on GPCR-cAMP reward logic.

**Falsification criterion (H4 overall):** H4 fully passes if both H4a and H4b pass. H4 partially passes if H4a passes and H4b falsification case (ii) triggers (reward signalling turns out to be phylum-specific, not functionally unified); the paper then claims "within-phylum conservation of reward machinery, without cross-phylum unity" — still publishable but reduces the cross-species inference. H4 fully fails if H4a is rejected in both Chordata and Arthropoda; this would eliminate the molecular evidence layer and the paper reduces to Parts 1 and 2 (human + animal-meta).

---

### H5 — Susceptibility covaries with life-history traits in a phylogenetically-controlled regression

**Claim:** After controlling for phylogeny, Sweet Trap susceptibility (Δ_ST) in animal species covaries with life-history traits in the direction predicted by evolutionary mismatch theory: shorter generation time, higher reproductive-rate/body-size ratio, and higher niche plasticity predict *lower* susceptibility (more scope for behavioural flexibility and rapid selection); specialised sensory systems and long generation time predict *higher* susceptibility.

**Predicted signatures:**
- PGLS (phylogenetic generalized least squares) regression of Δ_ST on PanTHERIA + AnAge life-history traits (N ≥ 30 mammalian + bird species for which traits are available): generation time β > 0 (p < 0.05); body mass β > 0 (p < 0.10).
- Residual phylogenetic signal (Pagel's λ on residuals) significantly reduced compared to Δ_ST alone, indicating life-history traits absorb phylogenetic variance.

**Falsification criterion:** If PGLS coefficients are null on all ≥3 predicted traits (all 95 % CI include 0), H5 is rejected. H5 is the paper's weakest hypothesis in terms of prior evidence, so a null here does not sink the paper — it strengthens the convergent-phenomenon interpretation from H3.

**Prior-evidence strength:** Weak-moderate. Life-history traits are known to covary with ecological-trap susceptibility (Hale & Swearer 2016) but no study has done this for a cross-phylum Sweet-Trap-operationalized outcome.

---

### H6 — Gene-level causal evidence for evolutionary shaping of reward-fitness decoupling

**Overall scope (Paper 1 lightweight):** H6 comprises six sub-hypotheses (H6a–H6f) covering the causal-genetic evidence that Sweet Trap susceptibility is not a descriptive artefact of receptor architecture but carries lineage-specific molecular footprints of evolutionary shaping. Paper 1 executes **H6a** (positive-selection branch-site scan) and **H6f** (cross-species genetic-manipulation literature summary) — both lightweight, 2-3 week compute envelope, feasible with Ensembl + PAML + public literature. H6b (Gene × Environment interaction in human biobanks), H6c (parallel positive selection across Chinese-native species via CNGBdb), H6d (polygenic risk score discriminant validity), and H6e (recent selection scans in human lineage) are **Paper 2 roadmap**, announced but not tested in Paper 1.

---

#### H6a — Lineage-specific positive selection on reward-receptor ligand-binding domains

**Claim:** In lineages with documented ecological shifts toward reward-fitness-decoupled environments (e.g., vertebrate sweet-food specialisation in hummingbirds post- TAS1R1 umami-to-sweet repurposing; vertebrate hyperpalatable-food adaptation in primate sugar-specialists; insect nectarivore specialisation in Apidae; mammalian sensory-specialisation in cetaceans), reward-receptor ligand-binding-domain (LBD) codons show signatures of **positive selection** (dN/dS > 1 on a subset of branches/sites) under PAML branch-site Model A — beyond the within-phylum purifying-selection baseline established by H4a.

**Predicted signatures:**
- **Branch-site Model A (foreground on ecological-shift lineage, background null):** Likelihood-ratio test (LRT) p < 0.05 on at least 3 of 15 target genes (DRD1-5 / OPRM1 / OPRK1 / OPRD1 / OPRL1 / TAS1R1-3 / HCRTR1-2 / NPY1/2/5R) across ≥ 4 independent ecological-shift lineages.
- **Positive control lineage (hummingbird TAS1R1):** Baldwin et al. 2014 *Science* documented selection for sweet-sensing recovery via TAS1R1 co-option; our pipeline re-detects this signal as a pipeline-validation positive control. Expected: ω > 1 on hummingbird TAS1R1 foreground branch with p < 0.01.
- **Bonferroni-corrected gene list:** ≥ 2 genes pass α = 0.05/15 = 0.0033 threshold.
- **Site model M2a vs M1a:** Confirms positive-selection sites within the LBD structural annotation (InterPro IPR000073 / IPR000276).

**Falsification criterion:** If branch-site Model A returns zero positive-selection signal (LRT p > 0.10) across all 15 genes × 4 ecological-shift lineages AND hummingbird TAS1R1 control also returns null (pipeline validation failure), H6a is rejected. If only hummingbird control passes but no other lineages do (only positive control validates), H6a reframes to "positive selection detectable only for documented textbook cases; cryptic selection on Sweet Trap-relevant lineages is below branch-site resolution." This is a restricted but still publishable finding.

**Prior-evidence strength:** Moderate-strong. Baldwin et al. 2014 (hummingbird TAS1R1) and Zhao et al. 2010 (panda T1R1 pseudogenisation) document positive selection / relaxed selection in specific reward-receptor lineages. The generalisation across multiple reward-receptor families × multiple ecological-shift lineages has not been packaged as a quantitative test.

**Contribution vs H4a:** H4a tests *purifying selection within phylum* (descriptive; the receptor is conserved). H6a tests *positive selection on specific lineages* (causal; the receptor was under active selection in lineages exposed to Sweet Trap environments). H6a is the causal-genetic counterpart of H4a's descriptive claim — and together they constitute the "shaped by evolution" evidence at the molecular level.

---

#### H6b–H6e — Reserved for Paper 2 (announced roadmap, not tested in Paper 1)

These four sub-hypotheses are defined here to establish conceptual priority for the Sweet Trap gene-level research programme but are **not executed in Paper 1** due to scope constraints (eLife RPP word budget, computational footprint, and data-access lead time).

- **H6b (Gene × Environment interaction):** Reward-receptor risk alleles (DRD2 TaqIA rs1800497; FTO rs9939609; CHRNA5 rs16969968; COMT Val158Met; MC4R) show main-effect × environmental-exposure (modern food environment, screen-time density, addictive-commodity availability) interaction on Sweet Trap-relevant phenotypes (BMI trajectory, HbA1c, problem gambling, UPF intake) in UK Biobank + FinnGen + All of Us. Expected GxE interaction p < 0.01 for ≥ 3 allele × environment pairings; main-effect-only models should *not* suffice (G main effect explains < 30 % of variance explained by GxE term). Paper 2 target.

- **H6c (Parallel positive selection across Chinese-native species):** H6a extended to 3-5 CNGBdb-hosted Chinese-native species (giant panda, golden snub-nosed monkey, Tibetan antelope, Tibetan fox, red-crowned crane). Multiple independent positive-selection footprints on orthologous reward-receptor LBDs across phylogenetically-dispersed lineages would constitute strong convergent-positive-selection evidence. Paper 2 target.

- **H6d (Polygenic risk score discriminant validity):** Construct per-domain PRS for 5 human Sweet Trap domains (C11 diet, C12 short-video, C13 luxury, C8 investment, D_alcohol) from UKB + FinnGen + BBJ + MVP + AoU GWAS summary statistics. Predict that each domain's PRS has stronger association with its own domain phenotype than with control phenotypes (discriminant validity on genetic level), with trans-ancestry replication across ≥ 3 ancestries. Paper 2 target.

- **H6e (Recent selection scans in human lineage):** Ancient-DNA-based selection-scan signatures (from Allen Ancient DNA Resource AADR v54, 1000 Genomes) on reward-receptor loci during the past 10,000 years of human lineage evolution, correlated with major dietary / environmental transitions (Neolithic / Bronze Age / industrial). Paper 2 target.

---

#### H6f — Cross-species genetic-manipulation literature summary (narrative + quantitative synthesis)

**Claim:** Published experimental genetic manipulation of reward-receptor homologs in non-human model organisms produces phenotypic consequences consistent with Sweet Trap logic — specifically, receptor-knockdown / knockout / overexpression changes the propensity for reward-fitness-decoupled behaviour in a direction predicted by A1-A4.

**Structure:** H6f is a *narrative + quantitative table*, not a primary analysis. We compile all published experiments in the 2000-2026 window that (i) manipulate a reward-receptor gene (DopR family / TAS1R family / opioid / orexin / NPY-receptor homologs) in (ii) a non-human metazoan organism (Drosophila, C. elegans, Apis, rodents) and (iii) measure a phenotype that can be coded against F1+F2 or Δ_ST logic. Each experiment is coded on: organism, gene manipulated, manipulation type, behaviour measured, direction of effect, sample size, published journal, DOI.

**Predicted signatures:**
- **Quantitative coding of ~30-50 published experiments**, with ≥ 70 % reporting directionally consistent effects (receptor loss-of-function → reduced pursuit of hyper-rewarding/low-fitness stimuli; receptor gain-of-function → enhanced pursuit). Canonical examples: Kaun et al. 2011 *Nat Neurosci* (Drosophila DopR knockout → reduced ethanol tolerance), Johnson & Kenny 2010 *Nat Neurosci* (mouse Drd2+/− → altered palatable-food seeking), de Bono 1998 *Cell* (C. elegans NPR-1 variant → altered social feeding), Baldwin et al. 2014 *Science* (hummingbird TAS1R1 co-option → sweet detection).
- **Cross-phylum coverage**: ≥ 3 phyla represented (Chordata, Arthropoda, Nematoda minimum) in the summary table.

**Falsification criterion:** If < 50 % of coded experiments show directionally consistent effects, H6f is rejected and the paper cannot claim that genetic-manipulation literature supports the Sweet Trap framework at the causal level. Most likely outcome given published evidence base: H6f passes at ~70-85 % concordance with directional consistency.

**Prior-evidence strength:** High. The individual experimental papers are well-established; the novelty is in the *synthesis under a common Δ_ST / F1+F2 coding scheme*, which has not been done before. The summary table becomes a reference resource for the field.

**Contribution:** H6f provides **causal-genetic validation** at the cross-phylum level without requiring the authors to run new experiments. It converts Layer E (full experimental Sweet Trap knockdown programme) from "must execute before submission" to "already partially supported by the literature; full experimental validation reserved for Paper 3 horizon."

---

## 4. Hypothesis Dependency Structure

H1-H4 are designed to be *mutually independent*: each can succeed or fail without logically entailing the others. H5 is a secondary prediction. H6a / H6f are Paper 1 gene-level tests; H6b-H6e are reserved for Paper 2. The paper's headline survives under the following minimum-evidence configurations (focusing on H6a since H6f almost certainly passes at ≥ 70 % concordance given published literature base):

| H1 | H2 | H3 | H4a | H4b | H5 | H6a | Headline |
|----|----|----|-----|-----|----|-----|----------|
| ✓ | ✓ | ✓ | ✓ | ✓ | any | ✓ | **Full claim:** Sweet Trap is phylogenetically inherited behaviour on convergently-assembled-but-within-phylum-conserved reward architecture with lineage-specific positive-selection footprints — the maximally evolutionarily-shaped claim |
| ✓ | ✓ | ✓ | ✓ | ✓ | any | ✗ | **Conservation-only claim:** Sweet Trap rides on deeply conserved receptor machinery without lineage-specific positive selection footprints; evolutionary shaping is indirect / via architecture-level constraints rather than codon-level selection |
| ✓ | ✓ | ✗ | ✓ | ✓ | any | ✓ | **Convergence claim with lineage selection:** universal behavioural convergence + convergent molecular architecture + lineage-specific positive selection — "repeatedly-shaped by evolution" framing |
| ✓ | ✓ | ✓ | ✓ | ✗ | any | ✓ | **Within-phylum claim with lineage selection:** Sweet Trap conserved within phyla, molecularly phylum-specific, but positive-selection footprints confirm evolutionary shaping in lineages where Sweet Trap environments emerged |
| ✓ | ✓ | ✓ | ✗ | any | any | any | **Behavioural-only claim:** phylogenetic signal present but molecular machinery heterogeneous — Part 3 + Part 4 reduced to SI, paper becomes Parts 1+2 only |
| ✗ | ✓ | any | any | any | any | any | **Comparative-biology claim only:** paper becomes an animal-evolutionary-trap paper; human section moves to Discussion |
| any | ✗ | any | any | any | any | any | **Paper does not reach publication threshold;** H2 is the load-bearing layer |

The critical path remains H2 (≥ 50 cases). H3 / H4a / H4b / H5 / H6a modulate the framing but not the publishability. The four-part design — Part 1 human + Part 2 animal + Part 3 molecular architecture + Part 4 gene-level causality (lightweight) — ensures that *any* reasonable combination of H4a / H4b / H6a outcomes produces a publishable headline; the framing shifts but the Sweet Trap construct + Δ_ST operationalisation + phylogenetic-signal claim survive.

---

## 5. What This Hypothesis Set Does NOT Claim

To forestall the hostile-reviewer "umbrella construct" objection, the following are *not* claims of this paper and are stated as such in the Limitations section of the final manuscript:

- **Not a welfare claim:** We do not claim Δ_ST implies welfare loss; that requires a normative framework out of scope here.
- **Not an intervention-asymmetry claim:** The T2 intervention-asymmetry theorem from the v3.x policy paper is not tested in this paper. Paper 1 is evolutionary biology, not behavioural policy.
- **Not a construct-supremacy claim:** We do not claim Sweet Trap supersedes ecological-trap, evolutionary-mismatch, or sensory-exploitation frameworks; we claim it unifies them operationally under a measurable scalar (Δ_ST) with a testable phylogenetic distribution and gene-level selection footprint.
- **Not a human-exceptionalism claim:** Humans are one clade among many; the paper's human section (Part 1) is demonstration, not the centre.
- **Not a full causal-molecular claim:** H4 (a + b) establishes within-phylum conservation and cross-phylum convergent architecture; H6a establishes lineage-specific positive selection. Together these provide *indirect causal evidence* for evolutionary shaping of reward-signalling, but direct causal demonstration (receptor-knockout within-species rescue experiments demonstrating Sweet Trap phenotype dependence on specific alleles) is **reserved for Paper 3 / Layer E future work**.
- **Not a full gene-level-causality claim in Paper 1:** H6b (GxE), H6c (cross-species parallel positive selection), H6d (PRS discriminant validity), H6e (ancient-DNA selection scans) are **reserved for Paper 2** (6-12 month horizon). Paper 1 Part 4 executes H6a + H6f only. Claiming H6b-H6e in Paper 1 would overpromise given Paper 1's compute and data-access envelope.

---

## 6. Pre-Registration Timing

Stage 0 hypothesis document will be deposited on OSF before any new data extraction begins (Week 0 of the 12-week plan). Specifically:

- **Week 0 (pre-registration):** H1-H5 + H6a + H6f (Paper 1 tested hypotheses) + H6b-H6e (Paper 2 announced roadmap) + analytical-pipeline document + journal-matching document committed to OSF with timestamp. bioRxiv priority preprint (4-page scoping) deposited same day.
- **Week 1-8 (execution):** Data extraction and analysis follow the pre-registered pipeline for Paper 1 hypotheses only. Paper 2 hypotheses (H6b-H6e) are explicitly not executed in this window — they are announced to establish conceptual priority but will be tested in a separate 6-12-month-later study.
- **Week 9-10 (writing):** Any deviations from pre-registered protocol are flagged in the Methods with reasons.

This addresses the hostile-reviewer objection on Layer B's post-hoc pre-registration rule (which was data-contingent). The new pre-registration is genuinely ex-ante because no new data have been extracted.

---

*Document version 1.0. Author: PI, Stage 6 research reset. Supersedes all HSSC-era hypothesis framing.*
