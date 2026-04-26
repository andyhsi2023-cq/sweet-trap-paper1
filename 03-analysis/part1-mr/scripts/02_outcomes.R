#!/usr/bin/env Rscript
# ==============================================================================
# 02_outcomes.R — extract outcome summary stats per ancestry, harmonise
# ==============================================================================
# For every exposure-outcome pair declared in 00_environment.R, iterate over the
# ancestries in that pair's `ancestries` column. For each ancestry, pick the
# preferred outcome GWAS ID from OUTCOME_ID_MAP, call
# TwoSampleMR::extract_outcome_data() against the exposure SNPs, then
# harmonise_data() and persist the result.
#
# Output:
#   outputs/outcome_<pair_id>_<ancestry>.rds     — extract_outcome_data result
#   outputs/harmonised_<pair_id>_<ancestry>.rds  — harmonised table (mr_keep)
#   outputs/outcomes_summary.csv                 — per-combo SNP counts
#   outputs/outcomes_failed.csv                  — any combos that failed
# ==============================================================================

source("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part1-mr/scripts/00_environment.R")
open_log("02_outcomes")
on.exit(close_log())

msg("=== 02_outcomes.R starting ===")

get_outcome_id <- function(outcome, ancestry) {
  r <- OUTCOME_ID_MAP %>%
    filter(outcome == !!outcome & ancestry == !!ancestry)
  if (nrow(r) == 0) return(list(id = NA_character_, note = "no mapping"))
  list(id = r$preferred_id[1], note = r$notes[1])
}

extract_outcome_retry <- function(snps, oid, tries = 3, pause = 5) {
  res <- NULL
  for (k in seq_len(tries)) {
    msg(sprintf("      attempt %d/%d: extract_outcome_data (n_snp=%d, id=%s)",
                k, tries, length(snps), oid))
    res <- tryCatch(
      extract_outcome_data(snps = snps, outcomes = oid, proxies = TRUE,
                           maf_threshold = 0.01),
      error = function(e) { msg("        ERR: ", conditionMessage(e)); NULL }
    )
    if (!is.null(res) && nrow(res) > 0) break
    api_wait(pause)
  }
  res
}

summ   <- list()
failed <- list()

for (i in seq_len(nrow(EXPOSURE_OUTCOME_PAIRS))) {
  pair <- EXPOSURE_OUTCOME_PAIRS[i, ]
  pid  <- pair$pair_id
  msg(sprintf("--- pair %s | outcome=%s | ancestries=%s ---",
              pid, pair$outcome, pair$ancestries))

  iv_path <- file.path(DIR_OUT, sprintf("instruments_%s.rds", pid))
  if (!file.exists(iv_path)) {
    msg("  missing IV rds: ", iv_path); next
  }
  iv <- readRDS(iv_path)
  msg(sprintf("  loaded %d exposure SNPs", nrow(iv)))

  ancestries <- strsplit(pair$ancestries, ",")[[1]]
  for (anc in ancestries) {
    msg(sprintf("    >> ancestry=%s", anc))
    m <- get_outcome_id(pair$outcome, anc)
    if (is.na(m$id)) {
      msg("       no preferred outcome ID — logged gap: ", m$note)
      failed[[paste(pid, anc, sep = "_")]] <- tibble(
        pair_id = pid, ancestry = anc, outcome = pair$outcome,
        outcome_id = NA_character_, reason = m$note
      )
      next
    }
    msg("       outcome_id=", m$id, " | ", m$note)

    # Extract
    oc <- extract_outcome_retry(iv$SNP, m$id)
    if (is.null(oc) || nrow(oc) == 0) {
      msg("       extract_outcome_data returned 0 — logged gap")
      failed[[paste(pid, anc, sep = "_")]] <- tibble(
        pair_id = pid, ancestry = anc, outcome = pair$outcome,
        outcome_id = m$id, reason = "extract_outcome_data returned 0 / API failure"
      )
      api_wait(3)
      next
    }
    msg(sprintf("       extracted %d outcome rows", nrow(oc)))

    # Annotate
    oc$outcome <- paste0(pair$outcome, "_", anc)
    oc$ancestry <- anc
    saveRDS(oc, file.path(DIR_OUT, sprintf("outcome_%s_%s.rds", pid, anc)))

    # Harmonise
    har <- tryCatch(
      harmonise_data(exposure_dat = iv, outcome_dat = oc, action = 2),
      error = function(e) { msg("       harmonise ERR: ", conditionMessage(e)); NULL }
    )
    if (is.null(har) || nrow(har) == 0) {
      msg("       harmonise_data empty")
      failed[[paste(pid, anc, sep = "_")]] <- tibble(
        pair_id = pid, ancestry = anc, outcome = pair$outcome,
        outcome_id = m$id, reason = "harmonise_data returned 0"
      )
      api_wait(3); next
    }
    har$pair_id <- pid; har$ancestry <- anc
    kept <- sum(har$mr_keep, na.rm = TRUE)
    msg(sprintf("       harmonised: n_total=%d | mr_keep=%d", nrow(har), kept))
    saveRDS(har, file.path(DIR_OUT, sprintf("harmonised_%s_%s.rds", pid, anc)))

    summ[[paste(pid, anc, sep = "_")]] <- tibble(
      pair_id = pid, ancestry = anc,
      outcome = pair$outcome, outcome_id = m$id,
      n_exposure_snp = nrow(iv), n_outcome_match = nrow(oc),
      n_harmonised = nrow(har), n_mr_keep = kept
    )
    api_wait(3)
  }
}

if (length(summ)) {
  summ_tbl <- bind_rows(summ)
  fwrite(summ_tbl, file.path(DIR_OUT, "outcomes_summary.csv"))
  msg("wrote outcomes_summary.csv n=", nrow(summ_tbl))
  print(summ_tbl)
}
if (length(failed)) {
  ft <- bind_rows(failed)
  fwrite(ft, file.path(DIR_OUT, "outcomes_failed.csv"))
  msg("wrote outcomes_failed.csv n=", nrow(ft))
  print(ft)
}

msg("=== 02_outcomes.R done ===")
