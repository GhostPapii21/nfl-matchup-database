"""Local integration tests for the durable game scheduler. No network."""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from scheduler.model import PHASES
from scheduler.orchestrator import Orchestrator, open_store
from scheduler.runner import HandlerResult
from scheduler.sources import games_from_packet_index, games_from_slate
from scheduler.store import SQLITE_DDL, Store
from scheduler.timeutil import ScheduleError, parse_kickoff, utc_iso
from scheduler.model import Game

ROOT = Path(__file__).resolve().parents[2]
NOW = datetime(2026, 11, 29, 18, 0, tzinfo=timezone.utc)


def _game(game_id: str, kickoff: datetime, status: str = "scheduled") -> Game:
    return Game(game_id, 2026, 12, "AWY", "HOM", kickoff, status)


def _orch(tmp_path, runner=None, **kw) -> Orchestrator:
    path = Path(tmp_path)
    path.mkdir(parents=True, exist_ok=True)
    store = Store(path / "queue.sqlite")
    defaults = dict(max_in_flight=2, max_heavy=1, lease_ttl=timedelta(seconds=30), max_attempts=3,
                    assumed_heavy_seconds=0)
    defaults.update(kw)
    return Orchestrator(store, runner=runner, **defaults)


class Probe:
    def __init__(self, *, fail: bool = False, refuse: bool = False, flag: str | None = None,
                 sleep: float = 0, artifact: bytes | None = b'{"ok":true}'):
        self.fail = fail
        self.refuse = refuse
        self.flag = flag
        self.sleep = sleep
        self.artifact = artifact
        self.lock = threading.Lock()
        self.current = 0
        self.peak = 0
        self.heavy_current = 0
        self.heavy_peak = 0
        self.calls: list[str] = []

    def run(self, ctx):
        import time
        with self.lock:
            self.current += 1
            self.peak = max(self.peak, self.current)
            if ctx.job["heavy"]:
                self.heavy_current += 1
                self.heavy_peak = max(self.heavy_peak, self.heavy_current)
            self.calls.append(ctx.job["phase"])
        try:
            if self.sleep:
                time.sleep(self.sleep)
            if self.fail:
                raise RuntimeError("boom")
            if self.flag:
                return HandlerResult(status="recorded", detail="blocked", **{self.flag: True})
            if self.refuse:
                return HandlerResult(status="refused", detail="source refused")
            artifacts = {} if self.artifact is None else {"note.json": self.artifact}
            return HandlerResult(status="recorded", detail="ok", artifacts=artifacts)
        finally:
            with self.lock:
                self.current -= 1
                if ctx.job["heavy"]:
                    self.heavy_current -= 1

    def reset_peaks(self) -> None:
        self.peak = 0
        self.heavy_peak = 0
        self.current = 0
        self.heavy_current = 0


def test_phase_windows_match_existing_gates():
    from pipeline.freshness import INACTIVES_POST_MINUTES_BEFORE_KICKOFF
    from pipeline.window import CLOSE_MINUTES
    injury, lock, post = PHASES
    assert injury.open_offset == timedelta(minutes=-INACTIVES_POST_MINUTES_BEFORE_KICKOFF)
    assert injury.deadline_offset == timedelta(minutes=-CLOSE_MINUTES)
    assert lock.deadline_offset == timedelta(0)
    assert lock.heavy and lock.immutable
    assert post.open_offset == timedelta(hours=3)


def test_timezone_and_dst():
    assert utc_iso(parse_kickoff("2026-09-13T13:00")) == "2026-09-13T17:00:00Z"
    assert utc_iso(parse_kickoff("2026-11-29T13:00")) == "2026-11-29T18:00:00Z"
    assert utc_iso(parse_kickoff("2026-11-29T13:00:00Z")) == "2026-11-29T13:00:00Z"
    first = parse_kickoff("2026-11-01T01:30", fold=0)
    second = parse_kickoff("2026-11-01T01:30", fold=1)
    assert utc_iso(first) == "2026-11-01T05:30:00Z"
    assert utc_iso(second) == "2026-11-01T06:30:00Z"
    with pytest.raises(ScheduleError, match="ambiguous"):
        parse_kickoff("2026-11-01T01:30")
    with pytest.raises(ScheduleError, match="does not exist"):
        parse_kickoff("2026-03-08T02:30")


def test_packet_index_eastern_kickoff():
    doc = json.loads((ROOT / "pregame" / "packets" / "latest.json").read_text())
    games, problems = games_from_packet_index(doc)
    assert problems == []
    kc = next(game for game in games if game.game_id == "2026_12_KC_BUF")
    assert utc_iso(kc.kickoff_utc) == "2026-11-27T01:20:00Z"


def test_duplicate_trigger(tmp_path):
    orch = _orch(tmp_path)
    game = _game("2026_12_DEN_PIT", NOW + timedelta(minutes=80))
    first = orch.tick([game], NOW, owner="a")
    second = orch.tick([game], NOW, owner="a")
    assert first.created == 3
    assert second.created == 0
    assert second.ran == []
    assert orch.store.count_jobs() == 3
    assert sum(1 for job in orch.store.list_jobs("succeeded") if job["phase"] == "injury_refresh") == 1


def test_delayed_trigger_still_runs_inside_the_window(tmp_path):
    probe = Probe()
    orch = _orch(tmp_path, probe)
    # T-75 is inside the injury window and before the lock opens at T-70.
    kickoff = NOW + timedelta(minutes=75)
    result = orch.tick([_game("G", kickoff)], NOW, owner="a")
    assert [row["status"] for row in result.ran] == ["succeeded"]
    job = orch.store.list_jobs("succeeded")[0]
    receipt = orch.store.receipts_for(job["id"])[0]
    assert receipt["delay_seconds"] == 15 * 60
    assert job["phase"] == "injury_refresh"


def test_missed_kickoff_window_does_not_call_the_handler(tmp_path):
    probe = Probe()
    orch = _orch(tmp_path, probe)
    kickoff = NOW - timedelta(minutes=1)
    result = orch.tick([_game("G", kickoff)], NOW, owner="a")
    assert result.ran == []
    assert probe.calls == []
    statuses = {job["phase"]: job["status"] for job in orch.store.list_jobs()}
    assert statuses["injury_refresh"] == "missed"
    assert statuses["prekick_lock"] == "missed"
    assert statuses["postgame_grade"] == "queued"
    assert {alert["kind"] for alert in orch.store.open_alerts()} >= {"missed"}


def test_worker_crash_retry_and_heartbeat(tmp_path):
    probe = Probe()
    orch = _orch(tmp_path, probe)
    game = _game("G", NOW + timedelta(minutes=80))
    orch.sync([game], NOW)
    claimed = orch.claim("crashed-worker", NOW)
    assert claimed[0]["attempt"] == 1
    assert orch.store.heartbeat(claimed[0]["id"], "crashed-worker", NOW + timedelta(seconds=10), orch.lease_ttl)
    assert orch.recover(NOW + orch.lease_ttl) == []
    later = NOW + timedelta(seconds=10) + orch.lease_ttl + timedelta(seconds=1)
    assert orch.recover(later) == [claimed[0]["id"]]
    assert orch.store.get_job(claimed[0]["id"])["status"] == "queued"
    ran = orch.claim_and_run("retry-worker", later)
    assert ran[0]["status"] == "succeeded"
    job = orch.store.get_job(claimed[0]["id"])
    assert job["attempt"] == 2
    receipts = orch.store.receipts_for(job["id"])
    assert [row["status"] for row in receipts] == ["crashed", "recorded"]


def test_late_owner_cannot_finish_after_recovery(tmp_path):
    orch = _orch(tmp_path, Probe())
    orch.sync([_game("G", NOW + timedelta(minutes=80))], NOW)
    first = orch.claim("a", NOW)[0]
    later = NOW + orch.lease_ttl + timedelta(seconds=1)
    orch.recover(later)
    assert orch.claim_and_run("b", later)[0]["status"] == "succeeded"
    kept = orch.store.finish(first["id"], "a", 1, later, "succeeded", "recorded", "{}", None, [])
    assert kept is False
    job = orch.store.get_job(first["id"])
    assert job["status"] == "succeeded"
    assert job["attempt"] == 2
    assert job["lease_owner"] is None


def test_concurrent_duplicate_and_no_overlap(tmp_path):
    orch = _orch(tmp_path, Probe())
    orch.sync([_game("G", NOW + timedelta(minutes=80))], NOW)
    barrier = threading.Barrier(2)
    claimed: list[list] = []

    def _grab(owner: str) -> None:
        barrier.wait()
        claimed.append(orch.claim(owner, NOW))

    threads = [threading.Thread(target=_grab, args=(owner,)) for owner in ("a", "b")]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert sum(len(batch) for batch in claimed) == 1

    started = threading.Event()
    release = threading.Event()

    class _Block:
        def run(self, ctx):
            started.set()
            assert release.wait(5)
            return HandlerResult(status="recorded", detail="ok")

    other = _orch(tmp_path / "overlap", _Block())
    other.sync([_game("G", NOW + timedelta(minutes=80))], NOW)
    runner = threading.Thread(target=lambda: other.claim_and_run("holder", NOW))
    runner.start()
    assert started.wait(2)
    assert other.claim("intruder", NOW) == []
    release.set()
    runner.join(timeout=5)
    assert not runner.is_alive()


def test_full_slate_bounded_concurrency(tmp_path):
    probe = Probe(sleep=0.05)
    orch = _orch(tmp_path, probe, max_in_flight=2, max_heavy=1)
    kickoff = NOW + timedelta(minutes=80)
    games = [_game(f"G{i:02d}", kickoff) for i in range(16)]
    first = orch.tick(games, NOW, owner="slate", parallel=True)
    assert first.created == 48
    assert probe.peak <= 2
    assert probe.heavy_peak == 0
    assert probe.calls.count("injury_refresh") == 16
    assert len(orch.store.list_jobs("succeeded")) == 16
    lock_now = kickoff - timedelta(minutes=50)
    cap = orch.claim("cap", lock_now)
    assert len(cap) == 1
    assert cap[0]["phase"] == "prekick_lock"
    assert cap[0]["heavy"] == 1
    assert orch._execute(cap[0], "cap", lock_now)["status"] == "succeeded"
    second = orch.tick(games, lock_now, owner="slate", parallel=True)
    assert second.created == 0
    assert probe.calls.count("prekick_lock") == 16
    locks = [job for job in orch.store.list_jobs("succeeded") if job["phase"] == "prekick_lock"]
    assert len(locks) == 16
    payload = json.loads(locks[0]["payload_json"])
    assert payload["workload_class"] == "simulation_300k"
    assert payload["analytical_execution"] is False
    assert payload["projection_ready"] is False


def test_backpressure_when_heavy_queue_cannot_finish(tmp_path):
    orch = _orch(tmp_path, Probe(), assumed_heavy_seconds=100, max_heavy=1)
    kickoff = NOW + timedelta(minutes=80)
    games = [_game(f"G{i}", kickoff) for i in range(8)]
    orch.tick(games, NOW, owner="a")
    assert orch.assess_backpressure(NOW) is False
    later = kickoff - timedelta(seconds=600)
    assert orch.assess_backpressure(later) is True
    assert any(alert["kind"] == "backpressure" for alert in orch.store.open_alerts())


def test_schedule_change_supersedes_queued_jobs_and_keeps_history(tmp_path):
    orch = _orch(tmp_path, Probe())
    original = _game("G", NOW + timedelta(minutes=80))
    orch.tick([original], NOW, owner="a")
    moved = _game("G", NOW + timedelta(days=1, minutes=80))
    stats = orch.sync([moved], NOW)
    assert stats["superseded"] == 2
    assert stats["created"] == 3
    rows = orch.store.list_jobs()
    assert sum(1 for job in rows if job["status"] == "succeeded" and job["phase"] == "injury_refresh") == 1
    assert sum(1 for job in rows if job["status"] == "superseded") == 2
    assert sum(1 for job in rows if job["status"] == "queued") == 3
    assert len({job["schedule_version"] for job in rows}) == 2


def test_postponement_cancels_queued_work(tmp_path):
    orch = _orch(tmp_path, Probe())
    game = _game("G", NOW + timedelta(minutes=80))
    orch.tick([game], NOW, owner="a")
    stats = orch.sync([_game("G", game.kickoff_utc, "postponed")], NOW)
    assert stats["cancelled"] == 2
    statuses = {job["phase"]: job["status"] for job in orch.store.list_jobs()}
    assert statuses["injury_refresh"] == "succeeded"
    assert statuses["prekick_lock"] == "cancelled"
    assert statuses["postgame_grade"] == "cancelled"
    assert any(alert["kind"] == "postponed" for alert in orch.store.open_alerts())


def test_final_opens_postgame_without_replacing_the_lock(tmp_path):
    probe = Probe()
    orch = _orch(tmp_path, probe)
    kickoff = NOW + timedelta(minutes=80)
    game = _game("G", kickoff)
    orch.tick([game], NOW, owner="a")
    orch.tick([game], kickoff - timedelta(minutes=50), owner="a")
    lock = next(job for job in orch.store.list_jobs("succeeded") if job["phase"] == "prekick_lock")
    final_now = kickoff + timedelta(minutes=10)
    result = orch.tick([_game("G", kickoff, "final")], final_now, owner="a")
    assert result.created == 0
    assert [row["status"] for row in result.ran] == ["succeeded"]
    assert orch.store.get_job(lock["id"])["status"] == "succeeded"
    post = next(job for job in orch.store.list_jobs("succeeded") if job["phase"] == "postgame_grade")
    assert post["id"] != lock["id"]


def test_dry_run_and_cli_do_not_write_the_live_queue(tmp_path):
    orch = _orch(tmp_path)
    game = _game("G", NOW + timedelta(minutes=80))
    plan = orch.dry_run([game], NOW, expected_ids=["G", "MISSING"])
    assert orch.store.count_jobs() == 0
    assert orch.store.refresh_count() == 0
    assert plan["created"] == 3
    assert [row["phase"] for row in plan["would_claim"]] == ["injury_refresh"]
    assert any(alert["kind"] == "missing" and alert["game_id"] == "MISSING" for alert in plan["alerts"])

    slate = tmp_path / "slate.json"
    slate.write_text(json.dumps({
        "expected_ids": ["G"],
        "games": [{
            "game_id": "G", "season": 2026, "week": 12, "away": "AWY", "home": "HOM",
            "kickoff": utc_iso(game.kickoff_utc), "status": "scheduled",
        }],
    }))
    from scheduler.__main__ import main
    db = tmp_path / "cli.sqlite"
    assert main(["tick", "--db", str(db), "--slate", str(slate), "--now", utc_iso(NOW), "--dry-run"]) == 0
    assert main(["status", "--db", str(db)]) == 0
    quiet = Store(db)
    try:
        assert quiet.count_jobs() == 0
    finally:
        quiet.close()
    assert main(["tick", "--db", str(db), "--slate", str(slate), "--now", utc_iso(NOW)]) == 0
    assert main(["worker", "--db", str(db), "--slate", str(slate), "--now", utc_iso(NOW), "--once"]) == 0
    assert main(["tick", "--db", "postgres://scheduler:secret@example/nfl", "--slate", str(slate)]) == 2
    index_db = tmp_path / "index.sqlite"
    index = ROOT / "pregame" / "packets" / "latest.json"
    assert main(["tick", "--db", str(index_db), "--packet-index", str(index),
                 "--now", "2026-11-20T00:00:00Z", "--dry-run"]) == 0
    opened = Store(index_db)
    try:
        assert opened.count_jobs() == 0
    finally:
        opened.close()


def test_replay_refuses_immutable_lock_and_retries_a_dead_postgame(tmp_path):
    state = {"fail": True}

    class _Toggle:
        def run(self, ctx):
            if state["fail"] and ctx.job["phase"] == "postgame_grade":
                raise RuntimeError("grade failed")
            return HandlerResult(status="recorded", detail="ok")

    orch = _orch(tmp_path, _Toggle(), max_attempts=1)
    kickoff = NOW + timedelta(minutes=80)
    game = _game("G", kickoff)
    orch.tick([game], NOW, owner="a")
    orch.tick([game], kickoff - timedelta(minutes=50), owner="a")
    lock = next(job for job in orch.store.list_jobs("succeeded") if job["phase"] == "prekick_lock")
    refused = orch.replay(lock["id"], kickoff - timedelta(minutes=30))
    assert refused["ok"] is False
    assert orch.store.count_jobs() == 3

    grade_now = kickoff + timedelta(hours=4)
    dead = orch.tick([game], grade_now, owner="a")
    assert dead.missed == 0
    post = next(job for job in orch.store.list_jobs() if job["phase"] == "postgame_grade" and ":replay:" not in job["idempotency_key"])
    assert post["status"] == "dead"
    state["fail"] = False
    replayed = orch.replay(post["id"], grade_now)
    assert replayed["ok"] is True
    ran = orch.claim_and_run("replay", grade_now)
    assert ran[0]["status"] == "succeeded"
    assert ":replay:1" in orch.store.get_job(replayed["job_id"])["idempotency_key"]


def test_rejects_projection_ready_betting_and_oversized_artifacts(tmp_path):
    orch = _orch(tmp_path, Probe(flag="projection_ready"))
    game = _game("G", NOW + timedelta(minutes=80))
    result = orch.tick([game], NOW, owner="a")
    assert result.ran[0]["status"] == "refused"
    job = orch.store.list_jobs("refused")[0]
    receipt = orch.store.receipts_for(job["id"])[-1]
    assert receipt["projection_ready"] == 0
    assert receipt["betting_started"] == 0
    assert receipt["publishing_started"] == 0
    body = json.loads(receipt["body_json"])
    assert body["projection_ready"] is False
    assert "projection_ready" in body["detail"]

    betting = _orch(tmp_path / "bet", Probe(flag="betting_started"))
    assert betting.tick([game], NOW, owner="a").ran[0]["status"] == "refused"

    huge = _orch(tmp_path / "huge", Probe(artifact=b"x" * 256_001))
    assert huge.tick([game], NOW, owner="a").ran[0]["status"] == "refused"
    assert huge.store.artifacts_for(huge.store.receipts_for(huge.store.list_jobs()[0]["id"])[-1]["id"]) == []

    with pytest.raises(sqlite3.IntegrityError):
        orch.store.conn.execute(
            """INSERT INTO receipts (job_id, attempt, status, worker_id, started_at, delay_seconds, body_json,
               projection_ready) VALUES (?,?, 'recorded', 't', ?, 0, '{}', 1)""",
            (job["id"], 9, utc_iso(NOW)),
        )


def test_missing_refused_and_default_runner(tmp_path):
    probe = Probe(refuse=True)
    orch = _orch(tmp_path, probe)
    game = _game("G", NOW + timedelta(minutes=80))
    orch.tick([game], NOW, owner="a", expected_ids=["G", "ABSENT"])
    orch.tick([game], NOW, owner="a", expected_ids=["G", "ABSENT"])
    kinds = {alert["kind"] for alert in orch.store.open_alerts()}
    assert "missing" in kinds
    assert "refused" in kinds
    statuses = {job["phase"]: job["status"] for job in orch.store.list_jobs()}
    assert statuses["injury_refresh"] == "refused"
    assert statuses["prekick_lock"] == "blocked"

    plain = _orch(tmp_path / "plain")
    plain.tick([game], NOW, owner="a")
    job = next(row for row in plain.store.list_jobs("succeeded") if row["phase"] == "injury_refresh")
    receipt = plain.store.receipts_for(job["id"])[-1]
    body = json.loads(receipt["body_json"])
    assert body["analytical_execution"] is False
    assert body["projection_ready"] is False
    artifact = plain.store.artifacts_for(receipt["id"])[0]
    assert artifact["sha256"] == hashlib.sha256(artifact["body"]).hexdigest()
    assert json.loads(artifact["body"])["analytical_execution"] is False


def test_dead_letter_after_repeated_failures(tmp_path):
    orch = _orch(tmp_path, Probe(fail=True), max_attempts=2)
    result = orch.tick([_game("G", NOW + timedelta(minutes=80))], NOW, owner="a")
    assert [row["status"] for row in result.ran] == ["queued", "dead"]
    job = orch.store.list_jobs("dead")[0]
    assert job["attempt"] == 2
    assert [row["status"] for row in orch.store.receipts_for(job["id"])] == ["failed", "failed"]
    assert orch.claim("again", NOW) == []
    assert any(alert["kind"] == "dead" for alert in orch.store.open_alerts())


def test_claimed_job_is_cancelled_when_the_kickoff_moves(tmp_path):
    probe = Probe()
    orch = _orch(tmp_path, probe)
    game = _game("G", NOW + timedelta(minutes=80))
    orch.sync([game], NOW)
    claimed = orch.claim("a", NOW)
    assert claimed
    orch.sync([_game("G", NOW + timedelta(days=2))], NOW)
    finished = orch._execute(claimed[0], "a", NOW)
    assert finished["status"] == "cancelled"
    assert probe.calls == []


def test_schema_matches_the_unapplied_postgres_proposal():
    def columns(sql: str) -> dict[str, list[str]]:
        found = {}
        for match in re.finditer(r"CREATE TABLE(?: IF NOT EXISTS)? (\w+) \((.*?)\);", sql, re.S | re.I):
            cols = []
            for line in match.group(2).splitlines():
                line = line.strip().rstrip(",")
                if not line or line.upper().startswith(("PRIMARY", "FOREIGN", "UNIQUE", "CHECK", "CONSTRAINT")):
                    continue
                cols.append(line.split()[0])
            found[match.group(1)] = cols
        return found

    sqlite_cols = columns(SQLITE_DDL)
    postgres_cols = columns((ROOT / "scheduler" / "schema_postgres.sql").read_text())
    assert sqlite_cols == postgres_cols
    assert "projection_ready" in sqlite_cols["receipts"]


def test_slate_file_roundtrip(tmp_path):
    slate = {
        "games": [{
            "game_id": "G", "season": 2026, "week": 12, "away": "DEN", "home": "PIT",
            "kickoff": "2026-11-29T13:00", "timezone": "America/New_York", "status": "scheduled",
        }],
    }
    games, expected = games_from_slate(slate)
    assert expected is None
    assert utc_iso(games[0].kickoff_utc) == "2026-11-29T18:00:00Z"
