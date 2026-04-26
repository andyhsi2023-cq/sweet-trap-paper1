#!/usr/bin/env bash
# Drain the remaining rows after 02b wrapper was killed. Respects n_workers=2
# by checking both pids (not just pids[0]).
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNS_DIR="$ROOT/data/codeml_runs"
LOGS_DIR="$ROOT/logs"
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG="$LOGS_DIR/02c_drain_${STAMP}.log"

# Remaining rows (those without lrt_stats.tsv)
CANDIDATES=(
    TAS1R1__apus_tip_v4
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

# Filter to those actually pending
ROWS=()
for r in "${CANDIDATES[@]}"; do
    if [ ! -f "$RUNS_DIR/$r/lrt_stats.tsv" ]; then
        ROWS+=("$r")
    fi
done

MAX_PAR=2
# Account for existing in-flight codeml (row 7 apus if still running); we can
# launch (MAX_PAR - in_flight_count) new rows immediately.
IN_FLIGHT_COUNT=$(pgrep -x codeml | wc -l | tr -d ' ' || echo 0)
echo "[$(date +%H:%M:%S)] START 02c_drain: ${#ROWS[@]} rows pending, codeml_in_flight=$IN_FLIGHT_COUNT" | tee "$LOG"

run_one_wrapper() {
    local run_id="$1"
    local per_log="$LOGS_DIR/02c_drain_${run_id}_${STAMP}.log"
    bash "$ROOT/scripts/02_run_branch_site.sh" "$run_id" > "$per_log" 2>&1
    echo "[$(date +%H:%M:%S)] DONE $run_id rc=$?" | tee -a "$LOG"
}

pids=()
for row in "${ROWS[@]}"; do
    # wait until codeml count < MAX_PAR
    while true; do
        # remove dead pids from our tracking
        new_pids=()
        if [ "${#pids[@]}" -gt 0 ]; then
            for p in "${pids[@]}"; do
                if kill -0 "$p" 2>/dev/null; then
                    new_pids+=("$p")
                fi
            done
        fi
        pids=()
        if [ "${#new_pids[@]}" -gt 0 ]; then
            pids=("${new_pids[@]}")
        fi

        current_cm=$(pgrep -x codeml | wc -l | tr -d ' ' || echo 0)
        if [ "$current_cm" -lt "$MAX_PAR" ]; then
            break
        fi
        sleep 4
    done
    echo "[$(date +%H:%M:%S)] LAUNCH $row" | tee -a "$LOG"
    run_one_wrapper "$row" &
    pids+=($!)
    sleep 1
done

# Drain remaining
if [ "${#pids[@]}" -gt 0 ]; then
    for p in "${pids[@]}"; do
        wait "$p" 2>/dev/null
    done
fi
echo "[$(date +%H:%M:%S)] ALL DONE" | tee -a "$LOG"
