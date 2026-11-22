"""Do game situations change receiver output beyond what the projection already expects?

Base projection: the repo's yards and targets GLMs (research/opportunity_tiers_2026-11-14/equations.py inputs), fit on
2022-2024. Each situation is then tested as a multiplier on top of that projection (Poisson GLM with offset =
log(projection)): coefficient, 95% CI, and whether adding it improves out-of-sample deviance on 2025-2026.
Situations (all known before kickoff): off bye (rest >= 13), short week (rest <= 5), international game, first game
after an international game, rain/snow in the forecast text, wind >= 15 mph outdoors, temp <= 32 F outdoors, indoor,
team on a 2+ game losing streak, team on a 3+ game win streak, home, starting QB changed (qb_changed), divisional game."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research" / "opportunity_tiers_2026-11-14"))
import equations as E  # noqa: E402
import study as S  # noqa: E402

WET = re.compile(r"rain|shower|drizzle|snow|sleet|storm|thunder|flurr", re.I)


def context():
    g = pd.read_parquet(ROOT / "pregame" / ".cache" / "games.parquet")
    g = g[g.game_type == "REG"].copy()
    wx = []
    for y in sorted(g.season.unique()):
        f = ROOT / "pregame" / ".cache" / f"play_by_play_{y}.parquet"
        if f.exists():
            p = pd.read_parquet(f, columns=["game_id", "weather"])
            wx.append(p.dropna().groupby("game_id").weather.first())
    wx = pd.concat(wx)
    rows = []
    for r in g.itertuples():
        for team, rest, home, opp_score, my_score in ((r.home_team, r.home_rest, 1, r.away_score, r.home_score),
                                                      (r.away_team, r.away_rest, 0, r.home_score, r.away_score)):
            rows.append({"season": r.season, "week": r.week, "game_id": r.game_id, "team": team, "rest": rest, "home": home,
                         "intl": int(r.location == "Neutral"), "div": int(r.div_game == 1),
                         "wet": int(r.roof not in ("dome", "closed") and bool(WET.search(str(wx.get(r.game_id, ""))))),
                         "result": None if pd.isna(my_score) else np.sign(my_score - opp_score)})
    t = pd.DataFrame(rows).sort_values(["team", "season", "week"])
    t["after_intl"] = t.groupby(["team", "season"]).intl.shift(1).fillna(0).astype(int)
    prev = t.groupby(["team", "season"]).result.shift(1)
    prev2 = t.groupby(["team", "season"]).result.shift(2)
    prev3 = t.groupby(["team", "season"]).result.shift(3)
    t["lose2"] = ((prev < 0) & (prev2 < 0)).astype(int)
    t["win3"] = ((prev > 0) & (prev2 > 0) & (prev3 > 0)).astype(int)
    t["off_bye"] = (t.rest >= 13).astype(int)
    t["short_week"] = (t.rest <= 5).astype(int)
    return t.drop(columns=["result", "rest"])


def main():
    r = E.prep(S.load())
    tr = r[r.season.isin(S.TRAIN)]
    Xy = ["log_tgt", "log_ypt", "imp_c", "log_def_pos"]
    my = sm.GLM(tr.y_yds, sm.add_constant(tr[Xy]), family=sm.families.Poisson()).fit(scale="X2")
    mt = sm.GLM(tr.y_tgt, sm.add_constant(tr[["log_tgt", "imp_c", "log_def_pos"]]), family=sm.families.Poisson()).fit(scale="X2")
    r["pred_yds"] = my.predict(sm.add_constant(r[Xy], has_constant="add"))
    r["pred_tgt"] = mt.predict(sm.add_constant(r[["log_tgt", "imp_c", "log_def_pos"]], has_constant="add"))
    r = r.merge(context(), on=["season", "week", "game_id", "team"], how="left")
    outdoor = ~r.roof.isin(["dome", "closed"])
    r["windy"] = (outdoor & (r.wind.fillna(0) >= 15)).astype(int)
    r["cold"] = (outdoor & (r.temp.fillna(60) <= 32)).astype(int)
    r["indoor"] = (~outdoor).astype(int)
    r["qb_new"] = r.qb_changed.fillna(0).astype(int)
    ctx = ["off_bye", "short_week", "intl", "after_intl", "wet", "windy", "cold", "indoor", "lose2", "win3", "home", "qb_new", "div"]
    r[ctx] = r[ctx].fillna(0)
    out = {"n": int(len(r)), "seasons": sorted(int(s) for s in r.season.unique()), "effects": {}}
    for target, pred in (("y_yds", "pred_yds"), ("y_tgt", "pred_tgt")):
        res = {}
        full = sm.GLM(r[target], sm.add_constant(r[ctx]), family=sm.families.Poisson(), offset=np.log(r[pred])).fit(scale="X2")
        trn, tst = r[r.season.isin(S.TRAIN)], r[r.season.isin(S.TEST)]
        m_tr = sm.GLM(trn[target], sm.add_constant(trn[ctx]), family=sm.families.Poisson(), offset=np.log(trn[pred])).fit(scale="X2")
        for c in ctx:
            b, se = full.params[c], full.bse[c]
            res[c] = {"games": int(r[c].sum()), "multiplier": round(float(np.exp(b)), 3), "ci95": [round(float(np.exp(b - 1.96 * se)), 3), round(float(np.exp(b + 1.96 * se)), 3)],
                      "significant": bool(abs(b / se) > 1.96), "train_only_multiplier": round(float(np.exp(m_tr.params[c])), 3),
                      "raw_actual_vs_projection": round(float(r.loc[r[c] == 1, target].sum() / r.loc[r[c] == 1, pred].sum()), 3) if r[c].sum() else None}
        mu0 = tst[pred]
        mu1 = m_tr.predict(sm.add_constant(tst[ctx], has_constant="add"), offset=np.log(tst[pred]))

        def dev(y, mu):
            y = y.values
            mu = np.asarray(mu)
            return float(2 * np.sum(np.where(y > 0, y * np.log(np.where(y > 0, y, 1) / mu), 0) - (y - mu)))
        out["effects"][target] = {"by_situation": res, "test_deviance_base": round(dev(tst[target], mu0), 1),
                                  "test_deviance_with_context": round(dev(tst[target], mu1), 1),
                                  "test_mae_base": round(float(np.mean(np.abs(tst[target] - mu0))), 3),
                                  "test_mae_with_context": round(float(np.mean(np.abs(tst[target] - mu1))), 3)}
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    for target in out["effects"]:
        e = out["effects"][target]
        print(f"\n{target}: test deviance {e['test_deviance_base']} -> {e['test_deviance_with_context']}; MAE {e['test_mae_base']} -> {e['test_mae_with_context']}")
        for c, v in e["by_situation"].items():
            print(f"  {c:<11} n={v['games']:>5}  x{v['multiplier']:.3f}  CI {v['ci95']}  {'SIG' if v['significant'] else '   '}  train-only x{v['train_only_multiplier']:.3f}  raw {v['raw_actual_vs_projection']}")


if __name__ == "__main__":
    main()
