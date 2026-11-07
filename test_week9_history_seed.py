"""Offline regression for the verified Week 9 research-only historical seed.

Never computes sportsbook prices, Q1-Q4 predictions, or publishes wagers.
Historical positive-opportunity averages remain NOT full opportunity forecasts.
"""
import csv
import datetime as dt
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OFFENSE = ROOT / "research/WEEK9_VERIFIED_HISTORICAL_REFERENCE_20261107.csv"
COMBINED = ROOT / "research/WEEK9_HISTORICAL_RUSH_RECEIVE_REFERENCE_20261107.csv"
DEFENSE = ROOT / "research/WEEK9_DEFENSE_ALLOWED_HISTORICAL_REFERENCE_20261107.csv"
SLATE = [
    ("CIN", "ATL"), ("DEN", "CAR"), ("DAL", "IND"),
    ("NYJ", "KC"), ("DET", "MIA"), ("CLE", "NO"), ("NYG", "PHI"),
    ("LA", "WAS"), ("HOU", "LAC"), ("LV", "SF"), ("GB", "NE"),
    ("ARI", "SEA"), ("TB", "CHI"),
]
TEAMS = set(sum(([a, h] for a, h in SLATE), []))
EVENTS = {f"{a}@{h}" for a, h in SLATE}
VALID_MARKETS = {
    "player_pass_yds", "player_receptions", "player_reception_yds", "player_rush_yds",
}


def load(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class SundayResearchInputAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.player_rows, cls.combined, cls.defenses = load(OFFENSE), load(COMBINED), load(DEFENSE)

    def test_complete_sunday_source_coverage_not_forecasts(self):
        self.assertEqual(len(self.player_rows), 283)
        self.assertEqual(len(self.combined), 104)
        self.assertEqual(len(self.defenses), 26)
        self.assertEqual({x["team"] for x in self.player_rows}, TEAMS)
        self.assertEqual({x["team"] for x in self.combined}, TEAMS)
        self.assertEqual({x["defense_team"] for x in self.defenses}, TEAMS)
        self.assertEqual({x["event"] for x in self.player_rows}, EVENTS)
        self.assertEqual({x["event"] for x in self.combined}, EVENTS)
        self.assertEqual(len(EVENTS), 13)

    def test_observed_player_ids_and_game_dates(self):
        seen = set()
        for x in self.player_rows:
            key = (x["team"], x["player_id"], x["market_key"])
            self.assertNotIn(key, seen)
            seen.add(key)
            self.assertRegex(x["player_id"], r"^00-\d{7}$")
            self.assertIn(x["market_key"], VALID_MARKETS)
            self.assertGreaterEqual(int(x["positive_opportunity_games"]), 3)
            self.assertGreater(float(x["total_opportunities"]), 0)
            self.assertLess(dt.date.fromisoformat(x["last_observed_game"]), dt.date(2026, 11, 8))
            self.assertEqual(x["bet_eligible"], "false")
            self.assertEqual(x["data_status"], "HISTORICAL_POSITIVE_OPPORTUNITY_GAMES_NOT_PROJECTION")

    def test_combined_history_same_game_stat_means(self):
        seen = set()
        for x in self.combined:
            key = (x["team"], x["player_id"])
            self.assertNotIn(key, seen)
            seen.add(key)
            self.assertRegex(x["player_id"], r"^00-\d{7}$")
            self.assertGreater(int(x["positive_opportunity_games"]), 2)
            combined = float(x["combined_mean"])
            rush = float(x["rushing_mean"])
            receiving = float(x["receiving_mean"])
            self.assertAlmostEqual(combined, rush + receiving, delta=0.021)
            self.assertLess(dt.date.fromisoformat(x["last_observed_game"]), dt.date(2026, 11, 8))
            self.assertEqual(x["bet_eligible"], "false")
            self.assertEqual(x["data_status"], "HISTORICAL_OPPORTUNITY_GAMES_ONLY_NOT_PROJECTION")

    def test_defensive_metrics_are_team_level_not_fake_charting(self):
        seen = set()
        for x in self.defenses:
            self.assertNotIn(x["defense_team"], seen)
            seen.add(x["defense_team"])
            self.assertIn(x["week9_offense"], TEAMS)
            self.assertGreater(int(x["completed_games_w1_8"]), 0)
            self.assertLess(dt.date.fromisoformat(x["last_game"]), dt.date(2026, 11, 8))
            for absent in (
                "blitz_rate", "pressure_rate", "man_zone", "mofo_mofc",
                "explosive_passes_allowed", "player_responsibility",
            ):
                self.assertEqual(x[absent], "")
            self.assertEqual(
                x["data_status"], "COARSE_TEAM_DEFENSE_HISTORY_ONLY_NOT_COVERAGE_CHARTING",
            )


if __name__ == "__main__":
    unittest.main()
