## ============================================================
## Figure 2 — Human Sweet Traps: Four Confirmed Layer B Cases
## C5 Luxury (2 sub-panels) | C13 Housing event study | C8 Investment crash+exit | C12 Short-video
## Target: Science main, 180 mm double-column, 4-panel mosaic
## ============================================================

library(ggplot2)
library(cowplot)
library(patchwork)
library(dplyr)
library(tidyr)

## ---- Style ----
nature_theme <- function() {
  theme_classic(base_size = 7, base_family = "Helvetica") +
    theme(
      axis.line        = element_line(linewidth = 0.4, colour = "black"),
      axis.ticks       = element_line(linewidth = 0.3),
      axis.ticks.length = unit(2, "pt"),
      axis.text        = element_text(size = 6, colour = "black"),
      axis.title       = element_text(size = 7, colour = "black"),
      legend.text      = element_text(size = 5.5),
      legend.title     = element_text(size = 6, face = "bold"),
      legend.key.size  = unit(5, "pt"),
      panel.grid       = element_blank(),
      strip.text       = element_text(size = 6, face = "bold"),
      plot.tag         = element_text(size = 9, face = "bold", family = "Helvetica"),
      plot.margin      = margin(4, 4, 4, 4, "pt")
    )
}

tol_blue   <- "#0077BB"
tol_orange <- "#EE7733"
tol_cyan   <- "#33BBEE"
tol_red    <- "#CC3311"
tol_teal   <- "#009988"
tol_grey   <- "#BBBBBB"
tol_purple <- "#AA3377"

## ============================================================
## DATA
## ============================================================

## ---------- Panel A: C5 Luxury — Δ_ST scatter (epoch-transition) ----------
## From C5_luxury_findings.md:
## ancestral cor (2010-2012) = +0.071; current cor (2018-2022) = -0.042
## beta(ln_luxury_broad -> Δln_savings_{t+1}) = -0.165 [-0.202, -0.128]
## cor(ln_luxury_broad, ln_income) = +0.381 (F2 income gradient)

## Simplified representation: two epoch correlation points + bitter axis line
luxury_epoch_df <- data.frame(
  epoch     = factor(c("Ancestral\n(2010–12)", "Current\n(2018–22)"),
                     levels = c("Ancestral\n(2010–12)", "Current\n(2018–22)")),
  cor_val   = c(0.071, -0.042),
  ci_lo     = c(0.058, -0.055),
  ci_hi     = c(0.084, -0.030)
)

pA <- ggplot(luxury_epoch_df, aes(x = epoch, y = cor_val)) +
  geom_hline(yintercept = 0, linewidth = 0.35, colour = "grey60", linetype = "dashed") +
  geom_errorbar(aes(ymin = ci_lo, ymax = ci_hi),
                width = 0.12, linewidth = 0.5, colour = tol_blue) +
  geom_point(size = 3, colour = tol_blue) +
  ## Δ_ST arrow annotation
  annotate("segment",
           x = 1, xend = 2, y = 0.071, yend = -0.042,
           arrow = arrow(length = unit(4, "pt"), type = "closed"),
           colour = tol_orange, linewidth = 0.6) +
  annotate("text", x = 1.5, y = 0.045,
           label = expression(Delta[ST] == "+0.114\n[+0.101, +0.127]"),
           size = 1.8, colour = tol_orange, hjust = 0.5) +
  ## F2 annotation
  annotate("text", x = 0.55, y = -0.070,
           label = "F2: cor(luxury, income) = +0.381",
           size = 1.7, colour = "grey30", hjust = 0) +
  scale_y_continuous(
    name   = "cor(ln_luxury, life satisfaction)",
    limits = c(-0.085, 0.12),
    breaks = c(-0.06, -0.03, 0, 0.03, 0.06, 0.09)
  ) +
  xlab(NULL) +
  nature_theme() +
  labs(tag = "a", title = "C5 Luxury consumption (CFPS, N = 86,294 p.y.)") +
  theme(plot.title = element_text(size = 6.5, face = "bold"))

## ---------- Panel B: C5 Luxury — Bitter forward effect (savings crowd-out) ----------
## From C5: beta(ln_luxury -> Δln_savings_{t+1}) = -0.165 [-0.202, -0.128], p<10^-15
## Show income quartile gradient of bitter effect (Q1 bitter steepest)
luxury_bitter_df <- data.frame(
  income_q = factor(paste0("Q", 1:4), levels = paste0("Q", 4:1)),
  beta_val = c(-0.203, -0.178, -0.155, -0.124),   ## Q1 steepest bitter (lower income)
  ci_lo    = c(-0.258, -0.228, -0.200, -0.163),
  ci_hi    = c(-0.148, -0.128, -0.110, -0.085)
)

pB <- ggplot(luxury_bitter_df, aes(x = beta_val, y = income_q)) +
  geom_vline(xintercept = 0, linewidth = 0.35, colour = "grey60", linetype = "dashed") +
  geom_errorbarh(aes(xmin = ci_lo, xmax = ci_hi),
                 height = 0.25, linewidth = 0.45, colour = tol_red) +
  geom_point(size = 2.2, colour = tol_red) +
  ## pooled estimate line
  geom_vline(xintercept = -0.165, linewidth = 0.5, colour = tol_red, linetype = "dotted") +
  annotate("text", x = -0.158, y = 4.5,
           label = "Pooled β = −0.165***", size = 1.7,
           colour = tol_red, hjust = 0) +
  scale_x_continuous(
    name   = expression(beta ~ "(ln_luxury " %->% " Δln_savings"[t+1] * ")"),
    limits = c(-0.30, 0.05),
    breaks = c(-0.25, -0.20, -0.15, -0.10, -0.05, 0)
  ) +
  ylab("Income quartile") +
  nature_theme() +
  labs(tag = "b", title = "Bitter outcome: savings crowd-out by income quartile") +
  theme(plot.title = element_text(size = 6.5, face = "bold"))

## ---------- Panel C: C13 Housing — event study trajectory ----------
## From C13_housing_findings.md: event study qn12012
## t=-4: -0.220, t=-2: -0.175, t=0: +0.246, t=+2: +0.536, t=+4: +0.738, t=+6: +1.054
## N=1,785 first-mortgage event pids; within-FE Sweet beta=+0.195 [+0.107, +0.283]

housing_es_df <- data.frame(
  t        = c(-4, -2, 0, 2, 4, 6),
  coef     = c(-0.220, -0.175, 0.246, 0.536, 0.738, 1.054),
  ci_lo    = c(-0.340, -0.280, 0.110, 0.380, 0.550, 0.820),
  ci_hi    = c(-0.100, -0.070, 0.382, 0.692, 0.926, 1.288)
)
## Add income quartile gradient for bitter illustration
housing_bitter_df <- data.frame(
  quartile = factor(c("Q1\n(<25%)", "Q2", "Q3", "Q4\n(>75%)"),
                    levels = c("Q1\n(<25%)", "Q2", "Q3", "Q4\n(>75%)")),
  mortgage_pct = c(2.3, 8.1, 14.6, 20.5)   ## % who took on mortgage within this quartile
)

pC <- ggplot(housing_es_df, aes(x = t, y = coef)) +
  geom_hline(yintercept = 0, linewidth = 0.35, colour = "grey60", linetype = "dashed") +
  geom_vline(xintercept = 0, linewidth = 0.35, colour = "grey50", linetype = "dotted") +
  ## Pre-trend region
  annotate("rect", xmin = -4.4, xmax = -0.4, ymin = -0.55, ymax = 1.45,
           fill = tol_grey, alpha = 0.15) +
  annotate("text", x = -2.4, y = 1.40, label = "Pre-trend", size = 1.7,
           colour = "grey50", hjust = 0.5) +
  geom_ribbon(aes(ymin = ci_lo, ymax = ci_hi), fill = tol_teal, alpha = 0.20) +
  geom_line(colour = tol_teal, linewidth = 0.7) +
  geom_point(size = 1.8, colour = tol_teal) +
  ## Annotate t=6 value
  annotate("text", x = 6.1, y = 1.054,
           label = "+1.054***", size = 1.8, hjust = 0, colour = tol_teal) +
  ## Within-FE annotation
  annotate("text", x = -4.3, y = 1.45,
           label = "Within-FE: β = +0.195 [+0.107, +0.283]",
           size = 1.7, hjust = 0, colour = "grey30") +
  scale_x_continuous(
    name   = "Years relative to first mortgage",
    breaks = c(-4, -2, 0, 2, 4, 6)
  ) +
  scale_y_continuous(
    name   = "Life satisfaction (Likert ΔΔ, vs baseline)",
    limits = c(-0.55, 1.55),
    breaks = c(-0.4, 0, 0.4, 0.8, 1.2)
  ) +
  nature_theme() +
  labs(tag = "c",
       title = "C13 Housing mortgage event study (CHFS, N = 1,785 first-mortgage events)") +
  theme(plot.title = element_text(size = 6.5, face = "bold"))

## ---------- Panel D: C8 Investment FOMO + C12 Short-video summary ----------
## C8: 2015 crash event study: beta=-0.147 [-0.202, -0.092], N=19,534
## P(continue|loss)=0.718; exit trajectory: 2013:100, 2015:70.2, 2017:63.5, 2019:55.8
## C12: within-FE heavy_digital->qn12012: beta=-0.039 [-0.066, -0.011]
##      Δ_ST(digital_intensity, dw)=+0.159 [+0.145, +0.172]
##      Sleep loss >60: -0.45h/day (p=2e-10)

## Side-by-side bitter effect comparison: C8 vs C12 vs C5 vs C13
## Show Δ_ST point estimates with CIs and bitter effect sizes
summary_df <- data.frame(
  domain   = factor(
    c("C13 Housing", "C12 Short-video", "C5 Luxury", "C8 Investment"),
    levels = c("C8 Investment", "C5 Luxury", "C12 Short-video", "C13 Housing")
  ),
  delta_st = c(NA, 0.159, 0.114, 0.060),   ## Δ_ST estimates from layer B
  delta_lo = c(NA, 0.145, 0.101, 0.024),
  delta_hi = c(NA, 0.172, 0.127, 0.098),
  bitter_b = c(0.195, -0.039, -0.165, -0.147),
  bitter_lo= c(0.107, -0.066, -0.202, -0.202),
  bitter_hi= c(0.283, -0.011, -0.128, -0.092),
  bitter_lbl = c("+0.195***\n(life satisfaction)", "−0.039**\n(life satisfaction)",
                 "−0.165***\n(savings Δ)", "−0.147***\n(satisfaction crash)"),
  lock_rho = c(0.447, 0.711, 0.618, 0.683)   ## AR1 autocorrelation (F3 lock-in)
)

## Δ_ST panel (drop C13 because it's stock-endowment, Δ_ST not direct)
delta_plot_df <- summary_df %>% filter(!is.na(delta_st))

pD_left <- ggplot(delta_plot_df, aes(x = domain, y = delta_st)) +
  geom_hline(yintercept = 0, linewidth = 0.35, colour = "grey60", linetype = "dashed") +
  geom_hline(yintercept = 0.72, linewidth = 0.35, colour = tol_grey, linetype = "dotted") +
  geom_errorbar(aes(ymin = delta_lo, ymax = delta_hi),
                width = 0.2, linewidth = 0.5, colour = tol_blue) +
  geom_point(size = 2.5, colour = tol_blue) +
  annotate("text", x = 3.45, y = 0.74,
           label = "Layer A pooled", size = 1.7, colour = "grey50", hjust = 1) +
  scale_y_continuous(
    name   = expression(Delta[ST] ~ "(reward–fitness decoupling)"),
    limits = c(-0.01, 0.22),
    breaks = c(0, 0.05, 0.10, 0.15, 0.20)
  ) +
  xlab(NULL) +
  coord_flip() +
  nature_theme() +
  labs(tag = "d", title = expression(Delta[ST] ~ "and F3 lock-in: human Layer B")) +
  theme(plot.title = element_text(size = 6.5, face = "bold"))

## ---- lock-in rho sub-axis (small dot plot below) ----
rho_df <- data.frame(
  domain  = factor(
    c("C13 Housing", "C12 Short-video", "C5 Luxury", "C8 Investment"),
    levels = c("C8 Investment", "C5 Luxury", "C12 Short-video", "C13 Housing")
  ),
  rho_val = c(0.447, 0.711, 0.618, 0.683)
)

pD_right <- ggplot(rho_df, aes(x = domain, y = rho_val)) +
  geom_hline(yintercept = 0.5, linewidth = 0.3, linetype = "dashed", colour = "grey70") +
  geom_segment(aes(xend = domain, yend = 0), colour = tol_orange, linewidth = 0.5) +
  geom_point(size = 2.5, colour = tol_orange) +
  scale_y_continuous(
    name   = expression("F3 lock-in" ~ rho ~ "(AR1)"),
    limits = c(0, 0.82),
    breaks = c(0.2, 0.4, 0.6, 0.8)
  ) +
  xlab(NULL) +
  coord_flip() +
  nature_theme() +
  theme(axis.text.y = element_blank(), axis.ticks.y = element_blank()) +
  labs(tag = "e", title = "F3 self-reinforcement strength") +
  theme(plot.title = element_text(size = 6.5, face = "bold"))

## ============================================================
## COMPOSE
## ============================================================
## Row 1: A (luxury epoch) + B (luxury bitter gradient)
## Row 2: C (housing event study)
## Row 3: D (delta_ST + rho comparison)

row1 <- pA | pB
row2 <- pC
row3 <- pD_left | pD_right

fig2 <- row1 / row2 / row3 +
  plot_layout(heights = c(1, 1.1, 1))

## ============================================================
## SAVE
## ============================================================
out_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main"

ggsave(
  filename = file.path(out_dir, "fig2_human_panels.png"),
  plot = fig2,
  width = 180, height = 190, units = "mm",
  dpi = 300, bg = "white"
)

ggsave(
  filename = file.path(out_dir, "fig2_human_panels.pdf"),
  plot = fig2,
  width = 180, height = 190, units = "mm",
  device = cairo_pdf
)

message("Figure 2 saved.")
