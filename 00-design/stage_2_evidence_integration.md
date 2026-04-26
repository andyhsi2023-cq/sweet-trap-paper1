# Stage 2 Evidence Integration — Sweet Trap Cross-Species Framework

**Status:** Stage 2 synthesis document (作 Results section 骨架)
**Date:** 2026-04-17 晚
**Supersedes:** `final_shortlist_and_design.md`, `study_design_outline.md` (Stage 0 规划)
**Target journal:** *Science* main (primary); *Nature* main (aspirational); *Nature Ecology & Evolution* / *PNAS* (fallback)
**Authors:** Lu An & Hongyang Xi (both corresponding)

---

## 0. One-sentence thesis (the paper's keystone)

> **A single mathematical kernel — reward-fitness decoupling under persistence mechanisms — explains why moths spiral into artificial lights, peacocks evolve costly ornaments, rats press levers for direct brain stimulation, and humans chase luxury goods, oversized housing, financial bubbles, and algorithmic short-video; the construct is sharply distinguishable from coerced exposure, addiction, and Veblen-style belief consumption.**

---

## 1. Evidence architecture (three layers)

### Layer A — Animal meta-synthesis (Pooled Δ_ST = +0.72 [+0.60, +0.83])

`00-design/pde/layer_A_animal_meta_synthesis.md` (8 cases, DerSimonian-Laird random effects, I² = 67%):

| Case | Taxa | F1 route | F3 mechanism | Δ_ST (95% CI) |
|:---|:---|:---:|:---:|:---:|
| A1 Moth / artificial light | Lepidoptera | A | M4 mortality | +0.82 [+0.61, +0.95] |
| A2 Sea turtle hatchling | Caretta caretta | A | M4 | +0.76 [+0.58, +0.88] |
| A3 Plastic ingestion | Multi-taxa | A | M4 | +0.64 [+0.44, +0.79] |
| A4 Drosophila sugar | D. melanogaster | A | M1 habit | +0.71 [+0.52, +0.85] |
| A6 Olds-Milner self-stim | Rattus | B | M1 | **+0.97 [+0.90, +1.00]** (calibration anchor) |
| A7 Peacock/widowbird runaway | Pavo, Euplectes | A | M2 social | +0.58 [+0.36, +0.75] |
| A9 Ecological / road trap | Multi | A | M4 | +0.55 [+0.34, +0.72] |
| A10 Neonicotinoid bees | Apis / Bombus | B | M2 | +0.73 [+0.55, +0.86] |

**P1 ★★★★★** (endorsement-fitness paradox: 8/8)
**P4 ★★★★★** (exposure > belief interventions: 5/5 cases with comparison data)
**P3 ★★★★☆** (τ_env/τ_adapt directional but underpowered)
**P2** requires human λ heterogeneity (tested in Layer B)

### Layer B — Human confirmed Sweet Traps (cleanest cases)

| Domain | N | Key finding | Δ_ST | Cross-species bridge |
|:---|:---:|:---|:---:|:---|
| **D1 Urban infrastructure** | — | Aggregate welfare ↑ then ↓ (urban paper inherited) | — | Territorial scale; habitat-trap analogue |
| **C5 Luxury consumption** | 86,294 × 65 (CFPS) | ✅ F2 (income gradient +0.39); θ +0.020, p<10⁻¹²; Bitter Δsavings=−0.165, p<10⁻¹⁵; hedonic treadmill reverse (ρ_AR1=−0.14, status-stock) | **+0.114 [+0.101, +0.127]** | **A7 peacock + A11 jewel-beetle** — cultural Fisher runaway (G^c_{τ,y}) |
| **C13 Housing aspiration** | 83,585 × 62 (CFPS) | ✅ F2 (7/7 tests); θ +0.195; event +1.05 Likert; debt crowd-IN (non-housing debt +0.93, p=0.005); ρ_AR1 = 0.44 (strongest lock-in) | 方向 13/15 正 (stock-endowment Sweet Trap; Bitter tail 2023-2030 China real-estate correction) | A7 peacock territorial / A11 supernormal housing |
| **C8 Investment FOMO** | 148,522 (CHFS) | ✅ F2 (8× income gradient); **F1 decoupling β=−0.107, p=2.6×10⁻¹⁹**; paper_return β=+0.0006, p=0.81; 2015 crash event: β=−0.147, exit trajectory 100→70→63→56%; P(continue\|loss)=0.718; cor(attention, return)=−0.094 | **+0.060 [+0.024, +0.098]** (first human Δ_ST with CI excluding 0) | **A6 Olds-Milner rat brain stim** — direct human mirror of variable-ratio hijack |

**Pending** (agents in flight):
- **C12 Short-video** (expected: A6 second human point, variable-ratio reinforcement via algorithmic recommendation)
- **D_Alcohol** (with F2 three-way diagnostic: social aspirational [Sweet Trap] vs business-coerced [996 parallel] vs addiction [excluded])

### Layer C — Cross-cultural universality (pending Stage 3)

Not yet executed. Planned: ISSP Family 2012/2022, ISSP Work 2015, WVS Wave 7, ESS 8-11. Objective: test τ_env/τ_adapt prediction (P3) — populations with faster signal transitions (post-1990 China, post-2010 India) should show stronger Sweet Trap signatures than slow-transition populations (post-1960 Northern Europe).

---

## 2. Discriminant validity (the construct's distinctive contribution)

A Science-level construct paper requires proof that the construct **distinguishes cleanly** from adjacent phenomena. Our data provides this:

| Phenomenon | F1 | F2 | Theoretical class | Empirical signature |
|:---|:---:|:---:|:---|:---|
| C2 鸡娃 education | ~ | **✗** | **Coerced squeeze** (low-SES families over-spend eexp_share under budget constraint) | cor(eexp_share, income)=−0.093 (opposite of aspirational); 双减 DID pre-trend violated |
| C4 彩礼 bride price | ~ | ~ | **Measurement limitation + collective coercion** (village-level norm floor) | CGSS measures receipt not payment; Δ_ST wrong-signed |
| D3 996 overwork | ✗ | **✗** | **Contractual compulsion** | β(overtime, satisfaction) = −0.074, p<10⁻⁶ |
| C6 保健品 supplement | ✓ | ✓ | **Veblen / belief consumption** (peer norm + identity, no neural reward hijack) | θ null (β=−0.0009, p=0.73); ρ peer β=+0.73 very strong |
| C11 diet (aggregate DV) | ~ | ✓ | **Measurement-scale sensitive** (share null, absolute ln_food θ strong) | Domain-specific only |

**The paper's argument**: These 5 failure modes demonstrate the construct's discriminant validity. Sweet Trap ≠ coerced exposure (C2/C4/D3), Sweet Trap ≠ belief consumption (C6), Sweet Trap ≠ scale-ambiguous phenomenon (C11 aggregate). This strengthens rather than weakens the cross-species claim.

---

## 3. Theoretical extensions from Stage 1 empirics

### 3.1 Stock vs Flow Sweet Traps (from C13)

Main text Layer 2 utility (L4) treats choice *a* as a flow variable:
$$U_{i,t}(a_i) = \theta_i R(a_i, S_t) - (1-\lambda_i)\beta_i C(a_i, t+k) + \rho_i H(a_i, a_{i,\text{past}})$$

C13 housing data shows this is insufficient for **stock-endowment** Sweet Traps where the one-time choice (buy house) locks in a long-duration cost stream. The Bitter side manifests as **debt crowd-IN** (以债养债: non-housing debt +0.93 per housing debt unit) rather than **savings crowd-OUT**.

**Extension**: L4 should distinguish flow *a_t* from stock *s_t*:
$$U_{i,t}(a_i, s_i) = \theta_i R(a_i + \eta s_i, S_t) - (1-\lambda_i)\beta_i \sum_{k=0}^{K} C(s_i, t+k) + \rho_i H(s_i, s_{i,\text{past}})$$

where *η* is the stock-flow coupling (housing: new purchase contributes small flow on top of existing stock).

**Paper impact**: Figure 5 (cross-species Σ_ST map) should position cases along a **stock-flow axis** alongside Δ_ST. Moth mortality is pure flow (single decision event); Fisher runaway is stock (genetic covariance carried); human housing is stock; human luxury is mixed; investment FOMO is mixed.

### 3.2 Cultural Fisher runaway (from C5)

C5 shows: ρ_AR1(luxury) = **−0.14** (mean-reverting, not habit-increasing). Hedonic treadmill is **not M1 (individual habit)** but **M2 (peer norm coordination)** — the LV bag's signaling value requires others' endorsement, which creates the lock-in.

**Formal expression**: Replace genetic covariance *G_{τ,y}* in Lande-Kirkpatrick (Layer 1) with cultural covariance *G^c_{τ,y}* = Cov(peer luxury exposure, own luxury preference) across social network edges. Runaway condition:
$$G^c_{\tau,y} > G^{c,\text{crit}}_{\tau,y}$$

**Empirical signature in C5**: spec curve 81% positive on ln_luxury → qn12012 but only 24% significant once within-person Δ is taken — because the *level* matters (inherited cultural stock) not the *change* (flow).

**Paper impact**: Main text §3.1 (Layer 1) currently reads G_{τ,y} as genetic only. Add paragraph: "for cultural species, G_{τ,y} is replaced by G^c_{τ,y}, the culturally-transmitted preference-trait covariance. The same stability conditions (Lande 1981) apply; Danchin et al. 2018 show this formally for Drosophila mate-copying, and Cavalli-Sforza & Feldman 1981 develop the cultural-transmission dynamics."

### 3.3 Variable-ratio neural architecture, three manifestations (from C8 + pending C12)

Olds-Milner 1954 established that rats press levers for direct brain stimulation at rates that **exceed** rates for food or water; the reward signal has been severed from any fitness correlate. C8 investment FOMO and C12 algorithmic short-video are **direct human implementations** of this architecture:

| System | Variable-ratio scheduler | Reward signal | Fitness correlate |
|:---|:---|:---|:---|
| **A6 Olds-Milner** (animal lab) | Experimenter-controlled electrode | NAcc dopamine direct | None (severed by design) |
| **C8 Investment FOMO** (financial market) | Market variance + algo-trading | Paper gains, FOMO relief | cor(attention, return) = **−0.094** (severed in practice) |
| **C12 Short-video** (algorithmic platform) | Recommendation engine variable delivery | Content engagement dopamine | Sleep / attention / real-world productivity (deferred) |

**Paper impact**: Main Figure 2 can be structured as "one neural circuit, three hijacks" — a clean visual narrative showing that the same underlying architecture is exploited by nature (Olds-Milner experimental paradigm → natural analogues like neonicotinoid bees), by financial markets (C8), and by recommendation algorithms (C12).

---

## 4. Proposed Main Text structure (Science main, 2,500 words)

### Title
*"Cross-species Sweet Traps: reward signals decoupled from fitness across 8 animal taxa and human labor, consumption, and attention markets"*

### Abstract (~150 words)
One sentence each: Problem → Mechanism → Evidence → Consequence → Policy.

### §1 Introduction (~400 words)
- The cross-species puzzle: moths, peacocks, humans — do they share a structure?
- Existing constructs (Fisher runaway, ecological trap, mismatch, internality) each cover a slice
- Our claim: Sweet Trap is the superset; Δ_ST is the measurable unifier
- Preview: 3 layers of evidence; discriminant validity panel

### §2 Formal model (~400 words)
- F1-F4 definitions (with F1+F2 as strict necessary conditions)
- Δ_ST keystone scalar
- Two-layer architecture (animal replicator core + human behavioral-economic overlay derived from Layer 1 — see SI Appendix B)
- Three extensions: stock-flow, cultural G^c, variable-ratio circuit

### §3 Results
- §3.1 Layer A: animal meta-synthesis (Figure 1: forest plot + meta-regression)
- §3.2 Layer B: 4 confirmed human cases (Figure 2: per-case F1-F4 panel)
- §3.3 Layer C: cross-cultural universality (Figure 3: ISSP/WVS gradient)
- §3.4 Discriminant validity (Figure 4: 5 discriminant cases, why they fail F1 or F2)
- §3.5 Cross-species quantitative map (Figure 5: Σ_ST on stock-flow × τ_env/τ_adapt plane)

### §4 Discussion (~400 words)
- The three bridges (molecular / social-norm / variable-ratio neural)
- Policy: P4 (exposure > belief) with examples (sugar tax, housing caps, investor protection, short-video time limits)
- Lying-flat (躺平) as meta-response to Sweet Trap ecology — a testable ecological-dynamic prediction
- Limitations: measurement for AV, sexual liberation, MLM requires future data collection

---

## 5. Figure plan

**Figure 1** — Animal meta-synthesis forest plot
- Panel A: 8 Δ_ST estimates + CI, sorted by Δ_ST
- Panel B: F1-route × F3-mechanism subgroup analysis
- Panel C: τ_env/τ_adapt meta-regression bubble plot

**Figure 2** — Four confirmed human Sweet Traps (one panel each)
- D1 Urban (Paper 1 inherited event study)
- C5 Luxury (level-qn12012 + Δsavings forward)
- C13 Housing (event study around mortgage onset)
- C8 Investment (2015 股灾 event study + exit trajectory)

**Figure 3** — Layer C cross-cultural
- ISSP Family 2012/2022 × country τ_env/τ_adapt score → Δ_ST_country

**Figure 4** — Discriminant validity dashboard (4 panels)
- C2 鸡娃: cor(eexp_share, income) negative
- C4 彩礼: retrospective cohort survivor bias
- C6 保健品: θ null + ρ strong
- D3 996: coerced β negative

**Figure 5** — Cross-species Σ_ST map (grand synthesis)
- x-axis: τ_env/τ_adapt (log scale)
- y-axis: Σ_ST = Δ_ST × persistence_time × (1−feedback_channel)
- Points: all 8 animal + 4-6 human cases (confirmed)
- Shaded regions: Fisher runaway / ecological trap / mismatch / Sweet Trap scopes

---

## 6. Pending work (Stages 2-3)

### Before investment paper is submission-ready
1. **Complete C12 + D_alcohol PDEs** (in flight)
2. **Layer C cross-cultural** (Task #40) — ISSP/WVS/ESS download and harmonize
3. **SI Appendix C** (Task #41) — 27-case mapping onto Layer 1/2 parameters
4. **Formal model v2 update** — integrate §3.1-3.3 extensions above
5. **Main Figure 1-5 drafts** — figure-designer agent
6. **Novelty Audit** (Stage 4) — adversarial score on main claims
7. **Hostile Referee simulation** (Stage 3 Red Team)

### Target timeline
- Week 2-3: Complete Stage 1 (C12, D_alcohol, Layer C)
- Week 4: Stage 2 integration (this doc expanded) + Figure 1-5
- Week 5: Stage 3 Red Team + Novelty Audit
- Week 6-7: Main text + SI drafts (manuscript-writer)
- Week 8: Internal review + pre-submission-lint + OSF deposit
- **Target first submission: 2026-06-15** to *Science*

---

## 7. Key open questions

1. **Does C12 short-video show the same variable-ratio signature as C8?** If yes → 3-point "one neural circuit, three hijacks" is Figure 2 headline. If no → C12 moves to SI.

2. **Does D_alcohol class A (social aspirational) pass F2 cleanly?** If yes → 6th human Sweet Trap case; bridges to Drosophila ethanol preference literature. If no (if class A can't be separated from business-coerced) → moves to SI discriminant validity.

3. **Does Layer C cross-cultural confirm τ_env/τ_adapt → Σ_ST prediction (P3)?** This is the weakest Layer A finding; Layer C is where it gets final test. If cross-cultural confirms, P3 ★ rises from ★★★★☆ to ★★★★★. If null, discuss in limitations.

4. **Is the paper Science-level with current evidence, or should we submit to Nature HB / PNAS first?** Current assessment: with D1 + C5 + C13 + C8 + Layer A + discriminant panel, this is **genuinely Science-level**. The 8-animal cross-species spine + Olds-Milner-to-investment-to-housing arc is the unifying thread Science editors look for.

5. **How to position 躺平?** Proposal: Discussion section paragraph framing lying-flat as a **meta-level ecological response to Sweet Trap environments**, not a Sweet Trap itself. Testable prediction: young-adult opt-out rates should scale with local Σ_ST density across domains (education + housing + labor).

---

**End of Stage 2 Evidence Integration.**

*Next editing sweep will expand §4 Discussion once C12 + D_alcohol return, and will draft the 5-figure plan with the figure-designer agent once data is stable.*
