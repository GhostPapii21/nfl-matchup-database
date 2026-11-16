"""Fast offline tests for dashboard/coverage_model.py (no network, no data files)."""
import math

import pytest

from dashboard import coverage_model as C

SPLIT = {"man": {"targets": 30, "yards": 330, "team_targets": 150},     # 11.0 a target vs man
         "zone": {"targets": 50, "yards": 350, "team_targets": 330},    # 7.0 a target vs zone
         "mofo": {"targets": 35, "yards": 300, "team_targets": 210},
         "mofc": {"targets": 45, "yards": 380, "team_targets": 270}}
PRESSURED = {"dropbacks": 150, "sacks": 30, "attempts": 120, "completions": 54, "yards": 640}
CLEAN = {"dropbacks": 350, "sacks": 0, "attempts": 350, "completions": 250, "yards": 2700}


def test_nothing_is_applied_because_nothing_passed_the_holdout():
    assert (C.USE_COVERAGE, C.USE_PRESSURE, C.USE_TIER) == (False, False, False)
    c = C.coverage_multiplier(SPLIT, "WR", 0.45, 0.50, 80)
    p = C.pressure_multiplier(PRESSURED, CLEAN, 0.36, 0.294)
    t = C.tier_split(72.0, 5, 55.0, 0.87)
    assert c["ypt_mult"] == 1.0 and c["target_mult"] == 1.0 and c["applied"] is False
    assert p["ypt_mult"] == 1.0 and p["catch_mult"] == 1.0 and p["target_mult"] == 1.0 and p["applied"] is False
    assert t["yards_mult"] == 1.0 and t["applied"] is False
    for d in (c, p, t):
        assert d["why"].startswith("Not applied") and "holdout" in d["why"]


def test_coverage_raw_direction_and_neutral_cases():
    # better against man than the league pattern -> a man-heavy defense raises the raw number, a zone-heavy one lowers it
    hi = C.coverage_multiplier(SPLIT, "WR", 0.50, None)["raw_ypt_mult"]
    lo = C.coverage_multiplier(SPLIT, "WR", 0.15, None)["raw_ypt_mult"]
    assert hi > 1.0 > lo
    # opponent at the league rates -> exactly neutral
    same = C.coverage_multiplier(SPLIT, "WR", C.LEAGUE_MAN_RATE, C.LEAGUE_MOFO_RATE)
    assert same["raw_ypt_mult"] == pytest.approx(1.0) and same["raw_target_mult"] == pytest.approx(1.0)
    # no data and no rates -> neutral, no crash
    empty = C.coverage_multiplier({}, "TE", None, None)
    assert empty["raw_ypt_mult"] == 1.0 and empty["raw_target_mult"] == 1.0
    assert C.coverage_multiplier(None, None, None, None)["ypt_mult"] == 1.0


def test_coverage_shrinks_toward_league_split():
    # with no own data the raw number is the league effect: wide receivers gain less per target against man
    none = C.coverage_multiplier({}, "WR", 0.50, None)["raw_ypt_mult"]
    r = C.LEAGUE_SPLIT["WR"]
    expect = (0.5 * r["man"]["ypt"] + 0.5 * r["zone"]["ypt"]) / (C.LEAGUE_MAN_RATE * r["man"]["ypt"] + (1 - C.LEAGUE_MAN_RATE) * r["zone"]["ypt"])
    assert none == pytest.approx(expect, abs=1e-4) and none < 1.0
    # a heavier prior pulls his own split toward that league effect
    own = C.coverage_multiplier(SPLIT, "WR", 0.50, None, prior_targets=5)["raw_ypt_mult"]
    mid = C.coverage_multiplier(SPLIT, "WR", 0.50, None, prior_targets=40)["raw_ypt_mult"]
    far = C.coverage_multiplier(SPLIT, "WR", 0.50, None, prior_targets=4000)["raw_ypt_mult"]
    assert own > mid > far and far == pytest.approx(none, abs=5e-3)
    # running backs draw a larger share of targets against zone: a man-heavy defense lowers the raw target number
    assert C.coverage_multiplier({}, "RB", 0.50, None)["raw_target_mult"] < 1.0
    # a custom league dict is accepted
    flat = {k: {"ypt": 1.0, "share": 1.0} for k in ("man", "zone", "mofo", "mofc")}
    assert C.coverage_multiplier({}, flat, 0.6, 0.6)["raw_ypt_mult"] == pytest.approx(1.0)


def test_pressure_raw_direction_and_bounds():
    more = C.pressure_multiplier(PRESSURED, CLEAN, 0.38, 0.294)
    less = C.pressure_multiplier(PRESSURED, CLEAN, 0.22, 0.294)
    same = C.pressure_multiplier(PRESSURED, CLEAN, 0.294, 0.294)
    assert more["raw_ypt_mult"] < 1.0 < less["raw_ypt_mult"]
    assert more["raw_catch_mult"] < 1.0 < less["raw_catch_mult"]
    assert more["raw_target_mult"] < 1.0 < less["raw_target_mult"]
    assert more["expected_pressure_rate"] > same["expected_pressure_rate"] > less["expected_pressure_rate"]
    assert same["raw_ypt_mult"] == pytest.approx(1.0) and same["expected_pressure_rate"] == pytest.approx(same["usual_pressure_rate"])
    # no quarterback data -> league profile, still finite and bounded
    blank = C.pressure_multiplier({}, {}, 0.99, 0.294)
    assert 0.7 <= blank["raw_ypt_mult"] <= 1.3 and blank["expected_pressure_rate"] <= 0.70
    assert C.pressure_multiplier(None, None, None)["raw_ypt_mult"] == pytest.approx(1.0)


def test_tier_split_shrinkage():
    assert C.tier_split(80.0, 0, 50.0, 1.0)["raw_yards_mult"] == pytest.approx(1.0)            # no games: league ratio
    assert C.tier_split(80.0, 0, 50.0, 0.87)["raw_yards_mult"] == pytest.approx(0.87)
    few, many = C.tier_split(80.0, 2, 50.0)["raw_yards_mult"], C.tier_split(80.0, 30, 50.0)["raw_yards_mult"]
    assert 1.0 < few < many < 1.6
    assert C.tier_split(80.0, 8, 50.0, prior_games=8)["raw_yards_mult"] == pytest.approx((80 * 8 + 8 * 50) / 16 / 50)
    z = C.tier_split(None, None, 0)
    assert z["yards_mult"] == 1.0 and math.isfinite(z["raw_yards_mult"])


def test_switching_on_uses_the_fitted_strength(monkeypatch):
    monkeypatch.setattr(C, "USE_COVERAGE", True)
    monkeypatch.setitem(C.STRENGTH, "coverage_ypt", 0.5)
    monkeypatch.setitem(C.STRENGTH, "coverage_targets", 1.0)
    c = C.coverage_multiplier(SPLIT, "WR", 0.50, None)
    assert c["applied"] is True and c["ypt_mult"] == pytest.approx(c["raw_ypt_mult"] ** 0.5, abs=1e-3)
    assert c["target_mult"] == pytest.approx(c["raw_target_mult"], abs=1e-3)
    monkeypatch.setattr(C, "USE_TIER", True)
    monkeypatch.setitem(C.STRENGTH, "tier", 0.0)
    assert C.tier_split(80.0, 10, 50.0)["yards_mult"] == 1.0
