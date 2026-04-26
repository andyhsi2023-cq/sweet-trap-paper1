## ============================================================
## Figure 3 — Cross-Cultural Universality (Layer C)
## PLACEHOLDER: Layer C ISSP/WVS/ESS analysis pending (Task #40)
## This figure must be regenerated once Layer C data is available
## ============================================================

library(ggplot2)
library(patchwork)

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
      plot.tag         = element_text(size = 9, face = "bold", family = "Helvetica"),
      plot.margin      = margin(4, 4, 4, 4, "pt")
    )
}

tol_blue   <- "#0077BB"
tol_orange <- "#EE7733"
tol_grey   <- "#BBBBBB"

## ============================================================
## PLACEHOLDER LAYOUT
## Panel A: Country × Δ_ST hypothetical scatter (schematic only)
## Panel B: Conceptual τ_env gradient across cultural zones
## Panel C: Predicted F2 endorsement spectrum
## ============================================================

## ---------- Schematic country scatter ----------
## Hypothetical country-level Δ_ST vs income-inequality (Gini)
## This is a SCHEMATIC — all values synthetic, NOT from data
set.seed(42)
n_countries <- 30
country_df <- data.frame(
  gini_index  = rnorm(n_countries, mean = 42, sd = 10),
  delta_st_hyp = rnorm(n_countries, mean = 0.55, sd = 0.15),
  region = sample(c("East Asia", "S/SE Asia", "Europe", "Americas", "Africa"),
                  n_countries, replace = TRUE,
                  prob = c(0.20, 0.18, 0.25, 0.22, 0.15))
)
country_df$delta_st_hyp <- pmax(0.1, pmin(0.95, country_df$delta_st_hyp))
## Add weak positive trend (Gini higher → Δ_ST slightly higher)
country_df$delta_st_hyp <- country_df$delta_st_hyp +
  0.008 * (country_df$gini_index - 42) + rnorm(n_countries, 0, 0.05)
country_df$delta_st_hyp <- pmax(0.05, pmin(0.99, country_df$delta_st_hyp))

region_colours <- c(
  "East Asia" = tol_blue, "S/SE Asia" = tol_orange,
  "Europe" = tol_grey, "Americas" = "#009988", "Africa" = "#AA3377"
)

pA <- ggplot(country_df, aes(x = gini_index, y = delta_st_hyp, colour = region)) +
  ## Watermark
  annotate("text", x = 37, y = 0.9,
           label = "PRELIMINARY SCHEMATIC\nLayer C data pending",
           size = 7, colour = "grey90", fontface = "bold",
           angle = 20, hjust = 0.5) +
  geom_smooth(method = "lm", formula = y ~ x, se = TRUE,
              colour = "grey60", linewidth = 0.5, alpha = 0.15) +
  geom_point(size = 2, alpha = 0.8) +
  scale_colour_manual(name = "Region", values = region_colours) +
  scale_x_continuous(
    name   = "Income inequality (Gini index, schematic)",
    limits = c(20, 65),
    breaks = c(25, 35, 45, 55)
  ) +
  scale_y_continuous(
    name   = expression(Delta[ST] ~ "(schematic)"),
    limits = c(0.05, 1.0),
    breaks = c(0.2, 0.4, 0.6, 0.8)
  ) +
  nature_theme() +
  theme(legend.position = c(0.99, 0.01),
        legend.justification = c(1, 0),
        legend.background = element_rect(fill = "white", colour = "grey80", linewidth = 0.2)) +
  labs(tag = "a",
       title = "Hypothetical: Δ_ST × income inequality across nations (schematic)")

## ---------- Conceptual F2 endorsement spectrum ----------
endorsement_df <- data.frame(
  cultural_zone = factor(
    c("High individualism\n(N. Europe)", "Mixed\n(E. Europe)", "High collectivism\n(E. Asia)", "Low income\n(Global South)"),
    levels = c("High individualism\n(N. Europe)", "Mixed\n(E. Europe)",
               "High collectivism\n(E. Asia)", "Low income\n(Global South)")
  ),
  f2_endorsement_hyp = c(0.78, 0.65, 0.72, 0.41),   ## hypothetical
  ci_lo = c(0.60, 0.50, 0.55, 0.28),
  ci_hi = c(0.92, 0.78, 0.87, 0.55)
)

pB <- ggplot(endorsement_df,
             aes(x = cultural_zone, y = f2_endorsement_hyp)) +
  ## Watermark
  annotate("text", x = 2.5, y = 0.85,
           label = "SCHEMATIC", size = 8, colour = "grey90",
           fontface = "bold", angle = 15, hjust = 0.5) +
  geom_errorbar(aes(ymin = ci_lo, ymax = ci_hi),
                width = 0.18, linewidth = 0.5, colour = tol_blue) +
  geom_point(size = 2.5, colour = tol_blue) +
  geom_hline(yintercept = 0.50, linewidth = 0.3, linetype = "dashed", colour = "grey60") +
  scale_y_continuous(
    name   = "F2 endorsement index (schematic)",
    limits = c(0.2, 1.0),
    breaks = c(0.3, 0.5, 0.7, 0.9)
  ) +
  scale_x_discrete(name = "Cultural zone") +
  nature_theme() +
  labs(tag = "b",
       title = "Hypothetical F2 endorsement by cultural zone (schematic)")

## ---------- Data-pending notice panel ----------
notice_df <- data.frame(x = 0.5, y = 0.5,
                        label = "Layer C cross-cultural data pending\n\nPlanned sources:\n• ISSP 2012/2019 Work Orientations\n• WVS 7th wave (2017–2022)\n• ESS 2018/2020 (consumption module)\n\nPredict: Δ_ST > 0 in ≥ 10/12 countries\nEffect on universality claim: P-value test of\nH₀: Δ_ST ≤ 0 in any cultural zone\n\nBackground agent task #40 running...")

pC <- ggplot(notice_df, aes(x = x, y = y)) +
  geom_text(aes(label = label), size = 2.2, hjust = 0.5, vjust = 0.5,
            lineheight = 1.4, colour = "grey30") +
  scale_x_continuous(limits = c(0, 1), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0, 1), expand = c(0, 0)) +
  theme_void() +
  theme(
    panel.border = element_rect(colour = tol_grey, fill = NA, linewidth = 0.5),
    plot.tag = element_text(size = 9, face = "bold"),
    plot.margin = margin(4, 4, 4, 4, "pt")
  ) +
  labs(tag = "c")

## ============================================================
## COMPOSE — three panels
## ============================================================
fig3 <- (pA | pB) / pC +
  plot_layout(heights = c(1.2, 0.8)) +
  plot_annotation(
    caption = paste(
      "IMPORTANT: This is a preliminary schematic figure.",
      "All values are synthetic placeholders for layout purposes.",
      "Final figure requires Layer C ISSP/WVS/ESS analysis (Task #40).",
      sep = " "
    )
  ) &
  theme(plot.caption = element_text(size = 5, colour = tol_orange,
                                    face = "italic", hjust = 0))

## ============================================================
## SAVE
## ============================================================
out_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main"

ggsave(
  filename = file.path(out_dir, "fig3_cross_cultural_placeholder.png"),
  plot = fig3,
  width = 180, height = 130, units = "mm",
  dpi = 300, bg = "white"
)

message("Figure 3 placeholder saved. MUST replace with Layer C data.")
