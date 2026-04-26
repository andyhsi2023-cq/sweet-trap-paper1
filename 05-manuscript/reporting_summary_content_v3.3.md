# Reporting Summary — Content Draft for NHB Submission

> **Purpose.** This document holds the **pre-filled content** for the Nature Portfolio *Reporting Summary* (v5+, `reporting-summary-flat.pdf`). Andy should download the official flat PDF from the Nature Portfolio author portal, then copy each field's content from this file. All numeric values are cross-checked against Methods §M1–M8 of `main_v3.3_submission.docx`.
>
> **Study type.** Secondary analysis of public / access-controlled summary statistics and anonymised panel data. No new human or animal data collected.

---

## Part 1 — Statistics

### 1.1. Sample size

**Q.** For all statistical analyses, confirm that the exact sample size (n) for each experimental group/condition is given.

**Content:**
- **Layer A (animal meta-analysis):** n = 20 cases across seven taxonomic classes (Mammalia, Aves, Reptilia, Amphibia, Insecta, Gastropoda, Arachnida); DerSimonian–Laird random-effects. Sample-size floor: k ≥ 10 for random-effects is conventional; our k = 20 exceeds this.
- **Layer B (five focal domains, spec-curve):** 3,000 pre-registered specifications total (600 per focal domain × 5). Per-domain person-waves: C8 CHFS 2011–2019 n ≈ 40,000 person-waves; C11 CHARLS/CFPS n ≈ 180,000; C12 CFPS n ≈ 65,000; C13 CFPS n ≈ 180,000; D_alcohol CHARLS n ≈ 20,000.
- **Layer C (cross-cultural):** n = 2,896,233 individual records (ISSP 25 countries × 17 waves, 1985–2022).
- **Layer D (Mendelian randomisation, 19 chains):** Exposures n = 258,000–1,331,000 (UK Biobank GWAS); Outcomes cases n = 5,579–41,000 (FinnGen R12 per outcome). 34 per-chain rows × 5 methods = 170 estimates.
- **Discriminant validity:** 18 cases (10 dev + 3 held-out Round 1 + 5 Round 2 §11.7/negatives); two-coder blind κ = 1.00 [CI 0.65, 1.00].
- **Cross-level meta-regression (pre-registered A+D subset):** n = 2 rank-correlations (olds > sensory > fisher); headline β = +1.58, p = 0.019 on one dimension.

### 1.2. Data exclusions

**Q.** Describe any data exclusions.

**Content:**
- **Layer A:** Pre-specified inclusion requires Δ_ST ≥ 0 measurable and fitness-cost documented; two candidate cases (rhesus food caching, zebra finch song) excluded at screening for insufficient fitness-cost data (documented in `layer_A_animal_meta_v2.md`).
- **Layer B:** Pre-registered filters per script (e.g., CFPS requires age 18–65, non-missing outcome). Documented per focal in `spec_curve_<focal>.py` headers.
- **Layer C:** ISSP waves without the target item (Environment-III P3 question) dropped; n = 25 countries is the intersection with G^c cultural-weight availability.
- **Layer D:** Instrument-quality filters: F-statistic > 10 per SNP; harmonisation removes palindromic SNPs with MAF > 0.42. Per-chain details in `mr_extended_v2.py` log.
- **Discriminant:** No cases excluded; negative controls chosen ex ante.

### 1.3. Replication

**Q.** Describe whether the experimental findings were reliably reproduced.

**Content:** All analyses run from raw data via scripted pipelines. Cross-method robustness is the primary replication strategy:
- **MR:** 5 methods × 19 chains (IVW, MR-Egger, weighted median, MR-PRESSO, CAUSE); MVMR sensitivity for three core chains.
- **Spec-curve:** 3,000 model variants (x5 focals × 600 per focal) testing sensitivity to outcome, treatment operationalisation, control set, fixed-effect structure, sample filter, waves/lag.
- **Discriminant:** Round 1 (10 dev + 3 held-out) + Round 2 (2 §11.7 positives + 3 systematic negatives) independent blind κ = 1.00 both rounds.
- **US replication (Layer 2-D):** HRS USA C8/C13 replicate the Chinese focal signs.

### 1.4. Randomization

**Q.** Describe how samples/organisms/participants were allocated into experimental groups.

**Content:** Not applicable. This is a secondary observational / Mendelian-randomisation analysis. For Layer D (MR), "randomisation" is natural: germline genetic variants are randomly allocated at meiosis and used as instrumental variables.

### 1.5. Blinding

**Q.** Describe whether the investigators were blinded to group allocation during data collection and/or analysis.

**Content:**
- **Layer A/B/C/D:** Not applicable (secondary data).
- **Discriminant validity:** Both coders were blind to ground-truth class (Sweet Trap vs negative control) and to each other's ratings. κ = 1.00 [CI 0.65, 1.00] computed on independent codings.

---

## Part 2 — Reporting for specific materials, systems and methods

| Material / System / Method | Used? | Description |
|---|---|---|
| Antibodies | No | — |
| Eukaryotic cell lines | No | — |
| Palaeontology and archaeology | No | — |
| Animals and other organisms | No | No new animal data collected. Layer A is meta-analysis of published animal studies. |
| Human research participants | No (secondary) | No new participants recruited. Secondary analysis of public / access-controlled data from ISSP, CFPS, CHARLS, CHFS, UK Biobank, FinnGen R12 (see §1.1). All source datasets obtained informed consent and local ethics approval under their original protocols. |
| Clinical data | No | — |
| Dual-use research of concern | No | — |
| ChIP-seq | No | — |
| Flow cytometry | No | — |
| MRI-based neuroimaging | No | — |
| Magnetic resonance imaging | No | — |
| Plants | No | — |

---

## Part 3 — Behavioural & social sciences study design (applicable)

### 3.1. Study description

Quantitative, observational, secondary-data analysis. Four-layer cross-species integration combining animal meta-analysis, human focal-domain spec-curve, cross-cultural panel regression, and Mendelian randomisation. Theory: axiomatic formalism (four axioms, four theorems, one keystone scalar Δ_ST). Prediction tests: five theorem-derived predictions (P1–P5) with pre-registered empirical-status audit.

### 3.2. Research sample

Four distinct samples:
- **Animal cases (A):** 20 cases spanning seven taxonomic classes, selected ex ante from literature searches (PubMed, Web of Science) using pre-registered inclusion criteria (documented in `layer_A_animal_meta_v2.md`).
- **Human focal domains (B):** 5 domains (C8 investment FOMO, C11 diet, C12 short-video, C13 housing, D_alcohol) drawn from Chinese panel surveys (CFPS, CHARLS, CHFS) plus HRS USA replication.
- **Cross-cultural (C):** 25 countries × 17 ISSP waves (1985–2022), G^c cultural-weight available.
- **Mendelian randomisation (D):** 19 chains; exposures from UK Biobank (European, ≈ 500K); outcomes from FinnGen R12 (Finnish, ≈ 500K).

### 3.3. Sampling strategy

Pre-registered inclusion criteria per layer. No post-hoc sample modification. Targeted sample sizes set by (a) survey-wave availability (B, C), (b) GWAS public availability (D), and (c) literature coverage (A). Power analyses: Layer A random-effects meta-analysis reaches ≥ 80% power for between-class moderator at k = 20; Layer D MR chains reach ≥ 80% power for OR = 1.1 per SD exposure given observed exposure F-statistic > 30; Layer B spec-curve power driven by sample-size x waves structure (see `spec_curve_<focal>.py` Monte Carlo).

### 3.4. Data collection

All data are secondary. Analyses run on personal workstation (macOS 26.4, MacBook Pro M5 Pro, 24 GB RAM) with `n_workers ≤ 2`, rasters sequential, large files via DuckDB / pyarrow chunked reads. Compute time: Layer A R ≈ 5 min; Layer B spec-curve ≈ 45 min per focal × 5; Layer D MR full ≈ 90 min; Layer C ISSP ≈ 15 min.

### 3.5. Timing and spatial scale

Data spans 1985–2022 (ISSP); 2011–2019 (CHFS); 2010–2022 (CHARLS); 2010–2022 (CFPS); UK Biobank 2006–2016; FinnGen R12 (2023 release). Geographic scope: Layer C 25 ISSP countries; Layer B China; Layer 2-D USA replication; Layer D Europe (UK/Finland).

### 3.6. Data exclusions

See Part 1.2.

### 3.7. Non-participation

Not applicable (secondary).

### 3.8. Randomization

See Part 1.4.

---

## Part 4 — Reporting standards

- **Pre-registration:** OSF deposit `https://osf.io/ucxv7/` (public, 2026-04-18); axioms frozen 2026-04-18; A+D joint cross-level test pre-registered 2026-04-17 before analysis run (`cross_level_plan.md`); intervention-asymmetry compilation scope frozen 2026-04-18.
- **Reproducibility:** All seeds fixed to 20260418. R 4.3+; Python 3.12 with pandas ≥ 2.0, numpy ≥ 1.24, statsmodels ≥ 0.14, matplotlib ≥ 3.7.
- **Reporting guidelines followed:** PRISMA 2020 (Layer A meta-analysis), STROBE-MR (Layer D Mendelian randomisation), CONSORT-nudge preprint guidance (Layer B behavioural interventions), ISSP-wave codebook (Layer C).
- **Statistics:** Two-sided tests; random-effects meta-analysis (DerSimonian–Laird); IVW as primary MR method with MR-Egger/weighted-median/MR-PRESSO/CAUSE sensitivity; multiple-testing correction (Benjamini–Hochberg) for spec-curve within focal.

---

## Ethics statement (for inclusion at §M8 of main manuscript)

This study is a secondary analysis of publicly-available or access-controlled anonymised datasets: ISSP via GESIS under standard terms of use; CFPS via Peking University Institute of Social Science Survey data-access agreement; CHARLS via Peking University National School of Development; CHFS via Southwestern University of Finance and Economics; HRS USA via ICPSR; UK Biobank summary statistics via OpenGWAS public release; FinnGen R12 under the FinnGen Public Release Terms; GBD 2021 via IHME public API; WVS/ISSP cultural-dimension indices via public archives. **No new data from human participants or live animals were collected for this study.** All primary studies from which summary statistics were drawn obtained informed consent and institutional ethics approval under their respective protocols. Under the Declaration of Helsinki and the Chongqing Medical University Ethics Committee guidance, purely retrospective analysis of de-identified summary statistics is exempt from additional institutional review. Ethics-approval exemption confirmation reference pending (Andy TODO before submission if NHB portal requires a specific CMU ethics reference number).

---

## Inclusion & Ethics in Global Research statement

This study analyses publicly-accessible or access-controlled summary-statistics and anonymised-panel data generated by local consortia (CFPS at Peking University; CHARLS at Peking University; CHFS at Southwestern University of Finance and Economics; UK Biobank at Stockport UK; FinnGen in Finland). All primary data collection received local institutional ethics approval and public-release terms. Authors based in China (L.A., H.X.) conducted analyses within the primary jurisdiction of three of four primary Chinese datasets; UK and Finnish data access followed the respective datasets' public-release terms. No field data were collected abroad; no biological materials or cultural artefacts were transferred across jurisdictions. Local citations relevant to the behavioural domains analysed (ISSP China-wave; CFPS; CHARLS) are included in the reference list.

---

## Code and data availability summary

- **Code:** GitHub `sweet-trap-multidomain` (public); mirrored on OSF `https://osf.io/ucxv7/`. Primary pipelines: `layer_A_meta_v2.R`, `mr_extended_v2.py`, `cross_level_meta.py`, `cultural_Gc.py`, `discriminant_validity.py`, `run_all_spec_curves.py`, `mortality_daly_anchor.py`.
- **Data:**
  - *Open:* 20-case Layer A extraction; 19-chain MR harmonised parquet; 25-country ISSP cross-cultural panel; 5-focal spec-curve results (3,000 specs); 18-case discriminant-validity features. All at OSF.
  - *Access-controlled:* CFPS (application via Peking University ISSS); CHARLS (application via Peking University NSD); CHFS (application via SWUFE); HRS (ICPSR); UK Biobank individual-level (UKB Access portal); FinnGen individual-level (FinnGen consortium).
- **Environment:** `environment.yml` at repo root (conda-forge Python 3.12 + R 4.3 minimal dependencies).
