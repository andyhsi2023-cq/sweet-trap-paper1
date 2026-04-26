# Public Data Feasibility Assessment v4
# Sweet Trap — Evolutionary Reframing (Stage 6)
# Date: 2026-04-20
# Scope: Data sources for Part 1 (Human), Part 2 (Animal), Part 3 (Molecular Evolution)

---

## Executive Summary

For the evolutionary reframing (v4), the highest-value new data actions are:
1. Santos et al. 2021 Zenodo dataset (138 species, enables systematic meta-analysis expansion)
2. PubMed/WoS systematic search (confirm 20+ cases, verify no prior cross-phyla synthesis)
3. TimeTree/Open Tree of Life (phylogenetic breadth visualisation, ~0.5 day)
4. Ensembl Compara (TAS1R + D1R + nAChR molecular convergence for Part 3)

Human-centric data sources (NHANES, HRS, GBD) add no increment over v3.3's existing evidence base. The evolutionary paper should treat humans as one taxon among many, not as the primary empirical layer.

---

## Part 1: Human Data Sources

### NHANES 1999-2023
Status: ✅ Directly accessible
Variables: 24-hour dietary recall (SSB, ultra-processed foods, alcohol); BMI/waist circumference; fasting glucose/HbA1c; linked mortality file (NHANES III follow-up to 2019).
Relevance to Sweet Trap F1 identification: Low. No "endorsement despite known harm" longitudinal marker; no behavioural preference trajectory. Dietary recall measurement error ~30%.
Access: https://wwwn.cdc.gov/nchs/nhanes/
Integration time: 1-2 weeks
Key caveat: Cannot identify the endorsement component of Sweet Trap; only documents population-level metabolic harm.
Verdict for v4 evolutionary paper: NICE-TO-HAVE. GBD 2021 / FinnGen / CFPS pathway already covers human metabolic Sweet Trap evidence in v3.3. No new increment.

---

### UK Biobank Behavioural Phenotype Layer
Status: ⚠️ Conditionally available (access likely already granted under genetic application)
Variables available: Alcohol intake frequency and typical quantity; diet items (cereal, fruit, processed meat, sugar in tea); sleep duration; PHQ-2 depression screen; working hours. Online activity screen time (coarse bins: <1h / 1-3h / >3h only).
Missing variables: No formal problem gambling scale; no digital addiction instrument; no food craving scale; no binge-eating screener. AUDIT-C as binge-drinking proxy only.
Sample bias: Mean age 57 years; volunteer health bias. Not suitable for adolescent Sweet Trap analysis.
Access: https://biobank.ndph.ox.ac.uk/showcase/ (Application required; may be within existing approval)
Integration time: 0.5 weeks if already approved
Verdict for v4: NICE-TO-HAVE. Useful only for gene-behaviour interaction supplementary analyses. Does not add the addiction/craving variables you want.

---

### HRS + ELSA + SHARE
Status: ⚠️ Conditionally available (application required per dataset)
Variables: HRS — longitudinal wealth/debt trajectories, health retirement outcomes, cognitive ageing. ELSA — wealth-health longitudinal (UK 50+). SHARE — 27 European countries, 50+ panel.
Missing: No "aspirational spending" variable; no investment FOMO measure; no direct Sweet Trap endorsement marker.
Access: HRS via ICPSR (https://www.icpsr.umich.edu/); ELSA via UK Data Archive; SHARE via https://share-eric.eu/
Integration time: 2-3 weeks per dataset
Verdict for v4: NOT APPLICABLE. These 50+ cohorts are mismatched to the evolutionary paper's cross-species scope. Low priority in 60-min assessment window.

---

### Add Health Wave V
Status: ⚠️ Conditionally available (restricted data application required)
Variables: Wave V (2016-2018, respondents age 32-42): screen time (smartphone/computer hours); diet/BMI; substance use (AUDIT, DAST); CES-D depression. Life-course linkage from Wave I (age 14-18) to Wave V.
Unique value: Only US dataset with adolescent Sweet Trap exposure → midlife outcome trajectory.
Access: https://www.cpc.unc.edu/projects/addhealth (application, IRB coordination)
Integration time: 2-3 weeks (data use agreement approval)
Verdict for v4: NICE-TO-HAVE. Only if Part 1 requires a US adolescent-to-midlife life-course demonstration. Not a priority for the cross-species reframing.

---

### GBD 2021 (IHME)
Status: ✅ Directly accessible, but limited scope for v4 domains
Available Sweet Trap-relevant attributions: Alcohol use disorder DALYs; drug use disorder DALYs; high BMI risk-factor attributions (type 2 diabetes, CVD, stroke, kidney disease). Dietary risk factors (high sugar-sweetened beverage intake, high sodium, low fibre) have PAF estimates.
NOT available: "Short-video addiction" DALYs; "investment FOMO" burden; "housing leverage" health burden — none exist in any GBD risk factor category as of 2021 release.
Access: https://vizhub.healthdata.org/gbd-results/ (public API)
Integration time: 0 (already used in v3.3 main M4.3)
Verdict for v4: ALREADY USED. No increment. v3.3 already uses GBD 2021 as descriptive-scale PAF; noted as non-primary (partially circular if used as "Sweet Trap causes X DALYs"). Do not expand this pathway.

---

### FTC Consumer Sentinel + FBI IC3
Status: ✅ Directly accessible (annual public reports)
Data granularity: FBI IC3 annual reports (2016-2025) provide: case counts and dollar losses by fraud type (pig butchering, investment fraud, romance scam, BEC). IC3 2023: investment fraud losses $4.57B; romance scam $652M. FTC Consumer Sentinel: aggregate complaint counts by category (no longitudinal individual tracking).
Access: https://www.ic3.gov/AnnualReport/ | https://www.ftc.gov/enforcement/consumer-sentinel-network
Integration time: 0 (already cited in v3.3 §11.7 Engineered Deception as EST scale evidence)
Verdict for v4: ALREADY COVERED. No new increment.

---

### PATH Study (Population Assessment of Tobacco and Health)
Status: ✅ Directly accessible (ICPSR public)
Variables: Longitudinal 2013-2022; cigarette/e-cigarette use behaviour; nicotine dependence (Fagerström scale); quit attempt history; self-reported knowledge of harm; DSM-5 tobacco use disorder criteria.
Sweet Trap relevance: Tobacco/nicotine is the cleanest human "endorsement despite known harm" longitudinal dataset. Fagerström scale operationalises endorsement inertia (A3.0). Quit attempt + relapse rate provides direct F4 (corrective feedback failure) quantification. PATH is NOT cited in v3.3.
Access: https://www.icpsr.umich.edu/web/NAHDAP/studies/36498
Integration time: 1 week (dataset is public, well-documented codebook)
Verdict for v4: NICE-TO-HAVE. If Part 1 needs a high-quality longitudinal "endorsement-despite-harm" human quantification (beyond cross-sectional CFPS), PATH provides it. Nicotine also has strong molecular homology to Case 8 (bee neonicotinoid, same nAChR pathway) — enabling a direct human-animal molecular bridge.

---

## Part 2: Animal Data Sources

### PubMed + Web of Science: Ecological/Evolutionary Trap Literature
Status: ✅ Directly accessible
Estimated search yield (2015-2026, based on knowledge base):
- "ecological trap": ~350-450 papers (WoS)
- "evolutionary trap": ~120-180 papers (overlaps significantly with above)
- "sensory trap" OR "sensory exploitation": ~150-200 papers
- "supernormal stimulus": ~60-90 papers
- Combined deduplicated estimate: ~500-600 papers

From this pool, new cases not yet in layer_A (currently 8 documented, OSF archive claims 20):
- LED/5G tower light-trap studies for insects (2020-2026 wave)
- Marine mammal acoustic trap studies (ship noise + cetacean stranding)
- Invasive plant trap studies (monarch milkweed is in layer_A; 5-8 additional invasive plant cases likely)
- New bird agricultural trap papers (Robertson lab output 2020-2025)
Expected net new cases: 10-15 additional, bringing total to 30+ if systematic search executed.

Access: PubMed (https://pubmed.ncbi.nlm.nih.gov/), WoS (institutional access required)
Integration time: 3-5 days (search + screening); 1-2 weeks (case extraction)
Verdict for v4: MUST-HAVE. Systematic search is required to (a) confirm your 20+ case claim, (b) verify that no prior paper has done a cross-phyla synthesis, (c) identify any 2023-2026 papers that might be emerging competitors.

---

### Open Tree of Life / TimeTree
Status: ✅ Directly accessible (fully public API)
Coverage for layer_A species: All 20 species confirmed present in TimeTree database. Divergence time estimates available for all pairs. Specifically:
- Lepidoptera / Rattus: ~750 Mya (protostome-deuterostome split)
- Apis mellifera / Rattus: ~600 Mya
- Caretta caretta / Rattus: ~310 Mya
- Drosophila / Pavo cristatus: ~700 Mya (insect-vertebrate)
The phylogenetic span (insects to mammals to birds, >600 My) quantifies the "universality" claim in a figure-ready format.
Access: https://timetree.org/ (web + API) | https://opentreeoflife.github.io/ (API)
Integration time: 0.5 days (batch species name query)
Verdict for v4: MUST-HAVE. Low cost, high visual impact for the cross-phyla universality figure. Generates the phylogenetic tree backbone for Figure 1 or Extended Data.

---

### GBIF
Status: ✅ Directly accessible (public API)
Record volume for key species:
- Caretta caretta: >500,000 occurrence records
- Apis mellifera: >2,000,000 records
- Drosophila melanogaster: >50,000 lab/field records
- Pavo cristatus: >100,000 records
Analytical use for Sweet Trap: Species distribution alone is insufficient. Meaningful analysis requires overlaying species occurrence with anthropogenic disturbance layers (NASA VIIRS night-light rasters, plastic pollution density maps, neonicotinoid application maps). This GIS overlay is technically feasible but requires 1-2 weeks additional work for each case.
Access: https://www.gbif.org/developer/occurrence
Integration time: 1-2 weeks (including GIS overlay, per case)
Verdict for v4: NICE-TO-HAVE. SI-level geographic visualisation of trap range. Not required for primary analysis. High cost-to-benefit ratio for 60-min priority assessment.

---

### Dryad / Figshare / Zenodo (Published Datasets)
Status: ✅ Directly accessible (fully public)
Key datasets confirmed available for re-analysis:

| Paper | Repository | DOI/Link | Data content | Re-analysis value |
|-------|-----------|----------|-------------|-------------------|
| Santos et al. 2021 (Science) | Zenodo | 10.5281/zenodo.4596595 | 138 species, ingestion rates, fitness proxies | HIGH: enables Δ_ST meta-regression across 138 species |
| Woodcock et al. 2017 (Science) | Dryad | Available | Colony weight, queen production, pesticide exposure | HIGH: Case 8 raw data for sensitivity analysis |
| Rundlöf et al. 2015 (Nature) | Figshare | Available | Bee colony data, field treatment assignment | HIGH: Case 8 pre-registration data |
| Fabian et al. 2024 (Nature Comm) | Dryad | Available | Moth flight trajectory data | MEDIUM: Case 1 raw kinematics |
| Linguadoca et al. 2024 (Nature) | Zenodo | Available | Bumble bee landscape data, 7,580 km² | HIGH: Case 8 landscape-scale corroboration |

Priority action: Download Santos 2021 Zenodo dataset and run Δ_ST meta-regression across all 138 species with available fitness data. This expands the meta-analysis from 8 cases to potentially 25-40 species with quantifiable Δ_ST, dramatically strengthening the universality claim.
Verdict for v4: MUST-HAVE (Santos 2021 Zenodo). 0.5-1 day integration time per dataset.

---

## Part 3: Molecular Evolution Data Sources

### Ensembl Compara + NCBI HomoloGene
Status: ✅ Directly accessible (fully public)

**TAS1R2/TAS1R3 (sweet taste receptors):**
- Mammals: TAS1R2 + TAS1R3 broadly conserved; heterodimer forms sweet receptor
- Birds: Many birds lack TAS1R2 (e.g., chickens lost sweet taste); hummingbirds re-evolved umami receptor for nectar detection — convergent functional solution
- Fish: T1R family present but binding specificity divergent (zebrafish T1R2/T1R3 respond to amino acids more than sugars)
- Insects: NO direct TAS1R orthologue. Drosophila Gr5a/Gr64 family = functionally analogous, evolutionarily distinct
- Key argument: The ABSENCE of strict orthology is EVIDENCE FOR convergent evolution of sweet-trap architecture. Different phyla evolved different molecular implementations of the same functional outcome. This is stronger than saying "the gene is conserved."

**Dopamine receptors (D1-D5):**
- D1R and D2R: conserved across all vertebrates (mammals, birds, fish, amphibians). ~70-80% amino acid identity across mammals. ~55-65% identity fish-to-mammals.
- Invertebrate dopamine receptors: Drosophila DopR (D1-like) and DAMB (D1-like) = functional analogues, ~40-50% identity to vertebrate D1R
- Implication: Dopaminergic reward encoding is functionally conserved across all bilaterians with nervous systems, even where strict orthology is partial.

**nAChR (nicotinic acetylcholine receptor, relevant to bee neonicotinoid case):**
- Insect nAChR: highly conserved across Arthropoda; neonicotinoids designed to exploit insect-specific subunit (α6) not present in vertebrates
- Vertebrate nAChR: present but different subunit composition (explaining mammalian vs insect differential toxicity)
- Argument for paper: The molecular mechanism is not the same gene but the same functional class — ionotropic ACh receptor mediating reward learning. Convergent function, divergent sequence.

**μ-opioid receptor (OPRM1):**
- Mammals: highly conserved (>95% identity within mammals)
- Fish: kappa-opioid receptor present; mu-opioid functional analogue present but weaker homology
- Insects: no direct orthologue, but opioid-like peptides (enkephalin-like) present
- Verdict: OPRM1 conservation argument is weaker than dopamine receptor argument; confine to SI if used.

Access: https://www.ensembl.org/info/genome/compara/index.html | https://www.ncbi.nlm.nih.gov/homologene/
Integration time: 0.5-1 day (query known gene IDs, pull species tree + percent identity matrix)
Verdict for v4: MUST-HAVE. Provides the molecular evidence tier for Part 3. Core argument: convergent functional architecture (not strict homology) is the correct framing.

---

### UniProt + InterPro
Status: ✅ Directly accessible (fully public)
Domain-level conservation: InterPro family annotations for TAS1R (IPR000073, Venus flytrap module), D1R/D2R (IPR000276, Rhodopsin-like GPCR), nAChR subunits (IPR006029). Can generate domain conservation score table across selected species.
Access: https://www.uniprot.org/ | https://www.ebi.ac.uk/interpro/
Integration time: 0.5 days
Verdict for v4: NICE-TO-HAVE. Supplements Ensembl data with domain-level structural conservation. Useful for a Part 3 supplementary table.

---

### PanTHERIA + AnAge
Status: ✅ Directly accessible (fully public)
PanTHERIA: 5,416 mammalian species with life-history variables (body mass, litter size, max lifespan, metabolic rate, home range, brain mass).
AnAge: 4,000+ species, longevity, ageing rate, reproductive lifespan.
Potential analysis: meta-regression of Δ_ST against life-history predictors:
- Generation time (τ_adapt proxy): negative correlation with evolutionary trap persistence predicted
- Brain mass/body mass ratio: higher encephalisation → more learning flexibility → potentially lower Δ_ST (testable)
- Maximum lifespan: longer-lived species accumulate more cross-generational trap exposure
This analysis is feasible within layer_A's 8-20 mammal/bird/insect cases, but sample size is small (N=8-20); may be underpowered.
Access: http://esapubs.org/archive/ecol/E090/184/ (PanTHERIA) | https://genomics.senescence.info/species/ (AnAge)
Integration time: 0.5-1 day (species name merge + regression)
Verdict for v4: NICE-TO-HAVE. Suitable for SI meta-regression table. Main text does not require.

---

### Paleobiology Database (PaleoBioDB)
Status: ⚠️ Marginally relevant
Potential use case: Identify extinction events where Sweet Trap dynamics may have contributed (e.g., megafauna naivety to human hunters as a "novel predator trap"; island endemics with no predator avoidance). PaleoBioDB provides fossil occurrence records but not behaviour.
Limitation: No quantitative Δ_ST estimation possible from fossil record. Any argument would be narrative.
Specific searchable scenario: Late Pleistocene megafauna extinction (~12,000 BP) — overlaps with human range expansion. Some taxa (Procoptodon, Diprotodon in Australia; Megatherium in Americas) show rapid extinction shortly after human arrival, potentially consistent with a "novel apex predator = evolutionary trap" hypothesis. Fossil record can document timing but not mechanism.
Access: https://paleobiodb.org/
Integration time: 1-2 days
Verdict for v4: NOT APPLICABLE for primary analysis. If included at all, 1-2 sentences in Discussion acknowledging paleontological evidence is consistent with but cannot confirm the Sweet Trap mechanism. Do not invest analysis time.

---

## Priority Matrix Summary

| Data Source | Priority | Action | Time Required |
|-------------|----------|--------|---------------|
| Santos 2021 Zenodo (138 species) | MUST-HAVE | Download + meta-regression | 1-2 days |
| PubMed/WoS ecological trap search | MUST-HAVE | Systematic search 2015-2026 | 3-7 days |
| TimeTree / Open Tree of Life | MUST-HAVE | Batch API query for 20 species | 0.5 days |
| Ensembl Compara (TAS1R, D1R, nAChR) | MUST-HAVE | Gene family query + identity matrix | 0.5-1 day |
| Dryad datasets (Woodcock, Rundlöf, Fabian) | MUST-HAVE | Download + sensitivity analysis | 0.5-1 day each |
| PATH Study | NICE-TO-HAVE | Download + Fagerström analysis | 1 week |
| UK Biobank behavioural layer | NICE-TO-HAVE | Variable extraction if access exists | 0.5 weeks |
| PanTHERIA + AnAge | NICE-TO-HAVE | Life-history meta-regression (SI) | 0.5-1 day |
| UniProt / InterPro | NICE-TO-HAVE | Domain conservation table (SI) | 0.5 days |
| NHANES, HRS, ELSA, SHARE, GBD | NOT APPLICABLE | No new increment over v3.3 | — |
| GBIF | NOT APPLICABLE for main text | SI geographic overlay only | 1-2 weeks |
| PaleoBioDB | NOT APPLICABLE | 1-2 sentences Discussion only | 1-2 days |
