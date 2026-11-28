"""Call canonical equation modules. This file does not invent summary counts.

Only pregame.rain_model is invoked from a normal packet. A feature-table length is not an
opportunity equation, and a missing opponent factor is not filled with 1.0.
"""
from __future__ import annotations

import math


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


_STAT_KEYS = ("receiving_yards", "rushing_yards", "passing_yards")


def _finite(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _baseline_block(players: list) -> tuple[dict, str, dict] | None:
    """First player/stat block that has a finite mean, a finite opponent factor, and a positive game count."""
    for player in players:
        if not isinstance(player, dict):
            continue
        for key in _STAT_KEYS:
            block = player.get(key)
            if not isinstance(block, dict):
                continue
            games = block.get("games")
            if (_finite(block.get("weighted_mean")) and _finite(block.get("opponent_factor"))
                    and isinstance(games, int) and not isinstance(games, bool) and games > 0):
                return player, key, block
    return None


def run_player_baselines(ctx: dict) -> dict:
    """pregame.packet.player_baselines. A missing opponent factor is not filled with 1.0."""
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
    chosen = _baseline_block([p for p in (result.get("players") or []) if isinstance(p, dict)])
    if chosen is None:
        return _blocked(
            ctx, "ANALYTIC_OUTPUT_MISSING",
            "pregame.packet.player_baselines did not return a finite weighted_mean and opponent_factor "
            "on the same stat block with a positive game count. A missing factor is not set to 1.0.",
        )
    player, stat, block = chosen
    row = {
        "player": player.get("player"),
        "pos": player.get("pos"),
        "stat": stat,
        "weighted_mean": block["weighted_mean"],
        "opponent_factor": block["opponent_factor"],
        "games": block["games"],
    }
    return {
        "game_id": ctx["game_id"],
        "run_id": ctx["run_id"],
        "equation_id": "pregame.packet.player_baselines",
        "module_id": "pregame.packet",
        "metrics": {"weighted_mean": block["weighted_mean"], "opponent_factor": block["opponent_factor"]},
        "denominator": block["games"],
        "provenance": result.get("method") or "pregame.packet.player_baselines",
        "rows": [row],
        "warnings": ["BASELINE_RESEARCH_ONLY; not the three-model consensus"],
        "research_only": True,
        "projection_ready": False,
    }


def run_opportunity(ctx: dict) -> dict:
    """load_opp_lookup is a feature table. Its length is not an opportunity equation."""
    spec = (ctx.get("packet") or {}).get("opportunity_inputs")
    if not isinstance(spec, dict) or not spec.get("pbp_path") or not spec.get("game_ids"):
        return _blocked(
            ctx, "ANALYTIC_INPUT_ABSENT",
            "No as-of play-by-play path was supplied, and no per-player opportunity equation is registered. "
            "A snap-share count is not that equation.",
        )
    from core.possession_engine_v0.opportunity import load_opp_lookup

    lookup = load_opp_lookup(spec["pbp_path"], spec["game_ids"])
    nkeys = len(lookup) if isinstance(lookup, dict) else 0
    return _blocked(
        ctx, "ANALYTIC_OUTPUT_MISSING",
        "core.possession_engine_v0.opportunity.load_opp_lookup returned a feature table "
        f"({nkeys} keys), not per-player opportunity share, targets, carries, or touches. "
        "A feature count is not that equation. Route participation remains a separate source gap.",
    )
