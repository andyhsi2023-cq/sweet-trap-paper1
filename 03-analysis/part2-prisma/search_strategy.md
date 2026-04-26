# Search Strategy — Part 2 PRISMA-ScR Scoping Review
# Sweet Trap Cross-Animal Evidence Expansion (v1 → 50+ cases)

**Date:** 2026-04-24
**Prepared by:** Literature Specialist Agent (Stage 6, Week 1)
**PI:** Lu An / Hongyang Xi
**Target:** ≥50 F1+F2-passing animal cases across ≥6 phyla for H2 meta-analysis
**Anchors:** 20 cases from layer_A_animal_meta_v2.md (retained, not re-screened)
**Protocol will be retrospectively registered on OSF before submission**

---

## 1. Framing and PECO Structure

This review uses the Population / Exposure / Comparator / Outcome (PECO) framework adapted for comparative-ethology scoping, following PRISMA for Scoping Reviews (PRISMA-ScR; Tricco et al. 2018 *Ann Intern Med*) and Joanna Briggs Institute scoping review methodology (Peters et al. 2020).

| PECO element | Operationalisation |
|---|---|
| **Population (P)** | Any non-human animal taxon (Metazoa), any life stage, any natural or laboratory setting |
| **Exposure (E)** | A stimulus, cue, or environmental feature that generates an approach / preference / consumption / mating response in the focal organism, AND for which there is evidence or theoretical grounds that the stimulus-fitness correlation differs between ancestral (calibration) and current (exposure) environments |
| **Comparator (C)** | Same species / closely related species in ancestral calibration condition OR pre-manipulation baseline |
| **Outcome (O)** | Measurable fitness-relevant consequence: survival, reproduction, condition (body mass, parasite load, injury), or lifetime-fitness proxy; AND evidence or coding of voluntary endorsement (approach without coercion) |

**Inclusion rule:** A record must satisfy all four Sweet Trap signatures to advance to full-text extraction. See Section 4 for F1-F4 rubric.

---

## 2. Database Coverage and Access

### 2.1 Primary databases (Week 1 execution)

| Database | Coverage | Access method | Query date |
|---|---|---|---|
| **PubMed/MEDLINE** | Biomedical + ecology, 1966-2026 | Free public API (E-utilities) | 2026-04-24 |
| **Web of Science Core Collection** | Science Citation Index Expanded + BIOSIS, 1900-2026 | Institutional subscription (ZJU CARSI SSO available as backup) | 2026-04-24 |
| **Scopus** | Elsevier multidisciplinary, 1823-2026 | Institutional subscription (ZJU CARSI SSO) | 2026-04-24 |
| **Local corpus-index** | 35,858 social-science-leaning journal papers, 2015-2026 (semantic search) | `query.py` at `/Users/andy/Desktop/Research/.corpus-index/` | 2026-04-24 |

### 2.2 Secondary / grey literature sources (supplementary harvest)

| Source | Rationale |
|---|---|
| **bioRxiv** (biorxiv.org) | Evolutionary biology / behavioural ecology preprints 2013-2026; may contain unpublished trap cases |
| **arXiv q-bio.PE** | Quantitative-biology population/evolutionary papers |
| **Dryad Digital Repository** | Open-data deposits linked to ecological-trap studies; secondary harvest from Hale & Swearer 2016 *Proc R Soc B* Table S1 (43 cases) |
| **Zenodo** | Supplementary data from ecological-trap reviews |
| **Reference list snowballing** | Forward / backward citations from 5 anchor reviews: Schlaepfer et al. 2002 *TREE*; Robertson & Hutto 2006 *Ecology*; Robertson et al. 2013 *TREE*; Robertson & Chalfoun 2016 *Curr Opin Behav Sci*; Hale & Swearer 2016 *Proc R Soc B* |
| **Google Scholar (targeted)** | Hand-searches for Cnidaria, Nematoda, Echinodermata terms not well-covered by WOS/Scopus |

### 2.3 CARSI access note

ZJU CARSI SSO provides journal-level full-text access for: Nature, Science, Cell Press, Wiley, Springer, Elsevier (ScienceDirect), EMBO Press, Rockefeller University Press, Oxford Academic, Cambridge Core. This covers ~90% of expected target journals (Behaviour, Anim Behav, Proc R Soc B, J Exp Biol, Ecol Lett, Current Biology, PNAS, Nature Ecol Evol, Science).

---

## 3. Query Strings

### 3.1 Master conceptual domains covered by Boolean queries

The query architecture covers five conceptual clusters:
- **Cluster A:** Ecological / evolutionary trap + preference + fitness
- **Cluster B:** Supernormal stimulus + sensory exploitation
- **Cluster C:** Reward-fitness decoupling, maladaptive preference, mismatch
- **Cluster D:** Fisher runaway / Zahavi handicap / sexual selection cost
- **Cluster E:** Phylum-specific supplement queries (for under-represented phyla)

### 3.2 Query strings (raw text, ready to paste into databases)

---

#### QUERY 1 — Ecological / Evolutionary Trap (Cluster A)

**PubMed / WOS / Scopus:**

```
("ecological trap" OR "evolutionary trap" OR "behavioral trap" OR "behavioural trap")
AND
("preference" OR "attraction" OR "approach" OR "choice" OR "habitat selection" OR "oviposition" OR "foraging")
AND
("fitness" OR "survival" OR "mortality" OR "reproductive success" OR "reproduction" OR "fecundity" OR "maladaptive" OR "population decline")
```

*Expected yield:* 300-600 records across three databases; highest-priority cluster for the ecological-trap literature.

---

#### QUERY 2 — Supernormal Stimulus / Sensory Exploitation (Cluster B)

**PubMed / WOS / Scopus:**

```
("supernormal stimulus" OR "superstimulus" OR "super-normal" OR "sensory trap" OR "sensory exploitation" OR "sensory bias" OR "pre-existing bias" OR "pre-existing preference")
AND
("animal" OR "insect" OR "bird" OR "fish" OR "amphibian" OR "reptile" OR "mammal" OR "invertebrate")
AND
("fitness" OR "survival" OR "mortality" OR "reproduction" OR "cost" OR "maladaptive" OR "preference")
```

*Expected yield:* 200-400 records. High relevance for Arthropoda and Chordata cases.

---

#### QUERY 3 — Reward-Fitness Decoupling / Mismatch / Maladaptive Preference (Cluster C)

**PubMed / WOS / Scopus:**

```
("reward" OR "reward system" OR "dopamine" OR "reinforcement") AND ("mismatch" OR "decoupling" OR "maladaptive" OR "mismatched") AND ("animal" OR "non-human" OR "rodent" OR "primate" OR "fish" OR "insect" OR "bird")

OR

("evolutionary mismatch" OR "mismatch hypothesis" OR "habitat mismatch" OR "phenological mismatch" OR "oviposition preference performance" OR "preference-performance") AND ("fitness" OR "survival" OR "maladaptive")

OR

("reward-fitness" OR "reward fitness decoupling" OR "fitness decoupling")
```

*Expected yield:* 150-300 records. Important for Olds-Milner class cases and oviposition-mismatch cases.

---

#### QUERY 4 — Fisher Runaway / Sexual Selection Cost (Cluster D)

**PubMed / WOS / Scopus:**

```
("runaway selection" OR "Fisher runaway" OR "Lande-Kirkpatrick" OR "genetic covariance" OR "sexy son" OR "handicap principle" OR "Zahavi handicap" OR "honest signal" OR "condition-dependent ornament")
AND
("viability cost" OR "survival cost" OR "mortality" OR "predation" OR "parasite" OR "immune" OR "cost of reproduction" OR "good genes" OR "condition dependence" OR "fitness cost")
AND
("female preference" OR "mate choice" OR "sexual selection" OR "ornament" OR "signal")
```

*Expected yield:* 400-600 records. Covers Fisherian runaway and handicap cases across Chordata and Arthropoda.

---

#### QUERY 5 — Light Pollution / Artificial Light at Night (ALAN) (Cluster B supplement)

**PubMed / WOS / Scopus:**

```
("artificial light at night" OR "light pollution" OR "ALAN" OR "night lighting" OR "urban light" OR "phototaxis")
AND
("animal" OR "insect" OR "moth" OR "bird" OR "turtle" OR "frog" OR "fish" OR "bat" OR "firefly")
AND
("mortality" OR "disorientation" OR "attraction" OR "collision" OR "migration" OR "fitness" OR "predation")
```

*Expected yield:* 150-250 records. High yield for Arthropoda (moths, beetles) and Chordata (birds, turtles, fish).

---

#### QUERY 6 — Neonicotinoids / Pesticide Preference (Cluster C supplement)

**PubMed / WOS / Scopus:**

```
("neonicotinoid" OR "imidacloprid" OR "clothianidin" OR "thiamethoxam" OR "acetamiprid")
AND
("preference" OR "choice" OR "attraction" OR "consumption" OR "foraging" OR "approach")
AND
("bee" OR "Apis" OR "Bombus" OR "pollinator" OR "insect" OR "Drosophila" OR "fly")
AND
("fitness" OR "colony" OR "mortality" OR "reproduction" OR "survival" OR "queen" OR "brood")
```

*Expected yield:* 100-200 records. Focused on Arthropoda neonicotinoid traps.

---

#### QUERY 7 — Plastic Ingestion / Pollution Attraction (Cluster B supplement)

**PubMed / WOS / Scopus:**

```
("microplastic" OR "plastic ingestion" OR "plastic pollution" OR "marine debris")
AND
("preference" OR "attraction" OR "consumption" OR "mistaken" OR "confusion" OR "choice")
AND
("seabird" OR "fish" OR "sea turtle" OR "marine mammal" OR "invertebrate" OR "crab" OR "shrimp" OR "oyster" OR "mussel" OR "mollusc" OR "cnidaria" OR "jellyfish")
AND
("fitness" OR "mortality" OR "survival" OR "reproduction" OR "starvation" OR "toxicity")
```

*Expected yield:* 100-200 records. Important for Mollusca, Cnidaria, Echinodermata phyla.

---

#### QUERY 8 — Phylum-Supplement: Mollusca (Cluster E)

**PubMed / WOS / Scopus:**

```
("Aplysia" OR "Octopus" OR "Sepia" OR "Loligo" OR "squid" OR "cuttlefish" OR "sea slug" OR "nudibranch" OR "Lymnaea" OR "Helix" OR "Mytilus" OR "Crassostrea" OR "oyster" OR "gastropod" OR "cephalopod" OR "bivalve")
AND
("preference" OR "feeding" OR "mate choice" OR "chemotaxis" OR "attraction" OR "approach" OR "phototaxis")
AND
("fitness" OR "survival" OR "mortality" OR "maladaptive" OR "mismatch" OR "pollution" OR "cost" OR "reproductive success")
```

*Expected yield:* 80-150 records. Low base rate for qualifying cases; screening will be stringent.

---

#### QUERY 9 — Phylum-Supplement: Cnidaria (Cluster E)

**PubMed / WOS / Scopus:**

```
("Nematostella" OR "Hydra" OR "Acropora" OR "Exaiptasia" OR "jellyfish" OR "coral" OR "anemone" OR "Aurelia" OR "Chrysaora" OR "cnidarian")
AND
("preference" OR "attraction" OR "chemotaxis" OR "phototaxis" OR "feeding" OR "settlement" OR "substrate choice")
AND
("fitness" OR "survival" OR "mortality" OR "bleaching" OR "pollution" OR "noise" OR "light" OR "plastic" OR "maladaptive" OR "mismatch")
```

*Expected yield:* 50-100 records. Cases likely to be noise-pollution settlement disruption, plastic ingestion, or phototaxis mismatch.

---

#### QUERY 10 — Phylum-Supplement: Nematoda (Cluster E)

**PubMed / WOS / Scopus:**

```
("Caenorhabditis elegans" OR "C. elegans" OR "nematode" OR "roundworm" OR "Steinernema" OR "Meloidogyne")
AND
("food preference" OR "chemotaxis" OR "olfactory preference" OR "attraction" OR "foraging" OR "avoidance learning" OR "reward" OR "dopamine" OR "octopamine")
AND
("fitness" OR "survival" OR "fecundity" OR "lifespan" OR "maladaptive" OR "obesity" OR "pathogen" OR "toxin")
```

*Expected yield:* 40-80 records. C. elegans dopamine/food-preference literature is well-developed; strong overlap with molecular evidence for H4.

---

#### QUERY 11 — Phylum-Supplement: Echinodermata (Cluster E)

**PubMed / WOS / Scopus:**

```
("sea urchin" OR "starfish" OR "sea star" OR "Strongylocentrotus" OR "Asterias" OR "Pisaster" OR "Ophiura" OR "echinoderm" OR "brittle star" OR "holothurian" OR "sea cucumber")
AND
("preference" OR "attraction" OR "chemotaxis" OR "feeding" OR "settlement" OR "pheromone" OR "spawning" OR "aggregation")
AND
("fitness" OR "survival" OR "mortality" OR "reproduction" OR "maladaptive" OR "pollution" OR "acidification" OR "plastic" OR "mismatch")
```

*Expected yield:* 40-80 records. Lowest expected yield; primarily chemical-cue settlement disruption and spawning-aggregation mismatch cases.

---

#### QUERY 12 — Corpus-Index Semantic Search (local)

Executed via `query.py` at `.corpus-index/`:

```bash
HF_ENDPOINT=https://hf-mirror.com .corpus-index/venv312/bin/python \
  .corpus-index/scripts/query.py \
  "reward fitness decoupling animal mismatch ecological trap voluntary approach" \
  --k 30

HF_ENDPOINT=https://hf-mirror.com .corpus-index/venv312/bin/python \
  .corpus-index/scripts/query.py \
  "supernormal stimulus sensory exploitation maladaptive preference invertebrate" \
  --k 20

HF_ENDPOINT=https://hf-mirror.com .corpus-index/venv312/bin/python \
  .corpus-index/scripts/query.py \
  "Fisher runaway sexual selection viability cost ornament preference" \
  --k 20
```

*Expected yield:* 30-50 unique records not captured by database queries; particularly useful for social-science-adjacent treatment of animal reward systems.

---

## 4. Inclusion / Exclusion Criteria

### 4.1 Inclusion criteria (ALL four must be met)

| Criterion | Operationalisation | Notes |
|---|---|---|
| **I1 — Non-human animal** | Any Metazoa taxon (Porifera excluded; Placozoa, Ctenophora admitted if F1-F4 met) | Humans coded in Part 1, not Part 2 |
| **I2 — F1: Reward-fitness decoupling** | Evidence (experimental, observational, or fossil) that the stimulus generating approach/preference behavior is negatively or uncorrelated with fitness in the current or manipulated environment, whereas the same stimulus class was positively correlated with fitness in an ancestral or control environment | Ancestral baseline can be Tier 1 (direct control), Tier 2 (phylogenetic comparison / lab-field contrast), or Tier 3 (theoretical prior ≥+0.25); Tier must be recorded in coding sheet |
| **I3 — F2: Voluntary endorsement** | Agent voluntarily approaches, chooses, or pursues the reward cue without physical coercion; preference/approach behavior documented by behavioral observation, choice assay, or revealed preference | Traps that operate purely by physical entrapment (adhesive traps, pit traps) excluded unless voluntary approach component documented |
| **I4 — Fitness measurement** | At least one quantifiable fitness-relevant outcome: survival probability, reproductive success (offspring number / offspring survival), condition index, parasite load, metabolic consequence, or demonstrated population-level consequence | "Fitness" = any of these proxies; lifetime fitness not required |

### 4.2 Exclusion criteria

| Code | Reason | Example |
|---|---|---|
| **E1** | Pure sensory-exploitation mating (male-female signal) without measurable fitness cost to the preferring sex | Majority of sexual-selection papers where female preference has no documented viability cost |
| **E2** | Forced / coerced exposure — no voluntary component | Pesticide exposure by dermal contact; parasite infection without behavioral component |
| **E3** | No estimable Δ_ST — ancestral baseline absent AND theoretical prior < +0.25 cannot be justified | Papers documenting approach behavior without any fitness outcome |
| **E4** | No verifiable primary DOI or PubMed ID | Grey literature only; conference abstracts without data |
| **E5** | Duplicate taxon × mechanism pair already coded in the 20-case anchor set | A new paper on Apis neonicotinoid preference that adds no independent case |
| **E6** | Human subjects | All human cases coded in Part 1 |
| **E7** | Plant / microbial systems | Traps involving insectivorous plants excluded (plants are not the agent) |
| **E8** | Parasitic manipulation of host behavior | e.g., Toxoplasma gondii manipulation of rodent fear — the agent of manipulation is the parasite, not the host voluntarily endorsing a reward |

### 4.3 Borderline cases requiring adjudication

- **Domesticated animals:** Included if evidence of decoupling in domesticated context vs. ancestral wild baseline exists.
- **Laboratory strains with modified genotype:** Included if the behavioral phenotype can be mapped onto the F1-F4 logic; excluded if the modification is the primary cause of decoupling (would belong to H6f genetic-manipulation table, not Part 2 meta).
- **Parasitism-adjacent cases:** Include if voluntary approach component is the primary behavioral mechanism (e.g., host voluntarily approaches parasite habitat attracted by olfactory cue; the reward is the cue, the cost is parasitism).

---

## 5. Search Execution Plan

### 5.1 Sequencing

| Step | Action | Timeline |
|---|---|---|
| **Week 1 Day 1** | Run Queries 1-7 in WOS, PubMed, Scopus; export results as RIS/CSV | 2026-04-24 |
| **Week 1 Day 2** | Run Queries 8-11 (phylum supplements); corpus-index Query 12; Hale & Swearer Table S1 harvest | 2026-04-25 |
| **Week 1 Day 3** | Deduplication (DOI-first, then title fuzzy match); merge to master hit list | 2026-04-26 |
| **Week 1 Day 4-5** | Title+abstract screening (two passes: PI + co-coder; resolve discrepancies) | 2026-04-27-28 |
| **Week 2 Day 1-3** | Full-text retrieval and full-text eligibility assessment | 2026-04-29 — 2026-05-01 |
| **Week 2 Day 4-5** | F1-F4 coding of included cases; inter-rater reliability (κ calculation) | 2026-05-02-03 |

### 5.2 Deduplication protocol

Primary key: DOI. Secondary key: first-author surname + year + journal initials. Fuzzy title matching (Jaro-Winkler ≥ 0.92) as tertiary check. Implemented in Python (`jellyfish` library or `thefuzz`).

### 5.3 Inter-rater reliability

Coders: PI (Lu An) + 1 co-coder (Hongyang Xi) for Phase 1 (title+abstract). Target: Cohen's κ ≥ 0.70 at abstract-screening stage; Fleiss' κ ≥ 0.70 for F1-F4 full coding (three external coders to be recruited per `analytical_pipeline.md` §4). Discrepancies resolved by consensus discussion before full-text extraction begins.

---

## 6. PRISMA-ScR Compliance Notes

This protocol follows:
- Tricco et al. (2018). PRISMA Extension for Scoping Reviews (PRISMA-ScR). *Ann Intern Med*, 169(7), 467-473.
- Peters et al. (2020). Updated guidance for the conduct of scoping reviews. *JBI Manual for Evidence Synthesis*. Chapter 11.

Deviations from standard systematic-review protocol (declared):
1. No quality appraisal leading to exclusion (consistent with scoping review methodology — all F1-F4-passing cases included regardless of quality score; quality is a covariate).
2. Retrospective pre-registration (OSF) rather than prospective (per PI rule: post-analysis, pre-submission).
3. Tier 3 (theoretical prior) cases included in primary analysis with sensitivity analysis excluding them (per `analytical_pipeline.md` §1.5 response to hostile-reviewer objection).

---

*Version 1.0. Part of Sweet Trap v4 Stage 6 Week-1 deliverable set.*
