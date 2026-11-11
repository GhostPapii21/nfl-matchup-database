"""Independent arithmetic/identity checks against all supplied saved rows."""
import json
from pathlib import Path
import pytest

from market_calibration.audit import build_saved_audit
from market_calibration.quotes import load_saved_quotes, match_quote, MatchRequest
from market_calibration.settlement import ScoreCard
from test_quotes import request


def test_persisted_saved_audit_matches_regeneration():
    artifact = Path(__file__).resolve().parents[1] / "artifacts" / "saved_quote_audit.json"
    regenerated = json.dumps(build_saved_audit(), indent=2, sort_keys=True, allow_nan=False) + "\n"
    assert artifact.read_text() == regenerated


def test_partial_scores_never_invent_q4_or_ot():
    card = ScoreCard("401873037", "BAL", "JAX", {"Q1": (3, 10), "Q2": (0, 7)})
    assert card.points("H1") == (3, 17)
    for period in ("Q3", "Q4", "REG", "FG"):
        with pytest.raises(ValueError):
            card.points(period)


def test_all_saved_rows_pair_and_grade_with_no_false_book_validation():
    report = build_saved_audit()
    assert report["quote_count"] == 132
    assert report["pair_status_counts"] == {"MATCHED": 132}
    assert report["grade_status_counts"] == {"PASS": 100, "NOT_PRESENT": 32}
    assert report["scoring_label"] == "hindsight_settlement_audit"
    assert report["book_rules_verified"] is False
    assert report["model_validation"] == "NOT_RUN"
    assert all(row["status"] == "NOLINE" for row in report["pinnacle_absence_checks"])
    assert all(row["actionable_status"] == "NOLINE" for row in report["rows"])


def test_independent_novig_all_real_pairs():
    quotes = load_saved_quotes()
    for q in quotes:
        req = MatchRequest(game_id=q.game_id, book=q.book, market=q.market, period=q.period,
            side=q.side, line=q.line, settlement=q.settlement, team=q.team,
            cutoff_utc=q.pulled_utc, asof_utc=q.pulled_utc,
            pulled_utc=q.pulled_utc, last_update_utc=q.last_update_utc, line_timing=q.line_timing)
        match = match_quote(quotes, req)
        assert match.status == "MATCHED"
        implied = {side.side: (100 / (side.price + 100) if side.price > 0
                              else -side.price / (100 - side.price)) for side in match.quotes}
        for side, value in implied.items():
            assert match.probabilities[side] == pytest.approx(value / sum(implied.values()))
        assert sum(match.probabilities.values()) == pytest.approx(1.)
        assert len({(s.book, s.game_id, s.market, s.period, s.team, s.pulled_utc,
                     s.last_update_utc, s.snapshot_source) for s in match.quotes}) == 1
        assert match.pair_id and all(q.quote_id for q in match.quotes)
        assert all(not any("result" in key or "pts" in key for key in q.raw_quote_fields)
                   for q in match.quotes)


def test_independent_all_saved_grade_arithmetic_without_settlement_helpers():
    import csv
    from market_calibration.quotes import SOURCES
    tables = {}
    for source in SOURCES:
        with source.open(newline="") as stream:
            tables[str(source)] = list(csv.DictReader(stream))
    points = {}
    for row in tables[str(SOURCES[1])]:
        points[row["period"]] = (int(row["period_bal_pts"]), int(row["period_jax_pts"]))
    points["H1"] = tuple(points["Q1"][i] + points["Q2"][i] for i in (0, 1))
    checked = 0
    for q in load_saved_quotes():
        observed = tables[q.source_file][q.row_number - 2].get("result_W_L_P")
        if not observed:
            continue
        home, away = points[q.period]
        if q.market in {"spreads", "h2h"}:
            diff = (away - home if q.side == "JAX" else home - away)
            if q.market == "spreads":
                diff += q.line
        else:
            assert q.market == "totals"
            diff = home + away - q.line
            if q.side == "UNDER":
                diff = -diff
        expected = "W" if diff > 0 else "L" if diff < 0 else "P"
        assert observed == expected, (q.source_file, q.row_number)
        checked += 1
    assert checked == 100
