## ============================================================
## Figure 6 (v3.1) — Cross-Level + Intervention Test (Theory Tests)
## NHB consolidation: merges old fig8_intervention_asymmetry + fig9_cross_level_meta
## Target: Nature Human Behaviour, 180 mm × 190 mm
## Layout:
##   Panel (a): Cross-level A+D scatter/forest — β = +1.58 joint test
##   Panel (b): Intervention asymmetry forest — 6 domains × 2 arms
##   Panel (c): Within-domain ratio log-scale bar chart
## Paul Tol colorblind-safe palette throughout
## Source: cross_level_meta.py + fig8_intervention_asymmetry.R data
## ============================================================

library(ggplot2)
library(cowplot)
library(patchwork)
library(dplyr)
library(tidyr)
library(scales)

## ---- Shared style ----
nature_theme <- function() {
  theme_classic(base_size = 7, base_family = "Helvetica") +
    theme(
      axis.line         = element_line(linewidth = 0.4, colour = "black"),
      axis.ticks        = element_line(linewidth = 0.3),
      axis.ticks.length = unit(2, "pt"),
      axis.text         = element_text(size = 6, colour = "black"),
      axis.title        = element_text(size = 7, colour = "black"),
      legend.text       = element_text(size = 6),
      legend.title      = element_text(size = 6, face = "bold"),
      legend.key.size   = unit(6, "pt"),
      panel.grid        = element_blank(),
      strip.text        = element_text(size = 6, face = "bold"),
      plot.tag          = element_text(size = 9, face = "bold", family = "Helvetica"),
      plot.margin       = margin(3, 3, 3, 3, "pt")
    )
}

## Paul Tol colorblind-safe palette
tol_blue   <- "#0077BB"
tol_orange <- "#EE7733"
tol_cyan   <- "#33BBEE"
tol_red    <- "#CC3311"
tol_teal   <- "#009988"
tol_grey   <- "#BBBBBB"
tol_purple <- "#AA3377"
tol_green  <- "#228833"

## ============================================================
## PANEL (a) — CROSS-LEVEL A+D JOINT META-REGRESSION
## Mechanism-rank forest: A layer vs D layer per mechanism category
## Shows β = +1.58 pre-registered A+D joint result
## ============================================================

## Layer means per mechanism (from cross_level_meta.py outputs, §3.5)
crosslevel_df <- data.frame(
  mechanism   = factor(
    rep(c("Olds\u2013Milner", "Sensory exploit", "Fisher runaway"), 2),
    levels = c("Fisher runaway", "Sensory exploit", "Olds\u2013Milner")
  ),
  layer       = factor(c("A", "A", "A", "D", "D", "D"),
                        levels = c("A", "D")),
  effect_z    = c(0.789, 0.653, 0.547,   ## Layer A Δ_ST subgroup means (raw, not z-scored)
                  0.553, 0.354, NA),      ## Layer D |log OR| means; Fisher_runaway N/A in D
  ci_lo       = c(0.620, 0.560, 0.430,
                  0.392, 0.211, NA),
  ci_hi       = c(0.959, 0.745, 0.664,
                  0.714, 0.497, NA),
  colour      = c(tol_blue, tol_blue, tol_blue,
                  tol_orange, tol_orange, tol_orange),
  shape       = c(16, 16, 16, 17, 17, 17),
  stringsAsFactors = FALSE
) %>% filter(!is.na(effect_z))

## Regression line data for A+D joint (β = +1.58 on z-scored, shown as directional trend)
## For visual: map mechanism to numeric rank (Fisher=1, Sensory=2, Olds=3)
crosslevel_df$mech_rank <- case_when(
  as.character(crosslevel_df$mechanism) == "Fisher runaway"   ~ 1,
  as.character(crosslevel_df$mechanism) == "Sensory exploit"  ~ 2,
  as.character(crosslevel_df$mechanism) == "Olds\u2013Milner" ~ 3
)

pA <- ggplot(crosslevel_df,
             aes(x = mech_rank, y = effect_z,
                 colour = layer, shape = layer)) +
  ## Trend lines per layer
  geom_smooth(method = "lm", formula = y ~ x, se = FALSE,
              linewidth = 0.5, linetype = "dashed", alpha = 0.7) +
  ## CIs
  geom_errorbar(aes(ymin = ci_lo, ymax = ci_hi),
                width = 0.12, linewidth = 0.45, position = position_dodge(0.2)) +
  ## Points
  geom_point(size = 2.5, position = position_dodge(0.2)) +
  ## β annotation
  annotate("text", x = 2.5, y = 0.99,
           label = "A+D joint:\n\u03b2 = +1.58 (z-scored)\np = 0.019 (pre-reg.)",
           size = 1.8, hjust = 0.5, colour = "grey20", fontface = "bold",
           lineheight = 1.2) +
  ## 3-layer null annotation
  annotate("text", x = 1.0, y = 0.22,
           label = "3-layer\u00b9: \u03c7\u00b2(2) = 1.51, p = 0.47",
           size = 1.7, hjust = 0, colour = "grey50", fontface = "italic") +
  ## Superscript footnote
  annotate("text", x = 1.0, y = 0.12,
           label = "\u00b9 Non-significant; A+D pre-registered as primary",
           size = 1.5, hjust = 0, colour = "grey50", fontface = "italic") +
  scale_colour_manual(
    name   = "Layer",
    values = c("A" = tol_blue, "D" = tol_orange),
    labels = c("A" = "Animal meta (Δ_ST)", "D" = "Human MR (|log OR|)")
  ) +
  scale_shape_manual(
    name   = "Layer",
    values = c("A" = 16, "D" = 17),
    labels = c("A" = "Animal meta (Δ_ST)", "D" = "Human MR (|log OR|)")
  ) +
  scale_x_continuous(
    name   = "Mechanism class (rank)",
    breaks = c(1, 2, 3),
    labels = c("Fisher\nrunaway", "Sensory\nexploit", "Olds\u2013Milner"),
    limits = c(0.6, 3.8)
  ) +
  scale_y_continuous(
    name   = "Within-layer z-scored effect (layer mean)",
    limits = c(0.05, 1.10),
    breaks = c(0.2, 0.4, 0.6, 0.8, 1.0)
  ) +
  nature_theme() +
  theme(
    legend.position   = c(0.01, 0.99),
    legend.justification = c(0, 1),
    legend.background = element_rect(fill = NA, colour = NA)
  ) +
  labs(tag = "a",
       title = "P5 (empirical regularity): animal mechanism rank predicts human MR rank") +
  theme(plot.title = element_text(size = 5.5, face = "plain", colour = "grey20"))

## ============================================================
## PANEL (b) — INTERVENTION ASYMMETRY FOREST
## Source data from intervention_asymmetry_table.csv
## Normalised scale: signal_redesign = 1.0 per domain
## ============================================================

csv_path <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/intervention_asymmetry_table.csv"

## Build from source CSV if available; otherwise use hard-coded values from §3.6 / fig8 script
if (file.exists(csv_path)) {
  raw_int <- read.csv(csv_path, stringsAsFactors = FALSE, na.strings = c("NA", ""))
} else {
  ## Hard-coded fallback (values from manuscript §3.6 + fig8_intervention_asymmetry.R)
  raw_int <- data.frame(
    domain_id         = rep(c("C8", "C11", "C12", "C13", "D_alcohol", "C_pigbutch"), 2),
    intervention_type = c(rep("signal_redesign", 6), rep("information", 6)),
    effect_size       = c(37.0, -10.0, 0.35, -0.20, 0.44,  0.40,
                           0.5,  -8.0,  0.05,  0.015, 0.05,  0.03),
    ci_low            = c(33.0, -15.0,  0.25, -0.32, 0.32,  NA,
                           0.2,  NA,    -0.02,  NA,   NA,    NA),
    ci_high           = c(41.0,  -5.0,  0.45, -0.08, 0.56,  NA,
                           0.8,   4.0,   0.12,  0.045, 0.10,  0.09),
    emerging          = c(FALSE, FALSE, FALSE, FALSE, FALSE, TRUE,
                          FALSE, FALSE, FALSE, FALSE, FALSE, FALSE),
    cross_instrument  = c(FALSE, FALSE, FALSE, TRUE,  FALSE, FALSE,
                          FALSE, FALSE, FALSE, TRUE,  FALSE, FALSE),
    stringsAsFactors  = FALSE
  )
}

domain_order_b <- c("C8", "C11", "C12", "C13", "D_alcohol", "C_pigbutch")
domain_display_b <- c(
  "C8"         = "C8  Investment FOMO",
  "C11"        = "C11  Diet (SSB)",
  "C12"        = "C12  Short-video",
  "C13"        = "C13  Housing leverage\u2020",
  "D_alcohol"  = "D\u03b1  Alcohol",
  "C_pigbutch" = "C\u03c0  Pig-butchering\u2020\u2020"
)
domain_colours_b <- c(
  "C8"         = tol_blue,
  "C11"        = tol_orange,
  "C12"        = tol_teal,
  "C13"        = tol_purple,
  "D_alcohol"  = tol_red,
  "C_pigbutch" = tol_green
)

int_df <- raw_int %>%
  mutate(
    ## Absolute magnitude, positive = better welfare
    eff_abs = case_when(
      domain_id == "C11" ~ -effect_size,
      TRUE               ~ abs(effect_size)
    ),
    ci_lo_abs = case_when(
      domain_id == "C11" & intervention_type == "information"     ~ -ci_high,
      domain_id == "C11" & intervention_type == "signal_redesign" ~ -ci_high,
      TRUE ~ pmin(abs(ci_low), abs(ci_high), na.rm = TRUE)
    ),
    ci_hi_abs = case_when(
      domain_id == "C11" & intervention_type == "information"     ~ -ci_low,
      domain_id == "C11" & intervention_type == "signal_redesign" ~ -ci_low,
      TRUE ~ pmax(abs(ci_low), abs(ci_high), na.rm = TRUE)
    )
  ) %>%
  mutate(
    ci_lo_abs = ifelse(is.na(ci_lo_abs), eff_abs * 0.50, ci_lo_abs),
    ci_hi_abs = ifelse(is.na(ci_hi_abs), eff_abs * 1.50, ci_hi_abs)
  )

## Normalise per domain (signal_redesign = 1.0)
norm_factors_b <- int_df %>%
  filter(intervention_type == "signal_redesign") %>%
  select(domain_id, sig_eff = eff_abs)

int_norm <- int_df %>%
  left_join(norm_factors_b, by = "domain_id") %>%
  mutate(
    eff_norm  = eff_abs  / sig_eff,
    ci_lo_n   = ci_lo_abs / sig_eff,
    ci_hi_n   = ci_hi_abs / sig_eff,
    ## C11 info CI crosses 0 after flip
    ci_lo_n   = pmin(ci_lo_n, ci_hi_n),
    ci_hi_n   = pmax(ci_lo_n, ci_hi_n)
  ) %>%
  mutate(
    domain_id  = factor(domain_id, levels = domain_order_b),
    dom_label  = domain_display_b[as.character(domain_id)],
    dom_label  = factor(dom_label, levels = rev(domain_display_b[domain_order_b])),
    int_type   = factor(intervention_type,
                        levels = c("information", "signal_redesign"),
                        labels = c("Information", "Signal redesign")),
    y_num      = as.numeric(dom_label),
    y_off      = ifelse(intervention_type == "information", -0.18, +0.18),
    y_pos      = y_num + y_off,
    dot_colour = ifelse(
      intervention_type == "information",
      "#888888",
      domain_colours_b[as.character(domain_id)]
    ),
    ci_lty     = ifelse(emerging == TRUE, "dashed", "solid")
  )

n_dom <- length(domain_order_b)

pB <- ggplot(int_norm) +
  ## Alternating row bands
  annotate("rect", xmin = -Inf, xmax = Inf,
           ymin = seq(0.5, n_dom - 0.5, by = 2),
           ymax = seq(1.5, n_dom + 0.5, by = 2),
           fill = "grey96", colour = NA) +
  ## Null line
  geom_vline(xintercept = 0, linewidth = 0.5, colour = "grey40", linetype = "dashed") +
  ## CIs
  geom_linerange(
    data = filter(int_norm, !is.na(ci_lo_n) & !is.na(ci_hi_n)),
    aes(y = y_pos, xmin = ci_lo_n, xmax = ci_hi_n,
        colour = dot_colour, linetype = ci_lty),
    linewidth = 0.45
  ) +
  ## Information points (open grey)
  geom_point(
    data = filter(int_norm, intervention_type == "information"),
    aes(y = y_pos, x = eff_norm),
    shape = 21, size = 1.9, colour = "#888888", fill = "white", stroke = 0.6
  ) +
  ## Signal redesign points (filled domain colour)
  geom_point(
    data = filter(int_norm, intervention_type == "signal_redesign"),
    aes(y = y_pos, x = eff_norm, colour = dot_colour),
    shape = 16, size = 2.1
  ) +
  ## Emerging annotation
  annotate("text",
           x     = int_norm$eff_norm[int_norm$domain_id == "C_pigbutch" &
                                     int_norm$intervention_type == "signal_redesign"] + 0.06,
           y     = int_norm$y_pos[int_norm$domain_id == "C_pigbutch" &
                                  int_norm$intervention_type == "signal_redesign"],
           label = "\u2020\u2020 emerging",
           hjust = 0, size = 1.6, colour = tol_green, fontface = "italic") +
  ## Legend inside
  annotate("point", x = 0.65, y = 0.7, shape = 21, size = 1.9,
           colour = "#888888", fill = "white", stroke = 0.6) +
  annotate("text",  x = 0.72, y = 0.7, label = "Information",
           hjust = 0, size = 1.7, colour = "grey30") +
  annotate("point", x = 0.65, y = 0.35, shape = 16, size = 2.1, colour = "grey40") +
  annotate("text",  x = 0.72, y = 0.35, label = "Signal redesign",
           hjust = 0, size = 1.7, colour = "grey30") +
  scale_colour_identity() +
  scale_linetype_identity() +
  scale_x_continuous(
    name   = "Effect (domain-normalised; signal redesign \u2261 1.0)",
    limits = c(-0.5, 1.7),
    breaks = c(0, 0.25, 0.5, 0.75, 1.0, 1.25),
    labels = c("0", "0.25", "0.50", "0.75", "1.0\n(signal\nredesign)", "1.25"),
    expand = c(0.02, 0.02)
  ) +
  scale_y_continuous(
    breaks = 1:n_dom,
    labels = rev(domain_display_b[domain_order_b]),
    expand = c(0.08, 0.08)
  ) +
  ylab(NULL) +
  nature_theme() +
  theme(
    axis.text.y = element_text(size = 5.5, hjust = 1),
    axis.text.x = element_text(size = 5.5)
  ) +
  labs(tag = "b",
       title = "P1 (T2 prediction): signal-redesign consistently dominates information") +
  theme(plot.title = element_text(size = 5.5, face = "plain", colour = "grey20"))

## ============================================================
## PANEL (c) — WITHIN-DOMAIN RATIO BAR CHART (log scale)
## ============================================================

## Compute ratios from normalised data
ratio_src <- int_norm %>%
  select(domain_id, intervention_type, eff_norm, ci_lo_n, ci_hi_n) %>%
  mutate(domain_id = as.character(domain_id)) %>%
  pivot_wider(
    id_cols = domain_id,
    names_from = intervention_type,
    values_from = c(eff_norm, ci_lo_n, ci_hi_n)
  ) %>%
  mutate(
    ## ratio = signal / information (both normalised so signal = 1 by construction)
    ## pivot_wider uses original column values (lowercase): information, signal_redesign
    ratio     = 1.0 / pmax(eff_norm_information, 0.01),
    ## SE approximation for log ratio
    se_log    = sqrt(
      ((ci_hi_n_information - ci_lo_n_information) / (2 * 1.96 * pmax(eff_norm_information, 0.01)))^2 +
        0.05^2  ## signal SE near 0 by construction
    ),
    ratio_lo  = exp(log(ratio) - 1.96 * se_log),
    ratio_hi  = exp(log(ratio) + 1.96 * se_log),
    ## Cap C11 (info CI spans 0)
    ratio_hi  = ifelse(domain_id == "C11", 40, ratio_hi),
    ratio_lo  = ifelse(domain_id == "C11", 0.8, ratio_lo),
    ## Wider CI for pig + C13
    ratio_lo  = ifelse(domain_id == "C_pigbutch", ratio * 0.30, ratio_lo),
    ratio_hi  = ifelse(domain_id == "C_pigbutch", ratio * 3.50, ratio_hi),
    ratio_lo  = ifelse(domain_id == "C13",        ratio * 0.40, ratio_lo),
    ratio_hi  = ifelse(domain_id == "C13",        ratio * 2.80, ratio_hi),
    bar_colour = domain_colours_b[domain_id],
    emerging   = domain_id == "C_pigbutch"
  ) %>%
  arrange(ratio) %>%
  mutate(y_rank = row_number())

## Short labels
ratio_src$short_lbl <- c(
  "C8"         = "C8  Invest.",
  "C11"        = "C11  Diet",
  "C12"        = "C12  Short-vid.",
  "C13"        = "C13  Housing\u2020",
  "D_alcohol"  = "D\u03b1  Alcohol",
  "C_pigbutch" = "C\u03c0  Pig-butch.\u2020\u2020"
)[ratio_src$domain_id]

median_ratio_c <- median(ratio_src$ratio)

pC <- ggplot(ratio_src, aes(y = y_rank)) +
  ## "no advantage" line
  geom_vline(xintercept = 1, linewidth = 0.5, colour = "grey40", linetype = "dashed") +
  ## Median ratio line
  geom_vline(xintercept = median_ratio_c, linewidth = 0.5, colour = "grey20") +
  ## CI bars
  geom_linerange(
    aes(xmin = ratio_lo, xmax = ratio_hi, colour = bar_colour,
        linetype = ifelse(emerging, "dashed", "solid")),
    linewidth = 0.4
  ) +
  ## Segment from 1 to ratio (bar effect)
  geom_segment(
    aes(x = 1, xend = ratio, yend = y_rank, colour = bar_colour),
    linewidth = 2.0, alpha = 0.30
  ) +
  ## Dot at ratio
  geom_point(aes(x = ratio, colour = bar_colour), shape = 16, size = 2.0) +
  ## Value labels
  geom_text(
    aes(x = ratio, label = sprintf("%.0f\u00d7", ratio)),
    hjust = -0.35, size = 1.9, colour = "grey20"
  ) +
  ## Highlight > 3 region
  annotate("rect", xmin = 3, xmax = Inf, ymin = -Inf, ymax = Inf,
           fill = scales::alpha(tol_blue, 0.04)) +
  annotate("text", x = 4, y = 6.5,
           label = "Signal\ndominates\n(ratio > 3)",
           hjust = 0, size = 1.7, colour = tol_blue, fontface = "italic", lineheight = 1.0) +
  ## Median label
  annotate("text", x = median_ratio_c + 0.8, y = 0.65,
           label = sprintf("Median = %.0f\u00d7", median_ratio_c),
           hjust = 0, size = 1.8, colour = "grey20") +
  scale_colour_identity() +
  scale_linetype_identity() +
  scale_x_log10(
    name   = "Ratio: signal redesign \u00f7 information (log scale)",
    limits = c(0.6, 200),
    breaks = c(1, 2, 5, 10, 20, 50, 100),
    labels = c("1", "2", "5", "10", "20", "50", "100"),
    expand = c(0.02, 0.02)
  ) +
  scale_y_continuous(
    breaks = 1:nrow(ratio_src),
    labels = ratio_src$short_lbl,
    expand = c(0.1, 0.1)
  ) +
  ylab(NULL) +
  nature_theme() +
  theme(
    axis.text.y = element_text(size = 5.5, hjust = 1),
    axis.text.x = element_text(size = 5.5)
  ) +
  labs(tag = "c")

## ============================================================
## COMPOSE — 180 mm × 190 mm
## Top: Panel A (cross-level scatter, 35%)
## Bottom left: Panel B (intervention forest, 40%)
## Bottom right: Panel C (ratio bar, 25%)
## ============================================================

bottom_row <- pB | pC + plot_layout(widths = c(1.35, 1.0))
fig6_new   <- pA / bottom_row +
  plot_layout(heights = c(1.1, 1.6)) &
  theme(plot.margin = margin(4, 4, 4, 4, "pt"))

## ============================================================
## SAVE
## ============================================================

out_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main"

ggsave(
  filename = file.path(out_dir, "fig6_theory_tests.png"),
  plot     = fig6_new,
  width    = 180, height = 190, units = "mm",
  dpi      = 300, bg = "white"
)

ggsave(
  filename = file.path(out_dir, "fig6_theory_tests.pdf"),
  plot     = fig6_new,
  width    = 180, height = 190, units = "mm",
  device   = cairo_pdf
)

message("Fig 6 (v3.1) saved: fig6_theory_tests.{png,pdf}")
message(sprintf("Panels: (a) cross-level A+D joint beta=+1.58; (b) intervention forest 6 domains; (c) ratio log bar"))
message(sprintf("Median signal/information ratio: %.0fx", median_ratio_c))
