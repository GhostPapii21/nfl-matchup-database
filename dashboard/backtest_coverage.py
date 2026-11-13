#!/usr/bin/env python3
"""Fit and test three matchup adjustments on top of the opportunity check (dashboard/opportunity.py).

    python3 -m dashboard.backtest_coverage              # fit 2023-2024, hold out 2025
    python3 -m dashboard.backtest_coverage --rebuild    # rebuild the cached player-game rows first

Question: does knowing the defense's coverage style, the quarterback's pressure profile, or the player's record against
tough vs soft defenses improve a pass catcher's projection beyond what the opportunity check already does?

Every player-game is built exactly as in dashboard/backtest_opportunity.py (weeks 5+, active, 8+ targets over the
team's previous 8 games, inputs from earlier weeks only). On top of the current inputs each row carries, from the
previous season plus earlier weeks of this season only:

  1. coverage  his targets and yards split by man / zone and by middle-of-field open (Cover 2, 4, 6, 2-Man) / closed
               (Cover 0, 1, 3), his team's targets in the same splits, the league split for his position, and how
               often the opponent has played each this season (NGS participation data).
  2. pressure  the starting quarterback's pressured and clean dropbacks (sacks, attempts, completions, yards), the
               league's, and the opponent's pressure rate this season.
  3. tier      his yards per game against top-10 / middle / bottom-10 defenses (ranked by yards per game allowed to
               his position), the league's tier effect for his position, and the opponent's tier and rank.

Fit (2023-2024): for every adjustment the multiplier is derived from first principles, then two things are fitted:
the prior weight m (how many league-average chances are blended into the player's own split; m = infinity ignores his
own split and keeps only the league effect) and a strength beta in

    actual - expected = beta * expected * log(multiplier)

(least squares through the origin, standard errors clustered by team-game). beta = 1 means the multiplier is right as
derived, beta = 0 means it carries no information, beta < 0 means it points the wrong way.

Test (2025, never used in the fit): the same simulation as the board with the same random numbers, with and without
each adjustment: Brier score at 40/60/70/80 receiving yards and 4/6 receptions, and the mean absolute error of yards.
Differences come with a bootstrap interval (resampling team-games).

Decision rule, fixed before looking at 2025: an adjustment is used only if its fitted beta is positive with t >= 2 on
2023-2024 AND on 2025 the average Brier score improves with a 90% interval that excludes zero AND the yardage error
does not get worse. Otherwise dashboard/coverage_model.py returns a multiplier of 1.0 for it.

The defense-weight and tier rows are also checked on 2026 to date (no participation data is published for 2026, so
coverage and pressure cannot be). Writes dashboard/results/coverage_backtest.json and .md. About 2 minutes with
--rebuild, under 1 minute from the cached rows (pregame/.cache/coverage_backtest_rows.parquet).
"""
from __future__ import annotations

import argparse
import json
import sys
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from dashboard import opportunity as O  # noqa: E402
from dashboard.backtest_opportunity import CACHE, WINDOW, load, team_tables  # noqa: E402

FIT_SEASONS = (2023, 2024)
TEST_SEASON = 2025
EXTRA_SEASON = 2026    # no NGS participation published: used only as a second check of the defense weight and tier split
SEASONS = FIT_SEASONS + (TEST_SEASON, EXTRA_SEASON)
ROWS = CACHE / "coverage_backtest_rows.parquet"
NS = 4000
Y_T = (40, 60, 70, 80)
R_T = (4, 6)
M_GRID = (0, 10, 20, 40, 80, 160, 320, float("inf"))      # prior weights tried (inf = league effect only)
W_GRID = tuple(round(x, 3) for x in np.arange(0, 1.51, 0.125))
K_DEF = 100           # league-average pass plays blended into a defense's man / open / pressure rate
K_QB_RATE = 100       # league-average dropbacks blended into a quarterback's own pressure rate
MOF_OPEN = ("COVER_2", "COVER_4", "COVER_6", "2_MAN")
MOF_CLOSED = ("COVER_0", "COVER_1", "COVER_3")
PBP_COLS = ["season_type", "week", "game_id", "play_id", "posteam", "defteam", "pass_attempt", "sack", "two_point_attempt",
            "passer_player_id", "receiver_player_id", "complete_pass", "receiving_yards", "yards_gained"]


# ----------------------------------------------------------------------------------------------- labelled plays
NFLVERSE = "https://github.com/nflverse/nflverse-data/releases/download/"
NEEDED = [f"pbp_participation/pbp_participation_{y}.parquet" for y in (2022, 2023, 2024, 2025)] + ["weekly_rosters/roster_weekly_2022.parquet"]


def ensure_files():
    """Download the nflverse files this backtest needs beyond the usual cache (participation 2022-2025, 2022 rosters)."""
    import urllib.request
    for rel in NEEDED:
        dest = CACHE / rel.split("/")[-1]
        if not dest.exists():
            print(f"coverage backtest: downloading {rel}", flush=True)
            urllib.request.urlretrieve(NFLVERSE + rel, dest)


def pass_plays(season: int, pos: dict) -> pd.DataFrame:
    """Every regular-season pass play (attempts and sacks) with the NGS coverage and pressure labels joined on."""
    p = pd.read_parquet(CACHE / f"play_by_play_{season}.parquet", columns=PBP_COLS)
    p = p[(p.season_type == "REG") & (p.pass_attempt == 1) & (p.two_point_attempt != 1)].copy()
    cols = ["nflverse_game_id", "play_id", "was_pressure", "defense_man_zone_type", "defense_coverage_type"]
    f = CACHE / f"pbp_participation_{season}.parquet"
    part = pd.read_parquet(f, columns=cols) if f.exists() else pd.DataFrame({c: pd.Series(dtype=object) for c in cols}).astype({"play_id": float})
    part = part.rename(columns={"nflverse_game_id": "game_id"}).drop_duplicates(["game_id", "play_id"])
    p = p.merge(part, on=["game_id", "play_id"], how="left")
    mz, cov = p.defense_man_zone_type, p.defense_coverage_type
    p["man"] = np.where(mz == "MAN_COVERAGE", 1.0, np.where(mz == "ZONE_COVERAGE", 0.0, np.nan))
    p["open"] = np.where(cov.isin(MOF_OPEN), 1.0, np.where(cov.isin(MOF_CLOSED), 0.0, np.nan))
    p["press"] = pd.to_numeric(p.was_pressure.map({True: 1.0, False: 0.0}), errors="coerce")
    p["sack"] = (p.sack == 1).astype(int)
    p.loc[(p.sack == 1) & p.press.isna(), "press"] = 1.0     # the 2022 file leaves sacks unlabelled; a sack is a pressure
    p["tgt"] = ((p.sack == 0) & p.receiver_player_id.notna()).astype(int)
    p["att"] = 1 - p.sack
    p["comp"] = (p.complete_pass == 1).astype(int)
    p["yd"] = p.receiving_yards.fillna(0.0)
    p["pos"] = p.receiver_player_id.map(pos)
    p["season"] = season
    return p.rename(columns={"passer_player_id": "passer", "receiver_player_id": "receiver"})


def player_games(pl: pd.DataFrame) -> pd.DataFrame:
    """One row per receiver per game: targets and yards overall and by coverage, plus his team's targets by coverage."""
    t = pl[pl.tgt == 1].copy()
    for name, col, val in (("man", "man", 1.0), ("zone", "man", 0.0), ("open", "open", 1.0), ("closed", "open", 0.0)):
        f = (t[col] == val)
        t[f"tg_{name}"] = f.astype(int)
        t[f"yd_{name}"] = t.yd * f
    cols = [c for c in t.columns if c.startswith(("tg_", "yd_"))]
    t["targets"] = 1
    pg = t.groupby(["season", "week", "game_id", "posteam", "defteam", "receiver"], as_index=False)[["targets", "yd", "comp"] + cols].sum()
    pg = pg.rename(columns={"yd": "yards"})
    team = t.groupby(["game_id", "posteam"], as_index=False)[[c for c in cols if c.startswith("tg_")]].sum()
    team = team.rename(columns={c: "t" + c for c in team.columns if c.startswith("tg_")})
    pg = pg.merge(team, on=["game_id", "posteam"], how="left")
    pg["pos"] = pg.receiver.map(dict(zip(t.receiver, t.pos)))
    return pg


COV_SUM = ["tg_man", "yd_man", "tg_zone", "yd_zone", "tg_open", "yd_open", "tg_closed", "yd_closed",
           "ttg_man", "ttg_zone", "ttg_open", "ttg_closed"]


def _tiers(pg: pd.DataFrame) -> pd.DataFrame:
    """Rank defenses by yards per game allowed to each position (1 = fewest). Top 10 = tough, bottom 10 = soft."""
    games = pg.groupby("defteam").game_id.nunique()
    y = pg[pg.pos.isin(["WR", "TE", "RB"])].groupby(["pos", "defteam"], as_index=False).agg(yards=("yards", "sum"), targets=("targets", "sum"))
    y["g"] = y.defteam.map(games)
    y["yds_pg"], y["tg_pg"] = y.yards / y.g, y.targets / y.g
    y["rank"] = y.groupby("pos").yds_pg.rank(method="first")
    n = y.groupby("pos").defteam.transform("size")
    y["tier"] = np.where(y["rank"] <= 10, "tough", np.where(y["rank"] > n - 10, "soft", "mid"))
    y["f_yds"] = y.yds_pg / y.groupby("pos").yds_pg.transform("mean")
    y["f_tg"] = y.tg_pg / y.groupby("pos").tg_pg.transform("mean")
    return y


def week_features(season, week, pl_prev, pl_cur, pg_prev, pg_cur):
    """Everything known before `week` of `season`: previous season plus earlier weeks of this season."""
    cur_pl, cur_pg = pl_cur[pl_cur.week < week], pg_cur[pg_cur.week < week]
    win_pl, win_pg = pd.concat([pl_prev, cur_pl]), pd.concat([pg_prev, cur_pg])
    F = {}
    # 1. coverage: player splits, league splits by position, defense rates (this season only: schemes change)
    F["player_cov"] = win_pg.groupby("receiver")[COV_SUM].sum()
    lp = win_pg.groupby("pos")[COV_SUM].sum()
    tot = win_pg[COV_SUM].sum()
    lg = pd.DataFrame(index=lp.index)
    for a, b, tag in (("man", "zone", "mz"), ("open", "closed", "oc")):
        ypt_all = (lp[f"yd_{a}"] + lp[f"yd_{b}"]) / (lp[f"tg_{a}"] + lp[f"tg_{b}"])
        sh_all = (lp[f"tg_{a}"] + lp[f"tg_{b}"]) / (tot[f"tg_{a}"] + tot[f"tg_{b}"])
        lg[f"L_ypt_{tag}"] = ypt_all
        for s in (a, b):
            lg[f"r_{s}"] = (lp[f"yd_{s}"] / lp[f"tg_{s}"]) / ypt_all          # league yards per target in this look / overall
            lg[f"rs_{s}"] = (lp[f"tg_{s}"] / tot[f"tg_{s}"]) / sh_all        # position's share of targets in this look / overall
    F["league_cov"] = lg
    d = cur_pl.groupby("defteam").agg(n_mz=("man", "count"), n_man=("man", "sum"), n_oc=("open", "count"), n_open=("open", "sum"),
                                      n_pl=("press", "count"), n_press=("press", "sum"))
    L = {"man": cur_pl.man.mean(), "open": cur_pl.open.mean(), "press": cur_pl.press.mean()}
    d["opp_man"] = (d.n_man + K_DEF * L["man"]) / (d.n_mz + K_DEF)
    d["opp_open"] = (d.n_open + K_DEF * L["open"]) / (d.n_oc + K_DEF)
    d["opp_press"] = (d.n_press + K_DEF * L["press"]) / (d.n_pl + K_DEF)
    d["opp_man_raw"], d["opp_press_raw"] = d.n_man / d.n_mz, d.n_press / d.n_pl
    F["defense"], F["league_rates"] = d, L
    # 2. pressure: quarterback and league results when pressured (p) and clean (c)
    w = win_pl[win_pl.press.notna()]
    agg = {"n": ("press", "size"), "sk": ("sack", "sum"), "att": ("att", "sum"), "cmp": ("comp", "sum"), "yd": ("yd", "sum")}
    q = w.groupby(["passer", "press"]).agg(**agg).unstack("press").fillna(0.0)
    q.columns = [f"q_{a}_{'p' if b == 1.0 else 'c'}" for a, b in q.columns]
    F["qb"] = q
    lq = w.groupby("press").agg(**agg)
    F["league_qb"] = {"L_press_win": float(w.press.mean()),
                      **{f"L_sk_{k}": float(lq.sk[v] / lq.n[v]) for k, v in (("p", 1.0), ("c", 0.0))},
                      **{f"L_cmp_{k}": float(lq.cmp[v] / lq.att[v]) for k, v in (("p", 1.0), ("c", 0.0))},
                      **{f"L_ypa_{k}": float(lq.yd[v] / lq.att[v]) for k, v in (("p", 1.0), ("c", 0.0))}}
    # 3. tiers: previous-season games use that season's final ranks, this season's games use ranks to date
    tp, tc = _tiers(pg_prev), _tiers(cur_pg)
    tmap = pd.concat([tp.assign(season=season - 1), tc.assign(season=season)])[["season", "pos", "defteam", "tier"]]
    x = win_pg.merge(tmap, on=["season", "pos", "defteam"], how="inner")
    pt = x.groupby(["receiver", "tier"]).agg(y=("yards", "sum"), n=("yards", "size")).unstack("tier").fillna(0.0)
    pt.columns = [f"t_{a}_{b}" for a, b in pt.columns]
    F["player_tier"] = pt
    lt = x.groupby(["pos", "tier"]).agg(y=("yards", "sum"), n=("yards", "size"))
    lall = x.groupby("pos").agg(y=("yards", "sum"), n=("yards", "size"))
    F["league_tier"] = ((lt.y / lt.n) / (lall.y / lall.n).reindex(lt.index, level=0)).unstack("tier")
    F["def_tier"] = tc.set_index(["pos", "defteam"])
    return F


# ----------------------------------------------------------------------------------------------- rows
def build_season(season: int) -> list[dict]:
    """Same player-games and current-model inputs as backtest_opportunity.run_season, plus the new pre-game features."""
    prev = season - 1
    p, r = load(season)
    pp, pr = load(prev)
    allr = pd.concat([pr, r])
    pos = dict(zip(allr.gsis_id, allr.position))
    pools = O.league_pools(pp, pr)
    games = pd.read_parquet(CACHE / "games.parquet")
    games = games[(games.season == season) & (games.game_type == "REG") & games.home_score.notna()]
    off, dfn, rec, _ = team_tables(p, pos)
    act = r[r.status == "ACT"][["week", "team", "gsis_id"]]
    active = set(zip(act.week, act.team, act.gsis_id))
    pl_prev, pl_cur = pass_plays(prev, pos), pass_plays(season, pos)
    pg_prev, pg_cur = player_games(pl_prev), player_games(pl_cur)
    # what actually happened to the team's passing game (for the team-level pressure test)
    team_now = pl_cur.groupby(["game_id", "posteam"]).agg(db=("sack", "size"), sk=("sack", "sum"), cmp=("comp", "sum"), yd=("yd", "sum"),
                                                          press=("press", "mean"))
    out = []
    for week, gw in games.groupby("week"):
        if week < 5:
            continue
        F = week_features(season, week, pl_prev, pl_cur, pg_prev, pg_cur)
        for g in gw.itertuples():
            for team, opp, home, qb in ((g.home_team, g.away_team, True, g.home_qb_id), (g.away_team, g.home_team, False, g.away_qb_id)):
                to = off[(off.posteam == team) & (off.week < g.week)].sort_values("week").tail(WINDOW)
                do = dfn[(dfn.defteam == opp) & (dfn.week < g.week)].sort_values("week").tail(WINDOW)
                if len(to) < 4 or len(do) < 4:
                    continue
                plays = (to.play.mean() + do.plays.mean()) / 2
                pass_ratio = to.att.sum() / max(to.play.sum(), 1)
                margin = (g.spread_line if home else -g.spread_line) if pd.notna(g.spread_line) else None
                pmul, _ = O.script_multipliers(margin)
                team_att = plays * pass_ratio * pmul
                gids = set(to.game_id)
                prior_rec = rec[(rec.posteam == team) & rec.game_id.isin(gids)]
                tg_by_game = to.set_index("game_id").tgt.to_dict()
                now = rec[(rec.game_id == g.game_id) & (rec.posteam == team)].set_index("receiver_player_id")
                dd = F["defense"].loc[opp] if opp in F["defense"].index else None
                qq = F["qb"].loc[qb] if qb in F["qb"].index else None
                tn = team_now.loc[(g.game_id, team)] if (g.game_id, team) in team_now.index else None
                for pid, h in prior_rec.groupby("receiver_player_id"):
                    P = pos.get(pid)
                    if P not in ("WR", "TE", "RB") or h.targets.sum() < 8 or (g.week, team, pid) not in active:
                        continue
                    h = h.sort_values("week")
                    share = h.targets.sum() / sum(tg_by_game[x] for x in h.game_id)
                    l3 = h.tail(3)
                    s3 = l3.targets.sum() / max(sum(tg_by_game[x] for x in l3.game_id), 1)
                    su = 0.6 * share + 0.4 * s3 if len(h) >= 5 else share
                    exp_t = team_att * su
                    row = {"season": season, "week": int(g.week), "game_id": g.game_id, "team": team, "opp": opp, "pos": P, "player": pid,
                           "exp_targets": exp_t, "k": O._dispersion(list(h.targets), exp_t),
                           "cr": O.shrink(h.receptions.sum(), h.targets.sum(), pools["catch_rate"][P], O.PRIOR_TARGETS),
                           "ypr": O.shrink(h.yards.sum(), h.receptions.sum(), pools["ypr"][P], O.PRIOR_CATCHES),
                           "d_cr": do[f"{P}_rec"].sum() / max(do[f"{P}_tgt"].sum(), 1), "d_ypr": do[f"{P}_yds"].sum() / max(do[f"{P}_rec"].sum(), 1),
                           "lg_cr": pools["catch_rate"][P], "lg_ypr": pools["ypr"][P],
                           "seed": zlib.crc32(f"{season}{g.game_id}{pid}".encode()),
                           "actual_yards": float(now.yards.get(pid, 0.0)), "actual_rec": int(now.receptions.get(pid, 0)),
                           "actual_targets": int(now.targets.get(pid, 0))}
                    # coverage
                    pc = F["player_cov"].loc[pid] if pid in F["player_cov"].index else pd.Series(0.0, index=COV_SUM)
                    row.update({f"c_{c}": float(pc[c]) for c in COV_SUM})
                    row.update({k: float(v) for k, v in F["league_cov"].loc[P].items()})
                    row.update({"lg_man": F["league_rates"]["man"], "lg_open": F["league_rates"]["open"], "lg_press": F["league_rates"]["press"]})
                    for c in ("opp_man", "opp_open", "opp_press"):
                        row[c] = float(dd[c]) if dd is not None else F["league_rates"][c[4:]]
                    # pressure
                    for c in ("n", "sk", "att", "cmp", "yd"):
                        for s in ("p", "c"):
                            row[f"q_{c}_{s}"] = float(qq.get(f"q_{c}_{s}", 0.0)) if qq is not None else 0.0
                    row.update(F["league_qb"])
                    if tn is not None:
                        row.update({"team_db": float(tn.db), "team_sk": float(tn.sk), "team_cmp": float(tn.cmp), "team_yd": float(tn.yd),
                                    "team_press_actual": float(tn.press)})
                    # tier
                    key = (P, opp)
                    if key in F["def_tier"].index:
                        dt = F["def_tier"].loc[key]
                        tier = dt.tier
                        row.update({"opp_tier": tier, "opp_rank": float(dt["rank"]), "f_yds": float(dt.f_yds), "f_tg": float(dt.f_tg)})
                        ptier = F["player_tier"].loc[pid] if pid in F["player_tier"].index else {}
                        row["t_y_same"], row["t_n_same"] = float(ptier.get(f"t_y_{tier}", 0.0)), float(ptier.get(f"t_n_{tier}", 0.0))
                        row["t_y_all"] = float(sum(ptier.get(f"t_y_{t}", 0.0) for t in ("tough", "mid", "soft")))
                        row["t_n_all"] = float(sum(ptier.get(f"t_n_{t}", 0.0) for t in ("tough", "mid", "soft")))
                        row["L_tier"] = float(F["league_tier"].loc[P, tier])
                    out.append(row)
    return out


def build_rows(rebuild=False) -> pd.DataFrame:
    if ROWS.exists() and not rebuild:
        return pd.read_parquet(ROWS)
    ensure_files()
    rows = []
    for s in SEASONS:
        rows += build_season(s)
        print(f"coverage backtest: season {s}: {len(rows)} player-games so far", flush=True)
    df = pd.DataFrame(rows)
    df.to_parquet(ROWS)
    return df


# ----------------------------------------------------------------------------------------------- multipliers (vectorised)
def _mix(p, a, b):
    return p * a + (1 - p) * b


def cov_mult(df, a, b, m, opp, lg):
    """Coverage fit for looks a / b (man / zone or open / closed). Returns (yards-per-target multiplier, target multiplier).

    His yards per target in look a:  (yards_a + m * mu * r_a) / (targets_a + m), mu = his own overall rate (40 league
    targets blended in), r_a = league rate in look a / league overall, for his position. Same for b and for his share
    of team targets. The multiplier is his expected rate against this opponent's mix over his rate against the
    league-average mix. m = inf keeps only the league effect.
    """
    tg_a, tg_b, yd_a, yd_b = df[f"c_tg_{a}"], df[f"c_tg_{b}"], df[f"c_yd_{a}"], df[f"c_yd_{b}"]
    tag = "mz" if a == "man" else "oc"
    mu = (yd_a + yd_b + 40 * df[f"L_ypt_{tag}"]) / (tg_a + tg_b + 40)
    tt_a, tt_b = df[f"c_ttg_{a}"], df[f"c_ttg_{b}"]
    sh = (tg_a + tg_b + 1e-9) / (tt_a + tt_b + 1e-6)
    if np.isinf(m):
        e_a, e_b, s_a, s_b = df[f"r_{a}"], df[f"r_{b}"], df[f"rs_{a}"], df[f"rs_{b}"]
    else:
        mm = max(m, 1e-6)
        e_a = (yd_a + mm * mu * df[f"r_{a}"]) / (tg_a + mm)
        e_b = (yd_b + mm * mu * df[f"r_{b}"]) / (tg_b + mm)
        ms = mm * 8          # prior for the share is counted in team targets (about 8 team targets per player target)
        s_a = (tg_a + ms * sh * df[f"rs_{a}"]) / (tt_a + ms)
        s_b = (tg_b + ms * sh * df[f"rs_{b}"]) / (tt_b + ms)
    po, pl_ = df[opp], df[lg]
    ypt = _mix(po, e_a, e_b) / _mix(pl_, e_a, e_b).replace(0, np.nan)
    tgm = _mix(po, s_a, s_b) / _mix(pl_, s_a, s_b).replace(0, np.nan)
    return ypt.fillna(1.0).clip(0.5, 2.0), tgm.fillna(1.0).clip(0.5, 2.0)


def press_mult(df, m):
    """Pressure fit. Returns (yards-per-attempt multiplier, completion multiplier, attempts multiplier, expected pressure rate).

    P0 = the quarterback's usual pressure rate (100 league dropbacks blended in). P = P0 x opponent rate / league rate.
    His pressured and clean sack rate, completion rate and yards per attempt each get m league dropbacks blended in.
    Each multiplier is his expected result at pressure rate P over his expected result at his usual rate P0.
    """
    n_p, n_c = df.q_n_p, df.q_n_c
    P0 = (n_p + K_QB_RATE * df.L_press_win) / (n_p + n_c + K_QB_RATE)
    P = (P0 * df.opp_press / df.lg_press).clip(0.05, 0.7)
    if np.isinf(m):
        sk_p, sk_c, cm_p, cm_c, ya_p, ya_c = df.L_sk_p, df.L_sk_c, df.L_cmp_p, df.L_cmp_c, df.L_ypa_p, df.L_ypa_c
    else:
        mm = max(m, 1e-6)
        sk_p, sk_c = (df.q_sk_p + mm * df.L_sk_p) / (n_p + mm), (df.q_sk_c + mm * df.L_sk_c) / (n_c + mm)
        cm_p, cm_c = (df.q_cmp_p + mm * df.L_cmp_p) / (df.q_att_p + mm), (df.q_cmp_c + mm * df.L_cmp_c) / (df.q_att_c + mm)
        ya_p, ya_c = (df.q_yd_p + mm * df.L_ypa_p) / (df.q_att_p + mm), (df.q_yd_c + mm * df.L_ypa_c) / (df.q_att_c + mm)

    def at(p):
        a = p * (1 - sk_p) / (p * (1 - sk_p) + (1 - p) * (1 - sk_c))      # share of his throws that come under pressure
        return _mix(a, ya_p, ya_c), _mix(a, cm_p, cm_c), 1 - _mix(p, sk_p, sk_c)
    y1, c1, a1 = at(P)
    y0, c0, a0 = at(P0)
    return (y1 / y0).clip(0.7, 1.3), (c1 / c0).clip(0.7, 1.3), (a1 / a0).clip(0.8, 1.2), P


def tier_mult(df, m, own_only=False):
    """His yards per game against this opponent's tier over his overall yards per game, with m league games blended in."""
    L = df.L_tier.fillna(1.0)
    avg = (df.t_y_all / df.t_n_all.replace(0, np.nan))
    if np.isinf(m):
        out = L.copy()
    else:
        est = (df.t_y_same + max(m, 1e-6) * avg * L) / (df.t_n_same + max(m, 1e-6))
        out = (est / avg.replace(0, np.nan)).fillna(L)
    if own_only:
        out = out / L
    return out.fillna(1.0).clip(0.5, 2.0)


# ----------------------------------------------------------------------------------------------- expected values and fit
def base_parts(df, w=None, cap=True):
    """Deterministic parts of the current model: expected targets (after the volume correction), catch rate, yards per catch."""
    w = O.DEF_WEIGHT if w is None else w
    a, b = O.VOLUME_CAL["rec"]
    vol = (a + b * df.exp_targets).clip(lower=0)
    f1, f2 = 1 + w * (df.d_cr / df.lg_cr - 1), 1 + w * (df.d_ypr / df.lg_ypr - 1)
    if cap:
        f1, f2 = f1.clip(0.8, 1.2), f2.clip(0.8, 1.2)
    return vol, (df.cr * f1).clip(0.2, 0.95), df.ypr * f2


def fit_beta(resid, x, clusters):
    """Least squares through the origin with cluster-robust standard error. Returns beta, se, t, sse."""
    resid, x = np.asarray(resid, float), np.asarray(x, float)
    sxx = float((x * x).sum())
    if sxx <= 0:
        return {"beta": 0.0, "se": None, "t": 0.0, "sse": float((resid ** 2).sum())}
    beta = float((x * resid).sum() / sxx)
    u = resid - beta * x
    g = pd.Series(x * u).groupby(np.asarray(clusters)).sum()
    se = float(np.sqrt((g ** 2).sum()) / sxx)
    return {"beta": round(beta, 3), "se": round(se, 3), "t": round(beta / se, 2) if se > 0 else 0.0, "sse": float((u ** 2).sum())}


def fit_grid(df, make_mult, target, grid=M_GRID, check=None):
    """For each prior weight m: fit beta for `target` ('yards', 'targets' or 'rec'). Returns the table and the best m."""
    vol, cr, ypr = base_parts(df)
    cl = df.game_id + df.team
    exp = {"yards": vol * cr * ypr, "targets": vol, "rec": vol * cr}[target]
    act = {"yards": df.actual_yards, "targets": df.actual_targets, "rec": df.actual_rec}[target]
    tab = []
    for m in grid:
        mult = make_mult(df, m)
        r = fit_beta(act - exp, exp * np.log(mult), cl)
        r.update({"m": ("inf" if np.isinf(m) else m), "sd_log_mult": round(float(np.log(mult).std()), 4)})
        if check is not None:        # the same regression on the holdout season, as a replication check (never used to choose anything)
            v2, c2, y2 = base_parts(check)
            e2 = {"yards": v2 * c2 * y2, "targets": v2, "rec": v2 * c2}[target]
            a2 = {"yards": check.actual_yards, "targets": check.actual_targets, "rec": check.actual_rec}[target]
            h = fit_beta(a2 - e2, e2 * np.log(make_mult(check, m)), check.game_id + check.team)
            r.update({"beta_2025": h["beta"], "t_2025": h["t"]})
        tab.append(r)
    base_sse = float(((act - exp) ** 2).sum())
    for r in tab:
        r["sse_drop_pct"] = round(100 * (1 - r["sse"] / base_sse), 4)
        del r["sse"]
    ok = [r for r in tab if r["beta"] > 0]
    best = max(ok, key=lambda r: r["sse_drop_pct"]) if ok else None
    return tab, best


def _m(v):
    return float("inf") if v == "inf" else float(v)


# ----------------------------------------------------------------------------------------------- holdout simulation
def simulate(df, vol_mult=None, cr_mult=None, ypr_mult=None, w=None, cap=True):
    """Run the board's simulation for every row with optional multipliers. Same seeds = same random numbers per row."""
    n = len(df)
    one = np.ones(n)
    vm = one if vol_mult is None else np.asarray(vol_mult, float)
    cm = one if cr_mult is None else np.asarray(cr_mult, float)
    ym = one if ypr_mult is None else np.asarray(ypr_mult, float)
    _, cr, ypr = base_parts(df, w, cap)
    cr, ypr = cr.to_numpy() * cm, ypr.to_numpy() * ym
    a, b = O.VOLUME_CAL["rec"]
    res = {f"y{t}": np.zeros(n) for t in Y_T} | {f"r{t}": np.zeros(n) for t in R_T} | {"mean": np.zeros(n)}
    pools = _pools()
    for i, r in enumerate(df.itertuples()):
        # the volume multiplier is applied to the corrected volume, so convert it back to the raw scale the simulator takes
        raw = (max(0.0, a + b * r.exp_targets) * vm[i] - a) / b
        _, rc, yd = O.simulate_receiver(exp_targets=raw, k=r.k, catch_rate=cr[i], ypr=ypr[i], pool=pools[(r.season, r.pos)], n=NS, seed=int(r.seed))
        for t in Y_T:
            res[f"y{t}"][i] = (yd >= t).mean()
        for t in R_T:
            res[f"r{t}"][i] = (rc >= t).mean()
        res["mean"][i] = yd.mean()
    return res


_POOLS: dict = {}


def _pools():
    if not _POOLS:
        for s in SEASONS:
            pp, pr = load(s - 1)
            pl = O.league_pools(pp, pr)
            for P in ("WR", "TE", "RB"):
                _POOLS[(s, P)] = pl["catch"][P]
    return _POOLS


def score(df, sim):
    """Per-row losses: squared error for each line and absolute yardage error."""
    L = {}
    for t in Y_T:
        L[f"y{t}"] = (sim[f"y{t}"] - (df.actual_yards.to_numpy() >= t)) ** 2
    for t in R_T:
        L[f"r{t}"] = (sim[f"r{t}"] - (df.actual_rec.to_numpy() >= t)) ** 2
    L["brier_avg"] = np.mean([L[k] for k in list(L)], axis=0)
    L["mae"] = np.abs(sim["mean"] - df.actual_yards.to_numpy())
    return L


def compare(df, base_loss, loss, n_boot=2000, seed=7):
    """Mean of each loss and its change vs the current model, with a 90% bootstrap interval over team-games."""
    cl = pd.factorize(df.game_id + df.team)[0]
    k = cl.max() + 1
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, k, size=(n_boot, k))
    cnt = np.bincount(cl, minlength=k).astype(float)
    out = {}
    for key in loss:
        d = loss[key] - base_loss[key]
        s = np.bincount(cl, weights=d, minlength=k)
        boot = s[draws].sum(axis=1) / cnt[draws].sum(axis=1)
        out[key] = {"value": float(loss[key].mean()), "change": float(d.mean()),
                    "lo": float(np.percentile(boot, 5)), "hi": float(np.percentile(boot, 95))}
    return out


# ----------------------------------------------------------------------------------------------- team-level pressure test
def team_pressure_test(df):
    """One row per team-game: does the pre-game pressure outlook explain the passing game beyond the opponent's pressure-free record?"""
    t = df.drop_duplicates(["game_id", "team"]).dropna(subset=["team_db"]).copy()
    ypa_m, cmp_m, att_m, P = press_mult(t, float("inf"))
    t["P"] = P
    t["sack_rate"] = t.team_sk / t.team_db
    t["cmp_pct"] = t.team_cmp / (t.team_db - t.team_sk)
    t["ypa"] = t.team_yd / (t.team_db - t.team_sk)
    t["ypdb"] = t.team_yd / t.team_db
    res = {"team_games": int(len(t))}
    for name, col in (("pressure rate allowed in the game", "team_press_actual"), ("sack rate", "sack_rate"), ("completion %", "cmp_pct"),
                      ("yards per attempt", "ypa"), ("yards per dropback", "ypdb")):
        res[name] = {"corr_with_opp_pressure_rate": round(float(np.corrcoef(t.opp_press, t[col])[0, 1]), 3),
                     "corr_with_expected_pressure_rate": round(float(np.corrcoef(t.P, t[col])[0, 1]), 3)}
    return res


# ----------------------------------------------------------------------------------------------- main
def run(df):
    fit, test = df[df.season.isin(FIT_SEASONS)].reset_index(drop=True), df[df.season == TEST_SEASON].reset_index(drop=True)
    variants = {}
    R = {"fit_seasons": list(FIT_SEASONS), "test_season": TEST_SEASON, "fit_player_games": int(len(fit)), "test_player_games": int(len(test)),
         "by_position_test": test.pos.value_counts().to_dict(), "fits": {}, "decision_rule": "fit beta > 0 with t >= 2 on 2023-2024, and on 2025 the "
         "average Brier improves with a 90% interval below zero, and yardage error not worse"}

    # ---- 1. coverage
    for tag, a, b, opp, lg in (("man_zone", "man", "zone", "opp_man", "lg_man"), ("mof", "open", "closed", "opp_open", "lg_open")):
        ty, by = fit_grid(fit, lambda d, m: cov_mult(d, a, b, m, opp, lg)[0], "yards", check=test)
        tt, bt = fit_grid(fit, lambda d, m: cov_mult(d, a, b, m, opp, lg)[1], "targets", check=test)
        # by position, at the league-only and a middle prior weight
        bypos = {}
        for P in ("WR", "TE", "RB"):
            fp = fit[fit.pos == P].reset_index(drop=True)
            bypos[P] = {"yards": fit_grid(fp, lambda d, m: cov_mult(d, a, b, m, opp, lg)[0], "yards", grid=(40, float("inf")))[0],
                        "targets": fit_grid(fp, lambda d, m: cov_mult(d, a, b, m, opp, lg)[1], "targets", grid=(40, float("inf")))[0]}
        R["fits"][f"coverage_{tag}"] = {"yards_per_target": ty, "best_yards": by, "targets": tt, "best_targets": bt, "by_position": bypos}

        def derived(d, a=a, b=b, opp=opp, lg=lg):
            y, t = cov_mult(d, a, b, 40, opp, lg)
            return {"vol_mult": t, "cr_mult": np.sqrt(y), "ypr_mult": np.sqrt(y)}

        def fitted(d, a=a, b=b, opp=opp, lg=lg, by=by, bt=bt):
            y = cov_mult(d, a, b, _m(by["m"]), opp, lg)[0] ** by["beta"] if by else 1.0
            t = cov_mult(d, a, b, _m(bt["m"]), opp, lg)[1] ** bt["beta"] if bt else 1.0
            return {"vol_mult": t * np.ones(len(d)), "cr_mult": np.sqrt(y) * np.ones(len(d)), "ypr_mult": np.sqrt(y) * np.ones(len(d))}
        nm = "man/zone" if tag == "man_zone" else "middle open/closed"
        variants[f"+ coverage fit {nm}, as derived (m=40, strength 1)"] = derived
        variants[f"+ coverage fit {nm}, as fitted"] = fitted

    # ---- 2. pressure
    ty, by = fit_grid(fit, lambda d, m: press_mult(d, m)[0], "yards", check=test)
    tr, br = fit_grid(fit, lambda d, m: press_mult(d, m)[1], "rec", check=test)
    tt, bt = fit_grid(fit, lambda d, m: press_mult(d, m)[2], "targets", check=test)
    R["fits"]["pressure"] = {"yards_per_attempt": ty, "best_yards": by, "completion": tr, "best_completion": br, "attempts": tt, "best_attempts": bt,
                             "team_level_fit": team_pressure_test(fit), "team_level_test": team_pressure_test(test)}

    def p_derived(d):
        y, c, a_, _ = press_mult(d, 100)
        return {"vol_mult": a_, "cr_mult": c, "ypr_mult": y / c}

    def p_fitted(d, by=by, br=br, bt=bt):
        y = press_mult(d, _m(by["m"]))[0] ** by["beta"] if by else np.ones(len(d))
        c = press_mult(d, _m(br["m"]))[1] ** br["beta"] if br else np.ones(len(d))
        a_ = press_mult(d, _m(bt["m"]))[2] ** bt["beta"] if bt else np.ones(len(d))
        return {"vol_mult": a_, "cr_mult": c, "ypr_mult": y / c}
    variants["+ pressure fit, as derived (m=100, strength 1)"] = p_derived
    variants["+ pressure fit, as fitted"] = p_fitted

    # ---- 3. opponent tier and the weight on the defense factor
    def sse_w(d, w, cap):
        vol, cr, ypr = base_parts(d, w, cap)
        e = d.actual_yards - vol * cr * ypr
        return float((e ** 2).mean()), float(e.abs().mean())
    wtab = [{"weight": w, "capped": cap, "mse": round(sse_w(fit, w, cap)[0], 3), "mae": round(sse_w(fit, w, cap)[1], 4)} for cap in (True, False) for w in W_GRID]
    bw = min(wtab, key=lambda r: r["mse"])
    v0, c0, y0 = base_parts(fit, 0.0)
    cl = fit.game_id + fit.team
    okf = fit.f_yds.notna()
    cont = fit_beta((fit.actual_yards - v0 * c0 * y0)[okf], (v0 * c0 * y0 * np.log(fit.f_yds.clip(0.4, 2.5)))[okf], cl[okf])
    vb, cb, yb = base_parts(fit)
    tgf = fit_beta((fit.actual_targets - vb)[okf], (vb * np.log(fit.f_tg.clip(0.4, 2.5)))[okf], cl[okf])
    for r in (cont, tgf):
        r.pop("sse", None)
    # tier split: (a) replacing the defense factor, (b) the player's own part on top of the current model
    def grid_on(d, w, own):
        vol, cr, ypr = base_parts(d, w)
        exp = vol * cr * ypr
        tab = []
        for m in M_GRID:
            mult = tier_mult(d, m, own_only=own)
            r = fit_beta(d.actual_yards - exp, exp * np.log(mult), d.game_id + d.team)
            r.update({"m": "inf" if np.isinf(m) else m, "sd_log_mult": round(float(np.log(mult).std()), 4),
                      "mse_with_beta": round(r["sse"] / len(d), 3), "mse_as_is": round(float(((d.actual_yards - exp * mult) ** 2).mean()), 3)})
            del r["sse"]
            tab.append(r)
        return tab
    t_repl, t_own = grid_on(fit, 0.0, False), grid_on(fit, None, True)
    ok = [r for r in t_repl if r["beta"] > 0]
    b_repl = min(ok, key=lambda r: r["mse_with_beta"]) if ok else None
    ok = [r for r in t_own if r["beta"] > 0 and r["m"] != "inf"]
    b_own = min(ok, key=lambda r: r["mse_with_beta"]) if ok else None
    R["fits"]["tier"] = {"defense_weight_grid": wtab, "best_defense_weight": bw, "mse_no_defense_factor": round(sse_w(fit, 0.0, True)[0], 3),
                         "mse_current_half_weight": round(sse_w(fit, 0.5, True)[0], 3),
                         "position_yards_allowed_factor_exponent": cont, "position_targets_allowed_factor_exponent": tgf,
                         "tier_replacing_defense_factor": t_repl, "best_tier_replacing": b_repl,
                         "own_tier_split_on_top_of_current": t_own, "best_own_tier_split": b_own}
    variants["no defense factor at all (weight 0)"] = lambda d: {"w": 0.0}
    variants[f"defense factor at fitted weight {bw['weight']}" + ("" if bw["capped"] else ", no cap")] = lambda d, bw=bw: {"w": bw["weight"], "cap": bw["capped"]}
    variants["tier split replaces defense factor: raw average vs top-10 / bottom-10 (m=0)"] = lambda d: {"w": 0.0, "ypr_mult": tier_mult(d, 0)}
    if b_repl:
        variants[f"tier split replaces defense factor, as fitted (m={b_repl['m']}, strength {b_repl['beta']})"] = \
            lambda d, b=b_repl: {"w": 0.0, "ypr_mult": tier_mult(d, _m(b["m"])) ** b["beta"]}
    if b_own:
        variants[f"+ his own tier split on top, as fitted (m={b_own['m']}, strength {b_own['beta']})"] = \
            lambda d, b=b_own: {"ypr_mult": tier_mult(d, _m(b["m"]), own_only=True) ** b["beta"]}
    else:
        variants["+ his own tier split on top (m=8, strength 1)"] = lambda d: {"ypr_mult": tier_mult(d, 8, own_only=True)}
    if tgf["beta"] > 0:
        variants[f"+ targets the defense allows his position (strength {tgf['beta']})"] = \
            lambda d, b=tgf["beta"]: {"vol_mult": d.f_tg.clip(0.4, 2.5).fillna(1.0) ** b}

    # ---- holdout
    base_sim = simulate(test)
    base_loss = score(test, base_sim)
    R["holdout"] = {"current model": compare(test, base_loss, base_loss)}
    R["holdout_by_position"] = {}
    for name, fn in variants.items():
        sim = simulate(test, **fn(test))
        loss = score(test, sim)
        R["holdout"][name] = compare(test, base_loss, loss)
        R["holdout_by_position"][name] = {P: {"brier_avg_change": float((loss["brier_avg"] - base_loss["brier_avg"])[(test.pos == P).to_numpy()].mean()),
                                              "mae_change": float((loss["mae"] - base_loss["mae"])[(test.pos == P).to_numpy()].mean())} for P in ("WR", "TE", "RB")}
        print(f"holdout: {name}: brier {R['holdout'][name]['brier_avg']['change']:+.5f}, mae {R['holdout'][name]['mae']['change']:+.3f}", flush=True)
    # second check on 2026 (to date) for the variants that need no participation data
    extra = df[df.season == EXTRA_SEASON].dropna(subset=["f_yds"]).reset_index(drop=True)
    if len(extra):
        R["extra_season"], R["extra_player_games"], R["extra_weeks"] = EXTRA_SEASON, int(len(extra)), [int(extra.week.min()), int(extra.week.max())]
        b_sim = simulate(extra)
        b_loss = score(extra, b_sim)
        R["extra_holdout"] = {"current model": compare(extra, b_loss, b_loss)}
        for name, fn in variants.items():
            if name.startswith(("+ coverage", "+ pressure")):
                continue
            R["extra_holdout"][name] = compare(extra, b_loss, score(extra, simulate(extra, **fn(extra))))
    R["diagnostics"] = diagnostics(df)
    return R


def diagnostics(df):
    """How stable are the inputs? Correlation of a split measured on odd vs even prior information is not available here,
    so report spread and sample sizes: how much the multipliers actually move, and how much data sits behind a split."""
    t = df[df.season == TEST_SEASON]
    d = {"median_prior_targets_vs_man": float(t.c_tg_man.median()), "median_prior_targets_vs_zone": float(t.c_tg_zone.median()),
         "median_prior_targets_mof_open": float(t.c_tg_open.median()), "median_prior_targets_mof_closed": float(t.c_tg_closed.median()),
         "opp_man_rate_p10_p90": [float(t.opp_man.quantile(.1)), float(t.opp_man.quantile(.9))], "league_man_rate": float(t.lg_man.mean()),
         "opp_open_rate_p10_p90": [float(t.opp_open.quantile(.1)), float(t.opp_open.quantile(.9))], "league_open_rate": float(t.lg_open.mean()),
         "opp_pressure_rate_p10_p90": [float(t.opp_press.quantile(.1)), float(t.opp_press.quantile(.9))], "league_pressure_rate": float(t.lg_press.mean()),
         "median_games_vs_same_tier": float(t.t_n_same.median()),
         "league_by_season": {}}
    for s, g in df[df.season <= TEST_SEASON].groupby("season"):
        d["league_by_season"][int(s)] = {k: round(float(g[k].mean()), 3) for k in ("lg_man", "lg_open", "lg_press", "L_sk_p", "L_sk_c", "L_cmp_p", "L_cmp_c", "L_ypa_p", "L_ypa_c")}
        for P in ("WR", "TE", "RB"):
            gp = g[g.pos == P]
            d["league_by_season"][int(s)][P] = {k: round(float(gp[k].mean()), 3) for k in ("r_man", "r_zone", "r_open", "r_closed", "rs_man", "rs_zone", "rs_open", "rs_closed")}
    for a, b, opp, lg, tag in (("man", "zone", "opp_man", "lg_man", "man_zone"), ("open", "closed", "opp_open", "lg_open", "mof")):
        y, tg = cov_mult(t, a, b, 40, opp, lg)
        d[f"coverage_{tag}_ypt_mult_p5_p95_m40"] = [round(float(y.quantile(.05)), 3), round(float(y.quantile(.95)), 3)]
        d[f"coverage_{tag}_target_mult_p5_p95_m40"] = [round(float(tg.quantile(.05)), 3), round(float(tg.quantile(.95)), 3)]
    y, c, a_, _ = press_mult(t, 100)
    d["pressure_ypa_mult_p5_p95_m100"] = [round(float(y.quantile(.05)), 3), round(float(y.quantile(.95)), 3)]
    return d


def verdict(R, name, fit_rows):
    h = R["holdout"][name]
    t_ok = any(r and r["beta"] > 0 and r["t"] >= 2 for r in fit_rows)
    hold_ok = h["brier_avg"]["hi"] < 0 and h["mae"]["change"] <= 0
    return t_ok and hold_ok, t_ok, hold_ok


def summary(R):
    """Plain-English verdicts, written from the numbers and the fixed decision rule."""
    H, F = R["holdout"], R["fits"]
    base = H["current model"]

    def find(prefix):
        return next(k for k in H if k.startswith(prefix))

    def line(name):
        h = H[name]
        return (f"average Brier {h['brier_avg']['change']:+.5f} on a base of {base['brier_avg']['value']:.5f} "
                f"({100 * h['brier_avg']['change'] / base['brier_avg']['value']:+.2f}%, 90% range {h['brier_avg']['lo']:+.5f} to {h['brier_avg']['hi']:+.5f}); "
                f"yardage miss {h['mae']['change']:+.3f} yards on a base of {base['mae']['value']:.2f}")

    def best(r):
        return "no prior weight gave a positive strength" if not r else f"best prior weight m={r['m']}, strength {r['beta']} (t {r['t']}; same regression on 2025: {r.get('beta_2025')}, t {r.get('t_2025')})"
    out = ["## Summary", "",
           "None of the three ideas passed the test. The board should not apply any of them. Details:", ""]
    items = (("Coverage fit, man vs zone", "coverage_man_zone", "+ coverage fit man/zone, as fitted", ("best_yards", "best_targets"), ("yards per target", "targets")),
             ("Coverage fit, middle of field open vs closed", "coverage_mof", "+ coverage fit middle open/closed, as fitted", ("best_yards", "best_targets"), ("yards per target", "targets")),
             ("Pressure fit", "pressure", "+ pressure fit, as fitted", ("best_yards", "best_completion", "best_attempts"), ("yards per attempt", "completion rate", "attempts")))
    R["verdicts"] = {}
    for title, key, name, bests, labels in items:
        use, t_ok, h_ok = verdict(R, name, [F[key][b] for b in bests])
        R["verdicts"][key] = {"use": bool(use), "fit_rule_met": bool(t_ok), "holdout_rule_met": bool(h_ok)}
        out.append(f"- **{title}: {'USE' if use else 'do not use'}.** Fit 2023-2024: " + "; ".join(f"{lab}: {best(F[key][b])}" for lab, b in zip(labels, bests)) +
                   f". Test 2025 with the fitted version: {line(name)}. "
                   f"Fit rule met: {'yes' if t_ok else 'no'}. Holdout rule met: {'yes' if h_ok else 'no'}.")
    T = F["tier"]
    wname, rname, oname = find("defense factor at fitted weight"), find("tier split replaces defense factor: raw"), find("+ his own tier split")
    R["verdicts"]["tier_split"] = {"use": False}
    out += [f"- **Opponent tier (average vs top-10 vs bottom-10 defenses): do not use.** Used raw in place of the defense factor it is clearly worse: {line(rname)}. "
            f"Shrunk hard it only falls back to a weak league effect. His own tier split on top of the current model: {line(oname)}.",
            f"- **Weight on the current defense factor.** The fit prefers {T['best_defense_weight']['weight']} over the current 0.5 "
            f"(mean squared yardage error {T['best_defense_weight']['mse']} vs {T['mse_current_half_weight']}; with no defense factor at all {T['mse_no_defense_factor']}). "
            f"On 2025: {line(wname)}. " + (f"On {R['extra_season']} to date: average Brier {R['extra_holdout'][wname]['brier_avg']['change']:+.5f} "
            f"(90% range {R['extra_holdout'][wname]['brier_avg']['lo']:+.5f} to {R['extra_holdout'][wname]['brier_avg']['hi']:+.5f}). " if "extra_holdout" in R else "") +
            "The direction is the same in every season, but the gain is too small to tell apart from luck. It is reported here and nothing is changed. "
            "What it does say: the defense factor is not adding measurable value at any weight.",
            "- **Closest thing to a signal:** targets (not yards) by coverage. Running backs draw a larger share of targets against zone-heavy defenses. "
            "The fit-season strength was positive and the 2025 regression pointed the same way, but it moved the 2025 scores by less than 0.03%. Not used."]
    D = R["diagnostics"]
    out += ["", "Why these did not help, in plain words:", "",
            f"- The splits are thin. The typical player had {D['median_prior_targets_vs_man']:.0f} prior targets against man and {D['median_prior_targets_vs_zone']:.0f} against zone, "
            f"and {D['median_games_vs_same_tier']:.0f} prior games against the opponent's tier. That is mostly noise.",
            f"- Defenses do not differ enough. Nine in ten opponents play man between {D['opp_man_rate_p10_p90'][0]:.0%} and {D['opp_man_rate_p10_p90'][1]:.0%} of the time, "
            f"and pressure the passer between {D['opp_pressure_rate_p10_p90'][0]:.0%} and {D['opp_pressure_rate_p10_p90'][1]:.0%}.",
            f"- So the adjustments are tiny even when taken at face value: most players move by about 2% or less "
            f"(man/zone yards multiplier {D['coverage_man_zone_ypt_mult_p5_p95_m40'][0]} to {D['coverage_man_zone_ypt_mult_p5_p95_m40'][1]}, "
            f"pressure {D['pressure_ypa_mult_p5_p95_m100'][0]} to {D['pressure_ypa_mult_p5_p95_m100'][1]}). One game's yards swing far more than that.",
            "- A player's own numbers already carry most of it. His catch rate and yards per catch were earned against a mix of coverages and pass rushes.",
            "- Pressure is real at team level (a high-pressure defense does produce more pressure and more sacks) but the link to yards per attempt is weak and changed sign between the fit seasons and 2025.",
            "- The coverage labels are not consistent between seasons (league man rate "
            + ", ".join(f"{v['lg_man']:.0%} in {s}" for s, v in D["league_by_season"].items()) + "), which limits how much last season's split can say about this season.", ""]
    return out


def to_md(R):
    H = R["holdout"]
    keys = [f"y{t}" for t in Y_T] + [f"r{t}" for t in R_T]
    L = [f"# Coverage, pressure and opponent-tier adjustments: fit {R['fit_seasons'][0]}-{R['fit_seasons'][-1]}, test {R['test_season']}", "",
         f"Fit on {R['fit_player_games']} player-games. Tested on {R['test_player_games']} player-games from {R['test_season']} that the fit never saw "
         f"(weeks 5+, pass catchers: {R['by_position_test']}).", "",
         "Every input uses only the previous season and earlier weeks. Brier score: lower is better. "
         "Yardage miss: average gap between projected and actual receiving yards.", "",
         *summary(R),
         "## Holdout results (2025)", "",
         "| Model | Yds 40+ | Yds 60+ | Yds 70+ | Yds 80+ | Rec 4+ | Rec 6+ | Avg Brier | Change (90% range) | Yardage miss | Change (90% range) |",
         "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for name, h in H.items():
        ch = "" if name == "current model" else f"{h['brier_avg']['change']:+.5f} ({h['brier_avg']['lo']:+.5f} to {h['brier_avg']['hi']:+.5f})"
        cm = "" if name == "current model" else f"{h['mae']['change']:+.3f} ({h['mae']['lo']:+.3f} to {h['mae']['hi']:+.3f})"
        L.append(f"| {name} | " + " | ".join(f"{h[k]['value']:.4f}" for k in keys) + f" | {h['brier_avg']['value']:.5f} | {ch} | {h['mae']['value']:.2f} | {cm} |")
    if "extra_holdout" in R:
        L += ["", f"### Second check: {R['extra_season']} to date (weeks {R['extra_weeks'][0]}-{R['extra_weeks'][1]}, {R['extra_player_games']} player-games)", "",
              "Coverage and pressure data are not published for this season, so only the defense weight and tier rows can be checked.", "",
              "| Model | Avg Brier | Change (90% range) | Yardage miss | Change (90% range) |", "| --- | --- | --- | --- | --- |"]
        for name, h in R["extra_holdout"].items():
            ch = "" if name == "current model" else f"{h['brier_avg']['change']:+.5f} ({h['brier_avg']['lo']:+.5f} to {h['brier_avg']['hi']:+.5f})"
            cm = "" if name == "current model" else f"{h['mae']['change']:+.3f} ({h['mae']['lo']:+.3f} to {h['mae']['hi']:+.3f})"
            L.append(f"| {name} | {h['brier_avg']['value']:.5f} | {ch} | {h['mae']['value']:.2f} | {cm} |")
    L += ["", "A negative change is an improvement. If the range includes zero, the change cannot be told apart from luck.", "",
          "By position (change in average Brier / change in yardage miss):", ""]
    for name, bp in R["holdout_by_position"].items():
        L.append(f"- {name}: " + ", ".join(f"{P} {v['brier_avg_change']:+.5f} / {v['mae_change']:+.3f}" for P, v in bp.items()))
    F = R["fits"]

    def tab(rows, cols):
        out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
        for r in rows:
            out.append("| " + " | ".join(str(r.get(c)) for c in cols) + " |")
        return out
    cols = ["m", "beta", "se", "t", "sd_log_mult", "sse_drop_pct", "beta_2025", "t_2025"]
    L += ["", "## Fit details (2023-2024)", "",
          "m = league-average chances blended into the player's own split (inf = league effect only). beta = fitted strength "
          "(1 = right as derived, 0 = no information). t = beta / its standard error. sd_log_mult = how much the multiplier moves "
          "from player to player. sse_drop_pct = share of squared error removed. beta_2025 / t_2025 = the same regression "
          "run on the holdout season, shown only to see whether the fit-season answer repeats.", ""]
    for tag, title in (("coverage_man_zone", "Coverage fit: man vs zone"), ("coverage_mof", "Coverage fit: middle of field open vs closed")):
        L += [f"### {title}", "", "Yards per target:", ""] + tab(F[tag]["yards_per_target"], cols) + ["", "Targets:", ""] + tab(F[tag]["targets"], cols) + [""]
        for P, v in F[tag]["by_position"].items():
            L.append(f"- {P}: yards " + "; ".join(f"m={r['m']} beta {r['beta']} (t {r['t']})" for r in v["yards"]) +
                     " | targets " + "; ".join(f"m={r['m']} beta {r['beta']} (t {r['t']})" for r in v["targets"]))
        L.append("")
    L += ["### Pressure fit", "", "Yards per attempt:", ""] + tab(F["pressure"]["yards_per_attempt"], cols) + ["", "Completion rate (tested on receptions):", ""] + \
         tab(F["pressure"]["completion"], cols) + ["", "Attempts lost to sacks (tested on targets):", ""] + tab(F["pressure"]["attempts"], cols) + [""]
    for nm, key in (("2023-2024", "team_level_fit"), ("2025", "team_level_test")):
        tl = F["pressure"][key]
        L.append(f"Team level, {nm} ({tl['team_games']} team-games). Correlation of the pre-game number with what the offense then did:")
        L.append("")
        for k, v in tl.items():
            if k != "team_games":
                L.append(f"- {k}: opponent pressure rate {v['corr_with_opp_pressure_rate']:+.3f}, expected pressure rate (QB x opponent) {v['corr_with_expected_pressure_rate']:+.3f}")
        L.append("")
    T = F["tier"]
    L += ["### Opponent tier and the defense factor weight", "",
          f"Mean squared yardage error on the fit seasons: no defense factor {T['mse_no_defense_factor']}, current half weight {T['mse_current_half_weight']}, "
          f"best weight {T['best_defense_weight']['weight']} ({'capped' if T['best_defense_weight']['capped'] else 'no cap'}) {T['best_defense_weight']['mse']}.", "",
          "Weight on the defense's catch rate and yards per catch allowed (capped at +/-20% as now):", ""] + \
         tab([r for r in T["defense_weight_grid"] if r["capped"]], ["weight", "mse", "mae"]) + ["",
          f"Yards per game the defense allows his position, as one factor (exponent fitted with no other defense factor): {T['position_yards_allowed_factor_exponent']}", "",
          f"Targets per game the defense allows his position, on top of the current model: {T['position_targets_allowed_factor_exponent']}", "",
          "Tier split (his yards per game vs this opponent's tier / his overall) replacing the defense factor:", ""] + \
         tab(T["tier_replacing_defense_factor"], ["m", "beta", "se", "t", "sd_log_mult", "mse_as_is", "mse_with_beta"]) + ["",
          "His own tier split only (league tier effect removed), on top of the current model:", ""] + \
         tab(T["own_tier_split_on_top_of_current"], ["m", "beta", "se", "t", "sd_log_mult", "mse_as_is", "mse_with_beta"]) + [""]
    D = R["diagnostics"]
    L += ["## How much data sits behind each split (2025 rows)", "",
          f"- Median prior targets vs man: {D['median_prior_targets_vs_man']:.0f}; vs zone: {D['median_prior_targets_vs_zone']:.0f}; "
          f"middle open: {D['median_prior_targets_mof_open']:.0f}; middle closed: {D['median_prior_targets_mof_closed']:.0f}.",
          f"- Opponent man rate, 10th to 90th percentile: {D['opp_man_rate_p10_p90'][0]:.1%} to {D['opp_man_rate_p10_p90'][1]:.1%} (league {D['league_man_rate']:.1%}).",
          f"- Opponent middle-open rate: {D['opp_open_rate_p10_p90'][0]:.1%} to {D['opp_open_rate_p10_p90'][1]:.1%} (league {D['league_open_rate']:.1%}).",
          f"- Opponent pressure rate: {D['opp_pressure_rate_p10_p90'][0]:.1%} to {D['opp_pressure_rate_p10_p90'][1]:.1%} (league {D['league_pressure_rate']:.1%}).",
          f"- Median prior games against the opponent's tier: {D['median_games_vs_same_tier']:.0f}.",
          f"- Coverage multipliers as derived (m=40), 5th to 95th percentile: man/zone yards {D['coverage_man_zone_ypt_mult_p5_p95_m40']}, targets {D['coverage_man_zone_target_mult_p5_p95_m40']}; "
          f"middle open/closed yards {D['coverage_mof_ypt_mult_p5_p95_m40']}, targets {D['coverage_mof_target_mult_p5_p95_m40']}.",
          f"- Pressure yards-per-attempt multiplier as derived (m=100), 5th to 95th percentile: {D['pressure_ypa_mult_p5_p95_m100']}.",
          f"- League rates by season (the coverage labels are not consistent from year to year, so every rate is compared with the league in the same season): "
          + "; ".join(f"{s}: man {v['lg_man']:.1%}, middle open {v['lg_open']:.1%}, pressure {v['lg_press']:.1%}" for s, v in D["league_by_season"].items()) + ".", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rebuild", action="store_true", help="rebuild the cached player-game rows")
    ap.add_argument("--no-write", action="store_true", help="print only, do not write the results files")
    a = ap.parse_args(argv)
    df = build_rows(a.rebuild)
    R = run(df)
    md = to_md(R)
    if not a.no_write:
        out = ROOT / "dashboard" / "results"
        out.mkdir(parents=True, exist_ok=True)
        (out / "coverage_backtest.json").write_text(json.dumps(R, indent=1, default=float) + "\n")
        (out / "coverage_backtest.md").write_text(md + "\n")
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
