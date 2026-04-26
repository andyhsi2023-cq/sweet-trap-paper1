# Pfam Jaccard matched-random null baseline

**Script**: `03-analysis/part3-molecular/scripts/23_pfam_jaccard_null.py`  
**Source**: `outputs/domain_architecture_summary.csv` (51 proteins) and 
`outputs/architecture_consistency.csv` (family-level summary).

## 1. Observed Pfam sets (re-confirmed)

- TAS1R (13 proteins) canonical set: ['PF00003', 'PF01094', 'PF07562']  
- TAS1R full pool (all Pfam hits across 13 proteins): ['PF00003', 'PF01094', 'PF07562']
- Gr (38 proteins) canonical set: ['PF06151']  
- Gr full pool (all Pfam hits across 38 proteins): ['PF00151', 'PF06151', 'PF08395']

- Observed Jaccard (canonical-vs-canonical): **0.000**
- Observed Jaccard (full pool vs full pool): **0.000**

## 2. Null model

Two receptor families draw $k_1=|TAS1R|$ and $k_2=|Gr|$ distinct Pfam 
families independently and uniformly from a universe of size $N$. The 
probability that the two sets are disjoint (Jaccard = 0) is

$$P(J=0\,|\,N,k_1,k_2) = \frac{\binom{N-k_1}{k_2}}{\binom{N}{k_2}}.$$

### 2a. Null #1 — full Pfam-A v37 universe

- $N = 19,632$ Pfam-A families (Pfam v37, Jan 2025 release)
- $k_1 = 3$ (TAS1R), $k_2 = 1$ (Gr)
- **P(Jaccard = 0 | null) = 0.999847**
- Enrichment ratio observed / null ≈ 1.000 (≈1 means: no enrichment vs null)

### 2b. Null #2 — GPCR-Pfam universe (restricted)

A more informative null restricts the universe to Pfam families that 
encode a 7-TM GPCR-type fold (Pfam clans CL0192 7tmA + CL0193 7tmB, plus 
a handful of isolated families; ~20–100 depending on inclusion rule).

| $N$ (GPCR Pfam universe) | P(Jaccard = 0 \| null) |
|---:|---:|
| 20 | 0.8500 |
| 50 | 0.9400 |
| 100 | 0.9700 |

Even under the tightest restriction ($N=20$), P(Jaccard=0) is still 
0.850, i.e. well above any conventional α.

## 3. Honest interpretation

Under **every** reasonable null, Jaccard = 0 between two small Pfam sets 
(k1=3, k2=1) is the expected outcome, not an enriched signal. The 
observed Jaccard = 0 therefore does **not** constitute statistical 
evidence for convergent or divergent molecular architecture.

What the observation *does* establish is a **descriptive-architectural** 
fact: chordate sweet/umami reception (TAS1R) uses a Class-C GPCR with an 
obligate VFT + NCD3G + 7tm_3 module, whereas arthropod sweet/umami 
reception (Gr) uses a Class-unrelated Insect7TM_6 (Trehalose_recp) 
module. These two receptor systems evolved independently, as expected 
from ~600 Myr of lineage separation; they share the *functional role* 
(detect sweet reward) but not the protein scaffold.

## 4. Recommendation to manuscript team

- **Do not** frame this as 'Jaccard = 0 proves independent origin' 
  (that would be a statistical overclaim; the null expects it).
- **Do** frame this as: 'TAS1R and Gr belong to non-homologous GPCR 
  classes (Class-C VFT vs insect 7TM_6). This architectural disjoint 
  is consistent with convergent evolution of sweet detection atop 
  distinct receptor scaffolds but, given the large Pfam universe, 
  disjointness alone is not statistical evidence of convergence 
  (null P(Jaccard=0) ≈ 0.9999 under Pfam-A v37).'
- The *convergence* claim for sweet reception should instead be 
  supported by behavioral / ligand-binding / pathway-output evidence 
  (shared downstream G-protein cascade producing positive valence), 
  not by Pfam set disjointness.

## 5. Numbers for the manuscript

- Observed Jaccard = 0.00
- P(Jaccard = 0 | Pfam-A v37 null) = 0.9998
- Enrichment ratio observed / null ≈ 1.00 (no enrichment)
- Recommendation: report as descriptive-architectural, not as 
  convergence evidence.
