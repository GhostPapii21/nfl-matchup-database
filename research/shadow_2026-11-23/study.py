"""Three candidate additions to the 80-yard star model, tested before they run side by side with the board
(owner, 2026-11-23): streakiness, rising role, man vs zone.

  streak   l_cv        his game-to-game spread in yards earlier that season (sd / mean, log)
           big80       share of his earlier games with 80+ yards
           ex20_rate   20+ yard catches per target
  role     trend       log(last-3 target share / season share): role rising or falling
           last1       log(last game's target share / season share)
  coverage cov_match   log of his expected yards per target at this defense's man rate, from his own man and zone
                       yards per target earlier that season, over his usual (NGS participation, 2022-2025 only)
Base: the board's receiver star model. Fit 2022-24, held out 2025-26 (coverage: 2025). Passing bar: held-out log loss and
Brier both better, |z| >= 2. Writes results.json and weights.json (weights for the side-by-side run).

    python3 research/shadow_2026-11-23/study.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "pregame" / ".cache"
sys.path.insert(0, str(ROOT / "research" / "watch_model_2026-11-16"))
sys.path.insert(0, str(ROOT / "research" / "star_review_2026-11-23"))
import fit as F  # noqa: E402
import study as SR  # noqa: E402

RX = SR.RX


def add_streak_role(r):
    raw = pd.read_parquet(ROOT / "research" / "receiver_volatility_2026-11-14" / "rows.parquet")[["season", "week", "player", "y_yds", "y_tgt", "y_team_tgts"]]
    raw = raw.sort_values(["player", "season", "week"])
    g = raw.groupby(["player", "season"])
    raw["sd_prior"] = g.y_yds.transform(lambda s: s.shift().expanding().std())
    raw["mean_prior"] = g.y_yds.transform(lambda s: s.shift().expanding().mean())
    raw["big80"] = g.y_yds.transform(lambda s: (s >= 80).astype(float).shift().expanding().mean())
    raw["last_share"] = (raw.y_tgt / raw.y_team_tgts.replace(0, np.nan)).groupby([raw.player, raw.season]).shift()
    r = r.merge(raw[["season", "week", "player", "sd_prior", "mean_prior", "big80", "last_share"]], on=["season", "week", "player"], how="left")
    r["l_cv"] = np.log((r.sd_prior / r.mean_prior.clip(lower=5)).clip(0.1, 3)).fillna(0)
    r["big80"] = r.big80.fillna(0)
    r["trend"] = np.log((r.share_l3 / r.share).clip(0.3, 3))
    r["last1"] = np.log((r.last_share / r.share).clip(0.2, 4)).fillna(0)
    return r


def add_coverage(r):
    fr = []
    for y in (2022, 2023, 2024, 2025):
        pp = pd.read_parquet(C / f"pbp_participation_{y}.parquet", columns=["nflverse_game_id", "play_id", "defense_man_zone_type"]).rename(columns={"nflverse_game_id": "game_id"})
        p = pd.read_parquet(C / f"play_by_play_{y}.parquet", columns=["game_id", "play_id", "season", "week", "season_type", "defteam", "receiver_player_id", "pass_attempt", "receiving_yards", "sack"])
        p = p[(p.season_type == "REG") & (p.pass_attempt == 1) & (p.sack != 1)].merge(pp, on=["game_id", "play_id"])
        p["man"] = p.defense_man_zone_type.fillna("").str.upper().str.contains("MAN").astype(int)
        p["known"] = p.defense_man_zone_type.fillna("").str.upper().str.contains("MAN|ZONE").astype(int)
        p = p[p.known == 1]
        p["y"] = p.receiving_yards.fillna(0)
        fr.append(p)
    p = pd.concat(fr)
    rec = p.dropna(subset=["receiver_player_id"]).groupby(["receiver_player_id", "season", "week"]).apply(lambda d: pd.Series({
        "ym": d.y[d.man == 1].sum(), "tm": (d.man == 1).sum(), "yz": d.y[d.man == 0].sum(), "tz": (d.man == 0).sum()}), include_groups=False).reset_index()
    rec = rec.sort_values(["receiver_player_id", "season", "week"])
    for c in ("ym", "tm", "yz", "tz"):
        rec[c] = rec.groupby(["receiver_player_id", "season"])[c].transform(lambda s: s.shift().expanding().sum())
    dfn = p.groupby(["defteam", "season", "week"]).agg(m=("man", "sum"), n=("man", "size")).reset_index().sort_values(["defteam", "season", "week"])
    for c in ("m", "n"):
        dfn[c] = dfn.groupby(["defteam", "season"])[c].transform(lambda s: s.shift().expanding().sum())
    r = r.merge(rec.rename(columns={"receiver_player_id": "player"}), on=["player", "season", "week"], how="left")
    r = r.merge(dfn.rename(columns={"defteam": "opp"}), on=["opp", "season", "week"], how="left")
    ok = (r.tm >= 10) & (r.tz >= 15) & (r.n >= 150)
    ypt_m, ypt_z, mr = r.ym / r.tm, r.yz / r.tz, r.m / r.n
    usual = (r.ym + r.yz) / (r.tm + r.tz)
    r["cov_match"] = np.where(ok, np.log(((mr * ypt_m + (1 - mr) * ypt_z).clip(0.5)) / usual.clip(0.5)), np.nan)
    return r


def test(d, cands, train_max=2024, test_seasons=(2025, 2026)):
    tr, te = d[d.season <= train_max], d[d.season.isin(test_seasons)]
    def run(cols):
        m = sm.GLM(tr.hit80, sm.add_constant(tr[cols].astype(float)), family=sm.families.Binomial()).fit()
        p = m.predict(sm.add_constant(te[cols].astype(float), has_constant="add")).clip(1e-4, 1 - 1e-4)
        return m, {"logloss": round(float(-(te.hit80 * np.log(p) + (1 - te.hit80) * np.log(1 - p)).mean()), 5), "brier": round(float(((p - te.hit80) ** 2).mean()), 5)}
    _, b0 = run(RX)
    out = {"train": int(len(tr)), "test": int(len(te)), "base": b0, "candidates": {}}
    for name, cols in cands.items():
        m, s = run(RX + cols)
        zs = {c: round(float(m.params[c] / m.bse[c]), 2) for c in cols}
        out["candidates"][name] = {**s, "coef": {c: round(float(m.params[c]), 4) for c in cols}, "z": zs,
                                   "pass": bool(s["logloss"] < b0["logloss"] and s["brier"] < b0["brier"] and max(abs(v) for v in zs.values()) >= 2)}
    return out


def main():
    r = add_streak_role(F.receivers())
    res = {"streak_and_role": test(r, {"streak: spread (l_cv)": ["l_cv"], "streak: 80+ game share": ["big80"], "streak: 20+ catch rate": ["ex20_rate"],
                                       "streak: all three": ["l_cv", "big80", "ex20_rate"], "role: 3-game trend": ["trend"], "role: last game": ["last1"],
                                       "role: both": ["trend", "last1"]})}
    rc = add_coverage(r)
    rc = rc[rc.season <= 2025].dropna(subset=["cov_match"])
    res["coverage"] = test(rc, {"man vs zone match": ["cov_match"]}, test_seasons=(2025,))
    weights = {}
    for name, cols in (("streak", ["l_cv", "big80", "ex20_rate"]), ("role", ["trend", "last1"])):
        m = sm.GLM(r.hit80, sm.add_constant(r[RX + cols].astype(float)), family=sm.families.Binomial()).fit()      # all seasons, for the live side-by-side
        weights[name] = {k: round(float(v), 5) for k, v in m.params.items()}
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    (HERE / "weights.json").write_text(json.dumps(weights, indent=1) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
