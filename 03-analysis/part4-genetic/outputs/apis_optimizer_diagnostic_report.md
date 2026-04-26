# Apis Gr_sweet — Optimiser-boundary diagnostic

Generated: 2026-04-26 15:06:04

**Clade**: `Gr_sweet__amellifera_clade`
**Production**: omega0=0.5 -> lnL_alt=-52163.159208, foreground omega_2a=36.18, LRT=9.92
**lnL_null** (production, fix_omega=1): -52168.121073

**Asymmetric decision rule**:
- APIS_TRUE_POSITIVE: all 5 LRT > 6.63 AND all omega_2a in [10, 100]
- APIS_OPTIMIZER_ARTIFACT: any LRT < 1.0 OR omega_2a near 1.0 (|w-1| < 0.5) OR omega_2a > 200
- APIS_MIXED: anything else (partial agreement)

## Per-start results

| omega_0 | lnL_alt | LRT | omega_2a | p_2a+2b | flag | status | wall_s |
|---------|---------|-----|----------|---------|------|--------|--------|
| 0.1 | -52163.159208 | 9.9237 | 36.1818 | 0.1202 | escaped | ok | 3604 |
| 0.5 | -52163.159208 | 9.9237 | 36.1814 | 0.1202 | escaped | reused | 0 |
| 1.0 | -52163.159208 | 9.9237 | 36.1871 | 0.1202 | escaped | ok | 3354 |
| 2.0 | -52163.159208 | 9.9237 | 36.1771 | 0.1202 | escaped | ok | 3686 |
| 5.0 | -52169.361385 | -2.4806 | 1.6340 | 0.0000 | fail | ok | 3345 |

## Verdict

**APIS_OPTIMIZER_ARTIFACT**

At least one starting omega returns to the boundary (omega_2a ~ 1.0), produces a runaway omega (> 200), or yields LRT ~ 0. The production omega_2a = 36.18 is NOT robust to starting-value perturbation. Apis joins D. melanogaster as a third boundary-range optimiser-trapped escape. Manuscript Layer-4 verdict tightens: no robust positive-selection signals across any of the 6 production tests.

## Files
- CSV: `/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/outputs/apis_optimizer_diagnostic.csv`
- Per-run dirs: `/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/data/codeml_runs/Gr_sweet__amellifera_clade/alt_w0_<X>/`
- Orchestrator log: `/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/logs/optimizer_diagnostic/apis_orchestrator_20260426_130844.log`
- Total wall time: 7040 s (117.3 min)
