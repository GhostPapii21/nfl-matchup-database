# Durable game scheduler (NFL-84)

The production scheduler is a queue of per-game phases, not a GitHub Actions cron and not an HTTP request to a web service. This document is the reviewed plan. Nothing in it has been created on Render.

## What is running today

Workspace `My Workspace` (`tea-darrh017lnhs73eihgr0`), inspected 2026-11-27:

| Resource | Name | Type | Plan | Region | Repo |
| --- | --- | --- | --- | --- | --- |
| `srv-dbebg1lg1s2s73f2hfh0` | sportsbook-odds-bridge-staging | web service | free | virginia | sportsbook-odds-bridge |
| `srv-dbe99r0ae00c73ccd590` | sports-leader-mcp | web service | free | oregon | sports-leader-mcp |
| `srv-darrmogjo6nc7395uba0` | sportsbook-odds-bridge | web service | free | virginia | sportsbook-odds-bridge |
| `dpg-das712npn0mc73f3egq0-a` | sportsbook-odds-history | Postgres | `0.1c-256mb` | virginia | odds history, not this repo |

`list_services` returned those three web services and no cron job, background worker, or private service. `list_workflows` returned no workflows. `list_key_value` returned no Key Value instances. None of the services deploy `nfl-matchup-database`.

`.github/workflows/nfl-gameday-gate.yml` is still in the repo. It is the old path: a 15-minute Actions cron because scheduled jobs on this repo start hours late, with `pipeline.window` deciding which games are inside T-88 to T-40. The owner has said Actions usage is unavailable. This change does not delete or edit that workflow. Cutover is a separate approval.

NFL-82 (the phase inventory) was still in progress when this landed. The scheduler therefore does not call `pipeline.sim100k`, `snapshots.lock`, `pregame.build_packets`, or a publisher. A succeeded job is a scheduler receipt with `analytical_execution: false`. Wiring those commands waits on the inventory and on NFL-83 execution receipts.

## What the local scheduler does

`python -m scheduler` keeps six tables (games, jobs, receipts, artifacts, alerts, refresh log). Tests run them on SQLite. The Postgres DDL in `scheduler/schema_postgres.sql` has the same columns and is not applied.

For each scheduled game it enqueues three phases. Instants are UTC. A naive kickoff is read in `America/New_York`. A time that falls in the spring-forward gap is rejected. A time that occurs twice on the fall-back morning is rejected unless `fold` is 0 or 1.

| Phase | Opens | Closes | Concurrency class |
| --- | --- | --- | --- |
| `injury_refresh` | T-90 | T-40 | light |
| `prekick_lock` | T-70, and only after a validated `injury_refresh.json` for that game and kickoff version | kickoff, exclusive | heavy (`simulation_300k` slot) |
| `postgame_grade` | kickoff+3h, or immediately when the slate says `final` and kickoff has passed | kickoff+36h | light |

T-90 is `pipeline.freshness.INACTIVES_POST_MINUTES_BEFORE_KICKOFF`. T-40 is `pipeline.window.CLOSE_MINUTES`. The lock deadline is the same rule as `snapshots.lock`: a handler is not called at or after kickoff.

Idempotency key: `{game_id}:{phase}:{kickoff_version}`. A second sync in the same window does not insert another row. A kickoff change supersedes queued rows and leaves succeeded rows in place. `postponed` and `cancelled` cancel queued rows and raise an alert. `final` pulls the postgame open time forward without minting a new lock.

A worker claims with compare-and-swap (`status='queued'`), holds a lease, and heartbeats. A second claim while the lease is live gets nothing. When the lease expires the receipt is `crashed` and the job is queued again until `max_attempts`, then `dead`. A late worker whose lease was lost cannot mark the retry succeeded. A queued job whose deadline has passed becomes `missed` and the handler is not called. Replay inserts `{key}:replay:{n}`. Replay of a succeeded lock is refused.

Default caps are 2 jobs in flight and 1 heavy job. The heavy slot is where a 300k-trial run will go once NFL-83 is wired. The default handler refuses the phase. A refused or receipt-only injury refresh does not make the pre-kick lock claimable. The lock runs only after a succeeded injury job stores `injury_refresh.json` naming that game and that schedule version. `recorded` means the scheduler finished its bookkeeping; `succeeded` means the phase work completed. Artifacts over 256 KB are refused: the queue database is not the place for a simulation dump, and object storage is not configured. If `assumed_heavy_seconds` is set and the due heavy queue cannot finish before the earliest deadline at `max_heavy`, an open `backpressure` alert is recorded.

Receipt columns `projection_ready`, `betting_started`, and `publishing_started` are constrained to 0. A handler that reports any of those is refused and the columns stay 0.

```text
python -m scheduler tick --db /tmp/sched.sqlite --slate slate.json --now 2026-11-29T18:00:00Z
python -m scheduler tick --db /tmp/sched.sqlite --slate slate.json --dry-run
python -m scheduler replay --db /tmp/sched.sqlite --job 4
python -m scheduler status --db /tmp/sched.sqlite
python -m scheduler worker --db /tmp/sched.sqlite --slate slate.json --once
```

`--dry-run` plans the tick on a copy of the queue and does not call the handler. `worker` polls until SIGTERM or SIGINT, then finishes the tick it is on. A `postgres://` or `postgresql://` path is refused, so this process cannot write a Render database from this branch.

`--packet-index` reads a committed `pregame/packets/latest.json` file. It does not call ESPN, nflverse, or the packet builder. A kickoff that has not been committed is invisible to that command. A live schedule pull stays unwired for the same reason the analytical phases do: it is a side effect, and NFL-82 has not finished naming the entrypoint.

## Why the other shapes do not fit

| Option | What it gives | Why it is not the scheduler |
| --- | --- | --- |
| GitHub Actions | A cron and a matrix of game jobs | Owner says Actions is unavailable. Observed starts were hours late, which is why the workflow polls every 15 minutes. |
| Cursor / local session | A fine place to run tests | Not an always-on production process. |
| Existing free web services | Three free web services, none for this repo | [Free web services spin down after 15 minutes without inbound traffic](https://render.com/docs/free.md), lose local disk on spin-down, and can be restarted at any time. An inbound HTTP tick is the ephemeral request the issue excludes. They also cannot receive private-network traffic. |
| Render Cron Job | UTC cron, one run at a time, exits when done, 12-hour kill, minimum $1/month | UTC-only. A long Sunday run delays the next tick. One run cannot host overlapping per-game work. It still needs a durable queue somewhere else. |
| Render Key Value | A Redis-compatible broker | No instance exists. The free instance keeps data in memory and drops it on restart. A paid instance starts at $10/month and is unnecessary: the lease table is the queue. |
| Render Workflows | Per-task compute, retries, fan-out. Flex is $0.20 per active CPU-hour and $0.05 per active GB-hour | No workflows exist. Workflows have no native schedule; a cron or worker still has to start them. They do not replace the idempotency, lease, and dead-letter records. Preview environments skip them. Use them later, after approval, if one worker cannot finish the heavy slots before kickoff. |
| cron-job.org (mentioned in `docs/MODEL_REVIEW_2026_W10.md`) | An external ping at an exact minute | That ping is an HTTP request into a service that is not always on. It is not a queue. |
| `sportsbook-odds-history` | A live Postgres on plan `0.1c-256mb` | Different application. This plan does not write to it. |

## Minimum that actually stays up

Render's free tier covers web services, static sites, Postgres, and Key Value only. [Other service types have no free instance](https://render.com/docs/free.md). A free Postgres expires 30 days after creation, has no backups, and is limited to one per workspace.

Prices below are from the [Render pricing page](https://render.com/pricing) retrieved 2026-11-27. Confirm them again before applying anything.

| Piece | Plan | Price | Role |
| --- | --- | --- | --- |
| New Postgres, not the odds database | `0.1c-256mb` (less than 1 CPU, 256 MB, 100 connections) | $6/month | Queue, receipts, alerts. Expandable storage is listed at $0.30/GB; confirm included disk on the plan page. |
| Background worker | `0.5c-512mb` (less than 1 CPU, 512 MB) | $7/month | Always-on `python -m scheduler worker`. Same region as the new database. |
| Cron job | not in the minimum | $0.00016/minute on `0.5c-512mb`, $1/month minimum | Not required. The worker polls. |
| Key Value | not in the minimum | from $10/month paid | Not required. |
| Workflows | not in v1 | flex usage | Later fan-out for 300k trials, triggered by the worker, still recorded in the queue. |

Minimum before tax: **$13/month** for the worker plus a new database, plus storage beyond whatever that database plan includes. The 512 MB worker is the control plane. It is not sized to run 300k-trial simulations for a full slate inside the lock window. Do not turn `analytical_execution` on, and do not raise the heavy cap, until a larger worker (`1c-2g` at $25/month on the same page) or Workflows has been approved and object storage exists for the outputs.

A full Sunday slate is why the cap exists. Sixteen heavy jobs with one slot run one after another. `assess_backpressure` records an alert when the assumed heavy duration cannot fit before the earliest deadline. That alert is the signal to add Workflows or a bigger worker. It is not a reason to drop the lease and run every game at once on a free dyno.

Deploy behavior once the plan is approved, and not before:

- A new database and a new worker, same region. Oregon keeps them off the Virginia odds-bridge network. Do not point `DATABASE_URL` at `sportsbook-odds-history`.
- The worker start command polls the slate source and claims jobs. SIGTERM stops new claims and lets the current tick finish; Render does not kill an in-flight cron to do that, but a worker can.
- Deploys must not use a free web service as the clock. Disk on the worker is ephemeral. The queue lives in Postgres. SQLite on the instance is not an acceptable production store.
- This branch refuses Postgres URLs on purpose. After approval, the follow-up is a driver that uses `scheduler/schema_postgres.sql` and an explicit opt-in. Until that change, production writes are impossible from this command.
- Failure visibility is the `alerts` table (`missing`, `refused`, `missed`, `dead`, `blocked`, `postponed`, `cancelled`, `backpressure`) plus the worker log stream. Render failure notifications cover the process dying. They do not cover a game that was refused inside a healthy process; the alerts table does.
- The proposed Blueprint is `docs/automation/PROPOSED_render_scheduler.yaml`. It is not a root `render.yaml`, and it must not be applied from this change.

## Tests

`python3 -m pytest -q -p no:cacheprovider scheduler/tests` covers a 16-game slate, a duplicate trigger, a delayed trigger inside the window, a missed kickoff, crash then retry, a late owner after recovery, two workers claiming one job, a held lease that a second worker cannot take, Eastern DST (including the ambiguous and missing hours), a kickoff move, a postponement, a final that opens postgame grading, dry-run, replay, the projection/betting guards, missing and refused alerts, heavy-queue backpressure, and the Postgres URL refusal.

`scripts/test_offline.sh` runs that suite with the other offline suites. No network. No Render API calls. No production database writes.
