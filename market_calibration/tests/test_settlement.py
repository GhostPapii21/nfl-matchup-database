from dataclasses import replace
import pytest
from research.market_calibration.quotes import load_saved_quotes, match_quote
from research.market_calibration.settlement import ScoreCard, settle, compare_grade
from test_quotes import request


def card():
    # Small synthetic score-only fixture; no player or price estimates.
    return ScoreCard("401873037", "BAL", "JAX", {"Q1": (3, 10), "Q2": (0, 7),
                     "Q3": (0, 3), "Q4": (17, 0)}, overtime=(0, 3))


def test_h1_is_sum_and_periods_standalone():
    c = card()
    assert c.points("Q1") == (3, 10)
    assert c.points("Q2") == (0, 7)
    assert c.points("H1") == (3, 17)
    assert c.points("REG") == (20, 20)
    assert c.points("FG") == (20, 23)


def test_full_game_requires_ot_known_even_when_zero():
    c = replace(card(), overtime=None)
    with pytest.raises(ValueError, match="OT"):
        c.points("FG")
    assert c.points("REG") == (20, 20)
    assert replace(c, overtime=(0, 0)).points("FG") == (20, 20)


@pytest.mark.parametrize("market,side,line,settlement,period,expected", [
    ("spreads", "JAX", -7., "spread_2way", "Q1", "push"),
    ("spreads", "BAL", 6.5, "spread_2way", "Q1", "lose"),
    ("totals", "OVER", 13., "total_2way", "Q1", "push"),
    ("totals", "UNDER", 13.5, "total_2way", "Q1", "win"),
    ("h2h", "JAX", None, "ml_2way", "REG", "push"),
    ("h2h", "JAX", None, "ml_2way", "FG", "win"),
    ("h2h", "TIE", None, "winner_3way", "REG", "win"),
    ("h2h", "JAX", None, "winner_3way", "REG", "lose"),
    ("team_totals", "OVER", 17., "team_total_2way", "H1", "push"),
])
def test_settle_cases(market, side, line, settlement, period, expected):
    req = request(market=market, side=side, line=line, settlement=settlement, period=period,
                  team="JAX" if market == "team_totals" else None)
    assert settle(card(), req) == expected


@pytest.mark.parametrize("changes", [{"game_id": "WRONG"}, {"side": "XX"},
    {"line": None}, {"period": "OT"}, {"settlement": "total_2way"}])
def test_invalid_settlement_identity_raises(changes):
    with pytest.raises(ValueError):
        settle(card(), request(**changes))


def test_grade_comparison_requires_full_quote_identity():
    req = request()
    quote = next(q for q in load_saved_quotes() if q.book == "pinnacle" and q.market == "spreads"
                 and q.period == "Q1" and q.side == "JAX")
    assert compare_grade(card(), req, quote, "W").status == "PASS"
    for changes in ({"period": "H1"}, {"line": None}, {"side": "BAL"}, {"game_id": "X"},
                    {"book": "draftkings"}, {"settlement": "ml_2way"},
                    {"pulled_utc": "2026-11-06T00:00:00Z"}):
        assert compare_grade(card(), req, replace(quote, **changes), "W").status != "PASS"
    assert compare_grade(card(), req, quote, "L").status == "FAIL"
    assert compare_grade(card(), req, quote, "").status != "PASS"
