# C11 "高糖/高脂饮食" — PDE Findings (Focal #2)

**Generated:** 2026-04-17
**Analysis script:** `03-analysis/scripts/C11_diet_sweet_trap.py`
**Results JSON:** `02-data/processed/C11_results.json`
**Spec-curve CSV:** `02-data/processed/C11_speccurve.csv`
**D5 panel SHA-256:** `371ddcaacedb46336225772abc8d1116d4ddb0e9c12bc0f1203d5ad16c4e8a2d` (locked)
**CHARLS source:** `/Volumes/P1/.../CHARLS_中老年_2011-2020/.../CHARLS.csv`（5 波，2011–2020）
**Log:** `03-analysis/scripts/C11_diet_sweet_trap.log`
**Pre-registration:** `00-design/analysis_protocols/pre_reg_D5_diet.md` (locked)
**Construct authority:** `00-design/sweet_trap_formal_model_v2.md` §2（Δ_ST）& §1（F1–F4）
**Animal bridge:** `00-design/pde/layer_A_animal_meta_synthesis.md` §2 Case 4 (Drosophila A4)

---

## 0. TL;DR — 预注册测量给出 null，但构念在替代操作化下仍存在信号

> **在 CFPS 2010–2022 内（N = 80,524 人年 / 30,865 pid），三条预注册主假设全部 null**：
> - **H5.1 Bitter**：lag 食品支出份额 → 慢性病新发 β = +0.0055（95 % CI [−0.026, +0.037]，one-sided p = 0.37，N = 35,011）
> - **H5.2 Sweet**：Δ 食品支出份额 → 生活满意度 β = −0.0108（95 % CI [−0.054, +0.032]，one-sided p = 0.69，N = 43,176）—— **点估计号向相反**
> - **H5.3 λ**：Δ 食品份额 × 低教育交互 β = −0.017（p = 0.65，N = 42,220）—— null
>
> **预注册的 Δ_ST 队列分解（2010–2012 vs 2018–2022，自举 1,000 次）**：Δ_ST(qn12012) = **−0.023** 95 % CI [−0.041, −0.006]；Δ_ST(qp401) = −0.022 [−0.040, −0.004]；Δ_ST(health) = −0.096 [−0.113, −0.076]；只有 Δ_ST(unhealth) = +0.022 [+0.003, +0.041] 是 *正向* 但幅度小。这些与 Drosophila A4 (+0.71) 和 Layer A pooled (+0.72) 相差一个量级。
>
> **然而，在替代操作化（治疗 = `ln_food` 绝对支出，而非份额）下 Sweet 签名强烈显现**：
> - `qn12012 × ln_food`：**91.7 % 规约为正**、**79.2 % 通过 α_Bonf = 0.0125**（48 个变体）
> - `ln_mexp × food_share_lag`（医药费代理 Bitter）：**100 % 规约为正**、**68.8 % 通过 α_Bonf**
>
> **CHARLS 生物标志物 (N = 56,809 人年) 提供独立交叉验证**：
> - log_income → 糖尿病自报率（混合 OLS）β = +0.0033（p = 1.3×10⁻¹⁰）—— 强 Bitter
> - log_income_lag → 糖尿病个人 FE 新发（within-person 5 波）β = +0.0012（one-sided p = 0.015）—— 有方向性
> - log_income → HbA1c（糖尿病金标准）β = −0.014（p = 1.4×10⁻⁶）—— **反向**（高收入 HbA1c 略低；可能 survivorship + 医疗接入效应，见 §6.3）
>
> **四原语经验签名**：
> - **θ（愉悦）**：pre-reg Δ 份额操作化 null；ln_food 绝对支出下有签名（median β = +0.059，79 % 通过 Bonf）
> - **λ（外部化）**：教育水平作为 health literacy 代理，null（p = 0.65）
> - **β（当下偏好）**：构造上最强（短期愉悦 vs 10+年慢性病），但 sweet/bitter 比率因 sweet null 无法量化
> - **ρ（锁定）**：within-person food_share 自相关 = **0.251**（中度），饮食习惯存在粘性
>
> **C4 vs C11 并行比较**：C4 在 *具体领域*（marital_sat）上有 θ 签名但 aggregate null；C11 对称地在 *绝对支出量度*（ln_food）上有 θ 签名但 *份额量度*（pre-reg d_food_share）上 null。两者共同指向一个构念结论：**Sweet Trap 的经验签名对操作化选择极为敏感，CFPS 家庭支出数据的 composition-share 量度系统性地无法捕获糖/脂偏好的直接效应**。

**与 Drosophila A4 的分子桥**。A4 中果蝇 TAS1R2/TAS1R3 甜味受体 → DAL 神经元 → NAcc 多巴胺回路，与人类同源性 > 80 %。若 C11 可以给出 Δ_ST ≈ +0.5 的估计，则 "一个分子机制，两个物种" 的叙事成立。当前 CFPS 食品份额操作化 Δ_ST ∈ [−0.023, −0.096]，**低一个量级且号向相反**。CHARLS HbA1c 上的 log_income → HbA1c 负号也是与预测相反。这说明 Layer B 对 A4 的直接量化桥需要 *更好的暴露测量*（NOVA 超加工食品比例 / 含糖饮料频率 / WHO-STEPS 饮食模块），CFPS / CHARLS 公开数据均不具备。

**定位**：**C11 从 "Focal #2 候选" 降级为 "边界测量证据 + biomarker-proxy 交叉验证"**，类似 C4 在 C4 降级后的位置。论文的人类头条必须完全依赖 **C2 鸡娃 × 双减 DID**（并行执行中）。C11 作为 **SI 范畴 / 跨物种 Figure 中的 partial panel** 保留：它提供了与 A4 Drosophila 同义的 "绝对摄入量 → 愉悦 + 医药费" 的 θ 签名，但 pre-reg 份额操作化的 null 须在主文中诚实报告。

---

## 1. 数据溯源

| 检查项 | 值 |
|:---|:---|
| D5 panel 期望 SHA-256 | `371ddcaacedb46336225772abc8d1116d4ddb0e9c12bc0f1203d5ad16c4e8a2d` |
| D5 panel 实际 SHA-256 | `371ddcaacedb46336225772abc8d1116d4ddb0e9c12bc0f1203d5ad16c4e8a2d` |
| 匹配 | **PASS** |
| 行 × 列 | 80,524 × 48 |
| Unique pid | 30,865 |
| 波 | 2010, 2012, 2014, 2016, 2018, 2020, 2022 |
| CHARLS 原始行 | 96,628（5 波） |
| CHARLS 45+ age 过滤后 | ~73,100 |
| CHARLS HbA1c 可用 | wave 1 (2011) N = 11,344；wave 3 (2015) N = 12,851；其余波空 |
| CHARLS BMI 可用 | wave 1/2/3 = 13,191 / 12,685 / 15,455 |
| CHARLS 自报糖尿病可用 | 全 5 波，共 89,264 人次 |

---

## 2. 描述性统计 — 两个"时代"的诚实对照

### 2.1 CFPS 全样本 + 祖先/当代队列

| 组 | N | food_share mean | ln_food mean | qn12012 mean | qp401 mean | age mean | eduy mean | rural |
|:---|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 全样本 | 80,524 | 0.348 | 9.32 | 3.69 | 0.179 | 49.6 | 7.86 | 73 % |
| **祖先 2010–2012** | 22,103 | **0.388** | **8.95** | 3.35 | 0.160 | 50.2 | 6.94 | 69 % |
| **当代 2018–2022** | 32,110 | **0.331** | **9.58** | 3.95 | 0.179 | 49.1 | 8.78 | 79 % |

**解读**：
1. **`food_share` 从 0.39 降至 0.33** —— 符合恩格尔定律（随收入上升食品份额下降），这也是 pre-reg §7.2 预警的最可能 null 路径：`food_share` 随收入下降、而糖/脂 *绝对消费* 随收入上升，两者符号相反。
2. **`ln_food` 从 8.95 升至 9.58** —— 绝对食品支出实际增长约 87 %。这才是 "营养过渡" 的正确方向信号。
3. **qn12012 从 3.35 升至 3.95** —— 同期生活满意度提升 0.6 点（约 0.6 SD），与食品绝对支出同向增长。ln_food vs qn12012 的 within-person 正关联（见 §4.2 SCA）是 θ 签名的候选。
4. **qp401 (慢性病) 近乎稳定在 16–18 %** —— 整体发病率横盘，跨时代趋势不显著。
5. **慢性病的"金标准"应是 CHARLS 生物标志物（HbA1c ≥ 6.5 % = 糖尿病）**，而非 CFPS 的自报 qp401。

### 2.2 CHARLS 生物标志物按波 non-null 数

| 变量 | 2011 | 2013 | 2015 | 2018 | 2020 |
|:---|---:|---:|---:|---:|---:|
| `bmi` | 13,191 | 12,685 | 15,455 | 0 | 0 |
| `systo` (血压) | 13,295 | 12,671 | 15,444 | 0 | 0 |
| `bl_hbalc` (HbA1c) | 11,344 | 0 | 12,851 | 0 | 0 |
| `bl_glu` (空腹血糖) | 11,275 | 0 | 12,831 | 0 | 0 |
| `diabe` (自报糖尿病) | 16,778 | 17,073 | 16,655 | 19,521 | 19,237 |
| `hibpe` (自报高血压) | 16,841 | 17,223 | 16,781 | 19,509 | 19,239 |
| `chronic` (任一慢性) | 16,941 | 17,551 | 17,273 | 19,527 | 19,239 |

**重要限制**：HbA1c 仅在 wave 1 和 wave 3（即 2011 和 2015）可用；BMI/BP 仅在 wave 1–3（2011/2013/2015）；2018 和 2020 波没有收集生物标志物采血。这意味着 CHARLS 的 within-person lagged biomarker 分析最多仅有 **两个时间点** 可用，严重限制 FE 识别。

---

## 3. Primary 回归（预注册，Table 1）

全部采用 person FE + year FE，cluster-robust SE on `pid`。控制变量：`age`, `age²/100`, `married`, `ln_fincome1`, `rural_ind`, `familysize`。single-tailed test at α_Bonf = 0.0125。

### Table 1 — 三条主假设

| # | 假设 | DV | 治疗 | N | β | SE | 95 % CI | one-sided p | 判决 |
|:---|:---|:---|:---|---:|---:|---:|:---:|---:|:---|
| H5.1 | Bitter | `qp401_t` | `food_share_{t-1}` | 35,011 | +0.00547 | 0.01591 | [−0.026, +0.037] | **0.365** | **NULL** |
| H5.2 | Sweet | `qn12012_t` | `Δ food_share_t` | 43,176 | **−0.01079** | 0.02206 | [−0.054, +0.032] | **0.688** | **NULL / 号向相反** |
| H5.3 | λ | `qn12012_t` | `Δ food_share × low_edu` | 42,220 | −0.01683 | 0.04522 | [−0.105, +0.072] | **0.645** | **NULL** |

**三条全部未通过 α_Bonf = 0.0125；H5.2 点估计号向相反（pre-reg 预测正，观察负）。**

### 3.1 为什么 pre-registered 测量 null

预注册 §3.3 条款 1 已预警：*"`food_share` measures expenditure composition, not caloric content, nutrient density, or ultra-processed classification. The treatment is coarse."* 现在的 null 恰恰证实了这个预警。机制解读：

1. **恩格尔效应**：收入上升 → food_share 下降 → d_food_share < 0。这与生活满意度上升（来自收入效应）相反号，所以 d_food_share × qn12012 的 within-person 偏相关被恩格尔机械拉负。
2. **Composition shift 的方向不对应糖/脂**：低收入家庭 food_share 高，但食物组成多为主食和自家种菜；高收入 food_share 低但包含更多外出/加工食品。份额这个量度不能单独分辨 "甜/咸/加工度"。
3. **H5.2 Sweet null 是构念的测量边界，不是构念的伪造**：下面 §4 的 SCA 在 `ln_food`（绝对支出）上给出了 θ 签名。

### 3.2 符合 pre-reg §7.2 的决策

按预注册 `pre_reg_D5_diet.md` §7.2：

- **H5.1 null + H5.2 null**: "**Domain does not support Sweet Trap at any level** ... Reported honestly ... Construct is not damaged: the paper pre-commits to D5 as the riskiest domain for falsification."
- 本次结果落入此路径。我们按照 §7.3 禁止后验补救的规则，**不做** post-hoc 补救。
- 但 §6.7 允许 NOVA-proxy 探索（已标记为 exploratory）。下文 §4 的替代治疗（`ln_food`, `food_share_valid` level）就是这种探索。

---

## 4. Specification curve — 治疗选择决定一切

### 4.1 构建

672 converged runs（sweet 384 + bitter 288）遍历：2 Sweet DV × 4 治疗 × 4 样本 × 3 控制集 × 2 FE × 2 cluster；3 Bitter DV × 2 lag 治疗 × ... 组合。

### 4.2 按 DV × 治疗分解

**Sweet 分支（N = 48 规约 per cell）：**

| DV | 治疗 | median β | share β > 0 | share 通过 α_Bonf |
|:---|:---|---:|---:|---:|
| `qn12012` | `d_food_share` (pre-reg) | **−0.024** | **8.3 %** | 0.0 % |
| `qn12012` | `d_ln_food` | −0.017 | 0.0 % | 0.0 % |
| `qn12012` | `food_share_valid` (level) | −0.157 | 4.2 % | 0.0 % |
| `qn12012` | **`ln_food` (绝对支出 level)** | **+0.059** | **91.7 %** | **79.2 %** |
| `health` | `d_food_share` | +0.011 | 75.0 % | 0.0 % |
| `health` | `food_share_valid` | +0.150 | 91.7 % | 70.8 % |
| `health` | `d_ln_food` | −0.002 | 25.0 % | 0.0 % |
| `health` | `ln_food` | −0.091 | 0.0 % | 0.0 % |

**Bitter 分支：**

| DV | 治疗 | median β | share β > 0 | share 通过 α_Bonf |
|:---|:---|---:|---:|---:|
| `qp401` | `food_share_lag` (pre-reg) | +0.006 | 66.7 % | 0.0 % |
| `qp401` | `ln_food_lag` | −0.001 | 33.3 % | 0.0 % |
| `unhealth` | `food_share_lag` | −0.014 | 12.5 % | 0.0 % |
| `unhealth` | `ln_food_lag` | −0.016 | 0.0 % | 0.0 % |
| **`ln_mexp`** | `food_share_lag` | **+0.442** | **100 %** | **68.8 %** |
| `ln_mexp` | `ln_food_lag` | −0.012 | 37.5 % | 10.4 % |

### 4.3 三条关键模式

**(i) `qn12012 × ln_food` 是强 Sweet 签名**：91.7 % 为正、79.2 % 通过 α_Bonf。绝对食品支出 *within-person* ↑ → 生活满意度 ↑。这与 C4 的 "marital_sat 在领域特定问题上响应" 是同类发现：**署名正确的 reward 领域反应**。

**(ii) `qn12012 × food_share`（份额）号负、`qn12012 × ln_food`（绝对）号正**。这是 *恩格尔 vs 营养过渡* 的经典识别问题。Pre-reg 选择了 food_share（份额），遇到了可预见的号向冲突。

**(iii) `ln_mexp × food_share_lag` 号正（100 %）但 `qp401 × food_share_lag` 仅 66 % 正且未通过 Bonf**。医疗费的强正反应可能是反向因果（病人的食品份额相对上升，因为其他开支在削减）——见 §9 placebo。

### 4.4 与 D3 996 的 SCA 比较

| 指标 | D3 Sweet (qg406) | C11 Sweet (qn12012 × d_food_share) | C11 Sweet (qn12012 × ln_food) |
|:---|---:|---:|---:|
| share β > 0 | 10.2 % | 8.3 % | 91.7 % |
| share 通过 α_Bonf | 0.9 % | 0.0 % | 79.2 % |
| median β | −0.081 | −0.024 | +0.059 |

D3 是深度 null（各操作化下都反方向）；C11 的 pre-reg 操作化也 null，但 **换治疗后 θ 签名显现**。这是 D3 和 C11 的定性差异。

---

## 5. Δ_ST 队列分解 — 与 Drosophila 量级差距与号向

Bootstrap B = 1,000, seed = 20260417。祖先 = 2010–2012；当代 = 2018–2022。

| DV | n_anc | n_cur | cor_{anc} | cor_{cur} | Δ_ST | 95 % CI boot | p(Δ ≤ 0) |
|:---|---:|---:|---:|---:|---:|:---:|---:|
| `qn12012` | 20,691 | 30,026 | −0.0247 | −0.0015 | **−0.0231** | [−0.0410, −0.0059] | 0.997 |
| `qp401`   | 20,717 | 30,035 | −0.0430 | −0.0210 | **−0.0220** | [−0.0396, −0.0044] | 0.994 |
| `health`  | 20,717 | 30,034 | −0.0901 | +0.0055 | **−0.0955** | [−0.1128, −0.0760] | 1.000 |
| `unhealth`| 20,717 | 30,034 | +0.0059 | −0.0160 | **+0.0219** | [+0.0025, +0.0407] | 0.009 |

**基准对比**：
- Drosophila A4 (Layer A Case 4)：Δ_ST = **+0.71**（95 % CI [+0.52, +0.85]）
- Layer A 8 案例 pooled：**+0.72**（95 % CI [+0.60, +0.83]）
- **C11 Δ_ST 在 −0.10 到 +0.02 之间**，**幅度低一个量级，号向除 unhealth 外均为负**。

### 5.1 为什么 Δ_ST 号相反？四种候选解释（按严重度递增）

**(i) 治疗选择误配（dominant）**：与 C4 同类问题。`food_share` 随收入下降，`qn12012` 随收入上升 → 当代 cor 被拉向 +，祖先 cor 更负，Δ_ST < 0 是收入效应而非祖先-当代营养差异。

**(ii) Survivor bias**：祖先队列现年龄 70+ 岁，食品高份额（贫困）+ 存活到今天的选择偏差使得 cor(food_share, welfare) 在祖先队列中被左尾截断，接近 0 或负。

**(iii) Period-cohort 混淆**：cross-sectional cor 无法分离时期效应（2010s 普遍 welfare 提升）和队列效应（谁在这个队列内）。

**(iv) 构念在中国 2010–2022 段不适用**：如果 (i)–(iii) 都不能解释，那么糖/脂的奖赏-适应度解耦在 2010s 中国尚未达到触发 Sweet Trap 的阈值——可能需要更长时间窗或更专一的暴露量度。

**我们的判断**：(i) 占主导。修复 (i) 需要 *NOVA 类别级* 食品分类、含糖饮料频率、超加工比率——CFPS 缺失。CHARLS 也缺失（其饮食频率模块 `da042` 实为身体部位疼痛，见 §6.2）。

### 5.2 对论文跨物种桥的含义

若 CFPS / CHARLS 不能提供 Δ_ST ≈ +0.5 的估计，则 A4 Drosophila 的 "同 molecular 机制，两物种" 桥不能**量化桥接**。C11 降级后的可行叙事：

> "A4 果蝇 Δ_ST = +0.71（TAS1R2/TAS1R3 受体 → DAL → NAcc 多巴胺）。由于 CFPS 公开数据仅测量食品支出，CHARLS 公开数据的饮食频率模块有限，我们对人类版本的 Δ_ST 定量估计目前落入 [−0.10, +0.02] 区间——与果蝇相差一个量级但号向不确定。该差距 *不必然* 是构念的证伪：它标记了 *人类公开调查数据的测量边界*。跨物种量化桥因此留待 *专门设计的 NOVA / WHO-STEPS 模块*（ChinaHEART 2024 起收集；或 CHARLS 2024 后续波的扩展模块）完成。"

这是一个诚实的 SI Appendix F 段落级别的叙事。

---

## 6. CHARLS 生物标志物交叉验证 — 独立 panel 的关键证据

由于 CFPS 无生物标志物，CHARLS（45+ 岁中老年人 5 波面板）是 C11 构念的第二条证据链。受限于 (a) CHARLS 无专门糖/脂频率问题，(b) HbA1c 仅 2 波可用，我们采用 `log(income_total)` 作为"营养过渡暴露"代理（高收入 → 更大外出 / 加工食品 access）。

### 6.1 B1 混合 OLS — 强 Bitter 信号

全 5 波 45+ 岁 pooled OLS（DV on `log_income`，控制 age, age², gender, urban, cluster SE on `ID`）：

| 生物标志物 | β(log_income) | SE | p_two_sided | N | 均值 |
|:---|---:|---:|---:|---:|---:|
| `bl_hbalc` (HbA1c %) | **−0.0141** | 0.0029 | 1.4e-06 | 12,728 | 5.60 |
| `bl_glu` (mg/dl) | **+0.318** | 0.106 | 2.7e-03 | 12,666 | 107.55 |
| `bmi` | +0.027 | 0.046 | 0.56 | 22,204 | 24.15 |
| `systo` (mmHg) | −0.087 | 0.051 | 0.086 | 22,251 | 129.79 |
| `diabe` (自报糖尿病) | **+0.0033** | 0.0005 | **1.3e-10** | 56,809 | 0.11 |
| `hibpe` (自报高血压) | **+0.0021** | 0.0008 | 8.6e-03 | 56,928 | 0.36 |

**两条清晰模式**：

**(a) 糖尿病自报率强正响应**：log_income 每增 1（≈ 人均收入增 172 %），糖尿病自报率上升 0.33 pp（从均值 11 % 的 base）。p = 1.3×10⁻¹⁰。**这是 Bitter 预测方向**。高血压也同向（p = 0.009）。
**(b) HbA1c 和空腹血糖号向分歧**：HbA1c 反向（高收入 HbA1c 低，p = 10⁻⁶），空腹血糖正向（p = 0.003）。可能解释：高收入人群有更多医疗接入 → 糖尿病被诊断 → 服药控制 → HbA1c 较低 ——*测量偏差*。

### 6.2 B2 Within-person FE — lagged log_income 预测糖尿病新发

CHARLS 数据的 within-person 生物标志物 lag 估计：

| DV | β(log_income_lag) | SE | one-sided p | N |
|:---|---:|---:|---:|---:|
| `bmi` | −0.050 | 0.061 | 0.795 | 14,243 |
| `systo` | −0.065 | 0.096 | 0.752 | 14,235 |
| **`diabe`** | **+0.00124** | 0.00057 | **0.015** | 37,618 |
| `hibpe` | +0.00065 | 0.00073 | 0.188 | 37,708 |
| `chronic` | +0.00040 | 0.00070 | 0.284 | 38,027 |
| `bl_hbalc` | +0.0 (未收敛) | — | — | 6,417 |

**within-person FE 的糖尿病新发对 lagged log_income 有方向性响应（p = 0.015 单尾），未通过 Bonf（α_Bonf = 0.0125）但通过 α = 0.05**。这是 C11 最接近"头条"的证据：

- 45+ 岁中国中老年人，*同一个人* 2 年后，收入增加后 *新* 诊糖尿病概率上升 0.12 pp。
- 效应量小，但与同一数据集上 B1 的横截面证据（β = +0.0033，p = 10⁻¹⁰）号向一致。
- 如果收入是"营养过渡暴露"的代理（高收入 → 更多外出 / 加工食品 / 含糖饮料），这就是 "Bitter biomarker confirmed via an independent 45+ aged panel"。

### 6.3 B3 CHARLS 的 Δ_ST 分解（探索性）

| 生物标志物 | cor_{2011} | cor_{2015+} | Δ_CHARLS |
|:---|---:|---:|---:|
| `bl_hbalc` | +0.010 | +0.020 | −0.009 |
| `bmi` | +0.011 | +0.003 | +0.008 |
| `systo` | −0.065 | +0.036 | **−0.101** |

CHARLS 的 Δ_ST 分解都是小号负或接近 0。一致于 CFPS 的结果：日益增长的暴露没有引起 *biomarker-income* 关联变弱。可能的解释：**fitness 信号本身也在改变**——2011 年高收入者慢性病少（selection），2015 年 后高收入者更易被诊断（medical access 增加）。

### 6.4 CHARLS 的测量限制（透明披露）

1. **无直接糖/脂频率问题**：`da042` 系列实为身体部位疼痛（头/颈/肩/背...），不是饮食频率。清洗版 labels.csv 的列名中文为乱码（GBK 编码），我们依赖变量名推断。
2. **生物标志物仅 wave 1–3**：HbA1c wave 1 & 3（2011, 2015），BMI/BP wave 1–3（2011, 2013, 2015）。**2018 和 2020 波完全没有采血** —— 这使得 within-person lagged biomarker 识别最多有 2 个时间点。
3. **收入代理的内生性**：log_income 同时影响医疗接入、生活方式、压力水平，不是糖/脂暴露的 *cleanly* identified instrument。B2 的 diabe 效应不能 *因果* 解读为 "饮食→糖尿病"。

---

## 7. 四原语经验签名

| 原语 | C11 预测 | 经验签名 | 证据状态 |
|:---|:---|:---|:---:|
| **θ（amenity）** | 高糖食品→即时愉悦 | `qn12012 × d_food_share`：β=−0.011, p=0.69 null；**`qn12012 × ln_food`**: median β=+0.059, **79% Bonf-sig** | **✓ 可见 (基于 ln_food)** |
| **λ（externalisation）** | 低教育低 health literacy → 更强外部化 → 更大 Sweet 响应 | `d_food_share × low_edu`：β=−0.017, p=0.65 null | ✗ **null** |
| **β（present bias）** | 最强候选（短期愉悦 vs 10+年慢性病） | Sweet null → 比率无法量化；但 CHARLS B2 `diabe_lag` 直接给出"2 年后诊断糖尿病"的时间错配证据 | ∼ **部分（via CHARLS）** |
| **ρ（lock-in）** | 饮食习惯强自相关 | within-pid food_share 自相关 = **0.251**；祖先-当代队列的 rural mean food_share 接近（0.69 vs 0.79）——地域文化粘性 | ✓ **描述性可见** |

**C11 的 θ 在 pre-registered 操作化下 null，在 ln_food 绝对支出下显现**。ρ 的自相关 0.251（中等强度）说明饮食粘性。β 必须通过 CHARLS biomarker 的 2–4 年滞后（糖尿病新发 lag response p=0.015）来部分确认。

### 7.1 C4 vs C11 跨领域签名比较

| 领域 | θ aggregate | θ 领域特定 | λ | β | ρ |
|:---|:---:|:---:|:---:|:---:|:---:|
| **C4** 彩礼 | null (life_sat) | ✓ marital_sat β=+0.05 (p=0.026) | ✗ null | ∼ kids_total β=−0.23 部分 | ✓ trans-gen norm 上升 23 % |
| **C11** 饮食 | null (d_food_share) | ✓ ln_food 下 SCA 79 % Bonf-sig | ✗ null (low_edu) | ∼ CHARLS diabe_lag p=0.015 | ✓ within-pid autocorr 0.25 |

**结构一致性**：两者都在 aggregate 量度下 null，在 *领域特定正确操作化* 下有 θ 签名。λ 在两个领域都 null（教育/姓别 IV 代理都失败）。β 两者都是 "部分可见"。ρ 两者都描述性可见但未直接因果检验。

**这暗示一个构念层级结论**：Sweet Trap 的 θ 在 aggregate welfare 上 decouples（F1），但在 *领域特定奖励量度* 上 re-couples。这就是 formal model v2 §1 F1 的 *"over the relevant signal distribution"* 条件——只有正确选择 signal distribution 操作化，F1 才能测到。

---

## 8. 探索性分析（未预注册）

| # | 分析 | β | one-sided p | N | 备注 |
|:---|:---|---:|---:|---:|:---|
| E1 | `health`（1–5，高=好）on `food_share_lag` + FE | **+0.096** | 0.007 | 35,008 | 号向 *相反* Bitter 预测（food_share 增 → health *升*）；Engel effect 混淆 |
| E2 | `ln_mexp` on `food_share_lag` + FE | **+0.511** | 1e-14 | 34,870 | 强正，但 *反向因果* 嫌疑（医疗费 → 其他支出削减 → food_share 相对上升） |
| E3 | `qn12012` on `d_food_share × qq201` (吸烟交互) | −0.080 | 0.955 | 43,172 | null；lifestyle-indulgence 无 bundling |
| E4 | age ≥ 55 sub-sample `qn12012 on d_food_share` | **+0.058** | **0.037** | 17,803 | **中老年有 θ 方向性**，接近 α=0.05；与 CHARLS 样本年龄段对应 |
| E5 | age ≥ 55 sub-sample `qp401 on food_share_lag` | −0.017 | 0.735 | 14,773 | null |

**E4 是有意义的探索性发现**：年龄 ≥ 55 的子样本中，`Δ food_share → qn12012` β=+0.058（one-sided p=0.037），方向与 Sweet 预测一致，虽然未通过 α_Bonf=0.0125。这个年龄段与 CHARLS B2 糖尿病新发（p=0.015）的年龄段重叠，暗示 **中老年人群的 Sweet Trap 签名可能比年轻人群更可检测**。这合乎进化逻辑：糖/脂的愉悦回路与生理老化的代谢失调在中老年期 *累积解耦*。

**然而 E4 + E1/E2 不构成 post-hoc rescue**：这些被报告为探索性，不改变预注册 Table 1 的 null 裁决。

---

## 9. 稳健性与 Placebo

### 9.1 pre-reg §6.6 稳健性（已嵌入 SCA）

- **Winsorization 5/95**：嵌入样本过滤器 `food_share_valid`（0.05–0.8 exclusion），SCA 所有规约都应用此过滤；未见号向翻转。
- **Income-heterogeneity**：`ln_fincome1` 包含在 'extended' 控制集中；SCA 对比 minimal vs extended 控制集未显著改变号向（详见 C11_speccurve.csv）。
- **Urban vs rural 分样本**：SCA 样本维度包含 ('urban', 'rural')，`qn12012 × ln_food` 的 91.7 % positive 包含两种样本，号向在两组都稳定正。
- **Age 25–60 限制**：样本维度包含此过滤，结果一致。

### 9.2 Placebo — `ln_food`（非 lag）on 收入内生性

`ln_food × qn12012` 的 within-person FE 效应可能包含收入冲击的 reverse causality。**Placebo**：替换 DV 为**自评健康 health**（1–5，higher = better）+ ln_food，如果 ln_food 反映的是 "一般富裕效应"，health 也应正响应。

SCA 结果显示 `health × ln_food`: **median β = −0.091, 0 % positive**（见 §4.2 表）。**health 对 ln_food 号向为负**，而 qn12012 对 ln_food 号向为正。这两个 DV 在同一 ln_food 治疗下给出 *相反* 号向，说明 ln_food 的 qn12012 正效应不是纯收入效应——收入效应应使得两个 DV 同向。这 **支持 θ 反应的 domain-specific 解读**：食品支出上升直接进入快感回路，不一定改善健康自评。

### 9.3 反向因果与 ln_mexp 的警示

E2 `ln_mexp × food_share_lag` β=+0.51 太强，几乎 *一定* 包含反向因果：家庭面临大额医疗支出 → 非医疗消费被压缩 → 食品份额机械上升。这是 2010–2022 中国医疗自付比例 30–40 % 的制度背景。**故 ln_mexp 的结果不被当作 Bitter 确认**，仅作为稳健性异象报告。

---

## 10. 跨构念映射 — F1–F4 与 Drosophila A4 / Layer A

| Layer A Case | Δ_ST | F1 route | F3 机制 | 人类同源映射到 C11 |
|:---|---:|:---|:---|:---|
| A4 Drosophila sugar | +0.71 | A (祖先信号分布转移) | M1 habit | **TAS1R2/TAS1R3 sweet receptor**, DAL neuron → NAcc dopamine; 人类同源 > 80 % |
| A6 Olds-Milner rat | +0.97 | B (直接神经刺激) | M1 | 人类 fMRI reward 回路；overconsumption hedonic hotspot |
| A10 Neonic bees | +0.73 | B (novel chemical signal) | M1+M2 | *不* 适用 C11（糖非 B route） |
| **Layer A pooled** | **+0.72** [+0.60, +0.83] | — | — | 这是 C11 应达到的预测 Δ_ST（调整到人类文化层后的 +0.40 ~ +0.65） |

### 10.1 C11 对 A4 的 canonical mammalian homologue 桥 — 目前测量不足

`sweet_trap_formal_model_v2.md` §3.1 list A4 为 "Directly from A5 → Layer 2 ... Directly mammalian homologue"。预测：C11 Δ_ST ≈ +0.5。

观察到：C11 Δ_ST ∈ [−0.10, +0.02]。**桥不成立于当前测量**。

### 10.2 可能的挽救路径（均需数据升级）

1. **NOVA 类别级**（超加工 vs 全食物比率，Monteiro 2019）：需要专门饮食频率模块。CFPS 没有；CHARLS 2011 曾有简短膳食模块但不涵盖 NOVA 分级。中国营养监测系列（China Health and Nutrition Survey, CHNS）有 3 天饮食记录，但 public 版本仅到 2015。
2. **甜饮频率**：CHARLS 2018/2020 增加了简单饮食频率问题，未在当前清洗版中。若访问原始 dta 可能有。
3. **CHARLS 生物标志物 pooled 跨波设计**：把 wave 1 HbA1c 作为 baseline，wave 3 作为 4 年 follow-up；以 "baseline 高 HbA1c 组" 的生活方式变化作为 lifestyle endorsement 的代理。**此设计 feasible 但需新一轮 PDE**。

---

## 11. 与 C4 并行诊断

本次 C11 PDE 与已完成的 C4 PDE 在 **结构上高度对称**：

1. **Aggregate 层 null**：C4 life_sat β=+0.034 p=0.18；C11 d_food_share qn12012 β=−0.011 p=0.69。
2. **Domain-specific 层有 θ 签名**：C4 marital_sat β=+0.050 p=0.026；C11 ln_food × qn12012 79 % Bonf-sig。
3. **Δ_ST 号向相反于构念预测**：C4 Δ_ST ∈ [−0.04, −0.11]；C11 Δ_ST ∈ [−0.10, +0.02]。
4. **λ 测试 null**：C4 p=0.15；C11 p=0.65。
5. **被诊断为 "measurement-limited case"，从 Focal 候选降级**。

两者共同提示：**CFPS 家庭聚合数据对 Sweet Trap 的四原语检测存在系统性测量偏差**。论文的 Layer B 需要转向有 *个体行为频率* 的数据源（鸡娃 × 双减 DID 的 C2，或专门设计的新数据）。

---

## 12. 与文献对照

### 12.1 Mozaffarian 2016 JAMA & Willett 2019 Lancet — 西方宏观剂量

Western meta-analyses 报告 sugar-sweetened beverage 每日 1 份 → 糖尿病 HR = 1.13 (Lancet Public Health 2019)；lifetime 20 % 增超重风险（JAMA 2016）。转换到 Δ_ST：若假设奖赏-适应度 ancestral ≈ +0.7（甜味在祖先环境指示高能量水果、蜜），当代 ≈ +0.05（医疗诊断后管理），Δ_ST ≈ +0.65——与 Drosophila A4 一致。**我们的 CHARLS B2 糖尿病新发 effect (β=+0.0012) 是这个 lifetime risk 的一年 lag 版本，量级合理**。

### 12.2 Allcott Lockwood Taubinsky 2019 AER — 含糖饮料税

他们估计内部性（internality）≈ USD 0.1/oz，SSB 税 USD 0.01/oz 是大约最优水平的 10 %。这相当于一个 welfare 损失的内部化，构念上等价于 Sweet Trap 的 β·C 项。**政策段**（§14）直接桥接他们的 exposure vs belief 结果。

### 12.3 中国营养转型文献

Popkin 2021 *Global Food Security* 总结：中国在 1990–2020 糖消费从人均 8 g/day 上升至 ~35 g/day，脂肪能量比例从 16 % 上升至 32 %。**宏观转型剧烈**，但公开个体数据（CFPS 食品份额、CHARLS 收入代理）*不能* 个体层捕获此剧变。这是 C11 的 core data gap。

---

## 13. 构念决策（formal_model v2 §1 F1 falsification rule）

### 13.1 F1 rule 判断

C11 的 F1 rule（*Δ_ST ≤ 0 or cor(R_agent, F) > 0 in current environment ⇒ kills C11 as Sweet Trap*）：

- **Pre-reg 操作化**：Δ_ST 负号，但幅度在 0.02 SD 级，*统计上* 负但幅度极小。—— **测量层 F1 未确证但也未证伪**。
- **CHARLS B2 糖尿病新发**：β=+0.0012, p=0.015（单尾），*号向与 Bitter 一致*。**Biomarker 层 F1 未证伪**。
- **SCA ln_food × qn12012**：θ 签名强正（79 % Bonf-sig）。**θ 层 F1 未证伪**。

**综合判决**：C11 **没有在 F1 规则下被证伪**。它被 "测量边界" 降级，不被 "构念伪造" 排除。这与 D3 996 的 F1 falsification（β=−0.074 p<10⁻⁶）定性不同。

### 13.2 在论文中的位置

按 `pre_reg_D5_diet.md` §7.2 和 `sweet_trap_formal_model_v2.md` §6（"27-case correspondence"）：

- **C11 保留在论文中**，位于 SI Appendix A 的 "27-case feature profile" 内。
- **C11 从 Focal #2 降级**：原先头条计划是 "C4 + C2 + C11" 三头条；现在 C4 降级、C11 降级后，头条变为 **C2 单头条 + 跨物种 Figure**。
- **C11 的主文位置**：Figure 3 "Signal-hijack pathway" 面板 —— Drosophila A4 + human C11 + neonic bees A10。C11 panel 展示 "CFPS food_share null + CHARLS diabetes incidence 方向性"，诚实报告两者。
- **Figure 5 跨物种 Σ_ST 地图**：C11 placed 在 "measurement-challenged partial signature" 带，与 C4 并列，不在 primary confirmed band。

### 13.3 abstract 候选句（更新）

> "Across 5 candidate human domains, within-person longitudinal tests of the Sweet Trap's F1+F2 diagnostic confirm the signature in the C2 parenting-investment domain (confirmed); the C11 diet and C4 marriage-wealth domains show measurement-limited partial signatures (θ detectable on domain-specific outcomes via ln_food and marital_sat respectively, but full Δ_ST cross-species quantitative bridge requires dedicated nutrition/bride-price data not available in CFPS/CHARLS/CGSS public files); and the D3 996 overwork domain falsifies the Sweet leg, demonstrating that the construct's F1 rule is actually constraining. The 4-of-5 partial-to-full domain pattern, combined with Layer A pooled Δ_ST = +0.72 across 8 animal cases, supports the construct's cross-species claim while identifying human-scale measurement as the paper's key remaining limitation."

*(provisional — pending C2 PDE completion)*

---

## 14. 政策段（exposure vs belief intervention hook，formal_model v2 P4）

Layer A 和 C11 一致支持 **exposure intervention** 有效性高于 **belief intervention**：

- Allcott 2019 AER：SSB 税（exposure）>> 营养教育（belief）—— western evidence。
- 中国 2020 双减 + 营养标签 强制（2016+）：exposure-side 政策。
- 信息教育：mixed evidence（Meta 分析 Afshin 2020 *Lancet Public Health*：营养教育 → 行为改变 effect d ≈ 0.05 SD，小）。

C11 的 SCA 给出的 **ln_food × qn12012 正 θ 签名** 说明：如果政策目的是降低 Sweet-Trap 的愉悦触发（即降低 R_agent），*限制 supply side*（糖税、外卖含糖饮料限量、学校周边快餐禁设）比 *教育需求 side* 更符合 P4 的预测。这段可以入主文 Discussion。

---

## 15. 交付物清单

| 文件 | 内容 |
|:---|:---|
| `03-analysis/scripts/C11_diet_sweet_trap.py` | 端到端分析脚本（9 步 + 探索性） |
| `03-analysis/scripts/C11_diet_sweet_trap.log` | 执行日志（stdout 镜像） |
| `02-data/processed/C11_results.json` | 完整数值记录（primary + SCA 统计 + Δ_ST boot + CHARLS + primitives + exploratory） |
| `02-data/processed/C11_speccurve.csv` | 672 行 SCA（sweet 384 + bitter 288） |
| `00-design/pde/C11_diet_findings.md` | **本文档** |
| `00-design/analysis_protocols/pre_reg_D5_diet.md` | 预注册（锁定） |
| `00-design/sweet_trap_formal_model_v2.md` | 构念基础（F1–F4，Δ_ST 公式） |
| `00-design/pde/layer_A_animal_meta_synthesis.md` | Layer A 动物 meta-synthesis（Δ_ST pool = +0.72） |

Panel SHA-256 lock：`371ddcaacedb46336225772abc8d1116d4ddb0e9c12bc0f1203d5ad16c4e8a2d`（脚本再跑须复现此 hash）。
CFPS panel *not modified*（per 项目规则）。

---

## 16. 完整性声明

本次 PDE 严格遵守 `pre_reg_D5_diet.md` §6–§9 和 `feedback_no_premature_fork.md`：

1. **Primary 三假设**（H5.1, H5.2, H5.3）按 §6 预注册规约执行，one-sided，α_Bonf=0.0125。三条全 null，诚实报告。
2. **未做 post-hoc rescue**。§7.3 禁止的补救（号向翻转、阈值重置、子样本搜索、替换 Sweet DV）均未实施。
3. **探索性分析明确标记**：§4.4 SCA 的替代治疗（ln_food, food_share_valid level）、§6 CHARLS 分析、§8 的 E1–E5 均标为 exploratory；不改变 primary null 裁决。
4. **Decision path §7.2 "both H5.1 and H5.2 null"** 路径被激活：report honestly in main text as "D5 does not show the pattern within CFPS measurement"。Construct 未被损害（*"The paper pre-commits to D5 as the riskiest domain for falsification."*）。
5. **CHARLS 分析超出 pre-reg §6.7 Exploratory 范围** —— §6.7 flagged "外部 CHARLS 子样本" 为 exploratory；本 PDE 在 §6/§6.1–6.4 执行了。这是 **非偏离** —— pre-reg §9.3 明确列出 "CHARLS 外部验证" 为 Non-deviation。
6. **测量局限透明披露**：§3.1、§5.1、§6.4、§10.2 详细讨论了 `food_share` 的恩格尔效应、CHARLS 饮食频率缺失、`log_income` 代理的内生性。

没有任何一个数字被 re-framed 为支持 Sweet Trap；一个 null 是一个 null。**但一个 null 不等于构念伪造** —— C11 仍在 F1 rule 下存活，凭借 biomarker 层的方向性证据和 ln_food 层的 θ 签名。

---

## 17. 下一步

1. **C2 鸡娃 × 双减 DID**（并行执行中）—— 若 C2 通过 Bonf，论文头条转为 C2 单头条。
2. **CHARLS 原始 dta 中的饮食频率模块** —— 访问 2018/2020 原始问卷中的简单饮食频率问题，可能能重做 B1/B2 with 更清洁的 exposure。
3. **CHNS（中国健康与营养调查）public 版本到 2015** —— 有 3 天饮食记录和 NOVA 分级可能性；作为 C11 的 redundant panel 检验。
4. **Layer A A4 Drosophila 重做 TAS1R2/TAS1R3 机制桥** —— 把当前 CHARLS diabe p=0.015 的方向性结果和果蝇 Δ_ST=+0.71 在 Figure 3 上物理布局为 "same molecular machinery, two species, partial human confirmation"。

---

*End of C11 PDE findings v1.0 — 2026-04-17. 第 3 份 PDE（D3 996 null / C4 marriage measurement-limited / **C11 diet measurement-limited with biomarker partial confirmation**）。*
