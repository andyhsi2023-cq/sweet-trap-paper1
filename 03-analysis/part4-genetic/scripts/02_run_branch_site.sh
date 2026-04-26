#!/usr/bin/env bash
# =============================================================================
# 02_run_branch_site.sh
# =============================================================================
# Purpose: Execute PAML codeml for every prepared run directory under
#          data/codeml_runs/<gene>__<lineage>/. For each directory:
#            1. Run null model (null.ctl)          -> null_mlc.out, lnL_null
#            2. Run alt model with init omega=0.5  -> alt_init05_mlc.out
#            3. Run alt model with init omega=1.5  -> alt_init15_mlc.out
#            4. Take the max lnL_alt from the two alt runs
#            5. Write lnL summary to data/codeml_runs/<run>/lrt_stats.tsv
#
# Multiple-init policy: PAML branch-site is prone to local optima. We run TWO
# initial omega values on the alt and keep the higher lnL (Yang 2007 PAML manual;
# Anisimova & Yang 2007).
#
# Compute policy: codeml is single-threaded. We run runs SEQUENTIALLY to stay
# within CLAUDE.md n_workers <= 2 rule. Each run is ~0.5-1 h; 24 runs => ~1-2 days
# calendar. A parallel wrapper (GNU parallel -j 2) is commented in the script.
#
# Environment: requires codeml on PATH. Sourced from micromamba env `sweet-trap`
# (paml package provides codeml). Fallbacks: homebrew 'paml' formula or manual
# install from https://github.com/abacus-gene/paml.
#
# Usage:
#   bash 02_run_branch_site.sh                       # run all prepared dirs
#   bash 02_run_branch_site.sh TAS1R1__hummingbird  # run one
#   RUN_MODE=dry bash 02_run_branch_site.sh         # dry-run, skip codeml exec
#
# Outputs:
#   data/codeml_runs/<run>/null_mlc.out
#   data/codeml_runs/<run>/alt_init05_mlc.out
#   data/codeml_runs/<run>/alt_init15_mlc.out
#   data/codeml_runs/<run>/lrt_stats.tsv
#   logs/02_run_branch_site_<timestamp>.log
#
# Exit codes:
#   0  success on all attempted runs
#   1  codeml not found
#   2  one or more runs failed (see log)
# =============================================================================

# NOTE (2026-04-25): -e dropped because codeml exits non-zero after printing a
# cosmetic "end of tree file" warning even when the run succeeded and produced
# a valid mlc file. We therefore check for the presence of an 'lnL' line in the
# mlc output instead of relying on codeml's exit code. (Same logic as the
# positive_control_run.py re-runner.)
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNS_DIR="$ROOT/data/codeml_runs"
LOGS_DIR="$ROOT/logs"
mkdir -p "$LOGS_DIR"

STAMP="$(date +%Y%m%d_%H%M%S)"
MASTER_LOG="$LOGS_DIR/02_run_branch_site_${STAMP}.log"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$MASTER_LOG"; }

# ---- 1. Sanity: locate codeml ------------------------------------------------
if ! command -v codeml >/dev/null 2>&1; then
    log "ERROR: codeml not on PATH."
    log "Activate the sweet-trap env first: micromamba activate sweet-trap"
    log "Or install PAML: conda install -c bioconda paml   OR   brew install paml"
    exit 1
fi
log "codeml: $(command -v codeml)"
log "codeml version: $(codeml 2>&1 | head -2 || true)"

# ---- 2. Pick run set --------------------------------------------------------
if [[ $# -ge 1 ]]; then
    RUNS=("$1")
else
    mapfile -t RUNS < <(cd "$RUNS_DIR" && find . -mindepth 1 -maxdepth 1 -type d | sed 's|^\./||' | sort)
fi

if [[ ${#RUNS[@]} -eq 0 ]]; then
    log "ERROR: No run directories under $RUNS_DIR. Run 01_prepare_codeml_inputs.py first."
    exit 2
fi

log "Found ${#RUNS[@]} run directories"

# ---- 3. Helper: extract lnL from a PAML mlc file ----------------------------
extract_lnL() {
    # The mlc file contains a line like:
    #   lnL(ntime: 31  np: 35):  -4567.123456      +0.000000
    # We pull the first negative float after "lnL(".
    local mlc="$1"
    awk '/^lnL/ {
        for (i=1;i<=NF;i++) if ($i ~ /^-?[0-9]+\.[0-9]+$/ ) { print $i; exit }
    }' "$mlc"
}

# ---- 4. Runner --------------------------------------------------------------
run_one() {
    local run_id="$1"
    local run_dir="$RUNS_DIR/$run_id"
    local ctl="$2"
    local label="$3"
    local out_name="$4"
    local init_omega="${5:-}"

    log "  [$run_id] $label -> $out_name${init_omega:+ (init omega=$init_omega)}"

    # Make a working copy of the ctl so we can edit init omega without mutating source
    local work_ctl="$run_dir/.${label}.ctl"
    cp "$run_dir/$ctl" "$work_ctl"
    # Repoint outfile
    sed -i '' -e "s|outfile = .*|outfile = ${out_name}|" "$work_ctl" 2>/dev/null \
        || sed -i -e "s|outfile = .*|outfile = ${out_name}|" "$work_ctl"
    # Override init omega if requested
    if [[ -n "$init_omega" ]]; then
        sed -i '' -e "s|omega = .*|omega = ${init_omega}|" "$work_ctl" 2>/dev/null \
            || sed -i -e "s|omega = .*|omega = ${init_omega}|" "$work_ctl"
    fi

    if [[ "${RUN_MODE:-real}" == "dry" ]]; then
        log "    DRY-RUN skip codeml exec"
        return 0
    fi

    # Execute codeml. Ignore exit code (codeml emits cosmetic 'end of tree file'
    # warnings that cause a non-zero exit but produce valid mlc output).
    ( cd "$run_dir" && codeml "$(basename "$work_ctl")" >> "$run_dir/${label}_stdout.log" 2>&1 ) || true

    # Success criterion: mlc file exists AND contains an 'lnL' line.
    local mlc_path="$run_dir/$out_name"
    if [[ ! -f "$mlc_path" ]] || ! grep -q "^lnL" "$mlc_path"; then
        log "    codeml FAILED on $run_id $label (no lnL in $out_name)"
        return 1
    fi
    rm -f "$work_ctl"
}

# ---- 5. Main loop -----------------------------------------------------------
N_OK=0
N_FAIL=0
for run_id in "${RUNS[@]}"; do
    log "=== Run: $run_id ==="
    run_dir="$RUNS_DIR/$run_id"
    if [[ ! -f "$run_dir/null.ctl" || ! -f "$run_dir/alt.ctl" ]]; then
        log "  missing null.ctl/alt.ctl -> skip"
        ((N_FAIL++))
        continue
    fi

    # 5a. Null
    run_one "$run_id" "null.ctl" "null" "null_mlc.out" "" \
        || { ((N_FAIL++)); continue; }

    # 5b. Alt, two initial omega values
    run_one "$run_id" "alt.ctl" "alt_init05" "alt_init05_mlc.out" "0.5" \
        || { ((N_FAIL++)); continue; }
    run_one "$run_id" "alt.ctl" "alt_init15" "alt_init15_mlc.out" "1.5" \
        || { ((N_FAIL++)); continue; }

    if [[ "${RUN_MODE:-real}" == "dry" ]]; then
        log "  dry-run: skipping LRT extraction for $run_id"
        ((N_OK++))
        continue
    fi

    # 5c. Extract lnL
    lnL_null=$(extract_lnL "$run_dir/null_mlc.out" || true)
    lnL_alt05=$(extract_lnL "$run_dir/alt_init05_mlc.out" || true)
    lnL_alt15=$(extract_lnL "$run_dir/alt_init15_mlc.out" || true)

    # Best alt lnL
    lnL_alt=$(python3 -c "
vals=[x for x in ['${lnL_alt05}','${lnL_alt15}'] if x]
print(max(map(float, vals)) if vals else '')
")

    # LRT = 2 * (lnL_alt - lnL_null)  -> compare to chi-square df=1, halved p
    LRT=$(python3 -c "print(2*(float('${lnL_alt}') - float('${lnL_null}')))" 2>/dev/null || echo "")
    p_raw=$(python3 -c "
import math, sys
try:
    from scipy.stats import chi2
    lrt=float('${LRT}')
    p_full = 1 - chi2.cdf(max(lrt,0.0), df=1)
    print(p_full / 2.0)  # half-chi-square, one-sided
except Exception as e:
    print('NA')
")

    {
        echo -e "run_id\tlnL_null\tlnL_alt05\tlnL_alt15\tlnL_alt_best\tLRT_2dlnL\tp_raw_half_chi2_df1"
        echo -e "${run_id}\t${lnL_null}\t${lnL_alt05}\t${lnL_alt15}\t${lnL_alt}\t${LRT}\t${p_raw}"
    } > "$run_dir/lrt_stats.tsv"

    log "  lnL_null=$lnL_null  lnL_alt_best=$lnL_alt  LRT=$LRT  p=$p_raw"
    ((N_OK++))
done

log "DONE: $N_OK succeeded, $N_FAIL failed"
[[ $N_FAIL -eq 0 ]] || exit 2
exit 0
