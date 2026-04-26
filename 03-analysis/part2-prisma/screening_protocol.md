# Screening Protocol — Part 2 Animal Cases PRISMA Scoping Review
# Sweet Trap v4, Stage 6

**Date:** 2026-04-24
**Version:** 1.0
**Coders:** PI (Lu An) + Co-coder (Hongyang Xi) for abstract screening;
            PI + 3 external coders (to be recruited) for F1-F4 full coding
**Inter-rater target:** κ ≥ 0.70 (abstract screen); Fleiss' κ ≥ 0.70 (F1-F4 coding)

---

## 1. PRISMA Flow Template

The following flow structure will be populated as screening progresses. Numbers marked with `[TBD]` are targets based on expected yields from search_strategy.md.

```
IDENTIFICATION
  Records identified via database searches:
    PubMed:                         [TBD, est. 250-400]
    Web of Science Core Collection: [TBD, est. 400-600]
    Scopus:                         [TBD, est. 300-500]
    Corpus-index (local):           [TBD, est. 40-60]
    Grey literature / snowball:     [TBD, est. 60-100]
  ─────────────────────────────────────────────────────
  Total records before deduplication: [TBD, est. 1,050-1,660]

SCREENING — DEDUPLICATION
  Records removed (duplicate DOI):          [TBD]
  Records removed (duplicate title+author): [TBD]
  ─────────────────────────────────────────────────────
  Records after deduplication:              [TBD, est. 600-900]

SCREENING — TITLE + ABSTRACT
  Records screened:                         [TBD, est. 600-900]
  Records excluded at title+abstract:       [TBD, est. 450-700]
    Reason: no animal subject (E6/E7)       [TBD]
    Reason: no approach/preference behavior [TBD]
    Reason: no fitness outcome mentioned    [TBD]
    Reason: coerced exposure (E2)           [TBD]
    Reason: human subjects only (E6)        [TBD]
    Reason: review/theoretical (no cases)  [TBD]
  ─────────────────────────────────────────────────────
  Records advanced to full-text:            [TBD, est. 150-250]

ELIGIBILITY — FULL-TEXT ASSESSMENT
  Full texts retrieved:                     [TBD, est. 150-250]
  Full texts excluded:                      [TBD, est. 100-180]
    E1: No fitness cost to preferring agent [TBD]
    E2: Coerced/forced exposure             [TBD]
    E3: No estimable Δ_ST                   [TBD]
    E4: No verifiable DOI                   [TBD]
    E5: Duplicate taxon×mechanism (anchor)  [TBD]
    E8: Parasitic host manipulation         [TBD]
    Other reason                            [TBD]
  ─────────────────────────────────────────────────────
  Studies included in synthesis:            [TBD, target 30-40 NEW cases]

INCLUDED
  Anchor cases (layer_A_animal_meta_v2):   20 (retained without re-screening)
  New cases from this review:             [TBD, target 30-40]
  ─────────────────────────────────────────────────────
  Total in Part 2 meta-analysis:          [TBD, target ≥50]
```

---

## 2. F1-F4 Coding Rubric

### 2.1 Overview

Each full-text-assessed case receives a binary score (0 or 1) on each of the four Sweet Trap signatures. **All four must score 1 for inclusion.** Cases scoring 1 on three or fewer signatures are excluded from the primary meta-analysis but may appear in a "near-miss" sensitivity table.

### 2.2 F1 — Reward-Fitness Decoupling

**Definition:** The stimulus that generates approach / preference / consumption behavior in the focal animal is associated with a negative or negligible fitness outcome in the current or manipulated environment, whereas an equivalent or ancestrally-related stimulus class was associated with a positive fitness outcome in an ancestral or comparison environment.

**Score 1 if ANY of the following:**
- (a) Direct experimental comparison: same stimulus, two environments (ancestral/baseline vs. current/novel); fitness outcome significantly differs in direction or magnitude (p < 0.10 for directional comparison; effect not required to be significant at conventional threshold given small N in many animal studies)
- (b) Phylogenetic comparison: closely related species or populations differing in exposure to the stimulus show different fitness-behavior correlations in the expected direction
- (c) Theoretical prior supported by mechanistic argument: stimulus belongs to a class where ancestral calibration is well-documented in the literature (e.g., celestial phototaxis, conspecific chemical signals, sweet taste) AND current environment demonstrably disrupts the signal-fitness link; ancestral r ≥ +0.25 Tier 3 acceptable

**Score 0 if:**
- Only negative fitness outcome documented, with no evidence or argument for ancestral positive correlation
- Correlation is directionally ambiguous in both environments
- Fitness outcome is purely theoretical with no empirical grounding

**Coding notes:**
- Document the Tier of ancestral baseline: Tier 1 (direct experimental control), Tier 2 (phylogenetic / lab-field comparison), Tier 3 (theoretical prior)
- Record ancestral_r (point estimate + 95% CI) and current_r (point estimate + 95% CI) in data extraction form
- If ancestral_r is Tier 3, record the justification sentence

---

### 2.3 F2 — Voluntary Endorsement

**Definition:** The focal animal approaches, chooses, or pursues the reward-generating stimulus without physical coercion; the behavior is generated by the animal's own motivational/sensory system.

**Score 1 if ANY of the following:**
- (a) Explicit choice assay: animal presented with reward stimulus vs. alternative and chooses the reward stimulus at above-chance rate
- (b) Approach behavior documented: animal moves toward stimulus in absence of physical entrapment
- (b*) Oviposition or settlement: female deposits eggs on or near stimulus (voluntary motor act)
- (c) Continued engagement despite partial cost signals: animal does not terminate behavior when subsidiary cost signals are available (e.g., continues consuming despite partial satiety)
- (d) Population-level revealed preference: species preferentially aggregates near stimulus in field conditions consistent with active choice

**Score 0 if:**
- Exposure is purely passive (chemical contamination of habitat with no behavioral chemotaxis component)
- Physical entrapment mechanism operates without prior voluntary approach
- Behavior is exclusively triggered by conspecific social manipulation with no individual voluntary component

**Coding notes:**
- Note whether endorsement is documented in current environment only or also in ancestral/comparison environment
- Record the behavioral evidence type: choice_assay / field_aggregation / oviposition / consumption / continued_approach

---

### 2.4 F3 — Persistence Architecture (informational, not exclusionary)

**Definition:** A mechanism that maintains the decoupled behavior despite fitness cost, operating at one of four levels:
- M1: Individual neural sensitization / habit / instinct (cannot update within lifetime)
- M2: Social information propagation (conspecific behavior reinforces the choice)
- M3: Genetic covariance / cultural inheritance (preference transmitted across generations)
- M4: Fitness cost operates post-endorsement (delay between approach and cost prevents immediate learning)

**Note:** F3 is recorded as a descriptive coding variable for moderator analysis (§5.2 of layer_A_animal_meta_v2.md). A case is NOT excluded if F3 evidence is weak — F3 codes the persistence mechanism, which is theoretically required but difficult to document directly. If F3 mechanism is not documented, code as M_inferred and record the theoretical justification.

**Score 1 (informational, not exclusionary):** Any plausible persistence mechanism identifiable
**Score 0 (flag for sensitivity analysis):** No persistence mechanism identifiable AND fitness cost is near-instantaneous AND learning would be expected

---

### 2.5 F4 — Feedback Failure (informational, not exclusionary)

**Definition:** The system lacks a corrective feedback loop that would allow the agent (within-lifetime) or population (across-generations) to revise preference in response to fitness cost.

**Score 1:** Any of:
- (a) Fitness cost is delayed relative to reward signal (temporal separation prevents associative learning)
- (b) Fitness cost operates below threshold for behavioral inhibition (sublethal or diffuse)
- (c) Genetic lock-in: preference gene and fitness cost are not in selective opposition within-generation (e.g., Fisherian genetic covariance)
- (d) Cost occurs at different life stage or in different individual from the preferring agent (e.g., offspring mortality from parent's oviposition choice)
- (e) Environmental change rate exceeds evolutionary response rate (HIREC context)

**Score 0 (flag, not exclusion):** Feedback failure is not documentable; rapid learning documented; cost is immediate and associable

---

## 3. Data-Extraction Form

### 3.1 Form columns (one row per included case)

| Column | Type | Notes |
|---|---|---|
| `case_id` | string | New cases: B1, B2, … (B-prefix to distinguish from anchor A1-A20) |
| `species_latin` | string | Binomial name, authority year if available |
| `common_name` | string | English common name |
| `phylum` | categorical | Chordata / Arthropoda / Mollusca / Cnidaria / Nematoda / Echinodermata / Annelida / Other |
| `class` | string | Mammalia / Aves / Reptilia / Amphibia / Actinopterygii / Insecta / Arachnida / Malacostraca / etc. |
| `order_family` | string | Order and family |
| `setting` | categorical | lab / field / lab+field / fossil |
| `reward_type` | string | Brief description of reward signal (e.g., "sweet taste", "celestial light cue", "conspecific song") |
| `fitness_metric` | string | Specific metric used (e.g., "adult survival probability", "number of offspring fledged", "colony queen production") |
| `F1_score` | binary (0/1) | F1 coding |
| `F1_tier` | categorical | Tier1 / Tier2 / Tier3 |
| `ancestral_r_point` | numeric | Point estimate; NA if Tier 3 prior only |
| `ancestral_r_lb95` | numeric | Lower 95% CI; NA if Tier 3 |
| `ancestral_r_ub95` | numeric | Upper 95% CI; NA if Tier 3 |
| `ancestral_r_justification` | string | Source or theoretical argument for ancestral baseline |
| `current_r_point` | numeric | Point estimate for current environment |
| `current_r_lb95` | numeric | Lower 95% CI |
| `current_r_ub95` | numeric | Upper 95% CI |
| `current_r_source` | string | Source paper/method for current-environment correlation |
| `delta_ST_point` | numeric | **LEAVE BLANK at abstract screen / candidate-cases stage; fill at full-text extraction** |
| `delta_ST_lb95` | numeric | **LEAVE BLANK at candidate stage** |
| `delta_ST_ub95` | numeric | **LEAVE BLANK at candidate stage** |
| `crosswalk_applied` | boolean | Whether a d-to-r or OR-to-r crosswalk was needed |
| `crosswalk_formula` | string | If crosswalk: formula used |
| `F2_score` | binary (0/1) | F2 coding |
| `F2_evidence_type` | categorical | choice_assay / field_aggregation / oviposition / consumption / continued_approach |
| `F3_mechanism` | categorical | M1 / M2 / M3 / M4 / M_inferred / combinations |
| `F4_score` | binary (0/1) | F4 coding (informational) |
| `F4_type` | categorical | temporal_delay / threshold_below / genetic_lock / cross_stage / HIREC_rate |
| `effect_size_raw` | string | **LEAVE BLANK at candidate stage; raw statistic from paper** |
| `effect_size_metric` | string | **LEAVE BLANK at candidate stage; e.g., HR, OR, RR, d, r** |
| `sample_n` | integer | Total N in primary study (animals / colonies / populations) |
| `quality_score` | integer (0-6) | Identification (0-2) + Sample (0-2) + Fitness measurement (0-2) |
| `quality_identification` | integer (0-2) | 0=correlational; 1=quasi-experimental; 2=RCT/manipulation |
| `quality_sample` | integer (0-2) | 0=<50; 1=50-500; 2=>500 or population-level |
| `quality_fitness` | integer (0-2) | 0=proxy; 1=direct survival/repro; 2=lifetime fitness |
| `anthropogenic_driver` | boolean | Whether decoupling is driven by human environmental modification |
| `mechanism_category` | categorical | sensory_exploit / olds_milner / fisher_runaway / zahavi_handicap / repro_survival_tradeoff / oviposition_mismatch / phenological_mismatch |
| `F1_route` | categorical | A (ancestral mismatch) / B (novel stimulus hijack) |
| `primary_doi` | string | DOI of primary reference |
| `primary_reference` | string | Author Year Journal (formatted) |
| `secondary_doi` | string | DOI of secondary reference (if any) |
| `secondary_reference` | string | Author Year Journal |
| `geographic_context` | string | Continent / ocean / lab (global if multi-site) |
| `time_horizon` | string | Duration of fitness measurement or observation period |
| `coder_id` | string | Who coded this case |
| `coding_date` | date | YYYY-MM-DD |
| `adjudication_notes` | string | Notes if discrepancy between coders |

### 3.2 Filling protocol

- **Candidate-cases stage (Week 1):** Fill `case_id` through `primary_reference` and `F1_score` through `F4_score`. Leave `delta_ST_point`, `delta_ST_lb95`, `delta_ST_ub95`, `effect_size_raw`, `effect_size_metric` blank.
- **Full-text extraction stage (Week 2):** Fill remaining quantitative columns. Compute Δ_ST from ancestral_r and current_r using the pre-registered formula: Δ_ST = ancestral_r_point − current_r_point (sign-corrected so that higher Δ_ST = more decoupling in reward-positive direction).

---

## 4. Quality Assessment Rubric

Quality scoring follows the v2 scheme from layer_A_animal_meta_v2.md, extended with a fourth dimension for phylum-supplement cases to address the greater heterogeneity expected in the expanded set.

### 4.1 Primary dimensions (0-2 per dimension; max = 6)

**Identification quality (0-2):**
- 0 = Correlational only (observational, no comparison group, no manipulation)
- 1 = Quasi-experimental (before/after comparison, natural experiment, population-level contrast)
- 2 = Randomized or controlled experiment (RCT, randomized field experiment, controlled lab manipulation with randomized assignment)

**Sample quality (0-2):**
- 0 = < 50 individuals / animals / units
- 1 = 50–500 individuals, or population-level estimate from moderate-sized study
- 2 = > 500 individuals, or fossil population-level evidence, or large-scale monitoring database

**Fitness measurement quality (0-2):**
- 0 = Proxy measure (condition index, weight, biomarker; no direct survival/reproduction outcome)
- 1 = Direct survival or reproduction measure (adult survival, number of offspring, fledgling success)
- 2 = Lifetime fitness or multi-generation tracking; large-scale mortality estimation (e.g., national-scale mortality monitoring)

### 4.2 Use of quality score

- Quality score is a **moderator variable** in meta-regression (following layer_A_animal_meta_v2.md §5.4), not an exclusion criterion.
- Sensitivity analysis: repeat meta-analysis restricting to quality ≥ 4; present alongside full-sample results.
- Cases with quality = 0-2 (Tier 3 baseline + correlational identification + proxy fitness) are flagged in the data table and excluded in the primary Tier-3-exclusion sensitivity analysis.

---

## 5. Κ Calculation Protocol

### 5.1 Abstract screening κ

- Both coders screen all records independently.
- Binary decision: include (advance to full-text) / exclude (with reason code).
- Cohen's κ computed on all records after both coders complete.
- Discrepancies: both coders review full title + abstract together; consensus decision.
- Target: κ ≥ 0.70 at abstract-screening stage.

### 5.2 Full F1-F4 coding κ

- After full-text retrieval, three external coders receive case descriptions (text only, blinded to authors' F1-F4 coding and to Δ_ST values).
- Fleiss' κ computed across three external coders on F1 (primary) and F2 (secondary).
- Author-vs-external agreement: Cohen's κ per external coder against PI coding.
- Target: Fleiss' κ ≥ 0.70 on F1; κ ≥ 0.60 on F2 (F2 is somewhat more judgement-dependent than F1).
- If Fleiss' κ < 0.60 on F1: report openly; shift primary analysis to continuous Δ_ST (per analytical_pipeline.md §4 Falsifier clause).

### 5.3 Adjudication rule

For any case where at least two of three external coders disagree with PI on F1 classification: the case enters a "contested" category. Contested cases are included in a sensitivity analysis labeled "PI-inclusion" and excluded in the "conservative external-coder" sensitivity analysis.

---

## 6. Moderator Variables (Pre-Specified)

All moderator analyses are pre-specified here to prevent post-hoc forking.

| Moderator | Operationalisation | Expected direction | Pre-specified test |
|---|---|---|---|
| Mechanism category | sensory_exploit / olds_milner / fisher_runaway / oviposition_mismatch / phenological_mismatch | olds_milner > sensory_exploit > fisher_runaway (replicating v2) | Meta-regression QM test; subgroup pooling |
| F1 route (A vs B) | Route A = ancestral mismatch; Route B = novel stimulus hijack | Route B > Route A | β_RouteB meta-regression coefficient |
| Phylum | Chordata / Arthropoda / Mollusca / Cnidaria / Nematoda / Echinodermata | No a-priori direction; test heterogeneity | QM across phyla; leave-one-phylum-out |
| Quality score (continuous) | 0-6 as above | Higher quality → higher Δ_ST (replicating v2 β=+0.112 per point) | Continuous meta-regression |
| Anthropogenic driver | Yes/No | Anthropogenic > natural (evolutionary novelty is greater) | β_Anthropogenic |
| Ancestral baseline tier | Tier1 / Tier2 / Tier3 | Tier1 > Tier2 > Tier3 (replicating v2 tier effect) | QM subgroup test |
| Vertebrate vs. invertebrate | Binary | No significant difference expected (replicating v2 p=.695 null) | QM or β |

---

*Version 1.0. Complement to search_strategy.md. Part of Sweet Trap v4 Stage 6 Week-1 deliverable set.*
