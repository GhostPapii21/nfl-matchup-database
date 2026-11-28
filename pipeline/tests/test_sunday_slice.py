"""The Sunday slice runs existing engines and refuses a leaked week."""
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from pipeline import sunday as S

DEN = "2026_12_DEN_PIT"
NOW = datetime(2026, 11, 28, 2, 0, tzinfo=timezone.utc)


def test_den_pit_replay_is_labeled_and_not_sim_v6(tmp_path):
    result = S.run_game(DEN, n=80, possession_n=5, out_dir=tmp_path, pbp=None, now=NOW)
    assert result["status"] == "OK"
    assert result["projection_ready"] is False
    assert result["not_sim_v6"] is True
    assert result["not_sim100k"] is True
    assert result["mode"] == "historical_replay"
    period = result["primary_team_engine"]
    assert period["model_status"]["bias"].startswith("UNIMPLEMENTED")
    assert period["n"] == 80
    assert period["status"]["game_randomness"] == "NOT_APPLIED_THIS_CALL"
    scripts = result["cross_check_neighbors"]["scripts"]
    assert [s["name"] for s in scripts] == ["favorite_controls", "competitive", "underdog_chases"]
    assert abs(sum(s["probability"] for s in scripts) - 1) < 1e-6
    assert result["preflight"]["pbp_max_week"] < 12
    boards = result["player_boards_by_script"]
    assert set(boards) == {"favorite_controls", "competitive", "underdog_chases"}
    den = boards["competitive"]["sides"]["DEN"]["receivers"]
    assert any(r.get("yards_mean") is not None for r in den)
    poss = result["cross_check_possession"]
    assert poss["n_completed"] == 5
    assert poss["gate"] == "BYPASSED_DIRECT_CALL"
    text = Path(result["manifest_path"]).read_text()
    assert "sim_v6.py" not in text or "not the sim_v6" in text or "not sim_v6" in text.lower() or result["not_sim_v6"]
    saved = json.loads(Path(result["manifest_path"]).read_text())
    assert saved["projection_ready"] is False


def test_play_by_play_containing_the_target_week_is_refused(tmp_path):
    leaked = tmp_path / "leaked.parquet"
    pd.DataFrame({"week": [12], "season": [2026]}).to_parquet(leaked)
    pk = json.loads((S.PACKETS / DEN / "packet.json").read_text())
    gate = S.preflight(pk, pbp=leaked, now=NOW)
    assert gate["ok"] is False
    assert any("target week" in r for r in gate["reasons"])


def test_missing_market_is_refused():
    pk = json.loads((S.PACKETS / DEN / "packet.json").read_text())
    pk["market"] = {}
    pk["books"] = {}
    gate = S.preflight(pk, pbp=S.asof_pbp_path(2026, 12), now=NOW)
    assert gate["ok"] is False
    assert any("spread" in r for r in gate["reasons"])
