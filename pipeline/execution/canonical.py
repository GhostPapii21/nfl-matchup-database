"""Call canonical equation modules. This file does not invent summary counts.

Only pregame.rain_model is invoked from a normal packet. Other canonical functions are named
and refused until their real inputs are present. Absent modules are not given stand-ins.
"""
from __future__ import annotations


def _blocked(ctx: dict, code: str, message: str) -> dict:
    return {
        "blocked": True,
        "code": code,
        "game_id": ctx["game_id"],
        "run_id": ctx["run_id"],
        "rows": [],
        "denominator": 0,
        "message": message,
        "research_only": True,
        "projection_ready": False,
    }


def run_rain_model(ctx: dict) -> dict:
    """Measured rain and wind factors from pregame.rain_model.factor. Research only."""
    weather = (ctx.get("packet") or {}).get("weather") or {}
    rain, wind = weather.get("rain"), weather.get("wind_mph")
    if rain is None or wind is None:
        return _blocked(
            ctx, "ANALYTIC_INPUT_ABSENT",
            "pregame.rain_model.factor requires rain and wind on the weather record. They are not fabricated.",
        )
    from pregame.rain_model import coefficients, factor

    meta = coefficients()["_meta"]
    metrics = {
        "attempts_factor": factor("attempts", float(rain), float(wind)),
        "completion_pct_factor": factor("completion_pct", float(rain), float(wind)),
        "pass_yards_factor": factor("pass_yards", float(rain), float(wind)),
    }
    provenance = (
        f"research/weather/rain_effects.json seasons {meta['seasons'][0]}-{meta['seasons'][-1]}; "
        f"{meta['rain_team_games']} team-games in rain of {meta['team_games']} team-games"
    )
    return {
        "game_id": ctx["game_id"],
        "run_id": ctx["run_id"],
        "equation_id": "pregame.rain_model.factor",
        "module_id": "pregame.rain_model",
        "metrics": metrics,
        "denominator": int(meta["team_games"]),
        "provenance": provenance,
        "rows": [{
            "equation_id": "pregame.rain_model.factor",
            "rain": float(rain),
            "wind_mph": float(wind),
            **metrics,
        }],
        "warnings": [],
        "research_only": True,
        "projection_ready": False,
    }


def run_player_baselines(ctx: dict) -> dict:
    """pregame.packet.player_baselines. Refuses when the packet has no receiver and rusher logs."""
    inputs = (ctx.get("packet") or {}).get("baseline_inputs")
    if not isinstance(inputs, dict) or "off_players" not in inputs:
        return _blocked(
            ctx, "ANALYTIC_INPUT_ABSENT",
            "pregame.packet.player_baselines is the phase 5 equation and was not given receiver and rusher logs. "
            "A points count is not that equation.",
        )
    from pregame.packet import player_baselines

    result = player_baselines(
        inputs["off_players"], inputs.get("opp_def_sum") or {}, inputs.get("league_def_avg") or {},
        inputs.get("listed_qb"),
    )
    players = [p for p in (result.get("players") or []) if isinstance(p, dict)]
    means = []
    for player in players:
        for key in ("receiving_yards", "rushing_yards", "passing_yards"):
            block = player.get(key) or {}
            if isinstance(block, dict) and block.get("weighted_mean") is not None:
                means.append(block["weighted_mean"])
                factor = block.get("opponent_factor")
                break
        else:
            factor = None
        if means:
            break
    if not means:
        return _blocked(
            ctx, "ANALYTIC_OUTPUT_MISSING",
            "pregame.packet.player_baselines returned no weighted_mean. Empty baselines are not a pass.",
        )
    return {
        "game_id": ctx["game_id"],
        "run_id": ctx["run_id"],
        "equation_id": "pregame.packet.player_baselines",
        "module_id": "pregame.packet",
        "metrics": {"weighted_mean": means[0], "opponent_factor": factor if factor is not None else 1.0, "players_with_baseline": len(players)},
        "denominator": int((players[0].get("receiving_yards") or players[0].get("rushing_yards") or players[0].get("passing_yards") or {}).get("games") or 0),
        "provenance": result.get("method") or "pregame.packet.player_baselines",
        "rows": players,
        "warnings": ["BASELINE_RESEARCH_ONLY; not the three-model consensus"],
        "research_only": True,
        "projection_ready": False,
    }


def run_opportunity(ctx: dict) -> dict:
    """core.possession_engine_v0.opportunity.load_opp_lookup. Not called without an as-of play-by-play path."""
    spec = (ctx.get("packet") or {}).get("opportunity_inputs")
    if not isinstance(spec, dict) or not spec.get("pbp_path") or not spec.get("game_ids"):
        return _blocked(
            ctx, "ANALYTIC_INPUT_ABSENT",
            "core.possession_engine_v0.opportunity.load_opp_lookup needs an as-of play-by-play path and game ids. "
            "A snap-share count is not that lookup.",
        )
    from core.possession_engine_v0.opportunity import load_opp_lookup

    lookup = load_opp_lookup(spec["pbp_path"], spec["game_ids"])
    rows = [{"key": key, "features": len(value) if hasattr(value, "__len__") else 1} for key, value in list(lookup.items())[:50]]
    if not rows:
        return _blocked(ctx, "EMPTY_OUTPUT", "load_opp_lookup returned no rows for the supplied games.")
    return {
        "game_id": ctx["game_id"],
        "run_id": ctx["run_id"],
        "equation_id": "core.possession_engine_v0.opportunity.load_opp_lookup",
        "module_id": "core.possession_engine_v0.opportunity",
        "metrics": {"features": sum(row["features"] for row in rows)},
        "denominator": len(spec["game_ids"]),
        "provenance": f"as-of play-by-play {spec['pbp_path']}",
        "rows": rows,
        "warnings": [],
        "research_only": True,
        "projection_ready": False,
    }
