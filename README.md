# Sweet Trap v4 Paper 1

**Title**: *Sweet Trap is widespread but not universal: a pre-registered cross-metazoan falsification of reward-fitness decoupling as a shared evolutionary trait*

**Authors**: Lu An & Hongyang Xi (co-corresponding, equal contribution)
**Target journal**: Royal Society Open Science (RSOS)
**Priority anchors**:
- bioRxiv: [BIORXIV/2026/720498](https://www.biorxiv.org/) (deposited 2026-04-24)
- OSF pre-registration: [https://osf.io/pv3ch/](https://osf.io/pv3ch/) (deposited 2026-04-24 03:16 UTC)

## Headline finding

We pre-registered three sharp predictions of universality for reward-fitness decoupling across Metazoa. **All three are not supported by our data**:

| Layer | Prediction | Outcome |
|---|---|---|
| L1 Existence | F1+F2-passing N ≥ 50 spanning ≥ 6 phyla | **SUPPORTED** (114 cases / 7 phyla / 56 species) |
| L2 Phylogenetic signal | Blomberg K > 0.30 (≥ 80% posterior under A1–A4) | **REFUTED** (K = 0.117, p = 0.251) |
| L3 Shared molecular substrate | Pfam Jaccard ≥ 0.70 vs matched-random ≤ 0.30 | **NOT ENRICHED** (Jaccard = 0; P(=0\|null) = 0.9998) |
| L4 Universal positive selection | ≥ 1 positive-selected gene on ≥ 1 lineage at Bonferroni-corrected significance | **INCONCLUSIVE** (3 robustly null + 3 optimiser-sensitive + 0 robust positives after Yang & dos Reis 2011 diagnostic) |

**Synthesis**: Sweet Trap is **widespread but not universal** — a recurring, lineage-specific outcome rather than a phylogenetically inherited trait or a universal molecular-substrate-shared phenomenon.

## Repository layout

```
00-design/      research design, hypotheses, evidence architecture, Stage-7 audits
01-literature/  competing-literature maps + collision scans
02-data/        ※ raw + processed cohort data deposited on OSF (gitignored)
03-analysis/    Part 1 MR | Part 2 PRISMA + phylosig | Part 3 molecular | Part 4 codeml
04-figures/     Fig 1–5 + FigS1, all 600 dpi (PDF + PNG + SVG) + R scripts
05-manuscript/  manuscript.md, references.bib, cover_letter.md, rsos_submission_form.md, title_page.md
```

## Reproducibility

```bash
cd 05-manuscript
make clean && make && make lint
```

Produces `manuscript.docx` from `manuscript.md` + `references.bib` + figures via pandoc + pandoc-crossref + citeproc + elife.csl.

For codeml branch-site reproduction:

```bash
source tools/activate_env.sh   # PAML, mafft, iqtree, raxml-ng on PATH
python 03-analysis/part4-genetic/scripts/optimizer_diagnostic/run_optimizer_diagnostic.py
```

(Note: `tools/` is a 3.6 GB micromamba environment — installed from `tools/mamba-root/` recipes, not version-controlled.)

## Pre-registration verification

The OSF deposit `sweet_trap_v4_stage6_preregistration.zip` (168 KB, deposited 2026-04-24 03:16 UTC) contains 19 stage6 design documents with all three universality predictions verbatim:

- H3 K > 0.30 prediction: `bioRxiv_priority_preprint_draft.md` + `path_B_formal_model_H3.md`
- H4b Jaccard ≥ 0.70: `bioRxiv_priority_preprint_draft.md` + `evidence_architecture_v4.md`
- H6a ≥ 1 gene-lineage pair: `gantt_12_weeks.md` Gate-1 row

API verifiable: <https://api.osf.io/v2/nodes/pv3ch/>

## Deviations log

9 deviation rows documented in §2.6 of `manuscript.md`, including:
- H3 primary prediction failed (K=0.117 below predicted zone)
- H6a softened from "tentatively supported" to "INCONCLUSIVE" after optimiser-boundary diagnostic
- C-path framing pivot from convergence claim to widespread-but-not-universal falsification

## License

CC-BY 4.0 for manuscript and figures. MIT for code. See `LICENSE` for details.

## Contact

Hongyang Xi — `26708155@alu.cqu.edu.cn`
Lu An — `113781@hospital.cqmu.edu.cn`
