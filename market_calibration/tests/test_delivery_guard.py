"""Delivery quarantine is diagnostic; synthetic probabilities make no accuracy claim."""
from copy import deepcopy
from dataclasses import asdict, replace

import pytest

from research.market_calibration import guard_edge_delivery
from research.market_calibration.calibration import UNFITTED, separate_outputs
from research.market_calibration.delivery_guard import ANOMALY_EDGE_PP_THRESHOLD
from research.market_calibration.quotes import MatchResult, QuoteRecord


IDENTITY = dict(game_id="synthetic-game", game_id_namespace="saved_csv_game_id",
                player=None, team=None, market="spreads", period="Q1", side="JAX",
                line=-2.5, settlement="spread_2way")
BASIS = "two_way_push_excluded"
CALIBRATION = {"status": UNFITTED, "fitted": False}
QUOTE = dict(price=-110, price_format="american", pulled_utc="2026-11-05T20:00:00Z",
             last_update_utc="2026-11-05T19:59:00Z", line_timing="pregame",
             is_in_play=False, source_file="synthetic.csv", source_sha256="a" * 64)


def deliver(raw_p=.7, market_p=.5, **changes):
    raw = {"p_win": raw_p, "market_identity": deepcopy(IDENTITY),
           "probability_basis": BASIS, "nested": {"research": [1, 2]}}
    args = dict(raw_identity=deepcopy(IDENTITY), quote_identity=deepcopy(IDENTITY),
                probability_basis=BASIS, market_probability_basis=BASIS,
                quote_provenance=deepcopy(QUOTE), calibration_status=deepcopy(CALIBRATION),
                raw_model_output=raw, consensus_requested=False)
    return guard_edge_delivery(raw_p, market_p, **(args | changes))


@pytest.mark.parametrize("raw_p,market_p", [(.899, .5), (.101, .5), (.7, .5)])
def test_subthreshold_raw_edge_can_be_surfaced_for_research(raw_p, market_p):
    out = deliver(raw_p, market_p)
    assert ANOMALY_EDGE_PP_THRESHOLD == .40
    assert out["surfaceable"] is True and out["quarantined"] is False
    assert out["reason_codes"] == []
    assert out["surfaceable_payload"]["edge"] == pytest.approx(raw_p - market_p)
    assert out["actionable_status"] == "NOLINE"
    assert out["edge_basis"] == "RAW_ONLY"


@pytest.mark.parametrize("raw_p,market_p", [(.9, .5), (.5, .9), (.7, .3),
    (.3, .7), (1., .5), (0., .5)])
def test_40_and_50pp_quarantined_both_directions_raw_preserved(raw_p, market_p):
    out = deliver(raw_p, market_p)
    assert out["status"] == "DIAGNOSTIC_ANOMALY"
    assert out["quarantined"] is True and out["surfaceable"] is False
    assert out["reason_codes"] == ["EDGE_GAP_GE_40PP"]
    assert out["surfaceable_payload"] is None
    assert out["raw_p"] == raw_p and out["market_p"] == market_p
    assert out["raw_model_output"]["p_win"] == raw_p
    assert out["edge_gap"] == pytest.approx(abs(raw_p - market_p))


@pytest.mark.parametrize("bad", [55., -110., -.01, 1.01, float("nan"),
    float("inf"), True, "0.55", None])
@pytest.mark.parametrize("field", ["raw_p", "market_p"])
def test_no_unit_conversion_or_clipping(bad, field):
    out = deliver(**{field: bad})
    assert "UNITS_CHECK" in out["reason_codes"]
    assert out["quarantined"] is True and out["edge_gap"] is None
    assert out["surfaceable_payload"] is None
    if field == "raw_p":
        value = out["raw_model_output"]["p_win"]
        assert value == bad or (isinstance(bad, float) and bad != bad and value != value)


@pytest.mark.parametrize("field,value", [("game_id", "other"), ("player", "player-1"),
    ("market", "totals"), ("period", "H1"), ("side", "BAL"), ("line", 2.5),
    ("settlement", "winner_3way"), ("team", "JAX"), ("game_id_namespace", "canonical")])
def test_every_identity_field_is_checked(field, value):
    out = deliver(raw_identity=IDENTITY | {field: value})
    assert "ID_CHECK" in out["reason_codes"] and out["quarantined"]


def test_missing_identity_and_mismatched_basis_fail_closed():
    assert "ID_CHECK" in deliver(raw_identity={})["reason_codes"]
    assert "UNITS_CHECK" in deliver(market_probability_basis="three_way_unconditional")["reason_codes"]
    assert "UNITS_CHECK" in deliver(probability_basis=None)["reason_codes"]


@pytest.mark.parametrize("changes", [{"pulled_utc": None}, {"last_update_utc": ""},
    {"last_update_utc": "2026-11-05T20:01:00Z"}, {"pulled_utc": "2026-11-05T20:00:00"},
    {"freshness_status": "STALE"}, {"is_in_play": True}, {"is_in_play": "false"},
    {"line_timing": ""}, {"price": 1.91}, {"source_file": ""}, {"source_sha256": ""}])
def test_quote_time_price_and_provenance_inspected(changes):
    out = deliver(quote_provenance=QUOTE | changes)
    assert "PRICE_TIME_CHECK" in out["reason_codes"] and out["quarantined"]


def test_declared_stale_age_and_open_close_policy():
    policy = dict(asof_utc="2026-11-05T20:10:00Z", max_age_seconds=300)
    assert "PRICE_TIME_CHECK" in deliver(quote_policy=policy)["reason_codes"]
    fresh = deliver(quote_policy=policy | {"max_age_seconds": 660})
    assert fresh["surfaceable"] and fresh["quote_checks"]["quote_age_seconds"] == 660
    assert "PRICE_TIME_CHECK" in deliver(quote_policy={"expected_line_timing": "close"})["reason_codes"]
    assert "PRICE_TIME_CHECK" in deliver(quote_policy={"max_age_seconds": 300})["reason_codes"]
    assert "PRICE_TIME_CHECK" in deliver(quote_policy={"asof_utc": "2026-11-05T19:58:00Z"})["reason_codes"]


def test_unfitted_status_preserved_without_requiring_fake_fit():
    out = deliver()
    assert out["calibration_status"] == CALIBRATION
    assert out["calibration_status"]["fitted"] is False
    for status in (None, {"status": "FITTED", "fitted": True},
                   {"status": UNFITTED, "fitted": True}):
        out = deliver(calibration_status=status)
        assert out["calibration_status"] == status
        assert "CALIBRATION_CHECK" in out["reason_codes"]


def test_all_inspections_run_even_when_threshold_trips():
    out = deliver(.9, .5, raw_identity={}, quote_provenance={}, calibration_status=None,
                  probability_basis="percent")
    assert set(out["reason_codes"]) == {"ID_CHECK", "UNITS_CHECK", "PRICE_TIME_CHECK",
                                        "CALIBRATION_CHECK", "EDGE_GAP_GE_40PP"}


@pytest.mark.parametrize("changes,reason", [
    ({"prediction_family": "MARKET_ANCHORED"}, "CALIBRATION_CHECK"),
    ({"calibration_status": "FITTED"}, "CALIBRATION_CHECK"),
    ({"fitted": True}, "CALIBRATION_CHECK"),
    ({"p_win": .9}, "UNITS_CHECK"),
    ({"probability_basis": "three_way_unconditional"}, "UNITS_CHECK"),
    ({"market_identity": IDENTITY | {"player": "another-player"}}, "ID_CHECK"),
])
def test_raw_research_payload_cannot_contradict_checked_inputs(changes, reason):
    raw = {"p_win": .7, "probability_basis": BASIS, "market_identity": deepcopy(IDENTITY)} | changes
    out = deliver(raw_model_output=raw)
    assert out["raw_model_output"] == raw
    assert reason in out["reason_codes"] and out["surfaceable_payload"] is None


def test_just_below_threshold_is_not_rounded_into_quarantine():
    out = deliver(.6999999999999998, .3)
    assert out["surfaceable"]
    assert "EDGE_GAP_GE_40PP" not in out["reason_codes"]


def test_explicit_live_policy_and_stale_policy_hook():
    quote = QUOTE | {"line_timing": "in_play", "is_in_play": True}
    assert deliver(quote_provenance=quote, quote_policy={"allow_in_play": True})["surfaceable"]
    out = deliver(quote_policy={"freshness_status": "STALE"})
    assert "PRICE_TIME_CHECK" in out["reason_codes"]


def test_player_identity_matches_for_explicit_player_markets():
    identity = IDENTITY | {"market": "player_passing_yards", "player": "synthetic-player", "line": 250.5}
    raw = {"p_win": .7, "probability_basis": BASIS, "market_identity": deepcopy(identity)}
    assert deliver(raw_identity=identity, quote_identity=identity, raw_model_output=raw)["surfaceable"]
    raw["market_identity"]["player"] = None
    out = deliver(raw_identity=raw["market_identity"], quote_identity=identity, raw_model_output=raw)
    assert "ID_CHECK" in out["reason_codes"]


def matched_fixture():
    q = QuoteRecord(game_id=IDENTITY["game_id"], book="synthetic", market="spreads",
        period="Q1", side="JAX", line=-2.5, price=-110, settlement="spread_2way", team=None,
        pulled_utc=QUOTE["pulled_utc"], last_update_utc=QUOTE["last_update_utc"],
        line_timing="pregame", is_in_play=False, snapshot_source="synthetic.csv",
        source_file="synthetic.csv", source_sha256="a" * 64, row_number=2)
    return MatchResult("MATCHED", (), {"JAX": .3, "BAL": .7},
        (q, replace(q, side="BAL", line=2.5)), ({"synthetic": True},), "JAX", BASIS)


@pytest.mark.parametrize("weight", [None, 0., .3, 1.])
def test_separation_quarantine_on_envelope_only_cannot_be_hidden_by_anchor(weight):
    raw = {"p_win": .7, "probability_basis": BASIS, "market_identity": deepcopy(IDENTITY),
           "nested": {"research": [1, 2]}}
    original = deepcopy(raw)
    matched = matched_fixture()
    before = deepcopy(asdict(matched))
    out = separate_outputs(raw, matched, raw_weight=weight, consensus_requested=False)
    assert out["delivery_guard"]["quarantined"]
    assert "EDGE_GAP_GE_40PP" in out["delivery_guard"]["reason_codes"]
    assert out["raw_model_output"] == raw == original
    assert asdict(matched) == before
    anchor = out["market_anchored_output"]
    assert anchor["status"] == "PENDING_VALIDATION"
    assert anchor["weight_provenance"] == ("ABSENT" if weight is None else "CALLER_PROPOSED_NOT_FITTED")
    assert anchor["p_win"] == (None if weight is None else pytest.approx(weight * .7 + (1 - weight) * .3))
    assert anchor["actionable_status"] == "NOLINE" and out["edge_basis"] == "RAW_ONLY"
    assert out["calibration_status"] == UNFITTED
    assert "quarantined" not in raw and "quarantined" not in anchor
    out["delivery_guard"]["raw_model_output"]["nested"]["research"].append(3)
    assert out["raw_model_output"] == original and raw == original


def test_consumer_uses_guard_without_weight_and_passes_quote_policy():
    m = matched_fixture()
    raw = {"p_win": .699, "probability_basis": BASIS, "market_identity": deepcopy(IDENTITY)}
    assert separate_outputs(raw, m, consensus_requested=False)["delivery_guard"]["surfaceable"]
    assert separate_outputs(raw, m, quote_policy={"expected_line_timing": "close"})["delivery_guard"]["quarantined"]
    raw["market_identity"]["player"] = "wrong-player"
    out = separate_outputs(raw, m, raw_weight=.3)
    assert "ID_CHECK" in out["delivery_guard"]["reason_codes"]
    assert out["market_anchored_output"]["p_win"] is None


def test_misscaled_probability_is_quarantined_in_consumer_without_blending():
    raw = {"p_win": 55., "probability_basis": BASIS, "market_identity": deepcopy(IDENTITY)}
    out = separate_outputs(raw, matched_fixture(), raw_weight=.3)
    assert "UNITS_CHECK" in out["delivery_guard"]["reason_codes"]
    assert out["raw_model_output"] == raw and out["market_anchored_output"]["p_win"] is None


def test_no_quote_is_quarantined_without_inventing_market_probability():
    out = separate_outputs({"p_win": .7}, MatchResult("NOLINE", (), None))
    assert out["delivery_guard"]["quarantined"]
    assert out["delivery_guard"]["market_p"] is None
    assert out["delivery_guard"]["surfaceable_payload"] is None


# Consensus fixtures are synthetic, not claims of held quotes or model accuracy.
def consensus_fixture(p=.5):
    members = [dict(book=book, p=p, probability_basis=BASIS,
                    market_identity=deepcopy(IDENTITY), provenance=deepcopy(QUOTE),
                    retrieved=True, imputed=False)
               for book in ('pinnacle', 'draftkings')]
    consensus = dict(consensus_p=p, probability_basis=BASIS,
                     market_identity=deepcopy(IDENTITY),
                     asof_utc='2026-11-05T20:00:00Z',
                     method='equal_weight_mean', minimum_books=2, quotes=members)
    registry = dict(game_event_alias=IDENTITY['game_id'],
                    hierarchy={'primary': ['pinnacle', 'circa'], 'sharp': ['betcris']},
                    books=[dict(book=book, retrieved=True, consensus_eligible=True,
                                status='SAVED_ONLY', usable_for_run=False,
                                artifact_sha256_by_path={'synthetic.csv': 'a' * 64})
                           for book in ('pinnacle', 'draftkings')] +
                          [dict(book=book, retrieved=False, consensus_eligible=False,
                                status='MISSING') for book in ('circa', 'betcris')])
    return consensus, registry


def consensus_deliver(raw_p=.7, single_p=.5, consensus_p=.5, **changes):
    consensus, registry = consensus_fixture(consensus_p)
    return deliver(raw_p, single_p, **(dict(consensus_requested=True,
                   consensus=consensus, source_registry=registry) | changes))


@pytest.mark.parametrize('raw_p,consensus_p,quarantined', [
    (.899, .5, False), (.101, .5, False), (.9, .5, True), (.5, .9, True),
    (.7, .3, True), (.3, .7, True), (1., .5, True), (0., .5, True),
    (.6999999999999998, .3, False)])
def test_consensus_threshold_inclusive_both_signs(raw_p, consensus_p, quarantined):
    out = consensus_deliver(raw_p, consensus_p=consensus_p)
    assert out['quarantined'] is quarantined
    assert out['consensus_status'] == 'CONSENSUS_VALID'
    assert out['comparison_target'] == 'CONSENSUS'
    assert out['consensus_p'] == consensus_p
    assert out['edge_gap'] == pytest.approx(abs(raw_p - consensus_p))
    assert ('EDGE_GAP_GE_40PP' in out['reason_codes']) is quarantined
    if not quarantined:
        assert out['surfaceable_payload']['consensus_p'] == consensus_p
        assert out['surfaceable_payload']['edge'] == pytest.approx(raw_p - consensus_p)
    assert out['actionable_status'] == 'NOLINE'
    assert out['calibration_status'] == CALIBRATION


def test_threshold_uses_consensus_and_not_the_single_quote():
    out = consensus_deliver(.9, single_p=.8, consensus_p=.5)
    assert out['quarantined'] and out['edge_gap'] == .4
    assert out['market_p'] == .8  # Preserve the single quote separately.
    out = consensus_deliver(.7, single_p=.3, consensus_p=.6)
    assert out['surfaceable'] and out['edge_gap'] == .1
    assert 'EDGE_GAP_GE_40PP' not in out['reason_codes']
    assert out['surfaceable_payload']['comparison_target'] == 'CONSENSUS'


@pytest.mark.parametrize('raw_p', [.7, .9])
def test_requested_consensus_cannot_fall_back_to_single_quote(raw_p):
    out = deliver(raw_p, .5, consensus_requested=True)
    assert out['status'] == 'DIAGNOSTIC_SINGLE_BOOK_NOT_CONSENSUS'
    assert out['consensus_status'] == 'CONSENSUS_INSUFFICIENT'
    assert not out['surfaceable'] and out['surfaceable_payload'] is None
    assert out['consensus_p'] is None and out['edge_gap'] is None
    assert 'EDGE_GAP_GE_40PP' not in out['reason_codes']
    assert out['single_book_edge_gap'] == pytest.approx(abs(raw_p - .5))


def test_default_consumer_requires_consensus_and_forwards_it_without_affecting_anchor():
    raw = dict(p_win=.7, probability_basis=BASIS, market_identity=deepcopy(IDENTITY))
    assert separate_outputs(raw, matched_fixture())['delivery_guard']['status'] == 'DIAGNOSTIC_SINGLE_BOOK_NOT_CONSENSUS'
    c, registry = consensus_fixture(.3)
    out = separate_outputs(raw, matched_fixture(), raw_weight=0., consensus=c,
                           source_registry=registry)
    assert out['delivery_guard']['status'] == 'DIAGNOSTIC_ANOMALY'
    assert out['delivery_guard']['edge_gap'] == .4
    assert out['market_anchored_output']['p_win'] == .3
    assert out['raw_model_output'] == raw


def test_direct_guard_defaults_to_consensus_and_object_cannot_be_bypassed():
    # deliver() opts out for legacy single-book regression tests only.
    assert deliver(consensus_requested=True)['surfaceable'] is False
    c, registry = consensus_fixture(.3)
    out = deliver(.7, .6, consensus=c, source_registry=registry)
    assert out['comparison_target'] == 'CONSENSUS' and out['quarantined']


@pytest.mark.parametrize('field,value', [('game_id', 'other-event'), ('market', 'totals'),
    ('period', 'H1'), ('line', -3.5), ('side', 'BAL'), ('player', 'other-player'),
    ('settlement', 'winner_3way'), ('team', 'JAX'), ('game_id_namespace', 'other')])
def test_consensus_rejects_mixed_member_identity(field, value):
    c, registry = consensus_fixture()
    c['quotes'][1]['market_identity'][field] = value
    out = consensus_deliver(consensus=c, source_registry=registry)
    assert out['quarantined'] and 'ID_CHECK' in out['reason_codes']
    assert out['consensus_status'] == 'CONSENSUS_INVALID'


@pytest.mark.parametrize('field,value', [('retrieved', False), ('retrieved', 'true'),
    ('imputed', True), ('imputed', 'false'), ('book', 'circa'), ('book', 'betcris'),
    ('book', 'unknown'), ('book', 'pinnacle')])
def test_consensus_rejects_guessed_imputed_missing_and_duplicate_books(field, value):
    c, registry = consensus_fixture()
    c['quotes'][1][field] = value
    out = consensus_deliver(consensus=c, source_registry=registry)
    assert out['quarantined'] and 'CONSENSUS_SOURCE_CHECK' in out['reason_codes']
    assert out['surfaceable_payload'] is None


@pytest.mark.parametrize('field,value', [('source_sha256', 'b' * 64),
    ('source_sha256', ''), ('source_file', 'unregistered.csv'),
    ('pulled_utc', '2026-11-05T20:00:01Z'),
    ('last_update_utc', '2026-11-05T20:01:00Z'), ('freshness_status', 'STALE'),
    ('price', 1.91), ('is_in_play', True)])
def test_consensus_inspects_every_member_provenance_and_cutoff(field, value):
    c, registry = consensus_fixture()
    c['quotes'][1]['provenance'][field] = value
    out = consensus_deliver(consensus=c, source_registry=registry)
    assert out['quarantined'] and out['consensus_status'] == 'CONSENSUS_INVALID'


@pytest.mark.parametrize('change', [dict(consensus_p=.6), dict(method='hierarchy_guess'),
    dict(probability_basis='three_way_unconditional'), dict(asof_utc=None),
    dict(minimum_books=1), dict(minimum_books=True), dict(quotes='invented'),
    dict(market_identity=IDENTITY | {'line': -3.5})])
def test_invalid_consensus_envelope_fails_closed(change):
    c, registry = consensus_fixture()
    out = consensus_deliver(consensus=c | change, source_registry=registry)
    assert out['quarantined'] and out['consensus_status'] == 'CONSENSUS_INVALID'


@pytest.mark.parametrize('change', [dict(p=55.), dict(p=float('nan')),
    dict(probability_basis='three_way_unconditional')])
def test_member_probabilities_and_bases_are_validated(change):
    c, registry = consensus_fixture()
    c['quotes'][1].update(change)
    out = consensus_deliver(consensus=c, source_registry=registry)
    assert 'UNITS_CHECK' in out['reason_codes'] and out['quarantined']


def test_minimum_is_distinct_retrieved_books_and_never_imputed():
    c, registry = consensus_fixture()
    c['quotes'] = c['quotes'][:1]
    out = consensus_deliver(consensus=c, source_registry=registry)
    assert out['status'] == 'DIAGNOSTIC_SINGLE_BOOK_NOT_CONSENSUS'
    assert out['consensus_status'] == 'CONSENSUS_INSUFFICIENT'
    assert not out['surfaceable']
    c, registry = consensus_fixture()
    c['minimum_books'] = 3
    out = consensus_deliver(consensus=c, source_registry=registry)
    assert out['status'] == 'CONSENSUS_INSUFFICIENT'
    assert out['surfaceable_payload'] is None


@pytest.mark.parametrize('registry', [None, {}, {'books': []},
    {'game_event_alias': 'another-event', 'books': []}])
def test_registry_is_required_and_scoped_to_event(registry):
    assert consensus_deliver(source_registry=registry)['quarantined']


def test_consensus_requires_same_freeze_as_delivery_policy():
    out = consensus_deliver(quote_policy={'asof_utc': '2026-11-05T20:01:00Z'})
    assert out['quarantined'] and 'PRICE_TIME_CHECK' in out['reason_codes']
    out = consensus_deliver(quote_policy={'asof_utc': '2026-11-05T20:00:00Z',
                                         'max_age_seconds': 59})
    assert out['quarantined']


def test_consensus_mean_is_recomputed_and_all_research_inputs_deep_copied():
    c, registry = consensus_fixture(.5)
    c['quotes'][0]['p'], c['quotes'][1]['p'] = .4, .6
    before = deepcopy((c, registry))
    out = consensus_deliver(consensus=c, source_registry=registry)
    assert out['surfaceable'] and out['consensus_p'] == .5
    assert (c, registry) == before
    assert out['book_hierarchy'] == registry['hierarchy']
    assert out['consensus_checks']['eligible_books'] == ['pinnacle', 'draftkings']
    out['consensus']['quotes'][0]['p'] = .9
    out['source_registry']['hierarchy']['primary'].append('invented')
    assert (c, registry) == before


def test_aggregate_cannot_hide_boundary_with_rounding_or_fake_shrink():
    c, registry = consensus_fixture(.3)
    c['consensus_p'] = .30000000000001
    out = consensus_deliver(.7, consensus=c, source_registry=registry)
    assert out['quarantined'] and 'CONSENSUS_AGGREGATE_CHECK' in out['reason_codes']
    c['quotes'][0]['p'], c['quotes'][1]['p'] = .2, .4
    c['consensus_p'] = .3
    out = consensus_deliver(.7, consensus=c, source_registry=registry)
    assert out['edge_gap'] == .4 and 'EDGE_GAP_GE_40PP' in out['reason_codes']


def test_consensus_accepts_no_single_book_argument_when_all_members_are_valid():
    out = consensus_deliver(single_p=None, quote_identity=None, quote_provenance=None,
                            market_probability_basis=None)
    assert out['surfaceable'] and out['comparison_target'] == 'CONSENSUS'
    assert out['market_p'] is None and out['consensus_p'] == .5


def test_consensus_requires_exact_line_and_retrieval_flags():
    c, registry = consensus_fixture()
    c['quotes'][0]['market_identity']['line'] += 1e-10
    assert 'ID_CHECK' in consensus_deliver(consensus=c, source_registry=registry)['reason_codes']
    c, registry = consensus_fixture()
    del c['quotes'][0]['imputed']
    assert 'CONSENSUS_SOURCE_CHECK' in consensus_deliver(consensus=c, source_registry=registry)['reason_codes']
    c, registry = consensus_fixture()
    registry['books'][0]['retrieved'] = False
    assert 'CONSENSUS_SOURCE_CHECK' in consensus_deliver(consensus=c, source_registry=registry)['reason_codes']


@pytest.mark.parametrize('consensus', [False, [], 'invented', {'quotes': [None]}])
def test_malformed_consensus_cannot_crash_or_release_guard(consensus):
    assert consensus_deliver(consensus=consensus)['quarantined']


def test_no_quotes_means_insufficient_consensus_and_noline():
    c, registry = consensus_fixture()
    c['quotes'] = []
    out = consensus_deliver(consensus=c, source_registry=registry)
    assert out['status'] == 'CONSENSUS_INSUFFICIENT'
    assert out['actionable_status'] == 'NOLINE' and out['surfaceable_payload'] is None
