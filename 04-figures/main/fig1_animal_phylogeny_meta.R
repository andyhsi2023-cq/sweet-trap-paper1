## ============================================================
## Figure 1 (v3.1) — Animal Sweet Trap: Phylogenetic Overview + Effect Sizes
## NHB consolidation: replaces old fig1_animal_meta + fig2_human_panels
## Target: Nature Human Behaviour, 180 mm × 200 mm
## Layout:
##   Panel (a): Phylogenetic dot plot — 20 cases by taxonomic class (top half)
##   Panel (b): Forest plot Δ_ST by mechanism category (olds_milner / sensory_exploit /
##              fisher_runaway / repro_survival), 20 cases + pooled
##   Panel (c): Pooled Δ_ST summary bar + I² annotation
## Paul Tol colorblind-safe palette throughout
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
tol_green  <- "#228833"

## ============================================================
## DATA — 20 animal cases (mirrors cross_level_meta.py Layer A)
## ============================================================

animal_df <- data.frame(
  case_id   = paste0("A", 1:20),
  case_name = c(
    "Moth / artificial light",
    "Sea-turtle hatchling",
    "Plastic ingestion (seabird)",
    "Drosophila / high-sugar",
    "Rat ICSS (Olds–Milner)",
    "Fisherian runaway (widowbird)",
    "Ecological trap (HPL/road)",
    "Neonicotinoid Apis/Bombus",
    "Ostracod arms race",
    "Túngara frog phonotaxis",
    "Monarch / tropical milkweed",
    "Floral-scent NO\u2083 degradation",
    "Swordtail sword ornament",
    "Julodimorpha beetle / bottles",
    "Migratory bird / urban light",
    "Bumblebee social disruption",
    "Guppy rare-male preference",
    "Zebra finch hidden cost",
    "Stalk-eyed fly eye span",
    "Milkweed bug Oncopeltus"
  ),
  taxon = c(
    "Insect", "Reptile", "Bird",
    "Insect", "Mammal",
    "Bird", "Insect", "Insect",
    "Crustacean", "Amphibian", "Insect",
    "Insect", "Fish", "Insect",
    "Bird", "Insect", "Fish",
    "Bird", "Insect", "Insect"
  ),
  mechanism = c(
    "sensory_exploit", "sensory_exploit", "sensory_exploit",
    "olds_milner", "olds_milner",
    "fisher_runaway", "sensory_exploit", "olds_milner",
    "fisher_runaway", "sensory_exploit", "sensory_exploit",
    "sensory_exploit", "fisher_runaway", "sensory_exploit",
    "sensory_exploit", "olds_milner", "fisher_runaway",
    "repro_survival", "fisher_runaway", "repro_survival"
  ),
  delta_st = c(
    0.82, 0.76, 0.64, 0.71, 0.97,
    0.58, 0.55, 0.73, 0.45, 0.61,
    0.68, 0.59, 0.52, 0.67, 0.60,
    0.78, 0.48, 0.42, 0.53, 0.38
  ),
  ci_lo = c(
    0.61, 0.58, 0.44, 0.52, 0.90,
    0.36, 0.34, 0.55, 0.28, 0.42,
    0.50, 0.40, 0.32, 0.48, 0.41,
    0.62, 0.30, 0.24, 0.34, 0.20
  ),
  ci_hi = c(
    0.95, 0.88, 0.79, 0.85, 1.00,
    0.75, 0.72, 0.86, 0.61, 0.77,
    0.83, 0.75, 0.69, 0.83, 0.76,
    0.91, 0.65, 0.59, 0.70, 0.56
  ),
  stringsAsFactors = FALSE
)

## Pooled row (DerSimonian-Laird, k=20; mirrors manuscript §3.1)
pooled_row <- data.frame(
  case_id = "Pooled", case_name = "Pooled RE (k = 20)",
  taxon = "—", mechanism = "pooled",
  delta_st = 0.645, ci_lo = 0.557, ci_hi = 0.733
)

## Mechanism subgroup pooled estimates (mirrors §3.1 + Fig panel b)
mech_pool <- data.frame(
  mechanism  = c("olds_milner", "sensory_exploit", "fisher_runaway", "repro_survival"),
  delta_mean = c(0.789, 0.653, 0.547, 0.470),
  ci_lo      = c(0.620, 0.560, 0.430, 0.330),
  ci_hi      = c(0.959, 0.745, 0.664, 0.610),
  n_cases    = c(4, 9, 5, 2),
  stringsAsFactors = FALSE
)

## ============================================================
## PANEL (a) — PHYLOGENETIC DOT STRIP
## Horizontal dot chart ordered by taxonomic class then by Δ_ST
## ============================================================

## Taxon ordering: Mammal, Bird, Reptile, Amphibian, Fish, Insect, Crustacean
taxon_order <- c("Mammal", "Bird", "Reptile", "Amphibian", "Fish", "Insect", "Crustacean")
taxon_colours <- c(
  "Mammal"     = tol_red,
  "Bird"        = tol_blue,
  "Reptile"     = tol_teal,
  "Amphibian"   = tol_green,
  "Fish"        = tol_cyan,
  "Insect"      = tol_orange,
  "Crustacean"  = tol_purple
)

animal_df$taxon_f <- factor(animal_df$taxon, levels = taxon_order)

## sort within taxon by delta_st descending for cleaner display
animal_plot <- animal_df %>%
  arrange(taxon_f, delta_st) %>%
  mutate(
    y_pos    = row_number(),
    t_colour = taxon_colours[as.character(taxon_f)]
  )

## mechanism shape
mech_shapes <- c("olds_milner" = 16, "sensory_exploit" = 17,
                 "fisher_runaway" = 15, "repro_survival" = 18)
animal_plot$mech_shape <- mech_shapes[animal_plot$mechanism]

pA <- ggplot(animal_plot, aes(y = y_pos, x = delta_st)) +
  ## Taxon coloured background strips
  annotate("rect",
           xmin = -Inf, xmax = Inf,
           ymin  = c(0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 19.5),
           ymax  = c(1.5, 2.5, 3.5, 4.5, 5.5, 19.5, 20.5),
           fill  = c(tol_red, tol_blue, tol_teal, tol_green, tol_cyan, tol_orange, tol_purple),
           alpha = 0.08) +
  ## Null line
  geom_vline(xintercept = 0, linewidth = 0.35, colour = "grey60", linetype = "dashed") +
  ## Pooled line
  geom_vline(xintercept = 0.645, linewidth = 0.5, colour = "grey30", linetype = "dotted") +
  ## CIs
  geom_errorbarh(aes(xmin = ci_lo, xmax = ci_hi, colour = t_colour),
                 height = 0.3, linewidth = 0.4) +
  ## Points by mechanism shape
  geom_point(aes(colour = t_colour, shape = factor(mech_shape)), size = 2.0) +
  scale_shape_manual(
    name   = "Mechanism",
    values = c("16" = 16, "17" = 17, "15" = 15, "18" = 18),
    labels = c("16" = "Olds–Milner", "17" = "Sensory exploit",
               "15" = "Fisher runaway", "18" = "Repro-survival"),
    guide  = guide_legend(override.aes = list(colour = "grey30", size = 2.2))
  ) +
  scale_colour_identity() +
  scale_x_continuous(
    name   = expression(Delta[ST] ~ "(reward\u2013fitness decoupling)"),
    limits = c(-0.05, 1.15),
    breaks = c(0, 0.2, 0.4, 0.6, 0.8, 1.0)
  ) +
  scale_y_continuous(
    breaks = animal_plot$y_pos,
    labels = animal_plot$case_name,
    expand = c(0.02, 0.02)
  ) +
  ## Pooled annotation
  annotate("text", x = 0.655, y = 20.8,
           label = "Pooled = 0.645 [0.557, 0.733]",
           size = 1.8, hjust = 0, colour = "grey30", fontface = "bold") +
  ## I2 annotation
  annotate("text", x = 0.02, y = 0.6,
           label = "I\u00b2 = 85.4%,  \u03c4\u00b2 = 0.041,  k = 20",
           size = 1.7, hjust = 0, colour = "grey40") +
  ## Taxon labels (right margin annotations)
  annotate("text", x = 1.12, y = 1.0,  label = "Mammal",    size = 1.7, hjust = 0, colour = tol_red)    +
  annotate("text", x = 1.12, y = 3.5,  label = "Bird",      size = 1.7, hjust = 0, colour = tol_blue)   +
  annotate("text", x = 1.12, y = 5.0,  label = "Rept./Amph./Fish", size = 1.5, hjust = 0, colour = tol_teal) +
  annotate("text", x = 1.12, y = 12.0, label = "Insect",    size = 1.7, hjust = 0, colour = tol_orange) +
  annotate("text", x = 1.12, y = 19.5, label = "Crustacean",size = 1.6, hjust = 0, colour = tol_purple) +
  ylab(NULL) +
  nature_theme() +
  theme(
    axis.text.y     = element_text(size = 5.0, lineheight = 1.0),
    legend.position = c(0.01, 0.03),
    legend.justification = c(0, 0),
    legend.background = element_rect(fill = NA, colour = NA)
  ) +
  labs(tag = "a")

## ============================================================
## PANEL (b) — MECHANISM SUBGROUP FOREST
## ============================================================

mech_labels <- c(
  "olds_milner"   = "Olds\u2013Milner\ndirect reward\n(n = 4)",
  "sensory_exploit" = "Sensory\nexploitation\n(n = 9)",
  "fisher_runaway"= "Fisher\nrunaway\n(n = 5)",
  "repro_survival"= "Repro-survival\ntradeoff\n(n = 2)"
)
mech_colours <- c(
  "olds_milner"   = tol_red,
  "sensory_exploit" = tol_orange,
  "fisher_runaway"= tol_blue,
  "repro_survival"= tol_teal
)

mech_pool$mech_label <- factor(mech_labels[mech_pool$mechanism],
                                levels = rev(mech_labels))
mech_pool$colour     <- mech_colours[mech_pool$mechanism]

pB <- ggplot(mech_pool, aes(y = mech_label, x = delta_mean, colour = colour)) +
  geom_vline(xintercept = 0.645, linewidth = 0.4, colour = "grey50", linetype = "dashed") +
  geom_vline(xintercept = 0, linewidth = 0.3, colour = "grey70", linetype = "dashed") +
  geom_errorbarh(aes(xmin = ci_lo, xmax = ci_hi),
                 height = 0.25, linewidth = 0.55) +
  geom_point(size = 3.0) +
  ## Contrast annotation: olds_milner vs fisher_runaway
  annotate("text", x = 0.78, y = 0.7,
           label = "Olds\u2013Milner vs Fisher\n\u0394 = +0.242, p = 0.001",
           size = 1.7, hjust = 0.5, colour = "grey20") +
  ## Pooled reference label
  annotate("text", x = 0.655, y = 4.65,
           label = "Pooled 0.645", size = 1.7, colour = "grey40", hjust = 0) +
  scale_colour_identity() +
  scale_x_continuous(
    name   = expression(Delta[ST] ~ "(subgroup mean)"),
    limits = c(0.25, 1.10),
    breaks = c(0.3, 0.5, 0.7, 0.9)
  ) +
  ylab(NULL) +
  nature_theme() +
  theme(
    axis.text.y = element_text(size = 5.5, lineheight = 1.1)
  ) +
  labs(
    tag   = "b",
    title = expression("Mechanism category moderates " * Delta[ST] *
                        " severity (Q"[M] * "(3) = 13.22, p = 0.004)")
  ) +
  theme(plot.title = element_text(size = 5.5, face = "plain", colour = "grey20"))

## ============================================================
## PANEL (c) — POOLED SUMMARY BAR + PREDICTION INTERVAL
## ============================================================

summary_df <- data.frame(
  est     = c(0.645, NA, NA),
  lo      = c(0.557, 0.278, NA),
  hi      = c(0.733, 1.011, NA),
  lbl     = c("Pooled RE", "95% PI", NA),
  y       = c(2, 1, NA),
  stringsAsFactors = FALSE
)

summary_df2 <- data.frame(
  x    = c(0.557, 0.278),
  xend = c(0.733, 1.011),
  y    = c(2.0, 1.4),
  yend = c(2.0, 1.4),
  col  = c("black", tol_grey),
  lbl  = c("95% CI", "95% PI"),
  stringsAsFactors = FALSE
)

pC <- ggplot() +
  ## Null line
  geom_vline(xintercept = 0, linewidth = 0.3, colour = "grey70", linetype = "dashed") +
  ## PI bar
  geom_segment(data = summary_df2[2, ],
               aes(x = x, xend = xend, y = y, yend = yend, colour = col),
               linewidth = 2.8, alpha = 0.25) +
  ## CI bar
  geom_segment(data = summary_df2[1, ],
               aes(x = x, xend = xend, y = y, yend = yend, colour = col),
               linewidth = 2.8, alpha = 0.7) +
  ## Diamond for pooled
  geom_point(aes(x = 0.645, y = 2.0), shape = 18, size = 5.0, colour = "black") +
  ## Labels
  annotate("text", x = 0.645, y = 2.55,
           label = "0.645\n[0.557, 0.733]",
           size = 2.0, hjust = 0.5, colour = "black", fontface = "bold",
           lineheight = 1.0) +
  annotate("text", x = 0.645, y = 1.05,
           label = "95% PI [0.278, 1.011]",
           size = 1.8, hjust = 0.5, colour = "grey40") +
  ## I2 + all-positive annotation
  annotate("text", x = 0.10, y = 0.45,
           label = "I\u00b2 = 85.4%   p-heterog. < 10\u207b\u2074   20/20 cases positive",
           size = 1.7, hjust = 0, colour = "grey30") +
  scale_colour_identity() +
  scale_x_continuous(
    name   = expression(Delta[ST]),
    limits = c(0, 1.12),
    breaks = c(0, 0.2, 0.4, 0.6, 0.8, 1.0)
  ) +
  scale_y_continuous(limits = c(0.2, 3.0), breaks = NULL) +
  ylab(NULL) +
  nature_theme() +
  theme(axis.line.y = element_blank(), axis.ticks.y = element_blank()) +
  labs(tag = "c", title = "Pooled animal meta-analysis (DerSimonian\u2013Laird RE, k = 20)") +
  theme(plot.title = element_text(size = 5.5, face = "plain", colour = "grey20"))

## ============================================================
## COMPOSE — 180 mm wide × 200 mm tall
## Left: Panel A (70% height); Right column: B / C stacked
## ============================================================

right_col <- pB / pC + plot_layout(heights = c(1.6, 1))
fig1_new  <- pA | right_col +
  plot_layout(widths = c(2.4, 1.6)) &
  theme(plot.margin = margin(4, 4, 4, 4, "pt"))

## ============================================================
## SAVE
## ============================================================

out_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main"

ggsave(
  filename = file.path(out_dir, "fig1_animal_phylogeny_meta.png"),
  plot     = fig1_new,
  width    = 180, height = 200, units = "mm",
  dpi      = 300, bg = "white"
)

ggsave(
  filename = file.path(out_dir, "fig1_animal_phylogeny_meta.pdf"),
  plot     = fig1_new,
  width    = 180, height = 200, units = "mm",
  device   = cairo_pdf
)

message("Fig 1 (v3.1) saved: fig1_animal_phylogeny_meta.{png,pdf}")
message("Panels: (a) phylogenetic dot strip 20 cases; (b) mechanism subgroup; (c) pooled summary")
