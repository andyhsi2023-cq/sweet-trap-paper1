## ============================================================
## Figure 5 — Integrated Sweet Trap Evidence Architecture
## Sweet Trap v4 Paper 1 — §3.5 capstone synthesis figure
##
## Layout: four-quadrant with central diamond; L-shaped arrows
##   entering diamond from each quadrant's inner corner.
## Output: 180 × 130 mm, 600 dpi PNG / cairo PDF / SVG
## Palette: Okabe-Ito (colour-blind safe)
##
## Numbers verified against manuscript.md §3.5 on 2026-04-25
## ============================================================

library(grid)

base_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures"
out_pdf  <- file.path(base_dir, "Fig5_integrated_architecture.pdf")
out_png  <- file.path(base_dir, "Fig5_integrated_architecture.png")
out_svg  <- file.path(base_dir, "Fig5_integrated_architecture.svg")

w_in <- 180 / 25.4
h_in <- 130 / 25.4

# ── Okabe-Ito palette ──────────────────────────────────────────
OI <- list(
  blue   = "#0072B2",
  orange = "#E69F00",
  green  = "#009E73",
  purple = "#CC79A7",
  black  = "#000000",
  grey   = "#888888",
  lgrey  = "#DDDDDD"
)
fade <- function(col, a = 0.18) {
  v <- col2rgb(col)/255
  rgb(v[1]+(1-v[1])*(1-a), v[2]+(1-v[2])*(1-a), v[3]+(1-v[3])*(1-a))
}
BG <- list(
  blue   = fade(OI$blue),
  orange = fade(OI$orange),
  green  = fade(OI$green),
  purple = fade(OI$purple)
)

# ── Thin label badge (rounded rect + text) ────────────────────
badge <- function(x, y, label, col, fs = 5.5) {
  grid.roundrect(x=x, y=y,
                 width  = unit(nchar(label)*fs*0.62 + 6, "pt"),
                 height = unit(fs + 5, "pt"),
                 r = unit(2.5,"pt"),
                 gp = gpar(fill="white", col=col, lwd=1.0),
                 default.units="npc")
  grid.text(label, x=x, y=y,
            gp=gpar(fontsize=fs, col=col, fontface="bold"),
            default.units="npc")
}

draw_fig5 <- function() {

  pushViewport(viewport(0.5, 0.5, 1, 1))

  # ── Layout constants ──────────────────────────────────────────
  strip_h   <- 0.135
  diag_bot  <- strip_h + 0.008
  diag_top  <- 0.998

  # Center of diagram zone
  cx <- 0.500
  cy <- diag_bot + (diag_top - diag_bot) * 0.50

  # Diamond half-dimensions
  dw <- 0.100
  dh <- 0.072

  # Quadrant boundaries
  ql <- 0.008; qr <- 0.992
  qt <- diag_top; qb <- diag_bot
  mid_x <- cx; mid_y <- cy

  # Inner quadrant gap at center cross
  gap <- 0.006

  # Quadrant rectangle centres
  qcx_L  <- (ql + mid_x)/2;  qcx_R  <- (mid_x + qr)/2
  qcy_T  <- (mid_y + qt)/2;  qcy_B  <- (qb + mid_y)/2

  # ── Quadrant backgrounds ─────────────────────────────────────
  g <- gap/2
  # Q1 top-left (blue)
  grid.rect(x=qcx_L, y=qcy_T,
            width=mid_x-ql-g, height=qt-mid_y-g,
            gp=gpar(fill=BG$blue, col=OI$blue, lwd=0.8), default.units="npc")
  # Q2 top-right (orange)
  grid.rect(x=qcx_R, y=qcy_T,
            width=qr-mid_x-g, height=qt-mid_y-g,
            gp=gpar(fill=BG$orange, col=OI$orange, lwd=0.8), default.units="npc")
  # Q3 bottom-left (green)
  grid.rect(x=qcx_L, y=qcy_B,
            width=mid_x-ql-g, height=mid_y-qb-g,
            gp=gpar(fill=BG$green, col=OI$green, lwd=0.8), default.units="npc")
  # Q4 bottom-right (purple)
  grid.rect(x=qcx_R, y=qcy_B,
            width=qr-mid_x-g, height=mid_y-qb-g,
            gp=gpar(fill=BG$purple, col=OI$purple, lwd=0.8), default.units="npc")

  # ── Central diamond ───────────────────────────────────────────
  grid.polygon(x=c(cx, cx+dw, cx, cx-dw),
               y=c(cy+dh, cy, cy-dh, cy),
               gp=gpar(fill="white", col=OI$black, lwd=1.8), default.units="npc")

  grid.text("Sweet Trap",
            x=cx, y=cy+0.027,
            gp=gpar(fontface="bold", fontsize=8.8, col=OI$black), default.units="npc")
  grid.text(expression(Delta[ST]==U[perc]-E*"["*U[fit]*"|"*B*"]"),
            x=cx, y=cy+0.005,
            gp=gpar(fontsize=6.2, col=OI$black), default.units="npc")
  grid.text("Convergent vulnerability,",
            x=cx, y=cy-0.018,
            gp=gpar(fontsize=5.0, col=OI$grey), default.units="npc")
  grid.text("conserved architecture",
            x=cx, y=cy-0.031,
            gp=gpar(fontsize=5.0, col=OI$grey), default.units="npc")

  # ── Straight arrows: from midpoint of each quadrant inner edge ─
  # Each arrow runs from just outside the diamond toward the diamond vertex.
  # Start points on the inner quadrant boundary (the cross-centre lines)
  # Q1: comes from upper-left direction → enters diamond left vertex
  # Origin on the cross: (mid_x - 0.21, cy + 0.11) in diagram space
  # To keep it simple and clean: start from fixed offsets from diamond vertices

  arrowfrom <- function(ox, oy, tx, ty, col, gap_frac = 0.14) {
    # Draw arrow from (ox,oy) toward (tx,ty), stopping gap_frac before end
    xe <- ox + (tx - ox) * (1 - gap_frac)
    ye <- oy + (ty - oy) * (1 - gap_frac)
    grid.lines(x=c(ox,xe), y=c(oy,ye),
               gp=gpar(col=col, lwd=1.8),
               arrow=arrow(length=unit(5,"pt"), type="closed", ends="last"),
               default.units="npc")
  }

  # Arrow origins: placed in the clear zone of each quadrant (inner half)
  # Q1 (blue): from inner-left of Q1
  o1x <- mid_x - 0.200; o1y <- mid_y + 0.105
  # Q2 (orange): from inner-right of Q2
  o2x <- mid_x + 0.200; o2y <- mid_y + 0.105
  # Q3 (green): from inner-left of Q3
  o3x <- mid_x - 0.200; o3y <- mid_y - 0.105
  # Q4 (purple): from inner-right of Q4
  o4x <- mid_x + 0.200; o4y <- mid_y - 0.105

  arrowfrom(o1x, o1y, cx-dw, cy, OI$blue)
  arrowfrom(o2x, o2y, cx+dw, cy, OI$orange)
  arrowfrom(o3x, o3y, cx-dw, cy, OI$green)
  arrowfrom(o4x, o4y, cx+dw, cy, OI$purple)

  # Arrow method badges: on each arrow, at 50% position
  mid_arrow <- function(ox, oy, tx, ty, f=0.50) {
    c(ox + (tx-ox)*f, oy + (ty-oy)*f)
  }
  m1 <- mid_arrow(o1x, o1y, cx-dw, cy)
  m2 <- mid_arrow(o2x, o2y, cx+dw, cy)
  m3 <- mid_arrow(o3x, o3y, cx-dw, cy)
  m4 <- mid_arrow(o4x, o4y, cx+dw, cy)

  # Method badges: anchored near arrow midpoints,
  # placed in the outer (non-annotation) half of each quadrant
  # Q1/Q2 upper quadrants: badge below arrow (y-0.022)
  # Q3/Q4 lower quadrants: badge above arrow (y+0.022)
  bm1 <- mid_arrow(o1x, o1y, cx-dw, cy, f=0.50)
  bm2 <- mid_arrow(o2x, o2y, cx+dw, cy, f=0.50)
  bm3 <- mid_arrow(o3x, o3y, cx-dw, cy, f=0.50)
  bm4 <- mid_arrow(o4x, o4y, cx+dw, cy, f=0.50)

  # Q1/Q2: badges above-left/above-right of midpoint (in upper quadrant interior)
  # Q3/Q4: badges BELOW midpoint (in lower quadrant interior, away from Part labels)
  # Q1/Q2 badges: slightly below arrow midpoint (below the diagonal line)
  # Q3/Q4 badges: further below into lower quadrant
  badge(bm1[1]-0.018, bm1[2]-0.030, "Causality (MR)",              OI$blue,   5.2)
  badge(bm2[1]+0.025, bm2[2]-0.030, "Generality (phylogenetic)",    OI$orange, 5.2)
  badge(bm3[1]-0.018, bm3[2]-0.032, "Architecture (Pfam)",          OI$green,  5.2)
  badge(bm4[1]+0.025, bm4[2]-0.032, "Selection (branch-site ω>1)",  OI$purple, 5.2)

  # ── Part title labels — drawn AFTER badges so they render on top ──
  # Q1/Q2: top-left of upper quadrants
  # Q3/Q4: BOTTOM-left of lower quadrants (avoids mid_y badge zone)
  pxpad <- 0.020
  grid.text("Part 1 · Human",
            x=ql+pxpad, y=qt-0.018, just=c("left","top"),
            gp=gpar(fontface="bold", fontsize=7.5, col=OI$blue), default.units="npc")
  grid.text("Part 2 · Cross-species",
            x=mid_x+pxpad, y=qt-0.018, just=c("left","top"),
            gp=gpar(fontface="bold", fontsize=7.5, col=OI$orange), default.units="npc")
  # Q3/Q4 labels at top of lower quadrant but with white background patch for readability
  # White patch
  grid.rect(x=ql+0.086, y=mid_y-0.022, width=unit(80,"pt"), height=unit(12,"pt"),
            gp=gpar(fill="white", col=NA, alpha=0.85), default.units="npc")
  grid.text("Part 3 · Molecular",
            x=ql+pxpad, y=mid_y-0.018, just=c("left","top"),
            gp=gpar(fontface="bold", fontsize=7.5, col=OI$green), default.units="npc")
  grid.rect(x=mid_x+0.100, y=mid_y-0.022, width=unit(100,"pt"), height=unit(12,"pt"),
            gp=gpar(fill="white", col=NA, alpha=0.85), default.units="npc")
  grid.text("Part 4 · Genetic causality",
            x=mid_x+pxpad, y=mid_y-0.018, just=c("left","top"),
            gp=gpar(fontface="bold", fontsize=7.5, col=OI$purple), default.units="npc")

  # ── Icons ─────────────────────────────────────────────────────
  # Q1: three person silhouettes + MR badge
  ix1 <- ql + 0.095; iy1 <- qt - 0.090
  for (k in -1:1) {
    grid.circle(x=ix1+k*0.020, y=iy1+0.020, r=unit(4,"pt"),
                gp=gpar(fill=OI$blue,col=NA), default.units="npc")
    grid.lines(x=c(ix1+k*0.020-0.010, ix1+k*0.020+0.010),
               y=c(iy1-0.002, iy1-0.002),
               gp=gpar(col=OI$blue,lwd=3), default.units="npc")
  }
  badge(ix1+0.060, iy1+0.010, "MR", OI$blue, 5.8)

  # Q2: tree of life
  tx2 <- mid_x+0.110; ty2 <- qt-0.095
  grid.lines(x=c(tx2,tx2), y=c(ty2-0.035,ty2+0.008), gp=gpar(col=OI$orange,lwd=2.5), default.units="npc")
  for (s in c(-1,1)) {
    grid.lines(x=c(tx2,tx2+s*0.030), y=c(ty2+0.008,ty2+0.038), gp=gpar(col=OI$orange,lwd=2.0), default.units="npc")
    grid.lines(x=c(tx2+s*0.030,tx2+s*0.040), y=c(ty2+0.038,ty2+0.053), gp=gpar(col=OI$orange,lwd=1.5), default.units="npc")
    grid.lines(x=c(tx2+s*0.030,tx2+s*0.018), y=c(ty2+0.038,ty2+0.053), gp=gpar(col=OI$orange,lwd=1.5), default.units="npc")
  }

  # Q3: GPCR 7-helix membrane — placed in right side of Q3 (away from annotations)
  mx3 <- mid_x - 0.085; my3 <- qb+(mid_y-qb)*0.40
  grid.lines(x=c(mx3-0.045,mx3+0.045), y=c(my3+0.012,my3+0.012),
             gp=gpar(col=OI$green,lwd=0.9,lty="dashed"), default.units="npc")
  grid.lines(x=c(mx3-0.045,mx3+0.045), y=c(my3-0.012,my3-0.012),
             gp=gpar(col=OI$green,lwd=0.9,lty="dashed"), default.units="npc")
  for (k in -3:3) {
    grid.lines(x=c(mx3+k*0.013,mx3+k*0.013), y=c(my3-0.020,my3+0.020),
               gp=gpar(col=OI$green,lwd=2.2), default.units="npc")
  }
  grid.text("GPCR", x=mx3+0.062, y=my3,
            gp=gpar(fontsize=5.0,col=OI$green,fontface="bold"), default.units="npc")

  # Q4: DNA helix + omega — placed in right side of Q4
  dx4 <- mid_x+0.350; dy4 <- qb+(mid_y-qb)*0.40
  ns <- 10
  xseq <- seq(dx4-0.042,dx4+0.042,length.out=ns+1)
  ang1 <- seq(0,2*pi,length.out=ns+1)
  grid.lines(x=xseq, y=dy4+0.026*sin(ang1),     gp=gpar(col=OI$purple,lwd=2.0), default.units="npc")
  grid.lines(x=xseq, y=dy4+0.026*sin(ang1+pi),  gp=gpar(col=OI$purple,lwd=2.0), default.units="npc")
  for (k in seq(1,ns,2)) {
    grid.lines(x=c(xseq[k],xseq[k]),
               y=c(dy4+0.026*sin(ang1[k]), dy4+0.026*sin(ang1[k]+pi)),
               gp=gpar(col=OI$purple,lwd=0.9), default.units="npc")
  }
  grid.text(expression(omega*">1"), x=dx4+0.062, y=dy4,
            gp=gpar(fontsize=7.2,col=OI$purple,fontface="bold"), default.units="npc")

  # ── Annotation text blocks ────────────────────────────────────
  afs <- 5.3   # annotation fontsize
  lh  <- 0.033 # line height

  # Q1 — positioned in lower-left region, below icon
  a1x <- ql+0.020; a1y <- qt-0.265
  ann1 <- list(
    list("Trans-ancestry MR",                 OI$black, "plain"),
    list("4 reward pairs × 3 ancestries",     OI$black, "plain"),
    list("meta OR 1.12–1.41; p < 10⁻³",       OI$black, "plain"),
    list("4/4 directionally consistent",      OI$blue,  "bold")
  )
  for (k in seq_along(ann1)) {
    a <- ann1[[k]]
    grid.text(a[[1]], x=a1x, y=a1y-(k-1)*lh,
              just=c("left","top"), gp=gpar(fontsize=afs,col=a[[2]],fontface=a[[3]]),
              default.units="npc")
  }

  # Q2 — lower-right region of Q2
  a2x <- mid_x+0.020; a2y <- qt-0.265
  ann2 <- list(
    list("114 cases × 7 phyla",                    OI$black, "plain"),
    list("ΔST convergent (K=0.117, p=0.251)",      OI$black, "plain"),
    list("Within-Arthropoda K=1.45, p=0.007",      OI$orange,"bold")
  )
  for (k in seq_along(ann2)) {
    a <- ann2[[k]]
    grid.text(a[[1]], x=a2x, y=a2y-(k-1)*lh,
              just=c("left","top"), gp=gpar(fontsize=afs,col=a[[2]],fontface=a[[3]]),
              default.units="npc")
  }

  # Q3 — upper portion of Q3 (below Part label)
  a3x <- ql+0.020; a3y <- mid_y-0.056
  ann3 <- list(
    list("Tier-1 DRD: PF00001",                       OI$black, "plain"),
    list("100% / 3 phyla / n=25",                     OI$black, "plain"),
    list("Tier-2 Class-A GPCR PF00001",               OI$black, "plain"),
    list("4 phyla / n=39 | Jaccard(TAS1R,Gr)=0",      OI$green, "bold")
  )
  for (k in seq_along(ann3)) {
    a <- ann3[[k]]
    grid.text(a[[1]], x=a3x, y=a3y-(k-1)*lh,
              just=c("left","top"), gp=gpar(fontsize=afs,col=a[[2]],fontface=a[[3]]),
              default.units="npc")
  }

  # Q4 — upper portion of Q4 (pushed down below Selection badge)
  a4x <- mid_x+0.020; a4y <- mid_y-0.110
  ann4 <- list(
    list("Apis Gr clade branch-site",                 OI$black, "plain"),
    list("LRT=9.92, p=8.16×10⁻⁴, ω=36.2",           OI$purple,"bold"),
    list("5 informative negative clades",             OI$black, "plain"),
    list("Baldwin control LRT=55.90",                 OI$black, "plain")
  )
  for (k in seq_along(ann4)) {
    a <- ann4[[k]]
    grid.text(a[[1]], x=a4x, y=a4y-(k-1)*lh,
              just=c("left","top"), gp=gpar(fontsize=afs,col=a[[2]],fontface=a[[3]]),
              default.units="npc")
  }

  # ── Bottom strip: Problem → Mechanism → Consequence ───────────
  grid.lines(x=c(0.01,0.99), y=c(strip_h,strip_h),
             gp=gpar(col=OI$lgrey,lwd=0.8), default.units="npc")
  grid.rect(x=0.5, y=strip_h/2,
            width=0.99, height=strip_h,
            gp=gpar(fill="#F7F7F7",col=NA), default.units="npc")

  # Three-column layout within strip
  lbl_y <- strip_h * 0.80
  txt_y <- strip_h * 0.35

  cols3  <- c(OI$blue,  OI$green, OI$purple)
  labs3  <- c("Problem:", "Mechanism:", "Consequence:")
  xs3    <- c(0.030, 0.360, 0.695)
  texts3 <- c(
    "Reward cues decouple\nfrom fitness outcomes",
    "Evolutionary conservation of reward-receptor\narchitecture + clade-specific selection",
    "Systematic behavioral vulnerability\nacross animal kingdom (Table 4)"
  )
  for (i in 1:3) {
    grid.text(labs3[i],  x=xs3[i], y=lbl_y, just=c("left","center"),
              gp=gpar(fontface="bold",fontsize=6.2,col=cols3[i]), default.units="npc")
    grid.text(texts3[i], x=xs3[i], y=txt_y, just=c("left","center"),
              gp=gpar(fontsize=4.8,col=OI$black), default.units="npc")
  }
  # Arrows
  for (ax in c(0.238, 0.582)) {
    grid.lines(x=c(ax, ax+0.022), y=c(lbl_y,lbl_y),
               gp=gpar(col=OI$grey,lwd=1.0),
               arrow=arrow(length=unit(4,"pt"),type="open"),
               default.units="npc")
  }

  popViewport()
}

# ── Render all three formats ──────────────────────────────────
cairo_pdf(out_pdf, width=w_in, height=h_in, family="Helvetica")
draw_fig5(); dev.off()
message("PDF: ", out_pdf)

png(out_png, width=round(w_in*600), height=round(h_in*600),
    res=600, type="cairo", family="Helvetica")
draw_fig5(); dev.off()
message("PNG: ", out_png)

svg(out_svg, width=w_in, height=h_in, family="Helvetica")
draw_fig5(); dev.off()
message("SVG: ", out_svg)

message("Done.")
