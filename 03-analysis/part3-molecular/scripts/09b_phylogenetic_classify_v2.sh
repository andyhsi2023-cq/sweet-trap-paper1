#!/usr/bin/env bash
# 09b_phylogenetic_classify_v2.sh
# ===============================
# Faster v2: includes arthropod Dop1R/Dop2R as additional DRD anchors
# (fixes the "AMBIGUOUS: nearest=OctB2R" issue by adding genuine
# invertebrate dopamine-receptor anchors). Uses -fast mode for
# initial topology; UFBoot B=1000 replaced by B=1000 --bnni for faster
# convergence, but we set -nm 200 to cap iterations.
set -euo pipefail

PROJECT="/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular"
IN_DIR="${PROJECT}/data/orthofinder_input"
OUT_DIR="${PROJECT}/outputs/orthofinder_dop/global_tree_v2"
mkdir -p "${OUT_DIR}"

MERGED="${OUT_DIR}/all_amine_receptors.fa"
: > "${MERGED}"
for fa in "${IN_DIR}"/*.fa; do
  species=$(basename "${fa%.fa}")
  awk -v sp="${species}" '/^>/{print $0"__"sp; next} {print}' "${fa}" >> "${MERGED}"
done

n_seq=$(grep -c "^>" "${MERGED}")
echo "merged ${n_seq} sequences -> ${MERGED}"

ALN="${OUT_DIR}/all_amine_receptors.aln.fa"
mafft --auto --thread 2 "${MERGED}" > "${ALN}" 2> "${OUT_DIR}/mafft.log"
echo "aligned -> ${ALN}"

cd "${OUT_DIR}"
# -fast: quick ML tree (fewer search iterations). Still good topology
# for classification. No bootstraps to save time.
iqtree -s "${ALN}" -m LG+G4 -fast -nt 2 --prefix global_amine_tree_v2 -redo
echo "tree built -> ${OUT_DIR}/global_amine_tree_v2.treefile"
