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

# The season files NFL Savant offers for download on its About page (2013 onward). Only these published
# downloads are used: the site's robots.txt blocks AI crawlers from its pages, so its internal feeds are not touched.
URL = "https://pub-e9a6e73e336047fba26374ae44334139.r2.dev/pbp-{season}.csv"
NEED = ("GameId", "GameDate", "OffenseTeam", "DefenseTeam", "Yards", "Formation", "IsRush", "IsPass", "IsIncomplete", "PassType", "IsSack", "IsNoPlay")
TEAM_FIX = {"LAR": "LA", "WSH": "WAS", "JAC": "JAX", "ARZ": "ARI", "BLT": "BAL", "CLV": "CLE", "HST": "HOU"}
ZONES = ("SHORT LEFT", "SHORT MIDDLE", "SHORT RIGHT", "DEEP LEFT", "DEEP MIDDLE", "DEEP RIGHT")


def _get(url, timeout=120):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "nfl-pregame-packet/1.0 (research; public data)"}), timeout=timeout) as r:
        return r.read()


PAGES = (URL,)


def _is_csv(raw: bytes) -> bool:
    return b"GameId" in raw[:2000] and b"<html" not in raw[:2000].lower()


def _csv_links(html: bytes, base: str, season: int) -> list[str]:
    """Links on a Savant page that look like this season's play-by-play CSV."""
    import re
    from urllib.parse import urljoin
    out = []
    for href in re.findall(rb"""href\s*=\s*["']([^"']+)["']""", html, flags=re.I):
        h = href.decode("utf-8", "ignore")
        if str(season) in h and ".csv" in h.lower():
            u = urljoin(base, h)
            if u not in out:
                out.append(u)
    return out


def find_csv(season, fetch=_get):
    """Try the known page addresses; accept a CSV directly, or follow a CSV link found on the page."""
    tried, seen = [], []
    for page in PAGES:
        url = page.format(season=season)
        tried.append(url)
        try:
            raw = fetch(url)
        except Exception as exc:
            tried[-1] += f" ({type(exc).__name__})"
            continue
        if _is_csv(raw):
            return url, raw, tried
        import re
        for href in re.findall(rb"""(?:href|action|src)\s*=\s*["']([^"']+)["']""", raw, flags=re.I):
            h = href.decode("utf-8", "ignore")
            if any(k in h.lower() for k in ("csv", "pbp", "download", "dump", "data")) and h not in seen:
                seen.append(h)
        for link in _csv_links(raw, url, season)[:3]:
            tried.append(link)
            try:
                data = fetch(link)
            except Exception as exc:
                tried[-1] += f" ({type(exc).__name__})"
                continue
            if _is_csv(data):
                return link, data, tried
    if seen:
        tried.append("data-like links on those pages: " + ", ".join(seen[:12]))
    return None, None, tried


def load(season, *, offline=False, fetch=_get) -> dict:
    url = URL.format(season=season)
    if offline:
        return {"status": "SKIPPED_OFFLINE", "url": url, "plays": None}
    try:
        url, raw, tried = find_csv(season, fetch)
        if raw is None:
            return {"status": "UNAVAILABLE: no play-by-play CSV found; tried " + "; ".join(tried)[:900], "url": tried[0], "plays": None}
        df = pd.read_csv(io.BytesIO(raw), low_memory=False)
    except Exception as exc:
        return {"status": f"UNAVAILABLE: {type(exc).__name__}: {str(exc)[:120]}", "url": url, "plays": None}
    missing = [c for c in NEED if c not in df.columns]
    if missing:
        return {"status": f"SCHEMA_CHANGED: missing columns {missing}; file has {list(df.columns)[:60]}", "url": url, "plays": None}
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
