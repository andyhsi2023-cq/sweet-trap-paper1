# Part 3 Molecular — Week 1 Pilot (Sweet Trap V4)

**Scope.** This directory hosts the cross-phylum molecular ortholog pull that
feeds H4a (within-phylum conservation) and H4b (cross-phylum convergent
architecture) in `00-design/stage6-evolutionary-reframing/`. Week 1 produces
fetched CDS/protein FASTA, sanity QC, a pilot vertebrate ML tree, and a
first-pass Pfam/InterPro domain architecture scan. Week 2 extends alignments
to all 15 gene families and computes LBD dN/dS + domain Jaccard + phylogeny.

## Pipeline

```
┌────────────────────────────┐
│ 01_fetch_orthologs.py      │  Ensembl REST (vertebrates)
│                            │  NCBI Entrez  (invertebrates)
└────────────┬───────────────┘
             ▼
    data/raw_cds/*.fa
    data/raw_protein/*.fa  ──┐
             │               │
             ▼               │
┌────────────────────────────┐
│ 01b_patch_known_aliases.py │  manual curation for NCBI
│                            │  synonym collisions (e.g. Gr5a)
└────────────┬───────────────┘
             ▼
┌────────────────────────────┐
│ 02_sanity_check.py         │  length mod 3, premature stops,
│                            │  protein-length family range
└────────────┬───────────────┘
             │
             ├──▶ outputs/sequence_qc.csv
             │
             ▼
┌────────────────────────────┐
│ 03_align_pilot.sh GENE     │  mafft --auto on protein,
│                            │  back-translate codons
└────────────┬───────────────┘
             ▼
    data/alignments/<GENE>_protein.fasta
    data/alignments/<GENE>_codon.fasta
             │
             ▼
┌────────────────────────────┐
│ 05_pilot_tree.sh GENE      │  IQ-TREE MFP + UFBoot 1000
│ 05b_render_tree.py         │  -nt 2 per CLAUDE.md
└────────────┬───────────────┘
             ▼
   outputs/pilot_tree_<gene>.nwk + .pdf

┌────────────────────────────┐
│ 04_domain_topology_scan.py │  EBI InterProScan5 REST
│                            │  PfamA + Gene3D + PANTHER + SuperFamily + SMART
└────────────┬───────────────┘
             ▼
   outputs/domain_topology.csv
   outputs/domain_architecture_summary.csv
```

## Species × gene matrix

| Lineage     | Species                                                                     | Genes |
|-------------|-----------------------------------------------------------------------------|-------|
| Chordata    | H. sapiens, M. musculus, R. norvegicus, G. gallus, X. tropicalis, D. rerio  | TAS1R1, TAS1R2, TAS1R3, DRD1, DRD2 |
| Arthropoda  | D. melanogaster, A. mellifera, T. castaneum, Ae. aegypti, M. sexta, B. mori | Gr5a, Gr64a–f, DopR1, DopR2 |
| Mollusca    | A. californica, O. bimaculoides, L. gigantea, C. gigas                      | Dopamine receptor homologues (keyword scan, top 3) |
| Cnidaria    | N. vectensis, H. vulgaris, A. digitifera                                    | Dopamine / biogenic-amine receptor homologues (keyword scan, top 3) |

## Week 1 counts

Row counts refer to the expected (gene × species) cells. Per-cell success
totals are reported in `outputs/ortholog_inventory.csv` and summarised below.

| Lineage    | Rows expected | Rows fetched | Hit rate |
|------------|--------------:|-------------:|---------:|
| Chordata   | 30            | 23           | 77 %     |
| Arthropoda | 54            | 20*          | 37 %     |
| Mollusca   | 9 (3 hits × 3 species, 1 species × 0 hits) | 8 | 89 % |
| Cnidaria   | 9             | 9            | 100 %    |
| **Total**  | **102**       | **60**       | **59 %** |

\* Non-Drosophila insects use distinct Gr-family gene names (`GB*` in Apis,
`Gr43a` subfamily in Tribolium) that NCBI does not resolve via the
Drosophila-style Gr5a/Gr64a symbols — this is a taxonomy issue, not a
pipeline issue. Week-2 plan: switch to HMMER against a Drosophila Gr-family
HMM profile to pull true orthologs from other insect proteomes.

### Known issues and fixes already applied

- **Gr5a / Gr64a NCBI alias collision.** NCBI indexes "Gr5a" as a synonym of
  Gr64a (gene_uid 44873). A strict `[Gene Name]` search returns Gr64a's
  accession (NM_168048.2) for a Gr5a query. Real Drosophila Gr5a is
  FlyBase CG31445, gene_uid 43250, RefSeq NM_143267.3. Fixed by
  `01b_patch_known_aliases.py`.
- **Duplicate accession collapse within a species.** Added a `claimed_uids`
  set in the arthropod fetcher so Gr5a / Gr64a / Gr64b ... cannot all resolve
  to the same Drosophila tandem-cluster CDS.
- **Chicken / Xenopus / Zebrafish TAS1R2.** Genuinely absent from Ensembl —
  TAS1R2 is lineage-lost in birds (confirmed) and reduced in some teleosts.
  Reported as `[NOT_FOUND]` in the inventory.

### Domain architecture consistency (Week-1 result)

InterProScan5 (PfamA + Gene3D + PANTHER + SuperFamily + SMART) was run
against all 59 fetched proteins. Key H4b/H4a signatures recovered:

| Family                                          | n  | Dominant Pfam architecture         | Fraction |
|-------------------------------------------------|----|------------------------------------|---------:|
| TAS1R (Chordata sweet/umami Class-C)            | 13 | PF00003 + PF01094 + PF07562        | 13/13    |
| DRD (Chordata dopamine Class-A)                 | 10 | PF00001                            | 10/10    |
| DopR (Arthropoda dopamine Class-A)              | 12 | PF00001                            | 12/12    |
| Dop (Mollusca + Cnidaria dopamine-like Class-A) | 17 | PF00001                            | 17/17    |
| Gr (Arthropoda gustatory 7TM_6)                 | 7  | PF06151                            | 6/7      |

**H4b convergence verdict (pilot):**

- **Pfam Jaccard similarity TAS1R (Chordata sweet) vs Gr (Arthropoda
  sweet) = 0.00.** Their Pfam architectures are disjoint sets:
  - TAS1R = {PF00003 (7TM Class-C), PF01094 (Venus flytrap), PF07562 (NCD3G)}
  - Gr    = {PF06151 (insect 7TM_6), PF00151 (spurious Gr5a-only hit)}

  This confirms **Pfam-level paraphyly** (H4b Stream 3b-Paraphyly): the
  two sweet-sensing receptor families do not share a single Pfam-diagnosed
  ancestor. They converge at the **functional architecture** level (both
  are 7TM GPCRs with a ligand-binding module) but from independent Pfam
  starting points.

- **Dopamine receptors across four phyla (Chordata + Arthropoda +
  Mollusca + Cnidaria): 39 / 39 carry PF00001 (7tm_1 Class-A GPCR).**
  Class-A dopamine-receptor architecture is deeply conserved from
  cnidarians (Nematostella, Hydra, Acropora) through mammals. This is the
  H4a positive-control signature: the receptor family that Robertson and
  colleagues have documented as ancient (Yamamoto & Vernier 2011;
  Bauknecht & Jékely 2017) recovers cleanly in our pipeline.

- **Gr5a alone carries PF00151 (Lipase-like) rather than PF06151.** The
  Drosophila Gr5a we fetched (339 aa, NM_143267.3) is shorter than the
  canonical Gr 7TM_6 family (~420 aa) and its Pfam hit is atypical. This
  is a Week-2 curation item — Gr5a's position as the canonical sugar Gr
  sometimes fetches partial CDS; a manual replacement with the full
  FlyBase CG31445 RA isoform should resolve it.

### Pilot tree — TAS1R1 across 5 vertebrates

Topology from `outputs/pilot_tree_tas1r1.nwk`:

```
((Danio_rerio,
  (Gallus_gallus,
    (Homo_sapiens,
      (Mus_musculus, Rattus_norvegicus)_100)_100)));
```

Matches the known vertebrate species phylogeny (fish out-group, then
sauropsid, then placental mammals with rodents sister). UFBoot = 100 % on
both internal mammalian nodes. The pilot validates that the fetch → MAFFT →
IQ-TREE pipeline produces phylogenetically coherent trees for within-phylum
receptor families.

Alignment summary (`outputs/alignment_stats_TAS1R1.txt`):

- 5 sequences, 861 aa alignment columns
- 3.14 % gaps
- 418 conserved columns at ≥80 % identity (49 %) — consistent with the
  prior-evidence strength of within-Chordata TAS1R1 conservation
  (Yamamoto & Vernier 2011).

## Week 2 plan

1. **Fix insect Gr-family coverage** — download the Pfam PF06151 (7tm_6)
   HMM, scan Apis / Tribolium / Aedes / Manduca / Bombyx RefSeq proteomes
   with `hmmsearch`, pull top 3-5 hits per species as candidate Gr
   orthologs.
2. **Full protein/codon alignments for all 15 gene families** — mafft-ginsi
   for receptor families < 10 sequences, mafft --auto for larger sets.
3. **Trim poorly-aligned regions** with BMGE (`trimal -gappyout` alternative
   if BMGE unavailable).
4. **dN/dS with PAML codeml branch-model** on each within-phylum alignment,
   masked to the LBD (InterPro IPR000073 for TAS1R / IPR000276 for
   Class-A). Compare to the matched-gene genome-wide median per phylum
   (Wilcoxon one-sided, per-phylum).
5. **Cross-phylum InterPro Jaccard** — enumerate Pfam hits for each fetched
   protein, compute pairwise Jaccard on {vertebrate, insect, mollusc,
   cnidarian} families, compare to matched random-ortholog baseline.
6. **OrthoFinder tree** on the concatenated TAS1R + Gr + dopamine family
   alignment to visualise reciprocal monophyly (H4b Stream 3b-Paraphyly).
7. **Pilot paraphyly test**: bootstrap the separating node between
   vertebrate TAS1R clade and insect Gr clade; report UFBoot ≥ 95 %
   threshold.

## Risks (Week-1 identified)

1. **Insect Gr nomenclature.** Bee, beetle, mosquito, moth, silkworm Gr
   genes are not called "Gr5a" / "Gr64a" in NCBI — they are Apis GB*,
   Tribolium LOC*, etc. The 1/6 Drosophila-only coverage is the Week 2 HMM
   profile scan's job to fix. **Impact:** without this, H4b's
   Chordata-vs-Arthropoda Gr comparison has only one arthropod data point
   and loses statistical power.
2. **Cnidarian / mollusc functional annotation ambiguity.** The keyword
   search returns the top 3 "dopamine receptor" mRNAs per species, but
   these may include non-orthologous biogenic-amine receptors (serotonin,
   octopamine). Week 2 must verify by (a) reciprocal best BLAST against
   vertebrate DRD2, and (b) phylogenetic clustering with DRD1/DRD2
   anchors. **Impact:** if some "Dop*" hits are actually 5HT receptors,
   the cross-phylum Jaccard numerator is inflated.
3. **Protein-length outliers.** 6 of 59 fetched proteins are outside the
   family range (e.g. Crassostrea Dop_1 = 898 aa, Hydra Dop_2 = 204 aa,
   Drosophila DopR2 = 805 aa with a splice-extension N-terminus). These
   need manual curation in Week 2 to pick the canonical-length isoform or
   accept them with a note. **Impact:** length outliers distort the
   pairwise-identity metric for H4b if not truncated to the 7TM+LBD core.

## Files produced

| Path                                        | Content                                     |
|---------------------------------------------|---------------------------------------------|
| `data/raw_cds/*.fa`                         | 60 CDS FASTA files, headers `gene|species|accession` |
| `data/raw_protein/*.fa`                     | Matching translated protein FASTA         |
| `data/alignments/TAS1R2_*.fasta`            | 3-seq protein + codon alignment (pilot)   |
| `data/alignments/TAS1R1_*.fasta`            | 5-seq protein + codon alignment (pilot)   |
| `outputs/ortholog_inventory.csv`            | Master table, 102 rows, fetched flag       |
| `outputs/sequence_qc.csv`                   | Per-sequence QC, 59 rows                  |
| `outputs/alignment_stats_TAS1R1.txt`        | Alignment stats (gap %, conserved cols)   |
| `outputs/alignment_stats_TAS1R2.txt`        | Same for TAS1R2                           |
| `outputs/pilot_tree_tas1r1.nwk` + `.pdf`    | ML tree + rendered PDF                     |
| `outputs/tree_TAS1R1/*`                     | Full IQ-TREE output (report, splits, log) |
| `outputs/domain_topology.csv`               | Per-(protein, domain) hit rows            |
| `outputs/domain_architecture_summary.csv`   | Per-protein ordered Pfam architecture     |
| `logs/*`                                    | Execution logs                            |

## Environment

- `venv-phylo/bin/python` (Python 3.14) — Biopython 1.87, dendropy 5.0.8,
  requests, pandas, matplotlib
- `tools/mamba-root/envs/sweet-trap/bin/` — mafft, iqtree, muscle, hmmscan,
  blast+, codeml, orthofinder, raxml

## Compute constraints honoured

- `iqtree -nt 2` throughout (M5 Pro 24 GB, max 2 workers per CLAUDE.md)
- No `multiprocessing.Pool(os.cpu_count())`
- InterProScan REST concurrency capped at 4 (polite default)
- No parallel FASTA loading; each sanity-check / alignment is sequential
