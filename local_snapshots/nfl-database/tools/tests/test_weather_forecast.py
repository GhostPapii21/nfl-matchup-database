"""Rico 2026-11-01 (BUG-2026-11-01-WXDAYS): weather check days ahead at slip build. Test-first."""
import json, os, sys, tempfile, unittest
sys.path.insert(0, "/workspace/nfl-database/tools")
import weather_forecast as WF
KO = "2026-11-08T13:00"
def om(pop, wind, gust, start="2026-11-08T12:00", n=6):
    t = [f"2026-11-08T{12+i:02d}:00" for i in range(n)]
    return dict(time=t, precipitation_probability=[pop]*n, wind_speed_10m=[wind]*n, wind_gusts_10m=[gust]*n, precipitation=[0.0]*n, temperature_2m=[50]*n)
def nws(pop, wind):
    return [dict(startTime=f"2026-11-08T{12+i:02d}:00:00-05:00", windSpeed=wind, probabilityOfPrecipitation={"value": pop}, shortForecast="x", temperature=50) for i in range(6)]
class Window(unittest.TestCase):
    def test_open_meteo_window_is_kick_to_kick_plus_3_5h(self):
        h = om(10, 5, 8); h["precipitation_probability"][1] = 80; h["precipitation_probability"][0] = 99   # 12:00 is before kick
        s = WF.summarize_om(h, KO); self.assertEqual(s["precip_pct"], 80); self.assertEqual(s["hours"], 4)
    def test_nws_wind_range_takes_upper(self):
        s = WF.summarize_nws(nws(20, "10 to 16 mph"), KO); self.assertEqual(s["wind_mph"], 16); self.assertEqual(s["precip_pct"], 20)
    def test_nws_blank_wind_is_unknown_not_zero(self):
        s = WF.summarize_nws(nws(20, ""), KO); self.assertIsNone(s["wind_mph"])
    def test_no_hours_in_window_is_none(self):
        self.assertIsNone(WF.summarize_om(om(10, 5, 8, n=1), KO))
class Flags(unittest.TestCase):
    def test_thresholds_inclusive(self):
        self.assertEqual(WF.flags(50, 0, 0), ["precip 50%"]); self.assertEqual(WF.flags(49, 19, 14), [])
        self.assertEqual(WF.flags(0, 20, 0), ["gusts 20 mph"]); self.assertEqual(WF.flags(0, 0, 15), ["sustained wind 15 mph"])
    def test_combine_takes_worse_source(self):
        e = WF.combine("open", dict(precip_pct=30, wind_mph=10, gust_mph=None), dict(precip_pct=60, wind_mph=8, gust_mph=22))
        self.assertEqual((e["precip_pct"], e["wind_mph"], e["gust_mph"]), (60, 10, 22)); self.assertTrue(e["flag"])
    def test_combine_one_source_missing_still_ok(self):
        e = WF.combine("open", None, dict(precip_pct=10, wind_mph=5, gust_mph=9)); self.assertEqual(e["status"], "OK"); self.assertFalse(e["flag"])
        self.assertIn("nws missing", e["notes"])
    def test_combine_both_missing_open_air_is_missing(self):
        e = WF.combine("open", None, None); self.assertEqual(e["status"], "MISSING"); self.assertIsNone(e["flag"])
    def test_indoor_not_flagged(self):
        e = WF.combine("dome", None, None); self.assertEqual(e["status"], "INDOOR"); self.assertFalse(e["flag"])
    def test_unknown_roof_treated_open_air(self):
        self.assertTrue(WF.is_open_air("retractable (status TBD)")); self.assertFalse(WF.is_open_air("retractable_closed"))
class Output(unittest.TestCase):
    def test_writes_dated_file(self):
        d = tempfile.mkdtemp(); games = [dict(game="X@Y", kickoff_et=KO, roof="dome", lat=0, lon=0)]
        p = WF.run(games, d, now="2026-11-01T22:50", fetch=False)
        self.assertTrue(os.path.basename(p).startswith("forecast_2026-11-01_2250")); j = json.load(open(p))
        self.assertEqual(j["pulled_et"], "2026-11-01T22:50"); self.assertIn("X@Y", j["games"])
    def test_week9_schedule_covers_thu_sun_mon(self):
        g = {x["game"] for x in WF.load_schedule(9)}
        for k in ("JAX@BAL", "TB@CHI", "BUF@MIN", "GB@NE"): self.assertIn(k, g)
if __name__ == "__main__": unittest.main()
