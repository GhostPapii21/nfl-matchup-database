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
import re
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


def _norm(n: str) -> str:
    return re.sub(r"[^a-z]", "", re.sub(r"\b(jr|sr|ii|iii|iv)\b\.?", "", (n or "").lower()))


def book_price(lines: list | None, player: str, market: str, rung: float = 79.5) -> dict | None:
    """The book's price for `player` over `rung` in an alternate-yards market (pregame/direct_lines rows), or None."""
    want = _norm(player)
    for r in lines or []:
        if r.get("market") == market and r.get("line") == rung and str(r.get("side", "")).lower() == "over" and _norm(r.get("player")) == want:
            if r.get("break_even"):
                return {"book": r["book"], "american": r["american"], "break_even": r["break_even"]}
    return None


def shadow_role(model: dict, p80: float, log: list, team_t: dict, cuts: dict) -> dict | None:
    """Side-by-side only, never moves a star (owner, 2026-11-23). Rising role: his target share in his last game against
    his season share, added on the logit scale. Passed the held-out test (2025-26 log loss 0.2691 -> 0.2684, z 2.1;
    research/shadow_2026-11-23); graded weekly against the live stars before it can replace anything."""
    w = (model.get("shadow") or {}).get("role_last1")
    if not w or len(log) < 2:
        return None
    tot = sum(team_t.get(x["week"], 0) for x in log)
    last = log[-1]
    lt = team_t.get(last["week"], 0)
    if not tot or not lt:
        return None
    share, share1 = sum(x.get("targets", 0) for x in log) / tot, last.get("targets", 0) / lt
    if share <= 0:
        return None
    x = math.log(min(max(share1 / share, 0.2), 4.0))
    lg = math.log(min(max(p80, 1e-4), 1 - 1e-4) / (1 - min(max(p80, 1e-4), 1 - 1e-4)))
    p = _sig(lg + w["const"] + w["last1"] * x)
    return {"p80": round(p, 3), "stars": stars(p, cuts), "season_share": round(share, 3), "last_game_share": round(share1, 3), "candidate": "rising role"}


GATE_KEY = {"WR": "wr_rec_yards_pg", "TE": "te_rec_yards_pg", "RB": "rb_rush_yards_pg"}


def defensive_gate(sd: dict, pos: str) -> dict | None:
    """What this defense allows to his position, ranked (32 = allows the most). Shown beside each star; it does not
    move the star: the star weights already carry the defense (80-yard games allowed to the position for receivers, RB
    yards a game for backs), and on 2022-26 an extra gate term did not clear the bar -- starred receivers vs the softest
    third hit 42% against 41% predicted, starred backs vs the softest third 36% against 44%
    (research/defense_gate_2026-11-23)."""
    k = GATE_KEY.get(pos)
    r = ((sd.get("defense_rank") or {}).get(k) or {}) if k else {}
    if not r.get("rank"):
        return None
    allowed = (sd.get("defense_allowed") or {}).get(k)
    label = "soft" if r["rank"] >= 23 else "tough" if r["rank"] <= 10 else "middle"
    return {"label": label, "rank": r["rank"], "of": r.get("of", 32), "allowed_pg": round(allowed, 1) if allowed else None,
            "league_avg": round(r["league_avg"], 1) if r.get("league_avg") else None}


def pressure_note(sd: dict) -> str | None:
    """Context only: the defense blitzes or pressures a lot and this QB is much worse (or better) against it. Pressure and
    blitz matchups did not predict 80-yard games on 2022-25 (research/defense_gate_2026-11-23)."""
    cp, qb = sd.get("coverage_profile") or {}, ((sd.get("qb") or {}).get("this_season") or {})
    vb, nb = qb.get("vs_blitz") or {}, qb.get("no_blitz") or {}
    rate = cp.get("five_plus_rushers_rate")
    if not rate or not vb.get("yards_per_attempt") or not nb.get("yards_per_attempt") or (vb.get("dropbacks") or 0) < 40 or rate < 0.33:
        return None
    d = vb["yards_per_attempt"] - nb["yards_per_attempt"]
    if abs(d) < 1.0:
        return None
    return (f"defense sends 5+ rushers {rate:.0%} of dropbacks; {(sd.get('qb') or {}).get('player')} averages "
            f"{vb['yards_per_attempt']:.1f} yards an attempt vs the blitz, {nb['yards_per_attempt']:.1f} without")


def health_flags(sd: dict, player: str) -> dict | None:
    """His own status going in: Questionable/Doubtful on the report, a concussion listing, or back from missed games.
    Tags only. On 2025-26 (research/injury_context_2026-11-23): starred players listed Questionable hit 30% against 39%
    predicted (27 players; a lean, not proven), and about a quarter of Questionable players do not play at all, so wait for
    the inactives (T-90). Players back from 1-2 or 3+ missed games, or from a concussion listing, hit about as often as the
    model said (99 / 28 / 46 receiver games) -- no evidence for an automatic downgrade."""
    want = _norm(player)
    inj = next((x for x in sd.get("offense_injuries") or [] if _norm(x.get("player")) == want), None)
    ret = next((x for x in sd.get("returning") or [] if _norm(x.get("player")) == want and x.get("unit") == "offense"), None)
    out, notes = {}, []
    if inj and str(inj.get("game_status") or "") in ("Questionable", "Doubtful"):
        out["status"] = inj["game_status"]
        notes.append(f"listed {inj['game_status']} ({inj.get('injury') or 'injury'}): wait for the inactives before betting"
                     + ("; Doubtful players usually sit" if inj["game_status"] == "Doubtful" else ""))
    if inj and "concuss" in str(inj.get("injury") or "").lower():
        out["concussion"] = True
        notes.append("on the report with a concussion")
    if ret and (ret.get("games_since_return") or 0) <= 2:
        out["returning"] = {k: ret.get(k) for k in ("games_missed", "games_since_return", "snap_pct_before", "snap_pct_last_game", "status")}
        notes.append(f"back after missing {ret.get('games_missed')} game(s); {ret.get('status', '').lower()} "
                     f"({(ret.get('snap_pct_last_game') or 0):.0%} of snaps last game vs {(ret.get('snap_pct_before') or 0):.0%} before)")
    if not out:
        return None
    out["notes"] = notes
    return out


ROLE_GAP80 = 0.15     # model 15+ points off the book's 80+ price: Week 11's Smith (backup QB), Monangai and Allen (split backs)


def _attach_price(e: dict, lines: list | None, market: str, cuts: dict | None = None) -> None:
    """Adds the book's 80+ price. With a price, the stars come from the blend of model and price (Nov 23, 2026): the blend
    was the most accurate of the three on the held-out weeks 8-9 ladders (Brier 0.1118 vs 0.1136), and on Week 11 the
    blend's stars hit 14 of 26 against the model's 12 of 27 (research/star_review_2026-11-23)."""
    b = book_price(lines, e["player"], market)
    if not b:
        return
    blend = blend_with_book(e["p80"], b["break_even"])
    gap = e["p80"] - b["break_even"]
    e["book80"] = {**b, "blend": round(blend, 3), "model_minus_price": round(gap, 3)}
    if cuts:
        e["stars_model"], e["stars"], e["star_basis"] = e["stars"], stars(blend, cuts), "model + FanDuel price"
        if e["stars"] != e["stars_model"]:
            e.setdefault("why", []).append(f"the FanDuel price moves this from {e['stars_model']} to {e['stars']} stars")
    if abs(gap) >= ROLE_GAP80:
        e.setdefault("why", []).append(f"model {e['p80']:.0%} vs FanDuel {b['break_even']:.0%}: a big disagreement, check the QB and his role")


def watch_side(sd: dict, imp: dict | None, dctx: dict, model: dict | None, lines: list | None = None) -> dict | None:
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
        # Weather: the same measured rain/wind factors the yardage simulation uses (pregame/rain_model.py). Rain alone cuts
        # receiver yards about 15%; checked again on 13,526 receiver-games 2022-2026 (research/context_effects_2026-11-22).
        wam = float(opp.get("weather_attempts_multiplier") or 1.0)
        sim = o.get("sim", {})
        wx = (wam * float(inp.get("rain_yards") or sim.get("rain_yards") or 1.0) * float(inp.get("rain_catch") or sim.get("rain_catch") or 1.0)
              * float(inp.get("backup_qb_yards") or 1.0))       # backup QB: research/qb_script_2026-11-22
        blend *= wam
        x = {"l_tgt": math.log(max(blend, 0.5)), "l_yds": math.log(max(yds_pg * wx, 1.0)), "implied": imp_off or 22.0, "team_pass": team_pass,
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
        if wx < 0.97:
            why.append(f"rain/wind in the forecast cuts his yards about {round((1 - wx) * 100)}%")
        out["receivers"].append({"player": r.get("full_name") or r["player"], "player_id": r["player_id"], "pos": r["pos"], "tier": tier,
                                 "style": "explosive" if ex_pg >= 1.2 else "volume", "p80": round(p80, 3), "p100": round(p100, 3),
                                 "stars": stars(p80, cuts), "targets": round(blend, 1), "yds_pg": round(yds_pg, 1), "ex_pg": round(ex_pg, 2), "why": why,
                                 **({"shadow": sh} if (sh := shadow_role(model, p80, log, team_t, cuts)) else {})})
    rb_cpg = {}
    for r in (sd.get("roles") or {}).get("rushers") or []:
        o = by_player.get(r.get("player_id"))
        if o and not o.get("status") and r.get("pos") == "RB" and r.get("log"):
            rb_cpg[r.get("player_id")] = float(np.mean([x.get("carries", 0) for x in r["log"]]))
    for r in (sd.get("roles") or {}).get("rushers", []):
        o = by_player.get(r.get("player_id"))
        log = r.get("log", [])
        if not o or o.get("status") or len(log) < 3 or r.get("pos") != "RB":
            continue
        # split backfield: the busiest other active back who comes in averaging 10+ carries (0 if none).
        # Fit 2022-26 with the other weights (research/star_review_2026-11-23): -0.04 log-odds per carry he averages.
        mate_car = max([c for pid, c in rb_cpg.items() if pid != r.get("player_id") and c >= 10] or [0.0])
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
        if "mate_car" in rus_m:
            x["mate_car"] = mate_car
        p80 = _sig(rus_m["const"] + sum(rus_m[k] * v for k, v in x.items()))
        p100 = _sig(rus_100["const"] + sum(rus_100[k] * v for k, v in x.items()))
        why = [f"{cpg:.1f} carries a game"]
        if margin >= 3:
            why.append(f"favored by about {margin:.0f}")
        if (sd.get("defense_rank", {}).get("rb_rush_yards_pg") or {}).get("rank") and sd["defense_rank"]["rb_rush_yards_pg"]["rank"] >= 22:
            why.append(f"{dfn} allows {rb_allowed:.0f} rushing yards a game to backs")
        if inp.get("injury_bump"):
            why.append("a teammate's absence adds carries")
        if mate_car:
            why.append(f"splits the backfield (another back averages {mate_car:.0f} carries)")
        out["rushers"].append({"player": r.get("full_name") or r["player"], "player_id": r["player_id"], "pos": "RB", "p80": round(p80, 3), "p100": round(p100, 3),
                               "stars": stars(p80, cuts), "carries": round(cpg, 1), "yds_pg": r.get("yards_pg"), "why": why})
    pn = pressure_note(sd)
    for e in out["receivers"] + out["rushers"]:
        hf = health_flags(sd, e["player"])
        if hf:
            e["health"] = hf
            e.setdefault("why", []).extend(hf["notes"])
    for e in out["receivers"]:
        _attach_price(e, lines, "alt_receiving_yards", cuts)
        e["gate"] = defensive_gate(sd, e.get("pos"))
        if pn:
            e["pressure_note"] = pn
    for e in out["rushers"]:
        _attach_price(e, lines, "alt_rushing_yards", cuts)
        e["gate"] = defensive_gate(sd, "RB")
    for k in ("receivers", "rushers"):
        out[k].sort(key=lambda e: -e["p80"])
    return out
