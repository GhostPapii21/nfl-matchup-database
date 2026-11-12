"""Phase 6 regression tests from the real Nov 2-3 misses (Rico [pt785u]). Inputs are SHAPED like the real leg
(player, market, what the data said); numbers not in our files are illustrative and labelled so. Each test pins the RULE
the miss taught, so a future edit that re-opens the hole goes red."""
import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import depth_rule, rico_nov2_rules as n2, test_press_live as tpl
from test_rico_nov2 import run as n2run, SE
import door

def depth_leg(**kw):
    l = dict(type="WR", wr_rank=3, side="over", rung="low", price_fd=-110, no_vig=0.5, injury_status="Active",
             depth=dict(script_pass=dict(ok=True, source="Phase 13 spread/total"), target_share=dict(value=0.14, source="nflverse pbp"),
                        defender_giving=dict(ok=True, source="PFR per-defender")))
    l.update(kw); return l

class DepthReceiverMisses(unittest.TestCase):
    # Burden 7-56 TD, Odunze 4-87, Loveland 7-65: depth/secondary receivers the old #3/#4 ban cut blind.
    def test_burden_wr3_with_support_is_playable(self):
        self.assertEqual(depth_rule.evaluate(depth_leg(name="Rome Odunze-style WR3 over")), (True, []))
    def test_odunze_wr4_with_support_is_playable(self):
        self.assertTrue(depth_rule.evaluate(depth_leg(wr_rank=4))[0])
    def test_loveland_te2_with_support_is_playable(self):
        self.assertTrue(depth_rule.evaluate(depth_leg(type="TE", wr_rank=None, te_rank=2))[0])
    def test_raymond_not_cut_when_data_supports(self):
        # Raymond 3 rec: must NOT be cut if script/share/defender all support him
        ok, why = depth_rule.evaluate(depth_leg(name="Kalif Raymond rec o2.5", wr_rank=4))
        self.assertTrue(ok, why)
    def test_kupp_1_7_depth_over_without_support_blocked(self):
        # Kupp 1-7: depth over with no script/share/defender evidence must fail closed, in plain words
        ok, why = depth_rule.evaluate(dict(type="WR", wr_rank=3, side="over", rung="low", price_fd=-115, no_vig=.52, injury_status="Active"))
        self.assertFalse(ok); self.assertTrue(any("target share" in w for w in why))
    def test_depth_under_5pct_share_blocked(self):
        l = depth_leg(); l["depth"]["target_share"]["value"] = 0.04
        self.assertFalse(depth_rule.evaluate(l)[0])
    def test_depth_main_rung_blocked(self):
        self.assertFalse(depth_rule.evaluate(depth_leg(rung="main"))[0])

class WilsonZeroPlays(unittest.TestCase):
    # Wilson 0 plays: inactive / out players and missing injury status must block at the door.
    def _rules(self, inj):
        l = dict(name="Wilson rec yds o40.5", type="WR", side="over", price_fd=-110, no_vig=.5, recent_form=dict(values=[50,45,60], source="pbp"))
        if inj is not None: l["injury_status"] = inj
        return {f["rule"] for f in door.leg_rules(l["name"], l, {})}
    def test_out_blocks(self): self.assertIn("INJURY", self._rules("Out"))
    def test_inactive_blocks(self): self.assertIn("INJURY", self._rules("Inactive"))
    def test_missing_status_blocks(self): self.assertIn("INJURY", self._rules(None))
    def test_active_ok(self): self.assertNotIn("INJURY", self._rules("Active"))

class SeaSecondHalf(unittest.TestCase):
    # SEA 2H -1.5 vs script: period spread against the period script read is a cut (N3).
    def test_against_script_fails(self):
        g = n2run({"type": "SPREAD", "team": "SEA", "market": "2H spread -1.5", "script_read": {"expected_winner": "CHI", "source": "Phase 13"}})
        self.assertTrue(any("N3" in m for m in g.miss))
    def test_no_read_fails_closed(self):
        self.assertTrue(n2run({"type": "SPREAD", "team": "SEA", "market": "2H spread -1.5"}).miss)

class CharbonnetN1(unittest.TestCase):
    # Charbonnet: committee back under 60% of carries -> DO NOT PLAY; door RB_TRAIL also blocks.
    def test_n1_cut(self):
        g = n2run({"type": "RB", "carry_share": {"value": 0.48, "source": "nflverse pbp"}})
        self.assertTrue(any("DO NOT PLAY" in m for m in g.miss))
    def test_door_rb_trail(self):
        l = dict(name="Zach Charbonnet rush yds o45.5", type="RB", side="over", market="rushyds", price_fd=-110, no_vig=.5, injury_status="Active",
                 recent_form=dict(values=[40,50,30], source="pbp"), rb_role=dict(share60_3of4=False, shares=[.5,.45,.62,.4], tgt_pg=2, may_trail=True, source="pbp"))
        self.assertIn("RB_TRAIL", {f["rule"] for f in door.leg_rules(l["name"], l, {})})
    def test_door_rb_role_missing_fails_closed(self):
        l = dict(name="Zach Charbonnet rush yds o45.5", type="RB", side="over", market="rushyds", price_fd=-110, no_vig=.5, injury_status="Active", recent_form=dict(values=[40], source="pbp"))
        self.assertIn("RB_TRAIL", {f["rule"] for f in door.leg_rules(l["name"], l, {})})

class SlipBehavior(unittest.TestCase):
    def test_td_leg_blocked(self):
        l = dict(name="Harold Fannin anytime TD", type="TE", side="over", price_fd=150, no_vig=.4, injury_status="Active", recent_form=dict(values=[1], source="pbp"))
        self.assertIn("NO_TD", {f["rule"] for f in door.leg_rules(l["name"], l, {})})
    def test_minus_250_is_flag_not_block(self):
        l = dict(name="X rec o1.5", type="WR", side="over", price_fd=-260, no_vig=.7, injury_status="Active", recent_form=dict(values=[3,4,5], source="pbp"))
        f = [x for x in door.leg_rules(l["name"], l, {}) if x["rule"] == "SHORT_PRICE"]
        self.assertEqual(f[0]["sev"], "FLAG")
    def test_no_price_fails_closed(self):
        l = dict(name="X rec o1.5", type="WR", side="over", injury_status="Active", recent_form=dict(values=[3], source="pbp"))
        self.assertIn("FAIR_PRICE", {f["rule"] for f in door.leg_rules(l["name"], l, {})})

class SchemeEdgeBehavior(tpl.LiveRun):
    """last-2 is WARN only; explanation required to waive; under +3 alerts (alerts file covered in test_door)."""
    def _set(self, expl, form=None):
        m = json.load(open(self.mp)); l = m["legs"][0]; l["no_vig"] = 0.565
        l["scheme_edge"] = dict(SE, explanation=expl)
        if form: l["recent_form"]["values"] = form
        json.dump(m, open(self.mp, "w")); return l
    def test_explanation_required_to_waive(self):
        self._set(""); c, o = tpl.gate(self.d, "2026-11-08T12:00")
        self.assertEqual(c, 1); self.assertIn("plain-words edge explanation", o)
    def test_with_explanation_flags_not_cut(self):
        self._set("QB checks down to him vs middle zone"); c, o = tpl.gate(self.d, "2026-11-08T12:00")
        self.assertEqual(c, 0, o); self.assertIn("SCHEME_EDGE ALERT", o)
    def test_last2_is_warn_only(self):
        m = json.load(open(self.mp)); l = m["legs"][0]; ln = float(l["line"]); up = l["side"] == "over"
        hi, lo = (ln + 20, max(ln - 20, 0)) if up else (max(ln - 20, 0), ln + 20)
        l["scheme_edge"] = dict(SE, explanation="coverage fit"); rf = l["recent_form"]
        rf["values"] = [hi, hi, lo, lo][-len(rf["games"]):] if len(rf["games"]) <= 4 else rf["values"]
        json.dump(m, open(self.mp, "w")); c, o = tpl.gate(self.d, "2026-11-08T12:00")
        self.assertIn("WARN SCHEME_EDGE_LAST2", o); self.assertNotIn("§7 FAIL", o)
    test_tags_manifest_report_tracker = None

if __name__ == "__main__": unittest.main()
