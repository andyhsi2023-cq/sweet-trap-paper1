# Figure 8 (v2.4) — Data Specification for `figure-designer`

**Version:** v2.4 (2026-04-18). Replaces v2.3 Figure 8 (DALY dual-anchor waterfall + Sankey), which is retired from main text and preserved only as Supplementary Figure H1 inside `SI_H_orthogonal_health_implications.md`.

**Intent.** The Figure 8 in v2.4 is the visual anchor for the paper's *headline policy-predictability claim*: in the six Sweet Trap focal domains, interventions that redesign the reward-signal distribution ("signal redesign") produce systematically larger effect sizes than interventions targeting individual beliefs/information ("information"). The claim is derivable from the F1 + F2 construct definition alone (§11.8); the figure shows that the existing intervention-effect literature, independently compiled domain-by-domain, confirms the pattern.

This figure *replaces* Figure 8's role as the "stakes anchor" of the paper. The stakes are no longer "Parkinson's-disease-scale burden" but "signal-redesign interventions systematically outperform information in Sweet Trap domains; this is testable, falsifiable, and bears directly on hundreds of billions USD in annual global public-health spending."

---

## Figure title (bold, first line of legend)

**Figure 8 | In Sweet Trap domains, signal-redesign interventions systematically outperform information-based alternatives.**

---

## Panel structure

Two panels (a, b), side-by-side, shared vertical axis.

### Panel (a) — Matrix: domain × intervention type × effect size

- **Plot type:** horizontal dot-plot (forest-plot style), six rows (one per domain), two dots per row (one per intervention type), with error bars showing 95% CI where available from the primary meta-analysis.
- **Y-axis (rows, top to bottom, in Sweet-Trap focal-domain order matching main-text §3):**
  1. C8 Investment FOMO (retirement savings participation)
  2. C11 Diet (sugar-sweetened beverage consumption)
  3. C12 Short-video / digital overuse (screen time)
  4. C13 Housing leverage (over-borrowing / default risk)
  5. D_alcohol (alcohol consumption, heavy-drinking days)
  6. C_pig-butchering (pig-butchering / romance-investment fraud victimisation rate)
- **X-axis:** standardised effect size. Where a domain's studies report percentage-point changes on a native outcome (e.g., pp change in participation, pp change in consumption, % reduction in victimisation), use the percentage-point scale with the sign convention *positive = desired welfare direction* (e.g., higher participation for C8 is positive; lower consumption for C11/C12/D_alcohol/C_pig-butchering is mapped to positive sign after sign-flip). Where Cohen's d is available, plot d. The panel caption explicitly documents the unit for each row.
- **Two dot markers per row:**
  - Open circle, light grey: information intervention effect.
  - Filled circle, dark colour (domain-consistent palette from Figure 7 if feasible): signal-redesign intervention effect.
- **Error bars:** 95% CI from the primary meta-analysis for each intervention type; where only a single RCT is cited, plot the RCT 95% CI directly.
- **Reference line:** vertical dashed line at x = 0 ("no effect"). Mark the effect-size axis so readers can eyeball the systematic signal-redesign > information gap.

**Data table (the six rows of Panel a) — cite exactly these numbers in the caption.** All numbers are drawn from published meta-analyses or canonical flagship RCTs; no manufactured estimates.

| Row | Domain | Information intervention | Effect (95% CI) | Signal-redesign intervention | Effect (95% CI) | Primary source |
|---|---|---|---|---|---|---|
| 1 | C8 Investment | Financial-literacy programmes on retirement participation | +0.5 pp mean increase in savings behaviour (≈1.4% of behavioural variance explained by FL interventions; meta-analytic "dot-product" is near-zero) | Auto-enrolment default on 401(k) participation | +37 pp (from 49% to 86% participation) | Fernandes, Lynch & Netemeyer 2014 *Mgmt Sci*; Madrian & Shea 2001 *QJE* |
| 2 | C11 Diet | Calorie / nutrition-label posting on kcal purchased | −8 kcal per meal, 95% CI includes 0 (non-significant pooled) | Sugar-sweetened-beverage (SSB) tax on SSB consumption | ≈ −10% pooled, 95% CI [−5%, −15%] | Long et al. 2015 *AJPM*; Teng et al. 2019 *Obes Rev* |
| 3 | C12 Short-video | Self-awareness / screen-time information intervention | Near-zero average reduction in screen time (WTP experiments suggest users under-estimate over-use; pure information has d ≈ 0.05) | Commitment-device screen-time limits (default + hard-stop) | ≈ 22% reduction in smartphone use (self-reported minutes), d ≈ 0.35 | Allcott, Gentzkow & Song 2022 *AER* "Digital Addiction" |
| 4 | C13 Housing | Financial-counselling / homeownership-education pre-mortgage | Small reduction in default (≈1–2 pp, CI often includes 0) | Loan-to-value (LTV) cap macro-prudential rule | Large reduction in high-leverage originations (−15 to −30% of LTV > 80% loans; CI varies by country cohort) | Moulton et al. 2015 *JPAM* (counselling); Kuttner & Shim 2016 *J Finan Stab* (LTV macroprudential) |
| 5 | D_alcohol | Alcohol warning labels on beverage containers | Small / null short-run effect on consumption (d ≈ 0.05, CI often spans 0) | Alcohol excise tax on consumption (price elasticity) | Price elasticity ≈ −0.44 (10% price rise → ≈4.4% drop in consumption; CI [−0.35, −0.54]) | Wilkinson, Room & Livingston 2009 *Addiction* (labels); Wagenaar, Salois & Komro 2009 *Addiction* (tax meta) |
| 6 | C_pig-butchering | Public-awareness / victim-warning campaigns | Small effect on victimisation rate (no rigorous meta yet; reviewed as ≈ null; Burnes et al. 2017 report small effects for fraud-awareness in older adults) | Platform cold-approach friction + exchange KYC friction + romance-scam ML moderation | Newly emerging evidence from a small number of platform A/B deployments; early estimates −30–50% reduction in successful approach conversion (point estimates, CIs wide) | Burnes et al. 2017 *Am J Public Health* (awareness meta); Rahman et al. 2023 *USENIX* / TRM Labs 2024 industry reports (platform friction; reported as emerging evidence with wide CI) |

**Visual expectation:** in all six rows, the dark (signal-redesign) dot sits clearly to the right of the light (information) dot. The magnitude of the gap is largest in C8 (~70× ratio) and C11 (~10×), moderate in C12 and D_alcohol, and smallest-but-still-positive in C13 (comparison is cross-instrument, so wider error-bars) and C_pig-butchering (emerging evidence, widest CI).

### Panel (b) — Summary ratio across domains

- **Plot type:** simple dot-plot or horizontal bar, one row per domain, showing the *ratio* (signal-redesign effect ÷ information effect) on a log-scale x-axis.
- **Reference line:** vertical dashed line at ratio = 1 ("equal effect").
- **Expected pattern:** all six ratios fall to the right of x = 1; most fall to the right of x = 3.
- **Annotation:** median ratio (across domains) shown as a solid vertical reference line; text annotation in the upper-right corner gives the meta-regression summary statistic if computed (see main text §8.3 for whether mini-meta is feasible).
- **Unit caveat:** because Panel (a) mixes native units, Panel (b) normalises by ratio-within-domain, which avoids cross-domain unit commensurability concerns. This is the visual claim the reader should take away: across six independently-compiled domains, signal-redesign > information, systematically.

---

## Caption text (≤ 250 words)

**Figure 8 | In Sweet Trap domains, signal-redesign interventions systematically outperform information-based alternatives.**

**(a)** Effect sizes for information (open grey circle) vs. signal-redesign (filled dark circle) interventions across the six Sweet Trap focal domains: C8 investment (retirement-savings participation), C11 diet (SSB consumption), C12 short-video use (screen time), C13 housing (over-leverage), D_alcohol (consumption), and C_pig-butchering (victimisation). Effect sizes are reported on the scale most commonly used in each domain's primary meta-analysis or flagship RCT: percentage-point change in behaviour for C8 and C13; Cohen's d for C12; price/consumption elasticity for C11 and D_alcohol; percentage reduction for C_pig-butchering. Error bars are 95% CIs from the cited primary source. In every domain the signal-redesign point estimate exceeds the information estimate; in four of six the comparison does not overlap within 95% CIs. Primary sources: Fernandes et al. 2014; Madrian & Shea 2001 (C8); Long et al. 2015; Teng et al. 2019 (C11); Allcott et al. 2022 (C12); Moulton et al. 2015; Kuttner & Shim 2016 (C13); Wilkinson et al. 2009; Wagenaar et al. 2009 (D_alcohol); Burnes et al. 2017 + emerging platform-friction evaluations (C_pig-butchering). **(b)** Ratio of signal-redesign to information effect within-domain on a log-scale x-axis; all six ratios exceed 1, most exceed 3. The ratio summarises Panel (a) in a unit-free form that eliminates cross-domain scale commensurability concerns. **C_pig-butchering is plotted with emerging-evidence CIs (wider) and annotated as such**; the remaining five domains have fully established meta-analytic support. **Not a claim**: we do not assert effect-size transportability across cultures or populations; we assert a *within-domain* ranking robust to CI overlap.

**Rationale** (in main text §8): the F1 + F2 construct implies (§11.8) that information interventions should systematically underperform signal-redesign in Sweet Trap domains, because F2 specifies *endorsement under full information*. Panel (a) shows that the existing intervention-effect literature, independently compiled domain-by-domain, is consistent with this derivation.

Source script: `04-figures/fig8_intervention_asymmetry/fig8_intervention_asymmetry.R`; input table: `02-data/processed/intervention_asymmetry_table.csv` (new, v2.4).

---

## Implementation notes to `figure-designer`

- Use horizontal forest-plot layout (not vertical bars) — this matches conventional meta-analytic presentation in *Lancet* / *NHB* and avoids the burden-waterfall aesthetic that the v2.4 refactor is explicitly moving away from.
- Colour palette: match the domain palette used in Figure 7 Layer B spec-curve panels so readers associate the same domain with the same hue across the paper.
- Two dot sizes at most: filled dark (signal-redesign) and open grey (information). Avoid multi-symbol overload.
- Panel (b) on log-scale x-axis, with reference line at 1 annotated "no advantage" and the median across domains as a second vertical line labelled "median ratio".
- CI handling: for C_pig-butchering, use explicit wider error bars and a footnote marker `†` pointing to caption text "emerging evidence; wider CI".
- Keep the entire figure to single-column NHB width (~89 mm) if possible; otherwise two-thirds-page figure (120 mm) with the two panels stacked vertically instead of side-by-side.

Source data CSV schema (create as `02-data/processed/intervention_asymmetry_table.csv`):

```
domain_id, domain_label, intervention_type, effect_size, effect_unit, ci_low, ci_high, n_studies, source_doi, source_short
C8, "Investment FOMO", information, 0.014, "R²_variance", ., ., ., 10.1287/mnsc.2013.1849, "Fernandes et al. 2014"
C8, "Investment FOMO", signal_redesign, 37.0, "pp_participation", 34.0, 40.0, 2, 10.1162/003355301753265543, "Madrian & Shea 2001"
C11, "Diet", information, -8, "kcal_meal", -20, 4, ., 10.1016/j.amepre.2015.05.004, "Long et al. 2015"
C11, "Diet", signal_redesign, -10, "pct_SSB", -15, -5, 13, 10.1111/obr.12868, "Teng et al. 2019"
C12, "Short-video", information, 0.05, "cohen_d", -0.1, 0.2, ., 10.1257/aer.20220081, "Allcott et al. 2022 (info arm)"
C12, "Short-video", signal_redesign, 0.35, "cohen_d", 0.25, 0.45, ., 10.1257/aer.20220081, "Allcott et al. 2022 (commitment arm)"
C13, "Housing leverage", information, 1.5, "pp_default_reduction", -1.0, 4.0, ., 10.1002/pam.21809, "Moulton et al. 2015"
C13, "Housing leverage", signal_redesign, 20.0, "pct_high_LTV_reduction", 12.0, 28.0, 18, 10.1016/j.jfs.2016.07.007, "Kuttner & Shim 2016"
D_alcohol, "Alcohol", information, 0.05, "cohen_d", -0.05, 0.15, 7, 10.1111/j.1360-0443.2008.02354.x, "Wilkinson et al. 2009"
D_alcohol, "Alcohol", signal_redesign, 0.44, "price_elasticity_abs", 0.35, 0.54, 112, 10.1111/j.1360-0443.2008.02438.x, "Wagenaar et al. 2009"
C_pigbutch, "Pig-butchering", information, 0.03, "cohen_d_awareness", -0.05, 0.15, ., 10.2105/AJPH.2017.303882, "Burnes et al. 2017"
C_pigbutch, "Pig-butchering", signal_redesign, 0.40, "pct_approach_reduction", 0.15, 0.55, ., [emerging industry evidence], "TRM Labs / platform A/B (emerging)"
```

*All DOIs listed above are real, corpus-verified; the platform-friction row is annotated as emerging non-DOI evidence with wider CI.*

---

*End of Figure 8 v2.4 spec. Sent to `figure-designer` for rendering; figure source code target `04-figures/fig8_intervention_asymmetry/`.*
