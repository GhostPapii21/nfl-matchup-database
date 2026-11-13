"""NFL-75 Phase 2: Weeks 10-12 holdout grading entry point for the opportunity model. NOT RUN in PR #38.

    python3 -m calibration.opportunity_holdout_grade --week 10 --actual-pbp <path to nflverse PBP with that week>

The very first thing it does is calibration.opportunity_freeze.check_freeze(week): it refuses unless the committed
freeze manifest exists and the model code + frozen params match it byte for byte. Only after that check passes does it
touch the actual-results file (which is not in the repo). Research only. projection_ready stays false."""
from __future__ import annotations
import argparse

from calibration.opportunity_freeze import check_freeze, FreezeError, HOLDOUT_WEEKS


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--actual-pbp", required=True)
    a = ap.parse_args(argv)
    if a.week not in HOLDOUT_WEEKS:
        raise SystemExit(f"holdout grading covers weeks {HOLDOUT_WEEKS} only")
    try:
        m = check_freeze(a.week)  # BEFORE any actual is read
    except FreezeError as e:
        raise SystemExit(f"REFUSED: {e}")
    raise SystemExit(f"freeze verified ({m['model_commit'][:7]}); holdout grading itself is a separate, approved "
                     f"step (Rico's readiness bar) and is not implemented in PR #38")


if __name__ == "__main__":
    main()
