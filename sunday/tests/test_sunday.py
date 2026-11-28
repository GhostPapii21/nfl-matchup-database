"""Sunday CLI: preflight, one game, bounded slate, and the DEN@PIT replay. Offline."""
from __future__ import annotations

import hashlib
import json
import sys
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pipeline import freshness as F  # noqa: E402
from sunday import cli, discover, execute, preflight  # noqa: E402

AS_OF = datetime(2026, 11, 29, 12, 0, tzinfo=timezone.utc)
STAMP = AS_OF - timedelta(minutes=5)
GID = "2026_12_AAA_BBB"
FLAGS = ROOT / "known_flags" / "KNOWN_LIMITATIONS.json"
DEN_PACKET = ROOT / "pregame" / "packets" / "2026_12_DEN_PIT" / "packet.json"


@pytest.fixture(autouse=True)
def _offline_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(F, "CACHE", tmp_path / "no-cache")


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def _team():
    starters = [
        {"slot": "QB", "player": "Quincy Quartermain"},
        {"slot": "RB", "player": "Riley Runner"},
        {"slot": "WR", "player": "Wendy Wide"},
        {"slot": "TE", "player": "Terry Tight"},
    ]
    return {"depth_chart": {"status": "OK", "as_of": iso(STAMP), "starters": starters},
            "injuries": {"official_report": [], "espn_live": []}}


def _packet(game_id=GID, away="AAA", home="BBB", *, qb=True, books=True, future_source=False):
    retrieved = iso(AS_OF + timedelta(hours=2) if future_source else STAMP)
    publisher = {"status": "OK", "retrieved_utc": retrieved, "source_updated_at": retrieved}
    live = {"status": "OK", "retrieved_utc": retrieved}
    sources = {name: dict(publisher) for name in
               ("pbp", "rosters", "depth_charts", "snap_counts", "ftn", "pfr_def", "injuries",
                "ngs_passing", "ngs_receiving", "ngs_rushing")}
    sources["games"] = dict(live)
    sources["espn_injuries"] = dict(live)
    team = _team()
    if not qb:
        team = {"depth_chart": {"status": "OK", "as_of": iso(STAMP), "starters": [{"slot": "WR", "player": "Only Wide"}]},
                "injuries": {"official_report": []}}
    return {
        "schema": "pregame-packet/1",
        "projection_ready": False,
        "generated_utc": iso(STAMP),
        "game": {"game_id": game_id, "season": 2026, "week": 12, "away": away, "home": home,
                 "date": "2026-11-29", "kickoff_et": "13:00", "roof": "outdoors",
                 "listed_qbs": {away: "Quincy Quartermain", home: "Quincy Quartermain"}},
        "teams": {away: team, home: json.loads(json.dumps(team))},
        "data_freshness": {away: {"status": "OK"}, home: {"status": "OK"}},
        "books": ({"status": "OK", "retrieved_utc": retrieved, "markets": {"spread": {"line": 3.5}}}
                  if books else {"status": "MISSING"}),
        "weather": {"status": "OK", "retrieved_utc": retrieved, "source_updated_at": retrieved,
                    "kickoff_utc": "2026-11-29T18:00:00+00:00"},
        "sources": sources,
        "phase_ledger": [{"phase": n, "name": f"p{n}", "status": "AUTO"} for n in range(1, 15)]
        + [{"phase": 15, "name": "inactives", "status": "PENDING"}],
        "team_projection": {"status": "RESEARCH_ONLY_NOT_VALIDATED", "engine": "core/period_engine_v0", "trials": 20,
                            "samplers": {"matchup_pair": {"home_points": 21.0, "away_points": 17.0, "home_margin": 4.0,
                                                         "total": 38.0, "home_win": 0.6, "away_win": 0.4}}},
    }


def _freeze(repo: Path, away="AAA", home="BBB", name="freeze_20261129T115500Z.json", body=None):
    folder = repo / "pregame" / "price_freezes" / f"2026-11-29_{away}@{home}"
    folder.mkdir(parents=True, exist_ok=True)
    payload = body if body is not None else {
        "meta": {"status": "OK", "pulled_utc": iso(STAMP)},
        "rows": [{"book": b, "market": "spreads", "reference_only": False}
                 for b in ("fanduel", "draftkings", "betmgm", "williamhill_us")],
    }
    (folder / name).write_text(json.dumps(payload))


def _index(repo: Path, rows: list[dict]):
    path = repo / "pregame" / "packets" / "latest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema": "pregame-index/1", "games": rows}))


def _row(game_id, away, home):
    return {"game_id": game_id, "week": 12, "date": "2026-11-29", "kickoff_et": "13:00", "away": away, "home": home,
            "slot": "Sunday early window", "packet": f"pregame/packets/{game_id}/packet.json"}


def _write_game(repo: Path, game_id, away, home, **packet_kw):
    path = repo / "pregame" / "packets" / game_id / "packet.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_packet(game_id, away, home, **packet_kw)))
    _freeze(repo, away, home)


def _repo(tmp: Path, **packet_kw) -> Path:
    repo = tmp / "repo"
    _index(repo, [_row(GID, "AAA", "BBB")])
    _write_game(repo, GID, "AAA", "BBB", **packet_kw)
    return repo


def _run(repo: Path, out: Path, *extra) -> dict:
    code = cli.main(["game", "--repo", str(repo), "--out", str(out), "--game", GID, "--as-of", iso(AS_OF), *extra])
    packet = json.loads((out / "packet.json").read_text())
    packet["_exit"] = code
    return packet


def test_help_lists_commands_and_arguments(capsys):
    assert cli.main(["--help"]) == 0
    text = capsys.readouterr().out
    for word in ("preflight", "game", "slate", "replay"):
        assert word in text
    assert cli.main(["game", "--help"]) == 0
    game_help = capsys.readouterr().out
    for word in ("--game", "--as-of", "--market", "--repo", "--out", "--min-free-mb"):
        assert word in game_help
    assert cli.main(["slate", "--help"]) == 0
    slate_help = capsys.readouterr().out
    for word in ("--week", "--date", "--slot", "--include-started", "--all", "--concurrency"):
        assert word in slate_help


def test_rejects_a_game_id_that_could_escape_the_repo(tmp_path):
    assert cli.main(["game", "--repo", str(tmp_path), "--game", "../secret"]) == 1


def test_missing_schedule_index_exits_1(tmp_path):
    assert cli.main(["game", "--repo", str(tmp_path), "--game", GID, "--as-of", iso(AS_OF)]) == 1


def test_clear_critical_checks_are_partial_only_where_layers_or_config_are_open(tmp_path):
    repo = _repo(tmp_path)
    packet = _run(repo, tmp_path / "out")
    assert packet["projection_ready"] is False
    assert packet["result"] == "PARTIAL"
    assert packet["_exit"] == 0
    assert packet["critical_ids"] == []
    assert "engine_config" in packet["required_ids"]
    fresh = {row["id"] for row in packet["checks"] if row["status"] == "FRESH"}
    assert fresh.isdisjoint(packet["required_ids"])
    assert "NFL-87" in packet["layer_gaps"]
    assert packet["leakage"]["status"] == "PASS"
    assert packet["cited_outputs"]["hundred_k"]["status"] == "NOT_RUN"
    assert packet["cited_outputs"]["team_projection"]["status"] == "CITED_NOT_RERUN"


def test_rollup_is_pass_when_every_check_and_layer_is_clear():
    checks = [preflight.check("identity", "critical", "PASS", "ok"),
              preflight.check("freshness.schedule", "required", "NOT_YET", "before window"),
              preflight.check("freshness.odds", "required", "FRESH", "current")]
    layers = [{"issue": "NFL-87", "status": "OK"}]
    result, critical, required, gaps = preflight.rollup(checks, layers)
    assert (result, critical, required, gaps) == ("PASS", [], [], [])


def test_identity_mismatch_blocks(tmp_path):
    repo = _repo(tmp_path)
    index = json.loads((repo / "pregame" / "packets" / "latest.json").read_text())
    index["games"][0]["home"] = "ZZZ"
    (repo / "pregame" / "packets" / "latest.json").write_text(json.dumps(index))
    packet = _run(repo, tmp_path / "out")
    assert packet["result"] == "BLOCKED"
    assert packet["_exit"] == 2
    assert "identity" in packet["critical_ids"]


def test_missing_quarterback_blocks(tmp_path):
    repo = _repo(tmp_path, qb=False)
    packet = _run(repo, tmp_path / "out")
    assert packet["result"] == "BLOCKED"
    assert "roles" in packet["critical_ids"]


def test_market_request_without_a_snapshot_blocks(tmp_path):
    repo = _repo(tmp_path, books=False)
    packet = _run(repo, tmp_path / "out", "--market")
    assert packet["result"] == "BLOCKED"
    assert "freshness.odds" in packet["critical_ids"] or "odds_snapshot" in packet["critical_ids"]


def test_stamp_after_as_of_is_leakage(tmp_path):
    repo = _repo(tmp_path, future_source=True)
    packet = _run(repo, tmp_path / "out")
    assert packet["result"] == "BLOCKED"
    assert "leakage" in packet["critical_ids"]


def test_as_of_after_kickoff_blocks(tmp_path):
    repo = _repo(tmp_path)
    later = iso(AS_OF + timedelta(days=2))
    code = cli.main(["game", "--repo", str(repo), "--out", str(tmp_path / "out"), "--game", GID, "--as-of", later])
    packet = json.loads((tmp_path / "out" / "packet.json").read_text())
    assert code == 2 and packet["result"] == "BLOCKED"
    assert "identity" in packet["critical_ids"]


def test_low_disk_blocks(tmp_path):
    repo = _repo(tmp_path)
    code = cli.main(["preflight", "--repo", str(repo), "--out", str(tmp_path / "out"), "--min-free-mb", "999999999",
                     "--game", GID, "--as-of", iso(AS_OF)])
    packet = json.loads((tmp_path / "out" / "packet.json").read_text())
    assert code == 2 and "disk" in packet["critical_ids"]
    assert packet["command"].startswith("python -m sunday preflight")


def test_future_freeze_and_postgame_files_are_not_read(tmp_path):
    repo = _repo(tmp_path)
    _freeze(repo, name="freeze_20990101T000000Z.json", body={"marker": "FUTURE_LINE_MARKER"})
    post = repo / "grading" / "results" / "sources"
    post.mkdir(parents=True)
    (post / f"espn_summary_{GID}.json").write_text('{"marker": "FINAL_SCORE_MARKER", "home_score": 27}')
    snap = repo / "snapshots" / GID / "20990101T000000Z"
    snap.mkdir(parents=True)
    (snap / "summary.json").write_text('{"marker": "SNAP_MARKER", "points": {"BBB": 99}}')
    (snap / "LOCK.json").write_text('{"locked_utc": "2099-01-01T00:00:00+00:00", "projection_ready": false}')
    packet = _run(repo, tmp_path / "out")
    text = (tmp_path / "out" / "packet.json").read_text()
    assert "FUTURE_LINE_MARKER" not in text
    assert "FINAL_SCORE_MARKER" not in text
    assert "SNAP_MARKER" not in text
    excluded = {row["path"] for row in packet["leakage"]["excluded"]}
    assert f"grading/results/sources/espn_summary_{GID}.json" in excluded
    assert any(path.startswith(f"snapshots/{GID}/20990101T000000Z") for path in excluded)
    assert f"snapshots/{GID}/20990101T000000Z/summary.json" not in packet["leakage"]["inputs_read"]
    assert packet["leakage"]["status"] == "PASS"


def test_slate_isolates_a_bad_packet_and_links_every_report(tmp_path):
    repo = tmp_path / "repo"
    rows = []
    for gid, away, home in ((GID, "AAA", "BBB"), ("2026_12_CCC_DDD", "CCC", "DDD"), ("2026_12_EEE_FFF", "EEE", "FFF")):
        rows.append(_row(gid, away, home))
        if gid.endswith("FFF"):
            path = repo / "pregame" / "packets" / gid / "packet.json"
            path.parent.mkdir(parents=True)
            path.write_text("{")
        else:
            _write_game(repo, gid, away, home)
    _index(repo, rows)
    out = tmp_path / "slate"
    code = cli.main(["slate", "--repo", str(repo), "--out", str(out), "--as-of", iso(AS_OF), "--concurrency", "2", "--all"])
    index = json.loads((out / "index.json").read_text())
    assert index["projection_ready"] is False
    assert index["concurrency_used"] == 2
    assert index["concurrency_cap"] == 8
    assert index["peak_in_flight"] <= 2
    assert {row["game_id"]: row["result"] for row in index["games"]}["2026_12_EEE_FFF"] == "BLOCKED"
    assert index["games"][0]["result"] == "PARTIAL"
    text = (out / "INDEX.md").read_text()
    for row in index["games"]:
        assert f"]({row['report_rel']})" in text
        assert (out / row["report_rel"]).is_file()
    good = json.loads((out / GID / "packet.json").read_text())
    assert good["game_id"] == GID
    assert "EEE" not in json.dumps(good["roles"])
    assert code == 2  # one game is BLOCKED


def test_slate_concurrency_does_not_exceed_the_cap(tmp_path):
    games = [{"game_id": f"2026_12_A{i}A_B{i}B", "date": "2026-11-29", "kickoff_et": "13:00"} for i in range(4)]
    barrier = threading.Barrier(2)

    def runner(**kwargs):
        barrier.wait(timeout=3)
        return {"game_id": kwargs["game_id"], "result": "PASS", "canonical_sha256": "abc",
                "projection_ready": False, "critical_ids": [], "required_ids": []}

    slate = execute.run_slate(games, repo=tmp_path, out=tmp_path / "out", as_of=AS_OF, concurrency=2, runner=runner)
    assert slate["peak_in_flight"] == 2
    assert slate["concurrency_used"] == 2
    assert slate["result"] == "PASS"
    assert slate["projection_ready"] is False


def test_replay_of_a_synthetic_packet_matches(tmp_path):
    repo = _repo(tmp_path)
    out = tmp_path / "replay"
    code = cli.main(["replay", "--repo", str(repo), "--out", str(out), "--game", GID])
    record = json.loads((out / "replay.json").read_text())
    assert record["reproducibility"] == "PASS"
    assert record["projection_ready"] is False
    assert record["run_a"]["canonical_sha256"] == record["run_b"]["canonical_sha256"]
    assert record["result"] == "PARTIAL"
    assert code == 0
    assert record["as_of_utc"] == iso(STAMP)


def test_no_games_matched_exits_1(tmp_path):
    repo = _repo(tmp_path)
    assert cli.main(["slate", "--repo", str(repo), "--date", "1999-01-01", "--as-of", iso(AS_OF),
                     "--out", str(tmp_path / "out")]) == 1


@pytest.mark.skipif(not DEN_PACKET.is_file(), reason="DEN@PIT packet is not in this checkout")
def test_den_pit_replay_is_reproducible_and_does_not_read_postgame_files(tmp_path):
    before = hashlib.sha256(FLAGS.read_bytes()).hexdigest()
    out = tmp_path / "den"
    code = cli.main(["replay", "--repo", str(ROOT), "--out", str(out), "--game", "2026_12_DEN_PIT"])
    record = json.loads((out / "replay.json").read_text())
    assert hashlib.sha256(FLAGS.read_bytes()).hexdigest() == before
    assert json.loads(FLAGS.read_text())["projection_ready"] is False
    assert record["reproducibility"] == "PASS"
    assert record["projection_ready"] is False
    assert record["leakage"]["status"] == "PASS"
    assert record["result"] == "PARTIAL"
    assert record["run_a"]["critical_ids"] == []
    assert code == 0
    packet = json.loads((out / "run_a" / "2026_12_DEN_PIT" / "packet.json").read_text())
    assert packet["projection_ready"] is False
    assert packet["cited_outputs"]["hundred_k"]["status"] == "NOT_RUN"
    assert packet["cited_outputs"]["locked_snapshot"]["status"] == "EXCLUDED"
    read = set(packet["leakage"]["inputs_read"])
    excluded = {row["path"] for row in packet["leakage"]["excluded"]}
    for banned in (
        "grading/results/sources/espn_summary_2026_12_DEN_PIT_401873083.json",
        "data/historical/playlogs/2026_wk12/DEN_PIT.csv",
        "data/historical/projections/matchup_master_postgame_DEN_PIT.csv",
        "runs/2026-11-27_DEN@PIT/pbp/summary_FINAL.json",
    ):
        assert banned in excluded
        assert banned not in read
    assert "snapshots/2026_12_DEN_PIT/20261127T111648Z" in excluded
    assert "snapshots/2026_12_DEN_PIT/20261127T111648Z/summary.json" not in read
    text = json.dumps(packet)
    assert "summary_FINAL" not in text or "summary_FINAL" in json.dumps(packet["leakage"]["excluded"])
    assert packet["as_of_utc"].startswith("2026-11-27T04:31:50")


def test_real_sunday_slate_writes_every_report(tmp_path):
    out = tmp_path / "sunday"
    code = cli.main(["slate", "--repo", str(ROOT), "--out", str(out), "--date", "2026-11-29",
                     "--as-of", "2026-11-29T12:00:00+00:00", "--concurrency", "2"])
    index = json.loads((out / "index.json").read_text())
    assert index["projection_ready"] is False
    assert len(index["games"]) == 10
    assert index["peak_in_flight"] <= 2
    assert index["concurrency_used"] == 2
    for game in index["games"]:
        assert game["result"] in {"PASS", "PARTIAL", "BLOCKED"}
        report = out / game["report_rel"]
        assert report.is_file()
        packet = json.loads((out / game["game_id"] / "packet.json").read_text())
        assert packet["projection_ready"] is False
        assert packet["game_id"] == game["game_id"]
        assert "runner" not in (packet.get("critical_ids") or [])
    assert (out / "INDEX.md").is_file()
    assert code == (2 if index["result"] == "BLOCKED" else 0)
    discover_count = len(discover.select(
        json.loads((ROOT / "pregame" / "packets" / "latest.json").read_text())["games"],
        on_date="2026-11-29"))
    assert discover_count == 10
