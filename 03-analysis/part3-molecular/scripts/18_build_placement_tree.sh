#!/usr/bin/env bash
# 18_build_placement_tree.sh
# ==========================
# Step 5: Focused placement tree to classify the 15 cnidarian weak-RBH
# candidates as DRD vs non-DRD aminergic GPCRs.
#
# Taxon composition (n=52):
#   * 25 existing true-DRD orthogroup (from tree_DRD_true_orthogroup):
#     - 5 vertebrate DRD1 + 5 DRD2
#     - 6 arthropod DopR1 + 6 DopR2
#     - 3 mollusc DopR (Aplysia, Crassostrea, Octopus)
#   * 10 additional amine outgroups (human reference set):
#     HTR1A HTR1B HTR2A HTR4 HTR7 ADRB1 ADRB2 ADRB3 ADRA1A + Dmel_OCTB2R
#   * 15 cnidarian candidates (weak-RBH_DRD from BLASTP)
#   * + 2 outgroup roots: HUMAN_HRH1 (histamine) + Drosophila_OAMB
#
# Pipeline: mafft --auto -> iqtree LG+G4 + UFBoot 1000
# Output:
#   outputs/orthofinder_dop/tree_cnidarian_placement/cnidarian_placement.fa
#   ... .aln.fa
#   ... .treefile   (ML tree)
#   ... .contree    (UFBoot consensus)
#
# Compute: -nt 2 (project rule)

set -euo pipefail

ROOT="/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular"
cd "$ROOT"

DIR="outputs/orthofinder_dop/tree_cnidarian_placement"
mkdir -p "$DIR"
LOG="logs/tree_placement.log"
mkdir -p logs

OUT_FA="$DIR/cnidarian_placement.fa"
: > "$OUT_FA"

# 1) copy existing DRD tree taxa
cat outputs/orthofinder_dop/tree_DRD_true_orthogroup/true_DRD_orthogroup.fa >> "$OUT_FA"

# 2) append 15 cnidarian RBH candidates
cat outputs/blast_rbh/rbh_drd_candidates.faa >> "$OUT_FA"

# 3) append outgroups from human reference FASTA
#    Extract HTR1A, HTR1B, HTR2A, HTR4, HTR7, ADRB1, ADRB2, ADRB3, ADRA1A, and OCTB2R
#    (human_amine_reference.faa contains all of these)
python3 - <<'PYEOF' >> "$OUT_FA"
keep = {
    "HUMAN_HTR1A","HUMAN_HTR1B","HUMAN_HTR2A","HUMAN_HTR4","HUMAN_HTR7",
    "HUMAN_ADRB1","HUMAN_ADRB2","HUMAN_ADRB3","HUMAN_ADRA1A",
    "DMEL_OCTB2R",
}
from pathlib import Path
p = Path("data/queries/human_amine_reference.faa")
take = False
hdr = None
buf = []
out_buf = []
with p.open() as f:
    for ln in f:
        if ln.startswith(">"):
            if take and hdr:
                out_buf.append(hdr + "".join(buf))
            hdr = ln
            label = ln[1:].split("|")[0]
            take = label in keep
            buf = []
        else:
            if take:
                buf.append(ln)
if take and hdr:
    out_buf.append(hdr + "".join(buf))
import sys
sys.stdout.write("".join(out_buf))
PYEOF

# 4) add histamine H1 outgroup for rooting (human HRH1 was not in our reference set;
#    fetch it fresh)
curl -sL "https://rest.uniprot.org/uniprotkb/P35367.fasta" | \
    awk 'BEGIN{first=1} /^>/{if(first){print ">HUMAN_HRH1|P35367|histamine_H1_receptor"; first=0} else print; next} {print}' \
    >> "$OUT_FA"

N=$(grep -c '^>' "$OUT_FA")
echo "[place] assembled $N taxa in $OUT_FA" | tee "$LOG"

# 5) MAFFT alignment
echo "[place] running MAFFT ..." | tee -a "$LOG"
mafft --auto --thread 2 "$OUT_FA" > "$DIR/cnidarian_placement.aln.fa" 2>> "$LOG"
NCOL=$(awk 'BEGIN{n=0} /^>/{next} {n+=length($0); getline; while(length($0)>0 && !/^>/){n+=length($0); if(!getline) break}; print n; exit}' "$DIR/cnidarian_placement.aln.fa" || true)
echo "[place] alignment done" | tee -a "$LOG"

# 6) IQ-TREE: LG+G4, UFBoot 1000
echo "[place] running IQ-TREE ..." | tee -a "$LOG"
cd "$DIR"
rm -f cnidarian_placement.ckp.gz  # allow redo
iqtree -s cnidarian_placement.aln.fa \
       -m LG+G4 \
       -B 1000 \
       -nt 2 \
       -redo \
       -pre cnidarian_placement 2>&1 | tee -a "$ROOT/$LOG"

echo "[place] DONE. Tree: $DIR/cnidarian_placement.treefile" | tee -a "$ROOT/$LOG"
