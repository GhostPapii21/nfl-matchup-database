"""BUG-2026-11-01-RBMISS (A, E, F) — sim_v6 side. Pre-game data only (pbp thru 2026-10-29; 11:35-11:49 ET FanDuel lines)."""
import os, sys, json, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import sim_v6 as S
MODELS = ('mc','bias','gr'); N = int(os.environ.get('RBMISS_N', 20000))
class TestSoftRunD(unittest.TestCase):
    def test_43_does_not_boost(self): self.assertEqual(S.soft_run_d_boost(4.3)['applied'], 1.0)
    def test_44_uses_fit(self):
        b = S.soft_run_d_boost(4.45); self.assertTrue(b['soft']); self.assertEqual(b['fitted'], json.load(open(S.MISS_F))['soft_run_d']['boost'])
        self.assertGreaterEqual(b['applied'], 1.0)  # never a suppressor; fit below 1 => no boost
    def test_ypc_boost_key_all_models(self):
        E = S.Engine(cutoff='2026-11-01', n=4000); L = dict(player='Tony Pollard', team='TEN', opp='CIN', market='rushyds', spread=12.5, rungs=[65.5])
        a, _ = E.sim(L); b, _ = E.sim(dict(L, ypc_boost=1.10))
        for m in MODELS: self.assertGreater(b[m]['mean'], a[m]['mean'])
class TestPromotion(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.E = S.Engine(cutoff='2026-11-01', n=N)
    def _chk(self, r, rb2):
        self.assertEqual(r['rb2'], rb2); self.assertGreater(r['share_new'], r['share_own']); self.assertGreaterEqual(r['carry_boost'], 1.0); self.assertAlmostEqual(r['target_carries'], r['share_new']*r['team_rb_carries'], places=6)
        for m in MODELS: self.assertIn(m, r['p']); self.assertGreater(r['median'][m], 0)
        self.assertEqual(r['tau'], json.load(open(S.MISS_F))['promotion']['tau'])
    def test_allen_built_and_priced(self):
        r = S.promote_rb(self.E, dict(team='NYJ', opp='LV', spread=-1.5, injured='Breece Hall', rb2='Braelon Allen', market='rushyds', line=78.5, no_vig=0.5)); self._chk(r, 'Braelon Allen')
    def test_pollard_built_and_priced(self):
        r = S.promote_rb(self.E, dict(team='TEN', opp='CIN', spread=12.5, injured='Tyjae Spears', rb2='Tony Pollard', market='rushyds', line=65.5, no_vig=0.5)); self._chk(r, 'Tony Pollard')
class TestSplitReprice(unittest.TestCase):
    def test_warren_and_dowdle_priced(self):
        E = S.Engine(cutoff='2026-11-01', n=N)
        r = S.split_reprice(E, dict(team='PIT', opp='CLE', spread=-3.5, backs=[dict(player='Jaylen Warren', line=64.5, no_vig=0.5), dict(player='Rico Dowdle', line=31.5, no_vig=0.5)]))
        self.assertEqual([b['player'] for b in r['backs']], ['Jaylen Warren', 'Rico Dowdle'])
        for b in r['backs']:
            lo, hi = b['share_range']; self.assertLess(lo, hi)
            for k in ('lo','mid','hi'):
                for m in MODELS: self.assertIn(m, b['p'][k])
            self.assertLessEqual(b['p']['lo']['mc'], b['p']['hi']['mc'])
if __name__ == '__main__': unittest.main()
