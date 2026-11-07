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
EXPLOSIVES = ROOT / "research/WEEK9_DEFENSIVE_EXPLOSIVE_SACK_FLAG_RATES_20261107.csv"
TE_AUDIT = ROOT / "research/WEEK9_TE_USAGE_SOURCE_CROSSCHECK_20261107.csv"
MATCHUP = ROOT / "research/WEEK9_PLAYER_DEFENSE_JOIN_RESEARCH_ONLY_20261107.csv"
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



class SundayMatchupEnrichmentSafety(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.explosives = load(EXPLOSIVES)
        cls.te = load(TE_AUDIT)
        cls.context = load(MATCHUP)
        cls.offense = load(OFFENSE)

    def test_team_explosive_and_sack_flags_are_raw_not_coverage(self):
        self.assertEqual(len(self.explosives), 26)
        self.assertEqual({r["defense_team"] for r in self.explosives}, TEAMS)
        for r in self.explosives:
            self.assertIn(r["week9_opponent"], TEAMS)
            self.assertGreaterEqual(int(r["games"]), 7)
            pass_attempts = int(r["passes_faced"])
            sacks = int(r["sacks_recorded"])
            exp_passes = int(r["explosive_pass_20_allowed"])
            rush_attempts = int(r["rushes_faced"])
            exp_rushes = int(r["explosive_rush_10_allowed"])
            self.assertGreater(pass_attempts, 0)
            self.assertGreater(rush_attempts, 0)
            self.assertAlmostEqual(float(r["exp_pass_per_pass_attempt"]),
                                   exp_passes / pass_attempts,delta=0.000011)
            self.assertAlmostEqual(float(r["exp_rush_per_rush_attempt"]),
                                   exp_rushes / rush_attempts,delta=0.000011)
            self.assertAlmostEqual(float(r["sack_per_pass_or_sack_proxy"]),
                                   sacks / (pass_attempts+sacks),delta=0.000011)
            self.assertLessEqual(float(r["exp_pass_wilson95_lo"]),
                                 float(r["exp_pass_per_pass_attempt"]))
            self.assertGreaterEqual(float(r["exp_pass_wilson95_hi"]),
                                    float(r["exp_pass_per_pass_attempt"]))
            for inaccessible in (
                "coverage_man_zone", "safety_shell", "blitz_rate",
                "pressure_rate", "individual_cb_or_s_responsibility"
            ):
                self.assertEqual(r[inaccessible], "")
            self.assertEqual(r["projection_status"],
                             "DESCRIPTIVE_ONLY_NOT_PRESSURE_OR_CB_CHARTING")

    def test_grok_te_targets_are_crosschecked_before_any_role_adjustment(self):
        self.assertEqual(len(self.te), 10)
        self.assertEqual(sum(x["source_target_status"]=="MATCH" for x in self.te),8)
        barner = next(x for x in self.te if x["player"]=="AJ Barner")
        self.assertEqual(barner["source_target_status"], "CONFLICT")
        self.assertEqual(barner["render_targets"], "34")
        self.assertEqual(barner["grok_targets"], "51")
        warren = next(x for x in self.te if x["player"]=="Tyler Warren")
        self.assertEqual(warren["source_target_status"],"GROK_NOT_SUPPLIED")
        self.assertEqual(warren["render_targets"],"46")
        for r in self.te:
            self.assertRegex(r["gsis_id"],r"^00-\d{7}$")
            self.assertEqual(r["calibrated_in_model"],"false")
            self.assertEqual(r["source_url_status"],"NO_EXACT_PER_ROW_PROVIDER_URL")

    def test_matchup_board_contains_no_fabricated_conditional_forecasts(self):
        self.assertEqual(len(self.context),len(self.offense))
        hist = {(r["team"],r["player_id"],r["market_key"]):r for r in self.offense}
        covered = set()
        for r in self.context:
            key = (r["offense"],r["player_id"],r["market"])
            self.assertIn(key,hist)
            self.assertNotIn(key,covered)
            covered.add(key)
            self.assertEqual(r["historical_mean"],hist[key]["mean_opportunity_games"])
            self.assertIn(r["opponent_defense"],TEAMS)
            self.assertEqual(r["calibrated_probability"],"")
            self.assertEqual(r["matchup_adjusted_prediction"],"")
            self.assertEqual(r["estimated_conditional_opportunity"],"")
            self.assertEqual(r["bet_eligible"],"false")
            self.assertEqual(r["source_status"],"PUBLIC_SOURCE_TEAM_LEVEL_ONLY_NO_PERSONNEL_OR_COVERAGE")

if __name__ == "__main__":
    unittest.main()
