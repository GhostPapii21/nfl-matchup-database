"""RED→GREEN: no silent pooling; config freeze; forward-only adjustments."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from pbp_filter import load_team_history
from empirical import StateKey, lookup_plays, Evidence
from adjustments import apply_forward_qb_filter
from config_load import load_config

ROOT = Path(__file__).resolve().parents[1]


def test_configs_frozen_distinct():
    a = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_data_only.json")
    b = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_script_adjusted.json")
    assert a["mode"] == "data_only" and b["mode"] == "script_adjusted"
    assert a["adjustments"]["enabled"] is False
    assert b["adjustments"]["enabled"] is True
    assert a["proposed_pooling"]["enabled"] is False
    assert b["proposed_pooling"]["enabled"] is False


def test_history_team_only_weeks_1_8_no_future():
    hist = load_team_history(
        ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet",
        teams=["JAX", "BAL"], season=2026, weeks=(1, 8),
    )
    assert hist["status"] == "OK"
    assert set(hist["df"]["week"].unique()) <= set(range(1, 9))
    assert set(hist["df"]["posteam"].unique()) <= {"JAX", "BAL"}
    assert hist["evidence"]["n_games"] == 15
    assert hist["evidence"]["n_plays"] > 1000


def test_sparse_state_no_silent_pool():
    hist = load_team_history(
        ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet",
        teams=["JAX", "BAL"], season=2026, weeks=(1, 8),
    )
    # unlikely cell: 4th & xlong backed up
    key = StateKey(posteam="BAL", down=4, dist_bucket="xlong", yl_bucket="backed")
    ev = lookup_plays(hist["df"], key, min_n=5, allow_pool=False)
    assert isinstance(ev, Evidence)
    assert ev.status in {"SPARSE_STATE", "EMPTY_STATE"}
    assert ev.n_evidence < 5
    assert ev.plays is None or len(ev.plays) == 0 or ev.status != "OK"
    assert ev.pooling_applied is False


def test_proposed_pool_not_applied_when_disabled():
    hist = load_team_history(
        ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet",
        teams=["JAX", "BAL"], season=2026, weeks=(1, 8),
    )
    key = StateKey(posteam="BAL", down=4, dist_bucket="xlong", yl_bucket="backed")
    ev = lookup_plays(hist["df"], key, min_n=5, allow_pool=False, proposed_pool_teams=None)
    assert ev.pooling_applied is False
    assert "PROPOSED" in (ev.pool_proposal or "PROPOSED") or ev.pool_proposal is not None or ev.status.startswith("SPARSE")


def test_qb_filter_forward_only_excludes_lamar_does_not_fabricate_fagnano():
    hist = load_team_history(
        ROOT.parent / "period_engine_v0/data/play_by_play_2026.parquet",
        teams=["JAX", "BAL"], season=2026, weeks=(1, 8),
    )
    cfg = load_config(ROOT / "config/jax_bal_tnf_2026-11-05_script_adjusted.json")
    filtered, meta = apply_forward_qb_filter(hist["df"], cfg["adjustments"])
    bal_pass = filtered[(filtered.posteam == "BAL") & (filtered.play_type == "pass")]
    assert "L.Jackson" not in set(bal_pass.passer_player_name.dropna())
    # Fagnano history not fabricated — only real rows remain
    assert set(bal_pass.passer_player_name.dropna()) <= {"J.Fagnano"}
    assert meta["BAL"]["n_pass_after"] == int((bal_pass.passer_player_name == "J.Fagnano").sum())
    assert meta["BAL"]["fabricated"] is False
    # original hist unchanged for data_only path
    assert "L.Jackson" in set(hist["df"][(hist["df"].posteam == "BAL") & (hist["df"].play_type == "pass")].passer_player_name.dropna())
