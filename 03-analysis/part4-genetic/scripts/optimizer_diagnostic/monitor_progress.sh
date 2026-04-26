#!/bin/bash
PARTIAL=/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/outputs/optimizer_diagnostic.partial.csv
FINAL=/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/outputs/optimizer_diagnostic.csv
LOG=/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/logs/optimizer_diagnostic/milestones.log
TOTAL=20
LAST_DECILE=0

mkdir -p "$(dirname "$LOG")"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Monitor started; watching $PARTIAL (TOTAL=$TOTAL)" >> "$LOG"

while true; do
  if [ -f "$FINAL" ]; then
    DONE=$(($(wc -l < "$FINAL") - 1))
    [ "$DONE" -ge "$TOTAL" ] && DONE=$TOTAL
  elif [ -f "$PARTIAL" ]; then
    DONE=$(($(wc -l < "$PARTIAL") - 1))
    [ "$DONE" -lt 0 ] && DONE=0
  else
    DONE=0
  fi

  PCT=$(( DONE * 100 / TOTAL ))
  DECILE=$(( PCT / 10 * 10 ))

  if [ "$DECILE" -gt "$LAST_DECILE" ]; then
    TS=$(date '+%Y-%m-%d %H:%M:%S')
    MSG="MILESTONE ${DECILE}%: ${DONE}/${TOTAL} runs complete"
    echo "[$TS] $MSG" >> "$LOG"
    osascript -e "display notification \"${DONE}/${TOTAL} runs done — open chat to see details\" with title \"Sweet Trap Diagnostic ${DECILE}%\" sound name \"Glass\"" 2>/dev/null
    LAST_DECILE=$DECILE
  fi

  if [ "$DONE" -ge "$TOTAL" ] || [ -f "$FINAL" ]; then
    TS=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TS] DIAGNOSTIC COMPLETE — final CSV at $FINAL" >> "$LOG"
    osascript -e "display notification \"All ${TOTAL} runs done. Open chat for verdict integration.\" with title \"Sweet Trap Diagnostic 100%\" sound name \"Hero\"" 2>/dev/null
    break
  fi

  sleep 300
done
