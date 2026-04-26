#!/usr/bin/env python
"""
positive_control_v4_summarize.py
================================

Pull null/alt lnLs from each v4 run's mlc files, compute LRT + p_half, write
per-run lrt_stats.tsv + master summary TSV to outputs/.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from scipy.stats import chi2

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
RUNS = ROOT / "data" / "codeml_runs"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)


def get_lnL(p: Path) -> float | None:
    if not p.exists():
        return None
    m = re.search(r"^lnL.*?(-\d+\.\d+)", p.read_text(), re.MULTILINE)
    return float(m.group(1)) if m else None


def parse_site_classes(mlc_path: Path) -> dict:
    """Parse 'MLEs of dN/dS (w) for site classes (K=4)' block."""
    if not mlc_path.exists():
        return {}
    text = mlc_path.read_text()
    m = re.search(
        r"MLEs of dN/dS.*?\n\s*site class\s+0\s+1\s+2a\s+2b\s*\n"
        r"\s*proportion\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\n"
        r"\s*background w\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\n"
        r"\s*foreground w\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)",
        text)
    if not m:
        return {}
    g = [float(x) for x in m.groups()]
    return {
        "p0": g[0], "p1": g[1], "p2a": g[2], "p2b": g[3],
        "bg_w0": g[4], "bg_w1": g[5], "bg_w2a": g[6], "bg_w2b": g[7],
        "fg_w0": g[8], "fg_w1": g[9], "fg_w2a": g[10], "fg_w2b": g[11],
    }


def main() -> int:
    v4_runs = sorted(d.name for d in RUNS.iterdir()
                     if d.is_dir() and d.name.startswith("TAS1R1_pc_v4__"))

    rows = []
    for name in v4_runs:
        d = RUNS / name
        lnL_null = get_lnL(d / "null_mlc.out")
        lnL_a05 = get_lnL(d / "alt_init05_mlc.out")
        lnL_a15 = get_lnL(d / "alt_init15_mlc.out")
        alts = [x for x in (lnL_a05, lnL_a15) if x is not None]
        if not alts or lnL_null is None:
            print(f"[skip] {name}: missing lnL")
            continue
        lnL_alt = max(alts)
        best_alt_mlc = (d / "alt_init05_mlc.out") if (lnL_a05 == lnL_alt) else (d / "alt_init15_mlc.out")

        LRT = max(2.0 * (lnL_alt - lnL_null), 0.0)
        p_full = 1.0 - chi2.cdf(LRT, df=1)
        p_half = p_full / 2.0

        sc = parse_site_classes(best_alt_mlc)
        rows.append({
            "run_id": name, "lnL_null": lnL_null,
            "lnL_alt05": lnL_a05, "lnL_alt15": lnL_a15, "lnL_alt_best": lnL_alt,
            "LRT": LRT, "p_full": p_full, "p_half": p_half,
            **sc,
        })

        # Per-run tsv
        with (d / "lrt_stats.tsv").open("w") as fh:
            fh.write("run_id\tlnL_null\tlnL_alt05\tlnL_alt15\tlnL_alt_best\tLRT\tp_full\tp_half\n")
            fh.write(f"{name}\t{lnL_null}\t{lnL_a05}\t{lnL_a15}\t{lnL_alt}\t{LRT}\t{p_full}\t{p_half}\n")

    # Master summary
    cols = ["run_id", "lnL_null", "lnL_alt05", "lnL_alt15", "lnL_alt_best",
            "LRT", "p_full", "p_half",
            "p0", "p1", "p2a", "p2b",
            "bg_w0", "bg_w1", "bg_w2a", "bg_w2b",
            "fg_w0", "fg_w1", "fg_w2a", "fg_w2b"]
    out = OUTPUTS / "positive_control_v4_lrt_summary.tsv"
    with out.open("w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")
    print(f"[write] {out}")

    # Pretty print
    print()
    print(f"{'Run':<45} {'LRT':>10} {'p_half':>12}  {'fg ω(2a)':>10}  {'p2a+p2b':>8}")
    for r in rows:
        p2 = (r.get("p2a", 0) or 0) + (r.get("p2b", 0) or 0)
        fg2a = r.get("fg_w2a", "")
        print(f"{r['run_id']:<45} {r['LRT']:>10.4f} {r['p_half']:>12.4g}  {fg2a:>10}  {p2:>8.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
