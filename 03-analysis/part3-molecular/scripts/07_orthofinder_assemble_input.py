#!/usr/bin/env python3
"""
07_orthofinder_assemble_input.py
================================

Assembles species-specific protein FASTA files for OrthoFinder to
disambiguate the 17 mollusc/cnidarian "DopR" entries in
ortholog_inventory.csv. NCBI keyword "dopamine receptor" returns many
class-A GPCRs that are not true dopamine receptors (serotonin HTR,
octopamine OA, tyramine TAR, adrenergic ADR receptors are all Class-A
GPCRs with PF00001). We anchor the analysis with a vetted set of
vertebrate biogenic-amine receptors, then use OrthoFinder to cluster
the molluscan/cnidarian candidates by true orthology, not keyword.

Inputs
------
- Existing Part 3 protein FASTAs in data/raw_protein/ for DRD1/DRD2 (5
  vertebrates), DopR1/DopR2 (6 arthropods), DopR_1/2/3 (4 mollusca, 3
  cnidaria = 17 targets)
- Fetched via Entrez: vertebrate amine-receptor out-groups
  (DRD3/4/5, HTR1A, HTR2A, HTR1B, ADRA1A, ADRB1) for 3 mammals, plus
  invertebrate reference 5HT/OA/TAR receptors from D. melanogaster and
  A. californica (known curated sequences on NCBI).

Output
------
data/orthofinder_input/<Species_genus>.fa with one record per line
    >accession species=<Species> label=<functional_label>

Each species file is what OrthoFinder expects as a per-species proteome.
"""

from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

from Bio import Entrez, SeqIO

PROJECT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
RAW_PROTS = PROJECT / "data" / "raw_protein"
OUTDIR = PROJECT / "data" / "orthofinder_input"
LOGS = PROJECT / "logs"

Entrez.email = "26708155@alu.cqu.edu.cn"

# Vertebrate amine-receptor anchors (NCBI protein accession, species,
# functional label). Curated GenBank RefSeq entries — we trust the
# canonical symbols here.
VERTEBRATE_ANCHORS = [
    # Homo sapiens
    ("NP_000785.1", "Homo_sapiens", "DRD1"),
    ("NP_000786.1", "Homo_sapiens", "DRD2"),
    ("NP_000787.2", "Homo_sapiens", "DRD3"),
    ("NP_000788.2", "Homo_sapiens", "DRD4"),
    ("NP_000789.1", "Homo_sapiens", "DRD5"),
    ("NP_000515.2", "Homo_sapiens", "HTR1A"),
    ("NP_000612.1", "Homo_sapiens", "HTR2A"),
    ("NP_000854.1", "Homo_sapiens", "HTR1B"),
    ("NP_000671.2", "Homo_sapiens", "ADRA1A"),
    ("NP_000675.1", "Homo_sapiens", "ADRB1"),
    ("NP_000743.1", "Homo_sapiens", "CHRM1"),  # acetylcholine muscarinic, further out-group
    ("NP_000912.1", "Homo_sapiens", "HRH1"),   # histamine H1
    # Mus musculus
    ("NP_034207.2", "Mus_musculus", "DRD1"),
    ("NP_034208.2", "Mus_musculus", "DRD2"),
    ("NP_032334.2", "Mus_musculus", "HTR1A"),
    ("NP_766400.1", "Mus_musculus", "HTR2A"),
    ("NP_038497.1", "Mus_musculus", "ADRA1A"),
    # Rattus norvegicus
    ("NP_036676.1", "Rattus_norvegicus", "DRD1"),
    ("NP_036679.1", "Rattus_norvegicus", "DRD2"),
    ("NP_036826.1", "Rattus_norvegicus", "HTR1A"),
    ("NP_058940.1", "Rattus_norvegicus", "HTR2A"),
    # Gallus gallus
    ("NP_001138692.1", "Gallus_gallus", "DRD1"),
    ("NP_001076242.1", "Gallus_gallus", "DRD2"),
    ("NP_989495.1", "Gallus_gallus", "HTR2A"),
    # Danio rerio
    ("NP_878305.1", "Danio_rerio", "DRD1"),
    ("NP_898891.1", "Danio_rerio", "DRD2A"),
    ("NP_001139238.1", "Danio_rerio", "HTR2A"),
]

# Invertebrate amine-receptor discriminators (curated NCBI RefSeq for
# D. melanogaster; these disambiguate mollusc/cnidarian hits that may
# turn out to be OA/Tyr/5HT receptors rather than true DRD).
INVERT_ANCHORS = [
    # Drosophila melanogaster -- curated GPCRs beyond DopR1/DopR2
    ("NP_001356890.1", "Drosophila_melanogaster", "5HT1A_Dmel"),    # 5-HT1A
    ("NP_730859.1", "Drosophila_melanogaster", "5HT2A_Dmel"),       # 5-HT2A
    ("NP_732089.1", "Drosophila_melanogaster", "5HT7_Dmel"),        # 5-HT7
    ("NP_731254.1", "Drosophila_melanogaster", "OctR_Oamb_Dmel"),   # octopamine OAMB
    ("NP_001303505.1", "Drosophila_melanogaster", "OctB2R_Dmel"),   # Octbeta2R
    ("NP_569905.1", "Drosophila_melanogaster", "TyrR_Dmel"),        # tyramine Tyr receptor
    # Aplysia californica -- has characterised 5HT and OA receptors
    ("NP_001191623.1", "Aplysia_californica", "5HT1Ap_Acal"),        # 5-HT1Aplysia
    ("NP_001191560.1", "Aplysia_californica", "5HT2_Acal"),          # 5-HT2
]

# Target (candidate) species that already have FASTAs in raw_protein.
# We collect all existing entries plus the anchors above into one
# species-level FASTA per species.
SPECIES_TOKEN = {
    # vertebrate
    "hsapiens": "Homo_sapiens",
    "mmusculus": "Mus_musculus",
    "rnorvegicus": "Rattus_norvegicus",
    "ggallus": "Gallus_gallus",
    "xtropicalis": "Xenopus_tropicalis",
    # arthropods (not needed here but kept for completeness if included)
    "dmelanogaster": "Drosophila_melanogaster",
    "amellifera": "Apis_mellifera",
    "tcastaneum": "Tribolium_castaneum",
    "aaegypti": "Aedes_aegypti",
    "msexta": "Manduca_sexta",
    "bmori": "Bombyx_mori",
    # mollusca
    "acalifornica": "Aplysia_californica",
    "obimaculoides": "Octopus_bimaculoides",
    "cgigas": "Crassostrea_gigas",
    # cnidaria
    "nvectensis": "Nematostella_vectensis",
    "hvulgaris": "Hydra_vulgaris",
    "adigitifera": "Acropora_digitifera",
}

# Candidate mollusc/cnidarian + vertebrate DRD entries to include
# (filename prefix -> functional label). Every DopR_* from the target
# phyla + DRD1/DRD2 vertebrates + DopR1/2 arthropods.
CANDIDATE_FILE_GLOBS = [
    ("DRD1_*.fa", "DRD1_candidate"),
    ("DRD2_*.fa", "DRD2_candidate"),
    ("DopR_*.fa", "MollCnid_DopR_candidate"),   # 17 mollusc/cnidaria
    # include insect Dop1R/Dop2R as EXTRA DRD anchors -- they ARE the
    # characterised invertebrate dopamine receptors and anchor the
    # invertebrate amine clade to the DRD side rather than OA/TAR.
    ("DopR1_*.fa", "DopR1_invert_anchor"),
    ("DopR2_*.fa", "DopR2_invert_anchor"),
]


def setup_logging() -> logging.Logger:
    LOGS.mkdir(parents=True, exist_ok=True)
    log = logging.getLogger("of_assemble")
    log.setLevel(logging.INFO)
    log.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(LOGS / "07_orthofinder_assemble.log", mode="w")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout); sh.setFormatter(fmt)
    log.addHandler(fh); log.addHandler(sh)
    return log


def fetch_protein(acc: str, log: logging.Logger, retries: int = 3) -> str | None:
    """Fetch a single protein sequence via Entrez efetch."""
    for attempt in range(retries):
        try:
            h = Entrez.efetch(db="protein", id=acc, rettype="fasta", retmode="text")
            txt = h.read()
            h.close()
            if txt and txt.startswith(">"):
                return txt
            log.warning("empty response for %s (attempt %d)", acc, attempt + 1)
        except Exception as e:
            log.warning("fetch error %s attempt %d: %s", acc, attempt + 1, e)
        time.sleep(2 * (attempt + 1))
    return None


def species_from_fname(fname: str) -> str | None:
    """Take 'DRD1_hsapiens.fa' -> 'Homo_sapiens'."""
    base = fname.rsplit(".", 1)[0]
    parts = base.split("_")
    # The token is always the last underscore-separated piece.
    token = parts[-1]
    return SPECIES_TOKEN.get(token)


def gather_existing(log: logging.Logger) -> dict[str, list[tuple[str, str, str]]]:
    """Return {species: [(accession, label, sequence)]}."""
    buckets: dict[str, list[tuple[str, str, str]]] = {}
    for pattern, default_label in CANDIDATE_FILE_GLOBS:
        for fa in sorted(RAW_PROTS.glob(pattern)):
            species = species_from_fname(fa.name)
            if species is None:
                log.warning("skip (no species token match): %s", fa.name)
                continue
            # label from filename prefix
            prefix = fa.name.split("_")
            # collapse DRD1 / DRD2 / DopR_1 / DopR_2 / DopR_3
            if fa.name.startswith("DRD1"):
                label = "DRD1_candidate"
            elif fa.name.startswith("DRD2"):
                label = "DRD2_candidate"
            elif fa.name.startswith("DopR_"):
                label = f"MollCnid_DopR_{prefix[1]}_candidate"  # DopR_1, 2, 3
            else:
                label = default_label
            recs = list(SeqIO.parse(fa, "fasta"))
            if not recs:
                log.warning("empty fasta: %s", fa.name)
                continue
            for rec in recs:
                # accession is the bit after last "|" in the existing
                # Part 3 headers, or the first token.
                acc = rec.id.split("|")[-1]
                buckets.setdefault(species, []).append((acc, label, str(rec.seq)))
    return buckets


def dedup(recs: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    seen: set[str] = set()
    out = []
    for acc, label, seq in recs:
        if acc in seen:
            continue
        seen.add(acc)
        out.append((acc, label, seq))
    return out


def add_anchors(buckets: dict[str, list[tuple[str, str, str]]], anchors: list[tuple[str, str, str]], log: logging.Logger) -> None:
    for acc, species, label in anchors:
        txt = fetch_protein(acc, log)
        if not txt:
            log.warning("could not fetch anchor %s (%s)", acc, label)
            continue
        # parse the fasta text into (header, seq)
        lines = txt.strip().splitlines()
        seq = "".join(lines[1:]).replace(" ", "")
        buckets.setdefault(species, []).append((acc, label, seq))
        time.sleep(0.34)  # NCBI rate limit


def write_species_fastas(buckets: dict[str, list[tuple[str, str, str]]], log: logging.Logger) -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    # Clean previous output to avoid stale records contaminating OrthoFinder
    for old in OUTDIR.glob("*.fa"):
        old.unlink()
    for species, recs in buckets.items():
        recs = dedup(recs)
        path = OUTDIR / f"{species}.fa"
        with path.open("w") as fh:
            for acc, label, seq in recs:
                # OrthoFinder uses only the first whitespace-delimited
                # token as the identifier; we keep it unique and parse
                # label+species back from the species filename.
                rec_id = f"{acc}__{label}"
                fh.write(f">{rec_id}\n")
                # 60 char lines
                for i in range(0, len(seq), 60):
                    fh.write(seq[i:i + 60] + "\n")
        log.info("wrote %s (n=%d)", path.name, len(recs))


def main() -> int:
    log = setup_logging()
    log.info("gathering existing Part 3 FASTAs")
    buckets = gather_existing(log)

    log.info("fetching vertebrate amine-receptor anchors (n=%d)", len(VERTEBRATE_ANCHORS))
    add_anchors(buckets, VERTEBRATE_ANCHORS, log)

    log.info("fetching invertebrate amine-receptor anchors (n=%d)", len(INVERT_ANCHORS))
    add_anchors(buckets, INVERT_ANCHORS, log)

    log.info("writing species FASTAs to %s", OUTDIR)
    write_species_fastas(buckets, log)

    # summary
    log.info("-- summary --")
    for species in sorted(buckets):
        n = len({acc for acc, _, _ in buckets[species]})
        log.info("  %-25s n=%d", species, n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
