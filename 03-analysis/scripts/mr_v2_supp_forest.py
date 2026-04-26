#!/usr/bin/env python3
"""
mr_v2_supp_forest.py
====================
Build supplementary MR forest figures from v2 outputs.

Two panels:
  A) Per-chain main IVW + MR-PRESSO corrected side-by-side (OR forest)
  B) Leave-one-out OR range per chain (showing LOO min/median/max as
     horizontal interval; confirms no single SNP drives result)

Input:
  02-data/processed/mr_results_all_chains_v2.csv
  02-data/processed/mr_loo_all_v2.csv

Output:
  04-figures/supp/mr_supp_forest.png
  04-figures/supp/mr_supp_funnel.png  (bonus: aggregate funnel)
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJ = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
OUT  = PROJ / "02-data/processed"
FIG  = PROJ / "04-figures/supp"; FIG.mkdir(parents=True, exist_ok=True)

res = pd.read_csv(OUT / "mr_results_all_chains_v2.csv")
loo = pd.read_csv(OUT / "mr_loo_all_v2.csv")
fun = pd.read_csv(OUT / "mr_funnel_data_v2.csv")

# Chain order (v1 first, then v2-new grouped by outcome family)
chain_order = ["1a","1b","1c","5","5b","6","6b",               # psychiatric
               "2b","2a","2c","7","7b","7c",                   # alcohol/liver
               "3c","3a","3a2","3b","3b2","3b3"]               # metabolic
chain_order = [c for c in chain_order if c in res["chain"].unique()]

# Panel A: IVW + PRESSO corrected per chain ---------------------------------
fig, axes = plt.subplots(1, 2, figsize=(11, 0.35*len(chain_order) + 2),
                          gridspec_kw=dict(width_ratios=[1.1, 1]))

ax = axes[0]
y = np.arange(len(chain_order))[::-1]
labels = []
for i, ch in enumerate(chain_order):
    sub = res[res["chain"] == ch]
    ivw = sub[sub["method"] == "IVW_random"].iloc[0] if len(sub[sub["method"]=="IVW_random"]) else None
    presso = sub[sub["method"] == "MR_PRESSO_corrected"].iloc[0] if len(sub[sub["method"]=="MR_PRESSO_corrected"]) else None
    if ivw is not None and not pd.isna(ivw["or_"]):
        ax.errorbar(ivw["or_"], y[i]+0.15,
                    xerr=[[max(ivw["or_"]-ivw["or_lo"],0)], [max(ivw["or_hi"]-ivw["or_"],0)]],
                    fmt="o", ms=6, color="#234d8c", ecolor="#234d8c",
                    capsize=3, lw=1.4, label="IVW" if i==0 else None)
    if presso is not None and not pd.isna(presso.get("or_", np.nan)):
        ax.errorbar(presso["or_"], y[i]-0.15,
                    xerr=[[max(presso["or_"]-presso["or_lo"],0)], [max(presso["or_hi"]-presso["or_"],0)]],
                    fmt="s", ms=5, color="#b14436", ecolor="#b14436",
                    capsize=3, lw=1.2, label="MR-PRESSO (outliers removed)" if i==0 else None)
    label_base = f"{ch}: {ivw['exposure'][:14] if ivw is not None else ''} → {ivw['outcome'][:16] if ivw is not None else ''}"
    labels.append(label_base)
ax.axvline(1, color="k", lw=0.6, ls="--", alpha=0.7)
ax.set_xscale("log")
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel("OR [95% CI] per 1-SD increase in exposure")
ax.set_title("Panel A  |  IVW vs MR-PRESSO (outlier-corrected)")
ax.legend(loc="lower right", fontsize=8, frameon=False)
ax.grid(True, axis="x", alpha=0.2)

# Panel B: LOO range per chain ---------------------------------------------
ax = axes[1]
for i, ch in enumerate(chain_order):
    g = loo[loo["chain"] == ch]
    if len(g) == 0: continue
    or_vals = g["or_"].dropna().values
    if len(or_vals) == 0: continue
    lo, med, hi = np.min(or_vals), np.median(or_vals), np.max(or_vals)
    # IVW main estimate for reference
    sub = res[(res["chain"] == ch) & (res["method"] == "IVW_random")]
    or_main = sub["or_"].iloc[0] if len(sub) else np.nan
    ax.plot([lo, hi], [y[i], y[i]], color="#666", lw=1.6)
    ax.plot(med, y[i], "D", ms=4, color="#234d8c")
    ax.plot(or_main, y[i], "|", ms=18, mew=2, color="#b14436")
ax.axvline(1, color="k", lw=0.6, ls="--", alpha=0.7)
ax.set_xscale("log")
ax.set_yticks(y); ax.set_yticklabels([])
ax.set_xlabel("Leave-one-out OR range (min – max)")
ax.set_title("Panel B  |  LOO OR range (diamond = LOO median; red tick = full IVW)")
ax.grid(True, axis="x", alpha=0.2)

plt.tight_layout()
out_png = FIG / "mr_supp_forest.png"
plt.savefig(out_png, dpi=180, bbox_inches="tight")
plt.close()
print(f"wrote {out_png}")

# Bonus: funnel plot, one multi-panel figure ------------------------------
chains_with_data = [c for c in chain_order if c in fun["chain"].unique()]
ncol = 4
nrow = int(np.ceil(len(chains_with_data)/ncol))
fig, axs = plt.subplots(nrow, ncol, figsize=(ncol*3.2, nrow*2.6), squeeze=False)
for idx, ch in enumerate(chains_with_data):
    ax = axs[idx//ncol, idx%ncol]
    g = fun[fun["chain"] == ch]
    # drop extreme outliers for visual clarity (|wald|>3)
    gv = g[np.abs(g["wald"]) < 3].dropna(subset=["wald","precision"])
    ax.scatter(gv["wald"], gv["precision"], s=10, alpha=0.6, color="#234d8c", edgecolor="none")
    # reference line at IVW estimate
    sub = res[(res["chain"]==ch) & (res["method"]=="IVW_random")]
    if len(sub):
        ax.axvline(sub["beta"].iloc[0], color="#b14436", ls="--", lw=0.9)
    ax.axvline(0, color="k", lw=0.4, alpha=0.5)
    ax.set_title(f"{ch}: {sub['exposure'].iloc[0][:12] if len(sub) else ''} → {sub['outcome'].iloc[0][:12] if len(sub) else ''}",
                 fontsize=8)
    ax.set_xlabel("Wald ratio (log OR / unit)", fontsize=7)
    ax.set_ylabel("1 / SE(Wald)", fontsize=7)
    ax.tick_params(labelsize=7)
# hide unused cells
for idx in range(len(chains_with_data), nrow*ncol):
    axs[idx//ncol, idx%ncol].axis("off")
plt.suptitle("Supplementary funnel plots — per-chain Wald-ratio asymmetry check", y=1.001, fontsize=10)
plt.tight_layout()
out_png2 = FIG / "mr_supp_funnel.png"
plt.savefig(out_png2, dpi=160, bbox_inches="tight")
plt.close()
print(f"wrote {out_png2}")
