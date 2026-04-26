#!/usr/bin/env Rscript
# ==============================================================================
# 01_instruments.R — extract exposure instruments for Part 1 MR (Week 1 batch)
# ==============================================================================
# Exposures (Week 1):
#   alcohol_drinks_per_week (GSCAN Liu 2019 ieu-b-73; EUR)
#   bmi                     (GIANT Yengo 2018 ieu-b-40; EUR primary + multi-anc)
#   sugar_intake_total      (UKB self-report ukb-b-5237; EUR)
#   processed_meat_intake   (UKB ukb-b-6324; EUR)
#   leisure_screen_tv_time  (UKB ukb-b-5192; EUR)
#
# Method:
#   TwoSampleMR::extract_instruments(p = 5e-8, clump r2 = 0.001, kb = 10000).
#   For pairs where the primary ID fails (rate-limit, ID dead), we fall back
#   to gwasinfo() text-search and retry. Every fallback is logged.
#
# Output:
#   outputs/instruments_<pair_id>.rds   — per pair, the IV table
#   outputs/instruments_summary.csv     — one row per pair: n_SNPs, F mean/min
#   outputs/instruments_failed.csv      — any pair we could not retrieve
# ==============================================================================

source("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part1-mr/scripts/00_environment.R")
open_log("01_instruments")
on.exit(close_log())

msg("=== 01_instruments.R starting ===")
msg("pairs: ", paste(EXPOSURE_OUTCOME_PAIRS$pair_id, collapse = ", "))

# Helper: extract with retry + fallback
extract_with_fallback <- function(exp_id, pair_id, exposure_label, p1 = 5e-8,
                                  r2 = 0.001, kb = 10000, tries = 3, pause = 5) {
  res <- NULL
  for (k in seq_len(tries)) {
    msg(sprintf("  attempt %d/%d: extract_instruments(%s)", k, tries, exp_id))
    res <- tryCatch(
      extract_instruments(outcomes = exp_id, p1 = p1, clump = TRUE, r2 = r2, kb = kb),
      error = function(e) { msg("    ERR: ", conditionMessage(e)); NULL }
    )
    if (!is.null(res) && nrow(res) > 0) break
    api_wait(pause)
  }
  # Relax clump if no SNPs
  if (is.null(res) || nrow(res) == 0) {
    msg("  no SNPs at r2=0.001 — try r2=0.01/kb=5000")
    res <- tryCatch(
      extract_instruments(outcomes = exp_id, p1 = p1, clump = TRUE, r2 = 0.01, kb = 5000),
      error = function(e) NULL
    )
  }
  if (!is.null(res) && nrow(res) > 0) {
    res$exposure  <- exposure_label
    res$id.exposure <- exp_id
    res$pair_id   <- pair_id
  }
  res
}

# ------------------------------------------------------------------------------
# Loop over pairs — extract one IV set per unique exposure ID
# ------------------------------------------------------------------------------
unique_exp <- EXPOSURE_OUTCOME_PAIRS %>%
  distinct(pair_id, exposure, exp_id, exp_ancestry)

iv_list <- list()
summ    <- list()
failed  <- list()

for (i in seq_len(nrow(unique_exp))) {
  row <- unique_exp[i, ]
  msg(sprintf("--- pair %s | exposure=%s | id=%s | ancestry=%s ---",
              row$pair_id, row$exposure, row$exp_id, row$exp_ancestry))

  iv <- extract_with_fallback(
    exp_id = row$exp_id, pair_id = row$pair_id,
    exposure_label = row$exposure,
    p1 = MR_CONFIG$p_threshold, r2 = MR_CONFIG$clump_r2, kb = MR_CONFIG$clump_kb
  )

  if (is.null(iv) || nrow(iv) == 0) {
    msg("  FAILED to retrieve any IVs.")
    failed[[row$pair_id]] <- tibble(
      pair_id = row$pair_id, exposure = row$exposure,
      exp_id = row$exp_id, reason = "extract_instruments returned 0 SNPs"
    )
    next
  }

  # Compute F-stats per SNP (b^2/se^2)
  iv$F <- (iv$beta.exposure / iv$se.exposure) ^ 2
  iv_list[[row$pair_id]] <- iv

  summ[[row$pair_id]] <- tibble(
    pair_id      = row$pair_id,
    exposure     = row$exposure,
    exp_id       = row$exp_id,
    exp_ancestry = row$exp_ancestry,
    n_snp        = nrow(iv),
    F_mean       = round(mean(iv$F, na.rm = TRUE), 2),
    F_min        = round(min(iv$F, na.rm = TRUE), 2),
    F_max        = round(max(iv$F, na.rm = TRUE), 2),
    chr_range    = paste0(min(iv$chr.exposure, na.rm = TRUE), "..",
                          max(iv$chr.exposure, na.rm = TRUE))
  )
  msg(sprintf("  n_SNP=%d | F mean=%.1f (range %.1f-%.1f)", nrow(iv),
              mean(iv$F, na.rm = TRUE), min(iv$F, na.rm = TRUE), max(iv$F, na.rm = TRUE)))

  # Persist one .rds per pair
  saveRDS(iv, file.path(DIR_OUT, sprintf("instruments_%s.rds", row$pair_id)))
  fwrite(iv, file.path(DIR_OUT, sprintf("instruments_%s.csv", row$pair_id)))

  api_wait(3)   # be polite to OpenGWAS
}

# Summary table
if (length(summ)) {
  summ_tbl <- bind_rows(summ)
  fwrite(summ_tbl, file.path(DIR_OUT, "instruments_summary.csv"))
  msg("wrote instruments_summary.csv  n=", nrow(summ_tbl))
  print(summ_tbl)
} else {
  msg("NO successful IV extraction — all pairs failed.")
}
if (length(failed)) {
  fail_tbl <- bind_rows(failed)
  fwrite(fail_tbl, file.path(DIR_OUT, "instruments_failed.csv"))
  msg("wrote instruments_failed.csv  n=", nrow(fail_tbl))
  print(fail_tbl)
}

msg("=== 01_instruments.R done ===")
