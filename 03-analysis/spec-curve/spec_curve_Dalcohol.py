"""
Spec-Curve: D_alcohol (CHARLS)
===============================

Purpose
-------
Harmonize + visualize the 360-spec spec-curve from D_alcohol main analysis.

Input
-----
02-data/processed/D_alcohol_speccurve.csv (from D_alcohol_sweet_trap.py)

Output
------
03-analysis/spec-curve/spec_curve_Dalcohol_results.csv
04-figures/supp/spec_curve_Dalcohol.png
03-analysis/spec-curve/spec_curve_Dalcohol_summary.json

Spec dims遍历:
  dv∈{satlife, srh, cesd10} × 3
  treatment∈{drinkl, drinkn_c, type_A, freq_moderate} × 4
  controls∈{minimal, baseline, full} × 3
  fe∈{within_person, cross_sectional} × 2
  sample∈{all, current_drinkers, age_lt65, age_ge55, men_only} × 5
  ≈ 360 (some dropped)

Focal family: dv=srh, treatment=drinkl (current drinker).
Expected sign: positive (drinkers report better SRH = sweet-side gain signal,
headline β = +0.118 at p < 1e-16).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _spec_curve_utils import (CASES, SPEC_DIR, FIG_SUPP, load_normalized,
                               filter_focal, summarize, plot_spec_curve)


def main():
    cfg = CASES["D_alcohol"]
    print(f"[D_alcohol] loading {cfg.csv_path.name}")
    df = load_normalized("D_alcohol")
    print(f"     {len(df)} total specs after loading")

    focal = filter_focal(df, cfg)
    df["is_focal"] = False
    df.loc[focal.index, "is_focal"] = True
    print(f"     {len(focal)} specs in focal family ({cfg.primary_dv} ~ drinkl*)")

    out_csv = SPEC_DIR / "spec_curve_Dalcohol_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"[D_alcohol] wrote {out_csv}")

    summary = summarize(focal, cfg)
    with open(SPEC_DIR / "spec_curve_Dalcohol_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[D_alcohol] summary: median β={summary['beta_median']:+.4f}  "
          f"sign-stab={summary['sign_stability']:.1%}  "
          f"sig-same={summary['sig_rate_same_sign']:.1%}  "
          f"fragile={summary['fragile']}")

    plot_spec_curve(focal, cfg, FIG_SUPP / "spec_curve_Dalcohol.png")


if __name__ == "__main__":
    main()
