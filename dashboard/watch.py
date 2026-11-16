"""80-yard watch: stars the players with a real chance at 80+ yards, from fitted weights.

Weights come from dashboard/watch_model.json (research/watch_model_2026-11-16/fit.py: 2022 to 2026, checked on
2025-26). Receivers use his targets, yards a game, team implied total, his team's pass volume, how often the defense
gives up 20+ yard completions, and how many 80+ yard games it has allowed to his position. Backs use carries, yards
per carry, spread, team total and the rushing yards the defense allows. Each factor's weight was fitted, so ones that
do not predict (the defense's big-play rate) count for almost nothing and are shown as context only.

Stars: 3 = 50%+ for 80 yards, 2 = 40%+, 1 = 30%+. Research only; not graded against prices.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent / "watch_model.json"


def load_model(path: Path | None = None) -> dict | None:
    try:
        return json.loads((path or MODEL_PATH).read_text())
    except (OSError, ValueError):
        return None


def _sig(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def blend_with_book(p_model: float, book_break_even: float, logit_scale: float = 1.0) -> float:
    """Even blend, on the logit scale, of the model and a book's break-even price (vig included). The graded weeks 8-9
    ladders gave a Brier of 0.1118 for this against 0.1136 for either alone: a small gain, within noise."""
    lg = lambda p: math.log(min(max(p, 1e-4), 1 - 1e-4) / (1 - min(max(p, 1e-4), 1 - 1e-4)))
    return _sig(0.5 * lg(p_model) + 0.5 * logit_scale * lg(book_break_even))


def stars(p: float, cuts: dict) -> int:
    return 3 if p >= cuts["3"] else 2 if p >= cuts["2"] else 1 if p >= cuts["1"] else 0


def defense_context(pbp: pd.DataFrame | None, rosters: pd.DataFrame | None, before_week: int, min_targets: int = 20) -> dict:
    """Per defense, from games before `before_week`: rate of 20+ yard pass plays relative to the league, and 80+ yard
    receiving games allowed per game to WRs and TEs (receivers with at least `min_targets` targets that season)."""
    if pbp is None or rosters is None or not len(pbp):
        return {}
    p = pbp[(pbp.season_type == "REG") & (pbp.two_point_attempt != 1) & (pbp.week < before_week)]
    pos = dict(zip(rosters.dropna(subset=["gsis_id"]).sort_values("week").gsis_id, rosters.dropna(subset=["gsis_id"]).sort_values("week").position))
    att = p[(p.pass_attempt == 1) & (p.sack != 1)]
    ex = att.assign(e=(att.yards_gained >= 20).astype(int)).groupby("defteam").e.agg(["sum", "size"])
    lg = ex["sum"].sum() / max(ex["size"].sum(), 1)
    t = att[att.receiver_player_id.notna()].copy()
    t["pos"] = t.receiver_player_id.map(pos)
    t["y"] = t.receiving_yards.fillna(0)
    tot = t.groupby("receiver_player_id").size()
    keep = set(tot[tot >= min_targets].index)
    g = t[t.receiver_player_id.isin(keep)].groupby(["defteam", "week", "receiver_player_id", "pos"]).y.sum().reset_index()
    games = p.groupby("defteam").week.nunique()
    out = {}
    for d, n in games.items():
        row = {"games": int(n), "ex_rate_rel": float(ex.loc[d, "sum"] / max(ex.loc[d, "size"], 1) / lg) if d in ex.index else 1.0}
        for ps in ("WR", "TE"):
            c = int(((g.defteam == d) & (g.pos == ps) & (g.y >= 80)).sum())
            row[f"g80_{ps}"], row[f"g80_{ps}_pg"] = c, c / n
        out[d] = row
    rank = sorted(out, key=lambda d: -(out[d]["g80_WR"] + out[d]["g80_TE"]) / out[d]["games"])
    for i, d in enumerate(rank, 1):
        out[d]["g80_rank"] = i
    exr = sorted(out, key=lambda d: -out[d]["ex_rate_rel"])
    for i, d in enumerate(exr, 1):
        out[d]["ex_rank"] = i
    return out


def _tier(tgt_pg: float, yds_pg: float) -> str | None:
    return "alpha" if tgt_pg >= 8 and yds_pg >= 70 else "tier B" if tgt_pg >= 7 and yds_pg >= 55 else None


def watch_side(sd: dict, imp: dict | None, dctx: dict, model: dict | None) -> dict | None:
    """One side of a matchup: starred players. `sd` is a board side with roles, opportunity and offense_by_game."""
    if not model or not imp:
        return None
    off, dfn = sd["offense"], sd["defense"]
    cuts = model["stars"]
    opp = sd.get("opportunity") or {}
    by_player = {r.get("player_id"): r for r in (opp.get("receivers") or []) + (opp.get("rushers") or []) if r.get("player_id")}
    team_t = {g["week"]: (g.get("wr_targets") or 0) + (g.get("te_targets") or 0) + (g.get("rb_targets") or 0) for g in sd.get("offense_by_game", [])}
    team_pass = float(np.mean(list(team_t.values()))) if team_t else 0.0
    d = dctx.get(dfn, {})
    imp_off = imp.get(off)
    margin = (imp_off or 0) - (imp.get(dfn) or 0)
    pass_rank = (sd.get("offense_rank", {}).get("pass_yards_pg") or {}).get("rank")
    last5 = [g.get("pass_yards") or 0 for g in sd.get("offense_by_game", [])][-5:]
    ctx = {"pass_yards_last5": round(float(np.mean(last5)), 0) if last5 else None, "pass_offense_rank": pass_rank, "implied": imp_off,
           "defense_g80_rank": d.get("g80_rank"), "defense_explosive_rank": d.get("ex_rank")}
    rec_m, rus_m = model["receiver"]["models"]["80"]["coef"], model["rusher"]["models"]["80"]["coef"]
    rec_100, rus_100 = model["receiver"]["models"]["100"]["coef"], model["rusher"]["models"]["100"]["coef"]
    out = {"receivers": [], "rushers": [], "context": ctx, "record": model.get("star_record"), "book_grade": model.get("book_grade")}
    for r in (sd.get("roles") or {}).get("receivers", []):
        o = by_player.get(r.get("player_id"))
        log = [x for x in r.get("log", [])]
        if not o or o.get("status") or len(log) < 3 or r.get("pos") not in ("WR", "TE") or not team_pass:
            continue
        tgt_pg = float(np.mean([x.get("targets", 0) for x in log]))
        yds_pg = float(np.mean([x.get("yards", 0) for x in log]))
        l3 = log[-3:]
        l3_team = sum(team_t.get(x["week"], 0) for x in l3)
        share_l3 = sum(x.get("targets", 0) for x in l3) / l3_team if l3_team else 0.0
        blend = 0.6 * tgt_pg + 0.4 * share_l3 * team_pass
        inp = o.get("inputs", {})
        base_share = 0.6 * (inp.get("target_share_window") or 0) + 0.4 * (inp.get("target_share_last3") or 0)
        if base_share and inp.get("target_share_used"):
            blend *= max(0.5, min(2.0, inp["target_share_used"] / base_share))      # teammate-out and the like
        x = {"l_tgt": math.log(max(blend, 0.5)), "l_yds": math.log(max(yds_pg, 1.0)), "implied": imp_off or 22.0, "team_pass": team_pass,
             "l_ex": math.log(min(2.0, max(0.5, d.get("ex_rate_rel", 1.0)))), "g80_pg": d.get(f"g80_{r['pos']}_pg", 0.0)}
        z80 = rec_m["const"] + sum(rec_m[k] * v for k, v in x.items())
        z100 = rec_100["const"] + sum(rec_100[k] * v for k, v in x.items())
        p80, p100 = _sig(z80), _sig(z100)
        tier = _tier(tgt_pg, yds_pg)
        ex_pg = (r.get("explosive") or 0) / max(r.get("games") or 1, 1)
        why = []
        if tier:
            why.append(f"{tier} receiver: {tgt_pg:.1f} targets and {yds_pg:.0f} yards a game")
        if blend >= 9.5:
            why.append(f"{blend:.1f} projected targets")
        if (imp_off or 0) >= 25.7:
            why.append(f"team expected to score {imp_off:.0f}")
        elif (imp_off or 99) < 21.8:
            why.append(f"team only expected to score {imp_off:.0f}")
        if (ctx["pass_yards_last5"] or 0) >= 280:
            why.append(f"offense averaging {ctx['pass_yards_last5']:.0f} passing yards over its last five")
        if d.get("g80_rank") and d["g80_rank"] <= 8:
            why.append(f"{dfn} has allowed {d['g80_WR'] + d['g80_TE']} receivers 80+ in {d['games']} games")
        elif d.get("g80_rank") and d["g80_rank"] >= 25:
            why.append(f"{dfn} rarely allows 80+ games")
        if inp.get("injury_bump"):
            why.append("a teammate's absence adds targets")
        out["receivers"].append({"player": r.get("full_name") or r["player"], "player_id": r["player_id"], "pos": r["pos"], "tier": tier,
                                 "style": "explosive" if ex_pg >= 1.2 else "volume", "p80": round(p80, 3), "p100": round(p100, 3),
                                 "stars": stars(p80, cuts), "targets": round(blend, 1), "yds_pg": round(yds_pg, 1), "ex_pg": round(ex_pg, 2), "why": why})
    for r in (sd.get("roles") or {}).get("rushers", []):
        o = by_player.get(r.get("player_id"))
        log = r.get("log", [])
        if not o or o.get("status") or len(log) < 3 or r.get("pos") != "RB":
            continue
        carries = [x.get("carries", 0) for x in log]
        cpg = 0.6 * float(np.mean(carries)) + 0.4 * float(np.mean(carries[-3:]))
        inp = o.get("inputs", {})
        base = 0.6 * (inp.get("carry_share_window") or 0) + 0.4 * (inp.get("carry_share_last3") or 0)
        if base and inp.get("carry_share_used"):
            cpg *= max(0.5, min(2.5, inp["carry_share_used"] / base))
        if cpg < 10:
            continue
        ypc = (sum(x.get("yards", 0) for x in log) + 4.3 * 40) / (sum(carries) + 40)
        rb_allowed = (sd.get("defense_allowed") or {}).get("rb_rush_yards_pg") or 92.5
        x = {"l_car": math.log(cpg), "l_ypc": math.log(ypc), "spread": margin, "implied": imp_off or 22.0, "l_d": math.log(max(rb_allowed, 20.0))}
        p80 = _sig(rus_m["const"] + sum(rus_m[k] * v for k, v in x.items()))
        p100 = _sig(rus_100["const"] + sum(rus_100[k] * v for k, v in x.items()))
        why = [f"{cpg:.1f} carries a game"]
        if margin >= 3:
            why.append(f"favored by about {margin:.0f}")
        if (sd.get("defense_rank", {}).get("rb_rush_yards_pg") or {}).get("rank") and sd["defense_rank"]["rb_rush_yards_pg"]["rank"] >= 22:
            why.append(f"{dfn} allows {rb_allowed:.0f} rushing yards a game to backs")
        if inp.get("injury_bump"):
            why.append("a teammate's absence adds carries")
        out["rushers"].append({"player": r.get("full_name") or r["player"], "player_id": r["player_id"], "pos": "RB", "p80": round(p80, 3), "p100": round(p100, 3),
                               "stars": stars(p80, cuts), "carries": round(cpg, 1), "yds_pg": r.get("yards_pg"), "why": why})
    for k in ("receivers", "rushers"):
        out[k].sort(key=lambda e: -e["p80"])
    return out
