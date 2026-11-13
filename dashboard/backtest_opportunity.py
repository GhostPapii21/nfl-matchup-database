#!/usr/bin/env python3
"""Backtest the opportunity check on past games, using only what was known before each game.

    python3 -m dashboard.backtest_opportunity --seasons 2024 2025 2026

For every team game from week 5 on, each active pass catcher with 8+ targets (and each active running back with 15+
carries) over the team's previous 8 games is projected with the same simulation the board uses
(dashboard/opportunity.py). Inputs come only from earlier weeks: his share and rates, the team's pace and pass mix, the
opponent's allowed rates by position, the closing spread for the script, and the previous season's league per-catch and
per-carry outcomes. Weather and injury bumps are not applied here (no historical forecasts or reports are stored).

It reports, for each threshold, the Brier score of the simulation against a baseline (how often the player hit that
number in his own previous games, shrunk toward the league), and a calibration table: when the simulation said X%,
how often it happened. Writes dashboard/results/opportunity_backtest.json and .md.
"""
from __future__ import annotations

import argparse
import json
import zlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from dashboard import opportunity as O  # noqa: E402

CACHE = ROOT / "pregame" / ".cache"
REC_T = {"yards": (40, 60, 70, 80, 100), "receptions": (4, 6)}
RUSH_T = {"yards": (50, 70, 90), "carries": (12, 15)}
WINDOW = 8
NS = 4000


def load(season):
    p = pd.read_parquet(CACHE / f"play_by_play_{season}.parquet")
    p = p[p.season_type == "REG"]
    r = pd.read_parquet(CACHE / f"roster_weekly_{season}.parquet")
    r = r[r.game_type == "REG"]
    return p, r


def team_tables(p, pos):
    q = p[p.two_point_attempt != 1].copy()
    q["rpos"] = q.receiver_player_id.map(pos)
    q["tgt"] = ((q.pass_attempt == 1) & (q.sack != 1) & q.receiver_player_id.notna()).astype(int)
    q["att"] = ((q.pass_attempt == 1) & (q.sack != 1)).astype(int)
    q["car"] = ((q.rush_attempt == 1) & (q.qb_scramble != 1)).astype(int)
    q["play"] = q.play_type.isin(["pass", "run"]).astype(int)
    q["rbcar"] = (q.car == 1) & (q.rusher_player_id.map(pos) == "RB")
    agg = {"play": "sum", "att": "sum", "car": "sum", "tgt": "sum"}
    off = q.groupby(["game_id", "week", "posteam"]).agg(agg).reset_index()
    rows = []
    for (gid, wk, dfn), g in q.groupby(["game_id", "week", "defteam"]):
        d = {"game_id": gid, "week": wk, "defteam": dfn, "plays": int(g.play.sum())}
        for P in ("WR", "TE", "RB"):
            x = g[(g.rpos == P) & (g.tgt == 1)]
            d[f"{P}_tgt"], d[f"{P}_rec"], d[f"{P}_yds"] = int(len(x)), int(x.complete_pass.sum()), float(x.receiving_yards.fillna(0).sum())
        rb = g[g.rbcar]
        d["rb_car"], d["rb_yds"] = int(len(rb)), float(rb.rushing_yards.fillna(0).sum())
        rows.append(d)
    dfn = pd.DataFrame(rows)
    rec = q[q.tgt == 1].groupby(["game_id", "week", "posteam", "receiver_player_id"]).agg(
        targets=("tgt", "sum"), receptions=("complete_pass", "sum"), yards=("receiving_yards", lambda s: float(s.fillna(0).sum()))).reset_index()
    ru = q[q.car == 1].groupby(["game_id", "week", "posteam", "rusher_player_id"]).agg(
        carries=("car", "sum"), yards=("rushing_yards", lambda s: float(s.fillna(0).sum()))).reset_index()
    return off, dfn, rec, ru


def run_season(season, prev_season, rng_seed=0):
    p, r = load(season)
    pp, pr = load(prev_season)
    pos = dict(zip(pd.concat([pr, r]).gsis_id, pd.concat([pr, r]).position))
    pools = O.league_pools(pp, pr)
    games = pd.read_parquet(CACHE / "games.parquet")
    games = games[(games.season == season) & (games.game_type == "REG") & games.home_score.notna()]
    off, dfn, rec, ru = team_tables(p, pos)
    act = r[r.status == "ACT"][["week", "team", "gsis_id"]]
    active = set(zip(act.week, act.team, act.gsis_id))
    out = []
    for g in games.itertuples():
        if g.week < 5:
            continue
        for team, opp, home in ((g.home_team, g.away_team, True), (g.away_team, g.home_team, False)):
            to = off[(off.posteam == team) & (off.week < g.week)].sort_values("week").tail(WINDOW)
            do = dfn[(dfn.defteam == opp) & (dfn.week < g.week)].sort_values("week").tail(WINDOW)
            if len(to) < 4 or len(do) < 4:
                continue
            plays = (to.play.mean() + do.plays.mean()) / 2
            pass_ratio = to.att.sum() / max(to.play.sum(), 1)
            margin = (g.spread_line if home else -g.spread_line) if pd.notna(g.spread_line) else None
            pmul, rmul = O.script_multipliers(margin)
            team_att, team_rush = plays * pass_ratio * pmul, plays * (1 - pass_ratio) * rmul
            gids = set(to.game_id)
            prior_rec = rec[(rec.posteam == team) & rec.game_id.isin(gids)]
            prior_ru = ru[(ru.posteam == team) & ru.game_id.isin(gids)]
            team_tg_by_game = to.set_index("game_id").tgt.to_dict()
            team_car_by_game = to.set_index("game_id").car.to_dict()
            now_rec = rec[(rec.game_id == g.game_id) & (rec.posteam == team)].set_index("receiver_player_id")
            now_ru = ru[(ru.game_id == g.game_id) & (ru.posteam == team)].set_index("rusher_player_id")
            for pid, h in prior_rec.groupby("receiver_player_id"):
                P = pos.get(pid)
                if P not in ("WR", "TE", "RB") or h.targets.sum() < 8 or (g.week, team, pid) not in active:
                    continue
                h = h.sort_values("week")
                share = h.targets.sum() / sum(team_tg_by_game[x] for x in h.game_id)
                l3 = h.tail(3)
                s3 = l3.targets.sum() / max(sum(team_tg_by_game[x] for x in l3.game_id), 1)
                su = 0.6 * share + 0.4 * s3 if len(h) >= 5 else share
                cr = O.shrink(h.receptions.sum(), h.targets.sum(), pools["catch_rate"][P], O.PRIOR_TARGETS)
                ypr = O.shrink(h.yards.sum(), h.receptions.sum(), pools["ypr"][P], O.PRIOR_CATCHES)
                d_cr = do[f"{P}_rec"].sum() / max(do[f"{P}_tgt"].sum(), 1)
                d_ypr = do[f"{P}_yds"].sum() / max(do[f"{P}_rec"].sum(), 1)
                exp_t = team_att * su
                k = O._dispersion(list(h.targets), exp_t)
                tg, rc, yd = O.simulate_receiver(exp_targets=exp_t, k=k, catch_rate=cr * O.def_factor(d_cr, pools["catch_rate"][P]),
                                                 ypr=ypr * O.def_factor(d_ypr, pools["ypr"][P]), pool=pools["catch"][P], n=NS, seed=zlib.crc32(f'{season}{g.game_id}{pid}'.encode()))
                act_y = float(now_rec.yards.get(pid, 0.0)) if pid in now_rec.index else 0.0
                act_r = int(now_rec.receptions.get(pid, 0)) if pid in now_rec.index else 0
                row = {"season": season, "week": int(g.week), "kind": "rec", "pos": P, "player": pid, "exp_targets": exp_t,
                       "pred_yards_mean": float(yd.mean()), "actual_yards": act_y,
                       "actual_targets": int(now_rec.targets.get(pid, 0)) if pid in now_rec.index else 0, "games_prior": len(h), "share": su}
                for t in REC_T["yards"]:
                    row[f"p_y{t}"] = float((yd >= t).mean()); row[f"a_y{t}"] = int(act_y >= t)
                    row[f"b_y{t}"] = (int((h.yards >= t).sum()) + 2 * 0.25) / (len(h) + 2)
                for t in REC_T["receptions"]:
                    row[f"p_r{t}"] = float((rc >= t).mean()); row[f"a_r{t}"] = int(act_r >= t)
                    row[f"b_r{t}"] = (int((h.receptions >= t).sum()) + 2 * 0.3) / (len(h) + 2)
                out.append(row)
            for pid, h in prior_ru.groupby("rusher_player_id"):
                if pos.get(pid) != "RB" or h.carries.sum() < 15 or (g.week, team, pid) not in active:
                    continue
                h = h.sort_values("week")
                share = h.carries.sum() / sum(team_car_by_game[x] for x in h.game_id)
                l3 = h.tail(3)
                s3 = l3.carries.sum() / max(sum(team_car_by_game[x] for x in l3.game_id), 1)
                su = 0.6 * share + 0.4 * s3 if len(h) >= 5 else share
                ypc = O.shrink(h.yards.sum(), h.carries.sum(), pools["ypc"], O.PRIOR_CARRIES)
                d_ypc = do.rb_yds.sum() / max(do.rb_car.sum(), 1)
                exp_c = team_rush * su
                k = O._dispersion(list(h.carries), exp_c)
                car, yd = O.simulate_rusher(exp_carries=exp_c, k=k, ypc=ypc * O.def_factor(d_ypc, pools["ypc"]), pool=pools["carry"], n=NS,
                                            seed=zlib.crc32(f'{season}{g.game_id}{pid}r'.encode()))
                act_y = float(now_ru.yards.get(pid, 0.0)) if pid in now_ru.index else 0.0
                act_c = int(now_ru.carries.get(pid, 0)) if pid in now_ru.index else 0
                row = {"season": season, "week": int(g.week), "kind": "rush", "pos": "RB", "player": pid, "exp_carries": exp_c,
                       "pred_yards_mean": float(yd.mean()), "actual_yards": act_y,
                       "actual_carries": act_c, "games_prior": len(h), "share": su}
                for t in RUSH_T["yards"]:
                    row[f"p_y{t}"] = float((yd >= t).mean()); row[f"a_y{t}"] = int(act_y >= t)
                    row[f"b_y{t}"] = (int((h.yards >= t).sum()) + 2 * 0.3) / (len(h) + 2)
                for t in RUSH_T["carries"]:
                    row[f"p_c{t}"] = float((car >= t).mean()); row[f"a_c{t}"] = int(act_c >= t)
                    row[f"b_c{t}"] = (int((h.carries >= t).sum()) + 2 * 0.3) / (len(h) + 2)
                out.append(row)
    return out


def evaluate(df):
    res = {}
    for kind, spec in (("rec", {"y": REC_T["yards"], "r": REC_T["receptions"]}), ("rush", {"y": RUSH_T["yards"], "c": RUSH_T["carries"]})):
        d = df[df.kind == kind]
        if not len(d):
            continue
        rows = []
        for pre, ts in spec.items():
            for t in ts:
                p, a, b = d[f"p_{pre}{t}"], d[f"a_{pre}{t}"], d[f"b_{pre}{t}"]
                bins = pd.cut(p, [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0001], right=False)
                cal = d.assign(bin=bins).groupby("bin", observed=True).agg(n=(f"a_{pre}{t}", "size"), predicted=(f"p_{pre}{t}", "mean"), actual=(f"a_{pre}{t}", "mean")).reset_index()
                rows.append({"stat": {"y": "yards", "r": "receptions", "c": "carries"}[pre], "threshold": t, "n": int(len(d)),
                             "hit_rate": round(float(a.mean()), 3), "avg_predicted": round(float(p.mean()), 3),
                             "brier_sim": round(float(((p - a) ** 2).mean()), 4), "brier_own_history": round(float(((b - a) ** 2).mean()), 4),
                             "calibration": [{"bin": str(x.bin), "n": int(x.n), "predicted": round(float(x.predicted), 3), "actual": round(float(x.actual), 3)} for x in cal.itertuples()]})
        res[kind] = {"player_games": int(len(d)), "mean_abs_error_yards": round(float((d.pred_yards_mean - d.actual_yards).abs().mean()), 2),
                     "thresholds": rows}
    return res


def to_md(res, seasons):
    L = [f"# Opportunity check backtest ({', '.join(map(str, seasons))}, weeks 5+)", "",
         "Every projection uses only earlier weeks. Brier score: lower is better; the baseline is the player's own hit rate in his previous games.", ""]
    for kind, title in (("rec", "Pass catchers"), ("rush", "Running backs")):
        if kind not in res:
            continue
        R = res[kind]
        L += [f"## {title}: {R['player_games']} player-games, average yardage miss {R['mean_abs_error_yards']} yards", "",
              "| Stat | Line | Hit rate | Avg predicted | Brier (simulation) | Brier (own history) |", "| --- | --- | --- | --- | --- | --- |"]
        for t in R["thresholds"]:
            L.append(f"| {t['stat']} | {t['threshold']}+ | {t['hit_rate']:.1%} | {t['avg_predicted']:.1%} | {t['brier_sim']} | {t['brier_own_history']} |")
        L += ["", "Calibration (when the simulation said this, it happened this often):", ""]
        for t in R["thresholds"]:
            L.append(f"- {t['stat']} {t['threshold']}+: " + ", ".join(f"{c['bin']} said {c['predicted']:.0%}, hit {c['actual']:.0%} (n={c['n']})" for c in t["calibration"]))
        L.append("")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seasons", type=int, nargs="+", default=[2024, 2025, 2026])
    ap.add_argument("--share-cv", type=float, help="override the share uncertainty for both kinds (tuning)")
    ap.add_argument("--raw", action="store_true", help="no volume correction (shows the uncorrected model)")
    a = ap.parse_args(argv)
    if a.share_cv is not None:
        O.SHARE_CV = {"rec": a.share_cv, "rush": a.share_cv}
    if a.raw:
        O.VOLUME_CAL = {"rec": (0.0, 1.0), "rush": (0.0, 1.0)}
    rows = []
    for s in a.seasons:
        rows += run_season(s, s - 1)
        print(f"backtest: season {s}: {len(rows)} player-games so far")
    df = pd.DataFrame(rows)
    df.to_parquet(ROOT / "pregame" / ".cache" / "opportunity_backtest_rows.parquet")
    res = evaluate(df)
    res["fit_seasons_2024_2025"] = evaluate(df[df.season < 2026])
    res["holdout_2026"] = evaluate(df[df.season == 2026])
    out = ROOT / "dashboard" / "results"
    out.mkdir(parents=True, exist_ok=True)
    (out / "opportunity_backtest.json").write_text(json.dumps({"seasons": a.seasons, **res}, indent=1) + "\n")
    (out / "opportunity_backtest.md").write_text(to_md(res, a.seasons) + "\n")
    print(to_md(res, a.seasons))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
