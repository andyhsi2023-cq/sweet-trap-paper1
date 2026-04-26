#!/usr/bin/env bash
# 14_forward_blastp_anchors_vs_cnidaria.sh
# ==========================================
# Step 3 of Part 3 Risk 1 BLASTP reciprocal strategy.
#
# 输入:
#   data/queries/DRD_anchors.faa          (7 anchors: 5 human DRD + 2 Dmel Dop)
#   data/blast_db/{Hvul,Nvec,Adig}.*      (3 cnidarian BLAST DBs)
#
# 输出:
#   outputs/blast_rbh/forward_DRD_vs_Hvul.tsv
#   outputs/blast_rbh/forward_DRD_vs_Nvec.tsv
#   outputs/blast_rbh/forward_DRD_vs_Adig.tsv
#
# 格式: outfmt 6 + stitle, evalue <= 1e-10, max_target_seqs = 5
# 字段: qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle
#
# n_workers = 2 (遵循项目计算硬约束)

set -euo pipefail

ROOT="/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular"
cd "$ROOT"

Q="data/queries/DRD_anchors.faa"
OUT="outputs/blast_rbh"
LOG="logs/blast_forward.log"
mkdir -p "$OUT" logs

echo "[forward] $(date)" > "$LOG"
for SP in Hvul Nvec Adig; do
  DB="data/blast_db/${SP}"
  OUT_FILE="$OUT/forward_DRD_vs_${SP}.tsv"
  echo "[forward] BLASTP anchors vs $SP -> $OUT_FILE" | tee -a "$LOG"

  blastp -query "$Q" \
         -db "$DB" \
         -evalue 1e-10 \
         -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle" \
         -max_target_seqs 5 \
         -num_threads 2 \
         > "$OUT_FILE" 2>> "$LOG"

  N_ROWS=$(wc -l < "$OUT_FILE")
  echo "  hits (rows): $N_ROWS" | tee -a "$LOG"
done

echo "[forward] Done." | tee -a "$LOG"
