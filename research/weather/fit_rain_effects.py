#!/usr/bin/env python3
"""Measure what rain does to passing, from nflverse play-by-play (2018 onward), and write the coefficients.

Each team-game is compared with the same team's dry games in the same season (team-season fixed effects), so a good
passing team playing in rain is compared with itself, not with the league. Wind is fitted alongside rain, because
rainy games are windier and wind hurts passing on its own.

Rain tiers come from the game's recorded weather text (the `weather` field), which is free text written by the
home team's staff:
    light     "light rain", "drizzle", "showers", "mist"
    rain      "rain" with no qualifier (the common label; treat as moderate)
    heavy     "heavy", "steady", "pouring", "downpour", storms, or plain rain with wind of 15+ mph
The text rarely says "heavy", so the heavy tier is mostly rain-plus-wind games. That is a proxy, and it is stated
in the output.

    python3 research/weather/fit_rain_effects.py <dir with play_by_play_YYYY.parquet files> [more files...]
Writes research/weather/rain_effects.json. Research only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
COLS = ["game_id", "season", "season_type", "week", "posteam", "defteam", "weather", "roof", "wind", "temp", "play_type", "down", "qb_dropback",
        "pass_attempt", "complete_pass", "sack", "yards_gained", "air_yards", "interception", "rush_attempt", "qb_scramble", "receiver_player_id",
        "two_point_attempt", "fumble_lost", "yards_after_catch"]
METRICS = ["attempts", "completion_pct", "yards_per_attempt", "yards_per_completion", "pass_yards", "adot", "deep_share", "pass_rate", "int_rate",
           "sack_rate", "yac_per_completion", "wr_target_share", "te_target_share", "rb_target_share", "wr_catch_rate", "te_catch_rate", "rb_catch_rate",
           "wr_yards_per_target", "te_yards_per_target", "rb_yards_per_target"]


def rain_tier(text: str, wind) -> str:
    t = str(text or "").split("Temp:")[0].lower()
    if re.search(r"snow|sleet|flurr|freezing", t):
        return "snow"
    if re.search(r"chance|threat|possible|forecast|expected|%", t) and not re.search(r"raining|steady", t):
        return "dry"                                         # a forecast of rain is not rain
    if not re.search(r"rain|shower|drizzl|mist|storm|pour", t):
        return "dry"
    w = float(wind) if wind is not None and not pd.isna(wind) else 0.0
    if re.search(r"heavy|steady|pour|downpour|storm|hurricane", t):
        return "heavy"
    if re.search(r"light|drizzl|shower|mist", t):
        return "light"
    return "heavy" if w >= 15 else "rain"


def team_games(pbp: pd.DataFrame, pos: pd.Series) -> pd.DataFrame:
    p = pbp[pbp.play_type.isin(["pass", "run"]) & pbp.down.notna() & (pbp.two_point_attempt.fillna(0) == 0) & (pbp.season_type == "REG")].copy()
    n = lambda c: pd.to_numeric(p[c], errors="coerce").fillna(0.0)
    sack = n("sack") == 1
    p["att"] = ((n("pass_attempt") == 1) & ~sack).astype(float)
    p["cmp"] = (n("complete_pass") == 1).astype(float)
    p["yds"] = np.where(p.cmp == 1, n("yards_gained"), 0.0)
    p["air"] = np.where(p.att == 1, n("air_yards"), 0.0)
    p["deep"] = ((p.att == 1) & (n("air_yards") >= 20)).astype(float)
    p["db"] = (n("qb_dropback") == 1).astype(float)
    p["sk"] = sack.astype(float)
    p["int"] = (n("interception") == 1).astype(float)
    p["yac"] = np.where(p.cmp == 1, n("yards_after_catch"), 0.0)
    p["play"] = 1.0
    rp = p.receiver_player_id.map(pos).replace({"FB": "RB"})
    for g in ("WR", "TE", "RB"):
        m = (p.att == 1) & (rp == g)
        p[f"{g}_t"] = m.astype(float); p[f"{g}_c"] = (m & (p.cmp == 1)).astype(float); p[f"{g}_y"] = np.where(m, p.yds, 0.0)
    p["tgt"] = ((p.att == 1) & p.receiver_player_id.notna()).astype(float)
    keys = ["game_id", "season", "posteam"]
    s = p.groupby(keys, as_index=False)[["att", "cmp", "yds", "air", "deep", "db", "sk", "int", "yac", "play", "tgt", "WR_t", "WR_c", "WR_y", "TE_t", "TE_c", "TE_y", "RB_t", "RB_c", "RB_y"]].sum()
    meta = pbp.drop_duplicates("game_id")[["game_id", "weather", "roof", "wind", "temp"]]
    s = s.merge(meta, on="game_id", how="left")
    d = lambda a, b: np.where(b > 0, a / np.where(b > 0, b, 1), np.nan)
    out = s[keys + ["weather", "roof", "wind", "temp"]].copy()
    out["attempts"] = s.att; out["completion_pct"] = d(s.cmp, s.att); out["yards_per_attempt"] = d(s.yds, s.att); out["yards_per_completion"] = d(s.yds, s.cmp)
    out["pass_yards"] = s.yds; out["adot"] = d(s.air, s.att); out["deep_share"] = d(s.deep, s.att); out["pass_rate"] = d(s.db, s.play)
    out["int_rate"] = d(s["int"], s.att); out["sack_rate"] = d(s.sk, s.db); out["yac_per_completion"] = d(s.yac, s.cmp)
    for g in ("WR", "TE", "RB"):
        k = g.lower()
        out[f"{k}_target_share"] = d(s[f"{g}_t"], s.tgt); out[f"{k}_catch_rate"] = d(s[f"{g}_c"], s[f"{g}_t"]); out[f"{k}_yards_per_target"] = d(s[f"{g}_y"], s[f"{g}_t"])
    return out


def fit(tg: pd.DataFrame) -> dict:
    tg = tg[tg.attempts >= 10].copy()
    tg["outdoor"] = tg.roof.isin(["outdoors", "open"])
    tg["tier"] = [rain_tier(w, wd) if o else "indoor" for w, wd, o in zip(tg.weather, tg.wind, tg.outdoor)]
    tg = tg[tg.tier != "snow"]
    tg["wind_mph"] = np.where(tg.outdoor, pd.to_numeric(tg.wind, errors="coerce").fillna(0.0), 0.0)
    tg["wind10"] = np.clip(tg.wind_mph - 10, 0, None) / 10.0            # per 10 mph above 10
    counts = {k: int(v) for k, v in tg.tier.value_counts().items()}
    res = {"team_games": int(len(tg)), "team_games_by_tier": counts, "effects": {}, "baseline_mean": {}}
    ts = tg.season.astype(str) + "_" + tg.posteam
    cl = pd.factorize(tg.game_id)[0]
    wet = tg.tier.isin(["light", "rain", "heavy"]).astype(float)
    designs = {"effects": pd.DataFrame({"light": (tg.tier == "light").astype(float), "rain": (tg.tier == "rain").astype(float), "heavy": (tg.tier == "heavy").astype(float), "wind10": tg.wind10}),
               "pooled": pd.DataFrame({"any_rain": wet, "wind10": tg.wind10})}   # pooled = the model to use: one rain effect, wind as the severity dial
    res["pooled"] = {}
    for name, X in designs.items():
      Xd = X - X.groupby(ts).transform("mean")                            # team-season fixed effects by demeaning
      for m in METRICS:
          y = pd.to_numeric(tg[m], errors="coerce")
          ok = y.notna().values
          yd = (y - y.groupby(ts).transform("mean"))[ok].values
          A = Xd[ok].values
          beta, *_ = np.linalg.lstsq(A, yd, rcond=None)
          r = yd - A @ beta
          bread = np.linalg.pinv(A.T @ A)
          S = pd.DataFrame(A * r[:, None]).groupby(cl[ok]).sum().values     # clustered by game (both teams share the weather)
          se = np.sqrt(np.diag(bread @ (S.T @ S) @ bread))
          base = float(y[(tg.tier.isin(["dry", "indoor"])).values & ok].mean())
          res["baseline_mean"][m] = base
          res[name][m] = {k: {"change": float(b), "se": float(s), "pct_of_baseline": float(b / base) if base else None,
                                   "clear": bool(abs(b) > 1.96 * s)} for k, b, s in zip(X.columns, beta, se)}
    return res


def main(argv):
    files = []
    for a in argv:
        pth = Path(a)
        files += sorted(pth.glob("*.parquet")) if pth.is_dir() else [pth]
    if not files:
        raise SystemExit(__doc__)
    import pyarrow.parquet as pq
    parts = []
    for f in files:
        names = set(pq.read_schema(f).names)
        if not {"weather", "play_type", "game_id"} <= names:
            continue
        parts.append(pd.read_parquet(f, columns=[c for c in COLS if c in names]))
    pbp = pd.concat(parts, ignore_index=True)
    players = pd.read_parquet(ROOT / "fixtures" / "players.parquet")
    pos = players.drop_duplicates("gsis_id").set_index("gsis_id").position
    res = fit(team_games(pbp, pos))
    res.update(seasons=sorted(int(s) for s in pbp.season.unique()), method="team-season fixed effects; rain tiers and wind (per 10 mph above 10) fitted together; standard errors clustered by game",
               tier_definitions={"light": "weather text says light rain, drizzle, showers or mist", "rain": "weather text says rain with no qualifier (treat as moderate)",
                                 "heavy": "text says heavy / steady / pouring / storm, OR plain rain with wind of 15+ mph (proxy: the text rarely grades intensity)"},
               caveat="Observational. Weather text is written by team staff and describes kickoff, not the whole game. 'clear' means the change is larger than about two standard errors.")
    (ROOT / "research" / "weather" / "rain_effects.json").write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({"seasons": res["seasons"], "team_games_by_tier": res["team_games_by_tier"]}))
    for m in METRICS:
        e = res["effects"][m]
        q = res["pooled"][m]
        print(f"{m:22s} base {res['baseline_mean'][m]:7.3f} | " + " | ".join(f"{k} {e[k]['change']:+.3f}±{e[k]['se']:.3f}{'*' if e[k]['clear'] else ' '}" for k in ("light", "rain", "heavy"))
              + " || POOLED " + " | ".join(f"{k} {q[k]['change']:+.3f}±{q[k]['se']:.3f}{'*' if q[k]['clear'] else ' '} ({100 * q[k]['pct_of_baseline']:+.1f}%)" for k in ("any_rain", "wind10")))


if __name__ == "__main__":
    main(sys.argv[1:])
