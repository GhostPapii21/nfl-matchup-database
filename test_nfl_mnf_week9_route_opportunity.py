import unittest
from research.third_down.mnf_week9_route_opportunity_scenarios import derive,ROUTES,SCENARIOS
class OpportunityRoutes(unittest.TestCase):
 def test_source_route_denominators(self):
  out=derive()
  r=out["observed_route_evidence"]
  self.assertEqual((r["routes"],r["team_dropbacks"],r["hockenson_targets"]),(102,151,23))
  self.assertAlmostEqual(r["targets_per_route"],23/102,places=4)
 def test_hockenson_protection_reduces_catches(self):
  o=derive()["scenarios"]
  self.assertLess(o["hockenson_protection_increase"]["hockenson_expected_receptions"],
                  o["competitive_base"]["hockenson_expected_receptions"])
 def test_high_volume_increases_catches_not_certified_over(self):
  o=derive()["scenarios"]
  self.assertLess(o["competitive_base"]["hockenson_expected_receptions"],4.5)
  self.assertGreater(o["vikings_trailing_pass_heavy"]["hockenson_expected_receptions"],4.5)
  self.assertLess(o["competitive_base"]["jefferson_expected_receptions"],6.5)
 def test_excludes_abnormal_jefferson_inactive_game(self):
  with self.assertRaises(ValueError):
   derive(route_rows=ROUTES+[dict(week=4,routes=31,dropbacks=43,targets=13)])
 def test_prevents_overallocation(self):
  sc={key:dict(value) for key,value in SCENARIOS.items()}
  sc["competitive_base"]["jefferson_share"]=.99
  with self.assertRaisesRegex(ValueError,"exceed"):
   derive(scenarios=sc)
 def test_no_false_probability(self):
  result=derive()
  self.assertIn("NOT_CALIBRATED",result["status"])
  self.assertFalse(any("probability" in k or "win_rate" in k for k in result["scenarios"]["competitive_base"]))
if __name__=="__main__":unittest.main()
