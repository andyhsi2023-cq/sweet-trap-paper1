# Figure Renumbering Log — B1 Fix (NHB AIP §3)

**Date:** 2026-04-18
**Blocker:** NHB AIP §3 — figures must be cited in sequential order in main text.
**Problem:** Original citation order in main_v3.2_draft.md was 1, 3, 2, 5, 6, 4 (non-sequential).

---

## 1. Physical File Renames

`/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/main/`

| Old filename | New filename | Change |
|---|---|---|
| fig1_animal_phylogeny_meta.{pdf,png,R} | fig1_animal_phylogeny_meta.{pdf,png,R} | unchanged |
| fig3_spec_curve_5panel.{pdf,png} | fig2_spec_curve_5panel.{pdf,png} | old 3 → new 2 |
| fig2_issp_cross_cultural.{pdf,png,R} | fig3_issp_cross_cultural.{pdf,png,R} | old 2 → new 3 |
| fig5_mr_layer_D.{pdf,png,R} | fig4_mr_layer_D.{pdf,png,R} | old 5 → new 4 |
| fig6_theory_tests.{pdf,png,R} | fig5_theory_tests.{pdf,png,R} | old 6 → new 5 |
| fig4_discriminant_dashboard.{pdf,png,R} | fig6_discriminant_dashboard.{pdf,png,R} | old 4 → new 6 |

Method: two-phase rename via `fig_tmp<N>_*` intermediates to avoid name collisions.
Note: `fig3_spec_curve_5panel.R` did not exist in directory (no R script for spec-curve panel); only .pdf and .png were present — confirmed before rename.

---

## 2. Text Replacements

### 2a. main_v3.2_draft.md

Two-phase sed (macOS BSD `sed -i ''`) with temp tokens to prevent chain-collision:

| Old citation | New citation | Occurrences |
|---|---|---|
| Fig. 2 | Fig. 3 | 1 (L84) |
| Fig. 3 | Fig. 2 | 1 (L67) |
| Fig. 4 | Fig. 6 | 1 (L155) |
| Fig. 5 | Fig. 4 | 1 (L92) |
| Fig. 6 | Fig. 5 | 5 (L110, L118, L126, L128, L241) |

Total replacements: 9 citation instances across main text.
`ED Fig 2` (L169) was not touched — uses `ED Fig` prefix, not bare `Fig.`.

### 2b. figure_legends_v3.1.md

Legends reordered to match new figure sequence:
- New Fig 2 legend = old Fig 3 legend (spec-curve). File path updated: `fig3_spec_curve_5panel.png` → `fig2_spec_curve_5panel.png`.
- New Fig 3 legend = old Fig 2 legend (ISSP). File path updated: `fig2_issp_cross_cultural.R` → `fig3_issp_cross_cultural.R`.
- New Fig 4 legend = old Fig 5 legend (MR forest). File path updated: `fig5_mr_layer_D.R` → `fig4_mr_layer_D.R`.
- New Fig 5 legend = old Fig 6 legend (theory tests). File path updated: `fig6_theory_tests.R` → `fig5_theory_tests.R`.
- New Fig 6 legend = old Fig 4 legend (discriminant). File path updated: `fig4_discriminant_dashboard.R` → `fig6_discriminant_dashboard.R`.
- Version note in footer updated to document B1-fix renumber history.

### 2c. extended_data_v3.2.md

No changes required. File contains only `ED Fig 1` and `ED Fig 2` references; no main-figure citations.

---

## 3. Verification grep

```
grep -n "Fig\. [0-9]" main_v3.2_draft.md | grep -v "ED Fig"
```

Result (first-citation sequence):
| Line | Citation | Sequential? |
|---|---|---|
| L55 | Fig. 1 | first cite = 1 |
| L67 | Fig. 2 | second cite = 2 |
| L84 | Fig. 3 | third cite = 3 |
| L92 | Fig. 4 | fourth cite = 4 |
| L110 | Fig. 5 | fifth cite = 5 |
| L118 | Fig. 5a | repeat cite |
| L126 | Fig. 5b,c | repeat cite |
| L128 | Fig. 5b,c | repeat cite |
| L155 | Fig. 6 | sixth cite = 6 |
| L241 | Fig. 5c | repeat cite |

First-citation sequence: 1 → 2 → 3 → 4 → 5 → 6. NHB AIP §3 satisfied.
No temp tokens (FIG_TMP_*) remain in any file.
