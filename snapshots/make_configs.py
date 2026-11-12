"""Write frozen data_only + NFL-43 configs for a week's games from the pregame packets (no network).

    python3 -m snapshots.make_configs --week 10 --weekdays Sunday,Monday
Same settings as the WAS@NYG TNF config; only teams, kickoff and seed differ. Model weights unchanged.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG_DIR = ROOT / "core/possession_engine_v0/config"
TEMPLATE = CFG_DIR / "was_nyg_2026-11-12_data_only_nfl43.json"


def make(packet: dict, frozen_at_et: str) -> dict:
    g = packet["game"]
    t = json.loads(TEMPLATE.read_text())
    wk = int(g["week"])
    cid = f"{g['away'].lower()}_{g['home'].lower()}_{g['date']}_data_only_nfl43"
    t.update(config_id=cid, frozen_at_et=frozen_at_et, seed_base=int(g["date"].replace("-", "")))
    t["game"] = {"home": g["home"], "away": g["away"], "season": int(g["season"]), "week_asof_exclusive": wk,
                 "kickoff_et": f"{g['date']}T{g['kickoff_et']}:00-05:00", "game_id": g["game_id"]}
    t["history"]["teams"] = sorted([g["home"], g["away"]])
    t["history"]["weeks_inclusive"] = list(range(1, wk))
    return t


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--weekdays", default="Sunday,Monday")
    ap.add_argument("--frozen-at-et", required=True)
    a = ap.parse_args(argv)
    days = set(a.weekdays.split(","))
    for p in sorted((ROOT / "pregame/packets").glob(f"*_{a.week:02d}_*/packet.json")):
        pk = json.loads(p.read_text())
        if pk["game"]["weekday"] not in days:
            continue
        c = make(pk, a.frozen_at_et)
        out = CFG_DIR / f"{c['config_id']}.json"
        out.write_text(json.dumps(c, indent=2) + "\n")
        print(out.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
