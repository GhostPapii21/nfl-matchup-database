"""Assemble one game's pregame research packet from the loaded datasets."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from . import metrics as M, splits as SP

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "pregame-packet/1"
SLOTS = {"Thursday": "Thursday Night Football", "Monday": "Monday Night Football", "Saturday": "Saturday"}
INJ_OUT = {"Out", "Doubtful"}


def slot_name(weekday: str, gametime: str) -> str:
    if weekday == "Sunday":
        return "Sunday Night Football" if str(gametime) >= "19:00" else ("Sunday late window" if str(gametime) >= "16:00" else "Sunday early window")
    return SLOTS.get(weekday, weekday)


# ------------------------------------------------------------------ people: injuries, depth, defenders, moves
def injuries_for(team, week, inj, espn, starters):
    rows = []
    if inj is not None and len(inj):
        x = inj[(inj.team == team) & (inj.week == week)]
        for r in x.itertuples():
            rows.append({"player": r.full_name, "position": r.position, "game_status": None if pd.isna(r.report_status) else r.report_status,
                         "practice_status": None if pd.isna(r.practice_status) else r.practice_status,
                         "injury": None if pd.isna(r.report_primary_injury) else r.report_primary_injury,
                         "starter": r.gsis_id in starters, "source": "nflverse official report"})
    live = (espn or {}).get("teams", {}).get(team, [])
    return {"official_report": sorted(rows, key=lambda r: (not r["starter"], str(r["position"]))),
            "official_report_status": "OK" if rows else "NOT_POSTED_YET_OR_EMPTY",
            "espn_live": live, "espn_live_status": (espn or {}).get("status", "NOT_REQUESTED"),
            "note": "A player missing from the report is UNKNOWN, not healthy. Final inactives post about 90 minutes before kickoff and are not in this file."}


def depth_chart(team, dc):
    if dc is None or not len(dc):
        return {"status": "UNAVAILABLE", "starters": [], "starter_ids": set()}
    x = dc[dc.team == team]
    x = x[x.dt == x.dt.max()]
    st = x[x.pos_rank == 1]
    rows = [{"slot": r.pos_abb, "player": r.player_name, "group": r.pos_grp} for r in st.sort_values(["pos_grp", "pos_slot"]).itertuples()]
    backups = x[x.pos_rank == 2]
    return {"status": "OK", "as_of": str(x.dt.max()), "starters": rows, "starter_ids": set(st.gsis_id.dropna()),
            "second_string": [{"slot": r.pos_abb, "player": r.player_name} for r in backups.sort_values(["pos_grp", "pos_slot"]).itertuples()]}


def defenders(team, pfr, weeks):
    """Per-defender coverage and pass-rush lines (Pro Football Reference advanced defence via nflverse)."""
    if pfr is None or not len(pfr):
        return {"status": "UNAVAILABLE", "coverage": [], "pass_rush": []}
    x = pfr[(pfr.team == team) & pfr.week.isin(weeks)]
    g = x.groupby("pfr_player_name").agg(games=("week", "nunique"), targets=("def_targets", "sum"), completions=("def_completions_allowed", "sum"),
                                         yards=("def_yards_allowed", "sum"), td=("def_receiving_td_allowed", "sum"), ints=("def_ints", "sum"),
                                         pressures=("def_pressures", "sum"), sacks=("def_sacks", "sum"), hurries=("def_times_hurried", "sum"),
                                         blitzes=("def_times_blitzed", "sum"), missed_tackles=("def_missed_tackles", "sum"), tackles=("def_tackles_combined", "sum"))
    cov = g[g.targets > 0].sort_values("targets", ascending=False).head(10)
    rush = g[g.pressures > 0].sort_values("pressures", ascending=False).head(8)
    f = lambda v: None if pd.isna(v) else float(v)
    return {"status": "OK", "weeks": sorted(int(w) for w in x.week.unique()),
            "coverage": [{"player": n, "games": int(r.games), "targets": int(r.targets), "completions": int(r.completions), "yards": int(r.yards),
                          "yards_per_target": f(r.yards / r.targets), "td_allowed": int(r.td), "interceptions": int(r.ints),
                          "missed_tackles": int(r.missed_tackles)} for n, r in cov.iterrows()],
            "pass_rush": [{"player": n, "games": int(r.games), "pressures": int(r.pressures), "sacks": float(r.sacks), "hurries": int(r.hurries),
                           "blitzes": int(r.blitzes)} for n, r in rush.iterrows()]}


def roster_moves(team, rosters, week, lookback=4):
    """Players on this team's roster now who were on another team (or no roster) within the last few weeks."""
    r = rosters[rosters.week <= week]
    now = r[(r.team == team) & (r.week == r.week.max())]
    prev = r[(r.week >= r.week.max() - lookback) & (r.week < r.week.max())]
    last_team = prev.sort_values("week").drop_duplicates("gsis_id", keep="last").set_index("gsis_id").team
    arrivals = [{"player": x.full_name, "position": x.position, "from": last_team.get(x.gsis_id), "status": x.status}
                for x in now.itertuples() if x.gsis_id in last_team.index and last_team[x.gsis_id] != team]
    gone = prev[(prev.team == team)].drop_duplicates("gsis_id", keep="last")
    cur_team = r[r.week == r.week.max()].set_index("gsis_id").team
    departures = [{"player": x.full_name, "position": x.position, "to": cur_team.get(x.gsis_id)}
                  for x in gone.itertuples() if x.gsis_id in cur_team.index and cur_team[x.gsis_id] != team]
    return {"window_weeks": lookback, "arrivals_from_other_teams": arrivals, "departures_to_other_teams": departures,
            "note": "From weekly roster snapshots: covers trades, waiver claims and signings of players who were on another roster. It does not say which kind of move it was."}


def snap_shares(team, snaps, weeks):
    if snaps is None or not len(snaps):
        return {}
    x = snaps[(snaps.team == team) & snaps.week.isin(weeks) & (snaps.offense_snaps > 0)]
    g = x.groupby("player").offense_pct.mean()
    return {k: float(v) for k, v in g.items()}


# ------------------------------------------------------------------ baselines and projections
PCTS = (5, 10, 15, 20, 25, 50)


def _baseline(values, factor):
    """Recency-weighted mean and the player's own game distribution, both scaled by the opponent factor."""
    v = np.asarray(values, float)
    if len(v) < 3:
        return None
    w = np.linspace(1.0, 2.0, len(v))                      # most recent game counts double the oldest
    mean = float((v * w).sum() / w.sum()) * factor
    q = {f"p{p}": round(float(np.percentile(v * factor, p)), 1) for p in PCTS}
    return {"games": int(len(v)), "weighted_mean": round(mean, 1), "opponent_factor": round(factor, 3), **q,
            "label_map": "p5 Floor, p10 Slight Edge, p15 MAIN, p20 Edge, p25 Pure Edge, p50 Median (PHASE_SCRIPT labels)"}


def _factor(def_sum, def_league, key):
    """Half of the opponent's deviation from league average for that stat, capped at +/-15%."""
    a, b = def_sum.get(key), def_league.get(key)
    if not a or not b:
        return 1.0
    return float(np.clip(1 + 0.5 * (a / b - 1), 0.85, 1.15))


def player_baselines(off_players, opp_def_sum, league_def_avg):
    out = []
    for r in off_players["receivers"]:
        if r["pos"] not in M.POS_GROUPS or r["games"] < 4 or (r["target_share"] or 0) < 0.08:
            continue                                        # regular targets only: thin samples are not baselines
        k = r["pos"].lower()
        fy, fr = _factor(opp_def_sum, league_def_avg, f"{k}_rec_yards_pg"), _factor(opp_def_sum, league_def_avg, f"{k}_receptions_pg")
        out.append({"player": r["player"], "pos": r["pos"], "target_share": r["target_share"],
                    "receiving_yards": _baseline([g["yards"] for g in r["log"]], fy),
                    "receptions": _baseline([g["receptions"] for g in r["log"]], fr),
                    "targets": _baseline([g["targets"] for g in r["log"]], 1.0)})
    for r in off_players["rushers"]:
        if r["games"] < 3 or r["carries"] / max(r["games"], 1) < 5:
            continue
        f = _factor(opp_def_sum, league_def_avg, "rb_rush_yards_pg" if r["pos"] == "RB" else "rush_yards_pg")
        out.append({"player": r["player"], "pos": r["pos"], "carry_share": r["carry_share"],
                    "rushing_yards": _baseline([g["yards"] for g in r["log"]], f), "carries": _baseline([g["carries"] for g in r["log"]], 1.0)})
    for r in off_players["quarterbacks"][:1]:
        f = _factor(opp_def_sum, league_def_avg, "pass_yards_pg")
        out.append({"player": r["player"], "pos": "QB", "passing_yards": _baseline([g["yards"] for g in r["log"]], f),
                    "pass_attempts": _baseline([g["att"] for g in r["log"]], 1.0)})
    return {"status": "BASELINE_RESEARCH_ONLY",
            "method": "The player's own games in the window (recency-weighted mean; percentiles of his game log), scaled by half of the "
                      "opponent's allowed-per-game deviation from league average for that position, capped at +/-15%. "
                      "This is NOT the three-model consensus and has not been validated against prices. Injury replacements, "
                      "role changes and game script are not applied: the analyst must adjust for them.",
            "players": out}


def team_projection(home, away, season, week, pbp_path, spread_home, total, n=20000):
    """Period-engine score distribution (research only). spread_home is the home team's line (negative = favourite)."""
    try:
        sys.path.insert(0, str(ROOT / "core" / "period_engine_v0"))
        from reconstruct import load_pbp, period_table_from_pbp, as_of_mask, resolve_pbp_path
        from monte_carlo import simulate_game, raw_probs_from_sim
        parts = [period_table_from_pbp(load_pbp(pbp_path))]
        prior = resolve_pbp_path(ROOT / "core" / "period_engine_v0" / "data" / f"play_by_play_{season - 1}.parquet")
        if Path(prior).exists():
            parts.append(period_table_from_pbp(load_pbp(prior)))
        hist = pd.concat(parts, ignore_index=True)
        asof = hist[as_of_mask(hist, season, week)]
        out = {"status": "RESEARCH_ONLY_NOT_VALIDATED", "engine": "core/period_engine_v0", "trials": n,
               "history_games": int(len(asof)), "includes_prior_season": bool(Path(prior).exists()), "samplers": {}}
        for mode in ("matchup_pair", "independent"):
            sim = simulate_game(asof, home, away, n=n, seed=20261111 + week, sampling=mode)
            if sim.get("error"):
                out["samplers"][mode] = {"error": sim["error"]}
                continue
            s, a = sim["summaries"], sim["arrays"]
            fg_h, fg_a = a["fg_home"], a["fg_away"]
            row = {"home_points": round(s["fg"]["home_mean"], 1), "away_points": round(s["fg"]["away_mean"], 1),
                   "home_margin": round(s["fg"]["margin_home_mean"], 1), "total": round(s["fg"]["total_mean"], 1),
                   "home_win": round(float((fg_h > fg_a).mean()), 3), "away_win": round(float((fg_h < fg_a).mean()), 3),
                   "total_p10_p50_p90": [float(np.percentile(fg_h + fg_a, q)) for q in (10, 50, 90)],
                   "first_half": {"home": round(s["h1"]["home_mean"], 1), "away": round(s["h1"]["away_mean"], 1)},
                   "by_quarter": {q: {"home": round(s[q]["home_mean"], 1), "away": round(s[q]["away_mean"], 1)} for q in ("q1", "q2", "q3", "q4")}}
            if spread_home is not None and not pd.isna(spread_home):
                r = raw_probs_from_sim(sim, period="fg", market="spread_2way", line=float(spread_home), side="home")
                row["home_covers_market_spread"] = None if r["p_win_decisive"] is None else round(r["p_win_decisive"], 3)
            if total is not None and not pd.isna(total):
                r = raw_probs_from_sim(sim, period="fg", market="total_2way", line=float(total), side="over")
                row["over_market_total"] = None if r["p_win_decisive"] is None else round(r["p_win_decisive"], 3)
            out["samplers"][mode] = row
        out["note"] = ("Bootstrap of each team's real quarter scores. 'matchup_pair' includes the opponent's defence; 'independent' is the "
                       "legacy sampler. No injuries, no weather, no fitted calibration. On 2026 weeks 1-8 neither sampler beat the market; "
                       "treat probabilities near the market number as no information.")
        return out
    except Exception as exc:
        return {"status": f"UNAVAILABLE: {type(exc).__name__}: {str(exc)[:160]}"}


# ------------------------------------------------------------------ edges
EDGE_PAIRS = [  # (offence metric, defence metric, plain label)
    ("wr_rec_yards_pg", "wr_rec_yards_pg", "wide receiver yards"), ("te_rec_yards_pg", "te_rec_yards_pg", "tight end yards"),
    ("rb_rec_yards_pg", "rb_rec_yards_pg", "running back receiving yards"), ("rb_rush_yards_pg", "rb_rush_yards_pg", "running back rushing yards"),
    ("explosive_pass_pg", "explosive_pass_pg", "explosive passes (20+)"), ("explosive_rush_pg", "explosive_rush_pg", "explosive runs (15+)"),
    ("pass_yards_pg", "pass_yards_pg", "passing yards"), ("points_pg", "points_pg", "points"),
    ("third_down_rate", "third_down_rate", "third-down conversions"), ("red_zone_td_rate", "red_zone_td_rate", "red-zone touchdowns"),
    ("sack_rate", "sack_rate", "sacks (pass protection vs pass rush)"), ("pressure_rate", "pressure_rate", "pressure (sacks + hits)"),
]


def edges(off_team, off_sum, off_rank, def_team, def_sum, def_rank, n_teams=32):
    """Where a top-10 unit meets a bottom-10 unit. Ranks are 1 = best at its own job, over each team's window."""
    out = []
    top, bottom = 10, n_teams - 9
    for ok, dk, label in EDGE_PAIRS:
        o, d = off_rank.get(ok), def_rank.get(dk)
        if not o or not d:
            continue
        row = {"area": label, "is_rate": ok.endswith("_rate"), "offense_value": off_sum.get(ok), "offense_rank": o["rank"],
               "defense_value": def_sum.get(dk), "defense_rank": d["rank"], "league_avg": d["league_avg"],
               "why": f"{off_team} offence ranks {o['rank']} of {o['of']}, {def_team} defence ranks {d['rank']} of {d['of']} (1 = best at its own job)"}
        if o["rank"] <= top and d["rank"] >= bottom:
            out.append({**row, "edge": f"{off_team} OFFENCE ADVANTAGE"})
        elif o["rank"] >= bottom and d["rank"] <= top:
            out.append({**row, "edge": f"{def_team} DEFENCE ADVANTAGE"})
        elif d["rank"] >= bottom:
            out.append({**row, "edge": f"{def_team} DEFENCE WEAK SPOT"})
        elif d["rank"] <= 5:
            out.append({**row, "edge": f"{def_team} DEFENCE STRENGTH"})
        elif o["rank"] <= 5:
            out.append({**row, "edge": f"{off_team} OFFENCE STRENGTH"})
        elif o["rank"] >= n_teams - 4:
            out.append({**row, "edge": f"{off_team} OFFENCE WEAK SPOT"})
    return out


# ------------------------------------------------------------------ the packet
def build(game, *, data, window=8, espn=None, pbp_path=None, sources=None, books=None, weather=None):
    """game: a row of the nflverse schedule. data: dict of DataFrames (pbp prepared as 'plays')."""
    season, week, home, away = int(game.season), int(game.week), game.home_team, game.away_team
    p, games = data["plays"], data["games"]
    done = games[(games.season == season) & games.home_score.notna() & (games.week < week)]
    p = p[p.game_id.isin(done.game_id)]
    tg_def, tg_off = M.team_games(p, done, "defteam"), M.team_games(p, done, "posteam")
    lg_def, lg_off = M.league_table(tg_def, window), M.league_table(tg_off, window)
    lg_def_avg = {k: float(pd.to_numeric(lg_def[k], errors="coerce").mean()) for k in lg_def.columns if k not in ("weeks",)
                  and pd.to_numeric(lg_def[k], errors="coerce").notna().any()}
    teams = {}
    for team, opp in ((away, home), (home, away)):
        d_n, o_n = M.last_n(tg_def[tg_def.team == team], window), M.last_n(tg_off[tg_off.team == team], window)
        if not len(d_n):
            teams[team] = {"status": "NO_COMPLETED_GAMES_THIS_SEASON"}
            continue
        gids = list(d_n.game_id)
        weeks = [int(w) for w in d_n.week]
        dc = depth_chart(team, data.get("depth_charts"))
        starters = dc.pop("starter_ids")
        d_sum, o_sum = M.summarize(d_n), M.summarize(o_n)
        players = M.offense_players(p, team, gids, done)
        shares = snap_shares(team, data.get("snap_counts"), weeks)
        teams[team] = {
            "window": {"games": len(gids), "weeks": weeks, "requested": window},
            "defense": {"allowed": d_sum, "rank": M.ranks(lg_def, team, defense=True), "by_game": M.game_log(d_n),
                        "top_lines_allowed": M.top_lines_allowed(p, team, gids, done),
                        "run_defense_by_direction": M.run_direction(p, team, gids, "defteam"),
                        "defenders": defenders(team, data.get("pfr_def"), weeks)},
            "offense": {"produced": o_sum, "rank": M.ranks(lg_off, team, defense=False), "by_game": M.game_log(o_n),
                        "run_game_by_direction": M.run_direction(p, team, gids, "posteam"), "players": players,
                        "offense_snap_share": {k: round(v, 3) for k, v in sorted(shares.items(), key=lambda kv: -kv[1])[:22]}},
            "formation_zone_splits": SP.team_splits(p, team, list(o_n.game_id), gids),
            "depth_chart": dc,
            "injuries": injuries_for(team, week, data.get("injuries"), espn, starters),
            "roster_moves": roster_moves(team, data["rosters"], week),
        }
    matchup = {}
    for off, dfn in ((away, home), (home, away)):
        if "offense" not in teams[off] or "defense" not in teams[dfn]:
            continue
        o, d = teams[off]["offense"], teams[dfn]["defense"]
        matchup[f"{off}_offense_vs_{dfn}_defense"] = {
            "edges": edges(off, o["produced"], o["rank"], dfn, d["allowed"], d["rank"], n_teams=len(lg_def)),
            "player_baselines": player_baselines(o["players"], d["allowed"], lg_def_avg)}
    spread_home = None if pd.isna(game.spread_line) else -float(game.spread_line)     # nflverse: positive = home favoured
    total = None if pd.isna(game.total_line) else float(game.total_line)
    packet = {
        "schema": SCHEMA, "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "projection_ready": False, "status": "RESEARCH_ONLY_NOT_BETTING_ADVICE",
        "game": {"game_id": game.game_id, "season": season, "week": week, "away": away, "home": home, "date": str(game.gameday),
                 "weekday": game.weekday, "kickoff_et": str(game.gametime), "slot": slot_name(game.weekday, game.gametime),
                 "site": game.location, "stadium_id": game.stadium_id, "roof": game.roof or None, "surface": game.surface or None,
                 "away_rest_days": int(game.away_rest), "home_rest_days": int(game.home_rest), "division_game": bool(game.div_game),
                 "listed_qbs": {away: game.away_qb_name, home: game.home_qb_name}, "coaches": {away: game.away_coach, home: game.home_coach}},
        "market": {"source": "nflverse schedule (consensus line at retrieval; not a timestamped book quote)",
                   "home_spread": spread_home, "total": total,
                   "moneyline": {away: None if pd.isna(game.away_moneyline) else float(game.away_moneyline),
                                 home: None if pd.isna(game.home_moneyline) else float(game.home_moneyline)}},
        "books": books or {"status": "NOT_REQUESTED"},
        "weather": weather or {"status": "NOT_REQUESTED"},
        "teams": teams, "matchup": matchup,
        "team_projection": team_projection(home, away, season, week, pbp_path, spread_home, total) if pbp_path else {"status": "SKIPPED"},
        "sources": sources or {},
    }
    prop_check(packet)
    packet["phase_ledger"] = phase_ledger(packet)
    return packet


def _short(name):
    """'Zay Flowers' -> 'Z.Flowers' (the play-by-play name form)."""
    parts = str(name).replace(".", "").split()
    return f"{parts[0][0]}.{' '.join(parts[1:])}" if len(parts) > 1 else str(name)


def prop_check(pk):
    """Put each book prop line beside the player's own scaled game log. Counts only: no model probability is claimed."""
    props = {k: v for k, v in (pk.get("books", {}).get("markets") or {}).items() if "|" in k}
    if not props:
        return
    logs = {}
    for side in pk["matchup"].values():
        for r in side["player_baselines"]["players"]:
            logs[r["player"].replace(" ", "").lower()] = r
    rows = []
    for label, m in props.items():
        stat, player = label.split("|", 1)
        r = logs.get(_short(player).replace(" ", "").lower())
        b = (r or {}).get(stat)
        ref = m["reference"] if m["reference"].get("book") else None
        for book, q in m["books"].items():
            if book == "pinnacle" and len(m["books"]) > 1:
                continue
            row = {"player": player, "stat": stat, "book": book, "line": q["line"], "prices": q["prices"], "no_vig_over": q["no_vig"]["Over"],
                   "sharp_no_vig_over": ref["no_vig"]["Over"] if ref and ref["line"] == q["line"] else None,
                   "baseline_weighted_mean": b["weighted_mean"] if b else None, "baseline_median": b["p50"] if b else None,
                   "baseline_games": b["games"] if b else None,
                   "baseline_minus_line": round(b["weighted_mean"] - q["line"], 1) if b and q["line"] is not None else None}
            rows.append(row)
    pk["books"]["prop_check"] = {
        "note": "baseline_minus_line is the research baseline against the book line. It is NOT an edge: the baseline has not beaten "
                "the market in testing, uses 3-8 games, and ignores injuries and script. Use it to find props worth a full review.",
        "rows": sorted(rows, key=lambda r: -abs(r["baseline_minus_line"] or 0))}


def phase_ledger(pk):
    """The 15-phase ledger (research/WEEK9_PHASE_LEDGER_*): what this packet filled automatically and what it could not."""
    t = [v for v in pk["teams"].values() if "defense" in v]
    ok = len(t) == 2
    src = pk.get("sources", {})
    has = lambda k: str(src.get(k, {}).get("status", "")).startswith(("OK", "OFFLINE_CACHE"))
    inj = ok and all(x["injuries"]["official_report_status"] == "OK" for x in t)
    live = ok and all(str(x["injuries"]["espn_live_status"]).startswith("OK") for x in t)
    charted = ok and all((x["defense"]["allowed"].get("dropbacks_charted") or 0) > 0 for x in t)
    L = [
        (1, "Slate, schedule, venue", "AUTO", "Schedule, kickoff, site, roof, surface, rest days, listed QBs."),
        (2, "Player identity and position", "AUTO" if ok else "BLOCKED", "Positions from weekly rosters (GSIS IDs). Name-only joins are used for snap counts and PFR defenders."),
        (3, "Verified player game history", "AUTO" if ok else "BLOCKED", "Per-game logs for QBs, receivers and rushers over the window, from play-by-play."),
        (4, "Role, snaps, routes, opportunity", "PARTIAL", "Target share, air-yards share, carry share, red-zone looks, snap share. Routes run and route participation are NOT available."),
        (5, "Team offense/defense baselines", "AUTO" if ok else "BLOCKED", "Allowed and produced tables with league ranks and game-by-game trends."),
        (6, "Opponent context and game script", "PARTIAL", "Market spread/total, neutral pass rate, pace. The script call itself is the analyst's."),
        (7, "Coverage structure and shell", "PARTIAL" if charted else "BLOCKED", "Blitz and play-action rates from FTN charting. Man/zone and shell are NOT in any free source here."),
        (8, "Defender assignment and explosive allowance", "PARTIAL" if has("pfr_def") else "BLOCKED", "Per-defender targets/yards allowed (PFR) and explosive plays allowed. Who covers whom is NOT known."),
        (9, "QB pressure, blitz, scramble", "PARTIAL", "Sack rate, sacks + QB hits rate (a floor on pressure), blitz rate, scrambles."),
        (10, "Offensive line, pass rush, coaching", "PARTIAL", "Depth-chart line, pressure allowed, run yards by direction, pass-rush leaders. No line grades."),
        (11, "Injury and depth chart", "AUTO" if inj and live else ("PARTIAL" if inj or live else "PENDING"), "Official weekly report and depth chart; ESPN live list when reachable. Recent roster arrivals/departures."),
        (12, "Weather, roof, travel", {"OK": "AUTO", "INDOOR": "AUTO"}.get(str((pk.get("weather") or {}).get("status")), "PARTIAL"),
         "Roof, surface, rest days, site; National Weather Service kickoff forecast: " + str((pk.get("weather") or {}).get("status", "NOT_REQUESTED"))[:80] + "."),
        (13, "Timestamped book prices", "PARTIAL" if (pk.get("books") or {}).get("markets") else "BLOCKED",
         ("Pinnacle / DraftKings / FanDuel prices with no-vig and first-seen-to-now movement"
          + (", player props" if (pk.get("books") or {}).get("prop_check") else ", no player props in this run")
          + ". No FTN model, no true opening line.") if (pk.get("books") or {}).get("markets")
         else "No book prices: " + str((pk.get("books") or {}).get("status", "NOT_REQUESTED"))[:90] + ". Only the schedule's consensus spread/total."),
        (14, "Projection and simulation", "PARTIAL_RESEARCH_ONLY", "Period-engine team scores; player baselines. Not the three-model consensus; not validated."),
        (15, "Final inactive pregame freeze", "PENDING", "Inactives post about 90 minutes before kickoff. Re-run or check them by hand before any final call."),
    ]
    return [{"phase": n, "name": name, "status": st, "detail": d} for n, name, st, d in L]
