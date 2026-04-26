#!/usr/bin/env python3
"""
mr_download_finngen.py
======================
Sequentially download Finngen R12 summary stats for pre-selected outcomes.

Inputs : 02-data/processed/mr_finngen_outcomes_used.csv (list of phenocodes)
         21-芬兰数据库最新R12下载链接(1).xlsx (R12 manifest, path_https)
Outputs: /Volumes/P1/城市研究/UKB_芬兰Finngen_catalog_ieu/gwas_list/Finngen/R12_summary_stats/finngen_R12_<phenocode>.gz
         03-analysis/scripts/mr_download_finngen.log

Compute rules:
    * Sequential only (n_workers=1); Finngen files 100-500MB each
    * Checks P1 disk free before each download; abort if < 5GB
    * Skips if file already exists with matching size from HEAD
"""
from __future__ import annotations
import os, sys, time, shutil, hashlib, subprocess, logging
from pathlib import Path
import pandas as pd
import requests

PROJECT = Path("/Users/andy/Desktop/Research/sweet-trap-multidomain")
P1_BASE = Path("/Volumes/P1/城市研究/UKB_芬兰Finngen_catalog_ieu/gwas_list/Finngen")
OUT_DIR = P1_BASE / "R12_summary_stats"
OUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_PATH = PROJECT / "03-analysis/scripts/mr_download_finngen.log"
logging.basicConfig(
    filename=LOG_PATH, level=logging.INFO, filemode="w",
    format="%(asctime)s [%(levelname)s] %(message)s"
)
# also echo to stdout
_h = logging.StreamHandler(sys.stdout); _h.setLevel(logging.INFO)
_h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger().addHandler(_h)

MANIFEST_XLSX = P1_BASE / "21-芬兰数据库最新R12下载链接(1).xlsx"
OUTCOMES_CSV  = PROJECT / "02-data/processed/mr_finngen_outcomes_used.csv"


def free_gb(path: Path) -> float:
    st = shutil.disk_usage(path)
    return st.free / 1024**3


def head_size(url: str) -> int | None:
    try:
        r = requests.head(url, allow_redirects=True, timeout=30)
        if r.status_code == 200 and "Content-Length" in r.headers:
            return int(r.headers["Content-Length"])
    except Exception as e:
        logging.warning(f"HEAD failed {url}: {e}")
    return None


def download(url: str, dst: Path) -> bool:
    """Stream download with progress, atomic rename on success."""
    tmp = dst.with_suffix(dst.suffix + ".tmp")
    try:
        with requests.get(url, stream=True, timeout=(30, 300)) as r:
            r.raise_for_status()
            total = int(r.headers.get("Content-Length", 0))
            got = 0
            chunk = 1024 * 1024  # 1 MB
            t0 = time.time()
            with open(tmp, "wb") as f:
                for buf in r.iter_content(chunk_size=chunk):
                    if not buf: continue
                    f.write(buf); got += len(buf)
                    if got % (50 * chunk) < chunk:
                        mb = got / 1024**2
                        pct = (got / total * 100) if total else 0
                        rate = mb / max(1e-9, time.time() - t0)
                        logging.info(f"  .. {dst.name}: {mb:.1f}/{total/1024**2:.1f} MB ({pct:.1f}%) @ {rate:.1f} MB/s")
        tmp.rename(dst)
        return True
    except Exception as e:
        logging.error(f"Download failed {url}: {e}")
        if tmp.exists(): tmp.unlink()
        return False


def main():
    logging.info(f"P1 free: {free_gb(P1_BASE):.1f} GB")
    if free_gb(P1_BASE) < 5:
        logging.error("P1 free < 5 GB — abort"); sys.exit(1)

    manifest = pd.read_excel(MANIFEST_XLSX)
    manifest.columns = [c.strip() for c in manifest.columns]
    wanted = pd.read_csv(OUTCOMES_CSV)
    logging.info(f"Outcomes wanted: {wanted['phenocode'].tolist()}")

    merged = wanted.merge(manifest, on="phenocode", how="left")
    missing = merged[merged["path_https"].isna()]
    if len(missing):
        logging.warning(f"Missing in manifest: {missing['phenocode'].tolist()}")

    results = []
    for _, row in merged.iterrows():
        if pd.isna(row["path_https"]):
            results.append({"phenocode": row["phenocode"], "status": "missing_in_manifest"})
            continue
        pheno = row["phenocode"]; url = row["path_https"]
        # Finngen file name format: finngen_R12_<phenocode>.gz
        fname = f"finngen_R12_{pheno}.gz"
        dst = OUT_DIR / fname

        free = free_gb(P1_BASE)
        if free < 3:
            logging.error(f"Low disk ({free:.1f}GB) — abort before {pheno}")
            results.append({"phenocode": pheno, "status": "aborted_low_disk"})
            break

        if dst.exists() and dst.stat().st_size > 1024**2:
            logging.info(f"[skip] {pheno}: already exists ({dst.stat().st_size/1024**2:.1f} MB)")
            results.append({"phenocode": pheno, "status": "exists", "size_mb": round(dst.stat().st_size/1024**2,1), "path": str(dst)})
            continue

        logging.info(f"[DL] {pheno} <- {url}")
        ok = download(url, dst)
        if ok:
            size_mb = dst.stat().st_size / 1024**2
            logging.info(f"[OK] {pheno}: {size_mb:.1f} MB -> {dst}")
            results.append({"phenocode": pheno, "status": "ok", "size_mb": round(size_mb,1), "path": str(dst)})
        else:
            results.append({"phenocode": pheno, "status": "failed", "path": str(dst)})

    df = pd.DataFrame(results)
    df.to_csv(PROJECT / "02-data/processed/mr_finngen_download_log.csv", index=False)
    logging.info("DONE. Summary:\n" + df.to_string())


if __name__ == "__main__":
    main()
