# Sweet Trap 域 × 变量角色可用性热图

**快速决策矩阵**。行 = 8 个候选域，列 = Sweet Trap 构念的 4 个关键角色。
单元格符号：`***` 强 / `**` 中 / `*` 弱 / `—` 缺。

## 表 A. 自动正则归类结果（粗）

| 域 | sweet_DV | bitter_outcome | lambda_proxy | covariate |
|:---|:---:|:---:|:---:|:---:|
| 域 1: 城市过度投资 (已做) | 7 cols N≤84K | — | 3 cols N≤86K | — |
| 域 2: 鸡娃教育 | — | — | 3 cols N≤85K | 1 col N≤84K |
| 域 3: 996 工作 | 6 cols N≤53K | 1 col N≤6K | 2 cols N≤86K | 4 cols N≤83K |
| 域 4: 彩礼婚恋 | — | — | — | — |
| 域 5: 高糖高脂 | — | 1 col N≤84K | — | — |
| 域 6: BNPL / 信用卡 | — | 7 cols N≤86K | — | — |
| 域 7: 短视频 / 社媒 | — | — | — | — |
| 域 8: 高档房/车 | — | 6 cols N≤86K | 1 col N≤86K | — |

*(自动脚本仅按正则匹配；部分"bitter_outcome"实际是负债金额而非健康后果)*

## 表 B. 人工复核的"四原语 × 域"可用性矩阵

| 域 | Sweet DV (短期满足) | Bitter Outcome (长期代价) | Treatment (Sweet 触发) | λ proxy (外部化) | 整体 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **D1 城市** | `***` `qn12012` N=84K | `***` IGMI 外接 | `***` `igmi_residual` | `***` age/hukou/eduy | `***` |
| **D2 鸡娃** | `**` `qn12012` (借) | `*` 孩子模块待合并 | `***` `eexp`/`school` N=85K | `***` `child_num`/eduy | `**` |
| **D3 996** | `***` `qg401-406` N=42-53K | `***` `health`/`qp401`/`qq4010` | `***` `workhour` N=41K | `***` age/workplace | `***` |
| **D4 彩礼** | `—` | `—` | `—` 仅婚姻状态 | `*` marital | `不可做` |
| **D5 饮食** | `**` `qn12012` (借) | `**` `qp401`/`unhealth` | `*` `food` 支出粗 | `***` age/eduy | `**` |
| **D6 BNPL** | `*` `qn12012` (借) | `**` `savings` 挤出 | `**` `nonhousing_debts` | `**` `limit` | `*` |
| **D7 社媒** | `—` | `*` `qq4010` N=27K | `*` `internet` 0/1 | `**` age | `limited` |
| **D8 房/车** | `***` `dw`/`qn12012` | `***` `savings`/`house_debts` | `***` `mortage`/`resivalue` | `***` age/h_loan | `***` |

## 读图提示

- **`D3 996` 和 `D8 高档房/车` 是 4 个格子都 `***` 的唯二域** → 首推 focal。
- **`D1 城市` 已完成**，作 Study 1 铺垫。
- **`D2 鸡娃`** 的 bitter outcome 是最大缺口；治疗强 `eexp` 但需合并少儿问卷。
- **`D5 饮食`** treatment (`food` 支出) 过粗；建议降级为 SI 或辅助域。
- **`D4 彩礼` 和 `D7 社媒`** 应暂弃 — CFPS 主文件里缺核心变量。

## 5-6 个 focal domain 推荐

Tier 1（Focal A/B/C，直接开做）: **D1** (已做) + **D3** + **D8**
Tier 2（Focal D/E，补数据后做）: **D2** + **D5**
Tier 3（SI / 暂弃）: D4, D6, D7
