"""NFL-75: per-player rushing-yards distribution artifact from the per-player box recorder (pipeline/rush_dist.py).

Written BEFORE pipeline/rush_dist.py (tests-first). Research only; projection_ready stays false."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pipeline import rush_dist as RD  # noqa: E402

GAME = "2026_10_BUF_NYJ"


def _box(n=4000, seed=7):
    """Box-recorder-shaped (columns, values): QB with kneels, RB, a WR with no carries, UNASSIGNED, other team RB."""
    rng = np.random.default_rng(seed)
    cols, vals = [], []

    def add(team, player, stat, v):
        cols.append([team, player, stat])
        vals.append(np.asarray(v, dtype=float))
    qb_car = rng.poisson(6, n)
    add("BUF", "J.Allen", "carries", qb_car)
    add("BUF", "J.Allen", "rush_yds", np.round(rng.normal(32, 18, n)))
    add("BUF", "J.Allen", "kneel_yds", -rng.integers(0, 3, n))
    add("BUF", "J.Allen", "pass_yds", np.round(rng.normal(240, 60, n)))
    add("BUF", "J.Cook", "carries", rng.poisson(15, n))
    add("BUF", "J.Cook", "rush_yds", np.round(rng.gamma(4, 18, n)))
    add("BUF", "K.Shakir", "rec_yds", np.round(rng.gamma(3, 15, n)))       # never carries -> excluded
    add("BUF", "UNASSIGNED", "carries", rng.poisson(1, n))               # not a player -> excluded
    add("BUF", "UNASSIGNED", "rush_yds", rng.integers(0, 5, n))
    rare = (rng.random(n) < 0.05).astype(float)                           # carries in 5% of trials only
    add("NYJ", "B.Hall", "carries", rng.poisson(17, n))
    add("NYJ", "B.Hall", "rush_yds", np.round(rng.gamma(4, 20, n)))
    add("NYJ", "T.Taylor", "carries", rare)
    add("NYJ", "T.Taylor", "rush_yds", rare * 7)
    return cols, np.column_stack(vals)


def _yds(cols, vals, team, player, kneels=True):
    ix = {tuple(c): j for j, c in enumerate(cols)}
    x = vals[:, ix[(team, player, "rush_yds")]].copy()
    if kneels and (team, player, "kneel_yds") in ix:
        x += vals[:, ix[(team, player, "kneel_yds")]]
    return x


def test_includes_every_player_with_a_carry_and_nobody_else():
    cols, vals = _box()
    d = RD.build(cols, vals, game_id=GAME)
    keys = set(zip(d["summary"].team, d["summary"].player))
    assert keys == {("BUF", "J.Allen"), ("BUF", "J.Cook"), ("NYJ", "B.Hall"), ("NYJ", "T.Taylor")}
    tt = d["summary"].set_index("player").loc["T.Taylor"]
    assert tt.p_any_carry == pytest.approx(0.05, abs=0.02)


def test_quantiles_and_moments_match_trials_kneels_included():
    cols, vals = _box()
    d = RD.build(cols, vals, game_id=GAME)
    s = d["summary"].set_index("player")
    for team, pl in (("BUF", "J.Allen"), ("BUF", "J.Cook"), ("NYJ", "B.Hall")):
        x = _yds(cols, vals, team, pl)
        assert s.loc[pl, "n_trials"] == len(x)
        assert s.loc[pl, "mean"] == pytest.approx(x.mean())
        assert s.loc[pl, "sd"] == pytest.approx(x.std())
        for q in RD.QUANTILES:
            assert s.loc[pl, f"q{int(round(q * 100)):02d}"] == pytest.approx(np.quantile(x, q))
    # official-stat convention: kneel-downs are rushes, so the QB's kneel yards are in his rushing yards
    assert s.loc["J.Allen", "mean"] == pytest.approx(_yds(cols, vals, "BUF", "J.Allen").mean())
    assert s.loc["J.Allen", "mean"] != pytest.approx(_yds(cols, vals, "BUF", "J.Allen", kneels=False).mean())
    off = RD.build(cols, vals, game_id=GAME, include_kneels=False)["summary"].set_index("player")
    assert off.loc["J.Allen", "mean"] == pytest.approx(_yds(cols, vals, "BUF", "J.Allen", kneels=False).mean())


@pytest.mark.parametrize("line", [-3.5, 0, 0.5, 9.5, 24.5, 25, 31.5, 44.5, 45.3, 60, 79.5, 120.5, 999.5])
def test_p_under_any_line_matches_trials_exactly(line):
    cols, vals = _box()
    d = RD.build(cols, vals, game_id=GAME)
    for team, pl in (("BUF", "J.Allen"), ("BUF", "J.Cook"), ("NYJ", "B.Hall"), ("NYJ", "T.Taylor")):
        x = _yds(cols, vals, team, pl)
        p = RD.p_under(d["cdf"], team=team, player=pl, line=line)
        assert p["p_under"] == pytest.approx(np.mean(x < line), abs=1e-12)
        assert p["p_push"] == pytest.approx(np.mean(x == line), abs=1e-12)
        assert p["p_over"] == pytest.approx(np.mean(x > line), abs=1e-12)


def test_cdf_grid_is_half_lines_covering_support_and_monotone():
    cols, vals = _box()
    d = RD.build(cols, vals, game_id=GAME)
    c = d["cdf"]
    assert list(c.columns) == list(RD.CDF_COLUMNS)
    for (_, _), g in c.groupby(["team", "player"]):
        lines = g.line.to_numpy()
        assert np.allclose(lines % 1, 0.5) and np.all(np.diff(lines) == 1.0)
        assert np.all(np.diff(g.p_under.to_numpy()) >= 0)
        assert g.p_under.iloc[0] == 0.0 and g.p_under.iloc[-1] == 1.0
        assert np.allclose(g.p_under + g.p_over, 1.0)
        assert lines[0] <= RD.GRID_MIN and lines[-1] >= RD.GRID_MAX


def test_non_integer_yards_are_refused():
    cols, vals = _box(n=50)
    vals = vals.copy()
    vals[3, 1] += 0.25
    with pytest.raises(ValueError, match="integer"):
        RD.build(cols, vals, game_id=GAME)


def test_gsis_and_position_join_from_asof_pbp_and_roster():
    pbp = pd.DataFrame({"posteam": ["BUF", "BUF", "NYJ", "NYJ", "BUF"],
                        "rusher_player_name": ["J.Allen", "J.Cook", "B.Hall", None, None],
                        "rusher_player_id": ["00-1", "00-2", "00-3", None, None],
                        "passer_player_name": [None, None, None, None, "J.Allen"],
                        "passer_player_id": [None, None, None, None, "00-1"]})
    roster = pd.DataFrame({"gsis_id": ["00-1", "00-2", "00-3"], "position": ["QB", "RB", "RB"],
                           "full_name": ["Josh Allen", "James Cook", "Breece Hall"]})
    cols, vals = _box(n=200)
    d = RD.build(cols, vals, game_id=GAME, gsis_map=RD.gsis_map_from_pbp(pbp), roster=roster)
    s = d["summary"].set_index("player")
    assert s.loc["J.Allen", "gsis"] == "00-1" and s.loc["J.Allen", "position"] == "QB"
    assert s.loc["J.Allen", "full_name"] == "Josh Allen"
    assert s.loc["B.Hall", "gsis"] == "00-3" and s.loc["B.Hall", "position"] == "RB"
    assert pd.isna(s.loc["T.Taylor", "gsis"])          # not in the history -> no id, never guessed
    assert set(d["cdf"].gsis.dropna()) == {"00-1", "00-2", "00-3"}


def _legs():
    """selective_edge_live legs schema (calibration/selective_edge_live.py docstring)."""
    base = dict(week=10, game_id=GAME, kind="main", dec=1.87, p_nv=0.5, defender_verified=False,
                price_source="test fixture", actual=np.nan, source="live")
    rows = [dict(base, player="Josh Allen", gsis="00-1", position="QB", market="rushyds", side="Under", line=31.5),
            dict(base, player="Josh Allen", gsis="00-1", position="QB", market="rushyds", side="Over", line=31.5),
            dict(base, player="James Cook", gsis=np.nan, position="RB", market="rushyds", side="Under", line=70.0),
            dict(base, player="Breece Hall", gsis="00-3", position="RB", market="recyds", side="Under", line=20.5),
            dict(base, player="Nobody Here", gsis="00-9", position="RB", market="rushyds", side="Under", line=40.5)]
    df = pd.DataFrame(rows)
    df["p_model"] = np.nan
    return df


def test_attach_p_model_fills_rushyds_graded_side_only():
    cols, vals = _box()
    gm = {("BUF", "J.Allen"): "00-1", ("NYJ", "B.Hall"): "00-3"}
    d = RD.build(cols, vals, game_id=GAME, gsis_map=gm)
    legs = _legs()
    out = RD.attach_p_model(legs, d["cdf"])
    a = _yds(cols, vals, "BUF", "J.Allen")
    u, o = np.mean(a < 31.5), np.mean(a > 31.5)
    assert out.p_model[0] == pytest.approx(u / (u + o)) and out.p_model[1] == pytest.approx(o / (u + o))
    assert out.p_model[0] + out.p_model[1] == pytest.approx(1.0)
    # integer line: push removed (graded side conditional on no push); name fallback J.Cook (unique in game)
    c = _yds(cols, vals, "BUF", "J.Cook")
    u, o = np.mean(c < 70), np.mean(c > 70)
    assert out.p_model[2] == pytest.approx(u / (u + o))
    assert out.p_model_match[2] == "name"
    assert out.p_model_match[0] == "gsis"
    assert pd.isna(out.p_model[3])                       # receiving market untouched
    assert pd.isna(out.p_model[4]) and out.p_model_match[4] == "no_player"
    assert (out.p_model_source.dropna().str.contains("rush_dist")).all()
    assert list(legs.columns) == list(out.columns[:len(legs.columns)])   # schema preserved, columns only appended
    assert legs.p_model.isna().all()                     # input not mutated


def test_attach_never_overwrites_an_existing_p_model():
    cols, vals = _box()
    d = RD.build(cols, vals, game_id=GAME, gsis_map={("BUF", "J.Allen"): "00-1"})
    legs = _legs()
    legs.loc[0, "p_model"] = 0.123
    out = RD.attach_p_model(legs, d["cdf"])
    assert out.p_model[0] == 0.123 and out.p_model_match[0] == "preset"


def test_attached_legs_grade_with_the_frozen_classifier_unchanged():
    from calibration import selective_edge as se
    from calibration.selective_edge_freeze import verify_hashes
    from calibration.selective_edge_live import grade_live
    verify_hashes()                                      # classifier + params still match the freeze manifest
    cols, vals = _box()
    d = RD.build(cols, vals, game_id=GAME, gsis_map={("BUF", "J.Allen"): "00-1", ("NYJ", "B.Hall"): "00-3"})
    legs = RD.attach_p_model(_legs(), d["cdf"])
    ctx = pd.DataFrame({"carry_n_prior": [4.0] * len(legs), "carry_n60": [4.0] * len(legs),
                        "carry_share": [0.7] * len(legs), "usual": [30.0] * len(legs)})
    g = grade_live(legs, pd.DataFrame(), context=ctx)
    assert (g.projection_ready == False).all()  # noqa: E712
    allen_u = g.iloc[0]
    want = se.STRONG_UNDER if allen_u.p_model - 0.5 >= 0 else se.NO_EDGE
    assert allen_u.label == want
    assert g.iloc[4].label == se.INSUFFICIENT and g.iloc[4].reason == "model_prob_missing"


def test_write_and_read_artifact(tmp_path):
    cols, vals = _box(n=500)
    d = RD.build(cols, vals, game_id=GAME, meta={"seed": 1, "n": 500})
    paths = RD.write(d, tmp_path)
    assert {p.name for p in paths.values()} == {f"{GAME}.rush_dist.json", f"{GAME}.rush_dist.cdf.csv",
                                                f"{GAME}.rush_dist.summary.csv"}
    meta = json.loads(paths["json"].read_text())
    assert meta["schema"] == RD.SCHEMA and meta["projection_ready"] is False and meta["research_only"] is True
    assert meta["game_id"] == GAME and meta["n_trials"] == 500 and meta["seed"] == 1
    assert meta["rush_yds_definition"] and meta["p_under_definition"]
    back = RD.read(tmp_path, GAME)
    pd.testing.assert_frame_equal(back["cdf"].reset_index(drop=True), d["cdf"].reset_index(drop=True),
                                  check_dtype=False)
    assert list(back["summary"].columns) == list(RD.SUMMARY_COLUMNS)


def _npz(path, cols, vals):
    np.savez_compressed(path, columns=np.array(["|".join(c) for c in cols]), values=vals.astype(np.float32),
                        team_columns=np.array(["BUF|plays"]), team_values=np.zeros((len(vals), 1), np.float32))


def test_cli_from_sim100k_npz_and_attach(tmp_path):
    cols, vals = _box(n=300)
    npz = tmp_path / f"{GAME}.sim100k.player_box.npz"
    _npz(npz, cols, vals)
    out = tmp_path / "out"
    assert RD.main(["build", "--npz", str(npz), "--game", GAME, "--out", str(out)]) == 0
    assert (out / f"{GAME}.rush_dist.cdf.csv").exists()
    legs = tmp_path / "legs.csv"
    _legs().to_csv(legs, index=False)
    res = tmp_path / "legs_p.csv"
    assert RD.main(["attach", "--legs", str(legs), "--dist", str(out), "--out", str(res)]) == 0
    got = pd.read_csv(res)
    assert got.p_model.notna().sum() >= 2 and "p_model" in got.columns


def test_sim100k_rush_dist_flag_is_opt_in(tmp_path, monkeypatch):
    from pipeline import phases as PH
    from pipeline import sim100k as S
    cols, vals = _box(n=100)
    rep = {"status": "RAN_RESEARCH_ONLY", "reasons": [], "result": {
        "n": 100, "seed": 5, "player_box_trials": {"columns": cols, "values": vals,
                                                   "team_columns": [["BUF", "plays"]],
                                                   "team_values": np.zeros((100, 1))}}}
    import copy
    monkeypatch.setattr(S, "run", lambda g, p=None: (0, copy.deepcopy(rep)))
    monkeypatch.setattr(PH, "LEDGERS", tmp_path / "a")
    assert S.main(["--game", GAME, "--write"]) == 0
    default_files = sorted(p.name for p in (tmp_path / "a").iterdir())
    assert default_files == [f"{GAME}.sim100k.json", f"{GAME}.sim100k.player_box.npz"]   # unchanged default
    monkeypatch.setattr(PH, "LEDGERS", tmp_path / "b")
    assert S.main(["--game", GAME, "--write", "--rush-dist"]) == 0
    names = sorted(p.name for p in (tmp_path / "b").iterdir())
    assert names == sorted(default_files + [f"{GAME}.rush_dist.json", f"{GAME}.rush_dist.cdf.csv",
                                            f"{GAME}.rush_dist.summary.csv"])
    assert (tmp_path / "a" / f"{GAME}.sim100k.json").read_bytes() == (tmp_path / "b" / f"{GAME}.sim100k.json").read_bytes()
    meta = json.loads((tmp_path / "b" / f"{GAME}.rush_dist.json").read_text())
    assert meta["n_trials"] == 100 and meta["seed"] == 5 and meta["projection_ready"] is False


def test_sim100k_rush_dist_refused_run_writes_nothing(tmp_path, monkeypatch):
    from pipeline import phases as PH
    from pipeline import sim100k as S
    monkeypatch.setattr(S, "run", lambda g, p=None: (2, {"status": "REFUSED", "reasons": ["x"]}))
    monkeypatch.setattr(PH, "LEDGERS", tmp_path / "c")
    assert S.main(["--game", GAME, "--write", "--rush-dist"]) == 2
    assert not list((tmp_path / "c").glob("*rush_dist*"))


def test_rush_dist_requires_write():
    from pipeline import sim100k as S
    with pytest.raises(SystemExit):
        S.main(["--game", GAME, "--rush-dist"])


def test_module_is_offline_and_research_only():
    src = (ROOT / "pipeline" / "rush_dist.py").read_text()
    for bad in ("requests", "urllib", "the-odds-api", "ODDS_API", "projection_ready = True",
                "projection_ready=True"):
        assert bad not in src
