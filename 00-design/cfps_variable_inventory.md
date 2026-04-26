# CFPS 2010-2022 变量盘点：8 个 Sweet Trap 候选域

**生成时间**: 2026-04-17
**数据源**: `/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/2010-2022cfps非平衡面板数据(stata_推荐使用）.dta`
**观测数 × 变量数**: 86,294 × 204
**年份覆盖**: 2010, 2012, 2014, 2016, 2018, 2020, 2022（7 个波次，双年频）
**自动生成脚本**: `03-analysis/scripts/cfps_variable_inventory.py`
**全量元数据**: `02-data/linkage/cfps_variable_catalog.csv`

---

## 0. 总览

204 列按类型可分为 5 大类：

| 类别 | 列数 (约) | 代表 |
|:---|---:|:---|
| 人口/身份/ID | 25 | `pid`, `fid10..22`, `year`, `gender`, `age`, `hukou`, `minzu`, `communist` |
| 家庭收入/支出/资产/负债 | 70 | `lnincome`, `total_asset`, `savings`, `nonhousing_debts`, `mortage`, `house_debts`, `limit` |
| 就业/工作 | 10 | `jobclass`, `worknature`, `workhour`, `gongzi`, `fwage`, `wage`, `industry`, `bianzhi` |
| 人/家庭主观问卷 | 30 | `qg401..qg406` 工作满意度, `qn12012` 生活满意, `qn12016` 未来信心, `qn1101` 政府评价, `qn10021..26` 信任, `dw` 社会地位 |
| 健康/生活方式/互联网 | 15 | `health`, `unhealth`, `weak`, `qp401` 慢性病, `qq201` 吸烟, `qq4010` 睡眠, `internet`, `mobile`, `computer`, `onlineshopoping` |
| 教育 | 6 | `edu`, `educ`, `eduy`, `school`, `eexp`, `child_gender`, `child_num` |
| 宏观城市层 (merge in) | 10 | `人均GDP`, `财政支出占GDP比重`, `城镇化水平`, 二/三产增加值, 产业结构指数, 社消/邮电/工业占比 |

**关键诊断（和 auto-tag 脚本的差异）**：

| 关键问题 | 自动脚本输出 | 人工校正 |
|:---|:---|:---|
| 最佳变量 N | 报 86,294（即 id-like） | 剔除 id/pid/year/fid* 后，域内真正 Sweet DV / Bitter outcome 的 N 才是关键 |
| D4 彩礼 | 打星 `***` (2 列) | 只有 `marrige`/`mar` 二元婚姻状态 — **不是** 彩礼金额；D4 应降级 `不可做` |
| D6 BNPL | 打星 `***` (8 列) | 只有 `nonhousing_debts`、`qtqk`（是否非房贷）、`limit`（信贷约束）— **没有** 信用卡/分期变量；降为 `*` |
| D7 社媒 | 打星 `***` (7 列) | 有 `internet` 二元使用，**没有** 抖音/微博 app 类型、**没有** 使用时长、**没有** 抑郁/CES-D；降为 `limited` |
| D5 饮食 | 打星 `***` (6 列) | 有 `food` 食品支出、`qq201` 吸烟、`qp401` 慢性病；**没有** BMI/血糖/血压；降为 `**` |
| D2 鸡娃 | 打星 `***` (10 列) | 有 `eexp`/`school` (家庭教育支出)、`child_num`，但 Bitter outcome（孩子心理/成绩）**不在成人主文件**，需跨表链接孩子模块；`**` |
| D3 996 | 打星 `***` (27 列) | 最完整：`workhour` (周工时 N=41,528)、`gongzi` (月工资 N=20,889)、`qg401..406` 工作满意度 6 题 × 53,015 obs；**保持 `***`** |
| D8 房/车 | 打星 `***` (36 列) | 最完整：`resivalue` 现住房价值、`mortage`、`fd` 住房贷款、`total_asset`、`savings`、`dw` 社会地位；**保持 `***`** |
| D1 城市 | 打星 `***` (13 列) | 已用；`qn12012` 生活满意度主力；**保持 `***`** |

---

## 1. 域 1: 城市过度投资（衔接 Study 1）

**状态**: 已做，用于跨研究桥接。不需新变量。

| 列名 | label | N | 缺失率 | 年份 | 角色 |
|:---|:---|---:|---:|:---|:---|
| `pid` | 个人 ID | 86,294 | 0.0% | 2010-2022 | key |
| `year` | 年份 | 86,294 | 0.0% | 2010-2022 | key |
| `provcd` | 省国标码 | 86,292 | 0.0% | 2010-2022 | city merge key |
| `city` | 对应城市行政代码 | 77,187 | 10.6% | 2010-2022 | city merge key |
| `urban` | 城乡分类 | 84,860 | 1.7% | 2010-2022 | covariate |
| `rural` | 户口 1=农业 | 85,025 | 1.4% | 2010-2022 | λ proxy (hukou) |
| `qn12012` | 对自己生活满意度 | 84,328 | 2.3% | 2010-2022 | **Sweet DV** |
| `qn12016` | 对自己未来信心程度 | 84,110 | 2.5% | 2010-2022 | **Sweet DV 备选** |
| `人均GDP` 等 10 列 | 宏观已 merge | 86,294 | 0.0% | 2010-2022 | context (不用于 FE) |

**已有主规格**: `qn12012 ~ igmi_residual × age + person_FE + year_FE`（见 urban 项目）。

**评级**: `***`（主力 DV 覆盖 84K obs × 7 波次；already tested）。

---

## 2. 域 2: 鸡娃教育

**核心命题**: 家长教育投入 ↑ → 短期家长 pride/身份认同 ↑ → 长期家庭消费挤出、孩子心理/学业后果。

| 列名 | label | N | 缺失率 | 年份 | 角色建议 |
|:---|:---|---:|---:|:---|:---|
| `eexp` | 教育支出（家庭） | 85,594 | 0.8% | 2010-2022 | **Treatment (鸡娃强度)** |
| `school` | 教育培训支出（元/年） | 85,594 | 0.8% | 2010-2022 | **Treatment (课外补课)** |
| `eec` | 文教娱乐支出 | 84,856 | 1.7% | 2010-2022 | treatment-adjacent |
| `child_num` | 家庭少儿人口数量 | 72,977 | 15.4% | 2012-2022 | moderator (是否有孩子) |
| `child` | 是少儿 (0/1) | 72,954 | 15.4% | 2012-2022 | role filter |
| `child_gender` | 一孩性别 | 78,192 | 9.4% | 2010-2022 | heterogeneity |
| `child_p` | 少儿抚养比 | 77,336 | 10.4% | 2012-2022 | family burden |
| `qn10021` | 对父母信任程度 | 70,707 | 18.1% | 2012-2022 | 代际关系 proxy |
| `edu` / `educ` / `eduy` | 家长教育 | 83,564-85,700 | <3% | 2010-2022 | covariate (家长本人) |
| `qn12012` | 家长生活满意度 | 84,328 | 2.3% | 2010-2022 | **Sweet DV** (借用全域) |

**缺口**:
- 孩子心理/焦虑/成绩 **不在成人主文件**（需 CFPS 少儿问卷或家长自评）
- 补课时长、辅导班门数 — 仅有总支出金额
- 备选：用 `eexp_share = eexp / expense` 构造"鸡娃强度"比例

**评级**: `**`（有 treatment 与全域 DV，但 Bitter outcome 需借外部或合并少儿模块；建议**保留为 focal 但作 Study B 延后**）。

---

## 3. 域 3: 996 工作

**核心命题**: 工时/工资 ↑ → 短期晋升荣誉/收入满足 ↑ → 长期健康/家庭/睡眠 ↓。

| 列名 | label | N | 缺失率 | 年份 | 角色建议 |
|:---|:---|---:|---:|:---|:---|
| `workhour` | 每周工作时长 | 41,528 | 51.9% | 2010-2022 | **Treatment (996 指标)** |
| `gongzi` | 每月税后工资 | 20,889 | 75.8% | 2012-2022 | Sweet payoff |
| `fwage` | 家庭工资性收入 | 86,243 | 0.1% | 2010-2022 | Sweet payoff (family) |
| `wage` | 个人工资 | 51,580 | 40.2% | 2010-2022 | Sweet payoff |
| `jobclass` | 工作类型 | 49,597 | 42.5% | 2010-2022 | covariate |
| `worknature` | 工作性质 | 64,614 | 25.1% | 2010-2022 | covariate |
| `workplace` | 工作地点 | 32,108 | 62.8% | 2012-2022 | covariate / migrant proxy |
| `industry` | 行业 | 37,722 | 56.3% | 2010-2022 | covariate |
| `bianzhi` | 编制 | 5,643 | 93.5% | 2020-2022 | 体制内 dummy (N 小) |
| `qg401` | 工作收入满意度 | 42,288 | 51.0% | 2010-2022 | **Sweet DV** |
| `qg402` | 工作安全满意度 | 42,294 | 51.0% | 2010-2022 | Sweet DV |
| `qg403` | 工作环境满意度 | 42,292 | 51.0% | 2010-2022 | Sweet DV |
| `qg404` | 工作时间满意度 | 42,290 | 51.0% | 2010-2022 | Sweet DV (反向) |
| `qg405` | 工作晋升满意度 | 42,068 | 51.2% | 2010-2022 | Sweet DV |
| `qg406` | 工作总满意度 | 53,015 | 38.5% | 2010-2022 | **Sweet DV 主力** |
| `health` | 健康自评 1-5 | 85,948 | 0.4% | 2010-2022 | **Bitter outcome** |
| `unhealth` | 健康倒向 | 85,948 | 0.4% | 2010-2022 | **Bitter outcome** |
| `qp401` | 半年内慢性病 | 84,351 | 2.3% | 2010-2022 | **Bitter outcome** |
| `qq4010` | 睡眠时长 (h/day) | 26,880 | 68.8% | 2016-2022 | **Bitter outcome (sleep)** |

**评级**: `***`（Sweet DV 与 Bitter outcome 都齐、workhour 是清洁 treatment）。**主推 focal domain**。

**注意**：`workhour` N=41,528 是主文件最全的工时变量，但仅雇员有报；退休/农民缺。Study design 需限定样本 `jobclass ∈ {受雇者}`。

---

## 4. 域 4: 彩礼婚恋

| 列名 | label | N | 缺失率 | 年份 | 角色 |
|:---|:---|---:|---:|:---|:---|
| `marrige` / `mar` | 婚姻状况 | 85,474 | 0.9% | 2010-2022 | covariate (非 treatment) |

**缺口**:
- **没有** 彩礼金额、嫁妆、婚礼花费
- 没有结婚时间（只有当前状态）
- 没有婚姻满意度
- 仅能做"已婚 vs 未婚"的截面对比

**评级**: `不可做`。若要上则必须补 CGSS/CHARLS/CFPS 家庭模块（fa1, fb1 问卷）或其他数据源。建议**暂弃**，或改做"婚后财务压力"用 `house_debts` + `marrige` 交互。

---

## 5. 域 5: 高糖高脂饮食

| 列名 | label | N | 缺失率 | 年份 | 角色 |
|:---|:---|---:|---:|:---|:---|
| `food` | 食品支出 | 84,365 | 2.2% | 2010-2022 | **Treatment (饮食支出强度)** |
| `qq201` | 过去一个月吸烟吗 | 84,347 | 2.3% | 2010-2022 | lifestyle treatment |
| `health` | 健康自评 1-5 | 85,948 | 0.4% | 2010-2022 | **Bitter outcome** |
| `unhealth` | 同上反向 | 85,948 | 0.4% | 2010-2022 | Bitter outcome |
| `qp401` | 半年内慢性病 | 84,351 | 2.3% | 2010-2022 | **Bitter outcome (慢性病)** |
| `weak` | 家庭不健康人数 | 86,294 | 0.0% | 2010-2022 | Bitter outcome (family) |
| `mexp` | 医疗保健支出 | 85,401 | 1.0% | 2010-2022 | Bitter outcome ($-denominated) |
| `qn12012` | 生活满意度 | 84,328 | 2.3% | 2010-2022 | **Sweet DV** (借全域) |

**缺口**:
- **没有** BMI、身高、体重
- **没有** 血糖、血压、糖尿病诊断
- **没有** 具体肉/糖/蔬果摄入频率
- 仅能用 `food`（食品支出）做 treatment；用 `qp401`（慢性病 0/1）做 outcome

**评级**: `**`（Treatment 与 outcome 都在但都粗；`food` 的解释力需依赖价格/消费比例处理）。**可作次要 focal**，但 novelty < D3/D8。

---

## 6. 域 6: BNPL / 信用卡

| 列名 | label | N | 缺失率 | 年份 | 角色 |
|:---|:---|---:|---:|:---|:---|
| `qtqk` | 是否有非房产负债 | 86,294 | 0.0% | 2010-2022 | **Treatment (非房贷债务 0/1)** |
| `nonhousing_debts` / `nhd` | 非房贷金融负债（元） | 72,049-85,318 | 1-17% | 2010-2022 | **Treatment (金额)** |
| `limit` | 信贷约束 | 65,231 | 24.4% | 2012-2022 | λ proxy (融资约束家庭) |
| `h_loan` | 是否有房产负债 | 84,977 | 1.5% | 2010-2022 | 相关 |
| `house_debts` | 总房贷（元） | 85,287 | 1.2% | 2010-2022 | 相关 |
| `fd` | 住房贷款 | 6,940 | 92.0% | 2020-2022 | small |
| `debt_p` | 债务收入比 | 5,509 | 93.6% | 2020-2022 | key ratio (N 小) |

**缺口**:
- **没有** 信用卡使用、花呗、分期变量
- **没有** 财务压力/焦虑
- 只能做"消费信贷 vs 非"的代理：`nonhousing_debts > 0` 为 treatment

**评级**: `*`（treatment 可构造但粗；outcome 借用 `qn12012`/`health`/家庭消费波动；建议**合并到 D8（资产/负债整体）**或作 SI 用）。

---

## 7. 域 7: 短视频 / 社媒

| 列名 | label | N | 缺失率 | 年份 | 角色 |
|:---|:---|---:|---:|:---|:---|
| `internet` | 互联网使用 (0/1) | 72,476 | 16.0% | 2012-2022 | **Treatment (低维)** |
| `mobile` | 是否移动上网 | 46,153 | 46.5% | 2014-2022 | treatment |
| `computer` | 是否电脑上网 | 46,153 | 46.5% | 2014-2022 | treatment |
| `onlineshopoping` | 是否网购 | 28,075 | 67.5% | 2016-2022 | Sweet consumption |
| `qq4010` | 睡眠时长 | 26,880 | 68.8% | 2016-2022 | **Bitter outcome** |
| `health` | 健康自评 | 85,948 | 0.4% | 2010-2022 | Bitter outcome |
| `social` / `Soc`/`soc` | 人情礼支出 | 57,579 | 33.2% | 2012-2022 | social network (非社媒) |

**缺口**:
- **没有** 日均上网/刷短视频时长
- **没有** 具体 app (微博/微信/抖音)
- **没有** 抑郁量表 (CES-D)、注意力、心理健康
- 仅"是否上网"0/1 且 2020+ 接近普及率 80%+ → within-person 变异几乎消失

**评级**: `limited`（treatment 信息量薄；outcome 只有 sleep 且 N 仅 26K）。建议**暂弃**，除非补充 CFPS 孩子模块或外部 app 使用数据（微信/抖音发布官方报告），否则很难做出 Nature 级因果识别。

---

## 8. 域 8: 高档房/车

| 列名 | label | N | 缺失率 | 年份 | 角色 |
|:---|:---|---:|---:|:---|:---|
| `resivalue` | 现住房价值（万元） | 85,966 | 0.4% | 2010-2022 | **Treatment (房产价值)** |
| `house` | 居住支出 | 83,785 | 2.9% | 2010-2022 | treatment |
| `mortage` / `mor` | 房贷支出 | 19,976-85,866 | 1-77% | 2010-2022 | **Treatment (房贷强度)** |
| `h_loan` | 是否有房产负债 | 84,977 | 1.5% | 2010-2022 | treatment |
| `house_debts` | 总房贷（元） | 85,287 | 1.2% | 2010-2022 | treatment |
| `fd` | 住房贷款 | 6,940 | 92.0% | 2020-2022 | detail (N 小) |
| `total_asset` / `Asset` / `asset` | 家庭净资产 | 79,904-82,286 | 5-7% | 2010-2022 | wealth |
| `savings` / `sav` / `cas` | 现金/存款 | 85,983 | 0.4% | 2010-2022 | **Bitter outcome (储蓄挤出)** |
| `finance_asset` / `Fin`/`fin` | 金融资产 | 72,474-85,562 | 1-16% | 2010-2022 | wealth |
| `Esta`/`esta` | 家庭净房产 | 58,786-59,648 | 31% | 2012-2022 | wealth |
| `Est`/`est` | 家庭总房产 | 72,588 | 15.9% | 2010-2022 | wealth |
| `Hast`/`hast` | 总房产市值 | 60,870 | 29.5% | 2012-2022 | wealth |
| `land_asset`/`Land`/`land` | 土地资产 | 85,821 | 0.5% | 2010-2022 | wealth (agri) |
| `durables_asset` | 耐用消费品价值 | 71,923 | 16.7% | 2012-2022 | 车/家电 proxy |
| `company` | 经营资产 | 85,858 | 0.5% | 2010-2022 | wealth |
| `financial_product` | 金融产品 | 33,466 | 61.2% | 2018-2022 | detail |
| `fxzc` | 风险资产 | 29,634 | 65.7% | 2018-2022 | detail |
| `dw` | 社会地位（自评） | 83,991 | 2.7% | 2010-2022 | **Sweet DV (status pride)** |
| `qn12012` | 生活满意度 | 84,328 | 2.3% | 2010-2022 | **Sweet DV** |
| `qn12016` | 未来信心 | 84,110 | 2.5% | 2010-2022 | Sweet DV 备选 |

**评级**: `***`（最完整的变量群：treatment `mortage`/`resivalue`、短期满足 `dw`/`qn12012`、长期代价 `savings` 挤出/`house_debts` 负担；7 波 × 80K+）。**强烈推荐 focal domain**。

---

## 9. 域可用性综合评级与 Focal 推荐

| 域 | 列数 | Sweet DV | Bitter outcome | Treatment | 评级 | Focal 推荐 |
|:---|---:|:---|:---|:---|:---:|:---|
| D1 城市过度投资 | 13 | `qn12012` 有 | IGMI 外部 有 | `igmi_residual` 有 | `***` | **已做 (Study 1)** |
| D2 鸡娃教育 | 10 | `qn12012` (借) | 孩子模块需合并 | `eexp`/`school` 有 | `**` | **Study B (延后)** |
| D3 996 工作 | ~15 | `qg406` 有 | `health`/`qp401`/`qq4010` 有 | `workhour` 有 | `***` | **Focal A** |
| D4 彩礼婚恋 | 2 | - | - | 无彩礼金额 | `不可做` | **暂弃** |
| D5 高糖高脂 | 6 | `qn12012` (借) | `qp401`/`unhealth` 有 | `food` 支出 | `**` | **辅助 / SI** |
| D6 BNPL | 8 | `qn12012` (借) | `savings` ↓ | `nonhousing_debts` | `*` | **并入 D8 或 SI** |
| D7 社媒 | 7 | - | `qq4010` (N=27K) | `internet` 0/1 弱 | `limited` | **暂弃** |
| D8 高档房/车 | ~25 | `dw` 有 `qn12012` 有 | `savings` ↓ `house_debts` ↑ | `mortage`/`resivalue` 有 | `***` | **Focal B** |

### Stage 1 决策建议（5-6 个 focal）

**Tier 1 — 直接开做（3 域）**：
1. **D1 城市过度投资** — 已完成，作 narrative 起点
2. **D3 996 工作** — `workhour × qg406/health` 组合，treatment 与 outcome 都清洁
3. **D8 高档房/车** — `mortage × dw/savings` 组合，变量最完整

**Tier 2 — 需补数据或跨模块链接（2 域）**：
4. **D2 鸡娃教育** — `eexp` 作 treatment，需合并 CFPS 少儿问卷补 outcome
5. **D5 高糖高脂** — `food` 作 treatment，`qp401` 作 outcome；如能并 CHARLS 做体检指标更好

**Tier 3 — 暂弃或转 SI（3 域）**：
6. **D4 彩礼** — 需补 CGSS 或 CHARLS 婚姻模块；CFPS 无彩礼金额变量
7. **D6 BNPL** — 并入 D8 作为"消费信贷"子分析
8. **D7 社媒** — 需补 app 使用数据；CFPS 的 `internet` 0/1 不足

### λ (externalization capacity) 异质性代理变量清单

跨域复用：

| λ 维度 | CFPS 变量 | N | 说明 |
|:---|:---|---:|:---|
| Life-cycle horizon (age) | `age` | 86,271 | 年轻人 λ 高（长期成本外部化给未来自己） |
| Hukou mobility | `hukou` / `res` / `rural` | 85,025 | 农业户口者迁移成本不同 |
| Education (future mobility) | `eduy` | 83,564 | 高教育 更可能搬离 |
| Migrant status | `workplace` | 32,108 | 工作地 不等于 户籍地 高 λ |
| Party membership | `communist` | 56,622 | 体制内资源获取 |
| Homeownership | `h_loan`/`resivalue` | 85K | 有房者 λ 低（沉没成本绑定） |
| Child presence | `child_num` | 72,977 | 有孩子者 λ 低（intergenerational altruism） |
| Family size | `familysize` | 86,294 | 大家庭分担 risk |

其他 λ 代理需外部 merge：城市等级、城市迁出率、地方债存量。

---

## 10. 数据清洗与合并的工程建议（S1 起跑前）

1. **合并策略**: 主文件已是 person-year 长表，`pid × year` 唯一。可直接在现有 `cfps_igmi_expanded.parquet` 基础扩展列。
2. **样本筛选**: D3 限定 `jobclass ∈ {受雇者}` 约 N ≈ 40K；D2 限定 `child_num ≥ 1` 约 N ≈ 50K。
3. **派生变量**:
   - D3: `overtime_d = 1[workhour > 48]`（中国劳动法周 40h，48h 是加班阈值）
   - D8: `mortgage_burden = mortage / fincome1`（还款压力比）
   - D5: `food_share = food / expense`（恩格尔系数）
4. **冗余列**: `Asset`/`asset` 等大小写对（大写=金额，小写=对数）是同一指标不同变换，保留对数做主分析。
5. **宏观 10 列 (`人均GDP` 等)**: 已是 city × year 宏观，可作 covariate 或 IV；但 `pid` 内无变异时不能与 person FE 同时用（需 city × year FE）。

---

## 11. 文件清单

- **主报告**（本文件）: `00-design/cfps_variable_inventory.md`
- **全量元数据**: `02-data/linkage/cfps_variable_catalog.csv` (204 行，含 top5 value counts)
- **热图**: `00-design/cfps_variable_heatmap.md`
- **生成脚本**: `03-analysis/scripts/cfps_variable_inventory.py`
- **运行日志**: `03-analysis/scripts/cfps_variable_inventory.log`
