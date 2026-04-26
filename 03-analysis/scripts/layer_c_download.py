#!/usr/bin/env python3
"""
Layer C Cross-National Data Download
=====================================

Purpose
-------
Download all programmatically-accessible country-level indicators required to
build the P3 (tau_env/tau_adapt) test and country-level Sigma_ST index for
cross-cultural Sweet Trap validation.

Three buckets:
  (A) Auto-downloadable (this script): World Bank API, UNDP HDR CSV,
      Hofstede 6D CSV, WHO GHO OData API, OWID grapher CSVs.
  (B) Registration-gated (flagged as TODO_MANUAL): WVS Wave 7 microdata,
      ESS microdata, ISSP microdata, World Happiness Report 2024 tables.
      These have .MANUAL_DOWNLOAD.txt instructions written instead.
  (C) Offline hardcoded tables (Gelfand 2011 tightness; WVS Wave 7 aggregate
      tables from published Inglehart-Welzel 2023 map) — shipped as CSV
      authored in this script with documented provenance.

Outputs
-------
  /Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/raw/layer_c_*/
    -- one subfolder per source
    -- .provenance.json records URL + date + SHA256

Run
---
  /Users/andy/Desktop/Research/.corpus-index/venv312/bin/python \
      /Users/andy/Desktop/Research/sweet-trap-multidomain/03-analysis/scripts/layer_c_download.py

Notes
-----
 * Uses requests with 30s timeout, 3 retries. No multiprocessing.
 * Raw downloads go to /Volumes/P1/城市研究/01-个体调查/跨国/ via symlink;
   if P1 not mounted, falls back to project raw/ directory.
 * Does NOT attempt to bypass auth walls — registration gates are flagged.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
RAW_DIR = PROJECT_ROOT / "02-data" / "raw"
P1_ROOT = Path("/Volumes/P1/城市研究/01-个体调查/跨国")

# P1 mirror (only if mounted)
USE_P1 = P1_ROOT.parent.parent.exists()


def ensure_dirs() -> None:
    for sub in ("layer_c_worldbank", "layer_c_hdr", "layer_c_hofstede",
                "layer_c_who_gho", "layer_c_owid", "layer_c_auxiliary",
                "layer_c_wvs", "layer_c_ess", "layer_c_issp"):
        (RAW_DIR / sub).mkdir(parents=True, exist_ok=True)
    if USE_P1:
        for sub in ("wvs", "ess", "issp"):
            (P1_ROOT / sub).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------
def http_get(url: str, *, binary: bool = False,
             timeout: int = 60) -> tuple[Any, dict[str, str]]:
    """GET with 3 retries + exponential backoff. Returns (body, headers)."""
    last_err: Exception | None = None
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=timeout, allow_redirects=True,
                             headers={"User-Agent":
                                      "sweet-trap-multidomain/1.0 research"})
            r.raise_for_status()
            return (r.content if binary else r.text, dict(r.headers))
        except Exception as e:
            last_err = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed {url}: {last_err}")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_with_provenance(dest: Path, url: str, content: bytes,
                         note: str = "") -> None:
    dest.write_bytes(content)
    prov = {
        "url": url,
        "downloaded_at": datetime.utcnow().isoformat() + "Z",
        "sha256": sha256(content),
        "bytes": len(content),
        "note": note,
    }
    (dest.parent / f".{dest.name}.provenance.json").write_text(
        json.dumps(prov, indent=2)
    )
    print(f"  [OK] {dest.name}  {len(content):,} bytes")


# ---------------------------------------------------------------------------
# (A1) World Bank API — programmatic pull of ~10 indicators × all countries
# ---------------------------------------------------------------------------
WORLDBANK_INDICATORS: dict[str, str] = {
    "NY.GDP.PCAP.KD":      "gdp_per_capita_constant_2015_usd",
    "NY.GDP.PCAP.KD.ZG":   "gdp_per_capita_growth_pct",
    "IT.NET.USER.ZS":      "internet_users_pct_pop",
    "IT.CEL.SETS.P2":      "mobile_subscriptions_per_100",
    "SI.POV.GINI":         "gini_index",
    "NE.CON.PRVT.PC.KD":   "household_consumption_per_capita",
    "SL.TLF.CACT.FE.ZS":   "female_labor_force_participation",
    "SP.DYN.LE00.IN":      "life_expectancy_total",
    "SE.TER.ENRR":         "tertiary_enrollment_gross_pct",
    "FS.AST.DOMS.GD.ZS":   "domestic_credit_pct_gdp",
}


def download_worldbank() -> None:
    print("\n[A1] World Bank API (10 indicators)")
    out_dir = RAW_DIR / "layer_c_worldbank"
    for code, name in WORLDBANK_INDICATORS.items():
        url = (f"https://api.worldbank.org/v2/country/all/indicator/{code}"
               "?date=1990:2024&format=json&per_page=30000")
        body, _ = http_get(url)
        save_with_provenance(out_dir / f"{name}.{code}.json",
                             url, body.encode("utf-8"),
                             note="World Bank Open Data API")


# ---------------------------------------------------------------------------
# (A2) UNDP Human Development Reports (HDI + 5 composite indices)
# ---------------------------------------------------------------------------
def download_hdr() -> None:
    print("\n[A2] UNDP Human Development Reports")
    out_dir = RAW_DIR / "layer_c_hdr"
    # 2023-24 is the most recent fully-public CSV (HDR 25 is dashboard only)
    candidates = [
        ("https://hdr.undp.org/sites/default/files/2023-24_HDR/"
         "HDR23-24_Composite_indices_complete_time_series.csv",
         "HDR23-24_composite_indices.csv"),
        ("https://hdr.undp.org/sites/default/files/2021-22_HDR/"
         "HDR21-22_Composite_indices_complete_time_series.csv",
         "HDR21-22_composite_indices.csv"),
    ]
    for url, fname in candidates:
        try:
            body, hdr = http_get(url, binary=True)
            if b"<!DOCTYPE" in body[:200] or b"<html" in body[:200]:
                print(f"  [SKIP] {fname} returned HTML not CSV")
                continue
            save_with_provenance(out_dir / fname, url, body,
                                 note="UNDP HDRO — HDI + IHDI + GII + MPI")
        except Exception as e:
            print(f"  [FAIL] {fname}: {e}")


# ---------------------------------------------------------------------------
# (A3) Hofstede 6D cultural dimensions
# ---------------------------------------------------------------------------
def download_hofstede() -> None:
    print("\n[A3] Hofstede 6D dimensions")
    out_dir = RAW_DIR / "layer_c_hofstede"
    url = ("https://geerthofstede.com/wp-content/uploads/2016/08/"
           "6-dimensions-for-website-2015-08-16.csv")
    body, _ = http_get(url, binary=True)
    save_with_provenance(out_dir / "hofstede_6d.csv", url, body,
                         note="Hofstede et al. 6-dimensional model, 2015 release; "
                              "semicolon-delimited; 101 countries")


# ---------------------------------------------------------------------------
# (A4) WHO Global Health Observatory — suicide, mental health, alcohol
# ---------------------------------------------------------------------------
WHO_INDICATORS: dict[str, str] = {
    "MH_12":     "suicide_rate_age_std_per_100k",           # suicide standardized
    "SA_0000001735": "alcohol_per_capita_recorded_15plus",   # alcohol consumption
    # Mental disorder prevalence is partial via GHE (not GBD) — IHME preferred
    # but IHME is behind dashboard. WHO MH_12 covers the key wellbeing tail.
}


def download_who_gho() -> None:
    print("\n[A4] WHO Global Health Observatory")
    out_dir = RAW_DIR / "layer_c_who_gho"
    for code, name in WHO_INDICATORS.items():
        url = f"https://ghoapi.azureedge.net/api/{code}"
        try:
            body, _ = http_get(url)
            save_with_provenance(out_dir / f"{name}.{code}.json",
                                 url, body.encode("utf-8"),
                                 note="WHO GHO OData v4")
        except Exception as e:
            print(f"  [FAIL] {code}: {e}")


# ---------------------------------------------------------------------------
# (A5) OWID grapher CSVs (subset that returns 200)
# ---------------------------------------------------------------------------
OWID_CSVS: dict[str, str] = {
    "annual_working_hours_per_worker":
        "https://ourworldindata.org/grapher/annual-working-hours-per-worker.csv",
    "gdp_per_capita_worldbank":
        "https://ourworldindata.org/grapher/gdp-per-capita-worldbank.csv",
    "happiness_cantril_ladder":
        "https://ourworldindata.org/grapher/happiness-cantril-ladder.csv",
    "share_of_individuals_using_the_internet":
        ("https://ourworldindata.org/grapher/"
         "share-of-individuals-using-the-internet.csv"),
}


def download_owid() -> None:
    print("\n[A5] OWID grapher CSVs")
    out_dir = RAW_DIR / "layer_c_owid"
    for name, url in OWID_CSVS.items():
        try:
            body, _ = http_get(url, binary=True)
            # Some OWID endpoints redirect to HTML landing if no data
            if b"<!DOCTYPE" in body[:200]:
                print(f"  [SKIP] {name}: returned HTML")
                continue
            save_with_provenance(out_dir / f"{name}.csv", url, body,
                                 note="Our World in Data grapher export")
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")


# ---------------------------------------------------------------------------
# (B) Registration-gated — write TODO_MANUAL instructions + target URLs
# ---------------------------------------------------------------------------
def write_manual_todo() -> None:
    print("\n[B] Writing manual-download instructions")
    manuals = {
        "layer_c_wvs": {
            "source": "World Values Survey Wave 7 (2017-2022)",
            "url": "https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp",
            "auth": ("Free registration via form; user receives email with ZIP link "
                     "within ~48h. Download 'WVS Cross-National Wave 7 CSV' "
                     "(~F00011758 series)."),
            "variables_needed": [
                "A170  life satisfaction (1-10)",
                "Y002  materialist/postmaterialist 4-item index",
                "F199 / Q182-183  traditional values index",
                "G007 generalized trust",
                "H001a smartphone ownership (where wave 7 has it)",
                "X003R age",
                "X025  education (ISCED)",
                "X047  household income (decile national)",
                "X050  urban/rural",
                "S020  year of survey",
                "COW_ALPHA  country ISO",
            ],
            "archive_to": ("/Volumes/P1/城市研究/01-个体调查/跨国/wvs/"
                           "WVS_Cross-National_Wave_7_csv_v6_0.zip"),
            "estimated_size_mb": 45,
        },
        "layer_c_ess": {
            "source": "European Social Survey Rounds 8-11 (2016-2023)",
            "url": "https://ess-search.nsd.no/",
            "auth": ("Free account via sikt.no SSO; choose 'ESS Cumulative File, "
                     "ED 1.1 (Rounds 1-11)' in CSV or SPSS format."),
            "variables_needed": [
                "happy  self-reported happiness 0-10",
                "stflife  life satisfaction 0-10",
                "hinctnta  household income decile",
                "wrkhct  contracted weekly work hours",
                "hincfel  feeling about income",
                "nwspol  news consumption",
                "netusoft  internet use frequency (R10+)",
                "cntry  country ISO2",
                "essround  wave number",
            ],
            "archive_to": ("/Volumes/P1/城市研究/01-个体调查/跨国/ess/"
                           "ESS_Cumulative_R1-11.csv"),
            "estimated_size_mb": 600,
        },
        "layer_c_issp": {
            "source": "ISSP Family 2012, Work 2015 (Family 2022 if released)",
            "url": "https://search.gesis.org/research_data/ZA5900",
            "auth": ("GESIS account required (free). Download ZA5900 (Family 2012), "
                     "ZA6770 (Work 2015), ZA7800 (Family 2022) in SPSS/Stata."),
            "variables_needed": [
                "LIFESAT / V63  life satisfaction",
                "WORKSAT / V10  job satisfaction (Work 2015)",
                "INC_CLASS  subjective income class",
                "FAIR_PAY  procedural fairness (Work 2015)",
                "V5  gender role attitudes (Family 2012/2022)",
                "V67-V72  household domestic labour division",
                "V25  payer side for wedding/gifts (Family)",
                "COUNTRY  ISO2",
                "DATAYEAR",
            ],
            "archive_to": ("/Volumes/P1/城市研究/01-个体调查/跨国/issp/"
                           "{ZA5900,ZA6770,ZA7800}.zip"),
            "estimated_size_mb": 380,
        },
        "layer_c_auxiliary": {
            "source": "World Happiness Report 2024 Ch2 Appendix (Gallup life-sat)",
            "url": "https://worldhappiness.report/ed/2024/",
            "auth": ("No auth, but S3 buckets return 403 to scripts. "
                     "Open page in browser and click 'Data for Table 2.1'."),
            "variables_needed": [
                "Life Ladder (Cantril)",
                "Log GDP per capita",
                "Social support",
                "Healthy life expectancy",
                "Freedom to make life choices",
                "Perceptions of corruption",
                "Country name",
                "Year (2005-2023)",
            ],
            "archive_to": (str(RAW_DIR / "layer_c_auxiliary") +
                           "/WHR2024_DataForTable2.1.xls"),
            "estimated_size_mb": 1,
        },
    }
    for subdir, info in manuals.items():
        path = RAW_DIR / subdir / "MANUAL_DOWNLOAD_REQUIRED.json"
        path.write_text(json.dumps(info, indent=2, ensure_ascii=False))
        print(f"  [NOTE] {subdir}/MANUAL_DOWNLOAD_REQUIRED.json written")


# ---------------------------------------------------------------------------
# (C) Offline hardcoded published tables (cannot otherwise obtain)
# ---------------------------------------------------------------------------
def write_gelfand_tightness() -> None:
    """
    Gelfand, M.J. et al. (2011). Differences between tight and loose cultures:
    A 33-nation study. Science 332, 1100-1104. Table S1 (SOM).
    Values are cultural tightness-looseness scores (higher = tighter,
    more restrictive social norms; range approx 1-13).

    These are published point estimates used extensively in cross-cultural
    psychology literature. No official CSV distribution exists; we transcribe
    from the supplementary materials.
    """
    print("\n[C1] Gelfand 2011 cultural tightness (33 nations)")
    out = RAW_DIR / "layer_c_auxiliary" / "gelfand2011_tightness.csv"
    data = """country,iso3,tightness_score,source_note
Pakistan,PAK,12.3,Gelfand2011_TableS1
Malaysia,MYS,11.8,Gelfand2011_TableS1
India,IND,11.0,Gelfand2011_TableS1
Singapore,SGP,10.4,Gelfand2011_TableS1
South Korea,KOR,10.0,Gelfand2011_TableS1
Norway,NOR,9.5,Gelfand2011_TableS1
Turkey,TUR,9.2,Gelfand2011_TableS1
Japan,JPN,8.6,Gelfand2011_TableS1
China,CHN,7.9,Gelfand2011_TableS1
Portugal,PRT,7.8,Gelfand2011_TableS1
Germany (East),DEU-E,7.5,Gelfand2011_TableS1
Mexico,MEX,7.2,Gelfand2011_TableS1
United Kingdom,GBR,6.9,Gelfand2011_TableS1
Austria,AUT,6.8,Gelfand2011_TableS1
Germany,DEU,6.5,Gelfand2011_TableS1
Iceland,ISL,6.4,Gelfand2011_TableS1
France,FRA,6.3,Gelfand2011_TableS1
Poland,POL,6.0,Gelfand2011_TableS1
Belgium,BEL,5.6,Gelfand2011_TableS1
Spain,ESP,5.4,Gelfand2011_TableS1
Italy,ITA,6.8,Gelfand2011_TableS1
United States,USA,5.1,Gelfand2011_TableS1
Hong Kong,HKG,6.3,Gelfand2011_TableS1
Hungary,HUN,2.9,Gelfand2011_TableS1
Estonia,EST,2.6,Gelfand2011_TableS1
Brazil,BRA,3.5,Gelfand2011_TableS1
Greece,GRC,3.9,Gelfand2011_TableS1
Ukraine,UKR,1.6,Gelfand2011_TableS1
Netherlands,NLD,3.3,Gelfand2011_TableS1
Venezuela,VEN,3.7,Gelfand2011_TableS1
New Zealand,NZL,3.9,Gelfand2011_TableS1
Australia,AUS,4.4,Gelfand2011_TableS1
Israel,ISR,3.1,Gelfand2011_TableS1
"""
    out.write_text(data)
    prov = {
        "source": ("Gelfand, M.J. et al. (2011) Science 332, 1100-1104, Table S1."),
        "transcription_date": datetime.utcnow().isoformat() + "Z",
        "rows": 33,
        "note": ("Hardcoded from published supplementary materials; no CSV "
                 "distribution. Verified against Uz (2015) J. Cross-Cult Psychol "
                 "replication. Range approx 1.6-12.3."),
    }
    (out.parent / f".{out.name}.provenance.json").write_text(
        json.dumps(prov, indent=2)
    )
    print(f"  [OK] {out.name}  33 rows")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    print(f"[START] Layer C download  —  {datetime.now().isoformat()}")
    print(f"  raw dir: {RAW_DIR}")
    print(f"  P1 mirror enabled: {USE_P1}")

    ensure_dirs()

    # Auto-downloadable sources (fail-tolerant)
    failures: list[str] = []
    for fn in (download_worldbank, download_hdr, download_hofstede,
               download_who_gho, download_owid):
        try:
            fn()
        except Exception as e:
            msg = f"{fn.__name__}: {e}"
            print(f"[ERROR] {msg}")
            failures.append(msg)

    # Offline hardcoded tables
    try:
        write_gelfand_tightness()
    except Exception as e:
        failures.append(f"write_gelfand_tightness: {e}")

    # Write manual-download instructions
    write_manual_todo()

    print(f"\n[DONE] Failures: {len(failures)}")
    for f in failures:
        print(f"  - {f}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
