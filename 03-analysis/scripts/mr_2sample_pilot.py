#!/usr/bin/env python3
"""
mr_2sample_pilot.py
===================
Pure-Python 2-sample MR implementation for Sweet Trap Layer D.

Why Python rather than R/TwoSampleMR?
    The R TwoSampleMR::extract_instruments() requires a 2024-05+ IEU OpenGWAS
    JWT token we do not have. Instead:
      * Exposure IVs come from EBI GWAS Catalog REST API (mr_extract_ivs_ebi.py),
        already p<5e-8 and curated lead SNPs (approximate LD independence).
      * Outcome betas come from Finngen R12 summary stats (local gz files).
      * Harmonisation + MR estimators implemented from first principles with scipy.

MR estimators implemented:
    1) IVW random-effects (inverse-variance weighted, multiplicative RE)
    2) Simple median
    3) Weighted median
    4) MR-Egger regression (with intercept = pleiotropy test)
    5) Cochran Q
    6) Leave-one-out IVW
    7) Steiger directionality (Hemani 2017)

Outputs:
    02-data/processed/mr_results_all_chains.csv
    02-data/processed/mr_harmonised_data.parquet
    02-data/processed/mr_loo_<chain>.csv
    03-analysis/scripts/mr_2sample_pilot.log

Compute:
    * Sequential outcome processing (one Finngen gz at a time).
    * n_workers=1 throughout.
"""
from __future__ import annotations
import os, sys, gzip, io, logging, math, time
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import numpy as np
import pandas as pd
from scipy import stats

PROJ   = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
FINDIR = Path("/Volumes/P1/城市研究/UKB_芬兰Finngen_catalog_ieu/gwas_list/Finngen/R12_summary_stats")
OUT    = PROJ / "02-data/processed"
LOGP   = PROJ / "03-analysis/scripts/mr_2sample_pilot.log"

logging.basicConfig(filename=LOGP, level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
_h = logging.StreamHandler(sys.stdout)
_h.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
logging.getLogger().addHandler(_h)
log = logging.getLogger()

# ------------------------------------------------------------------
# 1. Chain definitions
# ------------------------------------------------------------------
@dataclass
class Chain:
    id: str
    exposure_label: str
    iv_file: str                # IV csv filename (in OUT)
    outcome_label: str
    outcome_phenocode: str
    outcome_ncase: int
    outcome_nctrl: int

CHAINS = [
    # Chain 1: risk-taking -> depression / antidepressants
    Chain("1a",  "risk_tolerance",         "mr_iv_risk_tolerance_GCST006810.csv",      "F5_DEPRESSIO",    "F5_DEPRESSIO",    59333,  434831),
    Chain("1b",  "risk_tolerance",         "mr_iv_risk_tolerance_GCST006810.csv",      "ANTIDEPRESSANTS", "ANTIDEPRESSANTS", 149403, 111976),
    Chain("1c",  "risk_tolerance",         "mr_iv_risk_tolerance_GCST006810.csv",      "F5_ANXIETY",      "F5_ANXIETY",      24643,  444414),
    # Chain 2: drinks/week -> alcohol pathology
    Chain("2a",  "drinks_per_week",        "mr_iv_drinks_per_week_GCST007461.csv",      "ALCOPANCCHRON",   "ALCOPANCCHRON",   2400,   497948),
    Chain("2b",  "drinks_per_week",        "mr_iv_drinks_per_week_GCST007461.csv",      "K11_ALCOLIV",     "K11_ALCOLIV",     3769,   485213),
    Chain("2c",  "drinks_per_week",        "mr_iv_drinks_per_week_GCST007461.csv",      "C3_HEP_EXALLC",   "C3_HEPATOCELLU_CARC_EXALLC", 947, 378749),
    # Chain 3: BMI -> diabetes nephropathy / stroke / T2D
    Chain("3a",  "bmi_locke2015",          "mr_iv_bmi_locke2015_GCST002783.csv",        "DM_NEPHROPATHY",  "DM_NEPHROPATHY",  5579,   90951),
    Chain("3b",  "bmi_locke2015",          "mr_iv_bmi_locke2015_GCST002783.csv",        "C_STROKE",        "C_STROKE",        53492,  360342),
    Chain("3c",  "bmi_locke2015",          "mr_iv_bmi_locke2015_GCST002783.csv",        "T2D",             "T2D",             82878,  403489),
    # Chain 4: insomnia -> depression
    Chain("4a",  "insomnia_jansen2019",    "mr_iv_insomnia_jansen2019_GCST007800.csv",  "F5_DEPRESSIO",    "F5_DEPRESSIO",    59333,  434831),
    Chain("4b",  "insomnia_jansen2019",    "mr_iv_insomnia_jansen2019_GCST007800.csv",  "F5_ANXIETY",      "F5_ANXIETY",      24643,  444414),
    # Chain 5: positive control - EA -> depression (known inverse)
    Chain("5",   "years_of_schooling",     "mr_iv_years_of_schooling_GCST006572.csv",   "F5_DEPRESSIO",    "F5_DEPRESSIO",    59333,  434831),
    # Chain 6: SWB -> depression (small n)
    Chain("6",   "subjective_wellbeing",   "mr_iv_subjective_wellbeing_GCST003766.csv", "F5_DEPRESSIO",    "F5_DEPRESSIO",    59333,  434831),
    # Chain 7: smoking initiation -> alcoholic liver (D_alcohol sensitivity)
    Chain("7",   "smoking_initiation",     "mr_iv_smoking_initiation_GCST007474.csv",   "K11_ALCOLIV",     "K11_ALCOLIV",     3769,   485213),
]

# ------------------------------------------------------------------
# 2. MR estimators
# ------------------------------------------------------------------
def ivw_random(bx, by, se_by, se_bx=None):
    """Inverse variance weighted, random-effects (Burgess 2013).
    Returns dict with beta, se, z, p, Q, Q_df, Q_p, I2.
    """
    bx = np.asarray(bx, float); by = np.asarray(by, float); se_by = np.asarray(se_by, float)
    w = 1.0 / (se_by**2)
    # Wald ratios
    wr = by / bx
    # IVW fixed
    beta_fe = np.sum(w * bx * by) / np.sum(w * bx**2)
    se_fe   = 1.0 / math.sqrt(np.sum(w * bx**2))
    # Cochran Q on Wald ratios (Bowden 2016 style)
    Q = np.sum(w * bx**2 * (wr - beta_fe)**2)
    df = len(bx) - 1
    Qp = 1 - stats.chi2.cdf(Q, df) if df > 0 else np.nan
    # random-effects (multiplicative over-dispersion)
    phi = max(Q / df, 1.0) if df > 0 else 1.0
    se_re = se_fe * math.sqrt(phi)
    I2 = max((Q - df) / Q, 0.0) if Q > 0 else 0.0
    z = beta_fe / se_re
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return dict(method="IVW_random", b=beta_fe, se=se_re, z=z, pval=p,
                Q=Q, Q_df=df, Q_pval=Qp, I2=I2, nsnp=len(bx), phi=phi)

def weighted_median_ratio(bx, by, se_by, B=1000, seed=42):
    """Weighted median with bootstrap SE (Bowden 2016)."""
    rng = np.random.default_rng(seed)
    bx = np.asarray(bx, float); by = np.asarray(by, float); se_by = np.asarray(se_by, float)
    wr = by / bx
    w  = (bx**2) / (se_by**2)           # weight = 1/var(Wald)=bx^2/se_by^2
    def wmed(vals, wts):
        idx = np.argsort(vals); v = vals[idx]; wt = wts[idx]
        cum = np.cumsum(wt) / np.sum(wt)
        return np.interp(0.5, cum, v)
    est = wmed(wr, w)
    # bootstrap SE (param bootstrap on by; keep bx fixed)
    boots = []
    for _ in range(B):
        by_b = by + rng.normal(0, se_by)
        wr_b = by_b / bx
        boots.append(wmed(wr_b, w))
    se = np.std(boots, ddof=1)
    z = est / se if se > 0 else np.nan
    p = 2 * (1 - stats.norm.cdf(abs(z))) if se > 0 else np.nan
    return dict(method="weighted_median", b=est, se=se, z=z, pval=p, nsnp=len(bx))

def simple_median(bx, by, se_by, B=1000, seed=43):
    rng = np.random.default_rng(seed)
    bx = np.asarray(bx, float); by = np.asarray(by, float); se_by = np.asarray(se_by, float)
    wr = by / bx
    est = np.median(wr)
    boots = []
    for _ in range(B):
        wr_b = (by + rng.normal(0, se_by)) / bx
        boots.append(np.median(wr_b))
    se = np.std(boots, ddof=1)
    z = est/se if se>0 else np.nan
    p = 2*(1-stats.norm.cdf(abs(z))) if se>0 else np.nan
    return dict(method="simple_median", b=est, se=se, z=z, pval=p, nsnp=len(bx))

def mr_egger(bx, by, se_by):
    """MR-Egger weighted regression: by = intercept + slope*bx; weights=1/se_by^2.
    Intercept test = pleiotropy; slope = causal estimate adjusted.
    Uses statsmodels via numpy (implement from scratch).
    """
    import numpy.linalg as la
    bx = np.asarray(bx, float); by = np.asarray(by, float); se_by = np.asarray(se_by, float)
    # orient by alignment: flip so bx>=0
    sign = np.where(bx < 0, -1.0, 1.0)
    bx_o = bx * sign; by_o = by * sign
    w = 1.0 / (se_by**2)
    X = np.column_stack([np.ones_like(bx_o), bx_o])
    W = np.diag(w)
    XtWX = X.T @ W @ X
    XtWy = X.T @ W @ by_o
    try:
        beta = la.solve(XtWX, XtWy)
    except la.LinAlgError:
        return dict(method="MR_Egger", b=np.nan, se=np.nan, intercept=np.nan,
                    intercept_se=np.nan, intercept_p=np.nan, pval=np.nan, nsnp=len(bx))
    intercept, slope = beta
    # residual variance
    resid = by_o - X @ beta
    # MR-Egger convention: use residual standard error with df-2
    df = len(bx) - 2
    if df <= 0:
        return dict(method="MR_Egger", b=slope, se=np.nan, intercept=intercept,
                    intercept_se=np.nan, intercept_p=np.nan, pval=np.nan, nsnp=len(bx))
    sigma2 = max(np.sum(w * resid**2) / df, 1.0)  # equivalent of phi >=1
    cov = sigma2 * la.inv(XtWX)
    int_se, slope_se = math.sqrt(cov[0,0]), math.sqrt(cov[1,1])
    int_z = intercept / int_se; int_p = 2*(1 - stats.norm.cdf(abs(int_z)))
    slope_z = slope / slope_se; slope_p = 2*(1 - stats.norm.cdf(abs(slope_z)))
    return dict(method="MR_Egger", b=slope, se=slope_se, pval=slope_p, z=slope_z,
                intercept=intercept, intercept_se=int_se, intercept_p=int_p,
                nsnp=len(bx))

def steiger_test(bx, se_bx, by, se_by, n_exposure, n_outcome, eaf, outcome_binary=False,
                 ncase=None, nctrl=None):
    """Steiger directionality test (Hemani 2017).
    Compares R^2 explained by SNP in exposure vs outcome. Exposure R2 should exceed outcome R2.
    """
    bx = np.asarray(bx, float); se_bx = np.asarray(se_bx, float)
    by = np.asarray(by, float); se_by = np.asarray(se_by, float)
    eaf = np.asarray(eaf, float)
    # R2 continuous-continuous approximation
    # For exposure (assumed continuous): R2 = 2*EAF*(1-EAF)*beta^2 (per SNP)
    var_gx = 2 * eaf * (1 - eaf)
    # For a quantitative exposure with scaled beta (SD units), R2 ≈ var_gx * beta^2
    r2_x = var_gx * bx**2
    # For binary outcome:
    if outcome_binary and ncase and nctrl:
        # Hemani 2017 Appx: convert logOR to r2 on liability scale
        # simplest: r2_y = var_gx * by^2 / (by^2 var_gx + pi^2/3)
        # (Lloyd-Jones 2018)
        prev = ncase / (ncase + nctrl)
        from scipy.stats import norm
        t = norm.ppf(1 - prev)
        z = norm.pdf(t)
        # logistic -> liability: multiplier ≈ z/(prev*(1-prev))
        liab_mult = z / max(prev*(1-prev), 1e-6)
        by_liab = by * liab_mult
        r2_y = var_gx * by_liab**2 / (var_gx * by_liab**2 + (math.pi**2)/3)
    else:
        r2_y = var_gx * by**2
    r2x_sum = np.nansum(r2_x); r2y_sum = np.nansum(r2_y)
    correct = r2x_sum > r2y_sum
    # Steiger p via Fisher Z test is complicated; return descriptive
    return dict(r2_exposure=float(r2x_sum), r2_outcome=float(r2y_sum),
                correct_direction=bool(correct))

# ------------------------------------------------------------------
# 3. Finngen parsing: extract rows matching target rsids
# ------------------------------------------------------------------
def parse_finngen_subset(gz_path: Path, target_rsids: set) -> pd.DataFrame:
    """Stream Finngen gz, keep rows whose rsids column contains any target.
    Finngen R12 columns: #chrom pos ref alt rsids nearest_genes pval mlogp beta sebeta af_alt [af_alt_cases af_alt_controls]
    """
    log.info(f"parsing {gz_path.name} ({gz_path.stat().st_size/1024**2:.1f} MB)")
    rows = []
    header = None
    n_lines = 0
    t0 = time.time()
    with gzip.open(gz_path, "rt") as f:
        header = f.readline().rstrip("\n").split("\t")
        col_idx = {c: i for i, c in enumerate(header)}
        rsid_col = col_idx["rsids"]
        for line in f:
            n_lines += 1
            # quick membership check before split
            # rsids may be "rs123" or "rs123,rs456"
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= rsid_col: continue
            rs_field = parts[rsid_col]
            if not rs_field.startswith("rs"): continue
            matched = None
            if "," in rs_field:
                for r in rs_field.split(","):
                    if r in target_rsids: matched = r; break
            else:
                if rs_field in target_rsids: matched = rs_field
            if matched is None: continue
            rows.append(parts + [matched])
            if n_lines % 2_000_000 == 0:
                log.info(f"  scanned {n_lines/1e6:.1f}M lines @ {n_lines/(time.time()-t0)/1e3:.0f}k/s, kept {len(rows)}")
    log.info(f"  done: scanned {n_lines:,} lines, kept {len(rows)}")
    cols = header + ["match_rsid"]
    df = pd.DataFrame(rows, columns=cols)
    # type conversions
    for c in ["pval","beta","sebeta","af_alt"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

# ------------------------------------------------------------------
# 4. Harmonisation
# ------------------------------------------------------------------
def harmonise(exp_df: pd.DataFrame, out_df: pd.DataFrame) -> pd.DataFrame:
    """Align effect alleles between exposure and outcome.
    Exposure columns: rsid, ea (effect allele), beta, se, pval, eaf
    Outcome  columns: match_rsid, ref, alt, beta, sebeta, pval, af_alt
      Finngen convention: beta is for 'alt' allele.
    Returns merged frame with:
      SNP, EA, OA, beta_x, se_x, beta_y, se_y, eaf_x, eaf_y, keep
    """
    m = exp_df.merge(out_df, left_on="rsid", right_on="match_rsid", how="inner",
                     suffixes=("_x", "_y"))
    if len(m) == 0: return m
    def align(row):
        ea_x = str(row["ea"]).upper()
        alt  = str(row["alt"]).upper()
        ref  = str(row["ref"]).upper()
        # Finngen outcome beta collides with exposure beta and gets suffix _y after merge
        by   = float(row.get("beta_y", row.get("beta", np.nan)))  # beta in outcome for alt
        se_y = float(row["sebeta"])
        eaf_y = float(row["af_alt"])
        eaf_x_val = row.get("eaf_x", row.get("eaf", np.nan))
        if ea_x == alt:
            sign = 1
        elif ea_x == ref:
            sign = -1
        else:
            return pd.Series(dict(beta_y=np.nan, se_y=np.nan, eaf_y=np.nan,
                                  OA=np.nan, keep=False, palindromic=False))
        # palindromic check (A/T or C/G): if EAF very close to 0.5, ambiguous -> drop
        pal = (ea_x, (alt if ea_x==alt else ref)) in [("A","T"),("T","A"),("C","G"),("G","C")]
        if pal and (not np.isnan(eaf_x_val)) and abs(eaf_x_val - 0.5) < 0.08:
            return pd.Series(dict(beta_y=np.nan, se_y=np.nan, eaf_y=np.nan,
                                  OA=(ref if sign==1 else alt),
                                  keep=False, palindromic=True))
        return pd.Series(dict(beta_y=sign * by, se_y=se_y, eaf_y=(eaf_y if sign==1 else 1-eaf_y),
                              OA=(ref if sign==1 else alt),
                              keep=True, palindromic=bool(pal)))
    aligned = m.apply(align, axis=1)
    # drop raw outcome columns that collide with aligned output
    drop_cols = [c for c in ["beta_y","se_y","eaf_y","sebeta","af_alt"] if c in m.columns]
    m_stripped = m.drop(columns=drop_cols)
    m2 = m_stripped.join(aligned)
    # rename exposure cols for clarity (each one independently; merge-suffix behaviour
    # depends on whether outcome also had that column name)
    rename_map = {}
    if "beta" in m2.columns and "beta_x" not in m2.columns: rename_map["beta"] = "beta_x"
    if "se"   in m2.columns and "se_x"   not in m2.columns: rename_map["se"]   = "se_x"
    if "eaf"  in m2.columns and "eaf_x"  not in m2.columns: rename_map["eaf"]  = "eaf_x"
    if rename_map:
        m2 = m2.rename(columns=rename_map)
    for c in ("beta_x", "se_x", "eaf_x"):
        if c not in m2.columns:
            m2[c] = np.nan
    return m2

# ------------------------------------------------------------------
# 5. Run chains
# ------------------------------------------------------------------
def main():
    log.info("=== Sweet Trap Layer D MR pilot (Python) ===")
    # Load all IV files
    iv_cache = {}
    for ch in CHAINS:
        if ch.iv_file in iv_cache: continue
        p = OUT / ch.iv_file
        if not p.exists():
            log.warning(f"IV file missing: {p}"); iv_cache[ch.iv_file] = None; continue
        df = pd.read_csv(p)
        df = df[df["beta"].notna() & df["se"].notna() & (df["se"] > 0) & df["pval"].notna()]
        df["ea"] = df["ea"].astype(str).str.upper()
        # F stat
        df["F"] = (df["beta"]/df["se"])**2
        iv_cache[ch.iv_file] = df
        log.info(f"IV {ch.iv_file}: n={len(df)} meanF={df['F'].mean():.1f}")

    # Group chains by outcome to parse each Finngen file once
    outcome_to_chains = {}
    for ch in CHAINS:
        outcome_to_chains.setdefault(ch.outcome_phenocode, []).append(ch)

    all_results = []
    all_harmonised = []

    for oc, chains_oc in outcome_to_chains.items():
        gz = FINDIR / f"finngen_R12_{oc}.gz"
        if not gz.exists():
            log.warning(f"Finngen file not yet downloaded: {gz}")
            for ch in chains_oc:
                all_results.append(dict(chain=ch.id, exposure=ch.exposure_label,
                                       outcome=ch.outcome_label, method="SKIPPED",
                                       note="outcome_file_missing"))
            continue
        # collect all target rsids across chains sharing this outcome
        all_rs = set()
        for ch in chains_oc:
            iv = iv_cache.get(ch.iv_file)
            if iv is None: continue
            all_rs |= set(iv["rsid"].tolist())
        log.info(f"\n=== OUTCOME {oc}: {len(chains_oc)} chain(s), {len(all_rs)} unique IV rsids ===")
        oc_df = parse_finngen_subset(gz, all_rs)
        if len(oc_df) == 0:
            log.warning(f"  no matching SNPs in {oc}"); continue

        for ch in chains_oc:
            iv = iv_cache.get(ch.iv_file)
            if iv is None:
                all_results.append(dict(chain=ch.id, exposure=ch.exposure_label,
                                       outcome=ch.outcome_label, method="SKIPPED",
                                       note="iv_missing")); continue
            har = harmonise(iv[["rsid","ea","beta","se","pval","eaf"]].copy(), oc_df.copy())
            if len(har) == 0:
                log.warning(f"  chain {ch.id}: 0 SNPs matched in outcome"); continue
            har_k = har[har["keep"]].dropna(subset=["beta_x","se_x","beta_y","se_y"])
            log.info(f"  chain {ch.id}: harmonised={len(har)} kept={len(har_k)} (dropped palindromic={har['palindromic'].sum()})")
            if len(har_k) < 3:
                log.warning(f"  chain {ch.id}: <3 SNPs, skip MR")
                for _, r in har_k.iterrows():
                    all_harmonised.append({**r.to_dict(), "chain": ch.id})
                continue
            bx = har_k["beta_x"].values; sx = har_k["se_x"].values
            by = har_k["beta_y"].values; sy = har_k["se_y"].values
            eafx = har_k["eaf_x"].values

            # IVW
            r_ivw = ivw_random(bx, by, sy)
            # Simple/weighted median
            r_med_s = simple_median(bx, by, sy, B=500)
            r_med_w = weighted_median_ratio(bx, by, sy, B=500)
            # MR-Egger
            r_egger = mr_egger(bx, by, sy)
            # Steiger
            n_x = int(iv.get("exposure_n", iv.get("n", [100000])).iloc[0]) if "exposure_n" in iv.columns else 100000
            steig = steiger_test(bx, sx, by, sy, n_x, ch.outcome_ncase+ch.outcome_nctrl, eafx,
                                 outcome_binary=True, ncase=ch.outcome_ncase, nctrl=ch.outcome_nctrl)
            meanF = float(((bx/sx)**2).mean())

            # Leave-one-out IVW
            loo_rows = []
            for i in range(len(bx)):
                mask = np.ones(len(bx), bool); mask[i] = False
                try:
                    r_loo = ivw_random(bx[mask], by[mask], sy[mask])
                    loo_rows.append(dict(chain=ch.id, dropped_snp=har_k.iloc[i]["rsid"],
                                        b=r_loo["b"], se=r_loo["se"], pval=r_loo["pval"]))
                except Exception:
                    pass
            pd.DataFrame(loo_rows).to_csv(OUT / f"mr_loo_chain{ch.id}.csv", index=False)

            def entry(d):
                b = d.get("b"); se = d.get("se")
                or_ = math.exp(b) if b is not None and not np.isnan(b) else np.nan
                or_lo = math.exp(b - 1.96*se) if b is not None and se is not None and not np.isnan(b) and not np.isnan(se) else np.nan
                or_hi = math.exp(b + 1.96*se) if b is not None and se is not None and not np.isnan(b) and not np.isnan(se) else np.nan
                return dict(
                    chain=ch.id, exposure=ch.exposure_label, outcome=ch.outcome_label,
                    method=d.get("method"), nsnp=d.get("nsnp"),
                    beta=b, se=se, pval=d.get("pval"),
                    or_=or_, or_lo=or_lo, or_hi=or_hi,
                    Q=d.get("Q"), Q_p=d.get("Q_pval"), I2=d.get("I2"),
                    egger_intercept=d.get("intercept"),
                    egger_intercept_se=d.get("intercept_se"),
                    egger_intercept_p=d.get("intercept_p"),
                    meanF=meanF,
                    r2_exp=steig["r2_exposure"], r2_out=steig["r2_outcome"],
                    steiger_dir=steig["correct_direction"],
                )
            all_results += [entry(r_ivw), entry(r_med_s), entry(r_med_w), entry(r_egger)]

            # summary line
            b, se, p = r_ivw["b"], r_ivw["se"], r_ivw["pval"]
            log.info(f"    [IVW]  b={b:.4f} se={se:.4f} OR={math.exp(b):.3f} 95%CI=({math.exp(b-1.96*se):.3f}–{math.exp(b+1.96*se):.3f}) p={p:.3g}  nIV={r_ivw['nsnp']} meanF={meanF:.0f}")
            log.info(f"    [WMed] b={r_med_w['b']:.4f} se={r_med_w['se']:.4f} p={r_med_w['pval']:.3g}")
            log.info(f"    [Egger] b={r_egger['b']:.4f} intercept={r_egger['intercept']:.4f} (p_int={r_egger['intercept_p']:.3g})")
            log.info(f"    [Q]    Q={r_ivw['Q']:.2f} df={r_ivw['Q_df']} p={r_ivw['Q_pval']:.3g} I2={r_ivw['I2']:.2f}")
            log.info(f"    [Steiger] r2_exp={steig['r2_exposure']:.4f} r2_out={steig['r2_outcome']:.4f} correct={steig['correct_direction']}")

            # harmonised rows
            h2 = har_k.copy(); h2["chain"] = ch.id
            all_harmonised.append(h2)

    # ------------------------------------------------------------------
    # 6. Save
    # ------------------------------------------------------------------
    res_df = pd.DataFrame(all_results)
    res_df.to_csv(OUT / "mr_results_all_chains.csv", index=False)
    log.info(f"wrote mr_results_all_chains.csv rows={len(res_df)}")

    if all_harmonised and any(isinstance(x, pd.DataFrame) for x in all_harmonised):
        hdf = pd.concat([x for x in all_harmonised if isinstance(x, pd.DataFrame)], ignore_index=True)
        hdf.to_csv(OUT / "mr_harmonised_data.csv", index=False)
        try:
            hdf.to_parquet(OUT / "mr_harmonised_data.parquet")
            log.info("wrote mr_harmonised_data.parquet")
        except Exception as e:
            log.warning(f"parquet write failed: {e}")
    log.info("=== DONE ===")

if __name__ == "__main__":
    main()
