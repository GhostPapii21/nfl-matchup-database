import json
import unittest
from research.third_down.mnf_20261109_joint_monte_carlo import run,quarter_shares,SCENARIOS,METHODS
class MNFResearch100kTests(unittest.TestCase):
 def test_quarters_and_quote_coverage_with_seed(self):
  x=run(70,100)
  self.assertEqual(x["total_trials"],len(SCENARIOS)*len(METHODS)*100)
  self.assertEqual(len(x["runs"]),9)
  for r in x["runs"]:
   self.assertEqual(len(r["player_props"]),28)
   self.assertEqual(set(r["quarters"]),{"Q1","Q2","Q3","Q4"})
   for q in r["quarters"].values():
    self.assertAlmostEqual(q["BUF_win_pct"]+q["MIN_win_pct"]+q["tie_pct"],100,delta=.03)
   for p in r["player_props"]:
    self.assertTrue(p["outcome"]["p10"]<=p["outcome"]["median"]<=p["outcome"]["p90"])
    for book in ("DK","FD"):
     if p[book]:
      self.assertAlmostEqual(p[book]["sim_over_pct"]+p[book]["sim_under_pct"]+p[book]["sim_push_pct"],100,delta=.03)
 def test_probabilities_not_misrepresented_as_main_or_lightning(self):
  self.assertTrue(run(1,10)["not_run_actual_main_or_lightning"])
 def test_quarter_priors_sum_to_one(self):
  for s in SCENARIOS:
   for m in METHODS:
    for team in ["MIN","BUF"]:
     self.assertAlmostEqual(quarter_shares(team,m,s).sum(),1.,places=8)
