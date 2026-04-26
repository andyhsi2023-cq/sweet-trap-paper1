# Red Team Review: Sweet Trap v4 Paper 1 — C++ FINAL pre-submit audit
**Stage**: S7 (post-Apis-cascade integration, immediately pre-RSOS submission)
**Target journal**: Royal Society Open Science (RSOS)
**Date**: 2026-04-25 (per system clock; manuscript & cascade timestamps 2026-04-26)
**Prior context**: Yes — read `red_team_v4_paper1_C_plus.md` (C+ audit), `optimizer_diagnostic_report.md` (LRT=0 5-clade diagnostic), `apis_optimizer_diagnostic_report.md` (Apis-only diagnostic), full `manuscript.md`, `cover_letter.md`, `rsos_submission_form.md`.

---

## 0. Desk-Reject Probability at RSOS

**Overall desk-reject probability: 8–12%** (down from C+'s 22–28%).

The C++ revision has done the rare thing: it has actually closed the C+ open items rather than papering over them. The Apis cascade is the central event. The C+ audit's single most credible reviewer concern was "the diagnostic was applied asymmetrically — LRT=0 clades only, Apis spared." That asymmetry is now gone: the Apis-only diagnostic was run (5 starts × 1 clade = 5 codeml runs, ~7,040 s wall, per `apis_optimizer_diagnostic_report.md`), the verdict came back APIS_OPTIMIZER_ARTIFACT, and the manuscript propagated the cascade across §3.4, §3.5, §4.1, §4.5, §4.6, Abstract, Title, Table 2, Figure 4, Figure 5, cover letter, and submission form. The §4.5 "Disclosure on H6a vs the pre-registered threshold" paragraph is unusually transparent — it admits the strict pre-registered reading would partially pass H6a but argues the diagnostic-augmented downgrade is more conservative. This kind of self-disclosure is what RSOS editors are trained to reward.

What remains:

1. The "self-defeating overcorrection" risk (~5%) — see Hostile Referee §1.1. The paper now has a Table 2 / Figure 4 / Figure 5 / Abstract that say "0 robust positives across 6 tests." A skim-reading editor will see "0 positives" before they see "the failure mode is insufficient method power, not confirmed absence of selection." If they stop at "0 positives," the desk reaction is "the experiment didn't work." This is mostly a presentation risk rather than a substance one, and §3.5 / §4.5 / §4.8 do contain the right caveats, but the headline number is now harsh enough that an unsympathetic editor could read the paper as "we tried, it failed, we're publishing the null."

2. OSF timestamp / verbatim-prediction verification (~3%). This was the C+ audit's #1 desk-vector and remains live; however, the C++ cover letter and §3.5 / §1 now invite the editor to download the deposit and check against the three predictions verbatim, which inverts the risk. If the OSF zip really contains the three thresholds as claimed, this stops being a vulnerability and becomes a credibility asset. Conditional on Andy's verification that the deposit contains what the manuscript says it contains (per project memory, Andy ran a "bulletproof" verification), this drops below 3%.

3. RSOS structural-soundness checklist (~2%). Abstract length, IRR commitment, deviation-log clarity. All addressed but no audit can be 100% certain how a particular ScholarOne automated checker reads them.

### Top desk-reject candidates (ranked)

1. **"Self-defeating overcorrection" headline impression on a skim read (~5%)** — the harshest open vector remaining. Resolvable by ensuring the abstract Conclusion sentence opens with a positive frame ("widespread *existence*; not *universal*") rather than enumerating four nulls in sequence.
2. **OSF deposit content audit (~3%)** — credibility-positive *if* verified, devastating *if* the editor finds the deposit lacks one of the three predictions.
3. **Lakatosian-rescue accusation by a hostile referee (~2%)** — see Hostile Referee §1.4. The cumulative pattern of (A→C path pivot in row #8) + (Layer-4 softening in row #9) + (Apis cascade in row #9 update) reads as a paper that has been adjusted to its data three times. Each adjustment is individually defensible; the cumulative pattern is what the most skeptical evolutionary-biology referee will surface.

---

## 1. Role 1 — Hostile Referee

### 1.1 The "0 robust positives across 6 tests" headline reads as null-result publishing
**Passages**: Abstract Results (iii) line 44 ("**3/6 optimiser-sensitive [...]; 0/6 robust positives**"); §4.1 line 264 ("**no clade among 6 production tests yields robust positive-selection signal after optimiser-boundary diagnostic**"); Table 2 row for *Apis* with [†] footnote (line 191, 222); Figure 4 caption line 224 ("No robust positive selection across 6 branch-site tests after optimiser-boundary diagnostic"); Figure 5 caption line 257 ("**0/6 robust positives**").

**Why it concerns me**: I count *seven* places in the manuscript where the phrase "0 robust positives" or its near-equivalent appears in a headline position (Abstract, §3.4 first paragraph, §3.5 verdict table row 4, §4.1 first paragraph, §4.5 first paragraph, Figure 4 caption, Figure 5 caption). The text correctly distinguishes "robust positive selection" (high methodological bar, requires diagnostic-stable LRT) from "absence of selection" (a different claim); but a reader who scans only the bold headline phrasings will conclude the experiment found nothing. RSOS publishes nulls — but the journal expects the null to be informative on the question. Here the null is *uninformative on selection presence* (the §4.5 line 286 admits "branch-site Model A on this alignment cannot resolve the universality question") and the manuscript has correctly absorbed Layer 4 into the synthesis as Layer 4 not contributing inference weight (only Layers 2 + 3 carry the "not universal" verdict). But the headline numbers nonetheless read as if the selection layer is the centerpiece. If Layer 4 is uninformative, why is "0/6 robust positives" the most repeated phrase in the paper? This is a **presentation imbalance** that invites the editor to read the paper as "selection failed" when the actual claim is "K + Jaccard refute universality; selection layer is uninformative."

**Counter-citation / precedent**: @rosenthal1979file *Psychological Bulletin* on the file-drawer effect frames null-publication standards as requiring (a) the test was high-powered, (b) the null was pre-registered, (c) the null was informative on the parameter of interest. The paper meets (b) but is honest that it fails (a) and (c) on Layer 4 — yet still platforms Layer 4 as a headline result. The fix is **not** to bury Layer 4 (transparency demands it stays), but to ensure that the synthesis frame leads with what *is* informative (Layers 2 + 3) rather than with what *isn't* (Layer 4).

**Impact on conclusion**: borderline. The conclusion "widespread but not universal" is correct; the framing puts uninformative evidence in headline positions, which is a rhetorical-balance failure that *could* be read as overcorrection.

### 1.2 The §4.5 "Disclosure on H6a vs the pre-registered threshold" paragraph is admirable but also a tell
**Passage**: §4.5 line 290.

**Why it concerns me**: The disclosure paragraph is unusually candid — it states that under the strict pre-registered reading, H6a is partially supported (Apis at $p_\text{Bonf-prereg} = 0.049$ passes), and that the authors elected the diagnostic-augmented downgrade because they judged it "more truthful." This is exactly the kind of transparency RSOS rewards. **But**: a skeptical referee (Maude Baldwin or Joe Thornton type — domain experts who know branch-site behaviour intimately) will read this paragraph and ask: "On what authority did the authors decide that a single $\omega_0 = 5.0$ start producing LRT = $-2.48$ on the Apis clade *invalidates* the production-positive result, when 4 of 5 starts converge to LRT = 9.92 with $\omega = 36.18$?" The Yang & dos Reis 2011 / Anisimova-Yang 2007 literature recommends interrogating LRT = 0 clades for boundary trapping; it does **not** prescribe that an asymmetric escape *to* the boundary in 1 of 5 starts on a positive-LRT clade reclassifies the result. The asymmetric decision rule (APIS_OPTIMIZER_ARTIFACT triggered by "any LRT < 1.0 OR omega_2a near 1.0 (|w-1| < 0.5) OR omega_2a > 200" on any single start) is in `apis_optimizer_diagnostic_report.md` — it is the authors' rule, not a pre-existing methodological convention. The disclosure paragraph admits this asymmetry by saying "**more conservative** than our pre-registration required" — which is honest, but also implicitly concedes that the rule was post-hoc.

**Counter-citation**: @anisimova2007branchsite *Mol Biol Evol* Table 2 documents that for $n \le 7$-taxon foregrounds with 100-codon alignments, foreground-$\omega$ estimates can range from 1.0 to >100 across replicate runs. They recommend reporting this instability rather than picking one run. They do *not* say that 1/5 escapes to the boundary should reclassify a 4/5 stable positive result. The authors' decision rule is thus a *judgement call dressed as a methodological convention*. Defensible? Yes. Pre-registered? No. The §4.5 disclosure paragraph correctly admits this.

**Impact on conclusion**: net positive — the disclosure makes the cascade defensible. But a referee who pushes on this will get the authors to admit the rule was generated by the data, not by the literature.

### 1.3 Lakatosian-rescue cumulative pattern: framing pivot + Layer-4 softening + Apis cascade = three adjustments to the data
**Passages**: Deviation row #8 (framing pivot from A path to C path); Deviation row #9 (Layer-4 softening from PARTIALLY REFUTED to INCONCLUSIVE); Deviation row #9 *update* (Apis cascade from TENTATIVELY SUPPORTED to APIS_OPTIMIZER_ARTIFACT).

**Why it concerns me**: Each individual move is defensible. The cumulative pattern is what a Lakatosian critic will name. The protective belt around the lineage-specific origins reading has been tightened three times in 48 hours: first by reframing the universality test from "convergent universality" to "widespread but not universal" pre-registered falsification; second by softening Layer 4 from a partial refutation to an inconclusive result that is excluded from the inference burden; third by the Apis cascade that takes the one remaining positive and reclassifies it as optimiser-sensitive. After all three moves, the lineage-specific origins reading survives unscathed because every adjustment removed evidence that *would* have been awkward for it (a partial Layer-4 pass would have favored universality; a robust Apis positive would have been "convergence" evidence, which is harder to reconcile with lineage-specific origins). The pattern is exactly Lakatos's criterion for an ad-hoc rescue: **the protected hypothesis becomes harder to falsify with each adjustment**.

**Counter-citation**: @lakatos1970methodology *Criticism and the Growth of Knowledge*; @mayo2018statistical Ch. 3 on "saving the hypothesis." The defence the authors can offer is that lineage-specific origins is the *post-hoc surviving residual* (§4.6 limitations explicitly admits this) and Paper 2 will commit to its predictions before the next data is collected. This defence is adequate but only if Paper 2 actually delivers a quantitative pre-reg before the fact.

**Impact on conclusion**: the synthesis claim survives but the *narrative arc* is now visibly post-hoc. A skeptical referee will note this.

### 1.4 "Insufficient method power" is invoked as if it diagnoses the data, but it is itself a post-hoc reading
**Passages**: §3.5 line 227 ("the failure mode is **insufficient method power on this alignment**, not confirmed absence of selection"); §4.5 line 286 ("branch-site Model A on this alignment cannot resolve the universality question"); §4.6 line 293 ("inconclusive between true biological null [...] and insufficient method power"); §4.8 line 299 ("is our test powerful enough to detect it").

**Why it concerns me**: The phrase "insufficient method power" appears 4× and is used as if it were a diagnosed property of the data. But branch-site Model A *was the pre-registered test*. A pre-registered test that returns null cannot be re-described as "insufficient method power" without that re-description being itself a post-hoc move. The data show: 3 robustly null clades + 3 optimiser-sensitive clades. From that, **two readings are equally compatible**: (a) selection is genuinely absent on these clades and the optimiser-sensitive results are spurious local optima with no biological signal; (b) selection is present but undetectable on this alignment / with this test. The manuscript declares (b) as the "honest reading" without justifying why (b) is preferred over (a). A pure Popperian reading would be (a): the test was pre-registered, it returned null, the universality prediction is refuted, end of story. Reading (b) gives the lineage-specific origins model a methodological alibi for not delivering positive evidence, which is again Lakatosian-protective.

**Counter-citation**: @yang2007paml on branch-site test interpretation; @anisimova2007branchsite on small-foreground-clade behaviour. Anisimova & Yang 2007 do discuss method power on small foregrounds — but they do not license the move "if my test returned null, conclude the test lacked power." That's reading the test by its desired outcome. The honest framing would be: "we cannot distinguish between true null and insufficient power on this alignment; we report both readings as live and defer disambiguation to Paper 2 with BUSTED/aBSREL/RELAX." §4.6 line 293 *does* say this — but §3.5, §4.5, and §4.8 lead with the "insufficient method power" reading as if it were the diagnosed answer. Inconsistent across sections.

**Impact on conclusion**: 80% honest, 20% protective. Fixable by a single sentence in §3.5 acknowledging that "insufficient power" is one of two readings, not the diagnosed reading.

### 1.5 The "small-clade boundary-artefact range" definition added in §2.5 is opportunistically convenient
**Passages**: §2.5 line 110 ("We classify a foreground $\omega_{2a} > 30$ on a clade with $n \le 7$ taxa as falling within the **small-clade boundary-artefact range** [@anisimova2007branchsite]").

**Why it concerns me**: The C+ audit asked for this threshold to be defined. C++ defined it. But the threshold ($\omega > 30$ on $n \le 7$ taxa) is **exactly calibrated to capture all three escape clades** — Apis ($\omega = 36.18$, $n = 4$), dmel Gr64 ($\omega = 144.9$, $n = 6$), dmel all-Grs ($\omega = 95.07$, $n = 7$). A skeptical reader can ask: "if the threshold were $\omega > 50$ or $n \le 5$, would Apis fall outside the artefact range and survive as a robust positive?" The answer is yes — Apis would be classified as robust under either alternative threshold. The chosen threshold is the only one of several plausible thresholds that captures Apis. Anisimova-Yang 2007 do not specify $\omega > 30$ on $n \le 7$ as a published cutoff; the manuscript writes "based on their reported instability ranges for foreground $\omega$ estimates on small alignments" but does not cite a specific table or figure number. The threshold is therefore a **reverse-engineered classification rule** that ensures Apis ends up in the artefact bucket. This is defensible if the authors can point to Anisimova-Yang 2007's exact stated instability ranges; problematic if they cannot.

**Counter-citation**: @anisimova2007branchsite Table 1 / Figure 2 reports type-I error rates and parameter-estimation bias as a function of foreground-clade size and true $\omega$, but does not give a "small-clade boundary-artefact range" with hard numerical bounds. The threshold in §2.5 is the authors' interpretation, not a published cutoff.

**Impact on conclusion**: borderline. The threshold is defensible but its calibration to capture exactly the three escape clades is suspicious. A referee will ask why $\omega > 30$ specifically.

### 1.6 The Pfam null-baseline result is a weak refutation and the manuscript is too quiet about that
**Passages**: §3.3 line 157 ("$P(\text{Jaccard} = 0 \mid \text{null}) = 0.9998$"); §4.4 line 281 ("the data are *consistent with* parallel functional emergence from non-orthologous parts but cannot statistically establish convergence").

**Why it concerns me**: The Pfam null-baseline result is *not* a refutation of universality in the strong sense the manuscript claims. The result is: "Jaccard = 0 between TAS1R and Gr Pfam sets, which is the modal outcome under a null where two random orthologs from these genomes share no Pfam domain 99.98% of the time." This means **the test had no power to distinguish shared from non-shared substrate** — the null predicted what we observed regardless of whether substrate is universal or non-universal. The manuscript correctly recognises this in §4.4 ("cannot statistically establish convergence"), but Layer 3's verdict in §3.5 is "NOT SUPPORTED" and the synthesis says Layer 3 is one of two layers carrying the "not universal" inference weight. **A test that cannot distinguish the two hypotheses cannot be load-bearing on either**. Layer 3 should be re-classified as **inconclusive** alongside Layer 4, leaving only Layer 2 ($K = 0.117$) as the load-bearing refutation of universality.

**Counter-citation**: @stern2013genetic *Nat Rev Genet* on parallel vs convergent molecular evolution explicitly notes that the absence of shared domains is the expected outcome for receptor families that arose in different lineages from different ancestral GPCR subfamilies — i.e., the Pfam null is *uninformative* on the universality of reward-fitness decoupling, because it tests substrate sharing rather than functional convergence.

**Impact on conclusion**: serious. If Layer 3 is reclassified as inconclusive, the synthesis claim "widespread but not universal" rests on Layer 2 alone, which is a single $K$ test on $n = 56$ species. That is a *much* weaker basis for the headline claim than the manuscript currently presents.

### 1.7 The "lineage-specific origins" reading is a residual, not a positive finding, and the abstract / §1 should not present it as a result
**Passages**: Abstract Conclusion line 46 ("supporting a *lineage-specific origins* model"); cover letter line 18 ("We interpret this as supporting a *lineage-specific origins* model"); §1 does not yet present lineage-specific origins as a result, but §4.1 line 266 does ("the fourth reading [...] is the most parsimonious surviving alternative").

**Why it concerns me**: The Abstract Conclusion sentence "We interpret these results as supporting a *lineage-specific origins* model" is a category error. Negative results on three universality predictions do not *support* lineage-specific origins — they fail to refute it. Lineage-specific origins survives as the *residual* reading because it is what's left when the universal readings are eliminated; but it has not itself been tested. The §4.6 limitations correctly classify the lineage-specific reading as "post-hoc and hypothesis-generating." But the Abstract and cover letter use the verb "supporting" — which to a casual reader implies the data confirm lineage-specific origins. They do not. The data refute (or fail to confirm) universality; lineage-specific origins is what *might* be true if universality is false, but Paper 1 has not demonstrated it.

**Counter-citation**: @popper1959logic on the asymmetry between corroboration (residual after refutation) and proof. The lineage-specific origins reading is at most *corroborated* (in Popper's sense of "not yet refuted"), not *supported* (in the natural-language sense of "the data favour this model").

**Impact on conclusion**: medium. Fix: change "supporting a lineage-specific origins model" to "consistent with a lineage-specific origins model that Paper 2 will test directly" — both in the Abstract Conclusion sentence and in the cover letter Core Thesis paragraph.

### 1.8 The 7 phyla / 56 species existence claim relies on author-only coding and IRR is deferred
**Passage**: §3.1 line 143 ("Two-coder inter-rater reliability for F1–F4 was computed on the full corpus; blinded external three-coder recoding on a 30% subset is deferred (§4.6 Limitations)"); §4.6 line 293 ("blinded external three-coder recoding on a 30% subset is not delivered in Paper 1 and is committed as a Paper-1 OSF addendum within 30 days of RSOS final publication").

**Why it concerns me**: Layer 1 (existence) is the only layer that comes out positive. It rests entirely on author-only coding of 114 cases against F1–F4. The two-coder author IRR is mentioned but not reported quantitatively (no Cohen's κ or Fleiss' κ value given in §3.1). The external three-coder Fleiss' κ is committed as a 30-day post-acceptance OSF addendum. RSOS reviewers in PRISMA-using fields (epidemiology, behavioural ecology meta-analysis) will flag this as a reporting gap: the standard expectation is that IRR is reported *in the paper*, not committed as an addendum. The C+ audit flagged this and it carries forward unaddressed.

**Counter-citation**: @page2021prisma PRISMA-2020 statement Item 6 explicitly requires "the methods used to assess risk of bias in the included studies, including details of the tool(s) used, how many reviewers assessed each study and whether they worked independently, and if applicable, details of automation tools used in the process." The committed-but-undelivered IRR fails this item.

**Impact on conclusion**: medium. Layer 1 is what makes the "widespread" half of the headline; if it is contested at IRR level, the headline collapses to "not universal" without the "widespread" prefix.

### 1.9 The cover letter overstates the OSF anchoring claim
**Passage**: Cover letter paragraph 4 ("All three pre-registered universality predictions ($K > 0.30$; Jaccard $\ge 0.70$; $\ge 1$ positive-selected gene-lineage pair at Bonferroni-corrected significance) are deposited verbatim in our OSF pre-registration").

**Why it concerns me**: The wording "$\ge 1$ positive-selected gene-lineage pair at Bonferroni-corrected significance" in the cover letter and §3.5 line 236 (L4: "$\ge 1$ positive-selected gene on $\ge 1$ lineage at branch-site Bonferroni-corrected significance") is the **strict** pre-registered threshold. Under that threshold, the *Apis* result at $p_\text{Bonf-prereg} = 0.049$ **passes**. The §4.5 disclosure paragraph admits this. So the cover letter is simultaneously claiming (a) the OSF deposit contains the threshold verbatim and (b) all three predictions are "not supported." But under the verbatim threshold from the OSF deposit, prediction (iii) **is** partially supported (Apis passes). The C++ paper has resolved this internally by adopting the diagnostic-augmented downgrade and saying "more conservative than pre-registration required." But the cover letter does not show its work — it just asserts "all three are not supported." A careful editor reading both the cover letter and §4.5 will notice the tension.

**Counter-citation**: §4.5 line 290 itself, which explicitly admits "Strictly read against this threshold, the *Apis* Gr_sweet production result [...] satisfies the pre-registered H6a Gate."

**Impact on conclusion**: small but fixable. The cover letter should add one clause after "all three are not supported": "(under our diagnostic-augmented reading; the strict pre-registered threshold is partially passed by the *Apis* result, and the §4.5 disclosure addresses this)."

### 1.10 No dose-response / continuous-effect quantification of Layer 1
**Passage**: §3.1.

**Why it concerns me**: Layer 1 is asserted as "widespread" with 114 cases / 7 phyla / 56 species, but $\Delta_{ST}$ is reported only descriptively (as a 0–1 magnitude on a per-case basis, averaged within species). There is no test that the distribution of $\Delta_{ST}$ values is non-trivially elevated above what would be expected under a null where reward-fitness coupling is the default and decoupling is a publication artefact. Without such a test, "widespread" is a claim about *case counts*, not a claim about effect-size magnitudes. A reviewer can ask: "is the mean $\Delta_{ST}$ across the 56 species significantly different from a small-effect null (e.g., $\Delta_{ST} < 0.10$)?" The manuscript does not answer this.

**Impact on conclusion**: small. The "widespread" framing is defensible on case counts alone for a PRISMA-style synthesis, but the absence of an effect-magnitude test means "widespread" is a phrase about coverage, not about effect strength.

### Recommendation: **Minor Revision** (with one item that could be argued as Major if the referee is hostile)

The C++ paper has cleared the major C+ concerns. The remaining items are presentation (1.1), the disclosure paragraph (1.2 — already admirably honest), and substantive but not lethal critiques (1.3 Lakatosian, 1.6 Layer-3 weak refutation, 1.7 "supporting" vs "consistent with"). Items 1.4, 1.5, 1.8, 1.9, 1.10 are 1-paragraph or 1-sentence fixes. None require re-execution.

### Summary for the Editor
This is a substantively improved revision. The Apis cascade is genuine — the diagnostic was actually run, the verdict came back optimiser-artefact, and the manuscript propagated the cascade across all relevant sections including the cover letter and figures. The §4.5 disclosure paragraph admitting the strict pre-registered reading would partially pass H6a is unusually candid. Three remaining concerns: (i) the "0/6 robust positives" headline appears in seven places and risks reading as null-result publishing rather than as a refutation of universality; (ii) the Pfam null-baseline result (Layer 3) is uninformative on universality direction and should be re-classified as inconclusive rather than NOT SUPPORTED, leaving Layer 2 as the sole load-bearing refutation; (iii) the "supporting a lineage-specific origins model" verb in the Abstract and cover letter overstates what nulls on universality can support — "consistent with" is the correct verb. None requires re-execution; all are revision-class. Send to review with one round of author revision.

---

## 2. Role 2 — Sympathetic Editor (RSOS)

### First 30 Seconds Impression

The title "Sweet Trap is widespread but not universal: a pre-registered cross-metazoan falsification of reward-fitness decoupling as a shared evolutionary trait" signals immediately what the paper does (pre-registered falsification), what scope (cross-metazoan), and what verdict (widespread but not universal). This is editor-friendly — I can tell from the title alone whether to send it for review. The Abstract opens with "Reward-fitness decoupling [...] has been described piecewise across animal taxa as evolutionary traps, ecological traps, sensory exploitation, and supernormal stimuli" — this anchors the construct in established literatures. The Question paragraph lists three pre-registered predictions with quantitative thresholds. The Results paragraph reports "All three universality predictions are not supported" with specific numbers — this is what RSOS rewards. The Conclusion sentence "Sweet Trap, defined as $\Delta_{ST} = U_\mathrm{perc} - \mathbb{E}[U_\mathrm{fit} \mid B]$, is a *widespread but not universal* phenomenon" gives me a citable verdict in one sentence. Editor reaction: **interested, would send to review subject to a quick technical-soundness check**.

The cover letter paragraph 4 emphasising the OSF anchoring is unusual and credibility-positive — most submissions tell the editor the data is on OSF; few invite the editor to verify each pre-registered threshold against the deposit. The author-signal disclosure (both ORCIDs 0009-, no senior co-author) is appropriately handled — RSOS's merit-based model accommodates this.

### Three Signals Checked (RSOS criteria)

1. **Scientific validity**: ✅ — Pre-registered framework, OSF + bioRxiv priority deposits 2026-04-24 before data extraction, deviation log 9 rows including the cascade. Diagnostic was actually executed (5 + 5 = 10 codeml runs on diagnostic with verifiable outputs in `outputs/optimizer_diagnostic_report.md` and `apis_optimizer_diagnostic_report.md`). The hummingbird TAS1R1 positive control at LRT = 55.9 confirms pipeline integrity. **Improvement vs C+**: yes — the asymmetric application that C+ flagged is now resolved; both LRT=0 and LRT>0 production clades have been subjected to the same diagnostic, and the verdict was propagated across the manuscript with internal consistency.

2. **Technical soundness**: ✅/⚠️ — Methods are sound; the Apis cascade is technically defensible. The §2.5 "small-clade boundary-artefact range" threshold is now defined ($\omega > 30$ on $n \le 7$). The ⚠️ remains because: (a) the $\omega > 30$ threshold is reverse-engineered (Hostile Referee §1.5); (b) the Layer-3 Pfam null-baseline test cannot distinguish shared from non-shared substrate (Hostile Referee §1.6) and arguably should be reclassified as inconclusive; (c) the Apis APIS_OPTIMIZER_ARTIFACT decision rule is the authors' rule, not a published methodological convention (Hostile Referee §1.2). None of these are fatal at desk; all are within scope of one revision round. **Improvement vs C+**: yes — the C+ #1 flagged asymmetric-diagnostic concern is resolved.

3. **Adequately reported**: ✅ — Deviation log 9 rows including row #9 update for the cascade. OSF deposit anchoring is explicit in §1, §3.5, §4.5, cover letter. GitHub repo public (https://github.com/andyhsi2023-cq/sweet-trap-paper1, 697 files, 28.8 MB per provided context). FigS1 delivered. Five suggested reviewers with verified emails (4 of 5 institutional, 1 institutional-pattern guess noted). Submission form complete except suggested AE (deferred for author lookup pre-dispatch). The IRR-as-addendum commitment is the one remaining reporting gap; acceptable for RSOS submission given the open-peer-review preference + 30-day-post-acceptance commitment. **Improvement vs C+**: yes — Figure 5 caption now matches §3.5 verdict; §4.1 verdict word fixed; abstract trimmed (~340 words from prior ~480).

### Decision: **Send to Referees**

This is a clear send. The pre-registered falsification framework + open-science deposits + transparent disclosure of the H6a strict-threshold reading are all aligned with RSOS's brand. The remaining concerns are revision-class, not desk-class.

### Send-to-Review Cover Note Draft (2 paragraphs)

> Dear Drs An and Xi,
>
> Your manuscript "Sweet Trap is widespread but not universal" has been examined by the editorial team and is being sent for peer review. The pre-registered four-layer falsification framework, the OSF + bioRxiv priority deposits dated 2026-04-24 ahead of data extraction, and the post-data-collection optimiser-boundary diagnostic propagated transparently across the manuscript and Deviation log row #9 are well-aligned with RSOS's open-science mission. We particularly appreciate the §4.5 "Disclosure on H6a vs the pre-registered threshold" paragraph, which acknowledges the strict pre-registered reading partially supports H6a and provides an explicit justification for the diagnostic-augmented downgrade.
>
> Reviewers will be asked to focus on three areas: (i) whether the §2.5 "small-clade boundary-artefact range" threshold ($\omega > 30$ on $n \le 7$) has adequate methodological grounding in @anisimova2007branchsite; (ii) whether Layer 3 (Pfam null-baseline non-enrichment) carries enough inference weight to remain in the synthesis as "NOT SUPPORTED" rather than "INCONCLUSIVE"; (iii) whether the "supporting a lineage-specific origins model" verb in the Abstract Conclusion is consistent with the §4.6 classification of that reading as "post-hoc and hypothesis-generating." We anticipate one round of author revision after referee comments.

---

## 3. Role 3 — Methodological Expert

### Q1 — Did the Apis cascade introduce new flaws?

**Verdict: net positive, two residual technical concerns.**

The cascade closed C+'s single biggest methodological concern (asymmetric application of the optimiser-boundary diagnostic). Apis was subjected to the same 5-start diagnostic; result classified as APIS_OPTIMIZER_ARTIFACT per the asymmetric decision rule. Cascade integrated to §3.4, §3.5, §4.1, §4.5, §4.6, §4.8, Abstract Results (iii), Title, Cover Letter Core Thesis, Table 2 [†] footnote, Figure 4 caption, Figure 5 caption, FigS1 (extended to 6 clades). Internal consistency across all these locations checked and confirmed.

**Residual concern A — the asymmetric decision rule**: APIS_OPTIMIZER_ARTIFACT is triggered by "any LRT < 1.0 OR omega_2a near 1.0 (|w-1| < 0.5) OR omega_2a > 200" on any single start. On Apis, 4 of 5 starts converge to LRT = 9.92 with $\omega = 36.18$; only the $\omega_0 = 5.0$ start escapes to LRT = $-2.48$ with $\omega = 1.63$. The rule classifies this as ARTIFACT because of the 1/5 escape. The methodological literature (@yang2007paml, @anisimova2007branchsite) recommends interrogating LRT = 0 results for boundary trapping but does not prescribe that 1/5 escapes should reclassify a 4/5 stable positive. The rule is the authors' rule. Defensible (the negative LRT is itself a sign of optimiser instability that should not be ignored); not standard. The §4.5 disclosure paragraph correctly admits this.

**Residual concern B — the "$\omega > 30$ on $n \le 7$" boundary-artefact range**: this threshold is now defined in §2.5 but is not anchored to a specific Anisimova-Yang 2007 table or figure number. The threshold happens to capture exactly the three escape clades. Calibration coincidence is suspicious. A referee will ask why $\omega > 30$ specifically (rather than $\omega > 50$ or $\omega > 20$). Acceptable but vulnerable.

**Has the verdict crossed into self-defeating overcorrection?** Marginal yes on the headline; substantively no. The verdict text in §3.5 explicitly anchors the synthesis on Layers 2 + 3 (not Layer 4), and §4.5 explicitly states "branch-site Model A on this alignment cannot resolve the universality question" — this is the right framing. But the "0/6 robust positives" phrasing appears in 7 headline positions (Hostile Referee §1.1), which can read to a skim-reader as if the experiment found nothing. The substance is correct; the presentation is unbalanced.

### Q2 — Does the §3.5 synthesis "widespread but not universal" still cohere with 0 robust positives?

**Verdict: yes, conditional on Layer 2 being load-bearing on its own; Layer 3 should arguably be reclassified to INCONCLUSIVE.**

The synthesis statement explicitly anchors on Layers 2 + 3 and excludes Layer 4 from the inference burden. Layer 2 ($K = 0.117$, $p = 0.251$) is a clean refutation of the pre-registered universality prediction ($K > 0.30$). The within-Arthropoda subset ($K = 1.446$) confirms the test can detect signal where it exists, ruling out a Type II reading at the cross-phylum level. So Layer 2 is genuinely load-bearing.

Layer 3, however, is a **null-baseline result**: Jaccard = 0 between TAS1R and Gr Pfam sets, where the matched-random null returns Jaccard = 0 with $P = 0.9998$. This test cannot distinguish between (a) substrate is genuinely shared (we'd expect Jaccard > 0) and (b) substrate is genuinely non-shared (we'd expect Jaccard = 0). The result is consistent with both — but the *null* also predicts (b) regardless of which is true. **A test whose null predicts the observed outcome regardless of the alternative is uninformative on the alternative**. §4.4 line 281 admits this ("cannot statistically establish convergence") but §3.5 keeps Layer 3 as load-bearing on the not-universal claim. This is inconsistent.

Strictly, Layer 3 should be reclassified as **INCONCLUSIVE** (alongside Layer 4), and the synthesis would then rest on Layer 2 alone. That is a much weaker basis than the manuscript currently presents. **Suggested fix**: update Layer 3 verdict in §3.5 table from "NOT SUPPORTED" to "INCONCLUSIVE — null-baseline uninformative on direction" and reword the synthesis to "the load-bearing refutation is Layer 2 (cross-phylum K refuted at $p = 0.251$); Layer 3 is null-baseline uninformative; Layer 4 is optimiser-sensitive."

### Q3 — Three measurement / data weaknesses

1. **Inter-rater reliability deferred**. Layer 1 (the only positive layer) rests on author-only F1–F4 coding of 114 cases. Two-coder κ mentioned in §3.1 but not numerically reported; external three-coder Fleiss' κ committed as 30-day-post-acceptance OSF addendum. PRISMA-2020 Item 6 [@page2021prisma] expects in-paper reporting. **Fix**: report two-coder κ value in §3.1; keep external three-coder as addendum.

2. **No effect-magnitude test on $\Delta_{ST}$**. Layer 1 reports case counts (114 cases / 7 phyla / 56 species) but no test that the distribution of $\Delta_{ST}$ values is significantly elevated above a small-effect null. "Widespread" is a coverage claim; an effect-magnitude test would strengthen it. **Fix**: add one-sample test against $\Delta_{ST} < 0.10$ null in §3.1.

3. **PRISMA recovery rate**: 23 of 216 candidates (10.6%) excluded as pdf-unavailable. Cnidaria ($n = 5$), Mollusca ($n = 4$), Annelida ($n = 2$) coverage is thin. Acceptable for a Layer-1 existence claim but would weaken any claim about phylum-level patterns within those phyla.

### Q4 — Three unaddressed identification threats

1. **Publication bias on Layer 1**. PRISMA-style synthesis of cases of reward-fitness decoupling is itself subject to the file-drawer problem [@rosenthal1979file]: cases where reward-fitness *coupling* is preserved (the negative result) are not published as cases. The 114 cases are 114 *observed* decouplings, not a representative sample of the species universe. "Widespread" therefore conflates "frequently published" with "frequently occurring." Manuscript does not address.

2. **Selection on the alignment for Layer 4**. The 38-taxon × 3,234-codon Gr_sweet alignment is the single alignment on which 3 of 6 branch-site tests run. If this alignment is poor (alignment quality, sites under saturation, paralog contamination), all three of those tests inherit the same problem. The manuscript reports that the Gr family has expanded heavily in *Drosophila* (38 sequences from a single species) and contracted in *Apis* (10 sequences total), which is exactly the kind of asymmetric paralog landscape that breaks branch-site assumptions. No alignment-quality diagnostics are reported (Gblocks columns retained; sites with saturation flagged; etc.).

3. **The lineage-specific origins reading as a residual**. The Discussion presents this as the "most parsimonious surviving alternative" but does not commit to a Paper-2 falsification protocol with quantitative thresholds. Without a quantitative pre-reg before Paper 2 data collection, the lineage-specific reading is an unfalsifiable residual.

### Q5 — Three "should have done but didn't"

1. **Power analysis on Blomberg's $K$ at $n = 56$**. Münkemüller et al. 2012 [@munkemuller2012brief] is cited but not used to compute a numerical power estimate at the $n = 56$ sample size against the pre-registered $K > 0.30$ threshold. A power calculation showing $1 - \beta \ge 0.80$ would harden Layer 2; absence of one leaves the Type II reading incompletely closed.

2. **PGLS-adjusted phylogenetic signal**. Standard practice is to report Blomberg's $K$ alongside PGLS estimates with covariate adjustment for body mass, generation time, ALAN exposure, and publication period. Manuscript defers PGLS to Paper 2 (§4.7). For a flagship Layer-2 result that carries the synthesis, PGLS should be in Paper 1 not Paper 2.

3. **BUSTED / aBSREL / RELAX triangulation on Apis**. The Apis result is the most consequential single test in the paper (the "most plausible candidate" for lineage-specific selection). It is now declared optimiser-artefact based on a single $\omega_0 = 5.0$ start escaping to a sub-null basin. The cleaner methodological move would be to triangulate with BUSTED / aBSREL / RELAX in Paper 1 itself rather than deferring to Paper 2; this would resolve whether Apis is genuinely positive (under triangulation) or genuinely artefact (negative under triangulation). The deferral leaves the most consequential result unresolved.

### Verdict

**Needs minor patching.** No re-execution required. The cascade is sound, the disclosure is admirable, the integration is internally consistent. The remaining concerns are revision-class and total approximately 2–4 hours of author work.

---

## 4. RSOS-specific desk-reject risks

### ScholarOne / RSOS submission checklist

| Item | Status | Comment |
|---|---|---|
| Article type (Research Article) | ✅ | Submission form §1 |
| Subject categories (≤3) | ✅ | Evolution / Behaviour / Genetics |
| Keywords (5) | ✅ | Submission form §3 |
| Corresponding authors with ORCID | ✅ | Both 0009-, both verified |
| Suggested AE | ⚠️ | DEFER — author lookup pre-dispatch (acceptable per RSOS guidance) |
| Suggested reviewers (3-5) | ✅ | 5 names with verified emails (1 institutional-pattern guess flagged) |
| COI declaration | ✅ | None |
| Funding statement | ✅ | None external |
| Data and code availability | ✅ | OSF pv3ch + GitHub mirror |
| Open data statement | ✅ | Yes |
| Open peer review preference | ✅ | Yes |
| CRediT contributions | ✅ | Both equal + Lu An (Resources) + Hongyang Xi (Supervision) |
| Ethical compliance | ✅ | Public summary statistics only |
| AI / authorship statement | ✅ | Disclosed |
| Word count | ⚠️ | Body 4,310 words (RSOS no hard limit; well within); Abstract ~340 words (RSOS guidance ~250 for structured abstracts — borderline acceptable but on the edge) |
| Number of figures | ✅ | 5 main + 1 supplementary |
| Number of tables | ✅ | 3 |
| Number of references | ✅ | 89 |
| Pre-registration declaration | ✅ | OSF pv3ch deposited 2026-04-24 |
| Preprint declaration | ✅ | bioRxiv BIORXIV/2026/720498 |

**Overall**: passes the ScholarOne checklist with two ⚠️ items (suggested AE deferred for author lookup; abstract length slightly above guidance). Neither is desk-blocking.

### RSOS technical-soundness criteria

- **Scientifically valid**: ✅ — pre-registered framework; OSF deposits pre-data; deviation log; transparent disclosure paragraph in §4.5.
- **Technically sound**: ✅/⚠️ — diagnostic delivered for both LRT=0 and Apis clades; asymmetric decision rule defensible; "$\omega > 30$" threshold reverse-engineered (Hostile Referee §1.5); Layer 3 verdict overstated (Hostile Referee §1.6); IRR deferred (Hostile Referee §1.8).
- **Adequately reported**: ✅ — Methods complete; Deviation log 9 rows; OSF + GitHub anchoring explicit; figures and table captions self-contained.

**Verdict**: meets all three RSOS criteria.

---

## 5. P0 / P1 catalogue

### P0 (must fix before submit; estimated <15 min total)

**P0-1**: Cover letter line 18 — change "supporting a *lineage-specific origins* model" to "consistent with a *lineage-specific origins* model that Paper 2 will test directly on independent data." (2 min)

**P0-2**: Abstract Conclusion line 46 — change "We interpret these results as supporting a *lineage-specific origins* model" to "We interpret these results as consistent with a *lineage-specific origins* model in which reward-fitness decoupling re-emerges wherever local ecological conditions decouple proximate signals from realized fitness; Paper 2 will test the lineage-specific predictions directly on an independent corpus." (3 min)

**P0-3**: Cover letter paragraph 4 — after "all three are not supported by our data" add "(under our diagnostic-augmented reading; the strict pre-registered H6a threshold is partially passed by the *Apis* result, with the §4.5 disclosure paragraph providing the rationale for the more conservative downgrade)." (3 min)

**Total P0 time: 8 min.** All edits to two files (manuscript.md Abstract section and cover_letter.md). No re-make required (manuscript.md change is in Abstract; cover_letter.md is pandoc-ed separately if at all).

### P1 (would-be-nice-to-fix; 30 min – 2 hours)

**P1-1**: §3.5 verdict table — reclassify Layer 3 from "NOT SUPPORTED" to "INCONCLUSIVE — null-baseline uninformative on direction" and update §3.5 synthesis text to "Layer 2 is the load-bearing refutation; Layer 3 is null-baseline uninformative; Layer 4 is optimiser-sensitive" (15 min).

**P1-2**: §3.1 — report the two-coder author Cohen's κ value numerically (5 min if value already computed; 30 min if needs to be re-run on the 114-case sheet).

**P1-3**: §2.5 — add explicit page/table citation to Anisimova-Yang 2007 anchoring the "$\omega > 30$ on $n \le 7$" threshold (or admit "based on our judgement of their reported instability ranges" — 5 min).

**P1-4**: §3.1 — add one-sample test that the distribution of $\Delta_{ST}$ values across 56 species is significantly above $\Delta_{ST} = 0.10$ small-effect null (20 min).

**P1-5**: Reduce the "0/6 robust positives" repetition from 7 places to 3–4 by replacing some with "Layer 4 is uninformative on universality direction" or "the selection layer cannot resolve the universality question on this alignment" (15 min — purely rewording).

**P1-6**: §3.5 — add explicit Popper / Lakatos one-sentence acknowledgement that "Layer 4 inconclusiveness places that layer outside the inference burden for either polarity; if Layer 4 had returned a robust positive, it would have complicated the not-universal verdict; the lineage-specific origins reading is the post-hoc surviving residual, not a positive finding." (5 min).

### P2 (defer to revision)

**P2-1**: PGLS-adjusted phylogenetic signal in §3.2 (~2 hours of analysis + write).
**P2-2**: Power analysis on Blomberg's $K$ at $n = 56$ against $K > 0.30$ (30 min).
**P2-3**: BUSTED / aBSREL / RELAX triangulation on Apis (Paper 2 — defer).
**P2-4**: External three-coder Fleiss' κ on 30% subset (committed as 30-day OSF addendum — defer).

---

## 6. Bottom-Line Verdict

**FIX-AND-SUBMIT** — three P0 edits totalling ~8 minutes, all wording / framing tweaks in the Abstract Conclusion sentence and cover letter. Once those three edits are applied, the manuscript is **SUBMIT-READY**.

### Acceptance probability after RSOS revision round

**78–85%** at RSOS, conditional on:
- (a) P0-1, P0-2, P0-3 applied (the "supporting" → "consistent with" verb fix and the cover-letter strict-threshold disclosure);
- (b) Reviewer revision round addresses P1-1 (Layer 3 reclassification), P1-2 (IRR κ value reported), P1-5 ("0/6" repetition reduced), and P1-6 (Lakatos-acknowledgement sentence);
- (c) The OSF deposit content matches what the manuscript and cover letter claim it contains (per project memory: Andy ran "bulletproof" verification of three predictions verbatim in deposit zip).

If submitted with all three P0 fixes, desk-reject probability drops to **6–8%**. The remaining risk is the "self-defeating overcorrection headline" (Hostile Referee §1.1) and the OSF-deposit-content audit (~3% if Andy's verification holds; up to ~10% if it does not).

### Genuine improvement vs C+?

**Yes — substantively, not cosmetically.** The C+ audit's three required-revisions items were: (i) §4.1 verdict-word inconsistency, (ii) Apis diagnostic asymmetry, (iii) "small-clade boundary-artefact range" numerically defined. C++ resolves (i) [Figure 5 caption + §4.1 text now consistent], resolves (ii) [Apis diagnostic actually run; verdict propagated], partially resolves (iii) [threshold defined but reverse-engineering concern remains — see Hostile Referee §1.5]. The §4.5 disclosure paragraph is a new admission that strengthens the paper's credibility. The Layer-4 verdict tightening from "3+2+1 with 1 tentative" to "3+3+0 with 0 robust positives" is a genuine epistemic move, not a cosmetic relabelling — it follows directly from the Apis diagnostic result and removes the asymmetry C+ identified. The cumulative-Lakatosian concern (Hostile Referee §1.3) is the new vulnerability introduced by the cascade, but it is offset by the §4.5 disclosure paragraph's transparency. **Net: C++ is a better paper than C+**, with desk-reject probability reduced from 22-28% to 8-12% and acceptance probability raised from 65-75% (C+ post-revision) to 78-85% (C++ post-revision).

---

## Final Synthesis: Bottom Line for the Author

The Apis cascade is a real epistemic improvement, not a cosmetic move: the diagnostic was actually run, the verdict came back optimiser-artefact, and the cascade was propagated across all relevant locations including the cover letter and figures. The §4.5 H6a disclosure paragraph is unusually candid and is a credibility asset. Three P0 fixes remain — all wording, totaling 8 minutes: change "supporting a lineage-specific origins model" to "consistent with" in the Abstract Conclusion and cover letter, and add the strict-pre-registered-threshold caveat to cover-letter paragraph 4. After those, this is submit-ready at RSOS with desk-reject probability under 12% and post-revision acceptance probability 78–85%. The two non-P0 substantive concerns the referees will surface are (a) Layer 3 should arguably be reclassified to INCONCLUSIVE because the matched-random Pfam null is uninformative on direction and (b) the "0/6 robust positives" headline appears in seven places and risks reading as null-result publishing rather than as a refutation of universality. Both are revision-class.

---

*Red-Team Review v1.3 — Stage 7 C++ FINAL pre-submit audit, 2026-04-25*
