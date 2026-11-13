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


# ---------------------------------------------------------------- reproduction from the pinned nflverse files
import os
from pathlib import Path

_PBP_DIR = Path(os.environ.get("NFLVERSE_PBP_DIR", "/tmp/nflverse_pbp"))
_FIT = json.loads(D.FIT_PATH.read_text())
_PINNED = _FIT["sources"]["files"]


def _pinned_ok():
    for name, meta in _PINNED.items():
        f = _PBP_DIR / name
        if not f.is_file():
            return False, f"pinned nflverse file absent: {f} (set NFLVERSE_PBP_DIR)"
        if F.sha256(f) != meta["sha256"]:
            return False, f"{f} sha256 differs from the pinned value (nflverse re-published); cannot reproduce"
    return True, ""


@pytest.fixture(scope="module")
def refit():
    ok, why = _pinned_ok()
    if not ok:
        pytest.skip(why)
    pbp, meta = F.load_pbp(_PBP_DIR)
    players = pd.read_parquet(_PBP_DIR / "players.parquet", columns=["gsis_id", "position"])
    return F.game_table(pbp), F.player_games(pbp, players), meta


def _flat(d, pre=""):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update(_flat(v, f"{pre}{k}/"))
        else:
            out[f"{pre}{k}"] = v
    return out


def test_refit_from_pinned_files_reproduces_committed_fit(refit):
    games, pg, meta = refit
    assert {k: v["sha256"] for k, v in meta.items()} == {k: v["sha256"] for k, v in _PINNED.items() if k in meta}
    new = _flat(F.fit(games, pg, 2026, 9))
    old = _flat({k: _FIT[k] for k in ("train_window", "margin_sd_by_abs_spread", "total_sd_by_total_line",
                                      "player_yards_lognormal")})
    assert set(new) == set(old)
    for k, v in old.items():
        if isinstance(v, float):
            assert new[k] == pytest.approx(v, rel=0, abs=1e-12), k
        else:
            assert new[k] == v, k


def test_refit_reproduces_one_walk_forward_week(refit):
    games, pg, _ = refit
    bt = json.loads((D.FIT_PATH.parent / "backtest_dispersion_wk04_09.json").read_text())
    f = F.fit(games, pg, 2026, 3)  # frozen fit used to score week 4
    for k, v in bt["fits_by_test_week"]["4"]["margin"].items():
        assert round(f["margin_sd_by_abs_spread"]["values"][k]["sd"], 3) == v
    for k, v in bt["fits_by_test_week"]["4"]["total"].items():
        assert round(f["total_sd_by_total_line"]["values"][k]["sd"], 3) == v


# ---------------------------------------------------------------- centre guard
def test_fitted_player_sigma_requires_trailing_mean_reference():
    assert _FIT["player_sigma_reference"] == "trailing_mean"
    with pytest.raises(ValueError, match="trailing mean"):
        D.yard_sigma("rush", "RB", 63.5, "fitted_nflverse_v1")                       # no reference
    with pytest.raises(ValueError, match="book line"):
        D.yard_sigma("rush", "RB", 63.5, "fitted_nflverse_v1", reference="book_line")
    with pytest.raises(ValueError):
        D.yard_cell("rec", "WR", 60.0, reference="market_line")
    s = D.yard_sigma("rush", "RB", 63.5, "fitted_nflverse_v1", reference="trailing_mean")
    assert s == pytest.approx(_FIT["player_yards_lognormal"]["rush:RB"]["cells"]["[50,70)"]["sigma"])
    assert D.yard_cell("rush", "RB", 63.5, reference="trailing_mean")["reference"] == "trailing_mean"


def test_fixed_sigmas_are_book_line_centred_only():
    assert D.yard_sigma("rec", "WR", 66.5, "fixed", reference="book_line") == 0.70
    with pytest.raises(ValueError):
        D.yard_sigma("rec", "WR", 66.5, "fixed", reference="trailing_mean")
