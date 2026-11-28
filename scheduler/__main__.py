"""Local controls: tick, dry-run, replay, status, and a one-shot worker loop.

    python -m scheduler tick --db /tmp/sched.sqlite --slate slate.json --now 2026-11-29T18:00:00Z
    python -m scheduler tick --db /tmp/sched.sqlite --slate slate.json --dry-run
    python -m scheduler replay --db /tmp/sched.sqlite --job 4
    python -m scheduler status --db /tmp/sched.sqlite
    python -m scheduler worker --db /tmp/sched.sqlite --slate slate.json --once

`worker` without `--once` polls until SIGTERM or SIGINT. A Postgres URL is
refused so this process cannot write a Render database before the plan in
docs/automation/SCHEDULER.md is approved.
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
import time

from .orchestrator import Orchestrator, TickResult, open_store
from .sources import games_from_slate, parse_now


def _print_tick(result: TickResult) -> None:
    print(json.dumps({
        "created": result.created,
        "superseded": result.superseded,
        "cancelled": result.cancelled,
        "recovered": result.recovered,
        "missed": result.missed,
        "blocked": result.blocked,
        "backpressure": result.backpressure,
        "ran": result.ran,
    }, indent=2, sort_keys=True))


def _load(path: str):
    with open(path) as handle:
        return json.load(handle)


def _games(args):
    from .sources import games_from_packet_index
    if args.packet_index:
        games, problems = games_from_packet_index(_load(args.packet_index))
        return games, None, problems
    games, expected = games_from_slate(_load(args.slate))
    return games, expected, []


def _cmd_tick(args, once_owner: str = "cli") -> int:
    store = open_store(args.db)
    try:
        orch = Orchestrator(store)
        games, expected, problems = _games(args)
        now = parse_now(args.now)
        if args.dry_run:
            plan = orch.dry_run(games, now, expected)
            plan["rejected_rows"] = [{"game_id": game_id, "message": message} for game_id, message in problems]
            print(json.dumps(plan, indent=2, sort_keys=True, default=str))
            return 0
        for game_id, message in problems:
            orch.store.alert("refused", f"{game_id} schedule row rejected: {message}", game_id or None, now)
        _print_tick(orch.tick(games, now, owner=once_owner, expected_ids=expected))
        return 0
    finally:
        store.close()


def _cmd_replay(args) -> int:
    store = open_store(args.db)
    try:
        orch = Orchestrator(store)
        print(json.dumps(orch.replay(args.job, parse_now(args.now)), indent=2, sort_keys=True))
        return 0
    finally:
        store.close()


def _cmd_status(args) -> int:
    store = open_store(args.db)
    try:
        jobs = store.list_jobs()
        counts: dict[str, int] = {}
        for job in jobs:
            counts[job["status"]] = counts.get(job["status"], 0) + 1
        print(json.dumps({
            "jobs": counts,
            "alerts": store.open_alerts(),
            "refreshes": store.refresh_count(),
        }, indent=2, sort_keys=True))
        return 0
    finally:
        store.close()


def _cmd_worker(args) -> int:
    stop = {"set": False}
    previous = {signal.SIGTERM: signal.getsignal(signal.SIGTERM), signal.SIGINT: signal.getsignal(signal.SIGINT)}

    def _stop(signum, _frame) -> None:
        stop["set"] = True
        print(f"scheduler: signal {signum}; finishing this tick", file=sys.stderr)

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    try:
        while not stop["set"]:
            code = _cmd_tick(args, once_owner="worker")
            if args.once or code != 0 or stop["set"]:
                return code
            time.sleep(args.poll)
        return 0
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m scheduler", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    tick = sub.add_parser("tick", help="discover the slate and run due phases")
    tick.add_argument("--db", required=True)
    source = tick.add_mutually_exclusive_group(required=True)
    source.add_argument("--slate", help="manual slate JSON")
    source.add_argument("--packet-index", help="committed pregame/packets/latest.json shape; no network")
    tick.add_argument("--now", help="ISO instant; default is the current UTC time")
    tick.add_argument("--dry-run", action="store_true")
    tick.set_defaults(func=_cmd_tick)

    replay = sub.add_parser("replay", help="enqueue a new attempt for a finished job")
    replay.add_argument("--db", required=True)
    replay.add_argument("--job", type=int, required=True)
    replay.add_argument("--now")
    replay.set_defaults(func=_cmd_replay)

    status = sub.add_parser("status", help="job counts and open alerts")
    status.add_argument("--db", required=True)
    status.set_defaults(func=_cmd_status)

    worker = sub.add_parser("worker", help="poll a local slate until signalled")
    worker.add_argument("--db", required=True)
    source = worker.add_mutually_exclusive_group(required=True)
    source.add_argument("--slate", help="manual slate JSON")
    source.add_argument("--packet-index", help="committed pregame/packets/latest.json shape; no network")
    worker.add_argument("--now")
    worker.add_argument("--dry-run", action="store_true")
    worker.add_argument("--poll", type=float, default=15)
    worker.add_argument("--once", action="store_true")
    worker.set_defaults(func=_cmd_worker)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"scheduler: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
