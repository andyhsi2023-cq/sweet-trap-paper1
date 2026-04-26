"""
Build CHARLS C6 (保健品/养生执念) Sweet Trap panel.

Source variables:
  - Cleaned merged panel `charls.dta` (5 waves 2011-2020, 96,628 person-waves,
    175 harmonized variables incl. biomarkers/CES-D/cognition/srh/income).
  - Household-level supplement expenditure from raw waves:
      ge010_7 (2013, 2015, 2018) and gf013_7 (2020): Chinese questionnaire text
      "保健费用，包括健身锻炼及产品器械、保健品等" — Health-care expenditure
      INCLUDING 保健品 (health-products/supplements), fitness equipment, etc.
      English data label "Fitness/Health-Care Expenditure" understates the item:
      per 2020 questionnaire (GF013_7), it explicitly includes 保健品.
  - Individual-level self-purchased medicine: ef001_w4 + ef002_w4_1 (2018)
    monthly cost. Captures OTC drugs + "自己存的药" including TCM/保健.

Key point on variable granularity:
  - There is NO independent "保健品" line item in CHARLS: we get it bundled
    with fitness/health-care in a single annual expenditure.
  - Bundle is dominated by 保健品 for elderly (>=60) households: Chinese
    fitness participation at home is typically zero-cost (walking, dancing);
    the elderly households with >1000 Yuan/year in this bucket are almost
    certainly spending on 保健品/养生 products (empirical validation in the
    findings report — correlation with srh and independence from exercise).
  - We operationalize three candidate treatments:
       T1 = ge010_7 / gf013_7 (household supplement+fitness annual, Yuan)
       T2 = ef002_w4_1 (individual self-purchased med monthly, Yuan, 2018)
       T3 = ge010_6 / gf013_6 (medical exp annual) as comparator

Output: /Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/panel_C6_supplement.parquet
"""

# Author: Claude (Sweet Trap multidomain C6 analyst)
# Date: 2026-04-17
# Compute budget: single-process, no multiprocessing. Avoid re-reading P1 in loops.

import os
import zipfile
import json
import numpy as np
import pandas as pd
from pathlib import Path

PROJ = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
P1 = Path("/Volumes/P1/城市研究/01-个体调查/CHARLS_中老年_2011-2020/charls2011~2020清洗好+原版数据")
RAW = P1 / "原始数据+问卷2011~2020"
CLEAN = P1 / "整理完的-charls数据" / "charls.dta"
OUT = PROJ / "02-data" / "processed" / "panel_C6_supplement.parquet"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Scratch for extracting zipped raw waves (2013/2015)
SCRATCH = Path("/tmp/charls_c6_scratch")
SCRATCH.mkdir(exist_ok=True)


def extract_if_needed(zip_path: Path, target_file: str, out_dir: Path) -> Path:
    """Extract single file from CHARLS zip to scratch."""
    out_path = out_dir / target_file
    if out_path.exists():
        return out_path
    with zipfile.ZipFile(zip_path) as zf:
        zf.extract(target_file, out_dir)
    return out_path


def read_household_income(wave: str) -> pd.DataFrame:
    """Return wave-level HH dataframe with cols: householdID, sup_exp, med_exp, beauty_exp, wave."""
    if wave == "2013":
        zip_path = RAW / "2013" / "CHARLS2013_Dataset.zip"
        fp = extract_if_needed(zip_path, "Household_Income.dta", SCRATCH / "2013")
        cols = ["householdID", "ge010_7", "ge010_6", "ge010_8"]
        wnum = 2
    elif wave == "2015":
        zip_path = RAW / "2015" / "CHARLS2015r.zip"
        fp = extract_if_needed(zip_path, "Household_Income.dta", SCRATCH / "2015")
        cols = ["householdID", "ge010_7", "ge010_6", "ge010_8"]
        wnum = 3
    elif wave == "2018":
        fp = RAW / "2018" / "CHARLS2018r" / "Household_Income.dta"
        cols = ["householdID", "ge010_7", "ge010_6", "ge010_8"]
        wnum = 4
    elif wave == "2020":
        fp = RAW / "2020" / "CHARLS2020r" / "Household_Income.dta"
        cols = ["householdID", "gf013_7", "gf013_6", "gf013_8"]
        wnum = 5
    else:
        raise ValueError(wave)
    df = pd.read_stata(fp, columns=cols, convert_categoricals=False)
    df = df.rename(columns={cols[1]: "sup_exp", cols[2]: "med_exp_hh", cols[3]: "beauty_exp"})
    df["wave"] = wnum
    # 2020 uses -1 as refuse/unknown; treat as NaN. Also treat negatives as NaN.
    for c in ["sup_exp", "med_exp_hh", "beauty_exp"]:
        df.loc[df[c] < 0, c] = np.nan
    return df


def read_ef_medicine_2018() -> pd.DataFrame:
    """Individual-level 2018 self-purchased medicine cost."""
    fp = RAW / "2018" / "CHARLS2018r" / "Health_Care_and_Insurance.dta"
    df = pd.read_stata(
        fp,
        columns=["householdID", "communityID", "ef001_w4", "ef002_w4_1", "ef003_1"],
        convert_categoricals=False,
    )
    # Individual ID: Health_Care_and_Insurance doesn't carry ID key in 2018?
    # Re-inspect:
    return df


def main() -> None:
    print("[C6] Building CHARLS supplement panel...")

    # ---- 1. Cleaned merged panel (individual × wave) ----
    print("[C6] Reading cleaned merged panel...")
    panel = pd.read_stata(CLEAN, convert_categoricals=False)
    print(f"       n={len(panel):,}  vars={panel.shape[1]}  waves={sorted(panel['wave'].dropna().unique())}")
    # Keep only needed columns to stay memory-lean
    keep = [
        "ID", "householdID", "communityID", "wave", "iwy", "age", "gender",
        "marry", "rural", "srh", "adlab_c",
        # Diseases
        "hibpe", "diabe", "cancre", "lunge", "hearte", "stroke", "psyche",
        "arthre", "dyslipe", "livere", "kidneye", "digeste", "asthmae", "memrye",
        # Health spend
        "oophos1y", "tothos1y", "oopdoc1m", "totdoc1m",
        # Income / HH
        "income_total", "hhcperc", "family_size", "hchild",
        # Child-to-parent / Parent-to-child transfers
        "fcamt", "tcamt",
        # Biomarkers
        "bl_hbalc", "bl_glu", "bl_cho", "bl_ldl", "bl_hdl", "bl_tg", "bl_crp",
        "systo", "diasto", "pulse", "mheight", "mweight", "mwaist", "bmi",
        # Psychological
        "cesd10", "satlife", "hope",
        # Cognition
        "memeory", "executive", "total_cognition",
        # Insurance
        "ins", "pension", "ea001s1", "ea001s2", "ea001s3", "ea001s4", "ea001s5",
        "ea001s6", "ea001s11",
        # Disability/Social/Other
        "disability", "chronic", "exercise", "sleep",
        "fall_down", "hear", "teeth",
        # Education
        "edu", "province", "city",
        # Sample weight for blood
        "bloodweight",
    ]
    panel = panel[[c for c in keep if c in panel.columns]].copy()
    # Standardize srh (1=Excellent ... 5=Very Poor in CHARLS). Reverse to higher=better.
    # Check
    print("       srh value counts:", panel["srh"].value_counts(dropna=True).sort_index().head(10).to_dict())
    # Create srh_good: higher = better (1..5 -> 5..1). If coding is 1..5 with 1=best, reverse.
    panel["srh_good"] = 6 - panel["srh"]

    # ---- 2. Supplement/health-care household expenditure merge ----
    sup_frames = []
    for wave in ["2013", "2015", "2018", "2020"]:
        print(f"[C6] Reading Household_Income {wave}...")
        sup_frames.append(read_household_income(wave))
    sup_df = pd.concat(sup_frames, ignore_index=True)
    print(f"       HH supplement observations: {len(sup_df):,}")
    print("       sup_exp nonzero share:", (sup_df["sup_exp"] > 0).mean())
    print("       sup_exp quantiles:", sup_df["sup_exp"].quantile([.5, .9, .95, .99]).tolist())

    # Merge on householdID + wave
    panel = panel.merge(sup_df, on=["householdID", "wave"], how="left")
    print(f"       Post-merge n={len(panel):,}; sup_exp coverage in merge-relevant waves:")
    for w in [2, 3, 4, 5]:
        sub = panel[panel["wave"] == w]
        print(f"         wave {w}: n={len(sub)}, sup_exp obs={sub['sup_exp'].notna().sum()}")

    # ---- 3. Wave 1 has no supplement expenditure; keep but flag ----
    panel["has_sup_exp"] = panel["sup_exp"].notna()

    # ---- 4. Per-capita and log transforms ----
    panel["sup_exp_pc"] = panel["sup_exp"] / panel["family_size"].clip(lower=1)
    panel["sup_exp_pos"] = (panel["sup_exp"] > 0).astype("Int8")
    panel["sup_exp_heavy"] = (panel["sup_exp"] >= 1000).astype("Int8")  # >= 1000 Y/yr: heavy user flag
    panel["ln_sup_exp_p1"] = np.log1p(panel["sup_exp"].clip(lower=0))
    panel["ln_income_total"] = np.log1p(panel["income_total"].clip(lower=0))
    panel["ln_savings_proxy"] = np.log1p(panel["hhcperc"].clip(lower=0))

    # ---- 5. Age bins ----
    panel["age"] = pd.to_numeric(panel["age"], errors="coerce")
    panel["age_bin"] = pd.cut(panel["age"], bins=[0, 55, 60, 65, 70, 75, 80, 120],
                              labels=["<55", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"])
    panel["elderly"] = (panel["age"] >= 65).astype("Int8")
    panel["age_c"] = panel["age"] - 65

    # ---- 6. Cognition buckets ----
    # total_cognition 0..21; low = bottom quartile
    panel["cog_low"] = (panel["total_cognition"] <= panel["total_cognition"].quantile(0.25)).astype("Int8")

    # ---- 7. Output ----
    print(f"[C6] Writing panel to {OUT} ...")
    panel.to_parquet(OUT, index=False)
    # Report
    meta = {
        "n_rows": int(len(panel)),
        "n_individuals": int(panel["ID"].nunique()),
        "waves": sorted([int(w) for w in panel["wave"].dropna().unique()]),
        "variables": int(panel.shape[1]),
        "sup_exp_coverage_by_wave": {
            int(w): int(panel[panel["wave"] == w]["sup_exp"].notna().sum())
            for w in sorted(panel["wave"].dropna().unique())
        },
        "sup_exp_positive_share": float((panel["sup_exp"] > 0).mean()),
        "sup_exp_heavy_share": float((panel["sup_exp"] >= 1000).mean()),
        "sup_exp_quantiles_positive": (
            panel.loc[panel["sup_exp"] > 0, "sup_exp"].quantile([.25, .5, .75, .9, .95, .99]).to_dict()
        ),
        "biomarker_availability": {
            "bl_hbalc_obs": int(panel["bl_hbalc"].notna().sum()),
            "bl_glu_obs": int(panel["bl_glu"].notna().sum()),
            "bl_ldl_obs": int(panel["bl_ldl"].notna().sum()),
        },
    }
    meta_path = OUT.with_suffix(".meta.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2, default=str)
    print(f"[C6] Meta: {json.dumps(meta, indent=2, default=str)}")
    print(f"[C6] Done. Panel shape: {panel.shape}")


if __name__ == "__main__":
    main()
