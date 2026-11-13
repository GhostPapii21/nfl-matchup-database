"""NFL-75 Phase 2b (Ghost6 review item 1): depth-chart point-in-time cutoff and training-leakage guards.

Cutoff rule: a game uses the latest depth-chart snapshot with dt STRICTLY before 04:00 UTC on the game day (before
midnight ET of game day); a snapshot stamped exactly at the cutoff or later is never used; no snapshot before the
cutoff = unknown (None), never a later one. Leakage: every Phase 2b fitter reads only data before the eval week.
Data-dependent tests skip when the uncommitted 2025 PBP / players table are absent (as test_opportunity_fit.py)."""
from __future__ import annotations
import json
import re

import pandas as pd
import pytest

from calibration import opportunity_fit as F
from calibration import opportunity_intcap as I
from calibration import opportunity_backtest as BT

needs_data = pytest.mark.skipif(not (F.SOURCES["pbp_2025"]["path"].exists() and F.SOURCES["players"]["path"].exists()),
                                reason="uncommitted nflverse 2025 PBP / players table missing")
GD = "2026-11-12"  # synthetic game day


def _snap(dt, rows):
    return [{"season": 2026, "team": "AAA", "dt": dt, "pos_abb": p, "pos_rank": r, "gsis_id": g, "player_name": g}
            for p, r, g in rows]


@pytest.fixture
def synthetic(monkeypatch):
    rows = (_snap("2026-11-10T12:00:00Z", [("WR", 1, "old1"), ("WR", 2, "x")])
            + _snap("2026-11-12T03:59:59Z", [("WR", 1, "pre"), ("WR", 2, "x"), ("WR", 3, "pre")])  # dup id: first row
            + _snap("2026-11-12T04:00:00Z", [("WR", 1, "at_cutoff")])
            + _snap("2026-11-12T18:00:00Z", [("WR", 1, "gameday")]))
    d = pd.DataFrame(rows)
    q = d[d["pos_rank"] == 1].rename(columns={})[["season", "team", "dt", "gsis_id", "player_name"]]
    monkeypatch.setattr(F, "_depth_skill", lambda: {(2026, "AAA"): d})
    monkeypatch.setattr(F, "_depth", lambda: {(2026, "AAA"): q.sort_values("dt")})
    monkeypatch.setattr(F, "_gamedays", lambda: {(2026, 10, "AAA"): GD, (2026, 11, "AAA"): "2026-11-10"})
    F.depth_skill.cache_clear()
    yield d
    F.depth_skill.cache_clear()


def test_skill_cutoff_is_latest_snapshot_strictly_before_04utc(synthetic):
    ch = F.depth_skill(2026, "AAA", 10)
    assert ch == {"pre": ("WR", 1), "x": ("WR", 2)}  # not at_cutoff (== 04:00Z), not gameday, not the older snapshot


def test_skill_unknown_when_no_snapshot_before_cutoff(synthetic):
    assert F.depth_skill(2026, "AAA", 11) is None  # game day 2026-11-10: only snapshots at/after 12:00Z exist
    assert F.depth_skill(2026, "BBB", 10) is None  # no chart for the team
    assert F.depth_skill(2026, "AAA", 12) is None  # no game day


def test_qb1_cutoff_matches(synthetic):
    assert F.depth_qb1(2026, "AAA", 10) == "pre"
    assert F.depth_qb1(2026, "AAA", 11) is None


def test_committed_snapshot_times_are_iso_utc():
    """The cutoff is a string comparison, valid only for fixed-width ISO-8601 UTC stamps."""
    pat = r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$"
    d = pd.read_csv(F.SOURCES["depth_skill"]["path"], usecols=["dt"])
    q = pd.read_csv(F.SOURCES["depth_qb1"]["path"], usecols=["dt"])
    assert d["dt"].str.match(pat).all() and q["dt"].str.match(pat).all()


def test_committed_was_week10_chart_is_point_in_time():
    gd = F._gamedays()[(2026, 10, "WAS")]
    d = pd.read_csv(F.SOURCES["depth_skill"]["path"], dtype={"gsis_id": str})
    d = d[(d["season"] == 2026) & (d["team"] == "WAS")]
    before = d[d["dt"] < f"{gd}T04:00:00Z"]
    last = before[before["dt"] == before["dt"].max()]
    F.depth_skill.cache_clear()
    ch = F.depth_skill(2026, "WAS", 10)
    assert set(ch) == set(last["gsis_id"].dropna())
    assert before["dt"].max() < f"{gd}T04:00:00Z" <= d[d["dt"] >= f"{gd}T04:00:00Z"]["dt"].min()


# ------------------------------------------------------------------ leakage
def test_train_set_guard_raises_on_eval_week_rows(monkeypatch):
    def fake(season, team, week, slot):
        return {"season": season, "team": team, "week": week, "weeks": [week], "actual": {"total": 1}}
    monkeypatch.setattr(F, "_season_tables", lambda s: (None, {"AAA": [3, 4, 5, 6]}))
    monkeypatch.setattr(F, "team_game_inputs", fake)
    assert max(x["week"] for x in F.train_set(2026, 6, "carry", seasons=()) ) == 5
    monkeypatch.setattr(F, "team_game_inputs",
                        lambda s, t, w, sl: {**fake(s, t, w, sl), "weeks": [w, 6]})  # history reaching week 6
    with pytest.raises(RuntimeError, match="eval week"):
        F.train_set(2026, 6, "carry", seasons=())


@needs_data
@pytest.mark.parametrize("w", [4, 9])
def test_fitter_inputs_stop_before_eval_week(w):
    for slot in ("carry", "target"):
        tr = F.train_set(2026, w, slot)
        cur = [x for x in tr if x["season"] == 2026]
        assert cur and max(x["week"] for x in cur) < w and max(max(x["weeks"]) for x in cur) < w
    rows = F.lik_rows(2026, w)
    assert rows[rows["season"] == 2026]["week"].max() < w
    tr = I.train_rows(2026, w)
    assert all(r[1] < w for r in tr if r[0] == 2026)  # W4: no 2026 rows at all (training weeks start at 4)
    assert all(r[0] < 2026 or r[1] < w for r in tr)


@needs_data
def test_intcap_league_rate_uses_prior_weeks_only():
    lr = I.league_rate(2026, 6)
    assert lr["weeks"] == [1, 5]
    tw = I._team_week(2026)
    d = tw[tw["week"] < 6]
    assert lr["att"] == int(d["att"].sum()) and lr["int"] == int(d["int"].sum())


def test_frozen_phase2b_files_are_walk_forward():
    run = F.ROOT / "research/runs/2026-11-13_opportunity_phase2b"
    for f in sorted((run / "params").glob("params_2026_w*.json")):
        p = json.loads(f.read_text())
        assert p["data_max_week_used"] == {"season": 2026, "week": p["eval_week"] - 1}
        assert p["phase"] == "2b"
    for f in sorted((run / "int_pool").glob("int_pool_2026_w*.json")):
        s = json.loads(f.read_text())
        w = s["meta"]["eval_week"]
        assert s["meta"]["league"]["weeks"] == [1, w - 1] and f"weeks 4..{w - 1}" in s["meta"]["fitted_on"]


def test_phase2b_backtest_and_fitters_refuse_holdout(monkeypatch):
    monkeypatch.setattr(BT, "OUT", BT.OUT)  # main() may retarget OUT; restore after
    for v in ("phase2b", "phase2b_noint"):
        with pytest.raises(SystemExit):
            BT.main(["--variant", v, "--weeks", "10"])
        with pytest.raises(SystemExit):
            BT.main(["--variant", v, "--weeks", "9", "--refit"])
    from calibration import opportunity_fit2b as F2B
    with pytest.raises(SystemExit):
        F2B.main(["11"])
    with pytest.raises(SystemExit):
        I.main(["11"])
