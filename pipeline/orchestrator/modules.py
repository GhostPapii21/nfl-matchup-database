"""Adapters over existing callables. Nothing here is a new model.

sim_v6 is a receipt-only absence check. pipeline.sim100k preflight is the NFL-43
gate and is not relabeled as sim_v6. Freshness and the phase checker stay
non-analytical. projection_ready is never set.
"""
from __future__ import annotations

from pathlib import Path

from .spec import GameCall, ModuleResult, ModuleSpec

ROOT = Path(__file__).resolve().parents[2]
_PASS = {"PASS", "PARTIAL"}


def game_identity(call: GameCall) -> ModuleResult:
    game = call.packet.get("game") or {}
    return ModuleResult(status="PASS", output={
        "entrypoint": "packet.game",
        "game_id": game.get("game_id"),
        "away": game.get("away"),
        "home": game.get("home"),
        "season": game.get("season"),
        "week": game.get("week"),
        "date": game.get("date"),
        "kickoff_et": game.get("kickoff_et"),
        "roof": game.get("roof"),
        "site": game.get("site"),
    })


def freshness_check(call: GameCall) -> ModuleResult:
    from pipeline.freshness import check

    rows = check(call.packet)
    slim = [{"source": r.get("source"), "status": r.get("status"), "reason": r.get("reason")} for r in rows]
    bad = [r for r in slim if r["status"] not in ("FRESH", "NOT_REQUIRED")]
    warnings = [f"{r['source']} {r['status']}: {r['reason']}" for r in bad]
    return ModuleResult(
        status="PASS" if not bad else "PARTIAL",
        output={"entrypoint": "pipeline.freshness.check", "rows": slim, "analytical": False},
        warnings=warnings,
    )


def phase_ledger(call: GameCall) -> ModuleResult:
    from pipeline.phases import ledger

    led = ledger(call.packet)
    phases = [{"phase": p["phase"], "name": p["name"], "status": p["status"]} for p in led.get("phases") or []]
    summary = led.get("summary") or {}
    return ModuleResult(
        status="PASS",
        output={
            "entrypoint": "pipeline.phases.ledger",
            "schema": led.get("schema"),
            "summary": summary,
            "phases": phases,
            "phase15_status": (led.get("phase15") or {}).get("status"),
            "analytical": False,
        },
        warnings=[f"phase checker is not analytical execution; summary {summary}"],
    )


def _team_blocks(packet: dict, off: str, defense: str):
    teams = packet.get("teams") or {}
    offense = ((teams.get(off) or {}).get("offense") or {})
    defending = ((teams.get(defense) or {}).get("defense") or {})
    return offense.get("produced"), offense.get("rank"), defending.get("allowed"), defending.get("rank")


def matchup_edges(call: GameCall) -> ModuleResult:
    from pregame.packet import edges

    game = call.packet.get("game") or {}
    away, home = game.get("away"), game.get("home")
    directions = []
    missing = []
    for offense, defense in ((away, home), (home, away)):
        off_sum, off_rank, def_sum, def_rank = _team_blocks(call.packet, offense, defense)
        if not (off_sum and off_rank and def_sum and def_rank):
            missing.append(f"{offense} vs {defense}")
            continue
        rows = edges(offense, off_sum, off_rank, defense, def_sum, def_rank)
        directions.append({"offense": offense, "defense": defense, "rows": rows, "n": len(rows)})
    output = {"entrypoint": "pregame.packet.edges", "directions": directions, "missing": missing}
    if not directions:
        return ModuleResult(
            status="PARTIAL",
            output=output,
            warnings=["matchup edges missing offense or defense blocks: " + ", ".join(missing)],
        )
    return ModuleResult(status="PASS", output=output)


def rain_adjustment(call: GameCall) -> ModuleResult:
    from pregame import rain_model
    from pregame.packet import rain_adjusted

    weather = call.packet.get("weather") or {}
    if weather.get("status") != "OK":
        return ModuleResult(
            status="NOT_APPLICABLE",
            output={
                "equation_id": "pregame.rain_model.factor",
                "entrypoint": "pregame.rain_model.factor",
                "reason": f"weather status {weather.get('status', 'absent')}; rain adjustment not applied",
                "subject_invoked": False,
            },
        )
    kick = weather.get("at_kickoff") or {}
    during = weather.get("during_game") or {}
    rain = float(kick.get("precip_chance_pct") or 0) / 100.0
    wind = float(during.get("wind_mph_max") or kick.get("wind_mph") or 0)
    metrics = ("attempts", "pass_yards", "completion_pct", "yards_per_attempt")
    factors = {metric: rain_model.factor(metric, rain, wind) for metric in metrics}
    meta = rain_model.coefficients().get("_meta") or {}
    game = call.packet.get("game") or {}
    listed = game.get("listed_qbs") or {}
    teams = []
    for team in (game.get("away"), game.get("home")):
        offense = ((call.packet.get("teams") or {}).get(team) or {}).get("offense")
        if not offense:
            continue
        block = rain_adjusted(offense, weather, listed.get(team))
        teams.append({
            "team": team,
            "status": block.get("status"),
            "receivers": len(block.get("receivers") or []),
            "forecast_attempts": ((block.get("team_passing") or {}).get("forecast") or {}).get("attempts"),
        })
    return ModuleResult(status="PASS", output={
        "equation_id": "pregame.rain_model.factor",
        "entrypoint": "pregame.rain_model.factor",
        "factors": factors,
        "rain": rain,
        "wind_mph": wind,
        "rain_team_games": meta.get("rain_team_games"),
        "teams": teams,
        "subject_invoked": True,
    })


def ngs_matchup(call: GameCall) -> ModuleResult:
    from pipeline import freshness
    from pipeline.ngs_matchup import check

    game = call.packet.get("game") or {}
    teams = [t for t in (game.get("away"), game.get("home")) if t]
    paths = {}
    for name in ("ngs_passing", "ngs_receiving", "ngs_rushing"):
        rel = freshness.CACHE_FILE[name]
        path = freshness.CACHE / rel
        paths[name] = str(path) if path.is_file() else None
    result = check(teams, game.get("week"), paths)
    status = result.get("status") or "MISSING"
    missing_wanted = [row["field"] for row in (result.get("fields") or {}).get("missing") or [] if row.get("source") == "public_ngs"]
    warnings = [] if status == "FRESH" else [result.get("reason") or status]
    return ModuleResult(status=status, output={
        "entrypoint": "pipeline.ngs_matchup.check",
        "status": status,
        "reason": result.get("reason"),
        "teams": result.get("teams"),
        "week": result.get("week"),
        "missing_wanted": missing_wanted,
        "analytical": False,
    }, warnings=warnings)


def sim100k_preflight(call: GameCall) -> ModuleResult:
    from pipeline.sim100k import preflight

    report = preflight(call.packet, include_phases=False)
    reasons = list(report.get("reasons") or [])
    ran = bool(report.get("ran"))
    return ModuleResult(
        status="PASS" if ran else "REFUSED",
        output={
            "entrypoint": "pipeline.sim100k.preflight",
            "ran": ran,
            "ok": bool(report.get("ok")),
            "gates": report.get("gates") or {},
            "reasons": reasons,
            "engine_invoked": False,
            "label": "NFL-43 possession preflight; not sim_v6",
            "analytical": False,
        },
        warnings=([reasons[0]] if reasons else []),
    )


def sim_v6_contract(call: GameCall) -> ModuleResult:
    path = ROOT / "tools" / "sim_v6.py"
    if path.is_file():
        return ModuleResult(status="FAILED", output={
            "entrypoint": "tools/sim_v6.py",
            "reason": "PRESENT_BUT_NOT_WIRED",
            "subject_invoked": False,
            "receipt_only": True,
            "path": "tools/sim_v6.py",
        }, warnings=["tools/sim_v6.py is present but this run does not execute it"])
    return ModuleResult(status="BLOCKED", output={
        "entrypoint": "tools/sim_v6.py",
        "reason": "MODULE_ABSENT",
        "subject_invoked": False,
        "receipt_only": True,
        "path": "tools/sim_v6.py",
    }, warnings=["tools/sim_v6.py is absent; no substitute engine was run"])


def default_registry() -> list[ModuleSpec]:
    """Existing modules only. Independent work depends on game identity and fans out together."""
    identity = ("game_identity",)
    return [
        ModuleSpec(
            "game_identity", "adapter", game_identity, critical=True, timeout_sec=5, retries=0,
            inputs=("game.game_id", "game.away", "game.home", "game.season", "game.week", "game.kickoff_et"),
            required_inputs=("game.game_id", "game.away", "game.home"),
            output_contract="game_id, away, home, season, week, kickoff",
        ),
        ModuleSpec(
            "freshness_check", "freshness", freshness_check, depends_on=identity, timeout_sec=30, retries=1,
            inputs=("packet sources", "weather", "books"),
            freshness=("schedule", "play_by_play", "rosters", "depth_charts", "snap_counts", "weather", "odds"),
            output_contract="source status rows from pipeline.freshness.check",
        ),
        ModuleSpec(
            "phase_ledger", "freshness", phase_ledger, depends_on=identity, timeout_sec=60, retries=1,
            inputs=("pregame packet",),
            freshness=("schedule", "official_inactives"),
            output_contract="nfl56-phase-ledger summary; not an execution receipt",
        ),
        ModuleSpec(
            "matchup_edges", "analytical", matchup_edges, depends_on=identity, timeout_sec=20, retries=1,
            inputs=("teams.*.offense.produced", "teams.*.offense.rank", "teams.*.defense.allowed", "teams.*.defense.rank"),
            output_contract="pregame.packet.edges rows for both directions",
        ),
        ModuleSpec(
            "rain_adjustment", "analytical", rain_adjustment, depends_on=identity, timeout_sec=20, retries=1,
            inputs=("weather.at_kickoff", "weather.during_game", "teams.*.offense"),
            freshness=("weather",),
            output_contract="pregame.rain_model.factor values for attempts, yards, completion",
        ),
        ModuleSpec(
            "ngs_matchup", "adapter", ngs_matchup, depends_on=identity, timeout_sec=30, retries=1,
            inputs=("game.away", "game.home", "game.week", "public NGS weekly files"),
            freshness=("ngs_passing", "ngs_receiving", "ngs_rushing"),
            output_contract="pipeline.ngs_matchup.check status; missing fields stay unknown",
        ),
        ModuleSpec(
            "sim100k_preflight", "gate", sim100k_preflight, depends_on=identity, timeout_sec=60, retries=0,
            inputs=("pregame packet", "known_flags", "engine config"),
            freshness=("official_inactives", "four_book_prices"),
            output_contract="pipeline.sim100k.preflight gates; engine not invoked",
        ),
        ModuleSpec(
            "sim_v6_contract", "stub", sim_v6_contract, depends_on=identity, timeout_sec=5, retries=0,
            inputs=("tools/sim_v6.py",),
            output_contract="MODULE_ABSENT or PRESENT_BUT_NOT_WIRED; subject not invoked",
        ),
    ]
