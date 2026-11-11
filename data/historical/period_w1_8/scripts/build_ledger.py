#!/usr/bin/env python3
"""Build the isolated 2026 W1–8 research ledger; never synthesize source data."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "nflverse_pbp+schedules"
PERIODS = ("Q1", "Q2", "Q3", "Q4", "H1", "H2", "REG", "OT")
QUOTES = ("home_moneyline", "away_moneyline", "spread_line", "home_spread_odds",
          "away_spread_odds", "total_line", "over_odds", "under_odds")
URLS = {
    "schedules": "https://github.com/nflverse/nflverse-data/releases/download/schedules/games.parquet",
    "pbp": "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet",
}
GAME_FIELDS = ["game_id", "season", "week", "gameday", "kickoff", "home", "away",
               "home_score", "away_score", "overtime"] + [
    f"{p.lower()}_{side}" for p in PERIODS for side in ("home", "away")
] + ["winner", "tie", "source", "pull_utc"]
PERIOD_FIELDS = ["game_id", "period", "home_pts", "away_pts", "cumulative_home",
                 "cumulative_away", "period_winner", "source", "status", "missing_reason", "pull_utc"]
LEDGER_FIELDS = ["game_id", "season", "week", "home", "away", "source", "schedule_source",
                 "pbp_source", "pull_utc", "scoreboard_status", "period_missing_reason",
                 "missing_periods", "overtime", "ot_status", "tie", "tie_status",
                 "source_identity_status", "pff_overview", "pff_source", "pff_attempt_status",
                 "market_spread_grade", "spread_result_home", "market_total_grade", "total_result",
                 "quote_source", "quote_timestamp", "quote_verified_closer", "quote_limitation",
                 "market_missing_reason"] + list(QUOTES) + [f"{p.lower()}_status" for p in PERIODS]


def number(value):
    try:
        n = float(value)
        return n if math.isfinite(n) else None
    except (TypeError, ValueError):
        return None


def integer(value):
    n = number(value)
    return int(n) if n is not None and n == int(n) else None


def flag(value):
    n = integer(value)
    return bool(n) if n in (0, 1) else None


def winner(home_pts, away_pts, home, away):
    if home_pts is None or away_pts is None:
        return None
    return home if home_pts > away_pts else away if away_pts > home_pts else "TIE"


def in_scope(row):
    return integer(row.get("season")) == 2026 and integer(row.get("week")) in range(1, 9) and row.get("game_type") == "REG"


def completed(row, as_of):
    day = str(row.get("gameday", ""))[:10]
    return (in_scope(row) and bool(day) and day <= as_of.astimezone(ZoneInfo("America/New_York")).date().isoformat()
            and all(integer(row.get(k)) is not None and integer(row[k]) >= 0 for k in ("home_score", "away_score")))


def reconstruct(schedule, plays):
    """Difference verified quarter endpoints, ignoring stale non-scoring rows."""
    declared_ot = flag(schedule.get("overtime"))
    observed_ot = any((integer(p.get("qtr")) or 0) > 4 for p in plays)
    overtime = True if observed_ot else declared_ot
    def missing(reason):
        return {}, overtime, reason
    if not plays:
        return missing("NO_PBP")
    if any(p.get("home_team") != schedule["home_team"] or p.get("away_team") != schedule["away_team"]
           or integer(p.get("season")) != 2026 or integer(p.get("week")) != integer(schedule["week"])
           for p in plays):
        return missing("PBP_IDENTITY_MISMATCH")
    if declared_ot is False and observed_ot:
        return missing("OVERTIME_CONFLICT")
    rows = []
    seen = {}
    for p in plays:
        q, pid = integer(p.get("qtr")), number(p.get("play_id"))
        h, a = integer(p.get("total_home_score")), integer(p.get("total_away_score"))
        if q is None or q < 1 or pid is None or h is None or a is None:
            continue
        signature = (q, h, a, flag(p.get("quarter_end")), flag(p.get("game_end")), p.get("desc"))
        if pid in seen and seen[pid] != signature:
            return missing("CONFLICTING_DUPLICATE_PLAY")
        seen[pid] = signature
        rows.append((pid, q, h, a, p))
    rows.sort(key=lambda r: r[0])
    if not rows or not end_game(rows[-1][4]):
        return missing("NO_SCORED_GAME_END")
    if (rows[-1][2], rows[-1][3]) != (integer(schedule["home_score"]), integer(schedule["away_score"])):
        return missing("FINAL_SCORE_MISMATCH")
    previous = (0, 0)
    previous_q = 1
    grouped = defaultdict(list)
    for _, q, h, a, p in rows:
        if q < previous_q:
            # A delayed boundary may follow a play from the next quarter. It
            # must corroborate the score already observed in its own quarter.
            if end_quarter(p) and grouped[q] and (h, a) == grouped[q][-1][:2]:
                grouped[q].append((h, a, p))
                continue
            if stale_non_scoring_row(p) and h <= previous[0] and a <= previous[1]:
                continue
            return missing("NONMONOTONIC_SCORE_OR_QUARTER")
        if h < previous[0] or a < previous[1]:
            # Never infer scoring from these rows, including a mixed update
            # where one side regresses and the other increases.
            if stale_non_scoring_row(p) and h <= previous[0] and a <= previous[1]:
                continue
            return missing("NONMONOTONIC_SCORE_OR_QUARTER")
        previous, previous_q = (h, a), q
        grouped[q].append((h, a, p))
    if any(q not in grouped for q in range(1, 5)):
        return missing("MISSING_REGULATION_QUARTER")
    if any(not end_quarter(grouped[q][-1][2]) for q in range(1, 4)):
        return missing("MISSING_QUARTER_END_MARKER")
    if observed_ot and not end_quarter(grouped[4][-1][2]):
        return missing("MISSING_REGULATION_END_MARKER")
    if declared_ot is True and not observed_ot:
        return missing("MISSING_OT_PBP")
    overtime = observed_ot
    endpoints = {q: grouped[q][-1][:2] for q in range(1, 5)}
    pts = {}
    previous = (0, 0)
    for q in range(1, 5):
        end = endpoints[q]
        pts[f"Q{q}"] = tuple(end[i] - previous[i] for i in (0, 1))
        previous = end
    pts["H1"] = endpoints[2]
    pts["H2"] = tuple(endpoints[4][i] - endpoints[2][i] for i in (0, 1))
    pts["REG"] = endpoints[4]
    pts["OT"] = tuple(rows[-1][i + 2] - endpoints[4][i] for i in (0, 1))
    return pts, overtime, ""


def end_game(row):
    return flag(row.get("game_end")) is True or bool(re.search(r"\bEND (?:OF )?(?:GAME|OVERTIME)\b", str(row.get("desc", "")).upper()))


def end_quarter(row):
    return (flag(row.get("quarter_end")) is True or end_game(row)
            or bool(re.search(r"\bEND (?:OF )?(?:QUARTER|HALF)\b", str(row.get("desc", "")).upper())))


def stale_non_scoring_row(row):
    """Narrow description allowlist; scoring plays and endpoints stay strict."""
    if end_quarter(row):
        return False
    desc = str(row.get("desc", "")).upper().strip()
    return (bool(re.match(r"TIMEOUT\b", desc))
            or desc == "THE STATUS OF THE GAME CLOCK WAS ASSISTED BY REPLAY."
            or bool(re.search(r"\bNO PLAY\b", desc))
            or ("INJURY UPDATE:" in desc and "PASS INCOMPLETE" in desc))


def market(row, retained):
    result = {k: number(row.get(k)) for k in QUOTES}
    result.update(market_spread_grade="NOLINE", spread_result_home=None,
                  market_total_grade="NOLINE", total_result=None,
                  quote_source=URLS["schedules"] if retained else "",
                  quote_timestamp="", quote_verified_closer=False,
                  quote_limitation="Retained nflverse schedule values; NOT verified closing lines; quote time and sportsbook unverified.",
                  market_missing_reason="NO_VERIFIED_CLOSER_QUOTE")
    return result


def build_rows(schedules, pbp, pull_utc, as_of, retained=False):
    expected = [s for s in schedules if completed(s, as_of)]
    ids = [s["game_id"] for s in expected]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate schedule game_id")
    by_game = defaultdict(list)
    id_set = set(ids)
    for p in pbp:
        if p.get("game_id") in id_set:
            by_game[p["game_id"]].append(p)
    games, periods, ledger = [], [], []
    for s in sorted(expected, key=lambda x: (integer(x["week"]), str(x["gameday"]), x["game_id"])):
        gid, home, away = s["game_id"], s["home_team"], s["away_team"]
        pts, overtime, reason = reconstruct(s, by_game[gid])
        hs, aws = integer(s["home_score"]), integer(s["away_score"])
        kickoff = ""
        if s.get("gametime"):
            kickoff = datetime.fromisoformat(f"{str(s['gameday'])[:10]}T{s['gametime']}").replace(tzinfo=ZoneInfo("America/New_York")).isoformat()
        g = dict(game_id=gid, season=2026, week=integer(s["week"]), gameday=str(s["gameday"])[:10],
                 kickoff=kickoff, home=home, away=away, home_score=hs, away_score=aws, overtime=overtime,
                 winner=winner(hs, aws, home, away), tie=hs == aws, source=SOURCE, pull_utc=pull_utc)
        for p in PERIODS:
            pair = pts.get(p, (None, None))
            for i, side in enumerate(("home", "away")):
                g[f"{p.lower()}_{side}"] = pair[i]
            end_q = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4, "H1": 2, "H2": 4, "REG": 4}.get(p)
            cumulative = ((hs, aws) if p == "OT" else tuple(sum(pts[f"Q{q}"][i] for q in range(1, end_q + 1)) for i in (0, 1))) if pts else (None, None)
            periods.append(dict(game_id=gid, period=p, home_pts=pair[0], away_pts=pair[1],
                                cumulative_home=cumulative[0], cumulative_away=cumulative[1],
                                period_winner=winner(*pair, home, away), source=SOURCE,
                                status="PRESENT" if pts else "MISSING", missing_reason=reason, pull_utc=pull_utc))
        games.append(g)
        l = dict(game_id=gid, season=2026, week=g["week"], home=home, away=away, source=SOURCE,
                 schedule_source=URLS["schedules"], pbp_source=URLS["pbp"], pull_utc=pull_utc,
                 scoreboard_status="PRESENT" if pts else "MISSING", period_missing_reason=reason,
                 missing_periods="" if pts else ";".join(PERIODS), overtime=overtime,
                 ot_status="PRESENT" if overtime is not None else "MISSING", tie=hs == aws, tie_status="PRESENT",
                 source_identity_status="MISMATCH" if reason == "PBP_IDENTITY_MISMATCH" else "PRESENT" if by_game[gid] else "MISSING_PBP",
                 pff_overview="MISSING", pff_source="", pff_attempt_status="NOT_ATTEMPTED")
        l.update(market(s, retained))
        l.update({f"{p.lower()}_status": "PRESENT" if pts else "MISSING" for p in PERIODS})
        ledger.append(l)
    return games, periods, ledger


def write_csv(path, rows, fields):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def acquire(as_of, offline=False):
    import polars as pl
    raw = ROOT / "data/raw"
    manifest_path = raw / "manifest.json"
    if offline:
        m = json.loads(manifest_path.read_text())
        if m.get("status") != "FETCHED" or m.get("season") != 2026 or m.get("weeks") != [1, 8]:
            raise ValueError("Offline replay requires a fetched 2026 W1–8 manifest")
        frames = {}
        for name in ("schedules", "pbp"):
            item = m["fetches"][name]
            if item["status"] != "OK":
                raise ValueError(f"Offline {name} snapshot unavailable")
            path = raw / item["file"]
            if path.parent != raw or digest(path) != item["sha256"]:
                raise ValueError(f"Offline {name} snapshot checksum/path mismatch")
            frames[name] = pl.read_parquet(path)
        return frames, m
    os.environ["NFLREADPY_CACHE"] = "off"
    os.environ["NFLREADPY_CACHE_DIR"] = str(raw / "cache")
    import nflreadpy as nfl
    from nflreadpy.config import update_config
    update_config(cache_mode="off", cache_dir=raw / "cache", timeout=30)
    m = dict(status="FETCHED", season=2026, weeks=[1, 8], pull_utc=datetime.now(timezone.utc).isoformat(),
             as_of_utc=as_of.isoformat(), nflreadpy_version=version("nflreadpy"), fetches={})
    frames = {}
    for name, fn in (("schedules", lambda: nfl.load_schedules(2026)), ("pbp", lambda: nfl.load_pbp(2026))):
        item = {"url": URLS[name], "attempt_utc": datetime.now(timezone.utc).isoformat()}
        try:
            df = fn()
            df = df.filter((pl.col("season") == 2026) & pl.col("week").is_between(1, 8))
            if name == "schedules":
                df = df.filter(pl.col("game_type") == "REG")
            else:
                # Retain only columns needed for reproducible scoreboard reconstruction.
                cols = ["game_id", "season", "week", "home_team", "away_team", "play_id", "qtr",
                        "total_home_score", "total_away_score", "quarter_end", "game_end", "desc"]
                df = df.select([c for c in cols if c in df.columns])
            path = raw / f"{name}_2026_w1_8.parquet"
            df.write_parquet(path)
            item.update(status="OK", file=path.name, sha256=digest(path), rows=df.height)
            frames[name] = df
        except Exception as e:
            item.update(status="ERROR", error_type=type(e).__name__, error=str(e))
            m["status"] = "FETCH_FAILED"
        m["fetches"][name] = item
    manifest_path.write_text(json.dumps(m, indent=2) + "\n")
    return frames, m


def publish(frames, manifest, as_of):
    schedules = frames["schedules"].to_dicts() if "schedules" in frames else []
    pbp = frames["pbp"].to_dicts() if "pbp" in frames else []
    games, periods, ledger = build_rows(schedules, pbp, manifest["pull_utc"], as_of,
                                        retained=manifest["fetches"].get("schedules", {}).get("status") == "OK")
    data = ROOT / "data"
    for name, rows, fields in (("games", games, GAME_FIELDS), ("period_scores", periods, PERIOD_FIELDS),
                               ("coverage_ledger", ledger, LEDGER_FIELDS)):
        write_csv(data / f"{name}_w1_8.csv", rows, fields)
    schedule_known = "schedules" in frames
    expected = sum(completed(s, as_of) for s in schedules) if schedule_known else None
    teams = sorted({g[side] for g in games for side in ("home", "away")})
    missing = sum(l["scoreboard_status"] == "MISSING" for l in ledger)
    status = "COMPLETE" if manifest["status"] == "FETCHED" and games and not missing else "BLOCKED_SOURCE_FETCH" if manifest["status"] != "FETCHED" else "INCOMPLETE_COVERAGE"
    summary = dict(status=status, as_of_utc=as_of.isoformat(), pull_utc=manifest["pull_utc"],
                   expected_completed_games=expected, built_games=len(games), scheduled_w1_8=len(schedules) if schedule_known else None,
                   missing_scoreboard_games=missing, missing_period_panels=sum(p["status"] == "MISSING" for p in periods),
                   missing_pff_overviews=len(ledger), overtime_games=sum(g["overtime"] is True for g in games),
                   unknown_overtime_games=sum(g["overtime"] is None for g in games), ties=sum(g["tie"] for g in games),
                   teams=teams, spread_grades=dict(Counter(l["market_spread_grade"] for l in ledger)),
                   total_grades=dict(Counter(l["market_total_grade"] for l in ledger)),
                   counts_verified=bool(schedule_known and games))
    (data / "build_status.json").write_text(json.dumps(summary, indent=2) + "\n")
    unknown = "UNKNOWN (schedule fetch failed)"
    lines = ["# W1–8 coverage counts", "", f"Build status: **{status}**.", "",
             f"As of UTC: {as_of.isoformat()}. Pull UTC: {manifest['pull_utc']}.", "",
             f"- Completed games expected from schedule: {expected if expected is not None else unknown}.",
             f"- Games built: {len(games)}. Schedule W1–8 rows: {len(schedules) if schedule_known else unknown}.",
             "- The fetched schedule determines the exact count; no task estimate is hard-coded.",
             f"- PRESENT scoreboard games: {len(games) - missing}.",
             f"- Missing scoreboard games / period panels among built games: {missing} / {summary['missing_period_panels']}.",
             f"- Missing PFF overviews among built games: {len(ledger)}; public scraping NOT_ATTEMPTED.",
             f"- OT games: {summary['overtime_games']}; unknown OT: {summary['unknown_overtime_games']}; ties: {summary['ties']}.",
             f"- Teams covered: {len(teams)}/32. All 32 verified: {len(teams) == 32 and summary['counts_verified']}.",
             f"- Teams: {', '.join(teams) or 'UNVERIFIED — no source rows'}.",
             f"- Spread grades: {summary['spread_grades']}; total grades: {summary['total_grades']}.", ""]
    reasons = Counter(l["period_missing_reason"] for l in ledger if l["scoreboard_status"] == "MISSING")
    lines += [f"- Residual scoreboard MISSING reasons: {dict(reasons) or 'none'}.", ""]
    for row in ledger:
        if row["scoreboard_status"] == "MISSING":
            lines.append(f"- {row['game_id']}: `{row['period_missing_reason']}`.")
    if not summary["counts_verified"]:
        lines += ["Empty CSVs are schema-only placeholders. Zero built/OT/PFF counts do not mean zero games or complete coverage.",
                  "Expected missing-game/panel and team counts remain UNKNOWN until schedule data is available.", ""]
    for name, item in manifest["fetches"].items():
        if item["status"] == "ERROR":
            lines += [f"Fetch failure ({name}): `{item.get('error_type')}` — {item.get('error')}", ""]
    lines += ["No PFF evidence was present inside this workspace. W9 JAX@BAL is excluded; no live notes outside the workspace were read.",
              "Market grades are NOLINE: NO_VERIFIED_CLOSER_QUOTE. Retained schedule values are transparency fields only; historic sportsbook and quote time are unverified.", ""]
    (ROOT / "reviews/COUNTS.md").write_text("\n".join(lines))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Replay checksummed snapshots from the last successful fetch")
    parser.add_argument("--as-of", help="Timezone-aware ISO datetime; default: current UTC")
    args = parser.parse_args()
    as_of = datetime.fromisoformat(args.as_of) if args.as_of else datetime.now(timezone.utc)
    if as_of.tzinfo is None:
        parser.error("--as-of requires a timezone")
    for directory in ("data/raw", "reviews"):
        (ROOT / directory).mkdir(parents=True, exist_ok=True)
    frames, manifest = acquire(as_of, args.offline)
    summary = publish(frames, manifest, as_of)
    print(json.dumps(summary, indent=2))
    return 0 if summary["status"] == "COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
