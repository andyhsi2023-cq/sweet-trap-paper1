# 04-figures — Sweet Trap v4 Figure Inventory

Target venue: eLife Reviewed Preprint Publication
Architecture version: v4.1 (2026-04-24)

---

## Figure 1 — Conceptual Framework (COMPLETE)

| File | Format | Purpose | Size |
|------|--------|---------|------|
| `Fig1_conceptual_framework.pdf` | PDF (vector) | Primary submission file | ~112 KB |
| `Fig1_conceptual_framework.png` | PNG, 600 dpi | Screen / supplementary | ~934 KB |
| `Fig1_conceptual_framework.svg` | SVG (editable) | Editorial revisions | ~274 KB |
| `Fig1_caption.md` | Markdown | Caption text (~330 words) | — |
| `Fig1_code.py` | Python 3.14 | **Canonical producer script** | — |
| `Fig1_code.R` | R 4.5.3 | Companion R script (panels B+C) | — |

### Design decisions

**Layout**: 2×2 GridSpec (panels a + b top row; panel c full-width bottom banner)
at 180 mm × 175 mm.

**Panel (a)** — Cross-phyla taxonomy.
Six geometric animal silhouettes (original constructions, no third-party images)
representing Arthropoda, Chordata ×2, Mollusca, Nematoda, Cnidaria.
Positioned in a 2-column × 3-row grid within the top-left quadrant.
Bottom legend: proximate reward → fitness cost arrow + Δ_ST > 0 label.

**Panel (b)** — Axiomatic framework + Δ_ST wedge.
Two overlapping normal distributions: S_anc (grey dashed) vs S_mod (blue solid).
Red shaded wedge area between peak positions = Δ_ST magnitude (symbolic only,
no fabricated numerical values). Right column: A1–A4 axioms in colour-coded tags
(Okabe-Ito: green/orange/blue/pink for A1-A4). Vertical separator line at x=0.715.

**Panel (c)** — Four-part evidence architecture.
Four numbered coloured boxes (blue/green/pink/red = Parts 1–4) with coloured headers,
body text (method families + key pre-registered statistic), linked by black arrows.
Footer note: all predicted statistics pre-registered on OSF.

**Colour palette**: Okabe-Ito (colour-blind safe). Verified legible in greyscale.

**Fonts**: Arial (sans-serif), falling back to DejaVu Sans. Body text ≥ 5.6pt
(≥ 8pt for primary labels), compliant with eLife ≥ 8pt guideline at 180 mm width.

**Compute**: Single-threaded Python (scipy, matplotlib, numpy). Wall time < 30 s.
No external API calls. All icons are programmatic (no Phylopic silhouettes used —
avoided to eliminate CC-BY attribution complexity at submission).

### Iteration plan

This is v1.0 (illustrative/conceptual). Expected revision cycles:

- **After Part 2 data**: Update Panel (a) animal icons to match the 50-case
  systematic-review species list; optionally add Echinodermata icon (currently
  Cnidaria used for 6th slot).
- **After Part 1 results**: Add actual pooled β and MR OR values as numerical
  callouts in Panel (c) Part 1 box.
- **After Part 3 results**: Replace "InterPro Jaccard ≥ 0.70" in Panel (c) Part 3
  with actual observed value.
- **Editorial revision**: May need to split into two separate figures if eLife
  requests simpler individual panels. The SVG format supports easy panel extraction.

### Licensing

All animal icons are original geometric constructions — no Phylopic downloads,
no stock images. No licensing encumbrances. Authors own the figure in its entirety.

---

## Figure 4 — Positive Selection: H6a Branch-Site Results (COMPLETE)

| File | Format | Purpose | Size |
|------|--------|---------|------|
| `Fig4_positive_selection.pdf` | PDF (vector) | Primary submission file | ~109 KB |
| `Fig4_positive_selection.png` | PNG, 600 dpi | Screen / supplementary | ~1.0 MB |
| `Fig4_positive_selection.svg` | SVG (editable) | Editorial revisions | ~361 KB |
| `Fig4_caption.md` | Markdown | Caption text (~200 words) | — |
| `Fig4_code.py` | Python 3.10 | **Canonical producer script** | — |

### Design decisions

**Layout**: 2×2 GridSpec at 180 mm × 185 mm. Panels (a)+(b) top row; (c)+(d) bottom row.

**Panel (a)** — 38-taxon Gr_sweet gene family cladogram (Bio.Phylo rectangular layout).
Apis mellifera clade highlighted in orange with orange background shading; MRCA node
marked with red star annotation showing ω = 36.2, LRT = 9.92, p = 8 × 10⁻⁴ (Bonferroni
significant). Species colour-coded by order (Okabe-Ito). UFBoot ≥ 70 shown.

**Panel (b)** — 21-row LRT landscape scatter plot. Y-axis = ROW_ORDER (TAS1R1 / TAS1R3 /
Gr_sweet grouped; clades before tips). Point area ∝ log(ω + 1); fill codes significance
tier (red = prereg Bonferroni, orange = realised Bonferroni, open = n.s.). Threshold
reference lines at LRT = 5.41 and 8.80. Three rows significant: Gr_sweet__amellifera_clade
(primary H6a), Gr_sweet__Gr5a_tip, TAS1R1__danio_tip_v4.

**Panel (c)** — BEB posterior stem plot for Gr_sweet__Gr5a_tip (53 sites P > 0.95;
1078-column alignment). PF06151 7TM_GR domain bar (residues 19–450); seven TM helix
positions shown as schematic blue rectangles (approximate; explicitly labeled "schematic").
Annotation note explains amellifera_clade 0-BEB-site situation.

**Panel (d)** — Positive-control replication: TAS1R1 Apodiformes (hummingbird) clade
(Baldwin 2014). BEB stems for 6 significant sites (P ≥ 0.95 from BEB column ≥ 0.95
in pc_beb data). Domain overlay: VFT/ANF_receptor (76–457, lobe-2 shaded 250–457),
NCD3G (492–545), 7tm_3 (562–811). Summary annotation box.

**Data sources**: all real, zero fabrication. BEB sites from
`branch_site_beb_sites.csv` and `positive_control_v4_beb_sites.tsv`. LRT values from
`branch_site_results.csv`. Tree from `Gr_family_pilot_tree.nwk`.

**eLife compliance**: 180 mm width, 600 dpi PNG + vector PDF + SVG, Arial font,
Okabe-Ito colour-blind-safe palette.

### Source data provenance
| Panel | Source file | Key statistic |
|-------|-------------|---------------|
| a | Gr_family_pilot_tree.nwk | 38 tips, 6 species |
| b | branch_site_results.csv | 21 production rows; 3 Bonferroni-significant |
| c | branch_site_beb_sites.csv | Gr5a_tip: 53 sites P > 0.95 |
| d | positive_control_v4_beb_sites.tsv | apodiformes_clade: 6 sites P ≥ 0.95 |

---

## Figures 2, 3, 5 (PENDING)

| Figure | Description | Status |
|--------|-------------|--------|
| Fig 2 | Part 1 summary: forest plot (behavioural β) + biomarker dose-response + trans-ancestry MR | Awaiting Part 1 data analysis |
| Fig 3 | Part 2: PRISMA forest + phylogenetic tree with Δ_ST tips | Awaiting systematic review |
| Fig 5 | Part 3: molecular convergence — dN/dS boxplots + InterPro domain grid + pathway matrix | Awaiting molecular analysis |

### Extended Data / Supplementary Figures (PENDING)

- ED Fig 1: PRISMA flow diagram (Part 2 systematic review)
- ED Fig 2: Specification-curve for NHANES domain (SI showcase, ~500 specs)
- ED Fig 3: Within-phylum synteny blocks (Chordata dopamine-receptor cluster)
- ED Fig 4: H3 ancestral-state reconstruction (SIMMAP topology)

---

## Source Data

Source data CSVs (per eLife data policy) will be deposited here as:
`source-data/fig2_source_data.csv`, etc.

Fig 1 is conceptual/illustrative and has no primary source data.

---

*Last updated: 2026-04-25. Figure Designer agent.*
