# Part 1 — Trans-ancestry Mendelian Randomisation (Sweet Trap V4, H1c)

**Project**: sweet-trap-multidomain
**Hypothesis**: H1c — instrumenting aspirational-reward-seeking behaviours (dietary, metabolic) causally affects mortality/morbidity fitness proxies across ≥3 ancestries.
**Target venue**: eLife Reviewed Preprint
**Pipeline executed**: 2026-04-24 (Week 1 first batch)
**Owner**: Claude Opus 4.7 (hand-off brief from Andy, Stage 6 evolutionary reframing)

---

## 1. Exposure-outcome pairs

| Pair id    | Exposure                          | Exposure GWAS  | Outcome                            | Ancestries attempted |
| ---------- | --------------------------------- | -------------- | ---------------------------------- | -------------------- |
| `alc-mort` | Alcohol drinks per week (GSCAN)   | `ieu-b-73`     | All-cause mortality                | EUR, EAS             |
| `bmi-mort` | Body mass index (GIANT 2018)      | `ieu-b-40`     | All-cause mortality                | EUR, EAS, AFR, SAS, AMR |
| `sug-cvdm` | Sugar intake total (UKB self-rep) | `ukb-b-5237`   | Cardiovascular mortality (CAD proxy) | EUR, EAS           |
| `upf-mort` | Processed meat intake (UKB; UPF proxy) | `ukb-b-6324` | All-cause mortality             | EUR                  |
| `scr-mort` | Leisure screen-time: TV watching (UKB) | `ukb-b-5192` | All-cause mortality             | EUR                  |

**Instrument selection**: `TwoSampleMR::extract_instruments()`, p < 5×10⁻⁸, clump r² < 0.001, kb = 10 000 (EUR LD panel — no non-EUR clumping reference available via OpenGWAS for the exposure GWAS, all of which are EUR).

---

## 2. Outcome GWAS IDs and ancestries actually used

| Outcome                 | Ancestry | OpenGWAS ID           | Study / n                                                                 |
| ----------------------- | -------- | --------------------- | -------------------------------------------------------------------------- |
| All-cause mortality     | EUR      | `ebi-a-GCST006701`    | Pilling 2017 parental longevity (father's attained age), EUR n=415,311    |
| All-cause mortality     | EAS      | `ukb-e-4501_EAS`      | Pan-UKB EAS sub-cohort, non-accidental death in close genetic family, n=1,122 |
| All-cause mortality     | AFR      | `ukb-e-1807_AFR`      | Pan-UKB African sub-cohort, father's age at death, n=3,732                |
| All-cause mortality     | SAS      | —                     | GAP: no SAS mortality / parental-lifespan GWAS in OpenGWAS                |
| All-cause mortality     | AMR      | —                     | GAP: All of Us pending registration                                        |
| Cardiovascular mortality | EUR     | `ebi-a-GCST005194`    | van der Harst 2018 CAD meta, EUR n=296,525                                |
| Cardiovascular mortality | EAS     | `bbj-a-159`           | Ishigaki 2020 BBJ CAD, EAS n=212,453                                      |

**Correction note**: the initial mapping used `ebi-a-GCST006414` as the "EUR all-cause mortality" GWAS. On verification this ID is **Nielsen 2018 Atrial fibrillation**, not mortality. Results with the correct ID (`ebi-a-GCST006701`) are reported here; the earlier mislabeled run has been purged from `outputs/`.

---

## 3. Software and versions

R 4.5.3 (2026-03-11) "Reassured Reassurer" on macOS 26.4 / Apple M5 Pro.

| Package                 | Version |
| ----------------------- | ------- |
| TwoSampleMR             | 0.7.4   |
| MendelianRandomization  | 0.10.0  |
| ieugwasr                | 1.1.0   |
| MRPRESSO                | 1.0     |
| MVMR                    | 0.4.4   |
| coloc                   | 5.2.3   |
| RadialMR                | 1.2.2   |
| metafor                 | 4.8.0   |
| data.table / dplyr / tidyr / tibble / purrr | CRAN current (Apr 2026) |

**OpenGWAS JWT token** is required (mrcieu API post-2024-05). Stored in `.Renviron` at project root; loaded into `OPENGWAS_JWT` env var by `00_environment.R`.

**renv status**: the project `renv` library does NOT contain the MR toolchain; all MR packages live in the system library at `/opt/homebrew/lib/R/4.5/site-library`. Scripts prepend that to `.libPaths()` at the top of `00_environment.R`.

---

## 4. Scripts (execute in order)

```
scripts/
├── 00_environment.R            # libraries, seeds, paths, pair/outcome tables
├── 01_instruments.R            # IV extraction per exposure
├── 02_outcomes.R               # outcome extraction + harmonisation per (pair × ancestry)
├── 03_mr_main.R                # IVW / Egger / WM / Mode / PRESSO / Steiger / LOO / Radial
├── 04_trans_ancestry_meta.R    # metafor random-effects meta across ancestries
└── 05_sensitivity.R            # F, I²_GX, Steiger-filter, Cook's D, MVMR
```

Standard invocation:

```bash
cd /Users/andy/Desktop/Research/sweet-trap-multidomain
for s in 01 02 03 04 05; do
  R --vanilla --quiet -f 03-analysis/part1-mr/scripts/${s}_*.R
done
```

End-to-end wall-clock from cold cache (OpenGWAS API round-trips included): **≈ 20–25 minutes**.

---

## 5. Outputs (all in `03-analysis/part1-mr/outputs/`)

### Primary headline
- `mr_main_week1.csv` — one row per (pair × ancestry × method). The critical first deliverable.
- `meta_trans_ancestry.csv` — trans-ancestry pooled estimates (DL / REML / FE + Q, I², τ²).

### Per-step artefacts
- `instruments_<pair>.rds` + `.csv` — exposure IV tables (after 5×10⁻⁸ + clump).
- `instruments_summary.csv` — n_SNP, F-stat per pair.
- `outcome_<pair>_<ancestry>.rds` — extract_outcome_data result.
- `harmonised_<pair>_<ancestry>.rds` — harmonise_data result (used by 03 and 05).
- `outcomes_summary.csv` / `outcomes_failed.csv` — success + failure log.
- `mr_pleiotropy.csv` — Egger intercept + Cochran Q per combo.
- `mr_steiger.csv` — directionality test result.
- `mr_radial_outliers.csv` — Radial-IVW outliers (α = 0.002 Bonferroni).
- `mr_loo_<pair>_<ancestry>.csv` — leave-one-out IVW.
- `mr_combo_summary.csv` — one row per combo: n_SNP + mean F.

### Sensitivity
- `sens_instrument_strength.csv` — F mean/min/frac<10 and I²_GX per combo.
- `sens_steiger_filtered.csv` — IVW/Egger/WM after Steiger filter.
- `sens_cooks_d.csv` — top-10 Cook's D SNPs per combo (flagged).
- `sens_mvmr.csv` — MVMR(BMI + alcohol → all-cause mortality, EUR).

### Logs
`logs/<script>.log` — timestamped per-script log (stdout + stderr + message tee).

---

## 6. Key headline statistics (post-run)

All estimates are IVW from the 2-sample MR, effect per +1 SD exposure on the outcome scale noted.

### 6.1 Per-pair IVW (and trans-ancestry meta where ≥2 ancestries)

| Pair       | Ancestry | n_SNP | β (SE)          | OR (95% CI)             | p        | F̄    |
| ---------- | -------- | ----- | --------------- | ------------------------ | -------- | ----- |
| alc-mort   | EUR      | 34    | 0.122 (0.038)   | 1.129 (1.049–1.216)     | 1.2×10⁻³ | 77.3  |
| alc-mort   | EAS      | 29    | 0.740 (0.635)   | 2.096 (0.604–7.269)     | 0.24     | 82.7  |
| alc-mort   | **meta REML (2 anc.)** | — | 0.124 (0.038)   | **1.132 (1.051–1.218)** | 9.8×10⁻⁴ | Q p=0.33, I²=0% |
| bmi-mort   | EUR      | 466   | 0.115 (0.010)   | 1.122 (1.100–1.143)     | 3.1×10⁻³¹ | 76.8 |
| bmi-mort   | EAS      | 470   | 0.098 (0.361)   | 1.102 (0.543–2.239)     | 0.79     | 76.4 |
| bmi-mort   | AFR      | 476   | 0.092 (0.097)   | 1.097 (0.907–1.325)     | 0.34     | 76.3 |
| bmi-mort   | **meta REML (3 anc.)** | — | 0.114 (0.010) | **1.121 (1.100–1.143)** | 2.0×10⁻³¹ | Q p=0.97, I²=0% |
| sug-cvdm   | EUR      | 38    | 0.313 (0.115)   | 1.368 (1.093–1.713)     | 6.3×10⁻³ | 74.5  |
| sug-cvdm   | EAS      | 33    | 0.451 (0.205)   | 1.570 (1.051–2.344)     | 0.028    | 61.6  |
| sug-cvdm   | **meta REML (2 anc.)** | — | 0.346 (0.100) | **1.414 (1.162–1.720)** | 5.4×10⁻⁴ | Q p=0.56, I²=0% |
| scr-mort   | EUR      | 108   | 0.191 (0.027)   | 1.210 (1.147–1.277)     | 3.4×10⁻¹² | 40.8 |
| upf-mort   | EUR      | 23    | -0.099 (0.053)  | 0.906 (0.816–1.006)     | 0.064    | 38.5  |

Notes:
- **"OR" for all-cause mortality uses the Pilling 2017 parental-longevity scale**; higher β means the exposure reduces parental attained age (i.e., higher mortality). Treat as log-hazard-ratio-equivalent rather than strict OR.
- **bmi-mort / scr-mort / alc-mort** consistency: all three point in the same direction across all methods (IVW, Egger, weighted median, weighted mode) in EUR.
- **upf-mort** shows a protective-looking negative estimate that is likely driven by "processed meat" being a poor UPF proxy — processed meat intake is confounded by vegetarianism/healthy-eater bias in UKB; a dedicated UPF GWAS from the NOVA food-classification framework is the Week 2 task.
- **bmi-mort / EAS/AFR under-power**: UKB-E ancestry sub-cohort mortality proxies have n=1,122 (EAS) and n=3,732 (AFR), >100× smaller than EUR (n=415,311). Meta heterogeneity I²=0% shows the estimates are *consistent* in direction; the CIs are wide simply because of power.

### 6.2 Supporting tests

| Test                       | Pair / Ancestry               | Result                            | Interpretation |
| -------------------------- | ----------------------------- | --------------------------------- | -------------- |
| Egger intercept p          | bmi-mort / EUR                | 0.65                              | No directional pleiotropy |
| Egger intercept p          | alc-mort / EUR                | 0.61                              | No directional pleiotropy |
| Egger intercept p          | sug-cvdm / EUR                | 0.91                              | No directional pleiotropy |
| Egger intercept p          | sug-cvdm / EAS                | 0.11                              | Borderline (Egger OR 2.85 vs IVW 1.57) |
| Steiger direction          | all 4 powered EUR pairs       | TRUE (p ≈ 0 for all)              | Causal direction exposure → outcome |
| I²_GX                       | all pairs                     | 0.97–0.99                          | Very strong NOME regime; Egger valid |
| MVMR BMI (adj. alcohol)    | EUR, n=455                    | β=0.118, OR=1.125 (1.10–1.15), p=7.7×10⁻³³ | BMI→mortality independent of alcohol |
| MVMR alcohol (adj. BMI)    | EUR, n=9                      | β=0.085, OR=1.089 (1.01–1.17), p=0.026      | Alcohol→mortality independent of BMI (but n=9 IVs) |

---

## 7. Known gaps

1. **SAS all-cause mortality**: no public GWAS in OpenGWAS. GBMI / Global Biobank Meta-analysis would provide one but requires a consortium request (logged as Week 2+ follow-up).
2. **AMR all-cause mortality**: All of Us registration still pending (brief notes this). No fallback identified.
3. **Pure BBJ all-cause mortality**: BBJ distributes disease-specific GWAS (bbj-a-*), not all-cause mortality. Current EAS mortality proxy is the small UKB-EAS sub-cohort (n=1,122) which is why EAS p-values are wide.
4. **UPF instrumentation**: UKB processed-meat is a known-poor proxy for UPF (healthy-eater correlation). A diet-pattern GWAS (Cole 2020 or similar) would improve this. The borderline-protective direction is consistent with the "health-conscious-eater" confound and should not be over-interpreted.
5. **Colocalisation (coloc.abf)**: deferred. Required region-level summary statistics for top loci (FTO, MC4R, ADH1B) — the OpenGWAS API currently exposes tophits only and region extraction needs direct file access. Deferred to Week 2 (will use locally-downloaded GWAS summary-stat files on P1 disk).
6. **Sign of the "OR"**: Pilling 2017 parental longevity is a continuous "age at death" phenotype; strict OR interpretation requires re-scaling. Our tables report exp(β) labelled as "OR" for consistency across mortality and CVD pairs; in manuscript text the longevity rows will be re-expressed as "hazard-ratio-equivalent via Pilling's lifespan-to-log-hazard scaling" (Pilling 2017 §Methods).

---

## 8. Top 3 methodological risks for the Part 1 story

### Risk 1 — Only one ancestry is well-powered for mortality
EUR mortality GWAS (n=415,311) dwarfs EAS (n=1,122) and AFR (n=3,732) by >100×. While the *meta is directionally consistent* (I²=0%), a reviewer can legitimately argue that "trans-ancestry replication" is a stretch when two of three ancestry estimates have CIs that include 1. **Mitigation**: Week 2 priority is to get GBMI or FinnGen+BBJ+MVP meta-mortality summary stats; reword Part 1 claim from "trans-ancestry causal evidence" → "EUR causal evidence with directionally-consistent trans-ancestry replication in two smaller ancestry-specific cohorts".

### Risk 2 — UPF proxy is non-orthogonal to healthy-eating bias
The processed-meat GWAS as a UPF proxy gives a borderline-protective point estimate (OR 0.91, p=0.06) that is likely confounded by healthy-eater reverse correlation. For an eLife Reviewed Preprint covering the Sweet Trap construct this is a publication liability. **Mitigation**: either (a) drop UPF from Part 1 and list as "future work" when a proper GWAS is available, or (b) run a Cole 2020 / Mozaffarian diet-pattern PGS as a better instrument in Week 2. Leaving the current OR<1 result in the paper with no caveat is not an option.

### Risk 3 — Pilling 2017 longevity scale and OR reporting
The "OR" values we report for mortality are exp(β) where β is on the parental-longevity scale (higher = longer life). The direction is correct (higher BMI → shorter paternal life) but the magnitude is not a per-allele mortality OR. Confusing the two in the manuscript will draw a hostile review. **Mitigation**: in the main text use Pilling's 2017 conversion factor (years of life per SD of exposure) as the headline and only report OR in supplementary tables with a clear scale footnote.

---

## 9. What is NOT done (and the next-step plan)

| # | Item | Why not now | Where to pick up |
|---|------|-------------|------------------|
| 1 | Colocalisation (coloc.abf) at FTO/MC4R/ADH1B | Needs region-level summary stats; OpenGWAS API rate limits | Download Finngen R12 + UKB locally; Week 2 |
| 2 | All of Us AMR MR | Registration pending | Follow-up in 6-12 weeks |
| 3 | GBMI trans-ancestry mortality meta | Requires consortium data access | Week 2 (dbGaP + Open Science Framework cross-check) |
| 4 | NOVA-classified UPF GWAS | No such GWAS exists (Cole 2020 is closest proxy) | Flag as future work |
| 5 | Cluster MR (Foley 2021) on BMI-mortality | Part of Week 2 sensitivity pack once outliers identified | Week 2 |
| 6 | Forest plot + funnel plot figures | `figure-designer` agent job | Hand-off when Part 2 (PRISMA meta) also done |

---

## 10. How to re-run from scratch

```bash
# 1. Clear outputs (optional)
rm /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part1-mr/outputs/*
rm /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part1-mr/logs/*

# 2. Check OpenGWAS token is present
grep OPENGWAS_JWT /Users/andy/Desktop/Research/sweet-trap-multidomain/.Renviron || {
  echo "Populate .Renviron with OPENGWAS_JWT=<your-token>" && exit 1
}

# 3. Run pipeline
cd /Users/andy/Desktop/Research/sweet-trap-multidomain
for s in 01_instruments 02_outcomes 03_mr_main 04_trans_ancestry_meta 05_sensitivity; do
  R --vanilla --quiet -f 03-analysis/part1-mr/scripts/${s}.R 2>&1 | tail -4
done
```

Expected total wall-clock ≈ 20–25 min (largest cost: OpenGWAS API round-trips + BMI 501-SNP outcome pulls).
