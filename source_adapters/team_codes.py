"""One canonical NFL team-code normalizer (refs NFL-75).

Canonical codes are nflverse's: play-by-play, schedules, rosters, pregame packets and the season context all use
them. Other sources use other codes for the same club: ESPN and the Blitz team database (LAR, WSH), NFL game books
(ARZ, BLT, CLV, HST), Pro Football Reference style (GNB, KAN, NWE, NOR, SFO, TAM, LVR), and older seasons (OAK, SD,
STL, JAC, WFT). Mixing them makes joins drop rows silently: the 2026-11-22 data audit found the Rams showed zero
coverage rows until LAR was mapped to LA.

Normalize when a file is read (`read_team_table`, `canon_frame`), before any join. Unknown codes raise instead of
passing through, so a new spelling fails loudly rather than vanishing from a join. Relocated franchises map to the
current code (OAK->LV, SD->LAC, STL->LA): that is franchise identity, which is what every join here needs.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

CANONICAL = frozenset(
    "ARI ATL BAL BUF CAR CHI CIN CLE DAL DEN DET GB HOU IND JAX KC LA LAC LV MIA MIN NE NO NYG NYJ PHI PIT SEA SF TB TEN WAS"
    .split())

ALIASES = {
    "LAR": "LA", "STL": "LA", "SL": "LA",           # Rams: ESPN / Blitz team DB, St. Louis era
    "WSH": "WAS", "WFT": "WAS",                       # Commanders: ESPN / Blitz team DB, Football Team era
    "JAC": "JAX",
    "OAK": "LV", "LVR": "LV",
    "SD": "LAC", "SDG": "LAC",
    "ARZ": "ARI", "BLT": "BAL", "CLV": "CLE", "HST": "HOU",   # NFL game book club codes
    "GNB": "GB", "KAN": "KC", "NWE": "NE", "NOR": "NO", "SFO": "SF", "TAM": "TB",
}


def canon(code) -> str:
    """Canonical code for one team code. Raises ValueError on anything that is not a known NFL code."""
    if not isinstance(code, str):
        raise ValueError(f"team code must be a string, got {code!r}")
    c = code.strip().upper()
    if c in CANONICAL:
        return c
    if c in ALIASES:
        return ALIASES[c]
    raise ValueError(f"unknown NFL team code {code!r}")


def canon_game(game: str, sep: str = "@") -> str:
    """'BUF@LAR' -> 'BUF@LA'."""
    return sep.join(canon(t) for t in str(game).split(sep))


def assert_canonical(values: Iterable, where: str = "") -> None:
    """Raise ValueError naming every value that is not a canonical code."""
    bad = sorted({repr(v) for v in values if not (isinstance(v, str) and v in CANONICAL)})
    if bad:
        raise ValueError(f"non-canonical team codes{(' in ' + where) if where else ''}: {', '.join(bad)}")


def canon_series(s: pd.Series) -> pd.Series:
    """Normalize a column; missing values stay missing, unknown codes raise."""
    return s.map(lambda v: v if (v is None or (isinstance(v, float) and v != v)) else canon(v))


def canon_frame(df: pd.DataFrame, cols: Iterable[str], game_cols: Iterable[str] = ()) -> pd.DataFrame:
    """Copy of df with each team column (and 'AWAY@HOME' game column) normalized."""
    out = df.copy()
    for c in cols:
        out[c] = canon_series(out[c])
    for c in game_cols:
        out[c] = out[c].map(lambda v: v if not isinstance(v, str) else canon_game(v))
    return out


def read_team_table(path, cols: Iterable[str], game_cols: Iterable[str] = (), **read_kw) -> pd.DataFrame:
    """Read a CSV and normalize its team columns at ingest. Use this for any table not already in nflverse codes."""
    read_kw.setdefault("dtype", str)
    read_kw.setdefault("low_memory", False)
    return canon_frame(pd.read_csv(Path(path), **read_kw), cols, game_cols)
