## ============================================================
## Figure 5 — Layered Evidence: Four-Layer Falsification of
##            Sweet Trap Universality
## Sweet Trap v4 Paper 1 — C-path pivot (RSOS target)
##
## Layout: single-panel vertical infographic
##   Four horizontal bars (L1–L4) stacked top-to-bottom
##   Each bar: layer label | hypothesis | verdict badge | evidence box
##   Bottom: horizontal arrow with lineage-specific origins conclusion
##
## Output: 180 × 140 mm, 600 dpi PNG / cairo PDF / SVG
## Palette: Okabe-Ito (colour-blind safe)
##
## Numbers verified against manuscript.md on 2026-04-25
## ============================================================

library(grid)

base_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures"
out_pdf  <- file.path(base_dir, "Fig5_falsification_layered.pdf")
out_png  <- file.path(base_dir, "Fig5_falsification_layered.png")
out_svg  <- file.path(base_dir, "Fig5_falsification_layered.svg")

w_in <- 180 / 25.4
h_in <- 140 / 25.4

# ── Okabe-Ito palette ─────────────────────────────────────────────────────────
OI <- list(
  blue    = "#0072B2",
  orange  = "#E69F00",
  green   = "#009E73",
  red     = "#D55E00",
  yellow  = "#F0E442",
  purple  = "#CC79A7",
  sky     = "#56B4E9",
  black   = "#000000",
  grey    = "#888888",
  lgrey   = "#DDDDDD",
  vlight  = "#F7F7F7"
)

COL_SUPPORTED <- OI$green
COL_REFUTED   <- OI$red
COL_PARTIAL   <- OI$orange

fade <- function(col, a = 0.22) {
  v <- col2rgb(col) / 255
  rgb(v[1] + (1 - v[1]) * (1 - a),
      v[2] + (1 - v[2]) * (1 - a),
      v[3] + (1 - v[3]) * (1 - a))
}

# Draw verdict symbol using grid primitives (avoids Unicode font issues)
draw_verdict_sym <- function(cx, cy, type, col, sz = 0.018) {
  if (type == "check") {
    grid.lines(x = c(cx - sz*0.9, cx - sz*0.1, cx + sz*1.0),
               y = c(cy - sz*0.3, cy - sz*1.1, cy + sz*0.8),
               gp = gpar(col = col, lwd = 2.4), default.units = "npc")
  } else if (type == "cross") {
    grid.lines(x = c(cx - sz*0.7, cx + sz*0.7),
               y = c(cy - sz*0.7, cy + sz*0.7),
               gp = gpar(col = col, lwd = 2.4), default.units = "npc")
    grid.lines(x = c(cx + sz*0.7, cx - sz*0.7),
               y = c(cy - sz*0.7, cy + sz*0.7),
               gp = gpar(col = col, lwd = 2.4), default.units = "npc")
  } else if (type == "diamond") {
    grid.polygon(x = c(cx, cx + sz, cx, cx - sz),
                 y = c(cy + sz*0.7, cy, cy - sz*0.7, cy),
                 gp = gpar(fill = col, col = col, lwd = 0.5),
                 default.units = "npc")
  }
}

# ── Layer data ────────────────────────────────────────────────────────────────
layers <- list(
  list(
    id        = "L1",
    label     = "L1\nExistence",
    hyp       = "Sweet Trap is detectable\nin many lineages",
    verdict   = "SUPPORTED",
    sym_type  = "check",
    bar_col   = COL_SUPPORTED,
    ev_lines  = c(
      "114 cases / 7 phyla / 56 species satisfy F1-F4",
      "4/4 trans-ancestry MR chains in H. sapiens (OR 1.12-1.41; p < 0.001)"
    )
  ),
  list(
    id        = "L2",
    label     = "L2\nPhylogenetic\nsignal",
    hyp       = "Delta_ST structured by\nancestry (K > 0.30)",
    verdict   = "REFUTED",
    sym_type  = "cross",
    bar_col   = COL_REFUTED,
    ev_lines  = c(
      "K = 0.117 cross-phylum (p = 0.251) — below falsification threshold",
      "Within-Arthropoda K = 1.446 (p = 0.007) — clade-level boundary case"
    )
  ),
  list(
    id        = "L3",
    label     = "L3\nShared\nmolecular",
    hyp       = "Reward receptors share\nPfam architecture across phyla",
    verdict   = "NOT\nENRICHED",
    sym_type  = "diamond",
    bar_col   = COL_PARTIAL,
    ev_lines  = c(
      "TAS1R / Gr Pfam Jaccard = 0 (zero shared domains)",
      "P(Jaccard=0|null) = 0.9998 — not statistically unexpected under null"
    )
  ),
  list(
    id        = "L4",
    label     = "L4\nUniversal\nselection",
    hyp       = "Multiple eco-shift clades\nshow LRT > Bonferroni threshold",
    verdict   = "INCONCLUSIVE\noptimiser-\nsensitive",
    sym_type  = "diamond",
    bar_col   = COL_PARTIAL,
    ev_lines  = c(
      "3/6 robustly null; 3/6 optimiser-sensitive; 0/6 robust positives",
      "All 3 non-zero signals in small-clade boundary-artefact range (omega > 30, n <= 7)"
    )
  )
)

# ── Layout constants ──────────────────────────────────────────────────────────
margin_l  <- 0.018
margin_r  <- 0.018
margin_t  <- 0.055   # space for title + header row
margin_b  <- 0.185   # space for bottom arrow + conclusion

plot_w    <- 1 - margin_l - margin_r
plot_h    <- 1 - margin_t - margin_b

n_layers  <- length(layers)
bar_gap   <- 0.012
bar_h     <- (plot_h - (n_layers - 1) * bar_gap) / n_layers

# Column layout (as fractions of plot_w):
#   col_id width  0.13 — layer label (multi-line)
#   col_hyp width 0.30 — hypothesis text
#   col_vrd width 0.17 — verdict badge
#   col_ev  width 0.40 — evidence text
col_id_w  <- 0.13
col_hyp_w <- 0.30
col_vrd_w <- 0.17
col_ev_w  <- 1 - col_id_w - col_hyp_w - col_vrd_w   # remainder

# Helpers
gt <- function(x, y, label, fs = 6, col = OI$black, face = "plain",
               hjust = "center", vjust = "center") {
  grid.text(label, x = x, y = y, just = c(hjust, vjust),
            gp = gpar(fontsize = fs, col = col, fontface = face),
            default.units = "npc")
}

rrect <- function(x, y, w, h, col, border = NA, lwd = 0.7,
                  r = unit(3, "pt")) {
  grid.roundrect(x = x, y = y, width = w, height = h, r = r,
                 gp = gpar(fill = col, col = border, lwd = lwd),
                 default.units = "npc")
}

# ── Draw one layer bar (called inside main viewport) ─────────────────────────
draw_layer <- function(lyr, y_bot, bar_h_npc) {
  # All x positions in npc relative to full figure
  xl   <- margin_l
  xr   <- 1 - margin_r
  ymid <- y_bot + bar_h_npc / 2

  # -- Background bar
  grid.rect(x = (xl + xr) / 2, y = ymid,
            width = xr - xl, height = bar_h_npc,
            gp = gpar(fill = fade(lyr$bar_col, 0.25),
                      col  = lyr$bar_col, lwd = 0.8),
            default.units = "npc")

  # -- Column boundaries (x in npc)
  x1 <- xl
  x2 <- x1 + plot_w * col_id_w
  x3 <- x2 + plot_w * col_hyp_w
  x4 <- x3 + plot_w * col_vrd_w
  x5 <- xr

  # Thin vertical dividers
  for (xd in c(x2, x3, x4)) {
    grid.lines(x = c(xd, xd),
               y = c(y_bot + 0.004, y_bot + bar_h_npc - 0.004),
               gp = gpar(col = lyr$bar_col, lwd = 0.4, lty = "solid"),
               default.units = "npc")
  }

  # -- Col 1: layer ID label
  gt((x1 + x2) / 2, ymid, lyr$label,
     fs = 5.8, col = lyr$bar_col, face = "bold")

  # -- Col 2: hypothesis (centred in bar)
  gt((x2 + x3) / 2, ymid, lyr$hyp,
     fs = 5.2, col = OI$black, face = "italic")

  # -- Col 3: verdict badge (filled box)
  rrect((x3 + x4) / 2, ymid,
        w = unit((x4 - x3) * w_in * 25.4 - 4, "mm"),
        h = unit(bar_h_npc * h_in * 25.4 - 4, "mm"),
        col = lyr$bar_col, border = NA,
        r = unit(4, "pt"))
  # symbol (drawn primitive)
  draw_verdict_sym((x3 + x4) / 2, ymid + 0.022, lyr$sym_type, "white", sz = 0.014)
  # verdict text — shrink font for 3-line verdicts so they fit in the badge
  n_verdict_lines <- length(strsplit(lyr$verdict, "\n", fixed = TRUE)[[1]])
  verdict_fs <- if (n_verdict_lines >= 3) 4.2 else 5.0
  gt((x3 + x4) / 2, ymid - 0.018, lyr$verdict,
     fs = verdict_fs, col = "white", face = "bold")

  # -- Col 4: evidence lines
  ev_x   <- x4 + 0.010
  ev_n   <- length(lyr$ev_lines)
  ev_lh  <- bar_h_npc * 0.30
  ev_top <- ymid + (ev_n - 1) * ev_lh / 2

  for (k in seq_along(lyr$ev_lines)) {
    gt(ev_x, ev_top - (k - 1) * ev_lh,
       lyr$ev_lines[[k]],
       fs = 4.8, col = OI$black, face = "plain", hjust = "left")
  }
}

# ── Bottom conclusion arrow ───────────────────────────────────────────────────
draw_conclusion <- function() {
  arr_y   <- margin_b * 0.62
  txt1_y  <- margin_b * 0.42
  txt2_y  <- margin_b * 0.22
  xl      <- margin_l + 0.02
  xr      <- 1 - margin_r - 0.02

  # Arrow
  grid.lines(x = c(xl, xr), y = c(arr_y, arr_y),
             gp = gpar(col = OI$black, lwd = 2.2),
             arrow = arrow(length = unit(7, "pt"), type = "closed", ends = "last"),
             default.units = "npc")
  gt(xl, arr_y + 0.022, "Lineage-specific origins model",
     fs = 7.2, col = OI$black, face = "bold", hjust = "left")
  gt(margin_l + 0.005, txt1_y,
     "Sweet Trap re-emerges where local ecological conditions decouple reward signals from fitness;",
     fs = 5.5, col = OI$black, face = "plain", hjust = "left")
  gt(margin_l + 0.005, txt2_y,
     "identifying these conditions is the Paper 2 mission.",
     fs = 5.5, col = OI$grey, face = "italic", hjust = "left")
}

# ── Master draw ───────────────────────────────────────────────────────────────
draw_fig5 <- function() {

  # Figure title
  grid.text("Figure 5  |  Four-layer pre-registered test of Sweet Trap universality",
            x = 0.5, y = 1 - margin_t * 0.25,
            gp = gpar(fontsize = 7.5, fontface = "bold", col = OI$black),
            default.units = "npc")

  # Column header row
  hdr_y <- 1 - margin_t * 0.55
  xl <- margin_l
  x2 <- xl + plot_w * col_id_w
  x3 <- x2 + plot_w * col_hyp_w
  x4 <- x3 + plot_w * col_vrd_w
  xr <- 1 - margin_r

  hdrs <- list(
    list((xl + x2) / 2, "Layer"),
    list((x2 + x3) / 2, "Pre-registered hypothesis"),
    list((x3 + x4) / 2, "Verdict"),
    list((x4 + xr) / 2, "Evidence")
  )
  for (h in hdrs) {
    gt(h[[1]], hdr_y, h[[2]], fs = 5.8, col = OI$grey, face = "bold")
  }
  grid.lines(x = c(margin_l, 1 - margin_r),
             y = c(1 - margin_t * 0.75, 1 - margin_t * 0.75),
             gp = gpar(col = OI$lgrey, lwd = 0.6), default.units = "npc")

  # Layer bars (draw from top to bottom: L1 at top)
  for (i in seq_len(n_layers)) {
    y_bot <- margin_b + (n_layers - i) * (bar_h + bar_gap)
    draw_layer(layers[[i]], y_bot, bar_h)
  }

  # Bottom separator
  sep_y <- margin_b - 0.010
  grid.lines(x = c(margin_l, 1 - margin_r), y = c(sep_y, sep_y),
             gp = gpar(col = OI$lgrey, lwd = 0.8), default.units = "npc")

  # Conclusion arrow
  draw_conclusion()
}

# ── Render ────────────────────────────────────────────────────────────────────
cairo_pdf(out_pdf, width = w_in, height = h_in, family = "Helvetica")
grid.newpage()
draw_fig5()
invisible(dev.off())
message("PDF: ", out_pdf)

png(out_png, width = round(w_in * 600), height = round(h_in * 600),
    res = 600, type = "cairo", family = "Helvetica")
grid.newpage()
draw_fig5()
invisible(dev.off())
message("PNG: ", out_png)

svg(out_svg, width = w_in, height = h_in, family = "Helvetica")
grid.newpage()
draw_fig5()
invisible(dev.off())
message("SVG: ", out_svg)

message("Done. Fig5_falsification_layered rendered.")
