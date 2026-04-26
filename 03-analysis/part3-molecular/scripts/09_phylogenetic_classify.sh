#!/usr/bin/env bash
# 09_phylogenetic_classify.sh
# ===========================
#
# OrthoFinder's MCL clustering is too blunt at this sample scale (62
# sequences, 13 species) to cleanly separate DRD from HTR/ADR/OA/TAR.
# We switch to a phylogenetic classification: build one global protein
# tree of ALL 62 sequences and read which mollusc/cnidarian sequences
# branch inside vs. outside the DRD clade.
#
# Output: outputs/orthofinder_dop/global_tree/
set -euo pipefail

PROJECT="/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular"
IN_DIR="${PROJECT}/data/orthofinder_input"
OUT_DIR="${PROJECT}/outputs/orthofinder_dop/global_tree"
mkdir -p "${OUT_DIR}"

# Merge all species FASTAs into one file with species-tagged headers.
# Header format: >ACCESSION__LABEL__SPECIES
MERGED="${OUT_DIR}/all_amine_receptors.fa"
: > "${MERGED}"
for fa in "${IN_DIR}"/*.fa; do
  species=$(basename "${fa%.fa}")
  awk -v sp="${species}" '/^>/{print $0"__"sp; next} {print}' "${fa}" >> "${MERGED}"
done

n_seq=$(grep -c "^>" "${MERGED}")
echo "merged ${n_seq} sequences -> ${MERGED}"

# Align with MAFFT (auto mode).
ALN="${OUT_DIR}/all_amine_receptors.aln.fa"
mafft --auto --thread 2 "${MERGED}" > "${ALN}" 2> "${OUT_DIR}/mafft.log"
echo "aligned -> ${ALN}"

# Build ML tree. ModelFinder + 1000 UFBoot + 2 threads.
# --prefix controls output basename.
cd "${OUT_DIR}"
iqtree -s "${ALN}" -m MFP -B 1000 -nt 2 --prefix global_amine_tree -redo
echo "tree built -> ${OUT_DIR}/global_amine_tree.treefile"
