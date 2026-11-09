"""Regression tests for Sunday matchup audit, fully offline."""
import unittest
from research.week9_20261108_integrity_audit import audit,check_live,EXPECTED
class SourceIntegrity(unittest.TestCase):
    def test_archived_complete_without_postgame_feature_reuse(self):
        v=audit()
        self.assertEqual(len(v["games"]),13)
        self.assertEqual(v["archived_forecast_rows"],1599)
    def test_live_scoreboard_missing_fails(self):
        with self.assertRaisesRegex(ValueError,"incomplete"):
            check_live(fetch=lambda:{"events":[]})
    def test_live_scoreboard_mock_matches(self):
        games=[]
        for game,(away,home) in EXPECTED.items():
            a,h=game.split("@")
            games.append({"id":game,"status":{"type":{"completed":True}},
                "competitions":[{"competitors":[
                    {"homeAway":"away","team":{"abbreviation":a},"score":str(away)},
                    {"homeAway":"home","team":{"abbreviation":h},"score":str(home)}
                ]}]})
        self.assertEqual(len(check_live(fetch=lambda:{"events":games})),13)
