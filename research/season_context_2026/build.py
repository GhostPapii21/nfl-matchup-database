"""2026 season context database, Weeks 1 to the last completed week. Sources: nflverse play-by-play, schedules,
snap counts and injury reports (pregame/.cache, refreshed by pregame.sources.fetch_all).

Writes to research/season_context_2026/:
  games.csv        one row per game: quarter-by-quarter scores, quarter/half/game winners, weather (rain/snow highlighted),
                   indoor/outdoor, international site, rest (bye / short week), coaches, QB change during the game.
  team_games.csv   one row per team per game: result, quarters won, halves, comeback / blown lead, opponent defense
                   tier (top 5 / bottom 5, season and as-of before the game), key players out and the share of offense
                   they carried, injury flag, first-half vs second-half changes (the coaching-adjustment read), off bye,
                   after an international trip.
  player_splits.csv  every WR/TE/RB with 3+ games: averages overall and by context (vs top-5 / bottom-5 defense, bad
                   weather, indoor, off bye, after an international game, key teammate out, home/away).
  team_profile.csv   per team: record by context (vs top-5, bad weather, with key players out, off bye, after an
                   international trip), quarter and half win rates, second-half adjustment rate.
  audit.json, AUDIT.md   completeness checks (every game present, quarters sum to the final, every team's games) and
                   flags (missing NFL game books by week).

Definitions (all stated so they can be checked):
  defense tier    rank of EPA per play allowed (lower = better); top 5 = ranks 1-5, bottom 5 = ranks 28-32. Pass and run
                  defense ranked separately for player splits. 'asof' ranks use only games before that week.
  bad weather     outdoor and (rain/snow/showers/drizzle/sleet/storm in the weather text, or wind >= 15 mph, or temp <= 32 F)
  key player      offense: averaged 60%+ of offensive snaps in games played (min 3 games) and is a QB, or a top-2 WR,
                  top TE, or top RB by touches+targets on his team; defense: averaged 70%+ of defensive snaps (min 3).
                  'Out' = no snaps that game after having played earlier in the season.
  injury factor   team lost and (starting QB out, or QB changed mid-game, or out players carried 25%+ of the team's
                  targets+carries, or 3+ key defenders out).
  adjustment      second half minus first half for offensive EPA/play, success rate and pass rate, and defensive EPA/play
                  allowed. 'Big' = a change of 0.20+ EPA/play; pass-rate shifts of 12+ points are labelled.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
C = ROOT / "pregame" / ".cache"
OUT = Path(__file__).resolve().parent
GAMEBOOKS = ROOT / "data" / "gamebooks" / "2026"
SEASON = 2026
WET = re.compile(r"rain|shower|drizzle|snow|sleet|storm|thunder|flurr", re.I)


def r2(x, n=3):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), n)


def load():
    p = pd.read_parquet(C / f"play_by_play_{SEASON}.parquet")
    g = pd.read_parquet(C / "games.parquet")
    g = g[(g.season == SEASON) & (g.game_type == "REG")].copy()
    full = [w for w, x in g.groupby("week") if x.home_score.notna().all()]
    g = g[g.week <= max(full)].copy()                      # completed weeks only
    p = p[p.game_id.isin(g.game_id)]
    s = pd.read_parquet(C / f"snap_counts_{SEASON}.parquet")
    s = s[s.game_id.isin(g.game_id)]
    inj = pd.read_parquet(C / f"injuries_{SEASON}.parquet")
    return p, g, s, inj


# ----------------------------------------------------------------------------------------------- quarters and halves
def quarter_scores(p, g):
    rows = []
    for gid, x in p.groupby("game_id"):
        gm = g[g.game_id == gid].iloc[0]
        end = x.groupby("qtr")[["total_home_score", "total_away_score"]].max().sort_index()
        prev_h = prev_a = 0
        q = {}
        for qt, r in end.iterrows():
            h, a = int(r.total_home_score), int(r.total_away_score)
            q[int(qt)] = (h - prev_h, a - prev_a)
            prev_h, prev_a = max(prev_h, h), max(prev_a, a)
        row = {"game_id": gid}
        for qt in (1, 2, 3, 4, 5):
            hq, aq = q.get(qt, (0, 0) if qt < 5 else (None, None))
            row[f"home_q{qt if qt < 5 else 'ot'}"] = hq
            row[f"away_q{qt if qt < 5 else 'ot'}"] = aq
        row["pbp_final_home"], row["pbp_final_away"] = prev_h, prev_a
        row["final_matches_schedule"] = prev_h == int(gm.home_score) and prev_a == int(gm.away_score)
        rows.append(row)
    return pd.DataFrame(rows)


def _winner(h, a, home, away):
    if h is None or a is None:
        return None
    return home if h > a else away if a > h else "TIE"


def qb_change(p):
    """Starting QB replaced during the game: the team's first-half main passer has no dropbacks after some point and
    another QB has 5+ dropbacks."""
    out = {}
    d = p[(p.qb_dropback == 1) & p.passer_player_id.notna()]
    for (gid, team), x in d.groupby(["game_id", "posteam"]):
        x = x.sort_values("play_id")
        first = x.passer_player_name.iloc[0]
        others = x[x.passer_player_name != first].passer_player_name.value_counts()
        if len(others) and others.iloc[0] >= 5:
            last_first = x[x.passer_player_name == first].qtr.max()
            out[(gid, team)] = f"{first} -> {others.index[0]} (Q{int(last_first)})"
    return out


# ----------------------------------------------------------------------------------------------- defense tiers
def defense_ranks(p, g):
    plays = p[p.play_type.isin(["pass", "run"]) & p.epa.notna()]
    weeks = sorted(g.week.unique())
    season = {}
    for kind, f in (("all", plays), ("pass", plays[plays.play_type == "pass"]), ("run", plays[plays.play_type == "run"])):
        season[kind] = f.groupby("defteam").epa.mean().rank(method="first").astype(int).to_dict()
    asof = {}
    for w in weeks:
        f = plays[plays.week < w]
        asof[w] = f.groupby("defteam").epa.mean().rank(method="first").astype(int).to_dict() if len(f) else {}
    return season, asof


def tier(rank):
    if rank is None or (isinstance(rank, float) and np.isnan(rank)):
        return None
    return "top5" if rank <= 5 else "bottom5" if rank >= 28 else "middle"


# ----------------------------------------------------------------------------------------------- key players out
def key_players(p, g, s):
    s = s.copy()
    usage = p[p.play_type.isin(["pass", "run"])]
    tgt = usage[usage.receiver_player_name.notna()].groupby(["posteam", "receiver_player_name"]).size()
    car = usage[usage.rusher_player_name.notna()].groupby(["posteam", "rusher_player_name"]).size()
    team_tot = usage.groupby("posteam").apply(lambda x: x.receiver_player_name.notna().sum() + x.rusher_player_name.notna().sum())
    played = s[(s.offense_snaps > 0) | (s.defense_snaps > 0)]
    avg = played.groupby(["team", "player", "position"]).agg(off=("offense_pct", "mean"), de=("defense_pct", "mean"), n=("game_id", "nunique"),
                                                             first_week=("week", "min")).reset_index()
    keys = []
    for team, t in avg.groupby("team"):
        off = t[(t.off >= 0.6) & (t.n >= 3)].copy()

        def share(name):
            short = _short(name)
            v = sum(tgt.get((team, k), 0) + car.get((team, k), 0) for k in {short, name})
            return v / max(team_tot.get(team, 1), 1)
        off["share"] = off.player.map(share)
        pick = pd.concat([off[off.position == "QB"].nlargest(1, "off"), off[off.position == "WR"].nlargest(2, "share"),
                          off[off.position == "TE"].nlargest(1, "share"), off[off.position == "RB"].nlargest(1, "share")])
        for r in pick.itertuples():
            keys.append({"team": team, "player": r.player, "position": r.position, "side": "offense", "share": r.share, "first_week": r.first_week})
        de = t[(t.de >= 0.7) & (t.n >= 3)]
        for r in de.itertuples():
            keys.append({"team": team, "player": r.player, "position": r.position, "side": "defense", "share": 0.0, "first_week": r.first_week})
    keys = pd.DataFrame(keys)
    in_game = set(zip(played.game_id, played.team, played.player))
    out = {}
    for r in g.itertuples():
        for team in (r.home_team, r.away_team):
            k = keys[(keys.team == team) & (keys.first_week < r.week)]
            miss = k[[(r.game_id, team, pl) not in in_game for pl in k.player]]
            out[(r.game_id, team)] = miss
    return keys, out


def _short(name):
    parts = str(name).split()
    return f"{parts[0][0]}.{' '.join(parts[1:])}" if len(parts) > 1 else name


# ----------------------------------------------------------------------------------------------- halves (adjustments)
def half_splits(p):
    plays = p[p.play_type.isin(["pass", "run"]) & p.epa.notna() & (p.qtr <= 4)]
    plays = plays.assign(half=np.where(plays.qtr <= 2, 1, 2), is_pass=(plays.play_type == "pass").astype(int))
    o = plays.groupby(["game_id", "posteam", "half"]).agg(epa=("epa", "mean"), sr=("success", "mean"), pr=("is_pass", "mean"), n=("epa", "size"))
    d = plays.groupby(["game_id", "defteam", "half"]).agg(depa=("epa", "mean"))
    return o, d


# ----------------------------------------------------------------------------------------------- main build
def build():
    p, g, s, inj = load()
    qs = quarter_scores(p, g)
    g = g.merge(qs, on="game_id", how="left")
    wx_text = p.groupby("game_id").weather.agg(lambda x: next((v for v in x if isinstance(v, str) and v.strip()), None))
    g["weather_text"] = g.game_id.map(wx_text)
    g["indoor"] = g.roof.isin(["dome", "closed"])
    g["rain_or_snow"] = (~g.indoor) & g.weather_text.fillna("").str.contains(WET)
    g["bad_weather"] = (~g.indoor) & (g.rain_or_snow | (g.wind.fillna(0) >= 15) | (g.temp.fillna(60) <= 32))
    g["international"] = g.location.eq("Neutral")
    qbc = qb_change(p)
    season_rank, asof_rank = defense_ranks(p, g)
    keys, missing = key_players(p, g, s)
    o, d = half_splits(p)

    games, tg = [], []
    for r in g.sort_values(["week", "gameday", "game_id"]).itertuples():
        H = {q: getattr(r, f"home_q{q}") for q in (1, 2, 3, 4)}
        A = {q: getattr(r, f"away_q{q}") for q in (1, 2, 3, 4)}
        h1, a1 = H[1] + H[2], A[1] + A[2]
        h2, a2 = H[3] + H[4], A[3] + A[4]
        row = {"game_id": r.game_id, "week": r.week, "date": r.gameday, "away": r.away_team, "home": r.home_team,
               "away_score": int(r.away_score), "home_score": int(r.home_score), "winner": _winner(r.home_score, r.away_score, r.home_team, r.away_team),
               "overtime": bool(r.overtime)}
        for q in (1, 2, 3, 4):
            row[f"q{q}"] = f"{r.away_team} {A[q]}-{H[q]} {r.home_team}"
            row[f"q{q}_winner"] = _winner(H[q], A[q], r.home_team, r.away_team)
        row["ot_score"] = None if pd.isna(r.home_qot) else f"{r.away_team} {int(r.away_qot)}-{int(r.home_qot)} {r.home_team}"
        row.update(first_half=f"{r.away_team} {a1}-{h1} {r.home_team}", first_half_winner=_winner(h1, a1, r.home_team, r.away_team),
                   second_half=f"{r.away_team} {a2}-{h2} {r.home_team}", second_half_winner=_winner(h2, a2, r.home_team, r.away_team),
                   roof=r.roof, indoor=bool(r.indoor), temp=r.temp, wind=r.wind, weather=r.weather_text,
                   rain_or_snow=bool(r.rain_or_snow), bad_weather=bool(r.bad_weather),
                   international=bool(r.international), stadium=r.stadium, away_rest=r.away_rest, home_rest=r.home_rest,
                   away_coach=r.away_coach, home_coach=r.home_coach,
                   qb_change=", ".join(f"{t}: {qbc[(r.game_id, t)]}" for t in (r.away_team, r.home_team) if (r.game_id, t) in qbc) or None,
                   quarters_sum_to_final=bool(r.final_matches_schedule))
        games.append(row)
        for team, opp, side in ((r.home_team, r.away_team, "home"), (r.away_team, r.home_team, "away")):
            pf, pa = (int(r.home_score), int(r.away_score)) if side == "home" else (int(r.away_score), int(r.home_score))
            mine, theirs = (H, A) if side == "home" else (A, H)
            f1, t1, f2, t2 = mine[1] + mine[2], theirs[1] + theirs[2], mine[3] + mine[4], theirs[3] + theirs[4]
            miss = missing.get((r.game_id, team), pd.DataFrame())
            miss_off = miss[miss.side == "offense"] if len(miss) else miss
            miss_def = miss[miss.side == "defense"] if len(miss) else miss
            qb_out = bool(len(miss_off) and (miss_off.position == "QB").any())
            off_share = float(miss_off.share.sum()) if len(miss_off) else 0.0
            won = pf > pa
            prev = [x for x in tg if x["team"] == team]
            rest = r.home_rest if side == "home" else r.away_rest
            oh = {h: o.loc[(r.game_id, team, h)] if (r.game_id, team, h) in o.index else None for h in (1, 2)}
            dh = {h: d.loc[(r.game_id, team, h)] if (r.game_id, team, h) in d.index else None for h in (1, 2)}
            adj = {}
            if oh[1] is not None and oh[2] is not None:
                adj = {"off_epa_h1": r2(oh[1].epa), "off_epa_h2": r2(oh[2].epa), "off_epa_change": r2(oh[2].epa - oh[1].epa),
                       "success_change": r2(oh[2].sr - oh[1].sr), "pass_rate_h1": r2(oh[1].pr), "pass_rate_h2": r2(oh[2].pr),
                       "pass_rate_change": r2(oh[2].pr - oh[1].pr)}
            if dh[1] is not None and dh[2] is not None:
                adj["def_epa_allowed_change"] = r2(dh[2].depa - dh[1].depa)
            notes = []
            if adj.get("off_epa_change") is not None and adj["off_epa_change"] >= 0.20:
                notes.append("offense much better after halftime")
            if adj.get("off_epa_change") is not None and adj["off_epa_change"] <= -0.20:
                notes.append("offense much worse after halftime")
            if adj.get("def_epa_allowed_change") is not None and adj["def_epa_allowed_change"] <= -0.20:
                notes.append("defense tightened after halftime")
            if adj.get("def_epa_allowed_change") is not None and adj["def_epa_allowed_change"] >= 0.20:
                notes.append("defense got worse after halftime")
            if adj.get("pass_rate_change") is not None and abs(adj["pass_rate_change"]) >= 0.12:
                notes.append(f"pass rate {'up' if adj['pass_rate_change'] > 0 else 'down'} {abs(adj['pass_rate_change']) * 100:.0f} pts after halftime")
            qbch = qbc.get((r.game_id, team))
            injury_factor = (not won) and (qb_out or bool(qbch) or off_share >= 0.25 or len(miss_def) >= 3)
            tg.append({"game_id": r.game_id, "week": r.week, "team": team, "opp": opp, "home_away": side, "points_for": pf, "points_against": pa,
                       "result": "W" if won else "L" if pf < pa else "T", "margin": pf - pa,
                       "quarters_won": sum(mine[q] > theirs[q] for q in (1, 2, 3, 4)), "quarters_lost": sum(mine[q] < theirs[q] for q in (1, 2, 3, 4)),
                       "won_first_half": f1 > t1, "won_second_half": f2 > t2, "halftime_margin": f1 - t1,
                       "comeback_win": won and f1 < t1, "blew_halftime_lead": (not won) and f1 > t1,
                       "opp_def_rank_season": season_rank["all"].get(opp), "opp_def_tier_season": tier(season_rank["all"].get(opp)),
                       "opp_def_rank_asof": asof_rank.get(r.week, {}).get(opp), "opp_def_tier_asof": tier(asof_rank.get(r.week, {}).get(opp)),
                       "indoor": bool(r.indoor), "bad_weather": bool(r.bad_weather), "rain_or_snow": bool(r.rain_or_snow),
                       "international": bool(r.international), "after_international": bool(prev and prev[-1]["international"]),
                       "rest_days": rest, "off_bye": bool(rest is not None and rest >= 13), "short_week": bool(rest is not None and rest <= 5),
                       "key_offense_out": ", ".join(f"{x.player} ({x.position})" for x in miss_off.itertuples()) or None,
                       "key_offense_out_share": r2(off_share), "starting_qb_out": qb_out, "qb_change_in_game": qbch,
                       "key_defense_out": ", ".join(f"{x.player} ({x.position})" for x in miss_def.itertuples()) or None,
                       "key_defense_out_count": int(len(miss_def)), "injury_factor_in_loss": injury_factor,
                       **adj, "adjustment_notes": "; ".join(notes) or None,
                       "coach": r.home_coach if side == "home" else r.away_coach})
    games, tg = pd.DataFrame(games), pd.DataFrame(tg)
    return p, g, s, keys, games, tg, season_rank


def player_splits(p, tg, season_rank, keys):
    plays = p[p.play_type.isin(["pass", "run"])]
    rec = plays[plays.receiver_player_name.notna()].groupby(["game_id", "posteam", "receiver_player_name"]).agg(
        targets=("pass_attempt", "size"), rec=("complete_pass", "sum"), rec_yds=("receiving_yards", lambda x: x.fillna(0).sum())).reset_index().rename(
        columns={"receiver_player_name": "player"})
    ru = plays[plays.rusher_player_name.notna()].groupby(["game_id", "posteam", "rusher_player_name"]).agg(
        carries=("rush_attempt", "size"), rush_yds=("rushing_yards", lambda x: x.fillna(0).sum())).reset_index().rename(columns={"rusher_player_name": "player"})
    pg = rec.merge(ru, on=["game_id", "posteam", "player"], how="outer").fillna(0).rename(columns={"posteam": "team"})
    pg["scrim_yds"] = pg.rec_yds + pg.rush_yds
    pg = pg.merge(tg, on=["game_id", "team"], how="left")
    pg["pass_def_tier"] = pg.opp.map(lambda t: tier(season_rank["pass"].get(t)))
    pg["run_def_tier"] = pg.opp.map(lambda t: tier(season_rank["run"].get(t)))
    pg["teammate_key_out"] = [isinstance(ko, str) and any(_short(k.split(" (")[0]) != pl for k in ko.split(", "))
                              for ko, pl in zip(pg.key_offense_out, pg.player)]
    agg = []
    for (team, pl), x in pg.groupby(["team", "player"]):
        if len(x) < 3 or (x.targets.sum() + x.carries.sum()) < 15:
            continue
        row = {"team": team, "player": pl, "games": len(x), "targets_pg": r2(x.targets.mean(), 1), "rec_pg": r2(x.rec.mean(), 1),
               "rec_yds_pg": r2(x.rec_yds.mean(), 1), "carries_pg": r2(x.carries.mean(), 1), "rush_yds_pg": r2(x.rush_yds.mean(), 1),
               "games_80_scrim": int((x.scrim_yds >= 80).sum())}
        conds = {"vs_top5_pass_def": x.pass_def_tier == "top5", "vs_bottom5_pass_def": x.pass_def_tier == "bottom5",
                 "vs_top5_run_def": x.run_def_tier == "top5", "vs_bottom5_run_def": x.run_def_tier == "bottom5",
                 "bad_weather": x.bad_weather == True, "indoor": x.indoor == True, "off_bye": x.off_bye == True,  # noqa: E712
                 "after_international": x.after_international == True, "key_teammate_out": x.teammate_key_out,  # noqa: E712
                 "home": x.home_away == "home", "away": x.home_away == "away"}
        for k, m in conds.items():
            y = x[m.fillna(False).astype(bool)]
            row[f"{k}_n"] = len(y)
            row[f"{k}_rec_yds"] = r2(y.rec_yds.mean(), 1) if len(y) else None
            row[f"{k}_rush_yds"] = r2(y.rush_yds.mean(), 1) if len(y) else None
            row[f"{k}_targets"] = r2(y.targets.mean(), 1) if len(y) else None
        agg.append(row)
    return pd.DataFrame(agg), pg


def team_profile(tg):
    rows = []
    for team, x in tg.groupby("team"):
        def rec(m):
            y = x[m]
            return f"{(y.result == 'W').sum()}-{(y.result == 'L').sum()}" + (f"-{(y.result == 'T').sum()}" if (y.result == "T").any() else "")
        rows.append({"team": team, "record": rec(x.result.notna()),
                     "vs_top5_def": rec(x.opp_def_tier_season == "top5"), "vs_bottom5_def": rec(x.opp_def_tier_season == "bottom5"),
                     "bad_weather": rec(x.bad_weather), "indoor": rec(x.indoor), "with_key_offense_out": rec(x.key_offense_out.notna()),
                     "starting_qb_out_or_changed": rec(x.starting_qb_out | x.qb_change_in_game.notna()),
                     "off_bye": rec(x.off_bye), "after_international": rec(x.after_international), "short_week": rec(x.short_week),
                     "avg_quarters_won": r2(x.quarters_won.mean(), 2),
                     "first_half_win_rate": r2(x.won_first_half.mean(), 2), "second_half_win_rate": r2(x.won_second_half.mean(), 2),
                     "comeback_wins": int(x.comeback_win.sum()), "blown_halftime_leads": int(x.blew_halftime_lead.sum()),
                     "avg_off_epa_change_h2": r2(x.off_epa_change.mean()), "avg_def_epa_allowed_change_h2": r2(x.def_epa_allowed_change.mean()),
                     "injury_factor_losses": int(x.injury_factor_in_loss.sum())})
    return pd.DataFrame(rows)


def audit(g, games, tg, p):
    sched = pd.read_parquet(C / "games.parquet")
    sched = sched[(sched.season == SEASON) & (sched.game_type == "REG")]
    done_weeks = sorted(sched[sched.home_score.notna()].week.unique())
    last_full = max(w for w in done_weeks if sched[(sched.week == w)].home_score.notna().all())
    flags, weeks = [], []
    for w in range(1, last_full + 1):
        sw = sched[sched.week == w]
        pb = set(p[p.week == w].game_id)
        gb_dir = GAMEBOOKS / f"wk{w:02d}"
        gb = {d.name for d in gb_dir.iterdir() if d.is_dir() and (d / "parsed").exists()} if gb_dir.exists() else set()
        miss_pbp = sorted(set(sw.game_id) - pb)
        miss_gb = sorted(set(sw.game_id) - gb)
        bad_q = sorted(games[(games.week == w) & ~games.quarters_sum_to_final].game_id)
        weeks.append({"week": w, "scheduled": len(sw), "final_scores": int(sw.home_score.notna().sum()), "play_by_play": len(pb & set(sw.game_id)),
                      "quarters_sum_to_final": int(games[(games.week == w)].quarters_sum_to_final.sum()), "gamebooks": len(gb & set(sw.game_id)),
                      "missing_play_by_play": miss_pbp, "quarter_mismatch": bad_q, "missing_gamebooks": miss_gb})
        if miss_pbp:
            flags.append(f"Week {w}: play-by-play missing for {', '.join(miss_pbp)}")
        if bad_q:
            flags.append(f"Week {w}: quarter scores do not add up to the final for {', '.join(bad_q)}")
        if miss_gb:
            flags.append(f"Week {w}: NFL game books missing for {len(miss_gb)} of {len(sw)} games")
    teams = []
    for t in sorted(set(sched.home_team) | set(sched.away_team)):
        sch = sched[((sched.home_team == t) | (sched.away_team == t)) & (sched.week <= last_full)]
        have = tg[tg.team == t]
        teams.append({"team": t, "scheduled_games": len(sch), "games_in_database": len(have)})
        if len(have) != len(sch):
            flags.append(f"{t}: {len(have)} games in the database, {len(sch)} scheduled through Week {last_full}")
    return {"season": SEASON, "through_week": int(last_full), "weeks": weeks, "teams": teams, "flags": flags,
            "play_by_play_complete": all(not w["missing_play_by_play"] for w in weeks),
            "quarters_verified": all(not w["quarter_mismatch"] for w in weeks)}


def write_audit_md(a):
    L = [f"# {SEASON} data audit, Weeks 1-{a['through_week']}", "",
         f"Play-by-play complete: **{'yes' if a['play_by_play_complete'] else 'NO'}**. Quarter scores add up to every final: "
         f"**{'yes' if a['quarters_verified'] else 'NO'}**.", "",
         "| Week | Games | Final scores | Play-by-play | Quarters verified | NFL game books |", "|---|---|---|---|---|---|"]
    for w in a["weeks"]:
        L.append(f"| {w['week']} | {w['scheduled']} | {w['final_scores']} | {w['play_by_play']} | {w['quarters_sum_to_final']} | {w['gamebooks']} |")
    L += ["", "## Flags", ""] + ([f"- {f}" for f in a["flags"]] or ["- none"])
    (OUT / "AUDIT.md").write_text("\n".join(L) + "\n")


def main():
    p, g, s, keys, games, tg, season_rank = build()
    splits, _ = player_splits(p, tg, season_rank, keys)
    prof = team_profile(tg)
    a = audit(g, games, tg, p)
    games.to_csv(OUT / "games.csv", index=False)
    tg.to_csv(OUT / "team_games.csv", index=False)
    splits.to_csv(OUT / "player_splits.csv", index=False)
    prof.to_csv(OUT / "team_profile.csv", index=False)
    keys.to_csv(OUT / "key_players.csv", index=False)
    (OUT / "audit.json").write_text(json.dumps(a, indent=1, default=str))
    write_audit_md(a)
    print(json.dumps({"games": len(games), "team_games": len(tg), "players": len(splits), "flags": a["flags"][:20]}, indent=1))


if __name__ == "__main__":
    main()
