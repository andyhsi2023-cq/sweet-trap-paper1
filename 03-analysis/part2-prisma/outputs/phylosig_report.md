# H3 Phylogenetic Signal Test — Δ_ST Proxy Across Species

**Sweet Trap Paper 1 — §3.2**
Analysis date: 2026-04-25
Script: `03-analysis/part2-prisma/scripts/06_phylosig_H3.R`

---

## 1. Hypothesis and decision rule

**H3 (phylogenetic independence).** Sweet Trap vulnerability (Δ_ST proxy) is
*not* strongly phylogenetically clustered. If vulnerability arises from shared
reward-system architecture and modern environmental mismatch rather than from
common recent ancestry, the trait should show weak-to-absent phylogenetic
signal across our cross-phylum case corpus.

**Pre-stated decision rule (task brief).**

| Outcome | Verdict |
|---|---|
| Blomberg's K > 1 **or** Pagel's λ > 0.7, *p* < 0.05 | SUPPORTED (trait clusters phylogenetically — H3 would *fail*) |
| K near 0 **or** λ near 0 | NOT SUPPORTED (informative null — H3 *holds*) |

Under H3 as formulated for Paper 1, an "informative null" (K≈0, λ≈0) is the
*predicted* result: vulnerability is orthogonal to deep phylogeny.

---

## 2. Methods

### 2.1 Phylogeny construction
- **Source.** TimeTree 5 web API (`timetree.org/ajax/prune/widget_load_names/`),
  retrieved 2026-04-25.
- **Input.** 76-line species list at
  `outputs/species_list_for_timetree.txt` covering the 114-case PRISMA corpus.
- **Resolution log (TimeTree).**
  - 2 taxa not found in NCBI: *Cyrtodiopsis dalmanni*, *Paro cristatus*.
  - 11 taxa substituted with nearest relative (e.g. *Bombus terrestris* → *Bombus*;
    *Ursus arctos horribilis* → *Ursus arctos*; *Ixodes scapularis* →
    *Ixodes hexagonus*; *Perciformes* → *Monodactylus argenteus*).
  - 7 taxa with insufficient data (Photinus, Steinernema, Scarabaeus satyrus,
    Tripedalia, Julodimorpha, Tubifex, Oncopeltus).
- **Output.** Full TimeTree return (`species_tree_timetree.nwk`) contained
  7,427 tips because order-level queries (Lepidoptera, Odonata, Ephemeroptera,
  Chiroptera) were expanded to all member species.
- **Pruning.** We mapped each case's `species_binomial` to the first matching
  tip (exact binomial first; genus-level fallback if binomial missing). The
  resulting pruned tree (`species_tree_pruned.nwk`) has 56 tips.
- **Format.** Tree is a time-calibrated chronogram in Myr; forced to strict
  ultrametricity for phytools (`force.ultrametric`, method `"extend"` — only
  numeric-tolerance rounding was needed, not rate smoothing), then binarised
  via `multi2di` (deterministic, seed fixed).

### 2.2 Trait vector
- **Variable.** `delta_st_proxy` (0–1 continuous, 5-component Sweet Trap score).
- **Case → species averaging.** Cases sharing a tip (e.g. three *Apis mellifera*
  cases) averaged to one species-level mean. Provenance in
  `phylosig_species_map.csv`.
- **Exclusions.** 44 cases dropped (unmapped tip, NA Δ_ST, or phylum="Multiple");
  logged.
- **Final analytic sample.** n = 56 species tips, 71 cases contributing.

### 2.3 Tests
- **Blomberg's K** — `phytools::phylosig(..., method="K", test=TRUE, nsim=9999)`.
- **Pagel's λ** — `phytools::phylosig(..., method="lambda", test=TRUE)`.
- **95 % CIs** — non-parametric bootstrap of the trait vector on the fixed
  pruned tree, B = 1000 draws, percentile method.
- **Moran's I (robustness)** — `ape::Moran.I` with W = 1 / D (D = patristic
  cophenetic distance; diagonal zeroed).
- **Subgroup analyses** — Chordata only, Chordata + Arthropoda, Arthropoda only
  — to show the main result is not an artefact of one dominant clade.

---

## 3. Results

### 3.1 Full corpus (n = 56 species, 7 phyla)

| Statistic | Estimate | 95 % CI | p |
|---|---:|:---:|---:|
| Blomberg K | **0.117** | [0.056, 0.169] | 0.251 |
| Pagel λ | **0.0001** | [0.0001, 0.413] | 1.00 |
| Moran's I (1/D) | −0.032 | — | 0.626 |

All three independent measures agree: **no detectable phylogenetic signal** in
the Δ_ST proxy. K is well below 1 (the Brownian-motion expectation) and not
significantly different from 0; λ is pinned at the lower boundary with
likelihood-ratio p ≈ 1; Moran's I is essentially zero.

### 3.2 Subgroups

| Subset | n | K | p(K) | λ | p(λ) |
|---|---:|---:|---:|---:|---:|
| Chordata only | 37 | 0.122 | 0.505 | 0.0001 | 1.00 |
| Chordata + Arthropoda | 50 | 0.105 | 0.406 | 0.0001 | 1.00 |
| Arthropoda only | **13** | **1.446** | **0.007** | **1.162** | **0.020** |

The **main null is robust**: both vertebrate-dominated subsets replicate K ≈
0.1 and λ ≈ 0. The Arthropoda-only subset (n=13, small) shows significant
clustering — this is driven by high Δ_ST values concentrated in phototactic
insects (moths, beetles, hemipterans sharing ALAN-vulnerability) relative to
non-phototactic arthropods (ticks, spiders, stoneflies). We interpret this as
*within-clade convergence on a shared modern stimulus type (ALAN)*, not as
evidence that Arthropoda-wide phylogeny predicts vulnerability; the finding is
compatible with the main result at the whole-corpus level.

---

## 4. Interpretation for Paper 1 §3.2

**Verdict: H3 NOT rejected (informative null as predicted).**

The Δ_ST proxy behaves as a near-phylogenetically-neutral trait across 56
species from 7 phyla spanning ~800 Myr of divergence. Three independent
statistics — Blomberg's K, Pagel's λ, Moran's I on patristic distances —
converge on a null. This supports the central claim of Paper 1:

> Sweet Trap vulnerability is predicted by the *mismatch* between an
> organism's reward-system architecture and its current signal environment,
> not by its phylogenetic position. A sea turtle hatchling misled by beach
> lighting and a moth circling a streetlamp share a mechanism (celestial-
> compass exploitation) despite >600 Myr of divergence; a tick and a honeybee
> share a phylum but diverge sharply on Δ_ST because only one is exposed to a
> modern supernormal signal.

### Boundary condition
The Arthropoda subgroup signal warns that **within narrow clades exposed to a
single shared novel stimulus (ALAN for phototactic insects), phylogenetic
convergence can emerge**. This is not evidence against H3 at the construct
level; it is the expected pattern when environmental exposure and clade
membership happen to be correlated. We note this caveat in the Paper 1
Discussion and recommend stimulus-stratified analyses as future work.

### Deviation log row #5
Pre-registered prediction of K < 0.3 and λ < 0.3 both satisfied. No deviation;
result is recorded as planned under Analysis Plan v4.

---

## 5. Files

| File | Purpose |
|---|---|
| `outputs/species_tree_timetree.nwk` | Raw TimeTree return (7,427 tips) |
| `outputs/species_tree_pruned.nwk` | Analytic tree (56 tips) |
| `outputs/phylosig_main.csv` | K, λ, Moran's I, 95% CIs, p values |
| `outputs/phylosig_subgroups.csv` | Chordata / Chordata+Arthropoda / Arthropoda |
| `outputs/phylosig_species_map.csv` | Case → tip provenance |
| `scripts/06_phylosig_H3.R` | Reproducible pipeline (seed = 42) |

### Software
R 4.5.3 · `ape` 5.x · `phytools` 2.5-2. Random seed fixed at 42. Bootstrap
B=1000; permutation nsim=9999 for K.
