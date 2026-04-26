#!/usr/bin/env bash
# 16_reverse_blastp_cnidaria_vs_human.sh
# ======================================
# Step 4 of Part 3 Risk 1 BLASTP reciprocal strategy.
#
# 对 52 个 cnidarian candidate hits (来自 forward BLASTP 正向集合) 反向
# BLASTP 到 human amine reference (DRD1-5 + HTR1A/1B/2A/2B/4/6/7 +
# ADRB1-3 + ADRA1A/2A + Dmel Dop1R1/Dop2R/Oct-β2R, n=20).
#
# 判定原则：
#   如果某 cnidarian candidate 的 top-1 reverse hit 是 HUMAN_DRD*,
#   且与 top-2 bitscore 有显著差距(bitscore delta >= 10)，
#   则判定为 "Reciprocal Best Hit (RBH) with DRD" -> 真 DRD ortholog 候选.
#
#   如果 top-1 是 HTR* / ADRB* / ADRA* / OCTB* ，则否定 DRD ortholog 归属。
#
# 输入:
#   outputs/blast_rbh/cnidarian_forward_hits.faa  (52 sequences)
#   data/blast_db/human_amine_ref.*               (20 reference sequences)
#
# 输出:
#   outputs/blast_rbh/reverse_cnidaria_vs_human.tsv

set -euo pipefail

ROOT="/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular"
cd "$ROOT"

Q="outputs/blast_rbh/cnidarian_forward_hits.faa"
DB="data/blast_db/human_amine_ref"
OUT="outputs/blast_rbh/reverse_cnidaria_vs_human.tsv"
LOG="logs/blast_reverse.log"

echo "[reverse] $(date)" > "$LOG"
echo "[reverse] BLASTP $Q vs $DB" | tee -a "$LOG"

# Keep ALL 20 reference hits to later compute confidence delta
blastp -query "$Q" \
       -db "$DB" \
       -evalue 1e-5 \
       -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle" \
       -max_target_seqs 20 \
       -num_threads 2 \
       > "$OUT" 2>> "$LOG"

N=$(wc -l < "$OUT")
echo "[reverse] rows: $N -> $OUT" | tee -a "$LOG"
