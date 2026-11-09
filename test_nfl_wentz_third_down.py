"""Fully offline NFL QB/3rd-down definitions and fail-closed tests."""
import unittest
from research.third_down.wentz_2025_third_down_audit import (
    WENTZ,ALLEN,flag,meaningful_third_down,is_wentz_dropback,is_allen_dropback,
    audit_team,audit_qb,bucket
)

def r(**kw):
    d=dict(game_id="2025_04_MIN_PIT",week="4",posteam="MIN",defteam="PIT",down="3",
      ydstogo="7",third_down_converted="1",third_down_failed="0",
      qb_dropback="1",pass_attempt="1",complete_pass="1",passer_player_id=WENTZ,
      rusher_player_id="",receiver_player_name="T.Hockenson",no_play="0",
      sack="0",qb_hit="0",qb_scramble="0",play_type="pass",desc="")
    d.update(kw)
    return d

class NFLDownTests(unittest.TestCase):
    def test_third_down_opportunity_team_vs_qb(self):
        sample=[r(),r(third_down_converted="0",third_down_failed="1",pass_attempt="0",
                      complete_pass="0",sack="1"),
                r(qb_dropback="0",pass_attempt="0",complete_pass="0",
                  play_type="run",rusher_player_id="running_back"),
                r(down="2",third_down_converted="0")]
        team=audit_team(sample,"MIN")
        qb=audit_qb(sample,"wentz","MIN")
        self.assertEqual((team["third_down_conversions"],team["third_down_attempts"]),(2,3))
        self.assertEqual((qb["third_down_eligible"],qb["third_down_dropback_conversions"]),(2,1))
        self.assertEqual(qb["third_down_sacks"],1)
    def test_no_play_is_not_allowed_to_be_qb_result(self):
        sample=[r(no_play="1"),r()]
        self.assertEqual(audit_qb(sample,"wentz","MIN")["third_down_dropbacks"],1)
    def test_scramble_and_sack_qb_identity(self):
        self.assertTrue(is_wentz_dropback(r(qb_scramble="1",rusher_player_id=WENTZ,
             passer_player_id="",pass_attempt="0")))
        self.assertTrue(is_wentz_dropback(r(pass_attempt="0",passer_player_id="",
             sack="1",desc="C.Wentz sacked for 5 yards")))
        self.assertTrue(is_allen_dropback(r(posteam="BUF",passer_player_id=ALLEN)))
        self.assertFalse(is_allen_dropback(r()))
    def test_distance_and_invalid_down(self):
        self.assertEqual(bucket("3"),"1-3")
        self.assertEqual(bucket("4"),"4-6")
        self.assertEqual(bucket("10"),"10+")
        self.assertFalse(meaningful_third_down(r(down="2")))
if __name__=="__main__":unittest.main()
