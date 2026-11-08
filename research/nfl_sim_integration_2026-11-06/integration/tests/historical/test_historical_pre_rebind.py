"""HISTORICAL_PRE_REBIND_RECORD: original expectations, never live acceptance.

These exact assertions/staged mutations are retained from the pre-refresh suite.
They describe the earlier adapter binding/wire behavior and are deliberately
skipped against the authorized current implementation. No old adapter is loaded,
no contract path is overridden, and no historical bytes are fed to the adapter.
Run separately with: python3 -m pytest integration/tests/historical -q -rs
"""
from copy import deepcopy
import pytest
from integration.integration_adversarial_tests import (
    ROOT, adapter, digest, producer_rows, RETAINED_IDS,
)

CONTRACT_HASH = "d6a4689f55bbc1231205dccf1d19de51019c40d87a7f7c1fd4ba5238cec836b9"
pytestmark = pytest.mark.skip(reason="HISTORICAL_PRE_REBIND_RECORD: superseded binding and missing-field stages; separate archival suite")


def test_contract_sha256_binding():
    assert digest(ROOT / "core_contract.md") == CONTRACT_HASH, "BLOCKER CONTRACT_HASH_MISMATCH"
    assert adapter.contract_info()["status"] == "CONTRACT_SCORE_TRANSPORT_ONLY"


@pytest.mark.parametrize("stage,error", [
    (0, "missing trial fields"), (1, "unsupported contract or incomplete/invalid"),
    (2, "missing freeze fields"), (3, "missing engine fields"),
    (4, "missing team_periods fields"),
])
def test_diagnostic_wire_blockers_are_independently_reproducible(producer_rows, stage, error):
    # Progressively expose errors masked by the first missing-field rejection.
    # Each staged copy is deliberately NOT represented as unchanged producer wire.
    rows = deepcopy(producer_rows)
    for row in rows:
        if stage >= 1:
            for key in ("completion_reason", "terminal_state", "went_ot"):
                row[key] = deepcopy(row["status"][key])
        if stage >= 2:
            row["status"] = row["status"]["state"]
        if stage >= 3:
            row["freeze"]["input_manifest_hash"] = row["freeze"]["input_manifest_digest"]
        if stage >= 4:
            row["engine"]["component_versions"] = {"joint_producer": row["engine"]["component_version"]}
            row["engine"]["dependency_versions"] = deepcopy(row["engine"]["dependencies"])
    with pytest.raises(ValueError, match=error):
        adapter.adapt_joint_trials(rows, expected_trial_ids=RETAINED_IDS)

