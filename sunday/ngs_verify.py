"""Read the local public NGS files and report what they actually cover.

A week that is absent stays absent. Route and defender fields are not in these
weekly files. There is no publisher as-of stamp in the CSV, so the file time
is not treated as proof the feed is current.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

FILES = {
    "passing": "data/ngs/nflverse_ngs_raw/ngs_passing.csv.gz",
    "receiving": "data/ngs/nflverse_ngs_raw/ngs_receiving.csv.gz",
    "rushing": "data/ngs/nflverse_ngs_raw/ngs_rushing.csv.gz",
}
TOUCHDOWNS = {
    "passing": "pass_touchdowns",
    "receiving": "rec_touchdowns",
    "rushing": "rush_touchdowns",
}
ABSENT_FIELDS = (
    "route",
    "defender",
    "coverage_assignment",
)


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(repo: Path) -> dict:
    feeds = {}
    for name, rel in FILES.items():
        path = repo / rel
        if not path.is_file():
            feeds[name] = {"status": "UNAVAILABLE", "path": rel, "rows": 0}
            continue
        frame = pd.read_csv(path)
        season = frame[frame["season"] == 2026] if "season" in frame.columns else frame.iloc[0:0]
        weeks = sorted(int(w) for w in season["week"].dropna().unique()) if "week" in season.columns else []
        regular = [w for w in weeks if w > 0]
        td_col = TOUCHDOWNS[name]
        feeds[name] = {
            "status": "READ",
            "path": rel,
            "sha256": _sha(path),
            "rows": int(len(frame)),
            "rows_2026": int(len(season)),
            "weeks_2026": regular,
            "max_week_2026": regular[-1] if regular else None,
            "week_12_rows": int((season["week"] == 12).sum()) if "week" in season.columns else 0,
            "touchdown_column": td_col if td_col in frame.columns else None,
            "publisher_as_of": None,
            "fields_absent": [field for field in ABSENT_FIELDS if field not in frame.columns],
        }
    max_week = feeds.get("passing", {}).get("max_week_2026")
    aggregate_usable = all(feed.get("status") == "READ" and feed.get("rows_2026", 0) > 0 for feed in feeds.values())
    missing_details = sorted({field for feed in feeds.values() for field in feed.get("fields_absent", [])})
    return {
        "schema": "ngs-verification/1",
        "projection_ready": False,
        "certification": False,
        "aggregate_usable": aggregate_usable,
        "chart_images_required_for_aggregates": False,
        "unavailable_play_level_fields": missing_details,
        "feeds": feeds,
        "week_12": "unavailable" if not any((feeds[name].get("week_12_rows") or 0) > 0 for name in feeds) else "present",
        "current_for_week_12": False,
        "reason": (
            f"Aggregate NGS 2026 passing coverage ends at week {max_week}. "
            "Chart images are not required to use uploaded passing/receiving/rushing aggregates. "
            "Week 12 player results are not expected before the games. "
            "Missing publisher as-of and play-level route/defender evidence remain explicit limitations."
        ),
    }
