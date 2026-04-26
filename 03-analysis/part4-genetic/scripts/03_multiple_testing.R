#!/usr/bin/env Rscript
# ============================================================================
# 03_multiple_testing.R
# ============================================================================
# Purpose : Collect per-run LRT statistics produced by 02_run_branch_site.sh
#           from data/codeml_runs/*/lrt_stats.tsv, apply Bonferroni and BH-FDR
#           multiple-testing corrections, flag positive-selection detections
#           (Bonferroni at alpha = 0.05 / (n_gene * n_lineage)), and parse the
#           Bayesian Empirical Bayes (BEB) posterior probabilities from the
#           alt-model rst file to identify site-level positive-selection
#           signatures (>0.95 posterior).
#
# Inputs  : data/codeml_runs/<run_id>/lrt_stats.tsv        (one per run)
#           data/codeml_runs/<run_id>/rst                  (BEB posteriors,
#                                                           produced by codeml
#                                                           ALT model with
#                                                           RateAncestor=1)
# Outputs : outputs/branch_site_results.csv                (one row per run)
#           outputs/branch_site_beb_sites.csv              (one row per BEB
#                                                           codon > 0.95)
#           outputs/branch_site_summary.md                 (text summary)
#           logs/03_multiple_testing_<timestamp>.log
#
# Stats policy:
#   * Raw p from 02_run_branch_site.sh is already HALF-CHI-SQUARE (df=1),
#     per Anisimova & Yang 2007 (one-sided test for positive selection).
#   * Bonferroni alpha = 0.05 / n_tests where n_tests = number of (gene, lineage)
#     pairs in the matrix (NOT per-family correction; genes are the unit).
#   * BH-FDR computed in parallel; we report BOTH corrections. Headline uses
#     Bonferroni because prior evidence on reward-receptor positive selection
#     is strong for hummingbird TAS1R1 only, and we want to report a
#     conservative list.
#   * Effect-size reporting: lnL difference + 2*dlnL + omega_foreground from
#     alt rst file.
#
# Multiple-hypothesis framework:
#   - 15 genes x 4+ lineages = at least 60 tests; the paper pre-registered
#     Bonferroni alpha = 0.05 / (15 * 4) = 0.00083 (~1e-3). If the realised
#     matrix expands (e.g. 24 rows in the default matrix), the Bonferroni
#     threshold tightens proportionally. Positive-selection detection is
#     reported under BOTH the pre-registered 0.00083 cutoff AND the realised-
#     n_tests cutoff to preserve the ex-ante commitment.
#
# Dependencies: base R, optparse (optional), data.table, stringr. Tested on R 4.5.
# ============================================================================

suppressPackageStartupMessages({
  library(data.table)
  library(stringr)
})

# Safe-default operator (R has no builtin %||%; define early so it is usable below)
`%||%` <- function(a, b) if (is.null(a) || length(a) == 0 || all(is.na(a))) b else a

args <- commandArgs(trailingOnly = TRUE)
DRY_RUN <- "--dry-run" %in% args

# --- Path resolution ---------------------------------------------------------
script_dir <- normalizePath(dirname(sub("--file=", "",
                            grep("--file=", commandArgs(), value = TRUE)[1] %||% ".")))
if (is.na(script_dir) || !nzchar(script_dir)) {
  script_dir <- getwd()
}
# Robust fallback: assume CWD is 03-analysis/part4-genetic OR scripts/
root_guess <- if (basename(script_dir) == "scripts") dirname(script_dir) else script_dir
if (!dir.exists(file.path(root_guess, "data", "codeml_runs")) &&
    dir.exists(file.path(getwd(), "data", "codeml_runs"))) {
  root_guess <- getwd()
}
ROOT <- normalizePath(root_guess, mustWork = FALSE)
RUNS_DIR <- file.path(ROOT, "data", "codeml_runs")
OUT_DIR  <- file.path(ROOT, "outputs")
LOG_DIR  <- file.path(ROOT, "logs")
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)
dir.create(LOG_DIR, showWarnings = FALSE, recursive = TRUE)

stamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
log_path <- file.path(LOG_DIR, sprintf("03_multiple_testing_%s.log", stamp))
sink(log_path, split = TRUE)
on.exit(sink(NULL), add = TRUE)

cat(sprintf("[%s] 03_multiple_testing.R starting; ROOT=%s\n", Sys.time(), ROOT))
cat(sprintf("DRY_RUN=%s\n", DRY_RUN))

# --- 1. Gather per-run stats -------------------------------------------------
run_dirs <- list.dirs(RUNS_DIR, recursive = FALSE)
if (length(run_dirs) == 0 && !DRY_RUN) {
  stop("No run directories found under ", RUNS_DIR,
       ". Run 01_prepare_codeml_inputs.py + 02_run_branch_site.sh first.")
}

collect_row <- function(rd) {
  stats_file <- file.path(rd, "lrt_stats.tsv")
  if (!file.exists(stats_file)) {
    return(data.table(run_id = basename(rd),
                      lnL_null = NA_real_, lnL_alt_best = NA_real_,
                      LRT_2dlnL = NA_real_, p_raw_half_chi2_df1 = NA_real_,
                      note = "missing lrt_stats.tsv (run pending?)"))
  }
  tb <- tryCatch(fread(stats_file, sep = "\t"), error = function(e) NULL)
  if (is.null(tb) || nrow(tb) == 0) {
    return(data.table(run_id = basename(rd), note = "empty stats"))
  }
  tb[, note := NA_character_]
  return(tb)
}

if (DRY_RUN || length(run_dirs) == 0) {
  cat("DRY-RUN: constructing empty placeholder table.\n")
  res <- data.table(
    run_id = c("TAS1R1__hummingbird", "TAS1R1__mouse_control", "TAS1R2__primate_sugar"),
    lnL_null = NA_real_, lnL_alt_best = NA_real_,
    LRT_2dlnL = NA_real_, p_raw_half_chi2_df1 = NA_real_,
    note = "dry_run_placeholder"
  )
} else {
  res <- rbindlist(lapply(run_dirs, collect_row), fill = TRUE)
}

# --- 2. Split run_id into gene + lineage -------------------------------------
res[, c("gene", "lineage") := tstrsplit(run_id, "__", fixed = TRUE, keep = 1:2)]

# --- 3. Multiple-testing corrections -----------------------------------------
# Realised n_tests (from actually-run rows with a p value)
n_tests_realised <- sum(!is.na(res$p_raw_half_chi2_df1))

# Pre-registered: 15 genes x 4 lineages = 60 tests
# alpha_bonferroni = 0.05 / 60 = 0.000833 (~1e-3)
N_TESTS_PREREG <- 15 * 4
ALPHA_PREREG <- 0.05 / N_TESTS_PREREG   # ~8.33e-4
ALPHA_REALISED <- if (n_tests_realised > 0) 0.05 / n_tests_realised else NA_real_

cat(sprintf("Pre-registered alpha (15g x 4L): %.3e   Realised alpha (n=%d): %.3e\n",
            ALPHA_PREREG, n_tests_realised,
            ALPHA_REALISED %||% NA))

res[, bonferroni_p_prereg  := pmin(p_raw_half_chi2_df1 * N_TESTS_PREREG, 1)]
res[, bonferroni_p_realised := if (n_tests_realised > 0) pmin(p_raw_half_chi2_df1 * n_tests_realised, 1) else NA_real_]
res[, bh_q := p.adjust(p_raw_half_chi2_df1, method = "BH")]

res[, positive_selection_prereg   := !is.na(p_raw_half_chi2_df1) & p_raw_half_chi2_df1 < ALPHA_PREREG]
res[, positive_selection_realised := !is.na(p_raw_half_chi2_df1) & !is.na(ALPHA_REALISED) &
                                     p_raw_half_chi2_df1 < ALPHA_REALISED]

# --- 4. Parse BEB sites from alt rst file ------------------------------------
parse_beb <- function(rst_path, run_id, threshold = 0.95) {
  if (!file.exists(rst_path)) return(data.table())
  lines <- readLines(rst_path, warn = FALSE)
  # Section header commonly reads:
  #   "Bayes Empirical Bayes (BEB) analysis (Yang, Wong & Nielsen 2005 Mol. Biol. Evol. 22:1107-1118)"
  start <- grep("Bayes Empirical Bayes|BEB analysis", lines)
  if (length(start) == 0) return(data.table())
  block <- lines[start[1]:length(lines)]
  # The BEB table rows typically look like:
  #   "  123 S    0.987*   2.456 +- 1.123"
  # We keep any line with a two-digit posterior > threshold.
  row_re <- "^\\s*([0-9]+)\\s+([A-Z])\\s+([0-9\\.]+)(\\*{0,2})"
  hits <- regmatches(block, regexec(row_re, block))
  out <- lapply(hits, function(m) {
    if (length(m) == 0) return(NULL)
    data.table(codon_site = as.integer(m[2]),
               codon_AA   = m[3],
               beb_posterior = as.numeric(m[4]),
               sig_mark = m[5])
  })
  out <- rbindlist(out, fill = TRUE)
  if (nrow(out) == 0) return(data.table())
  out <- out[beb_posterior >= threshold]
  if (nrow(out) > 0) out[, run_id := run_id]
  return(out)
}

if (DRY_RUN || length(run_dirs) == 0) {
  beb_all <- data.table()
} else {
  beb_all <- rbindlist(lapply(run_dirs, function(rd) {
    parse_beb(file.path(rd, "rst"), basename(rd))
  }), fill = TRUE)
}

# Attach BEB site count per run
beb_counts <- if (nrow(beb_all) > 0) beb_all[, .(n_beb_sites_gt95 = .N), by = run_id] else
              data.table(run_id = character(0), n_beb_sites_gt95 = integer(0))
res <- merge(res, beb_counts, by = "run_id", all.x = TRUE)
res[is.na(n_beb_sites_gt95), n_beb_sites_gt95 := 0L]

# --- 5. Write outputs --------------------------------------------------------
out_csv <- file.path(OUT_DIR, "branch_site_results.csv")
fwrite(res, out_csv)
cat(sprintf("Wrote %s (%d rows)\n", out_csv, nrow(res)))

beb_csv <- file.path(OUT_DIR, "branch_site_beb_sites.csv")
fwrite(beb_all, beb_csv)
cat(sprintf("Wrote %s (%d BEB sites)\n", beb_csv, nrow(beb_all)))

# Summary markdown
sink(NULL)
summary_md <- file.path(OUT_DIR, "branch_site_summary.md")
con <- file(summary_md, "w")
writeLines(c(
  sprintf("# Branch-site Model A - Results summary"),
  sprintf(""),
  sprintf("Generated: %s", format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z")),
  sprintf(""),
  sprintf("## Multiple-testing framework"),
  sprintf(""),
  sprintf("- Pre-registered n_tests = 15 genes x 4 lineages = %d; alpha_bonferroni = %.3e",
          N_TESTS_PREREG, ALPHA_PREREG),
  sprintf("- Realised n_tests = %d; realised Bonferroni alpha = %s", n_tests_realised,
          if (is.na(ALPHA_REALISED)) "NA" else sprintf("%.3e", ALPHA_REALISED)),
  sprintf(""),
  sprintf("## Counts"),
  sprintf(""),
  sprintf("- Total runs in table: %d", nrow(res)),
  sprintf("- Runs with completed LRT: %d", sum(!is.na(res$p_raw_half_chi2_df1))),
  sprintf("- Positive selection @ pre-registered alpha: %d",
          sum(res$positive_selection_prereg, na.rm = TRUE)),
  sprintf("- Positive selection @ realised alpha: %d",
          sum(res$positive_selection_realised, na.rm = TRUE)),
  sprintf("- BH q < 0.05: %d", sum(res$bh_q < 0.05, na.rm = TRUE)),
  sprintf(""),
  sprintf("## Positive-control validation (hummingbird TAS1R1)"),
  sprintf(""),
  {
    ctl <- res[grepl("hummingbird", run_id)]
    if (nrow(ctl) == 0) "- Positive control row not present in table."
    else sprintf("- %s : LRT=%s  p_raw=%s  bonferroni_p_prereg=%s  BEB_sites=%d",
                 ctl$run_id[1],
                 format(ctl$LRT_2dlnL[1], digits = 4),
                 format(ctl$p_raw_half_chi2_df1[1], digits = 3),
                 format(ctl$bonferroni_p_prereg[1], digits = 3),
                 ctl$n_beb_sites_gt95[1])
  },
  sprintf(""),
  sprintf("See `branch_site_results.csv` for per-run stats; `branch_site_beb_sites.csv` for BEB codons.")
), con)
close(con)
cat(sprintf("Wrote %s\n", summary_md))

cat("03_multiple_testing.R finished.\n")
