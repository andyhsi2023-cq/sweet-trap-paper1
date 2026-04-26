#!/usr/bin/env bash
# =============================================================================
# 02d_drain_opus.sh
# =============================================================================
# Fixed version of 02c_drain_remaining.sh. The prior version had a pipefail +
# `|| echo 0` bug that produced a two-line "0\n0" for the in-flight count and
# caused the gate to never open.
#
# Usage: bash 02d_drain_opus.sh
# Policy: n_workers = 2 (per CLAUDE.md M5 Pro rule)
# =============================================================================

# Intentional no-pipefail: we rely on `pgrep` exit code 1 (no match) being harmless.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNS_DIR="$ROOT/data/codeml_runs"
LOGS_DIR="$ROOT/logs"
mkdir -p "$LOGS_DIR"
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG="$LOGS_DIR/02d_drain_opus_${STAMP}.log"

# The 9 pending rows for Gr_sweet panel + apus_tip_v4 re-run
CANDIDATES=(
    Gr_sweet__amellifera_clade
    Gr_sweet__dmel_Gr64_cluster
    Gr_sweet__dmel_all_clade
    Gr_sweet__coleoptera_clade
    Gr_sweet__lepidoptera_clade
    Gr_sweet__aaegypti_clade
    Gr_sweet__Gr5a_tip
    Gr_sweet__Gr64a_tip
    TAS1R1__apus_tip_v4
)

# Filter to those actually pending (no lrt_stats.tsv)
ROWS=()
for r in "${CANDIDATES[@]}"; do
    if [ ! -f "$RUNS_DIR/$r/lrt_stats.tsv" ]; then
        ROWS+=("$r")
    fi
done

MAX_PAR=2

count_codeml() {
    # Always returns a single integer. `pgrep` returns 1 on no-match; we mask.
    local n
    n=$(pgrep -x codeml 2>/dev/null | wc -l | tr -d ' \n')
    if [ -z "$n" ]; then
        echo 0
    else
        echo "$n"
    fi
}

echo "[$(date +%H:%M:%S)] START 02d_drain_opus: ${#ROWS[@]} rows pending, codeml_in_flight=$(count_codeml)" | tee "$LOG"

run_one_wrapper() {
    local run_id="$1"
    local per_log="$LOGS_DIR/02d_drain_${run_id}_${STAMP}.log"
    bash "$ROOT/scripts/02_run_branch_site.sh" "$run_id" > "$per_log" 2>&1
    local rc=$?
    echo "[$(date +%H:%M:%S)] DONE $run_id rc=$rc" | tee -a "$LOG"
}

pids=()
for row in "${ROWS[@]}"; do
    # Wait for a slot (codeml-count-based throttle).
    while true; do
        # Reap any of our launched bg tasks that finished.
        new_pids=()
        for p in "${pids[@]:-}"; do
            if [ -n "$p" ] && kill -0 "$p" 2>/dev/null; then
                new_pids+=("$p")
            fi
        done
        pids=("${new_pids[@]:-}")

        current_cm=$(count_codeml)
        if [ "$current_cm" -lt "$MAX_PAR" ]; then
            break
        fi
        sleep 5
    done
    echo "[$(date +%H:%M:%S)] LAUNCH $row (in_flight=$(count_codeml))" | tee -a "$LOG"
    run_one_wrapper "$row" &
    pids+=("$!")
    # Give the just-launched wrapper time to spawn codeml before loop recounts.
    sleep 3
done

echo "[$(date +%H:%M:%S)] All rows launched, waiting for tail to drain..." | tee -a "$LOG"
# Wait for all background wrappers.
for p in "${pids[@]:-}"; do
    if [ -n "$p" ]; then
        wait "$p" 2>/dev/null
    fi
done
echo "[$(date +%H:%M:%S)] ALL DONE" | tee -a "$LOG"
