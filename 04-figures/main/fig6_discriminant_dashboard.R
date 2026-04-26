## ============================================================
## Figure 4 — Discriminant Validity Dashboard
## 5-panel: C2 jiwa | C4 Marriage | C6 Supplement | D3 996 | D_alcohol tripartite
## Shows construct BOUNDARIES — what is NOT a Sweet Trap
## Target: Science main, 180 mm double-column
## ============================================================

library(ggplot2)
library(patchwork)
library(dplyr)

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
null_col   <- "#888888"   ## grey for null/fail results

## ============================================================
## Panel A — C2 jiwa: F2 failure (SES gradient inverted)
## From C2_education_findings.md §3.2:
## cor(eexp_share, ln_income 2018) = -0.093
## Education quartile gradient: 0-6yr: 10.1%, 6-9yr: 9.7%, 9-12yr: 8.7%, 12+yr: 8.2%
## ============================================================
c2_f2_df <- data.frame(
  eduy_bracket = factor(
    c("0–6 yr", "6–9 yr", "9–12 yr", "12+ yr"),
    levels = c("0–6 yr", "6–9 yr", "9–12 yr", "12+ yr")
  ),
  eexp_share_mean = c(0.101, 0.097, 0.087, 0.082)
)

pA <- ggplot(c2_f2_df, aes(x = eduy_bracket, y = eexp_share_mean)) +
  geom_bar(stat = "identity", fill = null_col, alpha = 0.7, width = 0.65) +
  ## Arrow showing direction
  annotate("segment",
           x = 1.0, xend = 4.0, y = 0.104, yend = 0.079,
           arrow = arrow(length = unit(4, "pt"), type = "closed"),
           colour = tol_red, linewidth = 0.6) +
  annotate("text", x = 2.5, y = 0.108,
           label = "cor = −0.093  (F2 FAIL)", size = 1.9,
           colour = tol_red, hjust = 0.5, fontface = "bold") +
  ## Sweet Trap F2 expectation arrow (should be +)
  annotate("text", x = 0.6, y = 0.076,
           label = "Expected\nF2 ↑", size = 1.7, colour = "grey40", hjust = 0,
           fontface = "italic") +
  scale_y_continuous(
    name   = "Education spending share\n(eexp_share)",
    limits = c(0, 0.120),
    breaks = c(0.04, 0.06, 0.08, 0.10)
  ) +
  xlab("Parental education") +
  nature_theme() +
  labs(
    tag   = "a",
    title = "C2 jiwa: F2 fails — low-SES families\nbear higher education cost share"
  ) +
  theme(plot.title = element_text(size = 6.5, face = "bold", colour = tol_red))

## ============================================================
## Panel B — C4 Marriage: Δ_ST wrong sign (cohort decomposition)
## From C4_marriage_market_findings.md §5:
## life_sat: pre-reform cor = -0.022, reform-era cor = +0.018 -> Δ_ST = -0.039
## happy: -0.049 -> +0.026, Δ_ST = -0.075
## marital_sat: -0.031 -> +0.079, Δ_ST = -0.110
## ============================================================
c4_delta_df <- data.frame(
  dv       = factor(c("Life\nsatisfaction", "Happiness", "Marital\nsatisfaction"),
                    levels = c("Life\nsatisfaction", "Happiness", "Marital\nsatisfaction")),
  delta_st = c(-0.039, -0.075, -0.110),
  ci_lo    = c(-0.143, -0.190, -0.215),
  ci_hi    = c(+0.060, +0.034, -0.002)
)

pB <- ggplot(c4_delta_df, aes(x = dv, y = delta_st)) +
  geom_hline(yintercept = 0, linewidth = 0.4, colour = "grey60", linetype = "dashed") +
  ## Shaded "expected Sweet Trap" region (Δ_ST > 0)
  annotate("rect", xmin = 0.4, xmax = 3.6, ymin = 0, ymax = 0.25,
           fill = tol_blue, alpha = 0.07) +
  annotate("text", x = 3.55, y = 0.22,
           label = "Expected\nΔ_ST > 0", size = 1.7,
           colour = tol_blue, hjust = 1, fontface = "italic") +
  geom_errorbar(aes(ymin = ci_lo, ymax = ci_hi),
                width = 0.2, linewidth = 0.5, colour = null_col) +
  geom_point(size = 2.5, colour = null_col) +
  ## Annotate each point
  geom_text(aes(label = sprintf("%.3f", delta_st)),
            size = 1.8, vjust = 1.8, hjust = 0.5, colour = null_col) +
  scale_y_continuous(
    name   = expression(Delta[ST] ~ "(pre\u2192post reform)"),
    limits = c(-0.28, 0.28),
    breaks = c(-0.2, -0.1, 0, 0.1, 0.2)
  ) +
  scale_x_discrete(name = "Welfare DV") +
  nature_theme() +
  labs(
    tag   = "b",
    title = "C4 Marriage: Δ_ST wrong sign\n(measurement issue — payer side unobserved)"
  ) +
  theme(plot.title = element_text(size = 6.5, face = "bold", colour = null_col))

## ============================================================
## Panel C — C6 Supplement: θ null vs peer_β strong
## From C6_supplement_findings.md:
## θ (sweet within-FE): srh β = -0.0009 [−0.0064, +0.0045], null
## F3 peer: 10pp community heavy-use -> +7.3pp individual prob (β=+0.729)
## LDL bitter: ΔLDL = +0.771 [+0.306, +1.235]
## ============================================================
c6_sig_df <- data.frame(
  pathway   = factor(
    c("θ (sweet)\nwithin-FE β", "F3 peer\neffect β", "Bitter\nΔLDL β"),
    levels = c("θ (sweet)\nwithin-FE β", "F3 peer\neffect β", "Bitter\nΔLDL β")
  ),
  estimate = c(-0.0009, 0.729, 0.771),
  ci_lo    = c(-0.0064, 0.700, 0.306),
  ci_hi    = c(+0.0045, 0.758, 1.235),
  colour_id = c("null", "positive", "positive")
)

## Scale all to % of max for comparable display (different units)
## Actually show as separate sub-bar chart with unit annotation
pC <- ggplot(c6_sig_df, aes(x = pathway, y = estimate, fill = colour_id)) +
  geom_hline(yintercept = 0, linewidth = 0.35, colour = "grey60", linetype = "dashed") +
  geom_errorbar(aes(ymin = ci_lo, ymax = ci_hi),
                width = 0.2, linewidth = 0.5,
                colour = ifelse(c6_sig_df$colour_id == "null", null_col, tol_teal)) +
  geom_point(aes(colour = colour_id), size = 2.5) +
  scale_colour_manual(values = c("null" = null_col, "positive" = tol_teal), guide = "none") +
  scale_fill_manual(values = c("null" = null_col, "positive" = tol_teal), guide = "none") +
  ## Mark null
  annotate("text", x = 1, y = 0.08,
           label = "ns", size = 2.0, colour = null_col, hjust = 0.5, fontface = "bold") +
  ## Mark significant
  annotate("text", x = 2, y = 0.80, label = "***", size = 2.5, colour = tol_teal, hjust = 0.5) +
  annotate("text", x = 3, y = 1.32, label = "**", size = 2.5, colour = tol_teal, hjust = 0.5) +
  ## Note: F3 and Bitter strong, but θ=null → incomplete Sweet Trap
  annotate("text", x = 0.55, y = -0.08,
           label = "θ absent", size = 1.7, colour = null_col, hjust = 0) +
  scale_y_continuous(
    name   = "Standardised effect size (mixed units)",
    limits = c(-0.10, 1.45),
    breaks = c(0, 0.3, 0.6, 0.9, 1.2)
  ) +
  xlab(NULL) +
  nature_theme() +
  labs(
    tag   = "c",
    title = "C6 Supplement: F3 & Bitter real, θ absent\n→ incomplete Sweet Trap signature"
  ) +
  theme(plot.title = element_text(size = 6.5, face = "bold", colour = null_col))

## ============================================================
## Panel D — D3 996: β wrong sign (Bitter without Sweet)
## From D3_996_findings.md:
## Sweet: β(overtime -> qg406) = -0.074 [-0.103, -0.044], p=1.000 (H3.1 falsified)
## Bitter: β(overtime -> chronic_disease_{t+1}) = +0.023 [-0.003, +0.049], p=0.040
## Spec curve: only 10.2% of 432 variants positive
## ============================================================
d3_df <- data.frame(
  test     = factor(
    c("Sweet\n(job satisfaction)", "Bitter\n(chronic disease t+1)"),
    levels = c("Sweet\n(job satisfaction)", "Bitter\n(chronic disease t+1)")
  ),
  estimate = c(-0.074, +0.023),
  ci_lo    = c(-0.103, -0.003),
  ci_hi    = c(-0.044, +0.049),
  expected = c(1, 1)   ## 1 = Sweet Trap expects positive for both; Sweet: +, Bitter: +
)

## Helper data for annotation on factor x-axis (pD)
d3_annot_df <- data.frame(
  test     = d3_df$test,
  expected = c(0.093, 0.093),
  note     = c("β = \u22120.074***\n(FALSIFIED)", "β = +0.023\u00b0\n(directional)"),
  note_y   = c(-0.090, -0.090),
  col_id   = c("red", "grey")
)

pD <- ggplot(d3_df, aes(x = test, y = estimate)) +
  geom_hline(yintercept = 0, linewidth = 0.4, colour = "grey60", linetype = "dashed") +
  ## "Expected +" labels above zero line
  geom_text(data = d3_annot_df, aes(x = test, y = expected, label = "Expected+"),
            size = 1.7, colour = tol_blue, hjust = 0.5, fontface = "italic") +
  geom_errorbar(aes(ymin = ci_lo, ymax = ci_hi, colour = test),
                width = 0.2, linewidth = 0.5) +
  geom_point(aes(colour = test), size = 2.5) +
  scale_colour_manual(values = c("Sweet\n(job satisfaction)" = tol_red,
                                  "Bitter\n(chronic disease t+1)" = null_col),
                      guide = "none") +
  ## Annotations using factor-mapped positions
  geom_text(data = d3_annot_df,
            aes(x = test, y = note_y, label = note,
                colour = col_id),
            size = 1.9, hjust = 0.5, fontface = ifelse(d3_annot_df$col_id == "red", "bold", "plain"),
            show.legend = FALSE, inherit.aes = FALSE) +
  scale_colour_manual(values = c("red" = tol_red, "grey" = null_col), guide = "none") +
  scale_y_continuous(
    name   = "\u03b2 coefficient (within-person FE)",
    limits = c(-0.14, 0.13),
    breaks = c(-0.10, -0.05, 0, 0.05, 0.10)
  ) +
  xlab(NULL) +
  nature_theme() +
  labs(
    tag   = "d",
    title = "D3 996 overwork: Bitter only, no Sweet\n\u2192 F1 falsification (coerced exposure)"
  ) +
  theme(plot.title = element_text(size = 6.5, face = "bold", colour = tol_red))

## ============================================================
## Panel E — D_alcohol: F2 tripartite diagnostic
## From D_alcohol_findings.md:
## Type A (aspirational): cor(type, ln_income)=+0.051, cor(type,edu)=+0.056 -> PASS
## Type C (dependent): cor(type, ln_income)=-0.045, cor(type,edu)=-0.068 -> FAIL
## Type A Sweet event study: Δsatlife = +0.14 (p=0.009); Bitter: absent (health selection)
## ============================================================
d_alc_df <- data.frame(
  type_group = factor(
    rep(c("Type A\n(aspirational)", "Type B\n(coerced)", "Type C\n(dependent)"), 2),
    levels = c("Type A\n(aspirational)", "Type B\n(coerced)", "Type C\n(dependent)")
  ),
  sos_var    = rep(c("Income", "Education"), each = 3),
  cor_val    = c(+0.051, +0.008, -0.045, +0.056, +0.023, -0.068)
)

pE <- ggplot(d_alc_df, aes(x = type_group, y = cor_val, fill = sos_var)) +
  geom_hline(yintercept = 0, linewidth = 0.35, colour = "grey60", linetype = "dashed") +
  geom_col(position = position_dodge(width = 0.65), width = 0.60, alpha = 0.85) +
  scale_fill_manual(
    name   = "SES var",
    values = c("Income" = tol_blue, "Education" = tol_cyan)
  ) +
  ## F2 pass/fail labels
  annotate("text", x = 1, y = 0.070, label = "F2 PASS", size = 1.8,
           colour = tol_teal, fontface = "bold", hjust = 0.5) +
  annotate("text", x = 2, y = 0.040, label = "marginal", size = 1.8,
           colour = null_col, fontface = "italic", hjust = 0.5) +
  annotate("text", x = 3, y = -0.080, label = "F2 FAIL", size = 1.8,
           colour = tol_red, fontface = "bold", hjust = 0.5) +
  ## Arrow: Type A -> F2 pass only enables Sweet Trap claim
  annotate("text", x = 0.58, y = -0.095,
           label = "Only Type A\nqualifies as\nSweet Trap",
           size = 1.6, colour = tol_teal, hjust = 0) +
  scale_y_continuous(
    name   = "cor(type membership, SES)",
    limits = c(-0.12, 0.09),
    breaks = c(-0.10, -0.05, 0, 0.05)
  ) +
  xlab("Alcohol consumer type") +
  nature_theme() +
  theme(
    legend.position = c(0.99, 0.99),
    legend.justification = c(1, 1),
    legend.background = element_rect(fill = NA, colour = NA)
  ) +
  labs(
    tag   = "e",
    title = "D_alcohol: F2 tripartite — only Type A shows\nSweet signature; Type C = F2 failure"
  ) +
  theme(plot.title = element_text(size = 6.5, face = "bold", colour = null_col))

## ============================================================
## Construct boundary summary strip
## ============================================================
boundary_df <- data.frame(
  domain  = factor(
    c("C2 jiwa", "C4 Marriage", "C6 Supplement", "D3 996", "D_alc Type C"),
    levels = c("C2 jiwa", "C4 Marriage", "C6 Supplement", "D3 996", "D_alc Type C")
  ),
  f1_pass = c(0, 0, 1, 1, 1),    ## 1=pass, 0=fail/wrong-sign
  f2_pass = c(0, 0, 1, 0, 0),
  f3_pass = c(0, 0, 1, 0, 1),
  verdict = c("Coerced\nexposure", "Measurement\nlimit", "Veblen\nconsumption",
              "Coerced\nexposure", "Addiction/\ndependency")
)

## Heatmap-style diagnostic grid
boundary_long <- boundary_df %>%
  tidyr::pivot_longer(cols = c(f1_pass, f2_pass, f3_pass),
                      names_to = "condition", values_to = "pass_fail") %>%
  mutate(condition = recode(condition,
                            f1_pass = "F1: Decoupling",
                            f2_pass = "F2: Endorsement",
                            f3_pass = "F3: Self-reinforcement"))

library(tidyr)
pStrip <- ggplot(boundary_long, aes(x = condition, y = domain, fill = factor(pass_fail))) +
  geom_tile(colour = "white", linewidth = 0.5) +
  scale_fill_manual(
    name   = NULL,
    values = c("0" = "#FFCCCC", "1" = "#CCE5FF"),
    labels = c("0" = "FAIL", "1" = "PASS")
  ) +
  geom_text(aes(label = ifelse(pass_fail == 1, "P", "F")),
            size = 2.4, fontface = "bold",
            colour = ifelse(boundary_long$pass_fail == 1, tol_blue, tol_red)) +
  xlab(NULL) +
  ylab(NULL) +
  nature_theme() +
  theme(
    axis.text.x = element_text(angle = 20, hjust = 1, size = 6),
    legend.position = "right",
    axis.line = element_blank(),
    axis.ticks = element_blank()
  ) +
  labs(title = "Construct boundary: F1–F3 diagnostic matrix") +
  theme(plot.title = element_text(size = 6.5, face = "bold"))

## ============================================================
## COMPOSE
## ============================================================
row1 <- pA | pB | pC
row2 <- pD | pE | pStrip

fig4 <- row1 / row2 + plot_layout(heights = c(1, 1))

## ============================================================
## SAVE
## ============================================================
out_dir <- "/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main"

ggsave(
  filename = file.path(out_dir, "fig6_discriminant_dashboard.png"),
  plot = fig4,
  width = 180, height = 155, units = "mm",
  dpi = 300, bg = "white"
)

ggsave(
  filename = file.path(out_dir, "fig6_discriminant_dashboard.pdf"),
  plot = fig4,
  width = 180, height = 155, units = "mm",
  device = cairo_pdf
)

message("Figure 6 saved (v3.3 fix: jiwa + P/F labels).")
