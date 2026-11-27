"""python -m pipeline.read_rules --game 2026_13_JAX_CHI [--as-of-week 13] [--offline] [--out DIR]

Writes READ_RULES_<game>.md/.json. FLAGS ONLY; research only; projection_ready stays false."""
from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.read_rules import assert_flags_only
from pipeline.read_rules.flags import game_report, write_report
from pipeline.read_rules.common import ROOT


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.read_rules")
    ap.add_argument("--game", required=True)
    ap.add_argument("--as-of-week", type=int)
    ap.add_argument("--offline", action="store_true", help="skip NWS/Open-Meteo pulls (weather = unknown)")
    ap.add_argument("--pbp")
    ap.add_argument("--out", default=str(ROOT / "pipeline/ledgers/read_rules"))
    a = ap.parse_args(argv)
    assert_flags_only()
    rep = game_report(a.game, a.as_of_week, offline=a.offline, pbp_path=a.pbp)
    j, m = write_report(rep, Path(a.out))
    print(m)
    print(j)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
