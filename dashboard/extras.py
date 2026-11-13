"""Extra game-board sections computed from public nflverse data, on top of each pregame packet.

Every function returns plain JSON-safe dicts and labels its sample. Nothing here prices or recommends a bet.
Sections: schedule and travel context, head-to-head history with a breakdown of the last meeting, quarterback
against the blitz / pressure / man and zone, defensive coverage profile, defenders with their positions,
receiver and running-back roles, players working back from injury, injury impact, and a weather verdict.
"""
from __future__ import annotations

import math
import urllib.parse
from pathlib import Path

import pandas as pd

NFLVERSE = "https://github.com/nflverse/nflverse-data/releases/download"
EXTRA_DATASETS = {
    "pbp": "pbp/play_by_play_{season}.parquet",
    "ftn": "ftn_charting/ftn_charting_{season}.parquet",
    "snaps": "snap_counts/snap_counts_{season}.parquet",
    "rosters": "weekly_rosters/roster_weekly_{season}.parquet",
    "pfr_pass": "pfr_advstats/advstats_week_pass_{season}.parquet",
    "pfr_def": "pfr_advstats/advstats_week_def_{season}.parquet",
    "participation": "pbp_participation/pbp_participation_{season}.parquet",
    "games": "schedules/games.parquet",
    "combine": "combine/combine.parquet",
}

TEAM_NAMES = {
    "ARI": "Arizona Cardinals", "ATL": "Atlanta Falcons", "BAL": "Baltimore Ravens", "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers", "CHI": "Chicago Bears", "CIN": "Cincinnati Bengals", "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys", "DEN": "Denver Broncos", "DET": "Detroit Lions", "GB": "Green Bay Packers",
    "HOU": "Houston Texans", "IND": "Indianapolis Colts", "JAX": "Jacksonville Jaguars", "KC": "Kansas City Chiefs",
    "LV": "Las Vegas Raiders", "LAC": "Los Angeles Chargers", "LA": "Los Angeles Rams", "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings", "NE": "New England Patriots", "NO": "New Orleans Saints", "NYG": "New York Giants",
    "NYJ": "New York Jets", "PHI": "Philadelphia Eagles", "PIT": "Pittsburgh Steelers", "SF": "San Francisco 49ers",
    "SEA": "Seattle Seahawks", "TB": "Tampa Bay Buccaneers", "TEN": "Tennessee Titans", "WAS": "Washington Commanders",
}
# Home time zone as hours behind Eastern.
TZ_BEHIND_ET = {t: 0 for t in TEAM_NAMES}
TZ_BEHIND_ET.update({t: 1 for t in ("CHI", "DAL", "GB", "HOU", "KC", "MIN", "NO", "TEN")})
TZ_BEHIND_ET.update({t: 2 for t in ("DEN", "ARI")})
TZ_BEHIND_ET.update({t: 3 for t in ("LV", "LAC", "LA", "SF", "SEA")})
TZ_LABEL = {0: "Eastern", 1: "Central", 2: "Mountain", 3: "Pacific"}

DB_POS = {"CB", "S", "FS", "SS", "SAF", "LB", "ILB", "OLB", "MLB", "DB", "NB"}


# ----------------------------------------------------------------------------------------------- data loading
class Data:
    """Lazy loader for nflverse files, cached on disk. Missing files are recorded, never filled in."""

    def __init__(self, cache: Path, *, offline: bool = False, fetch=None):
        self.cache = Path(cache)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.offline = offline
        self.fetch = fetch
        self._frames: dict = {}
        self.missing: dict = {}

    def get(self, kind: str, season: int | None = None):
        key = (kind, season)
        if key in self._frames:
            return self._frames[key]
        rel = EXTRA_DATASETS[kind].format(season=season)
        path = self.cache / Path(rel).name
        df = None
        if not path.exists() and not self.offline and self.fetch is not None:
            try:
                path.write_bytes(self.fetch(f"{NFLVERSE}/{rel}"))
            except Exception as e:  # noqa: BLE001 - a missing file is a recorded gap
                self.missing[f"{kind}_{season}"] = f"{type(e).__name__}: {e}"[:160]
        if path.exists():
            try:
                df = pd.read_parquet(path)
            except Exception as e:  # noqa: BLE001
                self.missing[f"{kind}_{season}"] = f"unreadable: {e}"[:160]
        elif f"{kind}_{season}" not in self.missing:
            self.missing[f"{kind}_{season}"] = "not downloaded"
        self._frames[key] = df
        return df


def _f(x, nd=3):
    if x is None:
        return None
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return round(x, nd)


def _div(a, b):
    return a / b if b else None


# ----------------------------------------------------------------------------------------------- schedule and travel
def schedule_context(games: pd.DataFrame, g, packet: dict) -> dict:
    """Rest, short week, bye, last game abroad, time-zone travel and body-clock flags for both teams."""
    out = {}
    season = int(g["season"])
    gday = str(g["gameday"])
    this_neutral = str(g.get("location")) == "Neutral"
    for side, team, opp in (("away", g["away_team"], g["home_team"]), ("home", g["home_team"], g["away_team"])):
        rest = packet["game"].get(f"{side}_rest_days")
        prev = games[(games.season == season) & (games.gameday < gday) &
                     ((games.home_team == team) | (games.away_team == team))].sort_values("gameday")
        flags = []
        last = None
        if len(prev):
            p = prev.iloc[-1]
            was_home = p.home_team == team
            last = {"week": int(p.week), "date": str(p.gameday), "weekday": str(p.weekday),
                    "opponent": p.away_team if was_home else p.home_team, "site": "home" if was_home else "away",
                    "stadium": str(p.stadium), "neutral": str(p.location) == "Neutral",
                    "score": f"{int(p.away_score)}-{int(p.home_score)}" if pd.notna(p.home_score) else None}
            if last["neutral"]:
                flags.append({"level": "warn", "text": f"Coming off an international game ({p.stadium}, week {int(p.week)})"})
            if str(p.weekday) == "Monday":
                flags.append({"level": "info", "text": "Played last Monday night"})
        if rest is not None:
            if rest <= 4:
                flags.append({"level": "warn", "text": f"Short week: {rest} days of rest"})
            elif rest == 5:
                flags.append({"level": "warn", "text": "Short week: 5 days of rest"})
            elif rest >= 13:
                flags.append({"level": "good", "text": f"Coming off a bye ({rest} days of rest)"})
        # Travel: time zones crossed to the venue.
        venue_tz = TZ_BEHIND_ET.get(g["home_team"], 0)
        team_tz = TZ_BEHIND_ET.get(team, 0)
        if this_neutral:
            flags.append({"level": "warn", "text": f"International / neutral-site game: {g.get('stadium')}"})
        elif side == "away":
            crossed = abs(team_tz - venue_tz)
            if crossed >= 2:
                flags.append({"level": "warn", "text": f"Travels {crossed} time zones ({TZ_LABEL[team_tz]} to {TZ_LABEL[venue_tz]})"})
            kick = packet["game"].get("kickoff_et") or ""
            if team_tz == 3 and kick[:2] in ("12", "13"):
                flags.append({"level": "warn", "text": "West-coast team in a 1:00 PM ET start (10:00 AM body clock)"})
        out[team] = {"rest_days": rest, "last_game": last, "flags": flags}
    return out


# ----------------------------------------------------------------------------------------------- head to head
def _team_box(pl: pd.DataFrame, team: str) -> dict:
    o = pl[pl.posteam == team]
    d = pl[pl.defteam == team]
    third_att = int(((o.down == 3) & o.play_type.isin(["pass", "run"])).sum())
    third_conv = int(o.third_down_converted.fillna(0).sum())
    rz_drives = o[o.yardline_100 <= 20].fixed_drive.nunique()
    rz_td = o[(o.yardline_100 <= 20) & (o.touchdown == 1) & (o.td_team == team)].fixed_drive.nunique()
    return {
        "pass_yards": int(o.passing_yards.fillna(0).sum()),
        "rush_yards": int(o.rushing_yards.fillna(0).sum()),
        "plays": int(o.play_type.isin(["pass", "run"]).sum()),
        "turnovers": int(o.interception.fillna(0).sum() + o.fumble_lost.fillna(0).sum()),
        "sacks_taken": int(o.sack.fillna(0).sum()),
        "sacks_made": int(d.sack.fillna(0).sum()),
        "third_down": f"{third_conv}/{third_att}",
        "red_zone": f"{rz_td}/{rz_drives} TD",
        "explosive": int(((o.play_type == "pass") & (o.yards_gained >= 20)).sum() + ((o.play_type == "run") & (o.yards_gained >= 15)).sum()),
    }


def _leaders(pl: pd.DataFrame, team: str) -> dict:
    o = pl[pl.posteam == team]
    o = o.assign(att_ns=((o.pass_attempt.fillna(0) == 1) & (o.sack.fillna(0) == 0)).astype(int))
    pas = o[o.passer_player_name.notna() & (o.two_point_attempt != 1)].groupby(["passer_player_id", "passer_player_name"]).agg(
        att=("att_ns", "sum"), cmp=("complete_pass", "sum"), yds=("passing_yards", "sum"),
        td=("pass_touchdown", "sum"), int_=("interception", "sum"), sacks=("sack", "sum")).reset_index().sort_values("att", ascending=False)
    rus = o[o.rusher_player_name.notna() & (o.two_point_attempt != 1)].groupby(["rusher_player_id", "rusher_player_name"]).agg(
        car=("rush_attempt", "sum"), yds=("rushing_yards", "sum"), td=("touchdown", "sum")).reset_index().sort_values("yds", ascending=False)
    rec = o[o.receiver_player_name.notna() & (o.two_point_attempt != 1)].groupby(["receiver_player_id", "receiver_player_name"]).agg(
        tgt=("att_ns", "sum"), rec=("complete_pass", "sum"), yds=("receiving_yards", "sum"), td=("pass_touchdown", "sum")).reset_index().sort_values("yds", ascending=False)
    return {
        "passing": [{"id": r.passer_player_id, "player": r.passer_player_name, "line": f"{int(r.cmp)}/{int(r.att)}, {int(r.yds)} yds, {int(r.td)} TD, {int(r.int_)} INT",
                     "yards": int(r.yds)} for r in pas.head(1).itertuples()],
        "rushing": [{"id": r.rusher_player_id, "player": r.rusher_player_name, "line": f"{int(r.car)} car, {int(r.yds)} yds, {int(r.td)} TD",
                     "yards": int(r.yds)} for r in rus.head(2).itertuples()],
        "receiving": [{"id": r.receiver_player_id, "player": r.receiver_player_name, "line": f"{int(r.rec)}-{int(r.yds)} on {int(r.tgt)} tgt, {int(r.td)} TD",
                       "yards": int(r.yds)} for r in rec.head(4).itertuples()],
    }


def _quarters(pl: pd.DataFrame, home: str, away: str) -> dict:
    q = pl.groupby("qtr").agg(h=("total_home_score", "max"), a=("total_away_score", "max")).sort_index()
    hs, as_, ph, pa = [], [], 0, 0
    for qtr, r in q.iterrows():
        h, a = int(r.h if pd.notna(r.h) else ph), int(r.a if pd.notna(r.a) else pa)
        hs.append(h - ph); as_.append(a - pa); ph, pa = h, a
    labels = ["Q1", "Q2", "Q3", "Q4"] + ["OT"] * max(0, len(hs) - 4)
    return {"labels": labels[:len(hs)], home: hs, away: as_}


def head_to_head(games: pd.DataFrame, data: Data, g, packet: dict, roster_now: pd.DataFrame | None) -> dict:
    a, h = g["away_team"], g["home_team"]
    m = games[(((games.home_team == h) & (games.away_team == a)) | ((games.home_team == a) & (games.away_team == h)))
              & games.home_score.notna() & (games.gameday < str(g["gameday"]))].sort_values("gameday", ascending=False)
    meetings = []
    for r in m.head(8).itertuples():
        winner = r.home_team if r.home_score > r.away_score else (r.away_team if r.away_score > r.home_score else "TIE")
        cover = None
        if pd.notna(r.spread_line):   # nflverse spread_line: home favoured by this many points
            margin = r.home_score - r.away_score
            cover = r.home_team if margin > r.spread_line else (r.away_team if margin < r.spread_line else "PUSH")
        meetings.append({"game_id": r.game_id, "season": int(r.season), "week": int(r.week), "date": str(r.gameday),
                         "game_type": str(r.game_type), "away": r.away_team, "home": r.home_team,
                         "score": f"{r.away_team} {int(r.away_score)}, {r.home_team} {int(r.home_score)}",
                         "winner": winner, "total": int(r.away_score + r.home_score),
                         "closing_spread_home": _f(r.spread_line, 1), "closing_total": _f(r.total_line, 1), "covered": cover,
                         "over_under": (None if pd.isna(r.total_line) else ("Over" if r.away_score + r.home_score > r.total_line
                                                                            else "Under" if r.away_score + r.home_score < r.total_line else "Push"))})
    out = {"meetings": meetings, "last": None}
    if meetings:
        s = meetings[:6]
        out["record"] = {t: sum(1 for x in s if x["winner"] == t) for t in (a, h)}
        out["record_note"] = f"last {len(s)} meetings"
    if not len(m):
        return out
    last = m.iloc[0]
    yr = int(last.season)
    pbp = data.get("pbp", yr)
    q = f"{TEAM_NAMES.get(last.away_team, last.away_team)} vs {TEAM_NAMES.get(last.home_team, last.home_team)} highlights week {int(last.week)} {yr}"
    lastd = {"game_id": last.game_id, "season": yr, "week": int(last.week), "date": str(last.gameday),
             "away": last.away_team, "home": last.home_team,
             "score": f"{last.away_team} {int(last.away_score)}, {last.home_team} {int(last.home_score)}",
             "stadium": str(last.stadium), "roof": str(last.roof),
             "coaches": {last.away_team: str(last.away_coach), last.home_team: str(last.home_coach)},
             "highlights_url": "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q),
             "highlights_search": q}
    if pbp is None:
        lastd["breakdown_status"] = f"MISSING: play-by-play for {yr} not available"
        out["last"] = lastd
        return out
    pl = pbp[(pbp.game_id == last.game_id)]
    lastd["box"] = {t: _team_box(pl, t) for t in (last.away_team, last.home_team)}
    lastd["leaders"] = {t: _leaders(pl, t) for t in (last.away_team, last.home_team)}
    lastd["quarters"] = _quarters(pl, last.home_team, last.away_team)
    lastd["carryover"] = _carryover(lastd, packet, roster_now)
    out["last"] = lastd
    return out


def _carryover(lastd: dict, packet: dict, roster_now: pd.DataFrame | None) -> list[dict]:
    """Rules-based notes on what from the last meeting still applies now."""
    notes = []
    now_qb = packet["game"].get("listed_qbs", {})
    now_coach = packet["game"].get("coaches", {})
    ids_now = {}
    if roster_now is not None and len(roster_now):
        latest = roster_now[roster_now.week == roster_now.week.max()]
        ids_now = dict(zip(latest.gsis_id, latest.team))
    for team, L in lastd["leaders"].items():
        qb = (L["passing"] or [{}])[0]
        cur = now_qb.get(team)
        if qb.get("player"):
            same = _same_player(qb["player"], cur)
            notes.append({"team": team, "kind": "qb", "level": "info" if same else "warn",
                          "text": (f"Same QB as last meeting ({qb['player']}: {qb['line']})" if same
                                   else f"Different QB: {qb['player']} started last time ({qb['line']}); listed now: {cur or 'unknown'}")})
        if lastd["coaches"].get(team) and now_coach.get(team) and lastd["coaches"][team] != now_coach[team]:
            notes.append({"team": team, "kind": "coach", "level": "warn",
                          "text": f"Coaching change since then: {lastd['coaches'][team]} then, {now_coach[team]} now"})
        for grp in ("receiving", "rushing"):
            for p in L[grp]:
                if p["yards"] < (50 if grp == "receiving" else 40):
                    continue
                where = ids_now.get(p["id"])
                if where == team:
                    notes.append({"team": team, "kind": "player", "level": "good", "text": f"{p['player']} ({p['line']}) is still on {team}"})
                elif where:
                    notes.append({"team": team, "kind": "player", "level": "warn", "text": f"{p['player']} ({p['line']}) is now on {where}"})
                elif ids_now:
                    notes.append({"team": team, "kind": "player", "level": "warn", "text": f"{p['player']} ({p['line']}) is not on a current active roster"})
    return notes


def _same_player(a: str | None, b: str | None) -> bool:
    if not a or not b:
        return False
    a, b = a.replace(".", " ").split(), b.replace(".", " ").split()
    return a[-1].lower() == b[-1].lower() and a[0][0].lower() == b[0][0].lower()


# ----------------------------------------------------------------------------------------------- quarterback
def _pass_line(df: pd.DataFrame) -> dict | None:
    if not len(df):
        return None
    sk = int(df.sack.fillna(0).sum())
    att = int(((df.pass_attempt.fillna(0) == 1) & (df.sack.fillna(0) == 0)).sum())   # nflverse counts sacks as pass attempts
    db = int(len(df))
    return {"dropbacks": db, "attempts": att, "completion_pct": _f(_div(df.complete_pass.fillna(0).sum(), att)),
            "yards_per_attempt": _f(_div(df.passing_yards.fillna(0).sum(), att), 2), "td": int(df.pass_touchdown.fillna(0).sum()),
            "int": int(df.interception.fillna(0).sum()), "sack_rate": _f(_div(sk, db)),
            "epa_per_dropback": _f(df.epa.mean(), 3)}


def qb_profile(data: Data, season: int, team: str, qb_name: str | None, weeks: list[int]) -> dict:
    """The listed QB this season (blitz from FTN charting, pressure from PFR) and last season (man/zone and pressure from NGS participation)."""
    out = {"player": qb_name, "this_season": None, "last_season": None, "notes": []}
    pbp = data.get("pbp", season)
    if pbp is None or not qb_name:
        out["notes"].append("No play-by-play or no listed QB.")
        return out
    db = pbp[(pbp.qb_dropback == 1) & (pbp.posteam == team) & pbp.week.isin(weeks) & (pbp.two_point_attempt != 1)]
    ids = db[db.passer_player_name.fillna("").map(lambda n: _same_player(n, qb_name))].passer_player_id.dropna()
    qb_id = ids.mode().iloc[0] if len(ids) else None
    if qb_id is None:
        out["notes"].append(f"{qb_name} has no dropbacks for {team} in this window (new starter or name mismatch).")
        # fall back to his league-wide dropbacks this season
        alldb = pbp[(pbp.qb_dropback == 1) & (pbp.two_point_attempt != 1)]
        ids = alldb[alldb.passer_player_name.fillna("").map(lambda n: _same_player(n, qb_name))].passer_player_id.dropna()
        qb_id = ids.mode().iloc[0] if len(ids) else None
        if qb_id is None:
            return out
        db = alldb
    mine = db[db.passer_player_id == qb_id]
    out["player_id"] = qb_id
    cur = {"all": _pass_line(mine)}
    ftn = data.get("ftn", season)
    if ftn is not None and len(mine):
        j = mine.merge(ftn[["nflverse_game_id", "nflverse_play_id", "n_blitzers", "n_pass_rushers", "is_play_action", "is_qb_out_of_pocket"]],
                       left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "nflverse_play_id"], how="inner")
        if len(j):
            cur["vs_blitz"] = _pass_line(j[j.n_blitzers.fillna(0) >= 1])
            cur["no_blitz"] = _pass_line(j[j.n_blitzers.fillna(0) == 0])
            cur["blitzed_rate"] = _f(_div((j.n_blitzers.fillna(0) >= 1).sum(), len(j)))
            cur["play_action"] = _pass_line(j[j.is_play_action == True])  # noqa: E712
            cur["out_of_pocket"] = _pass_line(j[j.is_qb_out_of_pocket == True])  # noqa: E712
            cur["charted_dropbacks"] = int(len(j))
    pfr = data.get("pfr_pass", season)
    if pfr is not None:
        last = qb_name.replace(".", " ").split()[-1].lower()
        first = qb_name.strip()[0].lower()
        named = pfr[pfr.pfr_player_name.fillna("").str.lower().str.endswith(last) & pfr.pfr_player_name.fillna("").str.lower().str.startswith(first)]
        pr = named[(named.team == team) & named.week.isin(weeks)]
        if not len(pr):   # traded or newly signed: use his games for any team this season
            pr = named
        if len(pr):
            pressured = pr.times_pressured.fillna(0).sum()
            cur["pressured"] = {"times_pressured": int(pressured), "pressure_rate": _f(_div(pressured, len(mine))),
                                "times_blitzed": int(pr.times_blitzed.fillna(0).sum()), "bad_throw_pct": _f(pr.passing_bad_throw_pct.mean())}
    rz = mine[mine.yardline_100 <= 20]
    cur["red_zone"] = {"attempts": int(rz.pass_attempt.fillna(0).sum()), "td": int(rz.pass_touchdown.fillna(0).sum()),
                       "int": int(rz.interception.fillna(0).sum())}
    third = mine[mine.down == 3]
    cur["third_down"] = {"dropbacks": int(len(third)), "conversion_rate": _f(_div(third.third_down_converted.fillna(0).sum(), len(third)))}
    out["this_season"] = cur
    # Last season: NGS participation (man/zone, coverage shell, pressure).
    prev = season - 1
    pp, pb = data.get("participation", prev), data.get("pbp", prev)
    if pp is not None and pb is not None:
        pm = pb[(pb.qb_dropback == 1) & (pb.passer_player_id == qb_id) & (pb.season_type == "REG") & (pb.two_point_attempt != 1)]
        j = pm.merge(pp[["nflverse_game_id", "play_id", "defense_man_zone_type", "defense_coverage_type", "was_pressure", "time_to_throw"]],
                     left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "play_id"], how="inner")
        if len(j):
            ls = {"season": prev, "teams": sorted(set(pm.posteam.dropna())), "all": _pass_line(j),
                  "vs_man": _pass_line(j[j.defense_man_zone_type == "MAN_COVERAGE"]),
                  "vs_zone": _pass_line(j[j.defense_man_zone_type == "ZONE_COVERAGE"]),
                  "pressured": _pass_line(j[j.was_pressure == True]),  # noqa: E712
                  "clean": _pass_line(j[j.was_pressure == False]),  # noqa: E712
                  "pressure_rate": _f(_div((j.was_pressure == True).sum(), j.was_pressure.notna().sum())),  # noqa: E712
                  "avg_time_to_throw": _f(j.time_to_throw.mean(), 2)}
            out["last_season"] = ls
        else:
            out["notes"].append(f"No {prev} dropbacks with coverage data for this QB.")
    else:
        out["notes"].append(f"Man/zone data for {prev} not available.")
    out["notes"].append(f"Man/zone and coverage shells are not published for {season}; the latest free season is {prev}.")
    return out


# ----------------------------------------------------------------------------------------------- defense profile
def coverage_profile(data: Data, season: int, team: str) -> dict | None:
    """Last season's man/zone mix, top shells and pressure for this defense (NGS participation)."""
    prev = season - 1
    pp, pb = data.get("participation", prev), data.get("pbp", prev)
    if pp is None or pb is None:
        return None
    d = pb[(pb.defteam == team) & (pb.qb_dropback == 1) & (pb.season_type == "REG")]
    j = d.merge(pp[["nflverse_game_id", "play_id", "defense_man_zone_type", "defense_coverage_type", "was_pressure", "number_of_pass_rushers"]],
                left_on=["game_id", "play_id"], right_on=["nflverse_game_id", "play_id"], how="inner")
    j = j[j.defense_man_zone_type.isin(["MAN_COVERAGE", "ZONE_COVERAGE"])]
    if not len(j):
        return None
    shells = j.defense_coverage_type.value_counts(normalize=True).head(4)
    man = j[j.defense_man_zone_type == "MAN_COVERAGE"]
    zone = j[j.defense_man_zone_type == "ZONE_COVERAGE"]
    return {"season": prev, "dropbacks": int(len(j)), "man_rate": _f(len(man) / len(j)), "zone_rate": _f(len(zone) / len(j)),
            "shells": [{"shell": k.replace("_", " ").title(), "rate": _f(v)} for k, v in shells.items()],
            "pressure_rate": _f(_div((j.was_pressure == True).sum(), j.was_pressure.notna().sum())),  # noqa: E712
            "five_plus_rushers_rate": _f(_div((j.number_of_pass_rushers.fillna(0) >= 5).sum(), len(j))),
            "allowed_vs_man": _pass_line(man), "allowed_vs_zone": _pass_line(zone),
            "note": f"{prev} season (latest with free man/zone data). Coordinator or roster changes since then make it context, not current fact."}


def defenders_with_positions(packet_def: dict, rosters: pd.DataFrame | None, team: str, pfr_def: pd.DataFrame | None, weeks) -> dict:
    """Coverage defenders with their roster position and a 'target this player' grade against league rates."""
    pos = {}
    if rosters is not None and len(rosters):
        r = rosters[rosters.team == team].sort_values("week")
        for x in r.itertuples():
            pos[str(x.full_name)] = str(x.depth_chart_position or x.position or "")
    league = {}
    if pfr_def is not None and len(pfr_def):
        z = pfr_def[pfr_def.def_targets.fillna(0) > 0]
        t = z.def_targets.sum()
        league = {"yards_per_target": _f(z.def_yards_allowed.sum() / t, 2), "completion_pct": _f(z.def_completions_allowed.sum() / t),
                  "td_per_target": _f(z.def_receiving_td_allowed.sum() / t, 4)}
    cov = []
    for c in packet_def.get("coverage", []) or []:
        p = pos.get(c["player"], "")
        grp = "CB" if p in ("CB", "NB", "DB") else "S" if p in ("S", "FS", "SS", "SAF") else "LB" if "LB" in p else (p or "?")
        cmp_pct = _div(c.get("completions") or 0, c.get("targets") or 0)
        score, why = 0, []
        ypt = c.get("yards_per_target")
        if c.get("targets", 0) >= 12:
            if league and ypt and ypt >= league["yards_per_target"] * 1.15:
                score += 2; why.append(f"{ypt:.1f} yds/target (league {league['yards_per_target']:.1f})")
            if league and cmp_pct and cmp_pct >= league["completion_pct"] + 0.08:
                score += 1; why.append(f"{cmp_pct:.0%} completions allowed")
            if (c.get("td_allowed") or 0) >= 3:
                score += 2; why.append(f"{c['td_allowed']} TDs allowed")
            if (c.get("missed_tackles") or 0) >= 6:
                score += 1; why.append(f"{c['missed_tackles']} missed tackles")
            if (c.get("interceptions") or 0) >= 3:
                score -= 2; why.append(f"{c['interceptions']} INTs: ball hawk")
            if league and ypt and ypt <= league["yards_per_target"] * 0.8:
                score -= 1; why.append(f"only {ypt:.1f} yds/target")
        grade = "target" if score >= 2 else "avoid" if score <= -1 else "neutral" if c.get("targets", 0) >= 12 else "small sample"
        cov.append(dict(c, position=grp, raw_position=p, completion_pct=_f(cmp_pct), grade=grade, why=why))
    return {"coverage": cov, "pass_rush": packet_def.get("pass_rush", []), "league": league, "weeks": weeks}


# ----------------------------------------------------------------------------------------------- roles
def _cv(vals):
    vals = [v for v in vals if v is not None]
    if len(vals) < 3:
        return None
    m = sum(vals) / len(vals)
    if m <= 0:
        return None
    sd = (sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5
    return sd / m


def receiver_roles(players: dict, snap_share: dict, id_to_name: dict) -> dict:
    rec = [dict(r) for r in players.get("receivers", []) if r.get("targets")]
    rush = [dict(r) for r in players.get("rushers", []) if r.get("carries")]
    for r in rec:
        log = r.get("log", [])
        r["full_name"] = id_to_name.get(r.get("player_id"), r["player"])
        r["snap_share"] = snap_share.get(r["full_name"])
        r["targets_pg"] = _f(r["targets"] / max(r["games"], 1), 1)
        r["receptions_pg"] = _f(r["receptions"] / max(r["games"], 1), 1)
        r["yards_pg"] = _f(r["yards"] / max(r["games"], 1), 1)
        r["catch_rate"] = _f(_div(r["receptions"], r["targets"]))
        r["yards_cv"] = _f(_cv([x.get("yards") for x in log]), 2)
        last3 = [x.get("targets", 0) for x in log[-3:]]
        r["targets_last3_pg"] = _f(sum(last3) / len(last3), 1) if last3 else None
        r["tags"] = []
    if rec:
        top = max(rec, key=lambda r: r["target_share"] or 0)
        top["tags"].append({"tag": "Primary", "why": f"{top['target_share']:.0%} target share, team high"})
        rz = max(rec, key=lambda r: r.get("red_zone_targets") or 0)
        if (rz.get("red_zone_targets") or 0) >= 3:
            rz["tags"].append({"tag": "Red-zone #1", "why": f"{rz['red_zone_targets']} red-zone targets"})
        on = [r for r in rec if r.get("snap_share") is not None]
        if on:
            most = max(on, key=lambda r: r["snap_share"])
            most["tags"].append({"tag": "Most on field", "why": f"{most['snap_share']:.0%} of offensive snaps"})
        for r in rec:
            if r["targets_pg"] >= 7 and not any(t["tag"] == "Primary" for t in r["tags"]):
                r["tags"].append({"tag": "Volume", "why": f"{r['targets_pg']} targets a game"})
            if (r.get("avg_depth_of_target") or 0) >= 13 and r["targets"] >= 15:
                r["tags"].append({"tag": "Deep threat", "why": f"{r['avg_depth_of_target']:.1f}-yard average target depth"})
            if (r.get("avg_depth_of_target") or 99) < 7.5 and (r["catch_rate"] or 0) >= 0.72 and r["targets"] >= 15:
                r["tags"].append({"tag": "Possession", "why": f"{r['catch_rate']:.0%} catch rate on short targets"})
            if r["yards_cv"] is not None and r["games"] >= 4:
                if r["yards_cv"] >= 0.65:
                    r["tags"].append({"tag": "Boom-bust", "why": f"yards swing widely game to game (CV {r['yards_cv']:.2f})"})
                elif r["yards_cv"] <= 0.35 and r["yards_pg"] >= 30:
                    r["tags"].append({"tag": "Steady", "why": f"consistent yardage (CV {r['yards_cv']:.2f})"})
            if r["targets_last3_pg"] is not None and r["games"] >= 5:
                if r["targets_last3_pg"] >= r["targets_pg"] * 1.3 and r["targets_last3_pg"] - r["targets_pg"] >= 1.5:
                    r["tags"].append({"tag": "Rising", "why": f"{r['targets_last3_pg']} targets a game over the last 3 vs {r['targets_pg']}"})
                elif r["targets_last3_pg"] <= r["targets_pg"] * 0.7 and r["targets_pg"] - r["targets_last3_pg"] >= 1.5:
                    r["tags"].append({"tag": "Falling", "why": f"{r['targets_last3_pg']} targets a game over the last 3 vs {r['targets_pg']}"})
    for r in rush:
        r["full_name"] = id_to_name.get(r.get("player_id"), r["player"])
        r["snap_share"] = snap_share.get(r["full_name"])
        r["carries_pg"] = _f(r["carries"] / max(r["games"], 1), 1)
        r["yards_pg"] = _f(r["yards"] / max(r["games"], 1), 1)
        r["yards_cv"] = _f(_cv([x.get("yards") for x in r.get("log", [])]), 2)
        r["tags"] = []
        cs = r.get("carry_share") or 0
        if r.get("pos") == "QB":
            if r["carries_pg"] >= 5:
                r["tags"].append({"tag": "Running QB", "why": f"{r['carries_pg']} carries a game"})
            continue
        if cs >= 0.6:
            r["tags"].append({"tag": "Lead back", "why": f"{cs:.0%} of team carries"})
        elif cs >= 0.35:
            r["tags"].append({"tag": "Committee", "why": f"{cs:.0%} of team carries (under 60%)"})
    rbs = [r for r in rush if r.get("pos") != "QB"]
    if rbs and not any(t["tag"] == "Lead back" for r in rbs for t in r["tags"]):
        for r in rbs:
            cs = r.get("carry_share") or 0
            if 0.2 <= cs < 0.35:
                r["tags"].append({"tag": "Committee", "why": f"{cs:.0%} of team carries; no back above 60%"})
    if rbs:
        gl = max(rbs, key=lambda r: r.get("red_zone_carries") or 0)
        if (gl.get("red_zone_carries") or 0) >= 4:
            gl["tags"].append({"tag": "Goal-line back", "why": f"{gl['red_zone_carries']} red-zone carries"})
    for r in rec:
        r["opportunity"] = opportunity_label(r, "rec")
    for r in rush:
        r["opportunity"] = opportunity_label(r, "rush")
    return {"receivers": rec, "rushers": rush}


# ----------------------------------------------------------------------------------------------- injuries
def returning_players(snaps: pd.DataFrame | None, games: pd.DataFrame, season: int, team: str, before: str) -> list[dict]:
    """Players who missed games and came back in the last two games, with snap share before and after."""
    if snaps is None or not len(snaps):
        return []
    tg = games[(games.season == season) & (games.game_type == "REG") & (games.gameday < before) & games.home_score.notna() &
               ((games.home_team == team) | (games.away_team == team))].sort_values("gameday")
    order = list(tg.game_id)
    if len(order) < 3:
        return []
    s = snaps[(snaps.team == team) & snaps.game_id.isin(order)].copy()
    s["pct"] = s[["offense_pct", "defense_pct"]].max(axis=1)
    s["unit"] = s.apply(lambda r: "offense" if (r.offense_pct or 0) >= (r.defense_pct or 0) else "defense", axis=1)
    out = []
    recent = order[-2:]
    for name, grp in s.groupby("player"):
        played = {gid: p for gid, p in zip(grp.game_id, grp.pct) if p and p > 0}
        idx = [order.index(gid) for gid in played]
        if not idx:
            continue
        first, lastp = min(idx), max(idx)
        missed = [order[i] for i in range(first, lastp + 1) if order[i] not in played]
        if not missed or order[lastp] not in recent:
            continue
        miss_end = max(order.index(m) for m in missed)
        before_p = [played[order[i]] for i in range(first, miss_end) if order[i] in played]
        after_p = [played[order[i]] for i in range(miss_end + 1, len(order)) if order[i] in played]
        if not before_p or not after_p:
            continue
        pre = sum(before_p) / len(before_p)
        if pre < 0.35:
            continue
        post = after_p[-1]
        status = "Working back in" if post < pre * 0.8 else "Full workload again"
        out.append({"player": name, "position": str(grp.position.iloc[-1]), "unit": str(grp.unit.iloc[-1]), "games_missed": len(missed),
                    "snap_pct_before": _f(pre, 2), "snap_pct_last_game": _f(post, 2), "games_since_return": len(after_p), "status": status})
    out.sort(key=lambda r: (r["status"] != "Working back in", -r["snap_pct_before"]))
    return out[:10]


def injury_impact(team_pk: dict, snap_share: dict, def_snaps: dict) -> list[dict]:
    """Official report plus ESPN, one row per player, with how much that player plays and who is next up."""
    rows = {}
    starters = {s["player"]: s["slot"] for s in team_pk.get("depth_chart", {}).get("starters", [])}
    second = {}
    for s in team_pk.get("depth_chart", {}).get("second_string", []):
        second.setdefault(s["slot"], s["player"])
    for r in team_pk.get("injuries", {}).get("official_report", []) or []:
        rows[r["player"]] = {"player": r["player"], "position": r.get("position"), "game_status": r.get("game_status"),
                             "practice": r.get("practice_status"), "injury": r.get("injury"), "espn": None, "espn_comment": None}
    for r in team_pk.get("injuries", {}).get("espn_live", []) or []:
        x = rows.setdefault(r["player"], {"player": r["player"], "position": r.get("position"), "game_status": None,
                                          "practice": None, "injury": None})
        x["espn"] = r.get("status"); x["espn_comment"] = r.get("comment")
    out = []
    for name, x in rows.items():
        share = snap_share.get(name) or def_snaps.get(name)
        slot = starters.get(name)
        x["starter_slot"] = slot
        x["snap_share"] = share
        x["next_up"] = second.get(slot) if slot else None
        status = (x.get("game_status") or x.get("espn") or "").lower()
        weight = 3 if status in ("out", "injured reserve", "doubtful") else 2 if status == "questionable" else 1
        imp = (share or 0) + (0.5 if slot else 0)
        x["impact"] = "high" if imp >= 0.9 and weight >= 2 else "medium" if imp >= 0.5 and weight >= 2 else "low"
        x["status_level"] = weight
        out.append(x)
    out.sort(key=lambda r: ({"high": 0, "medium": 1, "low": 2}[r["impact"]], -r["status_level"], -(r["snap_share"] or 0)))
    return out


def defense_snap_share(snaps: pd.DataFrame | None, team: str, game_ids) -> dict:
    if snaps is None or not len(snaps):
        return {}
    s = snaps[(snaps.team == team) & snaps.game_id.isin(list(game_ids)) & (snaps.defense_pct.fillna(0) > 0)]
    return {k: _f(v, 3) for k, v in s.groupby("player").defense_pct.mean().items()}


# ----------------------------------------------------------------------------------------------- weather
def weather_verdict(wx: dict, roof: str, alerts: list[dict] | None = None) -> dict:
    roof = (roof or "").lower()
    if roof in ("dome", "closed"):
        return {"level": "good", "headline": "Indoors: weather is not a factor", "details": []}
    if wx.get("status") != "OK":
        return {"level": "unknown", "headline": f"Forecast not available ({wx.get('status')})", "details": []}
    dg = wx.get("during_game", {})
    rain = dg.get("precip_chance_pct_max") or 0
    wind = dg.get("wind_mph_max") or 0
    temp = dg.get("temp_f_min")
    det, level = [], "good"
    for a in alerts or []:
        det.append(f"NWS alert: {a.get('event')}: {a.get('headline') or ''}".strip())
        if any(k in (a.get("event") or "").lower() for k in ("hurricane", "tropical storm", "tornado", "blizzard", "winter storm", "high wind")):
            level = "bad"
    if rain >= 70 and wind >= 15:
        head = f"Weather game: {rain}% rain and wind up to {wind:.0f} mph. Passing and kicking take a hit; be careful with passing props."
        level = "bad"
    elif rain >= 60:
        head = f"Rain likely ({rain}%). Measured rain effect: pass yards about 15% lower, catches about 6% lower."
        level = "warn" if level != "bad" else level
    elif wind >= 20:
        head = f"High wind, up to {wind:.0f} mph: deep passing and field goals suffer."
        level = "warn" if level != "bad" else level
    elif wind >= 15:
        head = f"Breezy, up to {wind:.0f} mph: a small drag on deep passing and kicking."
        level = "warn" if level != "bad" else level
    elif rain >= 35:
        head = f"Some chance of rain ({rain}%). Watch the forecast closer to kickoff."
        level = "warn" if level != "bad" else level
    else:
        head = f"Clean conditions: {rain}% rain, wind up to {wind:.0f} mph."
    if temp is not None and temp <= 25:
        det.append(f"Cold: {temp}°F at the low. Ball is harder to throw and catch.")
        if level == "good":
            level = "warn"
    if level == "bad" and not head.startswith("Weather game"):
        head = "Severe weather alert at the stadium. " + head
    return {"level": level, "headline": head, "details": det}


def nws_alerts(home: str, roof: str, *, offline: bool, fetch_json=None) -> list[dict]:
    if offline or fetch_json is None or (roof or "").lower() in ("dome", "closed"):
        return []
    try:
        from pregame.weather import STADIUM
        lat, lon = STADIUM[home]
        d = fetch_json(f"https://api.weather.gov/alerts/active?point={lat},{lon}")
        return [{"event": f["properties"].get("event"), "headline": f["properties"].get("headline"),
                 "ends": f["properties"].get("ends")} for f in d.get("features", [])][:5]
    except Exception:  # noqa: BLE001 - alerts are optional
        return []


# ----------------------------------------------------------------------------------------------- betting trends
def team_trends(games: pd.DataFrame, season: int, team: str, before: str) -> dict:
    """This season's record straight up, against the closing spread and against the closing total (nflverse lines)."""
    g = games[(games.season == season) & (games.game_type == "REG") & (games.gameday < before) & games.home_score.notna() &
              ((games.home_team == team) | (games.away_team == team))].sort_values("gameday")
    rows = []
    for r in g.itertuples():
        home = r.home_team == team
        pf, pa = (r.home_score, r.away_score) if home else (r.away_score, r.home_score)
        line = None if pd.isna(r.spread_line) else (r.spread_line if home else -r.spread_line)   # points this team was favoured by
        ats = None if line is None else ("W" if pf - pa > line else "L" if pf - pa < line else "P")
        ou = None if pd.isna(r.total_line) else ("O" if pf + pa > r.total_line else "U" if pf + pa < r.total_line else "P")
        rows.append({"week": int(r.week), "opp": (r.away_team if home else r.home_team), "site": "home" if home else "away",
                     "pf": int(pf), "pa": int(pa), "su": "W" if pf > pa else "L" if pf < pa else "T", "fav_by": _f(line, 1),
                     "ats": ats, "ou": ou, "total_line": _f(r.total_line, 1)})

    def rec(sel, k, keys):
        x = [r[k] for r in sel if r[k]]
        return "-".join(str(x.count(c)) for c in keys)

    fav = [r for r in rows if r["fav_by"] is not None and r["fav_by"] > 0]
    dog = [r for r in rows if r["fav_by"] is not None and r["fav_by"] < 0]
    out = {"games": rows, "straight_up": rec(rows, "su", "WLT").rstrip("-0") if rows else "0-0",
           "ats": rec(rows, "ats", "WLP"), "over_under": rec(rows, "ou", "OUP"),
           "ats_as_favorite": rec(fav, "ats", "WLP"), "ats_as_underdog": rec(dog, "ats", "WLP"),
           "ats_home": rec([r for r in rows if r["site"] == "home"], "ats", "WLP"),
           "ats_away": rec([r for r in rows if r["site"] == "away"], "ats", "WLP"),
           "last5_ats": "".join(r["ats"] or "-" for r in rows[-5:]), "last5_ou": "".join(r["ou"] or "-" for r in rows[-5:]),
           "points_for_pg": _f(sum(r["pf"] for r in rows) / len(rows), 1) if rows else None,
           "points_against_pg": _f(sum(r["pa"] for r in rows) / len(rows), 1) if rows else None,
           "note": "Closing lines from the nflverse schedule. W-L-P against the spread; O-U-P against the total."}
    return out


def quarter_scoring(pbp: pd.DataFrame | None, team: str, weeks) -> dict | None:
    """Average points scored and allowed by quarter over the trend window (from the running score in play-by-play)."""
    if pbp is None:
        return None
    gs = pbp[((pbp.home_team == team) | (pbp.away_team == team)) & pbp.week.isin(list(weeks))]
    if not len(gs):
        return None
    tot = {"for": [0.0] * 4, "against": [0.0] * 4}
    n = 0
    for gid, pl in gs.groupby("game_id"):
        h, a = pl.home_team.iloc[0], pl.away_team.iloc[0]
        q = _quarters(pl, h, a)
        mine, theirs = (q[h], q[a]) if team == h else (q[a], q[h])
        for i in range(min(4, len(mine))):
            tot["for"][i] += mine[i]; tot["against"][i] += theirs[i]
        n += 1
    f = [_f(x / n, 1) for x in tot["for"]]
    ag = [_f(x / n, 1) for x in tot["against"]]
    return {"games": n, "for": f, "against": ag, "first_half": [_f(f[0] + f[1], 1), _f(ag[0] + ag[1], 1)],
            "second_half": [_f(f[2] + f[3], 1), _f(ag[2] + ag[3], 1)], "note": "Overtime points are left out."}


def opportunity_label(r: dict, kind: str) -> dict:
    """The analyst prompt's labels: expanding, shrinking, volume-supported or efficiency-driven."""
    log = r.get("log", [])
    key = "targets" if kind == "rec" else "carries"
    per = r.get("targets_pg") if kind == "rec" else r.get("carries_pg")
    last3 = [x.get(key, 0) for x in log[-3:]]
    l3 = sum(last3) / len(last3) if last3 else None
    if per and l3 is not None and r.get("games", 0) >= 5:
        if l3 >= per * 1.2 and l3 - per >= 1.0:
            return {"label": "expanding", "why": f"{l3:.1f} {key} a game over the last 3 vs {per:.1f} in the window"}
        if l3 <= per * 0.8 and per - l3 >= 1.0:
            return {"label": "shrinking", "why": f"{l3:.1f} {key} a game over the last 3 vs {per:.1f} in the window"}
    if kind == "rec":
        ypt = r.get("yards_per_target") or 0
        td_share = _div(r.get("td", 0), max(r.get("receptions", 0), 1)) or 0
        if (per or 0) >= 6:
            return {"label": "volume-supported", "why": f"{per:.1f} targets a game"}
        if ypt >= 10.5 or td_share >= 0.2:
            return {"label": "efficiency-driven", "why": f"{ypt:.1f} yards per target on {per or 0:.1f} targets a game" if ypt >= 10.5
                    else f"{r.get('td')} TDs on {r.get('receptions')} catches"}
        return {"label": "low volume", "why": f"{per or 0:.1f} targets a game"}
    if (per or 0) >= 12:
        return {"label": "volume-supported", "why": f"{per:.1f} carries a game"}
    if (r.get("yards_per_carry") or 0) >= 5.2:
        return {"label": "efficiency-driven", "why": f"{r['yards_per_carry']:.1f} yards per carry on {per or 0:.1f} carries"}
    return {"label": "low volume", "why": f"{per or 0:.1f} carries a game"}


def unit_injuries(inj: list[dict]) -> dict:
    """Offensive-line and secondary starters listed Out, Doubtful or Questionable."""
    ol = {"LT", "LG", "C", "RG", "RT", "T", "G", "OL"}
    db = {"CB", "S", "FS", "SS", "NB", "RCB", "LCB", "DB", "SAF"}
    lb = {"LB", "ILB", "OLB", "MLB", "LILB", "RILB", "WILL", "MIKE", "SAM"}
    dl = {"DE", "DT", "NT", "LDE", "RDE", "LDT", "RDT", "EDGE", "DL"}

    def pick(group):
        return [{"player": x["player"], "slot": x.get("starter_slot") or x.get("position"), "status": x.get("game_status") or x.get("espn") or x.get("practice")}
                for x in inj if x.get("status_level", 0) >= 2 and (x.get("starter_slot") in group or (x.get("position") in group and (x.get("snap_share") or 0) >= 0.5))]
    return {"offensive_line": pick(ol), "secondary": pick(db), "linebackers": pick(lb), "defensive_line": pick(dl)}
