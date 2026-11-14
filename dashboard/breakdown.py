"""Two-game receiving breakdown: explosive plays, 80-100 yard paths, coverage personnel and prop lines.

    python3 -m dashboard.breakdown 2026_10_MIN_GB 2026_10_PIT_CIN

Reads the board JSON (dashboard/data/<game>.json) for lines, props, weather, rest, injuries, coverage shell and the
opportunity simulation, and the cached nflverse tables in pregame/.cache for box scores and per-defender coverage.
Writes dashboard/results/breakdown_<games>.json. Research only: nothing here has been graded against prop prices.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "pregame" / ".cache"
DATA = ROOT / "dashboard" / "data"
OUT = ROOT / "dashboard" / "results"
ROWS = ROOT / "research" / "receiver_volatility_2026-11-14" / "rows.parquet"
EXPLOSIVE = 20          # yards on a completed pass
COVER_POS = {"CB", "S", "FS", "SS", "DB", "LB", "ILB", "OLB", "MLB"}
BOOKS = ("fanduel", "draftkings")


def _f(x, d=1):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), d)


def load(season: int, injuries_path: Path | None = None):
    pbp = pd.read_parquet(CACHE / f"play_by_play_{season}.parquet")
    pbp = pbp[(pbp.season_type == "REG")]
    ro = pd.read_parquet(CACHE / f"roster_weekly_{season}.parquet")
    pos = dict(zip(ro.dropna(subset=["gsis_id"]).sort_values("week").gsis_id, ro.dropna(subset=["gsis_id"]).sort_values("week").position))
    adv = pd.read_parquet(CACHE / f"advstats_week_def_{season}.parquet").fillna({"def_targets": 0})
    snaps = pd.read_parquet(CACHE / f"snap_counts_{season}.parquet")
    inj = pd.read_parquet(injuries_path or CACHE / f"injuries_{season}.parquet")
    return pbp, pos, adv, snaps, inj


def targets_table(pbp, pos):
    t = pbp[(pbp.pass_attempt == 1) & (pbp.sack != 1) & (pbp.two_point_attempt != 1) & pbp.receiver_player_id.notna()].copy()
    t["pos"] = t.receiver_player_id.map(pos)
    t["yds"] = t.receiving_yards.fillna(0)
    t["ex"] = ((t.complete_pass == 1) & (t.yds >= EXPLOSIVE)).astype(int)
    t["ex40"] = ((t.complete_pass == 1) & (t.yds >= 40)).astype(int)
    return t


def player_games(t):
    g = t.groupby(["receiver_player_id", "receiver_player_name", "posteam", "defteam", "week", "pos"]).agg(
        tgt=("pass_attempt", "size"), rec=("complete_pass", "sum"), yds=("yds", "sum"), ex=("ex", "sum"), long=("yds", "max")).reset_index()
    return g


# ------------------------------------------------------------------------------------------------ defense
def explosive_allowed(t):
    """Per defense: 20+ and 40+ completions allowed per game, by receiver position, with league rank (1 = allows most)."""
    games = t.groupby("defteam").week.nunique()
    out = {}
    tot = t.groupby("defteam").ex.sum() / games
    t40 = t.groupby("defteam").ex40.sum() / games
    rank = tot.rank(ascending=False, method="min")
    for d in games.index:
        x = t[t.defteam == d]
        bypos = {p: _f(x[x.pos == p].ex.sum() / games[d], 2) for p in ("WR", "TE", "RB")}
        yds_ex = x[x.ex == 1].yds.sum() / games[d]
        out[d] = {"games": int(games[d]), "ex20_pg": _f(tot[d], 2), "ex40_pg": _f(t40[d], 2), "rank": int(rank[d]),
                  "explosive_yards_pg": _f(yds_ex, 1), "by_pos_pg": bypos}
    out["_league"] = {"ex20_pg": _f(tot.mean(), 2), "ex40_pg": _f(t40.mean(), 2),
                      "by_pos_pg": {p: _f(np.mean([out[d]["by_pos_pg"][p] for d in games.index]), 2) for p in ("WR", "TE", "RB")}}
    return out


def big_games_allowed(pg, d, floor=80):
    x = pg[(pg.defteam == d) & (pg.yds >= floor)].sort_values("week")
    return [{"week": int(r.week), "player": r.receiver_player_name, "team": r.posteam, "pos": r.pos, "targets": int(r.tgt),
             "rec": int(r.rec), "yards": int(r.yds), "explosive": int(r.ex), "long": int(r.long)} for r in x.itertuples()]


def _status_lookup(inj, team, week, board_rows):
    i = inj[(inj.team == team) & (inj.week == week)]
    st = {}
    for r in i.itertuples():
        st[r.full_name] = {"status": r.report_status if isinstance(r.report_status, str) else None,
                           "practice": r.practice_status if isinstance(r.practice_status, str) else None,
                           "injury": r.report_primary_injury if isinstance(r.report_primary_injury, str) else None}
    for r in board_rows or []:
        x = st.setdefault(r["player"], {"status": None, "practice": r.get("practice"), "injury": r.get("injury")})
        if not x.get("status") and r.get("espn") in ("Injured Reserve", "Out"):
            x["status"] = r["espn"]
    return st


def _match(name, st):
    if name in st:
        return st[name]
    last = name.split()[-1].replace(".", "")
    first = name[0]
    for k, v in st.items():
        parts = k.replace(" Jr.", "").replace(" III", "").replace(" II", "").split()
        if parts and parts[-1].replace(".", "") == last.replace("Jr", "") and k[0] == first:
            return v
    for k, v in st.items():
        if k.split()[-1] == name.replace(" Jr.", "").split()[-1] and k[0] == first:
            return v
    return {"status": None, "practice": None, "injury": None}


def coverage_personnel(adv, snaps, inj, team, week, board_inj):
    """Every CB/S/LB who played 25%+ of defensive snaps in either of the team's last two games, with coverage allowed."""
    s = snaps[(snaps.team == team) & snaps.position.isin(COVER_POS)]
    weeks = sorted(s.week.unique())
    last2 = weeks[-2:]
    keep = s[s.week.isin(last2) & (s.defense_pct >= 0.25)].pfr_player_id.unique()
    st = _status_lookup(inj, team, week, board_inj)
    rows = []
    for pid in keep:
        me = s[s.pfr_player_id == pid].sort_values("week")
        name, position = me.player.iloc[-1], me.position.iloc[-1]
        a = adv[(adv.pfr_player_id == pid) & (adv.team == team)]
        gp = a.week.nunique()
        tg, rc, yd = a.def_targets.sum(), a.def_completions_allowed.fillna(0).sum(), a.def_yards_allowed.fillna(0).sum()
        stat = _match(name, st)
        rows.append({"player": name, "pos": position, "snap_last": _f(me.defense_pct.iloc[-1] * 100, 0),
                     "snap_season": _f(me.defense_pct.mean() * 100, 0), "games": int(gp),
                     "tgt_pg": _f(tg / gp) if gp else None, "rec_pg": _f(rc / gp) if gp else None, "yds_pg": _f(yd / gp) if gp else None,
                     "ypt": _f(yd / tg) if tg else None, "cmp_pct": _f(rc / tg * 100, 0) if tg else None,
                     "td": int(a.def_receiving_td_allowed.fillna(0).sum()), "ints": int(a.def_ints.fillna(0).sum()),
                     "yac": int(a.def_yards_after_catch.fillna(0).sum()), "missed_tackles": int(a.def_missed_tackles.fillna(0).sum()),
                     "status": stat.get("status"), "practice": stat.get("practice"), "injury": stat.get("injury")})
    order = {"CB": 0, "DB": 0, "S": 1, "FS": 1, "SS": 1, "LB": 2, "ILB": 2, "OLB": 2, "MLB": 2}
    rows.sort(key=lambda r: (order.get(r["pos"], 3), -(r["snap_season"] or 0)))
    return rows, [int(w) for w in last2]


def league_defender_baseline(adv):
    L = adv.groupby(["pfr_player_id", "team"]).agg(gp=("week", "nunique"), tgt=("def_targets", "sum"),
                                                    rec=("def_completions_allowed", "sum"), yds=("def_yards_allowed", "sum"))
    L = L[(L.gp >= 5) & (L.tgt >= 20)]
    return {"rec_pg": _f((L.rec / L.gp).median()), "yds_pg": _f((L.yds / L.gp).median()), "ypt": _f((L.yds / L.tgt).median()), "n": int(len(L))}


# ------------------------------------------------------------------------------------------------ receivers
def receiver_profile(pg, pid, ex_allowed, implied):
    me = pg[pg.receiver_player_id == pid].sort_values("week")
    if not len(me):
        return None
    log = [{"week": int(r.week), "opp": r.defteam, "targets": int(r.tgt), "rec": int(r.rec), "yards": int(r.yds),
            "explosive": int(r.ex), "long": int(r.long), "opp_ex_rank": ex_allowed.get(r.defteam, {}).get("rank")} for r in me.itertuples()]
    y = me.yds.to_numpy()
    hi = me[me.tgt >= 8]
    soft = me[me.defteam.map(lambda d: (ex_allowed.get(d, {}).get("rank") or 99) <= 12)]
    hard = me[me.defteam.map(lambda d: (ex_allowed.get(d, {}).get("rank") or 0) > 12)]
    return {"games": int(len(me)), "log": log, "explosive_pg": _f(me.ex.mean(), 2), "explosive_total": int(me.ex.sum()),
            "games_with_explosive": int((me.ex > 0).sum()),
            "hits": {str(k): int((y >= k).sum()) for k in (50, 60, 70, 80, 100)},
            "eight_plus": {"games": int(len(hi)), "rec_avg": _f(hi.rec.mean()) if len(hi) else None, "yds_avg": _f(hi.yds.mean()) if len(hi) else None,
                           "yds_median": _f(hi.yds.median()) if len(hi) else None,
                           "hit70": int((hi.yds >= 70).sum()), "hit80": int((hi.yds >= 80).sum()), "hit100": int((hi.yds >= 100).sum())},
            "under_eight": {"games": int((me.tgt < 8).sum()), "yds_avg": _f(me[me.tgt < 8].yds.mean()) if (me.tgt < 8).any() else None},
            "vs_explosive_friendly": {"games": int(len(soft)), "yds_avg": _f(soft.yds.mean()) if len(soft) else None,
                                      "ex_pg": _f(soft.ex.mean(), 2) if len(soft) else None},
            "vs_explosive_stingy": {"games": int(len(hard)), "yds_avg": _f(hard.yds.mean()) if len(hard) else None,
                                    "ex_pg": _f(hard.ex.mean(), 2) if len(hard) else None},
            "last3": {"targets_pg": _f(me.tail(3).tgt.mean()), "yds_pg": _f(me.tail(3).yds.mean())}}


def history_rates():
    """Pregame view from 2022-26: chance of 80+/100+ for a WR/TE, by his target rate coming in and the team's implied total."""
    if not ROWS.exists():
        return None
    r = pd.read_parquet(ROWS)
    r = r[r.pos.isin(["WR", "TE"]) & (r.games_prior >= 3) & r.implied.notna()]
    r["tgt_b"] = pd.cut(r.tgt_pg, [0, 5, 6.5, 8, 9.5, 30], labels=["<5", "5-6.5", "6.5-8", "8-9.5", "9.5+"])
    r["imp_b"] = pd.cut(r.implied, [0, 20, 24, 28, 60], labels=["<20", "20-24", "24-28", "28+"])
    pre = r.groupby(["tgt_b", "imp_b"], observed=True).agg(n=("y_yds", "size"), p80=("y_yds", lambda s: (s >= 80).mean()),
                                                              p100=("y_yds", lambda s: (s >= 100).mean())).reset_index()
    r["act_b"] = pd.cut(r.y_tgt, [-1, 5, 7, 9, 11, 40], labels=["0-5", "6-7", "8-9", "10-11", "12+"])
    act = r.groupby(["act_b", "pos"], observed=True).agg(n=("y_yds", "size"), p70=("y_yds", lambda s: (s >= 70).mean()),
                                                            p80=("y_yds", lambda s: (s >= 80).mean()), p100=("y_yds", lambda s: (s >= 100).mean()),
                                                            med=("y_yds", "median")).reset_index()
    return {"pregame": [{"targets_pg": str(x.tgt_b), "implied": str(x.imp_b), "n": int(x.n), "p80": _f(x.p80 * 100, 0), "p100": _f(x.p100 * 100, 0)}
                        for x in pre.itertuples() if x.n >= 30],
            "actual_targets": [{"targets": str(x.act_b), "pos": x.pos, "n": int(x.n), "p70": _f(x.p70 * 100, 0), "p80": _f(x.p80 * 100, 0),
                                "p100": _f(x.p100 * 100, 0), "median": _f(x.med, 0)} for x in act.itertuples()]}


# ------------------------------------------------------------------------------------------------ props
def props_for(board, player):
    m = board.get("books", {}).get("markets", {})
    out = {}
    for stat in ("receptions", "receiving_yards"):
        mk = m.get(f"{stat}|{player}")
        if not mk:
            continue
        for b in BOOKS:
            q = mk.get("books", {}).get(b)
            if q and q.get("line") is not None:
                out.setdefault(stat, {})[b] = {"line": q["line"], "over": q["prices"].get("Over"), "under": q["prices"].get("Under"),
                                               "no_vig_over": q.get("no_vig", {}).get("Over")}
    return out


def _amer_to_p(a):
    return None if a is None else (100 / (a + 100) if a > 0 else -a / (-a + 100))


def sim_at_line(sim_row, stat, line):
    tbl = sim_row.get("yards" if stat == "receiving_yards" else "receptions") or {}
    need = int(np.floor(line)) + 1
    keys = sorted(int(k) for k in tbl)
    if str(need) in tbl:
        return tbl[str(need)]
    lo = [k for k in keys if k <= need]; hi = [k for k in keys if k >= need]
    if lo and hi and lo[-1] != hi[0]:
        a, b = lo[-1], hi[0]
        return round(tbl[str(a)] + (tbl[str(b)] - tbl[str(a)]) * (need - a) / (b - a), 3)
    return None


# ------------------------------------------------------------------------------------------------ assemble
def side_report(board, side_key, pg, ex, adv, snaps, inj, base):
    s = board["sides"][side_key]
    off, de = s["offense"], s["defense"]
    week = board["game"]["week"]
    cov, last2 = coverage_personnel(adv, snaps, inj, de, week, s.get("defense_injuries", []) + s.get("offense_injuries", []))
    vis = s.get("visual", {})
    shell = vis.get("shell") or {}
    implied = board.get("implied_points", {}).get(off)
    opp = s.get("opportunity", {})
    recv = []
    pool = [r for r in opp.get("receivers", []) if r.get("pos") in ("WR", "TE") and (r.get("targets_mean") or 0) >= 2.5]
    pool = sorted(pool, key=lambda r: -(r.get("targets_mean") or 0))[:6]
    for r in pool:
        pid = r.get("player_id")
        prof = receiver_profile(pg, pid, ex, implied)
        rv = (vis.get("receivers", {}) or {}).get(pid, {})
        routes = rv.get("routes") or {}
        props = props_for(board, r["player"])
        for stat, books in props.items():
            for b, q in books.items():
                q["sim_over"] = sim_at_line(r, stat, q["line"])
                q["break_even"] = _f(_amer_to_p(q["over"]), 3)
        recv.append({"player": r["player"], "pos": r["pos"], "player_id": pid, "inputs": r.get("inputs"),
                     "targets_mean": r.get("targets_mean"), "receptions_mean": r.get("receptions_mean"),
                     "yards_mean": r.get("yards_mean"), "yards_median": r.get("yards_median"), "yards_p25_p75": r.get("yards_p25_p75"),
                     "p_yards": r.get("yards"), "p_rec": r.get("receptions"), "targets_needed": r.get("targets_needed"),
                     "targets_needed_chance": r.get("targets_needed_chance"), "profile": prof, "props": props,
                     "tiers": rv.get("tiers"),
                     "coverage_2025": {k: routes.get(k) for k in ("vs_man", "vs_zone", "vs_mofo", "vs_mofc")} if routes else None,
                     "coverage_season": routes.get("season") if routes else None})
    return {"offense": off, "defense": de, "implied": implied, "team_pass_attempts": opp.get("team_pass_attempts"),
            "script_pass_multiplier": opp.get("script_pass_multiplier"), "missing_target_share": opp.get("missing_target_share"),
            "defense_explosive": ex.get(de), "league_explosive": ex.get("_league"),
            "defense_allowed": {k: s.get("defense_allowed", {}).get(k) for k in ("pass_yards_pg", "pass_att_pg", "yards_per_pass_attempt",
                                                                                 "completion_rate", "deep_attempts_pg", "deep_completion_rate", "sack_rate", "pressure_rate")},
            "defense_rank": s.get("defense_rank"), "defense_by_game": s.get("defense_by_game"),
            "big_games_allowed": big_games_allowed(pg, de), "coverage_personnel": cov, "coverage_weeks": last2,
            "coverage_injured": [{"player": r.full_name, "pos": r.position, "status": r.report_status, "injury": r.report_primary_injury,
                                  "practice": r.practice_status} for r in inj[(inj.team == de) & (inj.week == week)].itertuples()
                                 if r.position in COVER_POS and isinstance(r.report_status, str)],
            "defender_league_median": base, "coverage_profile": s.get("coverage_profile"), "shell": shell,
            "pass_zones_defense": (s.get("pass_zones") or {}).get("defense"), "qb": s.get("qb"),
            "offense_injuries_own": [{"player": r.full_name, "pos": r.position, "status": r.report_status, "injury": r.report_primary_injury,
                                      "practice": r.practice_status} for r in inj[(inj.team == off) & (inj.week == week)].itertuples()
                                     if isinstance(r.report_status, str)],
            "offense_units_hurt": s.get("offense_units_hurt"), "defense_units_hurt": s.get("defense_units_hurt"),
            "receivers": recv}


def build(game_ids, injuries_path=None):
    boards = [json.loads((DATA / f"{g}.json").read_text()) for g in game_ids]
    season = boards[0]["game"]["season"]
    pbp, pos, adv, snaps, inj = load(season, injuries_path)
    t = targets_table(pbp, pos)
    pg = player_games(t)
    ex = explosive_allowed(t)
    base = league_defender_baseline(adv)
    out = {"generated_utc": pd.Timestamp.now('UTC').isoformat(timespec="seconds"), "history": history_rates(), "games": []}
    for b in boards:
        g = b["game"]
        out["games"].append({
            "game": g, "market": b.get("market"), "implied_points": b.get("implied_points"),
            "books_retrieved": b.get("books", {}).get("retrieved_utc"), "props_status": b.get("books", {}).get("props_status"),
            "game_lines": {k: b.get("books", {}).get("markets", {}).get(k) for k in ("spread", "total")},
            "weather": b.get("weather"), "weather_verdict": b.get("weather_verdict"), "context": b.get("context"),
            "sides": [side_report(b, f"{g['away']}_vs_{g['home']}", pg, ex, adv, snaps, inj, base),
                      side_report(b, f"{g['home']}_vs_{g['away']}", pg, ex, adv, snaps, inj, base)]})
    return out


def main(argv):
    inj = None
    if argv and argv[0].startswith("--injuries="):
        inj = Path(argv.pop(0).split("=", 1)[1])
    ids = argv or ["2026_10_MIN_GB", "2026_10_PIT_CIN"]
    res = build(ids, inj)
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"breakdown_{'__'.join(ids)}.json"
    p.write_text(json.dumps(res, indent=1, default=str))
    print(p)


if __name__ == "__main__":
    main(sys.argv[1:])
