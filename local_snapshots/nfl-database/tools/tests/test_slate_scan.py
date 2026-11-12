import os, sys, unittest
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import slate_scan as ss

def mk(rows):
    base = dict(car=0, ryds=0, tgt=0, rec=0, recyds=0, att=0, pyds=0, wx=False, team_spread=0.0, total=44.0, opp="OPP")
    return pd.DataFrame([{**base, **r} for r in rows])
def team(week_max, extra=()):
    r = []
    for w in range(1, week_max + 1):
        g = f"g{w}"
        r += [dict(game_id=g, week=w, team="T", pid="rb1", name="RB One", pos="RB", car=18, ryds=80, tgt=3, rec=2, recyds=15),
              dict(game_id=g, week=w, team="T", pid="rb2", name="RB Two", pos="RB", car=4, ryds=25, tgt=2, rec=2, recyds=12),
              dict(game_id=g, week=w, team="T", pid="wr1", name="WR One", pos="WR", tgt=9, rec=6, recyds=80),
              dict(game_id=g, week=w, team="T", pid="wr2", name="WR Two", pos="WR", tgt=7, rec=5, recyds=60),
              dict(game_id=g, week=w, team="T", pid="wr3", name="WR Three", pos="WR", tgt=3, rec=2, recyds=25),
              dict(game_id=g, week=w, team="T", pid="te1", name="TE One", pos="TE", tgt=5, rec=4, recyds=40)]
    return r + list(extra)

class Roles(unittest.TestCase):
    def test_roles_use_only_prior_weeks(self):
        pg = mk(team(5)); r = ss.roles(pg, "T", 5)
        self.assertEqual((r["RB1"], r["RB2"], r["WR1"], r["WR2"], r["TE1"]), ("rb1", "rb2", "wr1", "wr2", "te1"))
    def test_wr3_banned(self):
        pg = mk(team(5)); c = ss.candidates(pg, "T", 5, ctx=dict(wx=False, team_spread=0, total=44, opp="OPP"))
        self.assertNotIn("wr3", set(c.pid))
    def test_rb2_only_on_trigger_and_rule5_flag(self):
        pg = mk(team(5))
        c = ss.candidates(pg, "T", 5, ctx=dict(wx=False, team_spread=1.0, total=44, opp="OPP"))
        self.assertFalse(((c.pid == "rb2") & (c.market == "ryds")).any())
        c = ss.candidates(pg, "T", 5, ctx=dict(wx=True, team_spread=1.0, total=44, opp="OPP"))
        r = c[(c.pid == "rb2") & (c.market == "ryds")]
        self.assertEqual(len(r), 1); self.assertTrue(r.rule5_conflict.iat[0]); self.assertIn("weather", r.trigger.iat[0])
    def test_starter_out_promotes_rb2(self):
        pg = mk(team(5)); c = ss.candidates(pg, "T", 5, ctx=dict(wx=False, team_spread=1.0, total=44, opp="OPP"), out={"rb1"})
        self.assertIn("starter_out", c[(c.pid == "rb2") & (c.market == "ryds")].trigger.iat[0])
        self.assertNotIn("rb1", set(c.pid))
    def test_no_leakage(self):
        pg = mk(team(6)); ctx = dict(wx=True, team_spread=-3, total=44, opp="OPP")
        a = ss.candidates(pg, "T", 5, ctx=ctx); b = ss.candidates(pg[pg.week < 5], "T", 5, ctx=ctx)
        pd.testing.assert_frame_equal(a.reset_index(drop=True), b.reset_index(drop=True))
    def test_standin_line(self):
        self.assertEqual(ss.standin_line([10, 30, 20]), 20.5); self.assertIsNone(ss.standin_line([10]))

class Week8Acceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.c = ss.scan_week(8)
    def has(self, name, mk):
        r = self.c[(self.c.name == name) & (self.c.market == mk)]
        self.assertFalse(r.empty, f"{name} {mk} not surfaced"); return r.iloc[0]
    def test_gainwell(self): self.has("Kenny Gainwell", "ryds")
    def test_braelon_allen(self): self.has("Braelon Allen", "ryds")
    def test_adonai_mitchell(self): self.assertIn(self.has("Adonai Mitchell", "recyds").role, ("WR1", "WR2"))
    def test_chase_brown_receptions(self): self.has("Chase Brown", "rec")
    def test_emmett_johnson_receiving(self): self.has("Emmett Johnson", "recyds")
    def test_ranked_csv_columns(self):
        for k in ("rank", "score", "line", "line_src", "rule5_conflict", "trigger"): self.assertIn(k, self.c.columns)
if __name__ == "__main__": unittest.main()

class ScoreRegression(unittest.TestCase):
    def test_allowed_component_not_all_zero(self):  # bug 2026-11-01: DataFrame.div missing axis=0 -> all-NaN -> 0
        c = ss.scan_week(8); self.assertGreater((c.s_allow.abs() > 0).mean(), 0.5)

class FittedWeights(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.c = ss.scan_week(8)
    def r(self, n, m): return int(self.c[(self.c.name == n) & (self.c.market == m)]["rank"].iat[0])
    def test_wk8_misses_rank_higher(self):  # old equal-sum ranks: Gainwell 60, Mitchell 86, E.Johnson 128
        self.assertLess(self.r("Kenny Gainwell", "ryds"), 60); self.assertLess(self.r("Adonai Mitchell", "recyds"), 86)
        self.assertLess(self.r("Emmett Johnson", "recyds"), 128)
    def test_no_leak_before_valid_week(self):  # weights fit on wk3-7 must not score wk<=7
        c = ss.scan_week(7); s = ["s_allow","s_explosive","s_qb","s_script","s_weather","s_promo","s_rb2","s_deep","s_repeat"]
        self.assertTrue(((c[s].sum(axis=1).round(4) - c.score).abs() < 1e-6).all())


class RbRushCoverage(unittest.TestCase):
    """Regression: Mike Washington Jr. (LV, labelled RB2) got only rec/recyds in Week 8, never ryds."""
    CTX = dict(wx=False, team_spread=3.0, total=44, opp="NYJ")
    def lv(self, flip=False):
        car = {1: (23, 7), 2: (21, 3), 3: (19, 5), 4: (15, 9), 5: (10, 1), 6: (10, 9), 7: (8, 6)}
        if flip: car[7] = (5, 12)
        r = []
        for w, (j, m) in car.items():
            r += [dict(game_id=f"g{w}", week=w, team="LV", pid="jeanty", name="Ashton Jeanty", pos="RB", car=j, ryds=4 * j, tgt=6, rec=4, recyds=30),
                  dict(game_id=f"g{w}", week=w, team="LV", pid="mw", name="Mike Washington Jr.", pos="RB", car=m, ryds=5 * m, tgt=1, rec=1, recyds=5),
                  dict(game_id=f"g{w}", week=w, team="LV", pid="wr1", name="WR One", pos="WR", tgt=8, rec=5, recyds=60)]
        return mk(r)
    def test_washington_wk8_gets_rush_candidate(self):
        c = ss.candidates(self.lv(), "LV", 8, self.CTX)
        r = c[(c.pid == "mw") & (c.market == "ryds")]
        self.assertEqual(len(r), 1); self.assertIn("carry_share", r.trigger.iat[0])
    def test_low_share_rb_still_no_rush(self):
        pg = mk(team(5)); c = ss.candidates(pg, "T", 5, ctx=dict(wx=False, team_spread=1.0, total=44, opp="OPP"))
        self.assertFalse(((c.pid == "rb2") & (c.market == "ryds")).any())
    def test_role_flip_promotes_and_flags(self):
        c = ss.candidates(self.lv(flip=True), "LV", 8, self.CTX)
        r = c[(c.pid == "mw") & (c.market == "ryds")]
        self.assertEqual(r.role.iat[0], "RB1"); self.assertIn("role_flip", r.trigger.iat[0])
        self.assertEqual(c[(c.pid == "jeanty")].role.iat[0], "RB2")
    def test_depth_chart_rb1_gets_rush(self):
        pg = mk(team(5)); c = ss.candidates(pg, "T", 5, ctx=dict(wx=False, team_spread=1.0, total=44, opp="OPP"), depth_rb1="rb2")
        r = c[(c.pid == "rb2") & (c.market == "ryds")]
        self.assertEqual(len(r), 1); self.assertIn("depth_rb1", r.trigger.iat[0])
    def test_rb_rush_candidate_unique(self):
        c = ss.candidates(self.lv(), "LV", 8, dict(self.CTX, wx=True))
        self.assertEqual(len(c[(c.pid == "mw") & (c.market == "ryds")]), 1)
    def test_wr_te_candidates_still_generated(self):
        c = ss.candidates(self.lv(), "LV", 8, self.CTX)
        self.assertEqual(set(c[c.pos == "WR"].market), {"recyds", "rec"})
        pg = mk(team(5)); c = ss.candidates(pg, "T", 5, ctx=dict(wx=False, team_spread=1.0, total=44, opp="OPP"))
        self.assertTrue({"wr1", "wr2", "te1"} <= set(c.pid))
