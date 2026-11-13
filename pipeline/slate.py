"""What the scheduled workflow runs (NFL-56 item 4): for every game in pregame/packets/latest.json, write the
phase ledger and the 100k gate result under pipeline/ledgers/, plus INDEX.md.

    python -m pipeline.slate

A 100k refusal is a recorded result, not a crash: this exits 0 when every game was evaluated and written, and 1 if a
packet could not be read or the index is missing. No network, no API credits.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

from . import phases as PH, sim100k


def main(argv=None) -> int:
    idx_path = PH.PACKETS / "latest.json"
    try:
        games = json.loads(idx_path.read_text())["games"]
    except (OSError, ValueError, KeyError) as e:
        print(f"slate: cannot read {idx_path}: {e}")
        return 1
    PH.LEDGERS.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    rows, failed = [], False
    for g in games:
        gid = g["game_id"]
        try:
            pk = PH.load_packet(gid)
        except (OSError, ValueError) as e:
            print(f"slate: {gid}: packet unreadable: {e}")
            failed = True
            continue
        code, rep = sim100k.run(gid)
        led = PH.ledger(pk, now, gate=rep)
        (PH.LEDGERS / f"{gid}.json").write_text(json.dumps(led, indent=1) + "\n")
        (PH.LEDGERS / f"{gid}.md").write_text(PH.render(led))
        (PH.LEDGERS / f"{gid}.sim100k.json").write_text(json.dumps(rep, indent=1, default=str) + "\n")
        rows.append((g, led, rep))
        print(f"slate: {gid}: phase15 {(led.get('phase15') or {}).get('status')}; phases {led['summary']}; 100k {rep['status']}")
    L = ["# NFL-56 slate ledger", "", f"Checked {now:%Y-%m-%d %H:%M} UTC. Research only; `projection_ready` is false.", "",
         "| Game | Kickoff (ET) | Phase 15 inactives (source, pull time) | Phases | 100k entry point | First refusal reason |",
         "| --- | --- | --- | --- | --- | --- |"]
    for g, led, rep in rows:
        summ = ", ".join(f"{k} {v}" for k, v in led["summary"].items())
        first = (rep.get("reasons") or ["-"])[0].replace("|", "/")
        p15 = led.get("phase15") or {}
        src = ", ".join(f"{t} {u}" for t, u in (p15.get("source_urls") or {}).items() if u) or p15.get("source", "-")
        p15s = f"{p15.get('status', 'MISSING')}; {src}; pulled {p15.get('pull_et') or 'never'}".replace("|", "/")
        L.append(f"| [{g['game_id']}]({g['game_id']}.md) | {g.get('date')} {g.get('kickoff_et')} | {p15s} | {summ} | {rep['status']} | {first} |")
    (PH.LEDGERS / "INDEX.md").write_text("\n".join(L) + "\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
