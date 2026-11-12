"""One command per phase of the 15-phase ledger (NFL-56 item 1).

Reuses what exists: the pregame builder (`python -m pregame.build_packets`, pregame/packet.py) pulls the data and
writes its own phase ledger into each packet. This module re-checks that ledger input by input against the packet
and the freshness policy, and records for every phase which inputs are FILLED, MISSING, STALE or NOT_YET. Nothing
is skipped silently: a phase whose inputs are absent is MISSING, one that cannot exist yet is NOT_YET.

    python -m pipeline.phases --game 2026_10_WAS_NYG                 # all 15 phases, print table
    python -m pipeline.phases --game 2026_10_WAS_NYG --phase 12      # one phase
    python -m pipeline.phases --game 2026_10_WAS_NYG --write         # also write pipeline/ledgers/<game>.json
    python -m pipeline.phases --game 2026_10_WAS_NYG --strict        # exit 3 if any phase is not filled

Statuses: AUTO / PARTIAL (from the packet builder, all checked inputs present and fresh), MISSING, STALE, NOT_YET.
Phase 15 (official inactives, NFL-46) is decided per game by `phase15_status` from the official-inactives hook, not by
the packet builder's PENDING placeholder: AUTO (both clubs' official Inactives articles pulled after T-90), NOT_YET
(before T-90) or MISSING (window open but no complete official pull, or pulled too early), always with the source and
pull time. Every ledger carries it as a top-level "phase15" block. ESPN/wire lists are never used for Phase 15.
No network, no API credits, no model run.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import freshness, hooks

ROOT = Path(__file__).resolve().parents[1]
PACKETS = ROOT / "pregame" / "packets"
LEDGERS = Path(__file__).resolve().parent / "ledgers"
BLOCKING = ("MISSING", "STALE", "NOT_YET")

# phase: (name, packet inputs [dotted; "teams.*." = both teams], freshness sources, inputs no free source carries)
PHASES = {
    1: ("Slate, schedule, venue", ["game.kickoff_et", "game.date", "game.site", "game.roof", "game.listed_qbs"], ["schedule"], []),
    2: ("Player identity and position", ["teams.*.offense.players"], ["rosters"], []),
    3: ("Verified player game history", ["teams.*.offense.players", "teams.*.offense.by_game"], ["play_by_play"], []),
    4: ("Role, snaps, routes, opportunity", ["teams.*.offense.players", "teams.*.offense.offense_snap_share"], ["snap_counts"],
        ["routes run / route participation (no free source)"]),
    5: ("Team offense/defense baselines", ["teams.*.defense.allowed", "teams.*.offense.produced", "teams.*.defense.rank"], ["play_by_play"], []),
    6: ("Opponent context and game script", ["market.home_spread", "market.total"], ["schedule"], ["the script call itself (analyst)"]),
    7: ("Coverage structure and shell", ["teams.*.defense.allowed.dropbacks_charted"], ["ftn_charting"], ["man/zone and shell (no free source)"]),
    8: ("Defender assignment and explosive allowance", ["teams.*.defense.defenders"], ["pfr_defense"], ["who covers whom (no confirmed assignment)"]),
    9: ("QB pressure, blitz, scramble", ["teams.*.defense.allowed"], ["play_by_play", "ftn_charting"], ["true pressure rate (sacks + hits is a floor)"]),
    10: ("Offensive line, pass rush, coaching", ["teams.*.depth_chart", "game.coaches"], ["depth_charts"], ["line grades (paid source)"]),
    11: ("Injury and depth chart", ["teams.*.injuries.official_report", "teams.*.injuries.espn_live", "teams.*.depth_chart"],
         ["official_injuries", "news_injuries", "depth_charts"], []),
    12: ("Weather, roof, travel", ["game.roof", "weather.status"], ["weather"], []),
    13: ("Timestamped book prices", ["books.markets"], ["odds", "four_book_prices"], ["true opening line"]),
    14: ("Projection and simulation (100k)", ["team_projection"], [], []),
    15: ("Final inactive pregame freeze", [], ["official_inactives"], []),
}


def _present(pk, dotted):
    cur = pk
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return cur is not None and cur != [] and cur != {} and cur != ""


def _inputs(pk, dotted):
    """Expand 'teams.*.x' to each team in the game; returns [(label, present)]."""
    if dotted.startswith("teams.*."):
        g = pk.get("game") or {}
        teams = [t for t in (g.get("away"), g.get("home")) if t] or ["<no teams>"]
        rest = dotted[len("teams.*."):]
        return [(f"teams.{t}.{rest}", _present(pk, f"teams.{t}.{rest}")) for t in teams]
    return [(dotted, _present(pk, dotted))]


def load_packet(game_id: str, packet: Path | None = None) -> dict:
    p = Path(packet) if packet else PACKETS / game_id / "packet.json"
    return json.loads(p.read_text())


PHASE15_STATUSES = ("AUTO", "NOT_YET", "MISSING")
PHASE15_SOURCE = "club official site 'Inactives' article (phase15/official_inactives.py); ESPN/wire not used"


def _et(iso: str | None) -> str | None:
    d = freshness.parse_utc(iso)
    return None if d is None else d.astimezone(freshness.ET).strftime("%Y-%m-%d %I:%M %p ET")


def phase15_status(pk: dict, now: datetime | None = None, hook_impls=None) -> dict:
    """Per-game Phase 15 status (NFL-46): exactly one of AUTO / NOT_YET / MISSING, with source and pull time.
    Read-only (the hook reads the newest phase15/inactives/<game>/inactives_*.json; no network). Never invents a
    status: anything other than a complete official pull after T-90 is NOT_YET (window not open) or MISSING."""
    from datetime import timedelta
    now = now or datetime.now(timezone.utc)
    ko = freshness.kickoff_utc(pk)
    base = {"status": "MISSING", "source": PHASE15_SOURCE, "source_urls": {}, "pull_utc": None, "pull_et": None,
            "published_utc": {}, "file": None, "kickoff_utc": ko.isoformat() if ko else None,
            "posts_utc": None, "checked_utc": now.isoformat(timespec="seconds")}
    if ko is None:
        return {**base, "reason": "Kickoff time unknown, so the T-90 inactive window cannot be placed."}
    posts = ko - timedelta(minutes=freshness.INACTIVES_POST_MINUTES_BEFORE_KICKOFF)
    base["posts_utc"] = posts.isoformat()
    if now < posts:
        return {**base, "status": "NOT_YET",
                "reason": f"Official inactives post about {posts.astimezone(freshness.ET):%a %I:%M %p} ET (T-90); not available yet."}
    res = hooks.official_inactives(pk, impl=(hook_impls or {}).get("official_inactives"))
    detail = res.get("detail") if isinstance(res.get("detail"), dict) else res
    base.update(source_urls=detail.get("sources") or {}, pull_utc=detail.get("retrieved_utc"),
                pull_et=_et(detail.get("retrieved_utc")), file=detail.get("file"),
                published_utc=detail.get("published_utc") or {})
    if res.get("status") != "OK":
        return {**base, "reason": res.get("reason", "No official inactives pull.")}
    got = freshness.parse_utc(res.get("retrieved_utc"))
    if got is None:
        return {**base, "reason": "Official inactives pull has no retrieved_utc; pull time unknown is treated as missing."}
    if got < posts:
        return {**base, "reason": "Official inactives were pulled before they post (T-90); pull again."}
    g = pk.get("game") or {}
    no_src = [t for t in (g.get("away"), g.get("home")) if not (t and base["source_urls"].get(t))]
    if no_src:
        return {**base, "reason": f"Official inactives pull has no source URL for {no_src}; not accepted."}
    return {**base, "status": "AUTO", "inactives": res.get("inactives") or {},
            "reason": "Both clubs' official Inactives articles pulled after T-90."}


def run_phase(n: int, pk: dict, fresh_rows: list[dict], gate: dict | None = None, p15: dict | None = None) -> dict:
    name, inputs, sources, unavailable = PHASES[n]
    built = {r["phase"]: r for r in pk.get("phase_ledger") or []}.get(n, {})
    filled, missing, stale, not_yet = [], [], [], []
    for d in inputs:
        for label, ok in _inputs(pk, d):
            (filled if ok else missing).append(label)
    by_src = {r["source"]: r for r in fresh_rows}
    for s in sources:
        r = by_src.get(s)
        if r is None:
            missing.append(f"{s}: no freshness record")
        elif r["status"] == "FRESH" or r["status"] == "NOT_REQUIRED":
            filled.append(f"{s}: {r['status']}")
        elif r["status"] == "STALE":
            stale.append(f"{s}: {r['reason']}")
        elif r["status"] == "NOT_YET":
            not_yet.append(f"{s}: {r['reason']}")
        else:
            missing.append(f"{s}: {r['reason']}")
    if n == 14:
        g = gate or {}
        if not g.get("ran"):
            not_yet.append("100k entry point refused: " + "; ".join(r.rstrip(".") for r in (g.get("reasons") or ["gate not evaluated"])))
    if n == 15 and p15 is not None:
        # NFL-46: Phase 15 is decided by the official-inactives pull, never by the packet's PENDING placeholder.
        status = p15["status"]
        line = f"official_inactives: {p15['reason']} (source: {p15['source_urls'] or p15['source']}; pulled {p15['pull_utc'] or 'never'})"
        filled, missing, stale, not_yet = (([line], [], [], []) if status == "AUTO" else
                                           ([], [], [], [line]) if status == "NOT_YET" else ([], [line], [], []))
        return {"phase": n, "name": name, "status": status, "packet_status": built.get("status"),
                "filled": filled, "missing": missing, "stale": stale, "not_yet": not_yet,
                "not_available_from_free_sources": unavailable, "packet_detail": built.get("detail"), "phase15": p15,
                "command": f"python -m pipeline.phases --game {(pk.get('game') or {}).get('game_id')} --phase {n}"}
    if missing:
        status = "MISSING"
    elif stale:
        status = "STALE"
    elif not_yet:
        status = "NOT_YET"
    elif str(built.get("status", "")).startswith(("BLOCKED", "PENDING")) or not built:
        status = "MISSING"
        missing.append(f"packet ledger phase {n} is {built.get('status', 'absent')}")
    else:
        status = built["status"]
    return {"phase": n, "name": name, "status": status, "packet_status": built.get("status"),
            "filled": filled, "missing": missing, "stale": stale, "not_yet": not_yet,
            "not_available_from_free_sources": unavailable, "packet_detail": built.get("detail"),
            "command": f"python -m pipeline.phases --game {(pk.get('game') or {}).get('game_id')} --phase {n}"}


def ledger(pk: dict, now: datetime | None = None, phases=None, hook_impls=None, gate: dict | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    rows = freshness.check(pk, now, hook_impls)
    if gate is None and (phases is None or 14 in phases):
        from . import sim100k  # local import: sim100k imports this module
        gate = sim100k.preflight(pk, now=now, hook_impls=hook_impls, include_phases=False)
    p15 = phase15_status(pk, now, hook_impls)
    out = [run_phase(n, pk, rows, gate, p15) for n in (phases or PHASES)]
    return {"schema": "nfl56-phase-ledger/1", "game_id": (pk.get("game") or {}).get("game_id"),
            "checked_utc": now.isoformat(timespec="seconds"), "packet_generated_utc": pk.get("generated_utc"),
            "projection_ready": False, "research_only": True, "phase15": p15, "freshness": rows, "phases": out,
            "summary": {s: sum(1 for p in out if p["status"] == s) for s in sorted({p["status"] for p in out})}}


def render(led: dict) -> str:
    L = [f"# Phase ledger {led['game_id']}", "", f"Checked {led['checked_utc']} (UTC); packet built {led['packet_generated_utc']}. "
         "Research only; projection_ready is false.", ""]
    p15 = led.get("phase15")
    if p15:
        src = ", ".join(f"{t}: {u}" for t, u in (p15.get("source_urls") or {}).items() if u) or p15["source"]
        L += [f"**Phase 15 (official inactives): {p15['status']}**. Source: {src}. Pulled: "
              f"{(p15['pull_utc'] + ' UTC (' + p15['pull_et'] + ')') if p15.get('pull_utc') and p15.get('pull_et') else 'not pulled'}. "
              f"{p15['reason']}", ""]
    L += ["| Phase | Name | Status | Missing / stale / not yet |", "| --- | --- | --- | --- |"]
    for p in led["phases"]:
        why = "; ".join(p["missing"] + p["stale"] + p["not_yet"]) or (", ".join(p["not_available_from_free_sources"]) and
                                                                     "not in free sources: " + ", ".join(p["not_available_from_free_sources"])) or "-"
        L.append(f"| {p['phase']} | {p['name']} | {p['status']} | {why.replace('|', '/')} |")
    L += ["", "| Source | Freshness | Reason |", "| --- | --- | --- |"]
    L += [f"| {r['source']} | {r['status']} | {r['reason'].replace('|', '/')} |" for r in led["freshness"]]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--game", required=True)
    ap.add_argument("--packet", type=Path, help="packet.json path (default pregame/packets/<game>/packet.json)")
    ap.add_argument("--phase", type=int, action="append", choices=sorted(PHASES))
    ap.add_argument("--write", action="store_true", help="write pipeline/ledgers/<game>.json and .md")
    ap.add_argument("--strict", action="store_true", help="exit 3 if any selected phase is MISSING, STALE or NOT_YET")
    a = ap.parse_args(argv)
    try:
        pk = load_packet(a.game, a.packet)
    except (OSError, ValueError) as e:
        print(f"phases: MISSING packet for {a.game}: {e}. Build it with `python -m pregame.build_packets --game {a.game}`.")
        return 2
    led = ledger(pk, phases=a.phase)
    print(render(led))
    if a.write:
        LEDGERS.mkdir(parents=True, exist_ok=True)
        (LEDGERS / f"{a.game}.json").write_text(json.dumps(led, indent=1) + "\n")
        (LEDGERS / f"{a.game}.md").write_text(render(led))
    if a.strict and any(p["status"] in BLOCKING for p in led["phases"]):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
