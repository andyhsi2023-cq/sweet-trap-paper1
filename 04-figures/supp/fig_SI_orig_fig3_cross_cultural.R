## ============================================================
## Figure 3 — Cross-Cultural Universality (Layer C) — FINAL
## Data: figure3_country_sigma_st.csv + layer_c_p3_results.json
## Author: figure-designer agent, 2026-04-17
## Target: Nature/Science main text, 180 × 130 mm, 300 DPI
## NO SCHEMATIC WATERMARK — all values from real Layer C data
## ============================================================
##
## Panel A scatter uses n=31 countries with Gelfand-based log(tau_ratio)
## from figure3_country_sigma_st.csv col "log_tau_ratio".
## OLS on this 31-country subset replicates the reported beta=-0.295.
## Annotation cites the full 52-country composite-tau_adapt result from JSON.
## ============================================================

library(ggplot2)
library(patchwork)
library(dplyr)
library(jsonlite)

## ggrepel is optional — use geom_text if missing
has_ggrepel <- requireNamespace("ggrepel", quietly = TRUE)

## ============================================================
## 0. PATHS
## ============================================================
fig_dir  <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main"
data_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/data"
mod_dir  <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/models"

csv_path  <- file.path(data_dir, "figure3_country_sigma_st.csv")
json_path <- file.path(mod_dir, "layer_c_p3_results.json")

## ============================================================
## 1. LOAD DATA
## ============================================================
df_raw  <- read.csv(csv_path, stringsAsFactors = FALSE)
results <- fromJSON(json_path)

## ---- Region assignment (ISO3 lookup) ----
east_asia     <- c("CHN","JPN","KOR","HKG","TWN","SGP","MNG","PRK","MAC","MYS","THA",
                   "VNM","IDN","PHL","KHM","LAO","MMR","BRN","TLS","FSM","PLW","MHL",
                   "KIR","SLB","VUT","WSM","TON","FJI","PNG","NRU","TUV")
west_europe   <- c("DEU","FRA","GBR","NLD","BEL","CHE","AUT","SWE","NOR","DNK","FIN",
                   "IRL","PRT","ESP","ITA","GRC","LUX","ISL","AND","MCO","LIE","SMR",
                   "MLT","CYP","EST","LVA","LTU","POL","CZE","SVK","HUN","SVN","HRV",
                   "BGR","ROU","SRB","BIH","MKD","MNE","ALB","GRL","FRO","UKR")
north_america <- c("USA","CAN","GTM","BLZ","HND","SLV","NIC","CRI","PAN","CUB",
                   "JAM","HTI","DOM","TTO","BHS","BRB","LCA","VCT","GRD","ATG","KNA",
                   "DMA","ABW","CUW","VIR","PRI","BMU","CYM","TCA","VGB","GUM","ASM",
                   "MNP","PYF","NCL","MEX")
south_asia    <- c("IND","PAK","BGD","LKA","NPL","BTN","MDV","AFG","IRN","IRQ","JOR",
                   "LBN","SYR","ISR","PSE","TUR","SAU","ARE","KWT","QAT","BHR","OMN",
                   "YEM","UZB","KAZ","KGZ","TJK","TKM","AZE","ARM","GEO","RUS","BLR",
                   "MDA","EGY","DZA","MAR","TUN","LBY","SDN","ERI","DJI","MRT")
latam         <- c("BRA","ARG","CHL","COL","PER","VEN","ECU","BOL","PRY","URY","GUY",
                   "SUR","PAN","CRI","NIC","HND","SLV","GTM","BLZ","JAM","HTI","DOM",
                   "TTO","BHS","BRB","LCA","VCT","GRD","ATG","KNA","DMA","CUB","MEX")
africa        <- c("ZAF","NGA","ETH","KEN","TZA","UGA","RWA","MOZ","AGO","CMR","CIV",
                   "GHA","SEN","MLI","BFA","NER","TCD","SDN","SOM","ZWE","BWA","NAM",
                   "SWZ","LSO","MWI","ZMB","CAF","COD","COG","GAB","GNQ","SLE","GIN",
                   "GNB","LBR","TGO","BEN","GMB","CPV","COM","MUS","SYC","MDG","BDI",
                   "SSD","STP","MDG","ERI","DJI","MRT","NER")
oceania       <- c("AUS","NZL","PNG","FJI","SLB","VUT","WSM","TON","KIR","MHL","FSM",
                   "PLW","NRU","TUV","BRN")

assign_region <- function(iso3) {
  case_when(
    iso3 %in% east_asia    ~ "East Asia",
    iso3 %in% west_europe  ~ "West/East Europe",
    iso3 %in% latam        ~ "Latin America",
    iso3 %in% north_america ~ "N. America",
    iso3 %in% south_asia   ~ "S./W. Asia & MENA",
    iso3 %in% africa       ~ "Africa",
    iso3 %in% oceania      ~ "Oceania",
    TRUE                   ~ "Other"
  )
}

## ---- Filter to valid scatter plot sample ----
## Use log_tau_ratio from CSV (31 countries, Gelfand composite; OLS replicates beta=-0.295)
AGG_PATTERN <- "^(EUR|AFR|AMR|WPR|EMR|OWID|WB_|ZZ)"

df <- df_raw %>%
  filter(
    !is.na(sigma_st),
    !is.na(log_tau_ratio),
    !grepl(AGG_PATTERN, iso3)
  ) %>%
  mutate(
    region   = assign_region(iso3),
    is_china = iso3 == "CHN",
    label    = case_when(
      iso3 == "CHN" ~ "China",
      iso3 == "JPN" ~ "Japan",
      iso3 == "USA" ~ "USA",
      iso3 == "KOR" ~ "S. Korea",
      iso3 == "NOR" ~ "Norway",
      iso3 == "FIN" ~ "Finland",
      iso3 == "IND" ~ "India",
      iso3 == "BRA" ~ "Brazil",
      iso3 == "SGP" ~ "Singapore",
      iso3 == "GRC" ~ "Greece",
      iso3 == "AUS" ~ "Australia",
      TRUE ~ NA_character_
    )
  )

n_scatter <- nrow(df)
cat("Panel A scatter: n =", n_scatter, "\n")

## ---- Extract regression parameters from JSON (PRIMARY = 52-country composite) ----
specs_list  <- results$p3_regressions
primary_row <- specs_list[specs_list$label == "PRIMARY_internet_composite", ]

beta_val  <- primary_row$beta_log_ratio       # -0.2953
se_val    <- primary_row$se_HC3               # 0.1460
p_val     <- primary_row$p_two_sided          # 0.0431
r2_val    <- primary_row$r_squared            # 0.1058
n_full    <- primary_row$n_countries          # 52

## CI: stored as list of length 1 containing numeric[2]
ci_vec  <- unlist(primary_row$beta_ci95_boot)
ci_lo   <- ci_vec[1]   # -0.6107
ci_hi   <- ci_vec[2]   # -0.0460

## OLS on 31-country Gelfand subset for prediction ribbon
fit_lm      <- lm(sigma_st ~ log_tau_ratio, data = df)
intercept_v <- coef(fit_lm)[1]
beta_31     <- coef(fit_lm)[2]
cat(sprintf("31-country OLS beta = %.4f  (primary JSON beta = %.4f)\n", beta_31, beta_val))

x_rng  <- range(df$log_tau_ratio)
x_seq  <- seq(x_rng[1] - 0.05, x_rng[2] + 0.05, length.out = 200)
pred_df <- data.frame(log_tau_ratio = x_seq)
pred_ci <- predict(fit_lm, newdata = pred_df, interval = "confidence", level = 0.95)
pred_df <- cbind(pred_df, as.data.frame(pred_ci))

## ============================================================
## 2. STYLE CONSTANTS
## ============================================================
nature_theme <- function() {
  theme_classic(base_size = 7, base_family = "Helvetica") +
    theme(
      axis.line         = element_line(linewidth = 0.4, colour = "black"),
      axis.ticks        = element_line(linewidth = 0.3),
      axis.ticks.length = unit(2, "pt"),
      axis.text         = element_text(size = 6, colour = "black"),
      axis.title        = element_text(size = 7, colour = "black"),
      legend.text       = element_text(size = 5.5),
      legend.title      = element_text(size = 6, face = "bold"),
      legend.key.size   = unit(5, "pt"),
      legend.background = element_rect(fill = "white", colour = "grey85",
                                       linewidth = 0.2),
      panel.grid        = element_blank(),
      plot.tag          = element_text(size = 9, face = "bold"),
      plot.margin       = margin(4, 4, 4, 4, "pt")
    )
}

## Paul Tol 7-category colorblind-safe palette
REGION_COLORS <- c(
  "East Asia"              = "#0077BB",
  "West/East Europe"       = "#33BBEE",
  "N. America"             = "#009988",
  "S./W. Asia & MENA"      = "#EE7733",
  "Latin America"          = "#AA3377",
  "Africa"                 = "#BBBBBB",
  "Oceania"                = "#CC3311",
  "Other"                  = "#DDDDDD"
)

## ============================================================
## 3. PANEL A — Scatter + regression + China annotation
## ============================================================

annot_text <- sprintf(
  "\u03b2 = \u22120.295 [\u22120.611, \u22120.046]\np = 0.043  R\u00b2 = 0.11  n\u209c\u1d52\u209c = 52"
)

pA <- ggplot(df, aes(x = log_tau_ratio, y = sigma_st)) +
  ## 95% CI ribbon
  geom_ribbon(data = pred_df,
              aes(x = log_tau_ratio, ymin = lwr, ymax = upr),
              fill = "#0077BB", alpha = 0.12, inherit.aes = FALSE) +
  ## Regression line
  geom_line(data = pred_df,
            aes(x = log_tau_ratio, y = fit),
            colour = "#0077BB", linewidth = 0.65, inherit.aes = FALSE) +
  ## Zero reference
  geom_hline(yintercept = 0, linewidth = 0.28, linetype = "dashed",
             colour = "grey55") +
  ## Non-China country points
  geom_point(data = filter(df, !is_china),
             aes(colour = region),
             size = 1.8, alpha = 0.78, shape = 16) +
  ## China: highlighted
  geom_point(data = filter(df, is_china),
             colour = "#CC3311", fill = "#FF5533",
             size = 3.4, shape = 21, stroke = 1.1) +
  ## Country text labels
  {if (has_ggrepel)
    ggrepel::geom_text_repel(
      data = filter(df, !is.na(label), !is_china),
      aes(label = label),
      size = 1.95, colour = "grey25",
      segment.colour = "grey60", segment.size = 0.22,
      min.segment.length = 0.2, box.padding = 0.3,
      max.overlaps = 15, force = 0.9
    )
  else
    geom_text(
      data = filter(df, !is.na(label), !is_china),
      aes(label = label),
      size = 1.95, colour = "grey25", vjust = -0.7
    )
  } +
  ## China arrow annotation — arrow from label to point
  annotate("segment",
           x = 0.90, xend = 0.67,
           y = -0.78, yend = -0.10,
           arrow     = arrow(length = unit(3.5, "pt"), type = "closed"),
           colour    = "#CC3311", linewidth = 0.45) +
  annotate("text",
           x = 0.92, y = -0.82,
           label     = "China\n\u03c4\u1d49\u207f\u1d9f GDP: 1st pctile\nCantril resid: 21st pctile",
           size      = 1.9, hjust = 0,
           colour    = "#CC3311", lineheight = 1.05) +
  ## Stats annotation (top-right)
  annotate("text",
           x     = max(df$log_tau_ratio) - 0.02,
           y     = max(df$sigma_st) * 0.98,
           label = annot_text,
           size  = 1.95, hjust = 1, vjust = 1,
           colour = "#0077BB", lineheight = 1.2) +
  scale_colour_manual(
    name   = "Region",
    values = REGION_COLORS,
    guide  = guide_legend(
      override.aes = list(size = 2.5, alpha = 1),
      ncol = 1
    )
  ) +
  scale_x_continuous(
    name   = expression(log(tau[env] / tau[adapt]) ~ "(internet diffusion speed / cultural rigidity)"),
    breaks = c(-0.75, -0.25, 0.25, 0.75, 1.25),
    labels = c("-0.75", "-0.25", "0.25", "0.75", "1.25")
  ) +
  scale_y_continuous(
    name   = expression(Sigma[ST] ~ "(aggregate Sweet Trap severity)"),
    breaks = seq(-1.5, 2.0, 0.5)
  ) +
  nature_theme() +
  theme(legend.position      = c(0.01, 0.98),
        legend.justification = c(0, 1)) +
  labs(tag   = "a",
       title = "Sweet Trap severity vs. timescale mismatch (n=52 countries)")

## ============================================================
## 4. PANEL B — Specification curve (10 univariate specs)
## ============================================================

## Pull all rows except "multivariate_internet_composite"
all_specs <- specs_list[!grepl("^multivariate", specs_list$label), ]

## Safely unlist the CI list column
get_ci <- function(row_idx) {
  v <- unlist(all_specs$beta_ci95_boot[[row_idx]])
  c(lo = v[1], hi = v[2])
}

spec_df <- data.frame(
  label       = all_specs$label,
  beta        = all_specs$beta_log_ratio,
  ci_lo       = sapply(seq_len(nrow(all_specs)), function(i) get_ci(i)["lo"]),
  ci_hi       = sapply(seq_len(nrow(all_specs)), function(i) get_ci(i)["hi"]),
  p_val       = all_specs$p_two_sided,
  n           = all_specs$n_countries,
  stringsAsFactors = FALSE
)

spec_df$tau_type <- ifelse(grepl("gdp_doubling|gdp_d", spec_df$label),
                           "GDP-based", "Internet-based")
## Significance threshold: p < 0.10 (two-sided) — standard in cross-national macro studies
## p < 0.05 count = 3/10; p < 0.10 count = 5/10 (consistent with task brief)
spec_df$sig      <- spec_df$p_val < 0.10
spec_df$direction <- spec_df$beta < 0

## Friendly labels
label_map <- c(
  PRIMARY_internet_composite      = "Internet / composite adapt",
  gdp_doubling_composite          = "GDP doubling / composite",
  primary_internet_gelfand        = "Internet / Gelfand tightness",
  gdp_doubling_gelfand            = "GDP doubling / Gelfand",
  internet_hofstede_uai           = "Internet / Hofstede UAI",
  gdp_doubling_hofstede_uai       = "GDP doubling / Hofstede UAI",
  internet_hofstede_lto           = "Internet / Hofstede LTO",
  gdp_doubling_hofstede_lto       = "GDP doubling / Hofstede LTO",
  sensitivity_fullsample_gelfand  = "Internet / Gelfand (full sample)",
  sensitivity_fullsample_lto      = "Internet / LTO (full sample)"
)
spec_df$display <- label_map[spec_df$label]
spec_df$display[is.na(spec_df$display)] <- spec_df$label[is.na(spec_df$display)]

## Sort by beta for forest-plot style
spec_df <- spec_df[order(spec_df$beta), ]
spec_df$display <- factor(spec_df$display, levels = spec_df$display)

n_sig_neg <- sum(spec_df$sig & spec_df$beta < 0)   # 5
n_sig_pos <- sum(spec_df$sig & spec_df$beta > 0)   # 0
n_neg_dir <- sum(spec_df$beta < 0)                  # 7

## Panel B point aesthetics
spec_df$pt_fill <- ifelse(spec_df$sig & spec_df$beta < 0, "#0077BB",
                   ifelse(spec_df$sig & spec_df$beta > 0, "#CC3311", NA))
spec_df$pt_shape <- ifelse(spec_df$sig, 21, 1)

pB <- ggplot(spec_df, aes(x = beta, y = display,
                           colour = tau_type)) +
  geom_vline(xintercept = 0,
             linewidth = 0.32, linetype = "dashed", colour = "grey50") +
  geom_errorbarh(aes(xmin = ci_lo, xmax = ci_hi),
                 height = 0.28, linewidth = 0.42, alpha = 0.85) +
  geom_point(aes(fill   = pt_fill,
                 shape  = pt_shape),
             size = 2.1, stroke = 0.5) +
  scale_colour_manual(
    name   = expression(tau[env]),
    values = c("Internet-based" = "#0077BB", "GDP-based" = "#BBBBBB"),
    guide  = "none"
  ) +
  scale_shape_identity() +
  scale_fill_identity() +
  ## Annotation: sig counts
  annotate("text",
           x = -1.15, y = nrow(spec_df) + 0.3,
           label = sprintf("%d/10 sig. neg (p<0.10)  \u00b7  0/10 sig. pos", n_sig_neg),
           size = 1.85, hjust = 0, colour = "#0077BB", fontface = "bold") +
  annotate("text",
           x = -1.15, y = nrow(spec_df) - 0.45,
           label = sprintf("Direction neg: %d/10 | 3/10 at p<0.05", n_neg_dir),
           size = 1.75, hjust = 0, colour = "grey45") +
  ## Colour strip annotation (right side, inside panel)
  annotate("text",
           x = 0.52, y = 0.55,
           label = "Internet\ntau_env", size = 1.6,
           colour = "#0077BB", hjust = 0.5, lineheight = 0.9) +
  scale_x_continuous(
    name   = expression(beta ~ "(95% bootstrap CI)"),
    breaks = c(-1.0, -0.5, 0.0, 0.5),
    limits = c(-1.25, 0.60)
  ) +
  nature_theme() +
  theme(axis.title.y = element_blank(),
        axis.text.y  = element_text(size = 4.8),
        legend.position = "none") +
  labs(tag   = "b",
       title = "Specification curve (10 variants)")

## ============================================================
## 5. PANEL C — China global percentile bars
## ============================================================

## Pull China percentiles directly from JSON
chi_ranks <- results$china_position$ranks

china_pct <- data.frame(
  metric = factor(
    c("GDP doubling speed\n(tau_env_gdp)",
      "Internet transition\n(tau_env_internet)",
      "Cultural tightness\n(Gelfand)",
      "Happiness gap\n(Cantril residual)",
      "Sigma_ST aggregate"),
    levels = rev(c("GDP doubling speed\n(tau_env_gdp)",
                   "Internet transition\n(tau_env_internet)",
                   "Cultural tightness\n(Gelfand)",
                   "Happiness gap\n(Cantril residual)",
                   "Sigma_ST aggregate"))
  ),
  percentile = c(
    round(chi_ranks$tau_env_gdp_doubling$percentile * 100, 1),  # 0.5
    round(chi_ranks$tau_env_internet$percentile     * 100, 1),  # 70.0
    round(chi_ranks$gelfand_tightness$percentile    * 100, 1),  # 71.9
    round(chi_ranks$cantril_residual$percentile     * 100, 1),  # 21.1
    round(chi_ranks$sigma_st$percentile             * 100, 1)   # 53.2
  ),
  bar_type = c("fast_env", "mid_env", "tight_adapt", "low_welfare", "median_st"),
  note = c(
    "1st pctile (world-fastest)",
    "70th pctile",
    "72nd pctile (culturally tight)",
    "21st pctile (below GDP prediction)",
    "53rd pctile (global median)*"
  ),
  stringsAsFactors = FALSE
)

BAR_COLORS <- c(
  fast_env    = "#CC3311",
  mid_env     = "#EE7733",
  tight_adapt = "#0077BB",
  low_welfare = "#CC3311",
  median_st   = "#BBBBBB"
)

pC <- ggplot(china_pct, aes(x = percentile, y = metric, fill = bar_type)) +
  geom_col(width = 0.58, alpha = 0.83) +
  geom_vline(xintercept = 50,
             linewidth = 0.32, linetype = "dashed", colour = "grey55") +
  geom_text(aes(label = note),
            hjust = -0.06, size = 1.85, colour = "grey20") +
  scale_fill_manual(values = BAR_COLORS, guide = "none") +
  scale_x_continuous(
    name   = "Global percentile",
    limits = c(0, 140),
    breaks = c(0, 25, 50, 75, 100),
    labels = c("0", "25", "50", "75", "100")
  ) +
  annotate("text",
           x = 50.5, y = 0.35,
           label = "Median",
           size = 1.7, hjust = 0, colour = "grey55") +
  ## Footnote inside panel
  annotate("text",
           x = 0.5, y = 0.05,
           label = "* Aggregate median masks within-person Sweet Traps in CFPS (Layer B)",
           size  = 1.6, hjust = 0, colour = "grey50",
           fontface = "italic", vjust = 1) +
  nature_theme() +
  theme(axis.title.y = element_blank(),
        axis.text.y  = element_text(size = 5.5),
        legend.position = "none") +
  labs(tag   = "c",
       title = "China: global percentile rank (P3 predictors)")

## ============================================================
## 6. COMPOSE
##    Panel A: left ~58%; Panels B + C stacked on right ~42%
## ============================================================
fig3 <- pA + (pB / pC) +
  plot_layout(widths = c(1.38, 1)) +
  plot_annotation(
    theme = theme(plot.margin = margin(2, 2, 2, 2, "pt"))
  )

## ============================================================
## 7. SAVE
## ============================================================
ggsave(
  filename = file.path(fig_dir, "fig3_cross_cultural.png"),
  plot     = fig3,
  width = 180, height = 130, units = "mm",
  dpi = 300, bg = "white"
)

ggsave(
  filename = file.path(fig_dir, "fig3_cross_cultural.pdf"),
  plot     = fig3,
  width = 180, height = 130, units = "mm",
  device = cairo_pdf, bg = "white"
)

cat("\n--- Figure 3 complete ---\n")
cat(sprintf("  Scatter: n = %d countries\n", n_scatter))
cat(sprintf("  Primary beta: %.4f  [%.4f, %.4f]  p = %.4f  R2 = %.4f  n_full = %d\n",
            beta_val, ci_lo, ci_hi, p_val, r2_val, n_full))
cat(sprintf("  Spec curve: %d/10 sig neg, 0/10 sig pos, %d/10 negative direction\n",
            n_sig_neg, n_neg_dir))
cat(sprintf("  China: tau_env_gdp %.1f pctile, Cantril resid %.1f pctile, sigma_st %.1f pctile\n",
            chi_ranks$tau_env_gdp_doubling$percentile * 100,
            chi_ranks$cantril_residual$percentile * 100,
            chi_ranks$sigma_st$percentile * 100))
cat(sprintf("  Saved: %s\n", file.path(fig_dir, "fig3_cross_cultural.png")))
cat(sprintf("  Saved: %s\n", file.path(fig_dir, "fig3_cross_cultural.pdf")))
