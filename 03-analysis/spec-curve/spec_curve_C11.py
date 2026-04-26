"""
Spec-Curve: C11 Diet / Food Share (CHARLS)
===========================================

Purpose
-------
Harmonize + visualize the 672-spec spec-curve from C11 main analysis.

Input
-----
02-data/processed/C11_speccurve.csv (from C11_diet_sweet_trap.py)
02-data/processed/C11_results.json  (headline)

Output
------
03-analysis/spec-curve/spec_curve_C11_results.csv
04-figures/supp/spec_curve_C11.png
03-analysis/spec-curve/spec_curve_C11_summary.json

Spec dims遍历:
  branch∈{sweet, bitter} × 2
  dv∈{qn12012=life_sat, health, qp401, unhealth, ln_mexp} × 5
  treatment∈{d_food_share, food_share_valid, ln_food, d_ln_food, food_share_lag, ln_food_lag} × 6
  controls∈{minimal, demog, extended} × 3
  fe∈{person_year, person_year_province} × 2
  sample∈{all, urban, rural, age_25_60} × 4
  cluster∈{pid, provcd} × 2
  Total ≈ 672

Focal family: sweet branch, dv=qn12012, treatment contains "food_share".
Expected sign: negative (more food share → lower life-sat = sweet trap).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _spec_curve_utils import (CASES, SPEC_DIR, FIG_SUPP, load_normalized,
                               filter_focal, summarize, plot_spec_curve)


def main():
    cfg = CASES["C11"]
    print(f"[C11] loading {cfg.csv_path.name}")
    df = load_normalized("C11")
    print(f"     {len(df)} total specs after loading")

    focal = filter_focal(df, cfg)
    df["is_focal"] = False
    df.loc[focal.index, "is_focal"] = True
    print(f"     {len(focal)} specs in focal family "
          f"({cfg.primary_dv} ~ {cfg.primary_treat}* on sweet branch)")

    out_csv = SPEC_DIR / "spec_curve_C11_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"[C11] wrote {out_csv}")

    summary = summarize(focal, cfg)
    with open(SPEC_DIR / "spec_curve_C11_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[C11] summary: median β={summary['beta_median']:+.4f}  "
          f"sign-stab={summary['sign_stability']:.1%}  "
          f"sig-same={summary['sig_rate_same_sign']:.1%}  "
          f"fragile={summary['fragile']}")

    plot_spec_curve(focal, cfg, FIG_SUPP / "spec_curve_C11.png")


if __name__ == "__main__":
    main()
