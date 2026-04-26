# v2 → v2.1 Diff Summary

**Date:** 2026-04-18. **Author agent:** manuscript-writer.
**Scope:** 3 audit-driven revisions (A2 + A3 + selection-B) to `main_v2_draft.md` → `main_v2.1_draft.md`.

---

## A2 — DALY headline dual-anchor (Steiger-correct floor + extended envelope)

**Why.** Red Team v2 + Novelty Audit v2 converged: 11/19 Steiger ✗ chains mean the extended 34.6 M figure violates primary-filter norms (Hemani et al. 2017). Tier-1 Steiger-correct alone = 4.1 M — still ≈ Parkinson's. The "10× Parkinson" claim must not be the only headline.

**Changed.**
- **Title** now "4.1–34.6 million DALYs per year globally" (dual range).
- **Abstract** closing finding sentence → "4.1–34.6 million DALYs per year globally (Steiger-correct conservative floor to extended-inclusion envelope), equivalent to ≥1× Parkinson's disease burden and up to 10× under broader inclusion criteria."
- **Introduction contribution 4** restated with dual anchor.
- **§5 Results** Steiger paragraph rewritten to reference §8.3 rationale.
- **§8** restructured into three subsections:
  - §8.1 Primary: Tier-1 Steiger-correct 4.1 M as headline.
  - §8.2 Extended envelope: full 34.6 M.
  - §8.3 Steiger directionality rationale (socially-stratified GWAS).
- **Discussion limitations #1** rewritten around dual anchor.
- **Discussion closing** reframed "at least Parkinson's, plausibly order of magnitude larger."
- **Methods M7 + M10** updated to reflect primary vs extended anchor.
- **Figure 8 caption** rewritten as dual-anchor chart (side-by-side bars, both headlines labelled).

## A3 — Cross-level honest restatement (A+D p = 0.019 primary; three-layer p = 0.47 acknowledged)

**Why.** Red Team flagged ρ(A,D) = +1.00 on n = 2 cells as a geometric identity. Abstract/§6 overstated cross-level concordance. Must promote pre-registered A+D β = +1.58, p = 0.019 and openly report three-layer p = 0.47.

**Changed.**
- **Abstract** cross-level sentence rewritten: "In a pre-registered A+D joint analysis, the animal-mechanism rank predicts the human genetic-causal rank (β = +1.58, p = 0.019 on z-scale). The full three-layer test yielded Wald χ²(2) = 1.51, p = 0.47 due to an anomalous Layer B case (C13 housing); the A+D subset is reported as the pre-registered secondary test."
- **Introduction contribution 3** replaced ρ = +1.00 framing with the A+D β = +1.58 formulation.
- **§6** restructured into four subsections:
  - §6.1 Primary three-layer test: χ²(2) = 1.51, p = 0.47 (non-significant, reported openly).
  - §6.2 Pre-registered secondary A+D: β = +1.58, p = 0.019.
  - §6.3 C13 anomaly discussion — reclassification rescue (p = 0.033) labelled **exploratory, not primary**.
  - §6.4 Explicit caveat: n = 2 cells ρ = +1.00 is geometric identity, not inferential.
- **Discussion opening** recast ("not the three-layer aspirational goal [p = 0.47] but a two-layer pre-registered prediction").
- **Discussion limitations #5 + #7** added explicit statements of p = 0.47 and n = 2 geometric identity.
- **Methods M9** documents pre-registration of A+D as secondary (frozen 2026-04-17) and labels C13 reclassification as exploratory.
- **Figure 9 caption** rewritten: three-layer p = 0.47 shown in grey, A+D β = +1.58 highlighted as primary, ρ = +1.00 demoted to descriptive panel (d) with geometric-identity caveat.

## Selection B — §11.7 Engineered Deception extension (pig-butchering + PUA)

**Why.** Strengthens Engineered sub-class from single-case (C12) to a family of two sub-sub-classes, adds cross-operator mechanism evidence (human vs algorithmic both producing variable-ratio Olds–Milner phenotypes), and illustrates held-out positive classifier predictions.

**New file.** `s11_7_engineered_deception.md` (≈ 1,800 words). Contains:
- §11.7.1 Sub-class family promotion (Algorithmic vs Deception, same F1+F2 rule).
- §11.7.2 Pig-butchering case — F1=1, F2=1, F3=1, F4=0.5; S = 5.5 > 4.0 → Positive. Cites FBI IC3 2023, China MPS 2023, INTERPOL 2023, UNODC 2023. Animal homology: anglerfish, Photuris firefly, bolas spider (aggressive mimicry).
- §11.7.3 PUA case — F1=1, F2=0.5, F3=1, F4=0.5; S = 4.5 > 4.0 → Positive (borderline). Shares Olds–Milner variable-ratio schedule with C12. Cites Dutton & Painter 1993, Stark 2007.
- §11.7.4 F2 strict-boundary statement: aspirational-under-deception = 1, externally-compelled = 0, late-phase trauma-bonded = 0.5.
- §11.7.5 Methods §2.4 integration (Engineered Algorithmic vs Engineered Deception).
- Both cases are held-out positive classifier predictions; they do NOT enter dev-set κ.

**Changed in main text.**
- **Discussion §"Second" paragraph** rewritten to cover the Algorithmic vs Deception sub-sub-class distinction; PUA ↔ C12 variable-ratio schedule homology highlighted as additional within-family universality evidence.
- **Discussion limitations #8** added acknowledging §11.7 cases are held-out positive predictions, not independently coded.
- **References** added Lloyd 1975, Dutton & Painter 1993, FBI IC3 2023.

## Other minor v2.1 edits

- **§7 Discriminant validity** — "Cohen's κ = 1.00" replaced throughout with "dev-set accuracy = 1.00" + "Cohen's κ from blind second coder pending (target > 0.75)". Figure 4 caption reflects this.
- **§11.6 OSF statement** (in Methods M12) — "OSF time-stamp will be obtained at submission; all analytical decisions are date-stamped in the §11 limitations log and in `00-design/pre-analysis/`."
- **Data and code availability** — expanded to list processed file paths and pre-registration folder location (addresses Novelty v2 reproducibility −1).

## Word-count delta

- v2 main text: ≈ 4,250 words → v2.1 main text: ≈ 4,380 words (+130; within 7,000–7,500 total budget)
- v2 Methods: ≈ 3,900 words (≈ unchanged; only M7/M9/M10/M12 substantively edited).
- New standalone `s11_7_engineered_deception.md`: ≈ 1,800 words (supplementary / structured into §11 of formal model doc; not in main-text count).
- Total package: ≈ 7,280 words main+methods, within NHB Article budget.

---

*v2.1 freezes 2026-04-18. All three priority actions (A1 blind κ; A2 dual anchor; A3 honest restatement) are now either executed (A2, A3, B) or flagged-pending (A1 blind κ target > 0.75, deferred to revision round 1).*
