# H6f Phylum Coverage (triaged pilot)

Generated: 2026-04-24 11:54:23

## Triage process

- Input: `outputs/H6f_full_harvest.csv` (raw PubMed harvest, 9 queries).
- Filters applied (pre-registered in `H6f_search_strategy.md` §4):
  1. Non-canonical review articles dropped.
  2. Title-keyword boost for canonical manipulation terms (knockout, CRISPR, RNAi, pharmacological, mutant, etc.).
  3. Year weighting: 1995-1998 seminal boost, 2005-2015 slight downweight, 2016+ recent-CRISPR boost.
  4. Per-phylum caps ensuring no single bucket dominates (targets ~80-150 total).
  5. Canonical anchor PMIDs force-included regardless of filter (Johnson-Kenny 2010; de Bono 1998; Baldwin 2014).

## Triaged pilot counts by phylum bucket

| Phylum bucket | Cap | Retained |
|---------------|-----|----------|
| Chordata (rodent) | 35 | 35 |
| Chordata (non-rodent) | 10 | 10 |
| Arthropoda (Drosophila) | 15 | 15 |
| Arthropoda (Hymenoptera) | 15 | 15 |
| Nematoda | 15 | 15 |
| Mollusca | 15 | 15 |
| Cnidaria | 12 | 12 |
| cross-phylum | 8 | 8 |
| **TOTAL** | ~125 | 125 |

## Coverage pre-registered thresholds

- **Minimum (Paper 1 required):** >= 2 phyla with >= 5 studies each after full-text screening.
- **Ideal:** 4 phyla with 3-10 coded experiments each.
- Pilot-level phyla covered: **8 buckets with >= 5 pilot entries**.

## Canonical anchor inclusion verification

- PMID 20348917 [INCLUDED] : Johnson PM & Kenny PJ 2010 Nat Neurosci - Drd2 palatable food rats
- PMID 9741632 [INCLUDED] : de Bono M & Bargmann CI 1998 Cell - NPR-1 C. elegans social feeding
- PMID 25146290 [MISSING] : Baldwin MW et al. 2014 Science - TAS1R1 hummingbird sweet detection (biochem, not manipulation; retained for H6a positive-control reference)

## Week-2 workflow

1. Each pilot row gets title + abstract triage: `include_candidate`, `exclude_review`, `exclude_not_manipulation`, `exclude_not_reward_receptor`, `exclude_human_only`, `unclear_needs_fulltext`.
2. `unclear` + `include_candidate` rows proceed to full-text.
3. Coding uses `H6f_extraction_template.csv` schema.
4. 20% double-coding for kappa.
5. If final included N < 30 or < 3 phyla, sample additional rows from `H6f_full_harvest.csv` by dropping the phylum cap on the under-represented bucket(s).

## Notes on cnidarian coverage

- Cnidaria bucket is shallow (~20 raw hits). Full-text attrition likely leaves 0-2 usable cases.
- **Planned supplementation:** manual harvest from Layden & Martindale (2014) *Nematostella* neuropeptide literature + Anderson et al. 2020 jellyfish behavioural reviews via reference-list trawl.
- If Cnidaria ends with 0 coded experiments, H6f falls back to 3-phylum coverage (Chordata + Arthropoda + Nematoda) which still passes the minimum threshold.