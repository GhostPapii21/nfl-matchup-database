"""NFL-44 / NFL-45: protocol freeze, coverage gate, unscorable reasons, NOLINE fail-closed, calibration flags."""
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from evaluation import protocol as P

NOW = datetime(2026, 11, 12, 17, 0, tzinfo=timezone.utc)


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _lock(root, gid="2026_10_A_B", locked="2026-11-12T16:00:00+00:00", ko="2026-11-13T01:15:00+00:00",
          prices=True, n=100000, dirty=False, score=None):
    d = root / "snapshots" / gid / locked[:19].replace("-", "").replace(":", "")
    (d / "inputs").mkdir(parents=True)
    (d / "summary.json").write_text("{}")
    if prices:
        (d / "inputs/team_prices_x.json").write_text(json.dumps({"rows": [
            {"book": "draftkings", "market": "h2h", "price_a": 110, "price_b": -130, "player": None}]}))
    lk = {"game_id": gid, "locked_utc": locked, "kickoff_utc": ko, "code_dirty": dirty, "asof_checks": "PASS",
          "sim": {"n": n}, "projection_ready": False,
          "inputs": {"price_freeze_pulled_utc": "2026-11-12T15:00:00Z" if prices else None,
                     "price_status": "OK" if prices else "NOLINE", "price_freeze_origin": "o", "price_freeze_sha256": "s"},
          "files": {}}
    lk["files"] = {str(p.relative_to(d)): _sha(p) for p in d.rglob("*") if p.is_file()}
    (d / "LOCK.json").write_text(json.dumps(lk))
    if score is not None:
        (d / "SCORE.json").write_text(json.dumps({"metrics": score}))
    return d


def _root(tmp_path):
    (tmp_path / "evaluation").mkdir()
    shutil.copy(ROOT / "evaluation/PRISTINE_EVALUATION_PROTOCOL.json", tmp_path / "evaluation/")
    return tmp_path


M = {"win_logloss": 0.6, "win_brier": 0.2, "margin_crps": 8.0, "total_crps": 7.0, "margin_pit": 0.5,
     "total_pit": 0.5, "brier_model_mean_lines": 0.2, "brier_book_mean_lines": 0.25}


def test_protocol_flags():
    d = json.loads((ROOT / "evaluation/PRISTINE_EVALUATION_PROTOCOL.json").read_text())
    assert d["historical_pristine_claim"] is False
    assert d["insufficient_coverage_status"] == "UNSCORABLE_INSUFFICIENT_COVERAGE"
    assert {"NOLINE", "NOT_FINAL", "LOCK_HASH_MISMATCH", "NO_PROTOCOL_FREEZE"} <= set(d["unscorable_reasons"])


def test_no_freeze_means_nothing_scored(tmp_path):
    r = _root(tmp_path); _lock(r, score=M)
    e = P.evaluate(r)
    assert e["games"][0]["status"] == "NO_PROTOCOL_FREEZE" and e["games_scored"] == 0
    assert e["status"] == "UNSCORABLE_INSUFFICIENT_COVERAGE"


def test_freeze_hashes_only_future_unscored_locks(tmp_path):
    r = _root(tmp_path)
    _lock(r, "2026_10_A_B")
    _lock(r, "2026_09_C_D", locked="2026-11-05T16:00:00+00:00", ko="2026-11-06T01:15:00+00:00")
    fz = P.freeze(r, now=NOW)
    assert [x["game_id"] for x in fz["locks"]] == ["2026_10_A_B"] and fz["historical_pristine_claim"] is False
    try:
        P.freeze(r, now=NOW); assert False
    except SystemExit:
        pass


def test_scoring_coverage_and_reasons(tmp_path):
    r = _root(tmp_path)
    a = _lock(r, "2026_10_A_B")
    _lock(r, "2026_10_E_F", dirty=True)
    _lock(r, "2026_10_G_H", n=6000)
    _lock(r, "2026_10_I_J", prices=False)
    P.freeze(r, now=NOW)
    for gid in ("2026_10_A_B", "2026_10_E_F", "2026_10_G_H", "2026_10_I_J"):
        for d in (r / "snapshots" / gid).iterdir():
            (d / "SCORE.json").write_text(json.dumps({"metrics": M}))
    e = P.evaluate(r)
    st = {g["game_id"]: g for g in e["games"]}
    assert st["2026_10_A_B"]["status"] == "SCORED"
    assert st["2026_10_E_F"]["status"] == "CODE_DIRTY"
    assert st["2026_10_G_H"]["status"] == "N_SIMS_NOT_100K"
    assert st["2026_10_I_J"]["status"] == "SCORED" and st["2026_10_I_J"]["market_comparison"] == "NOLINE"
    assert st["2026_10_I_J"]["metrics"]["brier_book_mean_lines"] is None
    assert e["status"] == "UNSCORABLE_INSUFFICIENT_COVERAGE" and e["independently_calibrated"] is False
    (a / "summary.json").write_text('{"x":1}')
    assert {g["game_id"]: g for g in P.evaluate(r)["games"]}["2026_10_A_B"]["status"] == "LOCK_HASH_MISMATCH"


def test_lock_made_before_freeze_but_not_hashed_is_rejected(tmp_path):
    r = _root(tmp_path)
    P.freeze(r, now=NOW)
    _lock(r, "2026_10_A_B", score=M)  # locked 16:00 < freeze 17:00 and not listed
    assert P.evaluate(r)["games"][0]["status"] == "NOT_COVERED_BY_PROTOCOL_FREEZE"


def test_protocol_change_after_freeze_refuses(tmp_path):
    r = _root(tmp_path)
    P.freeze(r, now=NOW)
    p = r / "evaluation/PRISTINE_EVALUATION_PROTOCOL.json"
    p.write_text(p.read_text().replace('"games_scored": 30', '"games_scored": 1'))
    try:
        P.evaluate(r); assert False
    except SystemExit:
        pass


def test_quote_ledger_provenance_and_noline(tmp_path):
    r = _root(tmp_path)
    _lock(r, "2026_10_A_B"); _lock(r, "2026_10_I_J", prices=False)
    L = P.quote_ledger(r)
    g = {x["game_id"]: x for x in L["games"]}
    assert g["2026_10_A_B"]["price_status"] == "OK" and g["2026_10_A_B"]["source_sha256"] == "s"
    assert g["2026_10_A_B"]["quotes"][0]["book"] == "draftkings"
    assert g["2026_10_I_J"]["price_status"] == "NOLINE"
    assert L["independently_calibrated"] is False and L["market_anchored"] == "NOT_PRODUCED"
