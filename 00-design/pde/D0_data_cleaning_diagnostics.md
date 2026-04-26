# D0: CFPS Long-Panel Cleaning Diagnostics

**Generated:** 2026-04-17 18:26
**Pipeline script:** `03-analysis/scripts/build_cfps_long_panel.py`
**Source:** `/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/2010-2022cfps非平衡面板数据(stata_推荐使用）.dta`
**Full long panel:** `02-data/processed/cfps_long_panel.parquet` (86,294 person-years × 158 cols)

---

## 1. Panel structure

- **n_person_years** = 86,294
- **n_unique_pid** = 32,165
- **waves** = [2010, 2012, 2014, 2016, 2018, 2020, 2022]

| Wave | N | % |
|---:|---:|---:|
| 2010 | 13,317 | 15.4% |
| 2012 | 12,107 | 14.0% |
| 2014 | 13,597 | 15.8% |
| 2016 | 13,642 | 15.8% |
| 2018 | 13,503 | 15.6% |
| 2020 | 10,322 | 12.0% |
| 2022 | 9,806 | 11.4% |

---

## 2. Analysis-ready N by domain

| Domain | N (person-years) | N (unique pid) | N cols | File | Size |
|:---|---:|---:|---:|:---|---:|
| D1_urban | 84,328 | 31,612 | 38 | `02-data/processed/panel_D1_urban.parquet` | 2.61 MB |
| D2_education | 30,630 | 15,500 | 46 | `02-data/processed/panel_D2_education.parquet` | 1.59 MB |
| D3_work | 41,423 | 22,228 | 58 | `02-data/processed/panel_D3_work.parquet` | 1.79 MB |
| D5_diet | 80,524 | 30,865 | 48 | `02-data/processed/panel_D5_diet.parquet` | 3.71 MB |
| D8_housing | 83,585 | 31,511 | 62 | `02-data/processed/panel_D8_housing.parquet` | 5.71 MB |

### Comparison to Urban project (infra-growth-mismatch)

Paper-1 urban pipeline (`cfps_igmi_expanded.parquet`): ~28K person-years (IGMI-merged subsample).
This pipeline's D1_urban subset: 84,328 person-years (full qn12012 sample, pre-IGMI-merge).
The difference is expected: the IGMI merge drops observations in cities without IGMI series.

- **D2_education**: 30,630 person-years (1.09× urban-28K, larger)
- **D3_work**: 41,423 person-years (1.48× urban-28K, larger)
- **D5_diet**: 80,524 person-years (2.88× urban-28K, larger)
- **D8_housing**: 83,585 person-years (2.99× urban-28K, larger)

---

## 3. Tier confirmation vs Stage 0B ratings

| Domain | Stage 0B Tier | Anchor var | Stage 0B N | Cleaned N | Status |
|:---|:---:|:---|---:|---:|:---|
| D1_urban | *** | `qn12012` | 84,328 | 84,328 | confirmed (+0) |
| D2_education | ** | `eexp` | 85,594 | 85,594 | confirmed (+0) |
| D3_work | *** | `workhour` | 41,528 | 41,528 | confirmed (+0) |
| D5_diet | ** | `food` | 84,365 | 84,365 | confirmed (+0) |
| D8_housing | *** | `mortage` | 85,866 | 85,866 | confirmed (+0) |

Notes: Cleaned N < Stage 0B N usually reflects out-of-range value nulling (e.g. `qg405` sentinel 79, `workhour` > 168).

---

## 4. Year-coverage per variable (selected domain anchors)

| Variable | Role | Total N | 2010 | 2012 | 2014 | 2016 | 2018 | 2020 | 2022 |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pid` | key | 86,294 | 13317 | 12107 | 13597 | 13642 | 13503 | 10322 | 9806 |
| `year` | key | 86,294 | 13317 | 12107 | 13597 | 13642 | 13503 | 10322 | 9806 |
| `age` | covariate | 86,271 | 13317 | 12107 | 13596 | 13626 | 13498 | 10322 | 9805 |
| `gender` | covariate | 86,293 | 13317 | 12107 | 13597 | 13641 | 13503 | 10322 | 9806 |
| `eduy` | covariate | 83,564 | 13317 | 12105 | 13593 | 12404 | 12909 | 10148 | 9088 |
| `hukou` | lambda_proxy | 85,025 | 13296 | 12056 | 13237 | 13499 | 13187 | 10041 | 9709 |
| `qn12012` | sweet_DV | 84,328 | 13292 | 12003 | 12993 | 13508 | 13128 | 9978 | 9426 |
| `dw` | sweet_DV | 83,991 | 13242 | 11899 | 12952 | 13462 | 13088 | 9950 | 9398 |
| `workhour` | treatment | 41,528 | 3483 | 0 | 9161 | 3572 | 9729 | 7992 | 7591 |
| `qg406` | sweet_DV | 53,015 | 3605 | 0 | 10719 | 11135 | 10581 | 8736 | 8239 |
| `qg401` | sweet_DV | 42,288 | 3605 | 0 | 0 | 11132 | 10578 | 8734 | 8239 |
| `qp401` | bitter_outcome | 84,351 | 13312 | 12040 | 13006 | 13516 | 13111 | 9960 | 9406 |
| `health` | bitter_outcome | 85,948 | 13315 | 12105 | 13590 | 13641 | 13416 | 10214 | 9667 |
| `qq4010` | bitter_outcome | 26,880 | 0 | 0 | 3432 | 3597 | 3228 | 7433 | 9190 |
| `eexp` | treatment | 85,594 | 13196 | 11968 | 13516 | 13582 | 13384 | 10216 | 9732 |
| `school` | treatment | 85,594 | 13196 | 11968 | 13516 | 13582 | 13384 | 10216 | 9732 |
| `child_num` | covariate | 72,977 | 0 | 12107 | 13597 | 13642 | 13503 | 10322 | 9806 |
| `food` | treatment | 84,365 | 12429 | 11575 | 13444 | 13573 | 13408 | 10206 | 9730 |
| `qq201` | covariate | 84,347 | 13284 | 12044 | 13006 | 13518 | 13124 | 9959 | 9412 |
| `mortage` | treatment | 85,866 | 13298 | 11973 | 13597 | 13608 | 13414 | 10237 | 9739 |
| `resivalue` | treatment | 85,966 | 13311 | 12088 | 13597 | 13642 | 13384 | 10221 | 9723 |
| `savings` | bitter_outcome | 85,983 | 13212 | 12090 | 13597 | 13642 | 13450 | 10252 | 9740 |
| `house_debts` | bitter_outcome | 85,287 | 13306 | 12055 | 13028 | 13601 | 13414 | 10190 | 9693 |

Full coverage table: `02-data/linkage/variable_year_coverage.csv`

---

## 5. Sweet DV × Bitter outcome descriptives by wave

### D1_urban

**sweet** = `qn12012`

| Year | N | Mean | SD |
|---:|---:|---:|---:|
| 2010 | 13,292 | 3.422 | 1.060 |
| 2012 | 12,003 | 3.270 | 1.076 |
| 2014 | 12,993 | 3.733 | 1.043 |
| 2016 | 13,508 | 3.566 | 1.101 |
| 2018 | 13,128 | 3.958 | 0.982 |
| 2020 | 9,978 | 3.967 | 0.944 |
| 2022 | 9,426 | 3.923 | 0.929 |

### D2_education

**sweet** = `qn12012`

| Year | N | Mean | SD |
|---:|---:|---:|---:|
| 2010 | 13,292 | 3.422 | 1.060 |
| 2012 | 12,003 | 3.270 | 1.076 |
| 2014 | 12,993 | 3.733 | 1.043 |
| 2016 | 13,508 | 3.566 | 1.101 |
| 2018 | 13,128 | 3.958 | 0.982 |
| 2020 | 9,978 | 3.967 | 0.944 |
| 2022 | 9,426 | 3.923 | 0.929 |

**bitter** = `eexp_share`

| Year | N | Mean | SD |
|---:|---:|---:|---:|
| 2010 | 11,725 | 0.081 | 0.140 |
| 2012 | 10,398 | 0.070 | 0.124 |
| 2014 | 13,506 | 0.066 | 0.122 |
| 2016 | 13,582 | 0.060 | 0.109 |
| 2018 | 13,354 | 0.068 | 0.120 |
| 2020 | 10,159 | 0.058 | 0.112 |
| 2022 | 9,676 | 0.060 | 0.111 |

### D3_work

**sweet** = `qg406`

| Year | N | Mean | SD |
|---:|---:|---:|---:|
| 2010 | 3,605 | 3.283 | 0.809 |
| 2012 | 0 | — | — |
| 2014 | 10,719 | 3.518 | 0.915 |
| 2016 | 11,135 | 3.448 | 0.876 |
| 2018 | 10,581 | 3.631 | 0.979 |
| 2020 | 8,736 | 3.685 | 0.942 |
| 2022 | 8,239 | 3.698 | 0.962 |

**bitter** = `qp401`

| Year | N | Mean | SD |
|---:|---:|---:|---:|
| 2010 | 13,312 | 0.168 | 0.374 |
| 2012 | 12,040 | 0.156 | 0.362 |
| 2014 | 13,006 | 0.200 | 0.400 |
| 2016 | 13,516 | 0.192 | 0.394 |
| 2018 | 13,111 | 0.193 | 0.394 |
| 2020 | 9,960 | 0.167 | 0.373 |
| 2022 | 9,406 | 0.174 | 0.379 |

### D5_diet

**sweet** = `qn12012`

| Year | N | Mean | SD |
|---:|---:|---:|---:|
| 2010 | 13,292 | 3.422 | 1.060 |
| 2012 | 12,003 | 3.270 | 1.076 |
| 2014 | 12,993 | 3.733 | 1.043 |
| 2016 | 13,508 | 3.566 | 1.101 |
| 2018 | 13,128 | 3.958 | 0.982 |
| 2020 | 9,978 | 3.967 | 0.944 |
| 2022 | 9,426 | 3.923 | 0.929 |

**bitter** = `qp401`

| Year | N | Mean | SD |
|---:|---:|---:|---:|
| 2010 | 13,312 | 0.168 | 0.374 |
| 2012 | 12,040 | 0.156 | 0.362 |
| 2014 | 13,006 | 0.200 | 0.400 |
| 2016 | 13,516 | 0.192 | 0.394 |
| 2018 | 13,111 | 0.193 | 0.394 |
| 2020 | 9,960 | 0.167 | 0.373 |
| 2022 | 9,406 | 0.174 | 0.379 |

### D8_housing

**sweet** = `dw`

| Year | N | Mean | SD |
|---:|---:|---:|---:|
| 2010 | 13,242 | 2.773 | 0.977 |
| 2012 | 11,899 | 2.670 | 1.047 |
| 2014 | 12,952 | 2.941 | 1.012 |
| 2016 | 13,462 | 2.813 | 1.095 |
| 2018 | 13,088 | 3.103 | 1.091 |
| 2020 | 9,950 | 3.079 | 1.047 |
| 2022 | 9,398 | 3.002 | 1.050 |

**bitter** = `savings`

| Year | N | Mean | SD |
|---:|---:|---:|---:|
| 2010 | 13,212 | 10512.512 | 49032.511 |
| 2012 | 12,090 | 28974.638 | 96588.532 |
| 2014 | 13,597 | 32803.158 | 98408.687 |
| 2016 | 13,642 | 46870.021 | 148379.544 |
| 2018 | 13,450 | 55467.689 | 171256.811 |
| 2020 | 10,252 | 75171.847 | 189036.252 |
| 2022 | 9,740 | 99073.473 | 268319.374 |

---

## 6. λ (externalization capacity) proxy availability

| λ proxy | Total N | 2010 | 2012 | 2014 | 2016 | 2018 | 2020 | 2022 |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| `age` | 86,271 | 13317 | 12107 | 13596 | 13626 | 13498 | 10322 | 9805 |
| `hukou` | 85,025 | 13296 | 12056 | 13237 | 13499 | 13187 | 10041 | 9709 |
| `workplace` | 32,108 | 0 | 3641 | 5415 | 5922 | 5975 | 5570 | 5585 |
| `child_num` | 72,977 | 0 | 12107 | 13597 | 13642 | 13503 | 10322 | 9806 |
| `communist` | 56,622 | 13317 | 44 | 74 | 13641 | 11993 | 9033 | 8520 |
| `h_loan` | 84,977 | 13317 | 10790 | 13597 | 13642 | 13503 | 10322 | 9806 |
| `familysize` | 86,294 | 13317 | 12107 | 13597 | 13642 | 13503 | 10322 | 9806 |
| `eduy` | 83,564 | 13317 | 12105 | 13593 | 12404 | 12909 | 10148 | 9088 |
| `migrant` | 83,653 | 13296 | 12012 | 13125 | 13211 | 13016 | 9670 | 9323 |
| `age_young` | 86,271 | 13317 | 12107 | 13596 | 13626 | 13498 | 10322 | 9805 |
| `child_gender` | 78,192 | 12658 | 11487 | 12354 | 12175 | 11992 | 9064 | 8462 |
| `limit` | 65,231 | 13317 | 12107 | 9859 | 8890 | 8231 | 6542 | 6285 |

Full λ cross-tab: `02-data/linkage/lambda_proxy_coverage.csv`

---

## 7. Cleaning rules applied

1. **CFPS missing codes** (`-1, -2, -3, -8, -9, -10`) → `NaN` across all numeric columns.
2. **Out-of-range sentinels**:
   - `qg405`, `qn1101`: values > 5 (mostly `79` refusal code) → NaN
   - `qq4010`: < 0 or > 24 → NaN
   - `workhour`: ≤ 0 or > 168 → NaN
   - `age`: < 10 or > 100 → NaN
3. **Derived binaries**:
   - `overtime_48h = 1[workhour ≥ 48]` (China labor law)
   - `overtime_60h = 1[workhour ≥ 60]` (strong-996 proxy)
   - `has_mortgage = 1[mortage > 0]`
   - `education_squeeze = 1[eexp/fincome1 > 0.15]`
   - `has_child = 1[child_num ≥ 1]`
   - `age_young = 1[age < 40]`  (λ proxy: younger externalize more)
   - `migrant = 1[hukou=1 (rural) & urban=1]`
   - `post_2021 = 1[year ≥ 2021]` (双减 policy dummy)
4. **Derived shares/ratios**:
   - `mortgage_burden = mortage / fincome1` (winsorized 1/99%)
   - `eexp_share = eexp / expense` (winsorized 1/99%)
   - `eexp_income_ratio = eexp / fincome1` (winsorized 1/99%)
   - `food_share = food / expense` (winsorized 1/99%, Engel coefficient)
5. **Log transforms** (`log1p` after 1/99% winsorize):
   - `ln_savings, ln_house_debts, ln_resivalue, ln_nonhousing_debts, ln_total_asset, ln_durables_asset, ln_fincome1, ln_expense, ln_food, ln_eexp, ln_mexp`
6. **Female dummy**: `female = 1 - gender` (source `gender` is 1=male).

No row deletions in the full long panel — all cleaning is via NaN assignment. Domain analysis-ready subsets apply filters post hoc.

---

## 8. Missing-data pattern assessment (informal)

We do not run formal MCAR/MAR tests at this stage. Missing patterns are dominated by **wave-coverage holes** (CFPS questionnaires differ by wave — see Section 4) rather than item-level non-response. Specifically:

- `workhour` (N=41,528; 51.9% missing) — collected 2010/2014/2016/2018/2020/2022 and only for employed respondents. 2012 wave does NOT collect it.
- `qg401-qg406` job-satisfaction — collected 2010/2014/2016/2018/2020/2022, not 2012. Plus only employed respondents answer.
- `qq4010` sleep — only 2014+ waves (26,880 N).
- `mor` (alt mortgage label) — 2020/2022 only; `mortage` is the stable 7-wave label.
- `communist` — 2010/2016/2018/2020/2022 only (skipped 2012/2014).
- `minzu` — 2010 only; impute from first-observed value in full panel is recommended (not done here; flagged for D1/D3 analysis scripts).

Missingness in `eexp` is near-zero (0.8%) because CFPS asks all households regardless of child presence — NaN reflects true non-answer, not structural skip. Zero values (43,724 rows) reflect genuine no-education-spending households (50% of families), not missing.

**Recommendation:** treat wave-structural missingness as MAR conditional on `year` fixed effects. Item-level missingness in treatment variables (e.g. `workhour` among employees) may be MNAR and should be probed via selection models in the D3 robustness section.

---

## 9. Outputs

| File | Description |
|:---|:---|
| `02-data/processed/cfps_long_panel.parquet` | Full cleaned long panel |
| `02-data/processed/panel_D1_urban.parquet` | D1_urban analysis-ready subset |
| `02-data/processed/panel_D2_education.parquet` | D2_education analysis-ready subset |
| `02-data/processed/panel_D3_work.parquet` | D3_work analysis-ready subset |
| `02-data/processed/panel_D5_diet.parquet` | D5_diet analysis-ready subset |
| `02-data/processed/panel_D8_housing.parquet` | D8_housing analysis-ready subset |
| `02-data/linkage/variable_dict.csv` | Variable name / label / recoding rule |
| `02-data/linkage/variable_year_coverage.csv` | Wave-level N per variable |
| `02-data/linkage/lambda_proxy_coverage.csv` | λ-proxy availability cross-tab |
| `02-data/linkage/sweet_bitter_descriptives.json` | Descriptive stats (mean/SD) by wave/domain |
| `02-data/linkage/cfps_cleaning.log` | Full cleaning log |
| `00-design/pde/D0_data_cleaning_diagnostics.md` | **This file** |

---

*End D0 diagnostics. Stage 2 domain scripts consume these panels as the single data entry point.*