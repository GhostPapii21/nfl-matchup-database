"""Production safeguard: PROTOCOL_FREEZE protocol hash must match the live protocol file."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_freeze_protocol_sha_matches_protocol_file():
    proto = ROOT / "evaluation/PRISTINE_EVALUATION_PROTOCOL.json"
    fz = json.loads((ROOT / "evaluation/PROTOCOL_FREEZE.json").read_text())
    assert fz["protocol_sha256"] == hashlib.sha256(proto.read_bytes()).hexdigest()
    assert fz["historical_pristine_claim"] is False


def test_freeze_amendment_records_prior_sha_when_present():
    fz = json.loads((ROOT / "evaluation/PROTOCOL_FREEZE.json").read_text())
    amendments = fz.get("amendments") or []
    if not amendments:
        return
    last = amendments[-1]
    assert last["new_protocol_sha256"] == fz["protocol_sha256"]
    assert last["previous_protocol_sha256"]
    assert "aggregation" in last["reason"].lower()
