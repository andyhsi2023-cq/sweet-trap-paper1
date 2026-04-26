# Diff: main_v2.1_draft.md → main_v2.2_draft.md

**Date:** 2026-04-18
**Scope:** Priority actions P2 + P3 + OSF placeholder from Stage 3.5 mini-round.
**Summary (sub-500 words):**

## [DIFF-P2] PUA downgrade (Engineered Deception sub-sub-class refactored)

**Motivation.** Round 2 blind-κ audit (`blind_kappa_round2.md`) produced inter-coder disagreement on PUA's F2 coding: Coder B scored F2 = 1.0 per the canonical v2 construct, Coder A's late refinement scored F2 = 0.5 reflecting trauma-bonded late-phase dependency. Mean S across coders = 5.0 ± 1.0, the largest single-case disagreement in the audit. Red Team v3 mini-round separately flagged the v2.1 claim that "PUA and C12 short-video share the same Olds–Milner variable-ratio schedule" as rhetorical analogy rather than empirical finding.

**Action.**
1. **Main text §11.7 now retains pig-butchering only** as the canonical Engineered-Deception exemplar. Pig-butchering's F1–F4 coding was unanimous between coders (S = 5.5) and its animal homologues (anglerfish, Photuris fireflies, bolas spiders) provide direct aggressive-mimicry precedent.
2. **PUA is retained as SI boundary case** in the new file `SI_11_7b_pua_extended.md`. This SI documents: the F1–F4 assignment (including both coder readings explicitly); the honest discussion of F2 inter-coder disagreement and its construct-boundary implication; and a falsifiable future replication design (within-person cross-operator variable-ratio exposure).
3. **Rhetorical sentence in Discussion Second-implication softened** from direct-equivalence ("PUA and C12 short-video share the same Olds–Milner variable-ratio schedule") to analogical hypothesis with explicit falsifier:
   > "An analogical hypothesis — that PUA's intermittent reinforcement may share operant-conditioning architecture with algorithmically-curated feeds — is consistent with but not directly tested by current data; empirical test requires behavioural experiments contrasting matched variable-ratio schedules under human vs algorithmic operators on a common reward metric (see SI §11.7b and Limitations below)."
4. **Ninth limitation added** explicitly acknowledging the PUA F2 disagreement and SI-boundary-case status.
5. **§7 reliability statement** and **Methods §M12** updated to cite both §11.7 (pig-butchering main text) and SI §11.7b (PUA).

## [DIFF-P3] Word-count audit (no compression required)

**Action.** Section-level wc audit performed (`word_count_audit.md`). Main text measures **4,406 / 4,500 words** (NHB Article ceiling) with ~2% headroom; Methods **2,283 / 4,000 words** (NHB guidance); Abstract **287 / 300 words**. All three sections under their respective limits. Pre-committed compression targets (§6.3 C13 anomaly, §11.7 Methods integration, §8.3 Steiger rationale) are held in reserve for revision rounds but not executed in v2.2.

**v2.1 → v2.2 main-text delta:** +71 words, driven by Discussion (+64, from softened PUA sentence and new 9th limitation) and §7 reliability (+7).

## [DIFF-OSF] OSF DOI placeholder

**Action.** §M12 Transparency section and Data-Availability statement now carry the OSF registration placeholder:

> "Pre-registration: This study's framework document (`sweet_trap_formal_model_v2`) and cross-level pre-analysis plan (`cross_level_plan.md`) were deposited to Open Science Framework on 2026-04-18 and received registration DOI **[OSF_DOI_TO_INSERT]**. All analytical decisions taken after OSF deposit are documented in §11 limitations log with explicit timestamps."

**TODO flag:** Andy must manually obtain the issued OSF DOI and replace `[OSF_DOI_TO_INSERT]` at three locations in v2.2 (version block line 16; §M12 OSF statement; Data Availability statement) before submission.

## Files touched

- `main_v2.2_draft.md` — new, based on v2.1 with all diffs above.
- `abstract_v2.2.md` — new, identical content to v2.1 (abstract does not mention PUA).
- `SI_11_7b_pua_extended.md` — new SI file for PUA boundary-case treatment.
- `word_count_audit.md` — new, P3 measurement report.
- `diff_v2.1_to_v2.2.md` — this file.

## Residual weaknesses (Red Team v3 mini-round)

| # | Issue | v2.2 action | Status |
|---|---|---|---|
| 1 | Main-text length | Measured; under ceiling (4,406 / 4,500). | **Closed** |
| 2 | §11.7 scale cases secondary-source only | Unchanged; limitation statement explicit. | Open (requires primary data collection; post-publication) |
| 3 | Animal-homology cross-kingdom | Unchanged; anglerfish/Photuris/bolas-spider citations retained. | Open (survives audit; not a v2.2 blocker) |
| 4 | PUA rhetorical claim | Downgraded to SI; main-text sentence softened to falsifiable hypothesis. | **Closed** |
| 5 | Pre-reg timestamp | OSF DOI placeholder inserted; Andy TODO to replace after manual deposit. | **Partially closed** (pending DOI) |

No new analyses were run in v2.2. v2.2 is a presentation-level revision only; all statistical results, figures, and table contents are inherited unchanged from v2.1.
