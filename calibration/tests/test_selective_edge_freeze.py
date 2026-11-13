"""Phase 4 freeze manifest: live grading (Weeks 10-12) refuses unless the classifier code and the W4-7 params match
the committed manifest. Research only; projection_ready stays false."""
from __future__ import annotations
import json
import shutil

import numpy as np
import pandas as pd
import pytest

from calibration import selective_edge_freeze as FZ
from calibration import selective_edge_live as LV


def _tree(tmp_path):
    for f in FZ.CODE_FILES + (FZ.PARAMS_FILE,):
        d = tmp_path / f
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(FZ.ROOT / f, d)
    mp = tmp_path / FZ.MANIFEST.relative_to(FZ.ROOT)
    mp.parent.mkdir(parents=True, exist_ok=True)
    mp.write_text(FZ.MANIFEST.read_text())
    return mp


def test_committed_manifest_matches_tree():
    m = FZ.check_freeze(10)
    assert m["fit_weeks"] == [4, 5, 6, 7] and m["eval_weeks"] == [8, 9]
    assert m["holdout_weeks"] == [10, 11, 12] and m["projection_ready"] is False


def test_refuses_without_manifest(tmp_path):
    _tree(tmp_path).unlink()
    with pytest.raises(FZ.FreezeError, match="no freeze manifest"):
        FZ.check_freeze(10, root=tmp_path)


def test_refuses_when_params_change(tmp_path):
    _tree(tmp_path)
    p = tmp_path / FZ.PARAMS_FILE
    d = json.loads(p.read_text())
    d["alt_min_cushion"] = 0.01
    p.write_text(json.dumps(d))
    with pytest.raises(FZ.FreezeError, match="differ"):
        FZ.check_freeze(11, root=tmp_path)


def test_refuses_when_code_changes(tmp_path):
    _tree(tmp_path)
    f = tmp_path / "calibration/selective_edge.py"
    f.write_text(f.read_text() + "\n# tweak\n")
    with pytest.raises(FZ.FreezeError, match="differ"):
        FZ.check_freeze(12, root=tmp_path)


def test_refuses_week_not_in_holdout(tmp_path):
    _tree(tmp_path)
    with pytest.raises(FZ.FreezeError, match="not covered"):
        FZ.check_freeze(13, root=tmp_path)


def _live_leg(week):
    return dict(week=week, game_id=f"2026_{week:02d}_AAA_BBB", gsis="A", player="A", position="RB",
                market="rushyds", side="Under", kind="main", line=60.5, dec=1.91, p_nv=0.5, p_model=0.56,
                defender_verified=False, price_source="book:test", actual=40.0, source="live")


def test_live_grader_refuses_non_holdout_weeks():
    for w in (4, 8, 9):
        with pytest.raises(LV.LiveGradeError, match="weeks 10-12"):
            LV.grade_live(pd.DataFrame([_live_leg(w)]), pbp=pd.DataFrame())


def test_live_grader_checks_freeze_before_reading_actuals(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(LV, "check_freeze", lambda w, **k: calls.append(w) or (_ for _ in ()).throw(
        FZ.FreezeError("differ")))
    with pytest.raises(FZ.FreezeError):
        LV.grade_live(pd.DataFrame([_live_leg(10)]), pbp=pd.DataFrame())
    assert calls == [10]


def test_live_grader_uses_frozen_params_and_never_refits(monkeypatch):
    from calibration import selective_edge as se
    monkeypatch.setattr(se, "fit", lambda *a, **k: pytest.fail("live grading must not refit"))
    leg = _live_leg(10)
    out = LV.grade_live(pd.DataFrame([leg]), pbp=pd.DataFrame(), context=pd.DataFrame(
        [dict(carry_n_prior=4, carry_n60=4, carry_share=0.7, usual=np.nan)]))
    assert out.label.iloc[0] in (se.STRONG_UNDER, se.STANDARD) and out.win.iloc[0] == 1.0
    assert (out.projection_ready == False).all()  # noqa: E712
