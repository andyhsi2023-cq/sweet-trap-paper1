# SI Bundle Log — v3.3 Supplementary Information

**Date:** 2026-04-18
**Task:** W4 compliance blocker — single Supplementary Information PDF for NHB initial submission
**Output artefacts:**

- `SI_v3.3_master.md` (16,322 words, 1,144 lines)
- `SI_v3.3_master.docx` (70,112 bytes via `pandoc 3.9`)
- `SI_v3.3_master.pdf` (782,404 bytes / 768 KB, 46 pages, via LibreOffice headless `writer_pdf_Export`)

---

## 1. SI child files merged (in TOC order)

| # | TOC entry | Source file | Status |
|---|---|---|---|
| 1 | Supplementary Note 1 — SI overview + index | `SI_v3.0_outline.md` (entire content, adapted as overview) | Merged verbatim as overview narrative; SI-Math §1–§9 full text flagged pending (retained in `paper1-theory/` source repo; to be compiled at revision) |
| 2 | Supplementary Appendix B — θ/λ/β/ρ derivations | `SI_draft/SI_appendix_B_derivations.md` | Merged verbatim; sole change: SI Figure 3 reference re-pointed to Supplementary Figure S3 |
| 3 | Supplementary Note 2 — §11 framework refinements log | `s11_rewrite.md` | Merged verbatim; no figure/table citations to renumber |
| 4 | Supplementary Note 3 — §11.7 Engineered Deception | `s11_7_engineered_deception.md` | Merged verbatim; §11.7.3 PUA section replaced with a forward reference to Supplementary Note 4 (to avoid duplication with the SI §11.7b content) |
| 5 | Supplementary Note 4 — §11.7b PUA extended analysis | `SI_11_7b_pua_extended.md` | Merged verbatim; "main text §11.7" references clarified to "main-text §11.7 / Supplementary Note 3" where relevant |
| 6 | Supplementary Note 5 — §11.8 Policy predictability | `s11_8_policy_predictability.md` | Merged verbatim; main-text Figure/Table citations re-pointed ("Figure 8 and Table 4" → "main-text Fig. 5 and Supplementary Table S1"); "SI §11.7b" → "Supplementary Note 4" |
| 7 | Supplementary Appendix H — orthogonal DALY | `SI_H_orthogonal_health_implications.md` | Merged verbatim; "SI Appendix F" → "Appendix F in the OSF deposit" for figure cross-references; retained Supplementary Figure H1 but renumbered to Supplementary Figure S7 |
| 8 | Supplementary Note 6 — Extended Data items | `extended_data_v3.2.md` | Merged verbatim; ED Table/Fig numbering retained (these are ED items submitted separately to NHB, not SI-internal figures) |
| 9 | Supplementary Note 7 — expanded figure legends | `figure_legends_v3.1.md` | Merged verbatim; section headings changed from "Figure N" to "Main-text Fig. N" per SI cross-referencing convention |

**Total child files merged:** 9 of 9 requested in task specification (all present, no files missing).

---

## 2. NHB §11 SI renumbering operations performed

Following the Nature Human Behaviour supplementary-information style and the task specification's renumbering rules:

### 2.1 Main-text references inside SI

- All references of the form "Fig. N" that unambiguously point to the main manuscript were rewritten as **"main-text Fig. N"** (affects Supplementary Notes 3, 4, 5, 6, 7).
- All references of the form "Table N" pointing to the main manuscript were rewritten as **"main-text Table N"**. However, note: the task specification flagged "main Table 1/Table 2 → Supplementary Table S1 in SI references". On closer reading of the source files, the only such reference was in Supplementary Note 5 §11.8.3 pointing to "Figure 8 and Table 4" — which referred to v2.4 numbering, not main-text Table 1/2 at v3.3. This was updated to **"main-text Fig. 5 and Supplementary Table S1"** since the six-domain table is an SI-side table in v3.3, not a main-text table. No v3.3 main-text Table 1 / Table 2 references appear inside the SI content.

### 2.2 SI-internal figure/table numbering restart

Numbering restarts at S1 within the SI, per the cross-referencing convention stated at the head of `SI_v3.3_master.md`:

| Source label | Rewritten label | Note |
|---|---|---|
| "SI-M1" (containment diagram) | Supplementary Figure S1 | SI-Math §7.8 companion |
| "SI-A1" (Layer A full forest) | Supplementary Figure S2 | Appendix A companion |
| "SI-A2" (funnel plot) | Supplementary Figure S3 | Appendix A companion |
| "SI-B1–B3" (MR forests by sub-class) | Supplementary Figures S4–S6 | Appendix B empirical companion |
| "SI-H1" (DALY dual-anchor + Sankey) | Supplementary Figure S7 | Appendix H companion |
| "Supplementary Figure H1" (in Appendix H narrative) | Supplementary Figure S7 | Consolidated with above |
| "SI Figure 3" (in Appendix B derivations §B.7 criticism 4) | Supplementary Figure S3 | Sensitivity envelope for *r̄* ∈ [0, 0.5] |
| "SI Appendix F" (Appendix H §H.4) | "Appendix F in the OSF deposit" | No in-SI content for empirical Appendix F; deferred to OSF |

Supplementary Tables S1–S*n* are released as OSF spreadsheets; the SI body does not contain inline Supplementary Tables with NHB-style `S*n*` labels other than the one pointer in Supplementary Note 5 (see §2.1 above).

### 2.3 Cross-reference disambiguation

- The naming collision "Appendix B" appears twice in the source outline: once for the load-bearing axiomatic derivations (theoretical Appendix B) and once for the Layer D MR empirical-block appendix. In `SI_v3.3_master.md`:
  - The theoretical Appendix B is reproduced in full and titled "**Supplementary Appendix B — Derivation of the Layer 2 primitives (θ, λ, β, ρ) from Layer 1 evolutionary dynamics**".
  - The empirical Appendix B is referenced in the Block-2 SI-Empirical index (Supplementary Note 1) with an explicit disambiguation note, and its full contents are deferred to OSF.
- Main-text figures (main-text Fig. 1–6) do *not* appear in the SI, per the task specification rule.

---

## 3. Pandoc / LibreOffice conversion

### 3.1 Pandoc build

```
pandoc 3.9
SI_v3.3_master.md → SI_v3.3_master.docx
--resource-path=".:../04-figures/main:../04-figures/supp"
```

- No image references embedded in this SI (all figure content is narrative / legend form; actual figure images are submitted separately as part of the NHB figure bundle).
- No pandoc warnings or errors on stdout/stderr.
- DOCX size: 70,112 bytes (68 KB).

### 3.2 LibreOffice PDF export

```
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf
SI_v3.3_master.docx → SI_v3.3_master.pdf (writer_pdf_Export filter)
```

- PDF size: 782,404 bytes (768 KB) — well above the 100 KB floor, well below the NHB 10 MB soft ceiling and 30 MB hard ceiling.
- PDF page count: 46 pages.
- Metadata sanity: `mdls kMDItemNumberOfPages` returned 46.

---

## 4. Verification against task acceptance criteria

| Criterion | Status |
|---|---|
| SI master .md produced at `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/SI_v3.3_master.md` | OK |
| All 9 requested child files merged in specified order | OK |
| Title page shows SI v3.3 version label + OSF URL `https://osf.io/ucxv7/` | OK |
| NHB SI numbering applied (Supplementary Figure S*N* / Supplementary Table S*N*; main-text Fig. references prefixed) | OK |
| Main-text Figs 1–6 do not appear in SI | OK (only legends + references) |
| Pending / placeholder outline items flagged with `<!-- outline item pending -->` | OK (SI-Math §1–§9 full text block) |
| PDF > 100 KB | OK (768 KB) |
| PDF ≤ 10 MB | OK (0.75 MB, well under) |
| Main-text manuscript `main_v3.3_draft.md` unmodified | OK (not touched) |
| Figure files unmodified | OK (not touched) |
| All outputs placed inside `05-manuscript/` (no new sub-directory) | OK |

---

## 5. Action-needed items (none blocking submission)

No blocking issues. Two advisory notes for the revision round:

1. **SI-Math §1–§9 full mathematical text is currently in outline form only** (marked `<!-- outline item pending -->` inside Supplementary Note 1). The load-bearing mathematical supplement for initial submission is the in-full **Supplementary Appendix B** (axiomatic derivations of θ, λ, β, ρ). Reviewers requesting more theorem-proof detail than Appendix B provides will trigger a revision-stage compile of the full SI-Math block from the `paper1-theory/` repository.
2. **Supplementary Tables S1–S*n* are OSF-deposited as spreadsheets rather than embedded in this SI PDF.** The six-domain intervention-asymmetry table and the 59-country G^c table are the most likely candidates for inline embedding at revision; both are pointed to by file path in the relevant Supplementary Notes.

---

*End of SI bundle log.*
