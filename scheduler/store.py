"""SQLite queue. Production Postgres DDL is schema_postgres.sql and is not applied.

Leases use compare-and-swap inside a single immediate transaction: two workers
can both see a queued row, and only one UPDATE matches. The filesystem copy is
for local tests and the dry-run clone. Render's disk is ephemeral, so this file
is not the production store.
"""
from __future__ import annotations

import hashlib
import os
import sqlite3
import tempfile
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta

from .model import BLOCKERS, TERMINAL_FAILURE
from .timeutil import ScheduleError, utc_iso

SQLITE_DDL = """
CREATE TABLE IF NOT EXISTS games (
    game_id TEXT PRIMARY KEY,
    season INTEGER NOT NULL,
    week INTEGER NOT NULL,
    away TEXT NOT NULL,
    home TEXT NOT NULL,
    kickoff_utc TEXT NOT NULL,
    timezone TEXT NOT NULL,
    status TEXT NOT NULL,
    schedule_version TEXT NOT NULL,
    discovered_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    game_id TEXT NOT NULL,
    phase TEXT NOT NULL,
    schedule_version TEXT NOT NULL,
    not_before_utc TEXT NOT NULL,
    deadline_utc TEXT NOT NULL,
    status TEXT NOT NULL,
    attempt INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL,
    lease_owner TEXT,
    lease_until_utc TEXT,
    heartbeat_utc TEXT,
    heavy INTEGER NOT NULL,
    immutable INTEGER NOT NULL,
    payload_json TEXT NOT NULL,
    last_error TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    finished_at TEXT
);

CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL,
    attempt INTEGER NOT NULL,
    status TEXT NOT NULL,
    worker_id TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    delay_seconds INTEGER NOT NULL,
    body_json TEXT NOT NULL,
    projection_ready INTEGER NOT NULL DEFAULT 0 CHECK (projection_ready = 0),
    betting_started INTEGER NOT NULL DEFAULT 0 CHECK (betting_started = 0),
    publishing_started INTEGER NOT NULL DEFAULT 0 CHECK (publishing_started = 0)
);

CREATE TABLE IF NOT EXISTS artifacts (
    id INTEGER PRIMARY KEY,
    receipt_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    body BLOB NOT NULL
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY,
    game_id TEXT,
    kind TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL,
    acknowledged INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS refresh_log (
    id INTEGER PRIMARY KEY,
    at_utc TEXT NOT NULL,
    game_count INTEGER NOT NULL,
    created_jobs INTEGER NOT NULL,
    body_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS jobs_status_due ON jobs (status, not_before_utc, deadline_utc);
CREATE INDEX IF NOT EXISTS jobs_game_phase ON jobs (game_id, phase, schedule_version);
CREATE INDEX IF NOT EXISTS alerts_open ON alerts (kind, game_id, acknowledged);
"""

MAX_ARTIFACT_BYTES = 256_000


class Store:
    def __init__(self, path: str | os.PathLike):
        self.path = str(path)
        self._temp = False
        self.conn = sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")
        self.conn.executescript(SQLITE_DDL)

    def close(self) -> None:
        self.conn.close()
        if self._temp and os.path.exists(self.path):
            os.unlink(self.path)

    def clone(self) -> "Store":
        fd, name = tempfile.mkstemp(prefix="scheduler-dry-", suffix=".sqlite")
        os.close(fd)
        dest = sqlite3.connect(name)
        with self.lock:
            self.conn.backup(dest)
        dest.close()
        cloned = Store(name)
        cloned._temp = True
        return cloned

    @contextmanager
    def _tx(self):
        with self.lock:
            self.conn.execute("BEGIN IMMEDIATE")
            try:
                yield self.conn
            except Exception:
                self.conn.execute("ROLLBACK")
                raise
            else:
                self.conn.execute("COMMIT")

    def _alert(self, c, now: str, kind: str, message: str, game_id: str | None) -> None:
        row = c.execute(
            """SELECT id FROM alerts
               WHERE kind=? AND acknowledged=0 AND ifnull(game_id,'')=ifnull(?, '') AND message=?""",
            (kind, game_id, message),
        ).fetchone()
        if row:
            return
        c.execute(
            "INSERT INTO alerts (game_id, kind, message, created_at, acknowledged) VALUES (?,?,?,?,0)",
            (game_id, kind, message, now),
        )

    def apply_schedule(self, games: list, desired: list, now: datetime, expected_ids: list[str] | None,
                       max_attempts: int) -> dict:
        stamp = utc_iso(now)
        seen: set[str] = set()
        for game in games:
            if game.game_id in seen:
                raise ScheduleError(f"duplicate game_id in schedule: {game.game_id}")
            seen.add(game.game_id)
        created = superseded = cancelled = 0
        with self._tx() as c:
            for game in games:
                version = game.version()
                current = c.execute("SELECT schedule_version, discovered_at FROM games WHERE game_id=?",
                                    (game.game_id,)).fetchone()
                if current is None:
                    c.execute(
                        """INSERT INTO games (game_id, season, week, away, home, kickoff_utc, timezone, status,
                           schedule_version, discovered_at, updated_at)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                        (game.game_id, game.season, game.week, game.away, game.home, utc_iso(game.kickoff_utc),
                         game.timezone, game.status, version, stamp, stamp),
                    )
                else:
                    c.execute(
                        """UPDATE games SET season=?, week=?, away=?, home=?, kickoff_utc=?, timezone=?, status=?,
                           schedule_version=?, updated_at=? WHERE game_id=?""",
                        (game.season, game.week, game.away, game.home, utc_iso(game.kickoff_utc), game.timezone,
                         game.status, version, stamp, game.game_id),
                    )
                if game.status in ("postponed", "cancelled"):
                    cur = c.execute(
                        """UPDATE jobs SET status='cancelled', lease_owner=NULL, lease_until_utc=NULL,
                           finished_at=?, updated_at=?, last_error=?
                           WHERE game_id=? AND status IN ('queued','blocked')""",
                        (stamp, stamp, game.status, game.game_id),
                    )
                    cancelled += cur.rowcount
                    self._alert(c, stamp, game.status, f"{game.game_id} marked {game.status}; queued phases cancelled",
                                game.game_id)
                    continue
                cur = c.execute(
                    """UPDATE jobs SET status='superseded', lease_owner=NULL, lease_until_utc=NULL,
                       finished_at=?, updated_at=?
                       WHERE game_id=? AND status IN ('queued','blocked') AND schedule_version!=?""",
                    (stamp, stamp, game.game_id, version),
                )
                superseded += cur.rowcount
            for job in desired:
                existing = c.execute(
                    "SELECT id, status FROM jobs WHERE idempotency_key=?", (job.idempotency_key,)
                ).fetchone()
                if existing is None:
                    c.execute(
                        """INSERT INTO jobs (idempotency_key, game_id, phase, schedule_version, not_before_utc,
                           deadline_utc, status, attempt, max_attempts, heavy, immutable, payload_json,
                           created_at, updated_at)
                           VALUES (?,?,?,?,?,?, 'queued', 0, ?, ?, ?, ?, ?, ?)""",
                        (job.idempotency_key, job.game_id, job.phase, job.schedule_version,
                         utc_iso(job.not_before_utc), utc_iso(job.deadline_utc), max_attempts, int(job.heavy),
                         int(job.immutable), job.payload_json, stamp, stamp),
                    )
                    created += 1
                elif existing["status"] == "queued":
                    c.execute(
                        """UPDATE jobs SET not_before_utc=?, deadline_utc=?, payload_json=?, updated_at=?
                           WHERE id=? AND status='queued'""",
                        (utc_iso(job.not_before_utc), utc_iso(job.deadline_utc), job.payload_json, stamp,
                         existing["id"]),
                    )
            if expected_ids is not None:
                for game_id in expected_ids:
                    if game_id not in seen:
                        self._alert(c, stamp, "missing", f"{game_id} missing from schedule discovery", game_id)
            c.execute(
                "INSERT INTO refresh_log (at_utc, game_count, created_jobs, body_json) VALUES (?,?,?,?)",
                (stamp, len(games), created, "{}"),
            )
        return {"created": created, "superseded": superseded, "cancelled": cancelled, "games": len(games)}

    def list_jobs(self, status: str | None = None) -> list[dict]:
        with self.lock:
            if status is None:
                rows = self.conn.execute("SELECT * FROM jobs ORDER BY id").fetchall()
            else:
                rows = self.conn.execute("SELECT * FROM jobs WHERE status=? ORDER BY id", (status,)).fetchall()
        return [dict(row) for row in rows]

    def get_job(self, job_id: int) -> dict | None:
        with self.lock:
            row = self.conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        return dict(row) if row else None

    def get_game(self, game_id: str) -> dict | None:
        with self.lock:
            row = self.conn.execute("SELECT * FROM games WHERE game_id=?", (game_id,)).fetchone()
        return dict(row) if row else None

    def count_jobs(self) -> int:
        with self.lock:
            return self.conn.execute("SELECT count(*) FROM jobs").fetchone()[0]

    def open_alerts(self) -> list[dict]:
        with self.lock:
            rows = self.conn.execute(
                "SELECT * FROM alerts WHERE acknowledged=0 ORDER BY id"
            ).fetchall()
        return [dict(row) for row in rows]

    def receipts_for(self, job_id: int) -> list[dict]:
        with self.lock:
            rows = self.conn.execute(
                "SELECT * FROM receipts WHERE job_id=? ORDER BY id", (job_id,)
            ).fetchall()
        return [dict(row) for row in rows]

    def artifacts_for(self, receipt_id: int) -> list[dict]:
        with self.lock:
            rows = self.conn.execute(
                "SELECT id, receipt_id, name, sha256, body FROM artifacts WHERE receipt_id=? ORDER BY id",
                (receipt_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def refresh_count(self) -> int:
        with self.lock:
            return self.conn.execute("SELECT count(*) FROM refresh_log").fetchone()[0]

    def succeeded_immutable(self, game_id: str, phase: str, schedule_version: str) -> bool:
        with self.lock:
            row = self.conn.execute(
                """SELECT id FROM jobs WHERE game_id=? AND phase=? AND schedule_version=?
                   AND status='succeeded' AND immutable=1""",
                (game_id, phase, schedule_version),
            ).fetchone()
        return row is not None

    def replay_count(self, game_id: str, phase: str, schedule_version: str) -> int:
        prefix = f"{game_id}:{phase}:{schedule_version}:replay:%"
        with self.lock:
            return self.conn.execute(
                "SELECT count(*) FROM jobs WHERE game_id=? AND phase=? AND idempotency_key LIKE ?",
                (game_id, phase, prefix),
            ).fetchone()[0]

    def insert_replay(self, source: dict, now: datetime, deadline: datetime, key: str, max_attempts: int) -> int:
        stamp = utc_iso(now)
        with self._tx() as c:
            cur = c.execute(
                """INSERT INTO jobs (idempotency_key, game_id, phase, schedule_version, not_before_utc,
                   deadline_utc, status, attempt, max_attempts, heavy, immutable, payload_json, created_at, updated_at)
                   VALUES (?,?,?,?,?,?, 'queued', 0, ?, ?, ?, ?, ?, ?)""",
                (key, source["game_id"], source["phase"], source["schedule_version"], stamp, utc_iso(deadline),
                 max_attempts, source["heavy"], source["immutable"], source["payload_json"], stamp, stamp),
            )
            return int(cur.lastrowid)

    def recover(self, now: datetime) -> list[dict]:
        stamp = utc_iso(now)
        changed = []
        with self._tx() as c:
            rows = c.execute(
                """SELECT * FROM jobs WHERE status='leased' AND lease_until_utc IS NOT NULL AND lease_until_utc<=?""",
                (stamp,),
            ).fetchall()
            for row in rows:
                job = dict(row)
                c.execute(
                    """UPDATE receipts SET status='crashed', finished_at=?
                       WHERE job_id=? AND attempt=? AND status='running'""",
                    (stamp, job["id"], job["attempt"]),
                )
                if job["attempt"] >= job["max_attempts"] or stamp >= job["deadline_utc"]:
                    status = "dead" if job["attempt"] >= job["max_attempts"] else "missed"
                    c.execute(
                        """UPDATE jobs SET status=?, lease_owner=NULL, lease_until_utc=NULL, finished_at=?, updated_at=?,
                           last_error=? WHERE id=?""",
                        (status, stamp, stamp, "lease expired", job["id"]),
                    )
                    kind = "dead" if status == "dead" else "missed"
                    self._alert(c, stamp, kind, f"{job['game_id']} {job['phase']} {status} after lease expiry",
                                job["game_id"])
                else:
                    c.execute(
                        """UPDATE jobs SET status='queued', lease_owner=NULL, lease_until_utc=NULL, updated_at=?,
                           last_error='lease expired' WHERE id=?""",
                        (stamp, job["id"]),
                    )
                changed.append(job["id"])
        return changed

    def sweep(self, now: datetime) -> dict:
        stamp = utc_iso(now)
        missed = blocked = 0
        with self._tx() as c:
            rows = c.execute(
                """SELECT * FROM jobs WHERE status IN ('queued','blocked') AND deadline_utc<=?""",
                (stamp,),
            ).fetchall()
            for row in rows:
                c.execute(
                    """UPDATE jobs SET status='missed', finished_at=?, updated_at=?, last_error='window closed'
                       WHERE id=? AND status IN ('queued','blocked')""",
                    (stamp, stamp, row["id"]),
                )
                missed += 1
                self._alert(c, stamp, "missed", f"{row['game_id']} {row['phase']} missed its window", row["game_id"])
            locks = c.execute(
                "SELECT * FROM jobs WHERE status='queued' AND phase=?", ("prekick_lock",)
            ).fetchall()
            for lock in locks:
                injury = c.execute(
                    """SELECT status FROM jobs WHERE game_id=? AND phase='injury_refresh' AND schedule_version=?
                       ORDER BY id DESC LIMIT 1""",
                    (lock["game_id"], lock["schedule_version"]),
                ).fetchone()
                if injury and injury["status"] in TERMINAL_FAILURE:
                    c.execute(
                        """UPDATE jobs SET status='blocked', updated_at=?, last_error=?
                           WHERE id=? AND status='queued'""",
                        (stamp, f"injury_refresh {injury['status']}", lock["id"]),
                    )
                    blocked += 1
                    self._alert(
                        c, stamp, "blocked",
                        f"{lock['game_id']} prekick_lock blocked because injury_refresh {injury['status']}",
                        lock["game_id"],
                    )
        return {"missed": missed, "blocked": blocked}

    def claim(self, owner: str, now: datetime, ttl: timedelta, limit: int, heavy_limit: int) -> list[dict]:
        stamp = utc_iso(now)
        until = utc_iso(now + ttl)
        taken: list[dict] = []
        with self._tx() as c:
            in_flight = c.execute(
                """SELECT phase FROM jobs WHERE status='leased' AND lease_until_utc>?""",
                (stamp,),
            ).fetchall()
            slots = limit - len(in_flight)
            heavy_slots = heavy_limit - sum(1 for row in in_flight if row["phase"] in _heavy_names())
            if slots <= 0:
                return []
            rows = c.execute(
                """SELECT * FROM jobs WHERE status='queued' AND not_before_utc<=? AND deadline_utc>?
                   ORDER BY deadline_utc, id""",
                (stamp, stamp),
            ).fetchall()
            heavy_taken = 0
            for row in rows:
                if len(taken) >= slots:
                    break
                job = dict(row)
                if job["phase"] in _heavy_names():
                    if heavy_slots - heavy_taken <= 0:
                        continue
                if not _dependency_met(c, job):
                    continue
                overlap = c.execute(
                    """SELECT id FROM jobs WHERE game_id=? AND phase=? AND status='leased' AND lease_until_utc>?""",
                    (job["game_id"], job["phase"], stamp),
                ).fetchone()
                if overlap:
                    continue
                cur = c.execute(
                    """UPDATE jobs SET status='leased', lease_owner=?, lease_until_utc=?, heartbeat_utc=?,
                       attempt=attempt+1, updated_at=?
                       WHERE id=? AND status='queued'""",
                    (owner, until, stamp, stamp, job["id"]),
                )
                if cur.rowcount != 1:
                    continue
                updated = dict(c.execute("SELECT * FROM jobs WHERE id=?", (job["id"],)).fetchone())
                delay = int((now - _parse(updated["not_before_utc"])).total_seconds())
                c.execute(
                    """INSERT INTO receipts (job_id, attempt, status, worker_id, started_at, delay_seconds, body_json,
                       projection_ready, betting_started, publishing_started)
                       VALUES (?,?, 'running', ?, ?, ?, '{}', 0, 0, 0)""",
                    (updated["id"], updated["attempt"], owner, stamp, max(0, delay)),
                )
                taken.append(updated)
                if updated["phase"] in _heavy_names():
                    heavy_taken += 1
        return taken

    def heartbeat(self, job_id: int, owner: str, now: datetime, ttl: timedelta) -> bool:
        stamp = utc_iso(now)
        until = utc_iso(now + ttl)
        with self._tx() as c:
            cur = c.execute(
                """UPDATE jobs SET lease_until_utc=?, heartbeat_utc=?, updated_at=?
                   WHERE id=? AND status='leased' AND lease_owner=?""",
                (until, stamp, stamp, job_id, owner),
            )
            return cur.rowcount == 1

    def finish(self, job_id: int, owner: str, attempt: int, now: datetime, job_status: str,
               receipt_status: str, body_json: str, last_error: str | None,
               artifacts: list[tuple[str, bytes, str]]) -> bool:
        stamp = utc_iso(now)
        with self._tx() as c:
            cur = c.execute(
                """UPDATE jobs SET status=?, lease_owner=NULL, lease_until_utc=NULL, finished_at=?, updated_at=?,
                   last_error=?
                   WHERE id=? AND status='leased' AND lease_owner=? AND attempt=?""",
                (job_status, stamp, stamp, last_error, job_id, owner, attempt),
            )
            if cur.rowcount != 1:
                c.execute(
                    """UPDATE receipts SET status='orphaned', finished_at=?, body_json=?
                       WHERE job_id=? AND attempt=? AND status='running' AND worker_id=?""",
                    (stamp, body_json, job_id, attempt, owner),
                )
                return False
            rec = c.execute(
                """SELECT id FROM receipts WHERE job_id=? AND attempt=? AND status='running' AND worker_id=?""",
                (job_id, attempt, owner),
            ).fetchone()
            if rec is None:
                return False
            c.execute(
                "UPDATE receipts SET status=?, finished_at=?, body_json=? WHERE id=?",
                (receipt_status, stamp, body_json, rec["id"]),
            )
            for name, body, digest in artifacts:
                c.execute(
                    "INSERT INTO artifacts (receipt_id, name, sha256, body) VALUES (?,?,?,?)",
                    (rec["id"], name, digest, body),
                )
            return True

    def release_for_retry(self, job_id: int, owner: str, attempt: int, now: datetime, error: str,
                          body_json: str) -> str:
        """Return the resulting job status: queued or dead."""
        stamp = utc_iso(now)
        with self._tx() as c:
            job = c.execute(
                "SELECT * FROM jobs WHERE id=? AND status='leased' AND lease_owner=? AND attempt=?",
                (job_id, owner, attempt),
            ).fetchone()
            if job is None:
                c.execute(
                    """UPDATE receipts SET status='orphaned', finished_at=?, body_json=?
                       WHERE job_id=? AND attempt=? AND status='running' AND worker_id=?""",
                    (stamp, body_json, job_id, attempt, owner),
                )
                return "orphaned"
            status = "dead" if job["attempt"] >= job["max_attempts"] else "queued"
            if status == "dead":
                c.execute(
                    """UPDATE jobs SET status='dead', lease_owner=NULL, lease_until_utc=NULL, finished_at=?,
                       updated_at=?, last_error=? WHERE id=?""",
                    (stamp, stamp, error, job_id),
                )
                self._alert(c, stamp, "dead", f"{job['game_id']} {job['phase']} dead: {error}", job["game_id"])
            else:
                c.execute(
                    """UPDATE jobs SET status='queued', lease_owner=NULL, lease_until_utc=NULL, updated_at=?,
                       last_error=? WHERE id=?""",
                    (stamp, error, job_id),
                )
            c.execute(
                """UPDATE receipts SET status='failed', finished_at=?, body_json=?
                   WHERE job_id=? AND attempt=? AND status='running' AND worker_id=?""",
                (stamp, body_json, job_id, attempt, owner),
            )
            return status

    def alert(self, kind: str, message: str, game_id: str | None, now: datetime) -> None:
        with self._tx() as c:
            self._alert(c, utc_iso(now), kind, message, game_id)

    def backpressure_open(self) -> bool:
        with self.lock:
            row = self.conn.execute(
                "SELECT id FROM alerts WHERE kind='backpressure' AND acknowledged=0"
            ).fetchone()
        return row is not None

    def queued_heavy(self, now: datetime) -> list[dict]:
        stamp = utc_iso(now)
        with self.lock:
            rows = self.conn.execute(
                """SELECT * FROM jobs WHERE status='queued' AND heavy=1 AND not_before_utc<=? AND deadline_utc>?
                   ORDER BY deadline_utc, id""",
                (stamp, stamp),
            ).fetchall()
        return [dict(row) for row in rows]


def _heavy_names() -> frozenset[str]:
    from .model import HEAVY_PHASES
    return HEAVY_PHASES


def _parse(value: str) -> datetime:
    from .timeutil import parse_utc_iso
    return parse_utc_iso(value)


def _dependency_met(c, job: dict) -> bool:
    needed = BLOCKERS.get(job["phase"])
    if not needed:
        return True
    phase, status = needed
    row = c.execute(
        """SELECT status FROM jobs WHERE game_id=? AND phase=? AND schedule_version=?
           ORDER BY id DESC LIMIT 1""",
        (job["game_id"], phase, job["schedule_version"]),
    ).fetchone()
    return row is not None and row["status"] == status


def artifact_digest(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()
