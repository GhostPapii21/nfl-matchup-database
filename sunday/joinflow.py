"""Join research, script, player, and market artifacts for one game.

The decision board reads this packet. A missing hash, an as-of after a known
kickoff, or a withheld probability stays visible. Nothing here invents a
coverage assignment or a 100k probability.
"""
from __future__ import annotations

from datetime import datetime


def _qb_script(script: dict | None, player: str) -> dict:
    """Point at script-model records. Distributions stay in those artifacts."""
    if not isinstance(script, dict):
        return {"status": "UNAVAILABLE", "reason": "no script manifest was joined"}
    hits = []
    for model in script.get("models") or []:
        if not isinstance(model, dict):
            continue
        if model.get("engine_id") != "possession_engine_v0" or not model.get("simulated"):
            continue
        hits.append({
            "engine_id": model.get("engine_id"),
            "method": model.get("method"),
            "trials": model.get("trials"),
            "seed": model.get("seed"),
            "acceptance_100k": False,
            "branch_artifacts": model.get("branch_artifacts"),
            "scoring_conservation": model.get("scoring_conservation"),
            "player": player,
        })
    if not hits:
        return {"status": "UNAVAILABLE", "reason": "no simulated possession script record was joined", "player": player}
    return {"status": "JOINED", "records": hits, "note": "Branch files keep pass_yds and pass_td separate. They are not pooled."}


def _player_theses(players: dict | None, script: dict | None) -> list[dict]:
    """Expose existing engine distributions without inventing line probabilities."""
    theses = []
    for team in (players or {}).get("teams") or []:
        for person in team.get("players") or []:
            name = person.get("player")
            pid = person.get("player_id")
            if not name or not pid:
                continue
            pos = person.get("pos")
            projections = person.get("projections") or {}
            sit = person.get("situational") or {}
            receiving = projections.get("receiving") or {}
            rushing = projections.get("rushing") or {}
            candidates = {
                "rec_yds": receiving.get("receiving_yards"),
                "receptions": receiving.get("receptions"),
                "targets": receiving.get("volume"),
                "rush_yds": rushing.get("rushing_yards"),
                "rush_attempts": rushing.get("rush_attempts"),
                "rush_rec_yds": projections.get("rush_plus_receiving"),
                "td_opportunity": projections.get("td_opportunity"),
            }
            if pos == "QB":
                candidates["pass_yds"] = projections.get("passing")
            for market, projection in candidates.items():
                if not isinstance(projection, dict) or not projection:
                    continue
                theses.append({
                    "thesis_id": f"player:{pid}:{market}",
                    "subject": name,
                    "player_id": pid,
                    "team": team.get("team"),
                    "subject_kind": "player",
                    "market": market,
                    "side": "over",
                    "line": None,
                    "projection": projection,
                    "models": [],
                    "role_tag": "volume",
                    "efficiency_dependent": True,
                    "evidence_for": [],
                    "evidence_against": [{"severity": "material",
                        "text": "No verified market-line simulation probability was joined."}],
                    "sample_quality": {"withheld": True, "blocks_reads": True,
                        "limitation": "Research distributions only; no line-specific probability inferred."},
                    "joined_evidence": {
                        "pressure_targets": sit.get("pressure_targets"),
                        "coverage_assignment": sit.get("coverage_route_access"),
                        "opponent_quality": sit.get("opponent_quality"),
                        "red_zone": sit.get("red_zone"),
                        "goal_line": sit.get("goal_line"),
                        "efficiency": {"receiving": receiving.get("efficiency"),
                                       "rushing": rushing.get("efficiency")},
                        "script": _qb_script(script, name) if pos == "QB" else None,
                    },
                })
    return theses


def build_joined_decision_input(
    *,
    game: dict,
    kickoff_utc: str | None,
    kickoff_verification: str | None,
    as_of: datetime,
    research: dict | None,
    script: dict | None,
    players: dict | None,
    market_packet: dict,
    hashes: dict,
    base_packet: dict,
) -> dict:
    """Return a decision packet whose provenance lists the artifact hashes."""
    problems = []
    if kickoff_verification != "VERIFIED":
        problems.append("kickoff is UNVERIFIED, so as-of was not compared with an authoritative kickoff")
    elif not kickoff_utc:
        problems.append("verified kickoff timestamp missing")
    else:
        try:
            kick = datetime.fromisoformat(kickoff_utc)
            if as_of.utcoffset() is None or kick.utcoffset() is None:
                problems.append("as-of or kickoff lacked a timezone")
            elif as_of >= kick:
                problems.append("as-of is at or after the authoritative kickoff")
        except (TypeError, ValueError):
            problems.append("invalid kickoff timestamp")
    for name in ("research", "script", "player_board"):
        if not hashes.get(name):
            problems.append(f"missing sha256 for {name}")
    theses = _player_theses(players, script)
    packet = dict(base_packet)
    packet["theses"] = list(packet.get("theses") or []) + theses
    packet["joined"] = {
        "research_sha256": hashes.get("research"),
        "script_sha256": hashes.get("script"),
        "player_board_sha256": hashes.get("player_board"),
        "as_of_utc": as_of.isoformat(),
        "kickoff_utc": kickoff_utc,
        "kickoff_verification": kickoff_verification,
        "problems": problems,
        "scoring_conservation": next(
            (
                model.get("scoring_conservation")
                for model in (script or {}).get("models") or []
                if isinstance(model, dict) and model.get("scoring_conservation")
            ),
            {"status": "UNAVAILABLE", "evidence_tier": "unavailable"},
        ),
        "research_joined": isinstance(research, dict),
        "player_count": (players or {}).get("player_count"),
        "projection_ready": False,
    }
    packet["projection_ready"] = False
    packet["game_id"] = game.get("game_id")
    packet["home"] = game.get("home")
    packet["away"] = game.get("away")
    packet["kickoff_utc"] = kickoff_utc
    return packet


def hashes_match(recorded: dict, actual: dict) -> bool:
    """True only when every recorded artifact hash equals the file that was just written."""
    required = {"research", "script", "player_board"}
    if not required.issubset(recorded) or not required.issubset(actual):
        return False
    for key, value in recorded.items():
        if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
            return False
        if actual.get(key) != value:
            return False
    return True
