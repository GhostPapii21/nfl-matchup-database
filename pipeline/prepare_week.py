"""Weekly: write next week's snapshot-lock inputs so the game-day gate can lock every game before kickoff (NFL-49 P4).

1. data/historical/nflverse/pbp_<season>_w1_<N>_pulled_<ET>.parquet (+ provenance): nflverse play-by-play filtered to
   weeks 1..N, N = the last week whose games are all final (later weeks' plays never reach a lock).
2. core/possession_engine_v0/config/<away>_<home>_<date>_data_only_nfl43.json for every week N+1 game that has a pregame
   packet and no config yet (python -m snapshots.make_configs; model weights unchanged).
Idempotent: an existing pbp file for N and existing configs are left alone.

    python -m pipeline.prepare_week [--season 2026]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PBP_DIR = ROOT / "data" / "historical" / "nflverse"
URL = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{season}.parquet"


def last_full_week(season: int) -> int:
    g = pd.read_parquet(ROOT / "pregame" / ".cache" / "games.parquet")
    g = g[(g.season == season) & (g.game_type == "REG")]
    full = [int(w) for w, x in g.groupby("week") if x.home_score.notna().all()]
    return max(full) if full else 0


def write_pbp(season: int, n: int) -> Path:
    have = sorted(PBP_DIR.glob(f"pbp_{season}_w1_{n}_pulled_*.parquet"))
    if have:
        return have[-1]
    req = urllib.request.Request(URL.format(season=season), headers={"User-Agent": "nfl-matchup-database"})
    raw = urllib.request.urlopen(req, timeout=300).read()
    tmp = ROOT / "pregame" / ".cache" / f"_pbp_{season}_release.parquet"
    tmp.write_bytes(raw)
    p = pd.read_parquet(tmp)
    q = p[p.week <= n]
    ts = datetime.now(ZoneInfo("America/New_York")).strftime("%Y%m%dT%H%MET")
    out = PBP_DIR / f"pbp_{season}_w1_{n}_pulled_{ts}.parquet"
    q.to_parquet(out, index=False)
    prov = {"file": str(out.relative_to(ROOT)), "source_url": URL.format(season=season), "publisher": "nflverse (nflverse-data releases, CC-BY 4.0)",
            "pulled_et": ts, "pulled_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "release_sha256": hashlib.sha256(raw).hexdigest(),
            "release_weeks_present": sorted(int(w) for w in p.week.unique()), "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "season": season, "weeks_present": sorted(int(w) for w in q.week.unique()), "games": int(q.game_id.nunique()),
            "filter": f"week <= {n}", "written_by": "python -m pipeline.prepare_week",
            "note": f"As-of play-by-play for Week {n + 1} snapshot locks (NFL-49 P4). Research only, not validated."}
    out.with_suffix(".provenance.json").write_text(json.dumps(prov, indent=2) + "\n")
    tmp.unlink()
    return out


def write_configs(n_next: int) -> list[str]:
    from snapshots import make_configs as M
    frozen = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%dT%H:%M:%S-05:00")
    made = []
    for p in sorted((ROOT / "pregame" / "packets").glob(f"*_{n_next:02d}_*/packet.json")):
        pk = json.loads(p.read_text())
        g = pk["game"]
        ko = datetime.fromisoformat(f"{g['date']}T{g['kickoff_et']}:00").replace(tzinfo=ZoneInfo("America/New_York"))
        if ko <= datetime.now(ZoneInfo("America/New_York")):
            continue                                    # already kicked off: no lock is possible, no config needed
        c = M.make(pk, frozen)
        out = M.CFG_DIR / f"{c['config_id']}.json"
        if out.exists():
            continue
        out.write_text(json.dumps(c, indent=2) + "\n")
        made.append(str(out.relative_to(ROOT)))
    return made


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", type=int, default=2026)
    a = ap.parse_args(argv)
    n = last_full_week(a.season)
    pbp = write_pbp(a.season, n)
    made = write_configs(n + 1)
    print(f"prepare_week: last full week {n}; as-of pbp {pbp.relative_to(ROOT)}; {len(made)} new Week {n + 1} configs")
    for m in made:
        print("  " + m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
