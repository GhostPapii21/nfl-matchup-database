"""Human-readable Sunday reports. Research only."""
from __future__ import annotations

from sunday.preflight import ACCEPTABLE


def _lines(title: str, rows: list[dict]) -> list[str]:
    out = [f"## {title}", ""]
    if not rows:
        out.append("None.")
        out.append("")
        return out
    for row in rows:
        out.append(f"- `{row.get('id', row.get('issue', ''))}` **{row.get('status')}** — {row.get('detail')}")
    out.append("")
    return out


def render_game(packet: dict) -> str:
    runtime = packet.get("runtime") or {}
    memory = runtime.get("memory") or {}
    leak = packet.get("leakage") or {}
    lines = [
        f"# {packet.get('game_id')}",
        "",
        f"Result: **{packet.get('result')}**",
        "",
        "Research only. `projection_ready` is false. This is not a pick and not a scheduler.",
        "",
        f"- As of: {packet.get('as_of_utc')}",
        f"- Kickoff: {packet.get('kickoff_utc')}",
        f"- Command: `{packet.get('command')}`",
        f"- Code revision: `{packet.get('git_sha')}`",
        f"- Canonical sha256: `{packet.get('canonical_sha256')}`",
        f"- Wall time: {runtime.get('wall_seconds')} s",
        f"- Memory: {memory.get('detail')}",
        "",
    ]
    critical = [c for c in packet.get("checks") or [] if c.get("level") == "critical"]
    required = [c for c in packet.get("checks") or [] if c.get("level") == "required" and c.get("status") not in ACCEPTABLE]
    passed = [c for c in packet.get("checks") or [] if c.get("level") == "required" and c.get("status") in ACCEPTABLE]
    lines += _lines("Critical checks", critical)
    lines += _lines("Required checks that are not clear", required)
    lines.append(f"Required checks that are clear: {len(passed)}.")
    lines.append("")
    lines += _lines("Research layers", packet.get("layers") or [])
    roles = packet.get("roles") or {}
    lines.append("## Player roles")
    lines.append("")
    if not roles:
        lines.append("No role summary.")
        lines.append("")
    for team, block in roles.items():
        flags = block.get("availability_flags") or []
        names = ", ".join(f"{row.get('player')} ({row.get('game_status') or row.get('practice_status')})" for row in flags) or "none flagged"
        lines.append(f"- {team}: listed QB {block.get('listed_qb')}; availability flags: {names}.")
    lines.append("")
    lines.append("## Leakage")
    lines.append("")
    lines.append(f"Status: **{leak.get('status')}**.")
    for item in leak.get("late_stamps") or []:
        lines.append(f"- Late stamp: {item}")
    excluded = leak.get("excluded") or []
    lines.append(f"Excluded paths (not read): {len(excluded)}.")
    for item in excluded[:40]:
        lines.append(f"- `{item.get('path')}` — {item.get('reason')}")
    if len(excluded) > 40:
        lines.append(f"- … {len(excluded) - 40} more in packet.json")
    lines.append("")
    lines.append("## Cited outputs")
    lines.append("")
    cited = packet.get("cited_outputs") or {}
    for name, block in cited.items():
        if isinstance(block, dict):
            lines.append(f"- {name}: **{block.get('status')}** — {block.get('detail')}")
    lines.append("")
    lines.append("Inputs read:")
    lines.append("")
    for path in leak.get("inputs_read") or []:
        lines.append(f"- `{path}`")
    lines.append("")
    return "\n".join(lines)


def render_index(slate: dict) -> str:
    counts = slate.get("counts") or {}
    lines = [
        "# Sunday slate",
        "",
        "Research only. `projection_ready` is false. This command is not a scheduler.",
        "",
        f"As of {slate.get('as_of_utc')}. Concurrency {slate.get('concurrency_used')} of a cap of {slate.get('concurrency_cap')}.",
        f"Peak in-flight jobs: {slate.get('peak_in_flight')}.",
        f"Process max RSS: {slate.get('process_max_rss_kb')} KB (Linux ru_maxrss; process-wide, not per game).",
        "",
        f"**{slate.get('result')}.** {counts.get('PASS', 0)} PASS, {counts.get('PARTIAL', 0)} PARTIAL, {counts.get('BLOCKED', 0)} BLOCKED.",
        "",
        "| Game | Kickoff (ET) | Result | Report |",
        "| --- | --- | --- | --- |",
    ]
    for game in slate.get("games") or []:
        link = game.get("report_rel") or ""
        lines.append(f"| [{game.get('game_id')}]({link}) | {game.get('date')} {game.get('kickoff_et')} | {game.get('result')} | `{link}` |")
    lines.append("")
    return "\n".join(lines)


def render_replay(record: dict) -> str:
    lines = [
        f"# Replay {record.get('game_id')}",
        "",
        f"Result: **{record.get('result')}**",
        f"Reproducibility: **{record.get('reproducibility')}**",
        "",
        "Research only. `projection_ready` is false. Wall time and RSS are not part of the canonical hash.",
        "",
        f"- As of: {record.get('as_of_utc')}",
        f"- Canonical sha256: `{record.get('canonical_sha256')}`",
        f"- Run A wall: {(record.get('run_a') or {}).get('wall_seconds')} s",
        f"- Run B wall: {(record.get('run_b') or {}).get('wall_seconds')} s",
        f"- Run A memory: {(record.get('run_a') or {}).get('memory')}",
        f"- Run B memory: {(record.get('run_b') or {}).get('memory')}",
        "",
        record.get("detail") or "",
        "",
    ]
    return "\n".join(lines)
