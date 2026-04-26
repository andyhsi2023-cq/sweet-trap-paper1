#!/bin/bash
# Parallel Finngen R12 downloader using HTTP byte-range GET with N=4 connections.
# Usage: ./mr_download_finngen_parallel.sh <phenocode> <dst_dir>
#
# Example:
#   ./mr_download_finngen_parallel.sh F5_DEPRESSIO /Volumes/P1/.../R12_summary_stats
set -eu

PH=$1
DST_DIR=${2:-"/Volumes/P1/城市研究/UKB_芬兰Finngen_catalog_ieu/gwas_list/Finngen/R12_summary_stats"}
URL="https://storage.googleapis.com/finngen-public-data-r12/summary_stats/release/finngen_R12_${PH}.gz"
FINAL="${DST_DIR}/finngen_R12_${PH}.gz"

if [[ -f "$FINAL" ]] && [[ $(stat -f%z "$FINAL") -gt 1048576 ]]; then
  echo "[skip] $PH: already $(stat -f%z "$FINAL") bytes"
  exit 0
fi

echo "[info] probing size of $URL"
SIZE=$(curl -sI "$URL" | awk '/[Cc]ontent-[Ll]ength:/ {gsub("\r",""); print $2}' | tail -1)
if [[ -z "$SIZE" ]]; then
  echo "[error] cannot determine size"; exit 1
fi
echo "[info] total size = $SIZE bytes"

N=4
CHUNK=$((SIZE / N))
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

for i in $(seq 0 $((N-1))); do
  START=$((i * CHUNK))
  if [[ $i -eq $((N-1)) ]]; then
    END=$((SIZE - 1))
  else
    END=$(((i+1) * CHUNK - 1))
  fi
  (
    # retry loop per part
    attempt=1
    while true; do
      curl -sSL --retry 3 --retry-delay 2 --max-time 1800 \
        -r ${START}-${END} \
        -o "$TMPDIR/part_${i}" \
        "$URL"
      got=$(stat -f%z "$TMPDIR/part_${i}" 2>/dev/null || echo 0)
      want=$((END - START + 1))
      if [[ $got -eq $want ]]; then
        echo "[ok] part $i: $got bytes"
        break
      fi
      echo "[retry$attempt] part $i: got $got want $want"
      attempt=$((attempt+1))
      if [[ $attempt -gt 5 ]]; then echo "[fail] part $i"; exit 2; fi
      sleep 3
    done
  ) &
done
wait

# concatenate
echo "[info] assembling"
cat "$TMPDIR/part_"* > "${FINAL}.tmp"
ASSEMBLED=$(stat -f%z "${FINAL}.tmp")
if [[ $ASSEMBLED -ne $SIZE ]]; then
  echo "[error] assembled $ASSEMBLED != $SIZE"; exit 3
fi
mv "${FINAL}.tmp" "$FINAL"
echo "[done] $PH -> $FINAL ($ASSEMBLED bytes)"
