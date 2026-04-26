# Figure 4 Caption — Positive selection in sweet-receptor gene families (H6a)

**Figure 4. Lineage-specific positive selection in the *Apis mellifera* Gr_sweet
receptor clade, with positive-control replication.**

**(a)** Maximum-likelihood gene family tree of the insect Gr_sweet chemoreceptor
family (38 taxa; IQ-TREE UFBoot; PF06151 domain). Branches leading to the four
*A. mellifera* paralogues are coloured orange; the foreground MRCA used in the
branch-site test is marked with a red star. Orange shading highlights the
foreground clade. Node labels show UFBoot support ≥ 70.

**(b)** Likelihood-ratio test (LRT = 2ΔlnL) landscape across all 21 pre-registered
production rows. Each point represents one branch-site test; point area is
proportional to log(ω_2a + 1). Filled red circles: significant at the
pre-registered Bonferroni α (n = 60 tests, α = 8.33 × 10⁻⁴); filled orange
circles: significant at the realised Bonferroni α (n = 21 tests, α = 2.38 × 10⁻³).
Grey-shaded rows indicate tip-only foregrounds (single-branch, low statistical
power). Rows with ω > 50 are consistent with boundary estimation (ω → ∞ when
class proportion p2a + p2b is small; Anisimova & Yang 2007); these are reported
but not interpreted as primary evidence.

**(c)** Bayes Empirical Bayes (BEB) posterior probabilities for individual codons
under positive selection, shown for the Gr_sweet Gr5a-tip foreground run (53 sites
with P > 0.95; LRT = 12.29, ω = 57.0, BH q = 0.0024). The PF06151 7TM_GR domain
bar (residues 19–450) is shown above the x-axis; predicted transmembrane helix
positions are shown schematically (Robertson & Thomas 2006). Note: the
*amellifera*-clade run (H6a primary test; LRT = 9.92, ω = 36.2) yields 0 BEB
sites with P > 0.95, because selection in that run is detected at the level of
the class proportion parameter rather than concentrated on individual positions;
the Gr5a BEB profile is shown as the richer illustrative contrast within the same
gene family.

**(d)** Positive-control replication of Baldwin et al. (2014). BEB posterior map
for the TAS1R1 Apodiformes (hummingbird) clade foreground run (LRT = 55.9,
p < 10⁻¹⁴, fg ω = 9.38, 6 BEB sites P > 0.95). Domain overlay (dashed
boundaries): ANF_receptor/VFT (residues 76–457; shading marks lobe-2, 250–457),
NCD3G cysteine-rich (492–545), 7tm_3 (562–811). Site numbering follows the TAS1R1
v4 alignment columns. The six BEB-significant sites (357, 651, 557, 337, 826, 90)
match the ligand-binding and inter-subunit interface positions described by Baldwin
et al. (2014), confirming pipeline sensitivity.

*Source data:* `branch_site_results.csv`, `branch_site_beb_sites.csv`,
`positive_control_v4_beb_sites.tsv`, `Gr_family_pilot_tree.nwk`.
*Producer script:* `Fig4_code.py`. *eLife specs:* 180 mm width, 600 dpi, Arial.
