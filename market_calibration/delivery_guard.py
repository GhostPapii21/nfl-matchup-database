"""Fail-closed research delivery checks; never calibrate or alter predictions.

Consumers must use surfaceable_payload, which is absent on quarantine. Research
diagnostics retain the original values even when they are invalid probabilities.
"""
from copy import deepcopy
from decimal import Decimal
import math
import re

from .quotes import same_line, utc

ANOMALY_EDGE_PP_THRESHOLD = 0.40
MIN_CONSENSUS_BOOKS = 2
UNFITTED = "UNIMPLEMENTED_NO_FITTED_CALIB"
PROBABILITY_BASES = {"two_way_push_excluded", "three_way_unconditional"}
IDENTITY_KEYS = ("game_id_namespace", "game_id", "market", "period", "side",
                 "settlement", "team", "line")


def valid_probability(value):
    """No percent/odds conversion, coercion, clipping, or invented shrink."""
    return (type(value) in (int, float) and 0 <= value <= 1
            and math.isfinite(value))


def identities_match(raw_identity, quote_identity):
    if not isinstance(raw_identity, dict) or not isinstance(quote_identity, dict):
        return False
    for key in IDENTITY_KEYS:
        if key not in raw_identity or key not in quote_identity:
            return False
        a, b = raw_identity[key], quote_identity[key]
        if key == "line":
            if (a is not None and type(a) not in (int, float)
                    or b is not None and type(b) not in (int, float)
                    or not same_line(a, b)):
                return False
        elif a != b or (key != "team" and (not isinstance(a, str) or not a.strip())):
            return False
    # QuoteRecord currently supports game/team markets only. Missing player means
    # no player for those markets; a supplied player must always match exactly.
    if raw_identity.get("player") != quote_identity.get("player"):
        return False
    if raw_identity["market"].startswith("player_") and not raw_identity.get("player"):
        return False
    if raw_identity["market"] in {"spreads", "totals", "team_totals"} and raw_identity["line"] is None:
        return False
    return True


def _quote_checks(provenance, policy):
    """Inspect source, American price, timing and caller-declared age policy."""
    checks = {"quote_age_seconds": None, "freshness_policy": "NOT_DECLARED"}
    if not isinstance(provenance, dict) or not isinstance(policy, dict):
        return False, checks
    try:
        price = provenance.get("price")
        if (type(price) not in (int, float) or not math.isfinite(price)
                or abs(price) < 100 or provenance.get("price_format") != "american"):
            return False, checks
        if (not provenance.get("source_file") or not isinstance(provenance.get("source_sha256"), str)
                or not re.fullmatch(r"[0-9a-fA-F]{64}", provenance["source_sha256"])):
            return False, checks
        pulled, updated = utc(provenance.get("pulled_utc")), utc(provenance.get("last_update_utc"))
        timing, in_play = provenance.get("line_timing"), provenance.get("is_in_play")
        if (updated > pulled or not isinstance(timing, str) or not timing.strip()
                or type(in_play) is not bool):
            return False, checks
        if provenance.get("freshness_status") == "STALE" or policy.get("freshness_status") == "STALE":
            return False, checks
        allow_in_play = policy.get("allow_in_play", False)
        if type(allow_in_play) is not bool or (in_play and not allow_in_play):
            return False, checks
        if timing in {"in_play", "live"} and not in_play:
            return False, checks
        if "expected_line_timing" in policy and timing != policy["expected_line_timing"]:
            return False, checks
        if "asof_utc" in policy:
            asof = utc(policy["asof_utc"])
            checks["quote_age_seconds"] = (asof - updated).total_seconds()
            if pulled > asof:
                return False, checks
        if "max_age_seconds" in policy:
            checks["freshness_policy"] = "CALLER_DECLARED_MAX_AGE"
            age_limit = policy["max_age_seconds"]
            if (type(age_limit) not in (int, float) or not math.isfinite(age_limit)
                    or age_limit < 0 or checks["quote_age_seconds"] is None
                    or checks["quote_age_seconds"] > age_limit):
                return False, checks
    except (ValueError, TypeError, OverflowError):
        return False, checks
    return True, checks


def _consensus_checks(consensus, registry, raw_identity, basis, policy):
    """Validate an equal-weight mean against retrieved registry sources.

    Hashes are matched to the supplied registry, not independently authenticated
    against quote bytes here. Licensing/promotion gates remain separate.
    """
    reasons = []
    checks = {"minimum_books": MIN_CONSENSUS_BOOKS, "eligible_books": [],
              "members": [], "recomputed_p": None}

    def fail(reason):
        if reason not in reasons:
            reasons.append(reason)

    def same_key(identity):
        return (identities_match(raw_identity, identity)
                and raw_identity["line"] == identity["line"])

    if consensus is None:
        return None, "CONSENSUS_INSUFFICIENT", ["CONSENSUS_INSUFFICIENT"], checks
    if not isinstance(consensus, dict):
        return None, "CONSENSUS_INVALID", ["CONSENSUS_SCHEMA_CHECK"], checks
    minimum = consensus.get("minimum_books")
    if type(minimum) is not int or minimum < MIN_CONSENSUS_BOOKS:
        fail("CONSENSUS_SCHEMA_CHECK")
        minimum = MIN_CONSENSUS_BOOKS
    checks["minimum_books"] = minimum
    if (consensus.get("method") != "equal_weight_mean"
            or consensus.get("imputed", False) is not False
            or consensus.get("guessed", False) is not False):
        fail("CONSENSUS_SCHEMA_CHECK")
    if not same_key(consensus.get("market_identity")):
        fail("ID_CHECK")
    if (not valid_probability(consensus.get("consensus_p"))
            or consensus.get("probability_basis") != basis):
        fail("UNITS_CHECK")
    member_policy = dict(policy) if isinstance(policy, dict) else {}
    try:
        cutoff = utc(consensus.get("asof_utc"))
        if not isinstance(policy, dict) or ("asof_utc" in policy and utc(policy["asof_utc"]) != cutoff):
            fail("PRICE_TIME_CHECK")
        member_policy["asof_utc"] = consensus["asof_utc"]
    except (ValueError, TypeError, OverflowError):
        fail("PRICE_TIME_CHECK")

    entries = registry.get("books") if isinstance(registry, dict) else None
    by_book = {}
    if (not isinstance(entries, list) or not isinstance(raw_identity, dict)
            or registry.get("game_event_alias") != raw_identity.get("game_id")):
        fail("CONSENSUS_SOURCE_CHECK")
    else:
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("book"), str):
                fail("CONSENSUS_SOURCE_CHECK")
                continue
            if entry["book"] in by_book:
                fail("CONSENSUS_SOURCE_CHECK")
            by_book[entry["book"]] = entry

    members = consensus.get("quotes")
    if not isinstance(members, list):
        fail("CONSENSUS_SCHEMA_CHECK")
        members = []
    seen, probabilities = set(), []
    for member in members:
        if not isinstance(member, dict):
            fail("CONSENSUS_SCHEMA_CHECK")
            continue
        book = member.get("book")
        source = by_book.get(book, {}) if isinstance(book, str) else {}
        provenance = member.get("provenance")
        hashes = source.get("artifact_sha256_by_path")
        source_ok = (isinstance(book, str) and bool(book) and book not in seen
                     and source.get("retrieved") is True
                     and source.get("consensus_eligible") is True
                     and source.get("status") != "MISSING"
                     and member.get("retrieved") is True
                     and member.get("imputed") is False
                     and member.get("guessed", False) is False
                     and isinstance(provenance, dict) and isinstance(hashes, dict)
                     and isinstance(provenance.get("source_file"), str)
                     and hashes.get(provenance["source_file"]) == provenance.get("source_sha256"))
        if not source_ok:
            fail("CONSENSUS_SOURCE_CHECK")
        if isinstance(book, str):
            seen.add(book)
        identity_ok = same_key(member.get("market_identity"))
        if not identity_ok:
            fail("ID_CHECK")
        units_ok = valid_probability(member.get("p")) and member.get("probability_basis") == basis
        if not units_ok:
            fail("UNITS_CHECK")
        quote_ok, quote_checks = _quote_checks(provenance, member_policy)
        if not quote_ok:
            fail("PRICE_TIME_CHECK")
        checks["members"].append({"book": deepcopy(book), "quote_checks": quote_checks,
                                  "source_ok": source_ok, "identity_ok": identity_ok,
                                  "units_ok": units_ok, "quote_ok": quote_ok})
        if source_ok and identity_ok and units_ok and quote_ok:
            checks["eligible_books"].append(book)
            probabilities.append(Decimal(str(member["p"])))
    if probabilities:
        mean = sum(probabilities) / len(probabilities)
        checks["recomputed_p"] = float(mean)
        checks["recomputed_p_decimal"] = str(mean)
        if valid_probability(consensus.get("consensus_p")) and consensus["consensus_p"] != float(mean):
            fail("CONSENSUS_AGGREGATE_CHECK")
    if reasons:
        return None, "CONSENSUS_INVALID", reasons, checks
    if len(probabilities) < minimum:
        return None, "CONSENSUS_INSUFFICIENT", ["CONSENSUS_INSUFFICIENT"], checks
    return consensus["consensus_p"], "CONSENSUS_VALID", [], checks


def guard_edge_delivery(raw_p, market_p, *, raw_identity, quote_identity,
                        probability_basis, market_probability_basis,
                        quote_provenance, calibration_status, raw_model_output,
                        quote_policy=None, consensus=None, source_registry=None,
                        consensus_requested=True):
    """Return a diagnostic envelope and, only when checked, a RAW payload.

    Consensus is required by default. Supply a consensus object and source
    registry; only a checked same-key, same-basis mean of >=2 distinct retrieved
    books can release the consensus gate. Explicit consensus_requested=False
    retains the legacy single-book research check, labelled as SINGLE_BOOK.
    Supplying a consensus always enables consensus validation.
    calibration_status must honestly declare the current unfitted implementation.
    A false fitted flag is permitted for RAW research comparison, never a fitted
    edge claim. No market-anchored probability is accepted as the raw edge basis.

    quote_policy optionally declares asof_utc, max_age_seconds (age since quote
    update, inclusive limit), expected_line_timing, allow_in_play (default False)
    and freshness_status=STALE. No current-time or arbitrary age cutoff is used.
    """
    reasons = []
    use_consensus = consensus_requested is not False or consensus is not None
    if type(consensus_requested) is not bool:
        reasons.append("CONSENSUS_SCHEMA_CHECK")
    policy = {} if quote_policy is None else quote_policy
    consensus_p, consensus_status, consensus_reasons, consensus_checks = _consensus_checks(
        consensus, source_registry, raw_identity, probability_basis, policy) if use_consensus else (
            None, "NOT_REQUESTED", [], {})
    reasons.extend(reason for reason in consensus_reasons if reason not in reasons)
    comparison_p = consensus_p if use_consensus else market_p
    comparison_basis = consensus.get("probability_basis") if isinstance(consensus, dict) else None
    if not use_consensus:
        comparison_basis = market_probability_basis
    check_single = not use_consensus or consensus is None
    if check_single and not identities_match(raw_identity, quote_identity):
        reasons.append("ID_CHECK")
    valid_units = valid_probability(raw_p) and valid_probability(comparison_p)
    if (not valid_probability(raw_p) or not isinstance(probability_basis, str)
            or probability_basis not in PROBABILITY_BASES
            or (check_single and (not valid_probability(market_p)
                                  or probability_basis != market_probability_basis))):
        reasons.append("UNITS_CHECK")
    quote_ok, quote_checks = _quote_checks(quote_provenance, policy)
    if check_single and not quote_ok:
        reasons.append("PRICE_TIME_CHECK")
    if (not isinstance(calibration_status, dict)
            or calibration_status.get("status") != UNFITTED
            or calibration_status.get("fitted") is not False):
        reasons.append("CALIBRATION_CHECK")
    # Do not let a caller label an anchored object RAW or supply a different p
    # for checking than the one in the research object being delivered.
    if not isinstance(raw_model_output, dict):
        if "CALIBRATION_CHECK" not in reasons:
            reasons.append("CALIBRATION_CHECK")
    else:
        if (raw_model_output.get("prediction_family", "RAW") != "RAW"
                or raw_model_output.get("calibration_status", UNFITTED) not in (UNFITTED, calibration_status)
                or raw_model_output.get("fitted", False) is not False):
            if "CALIBRATION_CHECK" not in reasons:
                reasons.append("CALIBRATION_CHECK")
        if valid_probability(raw_p) and raw_model_output.get("p_win") != raw_p:
            if "UNITS_CHECK" not in reasons:
                reasons.append("UNITS_CHECK")
        if raw_model_output.get("probability_basis") != probability_basis:
            if "UNITS_CHECK" not in reasons:
                reasons.append("UNITS_CHECK")
        if not identities_match(raw_model_output.get("market_identity"), raw_identity):
            if "ID_CHECK" not in reasons:
                reasons.append("ID_CHECK")
    gap = None
    edge = None
    if valid_units:
        # Decimal text comparison avoids .7 - .3 rounding below exactly 40pp.
        market_decimal = (Decimal(consensus_checks["recomputed_p_decimal"])
                          if use_consensus else Decimal(str(comparison_p)))
        difference = Decimal(str(raw_p)) - market_decimal
        gap, edge = float(abs(difference)), float(difference)
        if abs(difference) >= Decimal(str(ANOMALY_EDGE_PP_THRESHOLD)):
            reasons.append("EDGE_GAP_GE_40PP")
    quarantined = bool(reasons)
    status = "DIAGNOSTIC_ANOMALY" if quarantined else "SURFACEABLE_RESEARCH_ONLY"
    if use_consensus and consensus_status == "CONSENSUS_INSUFFICIENT":
        count = len(consensus_checks["eligible_books"])
        single_available = count == 1 or (consensus is None and quote_ok
                                          and valid_probability(market_p)
                                          and identities_match(raw_identity, quote_identity))
        status = "DIAGNOSTIC_SINGLE_BOOK_NOT_CONSENSUS" if single_available else "CONSENSUS_INSUFFICIENT"
    return {
        "status": status,
        "surfaceable": not quarantined, "quarantined": quarantined,
        "reason_codes": reasons, "raw_p": deepcopy(raw_p), "market_p": deepcopy(market_p),
        "edge_gap": gap, "anomaly_edge_pp_threshold": ANOMALY_EDGE_PP_THRESHOLD,
        "probability_basis": probability_basis, "market_probability_basis": market_probability_basis,
        "raw_model_output": deepcopy(raw_model_output),
        "raw_identity": deepcopy(raw_identity), "quote_identity": deepcopy(quote_identity),
        "quote_provenance": deepcopy(quote_provenance), "quote_policy": deepcopy(quote_policy),
        "quote_checks": quote_checks, "calibration_status": deepcopy(calibration_status),
        "comparison_target": "CONSENSUS" if use_consensus else "SINGLE_BOOK",
        "consensus_status": consensus_status, "consensus_p": deepcopy(consensus_p),
        "consensus": deepcopy(consensus), "source_registry": deepcopy(source_registry),
        "consensus_checks": consensus_checks,
        "book_hierarchy": deepcopy(source_registry.get("hierarchy")) if isinstance(source_registry, dict) else None,
        "single_book_edge_gap": float(abs(Decimal(str(raw_p)) - Decimal(str(market_p))))
            if valid_probability(raw_p) and valid_probability(market_p) else None,
        "edge_basis": "RAW_ONLY", "actionable_status": "NOLINE",
        "surfaceable_payload": None if quarantined else {
            "raw_p": raw_p, "market_p": market_p, "edge": edge,
            "consensus_p": consensus_p, "comparison_target": "CONSENSUS" if use_consensus else "SINGLE_BOOK",
            "probability_basis": probability_basis, "market_identity": deepcopy(raw_identity),
            "edge_basis": "RAW_ONLY", "actionable_status": "NOLINE"},
    }
