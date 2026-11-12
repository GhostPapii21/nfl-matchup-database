"""NFL-43: penalties, returns and official overtime - conservation and rejection tests."""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
import pytest

from config_load import load_config
from semantics import (PenaltyDraw, PenaltyModel, OTTracker, build_penalty_model, enforce_penalty,
                       half_distance_move)
from simulate import attach_semantics, build_catalog, simulate_one, simulate_games
from pbp_filter import load_team_history
from state import GameState, start_ot_if_tied

PBP = ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet"
CFG = ROOT / "config/was_nyg_2026-11-12_data_only_nfl43.json"


def _cfg_w9():
    """Same semantics, as-of week 9 so the repo's bundled W1-8 PBP is sufficient offline."""
    cfg = copy.deepcopy(load_config(CFG))
    cfg["game"]["week_asof_exclusive"] = 9
    cfg["history"]["weeks_inclusive"] = list(range(1, 9))
    return cfg


# ---------- enforcement ----------
@pytest.mark.parametrize("yl,yards,side,expected", [
    (75, 10, "offense", 10),   # own 25, 10 back -> own 15
    (95, 10, "offense", 2),    # own 5: half the distance (5//2)
    (50, 15, "defense", -15),
    (6, 15, "defense", -3),    # half distance to goal
    (1, 5, "defense", 0),      # half of 1 yard rounds to no move
])
def test_half_distance(yl, yards, side, expected):
    assert half_distance_move(yards, yl, side) == expected


def test_enforcement_conserves_yards_and_never_scores_or_flips():
    rng = np.random.default_rng(7)
    for _ in range(5000):
        st = GameState.new_game(home="NYG", away="WAS")
        st.possession = "WAS"
        st.yardline_100 = int(rng.integers(1, 100))
        st.down = int(rng.integers(1, 5)); st.ydstogo = int(rng.integers(1, 25))
        side = "offense" if rng.random() < 0.5 else "defense"
        pen = PenaltyDraw(side=side, team="WAS" if side == "offense" else "NYG", yards=int(rng.choice([5, 10, 15, 30, 45])),
                          no_play=bool(rng.random() < 0.7), auto_first_down=bool(rng.random() < 0.3), penalty_type="x")
        before = st.yardline_100
        ev = enforce_penalty(st, pen, live_ball=not pen.no_play)
        assert st.possession == "WAS" and st.score_home == 0 and st.score_away == 0
        assert 1 <= st.yardline_100 <= 99
        assert st.yardline_100 - before == ev["applied_yardline_delta"]
        assert abs(ev["applied_yardline_delta"]) <= pen.yards
        assert st.penalty_yards[pen.team] == abs(ev["applied_yardline_delta"])
        if side == "defense":
            assert ev["applied_yardline_delta"] <= 0
            if pen.auto_first_down:
                assert st.down == 1
        else:
            assert ev["applied_yardline_delta"] >= 0


# ---------- penalty model (canonical log) ----------
def test_canonical_log_alias_and_asof():
    pm = build_penalty_model(["WAS", "NYG"], week_asof_exclusive=4)
    assert pm.meta["weeks_used"] == [1, 2, 3]
    for key in [("WAS", "offense"), ("WAS", "defense"), ("NYG", "offense"), ("NYG", "defense")]:
        assert 0.0 < pm.rates[key] < 0.2, key
        assert len(pm.pools[key]) > 0
    assert pm.meta["kick_play_fouls_excluded"] is True


def test_unknown_team_fails_closed():
    with pytest.raises(ValueError, match="UNSUPPORTED"):
        build_penalty_model(["XXX"], week_asof_exclusive=9)


def test_zero_rate_never_invents_penalty():
    pm = PenaltyModel(rates={}, pools={})
    rng = np.random.default_rng(0)
    assert all(pm.draw(rng, "A", "B") is None for _ in range(1000))


# ---------- overtime ----------
def _ot_state():
    st = GameState.new_game(home="H", away="A")
    st.qtr, st.game_seconds_remaining = 4, 0
    st.score_home = st.score_away = 17
    st.ot_rule = "official_2025_regular_season"
    st.ot_coin = lambda: 1  # away receives
    start_ot_if_tied(st)
    assert st.in_ot and st.possession == "A" and isinstance(st.ot_tracker, OTTracker)
    return st


def _step(st, *, score=None, pts=0, new_pos=None):
    prev = (st.possession, (st.score_home, st.score_away))
    if score:
        st.add_score(score, pts)
    if new_pos:
        st.possession = new_pos
    st.ot_tracker.update(st, *prev)


def test_ot_first_possession_fg_does_not_end_game():
    st = _ot_state()
    _step(st, score="A", pts=3, new_pos="H")
    assert not st.final, "2025 rule: opponent must get a possession"
    _step(st, new_pos="A")  # H punts, no score
    assert st.final and st.score_away > st.score_home


def test_ot_both_td_goes_sudden_death():
    st = _ot_state()
    _step(st, score="A", pts=7, new_pos="H")
    _step(st, score="H", pts=7, new_pos="A")
    assert not st.final and st.ot_tracker.phase == 2
    _step(st, score="A", pts=3, new_pos="H")
    assert st.final


def test_ot_second_team_takes_lead_ends():
    st = _ot_state()
    _step(st, score="A", pts=3, new_pos="H")
    _step(st, score="H", pts=7, new_pos="A")
    assert st.final and st.score_home > st.score_away


def test_ot_defensive_score_on_opening_possession_ends():
    st = _ot_state()
    _step(st, score="H", pts=2)  # safety
    assert st.final


def test_ot_tie_allowed_when_clock_expires():
    from simulate import _advance_period
    st = _ot_state()
    _step(st, score="A", pts=3, new_pos="H")
    _step(st, score="H", pts=3, new_pos="A")  # tied after both possessions -> sudden death
    assert not st.final and st.ot_tracker.phase == 2
    st.game_seconds_remaining = 0
    _advance_period(st, "H")
    assert st.final and st.score_home == st.score_away  # regular-season tie


# ---------- full-sim conservation ----------
@pytest.fixture(scope="module")
def sims():
    cfg = _cfg_w9()
    hist = load_team_history(PBP, teams=["NYG", "WAS"], season=2026, weeks=(1, 8))
    cat, _ = build_catalog(hist["df"], cfg, games_df=hist["games_df"])
    meta = attach_semantics(cat, cfg, PBP)
    rng = np.random.default_rng(11)
    return meta, [simulate_one(hist["df"], cat, cfg, rng) for _ in range(120)]


def test_scores_equal_score_credit_ledger(sims):
    _, states = sims
    for st in states:
        h = sum(e["pts"] for e in st.events if e.get("type") == "score_credit" and e["team"] == st.home)
        a = sum(e["pts"] for e in st.events if e.get("type") == "score_credit" and e["team"] == st.away)
        assert (h, a) == (st.score_home, st.score_away)
        ps = st.period_snapshot()
        assert ps["fg_home"] == st.score_home and ps["reg_home"] + ps["ot_home"] == st.score_home


def test_penalty_ledger_conserved(sims):
    _, states = sims
    total_pen = 0
    for st in states:
        evs = [e for e in st.events if e.get("type") == "penalty"]
        total_pen += len(evs)
        for team in (st.home, st.away):
            assert st.penalty_yards.get(team, 0) == sum(abs(e["applied_yardline_delta"]) for e in evs if e["team"] == team)
        for e in evs:
            assert e["to_yl"] - e["from_yl"] == e["applied_yardline_delta"]
            assert 1 <= e["to_yl"] <= 99
    assert total_pen > 0, "penalties path must be live when enabled"


def test_punt_net_kept_separate_from_return_td(sims):
    _, states = sims
    for st in states:
        for i, e in enumerate(st.events):
            if e.get("type") == "punt" and not e["touchback"]:
                assert e["net"] >= 1 and e["new_yl"] == int(np.clip(100 - (e["from_yl"] - e["net"]), 1, 99))


def test_return_tds_are_scored_once(sims):
    _, states = sims
    for st in states:
        for kind in ("kick_return_td", "punt_return_td", "def_return_td"):
            n_ev = sum(1 for e in st.events if e.get("type") == kind)
            assert n_ev == sum(st.special_scores[kind].values())


def test_zero_return_rate_never_invents_return_td():
    cfg = _cfg_w9()
    hist = load_team_history(PBP, teams=["NYG", "WAS"], season=2026, weeks=(1, 8))
    cat, _ = build_catalog(hist["df"], cfg, games_df=hist["games_df"])
    attach_semantics(cat, cfg, PBP)
    cat.semantics["returns"].kick_return_td_rate = 0.0
    cat.semantics["returns"].punt_return_td_rate = 0.0
    rng = np.random.default_rng(5)
    for _ in range(60):
        st = simulate_one(hist["df"], cat, cfg, rng)
        assert not st.special_scores["kick_return_td"] and not st.special_scores["punt_return_td"]


def test_legacy_config_reports_unsupported():
    cfg = load_config(ROOT / "config/dal_ind_2026-11-08_data_only.json")
    out = simulate_games(cfg, pbp_path=PBP, n=3, seed=1)
    assert out["semantics"]["status"] == "LEGACY_UNSUPPORTED"
    assert out["semantics"]["penalties"] == "UNSUPPORTED"


def test_enabled_semantics_metadata(sims):
    meta, _ = sims
    assert meta["status"] == "NFL43_SEMANTICS_V1"
    assert meta["overtime"] == "official_2025_regular_season"
    assert meta["penalties"]["weeks_used"] == list(range(1, 9))
    assert meta["returns"]["label"] == "AS_OF_LEAGUE_RATE_NOT_TEAM_FIT"
