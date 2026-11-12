"""WP1 (NFL-75): pace / penalty clock.

The engine charged a flat 4 s per no-play foul (semantics.NO_PLAY_CLOCK_SEC) and lost the seconds nflverse books on
rows it never simulates (timeouts ~12.8 s each), so simulated teams ran ~4.5 snaps a game too many (67.0 vs 62.5,
calibration/outputs/diag_total_w09_off_default.json). Fix: charge the as-of MEAN clock of no-play penalty rows, and
attribute unmodeled-row seconds to the modeled play before them when the mean clock is built. accounting="pre_wp12"
and "legacy" reproduce the old behaviour. Mechanics only: nothing here is fitted to scores or lines.
Research only, not validated."""
from __future__ import annotations
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import simulate  # noqa: E402
from simulate import (PlayCatalog, accounting_from_cfg, no_play_clock_sec, _no_play_penalty,  # noqa: E402
                      ACCOUNTING_DEFAULTS, ACCOUNTING_LEGACY, ACCOUNTING_PRE_WP12)
from semantics import NO_PLAY_CLOCK_SEC, PenaltyDraw  # noqa: E402
from state import GameState  # noqa: E402

REPO = HERE.parents[1]
PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
CFG = HERE / "config/was_nyg_2026-11-12_data_only_nfl43.json"


def _toy(n_cycles=40):
    """One quarter: pass (20 s) -> no-play penalty (11 s) -> run (30 s) -> timeout (12 s) -> repeat."""
    rows, t, pid = [], 900, 0
    for _ in range(n_cycles):
        for pt, pen, to, dt in (("pass", 0, 0, 20), ("no_play", 1, 0, 11), ("run", 0, 0, 30), ("no_play", 0, 1, 12)):
            rows.append(dict(game_id="g", play_id=pid, qtr=1, play_type=pt, penalty=pen, timeout=to,
                             game_seconds_remaining=t))
            t -= dt; pid += 1
    rows.append(dict(game_id="g", play_id=pid, qtr=1, play_type="punt", penalty=0, timeout=0, game_seconds_remaining=t))
    return pd.DataFrame(rows)


def test_accounting_keys_defaults_legacy_and_pre_wp12():
    assert accounting_from_cfg({})["no_play_clock"] == "asof_mean"
    assert accounting_from_cfg({})["unmodeled_row_clock"] == "attribute_to_prior_play"
    assert accounting_from_cfg({"accounting": "pre_wp12"}) == ACCOUNTING_PRE_WP12
    assert ACCOUNTING_PRE_WP12["no_play_clock"] == "flat_4s" and ACCOUNTING_PRE_WP12["unmodeled_row_clock"] == "drop"
    assert accounting_from_cfg({"accounting": "legacy"}) == ACCOUNTING_LEGACY
    # median clock has no no-play / attribution path: forced back to the old behaviour
    a = accounting_from_cfg({"accounting": {"clock": "legacy_median"}})
    assert a["no_play_clock"] == "flat_4s" and a["unmodeled_row_clock"] == "drop"
    with pytest.raises(ValueError):
        accounting_from_cfg({"accounting": {"no_play_clock": "ten"}})
    with pytest.raises(ValueError):
        accounting_from_cfg({"accounting": {"unmodeled_row_clock": "x"}})


def test_no_play_penalty_mean_and_timeout_attribution_toy():
    old = PlayCatalog.build_empirical_clock(_toy(), stat="mean")
    new = PlayCatalog.build_empirical_clock(_toy(), stat="mean", skip_unmodeled_rows=True)
    assert old["no_play_penalty"] == pytest.approx(11.0) and new["no_play_penalty"] == pytest.approx(11.0)
    assert old["run"] == pytest.approx(30.0), "without attribution the 12 s timeout is lost"
    assert new["run"] == pytest.approx(42.0), "timeout seconds belong to the run before it"
    assert new["pass"] == pytest.approx(20.0)
    assert new["skip_unmodeled_rows"] is True and old["skip_unmodeled_rows"] is False
    # conservation: modeled clock events sum to the whole quarter that elapsed
    cycles = 40
    elapsed = cycles * (20 + 11 + 30 + 12)
    assert cycles * (new["pass"] + new["no_play_penalty"] + new["run"]) == pytest.approx(elapsed)
    assert cycles * (old["pass"] + old["no_play_penalty"] + old["run"]) < elapsed


def test_no_play_penalty_needs_30_rows_else_flat_4s():
    m = PlayCatalog.build_empirical_clock(_toy(n_cycles=10), stat="mean", skip_unmodeled_rows=True)
    assert "no_play_penalty" not in m

    class C:
        clock_map = {k: v for k, v in m.items() if k not in ("source", "skip_unmodeled_rows")}
    assert no_play_clock_sec(C(), ACCOUNTING_DEFAULTS) == NO_PLAY_CLOCK_SEC == 4


def test_no_play_clock_sec_rounding_and_modes():
    class C:
        clock_map = {"no_play_penalty": 11.33}
    assert no_play_clock_sec(C(), ACCOUNTING_DEFAULTS) == 11
    C.clock_map = {"no_play_penalty": 11.6}
    assert no_play_clock_sec(C(), ACCOUNTING_DEFAULTS) == 12
    assert no_play_clock_sec(C(), ACCOUNTING_PRE_WP12) == 4
    assert no_play_clock_sec(C(), ACCOUNTING_LEGACY) == 4
    C.clock_map = {"no_play_penalty": float("nan")}
    assert no_play_clock_sec(C(), ACCOUNTING_DEFAULTS) == 4


def _st(secs):
    st = GameState.new_game(home="NYG", away="WAS")
    st.possession, st.yardline_100, st.down, st.ydstogo, st.game_seconds_remaining = "WAS", 50, 1, 10, secs
    return st


def test_no_play_penalty_charges_given_clock_and_keeps_untimed_down():
    st = _st(300)
    _no_play_penalty(st, PenaltyDraw("offense", "WAS", 5, True, False, "False Start"), clock_sec=11)
    assert st.game_seconds_remaining == 289
    st = _st(300)
    _no_play_penalty(st, PenaltyDraw("offense", "WAS", 5, True, False, "False Start"))
    assert st.game_seconds_remaining == 296, "default stays the flat 4 s for callers that pass nothing"
    st = _st(8)
    _no_play_penalty(st, PenaltyDraw("defense", "NYG", 5, True, False, "Offside"), clock_sec=11)
    assert st.game_seconds_remaining == 1 and st.events[-1]["type"] == "untimed_down"


needs_pbp = pytest.mark.skipif(not PBP.exists(), reason="committed nflverse W1-9 PBP not present")


@needs_pbp
def test_real_pbp_no_play_penalty_clock_is_about_11s_not_4():
    df = pd.read_parquet(PBP)
    asof = df[df["week"] <= 8]
    m = PlayCatalog.build_empirical_clock(asof, stat="mean", skip_unmodeled_rows=True)
    assert m["no_play_penalty_n"] >= 500
    assert 9.0 <= m["no_play_penalty"] <= 14.0
    old = PlayCatalog.build_empirical_clock(asof, stat="mean")
    assert m["run"] > old["run"] and m["pass"] >= old["pass"], "timeout seconds now land on the prior play"


@needs_pbp
def test_real_pbp_sim_pace_matches_actual_snaps_per_team_game():
    """WAS@NYG lock config (history W1-9): simulated snaps per team-game vs the same teams' actual W1-9 rate.
    Pre-fix runs ~3 snaps fast on this pair; the fixed clock must land within 1.5 snaps of actual."""
    from pbp_filter import load_team_history
    cfg0 = json.loads(CFG.read_text())
    cfg0.setdefault("defense_interaction", {})["h2h"] = "off"
    wk = cfg0["history"]["weeks_inclusive"]
    h = load_team_history(str(PBP), teams=cfg0["history"]["teams"], season=cfg0["history"]["season"], weeks=(wk[0], wk[-1]))
    p = pd.read_parquet(PBP)
    x = p[p["posteam"].isin(cfg0["history"]["teams"]) & p["week"].between(wk[0], wk[-1])]
    tg = x.groupby("posteam")["game_id"].nunique().sum()
    actual = len(x[x["play_type"].isin(["pass", "run"]) & x["down"].notna()]) / tg  # sim pool excludes kneels/spikes
    res = {}
    for name, acc in (("pre", "pre_wp12"), ("fixed", None)):
        cfg = json.loads(json.dumps(cfg0))
        cfg.pop("accounting", None)
        if acc:
            cfg["accounting"] = acc
        cat, _ = simulate.build_catalog(h["df"], cfg, games_df=h.get("games_df"))
        simulate.attach_semantics(cat, cfg, str(PBP))
        rng = np.random.default_rng(20261112)
        snaps = [sum(e["type"] == "snap" for e in simulate.simulate_one(h["df"], cat, cfg, rng).events) / 2
                 for _ in range(120)]
        res[name] = float(np.mean(snaps))
    assert res["pre"] - actual > 2.0, res
    assert abs(res["fixed"] - actual) < 1.5, (res, actual)


@needs_pbp
def test_real_pbp_clock_window_loses_under_0_2pct_of_same_quarter_seconds():
    """Review finding (codex, 2026-11-12): merging timeout seconds into the prior play and then applying the
    [0, 60] s window drops merged intervals > 60 s. Bound that loss instead of claiming exact conservation."""
    p = pd.read_parquet(PBP)
    d = p.sort_values(["game_id", "play_id"])
    is_np = d["play_type"] == "no_play"
    d = d[~(is_np & (d["penalty"].fillna(0) != 1))].copy()
    d["_d"] = d["game_seconds_remaining"] - d.groupby("game_id")["game_seconds_remaining"].shift(-1)
    sq = d.groupby("game_id")["qtr"].shift(-1) == d["qtr"]
    raw = d.loc[sq, "_d"].sum()
    kept = d.loc[sq & d["_d"].between(0, 60), "_d"].sum()
    assert 0 <= raw - kept < 0.002 * raw, (raw, kept)


CLOCK_ONLY = {"no_play_clock": "asof_mean", "unmodeled_row_clock": "attribute_to_prior_play",
              "goal_line_censoring": "truncate"}


@needs_pbp
def test_real_pbp_wp1_alone_fixes_pace_with_wp2_off():
    """Isolate WP1: the clock fix with the goal-line fix OFF must already remove most of the pace gap."""
    from pbp_filter import load_team_history
    cfg0 = json.loads(CFG.read_text())
    cfg0.setdefault("defense_interaction", {})["h2h"] = "off"
    wk = cfg0["history"]["weeks_inclusive"]
    h = load_team_history(str(PBP), teams=cfg0["history"]["teams"], season=cfg0["history"]["season"], weeks=(wk[0], wk[-1]))
    p = pd.read_parquet(PBP)
    x = p[p["posteam"].isin(cfg0["history"]["teams"]) & p["week"].between(wk[0], wk[-1])]
    actual = len(x[x["play_type"].isin(["pass", "run"]) & x["down"].notna()]) / x.groupby("posteam")["game_id"].nunique().sum()
    cfg = json.loads(json.dumps(cfg0))
    cfg["accounting"] = CLOCK_ONLY
    cat, prov = simulate.build_catalog(h["df"], cfg, games_df=h.get("games_df"))
    assert prov["accounting"]["goal_line_censoring"] == "truncate"
    simulate.attach_semantics(cat, cfg, str(PBP))
    rng = np.random.default_rng(7)
    snaps = [sum(e["type"] == "snap" for e in simulate.simulate_one(h["df"], cat, cfg, rng).events) / 2 for _ in range(120)]
    assert abs(float(np.mean(snaps)) - actual) < 1.5, (np.mean(snaps), actual)
    assert 10 <= simulate.no_play_clock_sec(cat, prov["accounting"]) <= 13


@needs_pbp
def test_pre_wp12_reproduces_main_9beb9b0_bit_for_bit():
    """Golden values computed 2026-11-12 ~6:25 PM ET on main 9beb9b0 (engine tree 72f1116) with the same call:
    WAS@NYG lock config, h2h off, n=60, seed 20261112. accounting="pre_wp12" must reproduce them exactly
    (same RNG stream, same scores), so the before/after comparison is clean."""
    import hashlib
    cfg = json.loads(CFG.read_text())
    cfg.setdefault("defense_interaction", {})["h2h"] = "off"
    cfg["accounting"] = "pre_wp12"
    o = simulate.simulate_games(cfg, pbp_path=str(PBP), n=60, seed=20261112)
    h, a = o["arrays"]["fg_home"].astype(int), o["arrays"]["fg_away"].astype(int)
    assert (int(h.sum()), int(a.sum())) == (1220, 1356)
    assert hashlib.sha256(np.stack([h, a]).tobytes()).hexdigest()[:16] == "fa3bb9cce9015d75"


@needs_pbp
@pytest.mark.parametrize("order", [("default", "pre_wp12"), ("pre_wp12", "default")])
def test_reused_catalog_rebuilds_clock_when_accounting_changes(order):
    """Review finding (codex pass 2): a catalog reused under different clock accounting must not keep the first
    run's map. Each run must see exactly the map a fresh catalog would build."""
    from pbp_filter import load_team_history
    cfg0 = json.loads(CFG.read_text())
    cfg0.setdefault("defense_interaction", {})["h2h"] = "off"
    wk = cfg0["history"]["weeks_inclusive"]
    h = load_team_history(str(PBP), teams=cfg0["history"]["teams"], season=cfg0["history"]["season"], weeks=(wk[0], wk[-1]))

    def cfg_for(name):
        c = json.loads(json.dumps(cfg0))
        c.pop("accounting", None)
        if name == "pre_wp12":
            c["accounting"] = "pre_wp12"
        return c

    fresh = {}
    for name in set(order):
        cat, _ = simulate.build_catalog(h["df"], cfg_for(name), games_df=h.get("games_df"))
        simulate.simulate_one(h["df"], cat, cfg_for(name), np.random.default_rng(0))
        fresh[name] = dict(cat.clock_map)
    assert fresh["default"]["run"] != fresh["pre_wp12"]["run"]
    cat, _ = simulate.build_catalog(h["df"], cfg_for(order[0]), games_df=h.get("games_df"))
    for name in order:
        simulate.simulate_one(h["df"], cat, cfg_for(name), np.random.default_rng(0))
        assert dict(cat.clock_map) == fresh[name], name
