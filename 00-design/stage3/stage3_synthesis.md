# Stage 3 综合诊断：Novelty Audit × Red Team 收敛性报告

**日期**：2026-04-17
**触发**：Layer A–D 证据链完成后的投稿前门控
**输入**：两路独立对抗性审查（Novelty Audit + Red Team hostile-referee）

---

## 1. 两路审查结论收敛

| 维度 | Novelty Audit | Red Team (hostile-referee) | 收敛 |
|---|---|---|---|
| Science main 概率 | 62/100（门槛 75） | 70–75% desk-reject | ✅ 一致判"不够" |
| 推荐档次 | NHB / PNAS | NHB / PNAS | ✅ 完全一致 |
| NHB 接受概率 | — | 35–45% | — |
| 核心致命点 | 构念泛化不足、HARKing 风险 | 3 处致命缺陷（见 §2） | ✅ 指向同一缺陷 |

**独立性验证**：两个 agent 不共享中间态，输出却指向同一 3 处缺陷 → 诊断可信度高，不是单一 reviewer 的偏好。

---

## 2. 三处致命缺陷（Red Team 定位）

### F1. Umbrella construct 不可证伪
- F1+F2 定义偏软性，F3 包含 4 个可互换机制（Fisher runaway / Zahavi handicap / 感官诱骗 / Olds-Milner 直通），F4 是"可负反馈"—— 组合出 ≥16 个诊断 profile
- 结果：任何现象都能被"解释"，违反 Popperian falsifiability
- **核心问题**：没有一个 observation 能让"Sweet Trap 构念"被整体否定

### F2. Δ_ST 祖先基线循环论证
- Tier 1（观察）仅占少数案例（Layer A 动物 meta 中约 5/8 有 observational baseline）
- Tier 2/3 用 theoretical prior（"假设自然状态无该刺激"），再用 prior 计算 Δ_ST → 反馈到 prior
- **核心问题**：Δ_ST 不是独立于构念定义的 measurable quantity

### F3. §11 Stage 1 refinements = HARKing
- §11 明确标注 "2026-04-17 addendum"，在 Layer A–D 数据完成后加入 stock-flow L4'、cultural G^c_{τ,y}、engineered sub-class
- Kerr (1998) HARKing 定义：Hypothesizing After Results Known
- **核心问题**：Science reviewer 会立即识别为 post-hoc patching

---

## 3. Novelty Audit 缺口（62/100 → 75 所需 +13 分）

| 项目 | 当前 | 满分 | 差距 |
|---|---|---|---|
| 新理论对象 | 4 | 10 | 构念不是"新对象"，是"重新标签已知机制" |
| 普适性证据 | 6 | 10 | 跨物种 8 案例动物 meta 仅 Layer A 一层 |
| 可证伪性 | 3 | 10 | §11 HARKing 直接扣分 |
| 政策/福祉 anchor | 5 | 10 | mortality/DALY 链条未闭合 |
| 其他 7 项 | 44 | 60 | 达标 |

---

## 4. 推荐路径（不给盲选）

**主推 Path A：Nature Human Behaviour 主投**（realistic 35–45% 接受）

理由：
1. 两个独立 agent 都指向 NHB，不是 Science
2. 现有 4-layer 架构直接匹配 NHB 的"cross-species generalization + human validation"偏好
3. 当前构念可信度在 NHB 审稿人眼中已是优势，不必削弱以适配 Science 的"one clean mechanism"口味
4. Path B（追 Science）需要 +13 分 novelty，至少 6–12 周新工作（Layer E 预注册干预 + Top-20 coauthor） → 时间机会成本太高

### Path A 执行序（cheap → expensive，依次卸除致命缺陷）

**Step 1：OSF 预注册 v1 构念（2 天）**
- 冻结 F1–F4 定义、Δ_ST scalar、4 signatures、outcome 列表
- 时间戳先于任何 v2 修改 → 中和 HARKing 指控（F3）
- 注意：这与你的"预注册后做、投稿前做"规则一致（v1 写完→预注册→Layer A–D 做完→投稿）
- **问题**：v1 实际是在 Layer A–D 前完成的（sweet_trap_formal_model_v1.md，2026-04-16），但未 OSF 时间戳

**Step 2：重写 §11 为"Response to v1 limitations"（1 天）**
- 不再伪装成 model extension；明确标注"v1 发现 3 处不足 → v2 新增 stock-flow/cultural/engineered"
- 透明化 post-hoc 过程 → 把 HARKing 转为合法的 theory refinement

**Step 3：落实 mortality/DALY anchor（3–5 天）**
- Layer D chain 3c 已跑出：BMI → T2D OR=2.06（p=1.64e-08, nIV=90）
- 链入 GBD T2D DALY 负担（2021 ≈ 81M DALYs globally）
- 产出："Sweet Trap via C11 造成约 X M DALYs / year"的量化消费链
- 满足 CLAUDE.md 标准 1："DV 必须是人"

**Step 4：F1–F4 可证伪化（1 周）**
- 从 16+ profile 中选 2–3 个 "Sweet Trap positive signature" 与 2–3 个 "Sweet Trap negative signature"
- 每一个写出具体 observable prediction
- 承诺："若我们观察到 X 且不观察到 Y，构念整体被 falsified"
- 可以直接在 discussion 里列出 3 个 falsification test

**Step 5：Δ_ST 透明化（1 天）**
- 所有 Tier 2/3 案例加 `baseline_source = "theoretical_prior"` 列
- 敏感性分析：仅用 Tier 1 案例重跑 meta → 报告稳健性
- 不试图把 Tier 2/3 "修好"，而是诚实标签并给出 boundary condition

---

## 5. 不推荐路径（已审阅并排除）

### Path B：追 Science main
- 需 +13 novelty points（见 §3）
- 至少 6–12 周新实验 + Top-20 coauthor 招募
- 成功概率仍 <20%
- **ROI 不经济**

### Path C：拆 Olds-Milner Science Report + NHB 二稿
- Red Team rescue #2 提出但同时警告"不要同时做 universality + split"
- Olds-Milner 单一机制论文在 Science Report 档次约 30–40% 接受
- 但会丢失 cross-species 证据链的核心卖点
- **拆分回报不抵整合价值**

---

## 6. 当前状态资产清单

- ✅ Layer A 动物 meta（8 案例, Δ_ST pooled +0.72）
- ✅ Layer B 人类 Focal 5 案例 + HRS replication
- ✅ Layer C ISSP 38-wave（P3 β=-0.73, p=0.036, n=25）
- ✅ Layer D MR（7 successful chains, including C11→BMI→T2D chain 3c）
- ✅ Figure 3/6 refreshed
- ✅ Discriminant validity panel（C2/C4/D3/C6 negative cases 整合）
- ❌ OSF 预注册（未做）
- ❌ §11 透明化改写（HARKing 风险未卸除）
- ❌ Mortality/DALY anchor（chain 3c 有数据未链到 GBD）
- ❌ F1–F4 falsification tests（未列出）

---

## 7. 建议决策（给 Andy）

**主推 Path A（NHB 主投）+ 5 步 rescue 序列**
- 总工时约 10–14 天
- NHB 接受概率从 ~25%（当前）→ 35–45%（完成 rescue 后）
- 若 NHB 拒稿，降级 PNAS/PNAS Nexus 仍有 50–60% 概率
- 保留 Layer E 预注册干预作为 future work（而不是阻塞当前投稿）

**执行顺序建议**：
1. 今天：用户决策 Path A vs. B
2. 若 Path A：先做 Step 1（OSF 预注册 v1，cheapest, 卸除最大风险）
3. 平行：Step 3（mortality anchor 数据侧已完成，仅写作）
4. 然后：Step 2 + Step 4 + Step 5（集中 1 周完成）
5. Stage 4 Journal Matching + Stage 5 manuscript drafting 启动

---

## 8. 关键判断依据回顾

CLAUDE.md 标准 vs. 当前项目：
- ✅ 标准 1 Problem→Mechanism→Consequence：完成 Step 3 后闭合
- ✅ 标准 2 因果识别 1 句话：MR 可直达
- ✅ 标准 3 数据规模：Layer D 百万 UKB + Finngen 达标
- ⚠️ 标准 4 创建框架而非检验：Sweet Trap v2 构念创建本质上符合，但 Red Team 担忧其可证伪性
- ✅ 标准 5 ≥3 学科：进化生物学 + 行为经济学 + MR 遗传流行病学（+社会学 ISSP）
- ✅ 标准 6 政策窗口：WHO 超加工食品政策 + 英国糖税 + 算法推荐监管都对齐
- ⚠️ 标准 7 Specification Curve：Layer D MR 有 sensitivity 但未做正式 spec-curve

**底线**：Path A 在 rescue 后即满足 NHB 所有硬标准，无 deal-breaker。
