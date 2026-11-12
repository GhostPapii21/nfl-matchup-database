"""Ghost6 audit 2026-11-03 wiring tests (written before the code changes in depth_rule/door/rulebook/assemble)."""
import os, sys, pandas as pd, pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import depth_wiring as W, depth_rule as d, door
from rules import rulebook as rb
R3 = "/workspace/nfl-database/runs/2026-11-02_CHI@SEA_r3/src/"
GOOD = dict(type="WR", wr_rank=3, side="over", rung="low", price=-120, no_vig=0.53, injury_status="active",
            depth=dict(script_pass=dict(ok=True, source="p13"), target_share=dict(value=0.09, source="pbp"), defender_giving=dict(ok=True, source="ledger")))

def _pbp():
    rows = []
    for g, qb in (("2026-10-01", "QB1"), ("2026-10-08", "QB2"), ("2026-10-15", "QB1")):
        rows += [dict(game_date=g, posteam="T", qb_dropback=1, passer_player_id=qb, rusher_player_id=None, rush_attempt=0, pass_attempt=1, sack=0, receiver_player_id=r) for r in ("W1", "W1", "TE1", "TE2", "TE1")]
        rows += [dict(game_date=g, posteam="T", qb_dropback=0, passer_player_id=None, rusher_player_id=r, rush_attempt=1, pass_attempt=0, sack=0, receiver_player_id=None) for r in ("RB1", "RB1", "RB2", "QB1", "QB1", "WR9")]
    return pd.DataFrame(rows)
POS = dict(RB1="RB", RB2="RB", QB1="QB", QB2="QB", WR9="WR", W1="WR", TE1="TE", TE2="TE")

# N1
def test_n1_rb_only_current_qb():
    cs = W.rb_carry_share(_pbp(), POS, "T", "RB1", "QB1")
    assert cs["value"] == pytest.approx(2 / 3, abs=1e-3) and cs["games"] == ["2026-10-01", "2026-10-15"]
@pytest.mark.skipif(not os.path.exists(R3 + "play_by_play_2026.parquet"), reason="r3 pbp")
def test_n1_swift_real():
    p = pd.read_parquet(R3 + "play_by_play_2026.parquet"); pl = pd.read_parquet(R3 + "players.parquet", columns=["gsis_id", "position"])
    sw = p[p.rusher_player_name == "D.Swift"].rusher_player_id.iloc[0]
    qb = p[(p.posteam == "CHI") & (p.passer_player_name == "C.Williams")].passer_player_id.iloc[0]
    cs = W.rb_carry_share(p, dict(zip(pl.gsis_id, pl.position)), "CHI", sw, qb)
    assert cs["value"] >= 0.60 and "2026-10-04" not in cs["games"]
# (a) depth fields
def test_target_share_current_qb():
    t = W.target_share(_pbp(), "T", "TE2", "QB1"); assert t["value"] == pytest.approx(0.2) and t["attempts"] == 10
def test_te_rank(): assert W.te_rank(_pbp(), POS, "T", "TE2", "QB1") == 2 and W.te_rank(_pbp(), POS, "T", "TE1", "QB1") == 1
def test_rung(): assert (W.rung(9.5, 19.5), W.rung(19.5, 19.5), W.rung(29.5, 19.5)) == ("low", "main", "high")
def test_script_pass():
    assert W.script_pass(3.5, 40, "odds")["ok"] and W.script_pass(-3, 48.5, "odds")["ok"] and not W.script_pass(-6, 42.5, "odds")["ok"]
    assert W.script_pass(None, 42, "odds")["ok"] is None
# (b) fail closed
def test_depth_missing_wr_rank_fails_closed():
    ok, w = d.evaluate(dict(GOOD, wr_rank=None)); assert not ok and any("wr_rank missing" in x for x in w)
def test_depth_missing_te_rank_fails_closed():
    ok, w = d.evaluate(dict(GOOD, type="TE", wr_rank=None, te_rank=None)); assert not ok and any("te_rank missing" in x for x in w)
def test_depth_missing_rank_under_unaffected(): assert d.evaluate(dict(GOOD, wr_rank=None, side="under"))[0]
def test_wr1_still_not_depth(): assert d.evaluate(dict(type="WR", wr_rank=1, side="over"))[0]
# (c) NO_PASS_YDS
def test_no_pass_yds_rule_exists(): assert rb.rule("NO_PASS_YDS")["sev"] == "BLOCK" and rb.rule("NO_PASS_YDS")["approved_by"] == "Rico"
@pytest.mark.parametrize("name,mk", [("Caleb Williams passyds over 224.5", "passyds"), ("Sam Darnold Pass Yds Over 199.5 [low]", "passyds"), ("X Alt Passing Yards 250+", "")])
def test_no_pass_yds_blocks(name, mk):
    f = door.leg_rules(name, dict(name=name, market=mk, type="QB", side="over", price=-110, no_vig=0.5, injury_status="active", recent_form=dict(values=[1], source="s")), {})
    assert any(x["rule"] == "NO_PASS_YDS" for x in f)
def test_no_pass_yds_ignores_rec_yds():
    f = door.leg_rules("JSN recyds over 89.5", dict(name="JSN recyds over 89.5", market="recyds", type="WR", wr_rank=1, side="over", price=-110, no_vig=0.5, injury_status="active", recent_form=dict(values=[1], source="s")), {})
    assert not any(x["rule"] == "NO_PASS_YDS" for x in f)
# (d) coverage-level vs zone-heavy
def test_defender_giving_defender_level():
    assert W.defender_giving(dict(name="CB", ypt=8.1, targets=20, source="pfr"), 7.2)["level"] == "defender"
def test_defender_giving_zone_coverage_level():
    g = W.defender_giving(dict(name="Pritchett", ypt=4.22, targets=9, source="pfr"), 7.2, zone_pct=90.0, coverage_allow=dict(value=8.4, bucket="WR middle", source="pbp"), league_cov=7.6)
    assert g["ok"] and g["level"] == "coverage"
def test_defender_giving_no_coverage_below_75():
    g = W.defender_giving(dict(name="CB", ypt=4.2, targets=9, source="pfr"), 7.2, zone_pct=70.0, coverage_allow=dict(value=9.0, source="pbp"), league_cov=7.6)
    assert not g["ok"]
# (e) slot/primary
def test_slot_primary_kupp():
    m = W.slot_primary(dict(defender="Kyler Gordon", lwr=10, slot=75, rwr=15), dict(nb=["Kyler Gordon"]))
    assert m["name"] == "Kyler Gordon" and "slot" in m["basis"]
    m = W.slot_primary(dict(defender="Jaylon Johnson", lwr=10, slot=75, rwr=15), dict(nb=["Kyler Gordon"]))
    assert m["name"] == "Kyler Gordon"
def test_outside_wr_keeps_charted(): assert W.slot_primary(dict(defender="Tyrique Stevenson", lwr=60, slot=10, rwr=30), dict(nb=["Gordon"]))["name"] == "Tyrique Stevenson"
