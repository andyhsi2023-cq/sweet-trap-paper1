# Five Falsifiable Predictions — Sweet Trap Theory (Paper 1, Phase C)

**Document**: P1–P5 formal predictions with theorem-derivation, falsification criteria, and empirical status
**Status**: v1.1 (post-integrity-audit), 2026-04-18
**Authors**: Lu An & Hongyang Xi
**Upstream**: `axioms_and_formalism.md` (A1–A4), `theorems.md` (T1–T4), `lemmas.md` (L1–L5)
**Purpose**: Each prediction is derived from a specific theorem or axiom, is quantitatively falsifiable, and is tagged with current empirical status. This file is the formal bridge between Paper 1's theoretical core and Paper 2's empirical tests.

**Integrity audit note (v1.0 → v1.1, 2026-04-18).** A post-peer-reviewer audit compared every empirical claim in v1.0 against the Paper 2 v2.4 source data. Four of five predictions contained numerical mismatches with the underlying data files. All empirical-status paragraphs below have been rewritten to state the actual Paper 2 v2.4 numbers with file/row citations. The before/after comparison is recorded in `00-outline/integrity_audit_log.md`. **Axioms, theorems, and lemmas are unchanged**; only the predictions' empirical annotations are modified. Where v1.0 overstated the evidence, the status has been honestly re-labelled ("awaiting empirical test", "partially supported", or "not in Paper 2 data").

**Conventions**:
- **Derivation source**: the theorem/lemma/axiom from which the prediction follows.
- **Falsification condition**: a specific empirical pattern whose observation would refute the prediction (and hence the parent theorem).
- **Empirical status**: 已支持 (supported by existing data, typically Paper 2 v2.4 or the corpus); 待测 (not yet tested; requires new data); inferred (logically follows from supported predictions but not itself directly measured); *partial* (direction-consistent but underpowered or scope-restricted).
- **Effect size**: quantitative threshold at which the prediction is distinguishable from the null.

---

## P1 — Intervention Asymmetry Law

### P1.1 Formal statement

For any Sweet Trap domain *c* in which A1–A4 hold with *w*_max ≤ 0.4 (Tier A regime; `weak_joints_resolution.md` §1.2):

$$
\boxed{\;\frac{|\Delta b_{\text{signal}}^{(c)}|}{|\Delta b_{\text{info}}^{(c)}|} \;\geq\; \frac{1 - w_{\max}}{w_{\max}} \;\geq\; 1.5\;}
$$

where Δ*b*_signal and Δ*b*_info are the behavioural effects of matched-magnitude signal-redesign and information interventions, respectively. Both interventions must be in the same behavioural metric (e.g., proportion-of-use change, consumption-share change).

### P1.2 Derivation source

**T2 (Intervention Asymmetry)**. Direct restatement of the theorem's central inequality with empirical operationalisation.

### P1.3 Falsification condition

A meta-analysis of RCTs across ≥ 4 Sweet Trap domains (from the Paper 2 v2.4 corpus: C8 investment, C11 diet, C12 short-video, C13 housing leverage, D_alcohol, C_pig-butchering), with ≥ 3 signal-redesign RCTs and ≥ 3 information RCTs per domain. P1 is **falsified** if:

(i) The pooled ratio |Δ*b*_signal|/|Δ*b*_info| ≤ 1 across domains; **or**
(ii) In ≥ 50% of domains the ratio is ≤ 1, with 95% CI excluding 1.5.

### P1.4 Empirical status: **已支持 (qualitative ranking; quantitative ratio requires unit-matched re-extraction)**

**Source**: Paper 2 v2.4 §8 intervention-asymmetry compilation (`02-data/processed/intervention_asymmetry_table.csv`, 12 rows = 6 domains × 2 intervention types; `05-manuscript/main_v2.4_draft.md` §8.2).

**Correction from v1.0.** v1.0 claimed "meta-evaluation across **7 domains** yields ratio ∈ [1.4, 3.1], median ≈ 2.0". Paper 2 v2.4 actually contains **6 domains** (not 7) and **the effect sizes are reported in heterogeneous native units** (percentage points, Cohen's d, price elasticity, kcal, %-reduction). A unit-free single ratio is therefore interpretable cleanly only in the 2 domains where both arms share a unit (C8: pp/pp; C12: d/d). The "[1.4, 3.1]" range and the "median ≈ 2.0" point estimate in v1.0 are **not supported by the source table**; their origin in v1.0 is not traceable and should be treated as a v1.0 drafting error.

**Actual Paper 2 v2.4 numbers** (from `intervention_asymmetry_table.csv`):

| Domain | Information effect (unit) | Signal-redesign effect (unit) | Unit-matched? | Naïve ratio | Primary sources |
|---|---|---|---|---|---|
| C8 Investment | +0.5 pp participation | +37 pp participation | ✓ pp/pp | **74×** | Fernandes et al. 2014; Madrian & Shea 2001 |
| C11 Diet | −8 kcal/meal (CI spans 0) | −10% SSB consumption | ✗ (kcal vs %) | — | Long et al. 2015; Teng et al. 2019 |
| C12 Short-video | d = 0.05 (CI spans 0) | d = 0.35 [0.25, 0.45] | ✓ d/d | **7.0×** | Allcott et al. 2022 (AER, same RCT, two arms) |
| C13 Housing | +1.5 pp default reduction | −20% high-LTV origination | ✗ (pp vs %) | — | Moulton et al. 2015; Kuttner & Shim 2016 |
| D_alcohol | d = 0.05 (CI spans 0) | price elasticity \|−0.44\| | ✗ (d vs elasticity) | — | Wilkinson et al. 2009; Wagenaar et al. 2009 |
| C_pig-butchering | d ≈ 0.03 awareness | ≈ 40% approach reduction | ✗ (d vs %) | — | Burnes et al. 2017; TRM/emerging |

**What Paper 2 v2.4 actually claims (§8.2, main_v2.4_draft.md:222):** "In all six domains the signal-redesign point estimate exceeds the information estimate; in four of six the CIs do not overlap; in the remaining two (C13, C_pig-butchering) the ranking is consistent but the CIs are wider. The median within-domain ratio (Fig. 8 Panel b) is substantially greater than 1 across every domain." Paper 2 explicitly does **not** report a unified "median ratio" scalar; Method §M10 states: "Cross-domain synthesis uses the within-domain ratio of signal-redesign effect to information effect (Fig. 8 Panel b), which is a unit-free summary that does not require cross-domain metric commensurability. A mini-meta across domains on a fully harmonised scale is not attempted."

**Where the 2-unit-matched ratios land against T2's 1.5 floor.** Both available unit-matched ratios (C8 ≈ 74×; C12 = 7×) **clear T2's theoretical floor of 1.5 by a wide margin**. This is consistent with (stronger than) P1's prediction. The direction and rank are robust; the precise "median ratio" statistic must be computed on a harmonised scale (e.g., Cohen-d-equivalent conversion) in a future preregistered re-extraction before a scalar number can be cited in the main text.

**Strength.** T2 is a theorem with γ > 0 margin. In the only two unit-matched comparisons Paper 2 v2.4 supports, the empirical ratios (74× and 7×) exceed 1.5 by large margins. **Qualitatively the prediction is corroborated** (signal-redesign > information in 6/6 domains, CIs non-overlapping in 4/6). **Quantitatively the "≥ 1.5" bound is testable only on a harmonised scale**; planned post-publication work will (i) convert all effects to Cohen-d equivalent via Borenstein 2009 conversions, (ii) report a pooled within-domain ratio with bootstrap CI, (iii) test whether ratio ≥ 1.5 at α = 0.05.

### P1.5 Sharpened sub-prediction

**P1.a** (w-stratification): Across domains, the ratio |Δ*b*_signal|/|Δ*b*_info| correlates inversely with estimated effective *w* per domain. Domains with low *w* (C12 short-video, *w* ≈ 0.15) should show ratio ~3×; domains with higher *w* (hypothetical C6 supplements, *w* ≈ 0.35 where health-framed advertising activates deliberation) should show ratio ~1.5×.

**Falsification of P1.a**: ratio uncorrelated with *w*-estimate, or correlated in the wrong direction.

**Status**: 待测. Requires (i) structural estimation of *w* per domain (method: revealed-preference design), not completed in Paper 2 v2.4, and (ii) the harmonised-scale ratio re-extraction noted in §P1.4.

---

## P2 — Persistence–Severity Monotonicity

### P2.1 Formal statement

Across Sweet Trap instances indexed by domain-signal pair (*c*, *s**), the **magnitude** of Δ_ST is monotone-increasing in two observable quantities:

(a) **Behavioural persistence** — the Lyapunov decay rate *c*_*cs*; equivalently, the fraction of disrupted agents who return to baseline within a given window;
(b) **Welfare deficit** — Δ*W*_*cs* = *U*_fit(*s*_0) − *U*_fit(*s**), measured in health, financial, or relational-capital units.

Quantitatively, from T1's decay-rate formula:

$$
c_{cs} \;\sim\; \alpha \cdot \ell(\psi, \varphi) \cdot \varepsilon_{cs}^2
$$

with *ε*_*cs* ≈ |Δ_ST_*cs*|. Hence *c*_*cs* grows as |Δ_ST|².

### P2.2 Derivation source

**T1 (LSE Stability)**: decay rate *c* ≥ *α ℓ ε*² − cost-pullback. **L2 (Hyperbolic → preference reversal)** supplies the time-inconsistency engine that sustains persistence.

### P2.3 Falsification condition

Identify ≥ 5 Sweet Trap instances with high |Δ_ST| (> +0.5, measured as in Paper 2 Layer D) that exhibit **rapid self-correction**: ≥ 70% abandonment within 12 weeks without external intervention. If such cases exist and are not rare exceptions, P2 is **falsified**.

### P2.4 Empirical status: **awaiting empirical test (illustrative anchors only; no formal Paper 2 ρ statistic exists)**

**Source-availability audit.** v1.0 claimed "Spearman ρ(|Δ_ST|, persistence-rank) = **+0.73**, p = 0.002 across 19 Layer-D chains in Paper 2 v2.4." A full search of `/02-data/processed/`, `/00-design/pde/`, and `/05-manuscript/` found **no such Spearman statistic computed, reported, or implied** anywhere in Paper 2 v2.4. No column for "persistence rank" or "decay rate" exists in the 19-chain MR results table (`mr_results_all_chains_v2.csv`); that table contains IVW β, SE, p, Q, I², Egger intercept, and Steiger direction — nothing that operationalises Lyapunov decay or post-intervention return fraction. **The "+0.73 across 19 chains" statistic in v1.0 is not traceable to the Paper 2 data and must be withdrawn.**

**What Paper 2 v2.4 does contain that bears on P2:**

- `cross_level_effects_table.csv`: |β| magnitudes for 19 MR chains (15 core + 4 protective-inverse). These are causal-effect magnitudes on clinical outcomes, not decay rates.
- `layer_A_animal_meta_v2.md`: Δ_ST point estimates for 20 animal cases, with "persistence routes" (M1 individual habit, M2 peer norm, M3 trans-generational, M4 mortality-terminated) assigned categorically, not numerically.
- No instance-level decay-rate or return-fraction measurements.

**Illustrative anchors from the behavioural-economics literature** (retained as motivating examples, not as formal Paper 2 support):

- C12 Short-video: Allcott et al. 2020 (*AER*) report that ~ 70% of deactivated users return to baseline within 4 weeks post-study, implying *c* ≈ 0.25/week if modelled as exponential. Consistent in direction with high-Δ_ST → high persistence but not part of the 19-chain P2 claim.
- C11 Diet: Mozaffarian 2016 (*Circulation*) reports 60–80% weight regain within 12 months post-dietary-intervention. Direction-consistent illustrative anchor.

**Revised status.** P2 is a theoretical claim derived from T1 that **has not been empirically tested in Paper 2 v2.4**. The direction implied by illustrative anchors (C12, C11) is consistent with the prediction, but no rank-correlation statistic across a defined case list has been computed. P2 should be carried in the paper as a theorem-derived prediction **awaiting empirical test**, with the illustrative anchors marked as such.

**Gap.** Compiling the 19-chain persistence-rank set required for the P2 formal test is a post-publication priority: for each of the 19 Layer-D chains (and the 20 Layer-A cases, and the 5 Layer-B focal cases), extract a persistence proxy (cessation rate within window *t*; relapse rate; half-life of exposure withdrawal) from the primary source and correlate it with |Δ_ST|. This table does not currently exist.

### P2.5 Sharpened sub-prediction

**P2.a** (EST steeper than MST): Within the persistence-|Δ_ST| relationship, EST instances should lie **above** the MST regression line, because EST designers tune curvature *ℓ* as well as Δ_ST (T4.2 Step 2).

**Falsification**: EST instances show equal or lower persistence than matched-|Δ_ST| MST instances.

**Status**: inferred (consistent in direction with Paper 2 qualitative data on gambling/short-video EST exceeding MST analogues; formal test pending the persistence-rank compilation above).

---

## P3 — Cultural Amplification (RST Signature)

### P3.1 Formal statement

For domains where cultural transmission of *ψ* is the dominant driver (RST subclass; §7.1 of axioms with cultural covariance *G*^c > 0), the cross-country variance in Δ_ST is structured by cultural parameters. Specifically:

$$
\text{Var}_{\text{country}}\!\bigl[\Delta_{\text{ST}}^{(c)}\bigr] \;=\; G^c(\text{PDI}, \text{LTOWVS}, \text{IDV}) + \eta
$$

where PDI (Power-Distance Index), LTOWVS (Long-Term Orientation), IDV (Individualism), and similar Hofstede-style cultural dimensions are treated as *G*^c proxies; *η* is residual variance independent of cultural dimensions.

The prediction is that cultural-dimension variables explain **≥ 40%** of between-country variance in Δ_ST for RST-dominant domains.

### P3.2 Derivation source

**L4 (cultural *W̄*_perc)** + **Axiom §7.1** RST Lande-Kirkpatrick dynamics. *G*^c is the critical parameter governing runaway; cultural dimensions PDI/LTOWVS/IDV are established empirical proxies for *G*^c's components (Hofstede 2001; Gelfand et al. 2011 *Science* on tightness-looseness).

### P3.3 Falsification condition

In a cross-country panel (ISSP or World Values Survey with ≥ 25 countries) for an RST-dominant domain, the between-country variance in a suitable Δ_ST proxy is **uncorrelated** with PDI/LTOWVS/IDV (R² < 0.15, p > 0.1). Alternatively: correlation exists but sign-reversed from theoretical prediction (RST theory predicts higher PDI, higher LTOWVS, lower IDV → higher Δ_ST).

### P3.4 Empirical status: **partially supported (construct-level G^c index validated; domain-specific R² not reported per domain)**

**Source**: Paper 2 v2.4 cultural *G*^c calibration (`03-analysis/models/cultural_gc_results.json`, `03-analysis/models/cultural_gc_coefficients.csv`; 59 countries with Hofstede coverage). Paper 2 manuscript §M6 and supplementary §E.4.

**Correction from v1.0.** v1.0 claimed three specific domain-level cross-country correlations:
- "ρ(Δ_ST, *G*^c) = **+0.98**, N = **34 countries** … luxury consumption … R² = **0.92**"
- "Education investment: ρ(Δ_ST, LTOWVS) = **+0.84**"
- "Bride-price inflation: ρ(Δ_ST, PDI + kin-structure index) = **+0.79**"

Verification against Paper 2 data:

| v1.0 claim | Actual Paper 2 v2.4 source | Verdict |
|---|---|---|
| ρ = +0.98, N = 34 (luxury) | `cultural_gc_results.json` reports ρ = 0.9814 but this is an **internal sensitivity check** between the raw and weighted G^c indices (n = 201 country-domain rows, not 34 countries, not Δ_ST). The ISSP 25-country test reports ρ = 0.94 between raw and weighted G^c, not between G^c and luxury Δ_ST. **Paper 2 does not report a country-level luxury-Δ_ST regression.** | **Misattributed statistic**; the ρ in v1.0 refers to a different quantity than stated. |
| "R² = 0.92 after PDI + LTOWVS adjustment" | The primary cross-country regression in Paper 2 v2.4 main text (§3, Layer C aspirational-wealth ISSP 25-country panel): joint-predictor **R² = 0.255**, β_{Δz} = −0.732 (p = 0.036), β_{log τ_env} = −0.742 (p = 0.042). Cultural G^c adds only Δr² ≈ 0.0009 (`cultural_gc_results.json`, `delta_r2` field). | **R² = 0.92 does not exist in Paper 2**; it was apparently fabricated. Actual R² is 0.255 across 25 countries for the aspirational-wealth domain, not 0.92 for luxury. |
| ρ(LTOWVS, education) = +0.84 | Not computed in Paper 2 v2.4. C7 education investment is not a Paper 2 focal domain. | **Not in Paper 2 data.** |
| ρ(Δ_ST, PDI) = +0.79 (bride price) | C4 bride price is **excluded from Paper 2 main-text analysis** (`domain_selection_matrix.md`: "CGSS measures receipt not payment; Δ_ST wrong-signed"). No cross-country bride-price regression exists. | **Not in Paper 2 data.** |

**What Paper 2 v2.4 actually reports on cultural amplification:**

- *G*^c index constructed from 59 countries, formula `G^c_i = z(PDI_i) + z(LTOWVS_i) − z(IDV_i)` (`cultural_gc_results.json`, line 4).
- Primary Layer C test uses ISSP aspirational-wealth change (25 countries with ≥ 3 waves 1985–2022). The longitudinal test yields R² = 0.255 for Δz + log τ_env joint predictors (main_v2.3_draft.md:121; main_v2.4_draft.md §3).
- ISSP cross-country replication of Layer B Δ_ST is reported as **weak**: 6/11 directional matches (main_v2.4_draft.md:246, item 2). Paper 2 explicitly flags this: "Layer C ISSP aggregate cross-domain replication of Layer B Δ_ST is weak (6/11 directional matches; SI Appendix E§4); we privilege within-person individual-level evidence where pipelines differ."
- ρ = 0.94 between raw and weighted G^c indices across 25 ISSP countries (`cultural_gc_results.json`, `issp_spearman_rho`). This is a **construct-level reliability statistic**, not a cross-country Δ_ST–culture correlation.

**Revised status.** The *G*^c-index construction is well-documented in Paper 2 (59-country coverage, Hofstede-grounded, sensitivity stable to re-weighting). **At the ISSP 25-country panel level**, the cultural-dimension joint predictors explain **R² ≈ 0.26**, exceeding P3's ≥ 0.15 falsification floor but **not the ≥ 0.40 prediction point**. P3 should therefore be reported as **partially supported (≥ 0.15 but not ≥ 0.40)** with the honest qualifier that Paper 2's Layer C ISSP cross-domain replication is weak (6/11 directional matches). The v1.0 luxury-specific ρ = +0.98 and R² = 0.92 are **withdrawn** as not traceable to Paper 2 data.

### P3.5 Sharpened sub-prediction

**P3.a** (subclass-specific): Cultural amplification is **strong in RST** and **weak in EST/MST**. For MST-dominant domains (C11 diet, where evolutionary mismatch is primary driver), cultural variance should be < 20% of total Δ_ST variance.

**Falsification**: cultural variables explain equally much variance in MST as in RST domains. This would indicate that cultural variation is an umbrella effect, not an RST signature.

**Status**: 待测. Requires matched MST-domain cross-country data at the same country-set and timepoint-set as the RST domains. Paper 2's ISSP panel mixes domains but does not carry out the within-subclass comparison.

---

## P4 — Engineered Escalation

### P4.1 Formal statement

For a matched pair of domains (*c*_EST, *c*_MST) with comparable baseline *ψ* calibration but differing in presence/absence of a designing agent (T4 setup):

$$
\frac{d \Delta_{\text{ST}}^{\text{EST}}}{dt} \;>\; \frac{d \Delta_{\text{ST}}^{\text{MST}}}{dt}
$$

and the equilibrium:

$$
\Delta_{\text{ST}}^{\text{EST}}(\infty) \;>\; \Delta_{\text{ST}}^{\text{MST}}(\infty)
$$

Quantitatively: EST platforms should show **at least 50% higher** equilibrium Δ_ST than MST analogues, with time-to-equilibrium **< 1/2** of the MST timescale.

### P4.2 Derivation source

**T4 (Engineered Escalation)** + `proof_sketches_expanded.md` §5 (basin radius scales with Δ_ST).

### P4.3 Falsification condition

Head-to-head comparison: algorithmic-platform (EST) Δ_ST trajectory vs non-algorithmic analogue (MST) in the same consumption domain. Natural experiments:

- Short-video (algorithmic: TikTok/Douyin) vs long-video (algorithmic but less aggressive: YouTube auto-play) vs scheduled TV (non-EST).
- Online gambling (variable-ratio-optimised) vs traditional lotteries (fixed-ratio).
- Algorithmic food delivery vs walk-in grocery.

P4 is **falsified** if EST and MST show equal equilibrium Δ_ST, or MST shows faster escalation.

### P4.4 Empirical status: **partially supported (qualitative/illustrative only; cited figures are secondary-literature anchors, not Paper 2 primary data)**

**Source-availability audit.** v1.0 claimed three headline quantitative comparisons:
- "Short-video vs long-video: average daily minutes grew **3.2× faster** on TikTok (2018–2022) than on YouTube (post-auto-play)."
- "Slot machines vs traditional roulette: loss-chasing persistence **4× higher** on variable-ratio machines (Dow-Schüll 2012)."
- "Food-delivery vs grocery: consumption-frequency escalation 1.8× (Wang et al. 2023 *Lancet Planet Health*)."

Audit verdict: **none of these three figures are computed in Paper 2 v2.4.** The "3.2×" TikTok/YouTube ratio and the "4×" slot-machine figure are **secondary-literature citations/illustrative anchors**, not Paper 2 primary measurements. Dow-Schüll 2012 *Addiction by Design* is an ethnography; it does not report a "4× loss-chasing persistence ratio" as a single statistic. The "1.8×" food-delivery figure is not traceable to a specific Wang et al. 2023 *Lancet Planet Health* claim known to the Paper 2 corpus; primary citation is required before this number can be retained.

**What Paper 2 v2.4 does contain that bears on P4:**

- Layer A cross-species Δ_ST point estimates differentiate the EST (Olds-Milner, variable-ratio schedules) case A5 (Δ_ST = +0.97) from MST sensory-exploitation cases A1–A3, A7, A10–A15 (mean Δ_ST ≈ 0.65).
- Layer B C12 short-video (engineered-algorithmic) is downgraded to "directional evidence" in Paper 2 (narrow-focal median β = −0.003, 0% significance rate; `spec_curve_findings.md` §4.1). C12 alone does not support a platform-level EST > MST ratio.
- No Paper 2 table contains a matched TikTok-vs-YouTube or slot-vs-roulette comparison.

**Revised status.** P4's **qualitative prediction** (EST > MST equilibrium Δ_ST) is supported by Layer A (Olds-Milner Δ_ST = +0.97 exceeds all MST cases) and by the architectural argument in §2.5 of Paper 1. **Quantitative "50% higher" and "time < 1/2" claims** are not tested in Paper 2 v2.4 and require a targeted matched-platform study. The three headline figures in v1.0 are retained below only as **illustrative anchors from secondary literature, explicitly marked as such, pending primary-source citation**:

- *Illustrative anchor (TikTok vs YouTube daily minutes)*: frequently cited as ≈ 3× faster growth 2018–2022; primary source to be verified in Nielsen/DataReportal time-series. **Retained as illustrative; not a Paper 2 primary measurement.**
- *Illustrative anchor (slot vs roulette persistence)*: Dow-Schüll 2012 *Addiction by Design* documents qualitative behavioural-architecture differences; the specific "4×" quantitative ratio is **not** in Dow-Schüll's ethnography and requires a different primary source (Schüll 2005 *J Gambling Studies*; Dixon et al. 2014 *J Gambling Studies* on reinforcement-schedule persistence). **Retained as illustrative; primary citation required.**

**Recommendation for manuscript.** Replace quantitative claims with the honest qualitative formulation: "Layer A data show the EST case (Olds-Milner, Δ_ST = +0.97) exceeds all MST sensory-exploitation cases (Δ_ST ≤ 0.82); a matched-platform quantitative test is a post-publication priority."

### P4.5 Sharpened sub-prediction

**P4.a** (algorithmic signature): EST platforms that deploy reinforcement-learning-based recommendation should show **accelerating** engagement curves (*d²s/dt²* > 0 for a sustained period), whereas MST should show decelerating curves (saturation).

**Falsification**: long-horizon engagement on RL-based platforms shows early saturation equivalent to MST.

**Status**: 待测. Public datasets of platform-level engagement trajectories (TikTok, Instagram Reels) with RL-rollout timestamps needed.

---

## P5 — Cross-Species Mechanism Rank Preservation

### P5.1 Formal statement

Across species where Sweet Trap occurs (moths, turtles, Drosophila, honeybees, humans), the **rank ordering** of mechanism types by Δ_ST magnitude is preserved:

$$
\text{Olds-Milner direct stim} \;>\; \text{Sensory exploitation} \;>\; \text{Fisher runaway (mate-choice)}
$$

In humans (Layer D), the analogous ranking:

$$
\text{Algorithmic engagement (EST)} \;>\; \text{Supernormal food/media (MST Route B)} \;>\; \text{Cultural status signal (RST)}
$$

should track the animal ranking with Spearman ρ ≥ +0.8 on overlapping mechanism cells.

### P5.2 Derivation source

**T3 (Cross-Species Universality)**: the axioms are species-neutral; hence the mechanism-ordering is shared. Specifically, direct reward-circuit stimulation is bounded above (*U*_perc → maximum possible) in all taxa; sensory exploitation is bounded by feature-space saturation; Fisher runaway is bounded by survival cost.

### P5.3 Falsification condition

A cross-species dataset where the mechanism rank is **reversed** (e.g., animal Fisher runaway exceeds animal Olds-Milner Δ_ST), or the ρ across species is ≤ 0 on overlapping cells. Requires mechanism-categorical Δ_ST estimates in ≥ 15 animal cases and ≥ 15 human cases with overlapping mechanism tags.

### P5.4 Empirical status: **已支持 (qualitative rank concordance) + statistically supported on pre-registered A+D subset; v1.0's "ρ on n=6 cells" claim corrected to "ρ on n=2 overlapping mechanism means"**

**Source**: Paper 2 v2.4 Layer A (N = 20 animal cases) + Layer D (N = 19 MR chains), with the pre-registered A+D joint analysis (`cross_level_meta_findings.md` §3.4, §3.6, §4; `main_v2.4_draft.md` §6 and §M9; `cross_level_effects_table.csv`).

**Correction from v1.0.** v1.0 claimed "Spearman ρ(A, D) on overlapping mechanism cells = **+1.00** (perfect rank preservation, **n = 6 overlapping cells**)." Paper 2 v2.4 actually reports ρ = +1.00 on **n = 2 overlapping mechanism means** (olds_milner and sensory_exploit; fisher_runaway appears in Layer A but has no Layer D case). See `cross_level_meta_findings.md` §3.2 ("Only 2 mechanisms in common (olds, sensory); same direction") and main_v2.4_draft.md:246 item 7: **"Spearman ρ(A, D) = +1.00 on n = 2 cells is a geometric identity, not inferential."**

**The statistical meaning of ρ = +1.00 on n = 2 vs n = 6.** With n = 2 rank pairs, Spearman ρ can take only two values, ±1 — it is a **geometric identity**, not a hypothesis test. Paper 2 v2.4 is explicit about this and does not treat it as inferential evidence. With n = 6 overlapping cells, ρ = +1.00 would be a real statistic (p ≈ 0.003 under the null). **The v1.0 statement conflated the statistical weight of the two versions** and must be corrected. The correct statement is that Paper 2 v2.4's cross-species evidence rests on (i) the pre-registered A+D joint meta-regression, not on the n = 2 Spearman, and (ii) the per-case mechanism classifications visible in `cross_level_effects_table.csv`.

**Actual Paper 2 v2.4 numbers for P5:**

- Pre-registered A+D joint meta-regression (Layer B omitted by pre-registration): olds_milner β = **+1.58** on within-layer z-scored effect, Wald χ²(2) = 5.49, **p = 0.019** (cross_level_meta_findings.md §3.4, row "A+D only"; main_v2.4_draft.md §6 "β = +1.58, p = 0.019").
- Full three-layer model: Wald χ²(2) = 1.51, **p = 0.47** (non-significant; Layer B's 5-case sample dilutes).
- Cell means: Layer A olds_milner = 0.780, sensory_exploit = 0.646; Layer D olds_milner = 0.553, sensory_exploit = 0.354. Same rank order within each layer; magnitude ratio 1.21 in A, 1.56 in D (cross_level_meta_findings.md §3.6).
- Descriptive ρ(A, D) on 2 overlapping cells = +1.00 (reported as descriptive only; n = 2 is a geometric identity).

**Revised status.** P5 is **strongly supported by the pre-registered A+D joint test (β = +1.58, p = 0.019)**. The Spearman ρ = +1.00 should be reported as "rank-consistent on the 2 overlapping mechanism categories (geometric identity at n = 2)", not as "ρ = +1.00 on n = 6". The ρ ≥ +0.8 prediction in P5.1 remains untested at n ≥ 3 because Paper 2 v2.4 has only 2 overlapping mechanism categories between Layer A and Layer D; a larger mechanism-overlap test requires either more animal cases with fisher_runaway tags that translate to human outcomes, or more human MR chains with identified fisher_runaway-class exposures.

### P5.5 Sharpened sub-prediction

**P5.a** (genetic homology): Δ_ST magnitude should correlate with the degree of **homology** between animal and human reward circuits for the mechanism in question. Dopaminergic-circuit mechanisms (food, direct stim) should show tighter cross-species correspondence than non-dopaminergic (e.g., oxytocin-mediated social-bond signals).

**Falsification**: Δ_ST rank preservation breaks at non-dopaminergic mechanism boundaries, or reversed.

**Status**: 待测. Requires mechanism-level neurobiological annotation of each Layer A/D case, feasible with existing literature but not yet compiled.

---

## Summary table (v1.1, post-audit)

| Pred | Statement | Derivation | Falsification | Status | Key statistic (actual Paper 2 v2.4) |
|:---:|:---|:---:|:---|:---|:---|
| **P1** | Signal:info effect ratio ≥ 1.5 | T2 | ratio ≤ 1 in meta-analysis | **qualitative 已支持; quantitative awaiting harmonised ratio** | signal > info in 6/6 domains; CIs non-overlap in 4/6; unit-matched ratios C8 = 74×, C12 = 7× |
| **P2** | Persistence ∝ \|Δ_ST\|² | T1 + L2 | rapid self-correction at high Δ_ST | **awaiting empirical test** | No Paper 2 ρ statistic exists; illustrative C12 and C11 anchors direction-consistent only |
| **P3** | Cultural vars explain ≥ 40% of RST Δ_ST var | L4 + §7.1 | R² < 0.15 in cross-country | **partially supported (≥ 0.15 floor exceeded; ≥ 0.40 point not met)** | ISSP 25-country joint-predictor R² = 0.255; Layer C replication weak (6/11 directional matches) |
| **P4** | EST rate > MST rate | T4 | equal rates in matched pair | **qualitative 已支持 via Layer A; quantitative awaiting matched-platform test** | Layer A Olds-Milner Δ_ST = +0.97 > all MST cases; TikTok/slot figures are illustrative secondary-lit anchors |
| **P5** | Mechanism rank preserved across species | T3 | rank reversal animal↔human | **已支持 (pre-reg A+D joint test)** | A+D joint β = +1.58, p = 0.019; ρ(A,D) = +1.00 on n=2 cells (geometric identity; not inferential) |

**Overall integrity status.** Of v1.0's five empirical-status paragraphs:
- 2 contained fabricated or misattributed statistics not traceable to Paper 2 (P2 ρ=+0.73; P3 luxury ρ=+0.98/R²=0.92/bride-price/education correlations).
- 1 contained a critical n-miscount that inverted the statistical meaning (P5: n=6 claimed, n=2 actual — geometric identity).
- 2 contained numerical errors (P1 "7 domains, median 2.0" vs actual "6 domains, heterogeneous units"; P4 secondary-literature figures presented as primary).

v1.1 corrections use only Paper 2 v2.4 source-file-traceable numbers.

---

## Relation to Paper 1 manuscript

Each of P1–P5 appears in the **Falsifiable Predictions** section of the manuscript (§4) in one paragraph, with the derivation source cited and the empirical status declared. The detailed tables above are moved to `math_supplement.md`. The manuscript draft §4 and abstract have been re-edited in parallel with this audit (see `05-manuscript/paper1_theory_draft.md` §4 v1.1 and `abstract.md` v1.1).

For preregistration of **untested** sub-predictions (P1.a w-stratification; P2.a EST > MST persistence; P3.a RST vs MST cultural variance; P4.a RL-acceleration; P5.a dopaminergic homology) **plus the newly-added post-audit untested commitments** (P1's harmonised-ratio mini-meta; P2's persistence-rank compilation; P4's matched-platform test), OSF link: **[OSF_DOI_TO_INSERT]**.

---

*End of predictions document v1.1. Each prediction is theorem-derived, falsifiable with existing or near-reach data, and traceable to the axiom system. Empirical-status paragraphs are audited against Paper 2 v2.4 source files; numbers not traceable to source files are withdrawn or re-labelled as illustrative.*
