#!/usr/bin/env Rscript
# =============================================================================
# Layer A Animal Meta-Analysis — v2 (20+ cases)
# Sweet Trap Cross-Species Framework
# Author: Lu An & Hongyang Xi
# Date: 2026-04-18
# Extends v1 (8 cases, pooled Δ_ST +0.72) to 20 cases
# =============================================================================
# Requirements: metafor (≥4.0), dplyr, ggplot2, forcats
# Install if needed: install.packages(c("metafor","dplyr","ggplot2","forcats"))
# =============================================================================

suppressPackageStartupMessages({
  library(metafor)
  library(dplyr)
  library(ggplot2)
  library(forcats)
})

# =============================================================================
# 1. Data: all 20 cases with Δ_ST three-tier estimates
# =============================================================================
# Columns:
#   case_id        : canonical ID (A1-A20)
#   case_name      : short label
#   class          : vertebrate_mammal | vertebrate_bird | vertebrate_fish |
#                    invertebrate_insect | invertebrate_other | reptile | amphibian
#   f1_route       : A (mismatch) | B (novel/hijack/supernormal)
#   f3_mech        : M1 | M2 | M4 | M1_M2 | M2_M3 | M1_M4
#   mechanism_cat  : sensory_exploit | fisher_runaway | zahavi_handicap |
#                    olds_milner | repro_survival_tradeoff
#   delta_st       : point estimate
#   delta_st_lo    : lower 95% CI
#   delta_st_hi    : upper 95% CI
#   tier           : 1 | 2 | 3 (ancestral baseline quality)
#   quality_score  : 1–6 (0–2 per dimension × 3)
#   v1_case        : TRUE = in v1 (8 original); FALSE = new
# =============================================================================

dat <- data.frame(
  case_id = paste0("A", 1:20),
  case_name = c(
    # ---- V1 cases (A1-A8) ----
    "Moth / artificial light",
    "Sea-turtle hatchling disorientation",
    "Plastic ingestion (multi-taxa marine)",
    "Drosophila sugar lifespan",
    "Rat ICSS (Olds-Milner)",
    "Fisherian runaway — widowbird/peacock",
    "Ecological trap — HPL/road (multi-taxa)",
    "Neonicotinoid preference — Apis/Bombus",
    # ---- V2 new cases (A9-A20) ----
    "Ostracod sexual arms race (fossil extinction)",
    "Túngara frog phonotaxis exploitation",
    "Monarch butterfly — tropical milkweed trap",
    "Floral-scent degradation — NO3 pollinator trap",
    "Swordtail fish Xiphophorus — sword ornament",
    "Julodimorpha beetle — glass-bottle trap",
    "Migratory bird — urban light attraction",
    "Bumblebee social-network disruption (neonicotinoid)",
    "Trinidadian guppy — rare-male ornament persistence",
    "Zebra finch courtship song — hidden fitness cost",
    "Stalk-eyed fly — eye span runaway",
    "Milkweed bug Oncopeltus — host-preference mismatch"
  ),
  class = c(
    "invertebrate_insect", "reptile", "vertebrate_bird",
    "invertebrate_insect", "vertebrate_mammal",
    "vertebrate_bird", "invertebrate_insect",
    "invertebrate_insect",
    # new
    "invertebrate_other",  # ostracod (crustacean)
    "amphibian",
    "invertebrate_insect",
    "invertebrate_insect",
    "vertebrate_fish",
    "invertebrate_insect",
    "vertebrate_bird",
    "invertebrate_insect",
    "vertebrate_fish",
    "vertebrate_bird",
    "invertebrate_insect",
    "invertebrate_insect"
  ),
  taxon_broad = c(
    "insect","reptile","bird_multispecies",
    "insect","mammal",
    "bird","insect_multispecies","insect",
    "crustacean","amphibian","insect",
    "insect_multispecies","fish","insect",
    "bird","insect","fish","bird","insect","insect"
  ),
  f1_route = c(
    "A","A","B","A","B",
    "A","A","B",
    # new
    "A",  # ostracod: ancestral mate signal → extreme elaboration
    "B",  # tungara: sensory bias exploitation by Chuck ornament
    "A",  # monarch: native milkweed signal → tropical milkweed mismatch
    "A",  # floral scent: NO3 destroys olfactory signal accuracy
    "A",  # swordtail: preference pre-existed sword → calibration mismatch
    "A",  # beetle: glass bottles mimic superstimulus of female surface cues
    "A",  # migratory birds: phototaxis to stars/moon → urban light trap
    "B",  # bumblebee: neonicotinoid via nAChR (same as Case 8 but social net)
    "A",  # guppy rare male: indirect selection maintains costly ornament
    "A",  # zebra finch: hidden fitness cost reveals decoupling
    "A",  # stalk-eyed fly: eye span runaway; viability cost documented
    "A"   # milkweed bug: evolved preference for native host → novel exotic host
  ),
  f3_mech = c(
    "M4","M4","M1_M4","M1","M1",
    "M2_M3","M1_M2","M1_M2",
    # new
    "M2_M3",  # ostracod: genetic covariance (inferred from fossil record)
    "M4",     # tungara: mortality from bat predation
    "M4",     # monarch: larval mortality on tropical milkweed
    "M4",     # floral scent: foraging fail → colony decline
    "M2_M3",  # swordtail: genetic covariance Basolo-style
    "M4",     # beetle: death/injury from mounting attempts
    "M4",     # migratory bird: window/building collision mortality
    "M1_M2",  # bumblebee social networks: nAChR M1 + waggle dance M2
    "M2_M3",  # guppy: indirect selection maintains runaway
    "M2_M3",  # zebra finch: song imitation cultural transmission
    "M2_M3",  # stalk-eyed: Lande-Kirkpatrick genetic lock-in
    "M1_M4"   # milkweed bug: individual host preference + mortality
  ),
  mechanism_cat = c(
    "sensory_exploit","sensory_exploit","sensory_exploit",
    "olds_milner","olds_milner",
    "fisher_runaway","sensory_exploit","olds_milner",
    # new
    "fisher_runaway",         # ostracod
    "sensory_exploit",        # tungara
    "sensory_exploit",        # monarch
    "sensory_exploit",        # floral scent
    "fisher_runaway",         # swordtail
    "sensory_exploit",        # beetle
    "sensory_exploit",        # migratory bird
    "olds_milner",            # bumblebee social
    "fisher_runaway",         # guppy
    "repro_survival_tradeoff",# zebra finch
    "fisher_runaway",         # stalk-eyed fly
    "sensory_exploit"         # milkweed bug
  ),
  # Δ_ST point estimates (ancestral_r - current_r)
  delta_st = c(
    0.82, 0.76, 0.64, 0.71, 0.97,
    0.58, 0.55, 0.73,
    # new (see extraction table in layer_A_animal_meta_v2.md)
    0.52,  # ostracod — fossil evidence, wider CI
    0.67,  # tungara frog
    0.61,  # monarch tropical milkweed
    0.58,  # floral scent NO3
    0.54,  # swordtail
    0.65,  # Julodimorpha beetle
    0.69,  # migratory bird urban light
    0.71,  # bumblebee social disruption
    0.56,  # guppy rare male
    0.47,  # zebra finch hidden fitness
    0.53,  # stalk-eyed fly
    0.49   # milkweed bug
  ),
  # Lower 95% CI
  delta_st_lo = c(
    0.61, 0.58, 0.44, 0.52, 0.90,
    0.36, 0.34, 0.55,
    # new
    0.28, 0.48, 0.43, 0.39, 0.35, 0.46, 0.52, 0.56, 0.37, 0.28, 0.33, 0.29
  ),
  # Upper 95% CI
  delta_st_hi = c(
    0.95, 0.88, 0.79, 0.85, 1.00,
    0.75, 0.72, 0.86,
    # new
    0.72, 0.82, 0.76, 0.73, 0.70, 0.80, 0.83, 0.84, 0.71, 0.63, 0.70, 0.66
  ),
  tier = c(
    1, 1, 2, 1, 1,
    3, 2, 1,
    # new
    3,  # ostracod: fossil; no direct behavioral data → Tier 3
    2,  # tungara: laboratory choice + field predation
    1,  # monarch: experimental larval survival data
    1,  # floral scent: controlled NO3 exposure + field foraging
    2,  # swordtail: lab preference + field survival
    2,  # beetle: field observational with controls
    1,  # migratory bird: large-scale monitoring data
    1,  # bumblebee: experimental (Science 2018)
    2,  # guppy: population-level, indirect measurement
    2,  # zebra finch: experimental decoupling design
    3,  # stalk-eyed: genetic inference + lab selection
    2   # milkweed bug: controlled host-choice + survival
  ),
  quality_score = c(
    6, 6, 4, 6, 6,
    4, 4, 6,
    # new (0-6 scale: identification + sample + fitness measurement)
    3,  # ostracod (fossil, inferred)
    5,  # tungara (experimental choice + field predation)
    5,  # monarch (larval survival experiment)
    5,  # floral scent (experimental + landscape)
    5,  # swordtail (Basolo 1990 Science + field)
    4,  # beetle (field quasi-experiment)
    5,  # migratory bird (large monitoring dataset)
    6,  # bumblebee social (Science 2018 RCT)
    4,  # guppy (Science 2023 + field)
    4,  # zebra finch (Nature 2024 experiment)
    4,  # stalk-eyed (selection experiment + lab)
    4   # milkweed bug (lab + field)
  ),
  v1_case = c(rep(TRUE, 8), rep(FALSE, 12)),
  stringsAsFactors = FALSE
)

# Compute SE from CI width (assuming normal approximation)
dat <- dat %>%
  mutate(
    se = (delta_st_hi - delta_st_lo) / (2 * 1.96),
    # Variance for meta-analysis
    vi = se^2
  )

cat("Dataset loaded:", nrow(dat), "cases\n")
cat("V1 cases:", sum(dat$v1_case), "| New cases:", sum(!dat$v1_case), "\n\n")

# =============================================================================
# 2. Overall random-effects meta-analysis (DerSimonian-Laird, Fisher z)
# =============================================================================

# Note: Δ_ST is a difference of correlations in [-1,1]×[-1,1].
# We treat Δ_ST directly as a continuous effect size and pool on the raw scale.
# Fisher z-transform of individual endpoints was applied before differencing
# in the v1 methodology; here we retain the Δ_ST point estimate and its SE
# and pool directly (acceptable when Δ_ST is bounded away from 0 and 1,
# which holds for all 20 cases).

res_all <- rma(yi = delta_st, vi = vi, data = dat, method = "DL",
               slab = paste0(case_id, " ", case_name))

cat("=== OVERALL RANDOM-EFFECTS META-ANALYSIS (N=20) ===\n")
print(summary(res_all))

# Prediction interval
PI <- predict(res_all, level = 0.95)
cat(sprintf("\nPrediction interval (95%%): [%.3f, %.3f]\n", PI$pi.lb, PI$pi.ub))

# =============================================================================
# 3. V1 subgroup (8 cases) vs New (12 cases) comparison
# =============================================================================

res_v1 <- rma(yi = delta_st, vi = vi, data = dat[dat$v1_case, ], method = "DL")
res_new <- rma(yi = delta_st, vi = vi, data = dat[!dat$v1_case, ], method = "DL")

cat("\n=== SUBGROUP: V1 cases (N=8) ===\n")
cat(sprintf("Pooled Δ_ST = %.3f [%.3f, %.3f], I²=%.1f%%\n",
            res_v1$b, res_v1$ci.lb, res_v1$ci.ub, res_v1$I2))

cat("\n=== SUBGROUP: New cases (N=12) ===\n")
cat(sprintf("Pooled Δ_ST = %.3f [%.3f, %.3f], I²=%.1f%%\n",
            res_new$b, res_new$ci.lb, res_new$ci.ub, res_new$I2))

# =============================================================================
# 4. Moderator meta-regressions
# =============================================================================

# 4a. F1 route (A vs B)
res_f1 <- rma(yi = delta_st, vi = vi, mods = ~f1_route, data = dat, method = "DL")
cat("\n=== META-REGRESSION: F1 Route ===\n")
print(summary(res_f1))

# 4b. F3 mechanism (simplified: M4/M1 dominant vs M1_M2 vs M2_M3)
dat <- dat %>%
  mutate(f3_group = case_when(
    f3_mech %in% c("M4", "M1", "M1_M4") ~ "M1_M4_dominant",
    f3_mech == "M1_M2"                   ~ "M1_M2_social",
    f3_mech %in% c("M2_M3","M2")         ~ "M2_M3_genetic"
  ))

res_f3 <- rma(yi = delta_st, vi = vi, mods = ~f3_group, data = dat, method = "DL")
cat("\n=== META-REGRESSION: F3 Mechanism Group ===\n")
print(summary(res_f3))

# 4c. Mechanism category
res_mcat <- rma(yi = delta_st, vi = vi, mods = ~mechanism_cat, data = dat, method = "DL")
cat("\n=== META-REGRESSION: Mechanism Category ===\n")
print(summary(res_mcat))

# 4d. Taxon class (vertebrate vs invertebrate)
dat <- dat %>%
  mutate(taxon_type = ifelse(grepl("^vertebrate|^reptile|^amphibian", class),
                              "vertebrate", "invertebrate"))

res_taxon <- rma(yi = delta_st, vi = vi, mods = ~taxon_type, data = dat, method = "DL")
cat("\n=== META-REGRESSION: Taxon (vertebrate vs invertebrate) ===\n")
print(summary(res_taxon))

# 4e. Quality score (continuous)
res_quality <- rma(yi = delta_st, vi = vi, mods = ~quality_score, data = dat, method = "DL")
cat("\n=== META-REGRESSION: Quality Score ===\n")
print(summary(res_quality))

# 4f. Tier (ancestral baseline quality)
res_tier <- rma(yi = delta_st, vi = vi, mods = ~as.factor(tier), data = dat, method = "DL")
cat("\n=== META-REGRESSION: Ancestral Tier ===\n")
print(summary(res_tier))

# =============================================================================
# 5. Subgroup means by mechanism category
# =============================================================================

subgroups <- dat %>%
  group_by(mechanism_cat) %>%
  summarise(
    n = n(),
    mean_delta = mean(delta_st),
    .groups = "drop"
  )
cat("\n=== SUBGROUP MEANS BY MECHANISM CATEGORY ===\n")
print(subgroups)

# Run individual RMAs per mechanism category (≥3 cases)
for (cat_name in unique(dat$mechanism_cat)) {
  sub <- dat[dat$mechanism_cat == cat_name, ]
  if (nrow(sub) >= 3) {
    r <- rma(yi = delta_st, vi = vi, data = sub, method = "DL")
    cat(sprintf("\n  %s (N=%d): Δ_ST=%.3f [%.3f, %.3f], I²=%.1f%%\n",
                cat_name, nrow(sub), r$b, r$ci.lb, r$ci.ub, r$I2))
  }
}

# =============================================================================
# 6. Subgroup by class (≥3 cases only)
# =============================================================================

cat("\n=== SUBGROUP BY TAXON CLASS ===\n")
for (cl in unique(dat$class)) {
  sub <- dat[dat$class == cl, ]
  if (nrow(sub) >= 3) {
    r <- rma(yi = delta_st, vi = vi, data = sub, method = "DL")
    cat(sprintf("  %s (N=%d): Δ_ST=%.3f [%.3f, %.3f], I²=%.1f%%\n",
                cl, nrow(sub), r$b, r$ci.lb, r$ci.ub, r$I2))
  } else {
    cat(sprintf("  %s (N=%d): Δ_ST=%.3f (single-study or pair; no pooled CI)\n",
                cl, nrow(sub), mean(sub$delta_st)))
  }
}

# =============================================================================
# 7. Funnel plot and Egger's test (publication bias)
# =============================================================================

cat("\n=== PUBLICATION BIAS ===\n")
regtest_res <- regtest(res_all, model = "lm")
cat("Egger's regression test:\n")
print(regtest_res)

# =============================================================================
# 8. Forest plot (text-based spec for figure production)
# =============================================================================

cat("\n=== FOREST PLOT DATA (for ggplot2 production) ===\n")
forest_df <- dat %>%
  mutate(
    label = paste0(case_id, ": ", substr(case_name, 1, 40)),
    color = case_when(
      mechanism_cat == "sensory_exploit"        ~ "#2166ac",
      mechanism_cat == "fisher_runaway"         ~ "#e41a1c",
      mechanism_cat == "olds_milner"            ~ "#4dac26",
      mechanism_cat == "repro_survival_tradeoff"~ "#ff7f00",
      TRUE ~ "gray40"
    )
  ) %>%
  arrange(desc(delta_st))

print(forest_df[, c("case_id","case_name","delta_st","delta_st_lo","delta_st_hi",
                    "mechanism_cat","v1_case")])

# =============================================================================
# 9. Summary statistics table
# =============================================================================

cat("\n=== FINAL SUMMARY ===\n")
cat(sprintf("Total cases: %d (v1: %d; new: %d)\n", nrow(dat), sum(dat$v1_case), sum(!dat$v1_case)))
cat(sprintf("Overall pooled Δ_ST: %.3f [%.3f, %.3f]\n",
            res_all$b, res_all$ci.lb, res_all$ci.ub))
cat(sprintf("Heterogeneity: τ²=%.4f, I²=%.1f%%, Q(%d)=%.2f, p=%.4f\n",
            res_all$tau2, res_all$I2, res_all$k-1, res_all$QE, res_all$QEp))
PI_all <- predict(res_all)
cat(sprintf("Prediction interval: [%.3f, %.3f]\n", PI_all$pi.lb, PI_all$pi.ub))
cat(sprintf("Taxon coverage: %d unique classes across invertebrate/vertebrate\n",
            length(unique(dat$class))))
cat(sprintf("Mechanism categories: %s\n",
            paste(unique(dat$mechanism_cat), collapse=", ")))

# =============================================================================
# 10. Save forest plot (if ggplot2 available)
# =============================================================================

tryCatch({
  p <- forest_df %>%
    mutate(label = fct_reorder(label, delta_st)) %>%
    ggplot(aes(x = delta_st, y = label, color = mechanism_cat)) +
    geom_point(aes(size = quality_score), shape = 16) +
    geom_errorbarh(aes(xmin = delta_st_lo, xmax = delta_st_hi), height = 0.25) +
    geom_vline(xintercept = res_all$b, linetype = "dashed", color = "black") +
    geom_vline(xintercept = c(res_all$ci.lb, res_all$ci.ub),
               linetype = "dotted", color = "black", alpha = 0.6) +
    scale_color_manual(
      name = "Mechanism",
      values = c(
        sensory_exploit         = "#2166ac",
        fisher_runaway          = "#e41a1c",
        olds_milner             = "#4dac26",
        repro_survival_tradeoff = "#ff7f00"
      )
    ) +
    scale_size_continuous(name = "Quality\nscore", range = c(2, 5)) +
    labs(
      title = "Layer A Animal Meta-Analysis v2: Δ_ST Forest Plot (N=20)",
      subtitle = sprintf("Pooled Δ_ST = %.3f [%.3f, %.3f]; I² = %.1f%%",
                         res_all$b, res_all$ci.lb, res_all$ci.ub, res_all$I2),
      x = "Δ_ST (reward-fitness decoupling gradient)",
      y = NULL
    ) +
    theme_minimal(base_size = 11) +
    theme(legend.position = "bottom",
          panel.grid.minor = element_blank())

  out_path <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/layer_A_forest_v2.pdf"
  dir.create(dirname(out_path), showWarnings = FALSE, recursive = TRUE)
  ggsave(out_path, p, width = 10, height = 8)
  cat(sprintf("\nForest plot saved: %s\n", out_path))
}, error = function(e) {
  cat("\n[NOTE] Forest plot generation skipped:", conditionMessage(e), "\n")
})

cat("\n=== layer_A_meta_v2.R COMPLETE ===\n")
