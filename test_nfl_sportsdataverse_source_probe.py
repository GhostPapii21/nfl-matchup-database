import unittest
from research.nfl_sportsdataverse_source_probe import football_game_id,normalize_name,summarize
class SourceParity(unittest.TestCase):
 def test_football_week9_only(self):
  self.assertEqual(football_game_id("2026_09_LA_WAS"),"LAR@WAS")
  self.assertIsNone(football_game_id("2026_08_LA_WAS"))
  self.assertIsNone(football_game_id("2026_09_NBA_PHI"))
 def test_case_normalization(self):
  self.assertEqual(normalize_name("Ja'Marr Chase"),normalize_name("Ja’Marr Chase"))
 def test_missing_games_block_ingest(self):
  r=summarize([dict(game_id="2026_09_CIN_ATL",player_id="p",player_name="X",team="CIN",targets=3)],[])
  self.assertEqual(r["status"],"BLOCKED_SOURCE_FRESHNESS_OR_PARITY")
  self.assertFalse(r["result_eligible_for_automated_model_ingest"])
 def test_unmatched_stat_never_auto_verified(self):
  r=summarize([dict(game_id="2026_09_CIN_ATL",player_id="p",player_name="X",team="CIN",targets=3)],
              [dict(game="CIN@ATL",team="CIN",player="X",market="targets",final="5")])
  self.assertEqual(r["official_metric_mismatch_count"],1)
  self.assertFalse(r["source_verified_for_research"])
