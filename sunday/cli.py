"""Local commands for one game and for a slate.

    python -m sunday preflight --game 2026_12_DEN_PIT --as-of 2026-11-27T04:31:50+00:00
    python -m sunday game --game 2026_12_DEN_PIT --as-of 2026-11-27T04:31:50+00:00 --trials 200
    python -m sunday slate --date 2026-11-29 --as-of 2026-11-28T18:00:00+00:00 --trials 200
    python -m sunday replay --game 2026_12_DEN_PIT --trials 200

Research only. projection_ready stays false. No network and no 100k gate execution.
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sunday.context import ROOT, load_packet, schedule_games
from sunday.jsonutil import jsonify, write_json
from sunday.runner import execute_game, preflight_only, run_isolated


def _command(argv: list[str] | None) -> str:
    args = list(sys.argv[1:] if argv is None else argv)
    return "python -m sunday " + " ".join(shlex.quote(a) for a in args)


def _as_of_replay(game_id: str) -> str:
    _path, packet, err = load_packet(game_id)
    if packet is None:
        raise SystemExit(f"replay: {err}")
    stamp = packet.get("generated_utc")
    if not stamp:
        raise SystemExit(f"replay: packet for {game_id} has no generated_utc")
    return str(stamp)


def _specs(games: list[dict], args, command: str, run_id: str) -> list[dict]:
    out = str(args.out) if args.out else str(ROOT / "sunday_runs" / run_id)
    as_of = args.as_of
    specs = []
    for game in games:
        specs.append({
            "game_id": game["game_id"] if isinstance(game, dict) else game,
            "as_of": as_of,
            "trials": args.trials,
            "out": out,
            "threads": args.threads,
            "run_id": run_id,
            "command": command,
        })
    return specs


def _print_results(results: list[dict]) -> int:
    exit_code = 0
    for row in results:
        print(f"{row.get('game_id')}: {row.get('status')} manifest={row.get('manifest')}")
        if row.get("error"):
            print(f"  error: {row['error']}")
        if row.get("critical"):
            for item in row["critical"]:
                print(f"  critical: {item}")
        exit_code = max(exit_code, int(row.get("exit") or 0))
    return exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m sunday", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_common(cmd):
        cmd.add_argument("--as-of", help="ISO-8601 timestamp. Must be before kickoff for a prediction.")
        cmd.add_argument("--trials", type=int, default=200, help="Research trials per executed engine (1-20000). Not the gated 100k.")
        cmd.add_argument("--out", type=Path, help="Run directory. Default sunday_runs/<run_id>.")
        cmd.add_argument("--threads", type=int, default=4, help="Concurrent components inside one game.")

    pre = sub.add_parser("preflight", help="Check identity, as-of leakage, freshness, and the 100k gate. No simulator.")
    pre.add_argument("--game")
    pre.add_argument("--date", help="Slate date YYYY-MM-DD from the local schedule.")
    pre.add_argument("--as-of")
    game = sub.add_parser("game", help="One game.")
    game.add_argument("--game", required=True)
    add_common(game)
    slate = sub.add_parser("slate", help="Every scheduled game on a date. One failure does not drop the others.")
    slate.add_argument("--date", required=True)
    slate.add_argument("--game-workers", type=int, default=2)
    add_common(slate)
    replay = sub.add_parser("replay", help="Historical pregame replay. As-of defaults to the packet generated_utc.")
    replay.add_argument("--game", default="2026_12_DEN_PIT")
    add_common(replay)

    args = parser.parse_args(argv)
    command = _command(argv)
    if args.cmd == "replay" and not args.as_of:
        args.as_of = _as_of_replay(args.game)
    if args.cmd != "preflight" and not args.as_of:
        args.as_of = datetime.now(timezone.utc).isoformat()

    if args.cmd == "preflight":
        if args.game:
            rows = schedule_games(game_id=args.game) or [{"game_id": args.game}]
        elif args.date:
            rows = schedule_games(on_date=args.date)
            if not rows:
                print(f"preflight: no scheduled games on {args.date}")
                return 2
        else:
            print("preflight: pass --game or --date")
            return 2
        exit_code = 0
        reports = []
        for row in rows:
            report = preflight_only({
                "game_id": row["game_id"],
                "as_of": args.as_of or datetime.now(timezone.utc).isoformat(),
                "trials": 1,
                "command": command,
            })
            reports.append(report)
            print(json.dumps(jsonify(report), indent=1))
            exit_code = max(exit_code, report["exit"])
        return exit_code

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8]
    if args.cmd == "game":
        games = [{"game_id": args.game}]
        workers = 1
    elif args.cmd == "replay":
        games = [{"game_id": args.game}]
        workers = 1
    else:
        games = schedule_games(on_date=args.date)
        if not games:
            print(f"slate: no scheduled games on {args.date}")
            return 2
        workers = args.game_workers
    specs = _specs(games, args, command, run_id)
    results = run_isolated(specs, worker=execute_game, max_workers=workers)
    out = Path(specs[0]["out"])
    slate_body = {
        "schema": "sunday-slate/1",
        "run_id": run_id,
        "command": command,
        "projection_ready": False,
        "research_only": True,
        "games": results,
    }
    write_json(out / "slate.json", slate_body)
    return _print_results(results)


if __name__ == "__main__":
    raise SystemExit(main())
