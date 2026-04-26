"""
cultural_Gc.py
==============
A priori construction and sensitivity analysis of the cultural weighting
function G^c_{τ,y} for the Sweet Trap cross-cultural framework.

Purpose
-------
Red Team (2026-04-17) flagged G^c in §11.2 as a HARKing risk: the cultural
Fisher-runaway extension was motivated by C5 luxury data (hedonic-treadmill
failure + peer-norm coordination), and G^c was not pre-specified.  This script
constructs G^c from PUBLISHED a priori theory (Hofstede 2010, Schwartz 2006,
Gelfand 2011) WITHOUT looking at the outcome variable (σ_ST), then tests
whether G^c improves rank-stability of the P3 result relative to raw Δ_ST.

Decision rule (pre-specified here)
-----------------------------------
- If Spearman ρ(Δ_ST rank with G^c weighting, Δ_ST rank without) ≥ 0.80:
  G^c is stable → RETAIN with transparency note.
- If ρ < 0.80: G^c materially reorders the cross-cultural pattern → report
  honestly; either simplify or delete depending on whether G^c-weighted or
  raw version better fits theoretical prediction.

Data sources
------------
- Hofstede 6D: /Volumes/P1/城市研究/01-个体调查/跨国/hofstede/hofstede_6d.csv
  (111 countries, IDV / PDI / UAI / LTOWVS / MAS / IVR)
- Existing country panel: 03-analysis/models/layer_c_p3_country_panel.csv
  (255 countries, σ_ST + τ_env + τ_adapt already computed)
- ISSP country trajectory:
  02-data/processed/issp_country_merged_with_prior.csv
  (53 countries: Δ_ST aspirational velocity from ISSP + σ_ST)

Author: Claude (Literature Specialist agent), 2026-04-18
"""

import os
import warnings
import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = "/Users/andy/Desktop/Research/sweet-trap-multidomain"
P1   = "/Volumes/P1/城市研究/01-个体调查/跨国"

HOFSTEDE_PATH = f"{P1}/hofstede/hofstede_6d.csv"
PANEL_PATH    = f"{BASE}/03-analysis/models/layer_c_p3_country_panel.csv"
ISSP_MERGED   = f"{BASE}/02-data/processed/issp_country_merged_with_prior.csv"

OUT_DIR       = f"{BASE}/03-analysis/models"
os.makedirs(OUT_DIR, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────
# §1  A PRIORI CONSTRUCTION OF G^c
# ──────────────────────────────────────────────────────────────────────────
# Theory basis (pre-specified, not derived from outcome data):
#
# G^c is the cultural weighting function that modulates how strongly the
# "cultural runaway" dynamic (G^cultural_{τ,y}, Eq. L1' in formal model v2
# §11.2) amplifies the Sweet Trap signal in human societies.
#
# Three Hofstede dimensions carry a priori theoretical relevance:
#
# (A) IDV — Individualism
#     High IDV: personal reward signals dominate social signals.
#     Cultural runaway (M2 peer-norm mechanism, F3) WEAKENS in high-IDV
#     societies because peer-endorsement feedback loops are weaker.
#     → G^c should DECREASE as IDV increases (inverse relationship).
#     Theoretical basis: Triandis (1995) individualism-collectivism;
#     Hofstede (2010) Ch.4; Heine et al. (2002) WEIRD-validity JPSP.
#
# (B) PDI — Power Distance
#     High PDI: hierarchical norm transmission is strong; norms propagate
#     top-down without questioning.  This amplifies M3 trans-generational
#     norm inheritance (F3 mechanism for C4 彩礼 and C2 鸡娃).
#     → G^c should INCREASE as PDI increases.
#     Theoretical basis: Hofstede (2010) Ch.3; House et al. (2004) GLOBE;
#     Markus & Kitayama (1991) self-construal.
#
# (C) LTOWVS — Long-Term Orientation
#     High LTO: future-oriented, perseverance values — paradoxically RAISES
#     tolerance for long-deferred costs.  High LTO societies can sustain
#     Sweet Traps longer because cost-deferral (F4: T_cost >> T_reward)
#     is culturally legitimated.
#     → G^c should INCREASE as LTOWVS increases.
#     Theoretical basis: Hofstede (2010) Ch.7 (originally labeled CVS);
#     Schwartz (2006) PB / "embeddedness" vs "autonomy" axis maps onto
#     LTO in the collectivist direction; Twenge et al. (2010) cultural
#     changes in materialism.
#
# Formula (a priori, derived from theory, not fitted to outcome):
#
#   G^c_i = z(PDI_i) + z(LTOWVS_i) - z(IDV_i)
#
# This is a unit-weighted additive combination — no empirical weights.
# Each dimension z-scored to equalize scale.  No intercept (G^c is a
# relative moderator, not an absolute scale).
#
# NOTE: IVR (Indulgence vs Restraint) was considered but excluded on
# a priori grounds: IVR measures gratification of desires, which
# conflates with the F2 endorsement condition itself, not with the
# cultural runaway amplifier.  Including IVR would introduce circularity.
#
# Schwartz (2006) 10-value theory independently supports the same axis:
# "Embeddedness" (collectivism + hierarchy) maps onto high PDI + low IDV;
# "Intellectual Autonomy" and "Affective Autonomy" map onto high IDV.
# "Hierarchy" value type maps onto high PDI.  Convergent validity.
# ──────────────────────────────────────────────────────────────────────────

def load_hofstede():
    """Load Hofstede 6D; handle #NULL! missing values; z-score each column."""
    df = pd.read_csv(HOFSTEDE_PATH, sep=";", na_values=["#NULL!"])
    # Rename columns to standard
    df.columns = [c.lower().strip() for c in df.columns]
    # ctr is Hofstede ISO3-like code; not standard ISO3 — need a mapping
    return df


def hofstede_to_iso2():
    """
    Hofstede uses its own 3-letter codes (e.g., AUL for Australia, GBR for UK).
    Map to standard ISO-2 for joining with the country panel.
    This mapping covers the 111 Hofstede countries.
    """
    mapping = {
        "AFE": None, "AFW": None,  # regional aggregates — skip
        "ALB": "AL", "ALG": "DZ", "AND": "AD", "ARA": None,  # regional
        "ARG": "AR", "ARM": "AM", "AUL": "AU", "AUT": "AT",
        "AZE": "AZ", "BAN": "BD", "BEL": "BE", "BIH": "BA",
        "BRA": "BR", "BUL": "BG", "BUR": "MM", "CAN": "CA",
        "CHI": "CN", "CHL": "CL", "CHN": "CN", "COL": "CO", "COS": "CR",
        "CRO": "HR", "CZE": "CZ", "DEN": "DK", "DOM": "DO",
        "EAF": None, "ECU": "EC", "EGY": "EG", "ELS": "SV",
        "EST": "EE", "ETH": "ET", "FIN": "FI", "FRA": "FR",
        "GBR": "GB", "GER": "DE", "GHA": "GH", "GRE": "GR",
        "GUA": "GT", "HKG": "HK", "HON": "HN", "HUN": "HU",
        "IDO": "ID", "IND": "IN", "IRA": "IR", "IRE": "IE",
        "ISR": "IL", "ITA": "IT", "JAM": "JM", "JPN": "JP",
        "KAZ": "KZ", "KOR": "KR", "KWT": "KW", "LAO": "LA",
        "LAT": "LV", "LEB": "LB", "LIT": "LT", "LUX": "LU",
        "MAC": "MO", "MAL": "MY", "MAT": "MT", "MEX": "MX",
        "MON": "MD", "MOR": "MA", "MOZ": "MZ", "NAM": "NA",
        "NET": "NL", "NOR": "NO", "NZL": "NZ", "PAK": "PK",
        "PAN": "PA", "PER": "PE", "PHI": "PH", "POL": "PL",
        "POR": "PT", "PUE": "PR", "ROM": "RO", "RUS": "RU",
        "SAF": "ZA", "SAR": "SA", "SCO": None,  # Scotland subset of GBR
        "SER": "RS", "SIN": "SG", "SLO": "SK", "SLV": "SI",
        "SPA": "ES", "SRI": "LK", "SUR": "SR", "SWE": "SE",
        "SWI": "CH", "TAI": "TW", "TAN": "TZ", "THA": "TH",
        "TRI": "TT", "TUR": "TR", "UKR": "UA", "URU": "UY",
        "USA": "US", "VEN": "VE", "VIE": "VN", "WAF": None,
        "ZIM": "ZW", "ZAM": "ZM",
    }
    return mapping


def build_gc_scores(df_hof, mapping):
    """
    Construct G^c for each country.
    Formula: G^c = z(PDI) + z(LTOWVS) - z(IDV)
    Returns DataFrame with iso2, ctr, country, pdi, idv, ltowvs, gc_raw, gc_z.
    """
    df = df_hof.copy()
    df["iso2"] = df["ctr"].map(mapping)
    df = df[df["iso2"].notna()].copy()

    # Require all three dimensions
    required = ["pdi", "idv", "ltowvs"]
    df_valid = df.dropna(subset=required).copy()

    # Z-score each dimension on this sample
    for col in required:
        df_valid[f"z_{col}"] = stats.zscore(df_valid[col].astype(float))

    # A priori formula: PDI + LTOWVS - IDV
    df_valid["gc_raw"] = df_valid["z_pdi"] + df_valid["z_ltowvs"] - df_valid["z_idv"]
    df_valid["gc_z"]   = stats.zscore(df_valid["gc_raw"])

    return df_valid[["iso2", "ctr", "country", "pdi", "idv", "ltowvs",
                     "z_pdi", "z_idv", "z_ltowvs", "gc_raw", "gc_z"]].copy()


# ──────────────────────────────────────────────────────────────────────────
# §2  LOAD EXISTING ANALYSIS DATA
# ──────────────────────────────────────────────────────────────────────────

def load_country_panel():
    df = pd.read_csv(PANEL_PATH)
    # iso3 → iso2 conversion (use pycountry if available; otherwise manual)
    iso3_to_iso2 = {
        "AFG":"AF","ALB":"AL","DZA":"DZ","AND":"AD","AGO":"AO","ARG":"AR",
        "ARM":"AM","AUS":"AU","AUT":"AT","AZE":"AZ","BHS":"BS","BHR":"BH",
        "BGD":"BD","BLR":"BY","BEL":"BE","BLZ":"BZ","BEN":"BJ","BTN":"BT",
        "BOL":"BO","BIH":"BA","BWA":"BW","BRA":"BR","BRN":"BN","BGR":"BG",
        "BFA":"BF","BDI":"BI","CPV":"CV","KHM":"KH","CMR":"CM","CAN":"CA",
        "CAF":"CF","TCD":"TD","CHL":"CL","CHN":"CN","COL":"CO","COM":"KM",
        "COD":"CD","COG":"CG","CRI":"CR","CIV":"CI","HRV":"HR","CUB":"CU",
        "CYP":"CY","CZE":"CZ","DNK":"DK","DJI":"DJ","DOM":"DO","ECU":"EC",
        "EGY":"EG","SLV":"SV","GNQ":"GQ","ERI":"ER","EST":"EE","SWZ":"SZ",
        "ETH":"ET","FJI":"FJ","FIN":"FI","FRA":"FR","GAB":"GA","GMB":"GM",
        "GEO":"GE","DEU":"DE","GHA":"GH","GRC":"GR","GTM":"GT","GIN":"GN",
        "GNB":"GW","GUY":"GY","HTI":"HT","HND":"HN","HKG":"HK","HUN":"HU",
        "ISL":"IS","IND":"IN","IDN":"ID","IRN":"IR","IRQ":"IQ","IRL":"IE",
        "ISR":"IL","ITA":"IT","JAM":"JM","JPN":"JP","JOR":"JO","KAZ":"KZ",
        "KEN":"KE","PRK":"KP","KOR":"KR","KWT":"KW","KGZ":"KG","LAO":"LA",
        "LVA":"LV","LBN":"LB","LSO":"LS","LBR":"LR","LBY":"LY","LIE":"LI",
        "LTU":"LT","LUX":"LU","MDG":"MG","MWI":"MW","MYS":"MY","MDV":"MV",
        "MLI":"ML","MLT":"MT","MRT":"MR","MUS":"MU","MEX":"MX","MDA":"MD",
        "MCO":"MC","MNG":"MN","MNE":"ME","MAR":"MA","MOZ":"MZ","MMR":"MM",
        "NAM":"NA","NPL":"NP","NLD":"NL","NZL":"NZ","NIC":"NI","NER":"NE",
        "NGA":"NG","MKD":"MK","NOR":"NO","OMN":"OM","PAK":"PK","PAN":"PA",
        "PNG":"PG","PRY":"PY","PER":"PE","PHL":"PH","POL":"PL","PRT":"PT",
        "QAT":"QA","ROU":"RO","RUS":"RU","RWA":"RW","SAU":"SA","SEN":"SN",
        "SRB":"RS","SLE":"SL","SGP":"SG","SVK":"SK","SVN":"SI","SOM":"SO",
        "ZAF":"ZA","SSD":"SS","ESP":"ES","LKA":"LK","SDN":"SD","SUR":"SR",
        "SWE":"SE","CHE":"CH","SYR":"SY","TWN":"TW","TJK":"TJ","TZA":"TZ",
        "THA":"TH","TLS":"TL","TGO":"TG","TTO":"TT","TUN":"TN","TUR":"TR",
        "TKM":"TM","UGA":"UG","UKR":"UA","ARE":"AE","GBR":"GB","USA":"US",
        "URY":"UY","UZB":"UZ","VEN":"VE","VNM":"VN","YEM":"YE","ZMB":"ZM",
        "ZWE":"ZW","MAC":"MO","MHL":"MH","KIR":"KI","PLW":"PW","VUT":"VU",
        "WSM":"WS","TON":"TO","FSM":"FM","NRU":"NR","TUV":"TV","KNA":"KN",
        "ATG":"AG","DMA":"DM","GRD":"GD","LCA":"LC","VCT":"VC","BRB":"BB",
        "TCA":"TC","CUW":"CW","SXM":"SX","BES":"BQ","ABW":"AW",
    }
    df["iso2"] = df["iso3"].map(iso3_to_iso2)
    return df


def load_issp_merged():
    """Load ISSP merged file if available."""
    try:
        df = pd.read_csv(ISSP_MERGED)
        return df
    except FileNotFoundError:
        return None


# ──────────────────────────────────────────────────────────────────────────
# §3  MERGE AND COMPUTE G^c-WEIGHTED Δ_ST
# ──────────────────────────────────────────────────────────────────────────

def build_analysis_frame(gc_scores, panel, issp_df):
    """
    Join G^c with:
      (a) σ_ST (country-level aggregate Sweet Trap severity)
      (b) Raw Δ_ST proxy: τ_env_internet (inverse; faster internet → higher Δ_ST)
      (c) ISSP aspirational velocity (delta_z_aspirational) if available

    G^c weighting of raw Δ_ST:
      Δ_ST_weighted = Δ_ST_raw × (1 + α × G^c_z)
    where α = 0.5 (a priori moderate weight; not fitted).
    This shrinks differences for low-G^c countries without zeroing them out.
    """
    # Merge gc into panel on iso2
    merged = panel.merge(
        gc_scores[["iso2", "gc_z", "pdi", "idv", "ltowvs", "gc_raw"]],
        on="iso2", how="left"
    )

    # Raw Δ_ST proxy: invert τ_env_internet so shorter time = higher Δ_ST
    # (countries with fast internet penetration = higher trap signal)
    merged["delta_st_raw"] = -np.log1p(
        merged["tau_env_internet"].fillna(merged["tau_env_internet"].median())
    )
    merged["delta_st_raw_z"] = stats.zscore(
        merged["delta_st_raw"].fillna(merged["delta_st_raw"].median())
    )

    # G^c-weighted Δ_ST (with α = 0.5)
    alpha = 0.5
    gc_fill = merged["gc_z"].fillna(0)  # neutral weight for countries without G^c
    merged["delta_st_weighted"] = merged["delta_st_raw_z"] * (1 + alpha * gc_fill)
    merged["delta_st_weighted_z"] = stats.zscore(
        merged["delta_st_weighted"].fillna(0)
    )

    # Merge ISSP if available (gives a second, independent Δ_ST proxy)
    if issp_df is not None and "delta_z_aspirational" in issp_df.columns:
        # ISSP uses iso2 directly
        issp_sub = issp_df[["iso2", "delta_z_aspirational",
                             "sigma_st"]].copy() if "iso2" in issp_df.columns else None
        if issp_sub is not None:
            # Rename ISSP sigma_st to avoid conflict
            issp_sub = issp_sub.rename(columns={
                "delta_z_aspirational": "issp_delta_z_asp",
                "sigma_st": "issp_sigma_st"
            })
            merged = merged.merge(issp_sub, on="iso2", how="left")

    return merged


# ──────────────────────────────────────────────────────────────────────────
# §4  SENSITIVITY ANALYSIS — Spearman rank stability
# ──────────────────────────────────────────────────────────────────────────

def sensitivity_analysis(df, outcome_col="sigma_st"):
    """
    Core test: does G^c weighting materially reorder the P3 prediction?

    We test the P3 regression β (Δ_ST → σ_ST) with raw vs G^c-weighted Δ_ST
    and report Spearman ρ between the two ranked Δ_ST vectors.

    Decision threshold: ρ ≥ 0.80 → G^c is rank-stable → retain.
    """
    results = {}

    # Filter to complete cases
    df_clean = df.dropna(subset=[outcome_col, "delta_st_raw_z",
                                 "delta_st_weighted_z"]).copy()
    n = len(df_clean)

    # Rank correlation between raw and weighted Δ_ST
    rho, p_rho = stats.spearmanr(
        df_clean["delta_st_raw_z"],
        df_clean["delta_st_weighted_z"]
    )
    results["spearman_rho_raw_vs_gc_weighted"] = float(rho)
    results["spearman_rho_p"] = float(p_rho)
    results["n_complete"] = int(n)
    results["decision_threshold"] = 0.80
    results["decision"] = "RETAIN" if rho >= 0.80 else "REVIEW"

    # OLS regression: raw Δ_ST → σ_ST
    x_raw = df_clean["delta_st_raw_z"].values
    y     = df_clean[outcome_col].values
    beta_raw, intercept_raw, r_raw, p_raw, se_raw = stats.linregress(x_raw, y)
    results["beta_raw"]     = float(beta_raw)
    results["p_raw"]        = float(p_raw)
    results["r_raw"]        = float(r_raw)
    results["r2_raw"]       = float(r_raw ** 2)

    # OLS regression: G^c-weighted Δ_ST → σ_ST
    x_gc = df_clean["delta_st_weighted_z"].values
    beta_gc, intercept_gc, r_gc, p_gc, se_gc = stats.linregress(x_gc, y)
    results["beta_gc"]      = float(beta_gc)
    results["p_gc"]         = float(p_gc)
    results["r_gc"]         = float(r_gc)
    results["r2_gc"]        = float(r_gc ** 2)

    # Gain in R²
    results["delta_r2"] = float(r_gc**2 - r_raw**2)

    # Also test on ISSP subsample if available
    if "issp_delta_z_asp" in df_clean.columns:
        df_issp = df_clean.dropna(subset=["issp_delta_z_asp",
                                          "issp_sigma_st"]).copy()
        n_issp = len(df_issp)
        if n_issp >= 15:
            # G^c-weighted ISSP velocity
            gc_fill_issp = df_issp["gc_z"].fillna(0)
            df_issp["issp_delta_gc"] = df_issp["issp_delta_z_asp"] * (1 + 0.5 * gc_fill_issp)
            df_issp["issp_delta_gc_z"] = stats.zscore(df_issp["issp_delta_gc"])

            rho_issp, p_rho_issp = stats.spearmanr(
                df_issp["issp_delta_z_asp"],
                df_issp["issp_delta_gc_z"]
            )
            b_raw_i, _, r_i_r, p_i_r, _ = stats.linregress(
                df_issp["issp_delta_z_asp"].values,
                df_issp["issp_sigma_st"].values
            )
            b_gc_i, _, r_i_gc, p_i_gc, _ = stats.linregress(
                df_issp["issp_delta_gc_z"].values,
                df_issp["issp_sigma_st"].values
            )

            results["issp_n"]                    = int(n_issp)
            results["issp_spearman_rho"]          = float(rho_issp)
            results["issp_spearman_p"]            = float(p_rho_issp)
            results["issp_beta_raw"]              = float(b_raw_i)
            results["issp_p_raw"]                 = float(p_i_r)
            results["issp_r2_raw"]                = float(r_i_r**2)
            results["issp_beta_gc_weighted"]      = float(b_gc_i)
            results["issp_p_gc"]                  = float(p_i_gc)
            results["issp_r2_gc"]                 = float(r_i_gc**2)
            results["issp_decision"]              = (
                "RETAIN" if rho_issp >= 0.80 else "REVIEW"
            )

    return results, df_clean


# ──────────────────────────────────────────────────────────────────────────
# §5  PER-COUNTRY G^c COEFFICIENT TABLE
# ──────────────────────────────────────────────────────────────────────────

def top_gc_table(gc_scores, n=35):
    """Return top and bottom countries by G^c_z."""
    df = gc_scores.sort_values("gc_z", ascending=False)
    top    = df.head(n)
    bottom = df.tail(10)
    return top, bottom


# ──────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────

def main():
    import json

    print("=" * 70)
    print("G^c CALIBRATION — Sweet Trap Cultural Weighting Function")
    print("=" * 70)

    # 1. Load Hofstede
    df_hof  = load_hofstede()
    mapping = hofstede_to_iso2()
    gc_scores = build_gc_scores(df_hof, mapping)
    print(f"\n[1] G^c constructed for {len(gc_scores)} countries "
          f"(Hofstede PDI + LTOWVS - IDV, unit-weighted z-scores)")

    # 2. Load panel + ISSP
    panel   = load_country_panel()
    issp_df = load_issp_merged()
    if issp_df is not None:
        print(f"[2] ISSP merged file loaded: {len(issp_df)} rows")
    else:
        print("[2] ISSP merged file not found; will run on panel-only")

    # 3. Build analysis frame
    analysis_df = build_analysis_frame(gc_scores, panel, issp_df)
    print(f"[3] Analysis frame: {len(analysis_df)} countries; "
          f"G^c available for "
          f"{analysis_df['gc_z'].notna().sum()} countries")

    # 4. G^c coefficient table (top 35)
    top_gc, bottom_gc = top_gc_table(gc_scores, n=35)
    print(f"\n[4] Top 10 countries by G^c (high cultural runaway amplification):")
    for _, row in top_gc.head(10).iterrows():
        print(f"    {row['iso2']:4s}  {row['country'][:22]:22s}"
              f"  PDI={int(row['pdi']):3d} IDV={int(row['idv']):3d}"
              f" LTO={int(row['ltowvs']):3d}  G^c_z={row['gc_z']:+.3f}")
    print(f"\n    Bottom 5 countries by G^c (low cultural runaway amplification):")
    for _, row in bottom_gc.tail(5).iterrows():
        print(f"    {row['iso2']:4s}  {row['country'][:22]:22s}"
              f"  PDI={int(row['pdi']):3d} IDV={int(row['idv']):3d}"
              f" LTO={int(row['ltowvs']):3d}  G^c_z={row['gc_z']:+.3f}")

    # 5. Sensitivity analysis
    print("\n[5] Sensitivity analysis:")
    sensitivity, df_clean = sensitivity_analysis(analysis_df)

    print(f"\n    --- Primary test (n={sensitivity['n_complete']}) ---")
    print(f"    Spearman ρ(raw Δ_ST, G^c-weighted Δ_ST) = "
          f"{sensitivity['spearman_rho_raw_vs_gc_weighted']:.4f} "
          f"(p={sensitivity['spearman_rho_p']:.4f})")
    print(f"    Decision threshold: ρ ≥ {sensitivity['decision_threshold']}")
    print(f"    *** DECISION: {sensitivity['decision']} ***")
    print(f"\n    β (raw Δ_ST → σ_ST):          {sensitivity['beta_raw']:+.4f}  "
          f"p={sensitivity['p_raw']:.4f}  R²={sensitivity['r2_raw']:.4f}")
    print(f"    β (G^c-weighted Δ_ST → σ_ST): {sensitivity['beta_gc']:+.4f}  "
          f"p={sensitivity['p_gc']:.4f}  R²={sensitivity['r2_gc']:.4f}")
    print(f"    ΔR² from G^c weighting: {sensitivity['delta_r2']:+.4f}")

    if "issp_n" in sensitivity:
        print(f"\n    --- ISSP subsample test (n={sensitivity['issp_n']}) ---")
        print(f"    Spearman ρ(ISSP Δz raw, G^c-weighted) = "
              f"{sensitivity['issp_spearman_rho']:.4f} "
              f"(p={sensitivity['issp_spearman_p']:.4f})")
        print(f"    β (raw ISSP Δz → σ_ST):          "
              f"{sensitivity['issp_beta_raw']:+.4f}  "
              f"p={sensitivity['issp_p_raw']:.4f}  "
              f"R²={sensitivity['issp_r2_raw']:.4f}")
        print(f"    β (G^c-weighted ISSP Δz → σ_ST): "
              f"{sensitivity['issp_beta_gc_weighted']:+.4f}  "
              f"p={sensitivity['issp_p_gc']:.4f}  "
              f"R²={sensitivity['issp_r2_gc']:.4f}")
        print(f"    *** ISSP DECISION: {sensitivity['issp_decision']} ***")

    # 6. Per-country G^c table (save)
    gc_full = gc_scores[["iso2", "ctr", "country",
                          "pdi", "idv", "ltowvs",
                          "gc_raw", "gc_z"]].sort_values("gc_z", ascending=False)
    gc_out_path = f"{OUT_DIR}/cultural_gc_coefficients.csv"
    gc_full.to_csv(gc_out_path, index=False, float_format="%.4f")
    print(f"\n[6] G^c coefficient table saved → {gc_out_path}")

    # 7. Full analysis frame (save)
    analysis_out = f"{OUT_DIR}/cultural_gc_analysis_frame.csv"
    cols_to_save = ["iso2", "iso3", "country", "sigma_st",
                    "delta_st_raw_z", "delta_st_weighted_z",
                    "gc_z", "gc_raw",
                    "tau_env_internet", "hofstede_uai", "hofstede_ltowvs",
                    "hofstede_pdi", "gelfand_tightness"]
    if "issp_delta_z_asp" in analysis_df.columns:
        cols_to_save += ["issp_delta_z_asp", "issp_sigma_st"]
    save_cols = [c for c in cols_to_save if c in analysis_df.columns]
    analysis_df[save_cols].to_csv(analysis_out, index=False, float_format="%.4f")
    print(f"[7] Full analysis frame saved → {analysis_out}")

    # 8. Results JSON
    results_payload = {
        "script": "cultural_Gc.py",
        "date": "2026-04-18",
        "gc_formula": "G^c_i = z(PDI_i) + z(LTOWVS_i) - z(IDV_i)",
        "gc_alpha_weight": 0.5,
        "theoretical_basis": {
            "PDI": "+z: high power distance amplifies M3 trans-generational norm lock-in (Hofstede 2010 Ch.3; House et al. 2004 GLOBE)",
            "IDV": "-z: high individualism weakens M2 peer-norm feedback loop (Triandis 1995; Heine et al. 2002)",
            "LTOWVS": "+z: high long-term orientation legitimates cost-deferral (F4 T_cost>>T_reward; Hofstede 2010 Ch.7; Schwartz 2006 embeddedness)",
            "IVR_excluded": "IVR conflates with F2 endorsement condition; excluded to avoid circularity"
        },
        "n_countries_gc": len(gc_scores),
        "sensitivity": sensitivity
    }
    json_path = f"{OUT_DIR}/cultural_gc_results.json"
    with open(json_path, "w") as f:
        json.dump(results_payload, f, indent=2)
    print(f"[8] Results JSON saved → {json_path}")

    return results_payload, gc_full, sensitivity


if __name__ == "__main__":
    results, gc_table, sensitivity = main()
