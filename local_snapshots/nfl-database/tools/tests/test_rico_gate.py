"""Rico 2026-11-01: (A) forecast check at slip build (BUG-2026-11-01-WXDAYS); (C) coverage profile on every receiving AND passing leg."""
import json, unittest
from test_run_gate import Base, H
FC = lambda **k: dict(source="tools/weather_forecast.py (api.weather.gov + api.open-meteo.com)", file="/x/forecast_2026-11-01_1000.json", pulled_et="2026-11-01T10:00",
                      games={"TEN@CIN": dict(dict(roof="open", status="OK", precip_pct=10, gust_mph=8, wind_mph=5, flag=False, why=[]), **k)})
class W9(Base):
    def setUp(self):
        super().setUp(); self.m["game_date"] = "2026-11-08"
        for s in self.m["sims"]: s["script"] = "/workspace/nfl-database/tools/sim_v6.py"
        for k in ("time_to_throw", "targets_under_pressure"): self.m["pressure_inputs"][k] = dict(value=2.7, source="ngs", pulled_et="2026-11-01T10:00")
        self.m["weather_forecast"] = FC()
class ForecastGateTest(W9):
    def test_fresh_unflagged_forecast_passes(self):
        self.save(); c, o = self.run_gate(); self.assertEqual(c, 0, o)
    def test_missing_forecast_fails(self):
        del self.m["weather_forecast"]; self.save(); self.assertFail("forecast")
    def test_forecast_older_than_24h_fails(self):
        self.m["weather_forecast"]["pulled_et"] = "2026-10-31T11:00"; self.save(); self.assertFail("forecast")
    def test_forecast_23h_ok(self):
        self.m["weather_forecast"]["pulled_et"] = "2026-10-31T13:00"; self.save(); c, o = self.run_gate(); self.assertEqual(c, 0, o)
    def test_open_air_game_missing_from_forecast_fails(self):
        self.m["weather_forecast"]["games"] = {"JAX@BAL": FC()["games"]["TEN@CIN"]}; self.save(); self.assertFail("no forecast")
    def test_open_air_status_missing_fails(self):
        self.m["weather_forecast"] = FC(status="MISSING", precip_pct=None, flag=None); self.save(); self.assertFail("no forecast")
    def test_indoor_game_without_numbers_passes(self):
        self.m["weather_forecast"] = FC(roof="dome", status="INDOOR", precip_pct=None, gust_mph=None, wind_mph=None); self.save()
        c, o = self.run_gate(); self.assertEqual(c, 0, o)
    def test_flagged_forecast_cuts_receiving_over_and_alerts(self):
        self.m["weather_forecast"] = FC(precip_pct=70, flag=True, why=["precip 70%"]); self.save()
        o = self.assertFail("forecast"); self.assertIn("WEATHER FORECAST ALERT", o); self.assertIn(H, o)
    def test_flag_recomputed_not_trusted(self):
        self.m["weather_forecast"] = FC(gust_mph=25, flag=False); self.save(); self.assertFail("forecast")
    def test_nov1_runs_not_required(self):
        self.m["game_date"] = "2026-11-01"; del self.m["weather_forecast"]; self.save(); c, o = self.run_gate(); self.assertEqual(c, 0, o)
QB = dict(name="Joe Burrow pass yds o240.5 -110", type="QB", market="passyds", receiving=False, status="PASS", side="over", line=240.5, no_vig=0.5, gaps=[])
class CoverageProfileTest(W9):
    def add_qb(self, cov=True):
        l = dict(QB, recent_form=dict(self.leg()["recent_form"], values=[300, 280, 290, 310]), price_fd=-110)
        if cov: import copy; l["coverage"] = copy.deepcopy({k: self.leg()["coverage"][k] for k in ("man_zone", "mof")})
        self.m["legs"].append(l)
        for s in self.m["sims"]: s["legs"][QB["name"]] = dict(p=0.6, median=290)
        import os; p = os.path.join(self.d, "checklist.md"); t = open(p).read()
        rows = [r for r in t.splitlines() if r.startswith(f"| {H} |")]
        open(p, "a").write("\n".join(r.replace(H, QB["name"]) for r in rows) + "\n")
    def test_receiving_leg_stale_man_zone_fails(self):
        self.leg()["coverage"]["man_zone"]["pulled_et"] = "2026-10-30T10:00"; self.save(); self.assertFail("man/zone")
    def test_receiving_leg_missing_mof_fails(self):
        del self.leg()["coverage"]["mof"]; self.save(); self.assertFail("MOF")
    def test_passing_leg_with_profile_passes(self):
        self.add_qb(); self.save(); c, o = self.run_gate(); self.assertEqual(c, 0, o)
    def test_passing_leg_without_profile_fails(self):
        self.add_qb(cov=False); self.save(); self.assertFail("coverage profile")
    def test_passing_leg_stale_profile_fails(self):
        self.add_qb(); self.m["legs"][-1]["coverage"]["mof"]["pulled_et"] = "2026-10-30T10:00"; self.save(); self.assertFail("stale")
if __name__ == "__main__": unittest.main()
class AssembleForecastTest(unittest.TestCase):
    A = "/workspace/nfl-database/runs/2026-11-05_shared_src/assemble.py"
    def test_preflight_requires_forecast_and_manifest_carries_it(self):
        s = open(self.A).read()
        self.assertIn("weather_forecast/", s); self.assertIn("PREFLIGHT FAIL: no weather forecast", s); self.assertIn("weather_forecast=", s)
