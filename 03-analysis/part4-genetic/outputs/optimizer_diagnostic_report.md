# Optimizer-boundary diagnostic — branch-site Model A alt

Generated: 2026-04-26 08:37:58  •  5 clades × 5 starting omegas (Yang & dos Reis 2011).

**Rule**: TRUE_NULL = all 5 LRT ≤ 0.01 AND all foreground ω_2a = 1.0;  OPTIMIZER_ARTIFACT = any LRT > 1.0 with ω_2a > 1.0;  MIXED = partial escapes but all LRT < 2.71 (no df=1 χ² sig).

## Per-clade verdicts

### Gr_sweet__dmel_Gr64_cluster
- **Verdict**: OPTIMIZER_ARTIFACT
- lnL_null (production): -52162.226067

| ω₀ start | lnL_alt | LRT | ω_2a | flag | status |
|----------|---------|-----|------|------|--------|
| 0.1 | -52162.226067 | 0.000000 | 1.0000 | boundary | ok |
| 0.5 | -52162.226067 | 0.000000 | 1.0000 | boundary | reused |
| 1.0 | -52162.226067 | 0.000000 | 1.0000 | boundary | ok |
| 2.0 | NA | NA | NA | fail | timeout |
| 5.0 | -52157.388390 | 9.675354 | 144.9114 | escaped | ok |

### Gr_sweet__dmel_all_clade
- **Verdict**: OPTIMIZER_ARTIFACT
- lnL_null (production): -52161.860100

| ω₀ start | lnL_alt | LRT | ω_2a | flag | status |
|----------|---------|-----|------|------|--------|
| 0.1 | -52161.860100 | 0.000000 | 1.0000 | boundary | ok |
| 0.5 | -52161.860100 | 0.000000 | 1.0000 | boundary | reused |
| 1.0 | -52161.860100 | 0.000000 | 1.0000 | boundary | ok |
| 2.0 | -52161.860100 | 0.000000 | 1.0000 | boundary | ok |
| 5.0 | -52159.696404 | 4.327392 | 95.0687 | escaped | ok |

### Gr_sweet__coleoptera_clade
- **Verdict**: TRUE_NULL
- lnL_null (production): -52145.027945

| ω₀ start | lnL_alt | LRT | ω_2a | flag | status |
|----------|---------|-----|------|------|--------|
| 0.1 | -52145.027945 | 0.000000 | 1.0000 | boundary | ok |
| 0.5 | -52145.027977 | -0.000064 | 1.0000 | boundary | reused |
| 1.0 | -52145.027945 | 0.000000 | 1.0000 | boundary | ok |
| 2.0 | -52145.027945 | 0.000000 | 1.0000 | boundary | ok |
| 5.0 | -52145.027945 | 0.000000 | 1.0000 | boundary | ok |

### Gr_sweet__lepidoptera_clade
- **Verdict**: TRUE_NULL
- lnL_null (production): -52144.978842

| ω₀ start | lnL_alt | LRT | ω_2a | flag | status |
|----------|---------|-----|------|------|--------|
| 0.1 | -52144.978842 | 0.000000 | 1.0000 | boundary | ok |
| 0.5 | -52144.978842 | 0.000000 | 1.0000 | boundary | reused |
| 1.0 | -52144.978842 | 0.000000 | 1.0000 | boundary | ok |
| 2.0 | -52144.978842 | 0.000000 | 1.0000 | boundary | ok |
| 5.0 | -52144.978842 | 0.000000 | 1.0000 | boundary | ok |

### Gr_sweet__aaegypti_clade
- **Verdict**: TRUE_NULL
- lnL_null (production): -52153.153732

| ω₀ start | lnL_alt | LRT | ω_2a | flag | status |
|----------|---------|-----|------|------|--------|
| 0.1 | -52153.153732 | 0.000000 | 1.0000 | boundary | ok |
| 0.5 | -52153.153741 | -0.000018 | 1.0000 | boundary | reused |
| 1.0 | -52153.153732 | 0.000000 | 1.0000 | boundary | ok |
| 2.0 | -52153.153732 | 0.000000 | 1.0000 | boundary | ok |
| 5.0 | -52153.153732 | 0.000000 | 1.0000 | boundary | ok |

## Integrated reading

**2 of 5 clades flipped to OPTIMIZER_ARTIFACT**: Gr_sweet__dmel_Gr64_cluster, Gr_sweet__dmel_all_clade

The manuscript §3.4 "5/6 LRT = 0" count must be revised downward and Layer-4 verdict in §3.5 likely needs softening from PARTIALLY REFUTED to INCONCLUSIVE — optimiser-sensitive.

## Files
- CSV: `/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/outputs/optimizer_diagnostic.csv`
- Per-run dirs: `/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/data/codeml_runs/<clade>/alt_w0_<X>/`
- Orchestrator log: `/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/logs/optimizer_diagnostic/orchestrator_20260425_150131.log`
