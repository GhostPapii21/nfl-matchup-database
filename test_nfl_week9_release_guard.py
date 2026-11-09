import unittest
from research.week9_20261108_release_guard import scan

class PropReleaseQuarantine(unittest.TestCase):
    def test_known_low_sample_w9_qb_remains_blocked(self):
        x=scan()
        self.assertEqual(x["status"],"RELEASE_BLOCKED_RESEARCH_ONLY")
        self.assertEqual(x["known_issue"]["player"],"Shedeur Sanders")
        self.assertEqual(x["known_issue"]["prior_games"],2)
        self.assertGreater(x["fatal_model_calibration"]["raw_not_bet_gradeable"],1000)
    def test_2026_w9_1pm_all_raw_model_rows_not_prob_calibrated(self):
        x=scan()
        self.assertEqual(x["fatal_model_calibration"]["raw_not_bet_gradeable"],1299)
        self.assertEqual(x["history_quality"]["below_three_prior_games"],48)
