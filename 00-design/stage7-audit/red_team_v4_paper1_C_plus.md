# Red Team Review: Sweet Trap v4 Paper 1 — C+ post-diagnostic audit
**Stage**: S7 (post-diagnostic-integration audit, pre-RSOS submission)
**Target journal**: Royal Society Open Science (RSOS)
**Date**: 2026-04-26
**Prior context**: Yes — read `red_team_v4_paper1_C_path.md` (2026-04-25), `optimizer_diagnostic_report.md` (2026-04-26 08:37), and `04-figures/FigS1_optimizer_diagnostic.png`.
**Manuscript**: 4,761 words; 5 figures + FigS1; 3 tables; Deviation log 9 rows; Layer-4 verdict softened from PARTIALLY REFUTED to **INCONCLUSIVE — optimiser-sensitive**.

---

## 0. Desk-Reject Probability at RSOS

**Overall desk-reject probability: 22–28%** (slightly *higher* than the C-path snapshot, despite the C+ technical fix).

Why higher? The C-path desk-risk was 18–25% gated by three vectors: IRR, strong-floor accounting, OSF timestamp. C+ has now resolved one of the original C-path "Required Revisions" items (the diagnostic is delivered, not placeholder). But it has introduced a **new desk-vector**: an editor scanning §3.5 and the Layer-4 row of the verdict table will see a verdict explicitly labelled "INCONCLUSIVE" carried into the integrated synthesis, and will notice that the synthesis nevertheless reads "widespread but not universal." This invites the question — *if Layer 4 is inconclusive between true null and insufficient method power, on what basis is Layer 4 contributing to a "not universal" claim at all?* The honest answer (it is not contributing — the synthesis explicitly says it rests on Layers 2 + 3) is sound, but only if the editor reads §3.5 carefully. If the editor reads only the abstract and the verdict table, they will see "3 not supported / 1 inconclusive" and may worry that the paper claims more than the data support. This is a presentation risk, not a substance risk, but it is real.

### Top-3 desk-reject candidates (ranked)

1. **OSF pre-registration timestamp still unverified by Andy (~12% probability of flagging)**. Carry-forward from C-path #3. Deviation row #8 (framing pivot) is dated 2026-04-25; OSF deposit claimed 2026-04-24 "before all data extraction"; row #9 (Layer-4 softening) is dated 2026-04-26. An editor opening osf.io/pv3ch will check whether the *original* protocol committed to (a) the four-layer falsification scheme, (b) the diagnostic-as-verdict-shifter rule, and (c) the K/Jaccard/Bonferroni numerical thresholds. If the OSF page does not contain all three, then the C+ framing (especially the diagnostic-driven softening) is post-hoc-relative-to-prereg. This is the single biggest live vulnerability and remains exactly as bad as in the C-path audit — possibly worse, because the diagnostic is now load-bearing on the verdict and the editor will check whether the diagnostic was pre-registered as a verdict-shifter or only as a sensitivity check.

2. **Inter-rater reliability still committed-but-undelivered (~8%)**. Carry-forward from C-path #1. §4.6 still says "blinded external three-coder recoding on a 30% subset is not delivered in Paper 1 and is committed as a Paper-1 OSF addendum within 30 days of RSOS final publication." The C-path audit flagged this as 10%; C+ has not addressed it. Layer 1 (existence: SUPPORTED) is the *only* layer that comes out positive in this paper, and it depends on author-coding alone at submission time. RSOS reviewers care about reporting completeness, and the IRR is exactly the kind of "you said you'd do this in your pre-reg" item they will surface. Probability lower than (1) only because RSOS editors have shown some tolerance for OSF-addendum commitments when other components are clean.

3. **The diagnostic-driven Layer-4 softening reads as a post-hoc rescue to a careful reader (~7%)**. New in C+. The honest read of the diagnostic data is that it reveals optimizer instability on this alignment — *not* that it adds evidence either for or against universality. The manuscript frames this correctly in places (§3.5 line 225 "the failure mode is insufficient method power on this alignment, not confirmed absence of selection"; §4.6 closing paragraph; §4.8 closing one-sentence). But §4.5 simultaneously deploys "the *Apis* escape is the most conservative of the three" framing, which subtly *reinforces* the lineage-specific story by saying *Apis* is "less of an outlier" now that two larger artefacts are visible alongside it. A skeptical editor reading §3.4–§4.5 in sequence will notice that the diagnostic was pre-registered as a sensitivity check, used to *invalidate* 5/6 negative tests, but framed as *contextualising* (rather than invalidating) the 1 positive test — an asymmetry that is technically defensible but rhetorically uneven.

---

## 1. Hostile Referee — First-Order Objections

### 1.1 The diagnostic-driven Layer-4 softening is asymmetric — invalidates negatives, contextualises the positive
**Passages**: §3.4 lines 174–179 (production-matrix paragraph; LRT = 0 paragraph); §4.5 line 286 ("the *Apis* escape is the most conservative of the three"); Table 2 rows 192–195 (Apis = primary production row; 2 *Drosophila* boundary escapes = DIAG rows, segregated below the line).

**Why it fails**: The diagnostic was applied *only to the 5 LRT = 0 clades*, not to the *Apis* production result. This is technically what the pre-reg specified (diagnostic on LRT = 0 clades to distinguish biological null from optimiser convergence), but the manuscript now uses the diagnostic outcome to *re-classify the 5/6 = 0 results as 3 robust-null + 2 optimiser-sensitive*, while the *Apis* result — which has $\omega_{2a} = 36.2$ on n = 4 taxa, sitting in the same boundary-artefact range as the *Drosophila* escapes ($\omega = 95.1, 144.9$) — is **not subjected to the same diagnostic**. Reviewer Goodman 2008 / Anisimova-Yang 2007 logic: if the boundary-artefact range is what disqualifies the *Drosophila* escapes from being primary positive results, then by symmetry it should disqualify the *Apis* signal too. The manuscript notes the asymmetry ("*Apis* is one of three boundary-range escapes") but resolves it by *retaining* *Apis* as "tentatively supported" rather than reclassifying it to "optimiser-sensitive." This is rhetorically defensible only if the diagnostic was pre-registered as a pure LRT = 0 sensitivity check; if it was pre-registered as a general boundary-artefact diagnostic, applying it asymmetrically is a problem. **The fix the manuscript needs is either: (a) run the diagnostic on the *Apis* clade with 5 starting $\omega_0$ values, or (b) reclassify *Apis* explicitly as also boundary-artefact-suspect.** The Paper-2 BUSTED commitment is not a substitute for the symmetry.

### 1.2 The synthesis "widespread but not universal" now rests on 2 of 4 layers
**Passage**: §3.5 line 225 ("The synthesis verdict — Sweet Trap is widespread but not universal — is unaffected because it rests on Layer 2 (cross-phylum $K = 0.117$) and Layer 3 (Pfam null-baseline non-enrichment), not on Layer 4 alone").

**Why it fails**: The verdict table at §3.5 still lists 4 rows: SUPPORTED (Layer 1), REFUTED (Layer 2), NOT SUPPORTED (Layer 3), INCONCLUSIVE (Layer 4). The integration sentence says only Layers 2 + 3 are load-bearing. But this means a *4-layer pre-registered framework* now reports its conclusion based on *2 layers*, with Layer 1 confirming existence (which is not what the universal-version hypothesis is about, by §1's own framing) and Layer 4 explicitly ducked. A reader can ask: if the framework was designed to require all four layers to converge, what does it mean that the conclusion now stands on half of them? The manuscript does not give a Lakatosian-style argument for why 2-of-4 is sufficient. **Counter-citation**: Mayo 2018, *Statistical Inference as Severe Testing*, on the asymmetric burden between "rejecting universality" and "supporting lineage-specific origins." The paper effectively rejects universality with K + Jaccard alone, but the integrated synthesis claim is slightly stronger than that. The honest framing would be: "Layers 2 and 3 alone refute universality; Layer 4 is uninformative on this dataset; the lineage-specific origins reading remains a hypothesis-generating residual." The current §4.1 line 260 framing ("partially refuted" for Layer 4) is no longer consistent with the new INCONCLUSIVE label — §4.1 still uses the old verdict word.

### 1.3 §4.1 and the Abstract Conclusion are inconsistent with the new Layer-4 verdict
**Passages**: Abstract Conclusion line 46 ("does not generate robust positive-selection signal distinguishable from optimiser-boundary artefacts in any tested clade after diagnostic interrogation"); §4.1 line 260 ("(iii) Detectable positive selection across multiple ecological-shift clades: **partially refuted** (1/6 clades tentative; 5/6 LRT = 0)").

**Why it fails**: The Abstract Conclusion is now C+-consistent ("does not generate robust positive-selection signal distinguishable from optimiser-boundary artefacts" — this is the INCONCLUSIVE phrasing). But §4.1 line 260 still calls Layer 4 "**partially refuted**" — that is the *old* C-path verdict word, not the new INCONCLUSIVE label. This is an internal inconsistency between the headline of §4 and the verdict in §3.5. A reviewer reading §3.5 then §4.1 will catch this in 30 seconds. **Direct fix**: §4.1 line 260 must be rewritten from "**partially refuted** (1/6 clades tentative; 5/6 LRT = 0)" to "**inconclusive — optimiser-sensitive** (3 robustly null; 2 optimiser-sensitive boundary escapes; 1 tentative in boundary range)." Without this fix, the C+ integration is incomplete and presents two incompatible verdicts in two consecutive sections.

### 1.4 The "small-clade boundary-artefact range" is invoked as if pre-defined, but the threshold is not stated
**Passages**: §3.4 line 175 ("foreground $\omega$ in the small-clade boundary-artefact range"); §3.4 line 179 ("Both *Drosophila* foreground $\omega_{2a}$ values lie within the small-clade boundary-artefact range that we elsewhere apply to quarantine the *Apis* signal"); §4.5 line 286 ("All three escape values lie in the small-clade boundary-artefact range").

**Why it fails**: The phrase "small-clade boundary-artefact range" is invoked five times (Abstract, §3.4, §3.5 verdict table, §4.5, §4.6) with citation to Anisimova-Yang 2007. But Anisimova-Yang 2007 do not define a numeric "small-clade boundary-artefact range" — they document estimation bias on $\omega$ in branch-site Model A under small foreground clades and recommend caution. The manuscript treats this as if there were a published $\omega > X$ threshold above which estimates are flagged as artefactual. There is not. The text reads as if there is a Pre-registered threshold of (say) $\omega > 30$ and all three escapes ($\omega = 36.2, 95.1, 144.9$) cross it; in fact the operational threshold is being applied case-by-case with no quantitative anchor. **The C+ paper needs a single sentence in §2.5 specifying the threshold**: "We classify foreground $\omega_{2a} > X$ on $n \le Y$-taxon foregrounds as in the small-clade boundary-artefact range per @anisimova2007branchsite." Without this, the diagnostic verdict is unfalsifiable in either direction.

### 1.5 FigS1 Panel B is hard to read — the artefact band is described in caption but not visually rendered
**Passage**: `04-figures/FigS1_optimizer_diagnostic.png` panel B.

**Why it fails (from inspection)**: Panel B (the $\omega_{2a}$ vs $\omega_0$ scatter) shows two pink/green divergent traces (D. mel. Gr64 cluster reaching $\omega_{2a} \approx 144.9$ at $\omega_0 = 5.0$; D. mel. all-Grs reaching $\omega_{2a} \approx 95.1$) and three flat traces (Coleoptera, Lepidoptera, Aedes) at $\omega_{2a} = 1.0$. The caption mentions a "small-clade boundary-artefact range (Anisimova & Yang 2007)" but there is no shaded band on the plot itself indicating *what range* (e.g., grey band over $\omega_{2a} > 30$ or > 50). The viewer is told there is an artefact band but cannot see its boundaries. Panel A (heatmap) is clean and readable. **Fix**: add a shaded grey rectangle on Panel B from $\omega_{2a} = X$ upward (with X chosen to match the 1.4 fix), and label the band "small-clade boundary-artefact range" in-figure rather than only in-caption. This would let the figure pass the standalone-readability test.

### 1.6 The post-hoc lineage-specific origins reading is now reinforced by an *additional* post-hoc move
**Passages**: §4.5 line 286 (newly extending the BUSTED/aBSREL/RELAX commitment from *Apis* alone to *Apis* + 2 *Drosophila* clades); §4.7 line 292 (Paper-2 scope expanded).

**Why it fails**: The C-path audit flagged the lineage-specific origins reading as post-hoc but adequately disclosed (§4.6). C+ now adds a second post-hoc move: extending Paper-2 scope to include *Drosophila* clades flagged by the diagnostic. This is *good practice* for resolving the boundary-artefact ambiguity, but it cumulates with the Layer-4 verdict softening to give the impression that the manuscript is making contingent commitments to Paper 2 in real time. Each individual move is defensible; the cumulative pattern (post-hoc reframe in §4.2 → diagnostic-driven softening in §3.5 → expanded Paper-2 scope in §4.5/§4.7) reads as a paper that is being adjusted to its data. **The Lakatosian concern is sharper now than in C-path**: each adjustment makes the surviving model harder to falsify. RSOS reviewers in evolutionary biology will recognise this pattern.

### 1.7 Deviation row #9 frames the softening as data-driven but does not state the verdict-shifter rule was pre-registered
**Passage**: Deviation row #9 (line 131).

**Why it fails**: The row reads "Optimiser-boundary diagnostic [...] revealed that 2 of 5 production LRT = 0 clades flip to boundary-escape under high $\omega_0$ start." This is honest reporting of the diagnostic outcome. But it does not say whether the pre-reg specified the rule "if optimiser-boundary diagnostic flips the verdict, soften from REFUTED to INCONCLUSIVE." If the pre-reg specified (a) "run diagnostic" and (b) "report outcome but do not change verdict," then the C+ softening is a deviation from the pre-reg analysis plan, not a deviation from a finding. The row should explicitly say either "the pre-reg committed to the diagnostic-as-verdict-shifter rule" or "the verdict-shifter rule was generated by the diagnostic outcome and is therefore a post-hoc analysis rule, deviating from pre-reg." Without this, a reviewer asking "was the rule that flipped the verdict pre-specified?" gets no clean answer.

### 1.8 Carry-forward: §3.6 "Boundary case" subsection title still demotes the strongest Layer-1 evidence
**Passage**: §3.6 line 236 (subsection title).

**Why it fails**: The C-path audit flagged this. C+ has not fixed it. The human MR results (n = 466 SNPs, OR 1.122, $p = 3.1 \times 10^{-31}$) are the most rigorous causal evidence in the paper and are buried under a subsection labelled "Boundary case." The label is semantic confusion (here meaning "instantiation at one phylogenetic tip"); a reviewer will read it as "edge-of-effect / borderline result." **Fix**: rename §3.6 to "Existence at the *Homo sapiens* tip (Layer-1 instantiation)" or "Instantiation in *Homo sapiens*." This is a 30-second fix that has been outstanding through the C-path audit.

### 1.9 Carry-forward: residual A-path framing in §3.5 / §4.4 / §4.5
**Passage**: §3.5 line 234 ("most parsimonious surviving alternative"); §4.4 line 277; §4.5 lines 280–286.

**Why it fails**: The C-path audit flagged 7 sentences for softening. Spot-check of C+ shows §4.4 line 277 has been rewritten to "consistent with parallel functional emergence from non-orthologous parts but cannot statistically establish convergence" — good. §4.5 line 282 has been softened to "consistent with a lineage-specific origins reading, although the model was post-hoc and *Apis* was not specified in advance" — good. But §3.5 line 234 still uses "most parsimonious surviving alternative" framing, which retains the impression that lineage-specific origins is an *empirical conclusion* rather than a *post-hoc residual*. A more defensible word: "the surviving hypothesis-generating reading." Three of the seven C-path-flagged sentences appear to remain.

### Recommendation: **Major Revision** (but on the cusp of Minor)

### Summary for the Editor
The C+ revision has delivered the optimiser-boundary diagnostic that was a "Required Revision" item under the C-path audit, and it has integrated the result with appropriate honesty in the Abstract Conclusion, §3.4, §3.5 verdict table, §4.6, and §4.8. This is a real technical improvement. However, the integration is incomplete: §4.1 still carries the old "partially refuted" verdict word for Layer 4, contradicting the new INCONCLUSIVE label two sections away; the diagnostic was applied only to the 5 LRT = 0 clades but not to the *Apis* production result, which sits in the same boundary-artefact $\omega$ range, creating an asymmetric application that needs either re-running on *Apis* or explicit defence; and the "small-clade boundary-artefact range" is invoked five times but never numerically defined. Three carry-forward items from the C-path audit (IRR, OSF timestamp, §3.6 title) remain. None require re-execution. The paper is closer to submit-ready than at C-path snapshot, but is not yet fully consistent with itself.

---

## 2. Sympathetic Editor — Triage Call (RSOS)

### First 30 Seconds Impression
The Abstract C+ rewrite is editor-friendly. The Results sentence (iii) now reads "After optimiser-boundary diagnostic on the 5 LRT = 0 clades, the production matrix resolves as: 3/6 robustly null, 2/6 optimiser-sensitive, and 1/6 tentative" — this is the kind of sentence that signals technical maturity to an RSOS editor. The Conclusion sentence "does not generate robust positive-selection signal distinguishable from optimiser-boundary artefacts in any tested clade after diagnostic interrogation" is also clean. I would read past the abstract into §3.5, see the verdict table with "INCONCLUSIVE — optimiser-sensitive" prominently displayed, and find this presentation refreshingly honest. The Deviation log row #9 (transparent disclosure of the post-data-collection diagnostic that softened the Layer-4 verdict) is exemplary. *However*: I would also notice §4.1 line 260 still says "partially refuted" for Layer 4, and I would flag that as an integration error before sending to review.

### Three Signals Checked (RSOS criteria)

1. **Scientific validity**: ✅/⚠️ — The pre-registration design is sound; the diagnostic is now delivered (not placeholder); the verdict softening is honestly disclosed in Deviation row #9. The OSF timestamp must be verified, but conditional on that, validity holds. **Improvement vs C-path**: yes — diagnostic delivered.

2. **Technical soundness**: ⚠️ — The diagnostic itself (5 starting $\omega_0$ × 5 clades = 25 runs) follows Yang & dos Reis 2011 minimum protocol. But the asymmetric application (LRT = 0 clades only, not *Apis*) is a technical-soundness concern. The "small-clade boundary-artefact range" invoked five times without numeric definition is a second concern. **Improvement vs C-path**: partial — placeholder concern resolved, but new asymmetry concern emerges.

3. **Adequately reported**: ⚠️ — Deviation log now 9 rows (excellent transparency). FigS1 delivered. But §4.1 vs §3.5 verdict-word inconsistency, IRR still committed-but-undelivered, §3.6 subsection title still misleading, and three flagged A-path-residue sentences remain. **Improvement vs C-path**: partial — FigS1 delivered, but §4.1 verdict-word inconsistency is new.

### Decision: **Send to Review with One-Round Author Revision Before Public Posting**

Three required-revisions items conditional on review (down from C-path's 3 of which 1 is now delivered, plus 2 new):
- (a) Fix §4.1 line 260 verdict word from "partially refuted" to "inconclusive — optimiser-sensitive" (10-second edit; required for internal consistency).
- (b) Either run the optimiser diagnostic on the *Apis* clade with 5 starting $\omega_0$ values, OR explicitly defend in §3.4 / §4.5 why the diagnostic does not apply to non-zero LRT results (this is the single most credible reviewer concern).
- (c) Define numerically the "small-clade boundary-artefact range" in §2.5 and propagate the threshold consistently.
- Carry-forward: confirm OSF timestamp; deliver IRR within 30-day OSF addendum window; rename §3.6.

### Cover Note Draft (if sending to review)

> Dear Drs An and Xi,
>
> Your manuscript "Sweet Trap is widespread but not universal" has been examined by the editorial team. The pre-registered four-layer falsification framework is well-aligned with RSOS's brand, and we particularly appreciate the transparent integration of the post-data-collection optimiser-boundary diagnostic in the new Deviation row #9 and Supplementary Figure S1. Before we send to review, we ask three items: (i) the Layer-4 verdict word in §4.1 line 260 ("partially refuted") is inconsistent with the verdict table in §3.5 ("INCONCLUSIVE — optimiser-sensitive"); please synchronise; (ii) the optimiser-boundary diagnostic was applied to the five LRT = 0 production clades but not to the *Apis* clade, whose foreground $\omega_{2a} = 36.2$ on n = 4 taxa lies in the same boundary range as the two flagged *Drosophila* escapes — please either run the diagnostic on the *Apis* clade or defend the asymmetry explicitly; (iii) the phrase "small-clade boundary-artefact range" is invoked five times without numeric definition; please specify the operational threshold in §2.5.
>
> Once these are received, we will move to public peer review.

---

## 3. Methodological Expert — Audit on Questions 1–6

### Q1 — Does the diagnostic-driven softening introduce HARKing 2.0?

**Verdict: (a) legitimate post-publication-of-deviation correction with one caveat about the verdict-shifter rule's pre-registration status.**

The diagnostic itself was committed in §2.5 of the original protocol ("A randomised-starting-$\omega$ diagnostic is run on every clade returning LRT = 0 to distinguish biological null from optimiser convergence at the boundary") and was previously reported as "Supplementary Figure S1 placeholder" in the C-path audit. Running the diagnostic and getting an outcome that softens the verdict is *not* HARKing — the diagnostic was pre-committed, the result is reported transparently, and the deviation is logged.

**However**: the manuscript does not explicitly state whether the *rule* "if 2/5 LRT = 0 clades flip to optimiser-artefact, soften the Layer-4 verdict from PARTIALLY REFUTED to INCONCLUSIVE" was pre-registered, or whether it is a post-hoc rule generated by the diagnostic outcome. The honest read of Yang & dos Reis 2011 + Anisimova-Yang 2007 is that 2/5 boundary escapes is a strong signal of optimiser instability on this alignment, which arguably *must* trigger a verdict softening regardless of whether the rule was pre-registered. But the manuscript should say this explicitly. Currently Deviation row #9 says "the synthesis 'widespread but not universal' is unaffected (rests on Layer 2 + Layer 3); Layer 4 is now reported as inconclusive" — this *describes* the rule but does not *justify* it as either pre-registered or as a forced consequence of the methodological literature. **One sentence fix in row #9**: "The verdict-shifter rule (≥ 1 of 5 clades flipping to optimiser-artefact softens the Layer-4 verdict to INCONCLUSIVE) was not pre-registered as a numeric threshold but follows from Anisimova-Yang 2007's recommendation that branch-site results from boundary-sensitive optimisations be classified as inconclusive rather than null."

Does §3.4 land the reading "doesn't add 2 confirmed positives — reveals optimizer instability" clearly? **Mostly yes**. §3.4 line 179 says "We therefore treat the *Drosophila* escapes as **optimiser-sensitive results**, not as confirmed positive-selection signals — the only way to distinguish would be expanded-taxon BUSTED / aBSREL / RELAX triangulation, committed for Paper 2." This is the right framing. *But the same paragraph also says* "*Apis* result, with $\omega_{2a} = 36.2$ on $n = 4$ taxa, is now one of three boundary-range escapes among six tests rather than a unique exemplar" — which subtly argues *Apis* is *less* of an outlier now. The two framings ("escapes are not positives" + "*Apis* is no longer a unique exemplar") together tilt the reading slightly toward "*Apis* is more credible because it has company," which is not what the data show. The data show *all three escapes are equally suspect*; the right reading is that *Apis* is no more nor less credible than before, and what changed is that the 5/6 = 0 picture is now 3/5 robust-null + 2/5 optimiser-artefact. **Score**: 80% honest, 20% tilted toward "lineage-specific origins becomes more credible because the Layer-4 picture is messier."

### Q2 — Is "widespread but not universal" still coherent after Layer-4 softening?

**Verdict: defensible but requires the §4.1 fix to be fully internally consistent.**

§3.5 explicitly anchors the synthesis on Layers 2 + 3 (line 225). This is a legitimate rhetorical move — RSOS allows the authors to specify which evidence carries the conclusion, and "K = 0.117 + Jaccard = 0 against null = 0.9998" is independently sufficient to refute the universality reading. The Layer-4 softening removes Layer 4 as load-bearing but does not subtract from Layers 2 + 3.

**Cherry-picking concern**: a reader can ask "if Layer 4 had come out as supported, would the manuscript still claim Layer 2 + 3 are sufficient, or would it have integrated Layer 4 into the universality reading?" The honest answer (Layer 4 was always one of three universality predictions and a positive Layer 4 would have *complicated* the not-universal verdict) is that no, the manuscript would have had to grapple with it. So the Layer-4 ducking is conditional on the Layer-4 outcome being non-confirmatory — which it is. This is acceptable Popperian practice but it should be acknowledged. **Suggested addition to §3.5**: "Layer 4 is uninformative on universality regardless of polarity: a robust positive across multiple clades would have been confirmatory, a robust null would have been refutatory, but the diagnostic-revealed inconclusiveness places Layer 4 outside the inference burden for either direction."

The §4.1 line 260 inconsistency (still "partially refuted") undercuts this rhetorical move. Until §4.1 is fixed, the synthesis claim is internally incoherent.

### Q3 — Does "three boundary-range escapes" weaken the Apis story honestly or dishonestly?

**Verdict: honestly, on net, with one rhetorical lean.**

The framing "*Apis* is the most conservative of three boundary escapes" (§4.5 line 286) is the natural reading of the diagnostic data. *Apis* has the smallest $\omega$ and smallest n among the three; this is descriptively accurate. And the manuscript is honest that *Apis* should also be subjected to BUSTED/aBSREL/RELAX in Paper 2.

**The dishonest-tilted reading**: the three-boundary-escapes framing implicitly *normalises* the *Apis* result — by saying "*Apis* sits among three boundary escapes, not alone," it removes *Apis* from the spotlight. A pure-honest framing would say: "all three non-zero LRTs in Layer 4 are equally suspect; *Apis* is not less suspect because there are now two more like it." The current framing leans toward the former by 10–15%.

The Texas Sharpshooter concern from the C-path audit (§4.5 still uses *Apis* as the predicted signature of the lineage-specific origins model) is *not addressed* by C+. *Apis* still serves as exemplar for the post-hoc lineage-specific reading, and now also serves as the most-conservative-of-three-boundary-escapes — *Apis* is now doing double duty as both exemplar and conservative case, which compounds rather than resolves the original Sharpshooter concern.

**Net assessment**: 75% honest, 25% rhetorical tilt. Fixable by adding one sentence to §4.5: "We do not claim *Apis* is more credible than the *Drosophila* escapes; all three lie in the same boundary range, and *Apis*'s priority in the lineage-specific origins reading rests on its biological coherence (Hymenopteran nectarivory) rather than on any statistical advantage."

### Q4 — Is FigS1 self-explanatory?

**Verdict: Panel A yes, Panel B partially.**

Panel A (5 × 5 LRT heatmap): clean, readable, colour-coded. A reviewer reading only the figure caption can see at a glance: 3 clades (Lepidoptera, Coleoptera, Aedes) are uniformly LRT = 0 across all 5 starting $\omega_0$ values; 2 clades (D. mel. Gr64 cluster, D. mel. all-Grs) escape only at $\omega_0 = 5.0$; one cell (Gr64 cluster, $\omega_0 = 2.0$) is NA. The "[NULL]" / "[ART.]" labels on the y-axis tags clades by verdict, which makes the artefact-clades visually distinct. **Standalone-readable**: yes.

Panel B ($\omega_{2a}$ vs $\omega_0$ scatter): readable but the artefact-band annotation is text-only, not visually rendered. A viewer can see two pink/green divergent traces and three flat traces — but the question "which $\omega_{2a}$ values count as boundary artefact?" is answered only by squinting at the right-side caption text "Small-clade boundary-artefact range (Anisimova & Yang 2007)" which is positioned next to (not on) the band. The plot has the data but lacks a shaded rectangle delineating the artefact zone. **Standalone-readable**: 70%.

**Test against the audit criteria**:
- (a) See that 3 clades are robust-null, 2 are optimiser-sensitive: ✅ via Panel A y-axis labels and uniform-zero rows.
- (b) Understand the boundary-artefact range: ⚠️ — caption mentions it, plot does not visually demarcate.
- (c) Recognize that escape at $\omega_0 = 5.0$ only is the diagnostic flag: ✅ via Panel A column-5 highlighting and Panel B traces that diverge only at $\omega_0 = 5.0$.

**Fix**: add a horizontal grey band in Panel B from $\omega_{2a} = 30$ (or whichever threshold the §2.5 fix sets) upward, labelled in-figure "boundary-artefact range." This would close the gap.

### Q5 — Methodological expert checks

**Power**: with 3 robust-null + 2 optimiser-sensitive + 1 tentative (also boundary), the universal-positive prediction is *not testable on this dataset*. The §4.6 closing paragraph says exactly this ("the Layer-4 universality test is therefore inconclusive between true biological null and insufficient method power") and §4.8 closing one-sentence ("the testable refinement for Paper 2 is therefore not just 'is selection present in these clades' but 'is our test powerful enough to detect it'"). Both statements are correct and stronger than what the C-path admitted. **However**, a stronger admission would be: "the test as deployed cannot resolve the universality question on this dataset; only the cross-phylum K and the Pfam-Jaccard null are bearing inference weight." This is more brutally honest than "the failure mode is insufficient method power" because it concedes the *test was the wrong tool for the question on this alignment*. The current §3.5 line 225 ("the failure mode is insufficient method power on this alignment, not confirmed absence of selection") gets 80% there. Verdict: **adequate; could be stronger**.

**Diagnostic adequacy**: 25 runs (5 × 5) is the minimum recommended by Yang & dos Reis 2011. Going to 7 starting $\omega_0$ values × 5 clades = 35 runs would not change the substantive outcome (the 2 escape clades both escape only at $\omega_0 = 5.0$; intermediate values yield the same boundary as $\omega_0 = 0.1, 0.5, 1.0, 2.0$). **5 starting points is sufficient by methodological consensus**. Whether 5 *clades* is adequate: the diagnostic was applied to all 5 LRT = 0 clades, so coverage is complete for that subset. The asymmetry is that *Apis* (the non-zero result) was not subjected to the diagnostic. This is the single biggest methodological loose end. **Verdict**: 5 × 5 is sufficient for what was tested; the omission of the Apis clade is the gap.

**Statistical claim discipline**: the verdict label "INCONCLUSIVE — optimiser-sensitive" is *not* standard PAML phrasing — Yang's textbook and the PAML documentation use "boundary effects on $\omega$ estimation" or "non-convergence of MLE optimisation." But "INCONCLUSIVE — optimiser-sensitive" is operationally clear and does not prejudice the reader. A reviewer might mark it for terminology consistency but not for content. **Verdict**: idiosyncratic but defensible.

**FigS1 reproducibility**: the optimizer_diagnostic.csv + 25 per-run codeml directories + orchestrator_log + the figure script (not yet inspected) form a reproducible package *if* the figure script is included in the GitHub deposit. **Verdict**: presumed reproducible pending GitHub upload at acceptance; adequate for submission.

### Q6 — Carry-forward from C-path audit

| Item | C-path status | C+ status | Action needed |
|---|---|---|---|
| OSF pre-reg content vs claim | flagged, pending Andy verification | unchanged — still pending | Andy must verify osf.io/pv3ch contents pre-submission |
| External-coder Fleiss κ | committed as 30-day OSF addendum | unchanged | Acceptable to submit with this commitment |
| Residual A-path language | 7 sentences flagged | 4 of 7 fixed; 3 still residual (§3.5 line 234, §4.1 line 260, §4.5 line 286) | Fix the 3 remaining |
| §3.6 subsection title | flagged | unchanged | 30-second rename |
| Layer-2 strong-floor accounting | flagged | unchanged | Add one sentence to §3.2 distinguishing ordinary-vs-strong falsification on K = 0.117 |
| Pfam-null parameter universe | flagged | unchanged | Specify in Supplementary Methods |

### Q7 — RSOS-specific final readiness

**Abstract length**: RSOS allows up to 200-word structured abstracts (no hard character limit). Current abstract is ~480 words across Background/Question/Approach/Results/Conclusion + Keywords. **This is over RSOS's typical guidance of 200–300 words for structured abstracts.** A reviewer or editor will flag this as needing a trim. **Estimated trim required**: cut ~150 words, primarily from the Results paragraph (which is currently ~200 words alone).

**Figure legends**: Figures 1–5 + FigS1. Spot-check: Figure 1 caption (line 251) is two sentences and reads as standalone — ✅. Figure 2 caption (line 152) has four panels described with the K = 1.446 within-Arthropoda subset annotated — ✅. Figure 3 caption (line 172) covers three panels with the Jaccard = 0 / null = 0.9998 annotation — ✅. Figure 4 caption (line 222) covers four panels (gene tree + LRT forest + BEB + hummingbird inset) — ✅. Figure 5 caption (line 253) describes the integrated verdict but uses "1-of-6 *Apis*-only positive-selection footprint (Layer 4 partially refuted)" — ⚠️ this is the *old* "partially refuted" verdict word and is inconsistent with the new INCONCLUSIVE label. **Fix**: Figure 5 caption needs updating to match §3.5 verdict table. FigS1 caption: covers Panel A heatmap and Panel B scatter — ✅ for Panel A, partial for Panel B (the artefact band is described but not visually rendered, see Q4).

**Cover letter P2 results-summary**: not seen by this audit; if the cover letter still describes Layer 4 as "partially refuted," it must be updated to "inconclusive — optimiser-sensitive" to match the C+ manuscript. **Andy should sweep the cover letter for verdict-word consistency.**

**Deviation log row #9 audit-readability**: the row clearly states the deviation, the reason, and the manuscript scope impact. A reviewer can audit it. **Verdict**: well-worded; passes the audit-readability test.

### Verdict
**Needs patching** (not re-execution). Six items: (1) Fix §4.1 line 260 verdict word; (2) run optimiser diagnostic on the *Apis* clade OR defend the asymmetry; (3) numerically define the "small-clade boundary-artefact range" in §2.5 and propagate; (4) update Figure 5 caption to match §3.5 verdict table; (5) trim abstract to ~250 words for RSOS guidance; (6) carry-forward C-path items (§3.6 title rename, 3 residual A-path-language fixes, OSF timestamp verification, IRR commitment statement). Items (1), (3), (4), (5), (6) are revision-class. Item (2) is the only one that requires re-running compute, and even there the alternative ("defend the asymmetry") is text-only.

---

## 4. Items Still Requiring Fix Before Submit

**P0 (must fix; 30 min total work)**:
1. §4.1 line 260: change "**partially refuted** (1/6 clades tentative; 5/6 LRT = 0)" → "**inconclusive — optimiser-sensitive** (3 robustly null; 2 optimiser-sensitive; 1 tentative in boundary range)."
2. Figure 5 caption: change "(Layer 4 partially refuted)" → "(Layer 4 inconclusive — optimiser-sensitive)."
3. §3.5 line 234: soften "most parsimonious surviving alternative" → "the surviving hypothesis-generating reading."
4. §3.6 subsection title: rename "Boundary case: existence in *Homo sapiens*" → "Existence at the *Homo sapiens* tip (Layer-1 instantiation)."
5. Abstract: trim from ~480 words to ~250–300 words for RSOS structured-abstract guidance.

**P1 (strongly recommended; 1–2 hours work)**:
6. §2.5: define "small-clade boundary-artefact range" as a numeric threshold (e.g., $\omega_{2a} > 30$ on $n \le 6$-taxon foregrounds) with citation; propagate to §3.4, §3.5, §4.5, §4.6.
7. §4.5 line 286: add one sentence — "*Apis*'s priority in the lineage-specific origins reading rests on biological coherence (Hymenopteran nectarivory), not statistical advantage; all three boundary escapes are equally suspect."
8. Deviation row #9: add one sentence on whether the verdict-shifter rule was pre-registered or follows from Anisimova-Yang 2007 by methodological convention.
9. FigS1 Panel B: add shaded grey band over the boundary-artefact $\omega_{2a}$ range.
10. Sweep cover letter for verdict-word consistency ("partially refuted" → "inconclusive — optimiser-sensitive").

**P2 (Andy decision)**:
11. Run optimiser diagnostic on the *Apis* clade (5 starting $\omega_0$ × 1 clade = 5 codeml runs, ~3 wall-hours). If the *Apis* result also escapes only at high $\omega_0$, the manuscript can reclassify *Apis* as also optimiser-sensitive (cleaner story, more brutally honest). If it does not escape, *Apis* survives as the *only* non-boundary-suspect signal and the lineage-specific story strengthens.

**P3 (carry-forward, acceptable as OSF addendum or Paper-2 commitment)**:
12. OSF pre-reg timestamp + content verification (Andy task).
13. Three-coder Fleiss κ delivery (committed as 30-day post-acceptance addendum).

## 5. Items Deferrable to OSF Addendum / Paper 2

- Inter-rater Fleiss' κ on 30%-subset (committed; 30-day OSF addendum window).
- BUSTED / aBSREL / RELAX triangulation on *Apis* + *Drosophila* clades (Paper 2).
- PGLS-adjusted phylogenetic signal (Paper 2).
- Extension of H_universal_2 to olfactory / opioid / photoreceptor / cognitive-reward families (Paper 2).
- Lineage-specific origins quantitative falsification predictions (Paper 2 pre-registration).
- Pfam-null parameter universe sensitivity analysis (could go into Supplementary Methods or OSF data dictionary).

## 6. Acceptance Probability Post-Revision at RSOS

**Acceptance-of-revised-version probability: 65–75%** at RSOS (vs C-path's 60–70%).

The C+ manuscript is genuinely improved on RSOS technical-soundness criterion: the diagnostic is delivered, Deviation row #9 is exemplary, Abstract Conclusion is C+-consistent. Conditional on:
- (a) OSF pre-registration timestamp verified;
- (b) §4.1 verdict-word fix + Figure 5 caption fix (both 30-second edits);
- (c) Either the *Apis* diagnostic re-run OR the asymmetry defended in text;
- (d) "Small-clade boundary-artefact range" numerically defined;
- (e) Abstract trimmed to RSOS guidance;
- (f) IRR delivered within 30 days post-acceptance,

acceptance probability rises to **75–82%**.

If submitted as-is (with §4.1 inconsistency unfixed), acceptance drops to **40–50%** — the internal contradiction will be a focused reviewer concern and may trigger another round.

## 7. Bottom-Line Verdict: **FIX-AND-SUBMIT**

The manuscript is *not* submit-ready as of this audit timestamp because of the §4.1 / Figure 5 / abstract-length inconsistencies. None of the fixes require re-execution; all are revision-class, and the P0 fixes total under 30 minutes of editing. With those P0 fixes applied, the manuscript clears the RSOS technical-soundness threshold and is genuinely better than the C-path snapshot — the diagnostic is delivered, the verdict is honestly softened, the deviation log is exemplary. The asymmetric application of the diagnostic (Apis vs LRT-zero clades) is the one substantive concern that is worth a 3-hour compute investment to close, but text-only defence is adequate as a fallback.

---

## Final Synthesis: Bottom Line for the Author

The C+ revision is a real technical improvement over C: the optimiser-boundary diagnostic that was a placeholder is now delivered, its outcome is honestly integrated into the Layer-4 verdict, and the synthesis is clean about what evidence is now load-bearing (Layers 2 + 3, not Layer 4). But the integration is incomplete — §4.1 still carries the old "partially refuted" verdict word, contradicting §3.5 two pages later; Figure 5 caption still uses the old verdict word; the diagnostic was applied asymmetrically (LRT = 0 clades, not *Apis*); and the "small-clade boundary-artefact range" is invoked five times without numerical anchor. Five P0 edits totalling ~30 minutes will close all consistency gaps. The harder methodological loose end — running the diagnostic on the *Apis* clade for symmetric application — is a 3-hour compute job that, if completed, would convert this from FIX-AND-SUBMIT to SUBMIT-READY with high confidence. Without it, the paper is still defensible but invites a focused reviewer concern that text-only defence will need to absorb.

---

*Red-Team Review v1.2 — Stage 7 C+ post-diagnostic-integration audit, 2026-04-26*
