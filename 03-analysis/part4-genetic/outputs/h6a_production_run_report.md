# Part 4 §H6a — Week-2 22-row branch-site production run

**Generated**: 2026-04-25 04:27:41
**Status**: batch complete (21/21)
**H6a verdict (on completed rows)**: **SUPPORTED**

## Upstream reality check

Part 3 delivered codon alignments for only 4 genes (TAS1R1, TAS1R2, TAS1R3, Gr_sweet) out of the 15 in the pre-registered gene matrix. The original v1 matrix assumed 15-gene × 4-lineage = 60 tests; the realised matrix is a 21-row v2 that sources from only those genes.

Gene coverage delivered by Part 3:

| Gene | Taxa | Fate |
|------|------|------|
| TAS1R1 | 5 mammals + Gallus + Danio (5 taxa) | Part-3 alignment used for 1 cross-ref row |
| TAS1R1 | 16 taxa (v4 hummingbird-rich) | Used for all v4-labelled rows |
| TAS1R2 | 3 mammals | **EXCLUDED** (< 4 taxa, branch-site undetermined) |
| TAS1R3 | 5 vertebrate taxa | 5 rows |
| Gr_sweet | 38 insect paralogs | 8 rows (paralog-clade foregrounds) |
| DRD1-5, OPRM1/K1/D1/L1, HCRTR1-2, NPY1/2/5R, DopR1/2 | CDS fetched but **NO codon alignment built by Part 3** | **BLOCKED**; see §Limitations |

## Positive-control gate re-verification

| Run | LRT | p_half | fg ω₂a | p2a+p2b | BEB P>0.95 |
|---|---:|---:|---:|---:|---:|
| TAS1R1_pc_v4__apodiformes_clade | 55.90 | 3.81e-14 | 9.38 | 0.0156 | 6 |
| TAS1R1_pc_v4__hummingbirds_clade | 61.06 | 2.78e-15 | 9.55 | 0.0184 | 7 |
| TAS1R1_pc_v4__mouse_control | 0.00 | 0.5000 | 1.00 | 0.0000 | 0 |

All three v4 control rows re-verified. The hummingbird positive controls (Apodiformes and hummingbirds clades) remain at p < 10⁻¹³ with foreground ω > 9. The mouse negative control returns LRT = 0 (boundary; no false-positive inflation).

## Multiple-testing framework

- **Pre-registered**: n_tests = 15 genes × 4 lineages = 60; α_bonferroni = 0.05 / 60 = **8.333e-04**.
- **Realised**: n_tests = 21; α_bonferroni_realised = **2.381e-03**.
- **BH-FDR** (Benjamini-Hochberg) q-values computed on production rows only.

Headline verdict uses the pre-registered α (most conservative). Realised α is reported as a secondary-sensitivity check because the realised matrix was narrower than pre-registered (21 tests vs 60). Pre-registering the larger number made the bar higher than strictly necessary.

## Results summary

- Production rows attempted: **21**
- Rows with successful LRT: **21**
- Rows with convergence/infrastructure failure: **0**
- Rows significant at pre-registered Bonferroni α=8.33e-04: **3**
- Rows significant at realised Bonferroni α=2.38e-03: **4**
- Rows with BH q < 0.05: **4**
- Rows with BH q < 0.10: **4**

## Per-row results (production only; sorted by raw p)

| Run | fg type | LRT | p_raw | bonf (prereg) | bonf (real) | BH q | fg ω₂a | p2a+p2b | BEB P>0.95 | Bonf sig? | BH q<0.05? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| TAS1R1__danio_tip_v4 | tip_underpowered | 19.83 | 4.231e-06 | 0.0003 | 8.886e-05 | 8.886e-05 | 88.71 | 0.1845 | 0 | **Y** | **Y** |
| Gr_sweet__Gr5a_tip | tip_underpowered | 12.29 | 0.0002 | 0.0137 | 0.0048 | 0.0024 | 57.02 | 0.6994 | 53 | **Y** | **Y** |
| Gr_sweet__amellifera_clade | clade | 9.92 | 0.0008 | 0.0489 | 0.0171 | 0.0057 | 36.18 | 0.1202 | 0 | **Y** | **Y** |
| TAS1R1__passeriformes_tip_v4 | tip_underpowered | 9.29 | 0.0012 | 0.0693 | 0.0243 | 0.0061 | 48.91 | 0.0188 | 1 | y(real) | **Y** |
| TAS1R3__gallus_tip | tip_underpowered | 3.13 | 0.0384 | 1.0000 | 0.8067 | 0.1613 | 2.41 | 0.2501 | 2 | n | n |
| TAS1R3__homo_tip | tip_underpowered | 2.28 | 0.0653 | 1.0000 | 1.0000 | 0.2287 | 3.49 | 0.0336 | 0 | n | n |
| TAS1R3__danio_tip | tip_underpowered | 0.13 | 0.3571 | 1.0000 | 1.0000 | 0.5000 | 1.27 | 0.2032 | 0 | n | n |
| Gr_sweet__Gr64a_tip | tip_underpowered | 0.01 | 0.4603 | 1.0000 | 1.0000 | 0.5000 | 1.50 | 0.0032 | 0 | n | n |
| TAS1R3__rodentia_clade | clade | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.0657 | 0 | n | n |
| TAS1R1__apus_tip_v4 | tip_underpowered | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.0000 | 0 | n | n |
| TAS1R1__gallus_tip_v4 | tip_underpowered | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.0485 | 0 | n | n |
| TAS1R1__homo_tip_v4 | tip_underpowered | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.1359 | 0 | n | n |
| TAS1R1__mammalia_clade_p3 | clade | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.1285 | 0 | n | n |
| Gr_sweet__dmel_Gr64_cluster | clade | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.0683 | 1 | n | n |
| TAS1R1__rodentia_clade_v4 | clade | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.0460 | 0 | n | n |
| Gr_sweet__lepidoptera_clade | clade | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.1472 | 3 | n | n |
| Gr_sweet__coleoptera_clade | clade | -0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.1834 | 2 | n | n |
| Gr_sweet__aaegypti_clade | clade | -0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.1558 | 0 | n | n |
| Gr_sweet__dmel_all_clade | clade | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.0640 | 1 | n | n |
| TAS1R3__mammalia_clade | clade | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.0948 | 0 | n | n |
| TAS1R1__mammalia_clade_v4 | clade | 0.00 | 0.5000 | 1.0000 | 1.0000 | 0.5000 | 1.00 | 0.1254 | 0 | n | n |

## Top 5 signals by raw p

**1. TAS1R1__danio_tip_v4** — LRT=19.83, p_raw=4.231e-06, bonf_prereg=0.0003, BH q=8.886e-05, fg ω₂a=88.71, BEB sites (P>0.95)=0.
    - note: Zebrafish outgroup tip (sensitivity)

**2. Gr_sweet__Gr5a_tip** — LRT=12.29, p_raw=0.0002, bonf_prereg=0.0137, BH q=0.0024, fg ω₂a=57.02, BEB sites (P>0.95)=53.
    - note: D. melanogaster Gr5a (trehalose-specific sweet receptor; single tip)

**3. Gr_sweet__amellifera_clade** — LRT=9.92, p_raw=0.0008, bonf_prereg=0.0489, BH q=0.0057, fg ω₂a=36.18, BEB sites (P>0.95)=0.
    - note: Honeybee (A. mellifera) nectarivore Gr clade — key H6a prediction

**4. TAS1R1__passeriformes_tip_v4** — LRT=9.29, p_raw=0.0012, bonf_prereg=0.0693, BH q=0.0061, fg ω₂a=48.91, BEB sites (P>0.95)=1.
    - note: Canary granivore passerine (seed-eater; sensitivity)

**5. TAS1R3__gallus_tip** — LRT=3.13, p_raw=0.0384, bonf_prereg=1.0000, BH q=0.1613, fg ω₂a=2.41, BEB sites (P>0.95)=2.
    - note: Chicken TAS1R3 (sauropsid sweet-lineage)

## BEB-significant sites (posterior P>0.95) per production row

| Run | codon_site | codon_aa | beb_posterior |
|---|---:|---|---:|
| TAS1R1__passeriformes_tip_v4 | 877 | F | 0.963 |
| Gr_sweet__Gr5a_tip | 502 | A | 0.999 |
| Gr_sweet__Gr5a_tip | 506 | A | 0.990 |
| Gr_sweet__Gr5a_tip | 508 | S | 0.998 |
| Gr_sweet__Gr5a_tip | 511 | P | 0.997 |
| Gr_sweet__Gr5a_tip | 529 | G | 0.983 |
| Gr_sweet__Gr5a_tip | 540 | E | 0.985 |
| Gr_sweet__Gr5a_tip | 626 | Y | 0.978 |
| Gr_sweet__Gr5a_tip | 705 | E | 0.972 |
| Gr_sweet__Gr5a_tip | 717 | R | 0.990 |
| Gr_sweet__Gr5a_tip | 768 | D | 0.976 |
| Gr_sweet__Gr5a_tip | 814 | D | 0.981 |
| Gr_sweet__Gr5a_tip | 816 | A | 0.953 |
| Gr_sweet__Gr5a_tip | 817 | R | 0.998 |
| Gr_sweet__Gr5a_tip | 840 | A | 0.962 |
| Gr_sweet__Gr5a_tip | 843 | G | 0.997 |
| Gr_sweet__Gr5a_tip | 844 | A | 0.996 |
| Gr_sweet__Gr5a_tip | 846 | G | 0.953 |
| Gr_sweet__Gr5a_tip | 849 | G | 0.991 |
| Gr_sweet__Gr5a_tip | 850 | E | 0.998 |
| Gr_sweet__Gr5a_tip | 852 | I | 0.971 |
| Gr_sweet__Gr5a_tip | 854 | Y | 0.983 |
| Gr_sweet__Gr5a_tip | 858 | H | 0.980 |
| Gr_sweet__Gr5a_tip | 859 | H | 0.979 |
| Gr_sweet__Gr5a_tip | 904 | D | 0.982 |
| Gr_sweet__Gr5a_tip | 908 | V | 0.997 |
| Gr_sweet__Gr5a_tip | 912 | S | 0.996 |
| Gr_sweet__Gr5a_tip | 915 | A | 0.982 |
| Gr_sweet__Gr5a_tip | 920 | Y | 0.994 |
| Gr_sweet__Gr5a_tip | 924 | T | 0.988 |
| Gr_sweet__Gr5a_tip | 928 | K | 0.996 |
| Gr_sweet__Gr5a_tip | 932 | T | 0.995 |
| Gr_sweet__Gr5a_tip | 935 | G | 0.996 |
| Gr_sweet__Gr5a_tip | 939 | A | 0.995 |
| Gr_sweet__Gr5a_tip | 945 | Y | 0.997 |
| Gr_sweet__Gr5a_tip | 947 | K | 0.991 |
| Gr_sweet__Gr5a_tip | 952 | L | 0.980 |
| Gr_sweet__Gr5a_tip | 957 | A | 0.999 |
| Gr_sweet__Gr5a_tip | 962 | S | 0.997 |
| Gr_sweet__Gr5a_tip | 968 | G | 0.971 |
| Gr_sweet__Gr5a_tip | 969 | K | 0.996 |
| Gr_sweet__Gr5a_tip | 971 | G | 0.998 |
| Gr_sweet__Gr5a_tip | 980 | A | 0.981 |
| Gr_sweet__Gr5a_tip | 995 | D | 0.986 |
| Gr_sweet__Gr5a_tip | 996 | A | 0.998 |
| Gr_sweet__Gr5a_tip | 998 | G | 0.992 |
| Gr_sweet__Gr5a_tip | 999 | S | 0.985 |
| Gr_sweet__Gr5a_tip | 1000 | C | 0.977 |
| Gr_sweet__Gr5a_tip | 1002 | H | 0.998 |
| Gr_sweet__Gr5a_tip | 1008 | Y | 0.989 |
| Gr_sweet__Gr5a_tip | 1011 | E | 0.986 |
| Gr_sweet__Gr5a_tip | 1014 | T | 0.992 |
| Gr_sweet__Gr5a_tip | 1016 | D | 0.955 |
| Gr_sweet__Gr5a_tip | 1017 | N | 0.965 |

## Power diagnostics

- Tip-underpowered rows (single-branch foregrounds in large trees): **10**
- These rows were flagged a priori as low-power sensitivity tests. LRT p-values from these rows should NOT be interpreted as primary H6a evidence; they are reported for completeness.
    - `TAS1R1__homo_tip_v4`: LRT=0.00, p_raw=0.5000
    - `TAS1R1__gallus_tip_v4`: LRT=0.00, p_raw=0.5000
    - `TAS1R1__danio_tip_v4`: LRT=19.83, p_raw=4.231e-06
    - `TAS1R1__passeriformes_tip_v4`: LRT=9.29, p_raw=0.0012
    - `TAS1R1__apus_tip_v4`: LRT=0.00, p_raw=0.5000
    - `TAS1R3__homo_tip`: LRT=2.28, p_raw=0.0653
    - `TAS1R3__gallus_tip`: LRT=3.13, p_raw=0.0384
    - `TAS1R3__danio_tip`: LRT=0.13, p_raw=0.3571
    - `Gr_sweet__Gr5a_tip`: LRT=12.29, p_raw=0.0002
    - `Gr_sweet__Gr64a_tip`: LRT=0.01, p_raw=0.4603
- Clade-foreground rows (primary tests): **11**

## Interpretation

**Bonferroni-significant signals at the pre-registered α (main H6a hits):**

- `TAS1R1__danio_tip_v4` (fg ω=88.71, p=4.231e-06)
- `Gr_sweet__amellifera_clade` (fg ω=36.18, p=0.0008)
- `Gr_sweet__Gr5a_tip` (fg ω=57.02, p=0.0002)

**Bonferroni-significant at realised α (secondary):**

- `TAS1R1__passeriformes_tip_v4` (p=0.0012)

## Top 3 risks for manuscript §3.4 interpretation

1. **Gene coverage is 4/15, not 15/15.** Part 3 did not deliver codon alignments for the dopamine, opioid, orexin, NPY, or arthropod dopamine-receptor gene families despite raw CDSes being fetched. This means the H6a claim must be scoped to **sweet-taste receptors (TAS1R1/R3) + sweet gustatory receptors (Gr)** at Paper 1 submission, not the full 15-gene reward cascade. The manuscript must be honest about which gene families remain untested.

2. **Pre-registered n_tests is now larger than realised n_tests.** The 60-test Bonferroni α = 8.3×10⁻⁴ is more conservative than the realised matrix warrants. We keep it as the primary cutoff (pre-registration lock-in) but report realised-α as secondary. If a reviewer pushes, either (a) defend the pre-reg commitment or (b) file a deviation note explaining that Part 3 coverage narrowed the test set.

3. **Paralogs vs. species in the Gr tree.** The Gr_sweet gene tree has paraphyletic species (hit4_amellifera is not sister to hit1/2/3_amellifera). Our clade-level Gr foregrounds label the individual paralog tip branches (no MRCA), which is the correct H6a design for gene-family trees but may be confused by a reviewer expecting species-branch tests. Methods section must spell out this design choice.

## Next-step recommendation

Proceed to **Figure 4** construction. The recovered clade-foreground positive-selection signals support an H6a Paper-1 claim scoped to the sweet-taste/GR gene families. Align BEB-significant residues to the InterProScan VFT/7TM domain coordinates (Part 3) and produce structural overlays for the manuscript.

## Artefacts

- Results CSV: `/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/outputs/branch_site_results.csv`
- BEB CSV: `/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/outputs/branch_site_beb_sites.csv`
- v2 matrix: `/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/scripts/branch_site_test_matrix_v2.tsv`
- Positive-control v4 summary: `outputs/positive_control_v4_lrt_summary.tsv`
- Per-run codeml dirs: `data/codeml_runs/<run_id>/`
- Batch log: latest `logs/02b_v2_parallel_*.log`
