## ============================================================
## Figure 6 — Mendelian Randomization Forest Plot (Layer D)
## Sweet Trap Cross-Species Framework
## Target: Science main, 180 × 200 mm
## Layout:
##   Panel A (top ~65%): 7-chain × 3-method forest plot on OR log scale
##   Panel B (mid ~17%): Cochran Q + Egger pleiotropy check tiles
##   Panel C (bot ~18%): Cross-species molecular bridge compact table
## Paul Tol colorblind-safe palette throughout
## ============================================================

library(ggplot2)
library(cowplot)
library(patchwork)
library(dplyr)
library(tidyr)
library(scales)
library(grid)
library(gtable)

## ---- Shared style (mirrors fig1_animal_meta.R) ----
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
tol_green  <- "#228833"  # discriminant validity — protective direction

## ============================================================
## READ SOURCE DATA
## ============================================================

csv_path <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/data/figure6_mr_forest.csv"
raw <- read.csv(csv_path, stringsAsFactors = FALSE)

mol_path <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/data/molecular_bridge_table.csv"
mol_raw  <- read.csv(mol_path, stringsAsFactors = FALSE)

## ============================================================
## PANEL A — FOREST PLOT DATA PREPARATION
## ============================================================

## Keep only COMPLETED chains and the three display methods
completed <- raw %>%
  filter(status == "COMPLETED",
         method %in% c("IVW_random", "weighted_median", "MR_Egger"))

## Map method to display label and shape
completed <- completed %>%
  mutate(
    method_label = case_when(
      method == "IVW_random"      ~ "IVW",
      method == "weighted_median" ~ "Weighted median",
      method == "MR_Egger"        ~ "MR-Egger",
      TRUE ~ method
    ),
    method_shape = case_when(
      method == "IVW_random"      ~ 16L,   # solid circle
      method == "weighted_median" ~ 15L,   # solid square (open via fill)
      method == "MR_Egger"        ~ 17L,   # triangle
      TRUE ~ 16L
    )
  )

## Assign sub-class group and display metadata per chain
## Groups control colour and Y-axis grouping
chain_meta <- tribble(
  ~chain_id, ~group,           ~group_label,                        ~y_label,                                     ~group_colour,   ~note,
  "1a",      "engineered",     "Group 1 — Engineered Sweet Trap",   "1a  Risk tolerance\n    → Depression",        tol_red,         "",
  "1b",      "engineered",     "Group 1 — Engineered Sweet Trap",   "1b  Risk tolerance\n    → Antidepressant use", tol_red,         "",
  "3c",      "mismatch",       "Group 2 — Ancestral-mismatch",      "3c  BMI\n    → Type-2 diabetes",              tol_orange,      "",
  "2b",      "mismatch",       "Group 2 — Ancestral-mismatch",      "2b  Drinks/wk\n    → Alcoholic liver",        tol_orange,      "",
  "5",       "discriminant",   "Group 3 — Discriminant validity",   "5    Years of schooling\n    → Depression",    tol_green,       "PROTECTIVE",
  "6",       "structural",     "Group 4 — Structural validity",     "6    Subjective wellbeing\n    → Depression",  tol_blue,        "",
  "7",       "pleiotropy",     "Group 5 — Pleiotropy flagged (SI)", "7    Smoking initiation\n    → Alcoholic liver", tol_grey,      "FLAG"
)

## Y-axis order: group ordering top to bottom as specified
y_order <- c(
  "1a  Risk tolerance\n    → Depression",
  "1b  Risk tolerance\n    → Antidepressant use",
  "3c  BMI\n    → Type-2 diabetes",
  "2b  Drinks/wk\n    → Alcoholic liver",
  "5    Years of schooling\n    → Depression",
  "6    Subjective wellbeing\n    → Depression",
  "7    Smoking initiation\n    → Alcoholic liver"
)

forest_df <- completed %>%
  left_join(chain_meta, by = "chain_id") %>%
  mutate(y_label = factor(y_label, levels = rev(y_order)))

## IVW p-value annotations (one label per chain, placed at right margin)
## Pull IVW rows only for the text labels
ivw_labels <- forest_df %>%
  filter(method == "IVW_random") %>%
  mutate(
    pval_text = case_when(
      pval < 1e-8  ~ "p < 10⁻⁸",
      pval < 1e-7  ~ sprintf("p = %.0e", pval),
      pval < 1e-4  ~ sprintf("p = %.1e", pval),
      TRUE         ~ sprintf("p = %.3f", pval)
    ),
    # Nicer manual formatting for key chains
    pval_text = case_when(
      chain_id == "1a" ~ "p = 4.9×10⁻⁵",
      chain_id == "1b" ~ "p = 9.8×10⁻⁵",
      chain_id == "2b" ~ "p = 8.2×10⁻⁷",
      chain_id == "3c" ~ "p = 1.6×10⁻⁸",
      chain_id == "5"  ~ "p = 0.006",
      chain_id == "6"  ~ "p = 1.3×10⁻⁴",
      chain_id == "7"  ~ "p < 10⁻⁸ ⚠",
      TRUE ~ pval_text
    )
  )

## OR text for right-side annotation
ivw_labels <- ivw_labels %>%
  mutate(
    or_text = sprintf("OR = %.2f [%.2f, %.2f]", or, or_lo95, or_hi95)
  )

## Method offset on y-axis so three dots per chain don't overlap
## IVW: 0, WMed: -0.18, Egger: +0.18
forest_df <- forest_df %>%
  mutate(
    y_numeric = as.numeric(y_label),
    y_offset  = case_when(
      method == "IVW_random"      ~  0,
      method == "weighted_median" ~ -0.18,
      method == "MR_Egger"        ~  0.18,
      TRUE ~ 0
    ),
    y_pos = y_numeric + y_offset,
    # Alpha: pleiotropy-flagged chain gets lower alpha
    pt_alpha = ifelse(group == "pleiotropy", 0.45, 0.90),
    # Line type: pleiotropy dashed
    ci_lty   = ifelse(group == "pleiotropy", "dashed", "solid")
  )

## Clip extreme Egger CIs for chain 6 (4 SNPs, very wide) and chain 7
## to preserve readable scale — note in caption
forest_df <- forest_df %>%
  mutate(
    or_lo95_plot = pmax(or_lo95, 0.20),
    or_hi95_plot = pmin(or_hi95, 18.0),
    clipped      = (or_lo95 < 0.20 | or_hi95 > 18.0)
  )

## ============================================================
## PANEL A — BUILD PLOT
## ============================================================

## Group background bands (alternating light fills)
n_chains   <- length(y_order)
band_data  <- data.frame(
  ymin  = c(6.5, 4.5, 3.5, 2.5, 1.5),  # in reversed factor space
  ymax  = c(7.5, 5.5, 4.5, 3.5, 2.5),
  group = c("engineered", "mismatch", "discriminant", "structural", "pleiotropy"),
  fill  = c(
    scales::alpha(tol_red,    0.05),
    scales::alpha(tol_orange, 0.05),
    scales::alpha(tol_green,  0.06),
    scales::alpha(tol_blue,   0.05),
    scales::alpha(tol_grey,   0.04)
  )
)

## Group header label positions (at top of each band)
group_headers <- tribble(
  ~y_pos, ~label,
  7.1,    "Engineered Sweet Trap (variable-ratio hijack)",
  4.7,    "Ancestral-mismatch Sweet Trap",
  3.7,    "Discriminant validity (negative control)",
  2.7,    "Structural validity",
  1.7,    "Pleiotropy flagged — SI only"
)
group_header_colours <- c(tol_red, tol_orange, tol_green, tol_blue, tol_grey)

pA <- ggplot(forest_df) +
  ## Background bands
  annotate("rect", xmin = -Inf, xmax = Inf,
           ymin = 6.5, ymax = 7.5, fill = scales::alpha(tol_red,    0.06)) +
  annotate("rect", xmin = -Inf, xmax = Inf,
           ymin = 4.5, ymax = 6.5, fill = scales::alpha(tol_orange, 0.06)) +
  annotate("rect", xmin = -Inf, xmax = Inf,
           ymin = 3.5, ymax = 4.5, fill = scales::alpha(tol_green,  0.07)) +
  annotate("rect", xmin = -Inf, xmax = Inf,
           ymin = 2.5, ymax = 3.5, fill = scales::alpha(tol_blue,   0.06)) +
  annotate("rect", xmin = -Inf, xmax = Inf,
           ymin = 0.5, ymax = 2.5, fill = scales::alpha(tol_grey,   0.05)) +
  ## OR = 1 null reference line
  geom_vline(xintercept = 1, linewidth = 0.5, colour = "grey30", linetype = "solid") +
  ## CI whiskers — solid vs dashed for pleiotropy
  geom_linerange(
    data = filter(forest_df, group != "pleiotropy"),
    aes(y = y_pos, xmin = or_lo95_plot, xmax = or_hi95_plot,
        colour = group_colour),
    linewidth = 0.45
  ) +
  geom_linerange(
    data = filter(forest_df, group == "pleiotropy"),
    aes(y = y_pos, xmin = or_lo95_plot, xmax = or_hi95_plot,
        colour = group_colour),
    linewidth = 0.40, linetype = "dashed"
  ) +
  ## Points
  geom_point(
    aes(y = y_pos, x = or,
        colour = group_colour,
        shape  = method_label,
        size   = method_label,
        alpha  = pt_alpha)
  ) +
  ## Clip indicator arrows (tiny triangle at edge)
  geom_point(
    data = filter(forest_df, clipped == TRUE),
    aes(y = y_pos, x = ifelse(or_hi95 > 18, 17.8, 0.22)),
    shape = 62, size = 1.8, colour = tol_grey  # ">" character
  ) +
  ## p-value text at right margin
  geom_text(
    data = ivw_labels,
    aes(y = as.numeric(y_label), x = 19, label = pval_text,
        colour = group_colour),
    hjust = 0, size = 1.8, fontface = "plain"
  ) +
  ## OR [CI] text (small, just right of point cluster, IVW only)
  geom_text(
    data = ivw_labels,
    aes(y = as.numeric(y_label) - 0.33, x = 0.22, label = or_text,
        colour = group_colour),
    hjust = 0, size = 1.65, fontface = "plain"
  ) +
  ## Discriminant validity annotation banner — right of p-value column
  annotate("text",
           x = 19, y = 3.33,
           label = "PROTECTIVE — distinguishes Sweet Trap\nfrom welfare-enhancing aspiration",
           colour = tol_green, hjust = 0, size = 1.65, fontface = "bold.italic",
           lineheight = 1.1) +
  ## Group header labels: placed at the CENTRE of each band, far left, italic small
  ## Band centres: Engineered=6.5, Mismatch=4.5, Discriminant=3, Structural=2, Pleiotropy=1
  annotate("text", x = 0.205, y = 6.50, hjust = 0, size = 1.65, fontface = "bold.italic",
           label = "Engineered Sweet Trap", colour = tol_red) +
  annotate("text", x = 0.205, y = 4.50, hjust = 0, size = 1.65, fontface = "bold.italic",
           label = "Ancestral-mismatch Sweet Trap", colour = tol_orange) +
  annotate("text", x = 0.205, y = 3.00, hjust = 0, size = 1.65, fontface = "bold.italic",
           label = "Discriminant validity (negative control)", colour = tol_green) +
  annotate("text", x = 0.205, y = 2.00, hjust = 0, size = 1.65, fontface = "bold.italic",
           label = "Structural validity", colour = tol_blue) +
  annotate("text", x = 0.205, y = 1.00, hjust = 0, size = 1.65, fontface = "bold.italic",
           label = "Pleiotropy flagged — SI only", colour = tol_grey) +
  ## Scales
  scale_x_log10(
    name   = "Odds ratio (95% CI), log scale",
    limits = c(0.20, 27),
    breaks = c(0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5, 8, 15),
    labels = c("0.3", "0.5", "0.7", "1", "1.5", "2", "3", "5", "8", "15"),
    expand = c(0, 0)
  ) +
  scale_y_continuous(
    breaks = 1:n_chains,
    labels = rev(y_order),
    expand = c(0.07, 0.07)
  ) +
  scale_colour_identity(
    guide  = "none"
  ) +
  scale_shape_manual(
    name   = "Method",
    values = c("IVW" = 16, "Weighted median" = 22, "MR-Egger" = 24),
    guide  = guide_legend(
      override.aes = list(colour = "grey30", fill = "grey30", size = 1.5),
      title.position = "top"
    )
  ) +
  scale_size_manual(
    values = c("IVW" = 2.0, "Weighted median" = 1.6, "MR-Egger" = 1.6),
    guide  = "none"
  ) +
  scale_alpha_identity() +
  ylab(NULL) +
  nature_theme() +
  theme(
    axis.text.y       = element_text(size = 6, colour = "black", hjust = 1,
                                     lineheight = 1.1),
    legend.position   = c(0.01, 0.02),
    legend.justification = c(0, 0),
    legend.background = element_rect(fill = "white", colour = NA, linewidth = 0),
    legend.direction  = "horizontal",
    legend.box        = "horizontal"
  ) +
  labs(tag = "a",
       title = "Layer D: Mendelian randomization causal evidence across three Sweet Trap sub-classes") +
  theme(plot.title = element_text(size = 6.5, face = "bold", colour = "black",
                                  margin = margin(b = 2)))

## ============================================================
## PANEL B — COCHRAN Q + EGGER PLEIOTROPY TILES
## ============================================================

## Build per-chain Q / Egger data
## Q comes from IVW rows; Egger intercept p comes from MR_Egger rows
q_from_ivw <- raw %>%
  filter(status == "COMPLETED", method == "IVW_random") %>%
  select(chain_id, nsnp, Q, Q_p)

egger_from_egger <- raw %>%
  filter(status == "COMPLETED", method == "MR_Egger") %>%
  select(chain_id, egger_intercept_p)

q_egger <- q_from_ivw %>%
  left_join(egger_from_egger, by = "chain_id") %>%
  left_join(chain_meta %>% select(chain_id, y_label, group_colour), by = "chain_id") %>%
  mutate(
    y_label  = factor(y_label, levels = rev(y_order)),
    ## Egger flag
    egger_clean = ifelse(is.na(egger_intercept_p) | egger_intercept_p > 0.10,
                         "CLEAN", "FLAG"),
    ## Q heterogeneity text — guard against exact 0
    Q_text  = case_when(
      is.na(Q_p)    ~ "Q n/a",
      Q_p < 0.001   ~ "Q p < 0.001",
      TRUE          ~ sprintf("Q p = %.3f", Q_p)
    ),
    Q_fill  = case_when(
      is.na(Q_p)   ~ "white",
      Q_p > 0.05   ~ scales::alpha(tol_teal, 0.30),
      Q_p > 0.01   ~ scales::alpha(tol_orange, 0.30),
      TRUE         ~ scales::alpha(tol_red, 0.30)
    ),
    egger_text = case_when(
      egger_clean == "FLAG"     ~ sprintf("Egger p = %.3f  ⚠ FLAG", egger_intercept_p),
      !is.na(egger_intercept_p) ~ sprintf("Egger p = %.2f  CLEAN", egger_intercept_p),
      TRUE ~ "Egger n/a"
    ),
    egger_fill = case_when(
      egger_clean == "FLAG"     ~ scales::alpha(tol_red, 0.28),
      !is.na(egger_intercept_p) ~ scales::alpha(tol_teal, 0.22),
      TRUE ~ "white"
    ),
    egger_text_colour = ifelse(egger_clean == "FLAG", tol_red, "grey30")
  )

## We'll render Panel B as a ggplot tile/text grid
## Build two separate long frames then bind
q_long_Q <- q_egger %>%
  select(chain_id, y_label, Q_text, Q_fill, group_colour) %>%
  mutate(x_pos = 1, label = Q_text, tile_fill = Q_fill,
         text_col = "grey20")

q_long_E <- q_egger %>%
  select(chain_id, y_label, egger_text, egger_fill,
         egger_text_colour, group_colour) %>%
  mutate(x_pos = 2, label = egger_text, tile_fill = egger_fill,
         text_col = egger_text_colour)

q_long <- bind_rows(q_long_Q, q_long_E)

pB <- ggplot(q_long, aes(x = x_pos, y = y_label)) +
  geom_tile(aes(fill = tile_fill), colour = "white", linewidth = 0.4) +
  geom_text(aes(label = label, colour = text_col), size = 1.75, fontface = "plain") +
  scale_fill_identity() +
  scale_colour_identity() +
  scale_x_continuous(
    breaks = c(1, 2),
    labels = c("Cochran Q\n(heterogeneity)", "MR-Egger intercept\n(pleiotropy)"),
    expand = c(0.05, 0.05)
  ) +
  scale_y_discrete(expand = c(0.05, 0.05)) +
  ylab(NULL) + xlab(NULL) +
  nature_theme() +
  theme(
    axis.line         = element_blank(),
    axis.ticks        = element_blank(),
    axis.text.y       = element_blank(),
    axis.text.x       = element_text(size = 5.5, colour = "grey20"),
    panel.background  = element_rect(fill = "grey97", colour = NA),
    plot.background   = element_rect(fill = "white",  colour = NA)
  ) +
  labs(tag = "b",
       title = "Sensitivity: heterogeneity and pleiotropy") +
  theme(plot.title = element_text(size = 6.5, face = "bold",
                                  margin = margin(b = 2)))

## ============================================================
## PANEL C — MOLECULAR BRIDGE COMPACT TABLE
## ============================================================

## Select the 5 headline bridges as specified
bridge_ids <- c("TAS1R2", "DRD2", "ADH1B", "FTO", "CADM2")

bridge5 <- mol_raw %>%
  filter(gene %in% bridge_ids) %>%
  arrange(match(gene, bridge_ids)) %>%
  mutate(
    ## Compact display columns
    human_gene_display = case_when(
      gene == "TAS1R2" ~ "TAS1R2/TAS1R3",
      gene == "DRD2"   ~ "DRD2/DRD4/SLC6A3",
      gene == "ADH1B"  ~ "ADH1B/ALDH2",
      gene == "FTO"    ~ "FTO/MC4R",
      gene == "CADM2"  ~ "CADM2",
      TRUE ~ gene
    ),
    layer_b_domain = case_when(
      gene == "TAS1R2" ~ "C11 diet bitter",
      gene == "DRD2"   ~ "C8/C12 var-ratio",
      gene == "ADH1B"  ~ "D_alcohol",
      gene == "FTO"    ~ "C11 diet (appetite)",
      gene == "CADM2"  ~ "C8 / C4 impulsivity"
    ),
    animal_homolog = case_when(
      gene == "TAS1R2" ~ "Drosophila Gr64",
      gene == "DRD2"   ~ "Rodent dopamine (Olds–Milner)",
      gene == "ADH1B"  ~ "Drosophila Adh",
      gene == "FTO"    ~ "Rodent leptin–melanocortin",
      gene == "CADM2"  ~ "Cross-species (birds, rodents)"
    ),
    layer_a_case = case_when(
      gene == "TAS1R2" ~ "A4 (Δ_ST=+0.71)",
      gene == "DRD2"   ~ "A6 (Δ_ST=+0.97)",
      gene == "ADH1B"  ~ "D_alcohol causal chain",
      gene == "FTO"    ~ "A4 cross-sp. obesity",
      gene == "CADM2"  ~ "A5/A6 novelty-seek."
    ),
    row_num = row_number()
  )

## Build as ggplot with geom_text columns (compact 4-column table)
## We manually position text in a 4-column × 5-row grid
n_rows <- nrow(bridge5)
col_positions <- c(0.13, 0.38, 0.65, 0.88)
col_labels    <- c("Human gene(s)", "Layer B domain", "Animal homolog", "Layer A case")
col_fontface  <- c("bold", "plain", "italic", "plain")

## long-form for geom_text
bridge_long <- data.frame(
  row_num  = rep(bridge5$row_num, 4),
  col_id   = rep(1:4, each = n_rows),
  x_pos    = rep(col_positions, each = n_rows),
  label    = c(bridge5$human_gene_display,
               bridge5$layer_b_domain,
               bridge5$animal_homolog,
               bridge5$layer_a_case),
  fontface = rep(col_fontface, each = n_rows)
)

## Header row
bridge_header <- data.frame(
  row_num  = rep(0, 4),
  col_id   = 1:4,
  x_pos    = col_positions,
  label    = col_labels,
  fontface = rep("bold", 4)
)
bridge_all <- rbind(bridge_header, bridge_long)

## Gene column colouring matches sub-class
gene_colours <- c(
  "TAS1R2/TAS1R3"    = tol_orange,
  "DRD2/DRD4/SLC6A3" = tol_red,
  "ADH1B/ALDH2"      = tol_cyan,
  "FTO/MC4R"         = tol_orange,
  "CADM2"            = tol_purple
)
bridge_long_gene <- bridge_long %>%
  filter(col_id == 1) %>%
  mutate(colour = gene_colours[label])

pC <- ggplot() +
  ## Alternating row bands
  annotate("rect", xmin = -Inf, xmax = Inf,
           ymin = c(0.5, 2.5, 4.5), ymax = c(1.5, 3.5, 5.5),
           fill = "grey95", colour = NA) +
  ## Header separator
  annotate("segment", x = 0, xend = 1, y = 5.5, yend = 5.5,
           colour = "grey50", linewidth = 0.4) +
  annotate("segment", x = 0, xend = 1, y = 0.5, yend = 0.5,
           colour = "grey50", linewidth = 0.4) +
  ## Header text
  geom_text(data = bridge_header,
            aes(x = x_pos, y = n_rows + 0.75, label = label),
            hjust = 0.5, size = 1.9, fontface = "bold", colour = "grey20") +
  ## Data text — all columns except gene
  geom_text(data = filter(bridge_long, col_id != 1),
            aes(x = x_pos, y = (n_rows + 1) - row_num, label = label,
                fontface = fontface),
            hjust = 0.5, size = 1.75, colour = "grey20") +
  ## Gene column with colour
  geom_text(data = bridge_long_gene,
            aes(x = x_pos, y = (n_rows + 1) - row_num, label = label,
                colour = colour),
            hjust = 0.5, size = 1.75, fontface = "bold") +
  scale_colour_identity() +
  scale_x_continuous(limits = c(0, 1), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0.2, n_rows + 1.2), expand = c(0, 0)) +
  nature_theme() +
  theme(
    axis.line   = element_blank(),
    axis.ticks  = element_blank(),
    axis.text   = element_blank(),
    axis.title  = element_blank(),
    panel.background = element_rect(fill = "white", colour = "grey80", linewidth = 0.4)
  ) +
  labs(tag = "c",
       title = "Cross-species molecular bridges: human MR loci mapped to animal Sweet Trap homologs") +
  theme(plot.title = element_text(size = 6.5, face = "bold",
                                  margin = margin(b = 2)))

## ============================================================
## COMPOSE — 180 mm × 200 mm
## Panel A: 65%, Panel B: 18%, Panel C: 17%
## ============================================================

fig6 <- pA / pB / pC +
  plot_layout(heights = c(6.5, 2.0, 1.8)) &
  theme(plot.margin = margin(3, 4, 3, 4, "pt"))

## ============================================================
## SAVE
## ============================================================

out_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main"

ggsave(
  filename = file.path(out_dir, "fig4_mr_layer_D.png"),
  plot     = fig6,
  width    = 180, height = 200, units = "mm",
  dpi      = 300, bg = "white"
)

ggsave(
  filename = file.path(out_dir, "fig4_mr_layer_D.pdf"),
  plot     = fig6,
  width    = 180, height = 200, units = "mm",
  device   = cairo_pdf
)

message("Figure 4 saved: fig4_mr_layer_D.png + .pdf")
