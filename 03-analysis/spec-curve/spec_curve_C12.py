"""
Spec-Curve: C12 Short-Video / Digital (CFPS)
=============================================

Purpose
-------
Harmonize + visualize the 576-spec spec-curve from C12 main analysis.

Input
-----
02-data/processed/C12_speccurve.csv (from C12_shortvideo_sweet_trap.py)

Output
------
03-analysis/spec-curve/spec_curve_C12_results.csv
04-figures/supp/spec_curve_C12.png
03-analysis/spec-curve/spec_curve_C12_summary.json

Spec dims遍历:
  branch∈{sweet, bitter} × 2
  dv∈{qn12012, qn12016, dw, qq4010, health, qq201} × 6
  treatment∈{internet(_lag), digital_intensity(_lag), heavy_digital(_lag),
             onlineshopoping(_lag)} × 8
  controls∈{minimal, ses, ses+edu} × 3
  lag∈{0, 1} × 2
  sample∈{all, young_u30, mid_30_55, old_55p} × 4
  Total ≈ 576

Focal family: sweet branch, dv=qn12012 (life-sat), treatment contains "internet".
Expected sign: negative (digital exposure → lower life-sat).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _spec_curve_utils import (CASES, SPEC_DIR, FIG_SUPP, load_normalized,
                               filter_focal, summarize, plot_spec_curve)


def main():
    cfg = CASES["C12"]
    print(f"[C12] loading {cfg.csv_path.name}")
    df = load_normalized("C12")
    print(f"     {len(df)} total specs after loading")

    focal = filter_focal(df, cfg)
    df["is_focal"] = False
    df.loc[focal.index, "is_focal"] = True
    print(f"     {len(focal)} specs in focal family")

    out_csv = SPEC_DIR / "spec_curve_C12_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"[C12] wrote {out_csv}")

    summary = summarize(focal, cfg)
    with open(SPEC_DIR / "spec_curve_C12_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[C12] summary: median β={summary['beta_median']:+.4f}  "
          f"sign-stab={summary['sign_stability']:.1%}  "
          f"sig-same={summary['sig_rate_same_sign']:.1%}  "
          f"fragile={summary['fragile']}")

    plot_spec_curve(focal, cfg, FIG_SUPP / "spec_curve_C12.png")


if __name__ == "__main__":
    main()
