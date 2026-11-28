"""Write one game's matchup research packet.

    python3 -m pipeline.matchup_research --game 2026_12_DEN_PIT --out research/runs/2026-11-27_DEN_PIT_matchup

Research only. projection_ready stays false. No network.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .build import ROOT, build_packet, render_report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", required=True, help="nflverse game_id, e.g. 2026_12_DEN_PIT")
    ap.add_argument("--out", type=Path, help="directory for packet.json and REPORT.md")
    ap.add_argument("--pbp", type=Path, default=None)
    ap.add_argument("--schedule", type=Path, default=None)
    args = ap.parse_args(argv)
    packet = build_packet(args.game, root=ROOT, pbp_path=args.pbp, schedule_path=args.schedule)
    text = json.dumps(packet, indent=1, allow_nan=False) + "\n"
    report = render_report(packet)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "packet.json").write_text(text)
        (args.out / "REPORT.md").write_text(report)
        print(f"wrote {args.out / 'packet.json'}")
    else:
        print(report)
    failed = [r["section"] for r in packet["receipts"] if r["status"] == "FAILED"]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
