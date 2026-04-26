#!/usr/bin/env Rscript
# =============================================================================
# 06_phylosig_H3.R
# Sweet Trap Part 2 — H3 phylogenetic signal test for Δ_ST proxy
#
# Purpose
#   Test whether Δ_ST proxy exhibits phylogenetic signal across 70+ species
#   spanning 7 phyla (Chordata, Arthropoda, Mollusca, Cnidaria, Nematoda,
#   Annelida, etc.). H3 predicts Sweet Trap vulnerability is NOT strongly
#   phylogenetically clustered — it should be explained by shared reward-system
#   architecture (ancestral signals) rather than relatedness.
#
# Inputs
#   - outputs/animal_cases_final.csv         (115 cases, 32 cols)
#   - outputs/species_tree_timetree.nwk      (TimeTree 5 API, 7427-tip expanded)
#   - outputs/species_list_for_timetree.txt  (species list submitted to API)
#
# Outputs
#   - outputs/species_tree_pruned.nwk        (pruned to matched species only)
#   - outputs/phylosig_main.csv
#   - outputs/phylosig_subgroups.csv
#   - outputs/phylosig_species_map.csv       (provenance: case → tip mapping)
#
# Methods
#   - Blomberg's K  (phytools::phylosig, method="K", nsim=9999)
#   - Pagel's lambda (phytools::phylosig, method="lambda", test=TRUE)
#   - Bootstrap 95% CI for K and lambda (1000 reps of trait resampling with
#     fixed tree topology; this is parameter uncertainty, not species-set
#     uncertainty — for the latter we use the subgroup analysis)
#
# Decision rule (pre-stated in task brief)
#   K > 1 OR lambda > 0.7, p < 0.05  → SUPPORTED (trait clusters phylo)
#   K near 0 OR lambda near 0        → NOT SUPPORTED (informative null)
#
# Author: Claude (Sweet Trap Paper 1 pipeline)
# Date: 2026-04-25
# =============================================================================

suppressPackageStartupMessages({
  library(ape)
  library(phytools)
})

set.seed(42)  # reproducibility

# ---- paths -----------------------------------------------------------------
ROOT    <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part2-prisma"
OUT     <- file.path(ROOT, "outputs")
CASES   <- file.path(OUT, "animal_cases_final.csv")
TREE    <- file.path(OUT, "species_tree_timetree.nwk")

# ---- 1. Load -----------------------------------------------------------------
cat("=== STEP 1: Load data =====================================\n")
d  <- read.csv(CASES, stringsAsFactors = FALSE)
tr <- read.tree(TREE)
cat(sprintf("cases: n=%d   tree tips: n=%d\n", nrow(d), length(tr$tip.label)))

# ---- 2. Build case -> representative species mapping -----------------------
# Rule set:
#   (a) If species_binomial contains a single clean Latin binomial that matches
#       a tip, use it.
#   (b) If multi-species ("A spp.", "A / B", "multiple") or higher taxon
#       (Lepidoptera, Odonata, Chiroptera, Ephemeroptera, Perciformes), pick
#       the first genus mentioned whose tip exists; if none, drop the case
#       from the phylosig analysis (logged).
#   (c) For cases labeled "Multiple" phylum, drop (cannot place).

# Helper: extract genus from a string
first_latin_word <- function(s) {
  toks <- unlist(strsplit(s, "[^A-Za-z]+"))
  toks <- toks[nchar(toks) > 2]
  toks <- toks[grepl("^[A-Z][a-z]+$", toks)]
  if (length(toks) == 0) NA_character_ else toks[1]
}

# Map each case to a tip label (underscore form)
map_case_to_tip <- function(sp_str, tips) {
  if (is.na(sp_str) || sp_str == "") return(NA_character_)
  raw <- trimws(sp_str)
  cand <- character(0)

  # (a) try exact first binomial: "Genus species" (ignoring "/" and "spp.")
  first_chunk <- trimws(strsplit(raw, "[/,]")[[1]][1])
  bi <- sub("^([A-Z][a-z]+)\\s+([a-z]+).*$", "\\1_\\2", first_chunk)
  if (bi %in% tips) return(bi)

  # (b) genus-only match (any tip starting with "Genus_")
  g <- first_latin_word(first_chunk)
  if (!is.na(g)) {
    hits <- grep(paste0("^", g, "_"), tips, value = TRUE)
    if (length(hits) >= 1) return(hits[1])
    # try exact genus (some unresolved cases keep the plain genus name)
    if (g %in% tips) return(g)
  }

  # (c) higher-taxon fall-back keywords
  # If sp_str mentions a higher taxon, try to find a representative
  # We intentionally do NOT use broad phylum-level matches here; unresolved stays NA.
  NA_character_
}

tips <- tr$tip.label
d$tip_label <- vapply(d$species_binomial, map_case_to_tip, character(1), tips = tips)

cat(sprintf("mapped: %d / %d cases have tip match\n",
            sum(!is.na(d$tip_label)), nrow(d)))

# Drop Multiple-phylum and NA delta cases
d_use <- d[!is.na(d$tip_label) & !is.na(d$delta_st_proxy) & d$phylum != "Multiple", ]
cat(sprintf("after drop (NA tip | NA delta | Multiple phylum): n_cases=%d\n", nrow(d_use)))
dropped <- d[is.na(d$tip_label) | is.na(d$delta_st_proxy) | d$phylum == "Multiple",
             c("case_id","species_binomial","phylum","delta_st_proxy")]
cat(sprintf("dropped (logged): n=%d\n", nrow(dropped)))

# ---- 3. Average Δ_ST per tip (species-level trait vector) ------------------
cat("\n=== STEP 3: Species-level trait vector ====================\n")
agg <- aggregate(delta_st_proxy ~ tip_label + phylum + class,
                 data = d_use, FUN = function(x) mean(x, na.rm = TRUE))
# If a tip appears under >1 phylum/class (shouldn't), keep first row
agg <- agg[!duplicated(agg$tip_label), ]
cat(sprintf("unique species/tips with trait: n=%d\n", nrow(agg)))

# Save mapping provenance
write.csv(
  merge(d_use[, c("case_id","species_binomial","phylum","class","delta_st_proxy","tip_label")],
        agg[, c("tip_label","delta_st_proxy"), drop = FALSE],
        by = "tip_label", suffixes = c("_case","_species_mean"),
        all.x = TRUE),
  file.path(OUT, "phylosig_species_map.csv"), row.names = FALSE)

# ---- 4. Prune tree to matched tips -----------------------------------------
cat("\n=== STEP 4: Prune tree =====================================\n")
keep <- agg$tip_label
drop_tips <- setdiff(tr$tip.label, keep)
tr_p <- drop.tip(tr, drop_tips)
cat(sprintf("pruned tree: n_tips=%d   ultrametric=%s   binary=%s\n",
            length(tr_p$tip.label), is.ultrametric(tr_p), is.binary(tr_p)))
# Force ultrametricity to numeric tolerance if needed
if (!is.ultrametric(tr_p)) {
  tr_p <- force.ultrametric(tr_p, method = "extend")
  cat("forced ultrametric via extend\n")
}
# Resolve polytomies for phylosig (needs binary)
if (!is.binary(tr_p)) tr_p <- multi2di(tr_p, random = FALSE)

write.tree(tr_p, file.path(OUT, "species_tree_pruned.nwk"))

# Align trait vector to tree tip order
x <- setNames(agg$delta_st_proxy[match(tr_p$tip.label, agg$tip_label)], tr_p$tip.label)
stopifnot(all(!is.na(x)))

# ---- 5. Main phylosig tests (K and lambda) ---------------------------------
cat("\n=== STEP 5: Main phylosig ==================================\n")
ks  <- phylosig(tr_p, x, method = "K",      test = TRUE, nsim = 9999)
lam <- phylosig(tr_p, x, method = "lambda", test = TRUE)

cat(sprintf("Blomberg K = %.4f   p = %.4g   (nsim=9999)\n", ks$K,   ks$P))
cat(sprintf("Pagel lambda = %.4f   logL = %.3f  logL0 = %.3f  p = %.4g\n",
            lam$lambda, lam$logL, lam$logL0, lam$P))

# Bootstrap CI for K and lambda (trait bootstrap with fixed tree) -----------
B  <- 1000
Kb <- numeric(B); Lb <- numeric(B)
for (b in seq_len(B)) {
  idx <- sample(seq_along(x), replace = TRUE)
  xb  <- setNames(x[idx], tr_p$tip.label)   # resample trait values onto existing tips
  # phytools::phylosig returns an atomic numeric when test=FALSE (method="K")
  # and a list when method="lambda". Handle both.
  Kb[b] <- tryCatch(as.numeric(phylosig(tr_p, xb, method = "K",      test = FALSE)),
                    error = function(e) NA_real_)
  Lb[b] <- tryCatch({
              r <- phylosig(tr_p, xb, method = "lambda", test = FALSE)
              if (is.list(r)) r$lambda else as.numeric(r)
           }, error = function(e) NA_real_)
}
k_ci <- quantile(Kb, c(.025, .975), na.rm = TRUE)
l_ci <- quantile(Lb, c(.025, .975), na.rm = TRUE)
cat(sprintf("K 95%% CI = [%.4f, %.4f]\n", k_ci[1], k_ci[2]))
cat(sprintf("lambda 95%% CI = [%.4f, %.4f]\n", l_ci[1], l_ci[2]))

# Robustness: Moran's I via phylogenetic distance matrix --------------------
D <- cophenetic(tr_p)
W <- 1 / D; diag(W) <- 0
moran <- ape::Moran.I(x, weight = W)
cat(sprintf("Moran's I = %.4f  expected = %.4f  p = %.4g\n",
            moran$observed, moran$expected, moran$p.value))

# Write main results --------------------------------------------------------
main <- data.frame(
  subset      = "All phyla",
  n_species   = length(x),
  K           = round(ks$K, 4),
  K_p         = ks$P,
  K_CI_low    = round(k_ci[1], 4),
  K_CI_high   = round(k_ci[2], 4),
  lambda      = round(lam$lambda, 4),
  lambda_p    = lam$P,
  lambda_CI_low  = round(l_ci[1], 4),
  lambda_CI_high = round(l_ci[2], 4),
  MoranI      = round(moran$observed, 4),
  MoranI_p    = moran$p.value,
  row.names   = NULL
)
write.csv(main, file.path(OUT, "phylosig_main.csv"), row.names = FALSE)

# ---- 6. Subgroup analyses --------------------------------------------------
cat("\n=== STEP 6: Subgroup phylosig ==============================\n")

run_sub <- function(keep_tips, label) {
  sub_tree <- drop.tip(tr_p, setdiff(tr_p$tip.label, keep_tips))
  if (length(sub_tree$tip.label) < 4) {
    cat("  SKIP (n<4):", label, "\n"); return(NULL)
  }
  if (!is.ultrametric(sub_tree)) sub_tree <- force.ultrametric(sub_tree, method="extend")
  if (!is.binary(sub_tree)) sub_tree <- multi2di(sub_tree, random = FALSE)
  xs <- x[sub_tree$tip.label]
  ks2  <- phylosig(sub_tree, xs, method = "K",      test = TRUE, nsim = 9999)
  lam2 <- phylosig(sub_tree, xs, method = "lambda", test = TRUE)
  cat(sprintf("  %s: n=%d  K=%.3f (p=%.3g)  lambda=%.3f (p=%.3g)\n",
              label, length(xs), ks2$K, ks2$P, lam2$lambda, lam2$P))
  data.frame(subset     = label,
             n_species  = length(xs),
             K          = round(ks2$K, 4),
             K_p        = ks2$P,
             lambda     = round(lam2$lambda, 4),
             lambda_p   = lam2$P)
}

chord_tips <- agg$tip_label[agg$phylum == "Chordata"]
ca_tips    <- agg$tip_label[agg$phylum %in% c("Chordata","Arthropoda")]
arth_tips  <- agg$tip_label[agg$phylum == "Arthropoda"]

sub_tbl <- do.call(rbind, list(
  run_sub(chord_tips, "Chordata only"),
  run_sub(ca_tips,    "Chordata + Arthropoda"),
  run_sub(arth_tips,  "Arthropoda only")
))
write.csv(sub_tbl, file.path(OUT, "phylosig_subgroups.csv"), row.names = FALSE)

# ---- 7. Verdict ------------------------------------------------------------
cat("\n=== STEP 7: Verdict ========================================\n")
supported <- (ks$K > 1 | lam$lambda > 0.7) && (ks$P < 0.05 | lam$P < 0.05)
cat("H3 verdict:", if (supported) "SUPPORTED" else "NOT SUPPORTED", "\n")
cat(sprintf("  K=%.3f (p=%.4g)  lambda=%.3f (p=%.4g)\n",
            ks$K, ks$P, lam$lambda, lam$P))

cat("\nDone.\n")
