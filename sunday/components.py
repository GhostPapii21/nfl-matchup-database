"""Calls into modules that already exist. Each function returns a plain dict.

Nothing here invents a score, a shell, or a sim_v6 result. If the entrypoint
or its as-of input is missing, the dict says so and ``ran`` is false.
"""
from __future__ import annotations

import sys
import threading
from pathlib import Path

from sunday.context import ROOT

_PATH_LOCK = threading.Lock()


DOCUMENTED_SIM_V6 = ROOT / "tools" / "sim_v6.py"
SIMV56_SCRATCH = ROOT / "calibration" / "simv56" / "engines" / "cc_sim_v6.py"
SIMV56_SRC = ROOT / "calibration" / "simv56" / "runs" / "2026-11-01_shared_src"
LIGHTNING_CANDIDATES = (
    ROOT / "tools" / "lightning.py",
    ROOT / "core" / "lightning_engine",
    ROOT / "calibration" / "lightning.py",
)


def _engine_path() -> None:
    with _PATH_LOCK:
        for path in (ROOT / "core" / "possession_engine_v0", ROOT / "core" / "period_engine_v0", ROOT):
            text = str(path)
            if text not in sys.path:
                sys.path.insert(0, text)


def _display_path(path) -> str | None:
    if path is None:
        return None
    try:
        return str(Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return Path(path).name


def _dist(values) -> dict:
    import numpy as np

    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return {"n": 0}
    qs = np.percentile(arr, [10, 50, 90])
    return {
        "n": int(arr.size),
        "mean": round(float(arr.mean()), 4),
        "p10": round(float(qs[0]), 4),
        "p50": round(float(qs[1]), 4),
        "p90": round(float(qs[2]), 4),
    }


def _trials(arrays: dict, keys: tuple[str, ...]) -> dict:
    import numpy as np

    out = {}
    for key in keys:
        arr = np.asarray(arrays[key])
        if arr.dtype == bool:
            out[key] = [bool(v) for v in arr.tolist()]
        else:
            out[key] = [int(v) for v in np.rint(arr).astype(int).tolist()]
    return out


def engine_roster(_ctx: dict) -> dict:
    """Identity check only. The scratch simv56 file is not executed in place of tools/sim_v6.py."""
    scratch_pbp = SIMV56_SRC / "play_by_play_2026.parquet"
    return {
        "status": "OK",
        "ran": True,
        "entrypoint": "sunday.components:engine_roster",
        "documented_sim_v6": {
            "entrypoint": "tools/sim_v6.py",
            "exists": DOCUMENTED_SIM_V6.is_file(),
            "ran": False,
            "methods": {"monte_carlo": "NOT_RUN", "calibrated_bias": "NOT_RUN", "game_randomness": "NOT_RUN"},
            "reason": (
                "PHASE_SCRIPT.md and the source run gate require tools/sim_v6.py for the three-method triad. "
                "That file is not in this revision, so the triad did not run."
                if not DOCUMENTED_SIM_V6.is_file()
                else "entrypoint exists; this slice does not launch it unless the file is the documented tool."
            ),
        },
        "simv56_scratch": {
            "entrypoint": "calibration/simv56/engines/cc_sim_v6.py:Engine.sim",
            "exists": SIMV56_SCRATCH.is_file(),
            "src_play_by_play_exists": scratch_pbp.is_file(),
            "ran": False,
            "reason": (
                "Scratch copy under calibration/simv56. It is not tools/sim_v6.py and was not imported or executed. "
                "Importing it reads a shared-src parquet at module import."
            ),
        },
        "lightning": {
            "candidates_checked": [str(p.relative_to(ROOT)) for p in LIGHTNING_CANDIDATES],
            "exists": any(p.exists() for p in LIGHTNING_CANDIDATES),
            "ran": False,
            "reason": "No Lightning engine entrypoint was found. A Monte Carlo result is not labeled Lightning.",
        },
        "main": {
            "entrypoint": None,
            "ran": False,
            "reason": (
                "No separate module is named Main. pipeline.sim100k.default_engine calls "
                "core/possession_engine_v0/simulate.simulate_games. This slice calls that function under its own name."
            ),
        },
        "possession": {
            "entrypoint": "core/possession_engine_v0/simulate.py:simulate_games",
            "exists": (ROOT / "core" / "possession_engine_v0" / "simulate.py").is_file(),
        },
        "period": {
            "entrypoint": "core/period_engine_v0/monte_carlo.py:simulate_game",
            "exists": (ROOT / "core" / "period_engine_v0" / "monte_carlo.py").is_file(),
            "bias": "UNIMPLEMENTED_NO_FITTED_CALIB",
        },
    }


def phase_ledger(ctx: dict) -> dict:
    from pipeline.phases import ledger

    # The 100k gate is its own component. Passing a gate stops ledger from calling it again.
    gate = {
        "ran": False,
        "reasons": ["100k gate is the sim100k_preflight component; phase 14 is not a completed simulation"],
    }
    led = ledger(ctx["packet"], now=ctx["as_of"], gate=gate)
    phases = []
    for row in led.get("phases") or []:
        phases.append({
            "phase": row.get("phase"),
            "name": row.get("name"),
            "status": row.get("status"),
            "missing": row.get("missing") or [],
            "stale": row.get("stale") or [],
            "gap": row.get("gap") or [],
            "not_yet": row.get("not_yet") or [],
            "not_available_from_free_sources": row.get("not_available_from_free_sources") or [],
        })
    return {
        "status": "OK",
        "ran": True,
        "entrypoint": "pipeline.phases:ledger",
        "schema": led.get("schema"),
        "checked_utc": led.get("checked_utc"),
        "summary": led.get("summary"),
        "phase15": led.get("phase15"),
        "freshness": led.get("freshness"),
        "phases": phases,
        "projection_ready": False,
    }


def sim100k_preflight(ctx: dict) -> dict:
    from pipeline.sim100k import preflight

    report = preflight(
        ctx["packet"], now=ctx["as_of"], include_phases=False, game_id=ctx["game_id"], root=ctx["root"],
    )
    report.pop("engine_inputs", None)
    return {
        "status": "PASS" if report.get("ok") else "REFUSED",
        "ran": True,
        "executed_100k": False,
        "entrypoint": "pipeline.sim100k:preflight",
        "gate": report,
        "reason": "Preflight only. python -m pipeline.sim100k is the gated 100k command and was not started.",
    }


def matchup_fields(ctx: dict) -> dict:
    from pipeline.matchup_sources import fields

    pbp = ctx.get("pbp_path")
    result = fields(
        (ctx["away"], ctx["home"]),
        ctx["season"],
        ctx["week"],
        pbp_path=str(pbp) if pbp else None,
        pbp_status="FRESH",
        pbp_as_of=ctx["as_of"].isoformat(),
    )
    compact = {}
    for name, row in result.items():
        value = row.get("value")
        source = row.get("source")
        if pbp is not None and isinstance(source, str):
            source = source.replace(str(pbp), _display_path(pbp) or pbp.name)
        compact[name] = {
            "status": row.get("status"),
            "source": source,
            "reason": row.get("reason"),
            "as_of": row.get("as_of"),
            "value_keys": sorted(value)[:12] if isinstance(value, dict) else None,
            "n_keys": len(value) if isinstance(value, dict) else None,
        }
        if name == "qb_success_vs_defense" and isinstance(value, dict):
            # Side-by-side rates are the analysis. Keep them, they are already week-filtered.
            compact[name]["value"] = value
        elif name == "target_location" and isinstance(value, dict):
            compact[name]["teams"] = sorted(value)
    return {
        "status": "OK",
        "ran": True,
        "entrypoint": "pipeline.matchup_sources:fields",
        "fields": compact,
        "pbp": None if pbp is None else pbp.name,
    }


def _players(side: dict) -> list[dict]:
    offense = (side or {}).get("offense") or {}
    grouped = offense.get("players") or {}
    snaps = offense.get("offense_snap_share") or {}
    rows = []
    if not isinstance(grouped, dict):
        return rows
    keep = (
        "player", "player_id", "pos", "games", "targets", "receptions", "yards", "td",
        "target_share", "air_yards_share", "avg_depth_of_target", "yards_per_target",
        "red_zone_targets", "carries", "carry_share", "yards_per_carry", "red_zone_carries",
        "rush_attempts_official", "rushing_yards_official",
    )
    for role, people in grouped.items():
        if not isinstance(people, list):
            continue
        for person in people:
            if not isinstance(person, dict):
                continue
            row = {k: person.get(k) for k in keep if k in person}
            row["role"] = role
            log = person.get("log") or []
            row["log_weeks"] = [item.get("week") for item in log if isinstance(item, dict)]
            name = person.get("player")
            row["snap_share"] = snaps.get(name) if isinstance(snaps, dict) else None
            row["snap_share_matched"] = bool(isinstance(snaps, dict) and name in snaps)
            row["routes"] = None
            row["route_participation"] = None
            row["routes_status"] = "NOT_IN_PACKET"
            rows.append(row)
    return rows


def _injuries(side: dict) -> dict:
    block = (side or {}).get("injuries") or {}
    report = []
    for row in block.get("official_report") or []:
        if not isinstance(row, dict):
            continue
        report.append({
            "player": row.get("player"),
            "position": row.get("position"),
            "game_status": row.get("game_status"),
            "practice_status": row.get("practice_status"),
            "injury": row.get("injury"),
            "starter": row.get("starter"),
            "source": row.get("source"),
        })
    return {
        "official_report_status": block.get("official_report_status"),
        "official_report": report,
        "espn_live_status": block.get("espn_live_status"),
        "note": block.get("note"),
    }


def packet_research(ctx: dict) -> dict:
    from dashboard.opportunity import script_multipliers

    packet = ctx["packet"]
    teams = packet.get("teams") or {}
    home, away = ctx["home"], ctx["away"]
    market = packet.get("market") or {}
    spread = market.get("home_spread")
    sides = {}
    for team in (away, home):
        block = teams.get(team) or {}
        defense = block.get("defense") or {}
        allowed = defense.get("allowed") or {}
        keep_allowed = (
            "games", "weeks", "points_pg", "plays_pg", "pass_att_pg", "pressure_rate", "sack_rate",
            "qb_hits", "yards_per_carry", "third_down_rate", "red_zone_td_rate", "red_zone_drives",
            "neutral_pass_rate", "explosive_pass_pg", "explosive_rush_pg", "avg_depth_of_target",
        )
        favored_by = None if spread is None else ((-float(spread)) if team == home else float(spread))
        pass_m, rush_m = script_multipliers(favored_by)
        depth = (block.get("depth_chart") or {})
        starters = []
        for row in depth.get("starters") or []:
            if isinstance(row, dict):
                starters.append({"slot": row.get("slot"), "player": row.get("player"), "group": row.get("group")})
        moves = block.get("roster_moves") or {}
        defenders = defense.get("defenders") or {}
        sides[team] = {
            "players": _players(block),
            "offense_produced_games": ((block.get("offense") or {}).get("produced") or {}).get("games"),
            "defense_allowed": {k: allowed.get(k) for k in keep_allowed if k in allowed},
            "defense_rank": defense.get("rank"),
            "defenders": {
                "status": defenders.get("status"),
                "weeks": defenders.get("weeks"),
                "coverage": defenders.get("coverage"),
                "pass_rush": defenders.get("pass_rush"),
            },
            "formation_zone_splits": block.get("formation_zone_splits"),
            "injuries": _injuries(block),
            "depth_status": depth.get("status"),
            "depth_as_of": depth.get("as_of"),
            "starters": starters,
            "roster_moves": {
                "arrivals": (moves.get("arrivals_from_other_teams") or [])[:12],
                "departures": (moves.get("departures_to_other_teams") or [])[:12],
                "note": moves.get("note"),
            },
            "script_multipliers": {
                "entrypoint": "dashboard.opportunity:script_multipliers",
                "favored_by_points": favored_by,
                "pass_attempt_multiplier": pass_m,
                "rush_attempt_multiplier": rush_m,
                "note": "Closed-form tilt from the listed spread. Not a game-script distribution and not applied to the simulators.",
            },
        }
    weather = packet.get("weather") or {}
    prior = packet.get("team_projection") or {}
    return {
        "status": "OK",
        "ran": True,
        "entrypoint": "pregame packet read + dashboard.opportunity:script_multipliers",
        "packet_generated_utc": packet.get("generated_utc"),
        "packet_status": packet.get("status"),
        "coaches": (packet.get("game") or {}).get("coaches"),
        "listed_qbs": (packet.get("game") or {}).get("listed_qbs"),
        "roof": (packet.get("game") or {}).get("roof"),
        "surface": (packet.get("game") or {}).get("surface"),
        "rest_days": {
            "away": (packet.get("game") or {}).get("away_rest_days"),
            "home": (packet.get("game") or {}).get("home_rest_days"),
        },
        "weather": {
            "status": weather.get("status"),
            "source": weather.get("source"),
            "retrieved_utc": weather.get("retrieved_utc"),
            "kickoff_utc": weather.get("kickoff_utc"),
            "roof": weather.get("roof"),
            "at_kickoff": weather.get("at_kickoff"),
            "flags": weather.get("flags"),
        },
        "sides": sides,
        "prior_packet_projection": {
            "ran_in_this_command": False,
            "status": prior.get("status"),
            "engine": prior.get("engine"),
            "trials": prior.get("trials"),
            "history_games": prior.get("history_games"),
            "includes_prior_season": prior.get("includes_prior_season"),
            "note": prior.get("note"),
            "samplers": prior.get("samplers"),
            "generated_utc": packet.get("generated_utc"),
        },
        "coverage_shells": {
            "status": "NOT_AVAILABLE_FROM_FREE_SOURCES",
            "ran_shell_model": False,
            "note": "Man/zone and coverage shell are listed unavailable by pipeline phase 7. Formation and zone splits above are the executed packet fields.",
        },
    }


def market_lines(ctx: dict) -> dict:
    books = (ctx["packet"] or {}).get("books") or {}
    markets = books.get("markets") or {}
    rows = []
    if isinstance(markets, dict):
        for name, block in markets.items():
            if not isinstance(block, dict):
                continue
            for book, quote in (block.get("books") or {}).items():
                if not isinstance(quote, dict):
                    continue
                rows.append({
                    "market": name,
                    "book": book,
                    "line": quote.get("line"),
                    "prices": quote.get("prices"),
                    "no_vig": quote.get("no_vig"),
                    "hold": quote.get("hold"),
                    "last_update": quote.get("last_update"),
                    "source": quote.get("source"),
                })
    return {
        "status": "OK" if rows else "MISSING",
        "ran": True,
        "entrypoint": "pregame packet books",
        "books_status": books.get("status"),
        "source": books.get("source"),
        "retrieved_utc": books.get("retrieved_utc"),
        "consensus_home_spread": (ctx["packet"].get("market") or {}).get("home_spread"),
        "consensus_total": (ctx["packet"].get("market") or {}).get("total"),
        "consensus_source": (ctx["packet"].get("market") or {}).get("source"),
        "quotes": rows,
    }


def run_possession(ctx: dict) -> dict:
    hit = ctx.get("config_hit") or {}
    if hit.get("status") != "OK":
        return {"status": "ABSENT", "ran": False, "entrypoint": "core/possession_engine_v0/simulate.py:simulate_games",
                "reason": hit.get("reason")}
    _engine_path()
    from config_load import load_config
    from simulate import simulate_games, stable_seed

    cfg = load_config(ctx["config_path"])
    game = cfg["game"]
    seed = stable_seed(int(cfg["seed_base"]), int(game["week_asof_exclusive"]), cfg["config_id"])
    result = simulate_games(
        cfg, pbp_path=ctx["pbp_path"], n=int(ctx["trials"]), seed=seed, record_players=True,
    )
    if result.get("status") not in ("OK", "OK_WITH_SPARSE_FLAGS"):
        return {
            "status": result.get("status") or "FAILED",
            "ran": False,
            "entrypoint": "core/possession_engine_v0/simulate.py:simulate_games",
            "error": result.get("error"),
            "n_completed": result.get("n_completed"),
        }
    arrays = result["arrays"]
    keys = (
        "q1_home", "q1_away", "q2_home", "q2_away", "q3_home", "q3_away", "q4_home", "q4_away",
        "h1_home", "h1_away", "reg_home", "reg_away", "ot_home", "ot_away", "went_ot",
    )
    box = result.get("player_box") or {}
    player_summary = None
    if box.get("columns") is not None and box.get("values") is not None:
        from player_box import summarize
        player_summary = summarize(box["columns"], box["values"])
    hist = result.get("history_evidence") or {}
    return {
        "status": "OK",
        "ran": True,
        "entrypoint": "core/possession_engine_v0/simulate.py:simulate_games",
        "engine_id": "possession_engine_v0",
        "not_named": ["Main", "Lightning", "sim_v6", "simv56"],
        "config_id": result.get("config_id"),
        "mode": result.get("mode"),
        "n_requested": result.get("n_requested"),
        "n_completed": result.get("n_completed"),
        "seed": result.get("seed"),
        "calibration": "not_fitted",
        "calibration_source": "known_flags/KNOWN_LIMITATIONS.json calibration_fitted_claim is false; this call does not fit anything",
        "pooling_silently_applied": result.get("pooling_silently_applied"),
        "semantics_overtime": (result.get("semantics") or {}).get("overtime"),
        "history_evidence": {
            **{k: hist.get(k) for k in ("n_games", "n_plays", "teams", "weeks", "season") if k in hist},
            "source": _display_path(hist.get("source")),
        },
        "pbp": _display_path(ctx["pbp_path"]),
        "regulation": {"home": _dist(arrays["reg_home"]), "away": _dist(arrays["reg_away"])},
        "quarters": {q: {"home": _dist(arrays[f"{q}_home"]), "away": _dist(arrays[f"{q}_away"])} for q in ("q1", "q2", "q3", "q4")},
        "trials": _trials(arrays, keys),
        "player_box_summary": player_summary,
        "player_box_reconciliation": (box.get("reconciliation") or None),
        "limitations": result.get("limitations"),
        "projection_ready": False,
    }


def run_period(ctx: dict) -> dict:
    _engine_path()
    from reconstruct import as_of_mask, load_pbp, period_table_from_pbp
    from monte_carlo import simulate_game

    raw = load_pbp(ctx["pbp_path"], seasons=[int(ctx["season"])])
    table = period_table_from_pbp(raw)
    asof = table[as_of_mask(table, int(ctx["season"]), int(ctx["week"]))]
    max_week = int(asof["week"].max()) if len(asof) else None
    if max_week is not None and max_week >= int(ctx["week"]):
        return {"status": "REFUSED", "ran": False, "reason": f"period table max week {max_week}"}
    seed = int(ctx["trials"]) * 1009 + int(ctx["week"]) * 17 + 20261127
    calls = (
        ("matchup_pair", dict(sampling="matchup_pair", apply_gr=False, seed=seed)),
        ("independent", dict(sampling="independent", apply_gr=False, seed=seed + 1)),
        ("game_randomness", dict(sampling="matchup_pair", apply_gr=True, seed=seed + 2)),
    )
    methods = {}
    for name, kwargs in calls:
        sim = simulate_game(asof, ctx["home"], ctx["away"], n=int(ctx["trials"]), **kwargs)
        if sim.get("error"):
            methods[name] = {"status": "FAILED", "ran": False, "error": sim.get("error"), "seed": kwargs["seed"]}
            continue
        arrays = sim["arrays"]
        methods[name] = {
            "status": "OK",
            "ran": True,
            "seed": sim.get("seed"),
            "n": sim.get("n"),
            "sampling": kwargs["sampling"],
            "apply_gr": kwargs["apply_gr"],
            "model_status": sim.get("status"),
            "summaries": sim.get("summaries"),
            "trials": _trials(arrays, ("reg_home", "reg_away", "fg_home", "fg_away")),
            "calibration": "bias_unimplemented",
        }
    return {
        "status": "OK" if any(m.get("ran") for m in methods.values()) else "FAILED",
        "ran": any(m.get("ran") for m in methods.values()),
        "entrypoint": "core/period_engine_v0/monte_carlo.py:simulate_game",
        "engine_id": "period_engine_v0",
        "not_named": ["sim_v6", "possession", "Lightning", "Main"],
        "asof_games": int(len(asof)),
        "asof_max_week": max_week,
        "pbp": Path(ctx["pbp_path"]).name,
        "bias": {"status": "UNIMPLEMENTED_NO_FITTED_CALIB", "ran": False},
        "methods": methods,
        "projection_ready": False,
    }


# Independent reads and simulators. Scripts, thresholds, and the board run after these return.
PARALLEL = (
    ("engine_roster", "sunday.components:engine_roster", engine_roster),
    ("phase_ledger", "pipeline.phases:ledger", phase_ledger),
    ("sim100k_preflight", "pipeline.sim100k:preflight", sim100k_preflight),
    ("matchup_fields", "pipeline.matchup_sources:fields", matchup_fields),
    ("packet_research", "sunday.components:packet_research", packet_research),
    ("market_lines", "sunday.components:market_lines", market_lines),
    ("possession", "core/possession_engine_v0/simulate.py:simulate_games", run_possession),
    ("period", "core/period_engine_v0/monte_carlo.py:simulate_game", run_period),
)
