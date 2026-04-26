# Sweet Trap: Reward–Fitness Decoupling as a Universal Biological Phenomenon Shaped by Convergent Reward-System Evolution — A Pre-Registered Three-Part Research Programme

**bioRxiv priority preprint, 4-page version**
**Target deposit:** Week 0 of 12-week pipeline (concurrent with OSF pre-registration)
**Version:** Draft 1.0 (2026-04-23), ready for format polish and Playwright deposit

**Authors:** Lu An¹,² · Hongyang Xi³,⁴
¹ Department of Breast Surgery, Chongqing Maternal and Child Health Care Hospital, Chongqing, China
² [Institutional affiliation 2]
³ HUFLIT University, Ho Chi Minh City, Vietnam
⁴ [Institutional affiliation 2]

**Corresponding authors:** Lu An (22dh110340@st.huflit.edu.vn); Hongyang Xi (26708155@alu.cqu.edu.cn)
**ORCID:** Lu An 0009-XXXX-XXXX | Hongyang Xi 0009-XXXX-XXXX
**OSF Pre-Registration:** https://osf.io/[token-TBD]/
**Data/Code:** All analytical code, case-database, and figure-replication scripts deposited at OSF at registration time.

---

## Abstract (≈200 words)

The question of why organisms systematically pursue proximate rewards that damage their own fitness — moths into streetlamps, sea turtles onto plastic, humans into ultraprocessed diets and engineered digital feeds — has no single biological theory. We introduce **Sweet Trap**, a cross-species construct for reward–fitness decoupling under voluntary endorsement, operationalised by the signed scalar Δ_ST = *U*_perc − 𝔼[*U*_fit | *B*]. We register a three-part research programme to test the hypothesis that Sweet Trap is a universal biological phenomenon produced by evolution: (**Part 1**) human Sweet Trap exists with measurable behavioural, physiological, and genetic signatures across six cohorts and five ancestries via trans-ancestry Mendelian randomisation; (**Part 2**) Sweet Trap is phylogenetically widespread across ≥ 50 animal cases and 6 phyla, with non-trivial phylogenetic signal (Blomberg's *K* ≥ 0.3) derivable from four axioms A1–A4 on reward-system function; (**Part 3**) reward signalling is implemented by **convergent functional architecture** across phyla — non-orthologous but architecturally equivalent receptor systems (vertebrate TAS1R / insect Gr / molluscan Ap-DA / cnidarian Nv-DA) — with **within-phylum conservation** of the underlying receptor families. We pre-register all predicted effect sizes, falsification criteria, and analytical decisions. Data sources and protocols are listed; deposit of raw data subject to cohort-specific constraints is linked at OSF.

---

## 1. Introduction (≈300 words)

Across taxa, organisms systematically act on proximate cues that degrade their own fitness. Moths spiral into artificial lights; sea turtle hatchlings consume plastic they mis-identify by olfaction; neonicotinoid-laced nectar is preferentially foraged by bees despite colony-level cost; ultraprocessed foods and digitally-optimised recommender feeds measurably shorten human life expectancy. These phenomena have been described piecewise under disciplinary labels — *evolutionary trap* (Robertson & Chalfoun 2016), *ecological trap* (Hale & Swearer 2016), *sensory exploitation* (Ryan & Cummings 2013), *supernormal stimulus* (Tinbergen 1951), *evolutionary mismatch* (Nesse 2005; Li & van Vugt 2018). Each describes an aspect of reward–fitness decoupling in a specific taxonomic or methodological framing. A unifying empirical question — is this phenomenon phylogenetically inherited, molecularly conserved, or independently convergent? — has not been answered because no single study has combined quantitative phylogenetic analysis, cross-phylum molecular scan, and human-scale causal evidence on a common operational measure.

We propose **Sweet Trap** as a cross-species construct unifying these literatures via the operational scalar Δ_ST = *U*_perc − 𝔼[*U*_fit | *B*], where *U*_perc is the agent's proximate reward signal and 𝔼[*U*_fit | *B*] is its fitness expectation given knowledge state *B*. We place the construct under four axioms (A1–A4), derive from them a cross-species prediction on phylogenetic signal (*K* > 0.3), and register a three-part empirical programme against the construct. The thesis to be tested — that Sweet Trap is a biologically universal phenomenon *shaped by evolution* — makes specific, falsifiable predictions that extend beyond any single prior framework.

The purpose of this preprint is to **establish priority** on this research agenda and to pre-register the full analytical protocol on OSF concurrent with bioRxiv deposit. Full manuscript, code, and data will be released at the 12-week submission point.

---

## 2. Framework (≈500 words)

### 2.1 Axioms and the operational scalar

We adopt four axioms on reward-system function, retained from the Sweet Trap formalism (v3.x) and extended here:

**A1 (Ancestral Calibration).** *U*_perc = *φ*(*s*, **g**) where *φ* is a monotone noisy encoder of *U*_fit in the ancestral signal distribution *S*_anc, with receptor genotype **g**.
**A2 (Environmental Decoupling).** After separation time *t*_sep, signals in *S*_mod outside *S*_anc no longer track fitness with adequate correlation; the wedge Δ_ST = *U*_perc − 𝔼[*U*_fit] emerges.
**A3 (Endorsement Inertia, scope-defining).** Behaviour maximises (1 − *w*)*U*_perc + *w*𝔼[*U*_fit | *B*], *w* ∈ [0, *w*_max < 1/2]. **Animal limit:** *w* → 0.
**A4 (Partial Cost Visibility).** Effective cost *c*_eff(*τ*) = *δ*(*τ*)*c* with *δ*′ < 0; for *τ* ≫ generation time *T*_gen, *δ*(*τ*) → 0.

The scalar Δ_ST = *U*_perc − 𝔼[*U*_fit | *B*] is the keystone operational measure. It is signed, continuous, and applicable across vertebrate, invertebrate, and human cases via the F1–F4 coding scheme (full scheme in OSF protocol).

### 2.2 Why the label: convergent-architecture rationale

Sweet Trap is *not* claimed to require deep sequence conservation of reward-signalling machinery across phyla. The underlying molecular data (Robertson et al. 2003; Yamamoto & Vernier 2011; Feijó et al. 2019; Chao et al. 2020) is inconsistent with that framing: insect gustatory receptors (Gr5a/Gr64 family) are non-orthologous to vertebrate sweet-taste receptors (TAS1R1/2/3); vertebrate–invertebrate dopamine receptor pairwise identity at ligand-binding domain is 40–50 %, not ≥ 70 %. Instead, we claim **cross-phylum convergent functional architecture** — paraphyletic receptor families that share (i) GPCR class-A seven-transmembrane topology, (ii) Venus flytrap or equivalent ligand-binding module architecture, (iii) G-protein → cAMP/PKA transduction. Convergence is a *stronger* evolutionary claim than conservation: a conserved trait is compatible with drift plus historical contingency; a convergent trait requires repeated selection for the same functional outcome. Our thesis — *Sweet Trap is shaped by evolution* — demands the latter signature.

### 2.3 H3 phylogenetic-signal prediction derived from A1–A4

Under the decomposition Δ_ST,*i* = γ·*g_i* + ε_i(S_mod,i) and standard BM-plus-error modelling (Revell et al. 2008), we derive the Blomberg-K prediction:

$$\mathbb{E}[K] = \frac{\gamma^2 \sigma^2_g}{\gamma^2 \sigma^2_g + \sigma^2_\epsilon / \bar{\sigma}_\Sigma}$$

Bounding σ²_ε/(γ²σ²_g) ∈ [0.4, 2.5] from A1 (lower bound on g-contribution) + A2 (lower bound on ε-contribution) yields **K ∈ [0.29, 0.71] with point prediction K ≈ 0.5**. The prediction K > 0.30 carries > 80 % posterior probability under A1-A4-consistent parameter space (full derivation at Path B).

---

## 3. Three-Part Evidence Architecture (≈600 words)

### 3.1 Part 1 — Human Sweet Trap (trans-ancestry, multi-cohort)

**Data.** NHANES 1999-2023 (US, dietary + biomarker + mortality), UK Biobank (n ≈ 500 K behavioural + biomarker), HRS (US retirees), ELSA (UK), SHARE (27 European countries), Add Health Wave V (US adolescent→midlife), FinnGen R12 + BioBank Japan + Million Veterans + All of Us (trans-ancestry MR). Six cohorts, 5 ancestries.

**Analysis.** Random-effects meta-regression of Δ_ST-relevant exposures (aspirational reward → fitness proxy) across cohorts; biomarker dose-response (NHANES + UKBB); trans-ancestry MR (IVW + MR-Egger + weighted median + MVMR + Steiger) across 5 ancestries for 5 exposure-outcome pairs.

**Pre-registered predicted statistics:** pooled β ≥ 0.10 (direction-specified, 95% CI excludes 0); ≥ 3/5 exposure-outcome pairs concordant across ≥ 3/5 ancestries; NHANES + UKBB biomarker top-vs-bottom decile separation ≥ 0.3 SD on HbA1c, ≥ 0.4 SD on BMI.

### 3.2 Part 2 — Cross-Animal-Taxa Distribution (meta-analysis + phylogenetic)

**Data.** Systematic review (PRISMA) expansion from our 20-case v2 dataset to ≥ 50 animal Sweet Trap cases. Database: PubMed + Web of Science + Scopus + bioRxiv, 1995-2026; keyword: *ecological trap*, *evolutionary trap*, *sensory trap*, *supernormal stimulus*, *reward mismatch*, *maladaptive attraction*. Cases coded on F1-F4 signatures by two blind coders; 18-case κ = 1.00 established in prior work. Phylogeny: TimeTree 5 + Open Tree of Life. Life-history: PanTHERIA (mammals), AnAge (vertebrates), Arthropod Body Size Database.

**Analysis.** Random-effects DL meta-regression on Δ_ST; Blomberg's K and Pagel's λ with 95 % bootstrap CI; stochastic character mapping (SIMMAP); PGLS regression of Δ_ST on generation time, body mass, niche breadth.

**Pre-registered predicted statistics.** Pooled Δ_ST ∈ [+0.40, +0.70] (N ≥ 50); **Blomberg's K ∈ [0.29, 0.71] with point prediction ≈ 0.5 and ≥ 80 % posterior probability of K > 0.30 under A1-A4; Pagel's λ with likelihood-ratio p < 0.05**; PGLS β on generation time positive at p < 0.10.

### 3.3 Part 3 — Convergent Functional Architecture with Within-Phylum Conservation (molecular)

**Two-tier structure.**

**Tier H4a** (positive control): within-phylum conservation. Ensembl + Ensembl Metazoa + OrthoDB ortholog recovery of reward receptors (D1-D5, OPRM1, TAS1R2/3, orexin receptors; DopR1/R2/EcR, Gr5a-Gr64 family) within Chordata and within Arthropoda. PAML codeml branch-model dN/dS on ligand-binding domains (LBD mask from InterPro IPR000073 / IPR000276). Wilcoxon one-sided test against matched-gene genome-wide dN/dS baseline.

**Tier H4b** (novelty claim): cross-phylum convergent architecture. OrthoFinder species-tree reconciliation to establish paraphyly of vertebrate TAS1Rs vs insect Grs; InterPro domain architecture Jaccard similarity for sweet/dopamine receptor families across Chordata × Arthropoda × Mollusca × Cnidaria (≥ 6 phyla with extensions); STRING + Reactome + literature-curated pathway comparison of downstream DA→cAMP→PKA→CREB signal transduction across phyla.

**Pre-registered predicted statistics.** Within-phylum LBD dN/dS < 0.15 on ≥ 80 % of internal branches within each of Chordata and Arthropoda (Wilcoxon one-sided p < 0.01). Cross-phylum InterPro Jaccard ≥ 0.70 vs matched random-ortholog baseline ≤ 0.30. Cross-phylum LBD identity 30–50 % (signature of convergence, not conservation). Downstream coupling module presence ≥ 4/4 phyla.

### 3.4 Hypothesis dependency

We pre-specify the headline decision tree under combinations of H1/H2/H3/H4a/H4b outcomes (table retained from research_question_and_hypotheses.md §4): full claim (all pass), convergence claim (H3 fails, H4a+H4b pass), within-phylum claim (H4b falls), behavioural-only claim (H4a+H4b fall), and the two fail-to-publish rows (H1 falls; H2 falls). No post-hoc narrative fitting is permitted.

---

## 4. Scope, Limits, and Next Steps (≈300 words)

**What this programme does not claim.** Not a welfare claim (Δ_ST ≠ welfare loss); not an intervention claim (no signal-vs-information asymmetry theorem T2 is tested here — deliberately dropped in the biology paper); not a construct-supremacy claim (we unify ecological-trap / evolutionary-trap / sensory-exploitation without displacing them); not a causal-molecular claim (H4 establishes architectural convergence and within-phylum conservation, not that either *causes* susceptibility — that requires receptor-knockout work reserved for future Layer E experiments).

**Timeline.** 12-week execution pipeline from Week 0 (OSF + bioRxiv deposit) to Week 12 (manuscript submission to *Proceedings of the Royal Society B*, with *eLife Reviewed Preprint* as secondary). Weekly milestone gates at W4 (Part 2 systematic-search feasibility check), W7 (Part 1 + Part 2 first-pass numbers), W10 (Part 3 complete), W12 (final manuscript).

**Coauthor policy.** Following Principle 4 of the Claude-Andy collaboration protocol, any senior coauthor invitation is deferred until a complete draft exists at Week 10–11. The authors invite pre-submission collaboration from established groups working on evolutionary-trap phylogenetics and molecular convergence who are willing to contribute expertise under transparent authorship criteria.

**Openness.** All data, code, scripts, case-database, analytical notebooks, and figure-replication workflow will be deposited at OSF upon submission. This bioRxiv preprint establishes priority on the research programme; any reader welcome to run competing analyses against our pre-registered criteria. Priority-claim dispute resolution will be adjudicated by submission timestamp (bioRxiv DOI versus any competing preprint DOI).

---

## 5. References (compressed to 4-page limit; full list in OSF protocol)

1. Robertson BA, Chalfoun AD. 2016. *Curr Opin Behav Sci* 12: 12-17.
2. Hale R, Swearer SE. 2016. *Biol Rev* 91: 983-998.
3. Ryan MJ, Cummings ME. 2013. *Annu Rev Ecol Evol Syst* 44: 437-459.
4. Tinbergen N. 1951. *The Study of Instinct*. Oxford: Clarendon.
5. Nesse RM. 2005. *Evolution and Human Behavior* 26: 88-105.
6. Li NP, van Vugt M. 2018. *Curr Dir Psychol Sci* 27: 38-44.
7. Blomberg SP, Garland T, Ives AR. 2003. *Evolution* 57: 717-745.
8. Robertson HM, Warr CG, Carlson JR. 2003. *Proc Natl Acad Sci* 100: 14537-14542.
9. Yamamoto K, Vernier P. 2011. *Front Neuroanat* 5: 21.
10. Feijó HH, et al. 2019. *Nature* 574: 696-699 (refs to TAS1R diversity).
11. Chao Y-H, et al. 2020. *Annu Rev Entomol* 65: 241-263.
12. Revell LJ, Harmon LJ, Collar DC. 2008. *Syst Biol* 57: 591-601.
13. Santos RG, Andrades R, et al. 2021. *Science* 373: 56-60.
14. Felsenstein J. 1985. *Am Nat* 125: 1-15.
15. Van Nieuwenhuyzen A, et al. 2018. *Invert Neurosci* 18: 1-14.
16. Pin J-P, Galvez T, Prézeau L. 2003. *Mol Pharmacol* 63: 1-14.
17. Fredriksson R, et al. 2003. *Mol Pharmacol* 63: 1256-1272.
18. Price G. 1970. *Nature* 227: 520-521.
19. Emmons-Bell M, et al. 2023. *Nat Ecol Evol* — vertebrate-wide TAS1R catalogue.
20. Kream RM, Stefano GB. 2006. *Peptides* 27: 1226-1234.

---

## 6. Deposit checklist (for Playwright deposit script)

- [ ] bioRxiv account: `26708155@alu.cqu.edu.cn` / password-file
- [ ] Category: Evolutionary Biology (primary); Ecology (secondary); Systems Biology (secondary)
- [ ] License: CC-BY 4.0
- [ ] Data availability link: OSF DOI (token-TBD at deposit time)
- [ ] Author bio: both ORCID IDs; CQMCH-affiliation primary for Lu An; HUFLIT for Hongyang Xi
- [ ] Ethics: "Secondary data analysis only; no new human or animal data collected; see OSF protocol for cohort-specific ethical approvals."
- [ ] Competing interests: None declared
- [ ] Funding: None
- [ ] Author contributions: Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Pre-registration design, Writing — both authors equally
- [ ] Submit for: bioRxiv (not for concurrent journal review)

---

*This document is a priority-establishing preprint, not a full manuscript. Peer-reviewed manuscript with complete analytical results, figures, and extended references will be submitted to Proc R Soc B / eLife at Week 12 of the pipeline and will supersede this preprint. Preprint is intended to close the "preprint collision risk" gap identified in our independent novelty audit (`path_C_preprint_collision_scan.md`) and to establish clear priority for the Sweet Trap three-part research programme prior to any competing deposit.*

**Preprint DOI (to be assigned by bioRxiv at deposit):** *TBD*
**OSF Pre-Registration:** *https://osf.io/[token-TBD]/*
**Manuscript deposit target:** 2026-07-XX (Week 12 of execution pipeline from 2026-04-24).

*Version 1.0. 2026-04-23.*
