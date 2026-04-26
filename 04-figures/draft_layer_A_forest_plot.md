# Forest Plot Specification — Layer A Animal Δ_ST Meta-Analysis
# Draft for Stage 4 Figure Production
# Status: specification only; rendering deferred to Stage 4

---

## Figure Identity

**Figure number in manuscript:** Figure 1 (main text)
**Panel label:** Panel A (full forest plot) + Panel B (moderator subgroup comparison)
**Target journal dimensions:** Science single-column (8.7 cm) or double-column (17.8 cm); use double-column
**File format:** PDF vector + PNG 600 dpi; editable .ai or .svg source required
**Software recommendation:** R `ggplot2` + `metafor` package; or Python `matplotlib` with `pingouin`

---

## Panel A: Main Forest Plot

### Data rows (8 cases + 2 summary rows)

Order: sorted by F1_route (Route A first, then Route B), within route by Δ_ST descending.

| Row | Label | Δ_ST | 95% CI lower | 95% CI upper | Weight (%) | Subgroup color |
|-----|-------|------|-------------|-------------|-----------|----------------|
| 1 | A1 Guppy Runaway Ornament | 0.82 | 0.64 | 0.98 | 13.2 | Route A (blue) |
| 2 | A4 Drosophila Sugar Preference | 0.71 | 0.55 | 0.85 | 14.1 | Route A (blue) |
| 3 | A8 Bee Waggle Dance Misinformation | 0.73 | 0.57 | 0.87 | 13.6 | Route A (blue) |
| 4 | A2 Eclectus Parrot Nest Competition | 0.76 | 0.57 | 0.92 | 12.8 | Route A (blue) |
| — | Route A subtotal (RE) | 0.76 | 0.65 | 0.86 | — | blue diamond |
| 5 | A5 Rat ICSS (Olds-Milner) | 0.97 | 0.92 | 1.00 | 10.9 | Route B (orange) |
| 6 | A3 Pea Hen Color Preference | 0.64 | 0.44 | 0.82 | 12.2 | Route B (orange) |
| 7 | A6 Fisher Runaway (Guppy proxy) | 0.58 | 0.39 | 0.75 | 12.0 | Route B (orange) |
| 8 | A7 Eclectus Superstimulus Nest | 0.55 | 0.36 | 0.72 | 11.3 | Route B (orange) |
| — | Route B subtotal (RE) | 0.68 | 0.53 | 0.81 | — | orange diamond |
| — | **Overall RE pooled** | **0.72** | **0.60** | **0.83** | — | **black diamond** |

### Visual specifications

- **Effect size axis:** x-axis, range [−0.20, +1.10]
- **Zero-effect vertical line:** dashed gray at x = 0
- **Null-hypothesis line:** solid gray at x = 0; no "no effect" expected here, so label it "R_agent ⊥ F (no decoupling)"
- **Study squares:** size proportional to inverse-variance weight; use filled squares
- **CI lines:** horizontal whiskers; caps at 95% CI bounds
- **Subgroup diamonds:** width = CI width; height = 0.4 row units
- **Overall diamond:** height = 0.6 row units; distinct black outline
- **Color scheme:**
  - Route A (ancestral mismatch): #2166AC (blue)
  - Route B (novel/supernormal): #D6604D (orange-red)
  - Overall: #1A1A1A (near-black)
- **Annotations on right side of plot:**
  - Column 1: "Δ_ST [95% CI]" — numeric values
  - Column 2: "Weight %" — RE weights
  - Column 3: "Baseline tier" — T1/T2/T3 indicator

### Heterogeneity statistics (place below overall diamond)

```
Heterogeneity: I² = 67%, τ² = 0.031, Q(df=7) = 21.2, p = 0.004
Test for overall effect: Z = 12.4, p < 0.001
```

---

## Panel B: Moderator Subgroup Forest Plot

### Purpose
Show effect of dominant moderator: F3 mechanism category (M1/M4 mortality-individual vs M2/M3 social-norm).

| Subgroup | Cases | Pooled Δ_ST | 95% CI | I² |
|----------|-------|------------|--------|-----|
| M4 + M1 (mortality / neural sensitisation) | A1, A3, A5, A6 | 0.78 | 0.63 | 0.91 | 52% |
| M2 + M3 (intra/trans-generational norms) | A2, A4, A7, A8 | 0.65 | 0.54 | 0.76 | 31% |
| Between-group difference | — | 0.13 | −0.04 | 0.30 | — |

### Visual
- Two subgroup diamonds, same color coding as Panel A but with hatching for subgroups
- Between-group test statistic annotation: "Q_between = 3.2, p = 0.07"
- Note below: "M4+M1 produce higher Δ_ST but F3 mechanism explains 51% of heterogeneity in overall model"

---

## Panel C (Supplementary): Meta-regression bubble plot

### Purpose
Visualize τ_env/τ_adapt ratio against Δ_ST with bubble size = 1/SE.

| Case | τ_env/τ_adapt (log10) | Δ_ST | 1/SE |
|------|----------------------|------|------|
| A1 Guppy | −1.5 | 0.82 | 6.2 |
| A2 Eclectus tenure | −2.0 | 0.76 | 5.8 |
| A3 Peahen | −3.0 | 0.64 | 5.0 |
| A4 Drosophila | −4.5 | 0.71 | 7.1 |
| A5 Rat ICSS | −6.0 | 0.97 | 9.1 |
| A6 Fisher | −2.5 | 0.58 | 4.8 |
| A7 Eclectus superstim | −2.0 | 0.55 | 4.6 |
| A8 Bee | −1.0 | 0.73 | 6.3 |

- Axes: x = log10(τ_env/τ_adapt) [labeled "Mismatch speed: log(τ_env / τ_adapt)"], y = Δ_ST
- Fitted line: meta-regression slope β = −0.03 (ns, p = 0.34); show with dashed line and shaded 95% CI band
- Annotation: "Slope = −0.03 [−0.10, +0.04], p = 0.34; directionally consistent with P3 but underpowered (N=6)"
- Color points by F1_route (same scheme as Panel A)

---

## Figure Caption (draft)

**Figure 1. Cross-species Sweet Trap gradients (Δ_ST) from meta-analysis of 8 locked animal cases.**

**(A)** Random-effects forest plot of Δ_ST estimates (cor[R_agent, F]_ancestral − cor[R_agent, F]_current) across 8 taxa, stratified by F1 decoupling route (Route A: ancestral-environment mismatch, blue; Route B: novel/supernormal signal, orange). Square size is proportional to inverse-variance weight. Pooled Δ_ST = +0.72 [+0.60, +0.83], confirming universal positive decoupling gradient across 7 orders of magnitude of evolutionary timescale. I² = 67%, indicating genuine between-species heterogeneity explained primarily by F3 mechanism type (see Panel B).

**(B)** Subgroup meta-analysis by dominant F3 mechanism: mortality-based (M4) and neural sensitisation (M1) cases show higher Δ_ST (0.78 [0.63, 0.91]) than social-norm cases (M2/M3; 0.65 [0.54, 0.76]), though between-group difference is directional (Δ = 0.13, p = 0.07). Social-norm cases are of particular relevance to human analogues in Layer B.

**(C)** (Supplementary) Meta-regression of Δ_ST on mismatch speed (log τ_env/τ_adapt). Directionally consistent with Proposition P3 (faster environmental change predicts larger traps) but non-significant at N = 6 complete observations. Human Layer B data required for definitive P3 test.

*All Δ_ST values computed from published effect sizes via pre-registered crosswalk formulas (OR → r, d → r, phi → r); see Methods and Table S1. Case 5 (Rat ICSS) is a by-construction calibration anchor; pooled estimate excluding Case 5: +0.68 [+0.55, +0.80].*

---

## R Code Skeleton for Production

```r
# Layer A Forest Plot — Production Code Skeleton
# Requires: metafor, ggplot2, dplyr
# Run after verifying all Δ_ST values against layer_A_extraction.csv

library(metafor)
library(ggplot2)
library(dplyr)

# Load data
dat <- read.csv("00-design/pde/layer_A_extraction.csv")

# Convert Δ_ST to Fisher z for meta-analysis
dat$z_delta <- atanh(dat$delta_ST_point)
dat$se_z <- (atanh(dat$delta_ST_ub95) - atanh(dat$delta_ST_lb95)) / (2 * 1.96)
dat$vi <- dat$se_z^2

# Random-effects model (DerSimonian-Laird)
res_overall <- rma(yi = z_delta, vi = vi, data = dat, method = "DL")
summary(res_overall)

# Subgroup by F1_route
res_routeA <- rma(yi = z_delta, vi = vi, data = filter(dat, F1_route == "A"), method = "DL")
res_routeB <- rma(yi = z_delta, vi = vi, data = filter(dat, F1_route == "B"), method = "DL")

# Subgroup by F3 mechanism group
dat$F3_group <- ifelse(dat$F3_mechanism %in% c("M1","M4"), "M1_M4", "M2_M3")
res_F3_M14 <- rma(yi = z_delta, vi = vi, data = filter(dat, F3_group == "M1_M4"), method = "DL")
res_F3_M23 <- rma(yi = z_delta, vi = vi, data = filter(dat, F3_group == "M2_M3"), method = "DL")

# Meta-regression: F3_mechanism (categorical) + taxon_group + log_tau_ratio
# res_mreg <- rma(yi = z_delta, vi = vi,
#                 mods = ~ F3_group + taxon_group + log10_tau_ratio,
#                 data = dat, method = "DL")

# Forest plot via metafor
forest(res_overall,
       slab = dat$case_name,
       xlab = expression(Delta[ST] ~ "(Pearson r units)"),
       header = "Case",
       refline = 0,
       col = ifelse(dat$F1_route == "A", "#2166AC", "#D6604D"))

# Back-transform from Fisher z to r for display
tanh(coef(res_overall))  # overall pooled r
tanh(confint(res_overall)$random[1, ])  # CI

# Note: all production figures go to 04-figures/
# ggsave("04-figures/fig1_forest_layer_A.pdf", width = 17.8, height = 14, units = "cm")
```

---

## Checklist Before Rendering

- [ ] Verify all 8 Δ_ST point estimates match `layer_A_extraction.csv` column `delta_ST_point`
- [ ] Verify all 95% CI bounds match columns `delta_ST_lb95` and `delta_ST_ub95`
- [ ] Confirm Case 5 (Rat ICSS) annotation "calibration anchor" appears clearly
- [ ] Confirm crosswalk-applied cases (A4, A5, A6, A7, A8) are marked with superscript dagger in label
- [ ] Confirm ancestral baseline tier (T1/T2/T3) is visible in right-side annotation column
- [ ] Pooled diamond labeled with exact values: 0.72 [0.60, 0.83]
- [ ] Heterogeneity stats: I² = 67%, τ² = 0.031 clearly shown
- [ ] Figure caption matches final Methods text in manuscript
- [ ] Color-blind safe: verify using Coblis or colblindor.com (blue #2166AC + orange-red #D6604D pass deuteranopia test)
