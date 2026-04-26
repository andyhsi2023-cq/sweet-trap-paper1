## figS1_optimizer_diagnostic.R
## Supplementary Figure S1 — codeml optimiser-boundary diagnostic
## Sweet Trap v4 Paper 1 (C-path)
## Layout : 180 × 120 mm, 600 dpi, Okabe-Ito palette
## Outputs: FigS1_optimizer_diagnostic.{pdf,png,svg}
## Run    : Rscript --vanilla --no-init-file figS1_optimizer_diagnostic.R
## Author : figure-designer agent, 2026-04-25

suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(dplyr)
  library(scales)
  library(grid)        # for grob manipulation
})

# ── 0. paths ──────────────────────────────────────────────────────────────────
data_path      <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/outputs/optimizer_diagnostic.csv"
data_path_apis <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/outputs/apis_optimizer_diagnostic.csv"
out_dir        <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures"

# ── 1. load & tidy ────────────────────────────────────────────────────────────
raw_main <- read.csv(data_path, stringsAsFactors = FALSE)
raw_apis <- read.csv(data_path_apis, stringsAsFactors = FALSE)

# Harmonise schema if needed (apis has p2a_p2b column, main has p_2a+2b or similar);
# we only use clade, omega_start, lnL_alt, LRT, omega_2a, status, verdict downstream.
keep_cols <- c("clade", "omega_start", "lnL_alt", "LRT", "omega_2a", "status", "verdict")
raw <- rbind(raw_main[, keep_cols], raw_apis[, keep_cols])

clade_key <- c(
  "Gr_sweet__aaegypti_clade"      = "Aedes aegypti",
  "Gr_sweet__coleoptera_clade"    = "Coleoptera",
  "Gr_sweet__dmel_all_clade"      = "D. mel. all-Grs",
  "Gr_sweet__dmel_Gr64_cluster"   = "D. mel. Gr64 cluster",
  "Gr_sweet__lepidoptera_clade"   = "Lepidoptera",
  "Gr_sweet__amellifera_clade"    = "Apis mellifera"
)
alpha_order <- sort(unname(clade_key))

verdict_map <- raw %>%
  distinct(clade, verdict) %>%
  mutate(
    clade_label = clade_key[clade],
    verdict     = ifelse(verdict == "APIS_OPTIMIZER_ARTIFACT", "OPTIMIZER_ARTIFACT", verdict)
  ) %>%
  select(clade_label, verdict)

df <- raw %>%
  mutate(
    clade_label   = factor(clade_key[clade], levels = alpha_order),
    omega_start_f = factor(omega_start, levels = c(0.1, 0.5, 1.0, 2.0, 5.0)),
    LRT_val  = ifelse(status == "timeout", NA_real_, LRT),
    LRT_val  = ifelse(!is.na(LRT_val) & abs(LRT_val) < 1e-3, 0, LRT_val),
    LRT_clip = pmin(LRT_val, 10, na.rm = FALSE),
    cell_lbl = case_when(
      status == "timeout" ~ "NA",
      is.na(LRT_val)      ~ "NA",
      TRUE                ~ sprintf("%.2f", LRT_val)
    ),
    # Escape cells:
    #   - status=="escaped" : LRT-positive escape (existing dmel diagnostic)
    #   - clade=="Gr_sweet__amellifera_clade" & omega_start==5.0 : Apis sub-null escape
    #   - clade=="Gr_sweet__amellifera_clade" & omega_start!=5.0 : production-basin convergence
    #     (highlight 4/5 starts as the production basin too — they confirm but are not "escapes")
    escape_cell    = (status == "escaped"),
    apis_subnull   = (clade == "Gr_sweet__amellifera_clade" &
                      abs(as.numeric(omega_start) - 5.0) < 1e-6)
  )

# ── 2. colour constants (Okabe-Ito) ───────────────────────────────────────────
oi6 <- c(
  "Aedes aegypti"        = "#0072B2",
  "Apis mellifera"       = "#F0E442",
  "Coleoptera"           = "#E69F00",
  "D. mel. all-Grs"      = "#009E73",
  "D. mel. Gr64 cluster" = "#CC79A7",
  "Lepidoptera"          = "#56B4E9"
)
tag_col <- c("TRUE_NULL" = "#009E73", "OPTIMIZER_ARTIFACT" = "#D55E00")

# ── 3. y-axis colour lookup for Panel A ───────────────────────────────────────
# We colour each y-axis tick label by its verdict
y_axis_colours <- sapply(alpha_order, function(cl) {
  v <- verdict_map$verdict[verdict_map$clade_label == cl]
  tag_col[v]
})
names(y_axis_colours) <- alpha_order

# ── 4. Panel A — 6×5 LRT heatmap ─────────────────────────────────────────────
escape_df       <- df %>% filter(escape_cell)
apis_subnull_df <- df %>% filter(apis_subnull)

# Build y-axis labels: "Clade name [verdict]" where verdict part is shown
# via axis tick colouring. We add a small square bracket suffix to encode class.
verdict_suffix <- sapply(alpha_order, function(cl) {
  v <- verdict_map$verdict[verdict_map$clade_label == cl]
  if (v == "TRUE_NULL") " [NULL]" else " [ART.]"
})
y_labels_with_tag <- paste0(alpha_order, verdict_suffix)
names(y_labels_with_tag) <- alpha_order

pA <- ggplot(df, aes(x = omega_start_f, y = clade_label)) +
  geom_tile(aes(fill = LRT_clip), colour = "white", linewidth = 0.35) +
  # dmel boundary escapes (positive LRT > 1.0) — orange border
  geom_tile(data = escape_df,
            aes(x = omega_start_f, y = clade_label),
            fill = NA, colour = "#D55E00", linewidth = 1.3) +
  # Apis sub-null escape (ω₀=5.0 only, LRT = -2.48) — magenta dashed border
  geom_tile(data = apis_subnull_df,
            aes(x = omega_start_f, y = clade_label),
            fill = NA, colour = "#CC0033", linewidth = 1.3, linetype = "dashed") +
  geom_text(aes(label = cell_lbl,
                colour = ifelse(!is.na(LRT_clip) & LRT_clip >= 4, "w", "d")),
            size = 2.1, family = "sans") +
  scale_colour_manual(values = c(d = "grey15", w = "white"), guide = "none") +
  scale_fill_gradientn(
    name    = "LRT",
    colours = c("#EBEBEB", "#FDE9C9", "#E69F00", "#D55E00", "#A50026"),
    values  = rescale(c(0, 0.01, 1, 5, 10)),
    limits  = c(0, 10),
    na.value = "#CCCCCC",
    guide   = guide_colourbar(
      barwidth   = 0.45,
      barheight  = 2.6,
      title.position = "top",
      title.hjust    = 0.5,
      ticks.colour   = "grey50"
    )
  ) +
  scale_x_discrete(expand = expansion(add = c(0.5, 0.5))) +
  scale_y_discrete(
    expand = expansion(add = c(0.5, 0.5)),
    labels = y_labels_with_tag
  ) +
  labs(x = expression(omega[0]~"start"), y = NULL) +
  theme_minimal(base_size = 7, base_family = "sans") +
  theme(
    axis.text.x      = element_text(size = 6.2),
    axis.text.y      = element_text(size = 5.8, face = "italic", hjust = 1,
                                    colour = y_axis_colours[alpha_order]),
    axis.title.x     = element_text(size = 7),
    panel.grid       = element_blank(),
    plot.margin      = margin(4, 4, 4, 4, "pt"),
    legend.position  = "right",
    legend.title     = element_text(size = 6),
    legend.text      = element_text(size = 5.5),
    legend.box.margin = margin(0, 0, 0, -2, "pt")
  )

# ── 5. Panel B — foreground ω₂ₐ vs ω₀ start (log-x) ─────────────────────────
df_B <- df %>%
  filter(status != "timeout") %>%
  mutate(omega_start_num = as.numeric(as.character(omega_start)))

escape_B <- df_B %>%
  filter(escape_cell | apis_subnull) %>%
  mutate(ann_label = paste0(clade_label, "\nω₂ₐ=", round(omega_2a, 1)))

pB <- ggplot(df_B, aes(x = omega_start_num, y = omega_2a,
                        colour = clade_label, group = clade_label)) +
  annotate("rect",
           xmin = -Inf, xmax = Inf,
           ymin = 30, ymax = 200,
           fill = "grey80", alpha = 0.30) +
  annotate("text",
           x = 0.07, y = 105,
           label = "Small-clade\nboundary-artefact\nrange\n(Anisimova &\nYang 2007)",
           hjust = 0, vjust = 0.5,
           size = 1.7, colour = "grey45",
           fontface = "italic", lineheight = 1.2,
           family = "sans") +
  geom_hline(yintercept = 1.0, linetype = "dashed",
             colour = "grey55", linewidth = 0.4) +
  annotate("text", x = 5.2, y = 1.0,
           label = "ω = 1.0 (boundary)",
           hjust = 1, vjust = -0.35,
           size = 1.75, colour = "grey50", family = "sans") +
  geom_line(linewidth = 0.55, alpha = 0.88) +
  geom_point(data = df_B %>% filter(!escape_cell),
             size = 1.3, shape = 16) +
  geom_point(data = escape_B,
             aes(x = omega_start_num, y = omega_2a),
             size = 2.8, shape = 21, stroke = 0.9,
             colour = "#D55E00", fill = NA) +
  geom_text(data = escape_B,
            aes(x = omega_start_num, y = omega_2a, label = ann_label),
            hjust  = 1.10, vjust = 0.5,
            size   = 1.7, colour = "#D55E00",
            fontface = "italic", lineheight = 1.15,
            family = "sans") +
  scale_x_log10(
    breaks = c(0.1, 0.5, 1.0, 2.0, 5.0),
    labels = c("0.1", "0.5", "1.0", "2.0", "5.0"),
    limits = c(0.055, 7)
  ) +
  scale_y_continuous(
    limits = c(0, 210),
    breaks = c(0, 1, 50, 100, 150, 200),
    expand = expansion(mult = c(0.02, 0.02))
  ) +
  scale_colour_manual(
    name   = NULL,
    values = oi6,
    guide  = guide_legend(
      ncol = 1,
      keywidth  = unit(0.7, "cm"),
      keyheight = unit(0.22, "cm"),
      override.aes = list(linewidth = 0.9, size = 1.6)
    )
  ) +
  labs(
    x = expression(omega[0]~"start (log scale)"),
    y = expression("Foreground "*omega["2a"])
  ) +
  theme_minimal(base_size = 7, base_family = "sans") +
  theme(
    axis.text        = element_text(size = 6),
    axis.title       = element_text(size = 7),
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(colour = "grey92", linewidth = 0.28),
    legend.position  = "right",
    legend.text      = element_text(size = 5.2, face = "italic"),
    legend.title     = element_blank(),
    legend.key.size  = unit(0.26, "cm"),
    legend.spacing.y = unit(0.03, "cm"),
    plot.margin      = margin(4, 4, 4, 4, "pt")
  )

# ── 6. assemble ───────────────────────────────────────────────────────────────
CAPTION <- paste0(
  "Supplementary Figure S1 | Optimiser-boundary diagnostic for all six production clades ",
  "(Yang & dos Reis 2011): five LRT = 0 clades under the symmetric rule plus the *Apis mellifera* ",
  "Gr_sweet production-positive clade under the asymmetric rule (6 clades × 5 ω₀ starts = 30 codeml runs). ",
  "(A) Branch-site Model A LRT magnitude across 5 randomised starting values of ω₀. Three clades ",
  "(Aedes aegypti, Coleoptera, Lepidoptera) converge to the boundary (LRT = 0, ω₂ₐ = 1.0) at all five starts ",
  "and are classified TRUE_NULL [NULL]. Two clades (D. melanogaster Gr64 cluster, D. mel. all-Grs) escape ",
  "the boundary only at ω₀ = 5.0, with LRT = 9.68 and 4.33 respectively, and are classified ",
  "OPTIMIZER_ARTIFACT [ART.] — orange borders. The Apis Gr_sweet clade reproduces the production basin ",
  "(LRT = 9.92, ω₂ₐ = 36.18) at 4 of 5 starts but escapes to a sub-null basin at ω₀ = 5.0 ",
  "(LRT = −2.48, ω₂ₐ = 1.63 — alt model fits worse than null), classifying APIS_OPTIMIZER_ARTIFACT under ",
  "the asymmetric rule (any near-null escape, LRT < 1.0, on a production-positive clade) — magenta dashed border. ",
  "The NA cell (D. mel. Gr64 cluster, ω₀ = 2.0) is a 2-h codeml timeout. ",
  "(B) Recovered foreground ω₂ₐ as a function of ω₀ start. Both dmel escape points fall within the ",
  "small-clade boundary-artefact range (ω = 30–200; Anisimova & Yang 2007), and the Apis production ω₂ₐ = 36.2 ",
  "also lies in this range — all three non-zero escapes are consistent with optimiser sensitivity rather ",
  "than confirmed positive selection."
)

pA_tag <- pA + labs(tag = "A") +
  theme(plot.tag = element_text(size = 8, face = "bold", family = "sans"))
pB_tag <- pB + labs(tag = "B") +
  theme(plot.tag = element_text(size = 8, face = "bold", family = "sans"))

fig <- (pA_tag | pB_tag) +
  plot_layout(widths = c(11, 7)) +
  plot_annotation(
    caption = CAPTION,
    theme = theme(
      plot.caption    = element_text(size = 5.2, colour = "grey30",
                                     hjust = 0, lineheight = 1.28,
                                     margin = margin(t = 5, unit = "pt")),
      plot.background = element_rect(fill = "white", colour = NA)
    )
  ) &
  theme(plot.background = element_rect(fill = "white", colour = NA))

# ── 7. save ───────────────────────────────────────────────────────────────────
W   <- 180 / 25.4
H   <- 120 / 25.4
DPI <- 600

ggsave(file.path(out_dir, "FigS1_optimizer_diagnostic.pdf"),
       fig, width = W, height = H, device = cairo_pdf, bg = "white")
message("PDF written.")

ggsave(file.path(out_dir, "FigS1_optimizer_diagnostic.png"),
       fig, width = W, height = H, dpi = DPI, device = "png", bg = "white")
message("PNG written.")

ggsave(file.path(out_dir, "FigS1_optimizer_diagnostic.svg"),
       fig, width = W, height = H, device = "svg", bg = "white")
message("SVG written.")

# ── 8. sanity check ───────────────────────────────────────────────────────────
chk <- raw[raw$clade == "Gr_sweet__dmel_Gr64_cluster" & raw$omega_start == 5.0, ]
cat(sprintf(
  "\n[SANITY] dmel_Gr64_cluster, omega0=5.0 -> LRT=%.4f, omega2a=%.3f, status=%s\n",
  chk$LRT, chk$omega_2a, chk$status
))
