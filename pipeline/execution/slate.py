"""Slate view of execution receipts. Executed phases are separate from merely available ones."""
from __future__ import annotations

REFUSING = {"FAILED", "MISSING", "STALE", "BLOCKED", "NOT_YET"}


def slate_summary(results: list[dict]) -> dict:
    games = []
    partial_games: list[str] = []
    refused_games: list[str] = []
    for res in results:
        executed, available, partial = [], [], []
        for phase in res.get("phases") or []:
            prerequisite = (phase.get("prerequisite") or {}).get("evidence_class")
            if phase.get("status") == "PASS" and phase.get("evidence_class") == "VALIDATED":
                executed.append(phase["phase_id"])
            elif prerequisite in {"FRESH", "DISCOVERED"} and phase.get("status") != "PASS":
                available.append(phase["phase_id"])
            if phase.get("status") == "PARTIAL":
                partial.append(phase["phase_id"])
        games.append({
            "game_id": res.get("game_id"),
            "run_id": res.get("run_id"),
            "executed_phases": executed,
            "available_only_phases": available,
            "partial_phases": partial,
            "projection_ready": False,
            "research_only": True,
        })
        game_id = res.get("game_id")
        if partial and game_id not in partial_games:
            partial_games.append(game_id)
        refused = res.get("status") in REFUSING or any((p.get("status") in REFUSING) for p in (res.get("phases") or []))
        if refused and game_id not in refused_games:
            refused_games.append(game_id)
    return {
        "games": games,
        "partial_games": partial_games,
        "refused_games": refused_games,
        "projection_ready": False,
        "research_only": True,
    }


def render_slate(summary: dict) -> str:
    lines = [
        "# Execution slate",
        "",
        "Research only. projection_ready is false. A fresh or discovered input is not execution.",
        "",
        "| Game | Run | Executed | Merely available | Partial |",
        "| --- | --- | --- | --- | --- |",
    ]
    for game in summary.get("games") or []:
        lines.append(
            f"| {game['game_id']} | {game['run_id']} | {game['executed_phases'] or '-'} | "
            f"{game['available_only_phases'] or '-'} | {game['partial_phases'] or '-'} |"
        )
    partial = ", ".join(summary.get("partial_games") or []) or "-"
    refused = ", ".join(summary.get("refused_games") or []) or "-"
    lines += ["", f"PARTIAL GAMES: {partial}", f"REFUSED GAMES: {refused}", ""]
    return "\n".join(lines)
