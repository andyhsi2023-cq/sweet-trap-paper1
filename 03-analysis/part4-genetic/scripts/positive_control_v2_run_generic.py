#!/usr/bin/env python
"""
positive_control_v2_run_generic.py
==================================

Run codeml (null + alt x2 init omegas) on a user-supplied list of run directories.

Usage:
    python positive_control_v2_run_generic.py RUN_DIR1 RUN_DIR2 ...

If no arguments, runs all dirs starting with 'TAS1R1_pc_v2__'.

Bypasses the set -e bash wrapper (codeml exits non-zero after cosmetic warnings).
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
from pathlib import Path
from scipy.stats import chi2

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic")


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
               override_omega: float | None = None) -> float | None:
    work_ctl = run_dir / f".{log_name}.ctl"
    src = (run_dir / ctl_file).read_text()
    src = re.sub(r"outfile\s*=\s*\S+", f"outfile = {out_name}", src)
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
    mlc = run_dir / out_name
    lnL = extract_lnL(mlc)
    if lnL is None:
        print(f"[codeml FAIL] {run_dir.name}/{out_name}: no lnL (exit={proc.returncode})")
        return None
    print(f"[codeml OK]   {run_dir.name}/{out_name}: lnL = {lnL:.6f} (exit={proc.returncode})")
    try:
        work_ctl.unlink()
    except OSError:
        pass
    return lnL


def main() -> int:
    if len(sys.argv) >= 2:
        run_names = sys.argv[1:]
    else:
        runs_dir = ROOT / "data" / "codeml_runs"
        run_names = sorted(d.name for d in runs_dir.iterdir()
                           if d.is_dir() and (d.name.startswith("TAS1R1_pc_v2__") or
                                              d.name.startswith("TAS1R1_pc_v3__") or
                                              d.name.startswith("TAS1R1_pc_v4__")))

    run_dirs = [ROOT / "data" / "codeml_runs" / n for n in run_names]

    for rd in run_dirs:
        if not (rd / "null.ctl").exists() or not (rd / "alt.ctl").exists():
            print(f"[skip] {rd.name}: missing null.ctl or alt.ctl")
            continue

        print(f"\n====== {rd.name} ======")

        # Clear stale mlc outputs
        for name in ("null_mlc.out", "alt_init05_mlc.out", "alt_init15_mlc.out"):
            try:
                (rd / name).unlink()
            except FileNotFoundError:
                pass

        lnL_null = run_codeml(rd, "null.ctl", "null_mlc.out", "null")
        lnL_alt05 = run_codeml(rd, "alt.ctl", "alt_init05_mlc.out", "alt_init05",
                               override_omega=0.5)
        lnL_alt15 = run_codeml(rd, "alt.ctl", "alt_init15_mlc.out", "alt_init15",
                               override_omega=1.5)

        alts = [x for x in (lnL_alt05, lnL_alt15) if x is not None]
        lnL_alt = max(alts) if alts else None

        if lnL_null is None or lnL_alt is None:
            print(f"[summary] {rd.name}: SKIP (null or alt failed)")
            continue

        LRT = 2.0 * (lnL_alt - lnL_null)
        p_full = 1.0 - chi2.cdf(max(LRT, 0.0), df=1)
        p_half = p_full / 2.0
        with (rd / "lrt_stats.tsv").open("w") as fh:
            fh.write("run_id\tlnL_null\tlnL_alt05\tlnL_alt15\tlnL_alt_best\tLRT\tp_full\tp_half\n")
            fh.write(f"{rd.name}\t{lnL_null}\t{lnL_alt05}\t{lnL_alt15}\t{lnL_alt}\t{LRT}\t{p_full}\t{p_half}\n")
        print(f"[summary] {rd.name}: LRT={LRT:.4f}  p_full={p_full:.4g}  p_half={p_half:.4g}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
