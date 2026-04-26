#!/bin/bash
# v3: use `curl -C - -o PART` so each part is truly resumable.
# No addon concat, no max-time cap that would truncate progress.
# Each of 8 workers writes to its own part_i file and curl resumes on retry.
set -eu

PH=$1
DST_DIR="/Volumes/P1/城市研究/UKB_芬兰Finngen_catalog_ieu/gwas_list/Finngen/R12_summary_stats"
PART_DIR="${DST_DIR}/_parts_${PH}"
mkdir -p "$PART_DIR"
URL="https://storage.googleapis.com/finngen-public-data-r12/summary_stats/release/finngen_R12_${PH}.gz"
FINAL="${DST_DIR}/finngen_R12_${PH}.gz"

if [[ -f "$FINAL" ]] && [[ $(stat -f%z "$FINAL") -gt 10485760 ]]; then
  echo "[skip] $PH"; exit 0
fi

echo "[info] probe size: $URL"
SIZE=$(curl -sI "$URL" | awk '/[Cc]ontent-[Ll]ength:/ {gsub("\r",""); print $2}' | tail -1)
[[ -z "$SIZE" ]] && { echo "[err] no size"; exit 1; }
echo "[info] size = $SIZE bytes ($((SIZE / 1024 / 1024)) MB)"

N=8
CHUNK=$((SIZE / N))
for i in $(seq 0 $((N-1))); do
  START=$((i * CHUNK))
  if [[ $i -eq $((N-1)) ]]; then END=$((SIZE - 1)); else END=$(((i+1) * CHUNK - 1)); fi
  PART="${PART_DIR}/part_${i}"
  NEED=$((END - START + 1))
  (
    attempt=1
    while true; do
      HAVE=0
      [[ -f "$PART" ]] && HAVE=$(stat -f%z "$PART")
      if [[ $HAVE -ge $NEED ]]; then
        # trim excess if any (can happen if resume overshoots)
        if [[ $HAVE -gt $NEED ]]; then
          # use dd to truncate
          dd if="$PART" of="${PART}.trim" bs=1m count=$((NEED/1048576)) 2>/dev/null
          mv "${PART}.trim" "$PART"
        fi
        echo "[ok] part $i: $HAVE/$NEED"; break
      fi
      # Resume: start absolute offset = START + HAVE, ask END
      RANGE="$((START + HAVE))-${END}"
      # NOTE: append mode: use curl with -C - is tricky for range, use explicit > append
      # We'll use curl without -o and append with tee:
      curl -sSL --retry 3 --retry-delay 2 --max-time 900 \
        -r "$RANGE" "$URL" >> "$PART" 2> "${PART}.err" || {
          echo "[retry$attempt] part $i curl exit after ${RANGE}"
          sleep 3
          attempt=$((attempt+1))
          [[ $attempt -gt 12 ]] && { echo "[fail] part $i gave up"; exit 2; }
          continue
        }
      HAVE=$(stat -f%z "$PART")
      echo "[progress] part $i have=$HAVE/$NEED ($((HAVE*100/NEED))%)"
      if [[ $HAVE -lt $NEED ]]; then
        attempt=$((attempt+1))
        [[ $attempt -gt 12 ]] && { echo "[fail] part $i"; exit 2; }
        sleep 2
      fi
    done
  ) &
done
wait

echo "[info] assembling..."
cat "$PART_DIR"/part_* > "${FINAL}.tmp"
ASSEMBLED=$(stat -f%z "${FINAL}.tmp")
if [[ $ASSEMBLED -ne $SIZE ]]; then
  echo "[err] assembled=$ASSEMBLED want=$SIZE"
  exit 3
fi
mv "${FINAL}.tmp" "$FINAL"
if ! gzip -t "$FINAL" 2>/dev/null; then
  mv "$FINAL" "${FINAL}.corrupt"; echo "[err] gzip fail"; exit 4
fi
rm -rf "$PART_DIR"
echo "[done] $PH size=$ASSEMBLED"
