#!/usr/bin/env python3
"""
04_domain_topology_scan.py
==========================

Scans every protein in data/raw_protein/ for InterPro / Pfam domains relevant
to the H4b convergent-architecture test:

  - GPCR class-A 7TM (Pfam PF00001 / InterPro IPR000276, and PF00002, PF00003)
  - Venus flytrap / metabotropic receptor ligand-binding module (Pfam PF01094
    / InterPro IPR001828 / IPR000337 -- the TAS1R-family LBD)
  - 7TM Class C (PF00003) for TAS1R context
  - Insect gustatory receptor family (PF06151 — 7tm_6)

Strategy: submit each protein to the EBI InterProScan REST API
(https://www.ebi.ac.uk/Tools/services/rest/iprscan5/), poll, parse, tabulate.

Output:
  outputs/domain_topology.csv  — one row per (protein, domain hit)
  outputs/domain_architecture_summary.csv — one row per protein with the
    ordered domain string (e.g. "7tm_1;ANF_receptor;NCD3G").
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
import time
from pathlib import Path

import requests
from Bio import SeqIO

PROJECT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
PROTS = PROJECT / "data" / "raw_protein"
OUT_HITS = PROJECT / "outputs" / "domain_topology.csv"
OUT_ARCH = PROJECT / "outputs" / "domain_architecture_summary.csv"
LOGS = PROJECT / "logs"

IPR_BASE = "https://www.ebi.ac.uk/Tools/services/rest/iprscan5"
EMAIL = "26708155@alu.cqu.edu.cn"

# Domains of interest (Pfam accession -> friendly tag).  The scan returns all
# Pfam hits; we annotate a "functional module" column for the ones relevant to
# Part 3 and leave others with module="other".
FOCUS_DOMAINS = {
    "PF00001": "GPCR_ClassA_7TM",
    "PF00002": "GPCR_ClassB_7TM",
    "PF00003": "GPCR_ClassC_7TM",
    "PF01094": "ANF_VenusFlytrap_LBD",        # IPR001828
    "PF00003": "GPCR_ClassC_7TM",
    "PF07654": "Ig_like",                      # irrelevant but helps debug
    "PF06151": "Insect_7TM_Gr_family",
    "PF10320": "NCD3G",                        # TAS1R cysteine-rich linker
    "PF13853": "7tm_GPCR_chemosensory",
}


def setup_logging() -> logging.Logger:
    LOGS.mkdir(parents=True, exist_ok=True)
    log = logging.getLogger("domain")
    log.setLevel(logging.INFO)
    log.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s",
                            "%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(LOGS / "04_domain_scan.log", mode="w"); fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout); sh.setFormatter(fmt)
    log.addHandler(fh); log.addHandler(sh)
    return log


def submit_job(sequence: str, name: str, log: logging.Logger) -> str | None:
    # EBI InterProScan5 REST expects specific PascalCase names; "Pfam" alone
    # is invalid — the correct value is "PfamA". See
    # https://www.ebi.ac.uk/Tools/services/rest/iprscan5/parameterdetails/appl
    data = {
        "email": EMAIL,
        "stype": "p",
        "title": name,
        "sequence": sequence,
        "appl": "PfamA,Gene3d,Panther,SuperFamily,SMART",
    }
    r = requests.post(f"{IPR_BASE}/run/", data=data, timeout=30)
    if r.status_code != 200:
        log.warning("submit failed %s: %s %s", name, r.status_code, r.text[:100])
        return None
    return r.text.strip()


def poll_job(job_id: str, log: logging.Logger, max_wait: int = 600) -> str | None:
    """Wait for 'FINISHED'. Return status."""
    t0 = time.time()
    while time.time() - t0 < max_wait:
        r = requests.get(f"{IPR_BASE}/status/{job_id}", timeout=20)
        if r.status_code != 200:
            log.warning("status fail %s: %s", job_id, r.status_code)
            time.sleep(10)
            continue
        status = r.text.strip()
        if status in ("FINISHED", "ERROR", "FAILURE", "NOT_FOUND"):
            return status
        time.sleep(8)
    return "TIMEOUT"


def fetch_result(job_id: str, log: logging.Logger) -> dict | None:
    r = requests.get(f"{IPR_BASE}/result/{job_id}/json", timeout=30)
    if r.status_code != 200:
        log.warning("result fetch fail %s: %s", job_id, r.status_code)
        return None
    try:
        return r.json()
    except Exception as exc:
        log.warning("json decode fail %s: %s", job_id, exc)
        return None


def parse_ipr_json(data: dict) -> list[dict]:
    """Flatten results into {database, accession, name, start, end, evalue}."""
    hits = []
    for res in data.get("results", []):
        for match in res.get("matches", []):
            sig = match.get("signature", {})
            db = sig.get("signatureLibraryRelease", {}).get("library") or sig.get("signatureDatabase") or "?"
            acc = sig.get("accession", "")
            name = sig.get("name") or sig.get("description") or ""
            entry = sig.get("entry") or {}
            ipr_acc = entry.get("accession") if entry else ""
            ipr_name = entry.get("name") if entry else ""
            for loc in match.get("locations", []):
                hits.append(dict(
                    database=db,
                    accession=acc,
                    name=name,
                    interpro=ipr_acc or "",
                    interpro_name=ipr_name or "",
                    start=loc.get("start"),
                    end=loc.get("end"),
                    evalue=loc.get("evalue", ""),
                ))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--concurrency", type=int, default=2,
                    help="max concurrent InterProScan jobs (polite default 2)")
    ap.add_argument("--limit", type=int, default=0,
                    help="process only first N files (0 = all)")
    ap.add_argument("--resume", action="store_true",
                    help="skip proteins already present in domain_topology.csv")
    args = ap.parse_args()

    log = setup_logging()
    OUT_HITS.parent.mkdir(parents=True, exist_ok=True)

    # Resume bookkeeping
    done_names: set[str] = set()
    existing_rows: list[dict] = []
    if args.resume and OUT_HITS.exists():
        with OUT_HITS.open() as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                existing_rows.append(row)
                done_names.add(row["protein"])
        log.info("resume: %d proteins already scanned", len(done_names))

    files = sorted(PROTS.glob("*.fa"))
    if args.limit:
        files = files[:args.limit]

    all_hits: list[dict] = list(existing_rows)

    # Queue-based submission keeping at most `concurrency` jobs live
    active: list[tuple[str, Path]] = []  # (job_id, file)

    def drain_one():
        job, f = active.pop(0)
        status = poll_job(job, log)
        log.info("  [%s] status=%s", f.name, status)
        if status == "FINISHED":
            data = fetch_result(job, log)
            if data is not None:
                hits = parse_ipr_json(data)
                for h in hits:
                    h["protein"] = f.stem
                    all_hits.append(h)
                log.info("    %d hits", len(hits))

    for f in files:
        pname = f.stem
        if pname in done_names:
            continue
        rec = next(SeqIO.parse(f, "fasta"))
        seq = str(rec.seq).rstrip("*")
        if len(seq) < 30:
            log.info("  skip %s (too short)", f.name)
            continue
        job = submit_job(seq, pname, log)
        if not job:
            continue
        log.info("submitted %s -> %s", pname, job)
        active.append((job, f))
        while len(active) >= args.concurrency:
            drain_one()
        time.sleep(1.0)

    while active:
        drain_one()

    # Write detailed hits
    keys = ["protein", "database", "accession", "name", "interpro",
            "interpro_name", "start", "end", "evalue"]
    with OUT_HITS.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for h in all_hits:
            # fill missing keys (existing rows from resume may have different schema)
            out = {k: h.get(k, "") for k in keys}
            w.writerow(out)
    log.info("wrote %d domain-hit rows -> %s", len(all_hits), OUT_HITS)

    # Summarise per protein: ordered Pfam list + focus-domain flags
    per_prot: dict[str, list[dict]] = {}
    for h in all_hits:
        per_prot.setdefault(h["protein"], []).append(h)

    summary_rows = []
    for prot, hits in per_prot.items():
        # pfam hits sorted by start
        pfam_hits = [h for h in hits if h.get("database") == "PFAM" or
                     (isinstance(h.get("accession", ""), str) and h["accession"].startswith("PF"))]
        try:
            pfam_hits.sort(key=lambda x: int(x.get("start") or 0))
        except Exception:
            pass
        arch = ";".join(
            f"{h.get('name', '')}({h.get('accession', '')})" for h in pfam_hits
        )
        focus_flags = {
            "has_gpcr_classA":     any(h.get("accession") == "PF00001" for h in hits),
            "has_gpcr_classC":     any(h.get("accession") == "PF00003" for h in hits),
            "has_VFT_ANF":         any(h.get("accession") == "PF01094" for h in hits),
            "has_insect_7TM_Gr":   any(h.get("accession") == "PF06151" for h in hits),
            "has_NCD3G":           any(h.get("accession") == "PF10320" for h in hits),
        }
        summary_rows.append(dict(protein=prot, domain_arch_pfam=arch, **focus_flags))

    with OUT_ARCH.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["protein", "domain_arch_pfam",
                                           "has_gpcr_classA", "has_gpcr_classC",
                                           "has_VFT_ANF", "has_insect_7TM_Gr",
                                           "has_NCD3G"])
        w.writeheader()
        for r in summary_rows:
            w.writerow(r)
    log.info("wrote %d architecture summary rows -> %s", len(summary_rows), OUT_ARCH)

    return 0


if __name__ == "__main__":
    sys.exit(main())
