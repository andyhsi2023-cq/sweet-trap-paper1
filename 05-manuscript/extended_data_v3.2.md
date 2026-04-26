# Extended Data — v3.2 (F7 adoption)

**Date**: 2026-04-18
**Rationale**: Because F5 dissolves the v3.1 §2 Theory section into Introduction narrative, readers lose the tabular synopsis of axioms and theorems. ED Table 1 restores that synopsis in one page without affecting main-text word count. ED Fig 1 is proposed but not required for initial submission; ED Fig 2 describes the pre-registered minimal experimental paradigm for future P1 confirmatory test (Appendix G in v3.1).

This file describes 1 ED Table (committed) + 2 ED Figures (optional; ED Fig 1 strongly recommended for reviewer accessibility; ED Fig 2 documents future work flagged in Discussion ¶3).

---

## ED Table 1 — Axiom system A1–A4 and theorem set T1–T4 synopsis (committed)

**Panel A — Axioms**

| Axiom | Claim (narrative) | Formal core | Scope / route variations | Falsification criterion |
|---|---|---|---|---|
| **A1 Ancestral Calibration** | Reward evolved because it tracked fitness in the ancestral signal distribution. | ∃ monotone *h*: *U*_perc = *h*(*U*_fit) + *ε* on *S*_anc, *σ*²_cal ≪ Var[*U*_fit]. | Applies to any agent with a reward-evaluation circuit; vertebrates + most invertebrates (dopaminergic RPE documented). | Find a taxon whose *U*_perc ranking contradicts *U*_fit ranking within *S*_anc (no known case). |
| **A2 Environmental Decoupling** | Novel signals outside the ancestral distribution no longer track fitness. | ∃ *t*_sep, *ρ*_crit ∈ (0, 1): *ρ*(*s*, *t*) < *ρ*_crit for *s* ∈ *S*_mod \ *S*_anc. | Route A: mismatch (environment shifts faster than calibration). Route B: supernormal / novel (Olds-Milner, variable ratio, algorithmic feeds). | Identify an *s* ∈ *S*_mod \ *S*_anc with *ρ* ≥ *ρ*_crit across the *ψ_i* distribution. |
| **A3 Endorsement Inertia** (scope-defining) | Within a specified scope, agents continue to endorse signals even when they know better. | A3.0 scope: post-info abandonment < 30% OR revealed *w* < 0.45. Within scope: *b_i* = argmax[(1 − *w_i*)*U*_perc + *w_i* 𝔼[*U*_fit]], *w_i* ≤ *w*_max < ½ (default 0.4). | Agents outside A3.0 scope (e.g., informed professional investors with *w* > 0.45) are **not Sweet Trap cases**; A3 makes no claim about them. This resolves the "any phenomenon fits" tautology concern (Stage 1-B F2). | Information interventions achieving > 70% abandonment in candidate Sweet Trap domains (observed: 5–15%). |
| **A4 Partial Cost Visibility + P1** | Fitness costs are gated by visibility and discounted by a decreasing function of horizon. | Observable cost *c_i*·*I*_visible; effective cost *δ*(*τ*)·*c_i*, *δ*(0) = 1, *δ*′ < 0 (axiomatic core). Default P1: *δ*(*τ*) = 1/(1 + *k_i τ*) hyperbolic. | Core (*δ*′ < 0) is universal; P1 is a parameterization. Exponential or Laibson *β*-*δ* preserve theorem directions with modified constants. | A domain where observed intertemporal cost treatment violates *δ*′ < 0 (no known case). |

**Panel B — Theorems**

| Theorem | Key inequality | Proof technique | Scope where it holds | Anchor |
|---|---|---|---|---|
| **T1 Sweet Trap Stability** | ‖*s_i*(*t*) − *s**‖² ≤ *C*·‖*s_i*(*t*_0) − *s**‖²·e^{−*c*(*t*−*t*_0)}, *c* ≥ *α ℓ ε*² − *β δ*_max *M* − *D*^drift | Jacobian negativity + Lyapunov function + basin Taylor expansion | Persistent Δ_ST ≥ *ε* > 0; bounded cost gradient; A3.0 scope | Allcott 2020 *AER* post-deactivation return; Mozaffarian 2016 *Circulation* |
| **T2 Intervention Asymmetry (core)** | \|Δ*b*_signal\|/\|Δ*b*_info\| ≥ (1 − *w*_max)/*w*_max ≥ 1.5 for *w*_max ≤ 0.4 | Argmax sensitivity on *Ũ_i* = (1−*w*)*U*_perc + *w*·𝔼[*U*_fit]; A3.3 bound on *w* | Dose-matched operational convention (T2.1.1); non-saturated regime *σ*′ ≥ *σ*′_min > 0; symmetric field shrinkage *κ*_signal ≈ *κ*_info | DellaVigna-Linos 2022 *Econometrica*; Mertens et al. 2022 *PNAS* |
| **T3 Cross-Species Universality** | A1–A4 are species-neutral ⟹ Sweet Trap applies to any agent with (i) reward calibration, (ii) signal-space separability via *φ*, (iii) environmental change exposure | Constructive invariance: each axiom's primitives verified species-neutral; moth + human worked examples | Magnitude rank preservation (empirical olds > sensory > fisher) requires additional *ψ*-commensurability premise → reported as empirical regularity, not theorem-derived (Stage 1-B M4) | Layer A (20 animal cases); Layer D (19 MR chains); Olds & Milner 1954 |
| **T4 Engineered Escalation** | Δ_ST^EST ≥ Δ_ST^MST; decay rate *c*^EST ≥ *c*^MST (*basin radius* demoted to Observation 4.1) | Envelope theorem (Milgrom-Segal 2002 *Econometrica*) on the designer's optimisation max_{s_design} Σ_i Δ_ST·ω_j | Designer's objective aligns with Δ_ST; *S*_design strictly larger than passive shift set | C12 short-video (Allcott 2020); gambling (Dow-Schüll 2012); engineered-deception pig-butchering |

**Panel C — Sub-classes**

| Sub-class | Generating mechanism | Empirical domains | Dynamics |
|---|---|---|---|
| **MST (Mismatch)** | Passive environmental shift (no designer); *ψ* calibrated ancestrally | Diet (C11); light pollution (moths); monarch tropical milkweed | Δ_ST fixed by environmental shift; decay rate *c* from T1 |
| **RST (Runaway)** | Culturally-transmitted *ψ* with self-referential covariance | Luxury consumption; dowry; status signalling (Layer C Hofstede patterns) | *W̄*_perc-based Lande–Kirkpatrick dynamics (Lemma L4.1) drive indefinite escalation |
| **EST (Engineered)** | External designer *j* optimises *φ* to maximise Σ_i Δ_ST·ω_j | C12 short-video (algorithmic); Olds–Milner self-stim (lab); slot machines; pig-butchering / PUA | T4: Δ_ST^EST ≥ Δ_ST^MST; *c*^EST ≥ *c*^MST |

---

## ED Fig 1 — Axiom system dependency diagram (recommended, optional for initial submission)

**Purpose**: visually depict (i) the four axioms as nodes, (ii) their dependencies (A4 requires A1 primitives; A3 uses A4 cost-visibility; T1 depends on A1+A2+A3+A4; T2 depends on A3.0 + non-saturation scope; T3 depends on A1–A4 species-neutrality; T4 depends on T1 + envelope), (iii) the three sub-classes MST/RST/EST as downstream nodes.

**Suggested layout**: top row = A1 A2 A3 A4; middle row = T1 T2 T3 T4 with edges to axioms; bottom row = MST RST EST with edges to relevant theorems. Falsification criteria as callout labels.

**Status**: **recommended, not committed**. If reviewers find the narrative-only axiom exposition in Introduction inadequate, this figure would restore the structural view. Can be generated via `04-figures/extended/ed_fig1_axiom_diagram.R` at revision stage; not required for initial submission.

---

## ED Fig 2 — Minimal pre-registered 3-arm factorial experimental paradigm (future work)

**Purpose**: document the minimal RCT design that could refute T2 in a single controlled study under the operational dose-matching convention (T2.1.1).

**Design**: 3-arm between-subjects; *n* = 400 per arm (total 1,200) via Prolific.
- **Arm 1 (Info, dose-calibrated)**: participants receive disclosure information calibrated (in a pre-RCT pilot) to shift 𝔼[*U*_fit ∣ *B*] by Δ*U*.
- **Arm 2 (Signal-redesign, dose-matched)**: participants face a choice environment where *φ* is modified to shift *U*_perc directly by the same Δ*U*.
- **Arm 3 (Control)**: no intervention.

**Primary outcome**: |Δ*b*_signal|/|Δ*b*_info| ratio in the target choice-domain task (e.g., short-video scrolling duration; high-LTV mortgage preference; SSB purchase).

**Pre-registered decision rule**: ratio ≥ 1.5 with 95% lower CL > 1.0 supports T2 prediction P1. Ratio < 1.0 refutes T2 (strong falsification). Ratio in [1.0, 1.5] with CL crossing 1.5 is inconclusive.

**Status**: **flagged future work in Discussion ¶3**. Not required for this submission. OSF-registered protocol at `paper1-theory/04-empirics/minimal_experimental_paradigm.md`.

---

## Items committed for initial submission

| Item | Status | Target location |
|---|---|---|
| ED Table 1 | **committed** | Submission file bundle (2-page PDF) |
| ED Fig 1 | recommended optional | Would supplement ED Table 1; create at revision if requested |
| ED Fig 2 | future-work reference only | Referenced in Discussion ¶3 + Methods §M6 |

**Total ED items at submission**: 1 (well below NHB Article ED ceiling of 10).
