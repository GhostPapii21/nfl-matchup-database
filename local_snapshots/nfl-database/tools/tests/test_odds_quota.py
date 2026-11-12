import csv, os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import odds_quota as Q

class Plan(unittest.TestCase):
    def test_cost_is_events_x_markets_x_region_units(self):
        p = Q.plan_cost(events=3, markets=["a", "b"], regions="us,eu")
        self.assertEqual(p["estimate"], 12); self.assertEqual(p["region_units"], 2)
    def test_bookmakers_count_per_10(self):
        self.assertEqual(Q.plan_cost(1, ["a"], bookmakers="fanduel,draftkings,pinnacle")["region_units"], 1)
        self.assertEqual(Q.plan_cost(1, ["a"], bookmakers=",".join(f"b{i}" for i in range(11)))["region_units"], 2)
    def test_zero_events_costs_zero(self):
        self.assertEqual(Q.plan_cost(0, ["a", "b"], regions="us")["estimate"], 0)

class Floor(unittest.TestCase):
    def test_floor_is_10pct_of_plan(self):
        self.assertEqual(Q.floor(used=400, remaining=600), 100)
    def test_allows_when_above_floor(self):
        ok, why = Q.check(estimate=50, used=400, remaining=600); self.assertTrue(ok)
    def test_stops_when_would_cross_floor(self):
        ok, why = Q.check(estimate=550, used=400, remaining=600)
        self.assertFalse(ok); self.assertIn("floor", why)
    def test_unknown_quota_is_allowed_but_says_so(self):
        ok, why = Q.check(estimate=5, used=None, remaining=None); self.assertTrue(ok); self.assertIn("unknown", why)

class Log(unittest.TestCase):
    def test_reads_headers_and_appends_csv(self):
        d = tempfile.mkdtemp(); p = os.path.join(d, "quota_log.csv")
        h = {"x-requests-remaining": "590", "x-requests-used": "410", "x-requests-last": "10"}
        Q.log_headers(p, "nfl_pull", "/events/x/odds", h, label="open", estimate=10)
        Q.log_headers(p, "nfl_pull", "/events/y/odds", h, label="open", estimate=10)
        rows = list(csv.DictReader(open(p)))
        self.assertEqual(len(rows), 2); self.assertEqual(rows[0]["remaining"], "590"); self.assertEqual(rows[0]["used"], "410")
        self.assertEqual(rows[0]["cost"], "10")
        self.assertEqual(Q.quota_from_headers(h), (410, 590))

if __name__ == "__main__": unittest.main()
