"""
Orchestrator: Run all 5 spec-curves and build composite figure.
================================================================

Usage
-----
python run_all_spec_curves.py

Produces
--------
- 03-analysis/spec-curve/spec_curve_<case>_results.csv  ×5
- 03-analysis/spec-curve/spec_curve_<case>_summary.json ×5
- 04-figures/supp/spec_curve_<case>.png                 ×5
- 04-figures/main/fig7_spec_curve_5panel.png            ×1
- 03-analysis/spec-curve/spec_curve_all_summary.csv      (cross-case)
"""
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _spec_curve_utils import (CASES, SPEC_DIR, FIG_MAIN, load_normalized,
                               filter_focal, filter_focal_narrow,
                               summarize, plot_spec_curve,
                               plot_5panel)


CASE_SLUGS = {"C8": "C8", "C11": "C11", "C12": "C12", "C13": "C13",
              "D_alcohol": "Dalcohol"}


def run_single(case: str):
    cfg = CASES[case]
    case_slug = CASE_SLUGS[case]
    print(f"\n===== {case} =====")
    df = load_normalized(case)
    print(f"  {len(df)} total specs")
    # Broad focal (for spec curve)
    focal = filter_focal(df, cfg)
    # Narrow focal (matches headline exactly)
    narrow = filter_focal_narrow(df, cfg)
    df["is_focal_broad"] = False
    df["is_focal_narrow"] = False
    df.loc[focal.index, "is_focal_broad"] = True
    df.loc[narrow.index, "is_focal_narrow"] = True
    print(f"  {len(focal)} broad-focal specs | {len(narrow)} narrow-focal specs")
    # Save harmonized (flat, annotated)
    df.to_csv(SPEC_DIR / f"spec_curve_{case_slug}_results.csv", index=False)
    # Summaries
    summary_broad = summarize(focal, cfg)
    summary_narrow = summarize(narrow, cfg)
    combined = {"broad_focal": summary_broad,
                "narrow_focal": summary_narrow}
    with open(SPEC_DIR / f"spec_curve_{case_slug}_summary.json", "w") as f:
        json.dump(combined, f, indent=2, default=str)
    print(f"  broad:  median β={summary_broad['beta_median']:+.4f}  "
          f"sign-stab={summary_broad['sign_stability']:.1%}  "
          f"sig-same={summary_broad['sig_rate_same_sign']:.1%}  "
          f"fragile={summary_broad['fragile']}")
    print(f"  narrow: median β={summary_narrow['beta_median']:+.4f}  "
          f"sign-stab={summary_narrow['sign_stability']:.1%}  "
          f"sig-same={summary_narrow['sig_rate_same_sign']:.1%}  "
          f"fragile={summary_narrow['fragile']}")
    # Plot (broad)
    from _spec_curve_utils import FIG_SUPP
    plot_spec_curve(focal, cfg,
                    FIG_SUPP / f"spec_curve_{case_slug}.png")
    return df, focal, narrow, summary_broad, summary_narrow


def main():
    dfs = {}
    focals = {}
    narrows = {}
    summaries_broad = {}
    summaries_narrow = {}
    for case in ["C8", "C11", "C12", "C13", "D_alcohol"]:
        df, focal, narrow, sb, sn = run_single(case)
        dfs[case] = df
        focals[case] = focal
        narrows[case] = narrow
        summaries_broad[case] = sb
        summaries_narrow[case] = sn

    # Composite 5-panel (use broad focal)
    out_png = FIG_MAIN / "fig7_spec_curve_5panel.png"
    plot_5panel(summaries_broad, focals, out_png)

    # Cross-case summary CSV (both broad and narrow)
    rows = []
    for case in ["C8", "C11", "C12", "C13", "D_alcohol"]:
        sb = summaries_broad[case]; sn = summaries_narrow[case]
        rows.append({
            "case": case,
            "n_broad": sb["n_specs"],
            "n_narrow": sn["n_specs"],
            "headline_beta": sb["headline_beta"],
            "median_beta_broad": sb["beta_median"],
            "median_ci_broad": f"[{sb['beta_median_ci_lo']:+.4f}, {sb['beta_median_ci_hi']:+.4f}]",
            "median_beta_narrow": sn["beta_median"],
            "median_ci_narrow": f"[{sn['beta_median_ci_lo']:+.4f}, {sn['beta_median_ci_hi']:+.4f}]",
            "sign_stab_broad": sb["sign_stability"],
            "sign_stab_narrow": sn["sign_stability"],
            "sig_same_broad": sb["sig_rate_same_sign"],
            "sig_same_narrow": sn["sig_rate_same_sign"],
            "fragile_broad": sb["fragile"],
            "fragile_narrow": sn["fragile"],
            "med_vs_head_broad": sb["median_vs_headline_ratio"],
            "med_vs_head_narrow": sn["median_vs_headline_ratio"],
        })
    cross_df = pd.DataFrame(rows)
    cross_df.to_csv(SPEC_DIR / "spec_curve_all_summary.csv", index=False)
    print("\n===== Cross-Case Summary =====")
    # Print condensed version
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    print(cross_df[["case", "n_broad", "n_narrow", "headline_beta",
                     "median_beta_broad", "median_beta_narrow",
                     "sign_stab_broad", "sign_stab_narrow",
                     "sig_same_broad", "sig_same_narrow",
                     "fragile_broad", "fragile_narrow"]].to_string(index=False))
    print(f"\nWrote cross-case summary -> {SPEC_DIR / 'spec_curve_all_summary.csv'}")


if __name__ == "__main__":
    main()
