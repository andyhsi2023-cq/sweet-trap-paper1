#!/usr/bin/env python3
"""
Layer C harmonization — country x year x variable long panel
=============================================================

Reads the heterogeneous raw files from `layer_c_download.py` and produces a
single parquet with columns:

  iso3  country  year  variable  value  source

Variables included (auto-downloadable tier only; manual WVS/ESS/ISSP are
merged in a second pass when Andy provides the files):

  gdp_per_capita_constant_2015_usd      WorldBank
  gdp_per_capita_growth_pct             WorldBank
  internet_users_pct_pop                WorldBank
  mobile_subscriptions_per_100          WorldBank
  gini_index                            WorldBank
  household_consumption_per_capita      WorldBank
  female_labor_force_participation      WorldBank
  life_expectancy_total                 WorldBank
  tertiary_enrollment_gross_pct         WorldBank
  domestic_credit_pct_gdp               WorldBank
  hdi                                   UNDP HDR
  gnipc                                 UNDP HDR (GNI per capita PPP)
  eys                                   UNDP HDR (expected years of schooling)
  mys                                   UNDP HDR (mean years of schooling)
  gdi                                   UNDP HDR (gender development)
  ihdi                                  UNDP HDR (inequality-adjusted)
  hofstede_pdi / idv / mas / uai / ltowvs / ivr   Hofstede (time-invariant)
  suicide_rate                          WHO GHO (age-standardised, both sexes)
  alcohol_per_capita_15plus             WHO GHO
  cantril_ladder                        OWID / Gallup WHR
  gelfand_tightness                     Gelfand2011 (time-invariant)
  working_hours_per_worker              OWID

Output
------
  02-data/processed/layer_c_cross_national.parquet

Notes
-----
 * ISO3 is the canonical country key. Hofstede file uses custom 3-letter
   codes (e.g., 'CHN') that we map to ISO3 directly.
 * Time-invariant variables (Hofstede, Gelfand) are broadcast to every year
   in the panel via a wide-form join done downstream; in the long panel they
   receive year = NaN as a marker of invariance.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
RAW = PROJECT_ROOT / "02-data" / "raw"
OUT = PROJECT_ROOT / "02-data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Country ISO helpers
# ---------------------------------------------------------------------------
# Hofstede / Gelfand non-standard codes -> ISO3
ISO_FIX = {
    "GBR": "GBR", "USA": "USA", "CHN": "CHN", "HKG": "HKG",
    "DEU-E": None,  # East Germany historical — drop
}

# Aggregate / regional codes in World Bank to drop
WB_AGG_PREFIXES = {
    # ISO-like codes for aggregates in WB data
    "AFE", "AFW", "ARB", "CEB", "CSS", "EAP", "EAR", "EAS", "ECA", "ECS",
    "EMU", "EUU", "FCS", "HIC", "HPC", "IBD", "IBT", "IDA", "IDB", "IDX",
    "INX", "LAC", "LCN", "LDC", "LIC", "LMC", "LMY", "LTE", "MEA", "MIC",
    "MNA", "NAC", "OED", "OSS", "PRE", "PSS", "PST", "SAS", "SSA", "SSF",
    "SST", "TEA", "TEC", "TLA", "TMN", "TSA", "TSS", "UMC", "WLD", "XKX",
}


# ---------------------------------------------------------------------------
# World Bank JSON -> long frame
# ---------------------------------------------------------------------------
def load_worldbank() -> pd.DataFrame:
    wb_dir = RAW / "layer_c_worldbank"
    frames: list[pd.DataFrame] = []
    for jf in sorted(wb_dir.glob("*.json")):
        var_name = jf.stem.split(".")[0]
        payload = json.loads(jf.read_text())
        if not isinstance(payload, list) or len(payload) < 2:
            continue
        rows = payload[1]
        if rows is None:
            continue
        df = pd.DataFrame([{
            "iso3":    r["countryiso3code"],
            "country": r["country"]["value"],
            "year":    int(r["date"]),
            "value":   r["value"],
        } for r in rows if r.get("value") is not None])
        df["variable"] = var_name
        df["source"] = "WorldBank"
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    # Drop aggregates
    out = out[~out["iso3"].isin(WB_AGG_PREFIXES)]
    out = out[out["iso3"].str.len() == 3]
    return out[["iso3", "country", "year", "variable", "value", "source"]]


# ---------------------------------------------------------------------------
# UNDP HDR wide CSV -> long frame
# ---------------------------------------------------------------------------
def load_hdr() -> pd.DataFrame:
    path = RAW / "layer_c_hdr" / "HDR23-24_composite_indices.csv"
    # UNDP file is latin-1 (country names with diacritics)
    df = pd.read_csv(path, encoding="latin-1")
    base = df[["iso3", "country"]].copy()
    # Extract year-suffixed columns for these indicators
    indicators = ["hdi", "le", "eys", "mys", "gnipc", "gdi", "ihdi", "gii"]
    long_frames: list[pd.DataFrame] = []
    for ind in indicators:
        cols = [c for c in df.columns if c.startswith(f"{ind}_")
                and c.split("_")[-1].isdigit()]
        if not cols:
            continue
        slim = df[["iso3", "country"] + cols].copy()
        tall = slim.melt(id_vars=["iso3", "country"],
                        value_vars=cols,
                        var_name="var_year", value_name="value")
        tall["year"] = tall["var_year"].str.extract(r"_(\d{4})$")[0].astype(int)
        tall["variable"] = {"hdi": "hdi", "le": "life_expectancy_hdr",
                            "eys": "exp_years_schooling",
                            "mys": "mean_years_schooling",
                            "gnipc": "gni_per_capita_ppp",
                            "gdi": "gender_dev_index",
                            "ihdi": "ihdi",
                            "gii": "gender_inequality_index"}[ind]
        tall["source"] = "UNDP_HDR"
        tall = tall.dropna(subset=["value"])
        long_frames.append(tall[["iso3", "country", "year",
                                 "variable", "value", "source"]])
    return pd.concat(long_frames, ignore_index=True)


# ---------------------------------------------------------------------------
# Hofstede (time-invariant, year = NaN sentinel = -1)
# ---------------------------------------------------------------------------
def load_hofstede() -> pd.DataFrame:
    path = RAW / "layer_c_hofstede" / "hofstede_6d.csv"
    df = pd.read_csv(path, sep=";")
    # The file uses 3-letter codes matching ISO3 mostly, with a few oddities
    df = df.rename(columns={"ctr": "iso3"})
    # Drop regional aggregates
    drops = {"AFE", "AFW", "AEA", "AMA", "AWE", "AWN", "GLO",
             "ARA", "EEU", "SEU", "ANZ", "CEE"}
    df = df[~df["iso3"].isin(drops)]
    dims = {"pdi": "hofstede_pdi", "idv": "hofstede_idv",
            "mas": "hofstede_mas", "uai": "hofstede_uai",
            "ltowvs": "hofstede_ltowvs", "ivr": "hofstede_ivr"}
    frames = []
    for src, dst in dims.items():
        if src not in df.columns:
            continue
        slim = df[["iso3", "country", src]].dropna(subset=[src]).copy()
        slim = slim.rename(columns={src: "value"})
        slim["variable"] = dst
        slim["year"] = -1  # sentinel: time-invariant
        slim["source"] = "Hofstede_6D_2015"
        slim["value"] = pd.to_numeric(slim["value"], errors="coerce")
        slim = slim.dropna(subset=["value"])
        frames.append(slim[["iso3", "country", "year",
                            "variable", "value", "source"]])
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------------------
# WHO GHO OData -> long
# ---------------------------------------------------------------------------
def load_who() -> pd.DataFrame:
    who_dir = RAW / "layer_c_who_gho"
    frames = []
    for jf in sorted(who_dir.glob("*.json")):
        payload = json.loads(jf.read_text())
        rows = payload.get("value", [])
        if not rows:
            continue
        name = jf.stem.split(".")[0]
        recs = []
        for r in rows:
            iso3 = r.get("SpatialDim")
            year = r.get("TimeDim")
            val = r.get("NumericValue")
            dim1 = r.get("Dim1")
            if not iso3 or len(iso3) != 3 or val is None or year is None:
                continue
            # For suicide: take both-sexes only (SEX_BTSX) to avoid triplication
            if dim1 is not None and dim1 not in (None, "SEX_BTSX"):
                continue
            recs.append({"iso3": iso3, "country": iso3,
                         "year": int(year), "value": float(val)})
        if not recs:
            continue
        df = pd.DataFrame(recs)
        # If duplicates (e.g., alcohol no Dim1), de-dup by mean
        df = df.groupby(["iso3", "country", "year"],
                        as_index=False)["value"].mean()
        df["variable"] = {"suicide_rate_age_std_per_100k": "suicide_rate",
                          "alcohol_per_capita_recorded_15plus":
                              "alcohol_per_capita"}.get(name, name)
        df["source"] = "WHO_GHO"
        frames.append(df[["iso3", "country", "year",
                          "variable", "value", "source"]])
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# ---------------------------------------------------------------------------
# OWID (includes Cantril ladder — canonical happiness)
# ---------------------------------------------------------------------------
def load_owid() -> pd.DataFrame:
    owid_dir = RAW / "layer_c_owid"
    map_ = {
        "happiness_cantril_ladder.csv":
            ("Self-reported life satisfaction", "cantril_ladder"),
        "share_of_individuals_using_the_internet.csv":
            ("Share of the population using the Internet", "internet_share_owid"),
        "gdp_per_capita_worldbank.csv":
            ("GDP per capita, PPP (constant 2017 international $)",
             "gdp_per_capita_ppp_owid"),
        "annual_working_hours_per_worker.csv":
            ("Average annual working hours per worker",
             "annual_working_hours"),
    }
    frames = []
    for fname, (col_guess, out_name) in map_.items():
        path = owid_dir / fname
        if not path.exists():
            continue
        df = pd.read_csv(path)
        df = df.rename(columns={"Entity": "country", "Code": "iso3",
                                "Year": "year"})
        # Drop regional aggregates (no ISO3 code)
        df = df.dropna(subset=["iso3"])
        # Find the value column
        val_col = None
        for c in df.columns:
            if c not in ("country", "iso3", "year"):
                val_col = c
                break
        if val_col is None:
            continue
        df = df.rename(columns={val_col: "value"})
        df["variable"] = out_name
        df["source"] = "OWID"
        df["year"] = df["year"].astype(int)
        df = df.dropna(subset=["value"])
        frames.append(df[["iso3", "country", "year",
                          "variable", "value", "source"]])
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------------------
# Gelfand 2011 tightness (time-invariant)
# ---------------------------------------------------------------------------
def load_gelfand() -> pd.DataFrame:
    df = pd.read_csv(RAW / "layer_c_auxiliary" / "gelfand2011_tightness.csv")
    df = df[df["iso3"].notna() & (df["iso3"].str.len() == 3)]
    out = df[["iso3", "country", "tightness_score"]].rename(
        columns={"tightness_score": "value"})
    out["variable"] = "gelfand_tightness"
    out["year"] = -1
    out["source"] = "Gelfand2011_Science"
    return out[["iso3", "country", "year", "variable", "value", "source"]]


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------
def main() -> None:
    print("[harmonize] World Bank...")
    wb = load_worldbank()
    print(f"  -> {len(wb):,} rows, {wb['iso3'].nunique()} countries,"
          f" {wb['variable'].nunique()} vars")

    print("[harmonize] UNDP HDR...")
    hdr = load_hdr()
    print(f"  -> {len(hdr):,} rows, {hdr['iso3'].nunique()} countries,"
          f" {hdr['variable'].nunique()} vars")

    print("[harmonize] Hofstede...")
    hof = load_hofstede()
    print(f"  -> {len(hof):,} rows, {hof['iso3'].nunique()} countries,"
          f" {hof['variable'].nunique()} vars")

    print("[harmonize] WHO GHO...")
    who = load_who()
    print(f"  -> {len(who):,} rows, {who['iso3'].nunique()} countries,"
          f" {who['variable'].nunique()} vars")

    print("[harmonize] OWID...")
    owid = load_owid()
    print(f"  -> {len(owid):,} rows, {owid['iso3'].nunique()} countries,"
          f" {owid['variable'].nunique()} vars")

    print("[harmonize] Gelfand...")
    gel = load_gelfand()
    print(f"  -> {len(gel):,} rows, {gel['iso3'].nunique()} countries")

    long = pd.concat([wb, hdr, hof, who, owid, gel], ignore_index=True)
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long = long.dropna(subset=["value"])

    # Write
    out_path = OUT / "layer_c_cross_national.parquet"
    long.to_parquet(out_path, compression="snappy")
    print(f"\n[OUT] {out_path}")
    print(f"  rows = {len(long):,}")
    print(f"  countries = {long['iso3'].nunique()}")
    print(f"  variables = {long['variable'].nunique()}")
    print(f"  year range = "
          f"{long[long['year']>0]['year'].min()}..{long['year'].max()}")

    # Variable coverage matrix
    cov = (long.groupby("variable")
               .agg(n_rows=("value", "size"),
                    n_countries=("iso3", "nunique"),
                    year_min=("year", lambda s: s[s > 0].min() if any(s>0) else np.nan),
                    year_max=("year", "max"))
               .sort_values("n_countries", ascending=False))
    cov.to_csv(OUT / "layer_c_variable_coverage.csv")
    print(f"  variable coverage -> {OUT / 'layer_c_variable_coverage.csv'}")


if __name__ == "__main__":
    main()
