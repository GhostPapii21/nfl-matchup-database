"""Fill official-inactives confirmation into phase15/status/<game>/<player>.json (status only, never numbers).

    python3 -m phase15.status_update --game 2026_10_WAS_NYG --player "Cam Skattebo"
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def update(game: str, player: str, root: Path = ROOT) -> dict:
    sf = root / "phase15/status" / game / (player.split()[-1].lower() + ".json")
    rec = json.loads(sf.read_text())
    files = sorted((root / "phase15/inactives" / game).glob("inactives_*.json"))
    if not files:
        raise SystemExit("no inactives pull yet")
    inv = json.loads(files[-1].read_text())
    t = inv["teams"].get(rec["team"]) or {}
    if t.get("status") != "OK":
        rec["official_inactives"] = {"status": t.get("status", "MISSING"), "pull_file": str(files[-1].relative_to(root)),
                                     "retrieved_utc": inv.get("retrieved_utc"), "reason": t.get("reason")}
        rec["status"] = "NO_DESIGNATION_PENDING_INACTIVES"
    else:
        last = player.split()[-1].lower()
        on = any(last in p["name"].lower() and player.split()[0][0].lower() == p["name"].strip()[0].lower() for p in t["players"])
        rec["official_inactives"] = {"status": "OK", "url": t.get("url"), "published_utc": t.get("published_utc"),
                                     "retrieved_utc": inv.get("retrieved_utc"), "pull_file": str(files[-1].relative_to(root)),
                                     "on_inactives_list": on, "inactives": [p["name"] for p in t["players"]]}
        rec["status"] = "INACTIVE (official inactives)" if on else "ACTIVE (not on official inactives list)"
    sf.write_text(json.dumps(rec, indent=1) + "\n")
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--player", required=True)
    a = ap.parse_args(argv)
    r = update(a.game, a.player)
    print(f"{a.player}: {r['status']}  {r['official_inactives'].get('url')}  retrieved {r['official_inactives'].get('retrieved_utc')}")
    return 0 if r["official_inactives"]["status"] == "OK" else 3


if __name__ == "__main__":
    sys.exit(main())
