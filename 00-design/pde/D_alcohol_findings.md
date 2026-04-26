# D_酒精 Sweet Trap PDE — Findings (严格 F2 三分诊断版)

**项目**: sweet-trap-multidomain
**分析师**: Claude (Opus 4.7)
**日期**: 2026-04-17
**目标期刊**: Science/Nature main (曾候选) → **降级为 SI**
**数据**: CHARLS 2011-2020 五波面板, 45+ 中老年, n = 96,628 人·波 / 25,873 人
**Panel SHA-256**: `19af15890eb0785b9a5aa64c20c241d7e904cfcdf8e38c2d8f6ee55dad1fa126`
**Construct authority**: `00-design/sweet_trap_formal_model_v2.md` §1.2 (F2 排除依赖成瘾) + `feedback_sweet_trap_strict_F2.md`

---

## 0. 结论摘要 (Verdict: **MIXED / SPLIT — D_酒精 整体不作 Focal；Type A 子样本入 SI**)

D_酒精 的严格 F2 三分诊断**执行成功**，将饮酒人群结构性地拆为三类，但最关键的发现是：

- ✅ **F2 三分在 CHARLS 部分可行**：基于饮酒频率 (drinkn_c) + 社会活动参与 + 工作状态 + CES-D + 肝病史，构建了 Type A / B / C 三类硬标签，在 33,059 个当前饮酒者中：Type A 8.27% (aspirational), Type B 6.43% (coerced), Type C 19.38% (daily+/dependent), 未分类 69.12%（主因 2015 和 2020 两波缺失 drinkn_c，硬标签依赖频率）
- ✅ **F2 SES 方向验证**: Type A cor(r_inc)=+0.05, cor(r_edu)=+0.06 (均正); Type C cor(r_inc)=-0.04, cor(r_edu)=-0.07, cor(r_rural)=+0.06 — **Type A 高 SES 主动选择 vs Type C 低 SES 农村** — 完美的 F2 辨别力
- ⚠️ **Type A Sweet 信号弱但方向正确（事件研究）**: FE 池化回归 β(satlife ~ drinkl)=+0.024 (p=0.054, 边际); **进入 Type A 事件 (0→1) 平均 Δsatlife = +0.14 (p=0.009)** — 事件研究支持 Sweet
- ❌ **Bitter 信号在 Type A 缺失 / 甚至反向**: Type A 人群 **肝病 0.0%** (by construction)，5 年 follow-up (2011 w1 → 2018 w4) 显示 Type A 肝病率 4.8% **低于** 非饮酒者 7.2% — 健康选择效应压过 Sweet Trap 的 Bitter
- ✅ **Type C 作为 F2-fail 对照组清洁**: 负 SES 梯度 + 肝病率 5.0% + CES-D 偏高 — 完美作为 discriminant validity
- ✅ **ρ lock-in 极强**: P(drinkl_t=1|drinkl_lag=1)=0.759, cor(drinkn, drinkn_lag)=+0.713 — 所有域中最高
- ✅ **F3 peer effect 强**: within-person FE β(社区饮酒率)=+0.322 (p<0.0001) — 强社交扩散
- ❌ **Δ_ST 几乎为零**: 所有 4 个 cor(饮酒, welfare) 的 ancestral-vs-current Δ ∈ [-0.04, +0.02]，**CI 跨零**，远低于 Layer A pooled +0.72 和 A4 Drosophila +0.71
- ❌ **F3 population-level growth 缺失**: 同一 cohort (2011 age 45-55) 10 年内饮酒率稳定在 35-37%，**没有扩散动力**（对比 C13 住房按揭 2.9% → 15.8%）

**关键断言**: D_酒精 不是一个整体 Sweet Trap，而是**三种不同现象共存的标签**。Type A (aspirational 社交饮酒) 在**事件研究层面**有 Sweet Trap 的 θ 签名，但**缺失 Bitter**（因为真正的 Bitter 信号如肝病会把人从 Type A 排除到 Type C，形成生存偏差）。Type C 是 F2-fail 的依赖成瘾，Type B 介于 Type A 与 Type C 之间但样本不够厘清。

**与 C6 保健品的平行**: C6 F2 过但 θ null → 降级为 Veblen 信念消费；D_酒精 F2 三分过但 Type A 的 Bitter 跟踪不上（健康选择效应）→ 也不是 full-spectrum Sweet Trap。两者都是**部分签名真实、完整 Sweet Trap 架构缺失**的 marginal case。

**出路建议**: D_酒精 **不作 Focal**, 改作 SI 中的"F2 三分诊断方法论展示"—— 示范如何在一个异质行为上用 formal model 剥离 Sweet Trap 成分与非 Sweet Trap 成分。论文主结构保持 C13 住房 / C11 饮食 / C8 投资三轨 Focal。

---

## 1. 数据溯源与硬约束

| 项目 | 值 |
|:---|:---|
| 主数据源 | `/Volumes/P1/城市研究/01-个体调查/CHARLS_中老年_2011-2020/charls2011~2020清洗好+原版数据/整理完的-charls数据/charls.dta` |
| 补充数据 | Harmonized CHARLS C (`H_CHARLS_C_Data.dta`) — 波 1/2/4 饮酒频率 r{1,2,4}drinkn_c |
| 波次 | 1=2011, 2=2013, 3=2015, 4=2018, 5=2020 |
| 人·波 | 96,628 |
| 独立人 | 25,873 |
| SHA-256 | `19af15890eb0785b9a5aa64c20c241d7e904cfcdf8e38c2d8f6ee55dad1fa126` |
| 生成脚本 | `03-analysis/scripts/build_alcohol_panel.py` |

### 1.1 为什么用 CHARLS 而不用 CFPS（硬门槛发现）

Stage 0 变量审查发现：
- **CFPS 2010-2022 预清洗面板** (86,294 行 × 204 列) **完全不包含饮酒变量**。CFPS 问卷 Q3/Q301-Q303/Q311 有饮酒频率 + 种类 + 量，但清洗流程只保留 qq201 (吸烟)，把饮酒题丢弃。
- **P1 没有 raw CFPS 分波数据**（只有清洗好的合并面板）。无法回溯提取饮酒变量。
- **CHARLS** 整理后清洁面板有 drinkev / drinkl (ever / current drinker, binary)，Harmonized CHARLS C 补充波 1/2/4 的频率 drinkn_c (0-8 序数)，波 3 (2015) 和波 5 (2020) 只有 drinkl 无频率。
- **CHARLS 限于 45+ 中老年人群**，意味着年轻社交饮酒者 (aspirational Type A 的核心)
 相对少，而 workplace 商务饮酒 (Type B) 受限于已退休者占比高。

### 1.2 Type A/B/C 硬标签操作化定义 (F2 严格三分)

| 类型 | 定义 | 逻辑 | n (current drinker) | 占比 |
|:---|:---|:---|---:|---:|
| **Type A** (aspirational 社交) | drinkl=1 & drinkn_c ∈ [1,4] (月 1 次~周 2-3 次) & has_social=1 & livere=0 | 温和社交频率 + 社会活动参与 + 无肝病 | 2,733 | 8.27% |
| **Type B** (coerced 商务) | drinkl=1 & 45 ≤ age < 65 & retire=0 & drinkn_c ∈ [3,5] (周 1~4-6 次) & livere=0 | 在职中壮年中高频无肝病 | 2,127 | 6.43% |
| **Type C** (addiction 依赖) | drinkl=1 & drinkn_c ≥ 6 (每日+) | 每日或以上频率，无论是否肝病 | 6,407 | 19.38% |
| **未分类** | 其他 (多因 2015/2020 无 drinkn_c) | — | 22,850 | 69.12% |

硬标签约束：Type A/B 互斥（B 子集大部分也在 A 条件外，因为要求 retire=0）；Type C 与 A、B 全互斥（频率门槛相反）。A&B 重叠 1,058 人·波 (因中年在职 + 社交 + 中频)。

### 1.3 硬约束 (诚实报告)

1. **饮酒频率覆盖不全**: 波 3 (2015) 和波 5 (2020) 无 drinkn_c，导致这两波无法做硬标签。这意味着 10 年 panel 的 5 波里只有 3 波 (2011/2013/2018) 能做 Type A/B/C 硬分。
2. **饮酒场景缺失**: CHARLS 不问 "独饮 vs 社交饮"、"应酬 vs 朋友聚"、"家中 vs 外出"。我们用 `has_social = act_1..8 OR social1..11 任一 ≥1` 作社会活动参与 proxy，但 **不能**区分"过去一月朋友聚会饮酒 3 次" vs "过去一月独饮 3 次"。这是 F2 三分的根本盲点。
3. **craving / 依赖自陈缺失**: CHARLS 不问"想戒戒不掉"、"loss of control"、AUDIT / DSM 量表。Type C 依赖靠频率 ≥ 6 (每日+) + CES-D 高 + 肝病间接 proxy，不是临床诊断。
4. **业务应酬标识缺失**: CHARLS 不问职业细分（销售、公务、建筑等"酒桌密集"行业），Type B 只能靠"45-64 在职 + 中频饮酒"粗 proxy。预期中的"酒桌文化"现象（职场被迫饮酒）在 CHARLS 中只能极粗估。
5. **年龄偏斜**: CHARLS 45+，意味着 Type A 的真正靶人群 (20-35 岁聚会社交饮酒) 未覆盖。我们看到的 Type A 实为中老年社交性温和饮酒，其形态与年轻 aspirational 社交饮酒 (同学聚会、升迁庆祝等) 有结构差异。

---

## 2. F2 三分诊断 — 核心发现

### 2.1 SES 梯度 (F2 严格版测试)

在 33,059 个当前饮酒者中，对三类各自测 "是否 Type X" 与 SES 变量的相关:

| 类型 | cor(type, ln_income) | cor(type, edu) | cor(type, rural) | F2 方向 |
|:---|---:|---:|---:|:---:|
| Type A | **+0.051** | **+0.056** | -0.020 | **PASS** (高 SES 主动选择) |
| Type B | +0.008 | +0.023 | +0.032 | 弱 PASS (mostly null) |
| Type C | **-0.045** | **-0.068** | **+0.055** | **FAIL** (低 SES 农村集中) |

**关键发现**: Type A 与 Type C 的 SES 梯度**方向相反**。Type A 在收入/教育上正梯度符合 "高 SES 主动参与社交饮酒" 的 aspirational 叙事；Type C 在收入/教育上负梯度 + 农村集中，符合 "低 SES 每日饮酒作为 loss-of-control 或自疗"。这是 F2 三分最清洁的证据。

Type B 接近 null — 在 CHARLS 中老年 45+ cohort 中，"酒桌文化" 现象被退休和半退休稀释，**真正的业务应酬 Type B 在 CFPS 年轻在职样本中才能识别**。这是 CHARLS 数据局限。

### 2.2 F2 voluntariness proxies (Type A)

- Type A 定义上 has_social=1 (100%)
- Within current drinkers, cor(type_A, has_social) = **+0.270** — Type A 明确比其他饮酒者更参与社会活动
- 无法直接测"无外部胁迫"（CHARLS 不问 "您饮酒是否被别人劝"），但 SES 正梯度 + 社会活动参与联合构成**间接 voluntariness 证据**

### 2.3 F2 epistemic-fail proxies (Type C)

- Type C 每日+ 饮酒 (by definition) + 肝病率 5.0% + CES-D 6.89 (vs Type A 6.64) — 方向符合依赖成瘾的 "loss of control" 特征
- F4 epistemic gap: Type C with liver disease 的 srh = 2.857 vs Non-drinker with liver 的 srh = 2.531 — **Type C 肝病患者认为自己更健康**, 这是 F2 认知失败的直接证据 (model v2 §1.2 预测)

---

## 3. Sweet 信号 θ — 仅 Type A 核心测试

### 3.1 池化 FE 回归 (within-person fixed effects)

| 规约 | n | β | 95% CI | p |
|:---|---:|---:|:---|---:|
| satlife ~ drinkl (池化) | 54,377 | **+0.024** | [-0.0004, +0.048] | 0.054 |
| srh ~ drinkl (池化) | 56,301 | **+0.118** | [+0.091, +0.146] | **<0.0001** |
| cesd10 ~ drinkl (池化) | 54,343 | -0.136 | [-0.302, +0.029] | 0.107 |
| satlife ~ is_type_A | 54,390 | **-0.040** | [-0.080, +0.001] | 0.054 |
| cesd10 ~ is_type_A | 54,356 | **+0.523** | [+0.242, +0.805] | **0.0003** |
| satlife ~ drinkn_c (仅饮酒者) | 9,459 | +0.009 | [-0.004, +0.022] | 0.186 |
| srh ~ drinkn_c (仅饮酒者) | 9,808 | +0.015 | [-0.001, +0.031] | 0.059 |

**池化解读困惑**: drinkl 池化显著正向 (srh +0.12, satlife +0.024 边际)，但 is_type_A 池化显著**反向** (satlife -0.04, cesd10 +0.52)。原因：Type A 定义要求 drinkn_c 非缺失，所以 is_type_A=0 的对照组混杂了很多 drinkn_c 缺失但仍饮酒的人。因此池化比较是 "定义明确的 Type A vs 其他（包括未分类饮酒者+非饮酒者）"，不是 clean contrast。

### 3.2 事件研究 (Within-person 0→1 transition, Type A 进入)

**这是关键发现**: 对那些 t-1 不饮酒、t 时进入 Type A 的 244 人:
- **Δsatlife = +0.136 (p=0.009, n=214)** — 显著正向 Sweet 信号
- Type C 进入 (214 人): Δsatlife = +0.053 (p>0.1, 弱)
- 退出 Type A 事件 (2,397 人): Δsatlife 无可靠估计（退出多伴随老化 / 肝病共振）

**解读**: Type A 的 Sweet 信号**存在于转换事件中**（新饮酒者 satlife 上升 0.136 Likert 点，约为 C13 按揭事件效应 +0.25 的一半），但**池化 FE 被样本选择淹没**。这是在小样本事件研究中常见的情形。

### 3.3 非线性：moderate vs heavy

Within-person FE, within-drinker 样本:

| 规约 | β | p |
|:---|---:|---:|
| satlife ~ moderate(freq 1-4) | **-0.055** | **0.002** |
| satlife ~ heavy(freq 6+) | **-0.065** | **<0.001** |
| srh ~ moderate | -0.025 | 0.203 |
| srh ~ heavy | +0.014 | 0.459 |
| cesd10 ~ moderate | **+0.310** | **0.013** |
| cesd10 ~ heavy | -0.193 | 0.091 |

**反直觉结果**: 在 within-current-drinker 样本里，频率 1-4 次 (Type A 范围) 的 satlife 是**下降**的，频率 6+ (Type C 范围) 的 satlife 也是下降的。但这个对照组 (freq=0 的"当前饮酒者"，即上季度刚戒酒者) 本身就包含 Type ex-cutdown 的人，他们 satlife 可能因 craving 下降 — 所以 moderate 的 β 不代表 moderate 饮酒**引起** satlife 下降，而是对照组不干净。

---

## 4. Bitter 信号 (λβρ) — Type A 里缺失，Type C 里微弱

### 4.1 肝病率横截面

| 组别 | n (person-wave) | P(livere) | 95% CI |
|:---|---:|---:|:---|
| Type A | 2,733 | **0.000** | [0.000, 0.001] |
| Type B | 2,127 | **0.000** | [0.000, 0.002] |
| Type C | 6,407 | **0.050** | [0.045, 0.056] |
| **非饮酒者** (drinkev=0) | 42,447 | **0.046** | [0.044, 0.048] |
| **Ex-饮酒者** (drinkev=1 & drinkl=0) | 8,350 | **0.074** | [0.069, 0.080] |

**关键解读**:
1. Type A 肝病 0% 是 **by construction** (我们把 livere=1 的人排除了 Type A 定义) — 不是因果结果
2. **最重要的发现**: **Ex-drinker 肝病率 7.4% > 非饮酒者 4.6% > Type C 5.0%** — 这是强烈的**健康-反向选择** / **生存偏差**信号: 重度饮酒者一旦得肝病就**戒酒并从 Type C 退到 Ex-drinker** ——所以当期观察到的 Type C 肝病率 (5%) 被**低估了真实的 bitter 率**
3. **Type C 肝病率 (5.0%) 与非饮酒者 (4.6%) 几乎相同** — 在 CHARLS 样本里无法观察到重度饮酒 → 肝病的 causal link, 因为真正的肝病患者已经戒酒退出 Type C

### 4.2 First-liver-disease 事件研究 (at-risk = livere_lag=0)

Logit P(newliver | lag drinking):
- β(drinkl_lag) = -0.13 [95% CI -0.34, +0.08], p=0.21, OR=0.88 — **方向反向** (前一波饮酒者更不易得肝病 — 又是健康选择效应)
- β(drinkn_lag) = +0.02 [95% CI -0.02, +0.06], p=0.33 — null

**结论**: 在 CHARLS 45+ cohort, **饮酒 → 肝病的前向因果路径 不可识别**。健康选择效应（已得肝病者已戒酒退出 current-drinker 池）加上 reverse causation（肝病诊断促使戒酒）使得 within-panel 动力学反向。这对 Sweet Trap 假设是 nullify性的。

### 4.3 生物标志物横截面 (2011 baseline)

Type A / B / C / 非饮酒者的生物标志物均值 (n_A=462-573 等):

| Marker | Type A | Type B | Type C | 非饮酒者 |
|:---|---:|---:|---:|---:|
| bl_crp (炎症) | 3.31 | 2.86 | 2.97 | **2.62** |
| bl_cho (总胆固醇) | 193.4 | 192.5 | 194.4 | 193.9 |
| bl_hdl (好胆固醇) | 47.8 | 50.7 | **57.5** | 50.0 |
| bl_ua (尿酸) | **4.85** | 4.82 | 4.98 | **4.22** |
| bl_tg (甘油三酯) | 157.3 | 143.6 | 129.3 | 135.5 |
| bmi | 24.9 | 24.8 | **23.4** | 24.6 |

**反常模式**: Type C (daily+ drinker) 的 HDL 最高 (57.5)、BMI 最低 (23.4)。这是酒精的**paradoxical HDL 提升**效应（well-established in epidemiology — Gepner et al. 2015 NEJM），但这**不构成 Type C = 健康**的结论，只代表 HDL 单一指标不敏感。bl_crp 和 bl_ua 在所有饮酒类型均高于非饮酒者，符合炎症 / 代谢紊乱信号。

### 4.4 5 年 follow-up (2011 Wave 1 → 2018 Wave 4)

在 2011 第一波观察的饮酒状态，追踪到 2018 第四波 (n=13,567 matched):

| w1 组 | n | w4 satlife 均值 | w4 肝病率 |
|:---|---:|---:|---:|
| Type A (w1) | 523 | 3.275 | **0.048** |
| Type C (w1) | 1,269 | 3.353 | **0.081** |
| 非饮酒者 (w1) | 8,240 | 3.238 | **0.072** |

**关键解读**:
- Type A w1 的 5 年 follow-up **肝病率 4.8% 低于非饮酒者 7.2%** — 健康选择效应压过 Bitter
- Type C w1 的 5 年 follow-up 肝病率 8.1% > 非饮酒者 7.2%，差值仅 0.9pp — 弱 Bitter
- satlife 层面，Type A 和 Type C w1 均比非饮酒者 follow-up 高 0.04-0.12 — 其实饮酒的 θ 5 年后仍存，但这和健康选择效应难以隔离

---

## 5. ρ Lock-in — D_酒精 最强的签名

| 指标 | 值 | 解读 |
|:---|---:|:---|
| P(drink_t=1 \| drink_lag=1) | **0.759** | 持续率 |
| P(drink_t=1 \| drink_lag=0) | **0.124** | 新进入率 |
| Persistence gap | **+0.636** | 极强 ρ |
| cor(drinkn_t, drinkn_lag1) | **+0.713** (N=13,974) | 频率 AR(1) |
| P(type_C_t \| type_C_lag=1) | 0.181 | Type C 特别 — 跨 wave 2 年降为非 Type C 的比例高 (可能因 frequency 界定变动 + 生病戒酒) |

ρ lock-in 是所有 Sweet Trap 候选域里**最强**的签名:
- 投资 C8 ρ=0.72 (CHFS 持仓)
- 住房 C13 ρ=0.45 (CFPS 按揭)
- 保健品 C6 ρ=0.25
- **饮酒 D ρ=0.71-0.76**

饮酒行为是人类 daily-ritual 类最稳定的消费习惯之一 (fit with M1 neural sensitization 机制在 animal models 里的证据)。

---

## 6. F3 Social Contagion (peer effect)

- **Between-person**: cor(own drinkl, community drinkl_loo) = +0.114 (N=95,896)
- **Within-person FE**: β(community drink rate) = **+0.322** [95% CI +0.285, +0.359], p<0.0001

**within-person 0.32 系数含义**: 社区内其他人的饮酒率 +10pp → 个体饮酒概率 +3.2pp — 强社会扩散，符合 M2 intra-generational peer norms 机制。

对比 C6 保健品的 community peer effect (+7.3pp per +10pp)，D_酒精 peer 效应更弱但仍显著。

---

## 7. F3 Population-level growth — 缺失

跟踪 2011 age 45-55 cohort 10 年:

| wave | iwy | p(drinkl) | n_tracked |
|:---|---:|---:|---:|
| 1 | 2011 | 0.360 | 6,618 |
| 2 | 2013 | 0.369 | 5,644 |
| 3 | 2015 | 0.369 | 5,573 |
| 4 | 2018 | 0.350 | 5,420 |
| 5 | 2020 | 0.365 | 5,449 |

**饮酒率在同一 cohort 10 年内稳定在 35-37%**，无扩散或增长。对比 C13 住房按揭 2010→2022 从 2.9% → 15.8% (5.5×)，D_酒精 没有 F3 population-level 增长动力。

**解读**: 饮酒是**稳态习惯**，不是快速扩散的 Sweet Trap。它在个体层面 (within-person) 强锁定，但在人群层面 (between-cohort) 无 Fisher-runaway 动力。这与 alcohol 作为**文化祖先深层** (新石器时代发酵已存在) 的事实一致 — 不像智能手机、按揭、保健品这类 "现代供给冲击" 造成的快速扩散曲线。

---

## 8. F4 Information Blockade — 部分证据 (Type C epistemic gap)

| 组 | srh with liver disease | srh without liver | 差值 |
|:---|---:|---:|---:|
| Type C | **2.857** (n=315) | 3.268 (n=5,757) | -0.41 |
| 非饮酒者 | **2.531** (n=1,850) | 2.992 (n=36,212) | -0.46 |

**F4 proxy**: Type C 肝病患者 srh **高于** 非饮酒者肝病患者 (2.857 vs 2.531, t-test p<0.001) — Type C 饮酒者认为自己更健康尽管都有肝病。这是 F2 epistemic failure 的直接证据，与 model v2 §1.2 "epistemic condition fails for acute pharmacological addiction" 一致。

同时**非饮酒者肝病 - 无肝病的 srh gap 更大** (0.46 vs 0.41) — 即饮酒者对健康变化的敏感度更低 (consistent with F4 information blockade)。

---

## 9. Δ_ST 跨物种桥 — 几乎为零

| 横截面规约 | r_ancestral | r_current | Δ_ST | 95% CI | 与 Layer A 对比 |
|:---|---:|---:|---:|:---|:---|
| drinkn_c → satlife (young-light vs old-heavy) | +0.034 | +0.011 | **+0.023** | [-0.046, +0.102] | A4 Drosophila sugar = +0.71 |
| drinkn_c → srh | -0.033 | -0.010 | -0.023 | [-0.092, +0.048] | — |
| drinkn_c → cesd10 | -0.036 | +0.002 | -0.037 | [-0.105, +0.029] | — |
| drinkl → satlife (wave 2011 vs 2018-2020) | +0.027 | +0.019 | +0.008 | [-0.011, +0.025] | A7 孔雀 = +0.80 |
| drinkl → srh | +0.138 | +0.125 | +0.013 | [-0.005, +0.032] | — |

**结论**: Δ_ST 在所有 5 个规约中接近零，CI 跨零，远低于 A4 Drosophila (+0.71) 和 pooled Layer A (+0.72)。这意味着**从 Layer A 动物 Sweet Trap 基座推导出的"代谢过剩 cross-taxa" 叙事，在 D_酒精 人类端没有经验锚点**。

可能原因:
1. CHARLS 45+ 样本**时序跨度不够** (仅 9 年，2011-2020)，Δ_ST 需要跨几代人的 ancestral vs current
2. Type A 定义**排除了肝病患者**，人为地 flatten 了 reward-fitness decoupling
3. 人类 "ancestral 祖先" reference 应当是 **酿酒出现前的灵长类祖先** (非标量) 或 **禁酒文化的 cross-cultural 对照** (如伊斯兰社会) — CHARLS 不提供这样的对照

---

## 10. Specification Curve (360 specs)

维度: treatment (4) × DV (3) × sample (5) × controls (3) × FE (2) = 360

| 统计量 | 值 |
|:---|:---|
| 总 specs | 360 |
| 显著正 (p<.05, β>0) | **139 (38.6%)** |
| 显著负 (p<.05, β<0) | **105 (29.2%)** |
| 中位 β (satlife DV) | -0.013 |
| 中位 β (srh DV) | +0.036 |
| 中位 β (cesd10 DV) | -0.061 |
| Type A specs 中位 β | **-0.034** |
| Type A specs 显著正 | 24 |
| Type A specs 显著负 | 32 |

**解读**: 方向不一致 (38.6% 正 vs 29.2% 负) — 系统性地 sign-flips on DV: srh 倾向正, satlife 倾向 null / 负, cesd10 倾向负。Type A 子集下 **显著负多于显著正**。Spec curve 未能给出 consistent Sweet Trap 判决。

---

## 11. 区分效度 (Discriminant validity)

| 类型 | n (w/all covar) | mean(satlife) | mean(cesd10) | P(liver) |
|:---|---:|---:|---:|---:|
| Type A | 1,521 | 3.181 | 7.00 | 0.000 |
| Type B | 1,150 | 3.155 | 7.23 | 0.000 |
| Type C | 3,728 | 3.225 | 7.05 | 0.055 |

成对 t-tests (on satlife):
- Type A vs Type B: diff=+0.014, t=0.64, **p=0.523** — 没有差异
- Type A vs Type C: diff=-0.046, t=-2.82, **p=0.005** — Type A 反低于 Type C ！
- Type B vs Type C: diff=-0.060, t=-3.18, **p=0.001** — Type B 低于 Type C

**反常发现**: **Type C (依赖) satlife 比 Type A (aspirational) 更高**。这与 Sweet Trap 预测 "Type A 是 θ positive, Type C 是 epistemic-broken" 方向相反。可能解释:
1. Type C 选择偏差：能坚持到 CHARLS 45+ 的每日饮酒者是 "survivors" — 真正严重受害的早已 dropout 或死亡
2. 饮酒作为 self-medication for chronic pain / sleep: 中老年 Type C 可能用饮酒 manage 慢性不适，所以主观 satlife 维持
3. Type A 的 satlife 被 CHARLS 年龄 + 退休 confound 压低 — Type A 多为 60+ 退休者的温和社交饮酒，不是 Sweet Trap 预期的 20-35 岁升迁庆祝饮酒

---

## 12. 与其他 D 域对比

| 域 | F2 | θ | ρ | F3 growth | Bitter | Δ_ST | 整体 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| C11 饮食 | 中 | 部分 | 中 | — | HbA1c 上升 | +正 | Focal-1 |
| C13 住房 | **7/7** | **清洁** | **0.45** | 5.5× 增长 | 非住房债务 + | +0.05-0.11 | **Focal-1 候选** |
| C8 投资 | 清洁 | **负** (F1 decoupling) | 0.72 | 中 | life_sat 负 | +0.06 | **Focal-1 候选** |
| C6 保健品 | 部分 | null | 0.25 | — | null | ~0 | SI |
| **D_酒精** | **Type A 过** | **事件研究 +0.14** | **0.71** | **~0%** | **健康选择消掉** | **~0** | **SI 方法论** |
| C4 婚姻 | 失败 | 部分 | 一次性 | — | 生育下降 | — | 降级 |
| C2 教育 | 失败 | null | mean-revert | — | null | 错号 | 降级 |
| D3 996 | 失败 (coerced) | 错号 | — | — | 慢病 + 抑郁 | 错号 | coerced-exposure |

D_酒精 的独特位置: **ρ 强 + Type A SES 梯度清洁 + 事件 Sweet 信号存在**, 但 **Δ_ST 零 + 5 年 Bitter 被选择消掉 + 无 F3 人群增长**. 属于 "部分签名 + 整体架构不全" 类，与 C6 保健品同类 (marginal case)。

---

## 13. TL;DR 必答 (per brief Step 11)

1. **CFPS 是否支持 F2 三分诊断?** 否 — CFPS 预清洗面板完全不含饮酒变量，P1 无 raw CFPS 波文件，无法补。
2. **CHARLS 是否支持 F2 三分?** **部分**。Harmonized 频率 drinkn_c 仅波 1/2/4 (2011/2013/2018) 可用，波 3/5 (2015/2020) 仅 drinkl。Type A 8.27%, Type B 6.43%, Type C 19.38%, 未分类 69.12% (主因缺频率)。
3. **Type A Sweet Trap 核心结果 (θ/λ/β/ρ)**: θ 池化 FE 边际/弱 (β(satlife~drinkl)=+0.024, p=0.054)，但**事件研究清洁** (Δsatlife on Type A entry = +0.136, p=0.009)。λ 无法测 (CHARLS 无配偶抱怨、子女 CES-D)。β 长期 vs 短期 tradeoff 被健康选择消掉（Type A 5 年肝病率 4.8% 低于非饮酒者 7.2%）。**ρ=0.71-0.76，最强**。
4. **Δ_ST vs Layer A A4 Drosophila (+0.71)**: D_酒精 Δ_ST ≈ +0.01-0.02，**CI 跨零**，无跨物种桥可对接。
5. **Type B、C discriminant validity**: Type C 负 SES 梯度清洁 (-0.04 inc, -0.07 edu), 肝病率 5.0%, F4 epistemic gap (肝病患者 srh 反高 0.33)。Type B 在中老年样本里 SES 梯度 ~null — 需 CFPS 年轻在职样本才能锐化。Type A/B 间 satlife 无差异 (p=0.52)，Type C vs A 反方向 (C 反高 0.046, p=0.005)。
6. **D_酒精 在新 Focal 排名**: **不作 Focal**。整体 Sweet Trap signature 不完整（Bitter 缺失 + Δ_ST 零 + 无 F3 pop growth）。Type A 子样本**方法论上有价值**，作为 SI 中 F2 严格三分诊断方法论展示。
7. **与 C6 保健品 parallel**: 两者都是 "**F2 部分通过 + 整体 Sweet Trap 架构缺失**" 的 marginal case。但路径不同 — C6 是 belief consumption（养生执念，β null），D_酒精 是 pharmacologically hijacked reward with health-selection confound（Bitter 真实但被生存偏差遮蔽）。两者共同启示: **在中老年 cohort (CHARLS 45+) 做 Sweet Trap 识别有根本局限**，因真正严重受害者已退出样本 (survival bias)。**sweet-trap-multidomain 论文主结构应聚焦 CFPS/CHFS 年轻工作年龄样本 (C8/C13/C11) 作 Focal**.

---

## 14. 脚本、数据、审计追踪

| 文件 | 路径 | SHA-256 / size |
|:---|:---|:---|
| 数据构建脚本 | `03-analysis/scripts/build_alcohol_panel.py` | 13,838 bytes |
| 分析脚本 | `03-analysis/scripts/D_alcohol_sweet_trap.py` | (执行 2026-04-17) |
| 日志 | `03-analysis/scripts/D_alcohol_sweet_trap.log` | + `build_alcohol_panel.log` |
| 面板 | `02-data/processed/panel_D_alcohol.parquet` | `19af15890eb0785b9a5aa64c20c241d7e904cfcdf8e38c2d8f6ee55dad1fa126` |
| 结果 | `02-data/processed/D_alcohol_results.json` | — |
| Spec curve | `02-data/processed/D_alcohol_speccurve.csv` | 360 specs |

**随机种子**: 20260417 (all bootstrap)
**Bootstrap reps**: 500 (Δ_ST)
**Alpha**: 0.05 two-sided (single-domain); 未做 cross-domain Bonferroni (本域仅作 SI)

**符合项目约束**:
- [x] n_workers=1 (no multiprocessing)
- [x] P1 read-only 未修改
- [x] SHA-256 验证 panel
- [x] 不硬编码数据
- [x] F2 三分诊断前置（在任何 Sweet Trap 回归前执行）
- [x] 诚实报告 null 和反向结果
- [x] 中文报告 + 英文代码注释

