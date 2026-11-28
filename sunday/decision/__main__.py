"""Write the historical DEN@PIT decision board.

    python3 -m sunday.decision
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .historical import ROOT, write_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Historical Sunday decision board")
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "sunday" / "artifacts" / "2026_12_DEN_PIT",
        help="directory for decision_board.json and decision_board.md",
    )
    args = parser.parse_args()
    report = write_report(args.out)
    counts = report["section_counts"]
    print(
        f"wrote {args.out} projection_ready={str(report['projection_ready']).lower()} "
        f"strong={counts['strong_reads']} soft={counts['soft_leans']} "
        f"avoid={counts['avoids']} no_play={counts['no_plays']}"
    )


if __name__ == "__main__":
    main()
