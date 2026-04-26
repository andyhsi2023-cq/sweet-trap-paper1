#!/usr/bin/env Rscript
# ==============================================================================
# 05_sensitivity.R — instrument strength, pleiotropy diagnostics, Cook's D,
#                    Steiger-filtered re-MR, and MVMR (where applicable)
# ==============================================================================
# Sensitivity analyses for every pair x ancestry combo:
#   (a) Per-instrument F-statistic distribution (mean, min, fraction below 10)
#   (b) MR-Egger I^2 (Bowden 2016) for instrument strength under NOME violation
#   (c) Steiger-filtered MR (retain only SNPs with correct causal direction),
#       then re-run IVW / Egger / WM
#   (d) Cook's-D on the IVW regression of beta.outcome on beta.exposure
#   (e) MVMR for BMI and alcohol — control for genetic correlation with a
#       second exposure to probe pleiotropy (BMI adjusted for drinks/wk;
#       alcohol adjusted for BMI). This is the causal-genetic sensitivity.
#
# Colocalisation (coloc.abf) is deferred to Part 1 Week 2 once region-level
# summary stats can be pulled for top loci (not addressable from tophits-only
# OpenGWAS extract); we log it as a known next step.
#
# Outputs:
#   outputs/sens_instrument_strength.csv   # F, I2, weak-IV metrics
#   outputs/sens_steiger_filtered.csv      # IVW/Egger/WM after Steiger filter
#   outputs/sens_cooks_d.csv               # Cook's D per SNP (top-tail)
#   outputs/sens_mvmr.csv                  # MVMR estimates
# ==============================================================================

source("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part1-mr/scripts/00_environment.R")
open_log("05_sensitivity")
on.exit(close_log())

msg("=== 05_sensitivity.R starting ===")

hfiles <- list.files(DIR_OUT, pattern = "^harmonised_.+\\.rds$", full.names = TRUE)
msg("found ", length(hfiles), " harmonised files")

parse_name <- function(f) {
  base <- sub("^harmonised_", "", tools::file_path_sans_ext(basename(f)))
  parts <- strsplit(base, "_")[[1]]
  list(pair_id = paste(parts[-length(parts)], collapse = "_"),
       ancestry = parts[length(parts)])
}

inst_rows     <- list()
stfilt_rows   <- list()
cooks_rows    <- list()

for (f in hfiles) {
  ids <- parse_name(f); pid <- ids$pair_id; anc <- ids$ancestry
  msg(sprintf("--- sensitivity on %s | ancestry=%s ---", pid, anc))
  har <- readRDS(f)
  if (!"mr_keep" %in% colnames(har)) har$mr_keep <- TRUE
  h <- har[!is.na(har$mr_keep) & as.logical(har$mr_keep), , drop = FALSE]
  n <- nrow(h); if (n < 3) { msg("  skip: n<3"); next }

  # (a) F-stat per SNP
  h$F <- (h$beta.exposure / h$se.exposure)^2
  f_mean <- mean(h$F, na.rm = TRUE)
  f_min  <- min(h$F, na.rm = TRUE)
  f_frac_weak <- mean(h$F < 10, na.rm = TRUE)

  # (b) I^2_GX (instrument strength adjusting for NOME)
  #     Standard formula (Bowden 2016): I^2 = (Q - (k-1)) / Q   where
  #     Q = sum( (beta.exp - mean(beta.exp, weighted))^2 / se.exp^2 ).
  w <- 1 / (h$se.exposure^2)
  bx_mean_w <- sum(w * h$beta.exposure) / sum(w)
  Qx <- sum(w * (h$beta.exposure - bx_mean_w)^2)
  i2_gx <- max(0, (Qx - (n - 1)) / Qx)

  inst_rows[[paste(pid, anc, sep = "_")]] <- tibble(
    pair_id = pid, ancestry = anc, n_snp = n,
    F_mean = f_mean, F_min = f_min, F_frac_below_10 = f_frac_weak,
    Qx = Qx, i2_gx = i2_gx
  )
  msg(sprintf("  F mean=%.1f min=%.1f frac<10=%.1f%% | Qx=%.1f I2_gx=%.3f",
              f_mean, f_min, 100 * f_frac_weak, Qx, i2_gx))

  # (c) Steiger-filter: keep only SNPs where r2_exposure > r2_outcome.
  # Use approximate r2 from beta/se + EAF when r.exposure / r.outcome are
  # missing (continuous-trait approximation used elsewhere in TwoSampleMR).
  h2 <- tryCatch(steiger_filtering(h), error = function(e) NULL)
  if (!is.null(h2) && "steiger_dir" %in% colnames(h2)) {
    kept <- sum(h2$steiger_dir, na.rm = TRUE)
    msg(sprintf("  Steiger filter: kept=%d / %d", kept, nrow(h2)))
    if (kept >= 3) {
      hf <- h2[h2$steiger_dir %in% TRUE, , drop = FALSE]
      mr_sf <- tryCatch(mr(hf, method_list =
                           c("mr_ivw", "mr_egger_regression", "mr_weighted_median")),
                        error = function(e) NULL)
      if (!is.null(mr_sf) && nrow(mr_sf) > 0) {
        mr_sf$pair_id <- pid; mr_sf$ancestry <- anc
        mr_sf$n_kept <- kept
        stfilt_rows[[paste(pid, anc, sep = "_")]] <- mr_sf
        ivw_sf <- mr_sf[mr_sf$method == "Inverse variance weighted", , drop = FALSE]
        if (nrow(ivw_sf) > 0)
          msg(sprintf("  [IVW Steiger-filtered] b=%.4f se=%.4f OR=%.3f p=%.3g n_snp=%d",
                      ivw_sf$b, ivw_sf$se, exp(ivw_sf$b), ivw_sf$pval, kept))
      }
    }
  } else {
    msg("  Steiger filter unavailable for this pair.")
  }

  # (d) Cook's distance on the simple IVW regression
  #     fit y = beta.outcome ~ beta.exposure with weights 1/se.outcome^2
  mod <- tryCatch(
    lm(h$beta.outcome ~ h$beta.exposure + 0, weights = 1 / h$se.outcome^2),
    error = function(e) NULL
  )
  if (!is.null(mod)) {
    cd <- cooks.distance(mod)
    top_thr <- 4 / n  # classical rule-of-thumb
    flags <- which(cd > top_thr)
    df <- tibble(pair_id = pid, ancestry = anc,
                 snp = h$SNP, beta.exposure = h$beta.exposure,
                 beta.outcome = h$beta.outcome, cooks_d = cd,
                 flag = cd > top_thr)
    cooks_rows[[paste(pid, anc, sep = "_")]] <- df
    msg(sprintf("  Cook's D>%.3f: %d SNP(s)", top_thr, length(flags)))
  }
}

# ------------------------------------------------------------------------------
# (e) MVMR — BMI and alcohol as joint exposures on mortality (EUR only)
# ------------------------------------------------------------------------------
mvmr_rows <- list()
msg("--- MVMR: BMI + alcohol -> all-cause mortality (EUR) ---")

mvmr_combo <- tryCatch({
  # use mv_extract_exposures to pull a jointly-clumped instrument panel
  exposures_mv <- c("ieu-b-40", "ieu-b-73")
  mv_exp <- mv_extract_exposures(id_exposure = exposures_mv,
                                 clump_r2 = MR_CONFIG$clump_r2,
                                 clump_kb = MR_CONFIG$clump_kb,
                                 harmonise_strictness = 2)
  # Use the Pilling 2017 parental longevity (father's attained age) EUR GWAS as
  # the all-cause-mortality proxy. Note: ebi-a-GCST006414 is Nielsen 2018 AF
  # (previously mis-labeled) and is NOT used here.
  mv_out <- extract_outcome_data(snps = mv_exp$SNP,
                                 outcomes = "ebi-a-GCST006701",
                                 proxies = TRUE)
  mv_har <- mv_harmonise_data(mv_exp, mv_out)
  fit_mv <- mv_multiple(mv_har)
  msg("  MVMR fit returned n_methods=", length(fit_mv))
  fit_mv
}, error = function(e) { msg("  MVMR ERR: ", conditionMessage(e)); NULL })

if (!is.null(mvmr_combo) && !is.null(mvmr_combo$result)) {
  r <- mvmr_combo$result
  r$or <- exp(r$b); r$or_lo <- exp(r$b - 1.96 * r$se); r$or_hi <- exp(r$b + 1.96 * r$se)
  fwrite(r, file.path(DIR_OUT, "sens_mvmr.csv"))
  msg("wrote sens_mvmr.csv")
  print(r)
} else {
  msg("  MVMR produced no result — skipped.")
}

# ------------------------------------------------------------------------------
# Write combined sensitivity outputs
# ------------------------------------------------------------------------------
if (length(inst_rows)) {
  fwrite(bind_rows(inst_rows), file.path(DIR_OUT, "sens_instrument_strength.csv"))
  msg("wrote sens_instrument_strength.csv")
}
if (length(stfilt_rows)) {
  fwrite(bind_rows(stfilt_rows), file.path(DIR_OUT, "sens_steiger_filtered.csv"))
  msg("wrote sens_steiger_filtered.csv")
}
if (length(cooks_rows)) {
  all_cd <- bind_rows(cooks_rows)
  # Keep only flagged rows to avoid bloat, plus top-5 per combo
  top_flags <- all_cd %>%
    dplyr::group_by(pair_id, ancestry) %>%
    dplyr::slice_max(cooks_d, n = 10, with_ties = FALSE) %>%
    dplyr::ungroup()
  fwrite(top_flags, file.path(DIR_OUT, "sens_cooks_d.csv"))
  msg("wrote sens_cooks_d.csv (top-10 per combo)")
}

msg("=== 05_sensitivity.R done ===")
