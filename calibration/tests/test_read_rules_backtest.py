"""Read-rules backtest helpers: verdict wording, paired diff CI, weather proxy unknowns, feature join keeps rows."""
import json

import numpy as np
import pandas as pd

from calibration import read_rules_backtest as RB


def _legs(n_games=40, wins_per_game=(1, 0), dec=1.9):
    rows = []
    for g in range(n_games):
        for i, w in enumerate(wins_per_game):
            rows.append(dict(game_id=f"G{g}", week=4 + g % 6, win=float(w), push=0, dec=dec, k=(i == 0)))
    return pd.DataFrame(rows)


def test_verdict_wording():
    assert RB.verdict(dict(n=10, margin=0.3, margin_lo=0.1)) == "insufficient sample (n<30)"
    assert RB.verdict(dict(n=40, margin=0.05, margin_lo=-0.02)) == "insufficient sample (CI includes 0)"
    assert RB.verdict(dict(n=40, margin=-0.05, margin_lo=-0.1)) == "no edge shown"
    assert RB.verdict(dict(n=40, margin=0.1, margin_lo=0.01)) == "margin CI > 0"


def test_diff_ci_positive_when_kept_subset_always_wins():
    d = _legs()
    out = RB.diff_ci(d, d.k, B=500)
    # kept subset hits 100%, full baseline 50%: diff = 0.5 exactly in every resample
    assert np.isclose(out["diff"], 0.5) and np.isclose(out["diff_lo"], 0.5) and np.isclose(out["diff_hi"], 0.5)


def test_diff_ci_empty_keep_is_nan():
    d = _legs()
    out = RB.diff_ci(d, pd.Series(False, index=d.index), B=50)
    assert np.isnan(out["diff"])


def test_kickoff_weather_unknown_and_indoor():
    pbp = pd.DataFrame(dict(game_id=["a", "b", "c", "d"], roof=["dome", "outdoors", "outdoors", "outdoors"],
                            wind=[None, 18.0, None, 3.0],
                            weather=[None, "Cloudy Temp: 40° F, Wind: N 18 mph", None, "Light Rain Temp: 50° F, Wind: S 3 mph"]))
    w = RB.kickoff_weather(pbp).set_index("game_id")
    assert w.loc["a", "wx_bad"] == "indoor"
    assert w.loc["b", "wx_bad"] == "bad" and w.loc["b", "wx_wind15"] == "wind>=15"
    assert w.loc["c", "wx_bad"] == "unknown"           # no observation -> unknown, never "not bad"
    assert w.loc["d", "wx_precip"] == "precip_reported" and w.loc["d", "wx_bad"] == "bad"


def test_open_meteo_proxy(tmp_path):
    p = tmp_path / "om.json"
    p.write_text(json.dumps({
        "A@B": dict(game_id="2026_06_A_B", roof="outdoors", kickoff=dict(status="OK", wind_mph=16, gust_mph=20, precip_pct=5)),
        "C@D": dict(game_id="2026_06_C_D", roof="dome", kickoff=dict(status="OK", wind_mph=1, gust_mph=2, precip_pct=0)),
        "E@F": dict(game_id="2026_06_E_F", roof="outdoors", kickoff=dict(status="MISSING")),
        "G@H": dict(game_id="2026_06_G_H", roof="outdoors", kickoff=dict(status="OK", wind_mph=5, gust_mph=26, precip_pct=0))}))
    om = RB.open_meteo_wk6_8(p).set_index("game_id").om_grade.to_dict()
    assert om == {"2026_06_A_B": "windy", "2026_06_C_D": "indoor", "2026_06_E_F": "unknown", "2026_06_G_H": "windy"}
    assert RB.open_meteo_wk6_8(tmp_path / "missing.json").empty


def test_add_features_never_adds_or_drops_legs():
    from pipeline.tests.test_read_rules import POS, _team_games
    pbp = _team_games()
    L = pd.DataFrame(dict(week=[5, 5, 5, 5], game_id=["2026_05_AAA_BBB"] * 4, gsis=["wr1", "wr1", "te1", "rb1"],
                          position=["WR", "WR", "TE", "RB"], market=["recyds", "recyds", "rec", "rushyds"],
                          line=[40.5, 60.5, 2.5, 30.5]))
    out = RB.add_features(L, pbp, POS)
    assert len(out) == len(L)
    assert list(out.rr_tf) == ["PASS", "PASS", "PASS", "NOT_APPLICABLE"]
    assert set(out.rr_def_run) <= {"soft", "not_soft", "unknown"}
