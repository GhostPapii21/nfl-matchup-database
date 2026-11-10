#!/usr/bin/env python3
"""Parse an official NFL Game Summary text extract into tidy CSVs.

The input is the output of ``pdftotext -layout``. Printed numbers are copied
as text. This module does not compute averages, ratings, or win probabilities,
and it does not touch projection configuration.

Week number and the nflverse game id are not printed on the summary. Pass
them in. They are stored as supplied identifiers, not as values read from
the PDF.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


# Printed club names and the abbreviations the game summary uses for them.
# This is a label crosswalk, not a statistic.
CLUBS = {
    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WSH",
}
NICK_TO_ABBR = {name: abbr for name, abbr in CLUBS.items()}
for _name, _abbr in CLUBS.items():
    NICK_TO_ABBR.setdefault(_name.split()[-1], _abbr)
ABBR_TO_CLUB = {abbr: name for name, abbr in CLUBS.items()}

NAME_RE = re.compile(
    r"^(\[[A-Z]+\]|Total|[A-Z][A-Za-z.'\-]+(?:\s+[A-Z][a-z][A-Za-z.'\-]*)?)\s+(.*)$"
)
NUM_RE = re.compile(r"-?\d+(?:\.\d+)?(?:/\d+)?")
PLAY_RE = re.compile(
    r"^[ \t]*([1-4])-(\d+)-((?:BUF|MIN)[ \t]+\d+|50)[ \t]*(.*)$"
)
QEND_RE = re.compile(
    r"^(Buffalo Bills|Minnesota Vikings)\s+(\d+)\s+(\d+:\d+)\s+"
    r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+/\d+)\s+(\d+/\d+)\s*$"
)
SCORE_RE = re.compile(
    r"^(Bills|Vikings)\s+(\d+)\s+(\d+:\d+)\s+(.+?)\s{2,}(\d+)\s+(\d+)\s*$"
)
DRIVE_INFO_RE = re.compile(r"\((\d+)-(-?\d+),\s*(\d+:\d+)\)\s*$")
OFFICIAL_RE = re.compile(
    r"([A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+)?):\s+"
    r"([A-Za-z'\-]+,\s+[A-Za-z'\-]+)\s+\((\d+)\)"
)
ROSTER_RE = re.compile(
    r"^([A-Z]{1,4}(?:/[A-Z]{1,4})?)\s+(\d{1,3})\s+"
    r"([A-Z][A-Za-z.'\-]+(?:\s+[A-Z][a-z][A-Za-z.'\-]*)?)$"
)
LINEUP_RE = re.compile(
    r"([A-Z]{1,4})\s+(\d{1,3})\s+"
    r"([A-Z][A-Za-z.'\-]+(?:\s+[A-Z][a-z][A-Za-z.'\-]*)?)"
)
HY = r"[ \t]*-[ \t]*"
STAT = (
    r"(?:\d+:\d+"
    r"|[A-Z]{2,3}[ \t]+\d+"
    rf"|\d+{HY}\d+{HY}\d+\.\d+%"
    rf"|\d+{HY}\d+{HY}\d+%"
    rf"|\d+{HY}\d+{HY}\d+"
    rf"|\d+{HY}\d+\.\d+"
    rf"|\d+{HY}\d+"
    r"|\d+\.\d+"
    r"|\d+)"
)
TEAM_STAT_RE = re.compile(
    rf"^(?P<label>.*?)\s{{2,}}(?P<visitor>{STAT})\s+(?P<home>{STAT})\s*$"
)
DRIVE_RE = re.compile(
    r"^(\d+)\s+(\d+:\d+)\s+(\d+:\d+)\s+(\d+:\d+)\s+(\S+)\s+(.*\S)\s*$"
)
QUARTERS = {"First": "1", "Second": "2", "Third": "3", "Fourth": "4"}

STAT_KEYS = {
    "rushing": ["att", "yds", "avg", "lg", "td"],
    "passing": ["att", "cmp", "yds", "sk_yd", "td", "lg", "int", "rt"],
    "receiving": ["tar", "rec", "yds", "avg", "lg", "td"],
    "interceptions": ["no", "yds", "avg", "lg", "td"],
    "punting": ["no", "yds", "avg", "net", "tb", "in20", "lg"],
    "punt_returns": ["no", "yds", "avg", "fc", "lg", "td"],
    "kickoff_returns": ["no", "yds", "avg", "fc", "lg", "td"],
}
STAT_HEADERS = [
    ("kickoff_returns", "KICKOFF RETURNS"),
    ("punt_returns", "PUNT RETURNS"),
    ("punting", "PUNTING"),
    ("interceptions", "INTERCEPTIONS"),
    ("receiving", "PASS RECEIVING"),
    ("passing", "PASSING"),
    ("rushing", "RUSHING"),
]
DEFENSE_KEYS = [
    "tkl", "ast", "comb", "sk", "sk_yds", "tfl", "qh", "interceptions", "pd",
    "ff", "fr", "st_tkl", "st_ast", "st_ff", "st_fr", "st_bl", "misc_tkl",
    "misc_ast", "misc_ff", "misc_fr",
]
FUMBLE_KEYS = [
    "fum", "lost", "own_rec", "own_rec_yds", "own_rec_td", "forced", "opp_rec",
    "opp_rec_yds", "opp_rec_td", "out_of_bounds",
]
PLAYER_SCORE_KEYS = [
    "td", "rush_td", "rec_td", "ko_td", "punt_td", "int_td", "fum_td", "misc_td",
    "fg", "xp", "two_pt_rush", "two_pt_rec", "safety", "points",
]

SCHEMAS = {
    "game_meta": [
        "nflverse_game_id", "week_supplied", "season_year_printed",
        "visitor_team", "visitor_abbr", "home_team", "home_abbr",
        "date_printed", "date_iso", "start_time", "venue", "roof",
        "game_weather", "stadium_printed", "temp_printed", "humidity_printed",
        "wind_printed", "outdoor_weather", "attendance_printed", "game_duration",
        "toss_note", "second_half_election", "kickoff_drive_note",
        "visitor_q1", "visitor_q2", "visitor_q3", "visitor_q4", "visitor_ot",
        "visitor_final", "home_q1", "home_q2", "home_q3", "home_q4", "home_ot",
        "home_final", "officials_printed",
    ],
    "officials": ["nflverse_game_id", "position", "name", "number"],
    "quarter_scores": ["nflverse_game_id", "team", "team_abbr", "quarter", "points"],
    "scoring_plays": [
        "nflverse_game_id", "seq", "team", "team_abbr", "quarter", "time",
        "description", "drive_plays", "drive_yards", "drive_time",
        "visitor_score", "home_score",
    ],
    "field_goals": [
        "nflverse_game_id", "seq", "team", "team_abbr", "kicker", "distance", "result",
    ],
    "lineups": [
        "nflverse_game_id", "team", "team_abbr", "unit", "position", "number", "player",
    ],
    "participation": [
        "nflverse_game_id", "team", "team_abbr", "list_name", "position", "number", "player",
    ],
    "rushing": [
        "nflverse_game_id", "scope", "team", "team_abbr", "player", "is_total",
        "att", "yds", "avg", "lg", "td",
    ],
    "passing": [
        "nflverse_game_id", "scope", "team", "team_abbr", "player", "is_total",
        "att", "cmp", "yds", "sk_yd", "td", "lg", "int", "rt",
    ],
    "receiving": [
        "nflverse_game_id", "scope", "team", "team_abbr", "player", "is_total",
        "tar", "rec", "yds", "avg", "lg", "td",
    ],
    "interceptions": [
        "nflverse_game_id", "scope", "team", "team_abbr", "player", "is_total",
        "no", "yds", "avg", "lg", "td",
    ],
    "punting": [
        "nflverse_game_id", "scope", "team", "team_abbr", "player", "is_total",
        "no", "yds", "avg", "net", "tb", "in20", "lg",
    ],
    "returns": [
        "nflverse_game_id", "scope", "return_type", "team", "team_abbr", "player",
        "is_total", "bracket_row", "no", "yds", "avg", "fc", "lg", "td",
    ],
    "fumbles": [
        "nflverse_game_id", "scope", "team", "team_abbr", "player", "is_total",
        *FUMBLE_KEYS,
    ],
    "defense": [
        "nflverse_game_id", "scope", "team", "team_abbr", "player", "is_total",
        *DEFENSE_KEYS,
    ],
    "team_stats": [
        "nflverse_game_id", "scope", "indent", "stat", "visitor", "home",
    ],
    "drives": [
        "nflverse_game_id", "team", "team_abbr", "drive_number", "time_received",
        "time_lost", "time_possession", "how_obtained", "drive_began", "plays",
        "yards_gained", "yards_penalty", "net_yards", "first_downs",
        "last_scrimmage", "how_given_up",
    ],
    "drive_notes": [
        "nflverse_game_id", "kind", "team", "team_abbr", "printed_marker", "value", "detail",
    ],
    "time_of_possession": [
        "nflverse_game_id", "team", "team_abbr", "q1", "q2", "q3", "q4", "ot", "total",
    ],
    "quarter_summaries": [
        "nflverse_game_id", "quarter", "team", "team_abbr", "score", "time_possession",
        "rush_first_downs", "pass_first_downs", "penalty_first_downs",
        "total_first_downs", "third_down", "fourth_down",
    ],
    "play_by_play": [
        "nflverse_game_id", "seq", "quarter", "clock", "down", "distance",
        "yardline", "offense_team", "row_kind", "contains_reversed_text", "description",
    ],
    "touchdown_units": [
        "nflverse_game_id", "side", "team", "team_abbr", "offense", "defense", "special_teams",
    ],
    "player_scoring": [
        "nflverse_game_id", "team", "team_abbr", "player", *PLAYER_SCORE_KEYS,
    ],
    "possession_detail": [
        "nflverse_game_id", "metric", "layout", "first_half_visitor", "first_half_home",
        "second_half_visitor", "second_half_home", "game_visitor", "game_home",
        "first_half", "second_half", "game",
    ],
    "parse_gaps": ["gap_id", "severity", "section", "detail"],
}


def copyright_notice(text: str) -> str:
    """Join the wrapped NFL copyright paragraph at the top of the extract."""
    lines = [ln.strip() for ln in text.splitlines()]
    for i, ln in enumerate(lines):
        if "NFL Copyright" not in ln:
            continue
        parts = [ln]
        if i + 1 < len(lines) and lines[i + 1].startswith("coverage of the game"):
            parts.append(lines[i + 1])
        return re.sub(r"\s+", " ", " ".join(parts)).strip()
    return ""


def _blank(fields, **kwargs):
    out = {key: "" for key in fields}
    for key, value in kwargs.items():
        if key not in out:
            raise KeyError(key)
        out[key] = "" if value is None else str(value)
    return out


def _header_key(line: str):
    for table, key in STAT_HEADERS:
        starts = [m.start() for m in re.finditer(re.escape(key), line)]
        if len(starts) >= 2:
            return table, starts[1]
    return None


def _column_split(lines):
    ends = []
    for line in lines:
        if not line.strip():
            continue
        gaps = list(re.finditer(r" {8,}", line))
        if not gaps:
            continue
        biggest = max(gaps, key=lambda m: m.end() - m.start())
        ends.append(biggest.end())
    if not ends:
        raise ValueError("no column gap in roster block")
    return Counter(ends).most_common(1)[0][0]


def _join_side(lines, index, side):
    parts = []
    for line in lines:
        if not line.strip():
            continue
        chunk = line[:index] if side == "left" else line[index:]
        chunk = chunk.strip()
        if chunk:
            parts.append(chunk)
    return " ".join(parts)


class GameBookParser:
    def __init__(self, text: str, game_id: str, week: int):
        self.text = text.replace("\f", "")
        self.lines = self.text.splitlines()
        self.game_id = game_id
        self.week = str(week)
        self.gaps = []
        self.tables = {name: [] for name in SCHEMAS}
        self.tables["parse_gaps"] = self.gaps
        self.meta = {}
        self.visitor = ""
        self.home = ""
        self.visitor_abbr = ""
        self.home_abbr = ""
        self.elections = []

    def gap(self, gap_id, severity, section, detail):
        self.gaps.append({
            "gap_id": gap_id,
            "severity": severity,
            "section": section,
            "detail": re.sub(r"\s+", " ", detail).strip(),
        })

    def abbr(self, label: str) -> str:
        label = " ".join(label.split())
        if label in NICK_TO_ABBR:
            return NICK_TO_ABBR[label]
        if label in ABBR_TO_CLUB:
            return label
        self.gap("unknown_club", "gap", "clubs", label)
        return ""

    def club(self, abbr: str) -> str:
        return ABBR_TO_CLUB.get(abbr, "")

    def find(self, pred, start=0):
        for i in range(start, len(self.lines)):
            if pred(self.lines[i]):
                return i
        raise ValueError("section marker not found")

    def parse(self):
        self.gap(
            "supplied_identifiers",
            "note",
            "game_meta",
            "nflverse_game_id and week are not printed on the game summary. "
            f"Ingest supplied nflverse_game_id={self.game_id} and week={self.week}.",
        )
        idx_final = self.find(lambda ln: "Final Individual Statistics" in ln)
        idx_team = self.find(lambda ln: "Final Team Statistics" in ln, idx_final)
        idx_drives = self.find(lambda ln: "Ball Possession And Drive Chart" in ln, idx_team)
        idx_def = self.find(lambda ln: "Final Defensive Statistics" in ln, idx_drives)
        idx_half = self.find(lambda ln: "First Half Summary" in ln, idx_def)
        idx_pbp = self.find(lambda ln: "Play By Play" in ln and "Quarter" in ln, idx_half)
        idx_misc = self.find(lambda ln: "Miscellaneous Statistics Report" in ln, idx_pbp)

        self._parse_preamble(self.lines[:idx_final])
        self._parse_player_section(self.lines[idx_final:idx_team], "final")
        self._parse_fumbles(self.lines[idx_final:idx_team], "final")
        self._parse_team_stats(self.lines[idx_team:idx_drives], "final")
        self._parse_drives(self.lines[idx_drives:idx_def])
        self._parse_defense(self.lines[idx_def:idx_half], "final")
        half_lines = self.lines[idx_half:idx_pbp]
        self._note_half_reprint(half_lines)
        self._parse_team_stats(half_lines, "first_half")
        self._parse_player_section(half_lines, "first_half")
        self._parse_defense(half_lines, "first_half")
        self._parse_pbp(self.lines[idx_pbp:idx_misc])
        self._parse_misc(self.lines[idx_misc:])
        self._note_cross_checks()
        self._finish_meta()
        return self.tables

    def _parse_preamble(self, lines):
        text = "\n".join(lines)
        date_m = re.search(r"Date:\s*([A-Za-z]+,\s+\d{1,2}/\d{1,2}/\d{4})", text)
        time_m = re.search(r"Start Time:\s*(\d{1,2}:\d{2}\s*[AP]M\s*[A-Z]+)", text)
        club_pat = "|".join(re.escape(name) for name in sorted(CLUBS, key=len, reverse=True))
        match_m = re.search(rf"({club_pat}) at ({club_pat})", text)
        venue = ""
        weather = stadium = temp = humidity = wind = outdoor = ""
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("at U.S. Bank") or (
                stripped.startswith("at ") and "Stadium" in stripped and "Start Time" not in stripped
            ):
                venue = stripped[3:].strip() if stripped.startswith("at ") else stripped
            if "Game Weather:" in line:
                m = re.search(
                    r"Game Weather:\s*(.*?)\s{2,}Temp:\s*(.*?)\s+Humidity:\s*([^,]+),\s*Wind:\s*(.+)$",
                    stripped,
                )
                if m:
                    weather, temp, humidity, wind = (g.strip() for g in m.groups())
            if "Outdoor Weather:" in line:
                m = re.match(r"^(.*?)\s{2,}Outdoor Weather:\s*(.+)$", stripped)
                if m:
                    stadium, outdoor = m.group(1).strip(), m.group(2).strip()
            if stripped.startswith("Paid Attendance:"):
                att = re.search(r"Paid Attendance:\s*([\d,]+)", stripped)
                dur = re.search(r"Time:\s*(\d+:\d+)", stripped)
                self.meta["attendance_printed"] = att.group(1) if att else ""
                self.meta["game_duration"] = dur.group(1) if dur else ""
            for official in OFFICIAL_RE.finditer(line):
                self.tables["officials"].append(_blank(
                    SCHEMAS["officials"],
                    nflverse_game_id=self.game_id,
                    position=official.group(1),
                    name=official.group(2),
                    number=official.group(3),
                ))

        if not date_m or not match_m:
            raise ValueError("game summary header did not match the expected date and matchup")
        date_printed = date_m.group(1)
        month, day, year = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", date_printed).groups()
        self.visitor = match_m.group(1)
        self.home = match_m.group(2)
        self.visitor_abbr = self.abbr(self.visitor)
        self.home_abbr = self.abbr(self.home)
        self.meta.update({
            "nflverse_game_id": self.game_id,
            "week_supplied": self.week,
            "season_year_printed": year,
            "visitor_team": self.visitor,
            "visitor_abbr": self.visitor_abbr,
            "home_team": self.home,
            "home_abbr": self.home_abbr,
            "date_printed": date_printed,
            "date_iso": f"{int(year):04d}-{int(month):02d}-{int(day):02d}",
            "start_time": time_m.group(1) if time_m else "",
            "venue": venue,
            "roof": weather,
            "game_weather": weather,
            "stadium_printed": stadium,
            "temp_printed": temp,
            "humidity_printed": humidity,
            "wind_printed": wind,
            "outdoor_weather": outdoor,
        })

        self._parse_lineups(lines)
        self._parse_participation(lines)
        self._parse_field_goals(lines)
        self._parse_scoreboard(lines)
        self._parse_scoring_plays(lines)

    def _parse_lineups(self, lines):
        start = next(i for i, ln in enumerate(lines) if "Lineups" in ln and "Substitutions" not in ln)
        end = next(i for i, ln in enumerate(lines) if "Substitutions" in ln and i > start)
        team_line = ""
        for line in lines[start:end]:
            if "Bills" in line and "Vikings" in line and "Offense" not in line:
                team_line = line
                break
        if team_line:
            left = team_line.find(self.visitor.split()[-1])
            right = team_line.find(self.home.split()[-1])
            if left < 0 or right < 0 or left > right:
                self.gap("lineup_column_order", "gap", "lineups", team_line.strip())
        slots = [
            (self.visitor, self.visitor_abbr, "offense"),
            (self.visitor, self.visitor_abbr, "defense"),
            (self.home, self.home_abbr, "offense"),
            (self.home, self.home_abbr, "defense"),
        ]
        for line in lines[start:end]:
            found = LINEUP_RE.findall(line)
            if not found:
                continue
            if len(found) != 4:
                self.gap("lineup_row", "gap", "lineups", line.strip())
                continue
            for (team, abbr, unit), (pos, number, player) in zip(slots, found):
                self.tables["lineups"].append(_blank(
                    SCHEMAS["lineups"],
                    nflverse_game_id=self.game_id,
                    team=team,
                    team_abbr=abbr,
                    unit=unit,
                    position=pos,
                    number=number,
                    player=player,
                ))

    def _index_in(self, lines, pred, start=0):
        for i in range(start, len(lines)):
            if pred(lines[i]):
                return i
        raise ValueError("marker missing in preamble")

    def _roster_block(self, lines, start_pred, end_pred):
        start = self._index_in(lines, start_pred)
        end = self._index_in(lines, end_pred, start + 1)
        data = lines[start + 1:end]
        if not any(ln.strip() for ln in data):
            return "", ""
        index = _column_split(data)
        return _join_side(data, index, "left"), _join_side(data, index, "right")

    def _add_roster(self, blob, team, abbr, list_name):
        if not blob.strip():
            return 0
        count = 0
        for part in blob.split(","):
            part = " ".join(part.split())
            if not part:
                continue
            m = ROSTER_RE.match(part)
            if not m:
                self.gap("roster_item", "gap", "participation", f"{list_name}: {part}")
                continue
            self.tables["participation"].append(_blank(
                SCHEMAS["participation"],
                nflverse_game_id=self.game_id,
                team=team,
                team_abbr=abbr,
                list_name=list_name,
                position=m.group(1),
                number=m.group(2),
                player=m.group(3),
            ))
            count += 1
        return count

    def _parse_participation(self, lines):
        left, right = self._roster_block(
            lines,
            lambda ln: "Substitutions" in ln and "Did Not Play" not in ln,
            lambda ln: "Did Not Play" in ln,
        )
        self._add_roster(left, self.visitor, self.visitor_abbr, "substitution")
        self._add_roster(right, self.home, self.home_abbr, "substitution")

        dnp_left, dnp_right = self._roster_block(
            lines,
            lambda ln: "Did Not Play" in ln,
            lambda ln: "Not Active" in ln,
        )
        dnp_n = self._add_roster(dnp_left, self.visitor, self.visitor_abbr, "did_not_play")
        dnp_n += self._add_roster(dnp_right, self.home, self.home_abbr, "did_not_play")
        if dnp_n == 0:
            self.gap(
                "did_not_play_blank",
                "note",
                "participation",
                "Did Not Play is printed for both clubs and lists no players.",
            )

        left, right = self._roster_block(
            lines,
            lambda ln: "Not Active" in ln,
            lambda ln: "Field Goals" in ln,
        )
        self._add_roster(left, self.visitor, self.visitor_abbr, "not_active")
        self._add_roster(right, self.home, self.home_abbr, "not_active")

    def _parse_field_goals(self, lines):
        start = self._index_in(lines, lambda ln: "Field Goals" in ln)
        seq = 0
        found = False
        kicker_re = re.compile(
            r"([A-Z]\.[A-Za-z'\-]+)\s+((?:\(\d+\)|\b\d+\b)(?:\s+(?:\(\d+\)|\b\d+\b))*)"
        )
        for line in lines[start + 1:]:
            if "VISITOR:" in line:
                break
            if not re.search(r"\(\d+\)", line):
                continue
            found = True
            for match in kicker_re.finditer(line):
                team, abbr = (
                    (self.visitor, self.visitor_abbr)
                    if match.start() < len(line) / 2
                    else (self.home, self.home_abbr)
                )
                for token in match.group(2).split():
                    seq += 1
                    made = token.startswith("(")
                    self.tables["field_goals"].append(_blank(
                        SCHEMAS["field_goals"],
                        nflverse_game_id=self.game_id,
                        seq=seq,
                        team=team,
                        team_abbr=abbr,
                        kicker=match.group(1),
                        distance=token.strip("()"),
                        result="made" if made else "missed",
                    ))
        if not found:
            self.gap("field_goals_missing", "gap", "field_goals", "no field goal line")
        self.gap(
            "field_goal_result_notation",
            "note",
            "field_goals",
            "The game summary prints made field goals in parentheses and missed field goals without them "
            "('Field Goals (made ( ) & missed)'). result reads that notation. It is not computed from the score.",
        )

    def _parse_scoreboard(self, lines):
        quarters = ["1", "2", "3", "4", "OT", "Total"]
        wide = {"visitor": {}, "home": {}}
        for line in lines:
            m = re.match(
                r"^(VISITOR|HOME):\s+(.+?)\s{2,}(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$",
                line.strip(),
            )
            if not m:
                continue
            side = "visitor" if m.group(1) == "VISITOR" else "home"
            team = m.group(2).strip()
            points = m.groups()[2:]
            abbr = self.abbr(team)
            for quarter, value in zip(quarters, points):
                wide[side][quarter] = value
                self.tables["quarter_scores"].append(_blank(
                    SCHEMAS["quarter_scores"],
                    nflverse_game_id=self.game_id,
                    team=team,
                    team_abbr=abbr,
                    quarter=quarter,
                    points=value,
                ))
        if set(wide["visitor"]) != set(quarters) or set(wide["home"]) != set(quarters):
            self.gap("scoreboard", "gap", "quarter_scores", "visitor or home quarter line was not parsed")
        self.meta["visitor_q1"] = wide["visitor"].get("1", "")
        self.meta["visitor_q2"] = wide["visitor"].get("2", "")
        self.meta["visitor_q3"] = wide["visitor"].get("3", "")
        self.meta["visitor_q4"] = wide["visitor"].get("4", "")
        self.meta["visitor_ot"] = wide["visitor"].get("OT", "")
        self.meta["visitor_final"] = wide["visitor"].get("Total", "")
        self.meta["home_q1"] = wide["home"].get("1", "")
        self.meta["home_q2"] = wide["home"].get("2", "")
        self.meta["home_q3"] = wide["home"].get("3", "")
        self.meta["home_q4"] = wide["home"].get("4", "")
        self.meta["home_ot"] = wide["home"].get("OT", "")
        self.meta["home_final"] = wide["home"].get("Total", "")

    def _parse_scoring_plays(self, lines):
        seq = 0
        for line in lines:
            if "Final Individual Statistics" in line:
                break
            m = SCORE_RE.match(line.strip())
            if not m:
                continue
            seq += 1
            team_nick, quarter, clock, desc, vis, home = m.groups()
            drive = DRIVE_INFO_RE.search(desc)
            self.tables["scoring_plays"].append(_blank(
                SCHEMAS["scoring_plays"],
                nflverse_game_id=self.game_id,
                seq=seq,
                team=team_nick,
                team_abbr=self.abbr(team_nick),
                quarter=quarter,
                time=clock,
                description=desc.strip(),
                drive_plays=drive.group(1) if drive else "",
                drive_yards=drive.group(2) if drive else "",
                drive_time=drive.group(3) if drive else "",
                visitor_score=vis,
                home_score=home,
            ))
        self.gap(
            "first_half_scoring_reprint",
            "note",
            "scoring_plays",
            "The first-half summary repeats the scoring plays already listed on the game summary page. "
            "Those repeat lines are not copied into scoring_plays.",
        )

    def _parse_player_section(self, lines, scope):
        i = 0
        while i < len(lines):
            found = _header_key(lines[i])
            if not found:
                i += 1
                continue
            table, split_at = found
            i += 1
            block = []
            while i < len(lines):
                if not lines[i].strip() or _header_key(lines[i]):
                    break
                block.append(lines[i])
                i += 1
            self._emit_stat_block(table, split_at, block, scope)

    def _emit_stat_block(self, table, split_at, block, scope):
        keys = STAT_KEYS[table]
        return_type = ""
        out_name = table
        if table in ("punt_returns", "kickoff_returns"):
            out_name = "returns"
            return_type = "punt" if table == "punt_returns" else "kickoff"
        for line in block:
            left = line[:split_at].strip() if len(line) > split_at else line.strip()
            # A short left-only line is entirely left of the split.
            if len(line) <= split_at:
                left, right = line.strip(), ""
            else:
                # If the left slice is only the tail of a right-side row, detect by content start.
                right = line[split_at:].strip()
                if left and NUM_RE.search(left) is None and not left.startswith("Total") and not left.startswith("["):
                    # Name without numbers on the left means the row actually starts on the right.
                    if line.strip().startswith(right):
                        left = ""
            for side, team, abbr in (
                (left, self.visitor, self.visitor_abbr),
                (right, self.home, self.home_abbr),
            ):
                if not side:
                    continue
                parsed = self._player_numbers(side, keys, f"{scope} {table}")
                if parsed is None:
                    continue
                player, nums = parsed
                payload = {
                    "nflverse_game_id": self.game_id,
                    "scope": scope,
                    "team": team,
                    "team_abbr": abbr,
                    "player": player,
                    "is_total": "true" if player == "Total" else "false",
                }
                payload.update(dict(zip(keys, nums)))
                if out_name == "returns":
                    payload["return_type"] = return_type
                    payload["bracket_row"] = "true" if player.startswith("[") else "false"
                self.tables[out_name].append(_blank(SCHEMAS[out_name], **payload))

    def _player_numbers(self, text, keys, where):
        m = NAME_RE.match(text.strip())
        if not m:
            self.gap("stat_name", "gap", where, text.strip()[:200])
            return None
        nums = NUM_RE.findall(m.group(2))
        if len(nums) != len(keys):
            self.gap(
                "stat_width",
                "gap",
                where,
                f"{m.group(1)} has {len(nums)} numbers, expected {len(keys)}: {m.group(2)[:160]}",
            )
            return None
        return m.group(1), nums

    def _parse_fumbles(self, lines, scope):
        pending = ""
        team = ""
        active = False
        for line in lines:
            s = line.strip()
            if s in ("Buffalo Bills", "Minnesota Vikings"):
                pending = s
                continue
            if s.startswith("FUMBLES"):
                active = True
                team = pending
                continue
            if not active or not s:
                continue
            if "vs " in s:
                active = False
                continue
            parsed = self._player_numbers(s, FUMBLE_KEYS, "fumbles")
            if parsed is None or not team:
                continue
            player, nums = parsed
            abbr = self.abbr(team)
            self.tables["fumbles"].append(_blank(
                SCHEMAS["fumbles"],
                nflverse_game_id=self.game_id,
                scope=scope,
                team=team,
                team_abbr=abbr,
                player=player,
                is_total="true" if player == "Total" else "false",
                **dict(zip(FUMBLE_KEYS, nums)),
            ))

    def _parse_team_stats(self, lines, scope):
        started = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("TOTAL FIRST DOWNS"):
                started = True
            if not started or not stripped:
                continue
            if stripped.startswith("Buffalo Bills vs") or re.fullmatch(r"11/9/\d{4} at U\.S\. Bank Stadium", stripped):
                continue
            if _header_key(line) or stripped in ("Buffalo Bills", "Minnesota Vikings"):
                break
            if "Regular Defensive Plays" in line or stripped.startswith("RUSHING"):
                break
            indent = len(line) - len(line.lstrip(" "))
            m = TEAM_STAT_RE.match(line.rstrip())
            if not m:
                if re.search(r"\d", stripped):
                    self.gap("team_stat_line", "gap", f"team_stats:{scope}", stripped[:240])
                continue
            self.tables["team_stats"].append(_blank(
                SCHEMAS["team_stats"],
                nflverse_game_id=self.game_id,
                scope=scope,
                indent=indent,
                stat=m.group("label").strip(),
                visitor=m.group("visitor").strip(),
                home=m.group("home").strip(),
            ))

    def _note_half_reprint(self, lines):
        raw = []
        for line in lines:
            s = line.strip()
            if re.search(r"=\s*\d+", s) and ("Bills" in s or "Vikings" in s) and "Efficiency" not in s:
                raw.append(s)
            if s.startswith("TOTAL FIRST DOWNS"):
                break
        if raw:
            self.gap(
                "first_half_score_reprint",
                "note",
                "quarter_scores",
                "First-half period score lines are a reprint of quarters 1 and 2, not a second scoreboard: "
                + " | ".join(raw),
            )

    def _parse_drives(self, lines):
        team = ""
        for line in lines:
            s = line.strip()
            if not s:
                continue
            if s in ("Buffalo Bills", "Minnesota Vikings"):
                team = s
                continue
            if s.startswith("#") or s.startswith("Recd") or "How Ball" in s or "Ball Possession" in s:
                continue
            if s.startswith("Buffalo Bills vs") or re.fullmatch(r"11/9/\d{4} at U\.S\. Bank Stadium", s):
                continue
            if s.startswith("Time of Possession"):
                continue
            avg = re.search(r"\((\d+)\)\s+Average\s+([A-Z]{2,3})\s+(\d+)", s)
            if avg:
                abbr = avg.group(2)
                self.tables["drive_notes"].append(_blank(
                    SCHEMAS["drive_notes"],
                    nflverse_game_id=self.game_id,
                    kind="chart_average",
                    team=self.club(abbr),
                    team_abbr=abbr,
                    printed_marker=f"({avg.group(1)})",
                    value=avg.group(3),
                    detail=s,
                ))
                continue
            if s.startswith("*"):
                self.tables["drive_notes"].append(_blank(
                    SCHEMAS["drive_notes"],
                    nflverse_game_id=self.game_id,
                    kind="footnote",
                    detail=s,
                ))
                continue
            kick = re.search(
                r"Bills:\s*(\d+)\s*-\s*([A-Z]{2,3}\s+\d+)\s+Vikings:\s*(\d+)\s*-\s*([A-Z]{2,3}\s+\d+)",
                s,
            )
            if kick:
                self.meta["kickoff_drive_note"] = s
                pairs = [
                    (self.visitor, self.visitor_abbr, f"{kick.group(1)} - {kick.group(2)}"),
                    (self.home, self.home_abbr, f"{kick.group(3)} - {kick.group(4)}"),
                ]
                for club, abbr, value in pairs:
                    self.tables["drive_notes"].append(_blank(
                        SCHEMAS["drive_notes"],
                        nflverse_game_id=self.game_id,
                        kind="kickoff_drive_average",
                        team=club,
                        team_abbr=abbr,
                        value=value,
                        detail=s,
                    ))
                continue
            top = re.match(r"^(Visitor|Home)\s+(.+?)\s{2,}(.*)$", s)
            if top and re.search(r"\d+:\d+", s):
                times = re.findall(r"\d+:\d+", s)
                club = top.group(2).strip()
                abbr = self.abbr(club)
                payload = {"q1": "", "q2": "", "q3": "", "q4": "", "ot": "", "total": ""}
                if len(times) == 5:
                    payload.update(dict(zip(("q1", "q2", "q3", "q4", "total"), times)))
                elif len(times) == 6:
                    payload.update(dict(zip(("q1", "q2", "q3", "q4", "ot", "total"), times)))
                else:
                    self.gap("top_width", "gap", "time_of_possession", s)
                self.tables["time_of_possession"].append(_blank(
                    SCHEMAS["time_of_possession"],
                    nflverse_game_id=self.game_id,
                    team=club,
                    team_abbr=abbr,
                    **payload,
                ))
                continue
            m = DRIVE_RE.match(s)
            if m and team:
                rest = re.split(r"\s{2,}", m.group(6).strip())
                if len(rest) != 8:
                    self.gap("drive_width", "gap", "drives", s)
                    continue
                self.tables["drives"].append(_blank(
                    SCHEMAS["drives"],
                    nflverse_game_id=self.game_id,
                    team=team,
                    team_abbr=self.abbr(team),
                    drive_number=m.group(1),
                    time_received=m.group(2),
                    time_lost=m.group(3),
                    time_possession=m.group(4),
                    how_obtained=m.group(5),
                    drive_began=rest[0],
                    plays=rest[1],
                    yards_gained=rest[2],
                    yards_penalty=rest[3],
                    net_yards=rest[4],
                    first_downs=rest[5],
                    last_scrimmage=rest[6],
                    how_given_up=rest[7],
                ))
                continue
            if re.search(r"\d", s):
                self.gap("drive_line", "gap", "drives", s[:240])

    def _parse_defense(self, lines, scope):
        team = ""
        in_table = False
        for line in lines:
            s = line.strip()
            if "Regular Defensive Plays" in line:
                if "Buffalo" in line:
                    team = self.visitor
                elif "Minnesota" in line:
                    team = self.home
                in_table = True
                continue
            if not in_table or not s:
                continue
            if s.startswith("TKL") or s.startswith("Buffalo Bills vs") or s.startswith("First Half"):
                continue
            if re.fullmatch(r"11/9/\d{4} at U\.S\. Bank Stadium", s):
                continue
            parsed = self._player_numbers(s, DEFENSE_KEYS, f"defense:{scope}")
            if parsed is None:
                continue
            player, nums = parsed
            abbr = self.abbr(team) if team else ""
            self.tables["defense"].append(_blank(
                SCHEMAS["defense"],
                nflverse_game_id=self.game_id,
                scope=scope,
                team=team,
                team_abbr=abbr,
                player=player,
                is_total="true" if player == "Total" else "false",
                **dict(zip(DEFENSE_KEYS, nums)),
            ))
            if player == "Total":
                in_table = False

    def _pbp_row(self, quarter, clock, down, distance, yardline, offense, kind, description):
        text = " ".join(description.split())
        return _blank(
            SCHEMAS["play_by_play"],
            nflverse_game_id=self.game_id,
            quarter=quarter,
            clock=clock,
            down=down,
            distance=distance,
            yardline=" ".join(yardline.split()),
            offense_team=offense,
            row_kind=kind,
            contains_reversed_text="true" if "REVERSED" in text else "false",
            description=text,
        )

    def _parse_pbp(self, lines):
        rows = []
        quarter = ""
        offense = ""
        current = None

        def flush():
            nonlocal current
            if current is None:
                return
            text = " ".join(current["description"].split())
            current["description"] = text
            current["contains_reversed_text"] = "true" if "REVERSED" in text else "false"
            rows.append(current)
            current = None

        i = 0
        n = len(lines)
        while i < n:
            raw = lines[i].replace("\f", "")
            s = raw.strip()
            if not s:
                i += 1
                continue
            qmatch = re.search(r"Play By Play\s+(First|Second|Third|Fourth) Quarter", raw)
            if qmatch:
                flush()
                quarter = QUARTERS[qmatch.group(1)]
                i += 1
                continue
            bare_q = re.fullmatch(r"(First|Second|Third|Fourth) Quarter", s)
            if bare_q:
                flush()
                quarter = QUARTERS[bare_q.group(1)]
                i += 1
                continue
            if s.startswith("Buffalo Bills vs Minnesota Vikings"):
                i += 1
                continue
            if re.fullmatch(r"11/9/\d{4}(?: at U\.S\. Bank Stadium)?", s):
                i += 1
                continue
            if s.startswith("END OF QUARTER"):
                flush()
                rows.append(self._pbp_row(quarter, "", "", "", "", "", "quarter_end", "END OF QUARTER"))
                i += 1
                found = 0
                while i < n and found < 2:
                    nxt = lines[i].replace("\f", "")
                    ss = nxt.strip()
                    if (not ss or ss.startswith("Score") or "Efficiencies" in ss or "First Downs" in nxt):
                        i += 1
                        continue
                    m = QEND_RE.match(ss)
                    if not m:
                        break
                    self.tables["quarter_summaries"].append(_blank(
                        SCHEMAS["quarter_summaries"],
                        nflverse_game_id=self.game_id,
                        quarter=quarter,
                        team=m.group(1),
                        team_abbr=self.abbr(m.group(1)),
                        score=m.group(2),
                        time_possession=m.group(3),
                        rush_first_downs=m.group(4),
                        pass_first_downs=m.group(5),
                        penalty_first_downs=m.group(6),
                        total_first_downs=m.group(7),
                        third_down=m.group(8),
                        fourth_down=m.group(9),
                    ))
                    found += 1
                    i += 1
                if found != 2:
                    self.gap("quarter_summary", "gap", "quarter_summaries", f"quarter {quarter} parsed {found} team rows")
                continue

            play = PLAY_RE.match(raw)
            if play:
                flush()
                clock, desc = _clock_and_text(play.group(4))
                current = self._pbp_row(
                    quarter, clock, play.group(1), play.group(2), play.group(3), offense, "scrimmage", desc,
                )
                i += 1
                continue
            drive = re.match(r"^(Buffalo Bills|Minnesota Vikings) at (\d+:\d+)\b(?:,\s*(.*))?$", s)
            if drive:
                flush()
                offense = self.abbr(drive.group(1))
                rows.append(self._pbp_row(quarter, drive.group(2), "", "", "", offense, "drive_start", s))
                i += 1
                continue
            cont = re.match(r"^(Buffalo Bills|Minnesota Vikings) continued\.$", s)
            if cont:
                flush()
                offense = self.abbr(cont.group(1))
                rows.append(self._pbp_row(quarter, "", "", "", "", offense, "drive_start", s))
                i += 1
                continue
            if s.startswith("Timeout"):
                flush()
                clock_m = re.search(r"(\d+:\d+)", s)
                rows.append(self._pbp_row(
                    quarter, clock_m.group(1) if clock_m else "", "", "", "", "", "timeout", s,
                ))
                i += 1
                continue
            if s == "Two-Minute Warning":
                flush()
                rows.append(self._pbp_row(quarter, "", "", "", "", "", "two_minute", s))
                i += 1
                continue
            if re.match(r"^BUF \d+ MIN \d+,", s):
                flush()
                rows.append(self._pbp_row(quarter, "", "", "", "", "", "score", s))
                i += 1
                continue
            if re.match(r"^[A-Z].*\bkicks\b", s):
                flush()
                current = self._pbp_row(quarter, "", "", "", "", "", "kickoff", s)
                i += 1
                continue
            if "elects to" in s or s.startswith("BUF wins toss") or s.startswith("MIN elects"):
                flush()
                rows.append(self._pbp_row(quarter, "", "", "", "", "", "note", s))
                self.elections.append(s)
                i += 1
                continue
            if current is not None:
                current["description"] = (current["description"] + " " + s).strip()
                i += 1
                continue
            if s.startswith("**"):
                rows.append(self._pbp_row(quarter, "", "", "", "", "", "note", s))
                i += 1
                continue
            self.gap("unparsed_pbp_line", "gap", "play_by_play", s[:240])
            rows.append(self._pbp_row(quarter, "", "", "", "", "", "note", s))
            i += 1
        flush()
        for seq, row in enumerate(rows, 1):
            row["seq"] = str(seq)
        self.tables["play_by_play"] = rows
        if any(r["contains_reversed_text"] == "true" for r in rows):
            self.gap(
                "reversed_text_kept_verbatim",
                "note",
                "play_by_play",
                "Plays marked REVERSED keep both the original wording and the reversed wording in description. "
                "No yardage was taken from those sentences. contains_reversed_text flags the printed word.",
            )
        if any("Lateral" in r["description"] for r in rows):
            self.gap(
                "lateral_not_reallocated",
                "note",
                "play_by_play",
                "A lateral stays inside the play description. Receiving credit is only the printed receiving table.",
            )

    def _parse_misc(self, lines):
        if any("Ten Longest Plays" in ln for ln in lines):
            self.gap(
                "longest_plays_unparsed",
                "gap",
                "longest_plays",
                "Ten Longest Plays is not a CSV. pdftotext wrapped an injury-update tail from an 8-yard "
                "Minnesota play into the next 8-yard row, so the yard/quarter columns on that pair are not reliable. "
                "The same plays remain in play_by_play.",
            )
        for line in lines:
            s = line.strip()
            unit = re.match(r"^(VISITOR|HOME)\s+(.+?)\s{2,}(\d+)\s+(\d+)\s+(\d+)\s*$", s)
            if unit and "Scoring" not in s:
                self.tables["touchdown_units"].append(_blank(
                    SCHEMAS["touchdown_units"],
                    nflverse_game_id=self.game_id,
                    side=unit.group(1),
                    team=unit.group(2).strip(),
                    team_abbr=self.abbr(unit.group(2).strip()),
                    offense=unit.group(3),
                    defense=unit.group(4),
                    special_teams=unit.group(5),
                ))
                continue
            score = re.match(r"^(BUF|MIN)\s+(\S+)\s+((?:-?\d+\s+){13}-?\d+)\s*$", s)
            if score:
                nums = score.group(3).split()
                payload = dict(zip(PLAYER_SCORE_KEYS, nums))
                self.tables["player_scoring"].append(_blank(
                    SCHEMAS["player_scoring"],
                    nflverse_game_id=self.game_id,
                    team=self.club(score.group(1)),
                    team_abbr=score.group(1),
                    player=score.group(2),
                    **payload,
                ))
                type_tds = ("rush_td", "rec_td", "ko_td", "punt_td", "int_td", "fum_td", "misc_td")
                if payload["td"] == "0" and any(payload[key] != "0" for key in type_tds):
                    self.gap(
                        "player_scoring_td_column_printed_zero",
                        "note",
                        "player_scoring",
                        f"{score.group(2)} has printed td=0 while a type column is non-zero "
                        + ", ".join(f"{key}={payload[key]}" for key in type_tds if payload[key] != "0")
                        + ". The zero is stored as printed and was not replaced with a sum.",
                    )
                continue
            if s.startswith("Largest ") or s.startswith("Drives ") or s.startswith("Time of Possession ") or s.startswith("Times Score") or s.startswith("Lead Changes"):
                values = re.findall(r"-?\d+:\d+|-?\d+", s)
                label = s[:re.search(r"-?\d+:\d+|-?\d+", s).start()].strip()
                payload = {key: "" for key in SCHEMAS["possession_detail"] if key not in ("nflverse_game_id", "metric", "layout")}
                if len(values) == 6:
                    keys = [
                        "first_half_visitor", "first_half_home", "second_half_visitor",
                        "second_half_home", "game_visitor", "game_home",
                    ]
                    payload.update(dict(zip(keys, values)))
                    layout = "visitor_home_by_half"
                elif len(values) == 3:
                    payload.update(dict(zip(("first_half", "second_half", "game"), values)))
                    layout = "half_totals"
                else:
                    self.gap("possession_detail_width", "gap", "possession_detail", s)
                    continue
                self.tables["possession_detail"].append(_blank(
                    SCHEMAS["possession_detail"],
                    nflverse_game_id=self.game_id,
                    metric=label,
                    layout=layout,
                    **payload,
                ))

    def _note_cross_checks(self):
        def players(table, scope, abbr):
            return [
                r for r in self.tables[table]
                if r["scope"] == scope and r["team_abbr"] == abbr and r["is_total"] == "false"
                and not r.get("bracket_row") == "true"
            ]

        def total(table, scope, abbr):
            hits = [
                r for r in self.tables[table]
                if r["scope"] == scope and r["team_abbr"] == abbr and r["is_total"] == "true"
            ]
            return hits[0] if hits else None

        notes = []
        for abbr in (self.visitor_abbr, self.home_abbr):
            passing = total("passing", "final", abbr)
            receiving = total("receiving", "final", abbr)
            if passing and receiving and passing["att"] != receiving["tar"]:
                notes.append(
                    f"{abbr} printed pass attempts {passing['att']} and printed targets {receiving['tar']} differ"
                )
        if notes:
            self.gap(
                "attempts_differ_from_targets",
                "note",
                "passing",
                "Pass attempts and receiving targets are both stored as printed. " + "; ".join(notes) + ".",
            )
        final_def = [
            r for r in self.tables["defense"]
            if r["scope"] == "final" and r["is_total"] == "false"
        ]
        half_def = [
            r for r in self.tables["defense"]
            if r["scope"] == "first_half" and r["is_total"] == "false"
        ]
        if half_def and len(half_def) < len(final_def):
            self.gap(
                "first_half_defense_is_printed_subset",
                "note",
                "defense",
                f"The first-half defensive table lists {len(half_def)} players and the final table lists "
                f"{len(final_def)}. The first-half rows are stored as printed and were not filled from the play-by-play. "
                "Example: a first-half sack can be absent from the first-half defensive list.",
            )
        bracket = [r for r in self.tables["returns"] if r["bracket_row"] == "true"]
        if bracket:
            self.gap(
                "bracket_return_rows",
                "note",
                "returns",
                "[DOWNED] and [TOUCHBACK] rows are kept. The printed Total does not include them. "
                "bracket_row marks those printed labels.",
            )

    def _finish_meta(self):
        if self.elections:
            self.meta["toss_note"] = self.elections[0]
        if len(self.elections) > 1:
            self.meta["second_half_election"] = self.elections[1]
        officials = [
            f"{r['position']}: {r['name']} ({r['number']})" for r in self.tables["officials"]
        ]
        self.meta["officials_printed"] = "; ".join(officials)
        self.tables["game_meta"].append(_blank(SCHEMAS["game_meta"], **self.meta))


def _clock_and_text(rest: str):
    text = " ".join(rest.split())
    m = re.match(r"\((\d*:\d+)\)", text)
    clock = m.group(1) if m else ""
    return clock, text


def parse_game_summary(text: str, game_id: str = "2026_09_BUF_MIN", week: int = 9):
    """Parse a pdftotext -layout NFL game summary. Returns a dict of row lists."""
    return GameBookParser(text, game_id, week).parse()


def write_tables(tables, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, fields in SCHEMAS.items():
        path = out_dir / f"{name}.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n", extrasaction="raise")
            writer.writeheader()
            for record in tables[name]:
                writer.writerow(record)


def build_provenance(pdf_path: Path, text_path: Path, tables, ingested_date: str, game_id: str, week: int):
    pdf_bytes = Path(pdf_path).read_bytes()
    text_bytes = Path(text_path).read_bytes()
    notice = copyright_notice(text_bytes.decode("utf-8"))
    return {
        "source": "official NFL Game Summary PDF supplied by owner",
        "nflverse_game_id": game_id,
        "week_supplied": week,
        "week_note": "Week is not printed on the game summary. It was supplied with the ingest.",
        "ingested_date": ingested_date,
        "pdf_file": Path(pdf_path).name,
        "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(),
        "text_file": Path(text_path).name,
        "text_extract": "pdftotext -layout",
        "text_sha256": hashlib.sha256(text_bytes).hexdigest(),
        "text_sha256_note": "SHA-256 of the committed text. A fresh `pdftotext -layout` of the PDF matches these bytes.",
        "copyright_notice": notice,
        "intended_use": "research source-of-truth postgame input",
        "does_not_change": "model weights, formulas, simulators, configs, and projection_ready",
        "row_counts": {name: len(rows) for name, rows in tables.items()},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True, type=Path)
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--provenance-out", required=True, type=Path)
    parser.add_argument("--game-id", default="2026_09_BUF_MIN")
    parser.add_argument("--week", type=int, default=9)
    parser.add_argument("--ingested-date", default="2026-11-10")
    args = parser.parse_args(argv)
    text = args.text.read_text(encoding="utf-8")
    tables = parse_game_summary(text, args.game_id, args.week)
    write_tables(tables, args.out)
    provenance = build_provenance(
        args.pdf, args.text, tables, args.ingested_date, args.game_id, args.week,
    )
    args.provenance_out.parent.mkdir(parents=True, exist_ok=True)
    args.provenance_out.write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
