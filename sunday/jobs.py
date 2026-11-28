"""Local durable game jobs. This is not GitHub Actions and it is not deployed.

Jobs live in a sqlite file. A duplicate idempotency key returns the existing
row. An expired lease can be claimed again after a crash. An inactive lock
refuses a later injury refresh for that game. Nothing here starts a bet or
sets projection_ready.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def _parse(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


class JobStore:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                idempotency_key TEXT PRIMARY KEY,
                game_id TEXT NOT NULL,
                window TEXT NOT NULL,
                status TEXT NOT NULL,
                lease_owner TEXT,
                lease_expires TEXT,
                deadline TEXT,
                inactive_lock TEXT,
                attempts INTEGER NOT NULL,
                result TEXT
            )
            """
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def enqueue(self, *, game_id: str, window: str, idempotency_key: str, deadline: datetime | None = None) -> dict:
        existing = self._one(idempotency_key)
        if existing:
            return {**existing, "duplicate": True}
        lock = self._lock(game_id)
        if window == "inactive_refresh" and lock:
            return {
                "idempotency_key": idempotency_key,
                "game_id": game_id,
                "window": window,
                "status": "REFUSED",
                "reason": "inactive list is locked; a later refresh was not queued",
                "inactive_lock": lock,
                "duplicate": False,
                "projection_ready": False,
            }
        self.conn.execute(
            """
            INSERT INTO jobs (idempotency_key, game_id, window, status, attempts, deadline)
            VALUES (?, ?, ?, 'queued', 0, ?)
            """,
            (idempotency_key, game_id, window, _iso(deadline) if deadline else None),
        )
        self.conn.commit()
        return {**self._one(idempotency_key), "duplicate": False}

    def claim(self, owner: str, now: datetime, lease_seconds: int = 60) -> dict | None:
        self.recover_expired(now)
        row = self.conn.execute(
            "SELECT * FROM jobs WHERE status = 'queued' ORDER BY idempotency_key LIMIT 1"
        ).fetchone()
        if row is None:
            return None
        expires = _iso(now + timedelta(seconds=lease_seconds))
        self.conn.execute(
            """
            UPDATE jobs
               SET status = 'leased', lease_owner = ?, lease_expires = ?, attempts = attempts + 1
             WHERE idempotency_key = ? AND status = 'queued'
            """,
            (owner, expires, row["idempotency_key"]),
        )
        self.conn.commit()
        return self._one(row["idempotency_key"])

    def heartbeat(self, key: str, owner: str, now: datetime, lease_seconds: int = 60) -> dict:
        row = self._one(key)
        if not row or row["lease_owner"] != owner or row["status"] != "leased":
            raise ValueError("heartbeat refused; this owner does not hold the lease")
        expires = _iso(now + timedelta(seconds=lease_seconds))
        self.conn.execute(
            "UPDATE jobs SET lease_expires = ? WHERE idempotency_key = ?",
            (expires, key),
        )
        self.conn.commit()
        return self._one(key)

    def complete(self, key: str, owner: str, result: str = "done") -> dict:
        row = self._one(key)
        if not row or row["lease_owner"] != owner or row["status"] != "leased":
            raise ValueError("complete refused; this owner does not hold the lease")
        self.conn.execute(
            "UPDATE jobs SET status = 'done', result = ?, lease_expires = NULL WHERE idempotency_key = ?",
            (result, key),
        )
        self.conn.commit()
        return self._one(key)

    def lock_inactives(self, game_id: str, now: datetime) -> str:
        stamp = _iso(now)
        self.conn.execute(
            "UPDATE jobs SET inactive_lock = ? WHERE game_id = ?",
            (stamp, game_id),
        )
        self.conn.commit()
        return stamp

    def mark_missed(self, now: datetime) -> list[dict]:
        """A queued job whose deadline has passed is missed. It is not run late."""
        rows = self.conn.execute(
            "SELECT * FROM jobs WHERE status = 'queued' AND deadline IS NOT NULL"
        ).fetchall()
        missed = []
        for row in rows:
            deadline = _parse(row["deadline"])
            if deadline is not None and deadline <= now:
                self.conn.execute(
                    "UPDATE jobs SET status = 'missed', result = 'deadline passed before claim' WHERE idempotency_key = ?",
                    (row["idempotency_key"],),
                )
                missed.append(self._one(row["idempotency_key"]))
        self.conn.commit()
        return missed

    def dispatch(self, handler, now: datetime, owner: str = "local") -> list[dict]:
        """Run due jobs. One handler exception is stored on that job and the next job still runs."""
        outcomes = self.mark_missed(now)
        while True:
            job = self.claim(owner, now)
            if job is None:
                break
            try:
                result = handler(job)
            except Exception as exc:  # noqa: BLE001 — isolation is the contract
                self.conn.execute(
                    "UPDATE jobs SET status = 'failed', result = ? WHERE idempotency_key = ?",
                    (f"{type(exc).__name__}: {exc}", job["idempotency_key"]),
                )
                self.conn.commit()
                outcomes.append(self._one(job["idempotency_key"]))
                continue
            outcomes.append(self.complete(job["idempotency_key"], owner, result=str(result)))
        return outcomes

    def recover_expired(self, now: datetime) -> int:
        rows = self.conn.execute("SELECT idempotency_key, lease_expires FROM jobs WHERE status = 'leased'").fetchall()
        recovered = 0
        for row in rows:
            expires = _parse(row["lease_expires"])
            if expires is not None and expires <= now:
                self.conn.execute(
                    """
                    UPDATE jobs
                       SET status = 'queued', lease_owner = NULL, lease_expires = NULL
                     WHERE idempotency_key = ?
                    """,
                    (row["idempotency_key"],),
                )
                recovered += 1
        self.conn.commit()
        return recovered

    def _lock(self, game_id: str) -> str | None:
        row = self.conn.execute(
            "SELECT inactive_lock FROM jobs WHERE game_id = ? AND inactive_lock IS NOT NULL LIMIT 1",
            (game_id,),
        ).fetchone()
        return row["inactive_lock"] if row else None

    def _one(self, key: str) -> dict | None:
        row = self.conn.execute("SELECT * FROM jobs WHERE idempotency_key = ?", (key,)).fetchone()
        if row is None:
            return None
        body = dict(row)
        body["projection_ready"] = False
        return body
