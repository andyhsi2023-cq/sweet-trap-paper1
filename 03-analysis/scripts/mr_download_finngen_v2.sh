#!/bin/bash
# v2 downloader: resumable parts (curl --continue-at), 8 parallel connections,
# writes parts to P1 (not /tmp so a Claude kill won't wipe progress),
# finalizes by cat to single gz.
#
# Usage: ./mr_download_finngen_v2.sh <phenocode>
set -eu

PH=$1
DST_DIR="/Volumes/P1/城市研究/UKB_芬兰Finngen_catalog_ieu/gwas_list/Finngen/R12_summary_stats"
PART_DIR="${DST_DIR}/_parts_${PH}"
mkdir -p "$PART_DIR"
URL="https://storage.googleapis.com/finngen-public-data-r12/summary_stats/release/finngen_R12_${PH}.gz"
FINAL="${DST_DIR}/finngen_R12_${PH}.gz"

if [[ -f "$FINAL" ]] && [[ $(stat -f%z "$FINAL") -gt 10485760 ]]; then
  echo "[skip] $PH: already $(stat -f%z "$FINAL") bytes"
  exit 0
fi

echo "[info] probe size: $URL"
SIZE=$(curl -sI "$URL" | awk '/[Cc]ontent-[Ll]ength:/ {gsub("\r",""); print $2}' | tail -1)
if [[ -z "$SIZE" ]]; then echo "[err] no size"; exit 1; fi
echo "[info] size = $SIZE bytes ($((SIZE / 1024 / 1024)) MB)"

N=8
CHUNK=$((SIZE / N))
for i in $(seq 0 $((N-1))); do
  START=$((i * CHUNK))
  if [[ $i -eq $((N-1)) ]]; then END=$((SIZE - 1)); else END=$(((i+1) * CHUNK - 1)); fi
  PART="${PART_DIR}/part_${i}"
  (
    attempt=1
    while true; do
      HAVE=0
      [[ -f "$PART" ]] && HAVE=$(stat -f%z "$PART")
      NEED=$((END - START + 1))
      if [[ $HAVE -ge $NEED ]]; then echo "[ok] part $i already complete"; break; fi
      # Range = START + HAVE ... END
      CURSTART=$((START + HAVE))
      curl -sSL --retry 5 --retry-delay 3 --retry-all-errors --max-time 600 \
        -r ${CURSTART}-${END} \
        -o "${PART}.addon" \
        "$URL" || { echo "[retry$attempt] part $i curl exit"; sleep 5; attempt=$((attempt+1)); [[ $attempt -gt 10 ]] && exit 2; continue; }
      if [[ -f "${PART}.addon" ]]; then
        cat "${PART}.addon" >> "$PART"
        rm -f "${PART}.addon"
      fi
      HAVE=$(stat -f%z "$PART")
      if [[ $HAVE -eq $NEED ]]; then echo "[ok] part $i done ($HAVE/$NEED)"; break; fi
      echo "[retry$attempt] part $i have=$HAVE want=$NEED"
      attempt=$((attempt+1))
      [[ $attempt -gt 10 ]] && { echo "[fail] part $i"; exit 2; }
      sleep 2
    done
  ) &
done
wait

echo "[info] assembling..."
cat "$PART_DIR"/part_* > "${FINAL}.tmp"
ASSEMBLED=$(stat -f%z "${FINAL}.tmp")
if [[ $ASSEMBLED -ne $SIZE ]]; then
  echo "[err] assembled=$ASSEMBLED size=$SIZE — keep parts, abort move"
  exit 3
fi
mv "${FINAL}.tmp" "$FINAL"
# test gzip integrity
if ! gzip -t "$FINAL" 2>/dev/null; then
  echo "[err] gzip integrity FAIL"
  mv "$FINAL" "${FINAL}.corrupt"
  exit 4
fi
rm -rf "$PART_DIR"
echo "[done] $PH -> $FINAL ($ASSEMBLED bytes)"
