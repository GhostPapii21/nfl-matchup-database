"""BUG-2026-11-02-BIASDUP: 'bias' must be an independent third model, not a copy of MC.
Also BUG-2026-11-02-QBBLEND (receiving/passing legs blend other QBs' games).
Written BEFORE the fix (RED on tools/sim_v6.py as of 2026-11-02 05:15 ET).
SIMV6_DIR selects which sim_v6.py to test (default: tools/). Run: python3 -m unittest -v test_biasdup"""
import os, sys, json, importlib, unittest
import numpy as np, pandas as pd
D = os.environ.get('SIMV6_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, D)
S = importlib.import_module('sim_v6')
MARKETS = ('passyds', 'rec', 'recyds', 'rushyds', 'rushrec')
LEGS = [dict(player='Jaxon Smith-Njigba', team='SEA', opp='CHI', market='recyds', spread=-3.0),
        dict(player="D'Andre Swift", team='CHI', opp='SEA', market='rushyds', spread=3.0),
        dict(player='Sam Darnold', team='SEA', opp='CHI', market='passyds', spread=-3.0),
        dict(player='Puka Nacua', team='LAR', opp='LAC', market='rec', spread=-3.0)]

class TestBiasIndependent(unittest.TestCase):
    def test_calib_multipliers_differ_every_market(self):
        C = json.load(open(S.CALIB_F))['multipliers']
        same = [mk for mk in MARKETS if C['bias'][mk]['M'] == C['mc'][mk]['M'] or C['bias'][mk]['raw'] == C['mc'][mk]['raw']]
        self.assertEqual(same, [], f'bias multipliers identical to MC for {same}')
    def test_fit_uses_bias_own_predictions(self):
        rng = np.random.default_rng(1); n = 200; rows = []
        for mk in MARKETS:
            a = rng.uniform(20, 80, n)
            rows += [dict(week=4, market=mk, actual=x, pred_mc=x, pred_bias=x / 1.2, pred_gr=x) for x in a]
        f = S.fit(pd.DataFrame(rows))
        for mk in MARKETS:
            self.assertAlmostEqual(f['mc'][mk]['raw'], 1.0, places=3)
            self.assertAlmostEqual(f['bias'][mk]['raw'], 1.2, places=3, msg=f'bias fit ignored pred_bias for {mk}')
    def test_raw_structure_differs_from_mc(self):
        """Uncalibrated means: a real model differs from MC by more than seed noise (>2%) on most legs."""
        E = S.Engine(n=20000, calib=None); diff = []
        for L in LEGS:
            o, _ = E.sim(dict(L, rungs=[]), raw=True)
            diff.append(abs(o['bias']['mean'] / o['mc']['mean'] - 1))
        self.assertGreaterEqual(sum(d > 0.02 for d in diff), 3, f'bias ~= mc raw means: {diff}')
    def test_calibrated_medians_not_equal(self):
        E = S.Engine(n=20000); eq = []
        for L in LEGS:
            o, _ = E.sim(dict(L, rungs=[]))
            if abs(o['bias']['median'] - o['mc']['median']) < 1e-9: eq.append(L['player'])
        self.assertEqual(eq, [])

class TestBiasCalibrated(unittest.TestCase):
    def test_fit_weeks_median_ratio_within_3pct(self):
        C = json.load(open(S.CALIB_F)); df = pd.read_csv(os.path.join(D, 'sim_v6_backtest.csv')); bad = []
        self.assertIn('pred_bias', df)
        for mk, g in df.groupby('market'):
            g = g[g.pred_bias > 0.5]
            r = float(np.median(g.actual / (g.pred_bias * C['multipliers']['bias'][mk]['M'])))
            if abs(r - 1) > 0.03: bad.append((mk, round(r, 3), len(g)))
        self.assertEqual(bad, [])
    def test_calib_stamps_data_through(self):
        C = json.load(open(S.CALIB_F))
        self.assertIn('pbp_data_through', C); self.assertGreaterEqual(C['pbp_data_through'], '2026-11-01')
        self.assertIn('bias_design', C)

class TestFitDeterministic(unittest.TestCase):
    def test_refit_same_seed_identical(self):
        a = S.backtest_rows((6,), 600, seed=11); b = S.backtest_rows((6,), 600, seed=11)
        self.assertTrue(len(a) > 50); pd.testing.assert_frame_equal(a, b)
        self.assertEqual(json.dumps(S.fit(a), sort_keys=True), json.dumps(S.fit(b), sort_keys=True))

class TestCurrentQBOnly(unittest.TestCase):
    def test_qb_filter_drops_other_qb_games(self):
        E = S.Engine(n=1000, calib=None)
        g = E.pid('Jaxon Smith-Njigba', 'SEA'); qb = E.pid('Sam Darnold', 'SEA')
        d_all, a_all, *_ = E.player('Jaxon Smith-Njigba', 'SEA', gsis=g)
        d_qb, a_qb, *_ = E.player('Jaxon Smith-Njigba', 'SEA', gsis=g, current_qb=qb)
        p = E.p; main = (p[(p.posteam == 'SEA') & (p.pass_attempt == 1)].groupby('game_id').passer_player_id.agg(lambda s: s.value_counts().idxmax()))
        self.assertTrue(set(a_qb.game_id) <= set(main[main == qb].index))
        self.assertLessEqual(len(a_qb), len(a_all))
    def test_leg_current_qb_reaches_sim(self):
        E = S.Engine(n=1000, calib=None)
        o, info = E.sim(dict(player='Jaxon Smith-Njigba', team='SEA', opp='CHI', market='recyds', spread=-3.0, rungs=[], current_qb='Sam Darnold'))
        self.assertEqual(info.get('qb_filter'), 'Sam Darnold')

if __name__ == '__main__': unittest.main()
