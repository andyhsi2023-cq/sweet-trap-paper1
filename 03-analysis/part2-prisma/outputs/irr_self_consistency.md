# Self-consistency recoding of F1–F4 on a blinded 20-case subsample

**Seed**: 42 · **n**: 20 · **Source**: `03-analysis/part2-prisma/outputs/animal_cases_final.csv` (114 cases)

**Blinded view**: `outputs/irr_subsample_blind.csv` (species, stimulus, 
fitness metric, DOI, abstract-level notes only — pre-coded F1-F4 columns 
stripped).

**Re-coded view**: `outputs/irr_subsample_recoded.csv` (original columns 
plus F1_recode/F2_recode/F3_recode/F4_recode/F4_type_recode).

## CRITICAL CAVEAT (read before using these numbers)

**This is a *self-consistency* check, not a true inter-rater reliability 
(IRR).** A single coder (the PI) labeled the full corpus; we then re-applied 
the screening_protocol.md §2 rubric to a blinded text-only view of 20 
randomly chosen cases and compared. This figure is reported as an 
**upper bound** on what independent IRR might yield — because the re-coder 
is the same person applying the same rubric, systematic biases (e.g. a 
lenient F1 heuristic) are shared and will not be caught. A true two-coder 
IRR with an independent external coder has **not** been run; we defer 
that exercise to Paper 2.

**Second caveat — paradox-affected κ**. The corpus is heavily imbalanced: 
112/113 cases are F1=1 and 111/113 are F2=1 and F4=1. Inside the n=20 
subsample the marginal is fully collapsed (all 20 have F1=1, F2=1, F4=1). 
When every case has the same label, Cohen's κ is either undefined or 
paradox-collapsed to 0 *even when observed agreement is 100%* (the Kappa 
Paradox, Feinstein & Cicchetti 1990). We therefore report three 
complementary statistics: observed agreement (p_o), Cohen's κ, Gwet's AC1 
(paradox-resistant), and Brennan-Prediger (free-marginal) κ.

## Results

| Field | Observed agreement p_o | Cohen's κ | Gwet's AC1 | Brennan-Prediger |
|---|---:|---:|---:|---:|
| F1 | 0.950 | 0.000 | 0.947 | 0.900 |
| F2 | 0.950 | 0.000 | 0.947 | 0.900 |
| F3 (mechanism) | 0.650 | 0.267 | 0.541 | 0.475 |
| F4 | 1.000 | undefined | undefined | undefined |
| F4_type | 0.450 | -0.095 | 0.341 | 0.267 |

### Notes on each row
- **F1** — Cohen's κ: po=0.950, pe=0.950; Brennan-Prediger: po=0.950, pe_free=0.500, q=2.
- **F2** — Cohen's κ: po=0.950, pe=0.950; Brennan-Prediger: po=0.950, pe_free=0.500, q=2.
- **F3 (mechanism)** — Cohen's κ: po=0.650, pe=0.522; Brennan-Prediger: po=0.650, pe_free=0.333, q=3.
- **F4** — Cohen's κ: undefined (only one label present across both raters); Brennan-Prediger: undefined (only one label).
- **F4_type** — Cohen's κ: po=0.450, pe=0.497; Brennan-Prediger: po=0.450, pe_free=0.250, q=4.

## Honest interpretation

- **F1, F2, F4 (binary)**: Observed agreement is very high (≥0.95) but 
  Cohen's κ is undefined/uninformative because every sampled case has 
  F1=F2=F4=1 in the original coding (paradox-collapsed marginal). 
  Gwet's AC1 is the defensible statistic here.
- **F3 (5-level categorical)**: Cohen's κ is well-defined and this is 
  the most informative row because the rubric leaves genuine judgement 
  space between M1/M3/M4 (neural lock vs genetic lock vs cross-stage).
- **F4_type (5-level categorical)**: same as F3; the main source of 
  potential two-coder disagreement, since HIREC vs cross-stage vs 
  temporal_delay can reasonably be argued multiple ways for the same 
  case.

## Recommendation

Report in the manuscript:

> 'Self-consistency of the F1–F4 rubric was assessed on a pre-registered 
> seed=42 random subsample of n=20 cases (scripts/07_irr_self_consistency.py). 
> Observed agreement between the original and blinded re-applied coding 
> was p_o = 0.95/0.95/0.65/1.00/0.45 
> on F1/F2/F3/F4/F4_type respectively. Binary fields (F1, F2, F4) have 
> collapsed marginals in this subsample, so Cohen\'s κ is paradox-
> uninformative and we report Gwet\'s AC1 in its place. Categorical 
> fields (F3: κ = 0.27; F4_type: κ = -0.09) carry meaningful judgement and are 
> the most informative targets for two-coder IRR in Paper 2.'

A full two-coder IRR on an external coder remains a planned deliverable 
for Paper 2 and is acknowledged as a limitation of Paper 1 in the 
manuscript's Limitations section.

## Files

- `03-analysis/part2-prisma/outputs/irr_subsample_blind.csv` — blinded 
  20-case view (text fields only, no pre-coded F1-F4).
- `03-analysis/part2-prisma/outputs/irr_subsample_recoded.csv` — blinded 
  view + recoder's F1-F4 labels (for audit trail).
- `03-analysis/part2-prisma/scripts/07_irr_self_consistency.py` — this 
  script (reproducible, seed=42).
