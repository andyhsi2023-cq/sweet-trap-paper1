# H6f Cross-Species Genetic-Manipulation Literature — Search Strategy

**Part 4, Stream 4b-LiteratureSynthesis · Sweet Trap V4**

This document pre-registers the systematic literature-search strategy for H6f
before full-text screening begins. All queries are timestamped and stored as
shell-executable commands in `scripts/04_h6f_pubmed_harvest.py` so that the
search can be rerun for trans-reviewer reproducibility.

---

## 1. Research question (pre-registered)

> Do published experimental manipulations of reward-receptor genes (knockout,
> knockdown, CRISPR, pharmacological block/activation) in non-human metazoan
> organisms produce behavioural changes consistent with Sweet Trap axioms
> (A1-A4)?

**H6f directional prediction:** ≥ 70 % of coded experiments show directional
consistency — receptor loss-of-function reduces pursuit of hyper-rewarding /
low-fitness stimuli; receptor gain-of-function increases such pursuit.

**Target inclusion N:** 30–50 papers spanning ≥ 3 phyla (vertebrate,
arthropod, plus at least one molluscan or nematode or cnidarian study).

---

## 2. Databases queried

1. **PubMed** via NCBI Entrez (`Bio.Entrez.esearch`, E-utilities). Primary
   database. Queries 2a–2g below.
2. **Web of Science** (TS field, 1995–2026) — queried via institutional CARSI
   portal; WOS record IDs captured manually for cross-validation against
   PubMed hit set.
3. **Scopus** — queried via institutional access; used as deduplication
   cross-check.
4. **bioRxiv + preprint review** — `biorxiv_query` API for 2020–2026 preprints
   not yet indexed on PubMed.

The PubMed queries below define the machine-reproducible core. WOS + Scopus
are used to verify that we have not missed key papers; any WOS/Scopus-only hit
is added manually with a `source=WOS` flag.

---

## 3. PubMed query library

All queries use date range `2000/01/01:2026/04/30`. Filters: `"English"[LA]
AND (Journal Article[pt] OR Review[pt])` (reviews retained for their reference
lists; reviews themselves are NOT coded as experiments).

### 3.1 Phylum-faceted core queries

#### Q-vertebrate-rodent
```
("knockout" OR "knock-out" OR "knockdown" OR "knock-down" OR "CRISPR"
  OR "pharmacological blockade" OR "receptor antagonist"
  OR "conditional deletion" OR "siRNA" OR "antisense")
AND
("taste receptor" OR "sweet receptor" OR "Tas1r" OR "T1R"
  OR "dopamine receptor" OR "Drd1" OR "Drd2" OR "Drd3"
  OR "mu opioid" OR "Oprm1" OR "Oprk1" OR "Oprd1"
  OR "orexin receptor" OR "Hcrtr"
  OR "NPY receptor" OR "Npy1r" OR "Npy2r" OR "Npy5r")
AND
(mouse OR mice OR rat OR rodent OR "Mus musculus" OR "Rattus")
AND
(behavior OR behaviour OR preference OR "food intake" OR "reward seeking"
  OR "self-administration" OR "sucrose" OR "palatable" OR addiction
  OR anhedonia OR feeding)
```

#### Q-vertebrate-primate-other
```
(same manipulation and receptor terms as Q-vertebrate-rodent)
AND
(primate OR macaque OR "Macaca" OR marmoset
  OR zebrafish OR "Danio rerio"
  OR hummingbird OR songbird OR "Gallus")
AND
(preference OR behavior OR behaviour OR feeding OR reward)
```

#### Q-arthropod-drosophila
```
("UAS-RNAi" OR "Gal4" OR "CRISPR" OR "P-element" OR "knock-in" OR "knockdown"
  OR "pharmacological")
AND
("DopR" OR "Dop1R" OR "Dop2R" OR "DopEcR"
  OR "Gr5a" OR "Gr64" OR "Gr43a" OR "gustatory receptor"
  OR "opioid-like" OR "dNPF" OR "NPF receptor"
  OR "dOrx" OR "orexin-like")
AND
("Drosophila" OR "fruit fly" OR "melanogaster")
AND
(preference OR feeding OR sugar OR ethanol OR cocaine OR reward OR valence)
```

#### Q-arthropod-bee
```
("RNAi" OR "siRNA" OR "pharmacological" OR "knockdown" OR "CRISPR")
AND
("Amel" OR "Apis mellifera" OR "honey bee" OR "honeybee" OR bumblebee
  OR "Bombus")
AND
("gustatory" OR "sucrose response" OR PER OR "proboscis extension"
  OR dopamine OR octopamine OR "reward learning" OR "foraging")
```

#### Q-nematode
```
("knockout" OR "mutant" OR "loss-of-function" OR "RNAi" OR "CRISPR")
AND
("C. elegans" OR "Caenorhabditis" OR nematode)
AND
("npr-1" OR "DOP-1" OR "DOP-2" OR "DOP-3" OR "cat-2" OR "NPF"
  OR "octopamine receptor" OR "tyramine")
AND
(feeding OR aggregation OR chemotaxis OR preference OR reward)
```

#### Q-mollusc
```
(Aplysia OR Lymnaea OR Biomphalaria OR octopus OR cuttlefish OR squid)
AND
(dopamine OR "reward" OR learning OR feeding OR memory)
AND
(manipulation OR "knockdown" OR RNAi OR injection OR pharmacological
  OR lesion OR "receptor block")
```

#### Q-cnidarian
```
(Hydra OR Nematostella OR "sea anemone" OR cnidarian OR jellyfish)
AND
(dopamine OR neuropeptide OR "chemical cue" OR feeding OR preference)
AND
("knockdown" OR "morpholino" OR RNAi OR CRISPR OR pharmacological)
```

### 3.2 Cross-phylum keyword queries (supplementary)

#### Q-supernormal-manipulation
```
("supernormal stimul*" OR "sensory trap" OR "signal exploitation"
  OR "evolutionary trap")
AND
("receptor" OR "gene" OR "manipulation")
AND
(behavior OR preference)
```

#### Q-reward-fitness-decoupling
```
("reward-fitness" OR "reward-fitness decoupling" OR "maladaptive reward"
  OR "hedonic overconsumption")
AND
("receptor" OR "knockout" OR "manipulation" OR "pharmacological")
```

---

## 4. Inclusion / exclusion criteria

### 4.1 Inclusion
- **I1:** Paper reports an experimental manipulation (loss-of-function,
  gain-of-function, pharmacological, or conditional) of a reward-receptor
  homolog. Pure observational studies excluded.
- **I2:** Manipulation is in a non-human metazoan organism.
- **I3:** At least one behavioural or fitness-relevant outcome measured in a
  way that admits F1 or F2 coding (preference, consumption, survival,
  fecundity, reproduction, learning).
- **I4:** Published 2000–2026 inclusive.
- **I5:** Peer-reviewed journal article (preprints included IF deposited on
  bioRxiv/medRxiv AND cited by ≥ 1 downstream peer-reviewed paper).

### 4.2 Exclusion
- **E1:** Review articles (used for reference-list harvest only; not coded as
  experiments).
- **E2:** In silico / computational-only studies.
- **E3:** Pure structural / biochemical studies without behavioural readout.
- **E4:** Studies in humans (H6f is explicitly non-human).
- **E5:** Studies manipulating non-reward receptors (serotonin without
  reward link, glutamate non-NMDA, etc. unless clearly reward-circuit-relevant).

### 4.3 Borderline cases — decision log
- **Studies manipulating BOTH genotype AND environment (GxE):** include; code
  the main-effect arm of the design.
- **Studies using pharmacological agonists/antagonists without genetic
  manipulation:** include, flagged with `manipulation_type = pharm`.
- **Studies in honeybee queen-worker caste comparison without gene manipulation:**
  exclude.
- **Partial loss-of-function alleles (hypomorph rather than null):** include,
  flagged as `manipulation_type = KD`.

---

## 5. Coding protocol

Each included paper is coded in `outputs/H6f_extraction_template.csv` along
twelve columns (described in that file's header). Specific codes:

- **direction_of_effect** = increase / decrease / none / mixed.
- **consistent_with_sweet_trap_axioms** = yes / no / partial
  - `yes` if receptor LoF → reduced pursuit of hyper-rewarding low-fitness
    stimulus (F1+F2 consistent), OR receptor GoF → increased such pursuit.
  - `partial` if the direction is consistent for one readout but not another
    within the same paper.
  - `no` if the direction opposes the prediction for the paper's primary
    readout.

A random 20 % sub-sample is double-coded by a second reader at Week 2. Cohen's
kappa ≥ 0.70 is the pre-registered minimum; below that we re-train and
re-code.

---

## 6. PRISMA 2020 reporting

We follow PRISMA 2020 for scoping / systematic reviews (Page et al. 2021
*BMJ* 372:n71). Flowchart template:

```
Records identified
  ├── PubMed (Q-vertebrate-rodent)       : n_1
  ├── PubMed (Q-vertebrate-primate-other): n_2
  ├── PubMed (Q-arthropod-drosophila)    : n_3
  ├── PubMed (Q-arthropod-bee)           : n_4
  ├── PubMed (Q-nematode)                : n_5
  ├── PubMed (Q-mollusc)                 : n_6
  ├── PubMed (Q-cnidarian)               : n_7
  ├── WOS cross-check                    : n_wos (unique adds only)
  └── Scopus cross-check                 : n_scopus (unique adds only)
        |
        v
  Deduplicated pool                      : n_dedup
        |
        v (title+abstract screening)
  Candidates                             : n_candidate
        |
        v (full-text screening)
  Included                               : n_included
        |
        +-- Coded                        : n_coded
        +-- Excluded at full-text        : n_fulltext_excl (reasons logged)
```

---

## 7. Reproducibility

- Every query is logged with timestamp, hit count, and retained IDs in
  `outputs/H6f_pilot_hit_list.csv`.
- The harvest script is version-controlled in
  `scripts/04_h6f_pubmed_harvest.py`.
- PubMed IDs (not titles) are the primary identifier; DOI harvested secondarily
  via `Bio.Entrez.efetch`.
- If a PubMed record is retracted after coding, we retain it in the coded set
  with a `retracted = yes` flag rather than delete, per PRISMA transparency.

---

## 8. Search-execution timeline

| Day | Activity |
|-----|----------|
| Day 1 (2026-04-24) | Initial PubMed harvest per query (this file) - automated |
| Day 2 | Deduplication; WOS + Scopus cross-check |
| Day 3-4 | Title + abstract screening (blinded by author pair) |
| Day 5-8 | Full-text screening + coding |
| Day 9 | Double-coding 20% sub-sample; κ calculation |
| Day 10 | Summary statistics + PRISMA flow diagram |

---

## 9. Expected hit counts (prior-based estimates)

Based on prior sense of the literature (Drosophila reward manipulation alone
has ≥ 80 papers; rodent reward knockouts ≥ 200; bee gustatory ≥ 40; C.
elegans npr-1 literature ≥ 50):

| Query | Expected raw hits | Expected after screening |
|-------|---|---|
| Q-vertebrate-rodent | 400-800 | 15-25 |
| Q-vertebrate-primate-other | 100-200 | 3-6 |
| Q-arthropod-drosophila | 200-400 | 10-15 |
| Q-arthropod-bee | 80-150 | 5-8 |
| Q-nematode | 150-300 | 4-7 |
| Q-mollusc | 30-80 | 1-3 |
| Q-cnidarian | 10-30 | 0-1 |

Target total retained: 30-50 papers. This is comfortably within the PubMed
retrieval envelope.

---

*Document version 1.0. Pre-registered timestamp: 2026-04-24.*
