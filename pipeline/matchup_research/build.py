"""Fan existing matchup research into one per-game packet.

Calls the modules already on main. Does not rebuild the models that live on
open PRs #140 (defense-allowed flags), #143 (defender coverage profiles), or
#144 (positional allowances). When those outputs or importable entrypoints are
present they are read; otherwise the field is unavailable.

Historical replays keep only plays from weeks before the game. Published Sharp
and StatRankings tables are separate charting sources and are not averaged.
projection_ready stays false.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import math
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PBP_REL = "data/historical/nflverse/pbp_2026_w1_11_pulled_20261124T1717ET.parquet"
SCHEDULE_REL = "data/historical/nflverse/games.csv"
DEPTH_REL = "data/historical/nflverse/depth_charts_2026.parquet"
COVERAGE_PULL_REL = "research/game_logs_2026_w11/sources/team_coverage_rates.csv"
SCHEMA = "matchup-research/1"

DB_SLOTS = {"LCB", "RCB", "CB", "NB", "SS", "FS", "S"}
OL_SLOTS = {"LT", "LG", "C", "RG", "RT"}
DL_SLOTS = {"LDE", "LDT", "RDE", "RDT", "NT"}
SHELLS = ("cover0_pct", "cover1_pct", "cover2_pct", "cover2m_pct", "cover3_pct", "cover4_pct", "cover6_pct", "cover9_pct")
SCHEDULE_COLS = [
    "game_id", "season", "game_type", "week", "gameday", "weekday", "gametime",
    "away_team", "home_team", "away_score", "home_score", "location", "roof", "surface",
    "temp", "wind", "away_rest", "home_rest", "away_coach", "home_coach", "stadium",
]
PBP_EXTRA = [
    "qb_hit", "qb_dropback", "epa", "pass_location", "pass_length", "air_yards", "no_huddle",
    "pass_attempt", "receiving_yards", "success", "game_seconds_remaining",
    "pass_defense_1_player_name", "pass_defense_2_player_name", "interception_player_name",
    "penalty_player_name", "penalty_type", "penalty_team", "interception",
]


def _rel(path, root: Path = ROOT) -> str:
    try:
        return str(Path(path).resolve().relative_to(Path(root).resolve()))
    except ValueError:
        return str(path)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _num(value):
    if value is None or (isinstance(value, float) and value != value):
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    return value


def json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    if isinstance(obj, Path):
        return str(obj)
    if hasattr(obj, "item") and not isinstance(obj, (str, bytes, dict)):
        try:
            return json_safe(obj.item())
        except Exception:
            return str(obj)
    if isinstance(obj, float) and (obj != obj or obj in (float("inf"), float("-inf"))):
        return None
    return obj


def fact(value, *, kind, source, as_of, numerator=None, denominator=None, sample_size=None,
         definition=None, reason=None, unit=None):
    """One profile figure. kind is measured, estimate, or unavailable. Unknown is never stored as zero."""
    unavailable = kind == "unavailable"
    return {
        "kind": kind,
        "value": "unknown" if unavailable else value,
        "unavailable": unavailable,
        "numerator": numerator,
        "denominator": denominator,
        "sample_size": sample_size if sample_size is not None else denominator,
        "unit": unit,
        "definition": definition,
        "reason": reason,
        "as_of": as_of,
        "source": source,
    }


def _blank(value) -> bool:
    return value is None or (isinstance(value, str) and value.strip() in ("", "None", "nan"))


def _published_number(text):
    if _blank(text):
        return None
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def _scheme():
    path = ROOT / "data" / "scheme_profiles" / "build_profiles.py"
    spec = importlib.util.spec_from_file_location("scheme_build_profiles", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _is_metric(obj) -> bool:
    return isinstance(obj, dict) and (obj.get("kind") in {"count", "rate", "rate_difference"} or obj.get("status") == "BLOCKED")


def short_source(scan: dict) -> dict:
    """Provenance for one figure. Game ids stay on the team scan, not on every rate."""
    keep = ("module", "file", "sha256", "as_of", "url", "pulled_utc", "source_updated", "source_url", "source_type", "pull_time", "weeks", "note", "method", "pr")
    return {k: scan[k] for k in keep if scan.get(k) not in (None, "")}


def _regulation(plays: pd.DataFrame) -> pd.DataFrame:
    """Same regulation cut as scheme aggregate_side: quarters 1-4."""
    if plays.empty or "qtr" not in plays.columns:
        return plays
    quarter = pd.to_numeric(plays["qtr"], errors="coerce")
    return plays[quarter <= 4]


def scheme_fact(metric: dict, scan: dict) -> dict:
    """Re-label a scheme-profile metric with the file this replay actually scanned.

    The scheme module stamps its pinned November 2025/2026 release constants on every
    metric. Those constants describe that builder's pinned file, not this scan, so the
    packet keeps the definition and the counts and records the scan file separately.
    """
    if metric.get("status") == "BLOCKED" or metric.get("observed") is False:
        return fact(
            "unknown", kind="unavailable", source=short_source(scan), as_of=scan.get("as_of"),
            numerator=metric.get("numerator"), denominator=metric.get("denominator"),
            definition=metric.get("definition") or metric.get("reason"),
            reason=metric.get("reason") or "not observed",
        )
    kind = "measured"
    return fact(
        metric.get("value"), kind=kind, source=short_source(scan), as_of=scan.get("as_of"),
        numerator=metric.get("numerator"), denominator=metric.get("denominator"),
        sample_size=metric.get("denominator") if metric.get("kind") == "rate" else metric.get("numerator"),
        definition=metric.get("definition"), unit="share" if metric.get("kind") == "rate" else "count",
    )


def annotate(obj, scan):
    if _is_metric(obj):
        return scheme_fact(obj, scan)
    if isinstance(obj, dict):
        return {k: annotate(v, scan) for k, v in obj.items()}
    if isinstance(obj, list):
        return [annotate(v, scan) for v in obj]
    return obj


def _rate(numer, denom, *, source, as_of, definition, unit="share"):
    numer = int(numer)
    denom = int(denom)
    if denom <= 0:
        return fact("unknown", kind="unavailable", source=source, as_of=as_of, numerator=numer, denominator=denom,
                    definition=definition, reason="denominator is zero; the rate is unknown, not zero", unit=unit)
    return fact(round(numer / denom, 6), kind="measured", source=source, as_of=as_of, numerator=numer,
                denominator=denom, definition=definition, unit=unit)


def _mean(series, *, source, as_of, definition, unit):
    known = pd.to_numeric(series, errors="coerce").dropna()
    if known.empty:
        return fact("unknown", kind="unavailable", source=source, as_of=as_of, numerator=None, denominator=0,
                    definition=definition, reason="no non-null observations", unit=unit)
    return fact(round(float(known.mean()), 6), kind="measured", source=source, as_of=as_of,
                numerator=None, denominator=int(len(known)), sample_size=int(len(known)),
                definition=definition, unit=unit)


def load_schedule(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, usecols=lambda c: c in SCHEDULE_COLS)
    return frame


def game_row(schedule: pd.DataFrame, game_id: str) -> dict:
    hit = schedule[schedule["game_id"] == game_id]
    if hit.empty:
        raise SystemExit(f"game_id {game_id} is not in the schedule")
    r = hit.iloc[0]
    scores = _num(r.get("away_score")) is not None and _num(r.get("home_score")) is not None
    return {
        "game_id": str(r.game_id),
        "season": int(r.season),
        "week": int(r.week),
        "game_type": str(r.game_type),
        "gameday": str(r.gameday),
        "weekday": None if _blank(r.get("weekday")) else str(r.weekday),
        "gametime": None if _blank(r.get("gametime")) else str(r.gametime),
        "away": str(r.away_team),
        "home": str(r.home_team),
        "location": None if _blank(r.get("location")) else str(r.location),
        "roof": None if _blank(r.get("roof")) else str(r.roof),
        "surface": None if _blank(r.get("surface")) else str(r.surface),
        "temp": _num(r.get("temp")),
        "wind": _num(r.get("wind")),
        "away_rest": None if _num(r.get("away_rest")) is None else int(r.away_rest),
        "home_rest": None if _num(r.get("home_rest")) is None else int(r.home_rest),
        "away_coach": None if _blank(r.get("away_coach")) else str(r.away_coach),
        "home_coach": None if _blank(r.get("home_coach")) else str(r.home_coach),
        "stadium": None if _blank(r.get("stadium")) else str(r.stadium),
        "schedule_score_status": "present_not_used" if scores else "absent",
    }


def load_prior_plays(path: Path, game: dict) -> tuple[pd.DataFrame, dict]:
    import pyarrow.parquet as pq
    names = set(pq.read_schema(path).names)
    from_scheme = _scheme()
    cols = [c for c in list(from_scheme.PBP_COLUMNS) + PBP_EXTRA if c in names]
    frame = pd.read_parquet(path, columns=cols)
    if "season_type" in frame.columns:
        frame = frame[frame["season_type"] == "REG"]
    frame = frame[frame["season"] == game["season"]]
    frame = frame[pd.to_numeric(frame["week"], errors="coerce") < game["week"]]
    if "game_date" in frame.columns:
        dates = pd.to_datetime(frame["game_date"], errors="coerce").dt.strftime("%Y-%m-%d")
        frame = frame[dates < game["gameday"]]
    frame = frame[frame["game_id"].astype(str) != game["game_id"]].copy()
    scan = {
        "module": "data/scheme_profiles/build_profiles.py",
        "file": _rel(path),
        "sha256": _sha256(path),
        "as_of": f"plays with week < {game['week']} and game_date < {game['gameday']}",
        "rows": int(len(frame)),
        "max_week": None if frame.empty else int(pd.to_numeric(frame["week"], errors="coerce").max()),
        "columns_absent": [c for c in ("defenders_in_box", "n_pass_rushers", "n_blitzers", "was_pressure", "time_to_throw", "defense_coverage_type") if c not in names],
    }
    return frame, scan


def _team_games(plays: pd.DataFrame, team: str) -> list[str]:
    if plays.empty:
        return []
    mask = (plays["home_team"] == team) | (plays["away_team"] == team) if "home_team" in plays.columns else (
        (plays["posteam"] == team) | (plays["defteam"] == team))
    return sorted(set(plays.loc[mask, "game_id"].astype(str)))


def _dropbacks(plays: pd.DataFrame, team: str, side: str) -> pd.DataFrame:
    col = "defteam" if side == "defense" else "posteam"
    frame = plays[plays[col] == team]
    if "qb_dropback" not in frame.columns:
        return frame.iloc[0:0]
    frame = frame[pd.to_numeric(frame["qb_dropback"], errors="coerce") == 1]
    if "two_point_attempt" in frame.columns:
        frame = frame[pd.to_numeric(frame["two_point_attempt"], errors="coerce").fillna(0) != 1]
    return frame


def _published_tables(root: Path):
    from pregame.coverage_rates import NAME2AB, load
    canonical = load(2026)
    pull_path = root / COVERAGE_PULL_REL
    sharp, stat = {}, {}
    if pull_path.exists():
        for row in csv.DictReader(pull_path.open()):
            abbr = NAME2AB.get(row.get("team", ""))
            if not abbr:
                continue
            bucket = stat if "statrankings" in (row.get("source_url") or "").lower() or "StatRankings" in (row.get("source_type") or "") else sharp
            if "Sharp" in (row.get("source_type") or "") or "sharpfootball" in (row.get("source_url") or ""):
                bucket = sharp
            bucket[abbr] = row
    return canonical, sharp, stat, pull_path


def _pct_fact(value, *, source, as_of, definition, reason=None):
    if value is None:
        return fact("unknown", kind="unavailable", source=source, as_of=as_of, definition=definition,
                    reason=reason or "this source did not publish the figure", unit="published_percent")
    return fact(value, kind="measured", source=source, as_of=as_of, definition=definition, unit="published_percent")


def section_coverage(ctx) -> dict:
    canonical, sharp_rows, stat_rows, pull_path = _published_tables(ctx["root"])
    scheme = ctx["scheme"]
    blocked = scheme.blocked_group()
    teams = {}
    for team in ctx["teams"]:
        can = canonical.get(team) or {}
        can_src = {
            "module": "pregame.coverage_rates.load",
            "file": "data/coverage/sharp_coverage_2026.csv",
            "url": "https://www.sharpfootballanalysis.com/stats-nfl/nfl-coverage-schemes/",
            "pulled_utc": can.get("pulled_utc"),
            "source_updated": can.get("source_updated"),
            "note": "Season-to-date published table. Not a week-by-week point-in-time rebuild. Not blended with StatRankings.",
        }
        sharp = sharp_rows.get(team) or {}
        sharp_src = {
            "file": _rel(pull_path, ctx["root"]),
            "source_type": sharp.get("source_type"),
            "source_url": sharp.get("source_url"),
            "source_updated": sharp.get("source_updated"),
            "pull_time": sharp.get("pull_time_AST"),
            "weeks": sharp.get("weeks"),
            "note": "Sharp coverage page plus the sibling defensive-tendencies blitz column. Not blended with StatRankings.",
        }
        stat = stat_rows.get(team) or {}
        stat_src = {
            "file": _rel(pull_path, ctx["root"]),
            "source_type": stat.get("source_type"),
            "source_url": stat.get("source_url"),
            "source_updated": stat.get("source_updated"),
            "pull_time": stat.get("pull_time_AST"),
            "weeks": stat.get("weeks"),
            "note": "StatRankings CoverageIQ public chips. A different charting system from Sharp.",
        }
        shells = {}
        for key in SHELLS:
            shells[key] = _pct_fact(
                _published_number(sharp.get(key)) if sharp else None,
                source=sharp_src, as_of=sharp.get("source_updated"),
                definition=f"Sharp published {key}. Blank means the page did not publish it.",
                reason=None if _published_number(sharp.get(key) if sharp else None) is not None else "Sharp's public coverage page does not publish this shell",
            )
            sr = _published_number(stat.get(key)) if stat else None
            shells[key + "_statrankings"] = _pct_fact(
                sr, source=stat_src, as_of=stat.get("source_updated"),
                definition=f"StatRankings published {key}. Kept separate from Sharp. Top-25 articles leave the other teams blank.",
                reason=None if sr is not None else "not in the committed StatRankings extract for this team",
            )
        man_c = can.get("man_pct")
        man_s = _published_number(sharp.get("man_pct")) if sharp else None
        teams[team] = {
            "sharp_canonical": {
                "man_pct": _pct_fact(man_c, source=can_src, as_of=can.get("source_updated"), definition="Sharp man rate, published percent, via pregame.coverage_rates.load"),
                "zone_pct": _pct_fact(can.get("zone_pct"), source=can_src, as_of=can.get("source_updated"), definition="Sharp zone rate, published percent"),
                "mofc_pct": _pct_fact(can.get("mofc_pct"), source=can_src, as_of=can.get("source_updated"), definition="Sharp middle-closed / single-high rate, published percent"),
                "mofo_pct": _pct_fact(can.get("mofo_pct"), source=can_src, as_of=can.get("source_updated"), definition="Sharp middle-open / two-high rate, published percent"),
                "blitz_pct": _pct_fact(None, source=can_src, as_of=can.get("source_updated"), definition="Blitz is not a column on the canonical Sharp coverage CSV", reason="blitz lives on the tendencies pull, not this file"),
            },
            "sharp_tendencies_pull": {
                "man_pct": _pct_fact(man_s, source=sharp_src, as_of=sharp.get("source_updated"), definition="Sharp man rate from the 2026-11-22 tendencies pull"),
                "zone_pct": _pct_fact(_published_number(sharp.get("zone_pct")) if sharp else None, source=sharp_src, as_of=sharp.get("source_updated"), definition="Sharp zone rate from the 2026-11-22 pull"),
                "mofc_pct": _pct_fact(_published_number(sharp.get("mofc_pct")) if sharp else None, source=sharp_src, as_of=sharp.get("source_updated"), definition="Sharp single-high / middle closed"),
                "mofo_pct": _pct_fact(_published_number(sharp.get("mofo_pct")) if sharp else None, source=sharp_src, as_of=sharp.get("source_updated"), definition="Sharp two-high / middle open"),
                "blitz_pct": _pct_fact(_published_number(sharp.get("blitz_pct")) if sharp else None, source=sharp_src, as_of=sharp.get("source_updated"), definition="Sharp blitz rate from the public defensive-tendencies page"),
            },
            "statrankings": {
                "man_pct": _pct_fact(_published_number(stat.get("man_pct")) if stat else None, source=stat_src, as_of=stat.get("source_updated"), definition="StatRankings man rate. Not averaged with Sharp."),
                "zone_pct": _pct_fact(_published_number(stat.get("zone_pct")) if stat else None, source=stat_src, as_of=stat.get("source_updated"), definition="StatRankings zone rate. Not averaged with Sharp."),
                "mofc_pct": _pct_fact(_published_number(stat.get("mofc_pct")) if stat else None, source=stat_src, as_of=stat.get("source_updated"), definition="StatRankings single-high"),
                "mofo_pct": _pct_fact(_published_number(stat.get("mofo_pct")) if stat else None, source=stat_src, as_of=stat.get("source_updated"), definition="StatRankings two-high"),
                "blitz_pct": _pct_fact(_published_number(stat.get("blitz_pct")) if stat else None, source=stat_src, as_of=stat.get("source_updated"), definition="StatRankings blitz rate. Not averaged with Sharp."),
            },
            "sharp_vs_canonical_man_pct": "agree" if man_c is not None and man_s is not None and float(man_c) == float(man_s) else "differ_or_missing",
            "cover_shells": shells,
            "play_level_man_zone": scheme_fact(blocked["man_zone"], ctx["scan"]),
            "play_level_coverage_shells": scheme_fact(blocked["coverage_shells"], ctx["scan"]),
        }
    return {
        "sources_not_blended": True,
        "blended_rate": fact("unknown", kind="unavailable", source={"note": "Sharp and StatRankings use different charting"}, as_of=None,
                             definition="No cross-source average is computed", reason="mixing the two charting systems would invent a rate neither source published"),
        "teams": teams,
    }


def _target_rows(drop: pd.DataFrame) -> list[dict]:
    if drop.empty or "receiver_player_name" not in drop.columns:
        return []
    named = drop[drop["receiver_player_name"].notna()]
    rows = []
    for name, group in named.groupby(named["receiver_player_name"].astype(str)):
        yards = pd.to_numeric(group.get("receiving_yards"), errors="coerce")
        complete = pd.to_numeric(group.get("complete_pass"), errors="coerce").fillna(0) == 1
        y = float(yards.where(complete, 0).fillna(0).sum()) if yards is not None else None
        rows.append({"receiver": name, "targets": int(len(group)), "yards": None if y is None else round(y, 1)})
    rows.sort(key=lambda r: (-r["targets"], r["receiver"]))
    return rows


def _pressure_side(plays: pd.DataFrame, team: str, side: str, scan: dict) -> dict:
    src = short_source({**scan, "module": "nflverse play-by-play qb_hit and sack; regulation quarters only"})
    as_of = scan.get("as_of")
    reg = _regulation(plays)
    drop = _dropbacks(reg, team, side)
    side_col = "defteam" if side == "defense" else "posteam"
    side_plays = reg[reg[side_col] == team] if len(reg) and side_col in reg.columns else reg.iloc[0:0]
    if "two_point_attempt" in side_plays.columns:
        side_plays = side_plays[pd.to_numeric(side_plays["two_point_attempt"], errors="coerce").fillna(0) != 1]
    if "qb_hit" not in plays.columns:
        missing = fact("unknown", kind="unavailable", source=src, as_of=as_of, definition="qb_hit", reason="qb_hit column absent")
        return {"qb_hit_rate": missing}
    known = drop[pd.to_numeric(drop["qb_hit"], errors="coerce").notna()] if len(drop) else drop
    hits = int((pd.to_numeric(known["qb_hit"], errors="coerce") == 1).sum()) if len(known) else 0
    hit_rows = known[pd.to_numeric(known["qb_hit"], errors="coerce") == 1] if len(known) else known
    clean_rows = known[pd.to_numeric(known["qb_hit"], errors="coerce") == 0] if len(known) else known
    passes = side_plays[side_plays["play_type"] == "pass"] if "play_type" in side_plays.columns else side_plays.iloc[0:0]
    sacks = int((pd.to_numeric(passes["sack"], errors="coerce").fillna(0) == 1).sum()) if len(passes) and "sack" in passes.columns else 0
    targets = _target_rows(hit_rows[pd.to_numeric(hit_rows["pass_attempt"], errors="coerce").fillna(0) == 1]) if "pass_attempt" in hit_rows.columns else []
    unknown_targets = 0
    if len(hit_rows) and "receiver_player_name" in hit_rows.columns and "pass_attempt" in hit_rows.columns:
        att = hit_rows[pd.to_numeric(hit_rows["pass_attempt"], errors="coerce").fillna(0) == 1]
        unknown_targets = int(att["receiver_player_name"].isna().sum())
    return {
        "qb_hit_rate": _rate(hits, len(known), source=src, as_of=as_of, definition="Dropbacks with qb_hit = 1 divided by dropbacks with a non-null qb_hit. This is a hit, not an FTN pressure chart."),
        "sack_rate": _rate(sacks, len(passes), source=src, as_of=as_of, definition="Sacks divided by pass plays (play_type pass), same play set the scheme profile uses for sack_rate."),
        "epa_when_qb_hit": _mean(hit_rows["epa"], source=src, as_of=as_of, definition="Mean nflverse EPA on dropbacks with qb_hit = 1", unit="epa") if "epa" in hit_rows.columns else fact("unknown", kind="unavailable", source=src, as_of=as_of, definition="EPA", reason="epa column absent"),
        "epa_when_clean": _mean(clean_rows["epa"], source=src, as_of=as_of, definition="Mean nflverse EPA on dropbacks with qb_hit = 0", unit="epa") if "epa" in clean_rows.columns else fact("unknown", kind="unavailable", source=src, as_of=as_of, definition="EPA", reason="epa column absent"),
        "completion_when_qb_hit": _completion(hit_rows, src, as_of),
        "completion_when_clean": _completion(clean_rows, src, as_of),
        "targets_under_qb_hit": {
            "kind": "measured" if targets or unknown_targets else "unavailable",
            "unavailable": not targets and not unknown_targets,
            "value": targets[:8] if targets else "unknown",
            "sample_size": int(sum(r["targets"] for r in targets) + unknown_targets),
            "numerator": int(sum(r["targets"] for r in targets)),
            "denominator": int(sum(r["targets"] for r in targets) + unknown_targets) or None,
            "unknown_receiver_targets": unknown_targets,
            "definition": "Receiver targets on qb_hit dropbacks that are pass attempts. Not an FTN pressure-chart split. Top 8 receivers by targets.",
            "as_of": as_of,
            "source": src,
        },
        "ftn_pressure_rate": fact("unknown", kind="unavailable", source=src, as_of=as_of, definition="FTN was_pressure / n_pass_rushers", reason="no ftn_charting parquet is on main, and this play-by-play extract has no was_pressure or n_pass_rushers column"),
        "rush_four_vs_blitz": fact("unknown", kind="unavailable", source=src, as_of=as_of, definition="Dropbacks with 4 rushers versus a blitz", reason="n_pass_rushers and n_blitzers are FTN charting fields and are not in this extract"),
        "quick_pressure": fact("unknown", kind="unavailable", source=src, as_of=as_of, definition="Pressure before a time-to-throw threshold", reason="time_to_throw is not in this play-by-play extract"),
    }


def _completion(frame, src, as_of):
    if frame is None or frame.empty or "pass_attempt" not in frame.columns or "complete_pass" not in frame.columns:
        return fact("unknown", kind="unavailable", source=src, as_of=as_of, definition="Completions divided by pass attempts", reason="no pass attempts in this split")
    att = frame[pd.to_numeric(frame["pass_attempt"], errors="coerce").fillna(0) == 1]
    made = int((pd.to_numeric(att["complete_pass"], errors="coerce").fillna(0) == 1).sum()) if len(att) else 0
    return _rate(made, len(att), source=src, as_of=as_of, definition="Completions divided by pass attempts on this qb_hit split")


def section_pressure(ctx) -> dict:
    plays = ctx["plays"]
    teams = {}
    for team in ctx["teams"]:
        teams[team] = {
            "defense": _pressure_side(plays, team, "defense", ctx["scan"]),
            "offense": _pressure_side(plays, team, "offense", ctx["scan"]),
        }
    return {"teams": teams, "measured_as": "qb_hit and sack on nflverse play-by-play. Not an FTN pressure or blitz model."}


def _event_counts(plays: pd.DataFrame, team: str) -> list[dict]:
    if plays.empty:
        return []
    d = plays[plays["defteam"] == team]
    counts: dict[str, dict] = {}

    def add(names, kind):
        for name in names.dropna().astype(str):
            row = counts.setdefault(name, {"player": name, "pbu": 0, "interception": 0, "dpi": 0})
            row[kind] += 1

    if "pass_defense_1_player_name" in d.columns:
        add(d["pass_defense_1_player_name"], "pbu")
    if "pass_defense_2_player_name" in d.columns:
        add(d["pass_defense_2_player_name"], "pbu")
    if "interception_player_name" in d.columns:
        add(d["interception_player_name"], "interception")
    if {"penalty_type", "penalty_team", "penalty_player_name"} <= set(d.columns):
        dpi = d[(d["penalty_type"] == "Defensive Pass Interference") & (d["penalty_team"] == team)]
        add(dpi["penalty_player_name"], "dpi")
    rows = list(counts.values())
    for row in rows:
        row["verified_events"] = row["pbu"] + row["interception"] + row["dpi"]
        row["label"] = "measured_pbp_event"
        row["not_a_coverage_assignment"] = True
    rows.sort(key=lambda r: (-r["verified_events"], r["player"]))
    return rows


def _depth_db(root: Path, team: str, gameday: str) -> dict:
    path = root / DEPTH_REL
    src = {"file": DEPTH_REL, "module": "nflverse depth_charts_2026"}
    if not path.exists():
        return fact("unknown", kind="unavailable", source=src, as_of=None, definition="CB/S/slot depth", reason="depth chart file missing")
    frame = pd.read_parquet(path, columns=["dt", "team", "player_name", "pos_abb", "pos_rank", "pos_grp"])
    frame = frame[(frame["team"] == team) & (frame["dt"] < gameday)]
    if frame.empty:
        return fact("unknown", kind="unavailable", source=src, as_of=None, definition="Depth chart before kickoff", reason="no depth-chart row before this game")
    as_of = str(frame["dt"].max())
    latest = frame[frame["dt"] == frame["dt"].max()]
    starters = latest[(latest["pos_rank"] == 1) & latest["pos_abb"].isin(DB_SLOTS | OL_SLOTS | DL_SLOTS)]
    rows = [{"slot": str(r.pos_abb), "player": str(r.player_name), "group": str(r.pos_grp)} for r in starters.sort_values(["pos_grp", "pos_abb"]).itertuples()]
    return {
        "kind": "measured",
        "unavailable": False,
        "value": rows,
        "sample_size": len(rows),
        "as_of": as_of,
        "source": src,
        "definition": "Depth-chart rank 1 at the latest snapshot strictly before kickoff. A roster slot, not a coverage assignment.",
        "stale": as_of[:10] < gameday,
        "not_a_coverage_assignment": True,
    }


def section_assignments(ctx) -> dict:
    from pipeline.matchup_sources import fields as matchup_fields
    game = ctx["game"]
    pulled = ctx["scan"].get("sha256")
    pbp_shown = None
    if ctx["pbp_path"]:
        relative = _rel(ctx["pbp_path"], ctx["root"])
        pbp_shown = relative if Path(relative).is_file() else str(ctx["pbp_path"])
    raw = matchup_fields(
        ctx["teams"], game["season"], game["week"],
        pbp_path=pbp_shown,
        pbp_status="FRESH",
        pbp_as_of=ctx["scan"].get("as_of"),
        part_path=None,
    )
    raw["freshness_scope"] = "replay_as_of: weeks before this game in the historical pull. Not pipeline.freshness."
    raw["pbp_sha256"] = pulled
    teams = {}
    for team in ctx["teams"]:
        events = _event_counts(ctx["plays"], team)
        teams[team] = {
            "verified_pbp_events": {
                "kind": "measured" if events else "unavailable",
                "unavailable": not events,
                "value": events[:12] if events else "unknown",
                "sample_size": int(sum(r["verified_events"] for r in events)),
                "numerator": int(sum(r["verified_events"] for r in events)),
                "denominator": int(len(ctx["plays"][ctx["plays"]["defteam"] == team])) if len(ctx["plays"]) else 0,
                "definition": "PBU (pass_defense_* names), interception_player_name, and DPI penalty_player_name on this defense's plays. Counts of named events, not coverage assignments and not the PR #143 defender model.",
                "as_of": ctx["scan"].get("as_of"),
                "source": ctx["scan"],
                "not_a_coverage_assignment": True,
            },
            "depth_chart": _depth_db(ctx["root"], team, game["gameday"]),
            "slot_vs_outside_alignment": fact(
                "unknown", kind="unavailable", source={"module": "pipeline.matchup_sources"}, as_of=ctx["scan"].get("as_of"),
                definition="Per-player slot versus outside alignment",
                reason="no free per-play alignment field is in this extract. pass_location left/middle/right is not slot versus outside.",
            ),
            "receiver_routes": fact(
                "unknown", kind="unavailable", source={"module": "pipeline.matchup_sources.participation_routes"}, as_of=None,
                definition="Route names from pbp_participation",
                reason="the 2026 participation file is not in this repo, so route labels stay missing",
            ),
        }
    return {
        "matchup_sources": raw,
        "teams": teams,
        "likely_defenders_are_not_verified_without_evidence": True,
    }


def section_trenches(ctx) -> dict:
    scheme = ctx["scheme"]
    blocked = scheme.blocked_group()
    scan = ctx["scan"]
    absent = set(scan.get("columns_absent") or [])
    box_reason = "defenders_in_box is not a column in this play-by-play extract" if "defenders_in_box" in absent else "not computed"
    teams = {}
    for team in ctx["teams"]:
        depth = _depth_db(ctx["root"], team, ctx["game"]["gameday"])
        ol, dl = [], []
        if isinstance(depth, dict) and isinstance(depth.get("value"), list):
            ol = [r for r in depth["value"] if r["slot"] in OL_SLOTS]
            dl = [r for r in depth["value"] if r["slot"] in DL_SLOTS]
        teams[team] = {
            "blocking_assignments": scheme_fact(blocked["blocking_assignments"], scan),
            "personnel_packages": scheme_fact(blocked["personnel_packages"], scan),
            "box_structure": fact("unknown", kind="unavailable", source=scan, as_of=scan.get("as_of"),
                                  definition="Defenders in the box / front structure", reason=box_reason),
            "ol_depth_chart": {
                "kind": "measured" if ol else "unavailable",
                "unavailable": not ol,
                "value": ol or "unknown",
                "sample_size": len(ol),
                "as_of": depth.get("as_of") if isinstance(depth, dict) else None,
                "definition": "Offensive-line depth-chart rank 1. Not a pass-protection grade.",
                "source": {"file": DEPTH_REL},
            },
            "dl_depth_chart": {
                "kind": "measured" if dl else "unavailable",
                "unavailable": not dl,
                "value": dl or "unknown",
                "sample_size": len(dl),
                "as_of": depth.get("as_of") if isinstance(depth, dict) else None,
                "definition": "Defensive-line depth-chart rank 1. Not a pass-rush grade.",
                "source": {"file": DEPTH_REL},
            },
            "opponent_adjusted_allowances": fact(
                "unknown", kind="unavailable", source={"pr": 144, "module": "data/coverage/positional_allowances_2026/build_allowances.py"},
                as_of=None, definition="Leave-one-out opponent-adjusted positional allowances",
                reason="PR #144 is not on main and data/coverage/positional_allowances_2026 was not built. The allowance model is not reimplemented here.",
            ),
            "run_direction_and_gap": {
                "kind": "measured",
                "unavailable": False,
                "value": "see situational.teams.<team>.defense.rush_direction and rush_gap",
                "definition": "Run location and gap shares from scheme aggregate_side, scanned on the prior-week plays.",
                "as_of": scan.get("as_of"),
                "source": scan,
            },
        }
    return {"teams": teams}


def section_situational(ctx) -> dict:
    scheme = ctx["scheme"]
    plays = ctx["plays"]
    teams = {}
    for team in ctx["teams"]:
        ids = _team_games(plays, team)
        phase = scheme.aggregate_phase(plays, team, "regulation", ids)
        scan = {**ctx["scan"], "team": team, "game_ids": ids, "games": len(ids)}
        off = annotate(phase["offense"], scan)
        defense = annotate(phase["defense"], scan)
        scr = off.get("scrimmage_plays", {})
        plays_n = scr.get("numerator") or 0
        pace = _rate(plays_n, len(ids), source=scan, as_of=scan.get("as_of"),
                     definition="Regulation pass and run plays divided by prior games. Kneels and spikes are excluded, matching scheme scrimmage_plays.",
                     unit="plays_per_game")
        off_plays = plays[plays["posteam"] == team] if len(plays) else plays
        scrimmage = off_plays[off_plays["play_type"].isin(["pass", "run"])] if len(off_plays) and "play_type" in off_plays.columns else off_plays
        if "no_huddle" in scrimmage.columns and len(scrimmage):
            known = scrimmage[pd.to_numeric(scrimmage["no_huddle"], errors="coerce").notna()]
            nh = int((pd.to_numeric(known["no_huddle"], errors="coerce") == 1).sum()) if len(known) else 0
            no_huddle = _rate(nh, len(known), source=scan, as_of=scan.get("as_of"), definition="Share of scrimmage plays with no_huddle = 1. Missing flags are excluded, not counted as huddled.")
        else:
            no_huddle = fact("unknown", kind="unavailable", source=scan, as_of=scan.get("as_of"), definition="no_huddle rate", reason="no_huddle column absent or no plays")
        teams[team] = {
            "scan": {"game_ids": ids, "games": len(ids), "max_week": scan.get("max_week"), "as_of": scan.get("as_of"), "file": scan.get("file"), "sha256": scan.get("sha256")},
            "offense": off,
            "defense": defense,
            "pace_plays_per_game": pace,
            "no_huddle_rate": no_huddle,
            "coaching_scheme_note": "Score-state pass rates (neutral, leading, trailing) are the measured scheme behavior in offense. Personnel packages and route concepts stay unavailable.",
        }
    return {"teams": teams, "phase": "regulation", "overtime": fact("unknown", kind="unavailable", source=ctx["scan"], as_of=ctx["scan"].get("as_of"), definition="Overtime situational rates", reason="this packet scans regulation only; overtime is a separate scheme phase and is not pooled in")}


def _miles(a, b) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return round(3958.8 * 2 * math.asin(math.sqrt(h)), 1)


def _previous_site(schedule: pd.DataFrame, team: str, game: dict) -> dict | None:
    prior = schedule[(schedule["season"] == game["season"]) & (schedule["game_type"] == "REG") & (schedule["gameday"] < game["gameday"])]
    prior = prior[(prior["away_team"] == team) | (prior["home_team"] == team)].sort_values("gameday")
    if prior.empty:
        return None
    row = prior.iloc[-1]
    home = str(row.home_team)
    return {"game_id": str(row.game_id), "gameday": str(row.gameday), "week": int(row.week),
            "was_home": home == team, "site_team": home, "stadium": None if _blank(row.get("stadium")) else str(row.stadium)}


def section_context(ctx) -> dict:
    from pregame.weather import STADIUM
    game = ctx["game"]
    schedule = ctx["schedule"]
    src = {"file": _rel(ctx["schedule_path"], ctx["root"]), "module": "nflverse schedule"}
    roof = (game.get("roof") or "").lower()
    indoor = roof in {"dome", "closed"}
    weather = {
        "roof": fact(game.get("roof"), kind="measured" if game.get("roof") else "unavailable", source=src, as_of=game["gameday"],
                     definition="Schedule roof", reason=None if game.get("roof") else "roof blank"),
        "pregame_forecast": fact(
            "unknown", kind="unavailable", source={"module": "pregame.weather.forecast"}, as_of=game["gameday"],
            definition="Hourly forecast at kickoff",
            reason="indoor game; no forecast is required" if indoor else "historical replay does not call the National Weather Service, and no stored pregame forecast file is attached. Schedule temp/wind are not used as a forecast.",
        ),
    }
    if game.get("temp") is not None or game.get("wind") is not None:
        weather["schedule_temp_wind"] = {
            "kind": "measured",
            "unavailable": False,
            "value": {"temp": game.get("temp"), "wind": game.get("wind")},
            "definition": "Values on the schedule row. For a completed game these are observed conditions, not a pregame forecast, and no profile treats them as a forecast.",
            "used_as_forecast": False,
            "as_of": game["gameday"],
            "source": src,
        }
    else:
        weather["schedule_temp_wind"] = fact("unknown", kind="unavailable", source=src, as_of=game["gameday"],
                                             definition="Schedule temp and wind", reason="the schedule row has no temp or wind")
    teams = {}
    for team, rest_days, coach in (
        (game["away"], game["away_rest"], game["away_coach"]),
        (game["home"], game["home_rest"], game["home_coach"]),
    ):
        prev = _previous_site(schedule, team, game)
        if rest_days is None:
            rest = fact("unknown", kind="unavailable", source=src, as_of=game["gameday"], definition="nflverse rest days", reason="rest blank on the schedule")
        else:
            rest = fact(rest_days, kind="measured", source=src, as_of=game["gameday"], sample_size=1, definition="nflverse away_rest or home_rest on this game row. Known before kickoff.", unit="days")
        if prev is None or team not in STADIUM or prev["site_team"] not in STADIUM:
            travel = fact("unknown", kind="unavailable", source={"module": "pregame.weather.STADIUM"}, as_of=game["gameday"],
                          definition="Miles from the previous game site to this stadium",
                          reason="no prior game, or a site is missing from the stadium coordinate table")
        else:
            this_site = game["home"]
            miles = _miles(STADIUM[prev["site_team"]], STADIUM[this_site])
            travel = fact(miles, kind="estimate", source={"module": "pregame.weather.STADIUM", "method": "haversine_miles"},
                          as_of=game["gameday"], sample_size=1,
                          definition="Great-circle miles between approximate stadium coordinates. An estimate, not a tracked itinerary.",
                          unit="miles")
        teams[team] = {
            "coach": fact(coach, kind="measured" if coach else "unavailable", source=src, as_of=game["gameday"],
                          definition="Head coach on the nflverse schedule", reason=None if coach else "coach blank"),
            "rest_days": rest,
            "previous_site": prev or fact("unknown", kind="unavailable", source=src, as_of=game["gameday"], definition="Previous game site", reason="no earlier game"),
            "travel_miles_from_previous_site": travel,
        }
    return {"weather": weather, "teams": teams}


def section_open_prs(ctx) -> dict:
    """Read PR #140/#143/#144 only when their code or built tables are already present."""
    out = {}
    try:
        from pipeline.read_rules.defense_allowed import profile as defense_profile
    except ImportError:
        defense_profile = None
    if defense_profile is None:
        out["pr_140_defense_allowed"] = fact(
            "unknown", kind="unavailable", source={"pr": 140, "module": "pipeline.read_rules.defense_allowed.profile"},
            as_of=None, definition="Role, depth, and run-defense allowed profile",
            reason="PR #140 is not merged. pipeline.read_rules.defense_allowed is absent, so the flag profile is not reimplemented.",
        )
    else:
        out["pr_140_defense_allowed"] = {"kind": "measured", "unavailable": False, "value": "callable", "source": {"pr": 140, "module": "pipeline.read_rules.defense_allowed.profile"}}
    defenders = ctx["root"] / "data" / "coverage" / "defender_profiles_2026" / "defenders_cb_s_lb.csv"
    if defenders.exists():
        out["pr_143_defender_profiles"] = {"kind": "measured", "unavailable": False, "value": str(defenders), "source": {"pr": 143}}
    else:
        out["pr_143_defender_profiles"] = fact(
            "unknown", kind="unavailable", source={"pr": 143, "module": "data/coverage/defender_profiles_2026/build.py"},
            as_of=None, definition="Per-defender CB/S/LB coverage profile",
            reason="PR #143 is not merged and defenders_cb_s_lb.csv is not on main. Verified PBP names in assignments are events, not that model.",
        )
    allowances = ctx["root"] / "data" / "coverage" / "positional_allowances_2026" / "allowances_windows.csv"
    if allowances.exists():
        out["pr_144_positional_allowances"] = {"kind": "measured", "unavailable": False, "value": str(allowances), "source": {"pr": 144}}
    else:
        out["pr_144_positional_allowances"] = fact(
            "unknown", kind="unavailable", source={"pr": 144, "module": "data/coverage/positional_allowances_2026/build_allowances.py"},
            as_of=None, definition="Positional allowances by window and opponent adjustment",
            reason="PR #144 is not merged and allowances_windows.csv is not on main. The leave-one-out model is not reimplemented.",
        )
    return out


SECTION_FUNCS = {
    "coverage": section_coverage,
    "pressure": section_pressure,
    "assignments": section_assignments,
    "trenches": section_trenches,
    "situational": section_situational,
    "context": section_context,
    "open_prs": section_open_prs,
}


def _run(name, fn, ctx):
    started = time.perf_counter()
    try:
        body = fn(ctx)
        status, error = "EXECUTED", None
    except Exception as exc:
        body = fact("unknown", kind="unavailable", source={"section": name}, as_of=None,
                    definition=name, reason=f"{type(exc).__name__}: {exc}")
        status, error = "FAILED", f"{type(exc).__name__}: {exc}"
    return {
        "section": name,
        "status": status,
        "module": f"{fn.__module__}.{fn.__name__}",
        "thread": threading.current_thread().name,
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 1),
        "error": error,
        "output": body,
    }


def build_packet(game_id: str, *, root: Path | None = None, pbp_path: Path | None = None,
                 schedule_path: Path | None = None, workers: int = 7) -> dict:
    root = Path(root or ROOT)
    schedule_path = Path(schedule_path or root / SCHEDULE_REL)
    pbp_path = Path(pbp_path or root / PBP_REL)
    schedule = load_schedule(schedule_path)
    game = game_row(schedule, game_id)
    if not pbp_path.exists():
        plays = pd.DataFrame()
        scan = {"file": str(pbp_path), "as_of": None, "rows": 0, "max_week": None, "sha256": None,
                "columns_absent": ["play-by-play file missing"], "module": "data/scheme_profiles/build_profiles.py"}
    else:
        plays, scan = load_prior_plays(pbp_path, game)
    ctx = {
        "root": root,
        "game": game,
        "teams": (game["away"], game["home"]),
        "plays": plays,
        "scan": scan,
        "pbp_path": pbp_path if pbp_path.exists() else None,
        "schedule": schedule,
        "schedule_path": str(schedule_path),
        "scheme": _scheme(),
    }
    receipts = []
    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="matchup") as pool:
        futs = [pool.submit(_run, name, fn, ctx) for name, fn in SECTION_FUNCS.items()]
        for fut in futs:
            receipts.append(fut.result())
    receipts.sort(key=lambda r: r["section"])
    packet = {
        "schema": SCHEMA,
        "projection_ready": False,
        "research_only": True,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "game": {k: v for k, v in game.items() if k not in ("temp", "wind")},
        "as_of": {
            "week_exclusive": game["week"],
            "before_date": game["gameday"],
            "max_play_week": scan.get("max_week"),
            "play_rows": scan.get("rows"),
            "pbp_file": scan.get("file"),
            "pbp_sha256": scan.get("sha256"),
            "columns_absent": scan.get("columns_absent"),
        },
        "receipts": [{k: v for k, v in r.items() if k != "output"} for r in receipts],
        "sections": {r["section"]: r["output"] for r in receipts},
    }
    return json_safe(packet)


def render_report(packet: dict) -> str:
    game = packet["game"]
    lines = [
        f"# Matchup research {game['away']} at {game['home']}",
        "",
        f"Game `{game['game_id']}` week {game['week']} on {game['gameday']}. Research only. `projection_ready` is false.",
        f"Plays used: week < {packet['as_of']['week_exclusive']} (max week in the scan: {packet['as_of']['max_play_week']}, {packet['as_of']['play_rows']} rows).",
        "Sharp and StatRankings stay in separate blocks. Estimates are labeled estimate. Missing inputs are unavailable, not zero.",
        "",
        "## Execution",
        "",
    ]
    for rec in packet["receipts"]:
        lines.append(f"- {rec['section']}: {rec['status']} in {rec['elapsed_ms']} ms on {rec['thread']}")
    lines.append("")
    sit = packet["sections"].get("situational", {}).get("teams", {})
    cov = packet["sections"].get("coverage", {}).get("teams", {})
    for team, side in sit.items():
        defense = side.get("defense", {})
        third = defense.get("third_down_conversion_rate", {})
        early = side.get("offense", {}).get("early_down_pass_rate", {})
        explosive = defense.get("explosive_pass_20_rate", {})
        man = cov.get(team, {}).get("sharp_canonical", {}).get("man_pct", {})
        mofo = cov.get(team, {}).get("sharp_canonical", {}).get("mofo_pct", {})
        lines.append(f"## {team}")
        lines.append("")
        lines.append(f"- Sharp man {man.get('value')}% ({man.get('kind')}), two-high {mofo.get('value')}% ({mofo.get('kind')}).")
        lines.append(f"- Offense early-down pass rate {early.get('value')} on {early.get('numerator')}/{early.get('denominator')} ({early.get('kind')}).")
        lines.append(f"- Defense third-down conversion rate allowed {third.get('value')} on {third.get('numerator')}/{third.get('denominator')} ({third.get('kind')}).")
        lines.append(f"- Defense explosive complete-pass rate allowed (20+ yards) {explosive.get('value')} on {explosive.get('numerator')}/{explosive.get('denominator')} ({explosive.get('kind')}).")
        lines.append(f"- Prior games in the scan: {side.get('scan', {}).get('games')}.")
        lines.append("")
    lines.append("Open PRs #140, #143, and #144 are referenced in `sections.open_prs` and are not copied into this packet.")
    lines.append("")
    return "\n".join(lines) + "\n"
