# Part 4 — Genetic Causality (Paper 1 lightweight)

Sweet Trap V4 · eLife Reviewed Preprint target · 2026-04-24

This directory executes **Part 4** of the Sweet Trap V4 evidence architecture
(see `00-design/stage6-evolutionary-reframing/evidence_architecture_v4.md §5`).
Two hypotheses are tested:

- **H6a** — Lineage-specific positive selection on reward-receptor LBDs
  (PAML branch-site Model A, 15 genes × ≥ 4 ecological-shift lineages).
- **H6f** — Cross-species genetic-manipulation literature summary
  (scoping review of ~30-50 experimental papers across ≥ 3 phyla).

Four further gene-level hypotheses (**H6b GxE / H6c cross-species parallel
selection / H6d PRS discriminant validity / H6e recent-human selection scan**)
are **announced as Paper 2 roadmap** but *not executed in Paper 1*.

---

## Environment activation (required before running any script)

PAML, mafft, iqtree, raxml-ng, hmmer, muscle, orthofinder are installed in
`tools/mamba-root/envs/sweet-trap/bin/` but **not on system PATH**.
Source the activator before any run:

```bash
source /Users/andy/Desktop/Research/sweet-trap-multidomain/tools/activate_env.sh
codeml -v   # sanity check
```

(Python 3.14 work that only needs biopython/scipy/pandas can use `venv-phylo/`
instead — see Part 3 README.)

---

## Directory layout

```
03-analysis/part4-genetic/
├── README.md                          # this file
├── README_branch_site.md              # H6a methodology + assumptions
├── scripts/
│   ├── 00_codeml_model_a_null.ctl     # H6a null model template
│   ├── 00_codeml_model_a_alt.ctl      # H6a alt model template
│   ├── 01_prepare_codeml_inputs.py    # build per-run codeml dirs
│   ├── 02_run_branch_site.sh          # drive codeml null + alt runs
│   ├── 03_multiple_testing.R          # Bonferroni + BH + BEB parsing
│   ├── 04_h6f_pubmed_harvest.py       # PubMed 9-query harvest
│   ├── 05_h6f_triage_pilot.py         # triage full harvest -> pilot 80-150
│   └── branch_site_test_matrix.tsv    # 23 (gene, lineage) rows for H6a
├── data/
│   └── codeml_runs/<gene>__<lineage>/ # per-run codeml input bundles (dry-run)
├── outputs/
│   ├── H6f_search_strategy.md         # pre-registered search protocol
│   ├── H6f_extraction_template.csv    # 20-column coding schema
│   ├── H6f_full_harvest.csv           # raw 4,066 PubMed records (full harvest)
│   ├── H6f_pilot_hit_list.csv         # triaged 125-row pilot for Week-2 screening
│   ├── H6f_phylum_coverage.md         # per-phylum coverage report
│   └── (post-run) branch_site_results.csv, branch_site_beb_sites.csv,
│                  branch_site_summary.md
└── logs/
    ├── 01_prepare_codeml_inputs_*.log
    ├── 01_prepare_summary.tsv
    ├── 04_h6f_pubmed_harvest_*.log
    └── 05_h6f_triage_pilot_*.log
```

---

## Status (2026-04-24)

### H6a branch-site pipeline

| Deliverable | Status |
|---|---|
| 1a. null.ctl template | WRITTEN |
| 1b. alt.ctl template | WRITTEN |
| 1c. 01_prepare_codeml_inputs.py | WRITTEN (dry-run tested, 23 run dirs scaffolded) |
| 1d. 02_run_branch_site.sh | WRITTEN (not executed; codeml binary not yet on PATH) |
| 1e. 03_multiple_testing.R | WRITTEN (dry-run tested, outputs/branch_site_results.csv emitted with 3-row placeholder) |
| 1f. README_branch_site.md | WRITTEN |
| Positive control row (hummingbird TAS1R1) | Present in test matrix (row 1) |
| **BLOCKED ON:** | (a) Part 3 delivering `<gene>_codon.fasta` alignments + per-gene species trees; (b) codeml binary on PATH (expected from micromamba env `sweet-trap`). |

### H6f literature synthesis

| Deliverable | Status |
|---|---|
| 2a. Search strategy document | WRITTEN + pre-registered |
| 2b. Extraction template CSV | WRITTEN (20-column schema) |
| 2c. Pilot hit list | **EXECUTED**: 125 PMIDs across 8 phylum buckets |
| 2d. Phylum coverage report | WRITTEN |
| Full harvest reservoir | **EXECUTED**: 4,066 unique PMIDs |
| Canonical anchor verification | Johnson-Kenny 2010 (Drd2) + de Bono 1998 (NPR-1) confirmed in pilot |

---

## H6f harvest results (live)

Full-harvest counts per query (PubMed, 1995-04-24 to 2026-04-30):

| Query | Candidate phylum | Raw hits |
|-------|-----------------|----------|
| Q-vertebrate-rodent | Chordata (rodent) | 3,338 |
| Q-mollusc | Mollusca | 138 |
| Q-arthropod-bee | Arthropoda (Hymenoptera) | 81 |
| Q-nematode | Nematoda | 54 |
| Q-cnidarian | Cnidaria | 21 |
| Q-arthropod-drosophila | Arthropoda (Drosophila) | 19 |
| Q-vertebrate-primate-other | Chordata (non-rodent) | 16 |
| Q-reward-fitness-decoupling | cross-phylum | 11 |
| Q-supernormal-manipulation | cross-phylum | 1 |
| **TOTAL (dedup)** | | **4,066** |

Triaged pilot (applies title-keyword boost, year weights, per-phylum caps,
and force-inclusion of canonical anchors):

| Phylum bucket | Pilot retained |
|---|---|
| Chordata (rodent) | 35 |
| Arthropoda (Drosophila) | 15 |
| Arthropoda (Hymenoptera) | 15 |
| Mollusca | 15 |
| Nematoda | 15 |
| Cnidaria | 12 |
| Chordata (non-rodent) | 10 |
| cross-phylum | 8 |
| **TOTAL** | **125** |

The triaged pilot sits at the middle of the 80-150 target window with all 8
buckets populated (including the load-bearing Nematostella cnidarian bucket).

---

## Execution recipe (post-Part-3 handoff)

```bash
# -- Activate the sweet-trap env (provides codeml, mafft, iqtree, etc.) --
micromamba activate sweet-trap

# -- H6a: Part 3 must have delivered these first --
ls ../part3-molecular/data/alignments/*_codon.fasta
ls ../part3-molecular/outputs/pilot_tree_*.nwk

# 1. Build codeml input bundles (23 runs)
python scripts/01_prepare_codeml_inputs.py

# 2. Sanity-check with positive control BEFORE running the rest
bash scripts/02_run_branch_site.sh TAS1R1__hummingbird
# If LRT p < 0.01 -> pipeline validated. If not -> debug Part 3 alignment.

# 3. Run the remaining 22 (sequential, ~30-60 h wall time on M5 Pro)
bash scripts/02_run_branch_site.sh

# 4. Multiple-testing correction + BEB site extraction
Rscript scripts/03_multiple_testing.R
# -> outputs/branch_site_results.csv
# -> outputs/branch_site_beb_sites.csv
# -> outputs/branch_site_summary.md

# -- H6f (network-only, already executed) --
# Re-run if the query library needs updating:
python scripts/04_h6f_pubmed_harvest.py --max-per-query 4000
python scripts/05_h6f_triage_pilot.py
```

---

## Week-2 handoff plan

### What Part 3 owes Part 4

- `data/alignments/<gene>_codon.fasta` for each of the 15 target genes,
  codon-aligned, with taxa matching the H6a species set (see
  `scripts/branch_site_test_matrix.tsv` for the expected taxon list).
- `outputs/pilot_tree_<gene>.nwk` per-gene species tree in Newick, or (fallback)
  `outputs/species_tree.nwk` as a common species tree.

### What Part 4 will do once handed off (execution window)

| Day | Task |
|---|---|
| Day 1 | Run 01_prepare_codeml_inputs.py against real alignments; spot-check taxon names vs matrix. |
| Day 2 | Run hummingbird TAS1R1 positive control first. If LRT p < 0.01, greenlight. |
| Days 3-6 | Run remaining 22 branch-site runs sequentially (two at a time; `n_workers ≤ 2`). |
| Day 7 | Collect + Bonferroni/BH correction via 03_multiple_testing.R. |
| Day 8 | Regenerate Figure 4 (lineage-x-gene p-value heatmap; see evidence_architecture_v4 §5.2). |

### What Part 4 is doing in parallel (network / no blocker)

| Day | Task |
|---|---|
| Day 1 | (today) Full PubMed harvest + triage to pilot. DONE. |
| Days 2-4 | Title + abstract screening of 125 pilot rows (2 blinded coders). |
| Days 5-8 | Full-text extraction + coding per extraction template. |
| Day 9 | Double-coding 20 % sub-sample for kappa. |
| Day 10 | H6f summary table + directional-consistency binomial test + Table 4 draft. |

---

## Top 3 risks

1. **Part 3 alignment quality could inflate H6a false positives.** If Part 3
   delivers noisy multi-sequence alignments for TAS1R or Gr genes (paraphyletic
   across phyla with poor codon alignment), the branch-site test picks up
   alignment artefacts as "positive selection". **Mitigation**: (a) Part 4
   sensitivity re-runs with `cleandata = 1`; (b) BEB site cluster analysis
   vs LBD mask to confirm functional localization; (c) hummingbird TAS1R1
   positive-control gate — if it doesn't reproduce Baldwin 2014, pipeline
   fails sanity and we stop.

2. **Cnidarian coverage thin for H6f.** Full harvest returned 21 Cnidaria raw
   hits; pilot has 12; full-text attrition likely leaves 0-2 usable
   manipulation studies. If we land at 0, the "≥ 3 phyla" H6f criterion
   tightens and we fall back to Chordata + Arthropoda + Nematoda coverage
   (still passes minimum). **Mitigation**: manual reference-list trawl of
   Layden & Martindale 2014 *Nematostella* neuropeptide literature and
   Anderson et al. 2020 cnidarian behavioural reviews. Flagged for Week-2.

3. **codeml binary not yet installed in the local Python environment.** The
   project description states `micromamba env sweet-trap` has codeml, but
   `micromamba` is not currently installed on this machine and the
   `venv-phylo/` virtualenv contains only Biopython/ete3, not PAML.
   **Mitigation**: before Part 3 handoff, install PAML either via
   `brew install paml` or via `conda install -c bioconda paml` or manual build
   from `https://github.com/abacus-gene/paml`. The 02_run_branch_site.sh script
   fails fast (exit 1) with a clear diagnostic if codeml is not on PATH.

---

## Key files for code review

- Statistical correctness: `scripts/03_multiple_testing.R` — half-chi-square
  p-value handling, Bonferroni alpha at pre-registered n=60 AND realised n,
  BH-FDR as alternative.
- Reproducibility: `outputs/H6f_search_strategy.md` + `scripts/04_h6f_pubmed_harvest.py`
  — every PubMed query is version-controlled and re-runnable.
- Positive control: `scripts/branch_site_test_matrix.tsv` row 1 (hummingbird
  TAS1R1, Baldwin 2014 replication target).

---

*For methodology details on branch-site Model A, see `README_branch_site.md`.*
*For H6f search strategy and inclusion/exclusion rules, see `outputs/H6f_search_strategy.md`.*
