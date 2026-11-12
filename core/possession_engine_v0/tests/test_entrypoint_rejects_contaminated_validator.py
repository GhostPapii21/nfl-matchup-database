"""NFL-42 item 4 (missing test 1/2): the contaminated suite_fix validator can never be invoked or promoted."""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pytest
from validation.entrypoint import ContaminatedEntrypoint, invoke, registry, run_validation

OLD = ROOT / "runs/dal_ind_suite_fix_2026-11-06/validate.py"
NEW = ROOT / "runs/dal_ind_invariance_decontam_2026-11-06/validate.py"


def test_old_gate_invoke_is_rejected():
    with pytest.raises(ContaminatedEntrypoint, match="CONTAMINATED"):
        invoke(OLD)


def test_copied_contaminated_bytes_are_rejected_by_hash(tmp_path):
    clone = tmp_path / "validate.py"
    clone.write_bytes(OLD.read_bytes())
    with pytest.raises(ContaminatedEntrypoint):
        invoke(clone)


def test_unregistered_validator_is_rejected(tmp_path):
    other = tmp_path / "validate.py"
    other.write_text("print('hi')\n")
    with pytest.raises(ContaminatedEntrypoint, match="not the registered"):
        invoke(other)


def test_contaminated_bytes_unchanged():
    assert hashlib.sha256(OLD.read_bytes()).hexdigest() == "29b6b0c2644f256a705b09b5e1a56716dd355d79eb07a6187b9c3df495ff93e9"


def test_entrypoint_routes_to_decontam_and_never_sets_policy():
    r = run_validation()
    assert r["status"] == "PASS", r
    assert r["accepted_policy"] is None
    assert r["policy_status"] == "RESEARCH_PROVISIONAL_NOT_PROMOTED"
    assert registry()["authorized"]["path"].endswith("dal_ind_invariance_decontam_2026-11-06/validate.py")
    assert invoke(NEW) == NEW.resolve()
