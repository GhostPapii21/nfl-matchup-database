"""Timestamped price freeze for one game, on the same pull path as the packets (research only).

All fetching, de-vig, same-line consensus, player matching, the credit floor and the freeze format live in
pregame/odds.py; this file is only a command line around them, for freezes between scheduled packet runs.
The player list comes from the game's pregame packet (pregame/packets/<game_id>/packet.json): props are matched on
full name + team and fail closed on any ambiguity. Passing yards are kept as reference fields flagged never-a-leg.

    python -m pregame.multibook --game 2026_10_WAS_NYG                      # game lines (3) + props (7): <= 10 credits
    python -m pregame.multibook --game 2026_10_WAS_NYG --dry-run            # free balance read + cost plan, no paid call
    python -m pregame.multibook --game 2026_10_WAS_NYG --compare pregame/price_freezes/2026-11-12_WAS@NYG/freeze_20261112T161430Z.json
    python -m pregame.multibook --movement OLD_FREEZE.json NEW_FREEZE.json  # offline, 0 credits
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from pregame import odds as O

ROOT = Path(__file__).resolve().parents[1]


def _print_credits():
    print("multibook: " + O.credit_line())


def freeze_game(game_id, packet_path=None, out=ROOT / "pregame" / "price_freezes", floor=O.DEFAULT_FLOOR, dry_run=False, compare=None):
    _, _, away, home = game_id.split("_")
    pk = json.loads(Path(packet_path or ROOT / "pregame" / "packets" / game_id / "packet.json").read_text())
    roster = O.roster_from_packet(pk)
    key = os.environ.get("ODDS_API_KEY", "").strip()
    if not key:
        return {"status": "NO_KEY: ODDS_API_KEY not set; no prices"}
    if dry_run:
        bal = O.read_balance(key)
        plan = []
        for what, n in (("game_lines", len(O.GAME_MARKETS)), ("props", len(O.PROP_MARKETS))):
            est = O.estimate_cost(n)
            ok, why = O.floor_check(bal, est, floor)
            plan.append({"call": what, "estimate_credits": est, "decision": why})
            bal = bal - est if (ok and bal is not None) else bal
        return {"status": "DRY_RUN", "balance_now": O.QUOTA.get("credits_remaining"), "plan": plan, "max_total_credits": sum(p["estimate_credits"] for p in plan)}
    lines = O.fetch_game_lines(floor=floor)
    ev = lines["events"].get((away, home))
    if not ev:
        return {"status": f"NO_GAME_LINES: {lines['status']}"}
    pr = O.fetch_props(ev["id"], floor=floor)
    full = dict(ev, bookmakers=ev.get("bookmakers", []) + ((pr.get("event") or {}).get("bookmakers", [])))
    mk = O.summarize_event(full, home, away)
    cons = O.consensus(mk, roster)
    meta = {"lines_status": lines["status"], "lines_retrieved_utc": lines.get("retrieved_utc"), "props_status": pr["status"],
            "props_retrieved_utc": pr.get("retrieved_utc"), "event_id": ev["id"], "commence_utc": ev.get("commence_time"),
            "roster_source": f"pregame/packets/{game_id}/packet.json generated {pk.get('generated_utc')} UTC",
            "pre_inactives": True}
    if compare:
        meta["movement_vs"] = str(compare)
        meta["movement"] = O.movement_vs_freeze(mk, json.loads(Path(compare).read_text()))
    m = O.write_freeze(game_id, away, home, mk, cons, {"game_lines": ev, "props": pr.get("event")}, out, meta=meta)
    m["status"] = "OK" if pr["status"] == "OK" else f"PARTIAL: props {pr['status']}"
    return m


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--game", help="nflverse game_id, e.g. 2026_10_WAS_NYG")
    ap.add_argument("--packet", help="packet.json for the roster (default pregame/packets/<game>/packet.json)")
    ap.add_argument("--out", default=str(ROOT / "pregame" / "price_freezes"))
    ap.add_argument("--floor", type=int, default=O.DEFAULT_FLOOR)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--compare", help="earlier freeze_*.json to report movement against (no extra credits)")
    ap.add_argument("--movement", nargs=2, metavar=("OLD", "NEW"), help="offline movement between two freezes (0 credits)")
    a = ap.parse_args(argv)
    if a.movement:
        old, new = (json.loads(Path(p).read_text()) for p in a.movement)
        print(json.dumps(O.movement_vs_freeze(new["markets"], old), indent=1))
        print("multibook: odds credits used this run=0 remaining=unknown (no API call made)")
        return 0
    if not a.game:
        ap.error("--game is required")
    m = freeze_game(a.game, a.packet, a.out, a.floor, a.dry_run, a.compare)
    print(json.dumps({k: v for k, v in m.items() if k not in ("movement",)}, indent=1, default=str))
    _print_credits()
    return 0 if m["status"] in ("OK", "DRY_RUN") else 2


if __name__ == "__main__":
    sys.exit(main())
