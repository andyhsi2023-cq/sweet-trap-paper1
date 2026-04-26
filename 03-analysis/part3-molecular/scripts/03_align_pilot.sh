#!/usr/bin/env bash
#
# 03_align_pilot.sh — pilot alignment: TAS1R2 across sampled vertebrates.
#
# Workflow (protein-guided codon alignment, TranslatorX-style):
#   1. Concatenate TAS1R2_*.fa protein files  ->  combined protein FASTA
#   2. mafft --auto on protein                 ->  protein alignment
#   3. Back-translate codon alignment from protein using CDS files
#   4. Write alignment stats (gap %, identity, conserved columns)
#
# Outputs:
#   data/alignments/TAS1R2_protein.fasta
#   data/alignments/TAS1R2_codon.fasta
#   outputs/alignment_stats_TAS1R2.txt

set -euo pipefail

ROOT="/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular"
ENV_BIN="/Users/andy/Desktop/Research/sweet-trap-multidomain/tools/mamba-root/envs/sweet-trap/bin"
PY="/Users/andy/Desktop/Research/sweet-trap-multidomain/venv-phylo/bin/python"

PROTS="${ROOT}/data/raw_protein"
CDSS="${ROOT}/data/raw_cds"
ALN="${ROOT}/data/alignments"
OUT="${ROOT}/outputs"
LOGS="${ROOT}/logs"

mkdir -p "${ALN}" "${OUT}" "${LOGS}"

GENE="${1:-TAS1R2}"
LOG="${LOGS}/03_align_${GENE}.log"

{
  echo "=== $(date) pilot alignment: ${GENE} ==="

  COMBINED_PROT="${ALN}/${GENE}_input_protein.fasta"
  COMBINED_CDS="${ALN}/${GENE}_input_cds.fasta"

  # gather all matching files
  shopt -s nullglob
  prot_files=( "${PROTS}/${GENE}_"*.fa )
  cds_files=( "${CDSS}/${GENE}_"*.fa )
  shopt -u nullglob

  if [[ ${#prot_files[@]} -lt 3 ]]; then
    echo "ERROR: need >=3 sequences, found ${#prot_files[@]}"
    exit 2
  fi

  cat "${prot_files[@]}" > "${COMBINED_PROT}"
  cat "${cds_files[@]}"  > "${COMBINED_CDS}"

  n_seq=$(grep -c '^>' "${COMBINED_PROT}")
  echo "Sequences combined: ${n_seq}"

  echo "Running mafft --auto..."
  "${ENV_BIN}/mafft" --auto --anysymbol "${COMBINED_PROT}" \
      > "${ALN}/${GENE}_protein.fasta" 2>> "${LOG}"

  echo "Back-translating to codon alignment..."
  "${PY}" - <<PY
from pathlib import Path
from Bio import SeqIO
gene = "${GENE}"
root = Path("${ROOT}")
prot_aln = root / "data/alignments" / f"{gene}_protein.fasta"
cds_in   = root / "data/alignments" / f"{gene}_input_cds.fasta"
cds_out  = root / "data/alignments" / f"{gene}_codon.fasta"

cds = {r.id: str(r.seq).upper() for r in SeqIO.parse(cds_in, "fasta")}
prot_aligned = list(SeqIO.parse(prot_aln, "fasta"))

with cds_out.open("w") as fh:
    for rec in prot_aligned:
        raw = cds.get(rec.id)
        if raw is None:
            print(f"WARN: no CDS for {rec.id}")
            continue
        aligned_aa = str(rec.seq)
        codons = []
        i = 0
        for aa in aligned_aa:
            if aa == "-":
                codons.append("---")
            else:
                if i + 3 <= len(raw):
                    codons.append(raw[i:i + 3])
                    i += 3
                else:
                    codons.append("---")
        codon_seq = "".join(codons)
        fh.write(f">{rec.id}\n")
        for j in range(0, len(codon_seq), 60):
            fh.write(codon_seq[j:j+60] + "\n")
print(f"codon alignment -> {cds_out}")
PY

  echo "Computing alignment stats..."
  "${PY}" - <<PY
from pathlib import Path
from Bio import SeqIO
from collections import Counter
gene = "${GENE}"
root = Path("${ROOT}")
out  = root / "outputs" / f"alignment_stats_{gene}.txt"
prot_aln = list(SeqIO.parse(root / f"data/alignments/{gene}_protein.fasta", "fasta"))
codon_aln = list(SeqIO.parse(root / f"data/alignments/{gene}_codon.fasta",   "fasta"))

prot_len = len(prot_aln[0].seq) if prot_aln else 0
total_cells = prot_len * len(prot_aln)
gap_cells = sum(str(r.seq).count("-") for r in prot_aln)
gap_pct   = 100 * gap_cells / total_cells if total_cells else 0.0

# conserved columns: columns where ≥80% of seqs share same (non-gap) aa
cons = 0
for col in range(prot_len):
    column = [str(r.seq)[col] for r in prot_aln]
    nongap = [c for c in column if c != "-"]
    if not nongap:
        continue
    cnt = Counter(nongap)
    top_aa, top_n = cnt.most_common(1)[0]
    if top_n / len(prot_aln) >= 0.8:
        cons += 1

lines = [
    f"Gene: {gene}",
    f"Sequences in alignment: {len(prot_aln)}",
    f"Alignment length (aa): {prot_len}",
    f"Codon alignment length (nt): {len(codon_aln[0].seq) if codon_aln else 0}",
    f"Overall gap fraction (%): {gap_pct:.2f}",
    f"Conserved columns (>=80% identity): {cons} / {prot_len}",
]
out.write_text("\n".join(lines) + "\n")
for l in lines: print(l)
PY

  echo "=== DONE ==="
} 2>&1 | tee -a "${LOG}"
