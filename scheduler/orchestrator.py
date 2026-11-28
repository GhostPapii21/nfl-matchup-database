"""Schedule sync, lease, and one-attempt execution.

tick() is the production step: refresh the slate, close expired leases, mark
missed windows, then run due jobs inside the concurrency caps. dry_run()
applies that plan to a throwaway copy of the queue and does not call a
handler. replay() enqueues a new idempotency key and will not replace a
succeeded pre-kick lock.
"""
from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .model import PHASES, DesiredJob, Game, idempotency_key, phase_window
from .runner import HandlerResult, JobContext, Runner, UnwiredRunner, reject_reason
from .store import MAX_ARTIFACT_BYTES, Store, artifact_digest
from .timeutil import ScheduleError, parse_utc_iso, utc_iso


@dataclass
class TickResult:
    created: int = 0
    superseded: int = 0
    cancelled: int = 0
    recovered: int = 0
    missed: int = 0
    blocked: int = 0
    ran: list[dict] = field(default_factory=list)
    backpressure: bool = False


class Orchestrator:
    def __init__(self, store: Store, runner: Runner | None = None, *, max_in_flight: int = 2,
                 max_heavy: int = 1, lease_ttl: timedelta = timedelta(seconds=60), max_attempts: int = 3,
                 assumed_heavy_seconds: int = 0, artifact_limit: int = MAX_ARTIFACT_BYTES):
        if max_in_flight < 1 or max_heavy < 1:
            raise ScheduleError("concurrency caps must be at least 1")
        if max_heavy > max_in_flight:
            raise ScheduleError("max_heavy cannot exceed max_in_flight")
        self.store = store
        self.runner = runner or UnwiredRunner()
        self.max_in_flight = max_in_flight
        self.max_heavy = max_heavy
        self.lease_ttl = lease_ttl
        self.max_attempts = max_attempts
        self.assumed_heavy_seconds = assumed_heavy_seconds
        self.artifact_limit = artifact_limit

    def sync(self, games: list[Game], now: datetime, expected_ids: list[str] | None = None) -> dict:
        desired = []
        active = []
        for game in games:
            if game.status in ("postponed", "cancelled"):
                active.append(game)
                continue
            active.append(game)
            version = game.version()
            for phase in PHASES:
                not_before, deadline = phase_window(phase, game, now)
                payload = {
                    "game_id": game.game_id,
                    "phase": phase.name,
                    "kickoff_utc": utc_iso(game.kickoff_utc),
                    "schedule_version": version,
                    "workload_class": "simulation_300k" if phase.heavy else "light",
                    "analytical_execution": False,
                    "projection_ready": False,
                }
                desired.append(DesiredJob(
                    game_id=game.game_id,
                    phase=phase.name,
                    schedule_version=version,
                    not_before_utc=not_before,
                    deadline_utc=deadline,
                    heavy=phase.heavy,
                    immutable=phase.immutable,
                    idempotency_key=idempotency_key(game.game_id, phase.name, version),
                    payload_json=json.dumps(payload, sort_keys=True),
                ))
        return self.store.apply_schedule(active, desired, now, expected_ids, self.max_attempts)

    def recover(self, now: datetime) -> list[int]:
        return self.store.recover(now)

    def sweep(self, now: datetime) -> dict:
        return self.store.sweep(now)

    def assess_backpressure(self, now: datetime) -> bool:
        if self.assumed_heavy_seconds <= 0:
            return False
        queued = self.store.queued_heavy(now)
        if not queued:
            return False
        earliest = min(parse_utc_iso(job["deadline_utc"]) for job in queued)
        slack = (earliest - now).total_seconds()
        demand = len(queued) * self.assumed_heavy_seconds
        # One heavy slot is the cap, so the queue cannot drain faster than that.
        if demand <= slack * self.max_heavy:
            return False
        self.store.alert(
            "backpressure",
            (f"{len(queued)} heavy jobs need about {demand}s and the earliest deadline "
             f"leaves {int(slack)}s at concurrency {self.max_heavy}"),
            None,
            now,
        )
        return True

    def claim(self, owner: str, now: datetime) -> list[dict]:
        return self.store.claim(owner, now, self.lease_ttl, self.max_in_flight, self.max_heavy)

    def claim_and_run(self, owner: str, now: datetime, *, parallel: bool = False) -> list[dict]:
        claimed = self.claim(owner, now)
        if not claimed:
            return []
        if not parallel or len(claimed) == 1:
            return [self._execute(job, owner, now) for job in claimed]
        results: list[dict | None] = [None] * len(claimed)

        def _go(index: int, job: dict) -> None:
            results[index] = self._execute(job, owner, now)

        threads = [threading.Thread(target=_go, args=(i, job)) for i, job in enumerate(claimed)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return [row for row in results if row is not None]

    def tick(self, games: list[Game], now: datetime, owner: str = "local",
             expected_ids: list[str] | None = None, *, parallel: bool = False) -> TickResult:
        recovered = self.recover(now)
        synced = self.sync(games, now, expected_ids)
        swept = self.sweep(now)
        pressure = self.assess_backpressure(now)
        ran = self._drain(owner, now, parallel=parallel)
        # A refusal during the drain can block a later phase that sweep has not seen yet.
        swept_after = self.sweep(now)
        return TickResult(
            created=synced["created"],
            superseded=synced["superseded"],
            cancelled=synced["cancelled"],
            recovered=len(recovered),
            missed=swept["missed"] + swept_after["missed"],
            blocked=swept["blocked"] + swept_after["blocked"],
            ran=ran,
            backpressure=pressure,
        )

    def dry_run(self, games: list[Game], now: datetime, expected_ids: list[str] | None = None) -> dict:
        """Plan the tick on a copy. The live queue and the handler are not touched."""
        clone = self.store.clone()
        try:
            shadow = Orchestrator(
                clone,
                runner=_DryRunRunner(),
                max_in_flight=self.max_in_flight,
                max_heavy=self.max_heavy,
                lease_ttl=self.lease_ttl,
                max_attempts=self.max_attempts,
                assumed_heavy_seconds=self.assumed_heavy_seconds,
                artifact_limit=self.artifact_limit,
            )
            shadow.recover(now)
            synced = shadow.sync(games, now, expected_ids)
            swept = shadow.sweep(now)
            pressure = shadow.assess_backpressure(now)
            claimable = [
                {"id": job["id"], "game_id": job["game_id"], "phase": job["phase"],
                 "idempotency_key": job["idempotency_key"]}
                for job in shadow.claim(owner="dry-run", now=now)
            ]
            return {
                "created": synced["created"],
                "superseded": synced["superseded"],
                "cancelled": synced["cancelled"],
                "missed": swept["missed"],
                "blocked": swept["blocked"],
                "backpressure": pressure,
                "would_claim": claimable,
                "alerts": clone.open_alerts(),
            }
        finally:
            clone.close()

    def replay(self, job_id: int, now: datetime) -> dict:
        job = self.store.get_job(job_id)
        if job is None:
            raise ScheduleError(f"no job {job_id}")
        if job["status"] in ("queued", "leased"):
            return {"ok": False, "reason": "job is still open", "job_id": job_id}
        game = self.store.get_game(job["game_id"])
        if game is None:
            raise ScheduleError(f"job {job_id} has no game row")
        kickoff = parse_utc_iso(game["kickoff_utc"])
        if job["immutable"] and self.store.succeeded_immutable(job["game_id"], job["phase"], job["schedule_version"]):
            self.store.alert("refused", f"{job['game_id']} {job['phase']} replay refused; lock is immutable",
                             job["game_id"], now)
            return {"ok": False, "reason": "immutable lock already succeeded", "job_id": job_id}
        if job["phase"] == "prekick_lock" and now >= kickoff:
            self.store.alert("refused", f"{job['game_id']} prekick_lock replay refused; kickoff has passed",
                             job["game_id"], now)
            return {"ok": False, "reason": "kickoff has passed", "job_id": job_id}
        deadline = parse_utc_iso(job["deadline_utc"])
        if job["phase"] == "prekick_lock":
            replay_deadline = deadline
        elif now < deadline:
            replay_deadline = deadline
        else:
            replay_deadline = now + timedelta(minutes=15)
        if replay_deadline <= now:
            return {"ok": False, "reason": "replay deadline is not in the future", "job_id": job_id}
        number = self.store.replay_count(job["game_id"], job["phase"], job["schedule_version"]) + 1
        key = idempotency_key(job["game_id"], job["phase"], job["schedule_version"], replay=number)
        new_id = self.store.insert_replay(job, now, replay_deadline, key, self.max_attempts)
        return {"ok": True, "job_id": new_id, "idempotency_key": key}

    def _drain(self, owner: str, now: datetime, *, parallel: bool) -> list[dict]:
        ran: list[dict] = []
        while True:
            batch = self.claim_and_run(owner, now, parallel=parallel)
            if not batch:
                return ran
            ran.extend(batch)

    def _execute(self, job: dict, owner: str, now: datetime) -> dict:
        game = self.store.get_game(job["game_id"])
        if game is None:
            raise ScheduleError(f"job {job['id']} has no game row")
        if game["status"] in ("postponed", "cancelled") or game["schedule_version"] != job["schedule_version"]:
            reason = f"schedule is {game['status']} at {game['schedule_version']}"
            self.store.finish(job["id"], owner, job["attempt"], now, "cancelled", "cancelled",
                              json.dumps({"detail": reason, "projection_ready": False}), reason, [])
            return {"job_id": job["id"], "status": "cancelled", "detail": reason}
        stop = threading.Event()

        def _beat() -> None:
            while not stop.wait(self.lease_ttl.total_seconds() / 3):
                self.store.heartbeat(job["id"], owner, datetime.now(now.tzinfo), self.lease_ttl)

        beater = threading.Thread(target=_beat, daemon=True)
        beater.start()
        try:
            ctx = JobContext(
                job,
                self.store.get_game(job["game_id"]),
                now,
                lambda at: self.store.heartbeat(job["id"], owner, at, self.lease_ttl),
            )
            try:
                result = self.runner.run(ctx)
            except Exception as exc:
                result = HandlerResult(status="failed", detail=f"{type(exc).__name__}: {exc}")
            return self._settle(job, owner, now, result)
        finally:
            stop.set()
            beater.join(timeout=1)

    def _settle(self, job: dict, owner: str, now: datetime, result: HandlerResult) -> dict:
        body = {
            "detail": result.detail,
            "analytical_execution": bool(result.analytical_execution),
            "projection_ready": False,
            "betting_started": False,
            "publishing_started": False,
            "handler_status": result.status,
            "phase": job["phase"],
            "game_id": job["game_id"],
            "attempt": job["attempt"],
            "delay_seconds": _delay(job, now),
        }
        blocked = reject_reason(result)
        if blocked:
            self.store.alert("refused", f"{job['game_id']} {job['phase']} {blocked}", job["game_id"], now)
            kept = self.store.finish(
                job["id"], owner, job["attempt"], now, "refused", "refused",
                json.dumps({**body, "detail": blocked}), blocked, [],
            )
            return {"job_id": job["id"], "status": "refused" if kept else "orphaned", "detail": blocked}
        if result.status == "failed":
            status = self.store.release_for_retry(job["id"], owner, job["attempt"], now, result.detail,
                                                   json.dumps(body))
            return {"job_id": job["id"], "status": status, "detail": result.detail}
        if result.status == "refused":
            self.store.alert("refused", f"{job['game_id']} {job['phase']} refused: {result.detail}",
                             job["game_id"], now)
            artifacts = self._pack_artifacts(result)
            if isinstance(artifacts, str):
                self.store.alert("refused", f"{job['game_id']} {job['phase']} {artifacts}", job["game_id"], now)
                self.store.finish(job["id"], owner, job["attempt"], now, "refused", "refused",
                                  json.dumps({**body, "detail": artifacts}), artifacts, [])
                return {"job_id": job["id"], "status": "refused", "detail": artifacts}
            kept = self.store.finish(
                job["id"], owner, job["attempt"], now, "refused", "refused",
                json.dumps(body), result.detail, artifacts,
            )
            return {"job_id": job["id"], "status": "refused" if kept else "orphaned", "detail": result.detail}
        if result.status != "recorded":
            status = self.store.release_for_retry(
                job["id"], owner, job["attempt"], now, f"unknown handler status {result.status}", json.dumps(body),
            )
            return {"job_id": job["id"], "status": status, "detail": f"unknown handler status {result.status}"}
        artifacts = self._pack_artifacts(result)
        if isinstance(artifacts, str):
            self.store.alert("refused", f"{job['game_id']} {job['phase']} {artifacts}", job["game_id"], now)
            self.store.finish(job["id"], owner, job["attempt"], now, "refused", "refused",
                              json.dumps({**body, "detail": artifacts}), artifacts, [])
            return {"job_id": job["id"], "status": "refused", "detail": artifacts}
        kept = self.store.finish(
            job["id"], owner, job["attempt"], now, "succeeded", "recorded",
            json.dumps(body), None, artifacts,
        )
        return {"job_id": job["id"], "status": "succeeded" if kept else "orphaned", "detail": result.detail}

    def _pack_artifacts(self, result: HandlerResult) -> list[tuple[str, bytes, str]] | str:
        packed = []
        for name, body in result.artifacts.items():
            if not name or "/" in name or "\\" in name or name != name.strip("."):
                return f"artifact name {name!r} is not a single file name"
            if not isinstance(body, (bytes, bytearray)):
                return f"artifact {name} is not bytes"
            if len(body) > self.artifact_limit:
                return (f"artifact {name} is {len(body)} bytes; the receipt store holds at most "
                        f"{self.artifact_limit}. Object storage is not configured, so the 300k output is refused.")
            packed.append((name, bytes(body), artifact_digest(bytes(body))))
        return packed


class _DryRunRunner:
    def run(self, ctx: JobContext) -> HandlerResult:
        raise ScheduleError("dry-run claimed a job; the handler must not run")


def _delay(job: dict, now: datetime) -> int:
    return max(0, int((now - parse_utc_iso(job["not_before_utc"])).total_seconds()))


def open_store(path: str) -> Store:
    lowered = path.lower()
    if lowered.startswith("postgres://") or lowered.startswith("postgresql://"):
        raise ScheduleError(
            "Refusing a Postgres URL. Production database writes are not approved (NFL-84). "
            "Use a local SQLite path."
        )
    return Store(path)
