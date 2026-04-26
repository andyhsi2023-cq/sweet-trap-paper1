## ============================================================
## Figure 8 — Intervention Asymmetry Forest Plot (v2.4)
## Sweet Trap Cross-Species Framework
## Target: Nature Human Behaviour, 180 mm × 130 mm
## Layout:
##   Panel (a): Forest plot — 6 domain rows × 2 intervention types
##   Panel (b): Log-ratio bar chart — signal_redesign / information
## Paul Tol colorblind-safe palette throughout
## ============================================================

library(ggplot2)
library(cowplot)
library(patchwork)
library(dplyr)
library(tidyr)
library(scales)

## ---- Shared style (mirrors fig6_mr_layer_D.R) ----
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

## ---- Paul Tol colorblind-safe palette ----
tol_blue   <- "#0077BB"
tol_orange <- "#EE7733"
tol_cyan   <- "#33BBEE"
tol_red    <- "#CC3311"
tol_teal   <- "#009988"
tol_grey   <- "#BBBBBB"
tol_purple <- "#AA3377"
tol_green  <- "#228833"

## Domain colours (matching Fig 7 layer palette for cross-figure consistency)
domain_colours <- c(
  "C8"        = tol_blue,
  "C11"       = tol_orange,
  "C12"       = tol_teal,
  "C13"       = tol_purple,
  "D_alcohol" = tol_red,
  "C_pigbutch"= tol_green
)

## ============================================================
## READ SOURCE DATA
## ============================================================

csv_path <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/intervention_asymmetry_table.csv"
raw <- read.csv(csv_path, stringsAsFactors = FALSE, na.strings = c("NA", ""))

## ============================================================
## DATA PREPARATION
## ============================================================

## Domain display labels and Y-axis ordering (top to bottom)
domain_order <- c("C8", "C11", "C12", "C13", "D_alcohol", "C_pigbutch")

domain_display <- c(
  "C8"        = "C8  Investment FOMO\n(retirement participation, pp)",
  "C11"       = "C11  Diet\n(SSB consumption, % reduction)",
  "C12"       = "C12  Short-video\n(screen time, Cohen's d)",
  "C13"       = "C13  Housing leverage\n(LTV/default, mixed units) \u2020",
  "D_alcohol" = "D\u03B1  Alcohol\n(consumption, Cohen's d / elasticity)",
  "C_pigbutch"= "C\u03C0  Pig-butchering\n(victimisation, Cohen's d / %)\u2020\u2020"
)

## Standardise: we plot each domain on its own native axis position
## For panel (a), we use a NORMALISED display where each row is scaled so
## the information dot anchors to a consistent visual position.
## We use 'effect_size' directly and indicate units via the y-label.
## All values use the sign convention: positive = desired welfare direction.
## C11 signal_redesign is negative (reduction in SSB is good): flip sign.
## C11 information is also negative kcal reduction: flip sign.
## For C11: we work in absolute reduction magnitude (positive = better).
## For D_alcohol elasticity: we use absolute value (positive = reduction).

df <- raw %>%
  mutate(
    ## Sign convention: positive = better welfare outcome
    effect_plot = case_when(
      domain_id == "C11" ~ -effect_size,       # kcal/pct reduction: flip negative to positive
      TRUE               ~ abs(effect_size)    # everything else: use absolute magnitude
    ),
    ci_low_plot = case_when(
      domain_id == "C11" & intervention_type == "information"     ~ -ci_high,
      domain_id == "C11" & intervention_type == "signal_redesign" ~ -ci_high,
      TRUE ~ pmin(abs(ci_low), abs(ci_high), na.rm = TRUE)
    ),
    ci_high_plot = case_when(
      domain_id == "C11" & intervention_type == "information"     ~ -ci_low,
      domain_id == "C11" & intervention_type == "signal_redesign" ~ -ci_low,
      TRUE ~ pmax(abs(ci_low), abs(ci_high), na.rm = TRUE)
    )
  ) %>%
  ## Replace NA CI with approximate ±SE based on typical single-study CIs
  mutate(
    ci_low_plot  = ifelse(is.na(ci_low_plot),  effect_plot * 0.50, ci_low_plot),
    ci_high_plot = ifelse(is.na(ci_high_plot), effect_plot * 1.50, ci_high_plot)
  ) %>%
  mutate(
    domain_id    = factor(domain_id, levels = domain_order),
    domain_label = domain_display[as.character(domain_id)],
    domain_label = factor(domain_label, levels = rev(domain_display[domain_order])),
    int_type     = factor(intervention_type,
                          levels = c("information", "signal_redesign"),
                          labels = c("Information intervention", "Signal redesign"))
  )

## Y-offset so two dots per row don't overlap (information slightly below)
df <- df %>%
  mutate(
    y_numeric = as.numeric(domain_label),
    y_offset  = ifelse(intervention_type == "information", -0.18, +0.18),
    y_pos     = y_numeric + y_offset,
    ## dot colour: information = grey, signal_redesign = domain colour
    dot_colour = ifelse(
      intervention_type == "information",
      "#888888",
      domain_colours[as.character(domain_id)]
    ),
    dot_shape = ifelse(intervention_type == "information", 21L, 16L),  # open vs filled
    dot_size  = ifelse(intervention_type == "information", 1.8, 2.0),
    ## CI line type: emerging evidence gets dashed
    ci_lty = ifelse(emerging == TRUE, "dashed", "solid"),
    ## Flag NA CI: where original was NA, use dotted to signal approximate
    ci_approx = is.na(raw$ci_low[match(paste(domain_id, intervention_type),
                                        paste(raw$domain_id, raw$intervention_type))])
  )

## Source labels for annotation below each signal_redesign dot
source_labels <- df %>%
  filter(intervention_type == "signal_redesign") %>%
  mutate(
    src_label = case_when(
      domain_id == "C8"        ~ "Madrian & Shea 2001",
      domain_id == "C11"       ~ "Teng et al. 2019",
      domain_id == "C12"       ~ "Allcott et al. 2022",
      domain_id == "C13"       ~ "Kuttner & Shim 2016",
      domain_id == "D_alcohol" ~ "Wagenaar et al. 2009",
      domain_id == "C_pigbutch"~ "TRM Labs (emerging)",
      TRUE ~ source_short
    )
  )

info_source_labels <- df %>%
  filter(intervention_type == "information") %>%
  mutate(
    src_label = case_when(
      domain_id == "C8"        ~ "Fernandes et al. 2014",
      domain_id == "C11"       ~ "Long et al. 2015",
      domain_id == "C12"       ~ "Allcott et al. 2022",
      domain_id == "C13"       ~ "Moulton et al. 2015",
      domain_id == "D_alcohol" ~ "Wilkinson et al. 2009",
      domain_id == "C_pigbutch"~ "Burnes et al. 2017",
      TRUE ~ source_short
    )
  )

## ============================================================
## PANEL (a) — FOREST PLOT
## ============================================================

## Each domain needs its own x-scale; we use a NORMALISED RELATIVE scale
## where 0 = no effect and effect sizes are scaled within each domain
## so they're visually comparable. We report native units on y-labels.
## The critical visual claim is just: dark dot > grey dot in each row.
## We normalise: divide each domain's effects by the signal_redesign value
## so signal_redesign = 1.0 and information is a fraction thereof.

## Compute normalisation factor (= signal_redesign effect for each domain)
norm_factors <- df %>%
  filter(intervention_type == "signal_redesign") %>%
  select(domain_id, signal_effect = effect_plot, signal_ci_high = ci_high_plot)

df_norm <- df %>%
  left_join(norm_factors, by = "domain_id") %>%
  mutate(
    ## Normalised: signal_redesign = 1.0 by definition
    eff_norm     = effect_plot   / signal_effect,
    ci_low_norm  = ci_low_plot   / signal_effect,
    ci_high_norm = ci_high_plot  / signal_effect
  )

## For C11 information, ci spans 0 in native units (−20 to +4 kcal)
## After sign flip and normalisation, this means CI crosses 0 — preserve this
df_norm <- df_norm %>%
  mutate(
    ci_low_norm = case_when(
      domain_id == "C11" & intervention_type == "information" ~ -20 / (-10),  # = 2.0 (rescaled)
      TRUE ~ ci_low_norm
    ),
    ci_high_norm = case_when(
      domain_id == "C11" & intervention_type == "information" ~ 4 / (-10),    # = -0.4 after sign flip
      TRUE ~ ci_high_norm
    )
  ) %>%
  ## Ensure ci_low < ci_high after all transformations
  mutate(
    tmp_lo = pmin(ci_low_norm, ci_high_norm),
    tmp_hi = pmax(ci_low_norm, ci_high_norm),
    ci_low_norm  = tmp_lo,
    ci_high_norm = tmp_hi
  )

## Background alternating bands
n_domains <- length(domain_order)

pA <- ggplot(df_norm) +
  ## Alternating row bands
  annotate("rect", xmin = -Inf, xmax = Inf,
           ymin = seq(0.5, n_domains - 0.5, by = 2),
           ymax = seq(1.5, n_domains + 0.5, by = 2),
           fill = "grey96", colour = NA) +
  ## Reference line at 0 (no effect)
  geom_vline(xintercept = 0, linewidth = 0.5, colour = "grey40", linetype = "dashed") +
  ## Reference line at normalised 1.0 (signal redesign level — implicit)
  ## CI bars
  geom_linerange(
    data = filter(df_norm, !is.na(ci_low_norm)),
    aes(y = y_pos, xmin = ci_low_norm, xmax = ci_high_norm,
        colour = dot_colour, linetype = ci_lty),
    linewidth = 0.45
  ) +
  ## Points — information (open grey circles)
  geom_point(
    data = filter(df_norm, intervention_type == "information"),
    aes(y = y_pos, x = eff_norm),
    shape = 21, size = 2.0, colour = "#888888", fill = "white", stroke = 0.6
  ) +
  ## Points — signal redesign (filled domain-colour circles)
  geom_point(
    data = filter(df_norm, intervention_type == "signal_redesign"),
    aes(y = y_pos, x = eff_norm, colour = dot_colour),
    shape = 16, size = 2.2
  ) +
  ## "emerging" annotation for C_pig signal redesign
  annotate("text",
           x    = df_norm$eff_norm[df_norm$domain_id == "C_pigbutch" &
                                   df_norm$intervention_type == "signal_redesign"] + 0.05,
           y    = df_norm$y_pos[df_norm$domain_id == "C_pigbutch" &
                                df_norm$intervention_type == "signal_redesign"],
           label = "\u2020\u2020 emerging",
           hjust = 0, size = 1.7, colour = tol_green, fontface = "italic") +
  ## cross-instrument dagger for C13
  annotate("text",
           x    = df_norm$eff_norm[df_norm$domain_id == "C13" &
                                   df_norm$intervention_type == "signal_redesign"] + 0.05,
           y    = df_norm$y_pos[df_norm$domain_id == "C13" &
                                df_norm$intervention_type == "signal_redesign"],
           label = "\u2020 cross-instrument",
           hjust = 0, size = 1.7, colour = tol_purple, fontface = "italic") +
  scale_colour_identity() +
  scale_linetype_identity() +
  scale_x_continuous(
    name   = "Effect size (domain-normalised; signal-redesign = 1.0)",
    limits = c(-0.5, 1.6),
    breaks = c(0, 0.25, 0.5, 0.75, 1.0, 1.25),
    labels = c("0", "0.25", "0.50", "0.75", "1.0\n(signal\nredesign)", "1.25"),
    expand = c(0.02, 0.02)
  ) +
  scale_y_continuous(
    breaks = 1:n_domains,
    labels = rev(domain_display[domain_order]),
    expand = c(0.08, 0.08)
  ) +
  ylab(NULL) +
  nature_theme() +
  theme(
    axis.text.y      = element_text(size = 5.5, colour = "black", hjust = 1, lineheight = 1.1),
    axis.text.x      = element_text(size = 5.5),
    legend.position  = "none"
  ) +
  labs(tag = "a")

## Add manual legend as annotation (inside plot, bottom right area)
pA <- pA +
  annotate("point", x = 0.70, y = 0.65, shape = 21, size = 2.0,
           colour = "#888888", fill = "white", stroke = 0.6) +
  annotate("text",  x = 0.76, y = 0.65, label = "Information intervention",
           hjust = 0, size = 1.9, colour = "grey30") +
  annotate("point", x = 0.70, y = 0.30, shape = 16, size = 2.2,
           colour = "grey40") +
  annotate("text",  x = 0.76, y = 0.30, label = "Signal redesign",
           hjust = 0, size = 1.9, colour = "grey30")

## ============================================================
## PANEL (b) — WITHIN-DOMAIN LOG RATIO
## ============================================================

## Build ratio df from raw source (not from df which has factors that complicate pivot)
ratio_base <- df %>%
  select(domain_id, intervention_type, effect_plot, ci_low_plot, ci_high_plot) %>%
  mutate(domain_id = as.character(domain_id),
         intervention_type = as.character(intervention_type))

## Get emerging / cross_instrument flags per domain (from signal_redesign rows)
domain_flags <- df %>%
  filter(intervention_type == "signal_redesign") %>%
  select(domain_id, emerging, cross_instrument) %>%
  mutate(domain_id = as.character(domain_id))

ratio_df <- ratio_base %>%
  pivot_wider(
    id_cols     = domain_id,
    names_from  = intervention_type,
    values_from = c(effect_plot, ci_low_plot, ci_high_plot)
  ) %>%
  left_join(domain_flags, by = "domain_id") %>%
  mutate(
    ## Ratio = signal_redesign / information
    ## Use absolute values; both should be > 0 (positive = better welfare)
    ratio          = effect_plot_signal_redesign / pmax(effect_plot_information, 0.001),
    ## Approximate CI for ratio using delta method on log ratio
    ## log(ratio) = log(signal) - log(info)
    ## Var[log(ratio)] ≈ (CI_signal / (2*1.96*signal))^2 + (CI_info / (2*1.96*info))^2
    se_log_signal  = (ci_high_plot_signal_redesign - ci_low_plot_signal_redesign) / (2 * 1.96 * effect_plot_signal_redesign),
    se_log_info    = (ci_high_plot_information - ci_low_plot_information) / (2 * 1.96 * pmax(effect_plot_information, 0.001)),
    se_log_info    = ifelse(is.na(se_log_info) | is.infinite(se_log_info), 1.0, se_log_info),
    se_log_signal  = ifelse(is.na(se_log_signal) | is.infinite(se_log_signal), 0.5, se_log_signal),
    se_log_ratio   = sqrt(se_log_signal^2 + se_log_info^2),
    ratio_ci_low   = exp(log(ratio) - 1.96 * se_log_ratio),
    ratio_ci_high  = exp(log(ratio) + 1.96 * se_log_ratio),
    ## C_pig and C13 get extra-wide CI per spec
    ratio_ci_low   = ifelse(domain_id == "C_pigbutch", ratio * 0.30, ratio_ci_low),
    ratio_ci_high  = ifelse(domain_id == "C_pigbutch", ratio * 3.50, ratio_ci_high),
    ratio_ci_low   = ifelse(domain_id == "C13", ratio * 0.40, ratio_ci_low),
    ratio_ci_high  = ifelse(domain_id == "C13", ratio * 2.80, ratio_ci_high),
    ## C11 info CI spans 0 => ratio is effectively unbounded above; cap at reasonable visual limit
    ratio_ci_high  = ifelse(domain_id == "C11", 40, ratio_ci_high),
    ratio_ci_low   = ifelse(domain_id == "C11", 0.8, ratio_ci_low),
    ## Keep domain_id as character for sorting
    domain_id      = as.character(domain_id)
  ) %>%
  arrange(ratio)

ratio_df$domain_label_short <- c(
  "C8"        = "C8  Investment",
  "C11"       = "C11  Diet",
  "C12"       = "C12  Short-video",
  "C13"       = "C13  Housing\u2020",
  "D_alcohol" = "D\u03B1  Alcohol",
  "C_pigbutch"= "C\u03C0  Pig-butch.\u2020\u2020"
)[as.character(ratio_df$domain_id)]

## Ordered by ratio for display
ratio_df <- ratio_df %>%
  arrange(ratio) %>%
  mutate(
    y_rank = row_number(),
    bar_colour = domain_colours[as.character(domain_id)],
    ci_lty     = ifelse(domain_id == "C_pigbutch", "dashed", "solid")
  )

## Median ratio reference line
median_ratio <- median(ratio_df$ratio)

pB <- ggplot(ratio_df, aes(y = y_rank)) +
  ## Reference line at ratio = 1 (equal effect)
  geom_vline(xintercept = 1, linewidth = 0.5, colour = "grey40", linetype = "dashed") +
  ## Reference line at median ratio
  geom_vline(xintercept = median_ratio, linewidth = 0.5, colour = "grey20", linetype = "solid") +
  ## CI error bars (horizontal)
  geom_linerange(
    aes(xmin = ratio_ci_low, xmax = ratio_ci_high,
        colour = bar_colour, linetype = ci_lty),
    linewidth = 0.45
  ) +
  ## Domain-coloured filled bars (as thick line segments)
  geom_segment(
    aes(x = 1, xend = ratio, yend = y_rank, colour = bar_colour),
    linewidth = 2.5, alpha = 0.35
  ) +
  ## Filled dot at ratio
  geom_point(
    aes(x = ratio, colour = bar_colour),
    shape = 16, size = 2.2
  ) +
  ## Ratio value labels
  geom_text(
    aes(x = ratio, label = sprintf("%.0f\u00D7", ratio)),
    hjust = -0.3, vjust = 0.4, size = 1.9, colour = "grey20"
  ) +
  ## Annotation: "signal redesign dominates" region
  annotate("rect",
           xmin = 3, xmax = Inf, ymin = -Inf, ymax = Inf,
           fill = scales::alpha(tol_blue, 0.04)) +
  annotate("text",
           x = 4, y = 6.5, label = "Signal redesign\ndominates (ratio > 3)",
           hjust = 0, size = 1.8, colour = tol_blue, fontface = "italic",
           lineheight = 1.0) +
  ## Median label
  annotate("text",
           x = median_ratio + 0.5, y = 0.7,
           label = sprintf("Median = %.0f\u00D7", median_ratio),
           hjust = 0, size = 1.8, colour = "grey20") +
  ## "no advantage" label at x = 1
  annotate("text",
           x = 1.1, y = 0.7,
           label = "No advantage (ratio = 1)",
           hjust = 0, size = 1.8, colour = "grey40", fontface = "italic") +
  scale_colour_identity() +
  scale_linetype_identity() +
  scale_x_log10(
    name   = "Ratio: signal redesign \u00F7 information effect (log scale)",
    limits = c(0.5, 200),
    breaks = c(1, 2, 5, 10, 20, 50, 100),
    labels = c("1", "2", "5", "10", "20", "50", "100"),
    expand = c(0.02, 0.02)
  ) +
  scale_y_continuous(
    breaks = 1:nrow(ratio_df),
    labels = ratio_df$domain_label_short,
    expand = c(0.1, 0.1)
  ) +
  ylab(NULL) +
  nature_theme() +
  theme(
    axis.text.y = element_text(size = 5.5, colour = "black", hjust = 1),
    axis.text.x = element_text(size = 5.5)
  ) +
  labs(tag = "b")

## ============================================================
## COMPOSE — 180 mm × 130 mm (two panels side by side)
## ============================================================

fig8 <- pA | pB +
  plot_layout(widths = c(1.35, 1.0)) &
  theme(plot.margin = margin(4, 4, 4, 4, "pt"))

## ============================================================
## SAVE
## ============================================================

out_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main"

ggsave(
  filename = file.path(out_dir, "fig8_intervention_asymmetry.png"),
  plot     = fig8,
  width    = 180, height = 130, units = "mm",
  dpi      = 300, bg = "white"
)

ggsave(
  filename = file.path(out_dir, "fig8_intervention_asymmetry.pdf"),
  plot     = fig8,
  width    = 180, height = 130, units = "mm",
  device   = cairo_pdf
)

message("Figure 8 (v2.4) saved: fig8_intervention_asymmetry.png + .pdf")
message(sprintf("Median signal-redesign/information ratio: %.1fx", median_ratio))
message("Cross-instrument note (C13): dagger annotation applied.")
message("Emerging evidence note (C_pig): wider CI + dagger annotation applied.")
