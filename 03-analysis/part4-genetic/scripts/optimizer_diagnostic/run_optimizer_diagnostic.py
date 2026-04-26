#!/usr/bin/env python3
"""
run_optimizer_diagnostic.py

Purpose
-------
Yang & dos Reis (2011) optimiser-boundary diagnostic for branch-site Model A
alternative-model runs. The C-path manuscript (sweet-trap-multidomain §3.4)
reports 5 of 6 production clades returning LRT = 0.000 exactly. This is
consistent with EITHER (a) a genuine biological null OR (b) codeml getting
stuck at the omega_2a = 1.0 boundary regardless of starting omega.

Diagnostic procedure (per clade)
--------------------------------
1. Build sibling subdirs alt_w0_<X>/ under each existing alt run dir, copy
   alignment.phy + tree_labelled.nwk, and edit a copy of alt.ctl to set the
   initial `omega = X` while keeping fix_omega=0, model=2, NSsites=2.
2. Run codeml in each subdir (single-threaded; concurrency limited to
   n_workers=2 per CLAUDE.md compute rules).
3. Reuse the production null lnL (already computed, fix_omega=1 omega=1).
4. Compute LRT = 2 * (lnL_alt - lnL_null) for each starting omega.
5. Verdict per clade:
     TRUE NULL          -> all 5 LRT <= 0.01 AND all foreground omega_2a == 1.0
     OPTIMIZER ARTIFACT -> any LRT > 1.0 AND foreground omega_2a > 1.0
     MIXED              -> some escape but all LRT < 2.71 (no df=1 chi2 sig)

Starting omegas tested: {0.1, 0.5, 1.0, 2.0, 5.0}
- omega=0.5 is reused from the existing alt_init05_mlc.out (production run).
- Four NEW codeml runs per clade for omega in {0.1, 1.0, 2.0, 5.0}.
- 5 clades x 4 new starts = 20 codeml jobs. Each ~50-70 min.
  Wall-time at n_workers=2: ~10 hours.

Inputs
------
- /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/data/codeml_runs/<run>/alignment.phy
- /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/data/codeml_runs/<run>/tree_labelled.nwk
- /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/data/codeml_runs/<run>/alt.ctl   (template)
- /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/data/codeml_runs/<run>/null_mlc.out (lnL_null reused)
- /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/data/codeml_runs/<run>/alt_init05_mlc.out (omega0=0.5 reused)

Outputs
-------
- /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/data/codeml_runs/<run>/alt_w0_<X>/alt_mlc.out
- /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/outputs/optimizer_diagnostic.csv
- /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/outputs/optimizer_diagnostic_report.md

Compute discipline
------------------
- n_workers = 2 strictly (CLAUDE.md M5 Pro rule)
- codeml is single-threaded; we parallelise across (clade, omega0) pairs
- Each worker spawns one codeml subprocess and waits

Usage
-----
    source /Users/andy/Desktop/Research/sweet-trap-multidomain/tools/activate_env.sh
    python /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/scripts/optimizer_diagnostic/run_optimizer_diagnostic.py

Author : data-analyst agent
Date   : 2026-04-25
"""
from __future__ import annotations

import concurrent.futures as cf
import logging
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import pandas as pd

# ---- Configuration -----------------------------------------------------------

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
PART4 = ROOT / "03-analysis" / "part4-genetic"
RUNS_DIR = PART4 / "data" / "codeml_runs"
OUTPUTS = PART4 / "outputs"
LOG_DIR = PART4 / "logs" / "optimizer_diagnostic"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 5 LRT=0 production clades to diagnose (manuscript §3.4 "5 of 6")
CLADES = [
    "Gr_sweet__dmel_Gr64_cluster",
    "Gr_sweet__dmel_all_clade",
    "Gr_sweet__coleoptera_clade",
    "Gr_sweet__lepidoptera_clade",
    "Gr_sweet__aaegypti_clade",
]

# 5 starting omega values per Yang & dos Reis (2011) recommendation
OMEGA_STARTS = [0.1, 0.5, 1.0, 2.0, 5.0]

# omega=0.5 is already done in production (alt_init05_mlc.out) — REUSE, do not rerun.
OMEGA_REUSE = {0.5: "alt_init05_mlc.out"}

N_WORKERS = 2  # CLAUDE.md compute rule

LOG_FILE = LOG_DIR / f"orchestrator_{time.strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

# ---- Helpers -----------------------------------------------------------------

LNL_RE = re.compile(r"^lnL.*?(-\d+\.\d+)", re.M)
FG_W_RE = re.compile(r"foreground w\s+[0-9.]+\s+[0-9.]+\s+([0-9.]+)")
PROP_RE = re.compile(r"proportion\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)")


def parse_lnL(mlc_path: Path) -> Optional[float]:
    if not mlc_path.exists():
        return None
    txt = mlc_path.read_text()
    m = LNL_RE.search(txt)
    return float(m.group(1)) if m else None


def parse_fg_omega_2a(mlc_path: Path) -> Optional[float]:
    if not mlc_path.exists():
        return None
    txt = mlc_path.read_text()
    m = FG_W_RE.search(txt)
    return float(m.group(1)) if m else None


def parse_proportion_2a_2b(mlc_path: Path) -> Optional[float]:
    if not mlc_path.exists():
        return None
    txt = mlc_path.read_text()
    m = PROP_RE.search(txt)
    if not m:
        return None
    return float(m.group(3)) + float(m.group(4))


def edit_omega_in_ctl(ctl_path: Path, new_omega: float) -> None:
    """Replace `omega = X` line in ctl with new value; also repoint outfile."""
    src = ctl_path.read_text().splitlines()
    out = []
    for line in src:
        s = line.split("*", 1)[0].strip()
        if s.lower().startswith("omega "):
            out.append(f"        omega = {new_omega}     * diagnostic init omega")
        elif s.lower().startswith("outfile "):
            out.append(f"      outfile = alt_mlc.out")
        else:
            out.append(line)
    ctl_path.write_text("\n".join(out) + "\n")


def setup_subdir(clade: str, omega0: float) -> Path:
    """Create alt_w0_<X>/ subdir, copy inputs + ctl, edit ctl. Return subdir path."""
    src = RUNS_DIR / clade
    sub = src / f"alt_w0_{omega0}"
    sub.mkdir(exist_ok=True)
    # Copy alignment + tree (small files; keep verbatim)
    for fn in ("alignment.phy", "tree_labelled.nwk"):
        if not (sub / fn).exists():
            shutil.copy(src / fn, sub / fn)
    # Copy alt.ctl as alt.ctl, then edit omega
    ctl_dst = sub / "alt.ctl"
    shutil.copy(src / "alt.ctl", ctl_dst)
    edit_omega_in_ctl(ctl_dst, omega0)
    return sub


def run_codeml(sub: Path, clade: str, omega0: float, timeout_s: int = 7200) -> dict:
    """Run codeml in `sub`. Return dict with parsed results.

    Note: codeml exits non-zero after a cosmetic 'end of tree file' warning
    even on success (see 02_run_branch_site.sh). Use lnL presence in mlc as
    success criterion.
    """
    mlc = sub / "alt_mlc.out"
    stdout_log = sub / "codeml_stdout.log"
    label = f"{clade}__w0_{omega0}"
    t0 = time.time()
    log.info(f"START {label} -> {sub}")
    try:
        with stdout_log.open("w") as fh:
            subprocess.run(
                ["codeml", "alt.ctl"],
                cwd=sub,
                stdout=fh,
                stderr=subprocess.STDOUT,
                timeout=timeout_s,
                check=False,
            )
    except subprocess.TimeoutExpired:
        log.error(f"TIMEOUT {label} after {timeout_s}s")
        return {"clade": clade, "omega_start": omega0, "lnL_alt": None,
                "omega_2a": None, "p2a_p2b": None, "status": "timeout",
                "wall_seconds": timeout_s}
    dt = time.time() - t0
    lnL = parse_lnL(mlc)
    if lnL is None:
        log.error(f"FAIL  {label} no lnL after {dt:.0f}s")
        return {"clade": clade, "omega_start": omega0, "lnL_alt": None,
                "omega_2a": None, "p2a_p2b": None, "status": "no_lnL",
                "wall_seconds": int(dt)}
    fg_w = parse_fg_omega_2a(mlc)
    p2ab = parse_proportion_2a_2b(mlc)
    log.info(f"DONE  {label} lnL={lnL} fg_w_2a={fg_w} dt={dt:.0f}s")
    return {"clade": clade, "omega_start": omega0, "lnL_alt": lnL,
            "omega_2a": fg_w, "p2a_p2b": p2ab, "status": "ok",
            "wall_seconds": int(dt)}


def collect_reuse(clade: str, omega0: float) -> dict:
    """For omega0 values already covered by a production run, parse that mlc."""
    src = RUNS_DIR / clade
    fn = OMEGA_REUSE[omega0]
    mlc = src / fn
    lnL = parse_lnL(mlc)
    fg_w = parse_fg_omega_2a(mlc)
    p2ab = parse_proportion_2a_2b(mlc)
    log.info(f"REUSE {clade}__w0_{omega0} from {fn} lnL={lnL} fg_w_2a={fg_w}")
    return {"clade": clade, "omega_start": omega0, "lnL_alt": lnL,
            "omega_2a": fg_w, "p2a_p2b": p2ab, "status": "reused",
            "wall_seconds": 0}


def get_lnL_null(clade: str) -> float:
    """Production null lnL (fix_omega=1, omega=1) — reused as denominator."""
    mlc = RUNS_DIR / clade / "null_mlc.out"
    v = parse_lnL(mlc)
    if v is None:
        raise RuntimeError(f"Missing null_mlc.out lnL for {clade}: {mlc}")
    return v


def verdict_for_clade(rows: pd.DataFrame) -> str:
    """Apply Yang & dos Reis (2011) decision rule per clade."""
    lrts = rows["LRT"].values
    fg_ws = rows["omega_2a"].values
    if all(lrt <= 0.01 for lrt in lrts) and all(abs(w - 1.0) < 0.001 for w in fg_ws):
        return "TRUE_NULL"
    if any(lrt > 1.0 and w > 1.0 for lrt, w in zip(lrts, fg_ws)):
        return "OPTIMIZER_ARTIFACT"
    return "MIXED"


# ---- Main --------------------------------------------------------------------

def main():
    log.info(f"Optimizer-boundary diagnostic starting. Log: {LOG_FILE}")
    log.info(f"Clades to diagnose: {len(CLADES)}; Omega starts: {OMEGA_STARTS}")

    # 1. Build the to-run task list (skip omega=0.5; reused from production)
    tasks_to_run = []   # list of (clade, omega0, subdir)
    for clade in CLADES:
        # sanity: does this clade run dir exist with all required inputs?
        run_dir = RUNS_DIR / clade
        for must in ("alignment.phy", "tree_labelled.nwk", "alt.ctl", "null_mlc.out", "alt_init05_mlc.out"):
            if not (run_dir / must).exists():
                raise FileNotFoundError(f"Missing {must} in {run_dir}")
        for w0 in OMEGA_STARTS:
            if w0 in OMEGA_REUSE:
                continue
            sub = setup_subdir(clade, w0)
            tasks_to_run.append((clade, w0, sub))
    log.info(f"Will run {len(tasks_to_run)} new codeml jobs (omega=0.5 reused).")

    # 2. Run with n_workers=2
    results = []
    completed = 0
    total = len(tasks_to_run)
    with cf.ThreadPoolExecutor(max_workers=N_WORKERS) as ex:
        future_map = {ex.submit(run_codeml, sub, clade, w0): (clade, w0)
                      for (clade, w0, sub) in tasks_to_run}
        for fut in cf.as_completed(future_map):
            clade, w0 = future_map[fut]
            try:
                r = fut.result()
            except Exception as e:
                log.error(f"EXCEPTION {clade}__w0_{w0}: {e}")
                r = {"clade": clade, "omega_start": w0, "lnL_alt": None,
                     "omega_2a": None, "p2a_p2b": None, "status": f"exception:{e}",
                     "wall_seconds": 0}
            results.append(r)
            completed += 1
            log.info(f"PROGRESS {completed}/{total}")
            # Save intermediate CSV after every completion (resilience)
            _save_intermediate(results)

    # 3. Add reused omega=0.5 rows
    for clade in CLADES:
        for w0 in OMEGA_REUSE:
            results.append(collect_reuse(clade, w0))

    # 4. Build full DataFrame: 25 rows
    df = pd.DataFrame(results)
    df = df.sort_values(["clade", "omega_start"]).reset_index(drop=True)

    # Add lnL_null and LRT
    null_lookup = {clade: get_lnL_null(clade) for clade in CLADES}
    df["lnL_null"] = df["clade"].map(null_lookup)
    df["LRT"] = 2 * (df["lnL_alt"] - df["lnL_null"])

    # Per-row verdict tag (boundary vs escaped)
    df["row_flag"] = df.apply(
        lambda r: "boundary" if (
            pd.notna(r["LRT"]) and r["LRT"] <= 0.01 and pd.notna(r["omega_2a"]) and abs(r["omega_2a"] - 1.0) < 0.001
        ) else ("escaped" if pd.notna(r["LRT"]) and r["LRT"] > 0.01 else "fail"),
        axis=1,
    )

    # 5. Per-clade verdict
    clade_verdicts = {}
    for clade in CLADES:
        sub = df[df["clade"] == clade]
        clade_verdicts[clade] = verdict_for_clade(sub)
    df["verdict"] = df["clade"].map(clade_verdicts)

    # 6. Write outputs
    out_csv = OUTPUTS / "optimizer_diagnostic.csv"
    df_out = df[["clade", "omega_start", "lnL_alt", "lnL_null", "LRT",
                 "omega_2a", "p2a_p2b", "row_flag", "status", "wall_seconds",
                 "verdict"]]
    df_out.to_csv(out_csv, index=False)
    log.info(f"WROTE {out_csv} ({len(df_out)} rows)")

    # 7. Per-clade markdown report
    report_lines = []
    report_lines.append("# Optimizer-boundary diagnostic — branch-site Model A alt")
    report_lines.append("")
    report_lines.append(
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}  •  "
        f"5 clades × 5 starting omegas (Yang & dos Reis 2011)."
    )
    report_lines.append("")
    report_lines.append(
        "**Rule**: TRUE_NULL = all 5 LRT ≤ 0.01 AND all foreground ω_2a = 1.0;  "
        "OPTIMIZER_ARTIFACT = any LRT > 1.0 with ω_2a > 1.0;  "
        "MIXED = partial escapes but all LRT < 2.71 (no df=1 χ² sig)."
    )
    report_lines.append("")
    report_lines.append("## Per-clade verdicts")
    report_lines.append("")
    for clade in CLADES:
        sub = df[df["clade"] == clade].sort_values("omega_start")
        v = clade_verdicts[clade]
        report_lines.append(f"### {clade}")
        report_lines.append(f"- **Verdict**: {v}")
        report_lines.append(f"- lnL_null (production): {null_lookup[clade]:.6f}")
        report_lines.append("")
        report_lines.append("| ω₀ start | lnL_alt | LRT | ω_2a | flag | status |")
        report_lines.append("|----------|---------|-----|------|------|--------|")
        for _, r in sub.iterrows():
            lna = f"{r['lnL_alt']:.6f}" if pd.notna(r["lnL_alt"]) else "NA"
            lrt = f"{r['LRT']:.6f}" if pd.notna(r["LRT"]) else "NA"
            w2a = f"{r['omega_2a']:.4f}" if pd.notna(r["omega_2a"]) else "NA"
            report_lines.append(
                f"| {r['omega_start']} | {lna} | {lrt} | {w2a} | {r['row_flag']} | {r['status']} |"
            )
        report_lines.append("")

    # Integrated reading
    n_true_null = sum(1 for v in clade_verdicts.values() if v == "TRUE_NULL")
    n_artifact = sum(1 for v in clade_verdicts.values() if v == "OPTIMIZER_ARTIFACT")
    n_mixed = sum(1 for v in clade_verdicts.values() if v == "MIXED")

    report_lines.append("## Integrated reading")
    report_lines.append("")
    if n_true_null == len(CLADES):
        report_lines.append(
            f"**ALL {len(CLADES)}/{len(CLADES)} clades remain TRUE NULL after starting-ω scan.**  "
            "The manuscript §3.4 claim that 5/6 production LRT-zero clades reflect a genuine "
            "biological null (rather than codeml optimiser-trapping at the ω₂ = 1 boundary) "
            "stands. Layer-4 verdict in §3.5 (PARTIALLY REFUTED) does NOT need softening."
        )
    elif n_artifact > 0:
        flipped = [c for c, v in clade_verdicts.items() if v == "OPTIMIZER_ARTIFACT"]
        report_lines.append(
            f"**{n_artifact} of {len(CLADES)} clades flipped to OPTIMIZER_ARTIFACT**: "
            + ", ".join(flipped)
        )
        report_lines.append("")
        report_lines.append(
            "The manuscript §3.4 \"5/6 LRT = 0\" count must be revised downward and "
            f"Layer-4 verdict in §3.5 likely needs softening from PARTIALLY REFUTED to "
            "INCONCLUSIVE — optimiser-sensitive."
        )
    else:
        report_lines.append(
            f"**{n_true_null} TRUE_NULL, {n_mixed} MIXED, {n_artifact} OPTIMIZER_ARTIFACT.**  "
            "MIXED clades show some optimiser sensitivity but no escape reaches df=1 χ² "
            "significance (LRT < 2.71). Recommend describing in §3.4 as 'weak null with "
            "optimiser sensitivity' rather than 'genuine biological null'."
        )

    report_lines.append("")
    report_lines.append("## Files")
    report_lines.append(f"- CSV: `{out_csv}`")
    report_lines.append(f"- Per-run dirs: `{RUNS_DIR}/<clade>/alt_w0_<X>/`")
    report_lines.append(f"- Orchestrator log: `{LOG_FILE}`")
    report_lines.append("")

    out_md = OUTPUTS / "optimizer_diagnostic_report.md"
    out_md.write_text("\n".join(report_lines))
    log.info(f"WROTE {out_md}")

    log.info(f"FINAL VERDICT TALLY: TRUE_NULL={n_true_null}, "
             f"MIXED={n_mixed}, OPTIMIZER_ARTIFACT={n_artifact}")
    log.info("Done.")


def _save_intermediate(rows):
    """Write a partial CSV after each codeml completion so a session crash
    doesn't lose progress."""
    if not rows:
        return
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUTS / "optimizer_diagnostic.partial.csv", index=False)


if __name__ == "__main__":
    main()
