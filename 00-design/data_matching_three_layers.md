# Stage 0δ — Three-Layer Data Matching Strategy

**Status:** Stage 0δ (data matching) — outputs feed Stage 0ε (final shortlist).
**Date:** 2026-04-17
**Supersedes:** Parts of `cfps_variable_inventory.md` §9 (the data-driven "8 domains" Tier-1/2/3 table). That table was built by inspecting CFPS columns and reverse-engineering domains. This document rebuilds from Stage 0α's 27 phenomenology cases forward to data, per `feedback_construct_from_phenomena.md`.
**Authorities used:**
- Construct: `sweet_trap_formal_model_v2.md` (Δ_ST + F1–F4 + Propositions P1–P4).
- Phenomena: `phenomenology_archive.md` §A (11 animal), §C (16 human), §D (false Sweet Traps, excluded).
- Data catalogue: `02-data/linkage/cfps_variable_catalog.csv` (205 columns × 86,294 person-years).
- External data registry: `/Volumes/P1/城市研究/INDEX.md` §01-个体调查.

**Guiding rule (hard constraint).** Phenomena → Construct → Data, never Data → Construct. D1 (996) and D7 (pure Internet 0/1) remain excluded even though their CFPS variables are the most complete; see §B.0 Exclusion Ledger.

---

## A. Layer A — Animal meta-analysis data strategy

### A.0 Objective

Layer A provides the cross-species universality evidence base. It is not new fieldwork; it is a *quantitative narrative synthesis* of already-published animal findings that test Proposition 1 (endorsement–fitness paradox), Proposition 3 (τ_env / τ_adapt trigger), and Proposition 4 (exposure > belief interventions, animal leg) on their non-human legs.

The Science benchmark is adg5277 (the 2023 light-at-night cross-species review) and abh0945 (Santos 2021 plastic ingestion evolutionary-trap synthesis). Our Section A meta is structured to match their granularity: one row per case × species × key study, with Δ_ST-analogue extracted where reported.

### A.1 Case-by-case data availability (11 animal cases)

| # | Case | Key empirical paper(s) | Data availability | Δ_ST proxy extractable? | Priority |
|:-:|:---|:---|:---|:---:|:---:|
| A1 | Moth-to-flame | Fabian et al. 2024 *Nat Commun* 15:689 (DOI 10.1038/s41467-024-44785-3); Dreyer et al. 2025 *Nature* N&V (DOI 10.1038/d41586-025-01709-5) | Fabian: high-speed video dataset, open via Dryad link in paper SI. Swaddle 2015 TREE 30:67 synthesises light-pollution mortality across 50+ species — supplementary Table S1 contains species-level mortality deltas. | Yes: dorsal-light-rule inversion angle; mortality rate under lit vs dark beach. | **Primary (tier 1)** |
| A2 | Sea-turtle hatchling | Salmon et al. 1995 foundational; Witherington & Bjorndal 1991 *Biol Cons*; FWC-Florida annual hatchling orientation reports 1995–2022 (NOAA open-data portal) | Open: FWC hatchling-misorientation datasets, 1995–present, beach × year panel. | Yes: proportion of hatchlings reaching the ocean under lit vs dark conditions. | **Primary** |
| A3 | Plastic ingestion | Santos et al. 2021 *Science* 373:56 DOI 10.1126/science.abh0945 (review with meta-table of 138 species) | Santos 2021 SI Table S1 is the meta-analysis substrate — already compiled. | Yes: species-level plastic ingestion rate × population-level reproductive failure (from Wilcox et al. 2015 PNAS for albatrosses; Schuyler 2013 Cons Biol for turtles). | **Primary** |
| A4 | Jewel-beetle/bottle | Gwynne & Rentz 1983; Fahrig et al. 2018 *Nature* 558:440 (DOI 10.1038/s41586-018-0074-6) is the canonical lethal-trap Nature paper; SI provides population-level data | Fahrig 2018 SI contains before/after beetle mount-rate data; regulation-change (bottle-colour ban, Western Australia 1989) provides a natural experiment. | Yes: male mate-choice preference toward bottles × population viability proxy. | **Primary** |
| A5 | Drosophila sugar | Libert et al. 2007 *Science* 315:1133 (olfactory lifespan); Pletcher/Libert lab follow-ups | Lab datasets open via Dryad; Nature 2026 DOI 10.1038/s41586-026-10306-z provides a contemporary sugar-sensor mechanistic paper. | Yes (the cleanest quantitative case): preference index for sucrose × median lifespan loss. | **Primary** |
| A6 | Olds-Milner self-stim | Olds & Milner 1954 J Comp Physiol Psychol; modern corpus-indexed Shadmehr 2023 Nature 614 (DOI 10.1038/s41586-022-05614-z) | Classical data reported in figures; not downloadable datasets but the quantitative endpoints (lever-pressing rate; food/water foregone) are consistent across replications. | Yes: by construction Δ_ST ≈ +1 — direct reward activation, zero fitness. | **Primary** (mechanistic anchor) |
| A7 | Fisher runaway (peacock, widowbird, swordtail) | Andersson 1982 *Nature* 299:818 widowbird; Basolo 1990 *Science* 250:808 swordtail; Kokko et al. 2002 *Proc R Soc B* 269:1331 continuum | Andersson 1982 tail-length manipulation field experiment has the quantitative data (Table 1). Kokko 2002 meta includes ≥30 studies with ornament cost ÷ mating benefit ratios. | Yes: ornament elaboration × individual survival cost; extract from Kokko meta + Alonso-Alvarez 2017 review. | **Primary** |
| A8 | Zahavi handicap failure | Trinidadian guppy rare-male preference (*Science* 2023 DOI 10.1126/science.ade5671, 22 cites indexed); songbird colouration loss (*Nature* 2015 DOI 10.1038/nature.2015.18735) | Science 2023 SI datasets open (dryad). Bright-males-yielding-fewer-young datasets available. | Yes, but noisier: signal cost × fitness deviation under environmental change. | **Tier 2** (weakest F4 — handicap slow-failure; include if primary 8 not reached) |
| A9 | Ecological trap (birds, insects on roads) | Schlaepfer et al. 2002 *TREE* 17:474 (theory); Horváth et al. 2009 *Front Ecol Environ* (polarised-light trap cross-species meta, already 20+ species); Robertson & Hutto 2006 *Ecology* 87:1075 | Horváth 2009 is a pre-compiled meta; Robertson & Hutto 2006 supplies the 4-criteria verification protocol — used across subsequent trap papers. Open Dryad datasets for indigo bunting (Shochat 2005 Auk), for dragonfly roof-laying (Horváth 2010). | Yes: preference index for trap habitat × realised fitness in trap vs source habitat. | **Primary** |
| A10 | Neonicotinoid bees | Woodcock et al. 2017 *Science* 356:1393 (DOI 10.1126/science.aam7470, 543 cites); Mitchell et al. 2017 *Science* 358:109 (DOI 10.1126/science.aan3684, 483 cites); Kessler et al. 2015 *Nature* 521:74; Rundlöf et al. 2015 *Nature* 521:77; Linguadoca et al. 2024 *Nature* 628:355 (DOI 10.1038/s41586-023-06773-3) | Woodcock 2017 SI dataset on colony reproduction is open. Rundlöf 2015 is the single cleanest choice-test dataset. Linguadoca 2024 is the most recent meta across European landscapes. | Yes: preference index for neonicotinoid-laced nectar × colony-level reproductive output. | **Primary** |
| A11 | Supernormal stimulus (Tinbergen) | Tinbergen 1951 foundational; *Nature* 2025 DOI 10.1038/s41586-025-09216-3 "Mapping the adaptive landscape of Batesian mimicry using 3D-printed stimuli" | 2025 Nature mimicry paper: open stimuli dataset. Multiple experimental traditions (eggs, gulls, fish) — coverage broad but fragmented. | Partially: preference strength for supernormal vs normal stimulus in lab; "fitness" usually not measured (lab horizon too short). | **Tier 2** (F3 weak — lab transients); retain as *diagnostic substrate* in SI |

### A.2 Preferred 8-case shortlist for Layer A primary synthesis

Selection criteria (applied in order): (i) Δ_ST extractable quantitatively; (ii) peer-reviewed within Nature/Science/TREE/Ecology/PNAS; (iii) covers all four routes (F1 Route A mismatch; F1 Route B novel signal; F3 via M1 individual habit vs M2/M3 social vs M4 mortality).

| # | Case | F1 route | F3 mechanism | Δ_ST unit | Primary source |
|:-:|:---|:---:|:---:|:---|:---|
| 1 | Moth/artificial light | A | M4 mortality | mortality/flight-exposure-hour | Fabian 2024 + Swaddle 2015 meta |
| 2 | Sea-turtle hatchling | A | M4 | proportion reaching ocean (baseline vs disturbed) | FWC 1995–2022 panel |
| 3 | Plastic ingestion, multi-taxa | B | M1 + M4 | ingestion rate × gastric-obstruction mortality | Santos 2021 SI Table S1 meta |
| 4 | Drosophila sugar lifespan | A | M1 | preference index × lifespan loss | Libert 2007 + Pletcher lab replications |
| 5 | Olds-Milner self-stim | B | M1 | lever-presses/hour × food/water forgone (proxy for fitness loss) | Olds & Milner 1954 + modern replications |
| 6 | Peacock/widowbird ornament | A | M2 | ornament size × individual survival cost | Andersson 1982 + Kokko 2002 meta |
| 7 | Ecological/road trap | A | M1 + M2 | preference for trap × F(trap) − F(source) | Horváth 2009 cross-species meta + Robertson-Hutto 2006 verified cases |
| 8 | Neonicotinoid bees | B | M1 + M2 | preference for neonic-nectar × colony reproductive output | Woodcock 2017 + Rundlöf 2015 + Linguadoca 2024 |

**Backup (if any primary fails peer-review or data-availability check):** A8 Zahavi failure (guppy/songbird); A11 supernormal stimulus (retained as diagnostic substrate for SI).

### A.3 Meta-analysis method

- **Method:** narrative synthesis + quantitative harmonisation. We do *not* claim new field data. Each case contributes (a) a standardised effect size (Hedges' g for preference, log-response-ratio for fitness), (b) a Δ_ST-analogue defined per case, (c) a qualitative F-profile.
- **Comparability:** all effect sizes converted to the shared scale "preference strength ÷ fitness loss, standardised to log units," following the pattern in Kokko 2002 and Santos 2021.
- **Heterogeneity reporting:** τ² and I² reported per proposition leg; random-effects pooling. Not a heterogeneity-fix exercise — we *expect* heterogeneity across species and *interpret* it via Proposition 3's τ_env / τ_adapt ratio.
- **Pre-registration target:** OSF, before Layer B FE regressions are run, so we cannot tune animal meta to fit human results.

### A.4 Work estimate

| Subtask | Days | Output |
|:---|---:|:---|
| A.4.1 Compile effect sizes from 8 primary papers' SI + meta-tables | 4 | Excel/CSV, one row per study-species-effect |
| A.4.2 Cross-walk Δ_ST units (correlation, preference ratio, log response) | 2 | Conversion script + validation |
| A.4.3 Forest plots per proposition (P1, P3, P4) | 2 | 3 PDF figures |
| A.4.4 Write SI Appendix C §"Animal meta-analysis" | 3 | ~15-page SI section |
| A.4.5 Pre-registration lodged at OSF | 1 | osf.io link |
| **Total** | **12 working days** | |

Critical risk: Santos 2021 Table S1 uses heterogeneous "ingestion rate" denominators across taxa — requires 1 extra day for harmonisation.

---

## B. Layer B — Human within-person re-audit (CFPS × 16 Stage 0α cases)

### B.0 Exclusion ledger (phenomena deliberately kept out of CFPS mapping)

Per Stage 0α §D and `feedback_construct_from_phenomena.md`:

- **D1 996 (coerced)** — F2 fails. CFPS has `workhour` N=41,528 but we do not promote it to a focal domain. If used at all in the paper, it appears as a *negative control*: we predict no Sweet Trap signal in the coerced-sample, which supports F2 as a diagnostic criterion.
- **D2 cigarette/nicotine** — pharmacological addiction, F1 wrong mechanism. `qq201` smoked-past-month kept only as covariate.
- **D3 gambling** — compulsion, F2 epistemic criterion fails. Not in CFPS main file anyway.
- **D4 oniomania** — clinical; out.
- **D5 poverty trap** — structural. Out; our λ proxies separate externalisation from constraint.
- **D6 workaholism (grey)** — grey-zone per Stage 0α §D.6; not in focal list; discussed as scope boundary.

### B.1 Reverse mapping — each of the 16 human Sweet Trap cases vs CFPS columns

| # | Human case (Stage 0α §C) | Sweet signal (R_agent) | Bitter outcome (F) | λ proxy | CFPS verdict | Key CFPS variables | FE-feasible? |
|:-:|:---|:---|:---|:---|:---:|:---|:---:|
| C1 | 打鸡血/画饼 (aspirational overwork) | Anticipated career success + belonging | Burnt-out health, savings-shortfall, spouse loss | Tenure × equity illusion | **Partial** (N~20K employed adults with multi-wave satisfaction) | `qg405` (promotion satisfaction), `qg406` (overall job satisfaction); `qn12012` (life satisfaction); `qn12016` (future confidence); `health`, `unhealth`, `qp401`, `qq4010` (sleep); `fwage` (family wage income) as aspirational proxy; `jobclass` to screen out coerced-formal contracts | Yes, but weak — requires heterogeneity-by-`worknature` to separate endorsed from coerced overwork. Best used as **negative/positive control pair with D1 996** (`workhour`>48) to demonstrate F2 *graded*. |
| C2 | 鸡娃 (intensive parenting) | Parent status pride in child's "winning" | Parent savings shortfall, parent life-satisfaction reversal, child psychological distress | `child_num > 0` + `child_gender` + urban dummy | **Yes — Focal** | `eexp` + `school` (education/tutoring spending, N=85,594); `eec` (culture-education-entertainment, N=84,856); `dw` (self-rated social status); `qn12012` (parent life satisfaction); **double-减 natural experiment 2021–2022 DID cut** | Yes. `pid × year` fixed effects on parents. Child outcome requires merge with CFPS youth module (fid × cyear) — identified gap. |
| C3 | Livestream tipping (直播打赏) | Parasocial recognition | Financial ruin, consumer credit debt | Age × marital single × urban | **Insufficient (CFPS)** — no platform variables | Only `onlineshopoping` 0/1 (N=28K, 2014-2022) and `internet` 0/1; no tipping, no platform-specific spend | No. Flagged for **supplementary data collection (platform webscraping or linked panel)**. See §B.4. |
| C4 | 彩礼 (bride-price) | Family honour + commitment-device signal | 20-year debt service, delayed marriage of sisters, pronatalist pressure | Groom vs bride family; sex-ratio × county | **CFPS main file insufficient** — only `marrige` 0/1 | `marrige`/`mar`; no amount, no wedding cost, no date | No (in CFPS main). **Requires CGSS 2013/2017/2021 bride-price modules or CHARLS marriage-history module.** See §C.1 for CGSS mapping. |
| C5 | Luxury goods / conspicuous consumption | Status-signalling reward | Savings erosion, consumer debt | Peer urbanism × age | **Partial** | `dress` (clothing, N=84,841); `daily` (household goods, N=83,970); `eec` (culture-education-entertainment); `durables_asset` (durable goods including cars, N=71,923); `dw` (self-rated status); `nonhousing_debts`, `Nhd`; `qn12012` life satisfaction | Yes for "conspicuous consumption" as a composite treatment (total luxury-adjacent spend / disposable income); but no brand variable. **Tier 2 / SI supplement.** |
| C6 | 保健品 / 养生执念 | "Doing something for my health" identity | Savings loss, actual health unchanged or worse | Age (elderly focus); rural low-science-literacy | **Partial** | `med` / `mexp` (medical-health expense, N=85,401) minus insurance-reimbursable — can construct out-of-pocket supplement spend; `health`, `qp401` (chronic disease) as outcome; `age` × rural as λ. Does not separate supplements from legitimate care. | Marginal; CFPS does not decompose medical spending into legitimate vs supplement. Would require linkage to pharmaceutical retail data. **SI only.** |
| C7 | MLM / 传销 | Upward-mobility narrative + belonging | Financial ruin + family rupture | N/A (out) | **Not in CFPS** | — | No. Acknowledge as an *out-of-panel* case in Discussion; rely on regulator data (MPS 传销 case registry) for qualitative treatment. |
| C8 | Investment FOMO | Trend-chasing reward | Wealth loss, late-entry cohort | Credit access × education | **Partial** | `financial_product` (N=33,466, 2018-22); `fxzc` (risk assets, N=29,634); `fincome1` (family income) as wealth denominator; `qn12012`, `qn12016` as affect outcomes; **no fund/stock-by-year holding-level variables**. **CHFS (家庭金融调查) is the right data** — see §C.2. | CFPS marginal. **CHFS 2013–2019 panel is the correct source** — available on P1 at `/Volumes/P1/城市研究/01-个体调查/CHFS_家庭金融_2011-2019/`. |
| C9 | 知识付费 FOMO | Self-improvement identity | Career unchanged, savings loss | Age × education × urban | **Not in CFPS** | No paid-course variable; `eec` conflates entertainment, culture, and adult-education | No. Out-of-panel; rely on platform reports in Discussion. |
| C10 | 宗教 / 民间信仰 over-donation | Supernatural patronage reward | Savings loss + unfalsifiable updating | Age + rural + specific provinces | **Not quantified in CFPS main** | CFPS 2012 had a `qm701` religion module but not in the cleaned panel we have; `social` (gift-giving, N=57,579) conflates religious donation with life-cycle gifting | Out-of-panel (with minor exception: aggregate gifting). Discussed as cross-cultural exemplar. |
| C11 | Sugar/fat/salt | Gustatory reward | Chronic disease (diabetes, hypertension), obesity | Age × medical coverage | **Yes — Focal, but proxied** | `food` (food spending, N=84,365) as imperfect proxy; `qp401` chronic disease (N=84,351); `health` (N=85,948); `unhealth`; `mexp` medical expenditure. **CHARLS Wave 2015 and 2018 biomarkers (HbA1c, BMI, blood pressure) are the gold standard** — available on P1 at `/Volumes/P1/城市研究/01-个体调查/CHARLS_中老年_2011-2020/`. | CFPS yes for FE on `food`×`qp401`; **CHARLS supplement for biomarker-grounded robustness check.** |
| C12 | Short-video / gacha | Variable-ratio dopaminergic reward | Sleep loss, attention/mental health | Age × hukou × rural | **Insufficient in CFPS** | Only `internet` 0/1, `mobile` 0/1, `computer` 0/1, `onlineshopoping` 0/1; no usage time; no app-level data; `qq4010` sleep hours N=26,880 | No panel-grade test. Allcott 2020 + Braghieri 2022 already cover global identification; we cite and move on. |
| C13 | Relationship-consumption (matchmaking) | Aspirational mate-search | Financial loss + no match | Age × gender × urban | **Not in CFPS** | No matchmaking variable | Out-of-panel. |
| C14 | (grey area — religion; same as C10) | — | — | — | — | — | — |
| C15 | Fitness/body-transformation consumerism | Somatic-investment identity | Injury + net financial loss | Age × income × urban | **Not in CFPS** | No gym/fitness expenditure; `eec` conflates | Out-of-panel. |
| C16 | International-school / elite education | Parental investment-in-offspring signal | Capital opportunity cost + cultural displacement | Urban × top-tier city | **Subset of C2 鸡娃** — merge | `eexp` × urban × top-tier-city interaction | Yes within C2 focal domain as heterogeneity cut. |

### B.2 Post-audit: which human cases qualify for primary within-person FE?

Using Andy's stated criterion (≥2 waves CFPS × valid Sweet signal + Bitter outcome within person, plus F2 graded above 0.7 on subjective endorsement):

| Case | CFPS-FE feasible? | Reason | Role in paper |
|:---|:---:|:---|:---|
| C1 打鸡血 | **Partial** | Sweet (`qg405/406` promotion satisfaction; `qn12016` future confidence) + Bitter (`health`, `qp401`, `qq4010`) all within-person; but no tech-layoff cohort flag. Needs Alibaba/Tencent 2022–2024 layoff cohort cross-walk. | Focal A (focal **conditional** on layoff cross-walk; otherwise demoted to SI) |
| C2 鸡娃 × 双减 | **Yes** | 2021 policy cut is sharp; `eexp`/`school` drops 40-60 % post-policy in treated strata; `qn12012` + `dw` within-person | **Focal A (definite)** |
| C5 luxury (subset of conspicuous consumption) | **Yes** | Aggregate-visible expenditure (`dress`+`durables_asset`+`eec`) vs savings + `qn12012` | Focal B (if we keep 4 focal) |
| C11 sugar/fat/salt | **Yes** | `food` × `qp401` + CHARLS biomarker bridge | Focal C |
| All others | No (see table above) | Data insufficient | Mentioned in Discussion, SI, or cross-cultural Layer C |

### B.3 Updated Focal shortlist (humans) — three primary + one conditional

1. **C2 鸡娃 × 双减 DID** — policy-identified; strongest Chinese novelty + best identification; CFPS + CFPS youth module.
2. **C4 彩礼 × sex-ratio IV** — conceptually strongest (Zahavian runaway × sex-ratio macro-IV, direct animal-F7 analogue); requires **CGSS** (or CFPS family module `fa`/`fb`) supplement.
3. **C11 sugar/fat/salt × CHARLS biomarker** — Lieberman paradigm × biomarker-grounded; directly parallel to Layer A5 Drosophila.
4. **C1 打鸡血 × tech-layoff cohort** (conditional on layoff-roster cross-walk) — the canonical F2 endorsement case that differentiates from D1 996.

These four humans × eight animals × two–three cross-cultural cases (Layer C) = the full paper skeleton.

### B.4 Data gaps requiring supplementary collection

Tagged for Andy's Stage 1 decision (Collaboration Contract v1 Fork #4: data-supplement decision):

- **C4 彩礼**: CGSS 2017/2021 bride-price module (already on P1, just needs integration — no new collection). **Action:** integrate CGSS, no new collection required.
- **C11 sugar/fat/salt**: CHARLS 2015/2018 blood-sample biomarker (HbA1c, BP) — already on P1. **Action:** integrate CHARLS, no new collection.
- **C1 打鸡血**: Tech-layoff roster cross-walk. Options: (a) self-reported layoff events in CFPS `qg` module; (b) web-scraped layoff database (LayOffs.fyi China mirror + Maimai posts); (c) official labour-dispute arbitration records. **Action:** Andy decision at Stage 0ε — likely (a) + SI discussion of (b).
- **C3 livestream, C7 MLM, C8 investment-FOMO (beyond CHFS), C9 knowledge-payment, C10 religion, C12 short-video, C13 matchmaking, C15 fitness**: all require new data collection. **Verdict:** out of the paper's Primary empirical section; they appear only in the Stage 0α cross-species Table 1 and the cross-cultural universality claim.

### B.5 What changed from the 8-domain inventory

| Old tier (`cfps_variable_inventory.md` §9) | New tier (this doc) | Reason |
|:---|:---|:---|
| Tier-1: D1 urban + D3 996 + D8 housing | Tier-1: C2 鸡娃 × 双减 + C4 彩礼 (CGSS) + C11 diet (CHARLS) + C1 打鸡血 (conditional) | D1 is a Study-1 bridge, not a Sweet Trap per se; D3 996 fails F2; D8 housing is a Sweet Trap but does not fit the three-cluster narrative (F.1/F.2/F.3 of Stage 0α §F) as cleanly as C2 (runaway), C4 (Zahavi), C11 (mismatch). Housing moves to SI robustness. |
| Tier-2: D2 鸡娃 + D5 diet | Promoted to Tier-1 | Stage 0α identified these as the cleanest mappings to Propositions P1/P3/P4 with cross-species parallels. |
| Tier-3 (暂弃): D4 彩礼 | Promoted with **CGSS integration** | Conceptually critical (Zahavi × sex-ratio = the cleanest human analogue of A7 Fisher runaway). Do not drop. |
| Tier-3 (暂弃): D6 BNPL, D7 social media | Stay dropped from focal | But BNPL folded into C5 luxury as robustness; social media remains cited via Allcott/Braghieri. |

---

## C. Layer C — Cross-cultural universality check (WVS / ESS / Gallup / CGSS)

### C.0 Objective

Proposition 4's human leg (exposure > belief interventions) and Proposition 3 (τ_env/τ_adapt) require evidence *outside China*. Without Layer C, the paper is at best Nature Human Behaviour grade (China-centric behavioural econ), not Science.

### C.1 CGSS (Chinese General Social Survey) — bridge from CFPS to cross-culturally-comparable survey

**Location:** `/Volumes/P1/城市研究/01-个体调查/CGSS_2011-2023/` (waves 2011, 2012, 2013, 2015, 2017, 2018, 2021, 2023).

**Why CGSS is included in Layer C rather than Layer B:** CGSS uses *ISSP* (International Social Survey Programme) and *EASS* (East Asian Social Survey) identical modules for religion, family, and consumption — each cycle is a cross-culturally harmonised module. Using CGSS automatically places the Chinese estimates on the ISSP scale.

**Variable availability for focal domains:**

| Focal domain | CGSS module(s) with relevant variables | Waves | Notes |
|:---|:---|:---|:---|
| C4 彩礼 | Marriage & Family module (A58 婚姻 series); 2017 ISSP Family module | 2013, 2017, 2021 | 2017 is the gold-standard wave for bride-price amount, groom/bride family bearer, debt |
| C2 鸡娃 | Education aspiration (EASS 2016 module); Parenting-time-use | 2015, 2017, 2021 | Less rich than CFPS for spending, but harmonises to Korea/Taiwan/Japan equivalents for cross-cultural comparison |
| C11 diet | Health lifestyle module | 2013, 2015 | Lower priority vs CHARLS biomarker |
| C1 打鸡血 | Work values module (ISSP Work Orientations 2015) | 2015 | Directly comparable to 34 ISSP countries |

**Work estimate for CGSS integration:** 8 days (see §D).

### C.2 CHFS (Chinese Household Finance Survey) — for financial-FOMO auxiliary

**Location:** `/Volumes/P1/城市研究/01-个体调查/CHFS_家庭金融_2011-2019/`.
**Waves:** 2013, 2015, 2017, 2019 panel. ~40,000 households.
**Relevance:** C8 investment-FOMO supplementary (not focal).
**Role:** SI robustness, not Layer C cross-cultural check per se. Still appears here because it sits in the "data-supplement decision" sub-tree.

### C.3 WVS / ESS / Gallup / ISSP — the three cross-cultural checks

Not currently on P1. Requires download.

| Data source | URL / access | Variables relevant to our propositions | Proposed Sweet-Trap case mapping | Work |
|:---|:---|:---|:---|:---:|
| **World Values Survey (WVS)** Wave 7 (2017–2022) | worldvaluessurvey.org, CC-BY | Life satisfaction (A008); happiness (A170); consumption-status attitudes (E016, E033 materialism); family values (D019 children-needed-for-fulfilment); religion (F034 religious donation); income & assets (X047_WVS7, X051); education aspirations (X025CSWVS) | C11 diet (F1 Route A): test Nutrition-transition cross-country; C2/C16 parenting investment; C5 luxury-status attitudes | Download 3 days |
| **European Social Survey (ESS)** Rounds 8–11 (2016–2024) | europeansocialsurvey.org, CC-BY | Life satisfaction (stflife); subjective health (health); work-life balance (wrklfbw); happiness (happy); consumption-debt items in the supplementary rounds | C1 aspirational overwork (cross-EU work-values); cross-cultural baseline for C11 diet | Download 2 days |
| **Gallup World Poll** (restricted) | gallup.com, requires license (~$$$) | Best-worst life evaluation (Cantril ladder); emotional wellbeing (positive/negative affect); food security; financial stress | Global cross-walk for all propositions; the paper's "global" leg | Access evaluation — *defer, probably replaceable by WVS+ESS* |
| **ISSP** (International Social Survey Programme) | gesis.org, CC-BY | Modules rotate: Family (2002, 2012, 2022), Work (2005, 2015), Social Inequality (2019) | C4 彩礼 (Family 2012/2022); C1 aspirational (Work 2015); C5 conspicuous (Inequality 2019) | Download 2 days |

### C.4 Final Layer C shortlist

Minimum viable cross-cultural check:

- **ISSP Family 2012/2022** for C4 彩礼 — gives cross-country bride-price/dowry prevalence in ~40 countries.
- **ISSP Work 2015** for C1 打鸡血 — gives cross-country aspirational-work-values scale.
- **WVS Wave 7** for C11 diet + C5 status consumption — gives ~80 countries life-satisfaction × materialism × body-image.
- **ESS Rounds 8–11** as a European robustness check for all four focal domains.

Skip Gallup in the first version; if reviewers ask for it, we can license it later.

### C.5 What Layer C lets us say

- **P3 (τ_env / τ_adapt)**: plot Σ_ST (composite persistence severity, estimated per country) against time-since-phenomenon-onset — e.g., for diet, the "post-1980 sugar-tax-transition" date for each country. Predict: larger Σ_ST in countries with compressed transition timelines (China ~25 yrs; Nigeria ~15 yrs; Sweden ~120 yrs).
- **P4 (exposure > belief)**: for each country with a known policy timing (sugar tax, wedding-expense caps, tutoring restriction), compute policy × Σ_ST within-country — predict larger effect from exposure policies.
- **Universality claim**: the F1–F4 diagnostic signature holds in ≥3 cultural clusters (East Asian, European, Anglo-American, Latin American, Sub-Saharan African) for ≥2 focal domains each.

### C.6 What Layer C cannot provide

- No within-person FE in WVS (cross-sectional, not panel). ESS has a partial rotating panel but not long enough for within-person FE.
- No Sweet Trap "endorsement" measure in the raw ISSP modules — we must use indirect proxies (e.g., stated approval of lavish weddings = F2 endorsement for C4).
- Sample-size heterogeneity: WVS/ISSP per country N ≈ 1,000–2,000. Statistical power for cross-country test is at the country level (N ~ 40–80 countries), not the person level.

**Honest framing in the manuscript:** Layer C is a *universality check*, not a primary identification layer. Primary identification lives in Layer A meta + Layer B CFPS FE + CGSS/CHARLS supplements.

---

## D. Total work estimate by layer and data-preparation timeline

| Layer | Subtask | Days |
|:---|:---|---:|
| **A Animal meta** | Compile 8 cases + Δ_ST harmonisation + forest plots + OSF | 12 |
| **B.1 CFPS base** | Re-derive C2, C5, C11, C1 from CFPS (`pid × year` FE) | 8 |
| **B.2 CFPS × 双减 DID** | 2021 policy panel cut, parent × wave DID | 4 |
| **B.3 CFPS youth module merge** | Family-level cross-table for C2 child outcomes | 5 |
| **B.4 CGSS integration** | C4 彩礼 module + cross-wave panel | 8 |
| **B.5 CHARLS biomarker merge** | C11 diet + HbA1c / BP / BMI | 5 |
| **B.6 C1 layoff cross-walk** | Decision tree from Stage 0ε | 0 or 10 |
| **C.1 ISSP download + harmonise** | Family 2012/2022; Work 2015; Inequality 2019 | 4 |
| **C.2 WVS Wave 7 harmonise** | Life satisfaction × status + diet attitudes | 3 |
| **C.3 ESS Rounds 8–11** | European robustness | 3 |
| **C.4 Cross-cultural regressions** | P3/P4 cross-country slopes | 5 |
| **D Spec curve** | Joint specification curve on focal 4 × Layer C × Layer A | 6 |
| **Total** | — | **~63 working days (~3 mo, solo), ~40 days if parallelised** |

### D.1 Parallelisation plan

Layer A + Layer B + Layer C can be executed in parallel:
- Animal meta (Layer A) is a synthesis task — independent.
- Layer B CFPS focal regressions — the project's primary empirical workstream.
- Layer C ISSP/WVS downloads — background task, wait for files then harmonise.

Recommended sequencing:
1. **Month 1:** B.1 CFPS baseline + A.1 animal compilation start + C.1 ISSP download (parallel).
2. **Month 2:** B.2 双减 DID + A.2 Δ_ST harmonisation + C.4 cross-cultural regressions.
3. **Month 3:** B.3 youth merge + B.4 CGSS + B.5 CHARLS + C.2/C.3 WVS/ESS + D spec curve.

This puts first-draft ready at ~3 mo from Stage 0 complete, matching Andy's 2026-04-16 target on the companion urban-wellbeing-curvature project.

---

## E. Next-step decisions Andy must make (Stage 0ε trigger)

1. **Confirm 4 focal humans** (C2, C4, C11, C1-conditional) per §B.3 — or override.
2. **Confirm Primary 8 animal cases** per §A.2 — or swap A8 handicap in if stronger Δ_ST derivable.
3. **Layer C minimum**: confirm ISSP + WVS only (drop Gallup); or require Gallup.
4. **C1 打鸡血 data decision** (per Collaboration Contract v1 Fork #4): do we cross-walk layoff-roster data or demote C1 to SI?

On these four decisions `final_shortlist_and_design.md` is written and Stage 1 can begin.

---

*End of Stage 0δ three-layer data-matching document. Downstream: `final_shortlist_and_design.md`, then Stage 1 analysis-plan registration on OSF.*
