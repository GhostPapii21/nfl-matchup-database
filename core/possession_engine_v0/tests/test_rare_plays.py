"""NFL-75: rare special-teams plays (rare_plays.py): kick-play fouls, blocked kicks, onside kicks, fakes.

Opt-in with cfg["semantics"]["rare_plays"] = "asof_league_v1"; absent / "off" reproduces the current engine bit for
bit. Still listed in nfl43.still_unsupported, so configs that enable it are refused; only capped research calls
(simulate_games research_unaccepted=("rare_plays",), n <= 20,000) can run it. Research only, not validated."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
REPO = HERE.parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
import simulate  # noqa: E402
import rare_plays as rp  # noqa: E402
from state import GameState  # noqa: E402

PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
CFG = HERE / "config/was_nyg_2026-11-12_data_only_nfl43.json"
needs_pbp = pytest.mark.skipif(not PBP.exists(), reason="committed nflverse W1-9 PBP missing")


def _cfg(mode=None):
    c = json.loads(CFG.read_text())
    c.setdefault("defense_interaction", {})["h2h"] = "off"
    if mode is not None:
        c["semantics"]["rare_plays"] = mode
    return c


# ---------------------------------------------------------------- config / gate
def test_mode_default_off_and_invalid():
    assert rp.mode_from_cfg({}) == "off"
    assert rp.mode_from_cfg({"semantics": {"rare_plays": "off"}}) == "off"
    assert rp.mode_from_cfg({"semantics": {"rare_plays": None}}) == "off"
    assert rp.mode_from_cfg({"semantics": {"rare_plays": "asof_league_v1"}}) == "asof_league_v1"
    with pytest.raises(ValueError):
        rp.mode_from_cfg({"semantics": {"rare_plays": "tuned"}})


def test_gate_lists_rare_plays_under_both_exclusions():
    from pipeline import nfl43_exclusions as ex
    flags = {"nfl43": {"still_unsupported": list(ex.CANONICAL)}}
    r = ex.check(flags, cfg={"semantics": {"rare_plays": "asof_league_v1"}})
    assert r["status"] == "REFUSED"
    assert set(r["enabled"]) == {"kick-play fouls", "blocked kicks/onside/fakes"}
    assert ex.check(flags, cfg={"semantics": {"rare_plays": "off"}})["status"] == "OK"


def test_no_committed_config_enables_rare_plays():
    for p in sorted((HERE / "config").glob("*.json")):
        assert rp.mode_from_cfg(json.loads(p.read_text())) == "off", p.name


@needs_pbp
def test_config_enabling_rare_plays_is_refused_without_research_flag():
    with pytest.raises(ValueError, match="still-unsupported"):
        simulate.simulate_games(_cfg("asof_league_v1"), pbp_path=str(PBP), n=2, seed=1)


@needs_pbp
def test_research_flag_is_capped_and_named():
    with pytest.raises(ValueError, match="capped"):
        simulate.simulate_games(_cfg("asof_league_v1"), pbp_path=str(PBP), n=simulate.RESEARCH_MAX_N + 1, seed=1,
                                research_unaccepted=("rare_plays",))
    with pytest.raises(ValueError, match="only allows"):
        simulate.simulate_games(_cfg(), pbp_path=str(PBP), n=2, seed=1, research_unaccepted=("kick-play fouls",))


@needs_pbp
def test_research_flag_does_not_lift_other_exclusions():
    c = _cfg("asof_league_v1")
    c["semantics"]["onside_kicks"] = True  # a different still_unsupported switch stays refused
    with pytest.raises(ValueError, match="still-unsupported"):
        simulate.simulate_games(c, pbp_path=str(PBP), n=2, seed=1, research_unaccepted=("rare_plays",))


# ---------------------------------------------------------------- reproduction
@needs_pbp
@pytest.mark.parametrize("mode", [None, "off"])
def test_off_reproduces_main_d817a3b_bit_for_bit(mode):
    """Golden values computed 2026-11-12 ~8:25 PM ET on main d817a3b (merge of PR #26), WAS@NYG lock config,
    h2h off, default accounting, n=60, seed 20261112 (same hash as WP12_EVIDENCE.md's golden check)."""
    o = simulate.simulate_games(_cfg(mode), pbp_path=str(PBP), n=60, seed=20261112)
    h, a = o["arrays"]["fg_home"].astype(int), o["arrays"]["fg_away"].astype(int)
    assert (int(h.sum()), int(a.sum())) == (1152, 1401)
    assert hashlib.sha256(np.stack([h, a]).tobytes()).hexdigest()[:16] == "18984268e877d4cb"
    assert o["semantics"]["rare_plays"] == "off"
    assert all(int(v.sum()) == 0 for k, v in o["special_teams_counts"].items()
               if k in ("punt_blocked", "fg_blocked", "fake", "onside_attempt", "kick_foul_presnap", "kick_foul_flagged"))


@needs_pbp
def test_off_catalog_identical_to_pre_nfl75():
    from pbp_filter import load_team_history
    c = _cfg()
    wk = c["history"]["weeks_inclusive"]
    h = load_team_history(str(PBP), teams=c["history"]["teams"], season=2026, weeks=(wk[0], wk[-1]))
    a = simulate.PlayCatalog(h["df"], min_n=5, games_df=h["games_df"], exclude_clock_mgmt=True)
    b = simulate.PlayCatalog(h["df"], min_n=5, games_df=h["games_df"], exclude_clock_mgmt=True, rare_plays=False)
    assert a.snaps.equals(b.snaps)
    assert np.array_equal(a.kickoff_starts, b.kickoff_starts)
    for k in a.specials:
        for t in a.specials[k]:
            assert a.specials[k][t].equals(b.specials[k][t])


# ---------------------------------------------------------------- classification / outcomes (toy data)
def _row(**kw):
    base = dict(game_id="g", season=2026, week=1, season_type="REG", game_half="Half1", qtr=1,
                game_seconds_remaining=3000, play_type="pass", desc="", posteam="AAA", defteam="BBB", down=1,
                ydstogo=10, yardline_100=50, timeout=0, penalty=0, punt_attempt=0, punt_blocked=0,
                field_goal_attempt=0, field_goal_result=None, extra_point_attempt=0, extra_point_result=None,
                two_point_attempt=0, kickoff_attempt=0, own_kickoff_recovery=0, return_touchdown=0,
                defensive_extra_point_conv=0, score_differential=0, posteam_score=0, posteam_score_post=0,
                defteam_score=0, defteam_score_post=0)
    base.update(kw)
    return base


def _toy():
    rows = [
        _row(play_id=1, play_type="no_play", penalty=1, down=4, ydstogo=5, yardline_100=60,
             desc="(Punt formation) PENALTY on AAA, Delay of Game, 5 yards - No Play."),
        _row(play_id=2, play_type="punt", punt_attempt=1, down=4, ydstogo=10, yardline_100=65, desc="punts 40 yards"),
        _row(play_id=3, posteam="BBB", defteam="AAA", yardline_100=70),
        _row(play_id=4, play_type="run", down=4, ydstogo=3, yardline_100=55, desc="(Punt formation) P.Punter right end for 12 yards"),
        _row(play_id=5, down=1, ydstogo=10, yardline_100=43),
        _row(play_id=6, play_type="punt", punt_attempt=1, punt_blocked=1, down=4, ydstogo=8, yardline_100=30,
             desc="punt is BLOCKED", defteam_score_post=6),
        _row(play_id=7, play_type="punt", punt_attempt=1, penalty=1, down=4, ydstogo=8, yardline_100=40,
             desc="punts. PENALTY on BBB, Holding"),
        _row(play_id=8, posteam="BBB", defteam="AAA", yardline_100=95),
        _row(play_id=9, play_type="field_goal", field_goal_attempt=1, field_goal_result="blocked", down=4,
             yardline_100=20, desc="field goal is BLOCKED", game_half="Half2"),
    ]
    return pd.DataFrame(rows)


def test_classify_toy():
    d = rp.classify(_toy())
    got = [None if (x is None or (isinstance(x, float) and np.isnan(x))) else x for x in d["_cls"].tolist()]
    assert got == ["presnap", "clean", None, "fake", None, "blocked", "flagged", None, "blocked"]
    assert d["_form"].tolist()[:2] == ["punt", "punt"] and d["_form"].iloc[8] == "field_goal"


def test_outcomes_toy_frames_scores_and_drops():
    d = rp.classify(_toy()).reset_index(drop=True)
    arr, dropped = rp._outcomes(d, np.array([0, 3, 5, 6, 8]), kicker_is_posteam=True)
    assert dropped == 1  # the blocked FG has no next play in its half
    presnap, fake, blocked, flagged = arr
    assert presnap[:7].tolist() == [0, 0, 1, 5, 4, 10, 65]  # kicking team keeps, 5 yards back (60 -> 65)
    assert presnap[7:].tolist() == [60, 4, 5, 0]            # own LOS, own down, own distance, not anchored
    assert fake[:7].tolist() == [0, 0, 1, -12, 1, 10, 43]   # kicking team gains 12, first down
    assert blocked[:3].tolist() == [0, 6, -1]               # receiving-team TD
    assert flagged[:7].tolist() == [0, 0, 0, 35, 1, 10, 95]  # receiving frame: 100 - 40 = 60 -> 95, shift +35


# ---------------------------------------------------------------- applying outcomes
class _Cat:
    def __init__(self, rpm=None):
        self.specials = {"punt": {}, "field_goal": {}, "extra_point": {}}
        self.semantics = {"rare_plays": rpm}


def _st(yl=40):
    st = GameState.new_game(home="AAA", away="BBB")
    st.possession, st.yardline_100, st.down, st.ydstogo = "AAA", yl, 4, 6
    return st


def test_apply_outcome_kicking_and_receiving_ball():
    st = _st(40)
    simulate._apply_rare_outcome(np.random.default_rng(0), _Cat(), st, "AAA", np.array([0, 0, 1, -12, 1, 10, 0, 40, 4, 6., 0]),
                                 kind="punt", cls="fake", ref_yl=40)
    assert (st.possession, st.yardline_100, st.down, st.ydstogo) == ("AAA", 28, 1, 10)
    st = _st(40)
    simulate._apply_rare_outcome(np.random.default_rng(0), _Cat(), st, "AAA", np.array([0, 0, 0, 35, 1, 10, 0.]),
                                 kind="punt", cls="flagged", ref_yl=40)
    assert (st.possession, st.yardline_100) == ("BBB", 95)


def test_apply_outcome_scores():
    st = _st(30)
    simulate._apply_rare_outcome(np.random.default_rng(0), _Cat(), st, "AAA", np.array([0, 6, -1, 0, 0, 0, -1.]),
                                 kind="punt", cls="blocked", ref_yl=30)
    assert st.score_away == 7  # 6 + sparse PAT assumed made
    assert st.events[-1]["type"] == "kickoff" and st.events[-1]["receiving"] == "AAA"
    st = _st(95)
    simulate._apply_rare_outcome(np.random.default_rng(0), _Cat(), st, "AAA", np.array([0, 2, -1, 0, 0, 0, -1.]),
                                 kind="punt", cls="blocked", ref_yl=95)
    assert st.score_away == 2 and st.events[-1]["receiving"] == "BBB"  # safety: kicking team free-kicks
    st = _st(10)
    simulate._apply_rare_outcome(np.random.default_rng(0), _Cat(), st, "AAA", np.array([3, 0, -1, 0, 0, 0, -1.]),
                                 kind="field_goal", cls="flagged", ref_yl=10)
    assert st.score_home == 3 and st.events[-1]["receiving"] == "BBB"
    assert simulate.special_teams_counts(st)["fg_made"] == 1


def test_unknown_class_never_drawn():
    m = rp.RarePlayModel(mode="asof_league_v1",
                         formation={"punt": {"p": {"presnap": None, "fake": None, "blocked": None, "flagged": None},
                                             "pools": {"presnap": np.zeros((0, 11))}}},
                         xp={}, onside={"cells": {}, "pool": np.zeros((0, 11))},
                         clean_punt_return_td_rate=None, clean_kick_return_td_rate=None)
    rng = np.random.default_rng(0)
    assert {m.draw_formation_class(rng, "punt") for _ in range(200)} == {"clean"}


def test_onside_rate_cells_and_coarsening():
    cells = {("other",): (100, 0), ("q4_trailing", 0, 0): (20, 18), ("q4_trailing", 0, 1): (4, 4),
             ("q4_trailing", 0, 2): (2, 0)}
    m = rp.RarePlayModel(mode="asof_league_v1", formation={}, xp={}, onside={"cells": cells, "pool": np.zeros((1, 11))},
                         clean_punt_return_td_rate=None, clean_kick_return_td_rate=None)
    assert m.onside_rate(2, 7, 100) == (0.0, "cell")            # not Q4: observed zero
    assert m.onside_rate(4, -3, 100) == (0.0, "cell")           # leading: observed zero
    assert m.onside_rate(4, 5, 100) == (0.9, "cell")
    assert m.onside_rate(4, 12, 100) == (22 / 26, "secs_bucket")  # n=4 < 10 -> seconds bucket
    assert m.onside_rate(4, 5, 700) == (None, "unknown")        # no kickoffs in that bucket at all: unknown


def test_onside_only_on_latest_kickoff():
    pool = np.array([[0, 0, 1, 0, 1, 10, 52, np.nan, np.nan, np.nan, 0]])  # kicking team recovers at its own 48 (yardline_100 52)
    m = rp.RarePlayModel(mode="asof_league_v1", formation={}, xp={},
                         onside={"cells": {("q4_trailing", 0, 0): (10, 10)}, "pool": pool},
                         clean_punt_return_td_rate=None, clean_kick_return_td_rate=None)
    st = GameState.new_game(home="AAA", away="BBB")
    st.qtr, st.game_seconds_remaining, st.score_home, st.score_away = 4, 60, 10, 14  # AAA trails by 4
    from state import apply_kickoff
    apply_kickoff(st, receiving="BBB", yardline_100=65)
    e = st.events[-1]
    assert simulate._rare_onside(np.random.default_rng(0), _Cat(m), st, e, m)
    assert (st.possession, st.yardline_100) == ("AAA", 52)
    assert simulate.special_teams_counts(st)["onside_recovered"] == 1
    apply_kickoff(st, receiving="BBB", yardline_100=65)
    old = st.events[-1]
    apply_kickoff(st, receiving="BBB", yardline_100=70)
    assert not simulate._rare_onside(np.random.default_rng(0), _Cat(m), st, old, m)


def test_pat_block_draw():
    m = rp.RarePlayModel(mode="asof_league_v1", formation={}, xp={"p_block": 1.0, "p_def2_given_block": 1.0},
                         onside={"cells": {}, "pool": np.zeros((0, 11))},
                         clean_punt_return_td_rate=None, clean_kick_return_td_rate=None)
    st = _st()
    simulate._attempt_pat(np.random.default_rng(0), _Cat(m), st, "AAA")
    assert (st.score_home, st.score_away) == (0, 2)
    c = simulate.special_teams_counts(st)
    assert c["pat_blocked"] == 1 and c["def_two_point"] == 1


# ---------------------------------------------------------------- catalog under rare plays
def test_rare_catalog_recodes_fakes_and_cleans_kick_pools():
    rows = []
    for i in range(6):
        rows.append(dict(game_id="g", play_id=10 * i, posteam="AAA", defteam="BBB", down=1, ydstogo=10, yardline_100=50,
                         play_type="pass", yards_gained=5, desc="pass"))
        rows.append(dict(game_id="g", play_id=10 * i + 1, posteam="AAA", defteam="BBB", down=4, ydstogo=5, yardline_100=60,
                         play_type="punt", yards_gained=0, desc="punts 45 yards", kick_distance=45, penalty=0))
    rows.append(dict(game_id="g", play_id=99, posteam="AAA", defteam="BBB", down=4, ydstogo=5, yardline_100=60,
                     play_type="run", yards_gained=12, desc="(Punt formation) P.Punter right end for 12 yards"))
    rows.append(dict(game_id="g", play_id=98, posteam="AAA", defteam="BBB", down=4, ydstogo=5, yardline_100=60,
                     play_type="punt", yards_gained=0, desc="punt is BLOCKED by X", kick_distance=0, penalty=0))
    rows.append(dict(game_id="g", play_id=97, posteam="AAA", defteam="BBB", down=4, ydstogo=5, yardline_100=60,
                     play_type="punt", yards_gained=0, desc="punts. PENALTY", kick_distance=40, penalty=1))
    df = pd.DataFrame(rows)
    old = simulate.PlayCatalog(df, min_n=1)
    new = simulate.PlayCatalog(df, min_n=1, rare_plays=True)
    assert (old.snaps["play_id"] == 99).any() and not (new.snaps["play_id"] == 99).any()
    assert len(old.specials["punt"]["AAA"]) == 8 and len(new.specials["punt"]["AAA"]) == 6
    f4_old = old.fourth_cells[("AAA",)]["play_type"].value_counts()
    f4_new = new.fourth_cells[("AAA",)]["play_type"].value_counts()
    assert f4_old.get("run", 0) == 1 and f4_new.get("run", 0) == 0 and f4_new["punt"] == f4_old["punt"] + 1


def test_kickoff_start_pool_drops_onside_only_when_asked():
    rows = [dict(game_id="g", play_id=1, play_type="kickoff", posteam="BBB", yardline_100=35, kickoff_attempt=1,
                 desc="kicks 65 yards"),
            dict(game_id="g", play_id=2, play_type="run", posteam="BBB", yardline_100=65, kickoff_attempt=0, desc=""),
            dict(game_id="g", play_id=3, play_type="kickoff", posteam="AAA", yardline_100=35, kickoff_attempt=1,
                 desc="kicks onside 10 yards"),
            dict(game_id="g", play_id=4, play_type="run", posteam="AAA", yardline_100=55, kickoff_attempt=0, desc="")]
    df = pd.DataFrame(rows)
    assert simulate.kickoff_start_yardlines(df).tolist() == [65, 55]
    assert simulate.kickoff_start_yardlines(df, exclude_onside=True).tolist() == [65]


# ---------------------------------------------------------------- data model (real PBP)
@needs_pbp
def test_model_provenance_point_in_time_and_counts():
    m = rp.build_rare_play_model(PBP, season=2026, week_asof_exclusive=5)
    src = m.meta["sources"]
    assert src[0]["weeks"] == [1, 2, 3, 4] and len(src[0]["sha256"]) == 64 and src[0]["pulled_et"]
    assert {s["season"] for s in src[1:]} == {2018, 2020, 2022, 2024}
    assert all(s.get("sha256") and s.get("rows", 0) > 0 for s in src[1:])
    f = m.meta["formation"]["punt"]
    assert sum(f["n"].values()) == f["formation_rows"] > 8000
    assert 0 < f["rate"]["blocked"] < 0.02 and 0 < f["rate"]["fake"] < 0.03 and 0.03 < f["rate"]["flagged"] < 0.2
    assert m.meta["onside"]["era"].startswith("2024")
    assert m.onside["cells"][("other",)][1] == 0  # no onside kick outside Q4-trailing in the 2024+ data
    with pytest.raises(ValueError):
        rp.build_rare_play_model(PBP, season=2026, week_asof_exclusive=5, prior_seasons=(2026,))


@needs_pbp
def test_penalty_model_kick_formation_exclusion_only_when_asked():
    from semantics import build_penalty_model
    a = build_penalty_model(["NYG", "WAS"], week_asof_exclusive=10, season=2026)
    b = build_penalty_model(["NYG", "WAS"], week_asof_exclusive=10, season=2026, exclude_kick_formation=True)
    assert "kick_formation_presnap_excluded" not in a.meta and b.meta["kick_formation_presnap_excluded"] > 0
    assert all(b.rates[k] <= a.rates[k] for k in a.rates)


@needs_pbp
def test_rare_semantics_need_rare_catalog():
    from pbp_filter import load_team_history
    c = _cfg()
    wk = c["history"]["weeks_inclusive"]
    h = load_team_history(str(PBP), teams=c["history"]["teams"], season=2026, weeks=(wk[0], wk[-1]))
    cat, _ = simulate.build_catalog(h["df"], c, games_df=h["games_df"])  # built with rare off
    with pytest.raises(ValueError, match="rare_plays=True"):
        simulate.attach_semantics(cat, _cfg("asof_league_v1"), str(PBP), research_unaccepted=("rare_plays",),
                                  research_n=2)


@needs_pbp
def test_rare_research_smoke_runs_and_labels():
    o = simulate.simulate_games(_cfg("asof_league_v1"), pbp_path=str(PBP), n=40, seed=3,
                                research_unaccepted=("rare_plays",))
    assert o["n_completed"] == 40
    meta = o["semantics"]["rare_plays"]
    assert meta["gate"].startswith("UNACCEPTED_RESEARCH_ONLY") and meta["mode"] == "asof_league_v1"
    assert o["effects_provenance"]["rare_plays_catalog"] is True
    tot = o["arrays"]["fg_home"] + o["arrays"]["fg_away"]
    assert 15 < float(tot.mean()) < 80
    sc = o["special_teams_counts"]
    assert int(sc["kick_foul_flagged"].sum() + sc["kick_foul_presnap"].sum()) > 0


# ---------------------------------------------------------------- review pass 1 fixes (live semantics, bands, cap)
def _pres(shift, next_down=4, row_togo=10.0, row_down=4):
    return np.array([0, 0, 1, shift, next_down, 10, 0, 50, row_down, row_togo, 0], dtype=float)


@pytest.mark.parametrize("shift,live_togo,want", [
    (5, 6, (45, 4, 11)),     # offensive delay of game: 5 back, 4th and 11, kick decision again
    (-5, 6, (35, 4, 1)),     # defensive offside short of the live line to gain: 4th and 1
    (-5, 3, (35, 1, 10)),    # defensive offside reaching the live line to gain: first down
])
def test_presnap_uses_live_down_and_distance(shift, live_togo, want):
    st = _st(40); st.ydstogo = live_togo
    simulate._apply_presnap(st, _pres(shift), 11, "punt", "band5")
    assert (st.yardline_100, st.down, st.ydstogo) == want
    assert st.game_seconds_remaining == 900 - 11


def test_presnap_auto_first_down_row():
    st = _st(40); st.ydstogo = 8
    simulate._apply_presnap(st, _pres(-5, next_down=1, row_togo=10.0), 11, "punt", "band5")  # e.g. roughing-type
    assert (st.down, st.ydstogo) == (1, 10)


def _fake_row(yards, **kw):
    r = dict(play_type="run", yards_gained=yards, interception=0, fumble_lost=0, sack=0, complete_pass=0,
             yardline_100=60, down=4, ydstogo=5)
    r.update(kw)
    return pd.Series(r)


def test_fake_runs_through_live_snap_mechanics():
    st = _st(60); st.ydstogo = 5
    simulate._apply_fake(np.random.default_rng(0), _Cat(), st, _fake_row(12), "punt", "band5")
    assert (st.possession, st.yardline_100, st.down) == ("AAA", 48, 1)
    st = _st(60); st.ydstogo = 15
    simulate._apply_fake(np.random.default_rng(0), _Cat(), st, _fake_row(12), "punt", "band5")
    assert (st.possession, st.yardline_100) == ("BBB", 52)  # short of the live line to gain: turnover on downs
    st = _st(10); st.ydstogo = 5
    simulate._apply_fake(np.random.default_rng(0), _Cat(), st, _fake_row(12), "field_goal", "band5")
    assert st.score_home >= 6 and simulate.special_teams_counts(st)["fake_kicking_td"] == 1
    assert not any(e.get("type") == "snap" and e.get("rare_fake") is None for e in st.events)


def test_outcome_draw_prefers_nearby_line_of_scrimmage():
    far = np.array([[0, 0, 0, 57, 1, 10, 90, 67, 4, 10., 0]] * 10)
    near = np.array([[0, 0, 0, 20, 1, 10, 80, 41, 4, 10., 0]] * 6)
    m = rp.RarePlayModel(mode="asof_league_v1", formation={"punt": {"p": {}, "pools": {"flagged": np.vstack([far, near])}}},
                         xp={}, onside={"cells": {}, "pool": np.zeros((0, 11))},
                         clean_punt_return_td_rate=None, clean_kick_return_td_rate=None)
    rng = np.random.default_rng(0)
    rows = [m.draw_outcome(rng, "punt", "flagged", 40) for _ in range(50)]
    assert all(r[7] == 41 and tag == "band1" for r, tag in rows)
    exact = np.array([[0, 0, 0, 30, 1, 10, 90, 40, 4, 10., 0]] * 5)
    m.formation["punt"]["pools"]["flagged"] = np.vstack([far, near, exact])
    assert all(m.draw_outcome(rng, "punt", "flagged", 40)[1] == "band0" for _ in range(20))


def test_presnap_first_down_row_is_not_auto_first_down():
    """Review pass 2: a 1st-and-10 row that stays 1st down after a 5-yard defensive foul is NOT an automatic first
    down; applied at live 4th-and-8 it gives 4th-and-3."""
    st = _st(40); st.ydstogo = 8
    simulate._apply_presnap(st, _pres(-5, next_down=1, row_togo=10.0, row_down=1), 11, "field_goal", "band0")
    assert (st.yardline_100, st.down, st.ydstogo) == (35, 4, 3)


def test_touchback_rows_keep_absolute_spot():
    """Review pass 1/2 example: a flagged punt from LOS 67 that was a touchback with receiving-team holding put the
    receiver at 90. From live LOS 40 the old translation gave 117 -> clipped 99; the anchored row keeps 90."""
    st = _st(40)
    row = np.array([0, 0, 0, 57, 1, 10, 90, 67, 4, 10., 1])
    simulate._apply_rare_outcome(np.random.default_rng(0), _Cat(), st, "AAA", row, kind="punt", cls="flagged", ref_yl=40)
    assert (st.possession, st.yardline_100) == ("BBB", 90)


@needs_pbp
def test_research_exception_needs_cap_and_budget_enforced():
    from pbp_filter import load_team_history
    c = _cfg("asof_league_v1")
    wk = c["history"]["weeks_inclusive"]
    h = load_team_history(str(PBP), teams=c["history"]["teams"], season=2026, weeks=(wk[0], wk[-1]))
    cat, _ = simulate.build_catalog(h["df"], c, games_df=h["games_df"])
    with pytest.raises(ValueError, match="research_n"):
        simulate.attach_semantics(cat, c, str(PBP), research_unaccepted=("rare_plays",))
    with pytest.raises(ValueError, match="research_n"):
        simulate.attach_semantics(cat, c, str(PBP), research_unaccepted=("rare_plays",),
                                  research_n=simulate.RESEARCH_MAX_N + 1)
    simulate.attach_semantics(cat, c, str(PBP), research_unaccepted=("rare_plays",), research_n=2)
    rng = np.random.default_rng(0)
    simulate.simulate_one(h["df"], cat, c, rng)
    simulate.simulate_one(h["df"], cat, c, rng)
    with pytest.raises(ValueError, match="budget"):
        simulate.simulate_one(h["df"], cat, c, rng)


@needs_pbp
def test_clean_punt_return_rate_population_excludes_touchbacks():
    m = rp.build_rare_play_model(PBP, season=2026, week_asof_exclusive=10)
    info = m.meta["clean_punt_return_td_rate"]
    assert "non-touchback" in info["source"]
    assert info["punts"] < m.meta["formation"]["punt"]["current_season_only"]["clean"]["n"]
