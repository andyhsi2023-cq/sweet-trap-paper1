#!/usr/bin/env python3
"""
01_fetch_orthologs.py
=====================

Fetches coding sequences (CDS) + translated protein for the receptor families
needed by Part 3 (H4a within-phylum conservation + H4b cross-phylum
convergence). Covers four lineages:

- Chordata   : TAS1R1/2/3, DRD1, DRD2  x 6 species
- Arthropoda : Gr5a, Gr64a-f, Dop1R1, Dop2R  x 6 species
- Mollusca   : dopamine-receptor homologues x 4 species
- Cnidaria   : dopamine-like Class-A GPCRs  x 3 species

Strategy
--------
1. Vertebrates: Ensembl REST lookup/symbol + sequence/id (canonical transcript CDS).
2. Arthropods + Mollusca + Cnidaria: NCBI Entrez (Biopython) — gene search,
   then fetch the representative mRNA's CDS feature.
3. All successes written to
   data/raw_cds/<gene>_<species_short>.fa  with header
       >gene|species|accession
   and matching protein sequence to data/raw_protein/.
4. Failures logged as [NOT_FOUND] rows in outputs/ortholog_inventory.csv.

No accession numbers are fabricated. If a search returns zero hits, the row is
marked NOT_FOUND and the pipeline moves on.

Usage
-----
    venv-phylo/bin/python scripts/01_fetch_orthologs.py [--limit GENE] [--dry-run]

Environment
-----------
Requires Biopython and `requests`. Set email in constant below (NCBI policy).
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import requests
from Bio import Entrez, SeqIO
from Bio.Seq import Seq


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
RAW_CDS = PROJECT_ROOT / "data" / "raw_cds"
RAW_PROT = PROJECT_ROOT / "data" / "raw_protein"
OUTPUTS = PROJECT_ROOT / "outputs"
LOGS = PROJECT_ROOT / "logs"
INVENTORY_CSV = OUTPUTS / "ortholog_inventory.csv"

EMAIL = "26708155@alu.cqu.edu.cn"  # NCBI Entrez requirement
ENTREZ_API_KEY = os.environ.get("NCBI_API_KEY", "")  # optional

ENSEMBL_BASE = "https://rest.ensembl.org"
NCBI_SLEEP = 0.34  # 3 req/s courtesy limit without API key


# ---------------------------------------------------------------------------
# Species x gene matrix
# ---------------------------------------------------------------------------

# Vertebrates — use Ensembl REST
VERT_SPECIES = {
    "Homo sapiens": "homo_sapiens",
    "Mus musculus": "mus_musculus",
    "Rattus norvegicus": "rattus_norvegicus",
    "Gallus gallus": "gallus_gallus",
    "Xenopus tropicalis": "xenopus_tropicalis",
    "Danio rerio": "danio_rerio",
}
VERT_GENES = ["TAS1R1", "TAS1R2", "TAS1R3", "DRD1", "DRD2"]

# Arthropods — use NCBI Entrez (Ensembl Metazoa REST coverage is patchy for Gr)
ARTHRO_SPECIES = [
    "Drosophila melanogaster",
    "Apis mellifera",
    "Tribolium castaneum",
    "Aedes aegypti",
    "Manduca sexta",
    "Bombyx mori",
]
# Symbol variants to try, in preference order
ARTHRO_GENES = {
    "Gr5a":   ["Gr5a", "gustatory receptor 5a"],
    "Gr64a":  ["Gr64a", "gustatory receptor 64a"],
    "Gr64b":  ["Gr64b", "gustatory receptor 64b"],
    "Gr64c":  ["Gr64c", "gustatory receptor 64c"],
    "Gr64d":  ["Gr64d", "gustatory receptor 64d"],
    "Gr64e":  ["Gr64e", "gustatory receptor 64e"],
    "Gr64f":  ["Gr64f", "gustatory receptor 64f"],
    "DopR1":  ["Dop1R1", "DopR1", "dumb", "dopamine receptor 1"],
    "DopR2":  ["Dop2R", "DopR2", "dopamine receptor 2"],
}

# Mollusca — dopamine receptor homologues
MOLLUSC_SPECIES = [
    "Aplysia californica",
    "Octopus bimaculoides",
    "Lottia gigantea",
    "Crassostrea gigas",
]
MOLLUSC_QUERIES = {
    "DopR": ["dopamine receptor"],
}

# Cnidaria — dopamine-like Class-A GPCRs (annotation sparse)
CNID_SPECIES = [
    "Nematostella vectensis",
    "Hydra vulgaris",
    "Acropora digitifera",
]
CNID_QUERIES = {
    "DopR": ["dopamine receptor", "biogenic amine receptor"],
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class OrthologRecord:
    gene: str
    species: str
    lineage: str
    source: str = ""
    accession: str = ""
    cds_length: int = 0
    protein_length: int = 0
    fetched: str = "N"
    note: str = ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def species_short(name: str) -> str:
    parts = name.replace(" ", "_").split("_")
    if len(parts) >= 2:
        return (parts[0][0] + parts[1]).lower()
    return name.lower().replace(" ", "_")


def slug_path(base: Path, gene: str, species: str, ext: str) -> Path:
    return base / f"{gene}_{species_short(species)}.{ext}"


def write_fasta(path: Path, header: str, seq: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fh:
        fh.write(f">{header}\n")
        # wrap 60 cols
        for i in range(0, len(seq), 60):
            fh.write(seq[i:i + 60] + "\n")


def translate_cds(cds: str) -> str:
    """Translate CDS; trim trailing Ns; stop at first premature stop."""
    seq = cds.upper().replace("U", "T")
    seq = re.sub(r"[^ACGT]", "N", seq)
    pad = (3 - len(seq) % 3) % 3
    seq += "N" * pad
    aa = str(Seq(seq).translate(to_stop=False))
    # drop terminal stop
    if aa.endswith("*"):
        aa = aa[:-1]
    return aa


# ---------------------------------------------------------------------------
# Ensembl vertebrate fetcher
# ---------------------------------------------------------------------------

class EnsemblFetcher:
    def __init__(self, log: logging.Logger):
        self.log = log
        self.sess = requests.Session()
        self.sess.headers.update({"Content-Type": "application/json",
                                  "Accept": "application/json"})

    def _get(self, endpoint: str, params: dict | None = None) -> dict | list | None:
        url = f"{ENSEMBL_BASE}{endpoint}"
        for attempt in range(4):
            try:
                r = self.sess.get(url, params=params or {}, timeout=30)
            except requests.RequestException as exc:
                self.log.warning("Ensembl transient error %s (try %d): %s", url, attempt, exc)
                time.sleep(2 ** attempt)
                continue
            if r.status_code == 429:
                retry = int(r.headers.get("Retry-After", "2"))
                time.sleep(retry + 0.5)
                continue
            if r.status_code >= 500:
                time.sleep(2 ** attempt)
                continue
            if r.status_code == 400 or r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json()
        return None

    def lookup_symbol(self, species: str, symbol: str) -> dict | None:
        return self._get(f"/lookup/symbol/{species}/{symbol}", {"expand": 0})

    def canonical_transcript(self, gene_id: str) -> str | None:
        data = self._get(f"/lookup/id/{gene_id}", {"expand": 1})
        if not data:
            return None
        return data.get("canonical_transcript") or data.get("Transcript", [{}])[0].get("id")

    def sequence_cds(self, transcript_id: str) -> str | None:
        # strip version suffix for sequence endpoint
        tid = transcript_id.split(".")[0]
        r = self.sess.get(
            f"{ENSEMBL_BASE}/sequence/id/{tid}",
            params={"type": "cds"},
            headers={"Content-Type": "text/plain"},
            timeout=30,
        )
        if r.status_code == 200 and r.text.strip():
            return r.text.strip()
        return None

    def sequence_protein(self, transcript_id: str) -> str | None:
        tid = transcript_id.split(".")[0]
        r = self.sess.get(
            f"{ENSEMBL_BASE}/sequence/id/{tid}",
            params={"type": "protein"},
            headers={"Content-Type": "text/plain"},
            timeout=30,
        )
        if r.status_code == 200 and r.text.strip():
            return r.text.strip()
        return None

    def homology_orthologs(self, gene_id: str, target_species: str) -> str | None:
        """Given a human (or any) Ensembl gene ID, return the target-species
        ortholog's gene ID via /homology/id/."""
        data = self._get(
            f"/homology/id/{gene_id.split('.')[0]}",
            {"target_species": target_species, "type": "orthologues",
             "sequence": "none"},
        )
        if not data or "data" not in data or not data["data"]:
            return None
        homs = data["data"][0].get("homologies", [])
        # prefer one-to-one
        for kind in ("ortholog_one2one", "ortholog_one2many",
                     "ortholog_many2many"):
            for h in homs:
                if h.get("type") == kind:
                    return h["target"]["id"]
        # fallback: any
        if homs:
            return homs[0]["target"]["id"]
        return None


def fetch_vertebrate(
    gene: str,
    species_display: str,
    species_slug: str,
    fetcher: EnsemblFetcher,
    log: logging.Logger,
    human_gene_id: str | None = None,
) -> OrthologRecord:
    """Pull a vertebrate ortholog from Ensembl.

    Strategy: (1) direct symbol lookup; if that fails and we have a human
    Ensembl gene ID for the same gene, (2) homology/id to fetch the target
    species ortholog ID.
    """
    rec = OrthologRecord(gene=gene, species=species_display, lineage="Chordata",
                         source="Ensembl")
    gene_id = None
    via = "symbol"
    lookup = fetcher.lookup_symbol(species_slug, gene)
    if lookup:
        gene_id = lookup.get("id")
        tx = lookup.get("canonical_transcript")
    else:
        tx = None

    if not gene_id and human_gene_id and species_slug != "homo_sapiens":
        gene_id = fetcher.homology_orthologs(human_gene_id, species_slug)
        tx = None
        via = "homology"

    if not gene_id:
        rec.note = "ensembl: no symbol and no homology ortholog"
        return rec

    if not tx:
        tx = fetcher.canonical_transcript(gene_id)
    if not tx:
        rec.note = f"gene {gene_id} via {via}: no canonical transcript"
        return rec

    cds = fetcher.sequence_cds(tx)
    prot = fetcher.sequence_protein(tx)
    if not cds or not prot:
        rec.note = f"{tx} via {via}: CDS or protein fetch failed"
        return rec

    rec.accession = tx
    rec.cds_length = len(cds)
    rec.protein_length = len(prot)
    rec.fetched = "Y"
    rec.note = f"via={via}; gene_id={gene_id}"

    cds_path = slug_path(RAW_CDS, gene, species_display, "fa")
    prot_path = slug_path(RAW_PROT, gene, species_display, "fa")
    header = f"{gene}|{species_display.replace(' ', '_')}|{tx}"
    write_fasta(cds_path, header, cds)
    write_fasta(prot_path, header, prot)
    log.info("  [OK] %s %s -> %s (%s; CDS %d, AA %d)", gene, species_display,
             tx, via, len(cds), len(prot))
    return rec


# ---------------------------------------------------------------------------
# NCBI Entrez invertebrate fetcher
# ---------------------------------------------------------------------------

def entrez_search_gene(symbol_variants: list[str], species: str,
                       log: logging.Logger,
                       already_used: set[str] | None = None) -> str | None:
    """Search NCBI Gene DB for any of the symbol variants in a species.
    Returns a Gene UID that has *not* already been claimed by an earlier
    fetch (prevents Gr5a and Gr64a landing on the same accession).

    Strategy:
      pass 1: strict [Gene Name] match
      pass 2: [Gene Name] + description match
      pass 3: [All Fields] (last resort, logs a warning)
    """
    already_used = already_used or set()

    def _esearch(term: str) -> list[str]:
        try:
            h = Entrez.esearch(db="gene", term=term, retmax=8)
            res = Entrez.read(h); h.close()
        except Exception as exc:
            log.warning("  esearch failed: %s", exc)
            time.sleep(1.0)
            return []
        time.sleep(NCBI_SLEEP)
        return list(res.get("IdList", []))

    # Pass 1 — strict gene name
    for sym in symbol_variants:
        ids = _esearch(f'"{sym}"[Gene Name] AND "{species}"[Organism]')
        for gid in ids:
            if gid not in already_used:
                return gid
    # Pass 2 — gene name OR descriptor
    for sym in symbol_variants:
        term = f'("{sym}"[Gene Name] OR "{sym}"[Gene/Protein Name]) AND "{species}"[Organism]'
        ids = _esearch(term)
        for gid in ids:
            if gid not in already_used:
                return gid
    # Pass 3 — loose (last resort, warn)
    for sym in symbol_variants:
        term = f'("{sym}"[All Fields]) AND "{species}"[Organism] AND gene[Filter]'
        ids = _esearch(term)
        for gid in ids:
            if gid not in already_used:
                log.warning("  [loose match] %s %s -> gene_uid=%s", species, sym, gid)
                return gid
    return None


def entrez_gene_to_refseq(gene_uid: str, log: logging.Logger) -> tuple[str | None, str | None]:
    """Return (refseq mRNA accession, refseq protein accession) for a Gene UID.
    Falls back to nuccore link if refseq_rna empty."""
    # elink Gene -> Nucleotide RefSeq RNA
    try:
        h = Entrez.elink(dbfrom="gene", db="nuccore", id=gene_uid,
                         linkname="gene_nuccore_refseqrna")
        res = Entrez.read(h); h.close()
        time.sleep(NCBI_SLEEP)
    except Exception as exc:
        log.warning("  elink refseq_rna failed %s: %s", gene_uid, exc)
        return None, None

    mrna_ids: list[str] = []
    for link_set in res:
        for db in link_set.get("LinkSetDb", []):
            for link in db.get("Link", []):
                mrna_ids.append(link["Id"])

    # Fallback: generic nuccore
    if not mrna_ids:
        try:
            h = Entrez.elink(dbfrom="gene", db="nuccore", id=gene_uid)
            res = Entrez.read(h); h.close()
            time.sleep(NCBI_SLEEP)
            for link_set in res:
                for db in link_set.get("LinkSetDb", []):
                    if db.get("LinkName") in ("gene_nuccore_refseqrna",
                                              "gene_nuccore_refseqmrna",
                                              "gene_nuccore",
                                              "gene_nuccore_pos"):
                        for link in db.get("Link", []):
                            mrna_ids.append(link["Id"])
        except Exception as exc:
            log.warning("  elink fallback failed %s: %s", gene_uid, exc)
            return None, None

    if not mrna_ids:
        return None, None

    # Pick the first one and fetch summary to get accession
    try:
        h = Entrez.esummary(db="nuccore", id=",".join(mrna_ids[:5]))
        sums = Entrez.read(h); h.close()
        time.sleep(NCBI_SLEEP)
    except Exception as exc:
        log.warning("  esummary nuccore failed: %s", exc)
        return None, None

    # Prefer RefSeq (NM_/XM_) over others
    best = None
    for entry in sums:
        acc = entry.get("AccessionVersion") or entry.get("Caption")
        if acc and (acc.startswith("NM_") or acc.startswith("XM_")):
            best = acc
            break
    if not best:
        best = sums[0].get("AccessionVersion") or sums[0].get("Caption")
    return best, None  # protein acc resolved later from CDS feature


def entrez_fetch_cds_and_protein(acc: str, log: logging.Logger) -> tuple[str | None, str | None, str | None]:
    """Given a nucleotide accession, return (cds_seq, protein_seq, protein_acc)
    by pulling the GenBank record and extracting the CDS feature."""
    try:
        h = Entrez.efetch(db="nuccore", id=acc, rettype="gb", retmode="text")
        rec = SeqIO.read(h, "genbank"); h.close()
        time.sleep(NCBI_SLEEP)
    except Exception as exc:
        log.warning("  efetch gb %s failed: %s", acc, exc)
        return None, None, None

    cds_feats = [f for f in rec.features if f.type == "CDS"]
    if not cds_feats:
        return None, None, None
    f = cds_feats[0]
    try:
        cds_seq = str(f.extract(rec.seq))
    except Exception as exc:
        log.warning("  CDS extract %s failed: %s", acc, exc)
        return None, None, None
    protein_acc = None
    protein_seq = None
    if "protein_id" in f.qualifiers:
        protein_acc = f.qualifiers["protein_id"][0]
    if "translation" in f.qualifiers:
        protein_seq = f.qualifiers["translation"][0].replace(" ", "").replace("\n", "")
    return cds_seq, protein_seq, protein_acc


def fetch_invertebrate(
    gene: str,
    symbol_variants: list[str],
    species: str,
    lineage: str,
    log: logging.Logger,
    claimed_uids: set[str] | None = None,
) -> OrthologRecord:
    rec = OrthologRecord(gene=gene, species=species, lineage=lineage,
                         source="NCBI Entrez")
    gene_uid = entrez_search_gene(symbol_variants, species, log,
                                  already_used=claimed_uids)
    if not gene_uid:
        rec.note = "esearch gene: no hits"
        return rec
    if claimed_uids is not None:
        claimed_uids.add(gene_uid)
    nacc, _ = entrez_gene_to_refseq(gene_uid, log)
    if not nacc:
        rec.note = f"gene {gene_uid}: no nuccore link"
        return rec
    cds, prot, pacc = entrez_fetch_cds_and_protein(nacc, log)
    if not cds or not prot:
        rec.note = f"{nacc}: CDS feature extraction failed"
        return rec

    rec.accession = nacc
    rec.cds_length = len(cds)
    rec.protein_length = len(prot)
    rec.fetched = "Y"
    rec.note = f"gene_uid={gene_uid}; protein={pacc or '-'}"

    cds_path = slug_path(RAW_CDS, gene, species, "fa")
    prot_path = slug_path(RAW_PROT, gene, species, "fa")
    header = f"{gene}|{species.replace(' ', '_')}|{nacc}"
    write_fasta(cds_path, header, cds)
    write_fasta(prot_path, header, prot)
    log.info("  [OK] %s %s -> %s (CDS %d, AA %d)", gene, species, nacc,
             len(cds), len(prot))
    return rec


# ---------------------------------------------------------------------------
# Mollusc / cnidarian dopamine hunter (keyword-based, multi-hit retrieval)
# ---------------------------------------------------------------------------

def fetch_dopamine_homologs(gene_label: str, queries: list[str], species: str,
                            lineage: str, log: logging.Logger,
                            max_hits: int = 3) -> list[OrthologRecord]:
    """For sparsely-annotated lineages, search mRNA directly with keyword terms
    and pull the top N hits. Each hit becomes its own OrthologRecord with
    numbered gene label (DopR_1, DopR_2 ...)."""
    records: list[OrthologRecord] = []

    all_nuc_ids: list[str] = []
    for q in queries:
        # mRNA / complete-cds search in nuccore
        term = f'("{species}"[Organism] AND ({q}[Title]) AND (mRNA[Filter] OR complete cds[Title]))'
        try:
            h = Entrez.esearch(db="nuccore", term=term, retmax=10)
            res = Entrez.read(h); h.close()
            time.sleep(NCBI_SLEEP)
        except Exception as exc:
            log.warning("  esearch nuccore failed %s %s: %s", species, q, exc)
            continue
        ids = res.get("IdList", [])
        all_nuc_ids.extend(ids)
        if len(all_nuc_ids) >= max_hits:
            break

    if not all_nuc_ids:
        # fall back: any nuccore hit regardless of Title filter
        term = f'"{species}"[Organism] AND ("dopamine receptor"[All Fields] OR "biogenic amine receptor"[All Fields])'
        try:
            h = Entrez.esearch(db="nuccore", term=term, retmax=5)
            res = Entrez.read(h); h.close()
            time.sleep(NCBI_SLEEP)
            all_nuc_ids = res.get("IdList", [])
        except Exception as exc:
            log.warning("  fallback esearch failed %s: %s", species, exc)

    if not all_nuc_ids:
        rec = OrthologRecord(gene=gene_label, species=species, lineage=lineage,
                             source="NCBI Entrez",
                             note="no dopamine/biogenic-amine mRNA found")
        records.append(rec)
        return records

    # Deduplicate in order
    seen = set(); unique = []
    for i in all_nuc_ids:
        if i not in seen:
            seen.add(i); unique.append(i)
    unique = unique[:max_hits]

    for idx, nid in enumerate(unique, start=1):
        # resolve accession
        try:
            h = Entrez.esummary(db="nuccore", id=nid)
            sums = Entrez.read(h); h.close()
            time.sleep(NCBI_SLEEP)
            acc = sums[0].get("AccessionVersion") or sums[0].get("Caption")
        except Exception as exc:
            log.warning("  esummary %s failed: %s", nid, exc)
            continue
        cds, prot, pacc = entrez_fetch_cds_and_protein(acc, log)
        label = f"{gene_label}_{idx}"
        rec = OrthologRecord(gene=label, species=species, lineage=lineage,
                             source="NCBI Entrez", accession=acc)
        if not cds or not prot:
            rec.note = f"{acc}: no CDS extractable"
            records.append(rec)
            continue
        rec.cds_length = len(cds)
        rec.protein_length = len(prot)
        rec.fetched = "Y"
        rec.note = f"protein={pacc or '-'}"

        cds_path = slug_path(RAW_CDS, label, species, "fa")
        prot_path = slug_path(RAW_PROT, label, species, "fa")
        header = f"{label}|{species.replace(' ', '_')}|{acc}"
        write_fasta(cds_path, header, cds)
        write_fasta(prot_path, header, prot)
        log.info("  [OK] %s %s -> %s (CDS %d, AA %d)", label, species, acc,
                 len(cds), len(prot))
        records.append(rec)

    return records


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    LOGS.mkdir(parents=True, exist_ok=True)
    log_path = LOGS / "01_fetch_orthologs.log"
    logger = logging.getLogger("fetch")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s",
                            "%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(log_path, mode="w"); fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout); sh.setFormatter(fmt)
    logger.addHandler(fh); logger.addHandler(sh)
    return logger


def write_inventory(records: list[OrthologRecord]) -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    with INVENTORY_CSV.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["gene", "species", "lineage", "source", "accession",
                    "cds_length", "protein_length", "fetched", "note"])
        for r in records:
            w.writerow([r.gene, r.species, r.lineage, r.source, r.accession,
                        r.cds_length, r.protein_length, r.fetched, r.note])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-gene", help="only run this gene symbol")
    ap.add_argument("--skip", choices=["vert", "arthro", "mollusc", "cnid"],
                    action="append", default=[],
                    help="skip a lineage (repeat allowed)")
    args = ap.parse_args()

    log = setup_logging()
    Entrez.email = EMAIL
    if ENTREZ_API_KEY:
        Entrez.api_key = ENTREZ_API_KEY

    RAW_CDS.mkdir(parents=True, exist_ok=True)
    RAW_PROT.mkdir(parents=True, exist_ok=True)

    records: list[OrthologRecord] = []

    # -------- Vertebrates (Ensembl) --------
    if "vert" not in args.skip:
        log.info("=== Vertebrate block (Ensembl REST) ===")
        fetcher = EnsemblFetcher(log)
        # Pre-resolve human gene IDs so we can use /homology/id/ as fallback
        human_ids: dict[str, str] = {}
        for gene in VERT_GENES:
            hlookup = fetcher.lookup_symbol("homo_sapiens", gene)
            if hlookup and hlookup.get("id"):
                human_ids[gene] = hlookup["id"]
                log.info("  [vert-index] %s = %s", gene, hlookup["id"])
        for gene in VERT_GENES:
            if args.limit_gene and gene != args.limit_gene:
                continue
            hgid = human_ids.get(gene)
            for sp_display, sp_slug in VERT_SPECIES.items():
                log.info("[vert] %s / %s", gene, sp_display)
                try:
                    rec = fetch_vertebrate(gene, sp_display, sp_slug, fetcher,
                                           log, human_gene_id=hgid)
                except Exception as exc:
                    log.exception("  unhandled error: %s", exc)
                    rec = OrthologRecord(gene=gene, species=sp_display,
                                         lineage="Chordata", source="Ensembl",
                                         note=f"exception:{exc}")
                records.append(rec)
                time.sleep(0.2)

    # -------- Arthropods (NCBI Entrez) --------
    if "arthro" not in args.skip:
        log.info("=== Arthropod block (NCBI Entrez) ===")
        # Within a species, track which gene_uids have already been claimed
        # so Gr5a, Gr64a, Gr64b... cannot collapse onto the same accession.
        for sp in ARTHRO_SPECIES:
            claimed: set[str] = set()
            for gene_label, symbols in ARTHRO_GENES.items():
                if args.limit_gene and gene_label != args.limit_gene:
                    continue
                log.info("[arthro] %s / %s", gene_label, sp)
                try:
                    rec = fetch_invertebrate(gene_label, symbols, sp,
                                             "Arthropoda", log,
                                             claimed_uids=claimed)
                except Exception as exc:
                    log.exception("  unhandled error: %s", exc)
                    rec = OrthologRecord(gene=gene_label, species=sp,
                                         lineage="Arthropoda", source="NCBI Entrez",
                                         note=f"exception:{exc}")
                records.append(rec)

    # -------- Mollusca (keyword dopamine search) --------
    if "mollusc" not in args.skip:
        log.info("=== Mollusc block (NCBI keyword search) ===")
        for sp in MOLLUSC_SPECIES:
            for gene_label, queries in MOLLUSC_QUERIES.items():
                if args.limit_gene and not gene_label.startswith(args.limit_gene):
                    continue
                log.info("[mollusc] %s / %s", gene_label, sp)
                try:
                    new = fetch_dopamine_homologs(gene_label, queries, sp,
                                                  "Mollusca", log, max_hits=3)
                except Exception as exc:
                    log.exception("  unhandled error: %s", exc)
                    new = [OrthologRecord(gene=gene_label, species=sp,
                                          lineage="Mollusca",
                                          source="NCBI Entrez",
                                          note=f"exception:{exc}")]
                records.extend(new)

    # -------- Cnidaria --------
    if "cnid" not in args.skip:
        log.info("=== Cnidaria block (NCBI keyword search) ===")
        for sp in CNID_SPECIES:
            for gene_label, queries in CNID_QUERIES.items():
                if args.limit_gene and not gene_label.startswith(args.limit_gene):
                    continue
                log.info("[cnid] %s / %s", gene_label, sp)
                try:
                    new = fetch_dopamine_homologs(gene_label, queries, sp,
                                                  "Cnidaria", log, max_hits=3)
                except Exception as exc:
                    log.exception("  unhandled error: %s", exc)
                    new = [OrthologRecord(gene=gene_label, species=sp,
                                          lineage="Cnidaria",
                                          source="NCBI Entrez",
                                          note=f"exception:{exc}")]
                records.extend(new)

    write_inventory(records)
    nok = sum(1 for r in records if r.fetched == "Y")
    log.info("=== SUMMARY === fetched=%d / total rows=%d", nok, len(records))
    log.info("Inventory -> %s", INVENTORY_CSV)
    return 0


if __name__ == "__main__":
    sys.exit(main())
