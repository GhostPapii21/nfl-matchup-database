import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rules import rulebook as rb
def test_every_rule_has_fields():
    for i, r in rb.RULES.items():
        assert r["sev"] in ("BLOCK", "FLAG", "WARN"), i
        assert r["text"] and "approved_by" in r and "params" in r, i
def test_rico_rules_have_timestamp():
    for i, r in rb.RULES.items():
        if r["approved_by"] == "Rico": assert r["approved_at"], i
def test_backdated_manifest_cannot_disable():
    assert rb.active("N1", game_date="2026-10-01", now="2026-11-03T09:00")
    assert not rb.active("N1", game_date="2026-10-01", now="2026-10-01T09:00")
def test_always_on():
    assert rb.active("NOSHRINK") and rb.active("DEPTH_RECEIVER", "1999-01-01")
def test_cap_is_warn_and_last2_warn():
    assert rb.rule("DEPTH_CAP")["sev"] == "WARN" and rb.rule("SCHEME_EDGE_LAST2")["sev"] == "WARN"
def test_version_stable():
    assert rb.version() == rb.version() and len(rb.version()) == 16
def test_nba_one_market_per_player_blocks_two_markets_same_night():
    r = rb.rule("NBA_ONE_MARKET")
    assert r["sev"] == "BLOCK" and r["approved_by"] == "Rico" and r["approved_at"] == "2026-11-03T01:41"
    slip = [dict(player="Lauri Markkanen", market="player_points", date="2026-11-02"),
            dict(player="Lauri Markkanen", market="player_points_rebounds_assists", date="2026-11-02"),
            dict(player="Cam Johnson", market="player_points", date="2026-11-02")]
    assert rb.one_market_violations(slip) == [("Lauri Markkanen", "2026-11-02")]
    assert rb.one_market_violations(slip[1:]) == []
    assert rb.one_market_violations([slip[0], dict(slip[1], date="2026-11-03")]) == []
def test_nba_role_bump_registered():
    r = rb.rule("NBA_ROLE_BUMP")
    assert r["approved_by"] == "Rico" and r["approved_at"] == "2026-11-03T01:42" and rb.param("NBA_ROLE_BUMP", "min_minutes") == 28.0
