"""Input directory for the restored tools/sim_v6.py (and tools/sim_v6r1.py).

The recovered engine reads `$SIMV6_SRC/play_by_play_2026.parquet` and `$SIMV6_SRC/players.parquet` at import. The
default it names (runs/2026-11-01_shared_src) was never committed. This helper builds that directory from files that
are committed, as symlinks, and sets SIMV6_SRC. It never downloads anything.

    python3 tools/simsrc.py [--pbp <parquet>] [--dir <out dir>]      # prints the directory
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PBP_DEFAULT = ROOT / "data/historical/nflverse/pbp_2026_w1_11_pulled_20261124T1717ET.parquet"
PLAYERS_DEFAULT = ROOT / "data/historical/nflverse/derived_pit/players_slim_shared_src_20261102.parquet"
DIR_DEFAULT = ROOT / "tools" / ".simsrc"   # gitignored


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def prepare(pbp: Path = PBP_DEFAULT, players: Path = PLAYERS_DEFAULT, out: Path = DIR_DEFAULT) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    for name, src in (("play_by_play_2026.parquet", pbp), ("players.parquet", players)):
        if not Path(src).exists():
            raise FileNotFoundError(src)
        link = out / name
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(Path(src).resolve())
    os.environ["SIMV6_SRC"] = str(out)
    return {"dir": str(out), "pbp": str(Path(pbp).resolve().relative_to(ROOT)), "pbp_sha256": sha256(Path(pbp)),
            "players": str(Path(players).resolve().relative_to(ROOT)), "players_sha256": sha256(Path(players))}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pbp", type=Path, default=PBP_DEFAULT)
    ap.add_argument("--players", type=Path, default=PLAYERS_DEFAULT)
    ap.add_argument("--dir", type=Path, default=DIR_DEFAULT)
    a = ap.parse_args()
    print(prepare(a.pbp, a.players, a.dir)["dir"])
