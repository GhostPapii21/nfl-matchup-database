"""NFL-42 item 4 (missing test 2/2): consumers cannot load contaminated role-policy metrics as production policy."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pytest
from validation.entrypoint import ContaminatedEntrypoint, load_role_policy

OLD_METRICS = ROOT / "runs/dal_ind_suite_fix_2026-11-06/role_policy_metrics.json"
NEW_METRICS = ROOT / "runs/dal_ind_invariance_decontam_2026-11-06/role_policy_metrics.json"


def test_contaminated_metrics_path_rejected():
    with pytest.raises(ContaminatedEntrypoint, match="CONTAMINATED_METRICS"):
        load_role_policy(OLD_METRICS)


def test_contaminated_metrics_copy_rejected_by_hash(tmp_path):
    p = tmp_path / "m.json"
    p.write_bytes(OLD_METRICS.read_bytes())
    with pytest.raises(ContaminatedEntrypoint):
        load_role_policy(p)


@pytest.mark.parametrize("payload", [{"accepted_policy": "mix_equal_0.25"}, {"accepted_policy": None, "gate_passed": True}])
def test_any_promoting_metrics_rejected(tmp_path, payload):
    p = tmp_path / "m.json"
    p.write_text(json.dumps(payload))
    with pytest.raises(ContaminatedEntrypoint, match="promotes"):
        load_role_policy(p)


def test_decontam_metrics_load_without_policy():
    m = load_role_policy(NEW_METRICS)
    assert m["accepted_policy"] is None and m["status"] == "RESEARCH_PROVISIONAL_NOT_PROMOTED"
