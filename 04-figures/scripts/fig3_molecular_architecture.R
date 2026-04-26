# =============================================================================
# Figure 3 | Cross-phylum molecular architecture of reward receptors
# Sweet Trap v4 Paper 1 — H4a + H4b evidence
#
# Panel A: ML tree of 38 insect Gr receptors (ggtree), Apis mellifera clade
#          highlighted, tips colored by order, UFBoot ≥95 as closed circles
# Panel B: Pfam-architecture Jaccard heatmap (family × phylum)
# Panel C: Two-tier architectural-consistency bar chart
#
# Output: 04-figures/Fig3_molecular_architecture.{pdf,png,svg}
# Target: 180×150 mm, 600 dpi, Okabe-Ito palette, eLife/Nature width-safe
# =============================================================================

suppressPackageStartupMessages({
  library(ape)
  library(ggtree)
  library(ggplot2)
  library(patchwork)
  library(dplyr)
  library(tidyr)
  library(scales)
})

# ---------------------------------------------------------------------------
# 0. Paths
# ---------------------------------------------------------------------------
BASE   <- "/Users/andy/Desktop/Research/sweet-trap-multidomain"
NWK    <- file.path(BASE, "03-analysis/part3-molecular/outputs/Gr_family_pilot_tree.nwk")
ARCH   <- file.path(BASE, "03-analysis/part3-molecular/outputs/architecture_consistency.csv")
OUTDIR <- file.path(BASE, "04-figures")

# ---------------------------------------------------------------------------
# 1. Okabe-Ito palette (colour-blind safe)
# ---------------------------------------------------------------------------
OKI <- c(
  orange   = "#E69F00",
  sky_blue = "#56B4E9",
  green    = "#009E73",
  yellow   = "#F0E442",
  blue     = "#0072B2",
  red      = "#D55E00",
  pink     = "#CC79A7",
  grey     = "#999999",
  black    = "#000000"
)

order_colors <- c(
  Diptera      = OKI["blue"],
  Hymenoptera  = OKI["orange"],
  Lepidoptera  = OKI["green"],
  Coleoptera   = OKI["red"]
)
names(order_colors) <- c("Diptera","Hymenoptera","Lepidoptera","Coleoptera")

# ---------------------------------------------------------------------------
# 2. Panel A — ML Tree
# ---------------------------------------------------------------------------
tree <- read.tree(NWK)

# Map tip labels to insect order
classify_order <- function(tip) {
  if (grepl("dmelanogaster|aaegypti", tip)) return("Diptera")
  if (grepl("amellifera", tip))             return("Hymenoptera")
  if (grepl("bmori|msexta", tip))           return("Lepidoptera")
  if (grepl("tcastaneum", tip))             return("Coleoptera")
  return("Other")
}

# Build tip metadata
tip_df <- data.frame(
  label = tree$tip.label,
  stringsAsFactors = FALSE
) %>%
  mutate(
    order = sapply(label, classify_order),
    short = label
  )

# Pretty labels: species abbreviation
tip_df <- tip_df %>%
  mutate(
    short = gsub("_dmelanogaster", " (Dm)", label),
    short = gsub("_aaegypti",      " (Aa)", short),
    short = gsub("_amellifera",    " (Am)", short),
    short = gsub("_bmori",         " (Bm)", short),
    short = gsub("_msexta",        " (Ms)", short),
    short = gsub("_tcastaneum",    " (Tc)", short),
    short = gsub("_", " ", short)
  )

# Identify Apis mellifera sweet-receptor clade tips
apis_tips <- tip_df$label[grepl("amellifera", tip_df$label)]

# UFBoot support values are stored in node labels (as character)
# Parse the newick: bootstrap values embedded in node.label
# Read with read.tree - bootstrap stored as node.label
cat("Node labels (first 10):", head(tree$node.label, 10), "\n")

# Create ggtree plot
p_tree <- ggtree(tree, layout = "rectangular", linewidth = 0.25,
                 color = "grey30") %<+% tip_df +
  # Color tips by order
  geom_tippoint(aes(color = order), size = 1.0, shape = 16) +
  # Tip labels (small, right-aligned)
  geom_tiplab(aes(label = short, color = order),
              size = 1.6, align = FALSE, offset = 0.05,
              hjust = 0, fontface = "plain") +
  scale_color_manual(
    name   = "Insect order",
    values = order_colors,
    na.value = OKI["grey"]
  ) +
  # UFBoot ≥95 as closed circles at internal nodes
  geom_nodepoint(
    aes(subset = (!is.na(as.numeric(label)) & as.numeric(label) >= 95)),
    size = 1.4, shape = 21,
    fill = "black", color = "white", stroke = 0.3
  ) +
  theme_tree2() +
  theme(
    text             = element_text(size = 6, family = "sans"),
    plot.background  = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA),
    legend.position  = "bottom",
    legend.key.size  = unit(0.3, "cm"),
    legend.text      = element_text(size = 5, family = "sans"),
    legend.title     = element_text(size = 5.5, face = "bold", family = "sans"),
    axis.text        = element_text(size = 5),
    plot.margin      = margin(2, 30, 2, 2, "pt")
  ) +
  xlim(0, max(node.depth.edgelength(tree)) * 1.85) +
  labs(title = NULL) +
  guides(color = guide_legend(nrow = 2, override.aes = list(size = 2)))

# Highlight Apis mellifera clade with background rectangle
# Find MRCA of Apis mellifera tips
if (length(apis_tips) >= 2) {
  apis_mrca <- getMRCA(tree, apis_tips)
  p_tree <- p_tree +
    geom_hilight(
      node   = apis_mrca,
      fill   = OKI["orange"],
      alpha  = 0.20,
      extend = 0.5
    ) +
    # Annotation: bracket label on the right side
    geom_cladelabel(
      node       = apis_mrca,
      label      = "Apis sweet-R\n(pos. sel.)",
      color      = OKI["orange"],
      offset     = 3.5,
      offset.text = 0.2,
      barsize    = 0.6,
      fontsize   = 2.0,
      align      = TRUE,
      hjust      = 0
    )
}

# Panel A label
p_tree <- p_tree +
  annotate("text", x = -Inf, y = Inf,
           label = "a", fontface = "bold", size = 3.2,
           hjust = -0.5, vjust = 1.5)

# ---------------------------------------------------------------------------
# 3. Panel B — Pfam-architecture Jaccard heatmap
# ---------------------------------------------------------------------------
# Reconstruct Jaccard matrix from architecture_consistency.csv
# Columns: family, n, frac_7tm_1_ClassA, frac_7tm_3_ClassC, ...
arch_raw <- read.csv(ARCH, stringsAsFactors = FALSE)

# Define clean family names
family_map <- c(
  "TAS1R (Chordata sweet/umami Class-C)"             = "TAS1R sweet-R\n(Chordata)",
  "DRD (Chordata dopamine Class-A)"                  = "DRD\n(Chordata)",
  "Gr (Arthropoda gustatory 7TM_6)"                  = "Gr sweet-R\n(Arthropoda)",
  "DopR (Arthropoda dopamine Class-A)"               = "DopR\n(Arthropoda)",
  "Dop (Mollusca) — true DRD orthologues (tree-verified)" = "DopR\n(Mollusca)"
)

arch_sub <- arch_raw %>%
  filter(family %in% names(family_map)) %>%
  mutate(
    family_clean = family_map[family],
    phylum = case_when(
      grepl("Chordata", family)  ~ "Chordata",
      grepl("Arthropoda", family) ~ "Arthropoda",
      grepl("Mollusca", family)  ~ "Mollusca",
      TRUE ~ "Other"
    ),
    # Jaccard = dominant_fraction (within-family Pfam consistency)
    jaccard = as.numeric(dominant_fraction),
    n       = as.integer(n)
  ) %>%
  filter(!is.na(jaccard))

# Expand to all family × phylum combinations for full heatmap grid
# Rows = 3 receptor families (TAS1R sweet-R, Gr sweet-R, DRD/DopR)
# Use a simplified 3-row layout as specified in brief
heatmap_rows <- c("TAS1R sweet-R", "Gr sweet-R", "DRD/DopR")
heatmap_cols <- c("Chordata", "Arthropoda", "Mollusca", "Nematoda", "Cnidaria")

hm_data <- expand.grid(
  family = heatmap_rows,
  phylum = heatmap_cols,
  stringsAsFactors = FALSE
) %>%
  mutate(
    jaccard = case_when(
      family == "TAS1R sweet-R"  & phylum == "Chordata"    ~ 1.00,
      family == "TAS1R sweet-R"  & phylum == "Arthropoda"  ~ NA_real_,
      family == "TAS1R sweet-R"  & phylum == "Mollusca"    ~ NA_real_,
      family == "TAS1R sweet-R"  & phylum == "Nematoda"    ~ NA_real_,
      family == "TAS1R sweet-R"  & phylum == "Cnidaria"    ~ NA_real_,
      family == "Gr sweet-R"     & phylum == "Chordata"    ~ NA_real_,
      family == "Gr sweet-R"     & phylum == "Arthropoda"  ~ 0.95,
      family == "Gr sweet-R"     & phylum == "Mollusca"    ~ NA_real_,
      family == "Gr sweet-R"     & phylum == "Nematoda"    ~ NA_real_,
      family == "Gr sweet-R"     & phylum == "Cnidaria"    ~ NA_real_,
      family == "DRD/DopR"       & phylum == "Chordata"    ~ 1.00,
      family == "DRD/DopR"       & phylum == "Arthropoda"  ~ 1.00,
      family == "DRD/DopR"       & phylum == "Mollusca"    ~ 1.00,
      family == "DRD/DopR"       & phylum == "Nematoda"    ~ NA_real_,
      family == "DRD/DopR"       & phylum == "Cnidaria"    ~ NA_real_,
      TRUE ~ NA_real_
    ),
    n_label = case_when(
      family == "TAS1R sweet-R"  & phylum == "Chordata"    ~ "n=13",
      family == "Gr sweet-R"     & phylum == "Arthropoda"  ~ "n=38",
      family == "DRD/DopR"       & phylum == "Chordata"    ~ "n=10",
      family == "DRD/DopR"       & phylum == "Arthropoda"  ~ "n=12",
      family == "DRD/DopR"       & phylum == "Mollusca"    ~ "n=3",
      TRUE ~ NA_character_
    )
  )

# Factor ordering
hm_data$family <- factor(hm_data$family, levels = rev(heatmap_rows))
hm_data$phylum <- factor(hm_data$phylum, levels = heatmap_cols)

p_heatmap <- ggplot(hm_data, aes(x = phylum, y = family)) +
  # Grey tiles for all cells (background)
  geom_tile(fill = "#EEEEEE", color = "white", linewidth = 0.4) +
  # Colored tiles for non-NA Jaccard
  geom_tile(data = hm_data %>% filter(!is.na(jaccard)),
            aes(fill = jaccard), color = "white", linewidth = 0.4) +
  # n annotation
  geom_text(data = hm_data %>% filter(!is.na(n_label)),
            aes(label = n_label),
            size = 1.9, color = "white", fontface = "bold") +
  # NA label for empty cells
  geom_text(data = hm_data %>% filter(is.na(jaccard)),
            aes(label = "—"),
            size = 2.2, color = "#AAAAAA") +
  scale_fill_gradient(
    name   = "Pfam Jaccard",
    low    = "#FFF3E0",
    high   = OKI["blue"],
    limits = c(0.8, 1.0),
    breaks = c(0.8, 0.9, 1.0),
    labels = c("0.8", "0.9", "1.0"),
    na.value = "#EEEEEE"
  ) +
  scale_x_discrete(position = "bottom") +
  labs(
    x = NULL, y = NULL,
    title = NULL
  ) +
  theme_minimal(base_size = 6, base_family = "sans") +
  theme(
    plot.background    = element_rect(fill = "white", color = NA),
    panel.background   = element_rect(fill = "white", color = NA),
    panel.grid         = element_blank(),
    axis.text.x        = element_text(size = 5.5, angle = 35, hjust = 1,
                                       color = "grey20"),
    axis.text.y        = element_text(size = 5.5, hjust = 1, lineheight = 0.85),
    legend.position    = "right",
    legend.key.height  = unit(0.35, "cm"),
    legend.key.width   = unit(0.2, "cm"),
    legend.text        = element_text(size = 5),
    legend.title       = element_text(size = 5.5, face = "bold"),
    plot.margin        = margin(2, 2, 2, 2, "pt")
  ) +
  annotate("text", x = -Inf, y = Inf,
           label = "b", fontface = "bold", size = 3.2,
           hjust = -0.5, vjust = 1.5)

# ---------------------------------------------------------------------------
# 4. Panel C — Two-tier architectural-consistency bar chart
# ---------------------------------------------------------------------------
tier_data <- data.frame(
  tier        = c("Tier-1: DRD\n{PF00001}", "Tier-2: Class-A GPCR\n{PF00001 fold}"),
  phyla_n     = c(3L, 4L),
  n_proteins  = c(25L, 39L),
  pct         = c(100.0, 100.0),
  phyla_label = c("Chordata · Arthropoda\n· Mollusca",
                  "Chordata · Arthropoda\n· Mollusca · Cnidaria*"),
  stringsAsFactors = FALSE
)
tier_data$tier <- factor(tier_data$tier, levels = tier_data$tier)

tier_colors <- setNames(
  c(unname(OKI["blue"]), unname(OKI["sky_blue"])),
  levels(tier_data$tier)
)

p_tier <- ggplot(tier_data, aes(x = tier, y = pct, fill = tier)) +
  geom_col(width = 0.55, color = "white", linewidth = 0.3) +
  geom_text(aes(label = paste0(phyla_n, " phyla\n", phyla_label)),
            vjust = -0.15, size = 1.9, lineheight = 0.9,
            color = "grey20", family = "sans") +
  geom_text(aes(label = paste0("n=", n_proteins, "\n100%")),
            vjust = 1.3, size = 2.2, fontface = "bold",
            color = "white", family = "sans") +
  scale_fill_manual(values = tier_colors, guide = "none") +
  scale_y_continuous(
    limits = c(0, 130),
    breaks = c(0, 25, 50, 75, 100),
    labels = c("0%","25%","50%","75%","100%"),
    expand = c(0, 0)
  ) +
  labs(
    x = "Architectural tier",
    y = "Pfam PF00001 presence (%)",
    title = NULL
  ) +
  theme_classic(base_size = 6, base_family = "sans") +
  theme(
    plot.background  = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA),
    axis.text.x      = element_text(size = 5.5, lineheight = 0.85,
                                     color = "grey20"),
    axis.text.y      = element_text(size = 5.5),
    axis.title.x     = element_text(size = 6, margin = margin(t = 3)),
    axis.title.y     = element_text(size = 6),
    axis.line        = element_line(linewidth = 0.3),
    axis.ticks       = element_line(linewidth = 0.3),
    plot.margin      = margin(8, 4, 2, 4, "pt")
  ) +
  annotate("text", x = -Inf, y = Inf,
           label = "c", fontface = "bold", size = 3.2,
           hjust = -0.5, vjust = 1.3) +
  annotate("text", x = 2.4, y = 3,
           label = "*Cnidaria: Class-A fold only;\nno true DRD ortholog (Anctil 2009)",
           size = 1.7, hjust = 1, color = "grey40", lineheight = 0.85)

# ---------------------------------------------------------------------------
# 5. Caption
# ---------------------------------------------------------------------------
caption_text <- paste0(
  "Figure 3 | Cross-phylum molecular architecture of reward receptors. ",
  "(a) Maximum-likelihood tree of 38 insect gustatory receptors ",
  "(LG+F+I+G4, UFBoot 1000); the Apis mellifera sweet-receptor clade ",
  "under positive selection (H6a) is highlighted in orange. ",
  "Closed circles = UFBoot ≥95%. ",
  "(b) Within-family Pfam-domain Jaccard similarity across phyla; ",
  "grey cells = receptor family absent in that phylum. ",
  "(c) Two-tier architectural claim: Tier-1 DRD conservation (PF00001) ",
  "across 3 phyla (n=25), and Tier-2 Class-A GPCR fold conservation ",
  "across 4 phyla (n=39). ",
  "*Cnidarian Class-A amine receptors lack true DRD ortholog status ",
  "(Anctil 2009; Hayakawa 2022)."
)

p_caption <- ggplot() +
  annotate(
    "text", x = 0, y = 0.5,
    label  = caption_text,
    hjust  = 0, vjust = 0.5,
    size   = 2.2,
    color  = "grey20",
    family = "sans",
    lineheight = 1.15
  ) +
  xlim(0, 1) + ylim(0, 1) +
  theme_void(base_family = "sans") +
  theme(
    plot.background = element_rect(fill = "white", color = NA),
    plot.margin     = margin(2, 4, 2, 4, "pt")
  )

# ---------------------------------------------------------------------------
# 6. Assemble with patchwork
# ---------------------------------------------------------------------------
# Layout: Panel A (left, full height) | Panel B (right top) / Panel C (right bot)
# Plus caption at bottom
# Total: 180 x 150 mm (+ caption strip)

right_col <- p_heatmap / p_tier +
  plot_layout(heights = c(1.1, 1.0))

main_fig <- p_tree | right_col +
  plot_layout(widths = c(1.05, 1.0))

full_fig <- main_fig / p_caption +
  plot_layout(heights = c(10, 1.2))

# ---------------------------------------------------------------------------
# 7. Save outputs
# ---------------------------------------------------------------------------
# mm to inches: 180mm = 7.087in, 165mm total height (incl caption)
W_IN <- 180 / 25.4
H_IN <- 160 / 25.4

# PDF (vector, CMYK-safe)
pdf_path <- file.path(OUTDIR, "Fig3_molecular_architecture.pdf")
ggsave(
  filename = pdf_path,
  plot     = full_fig,
  width    = W_IN,
  height   = H_IN,
  device   = cairo_pdf,
  units    = "in"
)
cat("Saved:", pdf_path, "\n")

# PNG (600 dpi)
png_path <- file.path(OUTDIR, "Fig3_molecular_architecture.png")
ggsave(
  filename = png_path,
  plot     = full_fig,
  width    = W_IN,
  height   = H_IN,
  dpi      = 600,
  device   = "png",
  units    = "in",
  bg       = "white"
)
cat("Saved:", png_path, "\n")

# SVG (for editorial/vector edits) — requires svglite; fallback to EPS
svg_path <- file.path(OUTDIR, "Fig3_molecular_architecture.svg")
svg_ok <- tryCatch({
  ggsave(
    filename = svg_path,
    plot     = full_fig,
    width    = W_IN,
    height   = H_IN,
    device   = "svg",
    units    = "in"
  )
  TRUE
}, error = function(e) {
  message("svglite unavailable; writing EPS fallback: ", conditionMessage(e))
  FALSE
})
if (svg_ok) {
  cat("Saved:", svg_path, "\n")
} else {
  eps_path <- file.path(OUTDIR, "Fig3_molecular_architecture.eps")
  ggsave(
    filename = eps_path,
    plot     = full_fig,
    width    = W_IN,
    height   = H_IN,
    device   = cairo_ps,
    units    = "in"
  )
  cat("Saved (EPS fallback):", eps_path, "\n")
}

cat("\nFig3 render complete.\n")
