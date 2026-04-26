"""
Spec-Curve: C8 Investment FOMO (CHFS)
======================================

Purpose
-------
Harmonize + visualize the 242-spec spec-curve from C8 main analysis.
Computes median β, sign stability, sig rate for the focal family
(life_sat ~ stock_hold variants).

Input
-----
02-data/processed/C8_speccurve.csv (from C8_investment_sweet_trap.py)
02-data/processed/C8_results.json  (headline)

Output
------
03-analysis/spec-curve/spec_curve_C8_results.csv  — harmonized, with "is_focal" flag
04-figures/supp/spec_curve_C8.png                 — figure
03-analysis/spec-curve/spec_curve_C8_summary.json — numeric summary

Notes
-----
Spec dims遍历 (main analysis 已跑过):
  dv∈{life_sat, risk_seek, fin_attention, ln_consump} × 4
  treatment∈{stock_hold, any_risky_hold, stock_share_assets} × 3
  controls∈{minimal, ses, full} × 3
  sample∈{all, high_income, rural, urban} × 4
  waves∈{pool_17_19, 2017_only} × 2
  ≈ 242 observed combinations (some dropped for collinearity/missing)

Focal family: dv=life_sat & treatment contains "stock".
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _spec_curve_utils import (CASES, CaseConfig, SPEC_DIR, FIG_SUPP,
                               load_normalized, filter_focal, summarize,
                               plot_spec_curve)


def main():
    cfg = CASES["C8"]
    print(f"[C8] loading {cfg.csv_path.name}")
    df = load_normalized("C8")
    print(f"     {len(df)} total specs after loading")

    # Focal family
    focal = filter_focal(df, cfg)
    df["is_focal"] = False
    df.loc[focal.index, "is_focal"] = True
    print(f"     {len(focal)} specs in focal family ({cfg.primary_dv} ~ {cfg.primary_treat}*)")

    # Save harmonized
    out_csv = SPEC_DIR / "spec_curve_C8_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"[C8] wrote {out_csv}")

    # Summary
    summary = summarize(focal, cfg)
    out_json = SPEC_DIR / "spec_curve_C8_summary.json"
    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[C8] summary: median β={summary['beta_median']:+.4f}  "
          f"sign-stab={summary['sign_stability']:.1%}  "
          f"sig-same={summary['sig_rate_same_sign']:.1%}  "
          f"fragile={summary['fragile']}")

    # Plot
    out_png = FIG_SUPP / "spec_curve_C8.png"
    plot_spec_curve(focal, cfg, out_png)


if __name__ == "__main__":
    main()
