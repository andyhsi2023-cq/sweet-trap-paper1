# Delta_ST Proxy Coding Rule
# Sweet Trap Part 2 — Full-Text Screening, 2026-04-24
# Version 1.0 (pre-registered at OSF https://osf.io/pv3ch)

## 1. Definition

Delta_ST (Δ_ST) is the signed scalar quantifying the magnitude of reward-fitness decoupling
for a given case. It is normalised to the interval [-1, +1].

**Positive Δ_ST** = reward signal exceeds fitness return (Sweet Trap condition).
**Negative Δ_ST** = fitness return exceeds reward signal (no Sweet Trap; over-aversion).
**Zero Δ_ST** = perfect calibration between reward signal and fitness return.

## 2. Primary Formula (when ancestral_r and current_r are available)

  Δ_ST = ancestral_r_point − current_r_point

Where:
- `ancestral_r_point` = Pearson r (or converted from other effect size) between reward-approach
  behavior and fitness in the ancestral/baseline environment
- `current_r_point` = Pearson r between reward-approach behavior and fitness in the current
  (degraded/novel) environment

Sign convention: ancestral_r is expected to be positive (approaching reward was adaptive).
current_r is expected to be zero or negative (approaching reward is now maladaptive).
Therefore Δ_ST = positive when the trap is active.

## 3. Effect Size Conversion Crosswalk

When primary papers report statistics other than Pearson r, the following conversions apply:

| Source metric | Conversion to r | Formula |
|---------------|-----------------|---------|
| Cohen's d | r = d / sqrt(d^2 + 4) | Standard conversion |
| Odds Ratio (OR) | r = log(OR) / sqrt(log(OR)^2 + pi^2/3) | Logistic-normal approximation |
| Hazard Ratio (HR) | r = log(HR) / sqrt(log(HR)^2 + pi^2/3) | Same as OR approximation |
| % change in fitness | r = tanh(% / 200) | Rough approximation; flag with crosswalk_applied = TRUE |
| Mean difference / SE | r = MD / sqrt(MD^2 + SE^2 * n) | Cohen's d intermediate step |
| Relative risk (RR) | r = log(RR) / sqrt(log(RR)^2 + pi^2/3) | Same as OR |

All crosswalk applications must set `crosswalk_applied = TRUE` and record `crosswalk_formula`.

## 4. Ancestral Baseline Tier

- **Tier 1**: direct experimental manipulation or controlled comparison within study
  (ancestral_r derived from same paper's control group or baseline period)
- **Tier 2**: phylogenetic or lab-vs-field comparison; ancestral_r from closely related
  taxon or pre-exposure population
- **Tier 3**: theoretical prior from literature; ancestral_r assigned as point estimate
  with explicit justification; default Tier 3 ancestral_r = +0.50 (mid-range ancestral
  adaptive behavior assumption) with wide CI [+0.10, +0.80]

## 5. When Effect Size Is Not Available

If full-text access is not achieved OR the paper does not report a quantifiable effect size:
- Set `delta_ST_point = NA`
- Set `delta_ST_lb95 = NA`, `delta_ST_ub95 = NA`
- Set `effect_size_raw = NA`
- Set `effect_size_metric = NA`
- Record reason in `notes` field

Cases with delta_ST = NA are included in the qualitative synthesis and phylum count
but excluded from the quantitative meta-analysis (delta_ST pooling). They appear in a
"qualitative-only" column of the PRISMA flow table and contribute to phylogenetic signal
analysis only if a sensitivity imputation is conducted.

## 6. Imputation for Sensitivity Analysis (pre-registered)

For the sensitivity analysis using continuous Δ_ST pooling (triggered if κ < 0.60 on F2),
cases with delta_ST = NA receive an imputed value drawn from the phylum-specific
mean Δ_ST ± 1.5 SD with 500 multiple imputations (mice package, predictive mean matching).
This imputation is flagged in the sensitivity table but not used in primary analysis.

## 7. Sign Correction Rule

If the paper reports a preference for a maladaptive stimulus without a numeric effect size,
but documents:
(a) significant mortality, reproductive failure, or survival reduction associated with
    the preferred stimulus, AND
(b) the ancestral stimulus class was demonstrably adaptive (Tier 2 or Tier 3 prior),

Then assign:
- delta_ST_point = +0.50 (median Sweet Trap prior, conservative)
- delta_ST_lb95 = +0.10
- delta_ST_ub95 = +0.80
- crosswalk_applied = TRUE
- crosswalk_formula = "prior_assignment_rule_7"

This assignment applies to no more than 30% of included cases (per pre-reg deviation
protocol). If more than 30% require rule-7 assignment, the meta-analysis is switched
from Δ_ST pooling to qualitative synthesis with ordinal effect size (strong/moderate/weak).

## 8. Revision History

v1.0 — 2026-04-24 — Initial version; matches screening_protocol.md v1.0
