#!/usr/bin/env python3
"""
08_orthofinder_classify.py
==========================

Parses the MCL clusters from OrthoFinder (OrthoFinder_graph.txt -> mcl)
and classifies each sequence into either:

  - TRUE_DRD       (co-clusters with vertebrate DRD1/DRD2/DRD3/DRD4/DRD5)
  - OTHER_AMINE    (co-clusters with HTR / ADR / TAR / OA / CHRM / HRH)
  - UNRESOLVED     (singleton or small cluster with no anchor)

OrthoFinder's default MCL inflation (I=1.2) produces a single
"biogenic-amine" super-cluster on sparse inputs. We therefore re-cluster
the OrthoFinder_graph.txt with higher inflation (I=3.0 and I=5.0) and
compare outcomes. The higher inflation is what teases DRD apart from
HTR / ADR / TAR / OA.

Outputs
-------
- outputs/orthofinder_dop/classification_I{I}.csv  (one row per sequence)
- outputs/orthofinder_dop/orthogroup_labels_I{I}.csv
- outputs/orthofinder_dop/dop_classification_summary.md

We also write a consolidated classification call per mollusc/cnidarian
sequence using the I=3.0 result as the primary decision (reported in
the summary.md).
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/part3-molecular")
OFDIR = PROJECT / "outputs" / "orthofinder_dop"
RESULTS_DIR = next(OFDIR.glob("Results_*"))
WD = RESULTS_DIR / "WorkingDirectory"
SEQID_FILE = WD / "SequenceIDs.txt"

# Anchor classification — we trust these labels as ground truth for
# the orthogroup identity call.
DRD_LABELS = {"DRD1", "DRD2", "DRD3", "DRD4", "DRD5", "DRD2A"}
HTR_LABELS = {"HTR1A", "HTR2A", "HTR1B"}
ADR_LABELS = {"ADRA1A", "ADRB1"}
OA_LABELS = {"OctR_Oamb_Dmel", "OctB2R_Dmel"}
TAR_LABELS = {"TyrR_Dmel"}
CHRM_LABELS = {"CHRM1"}
HRH_LABELS = {"HRH1"}
INVERT_5HT_LABELS = {"5HT1A_Dmel", "5HT2A_Dmel", "5HT7_Dmel",
                     "5HT1Ap_Acal", "5HT2_Acal"}

CANDIDATE_TAG = "MollCnid_DopR"  # substring in candidate labels


def parse_sequence_ids(path: Path) -> dict[str, str]:
    """Return {mcl_flat_id (str(N)): fasta_header_token}.

    OrthoFinder's MCL graph indexes sequences as flat 0-based integers
    matching the 0-based line position in SequenceIDs.txt. The 'N_M'
    labels in SequenceIDs.txt are species_seq indices for internal
    bookkeeping, but the MCL adjacency uses flat integer IDs."""
    mapping: dict[str, str] = {}
    with path.open() as fh:
        for idx, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            # format "N_M: header_token"
            key, val = line.split(": ", 1)
            mapping[str(idx)] = val
    return mapping


def parse_mcl_clusters(cluster_file: Path) -> list[list[str]]:
    """Parse MCL native-interchange output as produced by `mcl -o`.

    Format:
        # cline: ...
        (mclheader ...)
        (mclmatrix
        begin
        0  2 12 14 19 $
        1  3 4 9 17 $
        ...
        )

    We identify the cluster block by (mclmatrix ... begin ... ).
    Each cluster line is `cluster_idx member1 member2 ... $` possibly
    continued across multiple indented lines until `$`. The leading
    cluster_idx is NOT a member — skip it.
    """
    text = cluster_file.read_text()
    return parse_mcl_native(text)


def parse_mcl_native(text: str) -> list[list[str]]:
    clusters: list[list[str]] = []
    in_matrix = False
    pending: list[str] = []
    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not in_matrix:
            if stripped.startswith("(mclmatrix"):
                in_matrix = True
            continue
        # inside (mclmatrix ...) block
        if stripped.startswith("begin"):
            continue
        if stripped.startswith(")"):
            if pending:
                clusters.append(pending)
                pending = []
            in_matrix = False
            continue
        if not stripped:
            continue
        toks = stripped.split()
        finished = False
        filtered = []
        for tok in toks:
            if tok == "$":
                finished = True
                break
            filtered.append(tok)
        # A fresh cluster line begins at column 0 (raw[0] is not space);
        # continuation lines are indented. The first token of a fresh
        # line is the cluster row index (skip it).
        is_new_cluster = (not line.startswith(" ")) and (not line.startswith("\t"))
        if is_new_cluster:
            # If we still have an unfinished pending, flush it defensively
            if pending:
                clusters.append(pending)
                pending = []
            if filtered:
                # drop the leading cluster index
                filtered = filtered[1:]
        pending.extend(filtered)
        if finished:
            clusters.append(pending)
            pending = []
    return clusters


def label_of(header: str) -> str:
    """Extract label (e.g. 'DRD1', 'MollCnid_DopR_1_candidate') from
    the header which has the form accession__label or similar."""
    # Everything after the first '__'
    if "__" in header:
        return header.split("__", 1)[1]
    return header


def classify_cluster(headers: list[str]) -> str:
    """Assign a functional identity to a cluster based on its members."""
    labels = [label_of(h) for h in headers]
    has_drd = any(l in DRD_LABELS for l in labels)
    has_htr = any(l in HTR_LABELS for l in labels)
    has_adr = any(l in ADR_LABELS for l in labels)
    has_oa = any(l in OA_LABELS for l in labels)
    has_tar = any(l in TAR_LABELS for l in labels)
    has_5ht_invert = any(l in INVERT_5HT_LABELS for l in labels)
    has_chrm = any(l in CHRM_LABELS for l in labels)
    has_hrh = any(l in HRH_LABELS for l in labels)

    anchors = [
        ("TRUE_DRD", has_drd),
        ("HTR_serotonin", has_htr or has_5ht_invert),
        ("ADR_adrenergic", has_adr),
        ("OA_octopamine", has_oa),
        ("TAR_tyramine", has_tar),
        ("CHRM_muscarinic", has_chrm),
        ("HRH_histamine", has_hrh),
    ]
    present = [name for name, ok in anchors if ok]
    if len(present) == 1:
        return present[0]
    if len(present) > 1:
        # Ambiguous cluster — under-clustered. Still mark as mixed so
        # downstream knows.
        return "AMBIGUOUS_mixed:" + "+".join(present)
    return "UNRESOLVED_no_anchor"


def run_classification(cluster_file: Path, seqids: dict[str, str], inflation: str) -> list[dict[str, str]]:
    clusters_mcl = parse_mcl_clusters(cluster_file)
    rows = []
    for i, mcl_ids in enumerate(clusters_mcl):
        headers = [seqids.get(mid, f"UNKNOWN:{mid}") for mid in mcl_ids]
        call = classify_cluster(headers)
        for h in headers:
            rows.append({
                "orthogroup": f"OG_I{inflation}_{i:04d}",
                "cluster_size": str(len(headers)),
                "cluster_call": call,
                "sequence_header": h,
                "label": label_of(h),
            })
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def per_orthogroup_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups = defaultdict(list)
    for r in rows:
        groups[r["orthogroup"]].append(r)
    out = []
    for og, members in groups.items():
        labels = Counter(m["label"] for m in members)
        species_tokens = []
        for m in members:
            h = m["sequence_header"]
            # parse species from header — actually not in the header.
            # We'll just report labels (functional label carries enough).
            species_tokens.append(m["label"])
        out.append({
            "orthogroup": og,
            "n_members": str(len(members)),
            "call": members[0]["cluster_call"],
            "label_composition": ";".join(f"{k}:{v}" for k, v in labels.most_common()),
        })
    return out


def write_summary_md(rows_primary: list[dict[str, str]], rows_stringent: list[dict[str, str]], out_path: Path) -> None:
    # Per candidate sequence: primary call + stringent call
    prim = {r["sequence_header"]: r for r in rows_primary}
    strn = {r["sequence_header"]: r for r in rows_stringent}
    cand_headers = sorted(
        [h for h in prim if CANDIDATE_TAG in h],
        key=lambda x: (x.split("__")[1], x),
    )
    lines = []
    lines.append("# OrthoFinder classification of mollusc/cnidarian DopR candidates\n")
    lines.append("Primary inflation: I=3.0  |  Stringent: I=5.0\n")
    lines.append("")
    lines.append("| candidate header | I=3.0 call | I=5.0 call | I=3.0 cluster size | I=5.0 cluster size |")
    lines.append("|---|---|---|---|---|")
    for h in cand_headers:
        p = prim.get(h, {"cluster_call": "NA", "cluster_size": "NA"})
        s = strn.get(h, {"cluster_call": "NA", "cluster_size": "NA"})
        lines.append(f"| {h} | {p['cluster_call']} | {s['cluster_call']} | {p['cluster_size']} | {s['cluster_size']} |")
    # Summary counts
    lines.append("\n## Primary (I=3.0) call distribution for candidates\n")
    call_counts = Counter(prim[h]["cluster_call"] for h in cand_headers)
    for call, n in call_counts.most_common():
        lines.append(f"- {call}: {n}")
    lines.append("\n## Stringent (I=5.0) call distribution for candidates\n")
    call_counts_s = Counter(strn[h]["cluster_call"] for h in cand_headers)
    for call, n in call_counts_s.most_common():
        lines.append(f"- {call}: {n}")
    out_path.write_text("\n".join(lines))


def main() -> int:
    seqids = parse_sequence_ids(SEQID_FILE)
    print(f"loaded {len(seqids)} sequence IDs")

    for inflation_file, tag in [
        (WD / "clusters_I3.0.txt", "3.0"),
        (WD / "clusters_I5.0.txt", "5.0"),
    ]:
        if not inflation_file.exists():
            print(f"[WARN] missing {inflation_file}", file=sys.stderr)
            continue
        rows = run_classification(inflation_file, seqids, tag)
        csv_path = OFDIR / f"classification_I{tag}.csv"
        write_csv(csv_path, rows)
        og_summary = per_orthogroup_summary(rows)
        og_path = OFDIR / f"orthogroup_labels_I{tag}.csv"
        write_csv(og_path, og_summary)
        print(f"wrote {csv_path.name}  ({len(rows)} sequence rows, {len(og_summary)} orthogroups)")

    # read back the two result CSVs we just wrote
    def read_csv(p: Path) -> list[dict[str, str]]:
        with p.open() as fh:
            return list(csv.DictReader(fh))
    rows_p = read_csv(OFDIR / "classification_I3.0.csv")
    rows_s = read_csv(OFDIR / "classification_I5.0.csv")
    write_summary_md(rows_p, rows_s, OFDIR / "dop_classification_summary.md")
    print(f"wrote {OFDIR / 'dop_classification_summary.md'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
