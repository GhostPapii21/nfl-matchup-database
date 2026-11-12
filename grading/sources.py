"""Inputs for grading, all free and already used by this repository. No paid API is called here.

  * Pregame packet: the version of pregame/packets/<game>/packet.json committed before kickoff (git history),
    so a post-game packet refresh can never leak into what is graded.
  * Pre-kickoff prices: the packet's book section, pregame/line_history/<game>.jsonl and any saved price freeze
    pregame/price_freezes/*_<AWAY>@<HOME>/freeze_*.json. Every snapshot keeps its own pull time; only snapshots
    pulled before kickoff are used. Freeze files are read as data (no pregame module is imported or run).
  * Actual results: nflverse public releases (games, play-by-play, weekly rosters, snap counts), the same
    URLs pregame/sources.py uses.
"""
from __future__ import annotations

import glob
import hashlib
import json
import re
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from .core import UNKNOWN, known, parse_utc, u

ROOT = Path(__file__).resolve().parents[1]
ET = ZoneInfo("America/New_York")
NFLVERSE = "https://github.com/nflverse/nflverse-data/releases/download"   # same base as pregame/sources.py
DATASETS = {
    "games": "schedules/games.parquet",
    "pbp": "pbp/play_by_play_{season}.parquet",
    "rosters": "weekly_rosters/roster_weekly_{season}.parquet",
    "snap_counts": "snap_counts/snap_counts_{season}.parquet",
}
UA = {"User-Agent": "nfl-grading-loop/1.0 (research; public data)"}

TEAM_NAMES = {
    "Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL", "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR", "Chicago Bears": "CHI", "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL", "Denver Broncos": "DEN", "Detroit Lions": "DET", "Green Bay Packers": "GB",
    "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX", "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC", "Los Angeles Rams": "LA", "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN", "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG",
    "New York Jets": "NYJ", "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT", "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA", "Tampa Bay Buccaneers": "TB", "Tennessee Titans": "TEN", "Washington Commanders": "WAS",
}
FREEZE_MARKETS = {
    "h2h": "moneyline", "spreads": "spread", "totals": "total",
    "player_reception_yds": "receiving_yards", "player_receptions": "receptions", "player_rush_yds": "rushing_yards",
    "player_rush_attempts": "carries", "player_pass_yds": "passing_yards", "player_pass_attempts": "pass_attempts",
    "player_pass_completions": "completions",
}
SUFFIXES = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv", "v"}


# ---------------------------------------------------------------- names
def norm(name: str) -> str:
    return re.sub(r"[^a-z]", "", str(name).lower())


def abbrev(full_name: str) -> str:
    """'Malik Nabers' -> 'm.nabers'; 'J.J. McCarthy' -> 'j.mccarthy'; suffixes dropped (nflverse short-name style)."""
    toks = [t for t in str(full_name).replace("'", "").split() if t.lower() not in SUFFIXES]
    if len(toks) < 2:
        return norm(full_name)
    return toks[0][0].lower() + "." + norm(toks[-1])


def short_key(short_name: str) -> str:
    s = str(short_name)
    if "." in s:
        first, last = s.split(".", 1)[0], s.rsplit(".", 1)[-1]
        return first[:1].lower() + "." + norm(last)
    return norm(s)


# ---------------------------------------------------------------- packet before kickoff
def _git(root: Path, *args) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout


def packet_before_kickoff(game_id: str, kickoff: datetime, root: Path = ROOT, max_commits: int = 300):
    """Return (packet, source, generated_utc) for the newest packet generated before kickoff, or (None, reason, None)."""
    rel = f"pregame/packets/{game_id}/packet.json"
    try:
        shas = _git(root, "log", f"-{max_commits}", "--format=%H", "--", rel).split()
    except (subprocess.CalledProcessError, FileNotFoundError):
        shas = []
    for sha in shas:
        try:
            pk = json.loads(_git(root, "show", f"{sha}:{rel}"))
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            continue
        t = parse_utc(pk.get("generated_utc"))
        if t is not None and t < kickoff:
            return pk, f"git:{sha}:{rel}", pk.get("generated_utc")
    p = root / rel
    if not shas and p.exists():
        pk = json.loads(p.read_text())
        t = parse_utc(pk.get("generated_utc"))
        if t is not None and t < kickoff:
            return pk, f"file:{rel}", pk.get("generated_utc")
    return None, f"no {rel} generated before kickoff {kickoff.isoformat()}", None


# ---------------------------------------------------------------- pre-kickoff price snapshots
def packet_snapshots(pk: dict, source: str) -> list[dict]:
    books = pk.get("books") or {}
    pulled = books.get("retrieved_utc")
    out = []
    for key, m in (books.get("markets") or {}).items():
        for bk, q in (m.get("books") or {}).items():
            if not isinstance(q, dict):
                continue
            out.append({"market_key": key, "book": bk, "line": q.get("line"), "prices": q.get("prices") or {},
                        "snapshot_utc": pulled, "quote_utc": q.get("last_update"), "source": f"{source}#books"})
    return out


def line_history_snapshots(game_id: str, root: Path = ROOT) -> list[dict]:
    rel = f"pregame/line_history/{game_id}.jsonl"
    p = root / rel
    out = []
    if not p.exists():
        return out
    for n, ln in enumerate(p.read_text().splitlines(), 1):
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            continue
        for key, books in (r.get("markets") or {}).items():
            for bk, q in (books or {}).items():
                out.append({"market_key": key, "book": bk, "line": q.get("line"), "prices": q.get("prices") or {},
                            "snapshot_utc": r.get("t"), "quote_utc": UNKNOWN, "source": f"file:{rel}:line{n}"})
    return out


FREEZE_DIR = "pregame/price_freezes"


def _freeze_files(away: str, home: str, root: Path, ref: str | None):
    """Yield (relative path, text, source label) for every saved freeze of this game.

    ref=None reads the working tree. A git ref reads the files at that ref with `git ls-tree` / `git show`
    (data only: nothing on that ref is imported or executed). v2 files are listed first so that when a v1 and a
    v2 file share a pull time, the v2 quote wins.
    """
    pat = re.compile(rf"^{re.escape(FREEZE_DIR)}/[^/]*_{re.escape(away)}@{re.escape(home)}/freeze_[^/]*\.json$")
    if ref is None:
        rels = [str(Path(f).relative_to(root)) for f in glob.glob(str(root / FREEZE_DIR / f"*_{away}@{home}" / "freeze_*.json"))]
        rels = [r for r in rels if pat.match(r)]
        read, label = (lambda r: (root / r).read_text()), (lambda r: f"file:{r}")
    else:
        sha = _git(root, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()
        rels = [r for r in _git(root, "ls-tree", "-r", "--name-only", sha, "--", FREEZE_DIR + "/").split() if pat.match(r)]
        read, label = (lambda r: _git(root, "show", f"{sha}:{r}")), (lambda r: f"git:{ref}@{sha}:{r}")
    for rel in sorted(rels, key=lambda r: (0 if "/freeze_v2_" in r else 1, r)):
        try:
            yield rel, read(rel), label(rel)
        except (OSError, subprocess.CalledProcessError):
            continue


def _consensus_entry(c: dict | None, source: str, pulled):
    """A freeze market's consensus. A "no consensus" string (or anything that is not a same-line consensus) is
    unknown, recorded with the reason; it is never treated as missing data to be filled or as zero."""
    if not isinstance(c, dict):
        return None
    raw = c.get("consensus")
    if isinstance(raw, dict) and (known(raw.get("line")) or isinstance(raw.get("no_vig"), dict)):   # moneyline has no line
        val = {"line": raw.get("line") if known(raw.get("line")) else "n/a (no line)", "n_books_at_line": u(raw.get("n_books_at_line")),
               "books_at_line": raw.get("books_at_line") or [], "no_vig": raw.get("no_vig") or UNKNOWN}
        reason = ""
    else:
        val = UNKNOWN
        reason = str(raw) if isinstance(raw, str) and raw else (c.get("reason") or "no same-line consensus in freeze")
    return {"value": val, "reason": reason, "label": c.get("label") or UNKNOWN,
            "book_lines": c.get("book_lines") or {}, "source": source, "pulled_utc": pulled or UNKNOWN}


def freeze_data(away: str, home: str, root: Path = ROOT, ref: str | None = None) -> tuple[list[dict], list[dict]]:
    """Saved price freezes (Blitz's files), read as data. Returns (per-book snapshots, consensus records).

    Handles schema 1 (`rows` list, spread line quoted for side_a) and schema 2 / freeze_v2 (`markets` keyed like
    the packet's book section, spread line = home handicap, plus a `consensus` block). Per-book lines are what
    grading uses; consensus is reported for reference only. Unparseable rows are skipped, never guessed.
    """
    snaps, cons = [], []
    for rel, text, src in _freeze_files(away, home, root, ref):
        try:
            d = json.loads(text)
        except json.JSONDecodeError:
            continue
        pulled = (d.get("meta") or {}).get("pulled_utc")
        if isinstance(d.get("markets"), dict):                                   # schema 2 (freeze_v2_*.json)
            for key, m in d["markets"].items():
                for bk, q in ((m or {}).get("books") or {}).items():
                    if not isinstance(q, dict) or not isinstance(q.get("prices"), dict):
                        continue                                                   # e.g. a book with "no props"
                    if key != "moneyline" and not known(q.get("line")):
                        continue
                    snaps.append({"market_key": key, "book": bk, "line": q.get("line"), "prices": q["prices"],
                                  "snapshot_utc": pulled, "quote_utc": q.get("last_update"), "source": src})
            for key, c in (d.get("consensus") or {}).items():
                e = _consensus_entry(c, src, pulled)
                if e:
                    cons.append(dict(e, market_key=key))
            continue
        for r in d.get("rows") or []:                                              # schema 1
            mk = FREEZE_MARKETS.get(r.get("market"))
            if mk is None:
                continue
            a, b = r.get("side_a"), r.get("side_b")
            if mk in ("moneyline", "spread"):
                a, b = TEAM_NAMES.get(a, a), TEAM_NAMES.get(b, b)
                if {a, b} != {home, away}:
                    continue
            line = r.get("line")
            if mk == "spread":
                if not known(line):
                    continue
                line = float(line) if a == home else -float(line)       # store as the home handicap
            key = mk if mk in ("moneyline", "spread", "total") else f"{mk}|{r.get('player')}"
            snaps.append({"market_key": key, "book": r.get("book"), "line": line,
                          "prices": {a: r.get("price_a"), b: r.get("price_b")},
                          "snapshot_utc": pulled, "quote_utc": r.get("book_last_update"), "source": src})
    return snaps, cons


def freeze_snapshots(away: str, home: str, root: Path = ROOT, ref: str | None = None) -> list[dict]:
    return freeze_data(away, home, root, ref)[0]


def closing_consensus(cons: list[dict], market_key: str, kickoff) -> dict:
    """Consensus from the latest freeze before kickoff, for reference only (never used for CLV)."""
    best = None
    for c in cons:
        t = parse_utc(c.get("pulled_utc"))
        if c.get("market_key") != market_key or t is None or t >= kickoff:
            continue
        if best is None or t > parse_utc(best["pulled_utc"]):
            best = c
    if best is None:
        return {"value": UNKNOWN, "reason": "no saved freeze consensus before kickoff", "source": UNKNOWN, "pulled_utc": UNKNOWN}
    return {k: v for k, v in best.items() if k != "market_key"}


# ---------------------------------------------------------------- actual results (nflverse, free)
def _get(url: str, timeout: int = 180) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def fetch_nflverse(season: int, cache: Path, *, offline: bool = False, fetch=_get) -> dict:
    """Download (or reuse cached) nflverse files. Returns {name: {path, url, sha256, retrieved_utc, status}}."""
    cache.mkdir(parents=True, exist_ok=True)
    out = {}
    for name, rel in DATASETS.items():
        url = f"{NFLVERSE}/{rel.format(season=season)}"
        path = cache / Path(rel.format(season=season)).name
        stamp = path.with_suffix(path.suffix + ".retrieved_utc")
        rec = {"url": url, "path": None, "status": "OK", "retrieved_utc": UNKNOWN, "sha256": UNKNOWN}
        if not offline:
            try:
                path.write_bytes(fetch(url))
                stamp.write_text(datetime.now(timezone.utc).isoformat(timespec="seconds"))
            except Exception as exc:  # network or not yet published
                rec["status"] = f"FETCH_FAILED: {type(exc).__name__}"
        if path.exists():
            rec["path"] = str(path)
            rec["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            rec["retrieved_utc"] = stamp.read_text().strip() if stamp.exists() else UNKNOWN
            if rec["status"] != "OK":
                rec["status"] = "STALE_CACHE_USED; " + rec["status"]
        elif rec["status"] == "OK":
            rec["status"] = "MISSING_OFFLINE"
        out[name] = rec
    return out


def kickoff_from_games(games, game_id: str):
    row = games[games.game_id == game_id]
    if row.empty:
        return None
    r = row.iloc[0]
    try:
        local = datetime.strptime(f"{r.gameday} {r.gametime}", "%Y-%m-%d %H:%M").replace(tzinfo=ET)
    except (TypeError, ValueError):
        return None
    return local.astimezone(timezone.utc)


def kickoff_from_packet(pk: dict):
    g = (pk or {}).get("game") or {}
    try:
        return datetime.strptime(f"{g['date']} {g['kickoff_et']}", "%Y-%m-%d %H:%M").replace(tzinfo=ET).astimezone(timezone.utc)
    except (KeyError, TypeError, ValueError):
        return None


class Actuals:
    """Final score and per-player box stats for one game, computed from nflverse play-by-play.

    Player stats count only plays nflverse attributes to the player (no laterals), so a figure can differ from
    the official box score by a lateral or a late stat correction. A player with no snaps and no plays is
    "unknown" (did not play or not recorded), never 0.
    """

    STATS = ("receiving_yards", "receptions", "targets", "rushing_yards", "carries", "rush_attempts",
             "passing_yards", "pass_attempts", "completions")

    def __init__(self, game_id: str, games, pbp, rosters, snaps, provenance: dict):
        self.game_id, self.prov, self.games_df = game_id, provenance, games
        g = games[games.game_id == game_id]
        self.game = g.iloc[0].to_dict() if not g.empty else {}
        self.week = self.game.get("week")
        self.home, self.away = self.game.get("home_team"), self.game.get("away_team")
        self.pbp = pbp[pbp.game_id == game_id] if pbp is not None else None
        self.rosters = rosters
        self.snaps = snaps[snaps.game_id == game_id] if snaps is not None else None

    def src(self, name):
        r = self.prov.get(name) or {}
        return f"{r.get('url', UNKNOWN)} sha256={r.get('sha256', UNKNOWN)}", r.get("retrieved_utc", UNKNOWN)

    def final(self) -> bool:
        hs, as_ = self.game.get("home_score"), self.game.get("away_score")
        return known(hs) and known(as_) and self.pbp is not None and len(self.pbp) > 0

    def score(self, team: str):
        if not self.final():
            return UNKNOWN
        return int(self.game["home_score"] if team == self.home else self.game["away_score"])

    # identity -------------------------------------------------------------
    def _roster(self):
        r = self.rosters
        if r is None:
            return None
        r = r[r.team.isin([self.home, self.away])]
        if self.week is not None and "week" in r:
            wk = r[r.week == self.week]
            r = wk if len(wk) else r
        return r.drop_duplicates("gsis_id")

    def resolve_full(self, full_name: str, team: str | None = None) -> dict:
        """Match by full name (and team when given). Exactly one roster match or the player is unknown."""
        r = self._roster()
        if r is None or not known(full_name):
            return {"gsis_id": UNKNOWN, "team": UNKNOWN, "reason": "roster unavailable"}
        m = r[r.full_name.map(norm) == norm(full_name)]
        if team:
            m = m[m.team == team]
        if len(m) != 1:
            return {"gsis_id": UNKNOWN, "team": UNKNOWN, "reason": f"{len(m)} roster matches for '{full_name}' {team or ''}".strip()}
        return {"gsis_id": m.iloc[0].gsis_id, "team": m.iloc[0].team, "full_name": m.iloc[0].full_name, "reason": ""}

    def resolve_short(self, short_name: str, team: str) -> dict:
        r = self._roster()
        if r is None:
            return {"gsis_id": UNKNOWN, "team": UNKNOWN, "reason": "roster unavailable"}
        m = r[(r.team == team) & (r.full_name.map(abbrev) == short_key(short_name))]
        if len(m) != 1:
            return {"gsis_id": UNKNOWN, "team": UNKNOWN, "reason": f"{len(m)} roster matches for '{short_name}' on {team}"}
        return {"gsis_id": m.iloc[0].gsis_id, "team": team, "full_name": m.iloc[0].full_name, "reason": ""}

    # stats -----------------------------------------------------------------
    def _played(self, gsis_id: str, full_name: str | None, team: str) -> bool:
        p = self.pbp
        if p is not None and len(p):
            ids = set(p.passer_player_id.dropna()) | set(p.rusher_player_id.dropna()) | set(p.receiver_player_id.dropna())
            if gsis_id in ids:
                return True
        s = self.snaps
        if s is not None and full_name and len(s):
            m = s[(s.team == team) & (s.player.map(norm) == norm(full_name))]
            return bool(len(m)) and float(m.offense_snaps.fillna(0).sum()) > 0
        return False

    def stat(self, gsis_id, full_name, team, stat: str):
        """One stat for one player, or "unknown". Zero only when the player is confirmed to have played."""
        if not self.final() or not known(gsis_id) or stat not in self.STATS:
            return UNKNOWN
        if not self._played(gsis_id, full_name, team):
            return UNKNOWN
        p = self.pbp
        n = lambda c: p[c].fillna(0) if c in p else 0
        two = n("two_point_attempt") == 1
        if stat in ("receiving_yards", "receptions", "targets"):
            x = p[(p.receiver_player_id == gsis_id) & (n("pass_attempt") == 1) & (n("sack") == 0) & ~two]
            if stat == "targets":
                return int(len(x))
            if stat == "receptions":
                return int((x.complete_pass.fillna(0) == 1).sum())
            return int(x.receiving_yards.fillna(0).sum())
        if stat in ("rushing_yards", "carries", "rush_attempts"):
            x = p[(p.rusher_player_id == gsis_id) & (n("rush_attempt") == 1) & ~two]
            return int(len(x)) if stat in ("carries", "rush_attempts") else int(x.rushing_yards.fillna(0).sum())
        x = p[(p.passer_player_id == gsis_id) & (n("pass_attempt") == 1) & (n("sack") == 0) & ~two]
        if stat == "pass_attempts":
            return int(len(x))
        if stat == "completions":
            return int((x.complete_pass.fillna(0) == 1).sum())
        return int(x.passing_yards.fillna(0).sum())


def load_actuals(game_id: str, season: int, cache: Path, *, offline: bool = False, fetch=_get) -> Actuals:
    import pandas as pd
    prov = fetch_nflverse(season, cache, offline=offline, fetch=fetch)
    read = lambda k, cols=None: pd.read_parquet(prov[k]["path"], columns=cols) if prov[k]["path"] else None
    games = read("games")
    if games is None:
        raise SystemExit("grading: nflverse games file unavailable; nothing graded")
    pbp_cols = ["game_id", "play_type", "pass_attempt", "rush_attempt", "sack", "complete_pass", "two_point_attempt",
                "passer_player_id", "rusher_player_id", "receiver_player_id", "passing_yards", "rushing_yards", "receiving_yards"]
    pbp = read("pbp", pbp_cols)
    rosters = read("rosters")
    snaps = read("snap_counts")
    return Actuals(game_id, games, pbp, rosters, snaps, prov)
