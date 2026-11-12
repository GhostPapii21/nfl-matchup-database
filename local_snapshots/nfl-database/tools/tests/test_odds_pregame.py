import sys, unittest, datetime as dt
sys.path.insert(0, '/workspace/nfl-database/tools')
import odds_pregame as O
U = dt.timezone.utc
EV = [{"id": "a", "commence_time": "2026-11-01T21:05:00Z"}, {"id": "b", "commence_time": "2026-11-02T01:20:00Z"}]
class T(unittest.TestCase):
    def test_started_games_dropped(self):
        now = dt.datetime(2026, 11, 1, 23, 51, tzinfo=U)  # 18:51 ET
        self.assertEqual([e["id"] for e in O.pregame_events(EV, now)], ["b"])
    def test_rows_flagged_inplay_by_last_update(self):
        rows = [{"game": "g", "last_update_utc": "2026-11-01T23:38:36Z"}, {"game": "g", "last_update_utc": "2026-11-01T20:00:00Z"}]
        self.assertEqual(O.flag_inplay(rows, {"g": "2026-11-01T21:05:00Z"}), [True, False])
    def test_missing_commence_is_unknown_not_pregame(self):
        self.assertEqual(O.flag_inplay([{"game": "x", "last_update_utc": "2026-11-01T20:00:00Z"}], {}), [None])
if __name__ == '__main__': unittest.main()
