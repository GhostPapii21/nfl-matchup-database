"""Command line for the Sunday research run.

    python -m sunday preflight --game 2026_12_DEN_PIT --as-of 2026-11-27T04:31:50+00:00
    python -m sunday game --game 2026_12_DEN_PIT --as-of 2026-11-27T04:31:50+00:00
    python -m sunday slate --date 2026-11-29 --as-of 2026-11-29T12:00:00+00:00 --concurrency 4
    python -m sunday replay --game 2026_12_DEN_PIT

Exit 0 when every game wrote a packet and none is BLOCKED (the packet result may still be PARTIAL).
Exit 1 when the arguments or the schedule index cannot be used.
Exit 2 when a game is BLOCKED.
Research only. projection_ready stays false. Full argument notes: docs/SUNDAY_CLI.md.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sunday import discover, execute, preflight, replay
from sunday.preflight import CODE_ROOT


def _common() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo", type=Path, default=CODE_ROOT, help="repository root (default: this checkout)")
    common.add_argument("--out", type=Path, help="directory for JSON and Markdown (default: sunday/runs/ under --repo)")
    common.add_argument("--as-of", dest="as_of", help="UTC timestamp for the pregame cutoff (default: now, or the packet generated time for replay)")
    common.add_argument("--market", action="store_true", help="require a spread or total odds snapshot; missing or stale odds BLOCK the game")
    common.add_argument("--min-free-mb", type=int, default=64, help="minimum free space, in MB, required on the output volume")
    return common


def parser() -> argparse.ArgumentParser:
    common = _common()
    ap = argparse.ArgumentParser(prog="python -m sunday", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pre = sub.add_parser("preflight", parents=[common], help="validate one game and write preflight.json")
    pre.add_argument("--game", required=True, help="schedule game id, for example 2026_12_DEN_PIT")
    game = sub.add_parser("game", parents=[common], help="write one research projection packet")
    game.add_argument("--game", required=True, help="schedule game id, for example 2026_12_DEN_PIT")
    slate = sub.add_parser("slate", parents=[common], help="discover games and run them with bounded concurrency")
    slate.add_argument("--week", type=int, help="limit to this NFL week number")
    slate.add_argument("--date", dest="on_date", help="limit to this calendar date, YYYY-MM-DD")
    slate.add_argument("--slot", help="limit to index rows whose slot text contains this")
    slate.add_argument("--game", action="append", default=[], help="limit to this game id; repeatable; started games are kept")
    slate.add_argument("--concurrency", type=int, default=4, help="maximum in-flight games (capped at 8)")
    slate.add_argument("--include-started", action="store_true", help="keep games whose index kickoff is already at or before as-of")
    slate.add_argument("--all", action="store_true", dest="all_games", help="every game on the schedule index")
    rep = sub.add_parser("replay", parents=[common], help="run one historical game twice and compare the canonical hash")
    rep.add_argument("--game", default="2026_12_DEN_PIT", help="schedule game id (default: 2026_12_DEN_PIT)")
    return ap


def _as_of(args):
    if not args.as_of:
        return execute.now_utc()
    try:
        return preflight.parse_as_of(args.as_of)
    except ValueError as e:
        print(f"sunday: {e}")
        return None


def _entry(repo: Path, game_id: str):
    games, err = discover.load_index(repo)
    if err:
        print(f"sunday: {err}")
        return None, None, 1
    entry = next((g for g in games if g.get("game_id") == game_id), None)
    return games, entry, 0


def _emit_game(packet: dict) -> int:
    wall = (packet.get("runtime") or {}).get("wall_seconds")
    mem = ((packet.get("runtime") or {}).get("memory") or {}).get("detail")
    print(f"sunday: {packet.get('game_id')} {packet.get('result')} wall={wall}s {mem}")
    return execute.exit_code(str(packet.get("result")))


def main(argv=None) -> int:
    ap = parser()
    try:
        args = ap.parse_args(argv)
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
        return 0 if code == 0 else 1
    if args.min_free_mb < 1:
        print("sunday: --min-free-mb must be at least 1")
        return 1
    repo = args.repo
    if args.cmd in {"preflight", "game", "replay"} and not preflight.valid_game_id(args.game):
        print(f"sunday: {args.game!r} is not a schedule game id")
        return 1
    if args.cmd == "replay":
        out = args.out or (repo / "sunday" / "runs" / f"replay_{args.game}")
        override = None
        if args.as_of:
            override = _as_of(args)
            if override is None:
                return 1
        record = replay.run_replay(repo=repo, game_id=args.game, out=out, as_of=override, market=args.market,
                                   min_free_mb=args.min_free_mb)
        print(f"sunday: {record.get('game_id')} {record.get('result')} reproducibility={record.get('reproducibility')}")
        print(f"sunday: replay {out / 'replay.json'}")
        return execute.exit_code(str(record.get("result")))
    as_of = _as_of(args)
    if as_of is None:
        return 1
    if args.cmd == "slate":
        games, err = discover.load_index(repo)
        if err:
            print(f"sunday: {err}")
            return 1
        chosen = discover.select(games, week=args.week, on_date=args.on_date, slot=args.slot, only=args.game,
                                 as_of=as_of, include_started=args.include_started, all_games=args.all_games)
        if not chosen:
            print("sunday: no games matched")
            return 1
        out = args.out or (repo / "sunday" / "runs" / "slate")
        bits = [f"python -m sunday slate --as-of {preflight.iso(as_of)}", f"--concurrency {args.concurrency}"]
        if args.market:
            bits.append("--market")
        if args.week is not None:
            bits.append(f"--week {args.week}")
        if args.on_date:
            bits.append(f"--date {args.on_date}")
        if args.slot:
            bits.append(f"--slot {args.slot}")
        if args.include_started:
            bits.append("--include-started")
        if args.all_games:
            bits.append("--all")
        for gid in args.game:
            bits.append(f"--game {gid}")
        try:
            slate = execute.run_slate(chosen, repo=repo, out=out, as_of=as_of, market=args.market,
                                      min_free_mb=args.min_free_mb, concurrency=args.concurrency,
                                      command=" ".join(bits))
        except ValueError as e:
            print(f"sunday: {e}")
            return 1
        for game in slate["games"]:
            print(f"sunday: {game['game_id']} {game['result']} wall={game.get('wall_seconds')}s")
        counts = slate["counts"]
        print(f"sunday slate: {counts['PASS']} PASS, {counts['PARTIAL']} PARTIAL, {counts['BLOCKED']} BLOCKED")
        print(f"sunday: index {out / 'INDEX.md'}")
        return execute.exit_code(slate["result"])
    _games, entry, code = _entry(repo, args.game)
    if code:
        return code
    out = args.out or (repo / "sunday" / "runs" / args.game)
    command = f"python -m sunday {args.cmd} --game {args.game} --as-of {preflight.iso(as_of)}"
    if args.market:
        command += " --market"
    packet = execute.run_game(repo=repo, game_id=args.game, out_dir=out, as_of=as_of, market=args.market,
                              min_free_mb=args.min_free_mb, entry=entry, measure_memory=True, command=command)
    print(f"sunday: wrote {out / 'report.md'}")
    return _emit_game(packet)


if __name__ == "__main__":
    sys.exit(main())
