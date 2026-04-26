#!/usr/bin/env Rscript
# mr_2sample_pilot.R
# ========================
# 2-sample Mendelian Randomization pilot for Sweet Trap Layer D.
#
# Design (4 primary chains + extras):
#   Chain 1  Risk-taking (UKB GCST006810) -> F5_DEPRESSIO + ANTIDEPRESSANTS
#   Chain 2  Drinks/week (Liu GSCAN ieu-b-73) -> ALCOPANCCHRON + K11_ALCOLIV
#   Chain 3  BMI (Yengo GIANT ieu-b-40) -> DM_NEPHROPATHY + C_STROKE + T2D
#   Chain 4  Insomnia (UKB-b-3957) -> F5_DEPRESSIO
#   Chain 5  (positive control) Educational attainment (ieu-a-1239) -> F5_DEPRESSIO
#
# Pipeline:
#   (1) extract exposure instruments from IEU OpenGWAS via ieugwasr (p<5e-8, r2<0.001)
#   (2) parse local Finngen R12 summary stats, extract SNPs matching IVs
#   (3) harmonise (TwoSampleMR::harmonise_data)
#   (4) run IVW (random), MR-Egger, weighted median, MR-PRESSO, leave-one-out, Steiger
#   (5) write all results to 02-data/processed/mr_results_all_chains.csv
#       + harmonised table to mr_harmonised_data.parquet (via arrow)
# Compute:
#   * n_workers=1 (sequential). One Finngen file loaded at a time.
#   * Finngen files ~100-500MB gzip; we extract only SNPs in IV list (fread + filter).

suppressPackageStartupMessages({
  library(data.table); library(dplyr); library(tidyr); library(readr)
  library(TwoSampleMR); library(ieugwasr); library(MRPRESSO)
})

PROJ   <- "/Users/andy/Desktop/Research/sweet-trap-multidomain"
FINDIR <- "/Volumes/P1/城市研究/UKB_芬兰Finngen_catalog_ieu/gwas_list/Finngen/R12_summary_stats"
LOGP   <- file.path(PROJ, "03-analysis/scripts/mr_2sample_pilot.log")
OUTP   <- file.path(PROJ, "02-data/processed")

# redirect cat/message to log
sink(LOGP, split = TRUE, type = "output")
sink(LOGP, append = TRUE, type = "message")

msg <- function(...) cat(sprintf("[%s] ", format(Sys.time(), "%H:%M:%S")), ..., "\n", sep = "")

msg("=== Sweet Trap Layer D MR pilot ===")
msg("R version: ", R.version.string)
msg("TwoSampleMR: ", as.character(packageVersion("TwoSampleMR")))
msg("ieugwasr: ", as.character(packageVersion("ieugwasr")))

# ---------------------------------------------------------------
# Define chains
# ---------------------------------------------------------------
chains <- tribble(
  ~chain, ~exposure_label,           ~exposure_id,            ~outcome_label,                 ~outcome_phenocode,           ~outcome_ncase, ~outcome_nctrl,
  "1",   "risk_tolerance",          "ebi-a-GCST006810",      "F5_DEPRESSIO",                 "F5_DEPRESSIO",                59333,  434831,
  "1b",  "risk_tolerance",          "ebi-a-GCST006810",      "ANTIDEPRESSANTS",              "ANTIDEPRESSANTS",             149403, 111976,
  "2",   "drinks_per_week",         "ieu-b-73",              "ALCOPANCCHRON",                "ALCOPANCCHRON",               2400,   497948,
  "2b",  "drinks_per_week",         "ieu-b-73",              "K11_ALCOLIV",                  "K11_ALCOLIV",                 3769,   485213,
  "3a",  "bmi",                     "ieu-b-40",              "DM_NEPHROPATHY",               "DM_NEPHROPATHY",              5579,   90951,
  "3b",  "bmi",                     "ieu-b-40",              "C_STROKE",                     "C_STROKE",                    53492,  360342,
  "3c",  "bmi",                     "ieu-b-40",              "T2D",                          "T2D",                         82878,  403489,
  "4",   "insomnia",                "ukb-b-3957",            "F5_DEPRESSIO",                 "F5_DEPRESSIO",                59333,  434831,
  "5",   "educational_attainment",  "ieu-a-1239",            "F5_DEPRESSIO",                 "F5_DEPRESSIO",                59333,  434831
)
msg("chains defined: n=", nrow(chains))

# ---------------------------------------------------------------
# 1) Extract exposure instruments (one per exposure)
# ---------------------------------------------------------------
exposures_unique <- unique(chains$exposure_id)
msg("unique exposures: ", paste(exposures_unique, collapse=", "))

# cache results per exposure
iv_cache <- list()
for (eid in exposures_unique) {
  msg("-- extracting instruments for ", eid)
  iv <- tryCatch(
    extract_instruments(outcomes = eid, p1 = 5e-8, clump = TRUE, r2 = 0.001, kb = 10000),
    error = function(e) { msg("  ERR: ", conditionMessage(e)); NULL }
  )
  if (is.null(iv) || nrow(iv) == 0) {
    msg("  0 instruments returned — try with r2=0.01 relaxed")
    iv <- tryCatch(
      extract_instruments(outcomes = eid, p1 = 5e-8, clump = TRUE, r2 = 0.01, kb = 5000),
      error = function(e) NULL
    )
  }
  if (!is.null(iv)) {
    msg("  IVs: ", nrow(iv), " (F-stat range ", round(min(iv$beta.exposure^2/iv$se.exposure^2,na.rm=TRUE),1),
        "-", round(max(iv$beta.exposure^2/iv$se.exposure^2,na.rm=TRUE),1), ")")
    iv_cache[[eid]] <- iv
  } else {
    msg("  failed entirely")
    iv_cache[[eid]] <- NULL
  }
}

# persist raw IV tables
for (eid in names(iv_cache)) {
  if (!is.null(iv_cache[[eid]])) {
    fwrite(iv_cache[[eid]], file.path(OUTP, sprintf("mr_iv_%s.csv", gsub("[^A-Za-z0-9]", "_", eid))))
  }
}

# ---------------------------------------------------------------
# 2) Parse Finngen for matching SNPs per outcome
# ---------------------------------------------------------------
# Finngen R12 columns (standard): #chrom pos ref alt rsids nearest_genes pval mlogp beta sebeta af_alt af_alt_cases af_alt_controls
fin_cache <- list()
outcomes_unique <- unique(chains$outcome_phenocode)

all_iv_rsids <- unique(unlist(lapply(iv_cache, function(x) if(!is.null(x)) x$SNP else NULL)))
msg("total unique IV rsids across all exposures: ", length(all_iv_rsids))

for (oc in outcomes_unique) {
  fpath <- file.path(FINDIR, sprintf("finngen_R12_%s.gz", oc))
  if (!file.exists(fpath)) { msg("MISSING file: ", fpath); fin_cache[[oc]] <- NULL; next }
  msg("-- parse Finngen ", oc, " (", round(file.info(fpath)$size/1024^2,1), " MB)")
  # full read is feasible (gz ~100-300MB -> ~1-3GB uncompressed text, 20M rows)
  # but faster: use data.table fread with select=needed
  dt <- tryCatch(
    fread(cmd = sprintf("gunzip -c %s", shQuote(fpath)),
          select = c("#chrom","pos","ref","alt","rsids","pval","beta","sebeta","af_alt"),
          nThread = 2, showProgress = FALSE),
    error = function(e) { msg("  fread ERR: ", conditionMessage(e)); NULL }
  )
  if (is.null(dt)) next
  msg("  full rows: ", nrow(dt))
  # filter: rows whose rsids (may be comma list) contain any of our IVs
  dt <- dt[grepl("rs", rsids)]
  # explode rsid field (Finngen uses comma delim e.g. "rs123,rs456")
  # for speed, match by substring first
  pattern <- paste0("\\b(", paste(all_iv_rsids, collapse="|"), ")\\b")
  dt_match <- dt[grepl(pattern, rsids)]
  msg("  rows matching any IV rsid: ", nrow(dt_match))
  # extract the matched rsid
  dt_match[, match_rs := regmatches(rsids, regexpr(pattern, rsids))]
  setnames(dt_match, old=c("#chrom","pos","ref","alt","pval","beta","sebeta","af_alt"),
                     new=c("chrom","pos","ref","alt","pval","beta","se","eaf"))
  fin_cache[[oc]] <- dt_match
  rm(dt); gc(verbose = FALSE)
}

# ---------------------------------------------------------------
# 3) Run MR for each chain
# ---------------------------------------------------------------
results <- list()
harmonised_all <- list()

for (i in seq_len(nrow(chains))) {
  ch <- chains[i,]
  msg(sprintf("=== CHAIN %s: %s -> %s ===", ch$chain, ch$exposure_label, ch$outcome_label))

  iv <- iv_cache[[ch$exposure_id]]
  fo <- fin_cache[[ch$outcome_phenocode]]
  if (is.null(iv) || is.null(fo)) {
    msg("  skip: missing IV or outcome"); next
  }

  # build outcome data subset for this exposure's rsids
  oc_sub <- fo[match_rs %in% iv$SNP]
  msg("  IVs in exposure: ", nrow(iv), " | overlapping in outcome: ", nrow(oc_sub))
  if (nrow(oc_sub) < 3) { msg("  skip: < 3 overlapping IVs"); next }

  # format outcome data for TwoSampleMR
  oc_df <- data.frame(
    SNP = oc_sub$match_rs,
    beta.outcome = oc_sub$beta,
    se.outcome   = oc_sub$se,
    effect_allele.outcome = toupper(oc_sub$alt),   # Finngen: alt = effect allele
    other_allele.outcome  = toupper(oc_sub$ref),
    eaf.outcome = oc_sub$eaf,
    pval.outcome = oc_sub$pval,
    outcome = ch$outcome_label,
    id.outcome = ch$outcome_phenocode,
    stringsAsFactors = FALSE
  )
  # cases/controls for binary
  oc_df$ncase.outcome <- ch$outcome_ncase
  oc_df$ncontrol.outcome <- ch$outcome_nctrl
  oc_df$samplesize.outcome <- ch$outcome_ncase + ch$outcome_nctrl
  oc_df$units.outcome <- "log odds"

  # harmonise
  har <- tryCatch(
    harmonise_data(exposure_dat = iv, outcome_dat = oc_df, action = 2),
    error = function(e) { msg("  harmonise ERR: ", conditionMessage(e)); NULL }
  )
  if (is.null(har) || nrow(har) == 0) { msg("  skip: harmonise empty"); next }
  msg("  harmonised SNPs (kept mr=TRUE): ", sum(har$mr_keep, na.rm=TRUE))
  har$chain <- ch$chain
  harmonised_all[[ch$chain]] <- har

  har_use <- har[har$mr_keep, , drop = FALSE]
  if (nrow(har_use) < 3) { msg("  skip: < 3 usable after harmonise"); next }

  # F-stat
  har_use$F <- (har_use$beta.exposure / har_use$se.exposure)^2
  meanF <- mean(har_use$F, na.rm=TRUE)
  msg(sprintf("  mean F = %.1f (n_IV used = %d)", meanF, nrow(har_use)))

  # Main MR
  mr_res <- tryCatch(mr(har_use,
    method_list = c("mr_ivw","mr_egger_regression","mr_weighted_median","mr_simple_mode","mr_weighted_mode")),
    error = function(e) { msg("  mr() ERR: ", conditionMessage(e)); NULL })
  if (is.null(mr_res)) next

  # pleiotropy
  plei <- tryCatch(mr_pleiotropy_test(har_use),
    error = function(e) NULL)
  # heterogeneity
  het <- tryCatch(mr_heterogeneity(har_use),
    error = function(e) NULL)
  # Steiger
  steiger <- tryCatch(directionality_test(har_use),
    error = function(e) NULL)
  # leave-one-out
  loo <- tryCatch(mr_leaveoneout(har_use),
    error = function(e) NULL)

  # MR-PRESSO (only if >=4 IVs, binary outcome -> BETA is log-odds)
  presso <- NULL
  if (nrow(har_use) >= 4) {
    presso <- tryCatch(
      run_mr_presso(har_use, NbDistribution = 1000, SignifThreshold = 0.05),
      error = function(e) { msg("  PRESSO ERR: ", conditionMessage(e)); NULL }
    )
  }

  # attach to results list
  results[[ch$chain]] <- list(
    chain = ch, mr = mr_res, plei = plei, het = het,
    steiger = steiger, loo = loo, presso = presso,
    nIV_used = nrow(har_use), meanF = meanF
  )

  # print summary
  mr_ivw <- mr_res[mr_res$method == "Inverse variance weighted", , drop=FALSE]
  if (nrow(mr_ivw) > 0) {
    b  <- mr_ivw$b; se <- mr_ivw$se; p <- mr_ivw$pval
    or_lo <- exp(b - 1.96*se); or_hi <- exp(b + 1.96*se); or <- exp(b)
    msg(sprintf("  [IVW] beta=%.4f (se=%.4f) OR=%.3f (95%% CI %.3f–%.3f) p=%.3g nIV=%d",
                b, se, or, or_lo, or_hi, p, mr_ivw$nsnp))
  }
  if (!is.null(plei) && nrow(plei) > 0) {
    msg(sprintf("  Egger intercept=%.4f se=%.4f p=%.3g", plei$egger_intercept, plei$se, plei$pval))
  }
  if (!is.null(het) && nrow(het) > 0) {
    ivh <- het[het$method == "Inverse variance weighted", , drop=FALSE]
    if (nrow(ivh) > 0) msg(sprintf("  Cochran Q=%.2f df=%d p=%.3g", ivh$Q, ivh$Q_df, ivh$Q_pval))
  }
}

# ---------------------------------------------------------------
# 4) Save results
# ---------------------------------------------------------------
# Flat results table
rows <- list()
for (chn in names(results)) {
  r <- results[[chn]]
  mr <- r$mr
  for (k in seq_len(nrow(mr))) {
    rows[[length(rows)+1]] <- data.frame(
      chain = chn,
      exposure = r$chain$exposure_label,
      outcome  = r$chain$outcome_label,
      method = mr$method[k], nsnp = mr$nsnp[k],
      beta = mr$b[k], se = mr$se[k], pval = mr$pval[k],
      or = exp(mr$b[k]), or_lo = exp(mr$b[k] - 1.96*mr$se[k]),
      or_hi = exp(mr$b[k] + 1.96*mr$se[k]),
      meanF = r$meanF, nIV_used = r$nIV_used,
      egger_intercept = ifelse(!is.null(r$plei) && nrow(r$plei)>0, r$plei$egger_intercept, NA),
      egger_intercept_p = ifelse(!is.null(r$plei) && nrow(r$plei)>0, r$plei$pval, NA),
      q_ivw = ifelse(!is.null(r$het) && any(r$het$method == "Inverse variance weighted"),
                     r$het$Q[r$het$method == "Inverse variance weighted"], NA),
      q_ivw_p = ifelse(!is.null(r$het) && any(r$het$method == "Inverse variance weighted"),
                       r$het$Q_pval[r$het$method == "Inverse variance weighted"], NA),
      steiger_dir = ifelse(!is.null(r$steiger) && nrow(r$steiger)>0, r$steiger$correct_causal_direction, NA),
      steiger_p   = ifelse(!is.null(r$steiger) && nrow(r$steiger)>0, r$steiger$steiger_pval, NA),
      presso_global_p = if (!is.null(r$presso) && length(r$presso)>0)
          tryCatch(r$presso[[1]]$`MR-PRESSO results`$`Global Test`$Pvalue, error=function(e) NA) else NA,
      stringsAsFactors = FALSE
    )
  }
}
all_res <- do.call(rbind, rows)
fwrite(all_res, file.path(OUTP, "mr_results_all_chains.csv"))
msg("wrote mr_results_all_chains.csv rows=", nrow(all_res))

# Harmonised data
if (length(harmonised_all) > 0) {
  har_df <- do.call(rbind, lapply(names(harmonised_all), function(k) {
    d <- harmonised_all[[k]]; d$chain_id <- k; d
  }))
  fwrite(har_df, file.path(OUTP, "mr_harmonised_data.csv"))
  if (requireNamespace("arrow", quietly = TRUE)) {
    arrow::write_parquet(har_df, file.path(OUTP, "mr_harmonised_data.parquet"))
    msg("wrote mr_harmonised_data.parquet")
  } else {
    msg("arrow not installed; harmonised saved as csv only")
  }
}

# leave-one-out tables per chain
for (chn in names(results)) {
  loo <- results[[chn]]$loo
  if (!is.null(loo)) fwrite(loo, file.path(OUTP, sprintf("mr_loo_chain%s.csv", chn)))
}

msg("=== DONE ===")
sink(NULL, type = "output"); sink(NULL, type = "message")
