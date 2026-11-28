"""Historical leakage audit: are calibration claims backed by legitimate holdout / prospective evidence?

Reads committed artifacts only (JSON / CSV / source). Guards that no model is declared calibrated without prospective
evidence, and documents (xfail) where a "holdout" was also used for model selection or fitting.
See docs/audits/historical_leakage_audit.md.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def _j(rel):
    return json.loads((ROOT / rel).read_text())


# ------------------------------------------------------------------ guards that must keep passing
def test_no_model_is_declared_calibrated_without_prospective_coverage():
    ev = _j("evaluation/EVALUATION.json")
    kl = _j("known_flags/KNOWN_LIMITATIONS.json")
    assert ev["historical_pristine_claim"] is False
    assert kl["calibration_fitted_claim"] is False and kl["projection_ready"] is False
    if ev["games_scored"] < ev["min_coverage"]["games_scored"]:
        assert ev["status"] == "UNSCORABLE_INSUFFICIENT_COVERAGE"
        assert ev["independently_calibrated"] is False


def test_pristine_protocol_is_future_only():
    proto = _j("evaluation/PRISTINE_EVALUATION_PROTOCOL.json")
    assert proto["historical_pristine_claim"] is False


def test_selective_edge_train_eval_holdout_weeks_are_disjoint_and_ordered():
    from calibration import selective_edge as se
    tr, ev, ho = set(se.TRAIN_WEEKS), set(se.EVAL_WEEKS), set(se.HOLDOUT_WEEKS)
    assert not (tr & ev) and not (tr & ho) and not (ev & ho)
    assert max(tr) < min(ev) and max(ev) < min(ho)


def test_game_backtest_refuses_reserved_holdout_weeks():
    from calibration import backtest as bt
    assert bt.HOLDOUT_FIRST_WEEK == 10
    assert bt.main(["--weeks", "9-10", "--arms", "new_off", "--n", "10"]) == 2


def test_game_backtest_metrics_are_correct():
    import numpy as np
    from calibration import backtest as bt
    p, y = np.array([0.9, 0.2, 0.6]), np.array([1, 0, 0])
    assert abs(bt._brier(p, y) - float(np.mean((p - y) ** 2))) < 1e-12
    ll = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    assert abs(bt._logloss(p, y) - ll) < 1e-12


def test_week9_prospective_scorer_refuses_altered_lock():
    src = (ROOT / "research/evaluate_locked_week9.py").read_text()
    assert 'lock["calibration_claim"] is not False' in src and "FROZEN_PENDING_OUTCOMES" in src
    assert "brier_3way" in src and "logloss_3way" in src


# ------------------------------------------------------------------ findings (xfail = real, keep failing until fixed)
@pytest.mark.xfail(strict=True, reason=(
    "FINDING (HIGH): research/calibration_2026-11-22/fit.py:48-56 fits the board's calibration layer on 2024-25 and "
    "decides per stat whether to switch it ON using 2026 Brier (`keep = b1 < b0`). 2026 is then still reported as "
    "'holdout_2026' (dashboard/backtest_opportunity.py:220) and re-used for the W8-9 edge audit "
    "(research/model_audit_2026-11-24). 2026 is a selection set, not a clean holdout, for the board's chances."))
def test_board_calibration_enable_decision_not_made_on_reported_holdout():
    meta = _j("dashboard/calibration.json")["_meta"]
    res = _j("research/calibration_2026-11-22/results.json")["stats"]
    decided_on_2026 = any("brier_2026_calibrated" in v and "kept" in v for v in res.values())
    assert not (meta["tested"] == "2026" and decided_on_2026)


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (MED): dashboard/watch_model.json ships weights 'fitted 2022 to 2026' while its book_grade block "
    "(2026 Weeks 8-9) says 'weights from 2022-2025 only' and star_record covers 2025-2026. The shipped weights have "
    "seen the evaluation window, so those numbers cannot be reproduced from the shipped model as out-of-sample."))
def test_watch_model_shipped_weights_exclude_its_reported_eval_window():
    w = _j("dashboard/watch_model.json")
    fit_end = max(int(y) for y in re.findall(r"20\d\d", w["fitted"].split(",")[0]))
    eval_years = set(int(y) for y in re.findall(r"20\d\d", w["book_grade"]["source"].split(";")[0]))
    assert fit_end < min(eval_years)


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (MED): calibration/simv56/engines/cc_sim_v6_fix.py:10-14 fixes BIAS_REG / BIAS_WIN / K_BIAS / BIAS_OPP "
    "'tuned by wk4-7 leave-one-week-out'. Phase 4 (backtests/selective_under_alt_2026-11-12, calibration/"
    "selective_edge.py TRAIN_WEEKS=4-7) uses simv56 p_model on those same weeks, so TRAIN-period p_model is in-sample "
    "for the engine hyperparameters. OOS weeks 8-9 are not affected by this item."))
def test_engine_hyperparameters_not_tuned_on_selector_training_weeks():
    from calibration import selective_edge as se
    doc = (ROOT / "calibration/simv56/engines/cc_sim_v6_fix.py").read_text()[:4000]
    tuned = set()
    for a, b in re.findall(r"wk(\d)-(\d)", doc):
        tuned |= set(range(int(a), int(b) + 1))
    assert not (tuned & set(se.TRAIN_WEEKS))


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (MED): backtests/selective_under_alt_2026-11-12/SPEC_FROZEN.md discloses Weeks 3-8 prop outcomes and "
    "Weeks 4-9 game outcomes were already seen; the p_model there is reconstructed walk-forward (sims re-run after "
    "the games), not archived pregame predictions. Only Weeks 10-12 are clean live holdout."))
def test_phase4_p_model_is_archived_pregame_not_reconstructed():
    spec = (ROOT / "backtests/selective_under_alt_2026-11-12/SPEC_FROZEN.md").read_text()
    assert "already-seen" not in spec and "not a clean holdout" not in spec.lower()


@pytest.mark.xfail(strict=True, reason=(
    "MISSING METRIC (MED): calibration/selective_edge*.py grade selected legs by hit rate vs break-even only; the "
    "p_model probabilities themselves are never scored with Brier / log loss / reliability on W8-9 or W10-12."))
def test_selective_edge_scores_probabilities():
    txt = "".join(p.read_text() for p in (ROOT / "calibration").glob("selective_edge*.py")).lower()
    assert "brier" in txt and ("log_loss" in txt or "logloss" in txt)


@pytest.mark.xfail(strict=True, reason=(
    "MISSING TEST/EVIDENCE (MED): Lightning (sportsbook-odds-bridge experiment/nfl-lightning-opportunity-v1, draft "
    "PR #32) emits no probabilities, so no Brier / log loss / reliability exists, and its W9 'matched props' were built "
    "after the games (RESEARCH_ONLY_RETROSPECTIVE_NOT_BLIND). The only record in this repo is the Lightning report."))
def test_lightning_has_probability_calibration_evidence():
    rep = (ROOT / "data/historical/research/nfl56_status_2026-11-09/lightning/LIGHTNING_REPORT.md").read_text()
    assert "Brier, log loss and ROI for Lightning:** none" not in rep
