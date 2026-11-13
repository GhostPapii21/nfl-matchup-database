"""NFL-64: SD, CV, and NB kappa from saved sim outputs; frozen baseline unchanged."""
import json
from pathlib import Path

import pytest

from market_calibration.dispersion import (
    FROZEN_BASELINE, dispersion_report, frozen_normal_sd, moments, nb_kappa_mom,
    resolve_listed_side, score_dispersion_from_snapshot, series_dispersion,
)
from market_calibration.calibration import CalibrationBias


ROOT = Path(__file__).resolve().parents[2]
WAS_NYG = "snapshots/2026_10_WAS_NYG/20261112T171258Z"


def test_frozen_baseline_is_documented_and_unchanged():
    assert FROZEN_BASELINE["lognormal_cv"] == 0.55
    assert FROZEN_BASELINE["negative_binomial_kappa"]["default"] == 4.0
    assert FROZEN_BASELINE["negative_binomial_kappa"]["alternate"] == 2.5
    assert FROZEN_BASELINE["weights_changed"] is False
    assert FROZEN_BASELINE["status"] == "FROZEN_UNCHANGED"
    assert frozen_normal_sd(10) == pytest.approx(2.2)
    assert frozen_normal_sd(1) == pytest.approx(0.6)
    report = dispersion_report(repo_root=ROOT)
    assert report["weights_changed"] is False
    assert report["fitted_calibration"] is False
    assert report["independently_calibrated"] is False
    assert report["validation_claim"] == "NONE"
    assert report["frozen_baseline"] == FROZEN_BASELINE
    assert CalibrationBias.fitted is False


def test_moments_and_kappa_on_known_vector():
    stats = moments([0, 2, 4, 6])
    assert stats["n"] == 4
    assert stats["mean"] == pytest.approx(3)
    assert stats["variance"] == pytest.approx(5)
    assert stats["sd"] == pytest.approx(5 ** 0.5)
    assert stats["cv"] == pytest.approx((5 ** 0.5) / 3)
    kappa = nb_kappa_mom(3, 5)
    assert kappa["status"] == "METHOD_OF_MOMENTS"
    assert kappa["kappa"] == pytest.approx(9 / 2)
    assert nb_kappa_mom(3, 3)["status"] == "NOT_OVERDISPERSED_VS_POISSON"
    assert nb_kappa_mom(0, 2)["status"] == "NOT_APPLICABLE_NONPOSITIVE_MEAN"
    margin = series_dispersion([-2, 0, 2], market="margin", identity="fixture", apply_kappa=False)
    assert margin["kappa"]["status"].startswith("NOT_APPLICABLE")


def test_was_nyg_100k_matches_saved_summary_moments():
    pytest.importorskip("numpy")
    snapshot = score_dispersion_from_snapshot(WAS_NYG, repo_root=ROOT)
    summary = json.loads((ROOT / WAS_NYG / "summary.json").read_text())
    by_market = {(row["market"], row["identity"]): row for row in snapshot["markets"]}
    total = by_market[("total", "fg_total")]
    assert total["n"] == 100000
    assert total["mean"] == pytest.approx(summary["total"]["mean"])
    assert total["sd"] == pytest.approx(summary["total"]["sd"])
    assert total["cv"] == pytest.approx(summary["total"]["sd"] / summary["total"]["mean"])
    expected_kappa = (total["mean"] ** 2) / (total["variance"] - total["mean"])
    assert total["kappa"]["kappa"] == pytest.approx(expected_kappa)
    margin = by_market[("margin", "NYG_home_margin")]
    assert margin["mean"] == pytest.approx(summary["margin_home"]["mean"])
    assert margin["sd"] == pytest.approx(summary["margin_home"]["sd"])
    assert margin["kappa"]["kappa"] is None
    was = by_market[("team_points", "WAS_away")]
    nyg = by_market[("team_points", "NYG_home")]
    assert was["mean"] == pytest.approx(summary["points"]["WAS"])
    assert nyg["mean"] == pytest.approx(summary["points"]["NYG"])
    assert snapshot["weights_changed"] is False
    assert snapshot["fitted_calibration"] is False
    # Source path and hash are of the real saved files, not invented numbers.
    arrays = ROOT / WAS_NYG / "sim_arrays.npz"
    assert (ROOT / snapshot["source"]["path"]).resolve() == arrays.resolve()
    assert snapshot["source"]["bytes"] == arrays.stat().st_size


def test_saved_lines_push_probs_match_summary():
    pytest.importorskip("numpy")
    snapshot = score_dispersion_from_snapshot(WAS_NYG, repo_root=ROOT)
    summary = json.loads((ROOT / WAS_NYG / "summary.json").read_text())
    listed = {(row["book"], row["market"], row["line"]): row for row in snapshot["saved_lines"]}
    for row in summary["vs_market"]:
        if row["market"] not in {"total", "spread"}:
            continue
        got = listed[(row["book"], row["market"], row["line"])]
        assert got.get("flag") != "SIDE_UNRESOLVED"
        saved_push = row.get("p_model_push") or 0.0
        saved_over = row.get("p_model_cover") if row["market"] == "spread" else row.get("p_model")
        assert got["sim"]["p_push"] == pytest.approx(saved_push)
        assert got["sim"]["p_over"] == pytest.approx(saved_over)
        if row["line"] == int(row["line"]):
            assert got["sim"]["line_kind"] == "integer"
            assert got["sim"]["p_push"] > 0
        else:
            assert got["sim"]["line_kind"] == "half_or_fractional"
            assert got["sim"]["p_push"] == 0


def test_player_yard_cv_is_empirical_and_not_applied_as_a_weight():
    report = dispersion_report(repo_root=ROOT)
    players = report["player_summary"]
    assert players is not None
    assert players["n_completed"] == 500
    assert players["quotes"] == "NOLINE"
    assert players["weights_changed"] is False
    assert players["challenger_status"] == "RESEARCH_ONLY_NOT_APPLIED"
    rec = next(row for row in players["by_market"] if row["market"] == "rec_yards")
    # The number is computed from the saved file; it is not a production CV.
    assert rec["n_series"] > 0
    assert rec["cv_unweighted_mean"] is not None
    assert rec["cv_unweighted_mean"] != FROZEN_BASELINE["lognormal_cv"]
    # Frozen default stays 0.55 regardless of the empirical mean.
    assert report["frozen_baseline"]["lognormal_cv"] == 0.55
    prescott = next(row for row in players["players"] if row["identity"] == "DAL|D.Prescott" and row["market"] == "pass_yards")
    assert prescott["n"] == 500
    assert prescott["cv"] is not None
    assert prescott["frozen_lognormal_cv"] == 0.55


def test_side_resolution_does_not_confuse_new_york_teams():
    assert resolve_listed_side("Washington Commanders", "NYG", "WAS") == "away"
    assert resolve_listed_side("NYJ", "NYJ", "BUF") == "home"
    assert resolve_listed_side("New York Jets", "NYJ", "BUF") == "home"
    assert resolve_listed_side("New York Giants", "NYG", "WAS") == "home"
    assert resolve_listed_side("New York", "NYG", "NYJ") == "unresolved"
    assert resolve_listed_side("", "NYG", "WAS") == "unresolved"
