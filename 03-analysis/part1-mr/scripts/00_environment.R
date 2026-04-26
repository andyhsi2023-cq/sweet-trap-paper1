#!/usr/bin/env Rscript
# ==============================================================================
# 00_environment.R — Part 1 MR pipeline (Sweet Trap V4, H1c causal stream)
# ==============================================================================
# Purpose:   Load libraries, set seeds and paths, register OpenGWAS JWT token,
#            define the 5 exposure-outcome pairs for the trans-ancestry MR
#            battery, and record an execution-log header. This file is
#            source()'d by 01-05 scripts at their top.
#
# Pipeline (Week 1 first batch):
#   01_instruments.R         — pull exposure IVs from OpenGWAS
#   02_outcomes.R            — pull ancestry-matched mortality outcome stats
#   03_mr_main.R             — IVW / Egger / WM / WMo / PRESSO / Steiger / LOO / Radial
#   04_trans_ancestry_meta.R — random-effects meta across 5 ancestries (BMI pair)
#   05_sensitivity.R         — MVMR / Egger I2 / F-stats / coloc / Cook's D
#
# Known constraints:
#   - OpenGWAS: JWT-authenticated, 100k variants/10-min rate-limit.
#   - BBJ/FinnGen outcome GWAS may lack effect_allele frequency for some SNPs.
#   - All of Us summary stats not yet downloadable (registration pending);
#     logged as known gap.
#
# Compute rules (CLAUDE.md):  n_workers <= 2, sequential where possible.
# ==============================================================================

suppressPackageStartupMessages({
  # Use system library explicitly — project renv lacks the MR toolchain.
  .libPaths(c("/opt/homebrew/lib/R/4.5/site-library",
              "/opt/homebrew/Cellar/r/4.5.3/lib/R/library",
              .libPaths()))

  library(data.table)
  library(dplyr)
  library(tidyr)
  library(readr)
  library(tibble)
  library(purrr)

  library(TwoSampleMR)
  library(MendelianRandomization)
  library(ieugwasr)
  library(MRPRESSO)
  library(MVMR)
  library(coloc)
  library(RadialMR)
  library(metafor)
  library(here)
})

# ------------------------------------------------------------------------------
# 0. OpenGWAS authentication
# ------------------------------------------------------------------------------
# Token is stored in project-level .Renviron (OPENGWAS_JWT=...). If for some
# reason the variable is empty (e.g. running R --vanilla), read the .Renviron
# manually. Tokens are per-user; do not commit .Renviron to git.
.jwt <- Sys.getenv("OPENGWAS_JWT", unset = "")
if (!nzchar(.jwt)) {
  .ren <- file.path("/Users/andy/Desktop/Research/sweet-trap-multidomain", ".Renviron")
  if (file.exists(.ren)) {
    .kv <- readLines(.ren, warn = FALSE)
    .kv <- .kv[grepl("^OPENGWAS_JWT=", .kv)][1]
    if (!is.na(.kv)) {
      .jwt <- sub("^OPENGWAS_JWT=", "", .kv)
      Sys.setenv(OPENGWAS_JWT = .jwt)
    }
  }
}
stopifnot(nzchar(Sys.getenv("OPENGWAS_JWT")))

# ------------------------------------------------------------------------------
# 1. Paths
# ------------------------------------------------------------------------------
PROJ_ROOT <- "/Users/andy/Desktop/Research/sweet-trap-multidomain"
P1_ROOT   <- file.path(PROJ_ROOT, "03-analysis", "part1-mr")

DIR_SCRIPTS <- file.path(P1_ROOT, "scripts")
DIR_DATA    <- file.path(P1_ROOT, "data")
DIR_OUT     <- file.path(P1_ROOT, "outputs")
DIR_LOGS    <- file.path(P1_ROOT, "logs")

for (d in c(DIR_DATA, DIR_OUT, DIR_LOGS)) dir.create(d, recursive = TRUE, showWarnings = FALSE)

# ------------------------------------------------------------------------------
# 2. Random seed
# ------------------------------------------------------------------------------
SEED <- 20260424L
set.seed(SEED)

# ------------------------------------------------------------------------------
# 3. Exposure-outcome pairs — Week 1 first batch
# ------------------------------------------------------------------------------
# Column meaning:
#   pair_id      — short label for table joins
#   exposure     — descriptive name
#   exp_id       — OpenGWAS study ID (primary instrument source)
#   exp_ancestry — EUR / EAS / multi
#   outcome      — descriptive name
#   out_ids      — semicolon-separated OpenGWAS IDs per ancestry in preference order
#                  (empty slot "-" = known gap, not available via OpenGWAS)
#   ancestries   — comma-separated ancestry codes planned for this pair
#
# Ancestry codes: EUR = European, EAS = East Asian, AFR = African,
#                 SAS = South Asian, AMR = Admixed American.
#
# Selection rationale:
#   Pair 1  Alcohol: GSCAN drinks/wk (ieu-b-73 EUR; Saunders 2022 EAS in BBJ
#           release). Outcome: all-cause mortality (Pilling/Deelen IEU-a-1100 EUR;
#           BBJ ebi-a mortality or "longevity" proxy when absent).
#   Pair 2  BMI: GIANT 2018 Yengo (ieu-b-40) + BBJ/AGEN multi-ancestry (Akiyama 2017)
#           → 5 ancestries via Pan-UKB / GBMI. Outcome: mortality.
#   Pair 3  Sugar intake: UKB self-report total sugar (ukb-b-XXX). Outcome:
#           CVD mortality (cardiovascular) via UKB + BBJ.
#   Pair 4  UPF proxy: UKB diet pattern PGS / "processed meat" proxy
#           (ukb-b-*). Outcome: mortality. EUR only.
#   Pair 5  Leisure screen time: UKB leisure sedentary time (ukb-b-3837;
#           van de Vegte 2020 GCST90093138 TV-watching). Outcome: mortality. EUR.
#
# NOTE: Exact OpenGWAS IDs are resolved at runtime in 01_instruments.R /
#       02_outcomes.R via gwasinfo(trait = ...) query; the IDs below are the
#       preferred first-choice. Fallbacks handled by script, not hard-coded here.
# ------------------------------------------------------------------------------

EXPOSURE_OUTCOME_PAIRS <- tribble(
  ~pair_id,     ~exposure,                   ~exp_id,            ~exp_ancestry, ~outcome,                           ~ancestries,
  "alc-mort",   "alcohol_drinks_per_week",   "ieu-b-73",         "EUR",         "all_cause_mortality",              "EUR,EAS",
  "bmi-mort",   "bmi",                       "ieu-b-40",         "EUR",         "all_cause_mortality",              "EUR,EAS,AFR,SAS,AMR",
  "sug-cvdm",   "sugar_intake_total",        "ukb-b-5237",       "EUR",         "cardiovascular_mortality",         "EUR,EAS",
  "upf-mort",   "processed_meat_intake",     "ukb-b-6324",       "EUR",         "all_cause_mortality",              "EUR",
  "scr-mort",   "leisure_screen_tv_time",    "ukb-b-5192",       "EUR",         "all_cause_mortality",              "EUR"
)

# Preferred OpenGWAS outcome IDs per ancestry (resolved by 02_outcomes.R;
# missing cells trigger a trait-search fallback).
OUTCOME_ID_MAP <- tribble(
  ~outcome,                     ~ancestry, ~preferred_id,        ~notes,
  "all_cause_mortality",        "EUR",     "ebi-a-GCST006701",   "Pilling 2017 parental longevity — father's attained age (n=415,311 EUR). Standard MR mortality proxy; high power. Note: ebi-a-GCST006414 is Nielsen 2018 Atrial fibrillation, not mortality — previously mis-labeled and excluded.",
  "all_cause_mortality",        "EAS",     "ukb-e-4501_EAS",     "UKB EAS sub-cohort: non-accidental death in close genetic family (n=1,122). Under-powered. NO pure BBJ all-cause mortality GWAS available in OpenGWAS as of 2026-04.",
  "all_cause_mortality",        "AFR",     "ukb-e-1807_AFR",     "UKB African sub-cohort: Father's age at death (n=3,732). Alt: ukb-e-3526_AFR Mother's age at death (n=2,761). Under-powered.",
  "all_cause_mortality",        "SAS",     NA_character_,        "no public SAS mortality/parental-lifespan GWAS — logged gap",
  "all_cause_mortality",        "AMR",     NA_character_,        "no public AMR mortality GWAS — logged gap (All of Us pending registration)",
  "cardiovascular_mortality",   "EUR",     "ebi-a-GCST005194",   "van der Harst 2018 CAD meta (UKB+CARDIoGRAMplusC4D, n=296,525 EUR); CAD as proxy for CVD mortality.",
  "cardiovascular_mortality",   "EAS",     "bbj-a-159",          "BBJ coronary artery disease (Ishigaki 2020 n=212,453 EAS); CAD as proxy for CVD mortality."
)

# ------------------------------------------------------------------------------
# 4. MR configuration
# ------------------------------------------------------------------------------
MR_CONFIG <- list(
  p_threshold   = 5e-8,
  clump_r2      = 0.001,
  clump_kb      = 10000,
  clump_pop     = "EUR",   # default; overridden per-ancestry in 01_instruments.R
  steiger_thresh = 0.05,
  radial_alpha  = 0.05 / nrow(EXPOSURE_OUTCOME_PAIRS),  # Bonferroni
  presso_nboot  = 1000,
  meta_method   = "REML"
)

# ------------------------------------------------------------------------------
# 5. Logging helper
# ------------------------------------------------------------------------------
open_log <- function(script_name) {
  # Opens an append-mode log at logs/<script>.log and tees subsequent cat()
  # output there as well as stdout. Returns the log path invisibly.
  # Use a single connection so both output + message redirection share the file.
  lp <- file.path(DIR_LOGS, paste0(script_name, ".log"))
  if (file.exists(lp)) file.remove(lp)
  .LOGCON <<- file(lp, open = "wt")
  sink(.LOGCON, split = TRUE, type = "output")
  sink(.LOGCON,              type = "message")
  invisible(lp)
}
close_log <- function() {
  try(sink(NULL, type = "message"), silent = TRUE)
  try(sink(NULL, type = "output"),  silent = TRUE)
  if (exists(".LOGCON", inherits = TRUE)) {
    try(close(.LOGCON), silent = TRUE)
    rm(".LOGCON", envir = globalenv())
  }
}
msg <- function(...) cat(sprintf("[%s] ", format(Sys.time(), "%H:%M:%S")), ..., "\n", sep = "")

# Pacing helper for OpenGWAS API (avoid 429)
api_wait <- function(seconds = 2.0) Sys.sleep(seconds)

# ------------------------------------------------------------------------------
# 6. Session header (printed once when script is sourced interactively)
# ------------------------------------------------------------------------------
if (!exists(".ENV_PRINTED", inherits = FALSE)) {
  cat("===== Part 1 MR — environment =====\n")
  cat("R:           ", R.version.string, "\n")
  cat("TwoSampleMR: ", as.character(packageVersion("TwoSampleMR")), "\n")
  cat("ieugwasr:    ", as.character(packageVersion("ieugwasr")), "\n")
  cat("MRPRESSO:    ", as.character(packageVersion("MRPRESSO")), "\n")
  cat("coloc:       ", as.character(packageVersion("coloc")), "\n")
  cat("metafor:     ", as.character(packageVersion("metafor")), "\n")
  cat("SEED:        ", SEED, "\n")
  cat("JWT (first 20): ", substr(Sys.getenv("OPENGWAS_JWT"), 1, 20), "...\n")
  cat("pairs: ",  paste(EXPOSURE_OUTCOME_PAIRS$pair_id, collapse = ", "), "\n")
  cat("====================================\n")
  .ENV_PRINTED <- TRUE
}
