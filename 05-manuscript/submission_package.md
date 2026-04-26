# Submission Package — Nature Human Behaviour

**Project:** sweet-trap-multidomain
**Manuscript:** Sweet Trap: a cross-species reward–fitness decoupling equilibrium and a derived law of intervention effectiveness
**Target journal:** *Nature Human Behaviour* — Article
**Version:** v2.4 (2026-04-18, post benchmark-audit refactor)
**Prepared by:** manuscript-writer agent, Stage 4 v2.4 refactor

---

## 1. Manifest with status

| # | Item | Status | File path | Notes |
|---|---|:---:|---|---|
| 1 | Main manuscript (v2.4, DALY → policy-predictability refactor) | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/main_v2.4_draft.md` | Main 4,408 words; Methods 3,993; Abstract 296 |
| 2 | Abstract (standalone) | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/abstract_v2.4.md` | 296 / 300 words; final sentence rewritten [DIFF-C2] |
| 3 | Figure legends (v2.1 updated for Fig. 8 replacement) | ⚠️ pending update | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/figure_legends_v2.1.md` | Figure 8 legend needs v2.4 rewrite per `figure_8_v2.4_spec.md`; Figures 1–7 + 9 unchanged |
| 4 | Figures (Fig 1–9 source + rendered) | ⚠️ Fig. 8 pending | `/Users/andy/Desktop/Research/sweet-trap-multidomain/04-figures/` | Fig 1–7 + 9 rendered at v2.1; Fig 8 must be re-rendered per `figure_8_v2.4_spec.md` by figure-designer |
| 5 | Figure 8 v2.4 spec (data + intent) | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/figure_8_v2.4_spec.md` | 6-domain × 2-intervention-type matrix + within-domain ratio panel; data CSV schema included |
| 6 | Supplementary Information — outline | ⚠️ pending update | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/supplementary_v2_outline.md` | Needs addition of SI Appendix H to outline |
| 7 | SI Appendix H — orthogonal health-implications (DALY migrated) | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/SI_H_orthogonal_health_implications.md` | NEW v2.4; houses the v2.3 §8 DALY material + Fig. H1 legend |
| 8 | §11.7b PUA boundary case | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/SI_11_7b_pua_extended.md` | Moved from main text per v2.2 DIFF-P2 |
| 9 | §11.7 Engineered Deception | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/s11_7_engineered_deception.md` | Pig-butchering main-text exemplar + PUA pointer to §11.7b |
| 10 | §11.8 Policy predictability as construct derivative | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/s11_8_policy_predictability.md` | NEW v2.4; [DIFF-C5] |
| 11 | SI drafts (aux) | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/SI_draft/` | Appendix A–G per outline; H added v2.4 |
| 12 | Cover letter (v2.4) | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/cover_letter_nhb_v2.md` | Third core claim rewritten to policy-predictability; ~470 body words; 4 paragraphs |
| 13 | Data Availability statement | ✅ ready | *embedded in main_v2.4 §Data and code availability + §M11 + §M12 + §M13* | OSF DOI placeholder inserted |
| 14 | Author contributions statement | ✅ ready | *embedded in main_v2.4 §Author contributions* | Lu An: conception, analysis, writing; Hongyang Xi: analysis support, writing review |
| 15 | ORCID — Lu An | ✅ ready | — | 0009-0002-8987-7986 |
| 16 | ORCID — Hongyang Xi | ✅ ready | — | 0009-0007-6911-2309 |
| 17 | Competing interests statement | ✅ ready | *embedded in main_v2.4* | "The authors declare no competing interests." |
| 18 | Ethics statement | ✅ ready | *embedded in main_v2.4* | Publicly-available secondary data + summary statistics |
| 19 | Funding statement | ✅ ready | *embedded in main_v2.4* | No dedicated funding; institutional infrastructure only |
| 20 | Pre-registration (OSF) | ⏳ Andy action | OSF deposit pending | `[OSF_DOI_TO_INSERT]` placeholder in main_v2.4 §M13 + cover letter + Data Availability; Andy to upload v2 formal model + `cross_level_plan.md` + §11 + §11.8 + v2.4 intervention-asymmetry compilation to OSF and paste issued DOI |
| 21 | Reporting Summary (NHB template) | ⚠️ pending | — | NHB requires completed `NHB_Reporting_Summary.pdf`; fill from Methods §M4–M13 |
| 22 | Editorial Policy Checklist | ⚠️ pending | — | Standard NHB checklist form |
| 23 | Handling editor suggestion | ⏳ Andy action | — | TBD; cover letter leaves editor field at editorial discretion |
| 24 | Pre-submission lint | ⚠️ pending | — | Run `_meta/scripts/pre-submission-lint.py` against `main_v2.4_draft.md` per Andy rule |
| 25 | Word-count audit v2.4 | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/word_count_audit_v2.4.md` | Main 4,408 / 4,500; Methods 3,993 / 4,000; Abstract 296 / 300 |
| 26 | Diff log (v2.3 → v2.4) | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/diff_v2.3_to_v2.4.md` | Complete 7-edit changelog + honesty log |
| 27 | Intervention-asymmetry compilation CSV (v2.4) | ⚠️ pending | `/Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/intervention_asymmetry_table.csv` | Schema in `figure_8_v2.4_spec.md`; data-analyst to materialise |
| 28 | Benchmark audit documenting the refactor | ✅ ready | `/Users/andy/Desktop/Research/sweet-trap-multidomain/00-design/stage4/benchmark_construct_vs_daly.md` | Triggered and justifies the v2.4 Option C refactor |

---

## 2. Status summary (v2.4)

| Category | Count |
|---|:---:|
| ✅ Ready | 19 |
| ⚠️ Pending agent action | 7 (Figure 8 re-render, figure-legend update, SI outline update, Reporting Summary, Editorial Policy Checklist, pre-submission lint, intervention-asymmetry CSV) |
| ⏳ Andy action | 2 (OSF DOI, handling editor) |
| **Total** | **28** |

---

## 3. Remaining Andy-action checklist

1. **OSF deposit** — Upload the following files to OSF as a project with pre-registration:
   - `00-design/sweet_trap_formal_model_v2.md` (v2 formal model)
   - `00-design/pre-analysis/cross_level_plan.md` (pre-registered A+D joint test, frozen 2026-04-17)
   - `05-manuscript/s11_rewrite.md` (§11 framework document with date-stamped limitation log)
   - Paste issued DOI into three places: `main_v2.3_draft.md` front-matter + §M12 + §Data and code availability + `cover_letter_nhb.md`
   - Replace four `[OSF_DOI_TO_INSERT]` placeholders (one in cover letter; three in manuscript)

2. **Handling editor suggestion** — After Task #71 benchmark completes (NHB editor identification), paste editor name into cover letter §3 ("We do not propose a handling editor at this stage" → "We respectfully suggest Editor [Name] as handling editor").

3. **Reporting Summary form** — Complete the NHB template form (usually `NHB_Reporting_Summary_v5.pdf` from author portal) using numbers from Methods §M4–M10. Key fields: sample sizes per layer, statistical tests used, randomisation/blinding (N/A for secondary-data layers), replication attempts, code availability.

4. **Editorial Policy Checklist** — Standard NHB form; most items are N/A for an observational + meta-analytic + MR study (no clinical trials, no new ethics approval, no live subjects).

5. **Pre-submission lint** — Run `_meta/scripts/pre-submission-lint.py` against `main_v2.3_draft.md` for CJK / table-orphan / section-missing checks; fix any issues before submission per Andy memory `feedback_pre_submission_lint.md`.

6. **Optional diff log v2.2 → v2.3** — If desired for archival continuity; `main_v2.3_draft.md` already carries inline `[DIFF-M]` tags summarising all changes.

7. **Author-contributions review** — Confirm that L.A.: conception, analysis, writing; H.X.: analysis support, writing review accurately reflects roles, and adjust if needed.

---

## 4. Submission portal file list (NHB upload order)

The NHB author portal typically requests the following file uploads (order from the portal):

1. **Cover letter** — `cover_letter_nhb_v2.md` → convert to `.pdf` or `.docx` per portal
2. **Manuscript text** (Title page + Abstract + Main text + Methods + References + Tail sections) — `main_v2.4_draft.md` → `.docx`
3. **Figure files** (one per figure, high-resolution) — `04-figures/Fig1.pdf` through `Fig9.pdf` (or `.png`/`.tif` per portal spec). **Figure 8 must be re-rendered per `figure_8_v2.4_spec.md` before submission**; figures 1–7 and 9 unchanged from v2.1.
4. **Figure legends** — included in main manuscript end-block; separate file not usually needed for NHB. **Figure 8 legend must be rewritten per v2.4 spec**; see `figure_8_v2.4_spec.md` caption text.
5. **Supplementary Information** (one bundled PDF) — SI Appendix A–H per `supplementary_v2_outline.md` (+ new H from v2.4) → `SI.pdf`. **Appendix H is new v2.4 (DALY material migrated from main-text §8)**; re-render as Supplementary Figure H1 + appendix text.
6. **Reporting Summary** — `NHB_Reporting_Summary.pdf`
7. **Editorial Policy Checklist** — `NHB_Editorial_Policy_Checklist.pdf`

---

*Prepared 2026-04-18 by manuscript-writer agent at the close of Stage 4 v2.4 refactor for sweet-trap-multidomain. v2.4 is the submission-target version; v2.3 remains archived for diff continuity. Refactor triggered by benchmark audit (`00-design/stage4/benchmark_construct_vs_daly.md`) confirming that ≈0% of construct-type Nature/Science papers anchor on DALY; Option C (complete DALY removal from main text) confirmed by Andy. See `word_count_audit_v2.4.md` for section-level verification and `diff_v2.3_to_v2.4.md` for the 7-edit changelog.*
