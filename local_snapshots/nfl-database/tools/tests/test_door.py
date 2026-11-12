import json, os, sys, importlib, subprocess
from datetime import datetime
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import door_fixture as fx
NOW = datetime.fromisoformat(fx.NOW)
H, C, B, G = "Tee Higgins rec yds o58.5 -115", "Ja'Marr Chase rec yds o70.5 -120", "Chase Brown rush yds o62.5 -110", "Mike Gesicki rec yds o30.5 -110"
def setup():
    d, out = fx.make(); import door; importlib.reload(door); door.OUT = out; fx.green(door)
    import verify_stamp; importlib.reload(verify_stamp); return d, door, verify_stamp
def rules(r): return {f["rule"] for f in r["fails"]}

def test_clean_slip_passes_and_stamp_verifies():
    d, door, vs = setup(); r = door.build(fx.slip(d, [H, C, B]), NOW)
    assert r["status"] == "PASS", r["fails"]; assert vs.verify(r["file"])[0]
def test_hand_built_slip_fails_stamp():
    d, door, vs = setup(); p = door._o("approved", "x.json"); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(dict(slip_id="x", legs=[H, C, B]), open(p, "w")); assert not vs.verify(p)[0]
def test_edited_slip_fails_stamp():
    d, door, vs = setup(); r = door.build(fx.slip(d, [H, C, B]), NOW); rec = json.load(open(r["file"]))
    rec["payload"]["legs"][0]["line"] = 40.5; json.dump(rec, open(r["file"], "w")); assert "edited" in vs.verify(r["file"])[1]
def test_red_suite_blocks_stamp():
    d, door, vs = setup(); os.remove(door.status_f()); r = door.build(fx.slip(d, [H, C, B]), NOW)
    assert r["status"] == "BLOCKED" and "TEST_SUITE" in rules(r)
def test_five_legs_blocked():
    d, door, _ = setup(); fx.clone(d, H, "Tee Higgins rec yds o50.5 -140"); fx.clone(d, H, "Tee Higgins rec yds o45.5 -160")
    r = door.build(fx.slip(d, [H, C, B, G, "Tee Higgins rec yds o50.5 -140"]), NOW); assert "SLIP_SIZE" in rules(r) and r["status"] == "BLOCKED"
def test_td_leg_blocked():
    d, door, _ = setup(); fx.clone(d, H, "Tee Higgins anytime TD +150")
    r = door.build(fx.slip(d, [H, C, "Tee Higgins anytime TD +150"]), NOW); assert "NO_TD" in rules(r)
def test_missing_field_fails_closed():
    d, door, _ = setup(); fx.edit_leg(d, C, injury_status=None); r = door.build(fx.slip(d, [H, C, B]), NOW)
    assert any(f["rule"] == "INJURY" and "missing" in f["words"] for f in r["fails"]) and r["status"] == "BLOCKED"
def test_rb_missing_role_fails_closed():
    d, door, _ = setup(); fx.edit_leg(d, B, rb_role=None); r = door.build(fx.slip(d, [H, C, B]), NOW); assert "RB_TRAIL" in rules(r)
def test_rb_trailing_needs_4_targets():
    d, door, _ = setup(); fx.edit_leg(d, B, rb_role=dict(share60_3of4=True, tgt_pg=2.0, may_trail=True, source="pbp"))
    assert "RB_TRAIL" in rules(door.build(fx.slip(d, [H, C, B]), NOW))
def test_missing_team_file_blocks():
    d, door, _ = setup(); os.remove(door._o("teams", "CIN.json")); r = door.build(fx.slip(d, [H, C, B]), NOW)
    assert any(f["rule"] == "TEAM_FILES" and f["value"] == "CIN" for f in r["fails"])
def test_short_price_is_flag_not_block():
    d, door, _ = setup(); fx.edit_leg(d, C, price_fd=-260); r = door.build(fx.slip(d, [H, C, B]), NOW)
    assert "SHORT_PRICE" in rules(r) and r["status"] == "PASS"
def test_gate_fail_blocks_every_leg():
    d, door, _ = setup(); fx.edit_leg(d, H, no_vig=None); r = door.build(fx.slip(d, [H, C, B]), NOW)
    assert "GATE_PASS" in rules(r) and r["status"] == "BLOCKED"
def test_leg_not_in_run_is_hand_built():
    d, door, _ = setup(); r = door.build(fx.slip(d, [H, C, "Made Up Guy o9.5"]), NOW); assert "GATE_PASS" in rules(r)
def test_depth_cap_is_warn():
    d, door, _ = setup()
    dep = dict(type="WR", wr_rank=3, rung="low", depth=dict(script_pass=dict(ok=True, source="s"), target_share=dict(value=.1, source="pbp"), defender_giving=dict(ok=True, source="ledger")))
    fx.edit_leg(d, C, **dep); fx.edit_leg(d, H, **dep); r = door.build(fx.slip(d, [H, C, B]), NOW)
    assert any(f["rule"] == "DEPTH_CAP" and f["sev"] == "WARN" for f in r["fails"]) and r["status"] == "PASS", r["fails"]
def test_block_report_has_plain_words():
    d, door, _ = setup(); fx.edit_leg(d, C, injury_status="Out"); r = door.build(fx.slip(d, [H, C, B]), NOW)
    t = open(r["file"]).read(); assert "INJURY" in t and "player is Out" in t and C in t and "SWAP" in t and "OVERRIDE" in t
def test_cli_exits_nonzero_on_block(tmp_path):
    d, door, _ = setup(); s = tmp_path / "s.json"; json.dump(fx.slip(d, [H]), open(s, "w"))
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(HERE), "door.py"), "check", str(s)], capture_output=True, text=True, env=dict(os.environ, DOOR_OUT=door.OUT))
    assert r.returncode == 1 and "SLIP_SIZE" in r.stdout
def test_cli_has_no_now_flag():
    import door; assert "--now" not in open(door.__file__).read().split("def main", 1)[1]
# ---- swap / override ----
def _blocked(door, d):
    fx.edit_leg(d, C, injury_status="Out"); r = door.build(fx.slip(d, [H, C, B], "S1"), NOW); assert r["status"] == "BLOCKED"; return r
def test_swap_proposed_not_applied():
    d, door, _ = setup(); _blocked(door, d); p = door.propose_swap("S1", NOW)
    assert p["replaced"] == [C] and p["with_"] == [G] and p["would_status"] == "PASS" and p["applied"] is False
    assert not os.path.exists(door._o("approved", "2026-11-08", "S1_swap.json"))
def test_swap_needs_rico():
    d, door, _ = setup(); _blocked(door, d); door.propose_swap("S1", NOW)
    assert "error" in door.apply_swap("S1", "Ghost6", "2026-11-08T11:00", "ok", NOW)
    r = door.apply_swap("S1", "Rico", "2026-11-08T11:00", "Yes swap it", NOW); assert r["status"] == "PASS"
    assert os.path.exists(door._o("approved", "2026-11-08", "S1_swap.json"))
def test_override_without_approved_by_fails():
    d, door, _ = setup(); _blocked(door, d)
    assert "error" in door.override("S1", ["INJURY"], "r", None, "2026-11-08T11:00", "yes", NOW)
    assert "error" in door.override("S1", ["INJURY"], "r", "Rico", None, "yes", NOW)
    assert "error" in door.override("S1", ["INJURY"], "r", "Rico", "2026-11-08T11:00", "", NOW)
    assert "error" in door.override("S1", ["INJURY"], "r", "Rico", "2026-11-08T11:00", "Ghost6 relayed: Rico said ok", NOW)
    assert "error" in door.override("S1", ["N1"], "r", "Rico", "2026-11-08T11:00", "yes", NOW)   # rule that did not fail
def test_override_logged_and_marked():
    d, door, vs = setup(); _blocked(door, d)
    r = door.override("S1", ["INJURY"], "he was activated late", "Rico", "2026-11-08T11:00", "Yes play him", NOW)
    assert r["status"] == "OVERRIDDEN"; rec = json.load(open(r["file"]))
    assert rec["payload"]["status"] == "OVERRIDDEN" and rec["payload"]["overrides"][0]["rule"] == "INJURY"
    log = [json.loads(x) for x in open(door._o("overrides.log"))]; assert log[-1]["slip_id"] == "S1" and log[-1]["rules"] == ["INJURY"]
    ok, why = vs.verify(r["file"]); assert ok and "overridden" in why
# ---- NBA routed through the stamp only (gates.py logic unchanged) ----
NBA = dict(market="player_points", side="Over", line=20.5, base=5, worst=1, dvp=1.2, median=24, starter=True, spread=-3, h2h=25, l10mean=24, assist_avg=3)
def test_nba_pass_stamped_and_fail_blocked():
    d, door, vs = setup()
    s = dict(slip_id="N1", date="2026-11-08", sport="NBA", legs=[dict(leg=f"p{i}", gate_inputs=NBA) for i in range(3)])
    r = door.build(s, NOW); assert r["status"] == "PASS", r["fails"]; assert vs.verify(r["file"])[0]
    s2 = dict(s, slip_id="N2", legs=s["legs"][:2] + [dict(leg="bad", gate_inputs=dict(NBA, base=1))])
    assert door.build(s2, NOW)["status"] == "BLOCKED"
