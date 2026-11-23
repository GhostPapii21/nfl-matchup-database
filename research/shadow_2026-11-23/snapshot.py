"""Save the live stars and the side-by-side candidate for a game, before kickoff (refuses after kickoff).

    python3 research/shadow_2026-11-23/snapshot.py 2026_11_CIN_WAS
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline import freshness  # noqa: E402


def main(gid):
    d = json.loads((ROOT / "dashboard" / "data" / f"{gid}.json").read_text())
    pk = json.loads((ROOT / "pregame" / "packets" / gid / "packet.json").read_text())
    ko, now = freshness.kickoff_utc(pk), datetime.now(timezone.utc)
    if ko and now >= ko:
        raise SystemExit(f"snapshot: refused, {now.isoformat()} is after kickoff {ko.isoformat()}")
    rows = []
    for s in d["sides"].values():
        for p in (s.get("watch") or {}).get("receivers") or []:
            rows.append({"team": s["offense"], "player": p["player"], "p80_live": p["p80"], "stars_live": p["stars"],
                         "stars_model": p.get("stars_model", p["stars"]), "blend": (p.get("book80") or {}).get("blend"),
                         "p80_shadow": (p.get("shadow") or {}).get("p80"), "stars_shadow": (p.get("shadow") or {}).get("stars"),
                         "season_share": (p.get("shadow") or {}).get("season_share"), "last_game_share": (p.get("shadow") or {}).get("last_game_share")})
    out = {"game_id": gid, "saved_utc": now.isoformat(timespec="seconds"), "kickoff_utc": ko.isoformat() if ko else None,
           "board_built_utc": d.get("board_built_utc"), "candidate": "rising role (last game's target share vs season)", "receivers": rows}
    f = Path(__file__).resolve().parent / "live" / f"{gid}.json"
    f.write_text(json.dumps(out, indent=1) + "\n")
    print(f"snapshot: {len(rows)} receivers -> {f.relative_to(ROOT)}")
    for r in sorted(rows, key=lambda r: -r["p80_live"])[:12]:
        print(f"  {r['player']:22} live {r['p80_live']:.3f} ({r['stars_live']}*)  shadow {r['p80_shadow']} ({r['stars_shadow']}*)  share {r['season_share']} -> last {r['last_game_share']}")


if __name__ == "__main__":
    main(sys.argv[1])
