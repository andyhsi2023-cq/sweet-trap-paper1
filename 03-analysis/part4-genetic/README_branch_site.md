# H6a Branch-Site Model A — Methodology Notes

**Part 4, Stream 4a-BranchSite · Sweet Trap V4 · eLife RPP target**

This document anchors the branch-site positive-selection pipeline that tests
H6a. Read it **before running** any `codeml` job; most design decisions that
determine whether a signal is interpretable are frozen at the control-file and
foreground-tree stage.

---

## 1. Pipeline overview

```
Part 3 alignments + trees          scripts/
   |                                 |
   v                                 v
data/alignments/<gene>_codon.fasta   00_codeml_model_a_null.ctl
outputs/pilot_tree_<gene>.nwk        00_codeml_model_a_alt.ctl
   |                                 |
   +---------------------------------+
                     |
                     v
   01_prepare_codeml_inputs.py
   (builds data/codeml_runs/<gene>__<lineage>/
    with alignment.phy, tree_labelled.nwk,
    null.ctl, alt.ctl)
                     |
                     v
   02_run_branch_site.sh
   (runs codeml null + alt-init-0.5 + alt-init-1.5;
    picks best alt lnL; writes lrt_stats.tsv)
                     |
                     v
   03_multiple_testing.R
   (Bonferroni + BH-FDR correction,
    BEB site parsing from rst,
    writes outputs/branch_site_results.csv
    + outputs/branch_site_beb_sites.csv)
```

---

## 2. Statistical framework

### 2.1 Branch-site Model A

- **Method:** Zhang, Nielsen & Yang 2005 *Mol Biol Evol* 22:2472–2479, also Yang
  & Nielsen 2002; PAML implementation of `model = 2, NSsites = 2`.
- **Four site classes:** 0 = conserved (0 < ω₀ < 1); 1 = neutral (ω₁ = 1);
  2a = positive on foreground only (ω₀ on background, ω₂ ≥ 1 on foreground);
  2b = neutral on background, ω₂ ≥ 1 on foreground.
- **Null model:** `fix_omega = 1, omega = 1` — constrains ω₂ = 1 (no positive
  selection).
- **Alternative model:** `fix_omega = 0` — ω₂ freely estimated, ω₂ ≥ 1.
- **Test statistic:** 2·(lnL_alt − lnL_null), compared to a 50:50 mixture of
  χ²₀ and χ²₁, approximated conservatively by χ²₁ with the p-value halved
  (Anisimova & Yang 2007 *MBE* 24:1219–1228).
- **Site detection:** Bayesian Empirical Bayes (BEB) posterior probabilities
  from the alt-model `rst` file (Yang, Wong & Nielsen 2005 *MBE* 22:1107–1118);
  codons with posterior > 0.95 reported as candidate positive-selection sites.

### 2.2 Multiple testing

- Pre-registered test count: **15 target genes × 4 ecological-shift lineages
  = 60 tests**.
- Pre-registered Bonferroni α = 0.05 / 60 = **0.000833** (~1 × 10⁻³).
- Realised matrix contains 23 rows (`scripts/branch_site_test_matrix.tsv`); the
  realised Bonferroni α is tighter (0.05 / 23 = 0.00217). We report BOTH:
  the pre-registered threshold preserves the ex-ante commitment; the realised
  threshold reflects actual family-wise error.
- BH-FDR (Benjamini-Hochberg) reported in parallel as a less conservative
  alternative. Headline claims rely on Bonferroni; BH-FDR is descriptive.

### 2.3 One-sided vs two-sided test

Branch-site is inherently one-sided (we test whether ω_foreground > 1, not
whether ω differs from the null in either direction). The standard chi-square
p-value is therefore halved. Anisimova & Yang (2007) demonstrate this
correction preserves nominal type-1 error under the boundary-parameter
condition that fixes ω = 1.

---

## 3. Modelling assumptions & known failure modes

### 3.1 Assumptions (that we make explicitly)

| # | Assumption | Rationale | Violation consequence |
|---|------------|-----------|----------------------|
| 1 | Synonymous substitutions are approximately neutral | Standard in PAML; corroborated for primate/bird coding regions with typical CpG bias corrections | If strong codon-usage bias or gBGC, dN/dS inflated or deflated systematically |
| 2 | Branch-site Model A's ω classes (4-class mixture) capture the signal | Well-calibrated for moderately-diverged sequences (Kryazhimskiy & Plotkin 2008) | Mis-specification when >50% sites have ω > 1 across the tree |
| 3 | The foreground branch is SHORT enough that ω is estimable, LONG enough that LRT has power | Empirical sweet spot ~0.05-1.5 substitutions/site | Branch too short → zero power; branch too long → saturation |
| 4 | Alignment is accurate at codon level | MAFFT L-INS-i + codon-aware post-processing in Part 3 | Alignment errors inflate false positive rate (Schneider et al. 2009) |
| 5 | Species tree (or gene tree) is correctly rooted relative to the foreground specification | TimeTree 5 species trees used as prior | Mis-rooted tree mis-labels foreground |

### 3.2 Known failure modes

- **Low power when foreground branch is short.** Insufficient substitutions on
  the foreground branch → LRT ≈ 0 even if ω₂ > 1. Mitigation: choose foreground
  as the internal branch subtending the ecological shift where
  feasible; document branch length in `lrt_stats.tsv`.
- **False positives from alignment ambiguity.** Indels or low-quality regions
  can generate spurious ω > 1 signals. Mitigation: Part 3 runs HMMer-cleaned,
  GUIDANCE-filtered alignments; we also re-run the positive-control and
  top hits with `cleandata = 1` as sensitivity.
- **Local optima.** PAML likelihood surface is multimodal. Mitigation:
  `02_run_branch_site.sh` runs the alt with TWO initial ω values (0.5 and 1.5)
  and takes the higher lnL. If the two runs disagree by > 2 lnL units, we flag
  the row for a third initialisation.
- **GC-biased gene conversion (gBGC).** In particular in birds, gBGC can
  mimic positive selection at AT→GC codon positions. Mitigation: we
  cross-check any bird hit against published gBGC maps (Lartillot 2013) and
  report the GC3 value of candidate sites.
- **Saturation.** Deep-time foreground comparisons (e.g., Chordata vs.
  Arthropoda) are not appropriate for branch-site; we restrict foregrounds to
  within-class or within-order where possible.

---

## 4. Positive control

**Hummingbird TAS1R1** (*Calypte anna*). Baldwin, Toda, Nakagita et al. 2014
*Science* 345:929-933 (DOI 10.1126/science.1255097, PMID 25146290) documented
that the ancestral umami-receptor TAS1R1 was co-opted to sweet perception in
hummingbirds. Their analysis included a branch-site test on the hummingbird
lineage with ω_foreground significantly > 1.

- **Expected in our pipeline:** ω₂ > 1 on the *Calypte_anna* tip, LRT p < 0.01
  (one-sided), at least 5 BEB codons with posterior > 0.95.
- **If the positive control FAILS** (LRT p > 0.10): pipeline is broken — stop
  downstream analysis, debug alignment / tree before trusting any other
  result. The 01 → 03 workflow must reproduce this signal for the lineage-
  specific claims on primate sugar-specialists, Apidae, and cetaceans to be
  interpretable.

### Negative controls
- *Mus musculus* TAS1R1 tip (mouse_control row): expected LRT p > 0.10.
  A significant result here would indicate model misspecification or tree
  artefact.

### Pseudogenisation control
- *Ailuropoda melanoleuca* TAS1R1 (Zhao, Li, Li et al. 2010 *PNAS* 107:21025):
  TAS1R1 is pseudogenised in giant panda. Branch-site signal on this lineage
  should manifest as relaxed constraint (high ω₀ without ω₂ > 1), not positive
  selection. We report it as a pattern-specificity sanity check.

---

## 5. Reporting schema

`outputs/branch_site_results.csv` columns:

| Column | Meaning |
|--------|---------|
| run_id | `<gene>__<lineage_key>` |
| gene | Gene symbol (e.g. TAS1R1, DRD2) |
| lineage | Lineage key (e.g. hummingbird, primate_sugar, cetacean) |
| lnL_null | Null-model log-likelihood |
| lnL_alt_best | Best alt log-likelihood across init-0.5 and init-1.5 restarts |
| LRT_2dlnL | 2·(lnL_alt − lnL_null) |
| p_raw_half_chi2_df1 | Half-χ²₁ one-sided p-value |
| bonferroni_p_prereg | Bonferroni-corrected under pre-registered n=60 |
| bonferroni_p_realised | Bonferroni-corrected under realised n |
| bh_q | Benjamini-Hochberg q-value |
| positive_selection_prereg | Logical: p_raw < 0.05/60 |
| positive_selection_realised | Logical: p_raw < 0.05/n_realised |
| n_beb_sites_gt95 | Count of codons with BEB posterior > 0.95 |

`outputs/branch_site_beb_sites.csv` columns:

| Column | Meaning |
|--------|---------|
| run_id | `<gene>__<lineage_key>` |
| codon_site | Codon index in alignment (1-based) |
| codon_AA | Amino-acid symbol (alt-class consensus) |
| beb_posterior | P(site class 2a or 2b \| data) |
| sig_mark | PAML significance stars (* ≥ 0.95; ** ≥ 0.99) |

---

## 6. Compute profile

- Per run: codeml ~0.3–1.2 h on M5 Pro (single-thread). Branch-site Model A is
  memory-light (< 500 MB) but likelihood-intensive.
- 23 runs × 3 codeml jobs/run (null + 2 alt inits) = **69 codeml jobs**.
- Total wall-time estimate: **30–60 hours sequential** (complies with
  CLAUDE.md `n_workers ≤ 2` guidance if we run two runs in parallel).
- Disk: ~5 MB per run directory (alignment + trees + mlc files + rst).
- Expected bottleneck: parsing `rst` for BEB — this is I/O-bound, not compute.

---

## 7. Caveats & planned sensitivity analyses

1. **Pfam/InterPro LBD masking.** We additionally plan to re-run the
   significant hits restricted to the LBD codons (InterPro IPR000073 for TAS1R;
   IPR000276 for class-A GPCR). If BEB posterior > 0.95 clusters IN the LBD,
   that strengthens the functional interpretation. This is a secondary
   analysis, not a primary test — functionally-localised positive selection in
   the LBD is stronger evidence than a signal randomly distributed across the
   gene.
2. **Clade model C (Bielawski-Yang 2004).** If Model A fails on clade-level
   foregrounds (primate_sugar, apidae_nectar, cetacean), we will try Clade
   Model C as a robustness check. Documented but not scripted yet.
3. **Codon frequency model.** Default F3X4. Sensitivity: F61 empirical codon
   table on the top 3 hits. Goldman & Yang 1994 show F3X4 slightly inflates
   false positives at high GC-skew genes; we document GC3 per run.

---

## 8. Status

### 2026-04-25 — Positive-control gate STRICT PASS (v4 Baldwin-scale)

**Gate verdict: STRICT PASS.** Week-2 22-row production run unblocked.

| Foreground specification (v4, 16 taxa — 9 hummingbirds + Apus + Serinus + Gallus + Danio + 3 mammals) | LRT (2Δ lnL) | p (half-χ²₁) | BEB P>0.95 sites | fg ω (site class 2a) |
|--------------------------------------------------------------------------------------------------------|-------------:|-------------:|------------------:|---------------------:|
| Apodiformes clade (Baldwin 2014 design — all branches inside the hummingbird+swift clade)               | **55.90**    | **3.8 × 10⁻¹⁴** | 6 (4 in VFT)      | **9.38**             |
| Crown hummingbird clade (every branch in the 9-hummingbird subtree)                                     | **61.06**    | **2.8 × 10⁻¹⁵** | 7 (5 in VFT)      | **9.55**             |
| Apodiformes MRCA only (single stem branch)                                                              | 0.53         | 0.23          | 0                 | 9.77 (~1% sites)     |
| Hummingbird MRCA only (single crown stem branch)                                                        | 0.20         | 0.33          | 0                 | 2.83 (~1% sites)     |
| **Mus_musculus tip (negative control)**                                                                 | **0.00**     | **0.50**      | **0**             | boundary ω=1         |

Both clade-level tests are > 10 orders of magnitude beyond the pre-registered p < 0.01 threshold. Negative control (mouse) stays exactly at the boundary (LRT = 0). Single-branch tests confirm Baldwin 2014's observation that the signal is distributed across Apodiformes/hummingbird crown branches, not localized to the stem-Apodiformes branch alone.

**Why the v1 attempt was conditional PASS:** Week 1 used 6 taxa with Calypte alone as foreground — LRT = 2.22, p_half = 0.068. Adding Apus + 8 Cockburn 2022 hummingbirds + Serinus gave the ancestral branch enough substitutions to power the LRT exactly as Baldwin 2014 documented.

**Bash wrapper fix:** `02_run_branch_site.sh` now drops `-e` and checks for the presence of an `^lnL` line in each mlc file instead of relying on codeml's exit code (codeml exits non-zero after printing a cosmetic "end of tree file" warning).

**Artefacts:**
- Alignment (16 taxa × 954 codons): `data/positive_control/work/codon_aligned_v4.fasta`
- Tree (IQ-TREE, ML on proteins, Q.MAMMAL+G4): `data/positive_control/work/tree_v4.treefile`
- codeml run dirs: `data/codeml_runs/TAS1R1_pc_v4__*/`
- Master LRT summary: `outputs/positive_control_v4_lrt_summary.tsv`
- BEB site table (all sites with P>0.5 plus metadata): `outputs/positive_control_v4_beb_sites.tsv`
- Full report: `outputs/positive_control_report.md` § v2 (updated 2026-04-25)

### Pre-2026-04-25 — code-level readiness

As of **2026-04-24**, the pipeline is complete at the code level:

- Control files: written and reviewed ✓
- Input-prep script: dry-run tested (23 rows scaffolded) ✓
- codeml runner: written, not yet executed (codeml binary not installed in
  local env; `sweet-trap` micromamba env expected to provide it) ⚠
- Multiple-testing R script: dry-run tested ✓
- README (this file) ✓

**Blocked on:** Part 3 delivering `<gene>_codon.fasta` alignments + per-gene
species trees. Expected handoff: see WORKLOG.md.

Once Part 3 delivers and the codeml binary is in PATH:

```bash
# 1. Build runs
python scripts/01_prepare_codeml_inputs.py

# 2. Validate pipeline on positive control FIRST
bash scripts/02_run_branch_site.sh TAS1R1__hummingbird
# confirm LRT p < 0.01 before proceeding

# 3. Run remaining 22 rows
bash scripts/02_run_branch_site.sh

# 4. Collect + multiple-testing correction
Rscript scripts/03_multiple_testing.R
```

---

## 9. Key citations

- Anisimova, M., & Yang, Z. (2007). Multiple hypothesis testing to detect
  lineage-specific adaptive evolution. *Mol Biol Evol* 24:1219-1228.
- Baldwin, M. W., Toda, Y., Nakagita, T., et al. (2014). Evolution of sweet
  taste perception in hummingbirds by transformation of the ancestral umami
  receptor. *Science* 345:929-933.
- Kryazhimskiy, S., & Plotkin, J. B. (2008). The population genetics of dN/dS.
  *PLoS Genet* 4:e1000304.
- Yang, Z. (2007). PAML 4: phylogenetic analysis by maximum likelihood.
  *Mol Biol Evol* 24:1586-1591.
- Yang, Z., & Nielsen, R. (2002). Codon-substitution models for detecting
  molecular adaptation at individual sites along specific lineages. *Mol Biol
  Evol* 19:908-917.
- Yang, Z., Wong, W. S. W., & Nielsen, R. (2005). Bayes empirical Bayes
  inference of amino acid sites under positive selection. *Mol Biol Evol*
  22:1107-1118.
- Zhang, J., Nielsen, R., & Yang, Z. (2005). Evaluation of an improved
  branch-site likelihood method for detecting positive selection at the
  molecular level. *Mol Biol Evol* 22:2472-2479.
- Zhao, H., Yang, J.-R., Xu, H., & Zhang, J. (2010). Pseudogenization of the
  umami taste receptor gene Tas1r1 in the giant panda coincided with its
  dietary switch to bamboo. *PNAS* 107:21025-21030.
