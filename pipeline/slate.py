"""What the scheduled workflows run (NFL-56 item 4): write the phase ledger and the 100k gate result for games in
pregame/packets/latest.json under pipeline/ledgers/, plus INDEX.md.

    python -m pipeline.slate                                  # every game: run the gate, write ledgers and the index
    python -m pipeline.slate --game 2026_10_PIT_CIN           # only this game (repeatable); the index is not rewritten
    python -m pipeline.slate --game G --from-report           # ledger from the existing <G>.sim100k.json (no second run)
    python -m pipeline.slate --expect 2026_10_PIT_CIN         # exit 2 unless 100k RAN for every expected game
    python -m pipeline.slate --index-only                     # rebuild INDEX.md from the ledger files on disk

Exit codes (a refusal is still a recorded result, never hidden, but it is no longer reported as success):
  0  every requested game was evaluated and written, and every --expect game has a 100k that RAN
  1  a packet could not be read or the slate index is missing
  2  an --expect game was refused (or is missing)
The last line printed is always the count: "slate: N of M games have a 100k that ran; K refused".

A 100k that already RAN for a game is kept: a later check (after kickoff the gate always refuses) never overwrites it.
No network, no API credits.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

from . import phases as PH, sim100k

RAN = "RAN_RESEARCH_ONLY"


def _existing(gid: str) -> dict | None:
    try:
        return json.loads((PH.LEDGERS / f"{gid}.sim100k.json").read_text())
    except (OSError, ValueError):
        return None


def _write(gid: str, pk: dict, rep: dict, now: datetime) -> dict:
    led = PH.ledger(pk, now, gate=rep)
    (PH.LEDGERS / f"{gid}.json").write_text(json.dumps(led, indent=1) + "\n")
    (PH.LEDGERS / f"{gid}.md").write_text(PH.render(led))
    return led


def write_index(games: list[dict], now: datetime) -> tuple[int, int]:
    """INDEX.md from the ledger files on disk. Returns (ran, refused)."""
    L = ["# NFL-56 slate ledger", "", f"Checked {now:%Y-%m-%d %H:%M} UTC. Research only; `projection_ready` is false.", ""]
    body, ran, refused = [], 0, 0
    for g in games:
        gid = g["game_id"]
        rep = _existing(gid)
        try:
            led = json.loads((PH.LEDGERS / f"{gid}.json").read_text())
        except (OSError, ValueError):
            led = None
        if rep is None or led is None:
            body.append(f"| {gid} | {g.get('date')} {g.get('kickoff_et')} | - | no ledger yet | NOT_CHECKED | - |")
            continue
        ran += rep.get("status") == RAN
        refused += rep.get("status") != RAN
        summ = ", ".join(f"{k} {v}" for k, v in led["summary"].items())
        first = (rep.get("reasons") or ["-"])[0].replace("|", "/")
        p15 = led.get("phase15") or {}
        src = ", ".join(f"{t} {u}" for t, u in (p15.get("source_urls") or {}).items() if u) or p15.get("source", "-")
        p15s = f"{p15.get('status', 'MISSING')}; {src}; pulled {p15.get('pull_et') or 'never'}".replace("|", "/")
        when = str(rep.get("checked_utc", ""))[:16].replace("T", " ")
        body.append(f"| [{gid}]({gid}.md) | {g.get('date')} {g.get('kickoff_et')} | {p15s} | {summ} | {rep.get('status')} ({when} UTC) | {first} |")
    L += [f"**100k ran for {ran} of {len(games)} games; {refused} refused.**", "",
          "| Game | Kickoff (ET) | Phase 15 inactives (source, pull time) | Phases | 100k entry point (checked) | First refusal reason |",
          "| --- | --- | --- | --- | --- | --- |", *body]
    (PH.LEDGERS / "INDEX.md").write_text("\n".join(L) + "\n")
    return ran, refused


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Phase ledgers and the 100k gate for the slate.")
    ap.add_argument("--game", action="append", default=[], help="only this game id (repeatable); INDEX.md is left alone")
    ap.add_argument("--expect", action="append", default=[], help="game id whose 100k must have RAN (repeatable or comma list)")
    ap.add_argument("--from-report", action="store_true", help="use the existing <game>.sim100k.json instead of running the gate")
    ap.add_argument("--index-only", action="store_true", help="only rebuild INDEX.md from the ledger files")
    a = ap.parse_args(argv)
    expect = [x.strip() for e in a.expect for x in e.split(",") if x.strip()]
    idx_path = PH.PACKETS / "latest.json"
    try:
        games = json.loads(idx_path.read_text())["games"]
    except (OSError, ValueError, KeyError) as e:
        print(f"slate: cannot read {idx_path}: {e}")
        return 1
    PH.LEDGERS.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    failed = False
    todo = [] if a.index_only else [g for g in games if not a.game or g["game_id"] in a.game]
    for g in todo:
        gid = g["game_id"]
        try:
            pk = PH.load_packet(gid)
        except (OSError, ValueError) as e:
            print(f"slate: {gid}: packet unreadable: {e}")
            failed = True
            continue
        old = _existing(gid)
        if a.from_report:
            if old is None:
                print(f"slate: {gid}: no {gid}.sim100k.json to build the ledger from")
                failed = True
                continue
            led = _write(gid, pk, old, now)
            print(f"slate: {gid}: phases {led['summary']}; 100k {old.get('status')} (from the existing report)")
            continue
        if old is not None and old.get("status") == RAN:
            print(f"slate: {gid}: 100k already RAN at {old.get('checked_utc')}; kept (not re-checked)")
            continue
        code, rep = sim100k.run(gid)
        if isinstance(rep.get("result"), dict):
            rep["result"].pop("player_box_trials", None)   # per-trial arrays never go into the JSON report
        led = _write(gid, pk, rep, now)
        (PH.LEDGERS / f"{gid}.sim100k.json").write_text(json.dumps(rep, indent=1, default=str) + "\n")
        print(f"slate: {gid}: phase15 {(led.get('phase15') or {}).get('status')}; phases {led['summary']}; 100k {rep['status']}")
    if a.index_only or not a.game:
        ran, refused = write_index(games, now)
        scope = games
    else:
        scope = [g for g in games if g["game_id"] in a.game]
        reps = [_existing(g["game_id"]) for g in scope]
        ran = sum(1 for r in reps if r and r.get("status") == RAN)
        refused = len(scope) - ran
    missing = [gid for gid in expect if (_existing(gid) or {}).get("status") != RAN]
    for gid in missing:
        rep = _existing(gid) or {}
        print(f"slate: EXPECTED {gid} to run, but it was {rep.get('status', 'NOT_CHECKED')}: "
              + "; ".join(rep.get("reasons") or ["no report"]))
    print(f"slate: {ran} of {len(scope)} games have a 100k that ran; {refused} refused")
    if failed:
        return 1
    return 2 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
