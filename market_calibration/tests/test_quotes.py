"""Prices below come only from saved rows; replacements are adversarial identity mutations."""
from dataclasses import replace

import pytest

from research.market_calibration.quotes import (
    GAME_ID, SOURCES, MatchRequest, load_saved_quotes, match_quote,
)
from research.period_engine_v0.market import novig_two_way, novig_three_way


@pytest.fixture(scope="module")
def quotes():
    return load_saved_quotes()


def request(**kw):
    base = dict(game_id=GAME_ID, book="pinnacle", market="spreads", period="Q1",
                side="JAX", line=-2.5, settlement="spread_2way", team=None,
                cutoff_utc="2026-11-05T20:00:00Z", asof_utc="2026-11-05T20:00:00Z")
    return MatchRequest(**(base | kw))


def test_load_only_saved_books_without_grade_leakage(quotes):
    assert len(quotes) == 132
    assert {q.book for q in quotes} == {"fanduel", "draftkings", "pinnacle"}
    assert {q.source_file for q in quotes} == {str(p) for p in SOURCES}
    assert all(q.source_sha256 and q.row_number >= 2 for q in quotes)
    assert not any(hasattr(q, "result_W_L_P") or hasattr(q, "period_jax_pts") for q in quotes)


def test_real_pin_signed_pair_and_duplicate_provenance(quotes):
    m = match_quote(quotes, request())
    assert m.status == "MATCHED"
    assert m.probabilities["JAX"] == pytest.approx(novig_two_way(-114, -101)[0])
    assert set(m.probabilities) == {"JAX", "BAL"}
    assert len(m.quotes) == 2
    assert len(m.provenance) >= 4


@pytest.mark.parametrize("period", ["Q2", "Q3", "Q4"])
def test_pin_absent_is_noline(quotes, period):
    m = match_quote(quotes, request(period=period))
    assert m.status == "NOLINE" and m.probabilities is None


@pytest.mark.parametrize("changes", [
    {"line": -3.5}, {"game_id": "OTHER"}, {"side": "OTHER"},
    {"settlement": "winner_3way"}, {"line": None}, {"team": "BAL"},
])
def test_identity_never_false_pass(quotes, changes):
    m = match_quote(quotes, request(**changes))
    assert m.status in {"IDENTITY_BLOCKED", "NOLINE"}
    assert m.flags and m.probabilities is None


def test_cutoff_and_asof_cannot_use_future_quotes(quotes):
    for field in ("cutoff_utc", "asof_utc"):
        m = match_quote(quotes, request(**{field: "2026-11-04T19:59:30Z"}))
        assert m.status == "NOLINE" and m.probabilities is None


def test_exact_timestamp_and_line_timing(quotes):
    m = match_quote(quotes, request(pulled_utc="2026-11-04T19:59:57Z",
                                  last_update_utc="2026-11-04T19:59:09Z",
                                  line_timing="pregame"))
    assert m.status == "MATCHED"
    assert match_quote(quotes, request(pulled_utc="2026-11-05T19:59:57Z")).probabilities is None
    assert match_quote(quotes, request(line_timing="pregame_post_inactives")).probabilities is None


def test_one_sided_never_invents_opposite(quotes):
    only = [q for q in quotes if q.book == "pinnacle" and q.period == "Q1"
            and q.market == "spreads" and q.side == "JAX"]
    m = match_quote(only, request())
    assert m.status == "NOLINE" and "ONE_SIDED" in m.flags
    assert m.probabilities is None


def test_no_pair_across_books_times_or_snapshots(quotes):
    pair = match_quote(quotes, request()).quotes
    for mutation in ({"book": "draftkings"}, {"last_update_utc": "2026-11-04T19:59:10Z"},
                     {"snapshot_source": "other.csv"}, {"pulled_utc": "2026-11-04T20:00:00Z"}):
        assert match_quote([pair[0], replace(pair[1], **mutation)], request()).probabilities is None


def test_conflicting_duplicate_is_blocked(quotes):
    pair = match_quote(quotes, request()).quotes
    # Another genuinely observed price deliberately assigned to the same identity.
    m = match_quote([*pair, replace(pair[0], price=-101)], request())
    assert m.status == "IDENTITY_BLOCKED" and "CONFLICTING_DUPLICATE" in m.flags


def test_team_total_different_book_lines_not_paired(quotes):
    m = match_quote(quotes, request(market="team_totals", period="FG", side="OVER",
                                   line=26.5, team="JAX", settlement="team_total_2way"))
    assert m.status == "MATCHED"
    assert m.probabilities["OVER"] == pytest.approx(novig_two_way(104, -121)[0])
    assert match_quote(quotes, request(market="team_totals", period="FG", side="OVER",
                       line=24.5, team="JAX", settlement="team_total_2way")).probabilities is None


def test_fd_post_inactives_not_available_before_pull(quotes):
    early = match_quote(quotes, request(book="FD", asof_utc="2026-11-05T23:00:00Z"))
    late = match_quote(quotes, request(book="FD", cutoff_utc="2026-11-06T00:10:00Z",
                                      asof_utc="2026-11-06T00:10:00Z"))
    assert early.status == late.status == "MATCHED"
    assert early.quotes[0].pulled_utc == "2026-11-05T17:35:33Z"
    assert late.quotes[0].pulled_utc == "2026-11-06T00:04:02Z"


def test_three_way_tie_kept_and_cannot_use_two_way(quotes):
    pair = match_quote(quotes, request(market="h2h", line=None, settlement="ml_2way")).quotes
    # Test-only settlement/side mutation of saved prices, not a claim of a saved Tie quote.
    three = [replace(q, settlement="winner_3way") for q in pair]
    three.append(replace(three[0], side="TIE", price=195))
    req = request(market="h2h", line=None, settlement="winner_3way")
    m = match_quote(three, req)
    assert m.status == "MATCHED" and set(m.probabilities) == {"JAX", "BAL", "TIE"}
    expected = novig_three_way(*(next(q.price for q in three if q.side == s)
                                  for s in ("JAX", "BAL", "TIE")))
    assert m.probabilities["TIE"] == pytest.approx(expected[2])
    assert match_quote(three[:2], req).probabilities is None
    assert match_quote(three, replace(req, settlement="ml_2way")).probabilities is None


@pytest.mark.parametrize("bad", ["", "2026-11-05 12:00:00", "nonsense"])
def test_ambiguous_time_rejected(quotes, bad):
    with pytest.raises(ValueError):
        match_quote(quotes, request(cutoff_utc=bad))
