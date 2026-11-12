"""NFL-49 calibration harness tests (offline, fast). Research only, not validated."""
from __future__ import annotations
import pandas as pd
import pytest

from calibration import backtest
from calibration.common import make_cfg
from calibration.verify_penalty_recon import compare


def test_refuses_holdout_weeks_and_100k(capsys):
    assert backtest.main(["--weeks", "9-10", "--n", "10"]) == 2
    assert "holdout" in capsys.readouterr().out
    assert backtest.main(["--weeks", "9", "--n", "100000"]) == 2


def test_make_cfg_is_point_in_time():
    c = make_cfg("NYG", "WAS", 6, h2h="off")
    assert c["history"]["weeks_inclusive"] == [1, 2, 3, 4, 5]
    assert c["game"]["week_asof_exclusive"] == 6 and c["game"]["game_id"] == "2026_06_WAS_NYG"
    assert c["defense_interaction"]["h2h"] == "off"
    with pytest.raises(ValueError):
        make_cfg("NYG", "WAS", 1)


def test_american_to_prob():
    assert backtest.american_to_prob(-150) == pytest.approx(0.6)
    assert backtest.american_to_prob(150) == pytest.approx(0.4)


def test_close_prefers_consensus_and_keeps_blanks_unknown():
    rows = [
        dict(game_id="g1", week=6, pulled_utc="t0", book="draftkings", line_type="close", home_spread=-3, total=44, home_ml=-150, away_ml=130, source="dk"),
        dict(game_id="g1", week=6, pulled_utc="t1", book="consensus", line_type="close", home_spread=-2.5, total=43.5, home_ml=None, away_ml=None, source="nflverse"),
        dict(game_id="g2", week=9, pulled_utc="t2", book="draftkings", line_type="close", home_spread=-1, total=40, home_ml=-120, away_ml=100, source="dk"),
        dict(game_id="g2", week=9, pulled_utc="t2", book="pinnacle", line_type="close", home_spread=-2, total=41, home_ml=None, away_ml=None, source="pin"),
        dict(game_id="g3", week=9, pulled_utc="t3", book="consensus", line_type="open", home_spread=-7, total=50, home_ml=-300, away_ml=250, source="x"),
    ]
    c = backtest.close_for_games(pd.DataFrame(rows))
    assert c["g1"]["home_spread"] == -2.5 and c["g1"]["p_home_devig"] is None
    assert c["g2"]["home_spread"] == -1.5 and c["g2"]["total"] == 40.5
    assert c["g2"]["p_home_devig"] == pytest.approx((120 / 220) / (120 / 220 + 0.5))
    assert "g3" not in c  # open lines are never used as a close


def test_penalty_compare_counts_exact_matches():
    box = {("1", "A"): (5, 40), ("1", "B"): (3, 25)}
    parsed = {("1", "A"): (5, 40), ("1", "B"): (2, 20)}
    r = compare(box, parsed)
    assert r["team_games"] == 2 and r["exact_matches"] == 1 and r["box_flags"] == 8 and r["parsed_flags"] == 7
