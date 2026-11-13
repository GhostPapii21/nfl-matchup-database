"""Grading rules of calibration/slip_joint_validation.py: pushes and did-not-play legs void; clustered metrics."""
import numpy as np
import pandas as pd
from calibration.slip_joint_validation import actual_game, grade_leg, metrics


def _pbp():
    rows = [
        dict(game_id="G", posteam="AAA", play_type="pass", complete_pass=1, sack=0, yards_gained=30,
             passer_player_name="Q", receiver_player_name="W", rusher_player_name=None, home_score=24, away_score=20),
        dict(game_id="G", posteam="AAA", play_type="pass", complete_pass=0, sack=1, yards_gained=-7,
             passer_player_name="Q", receiver_player_name=None, rusher_player_name=None, home_score=24, away_score=20),
        dict(game_id="G", posteam="AAA", play_type="run", complete_pass=0, sack=0, yards_gained=12,
             passer_player_name=None, receiver_player_name=None, rusher_player_name="R", home_score=24, away_score=20),
    ]
    return pd.DataFrame(rows)


def test_actual_game_matches_sim_crediting_rules():
    a = actual_game(_pbp(), "G")
    assert a["players"]["pass_yards|AAA|Q"] == 30.0  # sack not credited, same as the engine
    assert a["players"]["rec_yards|AAA|W"] == 30.0 and a["players"]["rush_yards|AAA|R"] == 12.0
    assert a["home_pts"] == 24 and "AAA|Q" in a["played"]


def test_grade_leg_push_and_dnp_void():
    a = actual_game(_pbp(), "G")
    assert grade_leg(a, ("game", "total", ">", 44)) is None          # push
    assert grade_leg(a, ("game", "total", ">", 43.5)) is True
    assert grade_leg(a, ("rec_yards", "AAA|Nobody", ">=", 1)) is None  # did not play
    assert grade_leg(a, ("rush_yards", "AAA|R", ">=", 12.5)) is False


def test_metrics_sign_convention():
    df = pd.DataFrame({"game_id": ["a", "b", "c", "d"], "hit": [1, 0, 1, 0],
                       "p_joint": [0.9, 0.1, 0.9, 0.1], "p_indep": [0.5, 0.5, 0.5, 0.5]})
    m = metrics(df, B=200)
    assert m["brier_improvement_joint_vs_indep"] > 0 and m["brier_p_joint"] < m["brier_p_indep"]
