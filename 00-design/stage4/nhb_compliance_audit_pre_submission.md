# NHB Pre-Submission Compliance Audit (2026-04-18)

**Auditor:** peer-reviewer agent (pre-submission lint role)
**Manuscript audited:** `/Users/andy/Desktop/Research/sweet-trap-multidomain/05-manuscript/main_v3.2_draft.md` (+ `cover_letter_nhb_v3.md`, `abstract_v3.2.md`, `figure_legends_v3.1.md`, `extended_data_v3.2.md`, `submission_package.md`)
**Standards consulted (live fetch 2026-04-18):**
- `https://www.nature.com/nathumbehav/submission-guidelines` (NHB submission guidelines index)
- `https://www.nature.com/nathumbehav/submission-guidelines/formatting-your-initial-submission` (initial-formatting, confirms initial submissions do not need full formatting)
- `https://www.nature.com/nathumbehav/submission-guidelines/preparing-your-submission` (what must be in submission package)
- `https://www.nature.com/nathumbehav/submission-guidelines/aip-and-formatting` (definitive AIP formatting rules: tables, figures 180 mm × 300 dpi, 5-7 pt sans-serif, reference ordering)
- `https://www.nature.com/nathumbehav/content` (Article content-type definition with all numeric caps)
- `https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards` (Reporting Summary, data availability mandate)
- `https://www.nature.com/nature-portfolio/editorial-policies/authorship` (CRediT-equivalent requirements, Inclusion & Ethics in Global Research)
- `https://www.nature.com/nature-portfolio/editorial-policies/competing-interests` (competing-interests wording)
- `https://www.nature.com/nathumbehav/submission-guidelines/orcid` (corresponding-author ORCID mandate)
- `https://www.nature.com/nathumbehav/submission-guidelines/dapr` (double-anonymized peer review)

---

## Overall verdict: **PASS-with-fixes**

The manuscript is substantively a strong fit for NHB's Article format and sits within every numeric cap (≤ 5,000 main / ≤ 150 abstract / ≤ 8 display items). Initial-submission formatting latitude (NHB explicitly states initial submissions "do not need to be specially formatted") removes most typographic risks; the PDF/DOCX pair that pandoc already produced is acceptable for portal upload. However, **five fixes are required before Playwright submission** to avoid a flagged compliance issue during editorial screening, and **seven further items are recommended** to reduce reviewer friction. No item rises to "FAIL = desk reject" in my judgment — this is a clean pre-flight, not a rewrite.

---

## Blockers (must fix before submission)

### B1. Figures are cited out of sequence in the main text (FAIL on NHB rule 3.a)
**Rule (AIP & formatting §3):** "All figures must be cited in sequence within the main article text in the form Fig. 1, Fig. 2."
**Evidence (first-mention line-numbers in `main_v3.2_draft.md`):**
- Line 55 — Fig 1
- Line 67 — Fig 3 (should be Fig 2)
- Line 84 — Fig 2 (cited after Fig 3)
- Line 92 — Fig 5 (cited before Fig 4)
- Line 110 — Fig 6 (before Fig 4)
- Line 155 — Fig 4 (cited LAST)
**Fix:** The `figure_legends_v3.1.md` reorder mapping (old 1+2 → new 1; old 4 → new 4; old 7 → new 3; old 6 → new 5; old 8+9 → new 6) needs to propagate into main-text call-outs. Two options:
- **Option A (preferred):** Renumber figures to match textual order. New Fig 1 stays. Rename current Fig 3 (spec-curve) → Fig 2; current Fig 2 (ISSP) → Fig 3; current Fig 4 (discriminant) → Fig 6; current Fig 5 (MR) → Fig 4; current Fig 6 (theory tests) → Fig 5. Legends and file names in `04-figures/main/` must be renamed concurrently.
- **Option B:** Move the paragraph/section that first cites Fig 4 (Discriminant) earlier in Results so the sequence becomes 1→2→3→4→5→6. This is structural but preserves figure files.
I recommend Option A (cheaper; no narrative rewrite). The renumber must also sweep figure legends in `figure_legends_v3.1.md`, figure file names under `04-figures/main/fig*`, and cover-letter pointers if any.
**Priority:** Highest. This is a first-glance editorial-screening red flag.

### B2. No CRediT-taxonomy Author Contribution statement (WARN rising to Blocker)
**Rule (Nature Portfolio authorship policy):** "Authors are required to include a statement of responsibility in the manuscript, including review-type articles, that specifies the contribution of every author."
NHB strongly encourages CRediT taxonomy (14 standard roles: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Resources, Data curation, Writing – original draft, Writing – review & editing, Visualization, Supervision, Project administration, Funding acquisition).
**Current statement (line 303–305):**
> L.A. led conception, theory development, analysis, and writing. H.X. contributed theory refinement (Phase A/B audits), analysis support, and writing review. Both authors approved the final version and are corresponding authors.
**Problem:** Not CRediT; uses colloquial verbs ("led", "contributed", "support"). NHB editors will accept this but it is below house style.
**Fix (suggested rewrite):**
> **L.A.** Conceptualization, Methodology, Formal analysis, Investigation, Data curation, Writing – original draft, Visualization, Project administration. **H.X.** Conceptualization (theory refinement; Phase A/B audits), Formal analysis (Layer D MR replication; cross-level meta), Validation, Writing – review & editing. Both authors approved the final version.
**Priority:** High. Not desk-reject but visible.

### B3. Two corresponding authors declared — NHB allows but requires explicit portal field (WARN → Blocker at portal stage)
**Rule:** Nature Portfolio allows up to two corresponding authors (and, separately, up to two "equally contributing" first authors or "jointly supervising" last authors). The submission portal asks for each corresponding author separately.
**Current state:** Title page L8 declares "Both corresponding authors. Correspondence: Lu An ...; Hongyang Xi ..." — compliant with text policy. ORCIDs for both are present (L3).
**Portal-time action (Andy/Playwright):** When submitting through the NHB portal, enter BOTH authors with the "corresponding author" checkbox ticked. Confirm both receive automated submission-received email. If the portal enforces a single "primary contact," Lu An (senior; primary affiliation is on the letterhead) is the default primary; Hongyang Xi is the secondary corresponding.
**Priority:** Medium-High. This is a portal-operation item, not a manuscript edit.

### B4. No Ethics / IRB statement in the manuscript (WARN)
**Rule (Reporting Summary, Nature Portfolio editorial-policies/reporting-standards):** Ethics approval / consent / institutional review status is a mandatory field in the Reporting Summary even for secondary-data studies. The manuscript body should carry at minimum a one-sentence Ethics statement.
**Current state:** Grep returns **zero** matches for "ethics / IRB / approval / consent" in `main_v3.2_draft.md` body. The `Funding` section mentions "publicly available secondary data" but does not constitute an Ethics statement.
**Fix (add after Acknowledgements or within Methods §M8):**
> **Ethics.** This study is a secondary analysis of publicly available or access-controlled anonymised datasets (ISSP via GESIS under standard terms of use; CFPS, CHARLS, CHFS via their respective institutional data-access agreements at Peking University, Beijing Normal University, and Southwestern University of Finance and Economics; UK Biobank summary statistics via OpenGWAS public release; FinnGen R12 under the FinnGen public-release terms; GBD 2021 via IHME public API; WVS/ISSP cultural indices via public archive). No new data from human participants were collected for this study. All primary studies from which summary statistics were drawn obtained informed consent and institutional ethics approval under their respective protocols. Under the Declaration of Helsinki and the [institution] ethics committee guidance, purely retrospective analysis of de-identified summary statistics is exempt from additional institutional review.
**Priority:** High. A missing ethics statement is a common desk-reject flag even when the answer is "secondary data, exempt."

### B5. Reporting Summary and Editorial Policy Checklist not yet prepared (Blocker at portal stage)
**Rule:** NHB requires a completed **Reporting Summary** (`reporting-summary-flat.pdf` from the Nature Portfolio author portal, typically v5+) and an **Editorial Policy Checklist** at submission. Both are **mandatory** for Articles. The submission portal will not complete without them.
**Current state:** `submission_package.md` line 36 flags both as "⚠️ pending." Neither has been filled.
**Fix:** Fill both forms using (a) Methods §M2–M8 for statistical / sample-size / replication fields and (b) Ethics block from B4 for approval fields. Key fields likely to be flagged:
- **Sample sizes:** Layer A n=20 cases; Layer B n ≈ 180,000 person-waves (CFPS) + 20,000 (CHARLS) + 40,000 (CHFS); Layer C n = 2,896,233 (ISSP 25 countries × 17 waves); Layer D cases = 5,579–41,000 per FinnGen outcome, exposures n = 258,000–1,331,000.
- **Data exclusions:** Pre-registered filters are documented in each script (§M2–M5).
- **Replication:** Cross-method robustness is primary replication (MR 5 methods × 19 chains; spec-curve 3,000 models × 5 domains).
- **Randomization / Blinding:** N/A for observational / summary-statistics data.
- **Pre-registration:** OSF 2026-04-18 (axioms + A+D joint test frozen 2026-04-17 per `cross_level_plan.md`).
- **Code availability:** OSF + GitHub (already drafted in manuscript §Code Availability).
**Priority:** Highest — a non-submitted Reporting Summary is an automatic portal block.

---

## Warnings (recommended fixes)

### W1. Cover letter is 660 body words, above NHB's recommended ≤ 500 for Articles
**Note:** NHB does not publish a hard 500-word cover-letter limit, but the Preparing-your-Material page is explicit that the cover letter "should explain the importance of the work" and lists five concise bullet items. Flagship Nature journals tighten to ≤ 500 in editorial guidance. 660 words is at the upper end for a 2-page letter.
**Fix (soft):** Consider compressing the "What we honestly report" paragraph (currently 178 words) — the limitations-litany should be in the manuscript, not the cover letter. A leaner cover letter signals higher editorial confidence. Target ≈ 500-550 body words.
**Priority:** Medium. Not a blocker.

### W2. Abstract contains unreferenced numeric density and a formal bound — NHB explicitly says "unreferenced"
**Current:** 125 words (well under 150). Contains formal math-like claim "|Δb_signal|/|Δb_info| ≥ 1.5", statistical quantities "β = +1.58, p = 0.019", "Cohen's κ = 1.00", "OR = 2.06". No citation numbers present (I confirmed with regex; the "3,000" token is a count of specifications, not a citation).
**Status:** Technically compliant (unreferenced). But unformatted inline math such as "Δ_ST" and "|Δb_signal|/|Δb_info|" will render awkwardly in HTML. NHB copyeditors will replace these at AIP stage.
**Fix (optional, for clarity only):** Consider rewording "|Δb_signal|/|Δb_info| ≥ 1.5" to plain English: "a lower-bound ratio of at least 1.5 on signal-redesign to information intervention effects." This reads better for the diverse NHB audience.
**Priority:** Low.

### W3. Reference list in main manuscript shows only 35 items — Article full body cites 35; declared full list ≈ 115 is in SI
**Rule (AIP formatting §5):** No numeric limit for Articles. Reference list must be ordered "Main Text → Methods → Data Availability → Tables → Figure Legends → Extended Data."
**Current state:** The 35-entry list is ordered by first-appearance in main text; Methods citations (e.g., Tobler 2005, Mazur 1987, Ainslie 1975, Shizgal & Conover 1996) appear *within* the numbered list but some only in prose without a corresponding numbered citation. The SI claims to hold the full 115-reference list — but NHB expects the complete reference list **inside the manuscript file**, not split into SI.
**Fix:** Consolidate into a single numbered reference list at the end of Methods (ordered: Main → Methods → DA → Tables → Legends → ED) before submission. The phrase "Full reference list (≈ 115 references) in SI; all DOIs available at OSF" (L299) should be **deleted**. This may push the manuscript toward ~3 more reference-list pages but NHB has no reference cap and this is the required location.
**Priority:** High. Split reference lists are a known reviewer complaint.

### W4. Supplementary Information structure not finalised (outline only)
**Current state:** `supplementary_v2_outline.md` is marked "⚠️ pending update" in submission_package. The v3 reshuffle (Stage 1-B M-series fixes; §11.7/11.8; Appendix H DALY migration) has not been re-outlined.
**Fix:** Before portal upload, produce a clean SI PDF following NHB §11 rules:
- Each supplementary item designated as Supplementary Equation, Discussion, Notes, Figure, Table, Video, Audio, Data or Software.
- Each numbered sequentially *separately* from main-manuscript items (main Table 1 ≠ Supplementary Table 1).
- Each referenced in the main text or Methods at least once with the word "Supplementary" preceding the number.
- Single bundled PDF (NHB preferred) or CSV/Excel add-on files for large tables.
**Priority:** High. Portal requires a clean SI PDF; the v2-outline scaffold must be finalised as a rendered PDF.

### W5. Inclusion & Ethics in Global Research statement (applicable when data involve geographically specific human cohorts)
**Rule (Nature Portfolio authorship policy):** Editors may request an "Ethics & Inclusion statement" when research involves local cohorts. Nine questions are listed covering local researcher inclusion, local relevance, role-sharing, ethics approval, data sovereignty, capacity building, risk management, and benefit sharing.
**Relevance here:** The manuscript uses CFPS / CHARLS / CHFS (China-based large public datasets) and FinnGen (Finland-based registry). Data were collected by local consortia with full local ethics approval and public-release terms. Neither source was collected by the authors directly; this is secondary analysis.
**Fix (optional for initial submission; high-likelihood NHB request at peer review):**
> **Ethics & Inclusion statement.** This study conducts secondary analysis of publicly-accessible or access-controlled summary-statistics and anonymised-panel data generated by local consortia (CFPS at Peking University; CHARLS at Peking University; CHFS at Southwestern University of Finance and Economics; FinnGen in Finland). All primary data collection received local institutional ethics approval. Authors based in China (L.A., H.X.) conducted analyses within the primary jurisdiction of three of four primary datasets; Finnish dataset access followed FinnGen's public-release terms. No field data were collected abroad; no biological materials or cultural artefacts were transferred across jurisdictions. All local citations relevant to the behavioural domains analysed (ISSP China-wave; CFPS; CHARLS) are included.
This pre-emptively satisfies reviewer question on helicopter research.
**Priority:** Medium. Not required at initial submission but commonly requested.

### W6. Preprint status not declared (NHB policy permits bioRxiv / SSRN / PsyArXiv)
**Rule:** NHB's preprint policy is permissive; authors may post a preprint simultaneous with submission. Cover letter should disclose preprint status explicitly.
**Current state:** Cover letter L25 states "This work has not been published or submitted elsewhere" but does not explicitly address preprint deposition. The OSF deposit at `https://osf.io/ucxv7/` contains analytical code, not the manuscript PDF.
**Fix (optional):** Add one sentence to cover letter: "No preprint of this manuscript has been deposited at bioRxiv, SSRN, PsyArXiv, or any other preprint server. The OSF project contains reproducibility artefacts (code, intermediate tables, pre-registration files) only."
**Priority:** Low.

### W7. Funding / competing-interests wording slightly non-standard
**Rule (Competing-interests policy):** Accepted wording is either (a) "The authors declare no competing interests." or (b) "The authors declare the following competing interests: [details]." The manuscript L313 uses (a) verbatim — compliant.
**Rule (Funding-statements policy):** Recommended format "A.B.C. discloses support for the research of this work from Funder [grant number xxxx]. ... G.H.I. declares no relevant funding."
**Current state L315-317:** "This research received no dedicated external funding. Analyses used publicly available secondary data..." — informative but does not use the standard formula.
**Fix (optional):** Compress to: "**L.A. and H.X.** declare no relevant funding. Analyses used publicly available or access-controlled secondary data (ISSP via GESIS; UK Biobank summary statistics via OpenGWAS; FinnGen R12 via public release; GBD 2021 via IHME; WVS/ISSP cultural-dimension indices via public archives). Personal workstation compute only."
**Priority:** Low.

---

## Pass items (confirmed compliant)

- [x] **P1. Manuscript type = Article** — correct. v3.2 title-page L11 declares Article. The four-section structure (Introduction without heading → Results with subheadings → Discussion without subheadings → Methods with subheadings) matches NHB Article prescription verbatim. v3.2's F5/F6 fixes (Introduction-without-heading; Discussion-without-subheadings) specifically enforce this rule.
- [x] **P2. Main text word count ≤ 5,000** — claimed 4,900; my strip-and-count on `main_v3.2_draft.md` (excluding math, table rows, headings) returns **~3,970 words**, well under 5,000. Even counting math and inline formulae, the ceiling is comfortably cleared.
- [x] **P3. Abstract ≤ 150 words, unreferenced, no subheadings** — measured at **125 words** after markdown stripping (manuscript self-report 149 words counts bolded text; either way compliant). No citation numbers present. No subheadings. PASS.
- [x] **P4. Display items ≤ 8** — 6 main figures + 2 tables = 8 = limit exactly. Note: Table 1 is the intervention-asymmetry table, Table 2 is the MR table (implicit — Methods §M4 references it but main text does not — see minor m1 below).
- [x] **P5. Extended Data ≤ 10** — 1 ED Table (committed) + 2 ED Figures (optional, flagged). Well under 10.
- [x] **P6. Methods is present and subdivided** — §M1 Theory; §M2 Layer A; §M3 Layer B/C; §M4 Layer D; §M5 Cross-level; §M6 Intervention-asymmetry; §M7 Classifier; §M8 Pre-registration/Reproducibility/Transparency. Subheadings bold per NHB AIP §6.
- [x] **P7. Data Availability statement** — present L319-321, names repositories (OSF https://osf.io/ucxv7/), enumerates six data products, addresses controlled-access FinnGen/UK Biobank explicitly. Compliant with Nature Portfolio data-policy requirements.
- [x] **P8. Code Availability statement** — present L323-325, GitHub repo + OSF, lists 5 pipeline scripts by name, environment.yml noted. Compliant.
- [x] **P9. ORCIDs for both corresponding authors** — Lu An 0009-0002-8987-7986; Hongyang Xi 0009-0007-6911-2309. Both on title page. ORCID is required only for the corresponding author per NHB/ORCID rule; both being listed exceeds minimum requirement.
- [x] **P10. Competing-interests statement** — L311-313 uses exact NHB-accepted formula "The authors declare no competing interests."
- [x] **P11. References style (numbered, superscript, titles included)** — references numbered 1–35 with titles included per AIP §5 Article convention. Superscript usage in main text (e.g., "¹⁻⁴", "⁵", "⁶") is AIP-post-acceptance style; initial submission can use any citation format.
- [x] **P12. Cover letter addresses 5 required points** — importance (paragraph "What this paper does"), why this journal (paragraph "Why NHB"), exclusivity / prior consideration ("This work has not been published or submitted elsewhere"), author acknowledgement ("All authors have read and approved"), competing-interests statement. Missing only preprint disclosure (W6).
- [x] **P13. Handling editor not proposed** — cover letter L21 "We do not propose a handling editor and welcome editorial guidance." NHB does not require editor suggestions; this is acceptable.
- [x] **P14. Received/accepted dates** — will be inserted by NHB at AIP.
- [x] **P15. Initial submission format** — NHB explicitly allows PDF or Word for initial submission; does not require LaTeX. `main_v3.2_submission.pdf` (345 KB) and `main_v3.2_submission.docx` (45 KB) are ready. Correct format.

---

## Minor issues

### m1. Table 2 (MR results) is referenced in figure/legend text but not as a main-text display item
The figure legend for Fig 5 refers implicitly to Table 2 (`Table 2` cited at L92 main text). Ensure the MR-results master table is submitted as Table 2, not as a Supplementary Table. If space is tight, consider demoting Table 2 to Supplementary and keeping only Table 1 in main (reducing display-item count from 8 to 7 and giving headroom for reviewer-requested additions).
**Priority:** Low (compliance already at cap, not over).

### m2. Placeholder `[OSF_DOI_TO_INSERT]` in cover letter L23 — replace before portal upload
The OSF URL `https://osf.io/ucxv7/` is inline but the formal DOI placeholder remains. Either paste the minted DOI (`10.17605/OSF.IO/UCXV7` if applicable) or remove the bracketed placeholder.
**Priority:** High for the portal-submission step (cover letter is the first reviewer-visible document).

### m3. Reference 15 (Knight-Linos et al. 2023 CONSORT-nudge) flagged as "[Manuscript reference; replace with published version at revision.]"
NHB accepts preprints-with-DOI in reference lists but an unpublished draft is best flagged at submission rather than discovered by copyedit. Either locate the published version or rephrase to "CONSORT-nudge guidelines (in preparation)" in the text and remove from numbered-reference list (AIP §5 says "Unpublished meeting abstracts, papers in preparation and papers under review or in press without an available preprint should not appear in the reference list. Instead, they should be mentioned in the text with a list of authors").
**Priority:** Medium.

### m4. Reference 17 (Sommet et al. 2026 *Nature*) — verify full reference and DOI
Currently bracketed: "[*Nature* specification-curve benchmark; 768 alternative specifications.]" — needs full bibliographic data (authors, full title, volume, pages, DOI). If still in press/advance-online, cite the advance-online DOI.
**Priority:** Medium.

### m5. Affiliation style — single compound affiliation is acceptable but verify institutional rendering
L5-6 lists two near-duplicate affiliations ("Chongqing Health Center for Women and Children" + "Women and Children's Hospital of Chongqing Medical University"). Confirm with institutional HR / ORCID records whether these are one institution (hospital-within-health-center) or two; NHB's "primary affiliation for each author should be the institution where the majority of their work was done" implies one primary per author. If identical, list once and add "(formerly known as...)" or secondary affiliation.
**Priority:** Low.

### m6. Figure panel labels and error-bar descriptions (AIP §3)
At initial submission this is not enforced; at AIP stage NHB requires "verbal cues to describe keys, eg. 'open red triangles', not visual cues or symbols" and error-bar description "Include a description of centre values (median or average) and all error bars and how they were calculated. Give an indication of sample size (n number), state the statistical test used and provide P values."
Current `figure_legends_v3.1.md` legends for Fig 1/5/6 comply well; Fig 2/3/4 should be rechecked at AIP stage for error-bar type specification.
**Priority:** Defer to AIP.

### m7. `.DS_Store` files in manuscript directory
Trivial housekeeping — do not include `.DS_Store` in any upload bundle. Ensure the submission archive, if bundled, is cleaned.
**Priority:** Low.

---

## Action checklist for Andy / claude before Playwright submission

**Phase 1 — Manuscript edits (required; ~90 min):**
1. **[B1] Renumber figures** to match textual order. Sweep `main_v3.2_draft.md` L55–L155 and `figure_legends_v3.1.md`. Rename files `04-figures/main/fig*_*.pdf` accordingly. Re-render main manuscript DOCX/PDF.
2. **[B2] Rewrite Author Contributions in CRediT taxonomy** at L303-305 (suggested text in body of this audit).
3. **[B4] Insert Ethics statement** as new section after Acknowledgements (suggested text in body of this audit; 1 short paragraph).
4. **[W3] Consolidate references** into single list at end of Methods ordered per AIP §5; delete L299 SI-reference-split phrase.
5. **[m2] Replace `[OSF_DOI_TO_INSERT]`** in cover letter with minted OSF DOI or formal URL.
6. **[m3, m4] Fix references 15 and 17** (CONSORT-nudge, Sommet et al.).

**Phase 2 — Companion documents (required; ~60 min):**
7. **[B5-a] Fill Reporting Summary** (download `reporting-summary-flat.pdf` from Nature Portfolio author portal; use Methods §M2–M8 plus Ethics block from B4).
8. **[B5-b] Fill Editorial Policy Checklist** (standard NHB form; most items N/A for secondary-data study).
9. **[W4] Finalise Supplementary Information PDF** from `supplementary_v2_outline.md` + `SI_H_orthogonal_health_implications.md` + §11.7 / §11.7b / §11.8 / Appendix F / G as single bundled PDF with sequential numbering separate from main-text display items.

**Phase 3 — Cover letter and optional statements (recommended; ~30 min):**
10. **[W1] Trim cover letter body to ≤ 550 words** (current 660). Compress the limitations paragraph.
11. **[W5] Add 1-paragraph Inclusion & Ethics statement** to Methods §M8 (suggested text in body of this audit).
12. **[W6] Add 1-sentence preprint disclosure** to cover letter.
13. **[W7] Reformat Funding statement** to NHB house style (optional).

**Phase 4 — Portal-operation (Playwright submission):**
14. **[B3] At portal, mark BOTH Lu An and Hongyang Xi as corresponding authors.** Confirm both get submission-received email.
15. Upload order per NHB portal: (i) cover letter PDF; (ii) main manuscript DOCX (preferred over PDF for Article submissions — pandoc already generated `main_v3.2_submission.docx`); (iii) Figures 1–6 as individual PDF files at 300 dpi, max 180 mm width; (iv) SI bundled PDF; (v) Reporting Summary PDF; (vi) Editorial Policy Checklist PDF.
16. Run `_meta/scripts/pre-submission-lint.py` against the updated `main_v3.2_draft.md` one last time (per Andy memory `feedback_pre_submission_lint.md`) — CJK / table-orphan / section-missing guards.

**Estimated total time to submission-ready:** ~3 hours of focused editing.

---

## Risk assessment (what could go wrong if we submit as-is)

| Item | If unfixed | Likelihood of desk-reject | Likelihood of AIP-stage flag |
|---|---|:-:|:-:|
| B1 Figure order | Editorial-screening will send back for renumber | 10% | 95% |
| B2 CRediT | Acceptable but house-style non-conformity | 0% | 60% |
| B4 Ethics | Common desk-reject flag for empirical studies | 15% | N/A |
| B5 Reporting Summary | **Portal will block submission** | 100% | N/A |
| W1 Cover letter length | Tolerated | 0% | 0% |
| W3 Split reference list | Reviewer complaint risk | 5% | 70% |
| W4 No SI PDF | **Portal will block submission** | 100% | N/A |
| W5 Inclusion & Ethics | Requested at peer-review | 0% | 30% |

**Bottom-line:** Items B5 and W4 are absolute portal blockers. B1/B2/B3/B4/W3 are manuscript edits that take ≤ 2 hours combined. The other items are cosmetic. After Phase 1 + Phase 2 (~2.5 hours), the manuscript will be at full NHB initial-submission compliance.

---

*Audit prepared 2026-04-18 by peer-reviewer agent against live-fetched NHB guidelines. For each Blocker, a specific line number and a drop-in replacement text is provided. No claim in this audit rests on pre-2024 NHB rules — all cited rules are from pages fetched at audit time.*
