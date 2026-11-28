-- Proposed production schema for a dedicated NFL scheduler database.
-- DO NOT APPLY. NFL-84 forbids production database writes until the owner
-- approves the plan in docs/automation/SCHEDULER.md.
-- Column names match the SQLite schema the local tests run.
-- The sportsbook-odds-history database is a different application and is not this schema.

CREATE TABLE games (
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

CREATE TABLE jobs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
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

CREATE TABLE receipts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    job_id BIGINT NOT NULL,
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

CREATE TABLE artifacts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    receipt_id BIGINT NOT NULL,
    name TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    body BYTEA NOT NULL
);

CREATE TABLE alerts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    game_id TEXT,
    kind TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL,
    acknowledged INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE refresh_log (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    at_utc TEXT NOT NULL,
    game_count INTEGER NOT NULL,
    created_jobs INTEGER NOT NULL,
    body_json TEXT NOT NULL
);

CREATE INDEX jobs_status_due ON jobs (status, not_before_utc, deadline_utc);
CREATE INDEX jobs_game_phase ON jobs (game_id, phase, schedule_version);
CREATE INDEX alerts_open ON alerts (kind, game_id, acknowledged);
