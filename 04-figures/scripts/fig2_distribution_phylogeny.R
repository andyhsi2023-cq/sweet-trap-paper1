## ============================================================
## Figure 2 — Cross-species distribution & phylogenetic structure
## Sweet Trap v4 Paper 1
## Target: 180 x 170 mm, 600 dpi, Okabe-Ito palette
## Outputs: PDF (cairo_pdf), PNG, SVG
## ============================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(ggtree)
  library(patchwork)
  library(cowplot)
  library(dplyr)
  library(tidyr)
  library(ape)
  library(phytools)
  library(viridis)
  library(scales)
  library(grid)
})

# ── paths ────────────────────────────────────────────────────
BASE  <- "/Users/andy/Desktop/Research/sweet-trap-multidomain"
OUTS  <- file.path(BASE, "04-figures")
NWK   <- file.path(BASE, "03-analysis/part2-prisma/outputs/species_tree_pruned.nwk")
CSV   <- file.path(BASE, "03-analysis/part2-prisma/outputs/animal_cases_final.csv")
PSIG  <- file.path(BASE, "03-analysis/part2-prisma/outputs/phylosig_main.csv")
PSUB  <- file.path(BASE, "03-analysis/part2-prisma/outputs/phylosig_subgroups.csv")

# ── global style ─────────────────────────────────────────────
OKABE <- c(
  Chordata   = "#0077BB",
  Arthropoda = "#EE7733",
  Nematoda   = "#009988",
  Cnidaria   = "#CC3311",
  Mollusca   = "#AA3377",
  Annelida   = "#BBBBBB"
)

theme_fig2 <- function(...) {
  theme_classic(base_size = 6, base_family = "Helvetica") +
    theme(
      axis.line        = element_line(linewidth = 0.3),
      axis.ticks       = element_line(linewidth = 0.3),
      axis.text        = element_text(size = 5),
      axis.title       = element_text(size = 6),
      legend.text      = element_text(size = 5),
      legend.title     = element_text(size = 5.5, face = "bold"),
      legend.key.size  = unit(3, "pt"),
      plot.title       = element_text(size = 6.5, face = "bold"),
      ...
    )
}

# ── 1. LOAD & PREPARE DATA ───────────────────────────────────
tree_raw <- read.tree(NWK)
cases    <- read.csv(CSV, stringsAsFactors = FALSE)

# Keep only confirmed cases (not excluded / review-only / F2-fail)
cases_ok <- cases %>%
  filter(is.na(exclusion_reason) |
         exclusion_reason == "NA" |
         exclusion_reason == "") %>%
  filter(!(case_id %in% c("C08","C07","C11","C13")))

# Derive F3 flag (any F3_mechanism string that is non-empty)
cases_ok <- cases_ok %>%
  mutate(
    F3 = as.integer(!is.na(F3_mechanism) &
                    F3_mechanism != "" &
                    F3_mechanism != "none"),
    delta_st_numeric = suppressWarnings(as.numeric(delta_st_proxy))
  )

# Aggregate per species
species_dat <- cases_ok %>%
  group_by(species_binomial, phylum) %>%
  summarise(
    F1_mean       = mean(F1,              na.rm = TRUE),
    F2_mean       = mean(F2,              na.rm = TRUE),
    F3_mean       = mean(F3,              na.rm = TRUE),
    F4_mean       = mean(F4_score,        na.rm = TRUE),
    delta_st_mean = mean(delta_st_numeric, na.rm = TRUE),
    .groups = "drop"
  )

# Normalise delta_st to 0-1
dst_range <- range(species_dat$delta_st_mean, na.rm = TRUE)
species_dat <- species_dat %>%
  mutate(delta_st_scaled = (delta_st_mean - dst_range[1]) /
                           (dst_range[2] - dst_range[1]))

# ── 2. MATCH SPECIES TO TREE TIPS ────────────────────────────
tip_names <- tree_raw$tip.label

# underscore form of tip names
tip_tbl <- data.frame(
  tip_label = tip_names,
  key       = gsub(" ", "_", tip_names),
  stringsAsFactors = FALSE
)

# For species with "/" in binomial, take part before "/"
species_dat <- species_dat %>%
  mutate(
    key = gsub(" ", "_",
               trimws(sub("/.*", "", species_binomial)))
  )

# direct join
matched <- merge(species_dat, tip_tbl, by = "key", all = FALSE)

# For remaining multi-species, genus-only fallback
already_matched_keys <- matched$key
multi_miss <- species_dat %>%
  filter(grepl("/", species_binomial), !key %in% already_matched_keys)

if (nrow(multi_miss) > 0) {
  genus_hits <- lapply(seq_len(nrow(multi_miss)), function(i) {
    genus   <- sub("_.*", "", multi_miss$key[i])
    pattern <- paste0("^", genus, "_")
    hits    <- grep(pattern, tip_names, value = TRUE)
    if (length(hits) > 0) {
      cbind(multi_miss[i, ], data.frame(tip_label = hits[1],
                                        stringsAsFactors = FALSE))
    } else NULL
  })
  genus_df <- do.call(rbind, Filter(Negate(is.null), genus_hits))
  if (!is.null(genus_df) && nrow(genus_df) > 0) {
    matched <- rbind(matched, genus_df)
  }
}

# Deduplicate on tip_label
matched <- matched[!duplicated(matched$tip_label), ]

# Prune tree to matched tips
tips_keep   <- matched$tip_label
tree_pruned <- keep.tip(tree_raw, tips_keep)
tip_order   <- tree_pruned$tip.label   # order in which ggtree will draw tips

# Reorder matched to follow tip_order
matched <- matched[match(tip_order, matched$tip_label), ]
n_sp    <- length(tip_order)
cat(sprintf("Species retained in pruned tree: %d\n", n_sp))

# ── 3. PANEL A — TIME-CALIBRATED PHYLOGENY ───────────────────
# Named phylum vector for colouring tips
tip_phylum <- setNames(matched$phylum, matched$tip_label)

# Italic display labels (underscore → space)
display_labels <- setNames(
  gsub("_", " ", tip_order),
  tip_order
)

panel_A <- ggtree(tree_pruned, layout = "rectangular",
                  linewidth = 0.25, color = "grey40") +
  geom_tippoint(aes(color = tip_phylum[label]), size = 0.9) +
  geom_tiplab(aes(label = display_labels[label]),
              fontface = "italic", size = 1.15, offset = 8, hjust = 0) +
  scale_color_manual(
    values = OKABE,
    name   = "Phylum",
    guide  = guide_legend(ncol = 1,
                          override.aes = list(size = 1.5))
  ) +
  theme_tree2() +
  theme(
    axis.line.x       = element_line(linewidth = 0.3),
    axis.ticks.x      = element_line(linewidth = 0.3),
    axis.text.x       = element_text(size = 4.5),
    legend.position   = c(0.02, 0.5),
    legend.justification = c(0, 0.5),
    legend.background = element_rect(fill = alpha("white", 0.85), colour = NA),
    legend.text       = element_text(size = 4.5),
    legend.title      = element_text(size = 5, face = "bold"),
    legend.key.size   = unit(4, "pt"),
    plot.margin       = margin(2, 2, 2, 2, "pt")
  ) +
  labs(x = "Divergence time (Ma)") +
  xlim_tree(max(node.depth.edgelength(tree_pruned)) * 1.42)

# ── 4. PANEL B — Delta_ST HEATMAP ────────────────────────────
# Column labels as plain character (no expression objects)
col_levels <- c("F1_mean","F2_mean","F3_mean","F4_mean","delta_st_scaled")
col_labels  <- c("F1\nDeception","F2\nAsym-Info","F3\nFitness\nCost",
                 "F4\nScale","ΔST\nProxy")

heatmap_long <- matched %>%
  select(tip_label, F1_mean, F2_mean, F3_mean, F4_mean, delta_st_scaled) %>%
  pivot_longer(
    cols      = -tip_label,
    names_to  = "feature",
    values_to = "value"
  ) %>%
  mutate(
    feature   = factor(feature, levels = col_levels, labels = col_labels),
    tip_label = factor(tip_label, levels = rev(tip_order))
  )

panel_B <- ggplot(heatmap_long,
                  aes(x = feature, y = tip_label, fill = value)) +
  geom_tile(color = "white", linewidth = 0.15) +
  scale_fill_viridis(
    option  = "plasma",
    na.value = "grey90",
    name    = "Score\n(0-1)",
    limits  = c(0, 1),
    breaks  = c(0, 0.5, 1)
  ) +
  scale_x_discrete(expand = c(0, 0)) +
  scale_y_discrete(expand = c(0, 0)) +
  theme_fig2() +
  theme(
    axis.text.x       = element_text(size = 3.8, lineheight = 0.85),
    axis.text.y       = element_blank(),
    axis.ticks.y      = element_blank(),
    axis.title        = element_blank(),
    legend.position   = "right",
    legend.key.height = unit(14, "pt"),
    legend.key.width  = unit(4, "pt"),
    panel.border      = element_rect(fill = NA, linewidth = 0.3),
    plot.margin       = margin(2, 4, 2, 0, "pt")
  )

# ── 5. PANEL C — PHYLOGENETIC SIGNAL BAR CHART ───────────────
psig_main <- read.csv(PSIG, stringsAsFactors = FALSE)
psig_sub  <- read.csv(PSUB, stringsAsFactors = FALSE)

# Subgroup CSV has no CI columns — add them as NA
if (!"K_CI_low"  %in% names(psig_sub)) psig_sub$K_CI_low  <- NA_real_
if (!"K_CI_high" %in% names(psig_sub)) psig_sub$K_CI_high <- NA_real_

sig_all <- bind_rows(
  psig_main %>% select(subset, n_species, K, K_p, K_CI_low, K_CI_high,
                        lambda, lambda_p),
  psig_sub  %>% select(subset, n_species, K, K_p, K_CI_low, K_CI_high,
                        lambda, lambda_p)
)

sig_df <- sig_all %>%
  filter(subset %in% c("All phyla", "Chordata only", "Arthropoda only"))

# Build a clean label string
sig_df$label <- c(
  "All phyla (n=56)",
  "Chordata (n=37)",
  "Arthropoda (n=13)"
)[match(sig_df$subset, c("All phyla","Chordata only","Arthropoda only"))]

# factor with correct order (top → bottom in plot)
sig_df$label <- factor(sig_df$label,
  levels = c("Arthropoda (n=13)", "Chordata (n=37)", "All phyla (n=56)"))

sig_df <- sig_df %>%
  mutate(
    lam_lab   = sprintf("λ=%.2f p=%.3f", lambda, lambda_p),
    bar_color = dplyr::case_when(
      subset == "Arthropoda only" ~ unname(OKABE["Arthropoda"]),
      subset == "Chordata only"   ~ unname(OKABE["Chordata"]),
      TRUE                        ~ "grey60"
    ),
    sig_tag   = ifelse(K_p < 0.05, "SIGNAL", "NULL")
  )

panel_C <- ggplot(sig_df, aes(x = K, y = label)) +
  geom_col(aes(fill = bar_color), width = 0.42, alpha = 0.87) +
  scale_fill_identity() +
  # CI whiskers where available
  geom_segment(
    aes(x    = ifelse(is.na(K_CI_low),  K, K_CI_low),
        xend = ifelse(is.na(K_CI_high), K, K_CI_high),
        y = label, yend = label),
    linewidth = 0.8, color = "grey65"
  ) +
  # Brownian motion reference line at K=1
  geom_vline(xintercept = 1, linetype = "dashed", linewidth = 0.4,
             color = "grey55") +
  # K value + p labels (above bar)
  geom_text(aes(x = pmax(K, 0.05) + 0.04,
                label = sprintf("K=%.3f  p=%.3f", K, K_p)),
            hjust = 0, vjust = -0.55, size = 1.65, color = "grey20") +
  # lambda labels (below bar)
  geom_text(aes(x = 0.03, label = lam_lab),
            hjust = 0, vjust = 1.45, size = 1.55, color = "grey40") +
  # SIGNAL / NULL tags (far right, right-aligned)
  geom_text(
    data = sig_df %>% filter(sig_tag == "SIGNAL"),
    aes(x = 2.08, y = label, label = "SIGNAL"),
    hjust = 1, vjust = 0.4, size = 1.8, fontface = "bold",
    color = unname(OKABE["Arthropoda"])
  ) +
  geom_text(
    data = sig_df %>% filter(sig_tag == "NULL"),
    aes(x = 2.08, y = label, label = "NULL"),
    hjust = 1, vjust = 0.4, size = 1.65, color = "grey55"
  ) +
  scale_x_continuous(limits = c(0, 2.1), expand = c(0, 0),
                     breaks = c(0, 0.5, 1.0, 1.5)) +
  scale_y_discrete(expand = expansion(add = 0.6)) +
  labs(x = "Blomberg's K", y = NULL,
       title = "Phylogenetic signal (K=1: Brownian expectation)") +
  theme_fig2() +
  theme(
    axis.text.y        = element_text(size = 4.8, hjust = 1),
    panel.grid.major.x = element_line(linewidth = 0.2, color = "grey90"),
    panel.background   = element_rect(fill = "grey97", colour = NA),
    plot.margin        = margin(4, 6, 2, 2, "pt"),
    plot.title         = element_text(
      size = 5.0, face = "bold",
      margin = margin(0, 0, 3, 0, "pt")
    )
  )

# ── 6. ASSEMBLE COMPOSITE ────────────────────────────────────
# right column: B (heatmap, taller) / C (bar chart, shorter)
right_col <- panel_B / panel_C +
  plot_layout(heights = c(60, 40))

# full composite: tree (left) | right column
composite <- (panel_A | right_col) +
  plot_layout(widths = c(55, 45))

# panel labels a, b, c
composite <- composite +
  plot_annotation(
    tag_levels = "a",
    caption    = paste(
      "Figure 2 | Cross-species distribution and phylogenetic structure of Sweet Trap.",
      "(a) Time-calibrated tree of 56 species (TimeTree 5, 71 contributing cases across 7 phyla).",
      "(b) ΔST proxy and F1-F4 signature heatmap aligned to tips.",
      "(c) Phylogenetic signal is null at cross-phylum scale (Blomberg K=0.117, p=0.251;",
      "Pagel λ≈0) but strong within Arthropoda (K=1.45, p=0.007),",
      "consistent with convergent rather than inherited expression of Sweet Trap.",
      sep = " "
    )
  ) &
  theme(
    plot.tag     = element_text(size = 7, face = "bold",
                                margin = margin(0, 1, 0, 0, "pt")),
    plot.caption = element_text(size = 4.5, hjust = 0, lineheight = 1.25,
                                margin = margin(4, 0, 0, 0, "pt")),
    plot.margin  = margin(3, 3, 3, 3, "pt")
  )

# ── 7. OUTPUT ────────────────────────────────────────────────
W_in <- 180 / 25.4
H_in <- 170 / 25.4
DPI  <- 600

out_pdf <- file.path(OUTS, "Fig2_distribution_phylogeny.pdf")
out_png <- file.path(OUTS, "Fig2_distribution_phylogeny.png")
out_svg <- file.path(OUTS, "Fig2_distribution_phylogeny.svg")

cairo_pdf(out_pdf, width = W_in, height = H_in, family = "Helvetica")
print(composite)
dev.off()

png(out_png, width = W_in, height = H_in, units = "in",
    res = DPI, type = "cairo")
print(composite)
dev.off()

svg(out_svg, width = W_in, height = H_in)
print(composite)
dev.off()

cat("--- Figure 2 outputs ---\n")
cat(out_pdf, "\n")
cat(out_png, "\n")
cat(out_svg, "\n")
cat(sprintf("Canvas: %.0f x %.0f mm  |  DPI (raster): %d\n",
            W_in * 25.4, H_in * 25.4, DPI))
cat(sprintf("Species in pruned tree: %d\n", n_sp))
cat("Done.\n")
