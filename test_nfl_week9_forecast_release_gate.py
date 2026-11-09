import csv,unittest
from research.nfl_week9_forecast_release_gate import evaluate,SOURCE
class PublicationGate(unittest.TestCase):
 def test_existing_board_denies_promotion(self):
  with SOURCE.open(newline="",encoding="utf-8") as f:r=evaluate(list(csv.DictReader(f)))
  self.assertFalse(r["publish_to_production"])
  self.assertEqual(r["source_rows"],1299)
  self.assertTrue(r["counts"]["shedeur_unrealistic_mean"]>0)
 def test_unknown_model_fails_closed(self):
  with SOURCE.open(newline="",encoding="utf-8") as f:
   rows=list(csv.DictReader(f))
  rows[0]["model"]="postgame_fake"
  with self.assertRaisesRegex(ValueError,"unknown model"):
   evaluate(rows)
