"""Regenerate fig3_spec_curve_5panel.pdf from existing summaries + dataframes."""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from _spec_curve_utils import plot_5panel

SPEC_DIR = Path(__file__).parent
FIG_MAIN = Path(__file__).parents[2] / "04-figures" / "main"
FOCALS = ["C8", "C11", "C12", "C13", "Dalcohol"]
KEY_MAP = {"C8": "C8", "C11": "C11", "C12": "C12", "C13": "C13", "Dalcohol": "D_alcohol"}

summaries_broad = {}
dfs = {}
for focal in FOCALS:
    with open(SPEC_DIR / f"spec_curve_{focal}_summary.json") as f:
        d = json.load(f)
    key = KEY_MAP[focal]
    summaries_broad[key] = d.get("broad_focal", d)
    dfs[key] = pd.read_csv(SPEC_DIR / f"spec_curve_{focal}_results.csv")

for ext in ("png", "pdf"):
    out = FIG_MAIN / f"fig3_spec_curve_5panel.{ext}"
    plot_5panel(summaries_broad, dfs, out)
