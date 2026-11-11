from copy import deepcopy
from dataclasses import replace
import pytest
from market_calibration.calibration import (
    Provenance, CalibrationBias, validate_splits, separate_outputs, score_predictions,
)
from market_calibration.quotes import load_saved_quotes, match_quote
from test_quotes import request


def provenance(**kw):
    return Provenance(**(dict(game_id="UNSEEN", season=2026, week=9, split="train",
        inspected=False, prediction_utc="2026-11-01T10:00:00Z",
        outcome_known_utc="2026-11-02T10:00:00Z", model_id="raw-model", source="fixture",
        source_sha256="a" * 64, scoring_label="baseline",
        event_start_utc="2026-11-01T12:00:00Z") | kw))


def test_inspected_weeks_cannot_be_untouched_holdout():
    for week in range(1, 9):
        p = provenance(week=week, split="development")
        assert p.effective_split == "development_inspected"
        with pytest.raises(ValueError, match="holdout"):
            validate_splits([replace(p, split="holdout")])


def test_refuse_any_holdout_fit_and_no_fabricated_coefficients():
    model = CalibrationBias()
    with pytest.raises(ValueError, match="holdout"):
        model.fit([provenance(split="holdout")])
    result = model.fit([provenance()])
    assert result["status"] == "UNIMPLEMENTED_NO_FITTED_CALIB"
    assert result["coefficients"] is None and model.fitted is False
    assert result["provenance"][0]["source_sha256"] == "a" * 64


def test_tnf_inspected_and_cross_split_game_leakage():
    p = provenance(game_id="401873037", week=9, split="holdout")
    with pytest.raises(ValueError):
        validate_splits([p])
    p = provenance()
    with pytest.raises(ValueError, match="overlap"):
        validate_splits([p, replace(p, split="development")])


@pytest.mark.parametrize("changes", [{"source": ""}, {"source_sha256": ""},
    {"split": "validation"}, {"prediction_utc": ""}, {"model_id": ""}])
def test_missing_provenance_or_unknown_split_refused(changes):
    with pytest.raises(ValueError):
        validate_splits([provenance(**changes)])


def test_raw_anchored_distinct_deep_copies():
    raw = {"p_win": 0.7, "probability_basis": "two_way_push_excluded", "nested": {"seed": 81}}
    original = deepcopy(raw)
    matched = match_quote(load_saved_quotes(), request())
    q = next(q for q in matched.quotes if q.side == "JAX")
    raw["market_identity"] = {k: getattr(q, k) for k in ("game_id", "market", "period", "side", "line", "settlement", "team")}
    raw["market_identity"]["game_id_namespace"] = "saved_csv_game_id"
    original = deepcopy(raw)
    out = separate_outputs(raw, matched, raw_weight=0.3)
    assert raw == original and out["raw_model_output"] == raw
    assert out["market_anchored_output"]["status"] == "PENDING_VALIDATION"
    assert out["market_anchored_output"]["p_win"] == pytest.approx(
        .3 * raw["p_win"] + .7 * matched.probabilities["JAX"])
    out["raw_model_output"]["nested"]["seed"] = 99
    assert raw == original
    assert out["edge_basis"] == "RAW_ONLY"


def test_anchoring_blocked_on_identity_and_invalid_weights():
    m = match_quote(load_saved_quotes(), request(line=-3.5))
    out = separate_outputs({"p_win": .7}, m, raw_weight=.3)
    assert out["market_anchored_output"]["p_win"] is None
    for w in (-.1, 1.1, float("nan")):
        with pytest.raises(ValueError):
            separate_outputs({"p_win": .7}, m, raw_weight=w)


def test_baseline_hindsight_are_separate_and_late_baseline_refused():
    p = provenance()
    baseline = score_predictions([(.7, 1, p)], scoring_label="baseline")
    assert baseline["brier"] == pytest.approx(.09)
    assert baseline["scoring_label"] == "baseline"
    late = replace(p, prediction_utc="2026-11-03T10:00:00Z")
    with pytest.raises(ValueError, match="baseline"):
        score_predictions([(.7, 1, late)], scoring_label="baseline")
    hindsight = score_predictions([(.7, 1, replace(late, scoring_label="hindsight"))],
                                   scoring_label="hindsight")
    assert hindsight["scoring_label"] == "hindsight"
    with pytest.raises(ValueError):
        score_predictions([(.7, 1, p)], scoring_label="hindsight")
