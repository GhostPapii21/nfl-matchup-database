"""Historical leakage audit: simv56 (calibration/simv56_pmodel.py + vendored engines calibration/simv56/engines).

Uses the committed as-of inputs only (nflverse 2026 W1-9 PBP pulled 2026-11-12, players_slim 2026-11-02 snapshot,
games.csv, sim_v*_backtest.csv). The vendored engines are imported read-only; nothing is written to the repo.
xfail tests document REAL findings (see docs/audits/historical_leakage_audit.md); do not weaken them to make them pass.
"""
from __future__ import annotations

import importlib
import inspect
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from calibration import simv56_pmodel as SM  # noqa: E402

ENGINE_DIR = ROOT / "calibration" / "simv56" / "engines"
BACKTEST_WEEKS = (4, 5, 6, 7)

pytestmark = pytest.mark.skipif(not SM.PBP_DEFAULT.exists() or not SM.PLAYERS_DEFAULT.exists(),
                                reason="committed simv56 as-of inputs missing")


@pytest.fixture(scope="module")
def games():
    g = pd.read_csv(SM.GAMES_CSV, usecols=["season", "week", "game_type", "gameday"])
    return g[(g.season == 2026) & (g.game_type == "REG")]


@pytest.fixture(scope="module")
def v6(tmp_path_factory):
    """Import the vendored cc_sim_v6 exactly as simv56_pmodel._worker does (CC_OPP=0.5, SIMV6_SRC symlink dir)."""
    SM.verify_engines()
    src = SM.make_src(tmp_path_factory.mktemp("simv56_src"))
    old = {k: os.environ.get(k) for k in ("CC_OPP", "CC_SRC", "SIMV6_SRC")}
    os.environ.update(CC_OPP=SM.OPP, CC_SRC=str(src), SIMV6_SRC=str(src))
    sys.path.insert(0, str(ENGINE_DIR))
    try:
        sys.modules.pop("cc_sim_v6", None)
        M = importlib.import_module("cc_sim_v6")
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    yield M
    sys.modules.pop("cc_sim_v6", None)


# ------------------------------------------------------------------ Q2 game-week timestamps
@pytest.mark.parametrize("week", range(4, 13))
def test_cutoff_is_not_after_first_kickoff_of_week(week, games):
    first = games[games.week == week].gameday.min()
    assert SM.cutoff_for_week(week) <= first


@pytest.mark.parametrize("week", range(4, 10))
def test_engine_sees_no_play_on_or_after_cutoff(week, v6):
    cut = SM.cutoff_for_week(week)
    E = v6.Engine(cutoff=cut, calib=None, n=10)
    assert len(E.p) > 0
    assert E.p.game_date.max() < cut
    assert int(E.p.week.max()) < week
    assert set(E.tg.game_id.str.slice(5, 7).astype(int)) <= set(range(1, week))


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (LOW, information loss not leakage): simv56_pmodel.py:58 CUTOFF_OVERRIDES={9:'2026-11-02'} cuts Week 9 "
    "inputs before the Week 8 Monday game (2026-11-02), so W9 p_model ignores a completed prior-week game while W4-8 "
    "and W10+ use every prior-week game. Inconsistent as-of rule across weeks."))
def test_cutoff_keeps_every_completed_prior_week_game(games):
    week = 9
    last_prev = games[games.week == week - 1].gameday.max()
    assert SM.cutoff_for_week(week) > last_prev


def test_calibration_refit_rows_strictly_before_target_week():
    """_worker: tr = bt[bt.week < min(W, 8)] must never include the target week or later."""
    for eng in ("sim_v6", "sim_v6_fix"):
        bt = pd.read_csv(ENGINE_DIR / f"{eng}_backtest.csv")
        assert len(bt) > 0   # note: sim_v6_fix_backtest.csv also holds Week 8 rows; the min(W, 8) rule never uses them
        for W in range(4, 13):
            tr = bt[bt.week < min(W, 8)]
            assert tr.empty or tr.week.max() < W


# ------------------------------------------------------------------ Q3/Q4 rolling + opponent adjustment invariance
def _leg(week):
    legs = pd.read_csv(ROOT / "calibration/tests/fixtures/simv56_phase4_w8_w9_legs.csv")
    r = legs[legs.week == week].iloc[0]
    return dict(player=r.player, gsis=r.gsis, team=r.team, opp=r.opp, market=r.market, spread=float(r.spread),
                rungs=[float(r.line)])


@pytest.mark.parametrize("week", [8, 9])
def test_future_plays_cannot_move_simulation(week, v6, monkeypatch):
    """Mutate every play on/after the cutoff (yards x10, all completions) and rebuild the engine: the leg's
    simulated distribution, rolling-3 weights and opponent factors must be bit-identical."""
    cut = SM.cutoff_for_week(week)
    leg = _leg(week)
    a, ia = v6.Engine(cutoff=cut, calib=None, n=2000).sim(leg)
    P = v6._P.copy()
    fut = P.game_date >= cut
    P.loc[fut, "rushing_yards"] = P.loc[fut, "rushing_yards"] * 10
    P.loc[fut, "receiving_yards"] = P.loc[fut, "receiving_yards"] * 10
    P.loc[fut, "complete_pass"] = 1
    monkeypatch.setattr(v6, "_P", P)
    b, ib = v6.Engine(cutoff=cut, calib=None, n=2000).sim(leg)
    assert a == b
    for k in ("w_tgt", "w_car", "A_ypt", "A_cr", "A_ypc", "raw_opp_ypt", "raw_opp_cr", "n_games"):
        if k in ia:
            assert ia[k] == ib[k], k


@pytest.mark.parametrize("week", [8, 9])
def test_opponent_factor_uses_only_pre_cutoff_games(week, v6):
    cut = SM.cutoff_for_week(week)
    E = v6.Engine(cutoff=cut, calib=None, n=10)
    leg = _leg(week)
    opp = v6.NV.get(leg["opp"], leg["opp"])
    o = E.pp[E.pp.defteam == opp]
    assert len(o) > 0 and o.game_date.max() < cut


# ------------------------------------------------------------------ Q5 roles / depth / injuries as of the game
def test_qb_starter_ignores_depth_snapshots_after_as_of():
    depth = pd.DataFrame([
        dict(dt="2026-10-01T00:00:00Z", team="AAA", player_name="Old Starter", gsis_id="Q1", pos_abb="QB", pos_rank=1),
        dict(dt="2026-10-01T00:00:00Z", team="AAA", player_name="Backup", gsis_id="Q2", pos_abb="QB", pos_rank=2),
        dict(dt="2026-10-20T00:00:00Z", team="AAA", player_name="Backup", gsis_id="Q2", pos_abb="QB", pos_rank=1)])
    inj = pd.DataFrame(columns=["week", "gsis_id", "report_status"])
    st = SM.qb_starters(depth, inj, 6, "2026-10-10T00:00:00Z", {})
    assert st.set_index("team").loc["AAA", "starter_gsis"] == "Q1"


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (MED): simv56_pmodel.py:556 `as_of = a.as_of or datetime.now(...)`. For a historical week the depth-chart "
    "gate defaults to TODAY's newest snapshot (simv56_pmodel.py:253,258), i.e. a post-game depth chart, unless the "
    "operator remembers --as-of. The default should be the week's cutoff/kickoff."))
def test_historical_run_defaults_as_of_to_kickoff_not_now():
    line = [l for l in inspect.getsource(SM.run_cli).splitlines() if l.strip().startswith("as_of =")][0]
    assert "datetime.now" not in line


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (MED): the committed nflverse injury file has no per-row publication timestamp (no date_modified / "
    "report_time). simv56_pmodel._week_inj (line 246) and opportunity_fit.status_map read the whole week's "
    "report_status, so 'as it stood before kickoff' cannot be verified for historical weeks."))
def test_injury_rows_carry_publication_timestamp():
    inj = pd.read_parquet(ROOT / "data/historical/nflverse/injuries_2026_pulled_20261113T0526Z.parquet")
    assert {"date_modified", "report_time", "published_utc"} & set(inj.columns)


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (LOW): the engines map name->gsis and position from players_slim_shared_src_20261102 (latest_team, "
    "position_group; cc_sim_v6.py:41,52-55). For Weeks 4-8 that snapshot post-dates the cutoff, so team membership "
    "used for name disambiguation is the Nov 2 roster, not the roster as of the historical game."))
def test_player_table_snapshot_predates_cutoff():
    m = re.search(r"(\d{8})", SM.PLAYERS_DEFAULT.name)
    snap = f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:]}"
    late = [w for w in (4, 5, 6, 7, 8) if snap > SM.cutoff_for_week(w)]
    assert not late, f"players snapshot {snap} is after the cutoff for weeks {late}"


# ------------------------------------------------------------------ Q6 evaluation population
@pytest.mark.xfail(strict=True, reason=(
    "FINDING (HIGH for calibration multipliers): cc_sim_v6.py:259-260 (same in cc_sim_v6_fix.py backtest_rows) "
    "`if q.empty: continue` drops every universe player with no play in week W (inactive, DNP AND active-but-zero-"
    "touch) from sim_v6_backtest.csv. The sim_v6 / sim_v6_fix multipliers simv56 refits from that file "
    "(simv56_pmodel.py:127-129) are fitted on survivors only."))
def test_backtest_universe_keeps_zero_stat_and_inactive_players(v6):
    bt = pd.read_csv(ENGINE_DIR / "sim_v6_backtest.csv")
    missing = []
    for W in BACKTEST_WEEKS:
        cut = v6._P[v6._P.week == W].game_date.min()
        E = v6.Engine(cutoff=cut, calib=None, n=10)
        PW = v6._P[v6._P.week == W]
        played = set(PW.posteam.dropna())
        parts = [E.p[["game_date", "posteam", f"{r}_player_id"]].rename(columns={f"{r}_player_id": "g"})
                 for r in ("receiver", "rusher", "passer")]
        last_team = pd.concat(parts).dropna().sort_values("game_date").groupby("g").posteam.last()
        have = set(zip(bt[bt.week == W].gsis, bt[bt.week == W].market))
        for g, mkt in v6.universe(E):
            appeared = ((PW.passer_player_id == g) | (PW.receiver_player_id == g) | (PW.rusher_player_id == g)).any()
            if not appeared and last_team.get(g) in played and (g, mkt) not in have:
                missing.append((W, g, mkt))
    assert not missing, f"{len(missing)} universe player-markets on teams that played were dropped, e.g. {missing[:5]}"


@pytest.mark.xfail(strict=True, reason=(
    "FINDING (LOW): cc_sim_v6.py:268 adds uniform(-0.5, 0.5) noise to every receptions ACTUAL before it is written to "
    "sim_v6_backtest.csv, so the stored labels are not the real outcomes; any later Brier / hit rate computed from "
    "that file is on perturbed labels."))
def test_backtest_actuals_are_real_counts():
    bt = pd.read_csv(ENGINE_DIR / "sim_v6_backtest.csv")
    rec = bt[bt.market == "rec"].actual
    assert len(rec) and np.allclose(rec, rec.round())


def test_ensemble_inner_join_drops_legs_silently():
    """simv56_pmodel.ensemble (line 233) inner-joins the three engines; a leg one engine errors on disappears.
    Documents current behaviour (callers must reconcile the population) so a change is noticed."""
    def frame(ps):
        return pd.DataFrame({"gsis": ["a", "b"][:len(ps)], "market": "rushyds", "line": 10.5,
                             "p_mc": ps, "p_bias": ps, "p_gr": ps})
    per = {"sim_v5": frame([0.4, 0.5]), "sim_v6": frame([0.4, 0.5]), "sim_v6_fix": frame([0.4])}
    out = SM.ensemble(per)
    assert list(out.gsis) == ["a"]
