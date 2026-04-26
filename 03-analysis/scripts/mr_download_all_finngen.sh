#!/bin/bash
# Download all 9 Finngen R12 outcomes sequentially (each runs 4 parallel parts internally).
# Sequential because multiple 4-way parallel would saturate bandwidth without gain.
set -eu
PHENOS=(F5_DEPRESSIO ANTIDEPRESSANTS ALCOPANCCHRON K11_ALCOLIV C3_HEPATOCELLU_CARC_EXALLC DM_NEPHROPATHY C_STROKE F5_ANXIETY T2D)
SCRIPT_DIR=$(dirname "$0")
LOGP="$SCRIPT_DIR/mr_download_all_finngen.log"
: > "$LOGP"
for PH in "${PHENOS[@]}"; do
  echo "=========== $PH ===========" | tee -a "$LOGP"
  bash "$SCRIPT_DIR/mr_download_finngen_parallel.sh" "$PH" 2>&1 | tee -a "$LOGP"
done
echo "ALL DONE" | tee -a "$LOGP"
