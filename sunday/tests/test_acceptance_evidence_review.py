from datetime import datetime, timezone
from sunday.joinflow import hashes_match, build_joined_decision_input
from sunday.stack import ORDER, acceptance_result

def test_hashes_require_all_three_valid_digests():
    h = {k: "a"*64 for k in ("research", "script", "player_board")}
    assert hashes_match(h, h)
    assert not hashes_match({}, {})
    assert not hashes_match({"research": "a"*64}, h)
    assert not hashes_match(dict(h, script="bad"), dict(h, script="bad"))

def test_kickoff_boundary_and_missing_timestamp():
    now = datetime(2026, 11, 29, 18, tzinfo=timezone.utc)
    for kickoff in (now.isoformat(), None, "invalid"):
        packet = build_joined_decision_input(game={}, kickoff_utc=kickoff,
            kickoff_verification="VERIFIED", as_of=now, research={}, script={},
            players={}, market_packet={}, hashes={k:"a"*64 for k in
            ("research","script","player_board")}, base_packet={})
        assert packet["joined"]["problems"]

def test_analytical_receipt_required():
    rows = [{"id": cid, "status": "EXECUTED", "kind": "analytical",
             "analytical_execution": True} for cid in ORDER]
    assert acceptance_result([]) == "BLOCKED"
    assert acceptance_result(rows) == "PASS"
    assert acceptance_result(rows[:-1]) == "PARTIAL"
    assert acceptance_result(rows + [rows[-1]]) == "PARTIAL"
    assert acceptance_result(rows[:-1] + [dict(rows[-1], analytical_execution=False)]) == "PARTIAL"
    assert acceptance_result(rows[:-1] + [dict(rows[-1], status="UNKNOWN")]) == "PARTIAL"
