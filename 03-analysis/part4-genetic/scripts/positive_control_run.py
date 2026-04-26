#!/usr/bin/env python
"""
positive_control_run.py
=======================

Run codeml null + alt (x2 init omega) for the two positive-control directories,
bypassing the set -e bash wrapper. Handles codeml's cosmetic nonzero exit
caused by "end of tree file" warnings.

Also:
- Reformats tree files with PAML-style "n_tax 1" header to silence the
  cosmetic EOF warning.
- Re-runs null if tree rewrite invalidates existing result (it shouldn't,
  the tree topology is identical).

Writes final lrt_stats.tsv to each run dir.
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
from pathlib import Path
from scipy.stats import chi2

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")
RUN_DIRS = [
    ROOT / "data" / "codeml_runs" / "TAS1R1_pc__hummingbird",
    ROOT / "data" / "codeml_runs" / "TAS1R1_pc__mouse_control",
]


def reformat_tree(run_dir: Path) -> None:
    """Prepend '6 1' to tree_labelled.nwk if not already done."""
    tp = run_dir / "tree_labelled.nwk"
    text = tp.read_text().strip()
    # Count tips for header
    # Re-read the single tree and count taxa
    import re as _re
    # tips = words not followed by a '(' and appearing before ':' or ','
    # Simplest: count opening '(' implies n_internal = k, n_tips = k+1
    n_tips = text.count(",") + 1  # standard for unrooted trifurcation at root / rooted
    header = f" {n_tips} 1\n"
    # Detect if already has header (e.g. starts with "6 1")
    first_line = text.splitlines()[0]
    if re.match(r"^\s*\d+\s+\d+\s*$", first_line):
        return  # already has header
    tp.write_text(header + text + "\n")
    print(f"[reformat] {tp} -> header '{header.strip()}' prepended")


def extract_lnL(mlc_path: Path) -> float | None:
    if not mlc_path.exists():
        return None
    pat = re.compile(r"^lnL.*?(-[0-9]+\.[0-9]+)")
    for line in mlc_path.read_text().splitlines():
        m = pat.match(line)
        if m:
            return float(m.group(1))
    return None


def run_codeml(run_dir: Path, ctl_file: str, out_name: str, log_name: str,
               override_omega: float | None = None) -> int:
    """Execute codeml in run_dir with a modified ctl file.

    Returns the codeml-reported lnL OR None if the run truly failed.
    Treats codeml exit codes as advisory (codeml prints 'error: end of tree file'
    but still produces valid output).
    """
    work_ctl = run_dir / f".{log_name}.ctl"
    src = (run_dir / ctl_file).read_text()
    # Repoint outfile
    src = re.sub(r"outfile\s*=\s*\S+", f"outfile = {out_name}", src)
    # Override init omega if requested
    if override_omega is not None:
        src = re.sub(r"omega\s*=\s*[0-9.]+", f"omega = {override_omega}", src, count=1)
    work_ctl.write_text(src)

    stdout_log = run_dir / f"{log_name}_stdout.log"
    print(f"[codeml] cd {run_dir.name}; codeml {work_ctl.name}  (omega init override={override_omega})")
    with stdout_log.open("w") as fh:
        proc = subprocess.run(
            ["codeml", work_ctl.name],
            cwd=str(run_dir),
            stdout=fh, stderr=subprocess.STDOUT,
        )
    # Ignore exit code. Check that out file exists and has lnL.
    mlc = run_dir / out_name
    lnL = extract_lnL(mlc)
    if lnL is None:
        print(f"[codeml FAIL] {run_dir.name}/{out_name}: no lnL extractable (exit={proc.returncode})")
        return None
    print(f"[codeml OK]   {run_dir.name}/{out_name}: lnL = {lnL:.6f} (exit={proc.returncode})")
    # cleanup work ctl
    try:
        work_ctl.unlink()
    except OSError:
        pass
    return lnL


def main() -> int:
    for rd in RUN_DIRS:
        reformat_tree(rd)

    summary = []
    for rd in RUN_DIRS:
        print(f"\n====== {rd.name} ======")

        # Re-run null to refresh with new tree header (fast; <30s)
        lnL_null = run_codeml(rd, "null.ctl", "null_mlc.out", "null")

        # Alt with omega init 0.5
        lnL_alt05 = run_codeml(rd, "alt.ctl", "alt_init05_mlc.out", "alt_init05",
                               override_omega=0.5)

        # Alt with omega init 1.5
        lnL_alt15 = run_codeml(rd, "alt.ctl", "alt_init15_mlc.out", "alt_init15",
                               override_omega=1.5)

        # Take best alt
        alts = [x for x in (lnL_alt05, lnL_alt15) if x is not None]
        lnL_alt = max(alts) if alts else None

        if lnL_null is None or lnL_alt is None:
            print(f"[summary] {rd.name}: null={lnL_null} alt_best={lnL_alt}  -> SKIP LRT")
            summary.append({"run_id": rd.name, "lnL_null": lnL_null,
                            "lnL_alt05": lnL_alt05, "lnL_alt15": lnL_alt15,
                            "lnL_alt_best": lnL_alt, "LRT": None,
                            "p_full_df1": None, "p_half_df1": None})
            continue

        LRT = 2.0 * (lnL_alt - lnL_null)
        p_full = 1.0 - chi2.cdf(max(LRT, 0.0), df=1)
        p_half = p_full / 2.0
        summary.append({
            "run_id": rd.name, "lnL_null": lnL_null,
            "lnL_alt05": lnL_alt05, "lnL_alt15": lnL_alt15,
            "lnL_alt_best": lnL_alt, "LRT": LRT,
            "p_full_df1": p_full, "p_half_df1": p_half,
        })
        with (rd / "lrt_stats.tsv").open("w") as fh:
            fh.write("run_id\tlnL_null\tlnL_alt05\tlnL_alt15\tlnL_alt_best\tLRT\tp_full\tp_half\n")
            fh.write(f"{rd.name}\t{lnL_null}\t{lnL_alt05}\t{lnL_alt15}\t{lnL_alt}\t{LRT}\t{p_full}\t{p_half}\n")
        print(f"[summary] {rd.name}: LRT={LRT:.4f}  p_full(df=1)={p_full:.4g}  p_half={p_half:.4g}")

    # Master summary
    out = ROOT / "outputs" / "positive_control_lrt_summary.tsv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as fh:
        fh.write("run_id\tlnL_null\tlnL_alt05\tlnL_alt15\tlnL_alt_best\tLRT\tp_full\tp_half\n")
        for row in summary:
            fh.write("\t".join(str(row.get(k, "")) for k in
                     ["run_id", "lnL_null", "lnL_alt05", "lnL_alt15", "lnL_alt_best",
                      "LRT", "p_full_df1", "p_half_df1"]) + "\n")
    print(f"\n[write] master summary -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
