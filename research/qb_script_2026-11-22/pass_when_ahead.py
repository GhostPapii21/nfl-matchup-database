"""Do some teams keep throwing when they're ahead (Josh Allen, Week 11: 46 attempts while BUF led all game)?

Team-game base as in study.py (plays x pass ratio to date). Added: the team's pass rate over expected (nflverse pass_oe,
dropbacks vs the model's expected pass rate) on plays while LEADING by 7+, earlier that season (20+ such plays). Does a
favourite with a high 'pass when ahead' rate throw more than the base, beyond the refit script rule? Fit 2022-24, test 2025-26.

    python3 research/qb_script_2026-11-22/pass_when_ahead.py     # writes pass_when_ahead.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
C = HERE.parents[1] / "pregame" / ".cache"
import study as Q  # noqa: E402


def main():
    t = Q.team_games(Q.games())
    fr = []
    for y in range(2022, 2027):
        p = pd.read_parquet(C / f"play_by_play_{y}.parquet", columns=["game_id", "season", "week", "season_type", "posteam", "defteam", "play_type",
                                                                     "pass_attempt", "pass_oe", "score_differential"])
        fr.append(p[(p.season_type == "REG") & p.play_type.isin(["pass", "run"])])
    p = pd.concat(fr)
    tg = p.groupby(["season", "week", "game_id", "posteam", "defteam"]).agg(plays=("play_type", "size"), att=("pass_attempt", "sum")).reset_index()
    ah = p[(p.score_differential >= 7) & p.pass_oe.notna()].groupby(["season", "week", "posteam"]).agg(oe=("pass_oe", "sum"), n=("pass_oe", "size")).reset_index()
    tg = tg.merge(ah, on=["season", "week", "posteam"], how="left").fillna({"oe": 0, "n": 0}).sort_values(["season", "posteam", "week"])
    for c in ("plays", "att", "oe", "n"):
        tg[c + "_td"] = tg.groupby(["season", "posteam"])[c].transform(lambda s: s.shift().expanding().sum())
    tg["k"] = tg.groupby(["season", "posteam"]).cumcount()
    al = tg.sort_values(["season", "defteam", "week"]).copy()
    al["opp_allowed"] = al.groupby(["season", "defteam"]).plays.transform(lambda s: s.shift().expanding().mean())
    al["ok"] = al.groupby(["season", "defteam"]).cumcount()
    tg = tg.merge(al[["game_id", "defteam", "opp_allowed", "ok"]], on=["game_id", "defteam"])
    tg = tg.merge(t[["game_id", "team", "margin"]], left_on=["game_id", "posteam"], right_on=["game_id", "team"])
    tg = tg[(tg.k >= 3) & (tg.ok >= 3) & (tg.n_td >= 20)].copy()
    tg["base"] = (tg.plays_td / tg.k + tg.opp_allowed) / 2 * (tg.att_td / tg.plays_td)
    tg["pmul"] = 0.9855 - 0.0006 * tg.margin.clip(-10, 10)
    tg["pred"] = tg.base * tg.pmul
    tg["ahead_oe"] = tg.oe_td / tg.n_td             # percentage points (pass_oe is in %)
    tr, te = tg[tg.season <= 2024], tg[tg.season >= 2025]
    fav = lambda d: d[d.margin >= 3]
    # fit: att = pred * (1 + b * margin_capped * ahead_oe/100) on favourites
    x = lambda d: d.pred * d.margin.clip(0, 10) * d.ahead_oe / 100
    f = fav(tr)
    b = float(((f.att - f.pred) * x(f)).sum() / (x(f) ** 2).sum())
    def mae(d, bb):
        return round(float(np.abs(d.att - (d.pred + bb * x(d))).mean()), 3)
    res = {"rows_train_fav": int(len(f)), "rows_test_fav": int(len(fav(te))), "b": round(b, 4),
           "test_fav_mae_refit_rule": mae(fav(te), 0.0), "test_fav_mae_with_ahead_oe": mae(fav(te), b)}
    q = fav(te).assign(grp=pd.qcut(fav(te).ahead_oe, 3, labels=["low", "mid", "high"]))
    res["test_fav_by_pass_when_ahead_third"] = [{"third": str(k), "games": int(len(d)), "ahead_oe_avg": round(float(d.ahead_oe.mean()), 1),
                                                 "actual_over_refit": round(float(d.att.sum() / d.pred.sum()), 3)} for k, d in q.groupby("grp", observed=True)]
    qt = fav(tr).assign(grp=pd.qcut(fav(tr).ahead_oe, 3, labels=["low", "mid", "high"]))
    res["train_fav_by_pass_when_ahead_third"] = [{"third": str(k), "games": int(len(d)), "ahead_oe_avg": round(float(d.ahead_oe.mean()), 1),
                                                  "actual_over_refit": round(float(d.att.sum() / d.pred.sum()), 3)} for k, d in qt.groupby("grp", observed=True)]
    buf = tg[(tg.posteam == "BUF") & (tg.season == 2026)].tail(3)[["week", "margin", "att", "pred", "ahead_oe"]]
    res["buf_2026_last3"] = buf.round(2).to_dict("records")
    (HERE / "pass_when_ahead.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
