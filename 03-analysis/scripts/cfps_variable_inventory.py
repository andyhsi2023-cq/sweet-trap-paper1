"""
CFPS 2010-2022 变量盘点：8 个 Sweet Trap 候选域
===============================================
Purpose:
    Read the CFPS unbalanced panel (86,294 obs × 204 cols), catalog every
    column by name/label/value distribution/year-coverage, and map each
    column to one or more of the 8 candidate Sweet Trap domains.

Input:
    /Volumes/P1/城市研究/CFPS2010-2022清洗好数据/
        2010-2022cfps非平衡面板数据(stata_推荐使用）.dta

Output:
    02-data/linkage/cfps_variable_catalog.csv       (204 rows metadata)
    00-design/cfps_variable_inventory.md            (main report)
    00-design/cfps_variable_heatmap.md              (domain x vartype matrix)

Compute discipline:
    - Read .dta ONCE into memory (86K x 204 fits in RAM).
    - No multiprocessing.
    - No regression; inventory only.
"""

import pandas as pd
import numpy as np
import pyreadstat
import os
import re
import json
from collections import defaultdict, OrderedDict

DATA_PATH = (
    "/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/"
    "2010-2022cfps非平衡面板数据(stata_推荐使用）.dta"
)
PROJECT_ROOT = "/Users/andy/Desktop/Research/sweet-trap-multidomain"
OUT_CATALOG = f"{PROJECT_ROOT}/02-data/linkage/cfps_variable_catalog.csv"
OUT_INVENTORY = f"{PROJECT_ROOT}/00-design/cfps_variable_inventory.md"
OUT_HEATMAP = f"{PROJECT_ROOT}/00-design/cfps_variable_heatmap.md"

os.makedirs(os.path.dirname(OUT_CATALOG), exist_ok=True)
os.makedirs(os.path.dirname(OUT_INVENTORY), exist_ok=True)


# ---------------------------------------------------------------
# 1. Load data with labels via pyreadstat
# ---------------------------------------------------------------
print("[1/6] Reading CFPS .dta (once)...", flush=True)
df, meta = pyreadstat.read_dta(DATA_PATH)
print(f"   Shape: {df.shape}")
print(f"   Columns: {len(meta.column_names)}")
print(f"   Years present (if 'year' exists): ", end="")
if "year" in df.columns:
    print(sorted(df["year"].dropna().unique().tolist()))
else:
    print("[no 'year' column]")


# ---------------------------------------------------------------
# 2. Domain keyword dictionaries
# ---------------------------------------------------------------
# Each domain has a list of regex patterns to match (lower-cased) against
# both the column name AND the column label (English chars + Chinese).
# A single column can match multiple domains.

DOMAIN_RULES = OrderedDict([
    ("D1_urban_overinvest", {
        "name_patterns": [
            r"life_?sat", r"happi", r"satisf", r"provcd", r"city",
            r"igmi", r"^urban$", r"^rural$",
        ],
        "label_patterns": [
            r"生活满意", r"幸福", r"城市", r"城镇", r"省", r"满意",
        ],
    }),
    ("D2_jiwa_education", {
        "name_patterns": [
            r"edu", r"school", r"tutor", r"learn", r"math", r"teach",
            r"child", r"kid", r"homework", r"pressure", r"anxiet",
            r"exam", r"score", r"grade", r"jiang", r"xue", r"rea?d",
            r"parent", r"juvenile", r"student",
        ],
        "label_patterns": [
            r"教育", r"学校", r"学习", r"作业", r"辅导", r"成绩", r"考试",
            r"焦虑", r"压力", r"孩子", r"子女", r"父母", r"亲子",
            r"培训", r"补课", r"升学", r"大学", r"小学", r"中学",
        ],
    }),
    ("D3_996_work", {
        "name_patterns": [
            r"work", r"hour", r"wage", r"salar", r"promot", r"job",
            r"overtime", r"labor", r"employ", r"income", r"occup",
            r"career", r"office",
        ],
        "label_patterns": [
            r"工作", r"工时", r"工资", r"收入", r"加班", r"晋升", r"职业",
            r"劳动", r"上班", r"雇佣", r"就业", r"单位",
        ],
    }),
    ("D4_marriage_bride_price", {
        "name_patterns": [
            r"marr", r"wed", r"caili", r"dowry", r"honey", r"engage",
            r"spouse", r"bride", r"groom", r"divorc", r"fiance",
        ],
        "label_patterns": [
            r"婚", r"结婚", r"彩礼", r"嫁妆", r"订婚", r"配偶",
            r"离婚", r"婚礼", r"聘礼",
        ],
    }),
    ("D5_diet_health", {
        "name_patterns": [
            r"diet", r"food", r"meat", r"sweet", r"bmi", r"weight",
            r"height", r"diabet", r"hypertens", r"blood", r"^eat",
            r"sugar", r"salt", r"fat", r"alcohol", r"smok", r"drink",
            r"veget", r"fruit", r"exercise", r"sport",
        ],
        "label_patterns": [
            r"饮食", r"食物", r"肉", r"甜", r"体重", r"身高", r"血压",
            r"血糖", r"糖尿", r"高血压", r"烟", r"酒", r"吸烟",
            r"饮酒", r"蔬菜", r"水果", r"锻炼", r"运动",
            r"慢性", r"疾病", r"健康",
        ],
    }),
    ("D6_bnpl_credit", {
        "name_patterns": [
            r"credit", r"card", r"install", r"loan", r"debt", r"borrow",
            r"fin_?stress", r"mortgage", r"repay",
        ],
        "label_patterns": [
            r"信用卡", r"分期", r"贷款", r"债", r"借款", r"负债",
            r"按揭", r"还款", r"财务压力",
        ],
    }),
    ("D7_social_media", {
        "name_patterns": [
            r"internet", r"online", r"social", r"weibo", r"wechat",
            r"douyin", r"qq", r"sleep", r"depress", r"ces_?d", r"cesd",
            r"mobile", r"phone", r"screen", r"tv", r"watch",
        ],
        "label_patterns": [
            r"网络", r"上网", r"互联网", r"社交", r"微博", r"微信",
            r"抖音", r"睡眠", r"抑郁", r"手机", r"电视",
        ],
    }),
    ("D8_luxury_house_car", {
        "name_patterns": [
            r"house", r"car", r"apart", r"mortgag", r"saving", r"asset",
            r"wealth", r"own", r"home", r"property", r"vehicle",
            r"housing",
        ],
        "label_patterns": [
            r"房", r"车", r"公寓", r"按揭", r"储蓄", r"资产",
            r"财富", r"住宅", r"住房", r"房产", r"汽车",
        ],
    }),
])

# Variable-role keywords (sub-classification inside a domain)
ROLE_HINTS = {
    "sweet_DV": [
        r"satisf", r"happi", r"life_?sat", r"joy", r"sense",
        r"满意", r"幸福", r"愉悦", r"高兴",
    ],
    "bitter_outcome": [
        r"depress", r"anxiet", r"stress", r"debt", r"bmi", r"chronic",
        r"diabet", r"hypertens", r"sleep", r"抑郁", r"焦虑", r"压力",
        r"负债", r"慢性", r"失眠", r"疾病",
    ],
    "lambda_proxy": [
        r"age", r"hukou", r"migr", r"province", r"provcd", r"educ",
        r"eduy", r"urban", r"rural", r"^sex$", r"female", r"gender",
        r"户口", r"迁移", r"流动", r"城乡", r"年龄",
    ],
    "covariate": [
        r"income", r"marital", r"married", r"eduy", r"year", r"pid",
        r"family", r"hhsize", r"famsize", r"region",
    ],
}


def match_any(text: str, patterns) -> bool:
    if text is None or (isinstance(text, float) and np.isnan(text)):
        return False
    t = str(text).lower()
    for p in patterns:
        if re.search(p, t):
            return True
    return False


# ---------------------------------------------------------------
# 3. Column-level metadata
# ---------------------------------------------------------------
print("[2/6] Building column metadata...", flush=True)

col_labels = meta.column_names_to_labels  # dict name -> label
col_types = dict(zip(meta.column_names, meta.readstat_variable_types))
value_labels_map = meta.variable_to_label  # name -> label-set name
value_label_dict = meta.value_labels  # label-set name -> {val: str}

N = len(df)
records = []

# Year coverage per column (non-missing)
has_year = "year" in df.columns
if has_year:
    year_vals = sorted([int(y) for y in df["year"].dropna().unique()])
else:
    year_vals = []

for col in df.columns:
    s = df[col]
    n_nonmiss = int(s.notna().sum())
    miss_rate = 1.0 - n_nonmiss / N
    label = col_labels.get(col, "") or ""
    dtype = str(s.dtype)

    # Year coverage: for which years is this column at least 10% non-missing?
    if has_year and n_nonmiss > 0:
        yr_cov = []
        for y in year_vals:
            mask = df["year"] == y
            nn = int(s[mask].notna().sum())
            tot = int(mask.sum())
            if tot > 0 and nn / tot >= 0.10:
                yr_cov.append(y)
        yr_cov_str = ",".join(str(y) for y in yr_cov)
    else:
        yr_cov_str = ""

    # Top-5 value counts (non-missing)
    try:
        if pd.api.types.is_numeric_dtype(s):
            vc = s.dropna().value_counts().head(5)
        else:
            vc = s.dropna().astype(str).value_counts().head(5)
        top5 = "; ".join(f"{k}:{v}" for k, v in vc.items())
    except Exception:
        top5 = ""

    # Basic stats if numeric
    if pd.api.types.is_numeric_dtype(s) and n_nonmiss > 0:
        s_nn = s.dropna()
        s_min = float(s_nn.min())
        s_max = float(s_nn.max())
        s_mean = float(s_nn.mean())
    else:
        s_min = s_max = s_mean = np.nan

    # Domain assignments
    domains = []
    for dom, rules in DOMAIN_RULES.items():
        if (match_any(col, rules["name_patterns"]) or
                match_any(label, rules["name_patterns"]) or
                match_any(label, rules["label_patterns"])):
            domains.append(dom)

    # Role assignments
    roles = []
    for role, pats in ROLE_HINTS.items():
        if match_any(col, pats) or match_any(label, pats):
            roles.append(role)

    records.append({
        "column": col,
        "label": label,
        "dtype": dtype,
        "n_nonmiss": n_nonmiss,
        "miss_rate": round(miss_rate, 4),
        "year_coverage": yr_cov_str,
        "min": s_min, "max": s_max, "mean": s_mean,
        "top5": top5,
        "domains": "|".join(domains) if domains else "",
        "roles": "|".join(roles) if roles else "",
    })

cat = pd.DataFrame(records)
cat.to_csv(OUT_CATALOG, index=False, encoding="utf-8-sig")
print(f"   wrote catalog -> {OUT_CATALOG}")
print(f"   Summary: {len(cat)} columns, {cat['domains'].str.len().gt(0).sum()} assigned to >=1 domain")


# ---------------------------------------------------------------
# 4. Per-domain tables
# ---------------------------------------------------------------
print("[3/6] Compiling per-domain tables...", flush=True)


def availability_stars(n_rows: int, year_span: int) -> str:
    """Rough rating based on N non-missing and year span."""
    if n_rows >= 30000 and year_span >= 4:
        return "***"
    if n_rows >= 10000 and year_span >= 3:
        return "**"
    if n_rows >= 3000:
        return "*"
    return "limited"


def year_span(yc: str) -> int:
    if not yc:
        return 0
    return len([y for y in yc.split(",") if y])


# ---------------------------------------------------------------
# 5. Generate inventory markdown
# ---------------------------------------------------------------
print("[4/6] Writing inventory.md...", flush=True)

DOMAIN_HUMAN = {
    "D1_urban_overinvest": ("域 1: 城市过度投资 (已做)",
                            "已覆盖。用于衔接 urban study 1。"),
    "D2_jiwa_education":   ("域 2: 鸡娃教育",
                            "家长教育投入 → 孩子心理/成绩 / 父母满意。"),
    "D3_996_work":         ("域 3: 996 工作",
                            "工时/加薪 → 健康/家庭满意。"),
    "D4_marriage_bride_price": ("域 4: 彩礼婚恋",
                                "婚礼/彩礼 → 家庭债务/婚后满意。"),
    "D5_diet_health":      ("域 5: 高糖高脂饮食",
                            "饮食偏好 → BMI/慢性病。"),
    "D6_bnpl_credit":      ("域 6: BNPL / 信用卡",
                            "信用消费 → 家庭负债/财务压力。"),
    "D7_social_media":     ("域 7: 短视频 / 社媒",
                            "上网时长 → 睡眠/抑郁/注意力。"),
    "D8_luxury_house_car": ("域 8: 高档房/车",
                            "购房/购车 → 房贷车贷/储蓄。"),
}

lines = []
lines.append("# CFPS 2010-2022 变量盘点：8 个 Sweet Trap 候选域\n")
lines.append(f"**生成时间**: 2026-04-17  \n")
lines.append(f"**数据源**: `{DATA_PATH}`  \n")
lines.append(f"**观测数 × 变量数**: {N:,} × {len(df.columns)}  \n")
lines.append(f"**年份覆盖**: {year_vals}\n\n")

lines.append("## 0. 总览\n")
dom_counts = {}
for dom in DOMAIN_RULES:
    cnt = cat["domains"].str.contains(dom, na=False).sum()
    dom_counts[dom] = int(cnt)
lines.append("| 域 | 命中列数 |\n|:---|---:|\n")
for dom, label_tuple in DOMAIN_HUMAN.items():
    lines.append(f"| {label_tuple[0]} | {dom_counts.get(dom,0)} |\n")
lines.append("\n")
lines.append("- 其中多域重叠允许（例如 `income` 同时作 D3 和协变量）。\n")
lines.append("- 以下按域展开。列 `roles` 标注 Sweet DV / Bitter outcome / λ proxy / covariate 的启发式归类。\n\n")

# Per-domain sections
for dom, (title, descr) in DOMAIN_HUMAN.items():
    lines.append(f"## {title}\n\n")
    lines.append(f"*{descr}*\n\n")
    sub = cat[cat["domains"].str.contains(dom, na=False)].copy()
    sub = sub.sort_values("n_nonmiss", ascending=False)
    if len(sub) == 0:
        lines.append("**未命中任何列**。建议：外部数据补充或此域剔除。\n\n")
        continue
    # Stats
    n_cols_in_dom = len(sub)
    max_nonmiss = int(sub["n_nonmiss"].max())
    # Availability rating = based on best column in domain
    top_row = sub.iloc[0]
    yr_span = year_span(top_row["year_coverage"])
    stars = availability_stars(int(top_row["n_nonmiss"]), yr_span)
    lines.append(f"**该域命中 {n_cols_in_dom} 列，最佳列非缺失 N = {max_nonmiss:,}，覆盖 {yr_span} 年 → 可用性 `{stars}`**\n\n")

    # Show up to top 25 columns
    show = sub.head(25)
    lines.append("| 列名 | label | N | 缺失率 | 年份覆盖 | 角色建议 |\n")
    lines.append("|:---|:---|---:|---:|:---|:---|\n")
    for _, r in show.iterrows():
        lab = (r["label"] or "").replace("|", "/").strip()[:60]
        roles = r["roles"] or "-"
        lines.append(
            f"| `{r['column']}` | {lab} | {r['n_nonmiss']:,} | "
            f"{r['miss_rate']:.1%} | {r['year_coverage'] or '-'} | {roles} |\n"
        )
    if len(sub) > 25:
        lines.append(f"\n*...另有 {len(sub)-25} 列见 catalog.csv。*\n")
    lines.append("\n")

# Recommendations section (filled in below after scoring)
lines.append("## 9. 域可用性综合评级与推荐 focal domains\n\n")
lines.append("评级规则：最佳变量非缺失 N ≥ 30K 且年份 ≥ 4 → `***`；N ≥ 10K 且年份 ≥ 3 → `**`；N ≥ 3K → `*`；否则 `limited`。\n\n")
lines.append("| 域 | 列数 | 最佳 N | 年份 | 评级 | 建议 |\n")
lines.append("|:---|---:|---:|---:|:---:|:---|\n")

summary_rows = []
for dom, (title, _) in DOMAIN_HUMAN.items():
    sub = cat[cat["domains"].str.contains(dom, na=False)]
    if len(sub) == 0:
        summary_rows.append((dom, title, 0, 0, 0, "limited", "剔除或补外部数据"))
        continue
    best = sub.sort_values("n_nonmiss", ascending=False).iloc[0]
    yr_span = year_span(best["year_coverage"])
    stars = availability_stars(int(best["n_nonmiss"]), yr_span)
    suggest = {
        "***": "强烈建议 focal domain",
        "**": "可作 focal domain",
        "*": "可作辅助/备选",
        "limited": "不建议；需补外部数据",
    }[stars]
    summary_rows.append((dom, title, len(sub), int(best["n_nonmiss"]), yr_span, stars, suggest))
    lines.append(f"| {title} | {len(sub)} | {best['n_nonmiss']:,} | {yr_span} | `{stars}` | {suggest} |\n")

lines.append("\n")

# Save
with open(OUT_INVENTORY, "w", encoding="utf-8") as f:
    f.writelines(lines)
print(f"   wrote inventory -> {OUT_INVENTORY}")


# ---------------------------------------------------------------
# 6. Heatmap: domain x role availability
# ---------------------------------------------------------------
print("[5/6] Writing heatmap.md...", flush=True)

heat_lines = []
heat_lines.append("# Sweet Trap 域 × 变量角色可用性热图\n\n")
heat_lines.append("行 = 域，列 = 角色。单元格 = 该域命中且角色匹配的列数 (该域 max N)。\n\n")

roles_order = ["sweet_DV", "bitter_outcome", "lambda_proxy", "covariate"]
heat_lines.append("| 域 | " + " | ".join(roles_order) + " |\n")
heat_lines.append("|:---|" + "|".join([":---:"] * len(roles_order)) + "|\n")

for dom, (title, _) in DOMAIN_HUMAN.items():
    row_cells = [title]
    sub = cat[cat["domains"].str.contains(dom, na=False)]
    for role in roles_order:
        sub_r = sub[sub["roles"].str.contains(role, na=False)]
        n_cols_r = len(sub_r)
        if n_cols_r == 0:
            row_cells.append("-")
        else:
            max_n = int(sub_r["n_nonmiss"].max())
            row_cells.append(f"{n_cols_r} cols / N≤{max_n:,}")
    heat_lines.append("| " + " | ".join(row_cells) + " |\n")

heat_lines.append("\n## 读图提示\n")
heat_lines.append("- `sweet_DV` 空 → 该域内找不到满足/happiness 指标，需借用全域 life_sat 并定义 domain-specific proxy。\n")
heat_lines.append("- `bitter_outcome` 空 → 该域 Bitter 长期后果无直接 CFPS 变量，须补外部/年度健康问卷。\n")
heat_lines.append("- `lambda_proxy` 几乎每域都有 (age/hukou/migration/income)，跨域复用。\n")

with open(OUT_HEATMAP, "w", encoding="utf-8") as f:
    f.writelines(heat_lines)
print(f"   wrote heatmap -> {OUT_HEATMAP}")


# ---------------------------------------------------------------
# 7. Print summary to stdout for hand-off
# ---------------------------------------------------------------
print("\n[6/6] === SUMMARY ===", flush=True)
print(f"Total columns: {len(df.columns)}")
print(f"Total obs: {len(df):,}")
print(f"Years: {year_vals}")
print()
print("Domain availability:")
for dom, title, ncols, best_n, yrs, stars, sug in summary_rows:
    print(f"  {stars:>8}  {title}: {ncols} cols, best N={best_n:,}, yrs={yrs}  -> {sug}")
print()
print("Output files:")
print(f"  - {OUT_CATALOG}")
print(f"  - {OUT_INVENTORY}")
print(f"  - {OUT_HEATMAP}")
