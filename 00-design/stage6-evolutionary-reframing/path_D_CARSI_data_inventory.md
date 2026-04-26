# Path D — CARSI 基因/生物医学数据源盘点

**Date:** 2026-04-24
**Purpose:** 在方案 C（V4 四部分架构 + Part 4 基因证据）框架下，盘点 CARSI（浙江大学 IdP）可访问的基因与生物医学资源，判断其对 H6a-H6f 六类基因证据的增量价值。
**Access path:** CARSI 浙江大学 SSO 登录 → https://ds.carsi.edu.cn/resource/resource.php
**Scan coverage:** 333 条全量资源中"医学" (104) + "理学" (109) 学科子集，关键词搜索"基因/生物/分子"。

---

## 1. 一句话结论

**CARSI 对 Part 4 的增量价值主要是文献全文权限，不是基因数据库本身。** Part 4 主体分析（正选择扫描、GxE interaction、收敛正选择、PRS、ancient DNA）的**数据源全部在免费开放库**（Ensembl / NCBI / UniProt / GWAS Catalog / PGS Catalog / AADR），不需要机构订阅。CARSI 的真正增值只有一件事：**CNGBdb 国家基因库 + Nature / ScienceDirect / Cell Press / Wiley 等文献全文**，分别为 Part 4 补上**中国本地物种基因组**和**paywalled 论文全文**两块。

---

## 2. CARSI 上与基因/生物医学相关的资源

### 2.1 基因数据库类（唯一一项）

| 资源 | 类型 | 访问 | 对 Part 4 价值 |
|---|---|---|---|
| **CNGBdb 国家基因库生命大数据平台** | 研究数据 1 万条 + 索引 620 亿条 + 项目数据 5236 条 | **免费**（浙大 CARSI 直通） | **中-高**。华大基因自产测序数据 + NCBI/EBI/DDBJ 中文镜像 + 10 检索子库（文献/变异/基因/蛋白质/序列/项目/样本/实验/测序/组装） |

**CNGBdb 对 H6 的具体用处：**
- **H6a 正选择扫描**：可补充华大对**非模式物种**（Nematostella Cnidaria 参考组；Aplysia 软体海兔；各种甲壳类）的测序数据。这些物种在 Ensembl Metazoa 覆盖有限。
- **H6c 收敛正选择平行模式**：华大有**中国本土物种**（大熊猫、金丝猴、藏羚、藏狐、高原兽类）的 genome，其奖赏受体选择扫描可独立地给 H6c 增加 3-5 个 lineages。
- **变异子库**（CMDB-based）：对人类 GxE interaction 分析可提供东亚特异的变异数据，补 FinnGen+BBJ+MVP 之外的中国人群信息。

**访问流程附官方文档**：
- 流程 PDF：https://mgmt.carsi.edu.cn/frontend/web/member_files/cngb.org/国家基因库生命大数据平台.step_file.pdf
- 直达入口：CARSI 登录后点"访问资源" → 自动 Shibboleth 到 cngb.org

### 2.2 文献全文权限类（核心价值层）

| 资源 | 类型 | 对 Part 4 用途 |
|---|---|---|
| **NATURE 校购** | Nature Portfolio 全套 | Nature Genetics / Nature Ecol Evol / Nat Rev Genet / Nature Commun — Part 4 引用主力 |
| **SCIENCEDIRECT 校购** | Elsevier 全套 | Cell Press（Cell / Cell Rep / Mol Cell / Curr Biol） / Trends in Genetics / Heredity 等 |
| **Cell Press**（ScienceDirect 内） | Cell / Curr Biol / Neuron / Mol Cell | H6a 灵长类甜受体正选择、H6b DRD2 TaqIA 人类研究主阵地 |
| **Springer Link 校购** | Springer 全套 | Heredity / Genet Selection Evolution / BMC Evol Biol |
| **WILEY Online Library** | Wiley 全套 | Evolution / Mol Ecol / J Evol Biol / Evol Applications |
| **EMBASE 校购** | 生物医学/药理学文摘 | GWAS catalogue-derived 文献 + 精神病学遗传学 |
| **EMBO Press** | EMBO J / EMBO Rep / EMBO Mol Med / Mol Syst Biol | 分子演化机理综述 |
| **CLINICALKEY** | Elsevier 临床全文 | 人类 Sweet Trap 表型相关临床数据（BMI, MetS, addiction） |
| **SCOPUS 校购** | 文摘+引文 27 一级学科 | Part 4 综述引用计量 |
| **Cochrane Library** | 系统评价 | Part 2 PRISMA 方法论支撑；Part 4 GxE 系统评价 |
| **CAS SciFinder + REAXYS** | 化学/化合物数据 | Part 3 配体结合结构域分析辅助 |
| **本地 PubMed** | 华科-骥灏版 PubMed | 中文用户便利入口 |
| **Rockefeller University Press** | J Exp Med / J Gen Physiol / JCB | 补 Layer E 实验实证（放 Future Work） |
| **中国学术前沿期刊网** | 浙大出版社中文期刊 | 中文摘要与国内作者工作定位 |

### 2.3 CARSI 上**没有但 Part 4 必用**的资源（均为开放库，无需订阅）

| 资源 | 状态 | 用途 |
|---|---|---|
| Ensembl + Ensembl Metazoa | 免费开放 | H4a/H4b/H6a 核心基因组来源 |
| NCBI Gene / Protein / SRA / BLAST | 免费开放 | 同上 |
| UniProt | 免费开放 | 蛋白质序列 + 注释 |
| InterPro | 免费开放 | Domain architecture (H4b Jaccard 核心) |
| OrthoDB / OrthoFinder | 免费 | 直系同源推断 |
| PAML codeml | 免费工具 | H4a/H6a branch-site dN/dS |
| TimeTree 5 | 免费 | 分化时间树 |
| STRING + Reactome | 免费 | H4b 下游信号通路 |
| **GWAS Catalog** (EBI) | 免费 | H6a 受体 SNP 位点 |
| **PGS Catalog** | 免费 | H6d PRS 构建 |
| **gnomAD** | 免费 | 人群变异频率 |
| **1000 Genomes** | 免费 | 祖先分群 |
| **Allen Ancient DNA Resource (AADR v54)** | 免费 | H6e 近 1 万年选择扫描 |
| **UK Biobank** | 独立申请（已 approved 2026-04-21 PI memo） | H6b GxE 主阵地 |
| **FinnGen R12** | 独立申请（已有） | H6b 多祖先 MR anchor |
| **BioBank Japan + MVP + AoU** | 独立申请 | H6d trans-ancestry PRS |

---

## 3. 对 Part 4 六条证据的具体改编

| 证据链 | 首选免费数据源 | CARSI 补充 | 增量说明 |
|---|---|---|---|
| **H6a 正选择扫描 (PAML branch-site)** | Ensembl + UniProt + PAML | CNGBdb 华大非模式基因组；Nature Ecol Evol / Curr Biol 全文 | +1-2 个 clade（Nematostella、Aplysia、中国本土兽类）支持 |
| **H6b GxE interaction** | UK Biobank + FinnGen + NHANES (已申请通过) | Nature Genetics / AJHG / Am J Epi 全文（SCIENCEDIRECT） | CARSI 支撑**文献综述**，不提供 raw 数据 |
| **H6c 收敛正选择 parallelism** | Ensembl Metazoa + NCBI orthologs | CNGBdb 中国本土物种（金丝猴、藏羚、藏狐、红嘴相思鸟等） | +3-5 个独立 lineage 做 receptor gain/loss footprint |
| **H6d PRS discriminant validity** | PGS Catalog + UKB + FinnGen + BBJ + MVP + AoU | Nature Genetics 全文 | 纯文献支撑 |
| **H6e recent selection scans** | AADR v54 + 1000 Genomes + gnomAD | Cell / Nature 全文 | 纯文献支撑 |
| **H6f cross-species manipulation lit summary** | PubMed | Nature/Nat Neurosci/Cell Rep/eLife 全文 | CARSI 几乎全覆盖 Kaun 2011, Johnson & Kenny 2010 等关键实验论文原文 |

---

## 4. 对立项决策的影响

**不改变 Part 4 可行性结论。** 所有必用开放数据 + UKBiobank + FinnGen 已具备；CARSI 的 CNGBdb 是**锦上添花**（增加中国本土物种基因组广度），不是关键路径。

**两条实际操作收益：**
1. **文献全文下载零摩擦。** Part 4 引用的 ~150 篇主要 paper 中预估 140+ 篇可通过 CARSI 直接下载 PDF，不需要走 Sci-Hub 或文献代办。
2. **CNGBdb 作为 H6c 扩展数据源值得试跑。** 若 3-5 个中国本土物种的 TAS1R / DRD / OPRM 正选择扫描能和 Ensembl 主干结果对齐，是一个**作者团队地理定位上的 advantage**（CQU 系+HUFLIT 系+华大社区是同一生态圈内的合理叙事）。

**不推荐的动作：**
- 放弃 UKBiobank 迁移到 CNGBdb — UKB 是 H6b GxE 主战场，不可替代。
- 放弃 Ensembl 用 CNGBdb — Ensembl 的 gene tree / ortholog / synteny 基础设施比 CNGBdb 更完整。
- 在 Part 4 主线叙事里强调 CNGBdb — 它是补充数据源，不是方法论创新。

---

## 5. 执行动作 checklist

- [x] CARSI 浙大账号可用性验证（12126023 / haoyuan666 登录成功）
- [x] CNGBdb 确认免费接入（学科：生物学/生态学/生物医学工程/生物工程等）
- [x] Nature / ScienceDirect / Cell Press / Wiley / Springer 全套文献权限确认
- [ ] Week 1 Pilot: 跑一次 CNGBdb 对 Nematostella DRD / OPRM 查询，验证数据质量
- [ ] Week 2: 用 CARSI→ScienceDirect 权限批量下载 Part 4 所需 ~150 篇 paper 的 PDF 到本地引用库
- [ ] Week 3: 评估是否把 CNGBdb 3-5 个中国本土物种纳入 H6c supplementary analysis

---

*Document version 1.0. 2026-04-24. Authored by PI during Scheme C execution.*
