import unittest
from datetime import datetime, timezone
from research.nfl_odds_api_verify import validate

NOW = datetime(2026, 11, 11, 18, 0, tzinfo=timezone.utc)

def event(stamp="2026-11-11T17:50:00Z", price=1.91, point=-2.5):
    return [{"id": "fixture", "home_team": "Home", "away_team": "Away",
        "commence_time": "2026-11-12T01:00:00Z",
        "bookmakers": [{"key": "draftkings", "markets": [
            {"key": "spreads", "last_update": stamp,
             "outcomes": [{"name": "Home", "price": price, "point": point}]}]}]}]

class VerifyOdds(unittest.TestCase):
    def test_fresh_exact_line(self):
        self.assertTrue(validate(event(), NOW)["ok"])
    def test_stale_quote_fails(self):
        self.assertFalse(validate(event(stamp="2026-11-10T17:00:00Z"), NOW)["ok"])
    def test_missing_exact_line_fails(self):
        self.assertFalse(validate(event(point=None), NOW)["ok"])
    def test_invalid_price_fails(self):
        self.assertFalse(validate(event(price=1), NOW)["ok"])
    def test_empty_nfl_fails(self):
        self.assertFalse(validate([], NOW)["ok"])

if __name__ == "__main__":
    unittest.main()
