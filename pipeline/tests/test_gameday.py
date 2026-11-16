"""Game-day chain helpers: which games are due (pipeline.window) and the slate's exit codes (pipeline.slate)."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pipeline import phases as P, sim100k as S, slate as SL, window as W  # noqa: E402

KO = datetime(2026, 11, 16, 1, 20, tzinfo=timezone.utc)   # Sunday night, 8:20 PM ET
GID = "2026_10_PIT_CIN"


def repo(tmp_path, config=True, pbp=True, ran=False, games=(GID,)):
    r = tmp_path / "repo"
    (r / "pregame" / "packets").mkdir(parents=True)
    (r / "pipeline" / "ledgers").mkdir(parents=True)
    idx = []
    for g in games:
        d = r / "pregame" / "packets" / g
        d.mkdir()
        (d / "packet.json").write_text(json.dumps({"game": {"game_id": g, "date": "2026-11-15", "kickoff_et": "20:20"},
                                                    "weather": {"kickoff_utc": KO.isoformat()}}))
        idx.append({"game_id": g, "date": "2026-11-15", "kickoff_et": "20:20"})
        if config:
            c = r / S.CONFIG_REL
            c.mkdir(parents=True, exist_ok=True)
            (c / f"{g}.json").write_text(json.dumps({"mode": "data_only", "game": {"game_id": g, "season": 2026, "week_asof_exclusive": 10},
                                                     "history": {"season": 2026}}))
    (r / "pregame" / "packets" / "latest.json").write_text(json.dumps({"games": idx}))
    if pbp:
        (r / S.PBP_REL).mkdir(parents=True)
        (r / S.PBP_REL / "pbp_2026_w1_9_pulled_20261112T1116ET.parquet").write_bytes(b"x")
    if ran:
        (r / "pipeline" / "ledgers" / f"{GID}.sim100k.json").write_text(json.dumps({"status": "RAN_RESEARCH_ONLY"}))
    return r


@pytest.mark.parametrize("minutes, due, why", [
    (120, False, "opens at T-88"), (89, False, "opens at T-88"), (88, True, "inside"), (60, True, "inside"),
    (40, True, "inside"), (39, False, "closed at T-40"), (-5, False, "kicked off")])
def test_window_edges(tmp_path, minutes, due, why):
    res = W.evaluate(KO - timedelta(minutes=minutes), root=repo(tmp_path))
    row = res["games"][0]
    assert row["due"] is due and why in row["why"]
    assert [d["game_id"] for d in res["due"]] == ([GID] if due else [])


def test_due_row_carries_config_and_asof_pbp(tmp_path):
    d = W.evaluate(KO - timedelta(minutes=70), root=repo(tmp_path))["due"][0]
    assert d["config"].endswith(f"{GID}.json") and d["pbp"].endswith("pbp_2026_w1_9_pulled_20261112T1116ET.parquet")


def test_not_due_once_the_100k_ran(tmp_path):
    row = W.evaluate(KO - timedelta(minutes=70), root=repo(tmp_path, ran=True))["games"][0]
    assert row["due"] is False and "already ran" in row["why"]


def test_not_due_without_engine_config_or_asof_pbp(tmp_path):
    assert W.evaluate(KO - timedelta(minutes=70), root=repo(tmp_path, config=False))["due"] == []
    row = W.evaluate(KO - timedelta(minutes=70), root=repo(tmp_path / "b", pbp=False))["games"][0]
    assert row["due"] is False and "as-of play-by-play" in row["why"]


def test_only_filter_and_missing_index(tmp_path):
    r = repo(tmp_path, games=(GID, "2026_10_SF_DAL"))
    assert [d["game_id"] for d in W.evaluate(KO - timedelta(minutes=70), only=["2026_10_SF_DAL"], root=r)["due"]] == ["2026_10_SF_DAL"]
    res = W.evaluate(KO, root=tmp_path / "nothing")
    assert res["due"] == [] and "cannot read" in res["error"]


# ------------------------------------------------------------------------------------------------ slate exit codes
@pytest.fixture
def slate_env(tmp_path, monkeypatch):
    pk = {"game": {"game_id": GID, "date": "2026-11-15", "kickoff_et": "20:20", "away": "PIT", "home": "CIN"},
          "weather": {"kickoff_utc": KO.isoformat()}}
    d = tmp_path / "packets" / GID
    d.mkdir(parents=True)
    (d / "packet.json").write_text(json.dumps(pk))
    (tmp_path / "packets" / "latest.json").write_text(json.dumps({"games": [{"game_id": GID, "date": "2026-11-15", "kickoff_et": "20:20"}]}))
    monkeypatch.setattr(P, "PACKETS", tmp_path / "packets")
    monkeypatch.setattr(P, "LEDGERS", tmp_path / "ledgers")
    (tmp_path / "ledgers").mkdir()
    return tmp_path / "ledgers"


REFUSED = (2, {"status": "REFUSED", "reasons": ["G4: odds STALE"], "checked_utc": "2026-11-15T23:55:00+00:00"})
RAN = (0, {"status": "RAN_RESEARCH_ONLY", "reasons": [], "checked_utc": "2026-11-16T00:10:00+00:00",
           "result": {"n": 100000, "player_box_trials": {"values": "huge"}}})


def test_all_refused_is_reported_and_expect_fails(slate_env, monkeypatch, capsys):
    monkeypatch.setattr(S, "run", lambda gid, *a, **k: REFUSED)
    assert SL.main([]) == 0                       # a refusal is still a recorded result...
    out = capsys.readouterr().out
    assert "0 of 1 games have a 100k that ran; 1 refused" in out
    assert "100k ran for 0 of 1 games" in (slate_env / "INDEX.md").read_text()
    assert SL.main(["--expect", GID]) == 2        # ...but not a success for a game that was supposed to run
    assert f"EXPECTED {GID}" in capsys.readouterr().out


def test_expect_passes_when_it_ran_and_trials_are_not_written(slate_env, monkeypatch, capsys):
    monkeypatch.setattr(S, "run", lambda gid, *a, **k: RAN)
    assert SL.main(["--expect", GID]) == 0
    assert "1 of 1 games have a 100k that ran; 0 refused" in capsys.readouterr().out
    rep = json.loads((slate_env / f"{GID}.sim100k.json").read_text())
    assert rep["status"] == "RAN_RESEARCH_ONLY" and "player_box_trials" not in rep["result"]


def test_a_later_refusal_never_overwrites_a_run(slate_env, monkeypatch, capsys):
    (slate_env / f"{GID}.sim100k.json").write_text(json.dumps(RAN[1]))
    called = []
    monkeypatch.setattr(S, "run", lambda gid, *a, **k: called.append(gid) or REFUSED)
    assert SL.main(["--expect", GID]) == 0
    assert called == [] and json.loads((slate_env / f"{GID}.sim100k.json").read_text())["status"] == "RAN_RESEARCH_ONLY"
    assert "kept" in capsys.readouterr().out


def test_single_game_from_report_leaves_index_alone(slate_env, monkeypatch):
    (slate_env / f"{GID}.sim100k.json").write_text(json.dumps(REFUSED[1]))
    monkeypatch.setattr(S, "run", lambda *a, **k: pytest.fail("the gate must not run again with --from-report"))
    assert SL.main(["--game", GID, "--from-report"]) == 0
    assert (slate_env / f"{GID}.md").exists() and not (slate_env / "INDEX.md").exists()
    assert SL.main(["--game", GID, "--from-report", "--expect", GID]) == 2
    assert SL.main(["--index-only"]) == 0 and (slate_env / "INDEX.md").exists()


def test_from_report_without_a_report_is_an_error(slate_env):
    assert SL.main(["--game", GID, "--from-report"]) == 1
