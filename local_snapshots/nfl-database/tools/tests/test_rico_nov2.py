import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import rico_nov2_rules as r

class G:
    def __init__(s, d="2026-11-05"): s.game_date=d; s.miss=[]
    def fail(s, m): s.miss.append(m)

def run(leg, d="2026-11-05"):
    g=G(d); r.check(g, {}, {"x":leg}, {"x"}); return g

DEF={"name":"A. CB","primary":True,"source":"pfr"}
def test_rb_under_60_is_do_not_play():
    g=run({"type":"RB","carry_share":{"value":0.55,"source":"pfr"}}); assert any("DO NOT PLAY" in m for m in g.miss)
def test_rb_60_passes():
    assert not run({"type":"RB","carry_share":{"value":0.6,"source":"pfr"}}).miss
def test_rb_share_missing_fails():
    assert run({"type":"RB"}).miss
def test_rb_receiving_needs_both():
    g=run({"type":"RB","receiving":True,"carry_share":{"value":0.7,"source":"x"},"coverage":{"defenders":[{"name":"LB","source":"pbp"}]}})
    assert any("N2" in m for m in g.miss)
def test_wr_primary_defender_passes():
    assert not run({"type":"WR","receiving":True,"coverage":{"defenders":[DEF]}}).miss
def test_wr_no_primary_fails():
    assert run({"type":"TE","receiving":True,"coverage":{"defenders":[]}}).miss
def test_period_spread_mismatch():
    g=run({"type":"SPREAD","team":"SEA","market":"2H spread -1.5","script_read":{"expected_winner":"CHI","source":"phase6"}})
    assert any("N3" in m for m in g.miss)
def test_period_spread_match():
    assert not run({"type":"SPREAD","team":"CHI","market":"1H spread +1.5","script_read":{"expected_winner":"CHI","source":"phase6"}}).miss
def test_period_spread_no_read():
    assert run({"type":"SPREAD","team":"CHI","market":"Q1 spread +1.5"}).miss
def test_full_game_spread_not_period():
    assert not run({"type":"SPREAD","team":"CHI","market":"spread +3.5"}).miss
def test_before_start_date_untouched():
    assert not run({"type":"RB"}, d="2026-11-01").miss

# Rico 2026-11-02 23:52 ET: SCHEME_EDGE under +3 is a flag + full breakdown, not a cut; other legs still need +3
import json, unittest, test_press_live as tpl
SE={k:{"ok":True,"source":"src_"+k,"detail":"d_"+k} for k in ("matchup","scheme_fit","script","form_trend")}
class SchemeEdgeAlert(tpl.LiveRun):
    def _set(self, se):
        m=json.load(open(self.mp)); l=m["legs"][0]; l["no_vig"]=0.565  # avg p .58 -> +1.5 < +3
        if se: l["scheme_edge"]=dict(SE, explanation="QB checks down to him vs middle zone")
        json.dump(m,open(self.mp,"w"))
    def test_flag_and_breakdown(self):
        self._set(True); c,o=tpl.gate(self.d,"2026-11-08T12:00")
        self.assertEqual(c,0,o); self.assertIn("SCHEME_EDGE ALERT",o); self.assertIn("src_scheme_fit",o)
        self.assertIn("middle zone",o); self.assertIn("model bias",o)
    def test_no_scheme_edge_still_cut(self):
        self._set(False); c,o=tpl.gate(self.d,"2026-11-08T12:00")
        self.assertEqual(c,1); self.assertIn("< +3",o)
    test_tags_manifest_report_tracker=None
