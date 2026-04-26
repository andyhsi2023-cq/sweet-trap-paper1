# Supplementary Appendix H — Orthogonal health-implications analysis

**Status (v2.4, 2026-04-18):** *Secondary orthogonal analysis; not a primary claim of the construct paper.*

This appendix explores the downstream global-health footprint of Sweet Trap mechanisms by linking the MR-identified chains of Layer D (main-text §5) to GBD 2021 disease totals via Levin's population-attributable-fraction formula. The analysis was the main-text §8 in manuscript v2.3 and is retained in the Supplementary Information in v2.4 as a secondary observation that a reader focused on public-health accounting may find useful. **The paper's primary contribution is theoretical (cross-species construct + F1 + F2 classifier + pre-registered A + D concordance + derived policy-predictability prediction in main-text §8 and §11.8) rather than epidemiological.**

This framing matters. The construct paper does not claim the DALY figures below as an independent contribution; the figures re-aggregate GBD-attributed conditions that happen to overlap with the Sweet Trap domain set. Aggregating GBD totals for behaviours the construct already defines as Sweet Traps is circular if read as a "Sweet Trap causes X DALYs" attribution; it is non-circular only as a descriptive statement of *orthogonal scale* — i.e., "the MR-identified chains that survive construct-inclusion criteria map to exposure–disease pairs on the order of Parkinson's-disease burden globally." We report it that way.

---

## H.1 Methods: Levin PAF linkage to GBD 2021

**Formula.** Levin (1953) PAF = P_e (OR − 1) / [P_e (OR − 1) + 1]; attributable DALY = PAF × GBD-2021 disease total. Uncertainty envelope: 3 × 3 grid over (P_e, OR) 95% bounds; PAF_lo / PAF_hi are the min / max of the nine combinations.

**De-duplication.** Outcome aliasing (antidepressants → F5_DEPRESSIO pool; keep larger |PAF|). Shared outcome across different exposure families is retained (alcohol and smoking as independent GBD risk factors for K11_ALCOLIV). Protective chains (PAF < 0) are excluded from the harm sum.

**GBD 2021 baselines.** T2D 75.3 M DALYs/yr, alcoholic liver 14.2 M, depression 56.3 M (IHME GBD 2021, *Lancet* 2024 suite). Exposure prevalences: BMI ≥ 25 → 43% (NCD-RisC *Lancet* 2024); heavy drinkers ≈ 10% (WHO 2024); ever-smokers ≈ 22% (GBD 2021 Tobacco Collaborators); high risk-tolerance upper tail 20% (Falk et al. 2018 *QJE*).

**Pipeline.** `03-analysis/scripts/mortality_daly_anchor.py`.

---

## H.2 Conservative floor: Steiger-correct subset

Under the conservative inclusion criterion that retains only chains with Steiger directionality = ✓ (the standard primary filter in two-sample MR; Hemani, Tilling & Davey Smith 2017, *PLoS Genet* 13: e1007081), one chain survives the filter at nominal α = 0.05 and the Levin-PAF is computable:

- risk tolerance → depression (via antidepressants): **4.1 M DALYs/yr globally** [1.0, 11.8]

This is approximately equivalent to the GBD-2021 annual global burden of Parkinson's disease (≈ 3 M DALYs/yr).

## H.3 Extended envelope: all 19 chains

Under the broader inclusion criterion that retains the full 19 chains with Steiger ✗ flagged but not excluded (on the grounds that Steiger ✗ at socially-stratified loci reflects shared molecular architecture rather than reverse causation; see main-text §M7.3), four de-duplicated chains contribute:

- BMI → type-2 diabetes: 23.6 M DALYs (68% of extended total)
- drinks-per-week → alcoholic liver cirrhosis: 4.3 M (12%)
- risk tolerance → depression (via antidepressants): 4.1 M (12%)
- smoking initiation → alcoholic liver cirrhosis: 2.5 M (7%)

**Extended total: 34.6 M DALYs/yr globally** [16.2, 64.1] — approximately 10 × the annual burden of Parkinson's disease, approximately half the burden of low back pain (≈ 66 M), and ≈ 1.2 % of the world's 2021 all-cause DALY total (≈ 2,830 M).

## H.4 Steiger directionality rationale

The 11/19 chains with Steiger ✗ are not evidence of reverse causation; they are a known property of the genetic architecture of socially-stratified behavioural exposures. The loci driving BMI (FTO, MC4R), alcohol consumption (ADH1B, ALDH2), and smoking initiation (CHRNA5) have *partially organ-specific direct molecular pathways* in addition to the behavioural channel. This produces R²_outcome ≈ R²_exposure mechanically, which flips the Steiger directionality test, *without* changing the direction of the causal pathway (Hemani 2017; Davies et al. 2019 *eLife*). A reverse-causal interpretation would require the outcome (e.g., type-2 diabetes) to be genetically upstream of BMI, which is biologically implausible for adult-onset diabetes and is contradicted by bidirectional MR (SI Appendix F).

## H.5 Sensitivity

Primary floor 4.1 M; extended envelope 34.6 M [16.2, 64.1]; large-effect-only (OR ≥ 1.5) 30.4 M; prevalence ± 20% 29.3 – 39.4 M.

---

## H.6 Why this is retained only as secondary / orthogonal observation

**Scope-of-claim honesty.** The Sweet Trap v2.4 paper is a *construct paper*, not a *burden-estimation paper*. The construct is defined by F1 (reward–fitness decoupling) and F2 (endorsement without coercion). Domains were selected for this paper on construct grounds (C8, C11, C12, C13, D_alcohol are Sweet Traps; C2, C4, D3 are not). Aggregating the GBD totals of the Sweet Trap domains is therefore a re-labelling of pre-existing GBD attribution: the Sweet Trap construct does not claim *new* DALYs beyond those already captured by GBD 2021 risk factors.

What the construct *does* claim is a **new organising principle** explaining why these exposures persist against individual welfare, and a **falsifiable intervention prediction** (main-text §11.8): in domains satisfying F1 + F2, signal-redesign interventions structurally dominate information-based alternatives. This is the paper's primary contribution. The Appendix-H DALY aggregate is a descriptive, orthogonal statistic retained for readers who wish to situate the construct's footprint on the global-health accounting scale.

**Avoiding circular attribution.** If a reader reads the Appendix-H total as "Sweet Trap causes 4–35 M DALYs", the attribution is partially circular: the construct itself selects which exposures enter the sum. We therefore present the figures as: *the MR-identified Sweet Trap chains that survive Steiger-correct / extended inclusion criteria correspond to an annual global-health footprint of 4.1–34.6 M DALYs*, which is a descriptive scale statement rather than a causal attribution.

**Non-circular alternatives the main paper adopts.** The main paper's primary policy claim (§8 and §11.8) is derived from the construct definition (F1 + F2) *without* reference to GBD data: the construct directly predicts the asymmetry between signal-redesign and information-based interventions, and this prediction is testable against the existing intervention-effect meta-analytic literature (main-text Figure 8). This is the non-circular form of the stakes claim.

---

## Supplementary Figure H1 — Dual-anchor DALY visualisation (retired from main-text Figure 8)

**(a) Dual-anchor headline chart.** *Primary (left bar): Steiger-correct floor 4.1 M DALYs/yr* [1.0, 11.8] — retains only chain 1b (risk tolerance → antidepressants) under standard MR Steiger directionality filtering; approximately equivalent to the 2021 global burden of Parkinson's disease (≈ 3 M). *Extended (right bar): full envelope 34.6 M DALYs/yr* [16.2, 64.1] — all four de-duplicated MR chains under the broader inclusion rule (Steiger ✗ flagged but not excluded per Hemani 2017 for socially-stratified exposures): BMI → T2D 23.6 M (68%), drinks → alcoholic liver cirrhosis 4.3 M (12%), risk tolerance → antidepressants 4.1 M (12%), smoking → alcoholic liver 2.5 M (7%). ≈ 10× Parkinson's and ≈ half the burden of low back pain (≈ 66 M). Both anchors use Levin's (1953) PAF formula. **(b) Sensitivity panel:** primary floor 4.1 M; large-effect-only (OR ≥ 1.5) 30.4 M; prevalence ± 20% 29.3–39.4 M. **(c) Sankey flow (extended envelope):** exposures (BMI, alcohol, risk tolerance, smoking) → diseases (T2D, cirrhosis, depression, ancillary) → DALY category (cardiometabolic, hepatopancreatic, psychiatric).

Full reproducibility: `03-analysis/scripts/mortality_daly_anchor.py`; sensitivity table: `mortality_anchor_sensitivity.json`.

---

## H.7 References cited in this appendix

- IHME GBD 2021 Collaborators (2024). *Lancet* 403 suite.
- NCD-RisC (2024). *Lancet* 403, 1027–1050.
- WHO (2024). Global status report on alcohol and health.
- Falk, A., Becker, A., Dohmen, T., Enke, B., Huffman, D., & Sunde, U. (2018). *QJE* 133, 1645–1692.
- Hemani, G., Tilling, K., & Davey Smith, G. (2017). *PLoS Genet* 13, e1007081.
- Davies, N. M., Hill, W. D., Anderson, E. L. et al. (2019). *eLife* 8, e43990.
- Levin, M. L. (1953). *Acta Unio Int Contra Cancrum* 9, 531–541.

---

*End of Appendix H. This appendix explores health burden as one downstream manifestation of Sweet Trap mechanisms; the paper's primary contribution is theoretical rather than epidemiological.*
