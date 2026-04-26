# B 路径论文骨架预览（不动主稿）

**目的**：让 Andy 在切换前先看到 B 路径的 Abstract + §1 + 结构骨架长什么样，再决定是否动主稿。
**对比基线**：A 路径 = 现行 manuscript.md (Sweet Trap 4-part evidence architecture, eLife RPP)
**B 路径假设目标刊**：Proc R Soc B / Evolution Letters（其次 Evolution / Am Nat）

---

## 1. Working Title

> **Cross-phylum convergence and within-arthropod phylogenetic reinforcement of reward–fitness decoupling: a 56-species comparative test**

备选：
- "Reward-driven maladaptive behaviors are convergent across animal phyla but phylogenetically structured within arthropods"
- "Convergent rather than inherited evolution of reward–fitness decoupling: evidence from 56 species across seven phyla"

---

## 2. Abstract（约 230 词）

Reward-driven behaviors that decouple sensory-reward signals from realized fitness — from sucrose-laden traps that exploit insect gustation to artificial-light disorientation in moths — are repeatedly described in single-clade comparative studies, but their evolutionary origin remains untested at the cross-phylum scale. Two hypotheses compete: (i) **inheritance** of an ancestral reward–fitness coupling rule that has eroded along specific lineages, predicting positive phylogenetic signal in the magnitude of decoupling (Δ_ST); or (ii) **convergence**, in which decoupling arises independently in lineages that share ecological exposure to mismatched reward cues, predicting weak phylogenetic signal cross-phylum but possibly strong signal within tightly nested clades.

We assembled a PRISMA-screened dataset of **114 cross-species cases of reward–fitness decoupling spanning 7 phyla and 56 species**, each scored on four operationalised criteria (F1–F4) and a continuous Δ_ST proxy. Time-calibrated phylogenetic signal analysis (TimeTree 5; Blomberg K, Pagel λ, Moran's I, 9,999 permutations) recovered a **null cross-phylum signal (K = 0.117, 95% CI [0.056, 0.169], p = 0.251)** but a **strong within-Arthropoda signal (K = 1.45, p = 0.007; n = 13)**. To probe the molecular basis of the within-arthropod pattern, we ran a PAML branch-site test on the gustatory-receptor (Gr) family across 38 insect orthologs and detected lineage-specific positive selection in the **Apis mellifera sweet-receptor clade (LRT = 9.92, p = 8.2 × 10⁻⁴, ω = 36.2)**, replicating Baldwin et al. (2014) for the hummingbird TAS1R1 positive control (LRT = 55.9).

Our results favour the **convergence + within-clade reinforcement** hypothesis: reward–fitness decoupling is not an inherited trait but a recurrently re-derived ecological vulnerability, with phylogenetic structuring emerging only inside clades that share both gene-family architecture and selective regime. We discuss implications for comparative behavioural ecology, the limits of "Sweet Trap" as a unified construct, and a roadmap for independent-sample replication.

---

## 3. Introduction outline (§1, 约 1100 字 → 约 6 段落)

**P1. Opening paradox.**
Reward circuits should track fitness — natural selection should align valence with payoff. Yet across animals, cases accumulate where the alignment fails: moths circle artificial lights, cane toads consume toxic prey-mimics, kestrels overfeed on subsidised carrion, humans over-consume ultraprocessed food. *Anchor citations*: Robertson 2009 (ALAN); Hopkins 2011 (cane toads); Schlaepfer 2002 (ecological traps); Hall 2018 (UPF).

**P2. Two competing evolutionary explanations.**
Are these failures **homologous** — degenerate copies of an ancestral reward–fitness coupling that erodes along specific lineages? Or **convergent** — repeatedly re-derived in clades that share ecological exposure to mismatched cues, regardless of phylogenetic distance? The two hypotheses make opposite predictions about how decoupling magnitude is distributed on the tree of life. *Anchor citations*: Stern 2013 (convergence as null); Losos 2011 (convergent vs parallel); Conway-Morris 2003; Speed & Arbuckle 2017 (statistical tests of convergence).

**P3. Empirical gap.**
Despite the theoretical sharpness of this question, no published work has tested the homology-vs-convergence axis at cross-phylum scale for reward-driven maladaptive behaviour. Existing work is either (i) within-clade comparative (Robertson & Wanner 2006 on Hymenoptera Gr contraction; Anctil 2009 on cnidarian aminergic systems), (ii) single-mechanism (Baldwin 2014 on hummingbird umami→sweet); or (iii) phenomenological without phylogenetic statistics (most ALAN/UPF/ecological-trap reviews). The required dataset — a phylum-spanning, criterion-coded set of cases anchored to a time-calibrated tree — has not been built.

**P4. What this paper does.**
We assemble that dataset (114 cases / 56 species / 7 phyla, PRISMA-screened, F1–F4 + continuous Δ_ST proxy). We test phylogenetic signal cross-phylum and within each major clade, and probe the molecular signature of the strongest within-clade signal using a branch-site selection test on the gustatory-receptor family. Hypothesis structure: H₁ (inheritance) predicts K > 0.30 cross-phylum; H₂ (convergence) predicts K ≈ 0 cross-phylum with possible K > 1 inside clades sharing both gene-family architecture and selective regime.

**P5. What we find (preview).**
Cross-phylum signal is null (K = 0.117); within-Arthropoda signal is strong (K = 1.45); a single-clade branch-site signal in the *Apis* sweet-receptor clade is consistent with the within-Arthropoda reinforcement pattern but rests on n = 4 taxa and is reported as suggestive rather than decisive. The ensemble pattern favours **convergence + within-clade reinforcement** over **inheritance**.

**P6. What we do not claim.**
We do not introduce a new evolutionary construct. The "Sweet Trap" naming convention some prior work has applied to this phenomenon (Δ_ST = U_perc − E[U_fit | B]) is logically equivalent to the H₂ convergence framework and is treated in §4.5 as a candidate descriptive label, not a tested entity. We also do not claim the *Apis* signal generalises beyond Hymenoptera; replication on Apis–Bombus–Vespa (n ≥ 10) is reserved for a follow-up paper.

---

## 4. Section structure (vs A path)

| § | A 路径（当前） | B 路径（拟议） | 主要变化 |
|---|---|---|---|
| §1 Intro | Sweet Trap 构念 + 4-part architecture | 收敛 vs 继承 + 实证缺口 | 主题完全更换；构念退到 §4.5 |
| §2 Methods | Part 1-4 并列 | (a) PRISMA + Δ_ST 编码 (b) phylosig (c) branch-site | 删 Part 1 MR 至 supplementary；删 Part 3 Pfam 至 supplementary |
| §3.1 Results | Part 1 MR 4 pairs × 3 ancestries | **Cross-phylum null (K=0.117)** | 头条数据从 MR 换成 phylosig |
| §3.2 Results | Part 2 PRISMA 114 cases | **Within-clade signal (K=1.45 Arthropoda)** | 升级 H3 为主结果 |
| §3.3 Results | Part 3 Tier-1/Tier-2 architecture | ***Apis* Gr branch-site case study** | Apis 信号从 Part 4 副结果升为正文 case study |
| §3.4 Results | Part 4 H6a SUPPORTED | **Robustness**：PGLS / Moran's I / 子集复测 / Pfam null baseline | Pfam null baseline 直接进正文，不藏 supplementary |
| §3.5 | Integrated 4-part architecture | （删除） | B 路径不需要 integrated section |
| §4.1 Disc | Headline finding (convergence) | Headline + boundary conditions | 简化 |
| §4.2 | H3 reframe | **Convergence vs inheritance: theoretical implications** | 升级 |
| §4.3 | H4a DRD conservation | Phylogenetic comparative methods 在 behavioral ecology 的限制 | 重构 |
| §4.4 | H4b Class-A GPCR | Apis Gr 的 mechanistic prediction (Robertson-Wanner 2006 框架) | 收紧 |
| §4.5 | H6a Apis | **"Sweet Trap" as candidate descriptive label**：构念退场段 | **新段落**（关键诚实点） |
| §4.6 | Limitations | Limitations（含 single-clade Apis、114-case adequacy、PCM 假设） | 扩充 |
| §4.7 | Future directions | Paper 2: Apis-Bombus-Vespa replication + olfactory/opioid 扩展 | 收紧 |
| §4.8 | Conclusion | Conclusion | 单段 |

**篇幅**：B 路径 body 约 4500-5000 词（vs A 路径 4972）；图减为 3 张主图（Fig 2 phylosig + Fig 4 Apis branch-site + 1 张新 Fig 1 概念框架=H₁ vs H₂）。

---

## 5. 数据-章节映射：保留 / 退后 / 删除

### 保留（升级为主结果）
- Part 2 PRISMA 114 cases / 56 species / 7 phyla → §2 + §3.1 + §3.2
- H3 phylosig 主结果 + 子集 (Chordata / Chord+Arth / Arth-only) → §3.1 + §3.2
- Apis Gr clade branch-site (LRT=9.92, ω=36.2) + Baldwin 阳性对照 → §3.3
- 时间校准树 (TimeTree 5) + Δ_ST 编码本 → §2 Methods + Supplementary

### 退后（保留但降级到 Supplementary）
- Part 1 Trans-ancestry MR (4 reward pairs × 3 ancestries) → Supplementary §S3，作 "human direction-of-effect 初步证据"，不在 Abstract 出现
- Part 3 Tier-1/Tier-2 architectural consistency → Supplementary §S4，标注 "descriptive architectural summary; statistical convergence claim cannot be made under Pfam null baseline (P(Jaccard=0|null)=0.9998)"
- Pfam null baseline 分析 → Supplementary §S5（同时也作为 §3.4 Robustness 一段引用）
- Cnidarian DA-R BLASTP confirmatory → Supplementary §S6 + §4.6 一句话

### 删除（不要再写到论文里）
- Sweet Trap 4-part evidence architecture 整体框架（包括 Δ_ST = U_perc − E[U_fit | B] 的公式化包装、A1-A4 公理体系、F1-F4 编码与构念绑定的部分）→ 只在 §4.5 一段提到
- "Convergent evolution onto functionally equivalent reward architectures" 这类强声明 → 全部砍掉
- 5/6 production clades LRT=0 的含糊声明 → 直接说 "Apis is the only clade with detectable signal in our test matrix; remaining clades return null at our power"
- "Two-tier architectural claim" → 删

---

## 6. Anchoring literature (B 路径骨架引用)

理论 / 概念：
- Stern DL (2013) The genetic causes of convergent evolution. *Nat Rev Genet* 14:751-764.
- Losos JB (2011) Convergence, adaptation, and constraint. *Evolution* 65:1827-1840. ✓ 已在 bib
- Conway Morris S (2003) *Life's Solution*. Cambridge.
- Speed MP & Arbuckle K (2017) Quantification provides a conceptual basis for convergent evolution. *Biol Rev* 92:815-829.

PCM 方法：
- Felsenstein J (1985) Phylogenies and the comparative method. *Am Nat* 125:1-15.
- Blomberg SP, Garland T, Ives AR (2003) Testing for phylogenetic signal in comparative data. *Evolution* 57:717-745. ✓ 已在 bib
- Pagel M (1999) Inferring the historical patterns of biological evolution. *Nature* 401:877-884. ✓ 已在 bib
- Münkemüller T et al. (2012) How to measure and test phylogenetic signal. *MEE* 3:743-756. ✓ 已在 bib

Apis Gr / sweet-taste 收敛：
- Robertson HM & Wanner KW (2006) The chemoreceptor superfamily in the honey bee Apis mellifera. *Genome Res* 16:1395-1403. ✓ 已在 bib
- Baldwin MW et al. (2014) Evolution of sweet taste perception in hummingbirds. *Science* 345:929-933. ✓ 已在 bib

现象 anchors（保持不变）：
- Hopkins GR et al. 2011; Robertson BA et al. 2009/2013; Schlaepfer MA 2002 ✓ 应在 bib

**估计需新增 bib 条目**：3 个（Stern 2013, Conway-Morris 2003, Felsenstein 1985）。其余已有。

---

## 7. B 路径的 honest claims（vs A 路径）

| 主张 | A 路径 | B 路径 |
|---|---|---|
| 跨物种现象普适性 | "Sweet Trap 在人类+全物种普适" | "reward-fitness decoupling 在 7 phyla / 56 species 都有报告" |
| 收敛性 | "Tier-1/Tier-2 architectural convergence" | "phylogenetic signal cross-phylum is null; consistent with convergence not inheritance" |
| 选择信号 | "H6a SUPPORTED via Apis clade" | "*Apis* Gr clade shows lineage-specific positive selection (suggestive, n=4)" |
| 构念新颖性 | "Sweet Trap as unified evolutionary construct" | "We do not introduce a new construct; we test convergence vs inheritance" |
| MR 因果链 | Part 1 占 §3.1 头条 | Supplementary 一段 "human direction-of-effect 旁证" |
| 4-part architecture | 整本论文骨架 | 不出现 |

---

## 8. 风险评估（B 路径）

**好处**：
1. **完全符合 Andy memory 里"诚实评估"+"不强塞构念"的偏好**
2. **Hostile-audit 三大致命缺陷自动消解**：构念-分子 mismatch 不存在了；H3 不再 HARK；Apis 边际化合理
3. **方法-论题匹配**：phylogenetic comparative methods 用在 phylogenetic comparative paper 上
4. **接受率提升**：Proc R Soc B / Evolution Letters 接受率（30-40%）远高于 eLife RPP 公开评审的"过审 + 评分两轮"（实质 desk-reject 风险 + 公开评审接受率叠加 < 30%）

**代价**：
1. **目标刊降档**：从 eLife（IF≈8）→ Proc R Soc B（IF≈4.7）/ Evolution Letters（IF≈3.4）
2. **构念资产 sunk cost**：bioRxiv priority preprint + OSF 预注册 + 14 天工作的 Sweet Trap framing 不再是头条；只能作为 §4.5 一段
3. **冲量降低**：B 路径论文不会变成"talk of the town"，更接近一个 solid 但 narrow 的实证 paper
4. **Paper 2 战略受影响**：如果 Paper 2 想用 Sweet Trap 整合多个 reward modality，则 Paper 1 必须保留构念背书；B 路径切走构念后，Paper 2 必须重新 anchoring

**Paper 2 的可能性（B 路径下）**：
- B-后续 1：Apis-Bombus-Vespa n≥10 的 H6a 独立样本复测（confirmatory paper）
- B-后续 2：扩展 olfactory + opioid 受体到 phylosig 测试，验证收敛是否扩展到其他 reward modality
- B-后续 3：构念论文（"Sweet Trap as a unifying framework"）独立成篇，不依赖 PCM，投行为生态学/进化心理学刊

---

## 9. 决定标准

如果 Andy 同时满足以下三条，建议切 B：
1. 优先级是"诚实 + 实在的发现"而非"构念资产 + 高刊"
2. 接受目标刊降到 Proc R Soc B / Evolution Letters
3. 同意 Paper 2 走"独立复测 + 多 modality 扩展"路径（而非"Sweet Trap 大一统"路径）

如果其中任一条不成立，A 路径（已 hostile-audit 整改）仍是合理选择，只是需要 Paper 2 的 K 独立重测来 retroactively 补救 H3 HARKing。

---

## 10. 切换成本（如果 Andy 决定走 B）

- Abstract + §1 完全重写：约 2 小时
- §2 Methods 重组（删 MR 部分到 supplementary）：约 1 小时
- §3 Results 重组（重新排序 + 新增 Pfam null baseline 段）：约 2 小时
- §4 Discussion 重写（含 §4.5 构念退场段）：约 2 小时
- 删 Fig 1（Sweet Trap 概念图）+ 重制成 H₁ vs H₂ 图：约 1 小时
- Fig 5（integrated）作废
- references.bib 增减：约 30 分钟
- 新一轮 hostile-audit + lint + make：约 1 小时

**总切换成本：约 9-10 小时单 agent 时间**（可分散到 2-3 个并行 agent，2-3 小时实墙时间）。

---

*下一步等 Andy 决策：[A 提交] / [B 切换] / [先看 B-Abstract 改写后再决定]。*
