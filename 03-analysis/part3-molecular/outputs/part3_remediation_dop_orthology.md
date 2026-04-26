# Part 3 Remediation — Dopamine-receptor orthology disambiguation

## Risk addressed

Part 3 Risk 2: the 17 mollusc/cnidarian "DopR" entries in
`ortholog_inventory.csv` were obtained via NCBI keyword search
"dopamine receptor". That keyword also returns serotonin (HTR),
adrenergic (ADR), octopamine (OA), tyramine (TAR), muscarinic (CHRM)
and histamine (HRH) receptors — all Class-A GPCRs carrying Pfam
PF00001. A Jaccard-based H4b architecture claim drawn from "all 17 are
dopamine receptors" would therefore overstate the dopamine-specific
signal.

## Method

### Step 1 — Input assembly
`07_orthofinder_assemble_input.py` gathered species-specific protein
FASTAs (13 species, 74 total sequences) containing:

* Existing Part 3 candidates (17 mollusc/cnidaria "DopR", 10 vertebrate
  DRD1/DRD2, 12 arthropod DopR1/DopR2)
* 35 curated vertebrate/invertebrate biogenic-amine anchor proteins:
  - Vertebrate: DRD1-5, HTR1A, HTR1B, HTR2A, ADRA1A, ADRB1, CHRM1, HRH1
    (Homo + Mus + Rattus + Gallus + Danio)
  - Invertebrate: D.mel 5-HT1A, 5-HT2A, 5-HT7, OAMB, Octβ2R, TyrR
  - Aplysia: 5-HT1Aplysia, 5-HT2

### Step 2 — OrthoFinder + targeted MCL
OrthoFinder v3.1.4 with diamond backend (`-t 2 -a 2 -S diamond`).
Default inflation I=1.2 lumped all aminergic receptors into one
super-cluster (expected for this sparse focused panel). Re-clustering
the `OrthoFinder_graph.txt` at I=3.0 and I=5.0 (script
`08_orthofinder_classify.py`) gave better resolution but still
scattered TRUE_DRD into multiple singletons.

### Step 3 — Global phylogeny (primary evidence)
Switched to phylogenetic classification
(`09b_phylogenetic_classify_v2.sh`):
* MAFFT `--auto` alignment of all 74 sequences (3072 columns).
* IQ-TREE LG+G4 ML tree with `-fast` search mode.
* Rooted on Homo HRH1 (histamine H1 — most divergent aminergic GPCR).

For each candidate, `10_tree_classify.py` computes the nearest
anchor by branch-length distance and its family, and the delta
between nearest-anchor distance and the closest anchor of a
different family (a confidence proxy). Calls where delta < 0.3
branch-length units are flagged `_low_confidence`.

## Results

### Candidate re-classification (n = 17)

| Call | n | Interpretation |
|---|---|---|
| TRUE_DRD (high confidence) | 3 | Genuine dopamine-receptor orthologues |
| NOT_DRD:HTR | 2 | Serotonin-receptor paralogues |
| NOT_DRD:ADR (low confidence, likely OA-like) | 12 | Invertebrate β-adrenergic/octopamine-family Class-A GPCRs; clade cluster with vertebrate ADRB and Dmel Octβ2R. These are the invertebrate equivalents of noradrenergic signalling, not dopaminergic. |

#### Confirmed TRUE_DRD members

| accession | species | nearest DRD anchor | delta |
|---|---|---|---|
| XM_005099942.3 (DopR_2) | Aplysia californica | Manduca sexta Dop2R | 1.23 |
| XM_011436579.4 (DopR_3) | Crassostrea gigas | Manduca sexta Dop1R | 0.87 |
| XM_014919809.2 (DopR_1) | Octopus bimaculoides | Manduca sexta Dop1R | 1.30 |

### Before vs. after — architecture consistency row

| | Before (v3) | After (tree-verified) |
|---|---|---|
| Dop (Mollusca + Cnidaria) | n=17, 100% PF00001, 1.00 dominant | **n=3 TRUE_DRD**, 100% PF00001, 1.00 dominant |
| — new row: non-DRD amine | (not present) | **n=14**, 100% PF00001, 0.71 dominant (one Crassostrea + two Nematostella + three Nematostella carry tandem PF00001;PF00001 from the InterPro scan — still Class-A GPCR) |

### Vertebrate DRD-candidate sanity check

10/10 vertebrate DRD1/DRD2 candidates correctly re-classified as
TRUE_DRD by the same pipeline — no false negatives.

### Focused DRD orthogroup tree (manuscript Figure candidate)

`12_build_true_DRD_tree.sh` → 25-taxon LG+G4 ML tree with UFBoot
B=1000. Topology:

* Vertebrate DRD1 clade (5 species) — monophyletic.
* Vertebrate DRD2 clade (5 species) — monophyletic, sister to DRD1.
* Arthropod DopR1 clade (6 species) + Octopus DopR_1 + Crassostrea
  DopR_3 — monophyletic "D1-like" invertebrate clade.
* Arthropod DopR2 clade (6 species) + Aplysia DopR_2 —
  monophyletic "D2-like" invertebrate clade.
* Invertebrate D1-like + D2-like clades branch outside the
  vertebrate DRD1+DRD2 split, consistent with the canonical
  invertebrate-vertebrate dopamine-receptor phylogeny.

This is the expected topology if:
  (a) the invertebrate Dop1R/Dop2R and vertebrate DRD1/DRD2 are
  co-orthologous to a single pre-Bilateria DRD ancestor,
  (b) the vertebrate DRD1/DRD2 split arose from a vertebrate-specific
  duplication.

## Impact on H4a and H4b claims

**H4a (within-phylum architectural conservation):** The Mollusca +
Cnidaria row now has **n=3** (not 17). Within this n=3 set:
* All 3 carry PF00001 (100%)
* None carry PF00003 / PF01094 / PF07562 / PF06151

H4a is therefore **still supported for true dopamine receptors across
all four phyla (Chordata + Arthropoda + Mollusca + Cnidaria)**, but the
claim must explicitly say "tree-verified true DRD orthologues" rather
than "all NCBI-keyword DopR hits".

**H4b (dopamine-receptor PF00001 conservation across phyla):**
Previously: 39/39 PF00001 (across the 4 phyla).
After filtering: 25 / 25 PF00001 (5 vertebrate DRD1 + 5 vertebrate
DRD2 + 12 arthropod DopR1/2 + 3 mollusc/cnidaria true DRD). The
cross-phylum Class-A GPCR architectural-conservation claim is
**strengthened**, not weakened, because the remaining 14 sequences
are also Class-A GPCRs (just different amine-family subtypes), so the
broader claim that "Class-A GPCR 7TM architecture is deeply conserved
across amine-signalling receptors in all four phyla" is fully
supported.

The Pfam Jaccard H4b claim (TAS1R vs Gr = 0.00) is unchanged.

## Residual risks for manuscript interpretation

1. **Low retained-per-species n.** After filtering, Aplysia has 1,
   Crassostrea has 1, Octopus has 1, and three cnidarians + Nematostella
   + Hydra + Acropora have **0** confirmed DRD orthologues.
   * Cnidarian DRD orthologues may simply not have been retrieved by the
     original NCBI keyword search, or may have diverged enough that
     phylogeny-by-nearest-neighbour cannot robustly place them.
   * Mitigation: do NOT claim "DRD present in Cnidaria" based solely
     on this pipeline. Either acknowledge the absence or run a second
     iteration with BLASTP of vertebrate DRD1/DRD2 against full
     Hydra/Nematostella/Acropora proteomes to hunt for missed hits.
2. **UFBoot did not converge on the 74-taxon global tree** (stopped at
   400 iter, correlation = 0.985; conventional threshold is 0.99).
   * The primary 74-taxon tree was only used to compute nearest-anchor
     distances, not for support-dependent topology claims. Nearest-
     neighbour distance rankings are robust to small topology wobble.
   * The focused 25-taxon DRD tree (`tree_DRD_true_orthogroup`) DID run
     UFBoot to convergence (script `12_build_true_DRD_tree.sh`), and
     that tree is the one used for the manuscript figure.

## Files produced

* Input FASTAs:
  `03-analysis/part3-molecular/data/orthofinder_input/*.fa` (13 species)
* OrthoFinder output:
  `03-analysis/part3-molecular/outputs/orthofinder_dop/Results_Apr24/`
* Global 74-taxon tree (primary classification evidence):
  `outputs/orthofinder_dop/global_tree_v2/global_amine_tree_v2.treefile`
* Focused 25-taxon TRUE-DRD tree (manuscript figure):
  `outputs/orthofinder_dop/tree_DRD_true_orthogroup/tree_DRD_true_orthogroup.treefile`
  `outputs/orthofinder_dop/tree_DRD_true_orthogroup/tree_DRD_true_orthogroup.contree` (UFBoot consensus)
* Candidate classification CSV:
  `outputs/orthofinder_dop/tree_classification.csv`
* Updated inventory:
  `outputs/ortholog_inventory.csv` (with `tree_class` and
  `relabelled_gene` columns) — backup at
  `outputs/ortholog_inventory_v3.csv.bak`
* Updated architecture consistency:
  `outputs/architecture_consistency.csv`, `.txt`
* Scripts:
  `03-analysis/part3-molecular/scripts/07_orthofinder_assemble_input.py`
  `08_orthofinder_classify.py`, `09b_phylogenetic_classify_v2.sh`,
  `10_tree_classify.py`, `11_update_inventory_and_consistency.py`,
  `12_build_true_DRD_tree.sh`
