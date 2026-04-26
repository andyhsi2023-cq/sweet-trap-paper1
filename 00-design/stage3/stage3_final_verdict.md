# Stage 3 收官诊断：两路 v2 审查收敛性报告

**日期**：2026-04-18
**输入**：Red Team v2 + Novelty Audit v2（两路独立对抗性审查）

---

## 1. 两路独立审查收敛

| 维度 | Red Team v2 | Novelty Audit v2 | 收敛 |
|---|---|---|---|
| 推荐期刊 | NHB | NHB (71/100) | ✅ 完全一致 |
| Desk-reject 概率 | 15–25% (v1: 70–75%) | "defensible at 71" | ✅ 两者都显著改善 |
| R&R accept 概率 | 15–25% | 35% (可提到 45% 经 actions) | 接近 |
| 最大残留风险 | Steiger 8.4× 压缩 | Steiger 8.4× 压缩 | ✅ 完全一致 |
| 第二残留风险 | C13 anomaly + n=2 ρ=1.00 | n_groups=3 + A+D 次要测试 | ✅ 完全一致 |
| 第三残留风险 | Cohen's κ mis-cited | Dev-set circular (无 inter-rater) | ✅ 完全一致 |
| Priority actions | 3 条 (+18–28 pp) | 3 条 (+5–7 points) | ✅ 3 条 actions 交集完美 |

**独立性验证**：两个 agent 不共享中间态，priority actions 完全一致 → 诊断极度可信。

---

## 2. v1 → v2 升级效果（Novelty 10 项）

| 项目 | v1 | v2 | Δ |
|---|---:|---:|---:|
| Falsifiability / HARKing | 3 | **7** | **+4** ⭐ |
| Universality | 6 | **8** | +2 |
| Welfare anchor | 5 | **7** | +2 |
| New theoretical object | 4 | **6** | +2 |
| Methods / Scale / Interdisc. / Policy | +1 each | — | +4 |
| Reproducibility | 6 | **5** | **−1** (OSF 诚实扣分) |
| Narrative (new) | — | 8 | +8 (已含在上) |
| **Total** | **62** | **71** | **+9** |

单项最大贡献：F1+F2 necessary-sufficient + 10-case κ=1.00 + §11 透明化 + G^c ΔR²=0 的 falsifiability 组合拳（+4）。

---

## 3. 三个 Priority Actions（两路共识）

| # | 动作 | 工时 | Red Team uplift | Novelty uplift |
|---|---|---|---|---|
| **A1** | Blind second coder on 10 discriminant cases → real Cohen's κ | 2–3 天 | +5–8 pp | +2–3 |
| **A2** | Promote Tier-1 Steiger-correct **4.1M DALYs 为 headline**, 34.6M 为 extended envelope | 3–5 天 | +8–12 pp | +1 |
| **A3** | Replace ρ(A,D)=+1.00 headline with pre-registered A+D β=+1.58 p=0.019 + 公开声明三层 p=0.47 | 2–3 天 | +5–8 pp | — |

**Combined uplift**：
- Red Team: +18–28 pp → **desk-reject 5–10%, R&R-accept 35–50%**
- Novelty: 71 → 74–75（mid-NHB）→ 接受概率 35% → 45%

工时合计 **5–7 天**（可 A1/A3 并行，A2 连续）。

---

## 4. Andy 提出的新候选（杀猪盘 + PUA）评估

两者均满足 F1+F2 核心（aspirational endorsement under deception），**合法 Sweet Trap**，属新子类 **Engineered Deception / Predatory Mimicry**。

- **PUA variable-ratio intermittent reinforcement** ↔ **C12 短视频算法**：同一 Olds-Milner 机制 → 跨域 mechanism universality 新证据
- **F2 边界**：aspirational under deception（与 C4 coerced 严格区分）

### 推荐路径：选项 B（§11 子类扩展 + discussion 定性案例）
- 工时：2–3 天
- 数据代价低：secondary sources（FBI IC3 2023、公安部 2023 电诈数据）
- 风险：必须明确标注为 "deception-engineered" 子类，避免 umbrella 扩大指控

---

## 5. 最终整合执行计划（Stage 3.5）

**总工时 5–8 天并行完成**：

### Day 1–3（并行三线）
- **A1** blind κ（data-analyst 或 peer-reviewer 盲评 10 controls + 补 3 held-out: C3/C7/C10）
- **A3** cross-level headline 改写（manuscript-writer 改 Abstract + §6）
- **选项 B** §11.7 engineered deception sub-class + 杀猪盘/PUA qualitative case + F1+F2 classifier 跑这 2 case

### Day 3–7（A2 连续）
- **A2** Abstract + §8 改写：headline = "4.1–34.6M DALYs/year envelope, Steiger-correct floor 4.1M ≈ Parkinson's"
- 同步更新 Figure 8 waterfall 标注

### Day 7–8（整合）
- 手稿 v2.1 合并所有修订
- 可选：Red Team v3 mini-round（仅审改动部分，工时 < 2 小时）
- 更新 cover letter

### Exit criteria
- Red Team v3 desk-reject < 10%
- Novelty v2.1 ≥ 74
- Cover letter + pre-submission-lint 通过
- OSF 正式提交（at-submission acceptable for NHB）

---

## 6. 投稿预期

按上述执行计划：

| 阶段 | NHB 接受概率 |
|---|---|
| 当前 v2 as-is | ~35% |
| 完成 A1+A2+A3 | ~45% |
| + 选项 B (Engineered Deception 扩展) | ~48% |
| 若 R&R 后 handle reviewer 得当 | ~55–60% |

对比 Path B (Science) 预估 ~30% → **Path A + Stage 3.5 已逼近 Path B 收益，无实验成本**。

---

## 7. 决策（等 Andy 确认）

**推荐执行 A1 + A2 + A3 + 选项 B**（5–8 天）→ NHB 投稿。

若 Andy 同意，我立即并行启动 4 条工作线（A1 盲评、A2 headline 改写、A3 cross-level 改写、选项 B §11 扩展）。
