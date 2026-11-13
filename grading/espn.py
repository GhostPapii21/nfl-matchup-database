"""ESPN public box score as a fallback actual-results source for the grading loop.

nflverse posts final play-by-play the morning after a game. ESPN's public summary API has the official box score
minutes after the final whistle, so the loop can grade the same night:

    python -m grading.grade --game 2026_10_WAS_NYG --actuals espn --write

The raw response is saved under grading/results/sources/ (header + boxscore, plus the sha256 of the full response
and the pull time), so a grade can be re-run offline and audited later (`--offline`).

Interface matches sources.Actuals (final, score, src, resolve_full, resolve_short, stat, prov). Player ids are
ESPN athlete ids prefixed "espn:". ESPN lists only players who recorded a stat, so a player missing from the box is
"unknown" (could be a did-not-play), never 0. Free public endpoint; no key, no paid call.
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from .core import UNKNOWN, known, parse_utc
from .sources import ROOT, UA, abbrev, norm, short_key

SUMMARY = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={event}"
SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={season}&seasontype=2&week={week}"
ALIAS = {"WSH": "WAS", "LAR": "LA"}
SOURCES_DIR = ROOT / "grading" / "results" / "sources"


def team(abbr: str) -> str:
    return ALIAS.get(abbr, abbr)


def _get(url: str, timeout: int = 60) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read()


def find_event(game_id: str, fetch=_get) -> str | None:
    """ESPN event id for an nflverse game id (season_week_AWAY_HOME) from the public weekly scoreboard."""
    season, week, away, home = game_id.split("_")
    data = json.loads(fetch(SCOREBOARD.format(season=season, week=int(week))))
    for ev in data.get("events") or []:
        comp = (ev.get("competitions") or [{}])[0]
        sides = {c.get("homeAway"): team((c.get("team") or {}).get("abbreviation", "")) for c in comp.get("competitors") or []}
        if sides.get("home") == home and sides.get("away") == away:
            return str(ev.get("id"))
    return None


def saved_path(game_id: str, event: str, root: Path = SOURCES_DIR) -> Path:
    return root / f"espn_summary_{game_id}_{event}.json"


def fetch_summary(game_id: str, event: str, *, offline: bool = False, fetch=_get, root: Path = SOURCES_DIR) -> dict:
    """Pull (or reuse the saved copy of) the ESPN summary. Returns the saved record {url, retrieved_utc, sha256_full_response, header, boxscore}."""
    p = saved_path(game_id, event, root)
    if offline:
        if not p.exists():
            raise SystemExit(f"grading: --offline and no saved ESPN summary at {p}; nothing graded")
        return json.loads(p.read_text())
    url = SUMMARY.format(event=event)
    raw = fetch(url)
    d = json.loads(raw)
    rec = {"schema": "grading.espn_summary.v1", "game_id": game_id, "event": event, "url": url,
           "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "sha256_full_response": hashlib.sha256(raw).hexdigest(), "bytes_full_response": len(raw),
           "note": "header + boxscore kept from the full public response; nothing edited",
           "header": d.get("header"), "boxscore": d.get("boxscore")}
    root.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")
    return rec


class ESPNActuals:
    STATS = ("receiving_yards", "receptions", "targets", "rushing_yards", "carries", "rush_attempts",
             "passing_yards", "pass_attempts", "completions")

    def __init__(self, game_id: str, rec: dict, saved_rel: str):
        self.game_id, self.rec = game_id, rec
        comp = ((rec.get("header") or {}).get("competitions") or [{}])[0]
        self.comp = comp
        self.status = ((comp.get("status") or {}).get("type") or {})
        self.teams = {}
        for c in comp.get("competitors") or []:
            t = team((c.get("team") or {}).get("abbreviation", ""))
            self.teams[t] = {"homeAway": c.get("homeAway"), "score": c.get("score"),
                             "linescores": [x.get("displayValue") for x in c.get("linescores") or []]}
        self.home = next((t for t, v in self.teams.items() if v["homeAway"] == "home"), None)
        self.away = next((t for t, v in self.teams.items() if v["homeAway"] == "away"), None)
        self.kickoff = parse_utc(comp.get("date"))
        self.games_df = None
        label = f"{rec.get('url')} saved {saved_rel} sha256_full_response={rec.get('sha256_full_response')}"
        self._src = (label, rec.get("retrieved_utc", UNKNOWN))
        self.prov = {"espn_summary": {"url": rec.get("url"), "sha256": rec.get("sha256_full_response"),
                                      "retrieved_utc": rec.get("retrieved_utc", UNKNOWN), "status": self.status.get("name", UNKNOWN),
                                      "saved": saved_rel}}
        # players[espn_id] = {name, team, stats{...}}
        self.players: dict[str, dict] = {}
        for tb in (rec.get("boxscore") or {}).get("players") or []:
            t = team((tb.get("team") or {}).get("abbreviation", ""))
            for grp in tb.get("statistics") or []:
                labels = grp.get("labels") or []
                for a in grp.get("athletes") or []:
                    ath = a.get("athlete") or {}
                    pid = f"espn:{ath.get('id')}"
                    pl = self.players.setdefault(pid, {"name": ath.get("displayName"), "team": t, "stats": {}})
                    vals = dict(zip(labels, a.get("stats") or []))
                    self._parse(grp.get("name"), vals, pl["stats"])

    @staticmethod
    def _int(x):
        try:
            return int(str(x).strip())
        except (TypeError, ValueError):
            return UNKNOWN

    def _parse(self, group, v, out):
        if group == "passing" and "C/ATT" in v:
            c, _, a = str(v["C/ATT"]).partition("/")
            out.update(completions=self._int(c), pass_attempts=self._int(a), passing_yards=self._int(v.get("YDS")))
        elif group == "rushing":
            out.update(carries=self._int(v.get("CAR")), rush_attempts=self._int(v.get("CAR")), rushing_yards=self._int(v.get("YDS")))
        elif group == "receiving":
            out.update(receptions=self._int(v.get("REC")), receiving_yards=self._int(v.get("YDS")), targets=self._int(v.get("TGTS")))
        elif group in ("passing", "rushing", "receiving", "fumbles", "defensive", "interceptions", "kickReturns",
                       "puntReturns", "kicking", "punting"):
            out.setdefault("_appeared", True)

    def src(self, name):
        return self._src

    def final(self) -> bool:
        return bool(self.status.get("completed")) and self.status.get("name") == "STATUS_FINAL" and \
            all(known(self._int(v["score"])) for v in self.teams.values()) and len(self.teams) == 2

    def score(self, t: str):
        if not self.final() or t not in self.teams:
            return UNKNOWN
        return self._int(self.teams[t]["score"])

    def half_score(self, t: str, half: int):
        """Points in half 1 or 2 (sum of ESPN quarter line scores), or unknown."""
        ls = (self.teams.get(t) or {}).get("linescores") or []
        if not self.final() or len(ls) < 4:
            return UNKNOWN
        q = [self._int(x) for x in ls[:4]]
        if not all(known(x) for x in q):
            return UNKNOWN
        return q[0] + q[1] if half == 1 else q[2] + q[3]

    def _match(self, pred, what):
        m = [(pid, p) for pid, p in self.players.items() if pred(p)]
        if len(m) != 1:
            return {"gsis_id": UNKNOWN, "team": UNKNOWN, "reason": f"{len(m)} ESPN box-score matches for {what}"}
        pid, p = m[0]
        return {"gsis_id": pid, "team": p["team"], "full_name": p["name"], "reason": ""}

    def resolve_full(self, full_name: str, team_: str | None = None) -> dict:
        return self._match(lambda p: norm(p["name"]) == norm(full_name) and (not team_ or p["team"] == team_),
                           f"'{full_name}' {team_ or ''}".strip())

    def resolve_short(self, short_name: str, team_: str) -> dict:
        return self._match(lambda p: p["team"] == team_ and abbrev(p["name"]) == short_key(short_name),
                           f"'{short_name}' on {team_}")

    def resolve_surname(self, surname: str, team_: str | None = None, initial: str | None = None) -> dict:
        """Research-run leg names use a surname (optionally 'A.Williams'). Exactly one box-score player or unknown."""
        def ok(p):
            toks = [t for t in p["name"].replace("'", "").split() if t.lower().strip(".") not in ("jr", "sr", "ii", "iii", "iv", "v")]
            return (norm(toks[-1]) == norm(surname) and (not team_ or p["team"] == team_)
                    and (not initial or toks[0][:1].lower() == initial.lower()))
        return self._match(ok, f"surname '{surname}'" + (f" initial {initial}" if initial else ""))

    def stat(self, gsis_id, full_name, team_, stat: str):
        """Box-score stat. A player in the box but without that stat group recorded 0 only for groups ESPN
        always lists when any attempt happened (they did not get one); if the player is absent, unknown."""
        if not self.final() or not known(gsis_id) or stat not in self.STATS:
            return UNKNOWN
        p = self.players.get(gsis_id)
        if p is None:
            return UNKNOWN
        v = p["stats"].get(stat)
        if v is None:
            # In the box (played) but no line in this stat group: ESPN omits zero-attempt groups.
            return 0
        return v


def load(game_id: str, event: str | None = None, *, offline: bool = False, fetch=_get, root: Path = SOURCES_DIR) -> ESPNActuals:
    if event is None:
        saved = sorted(root.glob(f"espn_summary_{game_id}_*.json")) if offline else []
        if saved:
            event = saved[-1].stem.rsplit("_", 1)[-1]
        else:
            event = find_event(game_id, fetch=fetch)
        if event is None:
            raise SystemExit(f"grading: no ESPN event found for {game_id}; nothing graded")
    rec = fetch_summary(game_id, event, offline=offline, fetch=fetch, root=root)
    p = saved_path(game_id, event, root)
    try:
        rel = str(p.relative_to(ROOT))
    except ValueError:
        rel = str(p)
    return ESPNActuals(game_id, rec, rel)
