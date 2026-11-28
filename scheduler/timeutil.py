"""UTC instants and America/New_York kickoff parsing.

Every stored timestamp is a UTC instant rendered as YYYY-MM-DDTHH:MM:SSZ so
text comparison matches chronological order. Local kickoff strings use the
zone the NFL publishes (Eastern). Ambiguous DST times are rejected unless the
caller passes fold explicitly; times that do not exist (the spring-forward
gap) are always rejected.
"""
from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")


class ScheduleError(ValueError):
    """A kickoff or schedule row cannot be turned into a UTC instant."""


def utc_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        raise ScheduleError("refusing a naive datetime; pass an aware instant")
    rounded = dt.astimezone(timezone.utc).replace(microsecond=0)
    return rounded.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_utc_iso(value: str) -> datetime:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ScheduleError(f"not a UTC instant: {value}") from exc
    return parsed.replace(tzinfo=timezone.utc)


def _has_numeric_offset(value: str) -> bool:
    if len(value) < 6 or value[-3] != ":":
        return False
    return value[-6] in "+-" and value[-5:-3].isdigit() and value[-2:].isdigit()


def _ambiguous(naive: datetime, zone: ZoneInfo) -> bool:
    earlier = naive.replace(tzinfo=zone, fold=0).utcoffset()
    later = naive.replace(tzinfo=zone, fold=1).utcoffset()
    return earlier != later


def _missing(naive: datetime, zone: ZoneInfo) -> bool:
    """True when the wall time falls in a DST gap and both folds normalize away."""
    for fold in (0, 1):
        aware = naive.replace(tzinfo=zone, fold=fold)
        back = aware.astimezone(timezone.utc).astimezone(zone)
        if back.replace(tzinfo=None) == naive and back.fold == fold:
            return False
    return True


def parse_kickoff(value: str, *, tz: str = "America/New_York", fold: int | None = None) -> datetime:
    """Return a UTC instant for an ISO kickoff.

    An offset or Z suffix is used as given. A naive value is read in `tz`.
    """
    raw = str(value).strip()
    if not raw:
        raise ScheduleError("kickoff is empty")
    if raw.endswith("Z") or _has_numeric_offset(raw):
        try:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ScheduleError(f"kickoff is not ISO: {value}") from exc
        if parsed.tzinfo is None:
            raise ScheduleError(f"kickoff lost its offset: {value}")
        return parsed.astimezone(timezone.utc)
    try:
        naive = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ScheduleError(f"kickoff is not ISO: {value}") from exc
    if naive.tzinfo is not None:
        return naive.astimezone(timezone.utc)
    try:
        zone = ZoneInfo(tz)
    except Exception as exc:
        raise ScheduleError(f"unknown timezone {tz}") from exc
    if _missing(naive, zone):
        raise ScheduleError(f"{raw} does not exist in {tz} (DST gap)")
    if _ambiguous(naive, zone) and fold is None:
        raise ScheduleError(f"{raw} is ambiguous in {tz}; pass fold=0 (first) or fold=1 (second)")
    use_fold = 0 if fold is None else int(fold)
    if use_fold not in (0, 1):
        raise ScheduleError("fold must be 0 or 1")
    aware = naive.replace(tzinfo=zone, fold=use_fold)
    return aware.astimezone(timezone.utc)
