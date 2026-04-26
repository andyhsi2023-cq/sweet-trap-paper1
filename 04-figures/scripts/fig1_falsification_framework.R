## ============================================================
## Figure 1 — Pre-registered Falsification Framework
## Sweet Trap v4 Paper 1 — C-path pivot (RSOS target)
##
## Layout: 3 panels A | B | C  (all coordinates in panel-local npc)
##   A (~60 mm): Operational scalar definition (Δ_ST bar diagram + A1-A4)
##   B (~70 mm): Three pre-registered universality predictions + outcomes
##   C (~50 mm): Widespread-but-not-universal outcome label + tree cartoon
##
## Output: 180 × 130 mm, 600 dpi PNG / cairo PDF / SVG
## Palette: Okabe-Ito (colour-blind safe)
## ============================================================

library(grid)

base_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures"
out_pdf  <- file.path(base_dir, "Fig1_falsification_framework.pdf")
out_png  <- file.path(base_dir, "Fig1_falsification_framework.png")
out_svg  <- file.path(base_dir, "Fig1_falsification_framework.svg")

w_in <- 180 / 25.4
h_in <- 130 / 25.4

OI <- list(
  blue    = "#0072B2",
  orange  = "#E69F00",
  green   = "#009E73",
  red     = "#D55E00",
  purple  = "#CC79A7",
  sky     = "#56B4E9",
  black   = "#000000",
  grey    = "#888888",
  lgrey   = "#CCCCCC",
  vlight  = "#F6F6F6"
)
COL_REFUTED   <- OI$red
COL_PARTIAL   <- OI$orange
COL_SUPPORTED <- OI$green
COL_PRED      <- OI$blue

fade <- function(col, a = 0.22) {
  v <- col2rgb(col) / 255
  rgb(v[1]+(1-v[1])*(1-a), v[2]+(1-v[2])*(1-a), v[3]+(1-v[3])*(1-a))
}

# helpers: all coordinates in current viewport npc
gt <- function(x, y, label, fs=6, col=OI$black, face="plain",
               hjust="center", vjust="center") {
  grid.text(label, x=x, y=y, just=c(hjust, vjust),
            gp=gpar(fontsize=fs, col=col, fontface=face),
            default.units="npc")
}

rrect <- function(x, y, w, h, fill, border=NA, lwd=0.7, r=unit(3,"pt")) {
  grid.roundrect(x=x, y=y, width=w, height=h, r=r,
                 gp=gpar(fill=fill, col=border, lwd=lwd),
                 default.units="npc")
}

# Draw verdict symbol using grid primitives (avoids Unicode font issues)
# type: "check" | "cross" | "diamond"
draw_verdict_sym <- function(cx, cy, type, col, sz=0.020) {
  if (type == "check") {
    # tick: short down-left then longer up-right
    grid.lines(x=c(cx-sz*0.9, cx-sz*0.1, cx+sz*1.0),
               y=c(cy-sz*0.3, cy-sz*1.1, cy+sz*0.8),
               gp=gpar(col=col, lwd=2.2), default.units="npc")
  } else if (type == "cross") {
    # X: two diagonal lines
    grid.lines(x=c(cx-sz*0.7, cx+sz*0.7), y=c(cy-sz*0.7, cy+sz*0.7),
               gp=gpar(col=col, lwd=2.2), default.units="npc")
    grid.lines(x=c(cx+sz*0.7, cx-sz*0.7), y=c(cy-sz*0.7, cy+sz*0.7),
               gp=gpar(col=col, lwd=2.2), default.units="npc")
  } else if (type == "diamond") {
    grid.polygon(x=c(cx, cx+sz, cx, cx-sz),
                 y=c(cy+sz*0.7, cy, cy-sz*0.7, cy),
                 gp=gpar(fill=col, col=col, lwd=0.5), default.units="npc")
  }
}

# ══════════════════════════════════════════════════════════════════
# PANEL A  —  scalar definition + axioms
# ══════════════════════════════════════════════════════════════════
draw_panel_A <- function() {
  # Bar layout
  bx      <- 0.28
  bw      <- 0.28
  bar_bot <- 0.10
  bar_top <- 0.86

  total_h  <- bar_top - bar_bot
  ufit_h   <- total_h * 0.40
  uperc_h  <- total_h * 0.60

  y_fit_bot  <- bar_bot
  y_fit_top  <- bar_bot + ufit_h
  y_perc_bot <- y_fit_top
  y_perc_top <- bar_top

  # E[U_fit|B] — hatched bar
  grid.rect(x=bx, y=(y_fit_bot+y_fit_top)/2,
            width=bw, height=ufit_h,
            gp=gpar(fill=fade(OI$sky,0.5), col=OI$blue, lwd=0.9),
            default.units="npc")
  for (i in 1:7) {
    yh <- y_fit_bot + ufit_h/(7+1)*i
    grid.lines(x=c(bx-bw/2, bx+bw/2), y=c(yh,yh),
               gp=gpar(col=OI$blue, lwd=0.5), default.units="npc")
  }
  gt(bx, (y_fit_bot+y_fit_top)/2,
     expression(E*"["*U[fit]*"|"*B*"]"),
     fs=5.5, col=OI$blue, face="bold")

  # U_perc — solid bar
  grid.rect(x=bx, y=(y_perc_bot+y_perc_top)/2,
            width=bw, height=uperc_h,
            gp=gpar(fill=fade(OI$orange,0.5), col=OI$orange, lwd=0.9),
            default.units="npc")
  gt(bx, (y_perc_bot+y_perc_top)/2,
     expression(U[perc]), fs=5.5, col="#B85000", face="bold")

  # Δ_ST arrow on right side
  arr_x <- bx + bw/2 + 0.06
  grid.lines(x=c(arr_x,arr_x), y=c(y_fit_top, y_perc_top),
             gp=gpar(col=OI$red, lwd=1.8),
             arrow=arrow(length=unit(4,"pt"), type="closed", ends="both"),
             default.units="npc")
  grid.text(expression(Delta[ST]),
            x=arr_x+0.005, y=(y_fit_top+y_perc_top)/2 + 0.050,
            just=c("left","center"),
            gp=gpar(fontsize=6.5, col=OI$red, fontface="bold"),
            default.units="npc")
  grid.text(expression("= " * U[perc] - E*"["*U[fit]*"|"*B*"]"),
            x=arr_x+0.005, y=(y_fit_top+y_perc_top)/2 + 0.000,
            just=c("left","center"),
            gp=gpar(fontsize=5.0, col=OI$red, fontface="plain"),
            default.units="npc")

  # ── Axiom legend ─────────────────────────────────────────────────────────
  ax_x  <- 0.05
  ax_y0 <- 0.96
  ax_lh <- 0.108

  gt(ax_x, ax_y0+0.018, "Axioms", fs=5.8, col=OI$black, face="bold", hjust="left")

  axioms <- list(
    list("A1","Ancestral Calibration",   OI$blue),
    list("A2","Environmental Decoupling",OI$green),
    list("A3","Endorsement Inertia",     OI$orange),
    list("A4","Partial Cost Visibility", OI$purple)
  )
  for (i in seq_along(axioms)) {
    ax <- axioms[[i]]
    yy <- ax_y0 - i*ax_lh
    rrect(ax_x+0.036, yy+0.008, w=unit(14,"pt"), h=unit(9,"pt"),
          fill=ax[[3]], border=NA)
    gt(ax_x+0.036, yy+0.008, ax[[1]], fs=5.0, col="white", face="bold")
    gt(ax_x+0.105, yy+0.008, ax[[2]], fs=5.0, col=OI$black, hjust="left")
  }
}

# ══════════════════════════════════════════════════════════════════
# PANEL B  —  three predictions + observed outcomes
# All coordinates in panel-local npc [0,1]x[0,1]
# ══════════════════════════════════════════════════════════════════
draw_panel_B <- function() {

  # Three equal columns
  ncols  <- 3
  cpad   <- 0.020   # horizontal padding inside each column cell
  col_xs <- c(1/6, 3/6, 5/6)  # column centres
  col_w_npc <- 1/3 - cpad     # box width per column (npc)

  # Row geometry
  hdr_h    <- 0.060
  pred_top <- 1 - hdr_h - 0.008
  pred_bot <- 0.500 + 0.025
  pred_mid <- (pred_top + pred_bot) / 2
  pred_h   <- pred_top - pred_bot

  obs_top  <- 0.500 - 0.025
  obs_bot  <- 0.030
  obs_mid  <- (obs_top + obs_bot) / 2
  obs_h    <- obs_top - obs_bot

  # Section headers
  gt(0.50, 1 - hdr_h/2 - 0.002,
     "If Sweet Trap is universal...",
     fs=6.0, col=OI$black, face="bold")
  gt(0.50, 0.500,
     "Observed outcome",
     fs=6.0, col=OI$black, face="bold")

  # Divider
  grid.lines(x=c(0.01,0.99), y=c(0.499,0.499),
             gp=gpar(col=OI$lgrey, lwd=0.8, lty="dashed"),
             default.units="npc")

  # Thin vertical column separators
  for (xsep in c(1/3, 2/3)) {
    grid.lines(x=c(xsep,xsep), y=c(0.03,0.97),
               gp=gpar(col=OI$lgrey, lwd=0.4), default.units="npc")
  }

  preds <- list(
    list(
      title    = "Cross-phylum\nphylogenetic signal",
      pred_txt = "Predicted K > 0.30",
      icon_fn  = draw_tree_icon,
      verdict  = "REFUTED",
      v_col    = COL_REFUTED,
      v_sym    = "cross",
      ev       = list("K = 0.117", "p = 0.251", "(cross-phylum)")
    ),
    list(
      title    = "Shared molecular\nsubstrate",
      pred_txt = "Pfam Jaccard\n> null expectation",
      icon_fn  = draw_pfam_icon,
      verdict  = "NOT ENRICHED",
      v_col    = COL_PARTIAL,
      v_sym    = "diamond",
      ev       = list("TAS1R/Gr Jaccard = 0",
                      "P(J=0|null) = 0.9998",
                      "(non-convergent substrate)")
    ),
    list(
      title    = "Lineage-specific\npositive selection",
      pred_txt = ">=2 clades LRT\n> Bonferroni threshold",
      icon_fn  = draw_branch_icon,
      verdict  = "PARTIALLY\nREFUTED",
      v_col    = COL_REFUTED,
      v_sym    = "cross",
      ev       = list("1/6 clades tentative", "(Apis Gr_sweet)",
                      "5/6 LRT = 0")
    )
  )

  for (i in seq_along(preds)) {
    p  <- preds[[i]]
    cx <- col_xs[[i]]

    # ── Prediction box ────────────────────────────────────────────────────
    rrect(cx, pred_mid, w=col_w_npc, h=pred_h,
          fill=fade(COL_PRED, 0.28), border=COL_PRED, lwd=0.7,
          r=unit(3,"pt"))

    # Icon at top of prediction box
    icon_y <- pred_mid + pred_h*0.30
    p$icon_fn(cx, icon_y)

    # Column title
    gt(cx, pred_mid + 0.015, p$title,
       fs=5.2, col=OI$blue, face="bold")
    # Predicted threshold text
    gt(cx, pred_mid - pred_h*0.32, p$pred_txt,
       fs=4.8, col=OI$black)

    # Arrow from pred box to obs box
    arrow_bot <- pred_bot - 0.010
    arrow_top <- obs_top + 0.010
    grid.lines(x=c(cx,cx), y=c(arrow_bot, arrow_top),
               gp=gpar(col=OI$grey, lwd=0.8),
               arrow=arrow(length=unit(4,"pt"), type="open", ends="last"),
               default.units="npc")

    # ── Outcome box ───────────────────────────────────────────────────────
    rrect(cx, obs_mid, w=col_w_npc, h=obs_h,
          fill=fade(p$v_col, 0.30), border=p$v_col, lwd=0.9,
          r=unit(3,"pt"))

    # Symbol (drawn primitive — no Unicode)
    draw_verdict_sym(cx, obs_mid + obs_h*0.28, p$v_sym, "white", sz=0.028)
    # Verdict
    gt(cx, obs_mid + 0.010, p$verdict,
       fs=5.2, col=p$v_col, face="bold")
    # Evidence lines
    for (j in seq_along(p$ev)) {
      gt(cx, obs_mid - 0.040 - (j-1)*0.042,
         p$ev[[j]], fs=4.6, col=OI$black)
    }
  }
}

# ── Panel B icons (panel-local npc coordinates) ───────────────────────────────
draw_tree_icon <- function(cx, cy) {
  col <- OI$blue
  grid.lines(x=c(cx,cx), y=c(cy-0.030, cy-0.005),
             gp=gpar(col=col, lwd=1.6), default.units="npc")
  for (s in c(-1,1)) {
    grid.lines(x=c(cx, cx+s*0.033), y=c(cy-0.005, cy+0.022),
               gp=gpar(col=col, lwd=1.2), default.units="npc")
    grid.lines(x=c(cx+s*0.033, cx+s*0.048),
               y=c(cy+0.022, cy+0.040),
               gp=gpar(col=col, lwd=0.9), default.units="npc")
    grid.lines(x=c(cx+s*0.033, cx+s*0.016),
               y=c(cy+0.022, cy+0.040),
               gp=gpar(col=col, lwd=0.9), default.units="npc")
  }
}

draw_pfam_icon <- function(cx, cy) {
  col <- OI$blue
  grid.lines(x=c(cx-0.048, cx+0.048), y=c(cy+0.012, cy+0.012),
             gp=gpar(col=col, lwd=0.6, lty="dashed"), default.units="npc")
  grid.lines(x=c(cx-0.048, cx+0.048), y=c(cy-0.012, cy-0.012),
             gp=gpar(col=col, lwd=0.6, lty="dashed"), default.units="npc")
  for (k in -3:3) {
    grid.lines(x=c(cx+k*0.014, cx+k*0.014), y=c(cy-0.018, cy+0.018),
               gp=gpar(col=col, lwd=1.8), default.units="npc")
  }
}

draw_branch_icon <- function(cx, cy) {
  grid.lines(x=c(cx,cx), y=c(cy-0.030, cy+0.005),
             gp=gpar(col=OI$blue, lwd=1.6), default.units="npc")
  grid.lines(x=c(cx, cx+0.040), y=c(cy+0.005, cy+0.038),
             gp=gpar(col=OI$red, lwd=1.8), default.units="npc")
  grid.lines(x=c(cx, cx-0.030), y=c(cy+0.005, cy+0.038),
             gp=gpar(col=OI$blue, lwd=1.2), default.units="npc")
  gt(cx+0.055, cy+0.040, "*", fs=9, col=OI$red, face="bold")
}

# ══════════════════════════════════════════════════════════════════
# PANEL C  —  outcome summary + scattered-check tree
# ══════════════════════════════════════════════════════════════════
draw_panel_C <- function() {
  # Background
  rrect(0.50, 0.50, w=unit(0.96,"npc"), h=unit(0.96,"npc"),
        fill=fade(OI$green, 0.12), border=OI$green, lwd=0.9,
        r=unit(5,"pt"))

  gt(0.50, 0.93, "Sweet Trap is",
     fs=6.5, col=OI$black, face="plain")
  gt(0.50, 0.86, "WIDESPREAD",
     fs=9.5, col=COL_SUPPORTED, face="bold")
  gt(0.50, 0.79, "114 cases / 7 phyla",
     fs=5.0, col=OI$black)
  gt(0.50, 0.74, "56 species satisfy F1–F4",
     fs=5.0, col=OI$black)

  grid.lines(x=c(0.10,0.90), y=c(0.70,0.70),
             gp=gpar(col=OI$lgrey, lwd=0.6), default.units="npc")

  gt(0.50, 0.65, "but", fs=6.2, col=OI$grey, face="italic")

  gt(0.50, 0.58, "NOT UNIVERSAL",
     fs=8.5, col=COL_REFUTED, face="bold")
  gt(0.50, 0.52, "as a shared",
     fs=5.0, col=OI$black)
  gt(0.50, 0.47, "evolutionary trait",
     fs=5.0, col=OI$black)

  grid.lines(x=c(0.10,0.90), y=c(0.43,0.43),
             gp=gpar(col=OI$lgrey, lwd=0.6), default.units="npc")

  # Scattered tree cartoon
  draw_scattered_tree_C()
}

draw_scattered_tree_C <- function() {
  # Coordinates in panel C local npc
  cx   <- 0.50
  ybot <- 0.06
  ytop <- 0.41
  th   <- ytop - ybot

  # Trunk
  grid.lines(x=c(cx,cx), y=c(ybot, ybot+th*0.20),
             gp=gpar(col=OI$grey, lwd=1.4), default.units="npc")
  # Major branches
  brs <- list(
    c(cx, ybot+th*0.20, cx-0.24, ybot+th*0.58),
    c(cx, ybot+th*0.20, cx,      ybot+th*0.62),
    c(cx, ybot+th*0.20, cx+0.24, ybot+th*0.58)
  )
  for (b in brs)
    grid.lines(x=c(b[1],b[3]), y=c(b[2],b[4]),
               gp=gpar(col=OI$grey, lwd=1.0), default.units="npc")
  # Sub-branches & tips
  subs <- list(
    c(cx-0.24, ybot+th*0.58, cx-0.34, ytop-0.03),
    c(cx-0.24, ybot+th*0.58, cx-0.14, ytop-0.03),
    c(cx,      ybot+th*0.62, cx-0.08, ytop-0.03),
    c(cx,      ybot+th*0.62, cx+0.08, ytop-0.03),
    c(cx+0.24, ybot+th*0.58, cx+0.16, ytop-0.03),
    c(cx+0.24, ybot+th*0.58, cx+0.32, ytop-0.03)
  )
  tips_x  <- c(-0.34, -0.14, -0.08,  0.08,  0.16,  0.32)
  checks  <- c( TRUE,  FALSE, TRUE,  TRUE,  FALSE, TRUE)
  for (k in seq_along(subs)) {
    b <- subs[[k]]
    grid.lines(x=c(b[1],b[3]), y=c(b[2],b[4]),
               gp=gpar(col=OI$grey, lwd=0.8), default.units="npc")
    tx <- cx + tips_x[k]
    ty <- ytop + 0.008
    if (checks[k]) {
      draw_verdict_sym(tx, ty, "check", COL_SUPPORTED, sz=0.022)
    } else {
      grid.lines(x=c(tx-0.014, tx+0.014), y=c(ty, ty),
                 gp=gpar(col=OI$lgrey, lwd=1.5), default.units="npc")
    }
  }
  gt(cx, ybot+th*0.06,
     "(no clade clustering — signal absent)",
     fs=4.3, col=OI$grey, face="italic")
}

# ══════════════════════════════════════════════════════════════════
# MASTER DRAW
# ══════════════════════════════════════════════════════════════════
draw_fig1 <- function() {

  # Figure-level margins (npc)
  ml <- 0.010; mr <- 0.010
  mb <- 0.015; mt <- 0.042

  pw <- 1 - ml - mr   # total plot width
  ph <- 1 - mb - mt   # total plot height

  # Panel widths (proportional to mm widths 60:70:50)
  fA <- 60/180 * pw
  fB <- 70/180 * pw
  fC <- 50/180 * pw
  gap <- 0.008

  xA_l <- ml
  xA_r <- xA_l + fA
  xB_l <- xA_r + gap
  xB_r <- xB_l + fB
  xC_l <- xB_r + gap
  xC_r <- xC_l + fC

  ybot <- mb

  # Title
  grid.text("Figure 1  |  Pre-registered falsification framework",
            x=0.50, y=1 - mt*0.35,
            gp=gpar(fontsize=7.5, fontface="bold", col=OI$black),
            default.units="npc")

  # Panel labels  a  b  c
  for (info in list(
    list(xA_l + 0.004, "a"),
    list(xB_l + 0.004, "b"),
    list(xC_l + 0.004, "c")
  )) {
    grid.text(info[[2]], x=info[[1]], y=ybot+ph+0.005,
              just=c("left","bottom"),
              gp=gpar(fontsize=9, fontface="bold", col=OI$black),
              default.units="npc")
  }

  # Panel separators
  for (xd in c(xA_r+gap/2, xB_r+gap/2)) {
    grid.lines(x=c(xd,xd), y=c(ybot+0.02, ybot+ph-0.02),
               gp=gpar(col=OI$lgrey, lwd=0.5), default.units="npc")
  }

  # Panel A
  pushViewport(viewport(x=(xA_l+xA_r)/2, y=ybot+ph/2,
                        width=fA, height=ph))
  draw_panel_A()
  popViewport()

  # Panel B
  pushViewport(viewport(x=(xB_l+xB_r)/2, y=ybot+ph/2,
                        width=fB, height=ph))
  draw_panel_B()
  popViewport()

  # Panel C
  pushViewport(viewport(x=(xC_l+xC_r)/2, y=ybot+ph/2,
                        width=fC, height=ph))
  draw_panel_C()
  popViewport()
}

# ── Render ────────────────────────────────────────────────────────────────────
cairo_pdf(out_pdf, width=w_in, height=h_in, family="Helvetica")
grid.newpage(); draw_fig1(); invisible(dev.off())
message("PDF: ", out_pdf)

png(out_png, width=round(w_in*600), height=round(h_in*600),
    res=600, type="cairo", family="Helvetica")
grid.newpage(); draw_fig1(); invisible(dev.off())
message("PNG: ", out_png)

svg(out_svg, width=w_in, height=h_in, family="Helvetica")
grid.newpage(); draw_fig1(); invisible(dev.off())
message("SVG: ", out_svg)

message("Done. Fig1_falsification_framework rendered.")
