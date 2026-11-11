"""NFL Savant play-by-play (nflsavant.com, free CSV): formation and pass-zone splits nflverse does not label.

Adds, per team over its last N games: offence by formation (shotgun / under centre / no huddle) and passing by
zone (short or deep x left, middle, right), for and against. Never raises: an unreachable site or a changed
file layout is reported as a status and the packet simply has no Savant section.
"""
from __future__ import annotations

import io
import urllib.request
from datetime import datetime, timezone

import pandas as pd

URL = "https://nflsavant.com/pbp_data.php?year={season}"
NEED = ("GameId", "GameDate", "OffenseTeam", "DefenseTeam", "Yards", "Formation", "IsRush", "IsPass", "IsIncomplete", "PassType", "IsSack", "IsNoPlay")
TEAM_FIX = {"LAR": "LA", "WSH": "WAS", "JAC": "JAX", "ARZ": "ARI", "BLT": "BAL", "CLV": "CLE", "HST": "HOU"}
ZONES = ("SHORT LEFT", "SHORT MIDDLE", "SHORT RIGHT", "DEEP LEFT", "DEEP MIDDLE", "DEEP RIGHT")


def _get(url, timeout=120):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "nfl-pregame-packet/1.0 (research; public data)"}), timeout=timeout) as r:
        return r.read()


def load(season, *, offline=False, fetch=_get) -> dict:
    url = URL.format(season=season)
    if offline:
        return {"status": "SKIPPED_OFFLINE", "url": url, "plays": None}
    try:
        df = pd.read_csv(io.BytesIO(fetch(url)), low_memory=False)
    except Exception as exc:
        return {"status": f"UNAVAILABLE: {type(exc).__name__}: {str(exc)[:120]}", "url": url, "plays": None}
    missing = [c for c in NEED if c not in df.columns]
    if missing:
        return {"status": f"SCHEMA_CHANGED: missing columns {missing[:6]}", "url": url, "plays": None}
    df = df[(df.IsNoPlay == 0) & ((df.IsPass == 1) | (df.IsRush == 1) | (df.IsSack == 1))].copy()
    if not len(df):
        return {"status": "EMPTY: no scrimmage plays in the file", "url": url, "plays": None}
    for c in ("OffenseTeam", "DefenseTeam"):
        df[c] = df[c].astype(str).str.strip().replace(TEAM_FIX)
    df["GameDate"] = pd.to_datetime(df.GameDate, errors="coerce")
    df["Formation"] = df.Formation.astype(str).str.upper().str.strip()
    df["PassType"] = df.PassType.astype(str).str.upper().str.strip()
    return {"status": "OK", "url": url, "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "latest_game": str(df.GameDate.max().date()), "rows": int(len(df)), "plays": df}


def team_splits(plays, team, before, window=8) -> dict | None:
    """Formation and pass-zone splits for one team over its last `window` games before `before` (YYYY-MM-DD)."""
    if plays is None:
        return None
    p = plays[plays.GameDate < pd.Timestamp(before)]

    def recent(col):
        x = p[p[col] == team]
        gids = x.drop_duplicates("GameId").sort_values("GameDate").GameId.tolist()[-window:]
        return x[x.GameId.isin(gids)], len(gids)

    def formations(x):
        out = []
        for f, g in x.groupby("Formation"):
            if len(g) >= 10:
                out.append({"formation": f.title(), "plays": int(len(g)), "share": round(len(g) / len(x), 3),
                            "pass_rate": round(float(((g.IsPass == 1) | (g.IsSack == 1)).mean()), 3), "yards_per_play": round(float(g.Yards.mean()), 2)})
        return sorted(out, key=lambda r: -r["plays"])

    def zones(x):
        a = x[(x.IsPass == 1) & x.PassType.isin(ZONES)]
        out = []
        for z in ZONES:
            g = a[a.PassType == z]
            if len(g):
                out.append({"zone": z.title(), "attempts": int(len(g)), "share": round(len(g) / len(a), 3),
                            "completion_rate": round(float((g.IsIncomplete == 0).mean()), 3), "yards_per_attempt": round(float(g.Yards.mean()), 2)})
        return out

    off, n_off = recent("OffenseTeam")
    dfn, n_def = recent("DefenseTeam")
    if not n_off and not n_def:
        return None
    return {"games": {"offense": n_off, "defense": n_def}, "offense_by_formation": formations(off), "offense_pass_zones": zones(off),
            "defense_vs_formation": formations(dfn), "defense_pass_zones_allowed": zones(dfn)}
