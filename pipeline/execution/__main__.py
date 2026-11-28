"""One game, one run id, immutable phase execution receipts.

    python -m pipeline.execution --game 2026_10_WAS_NYG --run-id run-1 --receipt-dir pipeline/execution_receipts --strict

Research only. Does not call pipeline.sim100k, does not write a database, and does not set projection_ready.
Exit 2 when the packet cannot be read. Exit 3 with --strict when the run is not accepted.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .runner import run_game, summary_text
from .store import ReceiptStore

ROOT = Path(__file__).resolve().parents[2]
PACKETS = ROOT / "pregame" / "packets"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write phase execution receipts for one game.")
    parser.add_argument("--game", required=True)
    parser.add_argument("--packet", type=Path, help="packet.json (default pregame/packets/<game>/packet.json)")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--receipt-dir", type=Path, required=True)
    parser.add_argument("--code-revision", default="UNKNOWN")
    parser.add_argument("--phase", type=int, action="append")
    parser.add_argument("--freshness-json", type=Path, help="JSON list of freshness rows; otherwise the NFL-56 checker runs")
    parser.add_argument("--skip-task", action="append", default=[])
    parser.add_argument("--discover-only", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    path = args.packet or (PACKETS / args.game / "packet.json")
    try:
        packet = json.loads(Path(path).read_text())
    except (OSError, ValueError) as exc:
        print(f"execution: MISSING packet for {args.game}: {exc}")
        return 2
    game_id = (packet.get("game") or {}).get("game_id")
    if game_id != args.game:
        print(f"execution: WRONG_GAME packet says {game_id!r}, argument says {args.game!r}")
        return 3
    if args.freshness_json:
        try:
            freshness_rows = json.loads(args.freshness_json.read_text())
        except (OSError, ValueError) as exc:
            print(f"execution: MALFORMED freshness file: {exc}")
            return 2
    elif args.discover_only:
        freshness_rows = None
    else:
        from pipeline import freshness
        freshness_rows = freshness.check(packet)
    result = run_game(
        packet, run_id=args.run_id, store=ReceiptStore(args.receipt_dir), freshness_rows=freshness_rows,
        code_revision=args.code_revision, phases=args.phase, skip_tasks=set(args.skip_task),
        discover_only=args.discover_only,
    )
    print(summary_text(result))
    print(f"execution: {result['status']} accepted={result['accepted']} projection_ready=false")
    # Exit 0 only when every selected phase passed. --strict remains accepted and changes nothing.
    if result["accepted"]:
        return 0
    return 3


if __name__ == "__main__":
    sys.exit(main())
