import unittest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from penparse import parse_penalties
class T(unittest.TestCase):
    def test_accepted_noplay(self):
        r = parse_penalties("PENALTY on SEA-E.Saubert, False Start, 5 yards, enforced at 50 - No Play.")
        self.assertEqual(len(r), 1); x = r[0]
        self.assertEqual((x["team"], x["player"], x["type"], x["yards"], x["status"], x["no_play"]), ("SEA","E.Saubert","False Start",5,"accepted",True))
    def test_declined(self):
        r = parse_penalties("J.Allen pass short left to K.Shakir for 8 yards. PENALTY on MIA-J.Smith, Defensive Holding, declined.")
        self.assertEqual(r[0]["status"], "declined"); self.assertEqual(r[0]["yards"], 0); self.assertFalse(r[0]["no_play"])
    def test_offsetting(self):
        r = parse_penalties("(Shotgun) PENALTY on KC-T.Smith, Offensive Holding, 10 yards, enforced at KC 30 - No Play. PENALTY on DEN-Z.Allen, Defensive Offside, 5 yards, enforced at KC 30 - No Play. Penalties offset.")
        self.assertEqual(len(r), 2); self.assertTrue(all(x["status"] == "offsetting" for x in r))
    def test_double_spaces_and_normalize(self):
        r = parse_penalties("Direct snap to A.Barner.  A.Barner up the middle.PENALTY on  SEA-A.Bradford,  Offensive Offside,  4 yards, enforced at NE 46 - No Play.")
        self.assertEqual(r[0]["player"], "A.Bradford"); self.assertEqual(r[0]["type_norm"], "False Start/Offside"); self.assertEqual(r[0]["yards"], 4)
    def test_team_no_player(self):
        r = parse_penalties("PENALTY on LAR, Delay of Game, 5 yards, enforced at LAR 20 - No Play.")
        self.assertEqual(r[0]["team"], "LAR"); self.assertEqual(r[0]["player"], "")
    def test_dpi_norm(self):
        r = parse_penalties("pass incomplete.PENALTY on SEA-J.Jobe, Defensive Pass Interference, 34 yards, enforced at SEA 36 - No Play.")
        self.assertEqual(r[0]["type_norm"], "DPI")
if __name__ == "__main__": unittest.main()
class T2(unittest.TestCase):
    def test_kickoff_placed(self):
        r = parse_penalties("W.Lutz kicks 62 yards, out of bounds.PENALTY on DEN-W.Lutz, Kickoff Out of Bounds, placed at SEA 40.")
        self.assertEqual(len(r), 1); self.assertEqual(r[0]["status"], "accepted"); self.assertEqual(r[0]["team"], "DEN")
