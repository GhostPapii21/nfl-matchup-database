"""NFL-75 item 5: opt-in fitted dispersion. Offline, no network."""
import json
import numpy as np
import pandas as pd
import pytest

from market_calibration import fitted_dispersion as D
from market_calibration import fit_dispersion_nflverse as F


def test_default_mode_is_fixed_and_returns_current_values(monkeypatch):
    monkeypatch.delenv("NFL_DISPERSION_MODE", raising=False)
    assert D.resolve_mode() == "fixed"
    for s in (0, 2.5, 7, 14):
        assert D.margin_sd(s) == 13.5
    for t in (37.5, 44.5, 52.5):
        assert D.total_sd(t) == 13.0
    assert D.yard_sigma("rec", "WR", 66.5) == 0.70
    assert D.yard_sigma("rec", "TE", 46.5) == 0.75
    assert D.yard_sigma("rush", "RB", 63.5) == 0.45


def test_unknown_mode_refused(monkeypatch):
    with pytest.raises(ValueError):
        D.resolve_mode("tuned")
    monkeypatch.setenv("NFL_DISPERSION_MODE", "bogus")
    with pytest.raises(ValueError):
        D.margin_sd(3)


def test_env_flag_opts_in(monkeypatch):
    monkeypatch.setenv("NFL_DISPERSION_MODE", "fitted_nflverse_v1")
    fit = json.loads(D.FIT_PATH.read_text())
    assert D.margin_sd(3.5) == pytest.approx(fit["margin_sd_by_abs_spread"]["values"]["[3,7)"]["sd"])
    assert D.total_sd(44.5) == pytest.approx(fit["total_sd_by_total_line"]["values"]["[41,45)"]["sd"])


def test_committed_fit_is_sourced_and_sane():
    fit = json.loads(D.FIT_PATH.read_text())
    files = fit["sources"]["files"]
    assert {f"play_by_play_{y}.parquet" for y in range(2018, 2027)} <= set(files)
    assert all(len(v["sha256"]) == 64 for v in files.values())
    assert fit["train_window"]["last_week_inclusive_of_last_season"] == 9  # never weeks >= 10
    m = fit["margin_sd_by_abs_spread"]["values"]
    assert m["all"]["n"] > 2000 and 10 < m["all"]["sd"] < 16
    for k, c in fit["player_yards_lognormal"]["rec:WR"]["cells"].items():
        assert c["n"] > 100 and 0.2 < c["sigma"] < 1.5 and 0 <= c["p0"] < 1


def test_bin_edges_route_correctly():
    fit = {"margin_sd_by_abs_spread": {"bins": [0, 3, 7, 10, 99],
           "values": {"[0,3)": {"sd": 1}, "[3,7)": {"sd": 2}, "[7,10)": {"sd": 3}, "[10,99)": {"sd": 4}}}}
    got = [D.margin_sd(x, "fitted_nflverse_v1", fit) for x in (0, 2.9, 3, -6.5, 7, 9.5, 10, 17)]
    assert got == [1, 1, 2, 2, 3, 3, 4, 4]


def _synthetic(seed=0, sigma=0.6, n_players=60, games=16):
    rng = np.random.default_rng(seed)
    rows, grows = [], []
    for s in (2024, 2025):
        for w in range(1, games + 1):
            gid = f"{s}_{w:02d}"
            grows.append({"game_id": gid, "season": s, "week": w, "home": "A", "away": "B",
                          "home_score": 24, "away_score": 20, "spread_line": 3.0, "total_line": 44.0})
            for p in range(n_players):
                rows.append({"stat": "rec", "pid": f"p{p}", "pos": "WR", "game_id": gid, "season": s, "week": w,
                             "yards": float(50 * np.exp(rng.normal(0, sigma)))})
    pg = pd.DataFrame(rows).sort_values(["stat", "pid", "season", "week"]).reset_index(drop=True)
    pg["trail_mean"] = 50.0
    g = pd.DataFrame(grows)
    g["margin_resid"] = rng.normal(0, 12, len(g)); g["total_resid"] = rng.normal(0, 13, len(g))
    return g, pg


def test_fit_recovers_known_sigma():
    g, pg = _synthetic(sigma=0.6)
    fit = F.fit(g, pg, 2025, 16)
    c = fit["player_yards_lognormal"]["rec:WR"]["cells"]["[50,70)"]
    assert c["sigma"] == pytest.approx(0.6, abs=0.03)
    assert c["med_ratio"] == pytest.approx(1.0, abs=0.05)


def test_walk_forward_mask_excludes_test_week():
    g, pg = _synthetic()
    a = F.fit(g, pg, 2025, 8)["player_yards_lognormal"]["rec:WR"]["cells"]["[50,70)"]["n"]
    b = F.fit(g, pg, 2025, 9)["player_yards_lognormal"]["rec:WR"]["cells"]["[50,70)"]["n"]
    assert b - a == 60  # exactly week 9's player-games enter only when week 9 is in the training window


def test_trailing_mean_uses_only_prior_games():
    pbp_like = pd.DataFrame({"stat": "rec", "pid": "x", "yards": [10.0, 20, 30, 40, 50], "season": 2025,
                             "week": [1, 2, 3, 4, 5]})
    tm = F.trailing_mean(pbp_like)
    assert np.isnan(tm.iloc[2]) and tm.iloc[3] == 20.0 and tm.iloc[4] == 25.0
