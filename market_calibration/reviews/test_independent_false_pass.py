"""Independent regression probes; synthetic mutations are not observed quotes."""
from dataclasses import replace
import json
from pathlib import Path

import pytest

from market_calibration.quotes import GAME_ID, MatchRequest, load_saved_quotes, match_quote
from market_calibration.manifest import validate_manifest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("other_snapshot", ["independent-fixture-B", None])
def test_no_pair_across_explicit_snapshot_identity(other_snapshot):
    req = MatchRequest(GAME_ID, "pinnacle", "spreads", "Q1", "JAX", -2.5,
                       "spread_2way", "2026-11-05T20:00:00Z", "2026-11-05T20:00:00Z")
    pair = match_quote(load_saved_quotes(), req).quotes
    changed = [replace(pair[0], snapshot_id="independent-fixture-A"),
               replace(pair[1], snapshot_id=other_snapshot)]
    result = match_quote(changed, req)
    assert result.status != "MATCHED"
    assert result.probabilities is None
    coherent = [replace(q, snapshot_id="independent-fixture-A") for q in pair]
    assert match_quote(coherent, req).status == "MATCHED"


@pytest.mark.parametrize("section,key,value", [
    ("quotes", "network", True),
    ("quotes", "actionable_status", "MATCHED"),
    ("quotes", "canonical_crosswalk", "VERIFIED"),
    ("quotes", "rule_compatibility", "VERIFIED"),
    ("quotes", "identity_namespace", "CANONICAL"),
    ("quotes", "pinnacle_q2_q3_q4_spreads", "MATCHED"),
    ("adapter", "producer_simulations", "COMPLETE"),
    ("adapter", "player_targets", "IMPLEMENTED"),
    ("raw_outputs", "status", "VALIDATED"),
])
def test_manifest_rejects_contradictory_secondary_success_claims(section, key, value):
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
    manifest[section][key] = value
    with pytest.raises(ValueError):
        validate_manifest(manifest, ROOT)
