"""Shared helpers: sourced fields, pbp / roster loading with pull times. Missing -> "unknown", never zero."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

from pipeline.read_rules import UNKNOWN

ROOT = Path(__file__).resolve().parents[2]
NFLVERSE = ROOT / "data/historical/nflverse"
PBP_DEFAULT = NFLVERSE / "pbp_2026_w1_11_pulled_20261124T1717ET.parquet"
ROSTER_DEFAULT = NFLVERSE / "ros_2026.parquet"
SHARP_DEFAULT = ROOT / "data/coverage/sharp_coverage_2026.csv"
PFF_DIR_DEFAULT = ROOT / "data/pff_captures_w1_8"


def is_unknown(v) -> bool:
    if v is None:
        return True
    if isinstance(v, str):
        return v.strip().lower() in ("", UNKNOWN, "nan", "none")
    if isinstance(v, (list, dict, tuple)):
        return len(v) == 0
    try:
        return bool(pd.isna(v))
    except (TypeError, ValueError):
        return False


def field(value, source: str, pulled_at: str | None, **extra) -> dict:
    """One sourced figure. A missing value is stored as "unknown" (never 0) and keeps its source + pull time."""
    v = UNKNOWN if is_unknown(value) else value
    if hasattr(v, "item") and not isinstance(v, (list, dict, str)):
        v = v.item()  # numpy scalar -> python
    if isinstance(v, float):
        v = round(v, 4)
    d = {"value": v, "source": source, "pulled_at": pulled_at or UNKNOWN}
    d.update(extra)
    return d


def pull_time_for(path: Path) -> str:
    """Pull time from a sibling *.provenance.json (pulled_utc), else from a _pulled_<stamp> filename, else unknown."""
    path = Path(path)
    prov = path.with_name(path.name.replace(".parquet", ".provenance.json"))
    if prov.exists():
        try:
            j = json.loads(prov.read_text())
            for k in ("pulled_utc", "retrieved_utc", "pulled_et"):
                if j.get(k):
                    return str(j[k])
        except (OSError, ValueError):
            pass
    m = re.search(r"pulled_(\d{8}T\d{4,6}(?:ET|Z))", path.name)
    return m.group(1) if m else UNKNOWN


def load_pbp(path: Path | str | None = None) -> tuple[pd.DataFrame, str, str]:
    p = Path(path) if path else PBP_DEFAULT
    df = pd.read_parquet(p)
    if "season_type" in df:
        df = df[df.season_type.fillna("REG") == "REG"]
    return df, f"nflverse play-by-play ({p.relative_to(ROOT) if p.is_relative_to(ROOT) else p})", pull_time_for(p)


def load_positions(path: Path | str | None = None) -> dict:
    """gsis_id -> position (season roster). Unknown ids are simply absent (caller treats as unknown)."""
    p = Path(path) if path else ROSTER_DEFAULT
    if not p.exists():
        return {}
    r = pd.read_parquet(p, columns=["gsis_id", "position", "depth_chart_position"])
    r = r.dropna(subset=["gsis_id"]).drop_duplicates("gsis_id", keep="last")
    pos = r.position.fillna("").astype(str).str.upper()
    dcp = r.depth_chart_position.fillna("").astype(str).str.upper()
    # DB is the roster group; depth-chart position separates CB from S where present
    pos = pos.where(pos != "DB", dcp.where(dcp.isin(["CB", "S", "FS", "SS", "SAF", "NB"]), "DB"))
    return dict(zip(r.gsis_id, pos))


def clean_plays(pbp: pd.DataFrame) -> pd.DataFrame:
    p = pbp
    if "two_point_attempt" in p:
        p = p[p.two_point_attempt.fillna(0) != 1]
    return p
