# Path B 存档：追 Science main 路径（暂缓执行）

**日期**：2026-04-17 存档
**状态**：已评估，暂不执行，留作未来激活路径

---

## 核心要件

Layer E **预注册行为实验**是 Path B 的唯一不可替代组件。它同时拆除 Red Team 指出的 3 颗致命地雷：

| Red Team 缺陷 | Layer E 如何解决 |
|---|---|
| F1–F4 umbrella 不可证伪 | 预注册具体 prediction → binary falsifier |
| Δ_ST 循环论证 | Δ_ST 作为实验操纵量（manipulated, 非 prior） |
| §11 HARKing | v2 定稿后采集的 out-of-sample validation |

## Layer E 最小可行设计

**在线行为实验（Prolific 平台）**
- n ≈ 2000，2×2×2 因子（θ 显著性 × λ 外部化 × β 贴现）
- 20 轮重复选择任务，场景模拟"高即时奖励/低长期福利"
- 主 outcome：Sweet Trap 采纳率（持续选择 welfare-reducing option）
- 次 outcome：自我报告背书比例（F2 测试）
- 预算：$8–10K
- 时间线：IRB(2w) + 编程(2w) + 采集(4w) + 分析(2w) + 整合(3w) = **13 周**

## 激活条件

- [ ] 3 个月 timeline 可接受
- [ ] $8–10K 实验预算到位
- [ ] CQU IRB 批复（预计 2 周）
- [ ] urban-wellbeing-curvature 交付压缩或延后
- [ ] Layer A–D rescue 完成后，构念未被新数据证伪

## 预期收益（条件）

- Layer E 强支持 v2 预测（Δ>0.3, p<0.001）：Science 30–40%
- 部分支持：Science 10–15%，降级 NHB 70%
- 失败（null/反向）：Science <5%，构念整体需改写

## EV 估算（与 Path A 对比）

- Path A（NHB 主投 + 5-step rescue）：EV ≈ 0.40 NHB-unit
- Path B（NHB 主投 + Layer E）：EV ≈ 0.35 Science + 0.50 NHB ≈ **1.55 NHB-unit**（Science impact ≈ 3× NHB）
- Path B EV 约为 Path A 的 4 倍，但尾部风险（15% 完全失败）Path A 没有

## 激活触发

未来任一满足则重启 Path B：
1. 完成 Path A 后 NHB 被拒且审稿意见暗示需要实验证据
2. Andy 有 3 个月空档（其他项目交付后）
3. 出现 Sweet Trap 领域的竞争性论文 → 需加速差异化
4. 获得合适 coauthor（experimental psychology / behavioral econ 方向）
