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
# NFL-43 review T3: the W1-9 nflverse file the locks used (pulled 2026-11-12 11:16 AM ET), committed for reproducibility.
PBP_W9 = ROOT.parents[1] / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
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
    """Review T3: the real as-of-W10 config (history W1-9) on the committed W1-9 PBP, not an as-of-W9 stand-in."""
    cfg = copy.deepcopy(load_config(CFG))
    assert cfg["game"]["week_asof_exclusive"] == 10
    hist = load_team_history(PBP_W9, teams=["NYG", "WAS"], season=2026, weeks=(1, 9))
    cat, _ = build_catalog(hist["df"], cfg, games_df=hist["games_df"])
    meta = attach_semantics(cat, cfg, PBP_W9)
    rng = np.random.default_rng(11)
    return meta, [simulate_one(hist["df"], cat, cfg, rng) for _ in range(300)]


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
    """Review T1 (no longer tautological): each return-TD event is immediately followed by exactly one 6-point
    score_credit to the same team, and every 6-point credit is explained by exactly one TD event."""
    _, states = sims
    kinds = ("kick_return_td", "punt_return_td", "def_return_td")
    seen = 0
    for st in states:
        ev = st.events
        for i, e in enumerate(ev):
            if e.get("type") in kinds:
                seen += 1
                nxt = ev[i + 1]
                assert nxt["type"] == "score_credit" and nxt["pts"] == 6 and nxt["team"] == e["team"], (e, nxt)
        six = sum(1 for e in ev if e.get("type") == "score_credit" and e["pts"] == 6)
        tds = sum(1 for e in ev if e.get("type") in kinds + ("touchdown",))
        assert six == tds
    assert seen > 0, "300 sims with league return rates should contain at least one return TD"


def test_defensive_returns_use_league_pool(sims):
    """Review D2: defensive returns come from the league turnover pool, not the two teams' own rows."""
    meta, states = sims
    pools = meta["returns"]["def_return_pools"]
    assert pools["interception"] == {"plays": 197, "return_tds": 9, "mean_return_yards": pytest.approx(11.543, abs=1e-3)}
    assert pools["fumble_lost"]["plays"] == 157 and pools["fumble_lost"]["return_tds"] == 6
    assert meta["returns"]["def_return_mode"].startswith("LEAGUE_POOL")
    rets = [e for st in states for e in st.events if e.get("type") in ("def_return", "def_return_td")]
    assert rets and all(e["source"] == "league_pool" for e in rets)
    assert sum(1 for e in rets if e["type"] == "def_return_td") > 0  # the old two-team path produced exactly 0


def test_week9_penalty_gap_is_unknown_not_zero(sims):
    """Review D3: as-of W10, the penalty log stops at W8; W9 is reported unknown."""
    meta, _ = sims
    pen = meta["penalties"]
    assert pen["weeks_used"] == list(range(1, 9)) and pen["coverage_gap_weeks"] == [9]
    assert pen["unknown_weeks"] == [9] and "UNKNOWN" in pen["unknown_weeks_policy"]
    assert pen["source_pulled_et"].startswith("2026-11-01")


def test_zero_return_rate_never_invents_return_td():
    cfg = _cfg_w9()
    hist = load_team_history(PBP, teams=["NYG", "WAS"], season=2026, weeks=(1, 8))
    cat, _ = build_catalog(hist["df"], cfg, games_df=hist["games_df"])
    attach_semantics(cat, cfg, PBP)
    cat.semantics["returns"].kick_return_td_rate = 0.0
    cat.semantics["returns"].punt_return_td_rate = 0.0
    cat.semantics["returns"].def_return_pools = {k: np.zeros((0, 2)) for k in ("interception", "fumble_lost")}
    rng = np.random.default_rng(5)
    for _ in range(60):
        st = simulate_one(hist["df"], cat, cfg, rng)
        assert not st.special_scores["kick_return_td"] and not st.special_scores["punt_return_td"]
        assert not st.special_scores["def_return_td"]


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
    assert meta["penalties"]["week_asof_exclusive"] == 10
    assert meta["returns"]["label"] == "AS_OF_LEAGUE_RATE_NOT_TEAM_FIT"
    assert meta["returns"]["weeks"] == list(range(1, 10))


# ---------- review T2: previously untested rules ----------
def _st(pos="WAS", yl=50, down=2, togo=8, secs=600):
    st = GameState.new_game(home="NYG", away="WAS")
    st.possession, st.yardline_100, st.down, st.ydstogo, st.game_seconds_remaining = pos, yl, down, togo, secs
    return st


def test_untimed_down_after_defensive_no_play_foul_at_expiry():
    from simulate import _no_play_penalty
    st = _st(secs=3)
    _no_play_penalty(st, PenaltyDraw("defense", "NYG", 5, True, False, "Offside"))
    assert st.game_seconds_remaining == 1, "period cannot end on an accepted defensive foul"
    assert st.events[-1] == {"type": "untimed_down", "qtr": st.qtr}
    st2 = _st(secs=3)
    _no_play_penalty(st2, PenaltyDraw("offense", "WAS", 5, True, False, "False Start"))
    assert st2.game_seconds_remaining <= 0 and not any(e["type"] == "untimed_down" for e in st2.events)
    st3 = _st(secs=30)
    _no_play_penalty(st3, PenaltyDraw("defense", "NYG", 5, True, False, "Offside"))
    assert st3.game_seconds_remaining == 26 and not any(e["type"] == "untimed_down" for e in st3.events)


def test_untimed_down_is_followed_by_a_snap_in_full_sims(sims):
    _, states = sims
    for st in states:
        ev = st.events
        for i, e in enumerate(ev):
            if e.get("type") == "untimed_down":
                nxt = [x["type"] for x in ev[i + 1:] if x.get("type") in ("snap", "penalty", "end_q1", "halftime", "end_q3", "ot_start", "final", "punt", "field_goal")]
                assert nxt and nxt[0] in ("snap", "penalty", "punt", "field_goal"), nxt[:3]


@pytest.mark.parametrize("new_events,changed_pos,scored,enforced", [
    ([{"type": "snap"}], False, False, True),
    ([{"type": "snap"}, {"type": "turnover"}], True, False, False),
    ([{"type": "snap"}, {"type": "turnover_on_downs"}], True, False, False),
    ([{"type": "snap"}, {"type": "touchdown"}, {"type": "kickoff"}], True, True, False),
])
def test_live_ball_penalty_dropped_after_turnover_or_score(new_events, changed_pos, scored, enforced):
    from simulate import _live_ball_penalty
    st = _st(yl=40)
    prev_pos, prev_scores = st.possession, (st.score_home, st.score_away)
    if changed_pos:
        st.possession = "NYG"
    if scored:
        st.score_away += 7
    before = st.yardline_100
    pen = PenaltyDraw("defense", "NYG", 15, False, True, "Roughing")
    assert _live_ball_penalty(st, pen, prev_pos, prev_scores, new_events) is enforced
    if enforced:
        assert st.events[-1]["type"] == "penalty" and st.yardline_100 == before - 15
    else:
        assert st.events[-1] == {"type": "penalty_live_ball_dropped", "reason": "possession_change_or_score", "team": "NYG"}
        assert st.yardline_100 == before and st.penalty_yards.get("NYG", 0) == 0


def test_overtime_period_is_ten_minutes():
    st = _ot_state()
    assert st.qtr == 5 and st.game_seconds_remaining == 600


def test_full_sim_ot_clock_never_exceeds_ten_minutes(sims):
    _, states = sims
    for st in states:
        if st.in_ot:
            assert any(e.get("type") == "ot_start" and e.get("rule") == "official_2025_regular_season" for e in st.events)
            assert st.game_seconds_remaining <= 600


def _ret_catalog(pool_kind, rows):
    from semantics import ReturnModel
    rm = ReturnModel(0.0, 0.0, {}, def_return_pools={pool_kind: np.array(rows, dtype=float)})
    class C:  # minimal catalog for _attempt_pat / kickoff
        semantics = {"returns": rm, "penalties": None, "overtime": "official_2025_regular_season"}
    return C()


def test_end_zone_turnover_without_return_td_is_touchback():
    from simulate import _defensive_return
    st = _st(pos="NYG", yl=5)  # NYG already the defense with the ball after the turnover flip
    _defensive_return(np.random.default_rng(0), _ret_catalog("interception", [[40.0, 0.0]]), st, spot=-3, kind="interception")
    assert st.yardline_100 == 80 and st.down == 1 and st.ydstogo == 10
    assert st.score_home == st.score_away == 0
    assert st.events[-1]["type"] == "def_return" and st.events[-1]["touchback"] is True


def test_field_of_play_turnover_applies_league_return_yards():
    from simulate import _defensive_return
    st = _st(pos="NYG", yl=40)
    _defensive_return(np.random.default_rng(0), _ret_catalog("fumble_lost", [[12.0, 0.0]]), st, spot=40, kind="fumble_lost")
    assert st.yardline_100 == 60 - 12 and st.events[-1]["return_yards"] == 12


def test_kick_play_fouls_are_filtered_from_rates_and_pools(tmp_path):
    hdr = "season,week,game_id,team_penalized,side,play_type,status,no_play,auto_first_down,yards,penalty_type_norm\n"
    rows = ["2026,1,G1,AAA,offense,Kickoff,accepted,False,False,10,Holding",
            "2026,1,G1,AAA,offense,Punt,accepted,False,False,10,Holding",
            "2026,1,G1,AAA,offense,Field Goal Good,accepted,True,False,5,Delay",
            "2026,1,G1,AAA,offense,Pass,accepted,True,False,5,False Start"]
    log = tmp_path / "log.csv"
    log.write_text(hdr + "\n".join(rows) + "\n")
    games = tmp_path / "games.csv"
    games.write_text("week,game_id,team,off_plays\n1,G1,AAA,60\n1,G1,BBB,60\n")
    pm = build_penalty_model(["AAA"], week_asof_exclusive=2, log_path=log, games_path=games)
    pool = pm.pools[("AAA", "offense")]
    assert len(pool) == 1 and pool[0][3] == "False Start"
    assert pm.meta["per_team"]["AAA|offense"]["fouls"] == 1
    assert pm.rates[("AAA", "offense")] == pytest.approx(1 / (60 + 1))


# ---------- review D1/D6: the bounds figures and the sensitivity script are reproducible from the repo ----------
def test_bounds_figures_json_reproduces_from_committed_sources():
    sys.path.insert(0, str(ROOT / "bounds"))
    import derive_bounds
    assert derive_bounds.main(["--check"]) == 0


def test_bounds_doc_cites_derived_figures():
    figs = json.loads((ROOT / "bounds/bounds_figures.json").read_text())
    doc = (ROOT / "SEMANTICS_BOUNDS.md").read_text()
    pen, pbp = figs["penalty_log"]["figures"], figs["pbp"]["figures"]
    for needle in (f"{pen['accepted_flags_per_team_game']:.2f}", f"{pen['scrimmage_flags_per_team_game']:.2f}",
                   f"{pbp['ot_games']}/{pbp['games']}", f"{pbp['interception_return_tds']} of {pbp['interceptions']}",
                   "pulled", "unknown", "research only, not validated"):
        assert needle in doc, needle


def test_sensitivity_script_refuses_100k(capsys):
    sys.path.insert(0, str(ROOT / "bounds"))
    import sensitivity
    assert sensitivity.main(["--n", "100000", "--out", "/dev/null"]) == 2
