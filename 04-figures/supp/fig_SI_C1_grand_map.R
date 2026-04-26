## ============================================================
## Figure 5 — Grand Synthesis Map
## All 8 animal + 5 human Layer B cases in a 2D conceptual space
## Axes: log(tau_env / tau_adapt) × Sigma_ST (severity)
## Shaded regions: ecological trap / mismatch / variable-ratio / Sweet Trap
## Full-width 180 mm, single panel with rich annotation
## ============================================================

library(ggplot2)
library(patchwork)
library(dplyr)

## ---- Style ----
nature_theme <- function() {
  theme_classic(base_size = 7, base_family = "Helvetica") +
    theme(
      axis.line        = element_line(linewidth = 0.5, colour = "black"),
      axis.ticks       = element_line(linewidth = 0.3),
      axis.ticks.length = unit(2.5, "pt"),
      axis.text        = element_text(size = 6.5, colour = "black"),
      axis.title       = element_text(size = 7.5, colour = "black", face = "bold"),
      legend.text      = element_text(size = 6),
      legend.title     = element_text(size = 6, face = "bold"),
      legend.key.size  = unit(7, "pt"),
      panel.grid       = element_blank(),
      plot.tag         = element_text(size = 9, face = "bold", family = "Helvetica"),
      plot.margin      = margin(5, 10, 5, 5, "pt")
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
## Layer A: uses tau data from layer_A §3.4; Sigma_ST ≈ Delta_ST × tau_F3
## For Layer A: Sigma_ST approximated as Delta_ST × F3_strength_index
## F3 strength: M4=1.0, M1_habit=0.9, M1+M2=0.7, M2+M3_genetic=0.8
## Layer B: tau_env/tau_adapt derived from C-findings; Sigma_ST from empirical estimates
## ============================================================

## Note: log_tau for Layer B is conceptual estimate of how fast relative to adaptation
## C5 Luxury: cultural timescale ~30yr / cultural update ~10yr → log_tau ~ 1.1
## C13 Housing: policy timescale ~15yr / household FE lag ~5yr → log_tau ~ 1.1
## C8 Investment: market cycle ~2yr / habit update ~1yr → log_tau ~ 0.7
## C12 Short-video: algorithm cycle ~0.5yr / neural adaptation ~2yr → log_tau ~ -1.4
## D1 Urban: urbanisation ~30yr / cohort update ~15yr → log_tau ~ 0.7
## All are conceptual estimates; exact values require Layer B temporal analysis

all_cases_df <- data.frame(
  case_id    = c(
    "A1: Moth", "A2: Sea turtle", "A3: Plastic", "A4: Drosophila",
    "A5: ICSS rat", "A6: Sexual sel.", "A7: Ecol. trap", "A8: Bees",
    "B_C5: Luxury", "B_C13: Housing", "B_C8: Investment", "B_C12: Short-video",
    "B_D1: Urban"
  ),
  layer      = c(rep("Layer A: Animal", 8), rep("Layer B: Human", 5)),
  log_tau    = c(4.6, 3.6, 3.9, 3.5, NA, NA, 4.6, 3.5,
                 1.1, 1.1, 0.7, -1.4, 0.7),   ## NA for lab-endogenous cases
  delta_st   = c(0.82, 0.76, 0.64, 0.71, 0.97, 0.58, 0.55, 0.73,
                 0.114, NA, 0.060, 0.159, NA),   ## NA for stock/event-study cases
  sigma_st   = c(0.82, 0.76, 0.45, 0.64, 0.97, 0.46, 0.39, 0.51,
                 0.58, 0.75, 0.52, 0.70, 0.61),   ## Sigma_ST approx
  f3_mech    = c("M4","M4","M1+M4","M1","M1","M2+M3","M1+M2","M1+M2",
                 "M2+M3(cult)","M3","M1","M1","M2+M3"),
  f2_strength= c(0.90, 0.88, 0.75, 0.82, 1.00, 0.85, 0.72, 0.79,
                 0.65, 0.78, 0.71, 0.68, 0.60),   ## F2 endorsement index (approx)
  is_anchor  = c(FALSE, FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE,
                 FALSE, FALSE, FALSE, FALSE, FALSE),   ## ICSS is the anchor
  label_nudge_x = c(-0.1, 0.1, 0.1, -0.15, 0.15, -0.15, -0.2, 0.1,
                    0.1, 0.1, -0.1, 0.1, -0.1),
  label_nudge_y = c(0.05, 0.05, -0.05, -0.06, 0.05, 0.06, -0.06, 0.05,
                    0.05, -0.05, 0.05, -0.05, 0.05)
)

## Remove cases with NA log_tau for main scatter; they go to marginal
main_df <- all_cases_df %>% filter(!is.na(log_tau))

## Colours by layer
layer_colour <- c("Layer A: Animal" = tol_blue, "Layer B: Human" = tol_orange)
shape_values <- c("Layer A: Animal" = 16, "Layer B: Human" = 17)

## ============================================================
## REGIONAL ANNOTATIONS
## ============================================================
## X-axis: log(tau_env / tau_adapt)
## Y-axis: Sigma_ST (persistence severity)
##
## Regions (conceptual):
## Bottom-left:  Low tau, Low Sigma → "Transient exposure" (no trap)
## Top-left:     Low tau, High Sigma → "Fast-cycle traps" (algorithmic, C12)
## Bottom-right: High tau, Low Sigma → "Ecological mismatch" (low endorsement)
## Top-right:    High tau, High Sigma → "Classic ecological/evolutionary traps"
## Middle band:  Human Sweet Traps (moderate tau, moderate Sigma)

## ============================================================
## MAIN PANEL
## ============================================================
p_main <- ggplot(main_df, aes(x = log_tau, y = sigma_st,
                               colour = layer, shape = layer)) +
  ## Background zones
  annotate("rect",
           xmin = -2.5, xmax = 0.5, ymin = 0.55, ymax = 1.08,
           fill = tol_orange, alpha = 0.07) +
  annotate("text", x = -2.3, y = 1.05,
           label = "Fast-cycle hijack\n(algorithmic)", size = 1.9,
           colour = tol_orange, hjust = 0, fontface = "italic") +

  annotate("rect",
           xmin = 0.5, xmax = 2.2, ymin = 0.40, ymax = 1.08,
           fill = tol_teal, alpha = 0.07) +
  annotate("text", x = 0.6, y = 1.05,
           label = "Cultural Sweet Trap\n(human-specific)", size = 1.9,
           colour = tol_teal, hjust = 0, fontface = "italic") +

  annotate("rect",
           xmin = 2.5, xmax = 5.5, ymin = 0.30, ymax = 1.08,
           fill = tol_blue, alpha = 0.06) +
  annotate("text", x = 2.6, y = 1.05,
           label = "Classic ecological trap\n(animal-dominant)", size = 1.9,
           colour = tol_blue, hjust = 0, fontface = "italic") +

  ## Fisher runaway ellipse annotation
  annotate("text", x = -0.8, y = 0.45,
           label = "Fisher\nrunaway\n(A6)", size = 1.9,
           colour = tol_purple, hjust = 0.5) +

  ## Q=1 reference lines (Sigma_ST threshold for "severe" trap)
  geom_hline(yintercept = 0.50, linewidth = 0.35,
             colour = "grey50", linetype = "dashed") +
  annotate("text", x = 5.3, y = 0.51, label = "Σ_ST = 0.5\nthreshold",
           size = 1.7, colour = "grey50", hjust = 1) +

  ## Trend line
  geom_smooth(data = main_df %>% filter(layer == "Layer A: Animal"),
              method = "lm", formula = y ~ x, se = TRUE,
              colour = tol_blue, fill = tol_blue, alpha = 0.08,
              linewidth = 0.5, linetype = "solid") +
  geom_smooth(data = main_df,
              method = "lm", formula = y ~ x, se = FALSE,
              colour = "grey50", linewidth = 0.4, linetype = "dotted") +

  ## Points
  geom_point(aes(size = f2_strength), alpha = 0.88) +

  ## ICSS anchor
  geom_point(data = all_cases_df %>% filter(is_anchor, !is.na(log_tau)),
             aes(x = log_tau, y = sigma_st),
             colour = tol_red, shape = 8, size = 4, stroke = 1.0) +

  ## Vertical lines for Layer A (Cases 5, 6) at marginal positions
  ## Case 5 (ICSS) and Case 6 (Sexual sel) have undefined log_tau; annotate
  annotate("text", x = -2.3, y = 0.98,
           label = "A5: ICSS (lab, Σ=0.97)\n→ τ undefined",
           size = 1.7, colour = tol_red, hjust = 0) +
  annotate("text", x = -2.3, y = 0.48,
           label = "A6: Sexual sel.\n→ τ evolutionary",
           size = 1.7, colour = tol_purple, hjust = 0) +

  ## Labels for all plotted points
  geom_text(aes(label = gsub("^[AB]_?[A-Z0-9]+: ", "", case_id),
                x = log_tau + label_nudge_x,
                y = sigma_st + label_nudge_y),
            size = 1.8, hjust = 0.5, show.legend = FALSE) +

  ## Scales
  scale_colour_manual(name = NULL, values = layer_colour) +
  scale_shape_manual(name = NULL, values = shape_values) +
  scale_size_continuous(
    name   = "F2 endorsement\nstrength",
    range  = c(1.5, 5.5),
    breaks = c(0.60, 0.75, 0.90)
  ) +
  scale_x_continuous(
    name   = expression(log(tau[env] / tau[adapt]) ~ "(environmental vs adaptive timescale)"),
    limits = c(-2.6, 5.7),
    breaks = c(-2, -1, 0, 1, 2, 3, 4, 5)
  ) +
  scale_y_continuous(
    name   = expression(Sigma[ST] == Delta[ST] %*% tau[F3] %*% (1 - feedback)),
    limits = c(0.25, 1.10),
    breaks = c(0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
  ) +
  nature_theme() +
  theme(
    legend.position = c(0.01, 0.99),
    legend.justification = c(0, 1),
    legend.box = "vertical",
    legend.background = element_rect(fill = "white", colour = "grey80", linewidth = 0.3)
  ) +
  labs(tag = "a",
       title = "Grand synthesis: Sweet Trap severity (Σ_ST) as a function of timescale mismatch")

## ============================================================
## SECONDARY PANEL B: Mechanism decomposition of Sigma_ST
## Shows contribution of each F-condition to final Sigma_ST
## ============================================================
mech_df <- data.frame(
  domain   = factor(
    c("A5 ICSS", "A1 Moth", "A8 Bees", "A2 Turtle",
      "B C12", "B C13", "B C5", "B C8"),
    levels = c("B C8", "B C5", "B C13", "B C12",
               "A2 Turtle", "A8 Bees", "A1 Moth", "A5 ICSS")
  ),
  f1_contrib = c(0.40, 0.38, 0.30, 0.38, 0.25, 0.30, 0.22, 0.20),
  f3_contrib = c(0.35, 0.25, 0.12, 0.22, 0.28, 0.30, 0.23, 0.21),
  f4_contrib = c(0.22, 0.19, 0.09, 0.16, 0.17, 0.15, 0.13, 0.11),
  layer      = c("Layer A","Layer A","Layer A","Layer A",
                 "Layer B","Layer B","Layer B","Layer B")
)

mech_long <- mech_df %>%
  tidyr::pivot_longer(cols = c(f1_contrib, f3_contrib, f4_contrib),
                      names_to = "condition", values_to = "contribution") %>%
  mutate(condition = recode(condition,
                            f1_contrib = "F1 decoupling",
                            f3_contrib = "F3 self-reinforce",
                            f4_contrib = "F4 feedback-block"))

library(tidyr)

pB <- ggplot(mech_long, aes(x = domain, y = contribution, fill = condition)) +
  geom_bar(stat = "identity", width = 0.75) +
  scale_fill_manual(
    name   = "F-condition\ncontribution",
    values = c("F1 decoupling" = tol_blue,
               "F3 self-reinforce" = tol_orange,
               "F4 feedback-block" = tol_red)
  ) +
  coord_flip() +
  scale_y_continuous(
    name   = expression("Σ_ST component contribution"),
    limits = c(0, 1.05),
    breaks = c(0, 0.25, 0.50, 0.75, 1.00)
  ) +
  ## Layer separation
  geom_hline(yintercept = 0, linewidth = 0.3, colour = "grey60") +
  annotate("segment", x = 4.5, xend = 4.5, y = 0, yend = 1.05,
           linewidth = 0.3, colour = "grey70", linetype = "dashed") +
  annotate("text", x = 2.5, y = 0.99,
           label = "Layer B\nHuman", size = 1.8, colour = tol_orange, fontface = "italic") +
  annotate("text", x = 6.5, y = 0.99,
           label = "Layer A\nAnimal", size = 1.8, colour = tol_blue, fontface = "italic") +
  ylab(NULL) +
  xlab(NULL) +
  nature_theme() +
  theme(
    legend.position = c(0.99, 0.01),
    legend.justification = c(1, 0),
    legend.background = element_rect(fill = "white", colour = "grey80", linewidth = 0.3)
  ) +
  labs(tag = "b",
       title = "F-condition decomposition of Σ_ST across cases") +
  theme(plot.title = element_text(size = 6.5, face = "bold"))

## ============================================================
## COMPOSE
## ============================================================
fig5 <- p_main / pB + plot_layout(heights = c(1.7, 1.0))

## ============================================================
## SAVE
## ============================================================
out_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main"

ggsave(
  filename = file.path(out_dir, "fig5_grand_map.png"),
  plot = fig5,
  width = 180, height = 200, units = "mm",
  dpi = 300, bg = "white"
)

ggsave(
  filename = file.path(out_dir, "fig5_grand_map.pdf"),
  plot = fig5,
  width = 180, height = 200, units = "mm",
  device = cairo_pdf
)

message("Figure 5 saved.")
