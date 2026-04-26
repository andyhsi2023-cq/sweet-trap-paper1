# Stage 3 完善执行计划（1-7 全选）

**启动日期**：2026-04-18
**目标完成**：2026-05-30（6 周）
**最终产出**：NHB 投稿就绪包 + Path B 基础证据

---

## 总体目标

- NHB 投稿接受概率 40% → 55–60%
- 卸除 Red Team 3 处致命缺陷
- Novelty Audit 62/100 → 78/100
- 为未来激活 Path B（Science via Layer E）建好前置证据

---

## 七条工作线

| # | 工作线 | Effort | 依赖 | 主责 agent | Checkpoint 位置 |
|---|---|---|---|---|---|
| 1 | Layer A 动物 meta 扩展 8→20+ | 2 周 | 独立 | literature-specialist | `00-design/pde/layer_A_animal_meta_v2.md` |
| 2 | Layer D MR 扩展（5 outcomes + MVMR + MR-PRESSO + CAUSE） | 1 周 | Finngen 下载 | data-analyst | `00-design/pde/layer_D_MR_findings_v2.md` |
| 3 | Specification Curve for Focal 5 | 1 周 | Focal 5 数据就绪（已 ready） | data-analyst | `03-analysis/spec-curve/` |
| 4 | Mortality/DALY anchor | 3 天 | Layer D chain 3c/7/1a ✅ | data-analyst | `00-design/stage3/mortality_anchor.md` |
| 5 | Cross-level meta-regression | 1 周 | #1 + #2 完成 | data-analyst | `03-analysis/cross_level/` |
| 6 | Positive/Negative control matrix | 1 周 | 独立 | data-analyst | `00-design/pde/discriminant_validity_v2.md` |
| 7 | Cultural G^c WVS/ISSP 校准 | 1–2 周 | WVS 数据 | literature-specialist + data-analyst | `00-design/pde/cultural_Gc_calibration.md` |

---

## 时间表（6 周并行执行）

### Week 1 (2026-04-18 → 04-24) — 四线并行启动

| 工作线 | 具体动作 |
|---|---|
| #1 Layer A 扩展 | corpus-index 系统搜索 → 抽取 12+ 新案例 → 效应量计算 |
| #2 Finngen 补充 | 下载剩余 5 outcomes（F5_ANXIETY/ALCOPANCCHRON/C3_HEP/DM_NEPHROPATHY/C_STROKE）|
| #6 控制矩阵 | 设计 5 positive + 5 systematic negative，定义判别特征 |
| #7 Cultural G^c | WVS 7-wave + ISSP 文化维度文献扫描 |

**Checkpoint**：每条线每 2 天写进度到对应 `.md` 文件

### Week 2 (2026-04-25 → 05-01) — 核心分析 + 启动 #3

| 工作线 | 具体动作 |
|---|---|
| #1 | 完稿 20+ 案例 meta → 新 pooled Δ_ST + 异质性分析 |
| #2 | MR 扩展：MR-PRESSO/CAUSE/MVMR/sex-stratified |
| #3 Spec-curve 启动 | Focal 5（C8/C11/C12/C13/D_酒精）每个至少 128 spec 组合 |
| #6 | 控制矩阵数据分析 → confusion matrix |
| #7 | G^c 权重计算 |

### Week 3 (2026-05-02 → 05-08) — 交付 + 启动 #4

| 工作线 | 具体动作 |
|---|---|
| #2 | Layer D MR 最终报告 15+ chains |
| #3 | Spec-curve 完成 → headline 改为中位数 |
| #4 Mortality anchor 启动 | BMI→T2D→DALY + Alcohol→Liver→DALY + Depression→DALY |
| #6 | 控制矩阵完稿 |
| #7 | G^c 敏感性分析 → 决定保留/删除 |

### Week 4 (2026-05-09 → 05-15) — 整合 + 启动 #5

| 工作线 | 具体动作 |
|---|---|
| #4 | DALY 合成头条数字 |
| #5 Cross-level meta-regression 启动 | Layer A × Layer B × Layer D 效应量跨物种相关 |
| #7 | G^c 终稿 |
| Figure 7 | 跨层综合图 draft（figure-designer） |

### Week 5 (2026-05-16 → 05-22) — 最终整合

| 工作线 | 具体动作 |
|---|---|
| #5 | Cross-level meta 完稿 |
| 手稿 v2 | 整合所有新证据 |
| Figures | 所有 figures 更新（Figure 1-7）|
| §11 改写 | 透明化为 "Response to v1 limitations" |

### Week 6 (2026-05-23 → 05-30) — 审查 + 投稿准备

| 动作 | 输出 |
|---|---|
| Stage 3 二轮 Red Team | hostile-referee agent rerun |
| Stage 4 Novelty Audit v2 | 目标 78/100 |
| Stage 4 Journal Matching | NHB cover letter |
| Pre-submission lint | `_meta/scripts/pre-submission-lint.py` |
| Stage 7 最终门控 | 投稿就绪 |

---

## 自主执行规则

1. **每完成一条线** → checkpoint 写入指定 `.md`，memory 不更新（避免冗余）
2. **阻塞时**：优先查 corpus-index / 跑探索脚本 / 自己决策；不抛 A/B/C 给 Andy
3. **每周** → 跑 pre-submission-lint 检查累积进度
4. **新数据** → 先迁 P1 `/Volumes/P1/城市研究/` + 登记 INDEX.md
5. **计算** → n_workers ≤ 2，不得 Pool(os.cpu_count())
6. **Agent 并行** → 最多 4 个并发（避免上下文稀释）
7. **死线**：如任一工作线 > 计划 1.5 倍，暂停并向 Andy 汇报瓶颈（唯一 fork 点）

---

## 独立性 / 依赖关系图

```
Week 1: #1 #2 #6 #7 [都独立]
              ↓
Week 2-3: #3 [独立于上，依赖 Focal 5 数据（已就绪）]
              ↓
Week 3-4: #4 [依赖 #2 的 chain 3c/7/1a，已就绪]
              ↓
Week 4-5: #5 [依赖 #1 + #2 完成]
              ↓
Week 5-6: Figure 7 + 手稿整合 + Red Team v2
```

---

## 成功指标（Stage 3 退出标准）

- [ ] Layer A pooled Δ_ST 有 ≥ 20 案例，跨物种覆盖 ≥ 4 纲
- [ ] Layer D 有 ≥ 15 chains，MR-PRESSO/CAUSE/MVMR 交叉验证
- [ ] Focal 5 每个有 spec-curve，headline 用中位数
- [ ] Mortality/DALY 头条数字可量化（"Sweet Trap 造成约 X M DALYs/year"）
- [ ] Cross-level meta-regression β 有统计显著
- [ ] 5 positive + 5 negative controls 的 confusion matrix 准确率 > 80%
- [ ] Cultural G^c 要么透明校准证明稳健，要么删除
- [ ] Red Team v2 desk-reject 概率 < 40%（从 70–75%）
- [ ] Novelty Audit v2 ≥ 75/100（从 62）
