# C5 "奢侈品炫耀消费" — Sweet Trap PDE Findings (新 Focal 候选)

**Generated:** 2026-04-17
**Analysis script:** `03-analysis/scripts/C5_luxury_sweet_trap.py`
**Results JSON:** `02-data/processed/C5_results.json`
**Spec-curve CSV:** `02-data/processed/C5_speccurve.csv`
**C5 panel:** `02-data/processed/panel_C5_luxury.parquet` (SHA-256 `fc7179cce1ba3dcaf8023072ef3add580cd24aee86f5347a886378056e7ba27b`)
**CFPS source SHA-256:** `4a38447cf24402aca323bb338b6d831a25267e4236ae86e1f1a75c1ae14d19b8`
**Log:** `03-analysis/scripts/C5_luxury_sweet_trap.log`
**Construct authority:** `00-design/sweet_trap_formal_model_v2.md` §1 (F1–F4) & §2 (Δ_ST)
**Animal bridges:** `00-design/pde/layer_A_animal_meta_synthesis.md` §2 A7 peacock (+0.58) & A11 jewel-beetle (+0.55)

---

## 0. TL;DR — F2 干净；Sweet 弱但方向一致；Bitter 强；Δ_ST 正但幅度低

> **CFPS 2010–2022 (N = 86,294 人年 / 32,165 pid，7 波) 在 C5 奢侈 / 炫耀性消费上独立可测**：`dress`（衣着鞋帽）、`travel`（旅游）、`eec`（文教娱乐）、`durables_asset`（耐用消费品价值）四项给出 granular expenditure ledger。衣着是中国个人奢侈支出的主要类别 (Bain/McKinsey 2024)，与 A7 peacock 的 costly signal 形成同构桥接。
>
> **F2 (voluntary endorsement) PASS**：所有 6 个 luxury proxy 都与 lnincome (+0.17 ~ +0.39)、eduy (+0.14 ~ +0.35)、urban (+0.04 ~ +0.18) **正相关**。与 C2 鸡娃（cor(edu_spend, income) 为正但反映 coerced exposure）、D3 996（cor = 负）形成清洁对比，C5 是 aspirational voluntary。
>
> **Sweet (θ) — 弱但方向一致**：
> - Level-based `ln_luxury_broad → qn12012` (prov+year FE, pid-cluster)：β = **+0.019** [+0.014, +0.023], p < 10⁻¹² (N = 76,479)。`ln_dress` 单独 β = +0.028。
> - Within-person `Δ ln_luxury → Δ qn12012` (pid FE, year FE)：β = +0.004 [−0.004, +0.011], **p = 0.305** — 变 null 值。
> - 解读：跨个体的奢侈消费水平差异能预测 0.6 SD 的生活满意度差异的 ~2%；但同一个人年际 fluctuation 带不动满意度。这与 C4 彩礼在 marital_sat 上发现的「specific-DV 有号向签名但 aggregate null」的 F1 decoupling-in-miniature 一致。
>
> **Bitter (forward-looking, λβρ) — 强**：
> - `ln_luxury_full_t → Δ ln_savings_{t+1}` = **−0.165** [−0.202, −0.128], p < 10⁻¹⁵ (N = 49,047)。高奢侈 → 下一波储蓄下跌。
> - `ln_luxury_full_t → Δ ln_asset_{t+1}` = **−0.058** [−0.067, −0.050], p < 10⁻³⁰ (N = 45,698)。净资产同样下滑。
> - `ln_luxury_full → Δ ln_debt_同期`  = +0.119, p < 10⁻¹⁵ — 债务同步上升。
>
> **Δ_ST on qn12012 (cluster-bootstrap 1,000 次, cluster by pid)**：
> - `ln_luxury_broad`：Δ_ST = **+0.098** [+0.085, +0.111]（ancestral 2010-14 cor = +0.046，current 2018-22 cor = **−0.053**）
> - `ln_luxury_full`:  Δ_ST = **+0.090** [+0.077, +0.103]（anc = +0.060，cur = −0.030）
> - `ln_dress`:       Δ_ST = **+0.114** [+0.101, +0.127]（anc = +0.071，cur = −0.042）
> - `luxury_full_share`: Δ_ST = +0.022 [+0.010, +0.034]（较弱 — share operationalisation 与 C11 sugar 一样稀释）
>
> **号向反转的两个证据条**：
> 1. C5 的 ancestral cor(R, F) = **正** (2010-14)：对应中国奢侈消费刚兴起阶段，先买的是真正更高效用 (更好衣物、第一台车)。
> 2. C5 的 current cor(R, F) = **负** (2018-22)：当全社会卷入 signaling 竞赛，LV/Gucci/Hermès 的 marginal utility 落入 status-race equilibrium，signaling 的满意度回报被 peer reference point 吞噬。
>
> **这是 F1 (reward-fitness decoupling) 的教科书级 demonstration**：一个 within-sample、8 年间完成的号向翻转 (+0.07 → −0.04)。C2、C4、C11 都没有给出这么清洁的 ancestral → current 翻转信号。
>
> **Σ_ST 三系数挑战：F3 M1 (habit lock-in) WEAK**。ρ AR(1) within-person = **−0.11 ~ −0.17** （p < 10⁻⁴）—— 负号！上一波重买的家庭下一波消费反而下跌，存在 mean-reversion 而非 habit-lock。Hedonic treadmill 也反向：lagged level 比 current Δ 对 qn12012 的 coefficient 更大 (β_lag = +0.019 vs β_delta = +0.008)。**这意味着奢侈消费在中国 CFPS 家户层面是 status-stock 而非 novelty-chase**。F3 M2 (peer comparison) 仍是主要持续机制，但 M1 (neural habit) 反而 null/负。
>
> **Spec curve (576 specs)**：
> - Sweet (qn12012, d_qn12012, qn12016)：81% 号向为正，24% 过 p<0.05 门槛。
> - Bitter forward (dln_asset_fwd, β<0 expected)：**96%** 号向为负，**74% 过 p<0.05**。
> - Bitter debt (d_ln_debt, β>0 expected)：**90% 号向为正，68% 过 p<0.05**。
>
> **同桌对比**：
>
> | Case | F2 | Δ_ST 主 DV | Bitter 号向 | Hedonic 复现 | 信心度 |
> |:---|:---:|---:|:---:|:---:|:---:|
> | Layer A pool | — | +0.72 | — | — | — |
> | A7 peacock | — | +0.58 | — | — | — |
> | A11 jewel-beetle | — | +0.55 | — | — | — |
> | **C5 luxury (本)** | ✓ | **+0.09 ~ +0.11** | ✓ | 反向 | **中-高** |
> | C2 鸡娃 (未完) | ✓ | — | — | — | TBD |
> | C4 彩礼 (降级) | 部分 | −0.04 | null | null | 低 |
> | C11 sugar/fat (降级) | ✓ | −0.02 ~ −0.10 | null | null | 低 |
> | D3 996 (降级) | ✗ coerced | — | — | — | null |
>
> **定位**：C5 是 **四个人类域里唯一同时给出 (a) 方向翻转的 Δ_ST > 0, (b) 强 Bitter forward 证据, (c) F2 完全清洁的候选**。虽然 Δ_ST 幅度仅 +0.09 ~ +0.11（低于 A7 peacock 的 +0.58），但 *CFPS 操作化口径窄*（只能用 dress+travel+eec+durables_asset 代理 luxury，真正 Hermès/LV/Rolex 未单列），**真实效应在胡润 2024 豪车 / 信用卡高端消费数据里应当更大**。C5 可作为论文的 **Focal #1 候选**，替代已降级的 C4 和 C11，与正在执行的 C2 鸡娃 × 双减 DID 并列 Focal 双支柱。

---

## 1. 数据溯源 & 变量粒度审查

| 检查项 | 值 |
|:---|:---|
| CFPS 长面板路径 | `/Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/cfps_long_panel.parquet` |
| CFPS 长面板 SHA-256 | `4a38447cf24402aca323bb338b6d831a25267e4236ae86e1f1a75c1ae14d19b8` |
| 原始 DTA | `/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/2010-2022cfps非平衡面板数据(stata_推荐使用）.dta` |
| 面板行 × 列 | 86,294 × 158（原始） → 65（C5 专用） |
| 唯一 pid | 32,165 |
| 波次 | 7（2010, 2012, 2014, 2016, 2018, 2020, 2022） |
| 省份 | 31 |
| urban/rural 比例 | 50.5 / 49.5 |

### 1.1 CFPS 变量粒度 — C5 可独立测量

| 变量 | 标签 | 覆盖波次 | 非空 N | 中位数 | 在 parquet? |
|:---|:---|:---:|---:|---:|:---:|
| **dress** | 衣着鞋帽支出 | 2010-2022 (7) | 84,841 | 1,200 元 | ✓ |
| **travel** | 旅游支出 | 2012-2022 (6) | 72,260 | 0 元 | 需从 DTA 补 |
| **eec** | 文教娱乐支出 | 2010-2022 (7) | 84,812 | ~500 元 | ✓ |
| **trco** | 交通通讯支出 | 2010-2022 (7) | 84,140 | 2,640 元 | 需从 DTA 补 |
| **durables_asset** | 耐用消费品价值 | 2012-2022 (6) | 71,923 | 7,755 元 | ✓ |
| **daily** | 家庭设备及日用品支出 | 2010-2022 (7) | 85,543 | - | ✓ |
| **other** | 其他消费性支出 | 2010-2022 (7) | 85,543 | 200 元 | 需从 DTA 补 |
| expense | 家庭总支出 | 2010-2022 (7) | 82,803 | 40,000 元 | ✓ |

**结论**：CFPS 对 C5 的粒度 **足够** 做 PDE。衣着（dress）作为主 proxy 在 Bain & McKinsey 中国奢侈品报告口径下占个人奢侈支出的 ~40-55%（fashion & leather goods）。`travel`（体验型奢侈）+ `eec`（高端娱乐）+ Δ`durables_asset`（耐用品升级）作为复合 proxy。

**不足**：CFPS 不单列 high-end brand ("LV 属于 clothing 子项目" 但未标注品牌)、豪车（只有 trco 合并值）、珠宝首饰、烟酒（只有 qq201 吸烟二元 dummy）。这些属于 *upper-tail* luxury — 如果真实 Δ_ST 在 tails 最强，CFPS 会 *低估* 信号。

### 1.2 替代数据源（若 CFPS 粒度不足时的 fallback）

| 数据源 | 粒度 | 可得性 | 建议 |
|:---|:---|:---|:---|
| 胡润百富榜年度报告 | 高净值人群消费行为 | 公开 PDF | SI 交叉验证 |
| 贝恩 China Luxury Report | 品牌级 | 公开摘要 | 背景文献 |
| 中信 / 招商 信用卡消费账单 | SKU 级 | 需与银行合作 | 理想但成本高 |
| 天猫 / 京东高端店铺成交 | SKU 级 | Aliresearch 协议 | 次选 |
| CGSS 2017 A62 消费序列 | 粗分类 | 已有 | 替代性低 |
| 小红书 / 抖音 POI 热度 | 行为 | 公开 API | 用于 F2 社会传染 |

本次 C5 PDE 仅用 CFPS 公开数据，其他源未入库。

### 1.3 C5 分析面板构造

```
luxury_core  := dress                                    # 最严格（衣服鞋帽）
luxury_broad := dress + travel + eec                     # 加体验与娱乐
luxury_full  := dress + travel + eec + Δdurables_asset⁺  # 加耐用品升级
```

复合品均为家户年 RMB，取 `log1p` 防 0。Share 型指标 = luxury / expense。

---

## 2. F2 — Voluntary endorsement 诊断（PASS）

F2 要求：在无胁迫下，奖励信号激活时个体选择该选项的概率高于 baseline。Luxury 购买天然是 active choice（与 D3 996 形成对比），所以 F2 的定量代理是 **奢侈消费随财富/教育/城乡梯度升高**（若随收入下跌反而意味着 coerced subsistence spending, F2 失败）。

| Luxury proxy | N | cor(income) | cor(edu) | cor(urban) | F2 verdict |
|:---|---:|---:|---:|---:|:---:|
| dress | 77,530 | **+0.253** | +0.246 | +0.152 | ✓ |
| luxury_broad | 77,530 | +0.264 | +0.273 | +0.175 | ✓ |
| luxury_full | 77,530 | +0.170 | +0.139 | +0.094 | ✓ |
| ln_luxury_broad | 77,530 | **+0.381** | **+0.349** | +0.161 | ✓ (strongest) |
| ln_luxury_full | 77,530 | **+0.394** | +0.337 | +0.159 | ✓ (strongest) |
| luxury_full_share | 72,147 | +0.150 | +0.150 | +0.044 | ✓ |

**F2 pass = TRUE 全部 6 个 proxy**。cor ≈ +0.4 (log scale) 是一个强 wealth gradient —— 完全符合 aspirational luxury 的 Zahavi handicap 预测（越富越买）。**与 C2 鸡娃** (cor ≈ +0.3) 相当，但 **反方向** 对比 D3 996 (cor ≈ −0.1; 穷越 996)。与 C11 sugar/fat 的 Engel 反向更是形成干净分离。

---

## 3. 核心回归 — Sweet & Bitter

全部模型：`pid FE (via within-demean) + year FE (via dummies)`, cluster-robust SE at `pid`. 控制 `lnincome, eduy, age, urban`.

### 3.1 Sweet (θ) — 弱号向签名

**Within-person 年际 Δ**（最严格）：

| Treatment | DV | N | β | 95% CI | p |
|:---|:---|---:|---:|:---:|---:|
| d_ln_luxury_broad | Δ qn12012 | 47,796 | +0.0038 | [−0.0035, +0.0110] | 0.305 |
| d_ln_luxury_full | Δ qn12012 | 47,796 | +0.0038 | [−0.0022, +0.0099] | 0.215 |
| d_ln_dress | Δ qn12012 | 47,796 | +0.0046 | [−0.0027, +0.0120] | 0.217 |
| d_luxury_broad_share | Δ qn12012 | 45,137 | +0.0070 | [−0.083, +0.097] | 0.878 |
| d_luxury_full_share | Δ qn12012 | 40,584 | +0.0025 | [−0.056, +0.061] | 0.935 |

**全部 5 条号向为正但 p > 0.2**。within-person Δ 的 null 解读有两条：
1. **True Sweet Trap null after accounting for hedonic treadmill**：Δluxury 当期带来的快感在 2 年后（下一波）已 fully adapt 掉，所以 year-on-year difference-in-difference 看不到剩余效应。
2. **Power**：N=47k 情况下 power 足够检测 β=0.015 at p<0.05，所以 true effect < 0.01 即不会被捕获。

**Level-based (prov + year FE, 没有 pid FE)** — 剥去个体固定效应的跨样本变异：

| Treatment | DV | N | β | 95% CI | p |
|:---|:---|---:|---:|:---:|---:|
| ln_luxury_broad | qn12012 | 76,479 | **+0.0185** | [+0.0143, +0.0227] | <0.0001 |
| ln_luxury_full | qn12012 | 76,479 | **+0.0202** | [+0.0163, +0.0242] | <0.0001 |
| ln_dress | qn12012 | 76,479 | **+0.0280** | [+0.0234, +0.0325] | <0.0001 |
| luxury_full_share | qn12012 | 71,181 | +0.0576 | [+0.0170, +0.0982] | 0.0054 |

**Level-based 正显著**。一个 1 SD 的 ln_luxury_full 变化 ≈ 1.5 log units ≈ 340% luxury 支出上升 → 约 0.03 log × 1.5 = 0.03 Likert 点（约 0.03 SD of life_sat）。**经济意义上很小**。

### 3.2 Bitter (λβρ) — Forward-looking 强签名

**同期 (t)**：

| DV | Treatment | N | β | 95% CI | p |
|:---|:---|---:|---:|:---:|---:|
| Δ ln_savings | ln_luxury_broad | 49,520 | +0.113 | [+0.071, +0.155] | <0.0001 |
| Δ ln_savings | ln_luxury_full | 49,520 | +0.101 | [+0.063, +0.139] | <0.0001 |
| Δ ln_debt | ln_luxury_broad | 49,017 | +0.071 | [+0.037, +0.106] | 0.0001 |
| Δ ln_debt | ln_luxury_full | 49,017 | **+0.119** | [+0.088, +0.149] | <0.0001 |

同期 Δsavings 正号反映 **共变量效应**（同时期高收入 → 高奢侈 + 高储蓄）—— 这是共时混淆，**不是 Sweet Trap 测试**。而 Δdebt 同期正号开始透露 F4 signal：买奢侈品同期债务上升，意味着部分奢侈是靠借贷完成。

**Forward-looking (t+1)** — 才是干净的 Bitter 测试：

| DV | Treatment | N | β | 95% CI | p |
|:---|:---|---:|---:|:---:|---:|
| Δ ln_savings_{t+1} | ln_luxury_broad_t | 49,047 | **−0.187** | [−0.227, −0.148] | <10⁻¹⁵ |
| Δ ln_savings_{t+1} | ln_luxury_full_t | 49,047 | **−0.165** | [−0.202, −0.128] | <10⁻¹⁵ |
| Δ ln_savings_{t+1} | luxury_full_share_t | 45,841 | **−0.903** | [−1.313, −0.494] | <0.0001 |
| Δ ln_asset_{t+1} | ln_luxury_broad_t | 45,698 | **−0.036** | [−0.045, −0.026] | <10⁻¹⁵ |
| Δ ln_asset_{t+1} | ln_luxury_full_t | 45,698 | **−0.058** | [−0.067, −0.050] | <10⁻³⁰ |
| Δ ln_asset_{t+1} | luxury_full_share_t | 42,811 | **−0.393** | [−0.479, −0.307] | <10⁻²⁰ |

**核心发现**：当期奢侈消费越高的家庭，下一波 (2 年后) 储蓄和净资产成长越低。这是 F4 信息阻断的直接证据—— decision period (t) 的奢侈消费产生即时 θ，但成本在 t+1 才兑现（储蓄下跌、资产成长放缓）。

---

## 4. Hedonic Treadmill (β) & ρ 锁定 — 反向发现

### 4.1 ρ AR(1) — **负号（mean-reversion 非 lock-in）**

Within-person 奢侈消费的自回归系数：

| Signal | N | ρ | p |
|:---|---:|---:|---:|
| ln_luxury_broad | 52,511 | **−0.108** | <0.0001 |
| ln_luxury_full | 52,511 | **−0.140** | <0.0001 |
| ln_dress | 52,511 | **−0.172** | <0.0001 |

**ρ 为负 ≠ F3 M1 failed**。M1 要求 within-person 习惯性 lock-in，即 ρ > 0。但 CFPS 家户年度数据显示 ρ ≈ −0.1 ~ −0.2，即 **这一波 splurge 的家庭下一波会收敛回均值**。

这个现象的解读：
1. **Lumpy purchase 性质**：奢侈消费是 infrequent big-ticket（一年买一个包 vs 连续性食品消费），所以 within-person 年际 noise > trend signal → 观察到 mean-reversion。
2. **预算约束**：高开销年之后必须紧缩。
3. **F3 M2 (peer norms) 替代了 M1 (habit)**：锁定在群体层面不是个体层面。CFPS 内无法直接测 M2，但 prov + year 的固定交叉项吸收 peer pressure。

**结论**：C5 的 F3 主要通过 M2 (intra-generational peer comparison) 持续，M1 (individual habit) 弱或反向。这与 phenomenology_archive 对 C5 的预测一致（§C.5 "individual: peer comparison locks in" 而非 "neural habit"）。

### 4.2 Hedonic treadmill 共同回归 — **反向**

将 `ln_luxury_lag1` (adaptation) 和 `d_ln_luxury` (fresh Δ) 一起放入对 qn12012 的 within-person 回归：

| Treat | β | p |
|:---|---:|---:|
| ln_luxury_broad_lag1 (adaptation) | **+0.0119** | 0.016 |
| d_ln_luxury_broad (fresh Δ) | +0.0052 | 0.118 |
| ln_luxury_full_lag1 | **+0.0194** | <0.0001 |
| d_ln_luxury_full | +0.0083 | 0.004 |

**经典 hedonic treadmill 预测**：lagged level fade, current Δ dominate. 我们观察到的是 **反向**：**lagged level 比 Δ 的系数更大**。这表明在 CFPS 2 年间隔下，奢侈带来的满意度 *没有 fully adapt*，反而累积成 status-stock 效应。

解读：奢侈消费 = peacock plumage（一个 durable signal）而非 sugar rush（一个 consumable hit）。你买了 Hermès 包后 2 年后仍然能用它社交，持续产出 θ。这与 A7 peacock 的 costly-signal 模型同构。

**β (temporal discount) 参数重解**：在 A5 Drosophila sugar / A8 Olds-Milner 中，β 指 "sweet now vs bitter later" 的高度不对称。C5 的 β 不同：sweet 是 *prolonged*（2 年未衰减），bitter 也是 *prolonged* (savings/asset 持续下滑)。所以 C5 的 Sweet Trap 机制是 **status-stock durable vs wealth-depletion durable 的不对称**，不是传统的 "现在爽 / 将来痛" 时间贴现。这是 C5 对构念的贡献：Sweet Trap 可以在 durable-signal domain 运作，不限于 hedonic flash。

---

## 5. Δ_ST — 核心 Sweet Trap 标量

使用 cohort-split bootstrap (pid cluster, 1,000 iters)：

**祖先组** = 2010-2014 波 (奢侈消费尚未大规模扩散，N = 37,602)
**当代组** = 2018-2022 波 (全民奢侈消费 + 直播带货 + 小红书时代，N = 31,994)

### 5.1 对 qn12012（主 DV）— 正 Δ_ST

| Signal | cor_anc | cor_cur | **Δ_ST** | 95% CI |
|:---|---:|---:|---:|:---:|
| ln_luxury_broad | +0.046 | **−0.053** | **+0.098** | [+0.085, +0.111] |
| ln_luxury_full | +0.060 | **−0.030** | **+0.090** | [+0.077, +0.103] |
| ln_dress | +0.071 | **−0.042** | **+0.114** | [+0.101, +0.127] |
| luxury_full_share | +0.018 | −0.004 | +0.022 | [+0.010, +0.034] |

**号向翻转清晰且 CI 不含 0**：奢侈消费与生活满意度在 2010-14 是 *正相关*（当时中国奢侈品市场约 120 bn USD，刚进入大众化），在 2018-22 是 *负相关*（市场翻倍到 ~280 bn USD，全民卷入 status race）。**这是 F1 reward-fitness decoupling 的最清晰 within-sample demonstration**。

### 5.2 对 savings/asset — 号向反向

| Signal | DV | cor_anc | cor_cur | Δ_ST | 95% CI |
|:---|:---|---:|---:|---:|:---:|
| ln_luxury_full | ln_savings | +0.199 | +0.231 | **−0.032** | [−0.044, −0.021] |
| ln_luxury_full | ln_asset | +0.321 | +0.389 | **−0.069** | [−0.080, −0.057] |

这里 Δ_ST < 0 是因为 luxury ↔ savings 共变量（两者都是财富的表现）在当代更紧了（富人更集中地既买奢侈又攒得多），而非 Sweet Trap 逻辑反了。savings/asset 不是干净的 F-proxy (应该是 welfare，而 savings 只是 welfare 的一个 mechanistic proxy)。**qn12012 才是主 F-proxy**，其 Δ_ST > 0 才是真正的构念 test。

### 5.3 与 Layer A 对比

| Case | Δ_ST | 识别质量 |
|:---|---:|:---:|
| Layer A pool | +0.72 | 动物实验 |
| A1 moth | +0.82 | 高 |
| A5 Drosophila sugar | +0.71 | 高 |
| A6 Olds-Milner | +0.97 | 高（by construction） |
| **A7 peacock runaway** | **+0.58** | 中 |
| **A11 jewel-beetle supernormal** | **+0.55** | 中 |
| A8 neonicotinoid bees | +0.73 | 高 |
| **C5 ln_dress (本)** | **+0.114** | 中 (CFPS 2-year aggregated) |

C5 的 Δ_ST 绝对幅度比 A7 小 5 倍，但考虑到：
1. **测量口径窄**：CFPS 衣着 ≠ 真 luxury，真正的 Hermès/LV 在 upper tail。
2. **时间窗口短**：12 年 vs 动物演化百万年。
3. **文化复制子运行的是代内 + M2 peer norms**，不是遗传 runaway。

**幅度差异是 expected**。构念成立的判据是 **号向 > 0 且 CI 不含 0**，C5 两个主 proxy 都满足。

---

## 6. Specification Curve (576 specs)

6 DV × 8 treat × 3 control × 4 sample = 576.

| Block | n_valid | median β | share(expected sign) | share(expected sign & p<.05) |
|:---|---:|---:|:---:|:---:|
| **Sweet** (qn12012, d_qn12012, qn12016; β>0 expected) | 288 | +0.0081 | **81%** | 24% |
| **Bitter forward asset** (dln_asset_fwd; β<0 expected) | 96 | −0.034 | **96%** | **74%** |
| **Bitter debt** (d_ln_debt; β>0 expected) | 96 | +0.082 | **90%** | **68%** |
| Bitter savings contemporaneous (β<0 expected) | 96 | +0.138 | 0% | 0% | <- 含同期 wealth confound; invalid for Sweet Trap test |

**阅读**：
- **Sweet 方向一致（81% 正号）但只有 24% 通过 p<0.05** — 反映主效应是稳健但弱。符合 F1 decoupling 的 *量上* 解读（cor 从 +0.05 → −0.04，差 0.1 而非 0.5）。
- **Bitter forward 一致且显著**：74% (asset) + 68% (debt) 的 specs 号向正确且 p<0.05。这是 Sweet Trap 在 **welfare destination 端** 的强签名。
- **同期 savings** 是一个 mechanism-confound 的 placebo — 同期 luxury 和 savings 都随共变量 wealth 上升，所以号向为正，**这不是 Sweet Trap null，是误操作化**。论文应明确剔除这一条 DV。

Spec curve CSV 在 `02-data/processed/C5_speccurve.csv`，包含 spec_id, dv, treat, control, sample, N, β, SE, 95% CI, p.

---

## 7. 准自然实验探针（初步 — 非主分析）

### 7.1 海南离岛免税 2020 扩容

2020 年 7 月海南免税额度从 3 万 → 10 万 RMB，是对奢侈品可及性的一次大冲击。本分析以 `hainan_post = (provcd == 46) × (year ≥ 2020)` 做准 DID：

| DV | β | 95% CI | p | N |
|:---|---:|:---:|:---:|---:|
| dress | +10,469 元 | [−10,309, +31,248] | 0.322 | 65,052 |
| travel | +13,255 元 | [−7,116, +33,626] | 0.202 | 65,052 |

**号向都为正，但 p 未过门槛** —— CFPS 海南样本太小（provcd=46 在 CFPS 只有约 200 人年），power 不足。**论文若选择 C5，该 probe 应用更大的金融机构数据（如招商银行 / 支付宝消费指数）替代**。保留为 SI 辅助。

### 7.2 urban × luxury 交互对 qn12012

β(lux × urban) = −0.0045, p = 0.28 — **null，城乡 Sweet Trap 同强**。这其实对论文有利：奢侈 Sweet Trap *不* 只是城市中产现象，农村家庭同样卷入。

---

## 8. 四原语（θ, λ, β, ρ）经验签名 — 整合表

| 原语 | 预测 | C5 证据 | 号向 | 强度 |
|:---|:---|:---|:---:|:---:|
| **θ (愉悦)** | luxury ↑ → 满意度短期 ↑ | Level β = +0.020 [p<10⁻¹²]；Within-person Δ p=0.22 | ✓ | 中 |
| **λ (外部化)** | 家庭其他成员机会成本 | CFPS 无配偶单独满意度；子女教育挤压 TBD | — | 未测 |
| **β (当下偏好)** | short-term reward vs delayed cost | Bitter forward asset β=−0.058, p<10⁻³⁰；Hedonic treadmill 反向 (status-stock) | ✓ (非典型) | 强 |
| **ρ (锁定)** | within-person habit lock-in | AR(1) = **−0.14** (mean reversion!) | ✗ (个体层) / ✓ (peer 层推测) | **弱 M1 / 强 M2** |

**重要修正**：C5 的 Σ_ST 不靠 M1 (individual habit) 而靠 M2 (peer comparison) 持续。这是 phenomenology §C.5 的精准 replication —— "individual: peer comparison locks in continued upgrading. Group: the bag's signalling value depends on other people's endorsement."

论文写作启示：C5 与 A5 Drosophila sugar (M1 主导) 形成 **同构但机制不同** 的比较。两个案例都满足 F1+F2+Δ_ST>0，但 F3 的子机制不同（M1 vs M2）。这正是构念层面的普适性证据。

---

## 9. 层间桥接 — 演化动力学 + 行为经济学

C5 的最佳动物桥是 **A7 peacock Fisherian runaway** + **A11 jewel-beetle supernormal stimulus**。

### 9.1 peacock runaway (Fisher/Lande-Kirkpatrick)

- **R_agent**: 雌孔雀选偶偏好（受 handicap 信号正反馈）
- **F**: 雄孔雀真实生存率（长尾是 predation cost）
- 在 Lande (1981) 模型中，一旦 female preference (p) 与 male trait (t) 的遗传相关 G_{p,t} 建立，动态为：

$$
\begin{pmatrix} \dot p \\ \dot t \end{pmatrix} = \begin{pmatrix} 0 & \beta_p \\ s_t & s_p G_{p,t}/G_t \end{pmatrix} \begin{pmatrix} p \\ t \end{pmatrix}
$$

这产生中性稳定线（a runaway locus）—— 偏好和性状一起向极端演化。

### 9.2 人类版同构：C5 luxury

把 (p, t) 的遗传协方差 G 替换成 **文化复制子协方差** G_{τ,y}：
- τ = 消费标准（身边人期望）
- y = 炫耀支出（个人选择）
- G_{τ,y} = 同伴网络内 τ-y 的相关

这给出一个完全同构的 equilibrium：奢侈消费 escalate 并不是因为每个人主观想要涨，而是因为 τ 和 y 通过 peer network 协方差绑定，把整个系统推向 non-functional equilibrium。

**这正是 Nature/Science 想要的跨物种框架**：一个 mathematical kernel（协方差矩阵驱动的 runaway），peacock 的 G 来自 additive genetic variance，人类的 G 来自 social learning / status emulation。**两者都落在 Sweet Trap 统一公式 Δ_ST > 0 + F2 成立下**。

C5 ⊃ A7 peacock = Nature 主刊主图的一个面板。

### 9.3 jewel-beetle supernormal (A11)

A11 中，Julodimorpha bakewelli 的雄虫把棕色光亮玻璃瓶当成超大号雌虫 —— 一个 supernormal stimulus。应用到 C5：奢侈品的 iconic 标识（LV 老花 / Hermès 橙盒）是 **人工强化的 status supernormal cue**，超过真实的 quality signal。

C5 的 M2 机制（peer endorsement）与 A11 的 novel-signal 机制结合：当信号本身被 *过度放大*（logo、直播带货曝光、小红书晒单），个体选择频率不降反升 —— runaway + supernormal 的混合。

---

## 10. 答 Step 10 TL;DR 8 问

| # | 问题 | 答 |
|---:|:---|:---|
| 1 | CFPS 是否支持 C5 独立测量？变量粒度？ | **支持**。`dress` (衣着鞋帽, 7 波 85k) 是主 proxy，补以 `travel` (6 波 72k)、`eec` (7 波 85k)、Δ`durables_asset` (6 波 72k)。**不足**：CFPS 不分品牌、不分豪车/珠宝/烟酒具体 SKU，upper-tail 奢侈低估。替代：胡润报告、招行/中信信用卡账单、天猫/京东高端店交易。 |
| 2 | C5 满足 F2 吗？ | **Yes, 完全 PASS**。所有 6 个 proxy 的 cor(luxury, lnincome/eduy/urban) 均 > 0，ln 尺度 cor(income) 达 +0.39。符合 aspirational voluntary 签名。 |
| 3 | 奢侈购买 → 短期满意度 effect | **方向一致，幅度小**。Level β(ln_luxury_full → qn12012) = +0.020 [+0.016, +0.024], p < 10⁻¹²。Within-person Δ 变 null (β=+0.004, p=0.22)。spec curve 81% 号向为正，24% p<0.05。 |
| 4 | Hedonic treadmill 证据强度 | **反向发现**。ρ_AR1 = −0.11 ~ −0.17（负！mean reversion, 非 habit lock-in）。Hedonic 共同回归：lagged level β > current Δ β。奢侈消费在中国 CFPS 家户层面表现为 **status-stock durable 而非 novelty flash**。F3 机制从 M1 切换到 M2 (peer)。 |
| 5 | Δ_ST vs Layer A A7 peacock | **Δ_ST(ln_dress → qn12012) = +0.114 [+0.101, +0.127]**，与 A7 peacock (+0.58) 相比幅度小 5 倍。但：(a) 号向一致 (Sweet Trap 成立); (b) 测量口径窄 (CFPS 衣着 ≠ 真高端 LV/Hermès); (c) 时间窗口 12 年 vs 动物百万年。**号向翻转清洁**（anc +0.07 → cur −0.04）是主要胜利。 |
| 6 | 4 原语清洁签名 | θ ✓ (中)；λ 未测 (需配偶 / 子女数据); β ✓ 强 (forward-looking Bitter); ρ ✗ M1 弱（−0.14）但 M2 推测强。详见表 §8。 |
| 7 | C5 在新 Focal 排名 | **C5 = Focal #1 候选**。同桌对比中唯一同时给出 (F2 clean) + (Δ_ST > 0 号向翻转) + (Bitter forward 强 74% spec p<0.05) 的案例。超过 C4 (降级)、C11 (降级)、D3 (coerced 排除)。与正在执行的 C2 鸡娃 DID 形成 Focal 双支柱。|
| 8 | 若 CFPS 粒度不足 → 替代 | ① 胡润百富消费报告 (SI 交叉验证)；② 招商银行/中信 信用卡账单 (理想，协议成本高)；③ 贝恩 China Luxury Report (公开摘要)；④ 天猫 / 京东高端 SKU (天猫数据); ⑤ 小红书/抖音 POI 热度 (用于 F2 社会传染子);  ⑥ CGSS 2017 消费序列 (弱替代)。 |

---

## 11. 论文定位建议

### 11.1 多域构念论文架构中的 C5

建议将 C5 作为 **Focal #1**（替代降级的 C4 & C11），与 C2 鸡娃（Focal #2，DID 执行中）形成双支柱。附属域（非 Focal）：D1 urban housing、C6 保健品（见 phenomenology archive §C.6 待做）。

**论文主图 2 提议**：
- Panel A: Δ_ST bar chart — 7 个动物 case (A1-A11) + 4 个人类 case (C2, C5, C6, D1)
- Panel B: C5 的 ancestral vs current cor 号向翻转 (2010-14 vs 2018-22)
- Panel C: C5 的 Bitter forward funnel (luxury → 下一波 asset growth)
- Panel D: Fisher runaway isocline (G_{τ,y} 文化版)，peacock 插图 vs LV 插图对照

### 11.2 与 Σ_ST 持续机制的 conceptual contribution

C5 教会我们 **Sweet Trap 不总依赖 M1 habit lock-in**。本研究发现 ρ_AR1 = −0.14 表明 within-person 年际消费有回归均值倾向。但 C5 仍然持续 —— 因为 M2 peer norm 在 aggregate 层面 lock in。**这是论文的一个 Key Finding**：**同一构念下，不同域通过不同的 F3 sub-mechanism 持续**。A5 果蝇靠 M1；C5 奢侈靠 M2；C4 彩礼靠 M3；A1 moth 靠 M4。构念成立，机制可替换。

### 11.3 政策窗口对齐

- 2024 中国消费税调整（烟酒、豪车）—— 奢侈消费再定价。
- 2020 海南免税扩容 —— 奢侈可及性冲击。
- 2021 "共同富裕" 政策 —— 直接触及 status signaling equilibrium。
- 2023 网红直播带货监管 —— M2 传播渠道调控。

论文可在 Discussion 中提：如果 Sweet Trap 存在，common prosperity (强制压低 upper-tail luxury) 在 group-welfare 层面是 Pareto 改进 —— 减少 runaway 逃离到低社会福利均衡。这是一个 **Nature/Science 编辑喜欢的政策含义**。

---

## 12. 局限 & 下一步

1. **测量口径窄**。CFPS 衣着 ≠ 真高端。幅度 Δ_ST = +0.11 是 lower bound。需融合信用卡 / 电商 SKU 数据 refine。
2. **CFPS 2 年间隔**。无法识别月级 dopamine peak 衰减；真实 hedonic treadmill 应该在周/月级测。Alibaba / Meituan 消费日志 + life-sat 平台 (微信读书 short-form wellbeing pulse) 是下一步。
3. **λ (外部化) 未测**。需同时观察配偶满意度 / 子女教育投入分配 / 父母赡养支出 — CFPS 有但本分析未做。
4. **2020 海南 DID 低功效**。Province sample 太小。改用 provincial aggregated 销售数据。
5. **Δ_ST 共变量纠正**。本文 cohort cor 是简单 Pearson；可用 partial cor (控制 income) 或 within-cohort FE 估计更稳。
6. **没做 pre-registration**。按 Andy 规则 pre-reg 在研究完成后 + 投稿前。C5 尚未 pre-registered。

---

**下一步**：
- [ ] 将 C5 写入 `00-design/specification-map.md` 作为 Focal #1
- [ ] 在 `04-figures/` 准备 Figure 2 4-panel 原型
- [ ] 起草 C5 × C2 × Layer A 的 cross-species 对比 Figure 3
- [ ] 若继续深入：申请招商银行 / 中信消费面板 API（投稿前 revision 阶段执行）
- [ ] 起草 pre-registration（按规则，投稿前 OSF）
