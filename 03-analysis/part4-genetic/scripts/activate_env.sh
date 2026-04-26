#!/bin/bash
# Activate the sweet-trap bioinformatics environment.
# Source this before running any Part 4 or Part 3 scripts:
#   source /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part4-genetic/scripts/activate_env.sh
#
# Provides on PATH: codeml, mafft, iqtree, raxml, hmmer, muscle, orthofinder (PAML 4.10.10 etc.)

export SWEET_TRAP_ROOT="/Users/andy/Desktop/Research/sweet-trap-multidomain"
export PATH="$SWEET_TRAP_ROOT/tools/mamba-root/envs/sweet-trap/bin:$SWEET_TRAP_ROOT/tools/bin:$PATH"
export CONDA_PREFIX="$SWEET_TRAP_ROOT/tools/mamba-root/envs/sweet-trap"

# Sanity check
if command -v codeml >/dev/null 2>&1; then
  echo "[env] sweet-trap activated. codeml: $(command -v codeml)"
else
  echo "[env] ERROR: codeml not found after activation." >&2
  return 1 2>/dev/null || exit 1
fi
