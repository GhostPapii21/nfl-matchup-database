"""Opportunity check: does this game give the player the chance to hit a number?

A defense that allows 75 yards a game to tight ends spreads those yards over every tight end it faced. What one player can
do depends on how many chances this game gives him (team plays, pass/run mix, the script implied by the spread, weather,
teammates out, his share) and on what he does with each chance (catch rate and yards per catch, or yards per carry,
against this defense). This module turns those into a distribution of outcomes by simulation:

    targets   = gamma-Poisson around team pass attempts x his target share (spread from his own game-to-game swings)
    catches   = binomial(targets, catch rate adjusted for this defense)
    yards     = sum of per-catch yards drawn from the league's real per-catch outcomes for his position, scaled to his
                yards per catch adjusted for this defense
    rushing   = gamma-Poisson carries, per-carry yards drawn from the league's real per-carry outcomes, shifted to his
                yards per carry adjusted for this defense

Output: expected volume, the chance of reaching each yardage and catch level, and how many targets he needs to get there.
Research only. Calibration is measured by dashboard/backtest_opportunity.py; see dashboard/OPPORTUNITY.md.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

REC_THRESHOLDS = (20, 30, 40, 50, 60, 70, 80, 90, 100, 120)
CATCH_THRESHOLDS = (2, 3, 4, 5, 6, 7, 8)
RUSH_THRESHOLDS = (30, 40, 50, 60, 70, 80, 100, 120)
CARRY_THRESHOLDS = (8, 10, 12, 15, 18, 20)
N_SIMS = 20000

# Shrinkage: how many league-average targets / catches / carries are blended into a player's own rate.
PRIOR_TARGETS = 40
PRIOR_CATCHES = 25
PRIOR_CARRIES = 60
DEF_WEIGHT = 0.5      # how much of the defense's deviation from league average is applied (half, as in the packet baselines)
# Volume correction fitted on 2024-2025 (dashboard/backtest_opportunity.py): raw share x team volume overstates what
# players get (in-game injuries, rotation, lost work), most at the top. Checked on 2026 games the fit never saw.
VOLUME_CAL = {"rec": (0.048, 0.877), "rush": (0.589, 0.799)}
# Game-to-game uncertainty in the player's share itself (role changes), as a coefficient of variation.
SHARE_CV = {"rec": 0.25, "rush": 0.25}


def _f(x, nd=3):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return None if (math.isnan(x) or math.isinf(x)) else round(x, nd)


# ----------------------------------------------------------------------------------------------- league pools
def league_pools(pbp: pd.DataFrame, rosters: pd.DataFrame | None) -> dict:
    """Per-catch receiving yards by position and per-carry rushing yards for running backs, from real plays."""
    pos = {}
    if rosters is not None and len(rosters):
        r = rosters.dropna(subset=["gsis_id"]).sort_values("week")
        pos = dict(zip(r.gsis_id, r.position))
    c = pbp[(pbp.complete_pass == 1) & pbp.receiving_yards.notna() & (pbp.two_point_attempt != 1)]
    t = pbp[(pbp.pass_attempt == 1) & (pbp.sack != 1) & pbp.receiver_player_id.notna() & (pbp.two_point_attempt != 1)]
    out = {"catch": {}, "catch_rate": {}, "ypr": {}}
    for p in ("WR", "TE", "RB"):
        ids = [k for k, v in pos.items() if v == p]
        cy = c[c.receiver_player_id.isin(ids)].receiving_yards.to_numpy(dtype=float)
        tt = t[t.receiver_player_id.isin(ids)]
        if len(cy) < 200:     # no roster positions: fall back to every catch
            cy = c.receiving_yards.to_numpy(dtype=float)
            tt = t
        out["catch"][p] = cy
        out["catch_rate"][p] = float(tt.complete_pass.mean())
        out["ypr"][p] = float(cy.mean())
    ru = pbp[(pbp.rush_attempt == 1) & (pbp.qb_scramble != 1) & pbp.rushing_yards.notna() & (pbp.two_point_attempt != 1)]
    rb_ids = [k for k, v in pos.items() if v == "RB"]
    rr = ru[ru.rusher_player_id.isin(rb_ids)].rushing_yards.to_numpy(dtype=float) if rb_ids else ru.rushing_yards.to_numpy(dtype=float)
    if len(rr) < 500:
        rr = ru.rushing_yards.to_numpy(dtype=float)
    out["carry"] = rr
    out["ypc"] = float(rr.mean())
    return out


# ----------------------------------------------------------------------------------------------- simulation core
def _dispersion(log_counts, mean) -> float:
    """Gamma shape k for a gamma-Poisson count with this player's game-to-game variance. Larger k = steadier."""
    x = [v for v in log_counts if v is not None]
    if len(x) < 3 or mean <= 0:
        return 8.0
    m = sum(x) / len(x)
    var = sum((v - m) ** 2 for v in x) / (len(x) - 1)
    if var <= m:
        return 50.0
    k = m * m / (var - m)
    return float(min(50.0, max(3.0, k)))


def _counts(rng, mean, k, n):
    lam = rng.gamma(shape=k, scale=mean / k, size=n) if mean > 0 else np.zeros(n)
    return rng.poisson(lam)


def _sum_draws(rng, counts, pool, scale=1.0, shift=0.0):
    """Sum `counts[i]` draws from `pool` for each simulation i (vectorised)."""
    total = int(counts.sum())
    out = np.zeros(len(counts))
    if total == 0:
        return out
    draws = rng.choice(pool, size=total, replace=True) * scale + shift
    idx = np.repeat(np.arange(len(counts)), counts)
    np.add.at(out, idx, draws)
    return out


def chances(values, thresholds):
    return {str(t): _f((values >= t).mean(), 3) for t in thresholds}


def _volume(rng, raw_mean, kind, k, n):
    a, b = VOLUME_CAL[kind]
    mean = max(0.0, a + b * raw_mean)
    cv = SHARE_CV[kind]
    mult = rng.gamma(shape=1 / cv ** 2, scale=cv ** 2, size=n) if cv > 0 else np.ones(n)
    lam = (rng.gamma(shape=k, scale=mean / k, size=n) if mean > 0 else np.zeros(n)) * mult
    return rng.poisson(lam)


def simulate_receiver(*, exp_targets, k, catch_rate, ypr, pool, rain_yards=1.0, rain_catch=1.0, n=N_SIMS, seed=0):
    """exp_targets is the raw share x team attempts; the fitted volume correction is applied here."""
    rng = np.random.default_rng(seed)
    tg = _volume(rng, exp_targets, "rec", k, n)
    cr = min(0.95, max(0.2, catch_rate * rain_catch))
    rec = rng.binomial(tg, cr)
    scale = (ypr / pool.mean()) * rain_yards if pool.mean() > 0 else 1.0
    yds = _sum_draws(rng, rec, pool, scale=scale)
    return tg, rec, yds


def simulate_rusher(*, exp_carries, k, ypc, pool, n=N_SIMS, seed=0):
    rng = np.random.default_rng(seed)
    car = _volume(rng, exp_carries, "rush", k, n)
    yds = _sum_draws(rng, car, pool, shift=ypc - pool.mean())
    return car, yds


def summary_receiver(tg, rec, yds, ypt):
    need = {str(t): (math.ceil(t / ypt) if ypt and ypt > 0 else None) for t in (50, 60, 70, 80, 100)}
    return {"targets_mean": _f(tg.mean(), 1), "receptions_mean": _f(rec.mean(), 1), "yards_mean": _f(yds.mean(), 1),
            "yards_median": _f(np.median(yds), 1), "yards_p25_p75": [_f(np.percentile(yds, 25), 0), _f(np.percentile(yds, 75), 0)],
            "yards": chances(yds, REC_THRESHOLDS), "receptions": chances(rec, CATCH_THRESHOLDS),
            "targets_needed": need,
            "targets_needed_chance": {t: (_f((tg >= v).mean(), 3) if v is not None else None) for t, v in need.items()}}


def summary_rusher(car, yds):
    return {"carries_mean": _f(car.mean(), 1), "yards_mean": _f(yds.mean(), 1), "yards_median": _f(np.median(yds), 1),
            "yards_p25_p75": [_f(np.percentile(yds, 25), 0), _f(np.percentile(yds, 75), 0)],
            "yards": chances(yds, RUSH_THRESHOLDS), "carries": chances(car, CARRY_THRESHOLDS)}


# ----------------------------------------------------------------------------------------------- inputs shared with the backtest
def shrink(own_num, own_den, league_rate, prior):
    return (own_num + league_rate * prior) / (own_den + prior)


def def_factor(def_rate, league_rate):
    if not def_rate or not league_rate:
        return 1.0
    return max(0.8, min(1.2, 1 + DEF_WEIGHT * (def_rate / league_rate - 1)))


def script_multipliers(implied_margin):
    """Team favoured by m points passes a little less and runs a little more (capped at +/-10%)."""
    if implied_margin is None:
        return 1.0, 1.0
    m = max(-10.0, min(10.0, implied_margin))
    return 1 - 0.01 * m, 1 + 0.012 * m


# ----------------------------------------------------------------------------------------------- board integration
def _pos_key(pos):
    p = (pos or "").upper()
    return "te" if p == "TE" else "rb" if p == "RB" else "wr"


def board_side(side: dict, game: dict, implied: dict | None, pools: dict, injuries_out: set[str], seed: int = 0) -> dict:
    """Opportunity for every pass catcher and back in one direction of the matchup."""
    off, dfn = side["offense"], side["defense"]
    op, da = side["offense_produced"], side["defense_allowed"]
    plays = None
    if op.get("plays_pg") and da.get("plays_pg"):
        plays = (op["plays_pg"] + da["plays_pg"]) / 2
    pass_ratio = (op.get("pass_att_pg") or 0) / op["plays_pg"] if op.get("plays_pg") else 0.55
    margin = None
    if implied:
        margin = implied.get(off, 0) - implied.get(dfn, 0)
    pmul, rmul = script_multipliers(margin)
    rain = side.get("rain") or {}
    tp = rain.get("team_passing") or {}
    att_rain = (tp.get("forecast", {}).get("attempts") or 0) / (tp.get("dry", {}).get("attempts") or 1) if tp.get("dry") else 1.0
    team_att = plays * pass_ratio * pmul * (att_rain or 1.0) if plays else op.get("pass_att_pg")
    team_rush = plays * (1 - pass_ratio) * rmul if plays else op.get("rush_att_pg")
    team_targets = sum((g.get("wr_targets") or 0) + (g.get("te_targets") or 0) + (g.get("rb_targets") or 0) for g in side.get("offense_by_game", []))
    weeks_targets = {g["week"]: (g.get("wr_targets") or 0) + (g.get("te_targets") or 0) + (g.get("rb_targets") or 0) for g in side.get("offense_by_game", [])}
    weeks_carries = {g["week"]: (g.get("carries") or 0) for g in side.get("offense_by_game", [])}
    roles = side.get("roles", {})
    rec = [r for r in roles.get("receivers", []) if (r.get("targets") or 0) >= 8]
    rush = [r for r in roles.get("rushers", []) if (r.get("carries") or 0) >= 8 and r.get("pos") == "RB"]
    out_names = {n.lower() for n in injuries_out}
    missing_share = sum(r.get("target_share") or 0 for r in rec if (r.get("full_name") or "").lower() in out_names)
    missing_carry = sum(r.get("carry_share") or 0 for r in rush if (r.get("full_name") or "").lower() in out_names)
    healthy_share = sum(r.get("target_share") or 0 for r in rec if (r.get("full_name") or "").lower() not in out_names) or 1
    healthy_carry = sum(r.get("carry_share") or 0 for r in rush if (r.get("full_name") or "").lower() not in out_names) or 1
    res = {"team": off, "vs": dfn, "team_pass_attempts": _f(team_att, 1), "team_rush_attempts": _f(team_rush, 1),
           "plays": _f(plays, 1), "pass_ratio": _f(pass_ratio, 3), "script_pass_multiplier": _f(pmul, 3), "weather_attempts_multiplier": _f(att_rain, 3),
           "implied_margin": _f(margin, 1), "missing_target_share": _f(missing_share, 3), "missing_carry_share": _f(missing_carry, 3),
           "receivers": [], "rushers": []}
    for i, r in enumerate(rec):
        name = r.get("full_name") or r["player"]
        if name.lower() in out_names:
            res["receivers"].append({"player": name, "pos": r.get("pos"), "status": "OUT: no projection"})
            continue
        pk = _pos_key(r.get("pos"))
        P = pk.upper()
        log = r.get("log", [])
        # Share over the games he played (as in the backtest), not diluted by games he missed.
        played_team = sum(weeks_targets.get(x["week"], 0) for x in log)
        share = (sum(x.get("targets", 0) for x in log) / played_team) if played_team else (r.get("target_share") or 0)
        l3 = log[-3:]
        l3_team = sum(weeks_targets.get(x["week"], 0) for x in l3)
        share_l3 = (sum(x.get("targets", 0) for x in l3) / l3_team) if l3_team else None
        share_used = 0.6 * share + 0.4 * share_l3 if share_l3 is not None and len(log) >= 5 else share
        bump = missing_share * (share_used / healthy_share) * 0.8 if missing_share else 0.0
        share_used += bump
        exp_t = (team_att or 0) * share_used
        lg_cr, lg_ypr = pools["catch_rate"].get(P, 0.65), pools["ypr"].get(P, 11.0)
        cr = shrink(r.get("receptions", 0), r.get("targets", 0), lg_cr, PRIOR_TARGETS)
        ypr = shrink(r.get("yards", 0), r.get("receptions", 0), lg_ypr, PRIOR_CATCHES)
        d_tg, d_rec, d_yds = da.get(f"{pk}_targets_pg"), da.get(f"{pk}_receptions_pg"), da.get(f"{pk}_rec_yards_pg")
        d_cr = (d_rec / d_tg) if d_tg else None
        d_ypr = (d_yds / d_rec) if d_rec else None
        cr_adj = cr * def_factor(d_cr, lg_cr)
        ypr_adj = ypr * def_factor(d_ypr, lg_ypr)
        rn = next((x for x in (rain.get("receivers") or []) if x.get("player") == r["player"]), None)
        ry = rc = 1.0
        if rn and rn.get("dry", {}).get("yards"):
            ry = (rn["forecast"]["yards"] / rn["dry"]["yards"]) / max(rn["forecast"]["catch_rate"] / rn["dry"]["catch_rate"], 1e-6)
            rc = rn["forecast"]["catch_rate"] / rn["dry"]["catch_rate"]
        k = _dispersion([x.get("targets") for x in log], exp_t)
        tg, rc_, yd = simulate_receiver(exp_targets=exp_t, k=k, catch_rate=cr_adj, ypr=ypr_adj, pool=pools["catch"][P],
                                        rain_yards=ry, rain_catch=rc, seed=seed + 101 * (i + 1))
        hist = [x.get("yards", 0) for x in log]
        pos_targets = sum(x.get(f"{pk}_targets", 0) for x in side.get("offense_by_game", [])) or 1
        slice_ = (d_yds or 0) * (r.get("targets", 0) / pos_targets)
        res["receivers"].append({
            "player": name, "pos": r.get("pos"),
            "inputs": {"target_share_window": _f(share, 3), "target_share_last3": _f(share_l3, 3), "target_share_used": _f(share_used, 3),
                       "injury_bump": _f(bump, 3), "catch_rate": _f(cr_adj, 3), "yards_per_catch": _f(ypr_adj, 1),
                       "yards_per_target": _f(cr_adj * ypr_adj * ry, 2), "dispersion_k": _f(k, 1),
                       "def_catch_rate_allowed": _f(d_cr, 3), "def_yards_per_catch_allowed": _f(d_ypr, 1),
                       "league_catch_rate": _f(lg_cr, 3), "league_yards_per_catch": _f(lg_ypr, 1),
                       "position_share": _f(r.get("targets", 0) / pos_targets, 3),
                       "def_allows_position_yards_pg": _f(d_yds, 1), "his_slice_of_that": _f(slice_, 1)},
            "history": {"games": len(hist), **{str(t): sum(1 for h in hist if h >= t) for t in (50, 70, 80, 100)}},
            "player_id": r.get("player_id"),
            "sim": {"targets_raw": _f(exp_t, 3), "k": _f(k, 2), "catch_rate": _f(cr_adj, 4), "ypr": _f(ypr_adj, 3),
                    "rain_yards": _f(ry, 4), "rain_catch": _f(rc, 4), "pool": P},
            **summary_receiver(tg, rc_, yd, cr_adj * ypr_adj * ry)})
    for i, r in enumerate(rush):
        name = r.get("full_name") or r["player"]
        if name.lower() in out_names:
            res["rushers"].append({"player": name, "pos": r.get("pos"), "status": "OUT: no projection"})
            continue
        log = r.get("log", [])
        played_team = sum(weeks_carries.get(x["week"], 0) for x in log)
        share = (sum(x.get("carries", 0) for x in log) / played_team) if played_team else (r.get("carry_share") or 0)
        l3 = log[-3:]
        l3_team = sum(weeks_carries.get(x["week"], 0) for x in l3)
        share_l3 = (sum(x.get("carries", 0) for x in l3) / l3_team) if l3_team else None
        share_used = 0.6 * share + 0.4 * share_l3 if share_l3 is not None and len(log) >= 5 else share
        bump = missing_carry * (share_used / healthy_carry) * 0.8 if missing_carry else 0.0
        share_used += bump
        exp_c = (team_rush or 0) * share_used
        ypc = shrink(r.get("yards", 0), r.get("carries", 0), pools["ypc"], PRIOR_CARRIES)
        d_ypc = da.get("rb_yards_per_carry")
        ypc_adj = ypc * def_factor(d_ypc, pools["ypc"])
        k = _dispersion([x.get("carries") for x in log], exp_c)
        car, yd = simulate_rusher(exp_carries=exp_c, k=k, ypc=ypc_adj, pool=pools["carry"], seed=seed + 977 * (i + 1))
        hist = [x.get("yards", 0) for x in log]
        res["rushers"].append({
            "player": name, "pos": r.get("pos"),
            "inputs": {"carry_share_window": _f(share, 3), "carry_share_last3": _f(share_l3, 3), "carry_share_used": _f(share_used, 3),
                       "injury_bump": _f(bump, 3), "yards_per_carry": _f(ypc_adj, 2), "def_yards_per_carry_allowed": _f(d_ypc, 2),
                       "league_yards_per_carry": _f(pools["ypc"], 2), "dispersion_k": _f(k, 1)},
            "history": {"games": len(hist), **{str(t): sum(1 for h in hist if h >= t) for t in (50, 70, 80, 100)}},
            "player_id": r.get("player_id"),
            "sim": {"carries_raw": _f(exp_c, 3), "k": _f(k, 2), "ypc": _f(ypc_adj, 3)},
            **summary_rusher(car, yd)})
    return res
