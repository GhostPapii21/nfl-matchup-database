"""Small saved-only diagnostic artifact. Not a model performance evaluation.

Actual scores are read only in this evidence path. H1 is recomputed from the
cleared standalone Q1 and Q2 points, never from the grades file's repeated Q1
columns. Q4/OT are not in these inputs, so they remain unknown.
"""
from collections import Counter
import csv
from hashlib import sha256
import json
from pathlib import Path

from .quotes import GAME_ID, SOURCES, MatchRequest, load_saved_quotes, match_quote
from .settlement import ScoreCard, compare_grade


def build_saved_audit():
    quotes = load_saved_quotes()
    saved = {}
    for source in SOURCES:
        with source.open(newline="") as stream:
            saved[str(source)] = list(csv.DictReader(stream))
    quarters = {}
    for row in saved[str(SOURCES[1])]:
        if row["game_id"] != GAME_ID or row["period"] not in {"Q1", "Q2", "Q3"}:
            raise ValueError("unexpected actual score identity")
        score = (int(row["period_bal_pts"]), int(row["period_jax_pts"]))
        if row["period"] in quarters and quarters[row["period"]] != score:
            raise ValueError("conflicting actual period scores")
        quarters[row["period"]] = score
    card = ScoreCard(GAME_ID, "BAL", "JAX", quarters, overtime=None)
    pair_counts, grade_counts = Counter(), Counter()
    rows = []
    for quote in quotes:
        req = MatchRequest(game_id=quote.game_id, book=quote.book, market=quote.market,
            period=quote.period, side=quote.side, line=quote.line, settlement=quote.settlement,
            team=quote.team, cutoff_utc=quote.pulled_utc, asof_utc=quote.pulled_utc,
            pulled_utc=quote.pulled_utc, last_update_utc=quote.last_update_utc,
            line_timing=quote.line_timing, is_in_play=quote.is_in_play)
        match = match_quote(quotes, req)
        pair_counts[match.status] += 1
        source_row = saved[quote.source_file][quote.row_number - 2]
        observed = source_row.get("result_W_L_P")
        comparison = compare_grade(card, req, quote, observed) if observed else None
        grade_status = comparison.status if comparison else "NOT_PRESENT"
        grade_counts[grade_status] += 1
        rows.append({"quote_id": quote.quote_id, "source_file": quote.source_file,
            "source_sha256": quote.source_sha256, "row_number": quote.row_number,
            "snapshot_source": quote.snapshot_source, "pair_id": match.pair_id,
            "book": quote.book, "market": quote.market, "period": quote.period,
            "side": quote.side, "line": quote.line, "team": quote.team,
            "pulled_utc": quote.pulled_utc, "last_update_utc": quote.last_update_utc,
            "pair_status": match.status, "pair_flags": match.flags,
            "actionable_status": match.actionable_status, "compatibility_flags": match.compatibility_flags,
            "novig_probabilities": match.probabilities, "comparison_basis": match.comparison_basis,
            "hindsight_grade_status": grade_status,
            "computed_grade": comparison.computed_grade if comparison else None})
    missing = []
    for period in ("Q2", "Q3", "Q4"):
        match = match_quote(quotes, MatchRequest(game_id=GAME_ID, book="pinnacle", market="spreads",
            period=period, side="JAX", line=-2.5, settlement="spread_2way",
            cutoff_utc="2026-11-05T20:00:00Z", asof_utc="2026-11-05T20:00:00Z"))
        # -2.5 here is only an exact-line absence probe copied from saved Q1,
        # not an assertion that a price/line exists in the missing period.
        missing.append({"book": "pinnacle", "market": "spreads", "period": period,
                        "status": match.status, "flags": match.flags,
                        "saved_row_count": sum(q.book == "pinnacle" and q.market == "spreads"
                                               and q.period == period for q in quotes)})
    return {"status": "SAVED_RESEARCH_AUDIT_ONLY", "quote_count": len(quotes),
        "game_id": GAME_ID, "game_id_namespace": "saved_csv_game_id", "canonical_crosswalk": None,
        "scoring_label": "hindsight_settlement_audit", "model_validation": "NOT_RUN",
        "book_rules_verified": False, "pair_scope": "QUOTE_PAIR_RESEARCH_ONLY",
        "known_standalone_scores_home_away": quarters, "Q4": None, "OT": None,
        "pair_status_counts": dict(pair_counts), "grade_status_counts": dict(grade_counts),
        "pinnacle_absence_checks": missing, "sources": [{"path": str(p),
            "sha256": sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size,
            "rows": len(saved[str(p)])} for p in SOURCES], "rows": rows}


def main():
    target = Path(__file__).resolve().parent / "artifacts" / "saved_quote_audit.json"
    report = build_saved_audit()
    target.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"artifact": str(target), "quote_count": report["quote_count"],
                      "pair_status_counts": report["pair_status_counts"],
                      "grade_status_counts": report["grade_status_counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
