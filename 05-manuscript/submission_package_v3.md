# Submission Package v3.0 — Nature Human Behaviour Article

**Manuscript title:** Sweet Trap: a theory of reward–fitness decoupling with cross-species empirical validation
**Authors:** Lu An¹,²,\* (0009-0002-8987-7986), Hongyang Xi¹,²,\* (0009-0007-6911-2309)
**Target:** *Nature Human Behaviour* — Article.
**Submission date:** 2026-04-18.

---

## 1. Required files checklist

| File | Status | Location | Word count |
|---|---|---|---|
| Cover letter | ready | `05-manuscript/cover_letter_nhb_v3.md` | 739 words (body; within NHB guidance) |
| Main manuscript (theory + empirics + Methods) | ready | `05-manuscript/main_v3.0_draft.md` | 8,697 total (Abstract 294; Main 4,484; Methods 2,773; Refs 866) |
| Standalone abstract | ready | `05-manuscript/abstract_v3.0.md` | 293 words |
| Supplementary Information outline | ready | `05-manuscript/SI_v3.0_outline.md` | 2 blocks: SI-Math (~3,500w); SI-Empirical A–I |
| Figure legends | **pending final** | `05-manuscript/figure_legends_v3.md` (v2.4 figure_legends_v2.4.md reusable base) | 9 main + 13 SI figures |
| Supplementary figures | — | existing v2.4 + new Fig. 8 (v2.4 spec) | 13 figures |
| Extended Data | — | ED Table 1 (positioning matrix); ED Fig. 1 (containment diagram) | 2 items |
| Data-availability statement | in manuscript + OSF | OSF DOI `[OSF_DOI_TO_INSERT]` | — |
| Pre-registration | deposited | OSF 2026-04-18; Paper 1 axioms + cross-level A+D plan (2026-04-17) | — |
| Reporting summary | **pending final** | NHB template to fill | — |
| Life-sciences checklist | **not applicable** | — | — |
| Behavioural & social-sciences checklist | **pending final** | NHB template to fill | — |

---

## 2. NHB Article length compliance

| Constraint | Budget | Actual | Status |
|---|---|---|---|
| Main text (Intro + Theory + Results + Discussion) | ≤ 4,500 words | 4,484 words | OK |
| Methods | 3,000–4,000 words | 2,773 words | OK (lower than midpoint; SI-Math carries theoretical detail) |
| Abstract | ≤ 300 words | 293 words | OK |
| References | ≤ 70 typical | 35 short-form + ≈ 80 in SI | OK |
| Main figures | up to 6 | 9 (NHB negotiable on merit) | to confirm |
| Main tables | up to 2 | 2 | OK |

Main-text length is 16 words below ceiling (99.6% utilisation). Abstract is 7 words below ceiling.

---

## 3. Data and code availability

### 3.1 Public data
- **ISSP 1985–2022**: GESIS archive, public-access.
- **Hofstede 6D**: Hofstede archive.
- **UK Biobank GWAS summary statistics**: via primary publications (Karlsson Linnér 2019; Saunders 2022; Okbay 2022; Locke 2015; Okbay 2016; Jansen 2019).
- **FinnGen R12**: finngen.fi/en/access_results (2024-12 release).
- **GBD 2021**: Institute for Health Metrics and Evaluation.

### 3.2 Restricted-access data
- **CFPS 2010–2020**: Peking University, via institutional application.
- **CHARLS 2011–2020**: Peking University.
- **CHFS 2011–2019**: SWUFE, via institutional application.
- **HRS, PSID**: US replication subsets under existing approvals.

### 3.3 Code and processed tables (OSF deposit)
- `02-data/processed/cross_level_effects_table.csv` (Layer A–D harmonised effect rows).
- `02-data/processed/layer_A_v2_extraction.csv` (20 animal cases).
- `02-data/processed/mr_results_all_chains_v2.csv` (19 MR chains, 5 methods, 3 MVMR).
- `02-data/processed/issp_panel_1985_2022.csv` (2,226 country × wave × variable cells).
- `02-data/processed/discriminant_validity_features.csv` (10 + 8 adversarial cases).
- `02-data/processed/intervention_asymmetry_table.csv` (6 domains × 2 intervention types).
- `02-data/processed/mortality_daly_anchor.json` (Appendix H orthogonal accounting).
- `03-analysis/scripts/*.py` and `03-analysis/scripts/*.R` pipelines.
- `04-figures/*/*.R` figure-generation scripts.

### 3.4 Paper 1 theory documents (OSF)
- `paper1-theory/01-math-foundation/axioms_and_formalism.md` (axioms A1–A4; Stage 1-B revised).
- `paper1-theory/01-math-foundation/relationship_to_existing_models.md` (7-theory positioning).
- `paper1-theory/01-math-foundation/nomenclature.md` (symbol table).
- `paper1-theory/02-theorems/theorems.md` (T1–T4, proof sketches; Stage 1-B revised).
- `paper1-theory/02-theorems/lemmas.md` (L1–L5 including new L4.1 mean-field).
- `paper1-theory/02-theorems/proof_sketches_expanded.md`.
- `paper1-theory/03-predictions/predictions.md` (v1.1 post-audit empirical status).
- `paper1-theory/03-predictions/minimal_experimental_paradigm.md` (for Appendix G).
- `paper1-theory/04-positioning/positioning.md`.
- `paper1-theory/00-outline/revision_log_stage1B.md` (F1–F3 + M1–M8 before/after).
- `paper1-theory/00-outline/integrity_audit_log.md` (P1–P5 audit).
- `paper1-theory/05-manuscript/math_supplement.md` (basis for SI-Math block).

---

## 4. Pre-submission lint checks (per `_meta/scripts/pre-submission-lint.py`)

- [ ] Run `_meta/scripts/pre-submission-lint.py` on main_v3.0_draft.md (CJK, table-orphan, section-missing detection).
- [ ] Verify all inline citations [1]–[35] resolve to the short-form reference list.
- [ ] Verify all figure / table cross-references resolve (Fig. 1–9, Table 1–2, ED Table 1, ED Fig. 1, SI-M1, SI-A1–A2, SI-B1–B3, SI-H1).
- [ ] Verify all supplementary-section cross-references (§M1–M8; Appendix A–I; SI-Math §1–§9).
- [ ] Verify all OSF placeholder strings `[OSF_DOI_TO_INSERT]` are replaced at OSF registration finalisation.
- [ ] Verify all author ORCIDs and postal addresses match `user_author_identity` memory.

---

## 5. Author and funding declarations

- **Correspondence:** Lu An <113781@hospital.cqmu.edu.cn>; Hongyang Xi <26708155@alu.cqu.edu.cn>.
- **Author contributions:** L.A. led conception, theory, analysis, writing. H.X. contributed theory refinement (Phase A/B audits), analysis, review. Both approved final and are corresponding authors.
- **Competing interests:** None declared.
- **Funding:** No external funding.
- **IRB / ethics:** Secondary-data analysis only; original approvals held by source-data custodians (CFPS PKU; CHARLS PKU; CHFS SWUFE; UK Biobank; FinnGen).
- **Acknowledgements:** ISSP / GESIS; CFPS Peking University; UK Biobank; FinnGen R12 consortium; Paper 1 Phase D and Paper 2 Red Team v1–v4 audits archived at OSF.

---

## 6. Communication with editor

The cover letter **does not** nominate a handling editor (per Andy's investigation protocol). It explicitly requests editorial guidance.

Per user memory `user_author_identity`, if reviewers request handling-editor suggestions in revision, candidates include (1) Sander van der Linden (Cambridge; belief/misinformation intersection); (2) Colin Camerer (Caltech; behavioural-economic theory); (3) David Laibson (Harvard; hyperbolic discounting theory); (4) Molly Crockett (Princeton; social decision-making). This list is deferred to revision-stage if requested.

---

## 7. Post-acceptance commitments

- **Pre-registration.** OSF DOI `[OSF_DOI_TO_INSERT]` to be finalised upon conditional acceptance; axioms frozen 2026-04-18, cross-level A+D plan frozen 2026-04-17.
- **Code deposit.** Complete pipeline as `sweet-trap-multidomain` GitHub repository, tagged with NHB DOI upon acceptance.
- **Data deposit.** All processed aggregate tables in OSF; individual-level data remain under source-custodian approvals.
- **Minimal experimental paradigm.** Appendix G protocol to be pre-registered as Stage-2 Registered Report upon NHB acceptance; pilot RCT planned for 2026-Q3 on Prolific.
- **Post-publication agenda.** (i) Unit-matched Borenstein-Cohen-d harmonised ratio across all six intervention-asymmetry domains; (ii) P2 persistence-rank compilation on all 44 Layer A/B/D cases; (iii) P4 matched-platform TikTok-vs-YouTube engagement-trajectory test; (iv) full analytical derivation of L4.1 mean-field RST; (v) rigorous basin-radius lower bound (Observation 4.1 → theorem).

---

*End of submission package v3.0. Go-no-go signed off on the pre-submission-lint sweep before send.*
