"""Rain and wind adjustment for passing volume, receptions and receiving yards.

Coefficients are measured, not chosen: research/weather/fit_rain_effects.py compares every team-game played in rain
(2018 onward) with the same team's dry games that season, fitting rain and wind together. Only effects that are
clearly different from zero are used; the rest are left at no change.

    R = 1 when it rains (or the forecast chance of rain, 0..1, for an expected value)
    W = max(0, wind mph - 10) / 10

    attempts'        = attempts        x (1 + a_rain R + a_wind W)
    targets_i'       = attempts' x target share_i x (1 + s_pos,wind W)
    catch rate_i'    = catch rate_i    x (1 + c_pos,rain R + c_pos,wind W)
    yards/target_i'  = yards/target_i  x (1 + y_pos,rain R + y_pos,wind W)
    receptions_i'    = targets_i' x catch rate_i'
    yards_i'         = targets_i' x yards/target_i'

The data cannot grade rain as light, moderate or heavy: game records almost always just say "Rain", and the few
labelled "light" do not come out milder. So rain is one measured step, and wind is the severity dial. Research only.
"""
from __future__ import annotations

import json
from pathlib import Path

EFFECTS = Path(__file__).resolve().parents[1] / "research" / "weather" / "rain_effects.json"
_cache: dict | None = None


def coefficients() -> dict:
    """{metric: {"rain": pct, "wind": pct}} as fractions of the dry baseline; 0 where the effect is not clear."""
    global _cache
    if _cache is None:
        r = json.loads(EFFECTS.read_text())
        pick = lambda e: float(e["pct_of_baseline"]) if e["clear"] else 0.0
        _cache = {"_meta": {"seasons": r["seasons"], "rain_team_games": sum(r["team_games_by_tier"].get(k, 0) for k in ("light", "rain", "heavy")),
                            "team_games": r["team_games"]},
                  **{m: {"rain": pick(e["any_rain"]), "wind": pick(e["wind10"]), "rain_points": e["any_rain"]["change"], "wind_points": e["wind10"]["change"]}
                     for m, e in r["pooled"].items()}}
    return _cache


def factor(metric: str, rain: float, wind_mph: float) -> float:
    c = coefficients().get(metric) or {"rain": 0.0, "wind": 0.0}
    w = max(0.0, float(wind_mph or 0) - 10.0) / 10.0
    return max(0.2, 1.0 + c["rain"] * max(0.0, min(1.0, rain)) + c["wind"] * w)


def adjust_receiver(pos: str, targets: float, catch_rate: float, yards_per_target: float, rain: float, wind_mph: float) -> dict:
    """Per-game line for one receiver. pos is WR, TE or RB."""
    k = {"WR": "wr", "TE": "te", "RB": "rb"}.get(pos, "wr")
    t = targets * factor("attempts", rain, wind_mph) * factor(f"{k}_target_share", rain, wind_mph)
    cr = min(1.0, catch_rate * factor(f"{k}_catch_rate", rain, wind_mph))
    ypt = yards_per_target * factor(f"{k}_yards_per_target", rain, wind_mph)
    return {"targets": round(t, 1), "catch_rate": round(cr, 3), "receptions": round(t * cr, 1), "yards_per_target": round(ypt, 2), "yards": round(t * ypt, 1)}


def adjust_qb(attempts: float, completion_pct: float, yards: float, rain: float, wind_mph: float) -> dict:
    a = attempts * factor("attempts", rain, wind_mph)
    cp = completion_pct * factor("completion_pct", rain, wind_mph)
    return {"attempts": round(a, 1), "completion_pct": round(cp, 3), "completions": round(a * cp, 1), "yards": round(yards * factor("pass_yards", rain, wind_mph), 1)}
