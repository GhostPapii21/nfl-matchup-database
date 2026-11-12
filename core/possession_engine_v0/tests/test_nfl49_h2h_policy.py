"""NFL-49 A: head-to-head (offense vs this defense) conditioning is a configurable, default-off policy.

Before NFL-49, simulate_one forced h2h conditioning on, so for WAS@NYG (as of W10) 100% of snaps came from the
single W5 game. These tests pin: default off, legacy reproduces always-on, shrunk weight follows n/(n+k).
Research only, not validated.
"""
from __future__ import annotations
import copy
import json
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import simulate  # noqa: E402
from simulate import PlayCatalog, h2h_policy_from_cfg, H2H_SHRUNK_DEFAULTS  # noqa: E402
from state import GameState  # noqa: E402

REPO = HERE.parents[1]
PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
CFG = HERE / "config/was_nyg_2026-11-12_data_only_nfl43.json"


def _cfg(h2h=None):
    c = json.loads(CFG.read_text())
    c.pop("semantics", None)
    if h2h is not None:
        c["defense_interaction"]["h2h"] = h2h
    return c


def test_policy_from_cfg_default_off():
    assert h2h_policy_from_cfg({}) == {"mode": "off"}
    assert h2h_policy_from_cfg(_cfg()) == {"mode": "off"}
    assert h2h_policy_from_cfg(_cfg("legacy_always")) == {"mode": "legacy_always"}


def _toy_catalog():
    import pandas as pd
    rows = []
    for i in range(40):
        rows.append(dict(posteam="AAA", defteam="BBB" if i < 10 else "CCC", play_type="run", down=1, ydstogo=10,
                         yardline_100=60, yards_gained=99 if i < 10 else 1))
    return PlayCatalog(pd.DataFrame(rows), min_n=5)


def _state():
    st = GameState.new_game(home="BBB", away="AAA")
    st.possession, st.down, st.ydstogo, st.yardline_100 = "AAA", 1, 10, 60
    return st


def test_unknown_mode_rejected():
    with pytest.raises(ValueError):
        _toy_catalog().set_h2h_policy({"mode": "always_please"})


def test_off_never_samples_h2h():
    cat = _toy_catalog(); cat.set_h2h_policy({"mode": "off"})
    rng = np.random.default_rng(0); st = _state()
    tags = [cat.sample_snap(rng, st, False)[1] for _ in range(300)]
    assert not any(t.startswith("DEF_COND") for t in tags)


def test_legacy_always_samples_h2h_every_snap():
    cat = _toy_catalog(); cat.set_h2h_policy({"mode": "legacy_always"})
    rng = np.random.default_rng(0); st = _state()
    tags = [cat.sample_snap(rng, st, False)[1] for _ in range(300)]
    assert all(t.startswith("DEF_COND") for t in tags)


def test_shrunk_weight_formula_and_rate():
    cat = _toy_catalog(); cat.set_h2h_policy({"mode": "shrunk", "k": 30, "max_weight": 0.5})
    assert cat.h2h_weight(10) == pytest.approx(0.5 * 10 / 40)
    assert cat.h2h_weight(4) == 0.0  # below min_n
    rng = np.random.default_rng(1); st = _state()
    n = 4000
    hits = sum(cat.sample_snap(rng, st, False)[1].startswith("DEF_COND") for _ in range(n))
    assert abs(hits / n - 0.125) < 0.02
    d = _toy_catalog().set_h2h_policy({"mode": "shrunk"})
    assert d["k"] == H2H_SHRUNK_DEFAULTS["k"] and d["max_weight"] == H2H_SHRUNK_DEFAULTS["max_weight"]


def test_legacy_switch_maps_to_policy():
    cat = _toy_catalog()
    cat.enable_defense_conditioning(True); assert cat.h2h_policy["mode"] == "legacy_always"
    cat.enable_defense_conditioning(False); assert cat.h2h_policy["mode"] == "off"


@pytest.mark.skipif(not PBP.exists(), reason="committed W1-9 PBP missing")
def test_real_was_nyg_default_has_no_h2h_snaps_and_legacy_is_100pct():
    off = simulate.simulate_games(_cfg(), pbp_path=str(PBP), n=40, seed=7)
    assert off["evidence_summary"]["defense_cond_flag_events"] == 0
    assert off["effects_provenance"]["defense_interaction"]["h2h"] == {"mode": "off"}
    leg = simulate.simulate_games(_cfg("legacy_always"), pbp_path=str(PBP), n=40, seed=7)
    # every offensive snap is h2h-tagged under legacy for WAS@NYG (single W5 meeting has >= min_n per down)
    snaps = leg["evidence_summary"]["defense_cond_flag_events"]
    assert snaps > 40 * 80
    sh = simulate.simulate_games(_cfg({"mode": "shrunk"}), pbp_path=str(PBP), n=40, seed=7)
    assert 0 < sh["evidence_summary"]["defense_cond_flag_events"] < snaps * 0.25
