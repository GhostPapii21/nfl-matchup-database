"""Holdout freeze manifest: grading refuses when the manifest is absent or code/params hashes differ. Never reads
Week 10-12 actuals (the grading entry point stops before touching --actual-pbp)."""
from __future__ import annotations
import json
import shutil

import pytest

from calibration import opportunity_freeze as FZ
from calibration import opportunity_holdout_grade as HG


def _tree(tmp_path):
    for f in FZ.CODE_FILES + tuple(set(FZ.PARAMS.values())):
        d = tmp_path / f
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(FZ.ROOT / f, d)
    m = json.loads(FZ.HOLDOUT_MANIFEST.read_text())
    mp = tmp_path / FZ.HOLDOUT_MANIFEST.relative_to(FZ.ROOT)
    mp.parent.mkdir(parents=True, exist_ok=True)
    mp.write_text(json.dumps(m))
    return mp


def test_committed_manifest_matches_tree():
    m = FZ.check_freeze(10)
    assert m["data_max_week_used_for_fit"]["week"] == 9 and m["projection_ready"] is False
    assert set(m["holdout_weeks"]) == {10, 11, 12}


def test_refuses_without_manifest(tmp_path):
    mp = _tree(tmp_path)
    mp.unlink()
    with pytest.raises(FZ.FreezeError, match="no holdout freeze manifest"):
        FZ.check_freeze(10, root=tmp_path)


def test_refuses_when_params_change(tmp_path):
    _tree(tmp_path)
    p = tmp_path / FZ.PARAMS[11]
    p.write_text(p.read_text().replace('"rho": 0.975', '"rho": 0.99'))
    with pytest.raises(FZ.FreezeError, match="re-freeze"):
        FZ.check_freeze(11, root=tmp_path)


def test_refuses_when_model_code_changes(tmp_path):
    _tree(tmp_path)
    f = tmp_path / "core/possession_engine_v0/opportunity.py"
    f.write_text(f.read_text() + "\n# change\n")
    with pytest.raises(FZ.FreezeError, match="opportunity.py"):
        FZ.check_freeze(12, root=tmp_path)


def test_week_outside_holdout_refused():
    with pytest.raises(FZ.FreezeError):
        FZ.check_freeze(9)


def test_grading_entry_checks_freeze_before_reading_actuals(tmp_path, monkeypatch):
    missing = tmp_path / "does_not_exist.parquet"  # never opened
    monkeypatch.setattr(HG, "check_freeze", lambda w: (_ for _ in ()).throw(FZ.FreezeError("absent")))
    with pytest.raises(SystemExit, match="REFUSED"):
        HG.main(["--week", "10", "--actual-pbp", str(missing)])
    with pytest.raises(SystemExit, match="weeks"):
        HG.main(["--week", "9", "--actual-pbp", str(missing)])
