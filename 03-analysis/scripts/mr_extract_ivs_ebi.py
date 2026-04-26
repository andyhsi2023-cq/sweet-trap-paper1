#!/usr/bin/env python3
"""
mr_extract_ivs_ebi.py
=====================
Pull genome-wide-significant lead SNPs (associations) for each exposure GWAS from
the EBI GWAS Catalog REST API. This bypasses the 2024-05 IEU OpenGWAS JWT requirement.

The EBI REST API provides:
  beta (numeric), standardError, pvalue, strongest risk allele (rs + allele),
  risk allele frequency.

We treat these lead SNPs as already LD-independent instruments (GWAS Catalog
reports curated lead SNPs, typically LD-pruned in the paper). For each SNP we
also cross-check that its p<5e-8.

Output: 02-data/processed/mr_iv_<label>_<accession>.csv
"""
from __future__ import annotations
import json, time, sys, logging, math
from pathlib import Path
import requests
import pandas as pd

PROJ = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
OUT  = PROJ / "02-data/processed"
OUT.mkdir(parents=True, exist_ok=True)

LOG = PROJ / "03-analysis/scripts/mr_extract_ivs_ebi.log"
logging.basicConfig(filename=LOG, level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
h = logging.StreamHandler(sys.stdout); h.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
logging.getLogger().addHandler(h)

EXPOSURES = [
    # label, EBI accession, expected n, exposure unit
    ("risk_tolerance",         "GCST006810", 436236, "beta_SD"),
    ("drinks_per_week",        "GCST007461", 941280, "beta_SD"),
    ("bmi_locke2015",          "GCST002783", 339224, "beta_SD"),       # Locke 2015 — Yengo 2018 (GCST006900) has 0 associations in catalog
    ("insomnia",               "GCST004695", 113006, "logOR"),
    ("years_of_schooling",     "GCST006572", 257841, "beta_SD"),       # Lee 2018 Cognitive perf (EA sister entry)
    ("subjective_wellbeing",   "GCST003766", 298420, "beta_SD"),
    ("smoking_initiation",     "GCST007474", 1232091,"logOR"),
    ("insomnia_jansen2019",    "GCST007800", 1331010,"logOR"),          # if exists
]

BASE = "https://www.ebi.ac.uk/gwas/rest/api"

def fetch_associations(accession: str) -> list[dict]:
    """Paginate through associations for a study. Returns list of flat dict."""
    out = []
    page = 0
    while True:
        url = f"{BASE}/studies/{accession}/associations?size=200&page={page}"
        try:
            r = requests.get(url, timeout=60, headers={"Accept": "application/json"})
        except Exception as e:
            logging.error(f"{accession} page {page} request failed: {e}")
            break
        if r.status_code != 200:
            logging.warning(f"{accession} page {page} http={r.status_code}"); break
        data = r.json()
        assoc = data.get("_embedded", {}).get("associations", [])
        if not assoc:
            break
        for a in assoc:
            # Extract SNP + allele
            loci = a.get("loci", []) or []
            if not loci: continue
            sra = loci[0].get("strongestRiskAlleles", []) or []
            if not sra: continue
            rallele = sra[0].get("riskAlleleName", "")  # "rs12345-T"
            if "-" not in rallele: continue
            rsid, ea = rallele.rsplit("-", 1)
            # Pvalue
            pval = a.get("pvalue") or None
            if pval is None:
                m, e = a.get("pvalueMantissa"), a.get("pvalueExponent")
                if m is not None and e is not None: pval = m * (10**e)
            # beta (prefer betaNum; else derive from OR + CI range)
            beta = a.get("betaNum")
            se   = a.get("standardError")
            direction = a.get("betaDirection", "")
            eaf = sra[0].get("riskFrequency", None)
            try: eaf = float(eaf) if eaf not in (None,"","NR") else None
            except: eaf = None
            if beta is not None and direction == "decrease":
                beta = -abs(float(beta))
            elif beta is not None:
                beta = abs(float(beta))
            # OR -> log-OR fallback
            or_val = a.get("orPerCopyNum")
            rng    = a.get("range")
            if (beta is None) and (or_val is not None) and (or_val > 0):
                beta_fallback = math.log(or_val)
                se_fallback = None
                if rng and isinstance(rng, str) and rng.startswith("[") and "-" in rng:
                    try:
                        rstripped = rng.strip("[]").replace(" ", "")
                        lo_s, hi_s = rstripped.split("-", 1)
                        # handle negative lo (unlikely for OR but safe)
                        if "--" in rstripped:   # rare
                            pass
                        lo, hi = float(lo_s), float(hi_s)
                        if lo > 0 and hi > lo:
                            se_fallback = (math.log(hi) - math.log(lo)) / 3.92
                    except Exception:
                        pass
                # if no range, use reported standardError (which may be the OR SE or log-OR SE — flag)
                if se_fallback is None and se is not None:
                    # When OR is reported and SE is reported for OR units, approx se(logOR) ~ se(OR)/OR
                    try:
                        se_fallback = float(se) / or_val
                    except Exception:
                        se_fallback = None
                beta = beta_fallback
                se   = se_fallback
            out.append({
                "accession": accession,
                "rsid": rsid, "ea": ea,
                "beta": beta, "se": se, "pval": pval, "eaf": eaf,
                "beta_unit": a.get("betaUnit",""),
                "or": a.get("orPerCopyNum"),
            })
        # pagination
        page_info = data.get("page", {})
        total_pages = page_info.get("totalPages", 1)
        if page + 1 >= total_pages: break
        page += 1
        time.sleep(0.2)   # polite
    return out

def main():
    summary = []
    for label, acc, n, unit in EXPOSURES:
        logging.info(f"=== {label} ({acc}) ===")
        rows = fetch_associations(acc)
        logging.info(f"  raw associations: {len(rows)}")
        df = pd.DataFrame(rows)
        if len(df) == 0:
            summary.append({"label": label, "accession": acc, "n_raw": 0, "n_kept": 0})
            continue
        # Filter: require beta, se, p<5e-8
        df0 = len(df)
        df = df[df["beta"].notna() & df["se"].notna() & df["pval"].notna()]
        df = df[df["pval"] < 5e-8]
        df = df[df["rsid"].str.startswith("rs")]
        # drop duplicates by rsid (keep smallest p)
        df = df.sort_values("pval").drop_duplicates("rsid", keep="first")
        logging.info(f"  kept SNPs (beta/se/p<5e-8, dedup): {len(df)}")
        # derive F-stat
        df["F"] = (df["beta"] / df["se"]) ** 2
        df["exposure_label"] = label
        df["exposure_n"] = n
        dst = OUT / f"mr_iv_{label}_{acc}.csv"
        df.to_csv(dst, index=False)
        logging.info(f"  wrote {dst}")
        summary.append({"label": label, "accession": acc, "n_raw": df0, "n_kept": len(df),
                        "mean_F": round(df["F"].mean(),1) if len(df) else None,
                        "median_F": round(df["F"].median(),1) if len(df) else None})
    pd.DataFrame(summary).to_csv(OUT / "mr_iv_extraction_summary.csv", index=False)
    logging.info("SUMMARY:\n" + pd.DataFrame(summary).to_string())

if __name__ == "__main__":
    main()
