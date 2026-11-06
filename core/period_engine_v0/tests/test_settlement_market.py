import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pytest
from settlement import (
    PeriodScore, standalone_quarters_to_h1, settle_spread_2way,
    settle_winner_3way, settle_total_2way, identity_flags,
)
from market import (
    novig_two_way, novig_three_way, forbidden_drop_tie_renorm,
    build_mirror, edge_basis_allowed, OLD_SHRINK, american_to_implied,
)


def test_q_vs_h1_not_equal():
    q1 = PeriodScore(7, 0)
    q2 = PeriodScore(3, 7)
    h1 = standalone_quarters_to_h1(q1, q2)
    assert h1 == PeriodScore(10, 7)
    assert (q1.home, q1.away) != (h1.home, h1.away)


def test_spread_push_and_cover():
    # underdog +6.5 style signed line
    assert settle_spread_2way(-6, 6.5) == "win"   # lost by 6, +6.5 covers
    assert settle_spread_2way(-7, 7.0) == "push"
    assert settle_spread_2way(-7, 6.5) == "lose"


def test_three_way_tie():
    assert settle_winner_3way(0) == "tie"
    assert settle_winner_3way(3) == "side"
    assert settle_winner_3way(-1) == "opp"


def test_total_push():
    assert settle_total_2way(20.5, 20.5, "over") == "push"
    assert settle_total_2way(21, 20.5, "over") == "win"


def test_identity_flags():
    f = identity_flags("Q1", "H1", "spread_2way", "spread_2way", -2.5, -2.5)
    assert "PERIOD_MISMATCH" in f
    f2 = identity_flags("H1", "H1", "winner_3way", "spread_2way", None, -6.5)
    assert "SETTLEMENT_MISMATCH" in f2


def test_novig_two_way_vs_vigin():
    u, o = novig_two_way(-108, -118)
    assert abs(u + o - 1) < 1e-9
    assert abs(u - 0.4896) < 1e-3
    assert u != american_to_implied(-108)


def test_novig_three_way_sums_one():
    a, b, t = novig_three_way(-280, 310, 950)
    assert abs(a + b + t - 1) < 1e-9
    assert t > 0


def test_forbidden_drop_tie():
    with pytest.raises(RuntimeError):
        forbidden_drop_tie_renorm(-280, 310, 950)


def test_raw_preserved_and_pending_anchored():
    m = build_mirror(
        {"monte_carlo": 0.55, "bias": "UNIMPLEMENTED", "game_randomness": 0.52},
        pinnacle_two_way=(-105, -115),
        pinnacle_side_index=0,
        consensus_two_ways=[("fanduel", -105, -115), ("draftkings", -108, -112)],
        consensus_pulled_et="2026-11-05 12:35",
        proposed_blend_weight=0.3,
    )
    assert m.raw_model_p["monte_carlo"] == 0.55
    assert m.market_anchored_status == "PENDING_VALIDATION"
    assert edge_basis_allowed(m) == "raw_vs_pinnacle_only"
    assert m.pinnacle_novig_p is not None


def test_pin_missing():
    m = build_mirror({"monte_carlo": 0.4, "bias": "UNIMPLEMENTED"})
    assert "PINNACLE_MISSING" in m.flags
    assert m.pinnacle_novig_p is None


def test_divergence_audit_no_autocut():
    m = build_mirror(
        {"monte_carlo": 0.80},
        pinnacle_two_way=(-110, -110),
        divergence_pts=0.10,
    )
    assert m.divergence_audit["auto_promote_edge"] is False
    assert m.divergence_audit["auto_cut_scenario"] is False
    assert "LARGE_RAW_PIN_DIVERGENCE" in m.flags


def test_no_old_shrink_in_mirror_path():
    raw = 0.7
    m = build_mirror({"monte_carlo": raw}, pinnacle_two_way=(-110, -110))
    assert m.raw_model_p["monte_carlo"] == raw
    assert m.raw_model_p["monte_carlo"] != OLD_SHRINK(raw)


def test_consensus_requires_meta():
    m = build_mirror(
        {"monte_carlo": 0.5},
        consensus_two_ways=[("fanduel", -110, -110)],
        consensus_pulled_et="2026-11-05 12:00",
    )
    assert m.consensus_meta["books"] == ["fanduel"]
    assert m.consensus_meta["method"]
    assert m.consensus_meta["pulled_et"]


def test_signed_favorite_spread_convention():
    assert settle_spread_2way(3, -2.5) == "win"
    assert settle_spread_2way(2, -2.5) == "lose"
    assert settle_spread_2way(7, -6.5) == "win"
    assert settle_spread_2way(6, -6.5) == "lose"
    assert settle_spread_2way(6.5, -6.5) == "push"
