## ============================================================
## Figure 1 — Animal Meta-Synthesis (Layer A)
## Sweet Trap Cross-Species Framework
## Target: Science main, 180 mm double-column
## Layout: Panel A (forest, 60% width) | Panel B (F3 subgroup, upper right) | Panel C (tau bubble, lower right)
## Paul Tol colorblind-safe palette
## ============================================================

library(ggplot2)
library(cowplot)
library(patchwork)
library(dplyr)
library(scales)

## ---- Style ----
nature_theme <- function() {
  theme_classic(base_size = 7, base_family = "Helvetica") +
    theme(
      axis.line        = element_line(linewidth = 0.4, colour = "black"),
      axis.ticks       = element_line(linewidth = 0.3),
      axis.ticks.length = unit(2, "pt"),
      axis.text        = element_text(size = 6, colour = "black"),
      axis.title       = element_text(size = 7, colour = "black"),
      legend.text      = element_text(size = 6),
      legend.title     = element_text(size = 6, face = "bold"),
      legend.key.size  = unit(6, "pt"),
      panel.grid       = element_blank(),
      strip.text       = element_text(size = 6, face = "bold"),
      plot.tag         = element_text(size = 9, face = "bold", family = "Helvetica"),
      plot.margin      = margin(3, 3, 3, 3, "pt")
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

## ============================================================
## DATA
## ============================================================

## --- Panel A: Forest plot data ---
forest_df <- data.frame(
  case_id    = 8:1,
  label      = c(
    "5 — ICSS rat\n(Olds & Milner 1954)",
    "1 — Moth / artificial light\n(Fabian et al. 2024)",
    "2 — Sea-turtle hatchling\n(FWC panel 1995–2022)",
    "8 — Neonicotinoid bees\n(Woodcock et al. 2017)",
    "4 — Drosophila sugar\n(Libert et al. 2007)",
    "3 — Plastic ingestion\n(Santos et al. 2021)",
    "6 — Fisherian runaway\n(Andersson 1982)",
    "7 — Ecological/road trap\n(Horváth et al. 2009)"
  ),
  delta_st   = c(0.97, 0.82, 0.76, 0.73, 0.71, 0.64, 0.58, 0.55),
  ci_lo      = c(0.90, 0.61, 0.58, 0.55, 0.52, 0.44, 0.36, 0.34),
  ci_hi      = c(1.00, 0.95, 0.88, 0.86, 0.85, 0.79, 0.75, 0.72),
  f1_route   = c("B","A","A","B","A","B","A","A"),
  id_quality = c("High","High","High","High","High","Med-High","Medium","Medium")
)
## Pooled row
pooled_row <- data.frame(
  case_id = 0, label = "Pooled (RE model)", delta_st = 0.72,
  ci_lo = 0.60, ci_hi = 0.83, f1_route = "pooled", id_quality = "—"
)
forest_all <- rbind(forest_df, pooled_row)
forest_all$label <- factor(forest_all$label,
                            levels = rev(forest_all$label))
forest_all$shape  <- ifelse(forest_all$f1_route == "pooled", 18, 16)
forest_all$colour <- case_when(
  forest_all$f1_route == "A"      ~ tol_blue,
  forest_all$f1_route == "B"      ~ tol_orange,
  forest_all$f1_route == "pooled" ~ "black",
  TRUE ~ tol_grey
)
forest_all$size_pt <- ifelse(forest_all$f1_route == "pooled", 3.5, 2.0)

## --- Panel B: F3 mechanism subgroup ---
f3_df <- data.frame(
  mechanism  = factor(
    c("M4 mortality\n(Cases 1, 2)", "M1 individual\nhabit (Cases 4, 5)",
      "M1+M2 social\n(Cases 3, 7, 8)", "M2+M3 genetic/\nsocial (Case 6)"),
    levels = c("M4 mortality\n(Cases 1, 2)", "M1 individual\nhabit (Cases 4, 5)",
               "M1+M2 social\n(Cases 3, 7, 8)", "M2+M3 genetic/\nsocial (Case 6)")
  ),
  delta_mean = c(0.79, 0.84, 0.64, 0.58),
  ci_lo      = c(0.62, 0.71, 0.51, 0.36),
  ci_hi      = c(0.91, 0.96, 0.76, 0.75),
  colour_id  = c(tol_red, tol_orange, tol_teal, tol_purple)
)

## --- Panel C: tau_env / tau_adapt meta-regression ---
tau_df <- data.frame(
  case_id  = c(1, 2, 3, 4, 7, 8),
  label    = c("Moth", "Sea turtle", "Plastic", "Drosophila", "Ecol. trap", "Bees"),
  log_tau  = c(4.6, 3.6, 3.9, 3.5, 4.6, 3.5),   ## log(tau_env / tau_adapt), per layer_A §3.4
  delta_st = c(0.82, 0.76, 0.64, 0.71, 0.55, 0.73),
  weight   = c(0.117, 0.131, 0.113, 0.120, 0.104, 0.123),   ## RE weights from §3.2
  f1_route = c("A","A","B","A","A","B")
)
tau_df$bubble_size <- tau_df$weight * 35
tau_df$colour <- ifelse(tau_df$f1_route == "A", tol_blue, tol_orange)

## ============================================================
## PANELS
## ============================================================

## ----- Panel A: Forest plot -----
pA <- ggplot(forest_all, aes(y = label, x = delta_st)) +
  ## Separator line above pooled
  geom_hline(yintercept = 1.5, linetype = "dashed", linewidth = 0.3, colour = "grey60") +
  ## Reference line at 0
  geom_vline(xintercept = 0, linewidth = 0.3, colour = "grey50") +
  ## 95% CI
  geom_errorbarh(aes(xmin = ci_lo, xmax = ci_hi, colour = f1_route),
                 height = 0.25, linewidth = 0.4) +
  ## Points
  geom_point(aes(colour = f1_route, size = case_id == 0, shape = f1_route)) +
  scale_colour_manual(
    name   = "F1 route",
    values = c("A" = tol_blue, "B" = tol_orange, "pooled" = "black"),
    labels = c("A" = "Route A: ancestral mismatch",
               "B" = "Route B: novel/hijack",
               "pooled" = "Pooled RE")
  ) +
  scale_shape_manual(
    values = c("A" = 16, "B" = 16, "pooled" = 18),
    guide  = "none"
  ) +
  scale_size_manual(values = c("FALSE" = 1.8, "TRUE" = 3.2), guide = "none") +
  scale_x_continuous(
    name   = expression(Delta[ST] ~ "(reward–fitness decoupling gradient)"),
    limits = c(-0.1, 1.15),
    breaks = c(0, 0.2, 0.4, 0.6, 0.8, 1.0),
    expand = c(0, 0)
  ) +
  ## Annotate pooled value
  annotate("text", x = 0.72, y = 1.15, label = "0.72 [0.60, 0.83]",
           size = 1.8, hjust = 0.5, fontface = "bold") +
  ## Annotate I2
  annotate("text", x = 0.04, y = 8.9,
           label = "I\u00b2 = 67%,  \u03c4\u00b2 = 0.031",
           size = 1.8, hjust = 0, colour = "grey30") +
  ylab(NULL) +
  nature_theme() +
  theme(
    legend.position   = c(0.01, 0.13),
    legend.background = element_rect(fill = NA, colour = NA),
    legend.justification = c(0, 0)
  ) +
  labs(tag = "a")

## ----- Panel B: F3 mechanism subgroup -----
pB <- ggplot(f3_df, aes(x = mechanism, y = delta_mean, colour = mechanism)) +
  geom_hline(yintercept = 0.72, linetype = "dashed", linewidth = 0.35, colour = "grey50") +
  geom_errorbar(aes(ymin = ci_lo, ymax = ci_hi), width = 0.2, linewidth = 0.5) +
  geom_point(size = 2.5) +
  scale_colour_manual(values = c(tol_red, tol_orange, tol_teal, tol_purple), guide = "none") +
  annotate("text", x = 4.45, y = 0.73, label = "Pooled", size = 1.7,
           colour = "grey40", hjust = 1) +
  scale_y_continuous(
    name   = expression(Delta[ST]),
    limits = c(0.3, 1.10),
    breaks = c(0.4, 0.6, 0.8, 1.0)
  ) +
  xlab("F3 persistence mechanism") +
  nature_theme() +
  theme(legend.position = "none") +
  labs(
    tag   = "b",
    title = expression("F3 mechanism moderates " * Delta[ST] * " severity")
  ) +
  theme(plot.title = element_text(size = 6, face = "plain", colour = "grey30"))

## ----- Panel C: tau bubble plot -----
pC <- ggplot(tau_df, aes(x = log_tau, y = delta_st, size = weight, colour = f1_route)) +
  geom_smooth(method = "lm", formula = y ~ x, se = FALSE,
              colour = "grey60", linewidth = 0.4, linetype = "dotted") +
  geom_point(alpha = 0.85) +
  geom_text(aes(label = label), size = 1.7, vjust = -1.0, hjust = 0.5,
            show.legend = FALSE) +
  scale_colour_manual(
    name   = "F1 route",
    values = c("A" = tol_blue, "B" = tol_orange),
    labels = c("A" = "Route A", "B" = "Route B")
  ) +
  scale_size_continuous(range = c(1.5, 5.5), guide = "none") +
  annotate("text", x = 3.4, y = 1.01,
           label = "β = +0.03 per log unit\np = 0.35 (N = 6)",
           size = 1.7, hjust = 0, colour = "grey40") +
  scale_x_continuous(
    name   = expression(log(tau[env] / tau[adapt])),
    limits = c(3.2, 5.0),
    breaks = c(3.5, 4.0, 4.5)
  ) +
  scale_y_continuous(
    name   = expression(Delta[ST]),
    limits = c(0.45, 1.08),
    breaks = c(0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
  ) +
  nature_theme() +
  theme(
    legend.position = c(0.98, 0.03),
    legend.justification = c(1, 0),
    legend.background = element_rect(fill = NA, colour = NA)
  ) +
  labs(
    tag   = "c",
    title = expression("P3: environmental vs adaptive timescale (" * tau[env] * "/" * tau[adapt] * ")")
  ) +
  theme(plot.title = element_text(size = 6, face = "plain", colour = "grey30"))

## ============================================================
## COMPOSE
## ============================================================
## Left column: Panel A (~60%); Right column: B over C (~40%)
right_col <- pB / pC + plot_layout(heights = c(1, 1))
fig1 <- pA | right_col +
  plot_layout(widths = c(3, 2))

## ============================================================
## SAVE — 180 mm wide, 120 mm tall @ 300 DPI
## ============================================================
out_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main"

ggsave(
  filename = file.path(out_dir, "fig1_animal_meta.png"),
  plot = fig1,
  width = 180, height = 120, units = "mm",
  dpi = 300, bg = "white"
)

ggsave(
  filename = file.path(out_dir, "fig1_animal_meta.pdf"),
  plot = fig1,
  width = 180, height = 120, units = "mm",
  device = cairo_pdf
)

message("Figure 1 saved.")
