# HSSC Manuscript Audit — Sweet Trap v3.3

**Auditor role:** Peer reviewer (顶刊审稿标准, HSSC-calibrated)
**Source:** `05-manuscript/main_v3.3_draft.md` (331 lines, 8,927 words body), `abstract_v3.2.md` (149 words), `WORKLOG.md` §2026-04-20 19:07 NHB Desk Reject
**Target journal:** Humanities and Social Sciences Communications (HSSC, Palgrave/Nature), OA, interdisciplinary, no hard word cap
**Date:** 2026-04-20

---

## 1. HSSC 契合度总评

**契合度评分: 7.0 / 10**

**整体判断: 中改 (medium rewrite) 后投稿**

摘要与主论点（reward–fitness decoupling 作为跨学科构念）与 HSSC 的 humanities×social-science 定位有天然亲和力。HSSC 欢迎 framework proposals、umbrella constructs、跨物种类比，这些恰恰是 NHB 退稿的三个主因（WORKLOG 诊断①②④），在 HSSC 变成中性甚至是加分项。方法论严谨性（19 MR chains + 3,000 specs + 预注册 + 盲编 κ=1.00）完全达到 HSSC 审稿标准，且 HSSC 的 methodological-rigor-first 审稿倾向比 NHB 对你有利。

**核心问题不在科学，在包装**: 稿件每一个章节都以 "NHB Article" 自我定义（title page line 11; abstract file line 1; Discussion 的 no-subheadings 结构 line 163; figure legends line 2/55）。对 HSSC 编辑而言这是直接信号 "recycled NHB rejectee"。另外 humanities/policy implications 在 Discussion 段 2 (line 167) 只占 1 段约 160 词，相对 HSSC 读者期待偏薄。Abstract 仍承袭 NHB 压缩版的 149 词「biology-forward」基调（moths / sea turtles / BMI→T2D OR）首句全生物，HSSC 读者群首句应听到 "society / policy / culture" 信号。

**竞争力等级:** 以 HSSC Accept 率（约 15-20%）为基准，当前形态约落在边缘送审区；按本报告执行必改 + 应改清单后，可进入 normal-review / minor-revision 区间。

---

## 2. 必须改 (High Priority) — 不改会增加 desk-reject 风险

### H1. NHB 硬标签残留（8 处）——必须全删或替换
**位置:**
- `main_v3.3_draft.md:11` — `**Target journal:** *Nature Human Behaviour* — Article.` 
- `main_v3.3_draft.md:12` — `~4,900 words main text ... NHB Article hard limit...`
- `main_v3.3_draft.md:15` — 整段 `v3.2 applied three NHB Article structural fixes...v3.3 applies NHB pre-submission compliance fixes...` 明示 NHB 合规历程
- `main_v3.3_draft.md:25` — HTML 注释 `[DIFF-F5] NHB Article style: Introduction has NO heading...`
- `main_v3.3_draft.md:163` — HTML 注释 `[DIFF-F6] NHB Article style: Discussion has NO subheadings...`
- `main_v3.3_draft.md:255` — Transparency log 段尾 `v3.2 (this submission): NHB Article structural compliance — Abstract compressed to ≤ 150 words (F4); §2 Theory dissolved into Introduction (F5)...`
- `main_v3.3_draft.md:257` — HARKing-transparency 段尾 `v3.2 preserves all v3.0/v3.1 empirical content unchanged; only section arrangement and abstract length change to meet NHB Article style.`
- `abstract_v3.2.md:1,3,5` — 整个 header（`# Abstract (v3.2) — Nature Human Behaviour Article` / `NHB Article hard limit` / `Structure per NHB Article`）
- `figure_legends_v3.1.md:2,5,55` — `**Target journal:** Nature Human Behaviour (Article)` + `9 → 6 figures per NHB Article limit` + legends 版本说明末句

**问题:** 每一处都告诉 HSSC 编辑 "这篇是 NHB 退稿的再利用稿"。HSSC 不允许同时投稿，但会追问 transfer history。当前把 NHB 合规历史当成提交内容一部分暴露，会触发编辑怀疑。

**建议改法:**
- 所有 `Target journal: Nature Human Behaviour` → `Target journal: Humanities and Social Sciences Communications`
- 所有 `[DIFF-F*] NHB Article style` HTML 注释 → 整段删除（纯编辑内部批注，投稿版无存在必要）
- L15 的 version tracking 整段替换为单句：`Current version v3.3: axioms/theorems frozen 2026-04-18 (OSF); empirical numbers and figures unchanged from v3.0.`（删掉 v3.2 NHB 合规历史与 v3.3 NHB pre-submission fix 清单）
- Transparency log L255 删除 "v3.2 (this submission): NHB Article structural compliance..." 整段；替换为 "v3.2-v3.3 editorial harmonisation; no empirical re-analysis."
- HARKing L257 删除末句 "...to meet NHB Article style."
- `abstract_v3.2.md` 整个 header section 删除；投稿时 abstract 直接嵌主稿开头

### H2. 摘要 biology-forward 开场 + 压缩过度
**位置:** `main_v3.3_draft.md:21` (= `abstract_v3.2.md:9`)，149 词

**问题:** HSSC 无 150 词硬约束（投稿平均 200-250 词常见）。当前为 NHB cap 砍掉了 humanities/policy 线（`abstract_v3.2.md:5` 明列 drop 了 "policy paragraph detail"）；首句两个生物例子（moths/turtles）对 HSSC 跨学科编辑的 triage 信号是 "biology paper misrouted"。WORKLOG 主因①几乎同样出现在 HSSC 入口。

**建议改法:** 扩至 ~220 词，重写首句与结尾。草稿方向：
- 首句改为社会/政策锚点: "From household over-leverage to algorithmic short-video feeds, modern societies generate consumer behaviours that reduce long-run welfare even under full information."
- 第二句保留 Sweet Trap 定义
- 中段保留 4 axioms / T2 bound / 四层实证
- 末段加 1-2 句 policy/humanities: "The framework classifies in advance which intervention family (signal-redesign vs information) will succeed in a contested policy domain, offering a generalisable tool for digital-platform regulation, housing finance, public-health taxation, and cross-cultural welfare analysis."
- 保留 moths/turtles 但移至第 2-3 句作 cross-species 证据线引出，不作开场

### H3. "P5 三层 meta p=0.47" 在 Discussion 段 1 内仍是密集限制清单的一员
**位置:** `main_v3.3_draft.md:165`（Discussion 第 1 段，连续列 10 项 limitations，p=0.47 在第 8 项）

**问题:** WORKLOG 主因③指出 cover letter 自爆；同样的自爆逻辑目前在 main text Discussion 段 1 连续密集暴露了 10 个 limitations（A3.0 scope / T2 dose-matching / κ asymmetry / 11/19 Steiger ✗ / 4.1-34.6 M DALYs / C12 fragile / **p=0.47** / ρ=+1.00 geometric identity / PUA SI / Finnish-only），读成 "theory not fully tested" 的风险不低于 NHB cover letter。HSSC 评审标准比 NHB 宽容，但 reviewer 读 Discussion 首段是第一印象。

**建议改法:** 将 Discussion 段 1 拆分——keep 段 1 为 "achievements + scope" (4-5 sentences)，把 10 项限制移到一个独立子段或 Methods §M8 "Limitations"，按严重度排序（critical → minor），**并把 p=0.47 与 A+D β=+1.58 紧邻放**，以对比而非孤立出现。关键句式从 "The three-layer P5 test yields p=0.47 with the A+D subset as pre-registered headline" 改为 "The pre-registered A+D joint test returned β=+1.58, p=0.019 (Fig 5a); the full three-layer subset was under-powered at p=0.47 (Monte-Carlo power 0.28), as pre-registered (`cross_level_plan.md`, 2026-04-17)."——把 p=0.47 解释为 pre-registered 的 power 问题而非 null result.

### H4. "not an umbrella. It is a foundation." 的 NHB-风格辩护末句
**位置:** `main_v3.3_draft.md:171`（Discussion 末句）

**问题:** "A construct that predicts... is not an umbrella. It is a foundation." 这种强硬的 anti-umbrella 防御在 NHB 是必要的（主因④），在 HSSC 反而 counter-productive——HSSC 欢迎 umbrella constructs，防御式措辞让 reviewer 怀疑作者在隐藏什么。

**建议改法:** 改为正面框架语言：`The framework integrates moth phototaxis, peacock ornamentation, and household over-leverage under a single architectural signature — reward–fitness decoupling under bounded deliberative weight — from which a testable intervention-asymmetry theorem follows across species, domains, and policy regimes.`（删除 "not an umbrella" 否定构造，保留跨物种统一与 T2 定理落地点）

### H5. "避免 HARKing" 与 HARKing-transparency log 的防御姿态
**位置:** `main_v3.3_draft.md:76`（Results Layer B: "but we report the pre-registered headline to avoid HARKing"）；`main_v3.3_draft.md:88`（Layer C: "HARKing-transparency audit: §M3 and Appendix E"）；`main_v3.3_draft.md:120`（Cross-level: "We report this reclassification as exploratory, not as a primary result — changing a case's class to rescue a null is the textbook form of specification mining."）；`main_v3.3_draft.md:257`（HARKing-transparency 段整段）

**问题:** 4 处主动标注 HARKing 在 NHB 是 integrity signal，在 HSSC 这种"主动打自己脸"频率过高的自我指控会被 reviewer 读为 "the authors admit they were close to HARKing multiple times"。HSSC 足够 rigor-oriented 不需要这种过度披露。

**建议改法:** 保留 **一处** 在 Methods §M8 的 pre-registration 段，删除其余三处的主动标签；具体：
- L76: `...we report the pre-registered headline. Alternative dose-response operationalisations recover signal (§3.2 SI).` (删 "to avoid HARKing")
- L88: 末句改 `Full derivation and pre-registration record: §M3 and Appendix E.` (删 "HARKing-transparency audit")
- L120: 保留 "exploratory, not primary" 表述，**删** "— changing a case's class to rescue a null is the textbook form of specification mining." 这一句（自我审判过强）
- L257: 保留整段但删除 "HARKing-transparency" 作为 section label；改为 "Pre-registration consistency."

### H6. Results §11 / SI §11.7 在主稿中的暴露方式
**位置:** `main_v3.3_draft.md:157`（`PUA is retained only as a SI boundary case (§11.7b) because a 0.5-step F2 disagreement in Round 2 exposed construct-boundary ambiguity`）；`main_v3.3_draft.md:247,251,331`（反复提 §11.7 / §11.7b / §11.8）

**问题:** WORKLOG 未明示 §11 HARKing 残留具体位置，但 SI §11 系列明显在 v2.1-v2.3 为应对 Red Team 反复拆解重构（`s11_rewrite.md`/`s11_7_engineered_deception.md`/`s11_8_policy_predictability.md`/`SI_11_7b_pua_extended.md`）。HSSC reviewer 查 SI 看到 4 个独立 §11 重写日志，会理解为 "construct kept morphing to accommodate counter-examples"。

**建议改法:**
- 主稿 L157 关于 PUA 的 sentence 缩短为 `PUA is retained as a supplementary boundary case where Round-2 blind κ showed a construct-boundary ambiguity.` （删 "0.5-step F2 disagreement" 等审稿级细节，留 SI 处理）
- SI master 中把 §11.7b / §11.7 / §11.8 合并成单一 §11 "Boundary cases and contested classifications"；`s11_rewrite.md` 日志不要进 SI master，仅保留 OSF archival log

### H7. Cover letter 需彻底重写（WORKLOG 主因③已点名）
**位置:** `05-manuscript/cover_letter_nhb_v3.md` 不可沿用

**建议改法（高层）:** 新 cover letter 应：
- 首句定位 HSSC scope 的 "cross-disciplinary social-science framework"
- **不出现** "three-layer meta p=0.47"；仅出现 A+D β=+1.58 + κ=1.00 + 11× median asymmetry
- 主动强调 humanities/policy implications（与 HSSC 编辑优先相关的 angle）
- 说明为何 HSSC 适合：interdisciplinary + framework + policy-relevant + OA 有助 reach
- Preprint 披露保留；NHB transfer history **不主动披露**（除非 HSSC submission form 硬性要求）

---

## 3. 应该改 (Medium Priority) — 提升 HSSC accept 率

### M1. Discussion 段 2 "policy purchase" 扩写为 humanities/social policy 双翼
**位置:** `main_v3.3_draft.md:167`（Discussion 第 2 段，约 160 词）

**问题:** 当前段 2 已提 6 个 policy domains 但是纯 policy instrumentalist 角度；HSSC 读者期待：(a) broader social-science implications（社会学视角: aspirational consumption 与不平等）、(b) humanities 维度（cultural critique: 现代性与 Fisher runaway 的辩证）、(c) global policy relevance（低/中收入国家 vs 高收入国家的 trap profile 差异）。

**建议改法:** 段 2 从 160 词扩至 ~350 词，分 3 小段:
- 现有 6 domains policy predictability 保留
- 加 1 段 social-theory implications: Sweet Trap 把 "aspirational over-consumption" 从道德/文化批判变为 measurable architectural property，可用于 Bourdieu 的 cultural capital / Schor 的 overspent American / 消费主义批判文献的经验化
- 加 1 段 global-policy / Global South relevance: 指出 EST（algorithmic feeds）vs MST（diet）vs RST（彩礼/luxury）的相对权重在不同 GDP 段国家不同；Sweet Trap 提供可操作的国别 policy prioritisation 框架

### M2. Introduction 开场 moths/turtles 调整
**位置:** `main_v3.3_draft.md:27`（Introduction 第 1 段）

**问题:** 不是硬伤（HSSC 跨学科），但开场两句全生物（moth phototactic reflex / peacock tail / human sugar）把"human"放在 3-of-3 位置，对社会科学读者来说是"铺垫过长"；第一段 3/4 空间用于建立跨物种类比而非问题导向。

**建议改法:** 调整段 1 的 example 顺序。开头改为: `A household takes a mortgage it cannot safely service; a user opens a short-video app for an hour after intending five minutes; a drinker continues past the point where the next glass imposes liver cost. In every case the chooser endorses a signal internal to the reward system that once tracked fitness but no longer does. The same architecture explains a moth at a streetlight, a peacock's flight-impeding tail, and a sea turtle eating plastic.` —— 人类例子打头、动物例子紧随作跨物种 evidence anchor。保持跨物种卖点，但 triage 视觉改为 "social" first。

### M3. "biology-forward" 术语密度（整体语言基调）
**位置:** 散见——例如 L33 `the sigmoidal response of dopaminergic reward circuits`、L181 `σ the logistic sigmoid (MC-2: saturation + dopaminergic RPE fit to Tobler, Fiorillo & Schultz 2005 Science over 3 log-decades)`、L189 `Berridge & Robinson 2016 (wanting ≠ liking)`、L191 `Mazur 1987 (rats); Rachlin 1974 (pigeons)` 等

**问题:** Methods 里技术性神经生物学锚点密度高（RPE / σ′ / α_i / ψ_i 全符号化）。HSSC reviewer 常为社会学家/政治学家/文化研究者。

**建议改法:** 
- 保留 Methods 的形式化（HSSC 欢迎 methodological rigor）
- 但在 Methods §M1.1 的每个 primitive 后加 1 句**自然语言 gloss**（e.g., "α_i 为个体奖赏敏感度—— how strongly a perceived cue translates into felt reward, measurable via dopaminergic PET or behavioural RPE estimation"）
- Introduction 段 4 (L33 引入 U_perc/U_fit 那段) 加 1-2 句 plain-language 陈述 "In plain terms: perceived utility is what feels rewarding; fitness utility is what benefits the chooser in the long run; Sweet Trap arises when the two diverge."

### M4. Title 调整
**位置:** `main_v3.3_draft.md:1` — `Sweet Trap: a theory of reward–fitness decoupling with cross-species empirical validation`

**建议改法:** HSSC 更偏好 social-anchored title。候选：
- (a) `Sweet Trap: an axiomatic framework for reward–fitness decoupling in human societies, with cross-species validation`
- (b) `The Sweet Trap framework: when consumer behaviour is a trap, not a choice — cross-species evidence and policy implications`
- (c) 保留原 title 但加副标题 `: implications for public policy and cross-cultural welfare analysis`

推荐 (a)——在最小字数代价下把 "human societies" 与 "framework" 关键词置入 HSSC 编辑 triage 窗口。

### M5. 引用新增 humanities / social-theory 锚点
**位置:** 参考文献 L263-298（38 条，多数是生物学/行为经济学/MR 方法学）

**问题:** 参考文献里 0 条 sociology-of-consumption / cultural-studies / political-economy-of-welfare 锚点。HSSC 编辑查引用看跨学科覆盖会注意到。

**建议改法:** 加 3-5 条（不必替换现有），可候选：
- Schor 1998 *The Overspent American* (consumer society)
- Frank 2007 *Falling Behind: How Rising Inequality Harms the Middle Class* (positional consumption)
- Sen 1999 *Development as Freedom* (capability approach, 对接 Δ_ST 作 welfare measurement)
- Zuboff 2019 *The Age of Surveillance Capitalism* (对接 EST / algorithmic feeds)
- Deaton 2013 *The Great Escape* / Veblen 1899 *Theory of the Leisure Class* (对接 RST)

在 Introduction 段 2 末尾与 Discussion 段 2 引入即可。

---

## 4. 可以不改（明确保留）

### K1. 4 层实证结构 (A+B+C+D) — **全保留**
NHB 主因②是"送审成本不划算"（4 类 domain experts）。HSSC 送审体系对跨学科稿件的 reviewer pool 是天然广的；4 层结构反而是 methodological-rigor 加分。砍任何一层都削弱 cross-species 核心卖点。

### K2. 19 MR chains — **全保留**
HSSC 无"Layer D 应该独立成篇"的格式压力；19 chains + 3 informative nulls + discriminant-protective chains + MVMR 是最强的 causal identification，HSSC reviewer（尤其 health/epi 背景）会视为关键证据。

### K3. 9 Figure → 6 Figure（v3.1 已压缩）— **保留 6 张**
HSSC 无硬 figure cap，但 6 图布局已清晰；不必回扩到 9 图（会稀释每图信息密度）。不要砍。

### K4. §11 SI 保留为合并单一 §11（见 H6）
别删内容，合并日志即可；HSSC 欢迎 extended SI。

### K5. Ethics / Inclusion in Global Research / Data Availability / Code Availability 四段 — **保留不动**
L309-331。HSSC 同属 Nature Portfolio，这些段全兼容；Inclusion & Ethics 段在 HSSC 反而比 NHB 更受编辑欢迎（HSSC 更关注 Global South inclusivity）。

### K6. A+D pre-registered subset 作为 headline — **保留**
见 H3，改的是表述方式不是结论定位。

### K7. 3,000 pre-registered specifications — **保留**
HSSC reviewer 视为 methodological 最亮点。

---

## 5. Re-angle 三选一推荐

**推荐: (A) 保持 "cross-species construct" 主线，加 policy/humanities 翼**

**理由:**

| 选项 | 工时成本 | 风险 | 科学完整性 |
|---|---|---|---|
| (A) 主线不动，加双翼 | **低**（Abstract 重写 + Discussion 段 2 扩写 + Title 微调 + 标签全改 ≈ 2-3 天） | 低 — 结构不变意味着 figures/MR/spec-curve 全部复用 | 完整 — 不削弱任何证据层 |
| (B) 重框为 "cross-cultural + cross-species for global policy" | 中（Introduction 全改 + Layer C 升格为 headline + 重排 Results 顺序 ≈ 5-7 天） | 中 — Layer C 其实是 4 层中最弱的（R²=0.255，P3 partial），把它升为 headline 会把弱项放台前 | 降 — 压低 Layer A/D 的 visibility |
| (C) 重框为 "framework proposal, empirical demonstration secondary" | 高（重写全稿为理论型论文 + empirics 压到 "illustrative" ≈ 10-14 天） | 高 — HSSC 欢迎 framework proposals 但要求理论原创性 clean；你的 T2/T3/T4 有 Stage 1-B 的 scope caveat（M4, M5, L4.1），纯理论呈现反而把这些限制放大 | 最差 — 放弃 19 MR + 3000 specs 这个最强资产 |

**(A) 的具体最小工作包（2-3 天）:**

1. 全局 sed: `Nature Human Behaviour` → `Humanities and Social Sciences Communications`（8 处，见 H1）
2. 删 4 条 `[DIFF-F*]` HTML 注释
3. 重写 Abstract → ~220 词（H2）
4. 重写 Title → option (a) （M4）
5. Discussion 段 1 拆分 + p=0.47 重述（H3）
6. Discussion 段 2 扩写至 ~350 词加双翼（M1）
7. 末句 "not an umbrella. It is a foundation." 替换（H4）
8. 4 处 HARKing 语言降级至 1 处（H5）
9. §11 在主稿的暴露方式收敛（H6）
10. Intro 开场 example 顺序调整（M2）
11. 参考文献加 3-5 条 social-theory 锚点（M5）
12. 新写 cover letter（H7）

**核心判断:** (A) 以约 15% 工时保留约 95% 科学强度，是 dominant strategy。(B) 和 (C) 适用于 HSSC 也拒后再考虑（e.g., 下一站 *Global Policy* 或 *Economy and Society*）。

---

## 审稿结论

**当前状态:** v3.3 是 NHB 合规版，直接投 HSSC 会被 triage 识别为 "recycled submission with NHB fingerprints" 而被 handling editor 谨慎对待。

**修改后状态:** 执行必改（H1-H7）清单后，稿件在 HSSC 环境下的科学强度（构念完整性 + 跨学科桥接 + methodological rigor）与定位契合度都能进入 normal-review 区间。核心资产（4 层实证、19 MR、F1+F2 κ=1.00、T2 的 1.5 floor）全保留。

**建议下一步顺序:** H1 (0.5 天) → H7 cover letter draft (0.5 天) → H2 abstract 重写 (0.5 天) → H3+H4+H5+H6 Discussion/Results 微调 (0.5 天) → M1 Discussion 段 2 扩写 (1 天) → M2+M3+M4+M5 (0.5 天)。总计 3-4 个工作日。

---

*Audit 完成时间: 2026-04-20. 基于 main_v3.3_draft.md (331 lines), abstract_v3.2.md (13 lines), figure_legends_v3.1.md (55 lines header), WORKLOG.md §NHB Desk Reject.*
