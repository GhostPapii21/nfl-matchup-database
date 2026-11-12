import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import depth_rule as d, press_tier as pt
GOOD = dict(type="WR", wr_rank=3, side="over", rung="low", price=-120, no_vig=0.53, injury_status="active",
            depth=dict(script_pass=dict(ok=True, source="phase13"), target_share=dict(value=0.09, source="pbp"), defender_giving=dict(ok=True, source="ledger")))
def test_depth_ok(): assert d.evaluate(GOOD) == (True, [])
def test_depth_low_share():
    ok, w = d.evaluate(dict(GOOD, depth=dict(GOOD["depth"], target_share=dict(value=0.04, source="pbp")))); assert not ok and "< 5%" in w[0]
def test_depth_missing_fails_closed():
    ok, w = d.evaluate(dict(GOOD, depth={})); assert not ok and len(w) == 3
def test_depth_high_rung(): assert not d.evaluate(dict(GOOD, rung="mid"))[0]
def test_wr2_not_depth(): assert d.evaluate(dict(type="WR", wr_rank=2, side="over"))[0]
def test_under_unaffected(): assert d.evaluate(dict(GOOD, depth={}, side="under"))[0]
def test_press_tier_no_longer_blanket_bans():
    base = dict(weather_stop=False, injury_status="active", on_inactives=False, sec11_conflict=False, wr_rank=3)
    assert "DEPTH_RECEIVER" in pt.evaluate(base)["reason"]          # missing depth data -> BLOCKED with depth reason
    r = pt.evaluate(dict(GOOD, **{k: v for k, v in base.items() if k != "injury_status"}))
    assert r["tier"] != "BLOCKED" or "DEPTH" not in r["reason"]
