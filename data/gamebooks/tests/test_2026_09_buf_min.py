"""Reconciliation checks for the 2026 week 9 BUF at MIN official game summary.

Numbers asserted here are the figures printed in the game summary, not
recomputed rates. Week and the nflverse game id are supplied identifiers.
"""

import csv
import hashlib
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from parse_nfl_game_summary import SCHEMAS, copyright_notice, parse_game_summary  # noqa: E402

GAME_DIR = REPO / "data" / "gamebooks" / "2026" / "wk09" / "2026_09_BUF_MIN"
TEXT_PATH = GAME_DIR / "2026_09_BUF_MIN_gamebook.txt"
PDF_PATH = GAME_DIR / "2026_09_BUF_MIN_gamebook.pdf"
PARSED = GAME_DIR / "parsed"
PROVENANCE = GAME_DIR / "provenance.json"
PDF_SHA256 = "056ac51502fffbff963f8c7ab1b425a6965e3631cc77b9d84890c3beb502f7a2"
TEXT_SHA256 = "189329381c78d5a032ba7e58627caad7e6dcb5b43504eef0fc2eda0a64a598d3"


def rows(table, **filters):
    return [row for row in table if all(row[key] == value for key, value in filters.items())]


def one(table, **filters):
    found = rows(table, **filters)
    if len(found) != 1:
        raise AssertionError(f"expected 1 row for {filters}, found {len(found)}")
    return found[0]


def as_int(value):
    return int(value)


def clock_seconds(value):
    minutes, seconds = value.split(":")
    return int(minutes) * 60 + int(seconds)


class BufMinWeek9GamebookTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = TEXT_PATH.read_text(encoding="utf-8")
        cls.tables = parse_game_summary(cls.text, game_id="2026_09_BUF_MIN", week=9)

    def test_pdf_and_text_bytes(self):
        self.assertEqual(hashlib.sha256(PDF_PATH.read_bytes()).hexdigest(), PDF_SHA256)
        self.assertEqual(hashlib.sha256(TEXT_PATH.read_bytes()).hexdigest(), TEXT_SHA256)
        notice = copyright_notice(self.text)
        self.assertIn("NFL Copyright © 2026 by The National Football League", notice)
        self.assertIn(
            "any other use of this material is prohibited without the written permission of the National Football League",
            notice,
        )

    def test_provenance_file(self):
        provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
        self.assertEqual(provenance["source"], "official NFL Game Summary PDF supplied by owner")
        self.assertEqual(provenance["ingested_date"], "2026-11-10")
        self.assertEqual(provenance["pdf_sha256"], PDF_SHA256)
        self.assertEqual(provenance["text_sha256"], TEXT_SHA256)
        self.assertEqual(provenance["nflverse_game_id"], "2026_09_BUF_MIN")
        self.assertEqual(provenance["week_supplied"], 9)
        self.assertIn("prohibited without the written permission", provenance["copyright_notice"])
        self.assertNotIn("projection_ready", provenance)
        for name, records in self.tables.items():
            self.assertEqual(provenance["row_counts"][name], len(records))

    def test_committed_csvs_match_parser(self):
        for name, fields in SCHEMAS.items():
            path = PARSED / f"{name}.csv"
            self.assertTrue(path.exists(), path)
            with path.open(newline="", encoding="utf-8") as handle:
                loaded = list(csv.DictReader(handle))
            self.assertEqual(loaded, self.tables[name], name)
            if loaded:
                self.assertEqual(list(loaded[0].keys()), fields)

    def test_game_meta_and_score(self):
        meta = one(self.tables["game_meta"])
        self.assertEqual(meta["date_printed"], "Monday, 11/9/2026")
        self.assertEqual(meta["date_iso"], "2026-11-09")
        self.assertEqual(meta["start_time"], "7:16 PM CST")
        self.assertEqual(meta["venue"], "U.S. Bank Stadium, Minneapolis, MN")
        self.assertEqual(meta["roof"], "Indoors")
        self.assertEqual(meta["stadium_printed"], "Closed Stadium on Field Turf")
        self.assertEqual(meta["temp_printed"], "52° F (11.1° C)")
        self.assertEqual(meta["humidity_printed"], "61%")
        self.assertEqual(meta["wind_printed"], "W 6 mph")
        self.assertEqual(meta["outdoor_weather"], "Cloudy")
        self.assertEqual(meta["attendance_printed"], "66,955")
        self.assertEqual(meta["game_duration"], "3:11")
        self.assertEqual(meta["visitor_final"], "23")
        self.assertEqual(meta["home_final"], "6")
        self.assertIn("wins toss", meta["toss_note"])
        self.assertIn("MIN elects to Receive", meta["second_half_election"])
        self.assertEqual(len(self.tables["officials"]), 8)
        referee = one(self.tables["officials"], position="Referee")
        self.assertEqual(referee["name"], "Cheffers, Carl")
        self.assertEqual(referee["number"], "51")
        replay = one(self.tables["officials"], position="Replay Official")
        self.assertEqual(replay["number"], "0")
        self.assertEqual(one(self.tables["officials"], position="Side Judge")["number"], "114")

        by_team = {}
        for row in self.tables["quarter_scores"]:
            by_team.setdefault(row["team_abbr"], {})[row["quarter"]] = as_int(row["points"])
        for abbr, final in (("BUF", 23), ("MIN", 6)):
            self.assertEqual(
                by_team[abbr]["1"] + by_team[abbr]["2"] + by_team[abbr]["3"] + by_team[abbr]["4"] + by_team[abbr]["OT"],
                final,
            )
            self.assertEqual(by_team[abbr]["Total"], final)
        self.assertEqual(by_team["BUF"]["OT"], 0)
        self.assertEqual(by_team["MIN"]["1"], 0)
        last = self.tables["scoring_plays"][-1]
        self.assertEqual((last["visitor_score"], last["home_score"]), ("23", "6"))
        self.assertEqual(len(self.tables["scoring_plays"]), 7)
        cook = one(self.tables["scoring_plays"], description="J.Cook 5 yd. run (T.Bass kick) (15-84, 8:32)")
        self.assertEqual((cook["quarter"], cook["time"], cook["drive_plays"], cook["drive_yards"], cook["drive_time"]),
                         ("4", "6:17", "15", "84", "8:32"))

    def test_final_individual_totals(self):
        passing = one(self.tables["passing"], scope="final", team_abbr="BUF", player="Total")
        self.assertEqual((passing["cmp"], passing["att"], passing["yds"], passing["sk_yd"]), ("21", "31", "234", "4/29"))
        allen = one(self.tables["passing"], scope="final", team_abbr="BUF", player="J.Allen")
        self.assertEqual((allen["cmp"], allen["att"], allen["yds"], allen["rt"]), ("21", "31", "234", "87.3"))
        wentz = one(self.tables["passing"], scope="final", team_abbr="MIN", player="C.Wentz")
        brosmer = one(self.tables["passing"], scope="final", team_abbr="MIN", player="M.Brosmer")
        min_pass = one(self.tables["passing"], scope="final", team_abbr="MIN", player="Total")
        self.assertEqual((wentz["att"], wentz["cmp"], wentz["yds"]), ("25", "8", "81"))
        self.assertEqual((brosmer["att"], brosmer["cmp"], brosmer["yds"], brosmer["rt"]), ("7", "6", "58", "101.2"))
        self.assertEqual(as_int(wentz["att"]) + as_int(brosmer["att"]), as_int(min_pass["att"]))
        self.assertEqual(as_int(wentz["cmp"]) + as_int(brosmer["cmp"]), as_int(min_pass["cmp"]))
        self.assertEqual(as_int(wentz["yds"]) + as_int(brosmer["yds"]), as_int(min_pass["yds"]))
        self.assertEqual((min_pass["att"], min_pass["cmp"], min_pass["yds"], min_pass["sk_yd"]), ("32", "14", "139", "2/12"))

        cook = one(self.tables["rushing"], scope="final", team_abbr="BUF", player="J.Cook")
        self.assertEqual((cook["att"], cook["yds"], cook["td"], cook["avg"]), ("31", "107", "1", "3.5"))
        self._sums_match("rushing", "final", "BUF", ["att", "yds", "td"])
        self._sums_match("rushing", "final", "MIN", ["att", "yds", "td"])
        self.assertEqual(
            (one(self.tables["rushing"], scope="final", team_abbr="BUF", player="Total")["att"],
             one(self.tables["rushing"], scope="final", team_abbr="BUF", player="Total")["yds"]),
            ("44", "134"),
        )
        self.assertEqual(
            (one(self.tables["rushing"], scope="final", team_abbr="MIN", player="Total")["att"],
             one(self.tables["rushing"], scope="final", team_abbr="MIN", player="Total")["yds"]),
            ("12", "51"),
        )
        self.assertEqual(one(self.tables["rushing"], scope="final", player="K.Allen")["yds"], "-2")

        self._sums_match("receiving", "final", "BUF", ["tar", "rec", "yds", "td"])
        self._sums_match("receiving", "final", "MIN", ["tar", "rec", "yds", "td"])
        buf_rec = one(self.tables["receiving"], scope="final", team_abbr="BUF", player="Total")
        min_rec = one(self.tables["receiving"], scope="final", team_abbr="MIN", player="Total")
        self.assertEqual((buf_rec["tar"], buf_rec["rec"], buf_rec["yds"]), ("29", "21", "234"))
        self.assertEqual((min_rec["tar"], min_rec["rec"], min_rec["yds"]), ("30", "14", "139"))
        self.assertEqual(one(self.tables["receiving"], scope="final", player="K.Shakir")["tar"], "4")
        self.assertEqual(one(self.tables["receiving"], scope="final", player="J.Jefferson")["tar"], "11")
        # Attempts and targets are both printed and are not the same number.
        self.assertNotEqual(passing["att"], buf_rec["tar"])
        self.assertEqual(passing["cmp"], buf_rec["rec"])
        self.assertEqual(passing["yds"], buf_rec["yds"])

        self._sums_match("interceptions", "final", "BUF", ["no", "yds"])
        self._sums_match("interceptions", "final", "MIN", ["no", "yds"])
        self.assertEqual(one(self.tables["interceptions"], scope="final", team_abbr="BUF", player="Total")["no"], "2")
        self.assertEqual(one(self.tables["interceptions"], scope="final", team_abbr="MIN", player="Total")["no"], "1")
        self.assertEqual(passing["int"], "1")
        self.assertEqual(min_pass["int"], "2")

        doman = one(self.tables["punting"], scope="final", player="T.Doman")
        thorson = one(self.tables["punting"], scope="final", player="B.Thorson")
        self.assertEqual((doman["no"], doman["yds"], doman["avg"], doman["net"]), ("5", "228", "45.6", "35.2"))
        self.assertEqual((thorson["no"], thorson["yds"], thorson["avg"], thorson["net"], thorson["lg"]),
                         ("5", "240", "48.0", "45.8", "66"))

        self.assertEqual(one(self.tables["fumbles"], scope="final", player="C.Wentz")["own_rec_yds"], "-3")
        self.assertEqual(one(self.tables["fumbles"], scope="final", player="C.Wentz")["lost"], "1")
        min_fum = one(self.tables["fumbles"], scope="final", team_abbr="MIN", player="Total")
        self.assertEqual((min_fum["fum"], min_fum["lost"], min_fum["own_rec"], min_fum["own_rec_yds"]),
                         ("2", "1", "1", "5"))
        buf_fum = one(self.tables["fumbles"], scope="final", team_abbr="BUF", player="Total")
        self.assertEqual((buf_fum["fum"], buf_fum["lost"]), ("0", "0"))

    def test_defense_and_first_half_not_mixed(self):
        rousseau = one(self.tables["defense"], scope="final", player="G.Rousseau")
        self.assertEqual((rousseau["sk"], rousseau["sk_yds"], rousseau["fr"]), ("1", "6", "1"))
        grable = one(self.tables["defense"], scope="final", player="T.Grable")
        self.assertEqual(grable["misc_tkl"], "1")
        self.assertEqual(grable["tkl"], "0")
        yurosek = one(self.tables["defense"], scope="final", player="B.Yurosek")
        self.assertEqual(yurosek["st_fr"], "1")
        self.assertEqual(yurosek["tkl"], "0")
        pace = one(self.tables["defense"], scope="final", player="I.Pace")
        self.assertEqual((pace["sk"], pace["sk_yds"], pace["st_tkl"]), ("1", "9", "1"))
        self.assertEqual(one(self.tables["defense"], scope="final", player="A.Van Ginkel")["player"], "A.Van Ginkel")
        self.assertEqual(one(self.tables["defense"], scope="final", player="K.Van Noy")["player"], "K.Van Noy")
        redmond = one(self.tables["defense"], scope="final", player="J.Redmond")
        self.assertEqual((redmond["sk"], redmond["sk_yds"]), ("0.5", "2.5"))
        ingram = one(self.tables["defense"], scope="final", player="T.Ingram-Dawkins")
        self.assertEqual((ingram["sk"], ingram["sk_yds"]), ("0.5", "2.5"))

        for abbr, sk, yards, comb in (("BUF", "2", "12", "35"), ("MIN", "4", "29", "87")):
            total = one(self.tables["defense"], scope="final", team_abbr=abbr, player="Total")
            self.assertEqual((total["sk"], total["sk_yds"], total["comb"]), (sk, yards, comb))
            players = rows(self.tables["defense"], scope="final", team_abbr=abbr, is_total="false")
            self.assertEqual(sum((Decimal(r["sk"]) for r in players), Decimal(0)), Decimal(sk))
            self.assertEqual(sum((Decimal(r["sk_yds"]) for r in players), Decimal(0)), Decimal(yards))
            self.assertEqual(sum(as_int(r["tkl"]) for r in players), as_int(total["tkl"]))
            self.assertEqual(sum(as_int(r["ast"]) for r in players), as_int(total["ast"]))
            for row in players + [total]:
                self.assertEqual(as_int(row["tkl"]) + as_int(row["ast"]), as_int(row["comb"]))

        half_cook = one(self.tables["rushing"], scope="first_half", player="J.Cook")
        self.assertEqual((half_cook["att"], half_cook["yds"]), ("15", "33"))
        self.assertEqual(one(self.tables["rushing"], scope="first_half", team_abbr="BUF", player="Total")["att"], "18")
        self.assertEqual(one(self.tables["rushing"], scope="first_half", team_abbr="BUF", player="Total")["yds"], "40")
        self.assertEqual(one(self.tables["rushing"], scope="first_half", team_abbr="MIN", player="Total")["yds"], "17")
        half_allen = one(self.tables["passing"], scope="first_half", player="J.Allen")
        self.assertEqual((half_allen["att"], half_allen["cmp"], half_allen["yds"]), ("20", "13", "122"))
        self.assertEqual(len(rows(self.tables["defense"], scope="first_half", team_abbr="BUF", is_total="false")), 4)
        self.assertGreater(
            len(rows(self.tables["defense"], scope="final", team_abbr="BUF", is_total="false")),
            4,
        )

    def test_team_stats_drives_and_possession(self):
        def stat(scope, name):
            return one(self.tables["team_stats"], scope=scope, stat=name)

        final_score = stat("final", "FINAL SCORE")
        self.assertEqual((final_score["visitor"], final_score["home"]), ("23", "6"))
        rush = stat("final", "NET YARDS RUSHING")
        self.assertEqual((rush["visitor"], rush["home"]), ("134", "51"))
        plays = stat("final", "Total Rushing Plays")
        self.assertEqual((plays["visitor"], plays["home"]), ("44", "12"))
        gross = stat("final", "Gross yards passing")
        self.assertEqual((gross["visitor"], gross["home"]), ("234", "139"))
        attempts = stat("final", "PASS ATTEMPTS-COMPLETIONS-HAD INTERCEPTED")
        self.assertEqual((attempts["visitor"], attempts["home"]), ("31-21-1", "32-14-2"))
        thrown = stat("final", "Times thrown - yards lost attempting to pass")
        self.assertEqual((thrown["visitor"], thrown["home"]), ("4-29", "2-12"))
        top = stat("final", "TIME OF POSSESSION")
        self.assertEqual((top["visitor"], top["home"]), ("42:32", "17:28"))
        half_pass = stat("first_half", "Pass Attempts-Completions-Had Intercepted")
        self.assertEqual(half_pass["visitor"], "20 - 13 - 1")
        self.assertEqual(half_pass["home"], "17 - 7 - 0")

        buf_drives = rows(self.tables["drives"], team_abbr="BUF")
        min_drives = rows(self.tables["drives"], team_abbr="MIN")
        self.assertEqual(len(buf_drives), 13)
        self.assertEqual(len(min_drives), 12)
        self.assertEqual(buf_drives[6]["how_given_up"], "Touchdown")
        self.assertEqual((buf_drives[6]["plays"], buf_drives[6]["net_yards"]), ("8", "80"))
        self.assertEqual(buf_drives[2]["last_scrimmage"], "* MIN 21")
        self.assertEqual(min_drives[5]["how_given_up"], "Field Goal")
        self.assertEqual((min_drives[5]["plays"], min_drives[5]["yards_gained"]), ("4", "9"))

        buf_top = one(self.tables["time_of_possession"], team_abbr="BUF")
        min_top = one(self.tables["time_of_possession"], team_abbr="MIN")
        self.assertEqual(buf_top["ot"], "")
        self.assertEqual(
            (buf_top["q1"], buf_top["q2"], buf_top["q3"], buf_top["q4"], buf_top["total"]),
            ("12:27", "8:02", "10:39", "11:24", "42:32"),
        )
        self.assertEqual(
            sum(clock_seconds(buf_top[q]) for q in ("q1", "q2", "q3", "q4")),
            clock_seconds(buf_top["total"]),
        )
        self.assertEqual(
            sum(clock_seconds(min_top[q]) for q in ("q1", "q2", "q3", "q4")),
            clock_seconds(min_top["total"]),
        )
        self.assertEqual(clock_seconds(buf_top["total"]) + clock_seconds(min_top["total"]), 3600)

        q1 = one(self.tables["quarter_summaries"], quarter="1", team_abbr="BUF")
        self.assertEqual((q1["score"], q1["time_possession"], q1["third_down"], q1["total_first_downs"]),
                         ("3", "12:27", "4/8", "4"))
        q4 = one(self.tables["quarter_summaries"], quarter="4", team_abbr="BUF")
        self.assertEqual(q4["score"], "23")
        self.assertEqual(one(self.tables["quarter_summaries"], quarter="4", team_abbr="MIN")["score"], "6")

        marker = one(self.tables["drive_notes"], kind="chart_average", team_abbr="BUF")
        self.assertEqual((marker["printed_marker"], marker["value"]), ("(373)", "29"))
        self.assertEqual(one(self.tables["drive_notes"], kind="chart_average", team_abbr="MIN")["printed_marker"], "(443)")

    def test_rosters_returns_and_scoring_tables(self):
        self.assertEqual(len(self.tables["lineups"]), 44)
        self.assertEqual(one(self.tables["lineups"], player="J.Allen", unit="offense")["number"], "17")
        self.assertEqual(one(self.tables["lineups"], player="J.Cook")["position"], "RB")
        self.assertEqual(one(self.tables["lineups"], player="C.Wentz")["number"], "11")
        self.assertEqual(one(self.tables["lineups"], player="A.Van Ginkel")["position"], "OLB")
        self.assertEqual(one(self.tables["lineups"], player="Jac.Thomas")["number"], "29")
        self.assertEqual(one(self.tables["lineups"], player="T.Ingram-Dawkins")["number"], "90")
        self.assertEqual(one(self.tables["lineups"], player="B.O'Neill")["position"], "RT")
        subs = rows(self.tables["participation"], list_name="substitution")
        self.assertEqual(len(rows(subs, team_abbr="BUF")), 26)
        self.assertEqual(len(rows(subs, team_abbr="MIN")), 26)
        for player in ("S.Franklin", "J.Andreessen", "J.Solomon", "K.Latu", "T.Felton",
                       "C.Chambliss", "M.Bredeson", "B.Yurosek", "E.Williams", "K.Van Noy"):
            one(subs, player=player)
        self.assertEqual(one(subs, player="I.Pace")["number"], "0")
        inactive = rows(self.tables["participation"], list_name="not_active")
        self.assertEqual(len(inactive), 12)
        one(inactive, player="D.Dawkins")
        one(inactive, player="T.Jackson")
        one(inactive, player="K.Murray")
        one(inactive, player="Jak.Thomas")
        self.assertEqual(one(inactive, player="A.Anderson")["position"], "C/G")
        self.assertEqual(rows(self.tables["participation"], list_name="did_not_play"), [])

        made = rows(self.tables["field_goals"], result="made")
        self.assertEqual(sorted(r["distance"] for r in made if r["kicker"] == "T.Bass"), ["25", "39", "52"])
        self.assertEqual(sorted(r["distance"] for r in made if r["kicker"] == "W.Reichard"), ["43", "53"])
        self.assertEqual(rows(self.tables["field_goals"], result="missed"), [])

        self.assertEqual(len(self.tables["player_scoring"]), 4)
        bass = one(self.tables["player_scoring"], player="T.Bass")
        self.assertEqual((bass["fg"], bass["xp"], bass["points"], bass["td"]), ("3", "2", "11", "0"))
        cook = one(self.tables["player_scoring"], player="J.Cook")
        self.assertEqual((cook["td"], cook["rush_td"], cook["points"]), ("0", "1", "6"))
        self.assertEqual(one(self.tables["player_scoring"], player="K.Latu")["rec_td"], "1")
        self.assertEqual(one(self.tables["player_scoring"], player="W.Reichard")["fg"], "2")
        units = one(self.tables["touchdown_units"], team_abbr="BUF")
        self.assertEqual((units["offense"], units["defense"], units["special_teams"]), ("2", "0", "0"))
        lead = one(self.tables["possession_detail"], metric="Largest Lead")
        self.assertEqual(lead["game_visitor"], "17")
        tied = one(self.tables["possession_detail"], metric="Times Score Tied Up")
        self.assertEqual((tied["layout"], tied["first_half"], tied["second_half"], tied["game"]),
                         ("half_totals", "1", "0", "1"))

    def test_play_by_play_keeps_printed_text(self):
        plays = rows(self.tables["play_by_play"], row_kind="scrimmage")
        self.assertGreaterEqual(len(plays), 1)
        raw_plays = []
        in_pbp = False
        for line in self.text.splitlines():
            if "Play By Play" in line and "Quarter" in line:
                in_pbp = True
            if "Miscellaneous Statistics Report" in line:
                break
            if in_pbp and __import__("re").match(r"^[ \t]*[1-4]-\d+-(?:(?:BUF|MIN)[ \t]+\d+|50)\b", line):
                raw_plays.append(line)
        self.assertEqual(len(plays), len(raw_plays))
        first = plays[0]
        self.assertEqual((first["quarter"], first["down"], first["distance"], first["yardline"], first["clock"]),
                         ("1", "1", "10", "MIN 36", "14:52"))
        self.assertIn("J.Cook right guard to MIN 35 for 1 yard", first["description"])
        late = one(self.tables["play_by_play"], clock=":57", down="1", distance="10", yardline="BUF 13")
        self.assertTrue(late["description"].startswith("(:57)"))
        kneel = [r for r in plays if "kneels" in r["description"]]
        self.assertEqual(len(kneel), 4)
        self.assertEqual(sum(1 for r in plays if "spiked the ball" in r["description"]), 1)
        reversed_rows = rows(self.tables["play_by_play"], contains_reversed_text="true")
        self.assertEqual(len(reversed_rows), 4)
        fumble = next(r for r in reversed_rows if "FUMBLES (Aborted)" in r["description"])
        self.assertIn("REVERSED", fumble["description"])
        self.assertIn("pass incomplete short right to J.Jefferson", fumble["description"])
        sack = next(r for r in reversed_rows if "A.Van Ginkel" in r["description"] and "sacked" in r["description"])
        self.assertIn("FUMBLES (A.Van Ginkel)", sack["description"])
        self.assertIn("sacked at BUF 2 for -8 yards (A.Van Ginkel).", sack["description"])
        lateral = one(self.tables["play_by_play"], row_kind="scrimmage", quarter="3", down="2", distance="24")
        self.assertIn("Lateral to K.Shakir", lateral["description"])
        holding = next(r for r in plays if "Defensive Holding" in r["description"])
        self.assertIn("No Play", holding["description"])
        self.assertIn("X1", holding["description"])
        intercepted = next(r for r in plays if "B.Murphy to MIN 47 for 54 yards" in r["description"])
        self.assertIn("(T.Grable)", intercepted["description"])
        kick = next(r for r in self.tables["play_by_play"] if "FUMBLES (T.Doman)" in r["description"])
        self.assertEqual(kick["row_kind"], "kickoff")
        self.assertIn("B.Yurosek to MIN 45 for 8 yards", kick["description"])
        cook_td = next(r for r in plays if "J.Cook up the middle for 5 yards, TOUCHDOWN" in r["description"])
        self.assertEqual(cook_td["quarter"], "4")
        scores = rows(self.tables["play_by_play"], row_kind="score")
        self.assertEqual(len(scores), 7)
        self.assertTrue(any(r["description"].startswith("BUF 23 MIN 6,") for r in scores))
        self.assertEqual(len(self.tables["quarter_summaries"]), 8)
        gaps = [g for g in self.tables["parse_gaps"] if g["severity"] == "gap"]
        self.assertEqual([g["gap_id"] for g in gaps], ["longest_plays_unparsed"])

    def _sums_match(self, table, scope, abbr, fields):
        players = rows(self.tables[table], scope=scope, team_abbr=abbr, is_total="false")
        players = [r for r in players if r.get("bracket_row") != "true"]
        total = one(self.tables[table], scope=scope, team_abbr=abbr, player="Total")
        for field in fields:
            self.assertEqual(
                sum(as_int(r[field]) for r in players),
                as_int(total[field]),
                f"{table} {scope} {abbr} {field}",
            )


if __name__ == "__main__":
    unittest.main()
