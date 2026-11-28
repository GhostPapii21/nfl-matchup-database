"""Critical inputs block a prediction. Everything else is a disclosed gap.

Critical: game identity, a readable pregame packet, an as-of instant before
kickoff, and a play-by-play file that stops before the target week.
Stale books, missing inactives, and an absent sim_v6 entrypoint are gaps.
They are recorded and they do not erase the other games or the other layers.
"""
from __future__ import annotations

from sunday.context import parse_utc, pbp_leakage, sha256_file


TRIAL_CAP = 20_000  # research calls only; the gated 100k path is pipeline.sim100k


def critical_preflight(ctx: dict) -> dict:
    reasons = []
    gaps = []
    packet = ctx.get("packet")
    if packet is None:
        reasons.append(ctx.get("packet_error") or f"no pregame packet for {ctx['game_id']}")
    else:
        gid = (packet.get("game") or {}).get("game_id")
        if gid != ctx["game_id"]:
            reasons.append(f"packet game_id {gid} != requested {ctx['game_id']}")
        for field, value in (("away", ctx.get("away")), ("home", ctx.get("home")),
                             ("season", ctx.get("season")), ("week", ctx.get("week"))):
            if not value:
                reasons.append(f"game.{field} is missing")
    kickoff = ctx.get("kickoff_utc")
    as_of = ctx.get("as_of")
    if kickoff is None:
        reasons.append("kickoff time is missing, so the as-of boundary cannot be checked")
    elif as_of is None:
        reasons.append("as_of timestamp is missing")
    elif as_of >= kickoff:
        reasons.append(
            f"as_of {as_of.isoformat()} is not before kickoff {kickoff.isoformat()} "
            "(post-kickoff inputs are not used for a pregame prediction)"
        )
    schedule_kick = parse_utc((ctx.get("schedule") or {}).get("kickoff_utc"))
    if kickoff is not None and schedule_kick is not None and abs((schedule_kick - kickoff).total_seconds()) > 60:
        reasons.append(
            f"kickoff sources disagree: schedule {schedule_kick.isoformat()} vs "
            f"{ctx.get('kickoff_source')} {kickoff.isoformat()}. The run does not choose one."
        )
    trials = int(ctx.get("trials") or 0)
    if trials < 1:
        reasons.append("trials must be at least 1")
    elif trials > TRIAL_CAP:
        reasons.append(
            f"trials {trials} exceed the research cap {TRIAL_CAP}. "
            "The gated 100,000-trial path is `python -m pipeline.sim100k --game <id>` and is not started here."
        )
    leakage = None
    pbp = ctx.get("pbp_path")
    if packet is not None and ctx.get("season") and ctx.get("week"):
        if pbp is None or not pbp.is_file():
            reasons.append(
                f"no as-of play-by-play data/historical/nflverse/pbp_{ctx['season']}_w1_{ctx['week'] - 1}_pulled_*.parquet"
            )
        else:
            leakage = pbp_leakage(pbp, ctx["season"], ctx["week"], ctx["game_id"])
            if leakage["contains_target_game"]:
                reasons.append(f"as-of play-by-play contains the target game {ctx['game_id']}")
            if leakage["weeks_at_or_after_target"]:
                reasons.append(
                    f"as-of play-by-play contains week >= {ctx['week']}: {leakage['weeks_at_or_after_target']}"
                )
    cfg = ctx.get("config_hit") or {}
    if cfg.get("status") != "OK":
        gaps.append({"item": "possession_config", "severity": "noncritical",
                     "detail": cfg.get("reason", "possession config unavailable")})
    return {
        "ok": not reasons,
        "critical": reasons,
        "noncritical_so_far": gaps,
        "policy": {
            "critical": [
                "packet identity",
                "as_of strictly before kickoff",
                "as-of play-by-play exists and has no target week or target game",
                f"research trial count between 1 and {TRIAL_CAP}",
            ],
            "noncritical": [
                "freshness STALE/GAP/MISSING rows",
                "official inactives",
                "tools/sim_v6.py absent",
                "Lightning engine absent",
                "possession config absent",
                "100k gate refusal",
                "routes and coverage shells with no free source",
            ],
        },
        "leakage": leakage,
        "pbp_sha256": sha256_file(pbp),
        "packet_sha256": sha256_file(ctx.get("packet_path")),
        "config_sha256": sha256_file(ctx.get("config_path")),
        "repository_root": True,
    }
