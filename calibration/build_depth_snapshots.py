"""Rebuild the point-in-time depth-chart tables in data/historical/nflverse/derived_pit/ (NFL-75 Phase 2 / 2b).

    python3 -m calibration.build_depth_snapshots --raw-dir /tmp/p2data [--check]

Inputs (not committed; nflverse release assets, retrieved 2026-11-13T08:01:05Z, sha256 verified before use):
  https://github.com/nflverse/nflverse-data/releases/download/depth_charts/depth_charts_2025.parquet
  https://github.com/nflverse/nflverse-data/releases/download/depth_charts/depth_charts_2026.parquet
Outputs:
  depth_qb1_snapshots_2025_2026.csv        rank-1 QB of every snapshot (first row per season, team, dt)
  depth_skill_snapshots_2025_2026.csv.gz   every RB/WR/TE/FB row of every snapshot (gzip mtime 0: reproducible bytes)
--check rebuilds in memory and compares to the committed sha256 values (exit 1 on mismatch); without it the files are
written. No network. Research only."""
from __future__ import annotations
import argparse
import hashlib
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/historical/nflverse/derived_pit"
RAW_SHA = {2025: "14f74185b3c2c48df234ced284ba3596bda3333d0b2a8df40841f68cd34539fa",
           2026: "288f3dbb414da991ddb9a2e5389c80d6c826a99ad8f2881252efb2224c7d8f8f"}
OUT_SHA = {"depth_qb1_snapshots_2025_2026.csv": "c1ab52498fad542f62677e02977494a9283e4e3d78e6d2eb08a3344b0068d5d2",
           "depth_skill_snapshots_2025_2026.csv.gz": "943a55ac51569c242a6a5396f117efffb2438fbbd2e9575444afe744d0941e67"}
SKILL_POS = ("RB", "WR", "TE", "FB")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_raw(raw_dir: Path) -> pd.DataFrame:
    parts = []
    for y, want in RAW_SHA.items():
        p = raw_dir / f"depth_charts_{y}.parquet"
        got = _sha(p.read_bytes())
        if got != want:
            raise SystemExit(f"{p}: sha256 {got} != {want}")
        d = pd.read_parquet(p, columns=["dt", "team", "gsis_id", "player_name", "pos_abb", "pos_rank"])
        d["season"] = y
        parts.append(d)
    return pd.concat(parts)


def build(raw: pd.DataFrame) -> dict:
    q = raw[(raw["pos_abb"] == "QB") & (raw["pos_rank"] == 1)].sort_values(["season", "team", "dt"], kind="stable")
    q = q.drop_duplicates(["season", "team", "dt"])[["season", "team", "dt", "gsis_id", "player_name"]]
    qb = q.to_csv(index=False).encode()
    s = raw[raw["pos_abb"].isin(SKILL_POS)].sort_values(["season", "team", "dt", "pos_abb", "pos_rank"])
    # written exactly as the committed file was: pandas to_csv to a path of that name, gzip mtime 0 (the gzip header
    # carries the file name, and pandas' chunked writes determine the deflate blocks)
    with tempfile.TemporaryDirectory() as td:
        tp = Path(td) / "depth_skill_snapshots_2025_2026.csv.gz"
        s[["season", "team", "dt", "pos_abb", "pos_rank", "gsis_id", "player_name"]].to_csv(
            tp, index=False, compression={"method": "gzip", "mtime": 0})
        sk = tp.read_bytes()
    return {"depth_qb1_snapshots_2025_2026.csv": qb, "depth_skill_snapshots_2025_2026.csv.gz": sk}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", type=Path, required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    out = build(load_raw(a.raw_dir))
    bad = 0
    for name, b in out.items():
        ok = _sha(b) == OUT_SHA[name]
        print(f"{name}: sha256 {_sha(b)} {'OK' if ok else 'MISMATCH (expected ' + OUT_SHA[name] + ')'}")
        bad += not ok
        if not a.check:
            (OUT / name).write_bytes(b)
    sys.exit(1 if (a.check and bad) else 0)


if __name__ == "__main__":
    main()
