#!/usr/bin/env bash
# =============================================================================
# 02b_run_v2_parallel.sh
# =============================================================================
# Purpose: Execute the 21-row Week-2 v2 production matrix with n_workers=2
#          parallelism (per CLAUDE.md compute rules).
# Usage:   bash 02b_run_v2_parallel.sh
# =============================================================================
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNS_DIR="$ROOT/data/codeml_runs"
LOGS_DIR="$ROOT/logs"
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG="$LOGS_DIR/02b_v2_parallel_${STAMP}.log"

# Exact 21-row list from matrix_v2
ROWS=(
    TAS1R1__mammalia_clade_v4
    TAS1R1__rodentia_clade_v4
    TAS1R1__homo_tip_v4
    TAS1R1__gallus_tip_v4
    TAS1R1__danio_tip_v4
    TAS1R1__passeriformes_tip_v4
    TAS1R1__apus_tip_v4
    TAS1R3__mammalia_clade
    TAS1R3__rodentia_clade
    TAS1R3__homo_tip
    TAS1R3__gallus_tip
    TAS1R3__danio_tip
    TAS1R1__mammalia_clade_p3
    Gr_sweet__dmel_Gr64_cluster
    Gr_sweet__amellifera_clade
    Gr_sweet__lepidoptera_clade
    Gr_sweet__coleoptera_clade
    Gr_sweet__aaegypti_clade
    Gr_sweet__dmel_all_clade
    Gr_sweet__Gr5a_tip
    Gr_sweet__Gr64a_tip
)

MAX_PAR=2
TOTAL=${#ROWS[@]}
echo "[$(date +%H:%M:%S)] START 02b_v2_parallel: $TOTAL rows with $MAX_PAR parallel workers" | tee "$LOG"

pids=()
row_for_pid=()

run_one_wrapper() {
    local run_id="$1"
    local per_log="$LOGS_DIR/02b_run_${run_id}_${STAMP}.log"
    bash "$ROOT/scripts/02_run_branch_site.sh" "$run_id" > "$per_log" 2>&1
    local rc=$?
    echo "[$(date +%H:%M:%S)] DONE $run_id rc=$rc" | tee -a "$LOG"
}

for ((i=0; i<TOTAL; i++)); do
    row="${ROWS[$i]}"
    echo "[$(date +%H:%M:%S)] LAUNCH ($((i+1))/$TOTAL) $row" | tee -a "$LOG"
    run_one_wrapper "$row" &
    pids+=($!)
    row_for_pid+=("$row")

    # If we're at capacity, wait for ANY pid to finish
    while [ "${#pids[@]}" -ge "$MAX_PAR" ]; do
        # poll the oldest pid
        if ! kill -0 "${pids[0]}" 2>/dev/null; then
            wait "${pids[0]}" 2>/dev/null
            pids=("${pids[@]:1}")
            row_for_pid=("${row_for_pid[@]:1}")
        else
            sleep 5
        fi
    done
done

# Drain
for pid in "${pids[@]}"; do
    wait "$pid" 2>/dev/null
done

echo "[$(date +%H:%M:%S)] ALL DONE" | tee -a "$LOG"
