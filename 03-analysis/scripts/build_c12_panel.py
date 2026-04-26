"""
Build C12 Short-Video / Algorithmic Recommendation Sweet Trap panel
====================================================================

Purpose
  Extract C12-specific variables from the CFPS 2010–2022 cleaned long panel
  (86,294 person-years × 204 cols) to build a slim analysis panel for the
  C12 short-video / digital-attention Sweet Trap PDE.

Data source (single file, no raw module access available on P1)
  /Volumes/P1/城市研究/CFPS2010-2022清洗好数据/
    2010-2022cfps非平衡面板数据(stata_推荐使用）.dta

Variable audit summary (see build log)
  Treatment candidates (C12 core):
    internet        — binary, 2010+2014-2022 (2012 missing)
    mobile          — binary "mobile internet", 2016-2022 only
    computer        — binary "computer internet", 2016-2022 only
    onlineshopoping — binary, 2014-2022
    digital_intensity = sum(internet, mobile, computer, onlineshopoping), 2016+
  NOTE: CFPS public-panel does NOT contain short-video hours, Douyin/Kuaishou
  variables, or daily screen-time. The cleaned panel offers only binary
  internet-use indicators. The analysis therefore operationalises C12 as the
  "digital-attention Sweet Trap" proxy bundle, with internet=primary, and
  explicitly documents this granularity ceiling in findings.md §1.

  Welfare outcomes:
    qn12012       life satisfaction (1-5)       2012+
    qn12016       future confidence (1-5)       2012+
    dw            self-rated social status      2010+
    health        self-rated health (1-5)       2010+
    qq4010        sleep hours/day               2014+   (KEY Bitter DV)
    qq201         smoked past month             2010+   (health-behaviour ctrl)

  Controls: age, gender, eduy, urban, rural, married, familysize,
            fincome1, total_asset (all present)

Output
  02-data/processed/panel_C12_shortvideo.parquet
  02-data/processed/panel_C12_shortvideo.meta.json  (SHA-256 + row/col counts)

Compute discipline
  - Read .dta once with pyreadstat (86k×204 fits easily).
  - No multiprocessing.
  - Read-only w.r.t. raw P1 file.
"""

import os
import json
import hashlib
from datetime import datetime

import numpy as np
import pandas as pd
import pyreadstat

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
RAW = (
    "/Volumes/P1/城市研究/CFPS2010-2022清洗好数据/"
    "2010-2022cfps非平衡面板数据(stata_推荐使用）.dta"
)
BASE = "/Users/andy/Desktop/Research/sweet-trap-multidomain"
OUT_PARQUET = os.path.join(BASE, "02-data/processed/panel_C12_shortvideo.parquet")
OUT_META = os.path.join(BASE, "02-data/processed/panel_C12_shortvideo.meta.json")
LOG = os.path.join(BASE, "03-analysis/scripts/build_c12_panel.log")


def log(msg):
    ts = datetime.utcnow().isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def main():
    open(LOG, "w").close()
    log("=== build_c12_panel.py START ===")

    log(f"Reading raw CFPS DTA: {RAW}")
    df, meta = pyreadstat.read_dta(RAW)
    log(f"  raw shape: {df.shape}")

    # ------------------------------------------------------------
    # Variable selection
    # ------------------------------------------------------------
    c12_cols = [
        # identifiers
        "pid", "year", "provcd", "city", "countyid",
        # C12 treatment indicators (all waves where present)
        "internet", "mobile", "computer", "onlineshopoping",
        # welfare DVs (Sweet + Bitter)
        "qn12012",   # life satisfaction
        "qn12016",   # future confidence
        "dw",        # social status
        "health",    # self-rated health
        "qq4010",    # sleep hours — KEY Bitter DV (screen-time > sleep-time hypothesis)
        "qq201",     # smoked past month (health behaviour ctrl)
        "qp401",     # chronic disease past 6 months
        # controls
        "age", "age2", "gender", "eduy", "urban", "rural",
        "marrige", "familysize", "communist", "minzu",
        # household SES
        "fincome1", "fincome1_per", "total_asset", "finance_asset",
        "savings", "debt_p", "limit", "expense", "pce",
        # consumption components (expenditure crowd-out test)
        "eec",       # 文教娱乐支出
        "travel",    # 旅游支出 (outdoor activity proxy)
        "eexp",      # 教育支出
        "trco",      # 交通通讯
        # work
        "workhour", "jobclass", "industry",
        # children (parenting externality proxy)
        "child_num", "elder_num",
        # geography
        "provname", "cityname",
    ]
    keep = [c for c in c12_cols if c in df.columns]
    log(f"  columns kept: {len(keep)}/{len(c12_cols)}")
    missing = set(c12_cols) - set(keep)
    if missing:
        log(f"  MISSING: {sorted(missing)}")

    panel = df[keep].copy()
    panel["year"] = panel["year"].astype(int)
    log(f"  panel shape: {panel.shape}")

    # ------------------------------------------------------------
    # Derived variables
    # ------------------------------------------------------------
    log("Building derived variables...")

    # Digital intensity = count of digital-engagement dummies (2016+)
    digital_cols = ["internet", "mobile", "computer", "onlineshopoping"]
    panel["digital_intensity"] = panel[digital_cols].sum(axis=1, min_count=1)
    # For 2016+ panel has all 4; 2014 has internet+onlineshopoping; pre-2014 only internet
    panel["digital_4_avail"] = panel[digital_cols].notna().all(axis=1).astype(int)
    panel["digital_intensity_z"] = np.nan
    # z within year for comparability
    for y in panel["year"].unique():
        mask = (panel["year"] == y) & panel["digital_intensity"].notna()
        if mask.sum() > 50:
            s = panel.loc[mask, "digital_intensity"]
            panel.loc[mask, "digital_intensity_z"] = (s - s.mean()) / s.std(ddof=0)

    # "Heavy digital user" = digital_intensity >= 3  (engage in 3+ digital channels)
    panel["heavy_digital"] = (panel["digital_intensity"] >= 3).astype("float")
    panel.loc[panel["digital_intensity"].isna(), "heavy_digital"] = np.nan

    # log transforms
    for (src, dst) in [
        ("fincome1", "ln_income"),
        ("total_asset", "ln_total_asset"),
        ("savings", "ln_savings"),
        ("expense", "ln_expense"),
        ("eec", "ln_eec"),
        ("travel", "ln_travel"),
    ]:
        if src in panel.columns:
            panel[dst] = np.log(panel[src].clip(lower=1))

    # married (1 = married, 0 otherwise; CFPS marrige==2 is married, per cleaning)
    if "marrige" in panel.columns:
        panel["married"] = (panel["marrige"] == 2).astype(int)

    # young cohort (< 30) for λ externalisation tests
    panel["young_u30"] = (panel["age"] < 30).astype("float")
    panel.loc[panel["age"].isna(), "young_u30"] = np.nan
    # student-age or working-age splits
    panel["age_group"] = pd.cut(
        panel["age"],
        [-1, 15, 25, 40, 60, 120],
        labels=["<=15", "16-25", "26-40", "41-60", ">60"],
    )

    # Post-Douyin era dummy (2019+ is post, 2018- is pre)
    # Douyin launched 2016-09, mass penetration ~2018-2019
    panel["post_douyin"] = (panel["year"] >= 2018).astype(int)
    panel["post_douyin_2020"] = (panel["year"] >= 2020).astype(int)

    # ρ lock-in: internet_lag
    panel = panel.sort_values(["pid", "year"])
    for v in ["internet", "mobile", "digital_intensity", "heavy_digital",
              "onlineshopoping", "computer"]:
        if v in panel.columns:
            panel[f"{v}_lag"] = panel.groupby("pid")[v].shift(1)

    # event indicator: first year with internet==1 per person
    panel["has_internet"] = (panel["internet"] == 1).astype("float")
    panel.loc[panel["internet"].isna(), "has_internet"] = np.nan
    first_internet = (
        panel[panel["has_internet"] == 1]
        .groupby("pid")["year"]
        .min()
        .rename("first_internet_year")
    )
    panel = panel.merge(first_internet, on="pid", how="left")
    panel["rel_internet_time"] = panel["year"] - panel["first_internet_year"]

    log(f"  final panel shape: {panel.shape}")

    # ------------------------------------------------------------
    # Coverage diagnostic
    # ------------------------------------------------------------
    log("Coverage by year:")
    cov_cols = ["internet", "mobile", "computer", "onlineshopoping",
                "digital_intensity", "qn12012", "qn12016", "dw",
                "qq4010", "qq201", "health"]
    cov_cols = [c for c in cov_cols if c in panel.columns]
    for y in sorted(panel["year"].unique()):
        sub = panel[panel["year"] == y]
        row = [f"y={int(y)} N={len(sub)}"]
        for c in cov_cols:
            row.append(f"{c}:{sub[c].notna().sum()}")
        log("  " + " | ".join(row))

    # ------------------------------------------------------------
    # Write parquet + meta
    # ------------------------------------------------------------
    # Drop category columns (cannot serialize cleanly to parquet without
    # schema fuss) — replace with string
    panel["age_group"] = panel["age_group"].astype("string")

    os.makedirs(os.path.dirname(OUT_PARQUET), exist_ok=True)
    panel.to_parquet(OUT_PARQUET, index=False)
    log(f"  wrote {OUT_PARQUET}")

    # SHA-256
    with open(OUT_PARQUET, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    log(f"  SHA-256: {sha}")

    meta = {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds"),
        "source_dta": RAW,
        "n_rows": int(panel.shape[0]),
        "n_cols": int(panel.shape[1]),
        "n_unique_pid": int(panel["pid"].nunique()),
        "waves": sorted(panel["year"].unique().tolist()),
        "sha256": sha,
        "notes": (
            "CFPS cleaned long panel — C12 slice. No raw short-video / "
            "screen-time variable available; analysis proceeds with "
            "internet/mobile/computer/onlineshopoping binary indicators "
            "and a composite digital_intensity score. Sleep hours qq4010 "
            "(2014+) is the key Bitter DV for screen-sleep crowd-out."
        ),
    }
    with open(OUT_META, "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    log(f"  wrote {OUT_META}")

    log("=== build_c12_panel.py END ===")


if __name__ == "__main__":
    main()
