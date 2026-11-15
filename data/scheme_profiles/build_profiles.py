#!/usr/bin/env python3
"""Build 2026 team scheme and opportunity profiles.

Research only. Reads the pinned public nflverse play-by-play pull and the
official gamebook extracts already in this repo, plus one Thursday gamebook
that is hashed and cross-checked but not stored. Does not set
projection_ready, and does not read or write model weights.

Missing measurements stay "unknown". A scanned count of zero is a count with
observed true. A rate whose denominator is zero is unknown, not 0.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
OUT_DIR = REPO / "data" / "scheme_profiles" / "2026"
EVIDENCE_REL = "data/scheme_profiles/2026/evidence_plays.csv.gz"
WEEK9_DIR = REPO / "data" / "gamebooks" / "2026" / "wk09"
GAMEBOOK_PARSER = REPO / "data" / "gamebooks"

PBP_URL = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet"
PBP_SHA = "05f37f2f65d3db42d9036cef0da1554d6fdbb861f6005a454756e14c34a836d8"
PBP_RETRIEVED = "2026-11-15T12:45:04Z"
PBP_LAST_MODIFIED = "2026-11-15T10:04:05Z"
PINNED_PBP = "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
PINNED_PBP_SHA = "1028614beb746bea596633bb2215948d19ddcc34f8928e74a3338635122ec5b8"
PINNED_PBP_RETRIEVED = "2026-11-12T16:16:00Z"

SCHEDULE_URL = "https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv"
SCHEDULE_SHA = "85e2dcb8211806d8fd77bfd8622e0cade40718af8e28a9cd9aa7c48337a31ebf"
SCHEDULE_RETRIEVED = "2026-11-15T12:44:36Z"
SCHEDULE_COLUMNS = [
    "game_id", "season", "game_type", "week", "gameday", "weekday",
    "away_team", "away_score", "home_team", "home_score",
]

LINKS_RETRIEVED = "2026-11-15T12:46:20Z"
NFL_GAMEBOOK_HELP = "https://support.nfl.com/hc/en-us/articles/35869678028180-Game-Books"
NFLVERSE_LICENSE = "https://github.com/nflverse/nflverse-data/blob/main/LICENSE.md"
GENERATED_UTC = "2026-11-15T12:50:00Z"

WEEK10_GAME = "2026_10_WAS_NYG"
WEEK10_PDF_URL = "https://static.www.nfl.com/image/upload/v1794570519/gamecenter/ab5828d9-4feb-11f1-abca-2c54536568a9.pdf"
WEEK10_PDF_SHA = "12c818cc26344849773621c74100defb2ad8e5cecfb343b8e28a9df44a8f0d3f"
WEEK10_PDF_RETRIEVED = "2026-11-15T12:47:02Z"
LAST_COMPLETED_WEEK = 9
LAST_PROFILE_DATE = "2026-11-12"

COPYRIGHT = (
    "NFL Copyright © 2026 by The National Football League. All rights reserved. "
    "This summary and play-by-play is for the express purpose of assisting media "
    "in their coverage of the game; any other use of this material is prohibited "
    "without the written permission of the National Football League."
)

TEAMS = [
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", "GB",
    "HOU", "IND", "JAX", "KC", "LA", "LAC", "LV", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WAS",
]
NAMES = {
    "ARI": "Arizona Cardinals", "ATL": "Atlanta Falcons", "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills", "CAR": "Carolina Panthers", "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals", "CLE": "Cleveland Browns", "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos", "DET": "Detroit Lions", "GB": "Green Bay Packers",
    "HOU": "Houston Texans", "IND": "Indianapolis Colts", "JAX": "Jacksonville Jaguars",
    "KC": "Kansas City Chiefs", "LA": "Los Angeles Rams", "LAC": "Los Angeles Chargers",
    "LV": "Las Vegas Raiders", "MIA": "Miami Dolphins", "MIN": "Minnesota Vikings",
    "NE": "New England Patriots", "NO": "New Orleans Saints", "NYG": "New York Giants",
    "NYJ": "New York Jets", "PHI": "Philadelphia Eagles", "PIT": "Pittsburgh Steelers",
    "SEA": "Seattle Seahawks", "SF": "San Francisco 49ers", "TB": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans", "WAS": "Washington Commanders",
}
SLUG = {
    "ARI": "cardinals", "ATL": "falcons", "BAL": "ravens", "BUF": "bills", "CAR": "panthers",
    "CHI": "bears", "CIN": "bengals", "CLE": "browns", "DAL": "cowboys", "DEN": "broncos",
    "DET": "lions", "GB": "packers", "HOU": "texans", "IND": "colts", "JAX": "jaguars",
    "KC": "chiefs", "LA": "rams", "LAC": "chargers", "LV": "raiders", "MIA": "dolphins",
    "MIN": "vikings", "NE": "patriots", "NO": "saints", "NYG": "giants", "NYJ": "jets",
    "PHI": "eagles", "PIT": "steelers", "SEA": "seahawks", "SF": "49ers", "TB": "buccaneers",
    "TEN": "titans", "WAS": "commanders",
}
REPO_ALIAS = {"LA": "LAR", "WAS": "WSH"}
GAMEBOOK_ABBR = {"ARZ": "ARI", "BLT": "BAL", "CLV": "CLE", "HST": "HOU"}
UUID_RE = re.compile(r"gamecenter/([0-9a-f-]+)\.pdf")
EFF_RE = re.compile(r"^(\d+)-(\d+)-([\d.]+)%$")
PASS_RE = re.compile(r"^(\d+)-(\d+)-(\d+)$")
SACK_RE = re.compile(r"^(\d+)-(\d+)$")

PBP_COLUMNS = [
    "play_id", "game_id", "season", "week", "season_type", "game_date",
    "home_team", "away_team", "posteam", "defteam", "qtr", "down", "ydstogo",
    "yardline_100", "score_differential", "play_type", "sack", "qb_scramble",
    "shotgun", "passer_player_id", "passer_player_name", "rusher_player_id",
    "rusher_player_name", "receiver_player_id", "receiver_player_name",
    "yards_gained", "complete_pass", "touchdown", "run_location", "run_gap",
    "third_down_converted", "third_down_failed", "fixed_drive", "field_goal_result",
    "two_point_attempt", "total_home_score", "total_away_score",
]
EVIDENCE_COLUMNS = [c for c in PBP_COLUMNS if c not in ("season_type", "total_home_score", "total_away_score")]

BLOCKED_REASON = (
    "Not an explicit field in the nflverse play-by-play extract or in the parsed "
    "official gamebook tables. Play-description prose, tacklers, targets, and "
    "formation labels are not treated as proof of this call."
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def game_center_url(away: str, home: str, week: int) -> str:
    return f"https://www.nfl.com/games/{SLUG[away]}-at-{SLUG[home]}-2026-reg-{int(week)}"


def own_gamebook_urls(link_rows: list[dict]) -> dict[str, str]:
    """Pick the game's own Game Book PDF, not the sitewide latest-book link."""
    counts: Counter[str] = Counter()
    for row in link_rows:
        for url in row["pdf_urls"]:
            match = UUID_RE.search(url)
            if not match:
                raise SystemExit(f"gamebook URL has no uuid: {url}")
            counts[match.group(1)] += 1
    chosen = {}
    for row in link_rows:
        urls = list(row["pdf_urls"])
        if len(urls) == 1:
            own = urls[0]
        else:
            unique = [url for url in urls if counts[UUID_RE.search(url).group(1)] == 1]
            if len(unique) != 1:
                raise SystemExit(f"could not isolate gamebook for {row['game_id']}: {urls}")
            own = unique[0]
        chosen[row["game_id"]] = own
    return chosen


def _stamp(definition: str, game_ids: list[str]) -> dict:
    return {
        "definition": definition,
        "source_url": PBP_URL,
        "source_sha256": PBP_SHA,
        "retrieved_utc": PBP_RETRIEVED,
        "game_ids": list(game_ids),
        "evidence_file": EVIDENCE_REL,
    }


def count_metric(n: int, definition: str, game_ids: list[str], scanned: bool = True) -> dict:
    payload = _stamp(definition, game_ids)
    payload["kind"] = "count"
    payload["numerator"] = int(n) if scanned else None
    payload["denominator"] = None
    if not scanned:
        payload["value"] = "unknown"
        payload["observed"] = False
        payload["reason"] = "the window was not scanned"
        return payload
    payload["value"] = int(n)
    payload["observed"] = True
    return payload


def rate_metric(numer: int, denom: int, definition: str, game_ids: list[str]) -> dict:
    numer = int(numer)
    denom = int(denom)
    if numer < 0 or denom < 0 or (denom and numer > denom):
        raise ValueError(f"rate out of range {numer}/{denom}: {definition}")
    payload = _stamp(definition, game_ids)
    payload["kind"] = "rate"
    payload["numerator"] = numer
    payload["denominator"] = denom
    if denom <= 0:
        payload["value"] = "unknown"
        payload["observed"] = False
        payload["reason"] = "denominator is zero; the rate is unknown, not zero"
        return payload
    payload["value"] = round(numer / denom, 6)
    payload["observed"] = True
    return payload


def difference_metric(later: dict, earlier: dict, definition: str, game_ids: list[str]) -> dict:
    payload = _stamp(definition, game_ids)
    payload["kind"] = "rate_difference"
    payload["later_numerator"] = later.get("numerator")
    payload["later_denominator"] = later.get("denominator")
    payload["earlier_numerator"] = earlier.get("numerator")
    payload["earlier_denominator"] = earlier.get("denominator")
    if later.get("value") == "unknown" or earlier.get("value") == "unknown":
        payload["value"] = "unknown"
        payload["observed"] = False
        payload["numerator"] = None
        payload["denominator"] = None
        payload["reason"] = "one side of the comparison has no scanned sample"
        return payload
    payload["value"] = round(float(later["value"]) - float(earlier["value"]), 6)
    payload["observed"] = True
    payload["numerator"] = None
    payload["denominator"] = None
    return payload


def blocked_field(reason: str) -> dict:
    return {
        "status": "BLOCKED",
        "value": "unknown",
        "observed": False,
        "reason": reason,
        "source_url": PBP_URL,
        "retrieved_utc": PBP_RETRIEVED,
    }


def blocked_group() -> dict:
    return {key: blocked_field(BLOCKED_REASON) for key in (
        "route_concepts", "coverage_shells", "man_zone",
        "blocking_assignments", "player_matchups", "personnel_packages",
    )}


def _ids(frame: pd.DataFrame) -> list[str]:
    if frame.empty:
        return []
    return sorted(set(frame["game_id"].astype(str)))


def _n(mask) -> int:
    return int(mask.sum())


def side_frame(plays: pd.DataFrame, team: str, side: str, phase: str) -> pd.DataFrame:
    if side == "offense":
        frame = plays[plays["posteam"] == team]
    elif side == "defense":
        frame = plays[plays["defteam"] == team]
    else:
        raise ValueError(side)
    quarter = pd.to_numeric(frame["qtr"], errors="coerce")
    if phase == "regulation":
        frame = frame[quarter <= 4]
    elif phase == "overtime":
        frame = frame[quarter >= 5]
    else:
        raise ValueError(phase)
    return frame


def _not_two_point(frame: pd.DataFrame) -> pd.DataFrame:
    if "two_point_attempt" not in frame.columns:
        return frame
    flag = pd.to_numeric(frame["two_point_attempt"], errors="coerce")
    return frame[flag != 1]


def _scrimmage(frame: pd.DataFrame) -> pd.DataFrame:
    """Pass and run plays from scrimmage. Two-point tries are a separate count."""
    frame = _not_two_point(frame)
    return frame[frame["play_type"].isin(["pass", "run"])]


def _player_rows(frame: pd.DataFrame, id_col: str, name_col: str, game_ids: list[str], kind: str) -> list[dict]:
    labeled = frame[frame[id_col].notna()].copy()
    if labeled.empty:
        return []
    labeled[id_col] = labeled[id_col].astype(str)
    rows = []
    grouped = labeled.groupby(id_col, sort=False)
    for player_id, group in grouped:
        names = [name for name in group[name_col].dropna().astype(str).unique()]
        rows.append({
            "player_id": str(player_id),
            "player_name": names[0] if len(names) == 1 else " | ".join(sorted(names)),
            "plays": int(len(group)),
            "team_plays": int(len(labeled)),
            "share": round(len(group) / len(labeled), 6),
            "games": int(group["game_id"].nunique()),
            "window_games": len(game_ids),
            "kind": kind,
            "source_url": PBP_URL,
            "source_sha256": PBP_SHA,
            "retrieved_utc": PBP_RETRIEVED,
            "game_ids": sorted(set(group["game_id"].astype(str))),
        })
    rows.sort(key=lambda item: (-item["plays"], item["player_name"], item["player_id"]))
    return rows


def player_window(plays: pd.DataFrame, team: str, game_ids: list[str], requested: int) -> dict:
    """Opportunity shares for the team's most recent games. No zero-padded games."""
    ordered = list(game_ids)
    status = "COMPLETE" if len(ordered) >= requested else "PARTIAL"
    window_ids = ordered[-requested:] if len(ordered) >= requested else ordered
    scope = _not_two_point(plays[plays["game_id"].isin(window_ids)])
    offense = scope[scope["posteam"] == team]
    passes = offense[offense["play_type"] == "pass"]
    drops = passes[passes["sack"] != 1]
    targets = drops[drops["receiver_player_id"].notna()]
    rushes = offense[(offense["play_type"] == "run") & (offense["rusher_player_id"].notna())]
    return {
        "games": len(window_ids),
        "requested_games": requested,
        "status": status,
        "game_ids": window_ids,
        "targets": _player_rows(targets, "receiver_player_id", "receiver_player_name", window_ids, "target"),
        "carries": _player_rows(rushes, "rusher_player_id", "rusher_player_name", window_ids, "carry"),
        "unassigned_pass_plays": count_metric(
            _n(passes["receiver_player_id"].isna()) if len(passes) else _n(drops["receiver_player_id"].isna()) if len(drops) else 0,
            "Pass plays, including sacks, with no receiver id. Sacks and throwaways stay unassigned. They are not a player with zero targets.",
            window_ids,
        ),
        "unassigned_rushes": count_metric(
            _n((offense["play_type"] == "run") & offense["rusher_player_id"].isna()),
            "Run plays with no rusher id. Kneels are a separate play type and are not carries.",
            window_ids,
        ),
    }


def _fix_unassigned_passes(offense: pd.DataFrame, game_ids: list[str]) -> dict:
    passes = offense[offense["play_type"] == "pass"]
    return count_metric(
        _n(passes["receiver_player_id"].isna()),
        "Pass plays, including sacks, with no receiver id. Sacks and throwaways stay unassigned. They are not a player with zero targets.",
        game_ids,
    )


def aggregate_side(plays: pd.DataFrame, team: str, side: str, phase: str, game_ids: list[str]) -> dict:
    """One side of the ball in regulation or overtime. Rates with an empty sample are unknown."""
    frame = side_frame(plays, team, side, phase)
    scr = _scrimmage(frame)
    ids = list(game_ids)
    subject = "by the offense" if side == "offense" else "allowed by the defense"
    passes = scr[scr["play_type"] == "pass"]
    runs = scr[scr["play_type"] == "run"]
    down = pd.to_numeric(scr["down"], errors="coerce")
    distance = pd.to_numeric(scr["ydstogo"], errors="coerce")
    score = pd.to_numeric(scr["score_differential"], errors="coerce")
    yard = pd.to_numeric(scr["yardline_100"], errors="coerce")
    early = scr[down.isin([1, 2])]
    early_pass = _n(early["play_type"] == "pass")
    early_run = _n(early["play_type"] == "run")
    neutral = scr[score.notna() & (score >= -7) & (score <= 7)]
    leading = scr[score.notna() & (score >= 8)]
    trailing = scr[score.notna() & (score <= -8)]
    tied = scr[score.notna() & (score == 0)]
    short = scr[distance.notna() & (distance <= 2)]
    long = scr[distance.notna() & (distance >= 7)]
    clock_or_scrimmage = _not_two_point(frame)
    third = clock_or_scrimmage[
        (pd.to_numeric(clock_or_scrimmage["down"], errors="coerce") == 3)
        & clock_or_scrimmage["play_type"].isin(["pass", "run", "qb_kneel", "qb_spike"])
    ]
    third_conv = _n(pd.to_numeric(third["third_down_converted"], errors="coerce") == 1)
    third_fail = _n(pd.to_numeric(third["third_down_failed"], errors="coerce") == 1)
    third_unknown = int(len(third) - third_conv - third_fail)
    red = scr[yard.notna() & (yard <= 20)]
    red_pass = _n(red["play_type"] == "pass")
    red_td = _n(pd.to_numeric(red["touchdown"], errors="coerce") == 1)
    sacks = _n(pd.to_numeric(passes["sack"], errors="coerce") == 1)
    scrambles = runs[pd.to_numeric(runs["qb_scramble"], errors="coerce") == 1]
    shotgun_known = scr[pd.to_numeric(scr["shotgun"], errors="coerce").notna()]
    shotgun_n = _n(pd.to_numeric(shotgun_known["shotgun"], errors="coerce") == 1)
    explosive_pass = _n(
        (pd.to_numeric(passes["complete_pass"], errors="coerce") == 1)
        & (pd.to_numeric(passes["yards_gained"], errors="coerce") >= 20)
    )
    rush_yards = pd.to_numeric(runs["yards_gained"], errors="coerce")
    explosive_10 = _n(rush_yards >= 10)
    explosive_15 = _n(rush_yards >= 15)
    kneels = frame[frame["play_type"] == "qb_kneel"]

    def direction(column: str, labels: set[str], noun: str) -> dict:
        values = runs[column].astype("string")
        known = values.isin(labels)
        payload = {
            "plays": count_metric(len(runs), f"Run plays scanned for {noun} {subject}.", ids),
            "unknown": count_metric(_n(~known), f"Run plays whose nflverse {column} is missing or outside {sorted(labels)}. Missing is unknown, not a direction.", ids),
        }
        for label in sorted(labels):
            payload[label] = {
                "plays": count_metric(_n(values == label), f"Run plays with {column} {label} {subject}.", ids),
                "share_of_runs": rate_metric(_n(values == label), len(runs), f"Share of run plays with {column} {label}. Unknown {noun} stays in the unknown count and is not recoded.", ids),
            }
        return payload

    drive_stats = _drive_stats(frame, ids, subject)
    return {
        "scrimmage_plays": count_metric(len(scr), f"Pass and run plays {subject}. Kneels, spikes, kicks, and no-plays are excluded.", ids),
        "unknown_down_plays": count_metric(_n(down.isna()), f"Scrimmage plays with no down {subject}.", ids),
        "early_down_plays": count_metric(len(early), "Scrimmage plays on down 1 or 2.", ids),
        "early_down_pass_plays": count_metric(early_pass, "Early-down pass plays, including sacks.", ids),
        "early_down_run_plays": count_metric(early_run, "Early-down run plays, including scrambles and excluding kneels.", ids),
        "early_down_pass_rate": rate_metric(early_pass, len(early), "Early-down pass plays divided by early-down scrimmage plays.", ids),
        "early_down_run_rate": rate_metric(early_run, len(early), "Early-down run plays divided by early-down scrimmage plays.", ids),
        "neutral_plays": count_metric(len(neutral), "Scrimmage plays with pre-play score margin from -7 to +7, including ties. Positive means the offense leads.", ids),
        "leading_plays": count_metric(len(leading), "Scrimmage plays with the offense ahead by 8 or more before the snap.", ids),
        "trailing_plays": count_metric(len(trailing), "Scrimmage plays with the offense behind by 8 or more before the snap.", ids),
        "tied_plays": count_metric(len(tied), "Scrimmage plays with the score tied before the snap. These plays are also inside the neutral count.", ids),
        "unknown_score_plays": count_metric(_n(score.isna()), "Scrimmage plays with no pre-play score margin.", ids),
        "neutral_pass_rate": rate_metric(_n(neutral["play_type"] == "pass"), len(neutral), "Pass rate when the pre-play margin is between -7 and +7.", ids),
        "leading_pass_rate": rate_metric(_n(leading["play_type"] == "pass"), len(leading), "Pass rate when the offense leads by 8 or more.", ids),
        "trailing_pass_rate": rate_metric(_n(trailing["play_type"] == "pass"), len(trailing), "Pass rate when the offense trails by 8 or more.", ids),
        "tied_pass_rate": rate_metric(_n(tied["play_type"] == "pass"), len(tied), "Pass rate when the score is tied before the snap.", ids),
        "unknown_distance_plays": count_metric(_n(distance.isna()), "Scrimmage plays with no yards-to-go.", ids),
        "short_yardage_plays": count_metric(len(short), "Scrimmage plays with 2 or fewer yards to go.", ids),
        "long_yardage_plays": count_metric(len(long), "Scrimmage plays with 7 or more yards to go.", ids),
        "short_yardage_pass_rate": rate_metric(_n(short["play_type"] == "pass"), len(short), "Pass rate on scrimmage plays with 2 or fewer yards to go.", ids),
        "long_yardage_pass_rate": rate_metric(_n(long["play_type"] == "pass"), len(long), "Pass rate on scrimmage plays with 7 or more yards to go.", ids),
        "third_down_plays": count_metric(len(third), "Third-down pass, run, kneel, and spike plays. Official gamebook attempts include kneels and spikes. Two-point tries are excluded.", ids),
        "third_down_conversions": count_metric(third_conv, "Those third-down plays with nflverse third_down_converted = 1.", ids),
        "third_down_failures": count_metric(third_fail, "Those third-down plays with nflverse third_down_failed = 1.", ids),
        "third_down_unknown_results": count_metric(third_unknown, "Third-down plays with neither conversion flag. The result is unknown, not a failure.", ids),
        "third_down_conversion_rate": rate_metric(third_conv, len(third), "Third-down conversions divided by third-down pass, run, kneel, and spike plays.", ids),
        "red_zone_plays": count_metric(len(red), "Scrimmage plays with yardline_100 <= 20, the snap at or inside the opponent 20.", ids),
        "unknown_yardline_plays": count_metric(_n(yard.isna()), "Scrimmage plays with no yardline_100. They are not treated as outside the red zone.", ids),
        "red_zone_pass_rate": rate_metric(red_pass, len(red), "Pass rate on red-zone scrimmage plays.", ids),
        "red_zone_touchdown_plays": count_metric(red_td, "Red-zone scrimmage plays with touchdown = 1. This is a play count, not an official red-zone trip.", ids),
        **drive_stats,
        "official_red_zone_trip_efficiency": blocked_field(
            "Official red-zone trip efficiency is printed on gamebooks. It is stored only on the games that were opened, and it is not averaged into a season rate."
        ),
        "explosive_pass_20_plays": count_metric(explosive_pass, "Complete passes with yards_gained >= 20. Derived from play yards. Not an official explosive label.", ids),
        "explosive_pass_20_rate": rate_metric(explosive_pass, len(passes), "Complete passes of 20 or more yards divided by pass plays, including sacks and incompletions.", ids),
        "explosive_rush_10_plays": count_metric(explosive_10, "Run plays with yards_gained >= 10. Derived. Not an official explosive label.", ids),
        "explosive_rush_10_rate": rate_metric(explosive_10, len(runs), "Run plays of 10 or more yards divided by run plays.", ids),
        "explosive_rush_15_plays": count_metric(explosive_15, "Run plays with yards_gained >= 15. Derived. A second threshold already used in this repo's team database, reported separately and not substituted for the 10-yard count.", ids),
        "explosive_rush_15_rate": rate_metric(explosive_15, len(runs), "Run plays of 15 or more yards divided by run plays.", ids),
        "official_explosive_label": blocked_field("Neither the gamebook tables nor nflverse play-by-play carry an official explosive-play label."),
        "sacks": count_metric(sacks, f"Sacks {subject}. A sack is a pass play with sack = 1.", ids),
        "sack_rate": rate_metric(sacks, len(passes), f"Sacks divided by pass plays {subject}.", ids),
        "qb_scrambles": count_metric(len(scrambles), f"Run plays with qb_scramble = 1 {subject}. Designed quarterback runs stay in the run count and are not called scrambles.", ids),
        "qb_scramble_rate": rate_metric(len(scrambles), len(passes) + len(scrambles), "Scrambles divided by pass plays plus scrambles. Kneels are not dropbacks.", ids),
        "qb_kneels": count_metric(len(kneels), "Quarterback kneels. Excluded from scrimmage rates and from carry shares. Included in third-down attempts and in the gamebook rushing comparison.", ids),
        "qb_spikes": count_metric(
            _n((_not_two_point(frame)["play_type"] == "qb_spike")),
            "Quarterback spikes. Excluded from pass-rate denominators. Included in third-down attempts, matching the official gamebook.",
            ids,
        ),
        "two_point_attempts": count_metric(
            _n(pd.to_numeric(frame["two_point_attempt"], errors="coerce") == 1) if "two_point_attempt" in frame.columns else 0,
            "Two-point conversion attempts. Not scrimmage plays, not targets, and not carries. A missing flag is not counted as zero attempts unless the column was scanned.",
            ids,
            scanned="two_point_attempt" in frame.columns,
        ),
        "shotgun_plays": count_metric(shotgun_n, "Scrimmage plays with nflverse shotgun = 1. This is a formation label, not a personnel package.", ids),
        "unknown_shotgun_plays": count_metric(_n(pd.to_numeric(scr["shotgun"], errors="coerce").isna()), "Scrimmage plays with no shotgun flag. They are not counted as under center.", ids),
        "shotgun_rate": rate_metric(shotgun_n, len(shotgun_known), "Shotgun plays divided by scrimmage plays that have a shotgun flag.", ids),
        "rush_direction": direction("run_location", {"left", "right", "middle"}, "direction"),
        "rush_gap": direction("run_gap", {"end", "tackle", "guard"}, "gap"),
    }


def _drive_stats(frame: pd.DataFrame, game_ids: list[str], subject: str) -> dict:
    scr = _scrimmage(frame)
    yard = pd.to_numeric(scr["yardline_100"], errors="coerce")
    drive = pd.to_numeric(scr["fixed_drive"], errors="coerce")
    unknown_plays = scr[yard.notna() & (yard <= 20) & drive.isna()]
    keyed = scr[drive.notna()].copy()
    keyed["_drive"] = pd.to_numeric(keyed["fixed_drive"], errors="coerce")
    keyed["_yard"] = pd.to_numeric(keyed["yardline_100"], errors="coerce")
    keyed["_td"] = pd.to_numeric(keyed["touchdown"], errors="coerce") == 1
    fg = frame[(frame["play_type"] == "field_goal") & (frame["field_goal_result"] == "made")].copy()
    fg_drive = pd.to_numeric(fg["fixed_drive"], errors="coerce")
    fg_known = fg[fg_drive.notna() & fg["posteam"].notna() & fg["game_id"].notna()]
    fg_keys = set(zip(fg_known["game_id"].astype(str), fg_known["posteam"].astype(str), fg_drive[fg_known.index].astype(int)))
    unknown_fg = int(len(fg) - len(fg_known))
    rz = 0
    rz_td = 0
    rz_fg = 0
    if not keyed.empty:
        for (game_id, posteam, drive_id), group in keyed.groupby(["game_id", "posteam", "_drive"], dropna=False):
            if not (group["_yard"].notna() & (group["_yard"] <= 20)).any():
                continue
            rz += 1
            if bool(group["_td"].any()):
                rz_td += 1
            if (str(game_id), str(posteam), int(drive_id)) in fg_keys:
                rz_fg += 1
    return {
        "red_zone_drives": count_metric(rz, f"Drives with a scrimmage snap at or inside the 20 {subject}, keyed by game, posteam, and fixed_drive. Derived, not the official trip count.", game_ids),
        "red_zone_drives_with_touchdown": count_metric(rz_td, "Those derived red-zone drives that also have a scrimmage touchdown.", game_ids),
        "red_zone_drives_with_made_field_goal": count_metric(rz_fg, "Those derived red-zone drives that also have a made field goal on the same drive key.", game_ids),
        "red_zone_drive_touchdown_rate": rate_metric(rz_td, rz, "Derived red-zone drives with a touchdown, divided by derived red-zone drives.", game_ids),
        "unknown_drive_red_zone_plays": count_metric(len(unknown_plays), "Red-zone scrimmage plays with no fixed_drive. They stay in the play count and out of the drive rate.", game_ids),
        "unknown_drive_field_goals": count_metric(unknown_fg, "Made field goals that could not be joined to a drive key. They are not counted as zero red-zone field goals.", game_ids),
    }


def aggregate_phase(plays: pd.DataFrame, team: str, phase: str, game_ids: list[str]) -> dict:
    return {
        "offense": aggregate_side(plays, team, "offense", phase, game_ids),
        "defense": aggregate_side(plays, team, "defense", phase, game_ids),
    }


def trends_for(plays: pd.DataFrame, team: str, game_ids: list[str]) -> dict:
    def window_ids(n: int) -> list[str]:
        return game_ids[-n:] if len(game_ids) >= n else list(game_ids)

    def earlier_ids(n: int) -> list[str]:
        return game_ids[:-n] if len(game_ids) > n else []

    def pass_rate(ids: list[str]) -> dict:
        if not ids:
            return rate_metric(0, 0, "Early-down pass rate. No earlier games were scanned.", [])
        return aggregate_side(plays[plays["game_id"].isin(ids)], team, "offense", "regulation", ids)["early_down_pass_rate"]

    payload = {}
    for label, n in (("last_5", 5), ("last_8", 8)):
        recent = window_ids(n)
        prior = earlier_ids(n)
        recent_rate = pass_rate(recent)
        prior_rate = pass_rate(prior)
        payload[label] = {
            "games": len(recent),
            "requested_games": n,
            "status": "COMPLETE" if len(game_ids) >= n else "PARTIAL",
            "game_ids": recent,
            "earlier_games": len(prior),
            "earlier_game_ids": prior,
            "early_down_pass_rate": recent_rate,
            "earlier_early_down_pass_rate": prior_rate,
            "early_down_pass_rate_difference": difference_metric(
                recent_rate, prior_rate,
                f"Early-down pass rate in the last {n} games minus the rate in earlier completed games. Unknown when the earlier sample is empty.",
                recent + prior,
            ),
        }
    return payload


def build_team_profile(plays: pd.DataFrame, team: str, game_rows: list[dict], checks: dict[str, dict]) -> dict:
    mine = [row for row in game_rows if team in (row["away_team"], row["home_team"]) and row["included_in_profiles"]]
    mine.sort(key=lambda row: (row["game_date"], row["week"], row["game_id"]))
    game_ids = [row["game_id"] for row in mine]
    byes = sorted(set(range(1, LAST_COMPLETED_WEEK + 1)) - {int(row["week"]) for row in mine if int(row["week"]) <= LAST_COMPLETED_WEEK})
    season_players = player_window(plays, team, game_ids, len(game_ids) or 1)
    season_players["status"] = "COMPLETE" if game_ids else "PARTIAL"
    season_players["requested_games"] = len(game_ids)
    offense_all = _not_two_point(plays[(plays["posteam"] == team) & (plays["game_id"].isin(game_ids))])
    season_players["unassigned_pass_plays"] = _fix_unassigned_passes(offense_all, game_ids)
    last_5 = player_window(plays, team, game_ids, 5)
    last_8 = player_window(plays, team, game_ids, 8)
    team_checks = []
    for row in mine:
        check = checks.get(row["game_id"])
        if check is None:
            team_checks.append({
                "game_id": row["game_id"],
                "status": "NOT_PERSISTED",
                "source_url": row["gamebook"]["source_url"],
                "fields": ["gamebook PDF not downloaded; play-level evidence is nflverse only"],
            })
        else:
            team_checks.append({
                "game_id": row["game_id"],
                "status": "VERIFIED_NOT_PERSISTED" if check["persisted_in_repo"] is False and check["status"] == "MATCH" else check["status"],
                "source_url": check["source_url"],
                "fields": check["disagreement_fields"],
            })
    reasons = [
        "Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are BLOCKED.",
        "Official gamebook PDFs are persisted for Week 9 only. Other weeks cite the Game Center URL and were not stored.",
        "Opportunity counts are regulation nflverse pass and run plays. Overtime is a separate block. Kneels are not carries.",
        "Explosive counts are derived from yards_gained. There is no official explosive label.",
    ]
    disagreements = [item["game_id"] for item in team_checks if item["status"] == "DISAGREEMENT"]
    if disagreements:
        reasons.append("Gamebook cross-check disagreed on " + ", ".join(disagreements) + ". Profile counts stay on the nflverse play ids and do not absorb the unmatched book rows.")
    return {
        "schema_version": "scheme_opportunity_profile/1",
        "projection_ready": False,
        "research_only": True,
        "team": team,
        "repo_alias": REPO_ALIAS.get(team, team),
        "season": 2026,
        "season_type": "REG",
        "profile_status": "PARTIAL",
        "opportunity_status": "COMPLETE" if game_ids else "BLOCKED",
        "gamebook_status": "PARTIAL",
        "scheme_charting_status": "BLOCKED",
        "status_reasons": reasons,
        "window": {
            "last_completed_week": LAST_COMPLETED_WEEK,
            "games": len(game_ids),
            "game_ids": game_ids,
            "last_game_id": game_ids[-1],
            "last_game_date": mine[-1]["game_date"],
            "bye_weeks_before_last_completed_week": byes,
        },
        "sources": source_list(),
        "blocked": blocked_group(),
        "gamebook_checks": team_checks,
        "regulation": aggregate_phase(plays, team, "regulation", game_ids),
        "overtime": aggregate_phase(plays, team, "overtime", game_ids),
        "players": {"season": season_players, "last_5": last_5, "last_8": last_8},
        "trends": trends_for(plays, team, game_ids),
        "evidence_file": EVIDENCE_REL,
        "generated_utc": GENERATED_UTC,
    }


def source_list() -> list[dict]:
    return [
        {
            "name": "nflverse_play_by_play_2026",
            "url": PBP_URL,
            "sha256": PBP_SHA,
            "retrieved_utc": PBP_RETRIEVED,
            "note": (
                f"HTTP last-modified {PBP_LAST_MODIFIED}. Week 1-9 play counts and yards sums match "
                f"{PINNED_PBP} sha256 {PINNED_PBP_SHA} retrieved {PINNED_PBP_RETRIEVED}. "
                "This pull adds the final week-10 game only."
            ),
        },
        {
            "name": "nflverse_schedule_2026",
            "url": SCHEDULE_URL,
            "sha256": SCHEDULE_SHA,
            "retrieved_utc": SCHEDULE_RETRIEVED,
            "note": "Scores and game identity only. Spread, total, and moneyline columns were not read.",
        },
        {
            "name": "nflverse_license",
            "url": NFLVERSE_LICENSE,
            "sha256": None,
            "retrieved_utc": PBP_RETRIEVED,
            "note": "Public nflverse-data release. Redistribution follows that license.",
        },
        {
            "name": "nfl_game_books_help",
            "url": NFL_GAMEBOOK_HELP,
            "sha256": None,
            "retrieved_utc": LINKS_RETRIEVED,
            "note": "NFL confirms Game Book PDFs are linked from Game Center recap tabs.",
        },
    ]


def load_schedule(path: Path) -> pd.DataFrame:
    if sha256_file(path) != SCHEDULE_SHA:
        raise SystemExit(f"schedule sha256 does not match the recorded pull: {path}")
    frame = pd.read_csv(path, usecols=SCHEDULE_COLUMNS)
    frame = frame[(frame["season"] == 2026) & (frame["game_type"] == "REG")].copy()
    return frame


def load_pbp(path: Path) -> pd.DataFrame:
    if sha256_file(path) != PBP_SHA:
        raise SystemExit(f"play-by-play sha256 does not match the recorded pull: {path}")
    frame = pd.read_parquet(path, columns=PBP_COLUMNS)
    frame = frame[frame["season_type"] == "REG"].copy()
    frame["play_id"] = pd.to_numeric(frame["play_id"], errors="coerce").astype("Int64")
    frame["game_date"] = pd.to_datetime(frame["game_date"]).dt.strftime("%Y-%m-%d")
    keep = frame["play_type"].isin(["pass", "run", "qb_kneel", "qb_spike", "field_goal"])
    return frame.loc[keep, EVIDENCE_COLUMNS].reset_index(drop=True)


def completed_game_rows(schedule: pd.DataFrame, links: dict[str, dict], local_books: dict[str, dict]) -> list[dict]:
    rows = []
    for record in schedule.sort_values(["week", "gameday", "game_id"]).to_dict(orient="records"):
        scored = pd.notna(record["away_score"]) and pd.notna(record["home_score"])
        week = int(record["week"])
        game_id = str(record["game_id"])
        included = bool(scored and (week <= LAST_COMPLETED_WEEK or game_id == WEEK10_GAME))
        if scored and week > LAST_COMPLETED_WEEK and game_id != WEEK10_GAME:
            raise SystemExit(f"unexpected final game outside the reviewed window: {game_id}")
        link = links.get(game_id, {})
        local = local_books.get(game_id)
        pdf_url = link.get("pdf_url")
        if local:
            gamebook = {
                "status": "LOCAL_OWNER_SUPPLIED",
                "source_url": local["source_url"],
                "live_source_url": pdf_url,
                "sha256": local["pdf_sha256"],
                "retrieved_utc": "2026-11-10T05:32:00Z",
                "retrieved_note": "Owner provenance says fetched about 12:32 AM ET on 2026-11-10. The timestamp is approximate.",
                "persisted_in_repo": True,
                "rights_status": "NFL_MEDIA_ASSISTANCE_ONLY",
            }
        elif game_id == WEEK10_GAME:
            gamebook = {
                "status": "VERIFIED_NOT_PERSISTED",
                "source_url": WEEK10_PDF_URL,
                "live_source_url": pdf_url,
                "sha256": WEEK10_PDF_SHA,
                "retrieved_utc": WEEK10_PDF_RETRIEVED,
                "persisted_in_repo": False,
                "rights_status": "NFL_MEDIA_ASSISTANCE_ONLY",
            }
        else:
            gamebook = {
                "status": "REFERENCED_NOT_PERSISTED" if pdf_url else "URL_MISSING",
                "source_url": pdf_url,
                "live_source_url": pdf_url,
                "sha256": None,
                "retrieved_utc": LINKS_RETRIEVED if pdf_url else None,
                "persisted_in_repo": False,
                "rights_status": "NOT_DOWNLOADED",
            }
        rows.append({
            "game_id": game_id,
            "season": 2026,
            "season_type": "REG",
            "week": week,
            "game_date": str(record["gameday"]),
            "weekday": record.get("weekday"),
            "away_team": record["away_team"],
            "home_team": record["home_team"],
            "away_score": None if not scored else int(record["away_score"]),
            "home_score": None if not scored else int(record["home_score"]),
            "final": bool(scored),
            "in_last_completed_week_or_earlier": week <= LAST_COMPLETED_WEEK,
            "included_in_profiles": included,
            "game_center_url": game_center_url(record["away_team"], record["home_team"], week),
            "game_center_http_status": link.get("http_status"),
            "game_center_retrieved_utc": LINKS_RETRIEVED if link else None,
            "gamebook": gamebook,
            "exclusion_reason": None if included else (
                "no final score in the schedule pull" if not scored else "outside the reviewed final-game set"
            ),
        })
    included = [row for row in rows if row["included_in_profiles"]]
    if not included:
        raise SystemExit("no completed games")
    if max(row["game_date"] for row in included) > LAST_PROFILE_DATE:
        raise SystemExit("a profile game is after the recorded cutoff date")
    week10 = [row["game_id"] for row in included if row["week"] == 10]
    if week10 != [WEEK10_GAME]:
        raise SystemExit(f"week 10 profile games must be only {WEEK10_GAME}, got {week10}")
    return rows


def map_abbr(abbr: str) -> str:
    mapped = GAMEBOOK_ABBR.get(abbr, abbr)
    if mapped not in TEAMS:
        raise ValueError(f"unmapped gamebook abbreviation {abbr}")
    return mapped


def _false(value) -> bool:
    return value in (False, "false", "False", 0, "0")


def _num(value):
    if value is None or value == "":
        return None
    return int(float(value))


def _norm_name(value: str) -> str:
    return " ".join(str(value).replace("\u00a0", " ").split())


def load_week9_local() -> dict[str, dict]:
    books = {}
    for folder in sorted(path for path in WEEK9_DIR.iterdir() if (path / "parsed").is_dir()):
        provenance = json.loads((folder / "provenance.json").read_text())
        pdf = folder / provenance["pdf_file"]
        digest = sha256_file(pdf)
        if digest != provenance["pdf_sha256"]:
            raise SystemExit(f"local gamebook hash mismatch for {folder.name}")
        if COPYRIGHT not in provenance.get("copyright_notice", ""):
            raise SystemExit(f"copyright notice missing for {folder.name}")
        tables = {}
        for name in ("game_meta", "team_stats", "rushing", "receiving"):
            with (folder / "parsed" / f"{name}.csv").open(newline="", encoding="utf-8") as handle:
                tables[name] = list(csv.DictReader(handle))
        books[folder.name] = {
            "tables": tables,
            "source_url": provenance["source_url"],
            "pdf_sha256": digest,
            "persisted_in_repo": True,
            "retrieved_utc": "2026-11-10T05:32:00Z",
        }
    return books


def load_week10_tables(text_path: Path) -> dict:
    if str(GAMEBOOK_PARSER) not in sys.path:
        sys.path.insert(0, str(GAMEBOOK_PARSER))
    from parse_nfl_game_summary import parse_game_summary
    text = text_path.read_text(encoding="utf-8")
    if "prohibited without the written permission" not in text:
        raise SystemExit("week 10 gamebook text is missing the NFL usage restriction")
    tables = parse_game_summary(text, game_id=WEEK10_GAME, week=10)
    return {
        "tables": tables,
        "source_url": WEEK10_PDF_URL,
        "pdf_sha256": WEEK10_PDF_SHA,
        "persisted_in_repo": False,
        "retrieved_utc": WEEK10_PDF_RETRIEVED,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def _stat(tables, name: str, scope: str = "final") -> dict | None:
    for row in tables["team_stats"]:
        if row.get("stat") == name and row.get("scope") == scope:
            return row
    return None


def _eff(text: str) -> tuple[int, int]:
    match = EFF_RE.match(str(text).strip())
    if not match:
        raise ValueError(f"unparsed efficiency {text!r}")
    made, attempts, pct = int(match.group(1)), int(match.group(2)), float(match.group(3))
    if attempts and abs((made / attempts) * 100 - pct) > 0.2:
        raise ValueError(f"printed efficiency does not match its own fraction: {text}")
    return made, attempts


def crosscheck_game_full(game_id: str, book: dict, evidence: pd.DataFrame, score_row: dict) -> dict:
    tables = book["tables"]
    meta = tables["game_meta"][0]
    away = map_abbr(meta["visitor_abbr"])
    home = map_abbr(meta["home_abbr"])
    if away != score_row["away_team"] or home != score_row["home_team"]:
        raise ValueError(f"{game_id} gamebook teams do not match the schedule")
    game = evidence[evidence["game_id"] == game_id]
    diffs = []

    def add(field: str, book_value, pbp_value):
        if book_value != pbp_value:
            diffs.append({"field": field, "gamebook": book_value, "nflverse": pbp_value})

    add("away_score", _num(meta["visitor_final"]), score_row["away_score"])
    add("home_score", _num(meta["home_final"]), score_row["home_score"])

    third = _stat(tables, "THIRD DOWN EFFICIENCY")
    if third is None:
        diffs.append({"field": "third_down", "gamebook": "missing", "nflverse": "present"})
    else:
        for side, team, cell in (("away", away, third["visitor"]), ("home", home, third["home"])):
            made, attempts = _eff(cell)
            rows = _not_two_point(game)
            rows = rows[(rows["posteam"] == team) & (pd.to_numeric(rows["down"], errors="coerce") == 3) & rows["play_type"].isin(["pass", "run", "qb_kneel", "qb_spike"])]
            converted = _n(pd.to_numeric(rows["third_down_converted"], errors="coerce") == 1)
            add(f"third_down_{side}", {"made": made, "attempts": attempts}, {"made": converted, "attempts": int(len(rows))})

    sack_row = _stat(tables, "Times thrown - yards lost attempting to pass")
    if sack_row is not None:
        for side, team, cell in (("away", away, sack_row["visitor"]), ("home", home, sack_row["home"])):
            match = SACK_RE.match(str(cell).strip())
            book_sacks = int(match.group(1)) if match else None
            pbp_sacks = _n((game["posteam"] == team) & (game["play_type"] == "pass") & (pd.to_numeric(game["sack"], errors="coerce") == 1))
            add(f"sacks_{side}", book_sacks, pbp_sacks)

    play_row = _stat(tables, "Total Offensive Plays (inc. times thrown passing)")
    if play_row is not None:
        for side, team, cell in (("away", away, play_row["visitor"]), ("home", home, play_row["home"])):
            scoped = _not_two_point(game)
            pbp_plays = _n((scoped["posteam"] == team) & scoped["play_type"].isin(["pass", "run", "qb_kneel", "qb_spike"]))
            add(f"offensive_plays_{side}", _num(cell), pbp_plays)

    book_rush: Counter[tuple[str, str]] = Counter()
    for row in tables["rushing"]:
        if row.get("scope") != "final" or not _false(row.get("is_total")):
            continue
        book_rush[(map_abbr(row["team_abbr"]), _norm_name(row["player"]))] += _num(row["att"]) or 0
    pbp_rush: Counter[tuple[str, str]] = Counter()
    rush_rows = _not_two_point(game)
    rush_rows = rush_rows[rush_rows["play_type"].isin(["run", "qb_kneel"]) & rush_rows["rusher_player_name"].notna()]
    for _, row in rush_rows.iterrows():
        pbp_rush[(row["posteam"], _norm_name(row["rusher_player_name"]))] += 1
    rush_keys = sorted(set(book_rush) | set(pbp_rush))
    rush_diffs = [
        {"team": team, "player": player, "gamebook_attempts_including_kneels": book_rush[(team, player)], "nflverse_runs_plus_kneels": pbp_rush[(team, player)]}
        for team, player in rush_keys
        if book_rush[(team, player)] != pbp_rush[(team, player)]
    ]
    if rush_diffs:
        diffs.append({"field": "rushing_attempts_including_kneels", "rows": rush_diffs})

    book_targets: Counter[tuple[str, str]] = Counter()
    for row in tables["receiving"]:
        if row.get("scope") != "final" or not _false(row.get("is_total")):
            continue
        targets = _num(row.get("tar"))
        if not targets:
            continue
        book_targets[(map_abbr(row["team_abbr"]), _norm_name(row["player"]))] += targets
    pbp_targets: Counter[tuple[str, str]] = Counter()
    target_rows = _not_two_point(game)
    target_rows = target_rows[(target_rows["play_type"] == "pass") & (pd.to_numeric(target_rows["sack"], errors="coerce") != 1) & target_rows["receiver_player_name"].notna()]
    for _, row in target_rows.iterrows():
        pbp_targets[(row["posteam"], _norm_name(row["receiver_player_name"]))] += 1
    target_keys = sorted(set(book_targets) | set(pbp_targets))
    target_diffs = [
        {"team": team, "player": player, "gamebook_targets": book_targets[(team, player)], "nflverse_targets": pbp_targets[(team, player)]}
        for team, player in target_keys
        if book_targets[(team, player)] != pbp_targets[(team, player)]
    ]
    if target_diffs:
        diffs.append({"field": "targets", "rows": target_diffs})

    status = "MATCH" if not diffs else "DISAGREEMENT"
    return {
        "game_id": game_id,
        "away_team": away,
        "home_team": home,
        "status": status,
        "persisted_in_repo": book["persisted_in_repo"],
        "source_url": book["source_url"],
        "sha256": book["pdf_sha256"],
        "retrieved_utc": book["retrieved_utc"],
        "rights_status": "NFL_MEDIA_ASSISTANCE_ONLY",
        "persisted_pdf": book["persisted_in_repo"],
        "disagreement_fields": [item["field"] for item in diffs],
        "disagreements": diffs,
        "definition_notes": [
            "Gamebook rushing attempts include quarterback kneels. The nflverse side of this check is play_type run plus qb_kneel.",
            "Gamebook final third-down efficiency includes overtime, kneels, and spikes. This check uses every quarter, not the regulation-only profile rate.",
            "Two-point conversion attempts are excluded on both sides of the rushing, target, and offensive-play checks.",
            "Profile opportunity rates exclude kneels and overtime. A match here does not copy gamebook totals into those rates.",
        ],
    }


def compare_pinned_weeks(pbp_path: Path) -> dict:
    pinned = REPO / PINNED_PBP
    if sha256_file(pinned) != PINNED_PBP_SHA:
        raise SystemExit("pinned week 1-9 play-by-play hash changed")
    old = pd.read_parquet(pinned, columns=["game_id", "week", "yards_gained"])
    new = pd.read_parquet(pbp_path, columns=["game_id", "week", "yards_gained"])
    old = old[old["week"] <= LAST_COMPLETED_WEEK]
    new = new[new["week"] <= LAST_COMPLETED_WEEK]
    old_counts = old.groupby("game_id").size()
    new_counts = new.groupby("game_id").size()
    old_yards = old.groupby("game_id")["yards_gained"].sum()
    new_yards = new.groupby("game_id")["yards_gained"].sum()
    same_counts = bool(old_counts.equals(new_counts))
    same_yards = bool(old_yards.sort_index().round(6).equals(new_yards.sort_index().round(6)))
    if not (same_counts and same_yards):
        raise SystemExit("week 1-9 play-by-play no longer matches the pinned file; refusing to mix vintages")
    return {
        "pinned_file": PINNED_PBP,
        "pinned_sha256": PINNED_PBP_SHA,
        "pinned_retrieved_utc": PINNED_PBP_RETRIEVED,
        "week_1_9_play_counts_match": same_counts,
        "week_1_9_yards_match": same_yards,
        "week_1_9_games": int(new["game_id"].nunique()),
    }


def write_evidence(plays: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = plays.copy()
    frame["play_id"] = frame["play_id"].astype(int)
    frame.to_csv(path, index=False, compression="gzip")


def load_evidence(path: Path | None = None) -> pd.DataFrame:
    frame = pd.read_csv(path or (OUT_DIR / "evidence_plays.csv.gz"))
    frame["game_id"] = frame["game_id"].astype(str)
    frame["play_id"] = frame["play_id"].astype(int)
    for column in ("posteam", "defteam", "rusher_player_name", "receiver_player_name", "run_location", "run_gap", "field_goal_result"):
        if column in frame.columns:
            frame[column] = frame[column].astype("string")
    return frame


def _fmt_metric(metric: dict) -> str:
    if not isinstance(metric, dict) or "value" not in metric:
        return ""
    if metric["value"] == "unknown":
        return "unknown"
    if metric.get("kind") == "rate" and metric.get("denominator"):
        pct = 100 * metric["numerator"] / metric["denominator"]
        return f"{pct:.1f}% ({metric['numerator']}/{metric['denominator']})"
    if metric.get("kind") == "rate_difference":
        return f"{metric['value']:+.3f}"
    return str(metric["value"])


def render_team_md(profile: dict) -> str:
    team = profile["team"]
    reg = profile["regulation"]["offense"]
    defense = profile["regulation"]["defense"]
    ot = profile["overtime"]["offense"]
    lines = [
        f"# {team} scheme and opportunity profile, 2026",
        "",
        f"{NAMES[team]}. Research only. projection_ready is false. This file does not change model weights or formulas.",
        "",
        f"Overall status: {profile['profile_status']}. Opportunity evidence: {profile['opportunity_status']}. "
        f"Gamebooks: {profile['gamebook_status']}. Scheme charting: {profile['scheme_charting_status']}.",
        "",
        "## Window",
        "",
        f"{profile['window']['games']} completed games, last game {profile['window']['last_game_id']} on {profile['window']['last_game_date']}. "
        f"Last fully completed week is {profile['window']['last_completed_week']}. "
        f"Bye weeks inside weeks 1-9: {profile['window']['bye_weeks_before_last_completed_week'] or 'none'}.",
        "",
        "Game ids: " + ", ".join(profile["window"]["game_ids"]) + ".",
        "",
        "## Blocked fields",
        "",
        "Route concepts, coverage shells, man/zone, blocking assignments, player matchups, and personnel packages are unknown. "
        "A shotgun flag is a formation label and is reported below. It is not a personnel package. "
        "Tacklers in the play-by-play are not coverage assignments.",
        "",
        "## Offense, regulation",
        "",
        f"Scrimmage plays: {_fmt_metric(reg['scrimmage_plays'])}. Early-down pass rate: {_fmt_metric(reg['early_down_pass_rate'])}. "
        f"Early-down run rate: {_fmt_metric(reg['early_down_run_rate'])}.",
        f"Neutral pass rate (margin -7 to +7): {_fmt_metric(reg['neutral_pass_rate'])}. "
        f"Leading by 8+: {_fmt_metric(reg['leading_pass_rate'])}. Trailing by 8+: {_fmt_metric(reg['trailing_pass_rate'])}. "
        f"Tied: {_fmt_metric(reg['tied_pass_rate'])}.",
        f"Short-yardage pass rate (1st-and-2 or fewer yards, any down): {_fmt_metric(reg['short_yardage_pass_rate'])}. "
        f"Long-yardage pass rate (7+ yards to go): {_fmt_metric(reg['long_yardage_pass_rate'])}.",
        f"Third down: {_fmt_metric(reg['third_down_conversion_rate'])}. "
        f"Unknown third-down results: {_fmt_metric(reg['third_down_unknown_results'])}.",
        f"Red-zone plays: {_fmt_metric(reg['red_zone_plays'])}. Red-zone pass rate: {_fmt_metric(reg['red_zone_pass_rate'])}. "
        f"Derived red-zone drive touchdown rate: {_fmt_metric(reg['red_zone_drive_touchdown_rate'])}. "
        f"Official red-zone trip efficiency: unknown.",
        f"Derived explosives: pass 20+ {_fmt_metric(reg['explosive_pass_20_rate'])}; rush 10+ {_fmt_metric(reg['explosive_rush_10_rate'])}; "
        f"rush 15+ {_fmt_metric(reg['explosive_rush_15_rate'])}. Official explosive label: unknown.",
        f"Sacks taken: {_fmt_metric(reg['sacks'])}. Scrambles: {_fmt_metric(reg['qb_scrambles'])} "
        f"({_fmt_metric(reg['qb_scramble_rate'])} of dropbacks). Kneels, excluded from carries: {_fmt_metric(reg['qb_kneels'])}.",
        f"Shotgun rate, where the flag is present: {_fmt_metric(reg['shotgun_rate'])}. "
        f"Plays with no shotgun flag: {_fmt_metric(reg['unknown_shotgun_plays'])}.",
        "Rush direction counts (unknown is not folded into left, right, or middle): "
        + ", ".join(
            f"{label} {_fmt_metric(reg['rush_direction'][label]['plays'])}"
            for label in ("left", "middle", "right")
        )
        + f", unknown {_fmt_metric(reg['rush_direction']['unknown'])}.",
        "",
        "## Defense, regulation",
        "",
        f"Scrimmage plays faced: {_fmt_metric(defense['scrimmage_plays'])}. Early-down pass rate allowed: {_fmt_metric(defense['early_down_pass_rate'])}.",
        f"Third down allowed: {_fmt_metric(defense['third_down_conversion_rate'])}. "
        f"Sacks recorded: {_fmt_metric(defense['sacks'])}. Scrambles allowed: {_fmt_metric(defense['qb_scrambles'])}.",
        f"Explosive passes allowed (20+): {_fmt_metric(defense['explosive_pass_20_rate'])}. "
        f"Explosive rushes allowed (10+): {_fmt_metric(defense['explosive_rush_10_rate'])}.",
        "",
        "## Overtime",
        "",
        f"Offensive scrimmage plays: {_fmt_metric(ot['scrimmage_plays'])}. "
        f"Early-down pass rate: {_fmt_metric(ot['early_down_pass_rate'])}. "
        "A rate with no overtime plays is unknown, not zero.",
        "",
        "## Recent games",
        "",
    ]
    last_5 = profile["trends"]["last_5"]
    last_8 = profile["trends"]["last_8"]
    lines.append(
        f"Last 5 early-down pass rate: {_fmt_metric(last_5['early_down_pass_rate'])} "
        f"across {last_5['games']} games ({last_5['status']}). "
        f"Earlier games: {_fmt_metric(last_5['earlier_early_down_pass_rate'])}. "
        f"Difference: {_fmt_metric(last_5['early_down_pass_rate_difference'])}."
    )
    lines.append(
        f"Last 8 early-down pass rate: {_fmt_metric(last_8['early_down_pass_rate'])} "
        f"across {last_8['games']} games. Difference versus earlier: {_fmt_metric(last_8['early_down_pass_rate_difference'])}."
    )
    lines.extend(["", "## Player opportunity", ""])
    lines.append("Shares use players who have at least one target or carry in the window. A missing player is omitted, not listed at zero.")
    lines.append("")
    lines.append("| Player | Targets | Target share | Games |")
    lines.append("| --- | ---: | ---: | ---: |")
    for row in profile["players"]["season"]["targets"][:8]:
        lines.append(f"| {row['player_name']} | {row['plays']} | {row['share']:.3f} | {row['games']} |")
    lines.append("")
    lines.append("| Player | Carries | Carry share | Games |")
    lines.append("| --- | ---: | ---: | ---: |")
    for row in profile["players"]["season"]["carries"][:5]:
        lines.append(f"| {row['player_name']} | {row['plays']} | {row['share']:.3f} | {row['games']} |")
    lines.extend(["", "## Gamebook checks", ""])
    for check in profile["gamebook_checks"]:
        if check["status"] == "NOT_PERSISTED":
            continue
        fields = ", ".join(check["fields"]) if check["fields"] else "score, third down, sacks, plays, rushes including kneels, and targets matched"
        lines.append(f"- {check['game_id']}: {check['status']}. {fields} Source: {check['source_url']}")
    lines.extend([
        "",
        "Weeks without a persisted or opened gamebook are not given book-derived counts.",
        "",
        "## Sources",
        "",
        f"Play-by-play: {PBP_URL} retrieved {PBP_RETRIEVED}, sha256 `{PBP_SHA}`.",
        f"Evidence rows: `{EVIDENCE_REL}`. Every count above is the numerator of those rows.",
        "",
    ])
    return "\n".join(lines)


def render_verified_batch(checks: dict[str, dict], profiles: dict[str, dict]) -> str:
    lines = [
        "# Verified batch: Washington and the New York Giants",
        "",
        "This batch was cross-checked before the other 30 team profiles were written. Research only. projection_ready is false.",
        "",
        "Their most recent completed game is 2026-11-12, Commanders at Giants, final 24-21. "
        "Week 10 is not a completed week: the schedule pull has a final score for this game only, and the Sunday and Monday games are unplayed. "
        "Those unplayed games are excluded. Their previous completed games are Rams at Commanders and Giants at Eagles, both 2026-11-08, with owner-supplied Week 9 gamebooks already in the repo.",
        "",
        f"The Week 10 PDF was downloaded, hashed (`{WEEK10_PDF_SHA}`), parsed, and compared. It was not committed. {COPYRIGHT}",
        "",
    ]
    for game_id in (WEEK10_GAME, "2026_09_LA_WAS", "2026_09_NYG_PHI"):
        check = checks[game_id]
        lines.append(f"## {game_id}")
        lines.append("")
        stored = "stored in the repo" if check["persisted_in_repo"] else "not stored"
        lines.append(
            f"Status: {check['status']}. Away {check['away_team']}, home {check['home_team']}. "
            f"Gamebook PDF: {stored}. Retrieved {check['retrieved_utc']}."
        )
        lines.append(f"Source: {check['source_url']}")
        if check["disagreements"]:
            lines.append("")
            lines.append("Disagreements, left on the record. Profile counts were not edited to absorb them:")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(check["disagreements"], indent=2))
            lines.append("```")
        else:
            lines.append("")
            lines.append("Score, third down, sacks, offensive plays, rushing attempts including kneels, and targets match.")
        lines.append("")
    for team in ("WAS", "NYG"):
        profile = profiles[team]
        reg = profile["regulation"]["offense"]
        lines.append(f"## {team} regulation opportunity after the check")
        lines.append("")
        lines.append(
            f"Games in the profile: {profile['window']['games']}. Last game {profile['window']['last_game_id']}. "
            f"Early-down pass rate {_fmt_metric(reg['early_down_pass_rate'])}. "
            f"Third down {_fmt_metric(reg['third_down_conversion_rate'])}. "
            f"Scheme fields: unknown."
        )
        lines.append("")
    lines.append("The league profiles use the same definitions and the same play-by-play pull.")
    lines.append("")
    return "\n".join(lines)


def render_coverage(rows: list[dict], checks: dict[str, dict], profiles: dict[str, dict], pinned: dict) -> str:
    included = [row for row in rows if row["included_in_profiles"]]
    excluded = [row for row in rows if not row["included_in_profiles"]]
    complete_opportunity = sum(1 for profile in profiles.values() if profile["opportunity_status"] == "COMPLETE")
    complete_scheme = sum(1 for profile in profiles.values() if profile["scheme_charting_status"] == "COMPLETE")
    overall_complete = sum(1 for profile in profiles.values() if profile["profile_status"] == "COMPLETE")
    lines = [
        "# 2026 scheme and opportunity coverage",
        "",
        "Research only. projection_ready is false. No model weight or formula was changed, and no scheduled refresh was added.",
        "",
        render_verified_batch(checks, profiles),
        "## League coverage",
        "",
        f"Opportunity profiles with a play-level row for every included final game: {complete_opportunity} of 32.",
        f"Fully complete scheme profiles: {complete_scheme} of 32. Overall profile_status COMPLETE: {overall_complete} of 32.",
        "All 32 are PARTIAL. The blocked scheme fields are unknown for every team, and official gamebooks are not persisted for every completed game.",
        "",
        f"Included final games: {len(included)}. Last fully completed week: {LAST_COMPLETED_WEEK}. "
        f"Excluded scheduled games with no final score, or outside this review: {len(excluded)}.",
        "",
        "| Team | Games | Last game | Opportunity | Gamebook | Scheme |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]
    for team in TEAMS:
        profile = profiles[team]
        lines.append(
            f"| {team} | {profile['window']['games']} | {profile['window']['last_game_id']} | "
            f"{profile['opportunity_status']} | {profile['gamebook_status']} | {profile['scheme_charting_status']} |"
        )
    opened = sorted(checks)
    match_n = sum(1 for check in checks.values() if check["status"] == "MATCH")
    lines.extend([
        "",
        "## Gaps",
        "",
        f"Gamebooks opened and compared: {len(opened)} ({match_n} matched on the checked fields). "
        "Week 9 PDFs were already in the repo. The Week 10 Commanders-Giants PDF was hashed and not committed. "
        "Weeks 1-8 and the unplayed Week 10 games were not downloaded.",
        "",
        "Blocked on every team: route concepts, coverage shells, man/zone, blocking assignments, player matchups, personnel packages, official explosive label, official season red-zone trip efficiency.",
        "",
        "Rush gap is partial: nflverse `run_gap` is often blank. Blank gaps stay in the unknown count.",
        "",
        f"Week 1-9 of this play-by-play pull matches `{pinned['pinned_file']}` "
        f"(sha256 `{pinned['pinned_sha256']}`, retrieved {pinned['pinned_retrieved_utc']}) "
        f"on play counts and yards sums across {pinned['week_1_9_games']} games.",
        "",
        "## Sources",
        "",
        f"- Play-by-play: {PBP_URL} retrieved {PBP_RETRIEVED}, sha256 `{PBP_SHA}`.",
        f"- Schedule identity and final scores: {SCHEDULE_URL} retrieved {SCHEDULE_RETRIEVED}, sha256 `{SCHEDULE_SHA}`. Odds columns were not read.",
        f"- Game Center pages, retrieved {LINKS_RETRIEVED}, used to record each game's Game Book PDF URL. Help page: {NFL_GAMEBOOK_HELP}.",
        f"- Week 9 local PDFs under `data/gamebooks/2026/wk09/`, owner ingest about 12:32 AM ET on 2026-11-10. Hashes were rechecked against each `provenance.json`.",
        f"- Week 10 PDF {WEEK10_PDF_URL} retrieved {WEEK10_PDF_RETRIEVED}, sha256 `{WEEK10_PDF_SHA}`, not stored.",
        f"- License: {NFLVERSE_LICENSE}.",
        "",
        COPYRIGHT,
        "",
        "Generated " + GENERATED_UTC + ".",
        "",
    ])
    return "\n".join(lines)


def load_links(path: Path) -> dict[str, dict]:
    rows = json.loads(path.read_text())
    urls = own_gamebook_urls(rows)
    by_id = {row["game_id"]: row for row in rows}
    for game_id, url in urls.items():
        by_id[game_id]["pdf_url"] = url
    return by_id


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pbp", type=Path, required=True)
    parser.add_argument("--schedule", type=Path, required=True)
    parser.add_argument("--links", type=Path, required=True)
    parser.add_argument("--week10-text", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    args = parser.parse_args(argv)

    pinned = compare_pinned_weeks(args.pbp)
    schedule = load_schedule(args.schedule)
    links = load_links(args.links)
    local = load_week9_local()
    week10 = load_week10_tables(args.week10_text)
    books = dict(local)
    books[WEEK10_GAME] = week10
    evidence = load_pbp(args.pbp)
    rows = completed_game_rows(schedule, links, local)
    included_ids = {row["game_id"] for row in rows if row["included_in_profiles"]}
    evidence_ids = set(evidence["game_id"].astype(str))
    if evidence_ids != included_ids:
        missing = sorted(included_ids - evidence_ids)
        extra = sorted(evidence_ids - included_ids)
        raise SystemExit(f"evidence games do not match final games. missing={missing[:5]} extra={extra[:5]}")
    if evidence["game_date"].max() > LAST_PROFILE_DATE:
        raise SystemExit("evidence contains a game after the cutoff")
    score_index = {row["game_id"]: row for row in rows}
    # Schedule scores must match the end-of-game totals on the full pull. Evidence rows do not carry the total.
    full_scores = pd.read_parquet(args.pbp, columns=["game_id", "season_type", "total_home_score", "total_away_score", "home_team", "away_team"])
    full_scores = full_scores[full_scores["season_type"] == "REG"]
    for game_id, group in full_scores.groupby("game_id"):
        game_id = str(game_id)
        if game_id not in score_index or not score_index[game_id]["final"]:
            continue
        away = int(group["total_away_score"].max())
        home = int(group["total_home_score"].max())
        row = score_index[game_id]
        if away != row["away_score"] or home != row["home_score"]:
            raise SystemExit(f"score mismatch between schedule and play-by-play for {game_id}")
        if str(group["away_team"].iloc[0]) != row["away_team"] or str(group["home_team"].iloc[0]) != row["home_team"]:
            raise SystemExit(f"team mismatch for {game_id}")

    checks = {}
    for game_id, book in books.items():
        checks[game_id] = crosscheck_game_full(game_id, book, evidence, score_index[game_id])

    profiles = {}
    for team in TEAMS:
        profiles[team] = build_team_profile(evidence, team, rows, checks)
        validate_profile_numbers(profiles[team])

    out = args.out
    team_dir = out / "teams"
    team_dir.mkdir(parents=True, exist_ok=True)
    write_evidence(evidence, out / "evidence_plays.csv.gz")
    for team, profile in profiles.items():
        (team_dir / f"{team}.json").write_text(json.dumps(profile, indent=2) + "\n")
        (team_dir / f"{team}.md").write_text(render_team_md(profile))
    manifest = {
        "schema_version": "scheme_game_manifest/1",
        "projection_ready": False,
        "research_only": True,
        "generated_utc": GENERATED_UTC,
        "last_completed_week": LAST_COMPLETED_WEEK,
        "last_profile_game_date": LAST_PROFILE_DATE,
        "included_games": sum(1 for row in rows if row["included_in_profiles"]),
        "excluded_games": sum(1 for row in rows if not row["included_in_profiles"]),
        "teams": 32,
        "pinned_week_1_9": pinned,
        "sources": source_list(),
        "rights": {
            "gamebook_notice": COPYRIGHT,
            "persisted_pdfs": "Week 9 owner-supplied PDFs already in data/gamebooks/2026/wk09. No new PDF was added.",
            "week_10_pdf_sha256": WEEK10_PDF_SHA,
            "week_10_persisted": False,
        },
        "games": rows,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (out / "crosscheck_gamebooks.json").write_text(json.dumps({
        "schema_version": "scheme_gamebook_crosscheck/1",
        "projection_ready": False,
        "generated_utc": GENERATED_UTC,
        "games": [checks[key] for key in sorted(checks)],
    }, indent=2) + "\n")
    batch = render_verified_batch(checks, profiles)
    (out / "verified_batch_was_nyg.md").write_text(batch)
    (out / "COVERAGE.md").write_text(render_coverage(rows, checks, profiles, pinned))
    print(json.dumps({
        "teams": len(profiles),
        "included_games": manifest["included_games"],
        "crosscheck_match": sum(1 for check in checks.values() if check["status"] == "MATCH"),
        "crosscheck_disagreement": [
            {"game_id": check["game_id"], "fields": check["disagreement_fields"]}
            for check in checks.values() if check["status"] != "MATCH"
        ],
    }, indent=2))
    return 0


def validate_profile_numbers(profile: dict) -> None:
    if profile["projection_ready"] is not False:
        raise ValueError("projection_ready must stay false")
    seen = set()

    def walk(node):
        if isinstance(node, dict):
            if node.get("value") == 0 and node.get("observed") is False:
                raise ValueError("a zero is marked unobserved")
            if node.get("value") == "unknown" and node.get("observed") is True:
                raise ValueError("unknown is marked observed")
            if node.get("kind") == "rate" and node.get("denominator") == 0 and node.get("value") != "unknown":
                raise ValueError("zero-denominator rate is not unknown")
            if "source_url" in node and "retrieved_utc" in node:
                seen.add(node["source_url"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(profile)
    if PBP_URL not in seen:
        raise ValueError("profile is missing the play-by-play source")


if __name__ == "__main__":
    raise SystemExit(main())
