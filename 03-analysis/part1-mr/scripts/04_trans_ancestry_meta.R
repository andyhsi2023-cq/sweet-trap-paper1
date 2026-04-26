#!/usr/bin/env Rscript
# ==============================================================================
# 04_trans_ancestry_meta.R — random-effects meta across ancestries
# ==============================================================================
# Primary target: BMI -> all-cause mortality across {EUR, EAS, AFR}
#   (SAS and AMR are logged gaps — no public mortality GWAS.)
# Secondary: Alcohol -> mortality (EUR + EAS), Sugar -> CVD (EUR + EAS).
#
# Method: DerSimonian-Laird + REML random-effects via metafor::rma() on
#         IVW log-OR and SE. Report:
#           pooled beta & 95% CI
#           Cochran's Q heterogeneity + I^2 + tau^2
#           Between-study credibility intervals
#
# Outputs:
#   outputs/meta_trans_ancestry.csv
# ==============================================================================

source("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part1-mr/scripts/00_environment.R")
open_log("04_trans_ancestry_meta")
on.exit(close_log())

msg("=== 04_trans_ancestry_meta.R starting ===")

mr_tbl <- fread(file.path(DIR_OUT, "mr_main_week1.csv"))
msg("loaded mr_main_week1.csv rows=", nrow(mr_tbl))

# Use IVW as the summary effect per ancestry
ivw <- mr_tbl %>%
  dplyr::filter(method == "Inverse variance weighted") %>%
  dplyr::select(pair_id, ancestry, beta = b, se = se, pval = pval,
                nsnp = nsnp, meanF = meanF)
msg("IVW rows:\n")
print(ivw)

meta_rows <- list()

for (pid in unique(ivw$pair_id)) {
  sub <- ivw %>% dplyr::filter(pair_id == pid)
  if (nrow(sub) < 2) {
    msg(sprintf("SKIP %s — only %d ancestry, meta needs ≥2", pid, nrow(sub)))
    next
  }
  msg(sprintf("--- meta on %s (n_ancestry=%d) ---", pid, nrow(sub)))

  # DL
  fit_dl   <- tryCatch(metafor::rma(yi = sub$beta, sei = sub$se,
                                    method = "DL", slab = sub$ancestry),
                       error = function(e) { msg("  DL ERR: ", conditionMessage(e)); NULL })
  # REML
  fit_reml <- tryCatch(metafor::rma(yi = sub$beta, sei = sub$se,
                                    method = "REML", slab = sub$ancestry),
                       error = function(e) { msg("  REML ERR: ", conditionMessage(e)); NULL })
  # Fixed-effect (for comparison)
  fit_fe   <- tryCatch(metafor::rma(yi = sub$beta, sei = sub$se,
                                    method = "FE", slab = sub$ancestry),
                       error = function(e) { msg("  FE ERR: ", conditionMessage(e)); NULL })

  grab <- function(fit, method_label) {
    if (is.null(fit)) return(NULL)
    tibble(
      pair_id     = pid,
      meta_method = method_label,
      k           = fit$k,
      ancestries  = paste(sub$ancestry, collapse = ","),
      beta_pool   = fit$b[1, 1],
      se_pool     = fit$se,
      ci_lo       = fit$ci.lb,
      ci_hi       = fit$ci.ub,
      pval_pool   = fit$pval,
      or_pool     = exp(fit$b[1, 1]),
      or_lo       = exp(fit$ci.lb),
      or_hi       = exp(fit$ci.ub),
      q_stat      = fit$QE,
      q_df        = fit$k - 1,
      q_pval      = fit$QEp,
      i2          = fit$I2,
      h2          = fit$H2,
      tau2        = fit$tau2,
      tau2_se     = if (!is.null(fit$se.tau2)) fit$se.tau2 else NA_real_
    )
  }

  rows <- bind_rows(grab(fit_dl, "DL"), grab(fit_reml, "REML"), grab(fit_fe, "FE"))
  if (nrow(rows) > 0) {
    meta_rows[[pid]] <- rows
    # console summary (REML preferred)
    rr <- rows %>% dplyr::filter(meta_method == "REML")
    if (nrow(rr) > 0) {
      msg(sprintf("  REML pooled b=%.4f (%.4f-%.4f) OR=%.3f p=%.3g | Q=%.2f (df=%d) p=%.3g I2=%.1f%%",
                  rr$beta_pool, rr$ci_lo, rr$ci_hi, rr$or_pool, rr$pval_pool,
                  rr$q_stat, rr$q_df, rr$q_pval, rr$i2))
    }
  }
}

if (length(meta_rows)) {
  out <- bind_rows(meta_rows)
  fwrite(out, file.path(DIR_OUT, "meta_trans_ancestry.csv"))
  msg("wrote meta_trans_ancestry.csv rows=", nrow(out))
  print(out)
} else {
  msg("NO meta performed — insufficient multi-ancestry pairs")
}

msg("=== 04_trans_ancestry_meta.R done ===")
