"""Lessons audit 2026-11-01 (BUG-2026-11-01-PFFX, -SIMV6, -WXSLIPS, -ASM9). Test-first."""
import json, os, subprocess, sys, unittest
from test_run_gate import Base, H, NOW, GATE
DB = "/workspace/nfl-database/"
PFF = dict(leg=H, metric="CB coverage grade", value=72.0, scope="matchup", source="Rico PFF screenshot 2026-11-01", pulled_et="2026-11-01T10:00")
SEC = dict(name="ESPN pass block win rate", value=70.0, source="https://www.espn.com/nfl/story/_/id/x", pulled_et="2026-11-01T10:00")

class PFFCrossCheckTest(Base):
    def test_pff_with_agreeing_second_source_no_caution(self):
        self.m["pff_inputs"] = [dict(PFF, second_source=dict(SEC), tolerance=5)]; self.save()
        c, o = self.run_gate(); self.assertEqual(c, 0, o); self.assertNotIn("PFF CAUTION", o); self.assertIn("PFF CROSS-CHECK", o)
    def test_pff_missing_second_source_is_caution_not_block(self):
        self.m["pff_inputs"] = [dict(PFF)]; self.save()
        c, o = self.run_gate(); self.assertEqual(c, 0, o); self.assertIn("PFF CAUTION", o); self.assertIn("no second source", o)
    def test_pff_disagreement_is_caution_not_block(self):
        self.m["pff_inputs"] = [dict(PFF, second_source=dict(SEC, value=40.0), tolerance=5)]; self.save()
        c, o = self.run_gate(); self.assertEqual(c, 0, o); self.assertIn("PFF CAUTION", o); self.assertIn("disagree", o)
    def test_pff_second_source_without_source_or_time_is_caution(self):
        self.m["pff_inputs"] = [dict(PFF, second_source=dict(SEC, source="", pulled_et=None), tolerance=5)]; self.save()
        c, o = self.run_gate(); self.assertEqual(c, 0, o); self.assertIn("PFF CAUTION", o)
    def test_pff_second_source_cannot_be_pff(self):
        self.m["pff_inputs"] = [dict(PFF, second_source=dict(SEC, name="PFF premium", source="https://www.pff.com/x"), tolerance=5)]; self.save()
        c, o = self.run_gate(); self.assertEqual(c, 0, o); self.assertIn("PFF CAUTION", o)
    def test_pff_weather_scope_fails(self):
        self.m["pff_inputs"] = [dict(PFF, scope="weather", second_source=dict(SEC), tolerance=5)]; self.save(); self.assertFail("PFF")
    def test_pff_game_script_scope_fails(self):
        self.m["pff_inputs"] = [dict(PFF, scope="game_script", second_source=dict(SEC), tolerance=5)]; self.save(); self.assertFail("PFF")
    def test_pff_under_vs_own_matchup_over_is_caution(self):
        self.m["pff_inputs"] = [dict(PFF, second_source=dict(SEC), tolerance=5, pff_projection_side="under", pff_matchup_side="over")]; self.save()
        c, o = self.run_gate(); self.assertEqual(c, 0, o); self.assertIn("PFF CAUTION", o)
    def test_no_pff_inputs_prints_nothing(self):
        c, o = self.run_gate(); self.assertEqual(c, 0, o); self.assertNotIn("PFF", o)

class SimV6Test(Base):
    def setUp(self):
        super().setUp(); self.m["game_date"] = "2026-11-05"
    def test_week9_sim_without_v6_script_fails(self):
        self.save(); self.assertFail("sim_v6")
    def test_week9_sim_v5_script_fails(self):
        for s in self.m["sims"]: s["script"] = "/x/sim_v5.py"
        self.save(); self.assertFail("sim_v6")
    def test_week9_sim_v6_passes(self):
        for s in self.m["sims"]: s["script"] = "/workspace/nfl-database/tools/sim_v6.py"
        for k in ("time_to_throw", "targets_under_pressure"): self.m["pressure_inputs"][k] = dict(value=1, source="ngs", pulled_et="2026-11-01T10:00")
        self.m["weather_forecast"] = dict(source="tools/weather_forecast.py",file="fx",pulled_et="2026-11-01T10:00",games={"TEN@CIN":dict(roof="open",status="OK",precip_pct=10,gust_mph=8,wind_mph=5)})  # Rico 2026-11-01 forecast gate
        self.save(); c, o = self.run_gate(); self.assertEqual(c, 0, o)
    def test_nov1_runs_not_required(self):
        self.m["game_date"] = "2026-11-01"; self.save(); c, o = self.run_gate(); self.assertEqual(c, 0, o)

class WeatherSlipsWeekTest(Base):
    def test_week9_weather_alert_does_not_list_week8_slips(self):
        self.m["game_date"] = "2026-11-08"
        for s in self.m["sims"]: s["script"] = "tools/sim_v6.py"
        l = self.leg(); l["status"] = "CUT"
        for k in ("time_to_throw", "targets_under_pressure"): self.m["pressure_inputs"][k] = dict(value=1, source="ngs", pulled_et="2026-11-01T10:00")
        self.m["weather"] = {"TEN@CIN": dict(roof="open", precip_pct=80, gust_mph=5, wind_mph=5, source="https://api.weather.gov/x", pulled_et="2026-11-01T10:00")}
        self.m["game_script_rb"] = {"TEN@CIN": dict(fav_team="CIN", fav_spread=-3.5, opp_ypc=4.1, wx_flag=True, triggered=True, lead_rb="Chase Brown", rb2="Samaje Perine",
            boost=dict(lead=1.07, rb2=1.11, source="tools/rb_script_boost.json"), rb2_projection=dict(market="rushyds", median=dict(mc=20, bias=20, gr=20)),
            model_order=["rushyds", "recyds"], source="pbp", pulled_et="2026-11-01T10:00")}
        self.save(); c, o = self.run_gate()
        self.assertIn("WEATHER ALERT", o); self.assertIn("placed legs unknown", o); self.assertNotIn("slips_2026-11-01", o)

class Assemble9Test(unittest.TestCase):
    A = DB + "runs/2026-11-05_shared_src/assemble.py"
    def src(self): return open(self.A).read()
    def test_no_hardcoded_week8_inputs(self):
        self.assertNotIn("week8/", self.src())
        self.assertNotIn("_wk8", self.src()); self.assertNotIn("wk8 TNF", self.src()); self.assertNotIn("(wk8)", self.src())
    def test_no_sim_v5_labels(self):
        self.assertNotIn("sim_v5.py seed", self.src()); self.assertNotIn("SH+'sim_v5.py'", self.src())
    def test_preflight_blocks_missing_inputs(self):
        r = subprocess.run([sys.executable, self.A, "zz_none", "--date", "2026-11-05"], capture_output=True, text=True, timeout=120)
        self.assertNotEqual(r.returncode, 0); o = r.stdout + r.stderr
        self.assertIn("PREFLIGHT", o); self.assertIn("inactives.json", o); self.assertIn("placed_slips.json", o)
        self.assertFalse(os.path.exists(DB + "runs/2026-11-05_zz"))

if __name__ == "__main__": unittest.main()

class PressureW9Test(Base):
    """Lesson 5: receiving legs factor time to throw and targets under pressure (runs dated >= 2026-11-05)."""
    def setUp(self):
        super().setUp(); self.m["game_date"] = "2026-11-05"
        for s in self.m["sims"]: s["script"] = "/workspace/nfl-database/tools/sim_v6.py"
    def test_missing_ttt_fails_w9(self):
        self.save(); self.assertFail("time_to_throw")
    def test_present_passes_w9(self):
        for k in ("time_to_throw", "targets_under_pressure"):
            self.m["pressure_inputs"][k] = dict(value=2.7, source="https://nextgenstats.nfl.com/stats/passing", pulled_et="2026-11-01T10:00")
        self.m["weather_forecast"] = dict(source="tools/weather_forecast.py",file="fx",pulled_et="2026-11-01T10:00",games={"TEN@CIN":dict(roof="open",status="OK",precip_pct=10,gust_mph=8,wind_mph=5)})  # Rico 2026-11-01 forecast gate
        self.save(); c, o = self.run_gate(); self.assertEqual(c, 0, o)
