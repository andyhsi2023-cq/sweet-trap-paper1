# Sweet Trap Gap Matrix: 8 Domains × 3 Gap Dimensions
**Compiled:** 2026-04-17
**Purpose:** Stage 1 domain selection decision support

## Interpretation Guide

**Gap Dimensions:**
- **Measurement gap**: Does a study exist that measures BOTH the endorsement (θ/satisfaction/pride) AND the harm (health/financial/family deterioration) within the same sample?
- **Identification gap**: Is there a within-person longitudinal causal design (or near-equivalent) that isolates the endorsement-harm relationship?
- **Mechanism gap**: Is the Sweet Trap four-primitive mechanism (θ, λ, β, ρ) formally parameterized for this domain?

**Scores (gap severity — higher = more opportunity for us):**
- 3 = Gap completely open (no prior work)
- 2 = Gap partially addressed (some evidence but not within-person/formal)
- 1 = Gap mostly closed (existing literature is strong; our increment is incremental)
- 0 = No gap (domain already saturated; not worth pursuing)

---

## Gap Matrix

| Domain | Measurement Gap | Identification Gap | Mechanism Gap | Total Gap Score | CFPS Data Quality | Priority |
|:-------|:---------------:|:------------------:|:-------------:|:---------------:|:-----------------:|:--------:|
| 1. Urban over-investment | 0 | 0 | 0 | **0** | ✅ Excellent | DONE (Study 1) |
| 2. 鸡娃教育 | 3 | 3 | 3 | **9** | ⚠️ Moderate | HIGH |
| 3. 996 过劳 | 2 | 3 | 3 | **8** | ✅ Good | HIGH |
| 4. 彩礼婚恋 | 3 | 2 | 3 | **8** | ⚠️ Moderate | HIGH |
| 5. 高糖高脂 | 2 | 2 | 2 | **6** | ⚠️ Moderate | MEDIUM |
| 6. BNPL/信用卡 | 3 | 3 | 2 | **8** | ⚠️ Low-Moderate | MEDIUM |
| 7. 短视频/社媒 | 2 | 2 | 2 | **6** | ⚠️ Moderate | MEDIUM |
| 8. 高档住房/车 | 2 | 2 | 2 | **6** | ✅ Good | MEDIUM |

---

## Detailed Cell Justifications

### Domain 2: 鸡娃教育 (Total: 9/9)

| Gap | Score | Justification |
|:----|:-----:|:--------------|
| Measurement | 3 | Zero studies measure parental pride/endorsement + child mental health trajectory in same panel. Ethnographic work exists (Fong 2004) but no quantitative within-person design. |
| Identification | 3 | All existing work is cross-sectional or uses endogenous selection into shadow education. No within-person FE design. CFPS provides parent ID + child education module across waves. |
| Mechanism | 3 | θ (parental status pride), λ (cost transferred to child), β (short-term status gain over long-term child wellbeing), ρ (arms-race lock-in) — none formally parameterized. |

**Additional note:** 双减 policy (2021) creates a natural quasi-experiment: sudden reduction in tutoring availability. Pre/post within-person comparison is possible in CFPS 2022 wave if available.

---

### Domain 3: 996 过劳 (Total: 8/9)

| Gap | Score | Justification |
|:----|:-----:|:--------------|
| Measurement | 2 | Kivimäki et al. (2015) documents harm at scale; Goldin (2014) documents career reward. But no single study measures both career endorsement AND health/family outcomes within-person panel. |
| Identification | 3 | Epidemiological meta-analyses are cross-sectional/prospective cohort without within-person FE. No Chinese CFPS within-person design exists. |
| Mechanism | 3 | β + λ (health cost to future self + family) + ρ (career norms) — not formally unified in one study. |

---

### Domain 4: 彩礼婚恋 (Total: 8/9)

| Gap | Score | Justification |
|:----|:-----:|:--------------|
| Measurement | 3 | Anderson (2007) JEP review and Wei & Zhang (2011) JPE cover market effects, not within-person satisfaction + financial strain trajectory. |
| Identification | 2 | Wei & Zhang (2011) use sex-ratio variation for identification (a strong IV). We have this template. But no within-person design yet. |
| Mechanism | 3 | ρ (social norm compliance) as Sweet Trap mechanism is completely novel in formal behavioral economics. |

---

### Domain 5: 高糖高脂 (Total: 6/9)

| Gap | Score | Justification |
|:----|:-----:|:--------------|
| Measurement | 2 | Hall et al. (2019) RCT measures calorie intake + weight but not satisfaction endorsement. Longitudinal cohorts (Fiolet 2018) have diet + health but no satisfaction measure. |
| Identification | 2 | Hall (2019) is gold-standard causal for calorie effect; but for satisfaction-endorsement paradox, no RCT exists. Within-person panel is the gap. |
| Mechanism | 2 | β (present bias in food) well-theorized (Cawley & Ruhm 2011). λ (cost to health system / future self) quantified in epidemiology. But formal joint parameterization absent. |

---

### Domain 6: BNPL/信用卡 (Total: 8/9)

| Gap | Score | Justification |
|:----|:-----:|:--------------|
| Measurement | 3 | Gathergood (2012) has debt + life satisfaction but UK cross-section. No Chinese CFPS panel study. BNPL is very recent phenomenon (post-2018). |
| Identification | 3 | Credit card/BNPL adoption in China has temporal variation (2015-2020 rapid expansion) but no instrument-based design exists in literature. |
| Mechanism | 2 | β clearly theorized (Agarwal et al. 2009). λ less developed. ρ (spending habit lock-in) partially addressed in behavioral finance. |

**Risk note:** CFPS pre-2022 may undercount BNPL-specific behavior. Domain 6 may have high identification gap but low data availability — lower effective priority.

---

### Domain 7: 短视频/社媒 (Total: 6/9)

| Gap | Score | Justification |
|:----|:-----:|:--------------|
| Measurement | 2 | Allcott et al. (2020) measures wellbeing + re-endorsement behavior. That's the endorsement-harm gap partially addressed. But Chinese CFPS panel with Douyin-specific use is unmeasured. |
| Identification | 2 | Braghieri et al. (2022) strong DiD; Allcott et al. (2020) strong RCT. Within-person FE for Chinese context is the gap, but identification bar is high after these two papers. |
| Mechanism | 2 | β + ρ (re-engagement loop) discussed in literature but not formally parameterized as Sweet Trap four primitives. |

---

### Domain 8: 高档住房/车 (Total: 6/9)

| Gap | Score | Justification |
|:----|:-----:|:--------------|
| Measurement | 2 | Nettleton & Burrows (1998) and Wood et al. (2015) document mortgage stress + wellbeing in UK/AU. No Chinese within-person panel. |
| Identification | 2 | Fang et al. (2016) NBER have strong macro identification of housing boom. Individual-level within-person FE is the gap. |
| Mechanism | 2 | Frank (2007) and Luttmer (2005) cover θ (positional) and ρ (keeping up with Joneses). λ for housing (cost externalized to next generation via asset price bubble) is partially addressed. |

---

## Priority Recommendation for Stage 1

### Tier 1 — Highest priority (maximum gap + adequate CFPS data)
1. **Domain 3: 996 过劳** — Gap 8/9, CFPS work module is strong (working hours, income, health, family)
2. **Domain 2: 鸡娃教育** — Gap 9/9, but 双减 natural experiment is a bonus; CFPS child education module needs audit
3. **Domain 4: 彩礼婚恋** — Gap 8/9, but CFPS coverage of bride price is uncertain; priority conditional on data audit

### Tier 2 — Strong candidates (gap exists, data adequate)
4. **Domain 8: 高档住房/车** — Gap 6/9 but CFPS asset module is excellent; positional goods story is clean
5. **Domain 5: 高糖高脂** — Gap 6/9; CFPS dietary module needs audit; mechanism well-theorized

### Tier 3 — Conditional (data or identification uncertainty)
6. **Domain 7: 短视频/社媒** — Gap 6/9 but Allcott (2020) + Braghieri (2022) are strong priors; identification bar very high; CFPS internet module is shallow
7. **Domain 6: BNPL/信用卡** — Gap 8/9 but CFPS pre-2022 doesn't capture modern BNPL; very recent phenomenon

### Recommended Selection for ≥5 Focal Domains
**Core 5 (commit):** 1 (already done) + 3 (overwork) + 2 (education) + 8 (housing/vehicle) + 5 (diet)
**Backup 2:** Domain 4 (bride price, if data available) + Domain 7 (social media, if CFPS internet module is sufficient)
**Drop for now:** Domain 6 (BNPL — too recent, CFPS gap)

---

## Cross-Domain Meta-Observation

The matrix reveals a consistent pattern: **behavioral mechanisms are individually established in each domain, but no study has ever applied a unified four-primitive construct across domains simultaneously.** The literature lives in separate silos:
- Labor economics (Domain 3)
- Education economics (Domain 2)
- Family economics / sociology (Domain 4)
- Nutritional economics / public health (Domain 5)
- Digital economics (Domain 7)
- Consumer finance (Domain 6)
- Urban/real estate economics (Domain 8/1)

This silo structure is precisely the novelty claim: Sweet Trap is a **domain-invariant behavioral equilibrium pattern**, not a domain-specific phenomenon. The NHB cross-domain framing is justified because no prior paper has attempted this unification.
