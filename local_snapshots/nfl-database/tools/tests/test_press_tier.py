import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import press_tier as pt
from test_run_gate import Base
OK = dict(on_inactives=False, sec11_conflict=False, wr_rank=1, matchup=True, coverage=True, script=True, qb=True, form7=True, side="over", line=60.5,
          medians=[70, 68, 66], weather_stop=False, injury_status="Active")
class Press(unittest.TestCase):
    def test_all_clear_is_press(self):
        r = pt.evaluate(OK); self.assertEqual(r["tier"], "PRESS"); self.assertTrue(r["anchor_eligible"]); self.assertEqual(r["shrink"], "none")
    def test_default_is_two_of_three(self):
        self.assertEqual(pt.DEFAULT_MODELS_REQUIRED, 2)
        self.assertEqual(pt.evaluate({**OK, "medians": [70, 68, 55]})["tier"], "PRESS")
        self.assertEqual(pt.evaluate({**OK, "medians": [70, 68, 55]}, models_required=3)["tier"], "STANDARD")
    def test_one_model_never(self):
        self.assertEqual(pt.evaluate({**OK, "medians": [70, 50, 55]})["tier"], "STANDARD")
        with self.assertRaises(ValueError): pt.evaluate(OK, models_required=1)
    def test_two_requires_all_align(self):
        for k in ("matchup", "coverage", "script", "qb", "form7"):
            self.assertEqual(pt.evaluate({**OK, k: False, "medians": [70, 68, 55]})["tier"], "STANDARD", k)
            self.assertEqual(pt.evaluate({**OK, k: False})["tier"], "STANDARD", k)
    def test_weather_hard_stop_overrides(self):
        r = pt.evaluate({**OK, "weather_stop": True}); self.assertEqual(r["tier"], "BLOCKED"); self.assertIn("weather", r["reason"])
    def test_injury_overrides(self):
        for s in ("Out", "Doubtful", "Inactive", "Injured Reserve", "Suspension", "PUP"):
            r = pt.evaluate({**OK, "injury_status": s}); self.assertEqual(r["tier"], "BLOCKED"); self.assertIn("injury", r["reason"])
    def test_missing_input_is_not_press(self):
        r = pt.evaluate({k: v for k, v in OK.items() if k != "coverage"}); self.assertEqual(r["tier"], "STANDARD")
    def test_under_side(self):
        self.assertEqual(pt.evaluate({**OK, "side": "under", "medians": [50, 52, 55]})["tier"], "PRESS")

class GateFlag(Base):
    def test_flag_off_output_unchanged_and_on_is_advisory(self):
        c0, o0 = self.run_gate()
        self.assertNotIn("PRESS", o0)
        import subprocess
        from test_run_gate import GATE, NOW
        r = subprocess.run([sys.executable, GATE, self.d, "--now", NOW, "--press-tier"], capture_output=True, text=True)
        self.assertEqual(r.returncode, c0); self.assertIn("PRESS TIER (advisory", r.stdout)
        self.assertEqual(o0.splitlines()[0][:10], r.stdout.splitlines()[0][:10])
if __name__ == "__main__": unittest.main()
