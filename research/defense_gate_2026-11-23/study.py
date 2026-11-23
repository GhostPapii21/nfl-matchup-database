"""Defensive gate and pressure/blitz matchup for the 80-yard stars (asked after Week 11, 2026-11-23).

Owner's idea: star the player, then upgrade (or downgrade) through the "defensive gate" -- what the defense allows -- and,
for receivers, through the pass rush: the defense's pressure and blitz rates against how this QB plays under pressure and
against the blitz.

Base: the board's star models (receivers RX, backs BX + mate_car). Candidates, all from games before kickoff:
  receivers  gate_ypg      yards a game the defense allowed to his position, relative to the league (already partly in
                           g80_pg, the 80-yard games it allowed)
             gate_worst5   defense in the 5 most generous vs his position
             press_match   log(expected QB yards per attempt this game / his usual): his clean and pressured YPA mixed
                           at the defense's pressure rate (NGS participation, 2022-2025)
             blitz_match   same with his YPA vs 5+ rushers and the defense's 5+ rusher rate
  backs      gate_ypc      yards per carry the defense allowed to backs (relative), beyond l_d (RB yards a game)
             gate_worst5   defense in the 5 most generous vs backs (yards a game)
Fit 2022-24, held out 2025-26 (pressure/blitz: 2025 only, participation data ends there). Kept only if held-out log loss
and Brier both improve and |z| >= 2. Also: among players already starred (30%+), hit rate vs predicted by gate thirds --
does the model under-react to soft defenses?

    python3 research/defense_gate_2026-11-23/study.py --data DIR      # DIR as for research/game_types_2026-11-16/test_rb.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
C = ROOT / "pregame" / ".cache"
sys.path.insert(0, str(ROOT / "research" / "star_review_2026-11-23"))
import study as SR  # noqa: E402

RX, BX = SR.RX, SR.BX + ["mate_car"]


def qb_pressure_table():
    """Per (season, week, team): starter's clean/pressured/vs-blitz YPA to date and the opponent defense's pressure and
    5+ rusher rates to date. 2022-2025."""
    rows = []
    for y in (2022, 2023, 2024, 2025):
        pp = pd.read_parquet(C / f"pbp_participation_{y}.parquet", columns=["nflverse_game_id", "play_id", "was_pressure", "number_of_pass_rushers"])
        p = pd.read_parquet(C / f"play_by_play_{y}.parquet", columns=["game_id", "play_id", "season", "week", "season_type", "posteam", "defteam",
                                                                     "qb_dropback", "passer_player_id", "pass_attempt", "sack", "yards_gained", "two_point_attempt"])
        p = p[(p.season_type == "REG") & (p.qb_dropback == 1) & (p.two_point_attempt != 1)]
        p = p.merge(pp.rename(columns={"nflverse_game_id": "game_id"}), on=["game_id", "play_id"], how="inner").dropna(subset=["was_pressure"])
        p["pr"] = p.was_pressure.astype(bool).astype(int)
        p["bl"] = (p.number_of_pass_rushers >= 5).astype(int)
        p["att"] = ((p.pass_attempt == 1) | (p.sack == 1)).astype(int)
        p["y"] = p.yards_gained.fillna(0)
        # starter per team-game
        st = p.groupby(["game_id", "posteam", "passer_player_id"]).size().rename("n").reset_index().sort_values("n").drop_duplicates(["game_id", "posteam"], keep="last")
        g = p.groupby(["season", "week", "game_id", "posteam", "defteam"]).size().rename("db").reset_index().merge(st[["game_id", "posteam", "passer_player_id"]], on=["game_id", "posteam"])
        # QB splits to date (this season, all teams)
        q = p.groupby(["passer_player_id", "week"]).apply(lambda d: pd.Series({
            "c_y": d.y[d.pr == 0].sum(), "c_n": (d.pr == 0).sum(), "p_y": d.y[d.pr == 1].sum(), "p_n": (d.pr == 1).sum(),
            "b_y": d.y[d.bl == 1].sum(), "b_n": (d.bl == 1).sum(), "nb_y": d.y[d.bl == 0].sum(), "nb_n": (d.bl == 0).sum()}), include_groups=False).reset_index()
        q = q.sort_values(["passer_player_id", "week"])
        for c in ("c_y", "c_n", "p_y", "p_n", "b_y", "b_n", "nb_y", "nb_n"):
            q[c] = q.groupby("passer_player_id")[c].transform(lambda s: s.shift().expanding().sum())
        d = p.groupby(["defteam", "week"]).agg(pr=("pr", "sum"), bl=("bl", "sum"), n=("pr", "size")).reset_index().sort_values(["defteam", "week"])
        for c in ("pr", "bl", "n"):
            d[c] = d.groupby("defteam")[c].transform(lambda s: s.shift().expanding().sum())
        lg_pr, lg_bl = p.pr.mean(), p.bl.mean()
        g = g.merge(q, on=["passer_player_id", "week"], how="left").merge(d, on=["defteam", "week"], how="left")
        g["season"] = y
        g = g[(g.c_n >= 60) & (g.p_n >= 20) & (g.b_n >= 20) & (g.n >= 100)]
        ypa_c, ypa_p = g.c_y / g.c_n, g.p_y / g.p_n
        ypa_b, ypa_nb = g.b_y / g.b_n, g.nb_y / g.nb_n
        usual = (g.c_y + g.p_y) / (g.c_n + g.p_n)
        dpr, dbl = g.pr / g.n, g.bl / g.n
        g["press_match"] = np.log(((1 - dpr) * ypa_c + dpr * ypa_p).clip(0.5) / usual.clip(0.5))
        g["blitz_match"] = np.log(((1 - dbl) * ypa_nb + dbl * ypa_b).clip(0.5) / ((g.nb_y + g.b_y) / (g.nb_n + g.b_n)).clip(0.5))
        g["def_pressure_rel"], g["def_blitz_rel"] = dpr / lg_pr, dbl / lg_bl
        rows.append(g[["season", "week", "posteam", "press_match", "blitz_match", "def_pressure_rel", "def_blitz_rel"]].rename(columns={"posteam": "team"}))
    return pd.concat(rows)


def gate_thirds(te, col, label):
    s = te[te.p >= 0.30].copy()
    if s.empty:
        return []
    s["third"] = pd.qcut(s[col].rank(method="first"), 3, labels=["tough", "middle", "soft"])
    return [{"gate": str(k), "starred": int(len(d)), "predicted": round(float(d.p.mean()), 3), "hit80": round(float(d.hit80.mean()), 3),
             "gap_points": round(100 * float(d.hit80.mean() - d.p.mean()), 1)} for k, d in s.groupby("third", observed=True)]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", required=True); a = ap.parse_args()
    import fit as F
    import test_rb as T
    res = {}
    # ---------------- receivers
    r = F.receivers()
    lg = r.groupby(["season", "week", "pos"]).opp_pos_ypg.transform("mean")
    r["gate_ypg"] = r.opp_pos_ypg / lg
    rk = r.groupby(["season", "week", "pos"]).opp_pos_ypg.rank(ascending=False, method="dense")
    r["gate_worst5"] = (rk <= 5).astype(int)
    out, te = SR.evaluate(r, RX, ["gate_ypg", "gate_worst5", "opp_ypa"])
    res["receivers"] = out
    res["receivers_starred_by_gate"] = gate_thirds(te, "gate_ypg", "receivers")
    pq = qb_pressure_table()
    rp = r.merge(pq, on=["season", "week", "team"], how="inner")
    tr, te2 = rp[rp.season <= 2024], rp[rp.season == 2025]
    def run(cols):
        m = sm.GLM(tr.hit80, sm.add_constant(tr[cols].astype(float)), family=sm.families.Binomial()).fit()
        p = m.predict(sm.add_constant(te2[cols].astype(float), has_constant="add")).clip(1e-4, 1 - 1e-4)
        return m, {"logloss": round(float(-(te2.hit80 * np.log(p) + (1 - te2.hit80) * np.log(1 - p)).mean()), 5), "brier": round(float(((p - te2.hit80) ** 2).mean()), 5)}
    _, b0 = run(RX)
    pr = {"rows_train": int(len(tr)), "rows_test_2025": int(len(te2)), "base": b0, "candidates": {}}
    for c in ("press_match", "blitz_match", "def_pressure_rel", "def_blitz_rel"):
        m, s = run(RX + [c])
        z = float(m.params[c] / m.bse[c])
        pr["candidates"][c] = {**s, "coef": round(float(m.params[c]), 4), "z": round(z, 2), "keep": bool(s["logloss"] < b0["logloss"] and s["brier"] < b0["brier"] and abs(z) >= 2)}
    res["receivers_pressure_blitz"] = pr
    # ---------------- backs
    D = Path(a.data)
    b = pd.concat([T.season(y, D) for y in (2022, 2023, 2024, 2025, 2026)]).dropna(subset=["implied"]).reset_index(drop=True)
    b["l_car"], b["l_ypc"], b["l_d"] = np.log(0.6 * b.car_pg + 0.4 * b.car_l3), np.log(b.ypc), np.log(b.d_yds_pg)
    b["hit80"] = (b.y_yds >= 80).astype(int)
    mates = b.groupby(["season", "week", "team"]).car_pg.agg(list).rename("cars").reset_index()
    b = b.merge(mates, on=["season", "week", "team"])
    b["mate_car"] = [max([c for c in cs if c != me] or [0]) if cs.count(me) == 1 else max(cs) for cs, me in zip(b.cars, b.car_pg)]
    b["gate_ypc"] = b.d_ypc / b.groupby(["season", "week"]).d_ypc.transform("mean")
    b["gate_worst5"] = (b.groupby(["season", "week"]).d_yds_pg.rank(ascending=False, method="dense") <= 5).astype(int)
    out, teb = SR.evaluate(b, BX, ["gate_ypc", "gate_worst5"])
    res["backs"] = out
    res["backs_starred_by_gate"] = gate_thirds(teb, "d_yds_pg", "backs")
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
