"""Rico's three Week 13 read rules (approved Nov 26, 2026, 7:11 PM ET): FLAGS ONLY.

    1. targets_first    - WR/TE receiving legs need a real target share (WR >= 20% of team targets, TE top-two).
    2. defense_allowed  - what each defense allows (coverage shell, DBs, by role, by depth, run YPC), both sides.
    3. weather_grade    - hourly NWS + Open-Meteo rain-rate grade, sustained wind and gusts, run-tilt read.

None of these may cut, remove or downgrade a leg. `CUTS_ENABLED` is False for every rule and `annotate_legs`
only ADDS columns. Turning any rule into a cut needs a backtest that beats the rushing-under baseline AND Rico's
OK in a separate change. Missing data is "unknown", never zero. Research only; projection_ready stays false.
"""
from __future__ import annotations

RULES = ("targets_first", "defense_allowed", "weather_grade")
CUTS_ENABLED = {r: False for r in RULES}
PROJECTION_READY = False
UNKNOWN = "unknown"
APPROVED = "Rico, Nov 26 2026 7:11 PM ET (card answered via Ghost6, t1189u)"
STARTS_WEEK = 13


def assert_flags_only() -> None:
    """Raise if any rule has been switched to a cut. Called by every entry point."""
    bad = [r for r, on in CUTS_ENABLED.items() if on]
    if bad:
        raise RuntimeError(f"read rules are flags only until a backtest beats the rushing-under baseline: {bad}")
    if PROJECTION_READY:
        raise RuntimeError("projection_ready must stay False")
