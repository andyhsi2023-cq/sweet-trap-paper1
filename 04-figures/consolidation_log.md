# Figure Consolidation Log — Sweet Trap v3.1 (9 → 6 Figures)

**Date:** 2026-04-18
**Reason:** Nature Human Behaviour Article maximum is 6 main figures; v2.4 had 9 (desk-reject risk).
**Red Team origin:** Red Team v5 consolidation directive specifying merge pairs and surviving figure mapping.
**Executed by:** Figure Designer agent (Claude, claude-sonnet-4-6).

---

## Old → New Mapping

| Old numbering (v2.4) | Old file name | Action | New numbering (v3.1) | New file name |
|---|---|---|---|---|
| Fig 1 (8-case animal forest) | `fig1_animal_meta.*` | MERGED into new Fig 1 (part A) | — | → `supp/fig_SI_A1_animal_meta.*` |
| Fig 2 (Layer B human panels) | `fig2_human_panels.*` | MERGED into new Fig 1 (part B) | — | → `supp/fig_SI_B1_human_panels.*` |
| Fig 3 (ISSP cross-cultural) | `fig3_cross_cultural.*` | RENAMED | **Fig 2** | `fig2_issp_cross_cultural.*` |
| Fig 4 (discriminant dashboard) | `fig4_discriminant_dashboard.*` | KEPT (number unchanged) | **Fig 4** | `fig4_discriminant_dashboard.*` |
| Fig 5 (grand map) | `fig5_grand_map.*` | DISPLACED to SI | — | → `supp/fig_SI_C1_grand_map.*` |
| Fig 6 (MR layer D forest) | `fig6_mr_layer_D.*` | RENAMED | **Fig 5** | `fig5_mr_layer_D.*` |
| Fig 7 (spec curve 5-panel) | `fig7_spec_curve_5panel.png` | RENAMED (PNG only) | **Fig 3** | `fig3_spec_curve_5panel.png` |
| Fig 8 (intervention asymmetry) | `fig8_intervention_asymmetry.*` | MERGED into new Fig 6 (panels b+c) | — | → `supp/fig_SI_T2_intervention_detail.*` |
| Fig 9 (cross-level meta) | `fig9_cross_level_meta.*` | MERGED into new Fig 6 (panel a) | — | → `supp/fig_SI_P5_cross_level_detail.*` |

**New figures created by merge:**

| New figure | File | Origin | Panels |
|---|---|---|---|
| **Fig 1** | `fig1_animal_phylogeny_meta.*` | Replaces old Figs 1+2 | (a) 20-case phylogenetic dot strip; (b) mechanism subgroup forest; (c) pooled summary |
| **Fig 6** | `fig6_theory_tests.*` | Replaces old Figs 8+9 | (a) cross-level A+D scatter β=+1.58; (b) intervention asymmetry forest 6 domains; (c) ratio log-scale bar |

---

## Merge Rationale

### New Fig 1 (old Figs 1+2 merged)
Old Fig 1 had only 8 cases (Layer A animal forest, 3 panels) and old Fig 2 was the Layer B human panels (5 sub-panels). These occupied 2 figure slots to make one argument: Sweet Trap is cross-species and multi-domain. New Fig 1 drops the Layer B human sub-panels (moved to Extended Data / SI as `fig_SI_B1_human_panels`) and replaces the 8-case forest with a 20-case phylogenetic dot strip, adding the mechanism subgroup forest and pooled summary. This converts two weakly-focused panels into one high-impact flagship figure. The phylogenetic layout is more visually compelling as a Nature Fig 1 opener than a standard forest plot.

### New Fig 6 (old Figs 8+9 merged)
Old Fig 8 (intervention asymmetry forest) and old Fig 9 (cross-level meta) shared the same epistemic function: testing theory-level predictions P1 and P5. Together they constitute the "theory tests" evidence. Merging them into a single 3-panel Fig 6 preserves all key visual evidence while saving one figure slot. Panel (a) carries the cross-level A+D joint result (headline β=+1.58), panels (b+c) carry the T2 intervention-asymmetry evidence.

### Displaced figures
- **Old Fig 5 (grand map):** Visually appealing but not the primary inferential evidence. Moved to SI as `fig_SI_C1_grand_map` to recover a figure slot. The map's key message (cross-domain severity gradient) is now conveyed by the mechanism subgroup forest in new Fig 1b.
- **Old Figs 1, 2 detail components:** Preserved in `supp/` as `fig_SI_A1_animal_meta` and `fig_SI_B1_human_panels` for reviewers who want the full original figures.

---

## File State After Consolidation

### `04-figures/main/` (6 figure sets — submission-ready)
```
fig1_animal_phylogeny_meta.{R,png,pdf}   — NEW (20-case phylogenetic + mechanism)
fig2_issp_cross_cultural.{R,png,pdf}     — renamed from fig3_cross_cultural
fig3_spec_curve_5panel.png               — renamed from fig7_spec_curve_5panel (PNG only)
fig4_discriminant_dashboard.{R,png,pdf}  — unchanged
fig5_mr_layer_D.{R,png,pdf}             — renamed from fig6_mr_layer_D
fig6_theory_tests.{R,png,pdf}           — NEW (cross-level + intervention merged)
figure_captions.md                      — legacy caption file (superseded by figure_legends_v3.1.md)
```

### `04-figures/supp/` (displaced originals + all previous SI figures)
```
fig_SI_A1_animal_meta.*          — old Fig 1 (8-case forest)
fig_SI_B1_human_panels.*         — old Fig 2 (Layer B)
fig_SI_C1_grand_map.*            — old Fig 5 (grand map)
fig_SI_T2_intervention_detail.*  — old Fig 8 (full intervention forest, detail version)
fig_SI_P5_cross_level_detail.*   — old Fig 9 (cross-level full panels)
fig_SI_H1_daly_*                 — DALY waterfall/Sankey (retired from main in v2.4)
mr_supp_forest.png               — MR supplementary
mr_supp_funnel.png               — MR funnel
spec_curve_C*.png                — Per-domain spec curve panels
```

---

## Manuscript Updates Applied (main_v3.1_draft.md)

| Location | Old reference | New reference |
|---|---|---|
| Header | "9 main figures" | "6 main figures" |
| §3.1 (Layer A) | "Fig. 1–2" | "Fig. 1" |
| §3.2 (Layer B) | "Fig. 4, 7" | "Fig. 3" |
| §3.3 (Layer C) | "Fig. 3" | "Fig. 2" |
| §3.4 (Layer D) | "Fig. 6" | "Fig. 5" |
| §3.5 primary test | "Fig. 9c" | "Fig. 6a" |
| §3.5 A+D headline | "Fig. 9c inset" | "Fig. 6a" |
| §3.6 intervention | "Fig. 8" | "Fig. 6b,c" |
| §3.7 discriminant | "Fig. 4" | "Fig. 4 (unchanged from v2.4)" |
| Methods M5 | pipeline note only | added fig6_theory_tests.R reference |
| Methods M6 | "Fig. 8 panel b" | "Fig. 6c" |

---

## Figure Legends Updated

`05-manuscript/figure_legends_v3.1.md` — 6 NHB-format captions (≤300 words each), replacing `figure_legends_v2.4.md` (9 figures). Old legends for displaced figures are preserved in the v2.4 file.

---

*Consolidation log version: 1.0, 2026-04-18.*
