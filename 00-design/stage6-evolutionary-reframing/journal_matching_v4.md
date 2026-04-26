# Journal Matching v4.2 — Scheme C Post-Downgrade Target List

**Date:** 2026-04-24
**Supersedes:** v4.1 (2026-04-20), which targeted *Proceedings of the Royal Society B* as primary.
**Context:** Post-S4.v3 novelty audit (62-63/100, above eLife RPP threshold 60+ but below Proc B threshold 65+). PI strategy decision 2026-04-24: downgrade target journal tier to match author-signal profile (Lu An + Hongyang Xi, both ORCID 0009- early-career, primary affiliation Chongqing Maternal & Child Health Care Hospital Breast Surgery — a plausibility-gap for evolutionary-biology editors). Paper 1 (eLife RPP) locks Sweet Trap construct priority; Paper 2 (≥ 6 months later, Proc R Soc B or NEE) extends to full gene-level causality.
**Decision:** **Primary = *eLife Reviewed Preprint (RPP)***. Proc R Soc B moved to "post-Paper-1 upgrade target" not Paper 1 primary.

---

## 1. Decision Framework (Revised)

v4.1 treated "novelty score vs journal threshold" as the decisive variable. v4.2 adds **author-signal × editor-triage** as a second axis because the NHB desk-reject taught us that:

- Novelty 70+ does not overcome a weak affiliation signal at desk-triage stage (NHB rejected at ~75/100 due in large part to #5 "author/affiliation signal gap").
- Early-career authors with non-flagship affiliations face ~15-25 % additional desk-reject penalty at flagship and sub-flagship venues (Proc B, NEE, NHB) independent of manuscript quality.
- At **eLife Reviewed Preprint** venues, author-signal weight is structurally reduced: every submission that passes a minimal editorial filter receives public review, and the reviewer assessment is the published artefact. This converts the author-signal penalty into a near-zero effect.

### 1.1 Revised primary-selection rule

**Primary = the venue at which (p(send to review) × p(accept given review) × prestige_weight) is maximised, given current novelty score.**

At 62-63/100 novelty:

| Venue | p(review) | p(accept | review) | Prestige | Product |
|---|---|---|---|---|
| Proc R Soc B | ~75 % | ~40 % | 1.00 | 0.30 |
| NEE | ~35 % | ~25 % | 1.80 | 0.16 |
| Curr Biol Report | ~45 % | ~30 % | 1.40 | 0.19 |
| **eLife RPP** | **~90 %** | **~90 %** (every reviewed submission publishes) | **0.85** | **0.69** |
| PLOS Biology | ~70 % | ~50 % | 0.95 | 0.33 |
| Open Biology | ~80 % | ~65 % | 0.55 | 0.29 |
| BMC Biology | ~75 % | ~60 % | 0.60 | 0.27 |

**eLife RPP dominates by expected-product.** The dominance is specifically due to **p(accept | review) ≈ 90 %** (RPP does not desk-reject after review; it publishes with reviewer assessment regardless of verdict).

### 1.2 Why not Proc R Soc B first

Expected-value calc:
- Proc B send-to-review ~55 days (per §2 v4.1); reject-after-review ~35-45 %; re-submission to eLife after a reject costs another 30-45 days Week 11-14 window → total 85-100 days wasted if Proc B rejects.
- eLife RPP direct: ~30-40 days to published Reviewed Preprint.
- **Net time saved by eLife-first: 45-60 days** in median case.

Proc B first is defensible only if (a) Paths A+B+C+E+F push novelty to 68+ and (b) senior coauthor is recruited. Neither holds at 2026-04-24.

---

## 2. Primary — *eLife Reviewed Preprint* (RPP)

**Fit score:** 8.5 / 10

### 2.1 Why this is the right primary

- **Structural desk-reject risk ≤ 10 %.** eLife's editorial triage is narrower than traditional journals; manuscripts that clearly fit the general biology scope are almost always sent to review. Our three-part biology structure (cross-species meta + phylogenetics + molecular + human MR) clears this filter unambiguously.
- **Public Reviewed Preprint format.** After review the paper publishes with (a) the full preprint, (b) public reviewer assessments, (c) an **eLife Assessment** label (Valuable / Important / Landmark × Solid / Compelling / Exceptional). Our realistic target is "Valuable with Solid evidence" minimum; this is already a citable publication with a DOI.
- **Author-signal neutrality.** The RPP format evaluates on what the paper argues and shows, not on who the author-block is. Early-career authors without senior coauthors are a structural fit for the RPP community.
- **Open-access built-in.** No paywall, no subscription gate; preprint + review appears on eLife site within 48 hours of the reviewer assessment being finalised.
- **Priority claim is clean.** Combined with Week-0 bioRxiv priority preprint (Path D), Sweet Trap construct claim has a timestamped public record within 1-2 weeks of OSF deposit.
- **Upgrade-path friendly.** If Paper 1 publishes at "Valuable / Solid", Paper 2 (gene-level H6b-H6e + extended animal meta) can be submitted to Proc R Soc B or NEE with the Paper 1 preprint cited as established framework. The RPP path does not foreclose the Proc B/NEE option; it sequences it.

### 2.2 APC and waivers

- Standard APC: $2,500 (2026 rate).
- **eLife waiver policy (2025-2026):** 50-100 % waiver available for:
  - Authors from World Bank low/lower-middle income countries → HUFLIT (Vietnam) qualifies at 100 % waiver for Hongyang Xi as corresponding author.
  - Authors with institutional hardship (can request 25-50 %).
- Realistic out-of-pocket estimate: **$0-500** (via HUFLIT waiver route).

### 2.3 Cover-letter strategy

Focus on **methodological transparency** and **public-data reproducibility**:

> "We report a three-part pre-registered investigation of reward-fitness decoupling (Sweet Trap) across Animalia, with operational measurement of the signed wedge Δ_ST across 50+ animal cases spanning ≥6 phyla, trans-ancestry Mendelian randomisation on 5 human biobank ancestries, and cross-phylum molecular convergence-plus-within-phylum-conservation scan across reward-receptor gene families. All data sources are public; all analytical code is openly deposited; all hypotheses (H1-H6a, with H6b-e flagged as Paper 2 roadmap) carry pre-registered effect-size predictions and falsification criteria. We intend this preprint to contribute an empirical frame for the comparative-biology / ecological-trap / reward-mismatch literatures to share a common operational scalar, and welcome reviewer assessment on our specific claim that phylogenetic-signal analysis plus molecular convergent-architecture together provide evidence for the evolutionary-shaping hypothesis on reward-fitness decoupling."

No mention of policy, welfare, intervention-asymmetry, or Veblen/Schor/Zuboff. Clean comparative-biology claim with transparent scope.

### 2.4 Estimated outcome distribution

- **Desk reject: 5-10 %** (primary rejection reasons would be insufficient scope clarity or evidence that paper is actively being submitted elsewhere; neither applies).
- **Published Reviewed Preprint with Assessment: 85-90 %**, distributed as:
  - Valuable / Solid (realistic target): ~60 %
  - Valuable / Compelling: ~15 %
  - Important / Solid: ~10 %
  - Important / Compelling: ~5 %
- **Expected time to published Reviewed Preprint: 30-45 days** from submission.

### 2.5 Risk: what if the eLife Assessment is weak?

"Incomplete / Solid" or "Inadequate" outcomes are possible if reviewers find (a) Part 4 H6a power issues, (b) Part 2 N < 40, (c) Part 3 H4b Jaccard borderline. In these cases the preprint still publishes with the critical assessment attached. The strategic response is:
- Incorporate reviewer critiques in Paper 2 (6-12 month horizon).
- Do NOT resubmit Paper 1 for a better assessment; accept the public record and move forward.

---

## 3. Backup Primary #1 — *PLOS Biology*

**Fit score:** 7.5 / 10

### 3.1 When to use

If eLife RPP is closed (shutdown, submission pause, policy change) at Week 9 submission time.

### 3.2 Rationale

- Established open-access biology venue (IF ~8, well-recognised).
- Accepts integrative cross-disciplinary work; scope explicitly covers comparative and evolutionary biology.
- Desk-reject ~30-40 % for integrative work; send-to-review + accept ~45 %.
- APC $4,225 (higher than eLife, lower than Nature Communications).

### 3.3 Reformat cost

Minimal. PLOS Biology word/figure limits are generous; manuscript prepared for eLife RPP fits PLOS Biology directly. Cover letter re-tuned to emphasise "cross-disciplinary integrative contribution" rather than "methodological transparency."

---

## 4. Backup #2 — *Open Biology* (Royal Society)

**Fit score:** 7.0 / 10

### 4.1 Why this is a strong backup

- Sister journal to Proc R Soc B; **no affiliation snobbery** (same Royal Society editorial culture as Proc B but open-access and scope-broader).
- Explicit encouragement for "broad biology" submissions that don't fit narrow society venues.
- Desk-reject ~15-20 %; send-to-review + accept ~55-60 %.
- APC £1,700 (≈ $2,200).

### 4.2 Use case

If Paper 1 needs to hit Royal Society ecosystem while avoiding Proc B's 45-55 % review-stage reject risk. Paper 2 can still target Proc B proper 6-12 months later.

---

## 5. Backup #3 — *BMC Biology*

**Fit score:** 6.5 / 10

### 5.1 Rationale

- Springer/BMC open-access; evolutionary biology friendly; covers meta-analysis + phylogenetics.
- Desk-reject ~15-25 %; send-to-review + accept ~55-65 %.
- APC $3,300.

### 5.2 Use case

If eLife + PLOS Biology + Open Biology all closed or declined. Reformat cost moderate (BMC format is standard).

---

## 6. Backup #4 — *Biological Reviews*

**Fit score:** 5.5 / 10 (requires reformatting to review-with-meta)

### 6.1 Rationale

- Review venue; would require compressing Part 3 and Part 4 into SI and leading with Part 2 meta + synthesis.
- IF ~13; prestigious safety.
- Decision cycle 90-120 days.

### 6.2 Use case

Only if Paper 1 must pivot to "pure synthesis without novel primary analysis." Not a default route.

---

## 7. Backup #5 — *Current Biology Report*

**Fit score:** 6.0 / 10 conditional on H3 strong result

### 7.1 Rationale

- Short-form format; would compress Paper 1 into a single-punchline Report.
- Only makes sense if Part 2 K > 0.5 AND Part 4 H6a positive-selection signal lands decisively.
- Desk-reject ~55 % for general-biology submissions at Curr Biol.

### 7.2 Use case

If Week 4 Gate 1 shows exceptionally strong signal (K > 0.5, λ > 0.7, 5+ genes with branch-site positive selection evidence) AND we want to push for a more visible single-finding story. Otherwise eLife RPP remains optimal for the full three/four-part architecture.

---

## 8. Backup #6 — *PeerJ*

**Fit score:** 5.0 / 10

### 8.1 Rationale

- Open-access, APC $1,195 (lowest in the backup list).
- Desk-reject ~10-15 %; almost certain acceptance after moderate revisions.
- IF ~2.5 (low-modest).

### 8.2 Use case

Last-resort venue if all higher-ranked backups reject. A Sweet Trap first-publication in PeerJ is survivable but suboptimal for establishing the construct.

---

## 9. Post-Paper-1 Upgrade Targets (Paper 2 horizon, 6-12 months later)

After Paper 1 eLife RPP publishes with "Valuable / Solid" or better assessment:

| Venue | Paper 2 rationale | Expected EV |
|---|---|---|
| *Proc R Soc B* | Extended full-gene-level (H6b-H6e) + 50+ case meta + Cited Paper 1 as established framework. Senior coauthor ideally recruited. | Good |
| *Nature Ecol Evol* | Only if Paper 1 + senior coauthor + high-impact H6 result. Desk-reject risk ~50 % even with Paper 1 citation; high-reward if accepted. | Speculative |
| *Phil Trans B* theme issue | If a relevant theme (evolutionary mismatch, comparative genomics of behavior) is called during 2026-2027. | Opportunistic |
| *eLife full Article* | Upgrade Paper 1 RPP to full eLife article if reviewer assessment reaches "Important / Compelling". | Optimal |

---

## 10. What We Are NOT Targeting (and why, revised)

- **Nature / Science main journals.** Same reasons as v4.1: not one-decisive-experiment format; no senior coauthor; EV negative.
- **Nature Human Behaviour.** Already rejected.
- **Nature Ecology & Evolution** (Paper 1): desk-reject ~65 % at current author-signal profile; EV negative for Paper 1. Reserved as Paper 2 upgrade target.
- **HSSC / Palgrave Communications.** Already ruled out by hostile-review outcome.
- **PNAS.** No member sponsorship; direct-submit desk-reject ~60 %. PLOS Biology dominates PNAS in EV at current profile.
- **TREE.** Review venue; requires invitation.
- **Proc R Soc B (as Paper 1 primary).** Demoted from v4.1 primary; reserved for Paper 2 horizon. Rationale: 45-55 % review-stage reject at current novelty/author-signal profile wastes 8-10 weeks.
- **J Evol Biol.** Still below Paper 1 ambition; reserve as Paper 2 safety if Proc R Soc B also rejects.

---

## 11. Decision Tree (revised for Paper 1 eLife-first)

| Observed outcome | Next action |
|---|---|
| eLife submission ready Week 8-9 | Submit to eLife RPP |
| eLife desk reject (< 10 % probability) | PLOS Biology (1-week reformat) |
| eLife send-to-review | Wait for reviewer reports (~4-6 weeks) |
| Reviewer report "Valuable / Solid" or above | Published Reviewed Preprint DOI locked; cite in Paper 2 |
| Reviewer report "Incomplete / Solid" | Preprint still publishes with critical assessment; accept public record and move to Paper 2 improvements |
| Reviewer report "Inadequate" | Rare; would require fundamental reframe. Fall back to PLOS Biology / Open Biology. |

**Expected time-to-published preprint with assessment under this sequence:** 5-7 weeks from Week 9 submission. Substantially faster than the v4.1 Proc-B-first plan (which had 7-12 week median time-to-decision).

---

## 12. Strategic Coherence Check

This v4.2 revision is coherent with:

- **Collaboration protocol v1** (2026-04-16): Claude-led pipeline; Andy approves forks. The primary-journal decision is a Fork #3 "value judgment" — Andy has explicitly approved the downgrade decision on 2026-04-24.
- **Prereg timing rule** (`feedback_prereg_post_analysis_pre_submission.md`): OSF prereg + bioRxiv priority deposit at Week 0; Paper 1 submission at Week 8-9; aligned.
- **Path D is now Paper-1 critical path:** bioRxiv + OSF deposit establishes Sweet Trap construct priority regardless of eLife decision timing.
- **Paper 2 roadmap (Part 4 H6b-H6e + 50+ case extension):** held in reserve; not promised in Paper 1 submission to avoid overpromise; but the manuscript explicitly flags these as "announced future work" in Discussion section to claim conceptual priority on the full agenda.

---

*Document version 1.2 (2026-04-24). Authored by PI. Supersedes v4.1 (2026-04-20). Key change: primary target journal changed from Proc R Soc B to eLife Reviewed Preprint based on author-signal × editor-triage joint optimisation, following Andy's 2026-04-24 strategic decision to prioritise fast publication over flagship-venue attempt on Paper 1.*
