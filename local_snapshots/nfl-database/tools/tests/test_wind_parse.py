import sys, unittest
import pandas as pd
sys.path.insert(0, '/workspace/nfl-database/tools')
import scan_data as S
class T(unittest.TestCase):
    def test_nan_wind_parsed_from_weather_string(self):
        w = S._wind_mph(pd.Series([float('nan'), float('nan'), 7.0, float('nan')]),
                        pd.Series(['Sunny Temp: 66° F, Wind: NE 18 mph', 'Wind: Calm', 'x', None]))
        self.assertEqual(w.iloc[0], 18.0); self.assertEqual(w.iloc[1], 0.0); self.assertEqual(w.iloc[2], 7.0)
        self.assertTrue(pd.isna(w.iloc[3]))  # unknown stays unknown, never silently 0
    def test_wk8_pregame_weather_flags_match_phase15(self):
        # phase15_4pm_2026-11-01.md flagged NE@MIA (NWS PoP 53-69%, open air); 1pm flagged ATL@TB rain
        self.assertTrue(S.WX8.get(("ATL", "TB")))
        self.assertTrue(S.WX8.get(("NE", "MIA")))
if __name__ == '__main__': unittest.main()
