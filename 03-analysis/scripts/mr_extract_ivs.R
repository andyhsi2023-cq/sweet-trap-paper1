#!/usr/bin/env Rscript
# mr_extract_ivs.R  — extract exposure IVs from IEU OpenGWAS, cache to disk.
# Runs independently of Finngen download.
suppressPackageStartupMessages({
  library(TwoSampleMR); library(ieugwasr); library(data.table); library(dplyr)
})
PROJ <- "/Users/andy/Desktop/Research/sweet-trap-multidomain"
OUTP <- file.path(PROJ, "02-data/processed")
LOGP <- file.path(PROJ, "03-analysis/scripts/mr_extract_ivs.log")
sink(LOGP, split = TRUE)

exposures <- c(
  risk_tolerance        = "ebi-a-GCST006810",
  drinks_per_week       = "ieu-b-73",
  bmi                   = "ieu-b-40",
  insomnia              = "ukb-b-3957",
  educational_attainment= "ieu-a-1239"
)

for (nm in names(exposures)) {
  eid <- exposures[[nm]]
  dst <- file.path(OUTP, sprintf("mr_iv_%s_%s.csv", nm, gsub("[^A-Za-z0-9]", "_", eid)))
  if (file.exists(dst)) { cat("skip ", nm, " (cached)\n"); next }
  cat(sprintf("[%s] extracting instruments for %s (%s)\n", format(Sys.time(), "%H:%M:%S"), nm, eid))
  iv <- tryCatch(
    extract_instruments(outcomes = eid, p1 = 5e-8, clump = TRUE, r2 = 0.001, kb = 10000),
    error = function(e) { cat("  ERR: ", conditionMessage(e), "\n"); NULL }
  )
  if (is.null(iv) || nrow(iv) == 0) {
    cat("  0 instruments; try r2=0.01\n")
    iv <- tryCatch(
      extract_instruments(outcomes = eid, p1 = 5e-8, clump = TRUE, r2 = 0.01, kb = 5000),
      error = function(e) NULL)
  }
  if (!is.null(iv)) {
    cat(sprintf("  IVs: %d | F range %.1f–%.1f\n",
        nrow(iv), min(iv$beta.exposure^2/iv$se.exposure^2,na.rm=TRUE),
        max(iv$beta.exposure^2/iv$se.exposure^2,na.rm=TRUE)))
    fwrite(iv, dst)
  } else {
    cat("  failed\n")
  }
}
sink(NULL)
