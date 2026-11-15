"""Schema and integrity checks for the 2026 scheme and opportunity profiles.

No network. The evidence file is the committed extract. Counts are recomputed
from it. Missing rates stay unknown. Overtime plays stay out of regulation.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import jsonschema
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from build_profiles import (  # noqa: E402
    LAST_PROFILE_DATE,
    PBP_RETRIEVED,
    PBP_URL,
    WEEK10_GAME,
    aggregate_side,
    load_evidence,
    player_window,
)

OUT = ROOT / "2026"
TEAMS = OUT / "teams"
SCHEMA = json.loads((ROOT / "schema" / "team_profile.schema.json").read_text())
VALIDATOR = jsonschema.Draft7Validator(SCHEMA, format_checker=jsonschema.Draft7Validator.FORMAT_CHECKER)


def play(**overrides):
    row = {
        "game_id": "2026_01_AA_BB",
        "play_id": 1,
        "season": 2026,
        "week": 1,
        "game_date": "2026-09-10",
        "home_team": "BB",
        "away_team": "AA",
        "posteam": "AA",
        "defteam": "BB",
        "qtr": 1,
        "down": 1,
        "ydstogo": 10,
        "yardline_100": 75,
        "score_differential": 0,
        "play_type": "run",
        "sack": 0,
        "qb_scramble": 0,
        "shotgun": 0,
        "passer_player_id": None,
        "passer_player_name": None,
        "rusher_player_id": "RB1",
        "rusher_player_name": "A.Back",
        "receiver_player_id": None,
        "receiver_player_name": None,
        "yards_gained": 3,
        "complete_pass": 0,
        "touchdown": 0,
        "run_location": "left",
        "run_gap": "end",
        "third_down_converted": 0,
        "third_down_failed": 0,
        "fixed_drive": 1,
        "field_goal_result": None,
        "two_point_attempt": 0,
    }
    row.update(overrides)
    return row


class SchemaAndProvenanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profiles = {}
        for path in sorted(TEAMS.glob("*.json")):
            cls.profiles[path.stem] = json.loads(path.read_text())
        cls.manifest = json.loads((OUT / "manifest.json").read_text())
        cls.crosscheck = json.loads((OUT / "crosscheck_gamebooks.json").read_text())
        cls.evidence = load_evidence(OUT / "evidence_plays.csv.gz")

    def test_thirty_two_profiles_match_the_schema(self):
        self.assertEqual(len(self.profiles), 32)
        for team, profile in self.profiles.items():
            errors = sorted(VALIDATOR.iter_errors(profile), key=lambda err: list(err.path))
            self.assertEqual(errors, [], f"{team}: {errors[:3]}")
            self.assertIs(profile["projection_ready"], False)
            self.assertEqual(profile["team"], team)

    def test_projection_ready_stays_false_on_every_output(self):
        self.assertIs(self.manifest["projection_ready"], False)
        self.assertIs(self.crosscheck["projection_ready"], False)
        for path in OUT.rglob("*"):
            if path.suffix not in {".json", ".md"}:
                continue
            text = path.read_text()
            self.assertNotIn('"projection_ready": true', text)
            self.assertNotIn("projection_ready is true", text)
            self.assertNotIn("projection_ready=true", text)

    def test_blocked_fields_are_unknown(self):
        for team, profile in self.profiles.items():
            for key, field in profile["blocked"].items():
                self.assertEqual(field["status"], "BLOCKED", team)
                self.assertEqual(field["value"], "unknown", key)
                self.assertIs(field["observed"], False)
            offense = profile["regulation"]["offense"]
            self.assertEqual(offense["official_explosive_label"]["value"], "unknown")
            self.assertEqual(offense["official_red_zone_trip_efficiency"]["value"], "unknown")

    def test_every_metric_cites_the_play_by_play_pull(self):
        def walk(node):
            if isinstance(node, dict):
                if node.get("kind") in {"count", "rate", "rate_difference", "target", "carry"}:
                    self.assertEqual(node["source_url"], PBP_URL)
                    self.assertEqual(node["retrieved_utc"], PBP_RETRIEVED)
                if node.get("kind") in {"count", "rate", "rate_difference"}:
                    self.assertTrue(node["definition"])
                    if node["value"] == "unknown":
                        self.assertIs(node["observed"], False)
                    if node["value"] == 0:
                        self.assertIs(node["observed"], True)
                    if node["kind"] == "rate" and node["denominator"] == 0:
                        self.assertEqual(node["value"], "unknown")
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        for profile in self.profiles.values():
            walk(profile)

    def test_no_future_games_and_only_the_reviewed_week_10_game(self):
        included = {row["game_id"] for row in self.manifest["games"] if row["included_in_profiles"]}
        excluded = {row["game_id"] for row in self.manifest["games"] if not row["included_in_profiles"]}
        evidence_ids = set(self.evidence["game_id"])
        self.assertTrue(excluded.isdisjoint(evidence_ids))
        self.assertEqual(evidence_ids, included)
        self.assertLessEqual(self.evidence["game_date"].max(), LAST_PROFILE_DATE)
        self.assertEqual(set(self.evidence.loc[self.evidence["week"] == 10, "game_id"]), {WEEK10_GAME})
        self.assertTrue((self.evidence["week"] <= 10).all())
        for row in self.manifest["games"]:
            if not row["final"]:
                self.assertIsNone(row["away_score"])
                self.assertIsNone(row["home_score"])
                self.assertNotIn("spread", json.dumps(row))

    def test_play_ids_join_to_one_game_and_recompute(self):
        dupes = self.evidence.duplicated(["game_id", "play_id"])
        self.assertFalse(dupes.any())
        for team, profile in self.profiles.items():
            ids = profile["window"]["game_ids"]
            self.assertEqual(len(ids), len(set(ids)))
            offense = aggregate_side(self.evidence, team, "offense", "regulation", ids)
            published = profile["regulation"]["offense"]
            for key in ("early_down_pass_rate", "third_down_conversion_rate", "scrimmage_plays", "qb_kneels"):
                self.assertEqual(offense[key]["numerator"], published[key]["numerator"], f"{team} {key}")
                self.assertEqual(offense[key]["value"], published[key]["value"], f"{team} {key}")
            overtime = aggregate_side(self.evidence, team, "offense", "overtime", ids)
            self.assertEqual(
                overtime["scrimmage_plays"]["value"],
                profile["overtime"]["offense"]["scrimmage_plays"]["value"],
                team,
            )

    def test_regulation_and_overtime_are_separate_denominators(self):
        saw_overtime = False
        saw_empty_overtime = False
        for team, profile in self.profiles.items():
            ids = set(profile["window"]["game_ids"])
            rows = self.evidence[(self.evidence["posteam"] == team) & self.evidence["game_id"].isin(ids)]
            rows = rows[pd.to_numeric(rows["two_point_attempt"], errors="coerce") != 1]
            regulation = rows[(pd.to_numeric(rows["qtr"], errors="coerce") <= 4) & rows["play_type"].isin(["pass", "run"])]
            overtime = rows[(pd.to_numeric(rows["qtr"], errors="coerce") >= 5) & rows["play_type"].isin(["pass", "run"])]
            self.assertEqual(profile["regulation"]["offense"]["scrimmage_plays"]["value"], len(regulation))
            self.assertEqual(profile["overtime"]["offense"]["scrimmage_plays"]["value"], len(overtime))
            if len(overtime):
                saw_overtime = True
            else:
                saw_empty_overtime = True
                rate = profile["overtime"]["offense"]["early_down_pass_rate"]
                self.assertEqual(rate["value"], "unknown")
                self.assertIs(rate["observed"], False)
                self.assertEqual(profile["overtime"]["offense"]["scrimmage_plays"]["value"], 0)
                self.assertIs(profile["overtime"]["offense"]["scrimmage_plays"]["observed"], True)
        self.assertTrue(saw_overtime)
        self.assertTrue(saw_empty_overtime)

    def test_direction_unknown_is_not_assigned_and_splits_partition(self):
        for team, profile in self.profiles.items():
            offense = profile["regulation"]["offense"]
            early = offense["early_down_pass_plays"]["value"] + offense["early_down_run_plays"]["value"]
            self.assertEqual(early, offense["early_down_plays"]["value"])
            score = (
                offense["neutral_plays"]["value"]
                + offense["leading_plays"]["value"]
                + offense["trailing_plays"]["value"]
                + offense["unknown_score_plays"]["value"]
            )
            self.assertEqual(score, offense["scrimmage_plays"]["value"])
            third = (
                offense["third_down_conversions"]["value"]
                + offense["third_down_failures"]["value"]
                + offense["third_down_unknown_results"]["value"]
            )
            self.assertEqual(third, offense["third_down_plays"]["value"])
            direction = offense["rush_direction"]
            located = sum(direction[label]["plays"]["value"] for label in ("left", "middle", "right"))
            self.assertEqual(located + direction["unknown"]["value"], direction["plays"]["value"])
            targets = profile["players"]["season"]["targets"]
            if targets:
                self.assertEqual(sum(row["plays"] for row in targets), targets[0]["team_plays"])

    def test_week_9_and_week_10_gamebooks_match_on_the_checked_fields(self):
        games = self.crosscheck["games"]
        self.assertEqual(len(games), 16)
        self.assertEqual({row["status"] for row in games}, {"MATCH"})
        self.assertIn(WEEK10_GAME, {row["game_id"] for row in games})
        week10 = next(row for row in games if row["game_id"] == WEEK10_GAME)
        self.assertIs(week10["persisted_in_repo"], False)
        self.assertTrue(week10["sha256"])
        self.assertTrue(week10["source_url"].startswith("https://"))
        week9 = [row for row in games if row["game_id"] != WEEK10_GAME]
        self.assertTrue(all(row["persisted_in_repo"] for row in week9))

    def test_verified_batch_is_written_before_the_league_table(self):
        coverage = (OUT / "COVERAGE.md").read_text()
        batch = (OUT / "verified_batch_was_nyg.md").read_text()
        self.assertIn("Verified batch: Washington", batch)
        self.assertLess(coverage.index("Verified batch"), coverage.index("## League coverage"))
        self.assertIn("0 of 32", coverage)
        self.assertIn("32", coverage)
        was = (TEAMS / "WAS.md").read_text()
        self.assertIn("unknown", was)
        self.assertIn("2026_10_WAS_NYG", was)


class SyntheticRuleTest(unittest.TestCase):
    def test_missing_direction_overtime_and_two_point_rules(self):
        frame = pd.DataFrame([
            play(play_id=1, play_type="run", run_location=None, run_gap=None, qtr=1, down=1),
            play(play_id=2, play_type="pass", qtr=5, down=1, receiver_player_id="WR1", receiver_player_name="B.Wide", yards_gained=20, complete_pass=1),
            play(play_id=3, play_type="qb_kneel", qtr=4, down=3, third_down_failed=1, rusher_player_id="QB1", rusher_player_name="C.Quarter"),
            play(play_id=4, play_type="pass", qtr=2, down=None, two_point_attempt=1, receiver_player_id="WR1", receiver_player_name="B.Wide"),
        ])
        ids = ["2026_01_AA_BB"]
        regulation = aggregate_side(frame, "AA", "offense", "regulation", ids)
        overtime = aggregate_side(frame, "AA", "offense", "overtime", ids)
        self.assertEqual(regulation["scrimmage_plays"]["value"], 1)
        self.assertEqual(regulation["rush_direction"]["unknown"]["value"], 1)
        self.assertEqual(regulation["rush_direction"]["left"]["plays"]["value"], 0)
        self.assertIs(regulation["rush_direction"]["left"]["plays"]["observed"], True)
        self.assertEqual(regulation["third_down_plays"]["value"], 1)
        self.assertEqual(regulation["third_down_failures"]["value"], 1)
        self.assertEqual(regulation["two_point_attempts"]["value"], 1)
        self.assertEqual(overtime["scrimmage_plays"]["value"], 1)
        self.assertEqual(overtime["early_down_pass_plays"]["value"], 1)
        self.assertNotEqual(regulation["early_down_pass_plays"]["value"], 1)
        empty = aggregate_side(frame.iloc[0:0], "AA", "offense", "overtime", ids)
        self.assertEqual(empty["scrimmage_plays"]["value"], 0)
        self.assertEqual(empty["early_down_pass_rate"]["value"], "unknown")
        self.assertIs(empty["early_down_pass_rate"]["observed"], False)
        window = player_window(frame, "AA", ids, 5)
        self.assertEqual([row["player_id"] for row in window["carries"]], ["RB1"])
        self.assertEqual([row["player_id"] for row in window["targets"]], ["WR1"])
        self.assertEqual(window["targets"][0]["plays"], 1)
        self.assertEqual(window["status"], "PARTIAL")


if __name__ == "__main__":
    unittest.main()
