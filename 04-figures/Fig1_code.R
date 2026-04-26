# =============================================================================
# Fig1_code.R — Sweet Trap v4 — eLife Research Advance
# Figure 1 companion R script (reference implementation)
#
# NOTE: The canonical production script is Fig1_code.py (Python/matplotlib).
# This R script produces an equivalent figure using ggplot2 + patchwork + cowplot
# for collaborators who prefer the R ecosystem or wish to modify individual panels
# in ggplot2 grammar.
#
# Run:
#   Rscript /Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/Fig1_code.R
#
# Dependencies (all confirmed available in project R 4.5.3 environment):
#   ggplot2, patchwork, cowplot, scales, grid, gridExtra, showtext, sysfonts, ragg
#
# Single-threaded — complies with project compute-ops-guide.md (n_workers = 1).
# =============================================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(cowplot)
  library(scales)
  library(grid)
  library(gridExtra)
  library(showtext)
  library(sysfonts)
  library(ragg)
})

# ── Font setup ────────────────────────────────────────────────────────────────
# Use system Arial if available; fall back to Liberation Sans (DejaVu-compatible)
if ("Arial" %in% sysfonts::font_families()) {
  font_add("Arial", regular = "Arial.ttf")
} else {
  font_add_google("Source Sans 3", "Arial")
}
showtext_auto()
showtext_opts(dpi = 600)

# ── Output paths ─────────────────────────────────────────────────────────────
SCRIPT_DIR <- normalizePath(dirname(sys.frame(1)$ofile), mustWork = FALSE)
if (!nchar(SCRIPT_DIR)) SCRIPT_DIR <- normalizePath(".")
OUT_DIR    <- file.path(
  "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures"
)
OUT_PDF <- file.path(OUT_DIR, "Fig1_conceptual_framework_R.pdf")
OUT_PNG <- file.path(OUT_DIR, "Fig1_conceptual_framework_R.png")

# ── Okabe-Ito colour-blind-safe palette ──────────────────────────────────────
OKI <- list(
  black   = "#000000",
  orange  = "#E69F00",
  sky     = "#56B4E9",
  green   = "#009E73",
  yellow  = "#F0E442",
  blue    = "#0072B2",
  red     = "#D55E00",
  pink    = "#CC79A7",
  grey    = "#999999",
  ltgrey  = "#DDDDDD",
  white   = "#FFFFFF"
)

PART_COLORS <- c(
  "1" = OKI$blue,
  "2" = OKI$green,
  "3" = OKI$pink,
  "4" = OKI$red
)

# ── eLife dimensions (mm → inches) ───────────────────────────────────────────
MM_TO_IN <- 1 / 25.4
FIG_W    <- 180 * MM_TO_IN   # 7.087 in
FIG_H    <- 175 * MM_TO_IN   # 6.890 in

# ── Base ggplot2 theme (eLife) ────────────────────────────────────────────────
theme_elife <- function(base_size = 8) {
  theme_classic(base_size = base_size, base_family = "Arial") +
    theme(
      text              = element_text(size = base_size, colour = "#000000"),
      plot.title        = element_text(size = base_size, face = "bold",
                                       hjust = 0.5, margin = margin(b = 4)),
      axis.title        = element_text(size = base_size - 0.5),
      axis.text         = element_text(size = base_size - 1.5),
      axis.line         = element_line(linewidth = 0.4),
      axis.ticks        = element_line(linewidth = 0.4),
      legend.text       = element_text(size = base_size - 2),
      legend.title      = element_text(size = base_size - 1, face = "bold"),
      panel.grid.major  = element_blank(),
      panel.grid.minor  = element_blank(),
      plot.margin       = margin(4, 4, 4, 4, "pt"),
    )
}

# =============================================================================
# PANEL B — Δ_ST distribution wedge diagram (ggplot2 version)
# =============================================================================

make_panel_B <- function() {
  x     <- seq(-0.1, 1.1, length.out = 600)
  mu_a  <- 0.30; sigma_a <- 0.10
  mu_m  <- 0.65; sigma_m <- 0.13

  y_a <- dnorm(x, mu_a, sigma_a)
  y_m <- dnorm(x, mu_m, sigma_m)
  y_a <- y_a / max(y_a) * 0.45 + 0.08
  y_m <- y_m / max(y_m) * 0.45 + 0.08

  df_a  <- data.frame(x = x, y = y_a, dist = "S_anc")
  df_m  <- data.frame(x = x, y = y_m, dist = "S_mod")
  df_all <- rbind(df_a, df_m)

  # Wedge polygon
  df_wedge <- data.frame(
    x = c(mu_a, mu_m, mu_m, mu_a),
    y = c(0.40, 0.40, 0.68, 0.68)
  )

  ggplot() +
    # Wedge
    geom_polygon(data = df_wedge,
                 aes(x = x, y = y),
                 fill = OKI$red, alpha = 0.10) +
    # S_anc
    geom_ribbon(data = df_a, aes(x = x, ymin = 0.08, ymax = y),
                fill = OKI$grey, alpha = 0.25) +
    geom_line(data = df_a, aes(x = x, y = y),
              colour = OKI$grey, linewidth = 0.9, linetype = "dashed") +
    # S_mod
    geom_ribbon(data = df_m, aes(x = x, ymin = 0.08, ymax = y),
                fill = OKI$blue, alpha = 0.25) +
    geom_line(data = df_m, aes(x = x, y = y),
              colour = OKI$blue, linewidth = 1.1) +
    # Baseline
    geom_hline(yintercept = 0.08, linewidth = 0.5, colour = "black") +
    # Peak dotted lines
    geom_vline(xintercept = mu_a, linewidth = 0.6, linetype = "dotted",
               colour = OKI$grey) +
    geom_vline(xintercept = mu_m, linewidth = 0.6, linetype = "dotted",
               colour = OKI$blue) +
    # Delta_ST brace annotation
    annotate("segment", x = mu_a, xend = mu_m, y = 0.64, yend = 0.64,
             colour = OKI$red, linewidth = 1.0,
             arrow = arrow(ends = "both", type = "closed",
                           length = unit(0.08, "cm"))) +
    annotate("text", x = (mu_a + mu_m) / 2, y = 0.67,
             label = expression(Delta[ST] == U[perc] - E * "[" * U[fit] * "|B]"),
             hjust = 0.5, vjust = 0, size = 2.5,
             colour = OKI$red, fontface = "bold") +
    # t_sep arrow
    annotate("segment", x = mu_a + 0.02, xend = mu_m + 0.04,
             y = 0.12, yend = 0.12,
             colour = OKI$orange, linewidth = 0.8,
             arrow = arrow(type = "closed", length = unit(0.08, "cm"))) +
    annotate("text", x = (mu_a + mu_m) / 2 + 0.04, y = 0.135,
             label = expression(t[sep]), hjust = 0.5, vjust = 0,
             size = 2.3, colour = OKI$orange) +
    # Distribution labels
    annotate("text", x = mu_a - 0.02, y = max(df_a$y) + 0.04,
             label = expression(S[anc]), size = 2.5, colour = OKI$grey,
             fontface = "italic", hjust = 0.5) +
    annotate("text", x = mu_m + 0.03, y = max(df_m$y) + 0.04,
             label = expression(S[mod]), size = 2.5, colour = OKI$blue,
             fontface = "italic", hjust = 0.5) +
    # Axiom text (right side, appended via cowplot::draw_label outside ggplot)
    labs(title = expression("Axiomatic framework & " * Delta[ST] * " scalar")) +
    scale_x_continuous(limits = c(-0.1, 1.1), expand = c(0, 0)) +
    scale_y_continuous(limits = c(0, 1.05), expand = c(0, 0)) +
    theme_elife() +
    theme(
      axis.text   = element_blank(),
      axis.ticks  = element_blank(),
      axis.title  = element_blank(),
      axis.line   = element_blank(),
      plot.title  = element_text(size = 8, face = "bold")
    )
}

# =============================================================================
# PANEL C — Four-part evidence architecture (ggplot2 version)
# =============================================================================

make_panel_C <- function() {
  # Build rectangles for 4 parts
  n      <- 4
  margin <- 0.04
  gap    <- 0.025
  bw     <- (1 - 2 * margin - (n - 1) * gap) / n
  bh     <- 0.78    # box height fraction
  by0    <- 0.08
  hdr_h  <- 0.20   # header as fraction of box height

  parts <- data.frame(
    num   = 1:4,
    title = c("Human\nSweet Trap", "Animal\nPhylogenetic",
              "Molecular\nConvergence", "Genetic\nCausality"),
    col   = unname(PART_COLORS),
    stringsAsFactors = FALSE
  )

  body_lines <- list(
    c("Trans-ancestry MR", "5 ancestries × 6 cohorts",
      "NHANES · UKBiobank · FinnGen", "BBJ · MVP · AoU",
      "Key stat: pooled β ≥ 0.10", "(H1: behavioural + causal)"),
    c("PRISMA meta-analysis", "≥ 50 cases × 6 phyla",
      "TimeTree + Open Tree of Life", "Blomberg K, Pagel λ, PGLS",
      "Key stat: K ≥ 0.30", "(H2 + H3 + H5)"),
    c("Two-tier: H4a + H4b", "Ensembl / Ensembl Metazoa",
      "PAML codeml dN/dS", "InterPro Jaccard ≥ 0.70",
      "Key stat: cross-phyla identity", "30–50 % (convergence sig.)"),
    c("Branch-site Model A (PAML)", "15 genes × 4 eco-shift lineages",
      "+ lit. synthesis ≥ 30 expts", "hummingbird TAS1R1 control",
      "Key stat: ≥ 3/15 genes LRT", "p < 0.05 (H6a + H6f)")
  )

  rects <- do.call(rbind, lapply(seq_len(n), function(i) {
    x0 <- margin + (i - 1) * (bw + gap)
    data.frame(
      xmin = x0, xmax = x0 + bw,
      ymin_body = by0, ymax_body = by0 + bh,
      ymin_hdr  = by0 + bh - hdr_h * bh,
      ymax_hdr  = by0 + bh,
      col = parts$col[i],
      num = parts$num[i],
      title = parts$title[i],
      x_ctr = x0 + bw / 2,
      stringsAsFactors = FALSE
    )
  }))

  # Arrow segments
  arrows_df <- data.frame(
    x0 = rects$xmax[-n] + 0.005,
    x1 = rects$xmin[-1] - 0.005,
    y  = by0 + bh / 2
  )

  p <- ggplot() +
    # Body rectangles
    geom_rect(data = rects,
              aes(xmin = xmin, xmax = xmax, ymin = ymin_body, ymax = ymax_body,
                  colour = col),
              fill = NA, linewidth = 0.6) +
    # Background fill (very light)
    geom_rect(data = rects,
              aes(xmin = xmin, xmax = xmax,
                  ymin = ymin_body, ymax = ymax_body),
              fill = rects$col, alpha = 0.07) +
    # Header fill
    geom_rect(data = rects,
              aes(xmin = xmin, xmax = xmax,
                  ymin = ymin_hdr, ymax = ymax_hdr),
              fill = rects$col, alpha = 0.75) +
    # Part numbers
    geom_text(data = rects,
              aes(x = xmin + 0.015,
                  y = (ymin_hdr + ymax_hdr) / 2,
                  label = as.character(num)),
              hjust = 0, vjust = 0.5,
              size = 5, fontface = "bold", colour = "white") +
    # Part titles
    geom_text(data = rects,
              aes(x = x_ctr,
                  y = (ymin_hdr + ymax_hdr) / 2,
                  label = title),
              hjust = 0.5, vjust = 0.5,
              size = 2.6, fontface = "bold", colour = "white") +
    # Connector arrows
    geom_segment(data = arrows_df,
                 aes(x = x0, xend = x1, y = y, yend = y),
                 colour = "black", linewidth = 0.7,
                 arrow = arrow(type = "closed",
                               length = unit(0.10, "cm"))) +
    scale_colour_identity() +
    scale_x_continuous(limits = c(0, 1), expand = c(0, 0)) +
    scale_y_continuous(limits = c(0, 1), expand = c(0, 0)) +
    labs(title = "Four-part evidence architecture testing the Sweet Trap thesis") +
    theme_void() +
    theme(
      plot.title = element_text(
        size = 8.5, face = "bold", hjust = 0.5,
        margin = margin(b = 4, t = 2)
      )
    )

  # Add body text via annotation_custom (grob approach, simpler)
  for (i in seq_len(n)) {
    lines <- body_lines[[i]]
    r     <- rects[i, ]
    line_h <- (r$ymin_hdr - r$ymin_body - 0.02) / length(lines)
    for (j in seq_along(lines)) {
      ly <- r$ymin_hdr - 0.02 - (j - 0.5) * line_h
      fw <- if (grepl("^Key stat", lines[j])) "bold" else "plain"
      lc <- if (grepl("^Key stat", lines[j])) r$col else "black"
      p  <- p + annotate("text",
                          x = r$x_ctr, y = ly,
                          label = lines[j],
                          size = 1.95, fontface = fw, colour = lc,
                          hjust = 0.5, vjust = 0.5)
    }
  }

  p
}

# =============================================================================
# Assemble and save
# =============================================================================

message("Building Panel B (distribution wedge)...")
pB <- make_panel_B()

message("Building Panel C (evidence architecture)...")
pC <- make_panel_C()

# Panel A is text-only in this R version — use a placeholder cowplot text panel
pA <- ggdraw() +
  draw_label("Panel (a): see Python script\nFig1_code.py for\nfully-rendered\ncross-phyla icons",
             fontfamily = "Arial", size = 7, colour = OKI$grey,
             x = 0.5, y = 0.5, hjust = 0.5, vjust = 0.5) +
  theme(plot.background = element_rect(
    fill = "white", colour = OKI$ltgrey, linewidth = 0.5))

message("Assembling figure...")
fig <- (pA + pB) / pC +
  plot_layout(heights = c(1, 0.85)) +
  plot_annotation(
    theme = theme(
      plot.background = element_rect(fill = "white", colour = NA),
      plot.margin     = margin(3, 3, 3, 3, "mm")
    )
  )

message("Saving R figure outputs...")
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

# PNG (raster, 600 dpi via ragg)
agg_png(OUT_PNG,
        width = FIG_W, height = FIG_H, units = "in",
        res = 600, background = "white")
print(fig)
invisible(dev.off())
message("Saved: ", OUT_PNG)

# PDF (vector via grDevices)
pdf(OUT_PDF,
    width = FIG_W, height = FIG_H,
    useDingbats = FALSE)
print(fig)
invisible(dev.off())
message("Saved: ", OUT_PDF)

message("R figure production complete.")
message("NOTE: Panels B and C rendered; Panel A uses placeholder.")
message("      For production-quality Panel A, use Fig1_code.py.")
