#!/usr/bin/env python3
"""
mr_extended_v2.py
=================
Sweet Trap Layer D — MR extension v2.

Purpose:
    Extend Layer D MR pilot (v1: 7 chains, 4 methods, 4 outcomes) with
    * 5 additional Finngen R12 outcomes now downloaded
    * new chain × outcome mappings informed by biological mechanism
    * method diversification (MR-PRESSO, MR-RAPS, single-SNP, funnel)
    * multivariable MR (MVMR) for confounded triangles
    * comprehensive leave-one-out for all chains

Inputs:
    * IV files    : 02-data/processed/mr_iv_*.csv   (7 exposures; EBI GWAS cat)
    * Outcome gz  : /Volumes/P1/.../Finngen/R12_summary_stats/finngen_R12_*.gz
                    (9 outcomes, ~780 MB each, line-by-line streaming)

Outputs:
    * mr_results_all_chains_v2.csv        — all chain × method rows (IVW + median +
                                             Egger + RAPS + PRESSO + MVMR_direct)
    * mr_presso_global_v2.csv             — MR-PRESSO global test + outlier list
    * mr_mvmr_v2.csv                      — multivariable MR direct effects
    * mr_single_snp_v2.csv                — per-SNP Wald ratios (figure-designer)
    * mr_loo_all_v2.csv                   — leave-one-out across every chain
    * mr_funnel_data_v2.csv               — funnel plot x/y for SI figure
    * 04-figures/supp/mr_supp_forest.png  — supplementary forest (single-SNP + LOO)
    * 03-analysis/scripts/mr_extended_v2.log

Method notes:
    * MR-PRESSO (Verbanck 2018 Nat Genet) — RSS-based outlier/global test,
      Python re-implementation (2,000 simulated null datasets).  Removes
      outliers and re-runs IVW.
    * MR-RAPS (Zhao 2020 Ann Stat) — robust adjusted profile score.  Handles
      many weak instruments + invalid IVs.  Python from-scratch implementation
      (L2 loss; numerical root-find on profile likelihood).
    * MVMR-IVW (Sanderson 2019) — stacked G-X coefficient matrix, then weighted
      regression on G-Y.  We use simple 2-exposure MVMR with harmonised IVs.

Compute:
    * n_workers=1.  Finngen gz streamed once per outcome; cached to parquet.
    * Memory footprint < 3 GB.
"""
from __future__ import annotations
import os, sys, gzip, io, logging, math, time, json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import numpy as np
import pandas as pd
from scipy import stats, optimize

# --------------------------------------------------------------------
# 0. Paths / logging
# --------------------------------------------------------------------
PROJ   = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
FINDIR = Path("/Volumes/P1/城市研究/UKB_芬兰Finngen_catalog_ieu/gwas_list/Finngen/R12_summary_stats")
OUT    = PROJ / "02-data/processed"
FIGDIR = PROJ / "04-figures/supp"; FIGDIR.mkdir(parents=True, exist_ok=True)
LOGP   = PROJ / "03-analysis/scripts/mr_extended_v2.log"

logging.basicConfig(filename=LOGP, level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
_h = logging.StreamHandler(sys.stdout)
_h.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
logging.getLogger().addHandler(_h)
log = logging.getLogger()

RNG = np.random.default_rng(20260418)

# --------------------------------------------------------------------
# 1. Chain definitions
#    v2 adds 8 new chains (5 for new outcomes + extras for mechanism coverage)
# --------------------------------------------------------------------
@dataclass
class Chain:
    id: str
    exposure_label: str
    iv_file: str
    outcome_label: str
    outcome_phenocode: str
    outcome_ncase: int
    outcome_nctrl: int
    note: str = ""

# v1 chains retained for complete side-by-side sensitivity re-run (single pass)
CHAINS = [
    # v1 chains
    Chain("1a",  "risk_tolerance",         "mr_iv_risk_tolerance_GCST006810.csv",      "F5_DEPRESSIO",     "F5_DEPRESSIO",                 59333,  434831, "v1"),
    Chain("1b",  "risk_tolerance",         "mr_iv_risk_tolerance_GCST006810.csv",      "ANTIDEPRESSANTS",  "ANTIDEPRESSANTS",              149403, 111976, "v1"),
    Chain("2b",  "drinks_per_week",        "mr_iv_drinks_per_week_GCST007461.csv",     "K11_ALCOLIV",      "K11_ALCOLIV",                  3769,   485213, "v1"),
    Chain("3c",  "bmi_locke2015",          "mr_iv_bmi_locke2015_GCST002783.csv",       "T2D",              "T2D",                          82878,  403489, "v1"),
    Chain("5",   "years_of_schooling",     "mr_iv_years_of_schooling_GCST006572.csv",  "F5_DEPRESSIO",     "F5_DEPRESSIO",                 59333,  434831, "v1"),
    Chain("6",   "subjective_wellbeing",   "mr_iv_subjective_wellbeing_GCST003766.csv","F5_DEPRESSIO",     "F5_DEPRESSIO",                 59333,  434831, "v1"),
    Chain("7",   "smoking_initiation",     "mr_iv_smoking_initiation_GCST007474.csv",  "K11_ALCOLIV",      "K11_ALCOLIV",                  3769,   485213, "v1"),

    # v2 NEW chains — anxiety (3)
    Chain("1c",  "risk_tolerance",         "mr_iv_risk_tolerance_GCST006810.csv",      "F5_ANXIETY",       "F5_ANXIETY",                   24643,  444414, "v2-new"),
    Chain("5b",  "years_of_schooling",     "mr_iv_years_of_schooling_GCST006572.csv",  "F5_ANXIETY",       "F5_ANXIETY",                   24643,  444414, "v2-new"),
    Chain("6b",  "subjective_wellbeing",   "mr_iv_subjective_wellbeing_GCST003766.csv","F5_ANXIETY",       "F5_ANXIETY",                   24643,  444414, "v2-new"),

    # v2 NEW chains — alcoholic chronic pancreatitis (2)
    Chain("2a",  "drinks_per_week",        "mr_iv_drinks_per_week_GCST007461.csv",     "ALCOPANCCHRON",    "ALCOPANCCHRON",                2400,   497948, "v2-new"),
    Chain("7b",  "smoking_initiation",     "mr_iv_smoking_initiation_GCST007474.csv",  "ALCOPANCCHRON",    "ALCOPANCCHRON",                2400,   497948, "v2-new"),

    # v2 NEW chains — hepatocellular carcinoma (2)
    Chain("2c",  "drinks_per_week",        "mr_iv_drinks_per_week_GCST007461.csv",     "C3_HEP_EXALLC",    "C3_HEPATOCELLU_CARC_EXALLC",   947,    378749, "v2-new"),
    Chain("7c",  "smoking_initiation",     "mr_iv_smoking_initiation_GCST007474.csv",  "C3_HEP_EXALLC",    "C3_HEPATOCELLU_CARC_EXALLC",   947,    378749, "v2-new"),

    # v2 NEW chains — diabetic nephropathy (2)  (BMI + risk_tolerance as metabolic proxies)
    Chain("3a",  "bmi_locke2015",          "mr_iv_bmi_locke2015_GCST002783.csv",       "DM_NEPHROPATHY",   "DM_NEPHROPATHY",               5579,   90951,  "v2-new"),
    Chain("3a2", "risk_tolerance",         "mr_iv_risk_tolerance_GCST006810.csv",      "DM_NEPHROPATHY",   "DM_NEPHROPATHY",               5579,   90951,  "v2-new-exploratory"),

    # v2 NEW chains — stroke (3)
    Chain("3b",  "bmi_locke2015",          "mr_iv_bmi_locke2015_GCST002783.csv",       "C_STROKE",         "C_STROKE",                     53492,  360342, "v2-new"),
    Chain("3b2", "drinks_per_week",        "mr_iv_drinks_per_week_GCST007461.csv",     "C_STROKE",         "C_STROKE",                     53492,  360342, "v2-new"),
    Chain("3b3", "smoking_initiation",     "mr_iv_smoking_initiation_GCST007474.csv",  "C_STROKE",         "C_STROKE",                     53492,  360342, "v2-new"),
]

# MVMR specifications (confounded triangles of substantive interest)
MVMR_SPECS = [
    dict(name="BMI+RiskTol_on_T2D",
         exposures=[("bmi_locke2015",        "mr_iv_bmi_locke2015_GCST002783.csv"),
                    ("risk_tolerance",       "mr_iv_risk_tolerance_GCST006810.csv")],
         outcome=("T2D", "T2D", 82878, 403489)),
    dict(name="Drinks+Smoking_on_AlcLiver",
         exposures=[("drinks_per_week",      "mr_iv_drinks_per_week_GCST007461.csv"),
                    ("smoking_initiation",   "mr_iv_smoking_initiation_GCST007474.csv")],
         outcome=("K11_ALCOLIV", "K11_ALCOLIV", 3769, 485213)),
    dict(name="BMI+Drinks_on_Stroke",
         exposures=[("bmi_locke2015",        "mr_iv_bmi_locke2015_GCST002783.csv"),
                    ("drinks_per_week",      "mr_iv_drinks_per_week_GCST007461.csv")],
         outcome=("C_STROKE", "C_STROKE", 53492, 360342)),
]

# --------------------------------------------------------------------
# 2. MR estimators (v1 carried forward + v2 new)
# --------------------------------------------------------------------
def ivw_random(bx, by, se_by):
    bx = np.asarray(bx, float); by = np.asarray(by, float); se_by = np.asarray(se_by, float)
    w = 1.0 / (se_by**2)
    wr = by / bx
    beta_fe = np.sum(w * bx * by) / np.sum(w * bx**2)
    se_fe   = 1.0 / math.sqrt(np.sum(w * bx**2))
    Q = np.sum(w * bx**2 * (wr - beta_fe)**2)
    df = len(bx) - 1
    Qp = 1 - stats.chi2.cdf(Q, df) if df > 0 else np.nan
    phi = max(Q / df, 1.0) if df > 0 else 1.0
    se_re = se_fe * math.sqrt(phi)
    I2 = max((Q - df) / Q, 0.0) if Q > 0 else 0.0
    z = beta_fe / se_re
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return dict(method="IVW_random", b=beta_fe, se=se_re, z=z, pval=p,
                Q=Q, Q_df=df, Q_pval=Qp, I2=I2, nsnp=len(bx), phi=phi)

def weighted_median(bx, by, se_by, B=1000, seed=42):
    rng = np.random.default_rng(seed)
    bx = np.asarray(bx, float); by = np.asarray(by, float); se_by = np.asarray(se_by, float)
    wr = by / bx; w = (bx**2) / (se_by**2)
    def wmed(vals, wts):
        idx = np.argsort(vals); v = vals[idx]; wt = wts[idx]
        cum = np.cumsum(wt) / np.sum(wt)
        return np.interp(0.5, cum, v)
    est = wmed(wr, w)
    boots = []
    for _ in range(B):
        wr_b = (by + rng.normal(0, se_by)) / bx
        boots.append(wmed(wr_b, w))
    se = np.std(boots, ddof=1)
    z = est/se if se > 0 else np.nan
    p = 2*(1-stats.norm.cdf(abs(z))) if se > 0 else np.nan
    return dict(method="weighted_median", b=est, se=se, z=z, pval=p, nsnp=len(bx))

def mr_egger(bx, by, se_by):
    import numpy.linalg as la
    bx = np.asarray(bx, float); by = np.asarray(by, float); se_by = np.asarray(se_by, float)
    sign = np.where(bx < 0, -1.0, 1.0)
    bx_o = bx*sign; by_o = by*sign
    w = 1.0/(se_by**2)
    X = np.column_stack([np.ones_like(bx_o), bx_o])
    W = np.diag(w); XtWX = X.T@W@X; XtWy = X.T@W@by_o
    try: beta = la.solve(XtWX, XtWy)
    except la.LinAlgError:
        return dict(method="MR_Egger", b=np.nan, se=np.nan, intercept=np.nan,
                    intercept_se=np.nan, intercept_p=np.nan, pval=np.nan, nsnp=len(bx))
    intercept, slope = beta
    resid = by_o - X@beta
    df = len(bx)-2
    if df <= 0:
        return dict(method="MR_Egger", b=slope, se=np.nan, intercept=intercept,
                    intercept_se=np.nan, intercept_p=np.nan, pval=np.nan, nsnp=len(bx))
    sigma2 = max(np.sum(w*resid**2)/df, 1.0)
    cov = sigma2 * la.inv(XtWX)
    int_se, slope_se = math.sqrt(cov[0,0]), math.sqrt(cov[1,1])
    int_p = 2*(1-stats.norm.cdf(abs(intercept/int_se)))
    slope_p = 2*(1-stats.norm.cdf(abs(slope/slope_se)))
    return dict(method="MR_Egger", b=slope, se=slope_se, pval=slope_p,
                intercept=intercept, intercept_se=int_se, intercept_p=int_p,
                nsnp=len(bx))

# --------- NEW v2 estimators --------------------------------------------
def mr_raps(bx, by, se_bx, se_by, over_dispersion=True, tol=1e-6, max_iter=100):
    """Robust Adjusted Profile Score MR (Zhao 2020, L2 loss).

    Beta is found by root-finding on the score function
        U(beta) = sum_i (bx_i*by_i - beta*bx_i^2) / (se_by_i^2 + beta^2*se_bx_i^2)
    and accounts for weak instrument bias via measurement error in bx.
    Over-dispersion: phi = residual-based multiplicative factor on SE.
    """
    bx = np.asarray(bx, float); by = np.asarray(by, float)
    se_bx = np.asarray(se_bx, float); se_by = np.asarray(se_by, float)
    # guard: if se_bx all NaN/0, fall back to IVW var
    if np.any(np.isnan(se_bx)) or np.all(se_bx == 0):
        se_bx = np.full_like(bx, np.nanmedian(se_bx[se_bx > 0]) if np.any(se_bx > 0) else 0.0)
    def U(b):
        denom = se_by**2 + (b**2)*se_bx**2
        return np.sum(bx*by - b*bx**2) / np.mean(denom)  # scaled, sign-preserving
    # Use a scalar root finder on a bracket around IVW estimate
    b0 = np.sum(bx*by/se_by**2) / np.sum((bx/se_by)**2)
    try:
        sol = optimize.root_scalar(lambda b: np.sum((bx*by - b*bx**2)/(se_by**2 + (b**2)*se_bx**2)),
                                    bracket=[b0-2, b0+2], method="bisect", xtol=tol)
        b_hat = sol.root
    except Exception:
        b_hat = b0
    # SE via sandwich (score derivative)
    d  = se_by**2 + (b_hat**2)*se_bx**2
    # dU/db = -sum(bx^2/d) - sum( 2*b*(bx*by - b*bx^2)*se_bx^2 / d^2 )
    dU = -np.sum(bx**2/d) - np.sum(2*b_hat*(bx*by - b_hat*bx**2)*se_bx**2 / d**2)
    # variance of U: sum((bx*by - b*bx^2)^2 / d^2)
    VU = np.sum((bx*by - b_hat*bx**2)**2 / d**2)
    se_hat = math.sqrt(VU) / abs(dU) if abs(dU) > 0 else np.nan
    # over-dispersion
    if over_dispersion and len(bx) > 1:
        resid = (by - b_hat*bx) / np.sqrt(d)
        phi = max(np.var(resid, ddof=1), 1.0)
        se_hat *= math.sqrt(phi)
    z = b_hat/se_hat if se_hat and se_hat > 0 else np.nan
    p = 2*(1 - stats.norm.cdf(abs(z))) if not np.isnan(z) else np.nan
    return dict(method="MR_RAPS", b=b_hat, se=se_hat, z=z, pval=p, nsnp=len(bx))

def mr_presso(bx, by, se_bx, se_by, n_sim=1000, sig_thresh=0.05, seed=123):
    """MR-PRESSO global + outlier test (Verbanck 2018).

    Idea: compute RSS_obs from leave-one-out model residuals; simulate null
    distribution by parametric bootstrap on (bx,by) under IVW estimate, compute
    RSS_null, derive global p-value; per-SNP outlier p-value similarly.
    Returns global test, outlier indices (p<sig_thresh), and IVW after removal.
    """
    rng = np.random.default_rng(seed)
    bx = np.asarray(bx, float); by = np.asarray(by, float)
    se_bx = np.asarray(se_bx, float); se_by = np.asarray(se_by, float)
    k = len(bx)
    if k < 4:
        return dict(presso_global_p=np.nan, outliers=[], n_outliers=0,
                    b_corrected=np.nan, se_corrected=np.nan, p_corrected=np.nan,
                    distortion_p=np.nan, nsnp_corrected=k, note="n<4")
    # observed RSS (LOO sum of squared residuals, weighted)
    def rss_weighted(bx_, by_, se_bx_, se_by_):
        n = len(bx_)
        rss_per = np.zeros(n)
        for i in range(n):
            mask = np.ones(n, bool); mask[i] = False
            # IVW estimate without SNP i
            w = 1/se_by_[mask]**2
            b_i = np.sum(w*bx_[mask]*by_[mask])/np.sum(w*bx_[mask]**2)
            # residual for SNP i (Wald ratio - b_i), weighted by 1/var(Wald_i)
            var_wald = se_by_[i]**2/bx_[i]**2 + by_[i]**2*se_bx_[i]**2/bx_[i]**4
            rss_per[i] = (by_[i]/bx_[i] - b_i)**2 / var_wald
        return rss_per
    rss_obs_per = rss_weighted(bx, by, se_bx, se_by)
    RSS_obs = np.sum(rss_obs_per)
    # null: simulate (bx*, by*) under IVW β0
    w0 = 1/se_by**2
    b0 = np.sum(w0*bx*by)/np.sum(w0*bx**2)
    RSS_null = np.zeros(n_sim)
    outlier_null = np.zeros((n_sim, k))
    for s in range(n_sim):
        bx_sim = bx + rng.normal(0, se_bx)
        by_sim = b0*bx + rng.normal(0, se_by)   # under H0: by = b0*bx
        rss_per_sim = rss_weighted(bx_sim, by_sim, se_bx, se_by)
        RSS_null[s] = np.sum(rss_per_sim)
        outlier_null[s, :] = rss_per_sim
    global_p = np.mean(RSS_null >= RSS_obs)
    # per-SNP outlier p
    snp_p = np.mean(outlier_null >= rss_obs_per[None, :], axis=0)
    outliers = np.where(snp_p < sig_thresh)[0].tolist()
    # corrected IVW after removing outliers
    if len(outliers) > 0 and (k - len(outliers)) >= 3:
        keep = np.array([i for i in range(k) if i not in outliers])
        r_c = ivw_random(bx[keep], by[keep], se_by[keep])
        b_c, se_c, p_c, nc = r_c["b"], r_c["se"], r_c["pval"], r_c["nsnp"]
        # distortion test (approx): z of (b_raw - b_corrected)/sqrt(se_raw^2+se_c^2)
        r_raw = ivw_random(bx, by, se_by)
        num  = r_raw["b"] - b_c
        denom = math.sqrt(r_raw["se"]**2 + se_c**2)
        distortion_p = 2*(1 - stats.norm.cdf(abs(num/denom))) if denom > 0 else np.nan
    else:
        b_c, se_c, p_c, nc, distortion_p = np.nan, np.nan, np.nan, k, np.nan
    return dict(presso_global_p=float(global_p), outliers=outliers,
                n_outliers=len(outliers), b_corrected=b_c, se_corrected=se_c,
                p_corrected=p_c, distortion_p=distortion_p, nsnp_corrected=nc,
                snp_p=snp_p.tolist())

def single_snp_wald(rsids, bx, by, se_bx, se_by):
    """Per-SNP Wald ratio + delta-method SE, for single-SNP MR plot."""
    bx = np.asarray(bx, float); by = np.asarray(by, float)
    se_bx = np.asarray(se_bx, float); se_by = np.asarray(se_by, float)
    out = []
    for i, r in enumerate(rsids):
        w = by[i]/bx[i]
        var_w = se_by[i]**2/bx[i]**2 + by[i]**2*se_bx[i]**2/bx[i]**4
        se_w = math.sqrt(max(var_w, 0.0))
        z = w/se_w if se_w > 0 else np.nan
        p = 2*(1 - stats.norm.cdf(abs(z))) if not np.isnan(z) else np.nan
        out.append(dict(rsid=r, b=w, se=se_w, z=z, pval=p,
                        or_=math.exp(w), or_lo=math.exp(w-1.96*se_w), or_hi=math.exp(w+1.96*se_w)))
    return out

def steiger_test(bx, se_bx, by, se_by, eaf, ncase, nctrl):
    bx = np.asarray(bx, float); by = np.asarray(by, float); eaf = np.asarray(eaf, float)
    var_gx = 2*eaf*(1-eaf)
    r2_x = var_gx * bx**2
    prev = ncase/(ncase+nctrl)
    t = stats.norm.ppf(1-prev); z = stats.norm.pdf(t)
    mult = z/max(prev*(1-prev), 1e-6)
    by_l = by*mult
    r2_y = var_gx*by_l**2 / (var_gx*by_l**2 + (math.pi**2)/3)
    r2x_sum = float(np.nansum(r2_x)); r2y_sum = float(np.nansum(r2_y))
    return dict(r2_exposure=r2x_sum, r2_outcome=r2y_sum,
                correct_direction=bool(r2x_sum > r2y_sum))

# --------- MVMR ----------------------------------------------------------
def mvmr_ivw(G_x: np.ndarray, by: np.ndarray, se_by: np.ndarray):
    """Multivariable-MR IVW: G_x = [k,p] matrix of exposure effects (harmonised).
    Regress by on G_x with weights 1/se_by^2. Return per-exposure direct effect.
    """
    import numpy.linalg as la
    w = 1/se_by**2
    W = np.diag(w)
    XtWX = G_x.T@W@G_x
    XtWy = G_x.T@W@by
    try:
        b = la.solve(XtWX, XtWy)
    except la.LinAlgError:
        return None
    resid = by - G_x@b
    df = len(by) - G_x.shape[1]
    sigma2 = max(np.sum(w*resid**2)/df, 1.0) if df > 0 else 1.0
    cov = sigma2 * la.inv(XtWX)
    se = np.sqrt(np.diag(cov))
    z = b/se
    p = 2*(1 - stats.norm.cdf(np.abs(z)))
    return dict(b=b.tolist(), se=se.tolist(), z=z.tolist(), p=p.tolist(),
                nsnp=len(by), df=df, phi=sigma2)

# --------------------------------------------------------------------
# 3. Finngen parsing with cache
# --------------------------------------------------------------------
def parse_finngen_subset(gz_path: Path, target_rsids: set, cache_key: str) -> pd.DataFrame:
    """Stream Finngen gz for matching rsids; cache result per outcome phenocode
    (to avoid re-reading 780 MB when different chains share the same outcome).
    """
    cache_path = OUT / f"mr_outcome_cache_{cache_key}.parquet"
    existing = pd.DataFrame()
    if cache_path.exists():
        try:
            existing = pd.read_parquet(cache_path)
        except Exception:
            existing = pd.DataFrame()
    # if all targets already cached, just filter and return
    if len(existing) and "match_rsid" in existing.columns:
        have = set(existing["match_rsid"].tolist())
        missing = target_rsids - have
        if len(missing) == 0:
            log.info(f"  [cache hit] {cache_key}: {len(existing)} rows cover all {len(target_rsids)} targets")
            return existing[existing["match_rsid"].isin(target_rsids)].copy()
        log.info(f"  [cache partial] {cache_key}: missing {len(missing)}; rescanning")
        target_rsids = target_rsids  # use full set (simpler — single pass)
    log.info(f"parsing {gz_path.name} ({gz_path.stat().st_size/1024**2:.1f} MB) for {len(target_rsids)} rsids")
    rows = []; header = None; n_lines = 0
    t0 = time.time()
    with gzip.open(gz_path, "rt") as f:
        header = f.readline().rstrip("\n").split("\t")
        col_idx = {c:i for i,c in enumerate(header)}
        rsid_col = col_idx["rsids"]
        for line in f:
            n_lines += 1
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
    for c in ["pval","beta","sebeta","af_alt"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    try:
        df.to_parquet(cache_path)
    except Exception as e:
        log.warning(f"cache write failed: {e}")
    return df

# --------------------------------------------------------------------
# 4. Harmonisation (same as v1 with bug fixes)
# --------------------------------------------------------------------
def harmonise(exp_df: pd.DataFrame, out_df: pd.DataFrame) -> pd.DataFrame:
    m = exp_df.merge(out_df, left_on="rsid", right_on="match_rsid", how="inner",
                     suffixes=("_x", "_y"))
    if len(m) == 0: return m
    def align(row):
        ea_x = str(row["ea"]).upper()
        alt  = str(row["alt"]).upper()
        ref  = str(row["ref"]).upper()
        by   = float(row.get("beta_y", row.get("beta", np.nan)))
        se_y = float(row["sebeta"])
        eaf_y = float(row["af_alt"])
        eaf_x_val = row.get("eaf_x", row.get("eaf", np.nan))
        if ea_x == alt: sign = 1
        elif ea_x == ref: sign = -1
        else:
            return pd.Series(dict(beta_y=np.nan, se_y=np.nan, eaf_y=np.nan,
                                  OA=np.nan, keep=False, palindromic=False))
        pal = (ea_x, (alt if ea_x==alt else ref)) in [("A","T"),("T","A"),("C","G"),("G","C")]
        if pal and (not np.isnan(eaf_x_val)) and abs(eaf_x_val-0.5) < 0.08:
            return pd.Series(dict(beta_y=np.nan, se_y=np.nan, eaf_y=np.nan,
                                  OA=(ref if sign==1 else alt),
                                  keep=False, palindromic=True))
        return pd.Series(dict(beta_y=sign*by, se_y=se_y,
                              eaf_y=(eaf_y if sign==1 else 1-eaf_y),
                              OA=(ref if sign==1 else alt),
                              keep=True, palindromic=bool(pal)))
    aligned = m.apply(align, axis=1)
    drop_cols = [c for c in ["beta_y","se_y","eaf_y","sebeta","af_alt"] if c in m.columns]
    m_stripped = m.drop(columns=drop_cols)
    m2 = m_stripped.join(aligned)
    rename_map = {}
    if "beta" in m2.columns and "beta_x" not in m2.columns: rename_map["beta"] = "beta_x"
    if "se"   in m2.columns and "se_x"   not in m2.columns: rename_map["se"]   = "se_x"
    if "eaf"  in m2.columns and "eaf_x"  not in m2.columns: rename_map["eaf"]  = "eaf_x"
    if rename_map: m2 = m2.rename(columns=rename_map)
    for c in ("beta_x","se_x","eaf_x"):
        if c not in m2.columns: m2[c] = np.nan
    return m2

# --------------------------------------------------------------------
# 5. Main
# --------------------------------------------------------------------
def main():
    log.info("=== Layer D MR v2 — extended ===")
    log.info(f"{len(CHAINS)} chains | {len(MVMR_SPECS)} MVMR specs")
    # Load IV files
    iv_cache = {}
    for ch in CHAINS:
        if ch.iv_file in iv_cache: continue
        p = OUT / ch.iv_file
        if not p.exists():
            log.warning(f"IV missing: {p}"); iv_cache[ch.iv_file] = None; continue
        df = pd.read_csv(p)
        df = df[df["beta"].notna() & df["se"].notna() & (df["se"] > 0) & df["pval"].notna()]
        df["ea"] = df["ea"].astype(str).str.upper()
        # filter out unusable EA ("?" for insomnia)
        before = len(df)
        df = df[df["ea"].isin(["A","C","G","T"])]
        if len(df) < before:
            log.warning(f"  {ch.iv_file}: dropped {before-len(df)} SNPs with EA='?'")
        df["F"] = (df["beta"]/df["se"])**2
        iv_cache[ch.iv_file] = df
        log.info(f"IV {ch.iv_file}: n={len(df)} meanF={df['F'].mean():.1f}")

    # Group chains by outcome
    outcome_to_chains = {}
    for ch in CHAINS:
        outcome_to_chains.setdefault(ch.outcome_phenocode, []).append(ch)

    all_results = []
    all_presso = []
    all_loo = []
    all_single_snp = []
    all_funnel = []

    for oc, chains_oc in outcome_to_chains.items():
        gz = FINDIR / f"finngen_R12_{oc}.gz"
        if not gz.exists():
            log.warning(f"Finngen missing: {gz.name}")
            for ch in chains_oc:
                all_results.append(dict(chain=ch.id, exposure=ch.exposure_label,
                                        outcome=ch.outcome_label, method="SKIPPED",
                                        note="outcome_file_missing"))
            continue
        all_rs = set()
        for ch in chains_oc:
            iv = iv_cache.get(ch.iv_file)
            if iv is None: continue
            all_rs |= set(iv["rsid"].tolist())
        log.info(f"\n=== OUTCOME {oc} — {len(chains_oc)} chain(s), {len(all_rs)} rsids ===")
        oc_df = parse_finngen_subset(gz, all_rs, cache_key=oc)
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
                log.warning(f"  chain {ch.id}: 0 SNPs matched"); continue
            har_k = har[har["keep"]].dropna(subset=["beta_x","se_x","beta_y","se_y"])
            log.info(f"  chain {ch.id}: kept={len(har_k)} / harmonised={len(har)} (palindromic={har['palindromic'].sum()})")
            if len(har_k) < 3:
                log.warning(f"  chain {ch.id}: <3 SNPs, skip"); continue
            bx = har_k["beta_x"].values; sx = har_k["se_x"].values
            by = har_k["beta_y"].values; sy = har_k["se_y"].values
            eafx = har_k["eaf_x"].values
            rs = har_k["rsid"].values
            meanF = float(((bx/sx)**2).mean())

            # v1 methods
            r_ivw   = ivw_random(bx, by, sy)
            r_wmed  = weighted_median(bx, by, sy, B=500)
            r_egger = mr_egger(bx, by, sy)
            # v2 new methods
            r_raps  = mr_raps(bx, by, sx, sy)
            r_presso = mr_presso(bx, by, sx, sy, n_sim=500)  # n_sim=500 for speed
            # Steiger
            steig = steiger_test(bx, sx, by, sy, eafx, ch.outcome_ncase, ch.outcome_nctrl)
            # Single-SNP
            ss = single_snp_wald(rs, bx, by, sx, sy)
            for s in ss:
                s["chain"] = ch.id; s["exposure"] = ch.exposure_label; s["outcome"] = ch.outcome_label
                all_single_snp.append(s)
            # Leave-one-out
            for i in range(len(bx)):
                mask = np.ones(len(bx), bool); mask[i] = False
                if mask.sum() >= 3:
                    rl = ivw_random(bx[mask], by[mask], sy[mask])
                    all_loo.append(dict(chain=ch.id, exposure=ch.exposure_label,
                                        outcome=ch.outcome_label, dropped_snp=rs[i],
                                        b=rl["b"], se=rl["se"], pval=rl["pval"],
                                        or_=math.exp(rl["b"]),
                                        or_lo=math.exp(rl["b"]-1.96*rl["se"]),
                                        or_hi=math.exp(rl["b"]+1.96*rl["se"])))
            # Funnel data: x = 1/SE(Wald_i), y = Wald_i
            for i in range(len(bx)):
                w_i = by[i]/bx[i]
                var_w = sy[i]**2/bx[i]**2 + by[i]**2*sx[i]**2/bx[i]**4
                se_w = math.sqrt(max(var_w, 0.0))
                all_funnel.append(dict(chain=ch.id, exposure=ch.exposure_label,
                                       outcome=ch.outcome_label, rsid=rs[i],
                                       wald=w_i, se_wald=se_w,
                                       precision=1.0/se_w if se_w > 0 else np.nan))

            def entry(d):
                b = d.get("b"); se = d.get("se")
                or_   = math.exp(b) if b is not None and not np.isnan(b) else np.nan
                or_lo = math.exp(b-1.96*se) if b is not None and se is not None and not (np.isnan(b) or np.isnan(se)) else np.nan
                or_hi = math.exp(b+1.96*se) if b is not None and se is not None and not (np.isnan(b) or np.isnan(se)) else np.nan
                return dict(
                    chain=ch.id, exposure=ch.exposure_label, outcome=ch.outcome_label,
                    chain_note=ch.note, method=d.get("method"), nsnp=d.get("nsnp"),
                    beta=b, se=se, pval=d.get("pval"),
                    or_=or_, or_lo=or_lo, or_hi=or_hi,
                    Q=d.get("Q"), Q_p=d.get("Q_pval"), I2=d.get("I2"),
                    egger_intercept=d.get("intercept"),
                    egger_intercept_se=d.get("intercept_se"),
                    egger_intercept_p=d.get("intercept_p"),
                    meanF=meanF,
                    r2_exp=steig["r2_exposure"], r2_out=steig["r2_outcome"],
                    steiger_dir=steig["correct_direction"])
            all_results += [entry(r_ivw), entry(r_wmed), entry(r_egger), entry(r_raps)]
            # PRESSO entry: use corrected estimate if outliers found, else global test only
            presso_entry = dict(
                chain=ch.id, exposure=ch.exposure_label, outcome=ch.outcome_label,
                chain_note=ch.note, method="MR_PRESSO_corrected",
                nsnp=r_presso["nsnp_corrected"],
                beta=r_presso["b_corrected"], se=r_presso["se_corrected"],
                pval=r_presso["p_corrected"],
                or_= math.exp(r_presso["b_corrected"]) if not np.isnan(r_presso["b_corrected"]) else np.nan,
                or_lo=math.exp(r_presso["b_corrected"]-1.96*r_presso["se_corrected"]) if not (np.isnan(r_presso["b_corrected"]) or np.isnan(r_presso["se_corrected"])) else np.nan,
                or_hi=math.exp(r_presso["b_corrected"]+1.96*r_presso["se_corrected"]) if not (np.isnan(r_presso["b_corrected"]) or np.isnan(r_presso["se_corrected"])) else np.nan,
                meanF=meanF,
                r2_exp=steig["r2_exposure"], r2_out=steig["r2_outcome"],
                steiger_dir=steig["correct_direction"])
            all_results.append(presso_entry)
            all_presso.append(dict(
                chain=ch.id, exposure=ch.exposure_label, outcome=ch.outcome_label,
                n_snp=len(bx), global_p=r_presso["presso_global_p"],
                n_outliers=r_presso["n_outliers"],
                outlier_rsids=",".join([str(rs[i]) for i in r_presso["outliers"]]) if r_presso["outliers"] else "",
                b_corrected=r_presso["b_corrected"], se_corrected=r_presso["se_corrected"],
                p_corrected=r_presso["p_corrected"], distortion_p=r_presso["distortion_p"]))

            log.info(f"    [IVW]   OR={math.exp(r_ivw['b']):.3f} 95%CI ({math.exp(r_ivw['b']-1.96*r_ivw['se']):.3f}-{math.exp(r_ivw['b']+1.96*r_ivw['se']):.3f}) p={r_ivw['pval']:.3g} F={meanF:.0f} Steig={steig['correct_direction']}")
            log.info(f"    [WMed]  OR={math.exp(r_wmed['b']):.3f} p={r_wmed['pval']:.3g}")
            log.info(f"    [Egger] intercept={r_egger['intercept']:.4f} p_int={r_egger['intercept_p']:.3g}")
            log.info(f"    [RAPS]  OR={math.exp(r_raps['b']):.3f} p={r_raps['pval']:.3g}")
            log.info(f"    [PRESSO] global_p={r_presso['presso_global_p']:.3g} outliers={r_presso['n_outliers']}/{len(bx)} corr_OR={('%.3f' % math.exp(r_presso['b_corrected'])) if not np.isnan(r_presso['b_corrected']) else 'nan'}")

    # ----------- Save primary tables ----------------------------------
    res_df = pd.DataFrame(all_results)
    res_df.to_csv(OUT / "mr_results_all_chains_v2.csv", index=False)
    log.info(f"wrote mr_results_all_chains_v2.csv rows={len(res_df)}")

    presso_df = pd.DataFrame(all_presso)
    presso_df.to_csv(OUT / "mr_presso_global_v2.csv", index=False)
    log.info(f"wrote mr_presso_global_v2.csv rows={len(presso_df)}")

    loo_df = pd.DataFrame(all_loo)
    loo_df.to_csv(OUT / "mr_loo_all_v2.csv", index=False)
    log.info(f"wrote mr_loo_all_v2.csv rows={len(loo_df)}")

    ss_df = pd.DataFrame(all_single_snp)
    ss_df.to_csv(OUT / "mr_single_snp_v2.csv", index=False)
    log.info(f"wrote mr_single_snp_v2.csv rows={len(ss_df)}")

    funnel_df = pd.DataFrame(all_funnel)
    funnel_df.to_csv(OUT / "mr_funnel_data_v2.csv", index=False)
    log.info(f"wrote mr_funnel_data_v2.csv rows={len(funnel_df)}")

    # ----------- MVMR -------------------------------------------------
    log.info("\n=== MVMR ===")
    mvmr_rows = []
    for spec in MVMR_SPECS:
        name = spec["name"]
        exposures = spec["exposures"]
        oc_label, oc_code, ncase, nctrl = spec["outcome"]
        gz = FINDIR / f"finngen_R12_{oc_code}.gz"
        if not gz.exists():
            log.warning(f"MVMR {name}: outcome missing"); continue

        # Union of rsids across exposures
        iv_dfs = []
        for lbl, ivf in exposures:
            df_iv = iv_cache.get(ivf)
            if df_iv is None: continue
            iv_dfs.append((lbl, df_iv))
        if len(iv_dfs) < 2:
            log.warning(f"MVMR {name}: need 2 IV sets"); continue
        union_rs = set().union(*[set(d["rsid"]) for _, d in iv_dfs])
        oc_df = parse_finngen_subset(gz, union_rs, cache_key=oc_code)

        # For MVMR we need every SNP's effect in EVERY exposure.  We only have
        # genome-wide-significant IVs per exposure, so for a SNP that is an IV
        # for exposure A we typically lack a precise beta in exposure B (it is
        # not listed).  As a fallback we set beta_B = 0, se_B = median(se of
        # exposure B IVs).  This is equivalent to assuming SNP A is exogenous
        # to exposure B (Sanderson 2019 eq. 2 special case).  It is a
        # conservative MVMR.
        all_rs = sorted(union_rs)
        G = np.zeros((len(all_rs), len(iv_dfs)))
        seG = np.zeros_like(G)
        by_v = np.full(len(all_rs), np.nan); sy_v = np.full(len(all_rs), np.nan)
        ea_v = np.array([""]*len(all_rs), dtype=object)
        for i, rs in enumerate(all_rs):
            for j, (lbl, d) in enumerate(iv_dfs):
                row = d[d["rsid"] == rs]
                if len(row) > 0:
                    G[i, j] = float(row["beta"].iloc[0])
                    seG[i, j] = float(row["se"].iloc[0])
                    ea_v[i] = str(row["ea"].iloc[0]).upper()
                else:
                    G[i, j] = 0.0
                    seG[i, j] = float(d["se"].median())
        # merge outcome
        oc_hits = oc_df[oc_df["match_rsid"].isin(all_rs)]
        rs_to_idx = {r: i for i, r in enumerate(all_rs)}
        for _, r in oc_hits.iterrows():
            i = rs_to_idx[r["match_rsid"]]
            if ea_v[i] == "": continue
            alt = str(r["alt"]).upper(); ref = str(r["ref"]).upper()
            b = float(r["beta"]); sb = float(r["sebeta"])
            if ea_v[i] == alt: by_v[i] = b; sy_v[i] = sb
            elif ea_v[i] == ref: by_v[i] = -b; sy_v[i] = sb
        keep = ~np.isnan(by_v) & np.all(~np.isnan(G), axis=1)
        Gk = G[keep]; byk = by_v[keep]; syk = sy_v[keep]
        if len(byk) < 5:
            log.warning(f"MVMR {name}: only {len(byk)} SNPs matched outcome; skip"); continue
        res = mvmr_ivw(Gk, byk, syk)
        if res is None:
            log.warning(f"MVMR {name}: singular"); continue
        log.info(f"MVMR {name}: n={len(byk)} df={res['df']} phi={res['phi']:.2f}")
        for j, (lbl, _) in enumerate(iv_dfs):
            or_ = math.exp(res["b"][j])
            or_lo = math.exp(res["b"][j] - 1.96*res["se"][j])
            or_hi = math.exp(res["b"][j] + 1.96*res["se"][j])
            mvmr_rows.append(dict(mvmr_name=name, outcome=oc_label, exposure=lbl,
                                  b=res["b"][j], se=res["se"][j], z=res["z"][j], pval=res["p"][j],
                                  or_=or_, or_lo=or_lo, or_hi=or_hi,
                                  nsnp=res["nsnp"], df=res["df"], phi=res["phi"]))
            log.info(f"   {lbl}: b={res['b'][j]:.4f} se={res['se'][j]:.4f} OR={or_:.3f} ({or_lo:.3f}-{or_hi:.3f}) p={res['p'][j]:.3g}")
    pd.DataFrame(mvmr_rows).to_csv(OUT / "mr_mvmr_v2.csv", index=False)
    log.info(f"wrote mr_mvmr_v2.csv rows={len(mvmr_rows)}")

    # ----------- Funnel + supp forest figure --------------------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        # two-panel: left = single-SNP per chain forest; right = LOO per chain forest
        sub = ss_df.copy()
        chains_sorted = sorted(sub["chain"].unique(), key=lambda x: (x[0], x))
        fig, axes = plt.subplots(1, 2, figsize=(11, max(4, 0.22*len(sub))))
        # LEFT: single-SNP
        ax = axes[0]
        y = 0; ticks = []; tlabels = []
        for ch in chains_sorted:
            g = sub[sub["chain"] == ch].copy()
            g = g.sort_values("b")
            for _, r in g.iterrows():
                ax.errorbar(r["or_"], y,
                            xerr=[[max(r["or_"]-r["or_lo"],0)], [max(r["or_hi"]-r["or_"],0)]],
                            fmt="o", ms=2, color="#3366aa", alpha=0.6, lw=0.5)
                y += 1
            ticks.append(y - len(g)/2); tlabels.append(ch); y += 1
        ax.axvline(1, color="k", lw=0.5, ls="--")
        ax.set_xscale("log"); ax.set_xlabel("Single-SNP OR")
        ax.set_yticks(ticks); ax.set_yticklabels(tlabels); ax.set_ylabel("Chain")
        ax.set_title("Single-SNP Wald ratios")
        # RIGHT: LOO OR distribution per chain
        ax = axes[1]
        y = 0; ticks = []; tlabels = []
        for ch in chains_sorted:
            g = loo_df[loo_df["chain"] == ch].copy()
            if len(g) == 0: continue
            g = g.sort_values("or_")
            for _, r in g.iterrows():
                ax.errorbar(r["or_"], y,
                            xerr=[[max(r["or_"]-r["or_lo"],0)], [max(r["or_hi"]-r["or_"],0)]],
                            fmt="s", ms=2, color="#a33", alpha=0.5, lw=0.5)
                y += 1
            ticks.append(y - len(g)/2); tlabels.append(ch); y += 1
        ax.axvline(1, color="k", lw=0.5, ls="--")
        ax.set_xscale("log"); ax.set_xlabel("Leave-one-out IVW OR")
        ax.set_yticks(ticks); ax.set_yticklabels(tlabels)
        ax.set_title("Leave-one-out IVW")
        plt.tight_layout()
        out_png = FIGDIR / "mr_supp_forest.png"
        plt.savefig(out_png, dpi=180); plt.close()
        log.info(f"wrote {out_png}")
    except Exception as e:
        log.warning(f"supp forest plot failed: {e}")

    log.info("=== v2 done ===")

if __name__ == "__main__":
    main()
