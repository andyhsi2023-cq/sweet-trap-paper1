#!/usr/bin/env python3
"""
build_issp_panel.py
====================

Step 1 + 2 of Layer C ISSP deep analysis (sweet-trap-multidomain).

Phase A (metadata scan): Writes issp_manifest.csv + per-wave label CSVs.
Phase B (harmonization): Loads only the matched columns per wave and builds
a long panel of country × wave × harmonized-variable cells, z-scored within
(variable × wave) so scales are comparable across waves.

Key fixes vs v1
---------------
- Case-insensitive country/year var detection (newer ISSP waves use UPPER).
- Priority order: C_ALPHAN > COUNTRY > V4 (ISO numeric) > V3 > cntry.
- match_targets EXCLUDES country-specific variants like `CN_V5` / `ES_V14`
  (regex `^[A-Z]{2}_V`).
- ZA4850 (Leisure 2007): only has numeric V4/V5 country codes; we accept
  them and post-hoc map to ISO3 via auxiliary table.
- ZA10000 cumulation (Family series concatenated): loaded separately to
  validate wave-by-wave harmonization against the one-off files.
- All variables scanned case-insensitive via a helper that finds the
  first matching column name regardless of case.
- Sentinel missing: drop values > 95 in ≤10-scale questions, handle NaN.

Inputs / Outputs: see v1 docstring.
"""

from __future__ import annotations

import json
import re
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
RAW_DIR = Path("/Volumes/P1/城市研究/01-个体调查/跨国/issp_gesis")
PROJ_ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
OUT_PROC = PROJ_ROOT / "02-data" / "processed"
OUT_LABELS = OUT_PROC / "issp_variable_labels"
OUT_PROC.mkdir(parents=True, exist_ok=True)
OUT_LABELS.mkdir(parents=True, exist_ok=True)

LOG_PATH = PROJ_ROOT / "03-analysis" / "scripts" / "build_issp_panel.log"

TOPIC_HYPOTHESES = {
    "ZA1700": ("Family", 1988),
    "ZA2620": ("Family", 1994),
    "ZA3880": ("Family", 2002),
    "ZA5900": ("Family", 2012),
    "ZA8794": ("Family", 2022),
    "ZA1840": ("Work", 1989),
    "ZA3090": ("Work", 1997),
    "ZA4350": ("Work", 2005),
    "ZA6770": ("Work", 2015),
    "ZA1680": ("SocialInequality", 1987),
    "ZA2310": ("SocialInequality", 1992),
    "ZA3430": ("SocialInequality", 1999),
    "ZA5400": ("SocialInequality", 2009),
    "ZA7600": ("SocialInequality", 2019),
    "ZA5800": ("Health", 2011),
    "ZA8000": ("Health", 2021),
    "ZA4850": ("Leisure", 2007),
    "ZA10000": ("CumulationFamily", None),
    "ZA10010": ("CumulationNatID", None),
}

# Target variable patterns.
# Each tuple: (harmonized_name, regex on label, sign).
# Patterns are written to match canonical ISSP wording.
TARGET_PATTERNS = {
    "Family": [
        ("life_happy",          r"(life\s+in\s+general|how\s+happy.*unhappy|general.*how\s+happy|happy\s+on\s+the\s+whole|life.*happy.*whole)", "+"),
        ("family_sat",          r"(satisfied\s+with\s+family|family\s+life.*satisf|satisfaction.*family\s+life)", "+"),
        ("work_sat",            r"(satisfied.*main\s+job|satisfaction.*main\s+job|how\s+satisfied.*job|satisfied\s+in\s+job)", "+"),
        ("working_mom_warm",    r"(work(g|ing)\s+mom.*warm|warm\s+relation.*child|mother.*warm|workg\s+mom)", "+"),
        ("family_suffers_ftj",  r"(family\s+life\s+suffers|workg\s+woman.*family|working\s+woman.*family\s+life)", "+"),
        ("housewife_fulfill",   r"(housewife.*fulfill|being\s+housewife|home.*kids|women.*want.*home)", "+"),
        ("man_earn_money",      r"(men.*earn\s+money|man.*earn.*money|men'?s\s+job.*earn|men'?s\s+job.*work)", "+"),
        ("marriage_better",     r"(married.*better|married\s+people.*happ|marri.*happi|better\s+off.*marri)", "+"),
        ("divorce_solution",    r"(divorce.*solution|divorce.*best.*solution|divorce\s+best)", "+"),
    ],
    "Work": [
        ("work_sat",            r"(how\s+satisfied.*main\s+job|satisfied.*main.*job|job\s+satisfaction|satisfied\s+in\s+job)", "+"),
        ("life_happy",          r"(how\s+happy.*unhappy|life\s+in\s+general|happy\s+on\s+the\s+whole)", "+"),
        ("work_central",        r"(work.*more\s+than.*money|work\s+most\s+imp|job\s+just\s+for\s+the\s+money|job.*more\s+than\s+just)", "+"),
        ("work_first_prio",     r"(work.*first\s+prior|job.*first\s+prior|work\s+should\s+come\s+first)", "+"),
        ("pay_fair",            r"(fair.*earn|earn.*fair|paid.*fair|fair\s+pay)", "+"),
        ("income_high",         r"(high\s+income|good\s+pay|income.*important|important:\s*high\s+income)", "+"),
        ("promote_chance",      r"(chances?.*advance|advance.*career|opportun.*promot|promot.*high)", "+"),
        ("interfer_family",     r"(job.*interfere.*family|demands.*job.*family)", "+"),
    ],
    "SocialInequality": [
        ("life_happy",          r"(how\s+happy.*unhappy|life\s+in\s+general|happy\s+on\s+the\s+whole)", "+"),
        ("income_diff_large",   r"(differences?\s+in\s+income.*large|income.*too\s+large|income\s+differences.*large|differen.*income.*too)", "+"),
        ("effort_gets_ahead",   r"(hard\s+work|work\s+hard.*get\s+ahead|get\s+ahead.*hard\s+work|gettg\s+ahead.*hard\s+work|getting\s+ahead.*hard)", "+"),
        ("rich_family",         r"(wealthy\s+family|coming\s+from.*wealthy|rich\s+family|ahead:\s*wealthy|ahead.*wealthy\s+family)", "+"),
        ("pay_responsibility",  r"(pay.*responsib|pay.*important\s+job)", "+"),
        ("gov_reduce_diff",     r"(government.*reduce.*difference|reduce.*income.*differ|should\s+redistribute)", "+"),
        ("high_status_own",     r"(own\s+status|where.*place\s+yourself|status.*society.*self)", "+"),
    ],
    "Health": [
        ("life_happy",          r"(how\s+happy.*unhappy|life\s+in\s+general|happy\s+on\s+the\s+whole)", "+"),
        ("health_self",         r"(health\s+in\s+general|state.*health|general\s+health|your\s+health.*general)", "+"),
        ("alt_medicine_sat",    r"(alternative\s+health.*practitioner|alternative\s+medicine)", "+"),
        ("doctor_visit_sat",    r"(satisfaction.*treatment.*last\s+visited\s+doctor|treatment:\s*last\s+visit)", "+"),
        ("healthy_food",        r"(fruits?\s+and\s+veget|eat.*fruit|balanced\s+diet|healthy\s+food)", "+"),
        ("exercise",            r"(physical\s+activit|exercise|sport.*regular|do\s+exercise)", "+"),
        ("healthcare_sat",      r"(satisfaction.*health\s+care\s+system)", "+"),
    ],
    "Leisure": [
        ("life_happy",          r"(how\s+happy.*unhappy|life\s+in\s+general|happy\s+on\s+the\s+whole)", "+"),
        ("tv_watch",            r"(watch\s+tv|tv.*hour|television)", "+"),
        ("shopping",            r"(go\s+out\s+shopping|shopping.*free\s+time|shopping)", "+"),
        ("internet_hours",      r"(internet|computer.*free\s+time|online|spend.*internet)", "+"),
        ("fitness",             r"(fitness|go\s+to.*gym|work\s+out|sport.*game)", "+"),
        ("cultural",            r"(go\s+to.*movies|cinema|museum|theater|concert|art)", "+"),
    ],
    "CumulationFamily": [
        ("life_happy",          r"(life\s+in\s+general.*happy|how\s+happy.*unhappy|happy\s+on\s+the\s+whole)", "+"),
        ("family_sat",          r"(satisfied.*family|family\s+life.*satisf)", "+"),
        ("work_sat",            r"(satisfied.*main\s+job|satisfaction.*main\s+job)", "+"),
        ("working_mom_warm",    r"(working\s+mom.*warm|mother.*warm)", "+"),
        ("family_suffers_ftj",  r"(family\s+life\s+suffers)", "+"),
        ("marriage_better",     r"(married.*better|better\s+off.*marri)", "+"),
    ],
    "CumulationNatID": [
        # cumul national-identity — skip (irrelevant to Sweet Trap)
    ],
}

# Country var candidates (higher priority first). Case-insensitive.
# NB: in old ISSP waves (1987-2002), `v3` is the country var (small serial int
# with value labels like 'aus', 'd', 'usa'); `v4`/`V4` in newer waves is the
# ISO numeric country code. C_ALPHAN is best when present.
COUNTRY_VAR_PRIORITY = ["C_ALPHAN", "c_alphan", "COUNTRY", "country",
                        "v3", "V3", "v4", "V4", "cntry", "CNTRY",
                        "c_sample"]

YEAR_VAR_PRIORITY = ["DATEYR", "dateyr", "year", "YEAR", "wave"]

# Mapping from ISSP country abbreviations / ISO3 / common short codes to
# canonical ISO-3166 alpha-2. Used after decoding v3/v4 value labels.
ISSP_CODE_TO_ISO2 = {
    # alpha abbreviations found in ISSP v3 value labels
    "aus": "AU", "AUS": "AU", "australia": "AU",
    "a": "AT", "aut": "AT", "austria": "AT",
    "d": "DE", "germany": "DE", "d-w": "DE", "d-e": "DE", "DE-W": "DE", "DE-E": "DE",
    "DE_W": "DE", "DE_E": "DE", "deu": "DE",
    "gb": "GB", "uk": "GB", "great britain": "GB", "GB-GBN": "GB", "GBN": "GB",
    "nirl": "GB", "NIRL": "GB",  # Northern Ireland folded into GB in our panel
    "GB-NIR": "GB",
    "usa": "US", "us": "US", "united states": "US",
    "h": "HU", "hu": "HU", "hun": "HU", "hungary": "HU",
    "nl": "NL", "nld": "NL", "netherlands": "NL",
    "i": "IT", "it": "IT", "ita": "IT", "italy": "IT",
    "irl": "IE", "ie": "IE", "ireland": "IE",
    "ch": "CH", "switzerland": "CH", "che": "CH",
    "pl": "PL", "pol": "PL", "poland": "PL",
    "n": "NO", "no": "NO", "nor": "NO", "norway": "NO",
    "il": "IL", "isr": "IL", "israel": "IL",
    "j": "JP", "jp": "JP", "jpn": "JP", "japan": "JP",
    "s": "SE", "se": "SE", "swe": "SE", "sweden": "SE",
    "cz": "CZ", "cze": "CZ", "czech republic": "CZ", "cz - czech republic": "CZ",
    "slo": "SI", "si": "SI", "svn": "SI", "slovenia": "SI",
    "bg": "BG", "bgr": "BG", "bulgaria": "BG",
    "rus": "RU", "ru": "RU", "russia": "RU",
    "nz": "NZ", "nzl": "NZ", "new zealand": "NZ",
    "cdn": "CA", "ca": "CA", "can": "CA", "canada": "CA",
    "rp": "PH", "ph": "PH", "phl": "PH", "philippines": "PH",
    "e": "ES", "es": "ES", "esp": "ES", "spain": "ES",
    "f": "FR", "fr": "FR", "fra": "FR", "france": "FR",
    "cy": "CY", "cyp": "CY", "cyprus": "CY",
    "p": "PT", "pt": "PT", "prt": "PT", "portugal": "PT",
    "dk": "DK", "dnk": "DK", "denmark": "DK",
    "bup": "BY",  # Belarus
    "sk": "SK", "svk": "SK", "slovakia": "SK", "slo-sk": "SK",
    "rch": "CL", "cl": "CL", "chl": "CL", "chile": "CL",
    "lv": "LV", "lva": "LV", "latvia": "LV",
    "lt": "LT", "ltu": "LT", "lithuania": "LT",
    "fi": "FI", "fin": "FI", "finland": "FI",
    "ee": "EE", "est": "EE", "estonia": "EE",
    "hr": "HR", "hrv": "HR", "croatia": "HR",
    "za": "ZA", "zaf": "ZA", "south africa": "ZA",
    "ua": "UA", "ukr": "UA", "ukraine": "UA",
    "ve": "VE", "ven": "VE", "venezuela": "VE",
    "mx": "MX", "mex": "MX", "mexico": "MX",
    "kr": "KR", "rok": "KR", "south korea": "KR", "korea, south": "KR", "korea": "KR",
    "tr": "TR", "tur": "TR", "turkey": "TR",
    "tw": "TW", "twn": "TW", "taiwan": "TW",
    "hk": "HK", "hkg": "HK", "hong kong": "HK",
    "cn": "CN", "chn": "CN", "china": "CN",
    "in": "IN", "ind": "IN", "india": "IN",
    "ar": "AR", "arg": "AR", "argentina": "AR",
    "br": "BR", "bra": "BR", "brazil": "BR",
    "is": "IS", "isl": "IS", "iceland": "IS",
    "su": "SU",  # soviet union pre-dissolution
    "yu": "YU",  # Yugoslavia pre-dissolution
    "uy": "UY", "ury": "UY", "uruguay": "UY",
    "sr": "SR",
    "th": "TH", "tha": "TH", "thailand": "TH",
    "ve-ven": "VE",
    "bg - bulgaria": "BG",
}

# ISO3166 numeric-ISO alpha2 mapping (for modern waves where v4 is iso-num).
ISO_NUM_TO_ALPHA2 = {
    36: "AU", 40: "AT", 56: "BE", 100: "BG", 124: "CA", 152: "CL", 156: "CN",
    158: "TW", 196: "CY", 203: "CZ", 208: "DK", 233: "EE", 246: "FI", 250: "FR",
    276: "DE", 300: "GR", 352: "IS", 356: "IN", 372: "IE", 376: "IL", 380: "IT",
    392: "JP", 410: "KR", 428: "LV", 440: "LT", 484: "MX", 528: "NL", 554: "NZ",
    578: "NO", 591: "PA", 608: "PH", 616: "PL", 620: "PT", 643: "RU", 703: "SK",
    705: "SI", 710: "ZA", 724: "ES", 752: "SE", 756: "CH", 792: "TR", 804: "UA",
    826: "GB", 840: "US", 858: "UY", 862: "VE", 191: "HR", 348: "HU",
    642: "RO", 368: "IQ", 504: "MA", 764: "TH", 704: "VN", 710.0: "ZA",
}

# Wave-to-year map for cumulation disambiguation (ZA10000 has multiple waves).
STUDYNO_TO_YEAR = {
    1700: 1988,  # Family 1988
    2620: 1994,
    3880: 2002,
    5900: 2012,
    # ZA10000 v2-0-0 cumulation seems to include up to 2012
}


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def reset_log() -> None:
    if LOG_PATH.exists():
        LOG_PATH.unlink()
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write(f"# build_issp_panel log — started {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def find_col_ci(df_cols: list[str], candidates: list[str]) -> str | None:
    """Find first case-insensitive match from candidates in df_cols."""
    lower_map = {c.lower(): c for c in df_cols}
    for cand in candidates:
        if cand in df_cols:
            return cand
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    return None


def pick_country_var(columns: list[str], labels: dict[str, str] | None = None) -> str | None:
    """Pick country var. If labels dict given, prefer vars whose LABEL contains
    'country'; skip vars labeled 'respondent' or 'study number' etc."""
    if labels:
        # Priority tier 1: C_ALPHAN always wins
        for pref in ["C_ALPHAN", "c_alphan"]:
            if pref in columns:
                return pref
        # Tier 2: vars whose label contains 'country' (but not 'respondent'/'id'/'sample number')
        country_hits = []
        for v in columns:
            lab = (labels.get(v, "") or "").lower()
            if "country" in lab and not any(k in lab for k in
                    ("respondent", "study number", "id number", "year", "birth",
                     "specific", "city", "region", "town")):
                country_hits.append(v)
        # Prefer one that looks like alpha; prefer those with 'iso' or 'alpha'
        for v in country_hits:
            lab = (labels.get(v, "") or "").lower()
            if "alpha" in lab or "prefix" in lab:
                return v
        if country_hits:
            return country_hits[0]
    # Fallback: original priority list
    return find_col_ci(columns, COUNTRY_VAR_PRIORITY)


def pick_year_var(columns: list[str]) -> str | None:
    return find_col_ci(columns, YEAR_VAR_PRIORITY)


# ---------------------------------------------------------------------------
# Phase A — metadata scan
# ---------------------------------------------------------------------------
def scan_file_metadata(path: Path) -> dict:
    stem = path.stem
    za_code = re.match(r"(ZA\d+)", stem).group(1) if re.match(r"ZA\d+", stem) else stem
    topic_hyp, year_hyp = TOPIC_HYPOTHESES.get(za_code, (None, None))
    result = {
        "file": path.name,
        "za_code": za_code,
        "ext": path.suffix,
        "size_mb": round(path.stat().st_size / 1e6, 1),
        "n_obs": None,
        "n_vars": None,
        "file_label": None,
        "topic_hyp": topic_hyp,
        "year_hyp": year_hyp,
        "country_var": None,
        "year_var": None,
        "error": None,
    }
    try:
        if path.suffix == ".dta":
            _, meta = pyreadstat.read_dta(str(path), metadataonly=True)
        elif path.suffix == ".por":
            _, meta = pyreadstat.read_por(str(path), metadataonly=True)
        elif path.suffix == ".sav":
            _, meta = pyreadstat.read_sav(str(path), metadataonly=True)
        else:
            result["error"] = f"unknown ext {path.suffix}"
            return result

        result["n_obs"] = int(meta.number_rows) if meta.number_rows is not None else None
        result["n_vars"] = len(meta.column_names)
        result["file_label"] = (meta.file_label or "").strip()[:300]

        vdf = pd.DataFrame({
            "variable": meta.column_names,
            "label": [meta.column_names_to_labels.get(v, "") or "" for v in meta.column_names],
            "type": [str(meta.readstat_variable_types.get(v, "")) for v in meta.column_names],
            "format": [str(meta.original_variable_types.get(v, "")) for v in meta.column_names],
        })
        vdf.to_csv(OUT_LABELS / f"{stem}_labels.csv", index=False, encoding="utf-8")

        labels_map = {v: (meta.column_names_to_labels.get(v, "") or "")
                      for v in meta.column_names}
        result["country_var"] = pick_country_var(meta.column_names, labels_map)
        result["year_var"] = pick_year_var(meta.column_names)

    except Exception as e:
        result["error"] = str(e)[:250]
    return result


def phase_a_scan() -> pd.DataFrame:
    log("Phase A: metadata scan of ISSP files...")
    files = sorted([p for p in RAW_DIR.iterdir()
                    if p.suffix in (".dta", ".por", ".sav") and not p.name.startswith("._")])
    log(f"Found {len(files)} candidate files")
    records = []
    for p in files:
        t0 = time.time()
        r = scan_file_metadata(p)
        log(f"  {p.name:35s} n_obs={r['n_obs']!s:>8s} n_vars={r['n_vars']!s:>5s} "
            f"topic={r['topic_hyp']!s:<18s} year={r['year_hyp']!s:<6s} "
            f"country={r['country_var']!s:<10s} year_v={r['year_var']!s:<8s} [{time.time()-t0:.2f}s]")
        if r["error"]:
            log(f"    ERROR: {r['error']}")
        records.append(r)

    mf = pd.DataFrame(records)
    mf.to_csv(OUT_PROC / "issp_manifest.csv", index=False, encoding="utf-8")
    log(f"Wrote manifest: {OUT_PROC / 'issp_manifest.csv'} ({len(mf)} rows)")
    return mf


# ---------------------------------------------------------------------------
# Phase B — harmonization
# ---------------------------------------------------------------------------
COUNTRY_SPECIFIC_RX = re.compile(r"^[A-Z]{2}_V\d+$")


def match_targets(vlabels_df: pd.DataFrame, topic: str) -> dict[str, tuple[str, str]]:
    """Return {harmonized_name: (variable_name, label)}.
    Excludes country-specific XX_V## variants.
    Prefers shortest matching label (the primary Q).
    """
    out: dict[str, tuple[str, str]] = {}
    patterns = TARGET_PATTERNS.get(topic, [])
    for harm_name, regex, _sign in patterns:
        rx = re.compile(regex, flags=re.IGNORECASE)
        hits = []
        for _, row in vlabels_df.iterrows():
            var = str(row["variable"] or "")
            lab = str(row["label"] or "")
            if COUNTRY_SPECIFIC_RX.match(var):
                continue
            if rx.search(lab):
                hits.append((var, lab))
        if hits:
            hits.sort(key=lambda x: (len(x[1]), x[0]))
            out[harm_name] = (hits[0][0], hits[0][1])
    return out


def load_subset(path: Path, var_list: list[str]):
    """Return (df, meta) — meta gives us variable_value_labels for decoding."""
    try:
        if path.suffix == ".dta":
            df, meta = pyreadstat.read_dta(str(path), usecols=var_list, apply_value_formats=False)
        elif path.suffix == ".por":
            df, meta = pyreadstat.read_por(str(path), usecols=var_list, apply_value_formats=False)
        elif path.suffix == ".sav":
            df, meta = pyreadstat.read_sav(str(path), usecols=var_list, apply_value_formats=False)
        else:
            return None, None
        return df, meta
    except Exception as e:
        log(f"    load_subset error ({var_list}): {str(e)[:160]}")
        return None, None


def _normalize_label_to_iso2(raw) -> str:
    """Given an ISSP country label (e.g., 'aus', 'USA - United States',
    'J - Japan', 'DE-W'), return canonical ISO2 (AU, US, JP, DE) or empty."""
    if raw is None or (isinstance(raw, float) and np.isnan(raw)):
        return ""
    s = str(raw).strip()
    if not s:
        return ""
    # 1) direct lookup (exact lowered)
    sl = s.lower()
    if sl in ISSP_CODE_TO_ISO2:
        return ISSP_CODE_TO_ISO2[sl]
    # 2) head before space/hyphen/slash: "J - Japan", "USA Germany"
    head = re.split(r"[\s\-/]+", s, maxsplit=1)[0]
    if head and head.lower() in ISSP_CODE_TO_ISO2:
        return ISSP_CODE_TO_ISO2[head.lower()]
    # 3) 'aus', 'USA', etc. already 2-4 char alpha
    alpha = re.match(r"^([A-Za-z]{2,4})", s)
    if alpha:
        k = alpha.group(1).lower()
        if k in ISSP_CODE_TO_ISO2:
            return ISSP_CODE_TO_ISO2[k]
    # 4) upper first 2 chars if plausible ISO2
    if len(s) >= 2 and s[:2].isalpha():
        return s[:2].upper()
    return ""


def decode_country_series(df, cvar: str, meta) -> pd.Series:
    """Given the country variable column and meta, return a Series of ISO2 codes."""
    vals = df[cvar]
    # Case 1: already alpha (c_alphan, COUNTRY string)
    if vals.dtype == object:
        return vals.apply(_normalize_label_to_iso2)

    # Case 2: numeric — consult value_labels
    vlab = None
    # try each-case key
    for key_try in (cvar, cvar.lower(), cvar.upper()):
        if meta is not None and key_try in meta.variable_value_labels:
            vlab = meta.variable_value_labels[key_try]
            break

    def _decode(v):
        if pd.isna(v):
            return ""
        try:
            iv = int(v)
        except Exception:
            return ""
        # First check value label
        if vlab:
            for key in (iv, float(iv)):
                if key in vlab:
                    return _normalize_label_to_iso2(vlab[key])
        # Fallback: treat as ISO numeric
        if iv in ISO_NUM_TO_ALPHA2:
            return ISO_NUM_TO_ALPHA2[iv]
        return ""
    return vals.apply(_decode)


def harmonize_one_wave(row: pd.Series) -> pd.DataFrame | None:
    za = row["za_code"]
    topic = row["topic_hyp"]
    year = row["year_hyp"]
    path = RAW_DIR / row["file"]
    vlabels_path = OUT_LABELS / f"{path.stem}_labels.csv"
    if not vlabels_path.exists():
        log(f"  {za}: missing label csv — skipped")
        return None

    vl = pd.read_csv(vlabels_path)
    # Ensure `variable` col is str (some labels blank)
    vl["label"] = vl["label"].fillna("")
    vl["variable"] = vl["variable"].astype(str)

    matched = match_targets(vl, topic)
    log(f"  {za} [{topic} {year}] matched {len(matched)} targets: {list(matched.keys())}")
    if not matched:
        return None

    want = [v for v, _ in matched.values()]

    # Country var
    all_cols = vl["variable"].tolist()
    labels_map = dict(zip(vl["variable"].astype(str), vl["label"].astype(str)))
    cvar = pick_country_var(all_cols, labels_map)
    if cvar is None:
        log(f"    {za}: NO country var → skipped")
        return None
    if cvar not in want:
        want.append(cvar)

    # Secondary country (for cumulation, we also want studyno for year)
    if topic in ("CumulationFamily", "CumulationNatID"):
        for extra in ["studyno", "STUDYNO", "DATEYR", "dateyr"]:
            if extra in all_cols and extra not in want:
                want.append(extra)

    # Weight
    wcol = None
    for wv in ["weight", "WEIGHT", "wght", "WGHT", "wt", "WT"]:
        if wv in all_cols:
            wcol = wv
            want.append(wv)
            break

    want = list(dict.fromkeys(want))
    log(f"    loading {len(want)} vars: country={cvar} weight={wcol}")
    df, meta = load_subset(path, want)
    if df is None or len(df) == 0:
        log(f"    {za}: load failed")
        return None

    # Country column — decode via value labels if numeric
    df["_country"] = decode_country_series(df, cvar, meta)
    # Weight
    if wcol and wcol in df.columns:
        df["_weight"] = pd.to_numeric(df[wcol], errors="coerce").fillna(1.0).clip(lower=0)
    else:
        df["_weight"] = 1.0

    # Resolve year for cumulation: prefer DATEYR, else map studyno->year
    if topic in ("CumulationFamily", "CumulationNatID"):
        year_col = None
        for yc in ["DATEYR", "dateyr"]:
            if yc in df.columns:
                year_col = yc
                break
        if year_col is not None:
            df["_year"] = pd.to_numeric(df[year_col], errors="coerce")
        else:
            # map studyno to year heuristically
            scol = None
            for sc in ["studyno", "STUDYNO"]:
                if sc in df.columns:
                    scol = sc
                    break
            if scol:
                df["_year"] = pd.to_numeric(df[scol], errors="coerce").map(STUDYNO_TO_YEAR)
            else:
                log(f"    {za}: cumulation — no year column; skipped")
                return None
    else:
        df["_year"] = year

    all_long = []
    for harm_name, (src_var, src_label) in matched.items():
        if src_var not in df.columns:
            continue
        vals = pd.to_numeric(df[src_var], errors="coerce")
        nn = vals.dropna()
        if len(nn) == 0:
            continue
        # ISSP sentinel: values > 90 in a ≤10-scale are missing
        share_small = (nn.abs() <= 10).mean()
        if share_small > 0.85:
            vals = vals.where(vals.abs() <= 10, np.nan)
        # And drop negatives (some waves encode missing as -1/-9)
        vals = vals.where(vals >= 0, np.nan)

        sub = pd.DataFrame({
            "za_code": za,
            "topic": topic,
            "year": pd.to_numeric(df["_year"], errors="coerce"),
            "country": df["_country"],
            "variable_harmonized": harm_name,
            "variable_source": src_var,
            "variable_label_source": src_label[:180],
            "value_raw": vals,
            "weight": df["_weight"],
        })
        sub = sub.dropna(subset=["value_raw", "year"])
        sub = sub[sub["country"].str.len() > 0]
        all_long.append(sub)

    if not all_long:
        return None
    out = pd.concat(all_long, ignore_index=True)
    del df
    return out


def phase_b_harmonize(manifest: pd.DataFrame) -> pd.DataFrame:
    log("\nPhase B: harmonization...")
    all_waves = []
    topic_order = ["Family", "Work", "SocialInequality", "Health", "Leisure",
                   "CumulationFamily"]  # skip CumulationNatID
    for topic in topic_order:
        rows = manifest[(manifest["topic_hyp"] == topic) & (manifest["error"].isna())]
        log(f"\n=== Topic: {topic} ({len(rows)} files) ===")
        for _, row in rows.iterrows():
            sub = harmonize_one_wave(row)
            if sub is not None and len(sub) > 0:
                all_waves.append(sub)
                log(f"    -> {len(sub):,} individual-level observations harvested")

    if not all_waves:
        log("NO harmonized data assembled")
        return pd.DataFrame()

    long = pd.concat(all_waves, ignore_index=True)
    log(f"\nTotal raw long (individual level): {len(long):,} rows, "
        f"{long['country'].nunique()} countries, "
        f"{long['za_code'].nunique()} waves, "
        f"{long['variable_harmonized'].nunique()} variables")

    # Collapse to (topic × variable × za_code × year × country) cells.
    long["vxw"] = long["value_raw"] * long["weight"]
    cell = (long.groupby(["topic", "variable_harmonized", "za_code", "year", "country"],
                         as_index=False)
                 .agg(v_sum=("vxw", "sum"),
                      w_sum=("weight", "sum"),
                      n_cell=("value_raw", "size"),
                      v_mean=("value_raw", "mean"),
                      v_std=("value_raw", "std")))
    cell["v_wmean"] = cell["v_sum"] / cell["w_sum"].replace(0, np.nan)
    cell = cell[cell["n_cell"] >= 30].copy()
    # Drop zero-variance cells (country used different variable entirely
    # — e.g., CN in ZA5800 used CN_V5 not V5 → V5=0 for all CN rows).
    before = len(cell)
    cell = cell[(cell["v_std"].isna()) | (cell["v_std"] > 1e-9)].copy()
    cell = cell[cell["v_wmean"].abs() > 1e-9].copy()  # reject exact-zero means (sentinel)
    log(f"Dropped {before - len(cell)} zero-variance/zero-mean cells")

    # z-score within (variable × wave).
    cell["value_z"] = cell.groupby(["topic", "variable_harmonized", "za_code"])["v_wmean"] \
                         .transform(lambda x: (x - x.mean()) / (x.std() if x.std() > 0 else 1.0))

    cell = cell.rename(columns={"v_wmean": "value_wmean"})
    out_path = OUT_PROC / "issp_long_1985_2022.parquet"
    cell[["topic", "variable_harmonized", "za_code", "year", "country",
          "n_cell", "value_wmean", "value_z", "v_mean", "v_std"]].to_parquet(
        out_path, index=False)
    log(f"Wrote: {out_path}  ({len(cell):,} country×wave×variable cells)")

    return cell


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    reset_log()
    log(f"pyreadstat {pyreadstat.__version__}  |  RAW_DIR exists={RAW_DIR.exists()}")

    try:
        manifest = phase_a_scan()
        cell = phase_b_harmonize(manifest)
    except Exception as e:
        log(f"FATAL: {e}\n{traceback.format_exc()}")
        return 1

    log("\n=== Manifest summary by topic ===")
    msum = manifest.groupby("topic_hyp", dropna=False).agg(
        n_waves=("za_code", "count"),
        total_obs=("n_obs", "sum"),
    )
    log(str(msum))

    if len(cell) > 0:
        log("\n=== Long panel coverage ===")
        cov = cell.groupby("topic").agg(
            n_cells=("value_wmean", "size"),
            n_countries=("country", "nunique"),
            n_waves=("za_code", "nunique"),
            n_vars=("variable_harmonized", "nunique"),
        )
        log(str(cov))

        log("\n=== Variable × wave matrix (country counts) ===")
        pivot = cell.pivot_table(index=["topic", "variable_harmonized"],
                                 columns="za_code", values="country",
                                 aggfunc="nunique", fill_value=0)
        log(str(pivot))

    log("DONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
