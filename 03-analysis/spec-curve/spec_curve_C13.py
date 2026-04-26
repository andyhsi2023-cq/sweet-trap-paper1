"""
Spec-Curve: C13 Luxury Housing / Mortgage (CFPS)
=================================================

Purpose
-------
Harmonize + visualize the 1152-spec spec-curve from C13 main analysis.

Input
-----
02-data/processed/C13_speccurve.csv (from C13_housing_sweet_trap.py)

Output
------
03-analysis/spec-curve/spec_curve_C13_results.csv
04-figures/supp/spec_curve_C13.png
03-analysis/spec-curve/spec_curve_C13_summary.json

Spec dims遍历:
  branch∈{sweet, bitter} × 2
  dv∈{dw, qn12012, qn12016, ln_savings, ln_nonhousing_debts, ln_expense, child_num} × 7
  treatment∈{mortgage_burden_w, has_mortgage, ln_house_debts, ln_resivalue,
             mortgage_burden_lag, has_mortgage_lag, ln_house_debts_lag} × 7
  controls∈{minimal, demog, extended} × 3
  fe∈{person_year, person_year_province} × 2
  sample∈{all, urban, rural, young_lt40} × 4
  cluster∈{pid, provcd} × 2
  Total ≈ 1152

Focal family: sweet branch, dv=qn12012 (life-sat), treatment contains "mortgage_burden".
Expected sign: positive (mortgage burden = aspirational signal → higher reported life-sat sweet-side).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _spec_curve_utils import (CASES, SPEC_DIR, FIG_SUPP, load_normalized,
                               filter_focal, summarize, plot_spec_curve)


def main():
    cfg = CASES["C13"]
    print(f"[C13] loading {cfg.csv_path.name}")
    df = load_normalized("C13")
    print(f"     {len(df)} total specs after loading")

    focal = filter_focal(df, cfg)
    df["is_focal"] = False
    df.loc[focal.index, "is_focal"] = True
    print(f"     {len(focal)} specs in focal family")

    out_csv = SPEC_DIR / "spec_curve_C13_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"[C13] wrote {out_csv}")

    summary = summarize(focal, cfg)
    with open(SPEC_DIR / "spec_curve_C13_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[C13] summary: median β={summary['beta_median']:+.4f}  "
          f"sign-stab={summary['sign_stability']:.1%}  "
          f"sig-same={summary['sig_rate_same_sign']:.1%}  "
          f"fragile={summary['fragile']}")

    plot_spec_curve(focal, cfg, FIG_SUPP / "spec_curve_C13.png")


if __name__ == "__main__":
    main()
