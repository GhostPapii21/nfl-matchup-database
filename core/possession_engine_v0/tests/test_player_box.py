"""NFL-75 per-player box recorder (player_box.py) on the 100k engine path (simulate_games -> snapshots/lock.run_sim ->
pipeline.sim100k). Written BEFORE the recorder.

1. Observational only: with the recorder on, every output block that existed on main 3dad900 (game results, special
   teams counts, the old yard ledger, evidence) is byte-identical for the same seed, on 4 configs x 2 seeds.
2. Reconciliation: per trial, team totals == sum of player lines (UNASSIGNED included) for every stat, and the team
   ledger agrees with the engine's own events (snaps, offensive TDs, turnovers, yards) and its existing yard ledger.
3. Attribution rules on toy rows, and the recorder never draws from the RNG.
Research only. projection_ready stays false."""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _player_box_golden as G  # noqa: E402
import simulate  # noqa: E402
from state import GameState  # noqa: E402

needs_pbp = pytest.mark.skipif(not G.PBP.exists(), reason="committed nflverse W1-9 PBP missing")
GOLD = json.loads((Path(__file__).resolve().parent / "player_box_golden_main_3dad900.json").read_text())

_CACHE: dict = {}


def _run(name, seed, **kw):
    key = (name, seed, tuple(sorted(kw.items())))
    if key not in _CACHE:
        _CACHE[key] = G.run(name, G.N, seed, **kw)
    return _CACHE[key]


# ------------------------------------------------------------------ 1. bit-identical vs main
@needs_pbp
@pytest.mark.parametrize("name", G.VARIANTS)
@pytest.mark.parametrize("seed", G.SEEDS)
def test_recorder_on_is_bit_identical_to_main(name, seed):
    out = _run(name, seed)
    assert "player_box" in out, "recorder must be on by default on the 100k path"
    assert G.digest(out) == GOLD["digests"][f"{name}|{seed}"]


@needs_pbp
def test_recorder_off_is_bit_identical_and_has_no_box():
    out = G.run("was_nyg_lock", G.N, 20261112, record_players=False)
    assert "player_box" not in out
    assert G.digest(out) == GOLD["digests"]["was_nyg_lock|20261112"]


# ------------------------------------------------------------------ 2. reconciliation
@needs_pbp
@pytest.mark.parametrize("name", G.VARIANTS)
def test_every_trial_reconciles(name):
    out = _run(name, 20261112)
    pb = out["player_box"]
    rec = pb["reconciliation"]
    assert rec["trials"] == G.N and rec["failures"] == 0, rec.get("first_failures")
    assert set(rec["checks"]) >= {"player_sum_eq_team", "plays_eq_engine_snaps", "plays_eq_play_types",
                                  "pass_att_eq_targets_plus_untargeted", "off_td_eq_engine_td_events",
                                  "turnovers_eq_engine_turnover_events", "yards_eq_engine_snap_yards",
                                  "rec_yds_eq_engine_ledger", "rush_yds_eq_engine_ledger", "pass_yds_eq_engine_ledger",
                                  "sacks_made_eq_sacks_taken"}
    vals, cols = pb["values"], pb["columns"]
    tvals, tcols = pb["team_values"], pb["team_columns"]
    assert vals.shape == (G.N, len(cols)) and tvals.shape == (G.N, len(tcols))
    # recompute player-sum == team from the stored matrices (independent of the in-engine check)
    tix = {(t, s): j for j, (t, s) in enumerate(tcols)}
    sums: dict = {}
    for j, (t, p, s) in enumerate(cols):
        sums.setdefault((t, s), np.zeros(G.N))
        sums[(t, s)] = sums[(t, s)] + vals[:, j]
    for (t, s), v in sums.items():
        assert np.array_equal(v, tvals[:, tix[(t, s)]]), (t, s)
    for (t, s), j in tix.items():
        if s in pb["player_stats"]:
            assert np.array_equal(sums.get((t, s), np.zeros(G.N)), tvals[:, j]), (t, s)


@needs_pbp
def test_box_has_real_players_and_plausible_volume():
    pb = _run("was_nyg_lock", 20261112)["player_box"]
    names = {(t, p) for t, p, s in pb["columns"]}
    assert ("NYG", "J.Dart") in names or any(t == "NYG" and p.endswith("Dart") for t, p in names)
    tix = {tuple(c): j for j, c in enumerate(pb["team_columns"])}
    for team in ("NYG", "WAS"):
        plays = pb["team_values"][:, tix[(team, "plays")]]
        assert 45 <= np.median(plays) <= 90


# ------------------------------------------------------------------ 3. attribution rules on toy rows
def _st():
    st = GameState.new_game(home="NYG", away="WAS")
    st.possession, st.yardline_100, st.down, st.ydstogo, st.game_seconds_remaining = "NYG", 50, 1, 10, 600
    import player_box as PB
    st.player_box = PB.BoxRecorder(home="NYG", away="WAS", lookup={})
    return st


class _Cat:
    clock_map = None
    semantics = None


def _row(pt, gain, **kw):
    r = dict(game_id="g", play_id=1, posteam="NYG", defteam="WAS", play_type=pt, yards_gained=gain,
             interception=0, fumble_lost=0, sack=0, complete_pass=0, passer_player_name=None,
             rusher_player_name=None, receiver_player_name=None)
    r.update(kw)
    return pd.Series(r)


def _apply(st, row, seed=0):
    rng = np.random.default_rng(seed)
    simulate._apply_row(rng, _Cat(), st, row)
    return rng


def _p(st, team, name, stat):
    return st.player_box.players.get(team, {}).get(name, {}).get(stat, 0)


def test_run_credits_carry_yards_and_td():
    st = _st()
    st.yardline_100 = 5
    _apply(st, _row("run", 7, rusher_player_name="T.Tracy"))
    assert _p(st, "NYG", "T.Tracy", "carries") == 1 and _p(st, "NYG", "T.Tracy", "rush_yds") == 5  # capped at goal
    assert _p(st, "NYG", "T.Tracy", "rush_td") == 1
    assert st.player_box.team["NYG"]["plays"] == 1


def test_incomplete_pass_is_target_not_reception():
    st = _st()
    _apply(st, _row("pass", 0, passer_player_name="J.Dart", receiver_player_name="M.Nabers"))
    assert _p(st, "NYG", "J.Dart", "pass_att") == 1 and _p(st, "NYG", "J.Dart", "pass_cmp") == 0
    assert _p(st, "NYG", "M.Nabers", "targets") == 1 and _p(st, "NYG", "M.Nabers", "rec") == 0


def test_complete_pass_credits_both_and_throwaway_is_untargeted():
    st = _st()
    _apply(st, _row("pass", 12, complete_pass=1, passer_player_name="J.Dart", receiver_player_name="T.Johnson"))
    assert _p(st, "NYG", "T.Johnson", "rec") == 1 and _p(st, "NYG", "T.Johnson", "rec_yds") == 12
    assert _p(st, "NYG", "J.Dart", "pass_yds") == 12 and _p(st, "NYG", "J.Dart", "pass_cmp") == 1
    _apply(st, _row("pass", 0, passer_player_name="J.Dart"))
    assert st.player_box.team["NYG"]["untargeted_att"] == 1 and st.player_box.team["NYG"]["targets"] == 1


def test_sack_credits_passer_and_defender_halves():
    import player_box as PB
    st = _st()
    st.player_box = PB.BoxRecorder(home="NYG", away="WAS", lookup={
        ("g", 1): {"sack_player_name": None, "half_sack_1_player_name": "A", "half_sack_2_player_name": "B"},
        ("g", 2): {"sack_player_name": "D.Payne"}})
    _apply(st, _row("pass", -7, sack=1, passer_player_name="J.Dart"))
    _apply(st, _row("pass", -3, sack=1, passer_player_name="J.Dart", play_id=2))
    assert _p(st, "NYG", "J.Dart", "sacks_taken") == 2 and _p(st, "NYG", "J.Dart", "sack_yds") == -10
    assert _p(st, "NYG", "J.Dart", "pass_att") == 0
    assert _p(st, "WAS", "A", "sacks_made") == 0.5 and _p(st, "WAS", "B", "sacks_made") == 0.5
    assert _p(st, "WAS", "D.Payne", "sacks_made") == 1 and st.player_box.team["WAS"]["sacks_made"] == 2


def test_interception_credits_thrower_and_defender():
    import player_box as PB
    st = _st()
    st.player_box = PB.BoxRecorder(home="NYG", away="WAS", lookup={("g", 1): {"interception_player_name": "Q.Martin"}})
    _apply(st, _row("pass", 0, interception=1, passer_player_name="J.Dart", receiver_player_name="M.Nabers"))
    assert _p(st, "NYG", "J.Dart", "int_thrown") == 1 and _p(st, "WAS", "Q.Martin", "def_int") == 1
    assert _p(st, "NYG", "M.Nabers", "targets") == 1 and st.possession == "WAS"


def test_foreign_rows_go_to_unassigned_never_to_named_defenders():
    import player_box as PB
    st = _st()
    st.player_box = PB.BoxRecorder(home="NYG", away="WAS", lookup={("g", 1): {"sack_player_name": "Other.Guy",
                                                                               "receiver_player_name": "X"}})
    _apply(st, _row("pass", -5, sack=1, posteam="DAL", defteam="PHI"))
    _apply(st, _row("pass", 0, posteam="DAL", defteam="PHI"))  # nulled foreign incomplete that had a receiver
    assert _p(st, "NYG", PB.UNASSIGNED, "sacks_taken") == 1
    assert _p(st, "WAS", PB.UNASSIGNED, "sacks_made") == 1 and _p(st, "WAS", "Other.Guy", "sacks_made") == 0
    assert _p(st, "NYG", PB.UNASSIGNED, "targets") == 1


def test_recorder_draws_nothing_from_rng():
    rows = [_row("pass", 9, complete_pass=1, passer_player_name="J.Dart", receiver_player_name="W.Robinson"),
            _row("run", 3, rusher_player_name="C.Skattebo"), _row("pass", -6, sack=1, passer_player_name="J.Dart")]
    for r in rows:
        a, b = _st(), _st()
        b.player_box = None
        ra, rb = _apply(a, r, seed=3), _apply(b, r, seed=3)
        assert ra.bit_generator.state == rb.bit_generator.state
        assert (a.yardline_100, a.down, a.ydstogo, a.score_home, a.possession, a.game_seconds_remaining) == \
               (b.yardline_100, b.down, b.ydstogo, b.score_home, b.possession, b.game_seconds_remaining)
        assert a.events == b.events and a.player_counts == b.player_counts


def test_summary_quantiles():
    import player_box as PB
    cols = [("NYG", "A", "rec"), ("NYG", "A", "rec_yds")]
    vals = np.array([[1, 10], [3, 30], [5, 50]], dtype=float)
    s = PB.summarize(cols, vals)
    assert s["NYG"]["A"]["rec"]["median"] == 3 and s["NYG"]["A"]["rec_yds"]["mean"] == 30
