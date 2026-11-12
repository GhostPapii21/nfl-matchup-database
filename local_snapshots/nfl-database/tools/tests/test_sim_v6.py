"""Tests for BUG-2026-11-01-BIAS fix (sim_v6). Written before sim_v6.py existed.
Run: cd tools/tests && python3 -m unittest -v test_sim_v6
Env SIMV6_TEST_N (default 4000) sets sims per model for speed; the calibration itself is fitted with
leave-one-week-out over weeks 4-7 (fit on the other weeks, score the held-out week)."""
import os, sys, json, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
N = int(os.environ.get('SIMV6_TEST_N', '4000'))
MODELS = ('mc', 'bias', 'gr')
MARKETS = ('passyds', 'rec', 'recyds', 'rushyds', 'rushrec')

class TestDeterminism(unittest.TestCase):
    def test_same_seed_same_output(self):
        import sim_v6 as S
        leg = dict(player='Puka Nacua', team='LAR', opp='LAC', market='rec', spread=-3.0, rungs=[7.5])
        a = S.Engine(n=2000, seed=7).sim(leg)[0]; b = S.Engine(n=2000, seed=7).sim(leg)[0]
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
    def test_different_seed_differs(self):
        import sim_v6 as S
        leg = dict(player='Puka Nacua', team='LAR', opp='LAC', market='recyds', spread=-3.0, rungs=[69.5])
        a = S.Engine(n=2000, seed=7).sim(leg)[0]; b = S.Engine(n=2000, seed=8).sim(leg)[0]
        self.assertNotEqual(a['mc']['mean'], b['mc']['mean'])

class TestNoFlatHaircut(unittest.TestCase):
    def test_bias_mode_has_no_hardcoded_092(self):
        src = open(os.path.join(os.path.dirname(__file__), '..', 'sim_v6.py')).read()
        self.assertNotIn('(0.92,0.97,0.95)', src.replace(' ', ''))

class TestHeldOutCalibration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import sim_v6 as S
        cls.res = S.cross_validate(weeks=(4, 5, 6, 7), n=N)
    def test_median_signed_error_within_3pct(self):
        bad = []
        for mk in MARKETS:
            for md in MODELS:
                r = self.res[mk][md]
                if r['n'] < 20: continue
                if abs(r['median_signed_err_pct']) > 3.0: bad.append((mk, md, round(r['median_signed_err_pct'], 2), r['n']))
        self.assertEqual(bad, [], f'held-out median signed error outside +/-3%: {bad}')

class TestTodayBelowLineShare(unittest.TestCase):
    def test_share_below_line_40_60(self):
        import sim_v6 as S
        sh = S.below_line_share(n=N)
        bad = {m: round(v, 3) for m, v in sh['share'].items() if not (0.40 <= v <= 0.60)}
        self.assertGreaterEqual(sh['n_legs'], 190)
        self.assertEqual(bad, {}, f'share of legs with model median below line outside 40-60%: {sh}')

# ---------- BUG-2026-11-01-RBSCRIPT: game-script RB rule ----------
FIXJ = os.path.join(os.path.dirname(__file__), 'fixtures', 'indjax_rbscript_input.json')
class TestGameScriptTrigger(unittest.TestCase):
    def test_minus_6_5_vs_4_5_no_weather_no_trigger(self):
        import sim_v6 as S
        self.assertFalse(S.rb_script_trigger(-6.5, 4.5, False))
    def test_minus_7_vs_4_3_no_trigger(self):
        import sim_v6 as S
        self.assertFalse(S.rb_script_trigger(-7.0, 4.3, False))
    def test_minus_7_vs_4_4_triggers_inclusive(self):
        import sim_v6 as S
        self.assertTrue(S.rb_script_trigger(-7.0, 4.4, False))
    def test_weather_alone_triggers(self):
        import sim_v6 as S
        self.assertTrue(S.rb_script_trigger(-1.0, 3.9, True))
    def test_boosts_come_from_fitted_file_not_hardcoded(self):
        import sim_v6 as S
        F = json.load(open(S.BOOST_F)); g = F['groups']
        self.assertIn('derivation', F); self.assertGreaterEqual(g['lead_fav']['n'], 20)
        b = S.rb_script_boosts(-10.5, 4.49, True)
        self.assertAlmostEqual(b['lead'], g['lead_fav']['boost'] * g['lead_wx']['boost'], places=6)
        self.assertAlmostEqual(b['rb2'], g['rb2_fav']['boost'] * g['rb2_wx']['boost'], places=6)
        self.assertEqual(S.rb_script_boosts(-6.5, 4.5, False)['lead'], 1.0)
    def test_weather_orders_rushing_overs_before_passing(self):
        import sim_v6 as S
        legs = [dict(player='a', market='recyds'), dict(player='b', market='passyds'), dict(player='c', market='rushyds'), dict(player='d', market='rec')]
        o = [l['market'] for l in S.model_order(legs, wx_flag=True)]
        self.assertEqual(o[0], 'rushyds'); self.assertEqual(S.model_order(legs, wx_flag=False), legs)

class TestCarryBoostAllModels(unittest.TestCase):
    def test_boost_raises_carries_in_all_three_models(self):
        import sim_v6 as S
        E = S.Engine(n=4000, seed=7); leg = dict(player='Bhayshul Tuten', team='JAX', opp='IND', market='rushyds', spread=-10.5, rungs=[59.5])
        a = E.sim(leg)[0]; b = E.sim(dict(leg, carry_boost=1.25))[0]
        for m in MODELS: self.assertGreater(b[m]['mean'], a[m]['mean'] * 1.12, m)
    def test_default_boost_is_identity(self):
        import sim_v6 as S
        E = S.Engine(n=2000, seed=7); leg = dict(player='Bhayshul Tuten', team='JAX', opp='IND', market='rushyds', spread=-10.5, rungs=[59.5])
        self.assertEqual(json.dumps(E.sim(leg)[0], sort_keys=True), json.dumps(E.sim(dict(leg, carry_boost=1.0))[0], sort_keys=True))

class TestIndJaxRegression(unittest.TestCase):
    """Replay 2026-11-01 IND@JAX with pre-game data only (pbp thru 2026-10-29, 07:09-07:30 ET odds)."""
    @classmethod
    def setUpClass(cls):
        import sim_v6 as S
        cls.fx = json.load(open(FIXJ)); cls.r = S.price_game_script(S.Engine(cutoff='2026-11-01', n=N), cls.fx)
    def test_triggers(self):
        self.assertTrue(self.r['triggered']); self.assertTrue(self.r['components']['fav']); self.assertTrue(self.r['components']['wx'])
    def test_tuten_repriced_in_all_three_models(self):
        L = self.r['lead']; self.assertEqual(L['player'], 'Bhayshul Tuten')
        for m in MODELS:
            self.assertIn(m, L['p']); self.assertNotEqual(round(L['p'][m], 4), round(self.fx['lead']['pregame_p'][m], 4))
        self.assertEqual(L['script'], 'boosted'); self.assertAlmostEqual(L['edge'], sum(L['p'].values()) / 3 - self.fx['lead']['no_vig'], places=6)
    def test_rodriguez_rb2_modeled(self):
        R = self.r['rb2']; self.assertEqual(R['player'], 'Chris Rodriguez Jr.')
        for m in MODELS: self.assertGreater(R['median'][m], 0)
        self.assertGreater(R['boost'], 1.0)
    def test_rushing_modeled_first(self):
        self.assertEqual(self.r['model_order'][0], 'rushyds')

if __name__ == '__main__':
    unittest.main()
