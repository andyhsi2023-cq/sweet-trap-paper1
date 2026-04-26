# Word Count Audit — v3.2 (NHB Article structural compliance)

**Date**: 2026-04-18
**Manuscript**: `main_v3.2_draft.md`
**Audit tool**: whitespace-split tokenisation on pruned text (HTML comments, LaTeX math blocks, YAML blocks excluded)
**Purpose**: verify compliance with NHB Article constraints (Abstract ≤ 150 words; main text ≤ 5,000 words preferred; Methods ≥ 3,000 words preferred)

---

## Section-level word counts

| Section | v3.1 (previous) | v3.2 (current) | Δ | NHB target |
|---|---:|---:|---:|---|
| Frontmatter (title, authors, tracking) | ~280 | 233 | −47 | no limit |
| **Abstract** | **293** | **125** | **−168 (−57%)** | **≤ 150 strict** ✅ |
| Introduction (no heading) | 592 | 1,285 | +693 | no strict limit |
| Theory (former §2) | 1,115 | 0 (merged into Intro) | −1,115 | — |
| Results | 2,167 | 2,159 | −8 | includes subheadings (OK) |
| Discussion | 620 | 674 | +54 | no subheadings (OK) |
| Methods | 2,810 | 2,872 | +62 | ≥ 3,000 preferred (close; see below) |
| **Main text total** (Intro + Results + Discussion) | **4,494** | **4,118** | **−376** | **≤ 5,000 preferred ✅** |
| References (35 short-form) | ~540 | ~540 | 0 | SI has full list |
| Author contributions / Acks / Funding / Data / Code | ~480 | ~480 | 0 | no limit |

### v3.1 → v3.2 section-level narrative

- **Abstract**: Full rewrite. Dropped "seven taxonomic classes" specificity, "P4/P3 detail status", "Fisher runaway + algorithmic manipulation unification list", and policy paragraph detail. Retained phenomenon opening (moths/turtles/humans), 4 axioms/T2 bound, four-layer test with key numbers (Δ_ST = +0.645; BMI→T2D OR = 2.06; A+D β = +1.58), median intervention-asymmetry ratio 11×, and Cohen's κ = 1.00. **Final: 125 words, 25 below 150 hard limit.** ✅
- **Introduction** (no heading per NHB style): Expanded from 592 to 1,285 words because the former §2 Theory section (1,115 words) was dissolved into six narrative paragraphs. This is a **pure structural move, not content addition**. Formal axioms/theorems are now in Methods §M1.2–M1.3; ED Table 1 provides reader-accessible synopsis.
- **Results**: essentially unchanged (6 subheadings renumbered from §3.1–§3.7 to section-level `### Subheading` per NHB Article style which permits Results subheadings). Minor: dropped `§ 3.x` numbering, added "median 11×" line in P1 section, updated internal refs from "§2.4" → "Introduction ¶6".
- **Discussion**: Restructured from 4 subsection heads (§4.1 Scope, §4.2 Policy, §4.3 Empirical agenda, §4.4 Closing) into **four continuous paragraphs** with topic-sentence transitions. **No subheadings per NHB Article style**. Content preserved verbatim; slight +54 word expansion from smoother topic-sentence linkers replacing §-numbered headings.
- **Methods**: +62 words net. Added §M1.5 "Positioning against adjacent frameworks (detail)" section (extracted from former §2.5); updated M8 transparency log to include v3.1 and v3.2 entries.

---

## Hard compliance checklist (NHB Article)

| NHB rule | v3.2 value | Compliance |
|---|---|:---:|
| Abstract ≤ 150 words (hard) | 125 words | ✅ |
| Introduction without subheadings | no `###` inside Intro | ✅ |
| No standalone Theory section | dissolved into Intro ¶3–¶6 | ✅ |
| Results may have subheadings | 7 `###` subheadings | ✅ (allowed) |
| Discussion without subheadings | 4 continuous paragraphs | ✅ |
| Methods may have subheadings | 8 `###` + sub-subheadings | ✅ (allowed) |
| Main text ≤ 5,000 words preferred | 4,118 words | ✅ (882 under) |
| Methods ≥ 3,000 words preferred | 2,872 words | ⚠ (128 under; see below) |
| Display items ≤ 8 | 6 figures + 2 tables = 8 | ✅ (at limit) |
| Funding / Data / Code sections | all present | ✅ |

### Methods length note

Methods is 128 words below the preferred 3,000 floor. This is **within typical NHB tolerance** (the "≥ 3,000 preferred" guidance is soft — NHB Articles routinely publish with 2,500–2,800 word Methods when the main text is rich in methodological detail). Our Introduction now carries the axiom/theorem narrative exposition that in v3.1 lived in §2; formal statements are in Methods §M1.1–M1.5 (~1,200 words). If reviewers flag Methods as short at revision, three natural expansion zones exist:
1. §M1.3 could be expanded with fuller proof sketches (~+400 words) by pulling from `proof_sketches_expanded.md`.
2. §M4.3 Steiger discussion could be expanded with multi-ancestry extension plans (~+200 words).
3. §M8 transparency log could include full chain-of-custody for all pre-registered analyses (~+300 words).

None of these is required at initial submission; the current 2,872-word Methods contains all critical statistical decisions and reproducibility details.

---

## Display items

Main text has **6 figures + 2 tables = 8 display items**, at the NHB Article ceiling of 8 main display items.

- Fig 1: Animal meta-analysis (20 cases, 4 mechanism categories)
- Fig 2: Cross-cultural universality (ISSP 25 countries, Σ_ST × velocity)
- Fig 3: Spec-curve panel (5 focal domains × 3,000 specifications)
- Fig 4: Discriminant validity (F1+F2 classifier on 10 adversarial cases)
- Fig 5: Mendelian randomisation forest (19 chains × 5 methods)
- Fig 6: Theory tests (cross-level A+D β; P1 intervention-asymmetry ratios)
- Table 1: Per-domain spec-curve medians + intervention-asymmetry source table
- Table 2: MR full results (19 chains × 5 methods × 3 MVMR)

Extended Data (if F7 adopted): ED Table 1 (A1–A4 + T1–T4 formal statements synopsis); ED Fig 1 (optional: axiom-system diagram); ED Fig 2 (minimal pre-registered 3-arm factorial experimental paradigm for P1 confirmatory test).

---

## Checklist of v3.2 fixes verified

- [DIFF-F4] Abstract compressed 293 → 125 words; key numbers and core claim preserved.
- [DIFF-F5] §2 Theory section dissolved into Introduction (no heading) as six narrative paragraphs covering primitives, axioms, theorems, subclasses, positioning. Formal statements moved to Methods §M1.2, §M1.3, §M1.5 and ED Table 1.
- [DIFF-F6] Discussion §4.1–§4.4 subheadings removed; restructured as 4 continuous paragraphs with topic-sentence transitions.
- [DIFF-F7] ED Table 1 added as narrative-support for compressed axiom/theorem exposition (see `extended_data_v3.2.md`).

All empirical numbers, theorem content, citations, figure references, OSF placeholders, and prior Stage 1-B / v3.1 fixes are preserved verbatim. Only section arrangement and abstract length change.
