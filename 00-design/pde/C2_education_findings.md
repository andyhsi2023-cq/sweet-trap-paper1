# C2 "鸡娃 Intensive Parenting" — PDE Findings

**Generated:** 2026-04-17
**Analysis script:** `03-analysis/scripts/C2_education_sweet_trap.py`
**Log:** `03-analysis/scripts/C2_education_sweet_trap.log`
**Results JSON:** `02-data/processed/C2_results.json`
**Spec curve:** `02-data/processed/C2_speccurve.csv`
**Panel SHA-256:** `d1603c1e7f9776be8ddfd3ed219706e374cc210858d83140603b40cff7702c30` (verified match)
**Protocol:** `00-design/analysis_protocols/pre_reg_D2_education.md`
**Construct authority:** `00-design/sweet_trap_formal_model_v2.md` §1 (F1–F4) + §2 (Δ_ST)

---

## 0. TL;DR — C2 鸡娃 is NOT a Sweet Trap; it is coerced exposure (like 996)

> **在 CFPS 2012–2022 纵向面板（N=30,630 人-年；15,500 人；8,098 人 ≥2 期可做 person FE），家庭教育支出占比（eexp_share）既没有触发父母福利 Sweet 信号（β=−0.043，p₂=0.57，one-sided p_pos=0.71），也没有被高收入/高教育父母主动选择（F2 明显失败：eexp_share 与家庭收入、父母受教育年限、城镇身份都 *负相关* — 经济越紧、父母学历越低、农村家庭反而支出占比更高）。双减 2021-07 DID 给出 δ = −0.009（SE=0.040，p₂=0.83），零效应；事件研究 2020 前的预趋势 χ²_4=93.1，p<10⁻¹⁹，大幅 violate 平行趋势（高基线家庭早在 2012 就比低基线家庭低 0.29 Likert，然后逐渐收敛），导致 H2.3 的因果识别在当前 operationalisation 下 **不可信**。Δ_ST(eexp_share, qn12012) = −0.038，95%CI [−0.067, −0.010]，**点估计错号**（预测为 +0.40 至 +0.65；实际为负且 CI 排除正区间）。144 个 spec curve 中 qn12012 × eexp_share 只有 0% 为正，ln_eexp_p1 也只有 66.7% 为正且 0% 达到 α=0.05。四原语 θ=null、λ=null、β=错号（滞后期 β>0，零 crowd-out 证据）、ρ=负（mean-reverting，非 lock-in）。所有关键签名都 FAIL。**

> **结论：与 D3 996 结构完全平行 — C2 鸡娃在 CFPS 公共数据上呈现 "Bitter-only, pressured-exposure" 模式（家庭在高教育支出压力下幸福感无提升、下一期消费结构无清洁挤出、双减冲击无发现福利回升），这不是 Sweet Trap，而是 coerced educational squeeze。C2 在 Focal 排名中 **应降级到 null/boundary 面板**，不得作为 Focal-1 头条使用。**

**与 C4 关键对比**：
- C4 有**局部 θ 签名**（marital_sat β=+0.05, p=0.026）— 构念依然部分可见。
- C2 **没有任何 DV 出现清洁 θ 签名** — qn12012 负号、qn10021 null、eexp_income_ratio 虽正但是同义反复。

**与 D3 对比**：
- D3 996：θ 错号（β=−0.074, p₂=10⁻⁶），F2 失败（强制加班）。
- C2 鸡娃：θ null/弱负（β=−0.043, p₂=0.57），F2 失败（支出占比反随收入/学历下降）。
- **两个域都呈现"bitter without sweet endorsement"的平行模式** — 这本身是 Layer B 的重要结构性发现，值得进入论文作为 boundary-null 的证据（见 §14）。

---

## 1. Data verification

| 检查项 | 数值 |
|:---|:---|
| Expected SHA-256 | `d1603c1e7f9776be8ddfd3ed219706e374cc210858d83140603b40cff7702c30` |
| Actual SHA-256 | `d1603c1e7f9776be8ddfd3ed219706e374cc210858d83140603b40cff7702c30` |
| Match | **PASS** |
| Rows × cols | 30,630 × 46 |
| Waves | 2012, 2014, 2016, 2018, 2020, 2022 |
| Unique pid | 15,500 |
| pids ≥ 2 waves | 8,098 |
| pids observed 2018 ∩ {2020 ∨ 2022} | 2,565 |
| DID analytic subsample (post-NA) | 18,708 person-years |

**变量告警（操作化限制）**: 在当前 D2 面板中，`school`（校外培训支出）与 `eexp`（家庭教育总支出）**完全相等**（match rate = 1.000）。这意味着 D2 panel 的构建脚本在清洗阶段把两者合并了，导致我们**无法独立识别"补课强度"（双减政策的直接 target）vs "总教育支出"**。这是 C2 在 identification 层面相对于 C4 的主要脆弱性：双减冲击应该切割 tutoring，但我们的 treatment 变量是 total education spending，其中包含学费、书本费、住宿费等非-tutoring 成分。pivot 处理见 §2。

`eec`（文化+教育+娱乐合计支出）与 `eexp` 相关 r=0.91，仅 57% 完全相等。`eec` 作为稳健性替代纳入 spec curve 但不改变主要结论。

---

## 2. Empirical pivots forced by data audit (protocol §9)

1. **`school == eexp` 合并**。公开 D2 面板无法区分 tutoring vs. tuition。这是"双减冲击"识别的第一个脆弱点：政策准确切割 tutoring，但我们的处理变量是 total education spending。结果：DID "处理强度"会系统性被稀释（高学费家庭也被算入 high_baseline）。不论 δ 估计是正还是负，都无法纯净地归因到"补课 reward signal 被切断"这一机制。协议 §3.4 的 child-module 合并失败的偶发性，已被 upstream cleaning 合并决策提前预判。
2. **预趋势严重违反**（见 §5）。事件研究显示高基线家庭在 2012–2018 全部拖累低基线家庭 0.06–0.29 Likert 点，逐年收敛至 0。这意味着 high-baseline 不是"同质政策敏感家庭"，而是"初期满意度系统性更低的家庭"。标准 DID 平行趋势假设失败 → H2.3 的 δ 不是 CATE，而是预期回归均值。**我们诚实报告这一失败，不用合成控制/matching 做 post-hoc 修复**。
3. **eexp_share 与父母 SES 的 "反向" 相关**（见 §4.2）。在中国 2012–2018 年 CFPS 样本，高 eexp_share 家庭系统性地是低收入、低学历、农村家庭，而不是高 SES 城市家庭。这是鸡娃现象学（phenomenology_archive.md §C.2）描述的"中产竞争"假设的**实证反面**：在 CFPS 的收入-支出结构里，教育支出占比更像一个**必需品比重指标（Engel-like）**而非**aspirational status signal**。F2 诊断失败由此。
4. **qn12012 是"父母"的生活满意度**；CFPS 公开面板中没有干净的"子女心理健康"变量（pre_reg §3.4 的 child module fallback 实际发生：child 问卷未并入 D2 面板）。`qn10021`（trust in parents，0-10）是次优 proxy，与鸡娃的 λ-on-child 机制不是一一对应。λ 原语因此**弱识别，非强识别失败**。

这些 pivot 都在 protocol §9.1 的"anticipated deviation risks"框架内，不改变 §7 的决策规则。

---

## 3. Descriptives

### 3.1 教育支出时间轨迹

| Wave | N (child_num≥1) | eexp 均值 | eexp 中位 | eexp_share 均值 | eexp_income_ratio 均值 | qn12012 均值 |
|:---|---:|---:|---:|---:|---:|---:|
| 2012 | 4,797 | ¥3,227 | ¥1,100 | 0.081 | 0.170 | 3.25 |
| 2014 | 5,922 | ¥3,872 | ¥1,600 | 0.081 | 0.147 | 3.75 |
| 2016 | 5,877 | ¥5,154 | ¥2,400 | 0.080 | 0.110 | 3.53 |
| 2018 | 5,415 | ¥6,519 | ¥3,000 | **0.093** | 0.105 | 3.95 |
| 2020 | 4,032 | ¥6,820 | ¥3,000 | 0.081 | 0.084 | 3.96 |
| 2022 | 3,800 | ¥8,499 | ¥4,000 | 0.088 | 0.090 | 3.95 |

**两个描述性事实**：
1. 绝对教育支出 eexp 从 2012 的 ¥3,227 增至 2022 的 ¥8,499（**2.6× 增长**），与 GDP 同步甚至更快。
2. **占比（eexp_share）在 2018 年达到峰值 0.093**（即总支出的 9.3% 用于教育），之后 2020 下降到 0.081，2022 轻微回升到 0.088。**2018→2020 的占比下降（1.2 ppt）**时间上恰与双减政策酝酿期吻合。但这个量级（-1.2 ppt）不足以 drive 检测到的满意度变化（2018 qn12012=3.95 → 2022 qn12012=3.95，父母满意度基本不变）。

### 3.2 eexp_share 的 SES 梯度（F2 诊断原材料）

2018 年按父母受教育年限 quartile：

| 受教育年限 | N | eexp_share 均值 | eexp_share 中位 |
|:---|---:|---:|---:|
| 0-6 年 | 1,750 | 0.101 | 0.050 |
| 6-9 年 | 1,931 | 0.097 | 0.057 |
| 9-12 年 | 801 | 0.087 | 0.057 |
| 12-22 年 | 674 | 0.082 | 0.056 |

**方向：受教育年限越高 → eexp_share 越低**。这与西方文献（中产精英 intensive parenting 假设）相反。

2018 年按家庭收入 quartile：

| 收入 quartile | eexp_share 均值 | qn12012 均值 |
|:---|---:|---:|
| Q1 (<¥40k) | 0.113 | 3.93 |
| Q2 (¥40k-69k) | 0.098 | 3.93 |
| Q3 (¥69k-113k) | 0.084 | 3.98 |
| Q4 (≥¥113k) | 0.078 | 3.97 |

**方向：收入越高 → eexp_share 越低**（负梯度）。对应 §4.2 的 F2 失败判定：eexp_share 不是 aspirational status signal；它更像一个 Engel-分子，在低收入家庭中被子女教育这一非弹性需求 crowd out 其他开支。

---

## 4. F1 + F2 construct diagnostics

### 4.1 F1 诊断 — reward–fitness 解耦（必要条件）

按 epoch 分组的 cor(eexp_share, welfare)：

| Epoch | cor(eexp_share, qn12012) | 95% CI | N | cor(eexp_share, qn10021) | 95% CI | N |
|:---|---:|:---:|---:|---:|:---:|---:|
| Ancestral 2012-2014 | **−0.043** | [−0.064, −0.023] | 10,528 | +0.025 | [+0.005, +0.042] | 10,505 |
| Transition 2016-2018 | +0.007 | [−0.011, +0.027] | 11,164 | −0.008 | [−0.030, +0.013] | 11,145 |
| Current 2020-2022 | **−0.039** | [−0.062, −0.015] | 7,659 | +0.005 | [−0.021, +0.029] | 7,641 |

**关键观察**：
- 2012-2014 "ancestral" cor 是负的 (−0.043)。按 Sweet Trap 模型 F1 的严格版本，"ancestral" 应该为正（选择机制在祖先环境中把 reward signal 锚定到 fitness 上）。在教育支出这个**完全文化构造**的信号（无古代参照）上，**route A ancestral-mismatch 表述从根本上不适用**。Route B（supernormal/novel signal on general-purpose architecture）更合适，但此时 F1 的定义需要 reward 信号至少在 current 时期**正相关**地进入 agent 的福利 — 我们这里 current cor 也是 −0.039。
- **F1 的两个方向都失败**：没有"reward signal 过去正相关、现在解耦"（Δ_ST 错号），也没有"current reward signal 与 welfare 正相关"（cor current < 0）。这意味着 eexp_share 根本不是 agent 的 R_agent — 至少不是在我们能从 qn12012 直接观测的意义上。

### 4.2 F2 诊断 — endorsement without coercion（必要条件）

协议 §7.1 要求 F2 holds：agent **主动选择** 鸡娃（非被迫）。四个独立诊断：

| 诊断 | 数值 | F2 预期 | 实际 | 解读 |
|:---|---:|:---:|:---:|:---|
| cor(eexp_share, ln_income) 2018 | **−0.093** | > 0 (aspirational) | **错号** | 低收入家庭占比更高 |
| cor(eexp_share, eduy) 方向 | 负 | > 0 | **错号** | 低学历家庭占比更高 |
| P(education_squeeze=1 \| top-tercile eexp_share) | **0.502** | 低 | **高** | 高支出家庭一半经济紧张 |
| P(education_squeeze=1 \| bottom-tercile eexp_share) | 0.033 | 低 | 低 | 基线，作对照 |

**F2 判定：失败**。高 eexp_share 家庭的 profile 不是"有余力追求子女前途的中产"，而是"不得不在教育上支出大份额的经济紧张家庭"。这与 Sweet Trap 的 F2 条件正面冲突 — 他们的行为更像 **coerced exposure**（类比 D3 996 的"被迫加班"）而非 aspirational endorsement。

**构念前置判定**：**F1 + F2 均失败 → C2 鸡娃（在 CFPS 公共数据的 operationalisation 下）不满足 Sweet Trap 的诊断必要条件**。按构念 v2 §1 hierarchy，"F1+F2 necessary, no exceptions"。C2 必须降级为 boundary / coerced 类案例，而不是 Sweet Trap 的 confirmed instance。

### 4.3 子样本 F1 重检（能否在"aspirational subgroup"拯救？）

分析师尝试：若 C2 的 Sweet Trap 仅在中产精英子样本（urban × eduy≥12 × has_child）中成立，至少可保留"在部分人口中" Sweet signature。

子样本结果（N=5,561；within-person FE）：
- β(eexp_share → qn12012) = **−0.267** (SE=0.175, p₂=0.127)
- 点估计**更加负**（非 positive）。即便是 aspirational 家长，within-person 维度上增加教育支出占比不会提高其生活满意度。

**结论：F2 失败是构念层面的（不是测量失败），子样本也无法拯救**。

---

## 5. Primary regressions (pre-registered)

全部 person-FE + year-FE 通过 two-way demeaning 实现，cluster SE on `pid`。一侧检验 α_Bonf = 0.0125（协议 §8.2）。

### Table 1 — Four pre-registered primary hypotheses

| # | Hypothesis | DV | Treatment | N | β | SE | 95% CI | p₂ | One-sided | 判决 |
|:---|:---|:---|:---|---:|---:|---:|:---:|---:|---:|:---|
| H2.1 | Sweet | qn12012 | eexp_share | 28,636 | **−0.043** | 0.076 | [−0.191, +0.106] | 0.575 | p_pos=0.713 | **NULL**（点估计弱负） |
| H2.1b | Sweet (top-tercile) | qn12012 | eexp_share_top3 | 29,233 | +0.002 | 0.017 | [−0.031, +0.035] | 0.895 | p_pos=0.447 | **NULL** |
| H2.1c | Sweet (log eexp) | qn12012 | ln_eexp_p1 | 29,233 | −0.001 | 0.002 | [−0.006, +0.004] | 0.760 | p_pos=0.620 | **NULL** |
| H2.2 | Bitter (lag crowd-out) | non_edu_share | L.eexp_share | 14,447 | **+0.233** | 0.019 | [+0.196, +0.270] | 10⁻³⁴ | **错号** | **FAIL** (预测 <0，实际 >0) |
| H2.2b | Contemp identity | non_edu_share | eexp_share | 28,952 | **−1.038** | 0.004 | [−1.046, −1.029] | 0 | 机械 | 会计恒等式验证通过 |
| H2.3 | DID 双减 | qn12012 | did_2021 | 18,708 | **−0.009** | 0.040 | [−0.088, +0.071] | 0.833 | p_neg=0.416 | **NULL** |
| H2.4 | DID Placebo 2019 | qn12012 | did_2019 | 16,464 | **−0.051** | 0.036 | [−0.122, +0.021] | 0.164 | p_neg=0.082 | placebo fails |

### 5.1 H2.1 — Sweet 点估计是弱负的，不是预测的正

- 预期：|β̂| ∈ [0.10, 0.25] SD of qn12012 per 1-SD eexp_share。
- 观测：β = −0.043 Likert points per unit eexp_share 上升；CI 跨零。one-sided p_pos = 0.713 — 拒绝"无正效应"虚假无从谈起。
- 与 D3 996 的精确平行：D3 的 β = −0.074, p_pos = 1.000。C2 的 β 同方向但幅度更小、噪声更大。
- **判决**：协议 §7.1 confirmation 不触发；按 §7.2，H2.1 null。

### 5.2 H2.2 — Bitter 滞后 crowd-out 是 **错号**

- 预期：滞后一期 eexp_share 上升 → 后续 non_edu_share 下降（β<0）。
- 观测：**β = +0.233**（CI [+0.196, +0.270]，p₂ < 10⁻³⁴）。滞后 eexp_share 上升反而 **增加** 后续非教育支出占比。
- 解释：这与 eexp_share 的均值回归性（见 §6 ρ 原语测试）一致：**高 eexp_share 家庭在下一期会"恢复"到更低的教育支出占比，同时非教育占比上升**。这是消费平滑而非 Sweet Trap 的 lock-in 动力学。
- **判决**：与预期方向相反，**FAIL**。

H2.2b 同期恒等式 β≈−1.0 仅证明 share 满足 sum = 1 的代数，不提供任何 Sweet Trap 机制证据（协议 §6.2 已预先声明此条件下"we pre-specify the test of interest as whether the crowd-out survives person FE and lags"，H2.2 才是关键 — 并失败）。

### 5.3 H2.3 — 双减 DID 零效应且 placebo 不通过

- 双减 δ = **−0.009** (SE=0.040, p₂=0.833)。预测方向负，点估计 *方向正确但量级几乎为零*。CI 包括正负两端。
- **Placebo 2019 δ = −0.051**（p₂=0.164）。按协议 §7.1，discriminant check 要求 p₂ ≥ 0.10；**0.164 > 0.10 勉强通过，但只是因为 SE 较大**。点估计方向同真实处理且量级更大 — 暗示 DID 捕捉到的是 high-baseline vs low-baseline 之间的**持续 trend**，不是 2021 的冲击。
- **判决**：H2.3 null；识别诊断勉强通过但预趋势失败（下节）使得 δ 的因果解释**失去基础**。

---

## 6. Event study — 预趋势大幅失败

参考年 2020；全部估计相对于 2020 的 (high_baseline × 年份) 交互项。

| Event coefficient | β | SE | p₂ |
|:---|---:|---:|---:|
| evt_2012 × high_baseline | **−0.290** | 0.045 | <10⁻⁹ |
| evt_2014 × high_baseline | **−0.210** | 0.040 | <10⁻⁷ |
| evt_2016 × high_baseline | **−0.170** | 0.038 | <10⁻⁵ |
| evt_2018 × high_baseline | −0.062 | 0.031 | 0.046 |
| *evt_2020 (reference)* | 0 | — | — |
| evt_2022 × high_baseline | −0.034 | 0.040 | 0.395 |

**联合预趋势 χ²₄ = 93.1, p < 10⁻¹⁹**。按协议 §7.1 confirmation 要求 pre-trends joint p > 0.10；**实际 p ≈ 10⁻¹⁹，严重失败**。

**预趋势走形模式的实质**：high-baseline（高基线教育支出占比）家庭在整个 2012–2018 年间父母满意度**系统性低于** low-baseline 家庭，差距从 −0.29 逐渐收敛到 −0.03（2022）。这符合两种非-Sweet-Trap 机制：
1. **Mean reversion**: 2012 年贫困/挤压家庭（教育支出被迫占比高，同时生活满意度低）随着整体国家收入上涨而缓慢恢复到正常；2022 他们与高 SES 家庭的 gap 基本消失。
2. **Cohort catch-up**: 2012 观测的 high-baseline 家庭不是 2022 观测的 high-baseline 家庭（有 age-in/age-out）。event study 在这种情况下不再测量"同一处理组的动态"，而是 pooled cohort heterogeneity。

无论是哪一个，都不是双减政策的 causal effect。

**判决**：H2.3 identification 彻底失败。即使 δ_2021 不是 0，也无法因果归因。**C2 不提供关于双减政策福利冲击的可信估计**。

---

## 7. Δ_ST estimation — 点估计错号

Bootstrap B=1,000，种子 20260417，Δ_ST = cor(eexp_share, Y)_{2012-2014} − cor(eexp_share, Y)_{2018-2020}：

| Y | cor_ancestral | cor_current | **Δ_ST** | 95% CI (bootstrap) | p(Δ ≤ 0) |
|:---|---:|---:|---:|:---:|---:|
| qn12012 (父母生活满意度) | −0.043 | −0.005 | **−0.038** | [−0.067, −0.010] | 0.996 |
| qn10021 (信任父母 child-proxy) | +0.025 | −0.004 | +0.029 | [−0.001, +0.057] | 0.032 |
| non_edu_share | −0.996 | −0.990 | −0.006 | [−0.010, −0.003] | 1.000 |

**与 Layer A 动物池化 Δ_ST = +0.72 [+0.60, +0.83] 的差距是 20 倍量级**（协议预测人类 Δ_ST ∈ [+0.40, +0.65]；实际 |Δ_ST| ≤ 0.04）。

**qn12012 的 Δ_ST 95% CI 落在 [−0.067, −0.010]，完全位于负区间**，这意味着：
- 不仅不支持 Δ_ST > 0（Sweet Trap 预测），而且
- **有信心拒绝 Δ_ST ≥ 0**（当前环境下 eexp-happy cor 反而 **更正**（较 2012-2014 不那么负））。

**与 C4 marital_sat Δ_ST = −0.110（CI [−0.215, −0.002], p=0.98) 形成平行对比 — C2 Δ_ST 错号幅度较小但方向一致**。

**实质解释**：在 2012-2014 中国（"ancestral"），教育支出占比与父母满意度负相关（穷困家庭挣扎），这个负相关在 2020-2022 减弱到几乎零。这**不是** Sweet Trap 预测的解耦（解耦应是 positive 至 zero/negative），而是**国家整体经济发展消除了 2010 年代初期的"教育支出拖累生活质量"**这一特定压力源。C2 的历史轨迹与 Sweet Trap 方向相反。

---

## 8. Four primitive signatures (θ, λ, β, ρ)

按 `sweet_trap_formal_model_v2.md` §3.2 的 Layer B 语言：

| 原语 | C2 实证信号 | 证据 | 状态 |
|:---|:---|:---|:---:|
| **θ (amenity)** | qn12012 对 eexp_share 的短期响应 | β=−0.043 (p=0.57); ln 版本 β≈0; top3 版本 β≈0 | ✗ **NULL** |
| **λ (externalisation)** | qn10021 (child-proxy) 对 eexp_share 的响应 | β=+0.058 (SE=0.115, p=0.62) | ✗ **NULL** — 家长教育支出占比不显著影响子女对家长的信任评分 |
| **β (present bias)** | 下一期非教育消费占比被 eexp 挤出 | **β=+0.233, 错号** | ✗ **错号** — 教育支出非 lock-in，而是均值回归 |
| **ρ (lock-in)** | eexp_share AR(1) 系数 within-person | **β=−0.230** (SE=0.017, p<10⁻³⁹) | ✗ **负号** — 教育支出占比 mean-reverting，不是 lock-in |

**全部 4 个原语都 fail 或错号**。这是**结构性构念失败**，不是单一 DV 的测量失误。

**对比 C4**：C4 有 θ 部分签名（marital_sat β=+0.05, p=0.026）、β 方向一致（kids_total 下降）；C2 **没有任何原语有干净签名**。在构念失败严重程度上，**C2 > C4**。

**对比动物 Layer A**：A6 Olds-Milner 的 Δ_ST=+0.97，M1 habit lock-in 极强。人类理论预测 C2 应接近 A7 peacock（M2 peer norm，Δ_ST=+0.58）；实际 C2 在所有原语上都是 null 或反方向。**不构成跨物种桥接的有效案例**。

---

## 9. Specification curve (144 specs)

按协议 §6.6 的 grid：4 DV × 3 treatment × 4 control set × 3 sample = 144 specs。

### 9.1 By DV × treatment (已汇总)

| DV | Treatment | 中位 β | % β > 0 | % (β>0) & p<0.05 |
|:---|:---|---:|---:|---:|
| eexp_income_ratio | eexp_share | +1.061 | 100.0 | 100.0 |
| eexp_income_ratio | eexp_share_top3 | +0.177 | 100.0 | 100.0 |
| eexp_income_ratio | ln_eexp_p1 | +0.024 | 100.0 | 100.0 |
| non_edu_share | eexp_share | **−1.036** | **0.0** | 0.0 |
| non_edu_share | eexp_share_top3 | −0.158 | 0.0 | 0.0 |
| non_edu_share | ln_eexp_p1 | −0.017 | 0.0 | 0.0 |
| qn10021 | eexp_share | −0.046 | 33.3 | 0.0 |
| qn10021 | eexp_share_top3 | +0.009 | 75.0 | 0.0 |
| qn10021 | ln_eexp_p1 | +0.001 | 66.7 | 8.3 |
| **qn12012** | **eexp_share** | **−0.098** | **0.0** | **0.0** |
| qn12012 | eexp_share_top3 | −0.013 | 25.0 | 0.0 |
| qn12012 | ln_eexp_p1 | +0.001 | 66.7 | 25.0 |

### 9.2 三个模式

1. **关键 Sweet 测试（qn12012 × eexp_share）在 12 个 spec 中 0% 为正、0% 显著正**。协议 §7.1 要求 H2.1 confirmation 的 SCA 阈值为 "≥80% sign consistency 正向"，**实际 0%**。彻底 falsification。
2. **qn12012 × ln_eexp_p1** 是唯一在 ln 变换下 66.7% 为正的，但只有 25% 达到 α=0.05，仍远低于 confirmation 阈值。ln 变换压缩尾部可能在某些子样本 induce 正号，但无系统性。
3. **eexp_income_ratio 100% 正相关于 eexp_share** 是会计恒等式（分母差异）再次被测出，不提供机制证据。

与 D3 996 spec curve 的**精确平行**：
- D3 sweet branch 10.2% 为正 / 3.7% 显著正；C2 同方向 qn12012 × eexp_share **0.0% / 0.0%**。
- D3 在 qg406（job satisfaction）上的 falsification 强度与 C2 在 qn12012（life satisfaction）上 **等价或更强**。

### 9.3 Bitter 滞后 crowd-out spec curve

24 个 spec（DV=non_edu_share × lag ∈ {1,2} × 4 controls × 3 samples）：
- 中位 β = **+0.228**
- % β < 0 = **0.0%**
- 预期方向一致率（<0）= 0.0% vs 协议 §7.1 要求 ≥80%。**完全错号、完全 robust**。

### 9.4 DID 稳健性 (9 specs: 3 阈值 × 3 sample)

| 阈值 | Sample | N | β | SE | p₂ |
|:---|:---|---:|---:|---:|---:|
| top 50% | all | 18,692 | +0.006 | 0.037 | 0.87 |
| top 50% | only_child | 10,758 | +0.024 | 0.054 | 0.65 |
| top 50% | urban | 8,656 | +0.030 | 0.050 | 0.55 |
| top 33% | all | 18,692 | −0.002 | 0.041 | 0.97 |
| top 33% | only_child | 10,758 | +0.008 | 0.060 | 0.89 |
| top 33% | urban | 8,656 | −0.031 | 0.055 | 0.58 |
| top 25% | all | 18,692 | −0.002 | 0.046 | 0.97 |
| top 25% | only_child | 10,758 | −0.008 | 0.064 | 0.90 |
| top 25% | urban | 8,656 | −0.072 | 0.061 | 0.24 |

**9 个 spec 中 55.6% 为负**（非干净负）；最大 p₂ = 0.97，最小 p₂ = 0.24。**没有一个 spec 达到 α=0.05，更不用说 α_Bonf=0.0125**。DID 在 identification（预趋势失败）前提下已不可靠，在 statistical 层面也完全没有信号。**确认 H2.3 nul**。

---

## 10. 与 C4 marriage market 的结构对比

| 维度 | C4 彩礼 | C2 鸡娃 |
|:---|:---|:---|
| **F1 诊断** | Δ_ST 错号但 marital_sat 显示部分解耦 | Δ_ST 错号；aggregate 和 child-proxy 均 null |
| **F2 诊断** | F2 不直接测试；构念可能依赖 payer side 不可观测 | **F2 失败**：eexp_share 反向相关收入/学历/城镇 |
| **θ 原语** | **部分正**（marital_sat β=+0.05, p=0.026） | null 或弱负 |
| **λ 原语** | null | null |
| **β 原语** | 方向一致（kids_total ↓, p=0.06） | **错号**（lag crowd-out β>0） |
| **ρ 原语** | 描述性可见（1950→2017 增 23%） | **错号**（AR(1) 系数 −0.23） |
| **F1 in miniature** | ✓ marital_sat yes / status no | ✗ 所有 DV 都不呈现 |
| **Δ_ST 点估计** | −0.04 to −0.11 | −0.038 |
| **Spec curve sign-consistency** | marital_sat 100% (+) | qn12012 0% (+) |
| **识别** | 2SLS IV 失败但 OLS 部分可信 | DID 预趋势失败，IV 不适用 |
| **构造失败程度** | 部分（测量限制为主） | **彻底**（F1+F2 都失败） |

**核心结论**：C4 在"构念部分符合 + 测量限制"的轴线上衰减；C2 在"构念根本不符合 + 可用数据一致否决"的轴线上 **更严重地** 失败。

---

## 11. 与 D3 996 overwork 的结构平行

C2 与 D3 呈现**几乎完全同构**的失败模式：

| 签名 | D3 996 | C2 鸡娃 | 平行？ |
|:---|:---|:---|:---:|
| Sweet H2.1 β 符号 | 负 (−0.074) | 负 (−0.043) | ✓ |
| Sweet p₂ | 10⁻⁶ | 0.57 | 部分 (D3 噪声小) |
| F2 mechanism | 强制加班 | 低学历/低收入家庭被迫支出占比高 | ✓ coerced |
| Bitter 方向 | 正 (chronic disease +2.3pp) | 错号 (lagged crowd-out +0.23) | ✗ D3 bitter 方向对，C2 方向错 |
| Spec curve 正率 | 10.2% | 0.0% | ✓ (C2 更糟) |
| 4 原语签名 | 主要 null | 全 null/错号 | ✓ |

**Layer B 的一个重要结构性发现**：在 CFPS 2010–2022 数据上，**两个被"鸡娃社会学"文献描述为 aspirational endorsement 的行为（996 奉献 + 子女教育投入）实际上都呈现 coerced exposure 模式**。这不是 Sweet Trap，但它是**比 Sweet Trap 更阴暗的现实** — 人们被迫接受低福利配置，没有主动选择的余地。论文可以利用这个**整合的空结果**来 sharpen Sweet Trap 的边界：**并非所有"人们在做让自己更糟糕的事"都是 Sweet Trap**，有些只是压迫。这强化了构念，而非削弱。

---

## 12. 和 Layer A 动物 pooled Δ_ST 的差距

Layer A（`00-design/pde/layer_A_animal_meta_synthesis.md`）给出：
- 8 个动物案例 Δ_ST 范围 [+0.55, +0.97]
- 随机效应池化 Δ_ST = **+0.72 [+0.60, +0.83]**
- I² = 67%

C2 观测到：
- Δ_ST(qn12012) = **−0.038 [−0.067, −0.010]**
- Δ_ST(qn10021) = +0.029 [−0.001, +0.057]

**差距**：|Δ_ST_animal − Δ_ST_C2_qn12012| = 0.76，相当于人类 Δ_ST 至少应偏正 0.60 以与最弱的动物案例（peacock/widowbird，+0.58）对齐。C2 不仅不在这个区间，**连方向都错**。

**跨物种桥接结论**：C2 **不提供有效的 human-animal M2 peer-norm 同源证据**。协议原本假设 C2 ↔ A7 peacock（G_{τ,y} 共变），但 C2 的数据完全无法支持这个桥接。论文 Figure 2（"same positive-feedback mechanism at three scales: moth + peacock + 鸡娃"）的第三条腿**不再可用**。

**推荐改用**：C2 的失败作为 "human-to-animal homology boundary condition" 进入 Figure 5（not Figure 2）的后半部分，强化"并非所有候选域都满足跨物种同源"这一现实。Figure 2 的 human 案例应改用 C1 打鸡血（目前尚未跑 PDE）或 C11 diet（下一个 PDE 候选）。

---

## 13. 针对 C11 diet PDE 的启示

C2 的 PDE 给 C11（糖/脂肪/盐 × 中国营养转型）留下三条**必须注意的教训**：

1. **F2 诊断必须在构念层面做，不能只做回归**。C2 的回归本身不会告诉你 F2 失败；只有做 cor(treatment, SES) 和 P(squeeze | treatment) 才能发现 "coerced exposure" 模式。C11 的预先检查必须同样做（是否 sugar/fat consumption 在低 SES 家庭更高而不是更低）。
2. **Δ_ST 要基于 *可比的* ancestral baseline**。C2 的 "2012-2014 ancestral" 不是真正的 ancestral — 它只是 CFPS 的最早 wave。C11 应更认真选择 ancestral proxy：例如鲁南/甘南等国家早期营养调查（1982, 1992 CNSS）或 WHO-CHOP archive。
3. **DID 预趋势的 sanity check 必须先跑**。C2 的 DID 识别在未检查预趋势前看似合理；一做 event study，彻底失败。C11 的所有政策冲击（2016 健康中国 2030、2019 儿童食品标识试点等）都应先跑 event study 再决定是否做 DID。

**对 C11 的具体操作建议**：
- 选择 Δ_ST 时用 CHNS 1989–2021 panel（比 CFPS 时间跨度更长），以获得真正的 "营养转型前" vs "营养转型后" 对比。
- 必备 F2 诊断：cor(糖/脂肪摄入量, SES) 的符号。如果 < 0 → 与 C2 一样的 coerced exposure 模式。
- 如果 F1 + F2 都通过，作为**继 C4 部分 θ 之后的第二个 candidate Focal**；如果 F2 失败，C11 也降级 → **Layer B 将只剩下 C4 作为部分-Sweet 候选，论文 human pillar 面临严重危机**。

---

## 14. 这对论文整体 paradigm 的影响

### 14.1 立即后果

1. **C2 不能做 Focal-1**。当前 Focal 排名需要重新洗牌。
2. **人类 pillar 当前实际情况**：
   - C4 彩礼：**partial θ 签名**（marital_sat），Δ_ST 错号，测量限制严重 → Focal-4
   - D3 996：**完全 falsified**（bitter without sweet, coerced）→ boundary panel
   - C2 鸡娃：**完全 falsified**（F1+F2 均失败, coerced pattern）→ boundary panel (此 PDE)
   - C11 diet：**未做**
   - C1 打鸡血：**未做**
   - D1 urban：**通过**（2025 PDE）
   - D5 diet：**未做**
   - D8 housing：**未做**

3. **如果 C11 也 fail F2**，论文 human pillar 只剩下 D1 urban 作为 full-positive case + C4 部分 θ + 多个 boundary null → 这是 **Nature 级发不出**的成绩。必须考虑：
   - (a) 重新考虑 C1/C5/C12/C13 等更早被 shortlist 排除的候选
   - (b) 重新设计测量（例如 CLDS for 彩礼 with 彩礼 amount；CHNS for diet with pre-transition baseline）
   - (c) 接受 paper 降级到 Nature Human Behaviour 或 PNAS

### 14.2 论文叙事重构建议

**保留**："not every candidate behavior that looks like a Sweet Trap is a Sweet Trap" 作为论文诚实性卖点。构念的 falsifiability 恰好得到了证明。

**修正**：Figure 2 的 "一个方程三层尺度（蛾+孔雀+鸡娃）" 叙事不可行 → 改为 "一个方程两层尺度（蛾+孔雀），加上一类边界条件案例（996+鸡娃 = coerced exposure）"。论文从 "发现新构念" 转向 "发现新构念 + 精准划界"。

**回答协议 §11.1 问题**：
> C2 鸡娃是否满足 F1+F2？**不满足。F1 Δ_ST 错号；F2 直接失败（coerced exposure 模式）**。
> 双减 DID 给出的因果估计量级和 CI？**δ=−0.009 [−0.088, +0.071]，零效应且预趋势失败，不可解释**。
> Δ_ST 多少？与 Layer A 动物 pooled (+0.72) 相比？**Δ_ST(qn12012)=−0.038，与动物差 0.76 且符号相反**。
> 四原语哪些有清洁签名？**全部 null 或错号**。
> C2 在修订的 Focal 排名中应该是多少位？**降级为 boundary null panel，不入 Focal**。
> 对 C11 diet PDE 的启示？**必须先做 F2 诊断；如 F2 失败则 C11 也降级；论文整体面临人类 pillar 稀薄问题**。

---

## 15. Deliverables

| 文件 | 内容 |
|:---|:---|
| `03-analysis/scripts/C2_education_sweet_trap.py` | 端到端分析脚本 |
| `03-analysis/scripts/C2_education_sweet_trap.log` | 执行日志（stdout 镜像） |
| `02-data/processed/C2_results.json` | 完整数值记录 |
| `02-data/processed/C2_speccurve.csv` | 144-row spec curve + 衍生 |
| `00-design/analysis_protocols/pre_reg_D2_education.md` | 锁定协议 |
| `00-design/pde/C2_education_findings.md` | **本文档** |

面板 SHA-256 lock: `d1603c1e7f9776be8ddfd3ed219706e374cc210858d83140603b40cff7702c30`（再运行脚本必须重现此 hash）。

---

## 16. Integrity statement

协议无偏离。所有 primary hypothesis tests 严格按 `pre_reg_D2_education.md` §6 执行；所有 null 结果均被直接报告，无 post-hoc rescue（不更换阈值、不搬动 placebo 年份、不升级 exploratory triple interaction）。F1/F2 诊断是协议 §6.6 在构念层面的自然延伸，所得 F2-failure 判决是**构念应用的首要条件检验**，不是 post-hoc 发现。C2 降级为 boundary null 是协议 §7.2 "If H2.1 null or opposite-signed: D2 fails the Sweet pillar" 的直接应用。

**核心承诺**：不强塞 Sweet Trap 结论。不掩盖 null。F2 失败是本次 PDE 最重要的单一发现 — 它证明构念有区分力，而非普适 rescue。

---

*C2 PDE findings 完成于 2026-04-17。C2 是多域论文的第三个完成 PDE（D3 996 为第一，C4 marriage market 为第二）。C2 呈现比 C4 更彻底的构念失败：F1+F2 均不成立，四原语全部 null 或错号，DID 识别预趋势失败。与 D3 996 形成精确平行的 "coerced exposure" 模式。Human pillar 现状：仅 D1 urban 为 full positive + C4 为 partial θ。C11 diet PDE 是决定 human pillar 最终能否支撑 Nature 级论文的关键下一步。*
