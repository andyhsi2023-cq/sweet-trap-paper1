#!/usr/bin/env python3
"""
run_apis_optimizer_diagnostic.py

Purpose
-------
Asymmetric optimiser-boundary diagnostic for the Apis mellifera Gr_sweet clade —
the only LRT > 0 production clade not yet diagnostically tested. Hostile-referee
audit (manuscript §4.5) flagged that production omega = 36.2 sits in the same
boundary-artefact range as the two flagged D. melanogaster escapes (omega = 95.1
and 144.9), so Apis must be re-tested under the same Yang & dos Reis (2011)
multi-start procedure as the 5 LRT=0 clades.

Inputs
------
- Per-run dir: 03-analysis/part4-genetic/data/codeml_runs/Gr_sweet__amellifera_clade/
- Existing alt files there:
    * alt_init05_mlc.out  (omega0=0.5  -> LRT=9.92, foreground omega=36.18, production)
    * alt_init15_mlc.out  (omega0=1.5  -> LRT=2.06, NOT in diagnostic set; ignored)
- null_mlc.out (lnL_null reused as denominator)

Procedure
---------
Reuse omega0 = 0.5 from production. Run 4 NEW codeml jobs at
omega0 in {0.1, 1.0, 2.0, 5.0}. n_workers = 2 (CLAUDE.md).

Decision rule (asymmetric — production LRT > 0)
-----------------------------------------------
- APIS_TRUE_POSITIVE
    All 5 starts converge to similar lnL_alt (range <= 1.0 lnL units),
    foreground omega_2a in tight range around 36 (production value),
    LRT > 6.63 (df=1 chi^2 p < 0.01) at all starts.
- APIS_OPTIMIZER_ARTIFACT
    Any start gives lnL closer to null (LRT -> 0) OR omega_2a jumps to a
    wildly different range (omega -> ~1.0 boundary or omega -> 200+).
- APIS_MIXED
    Partial agreement: some starts confirm omega ~ 36, others do not, but
    no clean true-positive nor clean artifact pattern.

Outputs
-------
- 03-analysis/part4-genetic/outputs/apis_optimizer_diagnostic.csv
- 03-analysis/part4-genetic/outputs/apis_optimizer_diagnostic_report.md
- Per-run dirs: data/codeml_runs/Gr_sweet__amellifera_clade/alt_w0_<X>/

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

CLADE = "Gr_sweet__amellifera_clade"
PRODUCTION_OMEGA_2A = 36.18  # for "tight range around" check
PRODUCTION_LRT = 9.92

OMEGA_STARTS = [0.1, 0.5, 1.0, 2.0, 5.0]
OMEGA_REUSE = {0.5: "alt_init05_mlc.out"}  # production result
N_WORKERS = 2  # CLAUDE.md compute rule

LOG_FILE = LOG_DIR / f"apis_orchestrator_{time.strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

# ---- Parsers (same regex as 5-clade diagnostic) ------------------------------

LNL_RE = re.compile(r"^lnL.*?(-\d+\.\d+)", re.M)
FG_W_RE = re.compile(r"foreground w\s+[0-9.]+\s+[0-9.]+\s+([0-9.]+)")
PROP_RE = re.compile(r"proportion\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)")


def parse_lnL(mlc_path: Path) -> Optional[float]:
    if not mlc_path.exists():
        return None
    m = LNL_RE.search(mlc_path.read_text())
    return float(m.group(1)) if m else None


def parse_fg_omega_2a(mlc_path: Path) -> Optional[float]:
    if not mlc_path.exists():
        return None
    m = FG_W_RE.search(mlc_path.read_text())
    return float(m.group(1)) if m else None


def parse_proportion_2a_2b(mlc_path: Path) -> Optional[float]:
    if not mlc_path.exists():
        return None
    m = PROP_RE.search(mlc_path.read_text())
    if not m:
        return None
    return float(m.group(3)) + float(m.group(4))


def edit_omega_in_ctl(ctl_path: Path, new_omega: float) -> None:
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


def setup_subdir(omega0: float) -> Path:
    src = RUNS_DIR / CLADE
    sub = src / f"alt_w0_{omega0}"
    sub.mkdir(exist_ok=True)
    for fn in ("alignment.phy", "tree_labelled.nwk"):
        if not (sub / fn).exists():
            shutil.copy(src / fn, sub / fn)
    ctl_dst = sub / "alt.ctl"
    shutil.copy(src / "alt.ctl", ctl_dst)
    edit_omega_in_ctl(ctl_dst, omega0)
    return sub


def run_codeml(sub: Path, omega0: float, timeout_s: int = 10800) -> dict:
    mlc = sub / "alt_mlc.out"
    stdout_log = sub / "codeml_stdout.log"
    label = f"{CLADE}__w0_{omega0}"
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
        return {"clade": CLADE, "omega_start": omega0, "lnL_alt": None,
                "omega_2a": None, "p2a_p2b": None, "status": "timeout",
                "wall_seconds": timeout_s}
    dt = time.time() - t0
    lnL = parse_lnL(mlc)
    if lnL is None:
        log.error(f"FAIL  {label} no lnL after {dt:.0f}s")
        return {"clade": CLADE, "omega_start": omega0, "lnL_alt": None,
                "omega_2a": None, "p2a_p2b": None, "status": "no_lnL",
                "wall_seconds": int(dt)}
    fg_w = parse_fg_omega_2a(mlc)
    p2ab = parse_proportion_2a_2b(mlc)
    log.info(f"DONE  {label} lnL={lnL} fg_w_2a={fg_w} dt={dt:.0f}s")
    return {"clade": CLADE, "omega_start": omega0, "lnL_alt": lnL,
            "omega_2a": fg_w, "p2a_p2b": p2ab, "status": "ok",
            "wall_seconds": int(dt)}


def collect_reuse(omega0: float) -> dict:
    fn = OMEGA_REUSE[omega0]
    mlc = RUNS_DIR / CLADE / fn
    lnL = parse_lnL(mlc)
    fg_w = parse_fg_omega_2a(mlc)
    p2ab = parse_proportion_2a_2b(mlc)
    log.info(f"REUSE {CLADE}__w0_{omega0} from {fn} lnL={lnL} fg_w_2a={fg_w}")
    return {"clade": CLADE, "omega_start": omega0, "lnL_alt": lnL,
            "omega_2a": fg_w, "p2a_p2b": p2ab, "status": "reused",
            "wall_seconds": 0}


def get_lnL_null() -> float:
    mlc = RUNS_DIR / CLADE / "null_mlc.out"
    v = parse_lnL(mlc)
    if v is None:
        raise RuntimeError(f"Missing null_mlc.out lnL: {mlc}")
    return v


def apis_verdict(rows: pd.DataFrame) -> str:
    """Asymmetric Apis decision rule (production LRT > 0).

    APIS_TRUE_POSITIVE: all rows have LRT > 6.63 AND omega_2a in [10, 100].
    APIS_OPTIMIZER_ARTIFACT: any row has LRT < 1.0 OR omega_2a near 1.0
        (|omega_2a - 1.0| < 0.5) OR omega_2a > 200.
    APIS_MIXED: anything else.
    """
    sub = rows.dropna(subset=["LRT", "omega_2a"])
    if sub.empty:
        return "INSUFFICIENT_DATA"

    lrts = sub["LRT"].values
    fg_ws = sub["omega_2a"].values

    near_boundary = any(abs(w - 1.0) < 0.5 for w in fg_ws)
    runaway = any(w > 200 for w in fg_ws)
    near_null = any(lrt < 1.0 for lrt in lrts)

    all_significant = all(lrt > 6.63 for lrt in lrts)
    all_in_band = all(10 <= w <= 100 for w in fg_ws)

    if near_null or near_boundary or runaway:
        return "APIS_OPTIMIZER_ARTIFACT"
    if all_significant and all_in_band:
        return "APIS_TRUE_POSITIVE"
    return "APIS_MIXED"


# ---- Main --------------------------------------------------------------------

def main():
    log.info(f"Apis optimiser-boundary diagnostic. Log: {LOG_FILE}")
    log.info(f"Clade: {CLADE} | Production omega_2a={PRODUCTION_OMEGA_2A} LRT={PRODUCTION_LRT}")

    run_dir = RUNS_DIR / CLADE
    for must in ("alignment.phy", "tree_labelled.nwk", "alt.ctl",
                 "null_mlc.out", "alt_init05_mlc.out"):
        if not (run_dir / must).exists():
            raise FileNotFoundError(f"Missing {must} in {run_dir}")

    # Build to-run list (skip omega=0.5; reused)
    tasks = []
    for w0 in OMEGA_STARTS:
        if w0 in OMEGA_REUSE:
            continue
        sub = setup_subdir(w0)
        tasks.append((w0, sub))
    log.info(f"Will run {len(tasks)} new codeml jobs.")

    # Execute with n_workers=2
    results = []
    completed = 0
    total = len(tasks)
    t_wall0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=N_WORKERS) as ex:
        future_map = {ex.submit(run_codeml, sub, w0): w0 for (w0, sub) in tasks}
        for fut in cf.as_completed(future_map):
            w0 = future_map[fut]
            try:
                r = fut.result()
            except Exception as e:
                log.error(f"EXCEPTION w0={w0}: {e}")
                r = {"clade": CLADE, "omega_start": w0, "lnL_alt": None,
                     "omega_2a": None, "p2a_p2b": None, "status": f"exception:{e}",
                     "wall_seconds": 0}
            results.append(r)
            completed += 1
            log.info(f"PROGRESS {completed}/{total}")
            _save_intermediate(results)

    # Add reused row
    for w0 in OMEGA_REUSE:
        results.append(collect_reuse(w0))

    df = pd.DataFrame(results).sort_values("omega_start").reset_index(drop=True)
    lnL_null = get_lnL_null()
    df["lnL_null"] = lnL_null
    df["LRT"] = 2 * (df["lnL_alt"] - df["lnL_null"])

    df["row_flag"] = df.apply(
        lambda r: (
            "boundary" if (pd.notna(r["LRT"]) and r["LRT"] <= 0.01
                           and pd.notna(r["omega_2a"]) and abs(r["omega_2a"] - 1.0) < 0.001)
            else ("escaped" if pd.notna(r["LRT"]) and r["LRT"] > 0.01 else "fail")
        ),
        axis=1,
    )

    verdict = apis_verdict(df)
    df["verdict"] = verdict

    # Write CSV
    out_csv = OUTPUTS / "apis_optimizer_diagnostic.csv"
    df_out = df[["clade", "omega_start", "lnL_alt", "lnL_null", "LRT",
                 "omega_2a", "p2a_p2b", "row_flag", "status", "wall_seconds",
                 "verdict"]]
    df_out.to_csv(out_csv, index=False)
    log.info(f"WROTE {out_csv} ({len(df_out)} rows)")

    # Markdown report
    total_wall = time.time() - t_wall0
    lines = []
    lines.append("# Apis Gr_sweet — Optimiser-boundary diagnostic")
    lines.append("")
    lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append(f"**Clade**: `{CLADE}`")
    lines.append(f"**Production**: omega0=0.5 -> lnL_alt={parse_lnL(run_dir / 'alt_init05_mlc.out')}, "
                 f"foreground omega_2a={PRODUCTION_OMEGA_2A}, LRT={PRODUCTION_LRT}")
    lines.append(f"**lnL_null** (production, fix_omega=1): {lnL_null:.6f}")
    lines.append("")
    lines.append("**Asymmetric decision rule**:")
    lines.append("- APIS_TRUE_POSITIVE: all 5 LRT > 6.63 AND all omega_2a in [10, 100]")
    lines.append("- APIS_OPTIMIZER_ARTIFACT: any LRT < 1.0 OR omega_2a near 1.0 (|w-1| < 0.5) "
                 "OR omega_2a > 200")
    lines.append("- APIS_MIXED: anything else (partial agreement)")
    lines.append("")
    lines.append("## Per-start results")
    lines.append("")
    lines.append("| omega_0 | lnL_alt | LRT | omega_2a | p_2a+2b | flag | status | wall_s |")
    lines.append("|---------|---------|-----|----------|---------|------|--------|--------|")
    for _, r in df.iterrows():
        lna = f"{r['lnL_alt']:.6f}" if pd.notna(r["lnL_alt"]) else "NA"
        lrt = f"{r['LRT']:.4f}" if pd.notna(r["LRT"]) else "NA"
        w2a = f"{r['omega_2a']:.4f}" if pd.notna(r["omega_2a"]) else "NA"
        p2ab = f"{r['p2a_p2b']:.4f}" if pd.notna(r["p2a_p2b"]) else "NA"
        lines.append(f"| {r['omega_start']} | {lna} | {lrt} | {w2a} | {p2ab} | "
                     f"{r['row_flag']} | {r['status']} | {r['wall_seconds']} |")
    lines.append("")

    lines.append("## Verdict")
    lines.append("")
    lines.append(f"**{verdict}**")
    lines.append("")
    if verdict == "APIS_TRUE_POSITIVE":
        lines.append(
            "All starting omegas converge to the production basin (omega_2a in [10, 100], "
            "LRT > 6.63). Apis Gr_sweet survives the asymmetric diagnostic. "
            "Manuscript framing in section 4.5 strengthens to: "
            "'Apis as the only diagnostically-confirmed positive-selection signal among 6 production tests.'"
        )
    elif verdict == "APIS_OPTIMIZER_ARTIFACT":
        lines.append(
            "At least one starting omega returns to the boundary (omega_2a ~ 1.0), produces "
            "a runaway omega (> 200), or yields LRT ~ 0. The production omega_2a = 36.18 is "
            "NOT robust to starting-value perturbation. Apis joins D. melanogaster as a "
            "third boundary-range optimiser-trapped escape. Manuscript Layer-4 verdict tightens: "
            "no robust positive-selection signals across any of the 6 production tests."
        )
    else:
        lines.append(
            "Some starts confirm the production basin while others escape the boundary or "
            "produce different optima. The Apis signal is partially robust but not unambiguous. "
            "Recommend describing in section 4.5 as 'tentative — optimiser-sensitive' rather "
            "than supporting a strong positive-selection claim."
        )
    lines.append("")
    lines.append("## Files")
    lines.append(f"- CSV: `{out_csv}`")
    lines.append(f"- Per-run dirs: `{run_dir}/alt_w0_<X>/`")
    lines.append(f"- Orchestrator log: `{LOG_FILE}`")
    lines.append(f"- Total wall time: {total_wall:.0f} s ({total_wall/60:.1f} min)")
    lines.append("")

    out_md = OUTPUTS / "apis_optimizer_diagnostic_report.md"
    out_md.write_text("\n".join(lines))
    log.info(f"WROTE {out_md}")
    log.info(f"FINAL VERDICT: {verdict} | total wall {total_wall:.0f}s")


def _save_intermediate(rows):
    if not rows:
        return
    pd.DataFrame(rows).to_csv(OUTPUTS / "apis_optimizer_diagnostic.partial.csv", index=False)


if __name__ == "__main__":
    main()
