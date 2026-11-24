"""This season's team coverage rates (man/zone, middle-of-field open vs closed) from Sharp Football Analysis' free public
table, for the board and the game-day brief (owner, Nov 24, 2026). Our free charting (NGS participation) only has man/zone
through last season.

    python -m pregame.coverage_rates            # refresh data/coverage/sharp_coverage_<season>.csv if older than 20 hours
    python -m pregame.coverage_rates --force

Light use: one page, at most once a day. Fail-soft: a failed pull keeps the previous file. Sharp and StatRankings chart
coverage differently; this file is Sharp only (research/game_logs_2026_w11/sources/COVERAGE_SOURCES.md).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "coverage"
URL = "https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/"
UA = {"User-Agent": "Mozilla/5.0 (research; nfl-matchup-database)"}
FALLBACK = ROOT / "research" / "game_logs_2026_w11" / "sources" / "team_coverage_rates.csv"
NAME2AB = {"Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL", "Buffalo Bills": "BUF", "Carolina Panthers": "CAR",
           "Chicago Bears": "CHI", "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE", "Dallas Cowboys": "DAL", "Denver Broncos": "DEN",
           "Detroit Lions": "DET", "Green Bay Packers": "GB", "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX",
           "Kansas City Chiefs": "KC", "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC", "Los Angeles Rams": "LA", "Miami Dolphins": "MIA",
           "Minnesota Vikings": "MIN", "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG", "New York Jets": "NYJ",
           "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT", "San Francisco 49ers": "SF", "Seattle Seahawks": "SEA",
           "Tampa Bay Buccaneers": "TB", "Tennessee Titans": "TEN", "Washington Commanders": "WAS"}
COLS = {"man rate": "man_pct", "zone rate": "zone_pct", "middle closed rate": "mofc_pct", "middle open rate": "mofo_pct"}


class _Table(HTMLParser):
    """First <table>: header cells and body rows as text."""
    def __init__(self):
        super().__init__()
        self.depth, self.done, self.cell, self.row, self.rows, self.head = 0, False, None, None, [], []

    def handle_starttag(self, tag, attrs):
        if self.done:
            return
        if tag == "table":
            self.depth += 1
        elif self.depth and tag == "tr":
            self.row = []
        elif self.depth and tag in ("td", "th"):
            self.cell = ""

    def handle_endtag(self, tag):
        if self.done:
            return
        if tag == "table" and self.depth:
            self.depth -= 1
            self.done = self.depth == 0
        elif self.depth and tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join(self.cell.split()))
            self.cell = None
        elif self.depth and tag == "tr" and self.row is not None:
            if not self.head:
                self.head = self.row
            else:
                self.rows.append(self.row)
            self.row = None

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data


def parse(html: str) -> dict:
    """{team_abbr: {man_pct, zone_pct, mofc_pct, mofo_pct}} plus the page's 'Updated' date."""
    t = _Table()
    t.feed(html)
    idx = {COLS[h.lower()]: i for i, h in enumerate(t.head) if h.lower() in COLS}
    teams = {}
    for r in t.rows:
        if not r or r[0] not in NAME2AB:
            continue
        vals = {}
        for k, i in idx.items():
            try:
                vals[k] = float(r[i])
            except (IndexError, ValueError):
                vals[k] = None
        teams[NAME2AB[r[0]]] = vals
    m = re.search(r"Updated:?\s*([A-Z][a-z]+ \d{1,2}(?:, \d{4})?)", html)
    return {"teams": teams, "updated": m.group(1) if m else None}


def path(season: int) -> Path:
    return OUT / f"sharp_coverage_{season}.csv"


def refresh(season: int, force=False, fetch=None) -> Path | None:
    p = path(season)
    if p.exists() and not force:
        age = datetime.now(timezone.utc) - datetime.fromtimestamp(p.stat().st_mtime, timezone.utc)
        if age < timedelta(hours=20):
            return p
    try:
        html = fetch(URL) if fetch else urllib.request.urlopen(urllib.request.Request(URL, headers=UA), timeout=30).read().decode("utf-8", "ignore")
        got = parse(html)
    except Exception as e:  # noqa: BLE001
        print(f"coverage_rates: pull failed ({type(e).__name__}: {e}); previous file kept", file=sys.stderr)
        return p if p.exists() else None
    if len(got["teams"]) < 30:
        print(f"coverage_rates: only {len(got['teams'])} teams parsed; previous file kept", file=sys.stderr)
        return p if p.exists() else None
    OUT.mkdir(parents=True, exist_ok=True)
    pulled = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(p, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["team", "season", "man_pct", "zone_pct", "mofc_pct", "mofo_pct", "source_updated", "pulled_utc", "source_url"])
        for ab, v in sorted(got["teams"].items()):
            w.writerow([ab, season, v.get("man_pct"), v.get("zone_pct"), v.get("mofc_pct"), v.get("mofo_pct"), got["updated"], pulled, URL])
    return p


def load(season: int) -> dict:
    """{team: {man_pct, zone_pct, mofc_pct, mofo_pct, source_updated, source}} from the latest pull, else the bots'
    Nov 22 Sharp rows (research/game_logs_2026_w11). Empty if neither exists."""
    out = {}
    p = path(season)
    if p.exists():
        for r in csv.DictReader(open(p)):
            out[r["team"]] = {k: (float(r[k]) if r[k] not in ("", "None") else None) for k in ("man_pct", "zone_pct", "mofc_pct", "mofo_pct")}
            out[r["team"]].update(source_updated=r["source_updated"], source="Sharp Football Analysis (public table)", pulled_utc=r["pulled_utc"])
        return out
    if FALLBACK.exists():
        for r in csv.DictReader(open(FALLBACK)):
            if "sharpfootball" not in r.get("source_url", "") or str(r.get("season")) != str(season) or r["team"] not in NAME2AB:
                continue
            f = lambda k: float(r[k]) if r.get(k) not in ("", None) else None
            out[NAME2AB[r["team"]]] = {"man_pct": f("man_pct"), "zone_pct": f("zone_pct"), "mofc_pct": f("mofc_pct"), "mofo_pct": f("mofo_pct"),
                                       "source_updated": r.get("source_updated"), "source": "Sharp Football Analysis (public table, Nov 22 pull)",
                                       "pulled_utc": r.get("pull_time_AST")}
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--season", type=int, default=datetime.now(timezone.utc).year if datetime.now(timezone.utc).month >= 8 else datetime.now(timezone.utc).year - 1)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    p = refresh(a.season, a.force)
    print(f"coverage_rates: {p.relative_to(ROOT) if p else 'none'}; {len(load(a.season))} teams")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
