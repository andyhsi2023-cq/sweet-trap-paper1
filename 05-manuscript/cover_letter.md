---
title: "Cover Letter — Sweet Trap Paper 1 submission to Royal Society Open Science"
date: 2026-04-25
target_journal: "Royal Society Open Science"
---

**To:** The Editor-in-Chief, *Royal Society Open Science*
(Current EiC to be confirmed on the journal masthead before dispatch; otherwise: Dear Editor)

**From:** Lu An (co-corresponding) and Hongyang Xi (co-corresponding)

---

Dear Editor,

We are pleased to submit our manuscript, **"Sweet Trap is widespread but not universal: a pre-registered cross-metazoan falsification of reward-fitness decoupling as a shared evolutionary trait"**, as a **Research Article** for consideration at *Royal Society Open Science*. A companion priority preprint is on bioRxiv (**BIORXIV/2026/720498**, deposited 2026-04-24) and the full pre-registration with raw datasets, codon alignments, time-calibrated trees, PAML codeml control files, and analysis scripts is public on OSF (**<https://osf.io/pv3ch>**, deposited 2026-04-24, *before* data extraction). The manuscript is not under consideration at any other journal.

**Core thesis.** We tested three pre-registered predictions of universality for reward-fitness decoupling across Metazoa; **all three are not supported by our data**. (i) Cross-phylum phylogenetic signal at Blomberg's $K > 0.30$ — refuted ($K = 0.117$, $p = 0.251$). (ii) Shared molecular substrate across phyla in sweet-receptor families exceeding a matched-random Pfam null baseline — not supported (vertebrate TAS1R vs insect Gr Jaccard = 0, with $P(\text{Jaccard}=0\,|\,\text{null}) = 0.9998$ — exactly the modal null outcome). (iii) Detectable positive selection on reward receptors across multiple ecological-shift lineages — **inconclusive — optimiser-sensitive** after randomised-starting-$\omega$ diagnostic on all 6 production clades [@anisimova2007branchsite, 30 codeml runs]: **0 robust positives + 3 optimiser-sensitive + 3 robust null** across 6 production clades after diagnostic (Apis Gr_sweet, dmel Gr64 cluster, dmel all-Grs all show boundary-escape behaviour with foreground $\omega$ in the small-clade boundary-artefact range, $\omega > 30$ on $n \le 7$ taxa). The pipeline is validated by reproducing the @baldwin2014hummingbird hummingbird TAS1R1 control at LRT = 55.9, $p < 4 \times 10^{-14}$; the failure mode is insufficient method power on the 38-taxon × 3,234-codon Gr_sweet alignment with small foreground clades, not confirmed absence of selection. The same dataset confirms widespread *existence*: 114 PRISMA-screened cases across 7 phyla and 56 species satisfy the F1–F4 operational criteria, and four trans-ancestry Mendelian-randomization chains anchor the phenomenon at the *Homo sapiens* tip (meta OR 1.12–1.41, all $p < 10^{-3}$). Sweet Trap exists widely but does not behave as a phylogenetically inherited, molecularly shared, or universally selected trait. We interpret this as supporting a *lineage-specific origins* model, with Paper 2 designed to identify the triggering ecological conditions (HIREC severity, generation time, gene-family pre-conditions) on an independent corpus.

**Scope-fit for *Royal Society Open Science*.** RSOS explicitly welcomes pre-registered null results, replication, and falsification papers — this manuscript is exactly that genre. We provide three falsified universality predictions, each with a quantitative pre-registered threshold, an explicit falsification band, and a matched alternative reading (Type II error vs lineage-specific origins) reported in the Discussion. The manuscript is structurally multidisciplinary: evolutionary biology (phylogenetic comparative methods, branch-site selection scans), comparative behaviour (PRISMA-ScR animal-case corpus across 7 phyla), molecular evolution (Pfam-domain architecture comparison, codon alignments), and human genetic epidemiology (trans-ancestry Mendelian randomization). The integration would not be possible by any single subdiscipline. RSOS's open-science mission — publishing rigorous research regardless of result direction — is the natural home for a paper whose primary contribution is a transparent refutation of a popular construct in its strong form. All three pre-registered universality predictions ($K > 0.30$; Jaccard $\ge 0.70$; $\ge 1$ positive-selected gene-lineage pair at Bonferroni-corrected significance) are deposited verbatim in our OSF pre-registration (<https://osf.io/pv3ch/>, deposited 2026-04-24 03:16 UTC, public node). We invite reviewers to download the 168 KB `sweet_trap_v4_stage6_preregistration.zip` and verify each pre-registered threshold against our reported outcomes — including the diagnostic-augmented downgrade of H6a from a strict pre-registered pass to INCONCLUSIVE.

**Author signal disclosure.** Both corresponding authors are early-career; both ORCIDs are 0009- (Lu An: 0009-0002-8987-7986; Hongyang Xi: 0009-0007-6911-2309); no senior co-author is on the byline. We mention this explicitly because RSOS's merit-based publishing model and open peer-review options are well suited to early-career-led submissions where evaluation rests on the rigor of the methods and the transparency of the analysis rather than on author seniority. We have committed our priority deposits (bioRxiv + OSF) on 2026-04-24 ahead of submission. The Methods and Supplementary Materials disclose all 9 entries of our deviation log in full, and we welcome adversarial peer review on every line.

**Why now.** Reward-fitness decoupling is increasingly invoked across multiple active discourses: ultra-processed food and the WHO/FAO 2024–2025 NOVA consultation, artificial light at night and IDA/IUCN-aligned policy frameworks, algorithmically-engineered digital feeds and the EU Digital Services Act, and the broader evolutionary-biology debate over sensory exploitation and ecological traps. A pre-registered falsification of the *universal* version of the construct — establishing that reward-fitness decoupling is a recurrently re-derived ecological vulnerability rather than a shared inherited trait — provides a sharper foundation for the lineage-specific Paper 2 work that several of these policy domains will require. Submission is timed against active multi-disciplinary attention to "engineered reward" environments.

**Data, code, and reproducibility.** All data, codon alignments, time-calibrated trees, codeml run directories, and analysis scripts are deposited on OSF (<https://osf.io/pv3ch>), with a GitHub mirror to be supplied at submission ([TBD-fill-on-submission]). The full manuscript is reproducible via a single `make` command in `05-manuscript/` (Markdown source → DOCX/PDF/HTML via pandoc). Both authors are corresponding and accept accountability for the work.

We are grateful for *Royal Society Open Science*'s consideration.

Sincerely,

**Lu An** (co-corresponding)
Department of Mammary Gland, Chongqing Health Center for Women and Children
Department of Mammary Gland, Women and Children's Hospital of Chongqing Medical University
Email: 113781@hospital.cqmu.edu.cn · ORCID: 0009-0002-8987-7986

**Hongyang Xi** (co-corresponding)
Department of Mammary Gland, Chongqing Health Center for Women and Children
Department of Mammary Gland, Women and Children's Hospital of Chongqing Medical University
Email: 26708155@alu.cqu.edu.cn · ORCID: 0009-0007-6911-2309
