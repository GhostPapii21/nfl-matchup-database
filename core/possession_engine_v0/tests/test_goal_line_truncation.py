"""WP2 (NFL-75): goal-line truncation of resampled gains.

A historical pass/run that scored from yardline y0 only says the play gained AT LEAST y0 yards. 19.9% of red-zone
pass/run rows on the W1-9 file are cut off like this (calibration/outputs/diag_total_w09_off_default.json,
goal_line_censoring.RZ). Drawn when the ball is further out (y > y0), the old engine used y0 as an ordinary gain.
Fix: Efron redistribute-to-the-right within the same pool (simulate._resolve_goal_line_censoring); nothing tuned
or fitted (the same-pool-then-team-pool fallback order is a structural choice).
accounting goal_line_censoring="truncate" (pre_wp12 / legacy) keeps the old behaviour. Research only, not validated."""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import simulate as sim  # noqa: E402
from simulate import PlayCatalog, _apply_snap, _gl_censored_at, _resolve_goal_line_censoring, accounting_from_cfg  # noqa: E402
from state import GameState  # noqa: E402

REPO = HERE.parents[1]
PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"


def _row(yl, gain, pt="run", td=None, **kw):
    # every toy row is 1st-and-10 so they share one (down, distance, red-zone) sampling cell
    td = int(gain >= yl) if td is None else td
    r = dict(game_id="g", play_id=0, posteam="NYG", defteam="WAS", down=1, ydstogo=10,
             yardline_100=yl, play_type=pt, yards_gained=gain, touchdown=td, interception=0, fumble_lost=0, sack=0,
             complete_pass=1 if pt == "pass" else 0, rusher_player_name="R" if pt == "run" else None,
             passer_player_name="Q" if pt == "pass" else None, receiver_player_name="W" if pt == "pass" else None)
    r.update(kw)
    return r


def _st(yl, down=1, togo=10):
    st = GameState.new_game(home="NYG", away="WAS")
    st.possession, st.yardline_100, st.down, st.ydstogo, st.game_seconds_remaining = "NYG", yl, down, togo, 600
    return st


def test_censored_at_definition():
    assert _gl_censored_at(pd.Series(_row(2, 2))) == 2
    assert _gl_censored_at(pd.Series(_row(15, 4))) is None
    assert _gl_censored_at(pd.Series(_row(3, 3, interception=1))) is None
    assert _gl_censored_at(pd.Series(_row(3, 3, pt="punt"))) is None
    assert _gl_censored_at(pd.Series(_row(3, float("nan")))) is None


def _cat(rows):
    df = pd.DataFrame(rows)
    df["play_id"] = range(len(df))
    return PlayCatalog(df, min_n=1)


def test_censored_short_td_no_longer_becomes_a_short_gain_far_out():
    # RZ cell, 1st down: a 2-yd TD plunge from the 2 plus runs from the 15/18 (4 yds, 6 yds, a 15-yd TD from the 15)
    cat = _cat([_row(2, 2), _row(15, 4), _row(18, 6), _row(15, 15), _row(1, 1)])
    rng = np.random.default_rng(0)
    gains_old, gains_new = [], []
    for mode, out in (("truncate", gains_old), ("redistribute_right", gains_new)):
        cat.goal_line_censoring = mode
        for _ in range(600):
            st = _st(15)
            _apply_snap(rng, cat, st, False)
            out.append(next(e for e in st.events if e["type"] == "snap")["yards"])
    assert {1.0, 2.0} <= set(gains_old), "old engine turns the 1-/2-yd TDs into 1-/2-yd gains at the 15"
    assert not ({1.0, 2.0} & set(gains_new)), "censored draws are resolved to rows known to gain >= y0"
    assert set(gains_new) <= {4.0, 6.0, 15.0}


def test_rows_from_further_out_are_untouched_and_y0_ge_y_kept():
    cat = _cat([_row(8, 8), _row(5, 2)])
    st = _st(5)
    cat._last_pool = cat.by_team["NYG"]
    r, tag = _resolve_goal_line_censoring(np.random.default_rng(0), cat, st, cat.by_team["NYG"].iloc[0])
    assert tag is None and r["yardline_100"] == 8, "censored at y0=8 >= y=5 is informative (TD from the 5)"


def test_unresolved_is_flagged_and_keeps_old_row():
    cat = _cat([_row(2, 2)])  # nothing else in the pool or the team
    st = _st(15)
    _apply_snap(np.random.default_rng(0), cat, st, False)
    snap = next(e for e in st.events if e["type"] == "snap")
    assert snap["goal_line_censoring"] == "GL_CENSOR_UNRESOLVED" and snap["yards"] == 2.0
    assert "GL_CENSOR_UNRESOLVED" in st.sparse_flags


def test_play_type_is_preserved_and_foreign_names_stay_blank():
    cat = _cat([_row(2, 2, pt="pass"), _row(15, 9, pt="pass"), _row(15, 7, pt="run")])
    pool = cat.by_team["NYG"]
    cat._last_pool, cat._last_pool_foreign = pool, True
    r, tag = _resolve_goal_line_censoring(np.random.default_rng(1), cat, _st(15), pool.iloc[0])
    assert tag == "GL_CENSOR_RESOLVED" and r["play_type"] == "pass" and r["yards_gained"] == 9
    assert r["passer_player_name"] is None and r["receiver_player_name"] is None


def test_chain_terminates_when_replacement_is_censored_again():
    # y=15: censored at 2 -> only candidate row is censored at 6 -> resolves to the 9-yd gain from the 12
    cat = _cat([_row(2, 2), _row(6, 6), _row(12, 9)])
    pool = cat.by_team["NYG"]
    cat._last_pool = pool
    seen = set()
    rng = np.random.default_rng(3)
    for _ in range(200):
        r, tag = _resolve_goal_line_censoring(rng, cat, _st(15), pool.iloc[0])
        assert tag == "GL_CENSOR_RESOLVED"
        seen.add(int(r["yards_gained"]))
    assert seen == {9}


def test_accounting_switch():
    assert accounting_from_cfg({})["goal_line_censoring"] == "redistribute_right"
    assert accounting_from_cfg({"accounting": "pre_wp12"})["goal_line_censoring"] == "truncate"
    assert accounting_from_cfg({"accounting": "legacy"})["goal_line_censoring"] == "truncate"
    with pytest.raises(ValueError):
        accounting_from_cfg({"accounting": {"goal_line_censoring": "cap"}})


needs_pbp = pytest.mark.skipif(not PBP.exists(), reason="committed nflverse W1-9 PBP not present")


DRAWS = 3


@pytest.fixture(scope="module")
def league_rz():
    """League-wide W1-9 pass/run pool under one label (so every red-zone state has a dense pool), and every actual
    pass/run snap snapped inside the 20 as the set of states to replay. Actual = offensive TD on that snap."""
    p = pd.read_parquet(PBP)
    snaps = p[p["play_type"].isin(["pass", "run"]) & p["down"].notna()].copy()
    lg = snaps.copy()
    lg["posteam"], lg["defteam"] = "LG", "OPP"
    cat = PlayCatalog(lg, min_n=5)
    rz = snaps[snaps["yardline_100"] <= 20].copy()
    rz["act_td"] = ((rz["touchdown"] == 1) & (rz["td_team"] == rz["posteam"])).astype(int)
    out = {}
    for mode in ("truncate", "redistribute_right"):
        cat.goal_line_censoring = mode
        rng = np.random.default_rng(20261112)
        td, trunc = [], []
        for r in rz.itertuples():
            t = k = 0
            for _ in range(DRAWS):
                st = GameState.new_game(home="LG", away="OPP")
                st.possession, st.down, st.ydstogo, st.yardline_100, st.game_seconds_remaining = \
                    "LG", int(r.down), int(r.ydstogo), int(r.yardline_100), 600
                _apply_snap(rng, cat, st, False)
                snap = next(e for e in st.events if e["type"] == "snap")
                t += any(e["type"] == "touchdown" for e in st.events)
                # truncated = a historical TD cut off at y0 < current spot, used as an ordinary y0-yard gain
                k += snap.get("goal_line_censoring") in ("GL_CENSOR_TRUNCATED", "GL_CENSOR_UNRESOLVED")
            td.append(t / DRAWS)
            trunc.append(k / DRAWS)
        out[mode] = {"td": np.array(td, float), "trunc": np.array(trunc, float)}
    return rz, out


@needs_pbp
def test_truncation_rate_and_td_share_inside_the_10(league_rz):
    """Replays every actual W1-9 red-zone pass/run state through _apply_snap (3 draws each, fixed seed).
    Measured 2026-11-12 (12 draws/state, same file): offensive-TD share per snap inside the 20 actual 19.8%,
    pre-fix 16.1%, fixed 21.2%; 11-20 yd band actual 8.6%, pre-fix 4.2%, fixed 8.6%; inside the 10 actual 32.3%,
    pre-fix 29.4%, fixed 35.2%. Inside the 10 the fix trades a ~3-pt under-count for a ~3-pt over-count (largest
    inside the 3): redistribute-to-the-right assumes the gain is independent of field position within the
    red-zone cell, which goal-line compression breaks. That residual is a declared limitation, not tuned away."""
    rz, out = league_rz
    y = rz["yardline_100"].to_numpy()
    act = rz["act_td"].to_numpy().astype(float)
    old, new = out["truncate"]["td"], out["redistribute_right"]["td"]
    in10, band = y <= 10, y > 10
    # red zone as a whole: pre-fix under-scores; the fix moves it toward actual
    assert old.mean() < act.mean() - 0.02, (old.mean(), act.mean())
    assert abs(new.mean() - act.mean()) < abs(old.mean() - act.mean())
    assert abs(new.mean() - act.mean()) < 0.025, (new.mean(), act.mean())
    # 11-20 yd band (where censored short TDs were drawn most often): pre-fix about half of actual, fixed on it
    assert old[band].mean() < act[band].mean() - 0.03, (old[band].mean(), act[band].mean())
    assert abs(new[band].mean() - act[band].mean()) < 0.015, (new[band].mean(), act[band].mean())
    # TD share inside the 10: pre-fix under, fixed within 4.5 pts (declared residual over-count, see docstring)
    assert old[in10].mean() < act[in10].mean(), (old[in10].mean(), act[in10].mean())
    assert abs(new[in10].mean() - act[in10].mean()) < 0.045, (new[in10].mean(), act[in10].mean())
    # truncation rate of red-zone snaps: material before, zero after (league pool: every censored draw resolves)
    assert out["truncate"]["trunc"].mean() > 0.05, out["truncate"]["trunc"].mean()
    assert out["truncate"]["trunc"][in10].mean() > 0.05
    assert out["redistribute_right"]["trunc"].mean() == 0.0


@needs_pbp
def test_pool_censoring_share_is_the_audited_19_9pct():
    """The data property behind WP2: share of W1-8 league red-zone pass/run rows cut off by the goal line."""
    p = pd.read_parquet(PBP)
    x = p[(p["week"] <= 8) & p["play_type"].isin(["pass", "run"]) & p["down"].notna() & (p["yardline_100"] <= 20)]
    rows = x.to_dict("records")
    share = np.mean([_gl_censored_at(pd.Series(r)) is not None for r in rows])
    assert 0.17 <= share <= 0.23, share


def test_tie_gain_equal_to_y0_counts_as_at_least_y0():
    # y=10: censored at 3; the only candidate gained exactly 3 from the 12 (uncensored) -> a 3-yd gain, resolved
    cat = _cat([_row(3, 3), _row(12, 3)])
    pool = cat.by_team["NYG"]
    cat._last_pool = pool
    r, tag = _resolve_goal_line_censoring(np.random.default_rng(0), cat, _st(10), pool.iloc[0])
    assert tag == "GL_CENSOR_RESOLVED" and r["yardline_100"] == 12 and r["yards_gained"] == 3


def test_unresolved_after_a_partial_chain_returns_the_original_draw():
    # y=15: censored at 2 -> replaced by the TD from the 6 (censored at 6 < 15) -> nothing gains >= 6 from > 6
    cat = _cat([_row(2, 2), _row(6, 6)])
    pool = cat.by_team["NYG"]
    cat._last_pool = pool
    r, tag = _resolve_goal_line_censoring(np.random.default_rng(0), cat, _st(15), pool.iloc[0])
    assert tag == "GL_CENSOR_UNRESOLVED" and r["yardline_100"] == 2 and r["yards_gained"] == 2


def test_long_chains_resolve_without_a_redraw_cap():
    # ball at the 40; censored TDs from every yardline 1..30 plus one 35-yd gain from the 36. Every chain must end
    # on the 35-yd gain however many censored rows it passes through (no fixed redraw cap; y0 strictly increases).
    rows = [_row(i, i) for i in range(1, 31)] + [_row(36, 35)]
    cat = _cat(rows)
    pool = cat.by_team["NYG"]
    rng = np.random.default_rng(5)
    for start in range(30):
        cat._last_pool = pool
        r, tag = _resolve_goal_line_censoring(rng, cat, _st(40), pool.iloc[start])
        assert tag == "GL_CENSOR_RESOLVED" and r["yardline_100"] == 36 and r["yards_gained"] == 35


def test_effects_catalog_tracks_the_blitz_redraw_pool():
    from effects.apply_supported import EffectsCatalog
    base_rows = [_row(15, 4, pt="pass")] * 6
    blitz_rows = [_row(2, 2, pt="pass")] + [_row(15, 9, pt="pass")] * 5
    base = _cat(base_rows)
    ann = pd.DataFrame(blitz_rows)
    ann["play_id"] = range(len(ann))
    ann["is_blitz_ftn"], ann["ftn_joined"] = True, True
    eff = EffectsCatalog(base, ann, enable_blitz_strata=True)
    eff.defense_blitz_rate = {"WAS": 1.0}
    rng = np.random.default_rng(0)
    for _ in range(30):
        row, tag = eff.sample_snap(rng, _st(15), False)
        assert "EFFECT_DEF_BLITZ_STRATA" in tag
        assert eff._last_pool.index.equals(eff.blitz_pools["NYG"].index), "redraw pool = the pool the row came from"
    # and a censored blitz draw resolves inside the blitz pool (to the 9-yd pass), never to the base pool's 4 yds
    eff.goal_line_censoring = "redistribute_right"
    seen = set()
    for _ in range(200):
        st = _st(15)
        _apply_snap(rng, eff, st, False)
        seen.add(next(e for e in st.events if e["type"] == "snap")["yards"])
    assert seen == {9.0}
