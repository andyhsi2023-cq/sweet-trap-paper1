#!/usr/bin/env Rscript
# ==============================================================================
# 03_mr_main.R — core 2-sample MR methods across all pair x ancestry combos
# ==============================================================================
# For each harmonised_<pair>_<ancestry>.rds produced by 02_outcomes.R, run:
#   - IVW (multiplicative random effects)
#   - MR-Egger (with intercept / pleiotropy test)
#   - Weighted median
#   - Simple mode & Weighted mode
#   - MR-PRESSO (outlier detection + global + distortion test if N>=4)
#   - Steiger filtering (directionality_test)
#   - Leave-one-out (IVW LOO)
#   - Radial MR (IVW radial, outlier detection with Bonferroni alpha)
#
# Outputs:
#   outputs/mr_main_week1.csv        — headline per pair x ancestry x method
#   outputs/mr_pleiotropy.csv        — Egger intercept + het Q per combo
#   outputs/mr_steiger.csv           — direction tests
#   outputs/mr_presso.csv            — PRESSO global + distortion
#   outputs/mr_loo_<pair>_<anc>.csv  — leave-one-out tables
#   outputs/mr_radial_outliers.csv   — any SNPs flagged by Radial-MR Q
# ==============================================================================

source("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part1-mr/scripts/00_environment.R")
open_log("03_mr_main")
on.exit(close_log())

`%||%` <- function(a, b) if (is.null(a) || length(a) == 0 || all(is.na(a))) b else a

msg("=== 03_mr_main.R starting ===")

# list harmonised inputs produced by 02_outcomes.R
hfiles <- list.files(DIR_OUT, pattern = "^harmonised_.+\\.rds$", full.names = TRUE)
msg("found ", length(hfiles), " harmonised files")
stopifnot(length(hfiles) > 0)

parse_name <- function(f) {
  # harmonised_<pair>_<anc>.rds
  base <- sub("^harmonised_", "", tools::file_path_sans_ext(basename(f)))
  parts <- strsplit(base, "_")[[1]]
  # pair can contain hyphens but not underscores, ancestry is last token
  anc  <- parts[length(parts)]
  pair <- paste(parts[-length(parts)], collapse = "_")
  list(pair_id = pair, ancestry = anc)
}

mr_rows     <- list()
plei_rows   <- list()
steig_rows  <- list()
presso_rows <- list()
radial_rows <- list()
summaries   <- list()

for (f in hfiles) {
  ids <- parse_name(f); pid <- ids$pair_id; anc <- ids$ancestry
  msg(sprintf("--- MR on %s | ancestry=%s ---", pid, anc))

  har <- readRDS(f)
  # Guard: mr_keep may be missing; recompute/fallback to TRUE if column absent
  if (!"mr_keep" %in% colnames(har)) har$mr_keep <- TRUE
  keep_idx <- !is.na(har$mr_keep) & as.logical(har$mr_keep)
  har_use <- har[keep_idx, , drop = FALSE]
  n_use <- nrow(har_use)
  msg(sprintf("  harmonised n=%d | mr_keep n=%d", nrow(har), n_use))
  if (n_use < 3) { msg("  skip: fewer than 3 SNPs usable"); next }

  # F-stat (re-computed for safety)
  har_use$F <- (har_use$beta.exposure / har_use$se.exposure)^2
  meanF <- mean(har_use$F, na.rm = TRUE)

  # -------- core MR --------
  mr_res <- tryCatch(
    mr(har_use,
       method_list = c("mr_ivw", "mr_egger_regression",
                       "mr_weighted_median", "mr_simple_mode", "mr_weighted_mode")),
    error = function(e) { msg("  mr() ERR: ", conditionMessage(e)); NULL }
  )
  if (is.null(mr_res)) next

  mr_res$pair_id <- pid
  mr_res$ancestry <- anc
  mr_res$nIV_used <- n_use
  mr_res$meanF    <- meanF
  mr_res$or       <- exp(mr_res$b)
  mr_res$or_lo    <- exp(mr_res$b - 1.96 * mr_res$se)
  mr_res$or_hi    <- exp(mr_res$b + 1.96 * mr_res$se)
  mr_rows[[paste(pid, anc, sep = "_")]] <- mr_res

  # One-line console summary (IVW)
  ivw <- mr_res[mr_res$method == "Inverse variance weighted", , drop = FALSE]
  if (nrow(ivw) > 0) {
    msg(sprintf("  [IVW]  b=%.4f se=%.4f OR=%.3f 95%%CI %.3f-%.3f p=%.3g n_snp=%d F=%.1f",
                ivw$b, ivw$se, ivw$or, ivw$or_lo, ivw$or_hi, ivw$pval, ivw$nsnp, meanF))
  }
  egg <- mr_res[mr_res$method == "MR Egger", , drop = FALSE]
  if (nrow(egg) > 0)
    msg(sprintf("  [Egg]  b=%.4f se=%.4f p=%.3g", egg$b, egg$se, egg$pval))
  wm <- mr_res[mr_res$method == "Weighted median", , drop = FALSE]
  if (nrow(wm) > 0)
    msg(sprintf("  [WM]   b=%.4f se=%.4f p=%.3g", wm$b, wm$se, wm$pval))

  # -------- pleiotropy + heterogeneity --------
  plei <- tryCatch(mr_pleiotropy_test(har_use), error = function(e) NULL)
  het  <- tryCatch(mr_heterogeneity(har_use, method_list = c("mr_ivw","mr_egger_regression")),
                   error = function(e) NULL)
  if (!is.null(plei) && nrow(plei) > 0) {
    plei$pair_id <- pid; plei$ancestry <- anc
  }
  # pull IVW Q from het
  q_ivw <- NA_real_; q_ivw_p <- NA_real_; q_egg <- NA_real_; q_egg_p <- NA_real_
  if (!is.null(het) && nrow(het) > 0) {
    r_ivw <- het[het$method == "Inverse variance weighted", , drop = FALSE]
    if (nrow(r_ivw) > 0) { q_ivw <- r_ivw$Q; q_ivw_p <- r_ivw$Q_pval }
    r_egg <- het[het$method == "MR Egger", , drop = FALSE]
    if (nrow(r_egg) > 0) { q_egg <- r_egg$Q; q_egg_p <- r_egg$Q_pval }
  }
  if (!is.null(plei) && nrow(plei) > 0) {
    plei$q_ivw <- q_ivw; plei$q_ivw_p <- q_ivw_p
    plei$q_egger <- q_egg; plei$q_egger_p <- q_egg_p
    plei_rows[[paste(pid, anc, sep = "_")]] <- plei
    msg(sprintf("  Egger intercept=%.4f (se=%.4f) p=%.3g | Q_ivw=%.2f p=%.3g",
                plei$egger_intercept, plei$se, plei$pval, q_ivw, q_ivw_p))
  }

  # -------- Steiger directionality --------
  stg <- tryCatch(directionality_test(har_use), error = function(e) NULL)
  if (!is.null(stg) && nrow(stg) > 0) {
    stg$pair_id <- pid; stg$ancestry <- anc
    steig_rows[[paste(pid, anc, sep = "_")]] <- stg
    msg(sprintf("  Steiger: correct_dir=%s r2_exp=%.4f r2_out=%.4f p=%.3g",
                as.character(stg$correct_causal_direction), stg$snp_r2.exposure,
                stg$snp_r2.outcome, stg$steiger_pval))
  }

  # -------- MR-PRESSO --------
  if (n_use >= 4 && n_use <= 200) {
    # MR-PRESSO needs N_boot > n_SNP * 1/alpha; auto-bump for large IV sets.
    # For n > 200 SNPs the permutation is O(minutes-hours); we rely on Radial-MR
    # for outlier detection in those cases (explicitly logged).
    nboot <- max(MR_CONFIG$presso_nboot, 20 * n_use)
    pr <- tryCatch(
      run_mr_presso(har_use, NbDistribution = nboot, SignifThreshold = 0.05),
      error = function(e) { msg("  PRESSO ERR: ", conditionMessage(e)); NULL }
    )
  } else if (n_use > 200) {
    msg(sprintf("  PRESSO: skipped (n_SNP=%d > 200; see Radial-MR outliers)", n_use))
    pr <- NULL
    if (!is.null(pr) && length(pr) > 0) {
      res  <- pr[[1]]
      mreps <- res$`Main MR results`
      global <- res$`MR-PRESSO results`$`Global Test`
      dist   <- res$`MR-PRESSO results`$`Distortion Test`

      # MR-PRESSO sometimes returns Pvalue as string "<0.001" when below
      # the empirical-null floor; coerce safely and store both numeric + string.
      to_num <- function(x) {
        if (is.null(x) || length(x) == 0) return(NA_real_)
        if (is.numeric(x)) return(x)
        # strip "<" or ">" prefix; if unparsable return NA
        xs <- as.character(x); xs2 <- sub("^[<>=]+", "", xs)
        suppressWarnings(as.numeric(xs2))
      }
      to_str <- function(x) {
        if (is.null(x) || length(x) == 0) return("NA")
        if (is.character(x)) return(x)
        if (is.numeric(x)) return(sprintf("%.3g", x))
        as.character(x)
      }

      global_p_num <- to_num(global$Pvalue)
      dist_p_num   <- to_num(dist$Pvalue)
      row <- tibble(
        pair_id     = pid, ancestry = anc,
        raw_b       = mreps$`Causal Estimate`[1],
        raw_se      = mreps$Sd[1],
        raw_p       = mreps$`P-value`[1],
        oc_b        = mreps$`Causal Estimate`[2],
        oc_se       = mreps$Sd[2],
        oc_p        = mreps$`P-value`[2],
        global_RSSobs = if (!is.null(global$RSSobs)) global$RSSobs else NA_real_,
        global_p    = global_p_num,
        global_p_raw = to_str(global$Pvalue),
        dist_p      = dist_p_num,
        n_outlier   = if (!is.null(res$`MR-PRESSO results`$`Distortion Test`$`Outliers Indices`))
                        length(res$`MR-PRESSO results`$`Distortion Test`$`Outliers Indices`) else 0
      )
      presso_rows[[paste(pid, anc, sep = "_")]] <- row

      msg(sprintf("  PRESSO: raw b=%.4f p=%.3g | oc b=%s p=%s | global p=%s n_outlier=%d",
                  row$raw_b, row$raw_p,
                  if (is.na(row$oc_b)) "NA" else sprintf("%.4f", row$oc_b),
                  if (is.na(row$oc_p)) "NA" else sprintf("%.3g", row$oc_p),
                  row$global_p_raw, row$n_outlier))
    }
  }

  # -------- Leave-one-out --------
  loo <- tryCatch(mr_leaveoneout(har_use), error = function(e) NULL)
  if (!is.null(loo)) {
    fwrite(loo, file.path(DIR_OUT, sprintf("mr_loo_%s_%s.csv", pid, anc)))
  }

  # -------- Radial MR --------
  rad <- tryCatch({
    # format for RadialMR
    rdat <- format_radial(BXG  = har_use$beta.exposure,
                          BYG  = har_use$beta.outcome,
                          seBXG = har_use$se.exposure,
                          seBYG = har_use$se.outcome,
                          RSID = har_use$SNP)
    ivw_r <- ivw_radial(rdat, alpha = MR_CONFIG$radial_alpha,
                        weights = 3, summary = FALSE)
    ivw_r
  }, error = function(e) { msg("  Radial ERR: ", conditionMessage(e)); NULL })
  if (!is.null(rad) && !is.null(rad$outliers) && is.data.frame(rad$outliers)) {
    out_df <- rad$outliers
    if (nrow(out_df) > 0) {
      out_df$pair_id <- pid; out_df$ancestry <- anc
      radial_rows[[paste(pid, anc, sep = "_")]] <- out_df
      msg(sprintf("  Radial: %d outlier(s) at alpha=%.3g", nrow(out_df),
                  MR_CONFIG$radial_alpha))
    } else {
      msg("  Radial: no outliers")
    }
  }

  summaries[[paste(pid, anc, sep = "_")]] <- tibble(
    pair_id = pid, ancestry = anc, n_SNP = n_use, F_mean = meanF
  )
}

# -------- write combined outputs --------
if (length(mr_rows)) {
  mr_tbl <- bind_rows(mr_rows)
  # Canonical column order
  mr_tbl <- mr_tbl %>%
    select(pair_id, ancestry, exposure, outcome, method, nsnp, b, se, pval,
           or, or_lo, or_hi, nIV_used, meanF, id.exposure, id.outcome)
  fwrite(mr_tbl, file.path(DIR_OUT, "mr_main_week1.csv"))
  msg("wrote mr_main_week1.csv rows=", nrow(mr_tbl))
}
if (length(plei_rows)) {
  fwrite(bind_rows(plei_rows), file.path(DIR_OUT, "mr_pleiotropy.csv"))
  msg("wrote mr_pleiotropy.csv")
}
if (length(steig_rows)) {
  fwrite(bind_rows(steig_rows), file.path(DIR_OUT, "mr_steiger.csv"))
  msg("wrote mr_steiger.csv")
}
if (length(presso_rows)) {
  fwrite(bind_rows(presso_rows), file.path(DIR_OUT, "mr_presso.csv"))
  msg("wrote mr_presso.csv")
}
if (length(radial_rows)) {
  fwrite(bind_rows(radial_rows), file.path(DIR_OUT, "mr_radial_outliers.csv"))
  msg("wrote mr_radial_outliers.csv")
}
if (length(summaries)) {
  fwrite(bind_rows(summaries), file.path(DIR_OUT, "mr_combo_summary.csv"))
}

msg("=== 03_mr_main.R done ===")
