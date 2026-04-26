#!/usr/bin/env bash
#
# 05_pilot_tree.sh — IQ-TREE ML tree for the pilot TAS1R2 protein alignment.
#
# Uses iqtree -s alignment.fasta -m MFP -B 1000 -nt 2 per CLAUDE.md compute rules.

set -euo pipefail

ROOT="/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular"
ENV_BIN="/Users/andy/Desktop/Research/sweet-trap-multidomain/tools/mamba-root/envs/sweet-trap/bin"
PY="/Users/andy/Desktop/Research/sweet-trap-multidomain/venv-phylo/bin/python"

GENE="${1:-TAS1R2}"
ALN="${ROOT}/data/alignments/${GENE}_protein.fasta"
OUT="${ROOT}/outputs"
LOG="${ROOT}/logs/05_tree_${GENE}.log"
TREE_DIR="${OUT}/tree_${GENE}"

mkdir -p "${TREE_DIR}"

if [[ ! -s "${ALN}" ]]; then
  echo "ERROR: alignment not found: ${ALN}" >&2
  exit 2
fi

{
  echo "=== $(date) IQ-TREE for ${GENE} ==="
  n_seq=$(grep -c '^>' "${ALN}")
  echo "sequences: ${n_seq}"
  if [[ ${n_seq} -lt 4 ]]; then
    echo "WARN: fewer than 4 sequences; iqtree -B 1000 bootstrap unreliable"
  fi

  "${ENV_BIN}/iqtree" \
      -s "${ALN}" \
      -m MFP \
      -B 1000 \
      -nt 2 \
      --prefix "${TREE_DIR}/${GENE}" \
      -redo

  gene_lc=$(echo "${GENE}" | tr '[:upper:]' '[:lower:]')
  cp "${TREE_DIR}/${GENE}.treefile" "${OUT}/pilot_tree_${gene_lc}.nwk"

  # Rasterise to PDF via ete3 (already in venv-phylo)
  "${PY}" - <<PY
from pathlib import Path
try:
    from ete3 import Tree, TreeStyle, TextFace, NodeStyle
except Exception as exc:
    print("ete3 render skipped:", exc)
    raise SystemExit(0)
gene = "${GENE}"
gene_lc = gene.lower()
t_path = Path("${OUT}") / f"pilot_tree_{gene_lc}.nwk"
pdf    = Path("${OUT}") / f"pilot_tree_{gene_lc}.pdf"
tree = Tree(str(t_path), format=0)
try:
    tree.set_outgroup(tree.get_midpoint_outgroup())
except Exception:
    pass
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_support = True
ts.scale = 120
ts.title.add_face(TextFace(f"{gene} pilot ML tree (IQ-TREE MFP, UFB 1000)",
                           fsize=12, bold=True), column=0)
try:
    tree.render(str(pdf), tree_style=ts)
    print(f"pdf -> {pdf}")
except Exception as exc:
    # PyQt / headless rendering can fail on macOS - degrade gracefully
    print(f"pdf render failed ({exc}); newick still at {t_path}")
PY

  echo "=== DONE ==="
} 2>&1 | tee "${LOG}"
