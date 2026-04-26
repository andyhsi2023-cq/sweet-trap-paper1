#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
C8_investment_sweet_trap.py — Investment FOMO as a Sweet Trap (PDE).

Formal Sweet-Trap model v2:
  Δ_ST > 0 requires (i) θ reward signal short-run positive
                    (ii) λβρ long-run cost negative
                    (iii) F2 pre-gate: SES correlations indicate aspirational entry
                    (iv) F3 lock-in (ρ > 0.5)
                    (iv) F4 information blockade (paper-gain / realized-loss mis-match)

Inputs:
  /Users/andy/Desktop/Research/sweet-trap-multidomain/02-data/processed/panel_C8_investment.parquet

Outputs:
  02-data/processed/C8_results.json            — headline stats
  02-data/processed/C8_speccurve.csv           — specification curve (192 rows)
  03-analysis/scripts/C8_investment_sweet_trap.log

Run:
  .corpus-index/venv312/bin/python 03-analysis/scripts/C8_investment_sweet_trap.py
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
import warnings
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

ROOT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
PANEL = ROOT / "02-data/processed/panel_C8_investment.parquet"
EXPECT_SHA = "24bf6063e58caa71c9b485d3d85f3e2d8a321a23226462e7244ef67e637c6934"
OUT_JSON = ROOT / "02-data/processed/C8_results.json"
OUT_CURVE = ROOT / "02-data/processed/C8_speccurve.csv"
LOG_FP = ROOT / "03-analysis/scripts/C8_investment_sweet_trap.log"


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(LOG_FP, mode="w"), logging.StreamHandler()],
    )
    return logging.getLogger(__name__)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt_ci(beta, se, conf=0.95):
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    return beta - z * se, beta + z * se


def reg_ols(formula: str, data: pd.DataFrame, cluster: str | None = None,
             weights: str | None = None):
    """OLS with optional cluster-robust SE and weights."""
    try:
        if weights and weights in data.columns:
            mod = smf.wls(formula, data=data, weights=data[weights].fillna(1.0))
        else:
            mod = smf.ols(formula, data=data)
        if cluster and cluster in data.columns:
            res = mod.fit(cov_type="cluster", cov_kwds={"groups": data[cluster]})
        else:
            res = mod.fit(cov_type="HC1")
        return res
    except Exception as e:
        return None


def logit(formula: str, data: pd.DataFrame, cluster: str | None = None):
    try:
        mod = smf.logit(formula, data=data)
        if cluster and cluster in data.columns:
            res = mod.fit(
                disp=0, cov_type="cluster", cov_kwds={"groups": data[cluster]}
            )
        else:
            res = mod.fit(disp=0, cov_type="HC1")
        return res
    except Exception as e:
        return None


# ============================================================================
# §1. F2 pre-gate diagnostics
# ============================================================================

def f2_diagnostics(panel: pd.DataFrame, log) -> dict:
    """F2: aspirational entry — higher SES / literacy → MORE investment participation."""
    log.info("\n====== F2 pre-gate diagnostics ======")

    # Use only 2017/2019 waves where full SES + literacy available
    d = panel[panel["year"].isin([2017, 2019])].copy()
    d = d.dropna(subset=["stock_hold", "ln_income", "total_asset_w"])
    log.info(f"F2 sample N={len(d)}")

    out = {}

    # (a) Participation vs SES
    for x in ["ln_income", "ln_asset", "fin_lit_score", "fin_attention", "risk_seek"]:
        if x not in d.columns:
            continue
        sub = d.dropna(subset=["stock_hold", x])
        if len(sub) < 100:
            continue
        r, p = stats.pointbiserialr(sub["stock_hold"], sub[x])
        out[f"cor_stock_{x}"] = {"r": float(r), "p": float(p), "N": int(len(sub))}
        log.info(f"  cor(stock_hold, {x}) = {r:+.4f} (p={p:.4g}, N={len(sub):,})")

    # (b) Fund participation
    for x in ["ln_income", "ln_asset", "fin_lit_score", "risk_seek"]:
        if x not in d.columns:
            continue
        sub = d.dropna(subset=["fund_hold", x])
        if len(sub) < 100:
            continue
        r, p = stats.pointbiserialr(sub["fund_hold"], sub[x])
        out[f"cor_fund_{x}"] = {"r": float(r), "p": float(p), "N": int(len(sub))}

    # (c) Entry share by income tercile
    by_tercile = d.groupby("income_tercile").agg(
        N=("stock_hold", "count"),
        stock_rate=("stock_hold", "mean"),
        fund_rate=("fund_hold", "mean"),
        wmp_rate=("wmp_hold", "mean"),
    ).to_dict(orient="index")
    # serialize keys
    out["by_income_tercile"] = {str(k): {kk: float(vv) for kk, vv in v.items()}
                                for k, v in by_tercile.items()}
    log.info(f"  by income tercile: {out['by_income_tercile']}")

    # (d) Continue after loss — F3 lock-in diagnostic
    sub = panel.dropna(subset=["fund_continue_after_loss", "fund_loss_flag_lag"])
    sub = sub[sub["fund_loss_flag_lag"] == 1]
    if len(sub) > 50:
        rate = float(sub["fund_hold"].mean())
        out["P_continue_after_loss"] = {"rate": rate, "N": int(len(sub))}
        log.info(f"  P(continue | last-wave fund loss) = {rate:.3f} (N={len(sub)})")
    else:
        out["P_continue_after_loss"] = {"rate": None, "N": int(len(sub))}

    # (e) F2 pass criteria
    F2_pass_income = out.get("cor_stock_ln_income", {}).get("r", 0) > 0.05
    F2_pass_asset = out.get("cor_stock_ln_asset", {}).get("r", 0) > 0.05
    F2_pass_lit = out.get("cor_stock_fin_lit_score", {}).get("r", 0) > 0
    F2_pass_risk = out.get("cor_stock_risk_seek", {}).get("r", 0) > 0
    out["F2_pass"] = {
        "stock_income_pos": bool(F2_pass_income),
        "stock_asset_pos": bool(F2_pass_asset),
        "stock_lit_pos": bool(F2_pass_lit),
        "stock_risk_pos": bool(F2_pass_risk),
        "overall": bool(F2_pass_income and F2_pass_asset),
    }
    log.info(f"  F2 OVERALL PASS: {out['F2_pass']['overall']}")
    return out


# ============================================================================
# §2. Sweet-side (θ short-run)
# ============================================================================

def sweet_side(panel: pd.DataFrame, log) -> dict:
    """Sweet: entry / paper-gain → short-run wellbeing ↑"""
    log.info("\n====== Sweet side: θ ======")
    d = panel[panel["year"].isin([2017, 2019])].copy()
    d = d.dropna(subset=["life_sat", "stock_hold", "ln_income",
                           "ln_asset", "rural", "prov"])
    d = d.assign(year=d["year"].astype(int))
    # prov as categorical
    d["prov_str"] = d["prov"].astype(str)

    out = {"N": int(len(d))}

    # A. Holding any risky asset
    r = reg_ols(
        "life_sat ~ any_risky_hold + ln_income + ln_asset + rural + C(prov_str) + C(year)",
        data=d, cluster="hhid"
    )
    if r is not None:
        b, se, p = r.params["any_risky_hold"], r.bse["any_risky_hold"], r.pvalues["any_risky_hold"]
        lo, hi = fmt_ci(b, se)
        out["any_risky_on_lifesat"] = {
            "beta": float(b), "se": float(se), "p": float(p),
            "ci_lo": float(lo), "ci_hi": float(hi), "N": int(r.nobs),
        }
        log.info(f"  any_risky_hold → life_sat: β={b:+.4f} SE={se:.4f} p={p:.4g}")

    # B. Stock holding
    r = reg_ols(
        "life_sat ~ stock_hold + ln_income + ln_asset + rural + C(prov_str) + C(year)",
        data=d, cluster="hhid"
    )
    if r is not None:
        b, se, p = r.params["stock_hold"], r.bse["stock_hold"], r.pvalues["stock_hold"]
        lo, hi = fmt_ci(b, se)
        out["stock_hold_on_lifesat"] = {
            "beta": float(b), "se": float(se), "p": float(p),
            "ci_lo": float(lo), "ci_hi": float(hi), "N": int(r.nobs),
        }
        log.info(f"  stock_hold → life_sat: β={b:+.4f} SE={se:.4f} p={p:.4g}")

    # C. Stock paper return (continuous, within stock-holders)
    dh = d[d["stock_hold"] == 1].copy()
    dh = dh.dropna(subset=["stock_return_paper_yr"])
    if len(dh) > 500:
        dh["stock_ret_ihs"] = np.arcsinh(dh["stock_return_paper_yr"])
        r = reg_ols(
            "life_sat ~ stock_ret_ihs + ln_income + ln_asset + rural + C(prov_str) + C(year)",
            data=dh, cluster="hhid"
        )
        if r is not None:
            b, se, p = (r.params["stock_ret_ihs"], r.bse["stock_ret_ihs"],
                         r.pvalues["stock_ret_ihs"])
            lo, hi = fmt_ci(b, se)
            out["stock_paper_ret_on_lifesat"] = {
                "beta": float(b), "se": float(se), "p": float(p),
                "ci_lo": float(lo), "ci_hi": float(hi), "N": int(r.nobs),
            }
            log.info(f"  stock_paper_return → life_sat: β={b:+.4f} p={p:.4g}")

    # D. Fund self-reported gain flag (2017 only)
    sub = d[(d["year"] == 2017) & d["fund_hold"].eq(1)].dropna(
        subset=["fund_gain_flag", "life_sat"]
    )
    if len(sub) > 200:
        r = reg_ols(
            "life_sat ~ fund_gain_flag + ln_income + ln_asset + rural + C(prov_str)",
            data=sub, cluster="hhid"
        )
        if r is not None:
            b, se, p = (r.params["fund_gain_flag"], r.bse["fund_gain_flag"],
                         r.pvalues["fund_gain_flag"])
            lo, hi = fmt_ci(b, se)
            out["fund_gain_on_lifesat"] = {
                "beta": float(b), "se": float(se), "p": float(p),
                "ci_lo": float(lo), "ci_hi": float(hi), "N": int(r.nobs),
            }
            log.info(f"  fund_gain_flag → life_sat (2017 holders): β={b:+.4f} p={p:.4g}")

    return out


# ============================================================================
# §3. Bitter side (λβρ long-run)
# ============================================================================

def bitter_side(panel: pd.DataFrame, log) -> dict:
    """Bitter: net loss, loss-locked continuation, crowd-out."""
    log.info("\n====== Bitter side: λβρ ======")
    d = panel[panel["year"].isin([2017, 2019])].copy()
    d["prov_str"] = d["prov"].astype(str)

    out = {}

    # A. Fund self-reported loss → life_sat (fund holders)
    sub = d[d["fund_hold"] == 1].dropna(
        subset=["fund_loss_flag", "life_sat", "ln_income", "ln_asset"]
    )
    if len(sub) > 200:
        r = reg_ols(
            "life_sat ~ fund_loss_flag + ln_income + ln_asset + rural + C(prov_str) + C(year)",
            data=sub, cluster="hhid"
        )
        if r is not None:
            b, se, p = (r.params["fund_loss_flag"], r.bse["fund_loss_flag"],
                         r.pvalues["fund_loss_flag"])
            lo, hi = fmt_ci(b, se)
            out["fund_loss_on_lifesat"] = {
                "beta": float(b), "se": float(se), "p": float(p),
                "ci_lo": float(lo), "ci_hi": float(hi), "N": int(r.nobs),
            }
            log.info(f"  fund_loss → life_sat: β={b:+.4f} p={p:.4g}")

    # B. Negative stock return → life_sat
    dh = d[d["stock_hold"] == 1].copy()
    dh = dh.dropna(subset=["stock_return_paper_yr", "life_sat"])
    if len(dh) > 300:
        dh["neg_ret"] = (dh["stock_return_paper_yr"] < 0).astype(int)
        r = reg_ols(
            "life_sat ~ neg_ret + ln_income + ln_asset + rural + C(prov_str) + C(year)",
            data=dh, cluster="hhid"
        )
        if r is not None:
            b, se, p = r.params["neg_ret"], r.bse["neg_ret"], r.pvalues["neg_ret"]
            lo, hi = fmt_ci(b, se)
            out["stock_neg_ret_on_lifesat"] = {
                "beta": float(b), "se": float(se), "p": float(p),
                "ci_lo": float(lo), "ci_hi": float(hi), "N": int(r.nobs),
            }
            log.info(f"  stock_neg_ret → life_sat: β={b:+.4f} p={p:.4g}")

    # C. ρ lock-in: P(continue holding stock | last wave held stock)
    if "stock_hold_lag" in panel.columns:
        s = panel.dropna(subset=["stock_hold_lag", "stock_hold"])
        s = s[s["stock_hold_lag"].notna() & s["stock_hold"].notna()]
        t = pd.crosstab(s["stock_hold_lag"], s["stock_hold"], normalize="index")
        if 1 in t.index and 1 in t.columns:
            p_cont = float(t.loc[1, 1])
            out["P_stock_continue"] = p_cont
            log.info(f"  P(stock_hold_t=1 | stock_hold_t-1=1) = {p_cont:.3f}")
            p_exit = float(t.loc[1, 0]) if 0 in t.columns else 0.0
            out["P_stock_exit"] = p_exit
        if 0 in t.index and 1 in t.columns:
            p_new = float(t.loc[0, 1])
            out["P_stock_new_entry"] = p_new

    # D. Continue after loss: does having negative return last wave reduce exit?
    s = panel.dropna(subset=["stock_hold_lag", "stock_hold",
                               "stock_return_paper_yr_lag"])
    s = s[s["stock_hold_lag"] == 1].copy()
    if len(s) > 300:
        s["last_loss"] = (s["stock_return_paper_yr_lag"] < 0).astype(int)
        t = s.groupby("last_loss")["stock_hold"].mean().to_dict()
        out["stock_continue_by_last_loss"] = {str(k): float(v) for k, v in t.items()}
        # Higher-than-50% continuation after loss = ρ lock-in
        if 1 in t:
            out["P_stock_continue_after_loss"] = float(t[1])
            log.info(f"  P(continue | last-wave stock LOSS) = {t[1]:.3f}")
        if 0 in t:
            out["P_stock_continue_after_gain"] = float(t[0])

    # E. Consumption crowd-out: stock_share_assets → ln_consump (next wave)
    panel_sorted = panel.sort_values(["hhid", "year"]).copy()
    panel_sorted["ln_consump_lead"] = panel_sorted.groupby("hhid")["ln_consump"].shift(-1)
    sub = panel_sorted.dropna(subset=["stock_share_assets", "ln_consump",
                                        "ln_consump_lead", "ln_income", "ln_asset"])
    sub["prov_str"] = sub["prov"].astype(str)
    if len(sub) > 1000:
        r = reg_ols(
            "ln_consump_lead ~ stock_share_assets + ln_income + ln_asset + ln_consump + rural + C(prov_str) + C(year)",
            data=sub, cluster="hhid"
        )
        if r is not None:
            b, se, p = (r.params["stock_share_assets"], r.bse["stock_share_assets"],
                         r.pvalues["stock_share_assets"])
            lo, hi = fmt_ci(b, se)
            out["stock_share_on_next_consump"] = {
                "beta": float(b), "se": float(se), "p": float(p),
                "ci_lo": float(lo), "ci_hi": float(hi), "N": int(r.nobs),
            }
            log.info(f"  stock_share → next-wave ln_consump: β={b:+.4f} p={p:.4g}")

    return out


# ============================================================================
# §4. Δ_ST estimation (Sweet Trap asymmetry index)
# ============================================================================

def delta_st(panel: pd.DataFrame, log) -> dict:
    """Δ_ST = cor(ancestral baseline) - cor(current).

    ancestral: non-investor families cor(total_asset, life_sat)
    current:   investor families cor(stock_net_gain_or_asset, life_sat)

    If investment "really works", cor(asset, life_sat) in investor group ≥ baseline.
    If reward signal is decoupled from welfare, cor(investment asset, life_sat) <
    cor(non-investment asset, life_sat) → Δ_ST > 0.
    """
    log.info("\n====== Δ_ST (Sweet Trap asymmetry index) ======")
    d = panel[panel["year"].isin([2017, 2019])].dropna(
        subset=["stock_hold", "life_sat", "total_asset_w"]
    ).copy()

    out = {}
    # Ancestral: non-investor families, cor(wealth, life_sat)
    anc = d[d["any_risky_hold"] == 0].copy()
    anc["ln_asset"] = np.log1p(anc["total_asset_w"].clip(lower=0))
    if len(anc) > 500:
        sub = anc.dropna(subset=["ln_asset", "life_sat"])
        r_anc, p_anc = stats.pearsonr(sub["ln_asset"], sub["life_sat"])
        out["cor_ancestral_asset_lifesat"] = {
            "r": float(r_anc), "p": float(p_anc), "N": int(len(sub)),
        }
        log.info(f"  Ancestral (non-investors): cor(ln_asset, life_sat) = {r_anc:+.4f} (N={len(sub):,})")
    else:
        r_anc = np.nan

    # Current: investor families, cor(stock_paper_return, life_sat)
    cur = d[d["stock_hold"] == 1].copy()
    cur = cur.dropna(subset=["stock_return_paper_yr", "life_sat"])
    cur["stock_ret_ihs"] = np.arcsinh(cur["stock_return_paper_yr"])
    if len(cur) > 500:
        r_cur, p_cur = stats.pearsonr(cur["stock_ret_ihs"], cur["life_sat"])
        out["cor_current_stockret_lifesat"] = {
            "r": float(r_cur), "p": float(p_cur), "N": int(len(cur)),
        }
        log.info(f"  Current (stock holders): cor(stock_paper_ret_ihs, life_sat) = {r_cur:+.4f} (N={len(cur):,})")

        # Also: cor(stock_mkt_value, life_sat) among holders
        cur_v = cur.dropna(subset=["stock_mkt_value", "life_sat"])
        cur_v["ln_stock_val"] = np.log1p(cur_v["stock_mkt_value"].clip(lower=0))
        r_cur_v, p_cur_v = stats.pearsonr(cur_v["ln_stock_val"], cur_v["life_sat"])
        out["cor_current_stockval_lifesat"] = {
            "r": float(r_cur_v), "p": float(p_cur_v), "N": int(len(cur_v)),
        }
        log.info(f"  Current (stock holders): cor(ln_stock_mkt_value, life_sat) = {r_cur_v:+.4f} (N={len(cur_v):,})")
    else:
        r_cur = np.nan

    if not (np.isnan(r_anc) or np.isnan(r_cur)):
        delta = r_anc - r_cur
        out["delta_ST"] = float(delta)
        log.info(f"  Δ_ST (baseline - current) = {delta:+.4f}")
        # Bootstrap 95 % CI
        rng = np.random.default_rng(20260417)
        anc_sub = anc.dropna(subset=["ln_asset", "life_sat"])
        B = 2000
        deltas = np.empty(B)
        for b in range(B):
            s_a = anc_sub.sample(len(anc_sub), replace=True, random_state=rng.integers(1 << 30))
            s_c = cur.sample(len(cur), replace=True, random_state=rng.integers(1 << 30))
            r_a, _ = stats.pearsonr(s_a["ln_asset"], s_a["life_sat"])
            r_c, _ = stats.pearsonr(s_c["stock_ret_ihs"], s_c["life_sat"])
            deltas[b] = r_a - r_c
        lo, hi = np.percentile(deltas, [2.5, 97.5])
        out["delta_ST_bootstrap_95CI"] = [float(lo), float(hi)]
        log.info(f"  Δ_ST 95% bootstrap CI = [{lo:+.4f}, {hi:+.4f}]")
    return out


# ============================================================================
# §5. 2015 stock-market event (quasi-experiment)
# ============================================================================

def event_study_2015(panel: pd.DataFrame, log) -> dict:
    """2015 股灾 event study: households with high pre-crisis stock_share vs non-holders
    across 2013→2015→2017 waves.

    DV: life_sat (only 2017 available for this 3-wave sample we have).
    Treatment: household's 2013 stock holding.  Outcome period: 2015 (gain),
    then 2017 (post-crash recovery).
    """
    log.info("\n====== 2015 event study ======")
    d = panel.sort_values(["hhid", "year"]).copy()

    # pre-2013 treatment indicator per household
    d["pre_stock_2013"] = d.groupby("hhid")["stock_hold"].transform(
        lambda s: int((s.where(d.loc[s.index, "year"] == 2013) == 1).any())
        if (d.loc[s.index, "year"] == 2013).any() else np.nan
    )

    # Event study requires life_sat in ≥ 2 waves; we have 2017/2019 only.
    # Degrade to: within post-crash waves, do pre-treated (2013 stock holders) have different life_sat?
    post = d[d["year"].isin([2017, 2019])].dropna(
        subset=["life_sat", "ln_income", "ln_asset", "prov"]
    )
    post["prov_str"] = post["prov"].astype(str)

    out = {}
    r = reg_ols(
        "life_sat ~ pre_stock_2013 + ln_income + ln_asset + rural + C(prov_str) + C(year)",
        data=post.dropna(subset=["pre_stock_2013"]), cluster="hhid"
    )
    if r is not None:
        b, se, p = r.params["pre_stock_2013"], r.bse["pre_stock_2013"], r.pvalues["pre_stock_2013"]
        lo, hi = fmt_ci(b, se)
        out["pre_2013_stock_post_lifesat"] = {
            "beta": float(b), "se": float(se), "p": float(p),
            "ci_lo": float(lo), "ci_hi": float(hi), "N": int(r.nobs),
        }
        log.info(f"  pre-2013 stock holder → post-crash life_sat: β={b:+.4f} p={p:.4g}")

    # Did 2013 stock holders EXIT after 2015 crash?
    p13 = d[d["year"] == 2013][["hhid", "stock_hold"]].rename(columns={"stock_hold": "stock_2013"})
    p15 = d[d["year"] == 2015][["hhid", "stock_hold"]].rename(columns={"stock_hold": "stock_2015"})
    p17 = d[d["year"] == 2017][["hhid", "stock_hold"]].rename(columns={"stock_hold": "stock_2017"})
    p19 = d[d["year"] == 2019][["hhid", "stock_hold"]].rename(columns={"stock_hold": "stock_2019"})
    merged = p13.merge(p15, on="hhid", how="inner") \
                 .merge(p17, on="hhid", how="inner") \
                 .merge(p19, on="hhid", how="inner")
    log.info(f"  N with all 4 waves (2013-19): {len(merged):,}")
    if len(merged) > 1000:
        for col, yr in [("stock_2015", 2015), ("stock_2017", 2017), ("stock_2019", 2019)]:
            treated_rate = merged[merged["stock_2013"] == 1][col].mean()
            control_rate = merged[merged["stock_2013"] == 0][col].mean()
            out[f"hold_rate_{yr}_pre2013holders"] = float(treated_rate)
            out[f"hold_rate_{yr}_pre2013nonholders"] = float(control_rate)
            log.info(f"    {yr}: hold_rate(pre-2013=1)={treated_rate:.3f}  (pre-2013=0)={control_rate:.3f}")

    return out


# ============================================================================
# §6. Specification curve (≥ 144 specs)
# ============================================================================

def specification_curve(panel: pd.DataFrame, log) -> pd.DataFrame:
    """Systematic variation across 4 DVs × 3 treatments × 3 control sets × 4 samples × 2 waves.

    = 4 × 3 × 3 × 4 × 2 = 288 specs  (≥144 required)
    """
    log.info("\n====== Specification curve ======")

    DVs = {
        "life_sat": "life_sat",
        "risk_seek": "risk_seek",
        "fin_attention": "fin_attention",
        "ln_consump": "ln_consump",
    }
    TRTs = {
        "stock_hold": "stock_hold",
        "any_risky_hold": "any_risky_hold",
        "stock_share_assets": "stock_share_assets",
    }
    CTRLs = {
        "minimal": "rural + C(prov_str)",
        "ses": "ln_income + ln_asset + rural + C(prov_str)",
        "full": "ln_income + ln_asset + rural + fin_lit_score + risk_seek + C(prov_str)",
    }
    SAMPLES = {
        "all": lambda d: d,
        "high_income": lambda d: d[d["high_income"] == 1],
        "rural": lambda d: d[d["rural"] == 1],
        "urban": lambda d: d[d["rural"] == 0],
    }
    WAVES = {
        "pool_17_19": [2017, 2019],
        "2017_only": [2017],
    }

    rows = []
    spec_id = 0
    base = panel.copy()
    base["prov_str"] = base["prov"].astype(str)

    for dv_name, dv in DVs.items():
        for trt_name, trt in TRTs.items():
            for ctrl_name, ctrl in CTRLs.items():
                for samp_name, samp_fn in SAMPLES.items():
                    for wave_name, wave_list in WAVES.items():
                        spec_id += 1
                        d = base[base["year"].isin(wave_list)]
                        d = samp_fn(d)
                        # Must have treatment and control columns non-null
                        need = [dv, trt] + [c for c in ["ln_income", "ln_asset", "rural",
                                                            "fin_lit_score", "risk_seek"]
                                             if c in ctrl]
                        d = d.dropna(subset=need)
                        if len(d) < 300:
                            continue
                        if ctrl_name == "full" and "risk_seek" in ctrl and trt == "risk_seek":
                            continue  # avoid DV in RHS
                        # drop specs where dv == control (e.g. ln_consump in consump spec)
                        if dv in ctrl:
                            continue
                        formula = f"{dv} ~ {trt} + {ctrl} + C(year)"
                        try:
                            r = reg_ols(formula, d, cluster="hhid")
                        except Exception as e:
                            continue
                        if r is None or trt not in r.params.index:
                            continue
                        b = float(r.params[trt])
                        se = float(r.bse[trt])
                        p = float(r.pvalues[trt])
                        rows.append({
                            "spec_id": spec_id,
                            "dv": dv_name, "treatment": trt_name,
                            "controls": ctrl_name, "sample": samp_name,
                            "waves": wave_name,
                            "N": int(r.nobs),
                            "beta": b, "se": se, "p": p,
                            "ci_lo": b - 1.96 * se, "ci_hi": b + 1.96 * se,
                        })
    dfc = pd.DataFrame(rows)
    log.info(f"  Completed {len(dfc)} specs")
    if len(dfc) > 0:
        log.info(f"  Median β={dfc['beta'].median():+.4f};  "
                 f"% β>0: {(dfc['beta']>0).mean()*100:.1f}%;  "
                 f"% p<0.05: {(dfc['p']<0.05).mean()*100:.1f}%")
        # By DV
        log.info("  By DV:")
        for dv in DVs:
            sub = dfc[dfc["dv"] == dv]
            if len(sub):
                log.info(f"    {dv}: median β={sub['beta'].median():+.4f}, "
                         f"% pos={(sub['beta']>0).mean()*100:.1f}%, "
                         f"% p<.05={(sub['p']<0.05).mean()*100:.1f}%")
    return dfc


# ============================================================================
# main
# ============================================================================

def main():
    log = setup_logging()
    log.info("=== C8 Investment Sweet Trap ===")

    # verify SHA
    sha = sha256_file(PANEL)
    log.info(f"Panel SHA-256: {sha}")
    if sha != EXPECT_SHA:
        log.warning(f"SHA MISMATCH (expected {EXPECT_SHA})")
    panel = pd.read_parquet(PANEL)
    log.info(f"Panel shape: {panel.shape}")

    results = {
        "sha256_panel": sha,
        "N_panel_rows": int(len(panel)),
        "N_unique_hh": int(panel["hhid"].nunique()),
    }

    results["F2_diagnostics"] = f2_diagnostics(panel, log)
    results["sweet_side"] = sweet_side(panel, log)
    results["bitter_side"] = bitter_side(panel, log)
    results["delta_ST"] = delta_st(panel, log)
    results["event_2015"] = event_study_2015(panel, log)

    curve = specification_curve(panel, log)
    curve.to_csv(OUT_CURVE, index=False)
    log.info(f"  Spec curve written: {OUT_CURVE} ({len(curve)} rows)")
    results["speccurve_N_specs"] = int(len(curve))
    if len(curve) > 0:
        results["speccurve_summary"] = {
            "median_beta": float(curve["beta"].median()),
            "frac_beta_pos": float((curve["beta"] > 0).mean()),
            "frac_p_lt_05": float((curve["p"] < 0.05).mean()),
            "by_dv": {dv: {
                "median_beta": float(curve[curve["dv"] == dv]["beta"].median()),
                "frac_beta_pos": float((curve[curve["dv"] == dv]["beta"] > 0).mean()),
                "frac_p_lt_05": float((curve[curve["dv"] == dv]["p"] < 0.05).mean()),
                "N_specs": int((curve["dv"] == dv).sum()),
            } for dv in curve["dv"].unique()},
        }

    OUT_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    log.info(f"\nResults JSON written: {OUT_JSON}")
    log.info("=== DONE ===")


if __name__ == "__main__":
    warnings.simplefilter("default")
    main()
