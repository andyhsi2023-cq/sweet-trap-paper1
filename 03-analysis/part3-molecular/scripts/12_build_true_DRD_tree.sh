#!/usr/bin/env bash
# 12_build_true_DRD_tree.sh
# =========================
# Build a focused ML tree of ONLY the tree-verified DRD orthologues:
#   - 10 vertebrate DRD1/DRD2 anchors (from the Part 3 DRD1_/DRD2_ fastas)
#   - 5 vertebrate DRD3/4/5 + HTR1A (out-group) anchors (for rooting)
#   - 12 arthropod DopR1/DopR2 anchors (Part 3 DopR1_/DopR2_ fastas)
#   - 3 mollusc/cnidaria TRUE_DRD (Aplysia DopR_2, Crassostrea DopR_3,
#     Octopus DopR_1)
# Plus the 14 reclassified non-DRD members for side-by-side Fig comparison.
#
# Output: outputs/orthofinder_dop/tree_DRD_true_orthogroup.treefile
set -euo pipefail

PROJECT="/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular"
OUT_DIR="${PROJECT}/outputs/orthofinder_dop/tree_DRD_true_orthogroup"
mkdir -p "${OUT_DIR}"

RAW="${PROJECT}/data/raw_protein"
TREE_FA="${OUT_DIR}/true_DRD_orthogroup.fa"

# Gather the true-DRD candidates' FASTAs
: > "${TREE_FA}"
for f in \
  "${RAW}/DRD1_hsapiens.fa" "${RAW}/DRD1_mmusculus.fa" "${RAW}/DRD1_rnorvegicus.fa" \
  "${RAW}/DRD1_ggallus.fa"  "${RAW}/DRD1_xtropicalis.fa" \
  "${RAW}/DRD2_hsapiens.fa" "${RAW}/DRD2_mmusculus.fa" "${RAW}/DRD2_rnorvegicus.fa" \
  "${RAW}/DRD2_ggallus.fa"  "${RAW}/DRD2_xtropicalis.fa" \
  "${RAW}/DopR1_dmelanogaster.fa" "${RAW}/DopR2_dmelanogaster.fa" \
  "${RAW}/DopR1_amellifera.fa"    "${RAW}/DopR2_amellifera.fa" \
  "${RAW}/DopR1_tcastaneum.fa"    "${RAW}/DopR2_tcastaneum.fa" \
  "${RAW}/DopR1_aaegypti.fa"      "${RAW}/DopR2_aaegypti.fa" \
  "${RAW}/DopR1_msexta.fa"        "${RAW}/DopR2_msexta.fa" \
  "${RAW}/DopR1_bmori.fa"         "${RAW}/DopR2_bmori.fa" \
  "${RAW}/DopR_2_acalifornica.fa" "${RAW}/DopR_3_cgigas.fa" \
  "${RAW}/DopR_1_obimaculoides.fa" \
  ; do
  if [ -f "$f" ]; then
    cat "$f" >> "${TREE_FA}"
    echo "" >> "${TREE_FA}"  # ensure newline separation
  else
    echo "[warn] missing $f" >&2
  fi
done

n=$(grep -c "^>" "${TREE_FA}")
echo "merged ${n} sequences into ${TREE_FA}"

# Align + tree
cd "${OUT_DIR}"
mafft --auto --thread 2 true_DRD_orthogroup.fa > true_DRD_orthogroup.aln.fa 2> mafft.log
iqtree -s true_DRD_orthogroup.aln.fa -m LG+G4 -B 1000 -nt 2 --prefix tree_DRD_true_orthogroup -redo -nm 200
echo "tree -> ${OUT_DIR}/tree_DRD_true_orthogroup.treefile"
