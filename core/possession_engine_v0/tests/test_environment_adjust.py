"""NFL-75 item 6: opt-in weather / injury adjustments (environment_adjust.py). Default off is bit-identical to main.
Research only, not validated."""
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
REPO = HERE.parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
import simulate  # noqa: E402
import environment_adjust as ea  # noqa: E402
from calibration.common import make_cfg  # noqa: E402

PBP = REPO / "data/historical/nflverse/pbp_2026_w1_9_pulled_20261112T1116ET.parquet"
TRAIN = "research/weather/rain_effects_train_2018_2025.json"
needs_pbp = pytest.mark.skipif(not PBP.exists(), reason="committed nflverse W1-9 PBP missing")

# Golden values computed 2026-11-13 ~12:40 AM ET on main 3dad900 BEFORE this change (n=60, seed 20261112, h2h off).
# Unchanged on main 6bc0c54 (PR #36 player box recorder adds output, not RNG draws); re-checked after the rebase.
GOLDEN = {("NYG", "WAS", 10): (1152, 1401, "18984268e877d4cb"), ("BAL", "JAX", 9): (1295, 1558, "a59ceb83b0aec394"),
          ("PIT", "IND", 5): (1099, 1272, "4869e54224982391"), ("NYJ", "CLE", 5): (1121, 1039, "83f0455a297eb30a")}
EVID = {"source": "test", "asof": "test"}


def _h(o):
    h, a = o["arrays"]["fg_home"].astype(int), o["arrays"]["fg_away"].astype(int)
    return int(h.sum()), int(a.sum()), hashlib.sha256(np.stack([h, a]).tobytes()).hexdigest()[:16]


@needs_pbp
@pytest.mark.parametrize("key", list(GOLDEN))
@pytest.mark.parametrize("variant", ["absent", "explicit_off"])
def test_off_reproduces_main_3dad900_bit_for_bit(key, variant):
    cfg = make_cfg(*key, h2h="off")
    if variant == "explicit_off":
        cfg["environment"] = {"weather": {"mode": "off"}}
        cfg["availability"] = {"mode": "off"}
    o = simulate.simulate_games(cfg, pbp_path=str(PBP), n=60, seed=20261112)
    assert _h(o) == GOLDEN[key]
    assert "environment_adjustments" not in o


def test_modes_and_unknown_refused():
    assert ea.weather_mode({}) == "off" and ea.availability_mode({}) == "off"
    assert ea.weather_mode({"environment": {"weather": None}}) == "off"
    with pytest.raises(ValueError):
        ea.weather_mode({"environment": {"weather": {"mode": "tuned"}}})
    with pytest.raises(ValueError):
        ea.availability_mode({"availability": {"mode": "guess"}})


def test_no_committed_config_enables_them():
    for p in sorted((HERE / "config").glob("*.json")):
        c = json.loads(p.read_text())
        assert ea.weather_mode(c) == "off" and ea.availability_mode(c) == "off", p.name


def _wx_cfg(**kw):
    cfg = make_cfg("NYJ", "CLE", 5, h2h="off")
    cfg["environment"] = {"weather": {"mode": "rain_wind_v1", "rain": 1.0, "wind_mph": 20.0, "effects_path": TRAIN,
                                      "evidence": EVID, **kw}}
    return cfg


@needs_pbp
def test_enabled_needs_research_flag_cap_and_evidence():
    with pytest.raises(ValueError, match="research only"):
        simulate.simulate_games(_wx_cfg(), pbp_path=str(PBP), n=2, seed=1)
    with pytest.raises(ValueError, match="capped"):
        simulate.simulate_games(_wx_cfg(), pbp_path=str(PBP), n=simulate.RESEARCH_MAX_N + 1, seed=1,
                                research_unaccepted=("weather_rain_wind_v1",))
    with pytest.raises(ValueError, match="evidence"):
        simulate.simulate_games(_wx_cfg(evidence={}), pbp_path=str(PBP), n=2, seed=1,
                                research_unaccepted=("weather_rain_wind_v1",))


def test_train_effects_exclude_2026():
    fit = json.loads((REPO / TRAIN).read_text())
    assert max(fit["seasons"]) <= 2025


def test_build_weather_uses_only_clear_coefficients(tmp_path, monkeypatch):
    fake = {"seasons": [2018], "pooled": {
        "completion_pct": {"any_rain": {"pct_of_baseline": -0.10, "clear": True}, "wind10": {"pct_of_baseline": -0.05, "clear": False}},
        "yards_per_completion": {"any_rain": {"pct_of_baseline": -0.20, "clear": True}, "wind10": {"pct_of_baseline": -0.04, "clear": True}}}}
    p = tmp_path / "fx.json"; p.write_text(json.dumps(fake))
    monkeypatch.setattr(ea, "REPO", tmp_path)
    wx = ea.build_weather({"environment": {"weather": {"mode": "rain_wind_v1", "rain": 1.0, "wind_mph": 30,
                                                       "effects_path": "fx.json", "evidence": EVID}}})
    assert wx["W"] == 2.0
    assert wx["keep_completion"] == pytest.approx(0.90)          # wind term not clear -> 0
    assert wx["ypc_factor"] == pytest.approx(1 - 0.20 - 0.08)


def test_apply_weather_row_mechanics():
    run = pd.Series({"play_type": "run", "yards_gained": 5.0})
    rng = np.random.default_rng(0); s0 = rng.bit_generator.state
    assert ea.apply_weather_row(rng, {"keep_completion": 0.0, "ypc_factor": 0.5}, run) is run
    assert rng.bit_generator.state == s0                                   # no draw for non-completions
    inc = pd.Series({"play_type": "pass", "complete_pass": 0, "sack": 0, "yards_gained": 0.0})
    assert ea.apply_weather_row(rng, {"keep_completion": 0.0, "ypc_factor": 0.5}, inc) is inc
    comp = pd.Series({"play_type": "pass", "complete_pass": 1, "sack": 0, "yards_gained": 21.0, "fumble_lost": 1,
                      "incomplete_pass": 0})
    r = ea.apply_weather_row(rng, {"keep_completion": 0.0, "ypc_factor": 1.0}, comp)
    assert r["complete_pass"] == 0 and r["yards_gained"] == 0 and r["fumble_lost"] == 0
    r = ea.apply_weather_row(rng, {"keep_completion": 1.0, "ypc_factor": 0.5}, comp)
    assert r["complete_pass"] == 1 and r["yards_gained"] == 10.0 and comp["yards_gained"] == 21.0  # copy, not mutate


def _hist():
    rows = []
    for i in range(80):
        rows.append({"posteam": "AAA", "play_type": "pass", "passer_player_id": "qb1" if i < 70 else "qb2",
                     "receiver_player_id": "wr1" if i % 2 else "wr2", "rusher_player_id": None})
    for i in range(20):
        rows.append({"posteam": "AAA", "play_type": "run", "passer_player_id": None, "receiver_player_id": None,
                     "rusher_player_id": "rb1"})
    rows.append({"posteam": "BBB", "play_type": "pass", "passer_player_id": "x", "receiver_player_id": "wr1",
                 "rusher_player_id": None})
    return pd.DataFrame(rows)


def test_availability_removes_listed_rows_only_for_that_team():
    cfg = {"availability": {"mode": "injury_report_out_v1", "out_player_ids": {"AAA": ["wr1", "rb1"]}, "evidence": EVID}}
    out, meta = ea.apply_availability(_hist(), cfg)
    assert meta["teams"]["AAA"]["rows_removed"] == 60
    assert not ((out.posteam == "AAA") & out.receiver_player_id.eq("wr1")).any()
    assert ((out.posteam == "BBB") & out.receiver_player_id.eq("wr1")).sum() == 1   # other team untouched


def test_availability_keeps_qb_rows_when_backup_history_sparse():
    cfg = {"availability": {"mode": "injury_report_out_v1", "out_player_ids": {"AAA": ["qb1"]}, "evidence": EVID}}
    out, meta = ea.apply_availability(_hist(), cfg)
    assert meta["teams"]["AAA"]["passer_rows_kept_sparse"] is True and meta["teams"]["AAA"]["rows_removed"] == 0
    with pytest.raises(ValueError, match="evidence"):
        ea.apply_availability(_hist(), {"availability": {"mode": "injury_report_out_v1", "out_player_ids": {}}})


@needs_pbp
def test_enabled_runs_are_deterministic_and_labeled():
    cfg = _wx_cfg()
    a = simulate.simulate_games(copy.deepcopy(cfg), pbp_path=str(PBP), n=40, seed=7, research_unaccepted=("weather_rain_wind_v1",))
    b = simulate.simulate_games(copy.deepcopy(cfg), pbp_path=str(PBP), n=40, seed=7, research_unaccepted=("weather_rain_wind_v1",))
    assert _h(a) == _h(b)
    env = a["environment_adjustments"]
    assert env["enabled"] == ["weather_rain_wind_v1"] and env["label"].startswith("UNACCEPTED_RESEARCH_ONLY")
    assert env["weather"]["keep_completion"] < 1 and env["weather"]["ypc_factor"] < 1


@needs_pbp
def test_off_keeps_player_box_identical_to_key_absent():
    """PR #36 player box recorder: explicit "off" adjustments give the same per-player box as no key at all."""
    a = simulate.simulate_games(make_cfg("NYJ", "CLE", 5, h2h="off"), pbp_path=str(PBP), n=30, seed=11)
    cfg = make_cfg("NYJ", "CLE", 5, h2h="off")
    cfg["environment"] = {"weather": {"mode": "off"}}; cfg["availability"] = {"mode": "off"}
    b = simulate.simulate_games(cfg, pbp_path=str(PBP), n=30, seed=11)
    assert "player_box" in a and json.dumps(a["player_box"], sort_keys=True, default=str) == \
        json.dumps(b["player_box"], sort_keys=True, default=str)


@needs_pbp
def test_unknown_research_name_error_lists_all_allowed():
    with pytest.raises(ValueError) as e:
        simulate.simulate_games(make_cfg("NYJ", "CLE", 5, h2h="off"), pbp_path=str(PBP), n=2, seed=1,
                                research_unaccepted=("nope",))
    msg = str(e.value)
    assert "'rare_plays'" in msg and "'weather_rain_wind_v1'" in msg and "'injury_report_out_v1'" in msg


def test_backtest_never_writes_committed_effects_file():
    src = (REPO / "calibration/weather_injury_backtest.py").read_text()
    assert "(ROOT / TRAIN_EFFECTS).write_text" not in src
    assert "calibration/outputs/runs/" in src
