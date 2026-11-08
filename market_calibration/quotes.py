"""Read the three saved CSVs only. Grades/scores are never quote features.

No network client exists here. Raw r6 game identity is bound by this explicit
source registry as a source-event alias, never a canonical ID; it is not inferred from an arbitrary filename or caller input.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from hashlib import sha256
import math
from pathlib import Path

import sys

_CORE = Path(__file__).resolve().parents[1] / "core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))
from period_engine_v0.market import novig_two_way, novig_three_way

GAME_ID = "401873037"
GAME_LABEL = "2026-11-05_JAX@BAL"
# Saved book CSVs are not in this public repository. Missing files stay NOLINE.
_SAVED = Path(__file__).resolve().parent / "saved_quotes"
SOURCES = (
    _SAVED / "odds_jaxbal_game.csv",
    _SAVED / "period_q1_q2_q3_fd_dk_cleared.csv",
    _SAVED / "period_line_grades.csv",
)
BOOKS = {"fanduel", "draftkings", "pinnacle"}
PERIODS = {"Q1", "Q2", "Q3", "Q4", "H1", "H2", "REG", "FG"}
SETTLEMENTS = {"spreads": {"spread_2way"}, "totals": {"total_2way"},
               "team_totals": {"team_total_2way"}, "h2h": {"ml_2way", "winner_3way"}}


def book_name(value):
    value = value.strip().lower()
    return {"fd": "fanduel", "dk": "draftkings", "pin": "pinnacle"}.get(value, value)


def side_name(value):
    value = value.strip().upper()
    return {"JACKSONVILLE JAGUARS": "JAX", "BALTIMORE RAVENS": "BAL",
            "DRAW": "TIE"}.get(value, value)


def utc(value: str) -> datetime:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None or dt.utcoffset() is None:
            raise ValueError("timezone required")
        return dt.astimezone(timezone.utc)
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError(f"explicit timezone timestamp required: {value!r}") from exc


def same_line(a, b):
    if a is None or b is None:
        return a is None and b is None
    try:
        return math.isfinite(a) and math.isfinite(b) and abs(a - b) < 1e-9
    except TypeError:
        return False


@dataclass(frozen=True)
class QuoteRecord:
    game_id: str
    book: str
    market: str
    period: str
    side: str
    line: float | None
    price: float
    settlement: str
    team: str | None
    pulled_utc: str
    last_update_utc: str
    line_timing: str
    is_in_play: bool
    snapshot_source: str
    source_file: str
    source_sha256: str
    row_number: int
    flags: tuple[str, ...] = ()
    raw_quote_fields: dict | None = None
    snapshot_id: str | None = None
    settlement_rule_ref: str | None = None
    ot_inclusion: str | None = None
    game_id_namespace: str = "saved_csv_game_id"

    @property
    def quote_id(self):
        return "sha256:" + sha256(f"{self.source_sha256}:{self.row_number}".encode()).hexdigest()


@dataclass(frozen=True)
class MatchRequest:
    game_id: str
    book: str
    market: str
    period: str
    side: str
    line: float | None
    settlement: str
    cutoff_utc: str
    asof_utc: str
    team: str | None = None
    pulled_utc: str | None = None
    last_update_utc: str | None = None
    line_timing: str | None = None
    is_in_play: bool = False


@dataclass(frozen=True)
class MatchResult:
    status: str
    flags: tuple[str, ...]
    probabilities: dict[str, float] | None
    quotes: tuple[QuoteRecord, ...] = ()
    provenance: tuple[dict, ...] = ()
    requested_side: str | None = None
    comparison_basis: str | None = None
    scope: str = "QUOTE_PAIR_RESEARCH_ONLY"
    actionable_status: str = "NOLINE"
    compatibility_flags: tuple[str, ...] = ("CANONICAL_CROSSWALK_UNVERIFIED", "SETTLEMENT_RULES_UNVERIFIED", "CORE_TRIAL_POPULATION_NOT_JOINED")

    @property
    def pair_id(self):
        if not self.quotes:
            return None
        material = sorted((q.quote_id, q.source_sha256) for q in self.quotes)
        import json
        return "sha256:" + sha256(json.dumps(material, separators=(",", ":")).encode()).hexdigest()

    def to_dict(self):
        return asdict(self) | {"pair_id": self.pair_id}


def load_saved_quotes() -> list[QuoteRecord]:
    result = []
    for source in SOURCES:
        digest = sha256(source.read_bytes()).hexdigest()
        with source.open(newline="") as stream:
            for row_num, row in enumerate(csv.DictReader(stream), 2):
                flags = []
                book = book_name(row["book"])
                if book not in BOOKS:
                    continue
                market = row["market"]
                period = "FG"
                for suffix in ("q1", "q2", "q3", "q4", "h1", "h2", "reg"):
                    if market.endswith("_" + suffix):
                        market, period = market[:-(len(suffix) + 1)], suffix.upper()
                        break
                if row.get("period") and row["period"] != period:
                    flags.append("PERIOD_MISMATCH")
                three_way = market == "h2h_3_way"
                if three_way:
                    market = "h2h"
                settlement = {"h2h": "winner_3way" if three_way else "ml_2way",
                    "spreads": "spread_2way", "totals": "total_2way",
                    "team_totals": "team_total_2way"}.get(market, "UNKNOWN")
                side = side_name(row.get("side") or row.get("selection_team", ""))
                if row.get("selection") and side_name(row["selection"]) != side:
                    flags.append("SIDE_MISMATCH")
                point = row.get("point", row.get("line_point", ""))
                game = row.get("game_id", GAME_ID)
                if game != GAME_ID:
                    flags.append("GAME_MISMATCH")
                result.append(QuoteRecord(
                    game, book, market, period, side, float(point) if point else None,
                    float(row.get("price", row.get("price_american", "nan"))), settlement,
                    side_name(row["player"]) if market == "team_totals" and row.get("player") else None,
                    row.get("pulled_utc", row.get("snapshot_pulled_utc", "")),
                    row.get("last_update_utc", row.get("snapshot_last_update_utc", "")),
                    row.get("line_timing", "pregame"), row.get("is_in_play_line", "0") != "0",
                    row.get("source_file") or str(source), str(source), digest, row_num, tuple(flags),
                    {k: v for k, v in row.items() if k in {"game_id", "snapshot_id", "book", "market", "period",
                        "player", "side", "selection", "selection_team", "point", "line_point", "price", "price_american",
                        "last_update_utc", "pulled_utc", "snapshot_last_update_utc", "snapshot_pulled_utc",
                        "line_timing", "is_in_play_line", "source_file"}}, row.get("snapshot_id")))
    return result


def request_flags(req):
    flags = []
    if req.game_id != GAME_ID:
        flags.append("GAME_MISMATCH")
    if book_name(req.book) not in BOOKS:
        flags.append("BOOK_MISMATCH")
    if req.period not in PERIODS:
        flags.append("PERIOD_MISMATCH")
    if req.settlement not in SETTLEMENTS.get(req.market, set()):
        flags.append("SETTLEMENT_MISMATCH")
    if req.market in {"spreads", "totals", "team_totals"}:
        if req.line is None or not same_line(req.line, req.line):
            flags.append("LINE_MISMATCH")
    elif req.line is not None:
        flags.append("LINE_MISMATCH")
    allowed = {"OVER", "UNDER"} if req.market in {"totals", "team_totals"} else {"JAX", "BAL"}
    if req.settlement == "winner_3way":
        allowed = allowed | {"TIE"}
    if side_name(req.side) not in allowed:
        flags.append("SIDE_MISMATCH")
    if (req.market == "team_totals" and req.team not in {"JAX", "BAL"}) or (
            req.market != "team_totals" and req.team is not None):
        flags.append("TEAM_MISMATCH")
    return flags


def identity_flags_for_quote(req, quote):
    flags = request_flags(req) + list(quote.flags)
    for field in ("game_id", "market", "period", "settlement", "team", "is_in_play"):
        if getattr(req, field) != getattr(quote, field):
            flags.append(field.upper() + "_MISMATCH")
    if book_name(req.book) != quote.book:
        flags.append("BOOK_MISMATCH")
    if side_name(req.side) != quote.side:
        flags.append("SIDE_MISMATCH")
    if not same_line(req.line, quote.line):
        flags.append("LINE_MISMATCH")
    if not time_eligible(req, quote):
        flags.append("TIME_MISMATCH")
    return tuple(dict.fromkeys(flags))


def time_eligible(req, quote):
    limit = min(utc(req.cutoff_utc), utc(req.asof_utc))
    pulled, updated = utc(quote.pulled_utc), utc(quote.last_update_utc)
    return (updated <= pulled <= limit
            and (req.pulled_utc is None or pulled == utc(req.pulled_utc))
            and (req.last_update_utc is None or updated == utc(req.last_update_utc))
            and (req.line_timing is None or req.line_timing == quote.line_timing))


def match_quote(quotes, req: MatchRequest) -> MatchResult:
    # Validate timestamps even when there are no candidate rows.
    for value in (req.cutoff_utc, req.asof_utc, req.pulled_utc, req.last_update_utc):
        if value is not None:
            utc(value)
    flags = request_flags(req)
    if flags:
        return MatchResult("IDENTITY_BLOCKED", tuple(flags), None)
    base = [q for q in quotes if (q.game_id, q.book, q.market, q.period, q.team, q.is_in_play) ==
            (req.game_id, book_name(req.book), req.market, req.period, req.team, req.is_in_play)]
    candidates = [q for q in base if time_eligible(req, q)]
    if not candidates:
        return MatchResult("NOLINE", ("NO_SAVED_QUOTE_AT_CUTOFF",), None)
    # Select newest coherent snapshot before looking for the line; no stale fallback.
    latest = max((utc(q.pulled_utc), utc(q.last_update_utc)) for q in candidates)
    candidates = [q for q in candidates if (utc(q.pulled_utc), utc(q.last_update_utc)) == latest]
    if any(q.settlement != req.settlement or q.flags for q in candidates):
        return MatchResult("IDENTITY_BLOCKED", ("SETTLEMENT_OR_SOURCE_IDENTITY_MISMATCH",), None)
    if req.settlement == "ml_2way" and any(q.side == "TIE" for q in candidates):
        return MatchResult("IDENTITY_BLOCKED", ("FORBIDDEN_DROP_TIE",), None)
    groups = {}
    for q in candidates:
        key = (q.snapshot_source, q.line_timing, q.snapshot_id)
        groups.setdefault(key, []).append(q)
    expected = ["JAX", "BAL", "TIE"] if req.settlement == "winner_3way" else (
        ["OVER", "UNDER"] if req.market in {"totals", "team_totals"} else ["JAX", "BAL"])
    complete = []
    provenance = []
    for key, rows in sorted(groups.items(), key=lambda item: tuple(str(v) for v in item[0])):
        selected = {}
        relevant = []
        for q in rows:
            target_line = (-req.line if q.side != side_name(req.side) else req.line) if req.market == "spreads" else req.line
            if same_line(q.line, target_line):
                relevant.append(q)
        if any(q.side not in expected for q in relevant):
            return MatchResult("IDENTITY_BLOCKED", ("UNEXPECTED_SIDE",), None)
        for q in relevant:
            if not math.isfinite(q.price) or abs(q.price) < 100:
                return MatchResult("IDENTITY_BLOCKED", ("INVALID_PRICE",), None)
            if q.side in selected and q.price != selected[q.side].price:
                return MatchResult("IDENTITY_BLOCKED", ("CONFLICTING_DUPLICATE",), None)
            selected[q.side] = q
        if set(selected) == set(expected):
            complete.append(tuple(selected[s] for s in expected))
            provenance.extend({"source_file": q.source_file, "source_sha256": q.source_sha256,
                               "row_number": q.row_number, "snapshot_source": q.snapshot_source}
                              for q in relevant)
    if not complete:
        return MatchResult("NOLINE", ("ONE_SIDED", "NO_EXACT_COHERENT_PAIR"), None)
    # Equivalent copies across saved files can confirm a quote, never average conflicts.
    pair = complete[0]
    if any(tuple(q.price for q in p) != tuple(q.price for q in pair) for p in complete[1:]):
        return MatchResult("IDENTITY_BLOCKED", ("CONFLICTING_SNAPSHOT",), None)
    probs = (novig_three_way if len(expected) == 3 else novig_two_way)(*(q.price for q in pair))
    basis = "three_way_unconditional" if len(expected) == 3 else "two_way_push_excluded"
    return MatchResult("MATCHED", (), dict(zip(expected, probs)), pair, tuple(provenance),
                       side_name(req.side), basis)
